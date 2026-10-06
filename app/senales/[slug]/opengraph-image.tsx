import { readFile } from "fs/promises";
import path from "path";
import { ImageResponse } from "next/og";
import { fechaLarga, getSenal, getSenales } from "@/lib/senales";

// La tarjeta de una señal cuando se comparte (LinkedIn, WhatsApp, X): la
// noche de la v1, el isotipo en hueso, el título en la editorial (Lora 600),
// la firma y el filete en el acento de la noche (oro de arena, BRAND_MVP
// §13). Se genera en el build, una por señal. Las fuentes son woff de
// @fontsource (OFL) porque el renderizador de next/og no lee woff2.

export const alt = "Señales — Curiana Radio";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export function generateStaticParams() {
  return getSenales().map((s) => ({ slug: s.slug }));
}

const raiz = process.cwd();
const fuente = (archivo: string) =>
  readFile(path.join(raiz, "app", "senales", "fuentes", archivo));

export default async function Imagen({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const senal = getSenal(slug);
  const [lora600, loraItalica, inter500, isotipo] = await Promise.all([
    fuente("lora-latin-600-normal.woff"),
    fuente("lora-latin-400-italic.woff"),
    fuente("inter-latin-500-normal.woff"),
    readFile(path.join(raiz, "public", "marca", "isotipo-hueso.png")),
  ]);
  const titulo = senal?.titulo ?? "Señales";
  // el título manda: se achica si es largo para que quepa en tres líneas
  const cuerpo = titulo.length > 90 ? 52 : titulo.length > 55 ? 62 : 74;

  return new ImageResponse(
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "64px 80px",
        background:
          "linear-gradient(135deg, #0F1621 0%, #1F2C3E 60%, #131C28 100%)",
        color: "#EEE6D4",
        fontFamily: "Inter",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
        {/* eslint-disable-next-line @next/next/no-img-element -- next/og sólo entiende <img> */}
        <img
          src={`data:image/png;base64,${isotipo.toString("base64")}`}
          width={56}
          height={56}
          alt=""
        />
        <div
          style={{
            display: "flex",
            fontSize: 20,
            letterSpacing: 6,
            color: "#C6CFD9",
          }}
        >
          CURIANA RADIO · SEÑALES
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
        <div
          style={{
            display: "flex",
            fontFamily: "Lora",
            fontWeight: 600,
            fontSize: cuerpo,
            lineHeight: 1.12,
            maxWidth: 1040,
          }}
        >
          {titulo}
        </div>
        {senal && (
          <div
            style={{
              display: "flex",
              fontFamily: "Lora",
              fontStyle: "italic",
              fontSize: 28,
              color: "#C6CFD9",
            }}
          >
            {senal.autor} · {fechaLarga(senal.fecha)}
          </div>
        )}
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
        <div
          style={{
            display: "flex",
            width: 96,
            height: 4,
            background: "#E6B43C" /* el acento de la noche: oro de arena */,
          }}
        />
        <div
          style={{
            display: "flex",
            fontSize: 20,
            letterSpacing: 4,
            color: "#C6CFD9",
          }}
        >
          CURIANARADIO.COM
        </div>
      </div>
    </div>,
    {
      ...size,
      fonts: [
        { name: "Lora", data: lora600, weight: 600, style: "normal" },
        { name: "Lora", data: loraItalica, weight: 400, style: "italic" },
        { name: "Inter", data: inter500, weight: 500, style: "normal" },
      ],
    },
  );
}
