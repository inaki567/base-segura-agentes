// Uso: node herramientas/grabar-reel.mjs reel/reel.html reel/reel.mp4 20
import { chromium } from 'playwright';
import ffmpeg from 'ffmpeg-static';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';

const [html, out, secs = '20'] = process.argv.slice(2);
if (!html || !out) { console.error('Uso: node grabar-reel.mjs entrada.html salida.mp4 segundos'); process.exit(1); }
const fps = 30, total = Math.round(Number(secs) * fps);
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'reel-'));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto('file://' + path.resolve(html));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(800);
await page.evaluate(() => document.getAnimations().forEach(a => a.pause()));
for (let i = 0; i < total; i++) {
  const t = (i * 1000) / fps;
  await page.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t; }), t);
  await page.screenshot({ path: path.join(dir, `f${String(i).padStart(5, '0')}.png`) });
}
await browser.close();
execFileSync(ffmpeg, ['-y', '-framerate', String(fps), '-i', path.join(dir, 'f%05d.png'),
  '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:a', 'aac', '-b:a', '128k',
  '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: 'inherit' });
fs.rmSync(dir, { recursive: true, force: true });
console.log('Reel listo:', out);
