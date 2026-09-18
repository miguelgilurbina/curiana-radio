#!/usr/bin/env python3
"""¿Rechazar en la REGISTRACIÓN lo que la plantilla ya enseña mueve el `score`?

El día 1 de la serie C (run `b7bc51dc`) registró dos «acuñaciones» que no lo
son: `kali-bana` —el ejemplo literal de `_IDENTIDAD_LINGUISTICA`, que va en el
system prompt de los 63 todos los turnos— y `warawara`, que está en
`VOCABULARIO_BASE`. El motor YA sabe cuáles son (`_FORMAS_EXCLUIDAS`, 5.898
formas: vocabulario base + lo que enseñan las tres plantillas) y las descuenta
de la métrica emergente; lo que no hace es impedir que se REGISTREN como
neologismos, así que `kali-bana` llegó a «adoptada en dos ámbitos».

Antes de tocar `LexicoComunitario.registrar_neologismo` hay que medir si el
filtro movería el instrumento, porque **el scorer no se toca**: si `score` o
`neologisms_proposed` cambian en una sola respuesta, el filtro no se aplica y
queda como propuesta.

Cómo se mide: se re-ejecuta el pipeline del Observer sobre las 72 respuestas
guardadas, EN SU ORDEN, dos veces —con el filtro y sin él— y se comparan
respuesta a respuesta. No hay cifras a mano y no se llama a la API: la única
entrada es la base local y el propio motor.

    python 6-fusion/scripts/medir_formas_de_plantilla.py
    python 6-fusion/scripts/medir_formas_de_plantilla.py --run b7bc51dc
    python 6-fusion/scripts/medir_formas_de_plantilla.py --json

⚠ No importa `curiana_orchestrator_v2` (arrastraría `curiana_database` y su
`load_dotenv()`): `_IDENTIDAD_LINGUISTICA` se saca del fichero con `ast`, el
mismo patrón de `medir_presupuesto_escena.py`.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIM = os.path.join(RAIZ, "curiana_sim")
sys.path.insert(0, SIM)

CONTENEDOR = "supabase_db_curiana_sim"
RUN_POR_DEFECTO = "b7bc51dc"
SEPARADOR = "\x1f"          # separador de campos: no aparece en el texto
FIN_DE_FILA = "\x1e"


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
            "dia": int(partes[0]), "turno": int(partes[1]), "agente": partes[2],
            "etnia": partes[3] or "caquetío", "tier": int(partes[4]),
            "momento": partes[5], "estacion": partes[6],
            "score_guardado": float(partes[7]),
            "neos_guardados": int(partes[8]),
            "lugar": partes[9] or None,
            "texto": partes[10],
        })
    return filas


# ── 2. La lista: construida desde las plantillas, nunca a mano ────────

def identidad_linguistica() -> str:
    """`_IDENTIDAD_LINGUISTICA` sin importar el orquestador."""
    ruta = os.path.join(SIM, "curiana_orchestrator_v2.py")
    with open(ruta, encoding="utf-8") as f:
        arbol = ast.parse(f.read())
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign):
            for destino in nodo.targets:
                if isinstance(destino, ast.Name) and destino.id == "_IDENTIDAD_LINGUISTICA":
                    return ast.literal_eval(nodo.value)
    raise SystemExit("no se encontró _IDENTIDAD_LINGUISTICA en el orquestador")


def formas_de_plantilla() -> frozenset:
    """Lo mismo que `_FORMAS_EXCLUIDAS`: base + las tres plantillas."""
    import curiana_lexicon as lx
    return (frozenset(lx.VOCABULARIO_BASE)
            | lx.formas_en_texto(identidad_linguistica())
            | lx.formas_en_texto(lx.prompt_reglas_completo())
            | lx.formas_en_texto(lx.prompt_reglas_breve()))


# ── 3. El replay: el pipeline del Observer, sin API ───────────────────

def replay(filas: list[dict], excluidas: frozenset | None) -> dict:
    """Re-ejecuta el análisis de las respuestas en su orden.

    `excluidas=None` es el motor de hoy. Con un conjunto, `registrar_neologismo`
    rechaza lo que la plantilla ya enseña — que es el cambio que se mide."""
    import curiana_lexicon as lx
    from curiana_observer import ObserverAgent

    lexico = lx.LexicoComunitario()
    observer = ObserverAgent(None, lexico)          # sin cliente: nada de API
    registrar = lexico.registrar_neologismo
    rechazadas: list[tuple[str, str]] = []

    if excluidas is not None:
        def registrar_filtrando(neo):
            if (neo.forma or "").lower() in excluidas:
                rechazadas.append((neo.autor, neo.forma))
                return
            registrar(neo)
        lexico.registrar_neologismo = registrar_filtrando   # type: ignore[method-assign]

    salida = []
    for fila in filas:
        lexico.situar(fila["agente"], fila["lugar"])
        registro = observer.analizar(
            agente=fila["agente"], etnia=fila["etnia"], tier=fila["tier"],
            texto=fila["texto"], dia=fila["dia"], turno=fila["turno"],
            momento=fila["momento"], estacion=fila["estacion"],
        )
        observer.procesar_adopciones(fila["texto"], fila["agente"],
                                     fila["turno"], dia=fila["dia"])
        salida.append({
            "agente": fila["agente"], "dia": fila["dia"], "turno": fila["turno"],
            "score": registro.score,
            "neologisms_proposed": len(registro.neologismos_extraidos),
            "palabras_caquetias": len(registro.palabras_caquetias),
        })
    return {
        "respuestas": salida,
        "rechazadas": rechazadas,
        "neologismos": len(lexico._neologismos),
        "adoptados": len(lexico.neologismos_adoptados()),
        "dos_ambitos": [n.forma for n in lexico.adoptados_en_dos_ambitos()],
    }


# ── 4. El informe ─────────────────────────────────────────────────────

def medir(prefijo: str) -> dict:
    filas = respuestas_del_run(prefijo)
    if not filas:
        raise SystemExit(f"el run {prefijo} no tiene respuestas en la base local")
    excluidas = formas_de_plantilla()
    hoy = replay(filas, None)
    con = replay(filas, excluidas)

    formas_rechazadas = sorted({f for _a, f in con["rechazadas"]})

    def diffs(campo):
        salida = []
        for fila, a, b in zip(filas, hoy["respuestas"], con["respuestas"]):
            if a[campo] == b[campo]:
                continue
            texto = (fila["texto"] or "").lower()
            salida.append({
                "agente": a["agente"], "dia": a["dia"], "turno": a["turno"],
                "hoy": a[campo], "con_filtro": b[campo],
                "dice": [f for f in formas_rechazadas if f in texto],
            })
        return salida

    # Control: ¿el replay reproduce lo que la base guardó?
    desvios_base = [
        (f["agente"], f["score_guardado"], r["score"])
        for f, r in zip(filas, hoy["respuestas"])
        if abs(f["score_guardado"] - r["score"]) > 1e-9
        or f["neos_guardados"] != r["neologisms_proposed"]
    ]
    return {
        "run": prefijo,
        "respuestas": len(filas),
        "formas_de_plantilla": len(excluidas),
        "control_replay_desvios": len(desvios_base),
        "control_ejemplos": desvios_base[:5],
        "score_cambia_en": len(diffs("score")),
        "score_ejemplos": diffs("score")[:10],
        "neologisms_proposed_cambia_en": len(diffs("neologisms_proposed")),
        "neologisms_proposed_ejemplos": diffs("neologisms_proposed")[:10],
        "palabras_caquetias_cambia_en": len(diffs("palabras_caquetias")),
        "palabras_caquetias_ejemplos": diffs("palabras_caquetias")[:10],
        "rechazadas": con["rechazadas"],
        "neologismos_hoy": hoy["neologismos"],
        "neologismos_con_filtro": con["neologismos"],
        "adoptados_hoy": hoy["adoptados"],
        "adoptados_con_filtro": con["adoptados"],
        "dos_ambitos_hoy": hoy["dos_ambitos"],
        "dos_ambitos_con_filtro": con["dos_ambitos"],
    }


CABECERA_YAML = """\
# ─────────────────────────────────────────────────────────────────────────
# GENERADO por 6-fusion/scripts/medir_formas_de_plantilla.py --yaml
# No se edita a mano: se vuelve a correr.
#
# La pregunta: ¿puede `LexicoComunitario.registrar_neologismo()` rechazar una
# forma que el prompt YA ENSEÑA —el vocabulario base y los ejemplos de las tres
# plantillas— sin mover el instrumento?
#
# La respuesta está en `veredicto`. El scorer no se toca: si `score` cambia en
# una sola respuesta, el filtro NO se aplica a mitad de serie y queda aquí como
# propuesta para un corte de serie de Miguel.
#
# Por qué se mueve (cuando se mueve): `kali-bana` se OFICIALIZA durante el día
# (dos adoptantes), y una forma adoptada entra en `lexico.palabras_activas()`,
# que es justo lo que `score_linguistico()` reconoce. Rechazarla en la
# registración le quita esa palabra a `palabras_caquetias` en las respuestas
# POSTERIORES que la dicen — y ahí se mueve el score. `neologisms_proposed` no
# se mueve nunca: sale de `extraer_neologismos_del_texto()`, que es anterior al
# registro.
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

    mueve = d["score_cambia_en"] > 0 or d["neologisms_proposed_cambia_en"] > 0
    veredicto = ("NO-APLICAR: el filtro mueve el instrumento"
                 if mueve else
                 "APLICAR: el filtro no mueve ni score ni neologisms_proposed")
    y = CABECERA_YAML
    y += "meta:\n"
    y += f"  run: {d['run']}\n"
    y += f"  respuestas: {d['respuestas']}\n"
    y += "  script: 6-fusion/scripts/medir_formas_de_plantilla.py\n"
    y += "  base: supabase local (docker exec supabase_db_curiana_sim psql)\n"
    y += ("  como_se_corre: 'CURIANA_ELENCO=era2 python "
          "6-fusion/scripts/medir_formas_de_plantilla.py'\n")
    y += f"  formas_de_plantilla: {d['formas_de_plantilla']}\n"
    y += ("  nota_lista: >-\n"
          "    Construida desde las plantillas, nunca a mano: VOCABULARIO_BASE +\n"
          "    formas_en_texto() de _IDENTIDAD_LINGUISTICA, prompt_reglas_completo()\n"
          "    y prompt_reglas_breve(). Es el mismo conjunto que\n"
          "    `curiana_orchestrator_v2._FORMAS_EXCLUIDAS`.\n")
    y += "\ncontrol:\n"
    y += ("  # El replay tiene que reproducir lo que la base guardó, o no mide nada.\n")
    y += f"  respuestas_identicas: {d['respuestas'] - d['control_replay_desvios']}\n"
    y += f"  desvios: {d['control_replay_desvios']}\n"
    y += "  ejemplos:" + bloque(d["control_ejemplos"])
    y += "\nrechazadas_por_el_filtro:" + bloque(
        [{"forma": f, "autor": a} for a, f in d["rechazadas"]], "  ")
    y += "\nefecto_en_el_instrumento:\n"
    y += f"  score_cambia_en: {d['score_cambia_en']}\n"
    y += "  score_detalle:" + bloque(d["score_ejemplos"])
    y += f"  neologisms_proposed_cambia_en: {d['neologisms_proposed_cambia_en']}\n"
    y += "  neologisms_proposed_detalle:" + bloque(d["neologisms_proposed_ejemplos"])
    y += f"  palabras_caquetias_cambia_en: {d['palabras_caquetias_cambia_en']}\n"
    y += "  palabras_caquetias_detalle:" + bloque(d["palabras_caquetias_ejemplos"])
    y += "\nefecto_en_el_registro:\n"
    y += f"  neologismos_hoy: {d['neologismos_hoy']}\n"
    y += f"  neologismos_con_filtro: {d['neologismos_con_filtro']}\n"
    y += f"  adoptados_hoy: {d['adoptados_hoy']}\n"
    y += f"  adoptados_con_filtro: {d['adoptados_con_filtro']}\n"
    y += ("  dos_ambitos_hoy: "
          + json.dumps(d["dos_ambitos_hoy"], ensure_ascii=False) + "\n")
    y += ("  dos_ambitos_con_filtro: "
          + json.dumps(d["dos_ambitos_con_filtro"], ensure_ascii=False) + "\n")
    y += "\nveredicto: " + json.dumps(veredicto, ensure_ascii=False) + "\n"
    return y


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", default=RUN_POR_DEFECTO, help="prefijo del run")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--yaml", action="store_true",
                    help="el documento de 6-fusion/, generado")
    args = ap.parse_args()
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")   # la consola de Windows es cp1252
    d = medir(args.run)
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return
    if args.yaml:
        print(a_yaml(d), end="")
        return
    print(f"\n  ── ¿el filtro de plantilla mueve el instrumento? run {d['run']} ──")
    print(f"  respuestas re-puntuadas: {d['respuestas']}")
    print(f"  FORMAS_DE_PLANTILLA: {d['formas_de_plantilla']} formas")
    print(f"  control (el replay reproduce la base): "
          f"{d['respuestas'] - d['control_replay_desvios']}/{d['respuestas']} exactas")
    for ej in d["control_ejemplos"]:
        print(f"      ⚠ {ej}")
    print(f"\n  score cambia en:               {d['score_cambia_en']} respuestas")
    for ej in d["score_ejemplos"]:
        print(f"      {ej}")
    print(f"  neologisms_proposed cambia en: {d['neologisms_proposed_cambia_en']}")
    for ej in d["neologisms_proposed_ejemplos"]:
        print(f"      {ej}")
    print(f"  palabras_caquetias cambia en:  {d['palabras_caquetias_cambia_en']}")
    print(f"\n  rechazadas por el filtro: {len(d['rechazadas'])}")
    for autor, forma in d["rechazadas"]:
        print(f"      {forma:22} ({autor})")
    print(f"\n  neologismos registrados: {d['neologismos_hoy']} → "
          f"{d['neologismos_con_filtro']}")
    print(f"  adoptados:               {d['adoptados_hoy']} → "
          f"{d['adoptados_con_filtro']}")
    print(f"  adoptados en dos ámbitos: {d['dos_ambitos_hoy']} → "
          f"{d['dos_ambitos_con_filtro']}")
    print()


if __name__ == "__main__":
    main()
