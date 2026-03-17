"""
book_helpers.py — переработанная версия v2
Исправления:
- Emoji заменены на ASCII-теги [ i ] [ > ] [ ! ]
- Синтаксическая подсветка TypeScript/JS
- Компактные пустые строки в коде
- Диаграммы как Flowable
- Цитаты разработчиков
"""

import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import HexColor

import os as _os, platform as _platform
def _font(name):
    if _platform.system() == 'Darwin':
        return _os.path.expanduser(f'~/Library/Fonts/{name}')
    return f'/usr/share/fonts/truetype/dejavu/{name}'

pdfmetrics.registerFont(TTFont('R',  _font('DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('B',  _font('DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('I',  _font('DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFont(TTFont('BI', _font('DejaVuSans-BoldOblique.ttf')))
pdfmetrics.registerFont(TTFont('M',  _font('DejaVuSansMono.ttf')))
pdfmetrics.registerFont(TTFont('MB', _font('DejaVuSansMono-Bold.ttf')))

W, H = A4
ML = MR = 2.2 * cm
CW = W - ML - MR

C = {
    'dark':    HexColor('#0D1117'), 'blue':   HexColor('#007ACC'),
    'lblue':   HexColor('#4FC3F7'), 'teal':   HexColor('#00BCD4'),
    'orange':  HexColor('#E8701A'), 'green':  HexColor('#28A745'),
    'purple':  HexColor('#6F42C1'), 'white':  HexColor('#FFFFFF'),
    'lgray':   HexColor('#F8F9FA'), 'mgray':  HexColor('#9E9E9E'),
    'dgray':   HexColor('#424242'), 'border': HexColor('#DEE2E6'),
    'codebg':  HexColor('#F5F5F0'), 'codefg': HexColor('#383A42'),
    'kw':      HexColor('#A626A4'), 'str_c':  HexColor('#50A14F'),
    'num':     HexColor('#986801'), 'com':    HexColor('#A0A1A7'),
    'func':    HexColor('#4078F2'), 'type_c': HexColor('#0184BC'),
    'text':    HexColor('#212529'),
    'tipbg':   HexColor('#E8F5E9'), 'tipbdr': HexColor('#2E7D32'),
    'warnbg':  HexColor('#FFF3E0'), 'warnbdr':HexColor('#E65100'),
    'notebg':  HexColor('#E3F2FD'), 'notebdr':HexColor('#1565C0'),
    'quotebg': HexColor('#F3E5F5'), 'quotebdr':HexColor('#7B1FA2'),
}

def ps(name, font='R', size=10, color=None, sb=0, sa=5,
       lead=None, align=TA_JUSTIFY, li=0, ri=0):
    return ParagraphStyle(
        name, fontName=font, fontSize=size, textColor=color or C['text'],
        spaceBefore=sb, spaceAfter=sa, leading=lead or int(size * 1.55),
        alignment=align, leftIndent=li, rightIndent=ri,
    )

S = {
    'h1':      ps('h1',  'B',  20, C['blue'],   16, 8,  align=TA_LEFT),
    'h2':      ps('h2',  'B',  15, C['blue'],   14, 6,  align=TA_LEFT),
    'h3':      ps('h3',  'B',  12, C['dgray'],  10, 4,  align=TA_LEFT),
    'h4':      ps('h4',  'B',  10.5,C['dgray'],  8, 3,  align=TA_LEFT),
    'body':    ps('body','R',  10,  C['text'],   0, 6,  16),
    'bodyi':   ps('bi',  'I',  10,  C['dgray'],  0, 5,  16),
    'bullet':  ps('bul', 'R',  10,  C['text'],   0, 3,  15, TA_LEFT, 14),
    'bullet2': ps('bu2', 'R',  9.5, C['dgray'],  0, 2,  14, TA_LEFT, 28),
    'code':    ps('cod', 'M',  8.5, C['codefg'], 0, 0,  13),
    'code_e':  ps('ce',  'M',  3,   C['codefg'], 0, 0,  4),
    'toc1':    ps('t1',  'B',  11,  C['blue'],   4, 2,  align=TA_LEFT),
    'toc2':    ps('t2',  'R',  10,  C['dgray'],  1, 1,  align=TA_LEFT, li=16),
    'partnum': ps('pn',  'R',  11,  C['lblue'],  0, 4,  align=TA_CENTER),
    'parttit': ps('pt',  'B',  26,  C['white'],  0, 8,  34, TA_CENTER),
    'partsub': ps('ps',  'I',  13,  HexColor('#B0BEC5'), 0, 4, align=TA_CENTER),
    'notet':   ps('nt',  'B',  9.5, C['blue'],   0, 2,  align=TA_LEFT),
    'noteb':   ps('nb',  'R',  9.5, C['text'],   0, 2,  14),
    'tipt':    ps('tt',  'B',  9.5, C['green'],  0, 2,  align=TA_LEFT),
    'tipb':    ps('tb',  'R',  9.5, C['text'],   0, 2,  14),
    'warnt':   ps('wt',  'B',  9.5, C['orange'], 0, 2,  align=TA_LEFT),
    'warnb':   ps('wb',  'R',  9.5, C['text'],   0, 2,  14),
    'rhead':   ps('rh',  'B',  9,   C['white'],  0, 0),
    'rkey':    ps('rk',  'M',  8.5, C['kw'],     0, 0,  13),
    'rval':    ps('rv',  'R',  9,   C['text'],   0, 0,  13),
    'caption': ps('cap', 'I',  8.5, C['mgray'],  2, 6,  align=TA_CENTER),
    'quote':   ps('qt',  'I',  11,  C['purple'],  4, 4,  18, TA_JUSTIFY, 8),
    'quoteauth':ps('qa', 'B',  9,   C['purple'],  0, 2,  align=TA_RIGHT),
    'diag':    ps('dg',  'I',  7.5, C['mgray'],  2, 4,  align=TA_CENTER),
    # Невидимый маркер для главы — отслеживается afterFlowable как уровень 0 TOC
    'ch_toc':  ps('ch_toc', 'B', 0.1, HexColor('#FFFFFF'), 0, 0, 1, TA_LEFT),
    # Маркер для h1-секции — уровень 1 TOC
    'sec_toc': ps('sec_toc', 'R', 0.1, HexColor('#FFFFFF'), 0, 0, 1, TA_LEFT),
}

# ─── Basic helpers ────────────────────────────────────────────────────────────

def esc(t): return str(t).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def sp(n=6): return Spacer(1, n)
def pb(): return PageBreak()

_SCREENSHOTS_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'screenshots')

def screenshot(filename, caption='', max_width=None):
    """Insert a screenshot image with optional caption. Preserves aspect ratio."""
    img_path = _os.path.join(_SCREENSHOTS_DIR, filename)
    if not _os.path.exists(img_path):
        return Paragraph(f'[Screenshot missing: {filename}]', S.get('body', ParagraphStyle('x')))
    max_w = max_width or CW
    max_h = 400
    img = Image(img_path)
    iw, ih = img.imageWidth, img.imageHeight
    # Scale preserving aspect ratio: fit within max_w x max_h
    ratio = min(max_w / iw, max_h / ih, 1.0)  # never upscale
    img = Image(img_path, width=iw * ratio, height=ih * ratio)
    elements = [img]
    if caption:
        elements.append(Spacer(1, 3))
        elements.append(Paragraph(caption, S.get('caption', ParagraphStyle('cap', fontName='I', fontSize=8.5, textColor=HexColor('#666666'), alignment=TA_CENTER))))
    if len(elements) == 1:
        return elements[0]
    from reportlab.platypus import KeepTogether
    return KeepTogether(elements)
def hl(col=None, thick=0.5):
    return HRFlowable(width='100%', thickness=thick,
                      color=col or C['border'], spaceAfter=4, spaceBefore=4)
def p(txt, s='body'): return Paragraph(txt, S[s] if isinstance(s,str) else s)
def bul(txt, lvl=1):
    dot = '•' if lvl == 1 else '◦'
    st = 'bullet' if lvl == 1 else 'bullet2'
    return Paragraph(f'{dot} {txt}', S[st])
def h1(t): return p(t, 'h1')
def h2(t): return p(t, 'h2')
def h3(t): return p(t, 'h3')

class AnchorFlowable(Flowable):
    """Zero-height flowable: bookmarks current page for PDF navigation.
    build_book.py catches these in afterFlowable to build the clickable TOC."""
    def __init__(self, key, title, level=0):
        Flowable.__init__(self)
        self.key   = key
        self.title = title
        self.level = level
        self.width = 0
        self.height = 0
    def wrap(self, w, h): return 0, 0
    def draw(self):
        self.canv.bookmarkPage(self.key)


class StableAnchor(Flowable):
    """Zero-height bookmark for cross-references (not picked up by TOC)."""
    def __init__(self, key):
        Flowable.__init__(self)
        self.key = key
        self.width = 0
        self.height = 0
    def wrap(self, w, h): return 0, 0
    def draw(self):
        self.canv.bookmarkPage(self.key)


_anchor_seq = [0]

def toc_ch(label):
    """Chapter-level TOC anchor (level 0)."""
    import re as _re
    _anchor_seq[0] += 1
    key = f'ch{_anchor_seq[0]}_' + _re.sub(r'[^\w]', '_', label[:24])
    return AnchorFlowable(key, label, level=0)

def toc_sec(label):
    """Section-level TOC anchor (level 1)."""
    import re as _re
    _anchor_seq[0] += 1
    key = f'sc{_anchor_seq[0]}_' + _re.sub(r'[^\w]', '_', label[:24])
    return AnchorFlowable(key, label, level=1)


# ─── Syntax Highlighting ──────────────────────────────────────────────────────

_TS_KW = {'const','let','var','function','class','interface','type','extends',
          'implements','import','export','from','return','if','else','for',
          'while','do','switch','case','break','continue','new','delete',
          'typeof','instanceof','void','null','undefined','true','false',
          'async','await','try','catch','finally','throw','in','of','default',
          'static','public','private','protected','readonly','abstract',
          'namespace','enum','as','this','super','require','module'}

_TS_TYPES = {'string','number','boolean','object','any','never','unknown',
             'Array','Promise','Record','Partial','Required','Readonly','Map',
             'Set','Error','Buffer','URL','Date','vscode','context','window'}

def _hl(line: str) -> str:
    """
    Syntax highlight one line of TypeScript/JS.
    Uses segment-based approach to avoid double-tagging.
    Returns ReportLab XML markup.
    """
    if not line.strip():
        return ' '

    kc = '#569CD6'   # keyword blue
    sc = '#CE9178'   # string orange
    nc = '#B5CEA8'   # number green
    cc = '#6A9955'   # comment grey-green
    fc = '#DCDCAA'   # function yellow

    # We work on the raw line (not HTML-escaped) to tokenize safely,
    # then escape each token individually.

    # 1. If line is a comment, color whole line
    stripped = line.lstrip()
    if stripped.startswith('//') or stripped.startswith('#'):
        return f'<font color="{cc}">{esc(line)}</font>'

    # 2. If line starts with * (JSDoc / block comment content), grey it
    if stripped.startswith('*'):
        return f'<font color="{cc}">{esc(line)}</font>'

    # 3. Simple token-based highlighting
    # We split into: strings, numbers, keywords, identifiers, operators
    segments = []  # list of (text, color_or_None)

    i = 0
    while i < len(line):
        c = line[i]

        # Single-line comment
        if c == '/' and i + 1 < len(line) and line[i+1] == '/':
            segments.append((line[i:], cc))
            break

        # String: single quote
        elif c == "'":
            j = i + 1
            while j < len(line) and line[j] != "'":
                if line[j] == '\\': j += 1
                j += 1
            j += 1
            segments.append((line[i:j], sc))
            i = j

        # String: double quote
        elif c == '"':
            j = i + 1
            while j < len(line) and line[j] != '"':
                if line[j] == '\\': j += 1
                j += 1
            j += 1
            segments.append((line[i:j], sc))
            i = j

        # Template literal
        elif c == '`':
            j = i + 1
            while j < len(line) and line[j] != '`':
                if line[j] == '\\': j += 1
                j += 1
            j += 1
            segments.append((line[i:j], sc))
            i = j

        # Number
        elif c.isdigit() and (i == 0 or not line[i-1].isalnum()):
            j = i
            while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                j += 1
            segments.append((line[i:j], nc))
            i = j

        # Identifier or keyword
        elif c.isalpha() or c == '_':
            j = i
            while j < len(line) and (line[j].isalnum() or line[j] == '_'):
                j += 1
            word = line[i:j]
            # Check what follows
            rest = line[j:].lstrip()
            if word in _TS_KW:
                segments.append((word, kc))
            elif rest.startswith('('):
                segments.append((word, fc))
            else:
                segments.append((word, None))
            i = j

        else:
            # Accumulate plain chars
            if segments and segments[-1][1] is None:
                segments[-1] = (segments[-1][0] + c, None)
            else:
                segments.append((c, None))
            i += 1

    # Build result
    parts = []
    for text, color in segments:
        safe = esc(text)
        if color and safe.strip():
            parts.append(f'<font color="{color}">{safe}</font>')
        else:
            parts.append(safe)
    return ''.join(parts) if parts else esc(line)


def _indent_spaces(line: str) -> str:
    """Convert leading spaces/tabs to &nbsp; so ReportLab preserves indentation."""
    result = []
    for ch in line:
        if ch == ' ':
            result.append('&nbsp;')
        elif ch == '\t':
            result.append('&nbsp;&nbsp;&nbsp;&nbsp;')
        else:
            break
    return ''.join(result) + line.lstrip(' \t')


def code(lines, lang='ts', highlight=True):
    """Code block with syntax highlighting and preserved indentation."""
    rows = []
    for line in lines:
        if not line.strip():
            rows.append([Paragraph(' ', S['code_e'])])
        else:
            # Preserve leading indentation as &nbsp;
            n_indent = len(line) - len(line.lstrip(' \t'))
            indent_html = '&nbsp;' * n_indent if n_indent else ''
            body = line.lstrip(' \t')

            if highlight and lang in ('ts', 'js', 'typescript', 'javascript'):
                try:
                    rendered = indent_html + _hl(body)
                except Exception:
                    rendered = indent_html + esc(body)
            else:
                rendered = indent_html + esc(body)
            rows.append([Paragraph(rendered, S['code'])])

    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), C['codebg']),
        ('TOPPADDING',    (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 0.4, HexColor('#E0E0E0')),
    ]))
    return t


def code_plain(lines):
    return code(lines, lang='plain', highlight=False)


# ─── Callout boxes (без emoji — ASCII метки) ─────────────────────────────────

def box(title, body, kind='note'):
    cfg = {
        'note': ('[ i ]', 'notet', 'noteb', 'notebg',  'notebdr'),
        'tip':  ('[ > ]', 'tipt',  'tipb',  'tipbg',   'tipbdr'),
        'warn': ('[ ! ]', 'warnt', 'warnb', 'warnbg',  'warnbdr'),
    }
    label, ts, bs, bg, bdr = cfg.get(kind, cfg['note'])
    rows = [
        [Paragraph(f'<font name="MB">{label}</font>  <b>{title}</b>', S[ts])],
        [Paragraph(body, S[bs])],
    ]
    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), C[bg]),
        ('TOPPADDING',    (0,0),(-1,-1), 7),
        ('BOTTOMPADDING', (0,0),(-1,-1), 7),
        ('LEFTPADDING',   (0,0),(-1,-1), 14),
        ('RIGHTPADDING',  (0,0),(-1,-1), 14),
        ('BOX',           (0,0),(-1,-1), 1.5, C[bdr]),
        ('LINEBELOW',     (0,0),(-1,0),  0.5, C[bdr]),
    ]))
    return t


# ─── Quote block ──────────────────────────────────────────────────────────────

def quote(text, author, role=''):
    attr = f'— <b>{author}</b>'
    if role: attr += f',  {role}'
    rows = [
        [Paragraph(f'<i>&quot;{esc(text)}&quot;</i>', S['quote'])],
        [Paragraph(attr, S['quoteauth'])],
    ]
    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',  (0,0),(-1,-1), C['quotebg']),
        ('TOPPADDING',  (0,0),(-1,-1), 10),
        ('BOTTOMPADDING',(0,0),(-1,-1), 10),
        ('LEFTPADDING', (0,0),(-1,-1), 20),
        ('RIGHTPADDING',(0,0),(-1,-1), 14),
        ('LINEBEFORE',  (0,0),(0,-1),  4, C['quotebdr']),
    ]))
    return t


# ─── Tables ───────────────────────────────────────────────────────────────────

def tblh(hdrs, ratio=0.40):
    w1, w2 = CW*ratio, CW*(1-ratio)
    row = [Paragraph(f'<b>{h}</b>', S['rhead']) for h in hdrs]
    t = Table([row], colWidths=[w1, w2])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), C['dark']),
        ('TOPPADDING',   (0,0),(-1,-1), 7),
        ('BOTTOMPADDING',(0,0),(-1,-1), 7),
        ('LEFTPADDING',  (0,0),(-1,-1), 8),
        ('RIGHTPADDING', (0,0),(-1,-1), 8),
    ]))
    return t

def tbl2(data, ratio=0.40):
    w1, w2 = CW*ratio, CW*(1-ratio)
    rows = [[Paragraph(esc(k), S['rkey']), Paragraph(v, S['rval'])] for k,v in data]
    t = Table(rows, colWidths=[w1, w2])
    t.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[C['lgray'],C['white']]),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
        ('GRID',(0,0),(-1,-1), 0.3, C['border']),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    return t

def banner(part, title, sub=''):
    rows = [[p(part, 'partnum')], [p(title, 'parttit')]]
    if sub: rows.append([p(sub, 'partsub')])
    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), C['dark']),
        ('TOPPADDING',   (0,0),(-1,-1), 14),
        ('BOTTOMPADDING',(0,0),(-1,-1), 14),
        ('LEFTPADDING',  (0,0),(-1,-1), 24),
        ('RIGHTPADDING', (0,0),(-1,-1), 24),
        ('LINEBELOW',(0,-1),(-1,-1), 4, C['blue']),
    ]))
    return t


# ─── Diagram Flowables ────────────────────────────────────────────────────────

def _rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0,2,4))


class ArchDiagram(Flowable):
    """VS Code process architecture — 3 boxes with arrows."""
    def __init__(self, w=None, h=150):
        super().__init__()
        self.w = w or CW
        self.h = h

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        boxes = [
            ('Main\nProcess',        0.01, 0.50, 0.26, 0.40, '#1565C0', '#E3F2FD'),
            ('Renderer\n(Chromium)', 0.30, 0.50, 0.26, 0.40, '#1B5E20', '#E8F5E9'),
            ('Extension Host\n(Node.js)',0.59, 0.50, 0.40, 0.40, '#E65100', '#FFF3E0'),
        ]

        for label, xr, yr, wr, hr, border, bg in boxes:
            bx, by, bw, bh = xr*w, yr*h, wr*w, hr*h
            c.setFillColorRGB(*_rgb(bg))
            c.setStrokeColorRGB(*_rgb(border))
            c.setLineWidth(1.5)
            c.roundRect(bx, by, bw, bh, 5, fill=1, stroke=1)
            c.setFillColorRGB(*_rgb(border))
            c.setFont('B', 8)
            lines = label.split('\n')
            cy = by + bh/2 + (len(lines)-1)*5
            for ln in lines:
                c.drawCentredString(bx + bw/2, cy, ln); cy -= 11

        # Extensions inside Extension Host
        for j, ename in enumerate(['Ext A', 'Ext B', 'Ext C']):
            bx = (0.60 + j * 0.125) * w
            by, bw, bh = 0.10*h, 0.11*w, 0.32*h
            c.setFillColorRGB(0.1,0.1,0.1)
            c.setStrokeColorRGB(0.34,0.49,0.73)
            c.setLineWidth(1)
            c.roundRect(bx, by, bw, bh, 3, fill=1, stroke=1)
            c.setFillColorRGB(0.83,0.83,0.83)
            c.setFont('M', 7)
            c.drawCentredString(bx + bw/2, by + bh/2 - 3, ename)

        # Arrows
        ay = h * 0.70
        for x1, x2 in [(0.27*w, 0.30*w), (0.56*w, 0.59*w)]:
            c.setStrokeColorRGB(0.4,0.4,0.4); c.setLineWidth(1.2)
            c.line(x1, ay, x2-4, ay)
            c.setFillColorRGB(0.4,0.4,0.4)
            p = c.beginPath()
            p.moveTo(x2-4, ay+4); p.lineTo(x2-4, ay-4); p.lineTo(x2+2, ay); p.close()
            c.drawPath(p, fill=1, stroke=0)

        c.setFillColorRGB(0.5,0.5,0.5); c.setFont('I', 7)
        c.drawCentredString(0.285*w, ay-10, 'IPC')
        c.drawCentredString(0.575*w, ay-10, 'IPC')

        c.setFillColorRGB(0.3,0.3,0.3); c.setFont('I', 8)
        c.drawCentredString(w/2, h*0.03,
            'Рис. 1 — Extension Host изолирован от UI: падение расширения не затрагивает редактор')
        c.restoreState()


class LSPDiagram(Flowable):
    """M языков × N редакторов → LSP решает M*N проблему."""
    def __init__(self, w=None, h=120):
        super().__init__()
        self.w = w or CW
        self.h = h

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        left_items  = ['VS Code', 'Vim/Neovim', 'Emacs', 'IntelliJ']
        right_items = ['TypeScript LSP', 'rust-analyzer', 'Pylance (Python)', 'clangd (C++)']
        col_w = w * 0.27
        bh = h * 0.72
        by = h * 0.18

        for i, (items, bx, border, bg) in enumerate([
            (left_items,  0.01*w, '#1565C0', '#E3F2FD'),
            (right_items, 0.72*w, '#1B5E20', '#E8F5E9'),
        ]):
            c.setFillColorRGB(*_rgb(bg)); c.setStrokeColorRGB(*_rgb(border))
            c.setLineWidth(1.5); c.roundRect(bx, by, col_w, bh, 5, fill=1, stroke=1)
            c.setFillColorRGB(*_rgb(border)); c.setFont('B', 8)
            label = 'Редакторы' if i == 0 else 'Языковые серверы'
            c.drawCentredString(bx + col_w/2, by + bh - 10, label)
            c.setFont('R', 7.5); c.setFillColorRGB(0.2,0.2,0.2)
            iy = by + bh - 24
            for item in items:
                c.drawCentredString(bx + col_w/2, iy, item); iy -= 13

        # Protocol box in middle
        px, pw = 0.30*w, w*0.40
        c.setFillColorRGB(*_rgb('#EDE7F6')); c.setStrokeColorRGB(*_rgb('#4527A0'))
        c.setLineWidth(1.5); c.roundRect(px, by, pw, bh, 5, fill=1, stroke=1)
        c.setFillColorRGB(*_rgb('#4527A0')); c.setFont('B', 8)
        c.drawCentredString(px + pw/2, by + bh - 10, 'Language Server Protocol')
        c.setFont('R', 7.5); c.setFillColorRGB(0.3,0.3,0.3)
        c.drawCentredString(px + pw/2, by + bh/2, 'JSON-RPC over stdio')
        c.drawCentredString(px + pw/2, by + bh/2 - 13, 'M + N  вместо  M * N')

        c.setFillColorRGB(0.3,0.3,0.3); c.setFont('I', 8)
        c.drawCentredString(w/2, h*0.04,
            'Рис. 2 — LSP: один языковой сервер работает во всех редакторах')
        c.restoreState()


class UXPyramid(Flowable):
    """UI visibility pyramid — 3 levels."""
    def __init__(self, w=None, h=130):
        super().__init__()
        self.w = w or CW
        self.h = h

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        levels = [
            ('Уровень 3 — По запросу: Command Palette, Tree View, Webview',
             0.04, 0.60, 0.92, 0.28, '#E3F2FD', '#1565C0'),
            ('Уровень 2 — В контексте: Editor Toolbar, Context Menu',
             0.12, 0.30, 0.76, 0.26, '#E8F5E9', '#2E7D32'),
            ('Уровень 1 — Всегда: максимум 1-2 Status Bar элемента',
             0.24, 0.04, 0.52, 0.22, '#FFF3E0', '#E65100'),
        ]

        for label, xr, yr, wr, hr, bg, bdr in levels:
            bx, by, bw, bh = xr*w, yr*h, wr*w, hr*h
            c.setFillColorRGB(*_rgb(bg)); c.setStrokeColorRGB(*_rgb(bdr))
            c.setLineWidth(1.5); c.roundRect(bx, by, bw, bh, 4, fill=1, stroke=1)
            c.setFillColorRGB(*_rgb(bdr)); c.setFont('R', 7.5)
            c.drawCentredString(bx + bw/2, by + bh/2 - 4, label)

        # Left arrow
        c.setStrokeColorRGB(0.4,0.4,0.4); c.setLineWidth(1)
        c.line(0.02*w, 0.08*h, 0.02*w, 0.86*h)
        c.setFillColorRGB(0.4,0.4,0.4)
        pa = c.beginPath()
        pa.moveTo(0.02*w-3, 0.80*h); pa.lineTo(0.02*w+3, 0.80*h)
        pa.lineTo(0.02*w, 0.86*h); pa.close()
        c.drawPath(pa, fill=1, stroke=0)
        c.setFont('I', 6.5)
        c.drawString(0.001*w, h*0.5, 'Больше\nпользователей')

        c.setFillColorRGB(0.3,0.3,0.3); c.setFont('I', 7.5)
        c.drawCentredString(w/2, h*0.01,
            'Рис. 3 — Пирамида видимости: основные функции — на уровне 3 (по запросу)')
        c.restoreState()


class MonetizationDiagram(Flowable):
    """Business models for VS Code extensions."""
    def __init__(self, w=None, h=130):
        super().__init__()
        self.w = w or CW
        self.h = h

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        models = [
            ('Freemium',      'Базово бесплатно,\nпремиум — платно', '#1565C0', '#E3F2FD', 0.01),
            ('SaaS Backend',  'Расширение бесплатно,\nплатный API/сервис', '#1B5E20', '#E8F5E9', 0.26),
            ('Open Source\n+ Enterprise', 'OSS-ядро +\nплатная поддержка', '#4A148C', '#F3E5F5', 0.51),
            ('Brand\nAwareness', 'Расширение как\nмаркетинг продукта', '#B71C1C', '#FFEBEE', 0.76),
        ]

        for label, desc, border, bg, xr in models:
            bx, by, bw, bh = xr*w, 0.18*h, w*0.22, h*0.62
            c.setFillColorRGB(*_rgb(bg)); c.setStrokeColorRGB(*_rgb(border))
            c.setLineWidth(1.5); c.roundRect(bx, by, bw, bh, 5, fill=1, stroke=1)
            c.setFillColorRGB(*_rgb(border)); c.setFont('B', 7.5)
            lines = label.split('\n')
            cy = by + bh - 12
            for ln in lines: c.drawCentredString(bx+bw/2, cy, ln); cy -= 11
            c.setFont('R', 7); c.setFillColorRGB(0.2,0.2,0.2)
            cy -= 4
            for ln in desc.split('\n'): c.drawCentredString(bx+bw/2, cy, ln); cy -= 10

        c.setFillColorRGB(0.3,0.3,0.3); c.setFont('I', 8)
        c.drawCentredString(w/2, h*0.04,
            'Рис. 4 — Четыре модели монетизации расширений VS Code')
        c.restoreState()


# ─── Cover + page events ─────────────────────────────────────────────────────

_IMAGES_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'images')

class Cover(Flowable):
    """Full-bleed cover page with background image, gradient overlay, and minimal text."""
    def wrap(self, aw, ah): return W, H
    def draw(self):
        c = self.canv; c.saveState()
        cover_img = _os.path.join(_IMAGES_DIR, 'cover.jpg')
        if _os.path.exists(cover_img):
            # Crop-to-fill: scale image so it covers the entire page
            from reportlab.lib.utils import ImageReader
            img = ImageReader(cover_img)
            iw, ih = img.getSize()
            # Scale to fill — use the larger scale factor
            scale = max(W / iw, H / ih)
            draw_w, draw_h = iw * scale, ih * scale
            # Center the image (crop overflow)
            x_off = (W - draw_w) / 2
            y_off = (H - draw_h) / 2
            p = c.beginPath()
            p.rect(0, 0, W, H)
            c.clipPath(p, stroke=0)
            c.drawImage(cover_img, x_off, y_off, width=draw_w, height=draw_h)
        else:
            c.setFillColor(C['dark']); c.rect(0, 0, W, H, fill=1, stroke=0)
        # Semi-transparent overlay at top for topics
        for i in range(25):
            alpha = (1 - i / 25.0) ** 2 * 0.5
            c.setFillColorRGB(0.02, 0.02, 0.05, alpha)
            c.rect(0, H - (i + 1) * (H * 0.12 / 25), W, H * 0.12 / 25, fill=1, stroke=0)
        # Topics as centered text, ~80% width
        topics = 'Architecture  ·  Commands & Menus  ·  Tree View  ·  Webview  ·  LSP'
        topics2 = 'Testing  ·  AI & MCP  ·  UX  ·  Publishing  ·  Performance'
        c.setFont('R', 8); c.setFillColorRGB(0.65, 0.7, 0.75, 0.75)
        c.drawCentredString(W / 2, H - 1.6 * cm, topics)
        c.drawCentredString(W / 2, H - 2.1 * cm, topics2)
        # Dark gradient overlay at bottom for text readability
        for i in range(60):
            alpha = (i / 60.0) ** 1.5 * 0.92
            c.setFillColorRGB(0.03, 0.03, 0.06, alpha)
            y = H * 0.45 * (1 - i / 60.0)
            c.rect(0, 0, W, y + H * 0.08, fill=1, stroke=0)
        # Title — one line, sized to fit
        c.setFont('B', 32); c.setFillColor(C['white'])
        c.drawString(2.2*cm, H * 0.22, 'VS Code Extension API')
        # Subtitle
        c.setFont('I', 13); c.setFillColorRGB(0.65, 0.72, 0.82)
        c.drawString(2.2*cm, H * 0.185, 'The Complete Developer Guide')
        # Subtle line
        c.setStrokeColorRGB(0.4, 0.6, 0.9, 0.4); c.setLineWidth(1)
        c.line(2.2*cm, H * 0.175, 13*cm, H * 0.175)
        # Author
        c.setFont('R', 12); c.setFillColorRGB(0.75, 0.78, 0.83)
        c.drawString(2.2*cm, H * 0.145, 'Alex Mextner')
        c.setFont('R', 9); c.setFillColorRGB(0.5, 0.53, 0.58)
        c.drawString(2.2*cm + c.stringWidth('Alex Mextner  ', 'R', 12), H * 0.147, 'CTO HyperIDE')
        # Year
        c.setFont('R', 10); c.setFillColorRGB(0.38, 0.4, 0.45)
        c.drawString(2.2*cm, H * 0.115, '2026')
        c.restoreState()


def on_first_page(canvas, doc): pass

def on_later_pages(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(C['border']); canvas.setLineWidth(.5)
    canvas.line(ML, H-1.3*cm, W-MR, H-1.3*cm)
    canvas.setFont('R',8); canvas.setFillColor(C['mgray'])
    canvas.drawString(ML, H-1.1*cm, 'VS Code Extension API — Полное руководство разработчика')
    canvas.drawRightString(W-MR, H-1.1*cm, f'стр. {doc.page}')
    canvas.setLineWidth(.5); canvas.line(ML,1.3*cm,W-MR,1.3*cm)
    canvas.setFont('R',7.5)
    canvas.drawCentredString(W/2, 1.0*cm, 'code.visualstudio.com/api  •  github.com/microsoft/vscode  •  2026')
    canvas.restoreState()
