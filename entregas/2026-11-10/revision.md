OK con notas

# Revisión entrega 2026-11-10 (revisor, 10-11-2026)

## Resultado
Ninguna pieza bloquea la entrega. Revisé todas las cifras y normas en la fuente oficial y coinciden. Corregí un texto (linkedin.md). Dejo correcciones recomendadas, no bloqueantes, para la imagen de LinkedIn y el reel.

## 1. Cifras y normas, verificadas en la fuente (10-11-2026)
- Suseso, "Principales estadísticas SST 2025" (datos al 23/03/2026): 1.770 accidentes graves, 498 por "Caídas de altura de más de 1,8 metros". OK (reel, guion y caption).
- Compendio Suseso, Libro IV, Tít. I, Letra D: grave = "caída de altura de más de 1.8 metros". OK.
- Ley 16.744, art. 76 (texto Suseso): informar inmediatamente a la Inspección del Trabajo y a la Seremi de Salud, "deberá suspender de forma inmediata las faenas afectadas", reanudación previa fiscalización y multa "de cincuenta a ciento cincuenta unidades tributarias mensuales". OK. La cita de la tarjeta de la ley es textual.
- Código del Trabajo (texto DT al 02-11-2026): art. 184 ("informando de los posibles riesgos", "los implementos necesarios para prevenir accidentes") y art. 183-E (la empresa principal debe "proteger eficazmente la vida y salud de todos los trabajadores que laboran en su obra, empresa o faena"). OK. La DT (consulta w3-article-94209) lo confirma.
- Suseso, noticia del 06-11-2026: oficio que "instruye a las mutualidades" (ACHS, IST y Mutual de Seguridad), al ISL y a las empresas con administración delegada. Les pide "desarrollar un plan preventivo frente a la amenaza de incendios forestales", identificar a las empresas en zonas de mayor exposición y prescribir y verificar medidas (vegetación seca, materiales combustibles, sistemas eléctricos y maquinarias, extintores, vías de evacuación señalizadas, trabajos de soldadura o corte). OK.
- Decreto exento N° 1.142 (Interior, 02-06-2026, Diario Oficial del 26-06-2026): emergencia preventiva "por amenaza de incendios forestales" en 13 regiones, incluida La Araucanía, de junio de 2026 a marzo de 2027. OK. La nota de Suseso la llama "por calor"; linkedin.md usa bien la redacción del decreto.

## 2. Precios y descuentos
OK. Solo aparecen los "desde" de CLAUDE.md: IRL $20.000 por puesto y matriz $62.000, siempre con "+ IVA" y "referencial". No hay precio del Plan 2. El único descuento es −10 % (2 documentos), y está bien aplicado. LinkedIn no lleva precio.

## 2b. Carrusel y cierres
OK. El carrusel tiene 4 láminas sencillas. Todas las piezas cierran en basesegura.cl, basesegura.cl/cotizar o contacto@basesegura.cl. No aparece "Comenta DIAGNÓSTICO".

## 3. Ortografía, tono y contacto
OK. Usamos "nosotros" y el tono de sugerencia, y citamos los artículos. El contacto está correcto. LinkedIn tiene unas 244 palabras y 3 hashtags.

## 4. Archivos
Están post/01-04.png y vista-previa.jpg, y el texto se lee bien. Está reel/guion.json; el reel.mp4 ya venía verificado por el jefe (64,1 s, 1080x1920). Están linkedin/linkedin.md e imagen.png, y la imagen cumple el estilo (fondo oscuro, logo, título en 2 colores, 1 línea de apoyo y basesegura.cl).

## 5. Temas
- Post (empresa de aseo como contratista, CT 184 y 183-E): es nuevo.
- LinkedIn (oficio Suseso sobre incendios forestales): es nuevo. No choca con "amago de incendio en cocina".
- Reel (caída de más de 1,8 m = accidente grave, art. 76): es nuevo, pero se acerca a "Se accidentó un trabajador, ¿y ahora qué hago?" (03-11). El ángulo es distinto (el umbral de 1,8 m, la suspensión de la faena y la multa), así que lo acepto. Lo dejo como nota para el jefe.

## Correcciones de texto hechas por el revisor
- linkedin/linkedin.md: ajusté la redacción para que sea fiel a la nota de Suseso.
  - "un plan de prevención de incendios forestales" pasa a "un plan preventivo frente a la amenaza de incendios forestales".
  - "retiro de material combustible" pasa a "retiro de materiales combustibles".
  - "revisión eléctrica y de maquinaria" pasa a "revisión de sistemas eléctricos y maquinarias".
- caption.txt (post y reel) y textos.md: sin cambios. Están correctos.

## Correcciones pendientes en imágenes y reel (no las corregí)
1. linkedin/imagen.png e imagen.html, línea de apoyo (recomendado).
   - Texto actual: "La Suseso pidió a las mutualidades revisar a las empresas expuestas."
   - Por qué cambiarla: no es falsa (identificar y verificar medidas equivale a "revisar"), pero la fuente dice "instruye" y también incluye al ISL. "Pidió" le baja el peso.
   - Texto propuesto: "La Suseso instruyó a mutualidades e ISL identificar a las empresas expuestas." (mismos resaltados: "Suseso" en azul y "empresas expuestas" en naranja).
2. linkedin/imagen.png, pastilla "TEMPORADA DE INCENDIOS" (opcional). Es correcta: Suseso habla de la temporada de riesgo y no afirma nada nuevo. Para alinearla con el decreto y con el título, propongo "TEMPORADA DE INCENDIOS FORESTALES".
3. reel/reel.html y reel.mp4, subtítulos karaoke (opcional, en la próxima pasada).
   - En el cierre se lee "base segura punto cl"; lo ideal es mostrar "basesegura.cl" en pantalla aunque la voz lo deletree.
   - Igual con "U T M": mostrar "UTM".
4. post/02.png (cosmético, opcional): es la única lámina sin "DESLIZA →" en el pie (lleva puntos de avance). Se puede dejar.
5. post/html/04.html (técnico): carga Google Fonts desde internet además de fonts.css local. Si se vuelve a renderizar sin red, conviene quitar ese link.

## Hecho por el jefe (10-11-2026)
- LinkedIn `imagen.png`: línea de apoyo cambiada a "La Suseso instruyó a mutualidades e ISL identificar a las empresas expuestas." y pastilla a "TEMPORADA DE INCENDIOS FORESTALES". Reexportada 1200x1500.
- Reel: subtítulos en pantalla muestran "basesegura.cl" y "UTM" (antes "base segura punto cl" y "U T M").
- Reel: se quitó el precio del cierre (voz y pantalla), como pidió Iñaki el 05-11 ("no pongas el precio en la parte final del video"). Cierre nuevo: "Te hacemos la matriz de riesgos para que nadie termine en el suelo… cotiza en un minuto". El precio referencial queda solo en el caption. Reel regrabado.
- Pendientes cosméticos no aplicados: "DESLIZA →" en la lámina 02 (lleva puntos de avance) y link a Google Fonts en post/html/04.html (no afecta los PNG).
