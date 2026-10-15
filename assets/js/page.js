/* =====================================================================
   The R workbench's set-up: the file system (your files, kept in the
   browser; the starter files on the first visit), the tabs – each built
   the first time it is shown –, opening files in the right place, and
   what the buttons of the instructions do (MG.actions) and what the tasks
   look for (MG.checks).
   ===================================================================== */
(function () {
  'use strict';
  const MG = window.MG;
  const { h, esc, bus, toast, store } = MG;
  const CFG = MG.config;
  MG.app = MG.app || {};
  MG.page = MG.page || {};
  MG.actions = MG.actions || {};
  MG.checks = MG.checks || {};

  const HOME = '/home/user';
  MG.app.HOME = HOME;
  const abs = (u) => new URL(u, location.href).href;
  /* the files a new user finds in ~/data: the site's data/ folder (the list is written into the page by build/make_page.py) */
  const STARTERS = window.RWB_STARTERS || [];

  async function setupFs() {
    const fs = new MG.VFS(HOME);
    fs.mkdirp('/tmp');
    await MG.project.restore(fs, [HOME]);
    fs.cwd = HOME;
    // the first visit: the data and examples of the practicals (a file that is there already is left alone)
    const seeded = store.get('seeded', 0);
    const version = Number(window.RWB_STARTERS_VERSION || 1);
    if (seeded < version) {
      for (const s of STARTERS) {
        const path = HOME + '/data/' + s.p;
        if (fs.exists(path)) continue;
        try {
          const r = await fetch(abs('data/' + s.p));
          if (!r.ok) continue;
          const bytes = new Uint8Array(await r.arrayBuffer());
          const text = MG.looksText(s.p, bytes);
          fs.mkdirp(MG.path.dirname(path));
          if (text != null) fs.put(path, { kind: 'text', text, mtime: Date.parse('2026-10-14T09:00:00Z') });
          else fs.put(path, { kind: 'blob', blob: new Blob([bytes]), mtime: Date.parse('2026-10-14T09:00:00Z') });
        } catch (e) {
          /* offline: no starter */
        }
      }
      store.set('seeded', version);
    }
    MG.project.watch(fs);
    return fs;
  }

  MG.page.firstBench = 'console';
  MG.page.init = async function () {
    MG.app.fs = await setupFs();
    MG.project.persist();
  };

  /* ------------------------------------------------------------------
     the tabs, built when first shown
     ------------------------------------------------------------------ */
  MG.page.lazy = {
    console: (pane) => {
      MG.app.rcon = new MG.RConsoleApp(pane.querySelector('#rconRoot'));
    },
    rstudio: (pane) => {
      MG.app.rstudio = new MG.RStudioApp(pane.querySelector('#rsRoot'), { fs: MG.app.fs });
    },
    notebook: async (pane) => {
      MG.app.nbApp = new MG.NotebookApp(pane.querySelector('#nbRoot'), { fs: MG.app.fs, dir: HOME + '/notebooks' });
      const last = store.get('nbOpen', null);
      const start = (last && MG.app.fs.exists(last) && last) || (MG.app.nbApp.list()[0] || {}).path;
      if (start) await MG.app.nbApp.open(start);
      else await MG.app.nbApp.newNotebook('r');
    },
    terminal: (pane) => {
      MG.app.term = new MG.TerminalUI(pane.querySelector('#termRoot'), {
        fs: MG.app.fs,
        hostname: CFG.hostname || 'workbench',
        env: {},
        welcome:
          `A Linux terminal (bash), in your browser. R is here as it is on a computer: Rscript script.R runs a script, R CMD BATCH script.R keeps a record of a run, R starts R's console. Your files: ~ (${HOME}). Type  help  for the commands.` +
          (MG.user.name() === MG.user.DEFAULT ? ' To see your name in place of user, click “user” at the top of the page.' : '')
      });
    },
    editor: (pane) => {
      MG.app.editor = new MG.Editor(pane.querySelector('#edRoot'), { fs: MG.app.fs });
    },
    assistant: (pane) => {
      MG.app.ai = new MG.Assistant(pane.querySelector('#aiRoot'), {});
    }
  };
  /* each time a tab is shown */
  MG.page.shown = {
    console: (pane, opts) => MG.app.rcon && MG.app.rcon.shown(opts),
    rstudio: (pane, opts) => MG.app.rstudio && MG.app.rstudio.shown(opts),
    notebook: () => MG.app.nbApp && MG.app.nbApp.shown(),
    terminal: (pane, opts) => {
      if (MG.app.term && !(opts && opts.resize) && !window.matchMedia('(max-width: 900px)').matches) MG.app.term.focus();
    },
    editor: () => MG.app.editor && MG.app.editor.shown && MG.app.editor.shown(),
    assistant: () => MG.app.ai && MG.app.ai.shown && MG.app.ai.shown()
  };

  async function waitFor(get, ms = 6000) {
    for (let t = 0; t < ms && !get(); t += 50) await new Promise((r) => setTimeout(r, 50));
    return get();
  }
  MG.app.waitFor = waitFor;

  /* ------------------------------------------------------------------
     opening files
     ------------------------------------------------------------------ */
  /** edit or look at a file in the Files tab */
  MG.app.editFile = async (path, opts = {}) => {
    await MG.app.showWorkbench('editor');
    const ed = await waitFor(() => MG.app.editor);
    if (ed) await ed.openFile(path, opts);
  };
  /** open a file where it belongs: a notebook in the Notebook tab, the rest in Files */
  MG.app.openFile = async (path, opts = {}) => {
    const p = MG.app.fs.resolve(path);
    if (!opts.edit && /\.ipynb$/i.test(p)) {
      await MG.app.showWorkbench('notebook');
      const nb = await waitFor(() => MG.app.nbApp);
      return nb && nb.open(p);
    }
    return MG.app.editFile(p, opts);
  };
  /** open a file in RStudio's Source pane */
  MG.app.openInRStudio = async (path, opts = {}) => {
    await MG.app.showWorkbench('rstudio');
    const rs = await waitFor(() => MG.app.rstudio);
    if (rs) return rs.openFile(MG.app.fs.resolve(path), opts);
  };
  /** show a folder or file in the Files tab */
  MG.app.revealFile = async (path) => {
    await MG.app.showWorkbench('editor');
    const ed = await waitFor(() => MG.app.editor);
    if (ed && ed.reveal) ed.reveal(MG.app.fs.resolve(path));
  };
  /** what R's browseURL() asks to be shown: a web address in a new browser tab; a file of R's (an HTML report) in
      RStudio's Viewer when RStudio asked, else in a new browser tab */
  MG.app.browse = async (url, opts = {}) => {
    url = String(url || '');
    if (/^https?:\/\//i.test(url)) {
      window.open(url, '_blank', 'noopener');
      return;
    }
    const fs = MG.app.fs;
    const p = fs.resolve(url.replace(/^file:\/\//, ''));
    if (!fs.exists(p)) {
      toast(`There is no file ${esc(url)} to show.`, 'warn');
      return;
    }
    if (opts.from === 'rstudio' && MG.app.rstudio) return MG.app.rstudio.viewFile(p);
    const blob = await fs.toBlob(p);
    const type = /\.html?$/i.test(p) ? 'text/html' : /\.pdf$/i.test(p) ? 'application/pdf' : /\.svg$/i.test(p) ? 'image/svg+xml' : /\.png$/i.test(p) ? 'image/png' : 'text/plain';
    const u = URL.createObjectURL(new Blob([blob], { type }));
    const w = window.open(u, '_blank');
    if (!w) toast('The browser did not open a new tab (pop-ups are blocked?). The file is in the Files tab.', 'warn', 6000);
    setTimeout(() => URL.revokeObjectURL(u), 60000);
  };
  /* Files edited in the Files tab and in RStudio are saved with Save / Ctrl+S: before the page is left or reloaded
     with unsaved edits, the browser asks */
  window.addEventListener('beforeunload', (e) => {
    const dirty = (MG.app.editor && MG.app.editor.dirtyPaths ? MG.app.editor.dirtyPaths() : []).concat(MG.app.rstudio && MG.app.rstudio.dirtyPaths ? MG.app.rstudio.dirtyPaths() : []);
    if (dirty.length) {
      e.preventDefault();
      e.returnValue = '';
    }
  });

  /* ------------------------------------------------------------------
     buttons in the instructions
     data-rcon="code"        type code into the R console (not run)
     data-rcon-run="code"    run code in the R console
     data-rs-open="path"     open a file in RStudio
     data-rs-run="code"      run code in RStudio's console
     data-nb-open="path"     open a notebook
     data-edit="path"        open a file in Files
     data-file-create="path" make the file shown in the instructions (a .codefile)
     data-prompt="text"      put a prompt into the AI's box
     ------------------------------------------------------------------ */
  const inHome = (p) => (p.startsWith('/') ? p : p.startsWith('~/') ? HOME + p.slice(1) : HOME + '/' + p);
  const code = (s) => String(s).replace(/\\n/g, '\n');
  MG.actions.rcon = async (c) => {
    await MG.app.showWorkbench('console');
    const A = await waitFor(() => MG.app.rcon);
    if (A) A.type(code(c));
  };
  MG.actions.rconRun = async (c) => {
    await MG.app.showWorkbench('console');
    const A = await waitFor(() => MG.app.rcon);
    if (A) A.run(code(c));
  };
  MG.actions.rsOpen = async (p) => MG.app.openInRStudio(inHome(p));
  MG.actions.rsRun = async (c) => {
    await MG.app.showWorkbench('rstudio');
    const A = await waitFor(() => MG.app.rstudio);
    if (A) A.consoleRun(code(c));
  };
  MG.actions.nbOpen = async (p) => {
    await MG.app.showWorkbench('notebook');
    const nb = await waitFor(() => MG.app.nbApp);
    if (nb) await nb.open(inHome(p));
  };
  MG.actions.edit = async (p) => MG.app.editFile(inHome(p), { create: true });
  MG.actions.prompt = async (text) => {
    await MG.app.showWorkbench('assistant');
    const A = await waitFor(() => MG.app.ai);
    if (A && A.offerPrompt) A.offerPrompt(text);
  };
  const codeOf = (btn) => {
    const box = btn.closest('.codefile');
    return box ? box.querySelector('pre').textContent : '';
  };
  MG.actions.fileCreate = async (rel, btn) => {
    const fs = MG.app.fs;
    const path = inHome(rel);
    const text = codeOf(btn).replace(/\s+$/, '') + '\n';
    const e = fs.get(path);
    if (e && e.kind !== 'dir') {
      const old = await fs.readText(path);
      if (old !== text && !(await MG.confirmBox('Replace the file?', `<p><b>${esc(fs.pretty(path))}</b> is there already. Replace what is in it with the version in the instructions?</p>`, 'Replace it'))) return;
    }
    fs.mkdirp(MG.path.dirname(path));
    fs.writeText(path, text, e && e.mode ? { mode: e.mode } : {});
    bus.emit('file:create', { path, name: path.split('/').pop() });
    if (btn && btn.dataset.openIn === 'files') return MG.app.editFile(path, { line: 1 });
    return MG.app.openInRStudio(path);
  };
  MG.actions.copyCode = async (v, btn) => toast((await MG.copyText(codeOf(btn))) ? 'Copied.' : 'Could not copy – select the text and copy it.', null, 1800);

  /* ------------------------------------------------------------------
     what the tasks look at (data-check="name:arg")
     ------------------------------------------------------------------ */
  const textOf = (rel) => {
    const e = MG.app.fs && MG.app.fs.get(inHome(rel));
    return e && e.kind === 'text' ? e.text : null;
  };
  MG.checks.exists = (t, d, path) => !!MG.app.fs && MG.app.fs.exists(inHome(path));
  MG.checks.has = (t, d, arg) => {
    const cut = arg.indexOf('|');
    const txt = textOf(arg.slice(0, cut));
    return txt != null && new RegExp(arg.slice(cut + 1), 'm').test(txt);
  };
  MG.checks.installed = (t, d, pkg) => MG.R.userlib.list().includes(pkg);
  MG.checks.bench = (t, d, name) => MG.app.currentBench === name;

  /* the Help button at the top of the page */
  MG.page.help = function () {
    MG.modal(
      'How this page works',
      `<ul>
<li><b>Instructions</b> are on the left, the <b>workbench</b> on the right. Drag the divider to resize; the button at the top left (or <kbd>Ctrl</kbd>+<kbd>\\</kbd>) hides the instructions.</li>
<li><b>R console</b>: R on its own, as R’s own program shows it. <b>RStudio</b>: an IDE for R in the manner of RStudio – scripts, documents (R Markdown, Quarto), plots, help and files around them. <b>Notebook</b>: Jupyter-style notebooks in R. <b>Terminal</b>: bash, with <code>Rscript</code>, <code>R CMD BATCH</code> and <code>R</code> (type <code>help</code> for the list of programs). <b>Files</b>: your files and an editor. <b>AI</b>: an AI assistant to ask about R.</li>
<li>Each of them is an R of its own, as on a computer: an object made in one is not in another. They share your files (your home folder, <code>~</code>) and the packages you install. <kbd>Esc</kbd> stops what R is doing.</li>
<li>R runs in your browser, on this computer: R 4.6, compiled to WebAssembly (webR). It is downloaded the first time a tab needs it (about 30 MB); a package you install is downloaded once and is there for every R of the page.</li>
<li><b>show me</b> buttons type code for you – press <kbd>Enter</kbd> to run it. The steps of an activity tick themselves when you do them (<b>✓ spotted</b>); you can tick them yourself, too.</li>
<li><b>Saved in this browser:</b> your ticks and answers, your files and the packages you installed – they are still there after a reload. <b>My answers</b> downloads your answers; <b>My files</b> downloads all your files as a .zip file. Lab computers may clear the browser’s storage when you log out: download your work before you leave.</li>
<li><b>The AI assistant</b> needs a key of your own (Google Gemini has a free tier). The key stays in this browser tab and is sent only to the AI service you chose. What you send goes to that service – never type personal or patient data into it, or into any AI tool.</li>
<li>To start again: <b>My answers → Start again</b> clears your ticks and answers; <b>My files → Start afresh</b> deletes your files.</li>
</ul>`
    );
  };

  /* Start afresh: forget what the tabs remember */
  MG.page.beforeReset = async () => {
    for (const k of ['nbOpen', 'seeded', 'termHistory', 'rconHistory', 'rsOpen', 'rsHistory', 'rlib', 'bench']) store.remove(k);
  };
})();
