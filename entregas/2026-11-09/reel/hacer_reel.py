#!/usr/bin/env python3
# Reel 2026-11-09: "¿Cuánto peso puede cargar un trabajador?" (CT arts. 211-G a 211-J) — estilo marca/ESTILO-REELS.md
# Uso: python3 hacer_reel.py entregas/2026-11-09/reel   (lee tiempos.json, escribe reel.html)
import json, sys, html, random
R = sys.argv[1]
T = json.load(open(f"{R}/tiempos.json", encoding="utf-8"))
E = T["escenas"]; TOT = T["total"]
LOGO = open("/tmp/bs/marca/logo.svg").read().replace('<svg ', '<svg width="200" height="200" ', 1)
random.seed(9)


def iso(x, y, z=0):
    return 540 + (x - y) * 52, 250 + (x + y) * 30 - z * 60


def rel(x, y, z=0):
    return (x - y) * 52, (x + y) * 30 - z * 60


def poly(pts, fill, extra="", f=iso):
    p = " ".join(f"{a:.1f},{b:.1f}" for a, b in (f(*q) for q in pts))
    return f'<polygon points="{p}" fill="{fill}" {extra}/>'


def linea(p, q, color, w=6, extra="", f=iso):
    a, b = f(*p), f(*q)
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def caja(x0, y0, z0, dx, dy, dz, top, left, right, extra="", f=iso):
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    return (f'<g {extra}>' +
            poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], left, f=f) +
            poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], right, f=f) +
            poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, f=f) + '</g>')


def saco(x, y, z, f=iso, chico=False):
    dx, dy, dz = (0.55, 0.38, 0.17) if chico else (0.7, 0.45, 0.2)
    s = caja(x, y, z, dx, dy, dz, "#eadfc4", "#cdbb95", "#b29f7a", f=f)
    s += poly([(x + dx * 0.3, y + dy, z + 0.03), (x + dx * 0.7, y + dy, z + 0.03), (x + dx * 0.7, y + dy, z + dz - 0.03), (x + dx * 0.3, y + dy, z + dz - 0.03)], "#E5484D" if not chico else "#1FA9E8", f=f)
    return s


def arbol(x, y, r=0.9):
    a = iso(x, y)
    return (f'<g><ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="26" ry="9" fill="#0006"/><rect x="{a[0]-5:.0f}" y="{a[1]-50:.0f}" width="10" height="50" fill="#6b4a2b"/>'
            f'<circle cx="{a[0]:.0f}" cy="{a[1]-70:.0f}" r="{r*40:.0f}" fill="#2b8a3e"/><circle cx="{a[0]-10:.0f}" cy="{a[1]-80:.0f}" r="{r*18:.0f}" fill="#51cf66" opacity=".45"/></g>')


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
                f'<path d="M-11 {cy+16} q5.5 -6 11 0 q5.5 6 11 0" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>'
                f'<path class="gota" d="M30 {cy-14} q6 9 0 13 q-6 -4 0 -13Z" fill="#9fd0ff"/>')
    ojos = f'<circle cx="-13" cy="{cy-4}" r="5" fill="#111"/><circle cx="13" cy="{cy-4}" r="5" fill="#111"/>'
    boca = {'feliz': f'<path d="M-10 {cy+12} Q0 {cy+20} 10 {cy+12}" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>',
            'susto': f'<ellipse cx="0" cy="{cy+15}" rx="6" ry="8" fill="#111"/>',
            'sudor': f'<path d="M-10 {cy+16} Q0 {cy+9} 10 {cy+16}" stroke="#111" stroke-width="4" fill="none" stroke-linecap="round"/>',
            'manda': f'<path d="M-12 {cy+12} L12 {cy+12} L8 {cy+20} L-8 {cy+20}Z" fill="#111"/>',
            'duda': f'<path d="M-9 {cy+15} L9 {cy+12}" stroke="#111" stroke-width="4" stroke-linecap="round"/>'}[cara]
    cejas = {'susto': f'<path d="M-21 {cy-18} L-7 {cy-14} M21 {cy-18} L7 {cy-14}" stroke="#111" stroke-width="4" stroke-linecap="round"/>',
             'sudor': f'<path d="M-21 {cy-14} L-7 {cy-19} M21 {cy-14} L7 {cy-19}" stroke="#111" stroke-width="4" stroke-linecap="round"/>',
             'manda': f'<path d="M-21 {cy-19} L-7 {cy-13} M21 {cy-19} L7 {cy-13}" stroke="#111" stroke-width="4" stroke-linecap="round"/>',
             'duda': f'<path d="M-21 {cy-17} L-7 {cy-17} M21 {cy-21} L7 {cy-15}" stroke="#111" stroke-width="4" stroke-linecap="round"/>'}.get(cara, '')
    extra = f'<path class="gota" d="M30 {cy-14} q6 9 0 13 q-6 -4 0 -13Z" fill="#9fd0ff"/>' if cara == "sudor" else ""
    return ojos + cejas + boca + extra


def cabeza(cara, casco, pelo="", bigote=False):
    big = '<path d="M-16 -128 Q-8 -138 0 -131 Q8 -138 16 -128 Q8 -126 0 -129 Q-8 -126 -16 -128Z" fill="#4a3424"/>' if bigote else ''
    return (f'{pelo}<circle cx="0" cy="-146" r="34" fill="#F2C9A0"/>{cara_svg(cara)}{big}'
            f'<path d="M-34 -160 A34 32 0 0 1 34 -160 Z" fill="{casco}"/><rect x="-40" y="-164" width="80" height="9" rx="4.5" fill="{casco}"/>')


COLA = '<circle cx="30" cy="-132" r="15" fill="#5c3b1e"/><path d="M-34 -152 Q-30 -178 0 -178 Q30 -178 34 -152" fill="#5c3b1e"/>'


def mono(color="#3b5bdb", casco="#FFD43B", cara="feliz", escala=1.0, cola=False, bigote=False, brazo="normal", saco_hombro=False):
    pelo = COLA if cola else ''
    if brazo == "apunta":
        brazos = (f'<rect x="-38" y="-108" width="14" height="46" rx="7" fill="{color}"/>'
                  f'<g transform="rotate(-100 31 -102)"><rect x="24" y="-108" width="14" height="58" rx="7" fill="{color}"/><circle cx="31" cy="-50" r="9" fill="#F2C9A0"/></g>')
    elif brazo == "arriba":
        brazos = (f'<rect x="-38" y="-108" width="14" height="46" rx="7" fill="{color}"/>'
                  f'<g transform="rotate(200 31 -102)"><rect x="24" y="-108" width="14" height="48" rx="7" fill="{color}"/></g>')
    elif brazo == "empuja":
        brazos = (f'<g transform="rotate(45 -31 -102)"><rect x="-38" y="-108" width="14" height="52" rx="7" fill="{color}"/><circle cx="-31" cy="-56" r="8" fill="#F2C9A0"/></g>'
                  f'<g transform="rotate(30 31 -102)"><rect x="24" y="-108" width="14" height="50" rx="7" fill="{color}"/></g>')
    elif brazo == "carga":
        brazos = (f'<g transform="rotate(25 -31 -102)"><rect x="-38" y="-108" width="14" height="50" rx="7" fill="{color}"/></g>'
                  f'<g transform="rotate(-25 31 -102)"><rect x="24" y="-108" width="14" height="50" rx="7" fill="{color}"/></g>')
    else:
        brazos = f'<rect x="-38" y="-108" width="14" height="46" rx="7" fill="{color}"/><rect x="24" y="-108" width="14" height="46" rx="7" fill="{color}"/>'
    sh = ''
    if saco_hombro:
        sh = ('<g transform="rotate(-10 40 -190)"><rect x="-10" y="-222" width="120" height="58" rx="24" fill="#eadfc4" stroke="#b29f7a" stroke-width="4"/>'
              '<rect x="30" y="-222" width="20" height="58" fill="#E5484D"/>'
              '<text x="50" y="-183" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="26" fill="#0D1117">50 KG</text></g>')
    return f'''<g transform="scale({escala})">
<ellipse cx="0" cy="0" rx="34" ry="11" fill="#0006"/>
<g class="pierna p1"><rect x="-20" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<g class="pierna p2"><rect x="3" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/></g>
<rect x="-26" y="-112" width="52" height="62" rx="20" fill="{color}"/>
<rect x="-26" y="-84" width="52" height="9" fill="#FFD43B"/>
<g class="brazos">{brazos}</g>
{cabeza(cara, casco, pelo, bigote)}{sh}
</g>'''


def doblado(color="#3b5bdb", casco="#FFD43B", escala=0.9):
    # Pedro doblado por el tirón: piernas fijas, torso inclinado, mano en la espalda
    return f'''<g transform="scale({escala})"><ellipse cx="20" cy="0" rx="56" ry="13" fill="#0006"/>
<rect x="-20" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/><rect x="3" y="-58" width="17" height="58" rx="8" fill="#1d2b4f"/>
<g transform="rotate(58 0 -58)"><rect x="-26" y="-112" width="52" height="62" rx="20" fill="{color}"/><rect x="-26" y="-84" width="52" height="9" fill="#FFD43B"/>
<rect x="24" y="-108" width="14" height="50" rx="7" fill="{color}" transform="rotate(-50 31 -104)"/>{cabeza("dolor", casco)}</g>
<g transform="rotate(-30 -30 -80)"><rect x="-44" y="-102" width="14" height="44" rx="7" fill="{color}"/><circle cx="-37" cy="-58" r="8" fill="#F2C9A0"/></g>
<g class="tiron"><path d="M-48 -96 l-14 -8 l10 -8 l-16 -8" stroke="#E5484D" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M-40 -60 l-18 2 l8 10 l-18 4" stroke="#E5484D" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
<g transform="translate(70,-6)"><rect x="-10" y="-40" width="110" height="46" rx="20" fill="#eadfc4" stroke="#b29f7a" stroke-width="4"/>
<rect x="34" y="-40" width="18" height="46" fill="#E5484D"/><text x="45" y="-9" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="22" fill="#0D1117">50 KG</text></g></g>'''


def agachado(color, casco, cara="feliz", cola=False, escala=0.85, lado=1):
    # cargando en equipo: rodillas flexionadas, espalda recta, brazos hacia el saco
    pelo = COLA if cola else ''
    return f'''<g transform="scale({escala * lado},{escala})">
<ellipse cx="0" cy="0" rx="36" ry="11" fill="#0006"/>
<path d="M-18 -46 L-26 -24 L-18 0" stroke="#1d2b4f" stroke-width="17" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M10 -46 L20 -24 L12 0" stroke="#1d2b4f" stroke-width="17" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<g transform="translate(0,12)"><rect x="-26" y="-112" width="52" height="62" rx="20" fill="{color}"/><rect x="-26" y="-84" width="52" height="9" fill="#FFD43B"/>
<g transform="rotate(-50 31 -102)"><rect x="24" y="-108" width="14" height="52" rx="7" fill="{color}"/><circle cx="31" cy="-56" r="8" fill="#F2C9A0"/></g>
<rect x="-38" y="-108" width="14" height="46" rx="7" fill="{color}"/>
<g transform="scale({lado},1)">{cabeza(cara, casco, pelo)}</g></g></g>'''


# ---------- mundo: ferretería de noche con camión ----------
w = []
w.append(poly([(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)], "#1b2230"))
for i in range(1, 10):
    a, b = iso(i, 0), iso(i, 10); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0d" stroke-width="2"/>')
    a, b = iso(0, i), iso(10, i); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0d" stroke-width="2"/>')
# calle al frente con línea amarilla
w.append(poly([(0, 8.4, 0), (10, 8.4, 0), (10, 10, 0), (0, 10, 0)], "#11151d"))
for k in range(6):
    w.append(poly([(0.4 + k * 1.7, 9.15, 0), (1.3 + k * 1.7, 9.15, 0), (1.3 + k * 1.7, 9.3, 0), (0.4 + k * 1.7, 9.3, 0)], "#FFC53D"))
w.append(poly([(0, 10, 0), (10, 10, 0), (10, 10, -0.4), (0, 10, -0.4)], "#141922"))
w.append(poly([(10, 0, 0), (10, 10, 0), (10, 10, -0.4), (10, 0, -0.4)], "#0f131a"))
w.append(arbol(0.5, 0.6, 0.9))
# ferretería
w.append(caja(0.6, 0.8, 0, 3.6, 2.4, 1.9, "#FF8A3D", "#d8cbb5", "#b9ab94"))
w.append(caja(0.6, 0.8, 1.9, 3.6, 2.4, 0.08, "#e8590c", "#c24f0b", "#a8440a"))
w.append(poly([(1.5, 3.2, 0), (2.7, 3.2, 0), (2.7, 3.2, 1.2), (1.5, 3.2, 1.2)], "#ffd27a"))   # portón abierto, interior iluminado
for z in (0.35, 0.7, 1.0):
    w.append(linea((1.55, 3.2, z), (2.65, 3.2, z), "#c08a4b", 4))
w.append(poly([(3.0, 3.2, 0.6), (3.9, 3.2, 0.6), (3.9, 3.2, 1.25), (3.0, 3.2, 1.25)], "#ffe8a3"))
w.append(poly([(4.2, 1.2, 0.6), (4.2, 2.5, 0.6), (4.2, 2.5, 1.25), (4.2, 1.2, 1.25)], "#ffe8a3"))
# toldo a rayas sobre el portón
for k in range(6):
    xa = 1.2 + k * 0.5
    w.append(poly([(xa, 3.2, 1.55), (xa + 0.5, 3.2, 1.55), (xa + 0.5, 3.75, 1.3), (xa, 3.75, 1.3)], "#E5484D" if k % 2 == 0 else "#f1f3f5"))
# letrero
a = iso(1.0, 2.0, 2.0)
w.append(poly([(1.0, 2.0, 1.98), (3.9, 2.0, 1.98), (3.9, 2.0, 2.6), (1.0, 2.0, 2.6)], "#0D1117", 'stroke="#FFC53D" stroke-width="4"'))
a = iso(2.45, 2.0, 2.18)
w.append(f'<text transform="translate({a[0]:.0f},{a[1]:.0f}) skewY(30)" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="30" fill="#FFC53D">FERRETERÍA</text>')
# sacos apilados junto a la puerta (25 kg)
w.append(caja(0.7, 3.6, 0, 1.2, 0.9, 0.12, "#c08a4b", "#9c6d39", "#80582d"))
for i, (dx, dy, dz) in enumerate([(0, 0, 0), (0.6, 0, 0), (0, 0.45, 0), (0.6, 0.45, 0), (0.1, 0.2, 0.17), (0.6, 0.2, 0.17)]):
    w.append(saco(0.72 + dx, 3.62 + dy, 0.12 + dz, chico=True))
# camión
w.append(caja(5.0, 0.9, 0.3, 2.8, 1.5, 0.15, "#495057", "#343a40", "#2b3035"))
for (x, y, z) in [(5.15 + 0.75 * i, 0.98 + 0.48 * j, 0.45 + 0.2 * l) for l in range(2) for j in range(3) for i in range(3) if not (l == 1 and i == 0)]:
    w.append(saco(x, y, z))
w.append(caja(5.0, 0.9, 0.45, 2.8, 0.06, 0.45, "#868e96", "#adb5bd", "#868e96"))
w.append(caja(7.9, 0.9, 0.3, 1.3, 1.5, 1.35, "#1FA9E8", "#1677a8", "#1a8fc4"))
w.append(poly([(9.2, 1.05, 1.0), (9.2, 2.25, 1.0), (9.2, 2.25, 1.55), (9.2, 1.05, 1.55)], "#a5d8ff"))
w.append(poly([(8.0, 2.4, 1.0), (8.9, 2.4, 1.0), (8.9, 2.4, 1.5), (8.0, 2.4, 1.5)], "#a5d8ff"))
for (x, y) in [(5.6, 2.4), (7.0, 2.4), (8.6, 2.4)]:
    a = iso(x, y, 0.22)
    w.append(f'<ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="20" ry="24" fill="#111"/><ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="8" ry="10" fill="#868e96"/>')
a = iso(9.2, 1.3, 0.55); w.append(f'<circle cx="{a[0]:.0f}" cy="{a[1]:.0f}" r="9" fill="#FFE066"/>')
a = iso(9.2, 2.1, 0.55); w.append(f'<circle cx="{a[0]:.0f}" cy="{a[1]:.0f}" r="9" fill="#FFE066"/>')
# estantería al fondo derecha
w.append(caja(8.8, 3.6, 0, 0.6, 2.2, 1.6, "#495057", "#343a40", "#2b3035"))
for z in (0.5, 1.0, 1.5):
    for k in range(3):
        w.append(caja(8.85, 3.7 + k * 0.7, z - 0.4, 0.5, 0.5, 0.32, ["#FFC53D", "#1FA9E8", "#E5484D"][k], "#9c7a2a", "#7a6020"))
w.append(farol(4.6, 0.6)); w.append(farol(9.6, 7.8))
w.append(cono(4.9, 8.0)); w.append(cono(1.2, 7.6)); w.append(cono(8.3, 2.95))
w.append(arbol(0.4, 9.0, 0.8)); w.append(arbol(9.5, 0.5, 0.8))

# ---------- tiempos ----------
e = E


def fin(i): return e[i]["inicio"] + e[i]["dur"]


def pal(i, palabra):
    for p in e[i]["palabras"]:
        if p["p"].lower().strip("¿?¡!.,:").startswith(palabra.lower()): return p["t"]
    return e[i]["inicio"]


t_levanta = pal(2, "levanta")
t_tiron = pal(2, "siente")
t_jefe = pal(1, "jefe")
t_baja = pal(1, "bájame")
t_tp0, t_tp1 = e[3]["inicio"] + 0.3, fin(3) - 0.2
t_par0, t_par1 = e[5]["inicio"] + 0.3, fin(5) - 0.3


def tr(p): a = iso(*p); return f"translate({a[0]:.0f}px,{a[1]:.0f}px)"


css_extra = []
P0 = (4.5, 3.0); J = (3.0, 4.7)
a = iso(*P0)
pedro = f'''<g transform="translate({a[0]:.0f},{a[1]:.0f})">
<g class="pa">{mono("#3b5bdb", "#FFD43B", "duda", 0.85)}</g>
<g class="pb">{mono("#3b5bdb", "#FFD43B", "sudor", 0.85, brazo="arriba", saco_hombro=True)}</g>
<g class="pc">{doblado()}</g></g>'''
a = iso(*J)
jefe = f'''<g transform="translate({a[0]:.0f},{a[1]:.0f})"><g class="jefe">
<g class="ja">{mono("#868e96", "#FFFFFF", "manda", 0.9, bigote=True, brazo="apunta")}</g>
<g class="jb">{mono("#868e96", "#FFFFFF", "susto", 0.9, bigote=True)}</g></g></g>'''

# transpaleta (paso 1)
TP0 = (6.4, 3.4); TP1 = (3.6, 6.2)
tpl = []
tpl.append(caja(-0.65, -0.45, 0.06, 1.3, 0.9, 0.13, "#c08a4b", "#9c6d39", "#80582d", f=rel))
for (dx, dy, dz) in [(-0.6, -0.4, 0.19), (0.0, -0.4, 0.19), (-0.6, 0.02, 0.19), (0.0, 0.02, 0.19), (-0.3, -0.2, 0.36)]:
    tpl.append(saco(dx, dy, dz, f=rel, chico=True))
tpl.append(linea((0.65, -0.1, 0.1), (1.05, -0.5, 1.15), "#E5484D", 7, f=rel))
tpl.append(linea((0.65, 0.1, 0.03), (0.65, -0.3, 0.03), "#E5484D", 8, f=rel))
hx, hy = rel(1.05, -0.5, 1.15)
tpl.append(f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="8" fill="#E5484D"/>')
px, py = rel(1.35, -0.75, 0)
tpl.append(f'<g transform="translate({px:.0f},{py:.0f})"><g class="pd">{mono("#3b5bdb", "#FFD43B", "feliz", 0.85, brazo="empuja")}</g></g>')
css_extra.append("@keyframes tpal{" + " ".join(f"{pct(t):.2f}%{{transform:{tr(p)}}}" for t, p in [(0, TP0), (t_tp0, TP0), (t_tp1, TP1), (TOT, TP1)]) + "}")
transpaleta = f'<g class="tpal">{"".join(tpl)}<g class="okmark"><circle cx="0" cy="-120" r="30" fill="#25D366"/><path d="M-13 -120 l9 10 l18 -20" stroke="#0D1117" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g>'

# cargando entre dos (paso 3)
A0 = (7.8, 5.4); A1 = (5.8, 7.4)
par = (f'<g class="par"><g transform="translate(-78,0)"><g class="caminaA">{agachado("#3b5bdb", "#FFD43B", "feliz", lado=1)}</g></g>'
       f'<g transform="translate(78,0)"><g class="caminaB">{agachado("#7048e8", "#FFFFFF", "feliz", cola=True, lado=-1)}</g></g>'
       f'<g transform="translate(0,-62)"><rect x="-56" y="-26" width="112" height="50" rx="22" fill="#eadfc4" stroke="#b29f7a" stroke-width="4"/>'
       f'<rect x="-10" y="-26" width="20" height="50" fill="#1FA9E8"/></g>'
       f'<g class="okmark2"><circle cx="0" cy="-200" r="30" fill="#25D366"/><path d="M-13 -200 l9 10 l18 -20" stroke="#0D1117" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g>')
css_extra.append("@keyframes par{" + " ".join(f"{pct(t):.2f}%{{transform:{tr(p)}}}" for t, p in [(0, A0), (t_par0, A0), (t_par1, A1), (TOT, A1)]) + "}")

# compañero de fondo en la estantería
a = iso(8.2, 4.6, 0)
fondo_mono = f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><g class="trabaja">{mono("#2f9e44", "#FFD43B", "feliz", 0.6)}</g></g>'


# ---------- cámara ----------
def foco(t, p, s):
    px, py = iso(*p)
    return (t, s, -s * (px - 540), -20 - s * (py - 520))


P_truck = (6.4, 1.8, 0.9); P_pedro = (4.4, 3.2, 0.9); P_mid = (3.9, 3.9, 0.9); P_wide = (5, 4.6, 0.3)
cam = [foco(0, P_truck, 1.15), foco(e[1]["inicio"] - 0.1, P_truck, 1.3), foco(e[1]["inicio"] + 0.4, P_wide, 0.98),
       foco(t_jefe - 0.2, (4.8, 4.0, 0.5), 1.12), foco(t_jefe + 0.7, P_mid, 1.5), foco(fin(1), P_mid, 1.6),
       foco(e[2]["inicio"] + 0.3, P_pedro, 1.95), foco(fin(2), P_pedro, 2.05),
       foco(t_tp0, (TP0[0], TP0[1], 0.6), 1.55), foco(t_tp1, (TP1[0], TP1[1], 0.6), 1.65),
       foco(e[4]["inicio"] + 0.3, (TP1[0], TP1[1], 0.4), 1.3), foco(fin(4), (5, 5.5, 0.4), 1.15),
       foco(e[5]["inicio"] + 0.1, (A0[0], A0[1], 1.9), 1.6), foco(t_par1, (A1[0], A1[1], 1.9), 1.75),
       foco(e[6]["inicio"] + 0.3, P_wide, 1.05), foco(e[7]["inicio"], P_wide, 1.0), foco(fin(7), (5, 4.4, 0.4), 0.9), foco(TOT, (5, 4.4, 0.4), 0.9)]
cam_kf = " ".join(f"{pct(t):.2f}%{{transform:translate({x:.0f}px,{y:.0f}px) scale({s})}}" for t, s, x, y in cam)

# ---------- subtítulos karaoke ----------
clave = {0: ["cincuenta", "kilos", "hombro?", "doble"], 1: ["camión", "ferretería", "temuco", "pedro:", "bájame", "hombro."],
         2: ["tirón", "espalda.", "accidente", "trabajo."], 3: ["evita?", "uno:", "carro,", "transpaleta", "carretilla."],
         4: ["dos:", "veinticinco", "kilos.", "veinte", "dieciocho.", "embarazadas,", "nada."],
         5: ["tres:", "reparte", "dos,", "rota", "turnos", "espalda", "recta", "piernas", "flexionadas."],
         6: ["cuatro:", "matriz", "riesgos", "capacita"], 7: ["código", "trabajo,", "doscientos", "once", "h:", "veinticinco", "kilos."],
         8: ["mano?", "matriz", "capacitación.", "base", "segura", "punto", "cl", "minuto."]}
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
        ws = "".join(f'<span class="w{" k" if p["p"].lower() in clave.get(i, []) else ""}" style="animation-delay:{p["t"]:.2f}s">{html.escape(p["p"])}</span> ' for p in trz)
        subs.append(f'<div class="sub cut" style="--i:{a0:.2f}s;--d:{b0 - a0:.2f}s">{ws}</div>')


def pill(txt, bg, fg, t, d, top, chica=False):
    return f'<div class="pill win{" chica" if chica else ""}" style="--i:{t:.2f}s;--d:{d:.2f}s;top:{top}px"><span class="pop" style="animation-delay:{t:.2f}s;background:{bg};color:{fg}">{txt}</span></div>'


AM, NE, RO, AZ, VE = "#FFC53D", "#0D1117", "#E5484D", "#1FA9E8", "#25D366"
t_doble = pal(0, "doble") - 0.1
t_si = pal(2, "si") - 0.1
t_uno = pal(3, "uno") - 0.1
t_max = pal(4, "máximo") - 0.1
t_veinte = pal(4, "veinte") - 0.1
t_emb = pal(4, "embarazadas") - 0.1
t_esp = pal(5, "espalda") - 0.1
t_rota = pal(5, "rota") - 0.1
pills = [
    pill("⚠️ EL DOBLE DE LO QUE PERMITE LA LEY", RO, "#fff", t_doble, fin(0) - t_doble, 1400),
    pill("📍 FERRETERÍA · TEMUCO", AZ, NE, e[1]["inicio"] + 0.5, fin(1) - e[1]["inicio"] - 0.5, 1330),
    pill("⚠️ SACO DE 50 KG · TIRÓN EN LA ESPALDA", RO, "#fff", t_tiron - 0.05, fin(2) - t_tiron + 0.05, 1220),
    pill("✚ SI SE LESIONA: ACCIDENTE DEL TRABAJO", AZ, NE, t_si, fin(2) - t_si, 1330),
    pill("⏱ 4 COSAS · ANTES DE CARGAR", AM, NE, e[3]["inicio"] + 0.2, e[3]["dur"] - 0.2, 1220),
    pill("🛒 1 · CARRO O TRANSPALETA", AM, NE, t_uno, fin(3) - t_uno, 1330),
    pill("📖 Código del Trabajo · art. 211-G", "#ffffff", NE, t_uno + 0.4, fin(3) - t_uno - 0.4, 1440, chica=True),
    pill("🏋️ 25 KG · HOMBRES", AM, NE, t_max, fin(4) - t_max, 1150),
    pill("⚖️ 20 KG · MUJERES Y MENORES DE 18", AM, NE, t_veinte, fin(4) - t_veinte, 1260),
    pill("🚫 EMBARAZADAS · NADA", RO, "#fff", t_emb, fin(4) - t_emb, 1370),
    pill("👥 3 · ENTRE DOS Y CON TÉCNICA", AM, NE, e[5]["inicio"] + 0.2, e[5]["dur"] - 0.2, 1220),
    pill("🔄 ROTA LOS TURNOS", AZ, NE, t_rota, t_esp - t_rota, 1330),
    pill("✅ ESPALDA RECTA · PIERNAS FLEXIONADAS", VE, NE, t_esp, fin(5) - t_esp, 1330),
    pill("📋 4 · EVALÚA EL RIESGO Y CAPACITA", AM, NE, e[6]["inicio"] + 0.2, e[6]["dur"] - 0.2, 1300),
    pill("📖 DS 63 · art. 13", "#ffffff", NE, e[6]["inicio"] + 0.6, e[6]["dur"] - 0.6, 1410, chica=True),
]

# gancho
gancho = f'''<div class="gancho win" style="--i:0s;--d:{e[1]['inicio']:.2f}s">
<div class="gtit">¿Sacos de <span style="color:#F2A33A">50 kilos</span><br>al hombro?</div>
<svg viewBox="-200 -290 400 320" class="gmono"><g class="balancea">{mono("#3b5bdb", "#FFD43B", "sudor", 1.0, brazo="arriba", saco_hombro=True)}</g></svg></div>'''

# burbuja del jefe (escena 1)
burbuja = f'''<div class="burbuja win" style="--i:{t_baja - 0.3:.2f}s;--d:{fin(1) - t_baja + 0.3:.2f}s"><span class="bpop" style="animation-delay:{t_baja - 0.3:.2f}s">🗣️ “¡Bájame esos sacos<br><b style="color:#E5484D">al hombro</b>!”</span></div>'''

# báscula (escena 4)
bascula = f'''<div class="bascula win" style="--i:{e[4]['inicio']:.2f}s;--d:{e[4]['dur']:.2f}s"><div class="bas-card">
<div class="bas-t">2 · MÁXIMO <span style="color:#FFC53D">25 KILOS</span></div>
<svg viewBox="0 0 860 470" width="860" height="470">
<g transform="translate(200,0)"><g class="malo">
<rect x="-150" y="200" width="300" height="130" rx="56" fill="#eadfc4" stroke="#b29f7a" stroke-width="6"/><rect x="-24" y="200" width="48" height="130" fill="#E5484D"/>
<text x="0" y="292" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="62" fill="#0D1117" stroke="#eadfc4" stroke-width="8" paint-order="stroke">50 KG</text>
<path d="M-130 170 L130 360 M130 170 L-130 360" stroke="#E5484D" stroke-width="22" stroke-linecap="round"/></g>
<text x="0" y="420" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="34" fill="#E5484D">✕ A MANO, NO</text></g>
<g transform="translate(630,0)">
<rect x="-110" y="130" width="220" height="110" rx="34" fill="#eadfc4" stroke="#b29f7a" stroke-width="6" class="baja"/>
<rect x="-18" y="130" width="36" height="110" fill="#1FA9E8" class="baja"/>
<text x="0" y="205" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="46" fill="#0D1117" stroke="#eadfc4" stroke-width="7" paint-order="stroke" class="baja">25 KG</text>
<rect x="-170" y="250" width="340" height="40" rx="12" fill="#adb5bd"/><rect x="-150" y="290" width="300" height="80" rx="14" fill="#495057"/>
<rect x="-110" y="302" width="220" height="56" rx="10" fill="#0b1a10"/>
<text x="0" y="345" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="42" fill="#25D366">25,0 kg</text>
<text x="0" y="420" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="34" fill="#25D366">✓ LÍMITE GENERAL</text></g>
</svg></div></div>'''


# técnica (escena 5): vista lateral mal / bien
def lateral(bien):
    if bien:
        return ('<circle cx="0" cy="-196" r="30" fill="#F2C9A0"/><path d="M-30 -206 A30 28 0 0 1 30 -206Z" fill="#FFD43B"/>'
                '<rect x="-20" y="-166" width="40" height="80" rx="16" fill="#3b5bdb"/>'
                '<path d="M-8 -90 L34 -60 L4 -4" stroke="#1d2b4f" stroke-width="20" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                '<rect x="18" y="-120" width="70" height="52" rx="18" fill="#eadfc4" stroke="#b29f7a" stroke-width="4"/>'
                '<path d="M6 -150 L40 -100" stroke="#3b5bdb" stroke-width="14" stroke-linecap="round"/>'
                '<line x1="-34" y1="-226" x2="-34" y2="-80" stroke="#25D366" stroke-width="6" stroke-dasharray="12 10"/>')
    return ('<g transform="rotate(70 0 -90)"><circle cx="0" cy="-196" r="30" fill="#F2C9A0"/><path d="M-30 -206 A30 28 0 0 1 30 -206Z" fill="#FFD43B"/>'
            '<rect x="-20" y="-166" width="40" height="80" rx="16" fill="#3b5bdb"/></g>'
            '<path d="M0 -90 L0 -4" stroke="#1d2b4f" stroke-width="20" stroke-linecap="round"/>'
            '<path d="M80 -100 L120 -40" stroke="#3b5bdb" stroke-width="14" stroke-linecap="round"/>'
            '<rect x="110" y="-52" width="70" height="50" rx="18" fill="#eadfc4" stroke="#b29f7a" stroke-width="4"/>'
            '<path d="M40 -150 q14 -10 0 -20 q-14 -10 0 -20" stroke="#E5484D" stroke-width="6" fill="none"/>')


tecnica = f'''<div class="tecnica win" style="--i:{t_esp - 0.1:.2f}s;--d:{fin(5) - t_esp + 0.1:.2f}s"><div class="tec-card">
<div class="tec-col"><svg viewBox="-60 -250 260 260" width="300" height="300">{lateral(False)}</svg><div class="tec-l" style="background:#E5484D;color:#fff">✕ ESPALDA DOBLADA</div></div>
<div class="tec-col"><svg viewBox="-100 -250 260 260" width="300" height="300">{lateral(True)}</svg><div class="tec-l" style="background:#25D366;color:#0D1117">✓ PIERNAS, NO ESPALDA</div></div>
</div></div>'''

# matriz de riesgos (escena 6)
matriz = f'''<div class="matriz win" style="--i:{e[6]['inicio']:.2f}s;--d:{e[6]['dur']:.2f}s"><div class="mz-card">
<div class="mz-h">📋 MATRIZ DE RIESGOS</div>
<div class="mz-row"><span class="mz-k">Tarea</span><span class="mz-v">Descarga de sacos del camión</span></div>
<div class="mz-row"><span class="mz-k">Riesgo</span><span class="mz-v">Lesión de espalda <span class="mz-tag">ALTO</span></span></div>
<div class="mz-k mz-k2">Medidas</div>
<div class="mz-chk" style="animation-delay:{e[6]['inicio']+0.9:.2f}s">✓ Transpaleta o carro</div>
<div class="mz-chk" style="animation-delay:{e[6]['inicio']+1.5:.2f}s">✓ Máximo 25 kg por persona</div>
<div class="mz-chk" style="animation-delay:{pal(6, 'capacita'):.2f}s">✓ Capacitación al equipo</div>
</div></div>'''

ley = f'''<div class="ley win" style="--i:{e[7]['inicio']+0.2:.2f}s;--d:{e[7]['dur']-0.2:.2f}s"><div class="ley-card">
<div class="ley-h">CÓDIGO DEL TRABAJO · CHILE</div><div class="ley-art">Art. 211-H</div>
<p>"Si la manipulación manual es inevitable y las ayudas mecánicas no pueden usarse, <mark>no se permitirá que se opere con cargas superiores a 25 kilogramos</mark>."</p>
<div class="ley-tag">🇨🇱 Código del Trabajo · Chile · art. 211-H</div><div class="ley-sub">20 kg para mujeres y menores de 18: art. 211-J</div></div></div>'''

t_fase2 = pal(8, "te") - 0.2
minis = "".join(f'<div class="mini" style="animation-delay:{e[8]["inicio"]+0.4+k*0.25:.2f}s"><svg viewBox="-60 -240 120 250" width="150" height="312">{mono(c, h, cara, 1.0, cola=cola)}</svg></div>'
                for k, (c, h, cara, cola) in enumerate([("#3b5bdb", "#FFD43B", "sudor", False), ("#7048e8", "#FFFFFF", "duda", True), ("#868e96", "#FFFFFF", "susto", False)]))
cta = f'''<div class="cta win" style="--i:{e[8]['inicio']:.2f}s;--d:{TOT-e[8]['inicio']:.2f}s"><div class="cta-in">
<div class="logo">{LOGO}</div>
<div class="fase1 win" style="--i:{e[8]['inicio']:.2f}s;--d:{t_fase2-e[8]['inicio']+0.3:.2f}s">
<div class="cta-t">¿En tu bodega se carga<br><span style="color:#F2A33A">a mano</span>?</div>
<div class="minis">{minis}</div></div>
<div class="fase2">
<div class="cta-t2">Te armamos la <span style="color:#F2A33A">matriz de riesgos</span><br>y la capacitación</div>
<div class="cta-band">Cotiza tu matriz de riesgos<br>en <b>basesegura.cl</b></div>
<div class="cta-mail">contacto@basesegura.cl</div></div></div>
<div class="fuente">Fuente: Código del Trabajo (Chile), arts. 211-G, 211-H, 211-I y 211-J · DS 63, arts. 7 y 13 · DT, Ord. N° 1060 (22-03-2019) y Ord. N° 1300 (13-10-2023)</div></div>'''

polvo = "".join(f'<i style="left:{random.randint(20,1040)}px;animation-delay:-{random.random()*6:.2f}s;animation-duration:{5+random.random()*4:.2f}s;opacity:{0.12+random.random()*0.2:.2f}"></i>' for _ in range(30))

m = lambda a, b: f"{pct(a):.2f}%{{opacity:{b}}}"
ocultar = " ".join([m(0, .35), m(e[1]['inicio'] - 0.2, .35), m(e[1]['inicio'] + 0.2, 1), m(e[4]['inicio'], 1), m(e[4]['inicio'] + 0.3, .3),
                    m(fin(4) - 0.1, .3), m(e[5]['inicio'] + 0.2, 1), m(fin(5), 1), m(e[6]['inicio'] + 0.3, .25), m(e[7]['inicio'] - 0.1, .25),
                    m(e[7]['inicio'] + 0.3, .45), m(fin(7) - 0.1, .45), m(e[8]['inicio'] + 0.4, 0), m(TOT, 0)])

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
.shake{{animation:tiembla .09s linear {t_tiron:.2f}s 5 both}}
@keyframes tiembla{{0%{{transform:none}}25%{{transform:translate(12px,-7px)}}50%{{transform:translate(-11px,8px)}}75%{{transform:translate(8px,5px)}}100%{{transform:none}}}}
.polvo{{position:absolute;left:0;right:0;top:440px;height:1000px;overflow:hidden;pointer-events:none;animation:ocultaMundo {TOT}s linear both}}
.polvo i{{position:absolute;top:-20px;width:4px;height:4px;border-radius:50%;background:#cfd8e3;animation-name:cae;animation-timing-function:linear;animation-iteration-count:infinite}}
@keyframes cae{{to{{transform:translate(-60px,1020px)}}}}
.pa{{animation:fuera .01s linear {t_levanta:.2f}s both}}
.pb{{opacity:0;animation:dentro .01s linear {t_levanta:.2f}s both, fuera .01s linear {t_tiron:.2f}s forwards}}
.pc{{opacity:0;animation:dentro .01s linear {t_tiron:.2f}s both, fuera .01s linear {e[3]['inicio']:.2f}s forwards}}
.pb .brazos,.pa{{}}
.tiron{{animation:late .3s ease-in-out infinite alternate}}
.ja{{animation:fuera .01s linear {t_tiron:.2f}s both}}
.jb{{opacity:0;animation:dentro .01s linear {t_tiron:.2f}s both}}
.jefe{{transform-origin:0 0;animation:balancea .8s ease-in-out infinite alternate}}
.tpal{{opacity:0;animation:tpal {TOT}s linear both, dentro .01s linear {e[3]['inicio']:.2f}s forwards}}
.pd{{animation:fuera .01s linear {e[5]['inicio']:.2f}s both}}
.pd .p1{{animation:paso .3s ease-in-out {t_tp0:.2f}s 14 alternate}} .pd .p2{{animation:paso .3s ease-in-out {t_tp0:.2f}s 14 alternate-reverse}}
.okmark{{opacity:0;animation:pop .4s cubic-bezier(.2,1.6,.4,1) {t_tp1:.2f}s both, fuera .2s linear {e[4]['inicio']+0.2:.2f}s forwards}}
.par{{opacity:0;animation:par {TOT}s linear both, dentro .01s linear {e[5]['inicio']:.2f}s forwards}}
.caminaA,.caminaB{{animation:rebota .3s ease-in-out {t_par0:.2f}s 18 alternate}}
@keyframes rebota{{to{{transform:translateY(-8px)}}}}
.okmark2{{opacity:0;animation:pop .4s cubic-bezier(.2,1.6,.4,1) {t_esp:.2f}s both}}
.trabaja{{transform-origin:0 0;animation:balancea .5s ease-in-out infinite alternate}}
.gota{{animation:gotea 1s ease-in infinite}} @keyframes gotea{{from{{transform:none;opacity:1}}to{{transform:translateY(40px);opacity:0}}}}
@keyframes fuera{{to{{opacity:0}}}} @keyframes dentro{{to{{opacity:1}}}} @keyframes aparece{{to{{opacity:1}}}}
.pierna{{transform-box:fill-box;transform-origin:50% 0}}
@keyframes paso{{from{{transform:rotate(-14deg)}}to{{transform:rotate(14deg)}}}}
@keyframes late{{to{{opacity:.45}}}}
{' '.join(css_extra)}
.techo{{position:absolute;left:0;right:0;top:0;height:470px;background:linear-gradient(#0D1117 0,#0D1117dd 55%,#0D111700 100%)}}
.sub{{position:absolute;left:70px;right:70px;top:230px;text-align:center;font-family:Outfit;font-weight:800;font-size:62px;line-height:1.15;text-shadow:0 4px 18px #000;z-index:10}}
.w{{opacity:.22;animation:palabra .18s ease-out both}} .w.k{{color:#F2A33A}}
@keyframes palabra{{from{{opacity:.22;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.pill{{position:absolute;left:30px;right:30px;display:flex;justify-content:center;font-family:Outfit;font-weight:800;font-size:42px;letter-spacing:.3px;z-index:6;text-align:center}}
.pill.chica{{font-size:32px}} .pill.chica .pop{{padding:12px 26px;border:3px solid #0D1117}}
.pill .pop{{display:inline-block;padding:20px 32px;border-radius:60px;box-shadow:0 10px 30px #0008;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
@keyframes pop{{from{{transform:scale(.4);opacity:0}}to{{transform:none;opacity:1}}}}
.gancho{{position:absolute;inset:0}}
.gtit{{position:absolute;left:50px;right:50px;top:480px;text-align:center;font-family:Outfit;font-weight:900;font-size:96px;line-height:1.04;letter-spacing:-2px;text-shadow:0 6px 30px #000;animation:pop .6s cubic-bezier(.2,1.6,.4,1) .1s both}}
.gmono{{position:absolute;left:140px;top:760px;width:800px;height:640px}}
.balancea{{transform-origin:0 0;animation:balancea .6s ease-in-out infinite alternate}}
@keyframes balancea{{from{{transform:rotate(-4deg)}}to{{transform:rotate(4deg) translateY(-6px)}}}}
.burbuja{{position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;z-index:6}}
.bpop{{background:#fff;color:#0D1117;border-radius:40px;padding:26px 40px;text-align:center;font-family:Outfit;font-weight:800;font-size:52px;line-height:1.15;box-shadow:0 20px 50px #000a;animation:pop .5s cubic-bezier(.2,1.6,.4,1) both}}
.bascula,.tecnica,.matriz{{position:absolute;left:0;right:0;display:flex;justify-content:center;z-index:5}}
.bascula{{top:450px}} .tecnica{{top:440px}} .matriz{{top:440px}}
.bas-card{{width:940px;background:#0D1117e6;border:4px solid #2b3447;border-radius:40px;padding:30px 40px 20px;box-shadow:0 30px 80px #000c;text-align:center;animation:subeCard .55s cubic-bezier(.2,1.3,.4,1) {e[4]['inicio']:.2f}s both}}
.bas-t{{font-family:Outfit;font-weight:900;font-size:70px;letter-spacing:-1px}}
.malo{{animation:late .5s ease-in-out infinite alternate}}
.baja{{animation:bajaSaco .6s cubic-bezier(.3,1.4,.5,1) {e[4]['inicio']+0.6:.2f}s both}}
@keyframes bajaSaco{{from{{transform:translateY(-120px);opacity:0}}to{{transform:none;opacity:1}}}}
.tec-card{{display:flex;gap:30px;background:#0D1117fa;border:4px solid #2b3447;border-radius:40px;padding:24px 34px;box-shadow:0 30px 80px #000c;animation:pop .5s cubic-bezier(.2,1.6,.4,1) {t_esp-0.1:.2f}s both}}
.tec-col{{display:flex;flex-direction:column;align-items:center}}
.tec-l{{margin-top:6px;font-family:Outfit;font-weight:800;font-size:30px;padding:10px 20px;border-radius:30px}}
.mz-card{{width:880px;background:#fff;color:#0D1117;border-radius:34px;padding:40px 46px;box-shadow:0 30px 80px #000c;animation:subeCard .55s cubic-bezier(.2,1.3,.4,1) {e[6]['inicio']:.2f}s both}}
.mz-h{{font-family:Outfit;font-weight:900;font-size:54px;margin-bottom:22px}}
.mz-row{{display:flex;gap:20px;align-items:center;border-top:3px solid #e9ecef;padding:16px 0;font-size:36px;font-weight:700}}
.mz-k{{font-family:Outfit;font-weight:800;font-size:28px;color:#6b7280;width:150px;text-transform:uppercase}}
.mz-k2{{border-top:3px solid #e9ecef;padding-top:16px;width:auto}}
.mz-tag{{background:#E5484D;color:#fff;font-family:Outfit;font-weight:800;font-size:28px;padding:6px 16px;border-radius:20px;margin-left:10px}}
.mz-chk{{margin-top:14px;background:#d3f9d8;color:#0b5d1e;font-family:Outfit;font-weight:800;font-size:40px;padding:12px 24px;border-radius:20px;opacity:0;animation:pop .4s cubic-bezier(.2,1.6,.4,1) both}}
.ley{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:5}}
.ley-card{{width:880px;background:#fff;color:#0D1117;border-radius:34px;padding:46px 50px;box-shadow:0 30px 80px #000c;animation:subeCard .6s cubic-bezier(.2,1.3,.4,1) {e[7]['inicio']+0.2:.2f}s both;margin-top:40px}}
@keyframes subeCard{{from{{transform:translateY(900px)}}to{{transform:none}}}}
.ley-h{{background:#0D1117;color:#fff;display:inline-block;font-family:Outfit;font-weight:800;font-size:30px;padding:10px 20px;border-radius:12px;letter-spacing:1px}}
.ley-art{{font-family:Outfit;font-weight:900;font-size:86px;margin:14px 0 8px}}
.ley-card p{{font-size:40px;line-height:1.36;color:#374151}} .ley-card mark{{background:#FFE066;color:#0D1117;padding:0 6px;font-weight:800}}
.ley-tag{{display:inline-block;margin-top:26px;border:3px solid #0D1117;border-radius:40px;padding:10px 22px;font-family:Outfit;font-weight:800;font-size:28px}}
.ley-sub{{margin-top:14px;font-size:28px;color:#4b5563;font-weight:700}}
.cta{{position:absolute;inset:0;background:#0D1117;z-index:8}}
.cta-in{{position:absolute;left:0;right:0;top:420px;display:flex;flex-direction:column;align-items:center;animation:zoomLento {TOT-e[8]['inicio']:.2f}s linear {e[8]['inicio']:.2f}s both}}
@keyframes zoomLento{{from{{transform:scale(.97)}}to{{transform:scale(1.04)}}}}
.logo{{animation:pop .6s cubic-bezier(.2,1.6,.4,1) {e[8]['inicio']+0.1:.2f}s both}}
.fase1{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center}}
.cta-t{{font-family:Outfit;font-weight:900;font-size:76px;line-height:1.06;text-align:center;letter-spacing:-1px}}
.minis{{display:flex;gap:40px;margin-top:30px}} .mini{{opacity:0;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
.fase2{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center;opacity:0;animation:aparece .4s ease-out {t_fase2:.2f}s both}}
.cta-t2{{font-family:Outfit;font-weight:900;font-size:58px;line-height:1.14;text-align:center}}
.cta-band{{margin-top:46px;background:#F2A33A;color:#0D1117;font-family:Outfit;font-weight:800;font-size:50px;line-height:1.2;padding:32px 46px;border-radius:30px;text-align:center;animation:pop .5s cubic-bezier(.2,1.6,.4,1) {pal(8, 'entra')-0.2:.2f}s both}}
.cta-band b{{font-weight:900}}
.cta-mail{{margin-top:34px;font-family:Outfit;font-weight:800;font-size:46px;color:#1FA9E8}}
.fuente{{position:absolute;bottom:420px;left:90px;right:90px;text-align:center;font-size:26px;line-height:1.4;color:#8b949e}}
"""

page = f'''<!doctype html><html><head><meta charset="utf-8"><link href="file:///tmp/bs/fonts/fonts.css" rel="stylesheet"><style>{CSS}</style></head><body>
<div class="grid"></div>
<div class="mundo-wrap"><div class="cam"><div class="shake"><svg width="1080" height="1000" viewBox="0 0 1080 1000" overflow="visible">
{"".join(w)}{fondo_mono}{pedro}{jefe}{transpaleta}{par}</svg></div></div></div>
<div class="polvo">{polvo}</div>
<div class="techo"></div>
{gancho}{burbuja}{bascula}{tecnica}{matriz}{ley}{"".join(pills)}{cta}{"".join(subs)}
<div class="handle"><i></i>@basesegura.cl</div>
</body></html>'''
open(f"{R}/reel.html", "w", encoding="utf-8").write(page)
print("ok", TOT)
