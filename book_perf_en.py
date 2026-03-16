"""
book_perf_en.py — What Makes VS Code Fast
Technical deep dive + how to apply the same techniques in extensions
"""
from book_helpers import *


def build_perf_chapter():
    A = []
    def add(*x):
        for i in x: A.append(i)

    add(StableAnchor('chapter_perf'))
    add(toc_ch('What Makes VS Code Fast'), banner('Deep Dive', 'What Makes VS Code Fast',
               'Architecture, engine, rendering, and lessons for extension developers'),
        sp(12))

    add(h2('Introduction: Electron Is Not a Death Sentence'))
    add(p('VS Code is an Electron application. So are Slack (before the native rewrite), '
          'Discord, Figma, and Notion. All of these are known as "heavy" apps. '
          'But VS Code is not. Why?'))
    add(sp(4))
    add(p('The short answer: Electron does not make applications slow. '
          'Developers who don\'t think about performance do. '
          'VS Code is the result of <b>ten years of accumulated optimizations</b>, '
          'many of which have fed back into Electron and V8 themselves.'))
    add(sp(4))

    add(quote(
        'VS Code is the benchmark of what can be done with Electron '
        '— if you really, really care about performance.',
        'Hacker News', 'comment with 800+ upvotes, 2021'
    ))
    add(sp(6))

    add(quote(
        'Modern text editors have higher latency than 42-year-old Emacs. '
        'Text editors! What can be simpler? On each keystroke, all you have to do '
        'is update a tiny rectangular region and modern text editors '
        "can't do that in 16ms. It's a lot of time. A LOT.",
        'Nikita Prokopov (tonsky)', 'Software Disenchantment, tonsky.me, 2018'
    ))
    add(sp(4))
    add(p('Prokopov writes this as a critique of the industry at large. VS Code is one of the rare '
          'exceptions: an editor that actually cared about input latency and '
          'achieved results comparable to native applications.'))
    add(sp(6))

    # -- 1. MULTI-PROCESS ARCHITECTURE ------------------------------------------
    add(h1('1. Multi-Process Isolation'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('The fundamental architectural decision of VS Code is that <b>no extension '
          'can freeze the UI</b>. The Extension Host is a separate Node.js process. '
          'If an extension enters an infinite loop or crashes with out of memory, '
          'the editor keeps working. This is not trivial: most Electron applications '
          'do everything in a single renderer process.'))
    add(sp(3))
    add(tblh(['Process', 'What it does and why it is isolated']))
    add(tbl2([
        ('Main Process\n(Electron main)',
         'Window management, lifecycle, native dialogs. '
         'Deliberately kept light — an overloaded main = a frozen UI'),
        ('Renderer Process\n(Chromium)',
         'UI only: rendering, Monaco editor, input handling. '
         'Since 2023 — full sandbox, no Node.js access'),
        ('Extension Host\n(Node.js, UtilityProcess)',
         'ALL extensions in a single process. '
         'Isolated from the UI. Since 2023 — UtilityProcess instead of fork()'),
        ('Shared Process\n(hidden window)',
         'File watcher, extension installation, full-text search. '
         'Not tied to a specific window'),
        ('Language Server\n(child process)',
         'Each LSP server is a separate process. '
         'TypeScript analyzes code in the background without blocking typing'),
    ]))
    add(sp(4))
    add(box('UtilityProcess — new API (Electron 22+)',
        'In 2023 VS Code switched from fork() to UtilityProcess for the Extension Host. '
        'UtilityProcess is a native Electron API for creating protected '
        'child processes with V8 sandbox. '
        'This reduced overhead and improved security: '
        'extensions can no longer bypass the V8 sandbox via native addons '
        'without explicit permission.', 'note'))
    add(sp(6))

    # -- 2. V8 SNAPSHOTS AND CODE CACHING --------------------------------------
    add(h1('2. V8 Snapshots and Code Caching'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('The biggest problem when starting a JavaScript application is <b>parsing and compilation</b>. '
          'The VS Code workbench bundle is about 11.5 MB of minified code. '
          'Without optimizations, V8 parses it from scratch on every launch.'))
    add(sp(4))

    add(h3('V8 Code Caching'))
    add(p('Since 2017, VS Code has used V8 Code Cache: after the first launch, V8 saves '
          'compiled bytecode to disk. On subsequent launches it loads the bytecode '
          'directly, bypassing parsing + compilation.'))
    add(sp(3))
    add(p('Chromium does this automatically, but only for "hot" pages '
          '(frequently visited). VS Code uses the <b>bypassHeatCheck</b> parameter '
          'so the cache works from the very first launch — because this is a desktop application, '
          'not a web page.'))
    add(sp(4))

    add(h3('V8 Startup Snapshots'))
    add(p('A more aggressive technique: instead of caching bytecode — '
          'saving the entire V8 heap after initialization. '
          'On the next launch, V8 deserializes the ready-made heap instead of executing '
          'init code from scratch. VS Code has used this since 2017.'))
    add(sp(3))
    add(code([
        '// How this works conceptually:',
        '// 1. Launch: execute all init code',
        '// 2. Save a V8 heap snapshot to disk',
        '// 3. Next launch: deserialize the heap — code is already "executed"',
        '',
        '// For extensions: the analog is require() caching',
        '// Bundling (esbuild) + one large file instead of 100 small ones',
        '// = V8 caches and optimizes better',
    ]))
    add(sp(3))
    add(p('Three-stage V8 Startup Snapshot scheme: the first launch executes init code, saves the heap to disk, and subsequent launches deserialize the ready-made heap. Extensions don\'t have direct access to snapshots, but <b>bundling via esbuild</b> into a single file gives V8 better conditions for code caching — a similar effect.'))

    add(sp(4))

    add(h3('AMD -> ESM: +10% Startup Speed (VS Code 1.94, 2024)'))
    add(p('Historically, VS Code used AMD (Asynchronous Module Definition) '
          'with a custom loader. AMD is not native to V8, and each require() '
          'added overhead. In 2024, the team completed the migration to <b>ESM</b>:'))
    add(sp(2))
    for item in [
        'ESM is native to V8 — the engine understands the dependency graph statically',
        'The workbench bundle shrank by <b>&gt;10%</b>',
        'The overhead of the custom AMD loader was eliminated',
        'Tree-shaking at the engine level became possible',
    ]:
        add(bul(item))
    add(sp(3))
    add(box('Extensions are still on CommonJS',
        'After the VS Code core migrated to ESM, extensions are still loaded via '
        'CommonJS (require). This is temporary — github.com/microsoft/vscode/issues/130367. '
        'When ESM support for extensions is ready, it will further speed up Extension Host startup.',
        'note'))
    add(sp(6))

    # -- 3. MONACO: CUSTOM RENDERING -------------------------------------------
    add(h1('3. Monaco Editor: Text Rendering'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('Monaco is not just a textarea with syntax highlighting. '
          'It is a fully custom text rendering engine with '
          '<b>three layers</b>:'))
    add(sp(3))
    add(tblh(['Layer', 'Technology and purpose']))
    add(tbl2([
        ('DOM renderer\n(default)',
         'Each line is a separate &lt;div&gt;. Only visible lines in the DOM (virtualization). '
         'Characters are split into &lt;span&gt; by theme tokens. '
         'Works everywhere, good accessibility'),
        ('Canvas 2D renderer',
         'Text is drawn on an HTML Canvas. Bypasses the browser layout engine. '
         'Faster than DOM for large files. '
         'Uses a texture atlas for glyphs'),
        ('WebGL renderer\n(terminal xterm.js)',
         'Text as quads on the GPU via WebGL. '
         'The fastest — GPU parallelism. '
         'Used in the integrated terminal'),
    ]))
    add(sp(4))

    add(h3('Line Virtualization — the Key Technique'))
    add(p('The editor DOM <b>never contains all lines of a file</b>. '
          'Monaco computes the viewport and creates DOM elements only for visible lines '
          'plus a small buffer. Opening a 100,000-line file '
          'does not create 100,000 divs — only ~50 for the visible area.'))
    add(sp(3))
    add(code([
        '// Conceptual Monaco viewport manager:',
        'class ViewportManager {',
        '    private readonly OVERSCAN_LINES = 10;',
        '',
        '    getVisibleLines(scrollTop: number, viewportHeight: number): LineRange {',
        '        const firstLine = Math.floor(scrollTop / this.lineHeight);',
        '        const lastLine = Math.ceil(',
        '            (scrollTop + viewportHeight) / this.lineHeight',
        '        );',
        '        return {',
        '            start: Math.max(0, firstLine - this.OVERSCAN_LINES),',
        '            end: lastLine + this.OVERSCAN_LINES,',
        '        };',
        '    }',
        '    // On scroll: recycle DOM elements from old lines for new ones',
        '    // = zero allocation scrolling',
        '}',
    ]))
    add(sp(3))
    add(p('Monaco viewport virtualization: <b>getVisibleLines()</b> computes the range of visible lines from scrollTop and viewport height. <b>OVERSCAN_LINES</b> adds a buffer above and below so there is no flicker during fast scrolling. DOM elements from old lines are reused for new ones — zero allocation scrolling.'))

    add(sp(4))

    add(h3('Font Measurement — Why CSS Is Not Enough'))
    add(p('The term "custom font rendering" in the VS Code context is misleading: '
          'the actual glyph rendering was always done by Chromium/OS using standard methods. '
          'What is truly custom is <b>character measurement</b>. '
          'This is what distinguishes Monaco from a regular textarea, and this is where '
          'important lessons for extensions working with text positions lie:'))
    add(sp(3))
    add(p('CSS font metrics (getBoundingClientRect, offsetWidth) give imprecise results '
          'for cursor positioning — different OSes and fonts yield fractional values. '
          'This leads to cursor "drift" in long lines and incorrect '
          'column guide alignment.'))
    add(sp(3))
    add(p('Monaco measures the real width of each character via '
          '<b>canvas.measureText()</b> and builds a cache table. '
          'This provides pixel-perfect cursor positioning regardless of the font. '
          'Source: <b>github.com/microsoft/vscode/blob/main/src/vs/editor/browser/config/fontMeasurements.ts</b>'))
    add(sp(3))
    add(code([
        '// Monaco: measurement during initialization (simplified)',
        '// see fontMeasurements.ts in the VS Code repository',
        'class FontMeasurements {',
        '    private widthCache = new Map<string, number>();',
        '',
        '    measureChar(char: string, font: string): number {',
        '        const key = `${char}:${font}`;',
        '        if (this.widthCache.has(key)) {',
        '            return this.widthCache.get(key)!;',
        '            // Cache: don\'t re-measure for the same char+font',
        '        }',
        '        // Canvas measureText() is more precise than CSS layout engine',
        '        this.ctx.font = font;',
        '        const metrics = this.ctx.measureText(char);',
        '        const width = metrics.width;  // actual width in px',
        '        this.widthCache.set(key, width);',
        '        return width;',
        '    }',
        '',
        '    // When the font changes in settings — full reset and re-measurement',
        '    onFontSettingsChanged(): void {',
        '        this.widthCache.clear();',
        '        this.remeasureAllVisible();',
        '    }',
        '}',
        '// Result: cursor position is pixel-perfect with any font',
    ]))
    add(sp(3))
    add(p('Caching font measurer: <b>measureChar()</b> uses canvas.measureText() instead of CSS layout for pixel-perfect character width. Results are stored in a Map keyed by char+font. <b>onFontSettingsChanged()</b> resets the cache and re-measures everything — called when the font changes in settings.'))

    add(sp(4))

    add(h3('WebGPU Renderer — the Next Step (In Development)'))
    add(p('In 2024, the VS Code team started work on a WebGPU renderer for Monaco. '
          'Similar to how xterm.js uses WebGL for the terminal. '
          'Tracking: <b>github.com/microsoft/vscode/issues/221145</b> '
          '(GPU accelerated canvas renderer, vscode repository). '
          'Glyphs are drawn into a texture atlas on the CPU, then the GPU batch-renders '
          'thousands of characters in a single draw call.'))
    add(sp(3))
    add(tblh(['Renderer', 'Performance']))
    add(tbl2([
        ('DOM renderer',   'Baseline. Good for normal usage'),
        ('Canvas 2D',      '~2x faster than DOM for large files. Less layout thrashing'),
        ('WebGL (xterm)',  '~10x faster than DOM. Already used in the terminal'),
        ('WebGPU (future)','Potentially even faster + compute shaders for highlighting'),
    ]))
    add(sp(6))

    # -- 4. PROCESS SANDBOXING AND CODE CACHING --------------------------------
    add(h1('4. Process Sandboxing: Security and Performance'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('Between 2020 and 2023, the VS Code team carried out a multi-year effort to '
          '<b>sandbox-isolate the renderer process</b>. '
          'At first glance this is a security task, but it impacted architecture and speed as well.'))
    add(sp(3))
    add(p('Before sandboxing, the renderer had direct access to Node.js APIs (fork, file system). '
          'After — the renderer became a "pure" web context. All Node.js operations go '
          'through MessagePort to the shared/main process. '
          'This forced the elimination of unnecessary dependencies and made IPC explicit and measurable.'))
    add(sp(4))

    add(h3('MessagePort Instead of Node.js Sockets'))
    add(p('Before sandboxing: IPC via Node.js UNIX sockets. '
          'After: Web MessagePort API. '
          'The difference is that MessagePort does not require the main process — '
          'two renderers can communicate directly:'))
    add(sp(3))
    add(code([
        '// VS Code uses MessagePort for direct IPC between processes',
        '// (simplified):',
        '',
        '// Main process: creates the channel',
        'const { port1, port2 } = new MessageChannel();',
        '// port1 stays in the shared process, port2 is passed to the renderer',
        '',
        '// Renderer: receives port2 via preload script',
        'window.addEventListener("message", event => {',
        '    if (event.data.type === "port") {',
        '        const port = event.ports[0];',
        '        // Direct communication with shared process without main process!',
        '        port.postMessage({ type: "installExtension", id: "..." });',
        '    }',
        '});',
    ]))
    add(sp(3))
    add(p('Direct IPC pattern via <b>MessagePort</b>: the main process creates a MessageChannel and distributes ports to participants. The renderer receives a port via the preload script and communicates with the shared process directly — without routing through the main process. This reduces IPC latency and offloads the main process.'))

    add(sp(6))

    # -- 5. LAZY LOADING EVERYTHING --------------------------------------------
    add(h1('5. Lazy Loading — a Systemic Philosophy'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('VS Code does not load anything until it is actually needed. '
          'This applies at every level:'))
    add(sp(3))
    add(tblh(['Level', 'Implementation']))
    add(tbl2([
        ('Extensions',
         'Activation Events: an extension is not loaded until its event fires. '
         '~200 installed extensions -> only 5-10 are active at startup'),
        ('Language Features',
         'IntelliSense, diagnostics, hover — requested on demand. '
         'The TypeScript worker starts on the first .ts file open'),
        ('UI Panels',
         'SCM panel, Debug view, Extensions view — '
         'content loads on first open'),
        ('Workbench Modules',
         'Historically AMD with dynamic require(). With ESM — '
         'dynamic import() for infrequently used functions'),
        ('Language Packs',
         'NLS (localization) — needed strings are loaded lazily '
         'per file, not the entire pack at once'),
    ]))
    add(sp(4))
    add(box('Why this matters for extension developers',
        'Every extension with activationEvents: ["*"] or onStartupFinished '
        'breaks VS Code\'s systemic lazy-loading strategy. '
        'If all 200 installed extensions activate at startup — '
        'startup will take 5-10 seconds. '
        'Proper Activation Events are not just "good practice" — '
        'they are respect for the system architecture.', 'warn'))
    add(sp(4))
    add(quote(
        'VS Code and Atom eventually became faster versions of their original '
        'Electron prototypes. These improvements are accidental. '
        "It's sheer luck they happened. "
        'If you want to build a really fast program, '
        'pay attention to the performance from the start.',
        'Nikita Prokopov (tonsky)', 'Performance First, tonsky.me, 2020'
    ))
    add(sp(3))
    add(p('<b>Context:</b> Prokopov mentions Atom as a comparison — Atom was the first '
          'Electron editor (GitHub, 2014) and was known for being slow. '
          'VS Code came later (Microsoft, 2015) on the same technology but with a different '
          'approach to performance. Atom was discontinued in 2022. '
          'Prokopov writes that the performance improvements in both cases '
          'were a "lucky accident" rather than an intentional goal from the start — '
          'and urges making performance a priority from day one.'))
    add(sp(6))

    # -- 6. INCREMENTAL COMPUTATION --------------------------------------------
    add(h1('6. Incremental Computation'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('VS Code never recomputes from scratch what can be computed incrementally.'))
    add(sp(3))
    add(tblh(['Subsystem', 'Incrementality']))
    add(tbl2([
        ('TextModel (document)',
         'Piece Table tree: insert/delete O(log n), '
         'does not rebuild the entire string. '
         'Change history stores only deltas, not snapshots'),
        ('Syntax Highlighting\n(TreeSitter / TM)',
         'When a line changes: reparsing only the affected ranges. '
         'Async tokenization — does not block typing'),
        ('TypeScript LSP\n(Incremental Parsing)',
         'The TypeScript compiler API supports incremental parsing: '
         'when a file changes — only affected nodes are recomputed'),
        ('Diagnostics',
         'DiagnosticCollection is updated only for changed files. '
         'File watcher notifies about specific changes'),
        ('Search',
         'Full-text search index is built incrementally: '
         'watchers track changes and update only affected files'),
    ]))
    add(sp(6))

    # -- 7. INPUT LATENCY ------------------------------------------------------
    add(h1('7. Input Latency: Typing'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('The most sensitive UX metric of a code editor is the '
          '<b>latency between a keypress and the character appearing on screen</b>. '
          'VS Code has achieved results here comparable to native editors.'))
    add(sp(3))

    add(h3('Input -> Render Pipeline'))
    add(p('When the user presses a key:'))
    add(sp(2))
    for step in [
        '<b>OS keydown event</b> -> Chromium event handler (~0ms)',
        '<b>Monaco keyboard handler</b> -> updates TextModel (~0.1ms)',
        '<b>View layout</b> -> computes DOM changes (~0.5-1ms)',
        '<b>DOM mutation</b> -> browser repaints affected lines (~1-2ms)',
        '<b>GPU composite</b> -> frame on screen (~0-16ms until vsync)',
    ]:
        add(bul(step))
    add(sp(3))
    add(p('Total latency: <b>1-3ms</b> in a typical scenario. '
          'This is noticeably faster than competing Electron applications '
          'which spend the same ~15ms on JavaScript execution alone.'))
    add(sp(4))

    add(h3('Async Decorations — Don\'t Block Typing'))
    add(p('Inlay hints, code lens, inline completions — everything is computed '
          '<b>asynchronously after</b> the TextModel update. '
          'The user sees the text instantly; decorations appear slightly later.'))
    add(sp(3))
    add(p('VS Code does not provide a built-in debounce API. '
          'The standard pattern is setTimeout/clearTimeout. '
          'For serious projects, use lodash.debounce or p-debounce:'))
    add(sp(3))
    add(code([
        '// There is no built-in debounce in the vscode API — use setTimeout',
        '',
        '// BAD: blocks typing',
        'vscode.workspace.onDidChangeTextDocument(e => {',
        '    const result = heavySync(e.document);',
        '    applyDecorations(result);',
        '});',
        '',
        '// GOOD: debounce via setTimeout (standard JS)',
        'let timer: ReturnType<typeof setTimeout> | undefined;',
        '',
        'vscode.workspace.onDidChangeTextDocument(e => {',
        '    clearTimeout(timer);',
        '    timer = setTimeout(async () => {',
        '        const result = await heavyAsync(e.document);',
        '        applyDecorations(result);',
        '    }, 150);   // 150ms — balance between responsiveness and load',
        '});',
        '',
        '// GOOD: with cancellation via CancellationTokenSource (more robust)',
        'let cts = new vscode.CancellationTokenSource();',
        '',
        'vscode.workspace.onDidChangeTextDocument(e => {',
        '    cts.cancel();            // cancel previous',
        '    cts = new vscode.CancellationTokenSource();',
        '    const token = cts.token;',
        '    setTimeout(async () => {',
        '        if (token.isCancellationRequested) return;',
        '        const result = await heavyAsync(e.document, token);',
        '        if (!token.isCancellationRequested) applyDecorations(result);',
        '    }, 150);',
        '});',
        '',
        '// Also: es-toolkit (modern lodash replacement, actively maintained)',
        '// npm install es-toolkit',
        '// import { debounce, throttle } from "es-toolkit";',
        '// const update = debounce(async (doc) => { ... }, 150);',
        '// es-toolkit: 2-3x faster than lodash, 97% smaller, built-in TypeScript',
    ]))
    add(sp(3))
    add(p('Three approaches to handling document changes: synchronous (blocks typing — bad), debounce via <b>setTimeout</b> (standard JS pattern, 150ms delay), and debounce with <b>CancellationTokenSource</b> (more robust — cancels the previous request on new input). CancellationToken is passed to all async VS Code providers — check <b>token.isCancellationRequested</b> before expensive operations.'))
    add(sp(6))

    # -- 8. LESSONS FOR EXTENSIONS ---------------------------------------------
    add(h1('8. How to Apply This in Your Extension'))
    add(hl(C['blue']))
    add(sp(4))

    add(h2('Lesson 1: Activation Events — Copy VS Code\'s Strategy'))
    add(p('VS Code lazy-loads everything. Your extension should do the same:'))
    add(sp(3))
    add(code([
        '// Bad: activates on every VS Code startup',
        '"activationEvents": ["*"]',
        '',
        '// Good: only for your language',
        '"activationEvents": ["onLanguage:python"]',
        '',
        '// Better: workspaceContains — only if the project has our file',
        '"activationEvents": ["workspaceContains:**/pyproject.toml"]',
        '',
        '// Best (VS Code 1.74+): declare commands and Views —',
        '// activation events are generated automatically',
        '// Only non-standard ones need explicit declaration',
    ]))
    add(sp(3))
    add(p('Four levels of Activation Events from worst to best: <b>"*"</b> loads the extension on every startup, <b>onLanguage</b> — when a file of the target language is opened, <b>workspaceContains</b> — only if the project has a specific file. Starting from VS Code 1.74, events are generated automatically from declared commands and Views.'))

    add(sp(6))

    add(h2('Lesson 2: Bundle Like VS Code — One File'))
    add(p('The VS Code bundle is one large file, not a thousand small ones. '
          'The reason: V8 code cache works more efficiently with a single large file. '
          'The overhead of require() is paid once at load time. '
          'For extensions — the same applies:'))
    add(sp(3))
    add(code([
        '// esbuild.js — proper configuration',
        'await esbuild.context({',
        '    entryPoints: ["src/extension.ts"],',
        '    bundle: true,           // all dependencies in one file',
        '    minify: production,     // smaller file = faster parse',
        '    platform: "node",',
        '    outfile: "dist/extension.js",  // ONE file, not a folder',
        '    external: ["vscode"],   // don\'t include vscode — loaded at runtime',
        '});',
        '',
        '// package.json: main must point to the bundled file',
        '"main": "./dist/extension.js"  // not ./out/extension.js (unbundled)',
    ]))
    add(sp(3))
    add(p('<b>esbuild</b> configuration for bundling an extension into a single file: bundle combines all dependencies, minify reduces size for production, <b>external: ["vscode"]</b> excludes the VS Code API — it is provided at runtime. The <b>main</b> field in package.json must point to the bundled file in dist/, not the source files in out/.'))

    add(sp(6))

    add(h2('Lesson 3: Incremental Updates — Don\'t Recompute Everything'))
    add(p('VS Code only updates what has changed. '
          'Your extension should do the same — don\'t scan the entire workspace '
          'on every file change:'))
    add(sp(3))
    add(code([
        '// Bad: full scan on every change',
        'vscode.workspace.onDidSaveTextDocument(async doc => {',
        '    const allFiles = await vscode.workspace.findFiles("**/*.ts");',
        '    await rebuildIndex(allFiles);  // 500ms every time',
        '});',
        '',
        '// Good: incremental update for the changed file only',
        'const indexCache = new Map<string, IndexEntry>();',
        '',
        'vscode.workspace.onDidSaveTextDocument(async doc => {',
        '    if (doc.languageId !== "typescript") return;',
        '    // Update only this file',
        '    indexCache.set(doc.uri.toString(), await indexFile(doc));',
        '    onIndexUpdated.fire(doc.uri);',
        '});',
        '',
        '// FileSystemWatcher for external changes',
        'const watcher = vscode.workspace.createFileSystemWatcher("**/*.ts");',
        'watcher.onDidChange(uri => indexCache.delete(uri.toString()));',
        'context.subscriptions.push(watcher);',
    ]))
    add(sp(3))
    add(p('Incremental index pattern: instead of a full workspace scan on every save — update only the changed file in a <b>Map cache</b>. <b>onDidSaveTextDocument</b> updates the entry for a specific file, <b>FileSystemWatcher</b> invalidates the cache on external changes (git pull, branch switch).'))

    add(sp(6))

    add(h2('Lesson 4: Async Decorations — Don\'t Block the Cursor'))
    add(p('VS Code pattern: the user sees the character instantly, '
          'decorations appear after ~150ms. Copy this pattern:'))
    add(sp(3))
    add(quote(
        'When they crossed that 100ms barrier, a qualitative change happened. '
        'People changed their views of a tool from something they have to cope with '
        "to something that's fun, valuable, and eventually became their second nature. "
        'Speed is a feature.',
        'Nikita Prokopov (tonsky)', 'Speed is a feature, tonsky.me, 2018'
    ))
    add(sp(4))
    add(code([
        'let decorationTimer: NodeJS.Timeout | null = null;',
        'let cancelled = false;',
        '',
        'vscode.window.onDidChangeTextEditorSelection(event => {',
        '    // Cancel previous request',
        '    if (decorationTimer) clearTimeout(decorationTimer);',
        '    cancelled = true;',
        '',
        '    decorationTimer = setTimeout(() => {',
        '        cancelled = false;',
        '        computeDecorations(event.textEditor).then(ranges => {',
        '            if (!cancelled) {',
        '                event.textEditor.setDecorations(decorationType, ranges);',
        '            }',
        '        });',
        '    }, 150);  // 150ms debounce — balance between responsiveness and CPU',
        '});',
    ]))
    add(sp(3))
    add(p('Debounce pattern for decorations: on selection change, the previous request is cancelled via <b>clearTimeout</b>, and a new one is scheduled with a 150ms delay. The <b>cancelled</b> flag prevents applying stale results — if the user moves the cursor in time, old decorations won\'t be applied.'))

    add(sp(6))

    add(h2('Lesson 5: Measure First — Don\'t Optimize Blindly'))
    add(p('VS Code measures everything: time to first frame, latency of every operation, '
          'bundle size. Do the same for your extension:'))
    add(sp(3))
    add(code([
        '// Measuring activation time',
        'export async function activate(context: vscode.ExtensionContext) {',
        '    const t0 = Date.now();',
        '',
        '    await doInitialization();',
        '',
        '    const ms = Date.now() - t0;',
        '    if (ms > 100) {',
        '        // Log to Output Channel for diagnostics',
        '        output.appendLine(`[WARN] Slow activation: ${ms}ms`);',
        '    }',
        '    // Send to telemetry if available',
        '    reporter.sendTelemetryEvent("activation", {}, { activationMs: ms });',
        '}',
        '',
        '// Developer: Show Running Extensions — built-in profiler',
        '// Shows activation time of each extension',
        '// Use Developer: Open Process Explorer for CPU/memory',
    ]))
    add(sp(3))
    add(p('Measuring extension activation time: <b>Date.now()</b> before and after initialization, logging to Output Channel when a threshold is exceeded (100ms). The built-in command <b>Developer: Show Running Extensions</b> shows activation time for all extensions, <b>Process Explorer</b> — CPU and memory consumption.'))

    add(sp(4))

    add(h2('Lesson 6: Workers for Heavy Computation'))
    add(p('VS Code offloads the TypeScript compiler, search, and other heavy operations '
          'to separate processes/workers. '
          'Your extension can do the same via Node.js worker_threads:'))
    add(sp(3))
    add(code([
        '// Heavy computation — in a worker thread',
        'import { Worker, isMainThread, parentPort } from "worker_threads";',
        '',
        '// src/heavy-worker.ts',
        'if (!isMainThread) {',
        '    parentPort!.on("message", async (data) => {',
        '        const result = await doHeavyComputation(data);',
        '        parentPort!.postMessage(result);',
        '    });',
        '}',
        '',
        '// src/extension.ts',
        'const worker = new Worker(',
        '    path.join(context.extensionPath, "dist", "heavy-worker.js")',
        ');',
        '',
        'function runHeavyTask(input: any): Promise<any> {',
        '    return new Promise((resolve, reject) => {',
        '        worker.once("message", resolve);',
        '        worker.once("error", reject);',
        '        worker.postMessage(input);',
        '    });',
        '}',
        '',
        '// Extension Host = separate process (already good),',
        '// but a worker inside it = one more level of isolation',
        '// for CPU-intensive operations',
    ]))
    add(sp(3))
    add(p('Offloading heavy computation to <b>worker_threads</b>: the worker listens for messages via <b>parentPort</b>, executes the task, and sends the result back. The main thread creates a Worker from a bundled file and wraps communication in a Promise. The Extension Host already runs in a separate process, but a worker inside it adds one more level of isolation for CPU-intensive tasks.'))

    add(sp(6))

    add(h2('Real Numbers: Good and Bad'))
    add(p('Data from public VS Code extension performance analyses '
          '(source: freecodecamp.org/news/optimize-vscode-performance-best-extensions):'))
    add(sp(3))
    add(tblh(['Extension', 'Activation time / approach']))
    add(tbl2([
        ('GitLens (~6.5M installs)',
         '35ms — despite complex functionality. '
         'The secret: heavy operations (git blame, graph) are computed lazily, '
         'only on the first file open, not at startup'),
        ('rust-analyzer',
         'The server starts asynchronously — VS Code opens immediately. '
         'A progress bar in the Status Bar shows background indexing. '
         'Typing is instant even while the LSP is still loading'),
        ('An analyzed extension',
         '2513ms — activationEvents:["*"], no bundling (2.5MB of files). '
         'That\'s 2.5 seconds added to every VS Code startup. '
         'A user with 10 such extensions — startup takes 30+ seconds'),
        ('Target metrics',
         '< 50ms — excellent (like rust-analyzer). '
         '< 100ms — good. '
         '< 300ms — acceptable. '
         '> 500ms — needs optimization: bundling, lazy loading. '
         'Source: nicoespeon.com/en/2019/11/fix-vscode-extension-performance-issue/'),
    ]))
    add(sp(6))

    # -- SUMMARY TABLE ----------------------------------------------------------
    add(h1('Summary: Performance Cheat Sheet'))
    add(hl(C['blue']))
    add(sp(4))

    add(tblh(['VS Code Technique', 'Extension Equivalent']))
    add(tbl2([
        ('Lazy-load extensions via Activation Events',
         'Proper activationEvents. Never "*"'),
        ('V8 Code Caching / one large bundle',
         'esbuild bundle into one file. minify: true in production'),
        ('AMD -> ESM (+10% startup)',
         'Still CJS. Track github.com/microsoft/vscode/issues/130367'),
        ('Line virtualization in Monaco',
         'Virtualize long lists in Webview (react-virtual and similar)'),
        ('Async tokenization / don\'t block the cursor',
         'Debounce 100-200ms for heavy operations in onDidChangeTextDocument'),
        ('Incremental TypeScript compiler',
         'Invalidate only changed files in cache, don\'t rebuild everything'),
        ('MessagePort IPC without main process',
         'Worker threads for CPU-intensive tasks in extensions'),
        ('Measure first: time to first frame',
         'Log activate() time and send to telemetry'),
        ('UtilityProcess with V8 sandbox',
         'Since VS Code 1.94, the Extension Host runs in UtilityProcess with V8 sandbox enabled. '
         'Native addons (.node files, C++/Rust via N-API) run outside this isolation '
         'and have direct access to process memory — a potential vulnerability. '
         'Additionally, native addons are compiled for a specific Electron version (not Node.js) '
         'and break on every VS Code update. '
         'Addons using external array buffers are incompatible with V8 sandbox and will crash. '
         'If you need a native addon — use napi_create_buffer_copy instead of external buffers, '
         'or move the addon to a child process via worker_threads. '
         'Source: code.visualstudio.com/updates/v1_94 (section Remove custom allocator in the desktop app)'),
    ]))
    add(sp(4))

    add(quote(
        'Performance is not a feature you add at the end. '
        'It\'s a consequence of every decision you make during development. '
        'VS Code\'s performance comes from a decade of small, consistent choices.',
        'Benjamin Pasero', 'VS Code Core Team, Microsoft — author of the sandboxing blog post'
    ))
    add(pb())

    return A


if __name__ == '__main__':
    print(f'Performance chapter: {len(build_perf_chapter())} elements')
