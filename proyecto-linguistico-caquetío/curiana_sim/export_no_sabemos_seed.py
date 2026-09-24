#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — «Lo que no sabemos», generado desde las mediciones del vault
=====================================================================

Emite `content/wiki/no-sabemos.json` en el repo de Curiana Radio: cinco
preguntas abiertas del proyecto, cada una con lo que HAY medido y de qué
archivo sale. Es la capa de la web que dice en voz alta dónde se acaba lo que
sabemos (decisión cc.9 de Miguel, 2026-09-23, sobre la propuesta del escriba:
«una página "Lo que no sabemos": cuatro o cinco preguntas abiertas con lo que
hay medido»).

REGLA 1: NINGUNA CIFRA A MANO
-----------------------------
La pregunta y su planteamiento son texto editorial (como los títulos de
`export_wiki_seed.py`); **cada número** que el texto dice sale de un YAML de
medición del vault o se cuenta aquí mismo sobre `curiana_lexicon.py`, en el
momento de exportar. Si el archivo de medición cambia, la página cambia; si
desaparece, la pregunta sale sin cifras y lo declara (`faltan`), nunca con
un número viejo.

LO QUE ESPERA A LA CORRIDA BASE
-------------------------------
La pregunta de la koiné —¿convergen dos pueblos porque ven lo mismo o porque
se copian?— sólo la contesta la corrida base (serie `era2-base`), que todavía
no ha corrido. Va con `estado: espera-la-corrida-base` y sin cifras: el hueco
queda declarado en la página, no escondido.

Sin la base: lee YAML y el lexicón, nunca Supabase.

Uso:
    python export_no_sabemos_seed.py
    python export_no_sabemos_seed.py --dry-run
"""

import argparse
import datetime
import io
import json
import os
import re
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)                    # proyecto-linguistico-caquetío/
CURIANA_RADIO = os.path.dirname(REPO)            # Curiana Radio/
SALIDA = os.path.join(CURIANA_RADIO, "content", "wiki", "no-sabemos.json")
VAULT = "proyecto-linguistico-caquetío"

sys.path.insert(0, AQUI)
import curiana_lexicon as L                                   # noqa: E402
from export_fichas_seed import siglas_zavala                  # noqa: E402


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


class Falta(Exception):
    """Un dato que la pregunta necesita y el archivo ya no trae."""


def leer_yaml(rel: str) -> dict:
    ruta = os.path.join(REPO, rel)
    if not os.path.isfile(ruta):
        raise Falta(f"no existe {rel}")
    with open(ruta, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def dato(doc: dict, *camino):
    actual = doc
    for clave in camino:
        if not isinstance(actual, dict) or clave not in actual:
            raise Falta("falta " + ".".join(str(c) for c in camino))
        actual = actual[clave]
    return actual


def fecha_de(doc: dict) -> str | None:
    meta = doc.get("meta") or {}
    for clave in ("medido", "fecha", "recogido"):
        for fuente in (meta, doc):
            if fuente.get(clave):
                return str(fuente[clave])
    return None


def fuente(rel: str, que: str, doc: dict | None = None) -> dict:
    return {"ruta": f"{VAULT}/{rel}", "que": que, "fecha": fecha_de(doc) if doc else None}


# ══════════════════════════════════════════════════════════════════════
# LAS PREGUNTAS — en orden editorial
# ══════════════════════════════════════════════════════════════════════

def p_hermana():
    rel = "6-fusion/medicion_cercania_hermanas_2026-09-23.yaml"
    doc = leer_yaml(rel)
    por_lengua = dato(doc, "por_lengua")
    nombres = {
        "kal_mujeres": "kalinago, habla de mujeres",
        "kal_hombres": "kalinago, habla de hombres",
        "lokono": "lokono",
        "taino": "taíno",
        "achagua": "achagua",
        "guajiro": "wayuu (guajiro)",
        "paraujano": "paraujano",
        "maipure": "maipure",
        "ic_oliver": "caribe insular (columna de Oliver)",
    }
    barras = []
    for clave, fila in por_lengua.items():
        barras.append({
            "etiqueta": nombres.get(clave, clave),
            "valor": fila["media_de_similitud"],
            "detalle": f"{fila['se_parece_(>=0.50)']} de {fila['conceptos_con_forma']} conceptos se parecen",
            "n": fila["conceptos_con_forma"],
        })
    barras.sort(key=lambda b: -b["valor"])
    cara = dato(doc, "cara_a_cara", "kal_mujeres_contra_lokono")
    taino = dato(por_lengua, "taino", "conceptos_con_forma")
    mas = max(f["conceptos_con_forma"] for f in por_lengua.values())
    umbral = dato(doc, "meta", "umbral_de_parecido")
    return {
        "slug": "la-hermana-mas-cercana",
        "pregunta": "¿A qué lengua hermana se parece más el caquetío?",
        "planteamiento": (
            "El caquetío es arahuaco, pero no dejó gramática: se reconstruye mirando a sus "
            "hermanas. Cuál de ellas es la más cercana decide de dónde sale cada voz "
            "reconstruida. Se tomaron las voces atestiguadas de concepto directo y se "
            "compararon, forma contra forma, con la misma idea en cada hermana."),
        "medido": [
            f"Cara a cara, el habla de mujeres kalinago gana en {cara['kal_mujeres']} conceptos, "
            f"el lokono en {cara['lokono']} y empatan en {cara['empate']}.",
            f"El taíno sólo tiene forma para {taino} de los {mas} conceptos: su media no "
            f"se puede comparar con la de las demás.",
            f"«Se parece» quiere decir una similitud de {str(umbral).replace('.', ',')} o más.",
        ],
        "barras": {"titulo": "Similitud media con el caquetío atestiguado (0 a 1)",
                   "filas": barras},
        "lo_que_falta": (f"Más conceptos compartidos. Con {mas} palabras comparables, un "
                         "empate no distingue entre las dos candidatas."),
        "estado": "abierta",
        "fuentes": [fuente(rel, dato(doc, "meta", "instrumento"), doc)],
        "enlaces": [
            {"href": "/kaketiana/lexicon?capa=reconstruido", "texto": "Las voces reconstruidas"},
            {"href": "/kaketiana/lengua/metodo-comparativo", "texto": "El método comparativo"},
        ],
    }


def p_angulo_molina():
    rel = "6-fusion/propuesta_nominalizador_2026-09-21.yaml"
    doc = leer_yaml(rel)
    medido = dato(doc, "la_independencia_de_la_fuente", "medido")
    glosario = dato(medido, "todo_el_glosario_por_compilador")
    verbos = dato(medido, "verbos_de_accion_por_compilador")
    am_glosario = glosario.get("AM", 0)
    segundo = max((v for k, v in glosario.items() if k != "AM"), default=0)

    # Contado aquí, sobre el lexicón de hoy: las voces vivas que llegan por AM.
    sigla = re.compile(r"#\d+\s*\(([A-Z+]+)\)")
    atest = [v for v in L.VOCABULARIO_BASE.values()
             if L.capa_epistemica(v.get("fuente", "")) == "caquetío-atestiguado"]
    con_am = solo_am = 0
    for v in atest:
        siglas = set()
        for grupo in sigla.findall(" ".join(str(v.get(c) or "") for c in ("notas", "glosa_fuente"))):
            siglas |= set(grupo.split("+"))
        if "AM" in siglas:
            con_am += 1
            solo_am += siglas == {"AM"}
    compiladores = siglas_zavala()
    if not compiladores:
        raise Falta("no se leyeron las siglas de 4-fuentes/zavala-reyes-2015.md")
    return {
        "slug": "angulo-molina",
        "pregunta": "¿Quién fue Angulo Molina?",
        "planteamiento": (
            "El glosario de Zavala Reyes (2015) es la fuente central del caquetío atestiguado, "
            f"y lo compila a partir de {len(compiladores)} autores que nombra por sus siglas. "
            "El que más aporta es «AM», Angulo Molina. Zavala no da su obra: ni título, ni "
            "año, ni editorial, y no se ha encontrado en ninguna otra parte."),
        "medido": [
            f"En el glosario, AM aporta {am_glosario} entradas; el siguiente compilador, {segundo}.",
            f"Los {verbos.get('AM', 0)} verbos de acción del glosario son suyos: todo el verbo "
            f"caquetío que se conoce es una sola lista de un autor que no sabemos quién es.",
            f"Hoy, {con_am} de las {len(atest)} voces atestiguadas del lexicón llegan por él, "
            f"y {solo_am} sólo por él.",
        ],
        "lo_que_falta": ("Encontrar la obra. La pista más fuerte es Hernández Baño, "
                         "Los Caquetíos de Falcón (Coro, 1984), que no está en el repositorio."),
        "estado": "abierta",
        "fuentes": [
            fuente(rel, "la independencia de la fuente: entradas y verbos por compilador", doc),
            {"ruta": f"{VAULT}/curiana_sim/curiana_lexicon.py",
             "que": "las voces atestiguadas con la sigla AM, contadas al exportar",
             "fecha": datetime.date.today().isoformat()},
            {"ruta": f"{VAULT}/4-fuentes/angulo-molina.md", "que": "qué se sabe y dónde buscar",
             "fecha": None},
        ],
        "enlaces": [
            {"href": "/kaketiana/bibliografia#angulo-molina", "texto": "Angulo Molina en la bibliografía"},
            {"href": "/kaketiana/lexicon?capa=atestiguado", "texto": "Las voces atestiguadas"},
        ],
    }


def p_ana():
    rel = "6-fusion/censo_ana_esteves_109.yaml"
    doc = leer_yaml(rel)
    r = dato(doc, "respuesta")
    return {
        "slug": "que-quiere-decir-ana",
        "pregunta": "¿Qué quiere decir -ana, la terminación de Curiana y Paraguaná?",
        "planteamiento": (
            "La lectura de siempre es «lugar de». Para comprobarla se contaron los topónimos "
            "en -ana del inventario de Esteves (1989), la fuente que más nombres de lugar de "
            "Paraguaná analiza."),
        "medido": [
            f"Esteves tiene {r['formas_en_ana_en_el_indice']} nombres en -ana. Glosados "
            f"como «lugar de»: {r['glosadas_lugar_de']}.",
            f"{r['de_ellas_son_bana'] + r['bana_con_h_intercalada']} son en realidad -bana, "
            f"«cerro, sitio alto»; {r['ana_dentro_de_una_raiz']} llevan -ana dentro de la "
            f"raíz; {r['sin_glosa']} —Paraguaná entre ellos— no tienen glosa.",
            "Cuando Esteves quiere decir «lugar de», usa -bacoa.",
        ],
        "lo_que_falta": ("Una fuente que glose -ana. Hasta entonces el proyecto la usa como "
                         "terminación sin significado declarado, y no le inventa uno."),
        "estado": "abierta",
        "fuentes": [fuente(rel, dato(doc, "meta", "pregunta").strip(), doc)],
        "enlaces": [
            {"href": "/kaketiana/lengua/toponimia", "texto": "La toponimia como fuente"},
            {"href": "/kaketiana/bibliografia#esteves-1989", "texto": "Esteves 1989"},
        ],
    }


def p_raiz():
    rel = "6-fusion/medicion_raices_de_ninguna_parte_2026-09-20.yaml"
    doc = leer_yaml(rel)
    coste = dato(doc, "coste_de_la_puerta")
    base = dato(coste, "toda_la_base")
    control = dato(coste, "control")
    fijadas = dato(doc, "hasta_donde_llegaron", "fijaron_koine")
    lumina = next((f for f in fijadas if "lumina" in str(f.get("forma"))), None)
    medido = [
        f"En toda la base, {base['de_ninguna_parte']} de {base['acunaciones_distintas']} "
        f"palabras inventadas por los agentes llevan una raíz que no está en el lexicón.",
        f"En la cadena de control, {control['de_ninguna_parte']} de "
        f"{control['acunaciones_distintas']}, y {control['de_ellas_adoptadas']} de ellas "
        f"llegaron a adoptarse.",
    ]
    if lumina:
        medido.append(
            f"Una llegó a fijarse como la palabra de la comunidad para «{lumina['concepto']}»: "
            f"{lumina['forma']}, sobre el latín lumina, el día {lumina['dia']}.")
    return {
        "slug": "puede-un-pueblo-inventar-una-raiz",
        "pregunta": "¿Puede un pueblo inventar una raíz nueva?",
        "planteamiento": (
            "En la simulación, los agentes acuñan palabras cuando les falta una. Casi todas "
            "combinan raíces y afijos que ya existen. Pero algunas traen una raíz que no sale "
            "de ninguna parte del lexicón, y a veces de otra lengua. Hoy el instrumento las "
            "deja fuera. Las lenguas reales, en cambio, sí inventan raíces."),
        "medido": medido,
        "lo_que_falta": ("Decidir dónde está la frontera entre una raíz nueva legítima y una "
                         "palabra ajena disfrazada. Es una decisión abierta del proyecto."),
        "estado": "abierta",
        "fuentes": [
            fuente(rel, dato(doc, "regla"), doc),
            {"ruta": f"{VAULT}/6-fusion/issues-pendientes/raiz-inventada-puede-un-pueblo-inventar-una-raiz-2026-09-20.md",
             "que": "la pregunta y sus opciones", "fecha": "2026-09-20"},
        ],
        "enlaces": [{"href": "/kaketiana/experimento", "texto": "El experimento"}],
    }


def p_koine():
    return {
        "slug": "por-que-convergen",
        "pregunta": "Cuando dos pueblos se juntan, ¿hablan igual porque ven lo mismo o porque se copian?",
        "planteamiento": (
            "La simulación pone a dos comunidades vecinas de Paraguaná, Guaranao y Amuay, a "
            "vivir sus días por separado y a encontrarse en el cerro. Si terminan nombrando "
            "las cosas nuevas con las mismas palabras, puede ser porque vieron lo mismo o porque "
            "una palabra viaja con quien la lleva."),
        "medido": [],
        "lo_que_falta": ("La corrida base: la primera serie con el motor ya cerrado. "
                         "Ella dirá quién dijo primero cada palabra, en qué lugar, y si cruzó "
                         "de un pueblo al otro antes o después del encuentro."),
        "estado": "espera-la-corrida-base",
        "fuentes": [{"ruta": f"{VAULT}/5-experimento/BITACORA_RUNS.md",
                     "que": "la bitácora de las corridas", "fecha": None}],
        "enlaces": [{"href": "/kaketiana/experimento#escena", "texto": "El mapa de la escena"}],
    }


PREGUNTAS = [p_hermana, p_angulo_molina, p_ana, p_raiz, p_koine]


def construir():
    preguntas, faltan = [], []
    for fn in PREGUNTAS:
        try:
            preguntas.append(fn())
        except Falta as e:
            faltan.append(f"{fn.__name__}: {e}")
    return {
        "generado": datetime.date.today().isoformat(),
        "n": len(preguntas),
        "preguntas": preguntas,
        "faltan": faltan,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    semilla = construir()
    for p in semilla["preguntas"]:
        print(f"· {p['pregunta']}  [{p['estado']}]")
        for m in p["medido"]:
            print(f"    {m}")
    if semilla["faltan"]:
        print("\n⚠ preguntas que no salieron (su fuente cambió):")
        for f in semilla["faltan"]:
            print(f"    {f}")
    if not args.dry_run:
        with open(SALIDA, "w", encoding="utf-8") as fh:
            json.dump(semilla, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    print("\n(dry-run: no se escribió nada)" if args.dry_run else f"\nEscrito en {SALIDA}")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
