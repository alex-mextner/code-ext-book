"""
front_matter_en.py — English edition: cover, verso, dedication, table of contents
"""
from book_helpers import *
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class CoverEn(Flowable):
    """English cover — reuses the same Cover class from book_helpers."""
    def wrap(self, aw, ah): return W, H
    def draw(self):
        # Same cover for both languages — title is in English anyway
        Cover().drawOn(self.canv, 0, 0)


def build_front_matter_no_toc(toc_flowable):
    """
    Cover + verso + dedication + auto-generated TOC page.
    toc_flowable — a TableOfContents instance populated during multiBuild.
    """
    A = []
    def add(*x):
        for i in x: A.append(i)

    # ── 1. COVER ─────────────────────────────────────────────────────────────
    from reportlab.platypus import NextPageTemplate
    add(CoverEn(), NextPageTemplate('main'), pb())

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
    add(Paragraph('Author: Alex — CTO HyperIDE, 15 years in software development', verso_bold))
    add(Paragraph('t.me/mxtnr  &bull;  github.com/alex-mextner/code-ext-book', verso_style))
    add(sp(8))
    add(Paragraph('2026 Edition', verso_bold))
    add(sp(4))
    add(Paragraph(
        'Based on official Microsoft VS Code Extension API documentation.',
        verso_small
    ))
    add(Paragraph(
        'Original documentation: &copy; Microsoft Corporation, '
        'published under Creative Commons Attribution license.',
        verso_small
    ))
    add(Paragraph('Code examples: MIT License, github.com/microsoft/vscode-extension-samples', verso_small))
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
