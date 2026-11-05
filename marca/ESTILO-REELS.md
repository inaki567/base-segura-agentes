# Estilo de los reels de Base Segura (definido por Iñaki el 05-11-2026)

Referencias: `marca/referencias-reels/*.jpg` (12 cuadros de cada video de ejemplo). Míralas SIEMPRE antes de hacer un reel.
Son de otra marca: copia el ESTILO, nunca su logo, nombre, colores de marca ni textos. Todo lo de marca es de Base Segura.

## La idea
Mini historia animada de 45 a 65 segundos sobre una SITUACIÓN real de trabajo, contada por una voz en off cercana, que termina en qué hacer paso a paso y qué dice la ley chilena vigente.
Ejemplos: "Accidente grave: ¿qué haces primero?", "¿Accidente en la micro = accidente del trabajo?", "¿Qué hacer en un terremoto en la pega?", "¿Qué pasa si alguien cae de más de 1,8 m?".

## Estructura (en este orden)
1. **Gancho (0 a 3 s):** pregunta grande en el centro, con una palabra en color ("Accidente **grave**: ¿qué haces primero?", "¿Accidente en la micro **=** accidente del trabajo?"). Personaje en primer plano con cara de preocupación.
2. **La situación:** el escenario completo (faena, obra, oficina, calle, bodega) y lo que pasa (caída, sismo, choque, incendio). Etiqueta tipo pastilla con el hecho: "⚠️ CAÍDA DE MÁS DE 1,8 m".
3. **Qué hacer, numerado:** "3 COSAS · ⏱ DE INMEDIATO" y luego una pastilla por paso: "1 · SUSPENDER LA FAENA", "2 · AVISAR DE INMEDIATO", "3 · DENUNCIAR A LA MUTUAL O ISL".
4. **La ley:** tarjeta blanca que aparece desde abajo con encabezado "LEY 16.744 · CHILE", "Art. 76", un extracto corto del artículo con la parte clave resaltada en amarillo y debajo una pastilla chica "🇨🇱 Ley 16.744 · Chile · art. 76". Solo texto verificado en bcn.cl el mismo día.
5. **Elementos de interfaz que ayudan a contar:** pantalla de teléfono llamando ("Llamando… Inspección del Trabajo y Seremi de Salud" con el número real), formulario "DENUNCIA DE ACCIDENTE", candado cuando la faena queda bloqueada, cinta de peligro rojo y blanco, reloj/temporizador.
6. **Cierre:** fondo oscuro, logo de Base Segura al centro y una franja: "Comenta **"DIAGNÓSTICO"** para recibir más información sobre nuestro diagnóstico gratis" + WhatsApp +56 9 6863 3349. Abajo, en letra chica, la fuente: "Fuente: Ley 16.744 (Chile), art. 76 · …".

## Look
- **Escenario oscuro y nocturno** (azul-negro #0D1117 a #1a2233), suelo con grilla tenue, luz suave, sensación de maqueta 3D vista en isométrico. Lluvia o partículas sutiles opcionales.
- **Escenarios tipo maqueta:** andamios, casetas de faena con techos de colores, conos naranjos, edificios con ventanas iluminadas, calles con línea amarilla, micro/bus, árboles redondos. Hechos con SVG/CSS en perspectiva isométrica (transform: rotateX/rotateZ) con sombras suaves.
- **Personajes estilo juguete (tipo Playmobil):** cabeza grande y redonda, casco amarillo/blanco, ojos y cejas expresivos, cuerpo cilíndrico, colores planos (azul, morado, gris), franja reflectante amarilla en el cuerpo. Uno en primer plano para el gancho y varios chicos en la escena.
- **Cámara:** siempre en movimiento suave: acercamientos, paneos y giros leves entre escenas (animaciones de transform sobre el contenedor de la escena). Nunca una lámina estática más de 2 s.
- **Subtítulos karaoke ARRIBA:** 1 o 2 líneas cortas en blanco, letra Outfit 800, la palabra clave en amarillo/naranjo #F2A33A; van apareciendo palabra por palabra sincronizados con la voz (usa `palabras` de `reel/tiempos.json`).
- **Pastillas/etiquetas:** fondo de color sólido (rojo #E5484D para peligro, amarillo #FFC53D para pasos, azul #1FA9E8 para info, verde #25D366 para lo correcto), texto negro o blanco en MAYÚSCULAS, Outfit 800, con un emoji o ícono al inicio, bordes muy redondeados y sombra. Entran con un pequeño rebote.
- **Marca:** @basesegura.cl chico, arriba a la derecha con ícono de Instagram, fijo durante todo el video.
- Formato 1080x1920. Zona segura: nada importante a menos de 150 px del borde superior ni de 400 px del borde inferior (ahí van los botones de Instagram).

## Sonido
- Voz en off masculina, joven, cercana, ritmo ágil ("Imagina esto…", "Pero ojo con…", "Uno… Dos… Tres…").
- Efectos en cada momento clave (`herramientas/sfx/`): whoosh en cambios de cámara, golpe en caídas, temblor en sismos, alarma en emergencias, pop cuando aparece una pastilla, ding cuando aparece la ley, error en lo que NO se debe hacer.

## Cómo se arma (técnico)
1. `python3 herramientas/armar-reel.py reel/guion.json reel/ --voz` → genera la voz por escena y `reel/tiempos.json` (inicio, duración y tiempo de cada palabra).
2. Escribe `reel/reel.html` a mano con este estilo: una `<section>` por escena con `animation-delay` igual a su `inicio`, todas las animaciones en CSS (@keyframes), fuentes desde `file:///tmp/bs/fonts/fonts.css`.
3. `python3 herramientas/armar-reel.py reel/guion.json reel/ --grabar` → graba y mezcla voz + efectos (los efectos salen del campo `sfx` de cada escena del guion).
4. Revisa 5 o 6 cuadros con ffmpeg + Read antes de entregar.
La plantilla automática (sin `--voz`/`--grabar`) solo sirve de respaldo si se acaba el tiempo.
