"""The Files tab: the tree of ~ (the course data), a CSV file as a table, an R script edited and saved, its buttons to
the other tabs (Open in RStudio, Run with Rscript, Source in the R console), a PDF that Rscript drew, an R Markdown
document's highlighting, an Excel workbook's card (Import in RStudio), moving an open file, upload and delete – and the
tab at a phone's width."""
import time
from h import Page, check, done

p = Page(width=1500, height=950)
p.open('index.html')
p.js('() => MG.app.showWorkbench("editor")')
p.wait('() => MG.app.editor')
HOME = '/home/user'
row = lambda path: f'#edRoot .ed-row[data-path="{path}"]'
act = lambda name: f'#edRoot .ed-bar .ed-act[data-act="{name}"]'


def fs_text(path):
    return p.js('(f) => MG.app.fs.exists(f) ? MG.app.fs.readText(f) : null', path)


def term_idle(timeout=180000):
    p.wait('() => MG.app.term && !MG.app.term.busy', timeout=timeout)


# ---- the tree: the course data in ~/data
p.wait(f'() => document.querySelector(\'{row(HOME + "/data/penguins.csv")}\')', timeout=10000)
check(True, 'the tree lists ~/data/penguins.csv')
check(p.js(f'() => !!document.querySelector(\'{row(HOME + "/data/penguins.xlsx")}\')'), 'and ~/data/penguins.xlsx')
check('Every R sees the same files' in p.js('() => document.querySelector("#edRoot .ed-welcome").textContent'), 'nothing open: the tab says what it is for')

# ---- a CSV file: a table of 344 rows, with the column types of read.csv()
p.p.click(row(HOME + '/data/penguins.csv'))
p.wait('() => MG.app.editor._grid && document.querySelector("#edRoot .dg-info")', timeout=10000)
info = p.js('() => document.querySelector("#edRoot .dg-info").textContent')
check('Showing 344 of 344 entries, 8 total columns' in info, 'penguins.csv is a table of 344 rows: ' + info)
types = p.js('() => MG.app.editor._grid.cols.map((c) => c.type)')
check(types == ['character', 'character', 'numeric', 'numeric', 'integer', 'integer', 'character', 'integer'], 'the columns have the types read.csv() gives them: ' + str(types))
p.p.click('#edRoot .dg-hcell:has-text("body_mass")')
first = p.js('() => { const g = MG.app.editor._grid; return g.cols[5].values[g.order[0]]; }')
check(first == 2700, 'a click on a column\'s name sorts the rows: ' + str(first))
p.shot('files-01-table')
# "Read in the R console" types read.csv() into the R console
p.p.click(act('read'))
p.wait('() => MG.app.currentBench === "console" && MG.app.rcon', timeout=10000)
typed = p.js('() => MG.app.rcon.cv.input.value')
check(typed == 'penguins <- read.csv("~/data/penguins.csv")', 'Read in the R console types read.csv(): ' + typed)
p.js('() => { MG.app.rcon.cv.input.value = ""; MG.app.showWorkbench("editor"); }')

# ---- an R script: edited, saved with Ctrl+S
p.js(f'() => {{ MG.app.fs.mkdirp("{HOME}/scripts"); MG.app.fs.writeText("{HOME}/scripts/files_test.R", "x <- c(5, 3, 8)\\n"); }}')
p.wait(f'() => document.querySelector(\'{row(HOME + "/scripts")}\')')
if not p.js(f'() => MG.app.editor.expanded.has("{HOME}/scripts")'):
    p.p.click(row(HOME + '/scripts'))
p.p.click(row(HOME + '/scripts/files_test.R'))
p.wait(f'() => MG.app.editor.current === "{HOME}/scripts/files_test.R"')
check(p.js('() => MG.app.editor.cm.getOption("mode")') == 'r', 'an R script opens in the editor, as R')
p.js('() => { const cm = MG.app.editor.cm; cm.focus(); cm.setCursor(cm.lastLine(), 0); cm.replaceSelection(\'cat("mean:", mean(x), "\\\\n")\\n\'); }')
p.p.keyboard.type('# saved with Ctrl+S\n')
check(p.js('() => MG.app.editor.isDirty(MG.app.editor.current)'), 'an edit makes the file unsaved')
check(p.js('() => document.querySelector("#edRoot .ed-tab.on").classList.contains("dirty")'), 'its tab shows it')
p.p.keyboard.press('Control+s')
want = 'x <- c(5, 3, 8)\ncat("mean:", mean(x), "\\n")\n# saved with Ctrl+S\n'
saved = fs_text(HOME + '/scripts/files_test.R')
check(saved == want, 'Ctrl+S writes the text into the file system: ' + repr(saved))
check(not p.js('() => MG.app.editor.isDirty(MG.app.editor.current)'), 'and the file is saved')
p.js('() => { const cm = MG.app.editor.cm; cm.setCursor(cm.lastLine(), 0); cm.replaceSelection("y <- 1\\n"); }')
p.p.click('#edRoot .ed-save')
check(fs_text(HOME + '/scripts/files_test.R') == want + 'y <- 1\n', 'the Save button saves too')
p.shot('files-02-script')

# ---- Open in RStudio: the script in RStudio's Source pane
p.p.click(act('rstudio'))
p.wait(f'() => MG.app.rstudio && MG.app.rstudio.cur && MG.app.rstudio.cur.path === "{HOME}/scripts/files_test.R"', timeout=20000)
check(p.js('() => MG.app.currentBench') == 'rstudio', 'Open in RStudio opens the script in RStudio\'s Source pane')

# ---- Run with Rscript: in the Terminal, in the script's folder
p.js('() => MG.app.showWorkbench("editor")')
p.wait(f'() => MG.app.editor.current === "{HOME}/scripts/files_test.R"')
t0 = time.time()
p.p.click(act('rscript'))
p.wait('() => MG.app.term && MG.app.term.outEl.textContent.includes("mean: 5.333333")', timeout=180000)
print(f'Rscript ran in {time.time() - t0:.1f}s')
out = p.js('() => MG.app.term.outEl.textContent')
check('cd ~/scripts && Rscript files_test.R' in out and 'mean: 5.333333' in out, 'Run with Rscript runs the script in the Terminal, in its folder')
check(p.js('() => MG.app.currentBench') == 'terminal', 'the Terminal is shown')
term_idle()

# ---- Source in the R console
p.js('() => MG.app.showWorkbench("editor")')
p.wait(f'() => MG.app.editor.current === "{HOME}/scripts/files_test.R"')
p.p.click(act('source'))
p.wait('() => MG.app.rcon.cv.text().includes("mean: 5.333333")', timeout=180000)
check('source("~/scripts/files_test.R")' in p.js('() => MG.app.rcon.cv.text()'), 'Source in the R console runs source() there')

# ---- a PDF that Rscript drew is shown
p.js('() => MG.app.showWorkbench("terminal")')
term_idle()
code = p.js('''() => MG.app.term.exec("cd ~ && Rscript -e 'pdf(\\"p.pdf\\"); plot(1:10); dev.off()'")''')
check(code == 0 and p.js(f'() => MG.app.fs.exists("{HOME}/p.pdf")'), 'Rscript draws a plot into ~/p.pdf')
p.js('() => MG.app.showWorkbench("editor")')
p.wait(f'() => document.querySelector(\'{row(HOME + "/p.pdf")}\')')
p.p.click(row(HOME + '/p.pdf'))
p.wait('() => { const c = document.querySelector("#edRoot .pdfv-page canvas"); return c && c.width > 0; }', timeout=30000)
check(p.js('() => MG.app.editor.viewPath') == HOME + '/p.pdf' and 'of 1' in p.js('() => document.querySelector("#edRoot .pdfv-bar").textContent'), 'the PDF is shown: one page, drawn')
time.sleep(0.5)
p.shot('files-03-pdf')

# ---- an R Markdown document: highlighted as R Markdown, its chunks as R
p.js(f'''() => MG.app.fs.writeText("{HOME}/scripts/report.Rmd", '---\\ntitle: "Penguins"\\nauthor: "Ada Lovelace"\\noutput: html_document\\n---\\n\\n## Body mass\\n\\n```{{r mass}}\\nsummary(penguins$body_mass)\\n```\\n')''')
p.js(f'() => MG.app.editor.openFile("{HOME}/scripts/report.Rmd")')
p.wait(f'() => MG.app.editor.current === "{HOME}/scripts/report.Rmd"')
modes = p.js('() => { const cm = MG.app.editor.cm; return [cm.getOption("mode"), cm.getMode().name, cm.getTokenTypeAt({line: 8, ch: 1}), cm.getTokenTypeAt({line: 9, ch: 2})]; }')
check(modes[0] == 'rmarkdown' and modes[1] == 'rmarkdown', 'an .Rmd file opens with the rmarkdown mode: ' + str(modes[:2]))
check('rmd-chunk' in (modes[2] or '') and 'rmd-code' in (modes[3] or ''), 'its chunk is marked, its code is R: ' + str(modes[2:]))
check(p.js('() => Array.from(document.querySelectorAll("#edRoot .ed-bar .ed-act")).map((b) => b.dataset.act).join(" ")') == 'rstudio knit', 'it has the buttons Open in RStudio and Knit in RStudio')

# ---- an Excel workbook: a card that says how R reads it, and RStudio's Import Dataset
p.p.click(row(HOME + '/data/penguins.xlsx'))
p.wait('() => document.querySelector("#edRoot .ed-card h3")')
card = p.js('() => document.querySelector("#edRoot .ed-card").textContent')
check('An Excel workbook' in card and 'read_excel("~/data/penguins.xlsx")' in card and '18KB' in card, 'penguins.xlsx: a card with its size and the readxl code')
try:
    p.wait('() => document.querySelector("#edRoot .ed-sheets")', timeout=10000)
except Exception:
    pass
check('penguins, about' in p.js('() => (document.querySelector("#edRoot .ed-sheets") || {}).textContent || ""'), 'the card names the sheets of the workbook')
p.shot('files-04-xlsx')
p.p.click('#edRoot .ed-card .btn.primary')
p.wait('() => document.querySelector(".modal.rs-import")', timeout=20000)
check(p.js('() => MG.app.currentBench') == 'rstudio' and p.js('() => document.querySelector(".modal.rs-import input[type=text]").value') == '~/data/penguins.xlsx', 'Import in RStudio opens RStudio\'s Import Excel Data dialog with the file')
p.p.keyboard.press('Escape')
p.js('() => MG.app.showWorkbench("editor")')

# ---- Move to…: an open file follows its file, unsaved edits and all
p.js(f'() => MG.app.fs.writeText("{HOME}/scripts/move_me.R", "a <- 1\\n")')
p.js(f'() => MG.app.editor.openFile("{HOME}/scripts/move_me.R")')
p.wait(f'() => MG.app.editor.current === "{HOME}/scripts/move_me.R"')
p.js('() => { const cm = MG.app.editor.cm; cm.setCursor(cm.lastLine(), 0); cm.replaceSelection("b <- 2\\n"); }')
p.p.click(row(HOME + '/scripts/move_me.R') + ' .ed-more')
p.p.click('.popmenu button:has-text("Move to…")')
p.p.click(f'.modal .pick-item:text-is("~/data")')
p.wait(f'() => MG.app.fs.exists("{HOME}/data/move_me.R")')
moved = p.js('() => [MG.app.editor.current, MG.app.editor.isDirty(MG.app.editor.current), MG.app.editor.cm.getValue()]')
check(not p.js(f'() => MG.app.fs.exists("{HOME}/scripts/move_me.R")') and moved[0] == HOME + '/data/move_me.R', 'Move to… moves the file, and its open tab goes with it')
check(moved[1] and moved[2] == 'a <- 1\nb <- 2\n', 'the unsaved edit is still there')
p.js('() => MG.app.editor.save()')
check(fs_text(HOME + '/data/move_me.R') == 'a <- 1\nb <- 2\n', 'and is saved into the moved file')

# ---- upload (the file input), then delete (it asks first)
p.js(f'() => MG.app.editor.reveal("{HOME}/scripts")')
folder = p.js('() => MG.app.editor._baseDir()')
check(folder == HOME + '/scripts', 'a folder chosen in the tree is where new files go: ' + folder)
p.p.click('#edRoot .ed-treebar button[title^="Upload"]')
p.wait('() => document.querySelector("body > input[type=file]")')
p.p.set_input_files('body > input[type=file]', files=[{'name': 'notes.txt', 'mimeType': 'text/plain', 'buffer': 'Notes by Ada Lovelace\n'.encode()}])
up = folder + '/notes.txt'
p.wait(f'() => MG.app.fs.exists("{up}")', timeout=10000)
check(fs_text(up) == 'Notes by Ada Lovelace\n', 'Upload adds the file to the folder')
p.wait(f'() => MG.app.editor.current === "{up}" && document.querySelector(\'{row(up)}\')', timeout=5000)
check(True, 'the uploaded file is shown in the tree, and opened')
p.p.click(row(up) + ' .ed-more')
p.p.click('.popmenu button:has-text("Delete…")')
p.wait('() => document.querySelector(".modal .btn.danger")')
check(p.js(f'() => MG.app.fs.exists("{up}")'), 'Delete… asks first: the file is still there')
p.p.click('.modal .btn.danger')
p.wait(f'() => !MG.app.fs.exists("{up}")', timeout=5000)
time.sleep(0.4)
check(not p.js(f'() => MG.app.editor.open.has("{up}") || !!document.querySelector(\'{row(up)}\')'), 'Delete removes the file: from the tree and from the editor')

# ---- a phone's width: the tree above the file
p.p.set_viewport_size({'width': 420, 'height': 900})
p.js('() => MG.app.showWorkbench("editor")')
p.js(f'() => MG.app.editor.openFile("{HOME}/scripts/files_test.R")')
time.sleep(0.8)
box = p.js('() => { const s = document.querySelector("#edRoot .ed-side").getBoundingClientRect(), m = document.querySelector("#edRoot .ed-main").getBoundingClientRect(); return [s.width, m.width, s.bottom <= m.top + 1]; }')
check(box[2] and box[1] > 380, 'at a phone\'s width the tree is above the file, which is as wide as the tab: ' + str(box))
check(p.js('() => document.documentElement.scrollWidth <= window.innerWidth'), 'nothing is wider than the window')
p.shot('files-05-narrow')

errs = [e for e in p.errors if "'serviceWorker' property" not in e]
print('errors:', errs[:5])
check(not errs, 'no errors in the page')
p.close()
done()
