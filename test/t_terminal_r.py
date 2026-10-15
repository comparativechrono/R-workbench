"""R in the terminal: Rscript (a script, -e, arguments, errors, plots to Rplots.pdf), R CMD BATCH (the .Rout record,
.RData), R reading from a pipe, and R's console in the terminal (typed lines, q() and its question)."""
import time
from h import Page, check, done

p = Page()
p.open('index.html')
p.js('() => MG.app.showWorkbench("terminal")')
p.wait('() => MG.app.term')

def run(line, timeout=120000):
    p.js('() => { window._n0 = MG.app.term.outEl.children.length; }')
    code = p.js('(l) => MG.app.term.exec(l)', line)
    out = p.js('() => Array.from(MG.app.term.outEl.children).slice(window._n0 + 1).map((e) => e.textContent).join("")')
    return code, out

def write(path, text):
    p.js('([p, t]) => { MG.app.fs.mkdirp(MG.path.dirname(p)); MG.app.fs.writeText(p, t); }', [path, text])

write('/home/user/scripts/hello.R', '''penguins <- read.csv("data/penguins.csv")
cat("rows:", nrow(penguins), "\\n")
args <- commandArgs(trailingOnly = TRUE)
print(args)
plot(penguins$flipper_len, penguins$body_mass)
write.csv(head(penguins), "first_rows.csv", row.names = FALSE)
''')
t0 = time.time()
code, out = run('Rscript scripts/hello.R a b')
print(f'Rscript ran in {time.time() - t0:.1f}s')
check(code == 0, 'Rscript exits with 0')
check('rows: 344' in out and '[1] "a" "b"' in out, 'Rscript prints what the script prints, with its arguments: ' + out[:120].replace('\n', ' | '))
check(p.js('() => MG.app.fs.exists("/home/user/Rplots.pdf") && MG.app.fs.exists("/home/user/first_rows.csv")'), 'the plot went to Rplots.pdf, and the file the script wrote is there')
check(p.js('() => MG.app.fs.get("/home/user/first_rows.csv").text.startsWith("\\"species\\"")'), 'the CSV the script wrote is in the files')

code, out = run("Rscript -e 'x <- 1:10' -e 'mean(x)'")
check(code == 0 and '[1] 5.5' in out, 'Rscript -e: ' + out.strip())
code, out = run("Rscript -e 'stop(\"boom\")'; echo \"status $?\"")
check('Error: boom' in out and 'Execution halted' in out and 'status 1' in out, 'an error halts Rscript, exit status 1: ' + out.replace('\n', ' | '))
code, out = run('Rscript nosuch.R')
check(code == 2 and "cannot open file 'nosuch.R'" in out, 'a script that is not there: ' + out.strip())
code, out = run('Rscript --version')
check(code == 0 and 'Rscript (R) version 4.6' in out, 'Rscript --version: ' + out.strip())

# R CMD BATCH
code, out = run('R CMD BATCH scripts/hello.R')
check(code == 0 and out.strip() == '', 'R CMD BATCH prints nothing in the terminal')
rout = p.js('() => MG.app.fs.exists("/home/user/hello.Rout") ? MG.app.fs.get("/home/user/hello.Rout").text : ""')
check('R version 4.6' in rout and '> penguins <- read.csv("data/penguins.csv")' in rout and 'rows: 344' in rout and '> proc.time()' in rout, 'hello.Rout has the banner, the commands, their output and proc.time()')
check(p.js('() => MG.app.fs.exists("/home/user/.RData")'), 'R CMD BATCH saved the workspace in .RData')
print(rout[-400:])

# R reading commands from a pipe or a file
code, out = run("echo 'cat(2 + 2, \"\\n\")' | R --no-save -q")
check(code == 0 and '> cat(2 + 2, "\\n")' in out and '4' in out, 'R reading from a pipe shows the commands and the output: ' + out.replace('\n', ' | '))
code, out = run("echo '1' | R -q")
check(code == 2 and "you must specify '--save', '--no-save' or '--vanilla'" in out, 'R from a pipe needs --save or --no-save')

# R's console in the terminal
p.js('() => { window._rt = MG.app.term.exec("R -q"); }')
p.wait('() => MG.app.term.program && MG.app.term.program.prompt === "> "', timeout=120000)
check(p.js('() => MG.app.term.promptEl.textContent') == '> ', "the terminal's prompt is R's")
def typeR(line):
    p.js('(l) => { const t = MG.app.term; t.input.value = l; t.input.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true })); }', line)
typeR('y <- c(2, 4, 9)')
typeR('mean(y)')
p.wait('() => MG.app.term.outEl.textContent.includes("[1] 5")', timeout=30000)
check(True, 'R in the terminal runs typed lines')
typeR('q()')
p.wait('() => MG.app.term.program && MG.app.term.program.prompt.startsWith("Save workspace image?")', timeout=30000)
check(True, 'q() asks whether to save the workspace')
typeR('n')
code = p.js('() => window._rt')
check(code == 0 and not p.js('() => !!MG.app.term.program'), 'after q() the terminal is the shell again')
check('$' in p.js('() => MG.app.term.promptEl.textContent'), 'the prompt is the shell\'s')

code, out = run('help')
check('Rscript' in out and 'R CMD BATCH' in out, 'help lists R\'s commands')

errs = [e for e in p.errors if "'serviceWorker' property" not in e]
print('errors:', errs[:5])
check(not errs, 'no errors in the page')
p.shot('term-r')
p.close()
done()
