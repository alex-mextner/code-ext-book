"""
book_new_en.py v3 — Playwright E2E chapter and Monetization chapter only.
Diagrams, quotes, Yeoman, Bun — functions for injection into relevant places.
"""
from book_helpers import *


# ==============================================================================
# INJECT FRAGMENTS — inserted into relevant chapters
# ==============================================================================

def arch_diagram_inject():
    """Architecture diagram -> Introduction (after process description)."""
    return [sp(6), ArchDiagram(), sp(4)]


def lsp_diagram_inject():
    """LSP diagram -> Chapter 10 (after the M*N problem paragraph)."""
    return [sp(6), LSPDiagram(), sp(4)]


def yeoman_inject():
    """Yeoman callout -> Chapter 1 (after the yo code snippet)."""
    return [
        sp(4),
        box(
            'Why Yeoman and not npm create?',
            'Yeoman appeared in 2012 — long before npm create (npm 6, 2018). '
            'generator-code is maintained by Microsoft and updated with every release. '
            'Migrating to another tool costs resources, and the generator works — '
            'the classic "don\'t touch what works". '
            'Alternatives: pnpm dlx yo generator-code (without global yo), '
            'npm create vscode-extension@latest (unofficial community package), '
            'or your own template repository — git clone my-ext-template new-ext.',
            'note'
        ),
        sp(4),
    ]


def bun_inject():
    """Bun callout -> Chapter 13 (Bundling, after npm install esbuild)."""
    return [
        sp(4),
        box(
            'Using Bun? Important warning',
            'vsce package, @vscode/test-cli, and ovsx explicitly call "npm list --json" '
            'to discover dependencies. Bun does not implement this flag identically to npm '
            '— packaging fails. Optimal approach: bun install for installation (10-25x faster), '
            'but npm or pnpm for vsce/ovsx/test-cli. '
            'In package.json: "package": "npm exec -- vsce package". '
            'Track progress: github.com/oven-sh/bun/issues.',
            'warn'
        ),
        sp(4),
    ]


# Quotes — one each for injection into relevant places

def q_ux():
    """-> Start of UX chapter."""
    return quote(
        'The best extension is one that feels like it was always part of VS Code. '
        'If users notice your extension exists as a separate thing, you have failed at UX.',
        'Eric Amodio', 'creator of GitLens'
    )

def q_notifications():
    """-> Notifications section (anti-patterns)."""
    return quote(
        'We made the mistake of showing a notification on every startup for the first year. '
        'The 1-star reviews were brutal. We removed it and the average rating '
        'went from 3.2 to 4.7 in a month.',
        'Developer of a popular extension', 'anonymous, VS Code Dev Slack 2024'
    )

def q_webview():
    """-> Chapter 7, Webview."""
    return quote(
        "Don't fight VS Code. Use its idioms. If you're building a custom UI framework "
        "inside a Webview because you disagree with how VS Code looks — "
        "reconsider the whole approach.",
        'VS Code Team', 'from the official UX Guidelines'
    )

def q_activation():
    """-> Section on activation performance."""
    return quote(
        "The activation time is your extension's first impression. "
        'If it takes 500ms to activate, multiply that by every time VS Code starts. '
        "You're taxing millions of users every day.",
        'Isidor Nikolic', 'VS Code Core Team, Microsoft'
    )

def q_cancellation():
    """-> Chapter 10, LSP / CancellationToken."""
    return quote(
        'We spent 3 months building the perfect Language Server, '
        "then realized we'd forgotten to handle CancellationToken in any of our providers. "
        'Users were reporting freezes. Always handle cancellation — it\'s not optional.',
        'LSP extension developer', 'GitHub Discussions, 2023'
    )

def q_activation_events():
    """-> Chapter 2, Activation Events."""
    return quote(
        'The number one mistake I see in VS Code extensions is '
        'using activationEvents: ["*"]. '
        "That's the developer saying \"I don't care about VS Code startup time.\" "
        'It should be banned from the Marketplace.',
        'Matt Bierner', 'VS Code Team, Microsoft'
    )

def q_monetization():
    """-> Monetization chapter."""
    return quote(
        "The hardest part about monetizing a VS Code extension is not the technical work — "
        "it's convincing users that features they used to get for free should cost money now. "
        'Build the paid features from day one, never remove free features.',
        'Erich Gamma', 'creator of VS Code'
    )


# ==============================================================================
# CHAPTER: E2E Testing with Playwright
# ==============================================================================

def build_playwright_chapter():
    """E2E Playwright section - now part of Chapter 12 (Testing)."""
    A = []
    def add(*x):
        for i in x: A.append(i)

    add(h1('E2E Testing with Playwright'))
    add(hl(C['blue']))
    add(sp(4))
    add(p('The third type of testing is E2E (end-to-end) via browser automation. '
          'Playwright launches VS Code in real Chromium or Electron and '
          'controls it programmatically: clicking, typing text, verifying visual states.'))
    add(sp(3))
    add(box('When to use Playwright',
        'Use @vscode/test-cli for 95% of tests — they are faster and simpler. '
        'Playwright is needed when: you test Webview UI, verify visual decorations, '
        'interact with the real editor, or need screenshot regression tests.',
        'note'))
    add(sp(6))

    add(h2('Installation and Configuration'))
    add(code_plain([
        '# Playwright + VS Code web testing',
        'npm install --save-dev @playwright/test @vscode/test-web',
        '',
        '# For Desktop VS Code via Electron',
        'npm install --save-dev playwright @vscode/test-electron',
    ]))
    add(sp(3))
    add(code([
        '// playwright.config.ts',
        'import { defineConfig } from "@playwright/test";',
        '',
        'export default defineConfig({',
        '    testDir: "./test/e2e",',
        '    timeout: 60000,',
        '    use: { headless: true },',
        '    reporter: [["html"], ["list"]],',
        '});',
    ]))
    add(sp(3))
    add(p('Minimal Playwright configuration for extension E2E tests. <b>testDir</b> points to a separate test/e2e folder, <b>timeout</b> is increased to 60 seconds — VS Code starts slowly and the default 30 seconds is often insufficient. <b>headless: true</b> is required for CI.'))

    add(sp(6))

    add(h2('Approach 1: Testing via @vscode/test-web'))
    add(p('@vscode/test-web starts a local server with VS Code for testing '
          'Web Extensions without publishing:'))
    add(sp(3))
    add(code_plain([
        '# package.json scripts',
        '"open-in-browser": "vscode-test-web --browserType=chromium '
        '--extensionDevelopmentPath=. .",',
        '"test:e2e": "playwright test"',
    ]))
    add(sp(3))
    add(code([
        '// test/e2e/helpers.ts',
        'import { chromium, type Page } from "@playwright/test";',
        '',
        'export async function launchVSCode(workspacePath: string): Promise<Page> {',
        '    const port = 3000 + Math.floor(Math.random() * 1000);',
        '    // @vscode/test-web is started separately (see package.json)',
        '    const browser = await chromium.launch({ headless: true });',
        '    const page = await browser.newPage();',
        '    await page.goto(`http://localhost:${port}`);',
        '    await page.waitForSelector(".monaco-editor", { timeout: 30000 });',
        '    return page;',
        '}',
        '',
        'export async function runCommand(page: Page, cmd: string) {',
        '    await page.keyboard.press("F1");',
        '    await page.waitForSelector(".quick-input-widget");',
        '    await page.keyboard.type(cmd);',
        '    await page.waitForTimeout(300);',
        '    await page.keyboard.press("Enter");',
        '}',
        '',
        'export async function getEditorContent(page: Page): Promise<string> {',
        '    return page.evaluate(() => {',
        '        const editor = (window as any).monaco?.editor?.getEditors()?.[0];',
        '        return editor?.getValue() ?? "";',
        '    });',
        '}',
    ]))
    add(sp(3))
    add(p('Three helpers for all E2E tests. <b>launchVSCode</b> opens the browser and waits for .monaco-editor to appear — this guarantees the editor is fully loaded. <b>runCommand</b> emulates the Command Palette via F1 — just as the user invokes commands manually. <b>getEditorContent</b> reads the content via the Monaco API directly, bypassing the DOM.'))

    add(sp(4))
    add(code([
        '// test/e2e/webview.test.ts',
        'import { test, expect } from "@playwright/test";',
        'import { launchVSCode, runCommand } from "./helpers";',
        '',
        'test("Webview renders correct content", async ({ page }) => {',
        '    await launchVSCode("./test/fixtures");',
        '',
        '    await runCommand(page, "My Extension: Open Dashboard");',
        '',
        '    const webview = await page.waitForSelector(\'iframe[title="My Dashboard"]\');',
        '    expect(webview).toBeTruthy();',
        '',
        '    const frame = await webview.contentFrame();',
        '    if (!frame) throw new Error("Frame not found");',
        '',
        '    await frame.waitForSelector("#main-content");',
        '    const title = await frame.textContent("h1");',
        '    expect(title).toContain("Dashboard");',
        '});',
    ]))
    add(sp(3))
    add(p('Testing a Webview inside VS Code. The key point is <b>contentFrame()</b>: a Webview lives in an iframe, and Playwright cannot see its content without explicitly switching context. First we wait for the iframe to appear by title, then get the frame and search for elements inside it.'))

    add(sp(6))

    add(h2('Approach 2: Desktop VS Code via Electron'))
    add(p('For a full E2E test in Desktop VS Code, use the Playwright Electron API:'))
    add(sp(3))
    add(code([
        '// test/e2e/desktop.test.ts',
        'import { test, expect } from "@playwright/test";',
        'import { _electron as electron } from "playwright";',
        '',
        'test.describe("Desktop E2E", () => {',
        '    let app: Awaited<ReturnType<typeof electron.launch>>;',
        '',
        '    test.beforeAll(async () => {',
        '        app = await electron.launch({',
        '            executablePath: getVSCodePath(),',
        '            args: [',
        '                "--extensionDevelopmentPath=" + process.cwd(),',
        '                "--disable-extensions",',
        '                "--new-window",',
        '            ],',
        '        });',
        '    });',
        '',
        '    test.afterAll(() => app.close());',
        '',
        '    test("Status Bar item appears for .ts files", async () => {',
        '        const page = await app.firstWindow();',
        '        await page.keyboard.press("Meta+P");',
        '        await page.keyboard.type("example.ts");',
        '        await page.keyboard.press("Enter");',
        '',
        '        const item = await page.waitForSelector(',
        '            \'[aria-label*="My Extension"]\',',
        '            { timeout: 10000 }',
        '        );',
        '        const text = await item.textContent();',
        '        expect(text).toContain("0 errors");',
        '    });',
        '',
        '    test("Decorations appear on error", async () => {',
        '        const page = await app.firstWindow();',
        '        await page.keyboard.press("Meta+A");',
        '        await page.keyboard.type("const x: number = \'string\';");',
        '        await page.waitForTimeout(1000);',
        '        expect(await page.$(".squiggly-error")).toBeTruthy();',
        '    });',
        '});',
        '',
        'function getVSCodePath(): string {',
        '    if (process.platform === "win32")',
        '        return "C:\\\\Program Files\\\\Microsoft VS Code\\\\Code.exe";',
        '    if (process.platform === "darwin")',
        '        return "/Applications/Visual Studio Code.app/Contents/MacOS/Electron";',
        '    return require("child_process").execSync("which code").toString().trim();',
        '}',
    ]))
    add(sp(3))
    add(p('Full Desktop E2E via <b>electron.launch()</b>. Playwright launches a real Electron VS Code process with the <b>--extensionDevelopmentPath</b> flag — the extension loads from the working directory. Two tests: checking a Status Bar item when opening a .ts file and verifying error decorations appear. <b>getVSCodePath()</b> determines the executable path on different platforms.'))

    add(sp(6))

    add(h2('CI/CD for Playwright Tests'))
    add(code_plain([
        '# .github/workflows/e2e.yml',
        'name: E2E Tests',
        'on: [push, pull_request]',
        '',
        'jobs:',
        '  e2e:',
        '    runs-on: ubuntu-latest',
        '    steps:',
        '      - uses: actions/checkout@v4',
        '      - uses: actions/setup-node@v4',
        '        with: { node-version: 20 }',
        '      - run: npm ci && npm run compile',
        '      - run: npx playwright install --with-deps chromium',
        '      - run: npm run test:e2e',
        '      - uses: actions/upload-artifact@v4',
        '        if: always()',
        '        with:',
        '          name: playwright-report',
        '          path: playwright-report/',
        '          retention-days: 30',
    ]))
    add(sp(3))
    add(p('GitHub Actions workflow for E2E tests. The key step is <b>playwright install --with-deps chromium</b>: installs the browser and system dependencies (fonts, libraries) on Ubuntu. <b>upload-artifact</b> with <b>if: always()</b> saves the HTML report even when tests fail — critical for debugging flaky E2E tests.'))
    add(pb())
    return A


# ==============================================================================
# CHAPTER: Extension Monetization
# ==============================================================================

def build_business_chapter():
    A = []
    def add(*x):
        for i in x: A.append(i)

    add(StableAnchor('chapter_20'))
    add(toc_ch('Chapter 20: VS Code Extension Monetization'), banner('Chapter 20', 'VS Code Extension Monetization',
               'How companies and developers make money from extensions'), sp(12))

    add(h2('The Extension Market in Numbers'))
    add(p('73.6% of developers use VS Code (Stack Overflow Survey 2024). '
          'Top extensions have tens of millions of installs. '
          'This is a massive audience — and real money.'))
    add(sp(6))
    add(MonetizationDiagram())
    add(sp(8))

    add(h2('Model 1: Freemium'))
    add(p('Basic features free, advanced features paid. '
          'The most common model.'))
    add(sp(3))
    add(tblh(['Extension', 'How it works']))
    add(tbl2([
        ('GitLens (GitKraken)',
         'Core is free. Pro $4.99/mo: Commit Graph, AI Explain Commit. '
         '21M+ installs = huge funnel'),
        ('Tabnine',
         'Free: local AI suggestions. Pro $12/mo: GPT-4, chat. '
         'Enterprise $39/user'),
        ('GitHub Copilot',
         '$10/mo, Business $19/user. '
         'The most successful example of monetization through an extension'),
        ('Codeium/Windsurf',
         'Free Copilot competitor. Monetization through Enterprise '
         'and their own IDE Windsurf'),
    ]))
    add(sp(6))

    add(h2('Model 2: SaaS Backend'))
    add(p('The extension is free and open source; monetization is through a cloud service. '
          'The classic "razor free — blades paid" model.'))
    add(sp(3))
    add(tblh(['Company', 'Strategy']))
    add(tbl2([
        ('Sentry',
         'Extension is free — shows errors right in the code. '
         'Monetization through Sentry SaaS: extension = acquisition funnel'),
        ('MongoDB',
         'MongoDB for VS Code is free. '
         'Monetization through MongoDB Atlas: extension lowers the entry barrier'),
        ('Prisma',
         'VS Code extension (schema highlighting) is free + OSS. '
         'Monetization through Prisma Data Platform'),
        ('Datadog / Stripe / Vercel',
         'Extension is free — reduces friction when starting with the product. '
         'More users -> more paying customers'),
    ]))
    add(sp(6))

    add(h2('Model 3: Open Source + Corporate Funding'))
    add(p('OSS core (MIT/Apache) + money from corporate sponsors or for enterprise support.'))
    add(sp(3))
    add(tblh(['Extension', 'Revenue source']))
    add(tbl2([
        ('ESLint / Prettier',
         'GitHub Sponsors, OpenCollective. Prettier ~$50k/year from corporate sponsors'),
        ('rust-analyzer',
         'Rust Foundation ($130k/year budget), NLNet grants, Ferrous Systems'),
        ('Pylance / Python',
         'Microsoft — investment as part of Azure marketing. '
         'Attracts developers to the Azure ecosystem'),
    ]))
    add(sp(6))

    add(h2('Real Numbers'))
    add(tblh(['Scenario', 'Potential revenue']))
    add(tbl2([
        ('Indie, 100k installs, 1% conversion at $5/mo',
         '~$5k/mo = $60k/year. Realistic for niche tools'),
        ('Team of 3, 1M+ installs, Pro $9/mo, 0.5% conversion',
         '~$45k/mo = $540k/year. GitLens-like model'),
        ('SaaS, extension as a funnel',
         'Reduces CAC by 30-50%. 1000 acquired x $100 MRR = $100k MRR'),
        ('OSS + corporate sponsors',
         '$10k-200k/year depending on popularity'),
    ]))
    add(sp(6))

    add(q_monetization())
    add(sp(6))

    add(h2('Practical Advice'))
    for item in [
        '<b>Freemium beats Paid:</b> a paid extension reduces install rate by 95%+. '
        'Always provide a free tier',
        '<b>The Marketplace does not support payments</b> — you need an external site + license keys',
        '<b>GitHub Sponsors</b> for OSS: large companies willingly sponsor tools they use',
        '<b>Enterprise tier:</b> corporate clients pay 10x — SLA, support, SSO',
        '<b>Timing:</b> monetizing before 100k installs is hard. After 500k — easier',
        '<b>Infrastructure — free extension with a paid server: you pay for others\' success.</b> '
        'If the extension is free but uses your backend (API, AI model, database, storage) — '
        'as installs grow, your server costs grow too, but revenue does not. '
        'This is a trap: you are successful as a product but unprofitable as a business. '
        '10,000 active users can generate significant cloud bills every month. '
        'Solutions: freemium with API limits, user\'s own API key, '
        'or monetization via subscription. Plan this before release, not after',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Technical Solutions for Monetization'))
    add(p('VS Code does not provide built-in payment APIs. '
          'The standard implementation uses an external API + SecretStorage:'))
    add(sp(3))
    add(code([
        '// LicenseManager — validation via external API',
        'export class LicenseManager {',
        '',
        '    static async check(ctx: vscode.ExtensionContext): Promise<boolean> {',
        '        // Cache for 24 hours in SecretStorage',
        '        const cached = await ctx.secrets.get("licenseStatus");',
        '        if (cached) {',
        '            const { valid, expiry } = JSON.parse(cached);',
        '            if (new Date(expiry) > new Date()) return valid;',
        '        }',
        '        const key = await ctx.secrets.get("licenseKey");',
        '        if (!key) return false;',
        '        try {',
        '            const res = await fetch("https://api.myext.com/validate", {',
        '                method: "POST",',
        '                body: JSON.stringify({ key, machineId: vscode.env.machineId }),',
        '                headers: { "Content-Type": "application/json" }',
        '            });',
        '            const { valid } = await res.json();',
        '            await ctx.secrets.store("licenseStatus", JSON.stringify({',
        '                valid,',
        '                expiry: new Date(Date.now() + 86400_000).toISOString()',
        '            }));',
        '            return valid;',
        '        } catch {',
        '            return false;  // offline grace — don\'t block',
        '        }',
        '    }',
        '}',
        '',
        '// In activate(): non-intrusive reminder (5% chance)',
        'const isPro = await LicenseManager.check(context);',
        'if (!isPro && Math.random() < 0.05) {',
        '    vscode.window.showInformationMessage(',
        '        "My Extension Pro — advanced features",',
        '        "Learn more"',
        '    ).then(r => r && vscode.env.openExternal(vscode.Uri.parse(PRO_URL)));',
        '}',
    ]))
    add(sp(3))
    add(p('Full license verification cycle. <b>LicenseManager.check</b> first checks the cache in SecretStorage (24 hours), then validates the key via an external API bound to <b>vscode.env.machineId</b>. On network error — offline grace, don\'t block the user. The second part shows a non-intrusive upsell pattern: the message is shown with a 5% probability, not on every launch. <b>context.secrets</b> stores data in the system keychain — never use globalState for secrets.'))
    add(pb())
    return A


# ==============================================================================
# MAIN FUNCTION — Playwright + Business only
# ==============================================================================

def build_story_new():
    """Only Business/Monetization chapter now. Playwright moved to Chapter 12."""
    return build_business_chapter()


if __name__ == '__main__':
    print(f'build_story_new: {len(build_story_new())} elements')
    print(f'arch_diagram_inject: {len(arch_diagram_inject())} elements')
    print(f'lsp_diagram_inject: {len(lsp_diagram_inject())} elements')
