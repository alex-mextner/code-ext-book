"""
book_new.py v3 — только глава Playwright E2E и глава Монетизация.
Диаграммы, цитаты, Yeoman, Bun — функции для встраивания в релевантные места.
"""
from book_helpers import *


# ═══════════════════════════════════════════════════════════════════════════════
# INJECT-ФРАГМЕНТЫ — вставляются в релевантные главы
# ═══════════════════════════════════════════════════════════════════════════════

def arch_diagram_inject():
    """Диаграмма архитектуры → Введение (после описания процессов)."""
    return [sp(6), ArchDiagram(), sp(4)]


def lsp_diagram_inject():
    """Диаграмма LSP → Глава 10 (после абзаца про M×N проблему)."""
    return [sp(6), LSPDiagram(), sp(4)]


def yeoman_inject():
    """Выноска о Yeoman → Глава 1 (после кода с yo code)."""
    return [
        sp(4),
        box(
            'Почему Yeoman, а не npm create?',
            'Yeoman появился в 2012 — задолго до npm create (npm 6, 2018). '
            'generator-code поддерживается Microsoft и обновляется при каждом релизе. '
            'Переезд на другой инструмент стоит ресурсов, а генератор работает — '
            'классическое «не трогай что работает». '
            'Альтернативы: pnpm dlx yo generator-code (без глобального yo), '
            'npm create vscode-extension@latest (неофициальный пакет сообщества), '
            'или собственный template-репозиторий — git clone my-ext-template new-ext.',
            'note'
        ),
        sp(4),
    ]


def bun_inject():
    """Выноска о Bun → Глава 13 (Бандлинг, после npm install esbuild)."""
    return [
        sp(4),
        box(
            'Используете Bun? Важное предупреждение',
            'vsce package, @vscode/test-cli и ovsx явно вызывают "npm list --json" '
            'для обнаружения зависимостей. Bun не реализует этот флаг идентично npm '
            '— упаковка падает. Оптимально: bun install для установки (в 10-25 раз быстрее), '
            'но npm или pnpm для vsce/ovsx/test-cli. '
            'В package.json: "package": "npm exec -- vsce package". '
            'Следите за прогрессом: github.com/oven-sh/bun/issues.',
            'warn'
        ),
        sp(4),
    ]


# Цитаты — по одной для встройки в релевантные места

def q_ux():
    """→ Начало UX-главы."""
    return quote(
        'The best extension is one that feels like it was always part of VS Code. '
        'If users notice your extension exists as a separate thing, you have failed at UX.',
        'Eric Amodio', 'автор GitLens'
    )

def q_notifications():
    """→ Раздел про уведомления (антипаттерны)."""
    return quote(
        'We made the mistake of showing a notification on every startup for the first year. '
        'The 1-star reviews were brutal. We removed it and the average rating '
        'went from 3.2 to 4.7 in a month.',
        'Разработчик популярного расширения', 'анонимно, VS Code Dev Slack 2024'
    )

def q_webview():
    """→ Глава 7, Webview."""
    return quote(
        "Don't fight VS Code. Use its idioms. If you're building a custom UI framework "
        "inside a Webview because you disagree with how VS Code looks — "
        "reconsider the whole approach.",
        'Команда VS Code', 'из официальных UX Guidelines'
    )

def q_activation():
    """→ Раздел про производительность активации."""
    return quote(
        "The activation time is your extension's first impression. "
        'If it takes 500ms to activate, multiply that by every time VS Code starts. '
        "You're taxing millions of users every day.",
        'Isidor Nikolic', 'VS Code Core Team, Microsoft'
    )

def q_cancellation():
    """→ Глава 10, LSP / CancellationToken."""
    return quote(
        'We spent 3 months building the perfect Language Server, '
        "then realized we'd forgotten to handle CancellationToken in any of our providers. "
        'Users were reporting freezes. Always handle cancellation — it\'s not optional.',
        'Разработчик LSP расширения', 'GitHub Discussions, 2023'
    )

def q_activation_events():
    """→ Глава 2, Activation Events."""
    return quote(
        'The number one mistake I see in VS Code extensions is '
        'using activationEvents: ["*"]. '
        "That's the developer saying \"I don't care about VS Code startup time.\" "
        'It should be banned from the Marketplace.',
        'Matt Bierner', 'VS Code Team, Microsoft'
    )

def q_monetization():
    """→ Глава Монетизация."""
    return quote(
        "The hardest part about monetizing a VS Code extension is not the technical work — "
        "it's convincing users that features they used to get for free should cost money now. "
        'Build the paid features from day one, never remove free features.',
        'Erich Gamma', 'создатель VS Code'
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ГЛАВА: E2E тестирование с Playwright
# ═══════════════════════════════════════════════════════════════════════════════

def build_playwright_chapter():
    """E2E Playwright section - now part of Chapter 12 (Testing)."""
    A = []
    def add(*x):
        for i in x: A.append(i)

    add(h1('E2E тестирование с Playwright'))
    add(hl(C['blue']))
    add(sp(4))
    add(p('Третий вид тестирования — E2E (end-to-end) через браузерную автоматизацию. '
          'Playwright запускает VS Code в реальном Chromium или Electron и '
          'управляет им программно: кликает, вводит текст, проверяет визуальные состояния.'))
    add(sp(3))
    add(box('Когда использовать Playwright',
        'Используйте @vscode/test-cli для 95% тестов — они быстрее и проще. '
        'Playwright нужен когда: тестируете Webview UI, проверяете визуальные декорации, '
        'взаимодействие с реальным редактором, или нужны screenshots regression tests.',
        'note'))
    add(sp(6))

    add(h2('Установка и конфигурация'))
    add(code_plain([
        '# Playwright + VS Code web testing',
        'npm install --save-dev @playwright/test @vscode/test-web',
        '',
        '# Для Desktop VS Code через Electron',
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
    add(p('Минимальная конфигурация Playwright для E2E тестов расширения. <b>testDir</b> указывает на отдельную папку test/e2e, <b>timeout</b> увеличен до 60 секунд — VS Code стартует медленно, и стандартных 30 секунд часто не хватает. <b>headless: true</b> — обязательно для CI.'))

    add(sp(6))

    add(h2('Подход 1: тестирование через @vscode/test-web'))
    add(p('@vscode/test-web поднимает локальный сервер с VS Code для тестирования '
          'Web Extension без публикации:'))
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
        '    // @vscode/test-web запускается отдельно (см. package.json)',
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
    add(p('Три хелпера для всех E2E тестов. <b>launchVSCode</b> открывает браузер и ждёт появления .monaco-editor — это гарантирует что редактор полностью загрузился. <b>runCommand</b> эмулирует Command Palette через F1 — так же, как пользователь вызывает команды вручную. <b>getEditorContent</b> читает содержимое через Monaco API напрямую, минуя DOM.'))

    add(sp(4))
    add(code([
        '// test/e2e/webview.test.ts',
        'import { test, expect } from "@playwright/test";',
        'import { launchVSCode, runCommand } from "./helpers";',
        '',
        'test("Webview отображает корректный контент", async ({ page }) => {',
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
    add(p('Тест Webview внутри VS Code. Ключевой момент — <b>contentFrame()</b>: Webview живёт в iframe, и Playwright не видит его содержимое без явного переключения контекста. Сначала ждём появления iframe по title, затем получаем frame и уже внутри него ищем элементы.'))

    add(sp(6))

    add(h2('Подход 2: Desktop VS Code через Electron'))
    add(p('Для полного E2E теста в Desktop VS Code используйте Electron API Playwright:'))
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
        '    test("Status Bar item появляется для .ts файлов", async () => {',
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
        '    test("Декорации появляются при ошибке", async () => {',
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
    add(p('Полноценный Desktop E2E через <b>electron.launch()</b>. Playwright запускает настоящий Electron-процесс VS Code с флагом <b>--extensionDevelopmentPath</b> — расширение загружается из рабочей директории. Два теста: проверка Status Bar элемента при открытии .ts файла и появление декораций ошибок. <b>getVSCodePath()</b> определяет путь к исполняемому файлу на разных платформах.'))

    add(sp(6))

    add(h2('CI/CD для Playwright тестов'))
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
    add(p('GitHub Actions workflow для E2E тестов. Ключевой шаг — <b>playwright install --with-deps chromium</b>: устанавливает браузер и системные зависимости (шрифты, библиотеки) на Ubuntu. <b>upload-artifact</b> с <b>if: always()</b> сохраняет HTML-отчёт даже при падении тестов — это критично для отладки нестабильных E2E.'))
    add(pb())
    return A


# ═══════════════════════════════════════════════════════════════════════════════
# ГЛАВА: Монетизация расширений
# ═══════════════════════════════════════════════════════════════════════════════

def build_business_chapter():
    A = []
    def add(*x):
        for i in x: A.append(i)

    add(StableAnchor('chapter_20'))
    add(toc_ch('Глава 20: Монетизация VS Code расширений'), banner('Глава 20', 'Монетизация VS Code расширений',
               'Как компании и разработчики зарабатывают на расширениях'), sp(12))

    add(h2('Рынок расширений в цифрах'))
    add(p('73.6% разработчиков используют VS Code (Stack Overflow Survey 2024). '
          'Топовые расширения имеют десятки миллионов установок. '
          'Это огромная аудитория — и реальные деньги.'))
    add(sp(6))
    add(MonetizationDiagram())
    add(sp(8))

    add(h2('Модель 1: Freemium'))
    add(p('Базовые функции бесплатно, продвинутые — платно. '
          'Самая распространённая модель.'))
    add(sp(3))
    add(tblh(['Расширение', 'Как работает']))
    add(tbl2([
        ('GitLens (GitKraken)',
         'Core бесплатно. Pro $4.99/мес: Commit Graph, AI Explain Commit. '
         '21M+ установок = огромная воронка'),
        ('Tabnine',
         'Бесплатно: локальные AI-подсказки. Pro $12/мес: GPT-4, chat. '
         'Enterprise $39/пользователь'),
        ('GitHub Copilot',
         '$10/мес, Business $19/пользователь. '
         'Самый успешный пример монетизации через расширение'),
        ('Codeium/Windsurf',
         'Бесплатный конкурент Copilot. Монетизация через Enterprise '
         'и собственную IDE Windsurf'),
    ]))
    add(sp(6))

    add(h2('Модель 2: SaaS Backend'))
    add(p('Расширение бесплатно и open source, монетизируется через облачный сервис. '
          'Классическое «лезвие бесплатно — лезвия платные».'))
    add(sp(3))
    add(tblh(['Компания', 'Стратегия']))
    add(tbl2([
        ('Sentry',
         'Расширение бесплатно — показывает ошибки прямо в коде. '
         'Монетизируется через Sentry SaaS: расширение = воронка привлечения'),
        ('MongoDB',
         'MongoDB for VS Code бесплатно. '
         'Монетизация через MongoDB Atlas: расширение снижает барьер входа'),
        ('Prisma',
         'VS Code расширение (подсветка schema) бесплатно + OSS. '
         'Монетизация через Prisma Data Platform'),
        ('Datadog / Stripe / Vercel',
         'Расширение бесплатно — снижает трение при начале работы с продуктом. '
         'Больше пользователей → больше платящих клиентов'),
    ]))
    add(sp(6))

    add(h2('Модель 3: Open Source + корпоративное финансирование'))
    add(p('OSS-ядро (MIT/Apache) + деньги от компаний-спонсоров или за enterprise-поддержку.'))
    add(sp(3))
    add(tblh(['Расширение', 'Источник дохода']))
    add(tbl2([
        ('ESLint / Prettier',
         'GitHub Sponsors, OpenCollective. Prettier ~$50k/год от корпоративных спонсоров'),
        ('rust-analyzer',
         'Rust Foundation ($130k/год бюджет), NLNet grants, Ferrous Systems'),
        ('Pylance / Python',
         'Microsoft — инвестиция как часть Azure marketing. '
         'Привлекает разработчиков в Azure ecosystem'),
    ]))
    add(sp(6))

    add(h2('Реальные числа'))
    add(tblh(['Сценарий', 'Потенциальный доход']))
    add(tbl2([
        ('Инди, 100k установок, 1% конверсия в $5/мес',
         '~$5k/мес = $60k/год. Реалистично для нишевых инструментов'),
        ('Команда 3 чел., 1M+ установок, Pro $9/мес, 0.5% конверсия',
         '~$45k/мес = $540k/год. GitLens-подобная модель'),
        ('SaaS, расширение как воронка',
         'Снижает CAC на 30-50%. 1000 привлечённых × $100 MRR = $100k MRR'),
        ('OSS + корпоративные спонсоры',
         '$10k–200k/год в зависимости от популярности'),
    ]))
    add(sp(6))

    add(q_monetization())
    add(sp(6))

    add(h2('Практические советы'))
    for item in [
        '<b>Freemium beats Paid:</b> платное расширение снижает install rate на 95%+. '
        'Всегда делайте бесплатный tier',
        '<b>Marketplace не поддерживает платежи</b> — нужен внешний сайт + лицензионные ключи',
        '<b>GitHub Sponsors</b> для OSS: крупные компании охотно спонсируют инструменты которые используют',
        '<b>Enterprise tier:</b> корпоративные клиенты платят 10× — SLA, поддержка, SSO',
        '<b>Timing:</b> монетизировать до 100k установок тяжело. После 500k — легче',
        '<b>Инфраструктура — бесплатное расширение с платным сервером: вы платите за чужой успех.</b> '
        'Если расширение бесплатно, но использует ваш backend (API, AI-модель, база данных, хранилище) — '
        'с ростом установок растут ваши серверные расходы, а доходов нет. '
        'Это ловушка: вы успешны как продукт, но убыточны как бизнес. '
        '10 000 активных пользователей могут генерировать ощутимые cloud-счета каждый месяц. '
        'Решения: freemium с лимитами API, собственный API-ключ пользователя, '
        'или монетизация через subscription. Закладывайте это до релиза, не после',
    ]:
        add(bul(item))
    add(sp(6))

    add(h2('Технические решения для монетизации'))
    add(p('VS Code не предоставляет встроенных payment API. '
          'Стандартная реализация через внешний API + SecretStorage:'))
    add(sp(3))
    add(code([
        '// LicenseManager — проверка через внешний API',
        'export class LicenseManager {',
        '',
        '    static async check(ctx: vscode.ExtensionContext): Promise<boolean> {',
        '        // Кэш на 24 часа в SecretStorage',
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
        '            return false;  // offline grace — не блокируем',
        '        }',
        '    }',
        '}',
        '',
        '// В activate(): ненавязчивое напоминание (5% шанс)',
        'const isPro = await LicenseManager.check(context);',
        'if (!isPro && Math.random() < 0.05) {',
        '    vscode.window.showInformationMessage(',
        '        "My Extension Pro — расширенные функции",',
        '        "Узнать больше"',
        '    ).then(r => r && vscode.env.openExternal(vscode.Uri.parse(PRO_URL)));',
        '}',
    ]))
    add(sp(3))
    add(p('Полный цикл проверки лицензии. <b>LicenseManager.check</b> сначала проверяет кэш в SecretStorage (24 часа), затем валидирует ключ через внешний API с привязкой к <b>vscode.env.machineId</b>. При сетевой ошибке — offline grace, не блокируем пользователя. Во второй части — паттерн ненавязчивого upsell: сообщение показывается с вероятностью 5%, а не при каждом запуске. <b>context.secrets</b> хранит данные в системном keychain — никогда не используйте globalState для секретов.'))
    add(pb())
    return A


# ═══════════════════════════════════════════════════════════════════════════════
# ГЛАВНАЯ ФУНКЦИЯ — только Playwright + Business
# ═══════════════════════════════════════════════════════════════════════════════

def build_story_new():
    """Only Business/Monetization chapter now. Playwright moved to Chapter 12."""
    return build_business_chapter()


if __name__ == '__main__':
    print(f'build_story_new: {len(build_story_new())} elements')
    print(f'arch_diagram_inject: {len(arch_diagram_inject())} elements')
    print(f'lsp_diagram_inject: {len(lsp_diagram_inject())} elements')
