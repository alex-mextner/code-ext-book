#!/usr/bin/env bash
# Install DejaVu fonts required for PDF generation
set -euo pipefail

if [[ "$(uname)" == "Darwin" ]]; then
    if ls ~/Library/Fonts/DejaVuSans.ttf &>/dev/null; then
        echo "DejaVu fonts already installed"
        exit 0
    fi
    echo "Installing DejaVu fonts for macOS..."
    cd /tmp
    curl -sL "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2" -o dejavu.tar.bz2
    tar xjf dejavu.tar.bz2
    cp dejavu-fonts-ttf-2.37/ttf/DejaVuSans{,-Bold,-Oblique,-BoldOblique}.ttf ~/Library/Fonts/
    cp dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono{,-Bold}.ttf ~/Library/Fonts/
    rm -rf dejavu.tar.bz2 dejavu-fonts-ttf-2.37
    echo "Done: fonts installed to ~/Library/Fonts/"
elif [[ "$(uname)" == "Linux" ]]; then
    if ls /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf &>/dev/null; then
        echo "DejaVu fonts already installed"
        exit 0
    fi
    echo "Installing DejaVu fonts for Linux..."
    sudo apt-get install -y fonts-dejavu-core 2>/dev/null || \
    sudo dnf install -y dejavu-sans-fonts dejavu-sans-mono-fonts 2>/dev/null || \
    echo "Please install DejaVu fonts manually"
fi
