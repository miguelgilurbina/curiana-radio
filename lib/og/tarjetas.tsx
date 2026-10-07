import fs from "fs";
import path from "path";
import { ImageResponse } from "next/og";
import type { Capa } from "@/types/fichas";

// ── Las tarjetas para redes (og:image), 1200×630 ──────────────────────
// Se dibujan al compilar (las rutas de app/og son estáticas) con las fuentes
// de la marca en .woff (Satori no lee woff2; los archivos son el subconjunto
// latino de Fontsource, OFL — licencias al lado). Dos registros, los mismos
// del sitio: la noche (la radio, BRAND_MVP §8.1) y la sal y almagre
// (Kaketiana, design_handoff_kaketiana). Los hex son los de globals.css: aquí
// no hay CSS que resuelva tokens.

export const TAMANO = { width: 1200, height: 630 };

const FUENTES_DIR = path.join(process.cwd(), "lib", "og", "fuentes");
const leer = (archivo: string) => fs.readFileSync(path.join(FUENTES_DIR, archivo));

interface Fuente {
  name: string;
  data: Buffer;
  weight: 400 | 600;
  style: "normal" | "italic";
}
let fuentes: Fuente[] | null = null;
function cargarFuentes(): Fuente[] {
  fuentes ??= [
    { name: "Fraunces", data: leer("fraunces-latin-600-normal.woff"), weight: 600, style: "normal" },
    { name: "Fraunces", data: leer("fraunces-latin-400-italic.woff"), weight: 400, style: "italic" },
    { name: "Inter", data: leer("inter-latin-400-normal.woff"), weight: 400, style: "normal" },
    { name: "Inter", data: leer("inter-latin-600-normal.woff"), weight: 600, style: "normal" },
    { name: "Archivo Black", data: leer("archivo-black-latin-400-normal.woff"), weight: 400, style: "normal" },
  ];
  return fuentes;
}

let isotipoHueso: string | null = null;
/** El isotipo grande de la noche (PNG 512², hueso con alfa). */
function isotipoNoche(): string {
  isotipoHueso ??= `data:image/png;base64,${fs
    .readFileSync(path.join(process.cwd(), "public", "marca", "isotipo-hueso.png"))
    .toString("base64")}`;
  return isotipoHueso;
}

const espirales = new Map<string, string>();
/** La espiral vectorial (marca/espiral.svg) en un color: para el pie de las
 *  tarjetas, donde decodificar el PNG de 1024² por tarjeta costaba más que
 *  todo lo demás del build. */
function espiral(color: string): string {
  if (!espirales.has(color)) {
    const svg = fs
      .readFileSync(path.join(process.cwd(), "public", "marca", "espiral.svg"), "utf-8")
      .replaceAll("currentColor", color);
    espirales.set(color, `data:image/svg+xml;base64,${Buffer.from(svg).toString("base64")}`);
  }
  return espirales.get(color)!;
}

function responder(nodo: React.ReactElement) {
  return new ImageResponse(nodo, {
    ...TAMANO,
    fonts: cargarFuentes(),
    headers: { "Cache-Control": "public, max-age=86400, stale-while-revalidate=604800" },
  });
}

// ── La noche: la radio ────────────────────────────────────────────────

const NOCHE = {
  fondo: "#0f1621",
  hueso: "#eee6d4",
  hueso2: "#c6cfd9",
  filete: "#2a3a50",
  senal: "#e2a158",
};

export function tarjetaNoche({
  rotulo,
  titulo,
  bajada,
  pie = "curianaradio.com",
}: {
  rotulo: string;
  titulo: string;
  bajada: string;
  pie?: string;
}) {
  return responder(
    <div
      style={{
        ...TAMANO,
        display: "flex",
        background: NOCHE.fondo,
        color: NOCHE.hueso,
        padding: "64px 72px",
        fontFamily: "Inter",
      }}
    >
      <div style={{ display: "flex", flexDirection: "column", flex: 1, justifyContent: "space-between" }}>
        <div style={{ display: "flex", fontSize: 22, fontWeight: 600, letterSpacing: 5, color: NOCHE.senal }}>
          {rotulo.toUpperCase()}
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          {/* la voz de cartel (type 3c): Archivo Black, comprimida */}
          <div
            style={{
              display: "flex",
              fontFamily: "Archivo Black",
              fontSize: titulo.length > 16 ? 76 : 104,
              lineHeight: 0.95,
              letterSpacing: -1,
              textTransform: "uppercase",
              maxWidth: 760,
            }}
          >
            {titulo}
          </div>
          <div
            style={{
              display: "flex",
              marginTop: 28,
              fontFamily: "Fraunces",
              fontStyle: "italic",
              fontSize: 32,
              lineHeight: 1.3,
              color: NOCHE.hueso2,
              maxWidth: 700,
            }}
          >
            {bajada}
          </div>
        </div>
        <div
          style={{
            display: "flex",
            borderTop: `1px solid ${NOCHE.filete}`,
            paddingTop: 20,
            fontSize: 22,
            letterSpacing: 2,
            color: NOCHE.hueso2,
          }}
        >
          {pie}
        </div>
      </div>
      <div style={{ display: "flex", alignItems: "center", marginLeft: 40 }}>
        {/* eslint-disable-next-line @next/next/no-img-element, jsx-a11y/alt-text */}
        <img src={isotipoNoche()} width={300} height={300} />
      </div>
    </div>,
  );
}

// ── La sal y almagre: Kaketiana ───────────────────────────────────────

const SAL = {
  papel: "#f2ede3",
  hundido: "#e4dbc8",
  tinta: "#241d15",
  tintaSuave: "#4f4638",
  filete: "#d5c9b0",
  rubrica: "#9c3a1d",
  fuego: "#b06a1c",
};

const COLOR_CAPA: Record<Capa, string> = {
  atestiguado: "#2d6340",
  reconstruido: "#8c4e0c",
  retroabstraido: "#5a4a99",
  hipotetico: "#6f5f48",
};

function GlifoCapa({ capa, tamano }: { capa: Capa; tamano: number }) {
  const color = COLOR_CAPA[capa];
  return (
    <svg width={tamano} height={tamano} viewBox="0 0 12 12">
      {capa === "atestiguado" && <circle cx="6" cy="6" r="5.25" fill={color} />}
      {capa === "reconstruido" && <circle cx="6" cy="6" r="4.75" fill="none" stroke={color} strokeWidth="1.5" />}
      {capa === "reconstruido" && <path d="M6 1.25 A4.75 4.75 0 0 0 6 10.75 Z" fill={color} />}
      {capa === "retroabstraido" && <circle cx="6" cy="6" r="4.75" fill="none" stroke={color} strokeWidth="1.5" />}
      {capa === "retroabstraido" && <circle cx="6" cy="6" r="2" fill={color} />}
      {capa === "hipotetico" && (
        <circle cx="6" cy="6" r="4.75" fill="none" stroke={color} strokeWidth="1.5" strokeDasharray="2.2 1.5" />
      )}
    </svg>
  );
}

function MarcoSal({ rotulo, pie, children }: { rotulo: string; pie: string; children: React.ReactNode }) {
  return (
    <div
      style={{
        ...TAMANO,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        background: SAL.papel,
        color: SAL.tinta,
        padding: "60px 72px",
        fontFamily: "Inter",
        borderTop: `10px solid ${SAL.rubrica}`,
      }}
    >
      <div style={{ display: "flex", fontSize: 21, fontWeight: 600, letterSpacing: 5, color: SAL.rubrica }}>
        {rotulo.toUpperCase()}
      </div>
      {children}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          borderTop: `1px solid ${SAL.filete}`,
          paddingTop: 18,
          fontSize: 21,
          letterSpacing: 1,
          color: SAL.tintaSuave,
        }}
      >
        <span>{pie}</span>
        <span style={{ display: "flex", alignItems: "center", gap: 14 }}>
          {/* eslint-disable-next-line @next/next/no-img-element, jsx-a11y/alt-text */}
          <img src={espiral(SAL.tinta)} width={40} height={40} />
          <span style={{ fontWeight: 600, letterSpacing: 4 }}>CURIANA RADIO</span>
        </span>
      </div>
    </div>
  );
}

/** Una sección o un artículo de Kaketiana: la pregunta en la display. */
export function tarjetaSal({ rotulo, titulo, bajada, pie }: { rotulo: string; titulo: string; bajada?: string; pie: string }) {
  const largo = titulo.length;
  return responder(
    <MarcoSal rotulo={rotulo} pie={pie}>
      <div style={{ display: "flex", flexDirection: "column", maxWidth: 1000 }}>
        <div
          style={{
            display: "flex",
            fontFamily: "Fraunces",
            fontWeight: 600,
            fontSize: largo > 70 ? 54 : largo > 40 ? 66 : 84,
            lineHeight: 1.08,
            letterSpacing: -1,
          }}
        >
          {titulo}
        </div>
        {bajada && (
          <div
            style={{
              display: "flex",
              marginTop: 24,
              fontFamily: "Fraunces",
              fontStyle: "italic",
              fontSize: 30,
              lineHeight: 1.35,
              color: SAL.tintaSuave,
            }}
          >
            {bajada}
          </div>
        )}
      </div>
    </MarcoSal>,
  );
}

/** Una voz del diccionario: la forma en ocre, la glosa, y cómo la sabemos. */
export function tarjetaVoz({
  forma,
  glosa,
  capa,
  etiquetaCapa,
  categoria,
  fuente,
}: {
  forma: string;
  glosa: string;
  capa: Capa;
  etiquetaCapa: string;
  categoria: string | null;
  fuente: string | null;
}) {
  return responder(
    <MarcoSal rotulo="Kaketiana · El diccionario" pie="curianaradio.com/kaketiana/lexicon">
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 24 }}>
          <span
            style={{
              fontFamily: "Fraunces",
              fontWeight: 600,
              fontSize: forma.length > 14 ? 96 : 132,
              lineHeight: 1,
              letterSpacing: -2,
              color: SAL.fuego,
            }}
          >
            {forma}
          </span>
          {categoria && <span style={{ fontSize: 26, color: SAL.tintaSuave }}>{categoria}</span>}
        </div>
        <div
          style={{
            display: "flex",
            marginTop: 22,
            fontFamily: "Fraunces",
            fontStyle: "italic",
            fontSize: glosa.length > 60 ? 34 : 44,
            lineHeight: 1.25,
            maxWidth: 1000,
          }}
        >
          «{glosa}»
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 30 }}>
          <GlifoCapa capa={capa} tamano={26} />
          <span style={{ fontSize: 22, fontWeight: 600, letterSpacing: 3, color: COLOR_CAPA[capa] }}>
            {`VOZ ${etiquetaCapa.toUpperCase()}`}
          </span>
          {fuente && (
            <span style={{ fontSize: 22, color: SAL.tintaSuave, marginLeft: 12 }}>{`· ${fuente}`}</span>
          )}
        </div>
      </div>
    </MarcoSal>,
  );
}
