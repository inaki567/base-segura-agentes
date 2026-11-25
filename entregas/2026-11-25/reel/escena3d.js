// Reel 25-11-2026: trabajador que se niega a usar casco y arnés en el andamio (Ley 16.744 art. 67; CT arts. 154 N° 10 y 157).
// Pedro (inseguro) sube sin EPP; Ana (segura, supervisora) detiene la tarea, explica y aplica el reglamento.
// En el paso 3 Pedro pasa detrás de la caseta y reaparece equipado (pedroOk) para subir de nuevo, ahora seguro.
export default {
  escenario: 'obra',
  actores: {
    pedro: { tipo: 'inseguro', pos: [0.4, 0.6], rot: 0.2 },
    ana: { tipo: 'seguro', pos: [2.6, 1.2], rot: -0.9 },
    pedroOk: { tipo: 'seguro', pos: [4.4, -4.6], rot: 0 },        // Pedro ya con casco y chaleco, escondido tras la caseta
  },
  objetos: {
    reglamento: { tipo: 'caja', color: '#f4f4f4', pos: [2.1, 0.25, 1.6] },  // carpeta del reglamento interno
  },
  pasos: [
    // la excavadora queda al fondo a la derecha para no tapar a nadie
    { t: 0, o: 'excavadora', hacer: 'mover', hacia: [6.2, 0, -2.4], dur: 0.01 },
    // e0 gancho: Pedro, sin EPP, preocupado
    { t: 0, a: 'pedro', hacer: 'alerta', dur: 4.4, marca: 'peligro' },
    // e1 sube al andamio sin casco ni arnés y se tambalea; Ana le ofrece el EPP
    { t: 'e1', a: 'pedro', hacer: 'caminar', hacia: [-1.0, -1.3], dur: 1.2 },
    { t: 'e1+1.2', a: 'pedro', hacer: 'subir', altura: 1.6, dur: 1.2 },
    { t: 'e1+2.4', a: 'pedro', hacer: 'girar', rot: 0.3, dur: 0.3 },
    { t: 'e1+2.6', a: 'pedro', hacer: 'tambalear', dur: 2.2, marca: 'peligro' },
    { t: 'e1+0.6', a: 'ana', hacer: 'caminar', hacia: [0.9, 0.5], dur: 1.4 },
    { t: 'e1+2.1', a: 'ana', hacer: 'apuntar', dur: 2.6, mirarA: 'pedro' },
    // e2 paso 1: Ana detiene la tarea, Pedro baja, se cierra el acceso y conversan
    { t: 'e2', a: 'ana', hacer: 'saludo', dur: 1.4, mirarA: 'pedro' },
    { t: 'e2+0.3', a: 'pedro', hacer: 'subir', altura: 0, dur: 1.1 },
    { t: 'e2+1.5', a: 'pedro', hacer: 'caminar', hacia: [0.0, 0.7], dur: 1.0, mirar: 1.57 },
    { t: 'e2+0.6', o: 'valla', hacer: 'mover', hacia: [-1.0, 0, -0.35], dur: 1.2 },
    { t: 'e2+1.6', a: 'ana', hacer: 'caminar', hacia: [1.3, 0.7], dur: 0.8, mirar: -1.57 },
    { t: 'e2+2.6', a: 'ana', hacer: 'apuntar', dur: 2.2, mirarA: 'pedro', marca: 'ok' },
    // e3 paso 2: amonestación según el reglamento interno
    { t: 'e3+0.2', a: 'ana', hacer: 'caminar', hacia: [2.0, 1.35], dur: 1.0 },
    { t: 'e3+1.2', a: 'ana', hacer: 'agacharse', dur: 0.6 },
    { t: 'e3+1.5', a: 'ana', hacer: 'cargar', objeto: 'reglamento', dur: 0.1 },
    { t: 'e3+1.9', a: 'ana', hacer: 'caminar', hacia: [1.2, 0.8], dur: 1.0, mirar: -1.57 },
    { t: 'e3+3.0', a: 'ana', hacer: 'dejar', objeto: 'reglamento', en: [0.6, 0.25, 0.85], dur: 0.6 },
    { t: 'e3+3.7', a: 'ana', hacer: 'apuntar', dur: 2.6, mirarA: 'pedro', marca: 'ok' },
    { t: 'e3+3.4', a: 'pedro', hacer: 'agacharse', dur: 1.8 },
    // e4 paso 3: multa (máx. 25 %); Pedro va a equiparse y vuelve a subir con casco
    { t: 'e4+0.2', a: 'pedro', hacer: 'caminar', hacia: [4.2, -4.4], dur: 2.0 },
    { t: 'e4+2.3', a: 'pedro', hacer: 'caminar', hacia: [9.0, -4.6], dur: 0.6 },
    { t: 'e4+2.4', a: 'pedroOk', hacer: 'caminar', hacia: [-1.0, -1.3], dur: 2.4 },
    { t: 'e4+4.8', a: 'pedroOk', hacer: 'subir', altura: 1.6, dur: 1.0 },
    { t: 'e4+5.8', a: 'pedroOk', hacer: 'girar', rot: 0.3, dur: 0.3 },
    { t: 'e4+6.0', a: 'pedroOk', hacer: 'feliz', dur: 1.6, marca: 'ok' },
    { t: 'e4+0.5', a: 'ana', hacer: 'girar', rot: -0.6, dur: 0.5 },
    { t: 'e4+5.0', a: 'ana', hacer: 'saludo', dur: 2.5, mirarA: 'pedroOk' },
    // e5 ley y e6 cierre: obra ordenada, todos bien
    { t: 'e5+0.3', a: 'pedroOk', hacer: 'feliz', dur: 20 },
    { t: 'e5', a: 'ana', hacer: 'caminar', hacia: [0.7, -0.4], dur: 1.2, mirar: 0 },
    { t: 'e5+1.3', a: 'ana', hacer: 'saludo', dur: 20 },
  ],
  camara: [
    { t: 0, plano: 'cerca', mirar: [-0.05, 0, -0.85], ang: 0.3 },
    { t: 'e1', plano: 'general', mirar: [-0.4, 0, -0.9], ang: 0.4 },
    { t: 'e1+2.6', plano: 'medio', mirar: [-0.9, 0, -2.9], ang: 0.3 },
    { t: 'e2', plano: 'medio', mirar: [0.3, 0, -0.6], ang: -0.25 },
    { t: 'e3', plano: 'medio', mirar: [1.0, 0, 0.0], ang: -0.45 },
    { t: 'e4', plano: 'general', mirar: [1.1, 0, -2.4], ang: -0.25 },
    { t: 'e5', plano: 'general', mirar: [-0.3, 0, -2.4], ang: 0.05, orbita: 0.03 },
    { t: 'e6', plano: 'general', mirar: [0.3, 0, 0], orbita: 0.05 },
  ],
};
