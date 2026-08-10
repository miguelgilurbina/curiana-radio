/**
 * JAI Sounds · autenticación con Spotify
 * ---------------------------------------------------------------------
 * Dos flujos, para dos alcances distintos:
 *
 *   Client Credentials  → solo playlists PÚBLICAS por id. No hay usuario,
 *                         así que /me/* no existe.
 *   Authorization Code  → las playlists del usuario, incluidas privadas y
 *                         colaborativas, más /me/playlists y /me/tracks
 *                         (canciones guardadas).
 *
 * El segundo es el que hace falta aquí: 12.000 canciones repartidas en
 * decenas de listas no se enumeran a mano.
 *
 * El refresh_token se guarda FUERA del repo, en ~/.secrets/, porque el
 * proyecto vive dentro de OneDrive y cualquier archivo suyo se sincroniza
 * a la nube aunque esté gitignoreado.
 */

import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";

const CUENTAS = "https://accounts.spotify.com";

// Spotify prohíbe `localhost` como redirect URI desde abril de 2025: exige
// el literal de loopback. Usar localhost da INVALID_CLIENT y es el error
// más común al montar esto.
export const PUERTO_CALLBACK = 8888;
export const REDIRECT_URI = `http://127.0.0.1:${PUERTO_CALLBACK}/callback`;

const SCOPES = [
  "playlist-read-private",
  "playlist-read-collaborative",
  "user-library-read",
].join(" ");

export const TOKEN_PATH = path.join(
  os.homedir(),
  ".secrets",
  "jai-spotify-token.json"
);

/**
 * Falta de configuración, no fallo del programa: el usuario tiene algo que
 * hacer y un stack trace solo le estorba para leer qué.
 */
export class ErrorDeConfig extends Error {}

function credenciales() {
  const id = process.env.SPOTIFY_CLIENT_ID;
  const secret = process.env.SPOTIFY_CLIENT_SECRET;
  if (!id || !secret) {
    throw new ErrorDeConfig(
      "Faltan SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET en el entorno.\n" +
        "  Crear la app en https://developer.spotify.com/dashboard y exportarlas\n" +
        "  en la sesión del shell (NO en un archivo del repo — OneDrive sincroniza)."
    );
  }
  return { id, secret };
}

function basic() {
  const { id, secret } = credenciales();
  return Buffer.from(`${id}:${secret}`).toString("base64");
}

async function pedirToken(cuerpo) {
  const res = await fetch(`${CUENTAS}/api/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${basic()}`,
    },
    body: new URLSearchParams(cuerpo).toString(),
  });
  const json = await res.json();
  if (!res.ok) {
    throw new Error(
      `Spotify rechazó la petición de token (${res.status}): ${JSON.stringify(json)}`
    );
  }
  return json;
}

// ── Flujo de app (sin usuario) ───────────────────────────────────────

export async function tokenDeApp() {
  const { access_token } = await pedirToken({ grant_type: "client_credentials" });
  return access_token;
}

// ── Flujo de usuario ─────────────────────────────────────────────────

function guardarRefresh(refresh_token) {
  fs.mkdirSync(path.dirname(TOKEN_PATH), { recursive: true });
  fs.writeFileSync(
    TOKEN_PATH,
    JSON.stringify({ refresh_token, guardado: new Date().toISOString() }, null, 2),
    // Solo el dueño puede leerlo (en Windows es orientativo, pero no cuesta).
    { mode: 0o600 }
  );
}

export function haySesion() {
  return fs.existsSync(TOKEN_PATH);
}

/**
 * Abre el flujo de consentimiento y espera el callback en el loopback.
 * Devuelve cuando el refresh_token quedó guardado.
 */
export async function login() {
  const { id } = credenciales();
  const state = crypto.randomBytes(16).toString("hex");

  const url =
    `${CUENTAS}/authorize?` +
    new URLSearchParams({
      client_id: id,
      response_type: "code",
      redirect_uri: REDIRECT_URI,
      scope: SCOPES,
      state,
      show_dialog: "true",
    }).toString();

  console.log("\nAbre esta URL en el navegador y acepta:\n");
  console.log(`  ${url}\n`);
  console.log(`Esperando el callback en ${REDIRECT_URI} …\n`);

  const code = await new Promise((resolve, reject) => {
    const servidor = http.createServer((req, res) => {
      const recibida = new URL(req.url, `http://127.0.0.1:${PUERTO_CALLBACK}`);
      if (recibida.pathname !== "/callback") {
        res.writeHead(404).end();
        return;
      }

      const error = recibida.searchParams.get("error");
      const devuelto = recibida.searchParams.get("state");
      const codigo = recibida.searchParams.get("code");

      const responder = (mensaje) => {
        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end(
          `<!doctype html><meta charset="utf-8"><body style="font:16px system-ui;padding:3rem;background:#0b1119;color:#f1ece2">${mensaje}</body>`
        );
      };

      if (error) {
        responder("Permiso denegado. Puedes cerrar esta pestaña.");
        servidor.close();
        reject(new Error(`Spotify devolvió error=${error}`));
        return;
      }
      // El state protege contra que un tercero nos cuele su código.
      if (devuelto !== state) {
        responder("State inválido. Puedes cerrar esta pestaña.");
        servidor.close();
        reject(new Error("State no coincide — posible CSRF, abortado."));
        return;
      }

      responder("Listo. Ya puedes cerrar esta pestaña y volver a la terminal.");
      servidor.close();
      resolve(codigo);
    });

    servidor.on("error", (e) =>
      reject(
        new Error(
          `No pude escuchar en el puerto ${PUERTO_CALLBACK}: ${e.message}\n` +
            "  ¿Hay algo más usándolo?"
        )
      )
    );
    servidor.listen(PUERTO_CALLBACK, "127.0.0.1");
  });

  const tokens = await pedirToken({
    grant_type: "authorization_code",
    code,
    redirect_uri: REDIRECT_URI,
  });

  guardarRefresh(tokens.refresh_token);
  console.log(`✓ Sesión guardada en ${TOKEN_PATH}\n`);
  return tokens.access_token;
}

/** Access token de usuario a partir del refresh guardado. */
export async function tokenDeUsuario() {
  if (!haySesion()) {
    throw new ErrorDeConfig(
      "No hay sesión de Spotify guardada.\n" +
        "  Correr primero: node jai-sounds/scripts/ingest_spotify.mjs --login"
    );
  }
  const { refresh_token } = JSON.parse(fs.readFileSync(TOKEN_PATH, "utf-8"));
  const tokens = await pedirToken({
    grant_type: "refresh_token",
    refresh_token,
  });
  // Spotify a veces rota el refresh_token; si manda uno nuevo, hay que
  // quedarse con ese o la próxima sesión falla.
  if (tokens.refresh_token) guardarRefresh(tokens.refresh_token);
  return tokens.access_token;
}
