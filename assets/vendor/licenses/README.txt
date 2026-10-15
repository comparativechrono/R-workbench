Licences, sources and build recipes of the bundled programs
===========================================================
This folder belongs to the WebAssembly programs of the terminal, in ../biowasm/. Keep it with the
site: those programs are under the GNU General Public License, which asks whoever distributes
the programs to offer their source code and build scripts in the same place.

GPL-3.0.txt                    the GNU General Public License, version 3
Apache-2.0.txt                 the Apache License, version 2.0 – for Comlink and for the SIMD check
                                 of wasm-feature-detect, which are part of ../biowasm/aioli.js (see
                                 ../biowasm/LICENSE.txt)
sources/                       the source code of the programs, as released: GNU coreutils 8.32,
                                 diffutils 3.10, gawk 5.1.0, grep 3.7, grep 3.11 and sed 4.8
                                 (.tar.xz), and PCRE2 10.42 (.tar.bz2; BSD licence), which is part
                                 of the grep that carries out "grep -P"
source-archives.json           where each archive came from, its size and SHA-256, and how it was
                                 checked against the upstream release (signature; published
                                 checksum where there is one)
biowasm-build/                 the Biowasm recipes of coreutils, gawk, grep 3.7 and sed (their build
                                 scripts and gawk's patch), with the build scripts and settings of
                                 the Biowasm repository – from one pinned commit of
                                 https://github.com/biowasm/biowasm (97bb232). The commit and
                                 toolchain with which the files on the Biowasm CDN were built are
                                 not recorded: this is a pinned recipe for inspection and
                                 rebuilding, not a claim that rebuilding gives identical programs
biowasm-build-manifest.json    the list of those files, with their paths in the Biowasm repository,
                                 addresses and SHA-256, and the commits of the GNU sources that the
                                 recipes check out
diffutils-build/               how diff and cmp (GNU diffutils) were compiled for the course:
                                 patch, build script, instructions
grep-perl-build/               how GNU grep 3.11 with PCRE2 10.42 ("grep -P") was compiled for the
                                 course: build script, one added function, instructions
runtime-libraries/             the licences of the libraries that are part of every program
                                 (Emscripten's runtime, the C library musl, LLVM's compiler-rt) – see
                                 its README.txt, which also says which texts there apply to none of
                                 the programs of this site
local-patches/                 unbuffer-stdout.py – the one-byte change made to the 17 coreutils
                                 programs and to grep 3.7 (see the NOTICE.txt in
                                 ../biowasm/coreutils/8.32/ and ../biowasm/grep/3.7/)
                               fix-day-of-year.py – the day of the year in the loaders of date and
                                 gawk (see ../biowasm/RUNTIME-PATCHES.txt, section 2)
shinylive-MIT.txt              the MIT licence notice of Shinylive (Posit), whose way of running
                                 Shiny apps in a web page the site's Shiny code follows (the site's
                                 isolation-sw.js, and assets/js/shiny.js, shiny-socket.js and the
                                 Shiny part of rsession.js) – the file lists what follows what
SHA256SUMS                     checksums of everything in this folder

Next to each program in ../biowasm/NAME/VERSION/ are its licence, a NOTICE.txt (origin, local
changes, where its source is) and SHA256SUMS (the base module has a notice and checksums only;
its licence is ../biowasm/LICENSE.txt). ../biowasm/RUNTIME-PATCHES.txt lists the changes to the
runner and the programs. The table of all third-party parts of the site is THIRD_PARTY.md at the
top of the site.
