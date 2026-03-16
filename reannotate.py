"""
reannotate.py — удаляет все старые аннотации и вставляет новые,
уникальные для каждого кодового блока.
"""
import re

# ── Правила: список (pattern, annotation).
# Первое совпадение по НАИБОЛЕЕ СПЕЦИФИЧНОМУ паттерну побеждает.
# Порядок важен — специфичные паттерны идут первыми.
RULES = [
    # ── Строго специфичные ──────────────────────────────────────────────────
    (r'\bactivate\s*\(.*ExtensionContext',
     '<b>activate()</b> вызывается однажды при первой активации расширения. '
     '<b>context.subscriptions</b> — массив Disposable-объектов: VS Code вызовет '
     '<b>dispose()</b> для каждого при деактивации, предотвращая утечки ресурсов.'),

    (r'registerCommand\b',
     '<b>registerCommand(id, handler)</b> связывает строковый ID команды с функцией. '
     'ID должен совпадать с объявлением в <b>contributes.commands</b> package.json. '
     'Возвращаемый Disposable кладут в <b>context.subscriptions</b> — '
     'команда снимается автоматически при деактивации.'),

    (r'DiagnosticCollection|createDiagnosticCollection',
     '<b>DiagnosticCollection.set(uri, diagnostics[])</b> атомарно заменяет все '
     'диагностики для файла в Problems panel. Вызывайте <b>collection.clear()</b> '
     'при закрытии файла или смене документа чтобы убирать устаревшие ошибки.'),

    (r'registerCompletionItemProvider|CompletionItem\b',
     '<b>CompletionItem</b> описывает один пункт автодополнения: '
     '<b>label</b> — отображаемый текст, <b>kind</b> — иконка (Function/Variable/Class), '
     '<b>insertText</b> — что вставляется. Провайдер вызывается при каждом вводе '
     '— всегда проверяйте <b>CancellationToken</b>.'),

    (r'registerHoverProvider|provideHover|HoverProvider',
     '<b>HoverProvider.provideHover()</b> вызывается когда курсор задерживается над словом. '
     '<b>MarkdownString</b> позволяет использовать Markdown с подсветкой кода в hover-панели. '
     'Проверяйте <b>token.isCancellationRequested</b> — hover отменяется при движении мыши.'),

    (r'TreeDataProvider|getChildren|getTreeItem\b',
     '<b>getChildren(element)</b> возвращает дочерние узлы дерева; '
     'вызов без аргумента означает запрос корневых элементов. '
     '<b>getTreeItem()</b> конвертирует элемент данных в <b>TreeItem</b> с лейблом и иконкой. '
     'EventEmitter в <b>onDidChangeTreeData</b> сигнализирует VS Code об обновлении дерева.'),

    (r'createWebviewPanel\b',
     '<b>createWebviewPanel()</b> создаёт изолированный iframe внутри VS Code. '
     '<b>enableScripts: true</b> разрешает JavaScript (по умолчанию отключено). '
     '<b>localResourceRoots</b> ограничивает доступ к файлам расширения — обязательно для безопасности. '
     'Связь двусторонняя: <b>postMessage()</b> → Webview, <b>onDidReceiveMessage</b> ← Webview.'),

    (r'webview\.html\s*=|getHtml\b|getNonce\b',
     'HTML для Webview генерируется динамически с <b>nonce</b> — случайным значением, '
     'разрешённым в Content Security Policy. Это блокирует выполнение вредоносных скриптов. '
     '<b>webview.asWebviewUri()</b> конвертирует путь к файлу в URI, доступный из iframe.'),

    (r'onDidReceiveMessage|postMessage\b',
     'Двусторонняя связь Webview ↔ расширение: <b>webview.postMessage(data)</b> '
     'отправляет объект в iframe (получается через <b>window.addEventListener("message")</b>). '
     'В обратную сторону — <b>vscode.postMessage()</b> из iframe, '
     'перехватывается через <b>onDidReceiveMessage</b>.'),

    (r'createStatusBarItem|StatusBarAlignment|statusItem\.',
     '<b>createStatusBarItem(alignment, priority)</b> создаёт элемент в строке состояния. '
     '<b>priority</b> определяет позицию: большее число — ближе к центру. '
     'Вызывайте <b>hide()</b> когда расширение неактивно для текущего файла '
     '— Status Bar общий ресурс для всех расширений.'),

    (r'workspace\.getConfiguration|WorkspaceConfiguration',
     '<b>workspace.getConfiguration(section)</b> читает значения из settings.json. '
     '<b>get<T>(key, default)</b> возвращает типизированное значение с fallback. '
     '<b>ConfigurationTarget.Global</b> меняет глобальные настройки пользователя, '
     '<b>Workspace</b> — только настройки текущего проекта.'),

    (r'workspace\.fs\.|vscode\.Uri\.file|FileSystem\b',
     '<b>workspace.fs</b> — абстракция VS Code для работы с файлами. '
     'Используйте её вместо Node.js <b>fs</b> — иначе расширение не работает в '
     'Remote SSH, Dev Containers и vscode.dev. '
     '<b>Uri.file(path)</b> создаёт URI из локального пути.'),

    (r'createTextEditorDecorationType|setDecorations\b',
     '<b>createTextEditorDecorationType()</b> определяет стиль декорации — '
     'фон, рамку, текст до/после строки. Объект создаётся один раз и переиспользуется. '
     '<b>setDecorations(type, ranges)</b> при каждом вызове полностью заменяет '
     'предыдущий набор диапазонов для данного типа.'),

    (r'LanguageClient\b|LanguageClientOptions|ServerOptions',
     '<b>LanguageClient</b> из <b>vscode-languageclient</b> управляет LSP-сервером: '
     'запускает процесс, устанавливает JSON-RPC транспорт, автоматически обрабатывает '
     'initialize/shutdown. <b>DocumentSelector</b> в clientOptions определяет '
     'для каких файлов активен языковой клиент.'),

    (r'withProgress\b|ProgressLocation\b|progress\.report',
     '<b>window.withProgress()</b> показывает индикатор прогресса без блокировки UI. '
     '<b>ProgressLocation.Notification</b> — уведомление с баром; '
     '<b>ProgressLocation.Window</b> — тихий индикатор в Status Bar. '
     '<b>cancellable: true</b> добавляет кнопку Cancel и CancellationToken в callback.'),

    (r'isCancellationRequested|onCancellationRequested|CancellationToken',
     '<b>CancellationToken</b> передаётся во все асинхронные провайдеры VS Code. '
     'Проверяйте <b>token.isCancellationRequested</b> перед дорогостоящими операциями: '
     'пользователь мог закрыть файл, ввести следующий символ. '
     'Игнорирование токена тратит CPU впустую и замедляет редактор.'),

    (r'secrets\.store|secrets\.get\b|SecretStorage',
     '<b>context.secrets</b> — зашифрованное хранилище для токенов и ключей API. '
     'Данные хранятся в системном keychain (macOS Keychain / Windows Credential Store / libsecret). '
     'Никогда не кладите секреты в <b>globalState</b> — он хранится в открытом тексте.'),

    (r'isTelemetryEnabled|TelemetryReporter|sendTelemetryEvent',
     'Проверяйте <b>env.isTelemetryEnabled</b> перед любой отправкой данных — '
     'пользователь мог отключить телеметрию глобально. '
     '<b>@vscode/extension-telemetry</b> учитывает этот флаг автоматически. '
     'Никогда не отправляйте содержимое файлов или имена переменных без явного согласия.'),

    (r'clearTimeout|setTimeout.*clear|debounce\b',
     'Паттерн debounce через <b>setTimeout/clearTimeout</b>: каждый новый вызов '
     'сбрасывает предыдущий таймер — обработчик срабатывает только после паузы в N мс. '
     'Применяется для <b>onDidChangeTextDocument</b> чтобы не запускать анализ при каждом нажатии клавиши.'),

    (r'worker_threads|new Worker\(|parentPort|MessagePort',
     '<b>worker_threads</b> выносят CPU-интенсивные задачи из Extension Host '
     'в отдельный поток, не блокируя UI редактора. '
     '<b>parentPort.postMessage()</b> возвращает результат главному потоку. '
     'С VS Code 1.94 и V8 sandbox важно: native addons в worker требуют совместимых N-API вызовов.'),

    (r'esbuild|external.*vscode|bundle\b',
     'Конфигурация esbuild для VS Code расширения: <b>platform: "node"</b> и '
     '<b>external: ["vscode"]</b> обязательны — модуль vscode предоставляет рантайм, '
     'не включается в бандл. <b>sourcemap: "linked"</b> сохраняет карты для отладки '
     'в Extension Development Host.'),

    (r'ChatParticipant|createChatParticipant|request\.prompt',
     '<b>ChatParticipant</b> добавляет @-упоминание в Copilot Chat. '
     '<b>request.prompt</b> содержит текст после @participant, '
     '<b>request.references</b> — файлы и выделения из редактора. '
     '<b>stream.markdown()</b> отправляет ответ потоком — не ждите полной генерации.'),

    (r'sendRequest.*lm\.|LanguageModelChat|languageModel',
     '<b>vscode.lm.selectChatModels()</b> выбирает доступные LLM (GPT-4o, Claude и др.). '
     '<b>sendRequest(messages, options, token)</b> вызывает модель; '
     'ответ приходит как async iterable — читайте чанками через <b>for await</b> '
     'для streaming отображения.'),

    (r'registerTool|LanguageModelTool|prepareInvocation|ToolResult',
     '<b>lm.registerTool()</b> регистрирует инструмент для агентного режима Copilot. '
     '<b>prepareInvocation()</b> показывает пользователю что именно будет сделано. '
     '<b>invoke()</b> выполняет действие; результат передаётся модели как контекст '
     'для следующего шага рассуждения.'),

    (r'createSourceControl|SourceControl\b|ResourceGroup',
     '<b>createSourceControl(id, label)</b> регистрирует расширение в панели Source Control. '
     '<b>createResourceGroup(id, label)</b> создаёт группу изменений — аналог '
     '"Changes" и "Staged Changes" в Git-расширении. '
     '<b>inputBox.value</b> — текущий текст в поле коммит-сообщения.'),

    (r'authentication\.getSession|AuthenticationProvider|createSession',
     '<b>authentication.getSession(providerId, scopes)</b> запрашивает OAuth-сессию. '
     'VS Code показывает диалог только при <b>createIfNone: true</b>. '
     'Токены кэшируются и обновляются автоматически — не храните их вручную. '
     '<b>onDidChangeSessions</b> уведомляет о logout или смене аккаунта.'),

    (r'isTrusted|onDidGrantWorkspaceTrust',
     '<b>workspace.isTrusted</b> — false в Restricted Mode. '
     'Ограничивайте опасные операции (запуск кода, запись файлов) когда workspace не доверенный. '
     '<b>onDidGrantWorkspaceTrust</b> срабатывает при явном подтверждении — '
     'можно отложить полную активацию до этого момента.'),

    (r'NotebookController|createNotebookController|executeHandler',
     '<b>NotebookController</b> — движок выполнения ячеек. '
     '<b>executeHandler</b> вызывается для каждой ячейки при запуске. '
     '<b>NotebookCellOutput</b> с mime-типом определяет рендер результата: '
     '<b>text/plain</b>, <b>image/png</b> или <b>text/html</b>.'),

    (r'TaskProvider|ShellExecution|ProcessExecution',
     '<b>TaskProvider</b> добавляет задачи в Tasks: Run Task. '
     '<b>ShellExecution(command)</b> запускает команду в shell; '
     '<b>ProcessExecution(path, args)</b> — процесс напрямую без оболочки. '
     '<b>TaskGroup.Build</b> делает задачу доступной через Ctrl+Shift+B.'),

    (r'--vscode-|var\(--vscode',
     'CSS-переменные <b>--vscode-*</b> автоматически обновляются при смене темы. '
     'Используйте их вместо жёстких hex-цветов — иначе Webview сломается '
     'в светлой, High Contrast или кастомной теме. '
     'VS Code добавляет класс <b>vscode-dark</b>/<b>vscode-light</b> на <body>.'),

    (r'xvfb-run|github.*actions|runs-on.*ubuntu',
     '<b>xvfb-run</b> создаёт виртуальный дисплей на Linux-серверах CI — '
     'VS Code требует дисплея для запуска тестов. '
     'Матрица ОС гарантирует кроссплатформенную совместимость расширения. '
     'Секрет <b>VSCE_PAT</b> хранит Personal Access Token для публикации.'),

    (r'vsce package|vsce publish|--pre-release',
     '<b>vsce package</b> упаковывает расширение в .vsix файл для тестирования или установки. '
     '<b>vsce publish</b> публикует в Marketplace; требует PAT с правами Marketplace (Manage). '
     '<b>--pre-release</b> публикует pre-release версию — пользователи с '
     '"Auto Update" получат её только при явном opt-in.'),

    (r'"contributes"\s*:|"activationEvents"\s*:|"engines"\s*:.*vscode',
     'Манифест <b>package.json</b> — статическое описание расширения, читается при старте. '
     '<b>contributes</b> объявляет команды, настройки, меню без загрузки JavaScript. '
     '<b>activationEvents</b> управляет когда загружается код: '
     'используйте конкретные события вместо <b>"*"</b> — это ускоряет старт VS Code.'),

    (r'bookmarkPage|addOutlineEntry|TableOfContents',
     'ReportLab <b>bookmarkPage(key)</b> создаёт именованный PDF-дестинейшн. '
     '<b>TableOfContents</b> рендерит записи как <b>&lt;a href="#key"&gt;</b> '
     'при наличии ключа в notify — формируя кликабельные ссылки в оглавлении.'),

    # ── Контекстные по разделу ──────────────────────────────────────────────
    (r'shellIntegration|executeCommand.*terminal',
     '<b>terminal.shellIntegration?.executeCommand()</b> — Shell Integration API (VS Code 1.93+). '
     'Позволяет отслеживать вывод команд в терминале из расширения. '
     'Optional chaining <b>?.</b> обязателен: интеграция доступна только '
     'когда shell поддерживает её (bash, zsh, fish, PowerShell).'),

    (r'Mutex|mutex|semaphore|_running\s*=',
     'Mutex через флаг <b>_running</b> предотвращает параллельный запуск тяжёлых операций. '
     'Если предыдущий запуск ещё не завершён — новый пропускается. '
     'Паттерн важен для обработчиков <b>onDidChangeTextDocument</b> при быстром вводе.'),

    (r'SnippetString|insertSnippet|tabstop|\$\{[0-9]',
     '<b>SnippetString</b> поддерживает tabstops (<b>$1, $2</b>), '
     'placeholder-значения (<b>${1:default}</b>) и трансформации (<b>${1/(.*)/${1:/upcase}/}</b>). '
     '<b>editor.insertSnippet()</b> вставляет сниппет с полноценной tab-навигацией.'),

    (r'QuickPickItem|showQuickPick|quickPick\.',
     '<b>showQuickPick(items, options)</b> — базовый вариант для простых списков. '
     '<b>window.createQuickPick()</b> даёт полный контроль: обновление items в реальном времени, '
     'кастомные buttons, <b>activeItems</b> для подсветки. '
     '<b>matchOnDescription: true</b> включает поиск по описанию пункта.'),

    (r'registerFileSystemProvider|FileSystemProvider|stat\(|readDirectory',
     '<b>registerFileSystemProvider(scheme, provider)</b> регистрирует кастомную ФС. '
     '<b>stat()</b> возвращает метаданные файла, <b>readDirectory()</b> — список файлов. '
     'VS Code использует вашу ФС прозрачно — открытие, редактирование, сохранение '
     'через стандартный UI работают автоматически.'),

    (r'onDidChangeTextDocument|document\.getText|TextDocumentChangeEvent',
     '<b>workspace.onDidChangeTextDocument</b> срабатывает при каждом изменении в документе. '
     'Событие содержит <b>contentChanges[]</b> — массив изменений с диапазоном и новым текстом. '
     'Обязательно добавляйте debounce — событие генерируется при каждом нажатии клавиши.'),

    (r'InlayHint|registerInlayHintsProvider|InlayHintKind',
     '<b>InlayHint</b> — inline-аннотация в редакторе (типы переменных, имена параметров). '
     '<b>position</b> определяет где появится текст, <b>label</b> — что отображается. '
     '<b>InlayHintKind.Parameter</b> и <b>Type</b> задают визуальный стиль.'),

    # ── Общий fallback (только если совсем нет совпадений выше) ─────────────
    (r'async\s+\w+\s*\(|await\s+\w+|Promise<',
     'Асинхронный код использует <b>async/await</b> для работы с Promise. '
     'Большинство VS Code API возвращают Promise — await обеспечивает '
     'последовательное выполнение без callback-hell. '
     'Добавляйте <b>try/catch</b> для graceful обработки ошибок и отмены.'),
]


def best_annotation(code_text: str, section: str) -> str:
    for pattern, annotation in RULES:
        if re.search(pattern, code_text, re.IGNORECASE):
            return annotation
    return (f'Пример из раздела «{section}». '
            'Используйте <b>context.subscriptions</b> для регистрации всех провайдеров — '
            'VS Code вызовет dispose() при деактивации расширения.')


def strip_old_annotations(text: str) -> str:
    """Remove all previously inserted add(sp(3)) + add(p('...')) after code blocks."""
    # Pattern: optional whitespace, add(sp(3)), newline, add(p('...long annotation...')), newline
    # The annotation paragraphs we inserted are identified by being add(p('...'  with 40+ chars
    # We look for the pattern: after ])) block, sp(3) then p( with our annotation text
    
    # Remove: add(sp(3))\n    add(p('..annotation..'))
    # Only remove if it's one of our auto-generated annotations (contains <b> or is 80+ chars)
    pattern = re.compile(
        r"\n    add\(sp\(3\)\)\n    add\(p\('(?:[^'\\]|\\.){50,}'\)\)",
        re.DOTALL
    )
    cleaned = pattern.sub('', text)
    return cleaned


def annotate_file(filename: str):
    print(f"\n{filename}...")
    text = open(filename, encoding='utf-8').read()

    # Step 1: strip old annotations
    cleaned = strip_old_annotations(text)
    removed = text.count("add(sp(3))") - cleaned.count("add(sp(3))")
    print(f"  Removed {removed} old annotations")

    lines = cleaned.split('\n')
    insertions = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if not re.match(r'\s*add\(code\(\[', line):
            i += 1
            continue

        start = i
        depth = 0
        j = i
        while j < len(lines):
            for ch in lines[j]:
                if ch == '[': depth += 1
                elif ch == ']': depth -= 1
            if j > i and depth <= 0:
                break
            j += 1
        end = j

        # Check next non-empty line — skip if already manually annotated
        after = end + 1
        while after < len(lines) and not lines[after].strip():
            after += 1
        next_line = lines[after].strip() if after < len(lines) else ''
        if re.match(r'add\(p\(|add\(box\(', next_line):
            i = end + 1
            continue

        # Get section context
        section = 'VS Code Extensions'
        for k in range(start - 1, max(0, start - 100), -1):
            hm = re.search(r"add\(h[23]\('([^']+)'\)", lines[k])
            if hm:
                section = hm.group(1)
                break

        # Extract code text
        code_lines = []
        for cl in lines[start:end+1]:
            for s in re.findall(r"'((?:[^'\\]|\\.)*)'", cl):
                code_lines.append(s.replace("\\n","\n").replace("\\'","'"))
        code_text = '\n'.join(code_lines[:30])

        if not code_text.strip():
            i = end + 1
            continue

        annotation = best_annotation(code_text, section)
        insertions.append((end, annotation))
        i = end + 1

    # Apply insertions from end to start
    for end_line, annotation in reversed(insertions):
        insert_at = end_line + 1
        ann_escaped = annotation.replace("'", "\\'")
        lines.insert(insert_at, f"    add(sp(3))")
        lines.insert(insert_at + 1, f"    add(p('{ann_escaped}'))")

    open(filename, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f"  Inserted {len(insertions)} new annotations")


FILES = ['book_part1.py','book_part2.py','book_part3.py','book_part4.py',
         'book_ux.py','book_perf.py','book_new.py']

for fn in FILES:
    annotate_file(fn)
print("\nDone.")
