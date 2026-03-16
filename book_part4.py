from book_helpers import *
import re

def build_story_part4():
    A = []
    def add(*x):
        for i in x: A.append(i)

    def ch(title, sub=''):
        add(StableAnchor('chapter_tips'))
        add(toc_ch(title), banner('Лайфхаки', title, sub), sp(12))

    # ═══════════════════════════════════════════════════════════════════════════
    ch('50+ лайфхаков разработчика расширений',
       'Советы из реального мира — Reddit, GitHub, блоги, опыт команды VS Code')
    # ═══════════════════════════════════════════════════════════════════════════

    add(h2('Раздел 1: Разработка и отладка'))
    add(sp(3))

    add(h3('1. Изолированный экземпляр VS Code для отладки'))
    add(p('Запускайте отдельный экземпляр VS Code с чистым профилем — незаменимо при подозрениях на конфликты расширений:'))
    add(sp(2))
    add(code([
        '# Полностью изолированный экземпляр',
        'code --user-data-dir="$HOME/vscode-debug" \\',
        '     --extensions-dir="$HOME/vscode-debug/extensions"',
        '',
        '# Или через переменные окружения',
        'VSCODE_DATA_DIR=/tmp/vscode-clean code .',
    ]))
    add(sp(3))
    add(p('Запуск VS Code с отдельными <b>--user-data-dir</b> и <b>--extensions-dir</b> создаёт полностью изолированный экземпляр — собственные настройки, собственный набор расширений. Позволяет быстро проверить, вызвана ли проблема конфликтом расширений или конфигурацией.'))

    add(sp(3))
    add(box('Практика',
        'Держите этот алиас постоянно в ~/.bashrc или ~/.zshrc. Если проблема '
        'исчезает в чистом экземпляре — виноват конфликт расширений или конфигурация. '
        'Сэкономит часы отладки.', 'tip'))
    add(sp(4))

    add(h3('2. TypeScript без шага компиляции (VS Code 1.108+)'))
    add(p('С декабря 2025 года VS Code поддерживает расширения прямо на TypeScript без tsc:'))
    add(sp(2))
    add(code([
        '// package.json — просто укажите .ts как main (экспериментально)',
        '"main": "./src/extension.ts",',
        '',
        '// Плюсы: мгновенная перезагрузка, нет шага сборки в dev',
        '// Минусы: публикация, тесты — пока не стабильно',
        '// (экспериментально, следите за release notes)',
    ]))
    add(sp(3))
    add(p('Экспериментальная поддержка TypeScript-файлов напрямую как <b>main</b> в package.json — VS Code стриппит типы на лету без шага tsc. Убирает цикл сборки в dev-режиме, но для публикации и тестов пока нестабильно.'))

    add(sp(4))

    add(h3('3. Быстрый перезапуск без пересборки'))
    add(p('В режиме разработки с watch-mode нажмите <b>Ctrl+R</b> в окне Extension Development Host вместо перезапуска F5:'))
    add(sp(2))
    add(code([
        '// tasks.json — запуск watch в фоне',
        '{',
        '  "label": "watch",',
        '  "type": "npm",',
        '  "script": "watch",',
        '  "isBackground": true,',
        '  "problemMatcher": "$tsc-watch",',
        '  "group": { "kind": "build", "isDefault": true }',
        '}',
        '',
        '// launch.json — preLaunchTask запускает watch',
        '{',
        '  "type": "extensionHost",',
        '  "request": "launch",',
        '  "preLaunchTask": "${defaultBuildTask}",',
        '  "outFiles": ["${workspaceFolder}/out/**/*.js"]',
        '}',
    ]))
    add(sp(3))
    add(p('Связка <b>tasks.json</b> и <b>launch.json</b> для непрерывной перекомпиляции. Задача <b>watch</b> с флагом <b>isBackground</b> запускается фоново через <b>preLaunchTask</b>. После первой сборки tsc следит за изменениями — достаточно нажать Ctrl+R в Extension Development Host вместо полного F5.'))

    add(sp(4))

    add(h3('4. Логирование в Output Channel вместо console.log'))
    add(p('console.log виден только в Developer Tools Extension Host. Для постоянных логов используйте Output Channel:'))
    add(sp(2))
    add(code([
        '// Создаём глобальный канал один раз',
        'let logger: vscode.OutputChannel;',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    logger = vscode.window.createOutputChannel(\'My Extension\', \'log\');',
        '    context.subscriptions.push(logger);',
        '    log(\'Extension activated\');',
        '}',
        '',
        'export function log(msg: string, level: \'info\'|\'warn\'|\'error\' = \'info\') {',
        '    const ts = new Date().toISOString();',
        '    logger.appendLine(`[${ts}] [${level.toUpperCase()}] ${msg}`);',
        '    if (level === \'error\') logger.show(true);  // показываем при ошибках',
        '}',
        '',
        '// Использование: второй аргумент \'log\' включает structured log viewer в VS Code 1.90+',
    ]))
    add(sp(3))
    add(p('Выделенный Output Channel через <b>createOutputChannel</b> даёт пользователю постоянный доступ к логам расширения из панели Output. Функция-обёртка <b>log()</b> добавляет timestamp и уровень, а при ошибках автоматически открывает канал через <b>logger.show(true)</b>. Второй аргумент <b>\'log\'</b> при создании канала включает встроенную подсветку синтаксиса логов.'))

    add(sp(4))

    add(h3('5. Инспекция Extension Host из браузерных DevTools'))
    add(p('Extension Host — это Node.js процесс. К нему можно подключить полноценный V8 инспектор:'))
    add(sp(2))
    add(code([
        '// launch.json — добавьте к существующей конфигурации',
        '{',
        '  "name": "Attach to Extension Host",',
        '  "type": "node",',
        '  "request": "attach",',
        '  "port": 5870,',
        '  "sourceMaps": true,',
        '  "outFiles": ["${workspaceFolder}/out/**/*.js"]',
        '}',
        '',
        '// Запуск VS Code с инспектором:',
        'code --inspect-extensions=5870 .',
        '',
        '// Или через Developer Tools (Help -> Toggle Developer Tools)',
        '// -> Extension Host tab -> отдельный инспектор',
    ]))
    add(sp(3))
    add(p('Конфигурация <b>launch.json</b> для attach к Extension Host на порту 5870. Флаг <b>--inspect-extensions</b> при запуске VS Code открывает V8 Inspector — к нему можно подключиться из Chrome DevTools или через отдельную конфигурацию отладчика. Даёт доступ к профилированию, heap snapshot и полноценным breakpoints.'))

    add(sp(4))

    add(h3('6. Команда Developer: Show Running Extensions'))
    add(p('Команда <b>Developer: Show Running Extensions</b> показывает все активные расширения с временем активации и потреблением CPU. Незаменима для профилирования:'))
    add(sp(2))
    add(code([
        '// Также из CLI:',
        'code --status',
        '# Выводит: версию VS Code, список расширений, время активации',
        '',
        '// Или в самом расширении:',
        'const ext = vscode.extensions.getExtension(\'publisher.name\');',
        'console.log(`Active: ${ext?.isActive}, exports:`, ext?.exports);',
    ]))
    add(sp(3))
    add(p('Команда <b>code --status</b> из терминала выводит диагностику без открытия GUI. Из кода расширения <b>vscode.extensions.getExtension()</b> позволяет проверить статус активации и получить экспортируемый API конкретного расширения по его идентификатору.'))

    add(sp(6))

    add(h2('Раздел 2: Производительность и архитектура'))
    add(sp(3))

    add(h3('7. Правило: активация > 100ms = плохо'))
    add(p('Стандарт команды VS Code: расширение не должно тратить на активацию более 100ms. Проверьте через Developer: Show Running Extensions:'))
    add(sp(2))
    add(code([
        '// Измерение времени активации в коде',
        'export async function activate(context: vscode.ExtensionContext) {',
        '    const t0 = Date.now();',
        '',
        '    // ... инициализация ...',
        '',
        '    const elapsed = Date.now() - t0;',
        '    if (elapsed > 100) {',
        '        console.warn(`Slow activation: ${elapsed}ms`);',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('Простой замер <b>Date.now()</b> в начале и конце <b>activate()</b>. Если время превышает 100ms — выводится предупреждение в консоль. На практике это первый индикатор того, что инициализация требует оптимизации: вынесения тяжёлых операций в lazy-загрузку.'))

    add(sp(4))

    add(h3('8. Отложенная регистрация провайдеров'))
    add(p('Не регистрируйте все провайдеры сразу — регистрируйте по мере необходимости:'))
    add(sp(2))
    add(code([
        'let completionRegistered = false;',
        '',
        '// Регистрируем completion только при открытии нужного языка',
        'vscode.workspace.onDidOpenTextDocument(doc => {',
        '    if (doc.languageId === \'mylang\' && !completionRegistered) {',
        '        completionRegistered = true;',
        '        context.subscriptions.push(',
        '            vscode.languages.registerCompletionItemProvider(',
        '                \'mylang\', new MyCompletionProvider()',
        '            )',
        '        );',
        '    }',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('Completion-провайдер регистрируется не при активации, а при первом открытии документа нужного языка. Флаг <b>completionRegistered</b> предотвращает повторную регистрацию. Подход сокращает время activate() — провайдер создаётся только когда он реально нужен.'))

    add(sp(4))

    add(h3('9. Кэширование тяжёлых вычислений с инвалидацией'))
    add(p('Паттерн кэша с автоматической инвалидацией при изменении файлов:'))
    add(sp(2))
    add(code([
        'class CachedAnalyzer {',
        '    private cache = new Map<string, { data: AnalysisResult; mtime: number }>();',
        '',
        '    async analyze(uri: vscode.Uri): Promise<AnalysisResult> {',
        '        const key = uri.toString();',
        '        const stat = await vscode.workspace.fs.stat(uri);',
        '',
        '        // Проверяем кэш по времени модификации',
        '        const cached = this.cache.get(key);',
        '        if (cached && cached.mtime === stat.mtime) {',
        '            return cached.data;',
        '        }',
        '',
        '        // Пересчитываем',
        '        const data = await this.runAnalysis(uri);',
        '        this.cache.set(key, { data, mtime: stat.mtime });',
        '        return data;',
        '    }',
        '',
        '    invalidate(uri: vscode.Uri) {',
        '        this.cache.delete(uri.toString());',
        '    }',
        '',
        '    private async runAnalysis(uri: vscode.Uri): Promise<AnalysisResult> {',
        '        // тяжёлая работа здесь',
        '        return {};',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('Кэш по ключу URI с инвалидацией через <b>mtime</b> файла. Метод <b>analyze()</b> сравнивает время модификации через <b>vscode.workspace.fs.stat()</b> — если файл не изменился, возвращает закэшированный результат. Явный метод <b>invalidate()</b> позволяет сбросить кэш программно, например по событию <b>onDidChangeTextDocument</b>.'))

    add(sp(4))

    add(h3('10. Mutex для предотвращения параллельных запусков'))
    add(p('Если ваша операция не должна запускаться параллельно (например, сканирование файлов), используйте простой mutex:'))
    add(sp(2))
    add(code([
        'class Mutex {',
        '    private _locked = false;',
        '    private _queue: Array<() => void> = [];',
        '',
        '    async acquire(): Promise<() => void> {',
        '        if (!this._locked) {',
        '            this._locked = true;',
        '            return () => this._release();',
        '        }',
        '        return new Promise(resolve => {',
        '            this._queue.push(() => resolve(() => this._release()));',
        '        });',
        '    }',
        '',
        '    private _release() {',
        '        if (this._queue.length > 0) {',
        '            const next = this._queue.shift()!;',
        '            next();',
        '        } else {',
        '            this._locked = false;',
        '        }',
        '    }',
        '}',
        '',
        '// Использование',
        'const scanMutex = new Mutex();',
        '',
        'async function scanWorkspace() {',
        '    const release = await scanMutex.acquire();',
        '    try {',
        '        // только один параллельный скан',
        '        await doHeavyScan();',
        '    } finally {',
        '        release();',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('Класс <b>Mutex</b> с внутренней очередью гарантирует эксклюзивный доступ к ресурсу. <b>acquire()</b> возвращает функцию-release; если мьютекс занят — вызов ставится в очередь и ждёт. Паттерн try/finally в <b>scanWorkspace()</b> обеспечивает освобождение даже при ошибке. Применяйте для операций вроде полного сканирования workspace, которые не должны запускаться параллельно.'))
    add(sp(4))

    add(h3('11. Throttle для частых событий редактора'))
    add(p('Throttle (в отличие от debounce) гарантирует выполнение не чаще чем раз в N мс, при этом не теряет последнее событие:'))
    add(sp(2))
    add(code([
        'function throttle<T extends (...args: any[]) => any>(',
        '    fn: T, interval: number',
        '): (...args: Parameters<T>) => void {',
        '    let lastCall = 0;',
        '    let pending: ReturnType<typeof setTimeout> | null = null;',
        '',
        '    return (...args: Parameters<T>) => {',
        '        const now = Date.now();',
        '        const remaining = interval - (now - lastCall);',
        '',
        '        if (remaining <= 0) {',
        '            if (pending) { clearTimeout(pending); pending = null; }',
        '            lastCall = now;',
        '            fn(...args);',
        '        } else if (!pending) {',
        '            // Запланировать последний вызов',
        '            pending = setTimeout(() => {',
        '                lastCall = Date.now();',
        '                pending = null;',
        '                fn(...args);',
        '            }, remaining);',
        '        }',
        '    };',
        '}',
        '',
        '// Обновление декораций не чаще раза в 150ms',
        'const throttledUpdate = throttle(updateDecorations, 150);',
        'vscode.window.onDidChangeTextEditorSelection(e => {',
        '    throttledUpdate(e.textEditor);',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('Универсальная throttle-функция ограничивает частоту вызовов до одного раза в <b>interval</b> мс. Если вызов приходит в пределах интервала — планируется отложенный запуск через <b>setTimeout</b>, чтобы последнее событие не потерялось. В примере throttle применяется к <b>onDidChangeTextEditorSelection</b> для обновления декораций — без него каждое движение курсора вызывало бы перерисовку.'))
    add(sp(6))

    add(h2('Раздел 3: Антипаттерны и типичные ошибки'))
    add(sp(3))

    add(h3('12. Антипаттерн: синхронная работа с файлами'))
    add(p('Никогда не используйте синхронные операции Node.js fs в production-коде расширения:'))
    add(sp(2))
    add(code([
        '// ПЛОХО: ПЛОХО: блокирует Extension Host',
        'const content = fs.readFileSync(\'/path/to/file\', \'utf8\');',
        'const files = fs.readdirSync(\'/path/to/dir\');',
        '',
        '// OK: ХОРОШО: асинхронно через vscode.workspace.fs',
        'const bytes = await vscode.workspace.fs.readFile(uri);',
        'const content = Buffer.from(bytes).toString(\'utf8\');',
        '',
        '// OK: ХОРОШО: через Node.js async API (если нет альтернативы)',
        'const content = await fs.promises.readFile(\'/path/to/file\', \'utf8\');',
    ]))
    add(sp(3))
    add(p('Синхронные <b>readFileSync</b> и <b>readdirSync</b> блокируют Extension Host — все расширения зависают до завершения I/O. Предпочтительно <b>vscode.workspace.fs</b> — работает и с remote-файлами, и с виртуальными FS. Если vscode.workspace.fs не подходит — <b>fs.promises</b> как fallback.'))

    add(sp(4))

    add(h3('13. Антипаттерн: глобальный мутабельный стейт'))
    add(p('Глобальные переменные — источник трудноуловимых багов. Используйте pattern singleton через ExtensionContext:'))
    add(sp(2))
    add(code([
        '// ПЛОХО: ПЛОХО: глобальный стейт',
        'let globalData: any = null;',
        '',
        '// OK: ХОРОШО: всё хранится в context или в объекте расширения',
        'class ExtensionState {',
        '    private static _instance: ExtensionState;',
        '',
        '    private constructor(private context: vscode.ExtensionContext) {}',
        '',
        '    static initialize(ctx: vscode.ExtensionContext) {',
        '        ExtensionState._instance = new ExtensionState(ctx);',
        '    }',
        '',
        '    static get(): ExtensionState {',
        '        if (!ExtensionState._instance) throw new Error(\'Not initialized\');',
        '        return ExtensionState._instance;',
        '    }',
        '',
        '    get data() { return this.context.globalState.get<any>(\'data\'); }',
        '    set data(v: any) { this.context.globalState.update(\'data\', v); }',
        '}',
        '',
        'export function activate(ctx: vscode.ExtensionContext) {',
        '    ExtensionState.initialize(ctx);',
        '}',
    ]))
    add(sp(3))
    add(p('Singleton-класс <b>ExtensionState</b> инкапсулирует всё состояние расширения. Данные хранятся через <b>context.globalState</b> — встроенный key-value storage, который VS Code персистит автоматически. Инициализация через <b>initialize(ctx)</b> в activate() гарантирует единственный экземпляр с доступом к контексту.'))

    add(sp(4))

    add(h3('14. Антипаттерн: игнорирование CancellationToken'))
    add(p('Провайдеры часто вызываются параллельно. Без проверки токена — утечки и лишняя работа:'))
    add(sp(2))
    add(code([
        '// ПЛОХО: ПЛОХО: игнорируем токен отмены',
        'async provideHover(doc, pos, token) {',
        '    const result = await expensiveOp();  // зря считаем, если пользователь ушёл',
        '    return new vscode.Hover(result);',
        '}',
        '',
        '// OK: ХОРОШО: AbortController + CancellationToken',
        'async provideHover(doc, pos, token) {',
        '    const abort = new AbortController();',
        '    token.onCancellationRequested(() => abort.abort());',
        '',
        '    try {',
        '        const result = await expensiveOp({ signal: abort.signal });',
        '        if (token.isCancellationRequested) return null;',
        '        return new vscode.Hover(result);',
        '    } catch (e) {',
        '        if (abort.signal.aborted) return null;',
        '        throw e;',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('Два варианта одного провайдера: без и с проверкой <b>CancellationToken</b>. В правильном варианте <b>AbortController</b> привязан к токену — при отмене запроса тяжёлая операция прерывается через <b>signal</b>. Двойная проверка (signal.aborted + token.isCancellationRequested) страхует от race condition между завершением операции и отменой.'))
    add(sp(4))

    add(h3('15. Антипаттерн: уведомления при активации'))
    add(p('Расширение, показывающее уведомления при старте — один из главных источников низких оценок на Marketplace:'))
    add(sp(2))
    add(code([
        '// ПЛОХО: ПЛОХО: раздражает пользователей',
        'export function activate(ctx) {',
        '    vscode.window.showInformationMessage(\'My Extension activated! Version 2.0!\');',
        '    // или: "Don\'t forget to rate us!"',
        '}',
        '',
        '// OK: ХОРОШО: показываем только релевантные уведомления',
        'export function activate(ctx) {',
        '    const prevVersion = ctx.globalState.get<string>(\'version\');',
        '    const curVersion = ctx.extension.packageJSON.version;',
        '',
        '    if (prevVersion && prevVersion !== curVersion) {',
        '        // Показываем changelog только при реальном обновлении',
        '        const msg = `My Extension обновилось до ${curVersion}`;',
        '        vscode.window.showInformationMessage(msg, \'Что нового?\').then(r => {',
        '            if (r) vscode.env.openExternal(vscode.Uri.parse(CHANGELOG_URL));',
        '        });',
        '    }',
        '    ctx.globalState.update(\'version\', curVersion);',
        '}',
    ]))
    add(sp(3))
    add(p('Правильный подход: уведомление показывается только при реальном обновлении версии. Предыдущая версия хранится в <b>globalState</b> и сравнивается с текущей из <b>packageJSON.version</b>. Кнопка «Что нового?» открывает changelog во внешнем браузере через <b>vscode.env.openExternal()</b>.'))

    add(sp(4))

    add(h3('16. Антипаттерн: keywords > 30 в package.json'))
    add(p('Marketplace отклонит публикацию если ключевых слов больше 30. Частая ошибка при первой публикации:'))
    add(sp(2))
    add(code([
        '// ПЛОХО: 35 ключевых слов — vsce publish упадёт с ошибкой',
        '"keywords": ["vscode", "extension", "typescript", "javascript",',
        '  "python", "react", "vue", "angular", ... (35 слов)]',
        '',
        '// OK: только Go файлы — максимум 30, выбирайте самые значимые',
        '"keywords": ["vscode", "extension", "typescript", "linter"],',
    ]))
    add(sp(3))
    add(p('Marketplace ограничивает <b>keywords</b> до 30 элементов — при превышении <b>vsce publish</b> завершится ошибкой. Указывайте только значимые ключевые слова, которые реально помогают найти расширение через поиск.'))
    add(sp(4))

    add(h3('17. Антипаттерн: неправильная настройка PAT для vsce'))
    add(p('При создании Personal Access Token в Azure DevOps частая ошибка — выбрать конкретную организацию вместо "All accessible organizations":'))
    add(sp(2))
    add(code([
        '# Правильные настройки PAT:',
        '# Organization: All accessible organizations  ← ВАЖНО!',
        '# Scope:        Marketplace (Manage)          ← ТОЛЬКО ЭТО',
        '',
        '# Проверка что PAT работает:',
        'vsce verify-pat -p <ваш-PAT>',
    ]))
    add(sp(3))
    add(p('Критически важно при создании PAT выбрать <b>All accessible organizations</b> — токен с конкретной организацией не будет работать с Marketplace API. Scope должен быть строго <b>Marketplace (Manage)</b>. Команда <b>vsce verify-pat</b> проверяет валидность токена до первой публикации.'))

    add(sp(6))

    add(h2('Раздел 4: Безопасность расширений'))
    add(sp(3))

    add(h3('18. Расширения имеют полный доступ к системе'))
    add(p('В отличие от браузерных расширений, расширения VS Code работают как полноценное Node.js-приложение без sandbox:'))
    add(sp(2))
    for item in [
        'Могут запускать дочерние процессы (child_process.spawn)',
        'Имеют доступ к файловой системе без ограничений',
        'Могут делать сетевые запросы к любым хостам',
        'Могут читать переменные окружения включая секреты',
        'Автоматически обновляются без уведомления пользователя',
    ]:
        add(bul(item))
    add(sp(3))
    add(box('Рекомендации по безопасности',
        'Устанавливайте расширения только от проверенных издателей. '
        'Проверяйте количество загрузок и отзывы. '
        'По возможности выбирайте расширения с открытым исходным кодом. '
        'Не устанавливайте .vsix файлы из неизвестных источников — '
        'они могут содержать вредоносный код даже при показе "verified" бейджа.', 'warn'))
    add(sp(4))

    add(h3('18a. Причины отклонения и удаления расширений из Marketplace'))
    add(p('Microsoft может отклонить публикацию или удалить уже опубликованное расширение. '
          'Документированные причины и известные случаи:'))
    add(sp(3))
    add(tblh(['Причина', 'Детали']))
    add(tbl2([
        ('Сбор данных без согласия',
         'Самая частая причина удаления. В 2022–2025 годах удалены расширения '
         'с миллионами установок за сбор browsing history и данных проекта без явного opt-in. '
         'Правило: всегда проверяйте vscode.env.isTelemetryEnabled и показывайте '
         'явный consent dialog до первой отправки данных'),
        ('Имитация популярных расширений (typosquatting)',
         'Расширения вида "prettier-code", "pylance-ai", "copilot-extension" '
         'систематически удаляются. Некоторые успели набрать 100k+ установок '
         'до обнаружения. Не используйте в имени торговые марки Microsoft, GitHub, '
         'OpenAI без явного разрешения'),
        ('Вредоносный код',
         'Исследование Snyk 2023 выявило 1 283 расширения с потенциально вредоносным кодом '
         'в Marketplace (майнинг, кража токенов, reverse shell). '
         'Microsoft ввела автоматическое сканирование, но часть проходит. '
         'Источник: snyk.io/blog/malicious-vscode-extensions'),
        ('Нарушение Marketplace Terms of Use',
         'Keywords > 30, накрутка оценок, ложное описание функций, '
         'реклама платных услуг без их предоставления. '
         'Полный список запретов: aka.ms/vsmarketplace-ToU'),
        ('Нарушение лицензий зависимостей',
         'Включение GPL-зависимостей в закрытое расширение без соблюдения условий лицензии. '
         'Особенно актуально для расширений использующих LangChain, Tree-sitter, LLVM-инструменты'),
    ]))
    add(sp(4))
    add(box('Как избежать удаления',
        '1. isTelemetryEnabled — всегда проверяйте перед любой отправкой данных. '
        '2. Privacy Policy — обязательна если расширение собирает данные. '
        '3. Уникальное имя — проверьте Marketplace на похожие ID до публикации. '
        '4. Открытый исходный код — снижает риск удаления, пользователи могут аудировать. '
        '5. Changelog — документируйте что именно делает каждая версия.', 'tip'))
    add(sp(4))
    add(code([
        '// ПЛОХО: токены в globalState (хранятся в открытом тексте)',
        'await context.globalState.update(\'apiToken\', token);',
        '',
        '// ПЛОХО: токены в настройках (видны в settings.json)',
        'await vscode.workspace.getConfiguration(\'myExt\').update(\'token\', token);',
        '',
        '// ХОРОШО: SecretStorage — зашифровано ОС (Keychain / Credential Store)',
        'await context.secrets.store(\'apiToken\', token);',
        'const token = await context.secrets.get(\'apiToken\');',
        '',
        '// Слушать изменения секретов (например, при выходе из аккаунта)',
        'context.secrets.onDidChange(e => {',
        '    if (e.key === \'apiToken\') {',
        '        // обновить состояние расширения',
        '    }',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('Три способа хранения токенов — два неправильных и один правильный. <b>globalState</b> и <b>settings</b> хранят данные в открытом тексте на диске. <b>context.secrets</b> использует OS keychain (Keychain Access на macOS, Credential Manager на Windows). Событие <b>onDidChange</b> позволяет реагировать на удаление или обновление секрета из другого процесса.'))

    add(sp(4))

    add(h3('20. Проверка Workspace Trust перед опасными операциями'))
    add(p('Не выполняйте потенциально опасные операции в рабочем пространстве, которому пользователь не доверяет:'))
    add(sp(2))
    add(code([
        '// Проверка доверия к рабочему пространству',
        'if (!vscode.workspace.isTrusted) {',
        '    vscode.window.showWarningMessage(',
        '        \'Эта функция недоступна в ненадёжном рабочем пространстве\'',
        '    );',
        '    return;',
        '}',
        '',
        '// Слушать изменение уровня доверия',
        'vscode.workspace.onDidGrantWorkspaceTrust(() => {',
        '    // активировать функции, требующие доверия',
        '    registerSensitiveProviders();',
        '}, null, context.subscriptions);',
        '',
        '// В package.json — ограничить возможности в недоверенных WS',
        '"capabilities": {',
        '  "untrustedWorkspaces": {',
        '    "supported": "limited",',
        '    "restrictedConfigurations": [',
        '      "myExt.executablePath",',
        '      "myExt.runOnSave"',
        '    ]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('<b>workspace.isTrusted</b> — false в Restricted Mode. Ограничивайте опасные операции (запуск кода, запись файлов) когда workspace не доверенный. <b>onDidGrantWorkspaceTrust</b> срабатывает при явном подтверждении — можно отложить полную активацию до этого момента.'))
    add(sp(6))

    add(h3('18b. Подпись расширений и проверка при установке (VS Code 1.97+)'))
    add(p('С VS Code 1.97 все расширения из Marketplace проходят обязательную проверку подписи при установке. Если подпись не проходит — расширение не устанавливается:'))
    add(sp(2))
    for item in [
        '<b>Автоматическое сканирование секретов</b> — vsce (с 1.101) проверяет .vsix на наличие API-ключей, токенов, паролей при публикации',
        '<b>Trust prompts</b> — при первой установке от неизвестного publisher VS Code показывает диалог подтверждения',
        '<b>Verified publisher badge</b> — требует 6+ месяцев публикации + подтверждение домена',
        '<b>Pricing field</b> — "pricing": "Free" или "Trial" в package.json (для платных расширений)',
    ]:
        add(bul(item))
    add(sp(4))

    add(h2('Раздел 5: Телеметрия и аналитика'))
    add(sp(3))

    add(h3('21. Правила сбора телеметрии'))
    add(p('Официальные требования Microsoft к телеметрии расширений:'))
    add(sp(2))
    for good, bad in [
        ('Используйте @vscode/extension-telemetry для Azure Monitor', 'Не собирайте PII (имена, email, пути файлов)'),
        ('Уважайте vscode.env.isTelemetryEnabled', 'Не игнорируйте выбор пользователя'),
        ('Собирайте минимум данных для понимания поведения', 'Не собирайте больше, чем необходимо'),
        ('Будьте прозрачны: опишите что собираете в README', 'Не скрывайте факт сбора данных'),
    ]:
        add(bul(f'<b>✓ {good}</b>'))
        add(bul(f'<b>✗ {bad}</b>', 2))
    add(sp(4))

    add(h3('22. Правильная реализация телеметрии'))
    add(code([
        '// npm install @vscode/extension-telemetry',
        'import TelemetryReporter from \'@vscode/extension-telemetry\';',
        '',
        'let reporter: TelemetryReporter;',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    // Ключ из Azure Application Insights',
        '    const key = \'your-application-insights-key\';',
        '    reporter = new TelemetryReporter(key);',
        '    context.subscriptions.push(reporter);',
        '',
        '    // Автоматически уважает telemetry.telemetryLevel пользователя',
        '    reporter.sendTelemetryEvent(\'extension.activated\', {',
        '        version: context.extension.packageJSON.version',
        '    });',
        '}',
        '',
        '// Если НЕ используете Application Insights:',
        'function sendCustomTelemetry(event: string, data: object) {',
        '    // Всегда проверяйте разрешение пользователя',
        '    if (!vscode.env.isTelemetryEnabled) return;',
        '    // ваша реализация отправки',
        '}',
        '',
        '// Слушать изменения настройки телеметрии',
        'vscode.env.onDidChangeTelemetryEnabled(enabled => {',
        '    if (!enabled) reporter.dispose();',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('Пакет <b>@vscode/extension-telemetry</b> автоматически уважает настройку <b>telemetry.telemetryLevel</b> пользователя. Для кастомной телеметрии обязательна проверка <b>vscode.env.isTelemetryEnabled</b> перед каждой отправкой. Событие <b>onDidChangeTelemetryEnabled</b> позволяет остановить сбор данных в реальном времени при изменении настроек.'))

    add(sp(6))

    add(h2('Раздел 6: Marketplace и монетизация'))
    add(sp(3))

    add(h3('23. Pre-release версии для ранних тестеров'))
    add(p('С VS Code 1.63+ можно публиковать pre-release версии прямо в Marketplace. Пользователи сами выбирают: stable или pre-release:'))
    add(sp(2))
    add(code([
        '# Публикация pre-release версии',
        'vsce publish --pre-release',
        '',
        '# Версионирование: чётные minor = stable, нечётные = pre-release',
        '# 1.0.x — stable',
        '# 1.1.x — pre-release',
        '# 1.2.x — stable',
        '',
        '# В package.json для pre-release:',
        '"version": "1.1.0",',
        '"preview": true,',
        '"engines": { "vscode": "^1.63.0" },',
    ]))
    add(sp(3))
    add(p('Флаг <b>--pre-release</b> публикует версию в отдельный канал Marketplace. Конвенция версионирования: чётный minor — stable, нечётный — pre-release. Пользователи переключаются между каналами на странице расширения. Поле <b>"preview": true</b> помечает расширение как экспериментальное в интерфейсе.'))

    add(sp(4))

    add(h3('24. Platform-specific VSIX пакеты'))
    add(p('Если ваше расширение содержит нативные бинарники — публикуйте отдельные пакеты для каждой платформы:'))
    add(sp(2))
    add(code([
        '# Публикация для конкретной платформы',
        'vsce publish --target win32-x64',
        'vsce publish --target linux-x64',
        'vsce publish --target darwin-arm64',
        '',
        '# Поддерживаемые target:',
        '# win32-x64, win32-arm64',
        '# linux-x64, linux-arm64, linux-armhf',
        '# darwin-x64, darwin-arm64',
        '# alpine-x64, alpine-arm64',
        '# web',
        '',
        '# В GitHub Actions — матрица платформ',
        'strategy:',
        '  matrix:',
        '    target: [win32-x64, linux-x64, darwin-arm64]',
    ]))
    add(sp(3))
    add(p('Команда <b>vsce publish --target</b> публикует отдельный VSIX для конкретной ОС и архитектуры. VS Code автоматически скачивает нужный пакет. В CI используйте матрицу платформ чтобы собирать и публиковать все варианты за один прогон.'))
    add(sp(4))

    add(h3('25. Расширения Extension Packs'))
    add(p('Extension Pack — это расширение, которое автоматически устанавливает другие расширения. Идеально для стандартизации окружения в команде:'))
    add(sp(2))
    add(code([
        '// package.json Extension Pack',
        '{',
        '  "name": "my-team-pack",',
        '  "displayName": "My Team Extension Pack",',
        '  "description": "Стандартный набор расширений команды",',
        '  "extensionPack": [',
        '    "esbenp.prettier-vscode",',
        '    "ms-vscode.vscode-typescript-next",',
        '    "dbaeumer.vscode-eslint",',
        '    "my-publisher.my-custom-extension"',
        '  ]',
        '}',
        '',
        '// Пользователь устанавливает один пакет — получает всё',
    ]))
    add(sp(3))
    add(p('Поле <b>extensionPack</b> в package.json перечисляет ID расширений для автоустановки. Extension Pack сам по себе не содержит кода — это мета-пакет. Идеально для стандартизации набора инструментов в команде: один install вместо десяти.'))

    add(sp(6))

    add(h2('Раздел 7: Лайфхаки команды VS Code из release notes'))
    add(sp(3))

    add(h3('26. QuickPick.prompt — постоянный текст под полем ввода (VS Code 1.108+)'))
    add(code([
        '// Новый API: prompt под строкой поиска',
        'const qp = vscode.window.createQuickPick();',
        'qp.prompt = \'Введите имя файла (без расширения)\';  // постоянно виден',
        'qp.placeholder = \'Начните вводить...\';',
        'qp.items = await getItems();',
        'qp.show();',
    ]))
    add(sp(3))
    add(p('Новое свойство <b>prompt</b> отображает постоянную подсказку под полем ввода QuickPick — в отличие от <b>placeholder</b>, который исчезает при наборе текста. Используйте prompt для инструкций, а placeholder — для подсказки формата ввода.'))

    add(sp(4))

    add(h3('27. QuickPickItem.resourceUri — автоматические иконки и описания'))
    add(code([
        '// resourceUri автоматически задаёт:',
        '//  - label из имени файла',
        '//  - description из пути',
        '//  - icon из текущей темы иконок',
        'const items: vscode.QuickPickItem[] = files.map(uri => ({',
        '    label: \'\',      // VS Code сам заполнит из uri',
        '    resourceUri: uri,',
        '}));',
    ]))
    add(sp(3))
    add(p('Свойство <b>resourceUri</b> в QuickPickItem автоматически подставляет имя файла как label, путь как description и иконку из текущей темы иконок. Достаточно передать URI — VS Code сделает остальное, обеспечивая единообразие с нативными списками файлов.'))

    add(sp(4))

    add(h3('28. window.title с языком активного файла (VS Code 1.108+)'))
    add(code([
        '// Новая переменная в настройке window.title',
        '"window.title": "${activeEditorLanguageId} - ${activeEditorShort}"',
        '',
        '// В расширении: получить текущий langId',
        'const langId = vscode.window.activeTextEditor?.document.languageId;',
    ]))
    add(sp(3))
    add(p('Переменная <b>${activeEditorLanguageId}</b> в настройке <b>window.title</b> показывает язык текущего файла в заголовке окна. Из кода расширения тот же идентификатор доступен через <b>document.languageId</b> активного редактора.'))

    add(sp(4))

    add(h3('29. Snippet transformations: snakecase и kebabcase (VS Code 1.108+)'))
    add(code([
        '// Новые трансформации в сниппетах',
        '{',
        '  "Snake case filename": {',
        '    "prefix": "snakefile",',
        '    "body": ["${TM_FILENAME/(.*)/${1:/snakecase}/}"]',
        '  },',
        '  "Kebab case word": {',
        '    "prefix": "kebabword",',
        '    "body": ["${TM_CURRENT_WORD/(.*)/${1:/kebabcase}/}"]',
        '  }',
        '}',
        '// MyFileName.ts → my_file_name.ts (snakecase)',
        '// MyFileName.ts → my-file-name.ts (kebabcase)',
    ]))
    add(sp(3))
    add(p('Начиная с VS Code 1.108 в трансформациях сниппетов появились модификаторы <b>snakecase</b> и <b>kebabcase</b>. Применяются к переменным через синтаксис <b>${VAR/(.*)/${1:/snakecase}/}</b>. В примере <b>TM_FILENAME</b> и <b>TM_CURRENT_WORD</b> автоматически конвертируются из CamelCase в нужный формат прямо при вставке сниппета.'))
    add(sp(4))

    add(h3('30. Agent Skills — новый механизм обучения агентов (VS Code 1.108+)'))
    add(p('Agent Skills — папки с инструкциями, которые Copilot загружает автоматически при релевантных запросах:'))
    add(sp(2))
    from book_ui_diagrams import agent_skills_tree
    add(agent_skills_tree())
    add(sp(4))
    add(code([
        '// SKILL.md',
        '# My Skill',
        '## Когда использовать',
        'Использовать этот скилл когда пользователь спрашивает про...',
        '',
        '## Как действовать',
        '1. Шаг первый',
        '2. Шаг второй',
        '',
        '// Включить через настройку:',
        '"chat.useAgentSkills": true',
    ]))
    add(sp(3))
    add(p('Папка <b>.github/skills/</b> содержит инструкции, которые Copilot загружает автоматически при релевантных запросах. Файл <b>SKILL.md</b> описывает когда и как применять скилл, рядом лежат примеры кода и опциональная JSON-схема. Активируется через настройку <b>chat.useAgentSkills</b>.'))

    add(sp(6))

    add(h2('Раздел 8: Продвинутые паттерны из реальных расширений'))
    add(sp(3))

    add(h3('31. Паттерн "вежливого" расширения'))
    add(p('GitLens, Pylance и другие популярные расширения следуют принципу "не навязываться". Вот паттерн из их исходников:'))
    add(sp(2))
    add(code([
        '// Showing welcome walkthrough только один раз',
        'const hasShownWelcome = context.globalState.get<boolean>(\'hasShownWelcome\');',
        'if (!hasShownWelcome) {',
        '    await context.globalState.update(\'hasShownWelcome\', true);',
        '    // Открываем walkthrough, не уведомление',
        '    await vscode.commands.executeCommand(',
        '        \'workbench.action.openWalkthrough\',',
        '        `${context.extension.id}#my-walkthrough`',
        '    );',
        '}',
        '',
        '// Всегда предлагаем отключить функцию',
        '"configuration": {',
        '  "properties": {',
        '    "myExt.showWelcomeOnActivation": {',
        '      "type": "boolean",',
        '      "default": true',
        '    }',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Паттерн «вежливого» расширения: walkthrough вместо уведомления, показ только один раз через флаг в <b>globalState</b>. Команда <b>workbench.action.openWalkthrough</b> открывает встроенный пошаговый гайд. Настройка <b>showWelcomeOnActivation</b> даёт пользователю возможность отключить приветствие.'))

    add(sp(4))

    add(h3('32. Совместное использование состояния между Webview и расширением'))
    add(p('Паттерн из GitLens для двусторонней синхронизации состояния с Webview:'))
    add(sp(2))
    add(code([
        '// Типизированные сообщения для Webview',
        'type ToWebviewMessage =',
        '    | { type: \'init\'; data: InitData }',
        '    | { type: \'update\'; data: UpdateData }',
        '    | { type: \'error\'; message: string };',
        '',
        'type FromWebviewMessage =',
        '    | { type: \'ready\' }',
        '    | { type: \'action\'; payload: ActionPayload };',
        '',
        '// Типизированная отправка',
        'function sendToWebview(panel: vscode.WebviewPanel, msg: ToWebviewMessage) {',
        '    panel.webview.postMessage(msg);',
        '}',
        '',
        '// Типизированная обработка',
        'panel.webview.onDidReceiveMessage((msg: FromWebviewMessage) => {',
        '    switch (msg.type) {',
        '        case \'ready\':',
        '            sendToWebview(panel, { type: \'init\', data: getInitData() });',
        '            break;',
        '        case \'action\':',
        '            handleAction(msg.payload);',
        '            break;',
        '    }',
        '}, undefined, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('Типизированный протокол обмена сообщениями между Webview и расширением. Union-типы <b>ToWebviewMessage</b> и <b>FromWebviewMessage</b> гарантируют корректность на обоих концах. Поле <b>type</b> используется для маршрутизации в switch — Webview сообщает о готовности (<b>ready</b>), расширение отвечает инициализацией (<b>init</b>).'))
    add(sp(4))

    add(h3('33. Реестр команд как сервис-локатор'))
    add(p('Паттерн из популярных расширений для управления командами:'))
    add(sp(2))
    add(code([
        'type CommandHandler = (...args: any[]) => any;',
        '',
        'class CommandRegistry {',
        '    private commands = new Map<string, CommandHandler>();',
        '',
        '    register(id: string, handler: CommandHandler) {',
        '        this.commands.set(id, handler);',
        '        return vscode.commands.registerCommand(id, handler);',
        '    }',
        '',
        '    registerAll(ctx: vscode.ExtensionContext, prefix: string) {',
        '        return [...this.commands.entries()].map(([id, fn]) =>',
        '            vscode.commands.registerCommand(`${prefix}.${id}`, fn)',
        '        );',
        '    }',
        '}',
        '',
        '// В extension.ts',
        'const registry = new CommandRegistry();',
        'registry.register(\'myext.action1\', () => doAction1());',
        'registry.register(\'myext.action2\', () => doAction2());',
        '',
        '// Регистрируем все разом',
        'context.subscriptions.push(...registry.registerAll(context, \'myext\'));',
    ]))
    add(sp(3))
    add(p('<b>registerCommand(id, handler)</b> связывает строковый ID команды с функцией. ID должен совпадать с объявлением в <b>contributes.commands</b> package.json. Возвращаемый Disposable кладут в <b>context.subscriptions</b> — команда снимается автоматически при деактивации.'))
    add(sp(4))

    add(h3('34. Условная активация по файлу конфигурации'))
    add(p('Активировать расширение только если в проекте есть конкретный файл:'))
    add(sp(2))
    add(code([
        '// package.json',
        '"activationEvents": [',
        '  "workspaceContains:**/pyproject.toml",',
        '  "workspaceContains:**/setup.py",',
        '  "workspaceContains:.python-version"',
        ']',
        '',
        '// Множественные паттерны = OR (хотя бы один)',
        '// Расширение активируется если найден ХОТЯ БЫ ОДИН из файлов',
        '',
        '// Для сложных условий — проверяйте в activate():',
        'export async function activate(ctx: vscode.ExtensionContext) {',
        '    const hasPyproject = (await vscode.workspace.findFiles(',
        '        \'**/pyproject.toml\', \'**/node_modules/**\', 1',
        '    )).length > 0;',
        '    ',
        '    if (!hasPyproject) return; // тихо выйти',
        '    registerProviders(ctx);',
        '}',
    ]))
    add(sp(3))
    add(p('Событие <b>workspaceContains</b> активирует расширение при наличии файла по glob-паттерну. Несколько паттернов работают как OR. Для сложной логики — дополнительная проверка через <b>vscode.workspace.findFiles()</b> в activate() с тихим выходом если условие не выполнено.'))

    add(sp(4))

    add(h3('35. Программный запуск других расширений'))
    add(p('Расширения могут использовать API других расширений через экспортируемые публичные API:'))
    add(sp(2))
    add(code([
        '// Получить публичный API другого расширения',
        'const pythonExt = vscode.extensions.getExtension(\'ms-python.python\');',
        'if (!pythonExt) {',
        '    vscode.window.showErrorMessage(\'Требуется Python extension\');',
        '    return;',
        '}',
        '',
        '// Активировать если не активно',
        'if (!pythonExt.isActive) await pythonExt.activate();',
        '',
        '// Использовать публичный API',
        'const pythonApi = pythonExt.exports as PythonApi;',
        'const interpreter = await pythonApi.getActiveEnvironmentPath();',
        '',
        '// В своём расширении — экспортировать API',
        'export function activate(ctx: vscode.ExtensionContext) {',
        '    // Возвращаем публичный API из activate()',
        '    return {',
        '        version: \'1.0.0\',',
        '        doSomething: (input: string) => processInput(input),',
        '    };',
        '}',
    ]))
    add(sp(3))
    add(p('Метод <b>vscode.extensions.getExtension()</b> возвращает ссылку на другое расширение по ID. Вызов <b>activate()</b> гарантирует загрузку, после чего <b>exports</b> содержит публичный API. Чтобы экспортировать собственный API — верните объект из функции <b>activate()</b>.'))

    add(sp(6))

    add(h2('Раздел 9: Инструменты и экосистема'))
    add(sp(3))

    add(h3('36. Полезные инструменты разработчика расширений'))
    add(sp(2))
    add(tblh(['Инструмент', 'Назначение']))
    add(tbl2([
        ('@vscode/vsce',              'CLI для упаковки и публикации расширений'),
        ('ovsx',                      'CLI для публикации в Open VSX Registry'),
        ('@vscode/test-cli',          'Запуск integration tests с VS Code'),
        ('@vscode/extension-telemetry','Телеметрия с Azure Application Insights'),
        ('esbuild',                   'Быстрый бандлер. Рекомендован командой VS Code'),
        ('@vscode/prompt-tsx',        'JSX-синтаксис для создания AI-промптов'),
        ('vscode-languageclient',     'Language Client для LSP-расширений'),
        ('vscode-languageserver',     'Language Server для LSP-расширений'),
        ('@vscode/debugadapter',      'Базовый класс Debug Adapter'),
        ('vscode-uri',               'Работа с URI без зависимости от vscode'),
    ]))
    add(sp(4))

    add(h3('37. Полезные команды для разработчика расширений'))
    add(tblh(['Команда', 'Назначение']))
    add(tbl2([
        ('Developer: Show Running Extensions',     'Список расширений с временем активации'),
        ('Developer: Inspect Extension Host',       'Подключить дебаггер к Extension Host'),
        ('Developer: Toggle Developer Tools',       'Открыть DevTools Extension Host'),
        ('Developer: Reload Window',                'Перезагрузить Extension Development Host'),
        ('Developer: Generate Color Theme From Current Settings', 'Экспорт текущей темы в JSON'),
        ('Developer: Set Log Level',                'Управление уровнем логирования'),
        ('Developer: Open Process Explorer',        'Просмотр процессов VS Code'),
        ('Help: Report Issue',                      'Быстрый репорт бага в VS Code'),
    ]))
    add(sp(4))

    add(h3('38. Тестирование в VS Code Insiders'))
    add(p('Публикуйте в Insiders перед stable для раннего выявления проблем с новым API:'))
    add(sp(2))
    add(code([
        '// .vscode-test.mjs — тест на Insiders',
        'export default defineConfig([',
        '    {',
        '        label: \'stable\',',
        '        files: \'out/test/**/*.test.js\',',
        '        version: \'stable\'',
        '    },',
        '    {',
        '        label: \'insiders\',',
        '        files: \'out/test/**/*.test.js\',',
        '        version: \'insiders\'',
        '    }',
        ']);',
        '',
        '# В CI: запускать оба варианта',
        'vscode-test --label stable',
        'vscode-test --label insiders',
    ]))
    add(sp(3))
    add(p('Конфигурация <b>.vscode-test.mjs</b> с двумя профилями — stable и insiders. Каждый запускает одни и те же тесты на соответствующей версии VS Code. В CI обе конфигурации запускаются через <b>vscode-test --label</b>, чтобы поймать проблемы с новым API до их появления в stable.'))

    add(sp(6))

    add(h2('Раздел 10: Работа с AI и будущее расширений'))
    add(sp(3))

    add(h3('39. Чтение кода популярных расширений'))
    add(p('Лучший способ научиться — читать исходники успешных расширений. Все эти репозитории открыты:'))
    add(sp(2))
    add(tblh(['Расширение', 'Что изучать']))
    add(tbl2([
        ('github.com/gitkraken/vscode-gitlens',  'Сложный Tree View, декорации, Webview, интеграция SCM API'),
        ('github.com/microsoft/vscode-copilot-chat', 'Chat Participant API, Language Model Tools, промпты'),
        ('github.com/microsoft/vscode-python',   'LSP клиент, работа с интерпретаторами, Task Provider'),
        ('github.com/prettier/prettier-vscode',  'Форматтер, настройки, обработка ошибок'),
        ('github.com/microsoft/vscode-extension-samples', 'Официальные примеры для каждого API'),
        ('github.com/eamodio/vscode-gitlens',    '[Историческое зеркало] Репозиторий GitLens до 2022 года, '
                                                  'когда проект перешёл под GitKraken. '
                                                  'Актуальный репозиторий — gitkraken/vscode-gitlens (строка выше). '
                                                  'Ранняя архитектура без modern API — полезно сравнить эволюцию кода'),
    ]))
    add(sp(4))

    add(h3('40. @vscode/prompt-tsx — JSX для AI промптов'))
    add(p('Библиотека от команды VS Code для создания типизированных AI-промптов через JSX. Используется в самом Copilot:'))
    add(sp(2))
    add(code([
        '// npm install @vscode/prompt-tsx',
        'import { PromptElement, renderPrompt } from \'@vscode/prompt-tsx\';',
        '',
        'interface MyPromptProps {',
        '    userQuery: string;',
        '    codeContext: string;',
        '}',
        '',
        '// JSX синтаксис для промпта',
        'class MyPrompt extends PromptElement<MyPromptProps> {',
        '    render() {',
        '        return (',
        '            <>',
        '                <SystemMessage>',
        '                    Ты эксперт по TypeScript. Отвечай кратко.',
        '                </SystemMessage>',
        '                <UserMessage>',
        '                    Код контекста:',
        '                    <CodeBlock language="typescript">',
        '                        {this.props.codeContext}',
        '                    </CodeBlock>',
        '                    Вопрос: {this.props.userQuery}',
        '                </UserMessage>',
        '            </>',
        '        );',
        '    }',
        '}',
        '',
        '// Рендеринг с учётом token budget',
        'const { messages } = await renderPrompt(',
        '    MyPrompt,',
        '    { userQuery, codeContext },',
        '    { modelMaxPromptTokens: 4096 },',
        '    model',
        ');',
    ]))
    add(sp(3))
    add(p('Библиотека <b>@vscode/prompt-tsx</b> позволяет описывать AI-промпты через JSX-компоненты с типизированными пропами. Класс наследуется от <b>PromptElement</b>, метод <b>render()</b> возвращает структуру из <b>SystemMessage</b>, <b>UserMessage</b> и <b>CodeBlock</b>. Функция <b>renderPrompt()</b> автоматически обрезает контент под заданный token budget модели.'))

    add(sp(4))

    add(h3('41. Shell Execution API для агентских расширений'))
    add(p('Новый API для запуска команд в терминале VS Code с отслеживанием вывода — идеален для AI-агентов:'))
    add(sp(2))
    add(code([
        '// Shell Execution API (VS Code 1.93+)',
        'const terminal = vscode.window.createTerminal({',
        '    name: \'My Agent Terminal\',',
        '    shellPath: \'bash\'',
        '});',
        '',
        '// Выполнение с отслеживанием',
        'const execution = await terminal.shellIntegration?.executeCommand(',
        '    \'npm test\'',
        ');',
        '',
        '// Чтение вывода',
        'if (execution) {',
        '    const stream = execution.read();',
        '    for await (const data of stream) {',
        '        // data содержит stdout терминала',
        '        console.log(\'Output:\', data);',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('<b>terminal.shellIntegration?.executeCommand()</b> — Shell Integration API (VS Code 1.93+). Позволяет отслеживать вывод команд в терминале из расширения. Optional chaining <b>?.</b> обязателен: интеграция доступна только когда shell поддерживает её (bash, zsh, fish, PowerShell).'))
    add(sp(4))

    add(h3('42. ESM-модули в расширениях (VS Code 1.100+)'))
    add(p('С VS Code 1.100 расширения поддерживают ES Modules — можно использовать "type": "module" в package.json:'))
    add(sp(2))
    add(code([
        '// package.json',
        '{',
        '  "type": "module",',
        '  "main": "./out/extension.js",',
        '  "engines": { "vscode": "^1.100.0" }',
        '}',
        '',
        '// extension.ts — обычные ES imports',
        'import * as vscode from \'vscode\';',
        'import { analyzeFile } from \'./analyzer.js\';  // .js обязательно!',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    // ...',
        '}',
    ]))
    add(sp(3))
    add(p('ESM в расширениях VS Code работает только для NodeJS Extension Host (не для Web Extensions). Все относительные импорты должны указывать расширение <b>.js</b> — даже если исходник .ts. При бандлинге через esbuild используйте <b>format: "esm"</b> вместо "cjs". Ограничение: <b>require()</b> и динамический <b>import()</b> не работают — только статические импорты.'))
    add(sp(4))

    add(h3('43. Extension Bisect — диагностика проблемных расширений'))
    add(p('Если пользователь жалуется, что ваше расширение "сломало" VS Code — научите его использовать Extension Bisect:'))
    add(sp(2))
    add(code([
        '// Запуск через Command Palette',
        '// > Help: Start Extension Bisect',
        '',
        '// VS Code последовательно отключает половину расширений',
        '// и спрашивает "Проблема осталась?" — бинарный поиск',
        '// За ~5 шагов находит виновника среди 50+ расширений',
        '',
        '// Или программно из вашего расширения:',
        'vscode.commands.executeCommand(\'workbench.action.extensionBisect.start\');',
    ]))
    add(sp(3))
    add(p('Extension Bisect — встроенный бинарный поиск проблемного расширения. Если после bisect ваше расширение оказывается виновником — проверьте <b>Developer: Show Running Extensions</b> на время активации и потребление CPU. Чаще всего причина: долгая активация, утечки памяти в обработчиках событий, или конфликт с другими расширениями через общие ресурсы (форматтеры, Language Server).'))
    add(sp(4))

    add(h3('44. typeof navigator — ловушка Node.js 22 (VS Code 1.101+)'))
    add(p('С VS Code 1.101 Extension Host работает на Node.js 22, где <b>navigator</b> стал глобальным объектом:'))
    add(sp(2))
    add(code([
        '// СЛОМАНО с Node.js 22 — navigator теперь есть и в Node!',
        'if (typeof navigator !== \'undefined\') {',
        '    // Думали что это браузер? Нет — это Node.js',
        '}',
        '',
        '// ПРАВИЛЬНО — проверяем наличие Node.js',
        'const isNode = typeof process === \'object\' && !!process.versions?.node;',
        'const isBrowser = !isNode;',
        '',
        '// Или используйте vscode.env',
        'const isWeb = vscode.env.uiKind === vscode.UIKind.Web;',
    ]))
    add(sp(3))
    add(p('Самый надёжный способ проверить окружение — <b>vscode.env.uiKind</b>: <b>UIKind.Web</b> для vscode.dev/github.dev, <b>UIKind.Desktop</b> для десктопного VS Code. Не полагайтесь на наличие Node.js глобалов — они могут присутствовать или отсутствовать в зависимости от версии.'))
    add(sp(4))

    add(h3('45. Secondary Side Bar для дополнительных панелей (VS Code 1.106+)'))
    add(p('С VS Code 1.106 расширения могут размещать View-контейнеры во второй боковой панели (Secondary Side Bar, справа):'))
    add(sp(2))
    add(code([
        '"contributes": {',
        '  "viewsContainers": {',
        '    // Вместо "activitybar" используем "panel" для правой панели',
        '    "panel": [{',
        '      "id": "myExt.auxiliaryPanel",',
        '      "title": "My Extension Tools",',
        '      "icon": "$(tools)"',
        '    }]',
        '  },',
        '  "views": {',
        '    "myExt.auxiliaryPanel": [{',
        '      "id": "myExt.logs",',
        '      "name": "Logs",',
        '      "type": "webview"  // или обычный tree view',
        '    }]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Secondary Side Bar полезен для вспомогательных панелей, которые не должны конкурировать за место в основной боковой панели. Пользователь может открыть его через <b>View → Secondary Side Bar</b> или горячей клавишей. Типичные применения: логи, предпросмотр, отладочная информация.'))
    add(sp(4))

    add(h3('46. MarkdownString в TreeItem (VS Code 1.106+)'))
    add(p('С VS Code 1.106 TreeItem поддерживает Markdown в tooltip — можно показывать форматированные подсказки:'))
    add(sp(2))
    add(code([
        'class MyTreeItem extends vscode.TreeItem {',
        '    constructor(label: string, version: string, lastUpdate: string) {',
        '        super(label, vscode.TreeItemCollapsibleState.None);',
        '        ',
        '        // Markdown tooltip с форматированием',
        '        const md = new vscode.MarkdownString();',
        '        md.appendMarkdown(`**${label}** v${version}\\n\\n`);',
        '        md.appendMarkdown(`Last updated: *${lastUpdate}*\\n\\n`);',
        '        md.appendCodeblock(\'npm install \' + label, \'bash\');',
        '        md.supportHtml = true;  // разрешить HTML-теги',
        '        this.tooltip = md;',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('MarkdownString в tooltip поддерживает полный Markdown: жирный, курсив, кодовые блоки с подсветкой, ссылки. Флаг <b>supportHtml = true</b> дополнительно разрешает HTML-теги. Это значительно улучшает информативность Tree View без необходимости открывать отдельные панели.'))
    add(sp(4))
    add(screenshot('22-custom-treeview.png', 'Кастомный Tree View: Node Dependencies с иконками и версиями'))
    add(sp(4))
    add(screenshot('22b-treeview-tooltip.png', 'MarkdownString tooltip: форматированная подсказка при hover на элементе Tree View'))
    add(sp(6))

    # Финальная глава
    add(banner('Итог', 'Чек-лист перед публикацией расширения', 'Всё что нужно проверить'), sp(12))

    add(h2('Технический чек-лист'))
    for item in [
        'Активация < 100ms на типичной машине',
        'Нет синхронных файловых операций',
        'Все Disposable добавлены в context.subscriptions',
        'CancellationToken проверяется в провайдерах',
        'Дебаунс/тротл для частых событий редактора',
        'Web-совместимость (если планируется vscode.dev)',
        'Тесты пройдены на stable и insiders VS Code',
        'Bundle оптимизирован с esbuild --production',
        '.vscodeignore настроен, пакет < 5MB',
        'Секреты хранятся в context.secrets, не globalState',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('UX чек-лист'))
    for item in [
        'Нет уведомлений при активации без явного запроса пользователя',
        'Имена команд в формате "My Extension: Action Name"',
        'Иконка PNG 128×128 или 256×256 (не SVG)',
        'Walkthroughs для onboarding новых пользователей',
        'Настройки включают опцию отключения любой навязчивой функции',
        'Activity Bar иконка добавляется только если действительно нужна',
        'Status Bar использован только для постоянно актуальной информации',
        'Уважается Workspace Trust',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Marketplace чек-лист'))
    for item in [
        'README.md с GIF/скриншотами и примерами использования',
        'CHANGELOG.md актуален',
        'keywords ≤ 30 слов',
        'repository.url заполнен (GitHub)',
        'engines.vscode задан с минимальной поддерживаемой версией',
        'categories правильно выбраны',
        'Телеметрия: уважается isTelemetryEnabled пользователя',
        'PAT: "All accessible organizations" + "Marketplace (Manage)"',
        'Опубликовано в Open VSX для совместимости с Cursor',
        'CI/CD настроен для автоматической публикации по тегу',
    ]:
        add(bul(item))
    add(pb())

    # ── ГЛОССАРИЙ ──────────────────────────────────────────────────────────────
    add(toc_ch('Глоссарий'))
    add(banner('Глоссарий', 'Ключевые термины и аббревиатуры', 'Справочник понятий VS Code Extension API'), sp(12))

    add(p('Алфавитный справочник терминов, встречающихся при разработке расширений VS Code.'))
    add(sp(6))

    # glossary: (term, definition, chapter_anchor, chapter_label)
    # chapter_anchor — ключ StableAnchor, chapter_label — текст ссылки
    glossary = [
        ('Activation Event',
         'Событие, при котором VS Code загружает расширение. До события расширение '
         'не занимает ресурсы. Объявляется в package.json. '
         'Примеры: onLanguage:python, onCommand:myext.action, onStartupFinished.',
         'chapter_2', 'Глава 2'),
        ('AMD (Asynchronous Module Definition)',
         'Устаревший формат модулей JavaScript, который VS Code использовал до 2024 года. '
         'Заменён на ESM (ECMAScript Modules). Расширения пока используют CommonJS (require()).',
         'chapter_perf', 'Производительность'),
        ('CancellationToken',
         'Объект, сигнализирующий провайдеру что его результат больше не нужен '
         '(пользователь переключился на другой файл, ввёл следующий символ). '
         'Все Language Provider должны проверять token.isCancellationRequested.',
         'chapter_9', 'Глава 9'),
        ('Chat Participant',
         'Специализированный AI-ассистент в Copilot Chat, вызываемый через @имя. '
         'Регистрируется через vscode.chat.createChatParticipant(). '
         'Получает запрос пользователя и контекст, возвращает ответ в потоке.',
         'chapter_17', 'Глава 17'),
        ('CodeLens',
         'Интерактивные ссылки, отображаемые над строками кода (например «3 references»). '
         'Регистрируется через registerCodeLensProvider(). '
         'Часто используется для показа информации о тестах, git blame, количестве вызовов.',
         'chapter_9', 'Глава 9'),
        ('Codicons',
         'Встроенная библиотека иконок VS Code (600+ иконок). '
         'Используются через синтаксис $(icon-name) в командах, кнопках, Status Bar. '
         'Автоматически адаптируются к цветовой теме. '
         'Каталог: code.visualstudio.com/api/references/icons-in-labels',
         'chapter_4', 'Глава 4'),
        ('CompletionItem',
         'Объект, описывающий один пункт автодополнения: label, kind, insertText, documentation. '
         'Возвращается из провайдера registerCompletionItemProvider(). '
         'CompletionItemKind определяет иконку (Function, Variable, Snippet и др.).',
         'chapter_9', 'Глава 9'),
        ('Contribution Points',
         'Статические объявления расширений в package.json (contributes.*). '
         'Не требуют JavaScript — VS Code читает их при старте. '
         'Примеры: contributes.commands, contributes.views, contributes.themes.',
         'chapter_2', 'Глава 2'),
        ('DAP (Debug Adapter Protocol)',
         'Открытый протокол Microsoft для коммуникации между редактором и отладчиком. '
         'Аналог LSP для отладки. Позволяет одному отладчику работать в любом редакторе.',
         'chapter_10', 'Глава 10'),
        ('Decoration',
         'Визуальная разметка текста в редакторе: фоновый цвет, рамка, иконка в gutter, '
         'inline-текст до/после строки. Создаётся через createTextEditorDecorationType.',
         'chapter_6.5', 'Глава 6.5'),
        ('DiagnosticCollection',
         'Коллекция ошибок и предупреждений, отображаемых в Problems panel. '
         'Создаётся через languages.createDiagnosticCollection(). '
         'set(uri, diagnostics[]) атомарно заменяет все диагностики для файла.',
         'chapter_9', 'Глава 9'),
        ('Disposable',
         'Объект с методом dispose() для освобождения ресурсов. '
         'Все регистрации (команды, провайдеры, листенеры) возвращают Disposable. '
         'Добавляйте в context.subscriptions — VS Code вызовет dispose() при деактивации.',
         'chapter_2', 'Глава 2'),
        ('Document Paste API',
         'API для перехвата операций copy/paste и модификации вставляемого контента. '
         'Доступен с VS Code 1.97. Позволяет трансформировать данные из буфера обмена '
         'при вставке в редактор (например, конвертировать HTML в Markdown).',
         'chapter_9', 'Глава 9'),
        ('Document Selector',
         'Фильтр для языковых провайдеров: определяет для каких документов активен провайдер. '
         'Может быть строкой (languageId), объектом {language, scheme, pattern} или массивом.',
         'chapter_9', 'Глава 9'),
        ('ESM (ECMAScript Modules)',
         'Стандартный формат модулей JavaScript (import/export). '
         'VS Code core перешёл на ESM в 2024 (версия 1.94), что дало +10% к скорости старта. '
         'Расширения пока на CommonJS, переход планируется.',
         'chapter_perf', 'Производительность'),
        ('esbuild',
         'Быстрый JavaScript/TypeScript бандлер, рекомендуемый для расширений VS Code. '
         'Собирает всё дерево зависимостей в один файл. '
         'Ключевые опции: platform: "node", external: ["vscode"], sourcemap: "linked".',
         'chapter_13', 'Глава 13'),
        ('Extension Host',
         'Изолированный Node.js процесс, в котором выполняются все расширения. '
         'С VS Code 2023 — UtilityProcess с V8 sandbox. '
         'Падение расширения не затрагивает UI редактора.',
         'chapter_16', 'Глава 16'),
        ('ExtensionContext',
         'Объект жизненного цикла расширения, передаваемый в activate(context). '
         'Содержит subscriptions (для Disposable), workspaceState, globalState, '
         'secrets (SecretStorage), extensionUri и extensionMode.',
         'chapter_2', 'Глава 2'),
        ('File System Provider',
         'API для создания кастомных виртуальных файловых систем. '
         'registerFileSystemProvider регистрирует схему (например ftp://) '
         'и реализует полный интерфейс FS: read, write, stat, readDirectory.',
         'chapter_8', 'Глава 8'),
        ('FileSystemWatcher',
         'Наблюдатель за изменениями файлов в workspace. '
         'Создаётся через workspace.createFileSystemWatcher(globPattern). '
         'События: onDidCreate, onDidChange, onDidDelete. Не забывайте dispose().',
         'appendix_A', 'Справочник A'),
        ('HoverProvider',
         'Провайдер всплывающих подсказок при наведении курсора на символ. '
         'Регистрируется через registerHoverProvider(). '
         'Возвращает Hover с MarkdownString. Проверяйте token.isCancellationRequested.',
         'chapter_9', 'Глава 9'),
        ('Inlay Hint',
         'Inline-аннотация в редакторе: типы переменных, имена параметров функций. '
         'Появляются как серый текст прямо в коде. registerInlayHintsProvider.',
         'chapter_9', 'Глава 9'),
        ('L10n (Localization)',
         'API локализации расширений VS Code (vscode.l10n). '
         'Заменил устаревший vscode-nls. Строки оборачиваются в vscode.l10n.t("..."). '
         'Инструмент @vscode/l10n-dev извлекает строки и генерирует bundle.l10n.*.json.',
         'chapter_l10n', 'Локализация'),
        ('Language Model API',
         'API для вызова AI-моделей из кода расширения. '
         'vscode.lm.selectChatModels() выбирает доступные LLM (GPT-4o, Claude и др.). '
         'Запрос через model.sendRequest() с массивом LanguageModelChatMessage.',
         'chapter_17', 'Глава 17'),
        ('Language Server',
         'Отдельный процесс, реализующий языковой анализ (completion, diagnostics, hover). '
         'Общается с VS Code по LSP. Изолирован — падение не затрагивает редактор.',
         'chapter_10', 'Глава 10'),
        ('LSP (Language Server Protocol)',
         'Открытый протокол Microsoft для коммуникации между редактором и языковым сервером. '
         'JSON-RPC. Решает M*N проблему: один сервер работает во всех LSP-редакторах. '
         'Спецификация: microsoft.github.io/language-server-protocol',
         'chapter_10', 'Глава 10'),
        ('MCP (Model Context Protocol)',
         'Протокол для интеграции AI-моделей с инструментами. '
         'VS Code поддерживает MCP серверы для расширения возможностей Copilot.',
         'chapter_18', 'Глава 18'),
        ('MessagePort',
         'Web API для прямой IPC-коммуникации между процессами без участия main process. '
         'Используется VS Code для эффективного IPC после перехода на sandbox.',
         'chapter_16', 'Глава 16'),
        ('Monaco Editor',
         'Движок редактора кода, лежащий в основе VS Code. '
         'Доступен как отдельная библиотека (npm: monaco-editor). '
         'Использует кастомное измерение шрифтов через canvas для точного позиционирования курсора.',
         'chapter_perf', 'Производительность'),
        ('Nonce',
         'Случайное значение, использующееся в Content Security Policy Webview '
         'для разрешения конкретного script-тега. Генерируется при каждом создании Webview.',
         'chapter_7', 'Глава 7'),
        ('NotebookSerializer / NotebookController',
         'Компоненты Notebook API. Serializer конвертирует формат файла в NotebookData '
         '(deserialize/serialize). Controller выполняет ячейки и возвращает вывод. '
         'Третий компонент — NotebookRenderer — отвечает за визуализацию rich output.',
         'chapter_notebook', 'Notebook API'),
        ('Open VSX',
         'Открытый реестр расширений для редакторов на базе VS Code: '
         'Cursor, VSCodium, Gitpod, Theia, Eclipse Che. '
         'Управляется Eclipse Foundation. open-vsx.org',
         'chapter_14', 'Глава 14'),
        ('OutputChannel',
         'Канал вывода для логирования в панели Output. '
         'Создаётся через window.createOutputChannel(name). '
         'LogOutputChannel (с 1.74) добавляет уровни: info, warn, error, debug.',
         'chapter_3', 'Глава 3'),
        ('Piece Table',
         'Структура данных для хранения текста в Monaco. '
         'Вставка/удаление за O(log n). Используется вместо обычной строки — '
         'эффективна для частых редактирований больших файлов.',
         'chapter_perf', 'Производительность'),
        ('Proposed API',
         'Нестабильные API VS Code, доступные только в Extension Development Host. '
         'Требуют объявления enabledApiProposals в package.json. '
         'Не допускаются к публикации в Marketplace — только для прототипирования.',
         'chapter_tips', 'Лайфхаки'),
        ('Publisher',
         'Аккаунт издателя на VS Code Marketplace. '
         'Идентификатор расширения: publisher.extensionname. '
         'Создаётся на marketplace.visualstudio.com.',
         'chapter_14', 'Глава 14'),
        ('Quick Pick',
         'Встроенный UI-компонент VS Code для выбора из списка. '
         'showQuickPick() или createQuickPick() для расширенного контроля. '
         'Используйте вместо кастомных диалогов.',
         'chapter_3', 'Глава 3'),
        ('SCM (Source Control Management)',
         'API VS Code для интеграции систем контроля версий. '
         'Встроенный Git реализован через этот же API. '
         'vscode.scm.createSourceControl создаёт провайдер.',
         'chapter_3', 'Глава 3'),
        ('SecretStorage',
         'Зашифрованное хранилище для токенов и credentials. '
         'context.secrets.store/get/delete. '
         'Данные хранятся в OS keychain (Keychain Access, Windows Credential Manager).',
         'chapter_3', 'Глава 3'),
        ('Telemetry',
         'Аналитика использования расширения. '
         'Всегда проверяйте vscode.env.isTelemetryEnabled перед отправкой данных. '
         'Библиотека @vscode/extension-telemetry учитывает этот флаг автоматически. '
         'Никогда не собирайте PII (имена, email, пути файлов).',
         'chapter_tips', 'Лайфхаки'),
        ('TextEdit',
         'Объект, описывающий одно изменение в документе: диапазон + новый текст. '
         'Language провайдеры (форматтеры, code actions) возвращают TextEdit[], '
         'которые VS Code применяет к документу.',
         'chapter_9', 'Глава 9'),
        ('ThemeColor',
         'Ссылка на цвет из активной цветовой темы VS Code. '
         'Используйте вместо hex-значений для автоматической адаптации к теме. '
         'Справочник токенов: code.visualstudio.com/api/references/theme-color',
         'chapter_5', 'Глава 5'),
        ('Tree View',
         'UI-компонент для иерархических данных в боковой панели. '
         'Реализуется через TreeDataProvider. '
         'Используется для Explorer, Source Control, Extensions и кастомных представлений.',
         'chapter_6', 'Глава 6'),
        ('UtilityProcess',
         'Electron API для создания защищённых дочерних процессов с V8 sandbox. '
         'VS Code использует его для Extension Host с версии 1.94 (2024).',
         'chapter_16', 'Глава 16'),
        ('V8 Code Cache',
         'Механизм V8 для сохранения скомпилированного байткода на диск. '
         'При следующем запуске JS парсируется и компилируется не заново. '
         'VS Code принудительно включает кэш с первого запуска (bypassHeatCheck).',
         'chapter_perf', 'Производительность'),
        ('Virtual Document',
         'Документ без физического файла на диске. '
         'Создаётся через registerTextDocumentContentProvider. '
         'URI с кастомной схемой: myscheme:/path/file.ext',
         'chapter_8', 'Глава 8'),
        ('VSIX',
         'Формат пакета расширения VS Code (zip-архив). '
         'Создаётся командой vsce package. '
         'Можно установить через Extensions -> Install from VSIX.',
         'chapter_14', 'Глава 14'),
        ('Walkthrough',
         'Встроенный механизм пошагового онбординга для новых пользователей расширения. '
         'Объявляется через contributes.walkthroughs в package.json. '
         'Открывается через workbench.action.openWalkthrough. '
         'Предпочтительнее уведомлений для первого знакомства с расширением.',
         'chapter_ux', 'UX расширения'),
        ('Webview',
         'iframe внутри VS Code, управляемый расширением. '
         'Может рендерить HTML/CSS/JS. Общается с расширением через postMessage. '
         'Используйте ThemeColor CSS переменные для нативного вида.',
         'chapter_7', 'Глава 7'),
        ('When Clause',
         'Булево выражение, управляющее видимостью команд и меню. '
         'Вычисляется VS Code в реальном времени. '
         'Справочник: code.visualstudio.com/api/references/when-clause-contexts',
         'chapter_4', 'Глава 4'),
        ('WorkspaceState / GlobalState',
         'Key-value хранилища для данных расширения. '
         'workspaceState — данные текущего проекта. '
         'globalState — данные пользователя (между всеми проектами). '
         'Оба доступны через context.workspaceState и context.globalState.',
         'chapter_3', 'Глава 3'),
    ]

    # Render glossary as table with clickable chapter references.
    # Each definition ends with a link to the chapter where the term is discussed.
    add(p('<i>Каждый термин содержит ссылку на раздел книги, где он подробно рассматривается. '
          'В PDF-версии ссылки кликабельны.</i>', 'bodyi'))
    add(sp(4))
    add(tblh(['Термин', 'Определение']))
    glossary_rows = []
    for term, definition, ch_anchor, ch_label in glossary:
        slug = re.sub(r'[^\w]', '_', term[:24])
        anchor_name = f'gloss_{slug}'
        # Term cell: bold + invisible anchor
        term_cell = Paragraph(
            f'<a name="{anchor_name}"/><b>{esc(term)}</b>',
            S['rkey']
        )
        # Definition cell: text + clickable chapter link
        ref_link = (f' <font color="#007ACC"><a href="#{ch_anchor}" color="#007ACC">'
                    f'<u>{esc(ch_label)}</u></a></font>')
        def_cell = Paragraph(definition + ref_link, S['rval'])
        glossary_rows.append([term_cell, def_cell])

    w1, w2 = CW*0.24, CW*0.76
    gt = Table(glossary_rows, colWidths=[w1, w2])
    gt.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0),(-1,-1), [C['lgray'], C['white']]),
        ('TOPPADDING',     (0,0),(-1,-1), 6),
        ('BOTTOMPADDING',  (0,0),(-1,-1), 6),
        ('LEFTPADDING',    (0,0),(-1,-1), 8),
        ('RIGHTPADDING',   (0,0),(-1,-1), 8),
        ('GRID',           (0,0),(-1,-1), 0.3, C['border']),
        ('VALIGN',         (0,0),(-1,-1), 'TOP'),
    ]))
    add(gt)

    return A


if __name__ == '__main__':
    print(f'Part 4 has {len(build_story_part4())} elements')
