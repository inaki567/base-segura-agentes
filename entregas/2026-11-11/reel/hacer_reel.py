#!/usr/bin/env python3
# Reel 2026-11-11: "Llega el trabajador n° 10: el equipo elige Delegado de SST" (DS 44, art. 66 y 23) — estilo marca/ESTILO-REELS.md
# Uso: python3 hacer_reel.py entregas/2026-11-11/reel   (lee tiempos.json, escribe reel.html)
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




# ---------- mundo: taller mecánico en Temuco, de noche ----------
w = []
w.append(poly([(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)], "#1b2230"))
for i in range(1, 10):
    a, b = iso(i, 0), iso(i, 10); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0d" stroke-width="2"/>')
    a, b = iso(0, i), iso(10, i); w.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#ffffff0d" stroke-width="2"/>')
# patio de cemento frente al taller
w.append(poly([(0.4, 3.0, 0), (7.0, 3.0, 0), (7.0, 7.2, 0), (0.4, 7.2, 0)], "#232b3a"))
# calle al frente con línea amarilla
w.append(poly([(0, 7.6, 0), (10, 7.6, 0), (10, 8.2, 0), (0, 8.2, 0)], "#2a3242"))
w.append(poly([(0, 8.2, 0), (10, 8.2, 0), (10, 10, 0), (0, 10, 0)], "#11151d"))
for k in range(6):
    w.append(poly([(0.4 + k * 1.7, 9.05, 0), (1.3 + k * 1.7, 9.05, 0), (1.3 + k * 1.7, 9.2, 0), (0.4 + k * 1.7, 9.2, 0)], "#FFC53D"))
w.append(poly([(0, 10, 0), (10, 10, 0), (10, 10, -0.4), (0, 10, -0.4)], "#141922"))
w.append(poly([(10, 0, 0), (10, 10, 0), (10, 10, -0.4), (10, 0, -0.4)], "#0f131a"))
w.append(arbol(0.5, 0.5, 0.9)); w.append(arbol(9.5, 0.4, 0.8))
# edificio de fondo con ventanas encendidas
w.append(caja(7.0, 0.3, 0, 2.0, 1.6, 5.0, "#495057", "#3b4350", "#2f3640"))
for zz in (1.0, 2.2, 3.4):
    for xx in (7.3, 8.1):
        col = "#ffe8a3" if random.random() > 0.3 else "#2b3140"
        w.append(poly([(xx, 1.9, zz), (xx + 0.5, 1.9, zz), (xx + 0.5, 1.9, zz + 0.55), (xx, 1.9, zz + 0.55)], col))
    for yy in (0.6, 1.2):
        col = "#ffe8a3" if random.random() > 0.4 else "#2b3140"
        w.append(poly([(9.0, yy, zz), (9.0, yy + 0.4, zz), (9.0, yy + 0.4, zz + 0.55), (9.0, yy, zz + 0.55)], col))
# galpón del taller (portón abierto con auto adentro)
w.append(caja(0.6, 0.6, 0, 5.6, 2.2, 3.2, "#E5484D", "#d8cbb5", "#b9ab94"))
w.append(caja(0.5, 0.5, 3.2, 5.8, 2.4, 0.14, "#E5484D", "#c92a2a", "#a51d1d"))
w.append(poly([(1.0, 2.8, 0), (3.6, 2.8, 0), (3.6, 2.8, 2.2), (1.0, 2.8, 2.2)], "#141a24"))
w.append(poly([(1.0, 2.8, 2.2), (3.6, 2.8, 2.2), (3.6, 2.8, 2.35), (1.0, 2.8, 2.35)], "#868e96"))
# auto en el portón (rampa)
w.append(caja(1.4, 1.6, 0.25, 1.7, 1.1, 0.45, "#1FA9E8", "#1789bd", "#126f99"))
w.append(caja(1.75, 1.75, 0.7, 1.0, 0.8, 0.35, "#a5d8ff", "#74c0fc", "#4dabf7"))
for (xx, yy) in [(1.7, 2.7), (2.8, 2.7)]:
    a = iso(xx, yy, 0.22); w.append(f'<ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="15" ry="18" fill="#111"/>')
# ventana iluminada y puerta de oficina
w.append(poly([(4.2, 2.8, 0.9), (5.6, 2.8, 0.9), (5.6, 2.8, 1.9), (4.2, 2.8, 1.9)], "#ffe8a3"))
w.append(linea((4.9, 2.8, 0.9), (4.9, 2.8, 1.9), "#c9b98a", 4))
w.append(poly([(6.2, 1.2, 0), (6.2, 1.9, 0), (6.2, 1.9, 1.7), (6.2, 1.2, 1.7)], "#5c3b1e"))
# letrero
w.append(poly([(1.0, 2.8, 2.55), (5.0, 2.8, 2.55), (5.0, 2.8, 3.05), (1.0, 2.8, 3.05)], "#0D1117", 'stroke="#FFC53D" stroke-width="4"'))
a = iso(3.0, 2.8, 2.67)
w.append(f'<text transform="translate({a[0]:.0f},{a[1]:.0f}) skewY(30)" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="22" fill="#FFC53D">TALLER · TEMUCO</text>')
# neumáticos apilados
for k in range(3):
    a = iso(6.5, 3.4, 0.2 + k * 0.22)
    w.append(f'<ellipse cx="{a[0]:.0f}" cy="{a[1]:.0f}" rx="30" ry="15" fill="#212529" stroke="#495057" stroke-width="5"/>')
w.append(farol(0.4, 6.6)); w.append(farol(7.4, 7.5))
w.append(cono(6.6, 7.0)); w.append(cono(0.9, 3.4))
w.append(arbol(9.4, 9.0, 0.8)); w.append(arbol(0.4, 9.3, 0.7)); w.append(arbol(9.6, 2.6, 0.75))

# ---------- tiempos ----------
e = E


def fin(i): return e[i]["inicio"] + e[i]["dur"]


def limpia(s): return s.lower().strip("¿?¡!.,:;\"")


def pal(i, palabra, n=1):
    for p in e[i]["palabras"]:
        if limpia(p["p"]).startswith(palabra.lower()):
            n -= 1
            if n == 0: return p["t"]
    raise SystemExit(f"no encontré '{palabra}' en escena {i}")


t_g10 = pal(0, "diez"); t_ojo = pal(0, "ojo")
t_llega = pal(1, "llega"); t_son = pal(1, "diez"); t_preg = pal(1, "pregunta"); t_dele = pal(1, "delegado")
t_uno = pal(2, "uno"); t_cuenta = pal(2, "cuenta"); t_diez2 = pal(2, "diez"); t_25 = pal(2, "veinticinco")
t_dos = pal(3, "dos"); t_eligen = pal(3, "eligen"); t_asam = pal(3, "asamblea"); t_acta = pal(3, "acta")
t_desig = pal(3, "designa"); t_promu = pal(3, "promueve")
t_tres = pal(4, "tres"); t_anos = pal(4, "años"); t_part = pal(4, "participa"); t_desp = pal(4, "después")
t_mas = pal(6, "más"); t_comite = pal(6, "comité"); t_23 = pal(6, "veintitrés")
t_te = pal(7, "te"); t_entra = pal(7, "entra")


def tr(p): a = iso(*p); return f"translate({a[0]:.0f}px,{a[1]:.0f}px)"


def kf(nombre, pares):
    return "@keyframes " + nombre + "{" + " ".join(f"{pct(t):.2f}%{{{v}}}" for t, v in pares) + "}"


css_extra = []


def vis(nombre, tramos):
    pares = [(0, "opacity:1" if tramos[0][0] <= 0 else "opacity:0")]
    final = "opacity:0"
    for a, b in tramos:
        if a > 0: pares += [(a - 0.01, "opacity:0"), (a, "opacity:1")]
        if b >= TOT - 0.02: pares.append((TOT - 0.02, "opacity:1")); final = "opacity:1"
        else: pares += [(b, "opacity:1"), (b + 0.01, "opacity:0")]
    pares.append((TOT, final))
    pares.sort(key=lambda x: x[0])
    css_extra.append(kf(nombre, pares))


# ---------- el equipo (9 + el nuevo) ----------
ESC = 0.62
COL = ["#3b5bdb", "#7048e8", "#868e96", "#1098ad", "#3b5bdb", "#7048e8", "#e8590c", "#868e96", "#1098ad"]
CAS = ["#FFD43B", "#FFFFFF", "#FFD43B", "#FFFFFF", "#FFD43B", "#FFD43B", "#FFFFFF", "#FFD43B", "#FFFFFF"]
POS = [(2.2, 4.4), (3.3, 4.4), (4.4, 4.4), (5.5, 4.4), (1.8, 5.5), (2.9, 5.5), (4.0, 5.5), (5.1, 5.5), (6.2, 5.5)]
DEL = 5          # el delegado elegido (2.9, 5.5)
PREG = 6         # el que pregunta
NUEVO = (5.0, 6.6)
v_ini = e[3]["inicio"] + 0.3; v_fin = t_asam + 0.2   # votación a mano alzada
d_ini = e[4]["inicio"]; d_fin = fin(6)
vis("vVA", [(0, v_ini), (v_fin, TOT)]); vis("vVB", [(v_ini, v_fin)])
vis("vDA", [(0, v_ini), (v_fin, d_ini)]); vis("vDC", [(d_ini, TOT)])

personas = []
for k, (x, y) in enumerate(POS):
    a = iso(x, y)
    cola = k in (1, 6); big = k in (3,)
    cara = "duda" if k == PREG else "feliz"
    if k == DEL:
        inner = (f'<g class="vDA">{mono(COL[k], CAS[k], "feliz", ESC, cola=cola)}</g>'
                 f'<g class="vVB">{mono(COL[k], CAS[k], "feliz", ESC, cola=cola, brazo="arriba")}</g>'
                 f'<g class="vDC">{mono("#25D366", "#FFFFFF", "feliz", ESC, cola=cola, brazo="arriba")}'
                 f'<g transform="translate(0,-150)"><rect x="-70" y="-26" width="140" height="40" rx="20" fill="#25D366" stroke="#0D1117" stroke-width="3"/>'
                 f'<text y="3" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="22" fill="#0D1117">DELEGADO</text></g></g>')
    else:
        inner = (f'<g class="vVA">{mono(COL[k], CAS[k], cara, ESC, cola=cola, bigote=big)}</g>'
                 f'<g class="vVB">{mono(COL[k], CAS[k], "feliz", ESC, cola=cola, bigote=big, brazo="arriba")}</g>')
    personas.append((x + y, f'<g transform="translate({a[0]:.0f},{a[1]:.0f})">{inner}</g>'))

# dueño del taller (bigote, casco blanco, gris)
OW = (7.6, 4.2)
a = iso(*OW)
vis("vOA", [(0, t_preg + 0.6)]); vis("vOB", [(t_preg + 0.6, e[3]["inicio"])]); vis("vOC", [(e[3]["inicio"], TOT)])
dueno = (f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><g class="vOA">{mono("#495057", "#FFFFFF", "feliz", 0.7, bigote=True, brazo="arriba")}</g>'
         f'<g class="vOB">{mono("#495057", "#FFFFFF", "duda", 0.7, bigote=True, brazo="cabeza")}</g>'
         f'<g class="vOC">{mono("#495057", "#FFFFFF", "feliz", 0.7, bigote=True)}</g>'
         f'<g transform="translate(0,-150)"><rect x="-48" y="-24" width="96" height="36" rx="18" fill="#0D1117" stroke="#FFC53D" stroke-width="3"/>'
         f'<text y="2" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="20" fill="#FFC53D">DUEÑO</text></g></g>')
personas.append((OW[0] + OW[1], dueno))

# el trabajador nuevo camina desde la calle
N0 = (8.8, 9.3)
w_ini = e[1]["inicio"] + 0.1; w_fin = t_son - 0.1
nuevo = f'<g class="nuevo">{mono("#E5484D", "#FFD43B", "feliz", ESC)}</g>'
css_extra.append(kf("nuevo", [(0, f"transform:{tr(N0)}"), (w_ini, f"transform:{tr(N0)}"), (w_fin, f"transform:{tr(NUEVO)}"), (TOT, f"transform:{tr(NUEVO)}")]))
personas.append((99, nuevo))
personas.sort(key=lambda q: q[0])
equipo = "".join(p for _, p in personas)

# globos de pregunta
gp = iso(POS[PREG][0], POS[PREG][1], 2.6)
globo_t = (f'<g class="globoT" transform="translate({gp[0]:.0f},{gp[1]:.0f})"><g class="rebota"><rect x="-48" y="-56" width="96" height="80" rx="24" fill="#fff"/>'
           f'<path d="M-10 22 L0 44 L12 22Z" fill="#fff"/><text y="8" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="62" fill="#1FA9E8">?</text></g></g>')
go = iso(OW[0], OW[1], 2.9)
globo_d = (f'<g class="globoD" transform="translate({go[0]:.0f},{go[1]:.0f})"><g class="rebota"><rect x="-48" y="-56" width="96" height="80" rx="24" fill="#FFC53D"/>'
           f'<path d="M-10 22 L0 44 L12 22Z" fill="#FFC53D"/><text y="8" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="62" fill="#0D1117">?</text></g></g>')
vis("vglT", [(t_preg - 0.1, fin(1))]); vis("vglD", [(t_dele, e[2]["inicio"] + 0.3)])

# conteo: números sobre cada persona (1 a 10)
orden = [4, 0, 5, 1, 6, 2, 7, 3, 8, None]
c_ini = t_cuenta + 0.2; c_paso = (t_diez2 - c_ini) / 9
etiquetas = []
for n, k in enumerate(orden):
    x, y = (NUEVO if k is None else POS[k])
    a = iso(x, y, 0)
    t = c_ini + n * c_paso
    etiquetas.append(f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><g class="tag" style="animation-delay:{t:.2f}s,{fin(2)-0.2:.2f}s">'
                     f'<ellipse rx="42" ry="15" fill="none" stroke="#FFC53D" stroke-width="5"/>'
                     f'<g transform="translate(0,-148)"><circle r="25" fill="#FFC53D" stroke="#0D1117" stroke-width="3"/>'
                     f'<text y="10" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="30" fill="#0D1117">{n+1}</text></g></g></g>')
etiquetas = "".join(etiquetas)

# urna de votación junto al dueño (escena 2: la empresa da las facilidades)
UR = (6.9, 4.9)
a = iso(*UR)
urna = (f'<g class="urna" transform="translate({a[0]:.0f},{a[1]:.0f})"><ellipse rx="40" ry="13" fill="#0006"/>'
        f'<rect x="-34" y="-62" width="68" height="62" rx="6" fill="#e9ecef"/><rect x="-34" y="-62" width="68" height="14" fill="#1FA9E8"/>'
        f'<rect x="-16" y="-58" width="32" height="6" rx="3" fill="#0D1117"/><text y="-18" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="18" fill="#0D1117">VOTO</text></g>')
vis("vurna", [(e[3]["inicio"] + 0.3, fin(3))])

# más gente (escena 6) y mesa del Comité Paritario
EXTRA = [(0.9, 6.8), (2.0, 6.8), (3.1, 6.8), (4.2, 6.8), (6.2, 6.6), (1.2, 8.4), (2.3, 8.4), (3.4, 8.4), (4.5, 8.4),
         (5.6, 8.4), (6.7, 8.4), (9.2, 4.6), (9.3, 5.6), (7.8, 8.6), (0.9, 3.6), (6.4, 3.5)]
x_ini = t_mas - 0.2; x_paso = 1.6 / len(EXTRA)
extras = []
for n, (x, y) in enumerate(sorted(EXTRA, key=lambda q: q[0] + q[1])):
    a = iso(x, y)
    c = COL[n % len(COL)]; h = CAS[(n + 1) % len(CAS)]
    personas.append((x + y, f'<g transform="translate({a[0]:.0f},{a[1]:.0f})"><g class="extra" style="animation-delay:{x_ini + n * x_paso:.2f}s">{mono(c, h, "feliz", 0.55, cola=(n % 3 == 0))}</g></g>'))
personas.sort(key=lambda q: q[0])
equipo = "".join(p for _, p in personas)
extras = ""
ME = (8.1, 6.3)
mesa = [caja(7.5, 5.9, 0.55, 1.3, 0.8, 0.1, "#c08a4b", "#9c6d39", "#80582d")]
for (xx, yy) in [(7.55, 5.95), (8.75, 5.95), (7.55, 6.65), (8.75, 6.65)]:
    mesa.append(linea((xx, yy, 0), (xx, yy, 0.55), "#80582d", 6))
for (xx, yy) in [(7.7, 5.55), (8.15, 5.55), (8.6, 5.55), (7.7, 7.05), (8.15, 7.05), (8.6, 7.05)]:
    mesa.append(caja(xx - 0.15, yy - 0.15, 0, 0.3, 0.3, 0.32, "#1FA9E8", "#1789bd", "#126f99"))
ml = iso(8.1, 6.3, 2.3)
mesa_l = (f'<g class="mesa" style="animation-delay:{t_comite - 0.1:.2f}s"><g transform="translate({ml[0]:.0f},{ml[1]:.0f})"><rect x="-150" y="-30" width="300" height="52" rx="26" fill="#1FA9E8" stroke="#0D1117" stroke-width="3"/>'
            f'<text y="5" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="28" fill="#0D1117">COMITÉ PARITARIO</text></g></g>')
mesa = f'<g class="mesa" style="animation-delay:{t_comite - 0.1:.2f}s">{"".join(mesa)}</g>'


# ---------- cámara ----------
def foco(t, p, s):
    px, py = iso(*p)
    return (t, s, -s * (px - 540), -20 - s * (py - 520))


P_wide = (5.0, 5.2, 0.6); P_grp = (4.3, 5.3, 0.8); P_preg = (4.0, 5.3, 1.2); P_own = (7.2, 4.4, 1.2)
P_del = (3.2, 5.4, 1.1); P_big = (5.0, 6.0, 0.4)
cam = [foco(0, P_grp, 1.3), foco(e[1]["inicio"] - 0.1, P_grp, 1.35), foco(e[1]["inicio"] + 0.5, P_wide, 0.95),
       foco(w_fin, P_grp, 1.15), foco(t_preg, P_preg, 1.45), foco(t_dele + 0.2, P_own, 1.5), foco(fin(1), P_own, 1.6),
       foco(e[2]["inicio"] + 0.4, P_grp, 1.1), foco(fin(2), P_grp, 1.2),
       foco(e[3]["inicio"] + 0.4, (4.8, 5.0, 0.8), 1.05), foco(t_acta, (4.6, 5.0, 0.8), 1.15), foco(t_desig + 0.3, P_own, 1.4), foco(fin(3), P_own, 1.5),
       foco(e[4]["inicio"] + 0.4, P_del, 1.6), foco(fin(4), P_del, 1.75),
       foco(e[5]["inicio"] + 0.4, P_wide, 1.0), foco(fin(5), P_wide, 1.05),
       foco(e[6]["inicio"] + 0.5, P_wide, 1.0), foco(t_mas + 1.8, P_big, 0.88), foco(fin(6), P_big, 0.95),
       foco(TOT, P_big, 0.95)]
cam_kf = " ".join(f"{pct(t):.2f}%{{transform:translate({x:.0f}px,{y:.0f}px) scale({s})}}" for t, s, x, y in cam)

# ---------- subtítulos karaoke ----------
clave = {0: {"10", "ojo", "cambia"}, 1: {"temuco", "nuevo", "10", "delegado", "seguridad"},
         2: {"uno", "cuenta", "10", "25", "comité", "paritario", "delegado"},
         3: {"dos", "trabajadores", "asamblea", "acta", "designa", "promueve", "facilidades"},
         4: {"tres", "2 años", "gestión", "preventiva", "nuevo"},
         5: {"decreto", "supremo", "44", "66"},
         6: {"25", "comité", "paritario", "23"},
         7: {"creciendo", "ds", "44", "basesegura.cl", "minuto", "gratis"}}
PATRONES = [(["base", "segura", "punto", "cl"], "basesegura.cl"), (["d", "s"], "DS"), (["cuarenta", "y", "cuatro"], "44"),
            (["sesenta", "y", "seis"], "66"), (["veinticinco"], "25"), (["veintitrés"], "23"), (["diez"], "10"),
            (["dos", "años"], "2 años")]
subs = []
for i, ee in enumerate(E):
    ps = list(ee["palabras"]); trozos, cur = [], []
    for patron, unido in PATRONES:
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
        b0 = trozos[k + 1][0]["t"] - 0.05 if k + 1 < len(trozos) else (E[i + 1]["inicio"] if i + 1 < len(E) else TOT)
        ws = "".join(f'<span class="w{" k" if limpia(p["p"]) in clave.get(i, set()) else ""}" style="animation-delay:{p["t"]:.2f}s">{html.escape(p["p"])}</span> ' for p in trz)
        subs.append(f'<div class="sub cut" style="--i:{a0:.2f}s;--d:{b0 - a0:.2f}s">{ws}</div>')


def pill(txt, bg, fg, t, d, top, chica=False):
    return f'<div class="pill win{" chica" if chica else ""}" style="--i:{t:.2f}s;--d:{d:.2f}s;top:{top}px"><span class="pop" style="animation-delay:{t:.2f}s;background:{bg};color:{fg}">{txt}</span></div>'


AM, NE, RO, AZ, VE = "#FFC53D", "#0D1117", "#E5484D", "#1FA9E8", "#25D366"
pills = [
    pill("⚠️ OJO: ALGO CAMBIA", RO, "#fff", t_ojo - 0.1, fin(0) - t_ojo + 0.1, 1420),
    pill("👥 10 PERSONAS EN EL TALLER", AZ, NE, t_son - 0.1, fin(1) - t_son + 0.1, 1330),
    pill("⏱ 3 COSAS · PARA HACER YA", AM, NE, e[2]["inicio"] + 0.1, e[2]["dur"] - 0.1, 1190),
    pill("🔢 1 · CUENTA A TU EQUIPO", AM, NE, t_uno - 0.1, fin(2) - t_uno + 0.1, 1300),
    pill("🦺 10 A 25 + SIN COMITÉ = DELEGADO", AZ, NE, t_25 - 0.1, fin(2) - t_25 + 0.1, 1410),
    pill("🗳️ 2 · LO ELIGE EL EQUIPO", AM, NE, t_dos - 0.1, fin(3) - t_dos + 0.1, 1210),
    pill("📝 EN ASAMBLEA Y CON ACTA", AZ, NE, t_asam - 0.1, t_desig - t_asam - 0.1, 1315),
    pill("✋ LA EMPRESA NO LO DESIGNA", RO, "#fff", t_desig - 0.1, fin(3) - t_desig + 0.1, 1315),
    pill("✅ PROMUEVE Y DA FACILIDADES", VE, NE, t_promu - 0.1, fin(3) - t_promu + 0.1, 1420),
    pill("📅 3 · DURA HASTA 2 AÑOS", AM, NE, t_tres - 0.1, fin(4) - t_tres + 0.1, 1210),
    pill("📋 PARTICIPA EN LA GESTIÓN PREVENTIVA", AZ, NE, t_part - 0.1, fin(4) - t_part + 0.1, 1315),
    pill("🔁 LUEGO SE ELIGE DE NUEVO", VE, NE, t_desp - 0.1, fin(4) - t_desp + 0.1, 1420),
    pill("⚠️ MÁS DE 25 PERSONAS", RO, "#fff", t_mas - 0.1, fin(6) - t_mas + 0.1, 1220),
    pill("👥 → COMITÉ PARITARIO", AZ, NE, t_comite - 0.1, fin(6) - t_comite + 0.1, 1325),
    pill("📖 DS 44 · art. 23", "#ffffff", NE, t_23 - 0.1, fin(6) - t_23 + 0.1, 1435, chica=True),
]

# contador de personas (HUD)
cnt_kf = kf("cnt", [(0, "--n:10"), (t_cuenta, "--n:10"), (t_cuenta + 0.05, "--n:0"), (c_ini - 0.01, "--n:0"),
                    (c_ini + 9 * c_paso, "--n:10"), (t_mas, "--n:10"), (t_mas + 1.7, "--n:26"), (TOT, "--n:26")])
css_extra.append(cnt_kf)
vis("vcnt", [(t_son - 0.1, t_asam - 0.3), (e[4]["inicio"], fin(4)), (e[6]["inicio"], fin(6))])
contador = '<div class="cont"><span class="cont-ico">👷</span><span class="cont-n"></span><span class="cont-l">PERSONAS<br>EN EL TALLER</span></div>'

# gancho
gancho = f'''<div class="gancho win" style="--i:0s;--d:{e[1]['inicio']:.2f}s">
<div class="gtit">¿Contratas al trabajador <span style="color:#F2A33A">N° 10</span>?</div>
<div class="gsub">¿Qué hay que hacer <span style="color:#E5484D">ahora</span>?</div>
<svg viewBox="-200 -290 400 320" class="gmono"><g class="balancea">{mono("#495057", "#FFFFFF", "preocupa", 1.0, bigote=True, brazo="cabeza")}</g></svg>
<div class="gnum"><span class="g9">9</span><span class="g10">10</span><div class="gnl">TRABAJADORES</div></div></div>'''

# acta de elección (escena 3)
acta = f'''<div class="acta win" style="--i:{t_asam - 0.2:.2f}s;--d:{t_desig - t_asam + 0.1:.2f}s"><div class="acta-card">
<div class="acta-h">📝 ACTA DE ELECCIÓN</div>
<div class="acta-t">Delegado de Seguridad y<br>Salud en el Trabajo</div>
<div class="acta-r"><span>Lugar</span><b>Taller · Temuco</b></div>
<div class="acta-r"><span>Asamblea</span><b>10 personas trabajadoras</b></div>
<div class="acta-r"><span>Votos</span><b class="votos">{"".join(f'<i style="animation-delay:{t_asam + 0.2 + k*0.08:.2f}s">✋</i>' for k in range(10))}</b></div>
<div class="acta-r"><span>Elegido</span><b class="elegido">Delegado de SST ✔</b></div>
<svg class="firma" viewBox="0 0 400 90" width="400" height="90"><path d="M10 60 C40 10 60 80 90 40 S140 20 160 55 S220 70 240 30 S300 40 320 60 S370 30 390 45" stroke="#1FA9E8" stroke-width="6" fill="none" stroke-linecap="round"/></svg>
<div class="acta-f">Firma de los asistentes</div></div></div>'''

# calendario (escena 4)
cal = f'''<div class="cal win" style="--i:{t_anos - 0.3:.2f}s;--d:{fin(4) - t_anos + 0.3:.2f}s"><div class="cal-card">
<div class="cal-h">📅 MANDATO</div><div class="cal-y"></div><div class="cal-l">hasta 2 años</div></div></div>'''

ley = f'''<div class="ley win" style="--i:{e[5]['inicio']+0.1:.2f}s;--d:{e[5]['dur']-0.1:.2f}s"><div class="ley-card">
<div class="ley-h">DS 44 · CHILE</div><div class="ley-art">Art. 66</div>
<p>Donde "laboren <b>entre 10 y hasta 25 personas trabajadoras</b>" y "no funcionare un Comité Paritario", se elige un Delegado de SST.</p>
<p class="p2">"La entidad empleadora <mark>deberá promover y otorgar las facilidades necesarias</mark> para la realización de esta elección."</p>
<div class="ley-tag">🇨🇱 DS 44 · Chile · art. 66</div></div></div>'''

minis = "".join(f'<div class="mini" style="animation-delay:{e[7]["inicio"]+0.4+k*0.2:.2f}s"><svg viewBox="-60 -240 120 250" width="130" height="270">{mono(c, h, cara, 1.0, cola=cola, bigote=big, brazo=br)}</svg></div>'
                for k, (c, h, cara, cola, big, br) in enumerate([("#495057", "#FFFFFF", "feliz", False, True, "normal"), ("#25D366", "#FFFFFF", "feliz", True, False, "arriba"),
                                                                 ("#E5484D", "#FFD43B", "feliz", False, False, "normal"), ("#7048e8", "#FFFFFF", "feliz", True, False, "normal")]))
cta = f'''<div class="cta win" style="--i:{e[7]['inicio']:.2f}s;--d:{TOT-e[7]['inicio']:.2f}s"><div class="cta-in">
<div class="logo">{LOGO}</div>
<div class="fase1 win" style="--i:{e[7]['inicio']:.2f}s;--d:{t_te-e[7]['inicio']+0.3:.2f}s">
<div class="cta-t">¿Tu equipo está<br><span style="color:#F2A33A">creciendo</span>?</div>
<div class="minis">{minis}</div></div>
<div class="fase2">
<div class="cta-t2">Dejamos al día lo que pide<br>el <span style="color:#F2A33A">DS 44</span> para tu tamaño</div>
<div class="cta-p">Delegado · matriz de riesgos · <b>y más</b></div>
<div class="cta-band">Cotiza tu diagnóstico gratis<br>en <b>basesegura.cl</b></div>
<div class="cta-mail">contacto@basesegura.cl</div></div></div>
<div class="fuente">Fuente: DS 44 de 2023 (Chile), arts. 23, 64 y 66 · texto oficial en previsionsocial.gob.cl (consultado el 11-11-2026)</div></div>'''

lluvia = "".join(f'<i style="left:{random.randint(0,1100)}px;animation-delay:-{random.random()*2:.2f}s;animation-duration:{1.1+random.random()*0.8:.2f}s;opacity:{0.08+random.random()*0.14:.2f}"></i>' for _ in range(40))

m = lambda a, b: f"{pct(a):.2f}%{{opacity:{b}}}"
ocultar = " ".join([m(0, .3), m(e[1]['inicio'] - 0.2, .3), m(e[1]['inicio'] + 0.2, 1), m(t_asam - 0.5, 1), m(t_asam - 0.2, .3),
                    m(t_desig - 0.2, .3), m(t_desig + 0.1, 1), m(e[5]['inicio'], 1), m(e[5]['inicio'] + 0.3, .25),
                    m(fin(5) - 0.1, .25), m(e[6]['inicio'] + 0.2, 1), m(fin(6) - 0.1, 1), m(e[7]['inicio'] + 0.4, 0), m(TOT, 0)])

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
.lluvia{{position:absolute;left:0;right:0;top:440px;height:1000px;overflow:hidden;pointer-events:none;animation:ocultaMundo {TOT}s linear both}}
.lluvia i{{position:absolute;top:-60px;width:2px;height:46px;background:linear-gradient(#cfd8e300,#cfd8e3);transform:rotate(12deg);animation-name:llueve;animation-timing-function:linear;animation-iteration-count:infinite}}
@keyframes llueve{{to{{transform:translate(-220px,1080px) rotate(12deg)}}}}
.nuevo{{transform-origin:0 0;animation:nuevo {TOT}s linear both}}
.nuevo .p1{{animation:paso .28s ease-in-out {w_ini:.2f}s {max(1, int((w_fin-w_ini)/0.28))} alternate}} .nuevo .p2{{animation:paso .28s ease-in-out {w_ini:.2f}s {max(1, int((w_fin-w_ini)/0.28))} alternate-reverse}}
.vVA{{animation:vVA {TOT}s linear both}} .vVB{{animation:vVB {TOT}s linear both}} .vDA{{animation:vDA {TOT}s linear both}} .vDC{{animation:vDC {TOT}s linear both}}
.vOA{{animation:vOA {TOT}s linear both}} .vOB{{animation:vOB {TOT}s linear both}} .vOC{{animation:vOC {TOT}s linear both}}
.globoT{{animation:vglT {TOT}s linear both}} .globoD{{animation:vglD {TOT}s linear both}}
.rebota{{animation:rebota .5s ease-in-out infinite alternate}} @keyframes rebota{{to{{transform:translateY(-12px)}}}}
.urna{{animation:vurna {TOT}s linear both}}
.tag{{opacity:0;transform-box:fill-box;animation:tagpop .4s cubic-bezier(.2,1.6,.4,1) both,fuera .25s linear forwards}}
@keyframes tagpop{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:none}}}}
.extra{{opacity:0;animation:extrapop .45s cubic-bezier(.2,1.6,.4,1) both}}
@keyframes extrapop{{from{{opacity:0;transform:translateY(-80px)}}to{{opacity:1;transform:none}}}}
.mesa{{opacity:0;animation:aparece .4s ease-out both}}
@keyframes fuera{{to{{opacity:0}}}} @keyframes aparece{{to{{opacity:1}}}}
.pierna{{transform-box:fill-box;transform-origin:50% 0}}
@keyframes paso{{from{{transform:rotate(-16deg)}}to{{transform:rotate(16deg)}}}}
@keyframes late{{to{{opacity:.35}}}}
.gota{{animation:gotea 1s ease-in infinite}} @keyframes gotea{{from{{transform:none;opacity:1}}to{{transform:translateY(40px);opacity:0}}}}
{chr(10).join(css_extra)}
.techo{{position:absolute;left:0;right:0;top:0;height:470px;background:linear-gradient(#0D1117 0,#0D1117dd 55%,#0D111700 100%)}}
.sub{{position:absolute;left:70px;right:70px;top:230px;text-align:center;font-family:Outfit;font-weight:800;font-size:62px;line-height:1.15;text-shadow:0 4px 18px #000;z-index:10}}
.w{{opacity:.22;animation:palabra .18s ease-out both}} .w.k{{color:#F2A33A}}
@keyframes palabra{{from{{opacity:.22;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.pill{{position:absolute;left:30px;right:30px;display:flex;justify-content:center;font-family:Outfit;font-weight:800;font-size:42px;line-height:1.15;letter-spacing:.3px;z-index:6;text-align:center}}
.pill.chica{{font-size:32px}} .pill.chica .pop{{padding:12px 26px;border:3px solid #0D1117}}
.pill .pop{{display:inline-block;max-width:1000px;padding:20px 34px;border-radius:60px;box-shadow:0 10px 30px #0008;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
@keyframes pop{{from{{transform:scale(.4);opacity:0}}to{{transform:none;opacity:1}}}}
@property --n{{syntax:'<integer>';inherits:true;initial-value:0}}
@property --y{{syntax:'<integer>';inherits:true;initial-value:2026}}
.cont{{position:absolute;left:50px;top:470px;z-index:5;display:flex;align-items:center;gap:14px;background:#0D1117e6;border:4px solid #FFC53D;border-radius:30px;padding:12px 24px;box-shadow:0 10px 30px #0009;animation:cnt {TOT}s linear both,vcnt {TOT}s linear both}}
.cont-ico{{font-size:48px}}
.cont-n{{font-family:Outfit;font-weight:900;font-size:80px;line-height:1;color:#FFC53D;counter-reset:n var(--n);min-width:96px;text-align:center}}
.cont-n::after{{content:counter(n)}}
.cont-l{{font-family:Outfit;font-weight:800;font-size:24px;line-height:1.1;color:#c9d1d9}}
.gancho{{position:absolute;inset:0}}
.gtit{{position:absolute;left:50px;right:50px;top:440px;text-align:center;font-family:Outfit;font-weight:900;font-size:100px;line-height:1.02;letter-spacing:-2px;text-shadow:0 6px 30px #000;animation:pop .6s cubic-bezier(.2,1.6,.4,1) .1s both}}
.gsub{{position:absolute;left:50px;right:50px;top:670px;text-align:center;font-family:Outfit;font-weight:800;font-size:56px;text-shadow:0 6px 30px #000;animation:pop .6s cubic-bezier(.2,1.6,.4,1) .5s both}}
.gmono{{position:absolute;left:-120px;top:800px;width:1000px;height:760px}}
.balancea{{transform-origin:0 0;animation:balancea .6s ease-in-out infinite alternate}}
@keyframes balancea{{from{{transform:rotate(-3deg)}}to{{transform:rotate(3deg) translateY(-6px)}}}}
.gnum{{position:absolute;left:640px;top:880px;width:330px;height:330px;border-radius:50%;background:#0D1117;border:10px solid #FFC53D;box-shadow:0 20px 60px #000c;display:flex;align-items:center;justify-content:center;animation:pop .5s cubic-bezier(.2,1.6,.4,1) .3s both}}
.gnum span{{position:absolute;font-family:Outfit;font-weight:900;font-size:190px;line-height:1;top:44px}}
.g9{{color:#c9d1d9;animation:fuera .2s linear {t_g10-0.15:.2f}s forwards}}
.g10{{color:#FFC53D;opacity:0;animation:pop .45s cubic-bezier(.2,1.6,.4,1) {t_g10-0.1:.2f}s both}}
.gnl{{position:absolute;bottom:52px;font-family:Outfit;font-weight:800;font-size:28px;color:#c9d1d9;letter-spacing:1px}}
@keyframes subeCard{{from{{transform:translateY(900px)}}to{{transform:none}}}}
.acta{{position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;z-index:5}}
.acta-card{{width:860px;background:#fffdf5;color:#0D1117;border-radius:30px;padding:36px 48px;box-shadow:0 30px 80px #000c;animation:subeCard .55s cubic-bezier(.2,1.3,.4,1) {t_asam-0.2:.2f}s both}}
.acta-h{{display:inline-block;background:#1FA9E8;color:#0D1117;font-family:Outfit;font-weight:800;font-size:34px;padding:10px 24px;border-radius:14px}}
.acta-t{{font-family:Outfit;font-weight:900;font-size:50px;line-height:1.1;margin:18px 0 18px}}
.acta-r{{display:flex;justify-content:space-between;align-items:center;border-bottom:3px dashed #ced4da;padding:12px 0;font-size:34px}}
.acta-r span{{color:#6b7280;font-weight:700}} .acta-r b{{font-family:Outfit;font-weight:800}}
.votos i{{font-style:normal;font-size:32px;opacity:0;animation:aparece .2s linear both}}
.elegido{{color:#1a9b4b;opacity:0;animation:aparece .3s linear {t_acta+0.4:.2f}s both}}
.firma{{display:block;margin:16px auto 0}} .firma path{{stroke-dasharray:700;stroke-dashoffset:700;animation:firma 1s ease-out {t_acta-0.2:.2f}s forwards}}
@keyframes firma{{to{{stroke-dashoffset:0}}}}
.acta-f{{text-align:center;border-top:3px solid #0D1117;width:440px;margin:0 auto;padding-top:8px;font-size:26px;color:#6b7280;font-weight:700}}
.cal{{position:absolute;right:50px;top:470px;z-index:5}}
.cal-card{{width:330px;background:#fff;color:#0D1117;border-radius:28px;overflow:hidden;box-shadow:0 20px 60px #000c;text-align:center;animation:pop .5s cubic-bezier(.2,1.6,.4,1) {t_anos-0.3:.2f}s both}}
.cal-h{{background:#E5484D;color:#fff;font-family:Outfit;font-weight:800;font-size:32px;padding:12px}}
.cal-y{{font-family:Outfit;font-weight:900;font-size:100px;line-height:1.1;padding-top:8px;counter-reset:y var(--y);animation:anios 2.4s cubic-bezier(.3,.7,.3,1) {t_anos+0.1:.2f}s both}}
.cal-y::after{{content:counter(y)}}
@keyframes anios{{from{{--y:2026}}to{{--y:2028}}}}
.cal-l{{font-family:Outfit;font-weight:800;font-size:32px;padding:0 0 18px;color:#E5484D}}
.ley{{position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;z-index:5}}
.ley-card{{width:900px;background:#fff;color:#0D1117;border-radius:34px;padding:44px 52px;box-shadow:0 30px 80px #000c;animation:subeCard .6s cubic-bezier(.2,1.3,.4,1) {e[5]['inicio']+0.1:.2f}s both}}
.ley-h{{background:#0D1117;color:#fff;display:inline-block;font-family:Outfit;font-weight:800;font-size:32px;padding:10px 22px;border-radius:12px;letter-spacing:1px}}
.ley-art{{font-family:Outfit;font-weight:900;font-size:96px;margin:12px 0 8px}}
.ley-card p{{font-size:40px;line-height:1.34;color:#374151}} .ley-card mark{{background:#FFE066;color:#0D1117;padding:0 6px;font-weight:800}}
.ley-card b{{color:#0D1117}}
.ley-card .p2{{margin-top:20px}}
.ley-tag{{display:inline-block;margin-top:26px;border:3px solid #0D1117;border-radius:40px;padding:10px 22px;font-family:Outfit;font-weight:800;font-size:30px}}
.cta{{position:absolute;inset:0;background:#0D1117;z-index:8}}
.cta-in{{position:absolute;left:0;right:0;top:420px;display:flex;flex-direction:column;align-items:center;animation:zoomLento {TOT-e[7]['inicio']:.2f}s linear {e[7]['inicio']:.2f}s both}}
@keyframes zoomLento{{from{{transform:scale(.97)}}to{{transform:scale(1.03)}}}}
.logo{{animation:pop .6s cubic-bezier(.2,1.6,.4,1) {e[7]['inicio']+0.1:.2f}s both}}
.fase1{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center}}
.cta-t{{font-family:Outfit;font-weight:900;font-size:80px;line-height:1.06;text-align:center;letter-spacing:-1px}}
.minis{{display:flex;gap:30px;margin-top:30px}} .mini{{opacity:0;animation:pop .45s cubic-bezier(.2,1.6,.4,1) both}}
.fase2{{position:absolute;top:250px;left:0;right:0;display:flex;flex-direction:column;align-items:center;opacity:0;animation:aparece .4s ease-out {t_te-0.1:.2f}s both}}
.cta-t2{{font-family:Outfit;font-weight:900;font-size:62px;line-height:1.14;text-align:center;padding:0 50px}}
.cta-p{{margin-top:18px;font-family:Outfit;font-weight:800;font-size:44px;color:#c9d1d9}} .cta-p b{{color:#25D366}}
.cta-band{{margin-top:44px;background:#F2A33A;color:#0D1117;font-family:Outfit;font-weight:800;font-size:52px;line-height:1.2;padding:30px 46px;border-radius:30px;text-align:center;animation:pop .5s cubic-bezier(.2,1.6,.4,1) {t_entra-0.2:.2f}s both}}
.cta-band b{{font-weight:900}}
.cta-mail{{margin-top:30px;font-family:Outfit;font-weight:800;font-size:46px;color:#1FA9E8}}
.fuente{{position:absolute;bottom:420px;left:90px;right:90px;text-align:center;font-size:25px;line-height:1.4;color:#8b949e}}
"""

page = f'''<!doctype html><html><head><meta charset="utf-8"><link href="file:///tmp/bs/fonts/fonts.css" rel="stylesheet"><style>{CSS}</style></head><body>
<div class="grid"></div>
<div class="mundo-wrap"><div class="cam"><svg width="1080" height="1000" viewBox="0 0 1080 1000" overflow="visible">
{"".join(w)}{urna}{mesa}{etiquetas}{equipo}{extras}{globo_t}{globo_d}{mesa_l}</svg></div></div>
<div class="lluvia">{lluvia}</div>
<div class="techo"></div>
{contador}{gancho}{acta}{cal}{ley}{"".join(pills)}{cta}{"".join(subs)}
<div class="handle"><i></i>@basesegura.cl</div>
</body></html>'''
open(f"{R}/reel.html", "w", encoding="utf-8").write(page)
print("ok", TOT)
