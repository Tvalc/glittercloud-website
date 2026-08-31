#!/usr/bin/env python
"""THE PHASE 0 ACCEPTANCE GATE: play the level on the keyboard, driver disabled.

This does not call into the simulation. It switches the scripted driver OFF and
then dispatches REAL key events through the Chrome input pipeline, so the path
under test is exactly a player's:

    Input.dispatchKeyEvent -> page keydown/keyup -> keys[] -> humanInput()
                           -> W.input -> step()

The only thing this script reads back is the runner's x and whether his feet are
down, which is what a player sees. It decides to press Space the way a player
does: a hole or a ledge is coming up, so jump. If the level cannot be finished
this way, it is not a game, and Phase 0 has not passed.

  python tools/playtest.py --url http://localhost:8660/vault-chibi/phase0.html
"""
import argparse, base64, json, os, shutil, subprocess, sys, tempfile, time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import CDP, http_json, find_chrome  # noqa: E402

VK = {"ArrowRight": 39, "ArrowLeft": 37, "Space": 32, "KeyD": 68, "KeyR": 82}
KEYTXT = {"ArrowRight": "ArrowRight", "ArrowLeft": "ArrowLeft", "Space": " ",
          "KeyD": "d", "KeyR": "r"}


def key(cdp, code, down):
    cdp.send("Input.dispatchKeyEvent",
             type="rawKeyDown" if down else "keyUp",
             code=code, key=KEYTXT[code],
             windowsVirtualKeyCode=VK[code], nativeVirtualKeyCode=VK[code])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--port", type=int, default=9334)
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--shots", default="", help="directory to drop frames into")
    ap.add_argument("--width", type=int, default=1060)
    ap.add_argument("--height", type=int, default=660)
    a = ap.parse_args()

    profile = tempfile.mkdtemp(prefix="playprof")
    proc = subprocess.Popen([
        find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--no-first-run", "--no-default-browser-check", "--mute-audio",
        "--window-size=%d,%d" % (a.width, a.height),
        "--user-data-dir=" + profile,
        "--remote-debugging-port=%d" % a.port, "--remote-allow-origins=*",
        "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    cdp = None
    rc = 1
    try:
        http_json("http://127.0.0.1:%d/json/version" % a.port)
        tabs = http_json("http://127.0.0.1:%d/json/list" % a.port)
        pages = [t for t in tabs if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
        cdp = CDP(pages[0]["webSocketDebuggerUrl"])
        cdp.send("Page.enable")
        cdp.send("Runtime.enable")
        cdp.send("Page.navigate", url=a.url)
        time.sleep(1.2)
        while not cdp.evaluate("document.readyState==='complete'"):
            time.sleep(0.1)

        # the level's jump cues, read off the page the same way a player reads
        # the screen: where the holes and the ledges are.
        cues = cdp.evaluate("JSON.stringify(window.__probe.jumpCues())")
        cues = json.loads(cues)
        sys.stderr.write("cues: %s\n" % [c["id"] for c in cues])

        # DRIVER OFF. From here nothing but key events touches the runner.
        cdp.evaluate("window.__probe.setDriver(false); window.__probe.restart();"
                     "window.__probe.setDriver(false);")
        assert cdp.evaluate("window.__probe.world().driverOn") is False, "driver still on"

        cdp.send("Input.dispatchKeyEvent", type="rawKeyDown", code="Escape",
                 key="Escape", windowsVirtualKeyCode=27)  # focus the document
        key(cdp, "ArrowRight", True)          # hold right, like a player would

        pending = list(cues)
        pressed = []
        space_until = 0.0
        space_down = False
        shots = []
        t0 = time.time()
        last_x = -999
        stuck_since = t0
        while time.time() - t0 < a.seconds:
            st = json.loads(cdp.evaluate("JSON.stringify(window.__probe.state())"))
            now = time.time()
            if st["x"] > last_x + 0.5:
                last_x, stuck_since = st["x"], now
            if st.get("finished"):
                rc = 0
                break
            if st.get("held"):
                sys.stderr.write("FELL IN at x=%.1f\n" % st["x"])
                break
            if now - stuck_since > 4.0:
                sys.stderr.write("STUCK at x=%.1f for 4s\n" % st["x"])
                break
            # a player presses jump when the next obstacle is right in front
            if pending and st["x"] >= pending[0]["atX"] and st["onGround"]:
                c = pending.pop(0)
                key(cdp, "Space", True)
                space_down = True
                space_until = now + 0.30
                pressed.append({"id": c["id"], "x": round(st["x"], 1)})
                if a.shots and c["id"].startswith("PIT"):
                    shots.append((c["id"], now + 0.16))
            if space_down and now >= space_until:
                key(cdp, "Space", False)
                space_down = False
            for i, (name, when) in enumerate(list(shots)):
                if now >= when:
                    shots.pop(i)
                    r = cdp.send("Page.captureScreenshot", format="png")
                    p = os.path.join(a.shots, "play-%s.png" % name)
                    with open(p, "wb") as f:
                        f.write(base64.b64decode(r["data"]))
                    sys.stderr.write("shot %s\n" % p)
                    break
            time.sleep(0.012)

        key(cdp, "ArrowRight", False)
        st = json.loads(cdp.evaluate("JSON.stringify(window.__probe.state())"))
        ev = json.loads(cdp.evaluate("JSON.stringify(window.__probe.events())"))
        errs = cdp.evaluate("JSON.stringify(window.__consoleErrors||[])")
        print(json.dumps({
            "driverOn": cdp.evaluate("window.__probe.world().driverOn"),
            "reachedGoal": bool(st.get("finished")),
            "finalX": round(st["x"], 1),
            "simSeconds": round(st["t"], 2),
            "keyPresses": len(pressed),
            "spacePressesAt": pressed,
            "jumpsProduced": len([e for e in ev if e["kind"] == "jump"]),
            "landings": len([e for e in ev if e["kind"] == "land"]),
            "fellIn": [e for e in ev if e["kind"] == "fell-in"],
            "consoleErrors": json.loads(errs),
        }, indent=1))
    finally:
        if cdp:
            cdp.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        shutil.rmtree(profile, ignore_errors=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
