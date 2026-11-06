#!/usr/bin/env python3
# Reel 2026-11-06: "Caída bajando de la micro = accidente de trayecto" — estilo marca/ESTILO-REELS.md
import json, sys, html, random
R = sys.argv[1]
T = json.load(open(f"{R}/tiempos.json", encoding="utf-8"))
E = T["escenas"]; TOT = T["total"]
LOGO = open("/tmp/bs/marca/logo.svg").read().replace('<svg ', '<svg width="200" height="200" ', 1)
random.seed(7)

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

def ventanas(x0, y0, dx, dy, dz, prob=.6):
    out = []
    x1, y1 = x0 + dx, y0 + dy
    for j in range(int(dz / 0.9)):
        za, zb = 0.5 + j * 0.9, 0.5 + j * 0.9 + 0.5
        if zb > dz - 0.2: break
        for i in range(int(dx / 0.7)):
            xa = x0 + 0.25 + i * 0.7; xb = xa + 0.35
            c = "#FFD98A" if random.random() < prob else "#2b3447"
            out.append(poly([(xa, y1, za), (xb, y1, za), (xb, y1, zb), (xa, y1, zb)], c))
        for i in range(int(dy / 0.7)):
            ya = y0 + 0.25 + i * 0.7; yb = ya + 0.35
            c = "#E8B868" if random.random() < prob else "#232b3c"
            out.append(poly([(x1, ya, za), (x1, yb, za), (x1, yb, zb), (x1, ya, zb)], c))
    return "".join(out)

def edificio(x0, y0, dx, dy, dz, techo="#3a4660", prob=.6):
    return caja(x0, y0, 0, dx, dy, dz, techo, "#2a3347", "#20283a") + ventanas(x0, y0, dx, dy, dz, prob)

def letrero(x, y, z, txt, bg, fg="#fff", w=None, extra=""):
    a = iso(x, y, z); w = w or (len(txt) * 17 + 40)
    return (f'<g {extra} transform="translate({a[0]:.0f},{a[1]:.0f})"><line x1="0" y1="0" x2="0" y2="-22" stroke="#9aa4b2" stroke-width="4"/>'
            f'<rect x="{-w/2:.0f}" y="-66" width="{w:.0f}" height="46" rx="10" fill="{bg}" stroke="#0D1117" stroke-width="3"/>'
            f'<text x="0" y="-34" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="26" fill="{fg}">{txt}</text></g>')

def arbol(x, y, r=0.9):
    a = iso(x, y)
    return (f'<g><ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="26" ry="9" fill="#0006"/><rect x="{a[0]-5:.0f}" y="{a[1]-50:.0f}" width="10" height="50" fill="#6b4a2b"/>'
            f'<circle cx="{a[0]:.0f}" cy="{a[1]-70:.0f}" r="{r*40:.0f}" fill="#2f9e44"/><circle cx="{a[0]-10:.0f}" cy="{a[1]-80:.0f}" r="{r*18:.0f}" fill="#51cf66" opacity=".55"/></g>')

def farol(x, y):
    a = iso(x, y)
    return (f'<g><ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="70" ry="26" fill="#FFD98A" opacity=".16"/><rect x="{a[0]-3:.0f}" y="{a[1]-170:.0f}" width="6" height="170" fill="#5d6878"/>'
            f'<rect x="{a[0]-3:.0f}" y="{a[1]-172:.0f}" width="34" height="6" fill="#5d6878"/><circle cx="{a[0]+30:.0f}" cy="{a[1]-164:.0f}" r="9" fill="#FFE8A8"/>'
            f'<circle cx="{a[0]+30:.0f}" cy="{a[1]-164:.0f}" r="30" fill="#FFE8A8" opacity=".18"/></g>')

def pct(t): return max(0, min(100, t / TOT * 100))

# ---------- mundo: calle de noche con lluvia ----------
w = []
w.append(poly([(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)], "#18202e"))
for i in range(1, 10):
    a, b = iso(i, 0), iso(i, 10); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0c" stroke-width="2"/>')
    a, b = iso(0, i), iso(10, i); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0c" stroke-width="2"/>')
# veredas y calle (calle a lo largo de x, y 4.4..6.0)
w.append(poly([(0, 3.6, 0), (10, 3.6, 0), (10, 4.4, 0), (0, 4.4, 0)], "#3a4253"))
w.append(poly([(0, 6.0, 0), (10, 6.0, 0), (10, 7.0, 0), (0, 7.0, 0)], "#3a4253"))
w.append(poly([(0, 4.4, 0), (10, 4.4, 0), (10, 6.0, 0), (0, 6.0, 0)], "#11161f"))
for k in range(10):
    w.append(poly([(k + .15, 5.16, 0), (k + .7, 5.16, 0), (k + .7, 5.24, 0), (k + .15, 5.24, 0)], "#FFC53D"))
# pozas de agua
for (x, y, r) in [(5.6, 6.5, 1), (2.2, 6.4, .7), (7.8, 4.0, .8), (4.0, 5.6, .6)]:
    a = iso(x, y); w.append(f'<ellipse class="poza" cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="{48*r:.0f}" ry="{16*r:.0f}" fill="#6fb6ff33" stroke="#9fd0ff55" stroke-width="2"/>')
# lado del fondo: mutual (izq), edificios, trabajo (der)
w.append(edificio(0.4, 0.6, 2.2, 2.4, 3.6, "#c92a2a", .5))
w.append(letrero(1.5, 1.8, 3.9, "✚ MUTUAL / ISL", "#ffffff", "#c92a2a", 230))
w.append(edificio(3.4, 0.8, 1.6, 1.8, 5.2, "#3a4660", .65))
w.append(edificio(5.4, 1.2, 1.2, 1.6, 2.6, "#5c7cfa", .5))
w.append(edificio(7.1, 0.4, 2.3, 2.6, 4.4, "#F2A33A", .7))
w.append(letrero(8.2, 1.7, 4.7, "TRABAJO", "#F2A33A", "#0D1117", 170))
w.append(arbol(3.0, 3.2, .8)); w.append(arbol(6.6, 3.3, .9))
w.append(farol(2.0, 3.9)); w.append(farol(6.2, 3.9))

# ruta directa (escena 5) y desvío
def ruta_d(pts):
    return "M" + " L".join(f"{iso(x, y)[0]:.0f} {iso(x, y)[1]:.0f}" for x, y in pts)
RUTA = [(1.9, 7.6), (1.9, 5.2), (8.0, 5.2), (8.0, 3.2)]
DESV = [(6.6, 5.2), (6.6, 6.8), (9.0, 6.8), (9.0, 7.3)]
ruta_svg = (f'<path class="ruta" d="{ruta_d(RUTA)}" fill="none" stroke="#25D366" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" pathLength="100"/>'
            f'<path class="desv" d="{ruta_d(DESV)}" fill="none" stroke="#FF8A3D" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="4 3" pathLength="100"/>')
xa = iso(9.3, 7.8, 2.4)
desv_x = f'<g transform="translate({xa[0]:.0f},{xa[1]:.0f})"><g class="desvx"><circle r="40" fill="#E5484D" stroke="#fff" stroke-width="6"/><path d="M-16 -16 L16 16 M16 -16 L-16 16" stroke="#fff" stroke-width="10" stroke-linecap="round"/></g></g>'

# micro (llega y se detiene en el paradero, luego se va)
bx, by = 3.0, 4.6
micro = (caja(bx, by, 0.15, 3.6, 1.1, 2.6, "#dfe5ee", "#c8d1de", "#aab5c5") +
         poly([(bx, by + 1.1, 0.75), (bx + 3.6, by + 1.1, 0.75), (bx + 3.6, by + 1.1, 1.0), (bx, by + 1.1, 1.0)], "#1FA9E8"))
for k in range(5):
    xa_, xb_ = bx + 0.2 + k * 0.62, bx + 0.2 + k * 0.62 + 0.48
    if k == 3: continue
    micro += poly([(xa_, by + 1.1, 1.4), (xb_, by + 1.1, 1.4), (xb_, by + 1.1, 2.4), (xa_, by + 1.1, 2.4)], "#9fd0ff")
micro += poly([(bx + 2.08, by + 1.1, 0.25), (bx + 2.62, by + 1.1, 0.25), (bx + 2.62, by + 1.1, 2.4), (bx + 2.08, by + 1.1, 2.4)], "#FFD98A", 'class="puerta"')
micro += poly([(bx + 3.6, by + 0.1, 1.3), (bx + 3.6, by + 1.0, 1.3), (bx + 3.6, by + 1.0, 2.4), (bx + 3.6, by + 0.1, 2.4)], "#9fd0ff")
micro += poly([(bx + 3.6, by + 0.15, 0.4), (bx + 3.6, by + 0.35, 0.4), (bx + 3.6, by + 0.35, 0.6), (bx + 3.6, by + 0.15, 0.6)], "#FFF3BF")
micro += poly([(bx + 3.6, by + 0.75, 0.4), (bx + 3.6, by + 0.95, 0.4), (bx + 3.6, by + 0.95, 0.6), (bx + 3.6, by + 0.75, 0.6)], "#FFF3BF")
for xw in (bx + 0.7, bx + 3.0):
    a = iso(xw, by + 1.1, 0.15); micro += f'<ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="22" ry="22" fill="#111"/><circle cx="{a[0]:.0f}" cy="{a[1]:.0f}" r="9" fill="#868e96"/>'
a = iso(bx + 3.4, by + 0.5, 2.75)
micro += f'<rect x="{a[0]-40:.0f}" y="{a[1]-16:.0f}" width="80" height="26" rx="6" fill="#111"/><text x="{a[0]:.0f}" y="{a[1]+4:.0f}" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="20" fill="#FFC53D">210</text>'
w.append(f'<g class="micro">{micro}</g>')

# auto de Carabineros (escena 4)
cx0 = 6.4
car = caja(cx0, 4.55, 0.15, 1.8, 0.8, 0.7, "#e9ecef", "#1b6b3a", "#155a30")
car += caja(cx0 + 0.5, 4.6, 0.85, 0.9, 0.7, 0.4, "#9fd0ff", "#e9ecef", "#cfd6de")
car += poly([(cx0, 5.35, 0.4), (cx0 + 1.8, 5.35, 0.4), (cx0 + 1.8, 5.35, 0.55), (cx0, 5.35, 0.55)], "#ffffff")
a = iso(cx0 + 0.95, 4.95, 1.3)
car += f'<rect class="sirena1" x="{a[0]-22:.0f}" y="{a[1]-10:.0f}" width="22" height="12" rx="4" fill="#1FA9E8"/><rect class="sirena2" x="{a[0]:.0f}" y="{a[1]-10:.0f}" width="22" height="12" rx="4" fill="#E5484D"/>'
w.append(f'<g class="carab">{car}</g>')

# paradero
w.append(caja(3.0, 6.85, 0, 1.7, 0.08, 2.6, "#5d6878", "#9fd0ff40", "#9fd0ff30"))
w.append(caja(2.95, 6.85, 0, 0.08, 0.1, 2.6, "#5d6878", "#5d6878", "#4a5463"))
w.append(caja(4.65, 6.85, 0, 0.08, 0.1, 2.6, "#5d6878", "#5d6878", "#4a5463"))
w.append(caja(2.9, 6.2, 2.6, 1.9, 0.8, 0.14, "#1FA9E8", "#1677a8", "#126490"))
w.append(caja(3.2, 6.6, 0.6, 1.3, 0.25, 0.1, "#868e96", "#5d6878", "#4a5463"))
a = iso(2.75, 6.25, 0)
w.append(f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><rect x="-3" y="-200" width="6" height="200" fill="#9aa4b2"/><rect x="-36" y="-250" width="72" height="56" rx="10" fill="#1FA9E8" stroke="#fff" stroke-width="3"/>'
         f'<text x="0" y="-212" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="30" fill="#fff">PARE</text></g>')
# reloj del paradero
a = iso(3.2, 6.3, 2.75)
w.append(f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><rect x="-62" y="-60" width="124" height="54" rx="10" fill="#0D1117" stroke="#FFC53D" stroke-width="3"/>'
         f'<text x="0" y="-21" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="36" fill="#FFC53D">7:40</text></g>')

def mono(color="#7048e8", casco="#FFD43B", cara="feliz", escala=1.0, cola=False):
    ojos = '<circle cx="-13" cy="-150" r="5" fill="#111"/><circle cx="13" cy="-150" r="5" fill="#111"/>'
    boca = {'feliz': '<path d="M-10 -134 Q0 -126 10 -134" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>',
            'susto': '<ellipse cx="0" cy="-131" rx="6" ry="8" fill="#111"/>',
            'duda': '<path d="M-9 -131 L9 -134" stroke="#111" stroke-width="4" stroke-linecap="round"/>'}[cara]
    cejas = {'susto': '<path d="M-21 -164 L-7 -160 M21 -164 L7 -160" stroke="#111" stroke-width="4" stroke-linecap="round"/>',
             'duda': '<path d="M-21 -163 L-7 -163 M21 -167 L7 -161" stroke="#111" stroke-width="4" stroke-linecap="round"/>'}.get(cara, '')
    pelo = '<circle cx="30" cy="-132" r="15" fill="#5c3b1e"/><path d="M-34 -152 Q-30 -178 0 -178 Q30 -178 34 -152" fill="#5c3b1e"/>' if cola else ''
    return f'''<g transform="scale({escala})">
<ellipse cx="0" cy="0" rx="34" ry="11" fill="#0006"/>
<g class="pierna p1"><rect x="-20" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<g class="pierna p2"><rect x="3" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<rect x="-26" y="-112" width="52" height="62" rx="20" fill="{color}"/>
<rect x="-26" y="-84" width="52" height="9" fill="#FFD43B"/>
<g class="brazos"><rect x="-38" y="-108" width="14" height="46" rx="7" fill="{color}"/><rect x="24" y="-108" width="14" height="46" rx="7" fill="{color}"/></g>
{pelo}<circle cx="0" cy="-146" r="34" fill="#F2C9A0"/>
{ojos}{cejas}{boca}
<path d="M-34 -160 A34 32 0 0 1 34 -160 Z" fill="{casco}"/><rect x="-40" y="-164" width="80" height="9" rx="4.5" fill="{casco}"/>
</g>'''

def sentada(color="#7048e8", casco="#FFD43B"):
    return f'''<g><ellipse cx="10" cy="0" rx="62" ry="13" fill="#0006"/>
<rect x="-10" y="-22" width="86" height="18" rx="9" fill="#1d2b4f"/><rect x="-10" y="-8" width="80" height="16" rx="8" fill="#1d2b4f"/>
<circle class="duele" cx="72" cy="-2" r="16" fill="#E5484D" opacity=".75"/>
<rect x="-30" y="-80" width="52" height="66" rx="20" fill="{color}"/><rect x="-30" y="-52" width="52" height="9" fill="#FFD43B"/>
<rect x="10" y="-66" width="56" height="14" rx="7" fill="{color}" transform="rotate(28 10 -66)"/>
<circle cx="30" cy="-100" r="15" fill="#5c3b1e"/><circle cx="-4" cy="-112" r="32" fill="#F2C9A0"/>
<path d="M-18 -118 l8 5 l-8 5 M10 -118 l-8 5 l8 5" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M-14 -96 q4 -6 8 0 q4 6 8 0" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M-36 -126 A32 30 0 0 1 28 -126 Z" fill="{casco}"/><rect x="-42" y="-130" width="76" height="8" rx="4" fill="{casco}"/>
<g class="dolor" fill="#FFC53D"><path d="M96 -40 l6 14 l14 2 l-11 9 l3 14 l-12 -8 l-12 8 l3 -14 l-11 -9 l14 -2z"/></g></g>'''

# Camila: posición por tiempo
t_bajada, t_caida = 3.5, E[1]["inicio"] + 0.2
t_para, t_va = E[3]["inicio"] + 0.2, E[3]["inicio"] + 4.2
cam_ruta = [(0, (5.35, 5.75)), (t_bajada, (5.35, 5.75)), (t_caida, (5.55, 6.5)), (t_para + 0.4, (5.55, 6.5)),
            (E[3]["inicio"] + 2.0, (2.7, 5.6)), (t_va, (2.0, 3.3))]
frames = [f"{pct(t):.2f}%{{transform:translate({iso(x, y)[0]:.0f}px,{iso(x, y)[1]:.0f}px)}}" for t, (x, y) in cam_ruta]
frames.append(f"100%{{transform:translate({iso(2.0, 3.3)[0]:.0f}px,{iso(2.0, 3.3)[1]:.0f}px)}}")
css_extra = [f"@keyframes camila{{{' '.join(frames)}}} .camila{{animation:camila {TOT}s linear 0s both}}"]
camila = f'''<g class="camila"><g class="aparece">
<g class="de-pie1"><g class="cae-giro">{mono("#7048e8", "#FFD43B", "susto", 0.85, True)}</g></g>
<g class="sentada">{sentada()}</g>
<g class="de-pie2"><g class="cojea">{mono("#7048e8", "#FFD43B", "duda", 0.85, True)}</g></g></g></g>'''

# testigos (escena 4)
def testigo(x, y, color, casco, d):
    a = iso(x, y)
    return (f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><g class="testigo" style="animation-delay:{d:.2f}s">{mono(color, casco, "feliz", .75)}'
            f'<g transform="translate(36,-170)"><rect x="0" y="-44" width="70" height="52" rx="16" fill="#fff"/><path d="M8 4 L0 20 L22 6Z" fill="#fff"/>'
            f'<text x="35" y="-6" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="38" fill="#0D1117">👀</text></g></g></g>')
testigos = testigo(3.5, 6.55, "#3b5bdb", "#FFFFFF", E[4]["inicio"] + 1.8) + testigo(4.3, 6.6, "#868e96", "#FFD43B", E[4]["inicio"] + 2.2)

# lado cercano: casa (izq) y tienda (der)
cerca = []
cerca.append(caja(1.0, 7.6, 0, 1.8, 1.6, 1.8, "#e8590c", "#d9c7a8", "#bfae90"))
cerca.append(poly([(1.0, 9.2, 1.8), (2.8, 9.2, 1.8), (1.9, 9.2, 2.8)], "#c2410c"))
cerca.append(poly([(1.6, 9.2, 0), (2.1, 9.2, 0), (2.1, 9.2, 1.1), (1.6, 9.2, 1.1)], "#6b4a2b"))
cerca.append(poly([(2.8, 7.9, 0.8), (2.8, 8.6, 0.8), (2.8, 8.6, 1.4), (2.8, 7.9, 1.4)], "#FFD98A"))
cerca.append(letrero(1.9, 8.4, 3.0, "CASA", "#25D366", "#0D1117", 110))
cerca.append(caja(8.5, 7.3, 0, 1.5, 1.2, 1.6, "#7048e8", "#3d2f6b", "#2f2554"))
cerca.append(poly([(8.7, 8.5, 0.3), (9.8, 8.5, 0.3), (9.8, 8.5, 1.2), (8.7, 8.5, 1.2)], "#FFD98A"))
cerca.append(letrero(9.25, 7.9, 1.8, "TIENDA", "#7048e8", "#fff", 140))
cerca.append(arbol(4.6, 8.6, 1.0)); cerca.append(farol(0.8, 6.9))

# cámara
def foco(t, px, py, s):
    return (t, s, -s * (px - 540), -20 - s * (py - 520))
P_par = iso(5.0, 6.2, 1.2); P_mut = iso(2.0, 3.0, 1.6); P_mapa = iso(5, 5, 0.6)
cam = [foco(0, *P_par, 1.15), foco(E[0]["inicio"] + 4.2, *P_par, 1.25), foco(E[1]["inicio"], *P_par, 1.55),
       foco(E[1]["inicio"] + 3.0, *iso(5.4, 6.4, 1.0), 1.75), foco(E[2]["inicio"], *iso(5.4, 6.4, 1.0), 1.6),
       foco(E[2]["inicio"] + 4.0, *P_par, 1.3), foco(E[3]["inicio"] + 0.6, *iso(4, 5, 1), 1.2),
       foco(E[3]["inicio"] + 4.2, *P_mut, 1.45), foco(E[4]["inicio"], *P_mut, 1.5),
       foco(E[4]["inicio"] + 0.9, *iso(5.0, 6.0, 1.0), 1.45), foco(E[5]["inicio"] - 0.2, *iso(5.4, 5.8, 1.0), 1.6),
       foco(E[5]["inicio"] + 0.9, *P_mapa, 0.98), foco(E[5]["inicio"] + 4.0, *iso(6, 6.3, 0.6), 1.12),
       foco(E[6]["inicio"] + 1, *P_mapa, 0.95), foco(TOT, *P_mapa, 0.9)]
cam_kf = " ".join(f"{pct(t):.2f}%{{transform:translate({x:.0f}px,{y:.0f}px) scale({s})}}" for t, s, x, y in cam)

# subtítulos karaoke: trozos cortos (1-2 líneas)
clave = {0: ["micro,", "¿Es", "accidente", "trabajo?"], 1: ["Camila", "llueve,", "tuerce", "tobillo.", "cubre?"],
         2: ["trayecto,", "acreditarlo.", "tres", "cosas."], 3: ["Uno:", "mutual", "Instituto", "Seguridad", "Laboral.", "hora"],
         4: ["Dos:", "constancia", "Carabineros,", "testigos."], 5: ["Tres:", "directo.", "desviaste", "común."],
         6: ["Ley", "dieciséis", "mil", "setecientos", "cuarenta", "cuatro,", "trayecto", "directo,", "ida", "regreso."],
         7: ["pyme:", "mutual", "capacitación", "base", "segura", "punto", "cl", "minuto."]}
subs = []
for i, e in enumerate(E):
    ps = e["palabras"]; trozos, cur = [], []
    for p in ps:
        largo = len(" ".join(q["p"] for q in cur + [p]))
        if cur and largo > 30:
            trozos.append(cur); cur = []
        cur.append(p)
        if p["p"][-1] in ".,:?" and len(" ".join(q["p"] for q in cur)) >= 14:
            trozos.append(cur); cur = []
    if cur: trozos.append(cur)
    fin_esc = e["inicio"] + e["dur"]
    for k, tr in enumerate(trozos):
        a = tr[0]["t"] - 0.05 if k else e["inicio"]
        b = trozos[k + 1][0]["t"] - 0.05 if k + 1 < len(trozos) else fin_esc
        ws = "".join(f'<span class="w{" k" if p["p"] in clave.get(i, []) else ""}" style="animation-delay:{p["t"]:.2f}s">{html.escape(p["p"])}</span> ' for p in tr)
        subs.append(f'<div class="sub cut" style="--i:{a:.2f}s;--d:{b - a:.2f}s">{ws}</div>')

def pill(txt, bg, fg, t, d, top, extra=""):
    return f'<div class="pill win" style="--i:{t:.2f}s;--d:{d:.2f}s;top:{top}px;{extra}"><span class="pop" style="animation-delay:{t:.2f}s;background:{bg};color:{fg}">{txt}</span></div>'

e = E
fin_mundo = e[7]["inicio"]
AM, NE = "#FFC53D", "#0D1117"
pills = [
    pill("⏱ 7:40 · CAMINO A LA PEGA", "#1FA9E8", NE, e[1]["inicio"] + 0.6, e[1]["dur"] - 0.6, 1220),
    pill("⚠️ CAÍDA EN EL TRAYECTO", "#E5484D", "#fff", e[1]["inicio"] + 0.3, e[1]["dur"] - 0.3, 1330),
    pill("✅ SÍ: ACCIDENTE DE TRAYECTO", "#25D366", NE, e[2]["inicio"] + 0.2, 4.6, 1220),
    pill("⏱ 3 COSAS · DE INMEDIATO", "#25D366", NE, e[2]["inicio"] + 4.7, e[2]["dur"] - 4.7, 1330),
    pill("🏥 1 · MUTUAL O ISL DE TU EMPRESA", AM, NE, e[3]["inicio"] + 0.3, e[3]["dur"] - 0.3, 1330),
    pill("📄 2 · PARTE O TESTIGOS", AM, NE, e[4]["inicio"] + 0.3, e[4]["dur"] - 0.3, 1330),
    pill("🗺️ 3 · SIN DESVÍOS PERSONALES", AM, NE, e[5]["inicio"] + 0.3, e[5]["dur"] - 0.3, 1330),
    pill("⚠️ DESVÍO = ACCIDENTE COMÚN", "#E5484D", "#fff", e[5]["inicio"] + 3.0, e[5]["dur"] - 3.0, 1220),
]
gancho = f'''<div class="gancho win" style="--i:0s;--d:{e[1]['inicio']:.2f}s">
<div class="gtit">¿Caída en la micro <span style="color:#F2A33A">=</span><br>accidente del trabajo?</div>
<svg viewBox="-110 -250 220 280" class="gmono"><g class="balancea">{mono("#7048e8", "#FFD43B", "susto", 1.0, True)}</g></svg></div>'''
form = f'''<div class="form win" style="--i:{e[3]['inicio']+4.0:.2f}s;--d:{e[3]['dur']-4.0:.2f}s"><div class="form-card">
<div class="form-h">✚ DENUNCIA DE ACCIDENTE</div>
<div class="campo" style="animation-delay:{e[3]['inicio']+4.4:.2f}s"><span>¿Qué pasó?</span><b>Caída al bajar de la micro</b></div>
<div class="campo" style="animation-delay:{e[3]['inicio']+5.3:.2f}s"><span>¿A qué hora?</span><b>7:40 · camino al trabajo</b></div>
<div class="campo" style="animation-delay:{e[3]['inicio']+6.0:.2f}s"><span>¿Por dónde ibas?</span><b>Casa → trabajo, directo</b></div></div></div>'''
tk = e[6]["tarjeta"] if "tarjeta" in e[6] else None
ley = f'''<div class="ley win" style="--i:{e[6]['inicio']+0.4:.2f}s;--d:{e[6]['dur']-0.4:.2f}s"><div class="ley-card">
<div class="ley-h">LEY 16.744 · CHILE</div><div class="ley-art">Art. 5°<small> inciso 2°</small></div>
<p>"Son también accidentes del trabajo los ocurridos en el <mark>trayecto directo, de ida o regreso</mark>, entre la habitación y el lugar del trabajo"</p>
<div class="ley-tag">🇨🇱 Ley 16.744 · Chile · art. 5° inc. 2°</div></div></div>'''
t_entra = e[7]["inicio"] + 6.6
duda = "".join(f'<div class="mini" style="animation-delay:{e[7]["inicio"]+0.4+k*0.25:.2f}s"><svg viewBox="-60 -240 120 250" width="150" height="312">{mono(c, h, "duda", 1.0)}'
               f'<text x="0" y="-200" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="56" fill="#F2A33A" class="q">?</text></svg></div>'
               for k, (c, h) in enumerate([("#3b5bdb", "#FFFFFF"), ("#7048e8", "#FFD43B"), ("#868e96", "#FFD43B")]))
cta = f'''<div class="cta win" style="--i:{e[7]['inicio']:.2f}s;--d:{TOT-e[7]['inicio']:.2f}s"><div class="cta-in">
<div class="logo">{LOGO}</div>
<div class="fase1 win" style="--i:{e[7]['inicio']:.2f}s;--d:{t_entra-e[7]['inicio']:.2f}s">
<div class="cta-t">¿Tu equipo sabe<br>a qué <span style="color:#F2A33A">mutual</span> ir?</div>
<div class="minis">{duda}</div></div>
<div class="fase2">
<div class="cta-t2">Se enseña en la capacitación<br>del <span style="color:#F2A33A">DS 44</span></div>
<div class="cta-band">Cotiza tu capacitación en <b>basesegura.cl</b></div>
<div class="cta-mail">contacto@basesegura.cl</div></div></div>
<div class="fuente">Fuente: Ley 16.744 (Chile), art. 5° inc. 2° · DS 44, art. 16 n.° 4 · SUSESO, Compendio Ley 16.744</div></div>'''
lluvia = "".join(f'<i style="left:{random.randint(0,1080)}px;animation-delay:-{random.random()*0.8:.2f}s;animation-duration:{0.55+random.random()*0.35:.2f}s;opacity:{0.25+random.random()*0.4:.2f}"></i>' for _ in range(70))

CSS = f"""
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;background:radial-gradient(circle at 50% 45%,#1a2233 0,#0D1117 70%);font-family:Manrope;color:#fff;position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#ffffff07 2px,transparent 2px),linear-gradient(90deg,#ffffff07 2px,transparent 2px);background-size:90px 90px}}
.win{{opacity:0;animation:show var(--d) linear var(--i) both}}
@keyframes show{{0%{{opacity:0}}4%{{opacity:1}}96%{{opacity:1}}100%{{opacity:0}}}}
.cut{{opacity:0;animation:cut var(--d) linear var(--i) both}}
@keyframes cut{{0%{{opacity:0}}1%{{opacity:1}}99%{{opacity:1}}100%{{opacity:0}}}}
.handle{{position:absolute;top:150px;right:60px;font-family:Outfit;font-weight:800;font-size:28px;opacity:.85;display:flex;gap:10px;align-items:center;z-index:20}}
.handle i{{width:30px;height:30px;border:4px solid #fff;border-radius:9px;display:inline-block;position:relative}}
.handle i:after{{content:"";position:absolute;left:5px;top:5px;width:12px;height:12px;border:3px solid #fff;border-radius:50%;box-sizing:border-box}}
.mundo-wrap{{position:absolute;left:0;right:0;top:440px;height:1000px;animation:ocultaMundo {TOT}s linear both}}
@keyframes ocultaMundo{{0%{{opacity:.35}}{pct(e[1]['inicio']-0.2):.2f}%{{opacity:.35}}{pct(e[1]['inicio']+0.2):.2f}%{{opacity:1}}{pct(e[6]['inicio']+0.1):.2f}%{{opacity:1}}{pct(e[6]['inicio']+0.8):.2f}%{{opacity:.3}}{pct(fin_mundo-0.2):.2f}%{{opacity:.3}}{pct(fin_mundo+0.3):.2f}%{{opacity:0}}100%{{opacity:0}}}}
.cam{{width:1080px;height:1000px;transform-origin:540px 520px;animation:cam {TOT}s ease-in-out both}}
@keyframes cam{{{cam_kf}}}
.shake{{animation:tiembla .09s linear {e[1]['inicio']+0.2:.2f}s 4 both}}
@keyframes tiembla{{0%{{transform:none}}25%{{transform:translate(12px,-7px)}}50%{{transform:translate(-11px,8px)}}75%{{transform:translate(8px,5px)}}100%{{transform:none}}}}
.micro{{animation:micro {TOT}s linear both}}
@keyframes micro{{0%{{transform:translate(-416px,-240px)}}{pct(2.9):.2f}%{{transform:none;animation-timing-function:ease-in}}{pct(e[3]['inicio']):.2f}%{{transform:none}}{pct(e[3]['inicio']+2.5):.2f}%{{transform:translate(780px,450px);opacity:1}}{pct(e[3]['inicio']+2.6):.2f}%{{opacity:0}}100%{{opacity:0;transform:translate(780px,450px)}}}}
.puerta{{animation:abre {TOT}s linear both}}
@keyframes abre{{0%{{fill:#9fd0ff}}{pct(3.1):.2f}%{{fill:#9fd0ff}}{pct(3.2):.2f}%{{fill:#FFD98A}}100%{{fill:#FFD98A}}}}
.carab{{opacity:0;animation:carab {TOT}s linear both}}
@keyframes carab{{0%{{opacity:0;transform:translate(416px,240px)}}{pct(e[4]['inicio']):.2f}%{{opacity:0;transform:translate(416px,240px)}}{pct(e[4]['inicio']+0.1):.2f}%{{opacity:1;transform:translate(416px,240px);animation-timing-function:ease-out}}{pct(e[4]['inicio']+1.6):.2f}%{{opacity:1;transform:none}}{pct(e[6]['inicio']):.2f}%{{opacity:1;transform:none}}100%{{opacity:1}}}}
.sirena1{{animation:sir .4s steps(2) infinite}} .sirena2{{animation:sir .4s steps(2) infinite reverse}}
@keyframes sir{{50%{{opacity:.15}}}}
.testigo{{opacity:0;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
.ruta{{stroke-dasharray:100;stroke-dashoffset:100;animation:dibuja 1.6s ease-out {e[5]['inicio']+0.8:.2f}s both}}
.desv{{opacity:0;animation:aparece .4s ease-out {e[5]['inicio']+2.6:.2f}s both}}
@keyframes dibuja{{to{{stroke-dashoffset:0}}}} @keyframes aparece{{to{{opacity:1}}}}
.desvx{{opacity:0;animation:pop .45s cubic-bezier(.2,1.6,.4,1) {e[5]['inicio']+3.0:.2f}s both}}
.camila{{}}
.aparece{{opacity:0;animation:aparece .3s ease-out {t_bajada:.2f}s both, fuera .4s ease-in {E[4]['inicio']-0.2:.2f}s forwards}}
.de-pie1{{animation:fuera .01s linear {t_caida+0.35:.2f}s both}}
.cae-giro{{transform-origin:0 0;animation:caeGiro .35s cubic-bezier(.5,0,1,.6) {t_caida:.2f}s both}}
@keyframes caeGiro{{to{{transform:rotate(-80deg) translate(10px,10px)}}}}
.sentada{{opacity:0;animation:dentro .01s linear {t_caida+0.35:.2f}s both, fuera .01s linear {t_para:.2f}s forwards}}
.de-pie2{{opacity:0;animation:dentro .01s linear {t_para:.2f}s both}}
.cojea{{animation:cojea .5s ease-in-out infinite alternate}}
@keyframes cojea{{from{{transform:rotate(-6deg)}}to{{transform:rotate(4deg) translateY(-6px)}}}}
.de-pie2 .p1{{animation:paso .3s ease-in-out infinite alternate}} .de-pie2 .p2{{animation:paso .3s ease-in-out infinite alternate-reverse}}
.de-pie1 .p1{{animation:paso .3s ease-in-out {t_bajada:.2f}s 5 alternate}} .de-pie1 .p2{{animation:paso .3s ease-in-out {t_bajada:.2f}s 5 alternate-reverse}}
.duele{{animation:late .5s ease-in-out infinite alternate}} @keyframes late{{to{{opacity:.25}}}}
.dolor{{animation:late .3s steps(2) infinite alternate}}
@keyframes fuera{{to{{opacity:0}}}} @keyframes dentro{{to{{opacity:1}}}}
.pierna{{transform-box:fill-box;transform-origin:50% 0}}
@keyframes paso{{from{{transform:rotate(-14deg)}}to{{transform:rotate(14deg)}}}}
.poza{{animation:brilla 1.2s ease-in-out infinite alternate}} @keyframes brilla{{to{{opacity:.55}}}}
{' '.join(css_extra)}
.lluvia{{position:absolute;inset:0;overflow:hidden;pointer-events:none;animation:lluviaOff {TOT}s linear both}}
@keyframes lluviaOff{{0%,{pct(e[6]['inicio']):.2f}%{{opacity:1}}{pct(e[6]['inicio']+0.6):.2f}%,100%{{opacity:0}}}}
.lluvia i{{position:absolute;top:-80px;width:3px;height:56px;border-radius:3px;background:linear-gradient(#9fd0ff00,#9fd0ffcc);transform:rotate(12deg);animation-name:cae2;animation-timing-function:linear;animation-iteration-count:infinite}}
@keyframes cae2{{to{{transform:translate(-400px,2000px) rotate(12deg)}}}}
.techo{{position:absolute;left:0;right:0;top:0;height:470px;background:linear-gradient(#0D1117 0,#0D1117dd 55%,#0D111700 100%)}}
.sub{{position:absolute;left:70px;right:70px;top:230px;text-align:center;font-family:Outfit;font-weight:800;font-size:62px;line-height:1.15;text-shadow:0 4px 18px #000;z-index:10}}
.w{{opacity:.22;animation:palabra .18s ease-out both}} .w.k{{color:#F2A33A}}
@keyframes palabra{{from{{opacity:.22;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.pill{{position:absolute;left:0;right:0;display:flex;justify-content:center;font-family:Outfit;font-weight:800;font-size:44px;letter-spacing:.5px}}
.pill .pop{{display:inline-block;padding:20px 34px;border-radius:60px;box-shadow:0 10px 30px #0008;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
@keyframes pop{{from{{transform:scale(.4);opacity:0}}to{{transform:none;opacity:1}}}}
.gancho{{position:absolute;inset:0}}
.gtit{{position:absolute;left:50px;right:50px;top:520px;text-align:center;font-family:Outfit;font-weight:900;font-size:88px;line-height:1.04;letter-spacing:-2px;text-shadow:0 6px 30px #000;animation:pop .6s cubic-bezier(.2,1.6,.4,1) .1s both}}
.gmono{{position:absolute;left:300px;top:850px;width:480px;height:620px}}
.balancea{{transform-origin:0 0;animation:balancea .6s ease-in-out infinite alternate}}
@keyframes balancea{{from{{transform:rotate(-3deg)}}to{{transform:rotate(3deg) translateY(-6px)}}}}
.form{{position:absolute;inset:0;display:flex;justify-content:center}}
.form-card{{margin-top:610px;width:820px;height:560px;background:#fff;color:#0D1117;border-radius:34px;padding:44px 50px;box-shadow:0 30px 80px #000c;animation:subeCard .5s cubic-bezier(.2,1.3,.4,1) {e[3]['inicio']+4.0:.2f}s both}}
.form-h{{font-family:Outfit;font-weight:900;font-size:44px;color:#c92a2a;margin-bottom:18px}}
.campo{{border-bottom:3px solid #e5e7eb;padding:18px 0;opacity:0;animation:aparece .3s ease-out both}}
.campo span{{display:block;font-size:28px;color:#6b7280;font-weight:700}} .campo b{{font-family:Outfit;font-weight:800;font-size:42px}}
.ley{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}}
.ley-card{{width:840px;background:#fff;color:#0D1117;border-radius:34px;padding:50px;box-shadow:0 30px 80px #000c;animation:subeCard .6s cubic-bezier(.2,1.3,.4,1) {e[6]['inicio']+0.4:.2f}s both;margin-top:200px}}
@keyframes subeCard{{from{{transform:translateY(600px)}}to{{transform:none}}}}
.ley-h{{background:#0D1117;color:#fff;display:inline-block;font-family:Outfit;font-weight:800;font-size:30px;padding:10px 20px;border-radius:12px;letter-spacing:1px}}
.ley-art{{font-family:Outfit;font-weight:900;font-size:86px;margin:18px 0 10px}} .ley-art small{{font-size:44px;color:#6b7280}}
.ley-card p{{font-size:42px;line-height:1.38;color:#374151}} .ley-card mark{{background:#FFE066;color:#0D1117;padding:0 6px;font-weight:800}}
.ley-tag{{display:inline-block;margin-top:30px;border:3px solid #0D1117;border-radius:40px;padding:10px 22px;font-family:Outfit;font-weight:800;font-size:28px}}
.cta{{position:absolute;inset:0;background:#0D1117}}
.cta-in{{position:absolute;left:0;right:0;top:420px;display:flex;flex-direction:column;align-items:center;animation:zoomLento {TOT-e[7]['inicio']:.2f}s linear {e[7]['inicio']:.2f}s both}}
@keyframes zoomLento{{from{{transform:scale(.97)}}to{{transform:scale(1.04)}}}}
.logo{{animation:pop .6s cubic-bezier(.2,1.6,.4,1) {e[7]['inicio']+0.1:.2f}s both}}
.fase1{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center}}
.cta-t{{font-family:Outfit;font-weight:900;font-size:80px;line-height:1.05;text-align:center;letter-spacing:-1px}}
.minis{{display:flex;gap:40px;margin-top:30px}} .mini{{opacity:0;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
.q{{animation:late .4s ease-in-out infinite alternate}}
.fase2{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center;opacity:0;animation:aparece .4s ease-out {t_entra-0.9:.2f}s both}}
.cta-t2{{font-family:Outfit;font-weight:900;font-size:62px;line-height:1.1;text-align:center}}
.cta-band{{margin-top:50px;background:#F2A33A;color:#0D1117;font-family:Outfit;font-weight:800;font-size:50px;padding:34px 46px;border-radius:30px;text-align:center;animation:pop .5s cubic-bezier(.2,1.6,.4,1) {t_entra-0.4:.2f}s both}}
.cta-band b{{font-weight:900}}
.cta-mail{{margin-top:34px;font-family:Outfit;font-weight:800;font-size:46px;color:#1FA9E8}}
.fuente{{position:absolute;bottom:420px;left:90px;right:90px;text-align:center;font-size:26px;line-height:1.4;color:#8b949e}}
"""

page = f'''<!doctype html><html><head><meta charset="utf-8"><link href="file:///tmp/bs/fonts/fonts.css" rel="stylesheet"><style>{CSS}</style></head><body>
<div class="grid"></div>
<div class="mundo-wrap"><div class="cam"><div class="shake"><svg width="1080" height="1000" viewBox="0 0 1080 1000" overflow="visible">{"".join(w)}{ruta_svg}{testigos}{camila}{"".join(cerca)}{desv_x}</svg></div></div></div>
<div class="lluvia">{lluvia}</div>
<div class="techo"></div>
{gancho}{"".join(pills)}{form}{ley}{cta}{"".join(subs)}
<div class="handle"><i></i>@basesegura.cl</div>
</body></html>'''
open(f"{R}/reel.html", "w", encoding="utf-8").write(page)
print("ok", TOT)
