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
La voz de los reels es **Gemini TTS, voz Finn, acento chileno animado** (elegida por Iñaki). La nube no puede llamar a Gemini, así que la genera Apps Script (`herramientas/apps-script/Voz.gs`, proyecto Contenido):
1. Con `guion.json` listo (con `"voz": "gemini:Finn"`), manda con Gmail un correo a basesegura.cl@gmail.com, asunto `VOZ PEDIDO <carpeta>` y cuerpo SOLO este JSON: `{"fecha":"<carpeta>","escenas":["<voz escena 0>","<voz escena 1>",...]}` (los textos del campo `voz` de cada escena, en orden).
2. Cada 2 minutos busca en Gmail `subject:"VOZ LISTA <carpeta>"` (máximo 20 minutos). Cuando llegue, descarga el adjunto `voz.zip` y descomprímelo en `reel/voz/` (quedan `00.wav`, `01.wav`…).
3. `python3 herramientas/armar-reel.py reel/guion.json reel/ --voz` (calcula tiempos con esos wav), escribe `reel.html` y luego `--grabar`.
4. Si a los 20 minutos no llegó, usa el respaldo: cambia `"voz"` a `"kokoro:em_alex"` en el guion, corre igual y avisa en el correo de entrega que salió con la voz de respaldo.
Si cambias un texto de voz en un pedido de cambio, pide la voz de nuevo con asunto `VOZ PEDIDO <carpeta nueva>`.

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
- Solo los viernes: `linkedin-domingo/` con los mismos archivos que `linkedin/`.
- Solo existen las carpetas de las piezas que tocan ese día (ver calendario en `CLAUDE.md`).
- `revision.md`
- `contenido.json` (lo lee el script de Google; rutas relativas a la carpeta):
```json
{
  "carpeta": "2026-11-06",
  "post": { "imagenes": ["post/01.png", "post/02.png"], "vista_previa": "post/vista-previa.jpg", "caption": "..." },
  "reel": { "video": "reel/reel.mp4", "caption": "..." },
  "linkedin": { "texto": "...", "imagen": "linkedin/imagen.png", "cuenta": "personal | empresa" },
  "linkedin_domingo": { "texto": "...", "imagen": "linkedin-domingo/imagen.png", "cuenta": "empresa" },
  "revision": "OK o la lista de notas",
  "temas": { "post": "...", "reel": "...", "linkedin": "..." }
}
```
Incluye en `contenido.json` SOLO las claves de las piezas que existen ese día (no pongas claves vacías). Genera `contenido.json` con un script (python o node) que lea los archivos, nunca escribiendo los textos a mano en JSON.

## Temas ya usados (para no repetir)
- `publicado/temas.md` del repo.
- Gmail de basesegura.cl@gmail.com: correos con asunto `[CONTENIDO] Publicado` (aprobados) y `[CONTENIDO] Para aprobar` de los últimos 30 días (propuestos).

## Generación diaria
1. Preparación. Carpeta = fecha de hoy en Chile (`TZ=America/Santiago date +%F`). Si `entregas/<fecha>` ya existe, termina sin hacer nada. Si hoy es sábado o domingo, termina sin hacer nada.
   Mira el día de la semana (`TZ=America/Santiago date +%u`) y crea SOLO las piezas del "Calendario semanal" de `CLAUDE.md`: lunes, miércoles y viernes = reel + LinkedIn (lunes y viernes perfil personal, miércoles página de empresa; el viernes además `linkedin-domingo` para la página de empresa); martes y jueves = carrusel solo.
   **Pedidos de Iñaki:** si existe `pedidos/<fecha>.md`, léelo y obedécelo antes que todo (manda sobre el calendario y la elección de temas). Si existe `pedidos/<fecha>/<pieza>/`, esa pieza ya está hecha: cópiala tal cual a `entregas/<fecha>/<pieza>/` y no la vuelvas a generar.
2. Arma la lista de temas ya usados y pásasela al investigador.
3. Sigue `CLAUDE.md` con los cinco roles de `.claude/agents/` (investigador → redactor → disenador → editor-reel → revisor), trabajando dentro de `entregas/<fecha>/` en vez de `por-aprobar/`. Usa los subagentes si están disponibles; si no, cumple tú cada rol leyendo su archivo.
4. Comprueba que existan los archivos de las piezas del día (PNG y `vista-previa.jpg` si hay carrusel; `reel.mp4` de menos de 20 MB si hay reel; `linkedin.md` e `imagen.png` si hay LinkedIn) y mira tú mismo las imágenes con la herramienta Read.
5. Genera `contenido.json`.
6. Limpieza: borra con `git rm -r` las carpetas de `entregas/` de más de 7 días.
7. `git add -A && git commit -m "feat: contenido <carpeta>" && git push` (si falla por cambios remotos: `git pull --rebase` y push de nuevo).
8. Envía con Gmail `send_message` a basesegura.cl@gmail.com (única dirección permitida) un correo con asunto `[CONTENIDO] Para aprobar <carpeta>` y cuerpo: la carpeta, las piezas del día y su tema, una por línea (para LinkedIn indica si es perfil personal o página de empresa). Sin adjuntos.

## Cambios pedidos por Iñaki
1. Busca en Gmail correos con asunto `[CONTENIDO] Cambio` de los últimos 3 días que NO tengan la etiqueta `Cambio hecho`. Si no hay, termina sin hacer nada (no clones nada).
2. Por cada uno (del más antiguo al más nuevo): el asunto trae la carpeta y el cuerpo trae el pedido.
3. Preparación. Copia `entregas/<carpeta>` a `entregas/<carpeta base>-vN` (siguiente número libre) y aplica SOLO el cambio pedido con el rol que corresponda; vuelve a exportar las imágenes o el reel si cambiaron, pasa por el revisor y regenera `contenido.json` con la carpeta nueva.
4. Commit y push.
5. Correo `[CONTENIDO] Para aprobar <carpeta nueva>` (cuerpo: qué se cambió en 1 o 2 líneas).
6. Aplica la etiqueta `Cambio hecho` al hilo del pedido (búscala con list_labels; si no existe, créala).
