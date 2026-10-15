"""The RStudio tab, part 2: R Markdown from the New File dialog, knitting (knitr and markdown are installed when they
are first needed), an R Notebook and its .nb.html, Quarto, Import Dataset (readr, readxl)."""
import sys, time
from h import Page, check, done

p = Page(width=1500, height=950)
p.open('index.html')
p.js('() => { window.EV = []; for (const t of ["rstudio:knit", "rstudio:chunk", "rstudio:import", "rstudio:preview", "knit:done"]) MG.bus.on(t, (d) => EV.push(Object.assign({ t }, d))); }')
p.js('() => MG.app.showWorkbench("rstudio")')
p.wait('() => MG.app.rstudio && MG.app.rstudio.S && MG.app.rstudio.S.idle', timeout=120000)
print('R is ready')

def idle(timeout=60000):
    time.sleep(0.3)
    p.wait('() => MG.app.rstudio.S.idle && !MG.app.rstudio.capture && !MG.app.rstudio.chunkQueue.length', timeout=timeout)

def click(sel, text=None):
    p.wait('([s, t]) => Array.from(document.querySelectorAll(s)).some((b) => !t || b.textContent.trim() === t)', arg=[sel, text])
    p.js('([s, t]) => Array.from(document.querySelectorAll(s)).find((b) => !t || b.textContent.trim() === t).click()', [sel, text])

def save_as(name):
    p.js('() => { MG.app.rstudio.saveAs(); }')
    p.wait('() => document.querySelector(".rs-filedlg input[type=text]")')
    p.js('(n) => { const i = document.querySelector(".rs-filedlg input[type=text]"); i.value = n; document.querySelector(".rs-filedlg .btn.primary").click(); }', name)
    p.wait('(n) => MG.app.rstudio.cur.path === "/home/user/" + n && !MG.app.rstudio.cur.dirty', arg=name)

check(p.js('() => MG.app.fs.exists("/home/user/data/penguins.csv") && MG.app.fs.exists("/home/user/data/penguins.xlsx")'), 'the starter data are in ~/data')

# ---- New R Markdown (the dialog), Knit
p.js('() => MG.app.rstudio.newDocDialog("rmd")')
p.wait('() => document.querySelector(".rs-newdoc input")')
p.js('() => { const i = document.querySelectorAll(".rs-newdoc input[type=text]"); i[0].value = "Penguin report"; i[1].value = "Ada Lovelace"; }')
click('.rs-newdoc .btn.primary')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.kind === "rmd"')
text = p.js('() => MG.app.rstudio.cur.cmDoc.getValue()')
check('title: "Penguin report"' in text and 'author: "Ada Lovelace"' in text and 'output: html_document' in text, 'the new R Markdown has the title and author')
save_as('report.Rmd')
p.js('() => { MG.app.rstudio.knit(); }')
click('.modal .btn.primary', 'Install')
t0 = time.time()
p.wait('() => EV.some((e) => e.t === "rstudio:knit")', timeout=300000)
print(f'knitted (with installing) in {time.time() - t0:.1f}s')
ev = p.js('() => EV.filter((e) => e.t === "rstudio:knit")')
check(ev and ev[0].get('output') == '/home/user/report.html', 'Knit writes ~/report.html: ' + str(ev))
log = p.js('() => MG.app.rstudio.jobLog.textContent')
check('Output created: report.html' in log, 'the Background Jobs tab shows the knitting')
html = p.js('() => MG.app.fs.get("/home/user/report.html").text')
check('<h1 class="title toc-ignore">Penguin report</h1>' in html and 'Ada Lovelace' in html, 'the page has the title and author')
check('data:image/png;base64' in html, 'the plot is in the page')
check('Min.' in html and 'knitr::opts_chunk' not in html, 'the output is there, the setup chunk is not shown')
check(p.js('() => MG.app.rstudio.panes.files.cur') == 'viewer' and 'Penguin report' in p.js('() => MG.app.rstudio.viewerBox.querySelector("iframe").srcdoc'), 'the Viewer shows the page')
p.shot('rs-10-knit')
# an error in a knitted document: not found in the new R
p.js('''() => { const d = MG.app.rstudio.cur.cmDoc; d.replaceRange('\\n```{r}\\nmean(only_in_console)\\n```\\n', {line: d.lineCount(), ch: 0}); }''')
p.js('() => MG.app.rstudio.consoleRun("only_in_console <- 1:3")')
idle()
p.js('() => { EV.length = 0; MG.app.rstudio.knit(); }')
p.wait('() => EV.some((e) => e.t === "rstudio:knit")', timeout=120000)
log = p.js('() => MG.app.rstudio.jobLog.textContent')
check("object 'only_in_console' not found" in log and 'Execution halted' in log, 'an object made in the console is not there when knitting: ' + log[-300:].replace('\n', ' | '))

# ---- an R Notebook: chunks run inline; saving writes the .nb.html
p.js('() => MG.app.rstudio.newDocDialog("notebook")')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.kind === "notebook"')
save_as('notes.Rmd')
p.js('() => { const R = MG.app.rstudio; R.runChunks(R.cur, MG.Knit.chunks(R.cur.cmDoc.getValue())); }')
idle()
p.js('() => MG.app.rstudio.save()')
nb = p.js('() => MG.app.fs.exists("/home/user/notes.nb.html") && MG.app.fs.get("/home/user/notes.nb.html").text')
check(bool(nb) and 'Min.' in nb and 'rmd-source-code' in nb, 'saving the notebook writes notes.nb.html with the outputs')
p.js('() => MG.app.rstudio.preview()')
time.sleep(0.5)
check('notes' in p.js('() => MG.app.rstudio.viewerTitle.textContent'), 'Preview shows the .nb.html')

# ---- Quarto: Render
p.js('() => MG.app.rstudio.newDocDialog("qmd")')
p.wait('() => document.querySelector(".rs-newdoc input")')
click('.rs-newdoc .btn.primary')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.kind === "qmd"')
save_as('quarto.qmd')
p.js('() => { EV.length = 0; MG.app.rstudio.knit(); }')
p.wait('() => EV.some((e) => e.t === "rstudio:knit")', timeout=120000)
q = p.js('() => MG.app.fs.exists("/home/user/quarto.html") && MG.app.fs.get("/home/user/quarto.html").text')
check(bool(q) and 'title-block-header' in q and '#&gt;' in q, 'Render writes a Quarto-like page (#> before output)')
check(bool(q) and 'flipper_len' not in q and '<img' in q, '#| echo: false hides the code of a chunk, and its plot is there')

# ---- Import Dataset: readr
p.js('() => MG.app.rstudio.importDialog("readr", "/home/user/data/penguins.csv")')
p.wait('() => document.querySelector(".rs-import .preview table")')
hdr = p.js('() => Array.from(document.querySelectorAll(".rs-import .preview th")).map((t) => t.textContent)')
check(hdr[:3] == ['species(chr)', 'island(chr)', 'bill_len(dbl)'], 'the preview shows the columns and their types: ' + str(hdr[:4]))
code = p.js('() => document.querySelector(".rs-import pre.code").textContent')
check(code == 'library(readr)\npenguins <- read_csv("data/penguins.csv")\nView(penguins)', 'the code preview: ' + code)
p.shot('rs-11-import')
click('.rs-import .btn.primary', 'Import')
click('.modal .btn.primary', 'Install')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.type === "data" && MG.app.rstudio.cur.name === "penguins"', timeout=300000)
idle()
check('Showing 344 of 344 entries' in p.js('() => MG.app.rstudio.cur.view.textContent'), 'readr imported the data, and View() shows it')
env = p.js('() => MG.app.rstudio.envList.textContent')
check('344 obs. of 8 variables' in env, 'penguins is in the Environment')

# ---- Import Dataset: Excel
p.js('() => MG.app.rstudio.importDialog("excel", "/home/user/data/penguins.xlsx")')
p.wait('() => document.querySelector(".rs-import .preview table")')
sheets = p.js('() => Array.from(document.querySelectorAll(".rs-import select[aria-label=Sheet] option")).map((o) => o.value)')
check(sheets == ['', 'penguins', 'about'], 'the sheets of the workbook: ' + str(sheets))
hdr = p.js('() => Array.from(document.querySelectorAll(".rs-import .preview th")).map((t) => t.textContent)')
check(hdr[:3] == ['species(chr)', 'island(chr)', 'bill_len(dbl)'], 'the Excel preview: ' + str(hdr[:4]))
p.js('() => { const s = document.querySelector(".rs-import select[aria-label=Sheet]"); s.value = "about"; s.dispatchEvent(new Event("change")); }')
time.sleep(0.5)
code = p.js('() => document.querySelector(".rs-import pre.code").textContent')
check('read_excel("data/penguins.xlsx", sheet = "about")' in code, 'choosing a sheet: ' + code)
click('.rs-import .btn', 'Cancel')

# (Playwright's blocking of service workers reads navigator.serviceWorker in every frame: in the Viewer's sandboxed
# frames that is an error of the test's browser, not of the page)
errs = [e for e in p.errors if "'serviceWorker' property" not in e]
print('errors:', errs[:5])
check(not errs, 'no errors in the page')
p.close()
done()
