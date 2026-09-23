#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA SIGLA (E) DE ZAVALA ES ESTEVES — el canon re-medido (decisión cc.4).

«la sigla es Zavala Esteves, eh, ok, miramos también el canon de eso»
(Miguel, 2026-09-23). En el glosario de Zavala Reyes 2015 la sigla «(E)» es
Juan Esteves (p. 64): cuando el canon cuenta «Zavala (E)» y «Esteves» como dos
fuentes, cuenta una sola copiada (minar-fuente §8).

Lee la LECTURA hecha a mano —qué dice Esteves de cada voz, con página, y qué
otra fuente hay— en `6-fusion/sigla_E_zavala_lectura_2026-09-23.yaml` (sin
cifras: regla 1) y escribe la medición en
`6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml` (GENERADO):

  1. EL GLOSARIO: cuántas entradas de Zavala llevan (E) y cuántas sólo (E),
     con las siglas leídas del PDF (`minar_zavala_glosario.extraer()`), no de
     las notas del lexicón.
  2. EL CANON: qué entradas de VOCABULARIO_BASE y FUERA_DEL_HABLA citan una
     entrada con (E), por capa; cuántas atestiguadas dependen sólo de (E),
     contadas de dos maneras (todas las entradas citadas en la nota / sólo las
     que dan la glosa de la voz, según la lectura) y la diferencia nombrada.
     Cobertura: toda voz con (E) tiene lectura, y toda lectura cita obras que
     existen en 4-fuentes/bibliografia.yaml (regla 8).
  3. LA ETIQUETA POR OPCIÓN, derivada de la lectura con reglas declaradas
     abajo (`opciones()`), y cuántas voces cambian con cada una.
  4. EL COSTE, medido: usos en la base (sólo SELECT, `word_uses`, la voz
     suelta y en compuestos, con la lógica de raíz del motor), exposición en
     las plantillas, en `[Tu tierra]` y en el muestreo del prompt (el ensayo
     de `medir_pares_atestiguado_reconstruido.py`, semilla fija), y las
     semillas de idiolecto derivadas que se mueven si una voz pasa a
     hipotética (la capa hipotética no siembra).
  5. LAS CONSECUENCIAS EN CADENA: los archivos de la política «manda la
     atestiguada» (par por par, leídos de FUERA_DEL_HABLA), los afijos que el
     prompt enseña (y qué le pasaría al desafijador si se retiraran), los
     `voz_caquetia` del canon del mundo que copian la capa, y los topónimos A/B
     del canon con una pieza sólo de Esteves.

Uso:
    python 6-fusion/scripts/medir_sigla_E_zavala.py
    python 6-fusion/scripts/medir_sigla_E_zavala.py --check
    python 6-fusion/scripts/medir_sigla_E_zavala.py --sin-base   # sin Supabase

LO QUE NO HACE: no toca `curiana_sim/` ni el canon (regla 5), no llama a la API
y no abre `curiana_sim/.env` (el `load_dotenv` de `curiana_database` se
neutraliza con un stub antes de importar nada), y a la base sólo le hace
SELECT por `docker exec … psql`. Los cambios de etiqueta y la retirada de un
afijo se SIMULAN en memoria, en este proceso, y se deshacen.
"""
from __future__ import annotations

import argparse
import collections
import importlib.util
import os
import re
import sys
import types

import yaml

# ── El motor, sin abrir .env ──────────────────────────────────────────────
if "dotenv" not in sys.modules:
    _stub = types.ModuleType("dotenv")
    _stub.load_dotenv = lambda *a, **k: None          # noqa: E731
    _stub.dotenv_values = lambda *a, **k: {}          # noqa: E731
    sys.modules["dotenv"] = _stub

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SIM = os.path.join(RAIZ, "curiana_sim")
if SIM not in sys.path:
    sys.path.insert(0, SIM)
os.environ.setdefault("CURIANA_ELENCO", "era2")

FECHA = "2026-09-23"
LECTURA = os.path.join(RAIZ, "6-fusion", f"sigla_E_zavala_lectura_{FECHA}.yaml")
SALIDA = os.path.join(RAIZ, "6-fusion", f"medicion_sigla_E_zavala_{FECHA}.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")
CANON_TOPONIMOS = os.path.join(RAIZ, "2-lengua", "toponimos.yaml")
MUNDO = [os.path.join(RAIZ, "6-fusion", n) for n in ("clima_era2.yaml", "sitios_era2.yaml")]

ATEST, RECON, RETRO, HIPO = ("caquetío-atestiguado", "caquetío-reconstruido",
                             "caquetío-retroabstraido", "caquetío-hipotético")
CUENTA_COMO_ATESTACION = {"independiente-verificada", "independiente-sigla"}
OTRA_FUENTE_MISMA_COSA = CUENTA_COMO_ATESTACION | {"independiente-fuera-del-area",
                                                    "analisis-nuestro"}
ESTADOS = OTRA_FUENTE_MISMA_COSA | {"forma-sin-glosa", "otro-referente", "copia-de-esteves"}
CLASES = {"etimologia-de-toponimo", "dice-en-caquetio", "voz-viva", "no-esta"}

# Piezas de los topónimos del canon → clave del lexicón (grafía de fuente a lema).
ALIAS_PIEZA = {"cari": "kari", "judi": "juri", "quiba": "kiba", "quiva": "kiba",
               "aco": "ako", "capu": "kapu", "bacoa": "bakoa", "guarataro": "warataro",
               "sigua": "siwa", "rao": "rao", "tuba": "tuba", "yabu": "yabo"}
PIEZA_AFIJO = {"uco": "-uco", "uto": "-uco", "duco": "-uco", "iro": "-iro", "ima": "-ima",
               "dito": "dito", "bana": "-bana", "ana": "-bana"}


def _forzar_utf8() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:                                     # noqa: BLE001
            pass


def leer(ruta):
    with open(ruta, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _mp():
    """El script hermano de los pares: su criterio de «enseñar», su ensayo de
    muestreo, su lectura de la base y su lógica de raíz (la del motor)."""
    spec = importlib.util.spec_from_file_location(
        "_medir_pares", os.path.join(AQUI, "medir_pares_atestiguado_reconstruido.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ══════════════════════════════════════════════════════════════════════
# 1-2. EL GLOSARIO Y EL CANON
# ══════════════════════════════════════════════════════════════════════
# Un número de Zavala en una nota: «Zavala Reyes 2015 #178», «glosario #219»,
# «#190 (E+HP)», «#92 «Cuiva…»». NO los issues de GitHub: «(#45)», «#101
# (tanda…», «#123 (Miguel…».
_ZREF = re.compile(r"(?:Zavala[^#]{0,40}?|glosario\s*)#\s?(\d{1,3})\b|#\s?(\d{1,3})\s*(?:\(|«|:)")
_NO_ZAVALA = re.compile(r"#\s?\d+\s*\((?:tanda|Miguel|decisi)")
# El regex de la medición del lote (siglas tal como las escribe la nota).
_SIGLAS_EN_NOTA = re.compile(r"#\s?\d+[^()]{0,40}\(([A-Z+ ]{1,20})\)")


def glosario():
    import minar_zavala_glosario as Z
    G = {e["num"]: e for e in Z.extraer()}
    con_e = sorted(n for n, e in G.items() if "E" in e["siglas"])
    solo_e = sorted(n for n in con_e if G[n]["siglas"] == ["E"])
    return G, con_e, solo_e


def nums_zavala(texto: str) -> list[int]:
    out = set()
    for m in _ZREF.finditer(texto or ""):
        n = int(m.group(1) or m.group(2))
        if 1 <= n <= 288 and not _NO_ZAVALA.match(texto[m.start():m.end() + 12]):
            out.add(n)
    return sorted(out)


def siglas_en_nota(texto: str) -> set:
    out = set()
    for grupo in _SIGLAS_EN_NOTA.findall(texto or ""):
        out.update(s for s in re.split(r"[+ ]+", grupo.strip()) if s)
    return out


def canon_con_E(L, G):
    filas = []
    for donde, D in (("VOCABULARIO_BASE", L.VOCABULARIO_BASE), ("FUERA_DEL_HABLA", L.FUERA_DEL_HABLA)):
        for k, d in D.items():
            if not isinstance(d, dict):
                continue
            texto = f"{d.get('notas', '')} {d.get('glosa_fuente', '')}"
            if "avala" not in texto:
                continue
            ns = nums_zavala(texto)
            sig = sorted({s for n in ns for s in G[n]["siglas"]})
            if "E" in sig:
                filas.append({"clave": k, "donde": donde, "capa": d.get("fuente"),
                              "zavala_citadas": ns, "siglas_del_pdf": sig,
                              "siglas_en_la_nota": sorted(siglas_en_nota(texto)) or None})
    return filas


# ══════════════════════════════════════════════════════════════════════
# 3. LAS OPCIONES — reglas declaradas
# ══════════════════════════════════════════════════════════════════════
def derivar(v: dict) -> dict:
    """De la lectura de UNA voz, lo que cuenta y la etiqueta de cada opción.

    - independientes: las otras atestaciones que CUENTAN como atestación caquetía
      (otra sigla de Zavala, u otra obra leída con la misma palabra y la misma
      cosa en el área).
    - otra_fuente_misma_cosa: lo anterior, más la voz documentada fuera del
      área y la forma independiente que partimos nosotros. Es lo que el lote
      del 2026-09-22 pide para que una pieza de un topónimo no sea «sólo de
      Esteves».
    Opciones:
      A — «degradar todas»: sin atestación independiente → hipotético.
      B — «por lo que hace Esteves con cada una» (la recomendada): sin
          atestación independiente → reconstruido si una forma independiente
          la corrobora, retroabstraído si es voz viva, hipotético si es
          etimología de topónimo, dicho sin fuente o no está.
      C — «marcar sin degradar»: la capa no cambia; la nota y la procedencia
          pasan a decir Esteves 1989 con su página.
      D — «degradar sólo las etimologías»: sin atestación independiente y
          etimología/dicho/no-está sin corroborar → hipotético; las voces
          vivas y las corroboradas se quedan.
    """
    otras = v.get("otras_atestaciones") or []
    indep = [o for o in otras if o["estado"] in CUENTA_COMO_ATESTACION]
    misma_cosa = [o for o in otras if o["estado"] in OTRA_FUENTE_MISMA_COSA]
    corroborada = any(o["estado"] == "analisis-nuestro" for o in otras)
    clase = v["esteves"]["clase"]
    if indep:
        a = b = d = None                       # se sostiene
    else:
        a = HIPO
        if corroborada:
            b = RECON
        elif clase == "voz-viva":
            b = RETRO
        else:
            b = HIPO
        d = None if (clase == "voz-viva" or corroborada) else HIPO
        if v.get("forzar_B"):
            b = v["forzar_B"]
    return {"independientes": len(indep), "otra_fuente_misma_cosa": bool(misma_cosa),
            "corroborada_por_una_forma": corroborada,
            "copias_de_esteves": sum(1 for o in otras if o["estado"] == "copia-de-esteves"),
            "A": a, "B": b, "C": None, "D": d}


def capa_por_opcion(capa_hoy: str, der: dict, op: str) -> str:
    nueva = der[op]
    return capa_hoy if nueva is None else nueva


# ══════════════════════════════════════════════════════════════════════
# 4. EL COSTE
# ══════════════════════════════════════════════════════════════════════
def usos_por_raiz(MP, raices, usos, runs):
    """Suelta + compuestos por raíz, con el criterio de familia del motor."""
    tokens = sorted({w for _r, w, _n in usos})
    indice = collections.defaultdict(list)
    for tok in tokens:
        for raiz in raices:
            rol = MP.rol_en_la_familia(tok, raiz)
            if rol:
                indice[tok].append((raiz, rol))
    acum = {r: {"suelta": 0, "compuestos": 0, "total": 0, "era_2": 0, "runs": set(),
                "formas": collections.Counter()} for r in raices}
    for rid, tok, n in usos:
        for raiz, rol in indice.get(tok, []):
            a = acum[raiz]
            a["total"] += n
            a["suelta" if rol == "suelta" else "compuestos"] += n
            a["runs"].add(rid)
            if runs.get(rid, {}).get("elenco") == "era2":
                a["era_2"] += n
            if rol != "suelta":
                a["formas"][tok] += n
    out = {}
    for r, a in acum.items():
        d = {"total": a["total"], "suelta": a["suelta"], "compuestos": a["compuestos"],
             "en_la_era_2": a["era_2"], "runs": len(a["runs"])}
        top = sorted(a["formas"].items(), key=lambda kv: (-kv[1], kv[0]))[:5]
        if top:
            d["compuestos_mas_usados"] = {k: v for k, v in top}
        out[r] = d
    return out


def usos_de_afijo(usos, afijo: str) -> dict:
    seg = afijo.strip("-")
    formas = collections.Counter()
    for _rid, tok, n in usos:
        partes = tok.split("-")
        if len(partes) > 1 and seg in partes[1:]:
            formas[tok] += n
    top = sorted(formas.items(), key=lambda kv: (-kv[1], kv[0]))[:6]
    return {"usos": sum(formas.values()), "formas": len(formas),
            "mas_usadas": {k: v for k, v in top} or None}


def retirar_afijo(L, usos, afijo: str) -> dict:
    """Qué le pasa al desafijador si el afijo sale de TODAS_LAS_REGLAS (como
    -ko y -sha el 2026-09-14). Simulado en memoria y deshecho."""
    tokens = collections.Counter()
    for _rid, tok, n in usos:
        tokens[tok] += n
    antes = {t: (L._familia_de_token(t), L.es_raiz_de_ninguna_parte(t, archivadas_avalan=False))
             for t in tokens}
    s0, a0 = L._SUFIJOS_CAQ, L._AFIJOS_SUELTOS
    try:
        L._SUFIJOS_CAQ = frozenset(x for x in s0 if x != afijo)
        L._AFIJOS_SUELTOS = frozenset(x for x in a0 if x != afijo.strip("-"))
        despues = {t: (L._familia_de_token(t), L.es_raiz_de_ninguna_parte(t, archivadas_avalan=False))
                   for t in tokens}
    finally:
        L._SUFIJOS_CAQ, L._AFIJOS_SUELTOS = s0, a0
    cambia_lengua = sorted(t for t in tokens if antes[t][0] != despues[t][0])
    cambia_puerta = sorted(t for t in tokens if antes[t][1] != despues[t][1])
    ej = collections.Counter()
    for t in cambia_lengua:
        ej[f"{antes[t][0]}→{despues[t][0]}"] += 1
    return {"formas_que_cambian_de_lengua": len(cambia_lengua),
            "usos_que_cambian_de_lengua": sum(tokens[t] for t in cambia_lengua),
            "cambios": dict(ej) or None,
            "ejemplos": cambia_lengua[:8] or None,
            "formas_que_cambian_en_la_puerta_de_raiz": len(cambia_puerta),
            "ejemplos_puerta": cambia_puerta[:8] or None}


def semillas_que_se_mueven(nuevas_capas: dict) -> dict:
    """Semillas de idiolecto (era 2) que cambian si estas voces cambian de
    capa: la capa hipotética no siembra (`curiana_koine.CAPAS_DE_SEMILLA`).

    Ojo al mecanismo, que es lo que se mide: la semilla DERIVADA se sortea
    con `_dado(...) % len(pool)` sobre el campo del oficio, así que sacar una
    sola voz del pool re-sortea a casi todo el que deriva, lleve o no esa voz.
    Por eso se da también cuántas semillas contenían alguna de las voces."""
    import curiana_koine as K
    import curiana_lexicon as L
    agentes = sorted(getattr(K._elenco()[0], "keys", lambda: [])())

    def foto():
        K._vocabulario_cache = None
        K._cache_derivadas.clear()
        K._cache_emocionar.clear()
        return {a: tuple(K.formas_semilla(a, K.emocionar_de(a))) for a in agentes}

    antes = foto()
    determinista = antes == foto()
    viejas = {}
    try:
        for k, capa in nuevas_capas.items():
            if k in L.VOCABULARIO_BASE:
                viejas[k] = L.VOCABULARIO_BASE[k].get("fuente")
                L.VOCABULARIO_BASE[k]["fuente"] = capa
        despues = foto()
    finally:
        for k, f in viejas.items():
            L.VOCABULARIO_BASE[k]["fuente"] = f
        foto()
    cambian = sorted(a for a in agentes if antes[a] != despues[a])

    def lleva(sem):
        return any(p in nuevas_capas for f in sem for p in f.split("-"))
    escritas = sum(1 for a in agentes if K.formas_seed_de(a))
    return {"agentes": len(agentes), "con_semilla_escrita": escritas,
            "control_determinista": determinista,
            "semillas_que_cambian": len(cambian),
            "semillas_que_llevaban_alguna_de_estas_voces": sum(1 for a in agentes if lleva(antes[a]))}


def voz_en_el_mundo(claves) -> dict:
    """Los `voz_caquetia: {clave, capa}` del canon del mundo (copian la capa)
    y las frases del cargador que dicen la voz."""
    out = {}
    for ruta in MUNDO:
        texto = open(ruta, encoding="utf-8").read()
        nombre = os.path.basename(ruta)
        for k in claves:
            n_voz = len(re.findall(r"voz_caquetia:\s*\{clave:\s*" + re.escape(k) + r"\s*,", texto))
            if n_voz:
                out.setdefault(k, {})[f"{nombre}:voz_caquetia"] = n_voz
    clima = leer(MUNDO[0])
    frases = []
    for periodo, f in (clima.get("frases_del_cargador") or {}).items():
        frases.append((f"{periodo}.periodo", str(f.get("periodo") or "")))
        for mom, t in (f.get("momentos") or {}).items():
            frases.append((f"{periodo}.{mom}", str(t)))
    for k in claves:
        rx = re.compile(r"(?<![\wáéíóúüñ])" + re.escape(k) + r"(?![\wáéíóúüñ])", re.I)
        dichas = [n for n, t in frases if rx.search(t)]
        if dichas:
            out.setdefault(k, {})["clima_era2.yaml:frases_del_cargador"] = dichas
    return out


# ══════════════════════════════════════════════════════════════════════
# 5. LA CADENA
# ══════════════════════════════════════════════════════════════════════
def politica(L, capas_por_opcion) -> list:
    out = []
    for k, d in L.FUERA_DEL_HABLA.items():
        a = str(d.get("archivada") or "")
        m = re.search(r"atestiguado-manda · par (\d+) «([^»]+)» · manda `([^`]+)`", a)
        if not m:
            continue
        par, glosa, manda = int(m.group(1)), m.group(2), m.group(3)
        fila = {"par": par, "glosa": glosa, "archivada": k, "manda": manda,
                "capa_de_la_archivada": d.get("fuente"),
                "deuda_d11_en_su_nota": "D11" in str(d.get("notas") or "")}
        veredicto = {}
        for op, capas in capas_por_opcion.items():
            c = capas.get(manda, L.VOCABULARIO_BASE.get(manda, {}).get("fuente"))
            veredicto[op] = "se sostiene" if c == ATEST else f"se cae ({c})"
        fila["por_opcion"] = veredicto
        out.append(fila)
    return sorted(out, key=lambda f: f["par"])


def piezas_de(t: dict) -> list[str]:
    piezas = set((t.get("morfemas") or {}).keys())
    seg = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", str(t.get("segmentacion") or ""))
    piezas.update(p for p in re.split(r"[\s+~]+", seg.lower()) if p)
    return sorted(p.strip("-").lower() for p in piezas if p.strip("-"))


def pieza_independiente(v: dict) -> bool:
    """¿La pieza de un topónimo está en OTRA fuente con glosa compatible?

    La regla del lote del 2026-09-22: otra sigla, u otra obra con la misma
    cosa —aunque sea de fuera del área: aquí se juzga la voz, no su
    filiación—, o una forma independiente cuya glosa ya es compatible
    (`glosa_compatible`). Una forma que sólo partimos nosotros NO basta.
    """
    for o in v.get("otras_atestaciones") or []:
        if o["estado"] in CUENTA_COMO_ATESTACION | {"independiente-fuera-del-area"}:
            return True
        if o["estado"] == "analisis-nuestro" and o.get("glosa_compatible"):
            return True
    return False


def toponimos(lect, derivadas, capas_b) -> dict:
    canon = leer(CANON_TOPONIMOS)["toponimos"]
    todas = {**lect["voces"], **lect["afijos"]}
    solo_esteves = {k for k, v in lect["voces"].items() if not pieza_independiente(v)}
    acepciones = {k: v.get("acepcion_solo_de_esteves") for k, v in lect["voces"].items()
                  if v.get("acepcion_solo_de_esteves")}
    afijos_solo = {a for a in lect["afijos"] if not pieza_independiente(todas[a])}
    marcados = []
    for t in canon:
        if t.get("nivel") not in ("A", "B"):
            continue
        debiles = []
        for p in piezas_de(t):
            clave = ALIAS_PIEZA.get(p, p)
            if clave in solo_esteves:
                debiles.append(f"{p} ({clave}: sólo Esteves)")
            elif clave in acepciones:
                debiles.append(f"{p} ({clave}: la acepción «{acepciones[clave]}» es sólo de Esteves)")
            elif PIEZA_AFIJO.get(p) in afijos_solo:
                debiles.append(f"{p} ({PIEZA_AFIJO[p]}: sólo Esteves)")
        if debiles:
            veredicto = (lect.get("toponimos") or {}).get(t["id"]) or {}
            marcados.append({"id": t["id"], "forma": t["forma"], "nivel_hoy": t["nivel"],
                             "procedencia": (t.get("procedencia") or {}).get("obra"),
                             "piezas_solo_de_esteves": debiles,
                             "propuesta": veredicto.get("propuesta"),
                             "razon": veredicto.get("razon")})
    ids = {m["id"] for m in marcados}
    sin_veredicto = sorted(m["id"] for m in marcados if not m["propuesta"])
    veredicto_de_mas = sorted(set(lect.get("toponimos") or {}) - ids)
    return {"a_y_b_en_el_canon": sum(1 for t in canon if t.get("nivel") in ("A", "B")),
            "con_una_pieza_solo_de_esteves": len(marcados),
            "bajan": sum(1 for m in marcados if m["propuesta"] and m["propuesta"] != m["nivel_hoy"]),
            "se_quedan": sum(1 for m in marcados if m["propuesta"] == m["nivel_hoy"]),
            "control_sin_veredicto": sin_veredicto or None,
            "control_veredicto_sin_marca": veredicto_de_mas or None,
            "por_toponimo": marcados}


# ══════════════════════════════════════════════════════════════════════
# LA MEDICIÓN
# ══════════════════════════════════════════════════════════════════════
def medir(sin_base: bool = False) -> dict:
    import curiana_lexicon as L
    MP = _mp()
    lect = leer(LECTURA)
    biblio = {o["id"] for o in leer(BIBLIO)["obras"]}
    G, con_e, solo_e = glosario()
    V, F = L.VOCABULARIO_BASE, L.FUERA_DEL_HABLA

    # ── 2. el canon ──────────────────────────────────────────────────────
    filas = canon_con_E(L, G)
    atest = [k for k, d in V.items() if isinstance(d, dict) and d.get("fuente") == ATEST]
    voces = lect["voces"]
    afijos = lect["afijos"]
    controles = {"obras_que_no_estan_en_la_bibliografia": sorted({
        o["obra"] for v in list(voces.values()) + list(afijos.values())
        for o in v.get("otras_atestaciones") or [] if o.get("obra") and o["obra"] not in biblio}) or None}
    malos = sorted(f"{k}:{o['estado']}" for k, v in list(voces.items()) + list(afijos.items())
                   for o in v.get("otras_atestaciones") or [] if o["estado"] not in ESTADOS)
    malas_clases = sorted(k for k, v in list(voces.items()) + list(afijos.items())
                          if v["esteves"]["clase"] not in CLASES)
    controles["estados_desconocidos"] = malos or None
    controles["clases_desconocidas"] = malas_clases or None
    en_canon = {f["clave"] for f in filas if f["donde"] == "VOCABULARIO_BASE"}
    # La lectura cubre toda voz del habla con (E), salvo la que sólo CITA una
    # entrada ajena en su nota (kuru nombra a bara para declarar convivencia).
    ajenas = sorted(k for k in en_canon - set(voces)
                    if not (set(G[n]["lemas"][0].lower() for n in next(
                        f for f in filas if f["clave"] == k)["zavala_citadas"])
                            & {k, str(V[k].get("forma_fuente") or "").lower()}))
    controles["voces_con_E_sin_lectura"] = sorted(en_canon - set(voces) - set(ajenas)) or None
    controles["citan_una_entrada_E_ajena_(no_es_su_atestacion)"] = ajenas or None
    controles["lecturas_sin_voz_en_el_canon"] = sorted(set(voces) - set(V)) or None

    solo_e_nota = sorted(f["clave"] for f in filas if f["donde"] == "VOCABULARIO_BASE"
                         and f["capa"] == ATEST and f["siglas_del_pdf"] == ["E"])
    solo_e_propias = sorted(k for k, v in voces.items() if k in V and V[k].get("fuente") == ATEST
                            and all(G[n]["siglas"] == ["E"] for n in v["zavala"]))
    notas_lote = sorted(f["clave"] for f in filas if f["donde"] == "VOCABULARIO_BASE" and f["capa"] == ATEST
                        and f["siglas_en_la_nota"] and set(f["siglas_en_la_nota"]) <= {"E"})

    # ── 3. derivación por voz ────────────────────────────────────────────
    derivadas = {k: derivar(v) for k, v in voces.items()}
    derivadas.update({a: derivar(v) for a, v in afijos.items()})
    capa_hoy = {k: V[k]["fuente"] for k in voces if k in V}
    ops = ("A", "B", "C", "D")
    capas_por_opcion = {op: {k: capa_por_opcion(capa_hoy[k], derivadas[k], op) for k in capa_hoy}
                        for op in ops}
    cambios = {op: {k: c for k, c in capas_por_opcion[op].items() if c != capa_hoy[k]} for op in ops}

    # ── 4. coste ─────────────────────────────────────────────────────────
    raices = sorted(capa_hoy)
    formas = set(raices)
    exp_plant = MP.exposicion_plantillas(formas)
    exp_tierra = MP.exposicion_tu_tierra(formas)
    exp_muestreo = MP.ensayo_de_muestreo(formas)
    usos, runs, uso = [], {}, {}
    if not sin_base:
        runs = MP.leer_runs()
        usos = MP.leer_usos()
        uso = usos_por_raiz(MP, raices, usos, runs)
    mundo = voz_en_el_mundo(raices)

    fichas = []
    for k in sorted(voces, key=lambda x: (capa_hoy.get(x) != ATEST, x)):
        v = voces[k]
        d = derivadas[k]
        f = {"clave": k,
             "capa_hoy": capa_hoy.get(k),
             "zavala": [f"#{n} {G[n]['lemas'][0]} ({'+'.join(G[n]['siglas']) or 's/sigla'}): {G[n]['definicion']}"
                        for n in v["zavala"]],
             "solo_E": all(G[n]["siglas"] == ["E"] for n in v["zavala"]),
             "esteves": {"paginas": v["esteves"]["paginas"], "clase": v["esteves"]["clase"],
                         "verificado": v["esteves"].get("verificado"),
                         "lo_que_dice": " ".join(str(v["esteves"]["lo_que_dice"]).split())},
             "atestaciones_independientes": d["independientes"],
             "otras": [f"{o.get('obra') or '—'}{(' p. ' + str(o['pagina'])) if o.get('pagina') else ''}: "
                       f"{o['dice']} [{o['estado']}]" for o in v.get("otras_atestaciones") or []] or None,
             "etiqueta_por_opcion": {op: capas_por_opcion[op].get(k) for op in ops},
             "uso_en_la_base": uso.get(k),
             "exposicion": {
                 "plantillas_que_la_ensenan": exp_plant[k]["ensena"] or None,
                 "plantillas_donde_sale_sin_glosa": exp_plant[k]["solo_como_token"] or None,
                 "tu_tierra_bloques_que_la_dicen": exp_tierra["token"][k],
                 "muestreo_prompts_era2": exp_muestreo["en_muestreo"][k],
                 "prompt_entero_prompts_era2": exp_muestreo["en_prompt"][k],
                 "canon_del_mundo": mundo.get(k)},
             }
        for extra in ("nota", "castellano_probable", "razon_forzar_B", "acepcion_solo_de_esteves"):
            if v.get(extra):
                f[extra] = " ".join(str(v[extra]).split())
        fichas.append(f)

    def resumen_opcion(op):
        c = cambios[op]
        destino = collections.Counter(c.values())
        a_hipo = sorted(k for k, capa in c.items() if capa == HIPO)
        perdida = sum(exp_muestreo["en_muestreo"][k] for k in a_hipo)
        ensenadas = sorted(k for k in c if exp_plant[k]["ensena"] or exp_plant[k]["solo_como_token"])
        return {"cambian_de_capa": len(c), "a": dict(sorted(destino.items())),
                "salen_de_la_capa_atestiguada": sum(1 for k in c if capa_hoy[k] == ATEST),
                "atestiguadas_del_lexicon_despues": len(atest) - sum(1 for k in c if capa_hoy[k] == ATEST),
                "pasan_a_hipotetica_(salen_del_perfil_era2)": a_hipo or None,
                "apariciones_en_el_muestreo_del_ensayo_que_se_pierden": perdida,
                "usos_en_la_base_de_las_que_cambian": (sum(uso[k]["total"] for k in c) if uso else None),
                "usos_en_la_base_de_las_que_pasan_a_hipotetica": (sum(uso[k]["total"] for k in a_hipo)
                                                                   if uso else None),
                "cambian_y_alguna_plantilla_la_ensena": ensenadas or None,
                "voces": {k: v for k, v in sorted(c.items())} or None}

    por_opcion = {op: resumen_opcion(op) for op in ops}
    semillas = {op: semillas_que_se_mueven({k: HIPO for k in (por_opcion[op]["pasan_a_hipotetica_(salen_del_perfil_era2)"] or [])})
                for op in ("A", "B", "D")}

    # ── 5. afijos ────────────────────────────────────────────────────────
    af = {}
    for a, v in afijos.items():
        d = derivadas[a]
        regla = L.TODAS_LAS_REGLAS.get(a) or {}
        fila = {"donde": v["donde"],
                "zavala": [f"#{n} {G[n]['lemas'][0]} ({'+'.join(G[n]['siglas'])}): {G[n]['definicion']}"
                           for n in v["zavala"]],
                "esteves": {"paginas": v["esteves"]["paginas"], "clase": v["esteves"]["clase"],
                            "lo_que_dice": " ".join(str(v["esteves"]["lo_que_dice"]).split())},
                "atestaciones_independientes": d["independientes"],
                "copias_de_esteves": d["copias_de_esteves"],
                "otras": [f"{o.get('obra') or '—'}: {o['dice']} [{o['estado']}]"
                          for o in v.get("otras_atestaciones") or []] or None,
                "etiqueta_por_opcion": {op: ("se sostiene" if d[op] is None else d[op]) for op in ops},
                "lo_que_dice_hoy_el_motor": regla.get("atestiguado") or regla.get("evidencia"),
                "en_AFIJOS_ATESTIGUADOS": a in L.AFIJOS_ATESTIGUADOS}
        if a in L.AFIJOS_ATESTIGUADOS:
            linea_t1 = L._linea_afijo(a, L.AFIJOS_ATESTIGUADOS[a])
            fila["linea_que_enseña_al_tier_1"] = linea_t1
            fila["caracteres_de_esa_linea"] = len(linea_t1) + 5
            breve = L.prompt_afijos_atestiguados_breve()
            fila["en_la_linea_breve_de_los_63"] = a in breve
        if usos:
            fila["uso_en_la_base"] = usos_de_afijo(usos, a)
            # Sólo para los que CAMBIAN de etiqueta: retirar uno que se
            # sostiene no es ninguna de las opciones.
            if a in L.TODAS_LAS_REGLAS and a.startswith("-") and d["B"] is not None:
                fila["si_se_retirara_de_TODAS_LAS_REGLAS"] = retirar_afijo(L, usos, a)
        af[a] = fila

    # ── cadena ───────────────────────────────────────────────────────────
    cadena = {
        "politica_manda_la_atestiguada": politica(L, capas_por_opcion),
        "plantillas_que_ensenan_una_voz_que_cambia_con_B": {
            k: exp_plant[k]["ensena"] for k in sorted(cambios["B"]) if exp_plant[k]["ensena"]} or None,
        "canon_del_mundo_que_copia_la_capa_de_una_voz_que_cambia_con_B": {
            k: mundo[k] for k in sorted(cambios["B"]) if k in mundo} or None,
        "semillas_de_idiolecto_derivadas": semillas,
        "formas_seed_escritas_con_una_voz_que_cambia_con_B": _seed_escritas(set(cambios["B"])),
        "reglas_cuyo_ejemplo_o_instruccion_usa_una_voz_que_cambia_con_B": _reglas_con(L, set(cambios["B"])),
    }

    return {
        "meta": {
            "generado_por": "6-fusion/scripts/medir_sigla_E_zavala.py",
            "editar_a_mano": "no — se edita la lectura o el script y se regenera",
            "lectura": os.path.relpath(LECTURA, RAIZ).replace(os.sep, "/"),
            "decision": "cc.4 (6-fusion/decisiones_cierre_2026-09-23.yaml) → opción 1-A del issue "
                        "toponimos-esteves-lote-2026-09-22.md",
            "base": ("sin consultar (--sin-base)" if sin_base else
                     "Supabase local, sólo SELECT: word_uses (lo que el scorer reconoció; una voz dicha y no "
                     "reconocida no está ahí)"),
            "ensayo_de_muestreo": {"prompts": exp_muestreo["prompts"], "semilla": exp_muestreo["semilla"],
                                   "perfil": "era2 (atestiguado + reconstruido + retroabstraído: la "
                                             "hipotética NO entra)",
                                   "de_donde": "medir_pares_atestiguado_reconstruido.ensayo_de_muestreo(): "
                                               "63 agentes × 20 sorteos, sin API"},
            "uso_en_la_base_criterio": "una forma cuenta para una voz si ES la voz, si la lleva como uno de "
                                       "sus segmentos separados por guion, o si la voz es uno de los "
                                       "candidatos de raíz del desafijador "
                                       "(medir_pares_atestiguado_reconstruido.rol_en_la_familia). Residuo: "
                                       "las formas aglutinadas sin guion no cuentan.",
            "el_score_no_se_mueve": "score_linguistico() no lee la capa: capas_de_score tiene las cuatro "
                                    "(5-experimento/perfiles_de_run.yaml). La capa decide lo que el agente VE "
                                    "(el muestreo del perfil) y lo que siembra la koiné, no lo que puntúa.",
        },
        "glosario_zavala": {
            "entradas": len(G), "con_sigla_E": len(con_e), "solo_sigla_E": len(solo_e),
            "solo_E": [f"#{n} {G[n]['lemas'][0]}" for n in solo_e],
            "E_con_otra_sigla": [f"#{n} {G[n]['lemas'][0]} ({'+'.join(G[n]['siglas'])})"
                                 for n in con_e if n not in solo_e]},
        "el_canon": {
            "caquetio_atestiguado_en_VOCABULARIO_BASE": len(atest),
            "entradas_que_citan_una_E": {
                "por_capa": dict(collections.Counter(f"{f['donde']} · {f['capa']}" for f in filas)),
                "claves": sorted(f["clave"] for f in filas)},
            "atestiguadas_solo_E": {
                "contando_todas_las_entradas_que_cita_la_nota": len(solo_e_nota),
                "contando_solo_las_que_dan_su_glosa_(lectura)": len(solo_e_propias),
                "con_las_siglas_escritas_en_la_nota_(criterio_del_lote)": len(notas_lote),
                "diferencias": {
                    "solo_por_su_glosa_pero_la_nota_cita_otra_sigla":
                        sorted(set(solo_e_propias) - set(solo_e_nota)) or None,
                    "la_nota_no_dice_E_o_dice_otra": sorted(set(solo_e_propias) - set(notas_lote)) or None,
                    "la_nota_dice_solo_E_y_no_lo_es": sorted(set(notas_lote) - set(solo_e_propias)) or None},
                "claves": solo_e_propias},
            "controles": controles,
        },
        "por_opcion": por_opcion,
        "voces": fichas,
        "afijos": af,
        "cadena": cadena,
        "toponimos": toponimos(lect, derivadas, capas_por_opcion["B"]),
    }


def _reglas_con(L, claves: set):
    """Las reglas de TODAS_LAS_REGLAS cuyo ejemplo, uso o instrucción dice
    una de estas voces (p. ej. «ka + juri = ka-juri (hay viento)»)."""
    out = {}
    for regla, d in L.TODAS_LAS_REGLAS.items():
        texto = " ".join([*(d.get("ejemplos") or []), str(d.get("uso") or ""),
                          str(d.get("instruccion_agente") or "")])
        toks = {t for w in re.findall(r"[a-zA-Záéíóúüñ][a-zA-Záéíóúüñ-]*", texto.lower())
                for t in [w, *w.split("-")]}
        dice = sorted(toks & claves)
        if dice:
            out[regla] = dice
    return out or None


def _seed_escritas(claves: set):
    import curiana_koine as K
    out = {}
    for agente, formas in K.FORMAS_SEED.items():
        for f in formas:
            if f in claves or any(p in claves for p in f.split("-")):
                out.setdefault(f, []).append(agente)
    return {k: len(v) for k, v in sorted(out.items())} or None


def volcar(d) -> str:
    cab = ("# GENERADO por 6-fusion/scripts/medir_sigla_E_zavala.py — no editar a mano.\n"
           "# La sigla (E) de Zavala es Esteves: el canon re-medido (cc.4). La lectura voz por voz\n"
           "# es 6-fusion/sigla_E_zavala_lectura_2026-09-23.yaml; las opciones, en el issue\n"
           "# 6-fusion/issues-pendientes/sigla-E-zavala-canon-2026-09-23.md.\n")
    return cab + yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=110)


def main(argv=None) -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="¿la medición escrita está al día?")
    ap.add_argument("--sin-base", action="store_true", help="no consulta Supabase")
    a = ap.parse_args(argv)
    texto = volcar(medir(sin_base=a.sin_base))
    if a.check:
        with open(SALIDA, encoding="utf-8") as fh:
            ok = fh.read() == texto
        print("✓ al día" if ok else "✗ desfasada: regenerar")
        return 0 if ok else 1
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)
    d = yaml.safe_load(texto)
    print(f"✓ {os.path.relpath(SALIDA, RAIZ)}")
    print("  glosario:", {k: v for k, v in d["glosario_zavala"].items() if isinstance(v, int)})
    ec = d["el_canon"]
    print("  canon:", ec["caquetio_atestiguado_en_VOCABULARIO_BASE"], "atestiguadas;",
          {k: v for k, v in ec["atestiguadas_solo_E"].items() if isinstance(v, int)})
    print("  controles:", ec["controles"])
    for op, r in d["por_opcion"].items():
        print(f"  opción {op}: cambian {r['cambian_de_capa']} {r['a']}")
    t = d["toponimos"]
    print("  topónimos:", {k: v for k, v in t.items() if not isinstance(v, list)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
