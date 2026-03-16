/**
 * VS Code Screenshot Tool for the book "Building VS Code Extensions"
 *
 * Launches VS Code via Playwright Electron API and captures cropped
 * screenshots of various UI elements.
 *
 * Usage:
 *   npx tsx take-screenshots.ts
 *   DEBUG=1 npx tsx take-screenshots.ts   # keeps VS Code open on failure
 */

import { _electron as electron, type ElectronApplication, type Page, type Locator } from 'playwright';
import path from 'node:path';
import os from 'node:os';
import fs from 'node:fs/promises';
import { randomUUID } from 'node:crypto';

// ─── Config ────────────────────────────────────────────────────────────────────

const VSCODE_PATH =
  process.env.VSCODE_PATH ||
  '/Applications/Visual Studio Code.app/Contents/MacOS/Electron';

const SCREENSHOTS_DIR = path.join(import.meta.dirname, 'screenshots');
const SAMPLE_PROJECT = path.join(import.meta.dirname, 'sample-project');
const DEBUG = !!process.env.DEBUG;

// ─── Helpers ───────────────────────────────────────────────────────────────────

function log(msg: string) {
  const ts = new Date().toISOString().slice(11, 19);
  console.log(`[${ts}] ${msg}`);
}

async function ensureDir(dir: string) {
  await fs.mkdir(dir, { recursive: true });
}

/**
 * Save a screenshot - either element-level (cropped) or full page.
 */
async function saveScreenshot(
  target: Page | Locator,
  name: string,
  opts?: { padding?: number }
) {
  const filePath = path.join(SCREENSHOTS_DIR, `${name}.png`);
  await target.screenshot({ path: filePath, animations: 'disabled' });
  const stat = await fs.stat(filePath);
  log(`  Saved: ${name}.png (${(stat.size / 1024).toFixed(0)} KB)`);
}

/**
 * Open the Command Palette via F1, type a query, wait for results.
 */
async function openCommandPalette(page: Page, query?: string) {
  await page.keyboard.press('F1');
  const input = page.locator('.quick-input-widget input');
  await input.waitFor({ state: 'visible', timeout: 5_000 });

  if (query) {
    // F1 opens with ">", fill replaces everything so re-add ">"
    await input.fill(`> ${query}`);
    await page.waitForTimeout(600);
  }
  return input;
}

/**
 * Run a named command through the Command Palette.
 */
async function runCommand(page: Page, command: string) {
  await openCommandPalette(page, command);
  await page.waitForTimeout(400);
  const firstRow = page.locator('.quick-input-list .monaco-list-row').first();
  await firstRow.waitFor({ state: 'visible', timeout: 5_000 });
  await firstRow.click();
  await page.waitForTimeout(300);
}

/**
 * Close whatever quick-input / dialog is open.
 */
async function dismissDialog(page: Page) {
  await page.keyboard.press('Escape');
  await page.waitForTimeout(200);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(200);
}

// ─── Launch VS Code ────────────────────────────────────────────────────────────

async function launchVSCode(): Promise<{
  app: ElectronApplication;
  page: Page;
  userDataDir: string;
}> {
  const userDataDir = path.join(os.tmpdir(), `book-screenshots-${randomUUID()}`);
  await ensureDir(userDataDir);

  // Write clean settings
  const settingsDir = path.join(userDataDir, 'User');
  await ensureDir(settingsDir);
  await fs.writeFile(
    path.join(settingsDir, 'settings.json'),
    JSON.stringify(
      {
        'telemetry.telemetryLevel': 'off',
        'update.mode': 'none',
        'extensions.autoUpdate': false,
        'window.titleBarStyle': 'custom',
        'workbench.startupEditor': 'none',
        'workbench.tips.enabled': false,
        'workbench.welcomePage.walkthroughs.openOnInstall': false,
        'workbench.colorTheme': 'Default Dark Modern',
        'editor.fontSize': 14,
        'editor.minimap.enabled': true,
        'breadcrumbs.enabled': true,
      },
      null,
      2
    )
  );

  log('Launching VS Code...');
  const app = await electron.launch({
    executablePath: VSCODE_PATH,
    args: [
      `--extensionDevelopmentPath=${SAMPLE_PROJECT}`,
      '--disable-extensions',  // disable other extensions, our dev extension still loads
      '--skip-release-notes',
      '--skip-welcome',
      '--disable-workspace-trust',
      '--disable-telemetry',
      `--user-data-dir=${userDataDir}`,
      SAMPLE_PROJECT,
    ],
    env: {
      ...process.env,
      VSCODE_SKIP_PRELAUNCH: '1',
    },
    timeout: 60_000,
  });

  const page = await app.firstWindow();
  await page.waitForLoadState('domcontentloaded');
  log('VS Code window ready, waiting for UI to stabilize...');

  // Wait for the workbench to be fully rendered
  await page.waitForSelector('.monaco-workbench', { timeout: 30_000 });
  await page.waitForTimeout(3_000);

  // Dismiss any startup notifications
  await dismissNotifications(page);

  return { app, page, userDataDir };
}

async function dismissNotifications(page: Page) {
  await page.waitForTimeout(1_000);

  const closeButtons = page.locator('.notifications-toasts .codicon-notifications-clear');
  const count = await closeButtons.count();
  for (let i = 0; i < count; i++) {
    await closeButtons.nth(i).click().catch(() => {});
  }

  const dismissAll = page.locator('.notifications-center .codicon-notifications-clear-all');
  if (await dismissAll.isVisible().catch(() => false)) {
    await dismissAll.click().catch(() => {});
  }
}

// ─── Screenshot Routines ───────────────────────────────────────────────────────

async function screenshotFullWindow(page: Page) {
  log('Taking full window screenshot...');
  await saveScreenshot(page, '00-full-window');
}

async function screenshotCommandPalette(page: Page) {
  log('Taking Command Palette screenshot...');

  await openCommandPalette(page);
  await page.waitForTimeout(500);

  // The quick-input widget is the Command Palette container
  const widget = page.locator('.quick-input-widget');
  await widget.waitFor({ state: 'visible', timeout: 5_000 });

  await saveScreenshot(widget, '01-command-palette');
  await dismissDialog(page);
}

async function screenshotCommandPaletteWithSearch(page: Page) {
  log('Taking Command Palette with search screenshot...');

  await openCommandPalette(page, 'theme');
  await page.waitForTimeout(800);

  const widget = page.locator('.quick-input-widget');
  await widget.waitFor({ state: 'visible', timeout: 5_000 });

  // Wait for list items to appear
  await page.locator('.quick-input-list .monaco-list-row').first().waitFor({
    state: 'visible',
    timeout: 5_000,
  });

  await saveScreenshot(widget, '02-command-palette-search');
  await dismissDialog(page);
}

async function screenshotStatusBar(page: Page) {
  log('Taking Status Bar screenshot...');

  const statusBar = page.locator('.part.statusbar');
  await statusBar.waitFor({ state: 'visible', timeout: 5_000 });

  await saveScreenshot(statusBar, '03-status-bar');
}

async function screenshotActivityBar(page: Page) {
  log('Taking Activity Bar screenshot...');

  const activityBar = page.locator('.part.activitybar');
  await activityBar.waitFor({ state: 'visible', timeout: 5_000 });

  await saveScreenshot(activityBar, '04-activity-bar');
}

async function screenshotExplorer(page: Page) {
  log('Taking Explorer / Tree View screenshot...');

  // Open Explorer via keyboard shortcut
  await page.keyboard.press('Meta+Shift+e');
  await page.waitForTimeout(1_500);

  // The sidebar contains the explorer
  const sidebar = page.locator('.part.sidebar');
  await sidebar.waitFor({ state: 'visible', timeout: 5_000 });

  // Try expanding files if the tree is collapsed
  const treeRows = page.locator('.explorer-folders-view .monaco-list-row');
  if ((await treeRows.count()) > 0) {
    // Click first item to make sure tree is focused
    await treeRows.first().click().catch(() => {});
    await page.waitForTimeout(300);
  }

  await saveScreenshot(sidebar, '05-explorer-sidebar');
}

async function screenshotSettings(page: Page) {
  log('Taking Settings UI screenshot...');

  // Open settings via command
  await runCommand(page, 'Preferences: Open Settings (UI)');
  await page.waitForTimeout(2_000);

  // Settings has a specific container
  const settingsEditor = page.locator('.settings-editor');

  if (await settingsEditor.isVisible().catch(() => false)) {
    await saveScreenshot(settingsEditor, '06-settings-ui');
  } else {
    // Fallback: screenshot the whole editor area
    const editorArea = page.locator('.part.editor');
    await editorArea.waitFor({ state: 'visible', timeout: 5_000 });
    await saveScreenshot(editorArea, '06-settings-ui');
  }

  // Close settings tab
  await page.keyboard.press('Meta+w');
  await page.waitForTimeout(300);
}

async function screenshotQuickPick(page: Page) {
  log('Taking Quick Pick screenshot...');

  // "Change Language Mode" gives a nice quick pick list
  await openCommandPalette(page, 'Change Language Mode');
  await page.waitForTimeout(500);

  const firstRow = page.locator('.quick-input-list .monaco-list-row').first();
  await firstRow.waitFor({ state: 'visible', timeout: 5_000 });
  await firstRow.click();
  await page.waitForTimeout(800);

  // Now the language picker quick pick should be open
  const widget = page.locator('.quick-input-widget');
  if (await widget.isVisible().catch(() => false)) {
    // Wait for list to populate
    await page.locator('.quick-input-list .monaco-list-row').first().waitFor({
      state: 'visible',
      timeout: 5_000,
    }).catch(() => {});
    await page.waitForTimeout(300);

    await saveScreenshot(widget, '07-quick-pick');
  }

  await dismissDialog(page);
}

async function screenshotNotification(page: Page) {
  log('Taking Notification screenshot...');

  // Trigger an info notification via the command palette
  // "Show Release Notes" or "Developer: Show Running Extensions" won't always show a notification
  // Instead, use the notification via running a command that shows one
  await openCommandPalette(page, 'Notifications: Show Notifications');
  await page.waitForTimeout(500);

  const firstRow = page.locator('.quick-input-list .monaco-list-row').first();
  if (await firstRow.isVisible().catch(() => false)) {
    await firstRow.click();
    await page.waitForTimeout(1_000);
  }

  // Try to capture the notification center
  const notifCenter = page.locator('.notifications-center');
  if (await notifCenter.isVisible().catch(() => false)) {
    await saveScreenshot(notifCenter, '08-notification-center');
  } else {
    // Fallback: take full page, notification might be a toast
    log('  Notification center not visible, taking full page...');
    await saveScreenshot(page, '08-notification-fallback');
  }

  await dismissDialog(page);
}

async function screenshotEditorWithFile(page: Page) {
  log('Taking Editor with open file screenshot...');

  // Open extension.ts via quick open
  await page.keyboard.press('Meta+p');
  await page.waitForTimeout(500);

  const quickOpen = page.locator('.quick-input-widget input');
  await quickOpen.waitFor({ state: 'visible', timeout: 5_000 });
  await quickOpen.fill('extension.ts');
  await page.waitForTimeout(800);

  const firstRow = page.locator('.quick-input-list .monaco-list-row').first();
  if (await firstRow.isVisible().catch(() => false)) {
    await firstRow.click();
    await page.waitForTimeout(1_500);
  } else {
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1_500);
  }

  // Screenshot the editor area
  const editorArea = page.locator('.part.editor');
  await editorArea.waitFor({ state: 'visible', timeout: 5_000 });
  await saveScreenshot(editorArea, '09-editor-with-file');
}

async function screenshotTitleBar(page: Page) {
  log('Taking Title Bar screenshot...');

  const titleBar = page.locator('.part.titlebar');
  if (await titleBar.isVisible().catch(() => false)) {
    await saveScreenshot(titleBar, '10-title-bar');
  } else {
    log('  Title bar not visible (native title bar), skipping.');
  }
}

async function screenshotPanel(page: Page) {
  log('Taking Panel (Terminal/Problems) screenshot...');

  // Open terminal panel
  await page.keyboard.press('Meta+j');
  await page.waitForTimeout(1_500);

  const panel = page.locator('.part.panel');
  if (await panel.isVisible().catch(() => false)) {
    await saveScreenshot(panel, '11-panel-terminal');
  } else {
    log('  Panel not visible, skipping.');
  }

  // Close panel
  await page.keyboard.press('Meta+j');
  await page.waitForTimeout(300);
}

async function screenshotColorThemePicker(page: Page) {
  log('Taking Color Theme Picker screenshot...');

  await openCommandPalette(page, 'Preferences: Color Theme');
  await page.waitForTimeout(500);

  const firstRow = page.locator('.quick-input-list .monaco-list-row').first();
  await firstRow.waitFor({ state: 'visible', timeout: 5_000 });
  await firstRow.click();
  await page.waitForTimeout(1_000);

  const widget = page.locator('.quick-input-widget');
  if (await widget.isVisible().catch(() => false)) {
    await page.locator('.quick-input-list .monaco-list-row').first().waitFor({
      state: 'visible',
      timeout: 5_000,
    }).catch(() => {});
    await page.waitForTimeout(300);

    await saveScreenshot(widget, '12-color-theme-picker');
  }

  await dismissDialog(page);
}

async function screenshotProblemsPanel(page: Page) {
  log('Taking Problems Panel screenshot...');

  // Open Problems panel via Ctrl+Shift+M (on Mac: Cmd+Shift+M)
  await page.keyboard.press('Meta+Shift+m');
  await page.waitForTimeout(1_500);

  // Make sure we're on the Problems tab (click it if visible)
  const problemsTab = page.locator('.panel .action-label:has-text("Problems")');
  if (await problemsTab.isVisible().catch(() => false)) {
    await problemsTab.click();
    await page.waitForTimeout(500);
  }

  const panel = page.locator('.part.panel');
  if (await panel.isVisible().catch(() => false)) {
    await saveScreenshot(panel, '13-problems-panel');
  } else {
    log('  Problems panel not visible, skipping.');
  }

  // Close the panel
  await page.keyboard.press('Meta+Shift+m');
  await page.waitForTimeout(300);
}

async function screenshotExtensionsView(page: Page) {
  log('Taking Extensions View screenshot...');

  // Open Extensions sidebar via Cmd+Shift+X
  await page.keyboard.press('Meta+Shift+x');
  await page.waitForTimeout(2_000);

  const sidebar = page.locator('.part.sidebar');
  await sidebar.waitFor({ state: 'visible', timeout: 5_000 });

  // Wait for extensions list to load
  await page.waitForTimeout(2_000);

  await saveScreenshot(sidebar, '14-extensions-view');

  // Switch back to Explorer
  await page.keyboard.press('Meta+Shift+e');
  await page.waitForTimeout(500);
}

async function screenshotEditorMultipleTabs(page: Page) {
  log('Taking Editor with multiple tabs screenshot...');

  // Open extension.ts
  await page.keyboard.press('Meta+p');
  await page.waitForTimeout(500);
  let quickOpen = page.locator('.quick-input-widget input');
  await quickOpen.waitFor({ state: 'visible', timeout: 5_000 });
  await quickOpen.fill('extension.ts');
  await page.waitForTimeout(600);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1_000);

  // Open commands.ts
  await page.keyboard.press('Meta+p');
  await page.waitForTimeout(500);
  quickOpen = page.locator('.quick-input-widget input');
  await quickOpen.waitFor({ state: 'visible', timeout: 5_000 });
  await quickOpen.fill('commands.ts');
  await page.waitForTimeout(600);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1_000);

  // Open treeView.ts
  await page.keyboard.press('Meta+p');
  await page.waitForTimeout(500);
  quickOpen = page.locator('.quick-input-widget input');
  await quickOpen.waitFor({ state: 'visible', timeout: 5_000 });
  await quickOpen.fill('treeView.ts');
  await page.waitForTimeout(600);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1_000);

  // Screenshot the editor area showing all tabs
  const editorArea = page.locator('.part.editor');
  await editorArea.waitFor({ state: 'visible', timeout: 5_000 });
  await saveScreenshot(editorArea, '15-editor-multiple-tabs');
}

async function screenshotTerminalWithOutput(page: Page) {
  log('Taking Integrated Terminal with output screenshot...');

  // Open terminal
  await runCommand(page, 'Terminal: Create New Terminal');
  await page.waitForTimeout(2_000);

  // Type a command into the terminal
  await page.keyboard.type('echo "Hello from Extension Host"');
  await page.waitForTimeout(300);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1_500);

  const panel = page.locator('.part.panel');
  if (await panel.isVisible().catch(() => false)) {
    await saveScreenshot(panel, '16-terminal-with-output');
  } else {
    log('  Terminal panel not visible, skipping.');
  }

  // Close panel
  await page.keyboard.press('Meta+j');
  await page.waitForTimeout(300);
}

async function screenshotDebugSidebar(page: Page) {
  log('Taking Debug Sidebar screenshot...');

  // Open Run and Debug sidebar via Cmd+Shift+D
  await page.keyboard.press('Meta+Shift+d');
  await page.waitForTimeout(1_500);

  const sidebar = page.locator('.part.sidebar');
  await sidebar.waitFor({ state: 'visible', timeout: 5_000 });

  await saveScreenshot(sidebar, '17-debug-sidebar');

  // Switch back to Explorer
  await page.keyboard.press('Meta+Shift+e');
  await page.waitForTimeout(500);
}

async function screenshotMinimap(page: Page, app: ElectronApplication) {
  log('Taking Minimap screenshot...');

  // Resize window to be shorter/narrower so the minimap is more prominent
  const window = await app.browserWindow(page);
  await window.evaluate((win) => {
    win.setSize(1200, 500);
    win.center();
  });
  await page.waitForTimeout(800);

  // Open the long example file so the minimap has enough content to render
  await page.keyboard.press('Meta+p');
  await page.waitForTimeout(500);
  const quickOpen = page.locator('.quick-input-widget input');
  await quickOpen.waitFor({ state: 'visible', timeout: 5_000 });
  await quickOpen.fill('long-example.ts');
  await page.waitForTimeout(600);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1_500);

  // Screenshot the full editor area — best view of minimap alongside code
  const editorArea = page.locator('.part.editor');
  await editorArea.waitFor({ state: 'visible', timeout: 5_000 });
  await saveScreenshot(editorArea, '18-editor-with-minimap');

  // Restore window to original size
  await window.evaluate((win) => {
    win.setSize(1400, 900);
    win.center();
  });
  await page.waitForTimeout(800);
}

async function screenshotBreadcrumbs(page: Page) {
  log('Taking Breadcrumbs screenshot...');

  // Make sure a file is open so breadcrumbs are visible
  await page.keyboard.press('Meta+p');
  await page.waitForTimeout(500);
  const quickOpen = page.locator('.quick-input-widget input');
  await quickOpen.waitFor({ state: 'visible', timeout: 5_000 });
  await quickOpen.fill('extension.ts');
  await page.waitForTimeout(600);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1_000);

  // Screenshot the breadcrumbs bar
  const breadcrumbs = page.locator('.breadcrumbs-below-tabs');
  if (await breadcrumbs.isVisible().catch(() => false)) {
    await saveScreenshot(breadcrumbs, '19-breadcrumbs');
  } else {
    // Try alternative selector
    const breadcrumbsAlt = page.locator('.editor-breadcrumbs');
    if (await breadcrumbsAlt.isVisible().catch(() => false)) {
      await saveScreenshot(breadcrumbsAlt, '19-breadcrumbs');
    } else {
      log('  Breadcrumbs not visible, taking title area with breadcrumbs...');
      // Fallback: capture the editor group title area which contains breadcrumbs
      const titleArea = page.locator('.editor-group-container .title');
      if (await titleArea.isVisible().catch(() => false)) {
        await saveScreenshot(titleArea, '19-breadcrumbs');
      } else {
        log('  Could not find breadcrumbs element, skipping.');
      }
    }
  }
}

async function screenshotCustomTreeView(page: Page) {
  log('Taking custom Tree View screenshot...');

  // Our sample extension registers a "Dependencies" view in Activity Bar
  // Click on the package icon in the Activity Bar (last custom icon)
  const activityItems = page.locator('.activitybar .action-item');
  const itemCount = await activityItems.count();

  // Find the Dependencies container (our custom view) — it should be the package icon
  let found = false;
  for (let i = 0; i < itemCount; i++) {
    const item = activityItems.nth(i);
    const label = await item.getAttribute('aria-label').catch(() => '');
    if (label && label.includes('Dependencies')) {
      await item.click();
      found = true;
      break;
    }
  }

  if (!found) {
    // Fallback: try clicking activity bar items one by one to find our view
    // The custom view is usually after the built-in ones
    for (let i = itemCount - 3; i < itemCount; i++) {
      if (i >= 0) {
        await activityItems.nth(i).click().catch(() => {});
        await page.waitForTimeout(500);
        const sidebarTitle = page.locator('.sidebar .title .title-label');
        const text = await sidebarTitle.textContent().catch(() => '');
        if (text?.includes('DEPENDENCIES') || text?.includes('Dependencies') || text?.includes('NODE')) {
          found = true;
          break;
        }
      }
    }
  }

  await page.waitForTimeout(1_500);

  // Now hover over one of the tree items to show the Markdown tooltip
  const treeRows = page.locator('.sidebar .monaco-list-row');
  const rowCount = await treeRows.count();

  if (rowCount > 0) {
    // First take a clean screenshot of the tree view
    const sidebar = page.locator('.part.sidebar');
    await saveScreenshot(sidebar, '22-custom-treeview');

    // Now hover to show tooltip
    const targetRow = treeRows.nth(0); // First dependency
    await targetRow.hover();
    await page.waitForTimeout(2_500); // VS Code tooltip delay

    // Screenshot with tooltip visible (sidebar + any overflow)
    await saveScreenshot(page, '22b-treeview-tooltip');
  } else {
    // Extension might not have loaded, take what we have
    const sidebar = page.locator('.part.sidebar');
    await saveScreenshot(sidebar, '22-custom-treeview');
  }

  // Return to Explorer
  await page.keyboard.press('Meta+Shift+e');
  await page.waitForTimeout(500);
}

async function screenshotTaskRunner(page: Page) {
  log('Taking Task Runner (Run Task) screenshot...');

  // Open Command Palette and search for "run task" — screenshot the command list itself
  await openCommandPalette(page, 'run task');
  await page.waitForTimeout(1_000);

  // The task list quick pick should be visible now
  const widget = page.locator('.quick-input-widget');
  if (await widget.isVisible().catch(() => false)) {
    await page.locator('.quick-input-list .monaco-list-row').first().waitFor({
      state: 'visible',
      timeout: 5_000,
    }).catch(() => {});
    await page.waitForTimeout(300);

    await saveScreenshot(widget, '20-task-runner');
  } else {
    log('  Task runner widget not visible, taking full page...');
    await saveScreenshot(page, '20-task-runner-fallback');
  }

  await dismissDialog(page);
}

async function screenshotStatusBarHint(page: Page) {
  log('Taking Status Bar contextual hint screenshot...');

  // Open a TypeScript file to have relevant status bar items
  await page.keyboard.press('Meta+p');
  await page.waitForTimeout(500);
  const quickOpen = page.locator('.quick-input-widget input');
  await quickOpen.waitFor({ state: 'visible', timeout: 5_000 });
  await quickOpen.fill('extension.ts');
  await page.waitForTimeout(600);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1_500);

  // Screenshot the full status bar area — shows language, line/col, encoding etc.
  // This demonstrates contextual status bar items that change per file type
  const statusBar = page.locator('.part.statusbar');
  await statusBar.waitFor({ state: 'visible', timeout: 5_000 });

  await saveScreenshot(statusBar, '21-status-bar-contextual');

  // Also take a wider shot showing bottom of editor + status bar together
  // for better context in the book
  const lowerArea = page.locator('.part.editor, .part.statusbar').first();
  await saveScreenshot(page, '21b-editor-with-statusbar');
}

// ─── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  console.log('=== VS Code Screenshot Tool ===\n');

  await ensureDir(SCREENSHOTS_DIR);

  let app: ElectronApplication | undefined;
  let userDataDir: string | undefined;

  try {
    const instance = await launchVSCode();
    app = instance.app;
    userDataDir = instance.userDataDir;
    const { page } = instance;

    // Set a reasonable window size for consistent screenshots
    const window = await app.browserWindow(page);
    await window.evaluate((win) => {
      win.setSize(1400, 900);
      win.center();
    });
    await page.waitForTimeout(1_000);

    // Take screenshots in sequence
    await screenshotFullWindow(page);
    await screenshotTitleBar(page);
    await screenshotActivityBar(page);
    await screenshotStatusBar(page);
    await screenshotExplorer(page);
    await screenshotEditorWithFile(page);
    await screenshotCommandPalette(page);
    await screenshotCommandPaletteWithSearch(page);
    await screenshotQuickPick(page);
    await screenshotColorThemePicker(page);
    await screenshotSettings(page);
    await screenshotPanel(page);
    await screenshotNotification(page);
    await screenshotProblemsPanel(page);
    await screenshotExtensionsView(page);
    await screenshotEditorMultipleTabs(page);
    await screenshotTerminalWithOutput(page);
    await screenshotDebugSidebar(page);
    await screenshotMinimap(page, app);
    await screenshotBreadcrumbs(page);
    await screenshotCustomTreeView(page);
    await screenshotTaskRunner(page);
    await screenshotStatusBarHint(page);

    console.log(`\nDone! Screenshots saved to: ${SCREENSHOTS_DIR}`);

    // List all screenshots
    const files = await fs.readdir(SCREENSHOTS_DIR);
    const pngs = files.filter((f) => f.endsWith('.png')).sort();
    console.log(`\nGenerated ${pngs.length} screenshots:`);
    for (const f of pngs) {
      const stat = await fs.stat(path.join(SCREENSHOTS_DIR, f));
      console.log(`  ${f}  (${(stat.size / 1024).toFixed(0)} KB)`);
    }
  } catch (err) {
    console.error('\nFailed:', err);
    if (DEBUG) {
      console.log('\nDEBUG mode: VS Code is kept open. Press Ctrl+C to exit.');
      await new Promise(() => {}); // hang forever
    }
    process.exit(1);
  } finally {
    if (!DEBUG && app) {
      await app.close().catch(() => {});
    }
    if (userDataDir) {
      await fs.rm(userDataDir, { recursive: true, force: true }).catch(() => {});
    }
  }
}

main();
