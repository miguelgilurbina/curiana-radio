#!/usr/bin/env node
/**
 * JAI Sounds · auditoría de playlists publicadas
 * ---------------------------------------------------------------------
 * Responde a "¿qué falta para que esto se pueda mostrar?": qué playlists
 * públicas tienen descripción, cuáles tienen portada propia y cuáles
 * siguen con el mosaico automático que arma Spotify con las carátulas.
 *
 * Solo lee. No modifica nada en la cuenta.
 *
 *   node jai-sounds/scripts/auditar_playlists.mjs
 *   node jai-sounds/scripts/auditar_playlists.mjs --json salida.json
 *   node jai-sounds/scripts/auditar_playlists.mjs --todas   (incl. privadas)
 */

import fs from "node:fs";
import { ErrorDeConfig, haySesion, tokenDeUsuario } from "./spotify_auth.mjs";

const API = "https://api.spotify.com/v1";

/**
 * Spotify sirve el mosaico automático desde mosaic.scdn.co; una portada
 * subida a mano vive en i.scdn.co. Es la señal más fiable para saber si
 * una lista tiene arte propio sin mirarlas una por una.
 */
function claseDePortada(url) {
  if (!url) return "sin-imagen";
  if (url.includes("mosaic.scdn.co")) return "mosaico";
  return "propia";
}

async function api(ruta, token, intento = 0) {
  const res = await fetch(ruta.startsWith("http") ? ruta : `${API}${ruta}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  // Spotify devuelve 429 con QUOTA_EXCEEDED cuando se acumulan peticiones
  // (por ejemplo si una ingesta larga corre en paralelo). El Retry-After
  // puede ser de minutos: se respeta en vez de reintentar a ciegas.
  if (res.status === 429) {
    const espera = Number(res.headers.get("Retry-After") ?? 5) + 1;
    if (intento >= 4) {
      throw new ErrorDeConfig(
        `Cuota de Spotify agotada y no se recupera tras ${intento} esperas.\n` +
          "  Dejar de hacer peticiones un rato y reintentar. Si hay una ingesta\n" +
          "  corriendo en paralelo, esperar a que termine."
      );
    }
    console.error(`  · 429 — esperando ${espera}s`);
    await new Promise((r) => setTimeout(r, espera * 1000));
    return api(ruta, token, intento + 1);
  }

  if (!res.ok) {
    throw new Error(`Spotify ${res.status} en ${ruta}: ${await res.text()}`);
  }
  return res.json();
}

async function main() {
  if (!haySesion()) {
    throw new ErrorDeConfig(
      "No hay sesión de Spotify.\n" +
        "  Correr primero: node jai-sounds/scripts/ingest_spotify.mjs --login"
    );
  }
  const argv = process.argv.slice(2);
  const incluirPrivadas = argv.includes("--todas");
  const iJson = argv.indexOf("--json");
  const rutaJson = iJson >= 0 ? argv[iJson + 1] : null;

  const token = await tokenDeUsuario();
  const yo = await api("/me", token);

  const listas = [];
  let url = `${API}/me/playlists?limit=50`;
  while (url) {
    const p = await api(url, token);
    listas.push(...p.items.filter(Boolean));
    url = p.next;
  }

  const mias = listas
    .filter((p) => p.owner?.id === yo.id)
    .filter((p) => incluirPrivadas || p.public)
    .map((p) => ({
      id: p.id,
      nombre: p.name.trim(),
      publica: Boolean(p.public),
      pistas: p.items?.total ?? p.tracks?.total ?? null,
      descripcion: (p.description ?? "").trim(),
      portada: claseDePortada(p.images?.[0]?.url),
      imagen_url: p.images?.[0]?.url ?? null,
    }))
    .sort((a, b) => (b.pistas ?? 0) - (a.pistas ?? 0));

  const sinDesc = mias.filter((p) => !p.descripcion);
  const sinPortada = mias.filter((p) => p.portada !== "propia");
  const listas_ok = mias.filter((p) => p.descripcion && p.portada === "propia");

  console.log(
    `\n${mias.length} playlists ${incluirPrivadas ? "" : "públicas "}de ${yo.display_name}\n`
  );
  console.log("  D = tiene descripción    P = portada propia\n");
  for (const p of mias) {
    const d = p.descripcion ? "D" : "·";
    const pr = p.portada === "propia" ? "P" : p.portada === "mosaico" ? "·" : "!";
    console.log(
      `  ${d}${pr}  ${String(p.pistas ?? "?").padStart(4)}  ${p.nombre}`
    );
    if (p.descripcion) console.log(`         "${p.descripcion}"`);
  }

  console.log(`\n── Resumen ──`);
  console.log(`  listas para mostrar (D+P): ${listas_ok.length}`);
  console.log(`  sin descripción:           ${sinDesc.length}`);
  console.log(`  sin portada propia:        ${sinPortada.length}`);
  if (sinPortada.length) {
    console.log(`\n  Falta portada en:`);
    for (const p of sinPortada) console.log(`    · ${p.nombre}`);
  }

  if (rutaJson) {
    fs.writeFileSync(rutaJson, JSON.stringify(mias, null, 2) + "\n");
    console.log(`\n· JSON en ${rutaJson}`);
  }
  console.log();
}

main().catch((e) => {
  console.error(`\n✗ ${e instanceof ErrorDeConfig ? e.message : e.stack}\n`);
  process.exit(1);
});
