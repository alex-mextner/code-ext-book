from book_helpers import *

def build_story_part2():
    A = []
    def add(*x):
        for i in x: A.append(i)
    def ch(num, title, sub=''):
        part = f'Chapter {num}' if str(num).replace('.','').isdigit() else str(num)
        label = f'{part}: {title}' if str(num).replace('.','').isdigit() else title
        add(StableAnchor(f'chapter_{num}'))
        add(toc_ch(label), banner(part, title, sub), sp(12))

    # ── CHAPTER 10 ────────────────────────────────────────────────────────────
    ch('10', 'Language Server Protocol', 'LSP — the standard for language support')

    add(h2('Why LSP?'))
    add(p('When using the vscode.languages.* API directly, three problems arise:'))
    add(sp(2))
    for item in [
        '<b>Performance:</b> code analysis (AST, static checks) is resource-intensive. Running it in the Extension Host slows down the editor',
        '<b>Implementation languages:</b> Language Servers are often written in the same language they support. Integrating them into Node.js is difficult',
        '<b>The M×N problem:</b> M languages × N editors = M×N implementations. LSP: one server — works everywhere',
    ]:
        add(bul(item))
    add(sp(4))
    add(p('Language Server Protocol (LSP), developed by Microsoft, standardizes communication between an editor and a language server via JSON-RPC. Any LSP-compliant server works in any LSP-enabled editor.'))
    add(sp(3))
    add(p('For you as an extension developer, LSP is relevant in two scenarios. <b>First</b>: when installing extensions for Go, Rust, Python, C++ — the Language Server ships with the extension and provides autocompletion, navigation, and diagnostics. Understanding LSP helps you debug issues and configure servers. <b>Second</b>: if your company has a custom DSL, configuration language, or internal format — building your own Language Server (or at least a TextMate grammar for syntax highlighting) turns VS Code into a full-fledged IDE for that language. One server works across all editors: VS Code, Neovim, Emacs, Sublime.'))
    from book_new import lsp_diagram_inject, q_cancellation
    for _el in lsp_diagram_inject(): add(_el)
    add(sp(6))

    add(h2('LSP Extension Structure'))
    add(tblh(['Component', 'Description']))
    add(tbl2([
        ('Language Client',
         'A regular VS Code extension in TypeScript. Launches the Language Server, '
         'proxies requests. Library: vscode-languageclient'),
        ('Language Server',
         'An independent process implementing language logic. '
         'Can be written in any language. Library (Node.js): vscode-languageserver'),
    ]))
    add(sp(3))
    from book_ui_diagrams import lsp_tree
    add(lsp_tree('en'))
    add(sp(3))
    add(p('Typical LSP extension structure: two independent modules. <b>client/</b> contains the Language Client — a regular VS Code extension that launches the server process and proxies requests to it. <b>server/</b> — the Language Server implementing language logic. The shared <b>package.json</b> describes both modules as a single extension.'))

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
    add(p('The full Language Client lifecycle. <b>ServerOptions</b> describes how to launch the server process: module path and transport (<b>TransportKind.ipc</b> — inter-process communication, faster than stdio). <b>ClientOptions</b> sets the document filter and settings synchronization. In <b>deactivate()</b>, the client gracefully stops the server process via <b>client.stop()</b>.'))

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
        '            message: \'Unfinished task\',',
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
    add(p('A complete Language Server implementation with three key capabilities. <b>onInitialize()</b> declares capabilities — which features the server supports: document synchronization, autocompletion, hover, go-to-definition, references. The <b>validate()</b> function finds a pattern in the text and sends diagnostics via <b>sendDiagnostics()</b> — positionAt() converts an absolute offset to a line/column. <b>onCompletion()</b> returns a static list of keywords — in a real server the list is built dynamically based on the AST.'))
    add(pb())

    # ── CHAPTER 11 ────────────────────────────────────────────────────────────
    ch('11', 'UX Guidelines', 'Principles of quality user interface design')

    add(h2('Key Principles'))
    for item in [
        '<b>Don\'t interrupt.</b> No notifications on startup without the user asking',
        '<b>Follow VS Code patterns.</b> Use Command Palette, Quick Pick, InputBox',
        '<b>Minimize clicks.</b> The most frequent actions should be the fastest',
        '<b>Readable names.</b> Format: "My Extension: Do Action" in Command Palette',
        '<b>Respect resources.</b> Don\'t activate at VS Code startup unless necessary',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Activity Bar and Sidebar'))
    add(tblh(['Recommendation', 'Description']))
    add(tbl2([
        ('When to add',       'The extension has complex UI with multiple Views for regular use'),
        ('When NOT to add',   'The extension is rarely used. Better to add a command to the Command Palette'),
        ('Icon',              'SVG 16×16, monochrome. VS Code applies the theme color automatically'),
    ]))
    add(sp(6))

    add(h2('Status Bar'))
    add(p('Use it for always-relevant information: current branch, error count, active profile:'))
    add(sp(3))
    add(code([
        'const item = vscode.window.createStatusBarItem(',
        '    vscode.StatusBarAlignment.Left, 100',
        ');',
        'item.text    = \'$(check) Ready\';',
        'item.tooltip = \'My Extension — all good\';',
        'item.command = \'myext.showDetails\';',
        'item.show();',
        'context.subscriptions.push(item);',
        '',
        '// Update on editor change',
        'vscode.window.onDidChangeActiveTextEditor(editor => {',
        '    item.text = editor',
        '        ? `$(file-code) ${editor.document.languageId}`',
        '        : \'$(dash)\';',
        '});',
    ]))
    add(sp(3))
    add(p('<b>createStatusBarItem(alignment, priority)</b> creates an element in the status bar. <b>priority</b> determines position: a higher number means closer to the center. Call <b>hide()</b> when the extension is inactive for the current file — the Status Bar is a shared resource across all extensions.'))
    add(sp(6))

    add(h2('Quick Pick — Best Practices'))
    add(code([
        '// A well-built QuickPick with separators and descriptions',
        'const items: vscode.QuickPickItem[] = [',
        '    {',
        '        label: \'$(cloud-upload) Publish\',',
        '        description: \'Marketplace\',',
        '        detail: \'Requires a Personal Access Token\'',
        '    },',
        '    { label: \'\', kind: vscode.QuickPickItemKind.Separator },',
        '    {',
        '        label: \'$(package) Package\',',
        '        description: \'Create .vsix\'',
        '    },',
        '];',
        '',
        'const pick = await vscode.window.showQuickPick(items, {',
        '    title: \'Extension Actions\',',
        '    placeHolder: \'Choose...\',',
        '    matchOnDescription: true,',
        '    matchOnDetail: true',
        '});',
    ]))
    add(sp(3))
    add(p('An advanced QuickPick using VS Code UX patterns. Each item contains a <b>label</b> with a Codicon icon, a <b>description</b>, and <b>detail</b> for additional context. <b>QuickPickItemKind.Separator</b> visually groups elements. The flags <b>matchOnDescription</b> and <b>matchOnDetail</b> extend search — the user can find an item by any field, not just the label.'))
    add(sp(4))
    add(box('Walkthroughs',
        'For onboarding new users, use contributes.walkthroughs — '
        'step-by-step tutorials that appear when the extension is first installed. '
        'They significantly improve adoption rates.', 'tip'))
    add(pb())

    # ── CHAPTER 12 ────────────────────────────────────────────────────────────
    ch('12', 'Testing Extensions', 'Unit, Integration, and E2E tests')

    add(h2('Three Types of Tests'))
    add(p('The VS Code extension ecosystem recognizes three levels of testing — '
          'each serving its own purpose:'))
    add(sp(3))
    add(tblh(['Type', 'Description']))
    add(tbl2([
        ('Unit Tests',
         'Regular tests without VS Code. Test isolated business logic: '
         'parsers, utilities, algorithms. Any framework: Jest, Mocha, Vitest. '
         'The fastest — run in seconds'),
        ('Integration Tests\n(@vscode/test-cli)',
         'Run inside a real Extension Development Host. '
         'Full access to the vscode API: open a file, execute a command, check diagnostics. '
         'Slower — require launching VS Code. 90% of extension tests'),
        ('E2E Tests\n(Playwright)',
         'Test the real UI with browser automation tools: click buttons, '
         'verify visual states, test Webviews. '
         'The slowest. Needed for: Webview UI, visual decorations, '
         'screenshot tests. Covered in detail in chapter 19'),
    ]))
    add(sp(4))
    add(box('Playwright for E2E',
        'If you need to test Webview UI or visual components, '
        'use Playwright + @vscode/test-web. '
        'Full description with code examples is in chapter 19, "E2E Testing with Playwright".',
        'note'))
    add(sp(6))

    add(h2('@vscode/test-cli — The Modern Approach'))
    add(code([
        '# Installation',
        'npm install --save-dev @vscode/test-cli @vscode/test-electron',
        '',
        '# package.json',
        '"scripts": {',
        '    "test": "vscode-test"',
        '}',
    ]))
    add(sp(3))
    add(p('The <b>@vscode/test-cli</b> package is the modern replacement for the deprecated vscode-test. <b>@vscode/test-electron</b> downloads the required VS Code version for running tests. The <b>vscode-test</b> script in package.json reads configuration from .vscode-test.mjs and runs tests inside the Extension Development Host.'))
    add(sp(3))
    add(code([
        '// .vscode-test.mjs — configuration',
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
    add(p('The configuration file <b>.vscode-test.mjs</b> uses <b>defineConfig()</b> for type safety. <b>files</b> is the glob pattern for test files, <b>version</b> specifies which VS Code version to download (stable/insiders), <b>workspaceFolder</b> is the working folder for tests with fixtures. <b>mocha.timeout</b> is increased to 20 seconds — Extension Host startup is slower than regular tests.'))

    add(sp(6))

    add(h2('Writing Tests'))
    add(code([
        '// src/test/extension.test.ts',
        'import * as assert from \'assert\';',
        'import * as vscode from \'vscode\';',
        '',
        'suite(\'Extension Test Suite\', () => {',
        '',
        '    test(\'Extension activates\', async () => {',
        '        const ext = vscode.extensions.getExtension(',
        '            \'my-publisher.my-extension\'',
        '        );',
        '        assert.ok(ext, \'Extension should be installed\');',
        '        await ext!.activate();',
        '        assert.ok(ext!.isActive, \'Extension should be active\');',
        '    });',
        '',
        '    test(\'Command is registered\', async () => {',
        '        const commands = await vscode.commands.getCommands();',
        '        assert.ok(',
        '            commands.includes(\'myext.myCommand\'),',
        '            \'Command should be in the registry\'',
        '        );',
        '    });',
        '',
        '    test(\'Diagnostics work\', async () => {',
        '        const doc = await vscode.workspace.openTextDocument({',
        '            content: \'TODO: fix this\',',
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
    add(p('Three typical integration tests. The first checks that the extension is installed and activates via <b>getExtension()</b> + <b>activate()</b>. The second verifies the command is registered in the VS Code registry via <b>getCommands()</b>. The third opens a document with text via <b>openTextDocument()</b>, displays it, and waits for processing — after which you can check diagnostics via <b>getDiagnostics()</b>.'))
    add(sp(4))
    add(box('CI without a display',
        'On Linux in CI (GitHub Actions, GitLab CI), use: '
        'xvfb-run -a npm test '
        'VS Code requires a display to run. Xvfb emulates a virtual display.', 'warn'))
    add(sp(4))
    from book_new import build_playwright_chapter
    for el in build_playwright_chapter():
        add(el)
    add(pb())

    # ── CHAPTER 13 ────────────────────────────────────────────────────────────
    ch('13', 'Bundling with esbuild', 'Optimizing package size and Web compatibility')

    add(h2('Why Bundle?'))
    add(tblh(['Reason', 'Description']))
    add(tbl2([
        ('Web compatibility',
         'On vscode.dev and github.dev the extension must be a single JS file. '
         'Without a bundle it simply won\'t work'),
        ('Package size',
         'Without bundling, node_modules are included in the .vsix. '
         'With bundling — only the code actually used (tree-shaking)'),
        ('Loading speed',
         'One large file loads faster than 100 small ones due to filesystem overhead'),
    ]))
    add(sp(6))

    add(h2('esbuild — The Recommended Bundler'))
    add(code([
        '# Installation',
        'npm install --save-dev esbuild',
    ]))
    add(sp(3))
    add(p('esbuild configuration for a VS Code extension: <b>platform: "node"</b> and <b>external: ["vscode"]</b> are required — the vscode module is provided by the runtime and must not be included in the bundle. <b>sourcemap: "linked"</b> preserves source maps for debugging in the Extension Development Host.'))
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
        '        // IMPORTANT: vscode is provided by the runtime — do not include in bundle',
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
    add(p('The complete esbuild build script with two modes. In <b>--watch</b> mode, esbuild monitors file changes and rebuilds instantly (~10ms). Without the flag — a one-shot build and exit. <b>format: "cjs"</b> is required — the Extension Host loads modules via require(). <b>sourcesContent: false</b> reduces the source map size by referencing original files instead of embedding their contents.'))
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
    add(p('The set of scripts for the full development cycle. The key script is <b>vscode:prepublish</b>: @vscode/vsce calls it automatically before packaging into .vsix, which is why the <b>--production</b> flag is enabled here for minification. The <b>main</b> field points to <b>dist/extension.js</b> instead of the default out/ — VS Code loads this bundle.'))

    add(sp(6))

    add(h2('Web Extensions — Browser Extensions'))
    add(code([
        '// package.json',
        '"main":    "./dist/extension.js",      // Node.js',
        '"browser": "./dist/web/extension.js",  // Browser',
        '',
        '// esbuild.js — add web build',
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
    add(p('Dual entry point: <b>main</b> for Node.js (desktop) and <b>browser</b> for Web (vscode.dev, github.dev). <b>platform: "browser"</b> in esbuild replaces Node.js-specific modules with browser polyfills. Both bundles exclude vscode via <b>external</b> — the runtime provides the API in both environments.'))

    add(sp(4))
    add(box('Web Extension Limitations',
        'Unavailable in the browser: fs, path, child_process, os and other Node.js core modules. '
        'Use instead: fetch, crypto, TextEncoder, URL. '
        'For file operations — vscode.workspace.fs instead of fs.', 'warn'))
    add(sp(6))

    add(h3('Web Extension Limitations'))
    add(p('Web Extensions run in a browser context without Node.js. The following APIs and patterns <b>do not work</b>:'))
    add(sp(3))
    add(tblh(['What doesn\'t work', 'Alternative']))
    add(tbl2([
        ('require(), dynamic import()', 'Static import, bundle into a single file'),
        ('Node.js fs, path, os, child_process', 'vscode.workspace.fs for files'),
        ('URI.file(), fsPath', 'vscode.Uri.parse() with a custom scheme'),
        ('process.env, process.cwd()', 'vscode.workspace.workspaceFolders'),
        ('Native modules (*.node)', 'WebAssembly alternatives'),
        ('typeof navigator to detect environment', 'typeof process === "object" (as of Node.js 22, navigator exists in Node too!)'),
        ('child_process.spawn()', 'Terminal API or Language Server via WASM'),
    ]))
    add(sp(3))
    add(p('<b>Important since VS Code 1.101:</b> the upgrade to Node.js 22 added a global <b>navigator</b> to Node.js. Code like <b>if (typeof navigator !== "undefined")</b> is now broken — it returns true in Node as well. Use <b>typeof process === "object" &amp;&amp; process.versions?.node</b> to check for a Node.js environment.'))
    add(sp(6))
    add(pb())

    # ── CHAPTER 14 ────────────────────────────────────────────────────────────
    ch('14', 'Publishing to the Marketplace', '@vscode/vsce, VS Code Marketplace, and Open VSX Registry')

    add(h2('Requirements Before Publishing'))
    add(tblh(['File/Field', 'Requirements']))
    add(tbl2([
        ('README.md',      'A meaningful description with GIFs/screenshots and examples'),
        ('CHANGELOG.md',   'Version-by-version change history'),
        ('icon.png',       'PNG 128×128 or 256×256. SVG is not supported'),
        ('.vscodeignore',  'Excludes src/**, tests, node_modules to reduce .vsix size'),
        ('keywords',       '3–5 keywords for Marketplace search'),
        ('categories',     'The correct category for better visibility'),
        ('repository.url', 'A link to GitHub — essential for trust'),
        ('engines.vscode', 'A correct minimum version range'),
    ]))
    add(sp(6))

    add(h2('Publishing with @vscode/vsce'))
    add(p('<b>@vscode/vsce</b> (Visual Studio Code Extensions) is the official CLI for managing extensions. The package was previously called simply <b>vsce</b>, but was renamed to <b>@vscode/vsce</b>. The old name <b>vsce</b> on npm is deprecated — always use <b>@vscode/vsce</b>.'))
    add(sp(3))
    add(code([
        '# Installation',
        'npm install -g @vscode/vsce',
        '',
        '# Create a publisher account at marketplace.visualstudio.com',
        '# Create a PAT in Azure DevOps (Scope: Marketplace → Manage)',
        '',
        '# Login',
        'vsce login my-publisher-name',
        '',
        '# Package without publishing',
        'vsce package',
        '# → my-extension-1.0.0.vsix',
        '',
        '# Publish',
        'vsce publish',
        '',
        '# Publish with auto-incrementing version',
        'vsce publish patch   # 1.0.0 → 1.0.1',
        'vsce publish minor   # 1.0.0 → 1.1.0',
        'vsce publish major   # 1.0.0 → 2.0.0',
        '',
        '# Unpublish',
        'vsce unpublish (publisher).(extension)',
    ]))
    add(sp(3))
    add(p('After installing <b>@vscode/vsce</b>, the terminal CLI command remains <b>vsce</b> — it\'s an alias. <b>vsce package</b> bundles the extension into a .vsix file for testing or manual installation. <b>vsce publish</b> publishes to the Marketplace; it requires a PAT with Marketplace (Manage) permissions. <b>--pre-release</b> publishes a pre-release version — users with "Auto Update" will only receive it if they explicitly opt in.'))
    add(sp(4))
    add(code([
        '# .vscodeignore — exclusions from the package',
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
    add(p('The <b>.vscodeignore</b> file works like .gitignore — it excludes files from the .vsix package. Source code (src/**, **/*.ts), tests, source maps, and CI configs are not needed by the user. The patterns <b>!out/**</b> and <b>!dist/**</b> are exceptions to the exclusions: compiled code must be included in the package. Without .vscodeignore, node_modules and sources increase package size 5–10x.'))

    add(sp(6))

    add(h2('Categories, Tags, and Marketplace Discoverability'))

    add(p('The VS Code Marketplace is not a search engine in the traditional sense. '
          'Most installations come not through search, but through '
          'recommendations inside VS Code, the "Popular" tab, and direct links. '
          'That said, correct metadata affects filtering by category '
          'and suggestions when opening files of the relevant type.'))
    add(sp(4))

    add(h3('Official Categories'))
    add(p('Current list: <b>code.visualstudio.com/api/references/extension-manifest#categories</b>'))
    add(sp(3))
    add(p('The <b>categories</b> field in package.json accepts a strictly defined set. '
          'An invalid category is not a publishing error, but the extension will end up '
          'in the wrong Marketplace section:'))
    add(sp(3))
    add(tblh(['Category', 'When to use']))
    add(tbl2([
        ('Programming Languages',
         'Language support: syntax highlighting, IntelliSense, formatting. '
         'The largest category — high competition'),
        ('Snippets',
         'Extension with snippets only, no additional logic'),
        ('Linters',
         'Static code analysis, diagnostic output. '
         'ESLint, Pylance fall into this category'),
        ('Formatters',
         'Document formatting (registerDocumentFormattingEditProvider). '
         'Prettier, Black, gofmt. '
         '[*] A formatter returns TextEdit[] — VS Code applies changes '
         'to the editor buffer; the file on disk is unchanged until an explicit save (Ctrl+S). '
         'This is standard behavior of the entire Formatting API, not specific to Prettier. '
         'Source: code.visualstudio.com/api/references/vscode-api#DocumentFormattingEditProvider'),
        ('Debuggers',
         'Implements the Debug Adapter Protocol. '
         'For debugging support of a specific language/runtime'),
        ('Themes',
         'Color Theme or File Icon Theme. '
         'Visual appearance without functionality'),
        ('Testing',
         'Integration with test runners, TestController API'),
        ('SCM Providers',
         'Source Control Management — alternative VCS'),
        ('Other',
         'Everything else. The default category — '
         'avoid if something more specific fits'),
        ('AI',             'Chat Participants, Language Model Tools, Copilot integrations'),
        ('Chat',           'Chat interface extensions'),
        ('Keymaps',        'Ports keyboard shortcuts from another editor'),
        ('Education',      'Learning tools, interactive tutorials'),
        ('Data Science',   'Jupyter, data analysis, ML tools'),
        ('Visualization',  'Diagrams, graphviz, previews'),
        ('Notebooks',      'Notebook API extensions'),
    ]))
    add(sp(4))

    add(h3('Keywords'))
    add(p('The <b>keywords</b> field is an array of strings. '
          'The limit used to be 5; now it\'s not strictly documented, '
          'but going overboard (~30+) used to incur a search penalty. '
          'The sweet spot: 5–10 relevant words.'))
    add(sp(3))
    add(code([
        '// package.json — example of good metadata',
        '{',
        '  "categories": ["Programming Languages", "Formatters"],',
        '  "keywords": [',
        '    "python",      // target language',
        '    "formatter",   // functionality',
        '    "pep8",        // specific standard',
        '    "autopep8",    // tool name',
        '    "black"        // alternative (people search for comparisons)',
        '  ]',
        '}',
    ], highlight=False))
    add(sp(3))
    add(p('Example metadata for a Python formatter. <b>categories</b> contains two values — the extension will appear in both Marketplace sections. Keywords cover different search strategies: target language, type of functionality, specific standard, and names of alternative tools.'))

    add(sp(4))

    add(h3('Anti-patterns and Tips'))
    for btext in [
        '<b>Anti-pattern: the "Other" category</b> — the extension drops out of filters. '
        'If multiple categories apply — specify all of them (as an array)',
        '<b>Anti-pattern: generic tags</b> — "vscode", "extension", "plugin" don\'t help; '
        'thousands of extensions have them. Use tags specific to your domain',
        '<b>Tip: displayName</b> — the first field users search by. '
        'Include a keyword: "Python Formatter" is better than "PyFmt"',
        '<b>Tip: description</b> — the first 100 characters are visible in tooltips inside VS Code. '
        'Start with an action verb: "Formats Python code..." instead of "A formatter for..."',
        '<b>Tip: recommendations</b> — add the extension to .vscode/extensions.json '
        'of real projects (your own or via PR). '
        'When VS Code suggests installing extensions for a project — that\'s the highest-converting channel',
        '<b>Tip: precise activationEvents</b> — an extension that doesn\'t slow down VS Code '
        'gets better reviews organically. Speed matters more than any tags',
    ]:
        add(bul(btext))
    add(sp(4))

    add(box('Do tags actually help people find your extension?',
        'Honest answer: moderately. '
        'Marketplace search is not Google. The algorithm considers displayName, description, and keywords, '
        'but the main ranking factors are install count and rating. '
        'A new extension with zero installs will land on page 50 of search regardless of tags. '
        'Real traffic comes from: recommendations inside VS Code (workspaceContains), '
        'mentions in README files of popular projects, articles, and videos. '
        'Good metadata is hygiene, not marketing.',
        'note'))
    add(sp(6))

    add(h2('Open VSX Registry'))
    add(p('Open VSX is an Eclipse Foundation marketplace for editors based on VS Code that lack access to the official Marketplace: Cursor, VSCodium, Gitpod, Theia.'))
    add(sp(3))
    add(code([
        '# Installation',
        'npm install -g ovsx',
        '',
        '# Create a token: open-vsx.org → Settings → Access Tokens',
        '',
        '# Publish',
        'ovsx publish my-extension-1.0.0.vsix -p $OVSX_TOKEN',
        '',
        '# Or from source',
        'ovsx publish -p $OVSX_TOKEN',
    ]))
    add(sp(3))
    add(p('Publishing to Open VSX via the <b>ovsx</b> CLI tool. Two options: from a pre-built .vsix file (convenient in CI — one artifact for both marketplaces) or from source (ovsx will build the package itself). The token is created at open-vsx.org — separate from the Azure DevOps PAT.'))

    add(sp(4))
    add(box('Two registries — two publications',
        'VS Code Marketplace and Open VSX are independent platforms. '
        'To make your extension available everywhere, you need to publish to both. '
        'Automate this with GitHub Actions.', 'warn'))
    add(sp(6))

    add(h2('Why Extensions Get Rejected or Removed'))
    add(p('Microsoft doesn\'t publish a full list of rejection reasons, but based on '
          'public developer reports, the following categories stand out:'))
    add(sp(3))
    add(tblh(['Reason', 'Details']))
    add(tbl2([
        ('Data collection without consent',
         'The most common reason for removal in 2024-2025. '
         'Extensions collecting telemetry without explicit opt-in '
         'violate the Marketplace Terms. '
         'In 2025, Microsoft removed several popular extensions for this without warning. '
         'Solution: always check vscode.env.isTelemetryEnabled, '
         'use @vscode/extension-telemetry'),
        ('Malicious code',
         'The Marketplace scans every package with multiple antivirus engines. '
         'Dynamic detection runs the extension in a sandboxed VM. '
         'Obfuscated code raises suspicion even without obvious harm'),
        ('Name squatting',
         'Names imitating Microsoft, RedHat, or popular extensions '
         'are automatically rejected. '
         'Example: "microsoft-python" or "github-copilot-pro" will be rejected'),
        ('IP/license violations',
         'An extension that includes GPL code is incompatible with a closed license. '
         'Or: using someone else\'s branded icons without permission'),
        ('Technical requirements',
         'Missing README, invalid package.json, '
         'links to a non-existent repository.url, '
         'engines.vscode pointing to a non-existent version'),
        ('Content policy violations',
         'Adult content, political propaganda, spam. '
         'Extensions that don\'t do what their description claims'),
    ]))
    add(sp(3))
    add(p('<b>Pre-publication checklist:</b> '
          '<b>vsce ls</b> — lists files in the package (make sure there\'s nothing extra). '
          '<b>vsce package</b> — creates a .vsix without publishing (test locally). '
          'Appeals: vsmarketplace@microsoft.com with your publisher ID and extension ID.'))
    add(sp(3))
    add(box('Secret Scanning',
        'The Marketplace automatically scans every extension for secrets: '
        'API keys, Azure DevOps tokens, credentials. '
        'Do not include .env files, configs with tokens, or private keys in the .vsix. '
        'Use .vscodeignore for exclusions.',
        'warn'))
    add(pb())

    # ── CHAPTER 15 ────────────────────────────────────────────────────────────
    ch('15', 'CI/CD Automation', 'GitHub Actions for testing and publishing')

    add(h2('Testing Workflow'))
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
    add(p('A CI workflow with a matrix of 6 combinations: 3 OSes (Ubuntu, Windows, macOS) and 2 VS Code versions (stable, insiders). <b>xvfb-run</b> creates a virtual display on Linux — VS Code requires X11 even for headless tests. The <b>if: runner.os</b> condition splits the execution: on macOS and Windows a virtual display is not needed.'))
    add(sp(6))

    add(h2('Publishing Workflow'))
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
    add(p('A publishing workflow triggered by git tag <b>v*.*.*</b>. The sequence: build, test, package as .vsix, publish to both marketplaces, create a GitHub Release with the .vsix artifact. Tokens <b>VSCE_TOKEN</b> and <b>OVSX_TOKEN</b> are stored in GitHub Secrets — never in the code.'))
    add(sp(4))
    add(box('Storing tokens',
        'NEVER put tokens in code or yaml files. '
        'GitHub Settings → Secrets and variables → Actions → New repository secret.', 'warn'))
    add(pb())

    # ── CHAPTER 16 ────────────────────────────────────────────────────────────
    ch('16', 'Extension Host', 'Extension isolation architecture')

    add(h2('Types of Extension Host'))
    add(p('Current list: <b>code.visualstudio.com/api/advanced-topics/extension-host</b>'))
    add(sp(3))
    add(tblh(['Type', 'Description']))
    add(tbl2([
        ('local',  'A Node.js process on the same machine as the UI. The default for VS Code Desktop'),
        ('web',    'A browser host. Runs on vscode.dev, github.dev, VS Code for Web'),
        ('remote', 'A Node.js process running remotely: SSH, Dev Containers, GitHub Codespaces'),
    ]))
    add(sp(4))
    add(p('With Remote Development, some extensions run locally (UI extensions), others run remotely (workspace extensions). The location can be explicitly set in package.json:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"extensionKind": ["ui", "workspace"]',
        '// "ui"        — local UI host only',
        '// "workspace" — workspace host only (remote or local)',
        '// ["ui", "workspace"] — prefer UI, fall back to workspace',
        '',
        '// For Web Extension:',
        '"browser": "./dist/web/extension.js"',
    ]))
    add(sp(3))
    add(p('The <b>extensionKind</b> field determines where an extension runs during Remote Development. An array sets priority: <b>["ui", "workspace"]</b> means "prefer local, but if not possible — run remote." The <b>browser</b> field in package.json is the entry point for Web Extensions, used on vscode.dev and github.dev instead of <b>main</b>.'))

    add(sp(6))

    add(h2('Extension Host Best Practices'))
    for item in [
        '<b>Lazy activation:</b> use the minimum necessary Activation Events',
        '<b>async/await:</b> make all potentially long operations asynchronous',
        '<b>CancellationToken:</b> support cancellation in all providers',
        '<b>Dispose:</b> register everything in context.subscriptions',
        '<b>Don\'t block:</b> no synchronous file operations in production',
    ]:
        add(bul(item))
    add(sp(4))
    add(box('Monitoring the Extension Host',
        'The command Developer: Show Running Extensions displays all active extensions '
        'and their activation time. The command Developer: Inspect Extension Host lets you '
        'attach a debugger to the Extension Host process.', 'tip'))
    add(pb())

    # ── CHAPTER 17 ────────────────────────────────────────────────────────────
    ch('17', 'AI Extensions: Chat Participant', 'Copilot Chat API and Language Model API')

    add(h2('AI Extensibility in VS Code'))
    add(p('Starting with VS Code 1.90, the Extension API allows integration with GitHub Copilot:'))
    add(sp(2))
    for item in [
        '<b>Chat Participants</b> — specialized AI assistants in Copilot Chat (@my-assistant)',
        '<b>Language Model API</b> — calling AI models from extension code',
        '<b>Language Model Tools</b> — functions that AI calls automatically in agentic mode',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Chat Participant — Declaration in package.json'))
    add(code([
        '"contributes": {',
        '  "chatParticipants": [{',
        '    "id": "my-extension.assistant",',
        '    "name": "my-assistant",',
        '    "fullName": "My AI Assistant",',
        '    "description": "A specialized assistant for my project",',
        '    "isSticky": true,',
        '    "commands": [',
        '      { "name": "explain", "description": "Explain code" },',
        '      { "name": "fix",     "description": "Fix errors" }',
        '    ]',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Chat Participant declaration in package.json. <b>id</b> links the declaration to the registration code, <b>name</b> is the name for @-mentions in chat. <b>isSticky: true</b> means the participant stays selected between messages — the user doesn\'t need to re-type @name. The <b>commands</b> array adds slash commands: /explain, /fix — available after the @-mention.'))
    add(sp(6))

    add(h2('Chat Participant — Implementation'))
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
        '        stream.progress(\'Analyzing request...\');',
        '',
        '        // Get the Copilot model',
        '        const models = await vscode.lm.selectChatModels({',
        '            vendor: \'copilot\',',
        '            family: \'gpt-4o\'',
        '        });',
        '        if (models.length === 0) {',
        '            stream.markdown(\'Copilot is unavailable.\');',
        '            return;',
        '        }',
        '',
        '        // Context from the editor',
        '        const editor = vscode.window.activeTextEditor;',
        '        const code   = editor ? editor.document.getText(editor.selection) : \'\';',
        '',
        '        const messages = [',
        '            vscode.LanguageModelChatMessage.System(',
        '                \'You are a TypeScript expert. Respond concisely and to the point.\'',
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
        '                stream.markdown(`Error: ${e.message}`);',
        '        }',
        '    };',
        '',
        '    const participant = vscode.chat.createChatParticipant(',
        '        \'my-extension.assistant\', handler',
        '    );',
        '',
        '    // Follow-up questions',
        '    participant.followupProvider = {',
        '        provideFollowups() {',
        '            return [',
        '                { prompt: \'Explain in more detail\', label: \'$(info) More detail\' },',
        '                { prompt: \'Show an example\',        label: \'$(code) Example\'     },',
        '            ];',
        '        }',
        '    };',
        '',
        '    context.subscriptions.push(participant);',
        '}',
    ]))
    add(sp(3))
    add(p('A complete Chat Participant implementation in 4 parts. <b>1) Handler</b> — the request handler function, receiving the user\'s prompt, chat context, and a response stream. <b>2) Model</b> — selectChatModels() selects the Copilot LLM; sendRequest() calls it with system and user messages, the response is read in chunks via <b>for await</b>. <b>3) Context</b> — selected code from the active editor is appended to the prompt. <b>4) Follow-ups</b> — the provider suggests follow-up questions after the response.'))
    add(sp(6))

    add(h3('Libraries for Chat Participants'))
    add(p('Microsoft provides two libraries that significantly simplify Chat Participant development:'))
    add(sp(3))
    add(tblh(['Package', 'Purpose']))
    add(tbl2([
        ('@vscode/prompt-tsx', 'JSX/TSX syntax for building prompts with automatic token budget management'),
        ('@vscode/chat-extension-utils', 'Simplified Chat Participant creation with built-in tool calling support'),
    ]))
    add(sp(3))
    add(code([
        '// Example with @vscode/chat-extension-utils',
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
    add(p('<b>createChatParticipant()</b> from @vscode/chat-extension-utils handles all the infrastructure: message routing, tool calling, context management. You only define tools — a set of functions the LLM can call. Each tool is described by a JSON Schema for input parameters and an async invoke function.'))
    add(sp(6))

    add(pb())

    # ── CHAPTER 18 ────────────────────────────────────────────────────────────
    ch('18', 'Language Model Tools and MCP', 'AI Tools and the Model Context Protocol')

    add(h2('Language Model Tools'))
    add(p('Language Model Tools are functions that AI automatically calls as part of the agentic loop. The analog of function calling in the OpenAI API:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "languageModelTools": [{',
        '    "name": "myext_getFileInfo",',
        '    "displayName": "Get File Info",',
        '    "modelDescription": "Returns the type, size, and line count of a file",',
        '    "inputSchema": {',
        '      "type": "object",',
        '      "properties": {',
        '        "filePath": { "type": "string", "description": "Path to the file" }',
        '      },',
        '      "required": ["filePath"]',
        '    }',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Language Model Tool declaration in package.json. <b>modelDescription</b> is the key field: the AI reads it to decide when to call the tool (analogous to function description in OpenAI). <b>inputSchema</b> describes the JSON Schema of the parameters — the AI constructs the call based on this schema. The <b>myext_</b> prefix in the name prevents conflicts between extensions.'))
    add(sp(3))
    add(code([
        '// Tool registration',
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
    add(p('Tool registration via <b>vscode.lm.registerTool()</b>. The <b>invoke()</b> method receives typed input from the AI model and returns a <b>LanguageModelToolResult</b> with text parts. It uses <b>workspace.fs</b> instead of Node.js fs — required for compatibility with Remote SSH and vscode.dev. The tool is added to <b>subscriptions</b> for proper cleanup on deactivation.'))
    add(sp(6))

    add(h2('MCP Dev Guide'))
    add(p('Model Context Protocol (MCP) is an open standard by Anthropic for integrating AI with external data. VS Code supports MCP servers:'))
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
    add(p('MCP server integration in a VS Code extension. <b>McpServerDefinitionProvider</b> returns a list of MCP servers with their transports. <b>StdioMcpTransport</b> launches the server as a child process and communicates via stdin/stdout — the standard MCP transport. After registration via <b>registerMcpServerDefinitionProvider()</b>, the server\'s tools become available to AI models in Copilot Chat.'))
    add(sp(6))

    add(h3('MCP in VS Code Extensions (v1.101+)'))
    add(p('Starting with VS Code 1.101, extensions can programmatically register MCP servers. This lets you bundle MCP servers directly in the extension — the user doesn\'t need to install a separate Python/Node.js server:'))
    add(sp(3))
    add(code([
        '// package.json — MCP provider declaration',
        '"contributes": {',
        '  "mcpServerDefinitionProviders": [{',
        '    "id": "myext.mcpServers",',
        '    "label": "My Extension MCP Servers"',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('The declaration in package.json registers an MCP server provider. <b>id</b> is used during programmatic registration, <b>label</b> is displayed in MCP settings.'))
    add(sp(3))
    add(code([
        '// Registering an MCP server from an extension',
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
    add(p('The extension bundles an MCP server (a JavaScript file) and registers it via <b>McpStdioServerDefinition</b>. VS Code launches the server as a child process with the provided arguments and environment variables. <b>McpHttpServerDefinition</b> is also available for HTTP servers. MCP tool annotations (<b>readOnlyHint: true</b>) allow skipping user confirmation for safe read-only operations.'))
    add(sp(3))
    add(box('Copilot Chat — open source (v1.102)',
        'Starting with VS Code 1.102, the Copilot Chat extension is published under the MIT license on GitHub. '
        'It\'s ~50,000 lines of TypeScript — the best example of Chat Participant implementation, '
        'tool calling, MCP integration, and @vscode/prompt-tsx. '
        'Repository: github.com/microsoft/vscode-copilot-chat', 'tip'))
    add(sp(6))

    add(h3('Language Model Chat Provider (v1.104+)'))
    add(p('Starting with VS Code 1.104, extensions can register their own language models — cloud or local. A registered model appears in the model dropdown alongside GPT-4 and Claude:'))
    add(sp(3))
    add(code([
        '// Registering a custom model',
        'const provider: vscode.ChatModelProvider = {',
        '    async provideLanguageModelResponse(',
        '        messages: vscode.LanguageModelChatMessage[],',
        '        options: vscode.LanguageModelChatRequestOptions,',
        '        token: vscode.CancellationToken',
        '    ) {',
        '        // Send the request to your API',
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
        '        // Stream the response',
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
    add(p('The provider implements the <b>provideLanguageModelResponse()</b> method, which receives an array of messages and returns an async generator that streams tokens. The registered model is available to all Chat Participants via <b>vscode.lm.selectChatModels()</b> — the user selects the model in the interface, and your provider handles the requests.'))

    add(pb())

    # Appendices A/B/C/D have been moved to the end of the book.
    # The afterword has been moved to afterword.py (after the appendices).

    return A


if __name__ == '__main__':
    print(f'Part 2 has {len(build_story_part2())} elements')
