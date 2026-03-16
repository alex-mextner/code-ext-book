import * as vscode from 'vscode';

export class BookmarkTreeProvider implements vscode.TreeDataProvider<string> {
  getTreeItem(element: string): vscode.TreeItem {
    return new vscode.TreeItem(element, vscode.TreeItemCollapsibleState.None);
  }

  getChildren(): string[] {
    return ['Chapter 1', 'Chapter 2', 'Chapter 3'];
  }
}
