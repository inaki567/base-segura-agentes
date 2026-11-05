#!/usr/bin/env python3
"""Arma un reel completo de Base Segura a partir de reel/guion.json.

Uso:  python3 herramientas/armar-reel.py reel/guion.json reel/            (todo automático, plantilla simple)
      python3 herramientas/armar-reel.py reel/guion.json reel/ --voz      (solo voz + reel/tiempos.json)
      python3 herramientas/armar-reel.py reel/guion.json reel/ --grabar   (graba TU reel/reel.html y mezcla voz + efectos)

Flujo recomendado (estilo de marca/ESTILO-REELS.md): --voz, luego escribir reel/reel.html a mano usando
reel/tiempos.json (inicio, duración y tiempo de cada palabra por escena) y al final --grabar.

Hace todo: voz en off (Piper, sin internet), reel.html con personajes y
animaciones sincronizadas con la voz, grabación del video y mezcla con voz
y efectos de sonido. Deja reel/reel.html, reel/voz.wav y reel/reel.mp4.

guion.json:
{
  "voz": "es_MX-claude-high",          (opcional; ver VOCES)
  "escenas": [
    {
      "voz": "Texto que dice el narrador (frases cortas).",
      "texto": "TEXTO GRANDE EN PANTALLA",       (máx. ~8 palabras)
      "resalta": ["PALABRA"],                     (opcional: en azul/naranjo)
      "fondo": "oscuro|azul|blanco|naranjo",
      "personaje": "mascota|trabajador|ninguno",
      "pose": "habla|alerta|agachado|cae|ok|senala|piensa",
      "efecto": "temblor|zoom|ninguno",           (temblor sacude la escena)
      "sfx": "temblor|golpe|whoosh|alarma|pop|ding|error|",
      "norma": "DS 44, art. 15",                  (opcional: caja LO EXIGE)
      "cta": false                                (true = cierre con WhatsApp)
    }
  ]
}
"""
import html, json, os, subprocess, sys, tarfile, urllib.request, wave

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
VOCES = {
    "es_MX-claude-high": "Masculina, joven, latina (por defecto)",
    "es_ES-davefx-medium": "Masculina, acento de España",
}
URL_VOZ = "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-{v}.tar.bz2"
DIR_VOCES = "/tmp/voces"
FPS = 30
PAUSA = 0.35  # segundos de aire entre escenas

COL = {"negro": "#0D1117", "azul": "#1FA9E8", "naranjo": "#F2A33A", "blanco": "#FFFFFF", "wsp": "#25D366"}
FONDOS = {
    "oscuro": (COL["negro"], "#FFFFFF", COL["azul"]),
    "azul": (COL["azul"], "#FFFFFF", COL["negro"]),
    "blanco": ("#FFFFFF", COL["negro"], COL["azul"]),
    "naranjo": (COL["naranjo"], COL["negro"], "#FFFFFF"),
}


def sh(*cmd):
    subprocess.run(cmd, check=True)


def asegurar_voz(v):
    modelo = f"{DIR_VOCES}/vits-piper-{v}/{v}.onnx"
    if not os.path.exists(modelo):
        os.makedirs(DIR_VOCES, exist_ok=True)
        tar = f"{DIR_VOCES}/{v}.tar.bz2"
        urllib.request.urlretrieve(URL_VOZ.format(v=v), tar)
        with tarfile.open(tar) as t:
            t.extractall(DIR_VOCES)
    try:
        import piper  # noqa: F401
    except ImportError:
        sh(sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", "piper-tts")
    return modelo


def duracion(wav):
    with wave.open(wav) as w:
        return w.getnframes() / w.getframerate()


def palabras(texto, inicio, dur_voz):
    ps = texto.split()
    pesos = [len(p) + 2 for p in ps]
    tot, t, out = sum(pesos) or 1, inicio, []
    for p, w in zip(ps, pesos):
        out.append({"p": p, "t": round(t, 2)})
        t += dur_voz * w / tot
    return out


def locutar(escenas, modelo, carpeta):
    tiempos, t = [], 0.6
    partes = []
    os.makedirs(os.path.join(carpeta, "voz"), exist_ok=True)
    for i, e in enumerate(escenas):
        wav = os.path.join(carpeta, "voz", f"{i:02d}.wav")
        p = subprocess.run([sys.executable, "-m", "piper", "-m", modelo, "-f", wav, "--length-scale", "0.92",
                            "--sentence-silence", "0.15"], input=e["voz"].encode(), capture_output=True)
        if p.returncode:
            sys.exit(p.stderr.decode())
        d = duracion(wav)
        dur_escena = max(d + PAUSA, 1.6)
        tiempos.append({"inicio": round(t, 3), "dur": round(dur_escena, 3), "voz": round(d, 3),
                        "sfx": e.get("sfx", ""), "palabras": palabras(e["voz"], t, d)})
        partes.append((wav, t))
        t += dur_escena
    total = round(t + 1.2, 2)
    return tiempos, partes, total


# ---------- Personajes (SVG plano) ----------
def mascota(pose, cara="#1FA9E8", rasgos="#fff"):
    boca = f'<path class="boca" d="M70 118 Q100 150 130 118" stroke="{rasgos}" stroke-width="12" fill="none" stroke-linecap="round"/>'
    if pose == "alerta":
        boca = f'<ellipse class="boca" cx="100" cy="126" rx="16" ry="20" fill="{rasgos}"/>'
    ojos = f'<circle cx="74" cy="92" r="9" fill="{rasgos}"/><circle cx="126" cy="92" r="9" fill="{rasgos}"/>'
    brazo = ''
    if pose in ("senala", "ok"):
        brazo = f'<path d="M178 120 L240 70" stroke="{cara}" stroke-width="18" stroke-linecap="round"/>'
        if pose == "ok":
            brazo += f'<circle cx="246" cy="62" r="16" fill="{cara}"/>'
    return f'''<svg viewBox="-20 -60 300 300" class="pj mascota pose-{pose}">
  <g class="cuerpo">
    <path d="M100 20 C160 20 190 55 190 110 C190 165 155 195 100 195 C88 195 76 193 66 189 L28 215 L40 175 C20 158 10 136 10 110 C10 55 40 20 100 20Z" fill="{cara}"/>
    {ojos}{boca}{brazo}
    <path d="M30 40 Q100 -45 170 40 Z" fill="#0D1117"/><rect x="18" y="34" width="164" height="16" rx="8" fill="#0D1117"/>
    <rect x="90" y="-12" width="20" height="40" rx="6" fill="#F2A33A"/>
  </g></svg>'''


def trabajador(pose):
    casco = '<path d="M62 40 Q100 0 138 40 Z" fill="#F2A33A"/><rect x="54" y="36" width="92" height="10" rx="5" fill="#F2A33A"/>'
    cabeza = '<circle cx="100" cy="62" r="28" fill="#E8B48A"/>'
    chaleco = '<rect x="68" y="92" width="64" height="86" rx="18" fill="#F2A33A"/><rect x="68" y="130" width="64" height="8" fill="#fff"/>'
    piernas = '<rect x="74" y="172" width="20" height="78" rx="9" fill="#1d3557"/><rect x="106" y="172" width="20" height="78" rx="9" fill="#1d3557"/>'
    brazos = '<rect x="46" y="98" width="18" height="70" rx="9" fill="#E8B48A"/><rect x="136" y="98" width="18" height="70" rx="9" fill="#E8B48A"/>'
    if pose == "agachado":
        return f'''<svg viewBox="0 0 200 260" class="pj trabajador pose-agachado"><g class="cuerpo" transform="translate(0,60)">
  <ellipse cx="100" cy="182" rx="70" ry="14" fill="#0003"/>
  <path d="M60 170 Q60 110 100 104 Q140 110 140 170Z" fill="#F2A33A"/>
  <circle cx="100" cy="96" r="26" fill="#E8B48A"/>
  <path d="M66 82 Q100 44 134 82 Z" fill="#F2A33A"/>
  <path d="M58 92 Q100 40 142 92" stroke="#E8B48A" stroke-width="16" fill="none" stroke-linecap="round"/>
  <rect x="64" y="160" width="72" height="22" rx="10" fill="#1d3557"/></g></svg>'''
    if pose == "senala":
        brazos = '<rect x="46" y="98" width="18" height="70" rx="9" fill="#E8B48A"/><rect x="138" y="70" width="18" height="70" rx="9" fill="#E8B48A" transform="rotate(-50 147 105)"/>'
    if pose == "alerta":
        brazos = '<rect x="40" y="40" width="18" height="70" rx="9" fill="#E8B48A" transform="rotate(25 49 75)"/><rect x="142" y="40" width="18" height="70" rx="9" fill="#E8B48A" transform="rotate(-25 151 75)"/>'
    return f'''<svg viewBox="0 0 200 260" class="pj trabajador pose-{pose}"><g class="cuerpo">
  <ellipse cx="100" cy="252" rx="60" ry="10" fill="#0003"/>{piernas}{brazos}{chaleco}{cabeza}{casco}</g></svg>'''


def personaje(e):
    p, pose = e.get("personaje", "mascota"), e.get("pose", "habla")
    if p == "trabajador":
        return trabajador(pose)
    if p == "mascota":
        if e.get("fondo") == "azul":
            return mascota(pose, "#FFFFFF", "#1FA9E8")
        return mascota(pose)
    return ""


def titular(e, acento):
    t = html.escape(e.get("texto", ""))
    for r in e.get("resalta", []) or []:
        r = html.escape(r)
        t = t.replace(r, f'<span style="color:{acento}">{r}</span>')
    return t


CSS = """
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;font-family:Manrope;background:#0D1117}
.esc{position:absolute;inset:0;opacity:0;animation:ver var(--d) linear var(--i) both;padding:150px 90px 0}
@keyframes ver{0%{opacity:0}4%{opacity:1}96%{opacity:1}100%{opacity:0}}
.top{display:flex;justify-content:space-between;font-family:Outfit;font-weight:800;font-size:34px;letter-spacing:3px}
h1{font-family:Outfit;font-weight:900;text-transform:uppercase;font-size:118px;line-height:.95;letter-spacing:-3px;margin-top:70px;
   animation:entra .5s cubic-bezier(.2,1.4,.4,1) var(--i) both}
@keyframes entra{from{transform:translateY(80px) scale(.9);opacity:0}to{transform:none;opacity:1}}
.pjw{position:absolute;left:0;right:0;bottom:430px;display:flex;justify-content:center;animation:sube .6s cubic-bezier(.2,1.3,.4,1) calc(var(--i) + .15s) both}
@keyframes sube{from{transform:translateY(200px);opacity:0}to{transform:none;opacity:1}}
.pj{width:560px;height:560px;overflow:visible}
.pose-habla .cuerpo,.pose-ok .cuerpo,.pose-senala .cuerpo{animation:respira 1.2s ease-in-out infinite;transform-origin:50% 100%}
@keyframes respira{50%{transform:scale(1.03,0.97)}}
.mascota .boca{animation:habla .28s steps(2) infinite;transform-origin:100px 125px}
@keyframes habla{50%{transform:scaleY(.4)}}
.pose-alerta .cuerpo{animation:salta .5s ease-in-out infinite}
@keyframes salta{50%{transform:translateY(-30px)}}
.pose-cae .cuerpo{animation:cae 1.4s ease-in calc(var(--i) + .6s) both;transform-origin:50% 100%}
@keyframes cae{0%{transform:none}40%{transform:rotate(25deg)}100%{transform:translateY(180px) rotate(95deg)}}
.pose-piensa .cuerpo{animation:balancea 1.6s ease-in-out infinite;transform-origin:50% 100%}
@keyframes balancea{50%{transform:rotate(-6deg)}}
.temblor{animation:tiembla .12s linear infinite}
@keyframes tiembla{25%{transform:translate(14px,-8px) rotate(.6deg)}50%{transform:translate(-12px,10px)}75%{transform:translate(10px,6px) rotate(-.6deg)}}
.zoom{animation:zoom 4s ease-out both}@keyframes zoom{from{transform:scale(1)}to{transform:scale(1.08)}}
.sub{position:absolute;left:70px;right:70px;bottom:150px;background:#0D1117E6;color:#fff;border-radius:28px;padding:30px 38px;
     font-size:44px;font-weight:700;line-height:1.3;text-align:center;animation:entra .4s ease-out calc(var(--i) + .1s) both}
.norma{display:inline-block;margin-top:40px;background:#0D1117;color:#fff;font-family:Outfit;font-weight:800;font-size:36px;letter-spacing:2px;
       padding:20px 30px;border-radius:18px;animation:entra .4s ease-out calc(var(--i) + .4s) both}
.norma small{color:#F2A33A;margin-right:14px}
.cta .pill{display:inline-block;background:#0D1117;color:#fff;font-family:Outfit;font-weight:800;font-size:40px;padding:22px 36px;border-radius:50px;margin-top:40px}
.cta .wsp{margin-top:40px;background:#fff;border-radius:34px;padding:40px;display:flex;gap:30px;align-items:center;color:#0D1117}
.cta .wsp b{font-family:Outfit;font-size:60px}.cta .ico{width:120px;height:120px;border-radius:60px;background:#25D366;flex:none}
"""


def armar_html(escenas, tiempos, total):
    bloques = []
    n = len(escenas)
    for i, (e, t) in enumerate(zip(escenas, tiempos)):
        bg, fg, acento = FONDOS.get(e.get("fondo", "oscuro"), FONDOS["oscuro"])
        var = f"--i:{t['inicio']}s;--d:{t['dur']}s"
        clase_ef = {"temblor": "temblor", "zoom": "zoom"}.get(e.get("efecto", ""), "")
        top = f'<div class="top" style="color:{fg}"><span>@basesegura.cl</span><span style="opacity:.6">{i+1:02d} / {n:02d}</span></div>'
        norma = f'<div class="norma"><small>LO EXIGE</small>{html.escape(e["norma"])}</div>' if e.get("norma") else ""
        if e.get("cta"):
            cuerpo = f'''<h1 style="color:{fg}">{titular(e, acento)}</h1>
<div class="cta"><span class="pill">DIAGNÓSTICO GRATIS</span>
<div class="wsp"><div class="ico"></div><div><b>+56 9 6863 3349</b><div style="font-size:38px;font-weight:700">WhatsApp · basesegura.cl</div></div></div></div>'''
        else:
            cuerpo = f'<h1 style="color:{fg}">{titular(e, acento)}</h1>{norma}<div class="pjw">{personaje(e)}</div>'
        sub = f'<div class="sub">{html.escape(e["voz"])}</div>' if not e.get("cta") else ""
        bloques.append(f'<section class="esc" style="{var};background:{bg}"><div class="{clase_ef}" style="height:100%">{top}{cuerpo}</div>{sub}</section>')
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="file:///tmp/bs/fonts/fonts.css" rel="stylesheet"><style>{CSS}</style></head>
<body>{"".join(bloques)}</body></html>'''


def mezclar(video_mudo, partes, escenas, tiempos, total, salida):
    entradas, filtros, idx = ["-i", video_mudo], [], 1
    etiquetas = []
    for wav, t in partes:
        entradas += ["-i", wav]
        ms = int(t * 1000)
        filtros.append(f"[{idx}]adelay={ms}|{ms},volume=1.6[a{idx}]")
        etiquetas.append(f"[a{idx}]")
        idx += 1
    for e, t in zip(escenas, tiempos):
        s = e.get("sfx")
        f = os.path.join(AQUI, "sfx", f"{s}.wav") if s else ""
        if f and os.path.exists(f):
            entradas += ["-i", f]
            ms = int(max(t["inicio"] - 0.1, 0) * 1000)
            filtros.append(f"[{idx}]adelay={ms}|{ms},volume=0.55[a{idx}]")
            etiquetas.append(f"[a{idx}]")
            idx += 1
    filtros.append(f"{''.join(etiquetas)}amix=inputs={len(etiquetas)}:normalize=0,alimiter=limit=0.95[mix]")
    sh("ffmpeg", "-loglevel", "error", "-y", *entradas, "-filter_complex", ";".join(filtros),
       "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", str(total),
       "-movflags", "+faststart", salida)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    modo = "--voz" if "--voz" in sys.argv else "--grabar" if "--grabar" in sys.argv else "todo"
    if len(args) < 2:
        sys.exit(__doc__)
    guion = json.load(open(args[0], encoding="utf-8"))
    carpeta = args[1]
    os.makedirs(carpeta, exist_ok=True)
    escenas = guion["escenas"]
    html_path = os.path.join(carpeta, "reel.html")
    tj = os.path.join(carpeta, "tiempos.json")
    if modo in ("todo", "--voz"):
        modelo = asegurar_voz(guion.get("voz", "es_MX-claude-high"))
        tiempos, partes, total = locutar(escenas, modelo, carpeta)
        json.dump({"total": total, "escenas": tiempos, "partes": partes}, open(tj, "w"), indent=1, ensure_ascii=False)
        if modo == "--voz":
            print(f"Voz lista: {tj} ({total} s). Ahora escribe {html_path} y corre --grabar.")
            return
        open(html_path, "w", encoding="utf-8").write(armar_html(escenas, tiempos, total))
    d = json.load(open(tj, encoding="utf-8"))
    tiempos, partes, total = d["escenas"], [tuple(p) for p in d["partes"]], d["total"]
    mudo = os.path.join(carpeta, ".mudo.mp4")
    sh("node", os.path.join(AQUI, "grabar-reel.mjs"), html_path, mudo, str(total))
    mezclar(mudo, partes, escenas, tiempos, total, os.path.join(carpeta, "reel.mp4"))
    os.remove(mudo)
    print(f"Reel listo: {os.path.join(carpeta, 'reel.mp4')} ({total} s)")


if __name__ == "__main__":
    main()
