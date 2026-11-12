# Estilo de los reels de Base Segura (definido por Iñaki el 05-11-2026)

Referencias: `marca/referencias-reels/*.jpg` (12 cuadros de cada video de ejemplo). Míralas SIEMPRE antes de hacer un reel.
Son de otra marca: copia el ESTILO, nunca su logo, nombre, colores de marca ni textos. Todo lo de marca es de Base Segura.

## La idea
Mini historia animada en 3D de **45 a 50 segundos (nunca más de 50)** sobre una SITUACIÓN real de trabajo, contada por una voz en off cercana, que termina en qué hacer paso a paso y qué dice la ley chilena vigente.
Ejemplos: "Accidente grave: ¿qué haces primero?", "¿Accidente en la micro = accidente del trabajo?", "¿Qué hacer en un terremoto en el trabajo?", "¿Qué pasa si alguien cae de más de 1,8 m?".

## Estructura (en este orden)
1. **Gancho (0 a 3 s):** pregunta grande en el centro, con una palabra en color ("Accidente **grave**: ¿qué haces primero?", "¿Accidente en la micro **=** accidente del trabajo?"). Personaje en primer plano con cara de preocupación.
2. **La situación:** el escenario completo (faena, obra, oficina, calle, bodega) y lo que pasa (caída, sismo, choque, incendio). Etiqueta tipo pastilla con el hecho: "⚠️ CAÍDA DE MÁS DE 1,8 m".
3. **Qué hacer, numerado:** "3 COSAS · ⏱ DE INMEDIATO" y luego una pastilla por paso: "1 · SUSPENDER LA FAENA", "2 · AVISAR DE INMEDIATO", "3 · DENUNCIAR A LA MUTUAL O ISL".
4. **La ley:** tarjeta blanca que aparece desde abajo con encabezado "LEY 16.744 · CHILE", "Art. 76", un extracto corto del artículo con la parte clave resaltada en amarillo y debajo una pastilla chica "🇨🇱 Ley 16.744 · Chile · art. 76". Solo texto verificado en bcn.cl el mismo día.
5. **Elementos de interfaz que ayudan a contar:** pantalla de teléfono llamando ("Llamando… Inspección del Trabajo y Seremi de Salud" con el número real), formulario "DENUNCIA DE ACCIDENTE", candado cuando la faena queda bloqueada, cinta de peligro rojo y blanco, reloj/temporizador.
6. **Cierre:** fondo oscuro, logo de Base Segura al centro y una franja con el llamado a la página: "Cotiza tu diagnóstico gratis en **basesegura.cl**" y debajo "contacto@basesegura.cl". La voz lo dice: "Entra a basesegura.cl y cotiza en un minuto". Abajo, en letra chica, la fuente: "Fuente: Ley 16.744 (Chile), art. 76 · …". (No usar "Comenta DIAGNÓSTICO".)

## Look (3D, aprobado por Iñaki el 11-11-2026)
- **Escena 3D real** hecha con el motor `herramientas/3d/` (Three.js): luces, sombras suaves, aspecto de maqueta de juguete, fondo azul-negro. Nada de dibujos planos.
- **Escenarios** (elige el que calce con la situación): `obra` (terreno, andamios, excavadora, conos, valla), `local` (ferretería o comercio con góndolas, mostrador y escalera), `bodega` (estanterías altas con cajas que se pueden caer) y `transito` (bodega con grúa horquilla y pasillo peatonal).
- **Personajes tipo juguete:** el trabajador **inseguro** lleva polera roja, pantalón negro y va sin casco ni EPP (hace lo incorrecto); el trabajador **seguro** lleva chaleco reflectante azul y casco blanco, los colores de Base Segura (hace lo correcto). Caminan, cargan, se tambalean, caen, se asustan, celebran; parpadean y cambian la cara según lo que pasa.
- **Cámara:** siempre en movimiento: acercamiento en el gancho, plano general en la situación, cambio de plano en cada escena, temblor en caídas y golpes, órbita en la ley y el cierre.
- **Subtítulos karaoke ARRIBA:** 1 o 2 líneas cortas en blanco, letra Outfit 800, la palabra clave en amarillo/naranjo #F2A33A; van apareciendo palabra por palabra sincronizados con la voz (usa `palabras` de `reel/tiempos.json`).
- **Pastillas/etiquetas:** fondo de color sólido (rojo #E5484D para peligro, amarillo #FFC53D para pasos, azul #1FA9E8 para info, verde #25D366 para lo correcto), texto negro o blanco en MAYÚSCULAS, Outfit 800, con un emoji o ícono al inicio, bordes muy redondeados y sombra. Entran con un pequeño rebote.
- **Marca:** @basesegura.cl chico, arriba a la derecha con ícono de Instagram, fijo durante todo el video.
- Formato 1080x1920. Zona segura: nada importante a menos de 150 px del borde superior ni de 400 px del borde inferior (ahí van los botones de Instagram).

## Sonido
- Voz en off masculina, joven, cercana, ritmo ágil ("Imagina esto…", "Pero ojo con…", "Uno… Dos… Tres…").
- **Voz elegida por Iñaki (11-11-2026):** Gemini TTS, voz **Finn**, con este estilo exacto: "Acento chileno (español de Chile), narrador viral de reels: más animado y con chispa, sonriendo al hablar, mucho entusiasmo y energía alta pero natural, ritmo ágil, como un creador de contenido chileno joven que cuenta un dato curioso que lo emociona". Se genera desde Apps Script (propiedad `GEMINI_KEY`), porque la nube bloquea la API. Kokoro queda solo de respaldo. En `guion.json` va `"voz": "gemini:Finn"` (flujo en NUBE.md).
- Efectos en cada momento clave (`herramientas/sfx/`): whoosh en cambios de cámara, golpe en caídas, temblor en sismos, alarma en emergencias, pop cuando aparece una pastilla, ding cuando aparece la ley, error en lo que NO se debe hacer.

## Lenguaje
Formal y cercano, sin chilenismos ni palabras coloquiales ("pega", "harto", "al tiro", "cachai", "po"). Frases cortas y claras.

## Cómo se arma (técnico)
Todo el paso a paso está en `herramientas/3d/LEEME.md`: voz Finn → `tiempos.json` (45 a 50 s) → `reel/escena3d.js` → `armar-reel-3d.py reel/ --fotos` (revisar cuadros) → `armar-reel.py ... --grabar`.
Ejemplo completo: `herramientas/3d/ejemplo-escena3d.js`.
