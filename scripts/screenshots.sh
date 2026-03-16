#!/usr/bin/env bash
# Take VS Code screenshots using Playwright
# Requires: VS Code installed, Node.js
set -euo pipefail
cd "$(dirname "$0")/.."

npm install --silent 2>/dev/null
npx tsx take-screenshots.ts
