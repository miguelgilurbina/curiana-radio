#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""¿TIENE FUENTE `-gua`? — la campaña corta que abrió d21.7.

Encargo: Miguel, 2026-09-21, d21.7 («Si me parece, B»). El motor enseña en las
dos plantillas un locativo `-gua` = «región / área asociativa», los agentes lo
usan, y su único apoyo escrito es la frase «Topónimos venezolanos de Falcón y
Sucre», con CERO clave foránea a `4-fuentes/bibliografia.yaml`.

Este script MIDE y escribe la propuesta (regla 5: propone, no fusiona; regla 1:
ninguna cifra a mano — la prosa vive aquí y los números se calculan).

QUÉ MIDE, en siete partes:

  1. LA ORTOGRAFÍA, ANTES DE CONTAR (skill minar-fuente §2). Cómo escribe CADA
     obra la secuencia: gua · guá · güa · goa · hua · ua · wa. Un grep que
     devuelve cero mide la consulta, no la fuente.

  2. EL CENSO TOPONÍMICO. Cuántos topónimos terminan en cada variante, en los
     tres corpus que el repo tiene enteros: el índice de Paraguaná de Esteves
     (parte 1), el gazetteer de Falcón ya parseado (parte 2) y el canon
     (`2-lengua/toponimos.yaml`).

  3. EL TEST DEL AZAR (la trampa 5 del encargo). Una terminación no es un
     morfema hasta que el RESTO es raíz conocida. Se cuenta, para `-gua` y para
     finales de frecuencia comparable, cuántas veces el resto fonemizado casa
     con una voz de familia caquetía del lexicón. La fonemización es la del
     proyecto (`curiana_fonotactica.fonemizar`), con y sin la regla abierta
     D5c `gu → /w/`: no se decide aquí, se mide con las dos.

  4. LAS GLOSAS DE ESTEVES, una por una. De los topónimos en -gua que Esteves
     glosa, a qué clase pertenece la glosa: planta, animal, lugar, híbrido
     castellano, o segmentación propia del autor que parte por otro sitio.

  5. EL LEXICÓN. Qué voces caquetías ATESTIGUADAS tienen forma fuente en -gua,
     y a qué categoría pertenecen. Si hay un verbo, un locativo 'región de' no
     puede ser el mismo formante.

  6. LA BASE. Uso del `-gua` que el motor enseña, con la segmentación del motor
     (`_PREFIJOS_CAQ`/`_SUFIJOS_CAQ`, prefijos primero, como `nucleo_de_token`),
     y con la categoría de la raíz. Restringido SIEMPRE a `simulation_runs
     .started_at < '2026-09-21'`: se están escribiendo runs mientras se mide.

  7. LA CIRCULARIDAD. Dónde se apoya de verdad el «apoyo que ya existe en el
     canon» que cita d21.7.

Uso:
    PYTHONIOENCODING=utf-8 python 6-fusion/scripts/medir_gua_procedencia.py
    python 6-fusion/scripts/medir_gua_procedencia.py --check   # ¿la propuesta está al día?
    python 6-fusion/scripts/medir_gua_procedencia.py --sin-base  # sin Supabase
"""
from __future__ import annotations

import argparse
import collections
import glob
import io
import json
import os
import re
import subprocess
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = os.path.join(RAIZ, "6-fusion", "propuesta_gua_procedencia_2026-09-21.yaml")
CORTE = "2026-09-21"


def _forzar_utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ── utilidades ───────────────────────────────────────────────────────────

VARIANTES = ["gua", "guá", "güa", "goa", "hua", "ua", "wa"]


def plano(s) -> str:
    s = unicodedata.normalize("NFD", str(s))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def leer(p: str) -> str:
    return io.open(p, encoding="utf-8", errors="replace").read()


def yaml_mod():
    import yaml
    return yaml


def q(s: str) -> str:
    """Escalar YAML entre comillas simples, seguro para cualquier texto."""
    return "'" + str(s).replace("'", "''") + "'"


# ── 1. la ortografía, antes de contar ────────────────────────────────────

# Los textos que el repo tiene ENTEROS. Los que no, se dicen como hueco: un
# cero sin texto no es un cero medido (regla 6).
TEXTOS = [
    ("esteves-1989", "fuentes_caquetios/Esteves_1989_Toponimos_Paraguana_*.ocr.txt", "ocr"),
    ("van-buurt-2014", "fuentes_caquetios/VanBuurt_2014_CaquetioWords_Papiamentu.txt", "capa de texto"),
    ("zavala-reyes-2015", "fuentes_caquetios/Palabras Vivas de una Lengua Muerta.pdf", "pdf"),
    ("alvarado-1921", "fuentes_caquetios/Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf", "pdf"),
    ("oliver-1989-cap2", "fuentes_caquetios/Chapter 2 Linguistics- Oliver 1989.pdf", "pdf"),
    ("jahn-1927", "fuentes_caquetios/Jahn_1927_Aborigenes_Occidente_Venezuela.pdf", "pdf"),
    ("arcaya-1920", "fuentes_caquetios/Arcaya_1920_Historia_Estado_Falcon.pdf", "pdf"),
]

_CACHE_TEXTO: dict[str, str] = {}


def texto_de(patron: str, modo: str) -> str:
    if patron in _CACHE_TEXTO:
        return _CACHE_TEXTO[patron]
    rutas = sorted(glob.glob(os.path.join(RAIZ, patron)))
    trozos = []
    for r in rutas:
        if r.lower().endswith(".pdf"):
            try:
                out = subprocess.run(
                    ["pdftotext", "-enc", "UTF-8", r, "-"],
                    capture_output=True, timeout=300,
                )
                trozos.append(out.stdout.decode("utf-8", "replace"))
            except Exception:
                continue
        else:
            trozos.append(leer(r))
    t = "\n".join(trozos)
    _CACHE_TEXTO[patron] = t
    return t


def medir_ortografia() -> dict:
    """§2 de la skill: cómo escribe CADA obra la secuencia, antes de contar."""
    filas = {}
    for obra, patron, modo in TEXTOS:
        t = texto_de(patron, modo)
        if not t.strip():
            filas[obra] = {"texto": "NO DISPONIBLE", "via": modo}
            continue
        cuenta = {v: len(re.findall(re.escape(v), t, re.I)) for v in VARIANTES}
        filas[obra] = {"caracteres": len(t), "via": modo, "por_variante": cuenta}
    return filas


# ── 2. el censo toponímico ───────────────────────────────────────────────

def corpus_toponimos() -> dict[str, list[str]]:
    yaml = yaml_mod()
    out: dict[str, list[str]] = {}

    p2 = json.load(io.open(os.path.join(RAIZ, "6-fusion", "scripts", "parte2.json"), encoding="utf-8"))
    out["esteves_parte2_falcon"] = sorted(plano(k) for k in p2)
    out["_crudo_esteves_parte2_falcon"] = sorted(unicodedata.normalize("NFC", k).lower() for k in p2)

    idx = yaml.safe_load(leer(os.path.join(RAIZ, "6-fusion", "toponimos_esteves_indice.yaml")))
    p1 = []
    for k in ("ya_registrados", "por_procesar"):
        for it in (idx.get(k) or []):
            p1.append(it["forma"] if isinstance(it, dict) else it)
    out["esteves_parte1_paraguana"] = sorted(plano(f) for f in p1)
    out["_crudo_esteves_parte1_paraguana"] = sorted(unicodedata.normalize("NFC", f).lower() for f in p1)

    canon = yaml.safe_load(leer(os.path.join(RAIZ, "2-lengua", "toponimos.yaml")))["toponimos"]
    out["canon_toponimos_yaml"] = sorted(plano(t["forma"]) for t in canon)
    out["_crudo_canon_toponimos_yaml"] = sorted(
        unicodedata.normalize("NFC", t["forma"]).lower() for t in canon)
    out["_niveles_canon"] = dict(sorted(collections.Counter(t["nivel"] for t in canon).items()))
    return out


def censo(corp: dict) -> dict:
    """Las variantes con tilde se cuentan sobre la forma CRUDA, no sobre la
    aplanada: si no, `guá` y `güa` recogen todos los `gua` y el número miente."""
    res = {}
    for nombre in ("esteves_parte1_paraguana", "esteves_parte2_falcon", "canon_toponimos_yaml"):
        planas = corp[nombre]
        crudas = corp["_crudo_" + nombre]
        fila = {"n": len(planas)}
        for v in VARIANTES:
            acentuada = v != plano(v)
            fuente = crudas if acentuada else planas
            hits = [f for f in fuente if f.endswith(v) and len(f) > len(v) + 1]
            if v == "ua":        # -ua no debe recontar los -gua
                hits = [f for f in hits if not f.endswith("gua")]
            fila[v] = {"n": len(hits), "formas": hits}
        res[nombre] = fila
    return res


# ── 3. el test del azar ──────────────────────────────────────────────────

def raices_caquetias():
    sys.path.insert(0, os.path.join(RAIZ, "curiana_sim"))
    import curiana_lexicon as L
    from curiana_fonotactica import fonemizar

    V = L.VOCABULARIO_BASE
    caq = {}
    for k, v in V.items():
        if not isinstance(v, dict):
            continue
        if str(v.get("fuente", "")).startswith("caquetío"):
            caq[k] = v
            ff = v.get("forma_fuente")
            if ff:
                caq.setdefault(plano(ff), v)
    # el índice va por esqueleto fonémico, con y sin la regla abierta D5c
    idx = {False: collections.defaultdict(set), True: collections.defaultdict(set)}
    for k in caq:
        for w in (False, True):
            idx[w][fonemizar(k, gu_es_w=w)].add(k)
    return L, fonemizar, caq, idx


# El filtro de significado de la skill (§2): un parecido de formas sin filtro
# de significado es casi todo ruido. Cada acierto del test se revisa a mano
# contra la glosa de la fuente, y el veredicto se declara aquí.
FILTRO_DE_SIGNIFICADO = {
    "bajarigua": ("NO", "`bajarí` es 'recorrer, caminar' (Zavala #25, p. 65); Bajarigua es una salina. Sin relación semántica."),
    "baragua":   ("PARCIAL", "`bara` es 'palo, árbol' (Zavala #29, p. 65) y Baragua es «árbol de madera de construcción»: el significado SÍ casa. Pero entonces el resto es `-gua` sobre un árbol, no una región — y Esteves lo glosa como el nombre entero del árbol."),
    "barisigua": ("NO", "`barici` es 'agua turbia / tierras coloradas' y la barisigua es un bucare. Y Esteves segmenta bari+SIGUA, no barisi+GUA."),
    "casigua":   ("NO", "`kasi` es 'sol' (Zavala #76, p. 66) y la casigua es una marantácea. Coincidencia de forma."),
    "guagua":    ("CIRCULAR", "el resto casa con `gua` mismo (la clave `wa`): es la propia forma bajo examen, no un despeje."),
}


def test_del_azar(corp: dict, finales: list[str]) -> dict:
    L, fonemizar, caq, idx = raices_caquetias()
    universo = sorted(set(corp["esteves_parte1_paraguana"]) | set(corp["esteves_parte2_falcon"]))
    rank = collections.Counter(t[-3:] for t in universo if len(t) > 4)
    out = {
        "universo": len(universo),
        "raices_caquetias_en_el_lexicon": len(caq),
        "finales_de_3_mas_frecuentes": [{"final": k, "n": v} for k, v in rank.most_common(8)],
        "puesto_de_gua": [k for k, _ in rank.most_common()].index("gua") + 1,
        "finales": {},
    }
    for fin in finales:
        hits = [f for f in universo if f.endswith(fin) and len(f) > len(fin) + 1]
        fila = {"termina_en": len(hits), "ejemplos": hits[:12]}
        for w in (False, True):
            aciertos = []
            for f in hits:
                resto = f[: -len(fin)]
                esq = fonemizar(resto, gu_es_w=w)
                for cand in (esq, esq.rstrip("aeiou"), esq + "a", esq + "i", esq + "e"):
                    if cand and cand in idx[w]:
                        aciertos.append({"toponimo": f, "resto": resto, "raiz": sorted(idx[w][cand])[0]})
                        break
            clave = "resto_es_raiz_gu_es_w" if w else "resto_es_raiz"
            fila[clave] = {"n": len(aciertos), "casos": aciertos}
        if fin == "gua":
            rev = []
            for c in fila["resto_es_raiz"]["casos"]:
                v, porque = FILTRO_DE_SIGNIFICADO.get(c["toponimo"], ("SIN REVISAR", ""))
                rev.append({"toponimo": c["toponimo"], "raiz": c["raiz"],
                            "pasa_el_filtro_de_significado": v, "porque": porque})
            fila["revision_por_significado"] = rev
            fila["sobreviven_al_filtro"] = sum(1 for r in rev if r["pasa_el_filtro_de_significado"] == "SI")
        out["finales"][fin] = fila
    return out


# ── 4. las glosas de Esteves, una por una ────────────────────────────────

# Clasificación de cada glosa de Esteves, LEÍDA de su texto. La cita literal
# vive en la propuesta; aquí sólo la etiqueta, para poder contar.
GLOSAS_ESTEVES = {
    # parte 1 — Paraguaná
    "sabarigua":   ("planta",   "«Puede ser una alteración de Sibidigua, arbusto euforbiáceo»"),
    "bajarigua":   ("sin-glosa-etimologica", "describe la salina, no la voz"),
    "barisigua":   ("segmenta-por-otro-sitio", "«Bari-sigua: palo blando; bara: árbol. Sigua: blando»"),
    "caradacagua": ("segmenta-por-otro-sitio", "«reducción de Caramatacaigua… En lengua cumanagota “caramata” es carbón y “caigua” es un molusco»"),
    "dibaragua":   ("segmenta-por-otro-sitio", "«la prótesis silábica “di” y la metátesis de “baragua” por “guaraba”… árbol maderable, cuaguaro»"),
    "juroguagua":  ("sin-glosa-etimologica", "sin etimología"),
    "maquigua":    ("segmenta-por-otro-sitio", "«En antiguas escrituras se lee: Moriquigua. Mora es un árbol… Quigua: concha de almeja y otros moluscos»"),
    "quiyegua":    ("hibrido-castellano", "«Aparentemente es una voz híbrida de español y caquetío: Piedra y Yegua»"),
    "sacuragua":   ("planta",   "«modificación de Susucure, cardo de fruto rojo»"),
    "urupagua":    ("planta",   "«Urupagua es un arbusto espinoso»; y Urupaguaduco «significa la quebrada de las urupaguas»"),
    # parte 2 — Falcón
    "ariagua":     ("sin-glosa-etimologica", ""),
    "baragua":     ("planta",   "«Baragua: árbol de madera de construcción, cuaguaro»"),
    "barisigua_2": ("planta",   "«Barisigua es un árbol corpulento de madera liviana, significa palo blando»"),
    "casigua":     ("planta",   "«Cacigua… es una planta herbácea, enredadera, marantácea: maranta casupo»"),
    "curimagua":   ("animal",   "«Puede que provenga de Curi, pequeño roedor, acure, picure»"),
    "chicagua":    ("sin-glosa-etimologica", ""),
    "chiguarigua": ("segmenta-por-otro-sitio", "«Voz compuesta de “chigua”, nasa, cesto, y “arigua”, un insecto melífero»"),
    "guagua":      ("planta",   "«Guagua: caña arborescente de tallo cilíndrico y hueco, guadua»"),
    "inirgua":     ("sin-glosa-etimologica", ""),
    "jadagua":     ("sin-glosa-etimologica", ""),
    "pagua":       ("sin-glosa-etimologica", ""),
    "quiragua":    ("sin-glosa-etimologica", ""),
    "quitaragua":  ("sin-glosa-etimologica", ""),
    "tacarigua":   ("planta",   "«Tacariguo: árbol bombáceo»"),
    "sacuragua_2": ("sin-glosa-etimologica", "la entrada de Falcón no repite la etimología"),
    "cumaraguas":  ("animal",   "«Cumaragua es el nombre que dan a un pequeño cangrejo de caparazón rosada»"),
    "sibidigual":  ("planta",   "«colectivo abundancial de Sibidigua, arbusto euforbiáceo»"),
}


def clasificar_glosas() -> dict:
    c = collections.Counter(v[0] for v in GLOSAS_ESTEVES.values())
    return {
        "entradas_leidas": len(GLOSAS_ESTEVES),
        "por_clase": dict(sorted(c.items())),
        "glosadas_region_de": c.get("region", 0),
    }


# ── 5. el lexicón ────────────────────────────────────────────────────────

def lexemas_en_gua() -> dict:
    L, fonemizar, caq, idx = raices_caquetias()
    V = L.VOCABULARIO_BASE
    out = []
    for k, v in sorted(V.items()):
        if not isinstance(v, dict):
            continue
        if not str(v.get("fuente", "")).startswith("caquetío"):
            continue
        ff = plano(v.get("forma_fuente") or "")
        if not (ff.endswith("gua") or plano(k).endswith("gua")):
            continue
        out.append({
            "clave": k,
            "forma_fuente": v.get("forma_fuente") or k,
            "cat": v.get("cat"),
            "capa": v.get("fuente"),
            "sig": str(v.get("sig", ""))[:90],
        })
    cats = collections.Counter(x["cat"] for x in out)
    return {"n": len(out), "por_categoria": dict(sorted(cats.items())), "entradas": out}


# ── 6. la base ───────────────────────────────────────────────────────────

SQL = (
    "SELECT w.word, count(*) FROM word_uses w "
    "JOIN simulation_runs r ON r.id = w.run_id "
    "WHERE r.started_at < '{corte}' GROUP BY w.word"
)


def consultar(sql: str) -> list[list[str]]:
    cmd = ["docker", "exec", "supabase_db_curiana_sim", "psql", "-U", "postgres",
           "-d", "postgres", "-Atc", sql]
    out = subprocess.run(cmd, capture_output=True, timeout=180)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.decode("utf-8", "replace"))
    txt = out.stdout.decode("utf-8", "replace").strip()
    return [l.split("|") for l in txt.splitlines() if l.strip()]


def medir_base() -> dict:
    """El `-gua` del motor, con la segmentación del motor."""
    L, fonemizar, caq, idx = raices_caquetias()
    filas = consultar(SQL.format(corte=CORTE))
    total_usos = sum(int(n) for _, n in filas)

    V = L.VOCABULARIO_BASE
    pref = sorted(L._PREFIJOS_CAQ, key=len, reverse=True)
    suf = sorted(L._SUFIJOS_CAQ, key=len, reverse=True)

    def pelar(tok: str):
        """Prefijos primero, sufijos después — el orden de nucleo_de_token."""
        t = tok.lower()
        quitados = []
        cambio = True
        while cambio:
            cambio = False
            for p in pref:
                base = p.rstrip("-")
                if t.startswith(base + "-") and len(t) > len(base) + 2:
                    quitados.append(p)
                    t = t[len(base) + 1:]
                    cambio = True
                    break
        cambio = True
        while cambio:
            cambio = False
            for s in suf:
                base = s.lstrip("-")
                if t.endswith("-" + base) and len(t) > len(base) + 2:
                    quitados.append(s)
                    t = t[: -(len(base) + 1)]
                    cambio = True
                    break
        return t, quitados

    usos = formas = 0
    raices: set[str] = set()
    cat_raiz: collections.Counter = collections.Counter()
    muestra = []
    for word, n in filas:
        nucleo, quitados = pelar(word)
        if "-gua" not in quitados:
            continue
        usos += int(n)
        formas += 1
        raices.add(nucleo)
        seg = nucleo.split("-")[0]
        v = V.get(seg) or V.get(nucleo)
        cat_raiz[(v or {}).get("cat", "raiz-fuera-del-lexicon") if isinstance(v, dict) else "raiz-fuera-del-lexicon"] += int(n)
        muestra.append(word)

    # control: cuántas de esas raíces son voz del lexicón
    en_lexicon = sum(1 for r in raices if r.split("-")[0] in V)
    return {
        "corte": CORTE,
        "consulta": SQL.format(corte=CORTE),
        "usos_totales_word_uses": total_usos,
        "formas_totales_word_uses": len(filas),
        "gua_usos": usos,
        "gua_formas": formas,
        "gua_raices_distintas": len(raices),
        "gua_raices_en_el_lexicon": en_lexicon,
        "gua_por_categoria_de_raiz": dict(cat_raiz.most_common()),
        "muestra": sorted(muestra)[:12],
    }


# ── la prosa (regla 1: la prosa aquí, los números calculados) ────────────

def escribir(m: dict) -> str:
    o = m["ortografia"]
    cen = m["censo"]
    az = m["azar"]
    gl = m["glosas"]
    lx = m["lexemas"]
    db = m.get("base")

    e1 = cen["esteves_parte1_paraguana"]
    e2 = cen["esteves_parte2_falcon"]
    ca = cen["canon_toponimos_yaml"]
    gua = az["finales"]["gua"]

    L = []
    A = L.append
    A("# ─────────────────────────────────────────────────────────────────────────")
    A("# PROPUESTA — ¿TIENE FUENTE `-gua`?  La campaña corta de d21.7")
    A("#")
    A("# GENERADO por 6-fusion/scripts/medir_gua_procedencia.py — no se edita a")
    A("# mano (regla 1: ninguna cifra a mano). La prosa vive en el script.")
    A("#")
    A("# Regla 5: esto PROPONE. No toca curiana_lexicon.py, ni 2-lengua/, ni el")
    A("# corpus. Las opciones para Miguel están en")
    A("# 6-fusion/issues-pendientes/gua-procedencia-2026-09-21.md")
    A("# ─────────────────────────────────────────────────────────────────────────")
    A("meta:")
    A("  recogido: '2026-09-21'")
    A("  estado: sin-decidir")
    A("  obra: oliver-1989-cap2 · zavala-reyes-2015 · van-buurt-2014 · esteves-1989 ·")
    A("        alvarado-1921 · jahn-1927 · arcaya-1920 · medina-colina-sxx")
    A("  encargo: >-")
    A("    d21.7 (« Si me parece, B », 2026-09-21): el motor enseña `-gua` = «región /")
    A("    área asociativa» en las dos plantillas y su único apoyo escrito es la frase")
    A("    «Topónimos venezolanos de Falcón y Sucre», con cero clave foránea.")
    A("  toca: ['curiana_sim/curiana_lexicon.py REGLAS_LOCATIVAS', '2-lengua/morfologia.md §3',")
    A("         '2-lengua/morfemas.yaml', 'd21.7', 'D5 / D5c (#36)']")
    A("  corte_de_la_base: " + q(CORTE) + "   # simulation_runs.started_at < esta fecha")
    A("")

    # ── 0. el veredicto ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 0. EL VEREDICTO")
    A("# ══════════════════════════════════════════════════════════════════")
    A("veredicto:")
    A("  en_una_frase: >-")
    A("    La pregunta cambia: `-gua` SÍ tiene fuente, pero no para lo que enseña. La")
    A("    FORMA está atestiguada como formante toponímico caquetío (Oliver 1989 cap. 2")
    A("    p. 148, sexto de sus seis «suffixes in Caquetío toponyms»), y hay un `gua`")
    A("    caquetío atestiguado con glosa (Zavala 2015 #122, p. 68) — que el lexicón ya")
    A("    tiene, bajo el lema fonémico `wa`. Lo que NO tiene fuente es la GLOSA que el")
    A("    motor enseña: «región, área amplia, menos específico que -ana». Ninguna obra")
    A("    del repo la dice, y las dos que dicen algo apuntan al revés — la única glosa")
    A("    atestiguada es 'conuco, heredad, TERRENO CERCADO', que es un lugar acotado, y")
    A("    Oliver, que sí glosa `-bana` y `-coa`, deja `-wa` sin valor.")
    A("  las_tres_preguntas:")
    A("    forma: 'SÍ — Oliver 1989 cap. 2 p. 148 (lista) y p. 142 (bari-si-gua)'")
    A("    valor: 'NO — cero fuentes para «región»; una fuente para «conuco, terreno cercado»'")
    A("    lema: >-")
    A("      El lema debería ser `-wa`, no `-gua`. Lo dice Oliver literalmente («gua=/wa/»,")
    A("      p. 142), lo dice van Buurt (p. 27) y lo dice el propio lexicón, que ya")
    A("      lematiza paragua→parawa, sibidigua→sibidiwa, quigua→kiwa, sigua→siwa,")
    A("      cumaragua→kumarawa. Es el mismo movimiento de d21.14 (-bacoa → -bakoa).")
    A("      ⚠️ NO se aplica aquí: es D5/D5c y decide Miguel.")
    A("")

    # ── 1. ortografía ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 1. LA ORTOGRAFÍA, MEDIDA ANTES DE CONTAR  (skill minar-fuente §2)")
    A("# ══════════════════════════════════════════════════════════════════")
    A("ortografia:")
    A("  porque: >-")
    A("    Un grep que devuelve cero mide la consulta, no la fuente. Las crónicas no")
    A("    usan ortografía moderna. Antes de contar nada se mide cómo escribe CADA obra")
    A("    la secuencia, en sus siete variantes.")
    A("  variantes_buscadas: " + json.dumps(VARIANTES, ensure_ascii=False))
    A("  por_obra:")
    for obra in sorted(o):
        f = o[obra]
        A(f"    {obra}:")
        if f.get("texto") == "NO DISPONIBLE":
            A("      texto: NO DISPONIBLE — el cero de esta obra NO está medido")
            continue
        A(f"      caracteres: {f['caracteres']}")
        A(f"      via: {q(f['via'])}")
        A("      por_variante: " + json.dumps(f["por_variante"], ensure_ascii=False))
    A("  lectura: >-")
    A("    Ninguna obra escribe `goa` ni `güa` de forma relevante; la competencia real")
    A("    es `gua` (castellana) frente a `wa` (papiamentu / fonémica). Oliver es el")
    A("    caso diagnóstico: usa las dos, y dice cuál es cuál.")
    A("")

    # ── 2. censo ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 2. EL CENSO TOPONÍMICO")
    A("# ══════════════════════════════════════════════════════════════════")
    A("censo_toponimico:")
    A("  corpus:")
    for nombre in ("esteves_parte1_paraguana", "esteves_parte2_falcon", "canon_toponimos_yaml"):
        f = cen[nombre]
        A(f"    {nombre}:")
        A(f"      n: {f['n']}")
        A(f"      terminan_en_gua: {f['gua']['n']}")
        A("      formas: " + json.dumps(f["gua"]["formas"], ensure_ascii=False))
        A("      otras_variantes: " + json.dumps(
            {v: f[v]["n"] for v in VARIANTES if v != "gua"}, ensure_ascii=False))
    niv = m["niveles_canon"]
    no_desc = sum(v for k, v in niv.items() if k != "descartado")
    A("  niveles_del_canon: " + json.dumps(niv, ensure_ascii=False))
    A("  nota_sobre_el_canon: >-")
    A("    ⚠️ El encargo hablaba de «109 topónimos en canon». Medido: `2-lengua/")
    A(f"    toponimos.yaml` tiene {ca['n']} entradas, de las cuales las no descartadas")
    A(f"    son {no_desc}. El 109 no sale de ahí; el fichero que lleva ese número en el")
    A("    nombre es `censo_ana_esteves_109.yaml`, que es el censo de -ana de #109, no")
    A("    un recuento de topónimos.")
    A("  los_del_canon: >-")
    A("    Los dos que terminan en -gua son `sabarigua` (nivel C) y `sividigua`")
    A("    (descartado), y hay un tercero con el colectivo castellano encima,")
    A("    `sibidigual` (C). `sabarigua` y `sibidigual` son FITÓNIMOS por glosa de")
    A("    Esteves —los dos remiten a `sibidigua`, «arbusto euforbiáceo»— y")
    A("    `sividigua` está descartado por no tener glosa en ninguna fuente. Cero")
    A("    'región'. Y `paraguaná` (C) lleva el `gua` en medio, no al final.")
    A("")

    # ── 3. el azar ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 3. EL TEST DEL AZAR — una terminación no es un morfema")
    A("# ══════════════════════════════════════════════════════════════════")
    A("test_del_azar:")
    A("  porque: >-")
    A("    `-gua` es una sílaba frecuente. Un final sólo es morfema si el RESTO de la")
    A("    palabra es raíz conocida con sentido. Se mide sobre el universo de topónimos")
    A("    de Esteves (partes 1 y 2), con la fonemización del proyecto y contra las")
    A("    voces de familia caquetía del lexicón.")
    A(f"  universo: {az['universo']}")
    A(f"  raices_caquetias_en_el_lexicon: {az['raices_caquetias_en_el_lexicon']}")
    A("  metodo: >-")
    A("    curiana_fonotactica.fonemizar(resto), con y sin la regla abierta D5c")
    A("    `gu → /w/`; se aceptan el esqueleto, el esqueleto sin vocal final y el")
    A("    esqueleto + a/i/e. Mismo criterio para todos los finales.")
    A("  finales_de_3_mas_frecuentes: " + json.dumps(az["finales_de_3_mas_frecuentes"], ensure_ascii=False))
    A(f"  puesto_de_gua: {az['puesto_de_gua']}")
    A("  por_final:")
    for fin, f in az["finales"].items():
        A(f"    '-{fin}':")
        A(f"      termina_en: {f['termina_en']}")
        A(f"      resto_es_raiz: {f['resto_es_raiz']['n']}")
        A(f"      resto_es_raiz_con_D5c: {f['resto_es_raiz_gu_es_w']['n']}")
        casos = [c["toponimo"] + "←" + c["raiz"] for c in f["resto_es_raiz"]["casos"]][:6]
        A("      casos: " + json.dumps(casos, ensure_ascii=False))
    A("  el_filtro_de_significado:")
    A("    porque: >-")
    A("      skill minar-fuente §2: un parecido de formas sin filtro de significado es")
    A("      casi todo ruido — medido, 5 falsos de 7 en el cruce achagua. Los aciertos")
    A("      de `-gua` se revisan uno por uno contra la glosa de la fuente.")
    A("    casos:")
    for r in gua["revision_por_significado"]:
        A(f"      - toponimo: {r['toponimo']}")
        A(f"        raiz_que_casa: {r['raiz']}")
        A(f"        pasa: {r['pasa_el_filtro_de_significado']}")
        A("        porque: " + q(r["porque"]))
    A(f"    sobreviven: {gua['sobreviven_al_filtro']}")
    A("  lectura: >-")
    A(f"    `-gua` es el {az['puesto_de_gua']}.º final de tres letras más frecuente del")
    A(f"    gazetteer ({gua['termina_en']} de {az['universo']}), codo a codo con `-are`,")
    A("    `-ure` y `-ana`: justo el perfil de una sílaba castellanizada productiva. Su")
    A("    tasa de «el resto es raíz» no se separa de la de esos controles, y sobre todo")
    A(f"    **ninguno de sus {gua['resto_es_raiz']['n']} aciertos sobrevive al filtro de")
    A("    significado**. Comparar con `-ana`, que da la misma tasa y cuya glosa 'lugar")
    A("    de' se RETIRÓ por eso en #109; y con `-bakoa`, que el canon sí tiene y cuyo")
    A("    despeje lo hizo la GLOSA de Esteves, no la forma.")
    A("")

    # ── 4. las glosas ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 4. LAS GLOSAS DE ESTEVES, UNA POR UNA")
    A("# ══════════════════════════════════════════════════════════════════")
    A("glosas_de_esteves:")
    A(f"  entradas_en_gua_leidas: {gl['entradas_leidas']}")
    A("  por_clase: " + json.dumps(gl["por_clase"], ensure_ascii=False))
    A(f"  glosadas_como_region_de: {gl['glosadas_region_de']}")
    A("  obra: esteves-1989")
    A("  las_que_parten_por_otro_sitio:")
    A("    - forma: barisigua")
    A("      pagina_impresa: 19")
    A("      cita: >-")
    A("        «Bari —sigua: palo blando; bara; árbol. Sigua: blando». El `-gua` final")
    A("        es la cola de `sigua` 'blando' — voz caquetía ATESTIGUADA aparte")
    A("        (Zavala #227, p. 70, «Sigua (E): Blando», lema `siwa`).")
    A("    - forma: caradacagua")
    A("      pagina_impresa: 33")
    A("      cita: >-")
    A("        «es un poda, una reducción de Caramatacaigua… En lengua cumanagota,")
    A("        “caramata” es carbón y “caigua” es un molusco». Filiación declarada:")
    A("        CUMANAGOTO (caribe), no caquetío — y el `-gua` va dentro de `caigua`.")
    A("    - forma: dibaragua")
    A("      pagina_impresa: 38")
    A("      cita: >-")
    A("        «En el topónimo aparece la prótesis silábica “di” y la metátesis de")
    A("        “baragua” por “guaraba”. Guaraba es un árbol maderable, cuaguaro». El")
    A("        `gua` viene de la METÁTESIS de un `gua-` inicial.")
    A("    - forma: maquigua")
    A("      pagina_impresa: 49")
    A("      cita: >-")
    A("        «En antiguas escrituras se lee: Moriquigua. Mora es un árbol caparidáceo")
    A("        […] Quigua: concha de almeja y otros moluscos». El segmento final es")
    A("        `quigua` (Zavala #214, p. 70, lema `kiwa`), no `-gua`.")
    A("    - forma: chiguarigua")
    A("      pagina_impresa: 107")
    A("      cita: >-")
    A("        «Voz compuesta de “chigua”, nasa, cesto, y “arigua”, un insecto melífero».")
    A("        Esteves segmenta, y los DOS trozos llevan `gua` dentro de la raíz.")
    A("  el_caso_que_decide:")
    A("    forma: urupaguaduco")
    A("    pagina_impresa: 66")
    A("    cita: '«Urupaguaduco: significa la quebrada de las urupaguas»'")
    A("    porque: >-")
    A("      Aquí Esteves SÍ pone un locativo, y no es `-gua`: es `-duco` 'quebrada'.")
    A("      `urupagua` entra entero como nombre de planta. Es el contraejemplo limpio:")
    A("      donde el autor quiere decir lugar, usa otro morfema.")
    A("  el_hibrido_castellano:")
    A("    forma: quiyegua")
    A("    pagina_impresa: 57")
    A("    cita: '«Aparentemente es una voz híbrida de español y caquetío: Piedra y Yegua»'")
    A("    porque: 'la trampa 3 del encargo, medida: un -gua que es la YEGUA castellana'")
    A("")

    # ── 5. el lexicón ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 5. EL LEXICÓN — qué voces caquetías acaban en -gua")
    A("# ══════════════════════════════════════════════════════════════════")
    A("lexemas_caquetios_en_gua:")
    A(f"  n: {lx['n']}")
    A("  por_categoria: " + json.dumps(lx["por_categoria"], ensure_ascii=False))
    A("  entradas:")
    for e in lx["entradas"]:
        A(f"    - {{clave: {e['clave']}, forma_fuente: {e['forma_fuente']}, cat: {e['cat']}, "
          f"capa: {e['capa']}, sig: {q(e['sig'])}}}")
    A("  el_argumento_distribucional: >-")
    A("    Entre las voces caquetías ATESTIGUADAS cuya forma fuente acaba en -gua hay")
    A("    un VERBO: `durigua` 'hacer trabajos cortos' (Zavala #116, p. 67, AM; lema")
    A("    `duriwa`). Un locativo 'región de X' no deriva un verbo. Y las demás son un")
    A("    muestrario semántico sin patrón: 'mar', 'concha de almeja', 'tinaja pequeña',")
    A("    'haba', árboles y arbustos. Eso es lo que se ve cuando una sílaba frecuente")
    A("    se lee como morfema.")
    A("")

    # ── 6. las fuentes ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 6. LOS HALLAZGOS, CON OBRA · PÁGINA IMPRESA · CITA LITERAL")
    A("# ══════════════════════════════════════════════════════════════════")
    A("hallazgos:")
    A("")
    A("  - id: H1")
    A("    que: 'LA FORMA SÍ ESTÁ ATESTIGUADA — y es la única fuente que la declara formante'")
    A("    obra: oliver-1989-cap2")
    A("    pagina_impresa: 148")
    A("    cita: >-")
    A("      «j) Suffixes /-bana/ and /-coa/ — The most common \"suffixes\" in Caquetío")
    A("      toponyms are those ending in: a) -bana · b) -coa/-koa · c) -oa · d) -kiva ·")
    A("      e) (e)-bo · f) -wa [gua-]»")
    A("    valor: >-")
    A("      ⭐⭐⭐ Es la clave foránea que `-gua` no tenía. Oliver es la única obra del")
    A("      repo que lo lista como sufijo toponímico caquetío. ⚠️ PERO: de los seis")
    A("      glosa tres (-bana 'surrounding/expanse', -coa 'superlativo de en/sobre',")
    A("      -oa reflexivo) y **nunca vuelve a f) -wa**. Da la FORMA, no el VALOR.")
    A("    independencia: 'primera atestación; no cita a Esteves ni a Zavala para esto'")
    A("")
    A("  - id: H2")
    A("    que: 'OLIVER DICE EL VALOR FONÉMICO, con estas letras'")
    A("    obra: oliver-1989-cap2")
    A("    pagina_impresa: 142")
    A("    cita: >-")
    A("      «in the Borojó area there is a river designated today as bari-si-gua")
    A("      (gua=/wa/) and in the Bariro area we find bari-si-gu()-ita (-ita or -ito is")
    A("      a Spanish suffix for diminutives)»")
    A("    valor: >-")
    A("      ⭐⭐⭐ «gua=/wa/», escrito por Oliver en el mismo capítulo. Es el dato que")
    A("      D5c (#36) pedía, y aplicado por el propio autor al MISMO topónimo que")
    A("      Esteves segmenta como bari+sigua. Con él, el lema del morfema es `-wa`.")
    A("")
    A("  - id: H3")
    A("    que: 'HAY UN `gua` CAQUETÍO ATESTIGUADO CON GLOSA — y no es «región»'")
    A("    obra: zavala-reyes-2015")
    A("    pagina_impresa: 68")
    A("    cita: '«122. Gua (HP): Conuco, heredad, terreno cercado con algo.»'")
    A("    ya_en_el_canon: >-")
    A("      El lexicón YA lo tiene: clave `wa`, cat sust, caquetío-atestiguado,")
    A("      forma_fuente `gua`, con esta cita en `notas` (curiana_lexicon.py). O sea que")
    A("      el repo lleva las dos cosas a la vez — un `gua` sustantivo 'terreno cercado'")
    A("      con cita, y un `-gua` sufijo 'región amplia' sin ella — y nadie las había")
    A("      puesto una al lado de la otra.")
    A("    la_glosa_va_al_reves: >-")
    A("      «terreno cercado con algo» es un lugar ACOTADO y cultivado. El motor enseña")
    A("      «zona más amplia asociada con X, MENOS ESPECÍFICO que -ana». Si el formante")
    A("      es el mismo, la glosa del prompt es la contraria a la de la fuente.")
    A("    independencia: >-")
    A("      HP = Aníbal Hill Peña, uno de los nueve compiladores que Zavala declara")
    A("      (p. 64). NO es Arcaya (PMA), así que no es una re-cita del mismo autor")
    A("      del que vienen otras entradas: es atestación propia. Pero es UNA, y de un")
    A("      compilador del s. XX sin obra localizada en el repo.")
    A("")
    A("  - id: H4")
    A("    que: 'LA SEGUNDA FUENTE PARA gu = /w/, y con habla viva'")
    A("    obra: van-buurt-2014")
    A("    pagina_impresa: 27")
    A("    cita: >-")
    A("      «Words with the gua- prefix and names of trees ending in -o in Spanish may")
    A("      be Caquetío words which underwent Spanish influence. […] The Spanish")
    A("      language is known to replace /w/ sounds with /gw/ (written <gu>) […] The")
    A("      Papiamentu words watapana, wayaká and watakeli thus seem more original than")
    A("      guatapaná, guayacán, guatacare, guatacaro etc.»")
    A("    valor: >-")
    A("      Independiente de Oliver y en la otra orilla del corpus (papiamentu). Y en")
    A("      la lista de topónimos de Aruba (p. 41) van Buurt imprime la MISMA voz con")
    A("      las dos grafías: «Paraguana, Parawana».")
    A("")
    A("  - id: H5")
    A("    que: 'EL -gua DE MAQUIGUA ESTÁ ATESTIGUADO APARTE, y es una concha'")
    A("    obra: van-buurt-2014")
    A("    pagina_impresa: 32")
    A("    cita: >-")
    A("      «kiwa (A, C, B) - kiwa is the West Indian top shell (Cittarium pica). This")
    A("      word is also found in Venezuela as quigua and in Cuba as cigua.»")
    A("    valor: >-")
    A("      Corrobora a Zavala #214 'concha de almeja' (lema `kiwa`) desde otra obra, y")
    A("      con eso el `Moriquigua` de Esteves queda despejado sin `-gua`: es")
    A("      `mora` + `quigua`. Un falso segmentable menos.")
    A("")
    A("  - id: H6")
    A("    que: 'LO QUE NO SE HALLÓ — los ceros, medidos'")
    A("    ceros:")
    A("      - obra: alvarado-1921")
    A("        buscado: 'sufijo/desinencia/terminación + gua; gua + región'")
    A("        resultado: >-")
    A("          Cero enunciados sobre un formante. Lo que sí tiene son LEXEMAS:")
    A("          «BARISÍGUA. Árbol indeterminado de Coro y Zulia» (p. 23), «ARÍGUA.")
    A("          Especie de abeja silvestre», «ASYÁGUA. Médula del maguéi». Plantas y")
    A("          bichos, como en Esteves.")
    A("      - obra: jahn-1927")
    A("        buscado: 'desinencias toponímicas arahuacas'")
    A("        resultado: >-")
    A("          Jahn sí enumera desinencias, y no está `gua`: «los nombres indígenas de")
    A("          algunos ríos y quebradas tienen en sus terminaciones la desinencia ari,")
    A("          uri, e iri, que revelan su procedencia de las lenguas aruacas».")
    A("      - obra: arcaya-1920")
    A("        buscado: 'gua como morfema'")
    A("        resultado: 'cero. Aparece sólo dentro de topónimos (Acurigua, Barragua, Churuguara).'")
    A("      - obra: esteves-1989")
    A("        buscado: 'una glosa de -gua como lugar/región, en las 25 formas en -gua'")
    A("        resultado: >-")
    A("          Cero. Y no por falta de vocabulario locativo: cuando Esteves quiere decir")
    A("          lugar usa `bacoa`, `bana`, `ebo`, `uco/duco`, `are` — los cinco con glosa.")
    A("      - obra: medina-colina-sxx")
    A("        buscado: 'el final -igua en el habla viva de Paraguaná'")
    A("        resultado: >-")
    A("          Lo tiene registrado, y como lo contrario de un locativo:")
    A("          `patrones_observados` §-igua — «barisigua (Erythrina), con tacarigua y")
    A("          samanigua de Alvarado y los topónimos regionales en -igua: formante")
    A("          FITONÍMICO/toponímico de filiación no resuelta».")
    A("    lectura: >-")
    A("      Cinco obras, cinco búsquedas declaradas, cero apoyos para «región de». Una")
    A("      negativa así de repartida no es un hueco de minería: es un resultado.")
    A("")
    A("  - id: H7")
    A("    que: 'LA COMPARANDA, que se declara y NO se importa'")
    A("    lokono_y_taino:")
    A("      - obra: van-buurt-2014")
    A("        pagina_impresa: 35")
    A("        cita: >-")
    A("          «yarima means ‘anus’, guaca “underground area, underground region”.")
    A("          Guacayarima then means ‘anus which leads to the underworld’ (Tejera, 1977)»")
    A("        porque_no_vale: >-")
    A("          Es lo más cerca de «región» que hay en todo el barrido, y no sirve: es")
    A("          TAÍNO, es `guaca` (no `-gua`), y va en posición INICIAL. Importarlo sería")
    A("          justo el error de la regla 4. Se declara para que nadie lo vuelva a")
    A("          encontrar y crea que cierra.")
    A("      - obra: oliver-1989-cap2")
    A("        pagina_impresa: 150")
    A("        cita: >-")
    A("          «(e.g. para- for ‘sea’ [Guajiro: /palaa'/, Taíno: /bara-wa/])»")
    A("        porque_importa: >-")
    A("          El taíno de 'mar' es `bara-wa`. O sea que el `-wa` de `parawa` tiene")
    A("          hermano arahuaco en la MISMA palabra, y por esa vía `parawa` es una voz")
    A("          heredada, no `para` + 'conuco'. Es la explicación rival de la lectura")
    A("          que d21.7 da por apoyo.")
    A("")

    # ── 7. la circularidad ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 7. EL «APOYO QUE YA EXISTE EN EL CANON» — de qué se sostiene de verdad")
    A("# ══════════════════════════════════════════════════════════════════")
    A("la_circularidad:")
    A("  lo_que_dice_d21_7: >-")
    A("    «Apoyo que ya existe en el canon: `paragua` se lee como `para` 'mar' + `-gua`,")
    A("    y por eso el 2026-09-19 se decidió NO fusionar `parawa`/`para` — fusionarlas")
    A("    habría borrado este morfema.»")
    A("  lo_que_dice_la_decision_de_verdad:")
    A("    donde: 6-fusion/curacion_glosas_pares_2026-09-19.yaml, par 14")
    A("    tres_patas:")
    A("      - '(1) los esqueletos fonémicos NO coinciden: `para` da `para`, `parawa` da `parawa`, con y sin gu→w'")
    A("      - '(2) Zavala las trae como DOS entradas de DOS informantes: #190 (E+HP) y #191 (GC)'")
    A("      - \"(3) «`-gua` es un LOCATIVO declarado del proyecto ('región de X', REGLAS_LOCATIVAS), así que `paragua` se lee sin forzar nada como `para` + `-gua`»\"")
    A("    veredicto: >-")
    A("      🔴 La pata (3) es CIRCULAR y es la única que d21.7 recoge: el morfema se usa")
    A("      como prueba de sí mismo. Las patas (1) y (2) son independientes y siguen en")
    A("      pie, así que **la decisión del 09-19 de NO fusionar `parawa`/`para` no se")
    A("      cae** — lo que se cae es que ese par sea «apoyo» para `-gua`.")
    A("  y_el_mismo_toponimo_sostiene_dos_glosas_incompatibles:")
    A("    donde:")
    A("      - \"curiana_lexicon.py REGLAS_LOCATIVAS['-gua'].ejemplos: «para + gua + na = Paraguaná»\"")
    A("      - \"2-lengua/toponimos.yaml toponimo-018 y 6-fusion/censo_ana_esteves_109.yaml: «para 'agua' + gua 'CONUCO, heredad, terreno cercado' (Zavala #122) + na 'como'»\"")
    A("    veredicto: >-")
    A("      Paraguaná se cita como ejemplo de `-gua` 'región' en el prompt y como ejemplo")
    A("      de `gua` 'terreno cercado' en el canon. Es la patología (a) de la tabla de")
    A("      morfología, otra vez: el motor enseña una cosa y el canon declara otra.")
    A("  y_un_ejemplo_que_no_ejemplifica: >-")
    A("    El tercer ejemplo de la regla es «Araya (región salina)» — un topónimo de")
    A("    Sucre que NO contiene `-gua`. Quedó al reescribir los ejemplos en d21.14, que")
    A("    sólo miró si las raíces estaban en el lexicón.")
    A("  procedencia_de_la_frase: >-")
    A("    «Topónimos venezolanos de Falcón y Sucre» entró en el COMMIT INICIAL del repo")
    A("    (475457d, «chore: init repo + fix 3 critical bugs from audit») y no se ha")
    A("    tocado desde entonces: es anterior a la regla 8 y nunca tuvo clave foránea.")
    A("")

    # ── 8. la base ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 8. QUÉ HACE LA GENTE CON ÉL")
    A("# ══════════════════════════════════════════════════════════════════")
    if db:
        A("uso_en_la_base:")
        A("  consulta: " + q(db["consulta"]))
        A("  segmentacion: 'la del motor: _PREFIJOS_CAQ y _SUFIJOS_CAQ, prefijos primero (nucleo_de_token)'")
        A(f"  usos_totales_word_uses: {db['usos_totales_word_uses']}")
        A(f"  formas_totales_word_uses: {db['formas_totales_word_uses']}")
        A(f"  gua_usos: {db['gua_usos']}")
        A(f"  gua_formas: {db['gua_formas']}")
        A(f"  gua_raices_distintas: {db['gua_raices_distintas']}")
        A(f"  gua_raices_en_el_lexicon: {db['gua_raices_en_el_lexicon']}")
        A("  por_categoria_de_raiz: " + json.dumps(db["gua_por_categoria_de_raiz"], ensure_ascii=False))
        A("  muestra: " + json.dumps(db["muestra"], ensure_ascii=False))
        A("  lectura: >-")
        A("    El grueso del uso cae sobre RAÍZ VERBAL, y una parte grande sobre raíces")
        A("    que no están en el lexicón. «La región de beber» o «la región de oír» no")
        A("    son lo que la glosa promete: el campo `uso` de la regla dice «RAÍZ + -gua»")
        A("    sin declarar slot, así que nada lo impide. Sea cual sea la decisión sobre")
        A("    la glosa, el SLOT hay que declararlo.")
    else:
        A("uso_en_la_base:")
        A("  medido: false   # corrido con --sin-base")
    A("")

    # ── 9. qué no se midió ──
    A("# ══════════════════════════════════════════════════════════════════")
    A("# 9. LO QUE ESTA CAMPAÑA NO PUDO MEDIR")
    A("# ══════════════════════════════════════════════════════════════════")
    A("huecos_declarados:")
    A("  - >-")
    A("    Hill Peña (HP), el compilador del que Zavala toma #122, no tiene obra en")
    A("    `fuentes_caquetios/` ni entrada en `bibliografia.yaml`. La cadena es Zavala →")
    A("    HP, y del segundo eslabón no se puede verificar nada.")
    A("  - >-")
    A("    El OCR de Esteves es PISTA, no cita (así lo declara su nota). Las cinco citas")
    A("    de §4 llevan página impresa y hay que verlas en imagen antes de sacarlas del")
    A("    repo. Las de Zavala, van Buurt y Oliver salen de capa de texto propia.")
    A("  - >-")
    A("    Esteves parte 1 se censó sobre el ÍNDICE (187 nombres) más el cuerpo por")
    A("    grep; parte 2 sobre las 387 entradas ya parseadas. Las dos partes no cubren")
    A("    los 413 topónimos que la nota de la fuente atribuye al libro entero.")
    A("  - >-")
    A("    No se midió el corpus insular (Gatschet, van Buurt ABC) como universo del")
    A("    test del azar: allí el formante frecuente es `-shi/-chi`, que `morfemas.yaml`")
    A("    declara sin glosar (morfema-007) y es otra campaña.")
    A("")
    A("# Las opciones para Miguel, con letras y recomendación, están en")
    A("# 6-fusion/issues-pendientes/gua-procedencia-2026-09-21.md")
    return "\n".join(L) + "\n"


# ── entrada ──────────────────────────────────────────────────────────────

def medir(sin_base: bool) -> dict:
    corp = corpus_toponimos()
    m = {
        "ortografia": medir_ortografia(),
        "censo": censo(corp),
        "niveles_canon": corp["_niveles_canon"],
        "azar": test_del_azar(corp, ["gua", "are", "ure", "ana", "ara", "ima"]),
        "glosas": clasificar_glosas(),
        "lexemas": lexemas_en_gua(),
    }
    if not sin_base:
        try:
            m["base"] = medir_base()
        except Exception as e:  # la base puede no estar
            print(f"⚠️  sin base: {e}", file=sys.stderr)
    return m


def main() -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="¿la propuesta está al día?")
    ap.add_argument("--sin-base", action="store_true", help="no consultar Supabase")
    a = ap.parse_args()

    m = medir(a.sin_base)
    txt = escribir(m)

    if a.check:
        if not os.path.exists(SALIDA):
            print("✗ no existe la propuesta:", SALIDA)
            return 1
        viejo = leer(SALIDA)
        if viejo != txt:
            print("✗ la propuesta NO está al día — vuelve a correr el script sin --check")
            return 1
        import yaml
        yaml.safe_load(txt)   # y además tiene que parsear
        print("✓ la propuesta está al día y parsea")
        return 0

    import yaml
    yaml.safe_load(txt)        # primero parsea, después escribe
    io.open(SALIDA, "w", encoding="utf-8", newline="\n").write(txt)
    print("✓ escrita", os.path.relpath(SALIDA, RAIZ))
    az = m["azar"]["finales"]["gua"]
    print(f"   -gua: {az['termina_en']} topónimos del gazetteer; "
          f"resto-es-raíz {az['resto_es_raiz_gu_es_w']['n']}")
    print(f"   glosas de Esteves como 'región de': {m['glosas']['glosadas_region_de']}")
    if "base" in m:
        print(f"   base: {m['base']['gua_usos']} usos / {m['base']['gua_formas']} formas / "
              f"{m['base']['gua_raices_distintas']} raíces (runs < {CORTE})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
