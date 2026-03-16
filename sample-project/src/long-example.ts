import * as vscode from 'vscode';

// ─── Configuration ──────────────────────────────────────────────────────────

interface ExtensionConfig {
  enableDiagnostics: boolean;
  maxFileSize: number;
  excludePatterns: string[];
  outputChannel: string;
}

function loadConfig(): ExtensionConfig {
  const config = vscode.workspace.getConfiguration('myExtension');
  return {
    enableDiagnostics: config.get<boolean>('enableDiagnostics', true),
    maxFileSize: config.get<number>('maxFileSize', 1_000_000),
    excludePatterns: config.get<string[]>('excludePatterns', ['**/node_modules/**']),
    outputChannel: config.get<string>('outputChannel', 'My Extension'),
  };
}

// ─── Diagnostics Provider ───────────────────────────────────────────────────

class DiagnosticsProvider implements vscode.Disposable {
  private collection: vscode.DiagnosticCollection;
  private disposables: vscode.Disposable[] = [];

  constructor() {
    this.collection = vscode.languages.createDiagnosticCollection('myExtension');

    this.disposables.push(
      vscode.workspace.onDidSaveTextDocument((doc) => this.analyzeDocument(doc)),
      vscode.workspace.onDidOpenTextDocument((doc) => this.analyzeDocument(doc)),
    );
  }

  private analyzeDocument(document: vscode.TextDocument): void {
    if (document.languageId !== 'typescript') {
      return;
    }

    const diagnostics: vscode.Diagnostic[] = [];
    const text = document.getText();
    const lines = text.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Flag console.log statements as warnings
      const consoleMatch = line.match(/console\.(log|warn|error)\(/);
      if (consoleMatch) {
        const startChar = line.indexOf(consoleMatch[0]);
        const range = new vscode.Range(i, startChar, i, startChar + consoleMatch[0].length);
        diagnostics.push(
          new vscode.Diagnostic(range, 'Avoid console statements in production code', vscode.DiagnosticSeverity.Warning),
        );
      }

      // Flag TODO comments as information
      if (line.includes('TODO')) {
        const startChar = line.indexOf('TODO');
        const range = new vscode.Range(i, startChar, i, startChar + 4);
        diagnostics.push(
          new vscode.Diagnostic(range, 'Unresolved TODO comment', vscode.DiagnosticSeverity.Information),
        );
      }
    }

    this.collection.set(document.uri, diagnostics);
  }

  dispose(): void {
    this.collection.dispose();
    this.disposables.forEach((d) => d.dispose());
  }
}

// ─── Status Bar ─────────────────────────────────────────────────────────────

function createStatusBarItem(context: vscode.ExtensionContext): vscode.StatusBarItem {
  const item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  item.text = '$(check) My Extension';
  item.tooltip = 'Extension is active';
  item.command = 'myExtension.showStatus';
  item.show();
  context.subscriptions.push(item);
  return item;
}

// ─── Activation ─────────────────────────────────────────────────────────────

export function activate(context: vscode.ExtensionContext): void {
  const config = loadConfig();
  const output = vscode.window.createOutputChannel(config.outputChannel);

  output.appendLine('Extension activated');

  const provider = new DiagnosticsProvider();
  context.subscriptions.push(provider);

  const statusItem = createStatusBarItem(context);

  context.subscriptions.push(
    vscode.commands.registerCommand('myExtension.showStatus', () => {
      vscode.window.showInformationMessage(`Diagnostics: ${config.enableDiagnostics ? 'ON' : 'OFF'}`);
    }),
  );

  // Watch for configuration changes
  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('myExtension')) {
        const updated = loadConfig();
        statusItem.text = updated.enableDiagnostics ? '$(check) My Extension' : '$(x) My Extension';
        output.appendLine('Configuration updated');
      }
    }),
  );
}

export function deactivate(): void {
  // cleanup handled by disposables
}
