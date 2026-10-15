"""The RStudio tab: the four panes, Source (scripts, R Markdown chunks with their output under them, knitting,
notebooks), the Environment, Plots, View(), Help, Import Dataset."""
import sys, time
from h import Page, check, done

p = Page(width=1500, height=950)
p.open('index.html')
p.js('() => MG.app.showWorkbench("rstudio")')
p.wait('() => MG.app.rstudio && MG.app.rstudio.S && MG.app.rstudio.S.idle', timeout=120000)
A = '() => MG.app.rstudio'
print('R is ready')
p.shot('rs-01-start')

def idle(timeout=60000):
    time.sleep(0.3)
    p.wait('() => MG.app.rstudio.S.idle && !MG.app.rstudio.capture && !MG.app.rstudio.chunkQueue.length', timeout=timeout)

def console():
    return p.js('() => MG.app.rstudio.cv.text()')

# ---- the console
check('R version 4.6' in console(), 'the console shows R\'s banner')
p.js('() => MG.app.rstudio.consoleRun("x <- c(5, 3, 8)\\nmean(x)")')
idle()
check('[1] 5.333333' in console(), 'code run in the console prints there')
try:
    p.wait('() => MG.app.rstudio.envList.textContent.includes("num [1:3] 5 3 8")', timeout=10000)
except Exception:
    pass
env = p.js('() => MG.app.rstudio.envList.textContent')
check('x' in env and 'num [1:3] 5 3 8' in env, 'the Environment lists x: ' + env[:80])
hist = p.js('() => MG.app.rstudio.history.slice(-2)')
check(hist == ['x <- c(5, 3, 8)', 'mean(x)'], 'the History has the commands')

# ---- an R script: Run (Ctrl+Enter) runs the statement at the cursor, over several lines
p.js('''() => MG.app.rstudio.newDoc('r', 'y <- c(1,\\n       2,\\n       3)\\n\\nsum(y)\\nplot(y)\\n')''')
check(p.js('() => MG.app.rstudio.cur.name') == 'Untitled1', 'a new script is Untitled1')
check(p.js('() => MG.app.rstudio.cur.dirty') is True, 'a new script with text is unsaved')
p.js('() => { const R = MG.app.rstudio; R.cm.setCursor({line: 1, ch: 3}); R.runCurrent(); }')
idle()
c = console()
check('> y <- c(1,\n+        2,\n+        3)' in c, 'Run on the middle line runs the whole statement')
check(p.js('() => MG.app.rstudio.cm.getCursor().line') == 4, 'the cursor goes to the next line with code')
p.js('() => MG.app.rstudio.runCurrent()')
idle()
check('[1] 6' in console(), 'sum(y) printed 6')
p.js('() => MG.app.rstudio.runCurrent()')
idle()
time.sleep(0.5)
check(p.js('() => MG.app.rstudio.plots.length') == 1, 'plot(y) draws in the Plots pane')
check(p.js('() => MG.app.rstudio.panes.files.cur') == 'plots', 'the Plots tab is shown')
sz = p.js('() => { const c = MG.app.rstudio.plots[0].plot.canvas, b = MG.app.rstudio.plotBox.getBoundingClientRect(); return [c.width / 1.5, c.height / 1.5, b.width, b.height]; }')
check(abs(sz[0] - sz[2]) < 12 and abs(sz[1] - sz[3]) < 12, 'the plot is drawn at the size of the Plots pane: ' + str(sz))
p.shot('rs-02-script')

# save as, source
p.js('() => { MG.app.rstudio.fs.mkdirp("/home/user/scripts"); }')
p.js('() => { const R = MG.app.rstudio; R.cur.path = null; }')
# (Save As asks for a name: the dialog is answered here)
p.js('() => { MG.app.rstudio.saveAs(); }')
p.wait('() => document.querySelector(".rs-filedlg input[type=text]")')
p.js('() => { const i = document.querySelector(".rs-filedlg input[type=text]"); i.value = "scripts/analysis.R"; document.querySelector(".rs-filedlg .btn.primary").click(); }')
p.wait('() => MG.app.rstudio.cur.path === "/home/user/scripts/analysis.R" && !MG.app.rstudio.cur.dirty')
check(p.js('() => MG.app.fs.exists("/home/user/scripts/analysis.R")'), 'Save As writes the file')
check(p.js('() => MG.app.rstudio.cur.name') == 'analysis.R', 'the tab takes the file\'s name')
p.js('() => MG.app.rstudio.sourceDoc(true)')
idle()
if not check('> source("~/scripts/analysis.R", echo = TRUE)' in console(), 'Source with Echo runs source(…, echo = TRUE)'):
    print(console()[-600:])
time.sleep(0.5)
blank = p.js('() => { const P = MG.app.rstudio.plots; const c = P[P.length - 1].plot.canvas; const d = c.getContext("2d").getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i]) n++; return [P.length, n]; }')
check(blank[0] == 2 and blank[1] > 1000, 'the plot of the sourced script is a second plot, drawn: ' + str(blank))

# ---- R Markdown: chunks run with their output under them
p.js('''() => { const R = MG.app.rstudio; R.newDoc('rmd', MG.RStudio.rmdTemplate('Penguins', 'Ada Lovelace', 'rmd')); }''')
check(p.js('() => MG.app.rstudio.cur.kind') == 'rmd', 'an R Markdown document')
p.wait('() => MG.app.rstudio.cur.marks.length === 3')
check(p.js('() => document.querySelectorAll(".rs-chunkacts").length') >= 3, 'chunks have their buttons')
n0 = len(console())
np0 = p.js('() => MG.app.rstudio.plots.length')
p.js('() => { const R = MG.app.rstudio; const cs = MG.Knit.chunks(R.cur.cmDoc.getValue()); R.runChunks(R.cur, [cs[1]]); }')
idle()
outs = p.js('() => MG.app.rstudio.cur.outs.map((o) => o.node.textContent)')
check(len(outs) == 1 and 'Min.' in outs[0] and 'Max.' in outs[0], 'the chunk\'s output is under it: ' + (outs[0][:60] if outs else ''))
c = console()[n0:]
check('summary(penguins$body_mass)' in c and 'Min.' not in c, 'the console shows the code, not the output')
p.js('() => { const R = MG.app.rstudio; const cs = MG.Knit.chunks(R.cur.cmDoc.getValue()); R.runChunks(R.cur, [cs[2]]); }')
idle()
time.sleep(0.6)
nplots = p.js('() => MG.app.rstudio.cur.outs.map((o) => o.items.filter((i) => i.type === "plot").length)')
check(nplots == [0, 1], 'the plot of a chunk is under the chunk: ' + str(nplots))
check(p.js('() => MG.app.rstudio.plots.length') == np0, 'and not in the Plots pane')
size = p.js('() => { const c = MG.app.rstudio.cur.outs[1].node.querySelector("canvas"); return [c.width, c.height, Math.round(c.getBoundingClientRect().width)]; }')
check(size[0] == 1008 and size[1] == 720, 'a chunk plot is 7 × 5 inches: ' + str(size))
p.js('() => { const R = MG.app.rstudio; R.cm.scrollTo(0, R.cm.heightAtLine(15, "local")); }')
time.sleep(0.4)
p.shot('rs-03-rmd')
# an error stops the chunks
p.js('''() => { const R = MG.app.rstudio; const doc = R.cur.cmDoc; doc.replaceRange('\\n```{r broken}\\nstop("no!")\\nprint("after")\\n```\\n', {line: doc.lineCount(), ch: 0}); }''')
time.sleep(0.4)
p.js('() => { const R = MG.app.rstudio; const cs = MG.Knit.chunks(R.cur.cmDoc.getValue()); R.runChunks(R.cur, [cs[3]]); }')
idle()
last = p.js('() => { const o = MG.app.rstudio.cur.outs; return o[o.length - 1].node.textContent; }')
check('Error' in last and 'no!' in last and 'after' not in last, 'an error stops the chunk: ' + last[:60])

# ---- View(): data in a Source tab
p.js('() => MG.app.rstudio.consoleRun("View(penguins)")')
idle()
check(p.js('() => MG.app.rstudio.cur.type') == 'data', 'View() opens a data tab in Source')
info = p.js('() => MG.app.rstudio.cur.view.querySelector(".dg-info").textContent')
check('344' in info, 'the data viewer shows 344 rows: ' + info)
p.shot('rs-04-view')

# ---- help in the Help pane
p.js('() => MG.app.rstudio.consoleRun("?mean")')
idle()
time.sleep(0.5)
check(p.js('() => MG.app.rstudio.panes.files.cur') == 'help', '?mean shows the Help pane')
check('Arithmetic Mean' in p.js('() => MG.app.rstudio.helpBody.textContent'), 'the help page of mean')

# (Playwright's blocking of service workers reads navigator.serviceWorker in every frame: in the Viewer's sandboxed
# frames that is an error of the test's browser, not of the page)
errs = [e for e in p.errors if "'serviceWorker' property" not in e]
print('errors:', errs[:5])
check(not errs, 'no errors in the page')
p.close()
done()
