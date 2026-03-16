"""
book_perf.py — Что делает VS Code быстрым
Технический разбор + как применять те же техники в расширениях
"""
from book_helpers import *


def build_perf_chapter():
    A = []
    def add(*x):
        for i in x: A.append(i)

    add(StableAnchor('chapter_perf'))
    add(toc_ch('Что делает VS Code быстрым'), banner('Углублённо', 'Что делает VS Code быстрым',
               'Архитектура, движок, рендеринг и уроки для разработчиков расширений'),
        sp(12))

    add(h2('Введение: Electron — не приговор'))
    add(p('VS Code — Electron-приложение. Как и Slack (до переписки на нативный код), '
          'Discord, Figma, Notion. Все эти приложения известны как «тяжёлые». '
          'Но VS Code — нет. Почему?'))
    add(sp(4))
    add(p('Короткий ответ: Electron не делает приложения медленными. '
          'Его делают медленными разработчики, которые не думают о производительности. '
          'VS Code — результат <b>десяти лет накопленных оптимизаций</b>, '
          'многие из которых обратно повлияли на сам Electron и V8.'))
    add(sp(4))

    add(quote(
        'VS Code is the benchmark of what can be done with Electron '
        '— if you really, really care about performance.',
        'Hacker News', 'комментарий с 800+ upvotes, 2021'
    ))
    add(sp(6))

    add(quote(
        'Modern text editors have higher latency than 42-year-old Emacs. '
        'Text editors! What can be simpler? On each keystroke, all you have to do '
        'is update a tiny rectangular region and modern text editors '
        "can't do that in 16ms. It's a lot of time. A LOT.",
        'Никита Прокопов (tonsky)', 'Software Disenchantment, tonsky.me, 2018'
    ))
    add(sp(4))
    add(p('Прокопов пишет это как критику индустрии в целом. VS Code — одно из редких '
          'исключений: редактор, который действительно озаботился input latency и '
          'добился результатов сравнимых с нативными приложениями.'))
    add(sp(6))

    # ── 1. МНОГОПРОЦЕССНАЯ АРХИТЕКТУРА ─────────────────────────────────────
    add(h1('1. Многопроцессная изоляция'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('Фундаментальное архитектурное решение VS Code — <b>ни одно расширение '
          'не может заморозить UI</b>. Extension Host — отдельный Node.js процесс. '
          'Если расширение уходит в бесконечный цикл или падает с out of memory, '
          'редактор продолжает работать. Это не банальность: большинство Electron-приложений '
          'делают всё в одном renderer-процессе.'))
    add(sp(3))
    add(tblh(['Процесс', 'Что делает и почему изолирован']))
    add(tbl2([
        ('Main Process\n(Electron main)',
         'Управление окнами, lifecycle, нативные диалоги. '
         'Сознательно разгружен — перегруженный main = зависший UI'),
        ('Renderer Process\n(Chromium)',
         'Только UI: рендеринг, Monaco editor, реакция на ввод. '
         'С 2023 — полный sandbox, без доступа к Node.js'),
        ('Extension Host\n(Node.js, UtilityProcess)',
         'ВСЕ расширения в одном процессе. '
         'Изолирован от UI. С 2023 — UtilityProcess вместо fork()'),
        ('Shared Process\n(скрытое окно)',
         'Файловый watcher, установка расширений, fts-поиск. '
         'Не связан с конкретным окном'),
        ('Language Server\n(дочерний процесс)',
         'Каждый LSP-сервер — отдельный процесс. '
         'TypeScript анализирует код в фоне, не блокируя набор текста'),
    ]))
    add(sp(4))
    add(box('UtilityProcess — новый API (Electron 22+)',
        'VS Code в 2023 году перешёл с fork() на UtilityProcess для Extension Host. '
        'UtilityProcess — нативный API Electron для создания защищённых '
        'дочерних процессов с V8 sandbox. '
        'Это снизило overhead и улучшило безопасность: '
        'расширения больше не могут обходить V8 sandbox через нативные аддоны '
        'без явного разрешения.', 'note'))
    add(sp(6))

    # ── 2. V8 SNAPSHOTS И CODE CACHING ─────────────────────────────────────
    add(h1('2. V8 Snapshots и Code Caching'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('Самая большая проблема запуска JavaScript-приложения — <b>парсинг и компиляция</b>. '
          'Workbench bundle VS Code — около 11.5 MB минифицированного кода. '
          'Без оптимизаций V8 парсирует его заново при каждом запуске.'))
    add(sp(4))

    add(h3('V8 Code Caching'))
    add(p('VS Code с 2017 года использует V8 Code Cache: после первого запуска V8 сохраняет '
          'скомпилированный байткод на диск. При следующих запусках — загружает байткод '
          'напрямую, минуя parsing + compilation.'))
    add(sp(3))
    add(p('Chromium делает это автоматически, но только для «горячих» страниц '
          '(часто посещаемых). VS Code использует параметр <b>bypassHeatCheck</b>, '
          'чтобы кэш работал с первого запуска — потому что это десктопное приложение, '
          'а не веб-страница.'))
    add(sp(4))

    add(h3('V8 Startup Snapshots'))
    add(p('Более агрессивная техника: вместо кэширования байткода — '
          'сохранение всего V8 heap после инициализации. '
          'При следующем запуске V8 десериализует готовый heap вместо выполнения '
          'init-кода с нуля. VS Code использует это с 2017 года.'))
    add(sp(3))
    add(code([
        '// Как это работает концептуально:',
        '// 1. Запуск: выполняем весь init-код',
        '// 2. Сохраняем снимок V8 heap на диск',
        '// 3. Следующий запуск: десериализуем heap — код уже "выполнен"',
        '',
        '// Для расширений: аналог через require() кэш',
        '// Бандлинг (esbuild) + один большой файл вместо 100 маленьких',
        '// = V8 лучше кэширует и оптимизирует',
    ]))
    add(sp(3))
    add(p('Трёхэтапная схема V8 Startup Snapshot: первый запуск выполняет init-код, сохраняет heap на диск, последующие запуски десериализуют готовый heap. Для расширений прямого доступа к снапшотам нет, но <b>бандлинг через esbuild</b> в один файл даёт V8 лучшие условия для code caching — аналогичный эффект.'))

    add(sp(4))

    add(h3('AMD → ESM: +10% скорости запуска (VS Code 1.94, 2024)'))
    add(p('Исторически VS Code использовал AMD (Asynchronous Module Definition) '
          'с кастомным загрузчиком. AMD — не нативный для V8, каждый require() '
          'добавлял overhead. В 2024 году команда завершила миграцию на <b>ESM</b>:'))
    add(sp(2))
    for item in [
        'ESM нативен для V8 — движок понимает граф зависимостей статически',
        'Бандл workbench уменьшился на <b>&gt;10%</b>',
        'Исчез overhead кастомного AMD-загрузчика',
        'Появилась возможность tree-shaking на уровне движка',
    ]:
        add(bul(item))
    add(sp(3))
    add(box('Расширения всё ещё на CommonJS',
        'После перехода VS Code core на ESM расширения по-прежнему загружаются через '
        'CommonJS (require). Это временно — github.com/microsoft/vscode/issues/130367. '
        'Когда ESM для расширений будет готов, это ещё ускорит Extension Host startup.',
        'note'))
    add(sp(6))

    # ── 3. MONACO: КАСТОМНЫЙ РЕНДЕРИНГ ─────────────────────────────────────
    add(h1('3. Monaco Editor: рендеринг текста'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('Monaco — не просто textarea с подсветкой. '
          'Это полностью кастомный движок рендеринга текста с '
          '<b>тремя слоями</b>:'))
    add(sp(3))
    add(tblh(['Слой', 'Технология и назначение']))
    add(tbl2([
        ('DOM renderer\n(по умолчанию)',
         'Каждая строка — отдельный &lt;div&gt;. Только видимые строки в DOM (виртуализация). '
         'Символы разбиты на &lt;span&gt; по токенам темы. '
         'Работает везде, хорошая accessibility'),
        ('Canvas 2D renderer',
         'Текст рисуется на HTML Canvas. Обходит layout engine браузера. '
         'Быстрее DOM для больших файлов. '
         'Использует texture atlas для глифов'),
        ('WebGL renderer\n(терминал xterm.js)',
         'Текст как quad-ы на GPU через WebGL. '
         'Самый быстрый — GPU параллелизм. '
         'Используется в интегрированном терминале'),
    ]))
    add(sp(4))

    add(h3('Виртуализация строк — ключевая техника'))
    add(p('В DOM редактора <b>никогда нет всех строк файла</b>. '
          'Monaco вычисляет viewport и создаёт DOM-элементы только для видимых строк '
          'плюс небольшой буфер. Открытие файла в 100 000 строк '
          'не создаёт 100 000 div-ов — только ~50 для видимой области.'))
    add(sp(3))
    add(code([
        '// Концептуально Monaco viewport manager:',
        'class ViewportManager {',
        '    private readonly OVERSCAN_LINES = 10;',
        '',
        '    getVisibleLines(scrollTop: number, viewportHeight: number): LineRange {',
        '        const firstLine = Math.floor(scrollTop / this.lineHeight);',
        '        const lastLine = Math.ceil(',
        '            (scrollTop + viewportHeight) / this.lineHeight',
        '        );',
        '        return {',
        '            start: Math.max(0, firstLine - this.OVERSCAN_LINES),',
        '            end: lastLine + this.OVERSCAN_LINES,',
        '        };',
        '    }',
        '    // При скролле: recycle DOM-элементы старых строк для новых',
        '    // = zero allocation scrolling',
        '}',
    ]))
    add(sp(3))
    add(p('Виртуализация viewport в Monaco: <b>getVisibleLines()</b> вычисляет диапазон видимых строк по scrollTop и высоте viewport. <b>OVERSCAN_LINES</b> добавляет буфер сверху и снизу, чтобы при быстром скролле не было мерцания. DOM-элементы старых строк переиспользуются для новых — zero allocation scrolling.'))

    add(sp(4))

    add(h3('Измерение шрифтов — почему CSS недостаточно'))
    add(p('Термин «кастомный рендеринг шрифтов» в контексте VS Code вводит в заблуждение: '
          'сам рендеринг глифов всегда выполнял Chromium/OS стандартными средствами. '
          'Что действительно кастомное — это <b>измерение символов</b>. '
          'Именно это отличает Monaco от обычного textarea и именно здесь кроются '
          'важные уроки для расширений работающих с позициями текста:'))
    add(sp(3))
    add(p('CSS font metrics (getBoundingClientRect, offsetWidth) дают неточные результаты '
          'для позиционирования курсора — разные ОС и шрифты дают дробные значения. '
          'Это приводит к "плыву" курсора в длинных строках и неверному '
          'выравниванию column guides.'))
    add(sp(3))
    add(p('Monaco измеряет реальную ширину каждого символа через '
          '<b>canvas.measureText()</b> и строит кэш-таблицу. '
          'Это даёт пиксельно-точное позиционирование курсора независимо от шрифта. '
          'Источник: <b>github.com/microsoft/vscode/blob/main/src/vs/editor/browser/config/fontMeasurements.ts</b>'))
    add(sp(3))
    add(code([
        '// Monaco: измерение при инициализации (упрощённо)',
        '// см. fontMeasurements.ts в репозитории VS Code',
        'class FontMeasurements {',
        '    private widthCache = new Map<string, number>();',
        '',
        '    measureChar(char: string, font: string): number {',
        '        const key = `${char}:${font}`;',
        '        if (this.widthCache.has(key)) {',
        '            return this.widthCache.get(key)!;',
        '            // Кэш: не измеряем повторно для одного и того же char+font',
        '        }',
        '        // Canvas measureText() точнее CSS layout engine',
        '        this.ctx.font = font;',
        '        const metrics = this.ctx.measureText(char);',
        '        const width = metrics.width;  // реальная ширина в px',
        '        this.widthCache.set(key, width);',
        '        return width;',
        '    }',
        '',
        '    // При смене шрифта в настройках — полный сброс и повторное измерение',
        '    onFontSettingsChanged(): void {',
        '        this.widthCache.clear();',
        '        this.remeasureAllVisible();',
        '    }',
        '}',
        '// Результат: позиция курсора точная до пикселя при любом шрифте',
    ]))
    add(sp(3))
    add(p('Кэширующий измеритель шрифтов: <b>measureChar()</b> использует canvas.measureText() вместо CSS layout для пиксельно-точной ширины символа. Результаты хранятся в Map по ключу char+font. <b>onFontSettingsChanged()</b> сбрасывает кэш и перемеряет всё — вызывается при смене шрифта в настройках.'))

    add(sp(4))

    add(h3('WebGPU renderer — следующий шаг (в разработке)'))
    add(p('В 2024 году команда VS Code начала работу над WebGPU-рендерером для Monaco. '
          'Аналогично тому, как xterm.js использует WebGL для терминала. '
          'Трекинг: <b>github.com/microsoft/vscode/issues/221145</b> '
          '(GPU accelerated canvas renderer, репозиторий vscode). '
          'Глифы рисуются в texture atlas на CPU, затем GPU батчами рендерит '
          'тысячи символов за один draw call.'))
    add(sp(3))
    add(tblh(['Рендерер', 'Производительность']))
    add(tbl2([
        ('DOM renderer',   'Baseline. Хорошо для обычного использования'),
        ('Canvas 2D',      '~2× быстрее DOM для больших файлов. Меньше layout thrashing'),
        ('WebGL (xterm)',  '~10× быстрее DOM. Используется в терминале уже сейчас'),
        ('WebGPU (future)','Потенциально ещё быстрее + compute shaders для highlight'),
    ]))
    add(sp(6))

    # ── 4. PROCESS SANDBOXING И CODE CACHING ─────────────────────────────────
    add(h1('4. Process Sandboxing: безопасность и производительность'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('В 2020–2023 годах команда VS Code провела многолетнюю работу по '
          '<b>sandbox-изоляции renderer process</b>. '
          'На первый взгляд это задача безопасности, но повлияло на архитектуру и скорость.'))
    add(sp(3))
    add(p('До sandboxing renderer имел прямой доступ к Node.js API (fork, файловая система). '
          'После — renderer стал «чистым» веб-контекстом. Все Node.js операции идут '
          'через MessagePort в shared/main process. '
          'Это принудило избавиться от лишних зависимостей и сделало IPC явным и измеримым.'))
    add(sp(4))

    add(h3('MessagePort вместо Node.js sockets'))
    add(p('До sandboxing: IPC через Node.js UNIX sockets. '
          'После: Web MessagePort API. '
          'Разница в том, что MessagePort не требует участия main process — '
          'два renderer могут общаться напрямую:'))
    add(sp(3))
    add(code([
        '// VS Code использует MessagePort для прямого IPC между процессами',
        '// (упрощённо):',
        '',
        '// Main process: создаёт канал',
        'const { port1, port2 } = new MessageChannel();',
        '// port1 остаётся в shared process, port2 передаётся renderer-у',
        '',
        '// Renderer: получает port2 через preload script',
        'window.addEventListener("message", event => {',
        '    if (event.data.type === "port") {',
        '        const port = event.ports[0];',
        '        // Прямая связь с shared process без main process!',
        '        port.postMessage({ type: "installExtension", id: "..." });',
        '    }',
        '});',
    ]))
    add(sp(3))
    add(p('Паттерн прямого IPC через <b>MessagePort</b>: main process создаёт MessageChannel и раздаёт порты участникам. Renderer получает порт через preload script и общается с shared process напрямую — без маршрутизации через main process. Это снижает latency IPC и разгружает main process.'))

    add(sp(6))

    # ── 5. LAZY LOADING ВСЕГО ─────────────────────────────────────────────
    add(h1('5. Ленивая загрузка — системная философия'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('VS Code не загружает ничего до тех пор, пока это не понадобится. '
          'Это применяется на всех уровнях:'))
    add(sp(3))
    add(tblh(['Уровень', 'Реализация']))
    add(tbl2([
        ('Расширения',
         'Activation Events: расширение не загружается до своего события. '
         '~200 установленных расширений → только 5-10 активны при старте'),
        ('Языковые фичи',
         'IntelliSense, diagnostics, hover — запрашиваются по требованию. '
         'TypeScript worker запускается при первом открытии .ts файла'),
        ('Панели UI',
         'SCM panel, Debug view, Extensions view — '
         'содержимое загружается при первом открытии'),
        ('Workbench модули',
         'Исторически AMD с dynamic require(). С ESM — '
         'dynamic import() для нечасто используемых функций'),
        ('Языковые пакеты',
         'NLS (локализация) — нужные строки загружаются лениво '
         'по файлам, а не весь пакет сразу'),
    ]))
    add(sp(4))
    add(box('Почему это важно для разработчика расширений',
        'Каждое расширение с activationEvents: ["*"] или onStartupFinished '
        'разрушает системную lazy-loading стратегию VS Code. '
        'Если все 200 установленных расширений активируются при старте — '
        'стартап превратится в 5-10 секунд. '
        'Правильные Activation Events — не просто «хорошая практика», '
        'это уважение к системной архитектуре.', 'warn'))
    add(sp(4))
    add(quote(
        'VS Code and Atom eventually became faster versions of their original '
        'Electron prototypes. These improvements are accidental. '
        "It's sheer luck they happened. "
        'If you want to build a really fast program, '
        'pay attention to the performance from the start.',
        'Никита Прокопов (tonsky)', 'Performance First, tonsky.me, 2020'
    ))
    add(sp(3))
    add(p('<b>Контекст:</b> Прокопов упоминает Atom как сравнение — Atom был первым '
          'редактором на Electron (GitHub, 2014) и был известен медленностью. '
          'VS Code вышел позже (Microsoft, 2015) на той же технологии, но с иным '
          'подходом к производительности. Atom закрыт в 2022 году. '
          'Прокопов пишет, что улучшения производительности в обоих случаях '
          'были «счастливой случайностью», а не изначально заложенной целью — '
          'и призывает делать производительность приоритетом с первого дня.'))
    add(sp(6))

    # ── 6. INCREMENTAL COMPUTATION ───────────────────────────────────────
    add(h1('6. Инкрементальные вычисления'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('VS Code нигде не пересчитывает с нуля то, что можно пересчитать инкрементально.'))
    add(sp(3))
    add(tblh(['Подсистема', 'Инкрементальность']))
    add(tbl2([
        ('TextModel (документ)',
         'Дерево отрезков (Piece Table): вставка/удаление O(log n), '
         'не перестраивает всю строку. '
         'История изменений — только дельты, не снапшоты'),
        ('Syntax Highlighting\n(TreeSitter / TM)',
         'При изменении строки: перепарсивание только затронутых диапазонов. '
         'Async tokenization — не блокирует набор текста'),
        ('TypeScript LSP\n(Incremental Parsing)',
         'TypeScript compiler API поддерживает incremental parsing: '
         'при изменении файла — только affected nodes пересчитываются'),
        ('Diagnostics',
         'DiagnosticCollection обновляется только для изменённых файлов. '
         'File watcher уведомляет о конкретных изменениях'),
        ('Поиск',
         'Full-text search индекс строится инкрементально: '
         'watchers отслеживают изменения и обновляют только затронутые файлы'),
    ]))
    add(sp(6))

    # ── 7. INPUT LATENCY ─────────────────────────────────────────────────
    add(h1('7. Input Latency: набор текста'))
    add(hl(C['blue']))
    add(sp(4))

    add(p('Самый чувствительный UX-показатель кодового редактора — '
          '<b>latency между нажатием клавиши и появлением символа</b>. '
          'VS Code добился здесь результатов, сравнимых с нативными редакторами.'))
    add(sp(3))

    add(h3('Input → Render pipeline'))
    add(p('Когда пользователь нажимает клавишу:'))
    add(sp(2))
    for step in [
        '<b>OS keydown event</b> → Chromium event handler (~0ms)',
        '<b>Monaco keyboard handler</b> → обновляет TextModel (~0.1ms)',
        '<b>View layout</b> → вычисляет изменения DOM (~0.5-1ms)',
        '<b>DOM mutation</b> → браузер перерисовывает затронутые строки (~1-2ms)',
        '<b>GPU composite</b> → кадр на экране (~0-16ms до vsync)',
    ]:
        add(bul(step))
    add(sp(3))
    add(p('Совокупная latency: <b>1-3ms</b> в типичном сценарии. '
          'Это ощутимо быстрее, чем у конкурирующих Electron-приложений '
          'которые тратят те же ~15ms только на JavaScript execution.'))
    add(sp(4))

    add(h3('Async decorations — не блокируем набор текста'))
    add(p('Inlay hints, code lens, inline completions — всё вычисляется '
          '<b>асинхронно после</b> обновления TextModel. '
          'Пользователь видит текст мгновенно, декорации появляются чуть позже.'))
    add(sp(3))
    add(p('VS Code не предоставляет встроенного debounce API. '
          'Стандартный паттерн — setTimeout/clearTimeout. '
          'Для серьёзных проектов используйте lodash.debounce или p-debounce:'))
    add(sp(3))
    add(code([
        '// Встроенного debounce в vscode API нет — используем setTimeout',
        '',
        '// ПЛОХО: блокирует набор текста',
        'vscode.workspace.onDidChangeTextDocument(e => {',
        '    const result = heavySync(e.document);',
        '    applyDecorations(result);',
        '});',
        '',
        '// ХОРОШО: debounce через setTimeout (стандартный JS)',
        'let timer: ReturnType<typeof setTimeout> | undefined;',
        '',
        'vscode.workspace.onDidChangeTextDocument(e => {',
        '    clearTimeout(timer);',
        '    timer = setTimeout(async () => {',
        '        const result = await heavyAsync(e.document);',
        '        applyDecorations(result);',
        '    }, 150);   // 150ms — баланс между отзывчивостью и нагрузкой',
        '});',
        '',
        '// ХОРОШО: с отменой через CancellationTokenSource (надёжнее)',
        'let cts = new vscode.CancellationTokenSource();',
        '',
        'vscode.workspace.onDidChangeTextDocument(e => {',
        '    cts.cancel();            // отменяем предыдущий',
        '    cts = new vscode.CancellationTokenSource();',
        '    const token = cts.token;',
        '    setTimeout(async () => {',
        '        if (token.isCancellationRequested) return;',
        '        const result = await heavyAsync(e.document, token);',
        '        if (!token.isCancellationRequested) applyDecorations(result);',
        '    }, 150);',
        '});',
        '',
        '// Также: es-toolkit (современная замена lodash, активно поддерживается)',
        '// npm install es-toolkit',
        '// import { debounce, throttle } from "es-toolkit";',
        '// const update = debounce(async (doc) => { ... }, 150);',
        '// es-toolkit: 2-3x быстрее lodash, 97% меньше, built-in TypeScript',
    ]))
    add(sp(3))
    add(p('Три подхода к обработке изменений документа: синхронный (блокирует набор текста — плохо), debounce через <b>setTimeout</b> (стандартный JS-паттерн, задержка 150ms), и debounce с <b>CancellationTokenSource</b> (надёжнее — отменяет предыдущий запрос при новом вводе). CancellationToken передаётся во все асинхронные провайдеры VS Code — проверяйте <b>token.isCancellationRequested</b> перед дорогостоящими операциями.'))
    add(sp(6))

    # ── 8. УРОКИ ДЛЯ РАСШИРЕНИЙ ─────────────────────────────────────────
    add(h1('8. Как применить это в своём расширении'))
    add(hl(C['blue']))
    add(sp(4))

    add(h2('Урок 1: Activation Events — копируй стратегию VS Code'))
    add(p('VS Code lazy-загружает всё. Расширение должно делать то же самое:'))
    add(sp(3))
    add(code([
        '// Плохо: активируемся при каждом запуске VS Code',
        '"activationEvents": ["*"]',
        '',
        '// Хорошо: только для своего языка',
        '"activationEvents": ["onLanguage:python"]',
        '',
        '// Лучше: workspaceContains — только если проект содержит наш файл',
        '"activationEvents": ["workspaceContains:**/pyproject.toml"]',
        '',
        '// Ещё лучше (VS Code 1.74+): объявить команды и View —',
        '// activation events генерируются автоматически',
        '// Явно нужны только нестандартные',
    ]))
    add(sp(3))
    add(p('Четыре уровня Activation Events от худшего к лучшему: <b>"*"</b> загружает расширение при каждом запуске, <b>onLanguage</b> — при открытии файла нужного языка, <b>workspaceContains</b> — только если в проекте есть конкретный файл. Начиная с VS Code 1.74 события генерируются автоматически из объявленных команд и View.'))

    add(sp(6))

    add(h2('Урок 2: Бандли как VS Code — один файл'))
    add(p('VS Code bundle — один большой файл, не тысяча маленьких. '
          'Причина: V8 code cache работает эффективнее с одним большим файлом. '
          'Overhead на require() платится один раз при загрузке. '
          'Для расширений — то же самое:'))
    add(sp(3))
    add(code([
        '// esbuild.js — правильная конфигурация',
        'await esbuild.context({',
        '    entryPoints: ["src/extension.ts"],',
        '    bundle: true,           // все зависимости в один файл',
        '    minify: production,     // меньше файл = быстрее parse',
        '    platform: "node",',
        '    outfile: "dist/extension.js",  // ОДИН файл, не папка',
        '    external: ["vscode"],   // vscode не включаем — загрузится runtime',
        '});',
        '',
        '// package.json: main должен указывать на bundled файл',
        '"main": "./dist/extension.js"  // не ./out/extension.js (unbundled)',
    ]))
    add(sp(3))
    add(p('Конфигурация <b>esbuild</b> для бандлинга расширения в один файл: bundle объединяет все зависимости, minify уменьшает размер для production, <b>external: ["vscode"]</b> исключает VS Code API — он предоставляется runtime. Поле <b>main</b> в package.json должно указывать на bundled файл в dist/, а не на исходники в out/.'))

    add(sp(6))

    add(h2('Урок 3: Incremental updates — не пересчитывай всё'))
    add(p('VS Code обновляет только то, что изменилось. '
          'Расширение должно делать то же — не сканировать весь workspace '
          'при каждом изменении файла:'))
    add(sp(3))
    add(code([
        '// Плохо: полное сканирование при каждом изменении',
        'vscode.workspace.onDidSaveTextDocument(async doc => {',
        '    const allFiles = await vscode.workspace.findFiles("**/*.ts");',
        '    await rebuildIndex(allFiles);  // 500ms каждый раз',
        '});',
        '',
        '// Хорошо: инкрементальное обновление только изменённого файла',
        'const indexCache = new Map<string, IndexEntry>();',
        '',
        'vscode.workspace.onDidSaveTextDocument(async doc => {',
        '    if (doc.languageId !== "typescript") return;',
        '    // Обновляем только этот файл',
        '    indexCache.set(doc.uri.toString(), await indexFile(doc));',
        '    onIndexUpdated.fire(doc.uri);',
        '});',
        '',
        '// FileSystemWatcher для внешних изменений',
        'const watcher = vscode.workspace.createFileSystemWatcher("**/*.ts");',
        'watcher.onDidChange(uri => indexCache.delete(uri.toString()));',
        'context.subscriptions.push(watcher);',
    ]))
    add(sp(3))
    add(p('Паттерн инкрементального индекса: вместо полного сканирования workspace при каждом сохранении — обновление только изменённого файла в <b>Map-кэше</b>. <b>onDidSaveTextDocument</b> обновляет запись для конкретного файла, <b>FileSystemWatcher</b> инвалидирует кэш при внешних изменениях (git pull, переключение ветки).'))

    add(sp(6))

    add(h2('Урок 4: Async decorations — не блокируй курсор'))
    add(p('VS Code паттерн: пользователь видит символ мгновенно, '
          'декорации появляются через ~150ms. Копируй этот паттерн:'))
    add(sp(3))
    add(quote(
        'When they crossed that 100ms barrier, a qualitative change happened. '
        'People changed their views of a tool from something they have to cope with '
        "to something that's fun, valuable, and eventually became their second nature. "
        'Speed is a feature.',
        'Никита Прокопов (tonsky)', 'Speed is a feature, tonsky.me, 2018'
    ))
    add(sp(4))
    add(code([
        'let decorationTimer: NodeJS.Timeout | null = null;',
        'let cancelled = false;',
        '',
        'vscode.window.onDidChangeTextEditorSelection(event => {',
        '    // Отменяем предыдущий запрос',
        '    if (decorationTimer) clearTimeout(decorationTimer);',
        '    cancelled = true;',
        '',
        '    decorationTimer = setTimeout(() => {',
        '        cancelled = false;',
        '        computeDecorations(event.textEditor).then(ranges => {',
        '            if (!cancelled) {',
        '                event.textEditor.setDecorations(decorationType, ranges);',
        '            }',
        '        });',
        '    }, 150);  // 150ms debounce — баланс между responsiveness и CPU',
        '});',
    ]))
    add(sp(3))
    add(p('Debounce-паттерн для декораций: при смене выделения отменяется предыдущий запрос через <b>clearTimeout</b>, новый запускается с задержкой 150ms. Флаг <b>cancelled</b> предотвращает применение устаревших результатов — если пользователь успел переместить курсор, старые декорации не применятся.'))

    add(sp(6))

    add(h2('Урок 5: Measure first — не оптимизируй вслепую'))
    add(p('VS Code измеряет всё: время до первого кадра, latency каждой операции, '
          'размер bundle. Делай то же для своего расширения:'))
    add(sp(3))
    add(code([
        '// Измерение времени активации',
        'export async function activate(context: vscode.ExtensionContext) {',
        '    const t0 = Date.now();',
        '',
        '    await doInitialization();',
        '',
        '    const ms = Date.now() - t0;',
        '    if (ms > 100) {',
        '        // Логируем в Output Channel для диагностики',
        '        output.appendLine(`[WARN] Slow activation: ${ms}ms`);',
        '    }',
        '    // Отправляем в телеметрию если есть',
        '    reporter.sendTelemetryEvent("activation", {}, { activationMs: ms });',
        '}',
        '',
        '// Developer: Show Running Extensions — встроенный профайлер',
        '// Показывает время активации каждого расширения',
        '// Используй Developer: Open Process Explorer для CPU/memory',
    ]))
    add(sp(3))
    add(p('Измерение времени активации расширения: <b>Date.now()</b> до и после инициализации, логирование в Output Channel при превышении порога (100ms). Встроенная команда <b>Developer: Show Running Extensions</b> показывает время активации всех расширений, <b>Process Explorer</b> — потребление CPU и памяти.'))

    add(sp(4))

    add(h2('Урок 6: Worker для тяжёлых вычислений'))
    add(p('VS Code выносит TypeScript compiler, поиск и другие тяжёлые операции '
          'в отдельные процессы/workers. '
          'Расширение может делать то же через Node.js worker_threads:'))
    add(sp(3))
    add(code([
        '// Тяжёлые вычисления — в worker thread',
        'import { Worker, isMainThread, parentPort } from "worker_threads";',
        '',
        '// src/heavy-worker.ts',
        'if (!isMainThread) {',
        '    parentPort!.on("message", async (data) => {',
        '        const result = await doHeavyComputation(data);',
        '        parentPort!.postMessage(result);',
        '    });',
        '}',
        '',
        '// src/extension.ts',
        'const worker = new Worker(',
        '    path.join(context.extensionPath, "dist", "heavy-worker.js")',
        ');',
        '',
        'function runHeavyTask(input: any): Promise<any> {',
        '    return new Promise((resolve, reject) => {',
        '        worker.once("message", resolve);',
        '        worker.once("error", reject);',
        '        worker.postMessage(input);',
        '    });',
        '}',
        '',
        '// Extension Host = отдельный процесс (уже хорошо),',
        '// но worker внутри него = ещё один уровень изоляции',
        '// для CPU-intensive операций',
    ]))
    add(sp(3))
    add(p('Вынос тяжёлых вычислений в <b>worker_threads</b>: worker слушает сообщения через <b>parentPort</b>, выполняет задачу и отправляет результат обратно. Основной поток создаёт Worker из bundled-файла и оборачивает коммуникацию в Promise. Extension Host уже работает в отдельном процессе, но worker внутри него добавляет ещё один уровень изоляции для CPU-intensive задач.'))

    add(sp(6))

    add(h2('Реальные числа: хорошо и плохо'))
    add(p('Данные из публичных анализов производительности расширений VS Code '
          '(источник: freecodecamp.org/news/optimize-vscode-performance-best-extensions):'))
    add(sp(3))
    add(tblh(['Расширение', 'Время активации / подход']))
    add(tbl2([
        ('GitLens (~6.5M установок)',
         '35ms — несмотря на сложный функционал. '
         'Секрет: тяжёлые операции (git blame, граф) вычисляются лениво, '
         'только при первом открытии файла, не при старте'),
        ('rust-analyzer',
         'Сервер запускается асинхронно — VS Code открывается немедленно. '
         'Прогресс-бар в Status Bar показывает индексирование в фоне. '
         'Набор текста мгновенный пока LSP ещё загружается'),
        ('Некий анализируемый extension',
         '2513ms — activationEvents:["*"], нет бандлинга (2.5MB файлов). '
         'Это 2.5 секунды добавляется к каждому запуску VS Code. '
         'У пользователя с 10 такими расширениями — старт занимает 30+ секунд'),
        ('Целевые показатели',
         '< 50ms — отлично (как rust-analyzer). '
         '< 100ms — хорошо. '
         '< 300ms — приемлемо. '
         '> 500ms — нужна оптимизация: бандлинг, lazy loading. '
         'Источник: nicoespeon.com/en/2019/11/fix-vscode-extension-performance-issue/'),
    ]))
    add(sp(6))

    # ── ИТОГОВАЯ ТАБЛИЦА ─────────────────────────────────────────────────
    add(h1('Итог: шпаргалка производительности'))
    add(hl(C['blue']))
    add(sp(4))

    add(tblh(['Техника VS Code', 'Аналог для расширения']))
    add(tbl2([
        ('Lazy-load расширений через Activation Events',
         'Правильные activationEvents. Никогда "*"'),
        ('V8 Code Caching / один большой bundle',
         'esbuild bundle в один файл. minify: true в production'),
        ('AMD → ESM (+10% startup)',
         'Пока CJS. Следить за github.com/microsoft/vscode/issues/130367'),
        ('Виртуализация строк в Monaco',
         'Виртуализировать длинные списки в Webview (react-virtual и аналоги)'),
        ('Async tokenization / не блокировать курсор',
         'Debounce 100-200ms для тяжёлых операций в onDidChangeTextDocument'),
        ('Incremental TypeScript compiler',
         'Инвалидировать только изменённые файлы в кэше, не rebuild всё'),
        ('MessagePort IPC без main process',
         'Worker threads для CPU-intensive задач в расширении'),
        ('Measure first: время до первого кадра',
         'Логировать время activate() и отправлять в телеметрию'),
        ('UtilityProcess с V8 sandbox',
         'С VS Code 1.94 Extension Host работает в UtilityProcess с включённым V8 sandbox. '
         'Native addons (.node-файлы, C++/Rust через N-API) выполняются вне этой изоляции '
         'и имеют прямой доступ к памяти процесса — это потенциальная уязвимость. '
         'Кроме того, native addons компилируются под конкретную версию Electron (не Node.js) '
         'и ломаются при каждом обновлении VS Code. '
         'Аддоны использующие external array buffers несовместимы с V8 sandbox и упадут. '
         'Если нужен native addon — используйте napi_create_buffer_copy вместо external buffers, '
         'или вынесите аддон в дочерний процесс через worker_threads. '
         'Источник: code.visualstudio.com/updates/v1_94 (раздел Remove custom allocator in the desktop app)'),
    ]))
    add(sp(4))

    add(quote(
        'Performance is not a feature you add at the end. '
        'It\'s a consequence of every decision you make during development. '
        'VS Code\'s performance comes from a decade of small, consistent choices.',
        'Benjamin Pasero', 'VS Code Core Team, Microsoft — автор блога про sandboxing'
    ))
    add(pb())

    return A


if __name__ == '__main__':
    print(f'Performance chapter: {len(build_perf_chapter())} elements')
