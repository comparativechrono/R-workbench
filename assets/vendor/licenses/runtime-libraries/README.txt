Libraries that are part of the WebAssembly programs
===================================================
A program that is compiled to WebAssembly carries the libraries it uses inside its .wasm file and
its JavaScript loader. Their licences ask that the notices go with the programs; here they are.
The programs of this site are those in ../../biowasm/: GNU coreutils (17 programs), gawk, grep
3.7, grep 3.11 with PCRE2 (grep-perl), sed, diff and cmp, and the base module. All are C programs.

EMSCRIPTEN-LICENSE.txt   Emscripten (the compiler's runtime and the JavaScript loaders): MIT, or
                         University of Illinois/NCSA – in every program
MUSL-COPYRIGHT.txt       musl, the C library: MIT – in every program
LLVM-LICENSE.txt         compiler-rt, LLVM's compiler support functions, which Emscripten links
                         into a program where it needs them: Apache License 2.0 with LLVM
                         exceptions (older parts: MIT, or University of Illinois/NCSA). (By the
                         LLVM exception, parts of compiler-rt that compiling puts into a program
                         need no notice; the text is here all the same.) LLVM's C++ libraries,
                         libc++ and libc++abi, are in none of the programs here.

Not used by any program of this site – these three texts came with this folder from the
Bioinformatics workbench, where programs built on zlib and HTSlib use them:
ZLIB-LICENSE.txt         zlib
BZIP2-LICENSE.txt        bzip2 (libbzip2)
XZ-COPYING.txt           XZ Utils (liblzma)
None of the .wasm files in ../../biowasm/ contains zlib, bzip2 or liblzma (checked on 15 October
2026 by searching them for the tables and messages of these libraries, which a program that
contains them has). The Biowasm build settings make Emscripten's zlib available to every
program they build (-s USE_ZLIB=1 in ../biowasm-build/bin/shared.sh), but GNU coreutils, gawk,
grep and sed do not use it, so it is not linked into them.

PCRE2, which is part of grep-perl, has its licence next to that program:
../../biowasm/grep/3.11/PCRE2-LICENCE.

The texts of Emscripten, musl and LLVM are those of Emscripten 6.0.10, with which diff, cmp and
grep-perl were compiled for the course. The Biowasm builds were made with earlier versions of
Emscripten, under the same licences.
