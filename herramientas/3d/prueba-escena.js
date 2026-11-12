// Prueba 3D Base Segura: trabajador carga saco de 50 kg y luego usan carro. Render determinista: window.renderAt(seg)
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

const W = 1080, H = 1920;
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.getElementById('gl').appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color('#141b29');
scene.fog = new THREE.Fog('#141b29', 18, 34);
const cam = new THREE.PerspectiveCamera(38, W / H, 0.1, 100);

// Luces: cielo suave + sol con sombras + relleno azul de marca
scene.add(new THREE.HemisphereLight('#cfe8ff', '#2a2f3a', 1.1));
const sol = new THREE.DirectionalLight('#fff4e0', 2.6);
sol.position.set(5, 10, 6);
sol.castShadow = true;
sol.shadow.mapSize.set(2048, 2048);
Object.assign(sol.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8, near: 1, far: 30 });
sol.shadow.radius = 6;
scene.add(sol);
const rim = new THREE.DirectionalLight('#1FA9E8', 1.4);
rim.position.set(-6, 4, -5);
scene.add(rim);

const mat = (c, r = 0.45, m = 0) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
const caja = (w, h, d, c, rad = 0.06) => {
  const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, rad), mat(c));
  m.castShadow = m.receiveShadow = true; return m;
};
const esfera = (r, c) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 24), mat(c, 0.35)); m.castShadow = true; return m; };
const capsula = (r, l, c) => { const m = new THREE.Mesh(new THREE.CapsuleGeometry(r, l, 8, 16), mat(c, 0.4)); m.castShadow = true; return m; };

// ---------- Escenario tipo maqueta ----------
const piso = caja(14, 0.4, 10, '#2b3446', 0.15); piso.position.y = -0.2; scene.add(piso);
const loza = caja(9, 0.06, 6, '#3a465c', 0.03); loza.position.set(0, 0.03, 0); scene.add(loza);
for (let i = -3; i <= 3; i++) { const l = caja(0.5, 0.02, 0.12, '#F2A33A', 0.01); l.position.set(i * 1.3, 0.07, 2.6); scene.add(l); }
// Bodega (ferretería) al fondo
const muro = caja(9, 3.2, 0.3, '#e9e2d4', 0.05); muro.position.set(0, 1.6, -3); scene.add(muro);
const techo = caja(9.6, 0.35, 1.4, '#F2A33A', 0.08); techo.position.set(0, 3.25, -2.6); scene.add(techo);
const porton = caja(3.2, 2.4, 0.1, '#5b6578', 0.04); porton.position.set(-1.6, 1.2, -2.83); scene.add(porton);
for (let i = 0; i < 6; i++) { const r = caja(3.1, 0.04, 0.12, '#4a5366', 0.01); r.position.set(-1.6, 0.4 + i * 0.36, -2.76); scene.add(r); }
const letrero = caja(2.6, 0.55, 0.12, '#1FA9E8', 0.08); letrero.position.set(2.4, 2.55, -2.8); scene.add(letrero);
// Cono
const cono = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.6, 24), mat('#F2A33A', 0.5)); cono.position.set(3.8, 0.3, 1.8); cono.castShadow = true; scene.add(cono);

// Pallet con sacos
const pallet = new THREE.Group(); scene.add(pallet); pallet.position.set(1.2, 0, -0.6);
const base = caja(1.6, 0.18, 1.2, '#a8763e', 0.03); base.position.y = 0.09; pallet.add(base);
const SACO = '#e8dcc0';
const sacoGeo = () => { const s = caja(0.62, 0.26, 0.42, SACO, 0.12); return s; };
const sacos = [];
for (let f = 0; f < 3; f++) for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) {
  const s = sacoGeo(); s.position.set(-0.36 + i * 0.72, 0.31 + f * 0.27, -0.24 + j * 0.48); pallet.add(s); sacos.push(s);
}
const sacoMovil = sacoGeo(); scene.add(sacoMovil);

// Carro (transpaleta simple)
const carro = new THREE.Group(); scene.add(carro);
const plat = caja(1.3, 0.12, 0.9, '#1FA9E8', 0.05); plat.position.y = 0.32; carro.add(plat);
const asa = caja(0.08, 1.1, 0.08, '#0D1117', 0.03); asa.position.set(0.68, 0.85, 0); carro.add(asa);
const asa2 = caja(0.08, 0.08, 0.8, '#0D1117', 0.03); asa2.position.set(0.68, 1.38, 0); carro.add(asa2);
for (const [x, z] of [[-0.5, -0.35], [0.5, -0.35], [-0.5, 0.35], [0.5, 0.35]]) {
  const r = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.1, 20), mat('#222', 0.6)); r.rotation.x = Math.PI / 2;
  r.position.set(x, 0.13, z); r.castShadow = true; carro.add(r);
}
const sacosCarro = [];
for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) { const s = sacoGeo(); s.position.set(-0.32 + i * 0.64, 0.51, -0.22 + j * 0.44); carro.add(s); sacosCarro.push(s); }

// ---------- Personaje tipo juguete ----------
function muneco({ chaleco = '#F2A33A', pantalon = '#1d3557', casco = '#FFD23F', piel = '#f1c6a0' } = {}) {
  const g = new THREE.Group();
  const cadera = new THREE.Group(); cadera.position.y = 0.78; g.add(cadera);
  const torso = new THREE.Group(); cadera.add(torso);
  const cuerpo = caja(0.62, 0.72, 0.42, chaleco, 0.16); cuerpo.position.y = 0.36; torso.add(cuerpo);
  for (const y of [0.22, 0.42]) { const b = caja(0.64, 0.05, 0.44, '#e8f6ff', 0.02); b.position.y = y; b.material.emissive = new THREE.Color('#9fd8ff'); b.material.emissiveIntensity = 0.25; torso.add(b); }
  const cuello = new THREE.Group(); cuello.position.y = 0.78; torso.add(cuello);
  const cabeza = esfera(0.3, piel); cabeza.scale.set(1, 0.95, 0.95); cabeza.position.y = 0.22; cuello.add(cabeza);
  const ojoM = mat('#141414', 0.2);
  const ojos = [];
  for (const x of [-0.1, 0.1]) { const o = new THREE.Mesh(new THREE.SphereGeometry(0.045, 16, 12), ojoM); o.position.set(x, 0.26, 0.27); cuello.add(o); ojos.push(o);
    const br = new THREE.Mesh(new THREE.SphereGeometry(0.014, 8, 6), mat('#fff', 0.1)); br.position.set(x + 0.015, 0.275, 0.31); cuello.add(br); }
  const boca = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.016, 8, 20, Math.PI), mat('#7a2e2e', 0.4));
  boca.rotation.z = Math.PI; boca.position.set(0, 0.16, 0.27); cuello.add(boca);
  const mej = mat('#ff9b8a', 0.6); for (const x of [-0.18, 0.18]) { const m = new THREE.Mesh(new THREE.SphereGeometry(0.04, 12, 8), mej); m.position.set(x, 0.18, 0.24); m.scale.z = 0.4; cuello.add(m); }
  const c1 = new THREE.Mesh(new THREE.SphereGeometry(0.33, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), mat(casco, 0.3)); c1.position.y = 0.3; c1.castShadow = true; cuello.add(c1);
  const ala = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.04, 32), mat(casco, 0.3)); ala.position.set(0, 0.3, 0.05); ala.castShadow = true; cuello.add(ala);
  const brazo = (lado) => {
    const hombro = new THREE.Group(); hombro.position.set(lado * 0.4, 0.62, 0); torso.add(hombro);
    const b = capsula(0.09, 0.38, chaleco); b.position.y = -0.24; hombro.add(b);
    const mano = esfera(0.1, piel); mano.position.y = -0.5; hombro.add(mano);
    return hombro;
  };
  const pierna = (lado) => {
    const p = new THREE.Group(); p.position.set(lado * 0.16, 0, 0); cadera.add(p);
    const l = capsula(0.12, 0.42, pantalon); l.position.y = -0.33; p.add(l);
    const bota = caja(0.24, 0.16, 0.34, '#3b2a1e', 0.06); bota.position.set(0, -0.7, 0.05); p.add(bota);
    return p;
  };
  const partes = { cadera, torso, cuello, brazoI: brazo(-1), brazoD: brazo(1), piernaI: pierna(-1), piernaD: pierna(1), ojos, boca, cuerpo };
  g.userData = partes;
  return g;
}
const pedro = muneco(); scene.add(pedro);
const ana = muneco({ chaleco: '#1FA9E8', casco: '#ffffff', piel: '#d9a27a', pantalon: '#24324a' }); scene.add(ana);

// ---------- utilidades de tiempo ----------
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (t, a, b) => cl((t - a) / (b - a));
const eo = x => 1 - Math.pow(1 - x, 3);           // ease out
const eio = x => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const back = x => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;

function pose(m, t, { caminar = 0, agacharse = 0, carga = 0, tambaleo = 0, feliz = 0, empujar = 0 }) {
  const p = m.userData;
  const paso = Math.sin(t * 9) * caminar;
  p.piernaI.rotation.x = paso * 0.7; p.piernaD.rotation.x = -paso * 0.7;
  p.cadera.position.y = 0.78 + Math.abs(Math.cos(t * 9)) * 0.05 * caminar - agacharse * 0.22 + Math.sin(t * 2.2) * 0.008;
  p.torso.rotation.x = agacharse * 0.75 + empujar * 0.35 + carga * 0.18;
  p.torso.rotation.z = Math.sin(t * 7) * 0.12 * tambaleo;
  p.piernaI.rotation.x += agacharse * -0.5; p.piernaD.rotation.x += agacharse * -0.5;
  // brazos
  const balanceo = -paso * 0.6 * (1 - carga) * (1 - empujar);
  p.brazoI.rotation.x = balanceo + agacharse * -1.1 - empujar * 1.2; p.brazoD.rotation.x = -balanceo + agacharse * -1.1 - empujar * 1.2;
  p.brazoD.rotation.z = carga * 2.6 + feliz * 2.7; p.brazoI.rotation.z = -carga * 0.5 - feliz * 2.7;
  p.brazoD.rotation.x += carga * -0.2;
  // cara: parpadeo + sonrisa/tristeza
  const parp = (t % 2.7) < 0.12 ? 0.15 : 1;
  p.ojos.forEach(o => o.scale.y = parp);
  p.boca.rotation.z = tambaleo > 0.3 ? 0 : Math.PI;
  p.boca.position.y = tambaleo > 0.3 ? 0.12 : 0.16;
  p.cuerpo.material.emissive?.set(tambaleo > 0.3 ? '#ff2a2a' : '#000');
  p.cuerpo.material.emissiveIntensity = tambaleo > 0.3 ? 0.25 + 0.2 * Math.sin(t * 14) : 0;
}

const objetivo = new THREE.Vector3();
window.renderAt = (t) => {
  // --- Pedro: entra caminando, toma saco, se tambalea, lo deja ---
  const camina = seg(t, 0.3, 2.2);
  pedro.position.set(lerp(-2.4, 0.0, eio(camina)), 0, lerp(1.2, 0.2, eio(camina)));
  pedro.rotation.y = lerp(1.2, 0.55, eo(camina));
  const agacha = seg(t, 2.2, 2.7) - seg(t, 2.9, 3.4);
  const levanta = seg(t, 2.9, 3.4) - seg(t, 6.4, 7.0);
  const tamb = seg(t, 3.4, 3.7) - seg(t, 6.2, 6.5);
  const feliz = seg(t, 10.6, 11.0);
  pose(pedro, t, { caminar: camina > 0 && camina < 1 ? 1 : 0, agacharse: cl(agacha + seg(t, 6.4, 6.8) - seg(t, 7.0, 7.4)), carga: levanta, tambaleo: tamb, feliz });
  if (tamb > 0) pedro.position.x += Math.sin(t * 7) * 0.06 * tamb;
  // saco: del pallet al hombro y de vuelta
  const tope = sacos[sacos.length - 1]; tope.visible = !(t > 2.9 && t < 7.0);
  sacoMovil.visible = t > 2.9 && t < 7.0;
  if (sacoMovil.visible) {
    const desdePallet = new THREE.Vector3(); tope.getWorldPosition(desdePallet);
    const hombro = new THREE.Vector3(); pedro.userData.cuello.getWorldPosition(hombro); hombro.y -= 0.02; hombro.x += 0.42; hombro.z += 0.05;
    const k = eo(seg(t, 2.9, 3.4)) * (1 - eio(seg(t, 6.4, 7.0)));
    sacoMovil.position.lerpVectors(desdePallet, hombro, k);
    sacoMovil.rotation.set(0, pedro.rotation.y, Math.sin(t * 7) * 0.2 * tamb);
  }
  // --- Ana: entra con el carro ---
  const llega = seg(t, 7.2, 9.6);
  ana.position.set(lerp(6.5, 2.9, eio(llega)), 0, 1.0);
  ana.rotation.y = -Math.PI / 2 + feliz * 1.2;
  carro.position.set(ana.position.x - 1.05, 0, 1.0);
  carro.rotation.y = 0;
  pose(ana, t, { caminar: llega > 0 && llega < 1 ? 1 : 0, empujar: 1 - feliz, feliz });
  carro.children.filter(c => c.geometry?.type === 'CylinderGeometry').forEach(r => r.rotation.y = -ana.position.x * 3);
  sacosCarro.forEach((s, i) => { s.visible = t > 9.8 + i * 0.15; s.position.y = 0.51 + (1 - back(seg(t, 9.8 + i * 0.15, 10.2 + i * 0.15))) * 0.6; });
  if (feliz > 0) pedro.rotation.y = lerp(0.55, 0.2, feliz);

  // --- Cámara: plano abierto → acercamiento con temblor → abre → leve órbita ---
  const zoom = eio(seg(t, 1.8, 3.6)) - eio(seg(t, 6.3, 7.6));
  const orb = eio(seg(t, 9.6, 14)) * 0.35;
  const dist = lerp(12.5, 7.8, zoom), ang = 0.35 + orb - zoom * 0.15;
  const temb = tamb * 0.04;
  cam.position.set(Math.sin(ang) * dist + Math.sin(t * 31) * temb, lerp(7.2, 4.0, zoom) + Math.cos(t * 27) * temb, Math.cos(ang) * dist);
  objetivo.set(lerp(0.6, pedro.position.x, zoom), lerp(1.0, 1.4, zoom), lerp(0.2, 0.2, zoom));
  cam.lookAt(objetivo);
  renderer.render(scene, cam);
};
window.renderAt(0);
window.__listo = true;
