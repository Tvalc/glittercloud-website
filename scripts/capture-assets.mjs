import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const assets = path.join(root, "assets", "characters");

await mkdir(assets, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

await page.goto("https://www.amazon.com/videogames", {
  waitUntil: "domcontentloaded",
  timeout: 60000,
});
await page.waitForTimeout(3000);
await page.screenshot({
  path: path.join(assets, "amazon-videogames.jpg"),
  type: "jpeg",
  quality: 88,
  fullPage: false,
});

await browser.close();
console.log("Saved amazon-videogames.jpg");
