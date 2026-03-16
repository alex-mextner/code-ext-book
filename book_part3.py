from book_helpers import *

def build_story_part3():
    A = []
    def add(*x):
        for i in x: A.append(i)
    def ch(num, title, sub=''):
        part = f'Глава {num}' if str(num).replace('.','').isdigit() else str(num)
        label = f'{part}: {title}' if str(num).replace('.','').isdigit() else title
        add(StableAnchor(f'chapter_{num}'))
        add(toc_ch(label), banner(part, title, sub), sp(12))

    # ── ПРАКТИЧЕСКИЕ ПРИМЕРЫ ───────────────────────────────────────────────────
    add(StableAnchor('chapter_practice'))
    add(banner('Практика', 'Практические примеры', 'Реальные расширения от идеи до публикации'), sp(12))

    add(h2('Пример 1: Расширение для работы с TODO-комментариями'))
    add(p('Создадим полноценное расширение, которое находит TODO-комментарии в коде, показывает их в Tree View и позволяет быстро навигировать к ним. Это хороший пример, охватывающий сразу несколько API.'))
    add(sp(4))

    add(h3('Манифест — package.json'))
    add(code([
        '{',
        '  "name": "todo-highlighter",',
        '  "displayName": "TODO Highlighter",',
        '  "description": "Находит TODO/FIXME в коде и отображает в Tree View",',
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
        '        "title": "TODO: Обновить список",',
        '        "icon": "$(refresh)"',
        '      },',
        '      {',
        '        "command": "todoHighlighter.goToTodo",',
        '        "title": "TODO: Перейти к элементу"',
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
        '          "description": "Ключевые слова для поиска"',
        '        },',
        '        "todoHighlighter.filePattern": {',
        '          "type": "string",',
        '          "default": "**/*.{ts,js,py,rs,go}",',
        '          "description": "Glob-паттерн файлов для поиска"',
        '        }',
        '      }',
        '    }',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Манифест объявляет всё, что расширение предоставляет VS Code. <b>views</b> регистрирует панель TODO List в Explorer. <b>commands</b> добавляет две команды — обновление списка и переход к элементу. <b>menus</b> размещает кнопку refresh в заголовке панели. <b>configuration</b> позволяет пользователю настроить ключевые слова и glob-паттерн через Settings UI.'))

    add(sp(6))

    add(h3('Модель данных'))
    add(code([
        '// src/models.ts',
        '',
        'export interface TodoItem {',
        '    file: string;       // полный путь к файлу',
        '    line: number;       // номер строки (0-based)',
        '    keyword: string;    // TODO, FIXME, etc.',
        '    text: string;       // полный текст комментария',
        '    column: number;     // позиция в строке',
        '}',
        '',
        'export interface TodoFile {',
        '    path: string;       // путь к файлу',
        '    items: TodoItem[];  // список TODO в файле',
        '}',
    ]))
    add(sp(3))
    add(p('Модель данных расширения. <b>TodoItem</b> описывает одно найденное ключевое слово: файл, строку, колонку, тип (TODO/FIXME) и текст комментария. <b>TodoFile</b> группирует все TodoItem одного файла — эта структура напрямую ложится на двухуровневый Tree View.'))

    add(sp(6))

    add(h3('Сканер файлов'))
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
        '        // Создаём regex для поиска',
        '        const kwPattern = keywords.map(k => `\\\\b${k}\\\\b`).join(\'|\');',
        '        const regex = new RegExp(`(${kwPattern})[:\\\\s]+(.*)`, \'gi\');',
        '',
        '        // Ищем все файлы по паттерну',
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
    add(p('Сканер ищет TODO-комментарии во всех файлах воркспейса. <b>workspace.findFiles(pattern, exclude)</b> возвращает URI по glob-паттерну, исключая node_modules. Для каждого файла построчно прогоняется regex из настроек. Ключевые слова и паттерн файлов читаются из <b>workspace.getConfiguration</b> при каждом сканировании — если нужна реакция на изменения настроек в реальном времени, подпишитесь на <b>workspace.onDidChangeConfiguration</b>.'))
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
        '            // Это файл',
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
        '            // Это TODO-элемент',
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
        '            item.description = `Строка ${node.line + 1}`;',
        '            item.iconPath = new vscode.ThemeIcon(',
        '                \'circle-filled\',',
        '                new vscode.ThemeColor(colors[node.keyword] || \'charts.yellow\')',
        '            );',
        '            item.command = {',
        '                command: \'todoHighlighter.goToTodo\',',
        '                title: \'Перейти\',',
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
    add(p('Двухуровневый Tree View: файлы на верхнем уровне, TODO-элементы внутри. <b>getTreeItem</b> различает узлы через <b>\'items\' in node</b> — файлам назначается иконка и счётчик, а TODO-элементам — цветной кружок по типу (TODO жёлтый, FIXME красный) и команда навигации при клике. <b>EventEmitter</b> + <b>fire(undefined)</b> заставляет VS Code перезапросить всё дерево при обновлении.'))
    add(sp(6))

    add(h3('Основной файл extension.ts'))
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
        '    // Декорация для подсветки TODO в редакторе',
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
        '    // Команда обновления',
        '    const refreshCmd = vscode.commands.registerCommand(',
        '        \'todoHighlighter.refresh\', () => provider.refresh()',
        '    );',
        '',
        '    // Команда навигации к TODO',
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
        '    // Слушаем изменения редакторов',
        '    const editorSub = vscode.window.onDidChangeActiveTextEditor(editor => {',
        '        if (editor) highlightInEditor(editor);',
        '    });',
        '',
        '    // Слушаем изменения файлов',
        '    const docSub = vscode.workspace.onDidSaveTextDocument(() => {',
        '        provider.refresh();',
        '    });',
        '',
        '    // Подсвечиваем в текущем редакторе',
        '    if (vscode.window.activeTextEditor) {',
        '        highlightInEditor(vscode.window.activeTextEditor);',
        '    }',
        '',
        '    // Начальное сканирование',
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
    add(p('Точка входа собирает всё вместе. <b>createTreeView</b> создаёт панель с кнопкой Collapse All. <b>createTextEditorDecorationType</b> задаёт стиль подсветки TODO-слов прямо в редакторе. Две команды: refresh пересканирует файлы, goToTodo открывает файл и ставит курсор на нужную строку через <b>revealRange</b>. Подписки на <b>onDidChangeActiveTextEditor</b> и <b>onDidSaveTextDocument</b> обеспечивают автоматическое обновление подсветки и списка.'))

    add(pb())

    # ── Пример 2: Status Bar с информацией о строке ─────────────────────────
    add(h2('Пример 2: Status Bar с информацией о файле'))
    add(p('Простой пример расширения, показывающего в Status Bar информацию об активном файле: количество строк, символов, кодировку и переносы строк.'))
    add(sp(3))
    add(code([
        '// extension.ts — краткий, но полный пример',
        'import * as vscode from \'vscode\';',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '',
        '    // Создаём элемент слева',
        '    const linesItem = vscode.window.createStatusBarItem(',
        '        vscode.StatusBarAlignment.Left, 200',
        '    );',
        '    linesItem.command = \'fileInfo.showDetails\';',
        '    linesItem.tooltip = \'Нажмите для деталей о файле\';',
        '',
        '    // Создаём элемент справа',
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
        '        // Строки + символы (+ выделение если есть)',
        '        if (selChars > 0) {',
        '            linesItem.text = `$(symbol-string) ${lines} строк  |  выд: ${selChars} симв.`;',
        '        } else {',
        '            linesItem.text = `$(symbol-string) ${lines} строк, ${chars} симв.`;',
        '        }',
        '        linesItem.show();',
        '',
        '        // Кодировка и переносы строк',
        '        const eol = doc.eol === vscode.EndOfLine.LF ? \'LF\' : \'CRLF\';',
        '        encodingItem.text = `$(symbol-key) UTF-8  ${eol}`;',
        '        encodingItem.show();',
        '    }',
        '',
        '    // Команда деталей',
        '    const detailsCmd = vscode.commands.registerCommand(',
        '        \'fileInfo.showDetails\',',
        '        () => {',
        '            const editor = vscode.window.activeTextEditor;',
        '            if (!editor) return;',
        '            const doc = editor.document;',
        '            vscode.window.showInformationMessage(',
        '                `Файл: ${doc.fileName}\\n` +',
        '                `Язык: ${doc.languageId}\\n` +',
        '                `Строк: ${doc.lineCount}\\n` +',
        '                `Символов: ${doc.getText().length}\\n` +',
        '                `Изменён: ${doc.isDirty ? \'Да\' : \'Нет\'}`',
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
    add(p('Полный пример Status Bar расширения. Два элемента: слева — количество строк и символов (с учётом выделения), справа — кодировка и тип переносов. <b>createStatusBarItem(alignment, priority)</b> создаёт элемент; priority определяет порядок внутри стороны. Привязка <b>command</b> к элементу делает его кликабельным — здесь по клику показывается информация через <b>showInformationMessage</b>. Три подписки обеспечивают обновление: смена редактора, изменение выделения, правка документа.'))

    add(pb())

    # ── ГЛУБОКОЕ ПОГРУЖЕНИЕ: Работа с файловой системой ─────────────────────
    add(banner('Углублённо', 'Работа с файловой системой', 'vscode.workspace.fs и FileSystemProvider'), sp(12))

    add(h2('vscode.workspace.fs API'))
    add(p('Для работы с файлами в расширениях рекомендуется использовать <b>vscode.workspace.fs</b> вместо стандартного Node.js <b>fs</b>. Это обеспечивает совместимость с Remote Development и виртуальными файловыми системами.'))
    add(sp(4))
    add(code([
        '// Работа с файлами через vscode.workspace.fs',
        '',
        '// Чтение файла',
        'const uri = vscode.Uri.file(\'/path/to/file.json\');',
        'const bytes = await vscode.workspace.fs.readFile(uri);',
        'const text = Buffer.from(bytes).toString(\'utf8\');',
        'const data = JSON.parse(text);',
        '',
        '// Запись файла',
        'const content = JSON.stringify(data, null, 2);',
        'await vscode.workspace.fs.writeFile(uri, Buffer.from(content));',
        '',
        '// Создание папки',
        'const dirUri = vscode.Uri.file(\'/path/to/new-dir\');',
        'await vscode.workspace.fs.createDirectory(dirUri);',
        '',
        '// Получение метаданных',
        'const stat = await vscode.workspace.fs.stat(uri);',
        'console.log(`Размер: ${stat.size}, Тип: ${stat.type}`);',
        '// FileType: Unknown=0, File=1, Directory=2, SymbolicLink=64',
        '',
        '// Чтение содержимого папки',
        'const entries = await vscode.workspace.fs.readDirectory(dirUri);',
        '// entries: [name, type][]',
        'for (const [name, type] of entries) {',
        '    console.log(`${type === vscode.FileType.Directory ? \'[D]\' : \'[F]\'} ${name}`);',
        '}',
        '',
        '// Копирование файла',
        'const destUri = vscode.Uri.file(\'/path/to/dest.json\');',
        'await vscode.workspace.fs.copy(uri, destUri, { overwrite: false });',
        '',
        '// Переименование / перемещение',
        'await vscode.workspace.fs.rename(uri, destUri, { overwrite: true });',
        '',
        '// Удаление',
        'await vscode.workspace.fs.delete(uri, { recursive: false, useTrash: true });',
    ]))
    add(sp(3))
    add(p('Полный набор файловых операций через <b>workspace.fs</b>. Чтение возвращает <b>Uint8Array</b> — конвертируйте через Buffer.from().toString(). <b>stat</b> возвращает размер и тип (File, Directory, SymbolicLink). <b>readDirectory</b> даёт пары [имя, тип]. Операции copy, rename, delete принимают опции: <b>overwrite</b> для перезаписи, <b>useTrash</b> для удаления в корзину. Все методы работают с любой URI-схемой, не только file://.'))

    add(sp(6))

    add(h2('Кастомная файловая система (FileSystemProvider)'))
    add(p('FileSystemProvider позволяет создать виртуальную файловую систему с произвольной схемой URI. Используется для отображения архивов, удалённых ресурсов, баз данных как файловой системы.'))
    add(sp(3))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "filesystems": [{',
        '    "scheme": "memfs"',
        '  }]',
        '}',
        '',
        '// In-memory файловая система',
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
        '// Регистрация',
        'const memfs = new MemFS();',
        'context.subscriptions.push(',
        '    vscode.workspace.registerFileSystemProvider(\'memfs\', memfs, {',
        '        isCaseSensitive: true',
        '    })',
        ');',
        '',
        '// Создание файла в виртуальной ФС',
        'memfs.writeFile(',
        '    vscode.Uri.parse(\'memfs:/hello.ts\'),',
        '    Buffer.from(\'console.log("Hello from memfs!")\')',
        ');',
        '// Открытие файла',
        'await vscode.workspace.openTextDocument(vscode.Uri.parse(\'memfs:/hello.ts\'));',
    ]))
    add(sp(3))
    add(p('In-memory файловая система с кастомной схемой <b>memfs://</b>. Реализует все методы <b>FileSystemProvider</b>: stat, readFile, writeFile, readDirectory, createDirectory, delete, rename. <b>onDidChangeFile</b> (EventEmitter) уведомляет VS Code об изменениях — без него Explorer не обновится. Регистрация через <b>registerFileSystemProvider(scheme, provider)</b> привязывает провайдер к URI-схеме. После этого файлы с memfs:/ открываются в редакторе как обычные.'))

    add(pb())

    # ── Source Control API ─────────────────────────────────────────────────────
    add(banner('Углублённо', 'Source Control API', 'Создание SCM-провайдеров'), sp(12))

    add(h2('Что такое Source Control API'))
    add(p('Source Control API — это то, через что работает встроенная Git-интеграция VS Code. '
          'Расширения могут создавать собственные SCM-провайдеры для любой VCS: '
          'Mercurial, SVN, Perforce, Fossil, Jujutsu. '
          'Все они появляются в той же боковой панели Source Control с тем же UX.'))
    add(sp(3))
    add(p('Реальные примеры расширений на этом API: '
          '<b>vscode-hg</b> (Mercurial), <b>SVN Scm</b>, '
          '<b>Perforce for VS Code</b> (P4). '
          'Каждое использует createSourceControl и предоставляет привычный интерфейс.'))
    add(sp(3))
    add(tblh(['Концепция', 'Описание']))
    add(tbl2([
        ('SourceControl\n(createSourceControl)',
         'Корневой объект провайдера. Задаёт id, label, иконку. '
         'Появляется как отдельный провайдер в SCM панели'),
        ('SourceControlResourceGroup\n(createResourceGroup)',
         'Группа изменённых файлов. Например: "Staged", "Unstaged", "Untracked". '
         'Каждая группа — отдельный раздел в SCM панели'),
        ('SourceControlResourceState',
         'Один файл в группе. Содержит URI, декорации (иконка, цвет, badge), '
         'команду при клике (обычно diff)'),
        ('inputBox',
         'Поле ввода для сообщения коммита в верхней части SCM панели'),
        ('QuickDiffProvider',
         'Даёт VS Code "оригинальную" версию файла для показа diff в gutter редактора'),
    ]))
    add(sp(6))

    add(h2('Полный пример: простой SCM провайдер'))
    add(code([
        '// Полный пример SCM провайдера',
        'export function activate(ctx: vscode.ExtensionContext) {',
        '    // 1. Создаём провайдер (появляется в SCM панели)',
        '    const scm = vscode.scm.createSourceControl(',
        '        \'my-vcs\',        // уникальный id',
        '        \'My VCS\',        // отображаемое имя',
        '        vscode.Uri.file(workspaceRoot)  // корень репозитория',
        '    );',
        '    scm.quickDiffProvider = myQuickDiffProvider;',
        '    scm.inputBox.placeholder = \'Сообщение коммита (Enter для коммита)\';',
        '    scm.acceptInputCommand = {',
        '        command: \'myVcs.commit\',',
        '        title: \'Commit\',',
        '        tooltip: \'Зафиксировать изменения\'',
        '    };',
        '',
        '    // 2. Группы файлов',
        '    const stagedGroup   = scm.createResourceGroup(\'staged\',   \'Staged\');',
        '    const changedGroup  = scm.createResourceGroup(\'changes\',  \'Changes\');',
        '    const untrackedGroup = scm.createResourceGroup(\'untracked\', \'Untracked\');',
        '',
        '    // 3. Заполняем группы (после получения статуса от VCS)',
        '    async function refresh() {',
        '        const status = await myVcs.getStatus(workspaceRoot);',
        '',
        '        stagedGroup.resourceStates = status.staged.map(f => ({',
        '            resourceUri: vscode.Uri.file(f.path),',
        '            decorations: {',
        '                // Буква в SCM панели: A = Added, M = Modified, D = Deleted',
        '                letter: f.type === \'added\' ? \'A\' : f.type === \'modified\' ? \'M\' : \'D\',',
        '                color: new vscode.ThemeColor(\'gitDecoration.addedResourceForeground\'),',
        '                tooltip: f.path,',
        '            },',
        '            // При клике: открыть diff между HEAD и рабочей копией',
        '            command: {',
        '                command: \'vscode.diff\',',
        '                title: \'Открыть diff\',',
        '                arguments: [',
        '                    getOriginalUri(f.path),    // оригинал из VCS',
        '                    vscode.Uri.file(f.path),   // рабочая копия',
        '                    `${f.path} (HEAD)`',
        '                ]',
        '            }',
        '        }));',
        '',
        '        changedGroup.resourceStates = status.modified.map(/* ... */);',
        '        untrackedGroup.resourceStates = status.untracked.map(/* ... */);',
        '    }',
        '',
        '    // 4. Следим за изменениями файлов',
        '    const watcher = vscode.workspace.createFileSystemWatcher(\'**/*\');',
        '    watcher.onDidChange(refresh);',
        '    watcher.onDidCreate(refresh);',
        '    watcher.onDidDelete(refresh);',
        '',
        '    // 5. Регистрируем команды',
        '    ctx.subscriptions.push(',
        '        scm, stagedGroup, changedGroup, untrackedGroup, watcher,',
        '        vscode.commands.registerCommand(\'myVcs.commit\', async () => {',
        '            const message = scm.inputBox.value;',
        '            if (!message) {',
        '                vscode.window.showWarningMessage(\'Введите сообщение коммита\');',
        '                return;',
        '            }',
        '            await myVcs.commit(workspaceRoot, message);',
        '            scm.inputBox.value = \'\';  // очищаем поле после коммита',
        '            refresh();',
        '        }),',
        '    );',
        '',
        '    refresh(); // первичная загрузка',
        '}',
    ]))


    add(sp(4))
    add(p('<b>Ключевые аспекты:</b> createResourceGroup лучше вызывать один раз при активации. '
          'resourceStates — это свойство, не метод: просто присваивайте новый массив при каждом '
          'обновлении, VS Code сам перерисует панель. '
          'acceptInputCommand срабатывает при нажатии Enter или кнопки ✓ над полем ввода.'))
    add(sp(4))
    add(box('QuickDiffProvider — полосы изменений в редакторе',
        'Если вы хотите чтобы в gutter редактора появились зелёные/красные/синие полосы '
        '(как для Git), реализуйте QuickDiffProvider: '
        'provideOriginalResource(uri) должен возвращать URI оригинального файла (из VCS). '
        'VS Code сам вычислит diff и покажет полосы. '
        'Документация: code.visualstudio.com/api/extension-guides/scm-provider',
        'tip'))
    add(pb())

    # ── Debug Adapter Protocol ─────────────────────────────────────────────────
    add(banner('Углублённо', 'Debugger Extension', 'Debug Adapter Protocol — создание отладчиков'), sp(12))

    add(h2('Архитектура Debug Adapter'))
    add(p('Debugger Extension позволяет создавать отладчики для любых языков и рантаймов. Взаимодействие происходит по <b>Debug Adapter Protocol (DAP)</b> — ещё один открытый протокол Microsoft.'))
    add(sp(4))
    add(tblh(['Компонент', 'Описание']))
    add(tbl2([
        ('VS Code (DAP Client)',  'Отправляет запросы: запустить, поставить брейкпоинт, продолжить, получить переменные'),
        ('Debug Adapter',        'Транслирует DAP в команды реального отладчика. Отдельный процесс'),
        ('Runtime / Debugger',   'Реальный отладчик: gdb, lldb, node inspector, jvm debugger и т.д.'),
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
        '            "description": "Путь к программе для отладки"',
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
        '      "name": "Запустить программу",',
        '      "program": "${file}"',
        '    }]',
        '  }],',
        '  "breakpoints": [{ "language": "mylang" }]',
        '}',
        '',
        '// Регистрация Debug Adapter Factory',
        'class MyDebugAdapterFactory',
        '    implements vscode.DebugAdapterDescriptorFactory {',
        '    createDebugAdapterDescriptor(',
        '        session: vscode.DebugSession',
        '    ): vscode.DebugAdapterDescriptor {',
        '        // Запускаем DA как отдельный процесс',
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
    add(p('Два шага: манифест и фабрика. В <b>package.json</b> секция <b>debuggers</b> объявляет тип отладчика, поддерживаемые языки и атрибуты launch-конфигурации (program, stopOnEntry). <b>initialConfigurations</b> — шаблон для автогенерации launch.json. <b>breakpoints</b> разрешает ставить точки останова в файлах указанного языка. <b>DebugAdapterDescriptorFactory</b> запускает Debug Adapter как отдельный процесс через <b>DebugAdapterExecutable</b> — VS Code общается с ним по DAP через stdin/stdout.'))

    add(sp(4))
    add(box('Библиотека @vscode/debugadapter',
        'Для создания Debug Adapter используйте библиотеку @vscode/debugadapter. '
        'Она предоставляет базовый класс DebugSession с готовыми обработчиками всех DAP-сообщений.',
        'tip'))
    add(pb())

    # ── Task Provider ──────────────────────────────────────────────────────────
    add(banner('Углублённо', 'Task Provider', 'Автоматическое создание задач для рабочего пространства'), sp(12))

    add(h2('Что такое Task Provider?'))
    add(p('Task Provider позволяет расширению автоматически предоставлять задачи (tasks) на основе содержимого рабочего пространства. Например, расширение для Make может автоматически создавать задачи из Makefile.'))
    add(sp(4))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "taskDefinitions": [{',
        '    "type": "make",',
        '    "properties": {',
        '      "target": {',
        '        "type": "string",',
        '        "description": "Цель Make"',
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
        '            // Ищем targets: строки вида "target:"',
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
        '// Регистрация',
        'context.subscriptions.push(',
        '    vscode.tasks.registerTaskProvider(MakeTaskProvider.MakeType, new MakeTaskProvider())',
        ');',
    ]))
    add(sp(3))
    add(p('<b>TaskProvider</b> добавляет задачи в Tasks: Run Task. <b>ShellExecution(command)</b> запускает команду в shell; <b>ProcessExecution(path, args)</b> — процесс напрямую без оболочки. <b>TaskGroup.Build</b> делает задачу доступной через Ctrl+Shift+B.'))
    add(pb())

    # ── Authentication Provider ────────────────────────────────────────────────
    add(banner('Углублённо', 'Authentication API', 'Аутентификация пользователей в расширениях'), sp(12))

    add(h2('Работа с Authentication'))
    add(p('VS Code предоставляет унифицированный Authentication API для получения токенов от OAuth-провайдеров. Встроены: GitHub и Microsoft. Расширения могут регистрировать свои провайдеры.'))
    add(sp(4))

    add(h3('Использование существующих провайдеров'))
    add(code([
        '// Получить GitHub токен',
        'async function getGitHubToken(): Promise<string | undefined> {',
        '    try {',
        '        const session = await vscode.authentication.getSession(',
        '            \'github\',',
        '            [\'repo\', \'read:user\'],  // OAuth scopes',
        '            { createIfNone: true }    // предложить логин если нет',
        '        );',
        '        return session.accessToken;',
        '    } catch (e) {',
        '        vscode.window.showErrorMessage(\'Не удалось получить GitHub токен\');',
        '        return undefined;',
        '    }',
        '}',
        '',
        '// Получить Microsoft токен',
        'async function getMicrosoftToken(): Promise<string | undefined> {',
        '    const session = await vscode.authentication.getSession(',
        '        \'microsoft\',',
        '        [\'https://management.azure.com/.default\'],',
        '        { createIfNone: false }  // тихо, без диалога',
        '    );',
        '    return session?.accessToken;',
        '}',
        '',
        '// Слушать изменения сессий',
        'vscode.authentication.onDidChangeSessions(e => {',
        '    if (e.provider.id === \'github\') {',
        '        console.log(\'GitHub сессия изменилась\');',
        '    }',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('<b>authentication.getSession(providerId, scopes)</b> запрашивает OAuth-сессию. VS Code показывает диалог только при <b>createIfNone: true</b>. Токены кэшируются и обновляются автоматически — не храните их вручную. <b>onDidChangeSessions</b> уведомляет о logout или смене аккаунта.'))
    add(sp(6))

    add(h3('Создание собственного Authentication Provider'))
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
        '        // Открываем браузер для OAuth',
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
        '        // Реализация OAuth flow...',
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
    add(p('Реализация собственного OAuth-провайдера. Интерфейс <b>AuthenticationProvider</b> требует три метода: <b>getSessions</b> возвращает активные сессии, <b>createSession</b> запускает OAuth-flow и создаёт новую сессию, <b>removeSession</b> выполняет logout. EventEmitter <b>onDidChangeSessions</b> уведомляет VS Code о добавлении или удалении сессий. Регистрация через <b>registerAuthenticationProvider</b> с опцией <b>supportsMultipleAccounts</b>.'))
    add(pb())

    # ── Notebook API ───────────────────────────────────────────────────────────
    add(StableAnchor('chapter_notebook'))
    add(banner('Углублённо', 'Notebook API', 'Создание интерактивных ноутбуков в VS Code'), sp(12))

    add(h2('Обзор Notebook API'))
    add(p('Notebook API позволяет создавать интерактивные документы в стиле Jupyter Notebook прямо в VS Code. Встроенный Jupyter extension использует тот же API.'))
    add(sp(4))
    add(tblh(['Компонент', 'Описание']))
    add(tbl2([
        ('NotebookSerializer', 'Читает/пишет формат файла. Конвертирует байты ↔ NotebookData'),
        ('NotebookController',  'Выполняет ячейки. Отправляет вывод обратно в VS Code'),
        ('NotebookRenderer',   'Опциональный кастомный рендерер для rich output'),
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
        '// Serializer — чтение и запись формата',
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
        '// Controller — выполнение ячеек',
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
    add(p('Два компонента ноутбука. <b>NotebookSerializer</b> конвертирует файл в <b>NotebookData</b> с массивом ячеек (Code или Markup) и обратно — это определяет формат .mynb файлов. <b>NotebookController</b> выполняет ячейки: <b>createNotebookCellExecution</b> создаёт объект выполнения, <b>replaceOutput</b> отправляет результат (текст или ошибку), <b>exec.end(success)</b> завершает выполнение. Контроллер привязывается к типу ноутбука и указывает поддерживаемые языки.'))

    add(h3('Notebook API за пределами Jupyter'))
    add(p('Notebook API используется далеко не только для Jupyter. Реальные примеры:'))
    add(sp(3))
    add(tblh(['Расширение', 'Что делает']))
    add(tbl2([
        ('REST Book', 'HTTP-запросы как notebook-ячейки. Файлы .restbook, переменные между запросами'),
        ('vscode-sql-notebook', 'Обычные .sql файлы как notebook — разделитель ячеек: две пустые строки. MySQL, PostgreSQL, SQLite'),
        ('Runme', 'README.md как executable notebook — code-блоки в markdown становятся исполняемыми'),
        ('GitHub Issue Notebooks', 'Query language для поиска GitHub issues/PRs. От Microsoft'),
        ('Shell Runner Notebooks', '.sh/.ps1 скрипты как notebook — комментарии → markdown-ячейки'),
    ]))
    add(sp(6))

    add(h3('Пример: API Request Notebook'))
    add(p('Создадим расширение, которое открывает .http файлы как notebook. Каждая ячейка — HTTP-запрос, результат — ответ сервера. Три компонента: Serializer (парсинг формата), Controller (исполнение запросов), Renderer (вывод результатов).'))
    add(sp(3))
    add(code([
        '// package.json — объявление notebook типа',
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
    add(p('Блок <b>notebooks</b> регистрирует тип notebook и связывает его с файлами .http. <b>notebookRenderer</b> объявляет кастомный рендерер для MIME-типа x-application/http-response — VS Code загрузит его в изолированный iframe для отображения результатов.'))
    add(sp(3))
    add(code([
        '// NotebookSerializer — парсинг .http файла в ячейки',
        'class HttpNotebookSerializer implements vscode.NotebookSerializer {',
        '',
        '    deserializeNotebook(content: Uint8Array): vscode.NotebookData {',
        '        const text = new TextDecoder().decode(content);',
        '        // Разделяем по "###" — стандартный разделитель запросов',
        '        const blocks = text.split(/^###$/m);',
        '',
        '        const cells = blocks.map(block => {',
        '            const trimmed = block.trim();',
        '            if (trimmed.startsWith(\'//\') || trimmed.startsWith(\'#\')) {',
        '                // Комментарий → Markdown-ячейка',
        '                return new vscode.NotebookCellData(',
        '                    vscode.NotebookCellKind.Markup,',
        '                    trimmed.replace(/^\\/\\/ ?/gm, \'\'),',
        '                    \'markdown\'',
        '                );',
        '            }',
        '            // HTTP-запрос → Code-ячейка',
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
    add(p('<b>deserializeNotebook()</b> разбирает файл на ячейки: разделитель <b>###</b> отделяет блоки, строки с // становятся Markdown-ячейками, остальное — Code-ячейки с языком http. <b>serializeNotebook()</b> делает обратное — собирает ячейки обратно в .http файл. Формат файла остаётся человекочитаемым и совместимым с REST Client.'))
    add(sp(3))
    add(code([
        '// NotebookController — исполнение HTTP-запросов',
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
        '            // Парсим HTTP-запрос из ячейки',
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
        '            // Вывод результата в нескольких форматах',
        '            execution.replaceOutput([',
        '                new vscode.NotebookCellOutput([',
        '                    // Кастомный рендерер для красивого вывода',
        '                    vscode.NotebookCellOutputItem.json(',
        '                        { status: response.status, headers: Object.fromEntries(response.headers), body: data },',
        '                        \'x-application/http-response\'',
        '                    ),',
        '                    // Фоллбэк: plain JSON',
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
        '// Регистрация',
        'context.subscriptions.push(',
        '    vscode.workspace.registerNotebookSerializer(\'http-notebook\', new HttpNotebookSerializer()),',
        '    controller',
        ');',
    ]))
    add(sp(3))
    add(p('Контроллер создаётся через <b>createNotebookController()</b> с привязкой к типу notebook. <b>executeHandler</b> вызывается при нажатии Run на ячейке. Цикл <b>createNotebookCellExecution()</b> → start() → replaceOutput() → end() — стандартный lifecycle исполнения. Вывод поддерживает несколько MIME-типов: VS Code выберет лучший доступный рендерер. <b>NotebookCellOutputItem.error()</b> показывает ошибку в стандартном формате.'))
    add(sp(3))
    add(box('Ключевая идея Notebook API',
        'Notebook — это не только Jupyter. Любой файл можно представить как набор исполняемых ячеек: '
        'SQL-запросы, HTTP-запросы, shell-скрипты, даже обычный Markdown с code-блоками. '
        'Serializer определяет формат, Controller — логику исполнения, Renderer — визуализацию. '
        'Три независимых компонента, которые можно комбинировать.', 'tip'))
    add(pb())

    # ── Углублённо: Локализация (L10n) ──────────────────────────────────────
    add(StableAnchor('chapter_l10n'))
    add(toc_ch('Углублённо — Локализация расширений'))
    add(banner('Углублённо', 'Локализация расширений', 'vscode.l10n API и @vscode/l10n-dev'))
    add(sp(12))

    add(h2('Зачем локализовать расширение'))
    add(p('VS Code используется в 30+ странах. Локализация расширения увеличивает аудиторию в разы. '
          'С VS Code 1.73 появился встроенный <b>vscode.l10n</b> API, заменивший устаревший vscode-nls.'))
    add(sp(6))

    add(h2('Настройка L10n'))
    add(code([
        '// package.json — объявление поддержки локализации',
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
    add(p('Поле <b>"l10n": "./l10n"</b> указывает папку с переводами. Строки вида <b>%key%</b> в package.json автоматически подставляются из файла <b>package.nls.{locale}.json</b>. Для команд, настроек и меню — это единственный способ локализации, так как package.json читается до загрузки JavaScript.'))
    add(sp(3))
    add(code([
        '// package.nls.json — английский (по умолчанию)',
        '{ "myext.analyze.title": "Analyze File" }',
        '',
        '// package.nls.ru.json — русский',
        '{ "myext.analyze.title": "Анализировать файл" }',
        '',
        '// package.nls.zh-cn.json — китайский',
        '{ "myext.analyze.title": "分析文件" }',
    ]))
    add(sp(3))
    add(p('Для каждого языка создаётся отдельный файл <b>package.nls.{locale}.json</b> с теми же ключами. VS Code выбирает файл автоматически по языку интерфейса пользователя.'))
    add(sp(6))

    add(h2('vscode.l10n API — локализация в коде'))
    add(code([
        'import * as vscode from \'vscode\';',
        '',
        '// Простая строка',
        'const msg = vscode.l10n.t(\'File saved successfully\');',
        '',
        '// С параметрами (позиционные)',
        'const count = vscode.l10n.t(\'Found {0} errors in {1} files\', errorCount, fileCount);',
        '',
        '// С именованными параметрами',
        'const detail = vscode.l10n.t(',
        '    \'Extension {name} activated in {time}ms\',',
        '    { name: extName, time: elapsed }',
        ');',
        '',
        '// Для Markdown (hover, completion)',
        'const md = new vscode.MarkdownString(',
        '    vscode.l10n.t(\'Click [here]({0}) for details\', docsUrl)',
        ');',
    ]))
    add(sp(3))
    add(p('<b>vscode.l10n.t()</b> — основная функция локализации. Принимает строку-шаблон на английском (ключ для перевода) и опциональные параметры. Позиционные параметры подставляются как <b>{0}</b>, <b>{1}</b>; именованные — как <b>{name}</b>. Если перевод не найден — возвращает исходную английскую строку.'))
    add(sp(6))

    add(h2('Генерация файлов перевода'))
    add(code([
        '# Установка инструментов',
        'npm install -D @vscode/l10n-dev',
        '',
        '# Извлечение строк из кода в XLF',
        'npx @vscode/l10n-dev export --outDir ./l10n ./src',
        '',
        '# Создаёт: l10n/bundle.l10n.json (все строки)',
        '# Переводчики создают: l10n/bundle.l10n.ru.json, bundle.l10n.zh-cn.json и т.д.',
        '',
        '# Структура bundle.l10n.ru.json:',
        '# {',
        '#   "File saved successfully": "Файл сохранён",',
        '#   "Found {0} errors in {1} files": "Найдено {0} ошибок в {1} файлах"',
        '# }',
    ]))
    add(sp(3))
    add(p('<b>@vscode/l10n-dev export</b> сканирует все вызовы <b>vscode.l10n.t()</b> в исходниках и генерирует bundle.l10n.json с ключами. Переводчики создают файлы <b>bundle.l10n.{locale}.json</b> с теми же ключами и переведёнными значениями. При публикации все файлы включаются в .vsix автоматически.'))
    add(sp(3))
    add(box('Полный список locale-кодов',
        'VS Code поддерживает: de, es, fr, it, ja, ko, pt-br, ru, zh-cn, zh-tw, cs, hu, pl, tr и другие. '
        'Актуальный список: github.com/microsoft/vscode-l10n', 'note'))
    add(pb())

    # ── Советы по производительности ──────────────────────────────────────────
    add(banner('Рекомендации', 'Производительность и лучшие практики', 'Как создать быстрое и надёжное расширение'), sp(12))

    add(h2('Activation Events — стратегия'))
    add(p('Неправильный выбор Activation Events — самая частая причина медленного старта VS Code:'))
    add(sp(3))
    add(tblh(['Плохая практика', 'Хорошая замена']))
    add(tbl2([
        ('"activationEvents": ["*"]',
         '"activationEvents": ["onCommand:myext.doSomething"] — активироваться только при явном запросе'),
        ('"activationEvents": ["onStartupFinished"]',
         'Используйте только если расширение делает что-то полезное в фоне с самого старта'),
        ('Тяжёлая инициализация в activate()',
         'Ленивая инициализация: создавайте тяжёлые объекты только при первом использовании'),
    ]))
    add(sp(6))

    add(h2('Паттерны ленивой загрузки'))
    add(code([
        '// Плохо: тяжёлая операция при активации',
        'export async function activate(context: vscode.ExtensionContext) {',
        '    const db = await loadLargeDatabase(); // блокирует старт!',
        '    vscode.commands.registerCommand(\'myext.query\', () => query(db));',
        '}',
        '',
        '// Хорошо: ленивая инициализация',
        'let db: Database | undefined;',
        '',
        'async function getDB(): Promise<Database> {',
        '    if (!db) db = await loadLargeDatabase();',
        '    return db;',
        '}',
        '',
        'export function activate(context: vscode.ExtensionContext) {',
        '    // Быстро! Только регистрируем команду',
        '    vscode.commands.registerCommand(\'myext.query\', async () => {',
        '        const database = await getDB(); // загружается при первом вызове',
        '        return query(database);',
        '    });',
        '}',
    ]))
    add(sp(3))
    add(p('Сравнение двух подходов к инициализации. Плохой вариант выполняет <b>await loadLargeDatabase()</b> прямо в activate — это блокирует старт VS Code. Хороший вариант оборачивает тяжёлую операцию в функцию с кэшированием: база загружается только при первом вызове команды, а activate завершается мгновенно.'))

    add(sp(6))

    add(h2('Debounce и Throttle для частых событий'))
    add(p('Избегайте тяжёлых операций при каждом нажатии клавиши. '
          'VS Code не предоставляет встроенный debounce/throttle. '
          'Варианты: нативный setTimeout или библиотека <b>es-toolkit</b> '
          '(активная замена lodash: 2-3× быстрее, в 97% меньше, нативный TypeScript):'))
    add(sp(3))
    add(code([
        '// Вариант 1: нативный debounce через setTimeout (без зависимостей)',
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
        '// Применение: валидация с debounce 500ms',
        'const debouncedValidate = debounce((doc: vscode.TextDocument) => {',
        '    validateDocument(doc); // тяжёлая операция',
        '}, 500);',
        '',
        'vscode.workspace.onDidChangeTextDocument(e => {',
        '    debouncedValidate(e.document);',
        '}, null, context.subscriptions);',
        '',
        '// Вариант 2: es-toolkit (npm install es-toolkit)',
        '// import { debounce, throttle } from "es-toolkit";',
        '// const debouncedValidate = debounce(validateDocument, 500);',
        '// debouncedValidate.cancel() — для отмены при деактивации',
    ]))
    add(sp(3))
    add(p('Паттерн debounce через <b>setTimeout/clearTimeout</b>: каждый новый вызов сбрасывает предыдущий таймер — обработчик срабатывает только после паузы в N мс. Применяется для <b>onDidChangeTextDocument</b> чтобы не запускать анализ при каждом нажатии клавиши.'))
    add(sp(6))

    add(h2('Отмена долгих операций'))
    add(p('Все провайдеры получают CancellationToken — всегда проверяйте его:'))
    add(sp(3))
    add(code([
        '// В Language Provider',
        'async provideCompletionItems(',
        '    document: vscode.TextDocument,',
        '    position: vscode.Position,',
        '    token: vscode.CancellationToken  // <- ВСЕГДА принимайте token',
        '): Promise<vscode.CompletionItem[]> {',
        '',
        '    // Проверяем отмену перед тяжёлой операцией',
        '    if (token.isCancellationRequested) return [];',
        '',
        '    const results = await fetchCompletions(document, position);',
        '',
        '    // Проверяем снова после асинхронной операции',
        '    if (token.isCancellationRequested) return [];',
        '',
        '    return results;',
        '}',
        '',
        '// Передача token в fetch',
        'async function fetchCompletions(',
        '    doc: vscode.TextDocument,',
        '    pos: vscode.Position',
        '): Promise<vscode.CompletionItem[]> {',
        '    // Можно слушать token для отмены запроса',
        '    const abortController = new AbortController();',
        '    // если нужен token: token.onCancellationRequested(() => abortController.abort());',
        '    const response = await fetch(\'https://api.example.com/complete\', {',
        '        signal: abortController.signal',
        '    });',
        '    return await response.json();',
        '}',
    ]))
    add(sp(3))
    add(p('Правильная работа с <b>CancellationToken</b> в провайдерах. Проверяйте <b>token.isCancellationRequested</b> дважды: перед тяжёлой операцией и после каждого await. Для отмены HTTP-запросов подключите <b>AbortController</b> к событию <b>token.onCancellationRequested</b> — это прерывает fetch, а не просто игнорирует результат.'))

    add(sp(6))

    add(h2('Диагностика производительности расширения'))
    add(p('Несколько встроенных инструментов для профилирования расширений:'))
    add(sp(2))
    for item in [
        '<b>Help → Toggle Developer Tools</b> → Console: видны все console.log из расширения',
        '<b>Help → Developer: Show Running Extensions</b>: время активации и потребление ресурсов',
        '<b>Developer: Inspect Extension Host</b>: подключить Node.js профайлер к Extension Host',
        '<b>Developer: Set Log Level</b>: управление уровнем логирования',
        '<b>Output Channel</b>: просмотр логов расширения через View → Output',
    ]:
        add(bul(item))
    add(pb())

    return A


if __name__ == '__main__':
    print(f'Part 3 has {len(build_story_part3())} elements')
