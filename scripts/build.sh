#!/usr/bin/env bash
# Build the Russian PDF
set -euo pipefail
cd "$(dirname "$0")/.."
uv run --with reportlab python3 build_book.py
echo "Russian PDF: vscode-extensions-complete-guide-ru.pdf"
