"""The starter practical, "Four ways to use R", done as a student would do it: each step of each chapter, then a check
that the step ticked itself. (Shiny's step needs the service worker: see t_shiny.py.)"""
import time
from h import Page, check, done

p = Page(width=1500, height=950)
p.open('index.html')
HOME = '/home/user'


def chapter(cid):
    p.js('(c) => MG.app.showChapter(c, true)', cid)
    time.sleep(0.4)


def ticked(*ids):
    st = p.js('() => MG.app.state.tasks')
    missing = [i for i in ids if not st.get(i)]
    check(not missing, 'ticked: ' + ', '.join(ids) + (f' – NOT {missing}' if missing else ''))


def click(sel):
    p.js('(s) => document.querySelector(s).click()', sel)


def rcon(code, timeout=60000):
    p.js('(c) => MG.app.rcon.run(c)', code)
    time.sleep(0.4)
    p.wait('() => MG.app.rcon.S.idle', timeout=timeout)


def rs(code, timeout=120000):
    p.js('(c) => MG.app.rstudio.consoleRun(c)', code)
    time.sleep(0.4)
    p.wait('() => MG.app.rstudio.S.idle && !MG.app.rstudio.capture && !MG.app.rstudio.chunkQueue.length', timeout=timeout)


def rs_idle(timeout=120000):
    time.sleep(0.4)
    p.wait('() => MG.app.rstudio.S.idle && !MG.app.rstudio.capture && !MG.app.rstudio.chunkQueue.length', timeout=timeout)


def answer(label):
    """the main button of a dialog"""
    p.wait('(l) => Array.from(document.querySelectorAll(".modal .btn.primary")).some((b) => b.textContent.trim() === l)', arg=label, timeout=60000)
    p.js('(l) => Array.from(document.querySelectorAll(".modal .btn.primary")).find((b) => b.textContent.trim() === l).click()', label)


def save_as(name):
    p.js('() => { MG.app.rstudio.saveAs(); }')
    p.wait('() => document.querySelector(".rs-filedlg input[type=text]")')
    p.js('(n) => { const i = document.querySelector(".rs-filedlg input[type=text]"); i.value = n; document.querySelector(".rs-filedlg .btn.primary").click(); }', name)
    p.wait('(n) => MG.app.rstudio.cur.path === "/home/user/" + n && !MG.app.rstudio.cur.dirty', arg=name)


def term(line, timeout=120000):
    return p.js('(l) => MG.app.term.exec(l)', line)


# ---------------------------------------------------------------- 0 Start here
chapter('start')
click('#start [data-bench="console"]')
p.wait('() => MG.app.rcon && MG.app.rcon.S && MG.app.rcon.S.idle', timeout=120000)
rcon('1 + 1')
p.js('() => MG.app.showWorkbench("editor")')
p.wait('() => MG.app.editor')
p.js('() => MG.app.editor.openFile("/home/user/data/penguins.csv")')
time.sleep(1)
ticked('s-console', 's-type', 's-files')

# ---------------------------------------------------------------- 1 The R console
chapter('console')
p.wait('() => MG.app.currentBench === "console"')
for c in ['x <- c(3, 8, 1)', 'mean(x)', 'median(x)']:
    rcon(c)
p.js('() => MG.app.rcon.run("sum(x")')
time.sleep(0.5)
rcon(')')
for c in ['head(penguins)', 'summary(penguins$body_mass)', 'View(penguins)', 'plot(body_mass ~ flipper_len, data = penguins)', '?mean']:
    rcon(c)
time.sleep(0.8)
p.js('() => MG.app.rcon.run("q()")')
p.wait('() => MG.app.rcon.S.prompt && MG.app.rcon.S.prompt.startsWith("Save workspace image?")', timeout=30000)
p.js('() => MG.app.rcon.run("y")')
p.wait('() => MG.app.rcon.S.state === "ended"', timeout=30000)
time.sleep(0.5)
click('.rc-dead button')
p.wait('() => MG.app.rcon.S.idle', timeout=120000)
check('[Previously saved workspace restored]' in p.js('() => MG.app.rcon.cv.text()'), 'the new R restored the workspace')
rcon('x')
ticked('c-calc', 'c-up', 'c-plus', 'c-head', 'c-view', 'c-plot', 'c-help', 'c-q', 'c-again', 'c-x')

# ---------------------------------------------------------------- 2 Scripts in RStudio
chapter('rstudio')
p.wait('() => MG.app.rstudio && MG.app.rstudio.S && MG.app.rstudio.S.idle', timeout=120000)
click('#rstudio .codefile [data-file-create]')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.path === "/home/user/scripts/penguins.R"')
# Ctrl+Enter from the read.csv line to the end
p.js('() => { const R = MG.app.rstudio; R.cm.setCursor({ line: 1, ch: 0 }); }')
for _ in range(6):
    p.js('() => MG.app.rstudio.runCurrent()')
    rs_idle()
time.sleep(0.8)
rs('View(penguins)')
p.js('() => MG.app.rstudio.restart()')
time.sleep(1)
rs_idle()
p.js('() => MG.app.rstudio.activate(MG.app.rstudio.docs.find((d) => d.path && d.path.endsWith("penguins.R")))')
p.js('() => MG.app.rstudio.sourceDoc(false)')
rs_idle()
p.js('() => { const d = MG.app.rstudio.cur.cmDoc; d.replaceRange("table(penguins$species)\\n", { line: d.lineCount(), ch: 0 }); }')
p.js('() => MG.app.rstudio.save()')
time.sleep(0.5)
# Import Dataset ▸ From Excel
p.js('() => MG.app.rstudio.importDialog("excel", "/home/user/data/penguins.xlsx")')
p.wait('() => document.querySelector(".rs-import .preview table")')
p.js('() => Array.from(document.querySelectorAll(".rs-import .btn.primary")).find((b) => b.textContent.trim() === "Import").click()')
answer('Install')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.type === "data"', timeout=300000)
rs_idle()
ticked('r-make', 'r-line', 'r-more', 'r-env', 'r-restart', 'r-source', 'r-edit', 'r-import')

# ---------------------------------------------------------------- 3 Documents
chapter('docs')
p.js('() => MG.app.rstudio.newDocDialog("rmd")')
p.wait('() => document.querySelector(".rs-newdoc input")')
p.js('() => { const i = document.querySelectorAll(".rs-newdoc input[type=text]"); i[0].value = "Penguin report"; i[1].value = "Ada Lovelace"; }')
p.js('() => document.querySelector(".rs-newdoc .btn.primary").click()')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.kind === "rmd"')
save_as('reports/penguins.Rmd')
p.js('() => { const R = MG.app.rstudio; R.runChunks(R.cur, [MG.Knit.chunks(R.cur.cmDoc.getValue())[1]]); }')
rs_idle()
p.js('() => { window.KN = []; MG.bus.on("rstudio:knit", (d) => KN.push(d)); MG.app.rstudio.knit(); }')
answer('Install')
p.wait('() => KN.length', timeout=300000)
check(p.js('() => MG.app.fs.exists("/home/user/reports/penguins.html")'), 'the report was knitted')
# colours in the Console, used in a chunk, then knitted: it fails
p.js('() => document.querySelector("#docs [data-rs-run]").click()')
rs_idle()
p.js('''() => { const R = MG.app.rstudio, d = R.cur.cmDoc; d.replaceRange("\\n```{r}\\nbarplot(table(penguins$species), col = penguin_colours)\\n```\\n", { line: d.lineCount(), ch: 0 }); }''')
time.sleep(0.5)
p.js('() => { const R = MG.app.rstudio, cs = MG.Knit.chunks(R.cur.cmDoc.getValue()); R.runChunks(R.cur, [cs[cs.length - 1]]); }')
rs_idle()
p.js('() => { KN.length = 0; MG.app.rstudio.knit(); }')
p.wait('() => KN.length', timeout=120000)
check(p.js('() => KN[0].failed === true'), 'knitting stopped: penguin_colours is not in the new R')
check("object 'penguin_colours' not found" in p.js('() => MG.app.rstudio.jobLog.textContent'), 'Background Jobs says why')
# an R Notebook and a Quarto document
p.js('() => MG.app.rstudio.newDocDialog("notebook")')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.kind === "notebook"')
save_as('reports/notes.Rmd')
p.js('() => { const R = MG.app.rstudio; R.runChunks(R.cur, MG.Knit.chunks(R.cur.cmDoc.getValue())); }')
rs_idle()
p.js('() => MG.app.rstudio.preview()')
time.sleep(0.6)
p.js('() => MG.app.rstudio.newDocDialog("qmd")')
p.wait('() => document.querySelector(".rs-newdoc input")')
p.js('() => document.querySelector(".rs-newdoc .btn.primary").click()')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.kind === "qmd"')
save_as('reports/quarto.qmd')
p.js('() => { KN.length = 0; MG.app.rstudio.knit(); }')
p.wait('() => KN.length', timeout=120000)
ticked('d-new', 'd-save', 'd-chunk', 'd-knit', 'd-obj', 'd-use', 'd-fail', 'd-rnb', 'd-qmd')

# ---------------------------------------------------------------- 4 Jupyter notebooks
chapter('notebook')
click('#notebook [data-bench="notebook"]')
p.wait('() => MG.app.nbApp && MG.app.nbApp.view', timeout=60000)
p.wait('() => MG.kernels.peek("r") && MG.kernels.peek("r").state === "ready"', timeout=180000)


def cell(code, timeout=60000):
    p.js('''(code) => {
      const v = MG.app.nbApp.view;
      const c = v.addCell({ type: 'code', source: code }, { after: v.cells[v.cells.length - 1] });
      window.T = { c, done: false };
      v.runCell(c).then(() => (T.done = true));
    }''', code)
    p.wait('() => T.done', timeout=timeout)


cell('head(penguins)')
cell('hist(penguins$flipper_len, main = "Flipper length", xlab = "mm")')
p.js('''() => { const v = MG.app.nbApp.view; v.addCell({ type: 'markdown', source: 'Most flippers are 185–215 mm long.' }, { after: v.cells[v.cells.length - 1] }); MG.app.nbApp.view.saveNow(true); }''')
cell('n <- 10')
cell('n * 2')
p.js('() => MG.app.nbApp.restart(true).then(() => true)')
p.wait('() => MG.kernels.peek("r").state === "ready" && !MG.app.nbApp.running', timeout=180000)
p.js('() => MG.app.nbApp.downloadIpynb()')
time.sleep(1)
ticked('n-open', 'n-table', 'n-plot', 'n-text', 'n-a', 'n-fix', 'n-down')

# ---------------------------------------------------------------- 5 R in the terminal
chapter('terminal')
click('#terminal [data-bench="terminal"]')
p.wait('() => MG.app.term')
term('ls scripts')
check(term('Rscript scripts/penguins.R') == 0, 'Rscript runs the script')
click('#terminal .codefile [data-file-create]')
time.sleep(0.6)
p.js('() => MG.app.showWorkbench("terminal")')
term('Rscript scripts/count.R Gentoo')
check('Gentoo : 124 penguins' in p.js('() => MG.app.term.outEl.textContent'), 'count.R counts the Gentoo penguins')
term('for s in Adelie Chinstrap Gentoo; do Rscript scripts/count.R $s; done')
term('Rscript -e \'mean(no_such_thing)\'; echo "exit status: $?"')
check('exit status: 1' in p.js('() => MG.app.term.outEl.textContent'), 'the exit status of the failed script is 1')
term('R CMD BATCH scripts/penguins.R')
p.js('() => { window._rt = MG.app.term.exec("R -q"); }')
p.wait('() => MG.app.term.program && MG.app.term.program.prompt === "> "', timeout=120000)
p.js('() => { const t = MG.app.term; t.input.value = "q(\'no\')"; t.input.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true })); }')
p.wait('() => !MG.app.term.program', timeout=30000)
ticked('t-open', 't-run', 't-make', 't-arg', 't-loop', 't-err', 't-batch', 't-r')

# ---------------------------------------------------------------- the Help button at the top
p.p.click('#helpBtn')
p.wait('() => document.querySelector(".modal h3") && document.querySelector(".modal h3").textContent === "How this page works"', timeout=5000)
htext = p.js('() => document.querySelector(".modal").textContent')
check('Each of them is an R of its own' in htext and 'personal or patient data' in htext, 'Help shows how the page works')
p.p.keyboard.press('Escape')
p.wait('() => !document.querySelector(".modal")', timeout=5000)

errs = [e for e in p.errors if "'serviceWorker' property" not in e]
print('errors:', errs[:5])
check(not errs, 'no errors in the page')
print('progress:', p.js('() => document.querySelector(".progress-label").textContent'))
p.close()
done()
