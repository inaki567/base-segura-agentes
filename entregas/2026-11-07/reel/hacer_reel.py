#!/usr/bin/env python3
# Reel 2026-11-07: "Golpe de calor en la pega" (DS 594 art. 98 bis) — estilo marca/ESTILO-REELS.md
# Uso: python3 hacer_reel.py entregas/2026-11-07/reel   (lee tiempos.json, escribe reel.html)
import json, sys, html, random
R = sys.argv[1]
T = json.load(open(f"{R}/tiempos.json", encoding="utf-8"))
E = T["escenas"]; TOT = T["total"]
LOGO = open("/tmp/bs/marca/logo.svg").read().replace('<svg ', '<svg width="200" height="200" ', 1)
random.seed(11)


def iso(x, y, z=0):
    return 540 + (x - y) * 52, 250 + (x + y) * 30 - z * 60


def poly(pts, fill, extra=""):
    p = " ".join(f"{a:.1f},{b:.1f}" for a, b in (iso(*q) for q in pts))
    return f'<polygon points="{p}" fill="{fill}" {extra}/>'


def linea(p, q, color, w=6, extra=""):
    a, b = iso(*p), iso(*q)
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def caja(x0, y0, z0, dx, dy, dz, top, left, right, extra=""):
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    return (f'<g {extra}>' +
            poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], left) +
            poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], right) +
            poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top) + '</g>')


def arbol(x, y, r=0.9):
    a = iso(x, y)
    return (f'<g><ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="26" ry="9" fill="#0006"/><rect x="{a[0]-5:.0f}" y="{a[1]-50:.0f}" width="10" height="50" fill="#6b4a2b"/>'
            f'<circle cx="{a[0]:.0f}" cy="{a[1]-70:.0f}" r="{r*40:.0f}" fill="#2f9e44"/><circle cx="{a[0]-10:.0f}" cy="{a[1]-80:.0f}" r="{r*18:.0f}" fill="#51cf66" opacity=".55"/></g>')


def cono(x, y):
    a = iso(x, y)
    return (f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><ellipse rx="20" ry="7" fill="#0006"/><rect x="-18" y="-6" width="36" height="8" rx="3" fill="#e8590c"/>'
            f'<path d="M-13 -4 L0 -46 L13 -4Z" fill="#FF8A3D"/><path d="M-9 -18 L9 -18 L7 -26 L-7 -26Z" fill="#fff"/></g>')


def pct(t): return max(0, min(100, t / TOT * 100))


# ---------- personajes tipo juguete ----------
def cara_svg(cara, cy=-146):
    if cara == "calor":
        ojos = (f'<path d="M-19 {cy-4} a6 6 0 1 1 6 6 a3 3 0 1 1 -3 -3" stroke="#111" stroke-width="3" fill="none"/>'
                f'<path d="M7 {cy-4} a6 6 0 1 1 6 6 a3 3 0 1 1 -3 -3" stroke="#111" stroke-width="3" fill="none"/>')
        boca = f'<path d="M-10 {cy+14} q5 -5 10 0 q5 5 10 0" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>'
        cejas = f'<path d="M-21 {cy-16} L-7 {cy-12} M21 {cy-16} L7 {cy-12}" stroke="#111" stroke-width="4" stroke-linecap="round"/>'
        extra = (f'<ellipse cx="-20" cy="{cy+6}" rx="8" ry="5" fill="#E5484D" opacity=".7"/><ellipse cx="20" cy="{cy+6}" rx="8" ry="5" fill="#E5484D" opacity=".7"/>'
                 f'<path class="gota" d="M30 {cy-14} q6 9 0 13 q-6 -4 0 -13Z" fill="#9fd0ff"/>')
        return ojos + cejas + boca + extra
    if cara == "alivio":
        return (f'<path d="M-19 {cy-2} q6 -7 12 0 M7 {cy-2} q6 -7 12 0" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>'
                f'<path d="M-10 {cy+12} Q0 {cy+22} 10 {cy+12}" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>')
    ojos = f'<circle cx="-13" cy="{cy-4}" r="5" fill="#111"/><circle cx="13" cy="{cy-4}" r="5" fill="#111"/>'
    boca = {'feliz': f'<path d="M-10 {cy+12} Q0 {cy+20} 10 {cy+12}" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>',
            'susto': f'<ellipse cx="0" cy="{cy+15}" rx="6" ry="8" fill="#111"/>',
            'duda': f'<path d="M-9 {cy+15} L9 {cy+12}" stroke="#111" stroke-width="4" stroke-linecap="round"/>'}[cara]
    cejas = {'susto': f'<path d="M-21 {cy-18} L-7 {cy-14} M21 {cy-18} L7 {cy-14}" stroke="#111" stroke-width="4" stroke-linecap="round"/>',
             'duda': f'<path d="M-21 {cy-17} L-7 {cy-17} M21 {cy-21} L7 {cy-15}" stroke="#111" stroke-width="4" stroke-linecap="round"/>'}.get(cara, '')
    return ojos + cejas + boca


def piel(cara):
    return "#F4A58C" if cara == "calor" else "#F2C9A0"


def mono(color="#7048e8", casco="#FFD43B", cara="feliz", escala=1.0, cola=False, bigote=False):
    pelo = '<circle cx="30" cy="-132" r="15" fill="#5c3b1e"/><path d="M-34 -152 Q-30 -178 0 -178 Q30 -178 34 -152" fill="#5c3b1e"/>' if cola else ''
    big = '<path d="M-16 -128 Q-8 -138 0 -131 Q8 -138 16 -128 Q8 -126 0 -129 Q-8 -126 -16 -128Z" fill="#4a3424"/>' if bigote else ''
    return f'''<g transform="scale({escala})">
<ellipse cx="0" cy="0" rx="34" ry="11" fill="#0006"/>
<g class="pierna p1"><rect x="-20" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<g class="pierna p2"><rect x="3" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<rect x="-26" y="-112" width="52" height="62" rx="20" fill="{color}"/>
<rect x="-26" y="-84" width="52" height="9" fill="#FFD43B"/>
<g class="brazos"><rect x="-38" y="-108" width="14" height="46" rx="7" fill="{color}"/><rect x="24" y="-108" width="14" height="46" rx="7" fill="{color}"/></g>
{pelo}<circle cx="0" cy="-146" r="34" fill="{piel(cara)}"/>
{cara_svg(cara)}{big}
<path d="M-34 -160 A34 32 0 0 1 34 -160 Z" fill="{casco}"/><rect x="-40" y="-164" width="80" height="9" rx="4.5" fill="{casco}"/>
</g>'''


def sentado(color="#3b5bdb", casco="#FFFFFF", cara="calor", escala=0.85, bigote=True):
    big = '<path d="M-20 -94 Q-12 -104 -4 -97 Q4 -104 12 -94 Q4 -92 -4 -95 Q-12 -92 -20 -94Z" fill="#4a3424"/>' if bigote else ''
    return f'''<g transform="scale({escala})"><ellipse cx="10" cy="0" rx="62" ry="13" fill="#0006"/>
<rect x="-10" y="-22" width="86" height="18" rx="9" fill="#1d2b4f"/><rect x="-10" y="-8" width="80" height="16" rx="8" fill="#1d2b4f"/>
<rect x="-30" y="-80" width="52" height="66" rx="20" fill="{color}"/><rect x="-30" y="-52" width="52" height="9" fill="#FFD43B"/>
<rect x="10" y="-66" width="56" height="14" rx="7" fill="{color}" transform="rotate(28 10 -66)"/>
<g transform="translate(-4,34)">{'<circle cx="0" cy="-146" r="32" fill="' + piel(cara) + '"/>'}{cara_svg(cara)}</g>{big}
<path d="M-36 -126 A32 30 0 0 1 28 -126 Z" fill="{casco}"/><rect x="-42" y="-130" width="76" height="8" rx="4" fill="{casco}"/></g>'''


# ---------- mundo: obra al sol ----------
w = []
w.append(poly([(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)], "#2a2622"))
w.append(poly([(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)], "url(#calorSuelo)"))
for i in range(1, 10):
    a, b = iso(i, 0), iso(i, 10); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0d" stroke-width="2"/>')
    a, b = iso(0, i), iso(10, i); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0d" stroke-width="2"/>')
# borde de la maqueta
w.append(poly([(0, 10, 0), (10, 10, 0), (10, 10, -0.4), (0, 10, -0.4)], "#1a1714"))
w.append(poly([(10, 0, 0), (10, 10, 0), (10, 10, -0.4), (10, 0, -0.4)], "#14110f"))
# galpón en construcción (Luis trabaja en el techo)
w.append(caja(1.0, 1.2, 0, 3.2, 2.6, 1.5, "#8d97a6", "#cfc6b8", "#a99f90"))
for k in range(8):  # calaminas
    xa = 1.0 + 0.4 * k + 0.2
    w.append(linea((xa, 1.2, 1.5), (xa, 3.8, 1.5), "#6c7686", 3))
w.append(poly([(1.5, 3.8, 0), (2.3, 3.8, 0), (2.3, 3.8, 1.05), (1.5, 3.8, 1.05)], "#3a2e25"))
w.append(poly([(2.8, 3.8, 0.5), (3.7, 3.8, 0.5), (3.7, 3.8, 1.1), (2.8, 3.8, 1.1)], "#1c2230"))
w.append(poly([(4.2, 1.6, 0.5), (4.2, 2.6, 0.5), (4.2, 2.6, 1.1), (4.2, 1.6, 1.1)], "#1c2230"))
# escalera apoyada
for yy in (4.25, 4.55):
    pass
w.append(linea((3.9, 4.3, 0), (3.9, 3.8, 1.6), "#FFC53D", 6))
w.append(linea((3.5, 4.3, 0), (3.5, 3.8, 1.6), "#FFC53D", 6))
for k in range(1, 6):
    f = k / 6
    w.append(linea((3.5, 4.3 - 0.5 * f, 1.6 * f), (3.9, 4.3 - 0.5 * f, 1.6 * f), "#FFC53D", 4))
# andamio
for (x, y) in [(4.6, 1.4), (5.6, 1.4), (4.6, 2.4), (5.6, 2.4)]:
    w.append(linea((x, y, 0), (x, y, 2.6), "#9aa4b2", 5))
for z in (1.3, 2.6):
    w.append(caja(4.55, 1.35, z, 1.1, 1.1, 0.1, "#c08a4b", "#9c6d39", "#80582d"))
w.append(linea((4.6, 2.4, 0), (5.6, 2.4, 1.3), "#9aa4b2", 3))
w.append(linea((5.6, 1.4, 1.3), (5.6, 2.4, 2.6), "#9aa4b2", 3))
a = iso(5.1, 1.9, 2.75)
w.append(f'<circle cx="{a[0]:.0f}" cy="{a[1]:.0f}" r="9" fill="#E5484D" class="baliza"/>')
# ladrillos y saco de cemento
w.append(caja(5.0, 3.4, 0, 0.9, 0.6, 0.4, "#d9480f", "#b8400e", "#9a360c"))
w.append(caja(5.1, 3.5, 0.4, 0.7, 0.4, 0.3, "#e8590c", "#b8400e", "#9a360c"))
w.append(caja(6.2, 3.2, 0, 0.6, 0.5, 0.35, "#ced4da", "#adb5bd", "#868e96"))
# termómetro gigante + reloj
a = iso(8.6, 1.4, 0)
w.append(f'''<g transform="translate({a[0]:.0f},{a[1]:.0f})"><ellipse rx="40" ry="12" fill="#0006"/><rect x="-4" y="-150" width="8" height="150" fill="#9aa4b2"/>
<rect x="-70" y="-330" width="140" height="190" rx="22" fill="#0D1117" stroke="#FFC53D" stroke-width="4"/>
<rect x="-44" y="-310" width="24" height="120" rx="12" fill="#fff"/><circle cx="-32" cy="-178" r="20" fill="#E5484D"/>
<rect class="mercurio" x="-38" y="-300" width="12" height="118" rx="6" fill="#E5484D"/>
<text x="26" y="-252" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="42" fill="#FF8A3D">33°</text>
<text x="26" y="-196" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="30" fill="#FFC53D">14:00</text></g>''')
# toldo con sombra, bidón y banca
TX0, TY0, TDX, TDY, TZ = 6.2, 5.0, 2.4, 1.8, 2.8
w.append(poly([(TX0 - 0.3, TY0 + 0.4, 0), (TX0 + TDX - 0.3, TY0 + 0.4, 0), (TX0 + TDX - 0.3, TY0 + TDY + 0.4, 0), (TX0 - 0.3, TY0 + TDY + 0.4, 0)], "#0c1a2b", 'opacity=".75"'))
for (x, y) in [(TX0, TY0), (TX0 + TDX, TY0), (TX0, TY0 + TDY), (TX0 + TDX, TY0 + TDY)]:
    w.append(linea((x, y, 0), (x, y, TZ), "#ced4da", 5))
w.append(poly([(TX0, TY0, TZ), (TX0 + TDX, TY0, TZ), (TX0 + TDX, TY0 + TDY, TZ), (TX0, TY0 + TDY, TZ)], "#1FA9E8"))
for k in range(4):
    xa = TX0 + 0.3 + k * 0.6
    w.append(poly([(xa, TY0, TZ), (xa + 0.3, TY0, TZ), (xa + 0.3, TY0 + TDY, TZ), (xa, TY0 + TDY, TZ)], "#ffffff", 'opacity=".85"'))
w.append(poly([(TX0, TY0 + TDY, TZ), (TX0 + TDX, TY0 + TDY, TZ), (TX0 + TDX, TY0 + TDY, TZ - 0.25), (TX0, TY0 + TDY, TZ - 0.25)], "#1677a8"))
a = iso(8.4, 5.2, 0)
w.append(f'''<g transform="translate({a[0]:.0f},{a[1]:.0f})"><ellipse rx="26" ry="9" fill="#0006"/><rect x="-22" y="-62" width="44" height="62" rx="10" fill="#1FA9E8"/>
<ellipse cx="0" cy="-62" rx="22" ry="7" fill="#74c0fc"/><rect x="-8" y="-74" width="16" height="12" rx="3" fill="#fff"/><rect x="-26" y="-30" width="10" height="6" fill="#ced4da"/>
<text x="0" y="-22" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="20" fill="#fff">H₂O</text></g>''')
w.append(caja(6.3, 5.3, 0.45, 1.2, 0.35, 0.12, "#c08a4b", "#9c6d39", "#80582d"))
w.append(linea((6.4, 5.5, 0), (6.4, 5.5, 0.45), "#80582d", 5)); w.append(linea((7.4, 5.5, 0), (7.4, 5.5, 0.45), "#80582d", 5))
a = iso(7.4, 5.0, TZ + 0.6)
w.append(f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><rect x="-80" y="-30" width="160" height="44" rx="10" fill="#25D366" stroke="#0D1117" stroke-width="3"/>'
         f'<text x="0" y="2" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="26" fill="#0D1117">ZONA SOMBRA</text></g>')
# conos y árboles
w.append(cono(5.6, 4.6)); w.append(cono(2.6, 5.4)); w.append(cono(9.2, 3.6))
w.append(arbol(9.2, 0.6, 0.9)); w.append(arbol(0.6, 5.6, 1.0)); w.append(arbol(0.9, 8.6, 0.8))

# ---------- tiempos de la historia ----------
e = E
t_sit = e[1]["inicio"] + 0.15            # Luis se sienta mareado en el techo (golpe)
t_vale = e[1]["inicio"] + 2.35           # "Vale lo nota"
t_walk0, t_walk1 = e[3]["inicio"] + 0.1, e[3]["inicio"] + 3.0
t_alivio = e[8]["inicio"]
ROOF = iso(2.7, 2.6, 1.5)
BASE = (3.2, 4.7); L_T = (7.0, 7.0); V_T = (8.2, 6.4)
V0 = (6.6, 4.3); V_B = (4.0, 4.6)


def tr(p): a = iso(*p); return f"translate({a[0]:.0f}px,{a[1]:.0f}px)"


luis1 = f'''<g transform="translate({ROOF[0]:.0f},{ROOF[1]:.0f})"><g class="luis1">
<g class="l-pie"><g class="mareo">{mono("#3b5bdb", "#FFFFFF", "calor", 0.85, bigote=True)}</g></g>
<g class="l-sit">{sentado(cara="calor")}<g class="estrellas"><text x="0" y="-150" font-size="34" text-anchor="middle">💫</text></g></g></g></g>'''
walk = [(0, BASE), (t_walk0, BASE), (t_walk1, L_T), (TOT, L_T)]
css_extra = []
css_extra.append("@keyframes luis2{" + " ".join(f"{pct(t):.2f}%{{transform:{tr(p)}}}" for t, p in walk) + "}")
luis2 = f'''<g class="luis2"><g class="l-walk"><g class="apoyado">{mono("#3b5bdb", "#FFFFFF", "calor", 0.85, bigote=True)}</g></g></g>'''
a = iso(*L_T)
luis3 = f'''<g transform="translate({a[0]:.0f},{a[1]:.0f})"><g class="luis3"><g transform="scale(-1,1)">
<g class="l-sit-calor">{sentado(cara="calor")}</g><g class="l-sit-ok">{sentado(cara="alivio")}</g></g>
<g class="pano"><rect x="-26" y="-106" width="44" height="16" rx="6" fill="#74c0fc" stroke="#fff" stroke-width="3"/><circle class="gotea" cx="-4" cy="-86" r="5" fill="#9fd0ff"/></g>
<g class="vaso"><rect x="22" y="-70" width="18" height="24" rx="4" fill="#9fd0ff" stroke="#fff" stroke-width="2"/></g></g></g>'''
vrun = [(0, V0), (t_vale + 0.5, V0), (t_vale + 2.2, V_B), (t_walk0, V_B), (t_walk1, (L_T[0] + 0.8, L_T[1] - 0.4)),
        (e[4]["inicio"] + 0.1, (L_T[0] + 0.8, L_T[1] - 0.4)), (e[4]["inicio"] + 0.7, V_T), (TOT, V_T)]
css_extra.append("@keyframes vale{" + " ".join(f"{pct(t):.2f}%{{transform:{tr(p)}}}" for t, p in vrun) + "}")
vale = f'''<g class="vale"><g class="v-cuerpo">{mono("#7048e8", "#FFD43B", "susto", 0.85, cola=True)}</g>
<g class="v-alerta"><rect x="-26" y="-226" width="52" height="56" rx="16" fill="#FFC53D"/><text x="0" y="-182" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="44" fill="#0D1117">!</text></g></g>'''
# compañero de fondo trabajando
a = iso(6.4, 0.8, 0)
fondo_mono = f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><g class="trabaja">{mono("#868e96", "#FFD43B", "feliz", 0.6)}</g></g>'


# ---------- cámara ----------
def foco(t, p, s):
    px, py = iso(*p)
    return (t, s, -s * (px - 540), -20 - s * (py - 520))


P_roof = (2.7, 2.6, 2.4); P_toldo = (7.4, 6.6, 1.2); P_wide = (5, 5, 0.8)
cam = [foco(0, P_roof, 1.25), foco(e[1]["inicio"] - 0.1, P_roof, 1.4), foco(e[1]["inicio"] + 0.3, P_roof, 1.8),
       foco(t_vale - 0.2, P_roof, 1.75), foco(t_vale + 0.6, (4.6, 3.6, 1.2), 1.3), foco(e[2]["inicio"] - 0.1, (3.6, 3.6, 1.4), 1.45),
       foco(e[3]["inicio"], (3.6, 4.0, 1.0), 1.35), foco(e[3]["inicio"] + 0.4, (3.8, 4.8, 0.9), 1.6),
       foco(t_walk1, P_toldo, 1.65), foco(e[4]["inicio"] + 0.6, P_toldo, 1.95), foco(e[5]["inicio"], P_toldo, 2.05),
       foco(e[7]["inicio"], P_wide, 0.95), foco(e[8]["inicio"] - 0.3, (5.5, 5.5, 0.8), 1.05),
       foco(e[8]["inicio"], P_toldo, 1.8), foco(e[9]["inicio"], P_toldo, 1.95), foco(TOT, P_toldo, 1.95)]
cam_kf = " ".join(f"{pct(t):.2f}%{{transform:translate({x:.0f}px,{y:.0f}px) scale({s})}}" for t, s, x, y in cam)

# ---------- subtítulos karaoke ----------
clave = {0: ["treinta", "tres", "grados,", "marea", "techo."], 1: ["rojo", "confundido.", "golpe", "calor.", "tres", "cosas,"],
         2: ["Uno:", "SAMU,", "ciento", "treinta", "uno."], 3: ["Dos:", "sombra,", "fresco."],
         4: ["Tres:", "agua", "fría.", "mutual."], 5: ["primer", "verano", "noventa", "ocho", "bis"],
         6: ["salud", "altas", "temperaturas."], 7: ["alertas", "evalúa", "calor", "plan", "mutual", "equipo."],
         8: ["agua", "fresca,", "pausas", "sombra", "nadie", "solo."], 9: ["calor?", "ayudamos", "base", "segura", "punto", "cl", "minuto."]}
subs = []
for i, ee in enumerate(E):
    ps = ee["palabras"]; trozos, cur = [], []
    for p in ps:
        largo = len(" ".join(q["p"] for q in cur + [p]))
        if cur and largo > 30:
            trozos.append(cur); cur = []
        cur.append(p)
        if p["p"][-1] in ".,:?" and len(" ".join(q["p"] for q in cur)) >= 14:
            trozos.append(cur); cur = []
    if cur: trozos.append(cur)
    fin_esc = ee["inicio"] + ee["dur"]
    for k, trz in enumerate(trozos):
        a0 = trz[0]["t"] - 0.05 if k else ee["inicio"]
        b0 = trozos[k + 1][0]["t"] - 0.05 if k + 1 < len(trozos) else fin_esc
        ws = "".join(f'<span class="w{" k" if p["p"] in clave.get(i, []) else ""}" style="animation-delay:{p["t"]:.2f}s">{html.escape(p["p"])}</span> ' for p in trz)
        subs.append(f'<div class="sub cut" style="--i:{a0:.2f}s;--d:{b0 - a0:.2f}s">{ws}</div>')


def pill(txt, bg, fg, t, d, top):
    return f'<div class="pill win" style="--i:{t:.2f}s;--d:{d:.2f}s;top:{top}px"><span class="pop" style="animation-delay:{t:.2f}s;background:{bg};color:{fg}">{txt}</span></div>'


def fin(i): return e[i]["inicio"] + e[i]["dur"]


def pal(i, palabra):
    for p in e[i]["palabras"]:
        if p["p"].lower().startswith(palabra.lower()): return p["t"]
    return e[i]["inicio"]


AM, NE, RO, AZ, VE = "#FFC53D", "#0D1117", "#E5484D", "#1FA9E8", "#25D366"
t_golpe = pal(1, "puede") - 0.1
t_3cosas = pal(1, "Son") - 0.1
pills = [
    pill("🥵 ROJO · CONFUNDIDO", AZ, NE, e[1]["inicio"] + 0.6, t_3cosas - e[1]["inicio"] - 0.6, 1220),
    pill("⚠️ POSIBLE GOLPE DE CALOR", RO, "#fff", t_golpe, fin(1) - t_golpe, 1330),
    pill("⏱ 3 COSAS · DE INMEDIATO", AM, NE, t_3cosas, fin(1) - t_3cosas, 1220),
    pill("📞 1 · LLAMA AL SAMU 131", AM, NE, e[2]["inicio"] + 0.2, e[2]["dur"] - 0.2, 1330),
    pill("⛱️ 2 · SOMBRA Y LUGAR FRESCO", AM, NE, e[3]["inicio"] + 0.2, e[3]["dur"] - 0.2, 1330),
    pill("💧 3 · ENFRIAR CON PAÑOS FRÍOS", AM, NE, e[4]["inicio"] + 0.2, e[4]["dur"] - 0.2, 1330),
    pill("✚ AVISA A TU MUTUAL O ISL", AZ, NE, pal(4, "avisa") - 0.15, fin(4) - pal(4, "avisa") + 0.15, 1220),
    pill("ℹ️ NUEVO · DS 594 · D.O. 16-01-2026", AZ, NE, e[5]["inicio"] + 0.3, e[5]["dur"] - 0.3, 1330),
    pill("📋 LO QUE TE PIDE A TI", AZ, NE, e[7]["inicio"] + 0.1, e[7]["dur"] - 0.1, 880),
    pill("☀️ A · REVISA LAS ALERTAS CADA DÍA", AM, NE, pal(7, "revisa") - 0.1, fin(7) - pal(7, "revisa") + 0.1, 1010),
    pill("🌡️ B · EVALÚA EL CALOR POR PUESTO", AM, NE, pal(7, "evalúa") - 0.1, fin(7) - pal(7, "evalúa") + 0.1, 1130),
    pill("📝 C · PLAN CON TU MUTUAL Y EQUIPO", AM, NE, pal(7, "arma") - 0.1, fin(7) - pal(7, "arma") + 0.1, 1250),
    pill("💧 AGUA · ⛱️ SOMBRA · 👥 NADIE SOLO", AM, NE, pal(8, "agua") - 0.1, fin(8) - pal(8, "agua") + 0.1, 1220),
    pill("✅ RECOMENDACIÓN DE LA AUTORIDAD", VE, NE, e[8]["inicio"] + 0.2, e[8]["dur"] - 0.2, 1330),
]

# gancho
gancho = f'''<div class="gancho win" style="--i:0s;--d:{e[1]['inicio']:.2f}s">
<div class="gtit">Golpe de <span style="color:#F2A33A">calor</span>:<br>¿qué haces primero?</div>
<svg viewBox="-200 -290 400 320" class="gmono"><g class="balancea">{mono("#3b5bdb", "#FFFFFF", "calor", 1.0, bigote=True)}</g>
<g transform="translate(130,-10)"><rect x="-22" y="-200" width="44" height="170" rx="22" fill="#fff"/><circle cx="0" cy="-30" r="34" fill="#E5484D"/>
<rect class="sube" x="-11" y="-185" width="22" height="160" rx="11" fill="#E5484D"/><text x="0" y="-215" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="44" fill="#FF8A3D">33°</text></g></svg></div>'''

# teléfono (escena 2)
tel = f'''<div class="tel win" style="--i:{e[2]['inicio']:.2f}s;--d:{e[2]['dur']+0.1:.2f}s"><div class="tel-card">
<div class="tel-isla"></div><div class="tel-l">Llamando…</div><div class="tel-av">✚</div><div class="tel-n">SAMU</div><div class="tel-num">131</div>
<div class="tel-s">Urgencias · Chile</div><div class="tel-b"><span class="rojo">✕</span><span class="verde">📞</span></div></div></div>'''

# oficina (escenas 5 y 6)
def iso_o(x, y, z=0):
    return 540 + (x - y) * 70, 330 + (x + y) * 40 - z * 80


def poly_o(pts, fill, extra=""):
    p = " ".join(f"{a:.1f},{b:.1f}" for a, b in (iso_o(*q) for q in pts))
    return f'<polygon points="{p}" fill="{fill}" {extra}/>'


def caja_o(x0, y0, z0, dx, dy, dz, top, left, right):
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    return (poly_o([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], left) +
            poly_o([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], right) +
            poly_o([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top))


o = []
o.append(poly_o([(0, 0, 0), (6, 0, 0), (6, 6, 0), (0, 6, 0)], "#1b2433"))
for i in range(1, 6):
    a, b = iso_o(i, 0), iso_o(i, 6); o.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff10" stroke-width="2"/>')
    a, b = iso_o(0, i), iso_o(6, i); o.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff10" stroke-width="2"/>')
o.append(poly_o([(0, 0, 0), (6, 0, 0), (6, 0, 3.6), (0, 0, 3.6)], "#273246"))
o.append(poly_o([(0, 0, 0), (0, 6, 0), (0, 6, 3.6), (0, 0, 3.6)], "#1f2838"))
o.append(poly_o([(2.2, 0, 1.4), (4.6, 0, 1.4), (4.6, 0, 3.0), (2.2, 0, 3.0)], "#FF8A3D"))  # ventana con sol
a = iso_o(3.9, 0, 2.5); o.append(f'<circle cx="{a[0]:.0f}" cy="{a[1]:.0f}" r="34" fill="#FFE066"/>')
o.append(poly_o([(3.38, 0, 1.4), (3.42, 0, 1.4), (3.42, 0, 3.0), (3.38, 0, 3.0)], "#0D1117"))
o.append(poly_o([(0, 1.4, 1.6), (0, 2.8, 1.6), (0, 2.8, 3.0), (0, 1.4, 3.0)], "#f1f3f5"))  # calendario
o.append(poly_o([(0, 1.4, 2.6), (0, 2.8, 2.6), (0, 2.8, 3.0), (0, 1.4, 3.0)], "#E5484D"))
o.append(caja_o(1.6, 2.4, 0, 2.8, 1.3, 1.0, "#c08a4b", "#9c6d39", "#80582d"))  # escritorio
o.append(caja_o(2.4, 2.6, 1.0, 1.1, 0.12, 0.8, "#343a40", "#212529", "#343a40"))  # monitor
o.append(poly_o([(2.48, 2.72, 1.08), (3.42, 2.72, 1.08), (3.42, 2.72, 1.72), (2.48, 2.72, 1.72)], "#1FA9E8"))
a = iso_o(2.95, 2.72, 1.4); o.append(f'<text x="{a[0]:.0f}" y="{a[1]+10:.0f}" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="30" fill="#fff">33°</text>')
o.append(caja_o(3.8, 2.7, 1.0, 0.5, 0.4, 0.5, "#e9ecef", "#ced4da", "#adb5bd"))
a = iso_o(3.3, 4.4, 0)
o.append(f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><g class="duenno">{mono("#868e96", "#FFFFFF", "duda", 1.15)}</g>'
         f'<text class="q" x="58" y="-210" font-family="Outfit" font-weight="900" font-size="70" fill="#F2A33A">?</text></g>')
oficina = f'''<div class="oficina win" style="--i:{e[5]['inicio']:.2f}s;--d:{e[7]['inicio']-e[5]['inicio']+0.15:.2f}s">
<div class="of-cam"><svg width="1080" height="900" viewBox="0 0 1080 900" overflow="visible">{"".join(o)}</svg></div>
<div class="burbuja"><b>¿Y yo qué tenía</b><br>que hacer <span style="color:#F2A33A">antes</span>?</div>
<div class="of-dim"></div></div>'''

ley = f'''<div class="ley win" style="--i:{e[6]['inicio']+0.2:.2f}s;--d:{e[6]['dur']-0.2:.2f}s"><div class="ley-card">
<div class="ley-h">DS 594 · CHILE</div><div class="ley-art">Art. 98 bis</div>
<p>"Los empleadores y empleadoras <mark>deberán tomar las medidas necesarias para proteger la salud</mark> de las personas trabajadoras frente a condiciones climáticas que puedan ocasionar las altas temperaturas y altas temperaturas extremas"</p>
<div class="ley-tag">🇨🇱 DS 594 · Chile · art. 98 bis</div><div class="ley-sub">Agregado por el Decreto 40/2025 Minsal · D.O. 16-01-2026</div></div></div>'''

t_fase2 = pal(9, "Te") - 0.2
minis = "".join(f'<div class="mini" style="animation-delay:{e[9]["inicio"]+0.4+k*0.25:.2f}s"><svg viewBox="-60 -240 120 250" width="150" height="312">{mono(c, h, "calor", 1.0)}</svg></div>'
                for k, (c, h) in enumerate([("#3b5bdb", "#FFFFFF"), ("#7048e8", "#FFD43B"), ("#868e96", "#FFD43B")]))
cta = f'''<div class="cta win" style="--i:{e[9]['inicio']:.2f}s;--d:{TOT-e[9]['inicio']:.2f}s"><div class="cta-in">
<div class="logo">{LOGO}</div>
<div class="fase1 win" style="--i:{e[9]['inicio']:.2f}s;--d:{t_fase2-e[9]['inicio']+0.3:.2f}s">
<div class="cta-t">¿Tu plan de emergencia<br>ya incluye el <span style="color:#F2A33A">calor</span>?</div>
<div class="minis">{minis}</div></div>
<div class="fase2">
<div class="cta-t2">Te ayudamos a sumarlo<br>y a coordinarlo con tu <span style="color:#F2A33A">mutual</span></div>
<div class="cta-band">Cotiza tu plan de emergencia<br>en <b>basesegura.cl</b></div>
<div class="cta-mail">contacto@basesegura.cl</div></div></div>
<div class="fuente">Fuente: DS 594 (Chile), art. 98 bis, agregado por Decreto 40/2025 Minsal (D.O. 16-01-2026) · Minsal, Prevención ante episodios de alta temperatura</div></div>'''

calor = "".join(f'<i style="left:{random.randint(20,1040)}px;animation-delay:-{random.random()*3:.2f}s;animation-duration:{2.4+random.random()*1.6:.2f}s;opacity:{0.15+random.random()*0.25:.2f}"></i>' for _ in range(26))

CSS = f"""
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;background:radial-gradient(circle at 70% 30%,#3a2618 0,#1a2233 40%,#0D1117 75%);font-family:Manrope;color:#fff;position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#ffffff07 2px,transparent 2px),linear-gradient(90deg,#ffffff07 2px,transparent 2px);background-size:90px 90px}}
.win{{opacity:0;animation:show var(--d) linear var(--i) both}}
@keyframes show{{0%{{opacity:0}}4%{{opacity:1}}96%{{opacity:1}}100%{{opacity:0}}}}
.cut{{opacity:0;animation:cut var(--d) linear var(--i) both}}
@keyframes cut{{0%{{opacity:0}}1%{{opacity:1}}99%{{opacity:1}}100%{{opacity:0}}}}
.handle{{position:absolute;top:150px;right:60px;font-family:Outfit;font-weight:800;font-size:28px;opacity:.85;display:flex;gap:10px;align-items:center;z-index:20}}
.handle i{{width:30px;height:30px;border:4px solid #fff;border-radius:9px;display:inline-block;position:relative}}
.handle i:after{{content:"";position:absolute;left:5px;top:5px;width:12px;height:12px;border:3px solid #fff;border-radius:50%;box-sizing:border-box}}
.mundo-wrap{{position:absolute;left:0;right:0;top:440px;height:1000px;animation:ocultaMundo {TOT}s linear both}}
@keyframes ocultaMundo{{0%{{opacity:.35}}{pct(e[1]['inicio']-0.2):.2f}%{{opacity:.35}}{pct(e[1]['inicio']+0.2):.2f}%{{opacity:1}}{pct(e[2]['inicio']):.2f}%{{opacity:1}}{pct(e[2]['inicio']+0.3):.2f}%{{opacity:.4}}{pct(e[3]['inicio']-0.1):.2f}%{{opacity:.4}}{pct(e[3]['inicio']+0.2):.2f}%{{opacity:1}}{pct(e[5]['inicio']):.2f}%{{opacity:1}}{pct(e[5]['inicio']+0.3):.2f}%{{opacity:0}}{pct(e[7]['inicio']-0.1):.2f}%{{opacity:0}}{pct(e[7]['inicio']+0.3):.2f}%{{opacity:.45}}{pct(e[8]['inicio']-0.1):.2f}%{{opacity:.45}}{pct(e[8]['inicio']+0.2):.2f}%{{opacity:1}}{pct(e[9]['inicio']):.2f}%{{opacity:1}}{pct(e[9]['inicio']+0.4):.2f}%{{opacity:0}}100%{{opacity:0}}}}
.cam{{width:1080px;height:1000px;transform-origin:540px 520px;animation:cam {TOT}s ease-in-out both}}
@keyframes cam{{{cam_kf}}}
.shake{{animation:tiembla .09s linear {t_sit:.2f}s 4 both}}
@keyframes tiembla{{0%{{transform:none}}25%{{transform:translate(12px,-7px)}}50%{{transform:translate(-11px,8px)}}75%{{transform:translate(8px,5px)}}100%{{transform:none}}}}
.sol{{position:absolute;right:40px;top:470px;width:240px;height:240px;animation:ocultaMundo {TOT}s linear both}}
.sol .rayos{{transform-origin:120px 120px;animation:gira 12s linear infinite}}
.sol .nucleo{{transform-origin:120px 120px;animation:pulsa 1.4s ease-in-out infinite alternate}}
@keyframes gira{{to{{transform:rotate(360deg)}}}} @keyframes pulsa{{to{{transform:scale(1.07)}}}}
.calor{{position:absolute;left:0;right:0;top:500px;height:1000px;overflow:hidden;pointer-events:none;animation:ocultaMundo {TOT}s linear both}}
.calor i{{position:absolute;bottom:-60px;width:6px;height:90px;border-radius:6px;background:linear-gradient(#FF8A3D00,#FFC53Daa,#FF8A3D00);animation-name:sube2;animation-timing-function:ease-in-out;animation-iteration-count:infinite}}
@keyframes sube2{{0%{{transform:translate(0,0)}}50%{{transform:translate(14px,-500px)}}100%{{transform:translate(-6px,-1000px);opacity:0}}}}
.mercurio{{transform-box:fill-box;transform-origin:50% 100%;animation:mercurio 3s ease-out .3s both}}
@keyframes mercurio{{from{{transform:scaleY(.25)}}to{{transform:scaleY(1)}}}}
.baliza{{animation:sir .5s steps(2) infinite}} @keyframes sir{{50%{{opacity:.2}}}}
.luis1{{animation:fuera .01s linear {t_walk0:.2f}s both}}
.l-pie{{animation:fuera .01s linear {t_sit:.2f}s both}}
.mareo{{transform-origin:0 0;animation:mareo .7s ease-in-out infinite alternate}}
@keyframes mareo{{from{{transform:rotate(-7deg)}}to{{transform:rotate(7deg) translateX(6px)}}}}
.l-sit{{opacity:0;animation:dentro .01s linear {t_sit:.2f}s both}}
.estrellas{{animation:orbita 1s linear infinite}} @keyframes orbita{{0%{{transform:translateX(-22px)}}50%{{transform:translateX(22px)}}100%{{transform:translateX(-22px)}}}}
.luis2{{opacity:0;animation:luis2 {TOT}s linear both, dentro .01s linear {t_walk0:.2f}s forwards, fuera .01s linear {t_walk1:.2f}s forwards}}
.apoyado{{transform:rotate(10deg)}}
.l-walk .p1{{animation:paso .35s ease-in-out infinite alternate}} .l-walk .p2{{animation:paso .35s ease-in-out infinite alternate-reverse}}
.luis3{{opacity:0;animation:dentro .01s linear {t_walk1:.2f}s both}}
.l-sit-ok{{opacity:0;animation:dentro .01s linear {t_alivio:.2f}s both}}
.l-sit-calor{{animation:fuera .01s linear {t_alivio:.2f}s both}}
.pano{{opacity:0;animation:pop .4s cubic-bezier(.2,1.6,.4,1) {pal(4, 'enfríalo'):.2f}s both}}
.gotea{{animation:gotea .8s ease-in infinite}} @keyframes gotea{{from{{transform:none;opacity:1}}to{{transform:translateY(40px);opacity:0}}}}
.vaso{{opacity:0;animation:pop .4s cubic-bezier(.2,1.6,.4,1) {pal(8, 'agua'):.2f}s both}}
.vale{{animation:vale {TOT}s linear both}}
.vale .p1{{animation:paso .25s ease-in-out {t_vale+0.5:.2f}s 7 alternate,paso .3s ease-in-out {t_walk0:.2f}s 10 alternate}}
.vale .p2{{animation:paso .25s ease-in-out {t_vale+0.5:.2f}s 7 alternate-reverse,paso .3s ease-in-out {t_walk0:.2f}s 10 alternate-reverse}}
.v-alerta{{opacity:0;animation:pop .35s cubic-bezier(.2,1.6,.4,1) {t_vale:.2f}s both, fuera .2s linear {t_vale+2.4:.2f}s forwards}}
.trabaja{{transform-origin:0 0;animation:balancea .5s ease-in-out infinite alternate}}
.gota{{animation:gotea 1s ease-in infinite}}
@keyframes fuera{{to{{opacity:0}}}} @keyframes dentro{{to{{opacity:1}}}} @keyframes aparece{{to{{opacity:1}}}}
.pierna{{transform-box:fill-box;transform-origin:50% 0}}
@keyframes paso{{from{{transform:rotate(-14deg)}}to{{transform:rotate(14deg)}}}}
{' '.join(css_extra)}
.techo{{position:absolute;left:0;right:0;top:0;height:470px;background:linear-gradient(#0D1117 0,#0D1117dd 55%,#0D111700 100%)}}
.sub{{position:absolute;left:70px;right:70px;top:230px;text-align:center;font-family:Outfit;font-weight:800;font-size:62px;line-height:1.15;text-shadow:0 4px 18px #000;z-index:10}}
.w{{opacity:.22;animation:palabra .18s ease-out both}} .w.k{{color:#F2A33A}}
@keyframes palabra{{from{{opacity:.22;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.pill{{position:absolute;left:0;right:0;display:flex;justify-content:center;font-family:Outfit;font-weight:800;font-size:44px;letter-spacing:.5px;z-index:6}}
.pill .pop{{display:inline-block;padding:20px 34px;border-radius:60px;box-shadow:0 10px 30px #0008;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
@keyframes pop{{from{{transform:scale(.4);opacity:0}}to{{transform:none;opacity:1}}}}
.gancho{{position:absolute;inset:0}}
.gtit{{position:absolute;left:50px;right:50px;top:500px;text-align:center;font-family:Outfit;font-weight:900;font-size:92px;line-height:1.04;letter-spacing:-2px;text-shadow:0 6px 30px #000;animation:pop .6s cubic-bezier(.2,1.6,.4,1) .1s both}}
.gmono{{position:absolute;left:140px;top:780px;width:800px;height:640px}}
.balancea{{transform-origin:0 0;animation:balancea .6s ease-in-out infinite alternate}}
@keyframes balancea{{from{{transform:rotate(-4deg)}}to{{transform:rotate(4deg) translateY(-6px)}}}}
.sube{{transform-box:fill-box;transform-origin:50% 100%;animation:mercurio 2.5s ease-out .2s both}}
.tel{{position:absolute;inset:0;display:flex;justify-content:center}}
.tel-card{{margin-top:560px;width:470px;height:700px;background:linear-gradient(#1c2333,#0b0f17);border:10px solid #2b3447;border-radius:64px;box-shadow:0 30px 80px #000c;display:flex;flex-direction:column;align-items:center;animation:subeCard .5s cubic-bezier(.2,1.3,.4,1) {e[2]['inicio']:.2f}s both}}
.tel-isla{{width:120px;height:30px;background:#000;border-radius:20px;margin-top:18px}}
.tel-l{{margin-top:40px;font-size:32px;color:#9aa4b2;font-weight:700}}
.tel-av{{margin-top:26px;width:130px;height:130px;border-radius:50%;background:#E5484D;display:flex;align-items:center;justify-content:center;font-size:76px;font-weight:900;animation:late .6s ease-in-out infinite alternate}}
.tel-n{{margin-top:22px;font-family:Outfit;font-weight:900;font-size:64px}} .tel-num{{font-family:Outfit;font-weight:900;font-size:110px;color:#FFC53D;line-height:1}}
.tel-s{{font-size:28px;color:#9aa4b2;margin-top:8px}}
.tel-b{{margin-top:auto;margin-bottom:46px;display:flex;gap:120px}} .tel-b span{{width:96px;height:96px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:44px}}
.tel-b .rojo{{background:#E5484D}} .tel-b .verde{{background:#25D366;animation:late .5s ease-in-out infinite alternate}}
@keyframes late{{to{{opacity:.55}}}}
.oficina{{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,#1a2233 0,#0D1117 75%)}}
.of-cam{{position:absolute;left:0;right:0;top:520px;height:900px;transform-origin:540px 450px;animation:ofcam {e[7]['inicio']-e[5]['inicio']:.2f}s ease-in-out {e[5]['inicio']:.2f}s both}}
@keyframes ofcam{{from{{transform:scale(.95) rotate(-1deg)}}to{{transform:scale(1.15) translateY(40px) rotate(1deg)}}}}
.duenno{{transform-origin:0 0;animation:balancea .9s ease-in-out infinite alternate}}
.q{{animation:late .4s ease-in-out infinite alternate}}
.burbuja{{position:absolute;left:150px;right:150px;top:460px;background:#fff;color:#0D1117;border-radius:40px;padding:30px 30px;text-align:center;font-family:Outfit;font-weight:800;font-size:52px;line-height:1.15;box-shadow:0 20px 50px #000a;animation:pop .5s cubic-bezier(.2,1.6,.4,1) {e[5]['inicio']+0.8:.2f}s both}}
.burbuja b{{font-weight:900}}
.of-dim{{position:absolute;inset:0;background:#0D1117;opacity:0;animation:dim .4s linear {e[6]['inicio']:.2f}s both}} @keyframes dim{{to{{opacity:.75}}}}
.ley{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:5}}
.ley-card{{width:860px;background:#fff;color:#0D1117;border-radius:34px;padding:46px 50px;box-shadow:0 30px 80px #000c;animation:subeCard .6s cubic-bezier(.2,1.3,.4,1) {e[6]['inicio']+0.2:.2f}s both;margin-top:80px}}
@keyframes subeCard{{from{{transform:translateY(700px)}}to{{transform:none}}}}
.ley-h{{background:#0D1117;color:#fff;display:inline-block;font-family:Outfit;font-weight:800;font-size:30px;padding:10px 20px;border-radius:12px;letter-spacing:1px}}
.ley-art{{font-family:Outfit;font-weight:900;font-size:86px;margin:14px 0 8px}}
.ley-card p{{font-size:38px;line-height:1.36;color:#374151}} .ley-card mark{{background:#FFE066;color:#0D1117;padding:0 6px;font-weight:800}}
.ley-tag{{display:inline-block;margin-top:26px;border:3px solid #0D1117;border-radius:40px;padding:10px 22px;font-family:Outfit;font-weight:800;font-size:28px}}
.ley-sub{{margin-top:12px;font-size:24px;color:#6b7280;font-weight:700}}
.cta{{position:absolute;inset:0;background:#0D1117;z-index:8}}
.cta-in{{position:absolute;left:0;right:0;top:420px;display:flex;flex-direction:column;align-items:center;animation:zoomLento {TOT-e[9]['inicio']:.2f}s linear {e[9]['inicio']:.2f}s both}}
@keyframes zoomLento{{from{{transform:scale(.97)}}to{{transform:scale(1.04)}}}}
.logo{{animation:pop .6s cubic-bezier(.2,1.6,.4,1) {e[9]['inicio']+0.1:.2f}s both}}
.fase1{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center}}
.cta-t{{font-family:Outfit;font-weight:900;font-size:76px;line-height:1.06;text-align:center;letter-spacing:-1px}}
.minis{{display:flex;gap:40px;margin-top:30px}} .mini{{opacity:0;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
.fase2{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center;opacity:0;animation:aparece .4s ease-out {t_fase2:.2f}s both}}
.cta-t2{{font-family:Outfit;font-weight:900;font-size:60px;line-height:1.12;text-align:center}}
.cta-band{{margin-top:46px;background:#F2A33A;color:#0D1117;font-family:Outfit;font-weight:800;font-size:50px;line-height:1.2;padding:32px 46px;border-radius:30px;text-align:center;animation:pop .5s cubic-bezier(.2,1.6,.4,1) {pal(9, 'Entra')-0.2:.2f}s both}}
.cta-band b{{font-weight:900}}
.cta-mail{{margin-top:34px;font-family:Outfit;font-weight:800;font-size:46px;color:#1FA9E8}}
.fuente{{position:absolute;bottom:420px;left:90px;right:90px;text-align:center;font-size:26px;line-height:1.4;color:#8b949e}}
"""

sol = '''<svg class="sol" viewBox="0 0 240 240"><circle cx="120" cy="120" r="110" fill="#FFC53D" opacity=".12"/><g class="rayos">''' + "".join(
    f'<rect x="114" y="8" width="12" height="34" rx="6" fill="#FFC53D" transform="rotate({k*30} 120 120)"/>' for k in range(12)) + \
    '''</g><g class="nucleo"><circle cx="120" cy="120" r="58" fill="#FFD43B"/><circle cx="120" cy="120" r="44" fill="#FFE066"/></g></svg>'''

page = f'''<!doctype html><html><head><meta charset="utf-8"><link href="file:///tmp/bs/fonts/fonts.css" rel="stylesheet"><style>{CSS}</style></head><body>
<div class="grid"></div>
{sol}
<div class="mundo-wrap"><div class="cam"><div class="shake"><svg width="1080" height="1000" viewBox="0 0 1080 1000" overflow="visible">
<defs><radialGradient id="calorSuelo" cx="50%" cy="40%" r="60%"><stop offset="0" stop-color="#FF8A3D" stop-opacity=".22"/><stop offset="1" stop-color="#FF8A3D" stop-opacity="0"/></radialGradient></defs>
{"".join(w)}{fondo_mono}{luis1}{vale}{luis2}{luis3}</svg></div></div></div>
<div class="calor">{calor}</div>
<div class="techo"></div>
{gancho}{tel}{oficina}{ley}{"".join(pills)}{cta}{"".join(subs)}
<div class="handle"><i></i>@basesegura.cl</div>
</body></html>'''
open(f"{R}/reel.html", "w", encoding="utf-8").write(page)
print("ok", TOT)
