# Third-party software, data and source provenance

The R workbench bundles independently licensed programs and libraries, and uses others that the student's browser loads at run time. Each keeps its own licence: the MIT licence of the Biowasm build framework does **not** relicense the programs it compiled, and none of the licences below applies to the workbench's own text and code. Keep each component's notices and licence files when copying or redistributing its files.

## Command-line programs of the terminal (WebAssembly, run in the browser)

These are the real programs, compiled to WebAssembly. They run on the student's own computer, inside the web page – in the Terminal tab, also for the commands of the AI assistant's agent. Each folder `assets/vendor/biowasm/NAME/VERSION/` holds the program (`.wasm` and its JavaScript loader), its licence, a `NOTICE.txt` (origin, local changes and where its source is) and `SHA256SUMS`. (The folder of the base module has a notice and checksums only: its licence is the Biowasm licence in `assets/vendor/biowasm/LICENSE.txt`. The four files at the top of `assets/vendor/biowasm/` – the runner, its licence and the two descriptions of the local changes – have a `SHA256SUMS` of their own there.)

| Program | Version | Licence | Folder | Upstream source |
| --- | --- | --- | --- | --- |
| **GNU coreutils**: `cat comm cut date fold head join md5sum paste seq shuf sort tail tee tr uniq wc` | 8.32 | **GNU GPL 3 or later** | [coreutils/8.32](assets/vendor/biowasm/coreutils/8.32/) | [release source](https://ftp.gnu.org/gnu/coreutils/coreutils-8.32.tar.xz), [included](assets/vendor/licenses/sources/coreutils-8.32.tar.xz) |
| **GNU Awk** (`gawk`, also as `awk`) | 5.1.0 | **GNU GPL 3 or later** | [gawk/5.1.0](assets/vendor/biowasm/gawk/5.1.0/) | [release source](https://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz), [included](assets/vendor/licenses/sources/gawk-5.1.0.tar.xz) |
| **GNU grep** | 3.7 | **GNU GPL 3 or later** | [grep/3.7](assets/vendor/biowasm/grep/3.7/) | [release source](https://ftp.gnu.org/gnu/grep/grep-3.7.tar.xz), [included](assets/vendor/licenses/sources/grep-3.7.tar.xz) |
| **GNU grep with PCRE2** (`grep-perl`), for `grep -P` | grep 3.11, PCRE2 10.42 | grep: **GNU GPL 3 or later**; PCRE2: 3-clause BSD with the PCRE2 exemption (`PCRE2-LICENCE`) | [grep/3.11](assets/vendor/biowasm/grep/3.11/) | [grep release source](https://ftp.gnu.org/gnu/grep/grep-3.11.tar.xz), [PCRE2 release source](https://github.com/PCRE2Project/pcre2/releases/tag/pcre2-10.42); [grep](assets/vendor/licenses/sources/grep-3.11.tar.xz) and [PCRE2](assets/vendor/licenses/sources/pcre2-10.42.tar.bz2) included |
| **GNU sed** | 4.8 | **GNU GPL 3 or later** | [sed/4.8](assets/vendor/biowasm/sed/4.8/) | [release source](https://ftp.gnu.org/gnu/sed/sed-4.8.tar.xz), [included](assets/vendor/licenses/sources/sed-4.8.tar.xz) |
| **GNU diffutils**: `diff`, `cmp` | 3.10 | **GNU GPL 3 or later** | [diffutils/3.10](assets/vendor/biowasm/diffutils/3.10/) | [release source](https://ftp.gnu.org/gnu/diffutils/diffutils-3.10.tar.xz); [source](assets/vendor/licenses/sources/diffutils-3.10.tar.xz), patch and build script [included](assets/vendor/licenses/diffutils-build/) |
| Biowasm base module and the Aioli runner (`aioli.js`, which includes Comlink and the SIMD check of wasm-feature-detect) | base 1.0.0; Aioli 3.2.3 | MIT. Comlink and wasm-feature-detect: Apache 2.0 (Copyright 2019 Google) | [notice and MIT licence](assets/vendor/biowasm/LICENSE.txt); [Apache 2.0](assets/vendor/licenses/Apache-2.0.txt) | [biowasm](https://github.com/biowasm/biowasm), [aioli](https://github.com/biowasm/aioli), [comlink](https://github.com/GoogleChromeLabs/comlink), [wasm-feature-detect](https://github.com/GoogleChromeLabs/wasm-feature-detect) |

Every `.wasm` file also contains parts of the Emscripten runtime and of its C library, musl (MIT), and, where a program needs them, LLVM's compiler support functions, compiler-rt (Apache 2.0 with LLVM exceptions); the JavaScript loaders were written by Emscripten (MIT or University of Illinois/NCSA). The licence texts are in [assets/vendor/licenses/runtime-libraries/](assets/vendor/licenses/runtime-libraries/). All these programs are written in C: none contains a C++ library, zlib, bzip2 or liblzma.

**Where the builds came from.** GNU coreutils, gawk, grep 3.7 and sed, the base module and the runner come from the [Biowasm](https://biowasm.com) project: the programs and the base module were downloaded from `https://biowasm.com/cdn/v3/` between 30 September and 2 October 2026 (each `NOTICE.txt` has the dates), and `aioli.js` is Aioli 3.2.3 as that CDN serves it. `diff` and `cmp` (GNU diffutils 3.10) and `grep-perl` (GNU grep 3.11 with PCRE2 10.42) were compiled with Emscripten 6.0.10 for the course – `diff` from its release source unchanged, `cmp` with a one-line patch, grep and PCRE2 from theirs unchanged, with one added function that Emscripten's C library lacks (`splice`); they are not Biowasm builds. The programs, the runner and their local changes are the same as in the Bioinformatics workbench, from which this site was made. On 15 October 2026, `base.js`, `base.wasm`, `gawk.wasm` and `sed.wasm` were still identical to the files on the Biowasm CDN, and `aioli.js` differed from the CDN's only by the local changes below. How diff, cmp and grep-perl were built is in [assets/vendor/licenses/diffutils-build/](assets/vendor/licenses/diffutils-build/) and [assets/vendor/licenses/grep-perl-build/](assets/vendor/licenses/grep-perl-build/).

**Local changes** – all listed in [assets/vendor/biowasm/RUNTIME-PATCHES.txt](assets/vendor/biowasm/RUNTIME-PATCHES.txt):

- The JavaScript loaders of the programs record each program's exit status. The Aioli runner has two added methods: `execIO` runs a program with real standard input, output and error – and starts every program afresh for each run, as a process is on Linux –, and `statTree` lists the shared file system in one answer; [execio-source.txt](assets/vendor/biowasm/execio-source.txt) is their readable source. The runner also keeps its worker where the page can end it (Ctrl+C twice).
- In each of the 17 **coreutils** programs and in **grep** 3.7, **one byte** of the `.wasm` file is changed, which makes the C library's standard output unbuffered. Unchanged, these builds lose output that does not end with a newline (`tr`, `head -c`, `fold` …; `grep -lZ`, `grep -z`). The byte, the reason and the checksums of the files as downloaded are in the [coreutils notice](assets/vendor/biowasm/coreutils/8.32/NOTICE.txt) and the [grep notice](assets/vendor/biowasm/grep/3.7/NOTICE.txt); the script that makes the change is [unbuffer-stdout.py](assets/vendor/licenses/local-patches/unbuffer-stdout.py).
- In the loaders of **date** and **gawk** the day of the year is counted in calendar days ([fix-day-of-year.py](assets/vendor/licenses/local-patches/fix-day-of-year.py)): as downloaded, `date -d 2024-07-15` printed “invalid date” in zones with summer time.
- `base.js`, `base.wasm`, `gawk.wasm` and `sed.wasm` are unmodified.

**Source code of the GPL programs.** [assets/vendor/licenses/](assets/vendor/licenses/) – see its [README.txt](assets/vendor/licenses/README.txt) – holds:

- the full text of the GPL version 3 ([GPL-3.0.txt](assets/vendor/licenses/GPL-3.0.txt)) and of the Apache License 2.0 ([Apache-2.0.txt](assets/vendor/licenses/Apache-2.0.txt), for Comlink and wasm-feature-detect);
- the release sources of the five GNU packages (coreutils 8.32, diffutils 3.10, gawk 5.1.0, grep 3.7 and 3.11, sed 4.8) and of PCRE2 10.42, in [sources/](assets/vendor/licenses/sources/), with their origins, sizes and SHA-256 values, and how each was checked against the upstream release (OpenPGP signature; published checksum where the release announcement gives one), in [source-archives.json](assets/vendor/licenses/source-archives.json);
- for `diff` and `cmp`, and for the grep that carries out `grep -P`: the build scripts, patch and instructions;
- for the Biowasm builds: the recipes (scripts and patches) of the four programs used here, from one pinned commit of the Biowasm repository ([`97bb232`](https://github.com/biowasm/biowasm/tree/97bb23225892ba5cc59ba0deac8b212b957db66a)), in [biowasm-build/](assets/vendor/licenses/biowasm-build/), listed with checksums and their paths in that repository in [biowasm-build-manifest.json](assets/vendor/licenses/biowasm-build-manifest.json). The commit and toolchain of the original CDN builds are not known, so this is a pinned recipe for inspection and rebuilding, **not** a claim that rebuilding gives identical binaries;
- the licence texts of the libraries inside the programs (Emscripten's runtime, musl, LLVM's compiler-rt) in [runtime-libraries/](assets/vendor/licenses/runtime-libraries/);
- the scripts of the local changes to downloaded files in [local-patches/](assets/vendor/licenses/local-patches/).

The GPL's terms for distributing compiled programs and their Corresponding Source are in its section 6. Whoever hosts this site should keep `assets/vendor/licenses/`, the `NOTICE.txt` files and this file with it. Copyright statements of the programs and of the code they include remain in their source releases; a licence label in the table above does not replace the notices in individual source files.

## JavaScript libraries (bundled)

| Library | Version | Licence | Files |
| --- | --- | --- | --- |
| CodeMirror 5 (the editors: the R, Markdown, YAML, YAML front-matter, shell, JavaScript and Python modes; the add-ons for brackets, comments, the active line, search, overlay and multiplexed modes, and runmode – unchanged) | 5.65.18 | MIT | [assets/vendor/codemirror/LICENSE](assets/vendor/codemirror/LICENSE) |
| – `rmarkdown.js`, the mode for R Markdown and Quarto documents: not part of CodeMirror, written for the R workbench from CodeMirror's modes and its multiplex and YAML front-matter add-ons | – | MIT, as CodeMirror (its header) | [assets/vendor/codemirror/rmarkdown.js](assets/vendor/codemirror/rmarkdown.js) |
| marked (Markdown in notebook text cells and in the AI assistant's answers; `lib/marked.umd.js` of the npm package, unchanged, saved as `marked.min.js`) | 18.0.13 | MIT (its licence file also holds the BSD notice of the original Markdown) | [assets/vendor/marked/LICENSE](assets/vendor/marked/LICENSE) |
| DOMPurify (cleans HTML before display: AI answers, notebook output, R help pages) | 3.4.16 | Apache 2.0 or MPL 2.0 | [assets/vendor/dompurify/LICENSE](assets/vendor/dompurify/LICENSE) |
| JSZip (unpacking and saving .zip files; reading .xlsx files for previews; includes pako 1.0) | 3.10.1 | MIT or GPL v3; pako: MIT ([LICENSE-pako.txt](assets/vendor/jszip/LICENSE-pako.txt); also at the end of this file) | [assets/vendor/jszip/LICENSE.markdown](assets/vendor/jszip/LICENSE.markdown) |
| PDF.js (PDF files in the Files tab; the legacy build of the npm package pdfjs-dist, unchanged) | 6.3.289 | Apache 2.0 | [assets/vendor/pdfjs/LICENSE](assets/vendor/pdfjs/LICENSE), [README.txt](assets/vendor/pdfjs/README.txt) |
| – with it: the Foxit standard fonts (BSD), Adobe's CMaps (BSD), OpenJPEG (BSD 2-clause), PDFium's JBIG2 decoder (BSD 3-clause), qcms (MIT) – the last three as built for PDF.js by Mozilla (BSD 2-clause, Apache 2.0, MIT) –, a CMYK profile (CC0); the Liberation Sans fonts of the package are left out (GPL 2 with a font exception) | | as listed | [standard_fonts/LICENSE_FOXIT](assets/vendor/pdfjs/standard_fonts/LICENSE_FOXIT), [cmaps/LICENSE](assets/vendor/pdfjs/cmaps/LICENSE), [wasm/](assets/vendor/pdfjs/wasm/), [iccs/LICENSE](assets/vendor/pdfjs/iccs/LICENSE) |

Apart from webR and R packages (below), the page loads no code, fonts or style sheets from other sites: its fonts are those of the student's computer.

## Code adapted from another project

| Files | Adapted from | Licence |
| --- | --- | --- |
| [isolation-sw.js](isolation-sw.js) (its Shiny part), [assets/js/shiny.js](assets/js/shiny.js), [assets/js/shiny-socket.js](assets/js/shiny-socket.js), and the R functions `wb$shiny_*` in [assets/js/rsession.js](assets/js/rsession.js) – how Shiny apps run in the page | [Shinylive](https://github.com/posit-dev/shinylive) (Posit): `shinylive-sw.ts`, `messageporthttp.ts`, `messageportwebsocket.ts`, `messageportwebsocket-channel.ts`, `shinylive-inject-socket.ts` and the R code in `hooks/useWebR.tsx` | MIT – [notice](assets/vendor/licenses/shinylive-MIT.txt) |

These files were written again for the workbench, not copied; but they follow Shinylive's design closely – the messages between the page, the service worker and the app's frame, the stand-in for the app's WebSocket, the calls into Shiny with which R answers the app – and some parts are near to Shinylive's code. Shinylive's MIT notice is therefore kept with the site, in [assets/vendor/licenses/shinylive-MIT.txt](assets/vendor/licenses/shinylive-MIT.txt), which lists the files in detail. The rest of the site's code is the workbench's own: written for it, or taken from the Bioinformatics workbench, by the same authors – the terminal (`assets/js/shell*.js`, `terminal.js`, `tools-wasm.js`) among it.

## Imitations written for the workbench

These files contain and load none of the programs they imitate; their names, menus and messages follow the real programs, so that what students learn transfers.

| File | Imitates | Licence of the real program |
| --- | --- | --- |
| `assets/js/rstudio.js`, `rsource.js` (the RStudio tab) | the [RStudio](https://posit.co/products/open-source/rstudio/) IDE: its panes, menus, dialogs and messages. It is not RStudio, and is not made or endorsed by Posit (as its About box says) | RStudio (open-source edition): GNU AGPL 3 |
| `assets/js/knit.js` | knitting R Markdown documents and rendering Quarto documents to HTML. It runs the real knitr and markdown packages (below); the pages are styled like those of R Markdown's `html_document` (Bootstrap 3) and of Quarto, by short style sheets of its own that take some of their sizes and colours | rmarkdown: GNU GPL 3; Quarto: MIT |
| `assets/js/notebook.js`, `kernels.js` (the Notebook tab) | Jupyter notebooks (`.ipynb` files) with an R kernel | Jupyter Notebook: BSD 3-clause |

## Loaded at run time, not bundled

- **webR 0.6.0** – R 4.6.0 compiled to WebAssembly – is downloaded by the student's browser from `https://webr.r-wasm.org/v0.6.0/` when the first R starts (on a first visit, as the page opens: the R console tab comes first), and afterwards taken from the browser's cache; every R of the page – the R console, RStudio, the notebook, `Rscript` and `R` in the terminal, knitting – is one of these. The site does not distribute it. As [webR's licence notes](https://github.com/r-wasm/webr/blob/v0.6.0/LICENSE.md) state, R is under the GNU GPL versions 2 and 3, the webR binaries (with the libraries compiled into them, listed there) are distributed under the GNU GPL version 3, and webR's other software (its setup and build scripts, the webR REPL …) under the MIT licence unless its files say otherwise.
- **The R packages of webR's image**: R's base packages – base, compiler, datasets, graphics, grDevices, grid, methods, parallel, splines, stats, stats4, tcltk, tools, utils, with the translations of R's messages (part of R: GNU GPL 2 or 3) – and webR's support package webr (MIT). R's recommended packages (MASS, Matrix, lattice …) are not in it (webR 0.6.0 builds R without them); like other packages, they come from the webR repository when installed.
- **Other R packages** are downloaded by the student's browser from the webR repository, `https://repo.r-wasm.org` (CRAN packages built for webR), when the student installs them with `install.packages()` – and when a feature of the page needs them and the student agrees to install them: knitr and markdown to knit a document, shiny to run a Shiny app, readxl and readr for Import Dataset, each with the packages it depends on. The site does not distribute them. Each has its own licence, which `packageDescription("NAME")$License` shows in R; on 15 October 2026 the repository's builds for R 4.6 gave knitr GPL, markdown MIT, shiny MIT (1.13.0.8000), httpuv GPL (≥ 2), jsonlite MIT, readr MIT and readxl MIT.
- The **AI assistant** sends a student's messages – and the agent its commands and their output – to the AI service the student chose (Google's Gemini API, Anthropic's API, or an OpenAI-compatible service), with the student's own key. No AI model or service is part of the site.

## Data

| Data (`data/`) | Source | Terms |
| --- | --- | --- |
| `penguins.csv` | 344 penguins of three species from three islands of the Palmer Archipelago, Antarctica (2007–2009): R's `datasets::penguins` (R 4.5 and later), written with `write.csv()` in R 4.6.0. The data come from the palmerpenguins package (Horst, Hill & Gorman 2020) and were collected by Dr Kristen Gorman and the Palmer Station Long Term Ecological Research (LTER) Program (Gorman, Williams & Fraser 2014, *PLoS ONE* 9(3): e90081, doi:10.1371/journal.pone.0090081) | CC0 1.0 (public domain) |
| `penguins.xlsx` | the same data as an Excel workbook, with a sheet that describes the columns; made from `penguins.csv` with Python's openpyxl | CC0 1.0 |

Both files are copied into each user's `~/data` folder on the first visit. Details: [data/PROVENANCE.md](data/PROVENANCE.md).

## Licence notice of pako

JSZip ([assets/vendor/jszip/jszip.min.js](assets/vendor/jszip/jszip.min.js)) includes pako 1.0, whose notice is not in that file; it is kept beside it, in [LICENSE-pako.txt](assets/vendor/jszip/LICENSE-pako.txt), and here:

```
(The MIT License)

Copyright (C) 2014-2017 by Vitaly Puzrin and Andrei Tuputcyn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
