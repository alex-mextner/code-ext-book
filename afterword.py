"""afterword.py — Послесловие (в конце книги, после справочников)"""
from book_helpers import *

def build_afterword():
    A = []
    def add(*x):
        for i in x: A.append(i)

    add(pb())
    add(toc_ch('Послесловие'))
    add(banner('—', 'Послесловие', 'Экосистема, сообщество и дальнейшее развитие'), sp(12))

    add(h2('Экосистема расширений'))
    add(p('Более 60 000 расширений доступны в VS Code Marketplace. VS Code обновляется ежемесячно, '
          'и Extension API получает новые возможности с каждым выпуском. '
          'Самые популярные категории в 2026 году:'))
    add(sp(2))
    for item in [
        '<b>AI-ассистенты:</b> GitHub Copilot, Codeium, Tabnine',
        '<b>Языковые серверы:</b> Pylance (Python), rust-analyzer, clangd (C++)',
        '<b>Форматтеры:</b> Prettier, Black, ESLint',
        '<b>Темы:</b> One Dark Pro, Dracula, Catppuccin, Nord',
        '<b>Git:</b> GitLens, Git Graph',
        '<b>Remote Dev:</b> Remote SSH, Dev Containers, Codespaces',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Полезные ресурсы'))
    add(tblh(['Ресурс', 'Описание']))
    add(tbl2([
        ('code.visualstudio.com/api',                      'Официальная документация Extension API'),
        ('github.com/microsoft/vscode-extension-samples',  'Примеры для всех API'),
        ('github.com/microsoft/vscode-discussions',        'Форум разработчиков расширений'),
        ('stackoverflow.com/questions/tagged/vscode-extensions', 'Stack Overflow'),
        ('vscode-dev-community.slack.com',                 'Slack-сообщество разработчиков'),
        ('marketplace.visualstudio.com/vscode',            'VS Code Marketplace'),
        ('open-vsx.org',                                   'Open VSX Registry для Cursor, VSCodium'),
        ('github.com/microsoft/vscode',                    'Исходный код VS Code'),
    ]))
    add(sp(6))

    add(screenshot('cockpit.jpg', ''))
    add(sp(4))
    add(p('Вы изучили приборную панель. Теперь — взлёт.'))
    add(sp(8))

    add(h2('Следующие шаги'))
    for item in [
        'Изучить исходный код популярных расширений на GitHub',
        'Пройти официальные туториалы на code.visualstudio.com/api',
        'Участвовать в дискуссиях на github.com/microsoft/vscode-discussions',
        'Следить за monthly release notes — новые API каждый месяц',
        'Звёздочка vscode-extension-samples — там появляются примеры новых API',
    ]:
        add(bul(item))
    add(sp(8))

    add(box('Репозиторий книги',
        'Исходный код этой книги открыт: <b>github.com/alex-mextner/code-ext-book</b>. '
        'Нашли ошибку, устаревшую информацию или хотите предложить улучшение? '
        'Создайте Issue или Pull Request — мы ценим каждый вклад.', 'tip'))
    add(sp(8))

    add(hl(C['blue'], 1.5))
    add(sp(4))
    add(p(
        '<i>Автор: Alex (t.me/mxtnr) — CTO HyperIDE. '
        'На основе официальной документации Visual Studio Code Extension API (Microsoft). '
        'Лицензия: CC BY-SA 4.0. Версия март 2026.</i>',
        'bodyi'
    ))
    return A
