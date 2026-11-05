// Uso: node herramientas/cuadros.mjs reel.html salida_prefijo t1 t2 ... (segundos) — revisa cuadros sin grabar el video
import path from 'node:path'; import { abrir } from './navegador.mjs';
const [html, pref, ...ts] = process.argv.slice(2);
const b = await abrir(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + path.resolve(html)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
for (const t of ts) { await p.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t * 1000; }), +t); await p.screenshot({ path: `${pref}${t}.png` }); }
await b.close();
