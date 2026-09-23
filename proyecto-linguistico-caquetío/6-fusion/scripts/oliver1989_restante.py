#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — Oliver 1989, lo que quedaba a medias: el barrido medido
=================================================================

Tercera campaña de minería, parcela **M1** (2026-09-22). Emite TODAS las cifras
que citan `6-fusion/oliver1989_lexico_restante_2026-09-22.yaml`,
`6-fusion/oliver1989_restante_2026-09-22.yaml` y su issue
(`6-fusion/issues-pendientes/oliver1989-restante-2026-09-22.md`). Ninguna cifra
de esos documentos está escrita a mano (regla 1).

QUÉ MIDE
--------
a9_vs_lexicon   cada una de las 50 filas de la Tabla A-9 (leídas en imagen)
                contra el lexicón: activa en VOCABULARIO_BASE (por clave,
                `forma_fuente` o variante), archivada en FUERA_DEL_HABLA, sólo
                referencia (tablas de Zavala / topónimos) o ausente.
a9_vs_dictado   la A-9 verificada contra `6-fusion/tabla_a9_oliver.yaml` (el
                dictado de 2026-08-15/24): qué filas faltaban, cuántas cursivas.
c1_c3           C1 (/d-/ y no /t-/) y C3 (/b-/ y no /p-/) puestas a predecir
                sobre las iniciales de la A-9 NO cursiva y de las claves
                caquetío-atestiguado del lexicón.
a8_aritmetica   los seis porcentajes impresos de la Tabla 8 contra su fracción.
tabla15         la Tabla 15 leída en el escaneo de 1989 contra
                `6-fusion/tabla15_c14_oliver.yaml` (sacada del .DOC «recalibrado»).
fauna           las entradas `fauna:` por obra y por época.
mar             en qué ventanas de texto coinciden una palabra del MAR y una de
                la CREENCIA, en el cap. 3 (DOC, pdftotext), el cap. 4 y el
                cap. 3 §3.2.3/§3.3 (OCR). El cero de «el mar en la creencia» se
                mide aquí.
ortografia      controles positivos: que las dianas de nombre propio SÍ salen
                en cada texto antes de creerse un cero (minar-fuente §2).
antillas        menciones de las Antillas Mayores frente a las ABC en el cap. 4.
voces_cap4      Túcua y zazare en el lexicón y en la mesa de topónimos.

No escribe en el canon: escribe sólo su medición.

Uso:
    python 6-fusion/scripts/oliver1989_restante.py            # escribe la medición
    python 6-fusion/scripts/oliver1989_restante.py --check    # mide sin escribir
"""

import argparse
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
SIM = os.path.join(REPO, "curiana_sim")
FUS = os.path.join(REPO, "6-fusion")
FUENTES = os.path.join(REPO, "fuentes_caquetios")
sys.path.insert(0, SIM)

LEXICO_YAML = os.path.join(FUS, "oliver1989_lexico_restante_2026-09-22.yaml")
MUNDO_YAML = os.path.join(FUS, "oliver1989_restante_2026-09-22.yaml")
DICTADO_YAML = os.path.join(FUS, "tabla_a9_oliver.yaml")
T15_YAML = os.path.join(FUS, "tabla15_c14_oliver.yaml")
SALIDA = os.path.join(FUS, "medicion_oliver1989_restante_2026-09-22.yaml")

CAP3_DOC = os.path.join(FUENTES, "Chapter 3 Ethnohistory.DOC-comprimido.pdf")
OCR = {
    "cap3_s323_chibchas": os.path.join(FUENTES, "Oliver_1989_cap3_s323_chibchas.ocr.txt"),
    "cap3_s324_caribes": os.path.join(FUENTES, "Oliver_1989_cap3_s324_caribes.ocr.txt"),
    "cap3_s33_falcon_lara": os.path.join(FUENTES, "Oliver_1989_cap3_s33_falcon_lara.ocr.txt"),
    "cap4_s47_s415": os.path.join(FUENTES, "Oliver_1989_cap4_s47_s415_dabajuroide.ocr.txt"),
}


def _forzar_utf8():
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(flujo.buffer, encoding="utf-8",
                                                  errors="replace", line_buffering=True))


def norm(s):
    """Para BUSCAR, no para hacer lemas: minúsculas, ç→s, sin diacríticos ni guiones."""
    s = (s or "").lower().replace("ç", "s")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z]", "", s)


def cargar(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ─────────────────────────────────────────────────────────────── el lexicón
def indice_lexicon():
    import curiana_lexicon as L
    idx = {}

    def poner(forma, donde, clave, fuente, glosa):
        n = norm(forma)
        if n:
            idx.setdefault(n, []).append({"donde": donde, "clave": clave,
                                          "fuente": fuente, "glosa": (glosa or "")[:70]})

    for k, e in L.VOCABULARIO_BASE.items():
        g = e.get("sig") or e.get("es")
        for f in [k, e.get("forma_fuente")] + list(e.get("variantes") or []):
            if f:
                poner(f, "VOCABULARIO_BASE", k, e.get("fuente"), g)
    for k, e in (getattr(L, "FUERA_DEL_HABLA", {}) or {}).items():
        poner(k, "FUERA_DEL_HABLA", k, e.get("fuente"), e.get("sig") or e.get("es"))
    try:
        import lexicon_zavala as Z
        for tabla in ("TOPONIMOS_ZAVALA", "ANTROPONIMOS_ZAVALA", "DESCARTADOS_ZAVALA"):
            for k, g in getattr(Z, tabla, {}).items():
                poner(k, tabla, k, "zavala-referencia", g)
    except ImportError:
        pass
    try:
        import lexicon_toponimos as T
        for tabla in ("NIVEL_A", "NIVEL_B", "NIVEL_C", "DESCARTES", "ANTROPONIMOS"):
            for k in getattr(T, tabla, {}):
                poner(k, "lexicon_toponimos." + tabla, k, "toponimo", "")
    except ImportError:
        pass
    return idx


def formas_de_fila(e, c_cedilla_como_c=False):
    """Las formas con que se busca una fila. `norm` lee la ç como /s/ (así la
    transcribe Oliver: çabana → sabana); con `c_cedilla_como_c` se lee como el
    extractor que la pierde (çabana → cabana), para medir ese caso aparte."""
    if c_cedilla_como_c:
        e = dict(e, forma=str(e.get("forma") or "").replace("ç", "c").replace("Ç", "C"))
    cands = set()
    for campo in ("forma", "fonemica"):
        v = str(e.get(campo) or "")
        v = re.sub(r"\(also [^)]*\)", "", v)
        for x in re.split(r"[/,]", v):
            x = x.strip()
            if not x:
                continue
            cands.add(norm(x))
            cands.add(norm(re.sub(r"\([^)]*\)", "", x)))
    # bariqui/e → barique; bariki/-ke → barike
    f = str(e.get("forma") or "")
    if re.search(r"/[a-z]$", f):
        base, fin = f.rsplit("/", 1)
        cands.add(norm(base[:-1] + fin))
    return {c for c in cands if len(c) >= 3}


def estado_de(hits):
    if not hits:
        return "ausente"
    dondes = {h["donde"] for h in hits}
    if "VOCABULARIO_BASE" in dondes:
        fuentes = {h["fuente"] for h in hits if h["donde"] == "VOCABULARIO_BASE"}
        if any((f or "").startswith("caquetío") for f in fuentes):
            return "activa-caquetio"
        return "activa-otra-lengua"
    if "FUERA_DEL_HABLA" in dondes:
        return "archivada"
    return "solo-referencia"


def medir_a9(idx):
    lex = cargar(LEXICO_YAML)
    filas = lex["tabla_a9_verificada"]
    salida, cuenta = [], {}
    for e in filas:
        hits = []
        for c in sorted(formas_de_fila(e)):
            hits += idx.get(c, [])
        uniq = []
        for h in hits:
            if h not in uniq:
                uniq.append(h)
        est = estado_de(uniq)
        solo_con_c = None
        if est == "ausente" and "ç" in str(e["forma"]).lower():
            alt = []
            for c in sorted(formas_de_fila(e, c_cedilla_como_c=True)):
                alt += idx.get(c, [])
            if alt:
                solo_con_c = sorted({f'{h["donde"]}:{h["clave"]} ({h["fuente"]})' for h in alt})
        cuenta[est] = cuenta.get(est, 0) + 1
        salida.append({"num": e["num"], "forma": e["forma"], "cursiva": e["cursiva"],
                       "estado": est,
                       "donde": sorted({f'{h["donde"]}:{h["clave"]} ({h["fuente"]})' for h in uniq}),
                       "solo_si_la_ç_se_lee_c": solo_con_c})
    cursivas = [e["num"] for e in filas if e["cursiva"] is True]
    con_fuente = [e["num"] for e in filas if e.get("fuente_en_oliver")]
    por_polity = {}
    for e in filas:
        p = e.get("polity")
        if p:
            por_polity[p] = por_polity.get(p, 0) + 1
    por_epoca = {}
    for e in filas:
        p = e.get("epoca")
        if p:
            por_epoca[p] = por_epoca.get(p, 0) + 1
    de_la_relacion = [e["num"] for e in filas
                      if "Relación de Barquisimeto" in str(e.get("fuente_en_oliver") or "")]
    return {
        "filas": len(filas),
        "numeracion_completa_1_a_50": [e["num"] for e in filas] == list(range(1, 51)),
        "fuente_relacion_de_barquisimeto_1579": {"n": len(de_la_relacion), "filas": de_la_relacion},
        "cursivas": {"n": len(cursivas), "filas": cursivas},
        "estado": dict(sorted(cuenta.items())),
        "con_fuente_nombrada_por_oliver": {"n": len(con_fuente), "filas": con_fuente},
        "polity_de_la_fuente": por_polity,
        "epoca_de_la_fuente": por_epoca,
        "ausentes": [s["forma"] for s in salida if s["estado"] == "ausente"],
        "ausentes_que_aparecen_si_la_ç_se_lee_c": [s["forma"] + " → " + "; ".join(s["solo_si_la_ç_se_lee_c"])
                                                   for s in salida if s["solo_si_la_ç_se_lee_c"]],
        "activas_en_otra_lengua": [s["forma"] + " → " + "; ".join(s["donde"])
                                   for s in salida if s["estado"] == "activa-otra-lengua"],
        "solo_referencia": [s["forma"] + " → " + "; ".join(s["donde"])
                            for s in salida if s["estado"] == "solo-referencia"],
        "detalle": salida,
    }


def medir_dictado():
    lex = cargar(LEXICO_YAML)["tabla_a9_verificada"]
    dic = cargar(DICTADO_YAML)
    ent = dic["entradas"]
    formas_dic = set()
    for e in ent:
        for x in re.split(r"[/,]", str(e.get("forma") or "")):
            formas_dic.add(norm(x))
    faltan = [e["forma"] for e in lex if not (formas_de_fila(e) & formas_dic)]
    sin_num = sum(1 for e in ent if e.get("num") is None)
    curs_dic = sum(1 for e in ent if e.get("cursiva") is True)
    return {
        "entradas_en_el_dictado": len(ent),
        "entradas_sin_numero_en_el_dictado": sin_num,
        "cursivas_marcadas_en_el_dictado": curs_dic,
        "cursivas_en_la_imagen": sum(1 for e in lex if e["cursiva"] is True),
        "filas_de_la_imagen_que_faltan_en_el_dictado": faltan,
    }


# ─────────────────────────────────────────────────────────── C1 / C3
def medir_c1_c3():
    import curiana_lexicon as L
    lex = cargar(LEXICO_YAML)["tabla_a9_verificada"]

    def ini(forma):
        n = norm(re.sub(r"^\(h\)", "", str(forma)))
        return n[:1]

    a9 = [e for e in lex if e["cursiva"] is not True and not str(e["forma"]).startswith("-")]
    c_a9 = {k: sum(1 for e in a9 if ini(e["fonemica"]) == k) for k in "bpdt"}
    atest = [k for k, e in L.VOCABULARIO_BASE.items()
             if (e.get("fuente") or "") == "caquetío-atestiguado"]
    c_lx = {k: sum(1 for x in atest if norm(x)[:1] == k) for k in "bpdt"}
    p_atest = sorted(x for x in atest if norm(x)[:1] == "p")
    t_atest = sorted(x for x in atest if norm(x)[:1] == "t")
    return {
        "a9_no_cursiva": {"n": len(a9), "iniciales": c_a9},
        "lexicon_caquetio_atestiguado": {"n": len(atest), "iniciales": c_lx,
                                         "claves_con_p_inicial": p_atest,
                                         "claves_con_t_inicial": t_atest},
    }


# ─────────────────────────────────────────────────────────── A-8
def medir_a8():
    out = []
    for linea in cargar(LEXICO_YAML)["tabla_a8_complemento"]["porcentajes_verbatim"]:
        for m in re.finditer(r"(\d+)/(\d+)\s*=\s*([\d.]+)%", linea):
            a, b, p = int(m.group(1)), int(m.group(2)), float(m.group(3))
            real = round(100 * a / b, 1)
            out.append({"par": linea.split(":")[0].strip(), "fraccion": f"{a}/{b}",
                        "impreso": p, "calculado": real, "cuadra": abs(real - p) < 0.15})
    return {"porcentajes": out, "no_cuadran": sum(1 for o in out if not o["cuadra"])}


# ─────────────────────────────────────────────────────────── Tabla 15
def medir_t15():
    esc = cargar(MUNDO_YAML)["arqueologia"]["tabla_15_escaneo"]["filas"]
    doc = cargar(T15_YAML)["dataciones"]
    por_lab = {d["lab"]: d for d in doc}
    difieren = []
    for lab, sitio, bp, a, c, b in esc:
        d = por_lab.get(lab)
        if not d:
            difieren.append({"lab": lab, "motivo": "no está en el .DOC"})
            continue
        if list(d["cal"]) != [a, c, b] or norm(d["bp"]) != norm(bp):
            difieren.append({"lab": lab, "escaneo": [bp, a, c, b], "doc": [d["bp"]] + list(d["cal"])})
    return {"filas_escaneo_1989": len(esc), "filas_doc": len(doc),
            "filas_que_difieren": len(difieren), "detalle": difieren}


# ─────────────────────────────────────────────────────────── fauna
def medir_fauna():
    fa = cargar(MUNDO_YAML)["fauna"]
    por_obra, por_epoca = {}, {}
    for f in fa:
        por_obra[f["obra"]] = por_obra.get(f["obra"], 0) + 1
        por_epoca[f["epoca"]] = por_epoca.get(f["epoca"], 0) + 1
    return {"entradas": len(fa), "por_obra": por_obra, "por_epoca": por_epoca,
            "con_especie_probable": sum(1 for f in fa if f.get("especie_probable")),
            "con_sonido": sum(1 for f in fa if f.get("sonido"))}


# ─────────────────────────────────────────────────────────── textos
def texto_cap3_doc():
    exe = shutil.which("pdftotext")
    if not exe or not os.path.exists(CAP3_DOC):
        return None
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "c3.txt")
        subprocess.run([exe, "-enc", "UTF-8", CAP3_DOC, out], check=True)
        with open(out, encoding="utf-8", errors="replace") as f:
            return f.read()


def paginas_doc(txt):
    """El DOC: página = índice (1-based) + 182."""
    return [(i + 183, p) for i, p in enumerate(txt.split("\f"))]


def paginas_ocr(ruta):
    with open(ruta, encoding="utf-8") as f:
        t = f.read()
    trozos = re.split(r"=== pdf \d+ · impresa (-?\d+) ===", t)
    return [(int(trozos[i]), trozos[i + 1]) for i in range(1, len(trozos) - 1, 2)]


# Sin `coast`/`coastal`: «Coastal Caquetío» es el NOMBRE de la polity y
# convertiría cada frase sobre Manaure en una «mención del mar».
MAR = r"\b(sea|seas|marine|maritime|ocean|beach|beaches|fish|fishing|fishermen|shell|shells|salt|canoe|canoes|navigat\w*|sailed|sailors|island|islands|pearl\w*)\b"
CREENCIA = r"\b(myth\w*|belief\w*|religio\w*|sacred|supernatural|ritual\w*|rite|rites|god|gods|spirit\w*|shaman\w*|deit\w*|cosmo\w*|worship\w*|offering\w*|sacrific\w*|demon|devil|boratio|piache)\b"


def ventanas(paginas, radio=250):
    mar_total, co = 0, []
    for pag, txt in paginas:
        t = re.sub(r"\s+", " ", txt)
        for m in re.finditer(MAR, t, re.I):
            mar_total += 1
            s, e = max(0, m.start() - radio), min(len(t), m.end() + radio)
            ven = t[s:e]
            cre = re.findall(CREENCIA, ven, re.I)
            if cre:
                co.append({"pagina": pag, "mar": m.group(0), "creencia": sorted({c.lower() for c in cre}),
                           "texto": ven.strip()[:300]})
    # una ventana por (página, palabra de creencia) — no contar la misma frase N veces
    uniq, vistos = [], set()
    for c in co:
        k = (c["pagina"], tuple(c["creencia"]))
        if k not in vistos:
            vistos.add(k)
            uniq.append(c)
    return {"menciones_del_mar": mar_total, "ventanas_con_creencia": len(uniq), "ventanas": uniq}


def medir_mar():
    res = {}
    doc = texto_cap3_doc()
    if doc is not None:
        res["cap3_doc_2006"] = ventanas(paginas_doc(doc))
    for k, ruta in OCR.items():
        if os.path.exists(ruta):
            res[k] = ventanas(paginas_ocr(ruta))
    return res


def medir_ortografia():
    dianas = ["caquet", "manaur", "paraguan", "coro", "jirajar", "curazao|curacao|curaçao", "aruba"]
    out = {}
    fuentes = {k: open(r, encoding="utf-8").read() for k, r in OCR.items() if os.path.exists(r)}
    doc = texto_cap3_doc()
    if doc:
        fuentes["cap3_doc_2006"] = doc
    for k, t in fuentes.items():
        n = unicodedata.normalize("NFD", t.lower())
        n = "".join(c for c in n if unicodedata.category(c) != "Mn")
        out[k] = {d: len(re.findall(d, n)) for d in dianas}
    return out


def medir_antillas():
    r = OCR["cap4_s47_s415"]
    t = open(r, encoding="utf-8").read().lower()
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    dianas = {"antillas_mayores": r"hispaniol|santo domingo|puerto rico|cuba\b|jamaica|greater antill|taino",
              "antillas_neerlandesas": r"netherland|curacao|curagao|aruba|bonaire|knip|tanki|savaneta|savaan",
              "portacelli_rancheria": r"portacelli|rancheria"}
    return {k: len(re.findall(v, t)) for k, v in dianas.items()}


def medir_mundo():
    m = cargar(MUNDO_YAML)
    vec = m["vecinos"]
    faltan = [v["grupo"] for v in vec if str(v.get("en_etnias_yaml", "")).startswith("NO")]
    a8 = cargar(LEXICO_YAML)["tabla_a8_complemento"]["filas_que_faltaban"]
    return {"vecinos_con_pagina": len(vec),
            "vecinos_sin_entrada_en_etnias_yaml": {"n": len(faltan), "grupos": faltan},
            "sitios_nombrados_en_el_cap4": len(m["arqueologia"]["sitios_nombrados_en_el_texto"]),
            "tabla8_filas_nuevas_p592": len(a8)}


def medir_voces_cap4(idx):
    out = {}
    for f in ("tucua", "zazare", "sasare", "guarataro", "warataro"):
        out[f] = sorted({f'{h["donde"]}:{h["clave"]}' for h in idx.get(f, [])})
    return out


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="mide e imprime sin escribir")
    args = ap.parse_args()

    idx = indice_lexicon()
    med = {
        "meta": {"generado_por": "6-fusion/scripts/oliver1989_restante.py",
                 "campana": "tercera campaña de minería, parcela M1",
                 "fecha": "2026-09-22"},
        "a9_vs_lexicon": medir_a9(idx),
        "a9_vs_dictado": medir_dictado(),
        "c1_c3": medir_c1_c3(),
        "a8_aritmetica": medir_a8(),
        "tabla15": medir_t15(),
        "fauna": medir_fauna(),
        "mar": medir_mar(),
        "ortografia": medir_ortografia(),
        "antillas": medir_antillas(),
        "voces_cap4": medir_voces_cap4(idx),
        "mundo": medir_mundo(),
    }
    a9 = med["a9_vs_lexicon"]
    print(f"A-9: {a9['filas']} filas · cursivas {a9['cursivas']['n']} · estado {a9['estado']}")
    print(f"     ausentes: {a9['ausentes']}")
    print(f"dictado: faltan {med['a9_vs_dictado']['filas_de_la_imagen_que_faltan_en_el_dictado']}")
    print(f"C1/C3 A-9: {med['c1_c3']['a9_no_cursiva']} · lexicón: {med['c1_c3']['lexicon_caquetio_atestiguado']['iniciales']}")
    print(f"A-8: {med['a8_aritmetica']['no_cuadran']} porcentajes no cuadran")
    print(f"Tabla 15: {med['tabla15']['filas_que_difieren']} filas difieren entre el escaneo y el .DOC")
    print(f"fauna: {med['fauna']}")
    for k, v in med["mar"].items():
        print(f"mar · {k}: {v['menciones_del_mar']} menciones, {v['ventanas_con_creencia']} ventanas con creencia")
    print(f"antillas (cap. 4): {med['antillas']}")
    print(f"mundo: {med['mundo']}")
    print(f"A-9 con fuente en la Relación de Barquisimeto 1579: {a9['fuente_relacion_de_barquisimeto_1579']}")
    if args.check:
        return 0
    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write("# GENERADO por 6-fusion/scripts/oliver1989_restante.py — no se edita a mano.\n")
        yaml.safe_dump(med, f, allow_unicode=True, sort_keys=False, width=100)
    print(f"→ {os.path.relpath(SALIDA, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
