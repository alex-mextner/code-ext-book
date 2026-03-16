"""
book_appendices_en.py — Appendices A/B/C + Webview CSS tokens
Placed at the end of the book.
"""
from book_helpers import *


def build_appendices():
    A = []
    def add(*x):
        for i in x: A.append(i)
    def ch(num, title, sub=''):
        part = f'Appendix {num}'
        # Stable bookmark for cross-references: <a href="#appendix_A"> etc.
        add(StableAnchor(f'appendix_{num}'))
        add(toc_ch(f'{part}: {title}'), banner(part, title, sub), sp(12))

    # -- APPENDIX A ---------------------------------------------------------------
    ch('A', 'VS Code API', 'Key methods by namespace')
    add(p('Current version: <b>code.visualstudio.com/api/references/vscode-api</b>'))
    add(sp(4))

    add(h2('vscode.window'))
    add(tblh(['Method / Property', 'Description']))
    add(tbl2([
        ('showInformationMessage(msg, ...items)', 'Information notification, returns the selected item'),
        ('showWarningMessage(msg, ...items)',     'Warning notification'),
        ('showErrorMessage(msg, ...items)',       'Error message'),
        ('showInputBox(options)',                  'Input field. Promise<string | undefined>'),
        ('showQuickPick(items, options)',          'Selection list. Returns the selected element'),
        ('showOpenDialog(options)',                'File picker dialog. Returns Uri[]'),
        ('showSaveDialog(options)',                'Save dialog'),
        ('showTextDocument(doc, options)',         'Open a TextDocument in the editor'),
        ('createWebviewPanel(type,title,col,opt)', 'Create a Webview panel'),
        ('createTreeView(viewId, options)',        'Tree View with full control'),
        ('createStatusBarItem(align, priority)',   'Status Bar element'),
        ('createOutputChannel(name)',              'Output channel'),
        ('createTerminal(options)',                'Integrated terminal'),
        ('withProgress(options, task)',            'Execute a task with progress'),
        ('activeTextEditor',                       'Active TextEditor or undefined'),
        ('visibleTextEditors',                     'All visible editors'),
        ('onDidChangeActiveTextEditor',            'Event: active editor changed'),
    ], 0.48))
    add(sp(6))

    add(h2('vscode.workspace'))
    add(tblh(['Method / Property', 'Description']))
    add(tbl2([
        ('workspaceFolders',                    'Array of open workspace folders'),
        ('openTextDocument(uri | path)',         'Open a document. Promise<TextDocument>'),
        ('getConfiguration(section)',            'Get WorkspaceConfiguration'),
        ('findFiles(pattern, exclude)',          'Find files by glob'),
        ('createFileSystemWatcher(glob)',        'Watch for file changes'),
        ('applyEdit(edit)',                      'Apply a WorkspaceEdit'),
        ('fs',                                   'vscode.FileSystem — file system API'),
        ('onDidOpenTextDocument',                'Event: document opened'),
        ('onDidChangeTextDocument',              'Event: document changed'),
        ('onDidSaveTextDocument',                'Event: document saved'),
        ('onDidCloseTextDocument',               'Event: document closed'),
        ('registerTextDocumentContentProvider', 'Virtual document provider'),
    ], 0.48))
    add(sp(6))

    add(h2('vscode.languages'))
    add(tblh(['Method', 'Description']))
    add(tbl2([
        ('createDiagnosticCollection(name)',               'Create a diagnostic collection'),
        ('registerCompletionItemProvider(sel, prov, ...)', 'Completion provider'),
        ('registerHoverProvider(sel, provider)',           'Hover provider'),
        ('registerDefinitionProvider(sel, provider)',      'Go-to-definition provider'),
        ('registerReferenceProvider(sel, provider)',       'Find-references provider'),
        ('registerCodeActionsProvider(sel, provider)',     'Code Actions provider'),
        ('registerDocumentFormattingEditProvider(sel,prov)','Formatter'),
        ('registerDocumentHighlightProvider(sel, prov)',   'Highlight provider'),
        ('registerRenameProvider(sel, provider)',          'Rename provider'),
        ('registerSignatureHelpProvider(sel, prov, ...)',  'Signature help provider'),
        ('getDiagnostics(uri)',                            'Get diagnostics for a URI'),
    ], 0.55))
    add(pb())

    # -- APPENDIX B ---------------------------------------------------------------
    ch('B', 'Contribution Points', 'Full list of VS Code extension points')
    add(p('Current version: <b>code.visualstudio.com/api/references/contribution-points</b>'))
    add(sp(4))

    add(tblh(['Contribution Point', 'Purpose']))
    add(tbl2([
        ('contributes.commands',          'Commands: title, category, icon -> Command Palette'),
        ('contributes.menus',             'Menu items in 20+ locations: editor/context, explorer/context, view/title...'),
        ('contributes.keybindings',       'Keyboard shortcuts: key, command, when, mac'),
        ('contributes.configuration',     'Settings in Settings UI: properties with types and defaults'),
        ('contributes.configurationDefaults','Defaults for specific languages'),
        ('contributes.languages',         'Language: id, aliases, extensions, configuration, icon'),
        ('contributes.grammars',          'TextMate grammars for syntax highlighting'),
        ('contributes.snippets',          'Snippet files for languages'),
        ('contributes.themes',            'Editor and UI color themes'),
        ('contributes.iconThemes',        'File icon themes'),
        ('contributes.productIconThemes', 'VS Code interface icon themes'),
        ('contributes.views',             'Tree View: id, name, icon, contextualTitle'),
        ('contributes.viewsContainers',   'Containers for Views in Activity Bar or Panel'),
        ('contributes.viewsWelcome',      'Welcome content for empty Views'),
        ('contributes.taskDefinitions',   'Task types for Task Provider'),
        ('contributes.problemMatchers',   'Patterns for parsing task output into errors'),
        ('contributes.debuggers',         'Debug Adapter: type, label, languages'),
        ('contributes.breakpoints',       'Breakpoint types for languages'),
        ('contributes.walkthroughs',      'Step-by-step tutorials: id, title, steps'),
        ('contributes.chatParticipants',  'AI Chat Participants: id, name, commands'),
        ('contributes.languageModels',    'Custom Language Model providers'),
        ('contributes.colors',            'New theme colors: id, description, defaults'),
        ('contributes.customEditors',     'Custom editors: viewType, selector, priority'),
        ('contributes.notebooks',         'Custom notebook formats'),
        ('contributes.authentication',    'Authentication Provider: id, label'),
        ('contributes.jsonValidation',    'JSON Schema validation by URL pattern'),
        ('contributes.mcpServerDefinitionProviders', 'MCP Server providers for AI'),
    ]))
    add(pb())

    # -- APPENDIX C ---------------------------------------------------------------
    ch('C', 'Activation Events', 'Full list of activation events')
    add(p('Current version: <b>code.visualstudio.com/api/references/activation-events</b>'))
    add(sp(4))

    add(tblh(['Event', 'When it fires']))
    add(tbl2([
        ('onCommand:id',             'On first invocation of the command with the given ID'),
        ('onLanguage:langId',        'When a file with the given language is opened'),
        ('onView:viewId',            'When the View is first opened'),
        ('onViewContainer:id',       'When the View container is opened'),
        ('workspaceContains:pattern','If the workspace contains a file matching the pattern'),
        ('onFileSystem:scheme',      'When a file with a non-standard URI scheme is accessed'),
        ('onUri',                    'When a vscode://publisher.extension URI is opened'),
        ('onWebviewPanel:viewType',  'When a Webview is restored after VS Code restart'),
        ('onCustomEditor:viewType',  'When a custom editor is opened'),
        ('onNotebook:type',          'When a Notebook of the given type is opened'),
        ('onDebug',                  'On any debug session start'),
        ('onDebugResolve:type',      'When resolving a debug configuration'),
        ('onStartupFinished',        'After VS Code is fully loaded — does not block startup'),
        ('onTaskType:type',          'When a task of the given type is executed'),
        ('onChatParticipant:id',     'When an AI Chat Participant is invoked'),
        ('onAuthenticationRequest',  'On an authentication request'),
        ('*',                        'AVOID: fires on every VS Code startup'),
    ]))
    add(sp(4))
    add(box('Automatic Activation Events (VS Code 1.74+)',
        'Commands, Views, customEditors, and other contributions automatically create '
        'corresponding Activation Events — no need to declare them explicitly. '
        'Explicit declaration is only needed for: workspaceContains, onStartupFinished, onUri, '
        'onFileSystem, onAuthenticationRequest.',
        'note'))
    add(pb())

    # -- APPENDIX D -- Webview CSS variables --------------------------------------
    ch('D', 'VS Code Theme CSS Variables', 'For use in Webview')
    add(p('Full token list: <b>code.visualstudio.com/api/references/theme-color</b>. '
          'Use these variables in your Webview CSS so the interface automatically '
          'adapts when the user changes their theme.'))
    add(sp(4))

    add(h2('Core Editor Variables'))
    add(tblh(['CSS Variable', 'Purpose']))
    add(tbl2([
        ('--vscode-editor-background',        'Editor background'),
        ('--vscode-editor-foreground',        'Editor text color'),
        ('--vscode-editor-font-family',       'Editor font family'),
        ('--vscode-editor-font-size',         'Editor font size'),
        ('--vscode-editor-font-weight',       'Editor font weight'),
        ('--vscode-editorLineNumber-foreground', 'Line number color'),
        ('--vscode-editorCursor-foreground',  'Cursor color'),
        ('--vscode-editor-selectionBackground','Selection background'),
    ], 0.55))
    add(sp(4))

    add(h2('UI Elements'))
    add(tblh(['CSS Variable', 'Purpose']))
    add(tbl2([
        ('--vscode-button-background',        'Button background'),
        ('--vscode-button-foreground',        'Button text'),
        ('--vscode-button-hoverBackground',   'Button hover background'),
        ('--vscode-button-border',            'Button border (may be transparent)'),
        ('--vscode-button-secondaryBackground',     'Secondary button background'),
        ('--vscode-button-secondaryForeground',     'Secondary button text'),
        ('--vscode-input-background',         'Input field background'),
        ('--vscode-input-foreground',         'Input field text'),
        ('--vscode-input-border',             'Input field border'),
        ('--vscode-input-placeholderForeground', 'Placeholder color'),
        ('--vscode-focusBorder',              'Focus border (Accessibility)'),
        ('--vscode-badge-background',         'Badge/counter background'),
        ('--vscode-badge-foreground',         'Badge text'),
        ('--vscode-list-activeSelectionBackground', 'Selected list item background'),
        ('--vscode-list-activeSelectionForeground', 'Selected list item text'),
        ('--vscode-list-hoverBackground',     'List item hover background'),
    ], 0.55))
    add(sp(4))

    add(h2('Text and Links'))
    add(tblh(['CSS Variable', 'Purpose']))
    add(tbl2([
        ('--vscode-foreground',               'Primary interface text color'),
        ('--vscode-descriptionForeground',    'Secondary text, descriptions'),
        ('--vscode-disabledForeground',       'Disabled elements'),
        ('--vscode-textLink-foreground',      'Link color'),
        ('--vscode-textLink-activeForeground','Active link color'),
        ('--vscode-textCodeBlock-background', 'Inline code background'),
        ('--vscode-textBlockQuote-background','Block quote background'),
        ('--vscode-textSeparator-foreground', 'Separator color'),
    ], 0.55))
    add(sp(4))

    add(h2('Panels and Containers'))
    add(tblh(['CSS Variable', 'Purpose']))
    add(tbl2([
        ('--vscode-sideBar-background',        'Sidebar background'),
        ('--vscode-sideBar-foreground',        'Sidebar text'),
        ('--vscode-sideBar-border',            'Sidebar border'),
        ('--vscode-panel-background',          'Bottom panel background (Terminal, Problems)'),
        ('--vscode-panel-border',              'Panel border'),
        ('--vscode-statusBar-background',      'Status Bar background'),
        ('--vscode-statusBar-foreground',      'Status Bar text'),
        ('--vscode-tab-activeBackground',      'Active tab background'),
        ('--vscode-tab-inactiveBackground',    'Inactive tab background'),
        ('--vscode-tab-activeForeground',      'Active tab text'),
    ], 0.55))
    add(sp(4))

    add(h2('Webview Theme Template'))
    add(p('Use these variables in your Webview CSS for automatic theme adaptation:'))
    add(sp(3))
    add(code([
        '/* Minimal Webview CSS template */  ',
        'body {',
        '    background-color: var(--vscode-editor-background);',
        '    color: var(--vscode-editor-foreground);',
        '    font-family: var(--vscode-font-family);',
        '    font-size: var(--vscode-font-size);',
        '    /* Important: remove browser margin */',
        '    margin: 0; padding: 16px;',
        '}',
        '',
        'button.primary {',
        '    background: var(--vscode-button-background);',
        '    color: var(--vscode-button-foreground);',
        '    border: 1px solid var(--vscode-button-border, transparent);',
        '    padding: 4px 12px; border-radius: 2px; cursor: pointer;',
        '}',
        'button.primary:hover { background: var(--vscode-button-hoverBackground); }',
        '',
        'input, textarea, select {',
        '    background: var(--vscode-input-background);',
        '    color: var(--vscode-input-foreground);',
        '    border: 1px solid var(--vscode-input-border);',
        '    padding: 4px 8px;',
        '}',
        '',
        'a { color: var(--vscode-textLink-foreground); }',
        'a:hover { color: var(--vscode-textLink-activeForeground); }',
        '',
        'code, pre {',
        '    background: var(--vscode-textCodeBlock-background);',
        '    font-family: var(--vscode-editor-font-family);',
        '    font-size: var(--vscode-editor-font-size);',
        '}',
        '',
        '/* VS Code adds class vscode-dark / vscode-light / vscode-high-contrast */',
        '/* to <body> — use it for fine-tuning */',
        '.vscode-dark .special { border-color: rgba(255,255,255,0.1); }',
        '.vscode-light .special { border-color: rgba(0,0,0,0.1); }',
    ], highlight=False))
    add(sp(4))
    add(box('Why CSS variables instead of hard-coded colors',
        'VS Code has Light, Dark, High Contrast dark and light themes, '
        'plus thousands of user themes from the Marketplace. '
        'A hard-coded hex #1e1e1e looks fine in one theme and terrible in another. '
        'Also, Webview works in the web version (vscode.dev) — themes change dynamically there. '
        'CSS variables update automatically when the theme changes without reloading the Webview.',
        'note'))
    add(pb())

    return A


if __name__ == '__main__':
    print(f'Appendices: {len(build_appendices())} elements')
