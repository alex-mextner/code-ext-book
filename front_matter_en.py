"""
front_matter_en.py — English edition: cover, verso, dedication, table of contents
"""
from book_helpers import *
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class CoverEn(Flowable):
    """English cover page."""
    def wrap(self, aw, ah): return aw, ah
    def draw(self):
        c = self.canv; c.saveState()
        c.setFillColor(C['dark']); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(C['blue']); c.rect(0,H-10*mm,W,10*mm,fill=1,stroke=0)
        c.setFillColor(C['teal']); c.rect(0,0,8*mm,H,fill=1,stroke=0)
        c.setFillColor(HexColor('#0D2137')); c.circle(W*.78,H*.55,105,fill=1,stroke=0)
        c.setStrokeColor(C['blue']); c.setLineWidth(1.5); c.circle(W*.78,H*.55,105,fill=0,stroke=1)
        c.setStrokeColor(HexColor('#1565C0')); c.setLineWidth(.7); c.circle(W*.78,H*.55,122,fill=0,stroke=1)
        cx,cy = W*.78,H*.55
        c.setStrokeColor(C['blue']); c.setLineWidth(3)
        c.line(cx-27,cy+14,cx-11,cy); c.line(cx-27,cy-14,cx-11,cy)
        c.setStrokeColor(C['lblue'])
        c.line(cx+27,cy+14,cx+11,cy); c.line(cx+27,cy-14,cx+11,cy)
        c.setStrokeColor(C['orange']); c.setLineWidth(2.5); c.line(cx+5,cy+20,cx-5,cy-20)
        c.setFont('B',38); c.setFillColor(C['white'])
        c.drawString(3*cm, H*.52, 'VS Code')
        c.drawString(3*cm, H*.44, 'Extension')
        c.setFont('R',38); c.drawString(3*cm, H*.36, 'API')
        c.setStrokeColor(C['blue']); c.setLineWidth(2); c.line(3*cm,H*.33,14*cm,H*.33)
        c.setFont('I',14); c.setFillColor(C['lblue'])
        c.drawString(3*cm, H*.29, 'Architecture, API, UX, Testing, and Monetization')
        c.setFont('R',10.5); c.setFillColor(C['mgray'])
        c.drawString(3*cm, H*.25, 'Based on official Microsoft documentation and community experience')
        c.drawString(3*cm, H*.22, 'code.visualstudio.com/api  ·  github.com/microsoft/vscode')
        c.setFillColor(C['blue']); c.roundRect(3*cm,H*.15,110,22,4,fill=1,stroke=0)
        c.setFont('B',9.5); c.setFillColor(C['white'])
        c.drawCentredString(3*cm+55, H*.158, '2026 Edition  ·  160+ pages')
        chapters = [
            'Introduction — VS Code Architecture', 'First Extension: Hello World',
            'Extension Anatomy', 'Extension Capabilities',
            'Commands, Menus, and Settings', 'Color Themes',
            'Tree View API', 'Webview API',
            'Language Extensions + LSP', 'UX and Conflict Prevention',
            'Testing + Playwright E2E', 'Bundling and Publishing',
            'AI Extensions: Copilot Chat', 'Extension Monetization',
            'Yeoman vs npm create', 'Bun Compatibility',
            'Developer Tips & Tricks', 'API Reference',
        ]
        c.setFont('R', 7.5)
        for i, ch in enumerate(chapters):
            col = 0 if i < 9 else 1
            row = i if i < 9 else i - 9
            x = 3*cm + col*8.2*cm
            y = H*.9 - row*.87*cm
            c.setFillColor(C['blue']); c.circle(x-4*mm, y+2, 2.5, fill=1, stroke=0)
            c.setFillColor(HexColor('#B0BEC5')); c.drawString(x, y, ch)
        c.setFont('R',7.5); c.setFillColor(HexColor('#37474F'))
        c.drawCentredString(W/2, 1.4*cm, 'Visual Studio Code  •  Microsoft  •  Open Source MIT')
        c.restoreState()


def build_front_matter_no_toc(toc_flowable):
    """
    Cover + verso + dedication + auto-generated TOC page.
    toc_flowable — a TableOfContents instance populated during multiBuild.
    """
    A = []
    def add(*x):
        for i in x: A.append(i)

    # ── 1. COVER ─────────────────────────────────────────────────────────────
    add(CoverEn(), pb())

    # ── 2. VERSO (title page back) ───────────────────────────────────────────
    verso_style = ParagraphStyle(
        'verso2en', fontName='R', fontSize=9,
        textColor=HexColor('#555555'), leading=15,
        spaceAfter=6, alignment=TA_LEFT
    )
    verso_bold = ParagraphStyle(
        'verso_b2en', fontName='B', fontSize=9,
        textColor=HexColor('#333333'), leading=15,
        spaceAfter=4, alignment=TA_LEFT
    )
    verso_small = ParagraphStyle(
        'verso_s2en', fontName='I', fontSize=8,
        textColor=HexColor('#888888'), leading=13,
        spaceAfter=4, alignment=TA_LEFT
    )
    verso_title = ParagraphStyle(
        'verso_t2en', fontName='B', fontSize=16,
        textColor=C['blue'], leading=22,
        spaceAfter=8, alignment=TA_LEFT
    )
    add(sp(20))
    add(Paragraph('VS Code Extension API', verso_title))
    add(Paragraph('Extension Development: Architecture, API, UX, and Monetization', ParagraphStyle(
        'vt22en', fontName='I', fontSize=11, textColor=HexColor('#444444'),
        leading=16, spaceAfter=20
    )))
    add(hl(HexColor('#CCCCCC')))
    add(sp(12))
    add(Paragraph(
        'This book covers the entire journey of a VS Code extension developer — from the first '
        'Hello World command to publishing a language server, AI assistant, and monetization. '
        'The material is based on official Microsoft documentation, VS Code source code, '
        'real-world examples from popular extensions, and community experience.',
        verso_style
    ))
    add(sp(12))
    add(Paragraph('This book includes:', verso_bold))
    for item in [
        '18 core chapters with a complete breakdown of the Extension API',
        'VS Code and LSP architecture diagrams',
        'Practical examples from real-world extensions',
        'A chapter on UX and preventing conflicts between extensions',
        'Playwright E2E testing, Bun compatibility, Yeoman vs npm create',
        'A chapter on monetization: freemium, SaaS, OSS + sponsors',
        'Reference tables for all VS Code APIs, Contribution Points, and Activation Events',
        'Quotes from GitLens authors, the VS Code Team, and the creator of VS Code',
    ]:
        add(Paragraph(f'&bull; {item}', verso_style))
    add(sp(20))
    add(hl(HexColor('#CCCCCC')))
    add(sp(12))
    add(Paragraph('2026 Edition', verso_bold))
    add(sp(4))
    add(Paragraph('Based on official Microsoft documentation', verso_small))
    add(Paragraph(
        'Original documentation: &copy; Microsoft Corporation, '
        'published under Creative Commons Attribution license.',
        verso_small
    ))
    add(Paragraph('Code examples: MIT License, github.com/microsoft/vscode-extension-samples', verso_small))
    add(sp(8))
    add(Paragraph(
        'Diagrams, additional chapters, and adaptation: '
        'compiled from open sources and developer community experience.',
        verso_small
    ))
    add(sp(16))
    disclaimer_style = ParagraphStyle(
        'disc2en', fontName='I', fontSize=7.5,
        textColor=HexColor('#999999'), leading=11,
        spaceAfter=3, alignment=TA_LEFT
    )
    add(hl(HexColor('#DDDDDD')))
    add(sp(6))
    add(Paragraph(
        'Information in this book is provided "as is". VS Code and its Extension API '
        'are updated monthly — for the latest documentation refer to '
        'code.visualstudio.com/api. All trademarks mentioned belong to their respective owners.',
        disclaimer_style
    ))
    add(pb())

    # ── 3. DEDICATION ────────────────────────────────────────────────────────
    ded_style = ParagraphStyle(
        'ded2en', fontName='I', fontSize=14,
        textColor=HexColor('#333333'), leading=22,
        alignment=TA_CENTER
    )
    ded_line = ParagraphStyle(
        'dedl2en', fontName='R', fontSize=9,
        textColor=HexColor('#AAAAAA'), leading=14,
        alignment=TA_CENTER
    )
    add(sp(180))
    add(Paragraph('Dedicated to Lena', ded_style))
    add(sp(12))
    add(Paragraph('— with gratitude for patience and inspiration', ded_line))
    add(pb())

    # ── 4. TABLE OF CONTENTS (auto-generated) ────────────────────────────────
    toc_title_style = ParagraphStyle(
        'toc_title_en', fontName='B', fontSize=20,
        textColor=C['blue'], spaceBefore=16, spaceAfter=8,
        leading=26, alignment=TA_LEFT
    )
    add(Paragraph('Table of Contents', toc_title_style), hl(C['blue']), sp(12))
    add(toc_flowable)
    add(pb())

    return A
