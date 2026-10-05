import test from "node:test";
import assert from "node:assert/strict";
import { armar } from "./exportar.mjs";

const dial = [
  { slug: "sound-gods", nombre: "Sound Gods", spotify_id: "P1", portada: "/jai/portadas/sound-gods.webp" },
  { slug: "el-pozo", nombre: "El Pozo", spotify_id: "P2", portada: null },
];
const tablas = () => ({
  playlist_tracks: [
    { playlist_id: "P1", track_id: "T1", position: 0, added_at: "2023-09-17T10:00:00Z" },
    { playlist_id: "P1", track_id: "T2", position: 1, added_at: null },
    { playlist_id: "P2", track_id: "T2", position: 0, added_at: "2024-01-01T00:00:00Z" },
  ],
  tracks: [
    { id: "T1", name: "The Sound of Silence", slug: "the-sound-of-silence-simon-y-garfunkel", album_id: "AL1", track_number: 1, duration_ms: 185000, spotify_url: null },
    { id: "T2", name: "Goodnight Jade", slug: "goodnight-jade-squarepusher", album_id: "AL2", track_number: 4, duration_ms: 300000, spotify_url: "https://open.spotify.com/track/T2" },
  ],
  track_artists: [
    { track_id: "T1", artist_id: "A1", position: 0 },
    { track_id: "T2", artist_id: "A2", position: 0 },
  ],
  albums: [
    { id: "AL1", name: "Bookends", slug: "bookends", album_type: "album", release_date: "1968", image_url: "img1" },
    { id: "AL2", name: "Hard Normal Daddy", slug: "hard-normal-daddy", album_type: "album", release_date: "1997", image_url: "img2" },
  ],
  album_artists: [
    { album_id: "AL1", artist_id: "A1", position: 0 },
    { album_id: "AL2", artist_id: "A2", position: 0 },
  ],
  artists: [
    { id: "A1", name: "Simon & Garfunkel", slug: "simon-y-garfunkel", mbid: "mb-sg" },
    { id: "A2", name: "Squarepusher", slug: "squarepusher", mbid: "mb-sq" },
  ],
  mb_recordings: [
    { track_id: "T1", mbid: "r1", via: "isrc", primera_edicion: "1966-01-17", generos: ["folk rock"], tags: [], creditos: [{ rol: "producer", atributos: [], nombre: "Tom Wilson", mbid: "mb-tw" }, { rol: "vocal", atributos: [], nombre: "Simon & Garfunkel", mbid: "mb-sg" }], obras: [], ediciones: [] },
    { track_id: "T2", mbid: null, primera_edicion: null, generos: [], tags: [], creditos: [], obras: [], ediciones: [] },
  ],
  mb_artists: [{ mbid: "mb-sg", tipo: "Group", pais: "US", area: null, origen: null, inicio: "1963", fin: null, desambiguacion: null, generos: ["folk"], tags: [], miembros: [], integrante_de: [], wikipedia: null, wikidata: "https://www.wikidata.org/wiki/Q484918", discogs: null, bandcamp: null, web: null }],
  internet: [{ entidad: "artista", entidad_id: "A1", titulo: "Simon and Garfunkel", extracto: "Dúo de folk rock.", url: "https://es.wikipedia.org/wiki/Simon_and_Garfunkel", idioma: "es", licencia: "CC BY-SA 4.0" }],
  resenas: [
    { entidad: "cancion", entidad_id: "T1", cuerpo: "Publicada.", estado: "publicada", publicada_en: "2026-10-05" },
    { entidad: "cancion", entidad_id: "T2", cuerpo: "Borrador secreto.", estado: "borrador", publicada_en: null },
  ],
});

test("un borrador nunca sale en el export", () => {
  const w = armar(dial, tablas());
  assert.equal(w.canciones["the-sound-of-silence-simon-y-garfunkel"].resena.cuerpo, "Publicada.");
  assert.equal(w.canciones["goodnight-jade-squarepusher"].resena, undefined);
  assert.ok(!JSON.stringify(w).includes("Borrador secreto"));
});

test("distingue «MusicBrainz no la tiene» de «no se consultó»", () => {
  const t = tablas();
  assert.equal(armar(dial, t).canciones["goodnight-jade-squarepusher"].mb, null);
  t.mb_recordings = t.mb_recordings.filter((m) => m.track_id !== "T2");
  assert.equal(armar(dial, t).canciones["goodnight-jade-squarepusher"].mb, undefined);
});

test("el crédito enlaza al artista solo si está en el dial", () => {
  const cr = armar(dial, tablas()).canciones["the-sound-of-silence-simon-y-garfunkel"].mb.cr;
  assert.deepEqual(cr.map((c) => [c.n, c.a]), [["Tom Wilson", null], ["Simon & Garfunkel", "simon-y-garfunkel"]]);
});

test("cada canción sabe en qué estaciones suena, en qué puesto y desde cuándo", () => {
  const w = armar(dial, tablas());
  assert.deepEqual(w.canciones["goodnight-jade-squarepusher"].dial, [[0, 2, null], [1, 1, "2024-01-01"]]);
  assert.deepEqual(w.estaciones[0].pistas, ["the-sound-of-silence-simon-y-garfunkel", "goodnight-jade-squarepusher"]);
});

test("una coincidencia por título no le cambia el año al censo", () => {
  const t = tablas();
  t.mb_recordings[0].via = "busqueda";
  assert.equal(armar(dial, t).estaciones[0].censo.desde, 1968); // el de Spotify
});

test("el censo usa la primera edición de MusicBrainz cuando la hay", () => {
  const c = armar(dial, tablas()).estaciones[0].censo;
  assert.equal(c.desde, 1966); // no 1968, que es lo que dice Spotify
  assert.equal(c.hasta, 1997);
  assert.equal(c.artistas, 2);
  assert.equal(c.ms, 485000);
});

test("«suena cerca de» premia al que suena al lado, no al alfabeto", () => {
  const t = tablas();
  // Cuatro pistas en P1: Simon & Garfunkel, Squarepusher, (Aphex), (Zappa)
  t.tracks.push(
    { id: "T3", name: "Avril 14th", slug: "avril-14th-aphex-twin", album_id: "AL2", track_number: 1, duration_ms: 1, spotify_url: null },
    { id: "T4", name: "Peaches en Regalia", slug: "peaches-en-regalia-frank-zappa", album_id: "AL2", track_number: 2, duration_ms: 1, spotify_url: null }
  );
  t.artists.push({ id: "A3", name: "Aphex Twin", slug: "aphex-twin", mbid: null }, { id: "A4", name: "Frank Zappa", slug: "frank-zappa", mbid: null });
  t.track_artists.push({ track_id: "T3", artist_id: "A3", position: 0 }, { track_id: "T4", artist_id: "A4", position: 0 });
  t.playlist_tracks = [
    { playlist_id: "P1", track_id: "T4", position: 0, added_at: null }, // Zappa, al lado de S&G
    { playlist_id: "P1", track_id: "T1", position: 1, added_at: null }, // Simon & Garfunkel
    { playlist_id: "P1", track_id: "T2", position: 2, added_at: null },
    { playlist_id: "P1", track_id: "T3", position: 3, added_at: null }, // Aphex, a dos puestos
  ];
  const cerca = armar(dial, t).artistas["simon-y-garfunkel"].cerca.map(([a]) => a);
  assert.equal(cerca[0] === "frank-zappa" || cerca[0] === "squarepusher", true);
  assert.ok(cerca.indexOf("aphex-twin") > cerca.indexOf("frank-zappa"), "Aphex (a 2 puestos) va después de Zappa (al lado), aunque la «a» va antes que la «f»");
});

test("artistas con su ficha, sus voces y quién suena cerca", () => {
  const a = armar(dial, tablas()).artistas;
  assert.equal(a["simon-y-garfunkel"].mb.pais, "US");
  assert.equal(a["simon-y-garfunkel"].internet.titulo, "Simon and Garfunkel");
  assert.equal(a.squarepusher.mb, null);
  assert.deepEqual(a["simon-y-garfunkel"].cerca, [["squarepusher", 0]]);
});
