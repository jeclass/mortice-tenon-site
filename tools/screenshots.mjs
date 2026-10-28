// Full-page screenshots of every page at 1440px (desktop) and 390px (mobile) into _review/.
// Uses Chrome DevTools Protocol over Node's built-in WebSocket; no npm packages needed.
//   node tools/screenshots.mjs [baseUrl]
// baseUrl defaults to the local server from tools/serve.py.
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const base = process.argv[2] || "http://127.0.0.1:8765/mortice-tenon-site/";
const outDir = join(root, "_review");
mkdirSync(outDir, { recursive: true });

const pages = [
  ["home", ""], ["products", "products/"], ["install", "install/"], ["wholesale", "wholesale/"],
  ["about", "about/"], ["contact", "contact/"], ["privacy", "privacy/"], ["404", "no-such-page/"],
];
const viewports = [
  ["desktop", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false }],
  ["mobile", { width: 390, height: 844, deviceScaleFactor: 2, mobile: true }],
];

const PORT = 9333; // never 9222 (another profile's Chrome)
const chrome = spawn("google-chrome", [
  "--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "mtsite-shot-"))}`, "about:blank",
], { stdio: "ignore" });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsUrl;
for (let i = 0; i < 50 && !wsUrl; i++) {
  try {
    const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
    wsUrl = list.find((t) => t.type === "page")?.webSocketDebuggerUrl;
  } catch { /* chrome still starting */ }
  if (!wsUrl) await sleep(200);
}
if (!wsUrl) { chrome.kill(); throw new Error("Chrome did not start"); }

const ws = new WebSocket(wsUrl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let id = 0;
const pending = new Map();
const waiters = [];
ws.addEventListener("message", (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  else if (msg.method) waiters.filter((w) => w.method === msg.method).forEach((w) => w.resolve(msg));
});
const send = (method, params = {}) => new Promise((resolve) => {
  const mid = ++id; pending.set(mid, resolve); ws.send(JSON.stringify({ id: mid, method, params }));
});
const once = (method) => new Promise((resolve) => {
  const w = { method, resolve: (m) => { waiters.splice(waiters.indexOf(w), 1); resolve(m); } };
  waiters.push(w);
});

await send("Page.enable");
for (const [vpName, vp] of viewports) {
  await send("Emulation.setDeviceMetricsOverride", vp);
  for (const [name, path] of pages) {
    const loaded = once("Page.loadEventFired");
    await send("Page.navigate", { url: base + path });
    await loaded;
    // Scroll to the bottom and back so lazy images load, then let fonts settle.
    await send("Runtime.evaluate", { expression: "window.scrollTo(0, document.body.scrollHeight)" });
    await sleep(600);
    await send("Runtime.evaluate", { expression: "window.scrollTo(0, 0)" });
    await send("Runtime.evaluate", { expression: "document.fonts.ready", awaitPromise: true });
    await sleep(400);
    const m = await send("Page.getLayoutMetrics");
    const h = Math.ceil(m.result.cssContentSize.height);
    const shot = await send("Page.captureScreenshot", {
      format: "png", captureBeyondViewport: true,
      clip: { x: 0, y: 0, width: vp.width, height: h, scale: 1 },
    });
    const file = join(outDir, `${name}-${vpName}.png`);
    writeFileSync(file, Buffer.from(shot.result.data, "base64"));
    console.log(`${file}  ${vp.width}x${h}`);
  }
}
ws.close();
chrome.kill();
