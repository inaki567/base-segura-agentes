// Reel 3D "Acto inseguro vs condición insegura" (8 escenas)
export default {
  escenario: 'bodega',
  actores: {
    pedro: { tipo: 'inseguro', pos: [-1.0, 0.4], rot: 0.3 },
    ana: { tipo: 'seguro', pos: [1.4, 0.8], rot: -0.3 },
  },
  objetos: {
    b1: { tipo: 'caja', pos: [0.2, 0.25, 1.9] }, b2: { tipo: 'caja', pos: [0.75, 0.25, 2.0] }, b3: { tipo: 'caja', pos: [0.45, 0.75, 1.95] },
  },
  pasos: [
    // e0 gancho: ¿la persona o el lugar?
    { t: 'e0+0.3', a: 'pedro', hacer: 'saludo', dur: 2.0 },
    { t: 'e0+0.3', a: 'ana', hacer: 'apuntar', dur: 2.2, mirarA: 'b3' },
    // e1 acto inseguro: Pedro, sin casco, trepa por la estantería
    { t: 'e1', a: 'pedro', hacer: 'caminar', hacia: [-2.1, -2.2], dur: 1.4 },
    { t: 'e1+1.4', a: 'pedro', hacer: 'girar', rot: Math.PI, dur: 0.4 },
    { t: 'e1+1.8', a: 'pedro', hacer: 'subir', altura: 1.0, dur: 1.2, marca: 'peligro' },
    { t: 'e1+3.0', a: 'pedro', hacer: 'tambalear', dur: 2.2 },
    // e2 condición insegura: una caja mal apilada cae y el pasillo está bloqueado
    { t: 'e2', a: 'pedro', hacer: 'subir', altura: 0, dur: 0.8 },
    { t: 'e2+0.9', a: 'pedro', hacer: 'girar', rot: 0.4, dur: 0.4 },
    { t: 'e2+0.6', o: 'caja_alta7', hacer: 'caer', avance: 1.3, lateral: 0.4, dur: 1.0, marca: 'peligro' },
    { t: 'e2+2.4', o: 'b3', hacer: 'mover', hacia: [0.45, 0.75, 1.95], dur: 2.5, marca: 'peligro' },
    // e3 se juntan las dos: Pedro pasa y casi le cae otra caja
    { t: 'e3', a: 'pedro', hacer: 'caminar', hacia: [-1.2, -1.45], dur: 1.0 },
    { t: 'e3+1.0', o: 'caja_alta5', hacer: 'caer', avance: 1.5, lateral: 0.3, dur: 0.8 },
    { t: 'e3+1.3', a: 'pedro', hacer: 'alerta', dur: 1.8, marca: 'peligro' },
    // e4 actos inseguros: capacitar y exigir EPP
    { t: 'e4', a: 'ana', hacer: 'caminar', hacia: [-0.1, -0.9], dur: 1.4 },
    { t: 'e4+1.4', a: 'ana', hacer: 'apuntar', dur: 2.2, mirarA: 'pedro', marca: 'ok' },
    { t: 'e4+1.4', a: 'pedro', hacer: 'girar', rot: 1.2, dur: 0.5 },
    // e5 condiciones inseguras: inspecciona y corrige (despeja el pasillo)
    { t: 'e5', a: 'ana', hacer: 'caminar', hacia: [0.5, 1.4], dur: 1.0 },
    { t: 'e5+1.0', a: 'ana', hacer: 'agacharse', dur: 0.6 },
    { t: 'e5+1.4', a: 'ana', hacer: 'cargar', objeto: 'b3', dur: 0.1 },
    { t: 'e5+1.6', a: 'ana', hacer: 'caminar', hacia: [2.0, 0.4], dur: 1.0 },
    { t: 'e5+2.6', a: 'ana', hacer: 'dejar', objeto: 'b3', en: [2.8, 1.41, -0.4], dur: 0.6, marca: 'ok' },
    // e6 ley y e7 cierre
    { t: 'e6', a: 'pedro', hacer: 'caminar', hacia: [0.6, 0.2], mirar: 0.2, dur: 1.4 },
    { t: 'e6+0.5', a: 'ana', hacer: 'caminar', hacia: [1.6, 0.4], mirar: -0.2, dur: 1.0 },
    { t: 'e6+1.6', a: 'ana', hacer: 'feliz', dur: 20 }, { t: 'e6+1.6', a: 'pedro', hacer: 'saludo', dur: 20 },
  ],
  camara: [
    { t: 0, plano: 'general', mirar: [0, 0, 0.4], ang: 0.25 },
    { t: 'e1', plano: 'medio', a: 'pedro', ang: 0.5 },
    { t: 'e2', plano: 'medio', mirar: [-1.6, 0, -1.6], ang: 0.2 },
    { t: 'e2+2.3', plano: 'cerca', a: 'b3', ang: 0.35 },
    { t: 'e3', plano: 'cerca', a: 'pedro', ang: 0.4 },
    { t: 'e4', plano: 'medio', mirar: [-0.6, 0, -1.0], ang: -0.2 },
    { t: 'e5', plano: 'medio', a: 'ana', ang: 0.5 },
    { t: 'e6', plano: 'alto', mirar: [0.6, 0, 0], orbita: 0.06 },
    { t: 'e7', plano: 'general', mirar: [0.6, 0, 0], orbita: 0.05 },
  ],
};
