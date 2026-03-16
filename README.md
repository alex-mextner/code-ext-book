# VS Code Extension API — The Complete Developer Guide

By **[Alex](https://t.me/mxtnr)** — CTO at [HyperIDE](https://hyperide.ai), 15 years in software development.

A comprehensive book about building Visual Studio Code extensions. Covers the full journey from Hello World to publishing AI-powered extensions with Language Model API and MCP.

**~230 pages** | **19 chapters** | **50+ tips** | **4 reference appendices** | **51-term glossary**

Available in Russian (complete) and English (chapters 1-9, rest in progress).

## Quick Start

```bash
# Install fonts (first time only)
./scripts/install-fonts.sh

# Build Russian PDF
./scripts/build.sh

# Build English PDF
./scripts/build-en.sh

# Build both
./scripts/build-all.sh
```

Requires [uv](https://github.com/astral-sh/uv) (Python package runner) — no virtualenv needed.

## What's Inside

### Part I — Fundamentals (Chapters 1-9)
Hello World, extension anatomy (Activation Events, Contribution Points, VS Code API), editor & text manipulation, commands/menus/settings, themes, Tree View, Decoration API, Webview, Custom Editors, Virtual Documents, language extensions (completion, diagnostics, hover).

### Part II — Advanced (Chapters 10-18)
Language Server Protocol, UX guidelines, testing (`@vscode/test-cli`), bundling with esbuild, publishing to Marketplace & Open VSX, CI/CD with GitHub Actions, Extension Host architecture, AI Chat Participants, Language Model Tools & MCP.

### Part III — Practical Examples
TODO extension (full implementation), Status Bar info widget, FileSystemProvider, Source Control API, Debug Adapter, Task Provider, Authentication API, Notebook API (with HTTP Request Notebook example), Localization (L10n).

### UX & Performance
Extension UX design principles, conflict resolution, progressive disclosure. Deep dive into what makes VS Code fast — V8 code caching, virtual line rendering, MessagePort IPC, async decorations.

### 50+ Developer Tips
Isolated VS Code instances, ESM modules, Extension Bisect, Output Channel logging, lazy provider registration, caching patterns, security (trust prompts, secret scanning), telemetry, pre-release versions, platform-specific VSIX, and more.

### Reference Appendices
- **A** — VS Code API (key methods by namespace)
- **B** — All Contribution Points
- **C** — All Activation Events
- **D** — CSS theme variables for Webview

## Screenshots

Real VS Code screenshots captured automatically via Playwright.

```bash
# Regenerate screenshots (requires VS Code installed)
./scripts/screenshots.sh
```

Includes: Command Palette, Explorer, Settings UI, Problems panel, Extensions view, Debug sidebar, Editor with tabs/minimap/breadcrumbs, custom Tree View with MarkdownString tooltips, and more.

## Project Structure

```
build_book.py          # Main build script (Russian PDF)
build_book_en.py       # English PDF build
book_helpers.py        # Styles, colors, helpers, syntax highlighting
book_ui_diagrams.py    # FileTreeSVG diagrams, visual mockups
front_matter.py        # Cover, dedication, TOC
book_part1.py          # Chapters 1-9
book_part2.py          # Chapters 10-18
book_part3.py          # Practical examples, L10n
book_ux.py             # UX guidelines
book_perf.py           # Performance deep dive
book_new.py            # Playwright E2E, monetization
book_part4.py          # 50+ tips, glossary, checklists
book_appendices.py     # Reference tables A-D
afterword.py           # Afterword
take-screenshots.ts    # Playwright screenshot automation
sample-project/        # VS Code extension used for screenshots
scripts/               # Build and utility scripts
screenshots/           # Generated VS Code screenshots
```

## How It Works

The book is generated as PDF using Python + [ReportLab](https://www.reportlab.com/). Each chapter file exports a `build_story*()` function that returns a list of ReportLab Flowable elements. `build_book.py` assembles them and runs a 2-pass build (`multiBuild`) for clickable Table of Contents and cross-references.

Code blocks have automatic TypeScript/JavaScript syntax highlighting. File tree diagrams are drawn programmatically with folder/file icons and connector lines. Glossary terms link to their chapter of origin.

## Requirements

- **Python 3.11+** (via `uv run`)
- **DejaVu Sans fonts** (install via `scripts/install-fonts.sh`)
- **Node.js 18+** (only for screenshot generation)
- **VS Code** (only for screenshot generation)

## Contributing

The book content is in Russian by default. English translation files have the `_en` suffix. To translate a chapter, copy the Russian file (e.g., `book_part2.py` → `book_part2_en.py`), translate all text in `p()`, `h2()`, `h3()`, `box()`, `banner()`, `bul()`, and table cells. Keep code blocks and API names as-is.

## Author

**Alex** — CTO at [HyperIDE](https://hyperide.ai), 15 years in software development.
- Telegram: [@mxtnr](https://t.me/mxtnr)
- GitHub: [alex-mextner](https://github.com/alex-mextner)

## License

Content and code are provided as-is for educational purposes.
