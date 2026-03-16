from book_helpers import *

def build_story():
    A = []
    def add(*x):
        for i in x: A.append(i)

    def ch(num, title, sub=''):
        part = f'Chapter {num}' if str(num).replace('.','').isdigit() else str(num)
        label = f'{part}: {title}' if str(num).replace('.','').isdigit() else title
        add(StableAnchor(f'chapter_{num}'))
        add(toc_ch(label), banner(part, title, sub), sp(12))

    # Cover and TOC are in front_matter_en.py

    # ── PREFACE ───────────────────────────────────────────────────────────────
    add(toc_ch('Preface'), h1('Preface'), hl(C['blue']), sp(8))
    add(screenshot('sharpen-the-saw.jpg', ''))
    add(sp(6))
    add(quote(
        'Sharpen the saw. Give me six hours to chop down a tree and I will spend the first four sharpening the axe.',
        'Stephen Covey', '7 Habits of Highly Effective People, Habit 7'))
    add(sp(6))
    add(p('VS Code is your primary tool. Extensions are how you sharpen it for your specific needs. This book teaches you to build extensions that turn a code editor into the perfect instrument for your task.'))
    add(sp(6))
    add(p('This guide is a comprehensive reference to the VS Code Extension API. It covers the entire extension developer journey: from creating your first Hello World command to publishing a language server or AI assistant on the Marketplace.'))
    add(sp(4))
    add(p('VS Code has become one of the most popular code editors largely thanks to its open extension platform. Over <b>60,000 extensions</b> are available on the Marketplace — and every single one is built using the same Extension API described here.'))
    add(sp(4))
    add(p('This book is intended for developers familiar with TypeScript/JavaScript and Node.js. The first few chapters cover everything you need to get started.'))
    add(sp(4))
    add(box('About currency',
        'VS Code and the Extension API are updated monthly. This guide is current as of March 2026. For the latest documentation, visit code.visualstudio.com/api',
        'note'))
    add(sp(4))
    add(p('<b>Book structure.</b> Part I (chapters 1-5) covers the fundamentals: your first extension, architecture, commands, themes. Part II (chapters 6-11) dives into UI components and language extensions. Part III (chapters 12-18) covers testing, bundling, publishing, and AI. The Appendix provides complete API reference tables.'))
    add(pb())

    # ── INTRODUCTION ──────────────────────────────────────────────────────────
    add(banner('Introduction', 'VS Code as a Platform', 'History, architecture, and the role of extensions'), sp(12))

    add(h2('The History of Visual Studio Code'))
    add(p('Visual Studio Code was announced by Microsoft at Build 2015. The editor was created as a lightweight yet powerful alternative to full-scale IDEs — designed with web developers and JavaScript/TypeScript in mind.'))
    add(sp(4))
    add(p('From day one, VS Code has been <b>open source</b> under the MIT license and hosted on GitHub. Today, microsoft/vscode is one of the most popular repositories on GitHub. VS Code is built on <b>Electron</b> — every extension runs in a Node.js environment with full access to npm.'))
    add(sp(6))

    add(screenshot('00-full-window.png', 'Visual Studio Code: Activity Bar, Explorer, editor, Status Bar'))
    add(sp(6))

    add(h2('VS Code Architecture'))
    add(p('VS Code consists of several isolated processes:'))
    add(sp(3))
    add(tblh(['Process', 'Description']))
    add(tbl2([
        ('Main Process',       'Electron main — manages windows and lifecycle'),
        ('Renderer Process',   'Chromium renderer — displays the UI'),
        ('Extension Host',     'Separate Node.js process — runs ALL extensions in isolation'),
        ('Language Server',    'Optional process for LSP-based extensions'),
        ('Web Extension Host', 'Browser host for vscode.dev / github.dev'),
    ]))
    add(sp(4))
    add(p('The key architectural decision: <b>extensions never run in the UI process</b>. The Extension Host is isolated — a slow extension cannot freeze the editor. All interaction happens through a strictly defined API.'))
    from book_new import arch_diagram_inject
    for _el in arch_diagram_inject(): add(_el)
    add(sp(6))

    add(h2('What Can an Extension Do?'))
    for item in [
        'add commands to the Command Palette',
        'register new programming languages',
        'create custom panels (Tree View, Webview)',
        'change the appearance: color themes, file icons',
        'add IntelliSense, diagnostics, hover tooltips',
        'integrate with external services',
        'build AI assistants in Copilot Chat',
    ]:
        add(bul(item))
    add(sp(4))
    add(box('Fun fact',
        'Many of VS Code\'s built-in features — TypeScript support, the Node.js debugger, '
        'Git integration — are implemented as extensions using the exact same Extension API.', 'note'))
    add(pb())

    # ── CHAPTER 1 ─────────────────────────────────────────────────────────────
    ch('1', 'Your First Extension', 'Hello World — from zero to launch in 5 minutes')

    add(h2('Prerequisites'))
    add(tblh(['Tool', 'Purpose']))
    add(tbl2([
        ('Node.js 18+',    'Runtime environment; extensions and build tools run in Node.js'),
        ('npm / yarn',     'Package manager for dependencies'),
        ('Git',            'Version control system'),
        ('Visual Studio Code', 'For developing and debugging extensions'),
        ('TypeScript',     'Recommended; type safety significantly simplifies working with the API'),
    ]))
    add(sp(6))

    add(h2('Creating the Project'))
    add(p('Run the Yeoman generator — the official scaffolder for VS Code extensions:'))
    add(sp(3))
    add(code([
        '# Without global installation (recommended)',
        'npx --package yo --package generator-code -- yo code',
        '',
        '# Or install globally',
        'npm install -g yo generator-code',
        'yo code',
    ]))
    add(sp(3))
    add(p('Two ways to run the generator: via <b>npx</b> (nothing installed globally — preferred) or via a global install of <b>yo</b> and <b>generator-code</b>. The result is the same — an interactive wizard for creating an extension project.'))
    from book_new import yeoman_inject
    for _el in yeoman_inject(): add(_el)
    add(p('The generator asks a series of questions. Select <b>New Extension (TypeScript)</b>:'))
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
    add(p('The generator creates a project based on your answers: <b>New Extension (TypeScript)</b> — a template with pre-configured tsconfig, ESLint, and launch.json. The identifier (<b>helloworld</b>) becomes part of the command IDs and folder name. <b>unbundled</b> — no bundler, fine for getting started; for publishing you\'ll need esbuild or webpack (chapter 15).'))

    add(sp(4))
    add(p('The generated project structure:'))
    add(sp(4))
    from book_ui_diagrams import helloworld_tree
    add(helloworld_tree('en'))
    add(sp(6))

    add(h2('Running the Extension'))
    add(p('Open <b>src/extension.ts</b> and press <b>F5</b>. VS Code will compile the TypeScript and open a new window — the <b>Extension Development Host</b>.'))
    add(sp(4))
    add(box('Hot reload',
        'After making changes, run Developer: Reload Window (Ctrl+R) in the Extension Development Host window. '
        'The extension recompiles without a full restart.', 'tip'))
    add(sp(6))

    add(h2('Understanding extension.ts'))
    add(p('Open <b>src/extension.ts</b> — this is the extension\'s entry point:'))
    add(sp(4))
    add(screenshot('09-editor-with-file.png', 'extension.ts — minimal extension code in the VS Code editor'))
    add(sp(4))
    add(p('Let\'s break down each part:'))
    add(sp(3))
    add(code([
        'import * as vscode from \'vscode\';',
        '',
        '// Called once — when the extension is first activated',
        '// context provides access to storage, subscriptions, and file paths',
        'export function activate(context: vscode.ExtensionContext) {',
        '    console.log(\'Extension activated!\');',
        '',
        '    // Register a command handler',
        '    // The command ID must match "command" in package.json -> contributes.commands',
        '    const disposable = vscode.commands.registerCommand(',
        '        \'helloworld.helloWorld\',   // ID from package.json',
        '        () => {                     // Handler — called when the command is executed',
        '            vscode.window.showInformationMessage(\'Hello World!\');',
        '        }',
        '    );',
        '',
        '    // registerCommand returns a Disposable — an object with a dispose() method',
        '    // subscriptions — an array of Disposable objects; VS Code calls dispose()',
        '    // on each one when the extension is deactivated (e.g. VS Code closes)',
        '    context.subscriptions.push(disposable);',
        '}',
        '',
        '// Called on deactivation — for synchronous cleanup (optional)',
        '// For async cleanup, use context.subscriptions',
        'export function deactivate() {}',
    ]))
    add(sp(3))
    add(p('A minimal extension exports two functions: <b>activate()</b> and <b>deactivate()</b>. All logic lives in activate: this is where you register commands, providers, and listeners. Each one returns a <b>Disposable</b> — an object that must be added to <b>context.subscriptions</b> so VS Code automatically releases resources on deactivation. The command ID (<b>helloworld.helloWorld</b>) must exactly match what\'s declared in <b>package.json &rarr; contributes.commands</b> — otherwise the command won\'t work.'))
    add(sp(3))
    add(box('context.subscriptions',
        'Always add commands, listeners, and providers to context.subscriptions. '
        'VS Code will call dispose() on all objects during deactivation. Otherwise — memory leaks.', 'warn'))
    add(sp(6))

    add(h2('Debugging the Extension'))
    add(p('VS Code provides a full-featured debugger for extensions. Set a breakpoint — click the left gutter on a line in extension.ts. Invoke the command — the debugger pauses. All <b>console.log()</b> output is visible in the <b>Debug Console</b> panel of the main window.'))
    add(sp(3))
    add(box('Output Channel',
        'For persistent messages, create: '
        'const ch = vscode.window.createOutputChannel("MyExt"); '
        'ch.appendLine("msg"); ch.show(); — better than console.log for information the user should see.', 'tip'))
    add(pb())

    # ── CHAPTER 2 ─────────────────────────────────────────────────────────────
    ch('2', 'Extension Anatomy', 'Three concepts: Activation Events, Contribution Points, VS Code API')

    add(h2('Three Fundamental Concepts'))
    add(tblh(['Concept', 'Description']))
    add(tbl2([
        ('Activation Events',
         'Define WHEN the extension is loaded. Before the event — it consumes no resources. '
         'Examples: onCommand, onLanguage, onStartupFinished'),
        ('Contribution Points',
         'Static declarations in package.json. Require no code — VS Code reads them at startup. '
         'Examples: contributes.commands, contributes.views, contributes.themes'),
        ('VS Code API',
         'Dynamic JS calls at runtime. '
         'import * as vscode from "vscode". '
         'Examples: vscode.window.*, vscode.workspace.*, vscode.commands.*'),
    ]))
    add(sp(6))

    add(h2('The Extension Manifest — package.json'))
    add(p('Every extension must have a package.json — the manifest. It contains standard Node.js package fields plus VS Code-specific fields:'))
    add(sp(3))
    add(code([
        '{',
        '  "name": "helloworld-sample",',
        '  "version": "0.0.1",',
        '  "description": "My first extension",',
        '  "publisher": "my-publisher",',
        '',
        '  // Minimum VS Code version',
        '  "engines": { "vscode": "^1.90.0" },',
        '',
        '  "main": "./out/extension.js",',
        '  "categories": ["Other"],',
        '  "keywords": ["vscode", "extension"],',
        '  "icon": "images/icon.png",',
        '',
        '  // Activation Events (since VS Code 1.74+, commands activate automatically)',
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
    add(p('A complete extension manifest. The top section contains standard npm package fields (<b>name</b>, <b>version</b>, <b>publisher</b>). The <b>engines.vscode</b> field sets the minimum VS Code version — users on older versions won\'t see the extension in the Marketplace. <b>main</b> points to the compiled JS (not .ts). The <b>activationEvents</b> block defines when to load the code: here the extension activates when a Python file is opened or after VS Code finishes loading. The <b>contributes</b> block registers a command with an icon and binds it to the editor context menu via a <b>when</b> clause.'))
    add(sp(3))
    add(p('<b>What does "$(star)" mean?</b> — the <b>$(icon-name)</b> syntax refers to VS Code\'s built-in '
          'icons called <b>Codicons</b>. Over 600 icons ship with VS Code '
          'and automatically adapt to the current color theme. '
          'They\'re used in commands, buttons, the Status Bar, and Quick Pick.'))
    add(sp(2))
    add(box('Codicons — VS Code built-in icons',
        'Full catalog of all $(icon-name): code.visualstudio.com/api/references/icons-in-labels '
        'or use the "Help: Open Icons Viewer" command directly in VS Code. '
        'Custom SVGs: for Activity Bar, use your own .svg file via '
        '"icon": "./icons/myicon.svg" in viewsContainers. '
        'For editor commands, $(icon-name) is preferred — they always match the VS Code style.',
        'note'))
    add(sp(4))
    add(tblh(['Field', 'Purpose']))
    add(tbl2([
        ('name + publisher',   'Unique extension ID: publisher.name'),
        ('engines.vscode',     'Minimum VS Code version for compatibility'),
        ('main',               'Path to compiled JS — the entry point'),
        ('activationEvents',   'Since VS Code 1.74+, most events are generated automatically'),
        ('contributes',        'All static VS Code extensions'),
        ('icon',               'PNG 128x128. SVG is not supported for published extensions'),
        ('categories',         'AI, Chat, Debuggers, Formatters, Linters, Programming Languages, Themes...'),
    ]))
    add(sp(6))

    add(h2('Capabilities — Compatibility and Trust'))
    add(p('Since VS Code 1.56+, extensions declare capabilities in package.json. Without them, the extension may be silently disabled in certain environments:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"capabilities": {',
        '  // Support for virtual workspaces (vscode.dev, github.dev)',
        '  "virtualWorkspaces": {',
        '    "supported": "limited",',
        '    "description": "File operations work, but terminal commands are not available"',
        '  },',
        '  // Behavior in untrusted workspaces',
        '  "untrustedWorkspace": {',
        '    "supported": "limited",',
        '    "restrictedConfigurations": [',
        '      "myExtension.executable"  // dangerous settings disabled until trust is granted',
        '    ]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Two key declarations. <b>virtualWorkspaces</b> indicates whether the extension works on vscode.dev and github.dev — three options: <b>true</b> (full support), <b>"limited"</b> (partial, with a description of limitations), <b>false</b> (doesn\'t work without a local file system). <b>untrustedWorkspace</b> controls behavior before the user clicks "Trust" — <b>restrictedConfigurations</b> blocks settings that could execute arbitrary code (paths to executables, shell commands). Without these declarations, VS Code may disable the extension in Remote SSH, Dev Containers, or vscode.dev.'))
    add(sp(6))

    add(h2('Activation Events — Full List'))
    add(p('Complete up-to-date list — <a href="#appendix_C"><b>Appendix C</b></a> at the end of the book. '
          'Online: code.visualstudio.com/api/references/activation-events'))
    add(tblh(['Event', 'When it fires']))
    add(tbl2([
        ('onCommand:id',           'On first invocation of the command with the specified ID'),
        ('onLanguage:lang',        'When a file of the specified language is opened (python, typescript...)'),
        ('onView:id',              'When the View with the specified ID is first opened'),
        ('workspaceContains:glob', 'If the workspace contains a file matching the pattern'),
        ('onFileSystem:scheme',    'When a URI with a non-standard scheme is accessed'),
        ('onUri',                  'When a vscode://publisher.name URI is opened'),
        ('onWebviewPanel:type',    'When a Webview panel is restored'),
        ('onCustomEditor:type',    'When a custom editor is opened'),
        ('onDebug',                'When any debug session starts'),
        ('onChatParticipant:id',   'When an AI Chat Participant is invoked'),
        ('onStartupFinished',      'After VS Code is fully loaded — doesn\'t block startup'),
        ('*',                      'AVOID: activates on every VS Code launch'),
    ]))
    add(sp(6))

    add(h2('VS Code API — Namespace Overview'))
    add(p('Up-to-date list: <b>code.visualstudio.com/api/references/vscode-api</b>'))
    add(sp(3))
    add(tblh(['Namespace', 'Purpose']))
    add(tbl2([
        ('vscode.window',     'UI: notifications, input boxes, quick picks, webviews, terminals, status bar'),
        ('vscode.workspace',  'Files: open, configuration, change events, file system'),
        ('vscode.commands',   'Registering and executing commands'),
        ('vscode.languages',  'Language features: completion, hover, diagnostics, formatting'),
        ('vscode.env',        'Environment: clipboard, appName, openExternal'),
        ('vscode.debug',      'Debug management'),
        ('vscode.scm',        'Source Control Management'),
        ('vscode.tasks',      'Task management'),
        ('vscode.auth',       'Authentication: auth tokens'),
        ('vscode.lm',         'Language Models — working with AI'),
        ('vscode.chat',       'Chat API — Chat Participants'),
        ('vscode.tests',      'Testing API — test providers'),
    ]))
    add(sp(4))
    from book_new import q_activation_events
    add(q_activation_events())
    add(sp(4))
    add(pb())
    ch('3', 'Extension Capabilities', 'Working with the editor, text, UI, and storage')

    add(h2('Working with the Editor and Text'))
    add(p('Core text operations are performed through <b>vscode.window.activeTextEditor</b>:'))
    add(sp(3))
    add(code([
        'const editor = vscode.window.activeTextEditor;',
        'if (!editor) return;',
        '',
        '// Getting text',
        'const full    = editor.document.getText();',
        'const line    = editor.document.lineAt(0).text;',
        'const selected= editor.document.getText(editor.selection);',
        '',
        '// Positions and ranges',
        'const pos      = new vscode.Position(lineNum, charNum);',
        'const range    = new vscode.Range(startPos, endPos);',
        'const wordRange= editor.document.getWordRangeAtPosition(pos);',
        '',
        '// Editing',
        'await editor.edit(builder => {',
        '    builder.replace(editor.selection, \'new text\');',
        '    builder.insert(new vscode.Position(0, 0), \'// Header\\n\');',
        '    builder.delete(range);',
        '});',
        '',
        '// Decorations — visual highlighting',
        'const decType = vscode.window.createTextEditorDecorationType({',
        '    backgroundColor: \'rgba(255,200,0,0.3)\',',
        '    border: \'1px solid orange\',',
        '    borderRadius: \'2px\',',
        '});',
        'editor.setDecorations(decType, [range1, range2]);',
        '// Cleanup:',
        'editor.setDecorations(decType, []);',
    ]))
    add(sp(3))
    add(p('Four core editor operations. <b>Reading</b>: getText() without arguments returns the entire document, with a Range or Selection — a fragment. <b>Positions</b>: Position (line, character) and Range (two positions) are the basic types for specifying "where" in a document; getWordRangeAtPosition() is handy for operations on the word under the cursor. <b>Editing</b>: edit() takes a callback with a builder — use it for replace/insert/delete; the call is async and returns true on success. <b>Decorations</b>: createTextEditorDecorationType() creates a type once, setDecorations() applies it to an array of Ranges; to clear, pass an empty array.'))
    add(sp(6))

    add(h2('Notifications and User Input'))
    add(p('VS Code provides several built-in components for user interaction. '
          'Choosing the right type matters — more on this in the UX chapter:'))
    add(sp(3))
    add(code([
        '// Simple notifications (appear in the bottom-right corner)',
        'vscode.window.showInformationMessage(\'Operation complete\');',
        'vscode.window.showWarningMessage(\'Warning\');',
        'vscode.window.showErrorMessage(\'Error!\');',
        '',
        '// With buttons — returns the selected string or undefined',
        'const res = await vscode.window.showInformationMessage(',
        '    \'Reload?\', \'Yes\', \'No\'',
        ');',
        'if (res === \'Yes\') { /* ... */ }',
        '',
        '// InputBox — text input with real-time validation',
        'const name = await vscode.window.showInputBox({',
        '    prompt: \'Enter function name\',',
        '    placeHolder: \'myFunction\',',
        '    validateInput: v => /^\\w+$/.test(v) ? null : \'Letters and digits only\',',
        '});',
        '// name === undefined if the user pressed Escape',
        '',
        '// Quick Pick — searchable selection list',
        '// $(icon-name) — built-in Codicons',
        'const items: vscode.QuickPickItem[] = [',
        '    { label: \'$(cloud-upload) Publish\', description: \'To Marketplace\' },',
        '    { label: \'\', kind: vscode.QuickPickItemKind.Separator },',
        '    { label: \'$(package) Package\', description: \'Create .vsix\' },',
        '];',
        'const pick = await vscode.window.showQuickPick(items, {',
        '    title: \'Extension Action\',',
        '    placeHolder: \'Choose...\',',
        '});',
        '// pick === undefined if the user pressed Escape',
    ]))
    add(sp(3))
    add(p('Three built-in ways to interact with the user. <b>Notifications</b> (showInformation/Warning/ErrorMessage) — appear in the bottom-right corner; with buttons they return the selected option or undefined on Escape. <b>InputBox</b> — single-line input; validateInput is called on every keystroke and displays an error before confirmation. <b>Quick Pick</b> — a searchable list with Separator for grouping; use matchOnDescription to search the description field. All three APIs are async and return undefined on cancel — always check the result.'))
    add(sp(4))
    add(screenshot('07-quick-pick.png', 'Quick Pick: action selection palette (showQuickPick)'))
    add(sp(6))
    add(code([
        '// Progress API — three display modes:',
        '',
        '// 1. ProgressLocation.Window — in the Status Bar (unobtrusive)',
        'await vscode.window.withProgress({',
        '    location: vscode.ProgressLocation.Window,',
        '    title: \'$(sync~spin) Indexing...\',',
        '}, async () => { await buildIndex(); });',
        '',
        '// 2. ProgressLocation.Notification — popup with cancel button',
        'await vscode.window.withProgress({',
        '    location: vscode.ProgressLocation.Notification,',
        '    title: \'Analyzing project\',',
        '    cancellable: true,',
        '}, async (progress, token) => {',
        '    const files = await getFiles();',
        '    for (let i = 0; i < files.length; i++) {',
        '        if (token.isCancellationRequested) break;',
        '        // increment — percentage increase from the last call',
        '        progress.report({',
        '            increment: 100 / files.length,',
        '            message: `${i + 1}/${files.length}: ${files[i]}`,',
        '        });',
        '        await analyzeFile(files[i]);',
        '    }',
        '});',
        '',
        '// 3. ProgressLocation.SourceControl — in the SCM panel',
    ]))
    add(sp(3))
    add(p('Three progress indicators for different scenarios. <b>Window</b> — an unobtrusive spinner in the Status Bar, suitable for background tasks (indexing, syncing). <b>Notification</b> — a visible popup with a progress bar; <b>cancellable: true</b> adds a Cancel button and passes a CancellationToken to the callback — check token.isCancellationRequested in the loop. <b>progress.report({ increment })</b> increases progress by the specified percentage from the previous value, and <b>message</b> updates the text below the title.'))
    add(sp(4))
    add(screenshot('08-notification-center.png', 'Notification Center: notifications and progress'))
    add(sp(6))

    add(h2('Status Bar'))
    add(p('The Status Bar is the bottom strip of the editor. The left side shows global information, '
          'the right side shows contextual info (file language, encoding):'))
    add(sp(4))
    add(screenshot('03-status-bar.png', 'Status Bar: the status strip at the bottom of the editor'))
    add(sp(6))

    add(h2('Data Storage'))
    add(tblh(['API', 'Purpose']))
    add(tbl2([
        ('context.globalState',     'Global key-value store, persisted across sessions'),
        ('context.workspaceState',  'Store for the current workspace'),
        ('context.globalStorageUri','URI of a folder for file-based storage (global)'),
        ('context.storageUri',      'URI of a folder for workspace storage'),
        ('context.secrets',         'Secure encrypted store for tokens'),
    ]))
    add(sp(3))
    add(code([
        '// globalState — read and write',
        'await context.globalState.update(\'lastUsed\', new Date().toISOString());',
        'const last = context.globalState.get<string>(\'lastUsed\');',
        '',
        '// secrets — secure token storage',
        'await context.secrets.store(\'apiToken\', \'my-secret\');',
        'const token = await context.secrets.get(\'apiToken\');',
        'await context.secrets.delete(\'apiToken\');',
        '',
        '// File-based storage',
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
    add(p('Three data storage mechanisms. <b>globalState</b> / <b>workspaceState</b> — key-value stores (get/update), persisted across sessions; globalState is for all projects, workspaceState is for the current one. <b>secrets</b> — encrypted storage for tokens and passwords, data is not visible in settings.json. <b>globalStorageUri</b> — a disk folder for large data (caches, databases); use <b>workspace.fs</b> instead of Node.js fs — otherwise the extension won\'t work in Remote SSH, Dev Containers, or vscode.dev.'))
    add(pb())

    # ── CHAPTER 4 ─────────────────────────────────────────────────────────────
    ch('4', 'Commands, Menus, and Settings', 'Contribution Points — static VS Code extensions')

    add(h2('All Contribution Points'))
    add(p('Full list with descriptions — <a href="#appendix_B"><b>Appendix B</b></a> at the end of the book, '
          'up-to-date online: code.visualstudio.com/api/references/contribution-points'))
    add(sp(3))
    add(tblh(['Contribution Point', 'Purpose']))
    add(tbl2([
        ('contributes.commands',         'Commands with title, category, icon — in the Command Palette'),
        ('contributes.menus',            'Items in context menus and toolbars'),
        ('contributes.keybindings',      'Keyboard shortcuts for commands'),
        ('contributes.configuration',    'Extension settings in the Settings UI'),
        ('contributes.languages',        'Declaring a new programming language'),
        ('contributes.grammars',         'TextMate grammars for syntax highlighting'),
        ('contributes.snippets',         'Code snippets for languages'),
        ('contributes.themes',           'Editor and UI color themes'),
        ('contributes.iconThemes',       'File icon themes'),
        ('contributes.productIconThemes','VS Code UI icon themes'),
        ('contributes.views',            'Tree Views in the sidebar'),
        ('contributes.viewsContainers',  'Containers in the Activity Bar'),
        ('contributes.viewsWelcome',     'Welcome content for empty Views'),
        ('contributes.taskDefinitions',  'Task types for Task Providers'),
        ('contributes.debuggers',        'Debug Adapter: type, label, languages'),
        ('contributes.walkthroughs',     'Step-by-step tutorials on first launch'),
        ('contributes.chatParticipants', 'AI Chat Participants for Copilot'),
        ('contributes.languageModels',   'Custom Language Model providers'),
        ('contributes.customEditors',    'Custom editors for file types'),
        ('contributes.colors',           'New colors for themes'),
        ('contributes.authentication',   'Authentication Provider'),
    ]))
    add(sp(6))

    add(h2('Commands and Context Menus'))
    add(code([
        '"contributes": {',
        '  "commands": [{',
        '    "command": "myext.action",',
        '    "title": "My Extension: Do Something",',
        '    "category": "My Extension",',
        '    "icon": "$(star)"',
        '  }],',
        '  "menus": {',
        '    // Editor context menu',
        '    "editor/context": [{',
        '      "when": "editorHasSelection && resourceLangId == typescript",',
        '      "command": "myext.action",',
        '      "group": "1_modification@1"',
        '    }],',
        '    // Editor title bar (buttons near tabs)',
        '    "editor/title": [{',
        '      "when": "resourceExtname == .md",',
        '      "command": "myext.preview",',
        '      "group": "navigation"',
        '    }],',
        '    // Explorer context menu',
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
    add(p('Commands, menus, and keybindings wired together in a single contributes block. <b>commands</b> declares a command with a category — in the Command Palette it shows as "My Extension: Do Something". <b>menus</b> binds commands to specific UI locations: editor/context (right-click in the editor), editor/title (buttons near tabs), explorer/context (right-click in Explorer). The <b>when</b> clause filters visibility: here the command appears only when text is selected in a TypeScript file. <b>group</b> determines position in the menu: "1_modification@1" means the first section, first item. <b>keybindings</b> sets keyboard shortcuts with a separate mapping for Mac.'))
    add(sp(4))

    add(h3('When Clause Contexts'))
    add(p('When clauses are boolean expressions that control the visibility of commands, menus, and buttons. '
          'VS Code evaluates them in real time whenever the context changes. '
          'Full list of available contexts: '
          '<b>code.visualstudio.com/api/references/when-clause-contexts</b> — '
          'the list is updated with every VS Code release.'))
    add(sp(3))
    add(tblh(['Context', 'Description']))
    add(tbl2([
        ('editorIsOpen',            'At least one editor is open'),
        ('editorHasSelection',      'There is a selection'),
        ('editorTextFocus',         'Focus is in the text editor'),
        ('resourceLangId',          'File language (== typescript, python...)'),
        ('resourceExtname',         'File extension (== .json, .ts...)'),
        ('explorerResourceIsFolder','Selected Explorer item is a folder'),
        ('isInDiffEditor',          'Diff editor is active'),
        ('config.myext.enabled',    'Value of an extension setting'),
    ]))
    add(sp(3))
    add(p('Operators: <b>==</b>, <b>!=</b>, <b>&&</b>, <b>||</b>, <b>!</b>, <b>in</b>, <b>=~</b> (regex). '
          'Example compound condition: '
          '<b>editorTextFocus &amp;&amp; resourceLangId == python &amp;&amp; !isInDiffEditor</b> — '
          'focus is in a Python editor, not in diff mode.'))
    add(sp(6))

    add(h2('Extension Settings'))
    add(p('VS Code generates a full-featured UI from JSON setting declarations. Here is what the Settings UI looks like:'))
    add(sp(4))
    add(screenshot('06-settings-ui.png', 'Settings UI: auto-generated settings interface'))
    add(sp(4))
    add(code([
        '"contributes": {',
        '  "configuration": {',
        '    "title": "My Extension",',
        '    "properties": {',
        '      "myExtension.maxItems": {',
        '        "type": "number", "default": 100,',
        '        "minimum": 1, "maximum": 1000,',
        '        "description": "Maximum number of items"',
        '      },',
        '      "myExtension.format": {',
        '        "type": "string",',
        '        "enum": ["json", "yaml", "toml"],',
        '        "enumDescriptions": ["JSON format", "YAML format", "TOML format"],',
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
    add(p('Extension settings declared for the Settings UI. Each property in <b>properties</b> is a separate setting with a type, default value, and description. VS Code auto-generates the UI: <b>number</b> with min/max — a slider or input field, <b>enum</b> with enumDescriptions — a dropdown, <b>array</b> — an editable list. The key <b>myExtension.maxItems</b> is exactly how the user will see it in settings.json; the prefix before the dot (myExtension) groups all extension settings together.'))

    add(sp(3))
    add(code([
        '// Reading configuration',
        'const cfg = vscode.workspace.getConfiguration(\'myExtension\');',
        'const maxItems = cfg.get<number>(\'maxItems\', 100);',
        'const format   = cfg.get<string>(\'format\',   \'json\');',
        '',
        '// Updating',
        'await cfg.update(\'maxItems\', 200, vscode.ConfigurationTarget.Global);',
        '',
        '// Listening for changes',
        'vscode.workspace.onDidChangeConfiguration(e => {',
        '    if (e.affectsConfiguration(\'myExtension.maxItems\')) {',
        '        // re-read the value',
        '    }',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('<b>workspace.getConfiguration(section)</b> reads values from settings.json. <b>get&lt;T&gt;(key, default)</b> returns a typed value with a fallback. <b>ConfigurationTarget.Global</b> changes the user\'s global settings, <b>Workspace</b> — only the current project\'s settings.'))
    add(pb())

    # ── CHAPTER 5 ─────────────────────────────────────────────────────────────
    ch('5', 'Themes', 'Color Theme, File Icon Theme, Product Icon Theme')

    add(h2('Types of Themes'))
    add(p('Up-to-date list: <b>code.visualstudio.com/api/references/extension-manifest</b>'))
    add(sp(3))
    add(tblh(['Theme Type', 'Description']))
    add(tbl2([
        ('Color Theme',
         'Controls syntax colors (token colors) and UI colors (workbench colors). '
         'uiTheme: vs-dark | vs | hc-black | hc-light'),
        ('File Icon Theme',
         'Icons for files and folders in Explorer, Breadcrumbs, Quick Open. '
         'Examples: Material Icon Theme, vscode-icons'),
        ('Product Icon Theme',
         'VS Code UI icons: buttons, Activity Bar, menus. Available since VS Code 1.50'),
    ]))
    add(sp(6))

    add(h2('Creating a Color Theme'))
    add(p('Users select a theme via <b>Preferences: Color Theme</b> — a Quick Pick with live preview:'))
    add(sp(4))
    add(screenshot('12-color-theme-picker.png', 'Color Theme Picker: switching themes with live preview'))
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
    add(p('Registering a color theme in package.json. <b>uiTheme</b> sets the base: <b>vs-dark</b> for dark, <b>vs</b> for light, <b>hc-black</b> / <b>hc-light</b> for high contrast. A single extension can contain multiple themes — each in a separate JSON file.'))

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
    add(p('A theme file has two parts. <b>colors</b> — VS Code UI colors: editor background, sidebar, tabs, status bar (700+ keys in total — full list in <a href="#appendix_D">Appendix D</a>). <b>tokenColors</b> — syntax colors inherited from TextMate: each rule maps a <b>scope</b> (keyword, string, comment, entity.name.function) to a color and style. Scopes are hierarchical: "keyword" colors all keywords, "keyword.control.flow" colors only if/else/return.'))

    add(sp(4))
    add(box('How to save the current VS Code theme for editing',
        'Open Command Palette -> "Developer: Generate Color Theme From Current Settings". '
        'VS Code will create a JSON file with a complete description of the active theme — all UI colors and syntax tokens. '
        'This is the best way to start a new theme: take an existing theme you like as a base '
        'and tweak the values you want. '
        'The TextMate .tmTheme format is obsolete — modern VS Code themes use JSON directly.',
        'tip'))
    add(sp(6))

    add(h2('File Icon Theme'))
    add(p('A File Icon Theme is a set of icons for files and folders in Explorer. Introduced in VS Code 1.5 (2016). '
          'Users select them via <b>File -> Preferences -> File Icon Theme</b>. '
          'Popular themes: Material Icon Theme (40M+ installs), vscode-icons, Seti. '
          'If you\'re building an extension for a specific language — '
          'add an icon for its files: it noticeably improves the user experience.'))
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
        '    // Key — internal name, iconPath — path to SVG',
        '    "_ts": { "iconPath": "./icons/typescript.svg" },',
        '    "_folder": { "iconPath": "./icons/folder.svg" },',
        '    "_folder_open": { "iconPath": "./icons/folder-open.svg" }',
        '  },',
        '  // Mapping file extensions to icons',
        '  "fileExtensions": { "ts": "_ts", "tsx": "_ts" },',
        '  // Exact file names',
        '  "fileNames": { "package.json": "_npm" },',
        '  // By language ID (languageId from languages contribution)',
        '  "languageIds": { "typescript": "_ts" },',
        '  // Folders: collapsed / expanded',
        '  "folder": "_folder",',
        '  "folderExpanded": "_folder_open",',
        '  "rootFolder": "_folder",',
        '  "rootFolderExpanded": "_folder_open"',
        '}',
    ]))
    add(sp(3))
    add(p('File Icon Theme structure: declaration in package.json + a JSON file with mappings. <b>iconDefinitions</b> is a dictionary of icons with paths to SVGs. Then come the rules: <b>fileExtensions</b> maps file extensions to icons, <b>fileNames</b> matches exact names (package.json, Dockerfile), <b>languageIds</b> matches by registered language. <b>folder</b> / <b>folderExpanded</b> — icons for collapsed and expanded folders.'))
    add(sp(3))
    add(p('<b>Priority hierarchy:</b> fileNames > fileExtensions > languageIds. '
          'If a file is named "package.json", fileNames takes precedence '
          'even if there\'s a match by extension ".json".'))
    add(sp(4))
    add(box('Making SVG icons "native" to VS Code',
        'VS Code applies CSS classes to icons for theme adaptation. '
        'To make icons change with the theme: '
        '1) Use fill="currentColor" or stroke="currentColor" in SVG. '
        '2) Don\'t hardcode colors in SVG — VS Code applies them via CSS. '
        '3) For two variants (dark/light theme), specify "iconDefinitions": '
        '{ "_ts": { "iconPath": "./light.svg" }, "_ts_dark": { "iconPath": "./dark.svg" } } '
        'and "fileExtensions": { "ts": "_ts" } with "light": { "fileExtensions": { "ts": "_ts" } }, '
        '"highContrast": {...}. '
        'Test the result by switching themes in the Extension Dev Host.',
        'tip'))
    add(sp(6))

    add(box('SVGs are banned for the extension icon — but not for UI',
        'The "icon" field in package.json (the icon on the Marketplace and in the Extensions panel) '
        'accepts ONLY PNG 128x128. SVG is rejected when publishing via vsce. '
        'BUT: icons inside the extension (File Icon Theme, Activity Bar, commands) — '
        'can and should be SVG. '
        'TSX/JSX with an <svg> tag inside is just component code — '
        'it\'s not subject to this restriction. '
        'The restriction only applies to the top-level "icon" field in package.json.',
        'warn'))
    add(pb())

    # ── CHAPTER 6 ─────────────────────────────────────────────────────────────
    ch('6', 'Tree View API', 'Custom views in the VS Code sidebar')

    add(h2('Tree View API Overview'))
    add(p('The Tree View API creates hierarchical data views in the sidebar — just like the built-in Explorer, Source Control, and Extensions panels. Three parts: declaration in package.json -> TreeDataProvider implementation -> registration.'))
    add(sp(6))

    add(h2('Step 1: Declaration in package.json'))
    add(code([
        '"contributes": {',
        '  // Container in the Activity Bar',
        '  "viewsContainers": {',
        '    "activitybar": [{',
        '      "id": "myExtension",',
        '      "title": "My Extension",',
        '      "icon": "$(extensions)"',
        '    }]',
        '  },',
        '  // View inside the container',
        '  "views": {',
        '    "myExtension": [{',
        '      "id": "myExt.nodeList",',
        '      "name": "Node Dependencies",',
        '      "icon": "$(package)"',
        '    }],',
        '    // Or in standard containers',
        '    "explorer": [{',
        '      "id": "myExt.quickAccess",',
        '      "name": "Quick Access"',
        '    }]',
        '  },',
        '  // Buttons in the View header',
        '  "menus": {',
        '    "view/title": [{',
        '      "command": "myExt.refresh",',
        '      "when": "view == myExt.nodeList",',
        '      "group": "navigation"',
        '    }],',
        '    // Buttons on items',
        '    "view/item/context": [{',
        '      "command": "myExt.delete",',
        '      "when": "view == myExt.nodeList && viewItem == dependency"',
        '    }]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Three parts of a Tree View declaration. <b>viewsContainers.activitybar</b> adds an icon to the Activity Bar sidebar — this is the container for your Views. <b>views</b> registers specific panels inside the container; you can also place Views in standard containers (explorer, scm, debug). <b>menus</b> with view/title and view/item/context keys add buttons: in the View header (typically Refresh) and on individual items (Delete, Edit). The <b>viewItem == dependency</b> condition in when filters items by contextValue — this lets you show different actions for different types of tree nodes.'))

    add(sp(6))

    add(h2('Step 2: Data Model and TreeDataProvider'))
    add(code([
        'import * as vscode from \'vscode\';',
        'import * as fs from \'fs\';',
        'import * as path from \'path\';',
        '',
        '// Tree item',
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
        '        // contextValue is used in "when" conditions for menus',
        '        this.contextValue = \'dependency\';',
        '    }',
        '}',
        '',
        '// Data provider',
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
        '        return Promise.resolve([]);  // child dependencies',
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
    add(p('<b>getChildren(element)</b> returns the child nodes of the tree; a call without arguments requests root elements. <b>getTreeItem()</b> converts a data element into a <b>TreeItem</b> with a label and icon. The EventEmitter in <b>onDidChangeTreeData</b> signals VS Code to refresh the tree.'))
    add(sp(6))

    add(h2('Step 3: Registration and TreeView'))
    add(code([
        'export function activate(context: vscode.ExtensionContext) {',
        '    const provider = new NodeDependenciesProvider();',
        '',
        '    // createTreeView — more capabilities than registerTreeDataProvider',
        '    const treeView = vscode.window.createTreeView(\'myExt.nodeList\', {',
        '        treeDataProvider: provider,',
        '        showCollapseAll: true,   // "collapse all" button',
        '        canSelectMany: true,     // multi-select',
        '    });',
        '',
        '    // React to item selection',
        '    treeView.onDidChangeSelection(e => {',
        '        console.log(\'Selected:\', e.selection.map(d => d.label));',
        '    });',
        '',
        '    // Programmatic item selection',
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
    add(p('Registration via <b>createTreeView()</b> instead of registerTreeDataProvider gives you a TreeView object with extra capabilities: <b>showCollapseAll</b> adds a "collapse all" button, <b>canSelectMany</b> enables multi-select with Ctrl/Shift. The <b>onDidChangeSelection</b> event lets you react to item selection. The <b>reveal()</b> method programmatically expands and highlights an item — useful for navigating to search results. Both the treeView and the refresh command are registered in context.subscriptions for automatic cleanup.'))
    add(sp(4))
    add(box('DragAndDrop',
        'Since VS Code 1.70+, Tree View supports Drag and Drop via '
        'TreeDragAndDropController. Allows dragging items within and '
        'between views.', 'tip'))
    add(sp(8))
    add(h3('What Tree View Looks Like in the Editor'))
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
        'Tree View is a hierarchical data representation in the VS Code sidebar. '
        'Shown here is the Explorer with extension project files: src/ with TypeScript files, '
        'package.json, tsconfig.json. Similar Tree Views are created via <b>TreeDataProvider</b> '
        'for custom data — dependencies, tasks, bookmarks.',
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
    # caption removed — it floated away from the table
    add(pb())

    # ── CHAPTER 6.5: Decoration API ──────────────────────────────────────────
    ch('6.5', 'Decoration API and Built-in Components',
       'Visual markup in the editor without Webview')

    add(h2('Decoration API — What and Why'))
    add(p('The Decoration API lets you visually highlight text ranges in the editor: '
          'background highlights, borders, text color, gutter icons, inline text. '
          'It\'s <b>much lighter than Webview</b> and fully integrated into the editor DOM.'))
    add(sp(3))
    add(p('Use cases: error highlighting (red background), '
          'secret detection (GitGuardian), coverage lines (green/red gutter), '
          'git blame annotations (GitLens), indent guides (built-in).'))
    add(sp(4))
    add(h3('What Decorations Look Like'))
    add(p('Examples of visual results — background highlighting of a secret and squiggly errors:'))
    add(sp(4))
    add(screenshot('09-editor-with-file.png', 'VS Code editor with syntax highlighting and line numbers'))
    add(sp(6))

    add(h2('Creating and Applying Decorations'))
    add(code([
        '// 1. Create the decoration type (once, on activation)',
        'const secretDecoration = vscode.window.createTextEditorDecorationType({',
        '    // Background',
        '    backgroundColor: "rgba(139, 26, 26, 0.4)",',
        '    border: "1px solid #FF4444",',
        '    borderRadius: "2px",',
        '',
        '    // Gutter icon (left margin)',
        '    gutterIconPath: context.asAbsolutePath("./icons/warning.svg"),',
        '    gutterIconSize: "contain",',
        '',
        '    // Inline text after the line (after pseudo-element)',
        '    after: {',
        '        contentText: "  <- secret detected",',
        '        color: "#FF6666",',
        '        fontStyle: "italic",',
        '        fontSize: "0.85em",',
        '    },',
        '',
        '    // Optional: overviewRuler (scrollbar strip on the right)',
        '    overviewRulerColor: "#FF4444",',
        '    overviewRulerLane: vscode.OverviewRulerLane.Right,',
        '});',
        '',
        '// 2. Apply to the editor',
        'function applyDecorations(editor: vscode.TextEditor) {',
        '    const ranges: vscode.DecorationOptions[] = [];',
        '',
        '    // Search for a pattern in the text',
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
        '// 3. Update on editor change',
        'vscode.window.onDidChangeActiveTextEditor(editor => {',
        '    if (editor) applyDecorations(editor);',
        '}, null, context.subscriptions);',
        '',
        '// 4. Cleanup on deactivation (via Disposable)',
        'context.subscriptions.push(secretDecoration);',
    ]))
    add(sp(3))
    add(p('The full decoration lifecycle in 4 steps. <b>1) Type</b> — createTextEditorDecorationType() describes the visual style: background, border, gutter icon, inline text via the after pseudo-element, overviewRuler marker (right scrollbar strip). Created once on activation. <b>2) Application</b> — the function searches for a pattern in the text (here, API keys like sk-...), converts positions via positionAt(), and passes an array of Ranges to setDecorations(). <b>3) Update</b> — subscribing to onDidChangeActiveTextEditor recalculates decorations when tabs are switched. <b>4) Cleanup</b> — the DecorationType is added to subscriptions; don\'t create a new type on every update — only update the ranges array.'))
    add(sp(6))

    add(h2('Decoration Types'))
    add(tblh(['Property', 'Description']))
    add(tbl2([
        ('backgroundColor',    'Background color of the range. Use rgba() for transparency'),
        ('border / borderRadius', 'Border around the range'),
        ('color',              'Text color inside the range'),
        ('fontWeight / fontStyle', 'Bold and italic'),
        ('textDecoration',     'CSS text-decoration: underline, line-through...'),
        ('gutterIconPath',     'Icon in the left gutter. SVG or PNG'),
        ('before / after',     'Virtual text before/after (contentText, color, fontSize)'),
        ('overviewRulerColor', 'Marker color on the vertical scrollbar on the right'),
        ('isWholeLine',        'True — apply to the entire line, not just the range'),
        ('rangeBehavior',      'Behavior when editing inside the range'),
    ]))
    add(sp(6))

    add(h2('Built-in Editor UI Components'))
    add(p('Before creating a Webview, make sure native components aren\'t sufficient. '
          'They\'re <b>faster, lighter, and better integrated</b> into VS Code:'))
    add(sp(3))
    add(tblh(['Component', 'API and Purpose']))
    add(tbl2([
        ('InputBox',        'showInputBox() — single-line input with validation'),
        ('Quick Pick',      'showQuickPick() — searchable list, multi-select, separators'),
        ('Quick Input',     'createQuickPick() — full control over the Quick Pick panel'),
        ('Message',         'showInformationMessage/Warning/Error — notifications with buttons'),
        ('Progress',        'withProgress() — progress in Notification or Status Bar'),
        ('Status Bar Item', 'createStatusBarItem() — element in the status bar'),
        ('Output Channel',  'createOutputChannel() — output panel (log channel)'),
        ('Terminal',        'createTerminal() — built-in terminal'),
        ('Text Decoration', 'createTextEditorDecorationType() — text highlighting'),
        ('CodeLens',        'registerCodeLensProvider() — links above code lines'),
        ('Hover',           'registerHoverProvider() — hover tooltips'),
        ('InlayHint',       'registerInlayHintsProvider() — inline hints (types, parameter names)'),
    ]))
    add(pb())

    # ── CHAPTER 7 ─────────────────────────────────────────────────────────────
    ch('7', 'Webview API', 'Embedded web pages inside VS Code')

    add(h2('What Is a Webview?'))
    add(p('A Webview is an iframe inside VS Code controlled by an extension. It can render any HTML. It communicates with the extension via messages. Used in three scenarios:'))
    add(sp(2))
    for item in [
        '<b>WebviewPanel</b> — a separate editor tab with custom content',
        '<b>Custom Editor</b> — a custom editor for specific file types',
        '<b>WebviewView</b> — a panel in the sidebar (Sidebar or Panel)',
    ]:
        add(bul(item))
    add(sp(4))
    add(box('When to use Webview?',
        'Webviews are resource-intensive and run in a separate context. Use them only when '
        'the native API is insufficient. First consider TreeView, Decoration API, and '
        'built-in components.', 'warn'))
    add(sp(4))
    add(box('Theme CSS variables — essential for a native look',
        'A Webview is an isolated iframe. Without CSS variables it looks like a foreign website. '
        'Use var(--vscode-editor-background), var(--vscode-button-background), etc. — '
        'they update automatically when the theme changes. '
        'VS Code adds the class vscode-dark / vscode-light / vscode-high-contrast to <body>. '
        'Full variable reference — <a href="#appendix_D">Appendix D</a> at the end of the book.',
        'tip'))
    add(sp(6))

    add(h2('Creating a WebviewPanel'))
    add(code([
        'function createPanel(context: vscode.ExtensionContext) {',
        '    const panel = vscode.window.createWebviewPanel(',
        '        \'myWebview\',',
        '        \'My Dashboard\',',
        '        vscode.ViewColumn.One,',
        '        {',
        '            enableScripts: true,',
        '            retainContextWhenHidden: true,  // don\'t reset when hidden',
        '            localResourceRoots: [',
        '                vscode.Uri.joinPath(context.extensionUri, \'media\')',
        '            ]',
        '        }',
        '    );',
        '',
        '    panel.webview.html = getHtml(panel.webview, context.extensionUri);',
        '',
        '    // Messages from Webview to extension',
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
        '    // Sending from extension to Webview',
        '    panel.webview.postMessage({ command: \'init\', config: { theme: \'dark\' } });',
        '',
        '    panel.onDidDispose(() => console.log(\'Webview closed\'));',
        '}',
    ]))
    add(sp(3))
    add(p('<b>createWebviewPanel()</b> creates an isolated iframe inside VS Code. <b>enableScripts: true</b> enables JavaScript (disabled by default). <b>localResourceRoots</b> restricts access to extension files — mandatory for security. Communication is bidirectional: <b>postMessage()</b> -> Webview, <b>onDidReceiveMessage</b> <- Webview.'))
    add(sp(6))

    add(h2('HTML with Content Security Policy'))
    add(code([
        'function getHtml(webview: vscode.Webview, extUri: vscode.Uri): string {',
        '    // Convert local path to a URI accessible by the Webview',
        '    const scriptUri = webview.asWebviewUri(',
        '        vscode.Uri.joinPath(extUri, \'media\', \'main.js\')',
        '    );',
        '    const styleUri = webview.asWebviewUri(',
        '        vscode.Uri.joinPath(extUri, \'media\', \'style.css\')',
        '    );',
        '    // Nonce for Content Security Policy',
        '    const nonce = [...Array(32)].map(() =>',
        '        \'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\'',
        '            .charAt(Math.floor(Math.random() * 62))',
        '    ).join(\'\');',
        '',
        '    return `<!DOCTYPE html>',
        '    <html lang="en">',
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
        '        <button id="btn">Send Message</button>',
        '        <div id="output"></div>',
        '        <script nonce="${nonce}" src="${scriptUri}"></script>',
        '    </body>',
        '    </html>`;',
        '}',
    ]))
    add(sp(3))
    add(p('The Webview HTML is generated dynamically with a <b>nonce</b> — a random value allowed by the Content Security Policy. This blocks execution of malicious scripts. <b>webview.asWebviewUri()</b> converts a file path to a URI accessible from the iframe.'))
    add(sp(3))
    add(code([
        '// media/main.js — code inside the Webview',
        'const vscode = acquireVsCodeApi();',
        '',
        '// Send to the extension',
        'document.getElementById(\'btn\').addEventListener(\'click\', () => {',
        '    vscode.postMessage({ command: \'alert\', text: \'Hello from Webview!\' });',
        '});',
        '',
        '// Receive from the extension',
        'window.addEventListener(\'message\', event => {',
        '    const { command, items } = event.data;',
        '    if (command === \'data\') {',
        '        document.getElementById(\'output\').textContent =',
        '            JSON.stringify(items);',
        '    }',
        '});',
        '',
        '// Persist state between show/hide',
        'const state = vscode.getState() || { count: 0 };',
        'function save(newState) { vscode.setState(newState); }',
    ]))
    add(sp(3))
    add(p('Bidirectional communication Webview <-> extension: <b>webview.postMessage(data)</b> sends an object to the iframe (received via <b>window.addEventListener("message")</b>). In the other direction — <b>vscode.postMessage()</b> from the iframe, intercepted via <b>onDidReceiveMessage</b>.'))
    add(sp(4))
    add(box('Content Security Policy (CSP)',
        'ALWAYS set a strict CSP. Without it, the Webview is vulnerable to XSS attacks. '
        'Use a nonce for every script tag. '
        'default-src \'none\' is a good baseline. '
        'Important: this matters beyond just security — VS Code has a Web version '
        '(vscode.dev, github.dev, code-server). There, the Webview runs in a real browser '
        'and CSP is strictly enforced by the Chromium engine. '
        'An extension without CSP or with unsafe-inline may not work at all in the Web version. '
        'Test your extension on vscode.dev if you plan to support Web Extensions.',
        'warn'))
    add(pb())

    # ── CHAPTER 8 ─────────────────────────────────────────────────────────────
    ch('8', 'Custom Editors and Virtual Documents', 'Custom editors for non-standard formats')

    add(h2('Custom Text Editor'))
    add(p('A Custom Editor lets you provide your own UI for editing files. When a user opens a file, VS Code can use your editor instead of the default text editor.'))
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
    add(p('Custom editor declaration. <b>viewType</b> is a unique ID used when registering the provider. <b>selector</b> with filenamePattern defines which files the editor is available for. <b>priority: "option"</b> — the editor is offered as an alternative (via "Open With..."); <b>"default"</b> — it opens automatically instead of the standard text editor.'))

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
        '        // Document -> Webview',
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
        '        // Webview -> Document',
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
        '// Registration',
        'context.subscriptions.push(',
        '    vscode.window.registerCustomEditorProvider(',
        '        \'myext.jsonVisual\',',
        '        new JsonEditorProvider()',
        '    )',
        ');',
    ]))
    add(sp(3))
    add(p('Custom Text Editor implementation. The <b>resolveCustomTextEditor()</b> method receives a TextDocument (the standard VS Code model) and a WebviewPanel — your UI. The key task is two-way synchronization: when the document changes (onDidChangeTextDocument), update the Webview via postMessage; when edits happen in the Webview (onDidReceiveMessage), update the document via WorkspaceEdit. Important: VS Code itself manages save and undo/redo for the TextDocument — your editor gets this for free. Registration via registerCustomEditorProvider links the viewType from package.json to the provider.'))
    add(sp(6))

    add(h2('Virtual Documents'))
    add(p('Virtual Documents are files that exist only in memory, with no physical file on disk. '
          'VS Code opens them via a custom URI scheme (<b>myscheme:/path/file.md</b>), '
          'displays them in the editor like a regular file, but reads the content from your provider.'))
    add(sp(3))
    add(h3('Real-World Examples'))
    for item in [
        '<b>MongoDB for VS Code</b> — when opening a JSON document from the database, '
        'the extension creates a Virtual Document with a URI like <b>mongodb:/collection/doc_id.json</b>. '
        'The user edits JSON directly in the editor, the extension intercepts saves '
        'and updates the document in MongoDB',
        '<b>Git Diff</b> (built-in) — HEAD~1 files are opened as virtual documents '
        'with the <b>git:/path/to/file</b> scheme',
        '<b>decompiled.code</b> (Java/Kotlin) — "Go to Definition" opens the decompiled '
        'source of a .class file as a virtual .java document (scheme <b>jdt:/</b>)',
        '<b>REST Client</b> — the HTTP response is displayed as a virtual .json document',
        '<b>SVG Preview</b> and similar — preview panel with rendering without modifying the original',
    ]:
        add(bul(item))
    add(sp(4))
    add(code([
        '// 1. Implement the provider',
        'const provider: vscode.TextDocumentContentProvider = {',
        '    // EventEmitter allows refreshing the document content',
        '    onDidChange: onDidChangeEmitter.event,',
        '',
        '    // Called when VS Code wants the document text',
        '    provideTextDocumentContent(uri: vscode.Uri): string {',
        '        // uri.path contains the path, uri.query — query parameters',
        '        const docId = uri.path.replace(\'/\', \'\');',
        '        const data = myDatabase.getDocument(docId);',
        '        return JSON.stringify(data, null, 2);',
        '    }',
        '};',
        '',
        '// 2. Register the scheme (once on activation)',
        'const reg = vscode.workspace.registerTextDocumentContentProvider(',
        '    \'mongodb\',  // scheme — the part of the URI before ://',
        '    provider',
        ');',
        'context.subscriptions.push(reg);',
        '',
        '// 3. Open the virtual document',
        'const uri = vscode.Uri.parse(`mongodb:/users/${docId}.json`);',
        'const doc = await vscode.workspace.openTextDocument(uri);',
        'await vscode.window.showTextDocument(doc, {',
        '    preview: false,  // open as a permanent tab, not preview',
        '});',
        '',
        '// 4. Intercept save (onWillSaveTextDocument)',
        'vscode.workspace.onWillSaveTextDocument(e => {',
        '    if (e.document.uri.scheme !== \'mongodb\') return;',
        '    const updated = JSON.parse(e.document.getText());',
        '    const docId = e.document.uri.path.replace(\'/\', \'\').replace(\'.json\', \'\');',
        '    // e.waitUntil() blocks saving until the promise resolves',
        '    e.waitUntil(myDatabase.updateDocument(docId, updated));',
        '});',
        '',
        '// 5. Refresh content when the database changes',
        'onDidChangeEmitter.fire(uri);  // triggers another call to provideTextDocumentContent',
    ]))
    add(sp(3))
    add(p('The complete Virtual Document lifecycle in 5 steps. <b>1)</b> TextDocumentContentProvider with provideTextDocumentContent — returns the content string for a URI. <b>2)</b> Registration of a custom scheme (mongodb://) — VS Code will call the provider for any URI with this scheme. <b>3)</b> Opening via openTextDocument(uri) + showTextDocument() — the file appears in the editor as a regular tab. <b>4)</b> Intercepting save via onWillSaveTextDocument — e.waitUntil() blocks saving until the promise resolves (here, writing to the database). <b>5)</b> Refresh: fire(uri) via the EventEmitter triggers another provideTextDocumentContent call.'))
    add(sp(3))
    add(p('<b>Virtual Document limitations:</b> they are read-only by default. '
          'For editable virtual files, you need a full <b>FileSystemProvider</b> '
          '(registerFileSystemProvider) — it implements the entire file system interface: '
          'read, write, stat, readDirectory, etc.'))
    add(pb())

    # ── CHAPTER 9 ─────────────────────────────────────────────────────────────
    ch('9', 'Language Extensions', 'Syntax, snippets, IntelliSense, diagnostics')

    add(h2('Declarative vs Programmatic Approach'))
    add(tblh(['Approach', 'Description and Examples']))
    add(tbl2([
        ('Declarative',
         'Declared in package.json without code. '
         'Syntax highlighting (TextMate), snippets, language configuration'),
        ('Programmatic',
         'Implemented via the vscode.languages.* API. '
         'Completion, hover, diagnostics, formatting, code actions, rename, go-to-definition'),
    ]))
    add(sp(6))

    add(h2('Declaring a Language'))
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
    add(p('The declarative part of a language extension — three blocks in contributes. <b>languages</b> registers the language: id is used across all APIs, extensions/filenames determine automatic file association, icon is shown in Explorer. <b>grammars</b> connects a TextMate grammar for syntax highlighting (scopeName is the root scope, by convention source.langname). <b>snippets</b> is the snippet file for this language. All of this works without a single line of JavaScript.'))

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
    add(p('Language configuration defines editor behavior without grammars and without code. <b>comments</b> — which characters start a comment (Ctrl+/ will use lineComment). <b>brackets</b> — bracket pairs for highlighting and auto-closing. <b>autoClosingPairs</b> — automatic closing; notIn: ["string"] disables auto-closing of quotes inside strings. <b>indentationRules</b> — regular expressions for auto-indentation: increaseIndentPattern fires after a line with an opening brace, decreaseIndentPattern fires when a closing brace is typed.'))
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
        '            items[0].documentation = new vscode.MarkdownString(\'Converts to a string\');',
        '            items[0].insertText    = new vscode.SnippetString(\'toString()$0\');',
        '            items[0].detail        = \'(): string\';',
        '            return items;',
        '        }',
        '    },',
        '    \'.\' // trigger characters',
        ');',
        'context.subscriptions.push(completionProvider);',
    ]))
    add(sp(3))
    add(p('<b>CompletionItem</b> describes one auto-complete entry: <b>label</b> is the displayed text, <b>kind</b> is the icon (Function/Variable/Class), <b>insertText</b> is what gets inserted. The provider is called on every keystroke — always check the <b>CancellationToken</b>.'))
    add(sp(4))

    add(h2('Diagnostics'))
    add(p('Diagnostics are errors, warnings, and informational messages that appear in the <b>Problems</b> panel (Ctrl+Shift+M) and as underlines in the editor (red squiggly lines for errors, yellow for warnings). This is the primary way to show code issues to the user — analogous to ESLint, TypeScript, or Pylint output. Each diagnostic is bound to a specific range in a file.'))
    add(sp(4))
    add(screenshot('13-problems-panel.png', 'Problems panel: errors and warnings from DiagnosticCollection'))
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
        '            \'Unfinished task\',',
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
    add(p('<b>DiagnosticCollection.set(uri, diagnostics[])</b> atomically replaces all diagnostics for a file in the Problems panel. Call <b>collection.clear()</b> when closing a file or switching documents to remove stale errors.'))
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
        '                md.appendMarkdown(\'\\n\\nPrints a value to the console\');',
        '                return new vscode.Hover(md, range);',
        '            }',
        '        }',
        '    })',
        ');',
    ]))
    add(sp(3))
    add(p('<b>HoverProvider.provideHover()</b> is called when the cursor hovers over a word. <b>MarkdownString</b> lets you use Markdown with syntax-highlighted code in the hover panel. Check <b>token.isCancellationRequested</b> — hover is cancelled on mouse movement.'))
    add(pb())

    add(h2('Document Paste API (VS Code 1.97+)'))
    add(p('The Document Paste API lets extensions intercept copy/paste operations and modify pasted content. Available since VS Code 1.97:'))
    add(sp(3))
    add(code([
        'const pasteProvider: vscode.DocumentPasteEditProvider = {',
        '    async provideDocumentPasteEdits(',
        '        document: vscode.TextDocument,',
        '        ranges: readonly vscode.Range[],',
        '        dataTransfer: vscode.DataTransfer,',
        '        token: vscode.CancellationToken',
        '    ): Promise<vscode.DocumentPasteEdit | undefined> {',
        '        // Get the pasted text',
        '        const text = await dataTransfer.get(\'text/plain\')?.asString();',
        '        if (!text) return;',
        '',
        '        // Example: auto-import when pasting a component',
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
    add(p('The Document Paste API intercepts pasting via <b>provideDocumentPasteEdits()</b>. <b>DataTransfer</b> contains clipboard data in various MIME types (text/plain, text/html, image/png). The provider returns a <b>DocumentPasteEdit</b> with the modified text and an optional <b>additionalEdit</b> — a WorkspaceEdit applied alongside the paste. Typical use cases: auto-importing components, HTML-to-Markdown conversion, processing pasted images.'))
    add(pb())

    return A


if __name__ == '__main__':
    print(f'Part 1 has {len(build_story())} elements')
