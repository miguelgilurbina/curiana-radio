import test from "node:test";
import assert from "node:assert/strict";
import { articuloDeWikidata, deUrlWikipedia, filaInternet, qid } from "./wikipedia.mjs";

test("saca el Q-id y el artículo de las URLs", () => {
  assert.equal(qid("https://www.wikidata.org/wiki/Q484918"), "Q484918");
  assert.equal(qid(null), null);
  assert.deepEqual(deUrlWikipedia("https://en.wikipedia.org/wiki/Simon_%26_Garfunkel"), { idioma: "en", titulo: "Simon & Garfunkel" });
});

test("prefiere el artículo en español y cae al inglés", () => {
  const ambos = { sitelinks: { enwiki: { title: "Squarepusher" }, eswiki: { title: "Squarepusher (músico)" } } };
  assert.deepEqual(articuloDeWikidata(ambos), { idioma: "es", titulo: "Squarepusher (músico)" });
  assert.deepEqual(articuloDeWikidata({ sitelinks: { enwiki: { title: "SANAM" } } }), { idioma: "en", titulo: "SANAM" });
  assert.equal(articuloDeWikidata({ sitelinks: { dewiki: { title: "X" } } }), null);
});

test("una página de desambiguación o vacía no es voz del internet", () => {
  assert.equal(filaInternet("artista", "a", { type: "disambiguation", extract: "Puede referirse a…" }, "es"), null);
  assert.equal(filaInternet("artista", "a", { type: "standard", extract: "  " }, "es"), null);
});

test("la fila lleva fuente, licencia y enlace", () => {
  const f = filaInternet("artista", "sp1", { type: "standard", title: "Simon & Garfunkel", extract: "Dúo estadounidense de folk rock.", content_urls: { desktop: { page: "https://es.wikipedia.org/wiki/Simon_%26_Garfunkel" } } }, "es");
  assert.equal(f.fuente, "wikipedia");
  assert.equal(f.licencia, "CC BY-SA 4.0");
  assert.equal(f.url, "https://es.wikipedia.org/wiki/Simon_%26_Garfunkel");
  assert.equal(f.entidad_id, "sp1");
});
