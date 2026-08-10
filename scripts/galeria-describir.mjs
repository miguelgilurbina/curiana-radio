#!/usr/bin/env node
/**
 * Describe cada obra mirándola, y escribe el resultado en el manifest.
 *
 *   node scripts/galeria-describir.mjs enviar  [--limite N] [--modelo <id>]
 *   node scripts/galeria-describir.mjs recoger [--env <archivo>]
 *
 * Por qué existe: los títulos y textos alternativos actuales salen del prompt
 * de Midjourney, y 72 de esas 821 obras nombran a un artista. Publicarlos es
 * apoyar la obra en el nombre de otro. Estas descripciones salen de mirar la
 * imagen, no de leer el prompt.
 *
 * Va por la Batch API: 821 peticiones no tienen ninguna urgencia y cuestan la
 * mitad. `enviar` deja el lote encolado y `recoger` lo vuelca al manifest
 * cuando termina; entre una cosa y otra puedes cerrar el portátil.
 */

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const RAIZ = process.cwd();
const MANIFEST = path.join(RAIZ, "content", "galeria", "obras.json");
const TRABAJO = path.join(RAIZ, ".galeria-trabajo");
const LOTE = path.join(TRABAJO, "descripciones-lote.json");

/**
 * Se mira la variante de 400px, no el máster. A esa escala la imagen ya se
 * lee entera y cuesta unos pocos cientos de tokens en vez de unos miles:
 * describir no necesita resolución, necesita composición.
 */
const ANCHO_QUE_SE_MIRA = 400;

const MODELO = "claude-opus-5";

/**
 * El prompt vive en content/galeria/voz.md, no aquí. Es contenido editorial —
 * la voz de la galería — y quien la afina no debería tener que abrir un script
 * ni saber JavaScript. Los subagentes leen ese mismo archivo, así que hay una
 * sola fuente de verdad para el tono.
 */
const VOZ = path.join(RAIZ, "content", "galeria", "voz.md");

async function leerVoz() {
  try {
    return await fs.readFile(VOZ, "utf-8");
  } catch {
    salir(`No encuentro el prompt de la galería en ${VOZ}`);
  }
}

const ESQUEMA = {
  type: "object",
  properties: {
    titulo: { type: "string", description: "Dos a cinco palabras." },
    concepto: {
      type: "string",
      description: "Una sola frase, hasta 35 palabras.",
    },
    alt: {
      type: "string",
      description: "Una frase llana y factual para lectores de pantalla.",
    },
  },
  required: ["titulo", "concepto", "alt"],
  additionalProperties: false,
};

// ── Utilidades ────────────────────────────────────────────────────────

function salir(mensaje) {
  console.error(`\n✗ ${mensaje}\n`);
  process.exit(1);
}

async function cargarEnv(ruta) {
  let texto;
  try {
    texto = await fs.readFile(ruta, "utf-8");
  } catch {
    salir(`No pude leer el archivo de entorno: ${ruta}`);
  }
  for (const linea of texto.split(/\r?\n/)) {
    const limpia = linea.trim();
    if (!limpia || limpia.startsWith("#")) continue;
    const i = limpia.indexOf("=");
    if (i === -1) continue;
    const clave = limpia.slice(0, i).trim();
    const valor = limpia.slice(i + 1).trim().replace(/^["']|["']$/g, "");
    if (!process.env[clave]) process.env[clave] = valor;
  }
}

async function leerManifest() {
  return JSON.parse(await fs.readFile(MANIFEST, "utf-8"));
}

async function escribirManifest(m) {
  await fs.writeFile(MANIFEST, JSON.stringify(m, null, 2) + "\n", "utf-8");
}

async function cliente() {
  if (!process.env.ANTHROPIC_API_KEY && !process.env.ANTHROPIC_AUTH_TOKEN) {
    salir(
      "Falta ANTHROPIC_API_KEY en el entorno.\n" +
        "  Pásala con --env <archivo>, con el archivo FUERA del repo:\n" +
        "  esta carpeta sincroniza a OneDrive."
    );
  }
  const { default: Anthropic } = await import("@anthropic-ai/sdk");
  return new Anthropic();
}

/** Obras que tienen imagen mirable y aún no tienen concepto escrito. */
function pendientes(manifest) {
  return manifest.obras.filter(
    (o) => o.anchos?.length > 0 && !o.concepto?.trim()
  );
}

// ── Fase 1: enviar el lote ────────────────────────────────────────────

async function enviar(opciones) {
  const client = await cliente();
  const sistema = await leerVoz();
  const manifest = await leerManifest();
  const todas = pendientes(manifest);
  const obras = opciones.limite ? todas.slice(0, opciones.limite) : todas;

  if (obras.length === 0) salir("No hay obras pendientes de describir.");
  console.log(`\nPreparando ${obras.length} obra(s)…\n`);

  const peticiones = [];
  for (const obra of obras) {
    // Se manda el ancho más pequeño disponible que llegue a 400px.
    const ancho =
      obra.anchos.find((a) => a >= ANCHO_QUE_SE_MIRA) ??
      obra.anchos[obra.anchos.length - 1];
    const archivo = path.join(TRABAJO, `${obra.slug}-${ancho}.webp`);
    let datos;
    try {
      datos = await fs.readFile(archivo);
    } catch {
      console.log(`  ⚠ falta el webp de ${obra.slug}, la salto`);
      continue;
    }

    peticiones.push({
      custom_id: obra.slug,
      params: {
        model: opciones.modelo,
        max_tokens: 4000,
        system: sistema,
        // Efecto medio: describir una imagen no es un problema difícil, pero
        // sí es escritura, y en bajo la prosa se aplana.
        output_config: {
          effort: "medium",
          format: { type: "json_schema", schema: ESQUEMA },
        },
        messages: [
          {
            role: "user",
            content: [
              {
                type: "image",
                source: {
                  type: "base64",
                  media_type: "image/webp",
                  data: datos.toString("base64"),
                },
              },
              { type: "text", text: "Describe esta obra." },
            ],
          },
        ],
      },
    });
  }

  if (peticiones.length === 0) salir("No pude leer ninguna imagen.");

  const lote = await client.messages.batches.create({ requests: peticiones });
  await fs.writeFile(
    LOTE,
    JSON.stringify({ id: lote.id, enviadas: peticiones.length }, null, 2),
    "utf-8"
  );

  console.log(`✓ Lote encolado: ${lote.id}`);
  console.log(`  ${peticiones.length} obras · estado: ${lote.processing_status}`);
  console.log(`\nSuele tardar menos de una hora (máximo 24).`);
  console.log(`Cuando quieras: node scripts/galeria-describir.mjs recoger\n`);
}

// ── Fase 2: recoger resultados ────────────────────────────────────────

async function recoger() {
  const client = await cliente();

  let registro;
  try {
    registro = JSON.parse(await fs.readFile(LOTE, "utf-8"));
  } catch {
    salir("No hay ningún lote enviado. Corre `enviar` primero.");
  }

  const lote = await client.messages.batches.retrieve(registro.id);
  console.log(`\nLote ${lote.id}: ${lote.processing_status}`);
  if (lote.processing_status !== "ended") {
    const c = lote.request_counts;
    console.log(`  en proceso: ${c.processing} · listas: ${c.succeeded} · con error: ${c.errored}`);
    console.log(`\nTodavía no ha terminado. Vuelve a intentarlo más tarde.\n`);
    return;
  }

  const manifest = await leerManifest();
  const porSlug = new Map(manifest.obras.map((o) => [o.slug, o]));
  let escritas = 0;
  const problemas = [];

  // Los resultados llegan en cualquier orden: se casan por custom_id, nunca
  // por posición.
  for await (const r of await client.messages.batches.results(lote.id)) {
    const obra = porSlug.get(r.custom_id);
    if (!obra) continue;

    if (r.result.type !== "succeeded") {
      problemas.push(`${r.custom_id}: ${r.result.type}`);
      continue;
    }
    const msg = r.result.message;
    // Una imagen puede activar los clasificadores de seguridad. Eso no es un
    // fallo del script: se anota y se revisa a mano.
    if (msg.stop_reason === "refusal") {
      problemas.push(`${r.custom_id}: el modelo declinó describirla`);
      continue;
    }

    const bloque = msg.content.find((b) => b.type === "text");
    if (!bloque) {
      problemas.push(`${r.custom_id}: respuesta sin texto`);
      continue;
    }

    let ficha;
    try {
      ficha = JSON.parse(bloque.text);
    } catch {
      problemas.push(`${r.custom_id}: JSON ilegible`);
      continue;
    }

    obra.titulo = ficha.titulo.trim();
    obra.concepto = ficha.concepto.trim();
    obra.alt = ficha.alt.trim();
    escritas++;
  }

  await escribirManifest(manifest);

  console.log(`\n✓ ${escritas} obras descritas y escritas en el manifest`);
  if (problemas.length > 0) {
    console.log(`\n⚠ ${problemas.length} sin resolver:`);
    for (const p of problemas.slice(0, 15)) console.log(`   ${p}`);
    console.log(`\n   Vuelve a correr \`enviar\` para reintentar solo esas.`);
  }
  console.log("");
}

// ── Entrada ───────────────────────────────────────────────────────────

async function main() {
  const [comando, ...resto] = process.argv.slice(2);
  const opciones = { limite: null, env: null, modelo: MODELO };
  for (let i = 0; i < resto.length; i++) {
    if (resto[i] === "--limite") opciones.limite = Number(resto[++i]);
    else if (resto[i] === "--env") opciones.env = resto[++i];
    else if (resto[i] === "--modelo") opciones.modelo = resto[++i];
  }
  if (opciones.env) await cargarEnv(opciones.env);

  if (comando === "enviar") await enviar(opciones);
  else if (comando === "recoger") await recoger();
  else
    salir(
      "Uso:\n" +
        "  node scripts/galeria-describir.mjs enviar  [--limite N] [--modelo <id>] [--env <archivo>]\n" +
        "  node scripts/galeria-describir.mjs recoger [--env <archivo>]"
    );
}

main().catch((err) => salir(err.stack ?? String(err)));
