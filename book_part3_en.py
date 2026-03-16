from book_helpers import *

def build_story_part3():
    A = []
    def add(*x):
        for i in x: A.append(i)
    def ch(num, title, sub=''):
        part = f'Chapter {num}' if str(num).replace('.','').isdigit() else str(num)
        label = f'{part}: {title}' if str(num).replace('.','').isdigit() else title
        add(StableAnchor(f'chapter_{num}'))
        add(toc_ch(label), banner(part, title, sub), sp(12))

    # ── PRACTICAL EXAMPLES ───────────────────────────────────────────────────
    add(StableAnchor('chapter_practice'))
    add(banner('Practice', 'Practical Examples', 'Real extensions from idea to publication'), sp(12))

    add(h2('Example 1: Extension for Working with TODO Comments'))
    add(p('Let\'s create a full-featured extension that finds TODO comments in code, displays them in a Tree View, and allows quick navigation to them. This is a good example that covers several APIs at once.'))
    add(sp(4))

    add(h3('Manifest — package.json'))
    add(code([
        '{',
        '  "name": "todo-highlighter",',
        '  "displayName": "TODO Highlighter",',
        '  "description": "Finds TODO/FIXME in code and displays them in Tree View",',
        '  "version": "1.0.0",',
        '  "publisher": "my-publisher",',
        '  "engines": { "vscode": "^1.90.0" },',
        '  "categories": ["Other"],',
        '  "activationEvents": ["onStartupFinished"],',
        '  "main": "./dist/extension.js",',
        '  "contributes": {',
        '    "views": {',
        '      "explorer": [{',
        '        "id": "todoList",',
        '        "name": "TODO List",',
        '        "icon": "$(checklist)"',
        '      }]',
        '    },',
        '    "commands": [',
        '      {',
        '        "command": "todoHighlighter.refresh",',
        '        "title": "TODO: Refresh List",',
        '        "icon": "$(refresh)"',
        '      },',
        '      {',
        '        "command": "todoHighlighter.goToTodo",',
        '        "title": "TODO: Go to Item"',
        '      }',
        '    ],',
        '    "menus": {',
        '      "view/title": [{',
        '        "command": "todoHighlighter.refresh",',
        '        "when": "view == todoList",',
        '        "group": "navigation"',
        '      }]',
        '    },',
        '    "configuration": {',
        '      "title": "TODO Highlighter",',
        '      "properties": {',
        '        "todoHighlighter.keywords": {',
        '          "type": "array",',
        '          "items": { "type": "string" },',
        '          "default": ["TODO", "FIXME", "HACK", "NOTE"],',
        '          "description": "Keywords to search for"',
        '        },',
        '        "todoHighlighter.filePattern": {',
        '          "type": "string",',
        '          "default": "**/*.{ts,js,py,rs,go}",',
        '          "description": "Glob pattern for files to search"',
        '        }',
        '      }',
        '    }',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('The manifest declares everything the extension provides to VS Code. <b>views</b> registers a TODO List panel in Explorer. <b>commands</b> adds two commands — list refresh and navigation to an item. <b>menus</b> places a refresh button in the panel header. <b>configuration</b> allows the user to customize keywords and glob pattern through the Settings UI.'))

    add(sp(6))

    add(h3('Data Model'))
    add(code([
        '// src/models.ts',
        '',
        'export interface TodoItem {',
        '    file: string;       // full path to the file',
        '    line: number;       // line number (0-based)',
        '    keyword: string;    // TODO, FIXME, etc.',
        '    text: string;       // full comment text',
        '    column: number;     // position in the line',
        '}',
        '',
        'export interface TodoFile {',
        '    path: string;       // file path',
        '    items: TodoItem[];  // list of TODOs in the file',
        '}',
    ]))
    add(sp(3))
    add(p('The extension\'s data model. <b>TodoItem</b> describes a single found keyword: file, line, column, type (TODO/FIXME), and comment text. <b>TodoFile</b> groups all TodoItems of a single file — this structure maps directly to a two-level Tree View.'))

    add(sp(6))

    add(h3('File Scanner'))
    add(code([
        '// src/scanner.ts',
        'import * as vscode from \'vscode\';',
        'import { TodoItem, TodoFile } from \'./models\';',
        '',
        'export class TodoScanner {',
        '',
        '    private getKeywords(): string[] {',
        '        const cfg = vscode.workspace.getConfiguration(\'todoHighlighter\');',
        '        return cfg.get<string[]>(\'keywords\', [\'TODO\', \'FIXME\']);',
        '    }',
        '',
        '    private getFilePattern(): string {',
        '        const cfg = vscode.workspace.getConfiguration(\'todoHighlighter\');',
        '        return cfg.get<string>(\'filePattern\', \'**/*.{ts,js}\');',
        '    }',
        '',
        '    async scan(): Promise<TodoFile[]> {',
        '        const pattern = this.getFilePattern();',
        '        const keywords = this.getKeywords();',
        '',
        '        // Create regex for search',
        '        const kwPattern = keywords.map(k => `\\\\b${k}\\\\b`).join(\'|\');',
        '        const regex = new RegExp(`(${kwPattern})[:\\\\s]+(.*)`, \'gi\');',
        '',
        '        // Find all files matching the pattern',
        '        const uris = await vscode.workspace.findFiles(',
        '            pattern,',
        '            \'**/node_modules/**\'',
        '        );',
        '',
        '        const results: TodoFile[] = [];',
        '',
        '        for (const uri of uris) {',
        '            const doc = await vscode.workspace.openTextDocument(uri);',
        '            const items: TodoItem[] = [];',
        '',
        '            for (let i = 0; i < doc.lineCount; i++) {',
        '                const line = doc.lineAt(i).text;',
        '                let match;',
        '                regex.lastIndex = 0;',
        '',
        '                while ((match = regex.exec(line)) !== null) {',
        '                    items.push({',
        '                        file: uri.fsPath,',
        '                        line: i,',
        '                        keyword: match[1].toUpperCase(),',
        '                        text: match[2].trim(),',
        '                        column: match.index',
        '                    });',
        '                }',
        '            }',
        '',
        '            if (items.length > 0) {',
        '                results.push({ path: uri.fsPath, items });',
        '            }',
        '        }',
        '',
        '        return results.sort((a, b) => a.path.localeCompare(b.path));',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('The scanner searches for TODO comments across all workspace files. <b>workspace.findFiles(pattern, exclude)</b> returns URIs matching a glob pattern, excluding node_modules. For each file, a regex from settings is run line by line. Keywords and file patterns are read from <b>workspace.getConfiguration</b> on every scan — if you need real-time reaction to settings changes, subscribe to <b>workspace.onDidChangeConfiguration</b>.'))
    add(sp(6))

    add(h3('Tree View Provider'))
    add(code([
        '// src/provider.ts',
        'import * as vscode from \'vscode\';',
        'import * as path from \'path\';',
        'import { TodoScanner } from \'./scanner\';',
        'import { TodoFile, TodoItem } from \'./models\';',
        '',
        'type TreeNode = TodoFile | TodoItem;',
        '',
        'export class TodoTreeProvider',
        '    implements vscode.TreeDataProvider<TreeNode> {',
        '',
        '    private _onChange = new vscode.EventEmitter<TreeNode | undefined>();',
        '    readonly onDidChangeTreeData = this._onChange.event;',
        '',
        '    private _data: TodoFile[] = [];',
        '    private _scanner = new TodoScanner();',
        '',
        '    async refresh() {',
        '        this._data = await this._scanner.scan();',
        '        this._onChange.fire(undefined);',
        '    }',
        '',
        '    getTreeItem(node: TreeNode): vscode.TreeItem {',
        '        if (\'items\' in node) {',
        '            // This is a file',
        '            const item = new vscode.TreeItem(',
        '                path.basename(node.path),',
        '                vscode.TreeItemCollapsibleState.Expanded',
        '            );',
        '            item.description = `${node.items.length} TODO`;',
        '            item.tooltip = node.path;',
        '            item.resourceUri = vscode.Uri.file(node.path);',
        '            item.iconPath = vscode.ThemeIcon.File;',
        '            return item;',
        '        } else {',
        '            // This is a TODO item',
        '            const colors: Record<string, string> = {',
        '                TODO:  \'charts.yellow\',',
        '                FIXME: \'charts.red\',',
        '                HACK:  \'charts.orange\',',
        '                NOTE:  \'charts.blue\',',
        '            };',
        '            const item = new vscode.TreeItem(',
        '                `${node.keyword}: ${node.text}`,',
        '                vscode.TreeItemCollapsibleState.None',
        '            );',
        '            item.description = `Line ${node.line + 1}`;',
        '            item.iconPath = new vscode.ThemeIcon(',
        '                \'circle-filled\',',
        '                new vscode.ThemeColor(colors[node.keyword] || \'charts.yellow\')',
        '            );',
        '            item.command = {',
        '                command: \'todoHighlighter.goToTodo\',',
        '                title: \'Go to\',',
        '                arguments: [node]',
        '            };',
        '            item.contextValue = \'todoItem\';',
        '            return item;',
        '        }',
        '    }',
        '',
        '    getChildren(node?: TreeNode): TreeNode[] {',
        '        if (!node) return this._data;',
        '        if (\'items\' in node) return node.items;',
        '        return [];',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('A two-level Tree View: files at the top level, TODO items inside. <b>getTreeItem</b> distinguishes nodes via <b>\'items\' in node</b> — files get an icon and a counter, while TODO items get a colored circle by type (TODO yellow, FIXME red) and a navigation command on click. <b>EventEmitter</b> + <b>fire(undefined)</b> forces VS Code to re-request the entire tree on update.'))
    add(sp(6))

    add(h3('Main File extension.ts'))
    add(code([
        '// src/extension.ts',
        'import * as vscode from \'vscode\';',
        'import { TodoTreeProvider } from \'./provider\';',
        'import { TodoItem } from \'./models\';',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '',
        '    const provider = new TodoTreeProvider();',
        '',
        '    const view = vscode.window.createTreeView(\'todoList\', {',
        '        treeDataProvider: provider,',
        '        showCollapseAll: true',
        '    });',
        '',
        '    // Decoration for highlighting TODOs in the editor',
        '    const todoDecoration = vscode.window.createTextEditorDecorationType({',
        '        backgroundColor: \'rgba(255,200,0,0.2)\',',
        '        border: \'1px solid rgba(255,200,0,0.5)\',',
        '        borderRadius: \'2px\',',
        '    });',
        '',
        '    function highlightInEditor(editor: vscode.TextEditor) {',
        '        const keywords = [\'TODO\', \'FIXME\', \'HACK\', \'NOTE\'];',
        '        const pattern  = new RegExp(`\\\\b(${keywords.join(\'|\')})\\\\b`, \'g\');',
        '        const ranges: vscode.Range[] = [];',
        '        for (let i = 0; i < editor.document.lineCount; i++) {',
        '            const line = editor.document.lineAt(i).text;',
        '            let m;',
        '            pattern.lastIndex = 0;',
        '            while ((m = pattern.exec(line)) !== null) {',
        '                ranges.push(new vscode.Range(i, m.index, i, m.index + m[0].length));',
        '            }',
        '        }',
        '        editor.setDecorations(todoDecoration, ranges);',
        '    }',
        '',
        '    // Refresh command',
        '    const refreshCmd = vscode.commands.registerCommand(',
        '        \'todoHighlighter.refresh\', () => provider.refresh()',
        '    );',
        '',
        '    // Navigate to TODO command',
        '    const gotoCmd = vscode.commands.registerCommand(',
        '        \'todoHighlighter.goToTodo\',',
        '        async (item: TodoItem) => {',
        '            const uri = vscode.Uri.file(item.file);',
        '            const doc = await vscode.workspace.openTextDocument(uri);',
        '            const editor = await vscode.window.showTextDocument(doc);',
        '            const pos = new vscode.Position(item.line, item.column);',
        '            editor.selection = new vscode.Selection(pos, pos);',
        '            editor.revealRange(',
        '                new vscode.Range(pos, pos),',
        '                vscode.TextEditorRevealType.InCenter',
        '            );',
        '        }',
        '    );',
        '',
        '    // Listen for editor changes',
        '    const editorSub = vscode.window.onDidChangeActiveTextEditor(editor => {',
        '        if (editor) highlightInEditor(editor);',
        '    });',
        '',
        '    // Listen for file changes',
        '    const docSub = vscode.workspace.onDidSaveTextDocument(() => {',
        '        provider.refresh();',
        '    });',
        '',
        '    // Highlight in the current editor',
        '    if (vscode.window.activeTextEditor) {',
        '        highlightInEditor(vscode.window.activeTextEditor);',
        '    }',
        '',
        '    // Initial scan',
        '    provider.refresh();',
        '',
        '    context.subscriptions.push(',
        '        view, refreshCmd, gotoCmd, editorSub, docSub, todoDecoration',
        '    );',
        '}',
        '',
        'export function deactivate() {}',
    ]))
    add(sp(3))
    add(p('The entry point brings everything together. <b>createTreeView</b> creates a panel with a Collapse All button. <b>createTextEditorDecorationType</b> defines the highlighting style for TODO keywords directly in the editor. Two commands: refresh rescans files, goToTodo opens the file and places the cursor on the target line via <b>revealRange</b>. Subscriptions to <b>onDidChangeActiveTextEditor</b> and <b>onDidSaveTextDocument</b> ensure automatic updates of both highlighting and the list.'))

    add(pb())

    # ── Example 2: Status Bar with file info ─────────────────────────────────
    add(h2('Example 2: Status Bar with File Info'))
    add(p('A simple extension example that displays information about the active file in the Status Bar: line count, character count, encoding, and line endings.'))
    add(sp(3))
    add(code([
        '// extension.ts — short but complete example',
        'import * as vscode from \'vscode\';',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '',
        '    // Create a left-side item',
        '    const linesItem = vscode.window.createStatusBarItem(',
        '        vscode.StatusBarAlignment.Left, 200',
        '    );',
        '    linesItem.command = \'fileInfo.showDetails\';',
        '    linesItem.tooltip = \'Click for file details\';',
        '',
        '    // Create a right-side item',
        '    const encodingItem = vscode.window.createStatusBarItem(',
        '        vscode.StatusBarAlignment.Right, 200',
        '    );',
        '',
        '    function update(editor: vscode.TextEditor | undefined) {',
        '        if (!editor) {',
        '            linesItem.hide();',
        '            encodingItem.hide();',
        '            return;',
        '        }',
        '',
        '        const doc   = editor.document;',
        '        const lines = doc.lineCount;',
        '        const chars = doc.getText().length;',
        '        const sel   = editor.selection;',
        '        const selChars = doc.getText(sel).length;',
        '',
        '        // Lines + chars (+ selection if any)',
        '        if (selChars > 0) {',
        '            linesItem.text = `$(symbol-string) ${lines} lines  |  sel: ${selChars} chars`;',
        '        } else {',
        '            linesItem.text = `$(symbol-string) ${lines} lines, ${chars} chars`;',
        '        }',
        '        linesItem.show();',
        '',
        '        // Encoding and line endings',
        '        const eol = doc.eol === vscode.EndOfLine.LF ? \'LF\' : \'CRLF\';',
        '        encodingItem.text = `$(symbol-key) UTF-8  ${eol}`;',
        '        encodingItem.show();',
        '    }',
        '',
        '    // Details command',
        '    const detailsCmd = vscode.commands.registerCommand(',
        '        \'fileInfo.showDetails\',',
        '        () => {',
        '            const editor = vscode.window.activeTextEditor;',
        '            if (!editor) return;',
        '            const doc = editor.document;',
        '            vscode.window.showInformationMessage(',
        '                `File: ${doc.fileName}\\n` +',
        '                `Language: ${doc.languageId}\\n` +',
        '                `Lines: ${doc.lineCount}\\n` +',
        '                `Characters: ${doc.getText().length}\\n` +',
        '                `Modified: ${doc.isDirty ? \'Yes\' : \'No\'}`',
        '            );',
        '        }',
        '    );',
        '',
        '    context.subscriptions.push(',
        '        linesItem, encodingItem, detailsCmd,',
        '        vscode.window.onDidChangeActiveTextEditor(update),',
        '        vscode.window.onDidChangeTextEditorSelection(e => update(e.textEditor)),',
        '        vscode.workspace.onDidChangeTextDocument(e => {',
        '            if (e.document === vscode.window.activeTextEditor?.document)',
        '                update(vscode.window.activeTextEditor);',
        '        }),',
        '    );',
        '',
        '    update(vscode.window.activeTextEditor);',
        '}',
    ]))
    add(sp(3))
    add(p('A complete Status Bar extension example. Two items: on the left — line and character count (accounting for selection), on the right — encoding and line ending type. <b>createStatusBarItem(alignment, priority)</b> creates an item; priority determines the order within a side. Binding a <b>command</b> to an item makes it clickable — here, clicking shows information via <b>showInformationMessage</b>. Three subscriptions ensure updates: editor switch, selection change, document edit.'))

    add(pb())

    # ── DEEP DIVE: Working with the File System ──────────────────────────────
    add(banner('Deep Dive', 'Working with the File System', 'vscode.workspace.fs and FileSystemProvider'), sp(12))

    add(h2('vscode.workspace.fs API'))
    add(p('For file operations in extensions, it is recommended to use <b>vscode.workspace.fs</b> instead of the standard Node.js <b>fs</b>. This ensures compatibility with Remote Development and virtual file systems.'))
    add(sp(4))
    add(code([
        '// Working with files via vscode.workspace.fs',
        '',
        '// Reading a file',
        'const uri = vscode.Uri.file(\'/path/to/file.json\');',
        'const bytes = await vscode.workspace.fs.readFile(uri);',
        'const text = Buffer.from(bytes).toString(\'utf8\');',
        'const data = JSON.parse(text);',
        '',
        '// Writing a file',
        'const content = JSON.stringify(data, null, 2);',
        'await vscode.workspace.fs.writeFile(uri, Buffer.from(content));',
        '',
        '// Creating a directory',
        'const dirUri = vscode.Uri.file(\'/path/to/new-dir\');',
        'await vscode.workspace.fs.createDirectory(dirUri);',
        '',
        '// Getting metadata',
        'const stat = await vscode.workspace.fs.stat(uri);',
        'console.log(`Size: ${stat.size}, Type: ${stat.type}`);',
        '// FileType: Unknown=0, File=1, Directory=2, SymbolicLink=64',
        '',
        '// Reading directory contents',
        'const entries = await vscode.workspace.fs.readDirectory(dirUri);',
        '// entries: [name, type][]',
        'for (const [name, type] of entries) {',
        '    console.log(`${type === vscode.FileType.Directory ? \'[D]\' : \'[F]\'} ${name}`);',
        '}',
        '',
        '// Copying a file',
        'const destUri = vscode.Uri.file(\'/path/to/dest.json\');',
        'await vscode.workspace.fs.copy(uri, destUri, { overwrite: false });',
        '',
        '// Renaming / moving',
        'await vscode.workspace.fs.rename(uri, destUri, { overwrite: true });',
        '',
        '// Deleting',
        'await vscode.workspace.fs.delete(uri, { recursive: false, useTrash: true });',
    ]))
    add(sp(3))
    add(p('A complete set of file operations via <b>workspace.fs</b>. Reading returns a <b>Uint8Array</b> — convert it using Buffer.from().toString(). <b>stat</b> returns size and type (File, Directory, SymbolicLink). <b>readDirectory</b> provides [name, type] pairs. The copy, rename, and delete operations accept options: <b>overwrite</b> for overwriting, <b>useTrash</b> for moving to trash. All methods work with any URI scheme, not just file://.'))

    add(sp(6))

    add(h2('Custom File System (FileSystemProvider)'))
    add(p('FileSystemProvider allows creating a virtual file system with a custom URI scheme. It is used for displaying archives, remote resources, and databases as a file system.'))
    add(sp(3))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "filesystems": [{',
        '    "scheme": "memfs"',
        '  }]',
        '}',
        '',
        '// In-memory file system',
        'class MemFS implements vscode.FileSystemProvider {',
        '',
        '    private _files = new Map<string, Uint8Array>();',
        '    private _dirs  = new Set<string>();',
        '',
        '    private _onChange = new vscode.EventEmitter<vscode.FileChangeEvent[]>();',
        '    onDidChangeFile = this._onChange.event;',
        '',
        '    watch(): vscode.Disposable { return { dispose: () => {} }; }',
        '',
        '    stat(uri: vscode.Uri): vscode.FileStat {',
        '        const key = uri.path;',
        '        if (this._files.has(key)) {',
        '            return {',
        '                type: vscode.FileType.File,',
        '                ctime: Date.now(), mtime: Date.now(),',
        '                size: this._files.get(key)!.byteLength',
        '            };',
        '        }',
        '        if (this._dirs.has(key)) {',
        '            return { type: vscode.FileType.Directory, ctime: 0, mtime: 0, size: 0 };',
        '        }',
        '        throw vscode.FileSystemError.FileNotFound(uri);',
        '    }',
        '',
        '    readDirectory(uri: vscode.Uri): [string, vscode.FileType][] {',
        '        const results: [string, vscode.FileType][] = [];',
        '        const prefix = uri.path.endsWith(\'/\') ? uri.path : uri.path + \'/\';',
        '        for (const [path] of this._files) {',
        '            if (path.startsWith(prefix)) {',
        '                const name = path.slice(prefix.length).split(\'/\')[0];',
        '                if (name) results.push([name, vscode.FileType.File]);',
        '            }',
        '        }',
        '        return results;',
        '    }',
        '',
        '    readFile(uri: vscode.Uri): Uint8Array {',
        '        const data = this._files.get(uri.path);',
        '        if (!data) throw vscode.FileSystemError.FileNotFound(uri);',
        '        return data;',
        '    }',
        '',
        '    writeFile(uri: vscode.Uri, content: Uint8Array): void {',
        '        const existed = this._files.has(uri.path);',
        '        this._files.set(uri.path, content);',
        '        this._onChange.fire([{',
        '            type: existed',
        '                ? vscode.FileChangeType.Changed',
        '                : vscode.FileChangeType.Created,',
        '            uri',
        '        }]);',
        '    }',
        '',
        '    createDirectory(uri: vscode.Uri): void { this._dirs.add(uri.path); }',
        '    delete(uri: vscode.Uri): void { this._files.delete(uri.path); }',
        '    rename(oldUri: vscode.Uri, newUri: vscode.Uri): void {',
        '        const data = this._files.get(oldUri.path);',
        '        if (data) {',
        '            this._files.delete(oldUri.path);',
        '            this._files.set(newUri.path, data);',
        '        }',
        '    }',
        '}',
        '',
        '// Registration',
        'const memfs = new MemFS();',
        'context.subscriptions.push(',
        '    vscode.workspace.registerFileSystemProvider(\'memfs\', memfs, {',
        '        isCaseSensitive: true',
        '    })',
        ');',
        '',
        '// Creating a file in the virtual FS',
        'memfs.writeFile(',
        '    vscode.Uri.parse(\'memfs:/hello.ts\'),',
        '    Buffer.from(\'console.log("Hello from memfs!")\')',
        ');',
        '// Opening the file',
        'await vscode.workspace.openTextDocument(vscode.Uri.parse(\'memfs:/hello.ts\'));',
    ]))
    add(sp(3))
    add(p('An in-memory file system with a custom <b>memfs://</b> scheme. Implements all <b>FileSystemProvider</b> methods: stat, readFile, writeFile, readDirectory, createDirectory, delete, rename. <b>onDidChangeFile</b> (EventEmitter) notifies VS Code about changes — without it, Explorer won\'t update. Registration via <b>registerFileSystemProvider(scheme, provider)</b> binds the provider to a URI scheme. After that, files at memfs:/ open in the editor like regular files.'))

    add(pb())

    # ── Source Control API ─────────────────────────────────────────────────────
    add(banner('Deep Dive', 'Source Control API', 'Creating SCM Providers'), sp(12))

    add(h2('What is Source Control API'))
    add(p('Source Control API is what powers the built-in Git integration in VS Code. '
          'Extensions can create their own SCM providers for any VCS: '
          'Mercurial, SVN, Perforce, Fossil, Jujutsu. '
          'They all appear in the same Source Control sidebar with the same UX.'))
    add(sp(3))
    add(p('Real-world examples of extensions using this API: '
          '<b>vscode-hg</b> (Mercurial), <b>SVN Scm</b>, '
          '<b>Perforce for VS Code</b> (P4). '
          'Each uses createSourceControl and provides the familiar interface.'))
    add(sp(3))
    add(tblh(['Concept', 'Description']))
    add(tbl2([
        ('SourceControl\n(createSourceControl)',
         'Root provider object. Sets id, label, icon. '
         'Appears as a separate provider in the SCM panel'),
        ('SourceControlResourceGroup\n(createResourceGroup)',
         'Group of changed files. For example: "Staged", "Unstaged", "Untracked". '
         'Each group is a separate section in the SCM panel'),
        ('SourceControlResourceState',
         'A single file in a group. Contains URI, decorations (icon, color, badge), '
         'click command (usually diff)'),
        ('inputBox',
         'Input field for the commit message at the top of the SCM panel'),
        ('QuickDiffProvider',
         'Provides VS Code with the "original" version of a file for showing diff in the editor gutter'),
    ]))
    add(sp(6))

    add(h2('Full Example: Simple SCM Provider'))
    add(code([
        '// Full SCM provider example',
        'export function activate(ctx: vscode.ExtensionContext) {',
        '    // 1. Create the provider (appears in the SCM panel)',
        '    const scm = vscode.scm.createSourceControl(',
        '        \'my-vcs\',        // unique id',
        '        \'My VCS\',        // display name',
        '        vscode.Uri.file(workspaceRoot)  // repository root',
        '    );',
        '    scm.quickDiffProvider = myQuickDiffProvider;',
        '    scm.inputBox.placeholder = \'Commit message (Enter to commit)\';',
        '    scm.acceptInputCommand = {',
        '        command: \'myVcs.commit\',',
        '        title: \'Commit\',',
        '        tooltip: \'Commit changes\'',
        '    };',
        '',
        '    // 2. File groups',
        '    const stagedGroup   = scm.createResourceGroup(\'staged\',   \'Staged\');',
        '    const changedGroup  = scm.createResourceGroup(\'changes\',  \'Changes\');',
        '    const untrackedGroup = scm.createResourceGroup(\'untracked\', \'Untracked\');',
        '',
        '    // 3. Populate groups (after getting VCS status)',
        '    async function refresh() {',
        '        const status = await myVcs.getStatus(workspaceRoot);',
        '',
        '        stagedGroup.resourceStates = status.staged.map(f => ({',
        '            resourceUri: vscode.Uri.file(f.path),',
        '            decorations: {',
        '                // Letter in the SCM panel: A = Added, M = Modified, D = Deleted',
        '                letter: f.type === \'added\' ? \'A\' : f.type === \'modified\' ? \'M\' : \'D\',',
        '                color: new vscode.ThemeColor(\'gitDecoration.addedResourceForeground\'),',
        '                tooltip: f.path,',
        '            },',
        '            // On click: open diff between HEAD and working copy',
        '            command: {',
        '                command: \'vscode.diff\',',
        '                title: \'Open diff\',',
        '                arguments: [',
        '                    getOriginalUri(f.path),    // original from VCS',
        '                    vscode.Uri.file(f.path),   // working copy',
        '                    `${f.path} (HEAD)`',
        '                ]',
        '            }',
        '        }));',
        '',
        '        changedGroup.resourceStates = status.modified.map(/* ... */);',
        '        untrackedGroup.resourceStates = status.untracked.map(/* ... */);',
        '    }',
        '',
        '    // 4. Watch for file changes',
        '    const watcher = vscode.workspace.createFileSystemWatcher(\'**/*\');',
        '    watcher.onDidChange(refresh);',
        '    watcher.onDidCreate(refresh);',
        '    watcher.onDidDelete(refresh);',
        '',
        '    // 5. Register commands',
        '    ctx.subscriptions.push(',
        '        scm, stagedGroup, changedGroup, untrackedGroup, watcher,',
        '        vscode.commands.registerCommand(\'myVcs.commit\', async () => {',
        '            const message = scm.inputBox.value;',
        '            if (!message) {',
        '                vscode.window.showWarningMessage(\'Enter a commit message\');',
        '                return;',
        '            }',
        '            await myVcs.commit(workspaceRoot, message);',
        '            scm.inputBox.value = \'\';  // clear the field after commit',
        '            refresh();',
        '        }),',
        '    );',
        '',
        '    refresh(); // initial load',
        '}',
    ]))


    add(sp(4))
    add(p('<b>Key aspects:</b> it\'s better to call createResourceGroup once during activation. '
          'resourceStates is a property, not a method: simply assign a new array on each '
          'update, and VS Code will redraw the panel automatically. '
          'acceptInputCommand fires when pressing Enter or the checkmark button above the input field.'))
    add(sp(4))
    add(box('QuickDiffProvider — change indicators in the editor',
        'If you want green/red/blue bars to appear in the editor gutter '
        '(like for Git), implement QuickDiffProvider: '
        'provideOriginalResource(uri) should return the URI of the original file (from VCS). '
        'VS Code will compute the diff and show the bars itself. '
        'Documentation: code.visualstudio.com/api/extension-guides/scm-provider',
        'tip'))
    add(pb())

    # ── Debug Adapter Protocol ─────────────────────────────────────────────────
    add(banner('Deep Dive', 'Debugger Extension', 'Debug Adapter Protocol — creating debuggers'), sp(12))

    add(h2('Debug Adapter Architecture'))
    add(p('Debugger Extension allows creating debuggers for any language and runtime. Communication happens via the <b>Debug Adapter Protocol (DAP)</b> — another open protocol by Microsoft.'))
    add(sp(4))
    add(tblh(['Component', 'Description']))
    add(tbl2([
        ('VS Code (DAP Client)',  'Sends requests: launch, set breakpoint, continue, get variables'),
        ('Debug Adapter',        'Translates DAP into commands for the real debugger. Separate process'),
        ('Runtime / Debugger',   'The real debugger: gdb, lldb, node inspector, jvm debugger, etc.'),
    ]))
    add(sp(4))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "debuggers": [{',
        '    "type": "my-debugger",',
        '    "label": "My Debugger",',
        '    "languages": ["mylang"],',
        '    "configurationAttributes": {',
        '      "launch": {',
        '        "required": ["program"],',
        '        "properties": {',
        '          "program": {',
        '            "type": "string",',
        '            "description": "Path to the program to debug"',
        '          },',
        '          "stopOnEntry": {',
        '            "type": "boolean",',
        '            "default": false',
        '          }',
        '        }',
        '      }',
        '    },',
        '    "initialConfigurations": [{',
        '      "type": "my-debugger",',
        '      "request": "launch",',
        '      "name": "Launch Program",',
        '      "program": "${file}"',
        '    }]',
        '  }],',
        '  "breakpoints": [{ "language": "mylang" }]',
        '}',
        '',
        '// Debug Adapter Factory registration',
        'class MyDebugAdapterFactory',
        '    implements vscode.DebugAdapterDescriptorFactory {',
        '    createDebugAdapterDescriptor(',
        '        session: vscode.DebugSession',
        '    ): vscode.DebugAdapterDescriptor {',
        '        // Launch DA as a separate process',
        '        return new vscode.DebugAdapterExecutable(',
        '            \'node\',',
        '            [context.asAbsolutePath(\'./out/debug-adapter.js\')]',
        '        );',
        '    }',
        '}',
        '',
        'context.subscriptions.push(',
        '    vscode.debug.registerDebugAdapterDescriptorFactory(',
        '        \'my-debugger\',',
        '        new MyDebugAdapterFactory()',
        '    )',
        ');',
    ]))
    add(sp(3))
    add(p('Two steps: manifest and factory. In <b>package.json</b>, the <b>debuggers</b> section declares the debugger type, supported languages, and launch configuration attributes (program, stopOnEntry). <b>initialConfigurations</b> is a template for auto-generating launch.json. <b>breakpoints</b> enables setting breakpoints in files of the specified language. <b>DebugAdapterDescriptorFactory</b> launches the Debug Adapter as a separate process via <b>DebugAdapterExecutable</b> — VS Code communicates with it over DAP through stdin/stdout.'))

    add(sp(4))
    add(box('@vscode/debugadapter library',
        'To create a Debug Adapter, use the @vscode/debugadapter library. '
        'It provides a base DebugSession class with ready-made handlers for all DAP messages.',
        'tip'))
    add(pb())

    # ── Task Provider ──────────────────────────────────────────────────────────
    add(banner('Deep Dive', 'Task Provider', 'Automatic task creation for the workspace'), sp(12))

    add(h2('What is a Task Provider?'))
    add(p('Task Provider allows an extension to automatically provide tasks based on workspace contents. For example, a Make extension can automatically create tasks from a Makefile.'))
    add(sp(4))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "taskDefinitions": [{',
        '    "type": "make",',
        '    "properties": {',
        '      "target": {',
        '        "type": "string",',
        '        "description": "Make target"',
        '      }',
        '    }',
        '  }]',
        '}',
        '',
        '// Task Provider',
        'class MakeTaskProvider implements vscode.TaskProvider {',
        '',
        '    static MakeType = \'make\';',
        '    private makePromise: Thenable<vscode.Task[]> | undefined;',
        '',
        '    provideTasks(): Thenable<vscode.Task[]> {',
        '        if (!this.makePromise) {',
        '            this.makePromise = this.getMakeTasks();',
        '        }',
        '        return this.makePromise;',
        '    }',
        '',
        '    resolveTask(task: vscode.Task): vscode.Task | undefined {',
        '        const target = task.definition.target;',
        '        if (target) {',
        '            const def = task.definition;',
        '            return new vscode.Task(',
        '                def, task.scope ?? vscode.TaskScope.Workspace,',
        '                target, \'make\',',
        '                new vscode.ShellExecution(`make ${target}`)',
        '            );',
        '        }',
        '        return undefined;',
        '    }',
        '',
        '    private async getMakeTasks(): Promise<vscode.Task[]> {',
        '        const makefiles = await vscode.workspace.findFiles(\'**/Makefile\');',
        '        const tasks: vscode.Task[] = [];',
        '',
        '        for (const mf of makefiles) {',
        '            const doc = await vscode.workspace.openTextDocument(mf);',
        '            const text = doc.getText();',
        '            // Find targets: lines like "target:"',
        '            const targets = [...text.matchAll(/^([a-zA-Z][\\w-]*):(?!:)/gm)]',
        '                .map(m => m[1]);',
        '',
        '            for (const target of targets) {',
        '                const task = new vscode.Task(',
        '                    { type: \'make\', target },',
        '                    vscode.TaskScope.Workspace,',
        '                    target, \'make\',',
        '                    new vscode.ShellExecution(`make ${target}`),',
        '                    \'$gcc\'  // problem matcher',
        '                );',
        '                task.group = vscode.TaskGroup.Build;',
        '                tasks.push(task);',
        '            }',
        '        }',
        '',
        '        return tasks;',
        '    }',
        '}',
        '',
        '// Registration',
        'context.subscriptions.push(',
        '    vscode.tasks.registerTaskProvider(MakeTaskProvider.MakeType, new MakeTaskProvider())',
        ');',
    ]))
    add(sp(3))
    add(p('<b>TaskProvider</b> adds tasks to Tasks: Run Task. <b>ShellExecution(command)</b> runs the command in a shell; <b>ProcessExecution(path, args)</b> runs a process directly without a shell. <b>TaskGroup.Build</b> makes the task available via Ctrl+Shift+B.'))
    add(pb())

    # ── Authentication Provider ────────────────────────────────────────────────
    add(banner('Deep Dive', 'Authentication API', 'User authentication in extensions'), sp(12))

    add(h2('Working with Authentication'))
    add(p('VS Code provides a unified Authentication API for obtaining tokens from OAuth providers. Built-in providers: GitHub and Microsoft. Extensions can register their own providers.'))
    add(sp(4))

    add(h3('Using Existing Providers'))
    add(code([
        '// Get a GitHub token',
        'async function getGitHubToken(): Promise<string | undefined> {',
        '    try {',
        '        const session = await vscode.authentication.getSession(',
        '            \'github\',',
        '            [\'repo\', \'read:user\'],  // OAuth scopes',
        '            { createIfNone: true }    // prompt login if none exists',
        '        );',
        '        return session.accessToken;',
        '    } catch (e) {',
        '        vscode.window.showErrorMessage(\'Failed to obtain GitHub token\');',
        '        return undefined;',
        '    }',
        '}',
        '',
        '// Get a Microsoft token',
        'async function getMicrosoftToken(): Promise<string | undefined> {',
        '    const session = await vscode.authentication.getSession(',
        '        \'microsoft\',',
        '        [\'https://management.azure.com/.default\'],',
        '        { createIfNone: false }  // silent, no dialog',
        '    );',
        '    return session?.accessToken;',
        '}',
        '',
        '// Listen for session changes',
        'vscode.authentication.onDidChangeSessions(e => {',
        '    if (e.provider.id === \'github\') {',
        '        console.log(\'GitHub session changed\');',
        '    }',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('<b>authentication.getSession(providerId, scopes)</b> requests an OAuth session. VS Code shows a dialog only with <b>createIfNone: true</b>. Tokens are cached and refreshed automatically — do not store them manually. <b>onDidChangeSessions</b> notifies about logout or account switch.'))
    add(sp(6))

    add(h3('Creating a Custom Authentication Provider'))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "authentication": [{',
        '    "id": "my-auth-provider",',
        '    "label": "My Service"',
        '  }]',
        '}',
        '',
        '// AuthenticationProvider',
        'class MyAuthProvider implements vscode.AuthenticationProvider {',
        '',
        '    private _sessions: vscode.AuthenticationSession[] = [];',
        '    private _onChange = new vscode.EventEmitter<',
        '        vscode.AuthenticationProviderAuthenticationSessionsChangeEvent',
        '    >();',
        '    readonly onDidChangeSessions = this._onChange.event;',
        '',
        '    async getSessions(scopes?: string[]): Promise<vscode.AuthenticationSession[]> {',
        '        return this._sessions;',
        '    }',
        '',
        '    async createSession(scopes: string[]): Promise<vscode.AuthenticationSession> {',
        '        // Open browser for OAuth',
        '        const token = await this.authenticateWithOAuth();',
        '',
        '        const session: vscode.AuthenticationSession = {',
        '            id: `session-${Date.now()}`,',
        '            accessToken: token,',
        '            account: { id: \'user\', label: \'User Name\' },',
        '            scopes,',
        '        };',
        '',
        '        this._sessions.push(session);',
        '        this._onChange.fire({ added: [session], removed: [], changed: [] });',
        '        return session;',
        '    }',
        '',
        '    async removeSession(id: string): Promise<void> {',
        '        const idx = this._sessions.findIndex(s => s.id === id);',
        '        if (idx >= 0) {',
        '            const [removed] = this._sessions.splice(idx, 1);',
        '            this._onChange.fire({ added: [], removed: [removed], changed: [] });',
        '        }',
        '    }',
        '',
        '    private async authenticateWithOAuth(): Promise<string> {',
        '        // OAuth flow implementation...',
        '        return \'oauth-token\';',
        '    }',
        '}',
        '',
        'context.subscriptions.push(',
        '    vscode.authentication.registerAuthenticationProvider(',
        '        \'my-auth-provider\',',
        '        \'My Service\',',
        '        new MyAuthProvider(),',
        '        { supportsMultipleAccounts: false }',
        '    )',
        ');',
    ]))
    add(sp(3))
    add(p('Implementation of a custom OAuth provider. The <b>AuthenticationProvider</b> interface requires three methods: <b>getSessions</b> returns active sessions, <b>createSession</b> launches the OAuth flow and creates a new session, <b>removeSession</b> performs logout. The EventEmitter <b>onDidChangeSessions</b> notifies VS Code about session additions or removals. Registration via <b>registerAuthenticationProvider</b> with the <b>supportsMultipleAccounts</b> option.'))
    add(pb())

    # ── Notebook API ───────────────────────────────────────────────────────────
    add(StableAnchor('chapter_notebook'))
    add(banner('Deep Dive', 'Notebook API', 'Creating interactive notebooks in VS Code'), sp(12))

    add(h2('Notebook API Overview'))
    add(p('Notebook API allows creating interactive documents in the style of Jupyter Notebook right inside VS Code. The built-in Jupyter extension uses the same API.'))
    add(sp(4))
    add(tblh(['Component', 'Description']))
    add(tbl2([
        ('NotebookSerializer', 'Reads/writes the file format. Converts bytes to/from NotebookData'),
        ('NotebookController',  'Executes cells. Sends output back to VS Code'),
        ('NotebookRenderer',   'Optional custom renderer for rich output'),
    ]))
    add(sp(4))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "notebooks": [{',
        '    "type": "my-notebook",',
        '    "displayName": "My Notebook",',
        '    "selector": [{ "filenamePattern": "*.mynb" }]',
        '  }]',
        '}',
        '',
        '// Serializer — reading and writing the format',
        'class MyNotebookSerializer implements vscode.NotebookSerializer {',
        '',
        '    async deserializeNotebook(data: Uint8Array): Promise<vscode.NotebookData> {',
        '        const json = JSON.parse(Buffer.from(data).toString());',
        '        return new vscode.NotebookData(',
        '            json.cells.map((c: any) => new vscode.NotebookCellData(',
        '                c.kind === \'code\'',
        '                    ? vscode.NotebookCellKind.Code',
        '                    : vscode.NotebookCellKind.Markup,',
        '                c.source,',
        '                c.language || \'python\'',
        '            ))',
        '        );',
        '    }',
        '',
        '    async serializeNotebook(data: vscode.NotebookData): Promise<Uint8Array> {',
        '        const json = {',
        '            cells: data.cells.map(c => ({',
        '                kind: c.kind === vscode.NotebookCellKind.Code ? \'code\' : \'markup\',',
        '                source: c.value,',
        '                language: c.languageId',
        '            }))',
        '        };',
        '        return Buffer.from(JSON.stringify(json, null, 2));',
        '    }',
        '}',
        '',
        '// Controller — cell execution',
        'const controller = vscode.notebooks.createNotebookController(',
        '    \'my-nb-controller\',',
        '    \'my-notebook\',',
        '    \'My Kernel\'',
        ');',
        'controller.supportedLanguages = [\'python\'];',
        '',
        'controller.executeHandler = async (cells, _notebook, _controller) => {',
        '    for (const cell of cells) {',
        '        const exec = controller.createNotebookCellExecution(cell);',
        '        exec.start(Date.now());',
        '        try {',
        '            const output = await runCode(cell.document.getText());',
        '            exec.replaceOutput([',
        '                new vscode.NotebookCellOutput([',
        '                    vscode.NotebookCellOutputItem.text(output)',
        '                ])',
        '            ]);',
        '            exec.end(true);',
        '        } catch (e: any) {',
        '            exec.replaceOutput([',
        '                new vscode.NotebookCellOutput([',
        '                    vscode.NotebookCellOutputItem.error({',
        '                        name: \'Error\', message: e.message',
        '                    })',
        '                ])',
        '            ]);',
        '            exec.end(false);',
        '        }',
        '    }',
        '};',
        '',
        'context.subscriptions.push(',
        '    vscode.workspace.registerNotebookSerializer(\'my-notebook\', new MyNotebookSerializer()),',
        '    controller',
        ');',
    ]))
    add(sp(3))
    add(p('Two notebook components. <b>NotebookSerializer</b> converts a file into <b>NotebookData</b> with an array of cells (Code or Markup) and back — this defines the .mynb file format. <b>NotebookController</b> executes cells: <b>createNotebookCellExecution</b> creates an execution object, <b>replaceOutput</b> sends the result (text or error), <b>exec.end(success)</b> completes the execution. The controller is bound to a notebook type and specifies supported languages.'))

    add(h3('Notebook API Beyond Jupyter'))
    add(p('Notebook API is used far beyond just Jupyter. Real-world examples:'))
    add(sp(3))
    add(tblh(['Extension', 'What it does']))
    add(tbl2([
        ('REST Book', 'HTTP requests as notebook cells. .restbook files, variables shared between requests'),
        ('vscode-sql-notebook', 'Regular .sql files as a notebook — cell separator: two blank lines. MySQL, PostgreSQL, SQLite'),
        ('Runme', 'README.md as an executable notebook — code blocks in markdown become executable'),
        ('GitHub Issue Notebooks', 'Query language for searching GitHub issues/PRs. By Microsoft'),
        ('Shell Runner Notebooks', '.sh/.ps1 scripts as a notebook — comments become markdown cells'),
    ]))
    add(sp(6))

    add(h3('Example: API Request Notebook'))
    add(p('Let\'s create an extension that opens .http files as a notebook. Each cell is an HTTP request, the result is the server response. Three components: Serializer (format parsing), Controller (request execution), Renderer (output display).'))
    add(sp(3))
    add(code([
        '// package.json — notebook type declaration',
        '"contributes": {',
        '  "notebooks": [{',
        '    "type": "http-notebook",',
        '    "displayName": "HTTP Request Notebook",',
        '    "selector": [{ "filenamePattern": "*.http" }]',
        '  }],',
        '  "notebookRenderer": [{',
        '    "id": "http-response-renderer",',
        '    "displayName": "HTTP Response",',
        '    "entrypoint": "./out/renderer.js",',
        '    "mimeTypes": ["x-application/http-response"]',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('The <b>notebooks</b> block registers a notebook type and associates it with .http files. <b>notebookRenderer</b> declares a custom renderer for the MIME type x-application/http-response — VS Code will load it in an isolated iframe to display results.'))
    add(sp(3))
    add(code([
        '// NotebookSerializer — parsing .http file into cells',
        'class HttpNotebookSerializer implements vscode.NotebookSerializer {',
        '',
        '    deserializeNotebook(content: Uint8Array): vscode.NotebookData {',
        '        const text = new TextDecoder().decode(content);',
        '        // Split by "###" — the standard request separator',
        '        const blocks = text.split(/^###$/m);',
        '',
        '        const cells = blocks.map(block => {',
        '            const trimmed = block.trim();',
        '            if (trimmed.startsWith(\'//\') || trimmed.startsWith(\'#\')) {',
        '                // Comment -> Markdown cell',
        '                return new vscode.NotebookCellData(',
        '                    vscode.NotebookCellKind.Markup,',
        '                    trimmed.replace(/^\\/\\/ ?/gm, \'\'),',
        '                    \'markdown\'',
        '                );',
        '            }',
        '            // HTTP request -> Code cell',
        '            return new vscode.NotebookCellData(',
        '                vscode.NotebookCellKind.Code,',
        '                trimmed,',
        '                \'http\'',
        '            );',
        '        }).filter(c => c.value.length > 0);',
        '',
        '        return new vscode.NotebookData(cells);',
        '    }',
        '',
        '    serializeNotebook(data: vscode.NotebookData): Uint8Array {',
        '        const text = data.cells.map(cell => {',
        '            if (cell.kind === vscode.NotebookCellKind.Markup) {',
        '                return cell.value.split(\'\\n\').map(l => `// ${l}`).join(\'\\n\');',
        '            }',
        '            return cell.value;',
        '        }).join(\'\\n###\\n\');',
        '        return new TextEncoder().encode(text);',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('<b>deserializeNotebook()</b> parses the file into cells: the <b>###</b> separator divides blocks, lines starting with // become Markdown cells, and everything else becomes Code cells with the http language. <b>serializeNotebook()</b> does the reverse — assembles cells back into an .http file. The file format remains human-readable and compatible with REST Client.'))
    add(sp(3))
    add(code([
        '// NotebookController — executing HTTP requests',
        'const controller = vscode.notebooks.createNotebookController(',
        '    \'http-executor\',',
        '    \'http-notebook\',',
        '    \'HTTP Executor\'',
        ');',
        '',
        'controller.executeHandler = async (cells, notebook, ctrl) => {',
        '    for (const cell of cells) {',
        '        const execution = ctrl.createNotebookCellExecution(cell);',
        '        execution.start(Date.now());',
        '',
        '        try {',
        '            // Parse the HTTP request from the cell',
        '            const lines = cell.document.getText().split(\'\\n\');',
        '            const [method, url] = lines[0].split(\' \');',
        '            const headers: Record<string, string> = {};',
        '            let bodyStart = 1;',
        '            for (let i = 1; i < lines.length; i++) {',
        '                if (lines[i].includes(\':\')) {',
        '                    const [k, v] = lines[i].split(\':\').map(s => s.trim());',
        '                    headers[k] = v;',
        '                } else { bodyStart = i + 1; break; }',
        '            }',
        '            const body = lines.slice(bodyStart).join(\'\\n\').trim() || undefined;',
        '',
        '            const response = await fetch(url, { method, headers, body });',
        '            const data = await response.text();',
        '',
        '            // Output the result in multiple formats',
        '            execution.replaceOutput([',
        '                new vscode.NotebookCellOutput([',
        '                    // Custom renderer for pretty output',
        '                    vscode.NotebookCellOutputItem.json(',
        '                        { status: response.status, headers: Object.fromEntries(response.headers), body: data },',
        '                        \'x-application/http-response\'',
        '                    ),',
        '                    // Fallback: plain JSON',
        '                    vscode.NotebookCellOutputItem.text(data, \'application/json\'),',
        '                ])',
        '            ]);',
        '            execution.end(true, Date.now());',
        '        } catch (err: any) {',
        '            execution.replaceOutput([',
        '                new vscode.NotebookCellOutput([',
        '                    vscode.NotebookCellOutputItem.error(err)',
        '                ])',
        '            ]);',
        '            execution.end(false, Date.now());',
        '        }',
        '    }',
        '};',
        '',
        '// Registration',
        'context.subscriptions.push(',
        '    vscode.workspace.registerNotebookSerializer(\'http-notebook\', new HttpNotebookSerializer()),',
        '    controller',
        ');',
    ]))
    add(sp(3))
    add(p('The controller is created via <b>createNotebookController()</b> bound to the notebook type. <b>executeHandler</b> is called when Run is clicked on a cell. The <b>createNotebookCellExecution()</b> -> start() -> replaceOutput() -> end() cycle is the standard execution lifecycle. Output supports multiple MIME types: VS Code will choose the best available renderer. <b>NotebookCellOutputItem.error()</b> displays an error in the standard format.'))
    add(sp(3))
    add(box('Key Idea of Notebook API',
        'A notebook is not just Jupyter. Any file can be represented as a set of executable cells: '
        'SQL queries, HTTP requests, shell scripts, even regular Markdown with code blocks. '
        'Serializer defines the format, Controller defines the execution logic, Renderer defines the visualization. '
        'Three independent components that can be combined.', 'tip'))
    add(pb())

    # ── Deep Dive: Localization (L10n) ──────────────────────────────────────
    add(StableAnchor('chapter_l10n'))
    add(toc_ch('Deep Dive — Extension Localization'))
    add(banner('Deep Dive', 'Extension Localization', 'vscode.l10n API and @vscode/l10n-dev'))
    add(sp(12))

    add(h2('Why Localize an Extension'))
    add(p('VS Code is used in 30+ countries. Localizing your extension multiplies the audience significantly. '
          'Since VS Code 1.73, the built-in <b>vscode.l10n</b> API replaced the deprecated vscode-nls.'))
    add(sp(6))

    add(h2('Setting Up L10n'))
    add(code([
        '// package.json — declaring localization support',
        '{',
        '  "l10n": "./l10n",',
        '  "contributes": {',
        '    "commands": [{',
        '      "command": "myext.analyze",',
        '      "title": "%myext.analyze.title%"',
        '    }]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('The <b>"l10n": "./l10n"</b> field points to the translations folder. Strings like <b>%key%</b> in package.json are automatically substituted from the <b>package.nls.{locale}.json</b> file. For commands, settings, and menus, this is the only way to localize, since package.json is read before JavaScript loads.'))
    add(sp(3))
    add(code([
        '// package.nls.json — English (default)',
        '{ "myext.analyze.title": "Analyze File" }',
        '',
        '// package.nls.ru.json — Russian',
        '{ "myext.analyze.title": "Analyze File" }',
        '',
        '// package.nls.zh-cn.json — Chinese',
        '{ "myext.analyze.title": "Analyze File" }',
    ]))
    add(sp(3))
    add(p('A separate <b>package.nls.{locale}.json</b> file is created for each language with the same keys. VS Code automatically selects the file based on the user\'s interface language.'))
    add(sp(6))

    add(h2('vscode.l10n API — Localization in Code'))
    add(code([
        'import * as vscode from \'vscode\';',
        '',
        '// Simple string',
        'const msg = vscode.l10n.t(\'File saved successfully\');',
        '',
        '// With parameters (positional)',
        'const count = vscode.l10n.t(\'Found {0} errors in {1} files\', errorCount, fileCount);',
        '',
        '// With named parameters',
        'const detail = vscode.l10n.t(',
        '    \'Extension {name} activated in {time}ms\',',
        '    { name: extName, time: elapsed }',
        ');',
        '',
        '// For Markdown (hover, completion)',
        'const md = new vscode.MarkdownString(',
        '    vscode.l10n.t(\'Click [here]({0}) for details\', docsUrl)',
        ');',
    ]))
    add(sp(3))
    add(p('<b>vscode.l10n.t()</b> is the main localization function. It takes an English template string (used as the translation key) and optional parameters. Positional parameters are substituted as <b>{0}</b>, <b>{1}</b>; named ones as <b>{name}</b>. If no translation is found, it returns the original English string.'))
    add(sp(6))

    add(h2('Generating Translation Files'))
    add(code([
        '# Install tools',
        'npm install -D @vscode/l10n-dev',
        '',
        '# Extract strings from code to XLF',
        'npx @vscode/l10n-dev export --outDir ./l10n ./src',
        '',
        '# Creates: l10n/bundle.l10n.json (all strings)',
        '# Translators create: l10n/bundle.l10n.ru.json, bundle.l10n.zh-cn.json, etc.',
        '',
        '# Structure of bundle.l10n.ru.json:',
        '# {',
        '#   "File saved successfully": "File saved",',
        '#   "Found {0} errors in {1} files": "Found {0} errors in {1} files"',
        '# }',
    ]))
    add(sp(3))
    add(p('<b>@vscode/l10n-dev export</b> scans all <b>vscode.l10n.t()</b> calls in the source code and generates bundle.l10n.json with keys. Translators create <b>bundle.l10n.{locale}.json</b> files with the same keys and translated values. When publishing, all files are automatically included in the .vsix.'))
    add(sp(3))
    add(box('Full list of locale codes',
        'VS Code supports: de, es, fr, it, ja, ko, pt-br, ru, zh-cn, zh-tw, cs, hu, pl, tr and others. '
        'Current list: github.com/microsoft/vscode-l10n', 'note'))
    add(pb())

    # ── Performance tips ──────────────────────────────────────────────────────
    add(banner('Recommendations', 'Performance and Best Practices', 'How to create a fast and reliable extension'), sp(12))

    add(h2('Activation Events — Strategy'))
    add(p('Incorrect choice of Activation Events is the most common cause of slow VS Code startup:'))
    add(sp(3))
    add(tblh(['Bad Practice', 'Good Alternative']))
    add(tbl2([
        ('"activationEvents": ["*"]',
         '"activationEvents": ["onCommand:myext.doSomething"] — activate only on explicit request'),
        ('"activationEvents": ["onStartupFinished"]',
         'Use only if the extension does something useful in the background from startup'),
        ('Heavy initialization in activate()',
         'Lazy initialization: create heavy objects only on first use'),
    ]))
    add(sp(6))

    add(h2('Lazy Loading Patterns'))
    add(code([
        '// Bad: heavy operation on activation',
        'export async function activate(context: vscode.ExtensionContext) {',
        '    const db = await loadLargeDatabase(); // blocks startup!',
        '    vscode.commands.registerCommand(\'myext.query\', () => query(db));',
        '}',
        '',
        '// Good: lazy initialization',
        'let db: Database | undefined;',
        '',
        'async function getDB(): Promise<Database> {',
        '    if (!db) db = await loadLargeDatabase();',
        '    return db;',
        '}',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    // Fast! Only register the command',
        '    vscode.commands.registerCommand(\'myext.query\', async () => {',
        '        const database = await getDB(); // loaded on first call',
        '        return query(database);',
        '    });',
        '}',
    ]))
    add(sp(3))
    add(p('A comparison of two initialization approaches. The bad variant runs <b>await loadLargeDatabase()</b> right inside activate — this blocks VS Code startup. The good variant wraps the heavy operation in a function with caching: the database is loaded only on the first command call, and activate completes instantly.'))

    add(sp(6))

    add(h2('Debounce and Throttle for Frequent Events'))
    add(p('Avoid heavy operations on every keystroke. '
          'VS Code does not provide built-in debounce/throttle. '
          'Options: native setTimeout or the <b>es-toolkit</b> library '
          '(active lodash replacement: 2-3x faster, 97% smaller, native TypeScript):'))
    add(sp(3))
    add(code([
        '// Option 1: native debounce via setTimeout (no dependencies)',
        'function debounce<T extends (...args: any[]) => any>(',
        '    fn: T, delay: number',
        '): { (...args: Parameters<T>): void; cancel(): void } {',
        '    let timer: ReturnType<typeof setTimeout> | undefined;',
        '    const debounced = (...args: Parameters<T>) => {',
        '        clearTimeout(timer);',
        '        timer = setTimeout(() => fn(...args), delay);',
        '    };',
        '    debounced.cancel = () => clearTimeout(timer);',
        '    return debounced;',
        '}',
        '',
        '// Usage: validation with 500ms debounce',
        'const debouncedValidate = debounce((doc: vscode.TextDocument) => {',
        '    validateDocument(doc); // heavy operation',
        '}, 500);',
        '',
        'vscode.workspace.onDidChangeTextDocument(e => {',
        '    debouncedValidate(e.document);',
        '}, null, context.subscriptions);',
        '',
        '// Option 2: es-toolkit (npm install es-toolkit)',
        '// import { debounce, throttle } from "es-toolkit";',
        '// const debouncedValidate = debounce(validateDocument, 500);',
        '// debouncedValidate.cancel() — for cancellation on deactivation',
    ]))
    add(sp(3))
    add(p('The debounce pattern via <b>setTimeout/clearTimeout</b>: each new call resets the previous timer — the handler fires only after a pause of N ms. Applied to <b>onDidChangeTextDocument</b> to avoid running analysis on every keystroke.'))
    add(sp(6))

    add(h2('Cancelling Long Operations'))
    add(p('All providers receive a CancellationToken — always check it:'))
    add(sp(3))
    add(code([
        '// In a Language Provider',
        'async provideCompletionItems(',
        '    document: vscode.TextDocument,',
        '    position: vscode.Position,',
        '    token: vscode.CancellationToken  // <- ALWAYS accept the token',
        '): Promise<vscode.CompletionItem[]> {',
        '',
        '    // Check for cancellation before a heavy operation',
        '    if (token.isCancellationRequested) return [];',
        '',
        '    const results = await fetchCompletions(document, position);',
        '',
        '    // Check again after the async operation',
        '    if (token.isCancellationRequested) return [];',
        '',
        '    return results;',
        '}',
        '',
        '// Passing token to fetch',
        'async function fetchCompletions(',
        '    doc: vscode.TextDocument,',
        '    pos: vscode.Position',
        '): Promise<vscode.CompletionItem[]> {',
        '    // Can listen to token for request cancellation',
        '    const abortController = new AbortController();',
        '    // if token needed: token.onCancellationRequested(() => abortController.abort());',
        '    const response = await fetch(\'https://api.example.com/complete\', {',
        '        signal: abortController.signal',
        '    });',
        '    return await response.json();',
        '}',
    ]))
    add(sp(3))
    add(p('Proper handling of <b>CancellationToken</b> in providers. Check <b>token.isCancellationRequested</b> twice: before the heavy operation and after each await. To cancel HTTP requests, connect an <b>AbortController</b> to the <b>token.onCancellationRequested</b> event — this aborts the fetch rather than just ignoring the result.'))

    add(sp(6))

    add(h2('Diagnosing Extension Performance'))
    add(p('Several built-in tools for profiling extensions:'))
    add(sp(2))
    for item in [
        '<b>Help -> Toggle Developer Tools</b> -> Console: all console.log output from the extension is visible',
        '<b>Help -> Developer: Show Running Extensions</b>: activation time and resource consumption',
        '<b>Developer: Inspect Extension Host</b>: attach a Node.js profiler to the Extension Host',
        '<b>Developer: Set Log Level</b>: control the logging level',
        '<b>Output Channel</b>: view extension logs via View -> Output',
    ]:
        add(bul(item))
    add(pb())

    return A


if __name__ == '__main__':
    print(f'Part 3 has {len(build_story_part3())} elements')
