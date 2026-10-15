"""The AI tab: the setup card without a key and the offline help for R errors; a key put in through the settings dialog
(kept in memory only); a question that carries the R context that is ticked – and never what is in a data file;
answers whose code goes into RStudio, the R console and the terminal; the questions that other tabs send (term:ask
from a failed command, r:ask, nb:ask) and "Explain my last error"; the agent, which runs Rscript in a folder of its own.

No AI service is asked: every request to one is answered here (Playwright routes) with canned answers, streamed as
the service streams them, and the key is a fake one."""
import json
import time
from h import Page, check, done

FAKE = 'TEST-not-a-real-key'
SERVICES = ['https://generativelanguage.googleapis.com/**', 'https://api.anthropic.com/**', 'https://api.openai.com/**']

ANSWER = """`x` is `NA` because `body_mass` has missing values: give `mean()` the argument `na.rm = TRUE`.

```r
x <- mean(penguins$body_mass, na.rm = TRUE)
round(x)
```

To see how many lines of the file have a missing value, count them in the terminal:

```bash
grep -c NA ~/data/penguins.csv
```
"""
TERM_ANSWER = 'There is no file called `nosuch.csv` in `~/data`. See what is there:\n\n```bash\nls ~/data\n```\n'
R_ANSWER = "R does not know `y`: make it first, for example `y <- c(2, 4, 6)`, then run `mean(y)` again."
CELL_ANSWER = '`sqrt()` needs numbers, but `"a"` is text.'
CHIP_ANSWER = 'R does not know `qq`: it has not been made in the R console.'
AGENT_STEPS = [
    'First I look at the size of the data file.\n\n```bash\nwc -l ~/data/penguins.csv\n```',
    'Now I work out the mean body mass of each species with an R script.\n\n```bash\n'
    "cat > means.R << 'EOF'\n"
    'p <- read.csv("~/data/penguins.csv")\n'
    'm <- aggregate(body_mass ~ species, data = p, FUN = mean)\n'
    'write.csv(m, "means.csv", row.names = FALSE)\n'
    'writeLines("not here", "~/outside-agent.txt")\n'
    'print(m)\n'
    'EOF\n'
    'Rscript means.R\n```',
    'The data file has 345 lines: a header and 344 penguins. The script `means.R` worked out the mean body mass of '
    'each species and saved the table in `means.csv`.'
]

requests = []  # (url, parsed body) of every request to an AI service – the headers are not looked at


def sse(text):
    """an answer as Gemini streams it (server-sent events)"""
    parts = [text[i:i + 50] for i in range(0, len(text), 50)]
    return ''.join('data: ' + json.dumps({'candidates': [{'content': {'parts': [{'text': t}], 'role': 'model'}}]}) + '\r\n\r\n' for t in parts)


def service(route):
    url = route.request.url
    try:
        body = json.loads(route.request.post_data or '{}')
    except Exception:
        body = {}
    requests.append((url, body))
    if 'generativelanguage.googleapis.com' not in url:
        return route.fulfill(status=500, body='{"error": {"message": "not this service"}}', headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'})
    system = (body.get('system_instruction') or {}).get('parts', [{}])[0].get('text', '')
    contents = body.get('contents') or [{}]
    last = contents[-1].get('parts', [{}])[0].get('text', '')
    if 'You are an AI agent' in system:
        n = sum(1 for c in contents if c.get('role') == 'model')
        text = AGENT_STEPS[min(n, len(AGENT_STEPS) - 1)]
    elif 'Reply with the single word' in last:
        text = 'ready'
    elif 'My command failed' in last:
        text = TERM_ANSWER
    elif 'mean(qq)' in last:
        text = CHIP_ANSWER
    elif 'My R code gave an error' in last:
        text = R_ANSWER
    elif 'Explain this error' in last:
        text = CELL_ANSWER
    else:
        text = ANSWER
    route.fulfill(status=200, body=sse(text), headers={'Content-Type': 'text/event-stream', 'Access-Control-Allow-Origin': '*'})


def last_request():
    url, body = requests[-1]
    system = (body.get('system_instruction') or {}).get('parts', [{}])[0].get('text', '')
    msgs = '\n'.join(p.get('text', '') for c in body.get('contents') or [] for p in c.get('parts') or [])
    return url, system, msgs


p = Page(width=1500, height=950)
for pat in SERVICES:
    p.ctx.route(pat, service)
p.open('index.html')
p.js('() => MG.app.showWorkbench("assistant")')
p.wait('() => MG.app.ai')
A = '() => MG.app.ai'


def key_stored():
    """is anything of the key in the browser's storage?"""
    return p.js('''(k) => { const all = []; for (const s of [localStorage, sessionStorage]) for (let i = 0; i < s.length; i++) { const n = s.key(i); all.push(n + '=' + s.getItem(n)); } return all.some((x) => x.includes(k)); }''', FAKE)


def text_of(sel):
    return p.js('(s) => Array.from(document.querySelectorAll(s)).map((e) => e.innerText).join("\\n")', sel)


def last_text(sel):
    """the text of the last element that the selector finds"""
    return p.js('(s) => { const m = document.querySelectorAll(s); return m.length ? m[m.length - 1].innerText : ""; }', sel)


def wait_answer(n_before, timeout=30000):
    """wait for the assistant to finish an answer that comes after n_before messages"""
    p.wait(f'() => !MG.app.ai.busy && MG.app.ai.msgs.chat.length > {n_before}', timeout=timeout)
    time.sleep(0.3)


def ask(q):
    n = p.js('() => MG.app.ai.msgs.chat.length')
    p.js('(q) => { const a = MG.app.ai; a.input.value = q; a.send(); }', q)
    wait_answer(n)


# ---- no key: the setup card, the note on personal data, the offline help
card = text_of('.ai-thread[data-tab="chat"] .ai-setup')
check('Connect an AI model' in card, 'without a key, the chat shows the setup card')
check('personal or patient data' in card, 'the setup card says never to paste personal or patient data')
check(p.js('() => !!document.querySelector(".ai-thread[data-tab=chat] .ai-setup .ai-setup-acts .btn.primary")'), 'the setup card has "Connect a model"')
starters = p.js('() => Array.from(MG.app.ai.sugg.querySelectorAll(".chip")).map((b) => b.textContent)')
check(any('penguins' in s for s in starters) and not any(w in ' '.join(starters) for w in ('FASTA', 'samtools', 'Biopython', 'yeast')), 'the suggested questions are about R and the penguins: ' + str(starters[:2]))
p.shot('ai-01-setup')
p.p.set_viewport_size({'width': 420, 'height': 860})
p.js('() => { document.body.classList.add("bench-open"); MG.app.showWorkbench("assistant"); }')
time.sleep(0.5)
p.shot('ai-01b-setup-narrow')
p.p.set_viewport_size({'width': 1500, 'height': 950})
time.sleep(0.3)

# a prompt from the instructions (page.js: MG.actions.prompt): into the box, for the student to send
p.js('() => MG.actions.prompt("How do I make a histogram of body_mass?")')
check(p.js('() => MG.app.ai.input.value') == 'How do I make a histogram of body_mass?' and p.js('() => MG.app.ai.tab') == 'chat', 'a prompt from the instructions goes into the box, to be sent by the student')
p.js('() => { MG.app.ai.input.value = ""; }')

# an R error message typed into the box: what it means, offline
p.js('''() => { const a = MG.app.ai; a.input.value = "Error: object 'x' not found"; a.send(); }''')
p.wait('() => document.querySelector(".ai-thread[data-tab=chat] .ai-msg.offline")', timeout=5000)
off = text_of('.ai-thread[data-tab="chat"] .ai-msg.offline')
check('R does not know the name x' in off and 'ls()' in off and 'Each tab has its own R session' in off, 'the offline help explains "object \'x\' not found": ' + off[:90].replace('\n', ' '))
check('Offline help' in off and p.js('() => !!document.querySelector(".ai-msg.offline .ai-setup-acts")'), 'it says that it is offline help, with the ways to a model')
p.js('''() => { const a = MG.app.ai; a.input.value = 'Error in ggplot(penguins, aes(flipper_len, body_mass)) : could not find function "ggplot"'; a.send(); }''')
p.wait('() => document.querySelectorAll(".ai-msg.offline").length === 2', timeout=5000)
off2 = last_text('.ai-msg.offline')
check('library(ggplot2)' in off2 and 'install.packages("ggplot2")' in off2, 'and "could not find function": load the package (ggplot2)')
U = p.js('''() => { const H = MG.aiUtil.offlineHelp; return {
  pkg: H("Error in library(dplyr) : there is no package called ‘dplyr’", "r"),
  els: H("Error: unexpected 'else' in \\"else\\"", "r"),
  file: H("Error in file(file, \\"rt\\") : cannot open the connection\\nIn addition: Warning message: cannot open file 'penguins.csv': No such file or directory", "r"),
  na: H("Error in if (x > 3) print(1) : missing value where TRUE/FALSE needed", "r"),
  sh: H("bash: python: command not found", "shell", "python script.py"),
  rcode: H("bash: syntax error near unexpected token `penguins'", "shell", "summary(penguins)") }; }''')
check('install.packages("dplyr")' in (U['pkg'] or ''), 'offline help: there is no package called → install.packages()')
check('same line' in (U['els'] or ''), "offline help: unexpected 'else' → else on the line of the }")
check('getwd()' in (U['file'] or '') and '~/data/penguins.csv' in (U['file'] or ''), 'offline help: cannot open file → the working directory, ~/data')
check('is.na' in (U['na'] or ''), 'offline help: missing value where TRUE/FALSE needed')
check('python' in (U['sh'] or '') and 'not available in this workbench' in (U['sh'] or ''), 'offline help: python is not here')
check('R code' in (U['rcode'] or '') and 'Rscript' in (U['rcode'] or ''), 'offline help: R code typed into the terminal')
# the last command of a console, when it failed: an else on a line of its own (the error that ends it is "unexpected '}'"), a warning
E = p.js('''() => MG.aiUtil.lastRError("> x <- 5\\n> if (x > 3) {\\n+   print(1)\\n+ }\\n[1] 1\\n> else {\\nError: unexpected 'else' in \\"else\\"\\n>   print(2)\\n[1] 2\\n> }\\nError: unexpected '}' in \\"}\\"\\n")''')
check(bool(E) and E['code'].startswith('if (x > 3) {') and "unexpected 'else'" in E['error'], 'lastRError: an else on a line of its own – the else is what is asked about')
W = p.js('''() => MG.aiUtil.lastRError('> as.numeric("abc")\\n[1] NA\\nWarning message:\\nNAs introduced by coercion \\n')''')
check(bool(W) and W['warning'] and 'NAs introduced' in W['error'], 'lastRError: a warning of the last command is found too')
check(p.js('''() => MG.aiUtil.lastRError('> mean(1:3)\\n[1] 2\\n')''') is None, 'lastRError: nothing when the last command went well')

# r:ask without a key: the question is made, and answered offline
p.js('''() => MG.bus.emit('r:ask', { where: 'console', code: 'mean(y)', error: "Error: object 'y' not found", output: '' })''')
p.wait('() => document.querySelectorAll(".ai-msg.offline").length === 3', timeout=5000)
q = last_text('.ai-thread[data-tab=chat] .ai-msg.user')
check('My R code gave an error in the R console' in q and 'mean(y)' in q, 'r:ask makes a question of the code and its error: ' + q[:60].replace('\n', ' '))
check('R does not know the name y' in last_text('.ai-msg.offline'), 'and, without a key, answers it offline')
check(not requests, 'no AI service was asked without a key')

# ---- a key, through the settings dialog: in memory only
p.js('() => MG.app.ai.root.querySelector(".ai-bar [aria-label=\'AI settings\']").click()')
p.wait('() => document.querySelector(".ai-set [data-k=key]")')
check(p.js('() => !document.querySelector(".ai-set [data-k=agentWeb]")'), 'the settings have no internet option for the agent (no curl or wget here)')
p.p.fill('.ai-set [data-k="key"]', FAKE)
p.p.click('.ai-set [data-x="save"]')
p.wait('() => MG.app.ai.connected()')
check(p.js('() => MG.app.ai.modeEl.textContent.includes(MG.config.geminiModel)'), 'connected: the bar names the model')
check(not key_stored(), 'the key is not in localStorage or sessionStorage')
check(not p.js('''() => Object.keys(localStorage).some((k) => k.includes('ai') && !k.startsWith((MG.config.storePrefix || 'rwb') + ':'))'''), 'what the assistant keeps uses the prefix of the site')

# ---- RStudio: a script, an object; then a question from RStudio
p.js('() => MG.app.showWorkbench("rstudio")')
p.wait('() => MG.app.rstudio && MG.app.rstudio.S && MG.app.rstudio.S.idle', timeout=180000)
p.js('''() => MG.app.rstudio.newDoc('r', 'x <- mean(penguins$body_mass, na.rm = TRUE)')''')
p.js('() => MG.app.rstudio.consoleRun("df <- head(penguins)")')
p.wait('() => (MG.app.rstudio.vars || []).some((v) => v.name === "df")', timeout=60000)
p.js('() => MG.app.showWorkbench("assistant")')
time.sleep(0.3)
ticks = p.js('() => Array.from(MG.app.ai.ctxRow.querySelectorAll("label")).map((l) => l.textContent.trim())')
check('the code in RStudio' in ticks and 'my file names' in ticks and 'the R console’s last output' in ticks, 'the ticks name what is sent, for the tabs that are open: ' + str(ticks))
ask('Why is x NA?')
url, system, msgs = last_request()
check(':streamGenerateContent' in url and p.js('() => MG.config.geminiModel') in url, 'the question went to the Gemini model of config.js (mocked)')
check('x <- mean(penguins$body_mass, na.rm = TRUE)' in msgs, 'the request carries the script open in RStudio')
check('came to the AI tab from the RStudio tab' in msgs, 'and says which tab the student came from')
check('df (data.frame, 6 obs. of 8 variables)' in msgs, "and the names and classes of RStudio's objects")
check('Torgersen' not in msgs and 'Adelie,' not in msgs, 'but no values and nothing of the data file')
check('penguins.csv (' in msgs and 'notebooks/' not in msgs, 'and the names of the files')
check('R 4.6' in system and 'datasets::penguins' in system and 'tutor' in system and 'install.packages' in system, 'the system prompt sets up an R tutor for this workbench')
check(not any(w in system for w in ('samtools', 'Galaxy', 'Bioconductor', 'FASTQ', '/data/examples', 'Snakemake', '%%bash')), 'with nothing of bioinformatics in it')
boxes = p.js('''() => { const b = document.querySelectorAll('.ai-thread[data-tab=chat] .ai-msg.assistant'); const last = b[b.length - 1];
  return Array.from(last.querySelectorAll('.ai-codebox')).map((x) => ({ head: x.querySelector('.ai-code-head').textContent, buttons: Array.from(x.querySelectorAll('.ai-code-acts .btn')).map((y) => y.textContent || y.getAttribute('aria-label')) })); }''')
check(len(boxes) == 2, 'the answer shows its two code blocks')
if len(boxes) == 2:
    check(boxes[0]['buttons'][:3] == ['Put into RStudio', 'Run in the R console', 'Add to notebook'], 'R code: Put into RStudio first (the student came from RStudio), then the R console and the notebook: ' + str(boxes[0]['buttons']))
    check('Copy' in boxes[0]['buttons'] and 'More ways to use this code' in boxes[0]['buttons'], 'with Copy and more ways')
    check(boxes[1]['buttons'][0].startswith('Run in the terminal') and 'Copy' in boxes[1]['buttons'], 'shell code: Run in the terminal: ' + str(boxes[1]['buttons']))
p.shot('ai-02-answer')
p.p.set_viewport_size({'width': 420, 'height': 860})
p.js('() => { document.body.classList.add("bench-open"); const t = MG.app.ai.threads.chat; t.scrollTop = t.scrollHeight; }')
time.sleep(0.5)
p.shot('ai-03-answer-narrow')
wide = p.js('() => document.documentElement.scrollWidth <= window.innerWidth + 1 && MG.app.ai.root.scrollWidth <= MG.app.ai.root.clientWidth + 1')
check(wide, 'at 420 px nothing sticks out sideways')
p.p.set_viewport_size({'width': 1500, 'height': 950})
time.sleep(0.3)

# a data file in RStudio's Source: its name goes, not what is in it
p.js('() => MG.app.showWorkbench("rstudio")')
p.js('() => MG.app.rstudio.openFile("/home/user/data/penguins.csv")')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.path === "/home/user/data/penguins.csv"', timeout=10000)
p.js('() => MG.app.showWorkbench("assistant")')
ask('What is in the file I have open?')
url, system, msgs = last_request()
check('~/data/penguins.csv (a data or text file: what is in it is not sent)' in msgs, 'a data file open in RStudio: only its name is sent')
check('Adelie,Torgersen' not in msgs and 'species,island,bill_len' not in msgs, 'and nothing of what is in it')

# ---- the buttons: into RStudio (at the cursor of the script), the R console, the terminal
p.js('() => { const R = MG.app.rstudio; R.activate(R.docs.find((d) => d.name === "Untitled1" || (d.kind === "r" && !d.path))); R.cm.setCursor({ line: 0, ch: 5 }); }')
FIRST = '''(label) => { const b = document.querySelectorAll('.ai-thread[data-tab=chat] .ai-msg.assistant'); for (const m of b) for (const x of m.querySelectorAll('.ai-code-acts .btn')) if (x.textContent === label) { x.click(); return true; } return false; }'''
check(p.js(FIRST, 'Put into RStudio'), 'Put into RStudio is clicked')
p.wait('() => MG.app.currentBench === "rstudio" && MG.app.rstudio.cur.cmDoc.getValue().includes("round(x)")', timeout=15000)
doc = p.js('() => MG.app.rstudio.cur.cmDoc.getValue()')
check(doc.startswith('x <- mean(penguins$body_mass, na.rm = TRUE)\nx <- mean') and doc.rstrip().endswith('round(x)'), 'the code went into the script, after the line of the cursor: ' + repr(doc[:80]))
check(p.js('() => MG.app.rstudio.cur.dirty'), 'and the script shows that it has changed')

check(p.js(FIRST, 'Run in the R console'), 'Run in the R console is clicked')
p.wait('() => MG.app.currentBench === "console" && MG.app.rcon && MG.app.rcon.cv.text().includes("[1] 4202")', timeout=180000)
check('round(x)' in p.js('() => MG.app.rcon.cv.text()'), 'the R console ran the code: [1] 4202')

check(p.js(FIRST, 'Run in the terminal'), 'Run in the terminal is clicked')
p.wait('() => MG.app.term && (MG.app.term.transcript || []).some((e) => e.line === "grep -c NA ~/data/penguins.csv")', timeout=30000)
last = p.js('() => MG.app.term.transcript[MG.app.term.transcript.length - 1]')
check(last['code'] == 0 and last['stdout'].strip().isdigit(), 'the terminal ran the command: ' + last['stdout'].strip())

check(p.js(FIRST, 'Add to notebook'), 'Add to notebook is clicked')
p.wait('() => MG.app.currentBench === "notebook" && MG.app.nbApp && MG.app.nbApp.view && MG.app.nbApp.view.cells.some((c) => c.cm.getValue().includes("round(x)"))', timeout=30000)
check(p.js('() => MG.app.nbApp.view.lang') == 'r', 'the code is in a new cell of the open R notebook')

# ---- a failed command in the terminal: "Ask the AI assistant about this error" (term:ask)
p.js('() => MG.app.term.exec("cat ~/data/nosuch.csv")')
p.wait('() => document.querySelector("#termRoot .term-ask:not([disabled])")', timeout=10000)
n0 = p.js('() => MG.app.ai.msgs.chat.length')
p.js('() => { const b = document.querySelectorAll("#termRoot .term-ask"); b[b.length - 1].click(); }')
p.wait(f'() => MG.app.currentBench === "assistant" && MG.app.ai.msgs.chat.length > {n0}', timeout=10000)
wait_answer(n0 + 1)
url, system, msgs = last_request()
check('My command failed:\n$ cat ~/data/nosuch.csv' in msgs and 'No such file or directory' in msgs, 'term:ask sends the command and its error')
check('There is no file called' in last_text('.ai-thread[data-tab="chat"] .ai-msg.assistant'), 'and the answer is shown')

# ---- r:ask from another tab: the question is made, and asked
n0 = p.js('() => MG.app.ai.msgs.chat.length')
p.js('''() => MG.bus.emit('r:ask', { where: 'rstudio', code: 'mean(y)', error: "Error: object 'y' not found", output: '' })''')
wait_answer(n0 + 1)
url, system, msgs = last_request()
check('My R code gave an error in RStudio' in msgs and "object 'y' not found" in msgs and 'The R code that gave the error, run in RStudio' in msgs, 'r:ask: the code, the error and where it ran go to the model')

# ---- nb:ask, as the notebook's "Ask AI" sends it
n0 = p.js('() => MG.app.ai.msgs.chat.length')
p.js('''() => MG.bus.emit('nb:ask', { kind: 'fix', cell: { id: 'c1', lang: 'r', path: '/home/user/notebooks/test.ipynb', code: 'sqrt("a")', count: 1, error: { ename: 'Error', evalue: 'non-numeric argument to mathematical function', traceback: 'Error in sqrt("a"): non-numeric argument to mathematical function', hints: [] }, output: '' } })''')
wait_answer(n0 + 1)
url, system, msgs = last_request()
check('Explain this error and how to fix it.' in msgs and 'sqrt("a")' in msgs and 'cell of the R notebook ~/notebooks/test.ipynb' in msgs, 'nb:ask: the cell and its error go to the model')

# ---- "Explain my last error": an error in the R console
p.js('() => MG.app.showWorkbench("console")')
p.js('() => MG.app.rcon.run("mean(qq)")')
p.wait('''() => MG.app.rcon.cv.text().includes("object 'qq' not found")''', timeout=30000)
p.js('() => MG.app.showWorkbench("assistant")')
p.wait('() => MG.app.ai.sugg.querySelector(".ai-errchip")', timeout=5000)
chip = p.js('() => MG.app.ai.sugg.querySelector(".ai-errchip").textContent')
check('Explain my last error (R console)' in chip and 'qq' in chip, 'an error in the tab the student came from: a chip to ask about it: ' + chip)
n0 = p.js('() => MG.app.ai.msgs.chat.length')
p.js('() => MG.app.ai.sugg.querySelector(".ai-errchip").click()')
wait_answer(n0 + 1)
url, system, msgs = last_request()
check('My R code gave an error in the R console:\n\nmean(qq)' in msgs, 'the chip asks about the command and its error')
check(not p.js('() => !!MG.app.ai.sugg.querySelector(".ai-errchip")'), 'and goes, once asked')

# ---- the agent: a task, run with Rscript in its own folder; what it writes outside the folder is undone
check(p.js('() => MG.agentRules.refusal("cd ~/data")').startswith('cd is not available'), 'the agent may not cd')
check('Rscript' in p.js('() => MG.agentRules.refusal("R")') and p.js('''() => MG.agentRules.refusal("Rscript -e 'mean(1:3)'") === "" && MG.agentRules.refusal("R -e 'mean(1:3)'") === "" && MG.agentRules.refusal("R CMD BATCH a.R") === "" && MG.agentRules.refusal("R --no-save < a.R") === ""'''), "R's console on its own is refused to the agent, Rscript and R -e are not")
p.js('() => MG.app.ai.showTab("agent")')
p.js('() => { const a = MG.app.ai; a.input.value = "Work out the mean body mass of each penguin species with an R script"; a.send(); }')
p.wait('() => MG.app.ai.busy', timeout=5000)
p.wait('() => !MG.app.ai.busy', timeout=300000)
time.sleep(0.5)
url, system, msgs = last_request()
check('You are an AI agent in the R workbench' in system and 'Rscript' in system, 'the agent is told how to do R here (Rscript)')
steps = p.js('() => Array.from(document.querySelectorAll(".ai-thread[data-tab=agent] .ag-step")).map((s) => s.innerText)')
check(len(steps) == 2 and 'wc -l ~/data/penguins.csv' in steps[0] and 'Rscript means.R' in steps[1], 'the agent ran its two steps: ' + str([s[:40] for s in steps]))
fs = p.js('''() => ({ means: MG.app.fs.exists('/home/user/ai-agent/run-1/means.csv'), outside: MG.app.fs.exists('/home/user/outside-agent.txt'), rec: MG.app.fs.exists('/home/user/ai-agent/run-1/agent-record.md') })''')
check(fs['means'], 'what the R script wrote in the agent\'s folder is there (means.csv)')
check(not fs['outside'], 'what it wrote outside the folder (~/outside-agent.txt) was undone')
check('outside-agent.txt' in (steps[1] if len(steps) > 1 else ''), 'and the step says so')
rec = p.js('() => MG.app.fs.readText("/home/user/ai-agent/run-1/agent-record.md")')
check(rec.startswith('# AI agent') and 'Rscript means.R' in rec and "### The agent's report" in rec and 'means.csv' in rec, 'the run is kept as a Markdown record in the folder')
check(not p.js('() => MG.app.fs.exists("/home/user/ai-agent/run-1/agent-record.ipynb")'), 'not as a notebook (the notebooks here run R, not shell commands)')
check(p.js('() => !MG.app.term.locked'), 'the terminal is the student\'s again')
p.shot('ai-04-agent')

# ---- in the end
check(not key_stored(), 'the key is still only in memory')
check(all('generativelanguage.googleapis.com' in u for u, b in requests), f'every request ({len(requests)}) went to the mocked Gemini API, none elsewhere')
errs = [e for e in p.errors if "'serviceWorker' property" not in e]
print('errors:', errs[:5])
check(not errs, 'no errors in the page')
p.close()
done()
