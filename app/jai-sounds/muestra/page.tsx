import type { Metadata } from "next";
import { getMuestra } from "@/lib/jai-sounds-muestra";
import PropuestaEstacion from "@/components/jai-sounds/PropuestaEstacion";
import PropuestaMesa from "@/components/jai-sounds/PropuestaMesa";
import PropuestaFichas from "@/components/jai-sounds/PropuestaFichas";

// Ruta de trabajo: no debe indexarse ni aparecer en el sitemap. Los datos
// son falsos y confundirlos con el catálogo real sería el peor resultado.
export const metadata: Metadata = {
  title: "JAI Sounds — Propuestas (datos de muestra)",
  robots: { index: false, follow: false },
};

function Seccion({
  id,
  numero,
  titulo,
  tesis,
  children,
}: {
  id: string;
  numero: string;
  titulo: string;
  tesis: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-20">
      <header className="mb-6">
        <p className="font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-[0.3em] text-(--jai-luz-faint)">
          Propuesta {numero}
        </p>
        <h2 className="font-(family-name:--jai-display) text-3xl md:text-4xl mt-2">
          {titulo}
        </h2>
        <p className="mt-3 max-w-reading text-(--jai-luz-soft)">{tesis}</p>
      </header>
      {children}
    </section>
  );
}

export default function MuestraPage() {
  const { pistas, listas, fichas, albums, moods } = getMuestra();

  return (
    <div>
      {/* El aviso viaja con el scroll: en ningún momento se puede estar
          mirando esta pantalla sin saber que los datos son inventados. */}
      <div className="sticky top-16 z-40 bg-(--jai-senal) text-(--jai-noche)">
        <p className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-2 font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-[0.2em] font-bold">
          Datos de muestra · no es el catálogo · las notas no son curaduría
        </p>
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16 space-y-20">
        <header>
          <h1 className="font-(family-name:--jai-display) text-4xl md:text-6xl leading-[1.05]">
            Tres propuestas
          </h1>
          <p className="mt-5 max-w-reading text-body text-(--jai-luz-soft)">
            Maquetas funcionales sobre 24 pistas y 15 artistas inventados para
            este fin. Los nombres de artista y álbum son reales porque son
            metadatos; las notas curatoriales son relleno y los identificadores
            llevan prefijo <span className="font-(family-name:--jai-mono)">muestra-</span>{" "}
            para que jamás lleguen a la base de datos.
          </p>
          <nav className="mt-6 flex flex-wrap gap-3">
            {[
              ["#estacion", "A · Estación"],
              ["#mesa", "B · Mesa de curaduría"],
              ["#fichas", "C · Fichas y cruces"],
            ].map(([href, texto]) => (
              <a
                key={href}
                href={href}
                className="font-(family-name:--jai-mono) text-[0.7rem] uppercase tracking-widest border border-(--jai-rule) rounded-full px-4 py-1.5 text-(--jai-luz-soft) hover:border-(--jai-senal) hover:text-(--jai-senal) transition-colors"
              >
                {texto}
              </a>
            ))}
          </nav>
        </header>

        <Seccion
          id="estacion"
          numero="A"
          titulo="Estación"
          tesis="Cómo se muestra una playlist al público. La playlist no es una tabla, es un texto: la pista con nota curatorial ocupa más espacio y las demás se repliegan a una línea. Lo contrario de un reproductor — aquí lo que se lee vale más que lo que se reproduce."
        >
          <div className="grid gap-6 lg:grid-cols-2">
            {listas.slice(0, 2).map((lista) => (
              <PropuestaEstacion key={lista.id} lista={lista} />
            ))}
          </div>
        </Seccion>

        <Seccion
          id="mesa"
          numero="B"
          titulo="Mesa de curaduría"
          tesis="Cómo se gestionan las canciones. Con 12.000 pistas, una herramienta que solo lista no sirve: nadie navega 12.000 filas. Esta muestra el hueco — cuánto falta por asignar y anotar — y ordena por deuda curatorial, no alfabéticamente. Los filtros funcionan; editar todavía no escribe."
        >
          <PropuestaMesa pistas={pistas} moods={moods} />
        </Seccion>

        <Seccion
          id="fichas"
          numero="C"
          titulo="Fichas y cruces"
          tesis="Cómo se gestionan artistas y álbumes. Un directorio alfabético no dice nada que Spotify no diga ya; lo que este proyecto puede mostrar es dónde se cruzan. La ficha no lleva biografía: lleva géneros y vecinos, con lo compartido resaltado. Los álbumes van por década, para ver de un golpe si el catálogo está sesgado a un periodo."
        >
          <PropuestaFichas artistas={fichas} albums={albums} />
        </Seccion>
      </div>
    </div>
  );
}
