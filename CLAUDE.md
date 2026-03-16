# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A VS Code Extension API book generated as PDF via Python + ReportLab. Russian edition (primary) and English translation (partial — chapters 1-9).

## Build Commands

```bash
./scripts/build.sh          # Russian PDF → output.pdf
./scripts/build-en.sh       # English PDF → output_en.pdf
./scripts/build-all.sh      # Both PDFs
./scripts/screenshots.sh    # Take VS Code screenshots → screenshots/*.png
./scripts/install-fonts.sh  # Install DejaVu fonts (first time)
python3 reannotate.py       # Rerun code annotation after adding chapters
```

## Architecture

**Build pipeline:** Each `book_*.py` file exports a `build_story*()` function returning a list of ReportLab Flowable elements. `build_book.py` assembles them in order and runs a 2-pass `multiBuild` for clickable TOC.

**Assembly order:** front_matter → book_part1 (ch1-9) → book_part2 (ch10-18) → book_part3 (practical examples, L10n) → book_ux → book_perf → book_new (Playwright, monetization) → book_part4 (50+ tips, glossary, checklists) → book_appendices (A-D) → afterword

**book_helpers.py** — all shared infrastructure:
- Styles dict `S` (body, h1, h2, h3, code, bullet, caption, etc.)
- Colors dict `C` (blue, codebg, codefg, border, etc.)
- Page dimensions: `W`, `H`, `ML`, `MR`, `CW` (content width)
- Helpers: `p()`, `h2()`, `h3()`, `code()`, `sp()`, `pb()`, `box()`, `bul()`, `tblh()`, `tbl2()`, `screenshot()`, `esc()`
- `AnchorFlowable` — TOC entries (caught by `BookDocTemplate.afterFlowable`)
- `StableAnchor` — cross-reference bookmarks (not in TOC, for glossary/appendix links)
- `_hl()` — TypeScript/JS syntax highlighter for code blocks
- Font aliases: R (Regular), B (Bold), I (Italic), BI (BoldItalic), M (Mono), MB (MonoBold)

**book_ui_diagrams.py** — visual components:
- `FileTreeSVG(items, title)` — file tree diagrams with folder/file icons and L-connectors. Auto-calculates height. Items: `(depth, is_dir, name, comment)` tuples
- `helloworld_tree()`, `lsp_tree()`, `agent_skills_tree()` — predefined trees
- Mockup classes (TreeViewMockup, QuickPickMockup, etc.) — mostly replaced by real screenshots

**Screenshots** — real VS Code screenshots taken via Playwright (`take-screenshots.ts`). Launched with `--extensionDevelopmentPath` loading `sample-project/` which has a TreeDataProvider with MarkdownString tooltips. Referenced via `screenshot('filename.png', 'caption')`.

## Chapter file pattern

Every chapter file follows this pattern:
```python
from book_helpers import *

def build_story():
    A = []
    def add(*x):
        for i in x: A.append(i)
    def ch(num, title, sub=''):
        add(StableAnchor(f'chapter_{num}'))
        add(toc_ch(label), banner(part, title, sub), sp(12))

    ch('1', 'Title', 'Subtitle')
    add(h2('Section'))
    add(p('Text with <b>bold</b> and <b>API names</b>.'))
    add(code(['line1', 'line2']))
    add(sp(3))
    add(p('Description of the code block above.'))

    return A
```

## Key conventions

- Every `code([...])` block MUST have a `p('...')` description after it (with `sp(3)` between)
- Cross-references to appendices use `<a href="#appendix_A">Справочник A</a>` (anchors from `StableAnchor`)
- Glossary terms link to chapters via `<a href="#chapter_N">Глава N</a>`
- Tables with official VS Code data must include a URL to the source documentation
- Code block comments in Russian (the book text language)
- `screenshot(filename, caption)` preserves aspect ratio, scales to fit `CW`
- `box(title, body, kind)` — kind: 'note' (blue), 'tip' (green), 'warn' (orange)

## Fonts

DejaVu Sans family required. On macOS: `~/Library/Fonts/DejaVu*.ttf`. On Linux: `/usr/share/fonts/truetype/dejavu/`. Install via `brew install --cask font-dejavu-sans` or download from dejavu-fonts GitHub releases.
