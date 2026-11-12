# Reels 3D (estilo vigente desde el 11-11-2026)

Flujo (desde la raíz del repo):
1. Pide la voz Finn (NUBE.md) y corre `python3 herramientas/armar-reel.py reel/guion.json reel/ --voz` → `reel/tiempos.json`. Debe durar **45 a 50 s**.
2. Escribe `reel/escena3d.js` (formato abajo; ejemplo completo en `herramientas/3d/ejemplo-escena3d.js`).
3. `python3 herramientas/armar-reel-3d.py reel/ --fotos` → `reel/reel.html` + 6 cuadros en `reel/cuadros/`. Míralos con Read y corrige cámara/posiciones hasta que todo se vea bien (personajes visibles, nada tapado por los textos).
4. `python3 herramientas/armar-reel.py reel/guion.json reel/ --grabar` (unos 20 minutos para 50 s).

## escena3d.js
```js
export default {
  escenario: 'bodega',            // bodega | transito | local | obra
  actores: { pedro: { tipo: 'inseguro', pos: [x, z], rot: 0.5 } },   // tipo: inseguro | seguro | jefe | cliente
  objetos: { s1: { tipo: 'saco', pos: [x, y, z], rot: 0 } },          // props extra
  pasos: [ { t: 'e2+0.5', a: 'pedro', hacer: 'caminar', hacia: [x, z], dur: 1.5 } ],
  camara: [ { t: 'e0', plano: 'cerca', a: 'pedro', ang: 0.3 } ],
};
```
- Tiempos: número en segundos, `'e3'` (inicio de la escena 3 en tiempos.json), `'e3+1.2'`, `'e3-0.5'`, `'fin'`.
- Suelo útil: x de -5 a 5, z de -3 a 3.5 (z positivo = hacia la cámara). `rot` en radianes (0 mira a la cámara).

### Personajes
- `inseguro`: polera roja, pantalón negro, SIN casco ni EPP → el que hace lo incorrecto.
- `seguro`: chaleco reflectante azul y casco blanco (colores de Base Segura) → el que hace lo correcto.
- `jefe` (camisa blanca, casco blanco) y `cliente` (sin EPP, morado).
Acciones de actor (`a: id`): `caminar`/`correr`/`empujar` {hacia:[x,z], mirar?}, `girar` {rot}, `agacharse`, `cargar` {objeto} (queda al hombro hasta `dejar`), `dejar` {objeto, en?:[x,y,z]}, `tambalear`, `alerta` (manos a la cabeza), `caer` {hasta?: altura} (queda tendido hasta `levantarse`), `levantarse`, `subir` {altura} (escalera/andamio), `feliz`, `saludo`, `apuntar`. Opcionales: `mirarA: 'id'`, `marca: 'peligro'|'ok'` (anillo rojo/verde en el suelo).
Acciones de objeto (`o: id`): `mover` {hacia:[x,y,z], rot?, orientar?}, `caer` {hasta?, avance?, lateral?, giro?}, `brazo` {ang} (excavadora), `girarCabina` {ang}, `horquilla` {altura} (grúa).

### Escenarios y sus objetos con id
- `bodega`: estanterías altas con cajas (`estante`, `estante2`, cajas que pueden caer: `caja_alta`, `caja_alta1`… `caja_alta8`), pallet con `caja1`…`caja4` en x≈2.8, z≈-0.4, extintor, líneas amarillas.
- `transito`: bodega + pasillo peatonal verde (z de 0.6 a 1.5) + grúa horquilla `grua` en (-3.2, 2.4) con carga. Para que avance: `{o:'grua', hacer:'mover', hacia:[3,0,2.4], dur:3}`.
- `local`: ferretería con góndolas de colores (`gondola`, `gondola2`), `mostrador`, `escalera` de tijera en (-2.9, -2.0), `extintor`, `caja1`…`caja3` apiladas en (1.8, 0.6).
- `obra`: losas y pilares al fondo, `andamio` de 2 pisos en (-1, -1.3) (pisos a 1.6 y 3.2 m), `excavadora` en (3.7, -0.4), ladrillos, conos, `valla`, caseta de faena.
Props para `objetos`: saco, caja, pallet, cono, carro, escalera, grua, excavadora, andamio, estante, mostrador, gondola, ladrillos, barril, extintor, valla.

### Cámara
`plano`: `general` | `medio` | `cerca` | `detalle` | `alto`; `a: 'id'` (sigue a un actor u objeto) o `mirar: [x, y, z]`; `ang` (radianes, giro alrededor), `orbita` (giro por segundo), `dur` (transición, 0.9 s). Cambia el plano en cada escena; en caídas y tambaleos tiembla sola. Acercamiento en el gancho, plano general en la situación, `alto` u órbita en la ley y el cierre.

### Textos en pantalla (salen del guion.json)
Subtítulos karaoke (palabras de `tiempos.json`, `resalta` en naranjo), `texto` grande solo en la escena 0 (gancho), `pastilla` por escena `{"texto": "1 · Usa un carro", "tipo": "peligro|paso|info|ok"}`, `tarjeta` (ley) y `cierre` (logo, franja, contacto y fuente) en la última escena.
