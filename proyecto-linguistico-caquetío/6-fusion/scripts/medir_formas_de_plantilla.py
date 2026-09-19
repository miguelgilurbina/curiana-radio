#!/usr/bin/env python3
"""El CORTE DE SERIE del 2026-09-18, medido: ¿qué mueve rechazar en la
REGISTRACIÓN lo que la plantilla ya enseña?

Miguel decidió la opción A del issue («dale pues con A»): una forma que está en
`VOCABULARIO_BASE` o que es un ejemplo de las plantillas del prompt no se
registra como acuñación, no entra en competencia y no puede adoptarse. La
puerta es una sola y vive en `curiana_lexicon.FORMAS_DE_PLANTILLA`.

Esto mide el ANTES y el DESPUÉS sobre los dos días de la serie C que corrieron
con el prompt contaminando la competencia:

    76ecf45c  día 1   `kali-bana` 2 usos de 2 agentes
    96b22194  día 2   12 usos de 11 agentes, en 10 lugares y en los dos nodos,
                      y la competencia de «las cuentas» 15,8 contra 3,1 y 2,9

Cómo se mide: se re-ejecuta el pipeline del Observer sobre las 144 respuestas
guardadas, EN SU ORDEN y encadenando los días como lo hizo `--continuar`, dos
veces —con la puerta y sin ella— y se comparan respuesta a respuesta. Se
replica además la competencia léxica del motor (el turno de nombramiento, las
propuestas, los reusos y la fijación al cerrar el día), que es donde se ve
quién lidera «las cuentas» sin `kali-bana`. No hay cifras a mano y no se llama
a la API: la única entrada es la base local y el propio motor.

    python 6-fusion/scripts/medir_formas_de_plantilla.py
    python 6-fusion/scripts/medir_formas_de_plantilla.py --runs b7bc51dc
    python 6-fusion/scripts/medir_formas_de_plantilla.py --yaml

CONTROL: el replay SIN la puerta tiene que reproducir lo que la base guardó
(`score` y `neologisms_proposed` de las 144) y lo que la bitácora anotó de la
competencia. Si el control falla, lo demás no mide nada.

⚠ No importa `curiana_orchestrator_v2` (arrastraría `curiana_database` y su
`load_dotenv()`). Desde el corte, tampoco hace falta sacar la plantilla con
`ast`: `IDENTIDAD_LINGUISTICA` vive en `curiana_lexicon` con las otras.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIM = os.path.join(RAIZ, "curiana_sim")
sys.path.insert(0, SIM)

CONTENEDOR = "supabase_db_curiana_sim"
# La cadena de la serie C: el día 1 y el día 2, en orden. Son los dos días que
# quedan del otro lado del corte.
CADENA_SERIE_C = ["76ecf45c", "96b22194"]
SEPARADOR = "\x1f"          # separador de campos: no aparece en el texto
FIN_DE_FILA = "\x1e"
# El motor introduce un referente nuevo cada `CADENCIA` turnos, y sólo con
# t > 0: en un run de seis turnos, el turno 5 (t = 4). No se escribe a mano —
# se lee del orquestador sería importar el bucle, así que se declara aquí con
# su fuente: `curiana_orchestrator_v2.auto_mode`, `cadencia_nombramiento = 4`.
CADENCIA_NOMBRAMIENTO = 4


# ── 1. La base, por docker exec (como el informe del día 1) ───────────

def psql(sql: str) -> str:
    r = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d", "postgres",
         "-Atc", sql],
        capture_output=True,
    )
    if r.returncode != 0:
        raise SystemExit("psql falló: " + r.stderr.decode("utf-8", "replace"))
    return r.stdout.decode("utf-8")


def config_del_run(prefijo: str) -> dict:
    """La config sellada del run: de ahí sale el elenco (y no de una variable
    de entorno que el que mide tenga puesta)."""
    crudo = psql("select config::text from simulation_runs "
                 f"where id::text like '{prefijo}%'").strip()
    if not crudo:
        raise SystemExit(f"el run {prefijo} no está en la base local")
    return json.loads(crudo.splitlines()[0])


def respuestas_del_run(prefijo: str) -> list[dict]:
    """Las respuestas del run, en el orden en que se dijeron.

    `response_text` lleva saltos de línea, así que se piden con separadores
    explícitos en vez de fiarse del salto de línea de psql."""
    sql = (
        "select t.day || '{S}' || t.turn_num || '{S}' || r.agent_name || '{S}' || "
        "coalesce(r.ethnicity,'') || '{S}' || coalesce(r.tier,2) || '{S}' || "
        "t.moment || '{S}' || t.season || '{S}' || r.score || '{S}' || "
        "r.neologisms_proposed || '{S}' || coalesce(r.lugar,'') || '{S}' || "
        "r.response_text || '{F}' "
        "from agent_responses r join turns t on t.id = r.turn_id "
        "join simulation_runs s on s.id = r.run_id "
        "where s.id::text like '{P}%' "
        "order by t.day, t.turn_num, r.created_at"
    ).format(S=SEPARADOR, F=FIN_DE_FILA, P=prefijo)
    crudo = psql(sql)
    filas = []
    for bloque in crudo.split(FIN_DE_FILA):
        if not bloque.strip("\n"):
            continue
        partes = bloque.lstrip("\n").split(SEPARADOR)
        if len(partes) < 11:
            continue
        filas.append({
            "run": prefijo,
            "dia": int(partes[0]), "turno": int(partes[1]), "agente": partes[2],
            "etnia": partes[3] or "caquetío", "tier": int(partes[4]),
            "momento": partes[5], "estacion": partes[6],
            "score_guardado": float(partes[7]),
            "neos_guardados": int(partes[8]),
            "lugar": partes[9] or None,
            "texto": partes[10],
        })
    return filas


# ── 2. El replay: el pipeline del Observer y la competencia, sin API ──

def _turnos_del_run(filas: list[dict]) -> list[list[dict]]:
    """Las respuestas agrupadas por turno, en orden. Un turno del motor es una
    ventana de agentes, y el nombramiento es una propiedad del TURNO."""
    turnos: list[list[dict]] = []
    visto = None
    for f in filas:
        if (f["dia"], f["turno"]) != visto:
            turnos.append([])
            visto = (f["dia"], f["turno"])
        turnos[-1].append(f)
    return turnos


def replay(por_run: list[tuple[str, list[dict]]], *, filtrar: bool) -> dict:
    """Re-ejecuta el análisis de las respuestas en su orden, encadenando los
    runs como lo hizo `--continuar` (un léxico, un campo y una competencia
    para toda la cadena).

    `filtrar=False` es el motor de ANTES del corte; `True`, el de hoy."""
    import curiana_lexicon as lx
    from curiana_koine import CampoLexico, CompetenciaLexica, REFERENTES_NOVEDOSOS
    from curiana_observer import ObserverAgent

    lexico = lx.LexicoComunitario(filtrar_plantilla=filtrar)
    observer = ObserverAgent(None, lexico)          # sin cliente: nada de API
    competencia = CompetenciaLexica(filtrar_plantilla=filtrar)
    campo = CampoLexico()
    pendientes = [dict(r) for r in REFERENTES_NOVEDOSOS]

    salida = []
    for _run, filas in por_run:
        dia = filas[0]["dia"] if filas else 0
        for t, turno in enumerate(_turnos_del_run(filas)):
            naming = None
            if pendientes and t > 0 and t % CADENCIA_NOMBRAMIENTO == 0:
                naming = pendientes.pop(0)
                competencia.activar(naming["id"], naming["desc"])
            for fila in turno:
                lexico.situar(fila["agente"], fila["lugar"])
                registro = observer.analizar(
                    agente=fila["agente"], etnia=fila["etnia"], tier=fila["tier"],
                    texto=fila["texto"], dia=fila["dia"], turno=fila["turno"],
                    momento=fila["momento"], estacion=fila["estacion"],
                )
                observer.procesar_adopciones(fila["texto"], fila["agente"],
                                             fila["turno"], dia=fila["dia"])
                neos = registro.neologismos_extraidos
                for neo in neos:
                    if naming:
                        competencia.proponer(naming["id"], neo.forma,
                                             fila["agente"], ambito=fila["lugar"])
                    else:
                        competencia.registrar_uso(neo.forma, fila["agente"])
                for forma in registro.palabras_caquetias:
                    competencia.registrar_uso(forma, fila["agente"])
                campo.registrar(registro.palabras_caquetias, ambito=fila["lugar"])
                campo.registrar([n.forma for n in neos], ambito=fila["lugar"])
                salida.append({
                    "agente": fila["agente"], "dia": fila["dia"],
                    "turno": fila["turno"], "score": registro.score,
                    "neologisms_proposed": len(neos),
                    "palabras_caquetias": len(registro.palabras_caquetias),
                })
            dia = turno[0]["dia"]
        # Al cerrar el día, el motor evalúa la fijación (auto_mode).
        competencia.evaluar_fijacion(dia)

    disputas = {
        cid: [(f, round(s, 2)) for f, s in ref["variantes"].most_common(5)]
        for cid, ref in competencia.activas().items()
    }
    return {
        "campo": campo,
        "respuestas": salida,
        "rechazadas": list(lexico.rechazos_de_plantilla),
        "reporte_rechazos": lexico.reporte_de_rechazos(),
        "neologismos": len(lexico._neologismos),
        "adoptados": len(lexico.neologismos_adoptados()),
        "dos_ambitos": [n.forma for n in lexico.adoptados_en_dos_ambitos()],
        "disputas": disputas,
        "fijadas": competencia.diccionario_koine(),
    }


def puerta_anterior() -> frozenset:
    """`_FORMAS_EXCLUIDAS` tal y como era ANTES del corte: el vocabulario base
    y las TRES plantillas que miraba. Se reconstruye desde las mismas
    plantillas, no se copia, y sirve para medir cuánto ensancha la puerta
    nueva —que mira además el refuerzo y el rescate— el descuento de la
    métrica emergente."""
    import curiana_lexicon as lx
    return (frozenset(lx.VOCABULARIO_BASE)
            | lx.formas_en_texto(lx.IDENTIDAD_LINGUISTICA)
            | lx.formas_en_texto(lx.prompt_reglas_completo())
            | lx.formas_en_texto(lx.prompt_reglas_breve()))


# ── 3. El informe ─────────────────────────────────────────────────────

def medir(prefijos: list[str]) -> dict:
    import curiana_lexicon as lx

    por_run = [(p, respuestas_del_run(p)) for p in prefijos]
    for p, filas in por_run:
        if not filas:
            raise SystemExit(f"el run {p} no tiene respuestas en la base local")
    filas = [f for _p, fs in por_run for f in fs]

    antes = replay(por_run, filtrar=False)          # el motor de antes del corte
    hoy = replay(por_run, filtrar=True)             # el motor con la puerta

    formas_rechazadas = sorted({f for f, _a, _d, _t in hoy["rechazadas"]})

    def diffs(campo):
        salida = []
        for fila, a, b in zip(filas, antes["respuestas"], hoy["respuestas"]):
            if a[campo] == b[campo]:
                continue
            texto = (fila["texto"] or "").lower()
            salida.append({
                "run": fila["run"], "agente": a["agente"], "dia": a["dia"],
                "turno": a["turno"], "antes": a[campo], "despues": b[campo],
                "dice": [f for f in formas_rechazadas if f in texto],
            })
        return salida

    # Control: ¿el replay SIN la puerta reproduce lo que la base guardó?
    desvios_base = [
        {"run": f["run"], "agente": f["agente"], "dia": f["dia"], "turno": f["turno"],
         "base": f["score_guardado"], "replay": r["score"],
         "neos_base": f["neos_guardados"], "neos_replay": r["neologisms_proposed"]}
        for f, r in zip(filas, antes["respuestas"])
        if abs(f["score_guardado"] - r["score"]) > 1e-9
        or f["neos_guardados"] != r["neologisms_proposed"]
    ]
    d_score = diffs("score")
    # El ENSANCHE de la puerta: lo que la lista nueva añade a la vieja y que
    # de verdad se dijo en estos días. Son formas que la métrica emergente
    # contaba como koiné y que el prompt enseña (el refuerzo y el rescate).
    vieja = puerta_anterior()
    ensanche = lx.FORMAS_DE_PLANTILLA - vieja
    dichas = {f for f, _p in antes["campo"].top(10 ** 6)}
    return {
        "runs": prefijos,
        "respuestas": len(filas),
        "respuestas_por_run": {p: len(fs) for p, fs in por_run},
        "formas_de_plantilla": len(lx.FORMAS_DE_PLANTILLA),
        "formas_de_plantilla_antes": len(vieja),
        "ensanche": len(ensanche),
        "ensanche_dicho_en_estos_runs": sorted(dichas & ensanche),
        "control_replay_desvios": len(desvios_base),
        "control_ejemplos": desvios_base[:5],
        "score_cambia_en": len(d_score),
        "score_delta_max": (max(abs(d["antes"] - d["despues"]) for d in d_score)
                            if d_score else 0.0),
        "score_ejemplos": d_score[:20],
        "neologisms_proposed_cambia_en": len(diffs("neologisms_proposed")),
        "neologisms_proposed_ejemplos": diffs("neologisms_proposed")[:10],
        "palabras_caquetias_cambia_en": len(diffs("palabras_caquetias")),
        "palabras_caquetias_ejemplos": diffs("palabras_caquetias")[:10],
        "rechazadas": hoy["rechazadas"],
        "reporte_rechazos": hoy["reporte_rechazos"],
        "neologismos_antes": antes["neologismos"],
        "neologismos_despues": hoy["neologismos"],
        "adoptados_antes": antes["adoptados"],
        "adoptados_despues": hoy["adoptados"],
        "dos_ambitos_antes": antes["dos_ambitos"],
        "dos_ambitos_despues": hoy["dos_ambitos"],
        "disputas_antes": antes["disputas"],
        "disputas_despues": hoy["disputas"],
        "fijadas_antes": antes["fijadas"],
        "fijadas_despues": hoy["fijadas"],
        # El diccionario emergente, cada uno con SU descuento: el de antes con
        # la puerta vieja, el de hoy con la nueva.
        "emergente_antes": [(f, round(p, 1))
                            for f, p in antes["campo"].top(15, excluir=vieja)],
        "emergente_despues": [(f, round(p, 1)) for f, p in
                              hoy["campo"].top(15, excluir=lx.FORMAS_DE_PLANTILLA)],
    }


CABECERA_YAML = """\
# ─────────────────────────────────────────────────────────────────────────
# GENERADO por 6-fusion/scripts/medir_formas_de_plantilla.py --yaml
# No se edita a mano: se vuelve a correr.
#
# EL CORTE DE SERIE del 2026-09-18 («dale pues con A», Miguel), medido sobre
# los dos días de la serie C que ya habían corrido. ANTES = el motor sin la
# puerta; DESPUÉS = el motor con ella, que es el de hoy.
#
# La puerta: `curiana_lexicon.FORMAS_DE_PLANTILLA` —el vocabulario base más lo
# que enseñan las plantillas estáticas del prompt— rechaza en
# `LexicoComunitario.registrar_neologismo()` y en `CompetenciaLexica.proponer()`.
#
# Por qué se mueve `score`: `kali-bana` se OFICIALIZA durante el día (dos
# adoptantes), y una forma adoptada entra en `lexico.palabras_activas()`, que es
# justo lo que `score_linguistico()` reconoce. Rechazarla en la registración le
# quita esa palabra a `palabras_caquetias` en las respuestas POSTERIORES que la
# dicen — y ahí se mueve el score. `neologisms_proposed` no se mueve nunca: sale
# de `extraer_neologismos_del_texto()`, que es anterior al registro. El scorer
# NO se tocó: `score_linguistico()` es el mismo.
#
# La medición anterior a la decisión —un run, sin competencia— queda en
# `6-fusion/medicion_formas_de_plantilla_2026-09-18.yaml`.
# ─────────────────────────────────────────────────────────────────────────
"""


def a_yaml(d: dict) -> str:
    """El documento entero, con las cifras del replay y ninguna a mano."""
    def bloque(items, sangria="    "):
        if not items:
            return " []\n"
        out = "\n"
        for it in items:
            out += sangria + "- " + json.dumps(it, ensure_ascii=False) + "\n"
        return out

    def disputas(dd, sangria="    "):
        if not dd:
            return " {}\n"
        out = "\n"
        for cid, variantes in dd.items():
            out += (sangria + cid + ": "
                    + json.dumps(variantes, ensure_ascii=False) + "\n")
        return out

    y = CABECERA_YAML
    y += "meta:\n"
    y += f"  runs: {json.dumps(d['runs'])}\n"
    y += f"  respuestas: {d['respuestas']}\n"
    y += ("  respuestas_por_run: "
          + json.dumps(d["respuestas_por_run"], ensure_ascii=False) + "\n")
    y += "  script: 6-fusion/scripts/medir_formas_de_plantilla.py\n"
    y += "  base: supabase local (docker exec supabase_db_curiana_sim psql)\n"
    y += ("  como_se_corre: 'python 6-fusion/scripts/medir_formas_de_plantilla.py'\n")
    y += f"  formas_de_plantilla: {d['formas_de_plantilla']}\n"
    y += f"  formas_de_plantilla_antes: {d['formas_de_plantilla_antes']}\n"
    y += f"  ensanche: {d['ensanche']}\n"
    y += ("  ensanche_dicho_en_estos_runs: "
          + json.dumps(d["ensanche_dicho_en_estos_runs"], ensure_ascii=False) + "\n")
    y += ("  nota_lista: >-\n"
          "    UNA puerta, construida desde las plantillas y nunca a mano:\n"
          "    VOCABULARIO_BASE + formas_en_texto() de IDENTIDAD_LINGUISTICA,\n"
          "    prompt_reglas_completo(), prompt_reglas_breve(), prompt_refuerzo()\n"
          "    (sus cuatro tramos) y prompt_rescate_linguistico() (sus tres\n"
          "    motivos). Las dos últimas no estaban en el viejo\n"
          "    `_FORMAS_EXCLUIDAS` (5.898 formas) y sí enseñan formas: ma-arua,\n"
          "    wa-duna, wana-ni, cati. El orquestador y analizar_nodos importan\n"
          "    ésta.\n")
    y += "\ncontrol:\n"
    y += ("  # El replay SIN la puerta tiene que reproducir lo que la base\n"
          "  # guardó (score y neologisms_proposed), o no mide nada.\n")
    y += f"  respuestas_identicas: {d['respuestas'] - d['control_replay_desvios']}\n"
    y += f"  desvios: {d['control_replay_desvios']}\n"
    y += "  ejemplos:" + bloque(d["control_ejemplos"])
    y += "\nrechazadas_por_la_puerta:" + bloque(
        [{"forma": f, "autor": a, "dia": dd, "turno": tt}
         for f, a, dd, tt in d["rechazadas"]], "  ")
    y += ("\n# Lo que el motor dice al cerrar el run: el rechazo se cuenta y se\n"
          "# dice, no se silencia.\n"
          "linea_de_cierre: "
          + json.dumps(d["reporte_rechazos"].strip(), ensure_ascii=False) + "\n")
    y += "\nefecto_en_el_instrumento:\n"
    y += f"  score_cambia_en: {d['score_cambia_en']}\n"
    y += f"  score_delta_max: {round(d['score_delta_max'], 4)}\n"
    y += "  score_detalle:" + bloque(d["score_ejemplos"])
    y += f"  neologisms_proposed_cambia_en: {d['neologisms_proposed_cambia_en']}\n"
    y += "  neologisms_proposed_detalle:" + bloque(d["neologisms_proposed_ejemplos"])
    y += f"  palabras_caquetias_cambia_en: {d['palabras_caquetias_cambia_en']}\n"
    y += "  palabras_caquetias_detalle:" + bloque(d["palabras_caquetias_ejemplos"])
    y += "\nefecto_en_el_registro:\n"
    y += f"  neologismos_antes: {d['neologismos_antes']}\n"
    y += f"  neologismos_despues: {d['neologismos_despues']}\n"
    y += f"  adoptados_antes: {d['adoptados_antes']}\n"
    y += f"  adoptados_despues: {d['adoptados_despues']}\n"
    y += ("  dos_ambitos_antes: "
          + json.dumps(d["dos_ambitos_antes"], ensure_ascii=False) + "\n")
    y += ("  dos_ambitos_despues: "
          + json.dumps(d["dos_ambitos_despues"], ensure_ascii=False) + "\n")
    y += "\ncompetencia:\n"
    y += ("  # Las disputas abiertas al cerrar el último día, con el soporte de\n"
          "  # cada variante (frecuencia × prestigio). Aquí se ve quién lidera\n"
          "  # «las cuentas» cuando el ejemplo del prompt no compite.\n")
    y += "  abiertas_antes:" + disputas(d["disputas_antes"])
    y += "  abiertas_despues:" + disputas(d["disputas_despues"])
    y += ("  fijadas_antes: "
          + json.dumps(d["fijadas_antes"], ensure_ascii=False) + "\n")
    y += ("  fijadas_despues: "
          + json.dumps(d["fijadas_despues"], ensure_ascii=False) + "\n")
    y += "\ndiccionario_emergente:\n"
    y += ("  # campo.top(15), cada uno con SU descuento: el de antes con la\n"
          "  # puerta vieja, el de hoy con la nueva (ver `ensanche`).\n")
    y += "  antes:" + bloque(d["emergente_antes"], "    ")
    y += "  despues:" + bloque(d["emergente_despues"], "    ")
    return y


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runs", default=",".join(CADENA_SERIE_C),
                    help="prefijos de los runs, en orden, separados por coma")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--yaml", action="store_true",
                    help="el documento de 6-fusion/, generado")
    args = ap.parse_args()
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")   # la consola de Windows es cp1252

    prefijos = [p.strip() for p in args.runs.split(",") if p.strip()]
    # El elenco lo dice la CONFIG del run, no el entorno de quien mide: el
    # scorer filtra nombres del elenco y el prestigio pondera la competencia.
    elenco = config_del_run(prefijos[0]).get("elenco") or "era1"
    os.environ["CURIANA_ELENCO"] = elenco

    d = medir(prefijos)
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return
    if args.yaml:
        print(a_yaml(d), end="")
        return
    print(f"\n  ── el corte de serie, medido · runs {', '.join(d['runs'])} "
          f"(elenco {elenco}) ──")
    print(f"  respuestas re-puntuadas: {d['respuestas']}  {d['respuestas_por_run']}")
    print(f"  FORMAS_DE_PLANTILLA: {d['formas_de_plantilla_antes']} → "
          f"{d['formas_de_plantilla']} formas (+{d['ensanche']}: el refuerzo y "
          f"el rescate)")
    print(f"  del ensanche, dichas en estos runs: "
          f"{d['ensanche_dicho_en_estos_runs']}")
    print(f"  control (el replay SIN la puerta reproduce la base): "
          f"{d['respuestas'] - d['control_replay_desvios']}/{d['respuestas']} exactas")
    for ej in d["control_ejemplos"]:
        print(f"      ⚠ {ej}")
    print(f"\n  score cambia en:               {d['score_cambia_en']} respuestas "
          f"(|Δ| máx {d['score_delta_max']:.2f})")
    for ej in d["score_ejemplos"]:
        print(f"      {ej}")
    print(f"  neologisms_proposed cambia en: {d['neologisms_proposed_cambia_en']}")
    for ej in d["neologisms_proposed_ejemplos"]:
        print(f"      {ej}")
    print(f"  palabras_caquetias cambia en:  {d['palabras_caquetias_cambia_en']}")
    print(f"\n  rechazadas por la puerta: {len(d['rechazadas'])}")
    for forma, autor, dia, turno in d["rechazadas"]:
        print(f"      {forma:22} ({autor}, día {dia} turno {turno})")
    print(f"  al cerrar el run:\n  {d['reporte_rechazos']}")
    print(f"\n  neologismos registrados:  {d['neologismos_antes']} → "
          f"{d['neologismos_despues']}")
    print(f"  adoptados:                {d['adoptados_antes']} → "
          f"{d['adoptados_despues']}")
    print(f"  adoptados en dos ámbitos: {d['dos_ambitos_antes']} → "
          f"{d['dos_ambitos_despues']}")
    print("\n  ── la competencia, al cerrar el último día ──")
    for etiqueta, dd in (("ANTES  ", d["disputas_antes"]),
                         ("DESPUÉS", d["disputas_despues"])):
        for cid, variantes in dd.items():
            print(f"  {etiqueta} {cid:16} "
                  + ", ".join(f"{f} {s}" for f, s in variantes))
    print(f"  fijadas: {d['fijadas_antes']} → {d['fijadas_despues']}")
    print("\n  ── diccionario emergente (15 primeras) ──")
    print(f"  antes:   {d['emergente_antes']}")
    print(f"  después: {d['emergente_despues']}")
    print()


if __name__ == "__main__":
    main()
