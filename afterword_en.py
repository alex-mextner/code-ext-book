"""afterword_en.py — Afterword (at the end of the book, after appendices)"""
from book_helpers import *

def build_afterword():
    A = []
    def add(*x):
        for i in x: A.append(i)

    add(pb())
    add(toc_ch('Afterword'))
    add(banner('—', 'Afterword', 'Ecosystem, community, and further development'), sp(12))

    add(h2('The Extension Ecosystem'))
    add(p('Over 60,000 extensions are available on the VS Code Marketplace. VS Code is updated monthly, '
          'and the Extension API gains new capabilities with every release. '
          'The most popular categories in 2026:'))
    add(sp(2))
    for item in [
        '<b>AI Assistants:</b> GitHub Copilot, Codeium, Tabnine',
        '<b>Language Servers:</b> Pylance (Python), rust-analyzer, clangd (C++)',
        '<b>Formatters:</b> Prettier, Black, ESLint',
        '<b>Themes:</b> One Dark Pro, Dracula, Catppuccin, Nord',
        '<b>Git:</b> GitLens, Git Graph',
        '<b>Remote Dev:</b> Remote SSH, Dev Containers, Codespaces',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Useful Resources'))
    add(tblh(['Resource', 'Description']))
    add(tbl2([
        ('code.visualstudio.com/api',                      'Official Extension API documentation'),
        ('github.com/microsoft/vscode-extension-samples',  'Samples for all APIs'),
        ('github.com/microsoft/vscode-discussions',        'Extension developer forum'),
        ('stackoverflow.com/questions/tagged/vscode-extensions', 'Stack Overflow'),
        ('vscode-dev-community.slack.com',                 'Developer Slack community'),
        ('marketplace.visualstudio.com/vscode',            'VS Code Marketplace'),
        ('open-vsx.org',                                   'Open VSX Registry for Cursor, VSCodium'),
        ('github.com/microsoft/vscode',                    'VS Code source code'),
    ]))
    add(sp(6))

    add(h2('Next Steps'))
    for item in [
        'Study the source code of popular extensions on GitHub',
        'Follow the official tutorials at code.visualstudio.com/api',
        'Participate in discussions at github.com/microsoft/vscode-discussions',
        'Follow the monthly release notes — new APIs every month',
        'Star vscode-extension-samples — new API samples appear there',
    ]:
        add(bul(item))
    add(sp(8))

    add(hl(C['blue'], 1.5))
    add(sp(4))
    add(p(
        '<i>This book is a translation and adaptation of the official '
        'Visual Studio Code Extension API documentation (Microsoft, MIT License). '
        'All code examples are taken from official Microsoft repositories and adapted. '
        'Version March 2026.</i>',
        'bodyi'
    ))
    return A
