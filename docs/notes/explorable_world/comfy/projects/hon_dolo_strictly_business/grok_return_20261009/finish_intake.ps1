$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath('D:\Documents\CFA')
$inbox = [IO.Path]::GetFullPath((Join-Path $repoRoot 'docs\notes\explorable_world\comfy\references\From Grok'))
$processed = [IO.Path]::GetFullPath((Join-Path $inbox 'Processed'))
$intake = $PSScriptRoot
$receipt = Get-Content -LiteralPath (Join-Path $intake 'received\intake_receipt.json') -Raw | ConvertFrom-Json
$ledger = Get-Content -LiteralPath (Join-Path $intake 'asset_ledger.json') -Raw | ConvertFrom-Json
if ($receipt.state -ne 'verified_crc_hash_size_decode') { throw 'Unverified intake' }
if ((Get-FileHash -LiteralPath (Join-Path $intake 'received\intake_receipt.json') -Algorithm SHA256).Hash.ToLower() -ne $ledger.receiptSHA256) { throw 'Receipt changed' }
$cleanupPath = Join-Path $intake 'cleanup_receipt.json'
if (Test-Path -LiteralPath $cleanupPath) { throw 'Cleanup already has a receipt; inspect it before retrying.' }
foreach ($file in $receipt.unique_files) {
    $path = [IO.Path]::GetFullPath((Join-Path $repoRoot $file.canonical_path))
    if (-not $path.StartsWith($repoRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Canonical path outside repository' }
    if ((Get-Item -LiteralPath $path).Length -ne $file.bytes -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower() -ne $file.sha256) { throw "Canonical bytes differ: $path" }
}
$archives = @()
foreach ($archive in $receipt.archives) {
    $path = [IO.Path]::GetFullPath((Join-Path $repoRoot $archive.source_path))
    if (-not $path.StartsWith($inbox + '\', [StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetExtension($path) -ne '.zip') { throw 'Archive deletion target outside named inbox' }
    if ((Get-Item -LiteralPath $path).Length -ne $archive.bytes -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower() -ne $archive.sha256) { throw "Archive bytes differ: $path" }
    $archives += [ordered]@{ path=$path; sha256=$archive.sha256; bytes=$archive.bytes; deleted=$false }
}
$names = @('GROK-HD-MASTER-20261009_part1of2','GROK-HD-MASTER-20261009_part2of2','NOVA-GUIDE-500.md')
1..8 | ForEach-Object { $names += ('LAG-500-MASTER-part{0:D2}' -f $_) }
$moves = @()
foreach ($name in $names) {
    $source = [IO.Path]::GetFullPath((Join-Path $inbox $name))
    $destination = [IO.Path]::GetFullPath((Join-Path $processed $name))
    if ([IO.Path]::GetDirectoryName($source) -ne $inbox -or [IO.Path]::GetDirectoryName($destination) -ne $processed) { throw 'Move escapes intended directories' }
    if (-not (Test-Path -LiteralPath $source)) { throw "Move source missing: $source" }
    if (Test-Path -LiteralPath $destination) { throw "Destination exists: $destination" }
    $moves += [ordered]@{ source=$source; destination=$destination; moved=$false }
}
$result = [ordered]@{ schema='grok-return-cleanup-v1'; startedAtUTC=[DateTime]::UtcNow.ToString('o'); state='verified_ready'; authorization='User requested verified extraction followed by ZIP removal, and moving processed incoming batches into Processed.'; canonicalFilesVerified=$receipt.unique_files.Count; archiveBytesFreed=0; archives=$archives; moves=$moves }
function Save-Receipt { $result | ConvertTo-Json -Depth 9 | Set-Content -LiteralPath $cleanupPath -Encoding utf8 }
Save-Receipt
foreach ($archive in $archives) {
    Remove-Item -LiteralPath $archive.path
    $archive.deleted=$true
    $result.archiveBytesFreed += $archive.bytes
    Save-Receipt
}
foreach ($move in $moves) {
    Move-Item -LiteralPath $move.source -Destination $move.destination
    if (-not (Test-Path -LiteralPath $move.destination) -or (Test-Path -LiteralPath $move.source)) { throw 'Move did not finish' }
    $move.moved=$true
    Save-Receipt
}
foreach ($file in $receipt.unique_files) {
    $path = Join-Path $repoRoot $file.canonical_path
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower() -ne $file.sha256) { throw 'Canonical bytes changed after cleanup' }
}
$result.state='complete'
$result.completedAtUTC=[DateTime]::UtcNow.ToString('o')
Save-Receipt
[pscustomobject]@{ state=$result.state; canonicalFilesVerified=$result.canonicalFilesVerified; archiveBytesFreed=$result.archiveBytesFreed } | ConvertTo-Json
