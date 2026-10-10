$ErrorActionPreference = 'Stop'
$sourceLiteral = 'C:\Users\Stephen\AppData\Local\Temp\stbc3hr1'
$destinationLiteral = 'D:\appdata\Offloaded_C_Temp\2026-10-09\stbc3hr1'
$receiptLiteral = 'D:\Documents\CFA\docs\notes\storage\drive_space_20261009\installer_offload_receipt.json'
$source = (Resolve-Path -LiteralPath $sourceLiteral).ProviderPath.TrimEnd('\')
$expectedSource = [IO.Path]::GetFullPath($sourceLiteral).TrimEnd('\')
$destination = [IO.Path]::GetFullPath($destinationLiteral).TrimEnd('\')
if ($source -cne $expectedSource -or $source -notlike 'C:\Users\Stephen\AppData\Local\Temp\*') { throw 'Unexpected source path.' }
if ($destination -cne 'D:\appdata\Offloaded_C_Temp\2026-10-09\stbc3hr1') { throw 'Unexpected destination path.' }
if ((Get-Item -LiteralPath $source).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Source is a reparse point.' }
$active = @(Get-Process | Where-Object { $_.ProcessName -match '^(msiexec|vs_installer|vs_installershell|vs_setup_bootstrapper)$' -or ($_.Path -and $_.Path.StartsWith($source + '\', [StringComparison]::OrdinalIgnoreCase)) })
if ($active.Count) { throw 'Matching installer is active; no relocation performed.' }
$entries = @(Get-ChildItem -LiteralPath $source -Force -Recurse)
if (@($entries | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw 'Reparse point found; aborting.' }
$files = @($entries | Where-Object { -not $_.PSIsContainer })
if ($files.Count -ne 505 -or ($files | Measure-Object Length -Sum).Sum -ne 2281232236) { throw 'Inventory changed; re-audit required.' }
if (@($files | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-2) }).Count) { throw 'Recently modified installer payload; aborting.' }
$freeBefore = (Get-PSDrive -Name C).Free
New-Item -ItemType Directory -Force -Path $destination | Out-Null
$resolvedDestination = (Resolve-Path -LiteralPath $destination).ProviderPath.TrimEnd('\')
if ($resolvedDestination -cne $destination) { throw 'Destination resolution changed.' }
foreach ($ancestor in @('D:\appdata','D:\appdata\Offloaded_C_Temp','D:\appdata\Offloaded_C_Temp\2026-10-09',$destination)) {
    if ((Get-Item -LiteralPath $ancestor).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Destination includes a reparse point.' }
}
$records = [Collections.Generic.List[object]]::new()
foreach ($file in $files) {
    $relative = $file.FullName.Substring($source.Length + 1)
    $target = [IO.Path]::GetFullPath((Join-Path $destination $relative))
    if (-not $target.StartsWith($destination + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Target escaped archive.' }
    $sourceHash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
    if (Test-Path -LiteralPath $target) {
        if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant() -ne $sourceHash) { throw 'Different file exists in archive.' }
    } else { Copy-Item -LiteralPath $file.FullName -Destination $target }
    if ((Get-Item -LiteralPath $target).Length -ne $file.Length -or (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant() -ne $sourceHash) { throw 'Archive verification failed.' }
    $records.Add([pscustomobject]@{ relativePath=$relative; bytes=$file.Length; sha256=$sourceHash })
}
# Recheck the complete source immediately before the one narrowly scoped removal.
$fresh = @(Get-ChildItem -LiteralPath $source -Force -Recurse)
if (@($fresh | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw 'Source reparse state changed.' }
if (@($fresh | Where-Object { -not $_.PSIsContainer }).Count -ne $records.Count) { throw 'Source inventory changed during copy.' }
foreach ($record in $records) {
    $original = Join-Path $source $record.relativePath
    if ((Get-FileHash -LiteralPath $original -Algorithm SHA256).Hash.ToLowerInvariant() -ne $record.sha256) { throw 'Source changed during copy.' }
}
$receipt = [ordered]@{ recordedAtUTC=[DateTime]::UtcNow.ToString('o'); source=$source; destination=$destination; files=$records.Count; bytes=2281232236; hashesVerified=$true; status='copied_and_verified_source_retained'; freeBytesCBefore=$freeBefore; entries=$records }
$receipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $receiptLiteral -Encoding utf8
if ((Resolve-Path -LiteralPath $source).ProviderPath.TrimEnd('\') -cne $expectedSource) { throw 'Final source resolution mismatch.' }
Remove-Item -LiteralPath $source -Recurse -Force
if (Test-Path -LiteralPath $source) { throw 'Source removal incomplete; archive remains intact.' }
$receipt.status = 'offloaded_and_verified'
$receipt.freeBytesCAfter = (Get-PSDrive -Name C).Free
$receipt.completedAtUTC = [DateTime]::UtcNow.ToString('o')
$receipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $receiptLiteral -Encoding utf8
[pscustomobject]$receipt | Select-Object status,source,destination,files,bytes,hashesVerified,freeBytesCBefore,freeBytesCAfter | ConvertTo-Json
