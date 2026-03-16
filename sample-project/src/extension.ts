import * as vscode from 'vscode';

class DependencyItem extends vscode.TreeItem {
  constructor(
    public readonly name: string,
    public readonly version: string,
    public readonly description: string,
    public readonly isDevDep: boolean
  ) {
    super(name, vscode.TreeItemCollapsibleState.None);
    this.description = version;
    this.iconPath = new vscode.ThemeIcon(isDevDep ? 'tools' : 'package');
    this.contextValue = isDevDep ? 'devDependency' : 'dependency';

    // MarkdownString tooltip (VS Code 1.106+)
    const md = new vscode.MarkdownString();
    md.appendMarkdown(`**${name}** \`v${version}\`\n\n`);
    md.appendMarkdown(`${description}\n\n`);
    md.appendMarkdown(`Type: *${isDevDep ? 'devDependency' : 'dependency'}*\n\n`);
    md.appendCodeblock(`npm install ${isDevDep ? '-D ' : ''}${name}@${version}`, 'bash');
    md.supportHtml = true;
    this.tooltip = md;
  }
}

class DependenciesProvider implements vscode.TreeDataProvider<DependencyItem> {
  getTreeItem(element: DependencyItem): vscode.TreeItem {
    return element;
  }

  getChildren(): DependencyItem[] {
    return [
      new DependencyItem('express', '4.18.2', 'Fast, unopinionated web framework', false),
      new DependencyItem('lodash', '4.17.21', 'Utility library delivering consistency', false),
      new DependencyItem('axios', '1.6.0', 'Promise based HTTP client', false),
      new DependencyItem('typescript', '5.3.3', 'TypeScript language compiler', true),
      new DependencyItem('@types/node', '20.10.0', 'Type definitions for Node.js', true),
      new DependencyItem('esbuild', '0.19.8', 'Extremely fast JavaScript bundler', true),
    ];
  }
}

export function activate(context: vscode.ExtensionContext) {
  const provider = new DependenciesProvider();
  const treeView = vscode.window.createTreeView('myExt.dependencies', {
    treeDataProvider: provider,
    showCollapseAll: true,
  });

  const disposable = vscode.commands.registerCommand(
    'myExtension.helloWorld',
    () => {
      vscode.window.showInformationMessage('Hello from My First Extension!');
    }
  );

  context.subscriptions.push(treeView, disposable);
}

export function deactivate() {}
