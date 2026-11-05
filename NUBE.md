# Cómo trabaja la oficina de contenido en la nube

Este repositorio es público: aquí NO van tokens, claves ni el webhook de Make.
Las tareas en la nube clonan el repo en `/tmp/bs` (las plantillas cargan las fuentes desde `file:///tmp/bs/fonts/fonts.css`).

## Piezas del flujo
1. **Generación diaria** (tarea en la nube, 7:13): crea las 3 piezas, las sube a `entregas/<carpeta>/` en este repo y avisa por correo.
2. **Script de Google "Contenido"** (en basesegura.cl@gmail.com, bot Base Segura Marketing): lee el aviso, baja los archivos desde GitHub, los manda a Telegram y escucha la respuesta de Iñaki.
   - `APRUEBO` (o `APRUEBO post linkedin`, etc.) → sube a Cloudinary, llama al webhook de Make y manda un correo `[CONTENIDO] Publicado <carpeta>`.
   - Cualquier otro texto → correo `[CONTENIDO] Cambio <carpeta>` con el pedido.
3. **Cambios** (tarea en la nube a los :05 y :35, de 8 a 21): aplica el pedido y sube una versión nueva (`<carpeta>-v2`, `-v3`…).

## Reels con voz y efectos
`python3 herramientas/armar-reel.py reel/guion.json reel/` hace todo. La primera vez instala `piper-tts` con pip y baja la voz desde GitHub (releases de k2-fsa/sherpa-onnx) a /tmp/voces; no necesita otra conexión. Tarda 2 a 4 minutos. Para el estilo de `marca/ESTILO-REELS.md` se usa en dos pasos: `--voz` y, después de escribir reel.html, `--grabar`.

## Preparación (siempre al empezar)
```bash
rm -rf /tmp/bs && git clone --depth 1 https://github.com/inaki567/base-segura-agentes /tmp/bs
cd /tmp/bs && npm ci --silent
```
Para poder hacer push, la sesión debe tener el repo agregado con permiso de escritura (herramienta `add_repo`, owner `inaki567`, repo `base-segura-agentes`, access `push`). Si `/tmp/bs` no es la ruta que pide `add_repo`, igual clona en `/tmp/bs`.

## Estructura de una entrega
`entregas/<carpeta>/` (carpeta = `AAAA-MM-DD` o `AAAA-MM-DD-v2`…):
- `post/brief.md`, `post/textos.md`, `post/html/*.html`, `post/01.png`…, `post/vista-previa.jpg`, `post/caption.txt`
- `reel/brief.md`, `reel/guion.json`, `reel/reel.html`, `reel/tiempos.json`, `reel/reel.mp4`, `reel/caption.txt`
- `linkedin/brief.md`, `linkedin/linkedin.md`, `linkedin/imagen.png` (obligatoria)
- `revision.md`
- `contenido.json` (lo lee el script de Google; rutas relativas a la carpeta):
```json
{
  "carpeta": "2026-11-06",
  "post": { "imagenes": ["post/01.png", "post/02.png"], "vista_previa": "post/vista-previa.jpg", "caption": "..." },
  "reel": { "video": "reel/reel.mp4", "caption": "..." },
  "linkedin": { "texto": "...", "imagen": "linkedin/imagen.png" },
  "revision": "OK o la lista de notas",
  "temas": { "post": "...", "reel": "...", "linkedin": "..." }
}
```
Genera `contenido.json` con un script (python o node) que lea los archivos, nunca escribiendo los textos a mano en JSON.

## Temas ya usados (para no repetir)
- `publicado/temas.md` del repo.
- Gmail de basesegura.cl@gmail.com: correos con asunto `[CONTENIDO] Publicado` (aprobados) y `[CONTENIDO] Para aprobar` de los últimos 30 días (propuestos).

## Generación diaria
1. Preparación. Carpeta = fecha de hoy en Chile (`TZ=America/Santiago date +%F`). Si `entregas/<fecha>` ya existe, termina sin hacer nada.
2. Arma la lista de temas ya usados y pásasela al investigador.
3. Sigue `CLAUDE.md` con los cinco roles de `.claude/agents/` (investigador → redactor → disenador → editor-reel → revisor), trabajando dentro de `entregas/<fecha>/` en vez de `por-aprobar/`. Usa los subagentes si están disponibles; si no, cumple tú cada rol leyendo su archivo.
4. Comprueba que existan los PNG, `vista-previa.jpg` y `reel.mp4` (menos de 20 MB), y mira tú mismo la vista previa con la herramienta Read.
5. Genera `contenido.json`.
6. Limpieza: borra con `git rm -r` las carpetas de `entregas/` de más de 7 días.
7. `git add -A && git commit -m "feat: contenido <carpeta>" && git push` (si falla por cambios remotos: `git pull --rebase` y push de nuevo).
8. Envía con Gmail `send_message` a basesegura.cl@gmail.com (única dirección permitida) un correo con asunto `[CONTENIDO] Para aprobar <carpeta>` y cuerpo: la carpeta y los 3 temas, uno por línea. Sin adjuntos.

## Cambios pedidos por Iñaki
1. Busca en Gmail correos con asunto `[CONTENIDO] Cambio` de los últimos 3 días que NO tengan la etiqueta `Cambio hecho`. Si no hay, termina sin hacer nada (no clones nada).
2. Por cada uno (del más antiguo al más nuevo): el asunto trae la carpeta y el cuerpo trae el pedido.
3. Preparación. Copia `entregas/<carpeta>` a `entregas/<carpeta base>-vN` (siguiente número libre) y aplica SOLO el cambio pedido con el rol que corresponda; vuelve a exportar las imágenes o el reel si cambiaron, pasa por el revisor y regenera `contenido.json` con la carpeta nueva.
4. Commit y push.
5. Correo `[CONTENIDO] Para aprobar <carpeta nueva>` (cuerpo: qué se cambió en 1 o 2 líneas).
6. Aplica la etiqueta `Cambio hecho` al hilo del pedido (búscala con list_labels; si no existe, créala).
