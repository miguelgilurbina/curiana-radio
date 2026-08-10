#!/usr/bin/env node
/**
 * Ingesta de la galería: de un volcado de PNG de Midjourney al manifest.
 *
 *   node scripts/galeria-ingesta.mjs preparar <carpeta...> [opciones]
 *   node scripts/galeria-ingesta.mjs subir [--overwrite]
 *
 * Dos fases a propósito. `preparar` no necesita credenciales: extrae los
 * metadatos, genera la escalera de WebP en una carpeta de trabajo fuera del
 * repo y escribe el manifest con las obras ya descritas. Se puede correr,
 * revisar y repetir sin tocar nada remoto. `subir` es la única que habla con
 * Vercel Blob.
 *
 * Ambas son reanudables: `preparar` salta lo que ya generó y `subir` lleva un
 * registro de lo ya subido. Con ~800 imágenes eso no es un lujo.
 *
 * El token NO se lee de ningún archivo del proyecto: este repo sincroniza a
 * OneDrive. Pásalo como variable de entorno solo para la corrida.
 */

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import sharp from "sharp";

// ── Constantes de ingesta ─────────────────────────────────────────────

const EXTENSIONES = new Set([".png", ".jpg", ".jpeg", ".webp"]);

/**
 * Escalera de anchos. Se recorta a la resolución real de cada fuente: las
 * exportaciones de Midjourney rondan los 1200-1456px, así que generar una
 * variante de 2000px produciría un archivo idéntico al de 1400 ocupando el
 * doble. Nunca se amplía.
 */
const ESCALERA = [400, 800, 1400];

/** Calidad WebP. 80 es el punto donde dejar de ver diferencia en pantalla. */
const CALIDAD = 80;

/** Cuántas imágenes se procesan a la vez. Sube CPU sin reventar memoria. */
const CONCURRENCIA = 4;

const RAIZ = process.cwd();
const MANIFEST = path.join(RAIZ, "content", "galeria", "obras.json");
/** Fuera del repo versionado: son cientos de MB de derivados regenerables. */
const TRABAJO = path.join(RAIZ, ".galeria-trabajo");
const REGISTRO_SUBIDA = path.join(TRABAJO, "subidas.json");

// ── Utilidades ────────────────────────────────────────────────────────

function salir(mensaje) {
  console.error(`\n✗ ${mensaje}\n`);
  process.exit(1);
}

const UUID = "[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}";
const RE_NOMBRE = new RegExp(`^(.*)_(${UUID})_(\\d+)$`, "i");

/**
 * Midjourney codifica el prompt en el nombre del archivo:
 *   `<prompt_con_guiones_bajos>_<uuid-de-generacion>_<variante>.png`
 * Ese uuid agrupa las cuatro imágenes de una misma parrilla, y el número final
 * dice cuál de las cuatro es. Aprovecharlo evita transcribir 800 prompts.
 */
function analizarNombre(base) {
  const m = base.match(RE_NOMBRE);
  if (!m) return { prompt: limpiarPrompt(base), generacion: null, variante: 0 };
  return {
    prompt: limpiarPrompt(m[1]),
    generacion: m[2].toLowerCase(),
    variante: Number(m[3]),
  };
}

function limpiarPrompt(crudo) {
  return crudo
    .replace(/_/g, " ")
    // Las referencias de imagen (`httpss.mj.run<hash>`) no son texto legible.
    .replace(/https?s?\.?mj\.run\S*/gi, "")
    .replace(/\s+/g, " ")
    .trim();
}

/** El título es el prompt sin sus parámetros y recortado a algo pronunciable. */
function tituloDesdePrompt(prompt) {
  const sinParametros = prompt.split(/\s--/)[0].trim();
  const palabras = sinParametros.split(" ").filter(Boolean).slice(0, 8);
  if (palabras.length === 0) return "Sin título";
  const texto = palabras.join(" ");
  return texto.charAt(0).toUpperCase() + texto.slice(1);
}

function aSlug(texto) {
  return texto
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 48)
    .replace(/-+$/g, "");
}

/**
 * Anchos a generar para una fuente de `anchoFuente` píxeles. Añade el ancho
 * nativo solo si la escalera se queda muy corta respecto a él; si no, la
 * variante extra sería casi idéntica a la mayor y solo ocuparía sitio.
 */
function anchosPara(anchoFuente) {
  const anchos = ESCALERA.filter((a) => a <= anchoFuente);
  if (anchos.length === 0) return [anchoFuente];
  const mayor = anchos[anchos.length - 1];
  if (mayor < anchoFuente * 0.85) anchos.push(anchoFuente);
  return anchos;
}

/** Color dominante aproximado: la imagen reducida a un solo píxel. */
async function colorDominante(imagen) {
  const { data } = await imagen
    .clone()
    .resize(1, 1, { fit: "fill" })
    .raw()
    .toBuffer({ resolveWithObject: true });
  const hex = (n) => n.toString(16).padStart(2, "0");
  return `#${hex(data[0])}${hex(data[1])}${hex(data[2])}`;
}

/** Ejecuta `tarea` sobre `items` con como mucho `limite` en vuelo. */
async function enParalelo(items, limite, tarea) {
  let siguiente = 0;
  const trabajadores = Array.from(
    { length: Math.min(limite, items.length) },
    async () => {
      while (siguiente < items.length) {
        const i = siguiente++;
        await tarea(items[i], i);
      }
    }
  );
  await Promise.all(trabajadores);
}

async function leerManifest() {
  try {
    return JSON.parse(await fs.readFile(MANIFEST, "utf-8"));
  } catch (err) {
    if (err.code === "ENOENT") return { blobBase: null, series: [], obras: [] };
    throw err;
  }
}

async function escribirManifest(manifest) {
  await fs.mkdir(path.dirname(MANIFEST), { recursive: true });
  await fs.writeFile(MANIFEST, JSON.stringify(manifest, null, 2) + "\n", "utf-8");
}

async function existe(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

// ── Fase 1: preparar ──────────────────────────────────────────────────

async function preparar(carpetas, opciones) {
  if (carpetas.length === 0) {
    salir(
      "Falta al menos una carpeta con imágenes.\n" +
        "  Si vienes de un ZIP, extráelo primero fuera del repo:\n" +
        '  Expand-Archive "$env:USERPROFILE\\Downloads\\midjourney_session_1.zip" -DestinationPath "$env:USERPROFILE\\galeria-fuente"'
    );
  }

  const manifest = await leerManifest();
  const serie = opciones.serie ?? manifest.series[0]?.id ?? "archivo";
  if (!manifest.series.some((s) => s.id === serie)) {
    manifest.series.push({
      id: serie,
      titulo: serie,
      descripcion: "TODO: describir la serie.",
    });
  }

  // Reunir archivos de todas las carpetas.
  const archivos = [];
  for (const carpeta of carpetas) {
    let entradas;
    try {
      entradas = await fs.readdir(carpeta);
    } catch {
      salir(`No pude leer la carpeta: ${carpeta}`);
    }
    for (const nombre of entradas.sort()) {
      if (EXTENSIONES.has(path.extname(nombre).toLowerCase())) {
        archivos.push(path.join(carpeta, nombre));
      }
    }
  }
  if (archivos.length === 0) salir("No encontré imágenes en esas carpetas.");

  const aProcesar = opciones.limite ? archivos.slice(0, opciones.limite) : archivos;
  await fs.mkdir(TRABAJO, { recursive: true });

  console.log(`\n${aProcesar.length} imagen(es) a preparar → ${TRABAJO}\n`);

  const porSlug = new Map(manifest.obras.map((o) => [o.slug, o]));
  const usados = new Set(porSlug.keys());
  const nuevas = [];
  let hechas = 0;
  let saltadas = 0;
  const errores = [];

  await enParalelo(aProcesar, CONCURRENCIA, async (origen) => {
    try {
      const base = path.basename(origen, path.extname(origen));
      const { prompt, generacion, variante } = analizarNombre(base);
      const titulo = tituloDesdePrompt(prompt);

      // El slug lleva un sufijo de la generación porque cuatro variantes del
      // mismo prompt producen el mismo título.
      const sufijo = generacion
        ? `${generacion.slice(0, 8)}-${variante}`
        : String(hechas);
      let slug = `${aSlug(titulo)}-${sufijo}`;
      while (usados.has(slug) && !porSlug.has(slug)) slug = `${slug}-x`;
      usados.add(slug);

      const imagen = sharp(origen).rotate();
      const meta = await imagen.metadata();
      const anchos = anchosPara(meta.width);

      // Reanudable: si ya están todas las variantes de este slug, no se
      // recomprime. Con 800 imágenes, repetir el trabajo cuesta media hora.
      const destinos = anchos.map((a) => path.join(TRABAJO, `${slug}-${a}.webp`));
      const yaEstan = (await Promise.all(destinos.map(existe))).every(Boolean);

      let mayorW = null;
      let mayorH = null;
      if (yaEstan) {
        saltadas++;
        const m = await sharp(destinos[destinos.length - 1]).metadata();
        mayorW = m.width;
        mayorH = m.height;
      } else {
        for (let i = 0; i < anchos.length; i++) {
          const salida = await imagen
            .clone()
            .resize({ width: anchos[i], withoutEnlargement: true })
            .webp({ quality: CALIDAD })
            .toFile(destinos[i]);
          if (i === anchos.length - 1) {
            mayorW = salida.width;
            mayorH = salida.height;
          }
        }
      }

      const color = await colorDominante(imagen);

      const existente = porSlug.get(slug);
      const obra = existente ?? {
        slug,
        serie,
        orden: 0,
        estado: "pendiente",
        // Sin texto curatorial: nadie escribe 800 statements. La ficha muestra
        // el prompt, que es el contenido real de una imagen generada.
        concepto: "",
        anio: 2025,
        tags: [],
        licencia: "reservado",
        licenciaDetalle: { tipo: "reservado", print: false },
        procedencia: { herramienta: "Midjourney" },
      };

      obra.titulo = existente?.titulo ?? titulo;
      // El alt sale del prompt: describe lo que se pidió que hubiera en la
      // imagen. No es una descripción escrita a mano, pero es honesto y muy
      // superior a dejarlo vacío.
      obra.alt = existente?.alt ?? (prompt.split(/\s--/)[0].trim() || titulo);
      obra.w = mayorW;
      obra.h = mayorH;
      obra.anchos = anchos;
      obra.color = color;
      if (generacion) obra.generacion = generacion;
      obra.procedencia = {
        ...obra.procedencia,
        herramienta: obra.procedencia?.herramienta ?? "Midjourney",
        prompt,
        generacion: generacion ?? undefined,
        variante,
      };

      if (!existente) nuevas.push(obra);
      hechas++;
      if (hechas % 50 === 0) {
        console.log(`  ${hechas}/${aProcesar.length}…`);
      }
    } catch (err) {
      errores.push(`${path.basename(origen)}: ${err.message}`);
    }
  });

  // Orden estable por título para que el manifest no baile entre corridas.
  manifest.obras.push(...nuevas);
  manifest.obras.sort((a, b) => a.slug.localeCompare(b.slug, "es"));
  manifest.obras.forEach((o, i) => {
    o.orden = i + 1;
  });

  await escribirManifest(manifest);

  console.log(`\n✓ ${hechas} preparadas (${saltadas} ya estaban)`);
  console.log(`  ${nuevas.length} obras nuevas en el manifest`);
  console.log(`  total en catálogo: ${manifest.obras.length}`);
  if (errores.length > 0) {
    console.log(`\n⚠ ${errores.length} fallo(s):`);
    for (const e of errores.slice(0, 10)) console.log(`   ${e}`);
  }
  console.log(`\nSiguiente: node scripts/galeria-ingesta.mjs subir\n`);
}

// ── Fase 2: subir ─────────────────────────────────────────────────────

/**
 * Carga un archivo de variables (el que produce `vercel env pull`) en
 * process.env. Se acepta una ruta explícita para poder tenerlo FUERA del
 * repo: `.env.local` en la carpeta del proyecto lo sincronizaría OneDrive
 * aunque esté en .gitignore.
 */
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
    const valor = limpia
      .slice(i + 1)
      .trim()
      .replace(/^["']|["']$/g, "");
    if (!process.env[clave]) process.env[clave] = valor;
  }
}

async function subir(opciones) {
  if (opciones.env) await cargarEnv(opciones.env);

  // Dos credenciales posibles. Vercel conecta los stores con OIDC por defecto
  // (token corto que rota solo) y solo crea BLOB_READ_WRITE_TOKEN si se pidió
  // al crear el store. El SDK resuelve solo: si están VERCEL_OIDC_TOKEN y
  // BLOB_STORE_ID en el entorno, usa OIDC; si no, cae al token estático.
  const tieneRW = Boolean(process.env.BLOB_READ_WRITE_TOKEN);
  const tieneOidc = Boolean(
    process.env.VERCEL_OIDC_TOKEN && process.env.BLOB_STORE_ID
  );
  if (!tieneRW && !tieneOidc) {
    salir(
      "No hay credenciales de Blob en el entorno. Dos opciones:\n\n" +
        "  a) OIDC (lo que Vercel crea por defecto):\n" +
        "     conecta el store al proyecto incluyendo el entorno Development, y luego\n" +
        "       vercel env pull \"$env:TEMP\\curiana-blob.env\"\n" +
        "       npm run galeria:subir -- --env \"$env:TEMP\\curiana-blob.env\"\n\n" +
        "  b) Token estático, si tu store creó BLOB_READ_WRITE_TOKEN:\n" +
        "       $env:BLOB_READ_WRITE_TOKEN = Read-Host \"Token\"\n\n" +
        "  En ambos casos, fuera del repo: esta carpeta sincroniza a OneDrive."
    );
  }
  console.log(
    `\nCredencial: ${tieneRW ? "BLOB_READ_WRITE_TOKEN" : "OIDC (VERCEL_OIDC_TOKEN + BLOB_STORE_ID)"}`
  );

  const { put } = await import("@vercel/blob");

  const manifest = await leerManifest();
  const publicables = manifest.obras.filter((o) => o.anchos?.length > 0);
  if (publicables.length === 0) salir("No hay nada preparado. Corre `preparar` primero.");

  let registro = {};
  if (await existe(REGISTRO_SUBIDA)) {
    registro = JSON.parse(await fs.readFile(REGISTRO_SUBIDA, "utf-8"));
  }

  // Aplanar a la lista de archivos concretos que faltan por subir.
  const pendientes = [];
  for (const obra of publicables) {
    for (const ancho of obra.anchos) {
      const clave = `${obra.slug}-${ancho}.webp`;
      if (registro[clave] && !opciones.overwrite) continue;
      pendientes.push({ clave, local: path.join(TRABAJO, clave) });
    }
  }

  if (pendientes.length === 0) {
    console.log("\n✓ Todo estaba subido ya.\n");
  } else {
    console.log(`\n${pendientes.length} archivo(s) por subir…\n`);
    let subidos = 0;
    const errores = [];
    // Concurrencia moderada: `put()` cuenta como operación avanzada y los
    // planes tienen tope por minuto (900/min en Hobby).
    await enParalelo(pendientes, 6, async ({ clave, local }) => {
      try {
        const cuerpo = await fs.readFile(local);
        const blob = await put(`galeria/${clave}`, cuerpo, {
          access: "public",
          contentType: "image/webp",
          addRandomSuffix: false,
          allowOverwrite: true,
          // Un año: el nombre incluye el slug y el ancho, así que un cambio de
          // imagen implica un nombre nuevo. Nunca hay que invalidar.
          cacheControlMaxAge: 31536000,
        });
        registro[clave] = blob.url;
        subidos++;
        if (subidos % 50 === 0) {
          console.log(`  ${subidos}/${pendientes.length}…`);
          await fs.writeFile(REGISTRO_SUBIDA, JSON.stringify(registro), "utf-8");
        }
      } catch (err) {
        errores.push(`${clave}: ${err.message}`);
      }
    });
    await fs.writeFile(REGISTRO_SUBIDA, JSON.stringify(registro), "utf-8");
    console.log(`\n✓ ${subidos} subidos`);
    if (errores.length > 0) {
      console.log(`⚠ ${errores.length} fallo(s) — vuelve a correr para reintentar:`);
      for (const e of errores.slice(0, 10)) console.log(`   ${e}`);
    }
  }

  // El manifest guarda el origen del store una sola vez, no una URL por
  // variante: con 800 obras x 3 anchos eso serían ~200 KB de JSON repetido.
  const cualquiera = Object.values(registro)[0];
  if (cualquiera) {
    const u = new URL(cualquiera);
    manifest.blobBase = `${u.origin}/galeria`;
  }
  for (const obra of manifest.obras) {
    // `length > 0` no es redundante: `[].every(...)` es true, y sin esa
    // comprobación las obras que son solo concepto —sin ninguna variante
    // generada— se marcarían como publicadas y aparecerían con licencia sobre
    // un degradado vacío, afirmando ser algo que no son.
    const tieneVariantes = obra.anchos?.length > 0;
    if (
      tieneVariantes &&
      obra.anchos.every((a) => registro[`${obra.slug}-${a}.webp`])
    ) {
      obra.estado = "publicada";
    }
  }
  await escribirManifest(manifest);
  console.log(`\n✓ Manifest actualizado. blobBase = ${manifest.blobBase}\n`);
}

// ── Entrada ───────────────────────────────────────────────────────────

async function main() {
  const [comando, ...resto] = process.argv.slice(2);
  const opciones = { serie: null, limite: null, overwrite: false, env: null };
  const posicionales = [];
  for (let i = 0; i < resto.length; i++) {
    const a = resto[i];
    if (a === "--serie") opciones.serie = resto[++i];
    else if (a === "--limite") opciones.limite = Number(resto[++i]);
    else if (a === "--env") opciones.env = resto[++i];
    else if (a === "--overwrite") opciones.overwrite = true;
    else if (!a.startsWith("--")) posicionales.push(a);
  }

  if (comando === "preparar") await preparar(posicionales, opciones);
  else if (comando === "subir") await subir(opciones);
  else
    salir(
      "Uso:\n" +
        "  node scripts/galeria-ingesta.mjs preparar <carpeta...> [--serie <id>] [--limite N]\n" +
        "  node scripts/galeria-ingesta.mjs subir [--env <archivo>] [--overwrite]"
    );
}

main().catch((err) => salir(err.stack ?? String(err)));
