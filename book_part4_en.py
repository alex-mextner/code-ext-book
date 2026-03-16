from book_helpers import *
import re

def build_story_part4():
    A = []
    def add(*x):
        for i in x: A.append(i)

    def ch(title, sub=''):
        add(StableAnchor('chapter_tips'))
        add(toc_ch(title), banner('Tips & Tricks', title, sub), sp(12))

    # ═══════════════════════════════════════════════════════════════════════════
    ch('50+ Extension Developer Tips & Tricks',
       'Advice from the real world — Reddit, GitHub, blogs, VS Code team experience')
    # ═══════════════════════════════════════════════════════════════════════════

    add(h2('Section 1: Development and Debugging'))
    add(sp(3))

    add(h3('1. Isolated VS Code Instance for Debugging'))
    add(p('Launch a separate VS Code instance with a clean profile — invaluable when you suspect extension conflicts:'))
    add(sp(2))
    add(code([
        '# Fully isolated instance',
        'code --user-data-dir="$HOME/vscode-debug" \\',
        '     --extensions-dir="$HOME/vscode-debug/extensions"',
        '',
        '# Or via environment variables',
        'VSCODE_DATA_DIR=/tmp/vscode-clean code .',
    ]))
    add(sp(3))
    add(p('Running VS Code with separate <b>--user-data-dir</b> and <b>--extensions-dir</b> creates a fully isolated instance — its own settings, its own set of extensions. Lets you quickly verify whether a problem is caused by an extension conflict or configuration.'))

    add(sp(3))
    add(box('Practice',
        'Keep this alias permanently in ~/.bashrc or ~/.zshrc. If the problem '
        'disappears in a clean instance — the culprit is an extension conflict or configuration. '
        'Will save hours of debugging.', 'tip'))
    add(sp(4))

    add(h3('2. TypeScript Without a Compilation Step (VS Code 1.108+)'))
    add(p('Since December 2025, VS Code supports extensions written directly in TypeScript without tsc:'))
    add(sp(2))
    add(code([
        '// package.json — just set .ts as main (experimental)',
        '"main": "./src/extension.ts",',
        '',
        '// Pros: instant reload, no build step in dev',
        '// Cons: publishing, tests — not stable yet',
        '// (experimental, follow the release notes)',
    ]))
    add(sp(3))
    add(p('Experimental support for TypeScript files directly as <b>main</b> in package.json — VS Code strips types on the fly without a tsc step. Eliminates the build cycle in dev mode, but not yet stable for publishing and tests.'))

    add(sp(4))

    add(h3('3. Quick Restart Without Rebuilding'))
    add(p('In development mode with watch-mode, press <b>Ctrl+R</b> in the Extension Development Host window instead of restarting with F5:'))
    add(sp(2))
    add(code([
        '// tasks.json — run watch in the background',
        '{',
        '  "label": "watch",',
        '  "type": "npm",',
        '  "script": "watch",',
        '  "isBackground": true,',
        '  "problemMatcher": "$tsc-watch",',
        '  "group": { "kind": "build", "isDefault": true }',
        '}',
        '',
        '// launch.json — preLaunchTask starts watch',
        '{',
        '  "type": "extensionHost",',
        '  "request": "launch",',
        '  "preLaunchTask": "${defaultBuildTask}",',
        '  "outFiles": ["${workspaceFolder}/out/**/*.js"]',
        '}',
    ]))
    add(sp(3))
    add(p('The combination of <b>tasks.json</b> and <b>launch.json</b> for continuous recompilation. The <b>watch</b> task with the <b>isBackground</b> flag runs in the background via <b>preLaunchTask</b>. After the first build, tsc watches for changes — just press Ctrl+R in the Extension Development Host instead of a full F5.'))

    add(sp(4))

    add(h3('4. Logging to Output Channel Instead of console.log'))
    add(p('console.log is only visible in Developer Tools Extension Host. For persistent logs, use an Output Channel:'))
    add(sp(2))
    add(code([
        '// Create a global channel once',
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
        '    if (level === \'error\') logger.show(true);  // show on errors',
        '}',
        '',
        '// Usage: the second argument \'log\' enables the structured log viewer in VS Code 1.90+',
    ]))
    add(sp(3))
    add(p('A dedicated Output Channel via <b>createOutputChannel</b> gives users persistent access to extension logs from the Output panel. The wrapper function <b>log()</b> adds a timestamp and level, and on errors automatically opens the channel via <b>logger.show(true)</b>. The second argument <b>\'log\'</b> when creating the channel enables built-in log syntax highlighting.'))

    add(sp(4))

    add(h3('5. Inspecting Extension Host from Browser DevTools'))
    add(p('Extension Host is a Node.js process. You can attach a full V8 inspector to it:'))
    add(sp(2))
    add(code([
        '// launch.json — add to your existing configuration',
        '{',
        '  "name": "Attach to Extension Host",',
        '  "type": "node",',
        '  "request": "attach",',
        '  "port": 5870,',
        '  "sourceMaps": true,',
        '  "outFiles": ["${workspaceFolder}/out/**/*.js"]',
        '}',
        '',
        '// Launch VS Code with the inspector:',
        'code --inspect-extensions=5870 .',
        '',
        '// Or via Developer Tools (Help -> Toggle Developer Tools)',
        '// -> Extension Host tab -> separate inspector',
    ]))
    add(sp(3))
    add(p('A <b>launch.json</b> configuration for attaching to the Extension Host on port 5870. The <b>--inspect-extensions</b> flag when launching VS Code opens the V8 Inspector — you can connect to it from Chrome DevTools or via a separate debugger configuration. Gives access to profiling, heap snapshots, and full breakpoints.'))

    add(sp(4))

    add(h3('6. Developer: Show Running Extensions Command'))
    add(p('The <b>Developer: Show Running Extensions</b> command shows all active extensions with activation time and CPU consumption. Indispensable for profiling:'))
    add(sp(2))
    add(code([
        '// Also from CLI:',
        'code --status',
        '# Outputs: VS Code version, extension list, activation times',
        '',
        '// Or from within the extension:',
        'const ext = vscode.extensions.getExtension(\'publisher.name\');',
        'console.log(`Active: ${ext?.isActive}, exports:`, ext?.exports);',
    ]))
    add(sp(3))
    add(p('The <b>code --status</b> command from the terminal outputs diagnostics without opening the GUI. From extension code, <b>vscode.extensions.getExtension()</b> lets you check the activation status and get the exported API of a specific extension by its identifier.'))

    add(sp(6))

    add(h2('Section 2: Performance and Architecture'))
    add(sp(3))

    add(h3('7. Rule: Activation > 100ms = Bad'))
    add(p('The VS Code team standard: an extension should not spend more than 100ms on activation. Check via Developer: Show Running Extensions:'))
    add(sp(2))
    add(code([
        '// Measuring activation time in code',
        'export async function activate(context: vscode.ExtensionContext) {',
        '    const t0 = Date.now();',
        '',
        '    // ... initialization ...',
        '',
        '    const elapsed = Date.now() - t0;',
        '    if (elapsed > 100) {',
        '        console.warn(`Slow activation: ${elapsed}ms`);',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('A simple <b>Date.now()</b> measurement at the start and end of <b>activate()</b>. If the time exceeds 100ms — a warning is printed to the console. In practice, this is the first indicator that initialization needs optimization: moving heavy operations to lazy loading.'))

    add(sp(4))

    add(h3('8. Deferred Provider Registration'))
    add(p('Don\'t register all providers at once — register them on demand:'))
    add(sp(2))
    add(code([
        'let completionRegistered = false;',
        '',
        '// Register completion only when the relevant language is opened',
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
    add(p('The completion provider is registered not at activation, but when the first document of the relevant language is opened. The <b>completionRegistered</b> flag prevents duplicate registration. This approach reduces activate() time — the provider is only created when it is actually needed.'))

    add(sp(4))

    add(h3('9. Caching Heavy Computations with Invalidation'))
    add(p('A cache pattern with automatic invalidation on file changes:'))
    add(sp(2))
    add(code([
        'class CachedAnalyzer {',
        '    private cache = new Map<string, { data: AnalysisResult; mtime: number }>();',
        '',
        '    async analyze(uri: vscode.Uri): Promise<AnalysisResult> {',
        '        const key = uri.toString();',
        '        const stat = await vscode.workspace.fs.stat(uri);',
        '',
        '        // Check cache by modification time',
        '        const cached = this.cache.get(key);',
        '        if (cached && cached.mtime === stat.mtime) {',
        '            return cached.data;',
        '        }',
        '',
        '        // Recompute',
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
        '        // heavy work here',
        '        return {};',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('A cache keyed by URI with invalidation via file <b>mtime</b>. The <b>analyze()</b> method compares the modification time via <b>vscode.workspace.fs.stat()</b> — if the file hasn\'t changed, it returns the cached result. The explicit <b>invalidate()</b> method allows programmatic cache reset, for example on <b>onDidChangeTextDocument</b> events.'))

    add(sp(4))

    add(h3('10. Mutex to Prevent Parallel Runs'))
    add(p('If your operation should not run in parallel (e.g., file scanning), use a simple mutex:'))
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
        '// Usage',
        'const scanMutex = new Mutex();',
        '',
        'async function scanWorkspace() {',
        '    const release = await scanMutex.acquire();',
        '    try {',
        '        // only one parallel scan',
        '        await doHeavyScan();',
        '    } finally {',
        '        release();',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('The <b>Mutex</b> class with an internal queue guarantees exclusive access to a resource. <b>acquire()</b> returns a release function; if the mutex is held — the call is queued and waits. The try/finally pattern in <b>scanWorkspace()</b> ensures release even on errors. Use this for operations like full workspace scanning that should not run in parallel.'))
    add(sp(4))

    add(h3('11. Throttle for Frequent Editor Events'))
    add(p('Throttle (unlike debounce) guarantees execution no more than once every N ms, while not losing the last event:'))
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
        '            // Schedule the last call',
        '            pending = setTimeout(() => {',
        '                lastCall = Date.now();',
        '                pending = null;',
        '                fn(...args);',
        '            }, remaining);',
        '        }',
        '    };',
        '}',
        '',
        '// Update decorations no more than once every 150ms',
        'const throttledUpdate = throttle(updateDecorations, 150);',
        'vscode.window.onDidChangeTextEditorSelection(e => {',
        '    throttledUpdate(e.textEditor);',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('A universal throttle function limits call frequency to once per <b>interval</b> ms. If a call arrives within the interval — a deferred run is scheduled via <b>setTimeout</b> so the last event is not lost. In the example, throttle is applied to <b>onDidChangeTextEditorSelection</b> for updating decorations — without it, every cursor movement would trigger a repaint.'))
    add(sp(6))

    add(h2('Section 3: Anti-patterns and Common Mistakes'))
    add(sp(3))

    add(h3('12. Anti-pattern: Synchronous File Operations'))
    add(p('Never use synchronous Node.js fs operations in production extension code:'))
    add(sp(2))
    add(code([
        '// BAD: BAD: blocks Extension Host',
        'const content = fs.readFileSync(\'/path/to/file\', \'utf8\');',
        'const files = fs.readdirSync(\'/path/to/dir\');',
        '',
        '// OK: GOOD: async via vscode.workspace.fs',
        'const bytes = await vscode.workspace.fs.readFile(uri);',
        'const content = Buffer.from(bytes).toString(\'utf8\');',
        '',
        '// OK: GOOD: via Node.js async API (if no alternative)',
        'const content = await fs.promises.readFile(\'/path/to/file\', \'utf8\');',
    ]))
    add(sp(3))
    add(p('Synchronous <b>readFileSync</b> and <b>readdirSync</b> block the Extension Host — all extensions freeze until I/O completes. Prefer <b>vscode.workspace.fs</b> — it works with remote files and virtual FS. If vscode.workspace.fs doesn\'t fit — <b>fs.promises</b> as a fallback.'))

    add(sp(4))

    add(h3('13. Anti-pattern: Global Mutable State'))
    add(p('Global variables are a source of hard-to-find bugs. Use the singleton pattern via ExtensionContext:'))
    add(sp(2))
    add(code([
        '// BAD: BAD: global state',
        'let globalData: any = null;',
        '',
        '// OK: GOOD: everything stored in context or in the extension object',
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
    add(p('The singleton class <b>ExtensionState</b> encapsulates all extension state. Data is stored via <b>context.globalState</b> — a built-in key-value storage that VS Code persists automatically. Initialization via <b>initialize(ctx)</b> in activate() guarantees a single instance with access to the context.'))

    add(sp(4))

    add(h3('14. Anti-pattern: Ignoring CancellationToken'))
    add(p('Providers are often called in parallel. Without checking the token — leaks and wasted work:'))
    add(sp(2))
    add(code([
        '// BAD: BAD: ignoring the cancellation token',
        'async provideHover(doc, pos, token) {',
        '    const result = await expensiveOp();  // wasted if user moved on',
        '    return new vscode.Hover(result);',
        '}',
        '',
        '// OK: GOOD: AbortController + CancellationToken',
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
    add(p('Two versions of the same provider: without and with <b>CancellationToken</b> checking. In the correct version, <b>AbortController</b> is bound to the token — when the request is cancelled, the heavy operation is interrupted via <b>signal</b>. Double checking (signal.aborted + token.isCancellationRequested) guards against race conditions between operation completion and cancellation.'))
    add(sp(4))

    add(h3('15. Anti-pattern: Notifications on Activation'))
    add(p('An extension that shows notifications on startup is one of the main sources of low Marketplace ratings:'))
    add(sp(2))
    add(code([
        '// BAD: BAD: annoys users',
        'export function activate(ctx) {',
        '    vscode.window.showInformationMessage(\'My Extension activated! Version 2.0!\');',
        '    // or: "Don\'t forget to rate us!"',
        '}',
        '',
        '// OK: GOOD: show only relevant notifications',
        'export function activate(ctx) {',
        '    const prevVersion = ctx.globalState.get<string>(\'version\');',
        '    const curVersion = ctx.extension.packageJSON.version;',
        '',
        '    if (prevVersion && prevVersion !== curVersion) {',
        '        // Show changelog only on actual update',
        '        const msg = `My Extension updated to ${curVersion}`;',
        '        vscode.window.showInformationMessage(msg, \'What\\\'s new?\').then(r => {',
        '            if (r) vscode.env.openExternal(vscode.Uri.parse(CHANGELOG_URL));',
        '        });',
        '    }',
        '    ctx.globalState.update(\'version\', curVersion);',
        '}',
    ]))
    add(sp(3))
    add(p('The correct approach: a notification is shown only on an actual version update. The previous version is stored in <b>globalState</b> and compared with the current one from <b>packageJSON.version</b>. The "What\'s new?" button opens the changelog in an external browser via <b>vscode.env.openExternal()</b>.'))

    add(sp(4))

    add(h3('16. Anti-pattern: keywords > 30 in package.json'))
    add(p('Marketplace will reject the publication if there are more than 30 keywords. A common mistake on first publish:'))
    add(sp(2))
    add(code([
        '// BAD: 35 keywords — vsce publish will fail with an error',
        '"keywords": ["vscode", "extension", "typescript", "javascript",',
        '  "python", "react", "vue", "angular", ... (35 words)]',
        '',
        '// OK: only Go files — max 30, choose the most meaningful',
        '"keywords": ["vscode", "extension", "typescript", "linter"],',
    ]))
    add(sp(3))
    add(p('Marketplace limits <b>keywords</b> to 30 items — exceeding this causes <b>vsce publish</b> to fail with an error. Only specify meaningful keywords that actually help users find the extension through search.'))
    add(sp(4))

    add(h3('17. Anti-pattern: Incorrect PAT Setup for vsce'))
    add(p('When creating a Personal Access Token in Azure DevOps, a common mistake is selecting a specific organization instead of "All accessible organizations":'))
    add(sp(2))
    add(code([
        '# Correct PAT settings:',
        '# Organization: All accessible organizations  <- IMPORTANT!',
        '# Scope:        Marketplace (Manage)          <- ONLY THIS',
        '',
        '# Verify that PAT works:',
        'vsce verify-pat -p <your-PAT>',
    ]))
    add(sp(3))
    add(p('It is critical when creating a PAT to select <b>All accessible organizations</b> — a token with a specific organization will not work with the Marketplace API. The scope must be strictly <b>Marketplace (Manage)</b>. The <b>vsce verify-pat</b> command checks token validity before the first publish.'))

    add(sp(6))

    add(h2('Section 4: Extension Security'))
    add(sp(3))

    add(h3('18. Extensions Have Full System Access'))
    add(p('Unlike browser extensions, VS Code extensions run as full Node.js applications without a sandbox:'))
    add(sp(2))
    for item in [
        'Can spawn child processes (child_process.spawn)',
        'Have unrestricted file system access',
        'Can make network requests to any host',
        'Can read environment variables including secrets',
        'Auto-update without notifying the user',
    ]:
        add(bul(item))
    add(sp(3))
    add(box('Security Recommendations',
        'Only install extensions from verified publishers. '
        'Check download counts and reviews. '
        'Prefer extensions with open source code when possible. '
        'Do not install .vsix files from unknown sources — '
        'they may contain malicious code even when displaying a "verified" badge.', 'warn'))
    add(sp(4))

    add(h3('18a. Reasons for Rejection and Removal of Extensions from Marketplace'))
    add(p('Microsoft can reject a publication or remove an already published extension. '
          'Documented reasons and known cases:'))
    add(sp(3))
    add(tblh(['Reason', 'Details']))
    add(tbl2([
        ('Data collection without consent',
         'The most common reason for removal. In 2022\u20132025, extensions '
         'with millions of installs were removed for collecting browsing history and project data without explicit opt-in. '
         'Rule: always check vscode.env.isTelemetryEnabled and show '
         'an explicit consent dialog before the first data submission'),
        ('Impersonating popular extensions (typosquatting)',
         'Extensions like "prettier-code", "pylance-ai", "copilot-extension" '
         'are systematically removed. Some accumulated 100k+ installs '
         'before detection. Do not use trademarks of Microsoft, GitHub, '
         'OpenAI in the name without explicit permission'),
        ('Malicious code',
         'A 2023 Snyk study identified 1,283 extensions with potentially malicious code '
         'in the Marketplace (mining, token theft, reverse shell). '
         'Microsoft introduced automatic scanning, but some slip through. '
         'Source: snyk.io/blog/malicious-vscode-extensions'),
        ('Violation of Marketplace Terms of Use',
         'Keywords > 30, review manipulation, false feature descriptions, '
         'advertising paid services without providing them. '
         'Full list of prohibitions: aka.ms/vsmarketplace-ToU'),
        ('Dependency license violations',
         'Including GPL dependencies in a closed-source extension without complying with license terms. '
         'Especially relevant for extensions using LangChain, Tree-sitter, LLVM tools'),
    ]))
    add(sp(4))
    add(box('How to Avoid Removal',
        '1. isTelemetryEnabled \u2014 always check before any data submission. '
        '2. Privacy Policy \u2014 required if the extension collects data. '
        '3. Unique name \u2014 check Marketplace for similar IDs before publishing. '
        '4. Open source \u2014 reduces removal risk, users can audit. '
        '5. Changelog \u2014 document what each version does.', 'tip'))
    add(sp(4))
    add(code([
        '// BAD: tokens in globalState (stored in plain text)',
        'await context.globalState.update(\'apiToken\', token);',
        '',
        '// BAD: tokens in settings (visible in settings.json)',
        'await vscode.workspace.getConfiguration(\'myExt\').update(\'token\', token);',
        '',
        '// GOOD: SecretStorage — encrypted by OS (Keychain / Credential Store)',
        'await context.secrets.store(\'apiToken\', token);',
        'const token = await context.secrets.get(\'apiToken\');',
        '',
        '// Listen for secret changes (e.g., on sign-out)',
        'context.secrets.onDidChange(e => {',
        '    if (e.key === \'apiToken\') {',
        '        // update extension state',
        '    }',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('Three ways to store tokens — two wrong and one right. <b>globalState</b> and <b>settings</b> store data in plain text on disk. <b>context.secrets</b> uses the OS keychain (Keychain Access on macOS, Credential Manager on Windows). The <b>onDidChange</b> event lets you react to secret deletion or update from another process.'))

    add(sp(4))

    add(h3('20. Checking Workspace Trust Before Dangerous Operations'))
    add(p('Do not perform potentially dangerous operations in a workspace that the user does not trust:'))
    add(sp(2))
    add(code([
        '// Check workspace trust',
        'if (!vscode.workspace.isTrusted) {',
        '    vscode.window.showWarningMessage(',
        '        \'This feature is not available in an untrusted workspace\'',
        '    );',
        '    return;',
        '}',
        '',
        '// Listen for trust level changes',
        'vscode.workspace.onDidGrantWorkspaceTrust(() => {',
        '    // activate features that require trust',
        '    registerSensitiveProviders();',
        '}, null, context.subscriptions);',
        '',
        '// In package.json — restrict capabilities in untrusted workspaces',
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
    add(p('<b>workspace.isTrusted</b> is false in Restricted Mode. Limit dangerous operations (code execution, file writes) when the workspace is untrusted. <b>onDidGrantWorkspaceTrust</b> fires on explicit confirmation — you can defer full activation until that moment.'))
    add(sp(6))

    add(h3('18b. Extension Signing and Verification on Install (VS Code 1.97+)'))
    add(p('Since VS Code 1.97, all extensions from the Marketplace undergo mandatory signature verification on install. If the signature fails — the extension is not installed:'))
    add(sp(2))
    for item in [
        '<b>Automatic secret scanning</b> — vsce (since 1.101) checks .vsix for API keys, tokens, passwords on publish',
        '<b>Trust prompts</b> — on first install from an unknown publisher, VS Code shows a confirmation dialog',
        '<b>Verified publisher badge</b> — requires 6+ months of publishing + domain verification',
        '<b>Pricing field</b> — "pricing": "Free" or "Trial" in package.json (for paid extensions)',
    ]:
        add(bul(item))
    add(sp(4))

    add(h2('Section 5: Telemetry and Analytics'))
    add(sp(3))

    add(h3('21. Telemetry Collection Rules'))
    add(p('Official Microsoft requirements for extension telemetry:'))
    add(sp(2))
    for good, bad in [
        ('Use @vscode/extension-telemetry for Azure Monitor', 'Do not collect PII (names, emails, file paths)'),
        ('Respect vscode.env.isTelemetryEnabled', 'Do not ignore user preferences'),
        ('Collect minimum data to understand behavior', 'Do not collect more than necessary'),
        ('Be transparent: describe what you collect in README', 'Do not hide the fact of data collection'),
    ]:
        add(bul(f'<b>\u2713 {good}</b>'))
        add(bul(f'<b>\u2717 {bad}</b>', 2))
    add(sp(4))

    add(h3('22. Proper Telemetry Implementation'))
    add(code([
        '// npm install @vscode/extension-telemetry',
        'import TelemetryReporter from \'@vscode/extension-telemetry\';',
        '',
        'let reporter: TelemetryReporter;',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    // Key from Azure Application Insights',
        '    const key = \'your-application-insights-key\';',
        '    reporter = new TelemetryReporter(key);',
        '    context.subscriptions.push(reporter);',
        '',
        '    // Automatically respects user\'s telemetry.telemetryLevel',
        '    reporter.sendTelemetryEvent(\'extension.activated\', {',
        '        version: context.extension.packageJSON.version',
        '    });',
        '}',
        '',
        '// If NOT using Application Insights:',
        'function sendCustomTelemetry(event: string, data: object) {',
        '    // Always check user permission',
        '    if (!vscode.env.isTelemetryEnabled) return;',
        '    // your sending implementation',
        '}',
        '',
        '// Listen for telemetry setting changes',
        'vscode.env.onDidChangeTelemetryEnabled(enabled => {',
        '    if (!enabled) reporter.dispose();',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('The <b>@vscode/extension-telemetry</b> package automatically respects the user\'s <b>telemetry.telemetryLevel</b> setting. For custom telemetry, checking <b>vscode.env.isTelemetryEnabled</b> before every send is mandatory. The <b>onDidChangeTelemetryEnabled</b> event lets you stop data collection in real time when settings change.'))

    add(sp(6))

    add(h2('Section 6: Marketplace and Monetization'))
    add(sp(3))

    add(h3('23. Pre-release Versions for Early Testers'))
    add(p('Since VS Code 1.63+, you can publish pre-release versions directly to the Marketplace. Users choose themselves: stable or pre-release:'))
    add(sp(2))
    add(code([
        '# Publishing a pre-release version',
        'vsce publish --pre-release',
        '',
        '# Versioning: even minor = stable, odd = pre-release',
        '# 1.0.x — stable',
        '# 1.1.x — pre-release',
        '# 1.2.x — stable',
        '',
        '# In package.json for pre-release:',
        '"version": "1.1.0",',
        '"preview": true,',
        '"engines": { "vscode": "^1.63.0" },',
    ]))
    add(sp(3))
    add(p('The <b>--pre-release</b> flag publishes a version to a separate Marketplace channel. Versioning convention: even minor — stable, odd — pre-release. Users switch between channels on the extension page. The <b>"preview": true</b> field marks the extension as experimental in the UI.'))

    add(sp(4))

    add(h3('24. Platform-specific VSIX Packages'))
    add(p('If your extension contains native binaries — publish separate packages for each platform:'))
    add(sp(2))
    add(code([
        '# Publishing for a specific platform',
        'vsce publish --target win32-x64',
        'vsce publish --target linux-x64',
        'vsce publish --target darwin-arm64',
        '',
        '# Supported targets:',
        '# win32-x64, win32-arm64',
        '# linux-x64, linux-arm64, linux-armhf',
        '# darwin-x64, darwin-arm64',
        '# alpine-x64, alpine-arm64',
        '# web',
        '',
        '# In GitHub Actions — platform matrix',
        'strategy:',
        '  matrix:',
        '    target: [win32-x64, linux-x64, darwin-arm64]',
    ]))
    add(sp(3))
    add(p('The <b>vsce publish --target</b> command publishes a separate VSIX for a specific OS and architecture. VS Code automatically downloads the correct package. In CI, use a platform matrix to build and publish all variants in a single run.'))
    add(sp(4))

    add(h3('25. Extension Packs'))
    add(p('An Extension Pack is an extension that automatically installs other extensions. Ideal for standardizing team environments:'))
    add(sp(2))
    add(code([
        '// package.json Extension Pack',
        '{',
        '  "name": "my-team-pack",',
        '  "displayName": "My Team Extension Pack",',
        '  "description": "Standard team extension set",',
        '  "extensionPack": [',
        '    "esbenp.prettier-vscode",',
        '    "ms-vscode.vscode-typescript-next",',
        '    "dbaeumer.vscode-eslint",',
        '    "my-publisher.my-custom-extension"',
        '  ]',
        '}',
        '',
        '// User installs one package — gets everything',
    ]))
    add(sp(3))
    add(p('The <b>extensionPack</b> field in package.json lists extension IDs for auto-installation. An Extension Pack itself contains no code — it\'s a meta-package. Ideal for standardizing a team\'s toolset: one install instead of ten.'))

    add(sp(6))

    add(h2('Section 7: VS Code Team Tips from Release Notes'))
    add(sp(3))

    add(h3('26. QuickPick.prompt — Persistent Text Below the Input Field (VS Code 1.108+)'))
    add(code([
        '// New API: prompt below the search bar',
        'const qp = vscode.window.createQuickPick();',
        'qp.prompt = \'Enter the file name (without extension)\';  // always visible',
        'qp.placeholder = \'Start typing...\';',
        'qp.items = await getItems();',
        'qp.show();',
    ]))
    add(sp(3))
    add(p('The new <b>prompt</b> property displays a persistent hint below the QuickPick input field — unlike <b>placeholder</b>, which disappears when typing. Use prompt for instructions, and placeholder for input format hints.'))

    add(sp(4))

    add(h3('27. QuickPickItem.resourceUri — Automatic Icons and Descriptions'))
    add(code([
        '// resourceUri automatically sets:',
        '//  - label from the file name',
        '//  - description from the path',
        '//  - icon from the current icon theme',
        'const items: vscode.QuickPickItem[] = files.map(uri => ({',
        '    label: \'\',      // VS Code will fill from uri',
        '    resourceUri: uri,',
        '}));',
    ]))
    add(sp(3))
    add(p('The <b>resourceUri</b> property in QuickPickItem automatically sets the file name as the label, the path as the description, and the icon from the current icon theme. Just pass the URI — VS Code does the rest, ensuring consistency with native file lists.'))

    add(sp(4))

    add(h3('28. window.title with the Active File Language (VS Code 1.108+)'))
    add(code([
        '// New variable in the window.title setting',
        '"window.title": "${activeEditorLanguageId} - ${activeEditorShort}"',
        '',
        '// In the extension: get the current langId',
        'const langId = vscode.window.activeTextEditor?.document.languageId;',
    ]))
    add(sp(3))
    add(p('The <b>${activeEditorLanguageId}</b> variable in the <b>window.title</b> setting shows the current file\'s language in the window title. From extension code, the same identifier is available via the active editor\'s <b>document.languageId</b>.'))

    add(sp(4))

    add(h3('29. Snippet Transformations: snakecase and kebabcase (VS Code 1.108+)'))
    add(code([
        '// New transformations in snippets',
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
        '// MyFileName.ts \u2192 my_file_name.ts (snakecase)',
        '// MyFileName.ts \u2192 my-file-name.ts (kebabcase)',
    ]))
    add(sp(3))
    add(p('Starting with VS Code 1.108, snippet transformations include <b>snakecase</b> and <b>kebabcase</b> modifiers. Applied to variables via the <b>${VAR/(.*)/${1:/snakecase}/}</b> syntax. In the example, <b>TM_FILENAME</b> and <b>TM_CURRENT_WORD</b> are automatically converted from CamelCase to the desired format right when the snippet is inserted.'))
    add(sp(4))

    add(h3('30. Agent Skills — A New Mechanism for Teaching Agents (VS Code 1.108+)'))
    add(p('Agent Skills are folders with instructions that Copilot loads automatically for relevant queries:'))
    add(sp(2))
    from book_ui_diagrams import agent_skills_tree
    add(agent_skills_tree('en'))
    add(sp(4))
    add(code([
        '// SKILL.md',
        '# My Skill',
        '## When to use',
        'Use this skill when the user asks about...',
        '',
        '## How to act',
        '1. Step one',
        '2. Step two',
        '',
        '// Enable via setting:',
        '"chat.useAgentSkills": true',
    ]))
    add(sp(3))
    add(p('The <b>.github/skills/</b> folder contains instructions that Copilot loads automatically for relevant queries. The <b>SKILL.md</b> file describes when and how to apply the skill, with code examples and an optional JSON schema alongside. Activated via the <b>chat.useAgentSkills</b> setting.'))

    add(sp(6))

    add(h2('Section 8: Advanced Patterns from Real Extensions'))
    add(sp(3))

    add(h3('31. The "Polite" Extension Pattern'))
    add(p('GitLens, Pylance, and other popular extensions follow the principle of "don\'t be intrusive." Here\'s a pattern from their source code:'))
    add(sp(2))
    add(code([
        '// Showing welcome walkthrough only once',
        'const hasShownWelcome = context.globalState.get<boolean>(\'hasShownWelcome\');',
        'if (!hasShownWelcome) {',
        '    await context.globalState.update(\'hasShownWelcome\', true);',
        '    // Open walkthrough, not a notification',
        '    await vscode.commands.executeCommand(',
        '        \'workbench.action.openWalkthrough\',',
        '        `${context.extension.id}#my-walkthrough`',
        '    );',
        '}',
        '',
        '// Always offer a way to disable the feature',
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
    add(p('The "polite" extension pattern: walkthrough instead of a notification, shown only once via a flag in <b>globalState</b>. The <b>workbench.action.openWalkthrough</b> command opens a built-in step-by-step guide. The <b>showWelcomeOnActivation</b> setting gives the user the ability to disable the welcome.'))

    add(sp(4))

    add(h3('32. Sharing State Between Webview and Extension'))
    add(p('A pattern from GitLens for bidirectional state synchronization with a Webview:'))
    add(sp(2))
    add(code([
        '// Typed messages for Webview',
        'type ToWebviewMessage =',
        '    | { type: \'init\'; data: InitData }',
        '    | { type: \'update\'; data: UpdateData }',
        '    | { type: \'error\'; message: string };',
        '',
        'type FromWebviewMessage =',
        '    | { type: \'ready\' }',
        '    | { type: \'action\'; payload: ActionPayload };',
        '',
        '// Typed sending',
        'function sendToWebview(panel: vscode.WebviewPanel, msg: ToWebviewMessage) {',
        '    panel.webview.postMessage(msg);',
        '}',
        '',
        '// Typed handling',
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
    add(p('A typed message protocol between Webview and extension. Union types <b>ToWebviewMessage</b> and <b>FromWebviewMessage</b> guarantee correctness on both ends. The <b>type</b> field is used for routing in a switch — the Webview reports readiness (<b>ready</b>), the extension responds with initialization (<b>init</b>).'))
    add(sp(4))

    add(h3('33. Command Registry as a Service Locator'))
    add(p('A pattern from popular extensions for managing commands:'))
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
        '// In extension.ts',
        'const registry = new CommandRegistry();',
        'registry.register(\'myext.action1\', () => doAction1());',
        'registry.register(\'myext.action2\', () => doAction2());',
        '',
        '// Register all at once',
        'context.subscriptions.push(...registry.registerAll(context, \'myext\'));',
    ]))
    add(sp(3))
    add(p('<b>registerCommand(id, handler)</b> binds a string command ID to a function. The ID must match the declaration in <b>contributes.commands</b> of package.json. The returned Disposable is placed in <b>context.subscriptions</b> — the command is automatically unregistered on deactivation.'))
    add(sp(4))

    add(h3('34. Conditional Activation by Configuration File'))
    add(p('Activate the extension only if a specific file exists in the project:'))
    add(sp(2))
    add(code([
        '// package.json',
        '"activationEvents": [',
        '  "workspaceContains:**/pyproject.toml",',
        '  "workspaceContains:**/setup.py",',
        '  "workspaceContains:.python-version"',
        ']',
        '',
        '// Multiple patterns = OR (at least one)',
        '// Extension activates if AT LEAST ONE file is found',
        '',
        '// For complex conditions — check in activate():',
        'export async function activate(ctx: vscode.ExtensionContext) {',
        '    const hasPyproject = (await vscode.workspace.findFiles(',
        '        \'**/pyproject.toml\', \'**/node_modules/**\', 1',
        '    )).length > 0;',
        '    ',
        '    if (!hasPyproject) return; // silently exit',
        '    registerProviders(ctx);',
        '}',
    ]))
    add(sp(3))
    add(p('The <b>workspaceContains</b> event activates the extension when a file matching the glob pattern exists. Multiple patterns work as OR. For complex logic — additional checking via <b>vscode.workspace.findFiles()</b> in activate() with a silent exit if the condition is not met.'))

    add(sp(4))

    add(h3('35. Programmatic Invocation of Other Extensions'))
    add(p('Extensions can use the API of other extensions via their exported public APIs:'))
    add(sp(2))
    add(code([
        '// Get the public API of another extension',
        'const pythonExt = vscode.extensions.getExtension(\'ms-python.python\');',
        'if (!pythonExt) {',
        '    vscode.window.showErrorMessage(\'Python extension is required\');',
        '    return;',
        '}',
        '',
        '// Activate if not active',
        'if (!pythonExt.isActive) await pythonExt.activate();',
        '',
        '// Use the public API',
        'const pythonApi = pythonExt.exports as PythonApi;',
        'const interpreter = await pythonApi.getActiveEnvironmentPath();',
        '',
        '// In your own extension — export an API',
        'export function activate(ctx: vscode.ExtensionContext) {',
        '    // Return the public API from activate()',
        '    return {',
        '        version: \'1.0.0\',',
        '        doSomething: (input: string) => processInput(input),',
        '    };',
        '}',
    ]))
    add(sp(3))
    add(p('The <b>vscode.extensions.getExtension()</b> method returns a reference to another extension by ID. Calling <b>activate()</b> guarantees loading, after which <b>exports</b> contains the public API. To export your own API — return an object from the <b>activate()</b> function.'))

    add(sp(6))

    add(h2('Section 9: Tools and Ecosystem'))
    add(sp(3))

    add(h3('36. Useful Extension Developer Tools'))
    add(sp(2))
    add(tblh(['Tool', 'Purpose']))
    add(tbl2([
        ('@vscode/vsce',              'CLI for packaging and publishing extensions'),
        ('ovsx',                      'CLI for publishing to Open VSX Registry'),
        ('@vscode/test-cli',          'Running integration tests with VS Code'),
        ('@vscode/extension-telemetry','Telemetry with Azure Application Insights'),
        ('esbuild',                   'Fast bundler. Recommended by the VS Code team'),
        ('@vscode/prompt-tsx',        'JSX syntax for creating AI prompts'),
        ('vscode-languageclient',     'Language Client for LSP extensions'),
        ('vscode-languageserver',     'Language Server for LSP extensions'),
        ('@vscode/debugadapter',      'Base class for Debug Adapters'),
        ('vscode-uri',               'Working with URIs without depending on vscode'),
    ]))
    add(sp(4))

    add(h3('37. Useful Commands for Extension Developers'))
    add(tblh(['Command', 'Purpose']))
    add(tbl2([
        ('Developer: Show Running Extensions',     'List of extensions with activation times'),
        ('Developer: Inspect Extension Host',       'Attach debugger to Extension Host'),
        ('Developer: Toggle Developer Tools',       'Open Extension Host DevTools'),
        ('Developer: Reload Window',                'Reload Extension Development Host'),
        ('Developer: Generate Color Theme From Current Settings', 'Export current theme to JSON'),
        ('Developer: Set Log Level',                'Manage logging level'),
        ('Developer: Open Process Explorer',        'View VS Code processes'),
        ('Help: Report Issue',                      'Quick bug report for VS Code'),
    ]))
    add(sp(4))

    add(h3('38. Testing in VS Code Insiders'))
    add(p('Publish to Insiders before stable for early detection of issues with new APIs:'))
    add(sp(2))
    add(code([
        '// .vscode-test.mjs — test on Insiders',
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
        '# In CI: run both variants',
        'vscode-test --label stable',
        'vscode-test --label insiders',
    ]))
    add(sp(3))
    add(p('The <b>.vscode-test.mjs</b> configuration with two profiles — stable and insiders. Each runs the same tests on the corresponding VS Code version. In CI, both configurations are run via <b>vscode-test --label</b> to catch issues with new APIs before they appear in stable.'))

    add(sp(6))

    add(h2('Section 10: Working with AI and the Future of Extensions'))
    add(sp(3))

    add(h3('39. Reading the Code of Popular Extensions'))
    add(p('The best way to learn is to read the source code of successful extensions. All these repositories are open:'))
    add(sp(2))
    add(tblh(['Extension', 'What to Study']))
    add(tbl2([
        ('github.com/gitkraken/vscode-gitlens',  'Complex Tree View, decorations, Webview, SCM API integration'),
        ('github.com/microsoft/vscode-copilot-chat', 'Chat Participant API, Language Model Tools, prompts'),
        ('github.com/microsoft/vscode-python',   'LSP client, interpreter management, Task Provider'),
        ('github.com/prettier/prettier-vscode',  'Formatter, settings, error handling'),
        ('github.com/microsoft/vscode-extension-samples', 'Official samples for every API'),
        ('github.com/eamodio/vscode-gitlens',    '[Historical mirror] GitLens repository before 2022, '
                                                  'when the project moved under GitKraken. '
                                                  'Current repository is gitkraken/vscode-gitlens (row above). '
                                                  'Early architecture without modern API — useful for comparing code evolution'),
    ]))
    add(sp(4))

    add(h3('40. @vscode/prompt-tsx — JSX for AI Prompts'))
    add(p('A library from the VS Code team for creating typed AI prompts via JSX. Used in Copilot itself:'))
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
        '// JSX syntax for the prompt',
        'class MyPrompt extends PromptElement<MyPromptProps> {',
        '    render() {',
        '        return (',
        '            <>',
        '                <SystemMessage>',
        '                    You are a TypeScript expert. Answer concisely.',
        '                </SystemMessage>',
        '                <UserMessage>',
        '                    Code context:',
        '                    <CodeBlock language="typescript">',
        '                        {this.props.codeContext}',
        '                    </CodeBlock>',
        '                    Question: {this.props.userQuery}',
        '                </UserMessage>',
        '            </>',
        '        );',
        '    }',
        '}',
        '',
        '// Rendering with token budget',
        'const { messages } = await renderPrompt(',
        '    MyPrompt,',
        '    { userQuery, codeContext },',
        '    { modelMaxPromptTokens: 4096 },',
        '    model',
        ');',
    ]))
    add(sp(3))
    add(p('The <b>@vscode/prompt-tsx</b> library lets you describe AI prompts via JSX components with typed props. The class inherits from <b>PromptElement</b>, the <b>render()</b> method returns a structure of <b>SystemMessage</b>, <b>UserMessage</b>, and <b>CodeBlock</b>. The <b>renderPrompt()</b> function automatically trims content to fit the model\'s token budget.'))

    add(sp(4))

    add(h3('41. Shell Execution API for Agent Extensions'))
    add(p('A new API for running commands in the VS Code terminal with output tracking — ideal for AI agents:'))
    add(sp(2))
    add(code([
        '// Shell Execution API (VS Code 1.93+)',
        'const terminal = vscode.window.createTerminal({',
        '    name: \'My Agent Terminal\',',
        '    shellPath: \'bash\'',
        '});',
        '',
        '// Execution with tracking',
        'const execution = await terminal.shellIntegration?.executeCommand(',
        '    \'npm test\'',
        ');',
        '',
        '// Reading output',
        'if (execution) {',
        '    const stream = execution.read();',
        '    for await (const data of stream) {',
        '        // data contains terminal stdout',
        '        console.log(\'Output:\', data);',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('<b>terminal.shellIntegration?.executeCommand()</b> — Shell Integration API (VS Code 1.93+). Allows tracking command output in the terminal from an extension. Optional chaining <b>?.</b> is mandatory: integration is only available when the shell supports it (bash, zsh, fish, PowerShell).'))
    add(sp(4))

    add(h3('42. ESM Modules in Extensions (VS Code 1.100+)'))
    add(p('Since VS Code 1.100, extensions support ES Modules — you can use "type": "module" in package.json:'))
    add(sp(2))
    add(code([
        '// package.json',
        '{',
        '  "type": "module",',
        '  "main": "./out/extension.js",',
        '  "engines": { "vscode": "^1.100.0" }',
        '}',
        '',
        '// extension.ts — regular ES imports',
        'import * as vscode from \'vscode\';',
        'import { analyzeFile } from \'./analyzer.js\';  // .js is required!',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    // ...',
        '}',
    ]))
    add(sp(3))
    add(p('ESM in VS Code extensions works only for the NodeJS Extension Host (not for Web Extensions). All relative imports must include the <b>.js</b> extension — even if the source is .ts. When bundling with esbuild, use <b>format: "esm"</b> instead of "cjs". Limitation: <b>require()</b> and dynamic <b>import()</b> do not work — only static imports.'))
    add(sp(4))

    add(h3('43. Extension Bisect — Diagnosing Problematic Extensions'))
    add(p('If a user complains that your extension "broke" VS Code — teach them to use Extension Bisect:'))
    add(sp(2))
    add(code([
        '// Launch via Command Palette',
        '// > Help: Start Extension Bisect',
        '',
        '// VS Code sequentially disables half of the extensions',
        '// and asks "Is the problem still there?" — binary search',
        '// Finds the culprit among 50+ extensions in ~5 steps',
        '',
        '// Or programmatically from your extension:',
        'vscode.commands.executeCommand(\'workbench.action.extensionBisect.start\');',
    ]))
    add(sp(3))
    add(p('Extension Bisect is a built-in binary search for problematic extensions. If after bisect your extension turns out to be the culprit — check <b>Developer: Show Running Extensions</b> for activation time and CPU consumption. Most often the cause is: slow activation, memory leaks in event handlers, or conflicts with other extensions via shared resources (formatters, Language Server).'))
    add(sp(4))

    add(h3('44. typeof navigator — Node.js 22 Trap (VS Code 1.101+)'))
    add(p('Since VS Code 1.101, Extension Host runs on Node.js 22, where <b>navigator</b> became a global object:'))
    add(sp(2))
    add(code([
        '// BROKEN with Node.js 22 — navigator now exists in Node too!',
        'if (typeof navigator !== \'undefined\') {',
        '    // Thought this was a browser? No — it\'s Node.js',
        '}',
        '',
        '// CORRECT — check for Node.js presence',
        'const isNode = typeof process === \'object\' && !!process.versions?.node;',
        'const isBrowser = !isNode;',
        '',
        '// Or use vscode.env',
        'const isWeb = vscode.env.uiKind === vscode.UIKind.Web;',
    ]))
    add(sp(3))
    add(p('The most reliable way to check the environment is <b>vscode.env.uiKind</b>: <b>UIKind.Web</b> for vscode.dev/github.dev, <b>UIKind.Desktop</b> for desktop VS Code. Do not rely on the presence of Node.js globals — they may or may not exist depending on the version.'))
    add(sp(4))

    add(h3('45. Secondary Side Bar for Additional Panels (VS Code 1.106+)'))
    add(p('Since VS Code 1.106, extensions can place View containers in the secondary side bar (Secondary Side Bar, on the right):'))
    add(sp(2))
    add(code([
        '"contributes": {',
        '  "viewsContainers": {',
        '    // Instead of "activitybar", use "panel" for the right panel',
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
        '      "type": "webview"  // or a regular tree view',
        '    }]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('The Secondary Side Bar is useful for auxiliary panels that should not compete for space in the main side bar. Users can open it via <b>View \u2192 Secondary Side Bar</b> or with a hotkey. Typical uses: logs, previews, debug information.'))
    add(sp(4))

    add(h3('46. MarkdownString in TreeItem (VS Code 1.106+)'))
    add(p('Since VS Code 1.106, TreeItem supports Markdown in tooltips — you can display formatted hints:'))
    add(sp(2))
    add(code([
        'class MyTreeItem extends vscode.TreeItem {',
        '    constructor(label: string, version: string, lastUpdate: string) {',
        '        super(label, vscode.TreeItemCollapsibleState.None);',
        '        ',
        '        // Markdown tooltip with formatting',
        '        const md = new vscode.MarkdownString();',
        '        md.appendMarkdown(`**${label}** v${version}\\n\\n`);',
        '        md.appendMarkdown(`Last updated: *${lastUpdate}*\\n\\n`);',
        '        md.appendCodeblock(\'npm install \' + label, \'bash\');',
        '        md.supportHtml = true;  // allow HTML tags',
        '        this.tooltip = md;',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('MarkdownString in tooltips supports full Markdown: bold, italic, code blocks with syntax highlighting, links. The <b>supportHtml = true</b> flag additionally allows HTML tags. This significantly improves Tree View informativeness without needing to open separate panels.'))
    add(sp(4))
    add(screenshot('22-custom-treeview.png', 'Custom Tree View: Node Dependencies with icons and versions'))
    add(sp(4))
    add(screenshot('22b-treeview-tooltip.png', 'MarkdownString tooltip: formatted hint on hover over a Tree View element'))
    add(sp(6))

    # Final chapter
    add(banner('Summary', 'Pre-publish Extension Checklist', 'Everything you need to verify'), sp(12))

    add(h2('Technical Checklist'))
    for item in [
        'Activation < 100ms on a typical machine',
        'No synchronous file operations',
        'All Disposables added to context.subscriptions',
        'CancellationToken is checked in providers',
        'Debounce/throttle for frequent editor events',
        'Web compatibility (if vscode.dev is planned)',
        'Tests pass on both stable and insiders VS Code',
        'Bundle optimized with esbuild --production',
        '.vscodeignore configured, package < 5MB',
        'Secrets stored in context.secrets, not globalState',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('UX Checklist'))
    for item in [
        'No notifications on activation without explicit user request',
        'Command names in the format "My Extension: Action Name"',
        'Icon PNG 128\u00d7128 or 256\u00d7256 (not SVG)',
        'Walkthroughs for onboarding new users',
        'Settings include an option to disable any intrusive feature',
        'Activity Bar icon added only if truly needed',
        'Status Bar used only for constantly relevant information',
        'Workspace Trust is respected',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Marketplace Checklist'))
    for item in [
        'README.md with GIFs/screenshots and usage examples',
        'CHANGELOG.md is up to date',
        'keywords \u2264 30 words',
        'repository.url is filled in (GitHub)',
        'engines.vscode set with the minimum supported version',
        'categories properly selected',
        'Telemetry: user\'s isTelemetryEnabled is respected',
        'PAT: "All accessible organizations" + "Marketplace (Manage)"',
        'Published to Open VSX for Cursor compatibility',
        'CI/CD configured for automatic publishing on tag',
    ]:
        add(bul(item))
    add(pb())

    # -- GLOSSARY ---------------------------------------------------------------
    add(toc_ch('Glossary'))
    add(banner('Glossary', 'Key Terms and Abbreviations', 'VS Code Extension API Reference'), sp(12))

    add(p('An alphabetical reference of terms encountered when developing VS Code extensions.'))
    add(sp(6))

    # glossary: (term, definition, chapter_anchor, chapter_label)
    # chapter_anchor — StableAnchor key, chapter_label — link text
    glossary = [
        ('Activation Event',
         'An event that causes VS Code to load the extension. Until the event, the extension '
         'consumes no resources. Declared in package.json. '
         'Examples: onLanguage:python, onCommand:myext.action, onStartupFinished.',
         'chapter_2', 'Chapter 2'),
        ('AMD (Asynchronous Module Definition)',
         'A legacy JavaScript module format that VS Code used until 2024. '
         'Replaced by ESM (ECMAScript Modules). Extensions still use CommonJS (require()).',
         'chapter_perf', 'Performance'),
        ('CancellationToken',
         'An object that signals to a provider that its result is no longer needed '
         '(the user switched to another file, typed the next character). '
         'All Language Providers should check token.isCancellationRequested.',
         'chapter_9', 'Chapter 9'),
        ('Chat Participant',
         'A specialized AI assistant in Copilot Chat, invoked via @name. '
         'Registered via vscode.chat.createChatParticipant(). '
         'Receives the user query and context, returns a response in a stream.',
         'chapter_17', 'Chapter 17'),
        ('CodeLens',
         'Interactive links displayed above lines of code (e.g., "3 references"). '
         'Registered via registerCodeLensProvider(). '
         'Often used for showing test info, git blame, call counts.',
         'chapter_9', 'Chapter 9'),
        ('Codicons',
         'VS Code\'s built-in icon library (600+ icons). '
         'Used via the $(icon-name) syntax in commands, buttons, Status Bar. '
         'Automatically adapts to the color theme. '
         'Catalog: code.visualstudio.com/api/references/icons-in-labels',
         'chapter_4', 'Chapter 4'),
        ('CompletionItem',
         'An object describing a single auto-completion item: label, kind, insertText, documentation. '
         'Returned from the registerCompletionItemProvider() provider. '
         'CompletionItemKind determines the icon (Function, Variable, Snippet, etc.).',
         'chapter_9', 'Chapter 9'),
        ('Contribution Points',
         'Static extension declarations in package.json (contributes.*). '
         'Require no JavaScript \u2014 VS Code reads them at startup. '
         'Examples: contributes.commands, contributes.views, contributes.themes.',
         'chapter_2', 'Chapter 2'),
        ('DAP (Debug Adapter Protocol)',
         'An open Microsoft protocol for communication between the editor and debugger. '
         'The LSP equivalent for debugging. Allows one debugger to work in any editor.',
         'chapter_10', 'Chapter 10'),
        ('Decoration',
         'Visual markup of text in the editor: background color, border, gutter icon, '
         'inline text before/after a line. Created via createTextEditorDecorationType.',
         'chapter_6.5', 'Chapter 6.5'),
        ('DiagnosticCollection',
         'A collection of errors and warnings displayed in the Problems panel. '
         'Created via languages.createDiagnosticCollection(). '
         'set(uri, diagnostics[]) atomically replaces all diagnostics for a file.',
         'chapter_9', 'Chapter 9'),
        ('Disposable',
         'An object with a dispose() method for releasing resources. '
         'All registrations (commands, providers, listeners) return a Disposable. '
         'Add to context.subscriptions \u2014 VS Code will call dispose() on deactivation.',
         'chapter_2', 'Chapter 2'),
        ('Document Paste API',
         'An API for intercepting copy/paste operations and modifying pasted content. '
         'Available since VS Code 1.97. Allows transforming clipboard data '
         'on paste into the editor (e.g., converting HTML to Markdown).',
         'chapter_9', 'Chapter 9'),
        ('Document Selector',
         'A filter for language providers: determines which documents a provider is active for. '
         'Can be a string (languageId), an object {language, scheme, pattern}, or an array.',
         'chapter_9', 'Chapter 9'),
        ('ESM (ECMAScript Modules)',
         'The standard JavaScript module format (import/export). '
         'VS Code core switched to ESM in 2024 (version 1.94), yielding +10% startup speed. '
         'Extensions still use CommonJS, migration is planned.',
         'chapter_perf', 'Performance'),
        ('esbuild',
         'A fast JavaScript/TypeScript bundler recommended for VS Code extensions. '
         'Bundles the entire dependency tree into a single file. '
         'Key options: platform: "node", external: ["vscode"], sourcemap: "linked".',
         'chapter_13', 'Chapter 13'),
        ('Extension Host',
         'An isolated Node.js process where all extensions run. '
         'Since VS Code 2023 \u2014 UtilityProcess with V8 sandbox. '
         'An extension crash does not affect the editor UI.',
         'chapter_16', 'Chapter 16'),
        ('ExtensionContext',
         'The extension lifecycle object passed to activate(context). '
         'Contains subscriptions (for Disposables), workspaceState, globalState, '
         'secrets (SecretStorage), extensionUri, and extensionMode.',
         'chapter_2', 'Chapter 2'),
        ('File System Provider',
         'An API for creating custom virtual file systems. '
         'registerFileSystemProvider registers a scheme (e.g., ftp://) '
         'and implements the full FS interface: read, write, stat, readDirectory.',
         'chapter_8', 'Chapter 8'),
        ('FileSystemWatcher',
         'A watcher for file changes in the workspace. '
         'Created via workspace.createFileSystemWatcher(globPattern). '
         'Events: onDidCreate, onDidChange, onDidDelete. Don\'t forget dispose().',
         'appendix_A', 'Reference A'),
        ('HoverProvider',
         'A provider for tooltips shown when hovering over a symbol. '
         'Registered via registerHoverProvider(). '
         'Returns a Hover with MarkdownString. Check token.isCancellationRequested.',
         'chapter_9', 'Chapter 9'),
        ('Inlay Hint',
         'An inline annotation in the editor: variable types, function parameter names. '
         'Appears as gray text directly in the code. registerInlayHintsProvider.',
         'chapter_9', 'Chapter 9'),
        ('L10n (Localization)',
         'VS Code extension localization API (vscode.l10n). '
         'Replaced the deprecated vscode-nls. Strings are wrapped in vscode.l10n.t("..."). '
         'The @vscode/l10n-dev tool extracts strings and generates bundle.l10n.*.json.',
         'chapter_l10n', 'Localization'),
        ('Language Model API',
         'An API for calling AI models from extension code. '
         'vscode.lm.selectChatModels() selects available LLMs (GPT-4o, Claude, etc.). '
         'Requests via model.sendRequest() with an array of LanguageModelChatMessage.',
         'chapter_17', 'Chapter 17'),
        ('Language Server',
         'A separate process that implements language analysis (completion, diagnostics, hover). '
         'Communicates with VS Code via LSP. Isolated \u2014 a crash does not affect the editor.',
         'chapter_10', 'Chapter 10'),
        ('LSP (Language Server Protocol)',
         'An open Microsoft protocol for communication between the editor and language server. '
         'JSON-RPC. Solves the M*N problem: one server works in all LSP editors. '
         'Specification: microsoft.github.io/language-server-protocol',
         'chapter_10', 'Chapter 10'),
        ('MCP (Model Context Protocol)',
         'A protocol for integrating AI models with tools. '
         'VS Code supports MCP servers for extending Copilot capabilities.',
         'chapter_18', 'Chapter 18'),
        ('MessagePort',
         'A Web API for direct IPC communication between processes without main process involvement. '
         'Used by VS Code for efficient IPC after the sandbox transition.',
         'chapter_16', 'Chapter 16'),
        ('Monaco Editor',
         'The code editor engine at the core of VS Code. '
         'Available as a standalone library (npm: monaco-editor). '
         'Uses custom font measurement via canvas for precise cursor positioning.',
         'chapter_perf', 'Performance'),
        ('Nonce',
         'A random value used in Webview Content Security Policy '
         'to allow a specific script tag. Generated each time a Webview is created.',
         'chapter_7', 'Chapter 7'),
        ('NotebookSerializer / NotebookController',
         'Components of the Notebook API. Serializer converts the file format to NotebookData '
         '(deserialize/serialize). Controller executes cells and returns output. '
         'The third component \u2014 NotebookRenderer \u2014 handles rich output visualization.',
         'chapter_notebook', 'Notebook API'),
        ('Open VSX',
         'An open extension registry for VS Code-based editors: '
         'Cursor, VSCodium, Gitpod, Theia, Eclipse Che. '
         'Managed by Eclipse Foundation. open-vsx.org',
         'chapter_14', 'Chapter 14'),
        ('OutputChannel',
         'An output channel for logging in the Output panel. '
         'Created via window.createOutputChannel(name). '
         'LogOutputChannel (since 1.74) adds levels: info, warn, error, debug.',
         'chapter_3', 'Chapter 3'),
        ('Piece Table',
         'A data structure for storing text in Monaco. '
         'Insert/delete in O(log n). Used instead of a plain string \u2014 '
         'efficient for frequent edits of large files.',
         'chapter_perf', 'Performance'),
        ('Proposed API',
         'Unstable VS Code APIs available only in Extension Development Host. '
         'Require declaring enabledApiProposals in package.json. '
         'Not allowed for Marketplace publication \u2014 for prototyping only.',
         'chapter_tips', 'Tips & Tricks'),
        ('Publisher',
         'A publisher account on VS Code Marketplace. '
         'Extension identifier: publisher.extensionname. '
         'Created at marketplace.visualstudio.com.',
         'chapter_14', 'Chapter 14'),
        ('Quick Pick',
         'A built-in VS Code UI component for selecting from a list. '
         'showQuickPick() or createQuickPick() for extended control. '
         'Use instead of custom dialogs.',
         'chapter_3', 'Chapter 3'),
        ('SCM (Source Control Management)',
         'VS Code API for version control system integration. '
         'The built-in Git is implemented via this same API. '
         'vscode.scm.createSourceControl creates a provider.',
         'chapter_3', 'Chapter 3'),
        ('SecretStorage',
         'Encrypted storage for tokens and credentials. '
         'context.secrets.store/get/delete. '
         'Data is stored in the OS keychain (Keychain Access, Windows Credential Manager).',
         'chapter_3', 'Chapter 3'),
        ('Telemetry',
         'Extension usage analytics. '
         'Always check vscode.env.isTelemetryEnabled before sending data. '
         'The @vscode/extension-telemetry library respects this flag automatically. '
         'Never collect PII (names, emails, file paths).',
         'chapter_tips', 'Tips & Tricks'),
        ('TextEdit',
         'An object describing a single document change: range + new text. '
         'Language providers (formatters, code actions) return TextEdit[], '
         'which VS Code applies to the document.',
         'chapter_9', 'Chapter 9'),
        ('ThemeColor',
         'A reference to a color from the active VS Code color theme. '
         'Use instead of hex values for automatic theme adaptation. '
         'Token reference: code.visualstudio.com/api/references/theme-color',
         'chapter_5', 'Chapter 5'),
        ('Tree View',
         'A UI component for hierarchical data in the side bar. '
         'Implemented via TreeDataProvider. '
         'Used for Explorer, Source Control, Extensions, and custom views.',
         'chapter_6', 'Chapter 6'),
        ('UtilityProcess',
         'An Electron API for creating protected child processes with V8 sandbox. '
         'VS Code uses it for Extension Host since version 1.94 (2024).',
         'chapter_16', 'Chapter 16'),
        ('V8 Code Cache',
         'A V8 mechanism for saving compiled bytecode to disk. '
         'On the next launch, JS is not parsed and compiled from scratch. '
         'VS Code force-enables the cache from the first launch (bypassHeatCheck).',
         'chapter_perf', 'Performance'),
        ('Virtual Document',
         'A document without a physical file on disk. '
         'Created via registerTextDocumentContentProvider. '
         'URI with a custom scheme: myscheme:/path/file.ext',
         'chapter_8', 'Chapter 8'),
        ('VSIX',
         'VS Code extension package format (zip archive). '
         'Created with the vsce package command. '
         'Can be installed via Extensions -> Install from VSIX.',
         'chapter_14', 'Chapter 14'),
        ('Walkthrough',
         'A built-in step-by-step onboarding mechanism for new extension users. '
         'Declared via contributes.walkthroughs in package.json. '
         'Opened via workbench.action.openWalkthrough. '
         'Preferable to notifications for first-time extension introduction.',
         'chapter_ux', 'Extension UX'),
        ('Webview',
         'An iframe inside VS Code, managed by the extension. '
         'Can render HTML/CSS/JS. Communicates with the extension via postMessage. '
         'Use ThemeColor CSS variables for a native look.',
         'chapter_7', 'Chapter 7'),
        ('When Clause',
         'A boolean expression controlling command and menu visibility. '
         'Evaluated by VS Code in real time. '
         'Reference: code.visualstudio.com/api/references/when-clause-contexts',
         'chapter_4', 'Chapter 4'),
        ('WorkspaceState / GlobalState',
         'Key-value stores for extension data. '
         'workspaceState \u2014 data for the current project. '
         'globalState \u2014 user data (across all projects). '
         'Both accessible via context.workspaceState and context.globalState.',
         'chapter_3', 'Chapter 3'),
    ]

    # Render glossary as table with clickable chapter references.
    # Each definition ends with a link to the chapter where the term is discussed.
    add(p('<i>Each term contains a link to the book section where it is discussed in detail. '
          'In the PDF version, the links are clickable.</i>', 'bodyi'))
    add(sp(4))
    add(tblh(['Term', 'Definition']))
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
