import { getAllEditions } from "@/lib/content";
import { getFichas, getFichasSeed } from "@/lib/fichas";
import { CAPAS_EPISTEMICAS } from "@/lib/sim-theme";
import { SITIO, urlAbsoluta } from "@/lib/seo";
import { getWikiGenerado, getWikiIndice, getWikiPagina } from "@/lib/wiki";
import { SECCIONES_WIKI, type SeccionWiki } from "@/types/wiki";
import type { CitaFicha } from "@/types/fichas";

// ── /llms.txt y /llms-full.txt: el sitio contado a un agente ──────────
// El formato es el de llmstxt.org: un markdown con el resumen del sitio y
// enlaces curados. Lo importante no son los enlaces sino las instrucciones de
// lectura: un agente que cita una voz caquetía sin su capa epistémica dice
// algo que el proyecto no dice. Todo sale de los mismos JSON que las páginas;
// aquí no se escribe ninguna cifra.

function cita(c: CitaFicha): string {
  return c.localizadores.length ? `${c.titulo}, ${c.localizadores.join(", ")}` : c.titulo;
}

function cabecera(): string {
  const seed = getFichasSeed();
  const capas = CAPAS_EPISTEMICAS.map(
    (c) => `- **${c.label}** (${seed.por_capa[c.key]} voces): ${seed.capas[c.key].que_es} Lo incierto: ${seed.capas[c.key].incierto}`,
  ).join("\n");
  return `# ${SITIO.nombre}

> ${SITIO.nombre} (${SITIO.lema}) es un proyecto cultural venezolano: una transmisión al mes de música, ensayo, una lengua que renace y arte, emitida desde una Paraguaná paralela. Su eje de investigación es Kaketiana, un wiki sobre el pueblo caquetío del Golfete de Coro (siglos XIV–XV) y la reconstrucción de su lengua, que nadie habla desde hace unos cuatrocientos años.

## Cómo leer y citar este sitio

El caquetío no tiene hablantes ni gramática documentada: se conservan voces sueltas en crónicas, glosarios y topónimos, y lo demás se reconstruye. Por eso cada voz del diccionario lleva una capa epistémica, y citarla sin la capa cambia lo que dice. Las capas, de lo documentado a lo conjeturado:

${capas}

- Una voz **reconstruida, retroabstraída o hipotética no es una palabra documentada del caquetío**: si la usas, di cuál es su capa. Donde hay forma atestiguada, la reconstruida se retira del uso.
- Cada afirmación del wiki lleva su fuente con página; la bibliografía tiene cada obra con su ancla.
- Las crónicas son posteriores al contacto (siglo XVI en adelante): describen el mundo colonial, no necesariamente el de antes. No tomes un dato colonial como norma precolombina salvo que el artículo lo proyecte.
- **El experimento** es una simulación: agentes de IA que conversan en caquetío reconstruido. Sus neologismos y sus personajes son producto de la simulación, no datos históricos.
- **La galería** son imágenes generadas con IA, y cada ficha lo declara con la herramienta y el prompt.
- Citar con enlace a la página de la voz o del artículo.
`;
}

function enlace(titulo: string, ruta: string, nota?: string): string {
  return `- [${titulo}](${urlAbsoluta(ruta)})${nota ? `: ${nota}` : ""}`;
}

export async function llmsTxt(): Promise<string> {
  const seed = getFichasSeed();
  const articulos = (s: SeccionWiki) =>
    getWikiIndice()
      .filter((p) => p.seccion === s)
      .sort((a, b) => a.orden - b.orden)
      .map((p) => enlace(p.titulo, `/kaketiana/${s}/${p.slug}`))
      .join("\n");
  const ediciones = (await getAllEditions())
    .map((e) => enlace(`#${e.number}: ${e.title}`, `/${e.slug}`, e.description))
    .join("\n");

  return `${cabecera()}
## Kaketiana — ${SECCIONES_WIKI.pueblo.label.toLowerCase()}

${enlace("Kaketiana", "/kaketiana", "la portada del wiki: el territorio, las cifras y las dos puertas")}
${enlace(SECCIONES_WIKI.pueblo.label, "/kaketiana/pueblo", SECCIONES_WIKI.pueblo.desc)}
${articulos("pueblo")}

## Kaketiana — ${SECCIONES_WIKI.lengua.label.toLowerCase()}

${enlace(SECCIONES_WIKI.lengua.label, "/kaketiana/lengua", SECCIONES_WIKI.lengua.desc)}
${articulos("lengua")}

## El diccionario y sus fuentes

${enlace("El diccionario", "/kaketiana/lexicon", `${seed.n} voces caquetías, cada una con su glosa, su capa y su fuente`)}
${enlace("El diccionario completo en texto", "/llms-full.txt", "todas las voces con su capa y su cita, y el texto de cada artículo")}
${enlace("Las voces retiradas", "/kaketiana/lexicon/retiradas", "lo que salió del habla y qué lo sustituye")}
${enlace("Bibliografía", "/kaketiana/bibliografia", "las obras sobre las que se sostiene todo lo demás")}
${enlace("Lo que no sabemos", "/kaketiana/no-sabemos", "las preguntas abiertas, con lo medido hasta hoy")}

## El experimento

${enlace("El experimento", "/kaketiana/experimento", "una lengua hablada de nuevo por agentes de IA, y lo que emerge")}
${enlace("La era 1", "/kaketiana/experimento/era-1", "cómo se construyó el motor (pruebas de desarrollo, no resultados)")}
${enlace("Neologismos", "/kaketiana/neologisms", "palabras inventadas por los agentes durante la simulación")}
${enlace("Personajes", "/kaketiana/personajes", "las voces de la simulación")}

## La radio

${enlace("Inicio", "/inicio", SITIO.descripcion)}
${enlace("Archivo de transmisiones", "/archivo")}
${ediciones}
${enlace("JAI Sounds", "/jai-sounds", "la curaduría musical: jai es «oír, escuchar» en caquetío. Cada canción, álbum y artista del dial tiene su ficha (/jai-sounds/canciones/…, /albumes/…, /artistas/…), con datos de MusicBrainz y el extracto de Wikipedia citado; la reseña, cuando la hay, es la voz de JAI")}
${enlace("Descubriendo con Chocolate", "/jai-sounds/descubriendo", "el podcast de JAI Sounds")}
${enlace("Galería", "/galeria", "experimentos visuales generados con IA, con su procedencia")}

## Optional

${enlace("El repositorio", SITIO.repo, "el código, el lexicón y la bitácora del experimento son públicos")}
`;
}

/** Hace absolutos los enlaces del markdown del vault («](/kaketiana/…»). */
function absolutizar(md: string): string {
  return md.replace(/\]\(\//g, `](${SITIO.url}/`);
}

export function llmsFullTxt(): string {
  const seed = getFichasSeed();
  const voces = [...getFichas()]
    .sort((a, b) => a.forma.localeCompare(b.forma, "es"))
    .map((f) => {
      const capa = CAPAS_EPISTEMICAS.find((c) => c.key === f.capa)!.label;
      const fuentes = f.citas.length ? ` Fuente: ${f.citas.map(cita).join("; ")}.` : "";
      const cat = f.categoria ? ` (${f.categoria})` : "";
      return `- **${f.forma}**${cat} — «${f.glosa}». Voz ${capa}.${fuentes} ${urlAbsoluta(`/kaketiana/lexicon/${f.slug}`)}`;
    })
    .join("\n");

  const articulos = getWikiIndice()
    .map((e) => getWikiPagina(e.seccion, e.slug))
    .filter((p) => p !== null)
    .map(
      (p) => `---

# ${p.titulo}

${urlAbsoluta(`/kaketiana/${p.seccion}/${p.slug}`)} · Kaketiana, ${SECCIONES_WIKI[p.seccion].label.toLowerCase()}

${absolutizar(p.cuerpo).trim()}
`,
    )
    .join("\n");

  return `${cabecera()}
Exportado del vault el ${getWikiGenerado()} (artículos) y el ${seed.generado} (diccionario).

## El diccionario: ${seed.n} voces caquetías

${voces}

## Los artículos de Kaketiana

${articulos}`;
}
