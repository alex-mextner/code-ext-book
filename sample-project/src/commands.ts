import * as vscode from 'vscode';

export function registerCommands(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('myExtension.openSettings', () => {
      vscode.commands.executeCommand('workbench.action.openSettings');
    })
  );
}
