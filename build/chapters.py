"""The chapters of the R workbench's starter practical, "Four ways to use R".

Students use the same R (R 4.6, running in the browser) in four different ways: the standard R console, scripts in
RStudio, documents (R Markdown and Quarto) and notebooks (R Notebooks and Jupyter), and the command line (Rscript and
R CMD BATCH in the terminal). Each chapter does a small piece of the same analysis of the Palmer penguins data, so that
students can compare the different ways of working."""
from lib import *

# (code that contains quotes or backslashes is kept out of the f-strings below)
COLOURS = 'penguin_colours <- c(Adelie = "darkorange", Chinstrap = "purple", Gentoo = "cyan4")'
EXIT = "Rscript -e 'mean(no_such_thing)'; echo \"exit status: $?\""
TABLE_CHECK = 'has:scripts/penguins.R|table\\(penguins\\$species\\)'


def ways():
    """the four ways of using R, as a figure"""
    items = [
        ('R console', 'The standard R console. You type a command and R answers straight away. It is quick, but apart from the history of your commands, nothing is kept.'),
        ('RStudio', 'An editor for scripts that you write, run and keep, with your data, plots, help pages and files alongside.'),
        ('Documents and notebooks', 'R Markdown, Quarto, R Notebooks and Jupyter notebooks, which combine text, code and results in a single file.'),
        ('Terminal', 'Running R from the command line with <code>Rscript</code> or <code>R CMD BATCH</code>, without any window at all.'),
    ]
    return '<div class="ways">' + ''.join(f'<div class="way"><b>{t}</b><span>{d}</span></div>' for t, d in items) + '</div>'


def table(head, rows, cls='compare'):
    th = ''.join(f'<th>{x}</th>' for x in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in rows)
    return f'<div class="table"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


# ---------------------------------------------------------------------------------------------------------------------
def ch_start():
    body = f'''
<h2 id="s-what">What’s in the workbench</h2>
<p>The workbench on the right gives you four different ways of using R. Behind each of them is the same version of R (R 4.6, running in your web browser), but each one suits a different kind of work:</p>
{ways()}
<p>In this practical you will do a small piece of analysis in each of them, so that you can see what each approach is good for and where it falls short. The data are measurements of 344 penguins from three islands in the Palmer Archipelago, Antarctica. You will find them in your files as <code>~/data/penguins.csv</code> (there is also an Excel version, <code>penguins.xlsx</code>), and the same data are built into R 4.6 as a dataset called <code>penguins</code>.</p>

<h2 id="s-how">How this page works</h2>
<ul>
<li>The instructions are on the left and the workbench is on the right. Use the tabs along the top of the workbench to move between the different ways of using R. The <b>Files</b> tab shows your files, and the <b>AI</b> tab has an AI assistant that you can ask about R.</li>
<li>Each activity is a list of steps. When you complete a step, it is ticked automatically and marked <span class="auto-tag">✓ spotted</span>, but you can also tick steps yourself. Buttons such as {rcon("1 + 1", "show me")} type the code in for you, and you then press <kbd>Enter</kbd> to run it.</li>
<li>Your answers and files are saved in this web browser, on this computer. To keep a copy, use <b>My answers</b> to download your answers and <b>My files</b> to download all your files as a .zip file. Do this before you clear your browser’s data or move to a different computer.</li>
<li>The first time you open a tab that uses R, R itself has to be downloaded (about 30 MB), so it may take a moment to start. Any packages you install are also only downloaded the first time.</li>
</ul>
{callout("info", "Each tab has its own R session", "<p>Just as on your own computer, the R console, RStudio, the notebook and each command you run in the terminal all use separate R sessions. An object you create in one of them doesn’t exist in the others. What they do share is your files (they all use the same home folder, <code>~</code>) and any packages you install.</p>")}
{callout("warn", "AI tools and your data", "<p>Anything you type into the AI assistant (and your code, if you allow it) is sent to an AI company. Never paste personal data or patient data into an AI tool.</p>")}
{activity("Find your way around", [
    task("s-console", f'Open the <b>R console</b> tab {bench("console", "show me")} and wait until R shows its prompt, <code>&gt;</code>, which means it is ready for a command.', auto="app:bench name=console", check="bench:console"),
    task("s-type", f'Type {rcode("1 + 1")} and press <kbd>Enter</kbd>.', auto="r:input kind=console line~1"),
    task("s-files", f'Have a look at the <b>Files</b> tab {bench("editor", "show me")}. Find <code>data/penguins.csv</code> and click on it to see the data.', auto="editor:view path~penguins.csv||editor:open path~penguins.csv"),
])}
'''
    return chapter("start", "0", "Start here", "console", "Four ways to use R", 10, "R is both a programming language and a program that runs your code. You can work with it in several ways – typing into a console, writing scripts in an editor, writing documents and notebooks, or running commands in a terminal – and the way you choose affects what you can do and what record you keep of your work.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_console():
    body = f'''
<p>The <b>R console</b> tab shows R as you get it when you install it on your own computer. There is a single window, the console, where you type a command after the prompt (<code>&gt;</code>) and R prints its answer underneath. Plots, help pages and data each open in a separate window.</p>

<h2 id="c-talk">Talking to R</h2>
{activity("Commands and objects", [
    task("c-calc", f'Type {rcode("x <- c(3, 8, 1)")}. Nothing is printed, because R has simply created an object called <code>x</code>. Now type {rcode("mean(x)")} to calculate its mean.', auto="r:input kind=console line~mean(x"),
    task("c-up", 'Press <kbd>↑</kbd> to bring back your last command, change <code>mean(x)</code> to <code>median(x)</code> and press <kbd>Enter</kbd>.', auto="r:input kind=console line~median(x"),
    task("c-plus", f'Type {rcode("sum(x")}, leaving out the closing bracket, and press <kbd>Enter</kbd>. R shows a <code>+</code> instead of the usual prompt, because it is waiting for you to finish the command. Type <code>)</code> and press <kbd>Enter</kbd>.', auto="r:input kind=console line~sum(x"),
])}
{callout("concept", "Assignment and printing", "<p><code>x &lt;- value</code> creates an object called <code>x</code> (or replaces it, if it already exists) and doesn’t print anything. A command that isn’t an assignment prints its result. The <code>[1]</code> at the start of a line of output tells you that the line begins with the first value of the result. If R is taking too long, or you get a <code>+</code> prompt by mistake, press <kbd>Esc</kbd> to stop and get back to the normal prompt.</p>")}

<h2 id="c-penguins">Looking at the penguin data</h2>
{activity("Look at the data", [
    task("c-head", f'{rcode("head(penguins)")} prints the first six rows of the data, and {rcode("summary(penguins$body_mass)")} summarises a single column.', auto="r:input kind=console line~summary("),
    task("c-view", f'{rcode("View(penguins)")} opens the data in a separate window, where you can sort the rows by any column or search for a value.', auto="r:view kind=console"),
    task("c-plot", f'{rcode("plot(body_mass ~ flipper_len, data = penguins)")} draws a scatter plot in a graphics window. Try moving the window and changing its size.', auto="rcon:plot"),
    task("c-help", f'{rcode("?mean")} opens R’s help page for the <code>mean</code> function. Find out what its <code>na.rm</code> argument does.', auto="r:help kind=console topic=mean"),
])}
{q("c-q-na", "<code>mean(penguins$body_mass)</code> returns <code>NA</code>. Why is that, and how can you calculate the mean of the masses that were actually measured?", "Two of the penguins have no body mass recorded (<code>NA</code> stands for a missing value), and R treats the mean of a set of numbers that includes a missing value as unknown. <code>mean(penguins$body_mass, na.rm = TRUE)</code> removes the missing values before calculating the mean, which is about 4202 g.")}

<h2 id="c-quit">Quitting R, and what is kept</h2>
<p>Everything you create in R is held in its memory, which is called the <em>workspace</em>. When you quit R, the workspace is lost unless you choose to save it.</p>
{activity("Save the workspace", [
    task("c-q", f'Type {rcode("q()")}. R asks <code>Save workspace image? [y/n/c]:</code>, and you answer <code>y</code> for yes.', auto="rcon:quit saved=true"),
    task("c-again", 'Click <b>Start R again</b> in the console. As it starts, R tells you <code>[Previously saved workspace restored]</code>.', auto="rcon:restart"),
    task("c-x", f'Type {rcode("x")}. Your object is back, because R saved the workspace in a file called <code>~/.RData</code> and loads that file whenever it starts.', auto="r:input kind=console line=x"),
])}
{mcq("c-q-mcq", "You created <code>x</code>, quit R <em>without</em> saving the workspace, and then started R again. What happens when you type <code>x</code>?", [
    ("Error: object 'x' not found", True, "Correct. A new R session starts with an empty workspace, unless it finds a saved .RData file to load."),
    ("The value you gave x", False, "Not without a saved .RData file. The value only existed in the memory of the R session that you quit."),
    ("NULL", False, "R doesn’t know about an object that hasn’t been created in the current session, so it reports that the object cannot be found."),
])}
{q("c-q-console", "What is the console good for? And if you come back next week, what will it <em>not</em> be able to tell you about how you got your results?", "The console is good for trying things out quickly, checking a value or reading a help page, because you get an answer straight away. However, it doesn’t keep a tidy record of your work. The history contains every line you typed, mistakes included, and a saved workspace contains objects but not the commands that created them. So next week you may have results that you cannot easily reproduce.")}
'''
    return chapter("console", "1", "The R console", "console", "The R console", 15, "The console is the quickest way to try things out in R, but it is also the way that keeps the least record of what you did.", body)


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
<p>RStudio is an <em>integrated development environment</em> (IDE) for R. Alongside R’s console, it gives you an editor for your scripts and documents (the <b>Source</b> pane, at the top left), a list of the objects in R’s memory (the <b>Environment</b> pane), and panes for your files, plots, packages and help pages, as well as a viewer for web pages. The <b>RStudio</b> tab of the workbench is modelled closely on RStudio, so what you learn here also works in the real program.</p>
{callout("info", "A separate R session", "<p>RStudio’s Console is a different R session from the one in the R console tab, so the <code>x</code> you created there doesn’t exist here. Everything you run in RStudio, whether it is a single line, a chunk or a whole script, runs in the R session shown in RStudio’s Console.</p>")}

<h2 id="r-script">Writing a script</h2>
<p>A script is a plain text file of R commands, saved with the extension <code>.R</code>. While you are working out your analysis, you can run the script one line at a time, and once it works you keep it so that you can run it again whenever you need to.</p>
{codefile("scripts/penguins.R", SCRIPT, note="<b>Create this file</b> saves the script in your files and opens it in RStudio’s Source pane.")}
{activity("Run a script, line by line", [
    task("r-make", 'Click <b>Create this file</b> above. The script opens in RStudio.', auto="file:create name=penguins.R"),
    task("r-line", 'Put the cursor on the line with <code>read.csv</code> and press <kbd>Ctrl</kbd>+<kbd>Enter</kbd> (<kbd>⌘</kbd>+<kbd>Enter</kbd> on a Mac). The line is sent to the Console and run, and <code>penguins</code> appears in the Environment pane.', auto="r:input kind=rstudio line~read.csv"),
    task("r-more", 'Keep pressing <kbd>Ctrl</kbd>+<kbd>Enter</kbd> until you reach the end of the script. A command that spans several lines, such as the <code>boxplot(</code> command, is run as a whole. The plot appears in the <b>Plots</b> pane.', auto="rstudio:plot"),
    task("r-env", 'In the Environment pane, click the ▶ next to <code>penguins</code> to see its columns, and click the table icon to view the data.', auto="r:view kind=rstudio"),
])}

<h2 id="r-repro">Your script is a record of your analysis</h2>
<p>Restarting R clears everything from its memory. If your work is in a script, that doesn’t matter: run the script again and all your objects and plots are recreated, exactly as before.</p>
{activity("Start again from your script", [
    task("r-restart", 'Choose Session ▸ <b>Restart R</b> (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F10</kbd>). The Environment pane is now empty.', auto="rstudio:restart"),
    task("r-source", 'Click <b>Source</b> at the top of the script. RStudio runs <code>source("~/scripts/penguins.R")</code>, which runs the whole script in one go.', auto="rstudio:source path~penguins.R"),
    task("r-edit", 'Add a line at the end of the script that counts the penguins of each species: <code>table(penguins$species)</code>. Save the script (<kbd>Ctrl</kbd>+<kbd>S</kbd>) and run the new line.', check=TABLE_CHECK),
])}
{callout("concept", "Let RStudio write the code for you", "<p>RStudio’s <b>Import Dataset</b> button (in the Environment pane) lets you read in a data file using a dialog, and it shows you the R code that it runs to do so. Copy that code into your script, so that reading in the data becomes part of your script too.</p>")}
{activity("Import a dataset", [
    task("r-import", 'In the Environment pane, choose <b>Import Dataset</b> ▸ <b>From Excel…</b> and use <b>Browse…</b> to find <code>data/penguins.xlsx</code>. Look at the preview and at the code underneath it, then click <b>Import</b>. (The first time you do this, RStudio needs to install the <code>readxl</code> package.)', auto="rstudio:import kind=excel"),
])}
{q("r-q-why", "You have both a script and a saved workspace (.RData). A colleague finds a mistake in the data file, and you correct it. Which of the two will give you corrected results, and why?", "The script. When you run it again, every result is recalculated from the corrected file. The saved workspace only holds the old results, and nothing in it tells you how they were produced. (This is why many people set RStudio never to save or restore .RData files, under Tools ▸ Global Options.)")}

<h2 id="r-app">If you have time: a Shiny app</h2>
<p>RStudio can also run <b>Shiny</b> apps. These are interactive web pages written in R, in which controls such as sliders and menus change what R calculates and plots. File ▸ New File ▸ <b>Shiny Web App…</b> creates an example app in a new folder, and <b>Run App</b> starts it in the Viewer pane. While the app is running the Console is busy, so click <b>Stop</b> (or press <kbd>Esc</kbd>) when you have finished with it.</p>
{activity("Run a Shiny app", [
    task("r-shiny", 'Create a Shiny web app and run it. Move the slider and watch the plot change.', auto="rstudio:shiny running=true"),
])}
'''
    return chapter("rstudio", "2", "Scripts in RStudio", "rstudio", "Scripts in RStudio", 20, "Writing your commands in a script lets you run them as you go, and gives you a record from which you can reproduce your results at any time.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_docs():
    body = f'''
<p>A report contains text, code and results, such as tables, plots and numbers quoted in sentences. In an <b>R Markdown</b> document (<code>.Rmd</code>), or in its successor <b>Quarto</b> (<code>.qmd</code>), you write all of these in one file: the text in Markdown, and the code in <em>chunks</em>. When you <em>knit</em> the document, the code is run and the whole thing is turned into a web page. (On a computer with the necessary software installed, it can also produce a PDF or Word document.)</p>

<h2 id="d-rmd">Writing an R Markdown document</h2>
{activity("Write and knit a report", [
    task("d-new", 'In RStudio, choose File ▸ New File ▸ <b>R Markdown…</b>. Enter <i>Penguin report</i> as the title and your name as the author, leave the output format as HTML, and click <b>OK</b>.', auto="rstudio:new kind=rmd"),
    task("d-save", 'Save the document (<kbd>Ctrl</kbd>+<kbd>S</kbd>), typing <code>reports/penguins.Rmd</code> as the file name.', check="exists:reports/penguins.Rmd"),
    task("d-chunk", 'Run one of the chunks by clicking the green ▶ at the right-hand end of its first line. Its output appears in the document, directly underneath the chunk.', auto="rstudio:chunk ok=true"),
    task("d-knit", 'Click <b>Knit</b>. The first time you do this, RStudio needs to install the <code>knitr</code> and <code>markdown</code> packages. The finished report opens in the Viewer pane and is saved as <code>reports/penguins.html</code>.', auto="rstudio:knit output~.html"),
])}
{callout("concept", "Knitting starts with an empty R session", "<p>When you click Knit, the document is run from the beginning in a brand new R session, not in the R session behind RStudio’s Console. This means the document has to create or read in everything it needs by itself. That is what makes a knitted report trustworthy: it shows that the code, exactly as written, produces the results in the report.</p>")}
{activity("Break it on purpose", [
    task("d-obj", f'Create an object called {c("penguin_colours")} in RStudio’s Console: {rsrun(COLOURS, "make it in the Console")}.', auto="r:input kind=rstudio line~penguin_colours <-"),
    task("d-use", 'Add a new chunk to the report (with the <b>+C</b> button, or <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>I</kbd>) containing <code>barplot(table(penguins$species), col = penguin_colours)</code>. Run the chunk with its ▶ button, and you will see that it works.', auto="rstudio:chunk ok=true"),
    task("d-fail", 'Now click <b>Knit</b>. This time knitting stops with the error <code>object &#39;penguin_colours&#39; not found</code>, which you can see in the <b>Background Jobs</b> tab. Fix the report so that it creates <code>penguin_colours</code> itself, and knit it again.', auto="rstudio:knit failed=true"),
])}
{q("d-q-fail", "Running the chunk with ▶ worked, but knitting failed. Explain why.", "The ▶ button runs the chunk in the R session behind RStudio’s Console, where you had already created <code>penguin_colours</code> by hand. Knit runs the whole document in a new, empty R session, so <code>penguin_colours</code> only exists if the document itself creates it. A report that knits successfully contains everything needed to produce its results.")}

<h2 id="d-nb">R Notebooks and Quarto</h2>
<p>An <b>R Notebook</b> is an R Markdown document that you run chunk by chunk as you work. Each time you save it, RStudio also saves a web page next to it (<code>.nb.html</code>) containing the text, the code and the outputs exactly as they are at that moment, without running anything again. <b>Quarto</b> documents are written in much the same way as R Markdown, and the <b>Render</b> button does the same job as Knit. Quarto also works with other languages, such as Python and Julia.</p>
{activity("Try them both", [
    task("d-rnb", 'Choose File ▸ New File ▸ <b>R Notebook</b>. Run its chunk, save the notebook as <code>reports/notes.Rmd</code>, and click <b>Preview</b>.', auto="rstudio:preview"),
    task("d-qmd", 'Choose File ▸ New File ▸ <b>Quarto Document…</b> and click <b>Create</b>. Save the document as <code>reports/quarto.qmd</code> and click <b>Render</b>.', auto="rstudio:knit kind=qmd"),
])}
{mcq("d-q-mcq", "You ran the chunks of an R Notebook in the order 3, 1, 2 and then saved it. What does its .nb.html file show?", [
    ("The outputs as they were when you ran the chunks in the order 3, 1, 2", True, "Correct. The notebook’s web page shows exactly what you saw on screen. Knitting the same document would run all of it again from the beginning."),
    ("The outputs you would get by running the chunks from the beginning", False, "That is what Knit (or Render) would give you. Preview doesn’t run anything."),
    ("No outputs, because they are generated when someone opens the page", False, "The outputs are saved in the page itself, as pictures and text."),
])}
'''
    return chapter("docs", "3", "Documents", "rstudio", "Documents: R Markdown and Quarto", 20, "An R Markdown or Quarto document keeps your text, code and results together in one file, and the whole document is run again from the beginning every time you knit it.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_notebook():
    body = f'''
<p>A <b>Jupyter notebook</b> (<code>.ipynb</code>) is made up of <em>cells</em>. There are code cells, whose output appears underneath them, and text cells written in Markdown. Jupyter started out with Python, but with an R kernel, as here, the code cells contain R. The outputs are saved in the notebook file, so other people can read a notebook without running it, for example on GitHub or in JupyterLab, VS Code or Google Colab.</p>
{callout("info", "Another separate R session", "<p>The notebooks use their own R session, which is separate from the ones in the R console tab and in RStudio. All the notebooks in this workbench share that one R session, and its working directory is the folder that the notebook is in.</p>")}

<h2 id="n-cells">Running cells</h2>
{activity("Run some cells", [
    task("n-open", f'Open the <b>Notebook</b> tab {bench("notebook", "show me")}. A new, empty notebook has been created for you in <code>~/notebooks</code>.', auto="app:bench name=notebook"),
    task("n-table", 'In the first code cell, type <code>head(penguins)</code> and press <kbd>Shift</kbd>+<kbd>Enter</kbd>. The data appear as a table. The number in <code>[1]</code> next to the cell shows that this was the first cell R ran.', auto="nb:run ok=true table=true"),
    task("n-plot", 'In the next cell, type <code>hist(penguins$flipper_len, main = "Flipper length", xlab = "mm")</code> and press <kbd>Shift</kbd>+<kbd>Enter</kbd>.', auto="nb:run ok=true plot=true"),
    task("n-text", 'Add a text cell (<b>+ Text</b>) and write a sentence about what the histogram shows. Press <kbd>Shift</kbd>+<kbd>Enter</kbd> to display it as formatted text.', auto="nb:saved"),
])}

<h2 id="n-state">Running cells out of order</h2>
<p>You can run the cells of a notebook in any order, and you can change a cell after it has run. When you do, the output shown under a cell may come from code that is no longer there.</p>
{activity("Hidden state", [
    task("n-a", 'Create a cell containing <code>n &lt;- 10</code> and run it. Below it, create a cell containing <code>n * 2</code> and run that too. The result is <code>20</code>.', auto="nb:run ok=true code~n * 2"),
    task("n-b", 'Change the first cell to <code>n &lt;- 1000</code>, but do <em>not</em> run it. Run only the <code>n * 2</code> cell. The answer is still <code>20</code>, so the notebook now shows code and a result that don’t match.'),
    task("n-fix", 'Open the kernel menu (the <b>R</b> button at the top) and choose <b>Restart R and run all cells</b>. Every cell is run again, from top to bottom, in a new R session.', auto="nb:restart runAll=true"),
    task("n-down", 'Click <b>Download</b> and choose <b>Jupyter notebook (.ipynb)</b>. The downloaded file can be opened, with its outputs, in Jupyter, JupyterLab, VS Code or Colab.', auto="nb:download format=ipynb"),
])}
{q("n-q-state", "Why is it risky to run a notebook’s cells out of order, and what habit protects you from the problem?", "The outputs in the notebook may not come from the code you can see, because each cell’s result depends on whatever was run before it, in whatever order, including cells that have since been changed or deleted. The habit that protects you is to restart R and run all the cells from the top (<b>Restart R and run all cells</b>) before you share a notebook or rely on its results. This is the same check that knitting does automatically for an R Markdown document.")}
{q("n-q-compare", "An R Markdown document (.Rmd) and a Jupyter notebook (.ipynb) can both contain text, code and results. Give one practical difference between the two kinds of file.", "An .Rmd file is plain text and contains no outputs, so it is easy to read, to compare with other versions and to keep under version control (for example with Git); its results are only produced when it is knitted. An .ipynb file is in JSON format, with the outputs stored inside it (plots are stored as long strings of base64 text). This means it shows its results without being run, but the differences between two versions are hard to read.")}
'''
    return chapter("notebook", "4", "Jupyter notebooks", "notebook", "Jupyter notebooks", 15, "A notebook keeps cells of code together with their output in a single file. Notebooks are easy to share, but they are also easy to run in the wrong order.", body)


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
<p>You don’t need a window to use R. Servers and computing clusters, where long analyses are often run, usually have no screen at all: R is started with a command, runs a script and then stops. The <b>Terminal</b> tab is a Linux-style terminal (bash) with R’s commands available: <code>Rscript</code> and <code>R CMD BATCH</code> run scripts, and <code>R</code> starts R’s console inside the terminal.</p>

<h2 id="t-rscript">Rscript</h2>
{activity("Run your script", [
    task("t-open", f'Open the <b>Terminal</b> tab {bench("terminal", "show me")} and type {cmd("ls scripts")}. The script you wrote in RStudio is there, because every tab works with the same files.', auto="term:command name=ls"),
    task("t-run", f'Run it with {cmd("Rscript scripts/penguins.R")}. Anything the script prints appears in the terminal. The plot has no window to go to, so R saves it in a file called <code>Rplots.pdf</code> instead ({cmd("ls -l Rplots.pdf", "see it")}).', auto="rscript:done file~penguins.R code=0"),
])}
{codefile("scripts/count.R", COUNT, note="This script uses <code>commandArgs()</code> to read the name of a species from the <em>command line</em>.")}
{activity("Scripts that take arguments", [
    task("t-make", 'Create <code>scripts/count.R</code> with the button above.', auto="file:create name=count.R"),
    task("t-arg", f'Run {cmd("Rscript scripts/count.R Gentoo")}, then try it again with <code>Chinstrap</code> instead of <code>Gentoo</code>.', auto="rscript:done file~count.R code=0"),
    task("t-loop", f'Count all three species with a single line of bash: {cmd("for s in Adelie Chinstrap Gentoo; do Rscript scripts/count.R $s; done")}', auto="term:command line~for s in"),
    task("t-err", f'When a script hits an error it stops, and its <em>exit status</em> tells you that something went wrong: {cmd(EXIT)}', auto="term:command line~exit status"),
])}
{callout("concept", "Exit status", "<p>Every program tells the shell how it finished by returning a number called its exit status: 0 means success, and anything else means that something failed. In bash, <code>$?</code> holds the exit status of the last command. A script that runs several steps can be told to stop at the first failure (with <code>set -e</code>), rather than carrying on with results that were never produced.</p>")}

<h2 id="t-batch">R CMD BATCH and R</h2>
{activity("Keep a record of a run", [
    task("t-batch", f'{cmd("R CMD BATCH scripts/penguins.R")} doesn’t print anything in the terminal. Instead, everything (the commands, their output and how long the run took) is written to a file called <code>penguins.Rout</code>. Have a look at it with {cmd("cat penguins.Rout")}.', auto="rbatch:done code=0"),
    task("t-r", f'{cmd("R -q")} starts R’s console inside the terminal (<code>-q</code> leaves out the welcome message). Try <code>summary(penguins$bill_len)</code>, then quit with <code>q()</code> and answer <code>n</code> when R asks whether to save the workspace.', auto="rterm:start"),
])}
{q("t-q-when", "Describe two situations in which you would run R with <code>Rscript</code> rather than in RStudio.", "For example: on a server or computing cluster that has no screen, such as a job submitted to a queue; for a long analysis that runs overnight; to run the same script on many inputs, such as a loop over files or species; as one step in a pipeline, or a scheduled job that runs without anyone watching; or simply to check that a script runs on its own, from start to finish, in a fresh R session.")}
'''
    return chapter("terminal", "5", "R in the terminal", "terminal", "Running R from the terminal", 15, "<code>Rscript</code>, <code>R CMD BATCH</code> and <code>R</code> let you start R with a command. This is how R is used on servers and computing clusters, in pipelines, and for any job that you need to run many times.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_compare():
    rows = [
        ('R console', 'Nothing, apart from the command history and, if you save it, the workspace', 'Trying things out, quick checks and reading help pages'),
        ('Script in RStudio', 'The script, which contains the commands that produce your results', 'Analyses you will run again, which is most of your work'),
        ('R Markdown / Quarto', 'A document that produces its own results each time it is knitted', 'Reports, papers and theses, where your methods are shared along with your results'),
        ('Jupyter notebook', 'The code, together with the output from the last time each cell was run', 'Exploring data and showing your work, teaching, and projects that mix languages'),
        ('Rscript / R CMD BATCH', 'The script, a log of the run (.Rout) and any output files', 'Servers, clusters, pipelines, and jobs that are scheduled or repeated'),
    ]
    body = f'''
<p>Each way of using R keeps a different kind of record, and each suits a different kind of job. In practice you will often move between them: you might try out a command in the console, add it to a script, knit the analysis into a report, and finally run it on a server with <code>Rscript</code>.</p>
{table(['Way of using R', 'What is kept', 'Good for'], rows)}
{q("w-q-choose", "You are starting a project to analyse a lab’s measurements. The analysis will be written up as a report for your supervisor, and it will need to be run again whenever new measurements come in. Which ways of using R would you use, and for what?", "For example, you could use the console to look at the data and try things out, and write the analysis in R scripts (in RStudio) or directly in an R Markdown or Quarto report, so that the report is rebuilt from the data each time it is knitted. You might also use <code>Rscript</code> to run the analysis again automatically when new data arrive. A notebook would work well for exploring the data, as long as you restart it and run it from the top before you share anything from it.")}

<h2 id="w-ai">Asking the AI assistant</h2>
<p>The <b>AI</b> tab gives you an AI assistant that knows about this workbench. It can explain an error message, a function or an idea, but it doesn’t always get things right, so check what it tells you and run any code yourself. When you get an error in one of the consoles, a button appears underneath it that lets you ask the assistant about the error.</p>
{prompt("Explain the difference between running an R Markdown chunk in RStudio and knitting the whole document. Keep it short and give an example of something that works in one and fails in the other.")}
{callout("warn", "Keep your data private", "<p>Never paste personal data or patient data into an AI tool.</p>")}
{q("w-q-reflect", "Which way of using R would you choose for your next piece of work, and why?", "There is no single right answer: any choice is fine if your reasons fit the work. Think about whether the work needs a record of how the results were produced (a script or a document), whether other people will read the results (a document or a notebook), and whether it will run unattended or many times (Rscript).")}
'''
    return chapter("compare", "6", "Which way, when?", "rstudio", "Which way, when?", 10, "The same R can be used in five different ways. This chapter compares them and shows how they fit together.", body)


def ALL():
    return [ch_start(), ch_console(), ch_rstudio(), ch_docs(), ch_notebook(), ch_terminal(), ch_compare()]
