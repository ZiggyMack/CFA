param([string]$EnginePath = (Join-Path $PSScriptRoot '..\..\.cache\godot-4.7.2\Godot_v4.7.2-stable_win64_console.exe'), [switch]$CloudBundle)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $EnginePath)) { throw 'Download the portable Godot engine first; see README.md.' }
$cfaBuildDir = Join-Path $PSScriptRoot 'builds\observatory'
$cfaLocalDir = Join-Path $PSScriptRoot '.local'
New-Item -ItemType Directory -Force -Path $cfaBuildDir, $cfaLocalDir | Out-Null
$env:APPDATA = Join-Path $cfaLocalDir 'osdata'
$env:OBSERVATORY_DATA_DIR = $cfaLocalDir
& $EnginePath --headless --path $PSScriptRoot --export-pack 'Windows Desktop' (Join-Path $cfaBuildDir 'Observatory.pck') --log-file (Join-Path $cfaLocalDir 'pack.log')
if ($LASTEXITCODE -ne 0) { throw 'Godot pack export failed.' }
$cfaGuiEngine = $EnginePath -replace '_console\.exe$', '.exe'
$cfaRuntimePath = Join-Path $cfaBuildDir 'Observatory.exe'
$cfaReuseRuntime = (Test-Path -LiteralPath $cfaRuntimePath) -and ((Get-FileHash -LiteralPath $cfaGuiEngine -Algorithm SHA256).Hash -eq (Get-FileHash -LiteralPath $cfaRuntimePath -Algorithm SHA256).Hash)
if (-not $cfaReuseRuntime) {
    Copy-Item -LiteralPath $cfaGuiEngine -Destination $cfaRuntimePath -Force
}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'GODOT_LICENSE.txt') -Destination $cfaBuildDir -Force
@'
@echo off
setlocal
set "APPDATA=%~dp0user_data\osdata"
set "OBSERVATORY_DATA_DIR=%~dp0user_data"
if not exist "%APPDATA%" mkdir "%APPDATA%"
start "The Observatory" "%~dp0Observatory.exe" --main-pack "%~dp0Observatory.pck" --rendering-method gl_compatibility --log-file "%~dp0user_data\play.log"
'@ | Set-Content -LiteralPath (Join-Path $cfaBuildDir 'Play.cmd') -Encoding ASCII
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'THIRD_PARTY_ASSETS.md') -Destination $cfaBuildDir -Force
@'
@echo off
setlocal
set "APPDATA=%~dp0user_data\osdata"
set "OBSERVATORY_DATA_DIR=%~dp0user_data"
if not exist "%APPDATA%" mkdir "%APPDATA%"
start "The Observatory - High Quality" "%~dp0Observatory.exe" --main-pack "%~dp0Observatory.pck" --rendering-method forward_plus --resolution 1920x1080 --log-file "%~dp0user_data\high-quality.log" -- --high-quality
'@ | Set-Content -LiteralPath (Join-Path $cfaBuildDir 'Play_High_Quality.cmd') -Encoding ASCII
@'
The Observatory: Water Before the Crossing

Double-click Play.cmd to enter. Keep all files in this folder together.
Play_High_Quality.cmd is an untested modern GPU / cloud-PC preset.
It runs on the current computer; it does not connect to a cloud service.
WASD: walk. Mouse or arrows: look. E: interact. Tab: journal. Esc: pause.
Shift: walk faster. M: sound toggle. F3: frame timing display.
Progress saves locally in user_data. Begin a new visit from the pause menu.
Esc > Story workshop compares two writing drafts without resetting your visit.

This is a portable development build: the official Godot 4.7.2 editor binary
runs the packed game directly. No editor UI, account, network, or Comfy session
is needed to play. It is not an optimized release-template export.

Geometry, story, and synthetic ambience are original project work.
Photo materials are CC0 Poly Haven assets; see THIRD_PARTY_ASSETS.md.
The Godot engine is distributed under the included MIT license.
'@ | Set-Content -LiteralPath (Join-Path $cfaBuildDir 'READ_ME.txt') -Encoding ASCII
Write-Output "Portable development build: $cfaBuildDir"

if ($CloudBundle) {
    # Explicit file list: never package user_data, logs, credentials or other CFA files.
    $cfaCloudFiles = @('Observatory.exe', 'Observatory.pck', 'Play.cmd', 'Play_High_Quality.cmd', 'GODOT_LICENSE.txt', 'THIRD_PARTY_ASSETS.md', 'READ_ME.txt')
    $cfaCloudPaths = $cfaCloudFiles | ForEach-Object { Join-Path $cfaBuildDir $_ }
    $cfaZipPath = Join-Path $PSScriptRoot 'builds\Observatory-cloud-test.zip'
    Compress-Archive -LiteralPath $cfaCloudPaths -DestinationPath $cfaZipPath -Force
    Write-Output "Cloud test bundle: $cfaZipPath"
    Get-FileHash -LiteralPath $cfaZipPath -Algorithm SHA256
}
