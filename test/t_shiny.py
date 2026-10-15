"""Shiny in RStudio: Run App shows the app in the Viewer, the inputs work (the app's websocket goes through the page),
the console is busy until Stop. Needs the service worker (isolation-sw.js): the page is opened with it allowed."""
import time
from h import Page, Server, check, done

srv = Server()
p = Page(service_workers='allow', base=srv.base)
p.open('index.html')
# (the first visit installs the service worker; it takes control of the page)
p.wait('() => navigator.serviceWorker && navigator.serviceWorker.controller', timeout=30000)
print('service worker in control; isolated:', p.js('() => window.crossOriginIsolated'))
p.js('() => MG.app.showWorkbench("rstudio")')
p.wait('() => MG.app.rstudio && MG.app.rstudio.S && MG.app.rstudio.S.idle', timeout=120000)

def idle(timeout=120000):
    time.sleep(0.4)
    p.wait('() => MG.app.rstudio.S.idle', timeout=timeout)

# a new Shiny app (File > New File > Shiny Web App): ~/myapp/app.R
p.js('() => { MG.app.rstudio.newShinyDialog(); }')
p.wait('() => document.querySelector(".prompt-form input")')
p.js('() => { const i = document.querySelector(".prompt-form input"); i.value = "penguinapp"; document.querySelector(".prompt-form .btn.primary").click(); }')
p.wait('() => MG.app.rstudio.cur && MG.app.rstudio.cur.path === "/home/user/penguinapp/app.R"')
check(p.js('() => !!document.querySelector(".rs-docbar") && document.querySelector(".rs-docbar").textContent.includes("Run App")'), 'an app.R has Run App in its toolbar')
p.js('() => { MG.app.rstudio.runApp(); }')
# (shiny is not installed yet: the dialog asks)
p.wait('() => Array.from(document.querySelectorAll(".modal .btn.primary")).some((b) => b.textContent.trim() === "Install")', timeout=30000)
p.js('() => Array.from(document.querySelectorAll(".modal .btn.primary")).find((b) => b.textContent.trim() === "Install").click()')
t0 = time.time()
p.wait('() => MG.app.rstudio.shinyApp', timeout=300000)
print(f'app started in {time.time() - t0:.1f}s')
check('Listening on http://127.0.0.1:' in p.js('() => MG.app.rstudio.cv.text()'), 'the console says where the app listens')
check(p.js('() => MG.app.rstudio.cv.held === true'), 'the console is busy while the app runs')
# the app in the Viewer's frame
fr = None
for _ in range(120):
    for f in p.p.frames:
        if '/app_' in f.url:
            fr = f
    if fr:
        break
    # (Playwright learns of new frames while it waits – not in time.sleep)
    p.p.wait_for_timeout(500)
if not check(fr is not None, 'the Viewer shows the app: ' + (fr.url if fr else '')):
    print('iframe:', p.js('() => { const f = MG.app.rstudio.viewerBox.querySelector("iframe"); return f && f.src; }'), [f.url for f in p.p.frames])
    print(p.js('() => MG.app.rstudio.cv.text().slice(-800)'))
    print(p.logs[-20:], p.errors[:5])
    p.shot('shiny-fail')
fr.wait_for_selector('#hist img', timeout=60000)
check(True, 'the app drew its histogram (renderPlot)')
src1 = fr.eval_on_selector('#hist img', 'e => e.src')
check(src1.startswith('data:image/png'), 'the plot is a picture')
title = fr.eval_on_selector('h2', 'e => e.textContent')
check('Penguin body mass' in title, 'the app\'s title: ' + title)
# move the slider: the plot is drawn again (the websocket works both ways)
fr.evaluate('() => { const el = $("#bins").data("ionRangeSlider"); el.update({ from: 40 }); }')
for _ in range(60):
    p.p.wait_for_timeout(500)
    if fr.eval_on_selector('#hist img', 'e => e.src') != src1:
        break
check(fr.eval_on_selector('#hist img', 'e => e.src') != src1, 'changing an input redraws the plot')
p.shot('shiny-01-viewer')
# Stop
p.js('() => MG.app.rstudio.interrupt()')
p.wait('() => !MG.app.rstudio.shinyApp', timeout=30000)
check(p.js('() => !MG.app.rstudio.cv.held'), 'after Stop the console is free again')
p.js('() => MG.app.rstudio.consoleRun("1 + 1")')
idle()
check('[1] 2' in p.js('() => MG.app.rstudio.cv.text()'), 'R runs commands again')

errs = [e for e in p.errors if "'serviceWorker' property" not in e]
print('errors:', errs[:5])
check(not errs, 'no errors in the page')
p.close()
srv.stop()
done()
