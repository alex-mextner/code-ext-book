"""
book_ui_diagrams.py — Визуальные макеты VS Code UI компонентов
Показывают как выглядят Tree View, Quick Pick, Progress, Decorations, Status Bar
"""
from book_helpers import *


def _rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))


class TreeViewMockup(Flowable):
    """Visual mockup of VS Code Tree View panel."""
    def __init__(self, w=None, h=180):
        super().__init__()
        self.w = w or CW
        self.h = h

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        # Panel background
        c.setFillColorRGB(*_rgb('#252526'))
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Title bar
        c.setFillColorRGB(*_rgb('#1E1E1E'))
        c.rect(0, h - 28, w, 28, fill=1, stroke=0)
        c.setFillColorRGB(0.7, 0.7, 0.7)
        c.setFont('B', 9)
        c.drawString(10, h - 18, 'NODE DEPENDENCIES')

        # Refresh button icon (simplified)
        c.setFillColorRGB(*_rgb('#007ACC'))
        c.circle(w - 20, h - 14, 5, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont('R', 7)
        c.drawCentredString(w - 20, h - 17, '↻')

        # Tree items
        items = [
            (0,  True,  '$(package)', 'lodash',           '4.17.21', '#4EC9B0'),
            (1,  False, '$(file)',    '  lodash.min.js',  '',        '#CE9178'),
            (0,  True,  '$(package)', 'express',          '4.18.2',  '#4EC9B0'),
            (1,  False, '$(file)',    '  index.js',       '',        '#CE9178'),
            (1,  False, '$(folder)',  '  lib/',           '',        '#DCDCAA'),
            (0,  False, '$(package)', 'typescript',       '5.3.0',   '#4EC9B0'),
        ]

        y = h - 48
        for level, expanded, icon, label, desc, label_color in items:
            # Hover highlight for first item
            if y == h - 48:
                c.setFillColorRGB(*_rgb('#2A2D2E'))
                c.rect(0, y - 4, w, 18, fill=1, stroke=0)

            x = 10 + level * 16

            # Expand arrow
            if expanded:
                c.setFillColorRGB(0.6, 0.6, 0.6)
                c.setFont('R', 8)
                c.drawString(x, y + 3, '▾')
            elif level == 0:
                c.setFillColorRGB(0.6, 0.6, 0.6)
                c.setFont('R', 8)
                c.drawString(x, y + 3, '▸')

            # Icon
            c.setFillColorRGB(*_rgb(label_color))
            c.setFont('R', 8)
            c.drawString(x + 12, y + 3, icon.replace('$(', '').replace(')', ''))

            # Label
            c.setFillColorRGB(0.85, 0.85, 0.85)
            c.setFont('R', 8.5)
            c.drawString(x + 26, y + 3, label)

            # Description
            if desc:
                c.setFillColorRGB(0.5, 0.5, 0.5)
                c.setFont('R', 7.5)
                c.drawString(x + 26 + c.stringWidth(label, 'R', 8.5) + 6, y + 3, desc)

            y -= 18

        # Caption
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.setFont('I', 7.5)
        c.drawCentredString(w / 2, 4, 'Рис. — Tree View: иерархические данные в боковой панели VS Code')
        c.restoreState()


class QuickPickMockup(Flowable):
    """Visual mockup of VS Code Quick Pick."""
    def __init__(self, w=None, h=200):
        super().__init__()
        self.w = w or CW
        self.h = h

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        # Shadow/background overlay
        c.setFillColorRGB(0, 0, 0, 0.3)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Panel
        pw, ph = w * 0.75, h * 0.82
        px, py = (w - pw) / 2, (h - ph) / 2
        c.setFillColorRGB(*_rgb('#3C3C3C'))
        c.roundRect(px, py, pw, ph, 4, fill=1, stroke=0)

        # Input box
        c.setFillColorRGB(*_rgb('#3C3C3C'))
        c.rect(px, py + ph - 36, pw, 36, fill=1, stroke=0)
        c.setStrokeColorRGB(*_rgb('#007ACC'))
        c.setLineWidth(2)
        c.line(px, py + ph - 36, px + pw, py + ph - 36)

        # Search icon
        c.setFillColorRGB(0.6, 0.6, 0.6)
        c.setFont('R', 10)
        c.drawString(px + 10, py + ph - 24, '⌕')

        # Input text
        c.setFillColorRGB(0.85, 0.85, 0.85)
        c.setFont('R', 10)
        c.drawString(px + 28, py + ph - 24, 'My Extension: ')
        # Cursor
        cursor_x = px + 28 + c.stringWidth('My Extension: ', 'R', 10)
        c.setFillColorRGB(*_rgb('#007ACC'))
        c.rect(cursor_x, py + ph - 26, 1.5, 12, fill=1, stroke=0)

        # Items
        items_data = [
            ('$(play) Run File',            'Run current file',         True),
            ('$(package) Build Package',     'Build current package',    False),
            ('$(gear) Open Settings',        'Extension settings',       False),
            ('$(info) Show Documentation',   'Open docs in browser',     False),
        ]

        iy = py + ph - 52
        for label, desc, selected in items_data:
            if selected:
                c.setFillColorRGB(*_rgb('#094771'))
                c.rect(px, iy - 4, pw, 20, fill=1, stroke=0)

            icon = label.split(')')[0].replace('$(', '') + ')'
            text = label.split(') ')[1] if ') ' in label else label

            c.setFillColorRGB(*_rgb('#4EC9B0'))
            c.setFont('R', 8)
            c.drawString(px + 10, iy + 2, icon)

            color = '#FFFFFF' if selected else '#BBBBBB'
            c.setFillColorRGB(*_rgb(color))
            c.setFont('R', 9)
            c.drawString(px + 28, iy + 2, text)

            c.setFillColorRGB(0.5, 0.5, 0.5)
            c.setFont('R', 7.5)
            c.drawString(px + 28 + c.stringWidth(text, 'R', 9) + 8, iy + 2, desc)

            iy -= 22

        # Caption
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.setFont('I', 7.5)
        c.drawCentredString(w / 2, 4, 'Рис. — Quick Pick: палитра выбора действий (Command Palette, showQuickPick)')
        c.restoreState()


class ProgressMockup(Flowable):
    """Visual mockup of VS Code Progress notification."""
    def __init__(self, w=None, h=130):
        super().__init__()
        self.w = w or CW
        self.h = h

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        # Background
        c.setFillColorRGB(*_rgb('#1E1E1E'))
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Notification card
        nw, nh = w * 0.45, 75
        nx, ny = w - nw - 16, h - nh - 16
        c.setFillColorRGB(*_rgb('#252526'))
        c.roundRect(nx, ny, nw, nh, 4, fill=1, stroke=0)
        c.setStrokeColorRGB(*_rgb('#454545'))
        c.setLineWidth(0.5)
        c.roundRect(nx, ny, nw, nh, 4, fill=0, stroke=1)

        # Title
        c.setFillColorRGB(0.85, 0.85, 0.85)
        c.setFont('B', 8.5)
        c.drawString(nx + 10, ny + nh - 16, 'Analysing project...')

        # Progress bar bg
        c.setFillColorRGB(*_rgb('#3E3E3E'))
        c.roundRect(nx + 10, ny + nh - 36, nw - 20, 6, 3, fill=1, stroke=0)

        # Progress bar fill (67%)
        c.setFillColorRGB(*_rgb('#007ACC'))
        c.roundRect(nx + 10, ny + nh - 36, (nw - 20) * 0.67, 6, 3, fill=1, stroke=0)

        # Progress text
        c.setFillColorRGB(0.6, 0.6, 0.6)
        c.setFont('R', 7.5)
        c.drawString(nx + 10, ny + nh - 52, '12 / 18 files')

        # Cancel button
        c.setFillColorRGB(*_rgb('#007ACC'))
        bw, bh = 50, 14
        bx = nx + nw - bw - 10
        by = ny + 8
        c.roundRect(bx, by, bw, bh, 3, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont('R', 7)
        c.drawCentredString(bx + bw / 2, by + 3, 'Cancel')

        # Status bar progress (Window mode)
        c.setFillColorRGB(*_rgb('#007ACC'))
        c.rect(0, 0, w, 22, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont('R', 8)
        c.drawString(10, 7, '$(sync~spin) Indexing... 67%')
        c.setFillColorRGB(*_rgb('#99BBCC'))
        c.setFont('R', 7.5)
        c.drawRightString(w - 10, 7, 'ProgressLocation.Window — в статус-баре (ненавязчиво)')

        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.setFont('I', 7.5)
        c.drawCentredString(w / 2, 26, 'Рис. — Progress API: Notification (справа) и Window (строка состояния, внизу)')
        c.restoreState()


class DecorationMockup(Flowable):
    """Visual mockup of VS Code text decorations."""
    def __init__(self, w=None, h=160):
        super().__init__()
        self.w = w or CW
        self.h = h

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        # Editor background
        c.setFillColorRGB(*_rgb('#1E1E1E'))
        c.rect(0, 15, w, h - 15, fill=1, stroke=0)

        # Line numbers gutter
        c.setFillColorRGB(*_rgb('#1A1A1A'))
        c.rect(0, 15, 36, h - 15, fill=1, stroke=0)

        lines_data = [
            (1, 'const apiKey = ', '"sk-abc123def456";', None, None, True, False),
            (2, 'const ', 'config', ' = {', None, False, False),
            (3, '    endpoint: ', '"https://api.example.com"', ',', None, False, False),
            (4, '    timeout: ', '5000', ',', None, False, True),   # error squiggly
            (5, '};', '', '', None, False, False),
            (6, '', '', '', '#TODO: add retry logic', False, False),
        ]

        y = h - 30
        for num, p1, p2, p3, comment, is_secret, has_error in lines_data:
            # Line number
            c.setFillColorRGB(0.4, 0.4, 0.4)
            c.setFont('R', 7.5)
            c.drawRightString(32, y, str(num))

            x = 48

            if comment:
                # Comment decoration
                c.setFillColorRGB(*_rgb('#6A9955'))
                c.setFont('I', 8)
                c.drawString(x, y, comment)
            else:
                # Normal code
                c.setFillColorRGB(*_rgb('#D4D4D4'))
                c.setFont('M', 8)
                c.drawString(x, y, p1)
                x += c.stringWidth(p1, 'M', 8)

                if p2:
                    if '"' in p2 or "'" in p2:
                        c.setFillColorRGB(*_rgb('#CE9178'))  # string
                    elif p2[0].isdigit():
                        c.setFillColorRGB(*_rgb('#B5CEA8'))  # number
                    else:
                        c.setFillColorRGB(*_rgb('#9CDCFE'))  # identifier
                    c.drawString(x, y, p2)
                    x += c.stringWidth(p2, 'M', 8)

                if p3:
                    c.setFillColorRGB(*_rgb('#D4D4D4'))
                    c.drawString(x, y, p3)

                # Secret decoration: background highlight
                if is_secret:
                    secret_x = 48 + c.stringWidth(p1, 'M', 8)
                    secret_w = c.stringWidth(p2, 'M', 8)
                    c.setFillColorRGB(*_rgb('#8B1A1A'))
                    c.setFillAlpha(0.4)
                    c.rect(secret_x - 2, y - 2, secret_w + 4, 12, fill=1, stroke=0)
                    c.setFillAlpha(1.0)
                    c.setStrokeColorRGB(*_rgb('#FF4444'))
                    c.setLineWidth(1.5)
                    c.rect(secret_x - 2, y - 2, secret_w + 4, 12, fill=0, stroke=1)
                    # Warning icon
                    c.setFillColorRGB(*_rgb('#FF4444'))
                    c.setFont('B', 8)
                    c.drawString(x + 8, y, '⚠')

                # Error squiggly under line
                if has_error:
                    err_x = 48
                    err_w = c.stringWidth('    timeout: 5000,', 'M', 8)
                    c.setStrokeColorRGB(*_rgb('#F14C4C'))
                    c.setLineWidth(0.8)
                    step = 3
                    cx = err_x
                    while cx < err_x + err_w:
                        c.line(cx, y - 3, cx + step / 2, y - 1)
                        c.line(cx + step / 2, y - 1, cx + step, y - 3)
                        cx += step

            y -= 18

        # Labels
        c.setFillColorRGB(*_rgb('#FF8C00'))
        c.setFont('I', 7)
        c.drawString(w * 0.52, h - 26, '← background decoration (secret token)')
        c.setFillColorRGB(*_rgb('#F14C4C'))
        c.drawString(w * 0.52, h - 104, '← squiggly decoration (ошибка)')

        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.setFont('I', 7.5)
        c.drawCentredString(w / 2, 4, 'Рис. — Decoration API: выделение секрета (красный фон) и ошибки (squiggly)')
        c.restoreState()


class StatusBarMockup(Flowable):
    """Visual mockup of VS Code Status Bar with multiple extension items."""
    def __init__(self, w=None, h=80):
        super().__init__()
        self.w = w or CW
        self.h = h

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        # Editor background hint
        c.setFillColorRGB(*_rgb('#1E1E1E'))
        c.rect(0, 22, w, h - 22, fill=1, stroke=0)
        c.setFillColorRGB(*_rgb('#2D2D2D'))
        c.setFont('M', 8)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawString(10, h - 20, '// extension.ts  —  VS Code Status Bar')

        # Status bar
        c.setFillColorRGB(*_rgb('#007ACC'))
        c.rect(0, 0, w, 22, fill=1, stroke=0)

        # Left items
        left_items = [
            ('↙ main', '#FFFFFF'),
            ('$(error) 0  $(warning) 2', '#FFFFFF'),
            ('$(sync~spin) Indexing', '#99CCFF'),
        ]
        x = 6
        for text, color in left_items:
            c.setFillColorRGB(*_rgb(color))
            c.setFont('R', 7.5)
            c.drawString(x, 7, text)
            x += c.stringWidth(text, 'R', 7.5) + 14

        # Right items
        right_items = [
            ('UTF-8  LF', '#FFFFFF'),
            ('TypeScript', '#FFFFFF'),
            ('Ln 42, Col 8', '#FFFFFF'),
            ('$(check) ESLint', '#AAFFAA'),
            ('Python 3.11', '#FFCC66'),
        ]
        x = w - 6
        for text, color in reversed(right_items):
            tw = c.stringWidth(text, 'R', 7.5)
            x -= tw + 14
            c.setFillColorRGB(*_rgb(color))
            c.setFont('R', 7.5)
            c.drawString(x, 7, text)

        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.setFont('I', 7.5)
        c.drawCentredString(w / 2, h - 8, 'Рис. — Status Bar: слева — глобальные элементы, справа — контекстные')
        c.restoreState()


class FileTreeSVG(Flowable):
    """Clean file tree diagram with proper connector lines."""
    LINE_H = 17
    INDENT = 16
    PAD_TOP = 14
    PAD_BOT = 10
    CAPTION_H = 16

    def __init__(self, w=None, h=None, items=None, title=''):
        super().__init__()
        self.w = w or CW * 0.7
        self.title = title
        self.items = items or []
        # Auto-calculate height from items
        content_h = self.PAD_TOP + len(self.items) * self.LINE_H + self.PAD_BOT
        self.h = h if h and h > content_h + self.CAPTION_H else content_h + self.CAPTION_H

    def wrap(self, aw, ah): return self.w, self.h

    def _is_last_at_depth(self, idx):
        """Check if item at idx is the last sibling at its depth."""
        d = self.items[idx][0]
        for j in range(idx + 1, len(self.items)):
            if self.items[j][0] < d:
                return True
            if self.items[j][0] == d:
                return False
        return True

    def draw(self):
        c = self.canv
        c.saveState()
        w = self.w
        box_h = self.h - self.CAPTION_H
        line_h = self.LINE_H
        indent = self.INDENT

        # Background
        c.setFillColorRGB(*_rgb('#1E1E1E'))
        c.roundRect(0, self.CAPTION_H, w, box_h, 4, fill=1, stroke=0)
        c.setStrokeColorRGB(*_rgb('#454545'))
        c.setLineWidth(0.5)
        c.roundRect(0, self.CAPTION_H, w, box_h, 4, fill=0, stroke=1)

        # Draw items top-to-bottom
        base_y = self.CAPTION_H + box_h - self.PAD_TOP
        for i, (depth, is_dir, name, comment) in enumerate(self.items):
            y = base_y - i * line_h
            x = 14 + depth * indent

            # Connector lines (L-shape) for non-root items
            if depth > 0:
                cx = 14 + (depth - 1) * indent + indent // 2  # center of parent indent
                is_last = self._is_last_at_depth(i)
                c.setStrokeColorRGB(*_rgb('#555555'))
                c.setLineWidth(0.7)
                # Vertical line from above
                c.line(cx, y + line_h - 2, cx, y + 5)
                # Horizontal line to item
                c.line(cx, y + 5, x - 2, y + 5)
                # Continue vertical line down for non-last siblings
                if not is_last:
                    c.line(cx, y + 5, cx, y - line_h + line_h - 2)

            # Folder/file icon
            if is_dir:
                # Small folder icon (filled rectangle with tab)
                ix = x + 1
                iy = y + 2
                c.setFillColorRGB(*_rgb('#C09553'))
                c.rect(ix, iy, 8, 6, fill=1, stroke=0)
                c.rect(ix, iy + 5, 4, 2, fill=1, stroke=0)
                # Name
                c.setFillColorRGB(*_rgb('#E8E8A0'))
                c.setFont('B', 8.5)
                c.drawString(x + 12, y + 2, name)
            else:
                # Small file icon (rectangle with folded corner)
                ix = x + 1
                iy = y + 1
                c.setFillColorRGB(*_rgb('#6A9FB5'))
                c.rect(ix, iy, 7, 8, fill=1, stroke=0)
                c.setFillColorRGB(*_rgb('#1E1E1E'))
                # Folded corner
                p = c.beginPath()
                p.moveTo(ix + 4, iy + 8)
                p.lineTo(ix + 7, iy + 5)
                p.lineTo(ix + 7, iy + 8)
                p.close()
                c.drawPath(p, fill=1, stroke=0)
                # Name
                c.setFillColorRGB(*_rgb('#9CDCFE'))
                c.setFont('R', 8.5)
                c.drawString(x + 12, y + 2, name)

            # Comment (gray italic)
            if comment:
                name_font = 'B' if is_dir else 'R'
                text_end = x + 12 + c.stringWidth(name, name_font, 8.5) + 8
                c.setFillColorRGB(*_rgb('#6A9955'))
                c.setFont('I', 7.5)
                c.drawString(text_end, y + 2, comment)

        # Caption below the box
        if self.title:
            c.setFillColorRGB(0.4, 0.4, 0.4)
            c.setFont('I', 7.5)
            c.drawCentredString(w / 2, 3, self.title)

        c.restoreState()


def helloworld_tree(lang='ru'):
    """File tree for Hello World extension project."""
    if lang == 'en':
        items = [
            (0, True,  'helloworld/', ''),
            (1, True,  '.vscode/', ''),
            (2, False, 'launch.json', '← launch Extension Host'),
            (2, False, 'tasks.json',  '← TypeScript compilation'),
            (1, True,  'src/', ''),
            (2, False, 'extension.ts', '← entry point'),
            (2, True,  'test/', ''),
            (3, False, 'extension.test.ts', ''),
            (1, False, '.vscodeignore', '← .vsix exclusions'),
            (1, False, 'esbuild.js',    '← build script'),
            (1, False, 'package.json',  '← extension manifest'),
            (1, False, 'tsconfig.json', ''),
            (1, False, 'README.md', ''),
        ]
        title = 'VS Code extension project structure'
    else:
        items = [
            (0, True,  'helloworld/', ''),
            (1, True,  '.vscode/', ''),
            (2, False, 'launch.json', '← запуск Extension Host'),
            (2, False, 'tasks.json',  '← компиляция TypeScript'),
            (1, True,  'src/', ''),
            (2, False, 'extension.ts', '← точка входа'),
            (2, True,  'test/', ''),
            (3, False, 'extension.test.ts', ''),
            (1, False, '.vscodeignore', '← исключения из .vsix'),
            (1, False, 'esbuild.js',    '← скрипт сборки'),
            (1, False, 'package.json',  '← манифест расширения'),
            (1, False, 'tsconfig.json', ''),
            (1, False, 'README.md', ''),
        ]
        title = 'Структура проекта расширения VS Code'
    return FileTreeSVG(w=CW * 0.72, h=240, items=items, title=title)


def lsp_tree(lang='ru'):
    """File tree for LSP extension project."""
    items = [
        (0, True,  'my-language-extension/', ''),
        (1, True,  'client/', ''),
        (2, True,  'src/', ''),
        (3, False, 'extension.ts', '← Language Client'),
        (1, True,  'server/', ''),
        (2, True,  'src/', ''),
        (3, False, 'server.ts', '← Language Server'),
        (1, False, 'package.json', ''),
    ]
    title = 'LSP extension structure: client and server' if lang == 'en' else 'Структура LSP-расширения: клиент и сервер'
    return FileTreeSVG(w=CW * 0.65, h=160, items=items, title=title)


def agent_skills_tree(lang='ru'):
    """File tree for Agent Skills structure."""
    if lang == 'en':
        items = [
            (0, True,  '.github/', ''),
            (1, True,  'my-skill/', ''),
            (2, False, 'SKILL.md', '← description and instructions'),
            (2, False, 'example.ts', '← code examples'),
            (2, False, 'schema.json', '← optional input schema'),
        ]
    else:
        items = [
            (0, True,  '.github/', ''),
            (1, True,  'my-skill/', ''),
            (2, False, 'SKILL.md', '← описание и инструкции'),
            (2, False, 'example.ts', '← примеры кода'),
            (2, False, 'schema.json', '← опциональная схема'),
        ]
    title = 'Agent Skill structure' if lang == 'en' else 'Структура Agent Skill'
    return FileTreeSVG(w=CW * 0.55, h=120, items=items, title=title)


if __name__ == '__main__':
    from reportlab.platypus import SimpleDocTemplate
    import io
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=ML, rightMargin=MR,
                            topMargin=2*cm, bottomMargin=2*cm)
    story = [
        TreeViewMockup(), sp(12),
        QuickPickMockup(), sp(12),
        ProgressMockup(), sp(12),
        DecorationMockup(), sp(12),
        StatusBarMockup(), sp(12),
        helloworld_tree(),
    ]
    doc.build(story)
    print(f'UI diagrams OK, size: {len(buf.getvalue())//1024}KB')
