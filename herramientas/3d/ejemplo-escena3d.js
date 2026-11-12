// Ejemplo completo: reel "sacos de 50 kg al hombro" (9 escenas, ver entregas/2026-11-09/reel/guion.json).
// 'e3' = inicio de la escena 3 según reel/tiempos.json; 'e3+1.5' = 1,5 s después.
export default {
  escenario: 'bodega',
  actores: {
    pedro: { tipo: 'inseguro', pos: [-0.6, 0.9], rot: 0.5 },     // trabajador sin EPP: polera roja, sin casco
    ana: { tipo: 'seguro', pos: [5.5, 1.2], rot: -1.6 },          // trabajadora segura: reflectante azul, casco blanco
    jefe: { tipo: 'jefe', pos: [-3.2, 1.6], rot: 0.9 },
  },
  objetos: {
    pal: { tipo: 'pallet', pos: [0.9, 0.08, -0.7] },
    s1: { tipo: 'saco', pos: [0.6, 0.29, -0.7] }, s2: { tipo: 'saco', pos: [1.25, 0.29, -0.7] }, s3: { tipo: 'saco', pos: [0.9, 0.56, -0.7] },
    carro: { tipo: 'carro', pos: [6.5, 0, 1.2] },
  },
  pasos: [
    // e0 gancho: Pedro ya con el saco, se tambalea
    { t: 'e0', a: 'pedro', hacer: 'cargar', objeto: 's3', dur: 0.1 },
    { t: 'e0+0.3', a: 'pedro', hacer: 'tambalear', dur: 5.5, marca: 'peligro' },
    { t: 'e1-0.3', a: 'pedro', hacer: 'dejar', objeto: 's3', dur: 0.6 },
    // e1 el jefe le pide bajar los sacos
    { t: 'e1+0.4', a: 'jefe', hacer: 'apuntar', dur: 4, mirarA: 'pedro' },
    { t: 'e1+0.6', a: 'pedro', hacer: 'girar', rot: -0.6, dur: 0.6 },
    // e2 levanta el saco y siente el tirón
    { t: 'e2', a: 'pedro', hacer: 'girar', rot: 0.6, dur: 0.4 },
    { t: 'e2+0.4', a: 'pedro', hacer: 'agacharse', dur: 0.9 },
    { t: 'e2+1.0', a: 'pedro', hacer: 'cargar', objeto: 's3', dur: 0.1 },
    { t: 'e2+1.6', a: 'pedro', hacer: 'tambalear', dur: 4.2, marca: 'peligro' },
    { t: 'e3-0.6', a: 'pedro', hacer: 'dejar', objeto: 's3', dur: 0.6 },
    // e3 uno: usar carro
    { t: 'e3', a: 'ana', hacer: 'empujar', hacia: [2.4, 1.2], dur: 3.2 },
    { t: 'e3', o: 'carro', hacer: 'mover', hacia: [1.4, 0, 1.2], dur: 3.2 },
    { t: 'e3+3.3', a: 'ana', hacer: 'feliz', dur: 1.6, marca: 'ok' },
    // e4 dos: máximo 25 kg — Ana carga un saco liviano sin problema
    { t: 'e4+0.3', a: 'ana', hacer: 'caminar', hacia: [1.2, 0.2], dur: 1.2 },
    { t: 'e4+1.6', a: 'ana', hacer: 'agacharse', dur: 0.8 },
    { t: 'e4+2.3', a: 'ana', hacer: 'cargar', objeto: 's1', dur: 0.1 },
    { t: 'e4+2.6', a: 'ana', hacer: 'feliz', dur: 0.1, marca: 'ok' },
    { t: 'e5-0.6', a: 'ana', hacer: 'dejar', objeto: 's1', en: [1.4, 0.56, 1.2], dur: 0.6 },
    // e5 tres: repartir el peso entre dos y técnica
    { t: 'e5+0.2', a: 'pedro', hacer: 'caminar', hacia: [0.4, 0.4], dur: 1.0 },
    { t: 'e5+1.3', a: 'pedro', hacer: 'agacharse', dur: 1.4 }, { t: 'e5+1.3', a: 'ana', hacer: 'agacharse', dur: 1.4 },
    { t: 'e5+3.0', a: 'pedro', hacer: 'feliz', dur: 2.5 }, { t: 'e5+3.0', a: 'ana', hacer: 'saludo', dur: 2.5 },
    // e6 cuatro: matriz y capacitación
    { t: 'e6', a: 'jefe', hacer: 'caminar', hacia: [-1.2, 1.8], dur: 1.4 },
    { t: 'e6+1.5', a: 'jefe', hacer: 'apuntar', dur: 2.5, mirarA: 'ana', marca: 'ok' },
    // e7 ley y e8 cierre: todos felices
    { t: 'e7+0.5', a: 'pedro', hacer: 'feliz', dur: 15 }, { t: 'e7+0.5', a: 'ana', hacer: 'feliz', dur: 15 }, { t: 'e7+0.5', a: 'jefe', hacer: 'saludo', dur: 15 },
  ],
  camara: [
    { t: 0, plano: 'cerca', a: 'pedro', ang: 0.3 },
    { t: 'e1', plano: 'general', mirar: [-1, 0, 0.5], ang: 0.5 },
    { t: 'e2', plano: 'medio', a: 'pedro', ang: 0.2 },
    { t: 'e2+1.6', plano: 'cerca', a: 'pedro', ang: 0.45 },
    { t: 'e3', plano: 'medio', a: 'carro', ang: -0.2 },
    { t: 'e4', plano: 'medio', a: 'ana', ang: 0.5 },
    { t: 'e5', plano: 'medio', mirar: [0.8, 0, 0.3], ang: 0.6 },
    { t: 'e6', plano: 'general', mirar: [0, 0, 0.6], ang: -0.3 },
    { t: 'e7', plano: 'alto', mirar: [0, 0, 0], orbita: 0.06 },
    { t: 'e8', plano: 'general', mirar: [0, 0, 0], orbita: 0.05 },
  ],
};
