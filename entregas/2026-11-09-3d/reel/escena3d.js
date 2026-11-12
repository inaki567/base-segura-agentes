// Reel 3D "sacos de 50 kg al hombro" (8 escenas, máx. 45 s)
export default {
  escenario: 'bodega',
  actores: {
    pedro: { tipo: 'inseguro', pos: [0.2, 0.3], rot: 0.4 },
    ana: { tipo: 'seguro', pos: [5.5, 1.3], rot: -1.6 },
  },
  objetos: {
    pal: { tipo: 'pallet', pos: [0.9, 0.08, -0.8] },
    s1: { tipo: 'saco', pos: [0.6, 0.29, -0.8] }, s2: { tipo: 'saco', pos: [1.25, 0.29, -0.8] }, s3: { tipo: 'saco', pos: [0.9, 0.56, -0.8] },
    carro: { tipo: 'carro', pos: [6.6, 0, 1.3] },
    c1: { tipo: 'saco', pos: [6.35, 0.51, 1.1] }, c2: { tipo: 'saco', pos: [6.35, 0.51, 1.5] },
  },
  pasos: [
    // e0 gancho: Pedro con el saco al hombro, tambaleando
    { t: 0, a: 'pedro', hacer: 'cargar', objeto: 's3', dur: 0.1 },
    { t: 'e0+0.2', a: 'pedro', hacer: 'tambalear', dur: 5.4, marca: 'peligro' },
    // e1 lleva el saco caminando
    { t: 'e1+0.2', a: 'pedro', hacer: 'caminar', hacia: [-1.6, 1.4], dur: 2.4 },
    { t: 'e1+2.8', a: 'pedro', hacer: 'caminar', hacia: [0.2, 0.3], mirar: 0.4, dur: 1.8 },
    // e2 tirón en la espalda
    { t: 'e2+0.3', a: 'pedro', hacer: 'tambalear', dur: 1.6, marca: 'peligro' },
    { t: 'e2+1.9', a: 'pedro', hacer: 'dejar', objeto: 's3', dur: 0.6 },
    { t: 'e2+2.6', a: 'pedro', hacer: 'alerta', dur: 2.2 },
    // e3 uno: carro
    { t: 'e3', a: 'ana', hacer: 'empujar', hacia: [2.8, 1.3], dur: 2.8 },
    { t: 'e3', o: 'carro', hacer: 'mover', hacia: [1.75, 0, 1.3], dur: 2.8 },
    { t: 'e3', o: 'c1', hacer: 'mover', hacia: [1.5, 0.51, 1.1], dur: 2.8 },
    { t: 'e3', o: 'c2', hacer: 'mover', hacia: [1.5, 0.51, 1.5], dur: 2.8 },
    { t: 'e3+2.9', a: 'ana', hacer: 'feliz', dur: 1.0, marca: 'ok' },
    // e4 dos: máximo 25 kg
    { t: 'e4+0.1', a: 'ana', hacer: 'caminar', hacia: [1.5, 0.1], dur: 1.0 },
    { t: 'e4+1.1', a: 'ana', hacer: 'agacharse', dur: 0.7 },
    { t: 'e4+1.6', a: 'ana', hacer: 'cargar', objeto: 's1', dur: 0.1 },
    { t: 'e4+2.1', a: 'ana', hacer: 'saludo', dur: 1.2, marca: 'ok' },
    { t: 'e5-0.5', a: 'ana', hacer: 'dejar', objeto: 's1', en: [2.0, 0.78, 1.3], dur: 0.5 },
    // e5 tres: entre dos y espalda recta
    { t: 'e5+0.1', a: 'pedro', hacer: 'caminar', hacia: [0.3, 0.1], mirar: 1.0, dur: 0.9 },
    { t: 'e5+0.1', a: 'ana', hacer: 'girar', rot: -1.0, dur: 0.6 },
    { t: 'e5+1.0', a: 'pedro', hacer: 'agacharse', dur: 1.4 }, { t: 'e5+1.0', a: 'ana', hacer: 'agacharse', dur: 1.4 },
    { t: 'e5+2.5', a: 'pedro', hacer: 'feliz', dur: 1.8, marca: 'ok' }, { t: 'e5+2.5', a: 'ana', hacer: 'feliz', dur: 1.8 },
    // e6 ley y e7 cierre
    { t: 'e6+0.3', a: 'pedro', hacer: 'girar', rot: 0.3, dur: 0.6 }, { t: 'e6+0.3', a: 'ana', hacer: 'girar', rot: -0.3, dur: 0.6 },
    { t: 'e6+0.5', a: 'pedro', hacer: 'saludo', dur: 20 }, { t: 'e6+0.5', a: 'ana', hacer: 'feliz', dur: 20 },
  ],
  camara: [
    { t: 0, plano: 'cerca', a: 'pedro', ang: 0.15 },
    { t: 'e1', plano: 'general', mirar: [-0.5, 0, 0.6], ang: 0.55 },
    { t: 'e2', plano: 'cerca', a: 'pedro', ang: 0.5 },
    { t: 'e3', plano: 'medio', a: 'carro', ang: -0.25 },
    { t: 'e4', plano: 'medio', a: 'ana', ang: 0.45 },
    { t: 'e5', plano: 'medio', mirar: [0.9, 0, 0.2], ang: 0.05 },
    { t: 'e6', plano: 'alto', mirar: [0.8, 0, 0.5], orbita: 0.06 },
    { t: 'e7', plano: 'general', mirar: [0.8, 0, 0.5], orbita: 0.05 },
  ],
};
