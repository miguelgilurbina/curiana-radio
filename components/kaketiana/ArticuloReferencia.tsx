import type { WikiPagina } from "@/types/wiki";
import { getVecinos } from "@/lib/wiki";
import { enlazarVoces } from "@/lib/fichas";
import { pieDeCitaAparte, seccionesDe } from "@/lib/articulo";
import { Overline } from "@/components/simulador/ui";
import { WikiProse } from "@/components/simulador/wiki-mdx";
import Sumario from "@/components/kaketiana/Sumario";
import MigaArticulo from "@/components/kaketiana/MigaArticulo";
import { obrasCitadas, SeguirLeyendo, SobreQueSeSostiene } from "@/components/kaketiana/PieDeArticulo";

// El artículo de la lengua, del manual de Kaketiana (Vistas §03; móvil en
// Sistema §06): obra de consulta, «se consulta, no se lee». Ancho completo,
// sin capitular y sin ceremonia; el sumario va plegado arriba porque son
// notas largas que se recorren por sección. Las tablas —una de cada cinco
// líneas— son las .kt del manual y en móvil se vuelven fichas, y la forma
// caquetía va como la escribe el comparatista (wiki-mdx.tsx).

export default function ArticuloReferencia({ pagina }: { pagina: WikiPagina }) {
  const { anterior, siguiente } = getVecinos("lengua", pagina.slug);
  const cuerpo = pieDeCitaAparte(enlazarVoces(pagina.cuerpo));
  const secciones = seccionesDe(cuerpo);
  const obras = obrasCitadas(cuerpo, pagina.fuentes);

  return (
    <>
      <MigaArticulo
        seccion={{ label: "La lengua", href: "/kaketiana/lengua" }}
        titulo={pagina.titulo}
        derecha="Referencia · se consulta, no se lee"
        derechaMovil="Referencia"
      />

      <article className="mt-10 sm:mt-12">
        <header>
          <Overline>La lengua · referencia</Overline>
          <h1 className="sim-display mt-3 max-w-[30ch] text-[1.9rem] font-semibold leading-[1.05] tracking-tight text-(--sim-ink) sm:text-[2.6rem]">
            {pagina.titulo}
          </h1>
        </header>

        {secciones.length > 0 && (
          <div className="mt-8">
            <Sumario secciones={secciones} plegado />
          </div>
        )}

        <WikiProse source={cuerpo} variante="referencia" className="mt-10" />

        <div className="max-w-reading">
          <SobreQueSeSostiene obras={obras} className="mt-16" />
          <SeguirLeyendo
            className="mt-14"
            siguiente={
              siguiente
                ? { href: `/kaketiana/lengua/${siguiente.slug}`, etiqueta: "Siguiente", titulo: siguiente.titulo }
                : { href: "/kaketiana/lexicon", etiqueta: "Sigue con", titulo: "El diccionario" }
            }
            anterior={anterior ? { href: `/kaketiana/lengua/${anterior.slug}`, titulo: anterior.titulo } : null}
          />
        </div>
      </article>
    </>
  );
}
