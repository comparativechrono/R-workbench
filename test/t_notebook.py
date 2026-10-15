"""The Notebook tab (notebook.js, kernels.js): Jupyter-style notebooks in R, run by the notebooks' own R (an
MG.R.Session of kind 'notebook'). A new notebook; what cells print, their tables, plots, errors (with a hint, stopping
the cell), warnings and messages; help and View(); the working folder; files; the Variables list; readline(); Stop
and Restart; long cells; the .ipynb that is saved; a notebook in another language; and that the notebooks' R is not
RStudio's."""
import sys, time, json, base64, struct
from h import Page, check, done

p = Page(width=1500, height=950)
p.open('index.html')
p.js('() => MG.app.showWorkbench("notebook")')
p.wait('() => MG.app.nbApp && MG.app.nbApp.view', timeout=60000)
HOME = '/home/user'


def cell(code, wait=True, timeout=60000):
    """a new code cell at the end of the open notebook, run → its outputs"""
    p.js('''(code) => {
      const v = MG.app.nbApp.view;
      const c = v.addCell({ type: 'code', source: code }, { after: v.cells[v.cells.length - 1] });
      window.T = { c, done: false };
      v.runCell(c).then(() => (T.done = true));
    }''', code)
    if wait:
        p.wait('() => T.done', timeout=timeout)
    return outs()


def outs():
    return p.js('''() => T.c.outputs.map((o) => ({ type: o.type, name: o.name || '', mime: o.mime || '',
      text: o.type === 'stream' ? o.text : o.type === 'error' ? o.traceback : o.mime === 'image/png' ? '' : String(o.data || ''),
      hints: o.hints || [], width: o.width || 0, png: o.mime === 'image/png' ? o.data.slice(0, 64) : '' }))''')


def text(os, name=None):
    return ''.join(o['text'] for o in os if o['type'] == 'stream' and (name is None or o['name'] == name))


def errors(os):
    return [o for o in os if o['type'] == 'error']


def png_size(b64):
    raw = base64.b64decode(b64[:64])
    return struct.unpack('>II', raw[16:24])


def colour_pixels(sel='img.nb-img'):
    """the red and blue pixels of the cell's last picture"""
    return p.js('''async (sel) => {
      const imgs = T.c.outEl.querySelectorAll(sel), img = imgs[imgs.length - 1];
      await img.decode();
      const c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0);
      const d = g.getImageData(0, 0, c.width, c.height).data;
      let red = 0, blue = 0;
      for (let i = 0; i < d.length; i += 4) {
        if (d[i] > 200 && d[i + 1] < 80 && d[i + 2] < 80) red++;
        if (d[i] < 80 && d[i + 1] < 80 && d[i + 2] > 200) blue++;
      }
      return [red, blue];
    }''', sel)


# ---- a new notebook: R, for IRkernel
p.js('() => MG.app.nbApp.newNotebook("r").then(() => true)')
p.wait('() => /\\/notebooks\\/Untitled\\d*\\.ipynb$/.test(MG.app.nbApp.view.path) && MG.app.nbApp.view.path !== "/home/user/notebooks/Untitled.ipynb"')
NB1 = p.js('() => MG.app.nbApp.view.path')
print('notebook:', NB1)
check(p.js('() => [MG.app.nbApp.view.lang, MG.app.nbApp.view.foreign, MG.app.nbApp.view.cells.length]') == ['r', False, 1], 'a new notebook is an R notebook with one empty cell')
meta = json.loads(p.js('(p) => MG.app.fs.get(p).text', NB1))['metadata']
check(meta['kernelspec'] == {'name': 'ir', 'display_name': 'R', 'language': 'R'}, 'its file says it is for the R kernel (IRkernel): ' + json.dumps(meta['kernelspec']))
t0 = time.time()
p.wait('() => MG.kernels.peek("r") && MG.kernels.peek("r").state === "ready"', timeout=180000)
print(f'R started in the background ({time.time() - t0:.1f}s after the notebook opened)')
check(p.js('() => MG.kernels.peek("r").S.kind') == 'notebook', 'the kernel is an R session of kind "notebook"')
pill = p.js('() => document.querySelector(".nb-kernel .nb-ktext").textContent')
check(pill.startswith('R 4.6'), 'the kernel pill shows R and its version: ' + pill)
ui = p.js('() => document.getElementById("nbRoot").textContent')
check('Python' not in ui, 'nothing in the notebook\'s toolbar speaks of Python')
p.js('() => MG.app.nbApp.notebookMenu(MG.app.nbApp.listBtn)')
menu = p.js('() => document.querySelector(".popmenu").textContent')
check('New notebook' in menu and 'Python' not in menu, 'the Notebooks menu: New notebook, no Python')
p.p.keyboard.press('Escape')

# ---- text, values
o = cell('print("hello")\n1 + 1\ny <- 2')
check(text(o) == '[1] "hello"\n[1] 2\n', 'a cell prints, and R shows the value of an expression (not of an assignment): ' + json.dumps(text(o)))
check(p.js('() => T.c.countEl.textContent') == '[1]', 'the first cell run is [1]')
o = cell('x <- c(5, 3, 8)\nmean(x)')
check(text(o) == '[1] 5.333333\n', 'mean(x): ' + json.dumps(text(o)))
o = cell('cat("no new line")')
check(text(o) == 'no new line', 'what is printed without a new line is shown: ' + json.dumps(text(o)))

# ---- a data frame: a table
o = cell('head(penguins)')
p.js('() => { window.TAB = T.c; }')
check(len(o) == 1 and o[0]['mime'] == 'text/html' and 'A data.frame: 6 × 8' in o[0]['text'], 'head(penguins) is shown as an HTML table')
tab = p.js('''() => { const t = T.c.outEl.querySelector("table.dataframe"); return t ? [t.querySelectorAll("tbody tr").length, Array.from(t.querySelectorAll("thead th")).map((x) => x.textContent)] : null; }''')
check(tab and tab[0] == 6 and 'species<fct>' in tab[1] and 'bill_len<dbl>' in tab[1], 'six rows, the columns with their types: ' + json.dumps(tab and tab[1][:4]))

# ---- plots
o = cell('plot(penguins$bill_len, penguins$body_mass)')
imgs = [x for x in o if x['mime'] == 'image/png']
check(len(o) == 1 and len(imgs) == 1, 'a plot is one picture (image/png) under the cell')
if imgs:
    wh = png_size(imgs[0]['png'])
    check(wh == (1008, 720) and imgs[0]['width'] == 672, f'7 × 5 inches: a {wh[0]} × {wh[1]} picture shown {imgs[0]["width"]} px wide')
    shown = p.js('() => Math.round(T.c.outEl.querySelector("img.nb-img").getBoundingClientRect().width)')
    check(shown == 672, f'and on the page it is {shown} px wide')
o = cell('plot(1:10)\nabline(h = 5, col = "red", lwd = 3)')
imgs = [x for x in o if x['mime'] == 'image/png']
red = colour_pixels()[0] if imgs else 0
check(len(imgs) == 1 and red > 500, f'plot() then abline() make ONE picture, with the line in it ({red} red pixels)')
p.js('() => TAB.el.scrollIntoView({ block: "start" })')
time.sleep(0.3)
p.shot('nb-01-outputs')
o = cell('abline(v = 3, col = "blue", lwd = 3)')
imgs = [x for x in o if x['mime'] == 'image/png']
rb = colour_pixels() if imgs else [0, 0]
check(len(imgs) == 1 and rb[0] > 500 and rb[1] > 500, f'abline() in a later cell shows the plot again with both lines ({rb})')
o = cell('for (i in 1:2) {\n  cat("plot", i, "\\n")\n  plot(i)\n}')
check([x['type'] for x in o] == ['stream', 'display', 'stream', 'display'], 'two plots with text between them come in order: ' + str([x['type'] + ':' + (x['mime'] or x['name']) for x in o]))
o = cell('options(repr.plot.width = 4, repr.plot.height = 3)\nhist(penguins$flipper_len)\noptions(repr.plot.width = NULL, repr.plot.height = NULL)')
imgs = [x for x in o if x['mime'] == 'image/png']
check(len(imgs) == 1 and png_size(imgs[0]['png']) == (576, 432) and imgs[0]['width'] == 384, 'options(repr.plot.width, repr.plot.height) set the size of the plots, as with IRkernel: ' + str(png_size(imgs[0]['png']) if imgs else None))

# ---- errors: the cell stops there, with a hint
o = cell('a1 <- 1\nprint(bill_length)\na2 <- 2\nprint("after")')
e = errors(o)
check(len(e) == 1 and "Error: object 'bill_length' not found" in e[0]['text'], 'an error is shown: ' + json.dumps(e[0]['text'] if e else o))
check(e and e[0]['hints'] and 'Run the cell that creates it' in e[0]['hints'][0], 'with a hint: ' + (e[0]['hints'][0][:90] if e and e[0]['hints'] else ''))
check('after' not in text(o), 'the lines after the error do not run')
check(p.js('() => !!T.c.outEl.querySelector(".nb-error") && T.c.el.classList.contains("has-error")'), 'the error is shown as an error')
o = cell('c(exists("a1"), exists("a2"))')
check('[1]  TRUE FALSE' in text(o), 'what came before the error ran, what came after it did not')
o = cell('stop("something went wrong")')
e = errors(o)
check(e and e[0]['text'] == 'Error: something went wrong' and not e[0]['hints'], 'stop(): the message, as R gives it')
p.js('() => T.c.el.scrollIntoView({ block: "center" })')
time.sleep(0.3)
p.shot('nb-02-error')
o = cell('ggplot(penguins)')
e = errors(o)
check(e and e[0]['hints'] and 'install.packages("ggplot2")' in e[0]['hints'][0] and 'library(ggplot2)' in e[0]['hints'][0], 'a function of a package that is not installed: install.packages(), then library(): ' + (e[0]['hints'][0][:100] if e and e[0]['hints'] else str(o)))
o = cell('f <- function(x) g(x)\ng <- function(x) stop("deep problem")\nf(1)')
e = errors(o)
check(e and 'Error in g(x): deep problem' in e[0]['text'] and 'Traceback:\n1. f(1)\n2. g(x)' in e[0]['text'], 'an error inside functions has a traceback: ' + json.dumps(e[0]['text'] if e else o))
o = cell('x <- c(1, 2\ny <- 3')
e = errors(o)
check(e and 'unexpected symbol in line 2' in e[0]['text'] and e[0]['hints'], 'code R cannot read: where, and a hint: ' + json.dumps(e[0]['text'] if e else o))

# ---- warnings and messages: on the error stream, the cell goes on
o = cell('w <- as.numeric(c("1", "two"))\nw')
check('Warning message' in text(o, 'stderr') and 'NAs introduced by coercion' in text(o, 'stderr') and '[1]  1 NA' in text(o, 'stdout'), 'a warning is shown and the cell goes on: ' + json.dumps(text(o)))
check('eval(' not in text(o), 'the warning does not name the notebook\'s own code')
o = cell('log(-1)')
check(text(o, 'stderr') == 'Warning message in log(-1):\n“NaNs produced”\n' and text(o, 'stdout') == '[1] NaN\n', 'a warning names the call that gave it: ' + json.dumps(text(o)))
o = cell('message("Hello, Ada Lovelace")')
check(text(o, 'stderr') == 'Hello, Ada Lovelace\n' and not text(o, 'stdout'), 'a message goes to stderr')
check(p.js('() => !!T.c.outEl.querySelector("pre.nb-stream.err")'), 'and is shown as such')
o = cell('message("one", appendLF = FALSE)\nmessage(" two")\nmessage(structure(class = c("rlang_message", "message", "condition"), list(message = "three", call = NULL)))\ncat("\\033[?25h")')
check(o == [{'type': 'stream', 'name': 'stderr', 'mime': '', 'text': 'one two\nthree\n', 'hints': [], 'width': 0, 'png': ''}], 'messages: appendLF = FALSE is kept; a message of rlang gets its new line; a lone control code shows nothing: ' + json.dumps(o))

# ---- help, View(), packages
o = cell('?mean')
check('Arithmetic Mean' in text(o) and 'Usage' in text(o), '?mean shows the help page as text under the cell')
o = cell('View(penguins)')
check(len(o) == 1 and o[0]['mime'] == 'text/html' and 'penguins · A data.frame: 344 × 8' in o[0]['text'], 'View(penguins) shows the data as a table')
check(p.js('() => T.c.outEl.querySelectorAll("table.dataframe tbody tr").length') == 344, 'all 344 rows')
o = cell('library(stats)\nsd(c(2, 4, 4, 4, 5, 5, 7, 9))')
check(text(o) == '[1] 2.13809\n' and not errors(o), 'library(stats) needs no installing')
o = cell('q()')
e = errors(o)
check(e and 'Restart' in e[0]['text'], 'q() does not end the notebook\'s R, and says how to restart it')
o = cell('system("ls")')
e = errors(o)
check(e and 'Terminal' in e[0]['text'], 'system() says that R cannot run programs here and points to the Terminal')
o = cell('%%bash\nls -l')
e = errors(o)
check(e and e[0]['hints'] and 'Terminal' in e[0]['hints'][0], '%%bash: R has no cell magics – shell commands go in the Terminal tab')

# ---- the working folder, files
o = cell('getwd()')
check(text(o) == '[1] "/home/user/notebooks"\n', 'R works in the notebook\'s folder: ' + json.dumps(text(o)))
o = cell('d <- read.csv("../data/penguins.csv")\nnrow(d)')
check(text(o) == '[1] 344\n', 'a data file of the user\'s is read from there')
o = cell('write.csv(head(penguins), "six_penguins.csv", row.names = FALSE)')
check(p.js('() => MG.app.fs.exists("/home/user/notebooks/six_penguins.csv")'), 'a file written by a cell is among the page\'s files')
first = p.js('() => (MG.app.fs.get("/home/user/notebooks/six_penguins.csv").text || "").split("\\n")[0]')
check(first.startswith('"species","island"'), 'with what R wrote: ' + first[:40])
p.js('() => MG.app.fs.writeText("/home/user/notebooks/from_page.txt", "written in the page\\n")')
o = cell('readLines("from_page.txt")')
check(text(o) == '[1] "written in the page"\n', 'a file written in the page reaches R')
o = cell('setwd("~/data")\ngetwd()')
check(text(o) == '[1] "/home/user/data"\n', 'setwd() moves R')
o = cell('getwd()')
check(text(o) == '[1] "/home/user/data"\n', 'and R stays there for the next cells')
# another notebook, in another folder: the same R (one for all the notebooks), working in that notebook's folder
p.js('() => { MG.app.fs.mkdirp("/home/user/project"); return MG.app.nbApp.newNotebook("r", { path: "/home/user/project/second.ipynb" }).then(() => true); }')
p.wait('() => MG.app.nbApp.view.path === "/home/user/project/second.ipynb"')
o = cell('getwd()\nexists("a1")')
check(text(o) == '[1] "/home/user/project"\n[1] TRUE\n', 'a notebook in another folder: R works there – and it is the same R as the other notebook\'s: ' + json.dumps(text(o)))
p.js('(p) => MG.app.nbApp.open(p).then(() => true)', NB1)
p.wait('(p) => MG.app.nbApp.view.path === p', arg=NB1)
o = cell('getwd()')
check(text(o) == '[1] "/home/user/notebooks"\n', 'back in the first notebook, R is in its folder again')

# ---- a cell longer than R's console line (4096 bytes)
code = 'long_vec <- c(' + ', '.join(str(i) for i in range(1500)) + ')\nlength(long_vec)\n# é ü ✓'
o = cell(code)
check(text(o) == '[1] 1500\n' and not errors(o), f'a cell of {len(code.encode())} bytes runs whole')

# ---- the Variables list
o = cell('my_var <- 42\npg <- penguins')
p.js('() => MG.app.nbApp.showVars()')
p.wait('() => document.querySelector(".modal .nb-vars")')
vt = p.js('() => document.querySelector(".modal .nb-vars").textContent')
check('my_var' in vt and 'numeric' in vt and '42' in vt and '344 rows × 8 columns' in vt, 'Variables lists what R has made: ' + vt[:160])
p.shot('nb-05-variables')
p.p.keyboard.press('Escape')

# ---- the notebooks' R is not RStudio's
p.js('() => MG.app.showWorkbench("rstudio")')
p.wait('() => MG.app.rstudio && MG.app.rstudio.S && MG.app.rstudio.S.idle', timeout=180000)
p.js('() => MG.app.rstudio.consoleRun("only_rstudio <- 1\\nexists(\\"my_var\\")")')
time.sleep(0.5)
p.wait('() => MG.app.rstudio.S.idle', timeout=30000)
con = p.js('() => MG.app.rstudio.cv.text()')
check('[1] FALSE' in con.split('exists("my_var")')[-1], 'RStudio\'s R does not have the notebook\'s variable: ' + json.dumps(con[-60:]))
p.js('() => MG.app.showWorkbench("notebook")')
time.sleep(0.3)
o = cell('only_rstudio')
e = errors(o)
check(e and "object 'only_rstudio' not found" in e[0]['text'] and e[0]['hints'] and 'RStudio' in e[0]['hints'][0], 'a variable made in RStudio is not in the notebook (an error with a hint): ' + (e[0]['hints'][0][:120] if e and e[0]['hints'] else str(o)))

# ---- readline(): an answer box under the cell
cell('name <- readline("Your name: ")\ncat("Hello,", name, "\\n")', wait=False)
p.wait('() => T.c.outEl.querySelector(".nb-input")', timeout=20000)
check(p.js('() => T.c.outEl.querySelector(".nb-input-p").textContent') == 'Your name: ', 'readline() asks in a box under the cell')
check(p.js('() => document.activeElement && document.activeElement.classList.contains("nb-input-f")'), 'the box has the keyboard')
bar = p.js('() => [MG.app.nbApp.titleEl, MG.app.nbApp.kernelEl, MG.app.nbApp.statusEl].map((e) => Math.round(e.getBoundingClientRect().top))')
check(max(bar) - min(bar) < 12 and 'waiting for your answer' in p.js('() => MG.app.nbApp.statusEl.textContent'), 'the status says R waits for an answer; the top bar stays on one line: ' + str(bar))
p.shot('nb-03-readline')
p.p.fill('.nb-input-f', 'Ada Lovelace')
p.p.press('.nb-input-f', 'Enter')
p.wait('() => T.done', timeout=20000)
o = outs()
check(text(o) == 'Your name: Ada Lovelace\nHello, Ada Lovelace \n', 'the answer reaches R: ' + json.dumps(text(o)))
check(not p.js('() => T.c.outEl.querySelector(".nb-input")'), 'the box is gone')
cell('choice <- menu(c("Adelie", "Gentoo"), title = "Which penguin?")\nchoice', wait=False)
p.wait('() => T.c.outEl.querySelector(".nb-input")', timeout=20000)
p.p.fill('.nb-input-f', '2')
p.p.press('.nb-input-f', 'Enter')
p.wait('() => T.done', timeout=20000)
o = outs()
check('1: Adelie' in text(o) and 'Selection: 2' in text(o) and text(o).endswith('[1] 2\n'), 'menu() too: ' + json.dumps(text(o)))

# ---- Stop: R is interrupted, and keeps its variables
check(p.js('() => crossOriginIsolated'), 'the page is cross-origin isolated (R can be interrupted)')
cell('keep_me <- "still here"\nSys.sleep(30)\ncat("not reached\\n")', wait=False)
time.sleep(2)
check(p.js('() => !MG.app.nbApp.stopBtn.hidden && T.c.countEl.textContent === "[*]"'), 'while a cell runs: [*] and the Stop button')
t1 = time.time()
p.js('() => MG.app.nbApp.stopBtn.click()')
p.wait('() => T.done', timeout=20000)
dt = time.time() - t1
o = outs()
check(dt < 10 and 'Interrupted' in text(o, 'stderr') and 'not reached' not in text(o), f'Stop interrupts Sys.sleep(30) ({dt:.1f}s): ' + json.dumps(text(o)))
cell('n <- 0\nwhile (TRUE) n <- n + 1', wait=False)
time.sleep(2)
p.js('() => MG.app.nbApp.stop()')
p.wait('() => T.done', timeout=20000)
check('Interrupted' in text(outs(), 'stderr'), 'Stop interrupts an endless loop')
o = cell('keep_me\nn > 0')
check(text(o) == '[1] "still here"\n[1] TRUE\n', 'after Stop, R still has its variables')
cell('readline("Never answered: ")', wait=False)
p.wait('() => T.c.outEl.querySelector(".nb-input")', timeout=20000)
p.js('() => MG.app.nbApp.stop()')
p.wait('() => T.done', timeout=20000)
check(not p.js('() => T.c.outEl.querySelector(".nb-input")') and p.js('() => MG.kernels.peek("r").S.idle'), 'Stop while R waits for an answer: the box goes, R is ready again')

# ---- Run all stops at an error (as Jupyter does)
p.js('''() => MG.app.nbApp.newNotebook("r", { path: "/home/user/notebooks/runall.ipynb", cells: [
  { type: 'markdown', source: '# Run all' }, { type: 'code', source: 'r1 <- 1' }, { type: 'code', source: 'stop("halt")' }, { type: 'code', source: 'r3 <- 3' }] }).then(() => true)''')
p.wait('() => MG.app.nbApp.view.path.endsWith("runall.ipynb")')
p.js('() => { window.RA = false; MG.app.nbApp.view.runAll().then(() => (RA = true)); }')
p.wait('() => RA', timeout=30000)
cnt = p.js('() => MG.app.nbApp.view.cells.map((c) => c.countEl.textContent)')
check(cnt[1] != '[ ]' and cnt[2] != '[ ]' and cnt[3] == '[ ]', 'Run all stops at the cell with the error: ' + str(cnt))
o = cell('c(exists("r1"), exists("r3"))')
check('[1]  TRUE FALSE' in text(o), 'the cells after the error did not run')
with p.p.expect_download() as dl:
    p.js('() => MG.app.nbApp.downloadScript()')
script = open(dl.value.path(), encoding='utf-8').read()
check(dl.value.suggested_filename == 'runall.R' and '# %% [markdown]\n# # Run all\n' in script and '# %%\nr1 <- 1\n' in script and '# %%\nstop("halt")\n' in script, 'Download → R script: the cells as # %% sections, the text as comments')

# ---- the .ipynb file
p.js('(p) => MG.app.nbApp.open(p).then(() => true)', NB1)
p.wait('(p) => MG.app.nbApp.view.path === p', arg=NB1)
p.js('() => MG.app.nbApp.view.saveNow()')
nb = json.loads(p.js('(p) => MG.app.fs.get(p).text', NB1))
md = nb['metadata']
check(nb['nbformat'] == 4 and nb['nbformat_minor'] >= 4 and md['kernelspec']['name'] == 'ir' and md['language_info']['name'] == 'R' and md['language_info'].get('version', '').startswith('4.6'), 'the saved .ipynb: nbformat 4, kernelspec ir, language R ' + md['language_info'].get('version', ''))
allout = [o for c in nb['cells'] if c['cell_type'] == 'code' for o in c['outputs']]
pngs = [o for o in allout if 'image/png' in o.get('data', {})]
htmls = [o for o in allout if 'text/html' in o.get('data', {})]
errs = [o for o in allout if o['output_type'] == 'error']
check(pngs and pngs[0]['output_type'] == 'display_data' and pngs[0]['metadata'].get('image/png', {}).get('width') == 672 and base64.b64decode(pngs[0]['data']['image/png'])[:8] == b'\x89PNG\r\n\x1a\n', f'its plots: image/png, shown 672 px wide ({len(pngs)})')
check(htmls and 'table' in ''.join(htmls[0]['data']['text/html']) and 'species' in ''.join(htmls[0]['data']['text/plain']), f'its tables: text/html, with text/plain beside ({len(htmls)})')
check(errs and isinstance(errs[0]['traceback'], list) and errs[0]['ename'] == 'Error', f'its errors ({len(errs)})')
check(all(c.get('id') for c in nb['cells']) and all(c['execution_count'] for c in nb['cells'] if c['cell_type'] == 'code' and c['outputs']), 'cells have ids and execution counts')

# ---- Restart: a new R, which has forgotten everything
p.js('() => { MG.app.nbApp.restart(); return true; }')
time.sleep(0.5)
p.wait('() => MG.kernels.peek("r").state === "ready" && MG.kernels.peek("r").S.idle', timeout=120000)
o = cell('exists("my_var")\ngetwd()')
check(text(o) == '[1] FALSE\n[1] "/home/user/notebooks"\n', 'after Restart, R has forgotten the variables, and works in the notebook\'s folder: ' + json.dumps(text(o)))
check(p.js('() => T.c.countEl.textContent') == '[1]', 'the cells count from [1] again')

# ---- a notebook in another language: it opens, with a warning; its cells do not run
py = {'cells': [{'cell_type': 'markdown', 'id': 'm1', 'metadata': {}, 'source': ['# Python']},
                {'cell_type': 'code', 'id': 'c1', 'metadata': {}, 'execution_count': 1, 'source': ['print(1 + 1)'],
                 'outputs': [{'output_type': 'stream', 'name': 'stdout', 'text': ['2\n']}]}],
      'metadata': {'kernelspec': {'name': 'python3', 'display_name': 'Python 3 (ipykernel)', 'language': 'python'},
                   'language_info': {'name': 'python', 'version': '3.12.1'}}, 'nbformat': 4, 'nbformat_minor': 5}
p.js('(t) => MG.app.fs.writeText("/home/user/notebooks/python-example.ipynb", t)', json.dumps(py))
p.js('() => MG.app.nbApp.open("/home/user/notebooks/python-example.ipynb").then(() => true)')
p.wait('() => MG.app.nbApp.view.path.endsWith("python-example.ipynb")')
ban = p.js('() => MG.app.nbApp.banner.hidden ? "" : MG.app.nbApp.banner.textContent')
check(p.js('() => MG.app.nbApp.view.foreign') and 'Python' in ban and 'R only' in ban, 'a Python notebook opens with a warning: ' + ban[:120])
check('Python' in p.js('() => document.querySelector(".nb-kernel").textContent'), 'the kernel pill says Python')
p.js('() => { const v = MG.app.nbApp.view; v.runCell(v.cells[1]); }')
time.sleep(0.8)
check(p.js('() => { const c = MG.app.nbApp.view.cells[1]; return c.outputs.length === 1 && c.outputs[0].text === "2\\n" && c.countEl.textContent === "[1]"; }'), 'its cells do not run here (their saved outputs stay)')
p.shot('nb-04-python')
p.js('() => MG.app.nbApp.view.saveNow()')
pm = json.loads(p.js('() => MG.app.fs.get("/home/user/notebooks/python-example.ipynb").text'))['metadata']
check(pm['kernelspec']['name'] == 'python3' and pm['language_info']['name'] == 'python', 'saved, it stays a Python notebook')

# ---- the help
p.js('(p) => MG.app.nbApp.open(p).then(() => true)', NB1)
p.wait('(p) => MG.app.nbApp.view.path === p', arg=NB1)
p.js('() => MG.app.nbApp.help()')
helptext = p.js('() => document.querySelector(".modal .nb-help").textContent')
check('one R' in helptext and 'RStudio' in helptext and 'install.packages' in helptext, 'the help tells how the notebooks\' R relates to the others')
p.shot('nb-06-help')
p.p.keyboard.press('Escape')

# (Playwright's blocking of service workers reads navigator.serviceWorker in every frame: in sandboxed frames that is
# an error of the test's browser, not of the page)
errs = [e for e in p.errors if "'serviceWorker' property" not in e]
print('errors:', errs[:5])
check(not errs, 'no errors in the page')
p.close()

# ---- a page that is not cross-origin isolated: R can neither be interrupted nor wait for an answer
p = Page(isolated=False)
p.open('index.html')
p.js('() => MG.app.showWorkbench("notebook")')
p.wait('() => MG.app.nbApp && MG.app.nbApp.view', timeout=60000)
p.wait('() => MG.kernels.peek("r") && MG.kernels.peek("r").state === "ready"', timeout=180000)
check(p.js('() => !crossOriginIsolated && !MG.kernels.peek("r").S.canBlock'), 'a page without cross-origin isolation')
o = cell('a <- readline("Your name: ")\nnchar(a)')
check('cannot wait for your answer' in text(o, 'stderr') and text(o, 'stdout').endswith('[1] 0\n') and not p.js('() => T.c.outEl.querySelector(".nb-input")'), 'readline() says it cannot wait for an answer here, and gets ""')
cell('Sys.sleep(3)\ncat("slept\\n")', wait=False)
time.sleep(1)
p.js('() => MG.app.nbApp.stop()')
p.wait('() => document.querySelector(".modal")', timeout=5000)
check('cannot be interrupted' in p.js('() => document.querySelector(".modal").textContent'), 'Stop explains that R cannot be interrupted here, and offers to restart it')
p.shot('nb-07-not-isolated')
p.js('() => document.querySelector(".modal [data-x=no]").click()')
p.wait('() => T.done', timeout=20000)
check(text(outs()) == 'slept\n', 'Let it run: the cell finishes')
errs = [e for e in p.errors if "'serviceWorker' property" not in e]
print('errors:', errs[:5])
check(not errs, 'no errors in that page either')
p.close()
done()
