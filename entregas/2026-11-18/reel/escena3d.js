// Reel 18-11-2026: cliente agresivo en el mostrador (Ley Karin, violencia de terceros, CT art. 2 letra c).
// Sin contacto físico: el cliente grita y apunta; la versión segura toma distancia y pide apoyo al jefe.
export default {
  escenario: 'local',
  actores: {
    vend: { tipo: 'inseguro', pos: [3.45, -2.0], rot: -0.45 },   // atiende sola, sin protocolo
    cliente: { tipo: 'cliente', pos: [2.6, -0.1], rot: 2.7 },     // grita y apunta desde el frente del mostrador
    ana: { tipo: 'seguro', pos: [7.5, -2.6], rot: -0.45 },        // versión CON protocolo (entra en e2)
    jefe: { tipo: 'jefe', pos: [-7.5, 1.0], rot: 1.2 },          // llega a apoyar (entra en e2)
  },
  objetos: {},
  pasos: [
    // fuera de cuadro las cajas de la entrada (tapaban el mostrador)
    { t: 0, o: 'caja1', hacer: 'mover', hacia: [-4.4, 0.25, -2.9], dur: 0.01 },
    { t: 0, o: 'caja2', hacer: 'mover', hacia: [-4.3, 0.75, -2.9], dur: 0.01 },
    { t: 0, o: 'caja3', hacer: 'mover', hacia: [-4.2, 1.25, -2.9], dur: 0.01 },
    // e0 gancho: el cliente apunta y grita; la vendedora se asusta
    { t: 'e0', a: 'cliente', hacer: 'apuntar', dur: 4.2, mirarA: 'vend', marca: 'peligro' },
    { t: 'e0+0.6', a: 'vend', hacer: 'alerta', dur: 3.2, mirarA: 'cliente' },
    // e1 la situación: el cliente sigue apuntando; ella sale a encararlo y queda sola
    { t: 'e1', a: 'cliente', hacer: 'tambalear', dur: 0.8 },
    { t: 'e1+0.8', a: 'cliente', hacer: 'apuntar', dur: 5.2, mirarA: 'vend' },
    { t: 'e1', a: 'vend', hacer: 'alerta', dur: 0.7, mirarA: 'cliente' },
    { t: 'e1+0.6', a: 'vend', hacer: 'caminar', hacia: [1.6, -2.1], dur: 1.2 },
    { t: 'e1+1.8', a: 'vend', hacer: 'caminar', hacia: [1.8, -0.4], dur: 1.1 },
    { t: 'e1+2.9', a: 'vend', hacer: 'girar', rot: 1.4, dur: 0.4 },
    { t: 'e1+3.4', a: 'vend', hacer: 'alerta', dur: 2.6, mirarA: 'cliente', marca: 'peligro' },
    // e2 paso 1 (versión correcta): se cambia el elenco
    { t: 'e2-0.05', a: 'vend', hacer: 'caminar', hacia: [-8, -2.5], dur: 0.05 },
    { t: 'e2-0.05', a: 'ana', hacer: 'caminar', hacia: [3.45, -2.0], dur: 0.05 },
    { t: 'e2-0.02', a: 'ana', hacer: 'girar', rot: -0.45, dur: 0.02 },
    { t: 'e2-0.05', a: 'jefe', hacer: 'caminar', hacia: [-0.6, -1.4], dur: 0.05 },
    { t: 'e2', a: 'cliente', hacer: 'apuntar', dur: 2.6, mirarA: 'ana' },
    { t: 'e2+0.4', a: 'ana', hacer: 'caminar', hacia: [3.9, -2.6], dur: 0.9 },
    { t: 'e2+1.3', a: 'ana', hacer: 'girar', rot: -0.45, dur: 0.4 },
    { t: 'e2+1.8', a: 'ana', hacer: 'saludo', dur: 1.2, marca: 'ok' },          // pide apoyo con la mano
    { t: 'e2+1.6', a: 'jefe', hacer: 'caminar', hacia: [2.0, -0.7], dur: 1.6 },
    { t: 'e2+3.3', a: 'jefe', hacer: 'girar', rot: 1.6, dur: 0.4 },
    { t: 'e2+3.7', a: 'jefe', hacer: 'apuntar', dur: 2.0, mirarA: 'cliente', marca: 'ok' },  // indica la salida
    { t: 'e2+4.2', a: 'cliente', hacer: 'caminar', hacia: [0.6, 3.0], dur: 2.4 },
    // e3 paso 2: registrar en el mostrador con el jefe al lado
    { t: 'e3-0.05', a: 'cliente', hacer: 'caminar', hacia: [-8, 5], dur: 0.05 },
    { t: 'e3', a: 'jefe', hacer: 'caminar', hacia: [2.55, -2.45], dur: 1.2 },
    { t: 'e3+1.2', a: 'jefe', hacer: 'girar', rot: 1.2, dur: 0.4 },
    { t: 'e3+0.2', a: 'ana', hacer: 'caminar', hacia: [3.45, -2.0], dur: 0.8 },
    { t: 'e3+1.0', a: 'ana', hacer: 'girar', rot: -0.3, dur: 0.3 },
    { t: 'e3+1.4', a: 'ana', hacer: 'agacharse', dur: 1.6, marca: 'ok' },     // escribe el registro
    { t: 'e3+3.8', a: 'ana', hacer: 'girar', rot: -1.4, dur: 0.4 },
    { t: 'e3+4.3', a: 'ana', hacer: 'saludo', dur: 1.6, mirarA: 'jefe' },     // avisa al jefe
    // e4 paso 3: protocolo al día; el jefe lo muestra y ella está tranquila
    { t: 'e4', a: 'jefe', hacer: 'caminar', hacia: [1.6, -1.6], dur: 1.0 },
    { t: 'e4+1.0', a: 'jefe', hacer: 'girar', rot: 0.2, dur: 0.3 },
    { t: 'e4+1.3', a: 'jefe', hacer: 'apuntar', dur: 2.6, mirarA: 'ana' },
    { t: 'e4+0.6', a: 'ana', hacer: 'girar', rot: -0.6, dur: 0.4 },
    { t: 'e4+1.5', a: 'ana', hacer: 'feliz', dur: 3.5, marca: 'ok' },
    // e5 ley y e6 cierre: local tranquilo
    { t: 'e5+0.3', a: 'ana', hacer: 'feliz', dur: 20 },
    { t: 'e5+0.3', a: 'jefe', hacer: 'saludo', dur: 20 },
  ],
  camara: [
    { t: 0, plano: 'medio', mirar: [2.25, 0, -3.4], ang: 0.3 },
    { t: 'e1', plano: 'general', mirar: [2.3, 0, -1.0], ang: 0.45 },
    { t: 'e1+3.0', plano: 'medio', mirar: [2.6, 0, -1.6], ang: -0.4 },
    { t: 'e2', plano: 'medio', mirar: [3.0, 0, -1.6], ang: -0.25 },
    { t: 'e2+4.0', plano: 'general', mirar: [2.0, 0, 0.0], ang: 0.2 },
    { t: 'e3', plano: 'medio', mirar: [3.1, 0, -2.6], ang: 0.1 },
    { t: 'e4', plano: 'medio', mirar: [2.4, 0, -1.8], ang: 0.25 },
    { t: 'e5', plano: 'alto', mirar: [2.9, 0, -0.6], ang: -0.1, orbita: 0.04 },
    { t: 'e6', plano: 'general', mirar: [1.2, 0, -1.2], orbita: 0.05 },
  ],
};
