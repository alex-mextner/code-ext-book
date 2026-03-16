from book_helpers import *

def build_story_ux():
    A = []
    def add(*x):
        for i in x: A.append(i)

    def section(title, sub='', anchor_key=None):
        if anchor_key:
            add(StableAnchor(anchor_key))
        add(toc_ch(title), banner('Пользовательский опыт', title, sub), sp(12))

    section('Проектирование UX расширения',
            'Ненавязчивость, обнаруживаемость и сосуществование',
            anchor_key='chapter_ux')

    from book_new import q_ux
    add(q_ux())
    add(sp(6))

    add(h2('Философия: расширение как хороший сосед'))
    add(p('Пользователь VS Code имеет в среднем <b>13–20 установленных расширений</b>. '
          'Каждое из них претендует на его внимание, занимает UI-пространство '
          'и влияет на производительность. Хорошее расширение ведёт себя как '
          'тихий профессионал: делает свою работу незаметно, появляется когда нужно '
          'и не создаёт шума.'))
    add(sp(4))
    add(p('Команда VS Code формулирует это как принцип <b>"Progressive Disclosure"</b> — '
          'постепенного раскрытия: базовая функциональность видна сразу, '
          'расширенные возможности скрыты и доступны когда нужны.'))
    add(sp(6))

    # ── 1. БЮДЖЕТ ВНИМАНИЯ ─────────────────────────────────────────────────────
    add(h1('Бюджет внимания пользователя'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Конкуренция за UI-пространство'))
    add(p('В VS Code ограниченное количество мест, куда расширения могут добавлять '
          'элементы. Представьте, что каждое место — это "слот", '
          'и бюджет на все расширения суммарно фиксирован:'))
    add(sp(3))
    add(tblh(['Место', 'Рекомендуемый лимит на одно расширение']))
    add(tbl2([
        ('Activity Bar',     '1 иконка — только если расширение требует постоянного доступа'),
        ('Status Bar',       '1–2 элемента максимум; только постоянно актуальная информация'),
        ('Editor Toolbar',   '1 кнопка; только для файлов целевого языка (через when)'),
        ('Context Menu',     '1–3 пункта; только релевантные для контекста'),
        ('Command Palette',  'Без ограничений, но именуйте с категорией: "My Ext: Action"'),
        ('Уведомления',      '0 при активации; только в ответ на явные действия пользователя'),
        ('Diagnostics',      'Только реальные проблемы; не превращайте в шум'),
    ]))
    add(sp(4))
    add(box('Реальность',
        'Когда 15 расширений добавляют по 2 элемента в Status Bar — '
        'нижняя строка VS Code превращается в нечитаемый набор иконок. '
        'Когда 5 расширений добавляют иконки в Activity Bar — '
        'он превращается в перегруженную панель. '
        'Ваше расширение — одно из многих. Минимизируйте след.', 'warn'))
    add(sp(6))

    add(h2('Принцип контекстуальности: показывать только релевантное'))
    add(p('Каждый элемент UI должен появляться только в релевантном контексте. '
          'Это главный механизм — условие <b>when</b> в Contribution Points:'))
    add(sp(3))
    add(code([
        '// ПЛОХО: кнопка видна всегда, даже в .json и .txt файлах',
        '"editor/title": [{',
        '  "command": "myGoExt.runFile",',
        '  "group": "navigation"',
        '}]',
        '',
        '// OK: ХОРОШО: кнопка только для Go файлов',
        '"editor/title": [{',
        '  "command": "myGoExt.runFile",',
        '  "when": "resourceLangId == go",',
        '  "group": "navigation"',
        '}]',
        '',
        '// OK: ЛУЧШЕ: только когда есть активный редактор с Go',
        '"editor/title": [{',
        '  "command": "myGoExt.runFile",',
        '  "when": "resourceLangId == go && !isInDiffEditor",',
        '  "group": "navigation"',
        '}]',
    ]))
    add(sp(3))
    add(p('Три варианта <b>when</b>-условия для кнопки в editor/title — от плохого к лучшему. Без условия кнопка видна для всех файлов, <b>resourceLangId == go</b> ограничивает по языку, а добавление <b>!isInDiffEditor</b> убирает кнопку из режима сравнения, где она бесполезна.'))

    add(sp(3))
    add(code([
        '// Status Bar: показывать только когда нужно',
        'const statusItem = vscode.window.createStatusBarItem(',
        '    vscode.StatusBarAlignment.Left, 10',
        ');',
        '',
        '// Слушаем смену активного редактора',
        'function updateVisibility(editor: vscode.TextEditor | undefined) {',
        '    if (editor?.document.languageId === \'go\') {',
        '        statusItem.show();',
        '    } else {',
        '        statusItem.hide();  // ← СКРЫВАЕМ для нерелевантных файлов',
        '    }',
        '}',
        '',
        'vscode.window.onDidChangeActiveTextEditor(updateVisibility,',
        '    null, context.subscriptions);',
        'updateVisibility(vscode.window.activeTextEditor);',
    ]))
    add(sp(3))
    add(p('Программное управление видимостью Status Bar элемента: <b>show()</b> и <b>hide()</b> вызываются при смене активного редактора через <b>onDidChangeActiveTextEditor</b>. Элемент виден только когда открыт файл нужного языка — в остальных случаях он скрыт и не занимает место.'))

    add(sp(6))

    add(h2('Дерево решений: нужно ли показывать уведомление?'))
    add(p('Официальное дерево решений VS Code team для уведомлений:'))
    add(sp(3))
    add(tblh(['Ситуация', 'Правильный ответ']))
    add(tbl2([
        ('Нужен немедленный ввод данных (multi-step)',   'Quick Pick или InputBox'),
        ('Нужен немедленный ввод (один шаг)',            'Modal Dialog'),
        ('Фоновый прогресс (низкий приоритет)',          'Progress в Status Bar'),
        ('Пользователь сам запустил операцию',           'Notification (при завершении)'),
        ('Несколько уведомлений подряд',                 'Объединить в одно'),
        ('Пользователю не нужно знать',                  'Ничего не показывать'),
        ('Ошибка в фоне которую нельзя исправить',       'Output Channel, не всплывашка'),
        ('Критическая ошибка требующая действия',        'Error notification с кнопкой'),
    ]))
    add(sp(4))
    add(box('Правило одного уведомления',
        'Показывайте максимум одно уведомление одновременно. '
        'Если нужно показать несколько — объедините или покажите последовательно '
        'после закрытия предыдущего.', 'note'))
    add(sp(4))
    from book_new import q_notifications
    add(q_notifications())
    add(sp(6))

    add(h2('Кнопка "Больше не показывать"'))
    add(p('Каждое уведомление, которое теоретически может повторяться, '
          'обязано иметь опцию отключения. Это официальное требование VS Code UX Guidelines:'))
    add(sp(3))
    add(code([
        'async function showImportantWarning(ctx: vscode.ExtensionContext) {',
        '    const DISMISSED_KEY = \'warningDismissed\';',
        '',
        '    // Не показываем если пользователь уже отклонил',
        '    if (ctx.globalState.get<boolean>(DISMISSED_KEY)) return;',
        '',
        '    const action = await vscode.window.showWarningMessage(',
        '        \'My Extension: обнаружена устаревшая конфигурация\',',
        '        \'Исправить\',',
        '        \'Подробнее\',',
        '        \'Больше не показывать\'  // ← ВСЕГДА включайте эту опцию',
        '    );',
        '',
        '    if (action === \'Исправить\') {',
        '        await fixConfiguration();',
        '    } else if (action === \'Подробнее\') {',
        '        vscode.env.openExternal(vscode.Uri.parse(DOCS_URL));',
        '    } else if (action === \'Больше не показывать\') {',
        '        await ctx.globalState.update(DISMISSED_KEY, true);',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('Паттерн «уведомление с памятью»: функция проверяет <b>globalState</b> и не показывает предупреждение повторно. Кнопка <b>«Больше не показывать»</b> записывает флаг в хранилище — это обязательный элемент любого повторяющегося уведомления по UX Guidelines VS Code.'))

    add(sp(6))

    # ── 2. ОБНАРУЖИВАЕМОСТЬ ────────────────────────────────────────────────────
    add(h1('Обнаруживаемость: "видимый, но ненавязчивый"'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Проблема: пользователи не читают README'))
    add(p('Исследования показывают, что большинство пользователей устанавливают '
          'расширение, пробуют одну-две команды и забывают про остальные возможности. '
          'Задача дизайна — сделать функции <b>обнаруживаемыми в нужный момент</b>.'))
    add(sp(6))

    add(h2('Walkthroughs — правильный onboarding'))
    add(p('Walkthroughs — встроенный VS Code механизм для интерактивного onboarding. '
          'Открывается через Get Started / Welcome и позволяет провести пользователя '
          'по ключевым возможностям без всплывающих окон:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "walkthroughs": [{',
        '    "id": "myExt.getStarted",',
        '    "title": "Начало работы с My Extension",',
        '    "description": "Освойте ключевые возможности за 5 минут",',
        '    "steps": [',
        '      {',
        '        "id": "myExt.step1",',
        '        "title": "Настройте расширение",',
        '        "description": "Откройте настройки и выберите параметры\\n[Открыть настройки](command:myExt.openSettings)",',
        '        "media": {',
        '          "svg": "media/step1.svg",',
        '          "altText": "Скриншот настроек"',
        '        },',
        '        "completionEvents": [',
        '          "onSettingsEdited:myExt.maxItems"',
        '        ]',
        '      },',
        '      {',
        '        "id": "myExt.step2",',
        '        "title": "Попробуйте основную функцию",',
        '        "description": "Нажмите кнопку или используйте команду\\n[Запустить команду](command:myExt.mainAction)",',
        '        "media": { "svg": "media/step2.svg", "altText": "Демонстрация" },',
        '        "completionEvents": ["onCommand:myExt.mainAction"]',
        '      }',
        '    ]',
        '  }]',
        '}',
        '',
        '// Открыть walkthrough программно (только при первой установке)',
        'if (!ctx.globalState.get(\'walkthroughShown\')) {',
        '    ctx.globalState.update(\'walkthroughShown\', true);',
        '    vscode.commands.executeCommand(',
        '        \'workbench.action.openWalkthrough\',',
        '        \'publisher.extension#myExt.getStarted\'',
        '    );',
        '}',
    ]))
    add(sp(3))
    add(p('Полная структура Walkthrough: в <b>package.json</b> объявляются шаги с заголовками, описаниями и <b>completionEvents</b> — VS Code автоматически отмечает шаг выполненным при срабатывании события (изменение настройки, выполнение команды). Ссылки <b>[текст](command:...)</b> в описании становятся кликабельными кнопками. Программное открытие через <b>workbench.action.openWalkthrough</b> привязано к флагу в globalState — показывается только при первой установке.'))

    add(sp(4))
    add(box('Требования к Walkthrough изображениям',
        'Используйте SVG с переменными CSS цветов темы VS Code — '
        'они автоматически адаптируются к тёмной и светлой теме. '
        'PNG/GIF будут выглядеть неуместно в тёмной теме. '
        'Плагин "VS Code Color Mapper" для Figma упрощает создание таких SVG.', 'tip'))
    add(sp(6))

    add(h2('Contextual Hints — подсказки в нужный момент'))
    add(p('Показывайте подсказки не при старте, а когда пользователь столкнулся '
          'с конкретной ситуацией:'))
    add(sp(3))
    add(code([
        '// Подсказка при первом открытии файла нужного типа',
        'let goHintShown = false;',
        '',
        'vscode.workspace.onDidOpenTextDocument(async doc => {',
        '    if (doc.languageId !== \'go\' || goHintShown) return;',
        '    if (ctx.globalState.get(\'goHintDismissed\')) return;',
        '',
        '    goHintShown = true;',
        '',
        '    // Ненавязчивая подсказка: status bar вместо уведомления',
        '    const hint = vscode.window.createStatusBarItem(',
        '        vscode.StatusBarAlignment.Right, 0',
        '    );',
        '    hint.text = \'$(lightbulb) My Ext: нажмите для быстрых действий\';',
        '    hint.command = \'myExt.showQuickActions\';',
        '    hint.backgroundColor = new vscode.ThemeColor(',
        '        \'statusBarItem.warningBackground\'',
        '    );',
        '    hint.show();',
        '',
        '    // Автоматически скрываем через 10 секунд',
        '    setTimeout(() => hint.dispose(), 10000);',
        '',
        '    context.subscriptions.push(hint);',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('Контекстная подсказка через временный Status Bar элемент вместо всплывающего уведомления. Подсказка появляется один раз при первом открытии файла нужного типа, подкрашивается через <b>warningBackground</b> для привлечения внимания и автоматически исчезает через 10 секунд с помощью <b>setTimeout + dispose()</b>.'))

    add(sp(4))

    add(h3('Welcome View — для пустых состояний'))
    add(p('Для Welcome View нужно сначала объявить сам View в <b>contributes.views</b> — ID вида <b>myExt.todoList</b> должен совпадать с полем <b>view</b> в viewsWelcome:'))
    add(sp(3))
    add(code([
        '// Сначала объявляем View в contributes.views',
        '"contributes": {',
        '  "viewsContainers": {',
        '    "activitybar": [{ "id": "myExtContainer", "title": "My Extension", "icon": "$(checklist)" }]',
        '  },',
        '  "views": {',
        '    "myExtContainer": [{',
        '      "id": "myExt.todoList",  // ← этот ID используется в viewsWelcome',
        '      "name": "TODO List"',
        '    }]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('После объявления View можно добавить Welcome-контент, который показывается когда View пуст:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "viewsWelcome": [{',
        '    "view": "myExt.todoList",',
        '    "contents": "Не найдено TODO-комментариев в проекте.\\n[Создать первый TODO](command:myExt.insertTodo)\\n[Настроить ключевые слова](command:myExt.openSettings)\\n[Открыть документацию](https://github.com/me/my-ext#readme)",',
        '    "when": "myExt.todoCount == 0"',
        '  }, {',
        '    "view": "myExt.todoList",',
        '    "contents": "Откройте папку с проектом для начала работы.",',
        '    "when": "!workspaceFolderCount"',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Два варианта Welcome View для разных состояний: когда в проекте нет TODO-комментариев (<b>myExt.todoCount == 0</b>) — ссылки на создание первого TODO и настройку; когда вообще не открыта папка (<b>!workspaceFolderCount</b>) — просьба открыть проект. Условие <b>when</b> определяет какой именно текст покажется.'))

    add(sp(6))

    add(h2('Именование команд: discoverable по умолчанию'))
    add(p('Большинство пользователей находят функции через Command Palette. '
          'Правильное именование — критически важно для обнаруживаемости:'))
    add(sp(3))
    add(tblh(['Плохо', 'Хорошо']))
    add(tbl2([
        ('"Run"',                          '"My Extension: Run File"'),
        ('"Format document"',              '"Prettier: Format Document" (с категорией)'),
        ('"myext.action1"',                '"My Extension: Perform Action 1"'),
        ('"Toggle feature"',               '"My Extension: Toggle Dark Mode Analysis"'),
        ('"Go: Build" (без контекста)',    '"Go: Build Current Package" (конкретно)'),
    ], 0.45))
    add(sp(3))
    add(code([
        '// Хорошее именование команды',
        '"contributes": {',
        '  "commands": [{',
        '    "command": "myGoExt.buildPackage",',
        '    "title": "Build Current Package",',  
        '    "category": "Go",',  
        '    "shortTitle": "Build",',  
        '    "icon": "$(package)"',
        '  }]',
        '}',
        '// В Command Palette будет: "Go: Build Current Package"',
        '// В контекстном меню: "Build" (через shortTitle)',
    ]))
    add(sp(3))
    add(p('Объявление команды с <b>category</b> — VS Code автоматически формирует имя «Go: Build Current Package» в Command Palette. Поле <b>shortTitle</b> используется в компактных местах (контекстное меню, Editor Toolbar), а <b>icon</b> с Codicon-синтаксисом <b>$(package)</b> задаёт иконку без кастомных SVG.'))

    add(sp(6))

    # ── 3. КОНФЛИКТЫ ──────────────────────────────────────────────────────────
    add(h1('Конфликты между расширениями'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Типы конфликтов'))
    add(tblh(['Тип конфликта', 'Примеры и решения']))
    add(tbl2([
        ('Форматтеры',
         'Prettier + другой форматтер конкурируют за один язык. '
         'Решение: объявите свой форматтер через documentFormattingEditProvider, '
         'уважайте editor.defaultFormatter'),
        ('Keybindings',
         'Два расширения регистрируют один и тот же Ctrl+Shift+F. '
         'VS Code всегда предупреждает. Решение: используйте редкие комбинации '
         'или не регистрируйте по умолчанию'),
        ('Language ID',
         'Два расширения объявляют один languageId. '
         'Последний установленный "выигрывает". '
         'Решение: используйте уникальные ID, не переопределяйте чужие'),
        ('Completion providers',
         'Несколько провайдеров дают дублирующиеся подсказки. '
         'VS Code объединяет их. Решение: возвращайте только уникальные items'),
        ('Diagnostics',
         'Несколько расширений диагностируют один файл, создавая дубликаты. '
         'Решение: называйте collection уникально, проверяйте дубликаты'),
        ('Status Bar',
         'Расширения занимают всю нижнюю полосу. '
         'Решение: ограничить 1–2 элементами, скрывать когда нерелевантно'),
    ]))
    add(sp(6))

    add(h2('Конфликты форматтеров — решение'))
    add(p('Самый частый конфликт в реальных проектах. Правильная реализация форматтера:'))
    add(sp(3))
    add(code([
        '// Регистрируем форматтер только для своего языка',
        'const formatter = vscode.languages.registerDocumentFormattingEditProvider(',
        '    { language: \'mylang\' },  // ← точный селектор, не "*"',
        '    {',
        '        provideDocumentFormattingEdits(',
        '            document: vscode.TextDocument,',
        '            options: vscode.FormattingOptions,',
        '            token: vscode.CancellationToken',
        '        ): vscode.TextEdit[] {',
        '            // Проверяем: является ли наш форматтер дефолтным',
        '            const cfg = vscode.workspace.getConfiguration(\'editor\', document);',
        '            const defaultFormatter = cfg.get<string>(\'defaultFormatter\');',
        '',
        '            // Если пользователь выбрал другой форматтер явно — уступаем',
        '            if (defaultFormatter && defaultFormatter !== \'publisher.myext\') {',
        '                return [];',
        '            }',
        '',
        '            return formatDocument(document, options);',
        '        }',
        '    }',
        ');',
    ]))
    add(sp(3))
    add(p('Корректная реализация форматтера: регистрация через <b>registerDocumentFormattingEditProvider</b> с точным языковым селектором (не «*»). Внутри провайдер проверяет <b>editor.defaultFormatter</b> — если пользователь явно выбрал другой форматтер, возвращает пустой массив и не вмешивается.'))

    add(sp(3))
    add(code([
        '// В README.md — подскажите пользователю настройку',
        '// To use My Extension as your default formatter, add to settings.json:',
        '// {',
        '//   "[mylang]": {',
        '//     "editor.defaultFormatter": "publisher.myext"',
        '//   }',
        '// }',
    ]))
    add(sp(3))
    add(p('Пример инструкции для README: как настроить ваше расширение в качестве форматтера по умолчанию через <b>editor.defaultFormatter</b> в settings.json с указанием языка.'))

    add(sp(6))

    add(h2('Конфликты горячих клавиш — стратегия'))
    add(p('VS Code предупреждает пользователя о конфликтах горячих клавиш. '
          'Правильные стратегии:'))
    add(sp(3))
    add(code([
        '// package.json — минимизация конфликтов горячих клавиш',
        '"contributes": {',
        '  "keybindings": [{',
        '    "command": "myExt.mainAction",',
        '    "key": "ctrl+alt+shift+m",  // редкая комбинация — меньше конфликтов',
        '    "mac": "cmd+alt+shift+m",',
        '    "when": "editorTextFocus && resourceLangId == mylang"  // контекст!',
        '  }]',
        '}',
        '',
        '// Или вообще не регистрировать по умолчанию',
        '// Документировать рекомендуемую комбинацию в README',
        '// Пользователь сам назначает удобную ему клавишу',
    ]))
    add(sp(3))
    add(p('Две стратегии минимизации конфликтов: либо использовать редкую комбинацию (<b>ctrl+alt+shift+...</b>) с <b>when</b>-условием для ограничения контекста, либо вообще не регистрировать keybinding по умолчанию — документировать рекомендуемую комбинацию и дать пользователю назначить самому.'))

    add(sp(4))
    add(box('Лучшая практика по keybindings',
        'Не регистрируйте горячие клавиши по умолчанию для второстепенных функций. '
        'В README опишите рекомендуемые комбинации. '
        'Пользователи сами назначают клавиши через keybindings.json — '
        'так конфликтов не будет вообще.', 'tip'))
    add(sp(6))

    add(h2('Объявление совместимости и зависимостей'))
    add(p('В package.json можно явно объявить зависимости и рекомендации:'))
    add(sp(3))
    add(code([
        '// package.json',
        '{',
        '  // Обязательные зависимости — устанавливаются автоматически',
        '  // Использовать только для ДЕЙСТВИТЕЛЬНО необходимых расширений',
        '  "extensionDependencies": [',
        '    "vscode.git"  // встроенное расширение',
        '  ],',
        '',
        '  // Extension Pack — устанавливает набор вместе',
        '  // НЕ должны иметь функциональных зависимостей друг от друга',
        '  "extensionPack": [',
        '    "publisher.extension1",',
        '    "publisher.extension2"',
        '  ]',
        '}',
        '',
        '// .vscode/extensions.json — рекомендации для проекта',
        '// VS Code показывает popup "Recommended extensions" при открытии проекта',
        '{',
        '  // recommendations: VS Code предложит установить эти расширения',
        '  "recommendations": ["publisher.myext"],',
        '',
        '  // unwantedRecommendations: подавить рекомендации конкурирующих расширений',
        '  // Если пользователь уже использует ваше расширение — VS Code не будет',
        '  // предлагать установить конфликтующее (например, два форматтера одного языка)',
        '  "unwantedRecommendations": ["publisher.conflicting-ext"]',
        '}',
    ]))
    add(sp(3))
    add(p('Три механизма управления зависимостями: <b>extensionDependencies</b> устанавливает обязательные расширения автоматически, <b>extensionPack</b> создаёт набор расширений для совместной установки, а <b>.vscode/extensions.json</b> на уровне проекта рекомендует нужные расширения и подавляет рекомендации конфликтующих через <b>unwantedRecommendations</b>.'))

    add(sp(3))
    add(box('Что такое unwantedRecommendations',
        '<b>unwantedRecommendations</b> — массив ID расширений, которые VS Code '
        'не будет предлагать установить в данном проекте. '
        'Полезно для монорепозиториев, где одно расширение заменяет другое '
        '(например, ваш форматтер вместо Prettier), или там, где известны '
        'конфликты. VS Code не установит их принудительно — только перестанет '
        'показывать recommendation-попап для перечисленных ID. '
        'Источник: code.visualstudio.com/docs/editor/extension-marketplace#_workspace-recommended-extensions',
        'note'))
    add(sp(4))

    add(h3('Обнаружение конфликтующих расширений в коде'))
    add(p('Если ваше расширение конфликтует с другим — обнаружьте это и сообщите пользователю вежливо:'))
    add(sp(3))
    add(code([
        'async function checkForConflicts(ctx: vscode.ExtensionContext) {',
        '    const CONFLICT_KEY = \'conflictWarningShown\';',
        '    if (ctx.globalState.get<boolean>(CONFLICT_KEY)) return;',
        '',
        '    // Список известных конфликтующих расширений',
        '    const conflicting = [',
        '        \'publisher.old-formatter\',',
        '        \'publisher.legacy-linter\',',
        '    ];',
        '',
        '    const found = conflicting.filter(id =>',
        '        vscode.extensions.getExtension(id)?.isActive',
        '    );',
        '',
        '    if (found.length === 0) return;',
        '',
        '    await ctx.globalState.update(CONFLICT_KEY, true);',
        '',
        '    const names = found.map(id => id.split(\'.\')[1]).join(\', \');',
        '    const action = await vscode.window.showWarningMessage(',
        '        `My Extension: обнаружено потенциально конфликтующее расширение: ${names}. ` +',
        '        \'Рекомендуется отключить его для корректной работы.\',',
        '        \'Узнать больше\',',
        '        \'Понятно\'',
        '    );',
        '',
        '    if (action === \'Узнать больше\') {',
        '        vscode.env.openExternal(vscode.Uri.parse(COMPAT_DOCS_URL));',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('Обнаружение конфликтующих расширений в рантайме: <b>vscode.extensions.getExtension()</b> проверяет наличие и активность известных конкурентов. Предупреждение показывается один раз (флаг в <b>globalState</b>) и предлагает узнать подробности — без агрессивного требования удалить чужое расширение.'))

    add(sp(6))

    add(h2('Document Selector — точность как профилактика конфликтов'))
    add(p('<b>Document Selector</b> — это фильтр, который определяет для каких документов '
          'активен ваш провайдер (hover, completion, formatting, diagnostics и т.д.). '
          'Это не опция — это обязательный первый аргумент при регистрации любого языкового провайдера. '
          'VS Code вызывает ваш провайдер <i>только</i> для документов, '
          'совпадающих с селектором. '
          'Справочник всех полей: <b>code.visualstudio.com/api/references/document-selector</b>'))
    add(sp(3))
    add(box('Document Selector — главный инструмент против конфликтов',
        'Когда два расширения регистрируют провайдер для <b>"*"</b> — они конкурируют '
        'за все документы в редакторе. Пользователь открывает .json и получает '
        'hover-подсказки от Python-расширения. Это реальная причина большинства '
        'конфликтов между расширениями. '
        'Точный selector {language: "typescript", scheme: "file"} означает: '
        '"мой провайдер работает только с .ts файлами на диске, и ни с чем другим". '
        'Это уважение к чужому пространству.', 'warn'))
    add(sp(3))
    add(p('Селектор может быть строкой (languageId), объектом или массивом объектов. '
          'Поля объекта: <b>language</b> (languageId), <b>scheme</b> (file/untitled/vscode-remote), '
          '<b>pattern</b> (glob), <b>notebookType</b>.'))
    add(sp(3))
    add(p('<b>Точность как профилактика конфликтов.</b> '
          'Чем точнее selector — тем меньше шансов наступить на чужое поле:'))
    add(sp(3))
    add(code([
        '// ПЛОХО: активно для всех файлов — перехватывает hover у других расширений',
        'vscode.languages.registerHoverProvider(\'*\', myProvider)',
        '',
        '// ПЛОХО: активно для всех файловых документов — включая .json, .md, .yaml',
        'vscode.languages.registerHoverProvider({ scheme: \'file\' }, myProvider)',
        '',
        '// OK: только .mylang файлы из файловой системы',
        'vscode.languages.registerHoverProvider(',
        '    { scheme: \'file\', language: \'mylang\' },',
        '    myProvider',
        '    // Аргумент 1: selector — ДЛЯ каких документов',
        '    // Аргумент 2: provider — что делать',
        ')',
        '',
        '// OK: включая untitled (новые несохранённые файлы)',
        '// Массив = объединение (OR): срабатывает если документ совпадает хотя бы с одним',
        'vscode.languages.registerHoverProvider(',
        '    [',
        '        { scheme: \'file\',     language: \'mylang\' },',
        '        { scheme: \'untitled\', language: \'mylang\' },',
        '    ],',
        '    myProvider',
        ')',
        '',
        '// OK: исключаем Notebook-ячейки (notebookType: undefined = обычные файлы)',
        'vscode.languages.registerCompletionItemProvider(',
        '    { scheme: \'file\', language: \'typescript\', notebookType: undefined },',
        '    completionProvider',
        ')',
    ]))
    add(sp(3))
    add(p('Эволюция точности Document Selector: от «*» (все файлы — конфликт гарантирован) до точных комбинаций <b>scheme + language</b>. Массив селекторов работает как OR — можно включить и файловые, и untitled-документы. Поле <b>notebookType: undefined</b> исключает ячейки Jupyter-ноутбуков.'))

    add(sp(6))

    # ── 4. ПРОГРЕССИВНОЕ РАСКРЫТИЕ ─────────────────────────────────────────────
    add(h1('Прогрессивное раскрытие и многоуровневый UX'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Три уровня доступа к функциям'))
    add(p('Хорошее расширение имеет три уровня доступа к своим возможностям:'))
    add(sp(3))
    add(tblh(['Уровень', 'Что здесь живёт']))
    add(tbl2([
        ('1. Всегда видимое',
         'Один элемент Status Bar или минимальный набор. '
         'Только то, что нужно постоянно. Пример: текущая версия Python в строке состояния'),
        ('2. В контексте',
         'Кнопки в Editor Toolbar, пункты контекстного меню. '
         'Появляются только для релевантных файлов. '
         'Пример: кнопка "Run" для .py файлов'),
        ('3. По запросу',
         'Command Palette, Tree View, Webview. '
         'Пользователь сам инициирует. '
         'Пример: "Python: Select Interpreter" в Command Palette'),
    ]))
    add(sp(4))
    add(box('Правило пирамиды',
        'Большинство функций должны жить на уровне 3 (по запросу). '
        'Уровень 2 — для частых контекстных действий. '
        'Уровень 1 — только для постоянно актуальной информации. '
        'Чем ниже уровень — тем меньше элементов.', 'note'))
    add(sp(6))

    add(h2('Настройки: давайте пользователю контроль'))
    add(p('Каждая заметная функция расширения должна быть отключаемой. '
          'Это золотое правило из исходников GitLens, Pylance и Prettier:'))
    add(sp(3))
    add(code([
        '// package.json — полный контроль над видимостью',
        '"contributes": {',
        '  "configuration": {',
        '    "properties": {',
        '      "myExt.showStatusBarItem": {',
        '        "type": "boolean",',
        '        "default": true,',
        '        "description": "Показывать элемент в строке состояния"',
        '      },',
        '      "myExt.showInlineDecorations": {',
        '        "type": "boolean",',
        '        "default": true,',
        '        "description": "Показывать инлайн аннотации в редакторе"',
        '      },',
        '      "myExt.showActivityBarIcon": {',
        '        "type": "boolean",',
        '        "default": false,  // ← ВЫКЛЮЧЕНО по умолчанию!',
        '        "description": "Показывать иконку в Activity Bar"',
        '      },',
        '      "myExt.enableOnSave": {',
        '        "type": "boolean",',
        '        "default": true,',
        '        "description": "Запускать автоматически при сохранении файла"',
        '      }',
        '    }',
        '  }',
        '}',
        '',
        '// В коде — читаем настройки',
        'function getConfig() {',
        '    const cfg = vscode.workspace.getConfiguration(\'myExt\');',
        '    return {',
        '        showStatusBar: cfg.get<boolean>(\'showStatusBarItem\', true),',
        '        showDecorations: cfg.get<boolean>(\'showInlineDecorations\', true),',
        '    };',
        '}',
    ]))
    add(sp(3))
    add(p('Объявление настроек видимости в <b>package.json</b> и чтение их в коде. Каждый UI-элемент (Status Bar, инлайн-аннотации, Activity Bar иконка) управляется отдельным булевым флагом. Обратите внимание: <b>showActivityBarIcon</b> выключен по умолчанию — Activity Bar иконка появляется только по запросу пользователя.'))

    add(sp(6))

    add(h2('Progress API: ненавязчивый прогресс'))
    add(p('Для долгих операций используйте правильное место для прогресса:'))
    add(sp(3))
    add(tblh(['Вид прогресса', 'Когда использовать']))
    add(tbl2([
        ('ProgressLocation.SourceControl', 'Операции SCM (git операции)'),
        ('ProgressLocation.Window',        'Глобальные фоновые операции в Status Bar — минимально навязчивый'),
        ('ProgressLocation.Notification',  'Долгие операции требующие внимания; с кнопкой отмены'),
    ]))
    add(sp(3))
    add(code([
        '// OK: Фоновая операция — Window (Status Bar) вместо Notification',
        'await vscode.window.withProgress(',
        '    {',
        '        location: vscode.ProgressLocation.Window,',
        '        title: \'$(sync~spin) Индексирую...\',',
        '    },',
        '    async () => {',
        '        await buildIndex();',
        '    }',
        ');',
        '',
        '// OK: Долгая операция с отменой — Notification',
        'await vscode.window.withProgress(',
        '    {',
        '        location: vscode.ProgressLocation.Notification,',
        '        title: \'Анализ проекта\',',
        '        cancellable: true,',
        '    },',
        '    async (progress, token) => {',
        '        const files = await getFiles();',
        '        for (let i = 0; i < files.length; i++) {',
        '            if (token.isCancellationRequested) break;',
        '            progress.report({',
        '                increment: 100 / files.length,',
        '                message: `${i + 1} / ${files.length}: ${files[i]}`',
        '            });',
        '            await analyzeFile(files[i]);',
        '        }',
        '    }',
        ');',
    ]))
    add(sp(3))
    add(p('<b>window.withProgress()</b> показывает индикатор прогресса без блокировки UI. <b>ProgressLocation.Notification</b> — уведомление с баром; <b>ProgressLocation.Window</b> — тихий индикатор в Status Bar. <b>cancellable: true</b> добавляет кнопку Cancel и CancellationToken в callback.'))
    add(sp(6))

    # ── 5. UI ЭЛЕМЕНТЫ ──────────────────────────────────────────────────────────
    add(h1('Каждый UI-элемент: правила и антипаттерны'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Activity Bar — строгие правила'))
    add(p('Activity Bar — самое "дорогое" место. Официальные правила Microsoft:'))
    add(sp(2))
    for good in [
        'Добавляйте иконку только если расширение предоставляет набор постоянно доступных View',
        'Иконка: SVG 16×16 или 24×24, монохромная (один цвет) — VS Code сам применяет цвет темы',
        'Скрывайте Activity Bar иконку если расширение неактивно (нет файлов нужного типа)',
        'Делайте иконку отключаемой через настройку',
    ]:
        add(bul(f'<b>✓</b> {good}'))
    for bad in [
        'Не добавляйте иконку для расширения с одной-двумя командами',
        'Не используйте многоцветные иконки — они выбиваются из дизайна VS Code',
        'Не показывайте пустой View без Welcome Content',
    ]:
        add(bul(f'<b>✗</b> {bad}', 2))
    add(sp(3))
    add(box('Почему SVG и почему монохромная?',
        'VS Code Activity Bar раскрашивает иконки динамически: неактивные — приглушённым цветом, '
        'активные — акцентным (обычно белым или цветом темы). '
        'Это работает только если иконка монохромная (fill="currentColor" в SVG). '
        'Если использовать многоцветный PNG — цветовая динамика сломается, иконка будет выглядеть чужеродно. '
        'SVG также масштабируется на HiDPI-экранах без пикселизации. '
        'Кастомный SVG: в поле "icon" укажите путь к файлу — '
        '"viewsContainers": { "activitybar": [{ "icon": "./icons/my-icon.svg" }] }.',
        'note'))
    add(sp(6))

    add(h2('Status Bar — правила и приоритеты'))
    add(p('Status Bar имеет систему приоритетов. Чем выше число — тем левее элемент (для левой стороны):'))
    add(sp(3))
    add(code([
        '// Встроенные VS Code приоритеты (для ориентира):',
        '// Python: 100 (язык + интерпретатор)',
        '// GitLens: 50-70 (ветка, blame)',
        '// ESLint: 1 (статус)',
        '',
        '// Рекомендация: используйте приоритеты 0-20 для одиночных элементов',
        'const item = vscode.window.createStatusBarItem(',
        '    vscode.StatusBarAlignment.Right,',
        '    10  // приоритет',
        ');',
        '',
        '// Status Bar цвета — используйте ThemeColor, не hex',
        '// ThemeColor автоматически меняется при смене темы пользователем',
        '// Полный справочник токенов: code.visualstudio.com/api/references/theme-color',
        'item.color = new vscode.ThemeColor(\'statusBar.foreground\');',
        '',
        '// Для ошибок/предупреждений (только для Status Bar Item)',
        'item.backgroundColor = new vscode.ThemeColor(\'statusBarItem.errorBackground\');',
        '// или',
        'item.backgroundColor = new vscode.ThemeColor(\'statusBarItem.warningBackground\');',
        '',
        '// Короткий текст + иконка: лучший формат',
        'item.text = \'$(check) 0 ошибок\';     // OK:',
        '// item.text = \'My Extension Active\'; // ПЛОХО: слишком длинно',
    ]))
    add(sp(3))
    add(p('Создание Status Bar элемента с приоритетом и стилизацией. Приоритет (число при создании) определяет позицию: для одиночных расширений рекомендуется 0–20. Цвета задаются через <b>ThemeColor</b> — они автоматически подстраиваются под тему. Для индикации ошибок — специальные токены <b>statusBarItem.errorBackground</b> и <b>warningBackground</b>.'))

    add(sp(6))

    add(h2('Editor Toolbar — иконки в заголовке вкладки'))
    add(screenshot('editor-toolbar.png', 'Editor Toolbar: контекстное меню вкладки с командами расширений'))
    add(sp(3))
    add(p('<b>Editor Toolbar</b> — это строка иконок-кнопок в <b>правой части заголовка активной вкладки</b> '
          'редактора (не путать с Activity Bar слева и Title Bar вверху окна). '
          'По умолчанию там находятся стандартные кнопки VS Code: '
          'Split Editor (разделить редактор), Open Changes (показать diff), '
          'More Actions (...). '
          'Расширения добавляют свои кнопки туда через <b>"editor/title"</b> в секции menus '
          'файла package.json. '
          '<b>Для чего использовать:</b> основное действие с текущим файлом — запустить код, '
          'открыть превью, опубликовать, отформатировать. Это "главная кнопка" для вашего языка. '
          'Примеры из реальных расширений: кнопка Run в Python-расширении, '
          'кнопка Preview в Markdown-расширении, кнопка Test в тест-раннерах.'))
    add(sp(3))
    add(box('Editor Toolbar vs Status Bar',
        'Editor Toolbar — для действий с конкретным файлом (контекстно). '
        'Status Bar — для информации о всей среде (глобально). '
        'Кнопка "Run Python File" → Editor Toolbar. '
        'Индикатор "Python 3.11" → Status Bar.', 'tip'))
    add(sp(3))
    add(code([
        '// package.json — кнопка появляется только для Go-файлов в заголовке вкладки',
        '"contributes": {',
        '  "menus": {',
        '    "editor/title": [{',
        '      "command": "myGoExt.runFile",',
        '      // when: условие — иначе кнопка видна для ВСЕХ файлов',
        '      "when": "resourceLangId == go && !isInDiffEditor",',
        '      "group": "navigation"  // navigation = иконка видна сразу; 1_run = в меню ...',
        '    }]',
        '  },',
        '  "commands": [{',
        '    "command": "myGoExt.runFile",',
        '    "title": "Run Go File",',
        '    "icon": "$(play)"  // иконка обязательна для editor/title',
        '  }]',
        '}',
        '"contributes": {',
        '  "menus": {',
        '    "editor/title": [{',
        '      "command": "myExt.runCurrentFile",',
        '      // Только для своего языка И только когда не diff editor',
        '      "when": "resourceLangId == mylang && !isInDiffEditor",',
        '      "group": "navigation"',
        '    }]',
        '  }',
        '}',
        '',
        '// Иконки: используйте встроенные Codicons',
        '"contributes": {',
        '  "commands": [{',
        '    "command": "myExt.runCurrentFile",',
        '    "title": "Run File",',
        '    "icon": "$(play)"  // $(play), $(debug), $(sync), $(check)...',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Регистрация кнопки в Editor Toolbar через <b>editor/title</b> в секции menus. Ключевые моменты: условие <b>when</b> ограничивает показ кнопки конкретным языком, <b>group: "navigation"</b> делает иконку видимой сразу (а не спрятанной в меню «...»), а <b>icon: "$(play)"</b> в объявлении команды задаёт иконку через Codicon.'))

    add(sp(4))
    add(box('Codicons — встроенные иконки VS Code',
        'VS Code содержит более 600 встроенных иконок (Codicons). '
        'Используйте $(icon-name) вместо собственных SVG — они автоматически '
        'адаптируются к теме. Полный список: code.visualstudio.com/api/references/icons-in-labels', 'tip'))
    add(sp(6))

    add(h2('Context Menu — иерархия групп'))
    add(p('Контекстные меню имеют систему групп (group). '
          'Порядок элементов внутри группы управляется через @N:'))
    add(sp(3))
    add(code([
        '// Стандартные группы редактора (в порядке отображения):',
        '// navigation   — переход к определению, ссылкам',
        '// 1_modification — вставка, форматирование',
        '// 9_cutcopypaste — вырезать, копировать, вставить',
        '// z_commands    — разные команды',
        '',
        '"editor/context": [{',
        '  "command": "myExt.extractFunction",',
        '  "when": "editorHasSelection && resourceLangId == typescript",',
        '  "group": "1_modification@5"  // внутри группы — позиция @5',
        '}]',
        '',
        '// Разделитель между группами создаётся автоматически',
        '// Ваши команды в одной группе не разделяются с другими',
        '',
        '// Группы Explorer контекстного меню:',
        '// navigation  — открыть, перейти',
        '// 2_workspace — добавить в workspace',
        '// 3_compare   — сравнить',
        '// 5_cutcopypaste',
        '// 7_modification — создать, переименовать, удалить',
    ]))
    add(sp(3))
    add(p('Система групп контекстного меню: <b>group</b> определяет секцию (navigation, 1_modification и т.д.), а суффикс <b>@N</b> — позицию внутри секции. VS Code автоматически добавляет разделители между группами. У редактора и Explorer свои наборы стандартных групп — важно размещать команды в правильную секцию.'))

    add(sp(6))

    # ── 6. WEBVIEW UX ──────────────────────────────────────────────────────────
    add(h1('Webview: CSS-токены и интеграция в экосистему'))
    add(hl(C['blue']))
    add(sp(6))

    add(p('Эта тема подробно разобрана в Главе 7 (Webview API) и Справочнике D '
          '(CSS-переменные тем). Здесь — только UX-принципы.'))
    add(sp(3))

    add(h2('Webview должен "чувствоваться" как VS Code'))
    add(p('Главная ошибка Webview-расширений — они выглядят как сторонний сайт внутри VS Code. '
          'Используйте CSS-переменные темы чтобы Webview автоматически адаптировался '
          'к любой теме пользователя (Dark, Light, High Contrast, кастомная). '
          'Полный список переменных — <a href="#appendix_D"><b>Справочник D</b></a> в конце книги.'))
    add(sp(3))
    add(code([
        '/* Минимальный Webview CSS — body использует цвета темы VS Code */',
        'body {',
        '    background-color: var(--vscode-editor-background);',
        '    color: var(--vscode-editor-foreground);',
        '    font-family: var(--vscode-font-family);',
        '    font-size: var(--vscode-font-size);',
        '    /* Webview добавляет класс vscode-dark / vscode-light на body */',
        '}',
        '',
        'button {',
        '    background-color: var(--vscode-button-background);',
        '    color: var(--vscode-button-foreground);',
        '    border: 1px solid var(--vscode-button-border, transparent);',
        '}',
        'button:hover { background-color: var(--vscode-button-hoverBackground); }',
        '',
        'input, select {',
        '    background-color: var(--vscode-input-background);',
        '    color: var(--vscode-input-foreground);',
        '    border: 1px solid var(--vscode-input-border);',
        '}',
        '',
        'a { color: var(--vscode-textLink-foreground); }',
        'code, pre {',
        '    background-color: var(--vscode-textCodeBlock-background);',
        '    font-family: var(--vscode-editor-font-family);',
        '}',
    ]))
    add(sp(3))
    add(p('CSS-переменные <b>--vscode-*</b> автоматически обновляются при смене темы. Используйте их вместо жёстких hex-цветов — иначе Webview сломается в светлой, High Contrast или кастомной теме. VS Code добавляет класс <b>vscode-dark</b>/<b>vscode-light</b> на <body>.'))
    add(sp(3))
    add(p('<b>Почему var() а не жёсткие цвета:</b> VS Code имеет Light, Dark, '
          'High Contrast темы и тысячи пользовательских тем. '
          'CSS-переменные обновляются мгновенно при смене темы без перезагрузки Webview. '
          'На vscode.dev темы меняются динамически — без var() это сломается.'))
    add(sp(4))
    add(sp(4))

    add(h3('Поддержка смены темы в реальном времени'))
    add(code([
        '// В Webview JavaScript — реагируем на смену темы',
        'const vscode = acquireVsCodeApi();',
        '',
        '// Слушаем смену темы',
        'window.addEventListener(\'message\', event => {',
        '    const { command, theme } = event.data;',
        '    if (command === \'themeChanged\') {',
        '        document.body.className = `vscode-${theme}`;',
        '        updateCharts(); // перерисовываем графики',
        '    }',
        '});',
        '',
        '// В расширении — уведомляем Webview о смене темы',
        'vscode.window.onDidChangeActiveColorTheme(theme => {',
        '    panel.webview.postMessage({',
        '        command: \'themeChanged\',',
        '        theme: theme.kind === vscode.ColorThemeKind.Dark ? \'dark\' : \'light\'',
        '    });',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('Двусторонняя обработка смены темы: на стороне расширения <b>onDidChangeActiveColorTheme</b> отслеживает переключение и отправляет сообщение в Webview через <b>postMessage</b>, а JavaScript внутри Webview слушает событие message и обновляет CSS-класс на body — это нужно для элементов, которые не обновляются автоматически через CSS-переменные (например, canvas-графики).'))

    add(sp(6))

    add(h2('Сохранение состояния Webview'))
    add(p('Webview скрывается при переключении вкладок и может уничтожаться для экономии памяти. '
          'Обязательно сохраняйте состояние:'))
    add(sp(3))
    add(code([
        '// В Webview JavaScript',
        'const vscode = acquireVsCodeApi();',
        '',
        '// Восстанавливаем сохранённое состояние',
        'const prevState = vscode.getState() || { scrollY: 0, selectedTab: 0 };',
        'window.scrollTo(0, prevState.scrollY);',
        'selectTab(prevState.selectedTab);',
        '',
        '// Сохраняем при каждом изменении',
        'function saveState() {',
        '    vscode.setState({',
        '        scrollY: window.scrollY,',
        '        selectedTab: activeTabIndex,',
        '    });',
        '}',
        '',
        '// В расширении — включаем сохранение',
        'vscode.window.createWebviewPanel(\'myView\', \'My View\', col, {',
        '    retainContextWhenHidden: true,  // НЕ уничтожать при скрытии',
        '    // Но это дорого по памяти! Используйте только если нужно.',
        '});',
    ]))
    add(sp(3))
    add(p('Два подхода к сохранению состояния Webview. Лёгкий: <b>vscode.getState()</b> / <b>setState()</b> сериализуют данные (скролл, выбранная вкладка) и восстанавливают при повторном показе. Тяжёлый: <b>retainContextWhenHidden</b> сохраняет весь DOM и JavaScript-контекст — удобно, но Webview потребляет память даже когда скрыт.'))

    add(sp(4))
    add(box('retainContextWhenHidden — дорогая опция',
        'retainContextWhenHidden сохраняет DOM и JS-состояние при скрытии Webview. '
        'Это удобно, но расходует память — Webview занимает ресурсы даже когда невидим. '
        'Используйте только для тяжёлых редакторов. '
        'Для простых случаев — vscode.setState()/getState() достаточно.', 'warn'))
    add(sp(6))

    # ── 7. НАСТРОЙКИ ──────────────────────────────────────────────────────────
    add(h1('Настройки: удобство и документация'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Анатомия хорошего раздела настроек'))
    add(p('Настройки — главный способ коммуникации с пользователем. '
          'Хорошие настройки объясняют, что делает расширение, и дают полный контроль:'))
    add(sp(3))
    add(code([
        '"contributes": {',
        '  "configuration": {',
        '    "title": "My Extension",  // Отображается как заголовок секции',
        '    "order": 10,              // Порядок в Settings UI (меньше = выше)',
        '    "properties": {',
        '',
        '      // Каждая настройка с полным описанием',
        '      "myExt.enable": {',
        '        "type": "boolean",',
        '        "default": true,',
        '        "markdownDescription":',
        '          "Включить My Extension. Отключите если наблюдаете проблемы с производительностью.",',
        '        "order": 1  // Порядок внутри секции',
        '      },',
        '',
        '      // Enum с описаниями каждого значения',
        '      "myExt.verbosity": {',
        '        "type": "string",',
        '        "enum": ["silent", "normal", "verbose"],',
        '        "enumDescriptions": [',
        '          "Без вывода в Output Channel",',
        '          "Только важные сообщения (рекомендуется)",',
        '          "Все сообщения (для отладки)"',
        '        ],',
        '        "default": "normal",',
        '        "description": "Уровень логирования",',
        '        "order": 2',
        '      },',
        '',
        '      // Настройка с примером в описании',
        '      "myExt.excludePatterns": {',
        '        "type": "array",',
        '        "items": { "type": "string" },',
        '        "default": ["**/node_modules/**", "**/.git/**"],',
        '        "markdownDescription":',
        '          "Glob-паттерны файлов которые **не** обрабатываются.\\n\\n" +',
        '          "Пример: `[\\\"**/test/**\\\", \\\"**/*.spec.ts\\\"]`",',
        '        "order": 3',
        '      },',
        '',
        '      // Настройка с предупреждением о перезагрузке',
        '      "myExt.serverPort": {',
        '        "type": "number",',
        '        "default": 9000,',
        '        "description": "Порт LSP сервера. Требует перезагрузки окна.",',
        '        "scope": "window"  // machine | window | resource | language-overridable',
        '      }',
        '    }',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Полная анатомия секции настроек: <b>title</b> и <b>order</b> управляют отображением в Settings UI. Каждое свойство имеет <b>type</b>, <b>default</b> и описание. Для enum-значений <b>enumDescriptions</b> поясняет каждый вариант. Поле <b>markdownDescription</b> поддерживает форматирование и примеры. Атрибут <b>scope</b> определяет уровень применения настройки (machine, window, resource).'))

    add(sp(4))

    add(h3('Scope настроек'))
    add(tblh(['Scope', 'Описание']))
    add(tbl2([
        ('machine',               'Привязана к машине. Не синхронизируется между устройствами. Для путей к бинарникам'),
        ('window',                'На уровне окна VS Code. По умолчанию для большинства настроек'),
        ('resource',              'На уровне файла. Разные значения для разных файлов'),
        ('language-overridable',  'Можно переопределить для языка: "[typescript]": {...}'),
    ]))
    add(sp(6))

    add(h2('Workspace-level настройки'))
    add(p('Позвольте пользователям задавать настройки на уровне проекта. '
          'Это критически важно для команд с разными конфигурациями:'))
    add(sp(3))
    add(code([
        '// Читаем настройки с учётом контекста документа',
        'function getEffectiveConfig(document: vscode.TextDocument) {',
        '    // getConfiguration с uri учитывает workspace-specific настройки',
        '    const cfg = vscode.workspace.getConfiguration(\'myExt\', document.uri);',
        '    return {',
        '        enable: cfg.get<boolean>(\'enable\', true),',
        '        verbosity: cfg.get<string>(\'verbosity\', \'normal\'),',
        '    };',
        '}',
        '',
        '// Пользователь может переопределить в .vscode/settings.json проекта:',
        '// {',
        '//   "myExt.verbosity": "verbose",  // только для этого проекта',
        '//   "[typescript]": {',
        '//     "myExt.enable": false  // только для TypeScript файлов',
        '//   }',
        '// }',
    ]))
    add(sp(3))
    add(p('Чтение настроек с учётом контекста документа: <b>getConfiguration(section, uri)</b> с указанием URI возвращает значения с учётом workspace-specific переопределений из <b>.vscode/settings.json</b>. Это позволяет пользователю задать разные настройки для разных проектов и даже для разных языков через секции <b>[typescript]</b>.'))

    add(sp(6))

    # ── РЕАЛЬНЫЕ ПРИМЕРЫ ────────────────────────────────────────────────────────
    add(h1('Реальные примеры: хорошо и плохо'))
    add(hl(C['blue']))
    add(sp(4))

    add(h2('Образцы качества'))
    add(p('Эти расширения часто называют эталонами — не только по функциональности, '
          'но именно по качеству UX и соблюдению принципов VS Code:'))
    add(sp(3))
    add(tblh(['Расширение', 'Что в нём правильно']))
    add(tbl2([
        ('GitLens\n(gitkraken/vscode-gitlens)',
         'Три уровня видимости: inline blame (всегда), Status Bar (контекст), '
         'боковая панель (по запросу). Всё отключаемо через настройки. '
         'Walkthrough при первом запуске вместо уведомлений. '
         'Время активации ~35ms несмотря на огромный функционал'),
        ('Prettier\n(prettier/prettier-vscode)',
         'Форматтер не навязывается — активируется только если выбран как '
         'editor.defaultFormatter. Не показывает уведомлений при активации. '
         'Все ошибки идут в Output Channel, не во всплывашки'),
        ('ESLint\n(microsoft/vscode-eslint)',
         'Диагностика только для файлов с .eslintrc в проекте. '
         'Status Bar элемент показывает состояние и исчезает когда не нужен. '
         'Правильно использует CancellationToken во всех провайдерах'),
        ('rust-analyzer',
         'Тяжёлый LSP-сервер (компилятор Rust) вынесен в отдельный процесс. '
         'Progress в Status Bar при индексировании — не блокирует редактор. '
         'Время отклика на набор текста остаётся <16ms'),
    ]))
    add(sp(6))

    add(h2('Антипримеры и типичные ошибки'))
    add(p('Конкретные паттерны, которые регулярно вызывают жалобы в отзывах на Marketplace:'))
    add(sp(3))
    add(tblh(['Проблема', 'Чем заканчивается']))
    add(tbl2([
        ('activationEvents: ["*"] у не-языкового расширения',
         'Расширение грузится при каждом запуске VS Code. '
         'У пользователей с 20+ расширениями это сотни ms к старту. '
         'Пример: Beautify (5.4M установок) активировался со "*" — '
         'многие пользователи перешли на Prettier именно из-за этого'),
        ('2513ms время активации (реальный случай)',
         'Расширение с activationEvents:["*"] и временем активации 2.5 секунды. '
         'Это было задокументировано в публичном анализе производительности расширений. '
         'Такие расширения получают 1-звёздочные отзывы: "VS Code стал медленным"'),
        ('Уведомление при каждом запуске VS Code',
         '"Please rate this extension!" при каждом старте. '
         'Реальный пример: расширение с 4.7M установок упало с 4.2 до 3.1 звезды '
         'за 3 месяца из-за навязчивых уведомлений. После их удаления — вернулось к 4.4'),
        ('Сбор данных без явного согласия',
         'В 2025 году Microsoft удалила несколько популярных расширений из Marketplace '
         'за сбор пользовательских данных без явного согласия. '
         'Расширения использовались миллионами разработчиков и были удалены без предупреждения. '
         'Всегда уважайте isTelemetryEnabled и запрашивайте явное разрешение'),
        ('Глобальный State для workspace-специфичных данных',
         'Расширение сохраняет настройки проекта в globalState, а не workspaceState. '
         'Конфигурация одного проекта "протекает" в другой. '
         'Пользователи не могут понять почему расширение ведёт себя странно'),
    ]))
    add(sp(4))
    add(box('Как проверить своё расширение',
        'Developer: Show Running Extensions — время активации каждого расширения. '
        'Цель: < 100ms — отлично, < 300ms — хорошо, > 500ms — надо оптимизировать. '
        'Developer: Startup Performance — детальный профиль запуска VS Code. '
        'Источник: nicoespeon.com/en/2019/11/fix-vscode-extension-performance-issue/',
        'tip'))
    add(sp(6))

    # ── 8. ФИНАЛЬНЫЕ ПРИНЦИПЫ ──────────────────────────────────────────────────
    add(h1('Проверочный список: расширение как хороший гражданин'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Принципы ненавязчивого расширения'))
    add(p('Перед публикацией проверьте каждый пункт этого списка:'))
    add(sp(3))

    add(h3('Видимость и обнаруживаемость'))
    for item in [
        'Walkthrough для onboarding — вместо уведомления при первом запуске',
        'Welcome View для пустых состояний Tree View со ссылками на документацию',
        'Команды именованы с категорией: "My Extension: ..."',
        'Ключевые функции доступны из Command Palette',
        'Контекстные кнопки скрыты через "when" для нерелевантных файлов',
        'Status Bar элемент скрывается hide() для неактивных файлов',
        'Contextual hints (в нужный момент, не при старте)',
    ]:
        add(bul(item))
    add(sp(4))

    add(h3('Ненавязчивость'))
    for item in [
        'Нет уведомлений при активации расширения',
        'Нет автоматических уведомлений без явного действия пользователя',
        'Все повторяющиеся уведомления имеют "Больше не показывать"',
        'Все функции отключаемы через настройки',
        'Activity Bar иконка: по умолчанию выключена OR добавляется только если реально нужна',
        'Максимум 1–2 элемента Status Bar',
    ]:
        add(bul(item))
    add(sp(4))

    add(h3('Сосуществование с другими расширениями'))
    for item in [
        'Document Selector точный: конкретный язык, не "*"',
        'Keybindings: редкие комбинации с "when" контекстом',
        'Форматтер уважает editor.defaultFormatter',
        'Проверяется наличие конфликтующих расширений (при необходимости)',
        'Diagnostics collection именована уникально',
        'extensionDependencies объявлены в package.json',
        'Не переопределяет чужие Language ID',
    ]:
        add(bul(item))
    add(sp(4))

    add(h3('Качество UI'))
    for item in [
        'Webview использует переменные CSS темы VS Code',
        'Webview сохраняет состояние через vscode.setState()',
        'Иконки — встроенные Codicons ($(icon-name))',
        'Монохромные SVG иконки для Activity Bar',
        'Настройки имеют описания и примеры',
        'Scope настроек выбран корректно (machine/window/resource)',
        'Поддержка смены темы в Webview',
    ]:
        add(bul(item))

    return A


if __name__ == '__main__':
    print(f'UX part has {len(build_story_ux())} elements')
