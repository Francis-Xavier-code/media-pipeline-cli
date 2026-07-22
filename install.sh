#!/usr/bin/env bash
# Official 1-Line Online Installer for media-pipeline-cli (Linux & macOS)

set -e

echo "=== 🚀 Installing AI Media Upscaler CLI (ai-media) for Linux/macOS ==="

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 is required. Please install python3 first."
    exit 1
fi

if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ Error: pip is required. Please install python3-pip first."
    exit 1
fi

PIP_BIN=$(command -v pip3 || command -v pip)

echo "📦 Installing ai-media-upscaler via pip..."
$PIP_BIN install --upgrade git+https://github.com/Francis-Xavier-code/media-pipeline-cli.git

echo ""
echo "🎉 SUCCESS! ai-media CLI successfully installed!"
echo "Run 'ai-media --help' to get started."
