#!/usr/bin/env bash
# Build the English PDF
set -euo pipefail
cd "$(dirname "$0")/.."
uv run --with reportlab python3 build_book_en.py
echo "English PDF: vscode-extensions-complete-guide-en.pdf"
