# Claude 영상 제작 오픈소스 7개 - Windows 설치 스크립트
# 실행: install-windows.bat 더블클릭 (또는 PowerShell에서 .\setup-windows.ps1)

$ErrorActionPreference = "Continue"
$Root  = Join-Path $HOME "ClaudeVideo"
$Repos = Join-Path $Root "repos"

function Step($msg) { Write-Host "`n=== $msg ===" -ForegroundColor Green }
function Has($cmd)  { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function RefreshPath {
    $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
                [Environment]::GetEnvironmentVariable("Path","User")
}
function WingetInstall($id, $cmd) {
    if ($cmd -and (Has $cmd)) { Write-Host "  [있음] $cmd"; return }
    Write-Host "  [설치] $id"
    winget install --id $id -e --accept-source-agreements --accept-package-agreements --silent
    RefreshPath
}

Step "1. 필수 도구 설치 (Git, Node.js, Python, ffmpeg, Chrome, Bun)"
if (-not (Has winget)) {
    Write-Host "winget이 없습니다. Microsoft Store에서 '앱 설치 관리자(App Installer)'를 설치한 뒤 다시 실행하세요." -ForegroundColor Red
    exit 1
}
WingetInstall "Git.Git"             "git"
WingetInstall "OpenJS.NodeJS.LTS"   "node"
WingetInstall "Python.Python.3.12"  "python"
WingetInstall "Gyan.FFmpeg"         "ffmpeg"
WingetInstall "Oven-sh.Bun"         "bun"
if (-not (Test-Path "$env:ProgramFiles\Google\Chrome\Application\chrome.exe") -and
    -not (Test-Path "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe") -and
    -not (Test-Path "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe")) {
    WingetInstall "Google.Chrome" $null
} else { Write-Host "  [있음] Chrome" }

Step "2. 버전 확인"
foreach ($c in "git","node","python","ffmpeg","bun") {
    if (Has $c) {
        $v = if ($c -eq "ffmpeg") { (& ffmpeg -version 2>$null | Select-Object -First 1) } else { (& $c --version 2>$null | Select-Object -First 1) }
        Write-Host ("  {0,-7} {1}" -f $c, $v)
    } else { Write-Host "  $c : 설치 후 새 터미널에서 다시 확인 필요" -ForegroundColor Yellow }
}

Step "3. 오픈소스 7개 내려받기 -> $Repos"
New-Item -ItemType Directory -Force -Path $Repos | Out-Null
$list = @(
    "yihui-dev/awesome-opus5-5-videos",     # 01 사례집 (프롬프트 703개)
    "lemomo-ai/lemo-opuscar",               # 02 스킬 (스타일 99개) - 플러그인으로도 설치
    "mexicat/pdoom-video",                  # 03 가사 싱크 뮤비 예제
    "Vincentwei1021/mg-styles-15",          # 04 모션그래픽 스타일 15개
    "JohnHeibel/ClaudeAnimationBase",       # 05 손그림 애니 스타터
    "athemeroy/awesome-claude-5-5-videos",  # 06 사례 424개
    "joeseesun/opus-video-prompts"          # 07 중국어 프롬프트 18개
)
foreach ($r in $list) {
    $name = $r.Split("/")[1]
    $dst  = Join-Path $Repos $name
    if (Test-Path (Join-Path $dst ".git")) {
        Write-Host "  [업데이트] $name"; git -C $dst pull --ff-only
    } else {
        Write-Host "  [받기] $name"; git clone --depth 1 "https://github.com/$r.git" $dst
    }
}

Step "4. 실행형 프로젝트 의존성 설치"
$cab = Join-Path $Repos "ClaudeAnimationBase"
if ((Test-Path $cab) -and (Has npm)) { Push-Location $cab; npm install; Pop-Location }
$pd = Join-Path $Repos "pdoom-video\app"
if ((Test-Path $pd) -and (Has bun)) { Push-Location $pd; bun install; Pop-Location }

Step "5. Lemo Opuscar 플러그인 (Claude Code)"
if (Has claude) {
    claude plugin marketplace add lemomo-ai/lemo-opuscar
    claude plugin install lemo-opuscar@lemolab
} else {
    Write-Host "  'claude' 명령이 없습니다. Claude Code 설치 후 아래 두 줄을 실행하세요:" -ForegroundColor Yellow
    Write-Host "    claude plugin marketplace add lemomo-ai/lemo-opuscar"
    Write-Host "    claude plugin install lemo-opuscar@lemolab"
}

Step "6. 첫 영상용 빈 작업 폴더"
$proj = Join-Path $Root "projects\첫영상"
New-Item -ItemType Directory -Force -Path $proj | Out-Null
Write-Host "  $proj"

Write-Host "`n완료! 새 터미널을 열고 작업 폴더에서 'claude' 실행 -> /effort high -> 프롬프트 붙여넣기 -> 'mp4로 렌더링해줘'" -ForegroundColor Green
