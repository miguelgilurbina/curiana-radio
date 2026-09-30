// Las piezas de la era 2 en la página del experimento: los hallazgos de una
// serie de dos brazos y los nombres que cada brazo le puso a lo nuevo. Todo
// número sale de content/simulador/series/<serie>.json (lib/serie.ts); aquí
// sólo se decide cómo se dice.
import type { ReactNode } from "react";
import {
  brazo,
  dec,
  decConSigno,
  formaLimpia,
  nombreDeConcepto,
  ventajaEscena,
  type BrazoSerie,
  type DisputaSerie,
  type SerieSeed,
} from "@/lib/serie";

const COLOR_ESCENA = "#8d83e8";
const COLOR_CONTROL = "#b09880";

function N({ children }: { children: ReactNode }) {
  return <span className="sim-mono whitespace-nowrap font-semibold text-(--sim-ink)">{children}</span>;
}

function Hallazgo({ n, titulo, children }: { n: number; titulo: string; children: ReactNode }) {
  return (
    <li className="border-t border-(--sim-rule) pt-5">
      <div className="flex items-baseline gap-3">
        <span className="sim-mono text-xs tabular-nums text-(--sim-ink-faint)">{String(n).padStart(2, "0")}</span>
        <h4 className="sim-display text-xl font-semibold text-(--sim-ink)">{titulo}</h4>
      </div>
      <p className="mt-2 max-w-reading pl-7 font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
        {children}
      </p>
    </li>
  );
}

function primero(b: BrazoSerie, clave: "acumulada" | "brecha") {
  return b.serie.find((p) => p[clave] != null)?.[clave] ?? null;
}
function ultimo(b: BrazoSerie, clave: "acumulada" | "brecha") {
  return [...b.serie].reverse().find((p) => p[clave] != null)?.[clave] ?? null;
}

export function HallazgosSerie({ seed }: { seed: SerieSeed }) {
  const e = brazo(seed, "escena");
  const c = brazo(seed, "control");
  if (!e || !c) return null;
  const ventaja = ventajaEscena(seed);
  const capE = seed.capubana.emergente_dia.escena;
  const capC = seed.capubana.emergente_dia.control;
  const bajanE = seed.capubana.bajan.escena;
  const bajanC = seed.capubana.bajan.control;
  const mismoVeredicto = e.veredicto.codigo === c.veredicto.codigo;

  return (
    <ol className="mt-10 space-y-8">
      <Hallazgo n={1} titulo={mismoVeredicto ? "La lengua común avanza y se estanca, con y sin mapa" : "La lengua común avanza"}>
        Contando todo lo dicho, la distancia entre las maneras de hablar cae de{" "}
        <N>{dec(primero(e, "acumulada"))}</N> a <N>{dec(ultimo(e, "acumulada"))}</N> con escena y de{" "}
        <N>{dec(primero(c, "acumulada"))}</N> a <N>{dec(ultimo(c, "acumulada"))}</N> en el control. Pero
        en la lectura exigente, la que sólo cuenta palabras nuevas, las dos curvas tocan fondo
        {e.emergente_min && c.emergente_min && (
          <>
            {" "}(el día <N>{e.emergente_min.dia}</N> con escena, el <N>{c.emergente_min.dia}</N> en el
            control)
          </>
        )}{" "}
        y después suben. {mismoVeredicto && (
          <>
            El veredicto del instrumento es el mismo en los dos: <em>{e.veredicto.mensaje}</em>. Si pasa
            con mapa y sin él, no es del mapa: es del motor, de lo que se enseña, del modelo o del ritmo
            de cosas nuevas.
          </>
        )}
      </Hallazgo>

      {ventaja && (
        <Hallazgo n={2} titulo="El mapa mantiene viva la variación">
          La distancia entre palabras nuevas del brazo con escena queda por encima de la del control{" "}
          <N>{ventaja.dias} de {ventaja.de}</N> días, en promedio <N>{decConSigno(ventaja.media, 3)}</N>.
          Cuando cada quien vive en su lugar y oye a quien tiene cerca, lo que se inventa se parece
          menos entre sí.
        </Hallazgo>
      )}

      <Hallazgo n={3} titulo="Cada pueblo empieza a hablar a su manera, pero sólo con mapa">
        La brecha entre pueblos mide cuánto más se parecen dos personas del mismo pueblo que dos de
        pueblos distintos. Es pequeña, pero con escena crece de <N>{decConSigno(primero(e, "brecha"))}</N> a{" "}
        <N>{decConSigno(ultimo(e, "brecha"))}</N>; en el control se cierra, de{" "}
        <N>{decConSigno(primero(c, "brecha"))}</N> a <N>{decConSigno(ultimo(c, "brecha"))}</N>. Con escena,{" "}
        <N>{e.formas.no_cruzaron}</N> palabras nuevas nunca salieron del pueblo donde nacieron; en el
        control, <N>{c.formas.no_cruzaron}</N>.
      </Hallazgo>

      {capE && capC && bajanE && bajanC && (
        <Hallazgo n={4} titulo="El día de Capubana se nota">
          Los días en que todos suben al cerro, la distancia entre palabras nuevas de ese día baja a{" "}
          <N>{dec(capE.capubana, 3)}</N>, contra <N>{dec(capE.resto, 3)}</N> el resto de los días, y{" "}
          <N>{bajanE.bajan} de {bajanE.de}</N> quedan por debajo del día anterior. En el control, los
          mismos días no se distinguen (<N>{dec(capC.capubana, 3)}</N> contra <N>{dec(capC.resto, 3)}</N>,{" "}
          <N>{bajanC.bajan} de {bajanC.de}</N>, lo que da el azar): allí no hay reunión. Es el placebo.
        </Hallazgo>
      )}
    </ol>
  );
}

// ── La misma cosa, dos nombres ─────────────────────────────────────────

function Celda({ d, minimo }: { d: DisputaSerie | undefined; minimo: number | null }) {
  if (!d) return <span className="text-(--sim-ink-faint)">—</span>;
  if (d.fijada) {
    return (
      <span>
        <span className="font-serif text-base italic text-(--sim-ink)">{formaLimpia(d.fijada)}</span>
        <span className="sim-mono ml-2 text-[0.7rem] text-(--sim-ink-faint)">
          fijada el día {d.fijada_dia} · entre {d.n_variantes} variantes
        </span>
      </span>
    );
  }
  const [a, b] = d.rivales;
  if (!a || (minimo != null && a.soporte < minimo)) {
    return <span className="font-sans text-xs text-(--sim-ink-faint)">todavía sin nombre</span>;
  }
  if (d.n_variantes === 1) {
    return (
      <span>
        <span className="font-serif text-base italic text-(--sim-ink-soft)">{formaLimpia(a.forma)}</span>
        <span className="sim-mono ml-2 text-[0.7rem] text-(--sim-ink-faint)">sin rival, sin fijar †</span>
      </span>
    );
  }
  return (
    <span>
      <span className="font-sans text-[0.7rem] uppercase tracking-[0.12em] text-(--sim-rubrica)">en disputa</span>{" "}
      <span className="font-serif italic text-(--sim-ink-soft)">{formaLimpia(a.forma)}</span>
      {b && (
        <>
          <span className="text-(--sim-ink-faint)"> contra </span>
          <span className="font-serif italic text-(--sim-ink-soft)">{formaLimpia(b.forma)}</span>
        </>
      )}
      <span className="sim-mono ml-2 text-[0.7rem] text-(--sim-ink-faint)">{d.n_variantes} variantes</span>
    </span>
  );
}

export function NombresDeLaSerie({ seed }: { seed: SerieSeed }) {
  const e = brazo(seed, "escena");
  const c = brazo(seed, "control");
  if (!e?.competencia || !c?.competencia) return null;
  const deControl = new Map(c.competencia.lista.map((d) => [d.concepto, d]));
  const minimo = e.competencia.soporte_minimo;
  const hayUnanime = [...e.competencia.lista, ...c.competencia.lista].some(
    (d) => !d.fijada && d.n_variantes === 1,
  );

  return (
    <div>
      <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
        Cada dos días el mundo les puso delante algo sin nombre. Los dos brazos vieron lo mismo, en el
        mismo orden y con las mismas semillas, y aun así casi nunca lo nombraron igual. Con escena la
        comunidad fijó <N>{e.competencia.fijados}</N> de <N>{e.competencia.referentes}</N>; en el
        control, <N>{c.competencia.fijados}</N>. Las que no se fijan no se resuelven: se acumulan.
      </p>

      <div className="mt-6 overflow-x-auto">
        <table className="w-full min-w-[560px] border-collapse text-left">
          <thead>
            <tr className="border-b border-(--sim-rule)">
              <th className="py-2 pr-4 font-sans text-[0.7rem] font-medium uppercase tracking-[0.14em] text-(--sim-ink-faint)">
                Lo que llegó
              </th>
              <th className="py-2 pr-4 font-sans text-[0.7rem] font-medium uppercase tracking-[0.14em]" style={{ color: COLOR_ESCENA }}>
                Con escena
              </th>
              <th className="py-2 font-sans text-[0.7rem] font-medium uppercase tracking-[0.14em]" style={{ color: COLOR_CONTROL }}>
                Control
              </th>
            </tr>
          </thead>
          <tbody>
            {e.competencia.lista.map((d) => (
              <tr key={d.concepto} className="border-b border-(--sim-rule)/60 align-top">
                <td className="py-3 pr-4">
                  <span className="font-sans text-sm font-semibold text-(--sim-ink)">
                    {nombreDeConcepto(d.concepto)}
                  </span>
                  <span className="mt-0.5 block max-w-[16rem] font-sans text-xs leading-snug text-(--sim-ink-faint)">
                    {d.descripcion}
                  </span>
                </td>
                <td className="py-3 pr-4">
                  <Celda d={d} minimo={minimo} />
                </td>
                <td className="py-3">
                  <Celda d={deControl.get(d.concepto)} minimo={c.competencia?.soporte_minimo ?? null} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-3 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
        Una forma se fija cuando reúne más del{" "}
        {e.competencia.umbral != null ? `${Math.round(e.competencia.umbral * 100)} %` : "umbral"} del
        apoyo, que suma cuántas veces se dijo y el prestigio de quien la dijo.
        {hayUnanime &&
          " † Un nombre sin rival nunca se fija, porque la regla pide al menos dos variantes: es un defecto anotado del instrumento, no una decisión de la comunidad."}{" "}
        Las formas se muestran sin las marcas de formato que el modelo a veces les pega.
      </p>
    </div>
  );
}
