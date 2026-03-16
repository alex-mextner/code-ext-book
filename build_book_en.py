"""build_book_en.py — English edition: 2-pass PDF with clickable TOC via AnchorFlowable."""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import book_helpers
from book_helpers import *
from front_matter_en import build_front_matter_no_toc
from book_part1_en import build_story
from book_part2_en import build_story_part2
from book_part3_en import build_story_part3
from book_part4_en import build_story_part4
from book_ux_en import build_story_ux
from book_new_en import build_story_new
from book_perf_en import build_perf_chapter
from book_appendices_en import build_appendices
from afterword_en import build_afterword

from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

_default_out = '/mnt/user-data/outputs/vscode-extensions-complete-guide.pdf'
OUT = _default_out if os.path.isdir(os.path.dirname(_default_out)) else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vscode-extensions-complete-guide-en.pdf')


class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        cover_frame = Frame(0, 0, A4[0], A4[1], id='cover',
                            leftPadding=0, rightPadding=0,
                            topPadding=0, bottomPadding=0)
        content_frame = Frame(self.leftMargin, self.bottomMargin,
                              self.width, self.height, id='main')
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[cover_frame],
                         onPage=self._on_cover_page),
            PageTemplate(id='main', frames=[content_frame],
                         onPage=self._on_content_page),
        ])

    def _on_cover_page(self, canvas, doc):
        pass

    def _on_content_page(self, canvas, doc):
        on_later_pages_en(canvas, doc)

    def afterFlowable(self, flowable):
        """Catch AnchorFlowable instances and register TOC entries."""
        if isinstance(flowable, AnchorFlowable):
            self.notify('TOCEntry', (flowable.level, flowable.title,
                                     self.page, flowable.key))


def on_later_pages_en(canvas, doc):
    """English page header/footer."""
    canvas.saveState()
    canvas.setStrokeColor(C['border']); canvas.setLineWidth(.5)
    canvas.line(ML, H-1.3*cm, W-MR, H-1.3*cm)
    canvas.setFont('R',8); canvas.setFillColor(C['mgray'])
    canvas.drawString(ML, H-1.1*cm, 'VS Code Extension API — The Complete Developer Guide')
    canvas.drawRightString(W-MR, H-1.1*cm, f'p. {doc.page}')
    canvas.setLineWidth(.5); canvas.line(ML,1.3*cm,W-MR,1.3*cm)
    canvas.setFont('R',7.5)
    canvas.drawCentredString(W/2, 1.0*cm, 'code.visualstudio.com/api  •  github.com/microsoft/vscode  •  2026')
    canvas.restoreState()


def build_toc():
    toc = TableOfContents()
    toc.dotsMinLevel = 0
    toc.levelStyles = [
        ParagraphStyle('TOC0', fontName='B', fontSize=11,
                       textColor=HexColor('#007ACC'),
                       spaceBefore=7, spaceAfter=2,
                       leftIndent=0, leading=16),
        ParagraphStyle('TOC1', fontName='R', fontSize=9.5,
                       textColor=HexColor('#444444'),
                       spaceBefore=1, spaceAfter=1,
                       leftIndent=16, leading=14),
    ]
    return toc


toc = build_toc()

full_story = (
    build_front_matter_no_toc(toc) +
    build_story() +
    build_story_part2() +
    build_story_part3() +
    build_story_ux() +
    build_perf_chapter() +
    build_story_new() +
    build_story_part4() +
    build_appendices() +
    build_afterword()
)

print(f'Story elements: {len(full_story)}')

doc = BookDocTemplate(
    OUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR,
    topMargin=2.0*cm + 0.5*cm,
    bottomMargin=1.8*cm + 0.3*cm,
    title='VS Code Extension API — The Complete Developer Guide',
    author='Alex (t.me/mxtnr) — CTO HyperIDE',
    subject='Visual Studio Code Extensions',
    creator='Claude / Anthropic',
)

print('Building (2-pass)...')
doc.multiBuild(full_story)
print(f'Done: {OUT}')
