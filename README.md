# R workbench

**A browser-based workbench for R practicals. It brings together the standard R console, an RStudio-style IDE, Jupyter-style notebooks, R Markdown, R Notebook and Quarto documents, Shiny apps, a terminal with `Rscript`, a file manager with a text editor, and an AI assistant, with the instructions for the practical alongside them.**

Everything runs in the student's web browser. R is provided by webR, a version of R 4.6 compiled to WebAssembly, and every tab that uses R (the console, RStudio, the notebooks, `Rscript` in the terminal, knitting and Shiny) runs a genuine R session. Students don't need to install anything, there is no server-side code, and students' files are stored in their own browser. Because the site is static (just HTML, CSS and JavaScript), it can be hosted for free on **GitHub Pages** or on any ordinary web server.

The workbench is intended as the base for the course's R practicals. Each practical uses this page with its own chapters in the left-hand pane (see [Writing a practical](#writing-a-practical)). It comes with a short starter practical, *Four ways to use R*.

---

## Contents

1. [What's in the workbench](#whats-in-the-workbench)
2. [The starter practical](#the-starter-practical)
3. [Before students use it](#before-students-use-it)
4. [Publishing it on GitHub Pages](#publishing-it-on-github-pages)
5. [Trying it on your own computer](#trying-it-on-your-own-computer)
6. [Settings in `config.js`](#settings-in-configjs)
7. [Writing a practical](#writing-a-practical)
8. [What students keep](#what-students-keep)
9. [Privacy](#privacy)
10. [Browser support and limitations](#browser-support-and-limitations)
11. [How it was tested](#how-it-was-tested)
12. [Files](#files)
13. [Credits and licences](#credits-and-licences)

---

## What's in the workbench

The workbench is a single page, `index.html`. The **instructions** are on the left: chapters made up of steps that tick themselves off as the student completes them, and questions with model answers. The **workbench** itself is on the right. Students can hide the instructions (with the button at the top left, or <kbd>Ctrl</kbd>+<kbd>\</kbd>) and make the workbench fill the screen. On a phone, the workbench opens on top of the instructions.

| Tab | What it contains |
| --- | --- |
| **R console** | The standard R console, as you get it when you install R. It has a command history (<kbd>↑</kbd>), name completion (<kbd>Tab</kbd>) and <kbd>Esc</kbd> to interrupt R. Each plot opens in its own graphics window, help pages open in a help window and `View()` opens the data in a separate window. `q()` asks whether to save the workspace (`.RData`). The tab deliberately has no script editor and no list of objects, so that students see what it is like to work in the console on its own. |
| **RStudio** | An IDE modelled on RStudio and made for teaching. The **Source** pane edits R scripts (with Run and Source), R Markdown documents (whose chunks show their output underneath, and which can be knitted), R Notebooks (with Preview and an `.nb.html` file), Quarto documents (with Render) and text files, and data opened with `View()` appear in tabs of their own. There is a **Console** (with Terminal and Background Jobs tabs), an **Environment** pane (with *Import Dataset* for CSV files, using base R or readr, and for Excel files) and a History pane, and **Files, Plots, Packages, Help and Viewer** panes. The menus, keyboard shortcuts and Global Options follow RStudio. *New File → Shiny Web App* and *Run App* run a Shiny app in the Viewer. |
| **Notebook** | Jupyter-style notebooks in R (`.ipynb` files, run the way Jupyter runs them with its R kernel). They have code and Markdown cells, plots, tables, errors that stop the cell, Restart, Run All and Jupyter's keyboard shortcuts, and they can be downloaded as `.ipynb`, `.R` or `.html` files. |
| **Terminal** | A bash-like shell with `Rscript` (for running a script or `-e` code, with arguments and an exit status; plots go to `Rplots.pdf`), `R CMD BATCH` (which writes an `.Rout` record of the run) and `R` (R's console inside the terminal). It also has the GNU text tools, such as `grep`, `sed`, `awk`, `sort`, `cut` and `diff`, compiled to WebAssembly. Typing `help` lists them all. |
| **Files** | The student's home folder (`~`, which is `/home/user`). It shows the folder tree (with upload, download – a folder downloads as a `.zip` file – and new, rename, move and delete), an editor for scripts and documents, and viewers for tables (which can be sorted, searched and filtered), pictures, PDFs and HTML reports. Buttons above each file send it to another tab: an R script to RStudio, `Rscript` or `source()`, a document to Knit, or a table to *Import Dataset*. |
| **AI** | An AI assistant set up as an R tutor. In **Chat**, students ask questions, and each question can include whatever context they choose to send: the end of the console, the document open in RStudio, the notebook's code, their last terminal commands and the names of their files (but never the contents of a data file). Code in the answers can be sent to the console, RStudio, a notebook, the terminal or a file with one click. Under an error in any tab, *Ask the AI assistant about this error* sends the code and the error message. The **Agent** carries out a task using `Rscript` in the terminal, working in a folder of its own, and keeps a record of every step. Students connect a model of their own (Google Gemini, Anthropic's Claude, or an OpenAI-compatible service). |

**Each tab has its own R session**, just as separate R programs on a computer would. An object created in the R console doesn't exist in RStudio, the notebook or a run of `Rscript`, and *Knit* runs a document in a brand new R session. What the sessions do share is the student's files (they all use the same home folder) and the packages the student has installed: a package installed in one tab can be loaded in all the others, and it is still there the next time the student visits.

## The starter practical

*Four ways to use R* takes about 1 hour 45 minutes and has 47 steps and 11 questions in 7 chapters. In each chapter students do a small part of the same analysis of the Palmer penguins data (in `~/data/penguins.csv`, and also built into R 4.6 as `penguins`) in a different way, so that they can see what each way of using R is good for and where it falls short.

| Chapter | Tab | What students do |
| --- | --- | --- |
| 0. Start here (10 min) | R console | Find out about the four ways of using R and how the page works, and learn that each tab has its own R session |
| 1. The R console (15 min) | R console | Create objects, use the command history and meet the continuation prompt `+`; look at the data with `head()`, `summary()` and `View()`, draw a plot and use `?mean`; quit with `q()` and see what is kept |
| 2. Scripts in RStudio (20 min) | RStudio | Run a script line by line with the Environment pane alongside; start again from the script (Restart R, then Source); use *Import Dataset*; and, if there is time, run a Shiny app |
| 3. Documents (20 min) | RStudio | Write and knit an R Markdown document, then break it on purpose; try an R Notebook and a Quarto document |
| 4. Jupyter notebooks (15 min) | Notebook | Run cells that produce tables and plots, deliberately run cells out of order, and download the `.ipynb` file |
| 5. R in the terminal (15 min) | Terminal | Run a script with `Rscript`, with arguments and in a loop; look at the exit status of a script that fails; try `R CMD BATCH` and `R` |
| 6. Which way, when? (10 min) | RStudio | Compare the different ways of using R, and ask the AI assistant a question (and check its answer) |

The model answers are included in the page (students see them with *Show answer* under each question; see `showModelAnswers` below), so the questions are meant for practice rather than assessment.

## Before students use it

1. **Computers and browsers.** Students need a laptop or desktop computer with a current version of Chrome, Edge, Firefox or Safari, and 8 GB of memory is comfortable. The workbench also works on a phone, although the screen is cramped.
2. **Network.** As well as your site, students' browsers must be able to reach `webr.r-wasm.org` (for R itself, which is about 30 MB on the first visit and is then kept in the browser's cache) and `repo.r-wasm.org` (for R packages: knitr and markdown for knitting, shiny, readr and readxl are downloaded from there the first time they are needed). They also need to reach the AI service that each student uses (for Gemini, that is `generativelanguage.googleapis.com`).
3. **AI keys.** The assistant uses a key that each student enters themselves. The key is only kept in the browser tab, never in a file or in the browser's long-term storage. Decide in advance which service your students should use, and tell them:
   - **Google Gemini**: students can get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (they need a Google account and must be 18 or over). The free tier allows a few requests per minute and a limited number per day for each model. When a model is busy or over its limit, the page tries the next model in `geminiFallbackModels`. Please read Google's [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms) first. On the free tier, Google may use what is sent to improve its products, and people may read it. However, for users in the European Economic Area, Switzerland and the United Kingdom, the data terms of the paid service apply to the free tier as well. The same terms say that API clients made available to users in those regions may only use the paid service. Whether a course page on which each student uses their own key counts as such a client is a question for your institution.
   - **Anthropic (Claude)** needs a paid key. Alternatively, students can use **any OpenAI-compatible service** that accepts requests from web pages (CORS), such as one provided by your university; they then enter its address, the model and, if needed, a key.
   - Check that the model names in `config.js` are still current (see the list of [Gemini models](https://ai.google.dev/gemini-api/docs/models)).
4. **Shared computers.** Students' files are stored in the browser profile, so computers that wipe profiles when students log out will lose them. Tell students to download their work before they leave (with *My files → Download all my files* and *My answers → Download my answers*), and to use *Start afresh* when they finish on a shared computer.
5. **Personal and patient data.** The workbench is meant for public data. The instructions, the help and the AI settings all tell students never to put personal or patient data into an AI tool.

## Publishing it on GitHub Pages

1. On GitHub, open the repository's *Settings → Pages → Build and deployment* page. Under Source choose **Deploy from a branch**, then choose the branch **main** and the folder **/ (root)**, and click Save. (The repository needs to be public, unless your GitHub plan supports Pages for private repositories.)
2. After a minute or so, the site will be available at `https://<owner>.github.io/<repository>/`, which for this repository is `https://comparativechrono.github.io/R-workbench/`. That is the address to give to students.
3. The first time a browser opens the site, the page reloads itself once. This installs a small service worker (`isolation-sw.js`, which sits next to `index.html`). The service worker makes the page *cross-origin isolated*, which R needs in order to wait for typed input (for `readline()`, or the question that `q()` asks) and to be interrupted with <kbd>Esc</kbd>. It also serves the Shiny apps that R runs (see [Browser support and limitations](#browser-support-and-limitations)).

The empty file `.nojekyll` stops GitHub from processing the site. The site itself doesn't need the `build/` and `test/` folders, but do keep `assets/vendor/licenses/`. To host the workbench on a different web server, just copy the folder (you can leave out `build/` and `test/`). It doesn't need any server-side code, but its address must use `https` (or be `localhost`) for the service worker to work.

**Students' files belong to the site's address.** The browser stores them for that address, so if the workbench moves to a different address, students will start with an empty home folder there (their files stay at the old address). All the GitHub Pages sites of one account share the same address (`https://<owner>.github.io`), which matters when you have more than one practical: see `storePrefix` below.

## Trying it on your own computer

Opening `index.html` directly from your disk (`file://…`) doesn't work, because browsers block the Web Workers and the data files. Instead, serve the folder with a local web server:

```bash
cd R-workbench
python3 serve.py 8000        # then open http://localhost:8000
```

`serve.py` sends the cross-origin isolation headers itself, and the page also installs its service worker there, which the Shiny apps need. Any other local web server will work too, as long as the address is `localhost` or uses `https`.

## Settings in `config.js`

`assets/js/config.js` is the only file you need to edit for most changes. **Never put an API key in it**, because anyone can read the files of a public site.

| Setting | What it does |
| --- | --- |
| `courseTitle`, `courseSubtitle` | The name shown at the top of the page (and in the browser tab), and the line underneath it |
| `storePrefix` | The prefix for everything the page saves in the browser (files, answers and settings). Sites at the same address, such as all the GitHub Pages sites of one account, share their files if their `storePrefix` is the same (see [Writing a practical](#writing-a-practical)) |
| `hostname` | The computer name shown in the terminal's prompt (`user@workbench`) |
| `showModelAnswers` | When this is `true`, there is a *Show answer* button under each question. Set it to `false` to hide the model answers (they are still in the page's source code, and adding `?answers` to the address shows them) |
| `webrBase`, `rRepos` | Where R is downloaded from (webR 0.6.0), and the repositories that R packages are installed from (CRAN packages built for webR) |
| `biowasmBase` | The folder containing the terminal's WebAssembly programs |
| `liveProvider`, `geminiModel`, `geminiFallbackModels`, `anthropicModel` | The AI service offered first, and the models to use. Models are retired from time to time, so keep these up to date |
| `aiWaitSeconds` | How long the assistant waits for an answer before it tries the next model |
| `storageWarnMB` | How many megabytes of files a student can store before the page warns them |

**Serving R from your own server.** If your network blocks `webr.r-wasm.org`, you can host R alongside the site instead. Download the webR 0.6.0 release, unpack it as `assets/vendor/webr/`, set `webrBase: 'assets/vendor/webr/'`, and keep its licence files with it. Packages will still come from `rRepos`; if you need to mirror those as well, the [rwasm](https://r-wasm.github.io/rwasm/) tools can do it.

## Writing a practical

### Making a new practical from the workbench

For each new practical, make a copy of this repository. The easiest way is to tick *Settings → General → Template repository* on this repository once, and then use *Use this template → Create a new repository* for each practical. Then, in the copy, change:

- `build/chapters.py`, which contains the chapters (see below);
- the files in `data/`, which are the practical's data. Everything in `data/` (except `PROVENANCE.md`) is copied into each student's `~/data` folder on their first visit; files that a student already has are left alone. If you add files after students have started using the page, increase `STARTERS_VERSION` in `build/make_page.py` so that they receive the new files. Record where the data came from in `data/PROVENANCE.md` and `THIRD_PARTY.md`;
- `courseTitle`, `courseSubtitle` and `storePrefix` in `assets/js/config.js`;
- in `build/template.html`, the `<title>`, the description, and the `data-page` attribute of `<body>`, which is the name under which the page saves its ticks, answers and settings.

Then run `python3 build/make_page.py`, try the page with `python3 serve.py`, and commit the new `index.html` together with your other changes.

**Sharing files between practicals.** If two practicals are hosted at the same address (for example, two GitHub Pages sites of one account) and have the same `storePrefix`, they share the student's home folder, so files made in one practical are available in the next. Giving them different `data-page` values keeps their ticks and answers separate. If a practical's files must be kept apart from the others, give it its own `storePrefix`. Note that *Start afresh* in one practical deletes the files of every practical that shares its `storePrefix`.

### Writing the chapters

The chapters are written in Python, in `build/chapters.py`, using the helper functions in `build/lib.py`. Running `python3 build/make_page.py` puts them into `index.html` (between the `<!--CHAPTERS-->` and `<!--/CHAPTERS-->` markers in `build/template.html`). It stops with an error if two tasks, questions or headings have the same name. `chapters.ALL()` lists the chapters in order.

| Helper | What it produces |
| --- | --- |
| `chapter(id, num, title, tab, heading, minutes, lede, body)` | A chapter. `num` and `title` appear in the chapter bar at the top, `tab` is the workbench tab shown with the chapter (`console`, `rstudio`, `notebook`, `terminal`, `editor` or `assistant`), and `heading`, `minutes` and `lede` give its heading, how long it takes and its opening sentence |
| `activity(title, [task(...), ...])` | A numbered list of steps |
| `task(id, html, auto='…', check='…')` | A step with a tick box. It ticks itself when an event on the page matches `auto`, or when the condition named by `check` is true |
| `q(id, question, model_answer, accept=, hint=)` | A question with a box for the student's answer and a model answer. If `accept` is given (regular expressions separated by `\|\|`), the answer is a short answer that is checked automatically |
| `mcq(id, question, [(option, correct, why), ...])` | A multiple-choice question |
| `callout(kind, title, html)` | A highlighted box: `info`, `warn`, `concept` or `ai` |
| `codefile(path, text)` | A file shown in the instructions, with a *Create this file* button (which opens the file in RStudio) and a *Copy* button |
| `rcode(code)`, `rcon(code)` | Code with a *show me* button that types it into the R console, ready for the student to press <kbd>Enter</kbd> |
| `cmd(line)`, `show(line)` | The same, but for the terminal |
| `rsopen(path)`, `rsrun(code)`, `nbopen(path)`, `edit(path)` | Buttons that open a file in RStudio, run code in RStudio's Console, open a notebook, or open a file in the Files tab |
| `bench(tab, label)`, `goto(id, label)` | Buttons that show a tab of the workbench, or a chapter (or a heading) of the instructions |
| `prompt(text)` | A prompt for the AI assistant, shown in full, with a button that puts it into the assistant's message box |

**`auto`** names an event, optionally followed by conditions on its fields: `=` means "equals", `~` means "contains", and `>` and `<` compare numbers. Alternatives are separated by `||`. For example, `auto="r:input kind=console line~summary("` ticks the step when the student runs a command containing `summary(` in the R console, and `auto="rstudio:knit path~report.Rmd||knit:done path~report.Rmd ok=true"` ticks it once that document has been knitted. A step only ticks while its chapter is on screen. These are the events:

| Event | When it happens | Fields |
| --- | --- | --- |
| `app:bench` | A tab of the workbench is shown | `name` |
| `r:input` | An R session reads a line at its prompt | `kind` (`console`, `rstudio`, or `rterm` for R in the terminal), `line` |
| `r:help`, `r:view`, `r:installed` | A help page is shown; `View()` is used; packages are installed | `kind`, `topic`, `package`; `kind`, `title`, `nrow`, `ncol`; `kind`, `pkgs` |
| `rcon:plot`, `rcon:quit`, `rcon:restart`, `rcon:shiny` | In the R console: a new plot, `q()`, a restart, a Shiny app | `saved`; `title`, `running` |
| `rstudio:new`, `rstudio:doc`, `rstudio:saved`, `rstudio:close` | RStudio's documents are created, shown, saved or closed | `kind` (`r`, `rmd`, `notebook`, `qmd`, `text` or `shiny`), `name`, `path` |
| `rstudio:chunk`, `rstudio:source` | A chunk has been run; Source has been used | `path`, `label`, `ok`, `outputs`; `path`, `echo` |
| `rstudio:knit`, `rstudio:preview`, `knit:done` | A document has been knitted or rendered; an R Notebook has been previewed | `path`, `output`, `kind`, `failed`; `ok`, `secs` |
| `rstudio:import`, `rstudio:plot`, `rstudio:tab`, `rstudio:shiny`, `rstudio:restart`, `rstudio:quit` | *Import Dataset*; a new plot; a pane's tab is shown; a Shiny app; Restart R; `q()` | `kind` (`base`, `readr` or `excel`), `path`, `name`; `n`; `pane`, `tab`; `title`, `running`; –; `saved` |
| `nb:open`, `nb:run`, `nb:saved`, `nb:restart`, `nb:download` | In the Notebook tab | `path`; `code`, `ok`, `error`, `plot`, `table`; `runAll`; `format` |
| `term:command` | A command in the terminal has finished | `line`, `name` (the program), `sub`, `code` (the exit status), `cwd` |
| `editor:open`, `editor:view`, `editor:save`, `file:create` | In the Files tab; *Create this file* | `path`, `name` |
| `ai:ask`, `ai:answer`, `ai:insert` | In the AI tab | `tab`; `model`; `target` |
| `q:checked` | A question has been answered | `id`, `ok` |

**`check`** names a condition, with its argument after a colon: `exists:scripts/penguins.R` (a file exists in `~`), `has:scripts/penguins.R|table\(penguins\$species\)` (a file's text matches a regular expression), `installed:shiny` (a package has been installed) or `bench:console` (that tab is being shown). You can add your own conditions in `assets/js/page.js` (`MG.checks.name = (event, data, arg) => true or false`), which is also where the buttons' actions are defined (`MG.actions`).

It is worth testing a new practical by working through it as a student would; `test/t_practical.py` does this for the starter practical.

## What students keep

Students' files, ticks, answers and settings, and the list of packages they have installed, are stored in the browser's storage for the site (IndexedDB and local storage) on their own computer, and they are still there when the student comes back in the same browser. Nothing is stored on a server, and nobody else can see them. A different browser, a different computer or a private window won't have them, and clearing the browser's data for the site deletes them. *My files → Download all my files* downloads everything as a `.zip` file, and *My answers → Download my answers* downloads the answers as a web page. Notebooks can also be downloaded as `.ipynb` files, and knitted documents are saved as `.html` files in the student's files. The page warns students if it is open in two tabs of the same browser, because both would write to the same files.

## Privacy

The site sets no cookies and has no tracking or analytics. The only things that leave a student's computer are: requests for the page itself (from your server); R and its packages (from `webr.r-wasm.org` and `repo.r-wasm.org`); anything the student's own R code requests (for example with `download.file()`, or `read.csv()` given a web address); and, only if the student connects an AI model, their questions and whatever context they choose to send with them, which go to the AI service they chose, using their own key. Shiny apps run inside the page, so nothing from them leaves the computer. The name a student gives the workbench (with the button at the top) is not sent anywhere: in anything that goes to the AI service, it is replaced by `user` wherever it refers to the student.

## Browser support and limitations

The workbench works in current versions of Chrome, Edge, Firefox and Safari. R in the browser is R 4.6.0 (webR 0.6.0), and it differs from R on a computer in a few ways. The AI assistant knows about these differences too.

- **One thread and limited memory.** Each R session runs on a single processor core, in a separate worker with WebAssembly's memory limit of a few gigabytes, and each tab's R session takes memory of its own. R cannot start parallel processes.
- **Packages** are installed from the webR repository, which has a large part of CRAN (including ggplot2, dplyr, tidyr, readr, readxl and stringr), although not every package with compiled code. R's recommended packages (MASS, Matrix, lattice and so on) are not built in, so they have to be installed like any other package. Bioconductor's repository is not set up.
- **No other programs.** `system()`, `system2()` and `shell()` stop with a message telling the student to use the Terminal tab instead. Pandoc and LaTeX are not available, so documents can only be knitted to HTML: R Markdown documents are knitted by knitr and converted to HTML by R's markdown package (`rmarkdown::render()` is not used), and a document that asks for `pdf_document` or `word_document` is knitted to HTML, with a note in the log. Quarto documents are rendered in the same way, without Quarto's own programs. Their R chunks, chunk options written with `#|`, title, author, date and table of contents all work, but Quarto's cross-references, callouts, other languages and other output formats do not. There are no RStudio projects, Git or add-ins, and there is no Python (so reticulate is not available).
- **Downloading from R** only works from sites that allow requests from web pages (CORS), and only GET requests are possible.
- **Shiny apps** run in R inside the page, with the help of the service worker. This means they need `https` or `localhost`, and a browser that allows service workers (some private windows don't). Each R session can run one app at a time, and, as in RStudio, the R session is busy while the app runs; *Stop* (or <kbd>Esc</kbd>) ends the app.
- **The RStudio tab is an imitation** made for teaching. It has the panes, menus, dialogs and messages of RStudio that the practicals need, but it is not RStudio itself.

**Cross-origin isolation.** R can only wait for typed input (for `readline()`, `browser()` or the question that `q()` asks) and be interrupted with <kbd>Esc</kbd> if the page is served with the headers `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`. GitHub Pages can't send these headers, so `assets/js/isolation.js` registers `isolation-sw.js`, a service worker that adds them to the page and its workers (it doesn't cache anything). On a student's first visit, the page reloads itself once and is isolated from then on. Isolation needs `https` (or `localhost`) and a browser that allows service workers there. Without it, R still works, but it can't wait for typed answers or be interrupted, and Shiny apps can't be shown. Adding `?isolation=off` to the end of the address removes the service worker. This was tested in Chromium, so please test Firefox and Safari on the computers your students will use.

## How it was tested

The workbench was tested in Chromium (using Playwright) on 15 October 2026, with R and its packages downloaded from webR's own servers, using the scripts in the `test/` folder. Between them they make more than 300 checks:

| Script | What it checks |
| --- | --- |
| `t_rsession.py` | The R sessions on their own: the console's output as R writes it, prompts, warnings and errors, plots, help, `View()`, `readline()`, <kbd>Esc</kbd>, the files shared with the page, the shared library of installed packages, separate memories, and `q()` and `.RData` |
| `t_rstudio.py`, `t_rstudio2.py` | The RStudio tab: the panes, scripts, chunks and their output, the Environment, Plots, `View()` and Help; R Markdown from *New File*, knitting (with knitr and markdown installed the first time they are needed), an R Notebook and its `.nb.html` file, Quarto, and *Import Dataset* (with base R, readr and readxl) |
| `t_shiny.py` | A Shiny app run from RStudio and shown in the Viewer, with its inputs working through the page and the console busy until *Stop* is pressed. The page is served by `serve.py`, with the service worker |
| `t_notebook.py` | Notebooks: cells, output, tables, plots, errors, warnings, help, files, the list of variables, `readline()`, Stop and Restart, the saved `.ipynb` file, and that the notebooks' R session is separate from RStudio's |
| `t_terminal_r.py` | `Rscript` (scripts, `-e`, arguments, errors and exit statuses, `Rplots.pdf`), `R CMD BATCH`, R reading commands from a pipe, and R's console in the terminal |
| `t_files.py` | The Files tab: the folder tree, tables, the editor, the buttons that send files to the other tabs, PDFs, uploading, moving and deleting, and the tab at the width of a phone |
| `t_assistant.py` | The AI tab, tested against stand-ins for the AI services with a fake key: that the key is only kept in memory, the context that is sent (never the contents of a data file), sending code to each tab, the questions that errors send, and the offline help |
| `t_practical.py` | The starter practical, worked through as a student would do it: every step of every chapter, checking that each step ticks itself |

To run the tests, install Playwright (`pip install playwright`, then `playwright install chromium`), go into the `test` folder and run each script, for example `python3 t_rstudio.py`. Screenshots of the page are saved in `test/out/`. The AI assistant has only been tested against stand-ins, so please try it with a real key, on the network your students will use, before you rely on it.

## Files

```
index.html             the page (built by build/make_page.py)
isolation-sw.js        the service worker for cross-origin isolation and Shiny apps (keep it next to index.html)
assets/js/             the workbench's code: config.js (settings), page.js (the actions and checks used by the
                       instructions), rsession.js (the R sessions), rconsole.js, rstudio.js and rsource.js (the R
                       console and RStudio), knit.js, shiny.js, notebook.js and kernels.js, terminal.js and the
                       shell*.js files, editor.js (Files), assistant.js (AI) and tutorial.js (the instructions)
assets/css/            the style sheets
assets/vendor/         the bundled programs and libraries, with their licences (see THIRD_PARTY.md); licenses/
                       holds the licence texts and the source code of the GNU programs
data/                  the files copied into each student's ~/data folder, and PROVENANCE.md
build/                 make_page.py, chapters.py (the starter practical), lib.py (the helper functions) and
                       template.html
test/                  the tests (Playwright)
serve.py               a small local web server (optional)
THIRD_PARTY.md         the third-party software and data, with their licences and sources
```

## Credits and licences

The workbench runs R using [webR](https://github.com/r-wasm/webr) (R itself is licensed under the GNU GPL), together with the R packages that students install from the webR repository, including knitr, markdown, shiny, readr and readxl. The GNU tools in the terminal were compiled to WebAssembly by the [Biowasm](https://biowasm.com) project or for this course. The editors use [CodeMirror](https://codemirror.net/5/), Markdown is converted by marked and made safe by DOMPurify, `.zip` and `.xlsx` files are read with JSZip, and PDFs are displayed with PDF.js. The way Shiny apps run inside the page follows the design of [Shinylive](https://github.com/posit-dev/shinylive) (MIT licence). Each of these keeps its own licence, and **[THIRD_PARTY.md](THIRD_PARTY.md)** lists them all, with their versions, licences, origins and any local changes. The GNU programs are licensed under the GNU General Public License, and their source code is included in `assets/vendor/licenses/sources/`, which should be kept with the site.

The RStudio tab imitates the RStudio IDE so that what students learn carries over to the real program. It contains no part of RStudio, and it is not made or endorsed by Posit (as its *About* box says). RStudio is a trademark of Posit Software, PBC. The Notebook tab reads and writes Jupyter's `.ipynb` format.

The penguin data come from the palmerpenguins package (Horst, Hill & Gorman 2020). They were collected by Dr Kristen Gorman and the Palmer Station Long Term Ecological Research Program (Gorman, Williams & Fraser 2014, *PLoS ONE* 9(3): e90081) and are released under CC0; see `data/PROVENANCE.md` for details.
