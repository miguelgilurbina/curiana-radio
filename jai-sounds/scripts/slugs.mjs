#!/usr/bin/env node
/**
 * JAI Sounds · slugs del wiki
 * ---------------------------------------------------------------------
 * Le da URL a cada artista, álbum y canción que todavía no la tiene:
 *
 *   /jai-sounds/artistas/max-richter
 *   /jai-sounds/albumes/the-blue-notebooks-max-richter   (si el nombre choca)
 *   /jai-sounds/canciones/on-the-nature-of-daylight-max-richter
 *
 * Un slug se asigna UNA vez y no se recalcula: un enlace guardado tiene que
 * seguir llevando a la misma página aunque Spotify cambie el nombre.
 *
 * Uso:  node jai-sounds/scripts/slugs.mjs [--dry-run]
 */
import { conectar, esPrincipal, log, slugificar, todas, upsert } from "./_comun.mjs";

/**
 * Asigna slugs únicos a las filas sin slug. `ocupados` trae los que ya
 * existen en la tabla; `base(fila)` da la forma preferida y `alterna(fila)`
 * la que se prueba si la preferida está tomada. Si las dos chocan, número.
 */
export function asignar(filas, ocupados, base, alterna = () => null) {
  const tomados = new Set(ocupados);
  const nuevos = [];
  for (const f of filas) {
    let s = base(f);
    if (tomados.has(s)) s = alterna(f) ?? s;
    if (tomados.has(s)) {
      let n = 2;
      while (tomados.has(`${s}-${n}`)) n++;
      s = `${s}-${n}`;
    }
    tomados.add(s);
    nuevos.push({ ...f, slug: s });
  }
  return nuevos;
}

// Los alfabetos no latinos no se transliteran: se usa el id de Spotify, que
// es estable, en vez de inventar una lectura.
const o = (texto, id) => slugificar(texto) || id.toLowerCase();

export const reglas = {
  artista: { base: (a) => o(a.name, a.id) },
  album: {
    base: (a) => o(a.name, a.id),
    alterna: (a) => (a.artista ? `${o(a.name, a.id)}-${slugificar(a.artista) || "x"}` : null),
  },
  cancion: {
    base: (t) => `${o(t.name, t.id)}-${slugificar(t.artista) || "x"}`,
  },
};

async function main() {
  const seco = process.argv.includes("--dry-run");
  const db = conectar();

  const artistas = await todas(() => db.from("artists").select("id, name, slug").order("id"));
  const albumes = await todas(() =>
    db.from("albums").select("id, name, slug, album_artists(position, artists(name))").order("id")
  );
  const pistas = await todas(() =>
    db.from("tracks").select("id, name, slug, track_artists(position, artists(name))").order("id")
  );
  // El primer artista acreditado: el que da apellido a canción y álbum.
  const primero = (rel) => [...(rel ?? [])].sort((a, b) => a.position - b.position)[0]?.artists?.name ?? null;

  const lotes = [
    ["artists", artistas, reglas.artista, (a) => ({ id: a.id, name: a.name, slug: a.slug })],
    ["albums", albumes.map((a) => ({ id: a.id, name: a.name, slug: a.slug, artista: primero(a.album_artists) })), reglas.album, (a) => ({ id: a.id, name: a.name, slug: a.slug })],
    ["tracks", pistas.map((t) => ({ id: t.id, name: t.name, slug: t.slug, artista: primero(t.track_artists) })), reglas.cancion, (t) => ({ id: t.id, name: t.name, slug: t.slug })],
  ];

  for (const [tabla, filas, regla, fila] of lotes) {
    const sin = filas.filter((f) => !f.slug);
    const nuevos = asignar(sin, filas.filter((f) => f.slug).map((f) => f.slug), regla.base, regla.alterna);
    log(`▸ ${tabla}: ${filas.length} filas, ${sin.length} sin slug`);
    if (seco) {
      nuevos.slice(0, 5).forEach((n) => log(`    ${n.slug}`));
      continue;
    }
    await upsert(db, tabla, nuevos.map(fila), "id");
  }
  log(seco ? "\n[dry-run] nada escrito.\n" : "\n✓ slugs listos.\n");
}

if (esPrincipal(import.meta.url)) await main();
