# Official 1-Line Online Installer for media-pipeline-cli (Windows PowerShell)

Write-Host "=== 🚀 Installing AI Media Upscaler CLI (ai-media) for Windows ===" -ForegroundColor Green

if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installing ai-media-upscaler via pip..." -ForegroundColor Cyan
python -m pip install --upgrade git+https://github.com/Francis-Xavier-code/media-pipeline-cli.git

# Auto-detect Python Scripts Directory
$pythonScripts = (python -c "import sysconfig; print(sysconfig.get_path('scripts'))").Trim()

# 1. Permanently update User PATH in Windows Registry
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$pythonScripts*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$pythonScripts", "User")
    Write-Host "✅ Permanently registered $pythonScripts in Windows User PATH!" -ForegroundColor Green
}

# 2. ⚡ IMMEDIATELY refresh current session's $env:Path memory variable
if ($env:Path -notlike "*$pythonScripts*") {
    $env:Path = "$pythonScripts;$env:Path"
    Write-Host "⚡ Refreshed current PowerShell session PATH variable!" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 SUCCESS! ai-media CLI successfully installed on Windows!" -ForegroundColor Green
Write-Host "Run 'ai-media --help' right here in PowerShell to get started." -ForegroundColor Yellow
