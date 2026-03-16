"""
book_appendices.py — Справочники A/B/C + CSS-токены Webview
Перемещены в конец книги.
"""
from book_helpers import *


def build_appendices():
    A = []
    def add(*x):
        for i in x: A.append(i)
    def ch(num, title, sub=''):
        part = f'Справочник {num}'
        # Stable bookmark for cross-references: <a href="#appendix_A"> etc.
        add(StableAnchor(f'appendix_{num}'))
        add(toc_ch(f'{part}: {title}'), banner(part, title, sub), sp(12))

    # ── СПРАВОЧНИК A ───────────────────────────────────────────────────────────
    ch('A', 'VS Code API', 'Ключевые методы по namespace')
    add(p('Актуальная версия: <b>code.visualstudio.com/api/references/vscode-api</b>'))
    add(sp(4))

    add(h2('vscode.window'))
    add(tblh(['Метод / Свойство', 'Описание']))
    add(tbl2([
        ('showInformationMessage(msg, ...items)', 'Информационное уведомление, возвращает выбранный item'),
        ('showWarningMessage(msg, ...items)',     'Предупреждение'),
        ('showErrorMessage(msg, ...items)',       'Сообщение об ошибке'),
        ('showInputBox(options)',                  'Поле ввода. Promise<string | undefined>'),
        ('showQuickPick(items, options)',          'Список выбора. Возвращает выбранный элемент'),
        ('showOpenDialog(options)',                'Диалог выбора файлов. Возвращает Uri[]'),
        ('showSaveDialog(options)',                'Диалог сохранения'),
        ('showTextDocument(doc, options)',         'Открыть TextDocument в редакторе'),
        ('createWebviewPanel(type,title,col,opt)', 'Создать Webview панель'),
        ('createTreeView(viewId, options)',        'Tree View с полным контролем'),
        ('createStatusBarItem(align, priority)',   'Элемент Status Bar'),
        ('createOutputChannel(name)',              'Канал вывода'),
        ('createTerminal(options)',                'Встроенный терминал'),
        ('withProgress(options, task)',            'Выполнить задачу с прогрессом'),
        ('activeTextEditor',                       'Активный TextEditor или undefined'),
        ('visibleTextEditors',                     'Все видимые редакторы'),
        ('onDidChangeActiveTextEditor',            'Событие: смена активного редактора'),
    ], 0.48))
    add(sp(6))

    add(h2('vscode.workspace'))
    add(tblh(['Метод / Свойство', 'Описание']))
    add(tbl2([
        ('workspaceFolders',                    'Массив открытых папок рабочего пространства'),
        ('openTextDocument(uri | path)',         'Открыть документ. Promise<TextDocument>'),
        ('getConfiguration(section)',            'Получить WorkspaceConfiguration'),
        ('findFiles(pattern, exclude)',          'Поиск файлов по glob'),
        ('createFileSystemWatcher(glob)',        'Следить за изменениями файлов'),
        ('applyEdit(edit)',                      'Применить WorkspaceEdit'),
        ('fs',                                   'vscode.FileSystem — API файловой системы'),
        ('onDidOpenTextDocument',                'Событие: открытие документа'),
        ('onDidChangeTextDocument',              'Событие: изменение документа'),
        ('onDidSaveTextDocument',                'Событие: сохранение документа'),
        ('onDidCloseTextDocument',               'Событие: закрытие документа'),
        ('registerTextDocumentContentProvider', 'Провайдер виртуальных документов'),
    ], 0.48))
    add(sp(6))

    add(h2('vscode.languages'))
    add(tblh(['Метод', 'Описание']))
    add(tbl2([
        ('createDiagnosticCollection(name)',               'Создать коллекцию диагностик'),
        ('registerCompletionItemProvider(sel, prov, ...)', 'Провайдер автодополнения'),
        ('registerHoverProvider(sel, provider)',           'Hover-провайдер'),
        ('registerDefinitionProvider(sel, provider)',      'Go-to-definition провайдер'),
        ('registerReferenceProvider(sel, provider)',       'Find-references провайдер'),
        ('registerCodeActionsProvider(sel, provider)',     'Code Actions провайдер'),
        ('registerDocumentFormattingEditProvider(sel,prov)','Форматтер'),
        ('registerDocumentHighlightProvider(sel, prov)',   'Highlight провайдер'),
        ('registerRenameProvider(sel, provider)',          'Rename провайдер'),
        ('registerSignatureHelpProvider(sel, prov, ...)',  'Signature help провайдер'),
        ('getDiagnostics(uri)',                            'Получить диагностики для URI'),
    ], 0.55))
    add(pb())

    # ── СПРАВОЧНИК B ───────────────────────────────────────────────────────────
    ch('B', 'Contribution Points', 'Полный список точек расширения VS Code')
    add(p('Актуальная версия: <b>code.visualstudio.com/api/references/contribution-points</b>'))
    add(sp(4))

    add(tblh(['Contribution Point', 'Назначение']))
    add(tbl2([
        ('contributes.commands',          'Команды: title, category, icon → Command Palette'),
        ('contributes.menus',             'Пункты в 20+ местах: editor/context, explorer/context, view/title...'),
        ('contributes.keybindings',       'Горячие клавиши: key, command, when, mac'),
        ('contributes.configuration',     'Настройки в Settings UI: properties с типами и defaults'),
        ('contributes.configurationDefaults','Defaults для конкретных языков'),
        ('contributes.languages',         'Язык: id, aliases, extensions, configuration, icon'),
        ('contributes.grammars',          'TextMate-грамматики для синтаксической подсветки'),
        ('contributes.snippets',          'Файлы сниппетов для языков'),
        ('contributes.themes',            'Цветовые темы редактора и UI'),
        ('contributes.iconThemes',        'Темы иконок файлов'),
        ('contributes.productIconThemes', 'Темы иконок интерфейса VS Code'),
        ('contributes.views',             'Tree View: id, name, icon, contextualTitle'),
        ('contributes.viewsContainers',   'Контейнеры для View в Activity Bar или Panel'),
        ('contributes.viewsWelcome',      'Приветственный контент для пустых View'),
        ('contributes.taskDefinitions',   'Типы задач для Task Provider'),
        ('contributes.problemMatchers',   'Паттерны парсинга вывода задач для ошибок'),
        ('contributes.debuggers',         'Debug Adapter: type, label, languages'),
        ('contributes.breakpoints',       'Типы breakpoints для языков'),
        ('contributes.walkthroughs',      'Пошаговые туториалы: id, title, steps'),
        ('contributes.chatParticipants',  'AI Chat Participants: id, name, commands'),
        ('contributes.languageModels',    'Кастомные Language Model провайдеры'),
        ('contributes.colors',            'Новые цвета для тем: id, description, defaults'),
        ('contributes.customEditors',     'Кастомные редакторы: viewType, selector, priority'),
        ('contributes.notebooks',         'Кастомные форматы ноутбуков'),
        ('contributes.authentication',    'Authentication Provider: id, label'),
        ('contributes.jsonValidation',    'JSON Schema валидация по URL-паттерну'),
        ('contributes.mcpServerDefinitionProviders', 'MCP Server провайдеры для AI'),
    ]))
    add(pb())

    # ── СПРАВОЧНИК C ───────────────────────────────────────────────────────────
    ch('C', 'Activation Events', 'Полный список событий активации')
    add(p('Актуальная версия: <b>code.visualstudio.com/api/references/activation-events</b>'))
    add(sp(4))

    add(tblh(['Событие', 'Когда срабатывает']))
    add(tbl2([
        ('onCommand:id',             'При первом вызове команды с указанным ID'),
        ('onLanguage:langId',        'При открытии файла с указанным языком'),
        ('onView:viewId',            'При первом открытии View'),
        ('onViewContainer:id',       'При открытии контейнера View'),
        ('workspaceContains:pattern','Если workspace содержит файл по паттерну'),
        ('onFileSystem:scheme',      'При доступе к файлу с нестандартной URI-схемой'),
        ('onUri',                    'При открытии vscode://publisher.extension URI'),
        ('onWebviewPanel:viewType',  'При восстановлении Webview после перезапуска VS Code'),
        ('onCustomEditor:viewType',  'При открытии кастомного редактора'),
        ('onNotebook:type',          'При открытии Notebook указанного типа'),
        ('onDebug',                  'При любом запуске отладки'),
        ('onDebugResolve:type',      'При разрешении конфигурации отладки'),
        ('onStartupFinished',        'После полной загрузки VS Code — не блокирует старт'),
        ('onTaskType:type',          'При выполнении задачи указанного типа'),
        ('onChatParticipant:id',     'При вызове AI Chat Participant'),
        ('onAuthenticationRequest',  'При запросе аутентификации'),
        ('*',                        'ИЗБЕГАЙТЕ: при каждом запуске VS Code'),
    ]))
    add(sp(4))
    add(box('Автоматические Activation Events (VS Code 1.74+)',
        'Команды, View, customEditors и другие contributions автоматически создают '
        'соответствующие Activation Events — объявлять явно не нужно. '
        'Явно нужны только: workspaceContains, onStartupFinished, onUri, '
        'onFileSystem, onAuthenticationRequest.',
        'note'))
    add(pb())

    # ── СПРАВОЧНИК D — CSS-переменные Webview ─────────────────────────────────
    ch('D', 'CSS-переменные тем VS Code', 'Для использования в Webview')
    add(p('Полный список токенов: <b>code.visualstudio.com/api/references/theme-color</b>. '
          'Используйте эти переменные в CSS Webview чтобы интерфейс автоматически '
          'адаптировался при смене темы пользователем.'))
    add(sp(4))

    add(h2('Основные переменные редактора'))
    add(tblh(['CSS-переменная', 'Назначение']))
    add(tbl2([
        ('--vscode-editor-background',        'Фон редактора'),
        ('--vscode-editor-foreground',        'Текст редактора'),
        ('--vscode-editor-font-family',       'Шрифт редактора'),
        ('--vscode-editor-font-size',         'Размер шрифта редактора'),
        ('--vscode-editor-font-weight',       'Жирность шрифта'),
        ('--vscode-editorLineNumber-foreground', 'Цвет номеров строк'),
        ('--vscode-editorCursor-foreground',  'Цвет курсора'),
        ('--vscode-editor-selectionBackground','Фон выделения'),
    ], 0.55))
    add(sp(4))

    add(h2('UI-элементы'))
    add(tblh(['CSS-переменная', 'Назначение']))
    add(tbl2([
        ('--vscode-button-background',        'Фон кнопки'),
        ('--vscode-button-foreground',        'Текст кнопки'),
        ('--vscode-button-hoverBackground',   'Фон кнопки при наведении'),
        ('--vscode-button-border',            'Рамка кнопки (может быть transparent)'),
        ('--vscode-button-secondaryBackground',     'Фон вторичной кнопки'),
        ('--vscode-button-secondaryForeground',     'Текст вторичной кнопки'),
        ('--vscode-input-background',         'Фон поля ввода'),
        ('--vscode-input-foreground',         'Текст поля ввода'),
        ('--vscode-input-border',             'Рамка поля ввода'),
        ('--vscode-input-placeholderForeground', 'Цвет placeholder'),
        ('--vscode-focusBorder',              'Рамка фокуса (Accessibility)'),
        ('--vscode-badge-background',         'Фон badge/счётчика'),
        ('--vscode-badge-foreground',         'Текст badge'),
        ('--vscode-list-activeSelectionBackground', 'Фон выбранного элемента списка'),
        ('--vscode-list-activeSelectionForeground', 'Текст выбранного элемента'),
        ('--vscode-list-hoverBackground',     'Фон элемента при наведении'),
    ], 0.55))
    add(sp(4))

    add(h2('Текст и ссылки'))
    add(tblh(['CSS-переменная', 'Назначение']))
    add(tbl2([
        ('--vscode-foreground',               'Основной цвет текста интерфейса'),
        ('--vscode-descriptionForeground',    'Вторичный текст, описания'),
        ('--vscode-disabledForeground',       'Недоступные элементы'),
        ('--vscode-textLink-foreground',      'Цвет ссылок'),
        ('--vscode-textLink-activeForeground','Цвет активной ссылки'),
        ('--vscode-textCodeBlock-background', 'Фон для инлайн-кода'),
        ('--vscode-textBlockQuote-background','Фон для блочных цитат'),
        ('--vscode-textSeparator-foreground', 'Цвет разделителей'),
    ], 0.55))
    add(sp(4))

    add(h2('Панели и контейнеры'))
    add(tblh(['CSS-переменная', 'Назначение']))
    add(tbl2([
        ('--vscode-sideBar-background',        'Фон боковой панели'),
        ('--vscode-sideBar-foreground',        'Текст боковой панели'),
        ('--vscode-sideBar-border',            'Рамка боковой панели'),
        ('--vscode-panel-background',          'Фон нижней панели (Terminal, Problems)'),
        ('--vscode-panel-border',              'Рамка панели'),
        ('--vscode-statusBar-background',      'Фон Status Bar'),
        ('--vscode-statusBar-foreground',      'Текст Status Bar'),
        ('--vscode-tab-activeBackground',      'Фон активной вкладки'),
        ('--vscode-tab-inactiveBackground',    'Фон неактивной вкладки'),
        ('--vscode-tab-activeForeground',      'Текст активной вкладки'),
    ], 0.55))
    add(sp(4))

    add(h2('Шаблон Webview с темами'))
    add(p('Используйте эти переменные в CSS Webview для автоматической адаптации к теме:'))
    add(sp(3))
    add(code([
        '/* Минимальный шаблон Webview CSS */  ',
        'body {',
        '    background-color: var(--vscode-editor-background);',
        '    color: var(--vscode-editor-foreground);',
        '    font-family: var(--vscode-font-family);',
        '    font-size: var(--vscode-font-size);',
        '    /* Важно: убираем margin браузера */',
        '    margin: 0; padding: 16px;',
        '}',
        '',
        'button.primary {',
        '    background: var(--vscode-button-background);',
        '    color: var(--vscode-button-foreground);',
        '    border: 1px solid var(--vscode-button-border, transparent);',
        '    padding: 4px 12px; border-radius: 2px; cursor: pointer;',
        '}',
        'button.primary:hover { background: var(--vscode-button-hoverBackground); }',
        '',
        'input, textarea, select {',
        '    background: var(--vscode-input-background);',
        '    color: var(--vscode-input-foreground);',
        '    border: 1px solid var(--vscode-input-border);',
        '    padding: 4px 8px;',
        '}',
        '',
        'a { color: var(--vscode-textLink-foreground); }',
        'a:hover { color: var(--vscode-textLink-activeForeground); }',
        '',
        'code, pre {',
        '    background: var(--vscode-textCodeBlock-background);',
        '    font-family: var(--vscode-editor-font-family);',
        '    font-size: var(--vscode-editor-font-size);',
        '}',
        '',
        '/* VS Code добавляет класс vscode-dark / vscode-light / vscode-high-contrast */',
        '/* на <body> — можно использовать для тонкой настройки */',
        '.vscode-dark .special { border-color: rgba(255,255,255,0.1); }',
        '.vscode-light .special { border-color: rgba(0,0,0,0.1); }',
    ], highlight=False))
    add(sp(4))
    add(box('Почему CSS-переменные, а не жёсткие цвета',
        'VS Code имеет Light, Dark, High Contrast тёмную и светлую темы, '
        'плюс тысячи пользовательских тем из Marketplace. '
        'Жёсткий hex #1e1e1e выглядит хорошо в одной теме и ужасно в другой. '
        'Также Webview работает в web-версии (vscode.dev) — там темы меняются динамически. '
        'CSS-переменные обновляются автоматически при смене темы без перезагрузки Webview.',
        'note'))
    add(pb())

    return A


if __name__ == '__main__':
    print(f'Appendices: {len(build_appendices())} elements')
