"""build_book.py — 2-pass PDF with clickable TOC via AnchorFlowable."""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import book_helpers
from book_helpers import *
from front_matter import build_front_matter_no_toc
from book_part1 import build_story
from book_part2 import build_story_part2
from book_part3 import build_story_part3
from book_part4 import build_story_part4
from book_ux import build_story_ux
from book_new import build_story_new
from book_perf import build_perf_chapter
from book_appendices import build_appendices
from afterword import build_afterword

from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

_default_out = '/mnt/user-data/outputs/vscode-extensions-полное-руководство.pdf'
OUT = _default_out if os.path.isdir(os.path.dirname(_default_out)) else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vscode-extensions-complete-guide-ru.pdf')


class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin,
                      self.width, self.height, id='main')
        self.addPageTemplates([
            PageTemplate(id='main', frames=[frame], onPage=self._on_page)
        ])

    def _on_page(self, canvas, doc):
        on_later_pages(canvas, doc)

    def afterFlowable(self, flowable):
        """Catch AnchorFlowable instances and register TOC entries."""
        if isinstance(flowable, AnchorFlowable):
            self.notify('TOCEntry', (flowable.level, flowable.title,
                                     self.page, flowable.key))


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
    title='VS Code Extension API — Полное руководство разработчика',
    author='На основе документации Microsoft и опыта сообщества',
    subject='Visual Studio Code Extensions',
    creator='Claude / Anthropic',
)

print('Building (2-pass)...')
doc.multiBuild(full_story)
print(f'Done: {OUT}')
