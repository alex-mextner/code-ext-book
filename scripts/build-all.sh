#!/usr/bin/env bash
# Build both Russian and English PDFs
set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== Building Russian PDF ==="
uv run --with reportlab python3 build_book.py

echo ""
echo "=== Building English PDF ==="
uv run --with reportlab python3 build_book_en.py

echo ""
echo "Done:"
ls -lh vscode-extensions-complete-guide-*.pdf
