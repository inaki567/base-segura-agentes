// Abre Chromium: usa el de Playwright si está, si no busca uno ya instalado (nube de Claude).
import { chromium } from 'playwright';
import fs from 'node:fs'; import path from 'node:path';
function buscar() {
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  if (!fs.existsSync(base)) return undefined;
  for (const d of fs.readdirSync(base).filter(d => /^chromium-\d+$/.test(d)).sort().reverse()) {
    for (const sub of ['chrome-linux64/chrome', 'chrome-linux/chrome']) {
      const p = path.join(base, d, sub); if (fs.existsSync(p)) return p;
    }
  }
}
export async function abrir() {
  try { return await chromium.launch(); }
  catch { return await chromium.launch({ executablePath: buscar() }); }
}
