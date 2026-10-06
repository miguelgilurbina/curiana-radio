import Link from "next/link";
import type { Metadata } from "next";
import { getWikiPorSeccion, getCifrasWiki } from "@/lib/wiki";
import { getFichasSeed } from "@/lib/fichas";
import { getSerie, brazo } from "@/lib/serie";
import { getMapa } from "@/lib/mapa";
import { ESTILO_NIVEL } from "@/lib/mapa-estilo";
import HeroPalabra from "@/components/kaketiana/HeroPalabra";
import { SCRIPT_HERO } from "@/lib/kaketiana-hero";
import MapaKaketiana from "@/components/kaketiana/MapaKaketiana";
import Etiqueta from "@/components/kaketiana/Etiqueta";
import SenalesDeArista from "@/components/senales/SenalesDeArista";

export const metadata: Metadata = {
  title: "Kaketiana — el mundo del kaketío | Curiana Radio",
  description:
    "Qué sabemos del pueblo caquetío del Golfete de Coro, siglos XIV-XV: cómo vivían, en qué creían, y cómo suena una lengua que nadie habla desde hace cuatrocientos años. Cada afirmación con su fuente.",
};

// La portada del manual de Kaketiana (design_handoff_kaketiana, Vistas §01 y
// hero 1a): placa clara 6b «Sal y almagre», la etimología como hero, el mapa
// del territorio, tres cifras, las dos puertas y la franja del experimento.
// Nada más: las listas de artículos viven en /kaketiana/pueblo y
// /kaketiana/lengua (decisión de Miguel, 2026-09-30: la portada estaba
// sobrecargada). Las cifras se miden, no se escriben a mano (regla 1).

function Cifra({ label, valor, sub }: { label: string; valor: number | string; sub: string }) {
  return (
    <div className="border-t border-(--sim-rule) pt-3">
      <span className="kk-label block text-[0.6rem] text-(--sim-ink-soft)">{label}</span>
      <span className="sim-display mt-1 block text-3xl font-semibold leading-none text-(--sim-ink)">{valor}</span>
      <span className="mt-1.5 block font-sans text-xs leading-snug text-(--sim-ink-soft)">{sub}</span>
    </div>
  );
}

function Puerta({
  href,
  overline,
  titulo,
  items,
  accion,
}: {
  href: string;
  overline: string;
  titulo: string;
  items: string[];
  accion: string;
}) {
  return (
    <Link
      href={href}
      className="group flex flex-col gap-3 border border-(--sim-rule) p-6 transition-colors duration-300 hover:border-(--sim-rubrica)"
    >
      <span className="kk-label text-[0.6rem] text-(--sim-ink-soft)">{overline}</span>
      <span className="sim-display text-2xl font-semibold text-(--sim-ink)">{titulo}</span>
      <ul className="flex flex-col gap-1.5 font-sans text-sm text-(--sim-ink-soft)">
        {items.map((i) => (
          <li key={i}>{i}</li>
        ))}
      </ul>
      <span className="kk-label mt-auto pt-2 text-[0.66rem] text-(--sim-rubrica)">{accion}</span>
    </Link>
  );
}

export default function KaketianaPage() {
  const cifras = getCifrasWiki();
  const pueblo = getWikiPorSeccion("pueblo");
  const lengua = getWikiPorSeccion("lengua");
  const fichas = getFichasSeed();
  const serie = getSerie();
  const escena = serie ? brazo(serie, "escena") : undefined;
  const mapa = getMapa();

  return (
    <div>
      {/* Corre antes de pintar el hero: ver SCRIPT_HERO */}
      <script dangerouslySetInnerHTML={{ __html: SCRIPT_HERO }} />

      <div className="mx-auto max-w-6xl px-4 pb-20 pt-10 sm:px-6 md:pt-14 lg:px-8">
        <p className="kk-label text-(--sim-rubrica)">Un wiki de investigación · Golfete de Coro · s. XIV–XV</p>

        {/* El hero y el mapa, lado a lado */}
        <div className="mt-6 grid grid-cols-1 gap-12 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,1fr)] lg:gap-14">
          <HeroPalabra />

          <div className="flex flex-col gap-5">
            {mapa && mapa.puntos.length > 0 && (
              <figure>
                <div className="relative h-[300px] overflow-hidden border border-(--sim-rule) bg-(--sim-paper-deep) md:h-[380px]">
                  <MapaKaketiana puntos={mapa.puntos} />
                  {/* La etiqueta y la marca van dentro del marco (manual) */}
                  <span className="pointer-events-none absolute right-2.5 top-2.5 z-[1000]">
                    <Etiqueta grado="rec" corta className="bg-(--sim-paper)" />
                  </span>
                  <span className="pointer-events-none absolute bottom-2 left-2.5 z-[1000] kk-label bg-(--sim-paper)/85 px-1.5 text-[0.52rem] tracking-[0.18em] text-(--sim-ink-soft)">
                    Kaketiana · datos propios
                  </span>
                </div>
                <figcaption className="mt-2.5 flex flex-col gap-2">
                  <span className="sim-mono text-[0.68rem] text-(--sim-ink-soft)">
                    {mapa.resumen.toponimos_con_lugar} de {mapa.resumen.toponimos_canon} topónimos del canon
                    tienen lugar en el mapa de hoy · {mapa.resumen.puntos} puntos
                  </span>
                  <span className="flex flex-wrap gap-x-4 gap-y-1 font-sans text-xs text-(--sim-ink-soft)">
                    {(["A", "B", "C", "sin"] as const).map((n) => {
                      const e = ESTILO_NIVEL[n];
                      return (
                        <span key={n} className="inline-flex items-center gap-1.5">
                          <svg width="12" height="12" aria-hidden="true">
                            <circle
                              cx="6"
                              cy="6"
                              r="4.5"
                              fill={e.relleno}
                              fillOpacity={e.opacidad}
                              stroke="#b06a1c"
                              strokeWidth="1.5"
                              strokeDasharray={e.trazo}
                            />
                          </svg>
                          {n === "sin" ? e.etiqueta : `${n} · ${e.etiqueta}`} ({mapa.resumen.por_nivel[n]})
                        </span>
                      );
                    })}
                  </span>
                  <span className="font-sans text-xs leading-relaxed text-(--sim-ink-soft)">
                    El trazo mide la lectura del nombre, no su existencia: todos están en el canon y en el mapa de
                    hoy, ubicados con OpenStreetMap. Los que no tienen lectura dicen por qué al pasar sobre ellos.
                  </span>
                </figcaption>
              </figure>
            )}

            <p className="font-serif text-base italic leading-relaxed text-(--sim-ink-soft)">
              Semiárido siempre: médanos, cardones, cujíes. Tierra pobre, mar rico. Nada de selva.
            </p>

            <div className="grid grid-cols-3 gap-4">
              <Cifra
                label="Artículos"
                valor={cifras.articulos}
                sub={`${pueblo.length} pueblo · ${lengua.length} lengua`}
              />
              <Cifra label="Obras citadas" valor={cifras.obras} sub={`${cifras.conLectura} se leen en línea`} />
              {serie?.elenco && (
                <Cifra label="Voces simuladas" valor={serie.elenco.total} sub="sólo en el experimento" />
              )}
            </div>
          </div>
        </div>

        {/* Las dos puertas */}
        <div className="mt-16 grid grid-cols-1 gap-5 md:grid-cols-2">
          <Puerta
            href="/kaketiana/pueblo"
            overline={`El pueblo · ${pueblo.length} artículos · ensayo`}
            titulo="Preguntas de fondo"
            items={pueblo.slice(0, 4).map((p) => p.titulo.split(" — ")[0].split(":")[0])}
            accion="Leer →"
          />
          <Puerta
            href="/kaketiana/lengua"
            overline={`La lengua · ${lengua.length} artículos · referencia`}
            titulo="Obra de consulta"
            items={[
              ...(fichas.n > 0 ? [`El diccionario · ${fichas.n} voces`] : []),
              ...lengua.slice(0, 3).map((p) => p.titulo.split(" — ")[0]),
            ]}
            accion="Consultar →"
          />
        </div>
        <p className="mt-4 font-sans text-sm text-(--sim-ink-soft)">
          También:{" "}
          <Link href="/kaketiana/no-sabemos" className="text-(--kk-extra) hover:text-(--sim-rubrica)">
            lo que no sabemos
          </Link>{" "}
          ·{" "}
          <Link href="/kaketiana/bibliografia" className="text-(--kk-extra) hover:text-(--sim-rubrica)">
            la bibliografía
          </Link>
        </p>

        {/* Lo que Miguel escribe con la arista Kaketiana: su voz, no el canon */}
        <SenalesDeArista arista="kaketiana" className="mt-16" />
      </div>

      {/* La franja del experimento: ya es del otro lado del umbral */}
      <Link href="/kaketiana/experimento" data-sim-acto="laboratorio" className="group block bg-(--sim-paper)">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-6 gap-y-3 px-4 py-7 sm:px-6 lg:px-8">
          <span className="kk-accion text-[0.75rem]">[ EXPERIMENTO ]</span>
          <span className="font-sans text-sm text-(--sim-ink-soft)">
            {serie?.elenco ? `${serie.elenco.total} voces simuladas` : "Voces simuladas"}
            {escena ? `, ${escena.dias} días en Paraguaná` : ""}: ficción declarada, del otro lado del umbral.
          </span>
          <span className="hidden flex-1 sm:block" />
          <Etiqueta grado="canon" />
        </div>
      </Link>
    </div>
  );
}
