# Official 1-Line Online Installer for media-pipeline-cli (Windows PowerShell)

Write-Host "=== 🚀 Installing AI Media Upscaler CLI (ai-media) for Windows ===" -ForegroundColor Green

if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installing ai-media-upscaler via pip..." -ForegroundColor Cyan
python -m pip install --upgrade git+https://github.com/Francis-Xavier-code/media-pipeline-cli.git

# Auto-add Python Scripts to User PATH
$scriptDir = "$env:APPDATA\Python\Python314\Scripts"
if (Test-Path $scriptDir) {
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -notlike "*$scriptDir*") {
        [Environment]::SetEnvironmentVariable("Path", "$userPath;$scriptDir", "User")
        $env:Path += ";$scriptDir"
        Write-Host "✅ Added $scriptDir to User PATH!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "🎉 SUCCESS! ai-media CLI successfully installed on Windows!" -ForegroundColor Green
Write-Host "Run 'ai-media --help' in PowerShell to get started." -ForegroundColor Yellow
