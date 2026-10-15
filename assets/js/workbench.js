/* =====================================================================
   The frame of the R workbench: the tabs on the right (each built the
   first time it is shown), the instructions on the left (which can be
   hidden, and resized), full screen, the "My files" menu, the storage
   indicator, the button with the person's name, and the start: the page's
   own set-up (page.js: MG.page.init), then the instructions
   (tutorial.js: MG.tutorial.init).
   ===================================================================== */
(function () {
  'use strict';
  const MG = window.MG;
  const { h, esc, bus, toast, store, $, $$ } = MG;
  MG.app = MG.app || {};
  MG.page = MG.page || {};
  MG.actions = MG.actions || {};

  const narrow = () => window.matchMedia('(max-width: 1000px)').matches;
  let ready = false;

  const TAB_NAME = { console: 'R console', rstudio: 'RStudio', notebook: 'Notebook', terminal: 'Terminal', editor: 'Files', assistant: 'AI assistant' };
  MG.app.tabName = TAB_NAME;

  /* ------------------------------------------------------------------
     the tabs of the workbench
     ------------------------------------------------------------------ */
  function initTabs() {
    const tabs = $$('.wb-tab[data-wb]');
    const panes = $$('.wb-pane');
    const built = new Set();
    const building = new Map();
    /** show a tab; the first time, build it. → a promise that resolves when it is built.
        opts.noOpen: on a narrow screen, do not slide the workbench over the instructions */
    MG.app.showWorkbench = (name, opts = {}) => {
      const pane = panes.find((p) => p.dataset.wb === name);
      if (!pane) return Promise.resolve();
      if (narrow() && !opts.noOpen && ready) document.body.classList.add('bench-open');
      tabs.forEach((t) => {
        const on = t.dataset.wb === name;
        t.classList.toggle('on', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        if (on) t.classList.remove('attn');
      });
      panes.forEach((p) => (p.hidden = p !== pane));
      const prev = MG.app.currentBench;
      if (prev && prev !== name) MG.app.prevBench = prev;
      MG.app.currentBench = name;
      let p = Promise.resolve();
      if (!built.has(name) && MG.page.lazy && MG.page.lazy[name]) {
        built.add(name);
        p = Promise.resolve()
          .then(() => MG.page.lazy[name](pane))
          .catch((e) => {
            console.error(e);
            pane.firstElementChild.innerHTML = `<div class="wb-failed"><h3>${esc(TAB_NAME[name] || name)} could not start</h3><p>${esc(e.message || String(e))}</p><p>Reload the page to try again.</p></div>`;
          });
        building.set(name, p);
      } else if (building.has(name)) p = building.get(name);
      p.then(() => {
        if (MG.app.currentBench !== name) return;
        const hook = MG.page.shown && MG.page.shown[name];
        if (hook) setTimeout(() => hook(pane, opts), 20);
      });
      if (prev !== name) {
        store.set('bench', name);
        bus.emit('app:bench', { name });
      }
      return p;
    };
    MG.app.tabBuilt = (name) => built.has(name);
    tabs.forEach((t) => t.addEventListener('click', () => MG.app.showWorkbench(t.dataset.wb)));
    // arrow keys move along the tabs (as in other tab lists)
    const list = $('.wb-tabs');
    list.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      e.preventDefault();
      const t = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      t.focus();
      MG.app.showWorkbench(t.dataset.wb);
    });
    const fab = $('.bench-fab'), close = $('.bench-close');
    if (fab) fab.addEventListener('click', () => document.body.classList.add('bench-open'));
    if (close) close.addEventListener('click', () => document.body.classList.remove('bench-open'));
  }

  /* ------------------------------------------------------------------
     the instructions: hide and show them, resize them, full screen
     ------------------------------------------------------------------ */
  const tutOpen = () => !document.body.classList.contains('tut-off');
  function setTutOpen(open, opts = {}) {
    if (narrow()) {
      document.body.classList.toggle('bench-open', !open);
      return;
    }
    document.body.classList.toggle('tut-off', !open);
    if (!opts.noSave) store.set('tutOff', !open);
    const t = $('#tutToggle');
    if (t) {
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
      t.title = open ? 'Hide the instructions: the workbench fills the window (Ctrl+\\)' : 'Show the instructions (Ctrl+\\)';
      t.innerHTML = MG.icon(open ? 'sidebarClose' : 'sidebarOpen');
    }
    const rail = $('#tutRail');
    if (rail) rail.hidden = open;
    resized();
    bus.emit('app:tut', { open });
  }
  MG.app.toggleInstructions = (open) => setTutOpen(open == null ? !tutOpen() : !!open);

  /** after the workbench changed size: the tabs measure themselves again */
  const resized = MG.debounce(() => {
    window.dispatchEvent(new Event('resize'));
    const hook = MG.page.shown && MG.page.shown[MG.app.currentBench];
    if (hook) hook($(`.wb-pane[data-wb="${MG.app.currentBench}"]`), { resize: true });
  }, 60);
  MG.app.resized = resized;

  function initTutPane() {
    const t = $('#tutToggle');
    if (t) t.addEventListener('click', () => MG.app.toggleInstructions());
    const rail = $('#tutRail');
    if (rail) rail.addEventListener('click', () => setTutOpen(true));
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && !e.altKey && (e.key === '\\' || e.code === 'Backslash')) {
        e.preventDefault();
        MG.app.toggleInstructions();
      }
    });
    if (!narrow()) setTutOpen(!store.get('tutOff', false), { noSave: true });

    // full screen: the browser's full screen, with the instructions hidden (and shown again afterwards)
    const full = $('#fullBtn');
    if (!full) return;
    let before = null;
    const label = () => {
      const on = !!document.fullscreenElement;
      full.innerHTML = MG.icon(on ? 'shrink' : 'expand') + `<span>${on ? 'Exit full screen' : 'Full screen'}</span>`;
      full.title = on ? 'Leave full screen (Esc)' : 'Full screen: the workbench fills the whole screen';
    };
    if (!document.documentElement.requestFullscreen) full.hidden = true;
    full.addEventListener('click', async () => {
      try {
        if (document.fullscreenElement) await document.exitFullscreen();
        else {
          before = tutOpen();
          setTutOpen(false, { noSave: true });
          await document.documentElement.requestFullscreen();
        }
      } catch (e) {
        toast('This browser did not allow full screen here. Press F11 (or ⌃⌘F on a Mac) instead.', 'warn');
        if (before != null) setTutOpen(before, { noSave: true });
        before = null;
      }
    });
    document.addEventListener('fullscreenchange', () => {
      label();
      if (!document.fullscreenElement && before != null) {
        setTutOpen(before, { noSave: true });
        before = null;
      }
      resized();
    });
    label();
  }

  function initSplitter() {
    const sp = $('.splitter');
    const saved = store.get('tutWidth', null);
    if (saved) document.documentElement.style.setProperty('--tut-w', saved);
    if (!sp) return;
    let drag = false;
    sp.addEventListener('pointerdown', (e) => {
      drag = true;
      sp.classList.add('drag');
      sp.setPointerCapture(e.pointerId);
      document.body.classList.add('dragging');
    });
    sp.addEventListener('pointermove', (e) => {
      if (!drag) return;
      const w = MG.clamp((e.clientX / window.innerWidth) * 100, 18, 65);
      document.documentElement.style.setProperty('--tut-w', w.toFixed(1) + '%');
    });
    const end = () => {
      if (!drag) return;
      drag = false;
      sp.classList.remove('drag');
      document.body.classList.remove('dragging');
      store.set('tutWidth', getComputedStyle(document.documentElement).getPropertyValue('--tut-w').trim());
      resized();
    };
    sp.addEventListener('pointerup', end);
    sp.addEventListener('pointercancel', end);
    sp.addEventListener('dblclick', () => {
      document.documentElement.style.removeProperty('--tut-w');
      store.remove('tutWidth');
      resized();
    });
    sp.tabIndex = 0;
    sp.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      const cur = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--tut-w')) || 38;
      const w = MG.clamp(cur + (e.key === 'ArrowRight' ? 2 : -2), 18, 65);
      document.documentElement.style.setProperty('--tut-w', w + '%');
      store.set('tutWidth', w + '%');
      resized();
    });
  }

  /* ------------------------------------------------------------------
     "My files": download everything, add files, start afresh
     ------------------------------------------------------------------ */
  function initFilesMenu() {
    const btn = $('#projectBtn');
    if (!btn) return;
    const HOME = () => MG.app.HOME;
    btn.addEventListener('click', async () => {
      const u = await MG.project.usage();
      const used = u && u.usage ? `${MG.humanSize(u.usage)}B used of about ${MG.humanSize(u.quota)}B` : '';
      MG.popmenu(btn, [
        ['zip', 'Download all my files (.zip)', () => MG.project.download(HOME(), 'r-workbench-files.zip')],
        ['upload', 'Add files from my computer…', () => MG.app.pickFiles(HOME(), false)],
        ['folder', 'Add a folder from my computer…', () => MG.app.pickFiles(HOME(), true)],
        ['folder', 'Show my files', () => MG.app.showWorkbench('editor')],
        ['info', 'Where are my files kept?' + (used ? ' (' + used + ')' : ''), () => filesInfo()],
        ['trash', 'Start afresh: delete all my files…', () => startAfresh()]
      ]);
    });
  }
  function filesInfo() {
    MG.modal(
      'Where your files are kept',
      `<p>Your files – scripts, R Markdown documents, notebooks, data, what R writes – are kept <b>in this browser, on this computer</b> (the browser's storage for this site). They are there next time you open the workbench in the same browser on the same computer.</p>
       <ul><li>Another computer or browser does not have them: use <b>My files → Download all my files</b>, and <b>Add files</b> there.</li>
       <li>A private window, or a computer that clears the browser when you log out, forgets them: download your work before you leave.</li>
       <li>Nothing is sent to a server. The packages that you install with <code>install.packages()</code> are kept too (the browser keeps the downloads).</li></ul>`
    );
  }
  /** a file picker that puts what is chosen into a folder */
  MG.app.pickFiles = (folder, dir) =>
    new Promise((resolve) => {
      const inp = h('input', { type: 'file', multiple: true, style: { display: 'none' } });
      if (dir) inp.webkitdirectory = true;
      document.body.appendChild(inp);
      inp.addEventListener('change', async () => {
        const files = Array.from(inp.files || []);
        inp.remove();
        if (!files.length) return resolve([]);
        const paths = await MG.project.addFiles(MG.app.fs, folder, files);
        if (paths.length) toast(`Added <b>${paths.length}</b> file${paths.length === 1 ? '' : 's'} to ${esc(MG.app.fs.pretty(folder))}.`, 'ok');
        resolve(paths);
      });
      inp.click();
    });

  function startAfresh() {
    const m = MG.modal(
      'Start afresh?',
      `<p>This deletes <b>every file</b> in your home folder (${esc(MG.app.fs.pretty(MG.app.HOME))}) – scripts, documents, notebooks, data, results – from this browser, and forgets the packages you installed. It cannot be undone. (Your ticks and answers stay: <b>My answers → Start again</b> clears those.)</p>
       <p>Download your files first if you want to keep any of them.</p>
       <p><label class="check"><input type="checkbox" data-x="sure"> I have downloaded what I want to keep</label></p>
       <div class="prompt-actions"><button class="btn" data-x="dl" type="button">${MG.icon('zip')}<span>Download all my files</span></button><span class="grow"></span><button class="btn" data-x="no" type="button">Cancel</button><button class="btn danger" data-x="yes" type="button" disabled>Delete everything</button></div>`
    );
    const yes = m.box.querySelector('[data-x="yes"]');
    m.box.querySelector('[data-x="sure"]').addEventListener('change', (e) => (yes.disabled = !e.target.checked));
    m.box.querySelector('[data-x="dl"]').addEventListener('click', () => MG.project.download(MG.app.HOME, 'r-workbench-files.zip'));
    m.box.querySelector('[data-x="no"]').addEventListener('click', () => m.close());
    yes.addEventListener('click', async () => {
      m.close();
      try {
        if (MG.page.beforeReset) await MG.page.beforeReset();
      } catch (e) {
        console.error(e);
      }
      await MG.project.reset(MG.app.fs);
      const keep = new Set(['tutOff', 'tutWidth', 'ai:settings', 'userName', 'progress', 'chapter']);
      try {
        const pfx = (MG.config.storePrefix || 'rwb') + ':' + document.body.dataset.page + ':';
        Object.keys(localStorage)
          .filter((k) => k.startsWith(pfx) && !keep.has(k.slice(pfx.length)))
          .forEach((k) => localStorage.removeItem(k));
      } catch (e) {
        /* ignore */
      }
      location.reload();
    });
  }

  /* ------------------------------------------------------------------
     The button with the person's name, at the top: R's USER and the terminal's prompt show it in place of
     "user". The name is kept in this browser only.
     ------------------------------------------------------------------ */
  function initUser() {
    const btn = $('#userBtn');
    if (!btn) return;
    const label = btn.querySelector('.user-name');
    const show = () => {
      const n = MG.user.name(), plain = n === MG.user.DEFAULT;
      if (label) label.textContent = n;
      btn.title = plain ? 'Put your name into the workbench: the terminal and R show it in place of user' : `Your name in the workbench: ${n} – click to change it`;
      btn.setAttribute('aria-label', plain ? 'Your name in the workbench: user (click to put in yours)' : `Your name in the workbench: ${n}`);
    };
    show();
    bus.on('user:name', show);
    btn.addEventListener('click', nameDialog);
  }
  function nameDialog() {
    const D = MG.user.DEFAULT, cur = MG.user.name();
    const host = (MG.app.term && MG.app.term.hostname) || MG.config.hostname || 'workbench';
    const m = MG.modal('Your name in the workbench', '');
    const input = h('input.prompt-input#userNameIn', { type: 'text', value: cur === D ? '' : cur, placeholder: D, maxlength: '40', spellcheck: 'false', autocomplete: 'off', autocapitalize: 'off', 'aria-describedby': 'userNameNote' });
    const preview = h('code.user-prompt');
    const note = h('p.user-note#userNameNote', { 'aria-live': 'polite' });
    const save = h('button.btn.primary', { type: 'submit' }, 'Save');
    const reset = h('button.btn', { type: 'button' }, `Use “${D}”`);
    const cancel = h('button.btn', { type: 'button' }, 'Cancel');
    const form = h(
      'form.user-form',
      h('p', 'The terminal shows your name in its prompt, in place of ', h('code', D), '; ', h('code', 'whoami'), ', ', h('code', '$USER'), ', ', h('code', 'ls -l'), ' and R’s ', h('code', 'Sys.getenv("USER")'), ' use it too (an R that is already running keeps the name it started with). It is kept in this browser only. Your home folder stays ', h('code', MG.app.HOME || '/home/user'), '.'),
      h('label.user-label', { for: 'userNameIn' }, 'Your name'),
      input,
      h('p.user-prev', h('span.muted', 'The prompt: '), preview),
      note,
      h('div.prompt-actions', reset, h('span.grow'), cancel, save)
    );
    m.box.querySelector('.modal-b').appendChild(form);
    let chosen = cur;
    const update = () => {
      const v = input.value.trim();
      const n = v === '' ? D : v === 'root' ? '' : MG.user.valid(v) ? v : MG.user.suggest(v);
      note.classList.toggle('bad', !n);
      if (v === 'root') note.textContent = 'root is the name of the administrator here: choose another name.';
      else if (!n) note.textContent = 'A name here begins with a letter and has letters, digits, dots, hyphens or underscores – no spaces: ada, ada.lovelace or a_lovelace, for example.';
      else if (v && n !== v) note.textContent = `A name here has no spaces or other signs: it will be ${n}.`;
      else note.textContent = '';
      chosen = n;
      preview.textContent = `${n || '…'}@${host}:~$`;
      save.disabled = !n;
    };
    input.addEventListener('input', update);
    update();
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!chosen || !MG.user.set(chosen)) return;
      m.close();
      toast(chosen === D ? `The terminal shows <b>${D}</b> again.` : `Saved: the terminal shows <b>${esc(chosen)}</b>@${esc(host)}.`, 'ok', 3500);
    });
    reset.addEventListener('click', () => {
      input.value = '';
      update();
      input.focus();
    });
    cancel.addEventListener('click', () => m.close());
    setTimeout(() => {
      input.focus();
      input.select();
    }, 30);
  }
  MG.app.nameDialog = nameDialog;
  MG.actions.username = () => nameDialog();

  /* the indicator in the top bar: are the files kept? */
  function initStoreStatus() {
    const el = $('#storeStatus');
    if (!el) return;
    const set = (state, text, title) => {
      el.dataset.state = state;
      el.innerHTML = `<i></i><span>${esc(text)}</span>`;
      if (title) el.title = title;
    };
    if (!MG.project.ok) {
      set('off', 'Not kept', 'This browser does not let the workbench keep files (private window?). Download your work before you close the page.');
      return;
    }
    const OK_TITLE = 'Your files are kept in this browser on this computer. Use My files → Download to take them elsewhere.';
    let warned = false;
    const saved = () => {
      const limit = Number(MG.config.storageWarnMB) || 0;
      let bytes = 0;
      if (limit && MG.app.fs) for (const [p, e] of MG.app.fs.entries) if (e.kind !== 'dir' && p.startsWith(MG.app.HOME + '/')) bytes += MG.app.fs.size(e) || 0;
      if (!limit || bytes <= limit * 1048576) return set('ok', 'Saved in this browser', OK_TITLE);
      const much = MG.humanSize(bytes) + 'B';
      set('busy', `Saved · ${much}`, `Your files take ${much} in this browser. Download what you want to keep, and delete large files you no longer need.`);
      if (!warned) {
        warned = true;
        toast(`Your files take <b>${much}</b> in this browser – more than ${limit} MB. Download what you want to keep, and delete large files you no longer need: browsers limit how much a site may keep.`, 'warn', 12000);
      }
    };
    saved();
    let t;
    bus.on('files:saving', () => set('busy', 'Saving…'));
    bus.on('files:saved', () => {
      clearTimeout(t);
      t = setTimeout(saved, 250);
    });
    bus.on('files:notsaved', () => set('off', 'Not saved', 'The browser has no room left: download your files and delete some.'));
  }

  /* the title and subtitle of config.js */
  function initBrand() {
    const C = MG.config || {};
    if (C.courseTitle) {
      const t = $('.brand-title'), a = $('.brand');
      if (t) t.textContent = C.courseTitle;
      if (a) a.title = C.courseTitle;
      document.body.dataset.title = C.courseTitle;
    }
    if (C.courseSubtitle != null) {
      const s = $('.brand-sub');
      if (s) s.textContent = C.courseSubtitle;
    }
    if (C.courseTitle || C.courseSubtitle) document.title = [C.courseTitle, C.courseSubtitle].filter(Boolean).join(' – ');
  }

  /* the page in two tabs or windows of one browser: both would write the same files */
  function initTabsWarning() {
    if (!window.BroadcastChannel) return;
    let ch;
    try {
      ch = new BroadcastChannel((MG.config.storePrefix || 'rwb') + '-tabs');
    } catch (e) {
      return;
    }
    const me = Math.random().toString(36).slice(2);
    const others = new Set();
    let bar = null, closed = false;
    const show = () => {
      if (others.size && !bar && !closed) {
        bar = h('div.tabs-warning', { role: 'alert', html: '<b>The R workbench is open in another tab or window of this browser.</b> Work in one of them only: both keep files in the same place, and each can overwrite what the other saved.' });
        const b = h('button.btn.small', { type: 'button' }, 'Close this note');
        b.addEventListener('click', () => {
          closed = true;
          bar.remove();
          bar = null;
        });
        bar.appendChild(b);
        document.body.appendChild(bar);
      } else if (!others.size && bar) {
        bar.remove();
        bar = null;
      }
    };
    ch.onmessage = (ev) => {
      const m = ev.data || {};
      if (!m.id || m.id === me) return;
      if (m.t === 'hello') {
        others.add(m.id);
        ch.postMessage({ t: 'here', id: me });
      } else if (m.t === 'here') others.add(m.id);
      else if (m.t === 'bye') others.delete(m.id);
      show();
    };
    ch.postMessage({ t: 'hello', id: me });
    window.addEventListener('pagehide', () => ch.postMessage({ t: 'bye', id: me }));
    window.addEventListener('pageshow', (ev) => ev.persisted && ch.postMessage({ t: 'hello', id: me }));
  }

  /* ------------------------------------------------------------------
     start
     ------------------------------------------------------------------ */
  async function init() {
    initBrand();
    initTabs();
    initSplitter();
    initTutPane();
    initFilesMenu();
    initUser();
    try {
      if (MG.page.init) await MG.page.init();
    } catch (e) {
      console.error(e);
      toast('The workbench did not start properly: ' + esc(e.message || String(e)), 'error', 15000);
    }
    initStoreStatus();
    initTabsWarning();
    try {
      if (MG.tutorial && MG.tutorial.init) MG.tutorial.init();
    } catch (e) {
      console.error(e);
    }
    const want = new URLSearchParams(location.search).get('tab');
    const first = (want && TAB_NAME[want] && want) || MG.app.currentBench || store.get('bench', null) || MG.page.firstBench || 'console';
    if (!MG.app.currentBench || want) MG.app.showWorkbench(TAB_NAME[first] ? first : 'console', { noOpen: true });
    ready = true;
    document.body.classList.add('ready');
    window.MG_READY = true;
    bus.emit('app:ready', {});
  }
  MG.app.isReady = () => ready;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
