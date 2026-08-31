#!/usr/bin/env python
"""Headless-Chrome capture rig for the temple build.

Loads a page, runs an arbitrary JS setup expression, waits until a JS predicate
returns true, then screenshots. Screenshots come from a REAL compositing
browser, which is the whole point: NOTES.md records a session that shipped an
invisible win meter because every DOM value check passed in a pane that was
never painting.

  python tools/shot.py --url http://localhost:8660/vault-chibi/phase0.html \
      --until "window.__probe.state().anim==='jump-up'" \
      --then  "window.__probe.world().paused=true" \
      --out   scratchpad/midjump.png

Also supports --eval to print a JSON result instead of (or as well as) shooting.
"""
import argparse, base64, json, os, shutil, subprocess, sys, tempfile, time
import urllib.request, urllib.error

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    raise SystemExit("no chrome/edge binary found")


class CDP(object):
    """Minimal Chrome DevTools Protocol client over a websocket."""

    def __init__(self, ws_url):
        from websocket import create_connection  # type: ignore
        self.ws = create_connection(ws_url, timeout=30)
        self.n = 0

    def send(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError("%s: %s" % (method, msg["error"]))
                return msg.get("result", {})

    def evaluate(self, expr, await_promise=False):
        r = self.send("Runtime.evaluate", expression=expr, returnByValue=True,
                      awaitPromise=await_promise)
        res = r.get("result", {})
        if r.get("exceptionDetails"):
            raise RuntimeError(json.dumps(r["exceptionDetails"])[:600])
        return res.get("value")

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def http_json(url, tries=60):
    for _ in range(tries):
        try:
            return json.loads(urllib.request.urlopen(url, timeout=1).read().decode())
        except Exception:
            time.sleep(0.25)
    raise SystemExit("chrome devtools endpoint never came up: " + url)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out")
    ap.add_argument("--until", default="true", help="JS predicate; polled until true")
    ap.add_argument("--then", default="", help="JS run once --until passes, before the shot")
    ap.add_argument("--setup", default="", help="JS run right after load")
    ap.add_argument("--eval", dest="ev", default="", help="JS whose JSON result is printed")
    ap.add_argument("--evalfile", default="", help="file of JS whose JSON result is printed")
    ap.add_argument("--width", type=int, default=1180)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--settle", type=float, default=0.6, help="s to wait after load")
    ap.add_argument("--timeout", type=float, default=45.0)
    ap.add_argument("--port", type=int, default=9333)
    ap.add_argument("--selector", default="", help="clip the shot to this element")
    ap.add_argument("--keep", action="store_true", help="leave the browser running")
    a = ap.parse_args()

    profile = tempfile.mkdtemp(prefix="shotprof")
    chrome = find_chrome()
    proc = subprocess.Popen([
        chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--no-first-run", "--no-default-browser-check", "--mute-audio",
        "--force-device-scale-factor=%g" % a.scale,
        "--window-size=%d,%d" % (a.width, a.height),
        "--user-data-dir=" + profile,
        "--remote-debugging-port=%d" % a.port,
        "--remote-allow-origins=*",
        "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    code = 0
    cdp = None
    try:
        http_json("http://127.0.0.1:%d/json/version" % a.port)
        # modern Chrome requires PUT for /json/new, so attach to the tab the
        # browser already opened instead of asking for another one.
        tabs = http_json("http://127.0.0.1:%d/json/list" % a.port)
        pages = [t for t in tabs if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
        if not pages:
            raise SystemExit("no page target to attach to")
        cdp = CDP(pages[0]["webSocketDebuggerUrl"])
        cdp.send("Page.enable")
        cdp.send("Runtime.enable")
        cdp.send("Log.enable")
        cdp.send("Page.navigate", url=a.url)
        time.sleep(a.settle)
        # wait for load
        t0 = time.time()
        while time.time() - t0 < a.timeout:
            if cdp.evaluate("document.readyState === 'complete'"):
                break
            time.sleep(0.1)
        if a.setup:
            cdp.evaluate(a.setup)
        # poll the predicate
        t0 = time.time()
        ok = False
        while time.time() - t0 < a.timeout:
            try:
                if cdp.evaluate("!!(" + a.until + ")"):
                    ok = True
                    break
            except Exception:
                pass
            time.sleep(0.03)
        if not ok:
            sys.stderr.write("TIMEOUT waiting for: %s\n" % a.until)
            code = 2
        if a.then:
            cdp.evaluate(a.then)
        ev = a.ev
        if a.evalfile:
            with open(a.evalfile, encoding="utf-8") as f:
                ev = f.read()
        if ev:
            r = cdp.evaluate(ev)
            try:
                print(json.dumps(json.loads(r), indent=1))
            except Exception:
                print(json.dumps(r, indent=1))
        if a.out:
            params = {"format": "png", "captureBeyondViewport": True}
            if a.selector:
                box = cdp.evaluate(
                    "(function(){var e=document.querySelector(%s);if(!e)return null;"
                    "var r=e.getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,"
                    "w:r.width,h:r.height};})()" % json.dumps(a.selector))
                if box:
                    params["clip"] = {"x": box["x"], "y": box["y"], "width": box["w"],
                                      "height": box["h"], "scale": a.scale}
            r = cdp.send("Page.captureScreenshot", **params)
            outp = os.path.abspath(a.out)
            d = os.path.dirname(outp)
            if d and not os.path.isdir(d):
                os.makedirs(d)
            with open(outp, "wb") as f:
                f.write(base64.b64decode(r["data"]))
            print("wrote %s" % outp)
    finally:
        if cdp:
            cdp.close()
        if not a.keep:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
            shutil.rmtree(profile, ignore_errors=True)
    sys.exit(code)


if __name__ == "__main__":
    main()
