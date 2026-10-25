# ERPNext Armenian v16 - Windows launcher (run from the docker folder)
$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
function Info($m){ Write-Host "[ERPNext-hy] $m" -ForegroundColor Cyan }
function Fail($m){ Write-Host "[ERPNext-hy] $m" -ForegroundColor Red; Read-Host "Press Enter to close"; exit 1 }

Info "Checking Docker Desktop..."
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  Fail "Docker Desktop is not installed. Install it from https://www.docker.com/products/docker-desktop/ (WSL 2 backend), restart Windows, then run this again."
}
$ok = $false
for ($i=0; $i -lt 3; $i++) { docker info *> $null; if ($LASTEXITCODE -eq 0) { $ok = $true; break }
  if ($i -eq 0) { Info "Starting Docker Desktop..."; $dd = "$Env:ProgramFiles\Docker\Docker\Docker Desktop.exe"; if (Test-Path $dd) { Start-Process $dd } }
  Start-Sleep -Seconds 40 }
if (-not $ok) { Fail "Docker Desktop is not running. Open Docker Desktop, wait until it says 'Engine running', then run this again." }

$logDir = Join-Path (Get-Location) "logs"; New-Item -ItemType Directory -Force $logDir | Out-Null
$img = docker images -q erpnext-armenian:v16
if (-not $img -or $args -contains "--rebuild") {
  Info "Building image (first time: 20-40 minutes, downloads ~3 GB). Log: logs\build.log"
  docker compose build backend 2>&1 | Tee-Object -FilePath "$logDir\build.log"
  if ($LASTEXITCODE -ne 0) { Fail "Build failed. Open an issue on GitHub and attach logs\build.log." }
}

Info "Starting containers..."
docker compose up -d 2>&1 | Tee-Object -FilePath "$logDir\up.log"
if ($LASTEXITCODE -ne 0) { Fail "docker compose up failed. Attach logs\up.log to a GitHub issue." }


Info "Waiting for site setup (first time: 5-15 minutes)..."
$deadline = (Get-Date).AddMinutes(30)
while ((Get-Date) -lt $deadline) {
  $state = docker compose ps -a --format "{{.Service}} {{.State}} {{.ExitCode}}" create-site
  if ($state -match "exited 0") { break }
  if ($state -match "exited [1-9]") { docker compose logs create-site > "$logDir\create-site.log"
Fail "Site creation failed. Attach logs\create-site.log to a GitHub issue." }
  Start-Sleep -Seconds 10; Write-Host -NoNewline "."
}
Write-Host ""
for ($i=0; $i -lt 60; $i++) {
  try { $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 5 http://localhost:8080/login; if ($r.StatusCode -eq 200) { break } } catch {}
  Start-Sleep -Seconds 5
}
# Sites created by older packages: make sure the erpnext_armenian app is installed, then refresh caches.
Info "Checking the Armenian translation app..."
$apps = docker compose exec -T backend bench --site frontend list-apps 2>$null
if (-not ($apps -match "erpnext_armenian")) {
  docker compose exec -T backend bench --site frontend install-app erpnext_armenian 2>&1 | Tee-Object -FilePath "$logDir\install-app.log"
}
docker compose exec -T backend bench --site frontend migrate 2>&1 | Out-File "$logDir\migrate.log"
docker compose exec -T backend bench --site frontend clear-cache | Out-Null
docker compose logs create-site > "$logDir\create-site.log"
Info "Ready:  http://localhost:8080   user: Administrator   password: admin"
Info "In the setup wizard choose language: Հայերեն, country: Armenia, currency: AMD."
Start-Process "http://localhost:8080"
Read-Host "Press Enter to close this window (ERPNext keeps running; use STOP.bat to stop it)"
