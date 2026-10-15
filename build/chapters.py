"""The chapters of the starter practical of the R workbench: "Four ways to use R".

The same R – R 4.6, in the browser – used in four ways: R's own console, scripts in RStudio, documents (R Markdown,
Quarto) and notebooks (R Notebooks, Jupyter), and R without a window (Rscript, R CMD BATCH in the terminal). Each chapter
does a little of the same work – the penguins of the Palmer Archipelago – so that the ways can be compared."""
from lib import *

# (code with quotes and backslashes: kept out of the f-strings below)
COLOURS = 'penguin_colours <- c(Adelie = "darkorange", Chinstrap = "purple", Gentoo = "cyan4")'
EXIT = "Rscript -e 'mean(no_such_thing)'; echo \"exit status: $?\""
TABLE_CHECK = 'has:scripts/penguins.R|table\\(penguins\\$species\\)'


def ways():
    """the four ways, as a figure"""
    items = [
        ('R console', 'Type a command, see the answer. R as it comes – quick, and nothing is kept but the history.'),
        ('RStudio', 'Scripts you edit, run and keep, with the environment, plots, help and files around them.'),
        ('Documents and notebooks', 'Text, code and results together: R Markdown, Quarto, R Notebooks and Jupyter.'),
        ('Terminal', '<code>Rscript</code> and <code>R CMD BATCH</code>: R with no window at all, run by commands.'),
    ]
    return '<div class="ways">' + ''.join(f'<div class="way"><b>{t}</b><span>{d}</span></div>' for t, d in items) + '</div>'


def table(head, rows, cls='compare'):
    th = ''.join(f'<th>{x}</th>' for x in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in rows)
    return f'<div class="table"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


# ---------------------------------------------------------------------------------------------------------------------
def ch_start():
    body = f'''
<h2 id="s-what">What is here</h2>
<p>The workbench on the right has R in four forms. They are all the same R – R 4.6, running in your browser – but each is a different way of working with it, and each has its place:</p>
{ways()}
<p>In this practical you do a little of the same work in each of them, so that you can see what each way is good for – and what it leaves out. The data are measurements of 344 penguins from three islands of the Palmer Archipelago in Antarctica: you find them in your files as <code>~/data/penguins.csv</code> (and <code>penguins.xlsx</code>), and R 4.6 has them built in, as <code>penguins</code>.</p>

<h2 id="s-how">How this page works</h2>
<ul>
<li>The instructions are on the left, the workbench on the right. The tabs at the top of the workbench switch between the ways of using R; <b>Files</b> shows your files, and <b>AI</b> is an AI assistant you can ask about R.</li>
<li>The steps of an activity tick themselves when you do them (<span class="auto-tag">✓ spotted</span>) – you can also tick them yourself. Buttons such as {rcon("1 + 1", "show me")} type the code for you; you press <kbd>Enter</kbd>.</li>
<li>Your answers and your files are kept in this browser, on this computer. <b>My answers</b> downloads your answers; <b>My files</b> downloads all your files as a .zip file. Download them before you clear the browser or move to another computer.</li>
<li>The first time a tab with R is opened, R is downloaded (about 30 MB) – that takes a moment. Packages you install are downloaded once, too.</li>
</ul>
{callout("info", "Every R here is an R of its own", "<p>As on your own computer, the R console, RStudio, the notebook and each run in the terminal are separate R sessions: an object you make in one is not in another. What they share is your files – the same home folder, <code>~</code> – and the packages you install.</p>")}
{callout("warn", "AI tools and your data", "<p>The AI assistant sends what you type (and, if you let it, your code) to an AI company. Never paste personal data – and never patient data – into an AI tool.</p>")}
{activity("Look around", [
    task("s-console", f'Open the <b>R console</b> tab {bench("console", "show me")} and wait until R shows its prompt, <code>&gt;</code>.', auto="app:bench name=console", check="bench:console"),
    task("s-type", f'Type {rcode("1 + 1")} and press <kbd>Enter</kbd>.', auto="r:input kind=console line~1"),
    task("s-files", f'Have a look at the <b>Files</b> tab {bench("editor", "show me")}: find <code>data/penguins.csv</code> and click it.', auto="editor:view path~penguins.csv||editor:open path~penguins.csv"),
])}
'''
    return chapter("start", "0", "Start here", "console", "Four ways to use R", 10, "R is a language and a program. How you talk to it – a console, an editor, a document, a command – changes what you can do with it.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_console():
    body = f'''
<p>The <b>R console</b> tab is R as it comes when you install it on a computer: one window, R's console, where you type a command after the prompt <code>&gt;</code> and R answers under it. Plots, help pages and data open in windows of their own.</p>

<h2 id="c-talk">Talking to R</h2>
{activity("Commands and objects", [
    task("c-calc", f'Type {rcode("x <- c(3, 8, 1)")} – nothing is printed: R made an object, <code>x</code>. Then {rcode("mean(x)")}.', auto="r:input kind=console line~mean(x"),
    task("c-up", 'Press <kbd>↑</kbd> to bring back <code>mean(x)</code>, change it to <code>median(x)</code> and press <kbd>Enter</kbd>.', auto="r:input kind=console line~median(x"),
    task("c-plus", f'Type {rcode("sum(x")} – with the closing bracket missing – and press <kbd>Enter</kbd>. R shows <code>+</code>: it waits for the rest of the command. Type <code>)</code> and <kbd>Enter</kbd>.', auto="r:input kind=console line~sum(x"),
])}
{callout("concept", "Assignment and printing", "<p><code>x &lt;- value</code> makes (or replaces) an object called <code>x</code>, and prints nothing. A command that is not an assignment prints its result: <code>[1]</code> marks the first value of the result. <kbd>Esc</kbd> stops what R is doing – and gets you out of a <code>+</code> you did not mean.</p>")}

<h2 id="c-penguins">The penguins</h2>
{activity("Look at the data", [
    task("c-head", f'{rcode("head(penguins)")} prints the first six penguins; {rcode("summary(penguins$body_mass)")} summarises one column.', auto="r:input kind=console line~summary("),
    task("c-view", f'{rcode("View(penguins)")} opens the data in a window of their own: sort by a column, search.', auto="r:view kind=console"),
    task("c-plot", f'{rcode("plot(body_mass ~ flipper_len, data = penguins)")} draws a plot in a graphics window. Move the window, resize it.', auto="rcon:plot"),
    task("c-help", f'{rcode("?mean")} opens R’s help for <code>mean</code>. Read what <code>na.rm</code> does.', auto="r:help kind=console topic=mean"),
])}
{q("c-q-na", "<code>mean(penguins$body_mass)</code> gives <code>NA</code>. Why, and how do you get the mean of the masses that were measured?", "Two of the penguins have no body mass (<code>NA</code>, a missing value), and the mean of anything with a missing value is unknown. <code>mean(penguins$body_mass, na.rm = TRUE)</code> leaves the missing values out: about 4202 g.")}

<h2 id="c-quit">Quitting – and what is kept</h2>
<p>When you quit R, everything in its memory – the <em>workspace</em> – goes, unless you save it.</p>
{activity("Save the workspace", [
    task("c-q", f'Type {rcode("q()")}. R asks <code>Save workspace image? [y/n/c]:</code> – answer <code>y</code>.', auto="rcon:quit saved=true"),
    task("c-again", 'Click <b>Start R again</b> in the console. R says <code>[Previously saved workspace restored]</code>.', auto="rcon:restart"),
    task("c-x", f'Type {rcode("x")} – your object is back. R saved it in the file <code>~/.RData</code>, and loads that file when it starts.', auto="r:input kind=console line=x"),
])}
{mcq("c-q-mcq", "You made <code>x</code>, quit R <em>without</em> saving the workspace, and started R again. What does <code>x</code> give?", [
    ("Error: object 'x' not found", True, "Right: a new R starts with an empty workspace – unless it finds a saved .RData."),
    ("The value you gave x", False, "Not without .RData: the values were only in the old R's memory."),
    ("NULL", False, "R does not know an object that was never made in this session: it says it is not found."),
])}
{q("c-q-console", "What is the console good for? And when you come back next week, what does it <em>not</em> tell you about how you got your results?", "Good for: trying things quickly, checking a value, reading help – an answer straight away. It does not keep a tidy record: the history has every line you typed, mistakes included, and the saved workspace has objects without the commands that made them. Next week you have results you cannot easily make again.")}
'''
    return chapter("console", "1", "The R console", "console", "R's own console", 15, "Type, see the answer, move on: the quickest way to talk to R – and the one that keeps least.", body)


# ---------------------------------------------------------------------------------------------------------------------
SCRIPT = '''# Penguins: body mass by species
penguins <- read.csv("data/penguins.csv")
str(penguins)

# the mean body mass of each species (missing masses left out)
mass <- aggregate(body_mass ~ species, data = penguins, FUN = mean)
mass

boxplot(body_mass ~ species, data = penguins,
        ylab = "Body mass (g)", col = "lightblue")
'''


def ch_rstudio():
    body = f'''
<p>RStudio is an <em>integrated development environment</em> (IDE) for R: around R's console it puts an editor for your scripts and documents (<b>Source</b>, top left), what is in R's memory (<b>Environment</b>), and your files, plots, packages, help and a viewer for web pages. The <b>RStudio</b> tab of the workbench works as RStudio does.</p>
{callout("info", "An R of its own", "<p>RStudio's Console is another R: <code>x</code> from the R console tab is not there. Everything you run in RStudio – a line, a chunk, a whole script – runs in this one R, the one its Console shows.</p>")}

<h2 id="r-script">A script</h2>
<p>A script is a text file of R commands, <code>.R</code>. You write it, run it a line at a time while you work it out – and keep it.</p>
{codefile("scripts/penguins.R", SCRIPT, note="<b>Create this file</b> saves it in your files and opens it in RStudio's Source pane.")}
{activity("Run a script, line by line", [
    task("r-make", 'Click <b>Create this file</b> above. The script opens in RStudio.', auto="file:create name=penguins.R"),
    task("r-line", 'Put the cursor on the line with <code>read.csv</code> and press <kbd>Ctrl</kbd>+<kbd>Enter</kbd> (on a Mac <kbd>⌘</kbd>+<kbd>Enter</kbd>): the line goes to the Console, and <code>penguins</code> appears in the Environment.', auto="r:input kind=rstudio line~read.csv"),
    task("r-more", 'Go on with <kbd>Ctrl</kbd>+<kbd>Enter</kbd> to the end. A statement over several lines – <code>boxplot(</code> – runs as one. The plot is in the <b>Plots</b> pane.', auto="rstudio:plot"),
    task("r-env", 'In the Environment, click the ▶ next to <code>penguins</code> to see its columns, and the table icon to view it.', auto="r:view kind=rstudio"),
])}

<h2 id="r-repro">The script is the record</h2>
<p>Restarting R empties its memory. With a script, that does not matter: run it again, and everything is back – made in the same way.</p>
{activity("Start again from the script", [
    task("r-restart", 'Session ▸ <b>Restart R</b> (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F10</kbd>). The Environment is empty.', auto="rstudio:restart"),
    task("r-source", 'Click <b>Source</b> at the top of the script: RStudio runs <code>source("~/scripts/penguins.R")</code> – the whole script, in one go.', auto="rstudio:source path~penguins.R"),
    task("r-edit", 'Add a line at the end of the script that counts the penguins of each species, <code>table(penguins$species)</code>. Save the script (<kbd>Ctrl</kbd>+<kbd>S</kbd>) and run the new line.', check=TABLE_CHECK),
])}
{callout("concept", "Code that writes code", "<p>RStudio's <b>Import Dataset</b> (in the Environment pane) reads a file through a dialog – and shows the R code it runs. Copy that code into your script: then the import is part of the record too.</p>")}
{activity("Import a dataset", [
    task("r-import", 'Environment ▸ <b>Import Dataset</b> ▸ <b>From Excel…</b>, Browse to <code>data/penguins.xlsx</code>. Look at the preview and the code – then <b>Import</b> (the first time, RStudio installs the <code>readxl</code> package).', auto="rstudio:import kind=excel"),
])}
{q("r-q-why", "You have a script and a saved workspace (.RData). A colleague finds a mistake in the data file, and you correct it. Which of the two gives you corrected results – and why?", "The script: run it again and every result is made afresh from the corrected file. The saved workspace holds the old results, and nothing in it says how they were made. (This is why RStudio can be set not to save or restore .RData at all: Tools ▸ Global Options.)")}

<h2 id="r-app">If you have time: an app</h2>
<p>RStudio also runs <b>Shiny</b> apps – web pages made in R, whose inputs (a slider, a menu) change what R computes and draws. File ▸ New File ▸ <b>Shiny Web App…</b> makes one in a folder of its own; <b>Run App</b> starts it in the Viewer. The Console is busy while the app runs: <b>Stop</b> (or <kbd>Esc</kbd>) ends it.</p>
{activity("A Shiny app", [
    task("r-shiny", 'Make a Shiny web app and run it. Move the slider.', auto="rstudio:shiny running=true"),
])}
'''
    return chapter("rstudio", "2", "Scripts in RStudio", "rstudio", "Scripts in RStudio", 20, "Write your commands in a script, run them as you go – and keep a record that makes your results again.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_docs():
    body = f'''
<p>A report has text, code and results: tables, plots, numbers in sentences. In an <b>R Markdown</b> document (<code>.Rmd</code>) – or its successor <b>Quarto</b> (<code>.qmd</code>) – they are written together: text in Markdown, code in <em>chunks</em>. Knitting runs the code and makes the whole into a web page (or, on a computer with the programs for it, a PDF or Word document).</p>

<h2 id="d-rmd">An R Markdown document</h2>
{activity("Write and knit a report", [
    task("d-new", 'In RStudio: File ▸ New File ▸ <b>R Markdown…</b>. Title: <i>Penguin report</i>, your name as the author, HTML – <b>OK</b>.', auto="rstudio:new kind=rmd"),
    task("d-save", 'Save it (<kbd>Ctrl</kbd>+<kbd>S</kbd>) as <code>reports/penguins.Rmd</code> – type <code>reports/penguins.Rmd</code> as the file name.', check="exists:reports/penguins.Rmd"),
    task("d-chunk", 'Run a chunk with its green ▶: its output appears under the chunk, in the document.', auto="rstudio:chunk ok=true"),
    task("d-knit", 'Click <b>Knit</b>. The first time, RStudio installs <code>knitr</code> and <code>markdown</code>. The report opens in the Viewer – and is saved as <code>reports/penguins.html</code>.', auto="rstudio:knit output~.html"),
])}
{callout("concept", "Knitting starts from nothing", "<p>Knit runs the document in a <em>new</em> R, from the top – not in the R of RStudio's Console. Whatever the report needs, it must make or read itself. That is what makes a knitted report trustworthy: it shows that the code, as written, gives these results.</p>")}
{activity("Break it, on purpose", [
    task("d-obj", f'In RStudio’s Console, make an object {c("penguin_colours")}: {rsrun(COLOURS, "make it in the Console")}.', auto="r:input kind=rstudio line~penguin_colours <-"),
    task("d-use", 'Add a chunk to the report (the <b>+C</b> button, or <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>I</kbd>) with <code>barplot(table(penguins$species), col = penguin_colours)</code>. Run the chunk with ▶ – it works.', auto="rstudio:chunk ok=true"),
    task("d-fail", 'Now <b>Knit</b>. It stops: <code>object &#39;penguin_colours&#39; not found</code> (see <b>Background Jobs</b>). Fix the report so that it makes <code>penguin_colours</code> itself, and knit again.', auto="rstudio:knit failed=true"),
])}
{q("d-q-fail", "Running the chunk with ▶ worked, knitting failed. Explain the difference.", "▶ runs the chunk in the R of RStudio's Console, where <code>penguin_colours</code> had been made by hand. Knit runs the whole document in a new, empty R: <code>penguin_colours</code> exists there only if the document makes it. A report that knits contains everything needed to make its results.")}

<h2 id="d-nb">R Notebooks and Quarto</h2>
<p>An <b>R Notebook</b> is an R Markdown document that you run chunk by chunk, as you work; when you save it, a web page with the text, the code and the outputs <em>as they are</em> is saved next to it (<code>.nb.html</code>) – nothing is run again. <b>Quarto</b> documents are written like R Markdown and <b>Render</b> like Knit; Quarto also works with Python and Julia.</p>
{activity("Try them", [
    task("d-rnb", 'File ▸ New File ▸ <b>R Notebook</b>. Run its chunk, save it as <code>reports/notes.Rmd</code>, and click <b>Preview</b>.', auto="rstudio:preview"),
    task("d-qmd", 'File ▸ New File ▸ <b>Quarto Document…</b> – <b>Create</b>, save it as <code>reports/quarto.qmd</code> and <b>Render</b> it.', auto="rstudio:knit kind=qmd"),
])}
{mcq("d-q-mcq", "You ran the chunks of an R Notebook in the order 3, 1, 2 and saved it. What does its .nb.html show?", [
    ("The outputs as they were when you ran the chunks – in the order 3, 1, 2", True, "Right: a notebook's page shows what you saw. Knitting the same document would run it again, from the top."),
    ("The outputs of a run from the top", False, "That is what Knit (or Render) gives. Preview runs nothing."),
    ("No outputs: they are made when someone opens the page", False, "The outputs are in the page, as pictures and text."),
])}
'''
    return chapter("docs", "3", "Documents", "rstudio", "Documents: R Markdown and Quarto", 20, "Text, code and results in one document – made again, from the top, every time you knit it.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_notebook():
    body = f'''
<p>A <b>Jupyter notebook</b> (<code>.ipynb</code>) is a list of <em>cells</em>: code cells, whose output appears under them, and text cells in Markdown. Jupyter started with Python; with an R kernel – as here – the code is R. The notebook file keeps the outputs, so it can be shared and read without running anything: on GitHub, in JupyterLab, VS Code or Google Colab.</p>
{callout("info", "Yet another R", "<p>The notebook's R is separate from the R console's and RStudio's. All notebooks here share one R – and it starts in the notebook's folder.</p>")}

<h2 id="n-cells">Cells</h2>
{activity("Run cells", [
    task("n-open", f'Open the <b>Notebook</b> tab {bench("notebook", "show me")}. A new notebook is there, in <code>~/notebooks</code>.', auto="app:bench name=notebook"),
    task("n-table", 'In the first code cell type <code>head(penguins)</code> and press <kbd>Shift</kbd>+<kbd>Enter</kbd>: the data appear as a table. The number in <code>[1]</code> says this was the first cell R ran.', auto="nb:run ok=true table=true"),
    task("n-plot", 'In the next cell: <code>hist(penguins$flipper_len, main = "Flipper length", xlab = "mm")</code>, <kbd>Shift</kbd>+<kbd>Enter</kbd>.', auto="nb:run ok=true plot=true"),
    task("n-text", 'Add a text cell (<b>+ Text</b>) with a sentence about what the histogram shows. <kbd>Shift</kbd>+<kbd>Enter</kbd> shows it as text.', auto="nb:saved"),
])}

<h2 id="n-state">Out of order</h2>
<p>Cells can be run in any order, and a cell can be changed after it ran. Its output then belongs to code that is no longer there.</p>
{activity("Hidden state", [
    task("n-a", 'Make a cell with <code>n <- 10</code> and run it; below it a cell with <code>n * 2</code> – run it: <code>20</code>.', auto="nb:run ok=true code~n * 2"),
    task("n-b", 'Change the first cell to <code>n <- 1000</code>, but do <em>not</em> run it. Run only the <code>n * 2</code> cell: still <code>20</code> – the notebook now shows code and a result that do not match.'),
    task("n-fix", 'Kernel menu (the <b>R</b> button at the top) ▸ <b>Restart R and run all cells</b>: every cell runs again, from the top, in a new R.', auto="nb:restart runAll=true"),
    task("n-down", '<b>Download</b> ▸ the notebook (.ipynb): it opens in Jupyter, JupyterLab, VS Code or Colab with its outputs.', auto="nb:download format=ipynb"),
])}
{q("n-q-state", "What is the danger of running a notebook's cells out of order – and what is the habit that protects you from it?", "The outputs on the page may not come from the code on the page: a cell's result depends on whatever ran before it, in any order, including cells since changed or deleted. Habit: before you share or trust a notebook, restart R and run all cells from the top (Restart & run all) – the same check that knitting does for an R Markdown document.")}
{q("n-q-compare", "An R Markdown document (.Rmd) and a Jupyter notebook (.ipynb) can both hold text, code and results. Name one practical difference between the files.", "A .Rmd file is plain text with no outputs in it: easy to read, compare and keep in version control (Git), and the results come from knitting. An .ipynb file is JSON with the outputs inside (plots as long strings of base64): it shows results without running, but differences between versions are hard to read.")}
'''
    return chapter("notebook", "4", "Jupyter notebooks", "notebook", "Jupyter notebooks", 15, "Cells of code with their output, kept in one file – easy to share, easy to run out of order.", body)


# ---------------------------------------------------------------------------------------------------------------------
COUNT = '''# How many penguins of a species? The species comes from the command line:
#   Rscript scripts/count.R Gentoo
args <- commandArgs(trailingOnly = TRUE)
species <- if (length(args) > 0) args[1] else "Adelie"

penguins <- read.csv("data/penguins.csv")
n <- sum(penguins$species == species)
cat(species, ":", n, "penguins\\n")
'''


def ch_terminal():
    body = f'''
<p>R does not need a window. On servers and computing clusters – where long analyses run – there is no screen: R is started by a command, runs a script and ends. The <b>Terminal</b> tab is a Linux terminal (bash) with R's commands: <code>Rscript</code> and <code>R CMD BATCH</code> run scripts, and <code>R</code> starts R's console in the terminal.</p>

<h2 id="t-rscript">Rscript</h2>
{activity("Run your script", [
    task("t-open", f'Open the <b>Terminal</b> {bench("terminal", "show me")}. Type {cmd("ls scripts")} – the script from RStudio is there: the files are the same everywhere.', auto="term:command name=ls"),
    task("t-run", f'Run it: {cmd("Rscript scripts/penguins.R")}. What it prints comes here; the plot has nowhere to go, so R puts it into <code>Rplots.pdf</code> ({cmd("ls -l Rplots.pdf", "see it")}).', auto="rscript:done file~penguins.R code=0"),
])}
{codefile("scripts/count.R", COUNT, note="This script reads the species from its <em>command line</em>, with <code>commandArgs()</code>.")}
{activity("Scripts that take arguments", [
    task("t-make", 'Create <code>scripts/count.R</code> (the button above).', auto="file:create name=count.R"),
    task("t-arg", f'{cmd("Rscript scripts/count.R Gentoo")} – then with <code>Chinstrap</code>.', auto="rscript:done file~count.R code=0"),
    task("t-loop", f'All three species with one line of bash: {cmd("for s in Adelie Chinstrap Gentoo; do Rscript scripts/count.R $s; done")}', auto="term:command line~for s in"),
    task("t-err", f'An error stops a script, and the exit status says so: {cmd(EXIT)}', auto="term:command line~exit status"),
])}
{callout("concept", "Exit status", "<p>Every program tells the shell how it ended: 0 for success, anything else for failure (<code>$?</code> holds it). A pipeline of scripts can stop at the first failure (<code>set -e</code>) – instead of carrying on with results that were never made.</p>")}

<h2 id="t-batch">R CMD BATCH and R</h2>
{activity("A record of the run", [
    task("t-batch", f'{cmd("R CMD BATCH scripts/penguins.R")} prints nothing: everything – the commands, their output, how long it took – goes into <code>penguins.Rout</code>. Look: {cmd("cat penguins.Rout")}.', auto="rbatch:done code=0"),
    task("t-r", f'{cmd("R -q")} starts R’s console in the terminal. Try <code>summary(penguins$bill_len)</code>, then <code>q()</code>.', auto="rterm:start"),
])}
{q("t-q-when", "Give two situations in which you would run R with <code>Rscript</code> rather than in RStudio.", "For example: on a server or a computing cluster with no screen (a job submitted to a queue); a long analysis that runs overnight; the same script for many inputs (a loop over files or species); a step in a pipeline or a scheduled job that runs without anyone there; checking that a script runs on its own, from the top, in a fresh R.")}
'''
    return chapter("terminal", "5", "R in the terminal", "terminal", "R without a window", 15, "Rscript, R CMD BATCH and R: R started by a command – for servers, clusters, pipelines and anything you run many times.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_compare():
    rows = [
        ('R console', 'nothing – only the history and, if saved, a workspace', 'trying things, quick checks, help'),
        ('Script in RStudio', 'the script: the commands that make the results', 'analyses you will run again; most of your work'),
        ('R Markdown / Quarto', 'a document that makes its results when knitted', 'reports, papers, theses; sharing methods with results'),
        ('Jupyter notebook', 'code with the outputs of the last runs', 'exploring and showing; teaching; mixing languages'),
        ('Rscript / R CMD BATCH', 'the script; a log of the run (.Rout); output files', 'servers, clusters, pipelines, scheduled and repeated runs'),
    ]
    body = f'''
<p>Each way of using R keeps something different, and suits a different job. In practice you will move between them: try a command in the console, put it in a script, knit the analysis into a report, run it on a server with <code>Rscript</code>.</p>
{table(['Way', 'What is kept', 'Good for'], rows)}
{q("w-q-choose", "You are starting a project: the analysis of a lab's measurements, written up as a report for your supervisor, run again when new measurements come in. Which ways of using R would you use, and for what?", "For example: the console to look at the data and try things; the analysis in R scripts (in RStudio) or directly in an R Markdown/Quarto report, so that the report is made again from the data each time it is knitted; possibly Rscript to re-run the analysis automatically when new data arrive. A notebook could serve for exploring – restarted and run from the top before anything is shared.")}

<h2 id="w-ai">Asking the AI assistant</h2>
<p>The <b>AI</b> tab is an AI model that knows about this workbench. It can explain an error, a function or an idea – it does not always get things right, so check what it says, and run the code yourself. After an error in a console a button offers to ask it about the error.</p>
{prompt("Explain the difference between running an R Markdown chunk in RStudio and knitting the whole document. Keep it short and give an example of something that works in one and fails in the other.")}
{callout("warn", "Your data stay yours", "<p>Never paste personal data – and never patient data – into an AI tool.</p>")}
{q("w-q-reflect", "Which way of using R would you choose for your own next piece of work – and why?", "Your own answer: any way is right if the reasons fit the work. Look for whether the work needs a record (script, document), whether others will read the results (document, notebook), and whether it runs unattended or many times (Rscript).")}
'''
    return chapter("compare", "6", "Which way, when?", "rstudio", "Which way, when?", 10, "The same R, five ways to work with it – and how they fit together.", body)


def ALL():
    return [ch_start(), ch_console(), ch_rstudio(), ch_docs(), ch_notebook(), ch_terminal(), ch_compare()]
