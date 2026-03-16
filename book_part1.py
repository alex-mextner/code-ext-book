from book_helpers import *

def build_story():
    A = []
    def add(*x):
        for i in x: A.append(i)

    def ch(num, title, sub=''):
        part = f'Глава {num}' if str(num).replace('.','').isdigit() else str(num)
        label = f'{part}: {title}' if str(num).replace('.','').isdigit() else title
        add(StableAnchor(f'chapter_{num}'))
        add(toc_ch(label), banner(part, title, sub), sp(12))

    # Обложка и оглавление перенесены в front_matter.py

    # ── ПРЕДИСЛОВИЕ ────────────────────────────────────────────────────────────
    add(toc_ch('Предисловие'), h1('Предисловие'), hl(C['blue']), sp(8))
    add(screenshot('sharpen-the-saw.png', ''))
    add(sp(6))
    add(quote('Затачивайте пилу. Если дать мне шесть часов на то, чтобы срубить дерево, первые четыре я потрачу на заточку топора.', 'Стивен Кови', '«7 навыков высокоэффективных людей», навык 7'))
    add(sp(6))
    add(p('VS Code — это ваш главный инструмент. Расширения — способ заточить его под себя. Эта книга учит создавать расширения, которые превращают редактор кода в инструмент, идеально подходящий для вашей задачи.'))
    add(sp(6))
    add(p('Это руководство — полный перевод и адаптация официальной документации VS Code Extension API. Оно охватывает весь путь разработчика расширений: от создания первой команды Hello World до публикации языкового сервера или AI-ассистента в Marketplace.'))
    add(sp(4))
    add(p('VS Code стал одним из самых популярных редакторов кода во многом благодаря открытой платформе расширений. Более <b>60 000 расширений</b> доступны в Marketplace — и каждое написано с использованием того же Extension API, который описан здесь.'))
    add(sp(4))
    add(p('Книга предназначена для разработчиков, знакомых с TypeScript/JavaScript и Node.js. Первые главы охватывают всё необходимое для старта.'))
    add(sp(4))
    add(box('Об актуальности',
        'VS Code и Extension API обновляются ежемесячно. Данное руководство актуально на март 2026. Самую свежую документацию ищите на code.visualstudio.com/api',
        'note'))
    add(sp(4))
    add(p('<b>Структура книги.</b> Часть I (главы 1–5) — основы: первое расширение, архитектура, команды, темы. Часть II (главы 6–11) — UI-компоненты и языковые расширения. Часть III (главы 12–18) — тестирование, бандлинг, публикация, AI. Справочник — полные таблицы API.'))
    add(pb())

    # ── ВВЕДЕНИЕ ───────────────────────────────────────────────────────────────
    add(banner('Введение', 'VS Code как платформа', 'История, архитектура, место расширений'), sp(12))

    add(h2('История Visual Studio Code'))
    add(p('Visual Studio Code был анонсирован Microsoft на Build 2015. Редактор создавался как лёгкая, мощная альтернатива полноценным IDE — с расчётом на веб-разработчиков и JavaScript/TypeScript.'))
    add(sp(4))
    add(p('С первого дня VS Code был <b>открытым исходным кодом</b> под MIT и размещён на GitHub. Сегодня microsoft/vscode — один из самых популярных репозиториев GitHub. VS Code построен на <b>Electron</b> — всё расширение работает в Node.js-окружении с доступом к npm.'))
    add(sp(6))

    add(screenshot('00-full-window.png', 'Visual Studio Code: Activity Bar, Explorer, редактор, Status Bar'))
    add(sp(6))

    add(h2('Архитектура VS Code'))
    add(p('VS Code состоит из нескольких изолированных процессов:'))
    add(sp(3))
    add(tblh(['Процесс', 'Описание']))
    add(tbl2([
        ('Main Process',       'Electron main — управляет окнами и жизненным циклом'),
        ('Renderer Process',   'Chromium renderer — отображает UI'),
        ('Extension Host',     'Отдельный Node.js — выполняет ВСЕ расширения в изоляции'),
        ('Language Server',    'Опциональный процесс для LSP-расширений'),
        ('Web Extension Host', 'Браузерный хост для vscode.dev / github.dev'),
    ]))
    add(sp(4))
    add(p('Ключевой момент архитектуры: <b>расширения никогда не работают в UI-процессе</b>. Extension Host изолирован — медленное расширение не заморозит редактор. Взаимодействие через строго определённый API.'))
    from book_new import arch_diagram_inject
    for _el in arch_diagram_inject(): add(_el)
    add(sp(6))

    add(h2('Что может расширение?'))
    for item in [
        'добавлять команды в Command Palette',
        'регистрировать новые языки программирования',
        'создавать кастомные панели (Tree View, Webview)',
        'изменять внешний вид: темы цветов, иконки файлов',
        'добавлять IntelliSense, диагностику, hover-подсказки',
        'интегрироваться с внешними сервисами',
        'создавать AI-ассистентов в Copilot Chat',
    ]:
        add(bul(item))
    add(sp(4))
    add(box('Факт',
        'Многие встроенные функции VS Code — поддержка TypeScript, отладчик Node.js, '
        'Git integration — реализованы как расширения, использующие тот же Extension API.', 'note'))
    add(pb())

    # ── ГЛАВА 1 ────────────────────────────────────────────────────────────────
    ch('1', 'Первое расширение', 'Hello World — от нуля до запуска за 5 минут')

    add(h2('Предварительные требования'))
    add(tblh(['Инструмент', 'Назначение']))
    add(tbl2([
        ('Node.js 18+',    'Среда выполнения; расширения и инструменты сборки работают в Node.js'),
        ('npm / yarn',     'Менеджер пакетов для зависимостей'),
        ('Git',            'Система контроля версий'),
        ('Visual Studio Code', 'Для разработки и отладки расширений'),
        ('TypeScript',     'Рекомендован; типизация значительно упрощает работу с API'),
    ]))
    add(sp(6))

    add(h2('Создание проекта'))
    add(p('Запустите Yeoman-генератор — официальный scaffolder для расширений VS Code:'))
    add(sp(3))
    add(code([
        '# Без глобальной установки (рекомендуется)',
        'npx --package yo --package generator-code -- yo code',
        '',
        '# Или глобально',
        'npm install -g yo generator-code',
        'yo code',
    ]))
    add(sp(3))
    add(p('Два способа запустить генератор: через <b>npx</b> (ничего не устанавливается глобально — предпочтительно) или через глобальную установку <b>yo</b> и <b>generator-code</b>. Результат одинаковый — интерактивный мастер создания проекта расширения.'))
    from book_new import yeoman_inject
    for _el in yeoman_inject(): add(_el)
    add(p('Генератор задаёт вопросы. Выберите <b>New Extension (TypeScript)</b>:'))
    add(sp(3))
    add(code([
        '? What type of extension do you want to create?',
        '  > New Extension (TypeScript)',
        '? What\'s the name of your extension? HelloWorld',
        '? What\'s the identifier? helloworld',
        '? Initialize a git repository? Yes',
        '? Which bundler to use? unbundled',
        '? Which package manager to use? npm',
    ]))
    add(sp(3))
    add(p('Генератор создаёт проект по ответам: <b>New Extension (TypeScript)</b> — шаблон с настроенными tsconfig, ESLint и launch.json. Идентификатор (<b>helloworld</b>) станет частью ID команд и имени папки. <b>unbundled</b> — без бандлера, подходит для начала; для публикации потребуется esbuild или webpack (глава 15).'))

    add(sp(4))
    add(p('Созданная структура проекта:'))
    add(sp(4))
    from book_ui_diagrams import helloworld_tree
    add(helloworld_tree())
    add(sp(6))

    add(h2('Запуск расширения'))
    add(p('Откройте <b>src/extension.ts</b> и нажмите <b>F5</b>. VS Code скомпилирует TypeScript и откроет новое окно — <b>Extension Development Host</b>.'))
    add(sp(4))
    add(box('Горячая перезагрузка',
        'После изменений выполните Developer: Reload Window (Ctrl+R) в окне Extension Development Host. '
        'Расширение перекомпилируется без перезапуска.', 'tip'))
    add(sp(6))

    add(h2('Разбор кода extension.ts'))
    add(p('Откройте <b>src/extension.ts</b> — это точка входа расширения:'))
    add(sp(4))
    add(screenshot('09-editor-with-file.png', 'extension.ts — минимальный код расширения в редакторе VS Code'))
    add(sp(4))
    add(p('Разберём каждую часть:'))
    add(sp(3))
    add(code([
        'import * as vscode from \'vscode\';',
        '',
        '// Вызывается однажды — при первой активации расширения',
        '// context даёт доступ к хранилищу, subscriptions и пути файлов',
        'export function activate(context: vscode.ExtensionContext) {',
        '    console.log(\'Расширение активировано!\');',
        '',
        '    // Регистрируем обработчик команды',
        '    // ID команды должен совпадать с "command" в package.json → contributes.commands',
        '    const disposable = vscode.commands.registerCommand(',
        '        \'helloworld.helloWorld\',   // ID из package.json',
        '        () => {                     // Обработчик — вызывается при выполнении команды',
        '            vscode.window.showInformationMessage(\'Hello World!\');',
        '        }',
        '    );',
        '',
        '    // registerCommand возвращает Disposable — объект с методом dispose()',
        '    // subscriptions — массив Disposable-объектов, VS Code вызовет dispose()',
        '    // на каждом при деактивации расширения (закрытие VS Code)',
        '    context.subscriptions.push(disposable);',
        '}',
        '',
        '// Вызывается при деактивации — для синхронной очистки (необязательна)',
        '// Асинхронная очистка: используйте context.subscriptions',
        'export function deactivate() {}',
    ]))
    add(sp(3))
    add(p('Минимальное расширение — две экспортируемые функции: <b>activate()</b> и <b>deactivate()</b>. Вся логика живёт в activate: здесь регистрируются команды, провайдеры, листенеры. Каждый из них возвращает <b>Disposable</b> — объект, который нужно добавить в <b>context.subscriptions</b>, чтобы VS Code автоматически освободил ресурсы при деактивации. ID команды (<b>helloworld.helloWorld</b>) должен точно совпадать с тем, что указан в <b>package.json → contributes.commands</b> — иначе команда не сработает.'))
    add(sp(3))
    add(box('context.subscriptions',
        'Всегда добавляйте команды, листенеры и провайдеры в context.subscriptions. '
        'VS Code вызовет dispose() на всех объектах при деактивации. Иначе — утечки памяти.', 'warn'))
    add(sp(6))

    add(h2('Отладка расширения'))
    add(p('VS Code предоставляет полноценный дебаггер для расширений. Поставьте брейкпоинт — кликните на левый гutter строки в extension.ts. Вызовите команду — дебаггер остановится. Все <b>console.log()</b> видны в панели <b>Debug Console</b> основного окна.'))
    add(sp(3))
    add(box('Output Channel',
        'Для долгоживущих сообщений создайте: '
        'const ch = vscode.window.createOutputChannel("MyExt"); '
        'ch.appendLine("msg"); ch.show(); — лучше console.log для информации, которую пользователь должен видеть.', 'tip'))
    add(pb())

    # ── ГЛАВА 2 ────────────────────────────────────────────────────────────────
    ch('2', 'Анатомия расширения', 'Три концепции: Activation Events, Contribution Points, VS Code API')

    add(h2('Три фундаментальных концепции'))
    add(tblh(['Концепция', 'Описание']))
    add(tbl2([
        ('Activation Events',
         'Определяют КОГДА расширение загружается. До события — не занимает ресурсы. '
         'Примеры: onCommand, onLanguage, onStartupFinished'),
        ('Contribution Points',
         'Статические объявления в package.json. Не требуют кода — VS Code читает их при старте. '
         'Примеры: contributes.commands, contributes.views, contributes.themes'),
        ('VS Code API',
         'Динамические JS-вызовы во время работы. '
         'import * as vscode from "vscode". '
         'Примеры: vscode.window.*, vscode.workspace.*, vscode.commands.*'),
    ]))
    add(sp(6))

    add(h2('Манифест расширения — package.json'))
    add(p('Каждое расширение обязано иметь package.json — манифест. Он содержит поля Node.js-пакета и специфичные для VS Code поля:'))
    add(sp(3))
    add(code([
        '{',
        '  "name": "helloworld-sample",',
        '  "version": "0.0.1",',
        '  "description": "Мой первый extension",',
        '  "publisher": "my-publisher",',
        '',
        '  // Минимальная версия VS Code',
        '  "engines": { "vscode": "^1.90.0" },',
        '',
        '  "main": "./out/extension.js",',
        '  "categories": ["Other"],',
        '  "keywords": ["vscode", "extension"],',
        '  "icon": "images/icon.png",',
        '',
        '  // Activation Events (с VS Code 1.74+ команды активируют автоматически)',
        '  "activationEvents": [',
        '    "onLanguage:python",',
        '    "onStartupFinished"',
        '  ],',
        '',
        '  // Contribution Points',
        '  "contributes": {',
        '    "commands": [{',
        '      "command": "myext.action",',
        '      "title": "My Extension: Action",',
        '      "category": "My Extension",',
        '      "icon": "$(star)"',
        '    }],',
        '    "menus": {',
        '      "editor/context": [{',
        '        "when": "editorHasSelection",',
        '        "command": "myext.action"',
        '      }]',
        '    }',
        '  },',
        '',
        '  "devDependencies": {',
        '    "@types/vscode": "^1.90.0",',
        '    "typescript": "^5.0.0"',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Полный манифест расширения. Верхняя часть — стандартные поля npm-пакета (<b>name</b>, <b>version</b>, <b>publisher</b>). Поле <b>engines.vscode</b> задаёт минимальную версию VS Code — пользователи на старых версиях не увидят расширение в Marketplace. <b>main</b> указывает на скомпилированный JS (не .ts). Блок <b>activationEvents</b> определяет, когда загружать код: здесь расширение активируется при открытии Python-файла или после загрузки VS Code. Блок <b>contributes</b> регистрирует команду с иконкой и привязывает её к контекстному меню редактора через <b>when</b>-условие.'))
    add(sp(3))
    add(p('<b>Что означает "$(star)"</b> — запись вида <b>$(icon-name)</b> — это встроенные иконки '
          'VS Code, называемые <b>Codicons</b>. Более 600 иконок поставляются вместе с VS Code '
          'и автоматически адаптируются под текущую цветовую тему. '
          'Используются в командах, кнопках, Status Bar и Quick Pick.'))
    add(sp(2))
    add(box('Codicons — встроенные иконки VS Code',
        'Полный каталог всех $(icon-name): code.visualstudio.com/api/references/icons-in-labels '
        'или команда "Help: Open Icons Viewer" прямо в VS Code. '
        'Кастомные SVG: для Activity Bar используйте собственный .svg файл через '
        '"icon": "./icons/myicon.svg" в viewsContainers. '
        'Для команд в редакторе $(icon-name) предпочтительнее — они всегда в стиле VS Code.',
        'note'))
    add(sp(4))
    add(tblh(['Поле', 'Назначение']))
    add(tbl2([
        ('name + publisher',   'Уникальный ID расширения: publisher.name'),
        ('engines.vscode',     'Минимальная версия VS Code для совместимости'),
        ('main',               'Путь к скомпилированному JS — точка входа'),
        ('activationEvents',   'С VS Code 1.74+ большинство событий генерируется автоматически'),
        ('contributes',        'Все статические расширения VS Code'),
        ('icon',               'PNG 128×128. SVG не поддерживается в публикуемых расширениях'),
        ('categories',         'AI, Chat, Debuggers, Formatters, Linters, Programming Languages, Themes...'),
    ]))
    add(sp(6))

    add(h2('Capabilities — совместимость и доверие'))
    add(p('С VS Code 1.56+ расширения объявляют capabilities в package.json. Без них расширение может быть молча отключено в определённых окружениях:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"capabilities": {',
        '  // Поддержка виртуальных рабочих пространств (vscode.dev, github.dev)',
        '  "virtualWorkspaces": {',
        '    "supported": "limited",',
        '    "description": "File operations work, but terminal commands are not available"',
        '  },',
        '  // Поведение при ненадёжном рабочем пространстве',
        '  "untrustedWorkspace": {',
        '    "supported": "limited",',
        '    "restrictedConfigurations": [',
        '      "myExtension.executable"  // опасные настройки отключены до доверия',
        '    ]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Два ключевых объявления. <b>virtualWorkspaces</b> указывает, работает ли расширение на vscode.dev и github.dev — три варианта: <b>true</b> (полная поддержка), <b>"limited"</b> (частичная, с описанием ограничений), <b>false</b> (не работает без локальной файловой системы). <b>untrustedWorkspace</b> контролирует поведение до того, как пользователь нажмёт «Trust» — <b>restrictedConfigurations</b> блокирует настройки, которые могут запускать произвольный код (пути к исполняемым файлам, shell-команды). Без этих объявлений VS Code может отключить расширение в Remote SSH, Dev Containers или vscode.dev.'))
    add(sp(6))

    add(h2('Activation Events — полный список'))
    add(p('Полный актуальный список — <a href="#appendix_C"><b>Справочник C</b></a> в конце книги. '
          'Онлайн: code.visualstudio.com/api/references/activation-events'))
    add(tblh(['Событие', 'Когда срабатывает']))
    add(tbl2([
        ('onCommand:id',           'При первом вызове команды с указанным ID'),
        ('onLanguage:lang',        'При открытии файла указанного языка (python, typescript...)'),
        ('onView:id',              'При первом открытии View с указанным ID'),
        ('workspaceContains:glob', 'Если workspace содержит файл по паттерну'),
        ('onFileSystem:scheme',    'При обращении к URI с нестандартной схемой'),
        ('onUri',                  'При открытии vscode://publisher.name URI'),
        ('onWebviewPanel:type',    'При восстановлении Webview панели'),
        ('onCustomEditor:type',    'При открытии кастомного редактора'),
        ('onDebug',                'При запуске любого сеанса отладки'),
        ('onChatParticipant:id',   'При вызове AI Chat Participant'),
        ('onStartupFinished',      'После полной загрузки VS Code — не блокирует старт'),
        ('*',                      'ИЗБЕГАЙТЕ: активирует при каждом запуске VS Code'),
    ]))
    add(sp(6))

    add(h2('VS Code API — обзор namespace'))
    add(p('Актуальный список: <b>code.visualstudio.com/api/references/vscode-api</b>'))
    add(sp(3))
    add(tblh(['Namespace', 'Назначение']))
    add(tbl2([
        ('vscode.window',     'UI: уведомления, input boxes, quick picks, webview, терминалы, статус-бар'),
        ('vscode.workspace',  'Файлы: открытие, конфигурация, события изменений, файловая система'),
        ('vscode.commands',   'Регистрация и выполнение команд'),
        ('vscode.languages',  'Языковые возможности: completion, hover, diagnostics, formatting'),
        ('vscode.env',        'Окружение: clipboard, appName, openExternal'),
        ('vscode.debug',      'Управление отладкой'),
        ('vscode.scm',        'Source Control Management'),
        ('vscode.tasks',      'Управление задачами'),
        ('vscode.auth',       'Аутентификация: auth tokens'),
        ('vscode.lm',         'Language Models — работа с AI'),
        ('vscode.chat',       'Chat API — Chat Participants'),
        ('vscode.tests',      'Testing API — test providers'),
    ]))
    add(sp(4))
    from book_new import q_activation_events
    add(q_activation_events())
    add(sp(4))
    add(pb())
    ch('3', 'Возможности расширений', 'Работа с редактором, текстом, UI и хранилищем')

    add(h2('Работа с редактором и текстом'))
    add(p('Основные операции с текстом выполняются через <b>vscode.window.activeTextEditor</b>:'))
    add(sp(3))
    add(code([
        'const editor = vscode.window.activeTextEditor;',
        'if (!editor) return;',
        '',
        '// Получение текста',
        'const full    = editor.document.getText();',
        'const line    = editor.document.lineAt(0).text;',
        'const selected= editor.document.getText(editor.selection);',
        '',
        '// Позиции и диапазоны',
        'const pos      = new vscode.Position(lineNum, charNum);',
        'const range    = new vscode.Range(startPos, endPos);',
        'const wordRange= editor.document.getWordRangeAtPosition(pos);',
        '',
        '// Редактирование',
        'await editor.edit(builder => {',
        '    builder.replace(editor.selection, \'новый текст\');',
        '    builder.insert(new vscode.Position(0, 0), \'// Header\\n\');',
        '    builder.delete(range);',
        '});',
        '',
        '// Декорации — визуальная подсветка',
        'const decType = vscode.window.createTextEditorDecorationType({',
        '    backgroundColor: \'rgba(255,200,0,0.3)\',',
        '    border: \'1px solid orange\',',
        '    borderRadius: \'2px\',',
        '});',
        'editor.setDecorations(decType, [range1, range2]);',
        '// Очистка:',
        'editor.setDecorations(decType, []);',
    ]))
    add(sp(3))
    add(p('Четыре основные операции с редактором. <b>Чтение</b>: getText() без аргумента возвращает весь документ, с Range или Selection — фрагмент. <b>Позиции</b>: Position (строка, символ) и Range (две позиции) — базовые типы для указания «где» в документе; getWordRangeAtPosition() удобен для операций над словом под курсором. <b>Редактирование</b>: edit() принимает callback с builder — через него replace/insert/delete; вызов асинхронный, возвращает true при успехе. <b>Декорации</b>: createTextEditorDecorationType() создаёт тип один раз, setDecorations() применяет его к массиву Range; для очистки передайте пустой массив.'))
    add(sp(6))

    add(h2('Уведомления и пользовательский ввод'))
    add(p('VS Code предоставляет несколько встроенных компонентов для взаимодействия '
          'с пользователем. Важно выбирать правильный тип — подробнее в главе UX:'))
    add(sp(3))
    add(code([
        '// Простые уведомления (появляются в правом нижнем углу)',
        'vscode.window.showInformationMessage(\'Операция завершена\');',
        'vscode.window.showWarningMessage(\'Предупреждение\');',
        'vscode.window.showErrorMessage(\'Ошибка!\');',
        '',
        '// С кнопками — возвращает выбранную строку или undefined',
        'const res = await vscode.window.showInformationMessage(',
        '    \'Перезагрузить?\', \'Да\', \'Нет\'',
        ');',
        'if (res === \'Да\') { /* ... */ }',
        '',
        '// InputBox — текстовый ввод с валидацией в реальном времени',
        'const name = await vscode.window.showInputBox({',
        '    prompt: \'Введите имя функции\',',
        '    placeHolder: \'myFunction\',',
        '    validateInput: v => /^\\w+$/.test(v) ? null : \'Только буквы и цифры\',',
        '});',
        '// name === undefined если пользователь нажал Escape',
        '',
        '// Quick Pick — список выбора с поиском',
        '// $(icon-name) — встроенные иконки Codicons',
        'const items: vscode.QuickPickItem[] = [',
        '    { label: \'$(cloud-upload) Опубликовать\', description: \'В Marketplace\' },',
        '    { label: \'\', kind: vscode.QuickPickItemKind.Separator },',
        '    { label: \'$(package) Упаковать\', description: \'Создать .vsix\' },',
        '];',
        'const pick = await vscode.window.showQuickPick(items, {',
        '    title: \'Действие с расширением\',',
        '    placeHolder: \'Выберите...\',',
        '});',
        '// pick === undefined если пользователь нажал Escape',
    ]))
    add(sp(3))
    add(p('Три встроенных способа взаимодействия с пользователем. <b>Уведомления</b> (showInformation/Warning/ErrorMessage) — появляются в правом нижнем углу; с кнопками возвращают выбранный вариант или undefined при Escape. <b>InputBox</b> — однострочный ввод; validateInput вызывается при каждом нажатии клавиши и показывает ошибку до подтверждения. <b>Quick Pick</b> — список с поиском, Separator разделяет группы; используйте matchOnDescription для поиска по description-полю. Все три API асинхронны и возвращают undefined при отмене — всегда проверяйте результат.'))
    add(sp(4))
    add(screenshot('07-quick-pick.png', 'Quick Pick: палитра выбора действий (showQuickPick)'))
    add(p('Вызывается через <b>Ctrl+Shift+P</b> (Command Palette) или программно через <b>vscode.window.showQuickPick()</b>.'))
    add(sp(6))
    add(code([
        '// Progress API — три вида отображения прогресса:',
        '',
        '// 1. ProgressLocation.Window — в Status Bar (ненавязчиво)',
        'await vscode.window.withProgress({',
        '    location: vscode.ProgressLocation.Window,',
        '    title: \'$(sync~spin) Индексирую...\',',
        '}, async () => { await buildIndex(); });',
        '',
        '// 2. ProgressLocation.Notification — всплывашка с кнопкой отмены',
        'await vscode.window.withProgress({',
        '    location: vscode.ProgressLocation.Notification,',
        '    title: \'Анализирую проект\',',
        '    cancellable: true,',
        '}, async (progress, token) => {',
        '    const files = await getFiles();',
        '    for (let i = 0; i < files.length; i++) {',
        '        if (token.isCancellationRequested) break;',
        '        // increment — на сколько % увеличить от последнего вызова',
        '        progress.report({',
        '            increment: 100 / files.length,',
        '            message: `${i + 1}/${files.length}: ${files[i]}`,',
        '        });',
        '        await analyzeFile(files[i]);',
        '    }',
        '});',
        '',
        '// 3. ProgressLocation.SourceControl — в SCM панели',
    ]))
    add(sp(3))
    add(p('Три вида индикации прогресса для разных сценариев. <b>Window</b> — ненавязчивый спиннер в Status Bar, подходит для фоновых задач (индексация, синхронизация). <b>Notification</b> — видимая всплывашка с полосой прогресса; <b>cancellable: true</b> добавляет кнопку Cancel и передаёт CancellationToken в callback — проверяйте token.isCancellationRequested в цикле. <b>progress.report({ increment })</b> увеличивает прогресс на указанный процент от предыдущего значения, а <b>message</b> обновляет текст под заголовком.'))
    add(sp(4))
    add(screenshot('08-notification-center.png', 'Notification Center: уведомления и прогресс'))
    add(sp(6))

    add(h2('Status Bar — элемент состояния'))
    add(p('Status Bar — нижняя строка редактора. Левая сторона для глобальной информации, '
          'правая — для контекстной (язык файла, кодировка):'))
    add(sp(4))
    add(screenshot('03-status-bar.png', 'Status Bar: строка состояния внизу редактора'))
    add(sp(6))

    add(h2('Хранение данных'))
    add(tblh(['API', 'Назначение']))
    add(tbl2([
        ('context.globalState',     'Глобальное key-value хранилище, сохраняется между сессиями'),
        ('context.workspaceState',  'Хранилище для текущего рабочего пространства'),
        ('context.globalStorageUri','URI папки для файлового хранилища (глобальное)'),
        ('context.storageUri',      'URI папки для хранилища workspace'),
        ('context.secrets',         'Безопасное зашифрованное хранилище для токенов'),
    ]))
    add(sp(3))
    add(code([
        '// globalState — чтение и запись',
        'await context.globalState.update(\'lastUsed\', new Date().toISOString());',
        'const last = context.globalState.get<string>(\'lastUsed\');',
        '',
        '// secrets — безопасное хранение токенов',
        'await context.secrets.store(\'apiToken\', \'my-secret\');',
        'const token = await context.secrets.get(\'apiToken\');',
        'await context.secrets.delete(\'apiToken\');',
        '',
        '// Файловое хранилище',
        'const storageUri = context.globalStorageUri;',
        'await vscode.workspace.fs.writeFile(',
        '    vscode.Uri.joinPath(storageUri, \'cache.json\'),',
        '    Buffer.from(JSON.stringify({ data: [] }))',
        ');',
        'const bytes = await vscode.workspace.fs.readFile(',
        '    vscode.Uri.joinPath(storageUri, \'cache.json\')',
        ');',
        'const data = JSON.parse(Buffer.from(bytes).toString());',
    ]))
    add(sp(3))
    add(p('Три механизма хранения данных. <b>globalState</b> / <b>workspaceState</b> — key-value хранилища (get/update), сохраняются между сессиями; globalState — для всех проектов, workspaceState — для текущего. <b>secrets</b> — шифрованное хранилище для токенов и паролей, данные не видны в settings.json. <b>globalStorageUri</b> — папка на диске для крупных данных (кэши, БД); используйте <b>workspace.fs</b> вместо Node.js fs — иначе расширение не работает в Remote SSH, Dev Containers и vscode.dev.'))
    add(pb())

    # ── ГЛАВА 4 ────────────────────────────────────────────────────────────────
    ch('4', 'Команды, меню и настройки', 'Contribution Points — статические расширения VS Code')

    add(h2('Все Contribution Points'))
    add(p('Полный список с описанием — <a href="#appendix_B"><b>Справочник B</b></a> в конце книги, '
          'актуальный онлайн-список: code.visualstudio.com/api/references/contribution-points'))
    add(sp(3))
    add(tblh(['Contribution Point', 'Назначение']))
    add(tbl2([
        ('contributes.commands',         'Команды с title, category, icon — в Command Palette'),
        ('contributes.menus',            'Пункты в контекстных меню и панелях инструментов'),
        ('contributes.keybindings',      'Горячие клавиши для команд'),
        ('contributes.configuration',    'Настройки расширения в Settings UI'),
        ('contributes.languages',        'Объявление нового языка программирования'),
        ('contributes.grammars',         'TextMate-грамматики для синтаксической подсветки'),
        ('contributes.snippets',         'Сниппеты кода для языков'),
        ('contributes.themes',           'Цветовые темы редактора и UI'),
        ('contributes.iconThemes',       'Темы иконок файлов'),
        ('contributes.productIconThemes','Темы иконок интерфейса VS Code'),
        ('contributes.views',            'Tree View в боковой панели'),
        ('contributes.viewsContainers',  'Контейнеры в Activity Bar'),
        ('contributes.viewsWelcome',     'Приветственный контент для пустых View'),
        ('contributes.taskDefinitions',  'Типы задач для Task Provider'),
        ('contributes.debuggers',        'Debug Adapter: type, label, languages'),
        ('contributes.walkthroughs',     'Пошаговые туториалы при первом запуске'),
        ('contributes.chatParticipants', 'AI Chat Participants для Copilot'),
        ('contributes.languageModels',   'Кастомные Language Model провайдеры'),
        ('contributes.customEditors',    'Кастомные редакторы для типов файлов'),
        ('contributes.colors',           'Новые цвета для тем'),
        ('contributes.authentication',   'Authentication Provider'),
    ]))
    add(sp(6))

    add(h2('Команды и контекстные меню'))
    add(code([
        '"contributes": {',
        '  "commands": [{',
        '    "command": "myext.action",',
        '    "title": "My Extension: Do Something",',
        '    "category": "My Extension",',
        '    "icon": "$(star)"',
        '  }],',
        '  "menus": {',
        '    // Контекстное меню редактора',
        '    "editor/context": [{',
        '      "when": "editorHasSelection && resourceLangId == typescript",',
        '      "command": "myext.action",',
        '      "group": "1_modification@1"',
        '    }],',
        '    // Панель редактора (кнопки у вкладок)',
        '    "editor/title": [{',
        '      "when": "resourceExtname == .md",',
        '      "command": "myext.preview",',
        '      "group": "navigation"',
        '    }],',
        '    // Explorer контекстное меню',
        '    "explorer/context": [{',
        '      "when": "explorerResourceIsFolder",',
        '      "command": "myext.newFile"',
        '    }]',
        '  },',
        '  "keybindings": [{',
        '    "command": "myext.action",',
        '    "key": "ctrl+shift+a",',
        '    "mac": "cmd+shift+a",',
        '    "when": "editorTextFocus"',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Связка команд, меню и горячих клавиш в одном блоке contributes. <b>commands</b> объявляет команду с category — в Command Palette отобразится как «My Extension: Do Something». <b>menus</b> привязывает команды к конкретным местам UI: editor/context (правый клик в редакторе), editor/title (кнопки у вкладок), explorer/context (правый клик в Explorer). <b>when</b>-условие фильтрует видимость: здесь команда появляется только при выделении текста в TypeScript-файле. <b>group</b> определяет позицию в меню: "1_modification@1" — первая секция, первый элемент. <b>keybindings</b> задаёт горячие клавиши с отдельным маппингом для Mac.'))
    add(sp(4))

    add(h3('When Clause Contexts'))
    add(p('When clauses — булевы выражения, управляющие видимостью команд, меню и кнопок. '
          'Вычисляются VS Code в реальном времени при каждом изменении контекста. '
          'Полный список доступных контекстов: '
          '<b>code.visualstudio.com/api/references/when-clause-contexts</b> — '
          'список обновляется с каждым релизом VS Code.'))
    add(sp(3))
    add(tblh(['Контекст', 'Описание']))
    add(tbl2([
        ('editorIsOpen',            'Открыт хоть один редактор'),
        ('editorHasSelection',      'Есть выделение'),
        ('editorTextFocus',         'Фокус в текстовом редакторе'),
        ('resourceLangId',          'Язык файла (== typescript, python...)'),
        ('resourceExtname',         'Расширение файла (== .json, .ts...)'),
        ('explorerResourceIsFolder','Выбранный элемент Explorer — папка'),
        ('isInDiffEditor',          'Активен diff editor'),
        ('config.myext.enabled',    'Значение настройки расширения'),
    ]))
    add(sp(3))
    add(p('Операторы: <b>==</b>, <b>!=</b>, <b>&&</b>, <b>||</b>, <b>!</b>, <b>in</b>, <b>=~</b> (regex). '
          'Пример составного условия: '
          '<b>editorTextFocus &amp;&amp; resourceLangId == python &amp;&amp; !isInDiffEditor</b> — '
          'фокус в редакторе Python, не в режиме сравнения.'))
    add(sp(6))

    add(h2('Настройки расширения'))
    add(p('VS Code генерирует полноценный UI из JSON-объявления настроек. Вот как выглядит Settings UI:'))
    add(sp(4))
    add(screenshot('06-settings-ui.png', 'Settings UI: автоматически сгенерированный интерфейс настроек'))
    add(sp(4))
    add(code([
        '"contributes": {',
        '  "configuration": {',
        '    "title": "My Extension",',
        '    "properties": {',
        '      "myExtension.maxItems": {',
        '        "type": "number", "default": 100,',
        '        "minimum": 1, "maximum": 1000,',
        '        "description": "Максимальное количество элементов"',
        '      },',
        '      "myExtension.format": {',
        '        "type": "string",',
        '        "enum": ["json", "yaml", "toml"],',
        '        "enumDescriptions": ["JSON формат", "YAML формат", "TOML формат"],',
        '        "default": "json"',
        '      },',
        '      "myExtension.paths": {',
        '        "type": "array",',
        '        "items": { "type": "string" },',
        '        "default": []',
        '      }',
        '    }',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Объявление настроек расширения в Settings UI. Каждое свойство в <b>properties</b> — отдельная настройка с типом, значением по умолчанию и описанием. VS Code автоматически генерирует UI: <b>number</b> с min/max — слайдер или поле ввода, <b>enum</b> с enumDescriptions — выпадающий список, <b>array</b> — редактируемый список. Ключ <b>myExtension.maxItems</b> — именно так пользователь увидит его в settings.json; префикс до точки (myExtension) группирует все настройки расширения.'))

    add(sp(3))
    add(code([
        '// Чтение конфигурации',
        'const cfg = vscode.workspace.getConfiguration(\'myExtension\');',
        'const maxItems = cfg.get<number>(\'maxItems\', 100);',
        'const format   = cfg.get<string>(\'format\',   \'json\');',
        '',
        '// Обновление',
        'await cfg.update(\'maxItems\', 200, vscode.ConfigurationTarget.Global);',
        '',
        '// Подписка на изменения',
        'vscode.workspace.onDidChangeConfiguration(e => {',
        '    if (e.affectsConfiguration(\'myExtension.maxItems\')) {',
        '        // перечитать значение',
        '    }',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('<b>workspace.getConfiguration(section)</b> читает значения из settings.json. <b>get<T>(key, default)</b> возвращает типизированное значение с fallback. <b>ConfigurationTarget.Global</b> меняет глобальные настройки пользователя, <b>Workspace</b> — только настройки текущего проекта.'))
    add(pb())

    # ── ГЛАВА 5 ────────────────────────────────────────────────────────────────
    ch('5', 'Темы оформления', 'Color Theme, File Icon Theme, Product Icon Theme')

    add(h2('Типы тем'))
    add(p('Актуальный список: <b>code.visualstudio.com/api/references/extension-manifest</b>'))
    add(sp(3))
    add(tblh(['Тип темы', 'Описание']))
    add(tbl2([
        ('Color Theme',
         'Управляет цветами синтаксиса (token colors) и интерфейса (workbench colors). '
         'uiTheme: vs-dark | vs | hc-black | hc-light'),
        ('File Icon Theme',
         'Иконки для файлов и папок в Explorer, Breadcrumbs, Quick Open. '
         'Пример: Material Icon Theme, vscode-icons'),
        ('Product Icon Theme',
         'Иконки интерфейса VS Code: кнопки, Activity Bar, меню. Доступно с VS Code 1.50'),
    ]))
    add(sp(6))

    add(h2('Создание Color Theme'))
    add(p('Пользователь выбирает тему через <b>Preferences: Color Theme</b> (<b>Ctrl+K Ctrl+T</b>) — Quick Pick с предпросмотром:'))
    add(sp(4))
    add(screenshot('12-color-theme-picker.png', 'Color Theme Picker: переключение тем с живым предпросмотром'))
    add(sp(4))
    add(code([
        '"contributes": {',
        '  "themes": [{',
        '    "label": "My Dark Theme",',
        '    "uiTheme": "vs-dark",',
        '    "path": "./themes/my-dark-theme.json"',
        '  }, {',
        '    "label": "My Light Theme",',
        '    "uiTheme": "vs",',
        '    "path": "./themes/my-light-theme.json"',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Регистрация цветовой темы в package.json. <b>uiTheme</b> задаёт базу: <b>vs-dark</b> — тёмная, <b>vs</b> — светлая, <b>hc-black</b> / <b>hc-light</b> — высококонтрастные. Одно расширение может содержать несколько тем — каждая в отдельном JSON-файле.'))

    add(sp(3))
    add(code([
        '// themes/my-dark-theme.json',
        '{',
        '  "name": "My Dark Theme",',
        '  "type": "dark",',
        '  "colors": {',
        '    "editor.background":       "#1a1a2e",',
        '    "editor.foreground":       "#e0e0e0",',
        '    "activityBar.background":  "#16213e",',
        '    "sideBar.background":      "#0f3460",',
        '    "statusBar.background":    "#533483",',
        '    "tab.activeBackground":    "#1a1a2e",',
        '    "tab.inactiveBackground":  "#16213e"',
        '  },',
        '  "tokenColors": [',
        '    {',
        '      "name": "Keywords",',
        '      "scope": ["keyword", "storage.type"],',
        '      "settings": { "foreground": "#c792ea", "fontStyle": "italic" }',
        '    },',
        '    {',
        '      "name": "Strings",',
        '      "scope": "string",',
        '      "settings": { "foreground": "#c3e88d" }',
        '    },',
        '    {',
        '      "name": "Comments",',
        '      "scope": "comment",',
        '      "settings": { "foreground": "#546e7a", "fontStyle": "italic" }',
        '    },',
        '    {',
        '      "name": "Functions",',
        '      "scope": "entity.name.function",',
        '      "settings": { "foreground": "#82aaff" }',
        '    }',
        '  ]',
        '}',
    ]))
    add(sp(3))
    add(p('Файл темы состоит из двух частей. <b>colors</b> — цвета интерфейса VS Code: фон редактора, боковая панель, вкладки, строка состояния (всего 700+ ключей — полный список в <a href="#appendix_D">Справочнике D</a>). <b>tokenColors</b> — цвета синтаксиса, унаследованные от TextMate: каждое правило связывает <b>scope</b> (keyword, string, comment, entity.name.function) с цветом и стилем. Scope — иерархическая система: "keyword" окрасит все ключевые слова, "keyword.control.flow" — только if/else/return.'))

    add(sp(4))
    add(box('Как сохранить текущую тему VS Code для редактирования',
        'Откройте Command Palette → "Developer: Generate Color Theme From Current Settings". '
        'VS Code создаст JSON-файл с полным описанием активной темы — все цвета UI и токены синтаксиса. '
        'Это лучший способ начать новую тему: берёте понравившуюся готовую тему за основу '
        'и правите нужные значения. '
        'TextMate .tmTheme формат устарел — современные темы VS Code используют JSON напрямую.',
        'tip'))
    add(sp(6))

    add(h2('File Icon Theme'))
    add(p('File Icon Theme — набор иконок для файлов и папок в Explorer. Появились в VS Code 1.5 (2016). '
          'Пользователи выбирают их через <b>File → Preferences → File Icon Theme</b>. '
          'Популярные темы: Material Icon Theme (40M+ установок), vscode-icons, Seti. '
          'Если вы разрабатываете расширение для конкретного языка — '
          'добавьте иконку для его файлов: это заметно улучшает опыт пользователя.'))
    add(sp(3))
    add(code([
        '"contributes": {',
        '  "iconThemes": [{',
        '    "id": "myIconTheme",',
        '    "label": "My Icon Theme",',
        '    "path": "./icons/my-icon-theme.json"',
        '  }]',
        '}',
        '',
        '// icons/my-icon-theme.json',
        '{',
        '  "iconDefinitions": {',
        '    // Ключ — внутреннее имя, iconPath — путь к SVG',
        '    "_ts": { "iconPath": "./icons/typescript.svg" },',
        '    "_folder": { "iconPath": "./icons/folder.svg" },',
        '    "_folder_open": { "iconPath": "./icons/folder-open.svg" }',
        '  },',
        '  // Сопоставление расширений файлов → иконки',
        '  "fileExtensions": { "ts": "_ts", "tsx": "_ts" },',
        '  // Точные имена файлов',
        '  "fileNames": { "package.json": "_npm" },',
        '  // По языковому ID (languageId из languages contribution)',
        '  "languageIds": { "typescript": "_ts" },',
        '  // Папки: закрытая / открытая',
        '  "folder": "_folder",',
        '  "folderExpanded": "_folder_open",',
        '  "rootFolder": "_folder",',
        '  "rootFolderExpanded": "_folder_open"',
        '}',
    ]))
    add(sp(3))
    add(p('Структура File Icon Theme: объявление в package.json + JSON-файл с маппингом. <b>iconDefinitions</b> — словарь иконок с путями к SVG. Далее идут правила: <b>fileExtensions</b> сопоставляет расширения файлов с иконками, <b>fileNames</b> — точные имена (package.json, Dockerfile), <b>languageIds</b> — по зарегистрированному языку. <b>folder</b> / <b>folderExpanded</b> — иконки для свёрнутой и развёрнутой папки.'))
    add(sp(3))
    add(p('<b>Иерархия приоритетов:</b> fileNames > fileExtensions > languageIds. '
          'Если файл называется "package.json" — сработает fileNames, '
          'даже если есть совпадение по расширению ".json".'))
    add(sp(4))
    add(box('Как делать SVG иконки "родными" для VS Code',
        'VS Code применяет CSS-класс к иконкам для адаптации к теме. '
        'Чтобы иконка менялась вместе с темой: '
        '1) Используйте fill="currentColor" или stroke="currentColor" в SVG. '
        '2) Не задавайте жёстких цветов в SVG — VS Code сам применит нужный через CSS. '
        '3) Для двух вариантов (тёмная/светлая тема) укажите "iconDefinitions": '
        '{ "_ts": { "iconPath": "./light.svg" }, "_ts_dark": { "iconPath": "./dark.svg" } } '
        'и "fileExtensions": { "ts": "_ts" } с "light": { "fileExtensions": { "ts": "_ts" } }, '
        '"highContrast": {...}. '
        'Проверяйте результат переключением темы прямо в Extension Dev Host.',
        'tip'))
    add(sp(6))

    add(box('SVG запрещены для иконки расширения — но не для UI',
        'Поле "icon" в package.json (иконка на Marketplace и в Extensions panel) '
        'принимает ТОЛЬКО PNG 128×128. SVG здесь отклоняется при публикации через vsce. '
        'НО: иконки внутри расширения (File Icon Theme, Activity Bar, команды) — '
        'могут и должны быть SVG. '
        'TSX/JSX с <svg> тегом внутри — это просто код компонента, '
        'он не подпадает под это ограничение. '
        'Ограничение распространяется только на поле "icon" верхнего уровня в package.json.',
        'warn'))
    add(pb())

    # ── ГЛАВА 6 ────────────────────────────────────────────────────────────────
    ch('6', 'Tree View API', 'Кастомные представления в боковой панели VS Code')

    add(h2('Обзор Tree View API'))
    add(p('Tree View API создаёт иерархические представления данных в боковой панели — точно как встроенные Explorer, Source Control и Extensions. Три части: объявление в package.json → реализация TreeDataProvider → регистрация.'))
    add(sp(6))

    add(h2('Шаг 1: объявление в package.json'))
    add(code([
        '"contributes": {',
        '  // Контейнер в Activity Bar',
        '  "viewsContainers": {',
        '    "activitybar": [{',
        '      "id": "myExtension",',
        '      "title": "My Extension",',
        '      "icon": "$(extensions)"',
        '    }]',
        '  },',
        '  // View внутри контейнера',
        '  "views": {',
        '    "myExtension": [{',
        '      "id": "myExt.nodeList",',
        '      "name": "Node Dependencies",',
        '      "icon": "$(package)"',
        '    }],',
        '    // Или в стандартных контейнерах',
        '    "explorer": [{',
        '      "id": "myExt.quickAccess",',
        '      "name": "Quick Access"',
        '    }]',
        '  },',
        '  // Кнопки в заголовке View',
        '  "menus": {',
        '    "view/title": [{',
        '      "command": "myExt.refresh",',
        '      "when": "view == myExt.nodeList",',
        '      "group": "navigation"',
        '    }],',
        '    // Кнопки на элементах',
        '    "view/item/context": [{',
        '      "command": "myExt.delete",',
        '      "when": "view == myExt.nodeList && viewItem == dependency"',
        '    }]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Три части объявления Tree View. <b>viewsContainers.activitybar</b> добавляет иконку в боковую панель Activity Bar — это контейнер для ваших View. <b>views</b> регистрирует конкретные панели внутри контейнера; можно размещать View и в стандартных контейнерах (explorer, scm, debug). <b>menus</b> с ключами view/title и view/item/context добавляет кнопки: в заголовке View (обычно Refresh) и на отдельных элементах (Delete, Edit). Условие <b>viewItem == dependency</b> в when фильтрует элементы по contextValue — это позволяет показывать разные действия для разных типов узлов дерева.'))

    add(sp(6))

    add(h2('Шаг 2: модель данных и TreeDataProvider'))
    add(code([
        'import * as vscode from \'vscode\';',
        'import * as fs from \'fs\';',
        'import * as path from \'path\';',
        '',
        '// Элемент дерева',
        'class Dependency extends vscode.TreeItem {',
        '    constructor(',
        '        public readonly label: string,',
        '        public readonly version: string,',
        '        public readonly collapsibleState: vscode.TreeItemCollapsibleState',
        '    ) {',
        '        super(label, collapsibleState);',
        '        this.tooltip   = `${label}@${version}`;',
        '        this.description = version;',
        '        this.iconPath  = new vscode.ThemeIcon(\'package\');',
        '        // contextValue используется в "when" условиях меню',
        '        this.contextValue = \'dependency\';',
        '    }',
        '}',
        '',
        '// Провайдер данных',
        'class NodeDependenciesProvider',
        '    implements vscode.TreeDataProvider<Dependency> {',
        '',
        '    private _onChange = new vscode.EventEmitter<Dependency | undefined>();',
        '    readonly onDidChangeTreeData = this._onChange.event;',
        '',
        '    refresh(): void { this._onChange.fire(undefined); }',
        '',
        '    getTreeItem(dep: Dependency): vscode.TreeItem { return dep; }',
        '',
        '    getChildren(dep?: Dependency): Thenable<Dependency[]> {',
        '        if (!vscode.workspace.workspaceFolders) return Promise.resolve([]);',
        '        if (!dep) return this.getRootDeps();',
        '        return Promise.resolve([]);  // дочерние зависимости',
        '    }',
        '',
        '    private getRootDeps(): Promise<Dependency[]> {',
        '        const folders = vscode.workspace.workspaceFolders!;',
        '        const pkgPath = path.join(folders[0].uri.fsPath, \'package.json\');',
        '        if (!fs.existsSync(pkgPath)) return Promise.resolve([]);',
        '',
        '        const pkg = JSON.parse(fs.readFileSync(pkgPath, \'utf8\'));',
        '        return Promise.resolve(',
        '            Object.entries(pkg.dependencies || {}).map(([name, ver]) =>',
        '                new Dependency(',
        '                    name, ver as string,',
        '                    vscode.TreeItemCollapsibleState.Collapsed',
        '                )',
        '            )',
        '        );',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('<b>getChildren(element)</b> возвращает дочерние узлы дерева; вызов без аргумента означает запрос корневых элементов. <b>getTreeItem()</b> конвертирует элемент данных в <b>TreeItem</b> с лейблом и иконкой. EventEmitter в <b>onDidChangeTreeData</b> сигнализирует VS Code об обновлении дерева.'))
    add(sp(6))

    add(h2('Шаг 3: регистрация и TreeView'))
    add(code([
        'export function activate(context: vscode.ExtensionContext) {',
        '    const provider = new NodeDependenciesProvider();',
        '',
        '    // createTreeView — больше возможностей, чем registerTreeDataProvider',
        '    const treeView = vscode.window.createTreeView(\'myExt.nodeList\', {',
        '        treeDataProvider: provider,',
        '        showCollapseAll: true,   // кнопка "свернуть всё"',
        '        canSelectMany: true,     // множественный выбор',
        '    });',
        '',
        '    // Реакция на выбор элемента',
        '    treeView.onDidChangeSelection(e => {',
        '        console.log(\'Выбрано:\', e.selection.map(d => d.label));',
        '    });',
        '',
        '    // Программный выбор элемента',
        '    // await treeView.reveal(dep, { select: true, expand: true });',
        '',
        '    const refreshCmd = vscode.commands.registerCommand(',
        '        \'myExt.refresh\', () => provider.refresh()',
        '    );',
        '',
        '    context.subscriptions.push(treeView, refreshCmd);',
        '}',
    ]))
    add(sp(3))
    add(p('Регистрация через <b>createTreeView()</b> вместо registerTreeDataProvider — даёт объект TreeView с дополнительными возможностями: <b>showCollapseAll</b> добавляет кнопку «свернуть всё», <b>canSelectMany</b> включает множественный выбор с Ctrl/Shift. Событие <b>onDidChangeSelection</b> позволяет реагировать на выбор элемента. Метод <b>reveal()</b> программно раскрывает и выделяет элемент — полезно для навигации к результатам поиска. И treeView, и команда refresh регистрируются в context.subscriptions для автоматической очистки.'))
    add(sp(4))
    add(box('DragAndDrop',
        'С VS Code 1.70+ Tree View поддерживает Drag and Drop через '
        'TreeDragAndDropController. Позволяет перетаскивать элементы внутри и '
        'между представлениями.', 'tip'))
    add(sp(8))
    add(h3('Как выглядит Tree View в редакторе'))
    add(sp(4))
    # Tree View screenshot with text wrapping (image left, text right)
    import os as _os_local
    from reportlab.platypus import Image as RLImage
    _img_path = _os_local.path.join(_os_local.path.dirname(_os_local.path.abspath(__file__)), 'screenshots', '05-explorer-sidebar.png')
    _tv_img = RLImage(_img_path)
    _iw, _ih = _tv_img.imageWidth, _tv_img.imageHeight
    _scale = min(CW * 0.35 / _iw, 280 / _ih)
    _tv_img = RLImage(_img_path, width=_iw * _scale, height=_ih * _scale)
    _tv_text = Paragraph(
        'Tree View — иерархическое представление данных в боковой панели VS Code. '
        'Здесь показан Explorer с файлами проекта расширения: src/ с TypeScript-файлами, '
        'package.json, tsconfig.json. Аналогичные Tree View создаются через <b>TreeDataProvider</b> '
        'для кастомных данных — зависимости, задачи, закладки.',
        S['body']
    )
    _tv_table = Table([[_tv_img, _tv_text]], colWidths=[CW * 0.38, CW * 0.62])
    _tv_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('LEFTPADDING', (1, 0), (1, 0), 12),
    ]))
    add(_tv_table)
    add(Paragraph('Tree View: иерархические данные в боковой панели VS Code', S['caption']))
    add(pb())

    # ── ГЛАВА 6.5: Decoration API ─────────────────────────────────────────────
    ch('6.5', 'Decoration API и встроенные компоненты',
       'Визуальная разметка редактора без Webview')

    add(h2('Decoration API — что это и зачем'))
    add(p('Decoration API позволяет визуально выделять диапазоны текста в редакторе: '
          'фоновые подсветки, рамки, цвет текста, иконки на полях, inline-текст. '
          'Это <b>намного легче Webview</b> и полностью интегрировано в DOM редактора.'))
    add(sp(3))
    add(p('Примеры использования: подсветка ошибок (красный фон), '
          'обнаружение секретов (GitGuardian), coverage-линии (зелёный/красный gutter), '
          'git blame аннотации (GitLens), indent guides (встроенные).'))
    add(sp(4))
    add(h3('Как выглядят декорации'))
    add(p('Примеры визуального результата — фоновая подсветка секрета и squiggly-ошибка:'))
    add(sp(4))
    add(screenshot('09-editor-with-file.png', 'Редактор VS Code с подсветкой синтаксиса и номерами строк'))
    add(sp(6))

    add(h2('Создание и применение декораций'))
    add(code([
        '// 1. Создаём тип декорации (один раз, при активации)',
        'const secretDecoration = vscode.window.createTextEditorDecorationType({',
        '    // Фон',
        '    backgroundColor: "rgba(139, 26, 26, 0.4)",',
        '    border: "1px solid #FF4444",',
        '    borderRadius: "2px",',
        '',
        '    // Иконка на левом поле (gutter)',
        '    gutterIconPath: context.asAbsolutePath("./icons/warning.svg"),',
        '    gutterIconSize: "contain",',
        '',
        '    // Inline текст после строки (after pseudo-element)',
        '    after: {',
        '        contentText: "  ← secret detected",',
        '        color: "#FF6666",',
        '        fontStyle: "italic",',
        '        fontSize: "0.85em",',
        '    },',
        '',
        '    // Опционально: overviewRuler (полоска справа)',
        '    overviewRulerColor: "#FF4444",',
        '    overviewRulerLane: vscode.OverviewRulerLane.Right,',
        '});',
        '',
        '// 2. Применяем к редактору',
        'function applyDecorations(editor: vscode.TextEditor) {',
        '    const ranges: vscode.DecorationOptions[] = [];',
        '',
        '    // Ищем паттерн в тексте',
        '    const text = editor.document.getText();',
        '    const pattern = /sk-[a-zA-Z0-9]{32,}/g;',
        '    let match;',
        '    while ((match = pattern.exec(text)) !== null) {',
        '        const start = editor.document.positionAt(match.index);',
        '        const end = editor.document.positionAt(match.index + match[0].length);',
        '        ranges.push({ range: new vscode.Range(start, end) });',
        '    }',
        '',
        '    editor.setDecorations(secretDecoration, ranges);',
        '}',
        '',
        '// 3. Обновляем при изменении',
        'vscode.window.onDidChangeActiveTextEditor(editor => {',
        '    if (editor) applyDecorations(editor);',
        '}, null, context.subscriptions);',
        '',
        '// 4. Очищаем при деактивации (через Disposable)',
        'context.subscriptions.push(secretDecoration);',
    ]))
    add(sp(3))
    add(p('Полный цикл работы с декорациями из 4 шагов. <b>1) Тип</b> — createTextEditorDecorationType() описывает визуальный стиль: фон, рамка, иконка в gutter, inline-текст через pseudo-element after, маркер на overviewRuler (полоска справа). Создаётся один раз при активации. <b>2) Применение</b> — функция ищет паттерн в тексте (здесь — API-ключи вида sk-...), конвертирует позиции через positionAt() и передаёт массив Range в setDecorations(). <b>3) Обновление</b> — подписка на onDidChangeActiveTextEditor пересчитывает декорации при переключении вкладок. <b>4) Очистка</b> — DecorationType добавляется в subscriptions; не создавайте новый тип при каждом обновлении — обновляйте только массив ranges.'))
    add(sp(6))

    add(h2('Типы декораций'))
    add(tblh(['Свойство', 'Описание']))
    add(tbl2([
        ('backgroundColor',    'Фоновый цвет диапазона. rgba() для прозрачности'),
        ('border / borderRadius', 'Рамка вокруг диапазона'),
        ('color',              'Цвет текста внутри диапазона'),
        ('fontWeight / fontStyle', 'Жирность и курсив'),
        ('textDecoration',     'CSS text-decoration: underline, line-through...'),
        ('gutterIconPath',     'Иконка на левом поле (gutter). SVG или PNG'),
        ('before / after',     'Виртуальный текст до/после (contentText, color, fontSize)'),
        ('overviewRulerColor', 'Цвет маркера на вертикальном скроллбаре справа'),
        ('isWholeLine',        'True — применить ко всей строке, не только диапазону'),
        ('rangeBehavior',      'Поведение при редактировании внутри диапазона'),
    ]))
    add(sp(6))

    add(h2('Встроенные UI-компоненты редактора'))
    add(p('Перед тем как создавать Webview, убедитесь что нативных компонентов недостаточно. '
          'Они <b>быстрее, легче и лучше интегрированы</b> в VS Code:'))
    add(sp(3))
    add(tblh(['Компонент', 'API и назначение']))
    add(tbl2([
        ('InputBox',        'showInputBox() — однострочный ввод с валидацией'),
        ('Quick Pick',      'showQuickPick() — список с поиском, множественный выбор, разделители'),
        ('Quick Input',     'createQuickPick() — полный контроль над Quick Pick панелью'),
        ('Message',         'showInformationMessage/Warning/Error — уведомления с кнопками'),
        ('Progress',        'withProgress() — прогресс в Notification или Status Bar'),
        ('Status Bar Item', 'createStatusBarItem() — элемент в строке состояния'),
        ('Output Channel',  'createOutputChannel() — панель вывода (лог-канал)'),
        ('Terminal',        'createTerminal() — встроенный терминал'),
        ('Text Decoration', 'createTextEditorDecorationType() — подсветка текста'),
        ('CodeLens',        'registerCodeLensProvider() — ссылки над строками кода'),
        ('Hover',           'registerHoverProvider() — всплывающие подсказки'),
        ('InlayHint',       'registerInlayHintsProvider() — inline-подсказки (типы, имена параметров)'),
    ]))
    add(pb())

    # ── ГЛАВА 7 ────────────────────────────────────────────────────────────────
    ch('7', 'Webview API', 'Встроенные веб-страницы внутри VS Code')

    add(h2('Что такое Webview?'))
    add(p('Webview — это iframe внутри VS Code, которым управляет расширение. Может рендерить любой HTML. Общается с расширением через сообщения. Используется в трёх сценариях:'))
    add(sp(2))
    for item in [
        '<b>WebviewPanel</b> — отдельная вкладка редактора с кастомным контентом',
        '<b>Custom Editor</b> — кастомный редактор для определённых типов файлов',
        '<b>WebviewView</b> — панель в боковой панели (Sidebar или Panel)',
    ]:
        add(bul(item))
    add(sp(4))
    add(box('Когда использовать Webview?',
        'Webview ресурсоёмки и работают в отдельном контексте. Используйте только когда '
        'нативного API недостаточно. Сначала рассмотрите TreeView, Decoration API и '
        'встроенные компоненты.', 'warn'))
    add(sp(4))
    add(box('CSS-переменные тем — обязательно для нативного вида',
        'Webview — изолированный iframe. Без CSS-переменных он выглядит как чужеродный сайт. '
        'Используйте var(--vscode-editor-background), var(--vscode-button-background) и другие — '
        'они автоматически обновляются при смене темы. '
        'VS Code добавляет класс vscode-dark / vscode-light / vscode-high-contrast на <body>. '
        'Полный справочник переменных — <a href="#appendix_D">Справочник D</a> в конце книги.',
        'tip'))
    add(sp(6))

    add(h2('Создание WebviewPanel'))
    add(code([
        'function createPanel(context: vscode.ExtensionContext) {',
        '    const panel = vscode.window.createWebviewPanel(',
        '        \'myWebview\',',
        '        \'Мой Дашборд\',',
        '        vscode.ViewColumn.One,',
        '        {',
        '            enableScripts: true,',
        '            retainContextWhenHidden: true,  // не сбрасывать при скрытии',
        '            localResourceRoots: [',
        '                vscode.Uri.joinPath(context.extensionUri, \'media\')',
        '            ]',
        '        }',
        '    );',
        '',
        '    panel.webview.html = getHtml(panel.webview, context.extensionUri);',
        '',
        '    // Сообщения от Webview к расширению',
        '    panel.webview.onDidReceiveMessage(msg => {',
        '        switch (msg.command) {',
        '            case \'alert\':',
        '                vscode.window.showInformationMessage(msg.text);',
        '                break;',
        '            case \'getData\':',
        '                panel.webview.postMessage({ command: \'data\', items: [1,2,3] });',
        '                break;',
        '        }',
        '    }, undefined, context.subscriptions);',
        '',
        '    // Отправка из расширения в Webview',
        '    panel.webview.postMessage({ command: \'init\', config: { theme: \'dark\' } });',
        '',
        '    panel.onDidDispose(() => console.log(\'Webview закрыт\'));',
        '}',
    ]))
    add(sp(3))
    add(p('<b>createWebviewPanel()</b> создаёт изолированный iframe внутри VS Code. <b>enableScripts: true</b> разрешает JavaScript (по умолчанию отключено). <b>localResourceRoots</b> ограничивает доступ к файлам расширения — обязательно для безопасности. Связь двусторонняя: <b>postMessage()</b> → Webview, <b>onDidReceiveMessage</b> ← Webview.'))
    add(sp(6))

    add(h2('HTML с Content Security Policy'))
    add(code([
        'function getHtml(webview: vscode.Webview, extUri: vscode.Uri): string {',
        '    // Конвертируем локальный путь в URI для Webview',
        '    const scriptUri = webview.asWebviewUri(',
        '        vscode.Uri.joinPath(extUri, \'media\', \'main.js\')',
        '    );',
        '    const styleUri = webview.asWebviewUri(',
        '        vscode.Uri.joinPath(extUri, \'media\', \'style.css\')',
        '    );',
        '    // Nonce для Content Security Policy',
        '    const nonce = [...Array(32)].map(() =>',
        '        \'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\'',
        '            .charAt(Math.floor(Math.random() * 62))',
        '    ).join(\'\');',
        '',
        '    return `<!DOCTYPE html>',
        '    <html lang="ru">',
        '    <head>',
        '        <meta charset="UTF-8">',
        '        <meta http-equiv="Content-Security-Policy"',
        '            content="default-src \'none\';',
        '                     style-src ${webview.cspSource};',
        '                     script-src \'nonce-${nonce}\';">',
        '        <link href="${styleUri}" rel="stylesheet">',
        '    </head>',
        '    <body>',
        '        <h1>Hello from Webview!</h1>',
        '        <button id="btn">Отправить сообщение</button>',
        '        <div id="output"></div>',
        '        <script nonce="${nonce}" src="${scriptUri}"></script>',
        '    </body>',
        '    </html>`;',
        '}',
    ]))
    add(sp(3))
    add(p('HTML для Webview генерируется динамически с <b>nonce</b> — случайным значением, разрешённым в Content Security Policy. Это блокирует выполнение вредоносных скриптов. <b>webview.asWebviewUri()</b> конвертирует путь к файлу в URI, доступный из iframe.'))
    add(sp(3))
    add(code([
        '// media/main.js — код внутри Webview',
        'const vscode = acquireVsCodeApi();',
        '',
        '// Отправка в расширение',
        'document.getElementById(\'btn\').addEventListener(\'click\', () => {',
        '    vscode.postMessage({ command: \'alert\', text: \'Привет из Webview!\' });',
        '});',
        '',
        '// Получение от расширения',
        'window.addEventListener(\'message\', event => {',
        '    const { command, items } = event.data;',
        '    if (command === \'data\') {',
        '        document.getElementById(\'output\').textContent =',
        '            JSON.stringify(items);',
        '    }',
        '});',
        '',
        '// Сохранение состояния между show/hide',
        'const state = vscode.getState() || { count: 0 };',
        'function save(newState) { vscode.setState(newState); }',
    ]))
    add(sp(3))
    add(p('Двусторонняя связь Webview ↔ расширение: <b>webview.postMessage(data)</b> отправляет объект в iframe (получается через <b>window.addEventListener("message")</b>). В обратную сторону — <b>vscode.postMessage()</b> из iframe, перехватывается через <b>onDidReceiveMessage</b>.'))
    add(sp(4))
    add(box('Content Security Policy (CSP)',
        'ВСЕГДА устанавливайте строгий CSP. Без него Webview уязвим к XSS-атакам. '
        'Используйте nonce для каждого тега script. '
        'default-src \'none\' — хорошая база. '
        'Важно: это актуально не только для безопасности — VS Code имеет Web-версию '
        '(vscode.dev, github.dev, code-server). Там Webview выполняется в реальном браузере '
        'и CSP строго соблюдается движком Chromium. '
        'Расширение без CSP или с unsafe-inline может вообще не работать в Web-версии. '
        'Тестируйте расширение на vscode.dev если планируете поддерживать Web Extension.',
        'warn'))
    add(pb())

    # ── ГЛАВА 8 ────────────────────────────────────────────────────────────────
    ch('8', 'Custom Editors и Virtual Documents', 'Кастомные редакторы для нестандартных форматов')

    add(h2('Custom Text Editor'))
    add(p('Custom Editor позволяет предоставить собственный UI для редактирования файлов. Когда пользователь открывает файл, VS Code может использовать ваш редактор вместо стандартного текстового.'))
    add(sp(4))
    add(code([
        '"contributes": {',
        '  "customEditors": [{',
        '    "viewType": "myext.jsonVisual",',
        '    "displayName": "JSON Visual Editor",',
        '    "selector": [{ "filenamePattern": "*.json" }],',
        '    "priority": "option"  // "default" | "option"',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Объявление кастомного редактора. <b>viewType</b> — уникальный ID, используется при регистрации провайдера. <b>selector</b> с filenamePattern определяет, для каких файлов доступен редактор. <b>priority: "option"</b> — редактор предлагается как альтернатива (через «Open With...»); <b>"default"</b> — открывается автоматически вместо стандартного текстового.'))

    add(sp(3))
    add(code([
        'class JsonEditorProvider implements vscode.CustomTextEditorProvider {',
        '',
        '    resolveCustomTextEditor(',
        '        document: vscode.TextDocument,',
        '        panel: vscode.WebviewPanel,',
        '        _token: vscode.CancellationToken',
        '    ): void {',
        '        panel.webview.options = { enableScripts: true };',
        '        panel.webview.html = this.getHtml();',
        '',
        '        // Документ → Webview',
        '        const updateWebview = () => {',
        '            panel.webview.postMessage({',
        '                type: \'update\',',
        '                text: document.getText(),',
        '            });',
        '        };',
        '',
        '        vscode.workspace.onDidChangeTextDocument(e => {',
        '            if (e.document.uri.toString() === document.uri.toString())',
        '                updateWebview();',
        '        });',
        '',
        '        // Webview → документ',
        '        panel.webview.onDidReceiveMessage(e => {',
        '            if (e.type === \'edit\') {',
        '                const edit = new vscode.WorkspaceEdit();',
        '                edit.replace(',
        '                    document.uri,',
        '                    new vscode.Range(0, 0, document.lineCount, 0),',
        '                    e.content',
        '                );',
        '                vscode.workspace.applyEdit(edit);',
        '            }',
        '        });',
        '',
        '        updateWebview();',
        '    }',
        '}',
        '',
        '// Регистрация',
        'context.subscriptions.push(',
        '    vscode.window.registerCustomEditorProvider(',
        '        \'myext.jsonVisual\',',
        '        new JsonEditorProvider()',
        '    )',
        ');',
    ]))
    add(sp(3))
    add(p('Реализация Custom Text Editor. Метод <b>resolveCustomTextEditor()</b> получает TextDocument (стандартную модель VS Code) и WebviewPanel — ваш UI. Ключевая задача — синхронизация в обе стороны: при изменении документа (onDidChangeTextDocument) обновляем Webview через postMessage, при правках в Webview (onDidReceiveMessage) обновляем документ через WorkspaceEdit. Важно: VS Code сам управляет сохранением и undo/redo для TextDocument — ваш редактор получает это бесплатно. Регистрация через registerCustomEditorProvider связывает viewType из package.json с провайдером.'))
    add(sp(6))

    add(h2('Virtual Documents'))
    add(p('Virtual Documents — файлы, существующие только в памяти, без физического файла на диске. '
          'VS Code открывает их через кастомную схему URI (<b>myscheme:/path/file.md</b>), '
          'показывает в редакторе как обычный файл, но читает содержимое у вашего провайдера.'))
    add(sp(3))
    add(h3('Реальные примеры использования'))
    for item in [
        '<b>MongoDB for VS Code</b> — при открытии JSON-документа из базы данных '
        'расширение создаёт Virtual Document с URI вида <b>mongodb:/collection/doc_id.json</b>. '
        'Пользователь редактирует JSON прямо в редакторе, расширение перехватывает сохранение '
        'и обновляет документ в MongoDB',
        '<b>Git Diff</b> (встроенный) — файлы HEAD~1 открываются как virtual documents '
        'со схемой <b>git:/path/to/file</b>',
        '<b>decompiled.code</b> (Java/Kotlin) — "Go to Definition" открывает декомпилированный '
        'исходник .class-файла как virtual .java документ (схема <b>jdt:/</b>)',
        '<b>REST Client</b> — ответ HTTP-запроса отображается как virtual .json документ',
        '<b>SVG Preview</b> и аналоги — Preview panel с рендером без изменения оригинала',
    ]:
        add(bul(item))
    add(sp(4))
    add(code([
        '// 1. Реализуем провайдер',
        'const provider: vscode.TextDocumentContentProvider = {',
        '    // EventEmitter позволяет обновлять содержимое документа',
        '    onDidChange: onDidChangeEmitter.event,',
        '',
        '    // Вызывается когда VS Code хочет получить текст документа',
        '    provideTextDocumentContent(uri: vscode.Uri): string {',
        '        // uri.path содержит путь, uri.query — параметры запроса',
        '        const docId = uri.path.replace(\'/\', \'\');',
        '        const data = myDatabase.getDocument(docId);',
        '        return JSON.stringify(data, null, 2);',
        '    }',
        '};',
        '',
        '// 2. Регистрируем схему (один раз при активации)',
        'const reg = vscode.workspace.registerTextDocumentContentProvider(',
        '    \'mongodb\',  // схема — часть URI до ://',
        '    provider',
        ');',
        'context.subscriptions.push(reg);',
        '',
        '// 3. Открываем виртуальный документ',
        'const uri = vscode.Uri.parse(`mongodb:/users/${docId}.json`);',
        'const doc = await vscode.workspace.openTextDocument(uri);',
        'await vscode.window.showTextDocument(doc, {',
        '    preview: false,  // открыть как постоянную вкладку, не превью',
        '});',
        '',
        '// 4. Перехватываем сохранение (onWillSaveTextDocument)',
        'vscode.workspace.onWillSaveTextDocument(e => {',
        '    if (e.document.uri.scheme !== \'mongodb\') return;',
        '    const updated = JSON.parse(e.document.getText());',
        '    const docId = e.document.uri.path.replace(\'/\', \'\').replace(\'.json\', \'\');',
        '    // e.waitUntil() блокирует сохранение пока не завершится промис',
        '    e.waitUntil(myDatabase.updateDocument(docId, updated));',
        '});',
        '',
        '// 5. Обновляем содержимое при изменении в БД',
        'onDidChangeEmitter.fire(uri);  // вызывает повторный вызов provideTextDocumentContent',
    ]))
    add(sp(3))
    add(p('Полный цикл Virtual Document из 5 шагов. <b>1)</b> TextDocumentContentProvider с методом provideTextDocumentContent — возвращает строку содержимого по URI. <b>2)</b> Регистрация кастомной схемы (mongodb://) — VS Code будет обращаться к провайдеру для любого URI с этой схемой. <b>3)</b> Открытие через openTextDocument(uri) + showTextDocument() — файл появляется в редакторе как обычная вкладка. <b>4)</b> Перехват сохранения через onWillSaveTextDocument — e.waitUntil() блокирует сохранение, пока промис не завершится (здесь — запись в БД). <b>5)</b> Обновление: fire(uri) через EventEmitter вызывает повторный provideTextDocumentContent.'))
    add(sp(3))
    add(p('<b>Ограничения Virtual Documents:</b> они доступны только для чтения по умолчанию. '
          'Для редактируемых виртуальных файлов нужен полноценный <b>FileSystemProvider</b> '
          '(registerFileSystemProvider) — он реализует весь интерфейс файловой системы: '
          'read, write, stat, readDirectory и т.д.'))
    add(pb())

    # ── ГЛАВА 9 ────────────────────────────────────────────────────────────────
    ch('9', 'Языковые расширения', 'Синтаксис, сниппеты, IntelliSense, диагностика')

    add(h2('Декларативный vs программный подход'))
    add(tblh(['Подход', 'Описание и примеры']))
    add(tbl2([
        ('Декларативный',
         'Объявляется в package.json без кода. '
         'Синтаксическая подсветка (TextMate), сниппеты, конфигурация языка'),
        ('Программный',
         'Реализуется через vscode.languages.* API. '
         'Completion, hover, diagnostics, formatting, code actions, rename, go-to-definition'),
    ]))
    add(sp(6))

    add(h2('Объявление языка'))
    add(code([
        '"contributes": {',
        '  "languages": [{',
        '    "id": "mylang",',
        '    "aliases": ["MyLang", "my-lang"],',
        '    "extensions": [".ml", ".mylang"],',
        '    "filenames": ["Makefile.ml"],',
        '    "configuration": "./language-configuration.json",',
        '    "icon": { "light": "./icons/ml-light.png", "dark": "./icons/ml-dark.png" }',
        '  }],',
        '  "grammars": [{',
        '    "language": "mylang",',
        '    "scopeName": "source.mylang",',
        '    "path": "./syntaxes/mylang.tmLanguage.json"',
        '  }],',
        '  "snippets": [{ "language": "mylang", "path": "./snippets/mylang.json" }]',
        '}',
    ]))
    add(sp(3))
    add(p('Декларативная часть языкового расширения — три блока в contributes. <b>languages</b> регистрирует язык: id используется во всех API, extensions/filenames определяют автоматическую привязку файлов, icon показывается в Explorer. <b>grammars</b> подключает TextMate-грамматику для синтаксической подсветки (scopeName — корневой scope, по конвенции source.langname). <b>snippets</b> — файл со сниппетами для этого языка. Всё это работает без единой строки JavaScript.'))

    add(sp(3))
    add(code([
        '// language-configuration.json',
        '{',
        '  "comments": { "lineComment": "//", "blockComment": ["/*", "*/"] },',
        '  "brackets": [["{","}"],[  "[","]"],["(",")" ]],',
        '  "autoClosingPairs": [',
        '    { "open": "{", "close": "}" },',
        '    { "open": "[", "close": "]" },',
        '    { "open": "(", "close": ")" },',
        '    { "open": "\\"", "close": "\\"", "notIn": ["string"] }',
        '  ],',
        '  "indentationRules": {',
        '    "increaseIndentPattern": "^.*\\\\{[^}]*$",',
        '    "decreaseIndentPattern": "^\\\\s*[}\\\\]]"',


        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Конфигурация языка определяет поведение редактора без грамматики и без кода. <b>comments</b> — какие символы начинают комментарий (Ctrl+/ будет использовать lineComment). <b>brackets</b> — пары скобок для подсветки и автозакрытия. <b>autoClosingPairs</b> — автоматическое закрытие; notIn: ["string"] отключает автозакрытие кавычек внутри строк. <b>indentationRules</b> — регулярные выражения для автоотступов: increaseIndentPattern срабатывает после строки с открывающей скобкой, decreaseIndentPattern — при вводе закрывающей.'))
    add(sp(6))

    add(h2('Completion Provider'))
    add(code([
        'const completionProvider = vscode.languages.registerCompletionItemProvider(',
        '    { scheme: \'file\', language: \'mylang\' },',
        '    {',
        '        provideCompletionItems(doc: vscode.TextDocument, pos: vscode.Position) {',
        '            const prefix = doc.lineAt(pos).text.substring(0, pos.character);',
        '            if (!prefix.endsWith(\'.\')) return undefined;',
        '',
        '            const items = [',
        '                new vscode.CompletionItem(\'toString\', vscode.CompletionItemKind.Method),',
        '                new vscode.CompletionItem(\'length\',   vscode.CompletionItemKind.Property),',
        '            ];',
        '            items[0].documentation = new vscode.MarkdownString(\'Преобразует в строку\');',
        '            items[0].insertText    = new vscode.SnippetString(\'toString()$0\');',
        '            items[0].detail        = \'(): string\';',
        '            return items;',
        '        }',
        '    },',
        '    \'.\' // триггерные символы',
        ');',
        'context.subscriptions.push(completionProvider);',
    ]))
    add(sp(3))
    add(p('<b>CompletionItem</b> описывает один пункт автодополнения: <b>label</b> — отображаемый текст, <b>kind</b> — иконка (Function/Variable/Class), <b>insertText</b> — что вставляется. Провайдер вызывается при каждом вводе — всегда проверяйте <b>CancellationToken</b>.'))
    add(sp(4))

    add(h2('Diagnostics'))
    add(p('Diagnostics — это ошибки, предупреждения и информационные сообщения, которые появляются в панели <b>Problems</b> (Ctrl+Shift+M) и как подчёркивания в редакторе (красные волнистые линии для ошибок, жёлтые для предупреждений). Это основной способ показать пользователю проблемы в коде — аналог вывода ESLint, TypeScript или Pylint. Каждая диагностика привязана к конкретному диапазону в файле.'))
    add(sp(4))
    add(screenshot('13-problems-panel.png', 'Problems panel: ошибки и предупреждения из DiagnosticCollection'))
    add(sp(3))
    add(code([
        'const diagCol = vscode.languages.createDiagnosticCollection(\'mylang\');',
        'context.subscriptions.push(diagCol);',
        '',
        'function validate(doc: vscode.TextDocument) {',
        '    if (doc.languageId !== \'mylang\') return;',
        '    const diags: vscode.Diagnostic[] = [];',
        '    const pattern = /\\bTODO\\b/g;',
        '    let m;',
        '    while ((m = pattern.exec(doc.getText())) !== null) {',
        '        const d = new vscode.Diagnostic(',
        '            new vscode.Range(doc.positionAt(m.index), doc.positionAt(m.index + 4)),',
        '            \'Незавершённая задача\',',
        '            vscode.DiagnosticSeverity.Warning',
        '        );',
        '        d.source = \'mylang-linter\';',
        '        d.code = \'todo-warning\';',
        '        diags.push(d);',
        '    }',
        '    diagCol.set(doc.uri, diags);',
        '}',
        '',
        'vscode.workspace.onDidChangeTextDocument(e => validate(e.document), null, context.subscriptions);',
        'vscode.workspace.onDidOpenTextDocument(validate, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('<b>DiagnosticCollection.set(uri, diagnostics[])</b> атомарно заменяет все диагностики для файла в Problems panel. Вызывайте <b>collection.clear()</b> при закрытии файла или смене документа чтобы убирать устаревшие ошибки.'))
    add(sp(4))

    add(h2('Hover Provider'))
    add(code([
        'context.subscriptions.push(',
        '    vscode.languages.registerHoverProvider(\'mylang\', {',
        '        provideHover(doc: vscode.TextDocument, pos: vscode.Position) {',
        '            const range = doc.getWordRangeAtPosition(pos);',
        '            const word  = doc.getText(range);',
        '            if (word === \'print\') {',
        '                const md = new vscode.MarkdownString();',
        '                md.appendCodeblock(\'print(value: any): void\', \'typescript\');',
        '                md.appendMarkdown(\'\\n\\nВыводит значение в консоль\');',
        '                return new vscode.Hover(md, range);',
        '            }',
        '        }',
        '    })',
        ');',
    ]))
    add(sp(3))
    add(p('<b>HoverProvider.provideHover()</b> вызывается когда курсор задерживается над словом. <b>MarkdownString</b> позволяет использовать Markdown с подсветкой кода в hover-панели. Проверяйте <b>token.isCancellationRequested</b> — hover отменяется при движении мыши.'))
    add(pb())

    add(h2('Document Paste API (VS Code 1.97+)'))
    add(p('Document Paste API позволяет расширениям перехватывать операции copy/paste и модифицировать вставляемый контент. Доступен с VS Code 1.97:'))
    add(sp(3))
    add(code([
        'const pasteProvider: vscode.DocumentPasteEditProvider = {',
        '    async provideDocumentPasteEdits(',
        '        document: vscode.TextDocument,',
        '        ranges: readonly vscode.Range[],',
        '        dataTransfer: vscode.DataTransfer,',
        '        token: vscode.CancellationToken',
        '    ): Promise<vscode.DocumentPasteEdit | undefined> {',
        '        // Получаем вставляемый текст',
        '        const text = await dataTransfer.get(\'text/plain\')?.asString();',
        '        if (!text) return;',
        '',
        '        // Пример: автоимпорт при вставке компонента',
        '        if (text.startsWith(\'<\') && document.languageId === \'typescriptreact\') {',
        '            const componentName = text.match(/<(\\w+)/)?.[1];',
        '            if (componentName) {',
        '                const edit = new vscode.DocumentPasteEdit(text, \'Import and paste\');',
        '                const importLine = `import { ${componentName} } from \'./components\';\\n`;',
        '                edit.additionalEdit = new vscode.WorkspaceEdit();',
        '                edit.additionalEdit.insert(',
        '                    document.uri,',
        '                    new vscode.Position(0, 0),',
        '                    importLine',
        '                );',
        '                return edit;',
        '            }',
        '        }',
        '    }',
        '};',
        '',
        'context.subscriptions.push(',
        '    vscode.languages.registerDocumentPasteEditProvider(',
        '        { language: \'typescriptreact\' },',
        '        pasteProvider,',
        '        { pasteMimeTypes: [\'text/plain\'] }',
        '    )',
        ');',
    ]))
    add(sp(3))
    add(p('Document Paste API перехватывает вставку через <b>provideDocumentPasteEdits()</b>. <b>DataTransfer</b> содержит данные из буфера обмена в разных MIME-типах (text/plain, text/html, image/png). Провайдер возвращает <b>DocumentPasteEdit</b> с модифицированным текстом и опциональным <b>additionalEdit</b> — WorkspaceEdit, который применяется вместе со вставкой. Типичные применения: автоимпорт компонентов, конвертация HTML→Markdown, обработка вставленных изображений.'))
    add(pb())

    return A


if __name__ == '__main__':
    print(f'Part 1 has {len(build_story())} elements')
