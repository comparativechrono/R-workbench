/* =====================================================================
   Settings for the R workbench.
   Edit and re-upload this file; nothing else needs to change.
   Never put an API key in this file: anyone could copy it from a public site.
   ===================================================================== */
window.MG_CONFIG = {
  courseTitle: 'R workbench',
  courseSubtitle: 'Four ways to use R – console, RStudio, notebooks and documents – in your browser',

  /* The prefix of what the page keeps in the browser (files, answers, settings). Change it only
     if two copies of the workbench on one web site must not share their saved work. */
  storePrefix: 'rwb',
  hostname: 'workbench',

  /* Model answers: shown with a "Show answer" button under each question. Set to false to hide
     them (they are still in the page's source); ?answers in the address shows them anyway. */
  showModelAnswers: true,

  /* R in the browser (webR). Every R of the page – the R console, RStudio, the notebook, Rscript in the
     terminal, knitting – downloads R from here (about 30 MB, kept by the browser after the first time).
     R packages come from the webR repository when install.packages() asks for them. */
  webrBase: 'https://webr.r-wasm.org/v0.6.0/',
  rRepos: ['https://repo.r-wasm.org'],

  /* The WebAssembly programs of the terminal (GNU coreutils, grep, sed, awk, diff). */
  biowasmBase: 'assets/vendor/biowasm',

  /* AI assistant. Each user enters their own API key in the assistant's settings; it is kept
     in the browser tab's memory (or, if the user ticks "Remember", in this tab's session
     storage, which is cleared when the tab closes) – never in this file or on the server.
     The service offered first ('gemini', 'anthropic' or 'openai') and the model of each.
     Models are retired from time to time: if the assistant reports that a model is not found,
     put a current one here (see ai.google.dev/gemini-api/docs/models). */
  liveProvider: 'gemini',
  geminiModel: 'gemini-3.8-flash',
  /* If that model is busy, over a limit or not found, the assistant asks these in turn. */
  geminiFallbackModels: ['gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite'],
  aiWaitSeconds: 60,
  anthropicModel: 'claude-sonnet-5-5',

  /* How much the workbench may keep in this browser before it warns (megabytes). */
  storageWarnMB: 1500
};
