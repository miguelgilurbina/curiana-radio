#!/usr/bin/env node
/**
 * JAI Sounds · «esto dice el internet»
 * ---------------------------------------------------------------------
 * La segunda voz de cada página del wiki: el primer párrafo de Wikipedia,
 * en español si existe y si no en inglés, siempre con su fuente, licencia y
 * enlace. Nunca se presenta como voz de JAI: esa es la reseña.
 *
 * El camino es MusicBrainz → Wikidata → Wikipedia:
 *   artista  mb_artists.wikidata (o su enlace directo a Wikipedia)
 *   álbum    el release group del álbum, por su url-rel de Wikidata
 *   canción  la obra (la composición), por su url-rel de Wikidata
 *
 * Correr DESPUÉS de musicbrainz.mjs. Cachés en ~/.cache/jai-sounds/.
 *
 * Uso:  node jai-sounds/scripts/wikipedia.mjs [--solo-artistas] [--dry-run]
 */
import { cacheEnDisco, conectar, esPrincipal, idsDelDial, log, todas, trozos, upsert } from "./_comun.mjs";
import { clienteMB } from "./musicbrainz.mjs";

const UA = "CurianaRadio-JAI/0.1 (https://curianaradio.com)";
const IDIOMAS = ["es", "en"];
const LICENCIA = "CC BY-SA 4.0";

/** Q-id de una URL de Wikidata. */
export function qid(url) {
  return url?.match(/wikidata\.org\/wiki\/(Q\d+)/)?.[1] ?? null;
}

/** Idioma y título de una URL de Wikipedia. */
export function deUrlWikipedia(url) {
  const m = url?.match(/^https?:\/\/([a-z-]+)\.wikipedia\.org\/wiki\/(.+)$/);
  return m ? { idioma: m[1], titulo: decodeURIComponent(m[2]).replace(/_/g, " ") } : null;
}

/** De la entidad de Wikidata, el primer artículo en los idiomas preferidos. */
export function articuloDeWikidata(entidad, idiomas = IDIOMAS) {
  for (const l of idiomas) {
    const t = entidad?.sitelinks?.[`${l}wiki`]?.title;
    if (t) return { idioma: l, titulo: t };
  }
  return null;
}

/** La fila de jai.internet, o null si el resumen no sirve (desambiguación, vacío). */
export function filaInternet(entidad, entidadId, resumen, idioma) {
  if (!resumen || resumen.type === "disambiguation" || !resumen.extract?.trim()) return null;
  return {
    entidad,
    entidad_id: entidadId,
    fuente: "wikipedia",
    idioma,
    titulo: resumen.title ?? null,
    extracto: resumen.extract.trim(),
    url: resumen.content_urls?.desktop?.page ?? `https://${idioma}.wikipedia.org/wiki/${encodeURIComponent(resumen.title)}`,
    licencia: LICENCIA,
    consultado_en: new Date().toISOString(),
  };
}

function clienteWeb(cache) {
  return async function get(url) {
    if (url in cache.datos) return cache.datos[url];
    for (let k = 0; k < 3; k++) {
      try {
        const r = await fetch(url, { headers: { "User-Agent": UA, Accept: "application/json" }, signal: AbortSignal.timeout(20000) });
        if (r.status === 429) {
          await new Promise((s) => setTimeout(s, 4000 * (k + 1)));
          continue;
        }
        const v = r.ok ? await r.json() : null;
        cache.datos[url] = v;
        cache.marcar();
        await new Promise((s) => setTimeout(s, 120));
        return v;
      } catch {
        await new Promise((s) => setTimeout(s, 2000));
      }
    }
    return null;
  };
}

async function main() {
  const seco = process.argv.includes("--dry-run");
  const soloArtistas = process.argv.includes("--solo-artistas");
  const db = conectar();
  const cacheWeb = cacheEnDisco("wikipedia.json");
  const cacheMB = cacheEnDisco("musicbrainz.json");
  const get = clienteWeb(cacheWeb);
  const mb = clienteMB(cacheMB);

  const resumen = async (art) =>
    art ? [await get(`https://${art.idioma}.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(art.titulo.replace(/ /g, "_"))}`), art.idioma] : [null, null];
  const articuloDeQ = async (q) => (q ? articuloDeWikidata((await get(`https://www.wikidata.org/wiki/Special:EntityData/${q}.json`))?.entities?.[q]) : null);
  const filas = [];

  // ── Artistas ──
  const artistas = await todas(() => db.from("artists").select("id, mbid").not("mbid", "is", null));
  const mbArt = new Map((await todas(() => db.from("mb_artists").select("mbid, wikidata, wikipedia"))).map((a) => [a.mbid, a]));
  log(`▸ artistas: ${artistas.length} con MusicBrainz`);
  for (const a of artistas) {
    const m = mbArt.get(a.mbid);
    if (!m) continue;
    const art = (await articuloDeQ(qid(m.wikidata))) ?? deUrlWikipedia(m.wikipedia);
    const f = filaInternet("artista", a.id, ...(await resumen(art)));
    if (f) filas.push(f);
  }
  log(`  con Wikipedia: ${filas.length}`);

  if (!soloArtistas) {
    // ── Álbumes: release group → Wikidata ──
    const albumes = await todas(() => db.from("albums").select("id, mb_release_group").not("mb_release_group", "is", null));
    log(`▸ álbumes: ${albumes.length} con release group`);
    const antes = filas.length;
    for (const al of albumes) {
      const g = await mb(`release-group/${al.mb_release_group}?inc=url-rels`);
      const q = qid((g?.relations ?? []).find((r) => r.type === "wikidata")?.url?.resource);
      const f = filaInternet("album", al.id, ...(await resumen(await articuloDeQ(q))));
      if (f) filas.push(f);
    }
    log(`  con Wikipedia: ${filas.length - antes}`);

    // ── Canciones: la obra → Wikidata ──
    const ids = await idsDelDial(db);
    const grabs = [];
    for (const lote of trozos(ids, 200)) {
      const { data, error } = await db.from("mb_recordings").select("track_id, obras").in("track_id", lote);
      if (error) throw error;
      grabs.push(...data.filter((g) => g.obras?.length));
    }
    log(`▸ canciones: ${grabs.length} con obra en MusicBrainz`);
    const antesC = filas.length;
    for (const g of grabs) {
      const w = await mb(`work/${g.obras[0].mbid}?inc=url-rels`);
      const q = qid((w?.relations ?? []).find((r) => r.type === "wikidata")?.url?.resource);
      const f = filaInternet("cancion", g.track_id, ...(await resumen(await articuloDeQ(q))));
      if (f) filas.push(f);
    }
    log(`  con Wikipedia: ${filas.length - antesC}`);
  }
  cacheWeb.guardar();
  cacheMB.guardar();

  if (seco) {
    log(`\n[dry-run] ${filas.length} extractos, nada escrito.\n`);
    return;
  }
  await upsert(db, "internet", filas, "entidad,entidad_id,fuente");
  log("\n✓ el internet, citado.\n");
}

if (esPrincipal(import.meta.url)) await main();
