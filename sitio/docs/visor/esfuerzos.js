/*
 * esfuerzos.js — los seis esfuerzos a lo largo de la barra, para el visor.
 *
 * Gemelo de `src/rukan/esfuerzos.py`. La fórmula vive en dos lenguajes porque
 * Python la evalúa para las sondas del proyecto y JavaScript para dibujar, y
 * `tests/test_esfuerzos_js.py` corre este módulo en `node` y compara las dos
 * implementaciones número a número sobre entradas aleatorias. Por eso este
 * archivo **no importa nada** —tampoco three.js—: tiene que poder cargarse
 * fuera del navegador.
 *
 * La fórmula. La entrada son los seis esfuerzos del **diagrama en el extremo
 * i** —las seis primeras de `casos.<c>.fuerzas[k]` de una `rukan/escena@2`— y
 * `w = [wx, wy, wz]`, la carga de vano en ejes locales (`casos.<c>.w[k]`, o
 * `null` si el caso no la tiene):
 *
 *     N(x)  = N_i − wx·x            Mz(x) = Mz_i + Vy_i·x − wy·x²/2
 *     Vy(x) = Vy_i − wy·x           My(x) = My_i − Vz_i·x + wz·x²/2
 *     Vz(x) = Vz_i − wz·x
 *     T(x)  = T_i
 *
 * No son una elección: salen del equilibrio del cuerpo libre [0, x] y son las
 * únicas que valen, en x = 0 y x = L, los valores de extremo que la escena
 * publica. La asimetría entre Mz y My —el `+Vy_i·x` contra el `−Vz_i·x`— es
 * real: los ejes son dextrógiros, ex × ey = ez pero ex × ez = −ey.
 *
 * De ahí caen dMz/dx = +Vy y dMy/dx = −Vz, que son las que fijan el signo del
 * corte. La **torsión** es el único componente sin diagrama del cual derivarse
 * y sigue esperando el contraste contra SAP2000: ver `lab/nota07`.
 *
 * Vale para carga de vano **uniforme**, que es la única que el modelo usa.
 */

export const COMPONENTES = ['N', 'Vy', 'Vz', 'T', 'My', 'Mz'];

// Tolerancia relativa con la que se acepta una estación en el borde: `x = L`
// calculado como k·L/n puede caer un ulp afuera.
const TOL = 1e-9;

export function esfuerzo(extremoI, w, L, componente, x) {
  if (!COMPONENTES.includes(componente)) {
    throw new Error(`componente ${componente}: vale ${COMPONENTES.join(' | ')}`);
  }
  if (x < -TOL * L || x > L * (1 + TOL)) {
    throw new Error(`la estación x = ${x} cae fuera de la barra (0 a ${L})`);
  }
  const [wx, wy, wz] = w == null ? [0, 0, 0] : w;
  const [Ni, Vyi, Vzi, Ti, Myi, Mzi] = extremoI;
  switch (componente) {
    case 'N':  return Ni - wx * x;
    case 'Vy': return Vyi - wy * x;
    case 'Vz': return Vzi - wz * x;
    case 'T':  return Ti;
    case 'My': return Myi - Vzi * x + wz * x * x / 2;
    default:   return Mzi + Vyi * x - wy * x * x / 2;
  }
}

/** Las `n` estaciones equiespaciadas de extremo a extremo, con n ≥ 2. */
export function estaciones(L, n) {
  if (n < 2) throw new Error(`un diagrama necesita al menos dos estaciones, no ${n}`);
  const xs = [];
  for (let k = 0; k < n; k++) xs.push(k * L / (n - 1));
  return xs;
}

/** Los seis componentes en `n` estaciones: una fila por estación. */
export function diagrama(extremoI, w, L, n) {
  return estaciones(L, n).map(
    x => COMPONENTES.map(c => esfuerzo(extremoI, w, L, c, x)));
}

/*
 * Ejes locales de la barra — el port de `loads.local_axes`, que es la misma
 * convención de `geomTransf Linear` de OpenSees:
 *
 *     ex = û(pj − pi)      ey = û(vecxz × ex)      ez = ex × ey
 *
 * El visor los necesita para dibujar el diagrama normal al eje: la ordenada de
 * Mz, Vy, N y T va sobre `ey`, y la de My y Vz sobre `ez`.
 */
export function ejesLocales(pi, pj, vecxz) {
  const ex = unit(sub(pj, pi));
  const ey = unit(cross(vecxz, ex));
  const ez = cross(ex, ey);
  return [ex, ey, ez];
}

function sub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
function cross(a, b) {
  return [a[1] * b[2] - a[2] * b[1],
          a[2] * b[0] - a[0] * b[2],
          a[0] * b[1] - a[1] * b[0]];
}
function unit(a) {
  const n = Math.sqrt(dot(a, a));
  return [a[0] / n, a[1] / n, a[2] / n];
}
