#!/usr/bin/env python3
# Reel 2026-11-10: "Se cayó de más de 1,80 m = accidente grave" (Ley 16.744, art. 76) — estilo marca/ESTILO-REELS.md
# Uso: python3 hacer_reel.py entregas/2026-11-10/reel   (lee tiempos.json, escribe reel.html)
import json, sys, html, random
R = sys.argv[1]
T = json.load(open(f"{R}/tiempos.json", encoding="utf-8"))
E = T["escenas"]; TOT = T["total"]
LOGO = open("/tmp/bs/marca/logo.svg").read().replace('<svg ', '<svg width="200" height="200" ', 1)
random.seed(10)


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
    return (f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><ellipse rx="{40*r:.0f}" ry="{14*r:.0f}" fill="#0006"/>'
            f'<rect x="-7" y="{-70*r:.0f}" width="14" height="{70*r:.0f}" fill="#6b4f2a"/>'
            f'<circle cy="{-110*r:.0f}" r="{52*r:.0f}" fill="#2f9e44"/><circle cx="{-14*r:.0f}" cy="{-124*r:.0f}" r="{24*r:.0f}" fill="#40c057" opacity=".7"/></g>')


def cono(x, y):
    a = iso(x, y)
    return (f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><ellipse rx="20" ry="7" fill="#0006"/><rect x="-18" y="-6" width="36" height="8" rx="3" fill="#e8590c"/>'
            f'<path d="M-13 -4 L0 -46 L13 -4Z" fill="#FF8A3D"/><path d="M-9 -18 L9 -18 L7 -26 L-7 -26Z" fill="#fff"/></g>')


def farol(x, y):
    a = iso(x, y)
    return (f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><ellipse rx="18" ry="6" fill="#0006"/><rect x="-4" y="-190" width="8" height="190" fill="#495057"/>'
            f'<rect x="-4" y="-190" width="46" height="8" fill="#495057"/><ellipse cx="40" cy="-180" rx="16" ry="7" fill="#FFE066"/>'
            f'<ellipse cx="40" cy="0" rx="90" ry="30" fill="#FFE066" opacity=".07"/></g>')


def pct(t): return max(0, min(100, t / TOT * 100))


# ---------- personajes tipo juguete ----------
def cara_svg(cara, cy=-146):
    if cara == "dolor":
        return (f'<path d="M-20 {cy-9} L-8 {cy-3} L-20 {cy+3} M20 {cy-9} L8 {cy-3} L20 {cy+3}" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M-11 {cy+16} q5.5 -6 11 0 q5.5 6 11 0" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>')
    ojos = f'<circle cx="-13" cy="{cy-4}" r="5" fill="#111"/><circle cx="13" cy="{cy-4}" r="5" fill="#111"/>'
    boca = {'feliz': f'<path d="M-10 {cy+12} Q0 {cy+20} 10 {cy+12}" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>',
            'susto': f'<ellipse cx="0" cy="{cy+15}" rx="6" ry="8" fill="#111"/>',
            'preocupa': f'<path d="M-10 {cy+17} Q0 {cy+9} 10 {cy+17}" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>',
            'duda': f'<path d="M-9 {cy+15} L9 {cy+12}" stroke="#111" stroke-width="4" stroke-linecap="round"/>'}[cara]
    cejas = {'susto': f'<path d="M-21 {cy-18} L-7 {cy-14} M21 {cy-18} L7 {cy-14}" stroke="#111" stroke-width="4" stroke-linecap="round"/>',
             'preocupa': f'<path d="M-21 {cy-14} L-7 {cy-19} M21 {cy-14} L7 {cy-19}" stroke="#111" stroke-width="4" stroke-linecap="round"/>',
             'duda': f'<path d="M-21 {cy-17} L-7 {cy-17} M21 {cy-21} L7 {cy-15}" stroke="#111" stroke-width="4" stroke-linecap="round"/>'}.get(cara, '')
    extra = f'<path class="gota" d="M30 {cy-14} q6 9 0 13 q-6 -4 0 -13Z" fill="#9fd0ff"/>' if cara == "preocupa" else ""
    return ojos + cejas + boca + extra


def cabeza(cara, casco, pelo="", bigote=False):
    big = '<path d="M-16 -128 Q-8 -138 0 -131 Q8 -138 16 -128 Q8 -126 0 -129 Q-8 -126 -16 -128Z" fill="#4a3424"/>' if bigote else ''
    return (f'{pelo}<circle cx="0" cy="-146" r="34" fill="#F2C9A0"/>{cara_svg(cara)}{big}'
            f'<path d="M-34 -160 A34 32 0 0 1 34 -160 Z" fill="{casco}"/><rect x="-40" y="-164" width="80" height="9" rx="4.5" fill="{casco}"/>')


COLA = '<circle cx="30" cy="-132" r="15" fill="#5c3b1e"/><path d="M-34 -152 Q-30 -178 0 -178 Q30 -178 34 -152" fill="#5c3b1e"/>'


def mono(color="#3b5bdb", casco="#FFD43B", cara="feliz", escala=1.0, cola=False, bigote=False, brazo="normal", sombra=True, extra=""):
    pelo = COLA if cola else ''
    if brazo == "arriba":
        brazos = (f'<rect x="-38" y="-108" width="14" height="46" rx="7" fill="{color}"/>'
                  f'<g transform="rotate(200 31 -102)"><rect x="24" y="-108" width="14" height="50" rx="7" fill="{color}"/><circle cx="31" cy="-58" r="8" fill="#F2C9A0"/></g>')
    elif brazo == "cabeza":  # manos a la cabeza (preocupado)
        brazos = (f'<g transform="rotate(150 -31 -102)"><rect x="-38" y="-108" width="14" height="48" rx="7" fill="{color}"/><circle cx="-31" cy="-60" r="8" fill="#F2C9A0"/></g>'
                  f'<g transform="rotate(-150 31 -102)"><rect x="24" y="-108" width="14" height="48" rx="7" fill="{color}"/><circle cx="31" cy="-60" r="8" fill="#F2C9A0"/></g>')
    elif brazo == "sujeta":
        brazos = (f'<g transform="rotate(-150 -31 -102)"><rect x="-38" y="-108" width="14" height="50" rx="7" fill="{color}"/><circle cx="-31" cy="-58" r="8" fill="#F2C9A0"/></g>'
                  f'<rect x="24" y="-108" width="14" height="46" rx="7" fill="{color}"/>')
    else:
        brazos = f'<rect x="-38" y="-108" width="14" height="46" rx="7" fill="{color}"/><rect x="24" y="-108" width="14" height="46" rx="7" fill="{color}"/>'
    sb = '<ellipse cx="0" cy="0" rx="34" ry="11" fill="#0006"/>' if sombra else ''
    return f'''<g transform="scale({escala})">{sb}
<g class="pierna p1"><rect x="-20" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<g class="pierna p2"><rect x="3" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<rect x="-26" y="-112" width="52" height="62" rx="20" fill="{color}"/>
<rect x="-26" y="-84" width="52" height="9" fill="#FFD43B"/>
<g class="brazos">{brazos}</g>
{cabeza(cara, casco, pelo, bigote)}{extra}
</g>'''


def agachado_tel(color, casco, escala=0.85):
    # compañero agachado junto al maestro, sin moverlo, hablando por teléfono
    return f'''<g transform="scale({escala})">
<ellipse cx="0" cy="0" rx="36" ry="11" fill="#0006"/>
<path d="M-18 -46 L-26 -24 L-18 0" stroke="#1d2b4f" stroke-width="17" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M10 -46 L20 -24 L12 0" stroke="#1d2b4f" stroke-width="17" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<g transform="translate(0,12)"><rect x="-26" y="-112" width="52" height="62" rx="20" fill="{color}"/><rect x="-26" y="-84" width="52" height="9" fill="#FFD43B"/>
<g transform="rotate(35 -31 -102)"><rect x="-38" y="-108" width="14" height="50" rx="7" fill="{color}"/></g>
<g transform="rotate(-160 31 -102)"><rect x="24" y="-108" width="14" height="44" rx="7" fill="{color}"/></g>
{cabeza("preocupa", casco, COLA)}
<rect x="30" y="-170" width="16" height="30" rx="4" fill="#0D1117" stroke="#1FA9E8" stroke-width="3"/>
<g class="ondas"><path d="M54 -170 q8 8 0 16 M62 -176 q14 14 0 28" stroke="#1FA9E8" stroke-width="4" fill="none" stroke-linecap="round"/></g></g></g>'''


# ---------- mundo: local comercial de noche con escalera ----------
w = []
w.append(poly([(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)], "#1b2230"))
for i in range(1, 10):
    a, b = iso(i, 0), iso(i, 10); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0d" stroke-width="2"/>')
    a, b = iso(0, i), iso(10, i); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0d" stroke-width="2"/>')
# vereda y calle al frente con línea amarilla
w.append(poly([(0, 7.6, 0), (10, 7.6, 0), (10, 8.2, 0), (0, 8.2, 0)], "#2a3242"))
w.append(poly([(0, 8.2, 0), (10, 8.2, 0), (10, 10, 0), (0, 10, 0)], "#11151d"))
for k in range(6):
    w.append(poly([(0.4 + k * 1.7, 9.05, 0), (1.3 + k * 1.7, 9.05, 0), (1.3 + k * 1.7, 9.2, 0), (0.4 + k * 1.7, 9.2, 0)], "#FFC53D"))
w.append(poly([(0, 10, 0), (10, 10, 0), (10, 10, -0.4), (0, 10, -0.4)], "#141922"))
w.append(poly([(10, 0, 0), (10, 10, 0), (10, 10, -0.4), (10, 0, -0.4)], "#0f131a"))
w.append(arbol(0.5, 0.5, 0.9))
# edificio de fondo con ventanas encendidas
w.append(caja(6.2, 0.4, 0, 2.2, 1.8, 5.2, "#495057", "#3b4350", "#2f3640"))
for zz in (1.0, 2.2, 3.4, 4.4):
    for xx in (6.5, 7.3):
        col = "#ffe8a3" if random.random() > 0.3 else "#2b3140"
        w.append(poly([(xx, 2.2, zz), (xx + 0.5, 2.2, zz), (xx + 0.5, 2.2, zz + 0.55), (xx, 2.2, zz + 0.55)], col))
    for yy in (0.7, 1.4):
        col = "#ffe8a3" if random.random() > 0.4 else "#2b3140"
        w.append(poly([(8.4, yy, zz), (8.4, yy + 0.45, zz), (8.4, yy + 0.45, zz + 0.55), (8.4, yy, zz + 0.55)], col))
# caseta de faena con techo de color
w.append(caja(7.6, 3.6, 0, 1.6, 1.2, 1.3, "#E5484D", "#e9ecef", "#ced4da"))
w.append(caja(7.5, 3.5, 1.3, 1.8, 1.4, 0.1, "#E5484D", "#c92a2a", "#a51d1d"))
w.append(poly([(7.9, 4.8, 0.5), (8.5, 4.8, 0.5), (8.5, 4.8, 1.0), (7.9, 4.8, 1.0)], "#a5d8ff"))
# local comercial (la pared donde se cambia la luminaria)
w.append(caja(0.6, 0.8, 0, 4.8, 2.6, 4.0, "#3b5bdb", "#d8cbb5", "#b9ab94"))
w.append(caja(0.6, 0.8, 4.0, 4.8, 2.6, 0.12, "#2f4ac0", "#2a3fa0", "#22358a"))
w.append(poly([(1.0, 3.4, 0), (1.9, 3.4, 0), (1.9, 3.4, 1.9), (1.0, 3.4, 1.9)], "#5c3b1e"))
w.append(poly([(3.9, 3.4, 0.4), (5.1, 3.4, 0.4), (5.1, 3.4, 1.9), (3.9, 3.4, 1.9)], "#ffe8a3"))
w.append(linea((4.5, 3.4, 0.4), (4.5, 3.4, 1.9), "#c9b98a", 4))
for yy in (1.2, 2.2):
    w.append(poly([(5.4, yy, 2.4), (5.4, yy + 0.7, 2.4), (5.4, yy + 0.7, 3.3), (5.4, yy, 3.3)], "#ffe8a3"))
w.append(poly([(1.0, 3.4, 2.3), (2.5, 3.4, 2.3), (2.5, 3.4, 2.85), (1.0, 3.4, 2.85)], "#0D1117", 'stroke="#FFC53D" stroke-width="4"'))
a = iso(1.75, 3.4, 2.42)
w.append(f'<text transform="translate({a[0]:.0f},{a[1]:.0f}) skewY(30)" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="19" fill="#FFC53D">MINIMARKET</text>')
# luminaria en la pared (apagada; se enciende al final)
w.append(caja(2.75, 3.4, 3.5, 0.5, 0.15, 0.18, "#868e96", "#495057", "#343a40"))
a = iso(3.0, 3.6, 3.48)
w.append(f'<g class="luz" opacity="0"><ellipse cx="{a[0]:.0f}" cy="{a[1]+70:.0f}" rx="120" ry="110" fill="#FFE066" opacity=".18"/>'
         f'<ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="22" ry="8" fill="#FFE066"/></g>')
w.append(farol(5.9, 7.4)); w.append(farol(0.4, 6.4))
w.append(cono(5.6, 5.4)); w.append(cono(6.4, 6.6)); w.append(cono(1.0, 7.0))
w.append(arbol(9.4, 9.0, 0.8)); w.append(arbol(9.5, 0.4, 0.8)); w.append(arbol(0.4, 9.2, 0.7))
# caballete con herramientas donde trabaja el compañero
w.append(caja(6.8, 5.4, 0.7, 1.4, 0.5, 0.1, "#c08a4b", "#9c6d39", "#80582d"))
for (xx, yy) in [(6.85, 5.45), (8.1, 5.45), (6.85, 5.8), (8.1, 5.8)]:
    w.append(linea((xx, yy, 0), (xx, yy, 0.7), "#80582d", 6))
w.append(caja(7.2, 5.5, 0.8, 0.5, 0.25, 0.2, "#E5484D", "#c92a2a", "#a51d1d"))

# ---------- tiempos ----------
e = E


def fin(i): return e[i]["inicio"] + e[i]["dur"]


def limpia(s): return s.lower().strip("¿?¡!.,:;\"")


def pal(i, palabra):
    for p in e[i]["palabras"]:
        if limpia(p["p"]).startswith(palabra.lower()): return p["t"]
    raise SystemExit(f"no encontré '{palabra}' en escena {i}")


t_sube = pal(1, "sube")
t_nadie = pal(1, "nadie")
t_cae = pal(1, "cae")
t_uno = pal(3, "uno")
t_susp = pal(4, "suspende")
t_retoma = pal(4, "retoma")
t_avisa = pal(5, "avisa")
t_insp = pal(5, "inspección")
t_multa = pal(6, "multa")
t_revisa = pal(7, "revisa")
t_informar = pal(7, "informar")
t_codigo = pal(7, "código")
R0 = e[7]["inicio"]  # rebobinado


def tr(p): a = iso(*p); return f"translate({a[0]:.0f}px,{a[1]:.0f}px)"


def kf(nombre, pares):
    return "@keyframes " + nombre + "{" + " ".join(f"{pct(t):.2f}%{{{v}}}" for t, v in pares) + "}"


css_extra = []

# escalera (apoyada en la pared; se desliza y cae; vuelve en el rebobinado)
B = (3.0, 4.5, 0)
bx, by = iso(*B)


def lrel(x, y, z):
    a = iso(x, y, z); return a[0] - bx, a[1] - by


def ll(p, q, color, wd):
    a, b = lrel(*p), lrel(*q)
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" stroke-width="{wd}" stroke-linecap="round"/>'


esc = []
for xr in (2.72, 3.28):
    esc.append(ll((xr, 4.5, 0), (xr, 3.45, 3.5), "#adb5bd", 10))
for k in range(1, 8):
    z = k * 0.44; yy = 4.5 - z / 3.5 * 1.05
    esc.append(ll((2.72, yy, z), (3.28, yy, z), "#ced4da", 7))
escalera = f'<g class="escalera">{"".join(esc)}</g>'
ang = 68
css_extra.append(kf("escalera", [(0, f"transform:{tr(B)} rotate(0deg)"), (t_cae - 0.35, f"transform:{tr(B)} rotate(0deg)"),
                                 (t_cae - 0.15, f"transform:{tr(B)} rotate(4deg)"),
                                 (t_cae + 0.45, f"transform:translate({bx+40:.0f}px,{by+18:.0f}px) rotate({ang}deg)"),
                                 (R0 + 0.15, f"transform:translate({bx+40:.0f}px,{by+18:.0f}px) rotate({ang}deg)"),
                                 (R0 + 0.95, f"transform:{tr(B)} rotate(0deg)"), (TOT, f"transform:{tr(B)} rotate(0deg)")]))

# maestro: arriba de la escalera -> cae al suelo -> vuelve arriba en el rebobinado
F = (3.0, 3.85, 2.7); G = (2.0, 5.3, 0)
maestro = (f'<g class="maestro"><g class="mA">{mono("#3b5bdb", "#FFD43B", "feliz", 0.82, brazo="arriba", sombra=False)}</g>'
           f'<g class="mB">{mono("#3b5bdb", "#FFD43B", "dolor", 0.82, sombra=False)}</g></g>')
css_extra.append(kf("maestro", [(0, f"transform:{tr(F)} rotate(0deg)"), (t_cae - 0.15, f"transform:{tr(F)} rotate(0deg)"),
                                (t_cae + 0.25, f"transform:{tr((2.6, 4.6, 1.3))} rotate(-40deg)"),
                                (t_cae + 0.5, f"transform:{tr(G)} rotate(-84deg)"), (t_cae + 0.62, f"transform:{tr((2.0, 5.3, 0.15))} rotate(-80deg)"),
                                (t_cae + 0.75, f"transform:{tr(G)} rotate(-84deg)"),
                                (R0 + 0.15, f"transform:{tr(G)} rotate(-84deg)"), (R0 + 0.95, f"transform:{tr(F)} rotate(0deg)"), (TOT, f"transform:{tr(F)} rotate(0deg)")]))
gx, gy = iso(*G)
sombra_suelo = f'<g class="sombraG"><ellipse cx="{gx-60:.0f}" cy="{gy+4:.0f}" rx="85" ry="18" fill="#0007"/></g>'
alerta_suelo = f'<g class="alertaG"><ellipse cx="{gx-60:.0f}" cy="{gy+4:.0f}" rx="120" ry="40" fill="none" stroke="#E5484D" stroke-width="6"/></g>'

# cota de altura (+1,8 m)
c0 = iso(2.1, 4.1, 0); c1 = iso(2.1, 4.1, 2.7)
cota = (f'<g class="cota"><line x1="{c0[0]:.0f}" y1="{c0[1]:.0f}" x2="{c1[0]:.0f}" y2="{c1[1]:.0f}" stroke="#FFC53D" stroke-width="5" stroke-dasharray="12 8"/>'
        f'<path d="M{c1[0]-12:.0f} {c1[1]+16:.0f} L{c1[0]:.0f} {c1[1]:.0f} L{c1[0]+12:.0f} {c1[1]+16:.0f}" stroke="#FFC53D" stroke-width="5" fill="none"/>'
        f'<line x1="{c0[0]-16:.0f}" y1="{c0[1]:.0f}" x2="{c0[0]+16:.0f}" y2="{c0[1]:.0f}" stroke="#FFC53D" stroke-width="5"/>'
        f'<rect x="{c1[0]-150:.0f}" y="{(c0[1]+c1[1])/2-26:.0f}" width="132" height="52" rx="26" fill="#E5484D"/>'
        f'<text x="{c1[0]-84:.0f}" y="{(c0[1]+c1[1])/2+11:.0f}" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="32" fill="#fff">+1,8 m</text></g>')

# compañero (Juan): trabaja en el caballete -> camina al maestro -> agachado al teléfono -> sujeta la escalera
J0 = (7.0, 6.2); J1 = (2.9, 6.1); JS = (3.55, 4.95)
w_ini = e[2]["inicio"] + 0.8; w_fin = e[3]["inicio"] - 0.3
juan = (f'<g class="juan"><g class="jA">{mono("#7048e8", "#FFFFFF", "susto", 0.82, cola=True)}</g>'
        f'<g class="jB">{agachado_tel("#7048e8", "#FFFFFF", 0.82)}</g>'
        f'<g class="jC">{mono("#7048e8", "#FFFFFF", "feliz", 0.82, cola=True, brazo="sujeta")}</g></g>')
css_extra.append(kf("juan", [(0, f"transform:{tr(J0)}"), (w_ini, f"transform:{tr(J0)}"), (w_fin, f"transform:{tr(J1)}"),
                             (R0 + 0.15, f"transform:{tr(J1)}"), (R0 + 0.95, f"transform:{tr(JS)}"), (TOT, f"transform:{tr(JS)}")]))


def vis(nombre, tramos):
    # tramos: lista de (desde, hasta) en que se ve
    pares = [(0, "opacity:0")]
    for a, b in tramos:
        pares += [(max(a - 0.01, 0), "opacity:0"), (a, "opacity:1"), (b, "opacity:1"), (b + 0.01, "opacity:0")]
    pares.append((TOT, "opacity:0"))
    pares.sort(key=lambda x: x[0])
    css_extra.append(kf(nombre, pares))


vis("vmA", [(0, t_cae - 0.1), (R0 + 0.6, TOT)])
vis("vmB", [(t_cae - 0.1, R0 + 0.6)])
vis("vjA", [(0, w_fin), (R0 + 0.15, R0 + 0.95)])
vis("vjB", [(w_fin, R0 + 0.15)])
vis("vjC", [(R0 + 0.95, TOT)])
vis("vsombra", [(t_cae + 0.5, R0 + 0.3)])
vis("valerta", [(t_cae + 0.55, fin(3))])
vis("vcota", [(t_sube - 0.1, t_cae + 0.2)])
vis("vcinta", [(t_susp - 0.1, R0 + 0.3)])
vis("vluz", [(fin(7) - 2.4, TOT)])

# cinta de peligro alrededor de la zona
cx0, cx1, cy0, cy1, cz = 1.2, 4.4, 3.6, 6.9, 0.55
esquinas = [(cx0, cy0), (cx1, cy0), (cx1, cy1), (cx0, cy1)]
cinta = []
for (x, y) in esquinas:
    cinta.append(linea((x, y, 0), (x, y, cz + 0.1), "#f1f3f5", 7))
for k in range(4):
    p, q = esquinas[k], esquinas[(k + 1) % 4]
    cinta.append(linea((p[0], p[1], cz), (q[0], q[1], cz), "#E5484D", 12))
    cinta.append(linea((p[0], p[1], cz), (q[0], q[1], cz), "#ffffff", 12, 'stroke-dasharray="18 18" stroke-linecap="butt"'))
cinta = f'<g class="cinta">{"".join(cinta)}</g>'

# candado sobre la zona (faena suspendida)
LK = iso(2.8, 5.2, 5.0)
candado = (f'<g class="candado"><circle r="62" fill="#0D1117" stroke="#E5484D" stroke-width="8"/>'
           f'<path d="M-22 -6 V-24 A22 22 0 0 1 22 -24 V-6" stroke="#FFC53D" stroke-width="10" fill="none"/>'
           f'<rect x="-32" y="-8" width="64" height="48" rx="10" fill="#FFC53D"/><circle cy="12" r="7" fill="#0D1117"/><rect x="-3" y="12" width="6" height="16" fill="#0D1117"/></g>')
css_extra.append("@keyframes lockpop{" + f"from{{transform:translate({LK[0]:.0f}px,{LK[1]:.0f}px) scale(.2);opacity:0}}60%{{transform:translate({LK[0]:.0f}px,{LK[1]:.0f}px) scale(1.15);opacity:1}}to{{transform:translate({LK[0]:.0f}px,{LK[1]:.0f}px) scale(1);opacity:1}}" + "}")

# check verde (rebobinado: así sí)
OK = iso(3.3, 4.4, 5.6)
check = (f'<g class="check"><circle r="40" fill="#25D366"/><path d="M-17 0 l12 13 l24 -26" stroke="#0D1117" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
css_extra.append("@keyframes checkpop{" + f"from{{transform:translate({OK[0]:.0f}px,{OK[1]:.0f}px) scale(.2);opacity:0}}60%{{transform:translate({OK[0]:.0f}px,{OK[1]:.0f}px) scale(1.15);opacity:1}}to{{transform:translate({OK[0]:.0f}px,{OK[1]:.0f}px) scale(1);opacity:1}}" + "}")


# ---------- cámara ----------
def foco(t, p, s):
    px, py = iso(*p)
    return (t, s, -s * (px - 540), -20 - s * (py - 520))


P_wide = (4.6, 4.8, 0.8); P_lad = (3.0, 4.2, 2.2); P_suelo = (2.5, 5.6, 0.5); P_cinta = (2.8, 5.2, 1.4)
cam = [foco(0, P_lad, 1.25), foco(e[1]["inicio"] - 0.1, P_lad, 1.4), foco(e[1]["inicio"] + 0.4, P_wide, 0.95),
       foco(t_nadie, P_lad, 1.35), foco(t_cae, P_lad, 1.5), foco(t_cae + 0.6, P_suelo, 1.55), foco(fin(1), P_suelo, 1.7),
       foco(e[2]["inicio"] + 0.4, P_wide, 1.0), foco(fin(2), (4.2, 5.4, 0.6), 1.1),
       foco(e[3]["inicio"] + 0.2, P_suelo, 1.75), foco(fin(3), (2.6, 5.8, 0.5), 1.85),
       foco(e[4]["inicio"] + 0.4, P_cinta, 1.2), foco(fin(4), P_cinta, 1.3),
       foco(e[5]["inicio"] + 0.4, P_wide, 1.05), foco(fin(5), (4.0, 5.0, 0.8), 1.12),
       foco(e[6]["inicio"] + 0.4, P_wide, 0.95), foco(fin(6), P_wide, 1.0),
       foco(R0 + 0.3, P_lad, 1.15), foco(R0 + 1.2, P_lad, 1.4), foco(t_informar, (3.2, 4.5, 1.6), 1.5), foco(fin(7), (3.4, 4.6, 1.4), 1.3),
       foco(TOT, P_wide, 1.0)]
cam_kf = " ".join(f"{pct(t):.2f}%{{transform:translate({x:.0f}px,{y:.0f}px) scale({s})}}" for t, s, x, y in cam)

# ---------- subtítulos karaoke ----------
clave = {0: {"cayó", "metro", "ochenta", "grave"}, 1: {"escalera", "nadie", "sujeta", "cae"},
         2: {"2025", "cuatrocientos", "noventa", "ocho", "suseso"}, 3: {"uno", "muevas", "ayuda", "mutual", "isl"},
         4: {"dos", "suspende", "faena", "fiscalización"}, 5: {"tres", "avisa", "inspección", "seremi", "salud"},
         6: {"ley", "dieciséis", "setenta", "seis", "multa", "cincuenta", "ciento"},
         7: {"escalera", "sujete", "informar", "obligación", "código", "ochenta", "cuatro"},
         8: {"altura", "matriz", "riesgos", "nadie", "suelo", "basesegura.cl", "minuto"}}
subs = []
for i, ee in enumerate(E):
    ps = list(ee["palabras"]); trozos, cur = [], []
    # mostrar en pantalla "basesegura.cl" y "UTM" en vez de la forma hablada
    for patron, unido in ((["base", "segura", "punto", "cl"], "basesegura.cl"), (["u", "t", "m"], "UTM")):
        j = 0
        while j + len(patron) <= len(ps):
            if [limpia(q["p"]) for q in ps[j:j + len(patron)]] == patron:
                cola = ps[j + len(patron) - 1]["p"]; fin_p = cola[-1] if cola[-1] in ".,:?" else ""
                ps[j:j + len(patron)] = [dict(ps[j], p=unido + fin_p)]
            j += 1
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
        ws = "".join(f'<span class="w{" k" if limpia(p["p"]) in clave.get(i, set()) else ""}" style="animation-delay:{p["t"]:.2f}s">{html.escape(p["p"])}</span> ' for p in trz)
        subs.append(f'<div class="sub cut" style="--i:{a0:.2f}s;--d:{b0 - a0:.2f}s">{ws}</div>')


def pill(txt, bg, fg, t, d, top, chica=False):
    return f'<div class="pill win{" chica" if chica else ""}" style="--i:{t:.2f}s;--d:{d:.2f}s;top:{top}px"><span class="pop" style="animation-delay:{t:.2f}s;background:{bg};color:{fg}">{txt}</span></div>'


AM, NE, RO, AZ, VE = "#FFC53D", "#0D1117", "#E5484D", "#1FA9E8", "#25D366"
t_grave = pal(0, "grave") - 0.15
pills = [
    pill("⚠️ ACCIDENTE GRAVE", RO, "#fff", t_grave, fin(0) - t_grave, 1410),
    pill("🪜 NADIE SUJETA LA ESCALERA", AZ, NE, t_nadie - 0.1, t_cae - t_nadie, 1330),
    pill("⚠️ CAÍDA DE MÁS DE 1,8 m<br>= ACCIDENTE GRAVE", RO, "#fff", t_cae + 0.3, fin(1) - t_cae - 0.3, 1290),
    pill("⏱ 3 COSAS · DE INMEDIATO", AM, NE, e[3]["inicio"] + 0.1, e[3]["dur"] - 0.1, 1220),
    pill("🚑 1 · NO MOVERLO Y PEDIR AYUDA", AM, NE, t_uno - 0.1, fin(3) - t_uno + 0.1, 1330),
    pill("🏥 MUTUAL O ISL", AZ, NE, pal(3, "mutual") - 0.1, fin(3) - pal(3, "mutual") + 0.1, 1440, chica=True),
    pill("🔒 2 · SUSPENDER LA FAENA", AM, NE, t_susp - 0.1, fin(4) - t_susp + 0.1, 1220),
    pill("🔍 SE RETOMA SOLO CON FISCALIZACIÓN", AZ, NE, t_retoma - 0.1, fin(4) - t_retoma + 0.1, 1330),
    pill("📞 3 · AVISAR DE INMEDIATO", AM, NE, t_avisa - 0.1, fin(5) - t_avisa + 0.1, 1210),
    pill("🏛️ INSPECCIÓN DEL TRABAJO<br>Y SEREMI DE SALUD", AZ, NE, t_insp - 0.1, fin(5) - t_insp + 0.1, 1315),
    pill("💸 MULTA: 50 A 150 UTM", RO, "#fff", t_multa - 0.1, fin(6) - t_multa + 0.1, 1400),
    pill("⏪ MEJOR QUE NO PASE", AZ, NE, R0 + 0.1, t_revisa - R0 - 0.1, 1260),
    pill("✅ ESCALERA REVISADA<br>Y ALGUIEN LA SUJETA", VE, NE, t_revisa - 0.1, fin(7) - t_revisa + 0.1, 1170),
    pill("✅ RIESGO INFORMADO ANTES DE SUBIR", VE, NE, t_informar - 0.1, fin(7) - t_informar + 0.1, 1320),
    pill("📖 Código del Trabajo · art. 184", "#ffffff", NE, t_codigo - 0.1, fin(7) - t_codigo + 0.1, 1430, chica=True),
]

# gancho
gancho = f'''<div class="gancho win" style="--i:0s;--d:{e[1]['inicio']:.2f}s">
<div class="gtit">¿Se cayó de más de <span style="color:#F2A33A">1,80 m</span>?</div>
<div class="gsub">Accidente <span style="color:#E5484D">grave</span>: ¿qué haces primero?</div>
<svg viewBox="-200 -290 400 320" class="gmono"><g class="balancea">{mono("#3b5bdb", "#FFD43B", "preocupa", 1.0, brazo="cabeza")}</g></svg></div>'''

# estadística Suseso (escena 2)
dato = f'''<div class="dato win" style="--i:{e[2]['inicio']:.2f}s;--d:{e[2]['dur']:.2f}s"><div class="dato-card">
<div class="dato-h">📊 ACCIDENTES GRAVES · 2025</div>
<div class="num"></div>
<div class="dato-l">por <b>caídas de más de 1,8 m</b></div>
<div class="barra"><i></i></div>
<div class="dato-s">de <b>1.770</b> accidentes graves en total</div>
<div class="dato-f">Fuente: Suseso, Estadísticas SST 2025</div></div></div>'''

# teléfono (escena 5)
tel = f'''<div class="tel win" style="--i:{e[5]['inicio']:.2f}s;--d:{e[5]['dur']:.2f}s"><div class="tel-b">
<div class="tel-notch"></div>
<div class="tel-ll">Llamando<span class="pts">…</span></div>
<div class="tel-av"><span class="anillo"></span><span class="anillo a2"></span><span class="tel-ico">🏛️</span></div>
<div class="tel-n">Inspección del Trabajo</div>
<div class="tel-y">y Seremi de Salud</div>
<div class="tel-m">Aviso de accidente grave</div>
<div class="tel-bt"><span style="background:#E5484D">✆</span><span style="background:#25D366">✆</span></div></div></div>'''

ley = f'''<div class="ley win" style="--i:{e[6]['inicio']+0.2:.2f}s;--d:{e[6]['dur']-0.2:.2f}s"><div class="ley-card">
<div class="ley-h">LEY 16.744 · CHILE</div><div class="ley-art">Art. 76</div>
<p>En accidentes graves, el empleador "…<mark>deberá suspender de forma inmediata las faenas afectadas</mark>…"</p>
<p class="p2">Multa "de cincuenta a ciento cincuenta unidades tributarias mensuales".</p>
<div class="ley-tag">🇨🇱 Ley 16.744 · Chile · art. 76</div></div></div>'''

rebob = f'''<div class="rebob win" style="--i:{R0:.2f}s;--d:1.1s"><div class="rb-ico">⏪</div></div>'''

t_fase2 = pal(8, "te") - 0.2
minis = "".join(f'<div class="mini" style="animation-delay:{e[8]["inicio"]+0.4+k*0.25:.2f}s"><svg viewBox="-60 -240 120 250" width="150" height="312">{mono(c, h, cara, 1.0, cola=cola)}</svg></div>'
                for k, (c, h, cara, cola) in enumerate([("#3b5bdb", "#FFD43B", "preocupa", False), ("#7048e8", "#FFFFFF", "duda", True), ("#868e96", "#FFFFFF", "susto", False)]))
cta = f'''<div class="cta win" style="--i:{e[8]['inicio']:.2f}s;--d:{TOT-e[8]['inicio']:.2f}s"><div class="cta-in">
<div class="logo">{LOGO}</div>
<div class="fase1 win" style="--i:{e[8]['inicio']:.2f}s;--d:{t_fase2-e[8]['inicio']+0.3:.2f}s">
<div class="cta-t">¿En tu empresa se trabaja<br><span style="color:#F2A33A">en altura</span>?</div>
<div class="minis">{minis}</div></div>
<div class="fase2">
<div class="cta-t2">Te hacemos la <span style="color:#F2A33A">matriz de riesgos</span></div>
<div class="cta-p">para que <b>nadie se caiga</b></div>
<div class="cta-r">Cotiza en 1 minuto · diagnóstico gratis</div>
<div class="cta-band">Cotiza tu matriz de riesgos<br>en <b>basesegura.cl</b></div>
<div class="cta-mail">contacto@basesegura.cl</div></div></div>
<div class="fuente">Fuente: Ley 16.744 (Chile), art. 76 · Código del Trabajo, art. 184 (texto DT al 02-11-2026) · Suseso, Compendio Ley 16.744, Libro IV, Tít. I, Letra D · Suseso, Estadísticas SST 2025 (datos al 23-03-2026)</div></div>'''

lluvia = "".join(f'<i style="left:{random.randint(0,1100)}px;animation-delay:-{random.random()*2:.2f}s;animation-duration:{1.1+random.random()*0.8:.2f}s;opacity:{0.10+random.random()*0.18:.2f}"></i>' for _ in range(45))

m = lambda a, b: f"{pct(a):.2f}%{{opacity:{b}}}"
ocultar = " ".join([m(0, .3), m(e[1]['inicio'] - 0.2, .3), m(e[1]['inicio'] + 0.2, 1), m(e[2]['inicio'], 1), m(e[2]['inicio'] + 0.3, .3),
                    m(fin(2) - 0.1, .3), m(e[3]['inicio'] + 0.2, 1), m(e[5]['inicio'], 1), m(e[5]['inicio'] + 0.3, .4),
                    m(fin(5) - 0.1, .4), m(e[6]['inicio'] + 0.3, .25), m(R0 - 0.1, .25), m(R0 + 0.3, 1), m(fin(7) - 0.1, 1),
                    m(e[8]['inicio'] + 0.4, 0), m(TOT, 0)])

CSS = f"""
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;background:radial-gradient(circle at 50% 35%,#1f2a3f 0,#1a2233 40%,#0D1117 78%);font-family:Manrope;color:#fff;position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#ffffff07 2px,transparent 2px),linear-gradient(90deg,#ffffff07 2px,transparent 2px);background-size:90px 90px}}
.win{{opacity:0;animation:show var(--d) linear var(--i) both}}
@keyframes show{{0%{{opacity:0}}4%{{opacity:1}}96%{{opacity:1}}100%{{opacity:0}}}}
.cut{{opacity:0;animation:cut var(--d) linear var(--i) both}}
@keyframes cut{{0%{{opacity:0}}1%{{opacity:1}}99%{{opacity:1}}100%{{opacity:0}}}}
.handle{{position:absolute;top:150px;right:60px;font-family:Outfit;font-weight:800;font-size:28px;opacity:.85;display:flex;gap:10px;align-items:center;z-index:20}}
.handle i{{width:30px;height:30px;border:4px solid #fff;border-radius:9px;display:inline-block;position:relative}}
.handle i:after{{content:"";position:absolute;left:5px;top:5px;width:12px;height:12px;border:3px solid #fff;border-radius:50%;box-sizing:border-box}}
.mundo-wrap{{position:absolute;left:0;right:0;top:440px;height:1000px;animation:ocultaMundo {TOT}s linear both}}
@keyframes ocultaMundo{{{ocultar}}}
.cam{{width:1080px;height:1000px;transform-origin:540px 520px;animation:cam {TOT}s ease-in-out both}}
@keyframes cam{{{cam_kf}}}
.shake{{animation:tiembla .09s linear {t_cae+0.5:.2f}s 6 both}}
@keyframes tiembla{{0%{{transform:none}}25%{{transform:translate(14px,-8px)}}50%{{transform:translate(-12px,9px)}}75%{{transform:translate(9px,6px)}}100%{{transform:none}}}}
.lluvia{{position:absolute;left:0;right:0;top:440px;height:1000px;overflow:hidden;pointer-events:none;animation:ocultaMundo {TOT}s linear both}}
.lluvia i{{position:absolute;top:-60px;width:2px;height:46px;background:linear-gradient(#cfd8e300,#cfd8e3);transform:rotate(12deg);animation-name:llueve;animation-timing-function:linear;animation-iteration-count:infinite}}
@keyframes llueve{{to{{transform:translate(-220px,1080px) rotate(12deg)}}}}
.escalera,.maestro,.juan,.candado,.check{{transform-origin:0 0}}
.escalera{{animation:escalera {TOT}s linear both}}
.maestro{{animation:maestro {TOT}s linear both}}
.juan{{animation:juan {TOT}s linear both}}
.mA{{animation:vmA {TOT}s linear both}} .mB{{animation:vmB {TOT}s linear both}}
.jA{{animation:vjA {TOT}s linear both}} .jB{{animation:vjB {TOT}s linear both}} .jC{{animation:vjC {TOT}s linear both}}
.jA .p1{{animation:paso .28s ease-in-out {w_ini:.2f}s {int((w_fin-w_ini)/0.28)} alternate}} .jA .p2{{animation:paso .28s ease-in-out {w_ini:.2f}s {int((w_fin-w_ini)/0.28)} alternate-reverse}}
.sombraG{{animation:vsombra {TOT}s linear both}}
.alertaG{{animation:valerta {TOT}s linear both}} .alertaG ellipse{{animation:late .45s ease-in-out infinite alternate}}
.cota{{animation:vcota {TOT}s linear both}}
.cinta{{animation:vcinta {TOT}s linear both}}
.luz{{animation:vluz {TOT}s linear both}}
.candado{{opacity:0;animation:lockpop .5s cubic-bezier(.2,1.4,.4,1) {t_susp+0.1:.2f}s both, fuera .3s linear {fin(4)-0.2:.2f}s forwards}}
.check{{opacity:0;animation:checkpop .5s cubic-bezier(.2,1.4,.4,1) {t_revisa:.2f}s both}}
.ondas{{animation:late .4s ease-in-out infinite alternate}}
.gota{{animation:gotea 1s ease-in infinite}} @keyframes gotea{{from{{transform:none;opacity:1}}to{{transform:translateY(40px);opacity:0}}}}
@keyframes fuera{{to{{opacity:0}}}} @keyframes aparece{{to{{opacity:1}}}}
.pierna{{transform-box:fill-box;transform-origin:50% 0}}
@keyframes paso{{from{{transform:rotate(-16deg)}}to{{transform:rotate(16deg)}}}}
@keyframes late{{to{{opacity:.35}}}}
{chr(10).join(css_extra)}
.techo{{position:absolute;left:0;right:0;top:0;height:470px;background:linear-gradient(#0D1117 0,#0D1117dd 55%,#0D111700 100%)}}
.sub{{position:absolute;left:70px;right:70px;top:230px;text-align:center;font-family:Outfit;font-weight:800;font-size:62px;line-height:1.15;text-shadow:0 4px 18px #000;z-index:10}}
.w{{opacity:.22;animation:palabra .18s ease-out both}} .w.k{{color:#F2A33A}}
@keyframes palabra{{from{{opacity:.22;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.pill{{position:absolute;left:30px;right:30px;display:flex;justify-content:center;font-family:Outfit;font-weight:800;font-size:42px;line-height:1.15;letter-spacing:.3px;z-index:6;text-align:center}}
.pill.chica{{font-size:32px}} .pill.chica .pop{{padding:12px 26px;border:3px solid #0D1117}}
.pill .pop{{display:inline-block;max-width:1000px;padding:20px 34px;border-radius:60px;box-shadow:0 10px 30px #0008;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
@keyframes pop{{from{{transform:scale(.4);opacity:0}}to{{transform:none;opacity:1}}}}
.gancho{{position:absolute;inset:0}}
.gtit{{position:absolute;left:50px;right:50px;top:470px;text-align:center;font-family:Outfit;font-weight:900;font-size:104px;line-height:1.02;letter-spacing:-2px;text-shadow:0 6px 30px #000;animation:pop .6s cubic-bezier(.2,1.6,.4,1) .1s both}}
.gsub{{position:absolute;left:50px;right:50px;top:700px;text-align:center;font-family:Outfit;font-weight:800;font-size:56px;text-shadow:0 6px 30px #000;animation:pop .6s cubic-bezier(.2,1.6,.4,1) .5s both}}
.gmono{{position:absolute;left:40px;top:790px;width:1000px;height:760px}}
.balancea{{transform-origin:0 0;animation:balancea .6s ease-in-out infinite alternate}}
@keyframes balancea{{from{{transform:rotate(-3deg)}}to{{transform:rotate(3deg) translateY(-6px)}}}}
@keyframes subeCard{{from{{transform:translateY(900px)}}to{{transform:none}}}}
.dato{{position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;z-index:5}}
.dato-card{{width:900px;background:#0D1117f0;border:4px solid #2b3447;border-radius:40px;padding:40px 50px;box-shadow:0 30px 80px #000c;text-align:center;animation:pop .55s cubic-bezier(.2,1.4,.4,1) {e[2]['inicio']:.2f}s both}}
.dato-h{{display:inline-block;background:#1FA9E8;color:#0D1117;font-family:Outfit;font-weight:800;font-size:38px;padding:12px 28px;border-radius:40px}}
@property --n{{syntax:'<integer>';inherits:false;initial-value:0}}
.num{{font-family:Outfit;font-weight:900;font-size:230px;line-height:1;margin-top:20px;color:#F2A33A;counter-reset:n var(--n);animation:cuenta 2.2s cubic-bezier(.2,.8,.3,1) {e[2]['inicio']+0.4:.2f}s both}}
.num::after{{content:counter(n)}}
@keyframes cuenta{{from{{--n:0}}to{{--n:498}}}}
.dato-l{{font-family:Outfit;font-weight:800;font-size:50px}} .dato-l b{{color:#F2A33A}}
.barra{{margin:30px auto 0;width:760px;height:40px;border-radius:20px;background:#2b3447;overflow:hidden}}
.barra i{{display:block;height:100%;width:28.1%;background:#E5484D;border-radius:20px;transform-origin:0 50%;animation:barra 2.2s cubic-bezier(.2,.8,.3,1) {e[2]['inicio']+0.4:.2f}s both}}
@keyframes barra{{from{{transform:scaleX(0)}}to{{transform:none}}}}
.dato-s{{margin-top:18px;font-size:40px;font-weight:700;color:#c9d1d9}}
.dato-f{{margin-top:22px;font-size:28px;color:#8b949e;font-weight:700}}
.tel{{position:absolute;left:0;right:0;top:460px;display:flex;justify-content:center;z-index:5}}
.tel-b{{position:relative;width:500px;height:710px;border-radius:70px;background:linear-gradient(#1c2333,#0D1117);border:10px solid #343a46;box-shadow:0 30px 80px #000d;display:flex;flex-direction:column;align-items:center;padding-top:64px;animation:telEntra .6s cubic-bezier(.2,1.3,.4,1) {e[5]['inicio']:.2f}s both}}
@keyframes telEntra{{from{{transform:translateX(700px) rotate(12deg)}}to{{transform:none}}}}
.tel-notch{{position:absolute;top:18px;width:140px;height:30px;border-radius:15px;background:#000}}
.tel-ll{{font-size:36px;font-weight:700;color:#8b949e}}
.tel-av{{position:relative;margin:26px 0 22px;width:140px;height:140px;border-radius:50%;background:#1FA9E8;display:flex;align-items:center;justify-content:center}}
.tel-ico{{font-size:72px}}
.anillo{{position:absolute;inset:0;border-radius:50%;border:6px solid #1FA9E8;animation:onda 1.2s ease-out infinite}} .a2{{animation-delay:-.6s}}
@keyframes onda{{from{{transform:scale(1);opacity:.9}}to{{transform:scale(1.7);opacity:0}}}}
.tel-n{{font-family:Outfit;font-weight:900;font-size:44px;text-align:center;line-height:1.1}}
.tel-y{{font-family:Outfit;font-weight:900;font-size:44px;color:#F2A33A}}
.tel-m{{margin-top:12px;font-size:30px;font-weight:700;color:#8b949e}}
.tel-bt{{position:absolute;bottom:34px;display:flex;gap:150px}}
.tel-bt span{{width:90px;height:90px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:54px;color:#fff}}
.ley{{position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;z-index:5}}
.ley-card{{width:900px;background:#fff;color:#0D1117;border-radius:34px;padding:46px 54px;box-shadow:0 30px 80px #000c;animation:subeCard .6s cubic-bezier(.2,1.3,.4,1) {e[6]['inicio']+0.2:.2f}s both}}
.ley-h{{background:#0D1117;color:#fff;display:inline-block;font-family:Outfit;font-weight:800;font-size:32px;padding:10px 22px;border-radius:12px;letter-spacing:1px}}
.ley-art{{font-family:Outfit;font-weight:900;font-size:96px;margin:14px 0 10px}}
.ley-card p{{font-size:44px;line-height:1.34;color:#374151}} .ley-card mark{{background:#FFE066;color:#0D1117;padding:0 6px;font-weight:800}}
.ley-card .p2{{margin-top:22px;font-size:38px}}
.ley-tag{{display:inline-block;margin-top:28px;border:3px solid #0D1117;border-radius:40px;padding:10px 22px;font-family:Outfit;font-weight:800;font-size:30px}}
.rebob{{position:absolute;left:0;right:0;top:440px;height:1000px;z-index:4;background:repeating-linear-gradient(#1FA9E814 0 6px,transparent 6px 18px);display:flex;align-items:center;justify-content:center}}
.rb-ico{{font-size:220px;opacity:.85;animation:late .25s ease-in-out infinite alternate}}
.cta{{position:absolute;inset:0;background:#0D1117;z-index:8}}
.cta-in{{position:absolute;left:0;right:0;top:420px;display:flex;flex-direction:column;align-items:center;animation:zoomLento {TOT-e[8]['inicio']:.2f}s linear {e[8]['inicio']:.2f}s both}}
@keyframes zoomLento{{from{{transform:scale(.97)}}to{{transform:scale(1.03)}}}}
.logo{{animation:pop .6s cubic-bezier(.2,1.6,.4,1) {e[8]['inicio']+0.1:.2f}s both}}
.fase1{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center}}
.cta-t{{font-family:Outfit;font-weight:900;font-size:76px;line-height:1.06;text-align:center;letter-spacing:-1px}}
.minis{{display:flex;gap:40px;margin-top:30px}} .mini{{opacity:0;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
.fase2{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center;opacity:0;animation:aparece .4s ease-out {t_fase2:.2f}s both}}
.cta-t2{{font-family:Outfit;font-weight:900;font-size:62px;line-height:1.14;text-align:center;padding:0 60px}}
.cta-p{{margin-top:18px;font-family:Outfit;font-weight:800;font-size:56px}} .cta-p b{{color:#25D366}}
.cta-r{{margin-top:8px;font-size:28px;color:#8b949e;font-weight:700;text-align:center;padding:0 90px}}
.cta-band{{margin-top:40px;background:#F2A33A;color:#0D1117;font-family:Outfit;font-weight:800;font-size:50px;line-height:1.2;padding:30px 46px;border-radius:30px;text-align:center;animation:pop .5s cubic-bezier(.2,1.6,.4,1) {pal(8, 'entra')-0.2:.2f}s both}}
.cta-band b{{font-weight:900}}
.cta-mail{{margin-top:30px;font-family:Outfit;font-weight:800;font-size:46px;color:#1FA9E8}}
.fuente{{position:absolute;bottom:420px;left:90px;right:90px;text-align:center;font-size:25px;line-height:1.4;color:#8b949e}}
"""

page = f'''<!doctype html><html><head><meta charset="utf-8"><link href="file:///tmp/bs/fonts/fonts.css" rel="stylesheet"><style>{CSS}</style></head><body>
<div class="grid"></div>
<div class="mundo-wrap"><div class="cam"><div class="shake"><svg width="1080" height="1000" viewBox="0 0 1080 1000" overflow="visible">
{"".join(w)}{sombra_suelo}{alerta_suelo}{escalera}{cota}{maestro}{juan}{cinta}{candado}{check}</svg></div></div></div>
<div class="lluvia">{lluvia}</div>
<div class="techo"></div>
{gancho}{dato}{tel}{ley}{rebob}{"".join(pills)}{cta}{"".join(subs)}
<div class="handle"><i></i>@basesegura.cl</div>
</body></html>'''
open(f"{R}/reel.html", "w", encoding="utf-8").write(page)
print("ok", TOT)
