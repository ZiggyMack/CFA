param([switch]$Execute)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repositoryRoot = [IO.Path]::GetFullPath('D:\Documents\CFA')
$auditRoot = [IO.Path]::GetFullPath((Join-Path $repositoryRoot 'docs\notes\explorable_world\comfy\projects\visual_library\grok_source_relocation_20261012'))
$preferredRoot = [IO.Path]::GetFullPath((Join-Path $repositoryRoot 'docs\notes\explorable_world\comfy\references\From Grok'))
$authorizedSourceRoots = @(
    [IO.Path]::GetFullPath((Join-Path $repositoryRoot 'docs\notes\downloads\GROK-HD-FALCON-1000')),
    [IO.Path]::GetFullPath((Join-Path $repositoryRoot 'docs\notes\downloads\GROK-HD-STORY-SET-02')),
    [IO.Path]::GetFullPath((Join-Path $repositoryRoot 'docs\notes\downloads\GROK-HD-ENABLERS-03'))
)
$planPath = Join-Path $auditRoot 'relocation_map.planned.json'
$activeMapPath = Join-Path $auditRoot 'relocation_map.json'
$journalPath = Join-Path $auditRoot 'transfer_journal.jsonl'
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Extended-Path([string]$path) {
    if ($path.StartsWith('\\?\')) { return $path }
    return '\\?\' + $path
}
function Within-Root([string]$path, [string]$root) {
    return $path.StartsWith($root.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)
}
function Checked-Path([string]$portable, [bool]$source) {
    if ([string]::IsNullOrEmpty($portable) -or $portable -match '[\\%?#:\x00-\x1f\x7f]' -or
        $portable.StartsWith('/') -or ($portable.Split('/') -contains '..') -or
        ($portable.Split('/') -contains '.') -or ($portable.Split('/') -contains '')) {
        throw "Unsafe portable path: $portable"
    }
    $absolute = [IO.Path]::GetFullPath((Join-Path $repositoryRoot ($portable.Replace('/', '\'))))
    if (-not (Within-Root $absolute $repositoryRoot)) { throw "Path escapes CFA: $absolute" }
    if ($source) {
        $inside = $false
        foreach ($scope in $authorizedSourceRoots) { if (Within-Root $absolute $scope) { $inside = $true } }
        if (-not $inside) { throw "Source escapes the three authorized Downloads packages: $absolute" }
    } elseif (-not (Within-Root $absolute $preferredRoot)) {
        throw "Destination escapes From Grok: $absolute"
    }
    $cursor = $absolute
    while ($cursor.Length -ge $repositoryRoot.Length) {
        try {
            $attributes = [IO.File]::GetAttributes((Extended-Path $cursor))
            if (($attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Reparse path is not eligible: $cursor"
            }
        } catch [IO.FileNotFoundException] {
            # A not-yet-created destination ancestor is checked again on transfer.
        } catch [IO.DirectoryNotFoundException] {
            # The intended absolute path still passed the strict root check.
        }
        if ($cursor.Equals($repositoryRoot, [StringComparison]::OrdinalIgnoreCase)) { break }
        $cursor = [IO.Path]::GetDirectoryName($cursor)
    }
    return $absolute
}
function Verified-File([string]$absolute, $entry) {
    $item = Get-Item -LiteralPath (Extended-Path $absolute) -Force
    if ($item.PSIsContainer -or $item.Length -ne [long]$entry.bytes) {
        throw "File type or size differs: $absolute"
    }
    $hash = (Get-FileHash -LiteralPath (Extended-Path $absolute) -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $entry.sha256) { throw "File hash differs: $absolute" }
    return $hash
}
function Journal($record) {
    [IO.File]::AppendAllText($journalPath, (($record | ConvertTo-Json -Compress -Depth 8) + "`n"), $utf8)
}

if ((Get-FileHash -LiteralPath $planPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne
    '501a38055140d9f0e0fc180721d2850ad1f1118b969b243333875135b9eee1a3') {
    throw 'The independently verified planned map changed.'
}
if (Test-Path -LiteralPath $activeMapPath) { throw 'An active map already exists; audit rather than repeat.' }
$plan = Get-Content -LiteralPath $planPath -Raw | ConvertFrom-Json -AsHashtable
if ($plan.state -ne 'planned' -or $plan.schemaVersion -ne 1 -or $plan.entries.Count -ne 2774 -or
    $plan.destinationRoot -ne 'docs/notes/explorable_world/comfy/references/From Grok') {
    throw 'Unexpected planned relocation scope.'
}
$rows = New-Object System.Collections.Generic.List[object]
$seenSources = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
$moveCount = 0
$reuseCount = 0
$preflightCount = 0
foreach ($entry in $plan.entries) {
    $source = Checked-Path $entry.originalRepoPath $true
    $destination = Checked-Path $entry.physicalRepoPath $false
    if (-not $seenSources.Add($source)) { throw "Duplicate source: $source" }
    $null = Verified-File $source $entry
    if ($entry.action -eq 'move_unique') {
        if (Test-Path -LiteralPath (Extended-Path $destination)) { throw "Unique destination already exists: $destination" }
        $moveCount++
    } elseif ($entry.action -eq 'reuse_verified_preferred') {
        $null = Verified-File $destination $entry
        $reuseCount++
    } else { throw "Unexpected action: $($entry.action)" }
    $rows.Add([pscustomobject]@{ entry = $entry; source = $source; destination = $destination })
    $preflightCount++
    if (($preflightCount % 500) -eq 0) { Write-Output "Preflight verified $preflightCount / 2774 sources and destinations." }
}
if ($moveCount -ne 2582 -or $reuseCount -ne 192) { throw 'Action counts differ from the verified plan.' }
Write-Output "Preflight passed: 2774 files; 2582 moves; 192 exact preferred duplicates."
if (-not $Execute) {
    Write-Output 'No transfers performed. Execute switch requires Root GO after integration review.'
    exit 0
}

$startedAt = [DateTime]::UtcNow.ToString('o')
Journal @{ event = 'started'; timestamp = $startedAt; planSHA256 = '501a38055140d9f0e0fc180721d2850ad1f1118b969b243333875135b9eee1a3'; files = 2774 }
$completed = 0
foreach ($row in $rows) {
    $entry = $row.entry
    $source = Checked-Path $entry.originalRepoPath $true
    $destination = Checked-Path $entry.physicalRepoPath $false
    $null = Verified-File $source $entry
    Journal @{ event = 'before'; originalRepoPath = $entry.originalRepoPath; physicalRepoPath = $entry.physicalRepoPath; action = $entry.action; sha256 = $entry.sha256; bytes = $entry.bytes; timestamp = [DateTime]::UtcNow.ToString('o') }
    if ($entry.action -eq 'move_unique') {
        if (Test-Path -LiteralPath (Extended-Path $destination)) { throw "Destination appeared after preflight: $destination" }
        $directory = [IO.Path]::GetDirectoryName($destination)
        $null = New-Item -ItemType Directory -Path (Extended-Path $directory) -Force
        $null = Checked-Path $entry.physicalRepoPath $false
        Move-Item -LiteralPath (Extended-Path $source) -Destination (Extended-Path $destination)
        $null = Verified-File $destination $entry
    } else {
        # Read back the exact preferred counterpart immediately before removing
        # only the verified duplicate source. No recursive deletion is used.
        $null = Verified-File $destination $entry
        Remove-Item -LiteralPath (Extended-Path $source)
        $null = Verified-File $destination $entry
    }
    if (Test-Path -LiteralPath (Extended-Path $source)) { throw "Transferred source still exists: $source" }
    Journal @{ event = 'completed'; originalRepoPath = $entry.originalRepoPath; physicalRepoPath = $entry.physicalRepoPath; action = $entry.action; sha256 = $entry.sha256; bytes = $entry.bytes; timestamp = [DateTime]::UtcNow.ToString('o') }
    $completed++
    if (($completed % 250) -eq 0) { Write-Output "Verified $completed / 2774 transferred files." }
}
# Activate only after a complete independent destination hash readback.
foreach ($row in $rows) {
    $destination = Checked-Path $row.entry.physicalRepoPath $false
    $null = Verified-File $destination $row.entry
    if (Test-Path -LiteralPath (Extended-Path $row.source)) { throw "Old source remains: $($row.source)" }
}
$finishedAt = [DateTime]::UtcNow.ToString('o')
$plan.state = 'active'
$plan['activatedAt'] = $finishedAt
$plan['transferStartedAt'] = $startedAt
$plan['plannedMapSHA256'] = '501a38055140d9f0e0fc180721d2850ad1f1118b969b243333875135b9eee1a3'
$plan['sourceCopiesCleared'] = 2774
$plan['transferJournalRepoPath'] = 'docs/notes/explorable_world/comfy/projects/visual_library/grok_source_relocation_20261012/transfer_journal.jsonl'
$temporaryMap = Join-Path $auditRoot 'relocation_map.active.tmp'
[IO.File]::WriteAllText($temporaryMap, (($plan | ConvertTo-Json -Depth 15) + "`n"), $utf8)
Move-Item -LiteralPath $temporaryMap -Destination $activeMapPath
Journal @{ event = 'activated'; timestamp = $finishedAt; activeMapSHA256 = (Get-FileHash -LiteralPath $activeMapPath -Algorithm SHA256).Hash.ToLowerInvariant(); moves = 2582; duplicatesCleared = 192; destinationsVerified = 2774 }
Write-Output "Relocation complete: 2582 moved, 192 verified duplicate source copies cleared; 2774 destinations rehashed; map active."
