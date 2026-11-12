// Motor 3D de los reels de Base Segura (Three.js). Render determinista: window.renderAt(segundos).
// Cada reel escribe reel/escena3d.js con `export default { escenario, actores, objetos, pasos, camara }`
// (formato en herramientas/3d/LEEME.md). Lo empaqueta herramientas/armar-reel-3d.py.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

const W = 1080, H = 1920;
const C = { negro: '#0D1117', azul: '#1FA9E8', naranjo: '#F2A33A', rojo: '#E5484D', verde: '#25D366', amarillo: '#FFC53D' };

// ---------- utilidades ----------
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (t, a, b) => (b <= a ? (t >= a ? 1 : 0) : cl((t - a) / (b - a)));
const eo = x => 1 - Math.pow(1 - x, 3);
const eio = x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const lerp = (a, b, x) => a + (b - a) * x;
const mat = (c, r = 0.45, m = 0) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
function caja(w, h, d, c, rad = 0.06) {
  const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 3, Math.min(rad, w / 2.1, h / 2.1, d / 2.1)), mat(c));
  m.castShadow = m.receiveShadow = true; return m;
}
const esfera = (r, c, ro = 0.35) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 24), mat(c, ro)); m.castShadow = true; return m; };
const capsula = (r, l, c) => { const m = new THREE.Mesh(new THREE.CapsuleGeometry(r, l, 8, 16), mat(c, 0.4)); m.castShadow = true; return m; };
const cilindro = (r, h, c, seg = 20) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, seg), mat(c, 0.5)); m.castShadow = m.receiveShadow = true; return m; };
const tubo = (a, b, r, c) => {  // cilindro entre dos puntos
  const va = new THREE.Vector3(...a), vb = new THREE.Vector3(...b), l = va.distanceTo(vb);
  const m = cilindro(r, l, c, 10); m.position.copy(va).add(vb).multiplyScalar(0.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), vb.clone().sub(va).normalize()); return m;
};
function letrero(txt, w, h, fondo = C.azul, color = '#fff') {
  const cv = document.createElement('canvas'); cv.width = 1024; cv.height = Math.round(1024 * h / w);
  const g = cv.getContext('2d'); g.fillStyle = fondo; g.fillRect(0, 0, cv.width, cv.height);
  g.fillStyle = color; g.font = `900 ${Math.round(cv.height * 0.55)}px Outfit, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillText(txt, cv.width / 2, cv.height / 2 + 4);
  const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.08), [mat(fondo), mat(fondo), mat(fondo), mat(fondo), new THREE.MeshStandardMaterial({ map: tx, roughness: 0.5 }), mat(fondo)]);
  m.castShadow = true; return m;
}

// ---------- props reutilizables ----------
const P = {
  saco: () => caja(0.62, 0.26, 0.42, '#e8dcc0', 0.12),
  caja: (c = '#c8955a') => { const g = new THREE.Group(); g.add(caja(0.6, 0.5, 0.5, c, 0.03)); const cinta = caja(0.62, 0.06, 0.12, '#e9d8b4', 0.01); cinta.position.y = 0.22; g.add(cinta); return g; },
  pallet: () => caja(1.4, 0.16, 1.1, '#a8763e', 0.03),
  cono: () => { const g = new THREE.Group(); const c = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.55, 24), mat(C.naranjo, 0.5)); c.position.y = 0.3; c.castShadow = true; g.add(c); const b = caja(0.4, 0.05, 0.4, '#222', 0.01); b.position.y = 0.025; g.add(b); const f = cilindro(0.13, 0.08, '#fff'); f.position.y = 0.33; g.add(f); return g; },
  carro: () => {
    const g = new THREE.Group(); const p = caja(1.2, 0.12, 0.85, C.azul, 0.05); p.position.y = 0.3; g.add(p);
    const a = caja(0.08, 1.0, 0.08, C.negro, 0.03); a.position.set(0.62, 0.8, 0); g.add(a);
    const a2 = caja(0.08, 0.08, 0.75, C.negro, 0.03); a2.position.set(0.62, 1.28, 0); g.add(a2);
    for (const [x, z] of [[-0.45, -0.33], [0.45, -0.33], [-0.45, 0.33], [0.45, 0.33]]) { const r = cilindro(0.12, 0.09, '#222'); r.rotation.x = Math.PI / 2; r.position.set(x, 0.12, z); g.add(r); }
    return g;
  },
  escalera: () => {  // escalera de tijera 2 m
    const g = new THREE.Group();
    for (const s of [-1, 1]) { g.add(tubo([-0.3, 0, s * 0.45], [-0.05, 2, s * 0.05], 0.035, '#c9ccd2')); g.add(tubo([0.3, 0, s * 0.45], [0.05, 2, s * 0.05], 0.035, '#c9ccd2')); }
    for (let i = 1; i < 6; i++) { const y = i * 0.33, k = 1 - y / 2; const p = caja(0.6 * k + 0.1, 0.04, 0.12, '#9aa0aa', 0.01); p.position.set(0, y, 0.45 * k); g.add(p); }
    return g;
  },
  grua: () => {  // grúa horquilla
    const g = new THREE.Group();
    const cuerpo = caja(1.3, 0.7, 1.0, C.amarillo, 0.12); cuerpo.position.set(0, 0.6, 0); g.add(cuerpo);
    const contrapeso = caja(0.4, 0.6, 1.0, '#333', 0.1); contrapeso.position.set(-0.75, 0.6, 0); g.add(contrapeso);
    const techo = caja(1.0, 0.06, 0.95, '#333', 0.02); techo.position.set(-0.05, 1.9, 0); g.add(techo);
    for (const [x, z] of [[0.4, 0.42], [0.4, -0.42], [-0.5, 0.42], [-0.5, -0.42]]) g.add(tubo([x, 0.9, z], [x, 1.9, z], 0.035, '#333'));
    const mastil = caja(0.12, 2.2, 0.8, '#444', 0.02); mastil.position.set(0.75, 1.15, 0); g.add(mastil);
    const horq = new THREE.Group(); horq.name = 'horquilla'; horq.position.set(0.85, 0.12, 0); g.add(horq);
    for (const z of [-0.25, 0.25]) { const h = caja(0.9, 0.05, 0.1, '#666', 0.01); h.position.set(0.45, 0, z); horq.add(h); }
    for (const [x, z] of [[0.45, 0.5], [0.45, -0.5], [-0.45, 0.5], [-0.45, -0.5]]) { const r = cilindro(0.22, 0.18, '#1a1a1a'); r.rotation.x = Math.PI / 2; r.position.set(x, 0.22, z); g.add(r); }
    const baliza = esfera(0.08, '#ff7a00'); baliza.name = 'baliza'; baliza.material.emissive = new THREE.Color('#ff7a00'); baliza.position.set(-0.05, 2.0, 0); g.add(baliza);
    return g;
  },
  excavadora: () => {
    const g = new THREE.Group();
    for (const z of [-0.6, 0.6]) { const o = caja(2.2, 0.45, 0.4, '#2a2a2a', 0.18); o.position.set(0, 0.25, z); g.add(o); }
    const giro = new THREE.Group(); giro.name = 'giro'; giro.position.y = 0.5; g.add(giro);
    const cuerpo = caja(1.8, 0.8, 1.5, C.amarillo, 0.12); cuerpo.position.set(-0.2, 0.45, 0); giro.add(cuerpo);
    const cabina = caja(0.8, 0.9, 0.7, C.amarillo, 0.1); cabina.position.set(0.25, 1.25, 0.35); giro.add(cabina);
    const vidrio = caja(0.05, 0.6, 0.55, '#8fd3ff', 0.02); vidrio.position.set(0.66, 1.3, 0.35); vidrio.material.metalness = 0.2; giro.add(vidrio);
    const brazo = new THREE.Group(); brazo.name = 'brazo'; brazo.position.set(0.5, 0.9, -0.3); giro.add(brazo);
    const b1 = caja(1.8, 0.28, 0.25, C.amarillo, 0.08); b1.position.set(0.8, 0.45, 0); b1.rotation.z = 0.5; brazo.add(b1);
    const ante = new THREE.Group(); ante.position.set(1.55, 0.85, 0); brazo.add(ante);
    const b2 = caja(1.4, 0.22, 0.22, C.amarillo, 0.07); b2.position.set(0.55, -0.35, 0); b2.rotation.z = -0.9; ante.add(b2);
    const balde = caja(0.5, 0.45, 0.6, '#555', 0.06); balde.position.set(1.0, -0.95, 0); ante.add(balde);
    return g;
  },
  andamio: (pisos = 2, conBaranda = true) => {
    const g = new THREE.Group(), w = 2.4, d = 1.0, hp = 1.6;
    for (const x of [-w / 2, w / 2]) for (const z of [-d / 2, d / 2]) g.add(tubo([x, 0, z], [x, pisos * hp + 1, z], 0.04, '#c9ccd2'));
    for (let p = 1; p <= pisos; p++) {
      const y = p * hp; const pl = caja(w + 0.1, 0.06, d, '#a8763e', 0.01); pl.position.y = y; g.add(pl);
      if (conBaranda || p < pisos) { g.add(tubo([-w / 2, y + 1, d / 2], [w / 2, y + 1, d / 2], 0.03, C.amarillo)); g.add(tubo([-w / 2, y + 0.5, d / 2], [w / 2, y + 0.5, d / 2], 0.03, C.amarillo)); }
      g.add(tubo([-w / 2, y - hp, d / 2], [w / 2, y, d / 2], 0.025, '#9aa0aa'));
    }
    return g;
  },
  estante: (cajas = true, alto = 3) => {
    const g = new THREE.Group(), w = 2.6, d = 0.9;
    for (const x of [-w / 2, w / 2]) for (const z of [-d / 2, d / 2]) { const p = caja(0.08, alto, 0.08, '#2f6fd1', 0.02); p.position.set(x, alto / 2, z); g.add(p); }
    const niveles = Math.round(alto / 1); const huecos = [];
    for (let i = 0; i < niveles; i++) {
      const y = 0.15 + i * (alto - 0.2) / (niveles - 0.4); const v = caja(w, 0.07, d, C.naranjo, 0.02); v.position.y = y; g.add(v);
      if (cajas) for (let k = 0; k < 3; k++) { const c = P.caja(['#c8955a', '#b9824a', '#d4a46c'][k]); c.position.set(-0.8 + k * 0.8, y + 0.28, 0); g.add(c); huecos.push(c); }
    }
    g.userData.cajas = huecos; return g;
  },
  mostrador: () => { const g = new THREE.Group(); const m = caja(2.2, 1.0, 0.7, '#e9e2d4', 0.06); m.position.y = 0.5; g.add(m); const t = caja(2.3, 0.08, 0.8, C.azul, 0.03); t.position.y = 1.02; g.add(t); const caj = caja(0.4, 0.3, 0.3, '#333', 0.04); caj.position.set(0.6, 1.2, 0); g.add(caj); return g; },
  gondola: () => {  // estantería de local con productos de colores
    const g = new THREE.Group(); const fondo = caja(2.4, 1.9, 0.12, '#dfe6ee', 0.03); fondo.position.y = 0.95; g.add(fondo);
    const cols = ['#E5484D', '#1FA9E8', '#FFC53D', '#25D366', '#F2A33A', '#8e6bd8'];
    for (let i = 0; i < 4; i++) { const v = caja(2.4, 0.06, 0.5, '#9aa0aa', 0.02); v.position.set(0, 0.2 + i * 0.45, 0.25); g.add(v);
      for (let k = 0; k < 6; k++) { const p = caja(0.28, 0.3, 0.3, cols[(i + k) % 6], 0.06); p.position.set(-1.0 + k * 0.4, 0.38 + i * 0.45, 0.3); g.add(p); } }
    return g;
  },
  ladrillos: () => { const g = new THREE.Group(); for (let f = 0; f < 4; f++) for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++) { const b = caja(0.4, 0.18, 0.2, '#b5532f', 0.02); b.position.set(-0.42 + i * 0.42 + (f % 2) * 0.1, 0.1 + f * 0.19, -0.11 + j * 0.22); g.add(b); } return g; },
  barril: () => { const b = cilindro(0.3, 0.9, C.azul, 24); b.position.y = 0.45; const g = new THREE.Group(); g.add(b); return g; },
  extintor: () => { const g = new THREE.Group(); const b = capsula(0.12, 0.4, C.rojo); b.position.y = 0.38; g.add(b); const t = cilindro(0.04, 0.12, '#222'); t.position.y = 0.72; g.add(t); return g; },
  valla: () => { const g = new THREE.Group(); for (let i = 0; i < 4; i++) { const f = caja(0.5, 0.18, 0.06, i % 2 ? '#fff' : C.rojo, 0.02); f.position.set(-0.75 + i * 0.5, 0.8, 0); g.add(f); } for (const x of [-1, 1]) { const p = caja(0.08, 0.9, 0.08, '#555', 0.02); p.position.set(x, 0.45, 0); g.add(p); } return g; },
};

// ---------- personaje tipo juguete ----------
// tipo: 'seguro' (chaleco reflectante azul, casco blanco = marca Base Segura) | 'inseguro' (polera roja, pantalón negro, sin casco) | 'jefe'
const TIPOS = {
  seguro: { torso: C.azul, pantalon: '#24324a', casco: '#ffffff', reflectante: true, guantes: '#FFC53D' },
  inseguro: { torso: '#d62828', pantalon: '#16181d', casco: null, reflectante: false, pelo: '#2b1d14' },
  jefe: { torso: '#f4f4f4', pantalon: '#3a3f4a', casco: '#ffffff', reflectante: false, pelo: '#4a3b2b', corbata: '#1FA9E8' },
  cliente: { torso: '#8e6bd8', pantalon: '#2c3e50', casco: null, reflectante: false, pelo: '#6b4423' },
};
function muneco(op = {}) {
  const T = { ...TIPOS[op.tipo || 'seguro'], ...op }; const piel = op.piel || '#f1c6a0';
  const g = new THREE.Group();
  const cadera = new THREE.Group(); cadera.position.y = 0.78; g.add(cadera);
  const torso = new THREE.Group(); cadera.add(torso);
  const cuerpo = caja(0.62, 0.72, 0.42, T.torso, 0.16); cuerpo.position.y = 0.36; torso.add(cuerpo);
  if (T.reflectante) for (const y of [0.22, 0.42]) { const b = caja(0.64, 0.05, 0.44, '#e8f6ff', 0.02); b.position.y = y; b.material.emissive = new THREE.Color('#bfe6ff'); b.material.emissiveIntensity = 0.35; torso.add(b); }
  if (T.corbata) { const cb = caja(0.1, 0.4, 0.05, T.corbata, 0.02); cb.position.set(0, 0.45, 0.22); torso.add(cb); }
  const cuello = new THREE.Group(); cuello.position.y = 0.78; torso.add(cuello);
  const cabeza = esfera(0.3, piel); cabeza.scale.set(1, 0.95, 0.95); cabeza.position.y = 0.22; cuello.add(cabeza);
  const ojos = [];
  for (const x of [-0.1, 0.1]) {
    const o = new THREE.Mesh(new THREE.SphereGeometry(0.045, 16, 12), mat('#141414', 0.2)); o.position.set(x, 0.26, 0.27); cuello.add(o); ojos.push(o);
    const br = new THREE.Mesh(new THREE.SphereGeometry(0.014, 8, 6), mat('#fff', 0.1)); br.position.set(x + 0.015, 0.275, 0.31); cuello.add(br); ojos.push(br);
  }
  const cejas = []; for (const x of [-0.1, 0.1]) { const c = caja(0.1, 0.02, 0.02, '#2b1d14', 0.008); c.position.set(x, 0.34, 0.27); cuello.add(c); cejas.push(c); }
  const boca = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.016, 8, 20, Math.PI), mat('#7a2e2e', 0.4)); boca.rotation.z = Math.PI; boca.position.set(0, 0.16, 0.27); cuello.add(boca);
  const bocaO = esfera(0.05, '#5a1e1e'); bocaO.scale.set(1, 1.2, 0.4); bocaO.position.set(0, 0.13, 0.27); bocaO.visible = false; cuello.add(bocaO);
  for (const x of [-0.18, 0.18]) { const m = new THREE.Mesh(new THREE.SphereGeometry(0.04, 12, 8), mat('#ff9b8a', 0.6)); m.position.set(x, 0.18, 0.24); m.scale.z = 0.4; cuello.add(m); }
  if (T.casco) {
    const c1 = new THREE.Mesh(new THREE.SphereGeometry(0.33, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), mat(T.casco, 0.3)); c1.position.y = 0.3; c1.castShadow = true; cuello.add(c1);
    const ala = cilindro(0.4, 0.04, T.casco, 32); ala.position.set(0, 0.3, 0.05); cuello.add(ala);
  } else {
    const pelo = new THREE.Mesh(new THREE.SphereGeometry(0.31, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2.3), mat(T.pelo, 0.8)); pelo.position.set(0, 0.25, -0.02); pelo.castShadow = true; cuello.add(pelo);
  }
  const brazo = lado => {
    const h = new THREE.Group(); h.position.set(lado * 0.4, 0.62, 0); torso.add(h);
    const b = capsula(0.09, 0.38, T.torso); b.position.y = -0.24; h.add(b);
    const mano = esfera(0.1, T.guantes || piel); mano.position.y = -0.5; h.add(mano); return h;
  };
  const pierna = lado => {
    const p = new THREE.Group(); p.position.set(lado * 0.16, 0, 0); cadera.add(p);
    const l = capsula(0.12, 0.42, T.pantalon); l.position.y = -0.33; p.add(l);
    const bota = caja(0.24, 0.16, 0.34, '#3b2a1e', 0.06); bota.position.set(0, -0.7, 0.05); p.add(bota); return p;
  };
  g.userData = { cadera, torso, cuello, cuerpo, ojos, cejas, boca, bocaO, brazoI: brazo(-1), brazoD: brazo(1), piernaI: pierna(-1), piernaD: pierna(1) };
  return g;
}

// ---------- escenarios ----------
function base(scene, suelo, loza) {
  const p = caja(16, 0.4, 12, suelo, 0.15); p.position.y = -0.2; scene.add(p);
  const l = caja(11, 0.05, 8, loza, 0.03); l.position.y = 0.025; l.receiveShadow = true; scene.add(l);
}
function linea(scene, x1, z1, x2, z2, color, ancho = 0.12) {
  const l = Math.hypot(x2 - x1, z2 - z1); const m = caja(l, 0.02, ancho, color, 0.005);
  m.position.set((x1 + x2) / 2, 0.06, (z1 + z2) / 2); m.rotation.y = -Math.atan2(z2 - z1, x2 - x1); scene.add(m);
}
const ESC = {
  bodega(s, O) {  // bodega con estanterías y cajas que se pueden caer
    base(s, '#2b3446', '#3a465c');
    const muro = caja(11, 3.6, 0.3, '#d9d4c7', 0.05); muro.position.set(0, 1.8, -3.9); s.add(muro);
    const porton = caja(3, 2.6, 0.1, '#5b6578', 0.04); porton.position.set(3.4, 1.3, -3.72); s.add(porton);
    const r1 = P.estante(true, 3.2); r1.position.set(-2.6, 0, -3.1); s.add(r1); O.estante = r1;
    const r2 = P.estante(true, 3.2); r2.position.set(0.3, 0, -3.1); s.add(r2); O.estante2 = r2;
    r1.userData.cajas.forEach((c, i) => O['caja_alta' + (i ? i : '')] = c);
    const pal = P.pallet(); pal.position.set(2.8, 0.08, -0.4); s.add(pal);
    for (let i = 0; i < 4; i++) { const c = P.caja(); c.position.set(2.5 + (i % 2) * 0.62, 0.41 + Math.floor(i / 2) * 0.5, -0.4); s.add(c); O['caja' + (i + 1)] = c; }
    const ext = P.extintor(); ext.position.set(-4.9, 0, -3.5); s.add(ext);
    const l = letrero('BODEGA', 2.2, 0.5, C.azul); l.position.set(-1.2, 3.3, -3.7); s.add(l);
    linea(s, -5, 1.6, 5, 1.6, C.amarillo); linea(s, -5, 2.8, 5, 2.8, C.amarillo);
  },
  transito(s, O) {  // bodega con tránsito de grúas horquilla y pasillo peatonal
    ESC.bodega(s, O);
    linea(s, -5, 0.6, 5, 0.6, C.verde, 0.1); linea(s, -5, 1.5, 5, 1.5, C.verde, 0.1);
    for (let i = -4; i <= 4; i++) linea(s, i * 1.1 - 0.25, 1.05, i * 1.1 + 0.25, 1.05, C.verde, 0.6);
    const gr = P.grua(); gr.position.set(-3.2, 0, 2.4); s.add(gr); O.grua = gr;
    const ps = P.pallet(); ps.position.set(0.45, 0.2, 0); gr.getObjectByName('horquilla').add(ps);
    const cj = P.caja(); cj.position.set(0.45, 0.53, 0); gr.getObjectByName('horquilla').add(cj);
  },
  local(s, O) {  // local comercial / ferretería
    base(s, '#2b3446', '#e9eef2');
    const muro = caja(11, 3.4, 0.3, '#f4efe6', 0.05); muro.position.set(0, 1.7, -3.9); s.add(muro);
    const g1 = P.gondola(); g1.position.set(-2.6, 0, -3.5); s.add(g1); O.gondola = g1;
    const g2 = P.gondola(); g2.position.set(0.2, 0, -3.5); s.add(g2); O.gondola2 = g2;
    const m = P.mostrador(); m.position.set(3.2, 0, -1.2); m.rotation.y = -0.3; s.add(m); O.mostrador = m;
    const l = letrero('FERRETERÍA', 3.6, 0.7, C.naranjo); l.position.set(-1.2, 3.0, -3.7); s.add(l);
    const esc = P.escalera(); esc.position.set(-2.9, 0, -2.0); s.add(esc); O.escalera = esc;
    const ext = P.extintor(); ext.position.set(4.6, 0, -3.5); s.add(ext); O.extintor = ext;
    for (let i = 0; i < 3; i++) { const c = P.caja('#c8955a'); c.position.set(1.8 + i * 0.1, 0.25 + i * 0.5, 0.6); s.add(c); O['caja' + (i + 1)] = c; }
  },
  obra(s, O) {  // obra en terreno con maquinaria y andamios
    base(s, '#4a3a2a', '#8a6a4a');
    const casa = new THREE.Group(); s.add(casa); casa.position.set(-1, 0, -3.2);
    for (const x of [-2, 0, 2]) { const col = caja(0.3, 4, 0.3, '#9a9a9a', 0.03); col.position.set(x, 2, 0); casa.add(col); }
    for (const y of [1.6, 3.2]) { const lz = caja(4.6, 0.25, 1.6, '#a7a7a7', 0.03); lz.position.set(0, y, 0.4); casa.add(lz); }
    const and = P.andamio(2, true); and.position.set(-1, 0, -1.3); s.add(and); O.andamio = and;
    const exc = P.excavadora(); exc.position.set(3.7, 0, -0.4); exc.rotation.y = -2.4; s.add(exc); O.excavadora = exc;
    const lad = P.ladrillos(); lad.position.set(1.6, 0, -1.2); s.add(lad);
    for (const [x, z] of [[-4.5, 2.5], [-3.5, 2.8], [4.6, -1.8]]) { const c = P.cono(); c.position.set(x, 0, z); s.add(c); }
    const v = P.valla(); v.position.set(1.0, 0, 3.2); s.add(v); O.valla = v;
    const caseta = caja(2, 1.8, 1.4, '#e9e2d4', 0.06); caseta.position.set(4.2, 0.9, -3); s.add(caseta);
    const techo = caja(2.3, 0.2, 1.7, C.azul, 0.06); techo.position.set(4.2, 1.9, -3); s.add(techo);
    const l = letrero('OBRA', 1.4, 0.45, C.naranjo); l.position.set(4.2, 1.3, -2.25); s.add(l);
  },
};

// ---------- runtime ----------
export function iniciar(PLAN, TIEMPOS) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  document.getElementById('gl').appendChild(renderer.domElement);
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#141b29'); scene.fog = new THREE.Fog('#141b29', 20, 38);
  const cam = new THREE.PerspectiveCamera(38, W / H, 0.1, 100);
  scene.add(new THREE.HemisphereLight('#cfe8ff', '#2a2f3a', 1.1));
  const sol = new THREE.DirectionalLight('#fff4e0', 2.6); sol.position.set(5, 11, 7); sol.castShadow = true;
  sol.shadow.mapSize.set(2048, 2048); Object.assign(sol.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9, near: 1, far: 34 }); scene.add(sol);
  const rim = new THREE.DirectionalLight(C.azul, 1.4); rim.position.set(-6, 4, -5); scene.add(rim);

  const O = {};  // objetos animables por id
  (ESC[PLAN.escenario] || ESC.bodega)(scene, O);
  for (const [id, o] of Object.entries(PLAN.objetos || {})) {  // props extra: { id: {tipo:'saco', pos:[x,y,z], rot} }
    const m = P[o.tipo] ? P[o.tipo](o.color) : P.caja(); m.position.set(...(o.pos || [0, 0, 0])); m.rotation.y = o.rot || 0; scene.add(m); O[id] = m;
  }
  const A = {};
  for (const [id, a] of Object.entries(PLAN.actores || {})) { const m = muneco(a); m.position.set(a.pos?.[0] || 0, 0, a.pos?.[1] || 0); m.rotation.y = a.rot || 0; scene.add(m); A[id] = m; }
  // anillos de señal (peligro/ok) bajo actores u objetos
  const anillo = c => { const m = new THREE.Mesh(new THREE.RingGeometry(0.55, 0.75, 48), new THREE.MeshBasicMaterial({ color: c, transparent: true, side: THREE.DoubleSide })); m.rotation.x = -Math.PI / 2; m.position.y = 0.08; m.visible = false; scene.add(m); return m; };

  // tiempos: número | 'e3' | 'e3+1.2' | 'e3-0.5' | 'fin'
  const esc = TIEMPOS?.escenas || [];
  const tt = v => {
    if (typeof v === 'number') return v;
    if (v === 'fin') return TIEMPOS.total;
    const m = /^e(\d+)([+-][\d.]+)?$/.exec(String(v)); if (!m) return 0;
    const e = esc[+m[1]] || { inicio: 0 }; return e.inicio + (m[2] ? parseFloat(m[2]) : 0);
  };
  const pasos = (PLAN.pasos || []).map(p => ({ ...p, t0: tt(p.t), dur: p.dur ?? 1 })).sort((a, b) => a.t0 - b.t0);
  pasos.forEach(p => { p.t1 = p.t0 + p.dur; if (p.marca) p.ring = anillo(p.marca === 'ok' ? C.verde : C.rojo); });

  // estado base de cada actor/objeto
  const ini = {};
  for (const [id, m] of Object.entries({ ...A, ...O })) { ini[id] = { pos: m.position.clone(), rot: m.rotation.clone(), parent: m.parent }; }
  const wp = new THREE.Vector3(), objetivo = new THREE.Vector3();

  function evaluarActor(id, m, t) {
    let pos = ini[id].pos.clone(), rotY = ini[id].rot.y; const w = { caminar: 0, agacharse: 0, carga: 0, tambaleo: 0, feliz: 0, empujar: 0, apuntar: 0, alerta: 0, caido: 0, subir: 0, saludo: 0 };
    let fase = 0;
    for (const p of pasos) {
      if (p.a !== id || p.t0 > t) continue;
      const k = seg(t, p.t0, p.t1), dentro = t < p.t1;
      const rampa = Math.min(seg(t, p.t0, p.t0 + 0.3), 1 - seg(t, p.t1 - 0.3, p.t1));
      switch (p.hacer) {
        case 'caminar': case 'empujar': case 'correr': {
          const hacia = new THREE.Vector3(p.hacia[0], pos.y, p.hacia[1]);
          if (dentro && k > 0) { const dir = hacia.clone().sub(pos); if (dir.lengthSq() > 1e-4) rotY = Math.atan2(dir.x, dir.z); w.caminar = 1; fase = t * (p.hacer === 'correr' ? 14 : 9); }
          pos.lerp(hacia, eio(k));
          if (p.hacer === 'empujar') w.empujar = dentro ? 1 : 0;
          if (!dentro && p.mirar !== undefined) rotY = p.mirar;
          break;
        }
        case 'girar': rotY = lerp(rotY, p.rot, eio(k)); break;
        case 'subir': pos.y = lerp(pos.y, p.altura, eio(k)); w.subir = dentro ? 1 : 0; break;
        case 'caer': case 'resbalar': w.caido = eo(k); if (p.hasta !== undefined) pos.y = lerp(pos.y, p.hasta, eo(k) * eo(k)); break;
        case 'levantarse': w.caido = 1 - eio(k); break;
        case 'cargar': w.carga = Math.max(w.carga, eo(k)); break;
        case 'dejar': w.carga = 1 - eio(k); w.agacharse = Math.max(w.agacharse, Math.sin(Math.PI * k)); break;
        default: if (dentro && w[p.hacer] !== undefined) w[p.hacer] = Math.max(w[p.hacer], rampa);  // agacharse, tambaleo, feliz, apuntar, alerta, saludo
      }
      if (p.hacer === 'tambalear' && dentro) w.tambaleo = Math.max(w.tambaleo, rampa);
      if (p.mirarA && dentro) { const o = A[p.mirarA] || O[p.mirarA]; if (o) { o.getWorldPosition(wp); rotY = lerp(rotY, Math.atan2(wp.x - pos.x, wp.z - pos.z), rampa); } }
    }
    m.position.copy(pos); m.rotation.y = rotY;
    if (w.tambaleo) m.position.x += Math.sin(t * 7) * 0.06 * w.tambaleo;
    // pose
    const u = m.userData, paso = Math.sin(fase) * w.caminar;
    u.piernaI.rotation.x = paso * 0.7 - w.agacharse * 0.5 + w.subir * Math.sin(t * 8) * 0.5;
    u.piernaD.rotation.x = -paso * 0.7 - w.agacharse * 0.5 - w.subir * Math.sin(t * 8) * 0.5;
    u.cadera.position.y = 0.78 + Math.abs(Math.cos(fase)) * 0.05 * w.caminar - w.agacharse * 0.22 + Math.sin(t * 2.2) * 0.008;
    u.torso.rotation.x = w.agacharse * 0.75 + w.empujar * 0.35 + w.carga * 0.18 - w.alerta * 0.15;
    u.torso.rotation.z = Math.sin(t * 7) * 0.12 * w.tambaleo;
    const bal = -paso * 0.6 * (1 - w.carga) * (1 - w.empujar);
    u.brazoI.rotation.set(bal - w.agacharse * 1.1 - w.empujar * 1.2 - w.alerta * 2.6 - w.subir * 2.4, 0, -w.carga * 0.5 - w.feliz * 2.7 - w.alerta * 0.3);
    u.brazoD.rotation.set(-bal - w.agacharse * 1.1 - w.empujar * 1.2 - w.carga * 0.2 - w.apuntar * 1.5 - w.alerta * 2.6 - w.subir * 2.4, 0,
      w.carga * 2.6 + w.feliz * 2.7 + w.alerta * 0.3 + w.saludo * (2.6 + Math.sin(t * 10) * 0.35));
    // caída: queda tendido de espaldas
    m.rotation.x = -w.caido * Math.PI / 2; m.position.y += w.caido * 0.25;
    // cara
    const parp = (t + id.length * 0.7) % 2.9 < 0.12 ? 0.15 : 1; u.ojos.forEach((o, i) => { if (i % 2 === 0) o.scale.y = parp; });
    const mal = w.tambaleo > 0.3 || w.alerta > 0.3 || w.caido > 0.3;
    u.boca.visible = !(w.alerta > 0.3 || w.caido > 0.3); u.bocaO.visible = !u.boca.visible;
    u.boca.rotation.z = mal ? 0 : Math.PI; u.boca.position.y = mal ? 0.12 : 0.16;
    u.cejas.forEach((c, i) => { c.rotation.z = (mal ? 0.35 : 0) * (i ? -1 : 1); c.position.y = 0.34 + (w.feliz > 0.3 ? 0.03 : 0); });
    u.cuerpo.material.emissive.set(mal ? '#ff2a2a' : '#000'); u.cuerpo.material.emissiveIntensity = mal ? 0.22 + 0.18 * Math.sin(t * 14) : 0;
    return w;
  }

  function evaluarObjeto(id, o, t) {
    const b = ini[id]; const bp = b.pos.clone(); o.position.copy(bp); o.rotation.copy(b.rot); let enMano = null;
    for (const p of pasos) {
      if (p.t0 > t) continue; const k = seg(t, p.t0, p.t1);
      if (p.objeto === id && (p.hacer === 'cargar' || p.hacer === 'dejar')) enMano = p;
      if (p.o !== id) continue;
      if (p.hacer === 'mover') {
        const h = new THREE.Vector3(...p.hacia), d = h.clone().sub(bp);
        if (p.orientar && d.lengthSq() > 1e-4) o.rotation.y = Math.atan2(d.x, d.z) - Math.PI / 2;
        if (p.rot !== undefined) o.rotation.y = lerp(o.rotation.y, p.rot, eio(k));
        o.position.lerpVectors(bp, h, eio(k)); bp.copy(o.position);
      }
      if (p.hacer === 'caer') {  // cae desde su altura al suelo con rebote y giro
        const suelo = p.hasta ?? 0.25, y0 = bp.y;
        o.position.y = k < 0.7 ? lerp(y0, suelo, (k / 0.7) ** 2) : suelo + Math.abs(Math.sin((k - 0.7) / 0.3 * Math.PI)) * 0.15 * (1 - k);
        const kk = eo(k); o.position.z = bp.z + (p.avance ?? 0.9) * kk; o.position.x = bp.x + (p.lateral ?? 0) * kk;
        o.rotation.x = b.rot.x + kk * (p.giro ?? 1.6); o.rotation.z = b.rot.z + kk * 0.4;
      }
      if (p.hacer === 'brazo' && o.getObjectByName('brazo')) o.getObjectByName('brazo').rotation.z = lerp(0, p.ang ?? 0.5, Math.sin(Math.PI * k));
      if (p.hacer === 'girarCabina' && o.getObjectByName('giro')) o.getObjectByName('giro').rotation.y = lerp(0, p.ang ?? 1, eio(k));
      if (p.hacer === 'horquilla' && o.getObjectByName('horquilla')) o.getObjectByName('horquilla').position.y = lerp(0.12, p.altura ?? 1.2, eio(k));
    }
    if (enMano) {  // pegado al hombro del actor que lo carga
      const act = A[enMano.a]; act.userData.cuello.getWorldPosition(wp);
      const h = wp.clone(); h.y -= 0.02; h.add(new THREE.Vector3(0.42, 0, 0.05).applyAxisAngle(new THREE.Vector3(0, 1, 0), act.rotation.y));
      const desde = bp.clone(); if (o.parent !== scene) o.parent.localToWorld(desde);
      const dest = enMano.hacer === 'dejar' && enMano.en ? new THREE.Vector3(...enMano.en) : desde;
      const k = enMano.hacer === 'cargar' ? eo(seg(t, enMano.t0, enMano.t0 + 0.5)) : 1 - eio(seg(t, enMano.t0, enMano.t1));
      const pw = dest.clone().lerp(h, k); if (o.parent !== scene) o.parent.worldToLocal(pw);
      o.position.copy(pw); o.rotation.y = lerp(b.rot.y, act.rotation.y, k);
    }
    const bal = o.getObjectByName && o.getObjectByName('baliza'); if (bal) bal.material.emissiveIntensity = 0.5 + 0.5 * Math.sin(t * 12);
  }

  // cámara: [{t, plano:'general'|'medio'|'cerca'|'detalle'|'alto', a:'id', ang:radianes, dur}]
  const PLANOS = { general: [13, 7.5, 1.0], medio: [9, 5.0, 1.2], cerca: [6.6, 3.6, 1.4], detalle: [4.8, 2.7, 1.3], alto: [9, 10, 0.5] };
  const camPasos = (PLAN.camara || [{ t: 0, plano: 'general' }]).map(c => ({ ...c, t0: tt(c.t), dur: c.dur ?? 0.9 })).sort((a, b) => a.t0 - b.t0);
  function posCam(c, t) {
    const [d, y, ty] = PLANOS[c.plano] || PLANOS.general; const o = c.a ? (A[c.a] || O[c.a]) : null;
    if (o) o.getWorldPosition(objetivo); else objetivo.set(...(c.mirar || [0, 0, 0]));
    const ang = (c.ang ?? 0.35) + (c.orbita ? (t - c.t0) * c.orbita : 0) + Math.sin(t * 0.4) * 0.03;
    const dd = d * (1 - Math.min(1, (t - c.t0) * 0.012));  // empuje lento
    return { p: new THREE.Vector3(objetivo.x + Math.sin(ang) * dd, y + Math.sin(t * 0.7) * 0.05, objetivo.z + Math.cos(ang) * dd), m: new THREE.Vector3(objetivo.x, ty, objetivo.z) };
  }

  window.renderAt = t => {
    let temblor = 0;
    for (const [id, m] of Object.entries(A)) { const w = evaluarActor(id, m, t); temblor = Math.max(temblor, w.tambaleo * 0.035, w.caido > 0 && w.caido < 1 ? 0.08 : 0); }
    for (const [id, o] of Object.entries(O)) evaluarObjeto(id, o, t);
    for (const p of pasos) if (p.ring) {
      const vis = t >= p.t0 && t < p.t1; p.ring.visible = vis;
      if (vis) { const o = A[p.a] || O[p.o] || O[p.a]; if (o) { o.getWorldPosition(wp); p.ring.position.set(wp.x, 0.08, wp.z); } const k = (t * 1.6) % 1; p.ring.scale.setScalar(0.8 + k * 0.6); p.ring.material.opacity = 0.9 * (1 - k); }
      if (p.hacer === 'caer' && t >= p.t0 && t < p.t0 + 0.6) temblor = Math.max(temblor, 0.05);
    }
    // cámara
    let i = 0; while (i + 1 < camPasos.length && camPasos[i + 1].t0 <= t) i++;
    const act = posCam(camPasos[i], t);
    if (i > 0) { const prev = posCam(camPasos[i - 1], t); const k = eio(seg(t, camPasos[i].t0, camPasos[i].t0 + camPasos[i].dur)); act.p.lerpVectors(prev.p, act.p, k); act.m.lerpVectors(prev.m, act.m, k); }
    cam.position.copy(act.p).add(new THREE.Vector3(Math.sin(t * 31) * temblor, Math.cos(t * 27) * temblor, 0));
    cam.lookAt(act.m);
    renderer.render(scene, cam);
  };
  window.renderAt(0);
  window.__listo = true;
}
