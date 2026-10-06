import test from "node:test";
import assert from "node:assert/strict";
import {
  candidatasBusqueda,
  filaArtista,
  filaGrabacion,
  filaNoEncontrada,
  grupoDelAlbum,
  mejorGrabacion,
  puenteArtistas,
  rutaBusqueda,
} from "./musicbrainz.mjs";

test("entre grabaciones con el mismo ISRC elige la del mismo artista", () => {
  const recs = [
    { id: "cover", "artist-credit": [{ name: "Una Banda de Covers" }] },
    { id: "original", "artist-credit": [{ name: "Simon & Garfunkel" }] },
  ];
  assert.equal(mejorGrabacion(recs, "Simon & Garfunkel").id, "original");
  assert.equal(mejorGrabacion([], "x"), null);
});

test("la búsqueda de respaldo descarta puntajes bajos y duraciones lejanas", () => {
  const recs = [
    { id: "a", score: 100, length: 185000 },
    { id: "b", score: 80, length: 185000 },
    { id: "c", score: 100, length: 240000 },
  ];
  assert.deepEqual(candidatasBusqueda(recs, 186000).map((r) => r.id), ["a"]);
});

test("la ruta de búsqueda escapa Lucene y quita el sufijo «- Remastered»", () => {
  const r = decodeURIComponent(rutaBusqueda("Helicopter - Remastered 2015", "Bloc Party"));
  assert.match(r, /recording:"Helicopter" AND artist:"Bloc Party"/);
  assert.match(decodeURIComponent(rutaBusqueda("What?", "AC/DC")), /What\\\?.*AC\\\/DC/);
});

test("la fila de grabación ordena géneros por votos y ediciones por fecha", () => {
  const det = {
    id: "rec-1",
    "first-release-date": "1966-01-17",
    genres: [{ name: "folk", count: 2 }, { name: "folk rock", count: 9 }],
    tags: [],
    relations: [
      { "target-type": "artist", type: "producer", attributes: [], artist: { name: "Tom Wilson", id: "tw" } },
      { "target-type": "work", type: "performance", work: { title: "The Sound of Silence", id: "w1" } },
    ],
    releases: [
      { "release-group": { id: "g2", title: "Greatest Hits", "primary-type": "Album", "secondary-types": ["Compilation"], "first-release-date": "1972" } },
      { "release-group": { id: "g1", title: "Sounds of Silence", "primary-type": "Album", "first-release-date": "1966-01-17" } },
      { "release-group": { id: "g1", title: "Sounds of Silence" } },
    ],
  };
  const f = filaGrabacion("t1", det, "isrc");
  assert.equal(f.primera_edicion, "1966-01-17");
  assert.deepEqual(f.generos, ["folk rock", "folk"]);
  assert.deepEqual(f.creditos, [{ rol: "producer", atributos: [], nombre: "Tom Wilson", mbid: "tw" }]);
  assert.deepEqual(f.obras, [{ titulo: "The Sound of Silence", mbid: "w1" }]);
  assert.deepEqual(f.ediciones.map((e) => e.id), ["g1", "g2"]);
});

test("la fila de no encontrada trae todas las columnas NOT NULL", () => {
  const f = filaNoEncontrada("t9");
  assert.equal(f.mbid, null);
  for (const c of ["generos", "tags", "creditos", "obras", "ediciones"]) assert.deepEqual(f[c], []);
});

test("el puente casa por nombre, luego por orden, y no adivina", () => {
  const spotify = [{ id: "s1", name: "Max Richter" }, { id: "s2", name: "Lorenz Dangel" }];
  assert.deepEqual(puenteArtistas(spotify, [{ id: "m2", name: "Lorenz Dangel" }, { id: "m1", name: "Max Richter" }]), { s1: "m1", s2: "m2" });
  assert.deepEqual(puenteArtistas(spotify, [{ id: "mx", name: "Otro" }, { id: "my", name: "Distinto" }]), { s1: "mx", s2: "my" });
  assert.deepEqual(puenteArtistas(spotify, [{ id: "mx", name: "Otro" }]), {});
});

test("la fila de artista separa miembros de grupos de los que fue parte", () => {
  const a = filaArtista({
    id: "a1", name: "Bloc Party", type: "Group", country: "GB", "life-span": { begin: "1999-08" },
    genres: [{ name: "indie rock", count: 3 }],
    relations: [
      { type: "member of band", direction: "backward", artist: { name: "Kele Okereke", id: "k" }, begin: "1999" },
      { type: "wikidata", url: { resource: "https://www.wikidata.org/wiki/Q7" } },
    ],
  });
  assert.equal(a.pais, "GB");
  assert.deepEqual(a.miembros, [{ nombre: "Kele Okereke", mbid: "k", desde: "1999", hasta: null }]);
  assert.deepEqual(a.integrante_de, []);
  assert.equal(a.wikidata, "https://www.wikidata.org/wiki/Q7");
});

test("el release group del álbum es el que se llama igual", () => {
  const ed = [{ id: "g1", titulo: "Silent Shout" }, { id: "g2", titulo: "Greatest Hits" }];
  assert.equal(grupoDelAlbum("Silent Shout (Deluxe Edition)", ed), "g1");
  assert.equal(grupoDelAlbum("Otro", ed), null);
});
