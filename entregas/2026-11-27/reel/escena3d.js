// Reel 27-11-2026: restaurante al cierre. Carla (insegura, polera roja, sin EPP) mezcla cloro con otro producto en un balde
// y sale vapor tóxico. Diego (seguro, reflectante azul y casco blanco) la saca al aire libre, ventila, llama a la mutual/ISL
// y ordena los productos en su envase original con etiqueta (DS 44, art. 15 N° 4; DS 594, art. 42).
//
// El motor no trae balde, vapor, mesas ni letreros de restaurante: este archivo agrega esos elementos a la escena
// sin tocar herramientas/3d/motor.js (captura la escena al primer scene.add y se actualiza en cada window.renderAt).
import * as THREE from 'three';

// ---------- tiempos ----------
const E = (i, d = 0) => (window.TIEMPOS?.escenas?.[i]?.inicio ?? 0) + d;
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (t, a, b) => cl((t - a) / (b - a));
const eo = x => 1 - Math.pow(1 - x, 3);
const pop = (t, a, b) => {  // aparece con rebote en a, desaparece en b
  if (t < a || t > b) return 0;
  const k = seg(t, a, a + 0.35); const s = k < 1 ? eo(k) * (1 + 0.25 * Math.sin(Math.PI * k)) : 1;
  return s * (1 - eo(seg(t, b - 0.25, b)));
};

// ---------- utilidades de modelado ----------
const mat = (c, r = 0.45, extra = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: r, ...extra });
const caja = (w, h, d, c, x, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat(c)); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; return m; };
const cil = (rt, rb, h, c, x, y, z) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, 24), mat(c)); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; return m; };

function lienzo(w, h, dibujar) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h; dibujar(cv.getContext('2d'), w, h);
  const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 4; return tx;
}
const redondo = (g, x, y, w, h, r) => { g.beginPath(); g.roundRect(x, y, w, h, r); };
function etiqueta(tx, ancho, alto) {  // sprite siempre de frente a la cámara y encima de todo
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tx, transparent: true, depthTest: false }));
  s.renderOrder = 20; s.userData.base = [ancho, alto]; s.scale.set(ancho, alto, 1); return s;
}
function pastilla3d(txt, bg, fg, ancho) {
  const W = 1024, H = 190;
  const tx = lienzo(W, H, (g) => {
    g.font = '800 82px Outfit, sans-serif'; const tw = Math.min(W - 40, g.measureText(txt).width + 110);
    g.fillStyle = 'rgba(0,0,0,.35)'; redondo(g, (W - tw) / 2, 30, tw, H - 36, 80); g.fill();
    g.fillStyle = bg; redondo(g, (W - tw) / 2, 8, tw, H - 36, 80); g.fill();
    g.fillStyle = fg; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(txt, W / 2, 8 + (H - 36) / 2 + 4, W - 90);
  });
  return etiqueta(tx, ancho, ancho * H / W);
}

// ---------- elementos extra ----------
function armar(scene) {
  const X = {}; const g = new THREE.Group(); scene.add(g);

  // letrero del local: FERRETERÍA -> RESTAURANTE
  scene.traverse(o => {
    if (o.isMesh && o.geometry?.type === 'BoxGeometry' && o.geometry.parameters.width === 3.6 && Array.isArray(o.material)) {
      o.material[4].map = lienzo(1024, 199, (c, w, h) => { c.fillStyle = '#F2A33A'; c.fillRect(0, 0, w, h); c.fillStyle = '#fff'; c.font = '900 110px Outfit, sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('RESTAURANTE', w / 2, h / 2 + 4); });
      o.material[4].needsUpdate = true; o.position.y = 2.75;
    }
  });

  // mesón de cocina (acero) al fondo izquierdo
  g.add(caja(2.2, 0.9, 0.7, '#b8c0cc', -1.2, 0.45, -2.55)); g.add(caja(2.3, 0.06, 0.78, '#dfe4ea', -1.2, 0.93, -2.55));
  g.add(cil(0.22, 0.22, 0.3, '#8a929e', -1.7, 1.11, -2.55)); g.add(cil(0.16, 0.16, 0.22, '#8a929e', -0.8, 1.07, -2.55));

  // mesas del comedor con sillas arriba (hora del cierre)
  const mesa = (x, z) => {
    const m = new THREE.Group(); m.position.set(x, 0, z); g.add(m);
    m.add(caja(1.1, 0.06, 0.8, '#a8763e', 0, 0.75, 0));
    for (const [a, b] of [[-0.48, -0.33], [0.48, -0.33], [-0.48, 0.33], [0.48, 0.33]]) m.add(caja(0.06, 0.72, 0.06, '#6b4a2a', a, 0.36, b));
    for (const s of [-1, 1]) {  // silla de patas arriba
      const si = new THREE.Group(); si.position.set(s * 0.27, 0.8, 0); m.add(si);
      si.add(caja(0.42, 0.05, 0.42, '#d9534f', 0, 0.03, 0));
      for (const [a, b] of [[-0.18, -0.18], [0.18, -0.18], [-0.18, 0.18], [0.18, 0.18]]) si.add(caja(0.04, 0.42, 0.04, '#333', a, 0.26, b));
      si.add(caja(0.42, 0.4, 0.04, '#d9534f', 0, -0.0, s * 0.0 + 0.2).translateY(0));
    }
  };
  mesa(2.3, 2.3); mesa(4.3, 2.3); mesa(3.7, 0.2);

  // ventana en el muro del fondo (se abre en el paso 1)
  g.add(caja(1.6, 1.2, 0.06, '#33415a', -4.6, 1.9, -3.73));
  const cielo = caja(1.44, 1.04, 0.02, '#bfe6ff', -4.6, 1.9, -3.69); cielo.material.emissive = new THREE.Color('#9fd4ff'); cielo.material.emissiveIntensity = 0.6; g.add(cielo);
  const hoja = (lado) => {
    const p = new THREE.Group(); p.position.set(-4.6 + lado * 0.72, 1.9, -3.66); g.add(p);
    const v = new THREE.Mesh(new THREE.BoxGeometry(0.72, 1.04, 0.03), mat('#7fc4f0', 0.1, { transparent: true, opacity: 0.55 })); v.position.x = -lado * 0.36; p.add(v);
    p.add(caja(0.05, 1.04, 0.05, '#e9eef2', -lado * 0.7, 0, 0)); return p;
  };
  X.hojaI = hoja(-1); X.hojaD = hoja(1);

  // salida al patio: marco de puerta, pasto, árbol y letrero SALIDA
  g.add(caja(2.3, 0.03, 2.3, '#5fb860', -4.35, 0.06, 2.85));
  for (const z of [1.75, 3.35]) g.add(caja(0.14, 2.3, 0.14, '#e9e2d4', -3.05, 1.15, z));
  g.add(caja(0.14, 0.14, 1.74, '#e9e2d4', -3.05, 2.3, 2.55));
  const sal = caja(0.06, 0.32, 1.0, '#25D366', -3.05, 2.55, 2.55); sal.material = [mat('#25D366'), mat('#25D366'), mat('#25D366'), mat('#25D366'), mat('#25D366'), mat('#25D366')];
  sal.material[0].map = lienzo(512, 164, (c, w, h) => { c.fillStyle = '#25D366'; c.fillRect(0, 0, w, h); c.fillStyle = '#fff'; c.font = '900 110px Outfit, sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('SALIDA', w / 2, h / 2 + 4); });
  sal.material[1].map = sal.material[0].map; g.add(sal);
  g.add(cil(0.1, 0.12, 1.2, '#6b4a2a', -5.1, 0.6, 1.95)); const copa = new THREE.Mesh(new THREE.SphereGeometry(0.6, 24, 16), mat('#3f9e4a', 0.7)); copa.position.set(-5.1, 1.6, 1.95); copa.castShadow = true; g.add(copa);

  // balde con la mezcla
  X.balde = new THREE.Group(); X.balde.position.set(-0.45, 0, 0.85); g.add(X.balde);
  const b = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.22, 0.42, 28, 1, true), mat('#2f6fd1', 0.5, { side: THREE.DoubleSide })); b.position.y = 0.21; b.castShadow = true; X.balde.add(b);
  X.balde.add(cil(0.22, 0.22, 0.02, '#2f6fd1', 0, 0.01, 0));
  const liq = cil(0.255, 0.255, 0.02, '#c9e86a', 0, 0.34, 0); liq.material.emissive = new THREE.Color('#7fbf3a'); liq.material.emissiveIntensity = 0.5; X.balde.add(liq); X.liq = liq;
  const asa = new THREE.Mesh(new THREE.TorusGeometry(0.26, 0.012, 6, 24, Math.PI), mat('#222')); asa.position.y = 0.42; X.balde.add(asa);

  // botellas: cloro (blanca, tapa azul) que se vacía, y otro producto (amarillo) junto al balde
  const botella = (cuerpo, tapa, conEtiqueta = true) => {
    const q = new THREE.Group();
    q.add(cil(0.08, 0.09, 0.34, cuerpo, 0, 0.17, 0)); q.add(cil(0.035, 0.05, 0.08, cuerpo, 0, 0.38, 0)); q.add(cil(0.04, 0.04, 0.05, tapa, 0, 0.44, 0));
    if (conEtiqueta) { const e = cil(0.092, 0.092, 0.13, '#ffffff', 0, 0.17, 0); e.material.color.set('#f7f7f7'); q.add(e); const fr = cil(0.093, 0.093, 0.03, tapa, 0, 0.2, 0); q.add(fr); }
    return q;
  };
  X.cloro = botella('#f4f4f4', '#1FA9E8'); g.add(X.cloro);
  X.otro = botella('#FFC53D', '#E5484D'); X.otro.position.set(-0.02, 0, 1.12); X.otro.rotation.z = 0; g.add(X.otro);
  X.chorro = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.012, 0.5, 8), mat('#e8ffd0', 0.2, { transparent: true, opacity: 0.8 })); g.add(X.chorro);

  // vapor tóxico: bolitas verdes translúcidas que suben del balde
  X.vapor = [];
  for (let i = 0; i < 14; i++) {
    const m = new THREE.Mesh(new THREE.SphereGeometry(1, 18, 14), mat('#a6e86e', 0.9, { transparent: true, opacity: 0, depthWrite: false, emissive: new THREE.Color('#5fae2a'), emissiveIntensity: 0.45 }));
    m.renderOrder = 5; g.add(m); X.vapor.push(m);
  }

  // armario de productos: envases originales con etiqueta (paso 3)
  const arm = new THREE.Group(); arm.position.set(2.75, 0, -3.35); g.add(arm);
  arm.add(caja(1.5, 1.9, 0.06, '#e9eef2', 0, 0.95, -0.25)); for (const s of [-1, 1]) arm.add(caja(0.06, 1.9, 0.55, '#e9eef2', s * 0.75, 0.95, 0));
  for (const y of [0.05, 0.65, 1.25, 1.87]) arm.add(caja(1.5, 0.05, 0.55, '#cfd6de', 0, y, 0));
  for (const s of [-1, 1]) { const pu = caja(0.74, 1.86, 0.04, '#1FA9E8', s * 1.1, 0.95, 0.5); pu.rotation.y = s * -1.2; arm.add(pu); }
  X.envases = [];
  const cols = [['#f4f4f4', '#1FA9E8'], ['#FFC53D', '#E5484D'], ['#25D366', '#0D1117'], ['#8e6bd8', '#ffffff'], ['#f4f4f4', '#E5484D'], ['#1FA9E8', '#ffffff']];
  cols.forEach(([c, t], i) => { const q = botella(c, t); q.position.set(-0.45 + (i % 3) * 0.45, i < 3 ? 0.68 : 1.28, 0.05); arm.add(q); X.envases.push(q); });
  X.sinEtiqueta = botella('#9a8f7a', '#555', false); X.sinEtiqueta.position.set(0.25, 0.08, 0.1); arm.add(X.sinEtiqueta);
  X.arm = arm;

  // etiquetas 3D (interfaz que ayuda a contar)
  X.lVentana = pastilla3d('ABRE PUERTAS Y VENTANAS', '#1FA9E8', '#fff', 2.4); X.lVentana.position.set(-3.6, 2.3, -2.4); g.add(X.lVentana);
  X.lSalida = pastilla3d('AIRE LIBRE', '#25D366', '#0D1117', 1.7); X.lSalida.position.set(-4.3, 2.5, 2.7); g.add(X.lSalida);
  X.tel = etiqueta(lienzo(512, 860, (c, w, h) => {
    c.fillStyle = '#0D1117'; redondo(c, 10, 10, w - 20, h - 20, 70); c.fill(); c.lineWidth = 14; c.strokeStyle = '#3a4456'; c.stroke();
    c.fillStyle = '#9aa6b8'; c.font = '600 46px Manrope, sans-serif'; c.textAlign = 'center'; c.fillText('Llamando…', w / 2, 230);
    c.fillStyle = '#fff'; c.font = '900 84px Outfit, sans-serif'; c.fillText('MUTUAL', w / 2, 340); c.fillText('o ISL', w / 2, 430);
    c.fillStyle = '#25D366'; c.beginPath(); c.arc(w / 2, 650, 80, 0, Math.PI * 2); c.fill();
    c.strokeStyle = '#fff'; c.lineWidth = 22; c.lineCap = 'round'; c.beginPath(); c.arc(w / 2, 650, 38, Math.PI * 0.75, Math.PI * 1.25 + Math.PI); c.stroke();
  }), 0.62, 1.04);
  X.tel.position.set(-4.35, 2.45, 3.3); g.add(X.tel);
  X.reloj = etiqueta(lienzo(256, 256, (c) => { c.fillStyle = '#fff'; c.beginPath(); c.arc(128, 128, 120, 0, 7); c.fill(); c.lineWidth = 16; c.strokeStyle = '#E5484D'; c.stroke(); c.fillStyle = '#0D1117'; for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; c.beginPath(); c.arc(128 + Math.sin(a) * 88, 128 - Math.cos(a) * 88, 7, 0, 7); c.fill(); } }), 0.55, 0.55);
  X.aguja = etiqueta(lienzo(256, 256, (c) => { c.strokeStyle = '#E5484D'; c.lineWidth = 14; c.lineCap = 'round'; c.beginPath(); c.moveTo(128, 128); c.lineTo(128, 40); c.stroke(); c.fillStyle = '#0D1117'; c.beginPath(); c.arc(128, 128, 14, 0, 7); c.fill(); }), 0.55, 0.55);
  X.reloj.position.set(-3.55, 2.0, 2.3); X.aguja.position.copy(X.reloj.position);
  X.aguja.renderOrder = 21; g.add(X.reloj); g.add(X.aguja);
  X.lAccidente = pastilla3d('ES UN ACCIDENTE DEL TRABAJO', '#1FA9E8', '#fff', 2.3); X.lAccidente.position.set(-4.1, 2.75, 2.9); g.add(X.lAccidente);
  X.lEnvase = pastilla3d('ENVASE ORIGINAL Y CON ETIQUETA', '#25D366', '#0D1117', 2.5); X.lEnvase.position.set(2.0, 2.5, -2.9); g.add(X.lEnvase);
  X.cruz = etiqueta(lienzo(256, 256, (c) => { c.strokeStyle = '#E5484D'; c.lineWidth = 34; c.lineCap = 'round'; c.beginPath(); c.moveTo(50, 50); c.lineTo(206, 206); c.moveTo(206, 50); c.lineTo(50, 206); c.stroke(); }), 0.5, 0.5);
  X.cruz.position.set(2.75 + 0.25, 0.35, -3.25); g.add(X.cruz);
  return X;
}

function escala(s, k) { const [w, h] = s.userData.base; s.scale.set(w * Math.max(k, 0.001), h * Math.max(k, 0.001), 1); s.visible = k > 0.001; }

function actualizar(X, t) {
  // botella de cloro: se vacía sobre el balde en el gancho y luego queda en el suelo
  const vaciando = t < E(0, 2.6);
  if (vaciando) { X.cloro.position.set(-0.62, 0.78, 0.78); X.cloro.rotation.set(0, 0, 2.3 + Math.sin(t * 5) * 0.08); }
  else { X.cloro.position.set(-0.85, 0, 1.2); X.cloro.rotation.set(0, 0, 0); }
  X.chorro.visible = t > E(0, 0.2) && vaciando;
  X.chorro.position.set(-0.5, 0.58, 0.82);
  // balde y botellas se retiran cuando la cocina ya está ventilada (fuera de cámara)
  const fuera = t > E(3, 2) && t < E(6);
  for (const o of [X.balde, X.cloro, X.otro]) o.visible = !fuera;
  X.chorro.visible = X.chorro.visible && !fuera;
  X.liq.material.emissiveIntensity = 0.3 + 0.3 * Math.sin(t * 6);

  // intensidad del vapor
  const sube = seg(t, E(0, 1.8), E(1, 0.6)), baja = seg(t, E(2, 0.8), E(2, 4.2));
  const I = sube * (1 - baja) * (t < E(3) ? 1 : 0);
  const deriva = seg(t, E(2, 0.3), E(2, 2.5));
  const vent = new THREE.Vector3(-4.6, 2.0, -3.6).sub(new THREE.Vector3(-0.45, 0.4, 0.85)).normalize();
  X.vapor.forEach((m, i) => {
    const u = ((t * 0.45) + i / X.vapor.length) % 1;
    const r = 0.16 + u * 0.42 * (0.6 + 0.4 * I);
    m.scale.setScalar(r);
    m.position.set(-0.45 + Math.sin(i * 1.7 + t * 1.3) * 0.28 * u, 0.42 + u * 2.1, 0.85 + Math.cos(i * 2.3 + t) * 0.25 * u);
    m.position.addScaledVector(vent, deriva * u * 3.2);
    m.material.opacity = I * Math.sin(Math.PI * u) * 0.6;
    m.visible = m.material.opacity > 0.01;
  });

  // ventana que se abre en el paso 1
  const ab = eo(seg(t, E(2, 0.6), E(2, 1.6))) * (t < E(5) ? 1 : 1);
  X.hojaI.rotation.y = -ab * 1.5; X.hojaD.rotation.y = ab * 1.5;

  // etiquetas 3D
  escala(X.lVentana, pop(t, E(2, 1.0), E(3)));
  escala(X.lSalida, pop(t, E(2, 2.6), E(3, 0.2)));
  escala(X.tel, pop(t, E(3, 0.4), E(3, 3.9)));
  const kr = pop(t, E(3, 3.6), E(4)); escala(X.reloj, kr); escala(X.aguja, kr);
  X.aguja.material.rotation = -t * 3;
  escala(X.lAccidente, pop(t, E(3, 4.0), E(4)));
  escala(X.lEnvase, pop(t, E(4, 2.6), E(5)));
  // armario: los envases con etiqueta aparecen uno a uno; el envase sin etiqueta se tacha y desaparece
  X.envases.forEach((q, i) => { const k = t < E(4) ? 1 : pop(t, E(4, 0.8 + i * 0.3), 1e9); q.scale.setScalar(Math.max(k, 0.001)); });
  const kx = pop(t, E(4, 3.0), E(4, 4.6)); escala(X.cruz, kx);
  const se = t < E(4, 4.2) ? 1 : 1 - eo(seg(t, E(4, 4.2), E(4, 4.6))); X.sinEtiqueta.scale.setScalar(Math.max(se, 0.001)); X.sinEtiqueta.visible = se > 0.01;
}

// ---------- enganche con el motor (sin modificarlo) ----------
let ESCENA = null, X = null;
const addOrig = THREE.Object3D.prototype.add;
THREE.Object3D.prototype.add = function (...o) { if (this.isScene && !ESCENA) ESCENA = this; return addOrig.apply(this, o); };
let ra = null;
Object.defineProperty(window, 'renderAt', {
  configurable: true,
  get() { return ra; },
  set(f) { ra = t => { if (ESCENA && !X) X = armar(ESCENA); if (X) actualizar(X, t); return f(t); }; },
});

export default {
  escenario: 'local',
  actores: {
    carla: { tipo: 'inseguro', pos: [-1.1, 0.55], rot: 0.75, pelo: '#3a2416' },          // trabajadora sin EPP
    diego: { tipo: 'seguro', pos: [5.8, 0.9], rot: -1.6 },                              // dueño: reflectante azul, casco blanco
    carla2: { tipo: 'inseguro', pos: [-30, -30], rot: 0, pelo: '#3a2416', guantes: '#25D366' },  // la misma trabajadora, ahora con guantes
  },
  objetos: {
    cinta: { tipo: 'valla', pos: [0.85, -1.2, 0.9], rot: 1.57 },   // cinta de peligro que sube del suelo en el paso 1
  },
  pasos: [
    // el local: fuera escalera y cajas, mostrador al costado
    { t: 0, o: 'escalera', hacer: 'mover', hacia: [-30, 0, -30], dur: 0.01 },
    { t: 0, o: 'caja1', hacer: 'mover', hacia: [-30, 0, -30], dur: 0.01 },
    { t: 0, o: 'caja2', hacer: 'mover', hacia: [-30, 0, -30], dur: 0.01 },
    { t: 0, o: 'caja3', hacer: 'mover', hacia: [-30, 0, -30], dur: 0.01 },
    { t: 0, o: 'mostrador', hacer: 'mover', hacia: [4.5, 0, -1.3], rot: -0.5, dur: 0.01 },
    // e0 gancho: Carla vacía el cloro en el balde y se asusta
    { t: 0, a: 'carla', hacer: 'agacharse', dur: E(0, 2.6) },
    { t: 'e0+2.6', a: 'carla', hacer: 'alerta', dur: 2.2, marca: 'peligro' },
    // e1 vapor: Carla tose y se tambalea; Diego entra alarmado
    { t: 'e1', a: 'carla', hacer: 'tambalear', dur: 4.9, marca: 'peligro' },
    { t: 'e1+0.4', a: 'diego', hacer: 'caminar', hacia: [0.9, 1.3], dur: 2.0 },
    { t: 'e1+2.5', a: 'diego', hacer: 'alerta', dur: 1.8, mirarA: 'carla' },
    // e2 paso 1: Diego señala la salida y salen al aire libre; se abre la ventana y sube la cinta
    { t: 'e2', a: 'diego', hacer: 'girar', rot: -1.2, dur: 0.3 },
    { t: 'e2+0.1', a: 'diego', hacer: 'apuntar', dur: 1.3 },
    { t: 'e2+0.5', a: 'carla', hacer: 'caminar', hacia: [-3.9, 2.45], dur: 2.6, mirar: 0.2 },
    { t: 'e2+1.2', a: 'diego', hacer: 'caminar', hacia: [-4.9, 3.1], dur: 2.6, mirar: 1.2 },
    { t: 'e2+1.0', o: 'cinta', hacer: 'mover', hacia: [0.85, 0, 0.9], dur: 0.8 },
    { t: 'e2+3.6', a: 'carla', hacer: 'feliz', dur: 1.3 },
    // e3 paso 2: afuera, Carla sentada; Diego llama a la mutual o al ISL
    { t: 'e3', a: 'carla', hacer: 'girar', rot: 0.7, dur: 0.5 },
    { t: 'e3+0.2', a: 'diego', hacer: 'apuntar', dur: 6.6, mirarA: 'carla' },
    // e4 paso 3: cocina ordenada, envases originales con etiqueta; Carla con guantes observa
    { t: 'e4', a: 'carla', hacer: 'caminar', hacia: [-30, -30], dur: 0.01 },
    { t: 'e4', o: 'cinta', hacer: 'mover', hacia: [0.85, -1.2, 0.9], dur: 0.01 },
    { t: 'e4', a: 'diego', hacer: 'caminar', hacia: [3.0, 0.9], dur: 0.01 },
    { t: 'e4+0.05', a: 'diego', hacer: 'caminar', hacia: [1.65, -2.3], dur: 1.2, mirar: 2.6 },
    { t: 'e4', a: 'carla2', hacer: 'caminar', hacia: [-1.0, -0.6], dur: 0.01 },
    { t: 'e4+0.05', a: 'carla2', hacer: 'caminar', hacia: [0.8, -1.5], dur: 1.6, mirar: 1.2 },
    { t: 'e4+1.4', a: 'diego', hacer: 'apuntar', dur: 2.6, mirarA: 'carla2' },
    { t: 'e4+4.2', a: 'diego', hacer: 'girar', rot: 0.15, dur: 0.4 },
    { t: 'e4+4.6', a: 'diego', hacer: 'feliz', dur: 1.4, marca: 'ok' },
    { t: 'e4+4.4', a: 'carla2', hacer: 'girar', rot: 0.3, dur: 0.4 },
    { t: 'e4+4.8', a: 'carla2', hacer: 'saludo', dur: 1.2, marca: 'ok' },
    // e5 ley y e6 cierre: todo en orden
    { t: 'e5+0.3', a: 'diego', hacer: 'saludo', dur: 30 },
    { t: 'e5+0.3', a: 'carla2', hacer: 'feliz', dur: 30 },
  ],
  camara: [
    { t: 0, plano: 'medio', mirar: [-0.6, 0, -0.4], ang: 0.35 },
    { t: 'e0+1.5', plano: 'cerca', mirar: [-0.7, 0, -0.2], ang: 0.25, dur: 2.0 },
    { t: 'e1', plano: 'medio', mirar: [-0.3, 0, 0.3], ang: -0.4 },
    { t: 'e1+2.4', plano: 'general', mirar: [0.0, 0, 0.4], ang: -0.15 },
    { t: 'e2', plano: 'general', mirar: [-2.2, 0, 0.6], ang: 0.2 },
    { t: 'e2+2.8', plano: 'medio', mirar: [-4.3, 0, 2.5], ang: 0.5 },
    { t: 'e3', plano: 'medio', mirar: [-4.1, 0, 2.4], ang: 0.6 },
    { t: 'e4', plano: 'medio', mirar: [1.5, 0, -2.2], ang: -0.05 },
    { t: 'e5', plano: 'alto', mirar: [1.6, 0, 0.6], ang: -0.3, orbita: 0.04 },
    { t: 'e6', plano: 'general', mirar: [0.5, 0, 0], orbita: 0.05 },
  ],
};
