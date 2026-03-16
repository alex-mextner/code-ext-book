from book_helpers import *

def build_story_part2():
    A = []
    def add(*x):
        for i in x: A.append(i)
    def ch(num, title, sub=''):
        part = f'Глава {num}' if str(num).replace('.','').isdigit() else str(num)
        label = f'{part}: {title}' if str(num).replace('.','').isdigit() else title
        add(StableAnchor(f'chapter_{num}'))
        add(toc_ch(label), banner(part, title, sub), sp(12))

    # ── ГЛАВА 10 ───────────────────────────────────────────────────────────────
    ch('10', 'Language Server Protocol', 'LSP — стандарт для языковой поддержки')

    add(h2('Зачем нужен LSP?'))
    add(p('При прямом использовании vscode.languages.* API возникают три проблемы:'))
    add(sp(2))
    for item in [
        '<b>Производительность:</b> анализ кода (AST, статика) ресурсоёмок. В Extension Host — замедляет редактор',
        '<b>Языки реализации:</b> Language Server часто пишут на том же языке что и сам язык. Интегрировать в Node.js сложно',
        '<b>M×N проблема:</b> M языков × N редакторов = M×N реализаций. LSP: один сервер — работает везде',
    ]:
        add(bul(item))
    add(sp(4))
    add(p('Language Server Protocol (LSP), разработанный Microsoft, стандартизирует коммуникацию между редактором и языковым сервером по JSON-RPC. Любой LSP-совместимый сервер работает в любом LSP-редакторе.'))
    add(sp(3))
    add(p('Для вас как разработчика расширений LSP актуален в двух сценариях. <b>Первый</b>: при установке расширений для Go, Rust, Python, C++ — Language Server приходит вместе с расширением и обеспечивает автодополнение, навигацию и диагностику. Понимание LSP помогает отлаживать проблемы и настраивать серверы. <b>Второй</b>: если в вашей компании есть кастомный DSL, конфигурационный язык или внутренний формат — создание собственного Language Server (или хотя бы TextMate-грамматики для цветовой разметки) превращает VS Code в полноценную IDE для этого языка. Один сервер работает во всех редакторах: VS Code, Neovim, Emacs, Sublime.'))
    from book_new import lsp_diagram_inject, q_cancellation
    for _el in lsp_diagram_inject(): add(_el)
    add(sp(6))

    add(h2('Структура LSP-расширения'))
    add(tblh(['Часть', 'Описание']))
    add(tbl2([
        ('Language Client',
         'Обычное расширение VS Code на TypeScript. Запускает Language Server, '
         'проксирует запросы. Библиотека: vscode-languageclient'),
        ('Language Server',
         'Независимый процесс, реализующий языковую логику. '
         'Может быть на любом языке. Библиотека (Node.js): vscode-languageserver'),
    ]))
    add(sp(3))
    from book_ui_diagrams import lsp_tree
    add(lsp_tree())
    add(sp(3))
    add(p('Типичная структура LSP-расширения: два независимых модуля. <b>client/</b> содержит Language Client — обычное VS Code расширение, которое запускает серверный процесс и проксирует к нему запросы. <b>server/</b> — Language Server, реализующий языковую логику. Общий <b>package.json</b> описывает оба модуля как единое расширение.'))

    add(sp(6))

    add(h2('Language Client'))
    add(code([
        'import * as path from \'path\';',
        'import * as vscode from \'vscode\';',
        'import {',
        '    LanguageClient, LanguageClientOptions,',
        '    ServerOptions, TransportKind',
        '} from \'vscode-languageclient/node\';',
        '',
        'let client: LanguageClient;',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    const serverModule = context.asAbsolutePath(',
        '        path.join(\'server\', \'out\', \'server.js\')',
        '    );',
        '',
        '    const serverOptions: ServerOptions = {',
        '        run:   { module: serverModule, transport: TransportKind.ipc },',
        '        debug: { module: serverModule, transport: TransportKind.ipc,',
        '            options: { execArgv: [\'--inspect=6009\'] }',
        '        }',
        '    };',
        '',
        '    const clientOptions: LanguageClientOptions = {',
        '        documentSelector: [{ scheme: \'file\', language: \'mylang\' }],',
        '        synchronize: {',
        '            configurationSection: \'myLangServer\',',
        '            fileEvents: vscode.workspace.createFileSystemWatcher(\'**/*.mylang\')',
        '        }',
        '    };',
        '',
        '    client = new LanguageClient(',
        '        \'myLangServer\', \'My Language Server\',',
        '        serverOptions, clientOptions',
        '    );',
        '    client.start();',
        '}',
        '',
        'export function deactivate(): Thenable<void> | undefined {',
        '    return client?.stop();',
        '}',
    ]))
    add(sp(3))
    add(p('Полный жизненный цикл Language Client. <b>ServerOptions</b> описывает запуск серверного процесса: путь к модулю и транспорт (<b>TransportKind.ipc</b> — межпроцессное взаимодействие, быстрее чем stdio). <b>ClientOptions</b> задаёт фильтр документов и синхронизацию настроек. В <b>deactivate()</b> клиент корректно останавливает серверный процесс через <b>client.stop()</b>.'))

    add(sp(6))

    add(h2('Language Server'))
    add(code([
        'import {',
        '    createConnection, TextDocuments, Diagnostic,',
        '    DiagnosticSeverity, ProposedFeatures,',
        '    CompletionItem, CompletionItemKind,',
        '    TextDocumentSyncKind, InitializeResult',
        '} from \'vscode-languageserver/node\';',
        'import { TextDocument } from \'vscode-languageserver-textdocument\';',
        '',
        'const connection = createConnection(ProposedFeatures.all);',
        'const documents  = new TextDocuments(TextDocument);',
        '',
        'connection.onInitialize((): InitializeResult => ({',
        '    capabilities: {',
        '        textDocumentSync: TextDocumentSyncKind.Incremental,',
        '        completionProvider: { resolveProvider: true },',
        '        hoverProvider: true,',
        '        definitionProvider: true,',
        '        referencesProvider: true,',
        '    }',
        '}));',
        '',
        'documents.onDidChangeContent(({ document }) => validate(document));',
        '',
        'async function validate(doc: TextDocument) {',
        '    const diags: Diagnostic[] = [];',
        '    const text = doc.getText();',
        '    const pattern = /\\bTODO\\b/g;',
        '    let m;',
        '    while ((m = pattern.exec(text)) !== null) {',
        '        diags.push({',
        '            severity: DiagnosticSeverity.Warning,',
        '            range: {',
        '                start: doc.positionAt(m.index),',
        '                end:   doc.positionAt(m.index + m[0].length)',
        '            },',
        '            message: \'Незавершённая задача\',',
        '            source: \'my-lsp\'',
        '        });',
        '    }',
        '    connection.sendDiagnostics({ uri: doc.uri, diagnostics: diags });',
        '}',
        '',
        'connection.onCompletion((): CompletionItem[] => [',
        '    { label: \'function\', kind: CompletionItemKind.Keyword },',
        '    { label: \'return\',   kind: CompletionItemKind.Keyword },',
        '    { label: \'if\',       kind: CompletionItemKind.Keyword },',
        ']);',
        '',
        'documents.listen(connection);',
        'connection.listen();',
    ]))
    add(sp(3))
    add(p('Полная реализация Language Server с тремя ключевыми возможностями. <b>onInitialize()</b> объявляет capabilities — какие фичи поддерживает сервер: синхронизация документов, автодополнение, hover, go-to-definition, references. Функция <b>validate()</b> находит паттерн в тексте и отправляет диагностики через <b>sendDiagnostics()</b> — positionAt() конвертирует абсолютный offset в строку/колонку. <b>onCompletion()</b> возвращает статический список ключевых слов — в реальном сервере список формируется динамически на основе AST.'))
    add(pb())

    # ── ГЛАВА 11 ───────────────────────────────────────────────────────────────
    ch('11', 'UX Guidelines', 'Принципы качественного пользовательского интерфейса')

    add(h2('Ключевые принципы'))
    for item in [
        '<b>Не мешай.</b> Никаких уведомлений при старте без запроса пользователя',
        '<b>Следуй паттернам VS Code.</b> Используй Command Palette, Quick Pick, InputBox',
        '<b>Минимум кликов.</b> Самые частые действия — самые быстрые',
        '<b>Читаемые имена.</b> Формат "My Extension: Do Action" в Command Palette',
        '<b>Уважай ресурсы.</b> Не активируйся при старте VS Code без необходимости',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Activity Bar и Sidebar'))
    add(tblh(['Рекомендация', 'Описание']))
    add(tbl2([
        ('Когда добавлять',   'Расширение имеет сложный UI с несколькими View для регулярного использования'),
        ('Когда НЕ добавлять','Расширение используется редко. Лучше добавить команду в Command Palette'),
        ('Иконка',           'SVG 16×16, монохромная. VS Code применит цвет темы автоматически'),
    ]))
    add(sp(6))

    add(h2('Status Bar'))
    add(p('Используйте для постоянно актуальной информации: текущая ветка, количество ошибок, активный профиль:'))
    add(sp(3))
    add(code([
        'const item = vscode.window.createStatusBarItem(',
        '    vscode.StatusBarAlignment.Left, 100',
        ');',
        'item.text    = \'$(check) Ready\';',
        'item.tooltip = \'My Extension — всё хорошо\';',
        'item.command = \'myext.showDetails\';',
        'item.show();',
        'context.subscriptions.push(item);',
        '',
        '// Обновление',
        'vscode.window.onDidChangeActiveTextEditor(editor => {',
        '    item.text = editor',
        '        ? `$(file-code) ${editor.document.languageId}`',
        '        : \'$(dash)\';',
        '});',
    ]))
    add(sp(3))
    add(p('<b>createStatusBarItem(alignment, priority)</b> создаёт элемент в строке состояния. <b>priority</b> определяет позицию: большее число — ближе к центру. Вызывайте <b>hide()</b> когда расширение неактивно для текущего файла — Status Bar общий ресурс для всех расширений.'))
    add(sp(6))

    add(h2('Quick Pick — лучшие практики'))
    add(code([
        '// Хороший QuickPick с разделителями и описаниями',
        'const items: vscode.QuickPickItem[] = [',
        '    {',
        '        label: \'$(cloud-upload) Опубликовать\',',
        '        description: \'Marketplace\',',
        '        detail: \'Потребует Personal Access Token\'',
        '    },',
        '    { label: \'\', kind: vscode.QuickPickItemKind.Separator },',
        '    {',
        '        label: \'$(package) Упаковать\',',
        '        description: \'Создать .vsix\'',
        '    },',
        '];',
        '',
        'const pick = await vscode.window.showQuickPick(items, {',
        '    title: \'Действие с расширением\',',
        '    placeHolder: \'Выберите...\',',
        '    matchOnDescription: true,',
        '    matchOnDetail: true',
        '});',
    ]))
    add(sp(3))
    add(p('Продвинутый QuickPick с UX-паттернами VS Code. Каждый item содержит <b>label</b> с Codicon-иконкой, <b>description</b> и <b>detail</b> для дополнительного контекста. <b>QuickPickItemKind.Separator</b> визуально группирует элементы. Флаги <b>matchOnDescription</b> и <b>matchOnDetail</b> расширяют поиск — пользователь находит элемент по любому полю, не только по label.'))
    add(sp(4))
    add(box('Walkthroughs',
        'Для onboarding новых пользователей используйте contributes.walkthroughs — '
        'пошаговые туториалы, появляющиеся при первой установке расширения. '
        'Значительно повышают adoption rate.', 'tip'))
    add(pb())

    # ── ГЛАВА 12 ───────────────────────────────────────────────────────────────
    ch('12', 'Тестирование расширений', 'Unit, Integration и E2E тесты')

    add(h2('Три вида тестов'))
    add(p('В экосистеме VS Code расширений принято выделять три уровня тестирования — '
          'каждый решает свою задачу:'))
    add(sp(3))
    add(tblh(['Вид', 'Описание']))
    add(tbl2([
        ('Unit Tests',
         'Обычные тесты без VS Code. Тестируют изолированную бизнес-логику: '
         'парсеры, утилиты, алгоритмы. Любой фреймворк: Jest, Mocha, Vitest. '
         'Самые быстрые — запускаются за секунды'),
        ('Integration Tests\n(@vscode/test-cli)',
         'Запускаются внутри реального Extension Development Host. '
         'Полный доступ к vscode API: открыть файл, выполнить команду, проверить диагностику. '
         'Медленнее — требуют запуска VS Code. 90% тестов расширения'),
        ('E2E Tests\n(Playwright)',
         'Тестируют реальный UI браузерными инструментами: кликают по кнопкам, '
         'проверяют визуальные состояния, тестируют Webview. '
         'Самые медленные. Нужны для: Webview UI, визуальных декораций, '
         'скриншотных тестов. Подробно — в главе 19'),
    ]))
    add(sp(4))
    add(box('Playwright для E2E',
        'Если вам нужно тестировать Webview UI или визуальные компоненты, '
        'используйте Playwright + @vscode/test-web. '
        'Полное описание с примерами кода — в главе 19 «E2E тестирование с Playwright».',
        'note'))
    add(sp(6))

    add(h2('@vscode/test-cli — современный подход'))
    add(code([
        '# Установка',
        'npm install --save-dev @vscode/test-cli @vscode/test-electron',
        '',
        '# package.json',
        '"scripts": {',
        '    "test": "vscode-test"',
        '}',
    ]))
    add(sp(3))
    add(p('Пакет <b>@vscode/test-cli</b> — современная замена устаревшему vscode-test. <b>@vscode/test-electron</b> скачивает нужную версию VS Code для запуска тестов. Скрипт <b>vscode-test</b> в package.json читает конфигурацию из .vscode-test.mjs и запускает тесты внутри Extension Development Host.'))
    add(sp(3))
    add(code([
        '// .vscode-test.mjs — конфигурация',
        'import { defineConfig } from \'@vscode/test-cli\';',
        '',
        'export default defineConfig([',
        '    {',
        '        label: \'integration\',',
        '        files: \'out/test/**/*.test.js\',',
        '        version: \'stable\',',
        '        workspaceFolder: \'./test-workspace\',',
        '        mocha: { timeout: 20000 }',
        '    }',
        ']);',
    ]))
    add(sp(3))
    add(p('Файл конфигурации <b>.vscode-test.mjs</b> использует <b>defineConfig()</b> для типобезопасности. <b>files</b> — glob-паттерн тестовых файлов, <b>version</b> — какую версию VS Code скачать (stable/insiders), <b>workspaceFolder</b> — рабочая папка для тестов с фикстурами. <b>mocha.timeout</b> увеличен до 20 секунд — запуск Extension Host медленнее обычных тестов.'))

    add(sp(6))

    add(h2('Написание тестов'))
    add(code([
        '// src/test/extension.test.ts',
        'import * as assert from \'assert\';',
        'import * as vscode from \'vscode\';',
        '',
        'suite(\'Extension Test Suite\', () => {',
        '',
        '    test(\'Расширение активируется\', async () => {',
        '        const ext = vscode.extensions.getExtension(',
        '            \'my-publisher.my-extension\'',
        '        );',
        '        assert.ok(ext, \'Расширение должно быть установлено\');',
        '        await ext!.activate();',
        '        assert.ok(ext!.isActive, \'Расширение должно быть активно\');',
        '    });',
        '',
        '    test(\'Команда зарегистрирована\', async () => {',
        '        const commands = await vscode.commands.getCommands();',
        '        assert.ok(',
        '            commands.includes(\'myext.myCommand\'),',
        '            \'Команда должна быть в реестре\'',
        '        );',
        '    });',
        '',
        '    test(\'Диагностика работает\', async () => {',
        '        const doc = await vscode.workspace.openTextDocument({',
        '            content: \'TODO: исправить это\',',
        '            language: \'plaintext\'',
        '        });',
        '        await vscode.window.showTextDocument(doc);',
        '        await new Promise(r => setTimeout(r, 1000));',
        '        // const diags = vscode.languages.getDiagnostics(doc.uri);',
        '        // assert.ok(diags.length > 0);',
        '    });',
        '});',
    ]))
    add(sp(3))
    add(p('Три типичных интеграционных теста. Первый проверяет что расширение установлено и активируется через <b>getExtension()</b> + <b>activate()</b>. Второй — что команда зарегистрирована в реестре VS Code через <b>getCommands()</b>. Третий открывает документ с текстом через <b>openTextDocument()</b>, показывает его и даёт время на обработку — после чего можно проверить диагностики через <b>getDiagnostics()</b>.'))
    add(sp(4))
    add(box('CI без дисплея',
        'На Linux в CI (GitHub Actions, GitLab CI) используйте: '
        'xvfb-run -a npm test '
        'VS Code требует дисплей для запуска. Xvfb эмулирует виртуальный дисплей.', 'warn'))
    add(sp(4))
    from book_new import build_playwright_chapter
    for el in build_playwright_chapter():
        add(el)
    add(pb())

    # ── ГЛАВА 13 ───────────────────────────────────────────────────────────────
    ch('13', 'Бандлинг с esbuild', 'Оптимизация размера и совместимость с Web')

    add(h2('Зачем нужен бандлинг?'))
    add(tblh(['Причина', 'Описание']))
    add(tbl2([
        ('Web-совместимость',
         'На vscode.dev и github.dev расширение должно быть одним JS-файлом. '
         'Без бандла работать не будет'),
        ('Размер пакета',
         'Без бандлинга node_modules входят в .vsix. '
         'С бандлингом — только используемый код (tree-shaking)'),
        ('Скорость загрузки',
         'Один большой файл загружается быстрее 100 маленьких из-за ФС'),
    ]))
    add(sp(6))

    add(h2('esbuild — рекомендуемый бандлер'))
    add(code([
        '# Установка',
        'npm install --save-dev esbuild',
    ]))
    add(sp(3))
    add(p('Конфигурация esbuild для VS Code расширения: <b>platform: "node"</b> и <b>external: ["vscode"]</b> обязательны — модуль vscode предоставляет рантайм, не включается в бандл. <b>sourcemap: "linked"</b> сохраняет карты для отладки в Extension Development Host.'))
    from book_new import bun_inject
    for _el in bun_inject(): add(_el)
    add(code([
        '// esbuild.js',
        'const esbuild = require(\'esbuild\');',
        '',
        'const production = process.argv.includes(\'--production\');',
        'const watch      = process.argv.includes(\'--watch\');',
        '',
        'async function main() {',
        '    const ctx = await esbuild.context({',
        '        entryPoints: [\'src/extension.ts\'],',
        '        bundle: true,',
        '        format: \'cjs\',',
        '        minify: production,',
        '        sourcemap: !production,',
        '        sourcesContent: false,',
        '        platform: \'node\',',
        '        outfile: \'dist/extension.js\',',
        '        // ВАЖНО: vscode предоставляется рантаймом — не включать в бандл',
        '        external: [\'vscode\'],',
        '        logLevel: \'warning\',',
        '    });',
        '',
        '    if (watch) {',
        '        await ctx.watch();',
        '        console.log(\'Watching...\');',
        '    } else {',
        '        await ctx.rebuild();',
        '        await ctx.dispose();',
        '    }',
        '}',
        '',
        'main().catch(e => { console.error(e); process.exit(1); });',
    ]))
    add(sp(3))
    add(p('Полный скрипт сборки esbuild с двумя режимами. В режиме <b>--watch</b> esbuild отслеживает изменения файлов и пересобирает мгновенно (~10мс). Без флага — однократная сборка и выход. <b>format: "cjs"</b> обязателен — Extension Host загружает модули через require(). <b>sourcesContent: false</b> уменьшает размер source map, ссылаясь на оригинальные файлы вместо встраивания их содержимого.'))
    add(sp(3))
    add(code([
        '// package.json scripts',
        '"scripts": {',
        '    "compile":          "node esbuild.js",',
        '    "watch":            "node esbuild.js --watch",',
        '    "vscode:prepublish":"node esbuild.js --production",',
        '    "test":             "vscode-test"',
        '},',
        '"main": "./dist/extension.js",',
    ]))
    add(sp(3))
    add(p('Связка скриптов для полного цикла разработки. Ключевой скрипт — <b>vscode:prepublish</b>: @vscode/vsce вызывает его автоматически перед упаковкой в .vsix, поэтому здесь включён флаг <b>--production</b> для минификации. Поле <b>main</b> указывает на <b>dist/extension.js</b> вместо стандартного out/ — VS Code загружает именно этот бандл.'))

    add(sp(6))

    add(h2('Web Extensions — расширения для браузера'))
    add(code([
        '// package.json',
        '"main":    "./dist/extension.js",      // Node.js',
        '"browser": "./dist/web/extension.js",  // Browser',
        '',
        '// esbuild.js — добавить web сборку',
        'await esbuild.build({',
        '    entryPoints: [\'src/web/extension.ts\'],',
        '    bundle:   true,',
        '    format:   \'cjs\',',
        '    platform: \'browser\',',
        '    outfile:  \'dist/web/extension.js\',',
        '    external: [\'vscode\'],',
        '});',
    ]))
    add(sp(3))
    add(p('Двойная точка входа: <b>main</b> для Node.js (десктоп) и <b>browser</b> для Web (vscode.dev, github.dev). <b>platform: "browser"</b> в esbuild заменяет Node.js-специфичные модули на браузерные полифиллы. Оба бандла исключают vscode через <b>external</b> — рантайм предоставляет API в обоих окружениях.'))

    add(sp(4))
    add(box('Ограничения Web Extensions',
        'В браузере недоступны: fs, path, child_process, os и Node.js core модули. '
        'Используйте: fetch, crypto, TextEncoder, URL. '
        'Для файловых операций — vscode.workspace.fs вместо fs.', 'warn'))
    add(sp(6))

    add(h3('Ограничения Web Extensions'))
    add(p('Web Extensions работают в браузерном контексте без Node.js. Следующие API и паттерны <b>не работают</b>:'))
    add(sp(3))
    add(tblh(['Что не работает', 'Альтернатива']))
    add(tbl2([
        ('require(), import() динамический', 'Статический import, бандлинг в один файл'),
        ('Node.js fs, path, os, child_process', 'vscode.workspace.fs для файлов'),
        ('URI.file(), fsPath', 'vscode.Uri.parse() с кастомной схемой'),
        ('process.env, process.cwd()', 'vscode.workspace.workspaceFolders'),
        ('Нативные модули (*.node)', 'WebAssembly альтернативы'),
        ('typeof navigator для проверки среды', 'typeof process === "object" (с Node.js 22 navigator есть и в Node!)'),
        ('child_process.spawn()', 'Terminal API или Language Server через WASM'),
    ]))
    add(sp(3))
    add(p('<b>Важно с VS Code 1.101:</b> обновление до Node.js 22 добавило глобальный <b>navigator</b> в Node.js. Код вида <b>if (typeof navigator !== "undefined")</b> теперь сломан — он возвращает true и в Node. Используйте <b>typeof process === "object" &amp;&amp; process.versions?.node</b> для проверки Node.js окружения.'))
    add(sp(6))
    add(pb())

    # ── ГЛАВА 14 ───────────────────────────────────────────────────────────────
    ch('14', 'Публикация в Marketplace', '@vscode/vsce, VS Code Marketplace и Open VSX Registry')

    add(h2('Требования перед публикацией'))
    add(tblh(['Файл/поле', 'Требования']))
    add(tbl2([
        ('README.md',      'Содержательное описание с GIF/скриншотами и примерами'),
        ('CHANGELOG.md',   'История изменений по версиям'),
        ('icon.png',       'PNG 128×128 или 256×256. SVG не поддерживается'),
        ('.vscodeignore',  'Исключает src/**, тесты, node_modules для уменьшения .vsix'),
        ('keywords',       '3–5 ключевых слов для поиска в Marketplace'),
        ('categories',     'Правильная категория для лучшей видимости'),
        ('repository.url', 'Ссылка на GitHub — обязательно для доверия'),
        ('engines.vscode', 'Корректный минимальный диапазон версий'),
    ]))
    add(sp(6))

    add(h2('Публикация через @vscode/vsce'))
    add(p('<b>@vscode/vsce</b> (Visual Studio Code Extensions) — официальный CLI для управления расширениями. Пакет ранее назывался просто <b>vsce</b>, но был переименован в <b>@vscode/vsce</b>. Старое имя <b>vsce</b> в npm deprecated — всегда используйте <b>@vscode/vsce</b>.'))
    add(sp(3))
    add(code([
        '# Установка',
        'npm install -g @vscode/vsce',
        '',
        '# Создание publisher-аккаунта на marketplace.visualstudio.com',
        '# Создание PAT в Azure DevOps (Scope: Marketplace → Manage)',
        '',
        '# Вход',
        'vsce login my-publisher-name',
        '',
        '# Упаковка без публикации',
        'vsce package',
        '# → my-extension-1.0.0.vsix',
        '',
        '# Публикация',
        'vsce publish',
        '',
        '# Публикация с автоинкрементом версии',
        'vsce publish patch   # 1.0.0 → 1.0.1',
        'vsce publish minor   # 1.0.0 → 1.1.0',
        'vsce publish major   # 1.0.0 → 2.0.0',
        '',
        '# Отзыв',
        'vsce unpublish (publisher).(extension)',
    ]))
    add(sp(3))
    add(p('После установки <b>@vscode/vsce</b> CLI-команда в терминале остаётся <b>vsce</b> — это алиас. <b>vsce package</b> упаковывает расширение в .vsix файл для тестирования или установки. <b>vsce publish</b> публикует в Marketplace; требует PAT с правами Marketplace (Manage). <b>--pre-release</b> публикует pre-release версию — пользователи с "Auto Update" получат её только при явном opt-in.'))
    add(sp(4))
    add(code([
        '# .vscodeignore — исключения из пакета',
        '.vscode/**',
        '.vscode-test/**',
        'src/**',
        'test/**',
        '**/*.map',
        '**/*.ts',
        '!out/**',
        '!dist/**',
        'node_modules/**',
        '.github/**',
        'esbuild.js',
        '*.yml',
        '*.yaml',
    ]))
    add(sp(3))
    add(p('Файл <b>.vscodeignore</b> работает аналогично .gitignore — исключает файлы из .vsix пакета. Исходники (src/**, **/*.ts), тесты, source maps и конфигурации CI не нужны пользователю. Паттерны <b>!out/**</b> и <b>!dist/**</b> — исключения из исключений: скомпилированный код должен попасть в пакет. Без .vscodeignore node_modules и исходники увеличивают размер пакета в 5–10 раз.'))

    add(sp(6))

    add(h2('Категории, теги и обнаруживаемость в Marketplace'))

    add(p('Marketplace VS Code — не поисковик в привычном смысле. '
          'Большинство установок приходит не через поиск, а через '
          'рекомендации внутри VS Code, вкладку «Popular» и прямые ссылки. '
          'Тем не менее правильные метаданные влияют на фильтрацию по категориям '
          'и подсказки при открытии файлов нужного типа.'))
    add(sp(4))

    add(h3('Официальные категории'))
    add(p('Актуальный список: <b>code.visualstudio.com/api/references/extension-manifest#categories</b>'))
    add(sp(3))
    add(p('Поле <b>categories</b> в package.json принимает строго определённый набор. '
          'Неверная категория — не ошибка при публикации, но расширение попадёт '
          'в неправильный раздел Marketplace:'))
    add(sp(3))
    add(tblh(['Категория', 'Когда использовать']))
    add(tbl2([
        ('Programming Languages',
         'Поддержка языка: подсветка, IntelliSense, форматирование. '
         'Самая крупная категория — высокая конкуренция'),
        ('Snippets',
         'Расширение только со сниппетами, без дополнительной логики'),
        ('Linters',
         'Статический анализ кода, вывод диагностик. '
         'ESLint, Pylance попадают сюда'),
        ('Formatters',
         'Форматирование документа (registerDocumentFormattingEditProvider). '
         'Prettier, Black, gofmt. '
         '[*] Форматтер возвращает TextEdit[] — VS Code применяет изменения '
         'к буферу редактора, файл на диске не меняется до явного сохранения (Ctrl+S). '
         'Это стандартное поведение всего Formatting API, не специфика Prettier. '
         'Источник: code.visualstudio.com/api/references/vscode-api#DocumentFormattingEditProvider'),
        ('Debuggers',
         'Реализует Debug Adapter Protocol. '
         'Для поддержки отладки конкретного языка/рантайма'),
        ('Themes',
         'Color Theme или File Icon Theme. '
         'Визуальное оформление без функциональности'),
        ('Testing',
         'Интеграция с тест-раннерами, TestController API'),
        ('SCM Providers',
         'Source Control Management — альтернативные VCS'),
        ('Other',
         'Всё остальное. Категория по умолчанию — '
         'не используйте если подходит что-то конкретное'),
        ('AI',             'Chat Participants, Language Model Tools, Copilot интеграции'),
        ('Chat',           'Расширения чат-интерфейса'),
        ('Keymaps',        'Переносит горячие клавиши из другого редактора'),
        ('Education',      'Учебные инструменты, интерактивные уроки'),
        ('Data Science',   'Jupyter, анализ данных, ML инструменты'),
        ('Visualization',  'Диаграммы, graphviz, превью'),
        ('Notebooks',      'Notebook API расширения'),
    ]))
    add(sp(4))

    add(h3('Ключевые слова (keywords)'))
    add(p('Поле <b>keywords</b> — массив строк. '
          'Раньше лимит был 5, сейчас он не документирован жёстко, '
          'но злоупотребление (~30+) раньше давало пенальти в поиске. '
          'Оптимально: 5–10 релевантных слов.'))
    add(sp(3))
    add(code([
        '// package.json — пример хороших метаданных',
        '{',
        '  "categories": ["Programming Languages", "Formatters"],',
        '  "keywords": [',
        '    "python",      // целевой язык',
        '    "formatter",   // функциональность',
        '    "pep8",        // конкретный стандарт',
        '    "autopep8",    // инструмент',
        '    "black"        // альтернатива (люди ищут сравнения)',
        '  ]',
        '}',
    ], highlight=False))
    add(sp(3))
    add(p('Пример метаданных для Python-форматтера. <b>categories</b> содержит два значения — расширение появится в обоих разделах Marketplace. Ключевые слова покрывают разные стратегии поиска: целевой язык, тип функциональности, конкретный стандарт и названия альтернативных инструментов.'))

    add(sp(4))

    add(h3('Антипаттерны и лайфхаки'))
    for btext in [
        '<b>Антипаттерн: категория "Other"</b> — расширение выпадает из фильтров. '
        'Если подходит несколько категорий — укажите все (массив)',
        '<b>Антипаттерн: общие теги</b> — "vscode", "extension", "plugin" не помогают, '
        'их у всех тысячи. Используйте специфичные для предметной области',
        '<b>Лайфхак: displayName</b> — поле, по которому первым делом ищут пользователи. '
        'Включите ключевое слово: "Python Formatter" лучше чем "PyFmt"',
        '<b>Лайфхак: description</b> — первые 100 символов видны в подсказках внутри VS Code. '
        'Начните с глагола действия: "Formats Python code..." вместо "A formatter for..."',
        '<b>Лайфхак: recommendations</b> — добавьте расширение в .vscode/extensions.json '
        'реальных проектов (собственных или через PR). '
        'Когда VS Code предлагает установить расширения для проекта — это самый конверсионный канал',
        '<b>Лайфхак: activationEvents точно</b> — расширение, которое не тормозит VS Code, '
        'получает лучшие отзывы органически. Скорость важнее любых тегов',
    ]:
        add(bul(btext))
    add(sp(4))

    add(box('Помогают ли теги найти расширение?',
        'Честный ответ: умеренно. '
        'Поиск в Marketplace — не Google. Алгоритм учитывает displayName, description и keywords, '
        'но главные факторы ранжирования — количество установок и рейтинг. '
        'Новое расширение с нулём установок окажется на 50-й странице поиска независимо от тегов. '
        'Настоящий трафик приходит через: рекомендации внутри VS Code (workspaceContains), '
        'упоминания в README популярных проектов, статьи и видео. '
        'Правильные метаданные — гигиена, не маркетинг.',
        'note'))
    add(sp(6))

    add(h2('Open VSX Registry'))
    add(p('Open VSX — маркетплейс Eclipse Foundation для редакторов на базе VS Code без доступа к официальному Marketplace: Cursor, VSCodium, Gitpod, Theia.'))
    add(sp(3))
    add(code([
        '# Установка',
        'npm install -g ovsx',
        '',
        '# Создание токена: open-vsx.org → Settings → Access Tokens',
        '',
        '# Публикация',
        'ovsx publish my-extension-1.0.0.vsix -p $OVSX_TOKEN',
        '',
        '# Или из исходников',
        'ovsx publish -p $OVSX_TOKEN',
    ]))
    add(sp(3))
    add(p('Публикация в Open VSX через CLI-утилиту <b>ovsx</b>. Два варианта: из готового .vsix файла (удобно в CI — один артефакт для обоих маркетплейсов) или из исходников (ovsx соберёт пакет самостоятельно). Токен создаётся на open-vsx.org — отдельный от Azure DevOps PAT.'))

    add(sp(4))
    add(box('Два реестра — две публикации',
        'VS Code Marketplace и Open VSX — независимые платформы. '
        'Для доступности расширения везде нужно публиковать в оба. '
        'Автоматизируйте через GitHub Actions.', 'warn'))
    add(sp(6))

    add(h2('Почему расширения отклоняются или удаляются'))
    add(p('Microsoft не публикует полный список причин отказа, но на основе '
          'публичных обращений разработчиков выделяются следующие категории:'))
    add(sp(3))
    add(tblh(['Причина', 'Подробности']))
    add(tbl2([
        ('Сбор данных без согласия',
         'Наиболее частая причина удаления в 2024-2025. '
         'Расширения, собирающие телеметрию без явного opt-in, '
         'нарушают Marketplace Terms. '
         'В 2025 году Microsoft удалила несколько популярных расширений за это без предупреждения. '
         'Решение: всегда проверять vscode.env.isTelemetryEnabled, '
         'использовать @vscode/extension-telemetry'),
        ('Вредоносный код',
         'Marketplace сканирует каждый пакет несколькими антивирусами. '
         'Динамическое обнаружение запускает расширение в sandboxed VM. '
         'Обфусцированный код вызывает подозрение даже без явного вреда'),
        ('Name squatting',
         'Имена, имитирующие Microsoft, RedHat или популярные расширения — '
         'отклоняются автоматически. '
         'Пример: "microsoft-python" или "github-copilot-pro" будут отклонены'),
        ('Нарушение IP/лицензий',
         'Расширение, включающее GPL-код несовместимо с закрытой лицензией. '
         'Или: использование чужих брендовых иконок без разрешения'),
        ('Технические требования',
         'Отсутствие README, невалидный package.json, '
         'ссылки на несуществующий repository.url, '
         'engines.vscode указывает на несуществующую версию'),
        ('Контент нарушающий правила',
         'Взрослый контент, политическая агитация, спам. '
         'Расширения, которые делают не то что написано в описании'),
    ]))
    add(sp(3))
    add(p('<b>Проверка перед публикацией:</b> '
          '<b>vsce ls</b> — список файлов в пакете (убедитесь что нет лишнего). '
          '<b>vsce package</b> — создаёт .vsix без публикации (тестируйте локально). '
          'Апелляции: vsmarketplace@microsoft.com с publisher ID и extension ID.'))
    add(sp(3))
    add(box('Secret Scanning',
        'Marketplace автоматически сканирует каждое расширение на наличие секретов: '
        'API ключи, токены Azure DevOps, credentials. '
        'Не включайте .env файлы, конфигурацию с токенами или private ключи в .vsix. '
        'Используйте .vscodeignore для исключения.',
        'warn'))
    add(pb())

    # ── ГЛАВА 15 ───────────────────────────────────────────────────────────────
    ch('15', 'CI/CD автоматизация', 'GitHub Actions для тестирования и публикации')

    add(h2('Workflow тестирования'))
    add(code([
        '# .github/workflows/ci.yml',
        'name: CI',
        'on:',
        '  push:',
        '    branches: [main]',
        '  pull_request:',
        '    branches: [main]',
        '',
        'jobs:',
        '  test:',
        '    strategy:',
        '      matrix:',
        '        os: [ubuntu-latest, windows-latest, macos-latest]',
        '        vscode: [stable, insiders]',
        '    runs-on: ${{ matrix.os }}',
        '    steps:',
        '      - uses: actions/checkout@v4',
        '      - uses: actions/setup-node@v4',
        '        with: { node-version: \'20\', cache: \'npm\' }',
        '      - run: npm ci',
        '      - run: npm run compile',
        '      - name: Run tests (Linux)',
        '        if: runner.os == \'Linux\'',
        '        run: xvfb-run -a npm test',
        '        env: { VSCODE_TEST_VERSION: ${{ matrix.vscode }} }',
        '      - name: Run tests (macOS/Windows)',
        '        if: runner.os != \'Linux\'',
        '        run: npm test',
        '        env: { VSCODE_TEST_VERSION: ${{ matrix.vscode }} }',
    ]))
    add(sp(3))
    add(p('CI workflow с матрицей из 6 комбинаций: 3 ОС (Ubuntu, Windows, macOS) и 2 версии VS Code (stable, insiders). <b>xvfb-run</b> создаёт виртуальный дисплей на Linux — VS Code требует X11 даже для headless тестов. Условие <b>if: runner.os</b> разделяет запуск: на macOS и Windows виртуальный дисплей не нужен.'))
    add(sp(6))

    add(h2('Workflow публикации'))
    add(code([
        '# .github/workflows/publish.yml',
        'name: Publish',
        'on:',
        '  push:',
        '    tags: [\'v*.*.*\']',
        '',
        'jobs:',
        '  publish:',
        '    runs-on: ubuntu-latest',
        '    steps:',
        '      - uses: actions/checkout@v4',
        '      - uses: actions/setup-node@v4',
        '        with: { node-version: \'20\' }',
        '      - run: npm ci && npm run compile',
        '      - run: xvfb-run -a npm test',
        '      - run: npx @vscode/vsce package',
        '      - name: Publish to VS Code Marketplace',
        '        run: npx @vscode/vsce publish -p ${{ secrets.VSCE_TOKEN }}',
        '      - name: Publish to Open VSX',
        '        run: npx ovsx publish *.vsix -p ${{ secrets.OVSX_TOKEN }}',
        '      - name: Create GitHub Release',
        '        uses: softprops/action-gh-release@v2',
        '        with:',
        '          files: \'*.vsix\'',
        '          generate_release_notes: true',
    ]))
    add(sp(3))
    add(p('Workflow публикации по git-тегу <b>v*.*.*</b>. Последовательность: сборка, тесты, упаковка в .vsix, публикация в оба маркетплейса, создание GitHub Release с .vsix артефактом. Токены <b>VSCE_TOKEN</b> и <b>OVSX_TOKEN</b> хранятся в GitHub Secrets — никогда не в коде.'))
    add(sp(4))
    add(box('Хранение токенов',
        'НИКОГДА не записывайте токены в код или yaml. '
        'GitHub Settings → Secrets and variables → Actions → New repository secret.', 'warn'))
    add(pb())

    # ── ГЛАВА 16 ───────────────────────────────────────────────────────────────
    ch('16', 'Extension Host', 'Архитектура изоляции расширений')

    add(h2('Виды Extension Host'))
    add(p('Актуальный список: <b>code.visualstudio.com/api/advanced-topics/extension-host</b>'))
    add(sp(3))
    add(tblh(['Вид', 'Описание']))
    add(tbl2([
        ('local',  'Node.js процесс на той же машине что и UI. Стандартный для VS Code Desktop'),
        ('web',    'Браузерный хост. Запускается на vscode.dev, github.dev, VS Code for Web'),
        ('remote', 'Node.js процесс удалённо: SSH, Dev Containers, GitHub Codespaces'),
    ]))
    add(sp(4))
    add(p('При Remote Development одни расширения работают локально (UI extensions), другие — удалённо (workspace extensions). Расположение можно явно задать в package.json:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"extensionKind": ["ui", "workspace"]',
        '// "ui"        — только локальный UI-хост',
        '// "workspace" — только workspace-хост (remote или local)',
        '// ["ui", "workspace"] — предпочтительно UI, иначе workspace',
        '',
        '// Для Web Extension:',
        '"browser": "./dist/web/extension.js"',
    ]))
    add(sp(3))
    add(p('Поле <b>extensionKind</b> определяет где запускается расширение при Remote Development. Массив задаёт приоритет: <b>["ui", "workspace"]</b> означает «предпочтительно локально, но если невозможно — удалённо». Поле <b>browser</b> в package.json — точка входа для Web Extension, используется на vscode.dev и github.dev вместо <b>main</b>.'))

    add(sp(6))

    add(h2('Лучшие практики для Extension Host'))
    for item in [
        '<b>Ленивая активация:</b> используйте минимально необходимые Activation Events',
        '<b>async/await:</b> все потенциально долгие операции — асинхронно',
        '<b>CancellationToken:</b> поддерживайте отмену во всех провайдерах',
        '<b>Dispose:</b> регистрируйте всё в context.subscriptions',
        '<b>Не блокируйте:</b> никаких синхронных файловых операций в production',
    ]:
        add(bul(item))
    add(sp(4))
    add(box('Мониторинг Extension Host',
        'Команда Developer: Show Running Extensions отображает все активные расширения '
        'и время их активации. Команда Developer: Inspect Extension Host позволяет '
        'подключить дебаггер к Extension Host процессу.', 'tip'))
    add(pb())

    # ── ГЛАВА 17 ───────────────────────────────────────────────────────────────
    ch('17', 'AI-расширения: Chat Participant', 'Copilot Chat API и Language Model API')

    add(h2('AI Extensibility в VS Code'))
    add(p('Начиная с VS Code 1.90, Extension API позволяет интегрироваться с GitHub Copilot:'))
    add(sp(2))
    for item in [
        '<b>Chat Participants</b> — специализированные AI-ассистенты в Copilot Chat (@my-assistant)',
        '<b>Language Model API</b> — вызов AI-моделей из кода расширения',
        '<b>Language Model Tools</b> — функции, которые AI вызывает автоматически в агентском режиме',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Chat Participant — объявление в package.json'))
    add(code([
        '"contributes": {',
        '  "chatParticipants": [{',
        '    "id": "my-extension.assistant",',
        '    "name": "my-assistant",',
        '    "fullName": "My AI Assistant",',
        '    "description": "Специализированный ассистент для моего проекта",',
        '    "isSticky": true,',
        '    "commands": [',
        '      { "name": "explain", "description": "Объяснить код" },',
        '      { "name": "fix",     "description": "Исправить ошибки" }',
        '    ]',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Объявление Chat Participant в package.json. <b>id</b> связывает декларацию с кодом регистрации, <b>name</b> — имя для @-упоминания в чате. <b>isSticky: true</b> означает что participant остаётся выбранным между сообщениями — пользователю не нужно повторно вводить @имя. Массив <b>commands</b> добавляет slash-команды: /explain, /fix — доступные после @-упоминания.'))
    add(sp(6))

    add(h2('Chat Participant — реализация'))
    add(code([
        'export function activate(context: vscode.ExtensionContext) {',
        '',
        '    const handler: vscode.ChatRequestHandler = async (',
        '        request: vscode.ChatRequest,',
        '        ctx:     vscode.ChatContext,',
        '        stream:  vscode.ChatResponseStream,',
        '        token:   vscode.CancellationToken',
        '    ) => {',
        '',
        '        stream.progress(\'Анализирую запрос...\');',
        '',
        '        // Получаем модель Copilot',
        '        const models = await vscode.lm.selectChatModels({',
        '            vendor: \'copilot\',',
        '            family: \'gpt-4o\'',
        '        });',
        '        if (models.length === 0) {',
        '            stream.markdown(\'Copilot недоступен.\');',
        '            return;',
        '        }',
        '',
        '        // Контекст из редактора',
        '        const editor = vscode.window.activeTextEditor;',
        '        const code   = editor ? editor.document.getText(editor.selection) : \'\';',
        '',
        '        const messages = [',
        '            vscode.LanguageModelChatMessage.System(',
        '                \'Ты эксперт по TypeScript. Отвечай кратко и по делу.\'',
        '            ),',
        '            vscode.LanguageModelChatMessage.User(',
        '                `${request.prompt}\\n\\n\`\`\`typescript\\n${code}\\n\`\`\``',
        '            )',
        '        ];',
        '',
        '        try {',
        '            const response = await models[0].sendRequest(messages, {}, token);',
        '            for await (const chunk of response.text) {',
        '                stream.markdown(chunk);',
        '            }',
        '        } catch (e) {',
        '            if (e instanceof vscode.LanguageModelError)',
        '                stream.markdown(`Ошибка: ${e.message}`);',
        '        }',
        '    };',
        '',
        '    const participant = vscode.chat.createChatParticipant(',
        '        \'my-extension.assistant\', handler',
        '    );',
        '',
        '    // Follow-up вопросы',
        '    participant.followupProvider = {',
        '        provideFollowups() {',
        '            return [',
        '                { prompt: \'Объясни подробнее\', label: \'$(info) Подробнее\' },',
        '                { prompt: \'Покажи пример\',     label: \'$(code) Пример\'    },',
        '            ];',
        '        }',
        '    };',
        '',
        '    context.subscriptions.push(participant);',
        '}',
    ]))
    add(sp(3))
    add(p('Полная реализация Chat Participant из 4 частей. <b>1) Handler</b> — функция обработки запроса, получает prompt пользователя, контекст чата и stream для ответа. <b>2) Модель</b> — selectChatModels() выбирает Copilot LLM; sendRequest() вызывает её с системным и пользовательским сообщениями, ответ читается чанками через <b>for await</b>. <b>3) Контекст</b> — выделенный код из активного редактора добавляется к промпту. <b>4) Follow-ups</b> — провайдер предлагает следующие вопросы после ответа.'))
    add(sp(6))

    add(h3('Библиотеки для Chat Participants'))
    add(p('Microsoft предоставляет две библиотеки, значительно упрощающие разработку Chat Participants:'))
    add(sp(3))
    add(tblh(['Пакет', 'Назначение']))
    add(tbl2([
        ('@vscode/prompt-tsx', 'JSX/TSX синтаксис для построения промптов с автоматическим управлением token budget'),
        ('@vscode/chat-extension-utils', 'Упрощённое создание Chat Participant с встроенной поддержкой tool calling'),
    ]))
    add(sp(3))
    add(code([
        '// Пример с @vscode/chat-extension-utils',
        'import { createChatParticipant } from \'@vscode/chat-extension-utils\';',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    const participant = createChatParticipant(context, {',
        '        id: \'myext.assistant\',',
        '        tools: [',
        '            {',
        '                name: \'searchFiles\',',
        '                description: \'Search for files in workspace\',',
        '                inputSchema: {',
        '                    type: \'object\',',
        '                    properties: {',
        '                        query: { type: \'string\', description: \'Search pattern\' }',
        '                    },',
        '                    required: [\'query\']',
        '                },',
        '                async invoke(input: { query: string }) {',
        '                    const files = await vscode.workspace.findFiles(input.query);',
        '                    return files.map(f => f.fsPath).join(\'\\n\');',
        '                }',
        '            }',
        '        ]',
        '    });',
        '}',
    ]))
    add(sp(3))
    add(p('<b>createChatParticipant()</b> из @vscode/chat-extension-utils берёт на себя всю инфраструктуру: маршрутизацию сообщений, tool calling, управление контекстом. Вы определяете только tools — набор функций, которые LLM может вызывать. Каждый tool описывается JSON Schema для входных параметров и async-функцией invoke.'))
    add(sp(6))

    add(pb())

    # ── ГЛАВА 18 ───────────────────────────────────────────────────────────────
    ch('18', 'Language Model Tools и MCP', 'Инструменты AI и Model Context Protocol')

    add(h2('Language Model Tools'))
    add(p('Language Model Tools — функции, которые AI автоматически вызывает как часть агентского цикла. Аналог function calling в OpenAI API:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "languageModelTools": [{',
        '    "name": "myext_getFileInfo",',
        '    "displayName": "Get File Info",',
        '    "modelDescription": "Возвращает тип, размер и число строк файла",',
        '    "inputSchema": {',
        '      "type": "object",',
        '      "properties": {',
        '        "filePath": { "type": "string", "description": "Путь к файлу" }',
        '      },',
        '      "required": ["filePath"]',
        '    }',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Декларация Language Model Tool в package.json. <b>modelDescription</b> — ключевое поле: AI читает его чтобы решить, когда вызвать инструмент (аналог function description в OpenAI). <b>inputSchema</b> описывает JSON Schema параметров — AI формирует вызов по этой схеме. Префикс <b>myext_</b> в имени предотвращает конфликты между расширениями.'))
    add(sp(3))
    add(code([
        '// Регистрация тула',
        'const tool = vscode.lm.registerTool(\'myext_getFileInfo\', {',
        '    async invoke(options, token) {',
        '        const { filePath } = options.input as { filePath: string };',
        '        const uri  = vscode.Uri.file(filePath);',
        '        const stat = await vscode.workspace.fs.stat(uri);',
        '        return new vscode.LanguageModelToolResult([',
        '            new vscode.LanguageModelTextPart(JSON.stringify({',
        '                size: stat.size,',
        '                type: stat.type === vscode.FileType.Directory ? \'dir\' : \'file\'',
        '            }))',
        '        ]);',
        '    }',
        '});',
        'context.subscriptions.push(tool);',
    ]))
    add(sp(3))
    add(p('Регистрация инструмента через <b>vscode.lm.registerTool()</b>. Метод <b>invoke()</b> получает типизированный input от AI-модели и возвращает <b>LanguageModelToolResult</b> с текстовыми частями. Используется <b>workspace.fs</b> вместо Node.js fs — обязательно для совместимости с Remote SSH и vscode.dev. Инструмент добавляется в <b>subscriptions</b> для корректной очистки при деактивации.'))
    add(sp(6))

    add(h2('MCP Dev Guide'))
    add(p('Model Context Protocol (MCP) — открытый стандарт Anthropic для интеграции AI с внешними данными. VS Code поддерживает MCP серверы:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "mcpServerDefinitionProviders": [{',
        '    "id": "my-mcp-provider"',
        '  }]',
        '}',
        '',
        '// extension.ts',
        'class MyMcpProvider implements vscode.McpServerDefinitionProvider {',
        '    async provideMcpServerDefinitions(token: vscode.CancellationToken) {',
        '        return [',
        '            new vscode.McpServerDefinition(',
        '                \'My MCP Server\',',
        '                new vscode.StdioMcpTransport(\'node\', [\'./server.js\'])',
        '            )',
        '        ];',
        '    }',
        '}',
        '',
        'vscode.lm.registerMcpServerDefinitionProvider(',
        '    \'my-mcp-provider\', new MyMcpProvider()',
        ');',
    ]))
    add(sp(3))
    add(p('Интеграция MCP-сервера в VS Code расширение. <b>McpServerDefinitionProvider</b> возвращает список MCP-серверов с их транспортом. <b>StdioMcpTransport</b> запускает сервер как дочерний процесс и общается через stdin/stdout — стандартный транспорт MCP. После регистрации через <b>registerMcpServerDefinitionProvider()</b> инструменты сервера становятся доступны AI-моделям в Copilot Chat.'))
    add(sp(6))

    add(h3('MCP в расширениях VS Code (v1.101+)'))
    add(p('С VS Code 1.101 расширения могут программно регистрировать MCP-серверы. Это позволяет паковать MCP-серверы прямо в расширение — пользователю не нужно устанавливать Python/Node.js сервер отдельно:'))
    add(sp(3))
    add(code([
        '// package.json — объявление MCP провайдера',
        '"contributes": {',
        '  "mcpServerDefinitionProviders": [{',
        '    "id": "myext.mcpServers",',
        '    "label": "My Extension MCP Servers"',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Объявление в package.json регистрирует провайдер MCP-серверов. <b>id</b> используется при программной регистрации, <b>label</b> отображается в настройках MCP.'))
    add(sp(3))
    add(code([
        '// Регистрация MCP сервера из расширения',
        'import * as vscode from \'vscode\';',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    const serverPath = context.asAbsolutePath(\'mcp-server/index.js\');',
        '',
        '    const provider: vscode.McpServerDefinitionProvider = {',
        '        provideMcpServerDefinitions() {',
        '            return [',
        '                new vscode.McpStdioServerDefinition({',
        '                    name: \'my-project-tools\',',
        '                    command: \'node\',',
        '                    args: [serverPath],',
        '                    env: { PROJECT_ROOT: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? \'\' },',
        '                }),',
        '            ];',
        '        }',
        '    };',
        '',
        '    context.subscriptions.push(',
        '        vscode.lm.registerMcpServerDefinitionProvider(\'myext.mcpServers\', provider)',
        '    );',
        '}',
    ]))
    add(sp(3))
    add(p('Расширение бандлит MCP-сервер (JavaScript файл) и регистрирует его через <b>McpStdioServerDefinition</b>. VS Code запускает сервер как дочерний процесс с переданными аргументами и переменными окружения. Доступен также <b>McpHttpServerDefinition</b> для HTTP-серверов. MCP tool annotations (<b>readOnlyHint: true</b>) позволяют пропускать подтверждение пользователя для безопасных операций чтения.'))
    add(sp(3))
    add(box('Copilot Chat — open source (v1.102)',
        'С VS Code 1.102 расширение Copilot Chat опубликовано под MIT-лицензией на GitHub. '
        'Это ~50 000 строк TypeScript — лучший пример реализации Chat Participant, '
        'tool calling, MCP интеграции и @vscode/prompt-tsx. '
        'Репозиторий: github.com/microsoft/vscode-copilot-chat', 'tip'))
    add(sp(6))

    add(h3('Language Model Chat Provider (v1.104+)'))
    add(p('С VS Code 1.104 расширения могут регистрировать собственные языковые модели — облачные или локальные. Зарегистрированная модель появляется в выпадающем списке моделей рядом с GPT-4 и Claude:'))
    add(sp(3))
    add(code([
        '// Регистрация кастомной модели',
        'const provider: vscode.ChatModelProvider = {',
        '    async provideLanguageModelResponse(',
        '        messages: vscode.LanguageModelChatMessage[],',
        '        options: vscode.LanguageModelChatRequestOptions,',
        '        token: vscode.CancellationToken',
        '    ) {',
        '        // Отправляем запрос к вашему API',
        '        const response = await fetch(\'https://my-llm-api.com/chat\', {',
        '            method: \'POST\',',
        '            body: JSON.stringify({',
        '                messages: messages.map(m => ({',
        '                    role: m.role === vscode.LanguageModelChatMessageRole.User',
        '                        ? \'user\' : \'assistant\',',
        '                    content: m.content.map(p => p.value).join(\'\')',
        '                }))',
        '            })',
        '        });',
        '',
        '        // Стриминг ответа',
        '        const reader = response.body!.getReader();',
        '        return {',
        '            stream: (async function*() {',
        '                while (true) {',
        '                    if (token.isCancellationRequested) break;',
        '                    const { done, value } = await reader.read();',
        '                    if (done) break;',
        '                    yield new TextDecoder().decode(value);',
        '                }',
        '            })()',
        '        };',
        '    }',
        '};',
        '',
        'vscode.lm.registerChatModelProvider(\'myext.localLlama\', provider, {',
        '    name: \'Local Llama 3\',',
        '    family: \'llama\',',
        '    version: \'3.1-8B\',',
        '    maxInputTokens: 128000,',
        '});',
    ]))
    add(sp(3))
    add(p('Провайдер реализует метод <b>provideLanguageModelResponse()</b>, который получает массив сообщений и возвращает async generator со стримингом токенов. Зарегистрированная модель доступна всем Chat Participants через <b>vscode.lm.selectChatModels()</b> — пользователь выбирает модель в интерфейсе, а ваш провайдер обрабатывает запросы.'))

    add(pb())

    # Справочники A/B/C/D перемещены в конец книги.
    # Послесловие перемещено в afterword.py (после справочников).

    return A


if __name__ == '__main__':
    print(f'Part 2 has {len(build_story_part2())} elements')
