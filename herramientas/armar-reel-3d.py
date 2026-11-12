#!/usr/bin/env python3
"""Reel 3D de Base Segura (estilo vigente desde el 11-11-2026).

Uso (desde la raíz del repo, después de `armar-reel.py reel/guion.json reel/ --voz`):
  python3 herramientas/armar-reel-3d.py reel/            -> escribe reel/reel.html (escena 3D + textos)
  python3 herramientas/armar-reel-3d.py reel/ --fotos    -> además saca 6 cuadros de revisión en reel/cuadros/
  python3 herramientas/armar-reel.py reel/guion.json reel/ --grabar   -> graba y mezcla voz + efectos

Necesita reel/guion.json, reel/tiempos.json y reel/escena3d.js (formato en herramientas/3d/LEEME.md).
Los textos de pantalla salen del guion: subtítulos karaoke (palabras de tiempos.json, `resalta` en naranjo),
`texto` grande en la escena 0 (gancho), `pastilla` por escena, `tarjeta` (ley) y `cierre`.
"""
import html, json, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
COLORES = {"peligro": ("#E5484D", "#fff"), "paso": ("#FFC53D", "#0D1117"), "info": ("#1FA9E8", "#fff"), "ok": ("#25D366", "#0D1117")}
MIN_S, MAX_S = 45, 50


def norm(p):
    return re.sub(r"[^\wáéíóúñü]", "", p.lower())


def subtitulos(escenas, tiempos):
    out = []
    for e, t in zip(escenas, tiempos):
        res = {norm(w) for r in e.get("resalta", []) for w in r.split()}
        pal = t["palabras"]
        fin_escena = t["inicio"] + t["dur"]
        grupos, g = [], []
        for w in pal:  # líneas de hasta 5 palabras / 30 letras
            if g and (len(g) >= 5 or sum(len(x["p"]) + 1 for x in g) + len(w["p"]) > 30):
                grupos.append(g); g = []
            g.append(w)
        if g:
            grupos.append(g)
        for i, g in enumerate(grupos):
            a = g[0]["t"]
            b = grupos[i + 1][0]["t"] if i + 1 < len(grupos) else fin_escena - 0.1
            spans = "".join(
                f'<span class="{"r" if norm(w["p"]) in res else ""}" style="animation-delay:{w["t"]:.2f}s">{html.escape(w["p"])}</span> '
                for w in g)
            out.append(f'<div class="lin" style="animation:ver {max(b - a, 0.2):.2f}s linear {a:.2f}s none">{spans}</div>')
    return "".join(out)


def pastilla(e, t):
    p = e.get("pastilla")
    if not p:
        return ""
    if isinstance(p, str):
        p = {"texto": p, "tipo": "paso"}
    bg, fg = COLORES.get(p.get("tipo", "paso"), COLORES["paso"])
    a, d = t["inicio"] + 0.25, max(t["dur"] - 0.35, 0.8)
    return (f'<div class="pill" style="background:{bg};color:{fg};animation:pop {d:.2f}s ease-out {a:.2f}s none">'
            f'{html.escape(p["texto"].upper())}</div>')


def tarjeta(e, t):
    c = e.get("tarjeta")
    if not c:
        return ""
    ext = html.escape(c.get("extracto", ""))
    am = c.get("resaltado_amarillo")
    if am and html.escape(am) in ext:
        ext = ext.replace(html.escape(am), f"<mark>{html.escape(am)}</mark>")
    a, d = t["inicio"] + 0.3, t["dur"] - 0.3
    return (f'<div class="ley" style="animation:sube {d:.2f}s cubic-bezier(.2,1.3,.4,1) {a:.2f}s none">'
            f'<div class="enc">{html.escape(c.get("encabezado", ""))}</div><div class="art">{html.escape(c.get("articulo", ""))}</div>'
            f'<div class="ext">{ext}</div><div class="chica">🇨🇱 {html.escape(c.get("pastilla_chica", ""))}</div></div>')


def cierre(e, t, total):
    c = e.get("cierre")
    if not c:
        return ""
    logo = open(os.path.join(RAIZ, "marca/logo.svg"), encoding="utf-8").read().replace("<svg ", '<svg width="240" height="240" ', 1)
    a = t["inicio"] + 0.6
    return (f'<div class="cierre" style="animation:fundido {total - a:.2f}s ease-out {a:.2f}s none">{logo}'
            f'<div class="franja">{html.escape(c.get("franja", "Cotiza en basesegura.cl"))}</div>'
            f'<div class="debajo">{html.escape(c.get("debajo", "contacto@basesegura.cl"))}</div>'
            f'<div class="fuente">{html.escape(c.get("fuente", ""))}</div></div>')


def gancho(e, t):
    txt = e.get("texto")
    if not txt:
        return ""
    s = html.escape(txt)
    for r in e.get("resalta", []):
        s = s.replace(html.escape(r), f'<b>{html.escape(r)}</b>')
    return f'<div class="gancho" style="animation:gancho {t["dur"]:.2f}s cubic-bezier(.2,1.5,.4,1) 0.05s none">{s}</div>'


CSS = """
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;background:#141b29;font-family:Outfit,Manrope,sans-serif;position:relative}
#gl,#gl canvas{position:absolute;inset:0}
.ui{position:absolute;inset:0}
.marca{position:absolute;top:70px;right:60px;color:#fff;font:700 34px Manrope;opacity:.85;text-shadow:0 2px 8px #0008}
.subs{position:absolute;top:170px;left:60px;right:60px;height:240px}
.lin{position:absolute;inset:0;display:flex;flex-wrap:wrap;align-content:center;justify-content:center;gap:0 18px;text-align:center;
 font-weight:800;font-size:68px;line-height:1.12;color:#fff;text-shadow:0 6px 0 #0D1117,0 10px 30px rgba(0,0,0,.6);opacity:0}
.lin span{display:inline-block;opacity:.35;animation:pal .25s ease-out both}
.lin span.r{color:#F2A33A}
@keyframes pal{from{opacity:.35;transform:translateY(14px) scale(.9)}to{opacity:1;transform:none}}
@keyframes ver{0%,100%{opacity:1}}
.gancho{position:absolute;top:560px;left:70px;right:70px;text-align:center;font:900 104px/1.05 Outfit;color:#fff;
 -webkit-text-stroke:8px #0D1117;paint-order:stroke;text-shadow:0 16px 40px rgba(0,0,0,.55);opacity:0}
.gancho b{color:#F2A33A}
@keyframes gancho{0%{opacity:0;transform:scale(.4) rotate(-4deg)}12%{opacity:1;transform:scale(1.06)}20%,88%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(.9)}}
.pill{position:absolute;top:1330px;left:50%;max-width:960px;padding:22px 40px;border-radius:999px;font:800 46px/1.15 Outfit;text-align:center;
 box-shadow:0 14px 0 rgba(0,0,0,.35);opacity:0;transform:translateX(-50%)}
@keyframes pop{0%{opacity:0;transform:translateX(-50%) scale(.3)}10%{opacity:1;transform:translateX(-50%) scale(1.1)}18%,90%{opacity:1;transform:translateX(-50%) scale(1)}100%{opacity:0;transform:translateX(-50%) scale(.9)}}
.ley{position:absolute;top:900px;left:70px;right:70px;background:#fff;border-radius:34px;padding:34px 40px;border-left:18px solid #1FA9E8;
 color:#0D1117;box-shadow:0 20px 50px rgba(0,0,0,.45);opacity:0}
.ley .enc{font:800 30px Outfit;color:#1FA9E8;letter-spacing:2px}.ley .art{font:900 58px Outfit;margin:6px 0 12px}
.ley .ext{font:600 36px/1.3 Manrope}.ley mark{background:#FFE066;padding:0 6px;border-radius:6px}
.ley .chica{margin-top:16px;display:inline-block;background:#eef6fc;border-radius:999px;padding:8px 20px;font:700 26px Manrope;color:#355}
@keyframes sube{0%{opacity:0;transform:translateY(160px)}15%,92%{opacity:1;transform:none}100%{opacity:0}}
.cierre{position:absolute;inset:0;background:rgba(13,17,23,.94);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;opacity:0;padding:0 70px 260px}
.cierre .franja{background:#1FA9E8;color:#fff;font:900 54px/1.15 Outfit;padding:26px 44px;border-radius:30px;text-align:center}
.cierre .debajo{color:#fff;font:700 44px Manrope}
.cierre .fuente{position:absolute;bottom:430px;left:80px;right:80px;color:#9aa6b8;font:500 24px/1.35 Manrope;text-align:center}
@keyframes fundido{0%{opacity:0}12%,100%{opacity:1}}
"""


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    R = sys.argv[1].rstrip("/")
    guion = json.load(open(f"{R}/guion.json", encoding="utf-8"))
    T = json.load(open(f"{R}/tiempos.json", encoding="utf-8"))
    escenas, tiempos, total = guion["escenas"], T["escenas"], T["total"]
    if not (MIN_S <= total <= MAX_S + 1.5):
        print(f"OJO: el reel dura {total} s. Iñaki pide entre {MIN_S} y {MAX_S} s: acorta o alarga las frases de voz y vuelve a pedir la voz.")
    escena = os.path.abspath(f"{R}/escena3d.js")
    if not os.path.exists(escena):
        sys.exit(f"Falta {escena} (formato en herramientas/3d/LEEME.md)")
    entrada = os.path.abspath(f"{R}/.entrada3d.js")
    open(entrada, "w").write(
        f"import {{ iniciar }} from '{RAIZ}/herramientas/3d/motor.js';\nimport PLAN from '{escena}';\n"
        "document.fonts.ready.then(() => iniciar(PLAN, window.TIEMPOS));\n")
    salida = f"{R}/.escena3d.bundle.js"
    subprocess.run([os.path.join(RAIZ, "node_modules/.bin/esbuild"), entrada, "--bundle", "--format=iife", "--minify",
                    f"--outfile={salida}", "--log-level=warning"], check=True, cwd=RAIZ)
    js = open(salida, encoding="utf-8").read()
    os.remove(entrada); os.remove(salida)
    ui = (subtitulos(escenas, tiempos) and f'<div class="subs">{subtitulos(escenas, tiempos)}</div>') + gancho(escenas[0], tiempos[0])
    ui += "".join(pastilla(e, t) + tarjeta(e, t) for e, t in zip(escenas, tiempos))
    ui += "".join(cierre(e, t, total) for e, t in zip(escenas, tiempos))
    pagina = (f'<!doctype html><html><head><meta charset="utf-8"><link href="file://{RAIZ}/fonts/fonts.css" rel="stylesheet">'
              f'<style>{CSS}</style></head><body><div id="gl"></div><div class="ui"><div class="marca">◎ @basesegura.cl</div>{ui}</div>'
              f'<script>window.TIEMPOS={json.dumps(T)};</script><script>{js}</script></body></html>')
    open(f"{R}/reel.html", "w", encoding="utf-8").write(pagina)
    print(f"Listo {R}/reel.html ({total} s). Ahora: python3 herramientas/armar-reel.py {R}/guion.json {R} --grabar")
    if "--fotos" in sys.argv:
        os.makedirs(f"{R}/cuadros", exist_ok=True)
        ts = [round(total * k, 2) for k in (0.03, 0.18, 0.35, 0.55, 0.75, 0.95)]
        subprocess.run(["node", os.path.join(AQUI, "3d/fotos.mjs"), os.path.abspath(f"{R}/reel.html"), os.path.abspath(f"{R}/cuadros"), *map(str, ts)], check=True, cwd=RAIZ)
        print("Cuadros en", f"{R}/cuadros/")


if __name__ == "__main__":
    main()
