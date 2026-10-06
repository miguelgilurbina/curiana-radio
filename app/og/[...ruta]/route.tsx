import { getAllEditions } from "@/lib/content";
import { getFichas, getFichasSeed } from "@/lib/fichas";
import { getAllPersonajes } from "@/lib/personajes";
import { CAPA } from "@/lib/sim-theme";
import { getWikiIndice } from "@/lib/wiki";
import { recortar, SITIO } from "@/lib/seo";
import { tarjetaNoche, tarjetaSal, tarjetaVoz } from "@/lib/og/tarjetas";
import { SECCIONES_WIKI } from "@/types/wiki";

// Las tarjetas para redes de todo el sitio. La ruta de la tarjeta es la de la
// página con /og delante (/og/kaketiana/lexicon/aburi es la de esa voz); la
// de la radio es /og/curiana. Todas se dibujan al compilar: ninguna se pinta
// por pedido, y una ruta que no está aquí es 404.
export const dynamic = "force-static";
export const dynamicParams = false;

type Dibujo = () => Response;

async function registro(): Promise<Map<string, Dibujo>> {
  const r = new Map<string, Dibujo>();
  const sal = (rotulo: string, titulo: string, bajada: string | undefined, pie: string) => () =>
    tarjetaSal({ rotulo, titulo, bajada, pie });

  // La radio, en la noche
  r.set("curiana", () =>
    tarjetaNoche({
      rotulo: "88.8 FM · transmisión desde Abya Yala",
      titulo: "Curiana Radio",
      bajada: "Una transmisión al mes: música, ensayo, una lengua que renace y el arte del camino.",
    }),
  );
  r.set("archivo", () =>
    tarjetaNoche({
      rotulo: "Curiana Radio · archivo",
      titulo: "Archivo de transmisiones",
      bajada: "Cada edición es una frecuencia única.",
      pie: "curianaradio.com/archivo",
    }),
  );
  r.set("galeria", () =>
    tarjetaNoche({
      rotulo: "Curiana Radio · galería",
      titulo: "Galería",
      bajada: "Experimentos visuales generados con IA, con su prompt y su procedencia a la vista.",
      pie: "curianaradio.com/galeria",
    }),
  );
  r.set("jai-sounds", () =>
    tarjetaNoche({
      rotulo: "Curiana Radio · curaduría musical",
      titulo: "JAI Sounds",
      bajada: "jai · caquetío · oír, escuchar. Un dial de estaciones que gira de color, no de canciones.",
      pie: "curianaradio.com/jai-sounds",
    }),
  );
  for (const e of await getAllEditions()) {
    r.set(e.slug, () =>
      tarjetaNoche({
        rotulo: `Transmisión #${e.number}`,
        titulo: e.title,
        bajada: recortar(e.description, 120),
        pie: `curianaradio.com/${e.slug}`,
      }),
    );
  }

  // Kaketiana, en la sal
  const k = "curianaradio.com/kaketiana";
  r.set(
    "kaketiana",
    sal("Kaketiana · el lugar de la gente", "Qué sabemos del pueblo caquetío del Golfete de Coro", "Siglos XIV–XV. Cada afirmación con su fuente.", k),
  );
  for (const [seccion, info] of Object.entries(SECCIONES_WIKI)) {
    r.set(`kaketiana/${seccion}`, sal("Kaketiana", info.label, info.desc, `${k}/${seccion}`));
  }
  for (const p of getWikiIndice()) {
    r.set(
      `kaketiana/${p.seccion}/${p.slug}`,
      sal(`Kaketiana · ${SECCIONES_WIKI[p.seccion].label}`, p.titulo, undefined, `${k}/${p.seccion}`),
    );
  }
  const seed = getFichasSeed();
  r.set(
    "kaketiana/lexicon",
    sal(
      "Kaketiana · el diccionario",
      "La lengua, palabra por palabra",
      `${seed.n} voces caquetías, cada una con la marca de cómo la sabemos y su fuente.`,
      `${k}/lexicon`,
    ),
  );
  for (const f of getFichas()) {
    const cita = f.citas[0];
    r.set(`kaketiana/lexicon/${f.slug}`, () =>
      tarjetaVoz({
        forma: f.forma,
        glosa: recortar(f.glosa, 90),
        capa: f.capa,
        etiquetaCapa: CAPA[f.capa].label,
        categoria: f.categoria,
        fuente: cita ? [cita.titulo, ...cita.localizadores.slice(0, 1)].join(", ") : null,
      }),
    );
  }
  r.set(
    "kaketiana/bibliografia",
    sal("Kaketiana · bibliografía", "Las obras sobre las que se sostiene todo lo demás", "Crónicas, glosarios, arqueología y lingüística comparada.", `${k}/bibliografia`),
  );
  r.set(
    "kaketiana/no-sabemos",
    sal("Kaketiana", "Lo que no sabemos", "Las preguntas que el proyecto no ha podido cerrar, con lo que hay medido hasta hoy.", `${k}/no-sabemos`),
  );
  r.set(
    "kaketiana/experimento",
    sal("Kaketiana · el experimento", "Una lengua hablada de nuevo", "Agentes que hablan caquetío reconstruido, y lo que emerge cuando lo hacen.", `${k}/experimento`),
  );
  r.set(
    "kaketiana/personajes",
    sal("Kaketiana · el experimento", "Personajes", "Las voces curadas de la Curiana y cómo cambió su lengua.", `${k}/personajes`),
  );
  r.set(
    "kaketiana/neologisms",
    sal("Kaketiana · el experimento", "Neologismos", "Las palabras que los agentes inventaron: cuáles prendieron y cuáles murieron.", `${k}/neologisms`),
  );
  for (const p of getAllPersonajes()) {
    r.set(
      `kaketiana/personajes/${p.slug}`,
      sal("Kaketiana · personaje del experimento", p.nombre, p.rol_comunidad ? recortar(p.rol_comunidad, 110) : undefined, `${k}/personajes`),
    );
  }
  return r;
}

export async function generateStaticParams() {
  return [...(await registro()).keys()].map((clave) => ({ ruta: clave.split("/") }));
}

export async function GET(_req: Request, { params }: { params: Promise<{ ruta: string[] }> }) {
  const { ruta } = await params;
  const dibujo = (await registro()).get(ruta.join("/"));
  if (!dibujo) return new Response(`Sin tarjeta en ${SITIO.url}/og/${ruta.join("/")}`, { status: 404 });
  return dibujo();
}
