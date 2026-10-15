# R workbench

**A workbench in the browser for R practicals: R's own console, an RStudio-style IDE, Jupyter-style notebooks, R Markdown, R Notebooks and Quarto documents, Shiny apps, a terminal with `Rscript`, a file manager with a text editor, and an AI assistant – with the instructions of the practical beside them.**

Everything runs in the student's browser. R is webR – R 4.6 compiled to WebAssembly – and every R of the page (the console, RStudio, the notebooks, `Rscript` in the terminal, knitting, Shiny) is a real R session. Nothing is installed, there is no server-side code, and students' files are kept in their own browser. The site is static (HTML, CSS, JavaScript), so it can be hosted free on **GitHub Pages** or on any web server.

The workbench is the base of the course's R practicals: each practical is this page with chapters of its own in the left-hand pane (see [Writing a practical](#writing-a-practical)). It comes with a short starter practical, *Four ways to use R*.

---

## Contents

1. [What is in it](#what-is-in-it)
2. [The starter practical](#the-starter-practical)
3. [Before students use it](#before-students-use-it)
4. [Put it on GitHub Pages](#put-it-on-github-pages)
5. [Try it on your own computer](#try-it-on-your-own-computer)
6. [Settings: `config.js`](#settings-configjs)
7. [Writing a practical](#writing-a-practical)
8. [What students keep](#what-students-keep)
9. [Privacy](#privacy)
10. [Browser support and limits](#browser-support-and-limits)
11. [How it was tested](#how-it-was-tested)
12. [Files](#files)
13. [Credits and licences](#credits-and-licences)

---

## What is in it

One page, `index.html`: the **instructions** on the left – chapters with steps that tick themselves when the student does them, questions with model answers –, the **workbench** on the right. The instructions can be hidden (the button at the top left, or <kbd>Ctrl</kbd>+<kbd>\</kbd>) and the workbench made full screen; on a phone the workbench opens over the instructions.

| Tab | What it is |
| --- | --- |
| **R console** | R on its own, as R's own program shows it: the console (history with <kbd>↑</kbd>, completion with <kbd>Tab</kbd>, <kbd>Esc</kbd> to interrupt), each plot in a graphics window of its own, help pages in a help window, `View()` in a data window, `q()` with its question about saving the workspace (`.RData`). No editor and no list of objects – what R alone gives you |
| **RStudio** | an IDE in the manner of RStudio, made for teaching. **Source**: R scripts (Run, Source), R Markdown documents (chunks run with their output under them; Knit), R Notebooks (Preview, `.nb.html`), Quarto documents (Render), text; data (`View()`) in tabs of their own. **Console**, with Terminal and Background Jobs. **Environment** (with *Import Dataset* from CSV – base or readr – and Excel), History. **Files, Plots, Packages, Help, Viewer**. Menus, keyboard shortcuts and Global Options as in RStudio; *New File → Shiny Web App* and *Run App* show a running Shiny app in the Viewer |
| **Notebook** | Jupyter-style notebooks in R (`.ipynb`, as Jupyter runs them with its R kernel): code and Markdown cells, plots, tables, errors that stop the cell, Restart, Run All, Jupyter's keys; download as `.ipynb`, `.R` or `.html` |
| **Terminal** | a bash-like shell with `Rscript` (a script, `-e`, arguments, exit status; plots go to `Rplots.pdf`), `R CMD BATCH` (the `.Rout` record) and `R` (R's console in the terminal), and the GNU text tools – `grep`, `sed`, `awk`, `sort`, `cut`, `diff` … – compiled to WebAssembly. `help` lists them |
| **Files** | the home folder (`~`, `/home/user`): a tree (upload, download – a folder as `.zip` –, new, rename, move, delete), an editor for scripts and documents, viewers for tables (sorted, searched, filtered), pictures, PDFs and HTML reports, and buttons that take a file to another tab (an R script to RStudio, `Rscript` or `source()`; a document to Knit; a table to *Import Dataset*) |
| **AI** | an AI assistant set up as a tutor for R. **Chat** answers questions with what the student chooses to send – the end of the console, the document open in RStudio, the notebook's code, the last terminal commands, the names of files (never what is in a data file) – and puts the code of its answers into the console, RStudio, a notebook, the terminal or a file with one click. Under an error in any tab, *Ask the AI assistant about this error* sends the code and the error. **Agent** carries out a task with `Rscript` in the terminal, in a folder of its own, and keeps a record of every step. The student connects a model of their own (Google Gemini, Anthropic's Claude, or an OpenAI-compatible service) |

**Every R is an R of its own**, as on a computer: what the R console makes in memory is not in RStudio, the notebook or a run of `Rscript`, and *Knit* runs a document in a new R. What they share is the files – the same home folder – and the packages that were installed: a package installed in one R can be loaded in all of them, and is still there on the next visit.

## The starter practical

*Four ways to use R* (about 1 hour 45 minutes; 47 steps and 11 questions in 7 chapters) does a little of the same work – the Palmer penguins, in `~/data/penguins.csv` and built into R 4.6 as `penguins` – in each way of using R, so that students can see what each is good for and what it leaves out:

| Chapter | Tab | What the student does |
| --- | --- | --- |
| 0. Start here (10 min) | R console | the four ways of using R; how the page works; every R is an R of its own |
| 1. The R console (15 min) | R console | commands and objects, the history, the continuation prompt `+`; `head()`, `summary()`, `View()`, a plot, `?mean`; `q()` and what is kept |
| 2. Scripts in RStudio (20 min) | RStudio | a script run line by line, with the Environment beside it; starting again from the script (Restart R, Source); *Import Dataset*; a Shiny app, if there is time |
| 3. Documents (20 min) | RStudio | an R Markdown document written and knitted – and broken on purpose; an R Notebook and a Quarto document |
| 4. Jupyter notebooks (15 min) | Notebook | cells, tables and plots; cells run out of order, on purpose; the `.ipynb` file |
| 5. R in the terminal (15 min) | Terminal | `Rscript` with a script, with arguments, in a loop; the exit status of a script that fails; `R CMD BATCH` and `R` |
| 6. Which way, when? (10 min) | RStudio | the ways compared; asking the AI assistant – and checking its answer |

The model answers are in the page (*Show answer* under each question; see `showModelAnswers` below), so the questions are for practice, not for assessment.

## Before students use it

1. **Computers and browsers.** A laptop or desktop with a current Chrome, Edge, Firefox or Safari; 8 GB of memory is comfortable. Phones work, cramped.
2. **Network.** Besides your site, the students' browsers must reach `webr.r-wasm.org` (R itself: about 30 MB on the first visit, then kept in the browser's cache) and `repo.r-wasm.org` (R packages – knitr and markdown for knitting, shiny, readr and readxl are fetched from there when first needed), and the AI service each student uses (for Gemini: `generativelanguage.googleapis.com`).
3. **AI keys.** The assistant uses a key that each student enters; it is kept only in the browser tab (never in a file or in the browser's long-term storage). Decide which service the students use, and tell them before:
   - **Google Gemini**: a free key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (a Google account; 18 or over). The free tier allows a few requests per minute and a limited number per day for each model; when a model is busy or over its limit, the page asks the next model of `geminiFallbackModels`. Read Google's [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms) first. On the free tier Google may use what is sent to improve its products, and people may read it – but for users in the European Economic Area, Switzerland and the United Kingdom the data terms of the paid service apply to the free tier too. The same terms say that API clients made available to users in those regions may use only the paid service: whether a course page on which each student uses a key of their own counts as such a client is for your institution to decide.
   - **Anthropic (Claude)** – a paid key; or **any OpenAI-compatible service** that allows requests from web pages (CORS), such as one your university provides: the address, the model and, if it needs one, a key.
   - Check that the model names in `config.js` are current ([Gemini models](https://ai.google.dev/gemini-api/docs/models)).
4. **Shared computers.** Students' files are kept in the browser profile. Computers that wipe profiles at log-out lose them: tell students to download their work (*My files → Download all my files*, *My answers → Download my answers*), and to use *Start afresh* when they leave a shared computer.
5. **Personal and patient data.** The workbench is for public data. The instructions, the help and the AI settings tell students never to put personal or patient data into an AI tool.

## Put it on GitHub Pages

1. On GitHub, open the repository's *Settings → Pages → Build and deployment*: Source **Deploy from a branch**, branch **main**, folder **/ (root)**. Save. (The repository must be public unless your plan supports Pages for private repositories.)
2. After a minute the site is at `https://<owner>.github.io/<repository>/` – for this repository, `https://comparativechrono.github.io/R-workbench/`. Share that address.
3. The first time a browser opens it, the page loads once more by itself: it installs a small service worker (`isolation-sw.js`, next to `index.html`) that makes the page *cross-origin isolated* – which R needs to wait for what is typed (`readline()`, the question of `q()`) and to be interrupted with <kbd>Esc</kbd> – and that serves the Shiny apps R runs (see [Browser support and limits](#browser-support-and-limits)).

The empty file `.nojekyll` stops GitHub from processing the site. The folders `build/` and `test/` are not needed by the site; keep `assets/vendor/licenses/`. On any other web server: copy the folder (without `build/` and `test/` if you like); it needs no server-side code, but the address must be `https` (or `localhost`) for the service worker.

**Students' files belong to the address.** They are kept by the browser for the site's address: if the workbench moves to another address, students start with an empty home folder there (their files stay at the old address). All the GitHub Pages sites of one account share one address (`https://<owner>.github.io`): see `storePrefix` below.

## Try it on your own computer

Opening `index.html` directly (`file://…`) does not work – browsers block the Web Workers and the data files. Serve the folder instead:

```bash
cd R-workbench
python3 serve.py 8000        # then open http://localhost:8000
```

`serve.py` sends the headers of cross-origin isolation itself; the page installs its service worker there too, for the Shiny apps. Any other local server works too, as long as the address is `localhost` or `https`.

## Settings: `config.js`

`assets/js/config.js` is the only file to edit for most changes. **Never put an API key in it**: anyone can read the files of a public site.

| Setting | What it does |
| --- | --- |
| `courseTitle`, `courseSubtitle` | the name at the top of the page (and in the browser's tab) and the line under it |
| `storePrefix` | the prefix of everything kept in the browser (files, answers, settings). Sites at one address – all the GitHub Pages sites of an account – share their files when their `storePrefix` is the same (see [Writing a practical](#writing-a-practical)) |
| `hostname` | the computer's name in the terminal's prompt (`user@workbench`) |
| `showModelAnswers` | `true`: a *Show answer* button under each question; `false` hides them (they are still in the page's source, and `?answers` at the end of the address shows them) |
| `webrBase`, `rRepos` | where R comes from (webR 0.6.0), and the repositories of R packages (CRAN packages built for webR) |
| `biowasmBase` | the folder of the terminal's WebAssembly programs |
| `liveProvider`, `geminiModel`, `geminiFallbackModels`, `anthropicModel` | the AI service offered first and its models. Models are retired from time to time: put current ones here |
| `aiWaitSeconds` | how long the assistant waits for an answer before it asks the next model |
| `storageWarnMB` | from how many megabytes of files the page warns the student |

**R from your own server.** To serve R with the site – for a network that blocks `webr.r-wasm.org` – download the webR 0.6.0 release, unpack it as `assets/vendor/webr/`, and set `webrBase: 'assets/vendor/webr/'` (and keep its licence files with it). Packages still come from `rRepos`; mirroring them is possible with the [rwasm](https://r-wasm.github.io/rwasm/) tools.

## Writing a practical

### A new practical from the workbench

Make a copy of this repository for each practical – on GitHub, tick *Settings → General → Template repository* here once, then *Use this template → Create a new repository* – and change, in the copy:

- `build/chapters.py`: the chapters (below);
- `data/`: the files of the practical. Everything in `data/` (but `PROVENANCE.md`) is copied into each student's `~/data` on their first visit; a file that is there already is left alone. After adding files for students who have used the page before, raise `STARTERS_VERSION` in `build/make_page.py`. Say where the data come from in `data/PROVENANCE.md` and `THIRD_PARTY.md`;
- `assets/js/config.js`: `courseTitle`, `courseSubtitle` and `storePrefix`;
- `build/template.html`: the `<title>`, the description, and `data-page` of `<body>` – the name under which the page keeps its ticks, answers and settings.

Then run `python3 build/make_page.py`, try the page with `python3 serve.py`, and commit `index.html` with the rest.

**Sharing files between practicals.** Two practicals at one address (two GitHub Pages sites of one account) with the same `storePrefix` share the student's home folder – the files made in one practical are there in the next –, while a different `data-page` keeps their ticks and answers apart. Give a practical its own `storePrefix` if its files must be kept apart (*Start afresh* in a practical deletes the files of every practical that shares its `storePrefix`).

### The chapters

The chapters are written in Python, in `build/chapters.py`, with the helpers of `build/lib.py`; `python3 build/make_page.py` puts them into `index.html` (between `<!--CHAPTERS-->` and `<!--/CHAPTERS-->` of `build/template.html`) and stops with an error when two tasks, questions or headings have the same name. `chapters.ALL()` lists the chapters in order.

| Helper | What it makes |
| --- | --- |
| `chapter(id, num, title, tab, heading, minutes, lede, body)` | a chapter: its number and short title in the bar at the top, the workbench tab shown with it (`console`, `rstudio`, `notebook`, `terminal`, `editor`, `assistant`), its heading, the time it takes and its opening line |
| `activity(title, [task(...), ...])` | numbered steps |
| `task(id, html, auto='…', check='…')` | a step with a tick box that ticks itself – when an event of the page matches `auto`, or when the state named by `check` is true |
| `q(id, question, model_answer, accept=, hint=)` | a question with a box for the answer and a model answer; `accept` (regular expressions separated by `\|\|`) makes it a short answer that is checked |
| `mcq(id, question, [(option, correct, why), ...])` | a multiple-choice question |
| `callout(kind, title, html)` | a box: `info`, `warn`, `concept` or `ai` |
| `codefile(path, text)` | a file shown in the instructions, with *Create this file* (it opens in RStudio) and *Copy* |
| `rcode(code)`, `rcon(code)` | code with a *show me* button that types it into the R console (the student presses <kbd>Enter</kbd>) |
| `cmd(line)`, `show(line)` | the same for the terminal |
| `rsopen(path)`, `rsrun(code)`, `nbopen(path)`, `edit(path)` | buttons that open a file in RStudio, run code in RStudio's console, open a notebook, open a file in the Files tab |
| `bench(tab, label)`, `goto(id, label)` | buttons that show a tab of the workbench, or a chapter (or a heading) of the instructions |
| `prompt(text)` | a prompt for the AI assistant, shown in full, with a button that puts it into the assistant's box |

**`auto`** names an event and conditions on its fields: `=` equal, `~` contains, `>` and `<` numbers; `||` separates alternatives. For example `auto="r:input kind=console line~summary("` ticks when the student runs a command with `summary(` in the R console, and `auto="rstudio:knit path~report.Rmd||knit:done path~report.Rmd ok=true"` when that document has been knitted. A task ticks only while its chapter is shown. The events:

| Event | When | Fields |
| --- | --- | --- |
| `app:bench` | a tab of the workbench is shown | `name` |
| `r:input` | an R reads a line at its prompt | `kind` (`console`, `rstudio`, `rterm` – R in the terminal), `line` |
| `r:help`, `r:view`, `r:installed` | a help page; `View()`; packages installed | `kind`, `topic`, `package`; `kind`, `title`, `nrow`, `ncol`; `kind`, `pkgs` |
| `rcon:plot`, `rcon:quit`, `rcon:restart`, `rcon:shiny` | the R console: a new plot, `q()`, a restart, a Shiny app | `saved`; `title`, `running` |
| `rstudio:new`, `rstudio:doc`, `rstudio:saved`, `rstudio:close` | RStudio's documents | `kind` (`r`, `rmd`, `notebook`, `qmd`, `text`, `shiny`), `name`, `path` |
| `rstudio:chunk`, `rstudio:source` | a chunk ran; Source | `path`, `label`, `ok`, `outputs`; `path`, `echo` |
| `rstudio:knit`, `rstudio:preview`, `knit:done` | a document knitted or rendered; an R Notebook's preview | `path`, `output`, `kind`, `failed`; `ok`, `secs` |
| `rstudio:import`, `rstudio:plot`, `rstudio:tab`, `rstudio:shiny`, `rstudio:restart`, `rstudio:quit` | *Import Dataset*; a plot; a pane's tab; a Shiny app; Restart R; `q()` | `kind` (`base`, `readr`, `excel`), `path`, `name`; `n`; `pane`, `tab`; `title`, `running`; –; `saved` |
| `nb:open`, `nb:run`, `nb:saved`, `nb:restart`, `nb:download` | the Notebook tab | `path`; `code`, `ok`, `error`, `plot`, `table`; `runAll`; `format` |
| `term:command` | a command of the terminal has ended | `line`, `name` (the program), `sub`, `code` (the exit status), `cwd` |
| `editor:open`, `editor:view`, `editor:save`, `file:create` | the Files tab; *Create this file* | `path`, `name` |
| `ai:ask`, `ai:answer`, `ai:insert` | the AI tab | `tab`; `model`; `target` |
| `q:checked` | a question answered | `id`, `ok` |

**`check`** names a state, with its argument after a colon: `exists:scripts/penguins.R` (a file in `~`), `has:scripts/penguins.R|table\(penguins\$species\)` (a file's text matches a regular expression), `installed:shiny` (a package installed), `bench:console` (the tab shown). More can be added in `assets/js/page.js` (`MG.checks.name = (event, data, arg) => true or false`); the buttons' actions are there too (`MG.actions`).

Test a practical as a student would do it – `test/t_practical.py` does that for the starter practical.

## What students keep

Students' files, their ticks and answers, their settings and the list of packages they installed are kept in their browser's storage for the site (IndexedDB and local storage), on their computer, and are there when they come back in the same browser. They are not on any server, and nobody else can see them. Another browser, another computer or a private window has none of them, and clearing the browser's site data deletes them. *My files → Download all my files* downloads everything as a `.zip`; *My answers → Download my answers* the answers as an HTML page; every notebook downloads as `.ipynb`, and knitted documents are `.html` files among the student's files. The page warns when two of its tabs are open in one browser (both would write the same files).

## Privacy

The site sets no cookies and has no tracking or analytics. What leaves a student's computer: requests for the page (your server), R and its packages (`webr.r-wasm.org`, `repo.r-wasm.org`), what the student's own R code asks for (`download.file()`, `read.csv()` of a web address), and – only when the student connects a model – the questions, and what the student chooses to send with them, to the AI service of their choice, with their own key. Shiny apps run in the page: nothing of them leaves the computer. The name a person gives the workbench (the button at the top) is not sent: in what goes to the AI service it is replaced by `user` where it names the user.

## Browser support and limits

Current Chrome, Edge, Firefox and Safari. R in the browser is R 4.6.0 (webR 0.6.0), with these differences from R on a computer – the AI assistant knows them too:

- **One thread, a few gigabytes.** Each R runs on one processor core, in a worker of its own with WebAssembly's limit on memory; every R of the page (console, RStudio, notebooks, terminal, knitting) takes memory of its own. No parallel processes.
- **Packages** come from the webR repository – a large part of CRAN, ggplot2, dplyr, tidyr, readr, readxl and stringr among them, but not every package with compiled code. R's recommended packages (MASS, Matrix, lattice …) are not built in: they are installed like any other. Bioconductor's repository is not set up.
- **No other programs.** `system()`, `system2()` and `shell()` stop with a message: commands go in the Terminal tab. There is no pandoc or LaTeX, so documents knit to HTML only: an R Markdown document is knitted by knitr and made into HTML by R's markdown package (`rmarkdown::render()` is not used), and a document that asks for `pdf_document` or `word_document` is knitted to HTML with a note in the log. Quarto documents are rendered the same way – R chunks with their `#|` options, the title, author, date and table of contents – without Quarto's own programs: its cross-references, callouts, other languages and other formats are not there. No RStudio projects, Git or add-ins; no Python (and so no reticulate).
- **The web from R**: only sites that allow requests from web pages (CORS), and only GET requests.
- **Shiny apps** run in R in the page, through the service worker: they need it (so `https` or `localhost`, and a browser that allows service workers – some private windows do not). One app at a time in each R, which is busy while the app runs, as in RStudio; *Stop* (or <kbd>Esc</kbd>) stops it.
- **The RStudio tab is an imitation** for teaching: it has what the practicals use – the panes, menus, dialogs and messages of RStudio – but it is not RStudio.

**Cross-origin isolation.** R can wait for what is typed (`readline()`, `browser()`, the question of `q()`) and be interrupted with <kbd>Esc</kbd> only in a page served with the headers `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`. GitHub Pages cannot send them, so `assets/js/isolation.js` registers `isolation-sw.js`, a service worker that adds them to the page and its workers (it caches nothing): on the first visit the page loads once more by itself, and is isolated from then on. Isolation needs `https` (or `localhost`) and a browser that allows service workers there; where it is missing, R works but cannot wait for typed answers or be interrupted, and Shiny apps cannot be shown. `?isolation=off` at the end of the address removes the service worker. It was tested in Chromium; test Firefox and Safari on your students' computers.

## How it was tested

The workbench was tested in Chromium (Playwright) on 15 October 2026, with R and its packages downloaded from webR's own servers, by the scripts in `test/` – over 300 checks in all:

| Script | What it checks |
| --- | --- |
| `t_rsession.py` | the R sessions on their own: the console's output as R writes it, prompts, warnings and errors, plots, help, `View()`, `readline()`, <kbd>Esc</kbd>, the files shared with the page, the shared library of installed packages, separate memories, `q()` and `.RData` |
| `t_rstudio.py`, `t_rstudio2.py` | the RStudio tab: the panes, scripts, chunks and their output, the Environment, Plots, `View()`, Help; R Markdown from *New File*, knitting (knitr and markdown installed when first needed), an R Notebook and its `.nb.html`, Quarto, *Import Dataset* (base, readr, readxl) |
| `t_shiny.py` | a Shiny app run from RStudio, in the Viewer, its inputs working through the page, the console busy until *Stop* – served by `serve.py`, with the service worker |
| `t_notebook.py` | notebooks: cells, output, tables, plots, errors, warnings, help, files, the variables, `readline()`, Stop and Restart, the saved `.ipynb`, and that the notebooks' R is not RStudio's |
| `t_terminal_r.py` | `Rscript` (scripts, `-e`, arguments, errors and exit status, `Rplots.pdf`), `R CMD BATCH`, R reading from a pipe, and R's console in the terminal |
| `t_files.py` | the Files tab: the tree, tables, the editor, the buttons to the other tabs, PDFs, upload, move and delete, and the tab at a phone's width |
| `t_assistant.py` | the AI tab, against stand-ins of the AI services with a fake key: the key kept in memory only, the context sent (never what is in a data file), code into each tab, the questions that errors send, offline help |
| `t_practical.py` | the starter practical done as a student would do it: every step of every chapter, and that each step ticked itself |

To run them: `pip install playwright`, `playwright install chromium`, then `cd test` and `python3 t_rstudio.py` (and so on); pictures of the page go into `test/out/`. The AI assistant was tested only against stand-ins: before you rely on it, try it with a real key on the network the students use.

## Files

```
index.html             the page (built by build/make_page.py)
isolation-sw.js        the service worker: cross-origin isolation and Shiny apps (keep it next to index.html)
assets/js/             the workbench: config.js (settings), page.js (the actions and checks of the instructions),
                       rsession.js (the R sessions), rconsole.js, rstudio.js and rsource.js (RStudio), knit.js,
                       shiny.js, notebook.js and kernels.js, terminal.js and shell*.js, editor.js (Files),
                       assistant.js (AI), tutorial.js (the instructions)
assets/css/            styles
assets/vendor/         bundled programs and libraries, with their licences (see THIRD_PARTY.md); licenses/: the
                       licence texts and the source code of the GNU programs
data/                  the files copied into each student's ~/data, and PROVENANCE.md
build/                 make_page.py, chapters.py (the starter practical), lib.py (the helpers), template.html
test/                  the tests (Playwright)
serve.py               a small local web server (optional)
THIRD_PARTY.md         the third-party software and data, their licences and sources
```

## Credits and licences

The workbench runs R through [webR](https://github.com/r-wasm/webr) (R is under the GNU GPL), with the R packages that students install from the webR repository – knitr, markdown, shiny, readr and readxl among them; the terminal's GNU tools were compiled to WebAssembly by the [Biowasm](https://biowasm.com) project or for the course; the editors are [CodeMirror](https://codemirror.net/5/); Markdown is read by marked and made safe by DOMPurify; `.zip` and `.xlsx` files are read by JSZip, and PDFs drawn by PDF.js. The way Shiny apps run in the page follows [Shinylive](https://github.com/posit-dev/shinylive) (MIT). Each keeps its own licence: **[THIRD_PARTY.md](THIRD_PARTY.md)** lists them all, with versions, licences, origins and the local changes. The GNU programs are under the GNU General Public License: their source code is in `assets/vendor/licenses/sources/` – keep it with the site.

The RStudio tab imitates the RStudio IDE so that what students learn carries over to it; it contains no part of RStudio, and it is not made or endorsed by Posit (its *About* box says so). RStudio is a trademark of Posit Software, PBC. The Notebook tab reads and writes Jupyter's `.ipynb` format.

The penguin data are from the palmerpenguins package (Horst, Hill & Gorman 2020), collected by Dr Kristen Gorman and the Palmer Station Long Term Ecological Research Program (Gorman, Williams & Fraser 2014, *PLoS ONE* 9(3): e90081), CC0 – see `data/PROVENANCE.md`.
