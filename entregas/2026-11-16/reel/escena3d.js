// Reel 16-11-2026: grúa horquilla y personas en el mismo pasillo (DS 594 art. 8).
export default {
  escenario: 'transito',
  actores: {
    pedro: { tipo: 'inseguro', pos: [-1.9, 1.5], rot: 0 },   // cruza mirando el celular, sin EPP
    ana: { tipo: 'seguro', pos: [4.4, 1.05], rot: -1.57 },         // usa el pasillo peatonal
    jefe: { tipo: 'jefe', pos: [3.6, -1.6], rot: -0.4 },           // supervisor: informa el riesgo
  },
  objetos: {
    c1: { tipo: 'caja', pos: [0.6, 0.25, 1.1] },                   // caja que estorba el pasillo
    cono1: { tipo: 'cono', pos: [-0.9, 0, 1.75] },
    cono2: { tipo: 'cono', pos: [0.1, 0, 1.75] },
  },
  pasos: [
    // e0 gancho: la grúa retrocede y Pedro cruza distraído
    { t: 0, o: 'grua', hacer: 'mover', hacia: [1.6, 0, 2.4], dur: 0.05 },
    { t: 'e0+0.2', o: 'grua', hacer: 'mover', hacia: [-0.5, 0, 2.4], dur: 2.4 },
    { t: 'e0+0.1', a: 'pedro', hacer: 'caminar', hacia: [-1.9, 2.6], dur: 1.6, marca: 'peligro' },
    { t: 'e0+1.9', a: 'pedro', hacer: 'girar', rot: 0.9, dur: 0.3 },
    { t: 'e0+2.3', a: 'pedro', hacer: 'alerta', dur: 2.0, mirarA: 'grua', marca: 'peligro' },
    // e1 la situación: pasillo compartido, Pedro sale del paso y la grúa sigue
    { t: 'e1+0.3', a: 'pedro', hacer: 'tambalear', dur: 1.2 },
    { t: 'e1+1.6', a: 'pedro', hacer: 'caminar', hacia: [-3.4, 3.1], dur: 1.4 },
    { t: 'e1+0.5', o: 'grua', hacer: 'mover', hacia: [2.6, 0, 2.4], dur: 3.0 },
    // e2 paso 1: pasillo peatonal libre; Ana lo usa
    { t: 'e2', o: 'c1', hacer: 'mover', hacia: [2.8, 0.91, -0.4], dur: 0.8 },
    { t: 'e2+0.4', a: 'ana', hacer: 'caminar', hacia: [1.0, 1.05], dur: 2.6, marca: 'ok' },
    { t: 'e2+3.1', a: 'ana', hacer: 'feliz', dur: 1.2 },
    // e3 paso 2: el jefe informa el riesgo a Pedro y Ana
    { t: 'e3', a: 'jefe', hacer: 'caminar', hacia: [1.4, -0.4], dur: 1.4 },
    { t: 'e3+0.2', a: 'pedro', hacer: 'caminar', hacia: [-0.2, -0.3], dur: 1.6 },
    { t: 'e3+1.6', a: 'jefe', hacer: 'apuntar', dur: 2.0, mirarA: 'pedro' },
    { t: 'e3+1.9', a: 'pedro', hacer: 'girar', rot: 0.9, dur: 0.4 },
    { t: 'e3+2.4', a: 'ana', hacer: 'girar', rot: -2.4, dur: 0.4 },
    // e4 paso 3: reglas claras; Ana espera en el cruce, la grúa pasa lento y luego cruza
    { t: 'e4', a: 'ana', hacer: 'caminar', hacia: [-0.4, 1.45], dur: 1.2 },
    { t: 'e4+1.3', a: 'ana', hacer: 'girar', rot: 0, dur: 0.3 },
    { t: 'e4+0.4', o: 'grua', hacer: 'mover', hacia: [-2.6, 0, 2.4], dur: 3.4 },
    { t: 'e4+4.0', a: 'ana', hacer: 'caminar', hacia: [-0.4, 3.3], dur: 1.2, marca: 'ok' },
    { t: 'e4+5.3', a: 'ana', hacer: 'saludo', dur: 1.2 },
    // e5 ley y e6 cierre: todos bien
    { t: 'e5+0.3', a: 'pedro', hacer: 'feliz', dur: 20 },
    { t: 'e5+0.3', a: 'ana', hacer: 'feliz', dur: 20 },
    { t: 'e5+0.3', a: 'jefe', hacer: 'saludo', dur: 20 },
  ],
  camara: [
    { t: 0, plano: 'medio', mirar: [-1.7, 1.9, 2.4], ang: 0.4 },
    { t: 'e0+1.6', plano: 'medio', mirar: [-1.4, 0, 2.6], ang: 0.5 },
    { t: 'e1', plano: 'general', mirar: [-0.4, 0, 2.0], ang: 0.35 },
    { t: 'e2', plano: 'medio', a: 'ana', ang: -0.3 },
    { t: 'e3', plano: 'medio', mirar: [0.6, 0, -0.2], ang: 0.4 },
    { t: 'e4', plano: 'medio', mirar: [-0.6, 0, 2.0], ang: 0.55 },
    { t: 'e5', plano: 'alto', mirar: [0, 0, 1.0], orbita: 0.06 },
    { t: 'e6', plano: 'general', mirar: [0, 0, 0.8], orbita: 0.05 },
  ],
};
