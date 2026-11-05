$os = Get-CimInstance Win32_OperatingSystem
Write-Output ('Edition: ' + $os.Caption)

$rdp = Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections -ErrorAction SilentlyContinue
Write-Output ('fDenyTSConnections (0=enabled, 1=disabled): ' + $rdp.fDenyTSConnections)

$nla = Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name UserAuthentication -ErrorAction SilentlyContinue
Write-Output ('NLA UserAuthentication (1=required): ' + $nla.UserAuthentication)

$svc = Get-Service TermService
Write-Output ('TermService: ' + $svc.Status + ' / ' + $svc.StartType)

$listen = netstat -ano | Select-String ':3389'
if ($listen) { Write-Output ('Listening 3389: ' + $listen[0].ToString().Trim()) } else { Write-Output 'Listening 3389: NO' }

Write-Output 'Firewall rules (Remote Desktop group):'
$fw = Get-NetFirewallRule -DisplayGroup 'Remote Desktop' -ErrorAction SilentlyContinue | Select-Object DisplayName, Enabled, Profile
if ($fw) { $fw | ForEach-Object { Write-Output ('  ' + $_.DisplayName + ' | Enabled=' + $_.Enabled + ' | Profile=' + $_.Profile) } } else { Write-Output '  (none found)' }

Get-NetConnectionProfile | ForEach-Object { Write-Output ('Network: ' + $_.Name + ' | Category=' + $_.NetworkCategory) }

$sleep = powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE | Select-String 'Current AC Power Setting Index'
Write-Output ('Sleep on AC: ' + ($sleep -replace '.*:\s*','') + ' (0 = never)')

Write-Output ('Last boot: ' + $os.LastBootUpTime)
Write-Output ('Logged-on console user: ' + (quser 2>$null | Out-String).Trim())
