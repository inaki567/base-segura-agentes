// node herramientas/3d/fotos.mjs reel.html carpeta t1 t2 ...  -> cuadros PNG (escala 1/2) para revisar sin grabar
import { abrir } from '../navegador.mjs';
import path from 'node:path';
const [html, dir, ...ts] = process.argv.slice(2);
const b = await abrir(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', e => console.log('ERROR en la página:', e.message));
await p.goto('file://' + path.resolve(html)); await p.evaluate(() => document.fonts.ready);
await p.waitForFunction(() => window.__listo, null, { timeout: 30000 });
await p.evaluate(() => document.getAnimations().forEach(a => a.pause()));
for (const t of ts.map(Number)) {
  await p.evaluate(t => { document.getAnimations().forEach(a => a.currentTime = t * 1000); window.renderAt(t); }, t);
  await p.screenshot({ path: path.join(dir, `t${t.toFixed(1)}.jpg`), type: 'jpeg', quality: 80, scale: 'css' });
}
await b.close();
