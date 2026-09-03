// El isotipo de Curiana Radio, en bulto. La espiral 3D no es una curva
// paramétrica: es un CALCO del PNG original. Se rasteriza a una rejilla, se
// binariza, y marching squares saca los contornos con todas las
// imperfecciones del dibujo a mano. El lazo de mayor área es el disco; los
// demás son agujeros (el canal espiral en negativo). Ver BRAND_MVP.md §8.
//
// Corre en el navegador (createImageBitmap + canvas 2D) una sola vez: la
// geometría queda cacheada a nivel de módulo por si la intro se remonta.

import { ExtrudeGeometry, Path, Shape, Vector2, Vector3 } from "three";

export const REJILLA = 180; // resolución del calco (px de lado)
const MIN_PUNTOS_LAZO = 24; // lazos más cortos son ruido del rasterizado
const MIN_AREA = 0.001; // en unidades normalizadas (~1 = ancho de la imagen)

/** Extrusión canónica del isotipo (handoff §1.3). */
export const EXTRUSION = {
  depth: 0.09,
  steps: 1,
  curveSegments: 8,
  bevelEnabled: true,
  bevelThickness: 0.012,
  bevelSize: 0.01,
  bevelSegments: 3,
} as const;

type Punto = [number, number];

/** Rasteriza el PNG a S×S y devuelve la máscara binaria: 1 = tinta. */
async function rasterizar(url: string, S: number): Promise<Uint8Array> {
  // createImageBitmap y no img.decode(): decode() puede colgarse en algunos
  // navegadores con PNG grandes.
  const respuesta = await fetch(url);
  if (!respuesta.ok) {
    throw new Error(`No se pudo cargar el isotipo ${url} (${respuesta.status})`);
  }
  const bmp = await createImageBitmap(await respuesta.blob());
  const cv = document.createElement("canvas");
  cv.width = cv.height = S;
  const c2 = cv.getContext("2d", { willReadFrequently: true });
  if (!c2) throw new Error("Sin contexto 2D para calcar el isotipo");
  c2.drawImage(bmp, 0, 0, S, S);
  bmp.close();
  const px = c2.getImageData(0, 0, S, S).data;
  const mascara = new Uint8Array(S * S);
  for (let i = 0; i < S * S; i++) {
    const o = i * 4;
    // pixel sólido = opaco y oscuro (el PNG es tinta negra sobre transparente)
    mascara[i] = px[o + 3] > 120 && px[o] + px[o + 1] + px[o + 2] < 400 ? 1 : 0;
  }
  return mascara;
}

/** Marching squares → lazos cerrados de puntos en coordenadas de rejilla. */
function contornos(mascara: Uint8Array, S: number): Punto[][] {
  const solido = (x: number, y: number) =>
    x < 0 || y < 0 || x >= S || y >= S ? 0 : mascara[y * S + x];

  // Cada punto de borde cae en medio de una arista de la rejilla: con ids
  // enteros precomputados, encadenar es lineal (Map) y no cuadrático.
  const W2 = (S + 3) * 2;
  const pid = (p: Punto) => Math.round(p[0] * 2 + 2) * W2 + Math.round(p[1] * 2 + 2);

  type Seg = { a: Punto; b: Punto; ia: number; ib: number; usado: boolean };
  const segs: Seg[] = [];
  for (let y = -1; y < S; y++) {
    for (let x = -1; x < S; x++) {
      const tl = solido(x, y);
      const tr = solido(x + 1, y);
      const br = solido(x + 1, y + 1);
      const bl = solido(x, y + 1);
      const cs = tl * 8 + tr * 4 + br * 2 + bl;
      if (cs === 0 || cs === 15) continue;
      const T: Punto = [x + 0.5, y];
      const R: Punto = [x + 1, y + 0.5];
      const B: Punto = [x + 0.5, y + 1];
      const L: Punto = [x, y + 0.5];
      const put = (a: Punto, b: Punto) =>
        segs.push({ a, b, ia: pid(a), ib: pid(b), usado: false });
      if (cs === 1 || cs === 14) put(L, B);
      else if (cs === 2 || cs === 13) put(B, R);
      else if (cs === 3 || cs === 12) put(L, R);
      else if (cs === 4 || cs === 11) put(T, R);
      else if (cs === 6 || cs === 9) put(T, B);
      else if (cs === 7 || cs === 8) put(L, T);
      else if (cs === 5) {
        put(L, T);
        put(B, R);
      } else {
        // cs === 10
        put(T, R);
        put(L, B);
      }
    }
  }

  const adj = new Map<number, number[]>();
  segs.forEach((s, i) => {
    for (const k of [s.ia, s.ib]) {
      let l = adj.get(k);
      if (!l) adj.set(k, (l = []));
      l.push(i);
    }
  });

  const lazos: Punto[][] = [];
  for (let i = 0; i < segs.length; i++) {
    if (segs[i].usado) continue;
    segs[i].usado = true;
    const lazo: Punto[] = [segs[i].a, segs[i].b];
    let cur = segs[i].ib;
    for (;;) {
      const cand = (adj.get(cur) ?? []).find((j) => !segs[j].usado);
      if (cand === undefined) break;
      const sg = segs[cand];
      sg.usado = true;
      if (sg.ia === cur) {
        lazo.push(sg.b);
        cur = sg.ib;
      } else {
        lazo.push(sg.a);
        cur = sg.ia;
      }
    }
    if (lazo.length > MIN_PUNTOS_LAZO) lazos.push(lazo);
  }
  return lazos;
}

/** Suaviza (2 pasadas 1-2-1), submuestrea 1 de cada 2 y normaliza a ~1 unidad, y arriba. */
function aPuntos(lazo: Punto[], S: number): Vector2[] {
  let p = lazo;
  for (let pasada = 0; pasada < 2; pasada++) {
    const prev = p;
    p = prev.map((q, i) => {
      const a = prev[(i - 1 + prev.length) % prev.length];
      const b = prev[(i + 1) % prev.length];
      return [(a[0] + q[0] * 2 + b[0]) / 4, (a[1] + q[1] * 2 + b[1]) / 4];
    });
  }
  return p
    .filter((_, i) => i % 2 === 0)
    .map((q) => new Vector2((q[0] - S / 2) / S, (S / 2 - q[1]) / S));
}

function area(pts: Vector2[]): number {
  let s = 0;
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i];
    const q = pts[(i + 1) % pts.length];
    s += p.x * q.y - q.x * p.y;
  }
  return Math.abs(s / 2);
}

/** La silueta del isotipo como Shape: el disco ovalado + el canal espiral (agujeros). */
export async function calcarEspiral(url: string, S = REJILLA): Promise<Shape> {
  const mascara = await rasterizar(url, S);
  const formas = contornos(mascara, S)
    .map((l) => aPuntos(l, S))
    .filter((p) => area(p) > MIN_AREA)
    .sort((a, b) => area(b) - area(a));
  if (formas.length === 0) throw new Error("El calco no encontró ningún contorno");
  const shape = new Shape(formas[0]);
  for (const h of formas.slice(1)) shape.holes.push(new Path(h));
  return shape;
}

/** Extruye la silueta con los parámetros canónicos y la centra en el origen. */
export function extruirEspiral(shape: Shape): ExtrudeGeometry {
  const geo = new ExtrudeGeometry(shape, EXTRUSION);
  geo.translate(0, 0, -EXTRUSION.depth / 2);
  geo.computeBoundingBox();
  const bb = geo.boundingBox;
  if (bb) {
    const c = bb.getCenter(new Vector3());
    geo.translate(-c.x, -c.y, -c.z);
  }
  return geo;
}

const cache = new Map<string, Promise<ExtrudeGeometry>>();

/** Geometría del isotipo, calcada una vez por URL y cacheada. Los consumidores
 *  NO deben disponerla: three la vuelve a subir a la GPU si hace falta. */
export function geometriaEspiral(url: string): Promise<ExtrudeGeometry> {
  let p = cache.get(url);
  if (!p) {
    p = calcarEspiral(url).then(extruirEspiral);
    p.catch(() => cache.delete(url)); // un fallo (red, sin PNG) no se queda pegado
    cache.set(url, p);
  }
  return p;
}
