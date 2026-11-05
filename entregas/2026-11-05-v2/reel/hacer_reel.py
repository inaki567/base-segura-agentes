#!/usr/bin/env python3
# Reel 2026-11-05: "Terremoto en la pega" — estilo marca/ESTILO-REELS.md
import json, sys, html
R = sys.argv[1]
T = json.load(open(f"{R}/tiempos.json", encoding="utf-8"))
E = T["escenas"]; TOT = T["total"]
LOGO = open("/tmp/bs/marca/logo.svg").read().replace('<svg ', '<svg width="220" height="220" ', 1)

def iso(x, y, z=0):
    return 540 + (x - y) * 52, 250 + (x + y) * 30 - z * 60

def poly(pts, fill, extra=""):
    p = " ".join(f"{a:.1f},{b:.1f}" for a, b in (iso(*q) for q in pts))
    return f'<polygon points="{p}" fill="{fill}" {extra}/>'

def caja(x0, y0, z0, dx, dy, dz, top, left, right, extra=""):
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    return (f'<g {extra}>' +
            poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], left) +
            poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], right) +
            poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top) + '</g>')

def pct(t): return max(0, min(100, t / TOT * 100))

# ---------- mundo (bodega) ----------
w = []
w.append(poly([(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)], "#1b2433"))
for i in range(1, 10):
    a, b = iso(i, 0), iso(i, 10); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff10" stroke-width="2"/>')
    a, b = iso(0, i), iso(10, i); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff10" stroke-width="2"/>')
w.append(poly([(0, 0, 0), (10, 0, 0), (10, 0, 5), (0, 0, 5)], "#273246"))
w.append(poly([(0, 0, 0), (0, 10, 0), (0, 10, 5), (0, 0, 5)], "#1f2838"))
# ventana (muro izquierdo x=0)
w.append(poly([(0, 2, 2), (0, 5.5, 2), (0, 5.5, 4.2), (0, 2, 4.2)], "#1FA9E8", 'opacity=".55" class="vidrio"'))
w.append(poly([(0, 3.75, 2), (0, 3.8, 2), (0, 3.8, 4.2), (0, 3.75, 4.2)], "#0D1117"))
# puerta de salida (muro del fondo y=0)
w.append(poly([(7.4, 0, 0), (9.2, 0, 0), (9.2, 0, 3.1), (7.4, 0, 3.1)], "#0f3d26"))
w.append(poly([(7.6, 0, 3.4), (9.0, 0, 3.4), (9.0, 0, 4.0), (7.6, 0, 4.0)], "#25D366", 'class="salida"'))
# ruta de evacuación (flechas verdes en el piso)
for (x, y) in [(6.2, 6.2), (7.0, 4.8), (7.6, 3.4), (8.1, 2.0)]:
    a = iso(x, y); w.append(f'<g class="ruta" transform="translate({a[0]:.0f},{a[1]:.0f})"><path d="M-26 8 L0 -10 L26 8" stroke="#25D366" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
# estante con cajas (contra el fondo)
for z in (0, 1.2, 2.4, 3.6):
    w.append(caja(1, 0.1, z, 3.6, 1.1, 0.12, "#8a96a8", "#5d6878", "#4a5463"))
for x in (1, 4.5):
    w.append(caja(x, 1.1, 0, 0.12, 0.12, 3.72, "#8a96a8", "#5d6878", "#4a5463"))
cajas = [(1.3, 0.3, 1.32, "#F2A33A"), (2.4, 0.3, 1.32, "#c98428"), (3.5, 0.3, 2.52, "#F2A33A"), (1.6, 0.3, 2.52, "#d9d2c3"), (2.8, 0.3, 3.72, "#c98428")]
t_caida = E[1]["inicio"] + 1.8
for k, (x, y, z, c) in enumerate(cajas):
    d = 0.35 + k * 0.45
    w.append(caja(x, y, z, 0.8, 0.7, 0.75, c, "#00000033", "#00000055",
                  f'class="cae" style="--dz:{z*60:.0f}px;animation-delay:{t_caida + d:.2f}s"'))
# mesa
w.append(caja(5, 4, 1.15, 2.2, 1.6, 0.18, "#9aa4b2", "#6b7584", "#5a6372"))
for (x, y) in [(5.1, 4.1), (7.0, 4.1), (5.1, 5.4), (7.0, 5.4)]:
    w.append(caja(x, y, 0, 0.12, 0.12, 1.15, "#6b7584", "#5a6372", "#4a5463"))
# zona de seguridad (afuera, al lado de la puerta)
a = iso(9.3, 1.2)
w.append(f'<g class="zs"><ellipse cx="{a[0]+70:.0f}" cy="{a[1]-40:.0f}" rx="95" ry="48" fill="#25D36633" stroke="#25D366" stroke-width="5" stroke-dasharray="14 10"/></g>')

def mono(color="#3b5bdb", casco="#FFD43B", cara="feliz", escala=1.0):
    ojos = '<circle cx="-13" cy="-150" r="5" fill="#111"/><circle cx="13" cy="-150" r="5" fill="#111"/>'
    boca = {'feliz': '<path d="M-10 -134 Q0 -126 10 -134" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>',
            'susto': '<ellipse cx="0" cy="-131" rx="6" ry="8" fill="#111"/>'}[cara]
    cejas = '<path d="M-21 -164 L-7 -160 M21 -164 L7 -160" stroke="#111" stroke-width="4" stroke-linecap="round"/>' if cara == 'susto' else ''
    return f'''<g transform="scale({escala})">
<ellipse cx="0" cy="0" rx="34" ry="11" fill="#0006"/>
<g class="pierna p1"><rect x="-20" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<g class="pierna p2"><rect x="3" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<rect x="-26" y="-112" width="52" height="62" rx="20" fill="{color}"/>
<rect x="-26" y="-84" width="52" height="9" fill="#FFD43B"/>
<g class="brazos"><rect x="-38" y="-108" width="14" height="46" rx="7" fill="{color}"/><rect x="24" y="-108" width="14" height="46" rx="7" fill="{color}"/></g>
<circle cx="0" cy="-146" r="34" fill="#F2C9A0"/>
{ojos}{cejas}{boca}
<path d="M-34 -160 A34 32 0 0 1 34 -160 Z" fill="{casco}"/><rect x="-40" y="-164" width="80" height="9" rx="4.5" fill="{casco}"/>
</g>'''

def mono_agachado(color, casco):
    return f'''<g><ellipse cx="0" cy="0" rx="40" ry="12" fill="#0006"/>
<rect x="-28" y="-62" width="56" height="58" rx="22" fill="{color}"/><rect x="-28" y="-40" width="56" height="8" fill="#FFD43B"/>
<circle cx="0" cy="-84" r="30" fill="#F2C9A0"/>
<path d="M-30 -96 A30 28 0 0 1 30 -96 Z" fill="{casco}"/><rect x="-36" y="-100" width="72" height="8" rx="4" fill="{casco}"/>
<path d="M-40 -70 Q0 -140 40 -70" stroke="{color}" stroke-width="14" fill="none" stroke-linecap="round"/></g>'''

# personajes: posiciones por tiempo (pantalla)
def pos(x, y): return iso(x, y)
gente = [
    dict(color="#3b5bdb", casco="#FFD43B", ruta=[(0, (3.2, 2.6)), (E[2]["inicio"] + 0.5, (3.2, 2.6)), (E[2]["inicio"] + 3.2, (5.6, 6.4)),
         (E[4]["inicio"] + 1.0, (5.6, 6.4)), (E[4]["inicio"] + 5.5, (8.3, 0.6))]),
    dict(color="#7048e8", casco="#FFFFFF", ruta=[(0, (1.6, 6.5)), (E[2]["inicio"] + 0.8, (1.6, 6.5)), (E[2]["inicio"] + 3.4, (4.4, 6.8)),
         (E[4]["inicio"] + 1.6, (4.4, 6.8)), (E[4]["inicio"] + 6.2, (8.0, 0.8))]),
    dict(color="#868e96", casco="#FFD43B", ruta=[(0, (7.8, 7.6)), (E[2]["inicio"] + 1.0, (7.8, 7.6)), (E[2]["inicio"] + 3.0, (7.6, 6.6)),
         (E[4]["inicio"] + 0.6, (7.6, 6.6)), (E[4]["inicio"] + 4.8, (8.6, 0.7))]),
]
css_extra, gente_svg = [], []
t_agacha, t_levanta = E[3]["inicio"] + 0.3, E[4]["inicio"] + 0.6
for n, g in enumerate(gente):
    frames = []
    for t, (x, y) in g["ruta"]:
        sx, sy = pos(x, y)
        frames.append(f"{pct(t):.2f}%{{transform:translate({sx:.0f}px,{sy:.0f}px)}}")
    sx, sy = pos(*g["ruta"][-1][1])
    frames.append(f"100%{{transform:translate({sx:.0f}px,{sy:.0f}px)}}")
    css_extra.append(f"@keyframes mueve{n}{{{' '.join(frames)}}} .g{n}{{animation:mueve{n} {TOT}s linear 0s both}}")
    sale = E[4]["inicio"] + 4.6 + n * 0.5
    gente_svg.append(f'''<g class="g{n}"><g class="sale" style="animation-delay:{sale:.2f}s">
<g class="de-pie" style="--a:{t_agacha:.2f}s;--b:{t_levanta:.2f}s">{mono(g["color"], g["casco"], "susto")}</g>
<g class="agachado" style="--a:{t_agacha:.2f}s;--b:{t_levanta:.2f}s">{mono_agachado(g["color"], g["casco"])}</g></g></g>''')

# cámara (mundo)
cam = [(0, 1.35, -60, 120), (E[1]["inicio"], 1.0, 0, 0), (E[1]["inicio"] + 4, 1.08, 30, -20), (E[2]["inicio"], 1.25, 40, -120),
       (E[3]["inicio"], 1.55, -10, -260), (E[4]["inicio"], 1.15, -120, 40), (E[4]["inicio"] + 6, 1.35, -260, 160),
       (E[5]["inicio"], 1.05, 0, 0), (E[7]["inicio"], 1.0, 0, 0)]
cam_kf = " ".join(f"{pct(t):.2f}%{{transform:translate({x}px,{y}px) scale({s})}}" for t, s, x, y in cam)
tiembla = []
for (a, b) in [(E[0]["inicio"], E[2]["inicio"] - 0.4)]:
    tiembla.append(f"animation:tiembla .11s linear {a:.2f}s {int((b-a)/0.11)} both")

# subtítulos karaoke
clave = {0: ["Terremoto", "primero?"], 1: ["moverse."], 2: ["calma,", "ventanas", "estantes."], 3: ["agáchate,", "cúbrete", "afírmate,"],
         4: ["evacúa", "zona", "seguridad.", "ascensores."], 5: ["opcional.", "plan", "emergencia,", "una", "vez", "al", "año."],
         6: ["simulacro"], 7: ["plan", "emergencia.", "base", "segura", "punto", "cl,"]}
subs = []
for i, e in enumerate(E):
    ws = "".join(f'<span class="w{" k" if p["p"] in clave.get(i, []) else ""}" style="animation-delay:{p["t"]:.2f}s">{html.escape(p["p"])}</span> ' for p in e["palabras"])
    subs.append(f'<div class="sub win" style="--i:{e["inicio"]:.2f}s;--d:{e["dur"]:.2f}s">{ws}</div>')

def pill(txt, bg, fg, t, d, top, extra=""):
    return f'<div class="pill win" style="--i:{t:.2f}s;--d:{d:.2f}s;top:{top}px;{extra}"><span class="pop" style="animation-delay:{t:.2f}s;background:{bg};color:{fg}">{txt}</span></div>'

e = E
fin_mundo = e[7]["inicio"]
pills = [
    pill("⚠️ SISMO FUERTE EN LA BODEGA", "#E5484D", "#fff", e[1]["inicio"] + 0.8, e[1]["dur"] - 0.8, 1330),
    pill("3 COSAS · ⏱ EN EL MOMENTO", "#FFC53D", "#0D1117", e[2]["inicio"] + 0.2, e[2]["dur"] - 0.2, 1240),
    pill("1 · ALÉJATE DE VENTANAS Y ESTANTES", "#1FA9E8", "#0D1117", e[2]["inicio"] + 1.6, e[2]["dur"] - 1.6, 1340),
    pill("2 · AGÁCHATE, CÚBRETE Y AFÍRMATE", "#1FA9E8", "#0D1117", e[3]["inicio"] + 0.4, e[3]["dur"] - 0.4, 1340),
    pill("3 · EVACÚA A LA ZONA DE SEGURIDAD", "#25D366", "#0D1117", e[4]["inicio"] + 0.6, e[4]["dur"] - 0.6, 1340),
    pill("🚫 NADA DE ASCENSORES", "#E5484D", "#fff", e[4]["inicio"] + 5.4, e[4]["dur"] - 5.4, 1240),
]
gancho = f'''<div class="gancho win" style="--i:0s;--d:{e[1]['inicio']:.2f}s">
<div class="gtit">Terremoto <span style="color:#F2A33A">en la pega</span>:<br>¿qué haces primero?</div>
<svg viewBox="-110 -250 220 280" class="gmono"><g class="tiemblaG">{mono("#3b5bdb", "#FFD43B", "susto", 1.0)}</g></svg></div>'''
ley = f'''<div class="ley win" style="--i:{e[5]['inicio']+0.6:.2f}s;--d:{e[5]['dur']-0.6:.2f}s"><div class="ley-card">
<div class="ley-h">DECRETO 44 · CHILE</div><div class="ley-art">Art. 19</div>
<p>Plan de emergencia: debe ensayarse "<mark>a lo menos una vez al año</mark> simulando una emergencia real en la entidad empleadora".</p>
<div class="ley-tag">🇨🇱 DS 44 · Chile · art. 19</div></div></div>'''
tel = f'''<div class="tel win" style="--i:{e[6]['inicio']:.2f}s;--d:{e[6]['dur']:.2f}s"><div class="tel-card">
<div class="tel-h">CHECKLIST DE TU EMPRESA</div>
<div class="chk"><span class="x">✕</span> Plan de emergencia</div><div class="chk"><span class="x">✕</span> Simulacro 2026</div><div class="chk"><span class="x">✕</span> Vías de evacuación señalizadas</div></div></div>'''
cta = f'''<div class="cta win" style="--i:{e[7]['inicio']:.2f}s;--d:{TOT-e[7]['inicio']:.2f}s">
<div class="logo">{LOGO}</div>
<div class="cta-t">¿Tu plan de emergencia<br><span style="color:#F2A33A">está al día?</span></div>
<div class="cta-band">Cotiza en 1 minuto en <b>basesegura.cl</b></div>
<div class="cta-mail">contacto@basesegura.cl</div>
<div class="fuente">Fuente: Decreto 44 (Chile), arts. 15 y 19.</div></div>'''

CSS = f"""
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;background:radial-gradient(circle at 50% 45%,#1a2233 0,#0D1117 70%);font-family:Manrope;color:#fff}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#ffffff08 2px,transparent 2px),linear-gradient(90deg,#ffffff08 2px,transparent 2px);background-size:90px 90px}}
.win{{opacity:0;animation:show var(--d) linear var(--i) both}}
@keyframes show{{0%{{opacity:0}}4%{{opacity:1}}96%{{opacity:1}}100%{{opacity:0}}}}
.handle{{position:absolute;top:96px;right:70px;font-family:Outfit;font-weight:800;font-size:28px;opacity:.85;display:flex;gap:10px;align-items:center}}
.handle i{{width:30px;height:30px;border:4px solid #fff;border-radius:9px;display:inline-block}}
.mundo-wrap{{position:absolute;left:0;right:0;top:440px;height:1000px;animation:ocultaMundo {TOT}s linear both}}
@keyframes ocultaMundo{{0%{{opacity:.35}}{pct(e[1]['inicio']-0.2):.2f}%{{opacity:.35}}{pct(e[1]['inicio']+0.2):.2f}%{{opacity:1}}{pct(e[5]['inicio']+0.3):.2f}%{{opacity:1}}{pct(e[5]['inicio']+1):.2f}%{{opacity:.35}}{pct(fin_mundo-0.2):.2f}%{{opacity:.35}}{pct(fin_mundo+0.3):.2f}%{{opacity:0}}100%{{opacity:0}}}}
.cam{{width:1080px;height:1000px;transform-origin:540px 520px;animation:cam {TOT}s ease-in-out both}}
@keyframes cam{{{cam_kf}}}
.shake{{{tiembla[0]}}}
@keyframes tiembla{{0%{{transform:none}}25%{{transform:translate(12px,-7px) rotate(.5deg)}}50%{{transform:translate(-11px,8px)}}75%{{transform:translate(8px,5px) rotate(-.5deg)}}100%{{transform:none}}}}
.cae{{animation:cae .9s cubic-bezier(.5,0,1,.6) both}}
@keyframes cae{{from{{transform:none}}to{{transform:translateY(var(--dz)) rotate(8deg)}}}}
.ruta{{opacity:0;animation:rutaOn .6s ease-out {e[4]['inicio']:.2f}s both}}
@keyframes rutaOn{{to{{opacity:1}}}}
.salida{{animation:parpadea .5s steps(2) {e[4]['inicio']:.2f}s 14 both}}
@keyframes parpadea{{50%{{opacity:.3}}}}
.zs{{opacity:0;animation:rutaOn .5s ease-out {e[4]['inicio']+3:.2f}s both}}
.de-pie{{animation:fuera .01s linear var(--a) both, dentro .01s linear var(--b) forwards}}
.agachado{{opacity:0;animation:dentro .01s linear var(--a) both, fuera .01s linear var(--b) forwards}}
@keyframes fuera{{to{{opacity:0}}}} @keyframes dentro{{to{{opacity:1}}}}
.pierna{{transform-box:fill-box;transform-origin:50% 0}}
.g0 .p1,.g1 .p1,.g2 .p1{{animation:paso .35s ease-in-out infinite alternate}} .g0 .p2,.g1 .p2,.g2 .p2{{animation:paso .35s ease-in-out infinite alternate-reverse}}
@keyframes paso{{from{{transform:rotate(-14deg)}}to{{transform:rotate(14deg)}}}}
.sale{{animation:salir .5s ease-in both}} @keyframes salir{{from{{opacity:1}}to{{opacity:0}}}}
{' '.join(css_extra)}
.sub{{position:absolute;left:70px;right:70px;top:190px;text-align:center;font-family:Outfit;font-weight:800;font-size:58px;line-height:1.18;text-shadow:0 4px 18px #000}}
.w{{opacity:.18;animation:palabra .18s ease-out both}} .w.k{{color:#F2A33A}}
@keyframes palabra{{from{{opacity:.18;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.pill{{position:absolute;left:0;right:0;display:flex;justify-content:center;font-family:Outfit;font-weight:800;font-size:44px;letter-spacing:.5px}}
.pill .pop{{display:inline-block;padding:20px 34px;border-radius:60px;box-shadow:0 10px 30px #0008;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
@keyframes pop{{from{{transform:scale(.4);opacity:0}}to{{transform:none;opacity:1}}}}
.gancho{{position:absolute;inset:0}}
.gtit{{position:absolute;left:60px;right:60px;top:560px;text-align:center;font-family:Outfit;font-weight:900;font-size:96px;line-height:1.02;letter-spacing:-2px;text-shadow:0 6px 30px #000}}
.gmono{{position:absolute;left:290px;top:860px;width:500px;height:640px}}
.tiemblaG{{animation:tiembla .11s linear 0s 40 both}}
.ley{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}}
.ley-card{{width:820px;background:#fff;color:#0D1117;border-radius:34px;padding:50px;box-shadow:0 30px 80px #000c;animation:subeCard .6s cubic-bezier(.2,1.3,.4,1) {e[5]['inicio']+0.6:.2f}s both;margin-top:260px}}
@keyframes subeCard{{from{{transform:translateY(500px)}}to{{transform:none}}}}
.ley-h{{background:#0D1117;color:#fff;display:inline-block;font-family:Outfit;font-weight:800;font-size:30px;padding:10px 20px;border-radius:12px;letter-spacing:1px}}
.ley-art{{font-family:Outfit;font-weight:900;font-size:90px;margin:20px 0 10px}}
.ley-card p{{font-size:42px;line-height:1.35;color:#374151}} .ley-card mark{{background:#FFE066;color:#0D1117;padding:0 6px;font-weight:800}}
.ley-tag{{display:inline-block;margin-top:30px;border:3px solid #0D1117;border-radius:40px;padding:10px 22px;font-family:Outfit;font-weight:800;font-size:28px}}
.tel{{position:absolute;inset:0;display:flex;justify-content:center;align-items:center}}
.tel-card{{width:760px;background:#fff;color:#0D1117;border-radius:50px;padding:60px 54px;border:14px solid #0D1117;outline:4px solid #333;box-shadow:0 30px 80px #000c;animation:subeCard .5s cubic-bezier(.2,1.3,.4,1) {e[6]['inicio']:.2f}s both;margin-top:200px}}
.tel-h{{font-family:Outfit;font-weight:800;font-size:32px;letter-spacing:2px;color:#6b7280;margin-bottom:30px}}
.chk{{font-family:Outfit;font-weight:800;font-size:46px;padding:24px 0;border-bottom:3px solid #eee;display:flex;gap:26px;align-items:center}}
.chk .x{{width:62px;height:62px;border-radius:16px;background:#E5484D;color:#fff;display:flex;align-items:center;justify-content:center;font-size:38px}}
.cta{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;padding-top:500px;background:#0D1117}}
.logo{{animation:pop .6s cubic-bezier(.2,1.6,.4,1) {e[7]['inicio']+0.1:.2f}s both}}
.cta-t{{font-family:Outfit;font-weight:900;font-size:84px;line-height:1.05;text-align:center;margin-top:50px;letter-spacing:-1px}}
.cta-band{{margin-top:60px;background:#F2A33A;color:#0D1117;font-family:Outfit;font-weight:800;font-size:52px;padding:34px 50px;border-radius:30px;text-align:center;animation:pop .5s cubic-bezier(.2,1.6,.4,1) {e[7]['inicio']+1.2:.2f}s both}}
.cta-band b{{font-weight:900}}
.cta-mail{{margin-top:34px;font-family:Outfit;font-weight:800;font-size:44px;color:#1FA9E8}}
.fuente{{position:absolute;bottom:430px;left:90px;right:90px;text-align:center;font-size:26px;color:#8b949e}}
"""

page = f'''<!doctype html><html><head><meta charset="utf-8"><link href="file:///tmp/bs/fonts/fonts.css" rel="stylesheet"><style>{CSS}</style></head><body>
<div class="grid"></div>
<div class="mundo-wrap"><div class="cam"><div class="shake"><svg width="1080" height="1000" viewBox="0 0 1080 1000">{"".join(w)}{"".join(gente_svg)}</svg></div></div></div>
{gancho}{"".join(pills)}{ley}{tel}{cta}{"".join(subs)}
<div class="handle"><i></i>@basesegura.cl</div>
</body></html>'''
open(f"{R}/reel.html", "w", encoding="utf-8").write(page)
print("ok", TOT)
