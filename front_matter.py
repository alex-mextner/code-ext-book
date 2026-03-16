"""
front_matter.py — обложка, оборот, посвящение, оглавление
"""
from book_helpers import *
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import NextPageTemplate

def build_front_matter():
    A = []
    def add(*x):
        for i in x: A.append(i)

    # ── 1. ОБЛОЖКА (full-bleed, no margins) ──────────────────────────────────
    add(Cover(), NextPageTemplate('main'), pb())

    # ── 2. ОБОРОТ ТИТУЛА (verso) ────────────────────────────────────────────
    # Традиционно левая страница после обложки — выходные данные
    verso_style = ParagraphStyle(
        'verso', fontName='R', fontSize=9,
        textColor=HexColor('#555555'), leading=15,
        spaceAfter=6, alignment=TA_LEFT
    )
    verso_bold = ParagraphStyle(
        'verso_b', fontName='B', fontSize=9,
        textColor=HexColor('#333333'), leading=15,
        spaceAfter=4, alignment=TA_LEFT
    )
    verso_small = ParagraphStyle(
        'verso_s', fontName='I', fontSize=8,
        textColor=HexColor('#888888'), leading=13,
        spaceAfter=4, alignment=TA_LEFT
    )
    verso_title = ParagraphStyle(
        'verso_t', fontName='B', fontSize=16,
        textColor=C['blue'], leading=22,
        spaceAfter=8, alignment=TA_LEFT
    )

    # Верхняя часть — название и описание
    add(sp(20))
    add(Paragraph('VS Code Extension API', verso_title))
    add(Paragraph('Разработка расширений: архитектура, API, UX и монетизация', ParagraphStyle(
        'vt2', fontName='I', fontSize=11, textColor=HexColor('#444444'),
        leading=16, spaceAfter=20
    )))

    add(hl(HexColor('#CCCCCC')))
    add(sp(12))

    add(Paragraph(
        'Книга охватывает весь путь разработчика расширений VS Code — от первой команды '
        'Hello World до публикации языкового сервера, AI-ассистента и монетизации. '
        'Материал основан на официальной документации Microsoft, исходном коде VS Code, '
        'реальных примерах из популярных расширений и опыте сообщества разработчиков.',
        verso_style
    ))
    add(sp(12))

    add(Paragraph(
        'Книга включает:', verso_bold
    ))
    for item in [
        '18 основных глав с полным разбором Extension API',
        'Диаграммы архитектуры VS Code и LSP',
        'Практические примеры из реальных расширений',
        'Главу по UX и предотвращению конфликтов между расширениями',
        'Playwright E2E тестирование, Bun совместимость, Yeoman vs npm create',
        'Главу по монетизации: freemium, SaaS, OSS + sponsors',
        'Справочник всех VS Code API, Contribution Points и Activation Events',
        'Цитаты авторов GitLens, VS Code Team, создателя VS Code',
    ]:
        add(Paragraph(f'• {item}', verso_style))
    add(sp(20))

    add(hl(HexColor('#CCCCCC')))
    add(sp(12))

    # Нижняя часть — выходные данные
    add(Paragraph('Автор: Alex — CTO HyperIDE, 15 лет в разработке', verso_bold))
    add(Paragraph('t.me/mxtnr  •  github.com/alex-mextner/code-ext-book', verso_style))
    add(sp(8))
    add(Paragraph('Издание 2026 года', verso_bold))
    add(sp(4))
    add(Paragraph(
        'На основе официальной документации Microsoft VS Code Extension API.',
        verso_small
    ))
    add(Paragraph(
        'Исходная документация: © Microsoft Corporation, '
        'опубликована под лицензией Creative Commons Attribution.',
        verso_small
    ))
    add(Paragraph(
        'Примеры кода: MIT License, '
        'github.com/microsoft/vscode-extension-samples',
        verso_small
    ))
    add(sp(16))

    # Отказ от ответственности
    disclaimer_style = ParagraphStyle(
        'disc', fontName='I', fontSize=7.5,
        textColor=HexColor('#999999'), leading=11,
        spaceAfter=3, alignment=TA_LEFT
    )
    add(hl(HexColor('#DDDDDD')))
    add(sp(6))
    add(Paragraph(
        'Информация в этой книге предоставлена "как есть". VS Code и его Extension API '
        'обновляются ежемесячно — за актуальной документацией обращайтесь на '
        'code.visualstudio.com/api. Все упомянутые торговые марки принадлежат '
        'их владельцам.',
        disclaimer_style
    ))
    add(pb())

    # ── 3. ПОСВЯЩЕНИЕ ────────────────────────────────────────────────────────
    # Пустая страница с посвящением — традиционно по центру правой страницы

    ded_style = ParagraphStyle(
        'ded', fontName='I', fontSize=14,
        textColor=HexColor('#333333'), leading=22,
        alignment=TA_CENTER
    )
    ded_line = ParagraphStyle(
        'dedl', fontName='R', fontSize=9,
        textColor=HexColor('#AAAAAA'), leading=14,
        alignment=TA_CENTER
    )

    # Вертикальный отступ ~⅓ страницы
    add(sp(180))
    add(Paragraph('Посвящаю своей любовнице Лене', ded_style))
    add(sp(12))
    add(Paragraph('— с благодарностью за терпение и вдохновение', ded_line))
    add(pb())

    # ── 4. СОДЕРЖАНИЕ ────────────────────────────────────────────────────────
    add(h1('Содержание'), hl(C['blue']), sp(8))

    toc = [
        ('Введение',         'VS Code как платформа — история и архитектура'),
        ('Глава 1',          'Первое расширение — Hello World'),
        ('Глава 2',          'Анатомия расширения'),
        ('Глава 3',          'Возможности расширений — обзор категорий'),
        ('Глава 4',          'Команды, меню и настройки'),
        ('Глава 5',          'Темы оформления'),
        ('Глава 6',          'Tree View API'),
        ('Глава 7',          'Webview API'),
        ('Глава 8',          'Custom Editors и Virtual Documents'),
        ('Глава 9',          'Языковые расширения'),
        ('Глава 10',         'Language Server Protocol (LSP)'),
        ('Глава 11',         'UX Guidelines — официальные принципы'),
        ('Глава 12',         'Тестирование расширений (@vscode/test-cli + Playwright E2E)'),
        ('Глава 13',         'Бандлинг с esbuild и webpack'),
        ('Глава 14',         'Публикация в Marketplace и Open VSX'),
        ('Глава 15',         'CI/CD автоматизация'),
        ('Глава 16',         'Extension Host — архитектура'),
        ('Глава 17',         'AI-расширения: Chat Participant и Language Model'),
        ('Глава 18',         'Language Model Tools и MCP'),
        ('─────────', ''),
        ('Раздел',            'Пользовательский опыт — конфликты и обнаруживаемость'),
        ('Раздел',            'Практика — реальные расширения с полным кодом'),
        ('Глава 19',          'Монетизация VS Code расширений'),
        ('─────────', ''),
        ('Раздел',            'Что делает VS Code быстрым — уроки для расширений'),
        ('Раздел',            '41 совет из реального мира + чек-листы'),
        ('─────────', ''),
        ('Справочник A',     'VS Code API — все ключевые namespace с методами'),
        ('Справочник B',     'Contribution Points — полный список'),
        ('Справочник C',     'Activation Events — полный список'),
        ('Справочник D',     'CSS-переменные тем для Webview'),
        ('Глоссарий',        'Ключевые термины и аббревиатуры'),
        ('Послесловие',      'Экосистема, сообщество и дальнейшее развитие'),
    ]

    sep_style = ParagraphStyle(
        'sep', fontName='R', fontSize=7,
        textColor=HexColor('#CCCCCC'), leading=10,
        spaceAfter=2, spaceBefore=4
    )

    for num, title in toc:
        if num.startswith('─'):
            add(Paragraph('· · ·', sep_style))
        elif title:
            add(p(f'<b>{num}</b>  {title}', 'toc1'), sp(2))
        else:
            add(p(f'<b>{num}</b>', 'toc1'), sp(2))

    add(pb())

    return A


if __name__ == '__main__':
    print(f'Front matter: {len(build_front_matter())} elements')


def build_front_matter_no_toc(toc_flowable):
    """
    Обложка + оборот + посвящение + страница оглавления с автоматическим TOC.
    toc_flowable — экземпляр TableOfContents, заполняемый при multiBuild.
    """
    A = []
    def add(*x):
        for i in x: A.append(i)

    # ── 1. ОБЛОЖКА (full-bleed, no margins) ──────────────────────────────────
    add(Cover(), NextPageTemplate('main'), pb())

    # ── 2. ОБОРОТ ТИТУЛА ────────────────────────────────────────────────────
    verso_style = ParagraphStyle(
        'verso2', fontName='R', fontSize=9,
        textColor=HexColor('#555555'), leading=15,
        spaceAfter=6, alignment=TA_LEFT
    )
    verso_bold = ParagraphStyle(
        'verso_b2', fontName='B', fontSize=9,
        textColor=HexColor('#333333'), leading=15,
        spaceAfter=4, alignment=TA_LEFT
    )
    verso_small = ParagraphStyle(
        'verso_s2', fontName='I', fontSize=8,
        textColor=HexColor('#888888'), leading=13,
        spaceAfter=4, alignment=TA_LEFT
    )
    verso_title = ParagraphStyle(
        'verso_t2', fontName='B', fontSize=16,
        textColor=C['blue'], leading=22,
        spaceAfter=8, alignment=TA_LEFT
    )
    add(sp(20))
    add(Paragraph('VS Code Extension API', verso_title))
    add(Paragraph('Разработка расширений: архитектура, API, UX и монетизация', ParagraphStyle(
        'vt22', fontName='I', fontSize=11, textColor=HexColor('#444444'),
        leading=16, spaceAfter=20
    )))
    add(hl(HexColor('#CCCCCC')))
    add(sp(12))
    add(Paragraph(
        'Книга охватывает весь путь разработчика расширений VS Code — от первой команды '
        'Hello World до публикации языкового сервера, AI-ассистента и монетизации. '
        'Материал основан на официальной документации Microsoft, исходном коде VS Code, '
        'реальных примерах из популярных расширений и опыте сообщества разработчиков.',
        verso_style
    ))
    add(sp(12))
    add(Paragraph('Книга включает:', verso_bold))
    for item in [
        '18 основных глав с полным разбором Extension API',
        'Диаграммы архитектуры VS Code и LSP',
        'Практические примеры из реальных расширений',
        'Главу по UX и предотвращению конфликтов между расширениями',
        'Playwright E2E тестирование, Bun совместимость, Yeoman vs npm create',
        'Главу по монетизации: freemium, SaaS, OSS + sponsors',
        'Справочник всех VS Code API, Contribution Points и Activation Events',
        'Цитаты авторов GitLens, VS Code Team, создателя VS Code',
    ]:
        add(Paragraph(f'• {item}', verso_style))
    add(sp(20))
    add(hl(HexColor('#CCCCCC')))
    add(sp(12))
    add(Paragraph('Издание 2026 года', verso_bold))
    add(sp(4))
    add(Paragraph('Перевод и адаптация: на основе официальной документации Microsoft', verso_small))
    add(Paragraph(
        'Исходная документация: © Microsoft Corporation, '
        'опубликована под лицензией Creative Commons Attribution.',
        verso_small
    ))
    add(Paragraph('Примеры кода: MIT License, github.com/microsoft/vscode-extension-samples', verso_small))
    add(sp(8))
    add(Paragraph(
        'Диаграммы, перевод, дополнительные главы и адаптация: '
        'составлены на основе открытых источников и опыта сообщества разработчиков.',
        verso_small
    ))
    add(sp(16))
    disclaimer_style = ParagraphStyle(
        'disc2', fontName='I', fontSize=7.5,
        textColor=HexColor('#999999'), leading=11,
        spaceAfter=3, alignment=TA_LEFT
    )
    add(hl(HexColor('#DDDDDD')))
    add(sp(6))
    add(Paragraph(
        'Информация в этой книге предоставлена "как есть". VS Code и его Extension API '
        'обновляются ежемесячно — за актуальной документацией обращайтесь на '
        'code.visualstudio.com/api. Все упомянутые торговые марки принадлежат их владельцам.',
        disclaimer_style
    ))
    add(pb())

    # ── 3. ПОСВЯЩЕНИЕ ────────────────────────────────────────────────────────
    ded_style = ParagraphStyle(
        'ded2', fontName='I', fontSize=14,
        textColor=HexColor('#333333'), leading=22,
        alignment=TA_CENTER
    )
    ded_line = ParagraphStyle(
        'dedl2', fontName='R', fontSize=9,
        textColor=HexColor('#AAAAAA'), leading=14,
        alignment=TA_CENTER
    )
    add(sp(180))
    add(Paragraph('Посвящаю своей любовнице Лене', ded_style))
    add(sp(12))
    add(Paragraph('— с благодарностью за терпение и вдохновение', ded_line))
    add(pb())

    # ── 4. ОГЛАВЛЕНИЕ (автоматическое) ──────────────────────────────────────
    # Используем отдельный стиль 'toc_title' чтобы afterFlowable не добавлял
    # само оглавление в себя (стиль 'h1' отслеживается, 'toc_title' — нет)
    toc_title_style = ParagraphStyle(
        'toc_title', fontName='B', fontSize=20,
        textColor=C['blue'], spaceBefore=16, spaceAfter=8,
        leading=26, alignment=TA_LEFT
    )
    add(Paragraph('Содержание', toc_title_style), hl(C['blue']), sp(12))
    add(toc_flowable)
    add(pb())

    return A
