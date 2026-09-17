"use client";

// EL VISOR DE REPETICIÓN — quién estaba dónde, turno a turno, sobre Paraguaná.
//
// No simula: LEE. La escena la decidió el motor y está guardada en `presencias`
// (los 63 agentes en un lugar cada momento del día, no sólo los 12 que hablan);
// aquí se dibuja. Es el diseño de §5b del issue de la escena y la decisión 10 de
// Miguel del 2026-09-17 («sobre el mapa real, en /kaketiana, estático»), con el
// volcado de texto debajo como andamio.
//
// Datos: content/simulador/escena/*.json vía lib/escena.ts — cero egress, como
// todo lo demás de /kaketiana. Mapa: Leaflet (el sitio no traía librería de
// mapas; es la más ligera que no pide clave) sobre las teselas estándar de
// OpenStreetMap, que son las únicas realmente sin clave — las oscuras de CARTO
// ya estampan «API KEY REQUIRED». El registro oscuro del Acto I se consigue
// filtrando el panel de teselas en CSS (`.mapa-escena` en globals.css), que no
// toca ni los puntos ni las líneas: esos son SVG por encima.
//
// Y es un guardián: el día que el Director narre que las canoas volvieron al
// Golfete y en el mapa no haya nadie en el Golfete, se ve de un vistazo.

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type * as LeafletNS from "leaflet";
import "leaflet/dist/leaflet.css";
import type { EscenaSeed, EscenaDeLugar, LugarEscena } from "@/lib/escena";
import { NODOS, nodoColor } from "@/lib/sim-theme";
import { Card, Overline } from "./ui";

// Teselas sin clave, con la atribución que su licencia exige.
const TESELAS = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";
const ATRIBUCION =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';

// Los 16 lugares «heredados» comparten el punto de su aldea (el canon no les da
// uno propio y no se inventa: §5b). Dibujados encima unos de otros serían un
// solo punto imposible de pinchar, así que se abren en corona alrededor de su
// aldea. Es un recurso de dibujo, no geografía: se dice en la leyenda.
const RADIO_CORONA = 0.0125; // grados

function tamanoDelPunto(n: number): number {
  if (!n) return 3.5;
  return Math.min(4 + Math.sqrt(n) * 3.2, 22);
}

/** Coordenada de cada lugar, con los heredados abiertos en corona. */
function posiciones(lugares: LugarEscena[]): Map<string, [number, number]> {
  const pos = new Map<string, [number, number]>();
  const porPunto = new Map<string, LugarEscena[]>();

  for (const l of lugares) {
    if (l.lat == null || l.lon == null) continue;
    const clave = `${l.lat},${l.lon}`;
    const grupo = porPunto.get(clave) ?? [];
    grupo.push(l);
    porPunto.set(clave, grupo);
  }

  for (const grupo of porPunto.values()) {
    // El que tiene punto propio se queda donde el canon lo puso; los demás
    // salen a la corona, en orden alfabético para que no bailen entre turnos.
    const anclados = grupo.filter((l) => l.tipo === "propio" || l.tipo === "zona");
    const corona = grupo
      .filter((l) => !anclados.includes(l))
      .sort((a, b) => a.id.localeCompare(b.id));
    for (const l of anclados) pos.set(l.id, [l.lat!, l.lon!]);
    corona.forEach((l, i) => {
      const angulo = (2 * Math.PI * i) / Math.max(corona.length, 1) - Math.PI / 2;
      pos.set(l.id, [
        l.lat! + RADIO_CORONA * Math.sin(angulo),
        l.lon! + RADIO_CORONA * Math.cos(angulo) * 1.02,
      ]);
    });
  }
  return pos;
}

export default function MapaDeEscena({ seed }: { seed: EscenaSeed }) {
  const [i, setI] = useState(0);
  const [lugarSel, setLugarSel] = useState<string | null>(null);
  const [corriendo, setCorriendo] = useState(false);
  const [estado, setEstado] = useState<"cargando" | "listo" | "falla">("cargando");

  const contenedor = useRef<HTMLDivElement | null>(null);
  const mapa = useRef<LeafletNS.Map | null>(null);
  const capas = useRef<Map<string, LeafletNS.CircleMarker>>(new Map());

  const turno = seed.turnos[i] ?? null;
  const lugares = seed.lugares;
  const pos = useMemo(() => posiciones(lugares), [lugares]);
  const porId = useMemo(
    () => new Map(lugares.map((l) => [l.id, l])),
    [lugares]
  );
  const escenaDe = useMemo(() => {
    const m = new Map<string, EscenaDeLugar>();
    for (const e of turno?.escenas ?? []) m.set(e.lugar, e);
    return m;
  }, [turno]);

  const seleccion = lugarSel ? porId.get(lugarSel) ?? null : null;
  const escenaSel = lugarSel ? escenaDe.get(lugarSel) ?? null : null;

  // ── El mapa, una sola vez ───────────────────────────────────────────
  useEffect(() => {
    let vivo = true;
    let mapaLocal: LeafletNS.Map | null = null;
    let limpieza: (() => void) | null = null;
    // El Map de marcas, capturado aquí: en la limpieza `capas.current` ya puede
    // ser otro (react-hooks/exhaustive-deps lo avisa, y tiene razón).
    const marcas = capas.current;

    (async () => {
      try {
        const L = await import("leaflet");
        if (!vivo || !contenedor.current || mapa.current) return;

        mapaLocal = L.map(contenedor.current, {
          scrollWheelZoom: false,
          attributionControl: true,
        });
        L.tileLayer(TESELAS, { attribution: ATRIBUCION, maxZoom: 18 }).addTo(mapaLocal);

        // Las zonas de pesca no son un punto: son la línea de costa que tocan.
        // Los caminos cuyos dos extremos nombra el canon van de punta a punta.
        for (const l of lugares) {
          if (!l.puntos || l.puntos.length < 2) continue;
          L.polyline(l.puntos as LeafletNS.LatLngExpression[], {
            color: nodoColor(l.compartido ? "compartido" : l.nodo),
            weight: l.tipo === "camino" ? 2 : 1.5,
            opacity: 0.5,
            dashArray: l.tipo === "camino" ? "2 6" : "6 6",
          }).addTo(mapaLocal);
        }

        for (const l of lugares) {
          const p = pos.get(l.id);
          if (!p) continue;
          const marca = L.circleMarker(p, {
            radius: 3.5,
            color: l.compartido ? "#f3ead4" : nodoColor(l.nodo),
            weight: l.compartido ? 1.6 : 1,
            fillColor: nodoColor(l.nodo),
            fillOpacity: 0.55,
          })
            .bindTooltip(l.nombre, { direction: "top", opacity: 0.9 })
            .addTo(mapaLocal);
          marca.on("click", () => setLugarSel(l.id));
          marcas.set(l.id, marca);
        }

        // El encuadre se rehace cuando el contenedor ya tiene alto: si se
        // encuadra antes de que el CSS aterrice, Leaflet cree que el mapa mide
        // 0 y se queda en la vista del mundo entero.
        const puntos = [...pos.values()] as LeafletNS.LatLngExpression[];
        const limites = puntos.length ? L.latLngBounds(puntos).pad(0.12) : null;
        let encuadrado = false;
        const encuadrar = () => {
          if (!mapaLocal) return;
          mapaLocal.invalidateSize();
          // Sólo se encuadra mientras no se haya podido: después, la vista es
          // del lector (si arrastró o acercó, nadie se la mueve).
          if (encuadrado || !contenedor.current?.clientHeight) return;
          if (limites) mapaLocal.fitBounds(limites);
          else mapaLocal.setView([11.78, -70.02], 10);
          encuadrado = true;
        };
        encuadrar();

        mapa.current = mapaLocal;
        setEstado("listo");
        const reencuadre = setTimeout(encuadrar, 80);
        const observador =
          typeof ResizeObserver !== "undefined" ? new ResizeObserver(encuadrar) : null;
        if (observador && contenedor.current) observador.observe(contenedor.current);
        limpieza = () => {
          clearTimeout(reencuadre);
          observador?.disconnect();
        };
      } catch {
        // Sin mapa la escena se sigue leyendo: debajo está el volcado de texto.
        if (vivo) setEstado("falla");
      }
    })();

    return () => {
      vivo = false;
      limpieza?.();
      marcas.clear();
      mapa.current = null;
      mapaLocal?.remove();
    };
  }, [lugares, pos]);

  // ── Cada turno repinta los puntos: el tamaño es cuánta gente hay ────
  useEffect(() => {
    if (estado !== "listo") return;
    for (const l of lugares) {
      const marca = capas.current.get(l.id);
      if (!marca) continue;
      const escena = escenaDe.get(l.id);
      const n = escena?.n ?? 0;
      const contacto = escena?.contacto ?? false;
      const activo = l.id === lugarSel;
      marca.setRadius(tamanoDelPunto(n));
      marca.setStyle({
        color: activo
          ? "#f3ead4"
          : contacto || l.compartido
            ? nodoColor("compartido")
            : nodoColor(l.nodo),
        weight: activo ? 3 : contacto || l.compartido ? 2 : 1,
        fillColor: contacto ? nodoColor("compartido") : nodoColor(l.nodo),
        fillOpacity: n ? 0.7 : 0.18,
      });
      marca.setTooltipContent(n ? `${l.nombre} — ${n}` : l.nombre);
    }
  }, [estado, escenaDe, lugarSel, lugares]);

  // ── La repetición ───────────────────────────────────────────────────
  useEffect(() => {
    if (!corriendo || seed.turnos.length < 2) return;
    const t = setInterval(() => {
      setI((prev) => (prev + 1 >= seed.turnos.length ? 0 : prev + 1));
    }, 1600);
    return () => clearInterval(t);
  }, [corriendo, seed.turnos.length]);

  const mover = useCallback(
    (delta: number) => {
      setCorriendo(false);
      setI((prev) => Math.min(Math.max(prev + delta, 0), Math.max(seed.turnos.length - 1, 0)));
    },
    [seed.turnos.length]
  );

  const hayTurnos = seed.turnos.length > 0;
  const conGente = (turno?.escenas ?? []).filter((e) => e.n > 0);
  const contactos = conGente.filter((e) => e.contacto);

  return (
    <div className="mt-6">
      {/* ── El deslizador de turnos ─────────────────────────────────── */}
      {hayTurnos ? (
        <div className="flex flex-wrap items-center gap-3 rounded-t-2xl border border-b-0 border-(--sim-rule) bg-(--sim-paper-deep) px-4 py-3">
          <div className="flex items-center gap-1">
            <BotonTurno label="Turno anterior" onClick={() => mover(-1)} disabled={i === 0}>
              ‹
            </BotonTurno>
            <BotonTurno
              label={corriendo ? "Parar la repetición" : "Correr la repetición"}
              onClick={() => setCorriendo((v) => !v)}
              disabled={seed.turnos.length < 2}
            >
              {corriendo ? "❚❚" : "▶"}
            </BotonTurno>
            <BotonTurno
              label="Turno siguiente"
              onClick={() => mover(1)}
              disabled={i >= seed.turnos.length - 1}
            >
              ›
            </BotonTurno>
          </div>

          <div className="min-w-[13rem] font-sans text-sm text-(--sim-ink)">
            <span className="sim-display text-lg font-semibold">
              Día {turno?.dia ?? "—"}
            </span>
            <span className="mx-2 text-(--sim-rule)">·</span>
            <span className="text-(--sim-fuego)">{turno?.momento || `turno ${turno?.turno}`}</span>
            <span className="sim-mono ml-3 text-xs text-(--sim-ink-faint)">
              {turno?.n_presencias ?? 0} presencias · {conGente.length} escenas
            </span>
          </div>

          <input
            type="range"
            min={0}
            max={Math.max(seed.turnos.length - 1, 0)}
            value={i}
            aria-label="Turno del día"
            onChange={(e) => {
              setCorriendo(false);
              setI(Number(e.target.value));
            }}
            className="h-1 min-w-[10rem] flex-1 cursor-pointer appearance-none rounded-full bg-(--sim-rule) accent-(--sim-rubrica)"
          />

          <span className="sim-mono text-xs tabular-nums text-(--sim-ink-faint)">
            {i + 1}/{seed.turnos.length}
          </span>
        </div>
      ) : null}

      {/* ── El mapa ──────────────────────────────────────────────────── */}
      <div
        className={`relative overflow-hidden border border-(--sim-rule) ${
          hayTurnos ? "rounded-b-2xl" : "rounded-2xl"
        }`}
      >
        <div
          ref={contenedor}
          className="mapa-escena h-[380px] w-full bg-(--sim-paper-deep) md:h-[500px]"
          role="application"
          aria-label="Mapa de Paraguaná con la escena del turno"
        />
        {estado !== "listo" && (
          <div className="pointer-events-none absolute inset-0 flex items-center justify-center bg-(--sim-paper-deep)/80 px-6 text-center font-sans text-sm text-(--sim-ink-soft)">
            {estado === "cargando"
              ? "Levantando el mapa de Paraguaná…"
              : "El mapa no cargó. La escena se lee igual, en texto, aquí debajo."}
          </div>
        )}
      </div>

      {/* ── Leyenda ──────────────────────────────────────────────────── */}
      <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 font-sans text-xs text-(--sim-ink-faint)">
        {Object.entries(NODOS).map(([clave, { label, color }]) => (
          <span key={clave} className="inline-flex items-center gap-1.5">
            <span
              className="inline-block h-2.5 w-2.5 rounded-full"
              style={{ background: color }}
              aria-hidden="true"
            />
            {label}
          </span>
        ))}
        <span>El punto crece con la gente que hay.</span>
        <span>
          Los {lugares.filter((l) => l.tipo === "heredado").length} lugares sin punto propio se
          abren en corona alrededor de su aldea: el canon no les da coordenada y no se inventa.
        </span>
      </div>

      {/* ── El panel: quiénes están y qué dijeron ────────────────────── */}
      <div className="mt-5 grid gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1.15fr)]">
        <Card className="p-5">
          <Overline>{seleccion ? "El lugar" : "El turno"}</Overline>
          {seleccion ? (
            <>
              <h4 className="sim-display mt-1 text-xl font-semibold text-(--sim-ink)">
                {seleccion.nombre}
              </h4>
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <Pildora color={nodoColor(seleccion.nodo)}>
                  {NODOS[seleccion.nodo ?? ""]?.label ?? "sin nodo"}
                </Pildora>
                {seleccion.compartido && (
                  <Pildora color={nodoColor("compartido")}>compartido entre nodos</Pildora>
                )}
                {escenaSel?.contacto && (
                  <Pildora color={nodoColor("compartido")}>los dos nodos, ahora</Pildora>
                )}
                <span className="sim-mono text-xs text-(--sim-ink-faint)">
                  {escenaSel?.n ?? 0} presentes
                </span>
              </div>
              {seleccion.por_que && (
                <p className="mt-2 font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
                  {seleccion.por_que}
                </p>
              )}
              <ul className="mt-4 flex flex-wrap gap-1.5">
                {(escenaSel?.presentes ?? []).map((p) => (
                  <li
                    key={p.agente}
                    className={`inline-flex items-center gap-1.5 rounded-full border px-2 py-0.5 font-sans text-xs ${
                      p.hablo
                        ? "border-(--sim-fuego) text-(--sim-ink)"
                        : "border-(--sim-rule) text-(--sim-ink-soft)"
                    }`}
                    title={p.hablo ? "habló aquí este turno" : "estuvo aquí"}
                  >
                    <span
                      className="inline-block h-1.5 w-1.5 rounded-full"
                      style={{ background: nodoColor(p.nodo) }}
                      aria-hidden="true"
                    />
                    {p.agente}
                  </li>
                ))}
              </ul>
              {!escenaSel && (
                <p className="mt-3 font-sans text-sm text-(--sim-ink-soft)">
                  Nadie en este lugar a esta hora.
                </p>
              )}
              <button
                type="button"
                onClick={() => setLugarSel(null)}
                className="mt-4 font-sans text-xs text-(--sim-rubrica) underline underline-offset-4"
              >
                ver el turno entero
              </button>
            </>
          ) : (
            <>
              <h4 className="sim-display mt-1 text-xl font-semibold text-(--sim-ink)">
                {hayTurnos
                  ? `Día ${turno?.dia} · ${turno?.momento || `turno ${turno?.turno}`}`
                  : "Todavía no hay escena"}
              </h4>
              <p className="mt-2 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
                {hayTurnos
                  ? `${conGente.length} lugares con gente, ${contactos.length} con los dos nodos a la vez. Pincha un punto para ver quién está y qué dijo ahí.`
                  : "El mapa son los 29 lugares que la tabla de escena resolvió. Se llenará cuando corra el primer run con escena."}
              </p>
              {hayTurnos && (
                <ul className="mt-4 space-y-1.5">
                  {[...conGente]
                    .sort((a, b) => b.n - a.n)
                    .slice(0, 8)
                    .map((e) => (
                      <li key={e.lugar}>
                        <button
                          type="button"
                          onClick={() => setLugarSel(e.lugar)}
                          className="flex w-full items-center gap-2 text-left font-sans text-sm text-(--sim-ink-soft) hover:text-(--sim-ink)"
                        >
                          <span
                            className="inline-block h-2 w-2 shrink-0 rounded-full"
                            style={{
                              background: nodoColor(
                                e.contacto ? "compartido" : porId.get(e.lugar)?.nodo
                              ),
                            }}
                            aria-hidden="true"
                          />
                          <span className="min-w-0 flex-1 truncate">
                            {porId.get(e.lugar)?.nombre ?? e.lugar}
                          </span>
                          <span className="sim-mono shrink-0 text-xs tabular-nums text-(--sim-ink-faint)">
                            {e.n}
                            {e.dichos.length ? ` · ${e.dichos.length} voz` : ""}
                          </span>
                        </button>
                      </li>
                    ))}
                </ul>
              )}
            </>
          )}
        </Card>

        <Card className="p-5">
          <Overline>Lo que se dijo aquí</Overline>
          {escenaSel && escenaSel.dichos.length > 0 ? (
            <ul className="mt-3 space-y-4">
              {escenaSel.dichos.map((d) => (
                <li key={d.agente} className="border-l-2 border-(--sim-rule) pl-3">
                  <div className="flex items-center gap-1.5 font-sans text-xs text-(--sim-ink-faint)">
                    <span
                      className="inline-block h-1.5 w-1.5 rounded-full"
                      style={{ background: nodoColor(d.nodo) }}
                      aria-hidden="true"
                    />
                    {d.agente}
                  </div>
                  <p className="mt-1 font-serif text-[0.95rem] leading-relaxed text-(--sim-ink)">
                    «{d.texto}»
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-3 font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
              {seleccion
                ? "Aquí no habló nadie este turno. La ventana que habla son doce de los sesenta y tres; los demás estaban, y eso también es el dato."
                : "Pincha un lugar del mapa para leer lo que se dijo en él."}
            </p>
          )}
          {escenaSel && escenaSel.dichos.some((d) => d.recortado) && (
            <p className="mt-4 font-sans text-xs text-(--sim-ink-faint)">
              Las intervenciones van recortadas a {seed.tope_texto} caracteres; el texto entero
              vive en la base.
            </p>
          )}
        </Card>
      </div>

      {/* ── El andamio: la escena en texto ───────────────────────────── */}
      {hayTurnos && (
        <details className="mt-4 rounded-2xl border border-(--sim-rule) bg-(--sim-paper-deep) px-4 py-3">
          <summary className="cursor-pointer font-sans text-xs text-(--sim-ink-soft)">
            Ver la escena de este turno en texto
          </summary>
          <pre className="sim-mono mt-3 overflow-x-auto text-xs leading-relaxed text-(--sim-ink-soft)">
            {conGente
              .map((e) => `${e.lugar}: ${e.presentes.map((p) => p.agente).join(", ")}`)
              .join("\n") || "sin presencias en este turno"}
          </pre>
        </details>
      )}

      {/* ── Los avisos: el visor también es un guardián ──────────────── */}
      {seed.avisos.length > 0 && (
        <ul className="mt-4 space-y-1 font-sans text-xs text-(--sim-ink-faint)">
          {seed.avisos.map((a) => (
            <li key={a}>⚠ {a}</li>
          ))}
        </ul>
      )}

      <p className="sim-mono mt-4 text-[0.7rem] text-(--sim-ink-faint)">
        {seed.vacio
          ? "seed vacío · tabla `presencias` sin filas"
          : `${seed.run.cadena.join(" → ")} · ${seed.run.n_presencias} presencias · ${seed.run.n_agentes} agentes`}
        {" · "}
        exportado por curiana_sim/export_escena_seed.py
      </p>
    </div>
  );
}

// ── Piezas menores ────────────────────────────────────────────────────

function BotonTurno({
  children,
  label,
  onClick,
  disabled,
}: {
  children: React.ReactNode;
  label: string;
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label={label}
      title={label}
      className="flex h-7 w-7 items-center justify-center rounded-full border border-(--sim-rule) font-sans text-xs text-(--sim-ink-soft) transition-colors hover:border-(--sim-rubrica) hover:text-(--sim-ink) disabled:cursor-not-allowed disabled:opacity-35"
    >
      {children}
    </button>
  );
}

function Pildora({ children, color }: { children: React.ReactNode; color: string }) {
  return (
    <span
      className="inline-flex items-center rounded-full px-2 py-0.5 font-sans text-[0.7rem]"
      style={{ background: `${color}22`, color }}
    >
      {children}
    </span>
  );
}
