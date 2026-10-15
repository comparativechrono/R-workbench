"""The R session engine (assets/js/rsession.js) on its own: R's console, streamed output, prompts, plots, help,
View(), quit, file sync with the page's files, the shared user library and a session made ready in advance."""
import time, json
from h import Page, check, done

PAGE = b'''<!doctype html><meta charset="utf-8"><title>rsession</title><body data-page="t">
<script src="assets/js/config.js"></script><script src="assets/js/core.js"></script><script src="assets/js/vfs.js"></script>
<script src="assets/js/project.js"></script><script src="assets/js/rsession.js"></script>
<script>
MG.app = { HOME: '/home/user' };
MG.app.fs = new MG.VFS('/home/user');
MG.app.fs.writeText('/home/user/data/hello.csv', 'x,y\\n1,2\\n3,4\\n');
window.T = { log: [], sessions: [] };
window.mk = async (opts) => {
  const S = new MG.R.Session(opts);
  const rec = { S, ev: [] };
  for (const t of ['state', 'output', 'echo', 'prompt', 'idle', 'plot', 'view', 'help', 'pager', 'browse', 'files', 'quit', 'installed', 'event', 'ended'])
    S.on(t, (d) => rec.ev.push(Object.assign({ t }, t === 'plot' ? { kind: d.kind, id: d.id, w: d.image && d.image.width } : t === 'help' ? { topic: d.topic, title: d.title, n: (d.html || '').length } : d)));
  T.sessions.push(rec);
  await S.start();
  return T.sessions.length - 1;
};
window.ev = (i, from) => T.sessions[i].ev.slice(from || 0).map((e) => (e.t === 'view' ? { t: 'view', title: e.title, nrow: e.nrow, cols: e.columns.map((c) => c.name + ':' + c.type + ':' + JSON.stringify(c.values.slice(0, 2))) } : e));
window.out = (i, from) => T.sessions[i].ev.slice(from || 0).filter((e) => e.t === 'output' || e.t === 'echo').map((e) => (e.t === 'echo' ? e.prompt + e.line + '\\n' : e.text)).join('');
window.MG_READY = true;
</script>'''

p = Page(extra={'t.html': (PAGE, 'text/html')})
p.open('t.html')
t0 = time.time()
i = p.js('() => mk({ kind: "console", banner: true, cwd: "/home/user" })')
print(f'started in {time.time() - t0:.1f}s')
banner = p.js('(i) => out(i)', i)
check('R version 4.6' in banner and 'Type \'q()\' to quit R.' in banner, 'the banner is shown')
# (start() resolves when R is set up; its first prompt may come a moment later, on a busy computer)
try:
    p.p.wait_for_function('(i) => T.sessions[i].S.state === "idle"', arg=i, timeout=15000)
except Exception:
    pass
check(p.js('(i) => T.sessions[i].S.state', i) == 'idle', 'idle after the start')

mark = [p.js('(i) => T.sessions[i].ev.length', i)]
def run(line, wait_idle=True, timeout=30000):
    m = p.js('(i) => T.sessions[i].ev.length', i)
    p.js('([i, l]) => T.sessions[i].S.send(l)', [i, line])
    if wait_idle:
        time.sleep(0.15)
        p.wait('(i) => T.sessions[i].S.idle', arg=i, timeout=timeout)
    return m

m = run('cat("abc")')
o = p.js('([i, m]) => out(i, m)', [i, m])
check(o == '> cat("abc")\nabc', 'cat("abc") is shown before the next prompt: ' + json.dumps(o))
m = run('x <- 1:30; x')
o = p.js('([i, m]) => out(i, m)', [i, m])
check(' [1]  1  2' in o and '[26] 26' in o, 'print of 1:30')
m = run('log(-1)')
o = p.js('([i, m]) => ev(i, m)', [i, m])
errs = ''.join(e['text'] for e in o if e['t'] == 'output' and e['stream'] == 'err')
check('Warning message:' in errs and 'NaNs produced' in errs, 'the warning goes to stderr: ' + json.dumps(errs))
m = run('stop("bad")')
o = p.js('([i, m]) => out(i, m)', [i, m])
check('Error: bad' in o, 'an error')
m = run('f <- function(a,', wait_idle=False)
time.sleep(0.8)
m2 = run('b) a + b')
o = p.js('([i, m]) => ev(i, m)', [i, m])
check(any(e['t'] == 'prompt' and e['kind'] == 'continue' for e in o), 'a continuation prompt (+)')
m = run('f(1, 2)')
check('[1] 3' in p.js('([i, m]) => out(i, m)', [i, m]), 'the function made over two lines works')
# files: the page → R → the page
m = run('d <- read.csv("data/hello.csv"); sum(d$y)')
check('[1] 6' in p.js('([i, m]) => out(i, m)', [i, m]), 'R reads a file of the page')
m = run('write.csv(d, "out.csv", row.names = FALSE); dir.create("res"); writeLines("hi", "res/a.txt")')
time.sleep(0.5)
check(p.js('() => MG.app.fs.exists("/home/user/out.csv") && MG.app.fs.exists("/home/user/res/a.txt")', None), 'files R wrote reach the page')
check(p.js('() => MG.app.fs.get("/home/user/out.csv").text', None) == '"x","y"\n1,2\n3,4\n', 'with their contents')
p.js('() => MG.app.fs.writeText("/home/user/res/b.txt", "page")')
p.js('() => MG.app.fs.remove("/home/user/out.csv")')
m = run('readLines("res/b.txt"); file.exists("out.csv")')
o = p.js('([i, m]) => out(i, m)', [i, m])
check('[1] "page"' in o and '[1] FALSE' in o, 'a file written and one removed in the page reach R')
m = run('unlink("res", recursive = TRUE)')
time.sleep(0.4)
check(not p.js('() => MG.app.fs.exists("/home/user/res")', None), 'a folder that R removed goes from the page')
# plots
m = run('plot(1:10)')
o = p.js('([i, m]) => ev(i, m)', [i, m])
check(any(e['t'] == 'plot' and e['kind'] == 'new' for e in o) and any(e['t'] == 'plot' and e['kind'] == 'image' for e in o), 'a plot: a new page and pictures')
# View()
m = run('View(penguins)')
o = [e for e in p.js('([i, m]) => ev(i, m)', [i, m]) if e['t'] == 'view']
check(o and o[0]['nrow'] == 344 and o[0]['title'] == 'penguins', 'View(penguins): 344 rows')
if o:
    print('   ', o[0]['cols'][:4])
# help
m = run('?mean', timeout=60000)
time.sleep(0.5)
o = [e for e in p.js('([i, m]) => ev(i, m)', [i, m]) if e['t'] == 'help']
check(o and o[0]['topic'] == 'mean' and o[0]['n'] > 1000, 'help as a page: ' + json.dumps(o)[:200])
# completions
c = p.js('(i) => T.sessions[i].S.complete("pengu")', i)
check(c and 'penguins' in c['items'], 'completions: ' + json.dumps(c)[:120])
c = p.js('(i) => T.sessions[i].S.complete("mean(x, na.")', i)
check(c and 'na.rm=' in c['items'], 'completions of an argument: ' + json.dumps(c)[:120])
# variables
v = p.js('(i) => T.sessions[i].S.variables()', i)
print('   ', v)
check(any(x['name'] == 'd' and x['kind'] == 'data' and '2 obs. of 2 variables' in x['desc'] for x in v), 'the variables (Environment)')
# readline and browser (cross-origin isolated)
m = run('a <- readline("Name: ")', wait_idle=False)
time.sleep(1)
o = p.js('([i, m]) => ev(i, m)', [i, m])
check(any(e['t'] == 'prompt' and e['kind'] == 'input' and e['prompt'] == 'Name: ' for e in o), 'readline() asks')
run('Ada')
m = run('a')
check('[1] "Ada"' in p.js('([i, m]) => out(i, m)', [i, m]), 'readline() got the answer')
# interrupt
m = run('while (TRUE) {}', wait_idle=False)
time.sleep(1.5)
check(p.js('(i) => T.sessions[i].S.state', i) == 'busy', 'busy in an endless loop')
p.js('(i) => T.sessions[i].S.interrupt()', i)
p.wait('(i) => T.sessions[i].S.idle', arg=i, timeout=10000)
check(True, 'Esc stops the loop, R stays')
m = run('exists("a")')
check('[1] TRUE' in p.js('([i, m]) => out(i, m)', [i, m]), 'the variables are still there')
# the user library
m = run('install.packages("jsonlite")', timeout=120000)
o = p.js('([i, m]) => out(i, m)', [i, m])
print('   ', json.dumps(o)[:300])
check(p.js('() => MG.R.userlib.list()', None) == ['jsonlite'], 'install.packages() adds to the user library')
# another R: the package comes by itself, pkg::fun too
j = p.js('() => mk({ kind: "rstudio", cwd: "/home/user" })')
mm = p.js('(j) => T.sessions[j].ev.length', j)
p.js('(j) => T.sessions[j].S.send("jsonlite::toJSON(1:3)")', j)
time.sleep(0.3)
p.wait('(j) => T.sessions[j].S.idle', arg=j, timeout=60000)
check('[1,2,3]' in p.js('([j, m]) => out(j, m)', [j, mm]), 'a package installed by another R loads here (pkg::fun)')
mm = p.js('(j) => T.sessions[j].ev.length', j)
p.js('(j) => T.sessions[j].S.send("library(ggplot2)")', j)
time.sleep(0.3)
p.wait('(j) => T.sessions[j].S.idle', arg=j, timeout=60000)
o = p.js('([j, m]) => out(j, m)', [j, mm])
check("Error in library(ggplot2) : there is no package called" in o, 'a package nobody installed is not there, as in R: ' + json.dumps(o)[:160])
check(p.js('(j) => T.sessions[j].S.state', j) == 'idle', 'the second R is idle')
# the first R does not see the second R's variables
p.js('(j) => T.sessions[j].S.send("only_here <- 1")', j)
time.sleep(0.5)
m = run('exists("only_here")')
check('[1] FALSE' in p.js('([i, m]) => out(i, m)', [i, m]), 'two Rs: separate memories')
# quit
m = run('q()', wait_idle=False)
time.sleep(1)
o = p.js('([i, m]) => ev(i, m)', [i, m])
check(any(e['t'] == 'prompt' and 'Save workspace image' in e['prompt'] for e in o), 'q() asks to save the workspace')
p.js('(i) => T.sessions[i].S.send("y")', i)
p.wait('(i) => T.sessions[i].S.state === "ended"', arg=i, timeout=20000)
check(p.js('() => MG.app.fs.exists("/home/user/.RData")', None), 'q() with y writes .RData')
o = p.js('([i, m]) => ev(i, m)', [i, m])
check(any(e['t'] == 'ended' and e.get('quit') for e in o), 'the session ended (quit)')
# a fresh session for scripts: spare made ready in advance
t1 = time.time()
k = p.js('async () => { const S = await MG.R.fresh({ kind: "script", graphics: "pdf", interactive: false, cwd: "/home/user" }); T.sessions.push({ S, ev: [] }); return T.sessions.length - 1; }')
print(f'   fresh R in {time.time() - t1:.1f}s')
time.sleep(6)
t1 = time.time()
k2 = p.js('async () => { const S = await MG.R.fresh({ kind: "script", graphics: "pdf", interactive: false, cwd: "/home/user" }); T.sessions.push({ S, ev: [] }); return T.sessions.length - 1; }')
dt = time.time() - t1
check(dt < 1.5, f'the next fresh R was ready in advance ({dt:.2f}s)')
r = p.js('(k) => T.sessions[k].S.evalString("paste(interactive(), getwd(), file.exists(\'data/hello.csv\'))")', k2)
check(r == 'FALSE /home/user TRUE', 'the spare R: not interactive, in the home folder, with the files: ' + str(r))
print('page errors:', p.errors[:5])
print('\n'.join(l for l in p.logs if 'error' in l.lower())[:2000])
p.close()
done()
