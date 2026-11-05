// Uso: node herramientas/foto.mjs entrada.html salida.png [ancho] [alto]
// Exporta un HTML a PNG o JPG esperando a que carguen las fuentes.
import path from 'node:path'; import { abrir } from './navegador.mjs';
const [html, out, w = '1080', h = '1350'] = process.argv.slice(2);
if (!html || !out) { console.error('Uso: node herramientas/foto.mjs entrada.html salida.png [ancho] [alto]'); process.exit(1); }
const browser = await abrir();
const page = await browser.newPage({ viewport: { width: +w, height: +h } });
await page.goto('file://' + path.resolve(html));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(1200);
await page.screenshot({ path: out, type: out.endsWith('.jpg') ? 'jpeg' : 'png', quality: out.endsWith('.jpg') ? 88 : undefined });
await browser.close();
console.log('Listo:', out);
