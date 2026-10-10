param([switch]$Archive)
$ErrorActionPreference = 'Stop'
$taskRoot = [System.IO.Path]::GetFullPath('D:\Documents\CFA')
$taskHere = $PSScriptRoot
$taskReceiptPath = Join-Path $taskHere 'received\intake_receipt.json'
$taskReceipt = Get-Content -LiteralPath $taskReceiptPath -Raw | ConvertFrom-Json
$taskInbox = [System.IO.Path]::GetFullPath((Join-Path $taskRoot 'docs\notes\explorable_world\comfy\references\From Grok'))
$taskProcessed = [System.IO.Path]::GetFullPath((Join-Path $taskInbox 'Processed'))
$taskCleanup = Join-Path $taskHere 'cleanup_receipt.json'
if ($taskReceipt.state -ne 'verified_hash_size_decode_complete_extracted_batch' -or -not $taskReceipt.package_completeness.complete) { throw 'Intake not verified complete.' }
if (Test-Path -LiteralPath $taskCleanup) { throw 'Cleanup receipt exists; inspect before retrying.' }
if (-not (Test-Path -LiteralPath $taskProcessed -PathType Container)) { throw 'Expected Processed directory is missing.' }
$taskPlans = @()
for ($taskPart = 1; $taskPart -le 4; $taskPart++) {
    $taskName = "CUR-DROP-20261009A_part${taskPart}of4"
    $taskSource = [System.IO.Path]::GetFullPath((Join-Path $taskInbox $taskName))
    $taskDestination = [System.IO.Path]::GetFullPath((Join-Path $taskProcessed $taskName))
    if (-not $taskSource.StartsWith($taskInbox + '\', [System.StringComparison]::OrdinalIgnoreCase) -or -not $taskDestination.StartsWith($taskProcessed + '\', [System.StringComparison]::OrdinalIgnoreCase) -or -not $taskDestination.StartsWith($taskRoot + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Exact archive path escaped intended workspace.' }
    if (-not (Test-Path -LiteralPath $taskSource -PathType Container) -or (Test-Path -LiteralPath $taskDestination)) { throw 'Missing source or existing destination; no overwrite allowed.' }
    $taskAll = @(Get-Item -LiteralPath $taskSource) + @(Get-ChildItem -LiteralPath $taskSource -Recurse -Force)
    if (@($taskAll | Where-Object { $_.Attributes -band [System.IO.FileAttributes]::ReparsePoint }).Count) { throw 'Source contains a reparse point.' }
    $taskRows = @($taskReceipt.occurrences | Where-Object part -eq $taskPart)
    if (@($taskAll | Where-Object { -not $_.PSIsContainer }).Count -ne $taskRows.Count) { throw 'Source file count changed.' }
    foreach ($taskRow in $taskRows) {
        $taskFile = [System.IO.Path]::GetFullPath((Join-Path $taskRoot $taskRow.source_path))
        $taskCanonical = [System.IO.Path]::GetFullPath((Join-Path $taskRoot $taskRow.canonical_path))
        if (-not $taskFile.StartsWith($taskSource + '\', [System.StringComparison]::OrdinalIgnoreCase) -or -not $taskCanonical.StartsWith($taskRoot + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Verification file path escaped scope.' }
        foreach ($taskVerify in @($taskFile, $taskCanonical)) {
            if ((Get-Item -LiteralPath $taskVerify).Length -ne $taskRow.bytes -or (Get-FileHash -LiteralPath $taskVerify -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskRow.sha256) { throw "Source/canonical mismatch: $taskVerify" }
        }
    }
    $taskPlans += [pscustomobject]@{ part=$taskPart; source=$taskSource; destination=$taskDestination; file_count=$taskRows.Count; bytes=($taskRows | Measure-Object bytes -Sum).Sum; state='verified_move_planned' }
}
if (-not $Archive) { $taskPlans | ConvertTo-Json -Depth 6; return }
$taskLog = [ordered]@{schema='cfa-verified-folder-archive-v1'; intakeID='CUR-DROP-20261009A'; recordedAtUTC=[DateTime]::UtcNow.ToString('o'); state='in_progress'; verified_intake_receipt=$taskReceiptPath; source_and_canonical_reverified=$true; plans=$taskPlans; moved=@(); deleted_files=@(); approvals_created=@()}
$taskLog | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskCleanup -Encoding utf8
foreach ($taskPlan in $taskPlans) {
    Move-Item -LiteralPath $taskPlan.source -Destination $taskPlan.destination -ErrorAction Stop
    $taskRows = @($taskReceipt.occurrences | Where-Object part -eq $taskPlan.part)
    $taskMovedFiles = @(Get-ChildItem -LiteralPath $taskPlan.destination -Recurse -File -Force)
    if ($taskMovedFiles.Count -ne $taskPlan.file_count -or (Test-Path -LiteralPath $taskPlan.source)) { throw 'Post-move count/location verification failed.' }
    foreach ($taskRow in $taskRows) {
        $taskRelative = [System.IO.Path]::GetRelativePath($taskPlan.source, (Join-Path $taskRoot $taskRow.source_path))
        $taskMovedPath = [System.IO.Path]::GetFullPath((Join-Path $taskPlan.destination $taskRelative))
        if (-not $taskMovedPath.StartsWith($taskPlan.destination + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Post-move path escaped exact destination.' }
        if ((Get-Item -LiteralPath $taskMovedPath).Length -ne $taskRow.bytes -or (Get-FileHash -LiteralPath $taskMovedPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskRow.sha256) { throw 'Post-move bytes differ.' }
    }
    $taskPlan.state = 'moved_and_hash_verified'
    $taskLog.moved += $taskPlan
    $taskLog | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskCleanup -Encoding utf8
}
$taskLog.state = 'complete'
$taskLog.completedAtUTC = [DateTime]::UtcNow.ToString('o')
$taskLog | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskCleanup -Encoding utf8
$taskLog | ConvertTo-Json -Depth 8
