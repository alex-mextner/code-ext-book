from book_helpers import *

def build_story_ux():
    A = []
    def add(*x):
        for i in x: A.append(i)

    def section(title, sub='', anchor_key=None):
        if anchor_key:
            add(StableAnchor(anchor_key))
        add(toc_ch(title), banner('User Experience', title, sub), sp(12))

    section('Designing Extension UX',
            'Unobtrusiveness, discoverability, and coexistence',
            anchor_key='chapter_ux')

    from book_new_en import q_ux
    add(q_ux())
    add(sp(6))

    add(h2('Philosophy: the Extension as a Good Neighbor'))
    add(p('The average VS Code user has <b>13-20 installed extensions</b>. '
          'Each one competes for their attention, occupies UI space, '
          'and affects performance. A good extension behaves like '
          'a quiet professional: does its job unobtrusively, appears when needed, '
          'and creates no noise.'))
    add(sp(4))
    add(p('The VS Code team formulates this as the <b>"Progressive Disclosure"</b> principle: '
          'basic functionality is visible immediately, '
          'advanced capabilities are hidden and available when needed.'))
    add(sp(6))

    # -- 1. ATTENTION BUDGET ----------------------------------------------------
    add(h1('User Attention Budget'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Competing for UI Space'))
    add(p('VS Code has a limited number of places where extensions can add '
          'elements. Think of each place as a "slot", '
          'and the budget for all extensions combined is fixed:'))
    add(sp(3))
    add(tblh(['Location', 'Recommended limit per extension']))
    add(tbl2([
        ('Activity Bar',     '1 icon — only if the extension requires constant access'),
        ('Status Bar',       '1-2 items max; only permanently relevant information'),
        ('Editor Toolbar',   '1 button; only for target language files (via when)'),
        ('Context Menu',     '1-3 items; only relevant to the context'),
        ('Command Palette',  'No limit, but name with a category: "My Ext: Action"'),
        ('Notifications',    '0 on activation; only in response to explicit user actions'),
        ('Diagnostics',      'Only real problems; don\'t turn into noise'),
    ]))
    add(sp(4))
    add(box('Reality',
        'When 15 extensions each add 2 items to the Status Bar — '
        'the bottom bar of VS Code becomes an unreadable jumble of icons. '
        'When 5 extensions add icons to the Activity Bar — '
        'it becomes an overloaded panel. '
        'Your extension is one of many. Minimize your footprint.', 'warn'))
    add(sp(6))

    add(h2('The Principle of Contextuality: Show Only What\'s Relevant'))
    add(p('Every UI element should appear only in a relevant context. '
          'The key mechanism is the <b>when</b> condition in Contribution Points:'))
    add(sp(3))
    add(code([
        '// BAD: button visible always, even in .json and .txt files',
        '"editor/title": [{',
        '  "command": "myGoExt.runFile",',
        '  "group": "navigation"',
        '}]',
        '',
        '// OK: GOOD: button only for Go files',
        '"editor/title": [{',
        '  "command": "myGoExt.runFile",',
        '  "when": "resourceLangId == go",',
        '  "group": "navigation"',
        '}]',
        '',
        '// OK: BETTER: only when there is an active editor with Go',
        '"editor/title": [{',
        '  "command": "myGoExt.runFile",',
        '  "when": "resourceLangId == go && !isInDiffEditor",',
        '  "group": "navigation"',
        '}]',
    ]))
    add(sp(3))
    add(p('Three variants of <b>when</b> condition for a button in editor/title — from bad to best. Without a condition the button is visible for all files, <b>resourceLangId == go</b> restricts by language, and adding <b>!isInDiffEditor</b> removes the button from diff mode where it is useless.'))

    add(sp(3))
    add(code([
        '// Status Bar: show only when needed',
        'const statusItem = vscode.window.createStatusBarItem(',
        '    vscode.StatusBarAlignment.Left, 10',
        ');',
        '',
        '// Listen for active editor changes',
        'function updateVisibility(editor: vscode.TextEditor | undefined) {',
        '    if (editor?.document.languageId === \'go\') {',
        '        statusItem.show();',
        '    } else {',
        '        statusItem.hide();  // <- HIDE for irrelevant files',
        '    }',
        '}',
        '',
        'vscode.window.onDidChangeActiveTextEditor(updateVisibility,',
        '    null, context.subscriptions);',
        'updateVisibility(vscode.window.activeTextEditor);',
    ]))
    add(sp(3))
    add(p('Programmatic visibility control of a Status Bar item: <b>show()</b> and <b>hide()</b> are called on active editor change via <b>onDidChangeActiveTextEditor</b>. The item is visible only when a file of the target language is open — otherwise it is hidden and takes no space.'))

    add(sp(6))

    add(h2('Decision Tree: Should You Show a Notification?'))
    add(p('The official VS Code team decision tree for notifications:'))
    add(sp(3))
    add(tblh(['Situation', 'Correct response']))
    add(tbl2([
        ('Immediate input needed (multi-step)',    'Quick Pick or InputBox'),
        ('Immediate input needed (single step)',    'Modal Dialog'),
        ('Background progress (low priority)',      'Progress in Status Bar'),
        ('User initiated an operation',             'Notification (on completion)'),
        ('Multiple notifications in a row',         'Combine into one'),
        ('User doesn\'t need to know',              'Show nothing'),
        ('Background error that can\'t be fixed',   'Output Channel, not a popup'),
        ('Critical error requiring action',         'Error notification with a button'),
    ]))
    add(sp(4))
    add(box('One Notification Rule',
        'Show at most one notification at a time. '
        'If you need to show several — combine them or show sequentially '
        'after the previous one is dismissed.', 'note'))
    add(sp(4))
    from book_new_en import q_notifications
    add(q_notifications())
    add(sp(6))

    add(h2('"Don\'t Show Again" Button'))
    add(p('Every notification that could potentially repeat '
          'must have a dismiss option. This is an official VS Code UX Guidelines requirement:'))
    add(sp(3))
    add(code([
        'async function showImportantWarning(ctx: vscode.ExtensionContext) {',
        '    const DISMISSED_KEY = \'warningDismissed\';',
        '',
        '    // Don\'t show if user already dismissed',
        '    if (ctx.globalState.get<boolean>(DISMISSED_KEY)) return;',
        '',
        '    const action = await vscode.window.showWarningMessage(',
        '        \'My Extension: outdated configuration detected\',',
        '        \'Fix\',',
        '        \'Learn More\',',
        '        \'Don\\\'t Show Again\'  // <- ALWAYS include this option',
        '    );',
        '',
        '    if (action === \'Fix\') {',
        '        await fixConfiguration();',
        '    } else if (action === \'Learn More\') {',
        '        vscode.env.openExternal(vscode.Uri.parse(DOCS_URL));',
        '    } else if (action === \'Don\\\'t Show Again\') {',
        '        await ctx.globalState.update(DISMISSED_KEY, true);',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('The "notification with memory" pattern: the function checks <b>globalState</b> and does not show the warning again. The <b>"Don\'t Show Again"</b> button writes a flag to storage — this is a mandatory element of any repeating notification per the VS Code UX Guidelines.'))

    add(sp(6))

    # -- 2. DISCOVERABILITY -----------------------------------------------------
    add(h1('Discoverability: "Visible but Unobtrusive"'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('The Problem: Users Don\'t Read README'))
    add(p('Studies show that most users install '
          'an extension, try one or two commands, and forget about the rest. '
          'The design challenge is to make features <b>discoverable at the right moment</b>.'))
    add(sp(6))

    add(h2('Walkthroughs — Proper Onboarding'))
    add(p('Walkthroughs are a built-in VS Code mechanism for interactive onboarding. '
          'Opened via Get Started / Welcome, they guide the user '
          'through key features without popups:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "walkthroughs": [{',
        '    "id": "myExt.getStarted",',
        '    "title": "Getting Started with My Extension",',
        '    "description": "Master key features in 5 minutes",',
        '    "steps": [',
        '      {',
        '        "id": "myExt.step1",',
        '        "title": "Configure the extension",',
        '        "description": "Open settings and choose your preferences\\n[Open Settings](command:myExt.openSettings)",',
        '        "media": {',
        '          "svg": "media/step1.svg",',
        '          "altText": "Settings screenshot"',
        '        },',
        '        "completionEvents": [',
        '          "onSettingsEdited:myExt.maxItems"',
        '        ]',
        '      },',
        '      {',
        '        "id": "myExt.step2",',
        '        "title": "Try the main feature",',
        '        "description": "Click the button or use the command\\n[Run Command](command:myExt.mainAction)",',
        '        "media": { "svg": "media/step2.svg", "altText": "Demo" },',
        '        "completionEvents": ["onCommand:myExt.mainAction"]',
        '      }',
        '    ]',
        '  }]',
        '}',
        '',
        '// Open walkthrough programmatically (only on first install)',
        'if (!ctx.globalState.get(\'walkthroughShown\')) {',
        '    ctx.globalState.update(\'walkthroughShown\', true);',
        '    vscode.commands.executeCommand(',
        '        \'workbench.action.openWalkthrough\',',
        '        \'publisher.extension#myExt.getStarted\'',
        '    );',
        '}',
    ]))
    add(sp(3))
    add(p('Complete Walkthrough structure: steps with titles, descriptions, and <b>completionEvents</b> are declared in <b>package.json</b> — VS Code automatically marks a step as completed when the event fires (setting change, command execution). Links <b>[text](command:...)</b> in descriptions become clickable buttons. Programmatic opening via <b>workbench.action.openWalkthrough</b> is tied to a flag in globalState — shown only on first install.'))

    add(sp(4))
    add(box('Walkthrough Image Requirements',
        'Use SVG with VS Code theme CSS color variables — '
        'they automatically adapt to dark and light themes. '
        'PNG/GIF will look out of place in a dark theme. '
        'The "VS Code Color Mapper" Figma plugin simplifies creating such SVGs.', 'tip'))
    add(sp(6))

    add(h2('Contextual Hints — Tips at the Right Moment'))
    add(p('Show hints not at startup, but when the user encounters '
          'a specific situation:'))
    add(sp(3))
    add(code([
        '// Hint on first open of target file type',
        'let goHintShown = false;',
        '',
        'vscode.workspace.onDidOpenTextDocument(async doc => {',
        '    if (doc.languageId !== \'go\' || goHintShown) return;',
        '    if (ctx.globalState.get(\'goHintDismissed\')) return;',
        '',
        '    goHintShown = true;',
        '',
        '    // Non-intrusive hint: status bar instead of notification',
        '    const hint = vscode.window.createStatusBarItem(',
        '        vscode.StatusBarAlignment.Right, 0',
        '    );',
        '    hint.text = \'$(lightbulb) My Ext: click for quick actions\';',
        '    hint.command = \'myExt.showQuickActions\';',
        '    hint.backgroundColor = new vscode.ThemeColor(',
        '        \'statusBarItem.warningBackground\'',
        '    );',
        '    hint.show();',
        '',
        '    // Automatically hide after 10 seconds',
        '    setTimeout(() => hint.dispose(), 10000);',
        '',
        '    context.subscriptions.push(hint);',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('A contextual hint via a temporary Status Bar item instead of a popup notification. The hint appears once on the first open of a target file type, is highlighted via <b>warningBackground</b> to attract attention, and automatically disappears after 10 seconds using <b>setTimeout + dispose()</b>.'))

    add(sp(4))

    add(h3('Welcome View — for Empty States'))
    add(p('For a Welcome View, you first need to declare the View itself in <b>contributes.views</b> — the view ID <b>myExt.todoList</b> must match the <b>view</b> field in viewsWelcome:'))
    add(sp(3))
    add(code([
        '// First declare the View in contributes.views',
        '"contributes": {',
        '  "viewsContainers": {',
        '    "activitybar": [{ "id": "myExtContainer", "title": "My Extension", "icon": "$(checklist)" }]',
        '  },',
        '  "views": {',
        '    "myExtContainer": [{',
        '      "id": "myExt.todoList",  // <- this ID is used in viewsWelcome',
        '      "name": "TODO List"',
        '    }]',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('After declaring the View, you can add Welcome content that is shown when the View is empty:'))
    add(sp(3))
    add(code([
        '// package.json',
        '"contributes": {',
        '  "viewsWelcome": [{',
        '    "view": "myExt.todoList",',
        '    "contents": "No TODO comments found in the project.\\n[Create First TODO](command:myExt.insertTodo)\\n[Configure Keywords](command:myExt.openSettings)\\n[Open Documentation](https://github.com/me/my-ext#readme)",',
        '    "when": "myExt.todoCount == 0"',
        '  }, {',
        '    "view": "myExt.todoList",',
        '    "contents": "Open a project folder to get started.",',
        '    "when": "!workspaceFolderCount"',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Two Welcome View variants for different states: when the project has no TODO comments (<b>myExt.todoCount == 0</b>) — links to create the first TODO and configure settings; when no folder is open at all (<b>!workspaceFolderCount</b>) — a prompt to open a project. The <b>when</b> condition determines which text is displayed.'))

    add(sp(6))

    add(h2('Command Naming: Discoverable by Default'))
    add(p('Most users find features through the Command Palette. '
          'Proper naming is critically important for discoverability:'))
    add(sp(3))
    add(tblh(['Bad', 'Good']))
    add(tbl2([
        ('"Run"',                          '"My Extension: Run File"'),
        ('"Format document"',              '"Prettier: Format Document" (with category)'),
        ('"myext.action1"',                '"My Extension: Perform Action 1"'),
        ('"Toggle feature"',               '"My Extension: Toggle Dark Mode Analysis"'),
        ('"Go: Build" (no context)',       '"Go: Build Current Package" (specific)'),
    ], 0.45))
    add(sp(3))
    add(code([
        '// Good command naming',
        '"contributes": {',
        '  "commands": [{',
        '    "command": "myGoExt.buildPackage",',
        '    "title": "Build Current Package",',
        '    "category": "Go",',
        '    "shortTitle": "Build",',
        '    "icon": "$(package)"',
        '  }]',
        '}',
        '// In Command Palette: "Go: Build Current Package"',
        '// In context menu: "Build" (via shortTitle)',
    ]))
    add(sp(3))
    add(p('Command declaration with <b>category</b> — VS Code automatically forms the name "Go: Build Current Package" in the Command Palette. The <b>shortTitle</b> field is used in compact locations (context menu, Editor Toolbar), and <b>icon</b> with Codicon syntax <b>$(package)</b> sets the icon without custom SVGs.'))

    add(sp(6))

    # -- 3. CONFLICTS ------------------------------------------------------------
    add(h1('Conflicts Between Extensions'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Types of Conflicts'))
    add(tblh(['Conflict type', 'Examples and solutions']))
    add(tbl2([
        ('Formatters',
         'Prettier + another formatter competing for the same language. '
         'Solution: declare your formatter via documentFormattingEditProvider, '
         'respect editor.defaultFormatter'),
        ('Keybindings',
         'Two extensions register the same Ctrl+Shift+F. '
         'VS Code always warns the user. Solution: use rare combinations '
         'or don\'t register by default'),
        ('Language ID',
         'Two extensions declare the same languageId. '
         'The last installed one "wins". '
         'Solution: use unique IDs, don\'t override others\''),
        ('Completion providers',
         'Multiple providers give duplicate suggestions. '
         'VS Code merges them. Solution: return only unique items'),
        ('Diagnostics',
         'Multiple extensions diagnose the same file, creating duplicates. '
         'Solution: name your collection uniquely, check for duplicates'),
        ('Status Bar',
         'Extensions fill the entire bottom bar. '
         'Solution: limit to 1-2 items, hide when irrelevant'),
    ]))
    add(sp(6))

    add(h2('Formatter Conflicts — Resolution'))
    add(p('The most common conflict in real projects. Proper formatter implementation:'))
    add(sp(3))
    add(code([
        '// Register formatter only for your language',
        'const formatter = vscode.languages.registerDocumentFormattingEditProvider(',
        '    { language: \'mylang\' },  // <- precise selector, not "*"',
        '    {',
        '        provideDocumentFormattingEdits(',
        '            document: vscode.TextDocument,',
        '            options: vscode.FormattingOptions,',
        '            token: vscode.CancellationToken',
        '        ): vscode.TextEdit[] {',
        '            // Check: is our formatter the default?',
        '            const cfg = vscode.workspace.getConfiguration(\'editor\', document);',
        '            const defaultFormatter = cfg.get<string>(\'defaultFormatter\');',
        '',
        '            // If user explicitly chose another formatter — yield',
        '            if (defaultFormatter && defaultFormatter !== \'publisher.myext\') {',
        '                return [];',
        '            }',
        '',
        '            return formatDocument(document, options);',
        '        }',
        '    }',
        ');',
    ]))
    add(sp(3))
    add(p('Correct formatter implementation: registration via <b>registerDocumentFormattingEditProvider</b> with a precise language selector (not "*"). Inside, the provider checks <b>editor.defaultFormatter</b> — if the user explicitly chose another formatter, it returns an empty array and does not interfere.'))

    add(sp(3))
    add(code([
        '// In README.md — guide the user on setup',
        '// To use My Extension as your default formatter, add to settings.json:',
        '// {',
        '//   "[mylang]": {',
        '//     "editor.defaultFormatter": "publisher.myext"',
        '//   }',
        '// }',
    ]))
    add(sp(3))
    add(p('Example README instruction: how to set your extension as the default formatter via <b>editor.defaultFormatter</b> in settings.json with the language specified.'))

    add(sp(6))

    add(h2('Keybinding Conflicts — Strategy'))
    add(p('VS Code warns the user about keybinding conflicts. '
          'Proper strategies:'))
    add(sp(3))
    add(code([
        '// package.json — minimizing keybinding conflicts',
        '"contributes": {',
        '  "keybindings": [{',
        '    "command": "myExt.mainAction",',
        '    "key": "ctrl+alt+shift+m",  // rare combination — fewer conflicts',
        '    "mac": "cmd+alt+shift+m",',
        '    "when": "editorTextFocus && resourceLangId == mylang"  // context!',
        '  }]',
        '}',
        '',
        '// Or don\'t register a default keybinding at all',
        '// Document the recommended shortcut in README',
        '// The user assigns their own convenient key',
    ]))
    add(sp(3))
    add(p('Two strategies for minimizing conflicts: either use a rare combination (<b>ctrl+alt+shift+...</b>) with a <b>when</b> condition to restrict context, or don\'t register a keybinding at all by default — document the recommended shortcut and let the user assign their own.'))

    add(sp(4))
    add(box('Keybinding Best Practice',
        'Don\'t register default keybindings for secondary functions. '
        'Describe recommended shortcuts in README. '
        'Users assign keys themselves via keybindings.json — '
        'this way there will be no conflicts at all.', 'tip'))
    add(sp(6))

    add(h2('Declaring Compatibility and Dependencies'))
    add(p('In package.json you can explicitly declare dependencies and recommendations:'))
    add(sp(3))
    add(code([
        '// package.json',
        '{',
        '  // Required dependencies — installed automatically',
        '  // Use only for TRULY necessary extensions',
        '  "extensionDependencies": [',
        '    "vscode.git"  // built-in extension',
        '  ],',
        '',
        '  // Extension Pack — installs a set together',
        '  // SHOULD NOT have functional dependencies on each other',
        '  "extensionPack": [',
        '    "publisher.extension1",',
        '    "publisher.extension2"',
        '  ]',
        '}',
        '',
        '// .vscode/extensions.json — project recommendations',
        '// VS Code shows "Recommended extensions" popup when opening the project',
        '{',
        '  // recommendations: VS Code will suggest installing these extensions',
        '  "recommendations": ["publisher.myext"],',
        '',
        '  // unwantedRecommendations: suppress recommendations for conflicting extensions',
        '  // If the user already uses your extension — VS Code won\'t',
        '  // suggest installing a conflicting one (e.g., two formatters for the same language)',
        '  "unwantedRecommendations": ["publisher.conflicting-ext"]',
        '}',
    ]))
    add(sp(3))
    add(p('Three mechanisms for managing dependencies: <b>extensionDependencies</b> installs required extensions automatically, <b>extensionPack</b> creates a set of extensions for joint installation, and <b>.vscode/extensions.json</b> at the project level recommends needed extensions and suppresses recommendations for conflicting ones via <b>unwantedRecommendations</b>.'))

    add(sp(3))
    add(box('What is unwantedRecommendations',
        '<b>unwantedRecommendations</b> is an array of extension IDs that VS Code '
        'will not suggest installing in this project. '
        'Useful for monorepos where one extension replaces another '
        '(e.g., your formatter instead of Prettier), or where conflicts '
        'are known. VS Code won\'t forcefully remove them — it will only stop '
        'showing the recommendation popup for the listed IDs. '
        'Source: code.visualstudio.com/docs/editor/extension-marketplace#_workspace-recommended-extensions',
        'note'))
    add(sp(4))

    add(h3('Detecting Conflicting Extensions in Code'))
    add(p('If your extension conflicts with another — detect it and inform the user politely:'))
    add(sp(3))
    add(code([
        'async function checkForConflicts(ctx: vscode.ExtensionContext) {',
        '    const CONFLICT_KEY = \'conflictWarningShown\';',
        '    if (ctx.globalState.get<boolean>(CONFLICT_KEY)) return;',
        '',
        '    // List of known conflicting extensions',
        '    const conflicting = [',
        '        \'publisher.old-formatter\',',
        '        \'publisher.legacy-linter\',',
        '    ];',
        '',
        '    const found = conflicting.filter(id =>',
        '        vscode.extensions.getExtension(id)?.isActive',
        '    );',
        '',
        '    if (found.length === 0) return;',
        '',
        '    await ctx.globalState.update(CONFLICT_KEY, true);',
        '',
        '    const names = found.map(id => id.split(\'.\')[1]).join(\', \');',
        '    const action = await vscode.window.showWarningMessage(',
        '        `My Extension: potentially conflicting extension detected: ${names}. ` +',
        '        \'We recommend disabling it for correct operation.\',',
        '        \'Learn More\',',
        '        \'Got It\'',
        '    );',
        '',
        '    if (action === \'Learn More\') {',
        '        vscode.env.openExternal(vscode.Uri.parse(COMPAT_DOCS_URL));',
        '    }',
        '}',
    ]))
    add(sp(3))
    add(p('Runtime detection of conflicting extensions: <b>vscode.extensions.getExtension()</b> checks for the presence and activity of known competitors. The warning is shown once (flag in <b>globalState</b>) and offers to learn more — without aggressively demanding removal of the other extension.'))

    add(sp(6))

    add(h2('Document Selector — Precision as Conflict Prevention'))
    add(p('<b>Document Selector</b> is a filter that determines which documents '
          'your provider is active for (hover, completion, formatting, diagnostics, etc.). '
          'This is not optional — it is a mandatory first argument when registering any language provider. '
          'VS Code calls your provider <i>only</i> for documents '
          'matching the selector. '
          'Reference for all fields: <b>code.visualstudio.com/api/references/document-selector</b>'))
    add(sp(3))
    add(box('Document Selector — the Main Anti-Conflict Tool',
        'When two extensions register a provider for <b>"*"</b> — they compete '
        'for all documents in the editor. The user opens a .json file and gets '
        'hover hints from a Python extension. This is the real cause of most '
        'conflicts between extensions. '
        'A precise selector {language: "typescript", scheme: "file"} means: '
        '"my provider works only with .ts files on disk, and nothing else". '
        'That is respect for others\' space.', 'warn'))
    add(sp(3))
    add(p('The selector can be a string (languageId), an object, or an array of objects. '
          'Object fields: <b>language</b> (languageId), <b>scheme</b> (file/untitled/vscode-remote), '
          '<b>pattern</b> (glob), <b>notebookType</b>.'))
    add(sp(3))
    add(p('<b>Precision as conflict prevention.</b> '
          'The more precise the selector, the less chance of stepping on someone else\'s territory:'))
    add(sp(3))
    add(code([
        '// BAD: active for all files — hijacks hover from other extensions',
        'vscode.languages.registerHoverProvider(\'*\', myProvider)',
        '',
        '// BAD: active for all file documents — including .json, .md, .yaml',
        'vscode.languages.registerHoverProvider({ scheme: \'file\' }, myProvider)',
        '',
        '// OK: only .mylang files from the file system',
        'vscode.languages.registerHoverProvider(',
        '    { scheme: \'file\', language: \'mylang\' },',
        '    myProvider',
        '    // Argument 1: selector — FOR which documents',
        '    // Argument 2: provider — what to do',
        ')',
        '',
        '// OK: including untitled (new unsaved files)',
        '// Array = union (OR): fires if the document matches at least one',
        'vscode.languages.registerHoverProvider(',
        '    [',
        '        { scheme: \'file\',     language: \'mylang\' },',
        '        { scheme: \'untitled\', language: \'mylang\' },',
        '    ],',
        '    myProvider',
        ')',
        '',
        '// OK: exclude Notebook cells (notebookType: undefined = regular files)',
        'vscode.languages.registerCompletionItemProvider(',
        '    { scheme: \'file\', language: \'typescript\', notebookType: undefined },',
        '    completionProvider',
        ')',
    ]))
    add(sp(3))
    add(p('Document Selector precision evolution: from "*" (all files — guaranteed conflict) to precise <b>scheme + language</b> combinations. An array of selectors works as OR — you can include both file and untitled documents. The <b>notebookType: undefined</b> field excludes Jupyter notebook cells.'))

    add(sp(6))

    # -- 4. PROGRESSIVE DISCLOSURE -----------------------------------------------
    add(h1('Progressive Disclosure and Multi-Level UX'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Three Levels of Feature Access'))
    add(p('A good extension has three levels of access to its capabilities:'))
    add(sp(3))
    add(tblh(['Level', 'What lives here']))
    add(tbl2([
        ('1. Always visible',
         'One Status Bar item or minimal set. '
         'Only what is needed constantly. Example: current Python version in the status bar'),
        ('2. In context',
         'Editor Toolbar buttons, context menu items. '
         'Appear only for relevant files. '
         'Example: "Run" button for .py files'),
        ('3. On demand',
         'Command Palette, Tree View, Webview. '
         'User-initiated. '
         'Example: "Python: Select Interpreter" in Command Palette'),
    ]))
    add(sp(4))
    add(box('The Pyramid Rule',
        'Most features should live at level 3 (on demand). '
        'Level 2 — for frequent contextual actions. '
        'Level 1 — only for constantly relevant information. '
        'The lower the level, the fewer elements.', 'note'))
    add(sp(6))

    add(h2('Settings: Give the User Control'))
    add(p('Every noticeable extension feature should be toggleable. '
          'This is the golden rule from the source code of GitLens, Pylance, and Prettier:'))
    add(sp(3))
    add(code([
        '// package.json — full control over visibility',
        '"contributes": {',
        '  "configuration": {',
        '    "properties": {',
        '      "myExt.showStatusBarItem": {',
        '        "type": "boolean",',
        '        "default": true,',
        '        "description": "Show item in the status bar"',
        '      },',
        '      "myExt.showInlineDecorations": {',
        '        "type": "boolean",',
        '        "default": true,',
        '        "description": "Show inline annotations in the editor"',
        '      },',
        '      "myExt.showActivityBarIcon": {',
        '        "type": "boolean",',
        '        "default": false,  // <- OFF by default!',
        '        "description": "Show icon in Activity Bar"',
        '      },',
        '      "myExt.enableOnSave": {',
        '        "type": "boolean",',
        '        "default": true,',
        '        "description": "Run automatically on file save"',
        '      }',
        '    }',
        '  }',
        '}',
        '',
        '// In code — read settings',
        'function getConfig() {',
        '    const cfg = vscode.workspace.getConfiguration(\'myExt\');',
        '    return {',
        '        showStatusBar: cfg.get<boolean>(\'showStatusBarItem\', true),',
        '        showDecorations: cfg.get<boolean>(\'showInlineDecorations\', true),',
        '    };',
        '}',
    ]))
    add(sp(3))
    add(p('Declaring visibility settings in <b>package.json</b> and reading them in code. Each UI element (Status Bar, inline annotations, Activity Bar icon) is controlled by a separate boolean flag. Note: <b>showActivityBarIcon</b> is off by default — the Activity Bar icon appears only at the user\'s request.'))

    add(sp(6))

    add(h2('Progress API: Unobtrusive Progress'))
    add(p('For long operations, use the right location for progress:'))
    add(sp(3))
    add(tblh(['Progress type', 'When to use']))
    add(tbl2([
        ('ProgressLocation.SourceControl', 'SCM operations (git operations)'),
        ('ProgressLocation.Window',        'Global background operations in Status Bar — minimally intrusive'),
        ('ProgressLocation.Notification',  'Long operations requiring attention; with a cancel button'),
    ]))
    add(sp(3))
    add(code([
        '// OK: Background operation — Window (Status Bar) instead of Notification',
        'await vscode.window.withProgress(',
        '    {',
        '        location: vscode.ProgressLocation.Window,',
        '        title: \'$(sync~spin) Indexing...\',',
        '    },',
        '    async () => {',
        '        await buildIndex();',
        '    }',
        ');',
        '',
        '// OK: Long operation with cancellation — Notification',
        'await vscode.window.withProgress(',
        '    {',
        '        location: vscode.ProgressLocation.Notification,',
        '        title: \'Project Analysis\',',
        '        cancellable: true,',
        '    },',
        '    async (progress, token) => {',
        '        const files = await getFiles();',
        '        for (let i = 0; i < files.length; i++) {',
        '            if (token.isCancellationRequested) break;',
        '            progress.report({',
        '                increment: 100 / files.length,',
        '                message: `${i + 1} / ${files.length}: ${files[i]}`',
        '            });',
        '            await analyzeFile(files[i]);',
        '        }',
        '    }',
        ');',
    ]))
    add(sp(3))
    add(p('<b>window.withProgress()</b> shows a progress indicator without blocking the UI. <b>ProgressLocation.Notification</b> — a notification with a progress bar; <b>ProgressLocation.Window</b> — a quiet indicator in the Status Bar. <b>cancellable: true</b> adds a Cancel button and a CancellationToken to the callback.'))
    add(sp(6))

    # -- 5. UI ELEMENTS ----------------------------------------------------------
    add(h1('Each UI Element: Rules and Anti-Patterns'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Activity Bar — Strict Rules'))
    add(p('The Activity Bar is the most "expensive" location. Official Microsoft rules:'))
    add(sp(2))
    for good in [
        'Add an icon only if the extension provides a set of permanently accessible Views',
        'Icon: SVG 16x16 or 24x24, monochrome (single color) — VS Code applies the theme color itself',
        'Hide the Activity Bar icon if the extension is inactive (no files of the target type)',
        'Make the icon toggleable via a setting',
    ]:
        add(bul(f'<b>OK</b> {good}'))
    for bad in [
        'Don\'t add an icon for an extension with only one or two commands',
        'Don\'t use multi-color icons — they clash with the VS Code design',
        'Don\'t show an empty View without Welcome Content',
    ]:
        add(bul(f'<b>NO</b> {bad}', 2))
    add(sp(3))
    add(box('Why SVG and why monochrome?',
        'The VS Code Activity Bar colors icons dynamically: inactive ones get a muted color, '
        'active ones get an accent color (usually white or the theme color). '
        'This only works if the icon is monochrome (fill="currentColor" in SVG). '
        'If you use a multi-color PNG — the color dynamics break and the icon looks foreign. '
        'SVG also scales on HiDPI screens without pixelation. '
        'Custom SVG: in the "icon" field specify the file path — '
        '"viewsContainers": { "activitybar": [{ "icon": "./icons/my-icon.svg" }] }.',
        'note'))
    add(sp(6))

    add(h2('Status Bar — Rules and Priorities'))
    add(p('The Status Bar has a priority system. Higher number = further left (for the left side):'))
    add(sp(3))
    add(code([
        '// Built-in VS Code priorities (for reference):',
        '// Python: 100 (language + interpreter)',
        '// GitLens: 50-70 (branch, blame)',
        '// ESLint: 1 (status)',
        '',
        '// Recommendation: use priorities 0-20 for single items',
        'const item = vscode.window.createStatusBarItem(',
        '    vscode.StatusBarAlignment.Right,',
        '    10  // priority',
        ');',
        '',
        '// Status Bar colors — use ThemeColor, not hex',
        '// ThemeColor automatically changes when the user switches themes',
        '// Full token reference: code.visualstudio.com/api/references/theme-color',
        'item.color = new vscode.ThemeColor(\'statusBar.foreground\');',
        '',
        '// For errors/warnings (Status Bar Item only)',
        'item.backgroundColor = new vscode.ThemeColor(\'statusBarItem.errorBackground\');',
        '// or',
        'item.backgroundColor = new vscode.ThemeColor(\'statusBarItem.warningBackground\');',
        '',
        '// Short text + icon: best format',
        'item.text = \'$(check) 0 errors\';     // OK:',
        '// item.text = \'My Extension Active\'; // BAD: too long',
    ]))
    add(sp(3))
    add(p('Creating a Status Bar item with priority and styling. The priority (number at creation) determines position: for single extensions, 0-20 is recommended. Colors are set via <b>ThemeColor</b> — they automatically adapt to the theme. For error indication — special tokens <b>statusBarItem.errorBackground</b> and <b>warningBackground</b>.'))

    add(sp(6))

    add(h2('Editor Toolbar — Icons in the Tab Header'))
    add(screenshot('editor-toolbar.png', 'Editor Toolbar: context menu of the tab with extension commands'))
    add(sp(3))
    add(p('<b>Editor Toolbar</b> is the row of icon buttons in the <b>right side of the active tab header</b> '
          'of the editor (not to be confused with the Activity Bar on the left or the Title Bar at the top). '
          'By default, standard VS Code buttons are there: '
          'Split Editor, Open Changes (show diff), '
          'More Actions (...). '
          'Extensions add their buttons via <b>"editor/title"</b> in the menus section '
          'of package.json. '
          '<b>What to use it for:</b> the primary action on the current file — run code, '
          'open preview, publish, format. This is the "main button" for your language. '
          'Examples from real extensions: the Run button in the Python extension, '
          'the Preview button in the Markdown extension, the Test button in test runners.'))
    add(sp(3))
    add(box('Editor Toolbar vs Status Bar',
        'Editor Toolbar — for actions on a specific file (contextual). '
        'Status Bar — for information about the entire environment (global). '
        '"Run Python File" button -> Editor Toolbar. '
        '"Python 3.11" indicator -> Status Bar.', 'tip'))
    add(sp(3))
    add(code([
        '// package.json — button appears only for Go files in the tab header',
        '"contributes": {',
        '  "menus": {',
        '    "editor/title": [{',
        '      "command": "myGoExt.runFile",',
        '      // when: condition — otherwise the button is visible for ALL files',
        '      "when": "resourceLangId == go && !isInDiffEditor",',
        '      "group": "navigation"  // navigation = icon visible immediately; 1_run = in ... menu',
        '    }]',
        '  },',
        '  "commands": [{',
        '    "command": "myGoExt.runFile",',
        '    "title": "Run Go File",',
        '    "icon": "$(play)"  // icon is required for editor/title',
        '  }]',
        '}',
        '"contributes": {',
        '  "menus": {',
        '    "editor/title": [{',
        '      "command": "myExt.runCurrentFile",',
        '      // Only for your language AND only when not a diff editor',
        '      "when": "resourceLangId == mylang && !isInDiffEditor",',
        '      "group": "navigation"',
        '    }]',
        '  }',
        '}',
        '',
        '// Icons: use built-in Codicons',
        '"contributes": {',
        '  "commands": [{',
        '    "command": "myExt.runCurrentFile",',
        '    "title": "Run File",',
        '    "icon": "$(play)"  // $(play), $(debug), $(sync), $(check)...',
        '  }]',
        '}',
    ]))
    add(sp(3))
    add(p('Registering a button in the Editor Toolbar via <b>editor/title</b> in the menus section. Key points: the <b>when</b> condition restricts the button to a specific language, <b>group: "navigation"</b> makes the icon immediately visible (not hidden in the "..." menu), and <b>icon: "$(play)"</b> in the command declaration sets the icon via Codicon.'))

    add(sp(4))
    add(box('Codicons — Built-in VS Code Icons',
        'VS Code contains over 600 built-in icons (Codicons). '
        'Use $(icon-name) instead of your own SVGs — they automatically '
        'adapt to the theme. Full list: code.visualstudio.com/api/references/icons-in-labels', 'tip'))
    add(sp(6))

    add(h2('Context Menu — Group Hierarchy'))
    add(p('Context menus have a group system. '
          'Item order within a group is controlled via @N:'))
    add(sp(3))
    add(code([
        '// Standard editor groups (in display order):',
        '// navigation   — go to definition, references',
        '// 1_modification — insert, format',
        '// 9_cutcopypaste — cut, copy, paste',
        '// z_commands    — miscellaneous commands',
        '',
        '"editor/context": [{',
        '  "command": "myExt.extractFunction",',
        '  "when": "editorHasSelection && resourceLangId == typescript",',
        '  "group": "1_modification@5"  // within group — position @5',
        '}]',
        '',
        '// Separators between groups are created automatically',
        '// Your commands in one group are not separated from others',
        '',
        '// Explorer context menu groups:',
        '// navigation  — open, go to',
        '// 2_workspace — add to workspace',
        '// 3_compare   — compare',
        '// 5_cutcopypaste',
        '// 7_modification — create, rename, delete',
    ]))
    add(sp(3))
    add(p('Context menu group system: <b>group</b> determines the section (navigation, 1_modification, etc.), and the <b>@N</b> suffix determines position within the section. VS Code automatically adds separators between groups. The editor and Explorer have their own sets of standard groups — it is important to place commands in the right section.'))

    add(sp(6))

    # -- 6. WEBVIEW UX -----------------------------------------------------------
    add(h1('Webview: CSS Tokens and Ecosystem Integration'))
    add(hl(C['blue']))
    add(sp(6))

    add(p('This topic is covered in detail in Chapter 7 (Webview API) and Appendix D '
          '(Theme CSS Variables). Here — only the UX principles.'))
    add(sp(3))

    add(h2('Webview Must "Feel" Like VS Code'))
    add(p('The biggest mistake of Webview extensions is that they look like a third-party website inside VS Code. '
          'Use theme CSS variables so the Webview automatically adapts '
          'to any user theme (Dark, Light, High Contrast, custom). '
          'Full list of variables — <a href="#appendix_D"><b>Appendix D</b></a> at the end of the book.'))
    add(sp(3))
    add(code([
        '/* Minimal Webview CSS — body uses VS Code theme colors */',
        'body {',
        '    background-color: var(--vscode-editor-background);',
        '    color: var(--vscode-editor-foreground);',
        '    font-family: var(--vscode-font-family);',
        '    font-size: var(--vscode-font-size);',
        '    /* Webview adds class vscode-dark / vscode-light to body */',
        '}',
        '',
        'button {',
        '    background-color: var(--vscode-button-background);',
        '    color: var(--vscode-button-foreground);',
        '    border: 1px solid var(--vscode-button-border, transparent);',
        '}',
        'button:hover { background-color: var(--vscode-button-hoverBackground); }',
        '',
        'input, select {',
        '    background-color: var(--vscode-input-background);',
        '    color: var(--vscode-input-foreground);',
        '    border: 1px solid var(--vscode-input-border);',
        '}',
        '',
        'a { color: var(--vscode-textLink-foreground); }',
        'code, pre {',
        '    background-color: var(--vscode-textCodeBlock-background);',
        '    font-family: var(--vscode-editor-font-family);',
        '}',
    ]))
    add(sp(3))
    add(p('CSS variables <b>--vscode-*</b> update automatically when the theme changes. Use them instead of hard-coded hex colors — otherwise the Webview will break in light, High Contrast, or custom themes. VS Code adds the class <b>vscode-dark</b>/<b>vscode-light</b> to <body>.'))
    add(sp(3))
    add(p('<b>Why var() instead of hard-coded colors:</b> VS Code has Light, Dark, '
          'High Contrast themes, and thousands of user themes. '
          'CSS variables update instantly when the theme changes without reloading the Webview. '
          'On vscode.dev, themes change dynamically — without var() this will break.'))
    add(sp(4))
    add(sp(4))

    add(h3('Real-Time Theme Change Support'))
    add(code([
        '// In Webview JavaScript — react to theme changes',
        'const vscode = acquireVsCodeApi();',
        '',
        '// Listen for theme changes',
        'window.addEventListener(\'message\', event => {',
        '    const { command, theme } = event.data;',
        '    if (command === \'themeChanged\') {',
        '        document.body.className = `vscode-${theme}`;',
        '        updateCharts(); // redraw charts',
        '    }',
        '});',
        '',
        '// In the extension — notify Webview of theme change',
        'vscode.window.onDidChangeActiveColorTheme(theme => {',
        '    panel.webview.postMessage({',
        '        command: \'themeChanged\',',
        '        theme: theme.kind === vscode.ColorThemeKind.Dark ? \'dark\' : \'light\'',
        '    });',
        '}, null, context.subscriptions);',
    ]))
    add(sp(3))
    add(p('Two-way theme change handling: on the extension side, <b>onDidChangeActiveColorTheme</b> detects the switch and sends a message to the Webview via <b>postMessage</b>, and JavaScript inside the Webview listens for the message event and updates the CSS class on body — this is needed for elements that don\'t update automatically via CSS variables (e.g., canvas charts).'))

    add(sp(6))

    add(h2('Saving Webview State'))
    add(p('A Webview is hidden when switching tabs and may be destroyed to save memory. '
          'Always save state:'))
    add(sp(3))
    add(code([
        '// In Webview JavaScript',
        'const vscode = acquireVsCodeApi();',
        '',
        '// Restore saved state',
        'const prevState = vscode.getState() || { scrollY: 0, selectedTab: 0 };',
        'window.scrollTo(0, prevState.scrollY);',
        'selectTab(prevState.selectedTab);',
        '',
        '// Save on every change',
        'function saveState() {',
        '    vscode.setState({',
        '        scrollY: window.scrollY,',
        '        selectedTab: activeTabIndex,',
        '    });',
        '}',
        '',
        '// In the extension — enable persistence',
        'vscode.window.createWebviewPanel(\'myView\', \'My View\', col, {',
        '    retainContextWhenHidden: true,  // DON\'T destroy when hidden',
        '    // But this is expensive on memory! Use only when necessary.',
        '});',
    ]))
    add(sp(3))
    add(p('Two approaches to saving Webview state. Lightweight: <b>vscode.getState()</b> / <b>setState()</b> serialize data (scroll, selected tab) and restore it on re-display. Heavyweight: <b>retainContextWhenHidden</b> preserves the entire DOM and JavaScript context — convenient, but the Webview consumes memory even when hidden.'))

    add(sp(4))
    add(box('retainContextWhenHidden — an Expensive Option',
        'retainContextWhenHidden preserves the DOM and JS state when the Webview is hidden. '
        'This is convenient but consumes memory — the Webview uses resources even when invisible. '
        'Use only for heavy editors. '
        'For simple cases — vscode.setState()/getState() is sufficient.', 'warn'))
    add(sp(6))

    # -- 7. SETTINGS --------------------------------------------------------------
    add(h1('Settings: Usability and Documentation'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Anatomy of a Good Settings Section'))
    add(p('Settings are the primary way of communicating with the user. '
          'Good settings explain what the extension does and give full control:'))
    add(sp(3))
    add(code([
        '"contributes": {',
        '  "configuration": {',
        '    "title": "My Extension",  // Displayed as section header',
        '    "order": 10,              // Order in Settings UI (lower = higher)',
        '    "properties": {',
        '',
        '      // Each setting with full description',
        '      "myExt.enable": {',
        '        "type": "boolean",',
        '        "default": true,',
        '        "markdownDescription":',
        '          "Enable My Extension. Disable if you experience performance issues.",',
        '        "order": 1  // Order within section',
        '      },',
        '',
        '      // Enum with descriptions for each value',
        '      "myExt.verbosity": {',
        '        "type": "string",',
        '        "enum": ["silent", "normal", "verbose"],',
        '        "enumDescriptions": [',
        '          "No output to Output Channel",',
        '          "Important messages only (recommended)",',
        '          "All messages (for debugging)"',
        '        ],',
        '        "default": "normal",',
        '        "description": "Logging level",',
        '        "order": 2',
        '      },',
        '',
        '      // Setting with an example in the description',
        '      "myExt.excludePatterns": {',
        '        "type": "array",',
        '        "items": { "type": "string" },',
        '        "default": ["**/node_modules/**", "**/.git/**"],',
        '        "markdownDescription":',
        '          "Glob patterns for files that are **not** processed.\\n\\n" +',
        '          "Example: `[\\\"**/test/**\\\", \\\"**/*.spec.ts\\\"]`",',
        '        "order": 3',
        '      },',
        '',
        '      // Setting with reload warning',
        '      "myExt.serverPort": {',
        '        "type": "number",',
        '        "default": 9000,',
        '        "description": "LSP server port. Requires window reload.",',
        '        "scope": "window"  // machine | window | resource | language-overridable',
        '      }',
        '    }',
        '  }',
        '}',
    ]))
    add(sp(3))
    add(p('Full anatomy of a settings section: <b>title</b> and <b>order</b> control display in the Settings UI. Each property has <b>type</b>, <b>default</b>, and a description. For enum values, <b>enumDescriptions</b> explains each option. The <b>markdownDescription</b> field supports formatting and examples. The <b>scope</b> attribute determines the setting\'s level of application (machine, window, resource).'))

    add(sp(4))

    add(h3('Setting Scope'))
    add(tblh(['Scope', 'Description']))
    add(tbl2([
        ('machine',               'Tied to the machine. Not synced between devices. For paths to binaries'),
        ('window',                'At the VS Code window level. Default for most settings'),
        ('resource',              'At the file level. Different values for different files'),
        ('language-overridable',  'Can be overridden per language: "[typescript]": {...}'),
    ]))
    add(sp(6))

    add(h2('Workspace-Level Settings'))
    add(p('Let users set settings at the project level. '
          'This is critically important for teams with different configurations:'))
    add(sp(3))
    add(code([
        '// Read settings with document context',
        'function getEffectiveConfig(document: vscode.TextDocument) {',
        '    // getConfiguration with uri respects workspace-specific settings',
        '    const cfg = vscode.workspace.getConfiguration(\'myExt\', document.uri);',
        '    return {',
        '        enable: cfg.get<boolean>(\'enable\', true),',
        '        verbosity: cfg.get<string>(\'verbosity\', \'normal\'),',
        '    };',
        '}',
        '',
        '// User can override in the project\'s .vscode/settings.json:',
        '// {',
        '//   "myExt.verbosity": "verbose",  // only for this project',
        '//   "[typescript]": {',
        '//     "myExt.enable": false  // only for TypeScript files',
        '//   }',
        '// }',
    ]))
    add(sp(3))
    add(p('Reading settings with document context: <b>getConfiguration(section, uri)</b> with a URI returns values respecting workspace-specific overrides from <b>.vscode/settings.json</b>. This lets users set different settings for different projects and even for different languages via <b>[typescript]</b> sections.'))

    add(sp(6))

    # -- REAL EXAMPLES ------------------------------------------------------------
    add(h1('Real Examples: Good and Bad'))
    add(hl(C['blue']))
    add(sp(4))

    add(h2('Quality Standards'))
    add(p('These extensions are often cited as benchmarks — not only for functionality, '
          'but specifically for UX quality and adherence to VS Code principles:'))
    add(sp(3))
    add(tblh(['Extension', 'What it does right']))
    add(tbl2([
        ('GitLens\n(gitkraken/vscode-gitlens)',
         'Three visibility levels: inline blame (always), Status Bar (context), '
         'side panel (on demand). Everything toggleable via settings. '
         'Walkthrough on first launch instead of notifications. '
         'Activation time ~35ms despite massive functionality'),
        ('Prettier\n(prettier/prettier-vscode)',
         'The formatter doesn\'t impose itself — activates only when chosen as '
         'editor.defaultFormatter. Shows no notifications on activation. '
         'All errors go to Output Channel, not to popups'),
        ('ESLint\n(microsoft/vscode-eslint)',
         'Diagnostics only for files with .eslintrc in the project. '
         'Status Bar item shows state and disappears when not needed. '
         'Properly uses CancellationToken in all providers'),
        ('rust-analyzer',
         'Heavy LSP server (Rust compiler) is in a separate process. '
         'Progress in Status Bar during indexing — does not block the editor. '
         'Typing response time stays <16ms'),
    ]))
    add(sp(6))

    add(h2('Anti-Examples and Common Mistakes'))
    add(p('Specific patterns that regularly generate complaints in Marketplace reviews:'))
    add(sp(3))
    add(tblh(['Problem', 'What happens']))
    add(tbl2([
        ('activationEvents: ["*"] for a non-language extension',
         'Extension loads on every VS Code startup. '
         'For users with 20+ extensions this is hundreds of ms added to startup. '
         'Example: Beautify (5.4M installs) activated with "*" — '
         'many users switched to Prettier precisely because of this'),
        ('2513ms activation time (real case)',
         'Extension with activationEvents:["*"] and 2.5 seconds activation time. '
         'This was documented in a public extension performance analysis. '
         'Such extensions get 1-star reviews: "VS Code became slow"'),
        ('Notification on every VS Code startup',
         '"Please rate this extension!" on every startup. '
         'Real example: an extension with 4.7M installs dropped from 4.2 to 3.1 stars '
         'in 3 months due to intrusive notifications. After removing them — returned to 4.4'),
        ('Data collection without explicit consent',
         'In 2025, Microsoft removed several popular extensions from the Marketplace '
         'for collecting user data without explicit consent. '
         'Extensions were used by millions of developers and were removed without warning. '
         'Always respect isTelemetryEnabled and request explicit permission'),
        ('globalState for workspace-specific data',
         'Extension saves project settings in globalState instead of workspaceState. '
         'Configuration from one project "leaks" into another. '
         'Users cannot understand why the extension behaves strangely'),
    ]))
    add(sp(4))
    add(box('How to Test Your Extension',
        'Developer: Show Running Extensions — activation time of every extension. '
        'Target: < 100ms — excellent, < 300ms — good, > 500ms — needs optimization. '
        'Developer: Startup Performance — detailed VS Code startup profile. '
        'Source: nicoespeon.com/en/2019/11/fix-vscode-extension-performance-issue/',
        'tip'))
    add(sp(6))

    # -- 8. FINAL PRINCIPLES -----------------------------------------------------
    add(h1('Checklist: Extension as a Good Citizen'))
    add(hl(C['blue']))
    add(sp(6))

    add(h2('Principles of an Unobtrusive Extension'))
    add(p('Before publishing, check every item on this list:'))
    add(sp(3))

    add(h3('Visibility and Discoverability'))
    for item in [
        'Walkthrough for onboarding — instead of a notification on first launch',
        'Welcome View for empty Tree View states with links to documentation',
        'Commands named with a category: "My Extension: ..."',
        'Key features accessible from the Command Palette',
        'Contextual buttons hidden via "when" for irrelevant files',
        'Status Bar item hidden via hide() for inactive files',
        'Contextual hints (at the right moment, not at startup)',
    ]:
        add(bul(item))
    add(sp(4))

    add(h3('Unobtrusiveness'))
    for item in [
        'No notifications on extension activation',
        'No automatic notifications without explicit user action',
        'All repeating notifications have "Don\'t Show Again"',
        'All features toggleable via settings',
        'Activity Bar icon: off by default OR added only when truly needed',
        'Maximum 1-2 Status Bar items',
    ]:
        add(bul(item))
    add(sp(4))

    add(h3('Coexistence with Other Extensions'))
    for item in [
        'Document Selector is precise: specific language, not "*"',
        'Keybindings: rare combinations with "when" context',
        'Formatter respects editor.defaultFormatter',
        'Checks for conflicting extensions (when necessary)',
        'Diagnostics collection is uniquely named',
        'extensionDependencies declared in package.json',
        'Does not override others\' Language IDs',
    ]:
        add(bul(item))
    add(sp(4))

    add(h3('UI Quality'))
    for item in [
        'Webview uses VS Code theme CSS variables',
        'Webview saves state via vscode.setState()',
        'Icons — built-in Codicons ($(icon-name))',
        'Monochrome SVG icons for Activity Bar',
        'Settings have descriptions and examples',
        'Setting scope chosen correctly (machine/window/resource)',
        'Theme change support in Webview',
    ]:
        add(bul(item))

    return A


if __name__ == '__main__':
    print(f'UX part has {len(build_story_ux())} elements')
