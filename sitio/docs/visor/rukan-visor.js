/*
 * <rukan-visor> — el visor 3D de una escena `rukan/escena@2`.
 *
 *   <rukan-visor src="galpon-grua.escena.json" modo="1"></rukan-visor>
 *   <rukan-visor src="galpon-grua.escena.json" caso="H_alero" vista="transversal"></rukan-visor>
 *   <rukan-visor src="galpon-grua.escena.json" caso="D" esfuerzo="Mz"
 *                filtro="RAF3_*,COL3A_*"></rukan-visor>
 *
 * Atributos: `src` (obligatorio, relativo a la página), `modo` (número de modo),
 * `caso` (nombre de caso o combinación; excluyente con `modo`), `esfuerzo`
 * (N | Vy | Vz | T | My | Mz; pide `caso`), `filtro` (globs sobre el nombre de
 * barra, separados por coma), `vista` (iso | planta | transversal |
 * longitudinal; por omisión iso), `escala` (factor sobre la escala automática,
 * por omisión 1), `animar` (presente = arranca animando), `alto` (px, por
 * omisión 460).
 *
 * Qué dibuja: barras sin deformar en trazo tenue, la deformada en acento,
 * apoyos como cubos, nudos con masa como puntos. Cámara ortográfica con
 * órbita, como las figuras de `vista.py`, y la misma paleta. Sin eliminación
 * de líneas ocultas ni sombreado: es un reticulado de líneas, y en una
 * estructura de barras eso se lee mejor que lo contrario.
 *
 * Con `esfuerzo` puesto, cada barra se pinta con una rampa divergente según el
 * valor del componente elegido —frío negativo, acento positivo— y, **solo para
 * las barras que `filtro` selecciona**, se dibuja además el diagrama normal al
 * eje. La regla es una sola: sin `filtro` no hay diagrama, porque mil barras con
 * su diagrama en una axonometría son una maraña ilegible (la misma razón por la
 * que `vista.escena()` tiene `filtro`). La ordenada va sobre el eje local `y`
 * para N, Vy, T y Mz, y sobre el `z` para Vz y My, con su signo tal cual y no
 * sobre la cara traccionada, que sería una segunda convención sin justificar.
 *
 * La escala automática hace que el desplazamiento —o la ordenada del diagrama—
 * máximo sea un 5 % de la diagonal del modelo; el deslizador la multiplica. El
 * rótulo bajo el lienzo dice siempre qué se está viendo y con qué factor: una
 * deformada, o un diagrama, sin escala declarada es una figura que miente.
 *
 * Dependencias: three.js, vendoreado en `vendor/` (ver `vendor/VERSION`) y
 * resuelto por el importmap de `overrides/main.html`, y `./esfuerzos.js`, que es
 * el gemelo de `rukan/esfuerzos.py` y no importa nada (ver su cabecera).
 */

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { COMPONENTES, esfuerzo, ejesLocales } from './esfuerzos.js';

const ESQUEMA = 'rukan/escena@2';
const PALETA = {            // = rukan.vista.PALETA
  tinta: '#2b2a26', suave: '#8a8578', linea: '#c9c4b5',
  fondo: '#fcfcfa', acento: '#a4442c', frio: '#2f5d7c',
};
const FRACCION = 0.05;      // δ_max / diagonal del modelo, escala automática
const PERIODO_ANIM = 2.4;   // s por ciclo de animación
const NSUB_COLOR = 8;       // tramos por barra al pintar: la parábola se ve
const NSUB_DIAG = 12;       // estaciones del diagrama normal al eje
// El eje local sobre el que sale la ordenada de cada componente: `y` para lo que
// vive en el plano local x-y, `z` para lo que vive en el x-z.
const EJE_ORDENADA = { N: 1, Vy: 1, T: 1, Mz: 1, Vz: 2, My: 2 };
const VISTAS = {
  iso:          { dir: [Math.cos(rad(25)) * Math.sin(rad(35)), -Math.cos(rad(25)) * Math.cos(rad(35)), Math.sin(rad(25))], up: [0, 0, 1] },
  planta:       { dir: [0, 0, 1],  up: [0, 1, 0] },
  transversal:  { dir: [1, 0, 0],  up: [0, 0, 1] },   // mira el plano YZ, como vista.elevacion("YZ")
  longitudinal: { dir: [0, -1, 0], up: [0, 0, 1] },   // mira el plano XZ
};

function rad(g) { return g * Math.PI / 180; }

// Coma decimal, como en los memos.
function num(v, cifras) {
  if (!Number.isFinite(v)) return '—';
  const s = cifras === undefined ? v.toPrecision(4) : v.toFixed(cifras);
  return s.replace('.', ',');
}
function sci(v) {
  if (v === 0) return '0';
  const a = Math.abs(v);
  return (a >= 1e-3 && a < 1e4) ? num(v) : v.toExponential(3).replace('.', ',');
}
function pct(v) { return num(100 * v, 1) + ' %'; }
function unidadDe(c) { return (c === 'N' || c === 'Vy' || c === 'Vz') ? 'kN' : 'kN·m'; }

// `filtro="RAF3_*,COL3A_*"` -> expresiones regulares sobre el nombre de barra.
function globs(s) {
  return (s || '').split(',').map(t => t.trim()).filter(Boolean).map(t =>
    new RegExp('^' + t.replace(/[.+^${}()|[\]\\]/g, '\\$&')
                      .replace(/\*/g, '.*').replace(/\?/g, '.') + '$'));
}

const C_FRIO = new THREE.Color(PALETA.frio);
const C_ACENTO = new THREE.Color(PALETA.acento);
const C_CERO = new THREE.Color(PALETA.linea);   // en cero, una barra normal
const _c = new THREE.Color();
// Rampa divergente: frío para lo negativo, acento para lo positivo, casi neutro
// en cero. `t` viene normalizado por el máximo absoluto del componente.
function rampa(t) {
  _c.copy(C_CERO);
  return t < 0 ? _c.lerp(C_FRIO, Math.min(1, -t)) : _c.lerp(C_ACENTO, Math.min(1, t));
}

let cssPuesto = false;
function ponerCss() {
  if (cssPuesto) return;
  cssPuesto = true;
  const st = document.createElement('style');
  st.textContent = `
    rukan-visor { display:block; margin:1.2em 0; font-family: ui-monospace,'IBM Plex Mono',Menlo,Consolas,monospace; font-size:.78rem; color:${PALETA.tinta}; }
    rukan-visor .rk-barra { display:flex; flex-wrap:wrap; gap:.4em .9em; align-items:center; padding:.45em .6em; background:#f1efe8; border:1px solid ${PALETA.linea}; border-bottom:0; border-radius:4px 4px 0 0; }
    rukan-visor .rk-barra label { display:inline-flex; align-items:center; gap:.35em; white-space:nowrap; }
    rukan-visor .rk-barra select, rukan-visor .rk-barra input[type=range] { font:inherit; color:inherit; background:${PALETA.fondo}; border:1px solid ${PALETA.linea}; border-radius:3px; padding:.1em .3em; max-width:16em; }
    rukan-visor .rk-barra input[type=range] { width:7em; padding:0; }
    rukan-visor .rk-barra button { font:inherit; color:inherit; background:${PALETA.fondo}; border:1px solid ${PALETA.linea}; border-radius:3px; padding:.1em .6em; cursor:pointer; }
    rukan-visor .rk-barra button[aria-pressed=true] { background:${PALETA.tinta}; color:${PALETA.fondo}; border-color:${PALETA.tinta}; }
    rukan-visor .rk-lienzo { position:relative; border:1px solid ${PALETA.linea}; background:${PALETA.fondo}; overflow:hidden; }
    rukan-visor .rk-lienzo canvas { display:block; }
    rukan-visor .rk-tip { position:absolute; pointer-events:none; background:${PALETA.fondo}; border:1px solid ${PALETA.suave}; border-radius:3px; padding:.35em .55em; white-space:pre; line-height:1.35; box-shadow:0 1px 4px rgba(0,0,0,.12); display:none; z-index:2; }
    rukan-visor .rk-pie { padding:.4em .6em; border:1px solid ${PALETA.linea}; border-top:0; border-radius:0 0 4px 4px; color:${PALETA.suave}; background:#f7f6f2; }
    rukan-visor .rk-pie b { color:${PALETA.tinta}; font-weight:600; }
    rukan-visor .rk-rampa { display:inline-block; width:5.5em; height:.7em; vertical-align:-.05em; border:1px solid ${PALETA.linea}; border-radius:2px; background:linear-gradient(to right, ${PALETA.frio}, ${PALETA.linea}, ${PALETA.acento}); }
    rukan-visor .rk-barra button:disabled { color:${PALETA.suave}; cursor:default; }
    rukan-visor .rk-barra select:disabled { color:${PALETA.suave}; background:#f1efe8; }
  `;
  document.head.appendChild(st);
}

class RukanVisor extends HTMLElement {
  connectedCallback() {
    if (this._iniciado) return;
    this._iniciado = true;
    ponerCss();
    this.alto = parseInt(this.getAttribute('alto') || '460', 10);
    this._dom();
    const src = new URL(this.getAttribute('src'), document.baseURI).href;
    fetch(src).then(r => {
      if (!r.ok) throw new Error(`${r.status} al pedir ${src}`);
      return r.json();
    }).then(esc => this._arrancar(esc)).catch(err => {
      this.pie.innerHTML = `<b>No se pudo cargar la escena:</b> ${err.message}`;
    });
  }

  disconnectedCallback() {
    if (this.ro) this.ro.disconnect();
    if (this.renderer) { this.renderer.setAnimationLoop(null); this.renderer.dispose(); }
  }

  // ------------------------------------------------------------ DOM
  _dom() {
    this.innerHTML = '';
    this.barra = el('div', 'rk-barra');
    this.selVista = this._select('Vista', Object.keys(VISTAS).map(k => [k, k]));
    this.selModo = this._select('Modo', [['', '—']]);
    this.selCaso = this._select('Caso', [['', '—']]);
    this.selEsf = this._select('Esfuerzo',
      [['', '—']].concat(COMPONENTES.map(c => [c, c])));
    this.rango = el('input'); this.rango.type = 'range';
    this.rango.min = -1; this.rango.max = 1; this.rango.step = 0.05; this.rango.value = 0;
    const lr = el('label'); lr.append('Escala', this.rango); this.barra.append(lr);
    this.btnAnim = el('button'); this.btnAnim.textContent = 'Animar';
    this.btnAnim.setAttribute('aria-pressed', 'false');
    this.barra.append(this.btnAnim);
    this.lienzo = el('div', 'rk-lienzo');
    this.lienzo.style.height = this.alto + 'px';
    this.tip = el('div', 'rk-tip');
    this.lienzo.append(this.tip);
    this.pie = el('div', 'rk-pie');
    this.pie.textContent = 'Cargando la escena…';
    this.append(this.barra, this.lienzo, this.pie);
  }

  _select(rotulo, opciones) {
    const s = el('select');
    for (const [v, t] of opciones) { const o = el('option'); o.value = v; o.textContent = t; s.append(o); }
    const l = el('label'); l.append(rotulo, s); this.barra.append(l);
    return s;
  }

  // ------------------------------------------------------------ escena
  _arrancar(esc) {
    if (esc.esquema !== ESQUEMA) {
      throw new Error(`la escena es ${esc.esquema || 'de esquema desconocido'} y ` +
                      `este visor dibuja ${ESQUEMA}; hay que regenerarla con ` +
                      '`python -m rukan escena`');
    }
    this.esc = esc;
    this.setAttribute('aria-label', esc.titulo || 'Modelo');
    const idx = new Map(esc.nudos.map((n, k) => [n.id, k]));
    this.idx = idx;
    const N = esc.nudos.length;
    this.base = new Float32Array(N * 3);
    esc.nudos.forEach((n, k) => { this.base.set(n.xyz, k * 3); });
    this.pares = new Uint32Array(esc.barras.length * 2);
    esc.barras.forEach((b, k) => { this.pares[2 * k] = idx.get(b.i); this.pares[2 * k + 1] = idx.get(b.j); });
    // Geometría de cada barra: extremos, largo y ejes locales. Los ejes salen de
    // `vecxz` con la misma función que `loads.local_axes`, cruzada contra ella
    // en `tests/test_esfuerzos_js.py`.
    this.geoBarra = esc.barras.map(b => {
      const pi = esc.nudos[idx.get(b.i)].xyz, pj = esc.nudos[idx.get(b.j)].xyz;
      return { pi, pj, L: Math.hypot(pj[0] - pi[0], pj[1] - pi[1], pj[2] - pi[2]),
               ejes: ejesLocales(pi, pj, b.vecxz) };
    });
    this.filtro = globs(this.getAttribute('filtro'));
    this.barrasFiltradas = this.filtro.length
      ? esc.barras.map((b, k) => k).filter(k => {
          const nm = String(esc.barras[k].nombre || esc.barras[k].id);
          return this.filtro.some(rx => rx.test(nm));
        })
      : [];

    // caja y diagonal
    const bb = new THREE.Box3();
    for (let k = 0; k < N; k++) bb.expandByPoint(new THREE.Vector3(this.base[3 * k], this.base[3 * k + 1], this.base[3 * k + 2]));
    this.centro = bb.getCenter(new THREE.Vector3());
    this.diag = bb.getSize(new THREE.Vector3()).length() || 1;
    this.esquinas = [];
    for (const x of [bb.min.x, bb.max.x]) for (const y of [bb.min.y, bb.max.y]) for (const z of [bb.min.z, bb.max.z])
      this.esquinas.push(new THREE.Vector3(x, y, z));

    // three
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(PALETA.fondo);
    this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, -100 * this.diag, 100 * this.diag);
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setPixelRatio(window.devicePixelRatio || 1);
    this.lienzo.prepend(this.renderer.domElement);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = false;
    this.controls.target.copy(this.centro);
    this.controls.addEventListener('change', () => this._render());

    // geometría sin deformar
    const gBase = new THREE.BufferGeometry();
    gBase.setAttribute('position', new THREE.BufferAttribute(this.base, 3));
    gBase.setIndex(new THREE.BufferAttribute(this.pares, 1));
    this.lineasBase = new THREE.LineSegments(gBase, new THREE.LineBasicMaterial({ color: PALETA.linea }));
    this.scene.add(this.lineasBase);

    // deformada
    this.def = new Float32Array(this.base);
    const gDef = new THREE.BufferGeometry();
    this.attrDef = new THREE.BufferAttribute(this.def, 3);
    this.attrDef.setUsage(THREE.DynamicDrawUsage);
    gDef.setAttribute('position', this.attrDef);
    gDef.setIndex(new THREE.BufferAttribute(this.pares, 1));
    this.lineasDef = new THREE.LineSegments(gDef, new THREE.LineBasicMaterial({ color: PALETA.acento }));
    this.lineasDef.visible = false;
    this.scene.add(this.lineasDef);

    // Barras subdivididas para pintar el esfuerzo: las posiciones son fijas (el
    // color va sobre la geometría sin deformar), los colores se recalculan.
    const S = NSUB_COLOR, M = esc.barras.length;
    const posC = new Float32Array(M * S * 2 * 3);
    this.colC = new Float32Array(M * S * 2 * 3);
    let o = 0;
    for (const g of this.geoBarra) {
      for (let s = 0; s < S; s++) {
        for (const t of [s / S, (s + 1) / S]) {
          posC[o++] = g.pi[0] + t * (g.pj[0] - g.pi[0]);
          posC[o++] = g.pi[1] + t * (g.pj[1] - g.pi[1]);
          posC[o++] = g.pi[2] + t * (g.pj[2] - g.pi[2]);
        }
      }
    }
    const gCol = new THREE.BufferGeometry();
    gCol.setAttribute('position', new THREE.BufferAttribute(posC, 3));
    this.attrCol = new THREE.BufferAttribute(this.colC, 3);
    this.attrCol.setUsage(THREE.DynamicDrawUsage);
    gCol.setAttribute('color', this.attrCol);
    this.lineasCol = new THREE.LineSegments(
      gCol, new THREE.LineBasicMaterial({ vertexColors: true }));
    this.lineasCol.visible = false;
    this.scene.add(this.lineasCol);

    // El diagrama normal al eje se rehace cada vez que cambia algo: son pocas
    // barras (las que `filtro` selecciona), así que no vale la pena preasignar.
    this.gDiag = new THREE.Group();
    this.scene.add(this.gDiag);

    // nudos (para el tooltip) y masas
    const gPts = new THREE.BufferGeometry();
    gPts.setAttribute('position', new THREE.BufferAttribute(this.base, 3));
    this.puntos = new THREE.Points(gPts, new THREE.PointsMaterial({ color: PALETA.tinta, size: 3, sizeAttenuation: false }));
    this.puntos.visible = false;
    this.scene.add(this.puntos);
    if (esc.masas.length) {
      const pm = new Float32Array(esc.masas.length * 3);
      esc.masas.forEach((m, k) => { const j = idx.get(m.nudo); pm.set(this.base.subarray(3 * j, 3 * j + 3), 3 * k); });
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.BufferAttribute(pm, 3));
      this.scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: PALETA.tinta, size: 5, sizeAttenuation: false })));
    }
    // apoyos
    const apoyos = esc.nudos.filter(n => n.fijo && n.fijo.some(Boolean));
    if (apoyos.length) {
      const lado = 0.012 * this.diag;
      const cubo = new THREE.InstancedMesh(new THREE.BoxGeometry(lado, lado, lado),
        new THREE.MeshBasicMaterial({ color: PALETA.tinta }), apoyos.length);
      const m4 = new THREE.Matrix4();
      apoyos.forEach((n, k) => { m4.makeTranslation(n.xyz[0], n.xyz[1], n.xyz[2] - lado / 2); cubo.setMatrixAt(k, m4); });
      this.scene.add(cubo);
    }

    // controles
    for (const m of esc.modos) {
      const o = el('option'); o.value = String(m.n);
      o.textContent = `${m.n} · T = ${num(m.T, 3)} s · ${this._dominante(m)}`;
      this.selModo.append(o);
    }
    for (const c of Object.keys(esc.casos)) { const o = el('option'); o.value = 'c:' + c; o.textContent = c; this.selCaso.append(o); }
    for (const c of Object.keys(esc.combinaciones)) { const o = el('option'); o.value = 'k:' + c; o.textContent = c + ' (comb.)'; this.selCaso.append(o); }
    this.selVista.addEventListener('change', () => this._vista(this.selVista.value));
    this.selModo.addEventListener('change', () => { if (this.selModo.value) this.selCaso.value = ''; this._estado(); });
    this.selCaso.addEventListener('change', () => { if (this.selCaso.value) this.selModo.value = ''; this._estado(); });
    this.selEsf.addEventListener('change', () => this._estado());
    this.rango.addEventListener('input', () => this._estado());
    this.btnAnim.addEventListener('click', () => this._animar(!this.animando));
    this.renderer.domElement.addEventListener('mousemove', e => this._hover(e));
    this.renderer.domElement.addEventListener('mouseleave', () => { this.tip.style.display = 'none'; });
    this.raycaster = new THREE.Raycaster();
    this.raycaster.params.Points.threshold = 0.012 * this.diag;
    this.raycaster.params.Line.threshold = 0.006 * this.diag;

    // estado inicial desde los atributos
    const modo = this.getAttribute('modo'), caso = this.getAttribute('caso');
    if (modo && esc.modos.some(m => String(m.n) === modo)) this.selModo.value = modo;
    else if (caso && esc.casos[caso]) this.selCaso.value = 'c:' + caso;
    else if (caso && esc.combinaciones[caso]) this.selCaso.value = 'k:' + caso;
    const esf = this.getAttribute('esfuerzo');
    if (esf && COMPONENTES.includes(esf)) this.selEsf.value = esf;
    const escala = parseFloat(this.getAttribute('escala') || '1');
    if (escala > 0) this.rango.value = Math.max(-1, Math.min(1, Math.log10(escala)));
    this.selVista.value = VISTAS[this.getAttribute('vista')] ? this.getAttribute('vista') : 'iso';

    this.ro = new ResizeObserver(() => this._tamano());
    this.ro.observe(this.lienzo);
    this._tamano();
    this._vista(this.selVista.value);
    this._estado();
    if (this.hasAttribute('animar')) this._animar(true);
  }

  _dominante(m) {
    const p = m.participacion;
    const d = ['X', 'Y', 'Z'].reduce((a, b) => (p[a] >= p[b] ? a : b));
    return `${d} ${pct(p[d])}`;
  }

  // ------------------------------------------------------------ cámara
  _tamano() {
    const w = this.lienzo.clientWidth || 600, h = this.alto;
    this.renderer.setSize(w, h);
    this._encuadrar();
    this._render();
  }

  // El frustum ortográfico se ajusta a la proyección de la caja del modelo en
  // la dirección actual de la cámara, con un margen: así una elevación llena el
  // lienzo con el marco y no con la diagonal 3D del galpón entero.
  _encuadrar() {
    const w = this.lienzo.clientWidth || 600, h = this.alto, asp = w / h;
    this.camera.updateMatrixWorld();
    const inv = this.camera.matrixWorldInverse;
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    for (const e of this.esquinas) {
      const q = e.clone().applyMatrix4(inv);
      x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y);
    }
    const sx = Math.max((x1 - x0) / 2, 1e-6), sy = Math.max((y1 - y0) / 2, 1e-6);
    const semi = 1.12 * Math.max(sy, sx / asp);
    this.camera.left = -semi * asp; this.camera.right = semi * asp;
    this.camera.top = semi; this.camera.bottom = -semi;
    this.camera.updateProjectionMatrix();
  }

  _vista(nombre) {
    const v = VISTAS[nombre] || VISTAS.iso;
    this.camera.up.set(...v.up);
    this.camera.position.copy(this.centro).addScaledVector(new THREE.Vector3(...v.dir), 2 * this.diag);
    this.camera.lookAt(this.centro);
    this.camera.zoom = 1;
    this._encuadrar();
    this.controls.target.copy(this.centro);
    this.controls.update();
    this._render();
  }

  // ------------------------------------------------------------ estado
  _estado() {
    const esc = this.esc, N = esc.nudos.length;
    this.campo = null; this.rotulo = '';
    const mult = Math.pow(10, parseFloat(this.rango.value));
    // Un modo no tiene esfuerzos, y sin caso no hay nada que evaluar.
    this.selEsf.disabled = !!this.selModo.value || !this.selCaso.value;
    if (this.selEsf.disabled) this.selEsf.value = '';
    this.comp = this.selEsf.value;
    if (this.comp) {
      // Un diagrama no se anima: es un campo estático, no una forma que oscile.
      if (this.animando) this._animar(false);
      this.btnAnim.disabled = true;
      this._esfuerzos(this.comp, mult);
      this.lineasDef.visible = false;
      this.lineasBase.visible = false;
      this.lineasCol.visible = true;
      this.gDiag.visible = true;
      this.pie.innerHTML = this.rotulo;
      this._render();
      return;
    }
    this.lineasCol.visible = false;
    this.gDiag.visible = false;
    this.lineasBase.visible = true;
    this.btnAnim.disabled = false;
    if (this.selModo.value) {
      const m = esc.modos.find(x => String(x.n) === this.selModo.value);
      this.campo = new Float32Array(N * 3);
      m.phi.forEach((v, k) => this.campo.set(v, 3 * k));     // max|phi| = 1
      this.factor = FRACCION * this.diag * mult;
      this.rotulo = `<b>Modo ${m.n}</b> · T = ${num(m.T, 4)} s · X ${pct(m.participacion.X)} · Y ${pct(m.participacion.Y)} · Z ${pct(m.participacion.Z)} · forma normalizada a δ<sub>máx</sub> = ${num(FRACCION * mult * 100, 0)} % de la diagonal`;
    } else if (this.selCaso.value) {
      const [tipo, nombre] = [this.selCaso.value.slice(0, 1), this.selCaso.value.slice(2)];
      const r = tipo === 'c' ? esc.casos[nombre] : esc.combinaciones[nombre];
      this.campo = new Float32Array(N * 3);
      let dmax = 0;
      r.u.forEach((v, k) => { this.campo.set(v.slice(0, 3), 3 * k); dmax = Math.max(dmax, Math.hypot(v[0], v[1], v[2])); });
      this.dmax = dmax;
      this.factor = dmax > 0 ? FRACCION * this.diag / dmax * mult : 0;
      this.rotulo = `<b>${nombre}</b>${tipo === 'k' ? ' (combinación)' : ''} · δ<sub>máx</sub> = ${sci(dmax)} m · deformada ×${num(this.factor, 0)}`;
    } else {
      this.rotulo = `<b>Geometría</b> · ${N} nudos · ${esc.barras.length} barras`;
    }
    this.lineasDef.visible = !!this.campo;
    this.lineasBase.material.color.set(this.campo ? PALETA.linea : PALETA.tinta);
    this.pie.innerHTML = this.rotulo;
    this._deformar(1);
    this._render();
  }

  // ------------------------------------------------------------ esfuerzos
  /** El esfuerzo `comp` de la barra `k` a distancia `x` de su extremo i. */
  _valor(comp, k, x) {
    const r = this._resultado().r, g = this.geoBarra[k];
    return esfuerzo(r.fuerzas[k], r.w ? r.w[k] : null, g.L, comp, x);
  }

  /** Pinta las barras, arma el diagrama del filtro y escribe el rótulo. */
  _esfuerzos(comp, mult) {
    const { nombre, r } = this._resultado();
    const M = this.esc.barras.length, S = NSUB_COLOR;
    // Una sola pasada: el máximo absoluto normaliza el color y fija la escala
    // del diagrama, así los dos hablan de la misma cifra.
    let vmax = 0, arg = { k: 0, x: 0 };
    const vals = new Array(M);
    for (let k = 0; k < M; k++) {
      const g = this.geoBarra[k], fila = new Array(S + 1);
      for (let s = 0; s <= S; s++) {
        const v = esfuerzo(r.fuerzas[k], r.w ? r.w[k] : null, g.L, comp, s * g.L / S);
        fila[s] = v;
        if (Math.abs(v) > vmax) { vmax = Math.abs(v); arg = { k, x: s / S }; }
      }
      vals[k] = fila;
    }
    const esc0 = vmax > 0 ? vmax : 1;
    let o = 0;
    for (let k = 0; k < M; k++) {
      for (let s = 0; s < S; s++) {
        for (const v of [vals[k][s], vals[k][s + 1]]) {
          const c = rampa(v / esc0);
          this.colC[o++] = c.r; this.colC[o++] = c.g; this.colC[o++] = c.b;
        }
      }
    }
    this.attrCol.needsUpdate = true;

    const factor = vmax > 0 ? FRACCION * this.diag / vmax * mult : 0;
    this._diagrama(comp, factor);

    const b = this.esc.barras[arg.k];
    const u = unidadDe(comp);
    this.rotulo =
      `<b>${comp}</b> · <b>${nombre}</b> · máx |${comp}| = ${sci(vmax)} ${u} ` +
      `en ${b.nombre || b.id} (x/L = ${num(arg.x, 2)}) · ` +
      `<span class="rk-rampa"></span> ${sci(-vmax)} … ${sci(vmax)} ${u}` +
      (this.barrasFiltradas.length
        ? ` · diagrama sobre ${this.barrasFiltradas.length} barras, ordenada máx = ` +
          `${num(FRACCION * mult * 100, 0)} % de la diagonal`
        : ' · sin <code>filtro</code> no se dibuja el diagrama');
  }

  /**
   * El diagrama normal al eje, solo para las barras de `filtro`: el contorno y
   * las dos costillas de extremo de cada barra.
   *
   * Solo las de extremo, y no una por estación como se dibuja a mano, porque un
   * miembro de este modelo está mallado en dieciséis tramos: una costilla por
   * estación son mil y pico líneas que se apelmazan en una mancha y tapan el
   * color de las barras. El contorno se lee igual y deja ver lo que hay debajo.
   */
  _diagrama(comp, factor) {
    for (const hijo of this.gDiag.children) hijo.geometry.dispose();
    this.gDiag.clear();
    if (!this.barrasFiltradas.length || !factor) return;
    const eje = EJE_ORDENADA[comp], n = NSUB_DIAG;
    const pts = [];
    for (const k of this.barrasFiltradas) {
      const g = this.geoBarra[k], nrm = g.ejes[eje];
      let ant = null;
      for (let s = 0; s <= n; s++) {
        const t = s / n, x = t * g.L;
        const v = this._valor(comp, k, x) * factor;
        const p = [0, 1, 2].map(c => g.pi[c] + t * (g.pj[c] - g.pi[c]));
        const d = [0, 1, 2].map(c => p[c] + v * nrm[c]);
        if (s === 0 || s === n) pts.push(...p, ...d);   // la costilla de extremo
        if (ant) pts.push(...ant, ...d);                // el contorno
        ant = d;
      }
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(pts), 3));
    this.gDiag.add(new THREE.LineSegments(
      geo, new THREE.LineBasicMaterial({ color: PALETA.tinta })));
  }

  _deformar(fase) {
    if (!this.campo) return;
    const f = this.factor * fase, b = this.base, c = this.campo, d = this.def;
    for (let k = 0; k < d.length; k++) d[k] = b[k] + f * c[k];
    this.attrDef.needsUpdate = true;
    this.lineasDef.geometry.computeBoundingSphere();
  }

  _animar(si) {
    this.animando = si;
    this.btnAnim.setAttribute('aria-pressed', String(si));
    if (si) {
      const t0 = performance.now();
      this.renderer.setAnimationLoop(t => {
        const w = 2 * Math.PI * ((t - t0) / 1000) / PERIODO_ANIM;
        this._deformar(this.selModo.value ? Math.sin(w) : (1 - Math.cos(w)) / 2);
        this.renderer.render(this.scene, this.camera);
      });
    } else {
      this.renderer.setAnimationLoop(null);
      this._deformar(1);
      this._render();
    }
  }

  _render() {
    if (this.renderer && !this.animando) this.renderer.render(this.scene, this.camera);
  }

  // ------------------------------------------------------------ tooltip
  _hover(e) {
    const rect = this.renderer.domElement.getBoundingClientRect();
    const p = new THREE.Vector2((e.clientX - rect.left) / rect.width * 2 - 1,
      -((e.clientY - rect.top) / rect.height) * 2 + 1);
    this.raycaster.setFromCamera(p, this.camera);
    let texto = null;
    const hp = this.raycaster.intersectObject(this.puntos, false);
    if (hp.length) texto = this._textoNudo(hp[0].index);
    else if (this.comp) {
      // Con el color puesto se apuntan las barras subdivididas: el índice de
      // vértice dice qué barra, y el punto del impacto, en qué estación.
      const hl = this.raycaster.intersectObject(this.lineasCol, false);
      if (hl.length) {
        const k = Math.floor(hl[0].index / (2 * NSUB_COLOR));
        texto = this._textoBarra(k, hl[0].point);
      }
    } else {
      const hl = this.raycaster.intersectObject(this.lineasBase, false);
      if (hl.length) texto = this._textoBarra(Math.floor(hl[0].index / 2));
    }
    if (!texto) { this.tip.style.display = 'none'; return; }
    this.tip.textContent = texto;
    this.tip.style.display = 'block';
    const x = e.clientX - rect.left + 14, y = e.clientY - rect.top + 14;
    this.tip.style.left = Math.min(x, rect.width - this.tip.offsetWidth - 6) + 'px';
    this.tip.style.top = Math.min(y, rect.height - this.tip.offsetHeight - 6) + 'px';
  }

  _resultado() {
    if (!this.selCaso.value) return null;
    const tipo = this.selCaso.value.slice(0, 1), nombre = this.selCaso.value.slice(2);
    return { nombre, r: tipo === 'c' ? this.esc.casos[nombre] : this.esc.combinaciones[nombre] };
  }

  _textoNudo(k) {
    const n = this.esc.nudos[k];
    let s = `nudo ${n.nombre || n.id}  (${n.xyz.map(v => num(v, 2)).join(', ')}) m`;
    if (n.fijo) s += `\napoyo ${n.fijo.join('')}`;
    const res = this._resultado();
    if (res) {
      const u = res.r.u[k];
      s += `\n${res.nombre}: u = (${u.slice(0, 3).map(sci).join(', ')}) m`;
      if (res.r.reacciones[String(n.id)]) {
        const R = res.r.reacciones[String(n.id)];
        s += `\nR = (${R.slice(0, 3).map(sci).join(', ')}) kN`;
      }
    } else if (this.selModo.value) {
      const m = this.esc.modos.find(x => String(x.n) === this.selModo.value);
      s += `\nφ = (${m.phi[k].map(v => num(v, 3)).join(', ')})`;
    }
    return s;
  }

  _textoBarra(k, punto) {
    const b = this.esc.barras[k];
    const ni = this.esc.nudos[this.idx.get(b.i)], nj = this.esc.nudos[this.idx.get(b.j)];
    const g = this.geoBarra[k];
    let s = `barra ${b.nombre || b.id}  ${b.seccion}\n${ni.nombre || ni.id} → ${nj.nombre || nj.id}` +
            `   L = ${num(g.L, 3)} m`;
    const res = this._resultado();
    if (res) {
      const f = res.r.fuerzas[k];
      s += `\n${res.nombre}:  N      Vy     Vz     T      My     Mz`;
      s += `\n  i: ${f.slice(0, 6).map(v => sci(v).padStart(7)).join('')}`;
      s += `\n  j: ${f.slice(6, 12).map(v => sci(v).padStart(7)).join('')}`;
      s += `\n  (kN, kN·m; signo del diagrama)`;
      if (this.comp && punto) {
        // La estación bajo el cursor: la proyección del impacto sobre el eje.
        const ex = g.ejes[0];
        const d = [punto.x - g.pi[0], punto.y - g.pi[1], punto.z - g.pi[2]];
        const x = Math.max(0, Math.min(g.L, d[0] * ex[0] + d[1] * ex[1] + d[2] * ex[2]));
        s += `\n  ${this.comp}(x = ${num(x, 3)} m; x/L = ${num(x / g.L, 2)}) = ` +
             `${sci(this._valor(this.comp, k, x))} ${unidadDe(this.comp)}`;
      }
    }
    return s;
  }
}

function el(tag, clase) { const e = document.createElement(tag); if (clase) e.className = clase; return e; }

if (!customElements.get('rukan-visor')) customElements.define('rukan-visor', RukanVisor);
