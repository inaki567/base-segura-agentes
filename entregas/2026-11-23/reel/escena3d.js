// Reel 23-11-2026: corte con cartonero en la bodega (Código del Trabajo art. 184).
// El corte se sugiere (alerta, brillo rojo, pastilla); nada de sangre.
export default {
  escenario: 'bodega',
  actores: {
    pedro: { tipo: 'inseguro', pos: [-0.8, -0.35], rot: 0 },     // abre cajas sin guantes, corta hacia el cuerpo
    ana: { tipo: 'seguro', pos: [-3.7, -2.0], rot: 0.6 },          // guantes, botiquín, traslado a la mutual
  },
  objetos: {
    mesa: { tipo: 'mostrador', pos: [-0.8, 0, 0.45], rot: Math.PI },   // mesa de embalaje
    cj: { tipo: 'caja', pos: [-0.6, 1.31, 0.45] },                      // caja que Pedro abre
    botiquin: { tipo: 'caja', color: '#25D366', pos: [-4.3, 1.3, -3.5] }, // botiquín verde en el muro
  },
  pasos: [
    // e0 gancho: Pedro se mira la mano, alarmado
    { t: 0, a: 'pedro', hacer: 'agacharse', dur: 0.9 },
    { t: 'e0+0.6', a: 'pedro', hacer: 'alerta', dur: 3.0, marca: 'peligro' },
    // e1 rebobinado: abre la caja apurado y la hoja se resbala
    { t: 'e1+0.1', a: 'pedro', hacer: 'agacharse', dur: 2.2 },
    { t: 'e1+2.3', a: 'pedro', hacer: 'tambalear', dur: 2.2, marca: 'peligro' },
    { t: 'e1+2.4', a: 'pedro', hacer: 'alerta', dur: 2.0 },
    // e2 paso 1: Ana toma el botiquín y lo atiende
    { t: 'e2', a: 'ana', hacer: 'cargar', objeto: 'botiquin', dur: 0.1 },
    { t: 'e2+0.4', a: 'ana', hacer: 'correr', hacia: [-1.9, -0.6], dur: 1.6 },
    { t: 'e2+2.0', a: 'ana', hacer: 'dejar', objeto: 'botiquin', en: [-1.75, 1.31, 0.45], dur: 0.6 },
    { t: 'e2+2.6', a: 'ana', hacer: 'girar', rot: 1.4, dur: 0.3 },
    { t: 'e2+2.9', a: 'ana', hacer: 'agacharse', dur: 1.5, mirarA: 'pedro', marca: 'ok' },
    { t: 'e2+0.5', a: 'pedro', hacer: 'girar', rot: -1.2, dur: 0.6 },
    { t: 'e2+0.2', a: 'pedro', hacer: 'tambalear', dur: 4.2 },
    // e3 paso 2: Ana lo acompaña a la salida (mutual / ISL)
    { t: 'e3+0.2', a: 'pedro', hacer: 'caminar', hacia: [3.0, -2.9], dur: 3.6 },
    { t: 'e3+0.2', a: 'ana', hacer: 'caminar', hacia: [2.2, -2.6], dur: 3.6 },
    { t: 'e3+3.9', a: 'pedro', hacer: 'caminar', hacia: [6.5, -2.9], dur: 1.2 },
    // e4 paso 3: Ana abre una caja bien, con guantes y hoja hacia afuera
    { t: 'e4', a: 'ana', hacer: 'caminar', hacia: [4.0, -0.35], dur: 1.6, mirar: -1.57 },
    
    { t: 'e4+2.0', a: 'ana', hacer: 'agacharse', dur: 3.0, marca: 'ok' },
    
    { t: 'e4+5.1', a: 'ana', hacer: 'girar', rot: -0.5, dur: 0.4 },
    { t: 'e4+5.5', a: 'ana', hacer: 'feliz', dur: 2.2 },
    // e5 ley y e6 cierre: Pedro vuelve atendido, todos bien
    { t: 'e5', a: 'pedro', hacer: 'caminar', hacia: [1.4, 0.9], dur: 2.0, mirar: 0 },
    { t: 'e5+0.2', a: 'ana', hacer: 'caminar', hacia: [2.6, 1.0], dur: 1.2, mirar: 0 },
    { t: 'e5+2.2', a: 'pedro', hacer: 'feliz', dur: 20 },
    { t: 'e5+1.6', a: 'ana', hacer: 'saludo', dur: 20 },
  ],
  camara: [
    { t: 0, plano: 'cerca', mirar: [-0.8, 0, -2.6], ang: 0.2 },
    { t: 'e1', plano: 'general', mirar: [-1.2, 0, -0.4], ang: 0.45 },
    { t: 'e1+2.3', plano: 'medio', a: 'pedro', ang: 0.3 },
    { t: 'e2', plano: 'medio', mirar: [-2.4, 0, -0.9], ang: -0.35 },
    { t: 'e3', plano: 'medio', a: 'pedro', ang: 0.5 },
    { t: 'e4', plano: 'medio', a: 'ana', ang: 0.6 },
    { t: 'e4+2.0', plano: 'medio', mirar: [3.6, 0, -0.9], ang: 0.35 },
    { t: 'e5', plano: 'alto', mirar: [1.6, 0, 2.8], ang: 0.2, orbita: 0.05 },
    { t: 'e6', plano: 'general', mirar: [0.5, 0, 0.4], orbita: 0.05 },
  ],
};
