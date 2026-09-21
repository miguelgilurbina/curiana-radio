# -*- coding: utf-8 -*-
"""¿De dónde salieron las voces taínas del proyecto, y quién las usa?

Campaña del Taíno, parcela T3 (2026-09-21). Esto NO propone nada al canon: mide
lo que hay y escribe el inventario que `6-fusion/taino_inventario_2026-09-21.yaml`
publica. Regla 1 (ninguna cifra a mano) y regla 6 (un cero se verifica).

Seis mediciones:

  A. CENSO. Las entradas de `curiana_lexicon.VOCABULARIO_BASE` con `fuente`
     `taíno` o `taíno-reconstruido`; las de `curiana_sim/taino_hipotetico.json`;
     y las de `6-fusion/tainismos_en_medina.yaml` (que NO son taínas en el
     canon: entraron como `caquetío-reconstruido` el 2026-09-12). Se mide el
     solapamiento, porque las tres listas comparten formas.

  B. PROCEDENCIA. `procedencia.obra` es la clave foránea (regla 8). Se cuenta
     cuántas la tienen y, para las que no, se busca cita EN PROSA dentro de
     `notas` contra una lista de obras conocidas. Una cita en prosa no es una
     clave foránea: se anota como candidata, no como procedencia.

  C. ORIGEN EN GIT. `git blame` sobre la línea de cada entrada: commit, fecha y
     asunto. Muchas entraron en bloque y el bloque es el dato.

  D. LA PUERTA DEL MOTOR. Qué ve de verdad el agente: `voces_de_fuera_posibles()`
     (el bloque [Voces de fuera], sólo tier 1), `ESFERA_DE_CONTACTO` vía
     `normalize_source_language`, `FORMA_DE_LA_ESFERA`, `SIN_FORMA_DE_LA_ESFERA`.
     Y quién importa `taino_hipotetico.json`, medido con un grep sobre el repo.

  E. USO REAL. `loanword_uses` (que nació con la migración 20260916000000 y sólo
     cubre los runs desde entonces: la tabla NO es el censo) y, porque un cero
     hay que verificarlo, un barrido de las 3.8xx `agent_responses.response_text`
     de toda la base con frontera de palabra.

  F. CLASE. (i) fuente primaria localizable, (ii) sólo secundaria, (iii) sin
     fuente ninguna, (iv) sospechosa de no ser taína. Las clases (i)/(ii)/(iii)
     se DEDUCEN de B; la (iv) es una lista DECLARADA a mano con su razón, porque
     un juicio de étimo no se mide con un regex — se marca y lo decide Miguel.

Uso:  python 6-fusion/scripts/medir_taino_inventario.py
      (necesita el Supabase local en Docker; sin él, las mediciones E salen
       marcadas `sin_base` y el resto corre igual)

Salida: YAML por stdout. Se redirige a 6-fusion/taino_inventario_2026-09-21.yaml.
"""
import collections
import csv
import io
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIM = os.path.join(RAIZ, "curiana_sim")
sys.path.insert(0, SIM)
CONTENEDOR = "supabase_db_curiana_sim"
LEXPY = os.path.join(SIM, "curiana_lexicon.py")

import curiana_lexicon as L                                     # noqa: E402
from curiana_database import normalize_source_language          # noqa: E402

FUENTES_TAINO = ("taíno", "taíno-reconstruido")


# ── utilidades ────────────────────────────────────────────────────────

def psql(sql: str):
    """SELECT y sólo SELECT. Devuelve [] si la base no está."""
    try:
        out = subprocess.run(
            ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d", "postgres",
             "-c", f"COPY ({sql}) TO STDOUT WITH CSV HEADER"],
            capture_output=True, text=True, encoding="utf-8", timeout=600)
    except Exception:
        return None
    if out.returncode:
        return None
    return list(csv.DictReader(io.StringIO(out.stdout)))


def _clave(k) -> str:
    """Una clave con `: `, `#` o comillas rompe el YAML. Los asuntos de commit
    los llevan casi siempre («corte(motor): la tanda…»), y eso hacía que el
    inventario entero no parseara — medido el 2026-09-21."""
    t = str(k)
    if re.search(r'[:#\[\]{}&*!|>\'"%@`,]|^\s|\s$|^[-?]', t) or t == "":
        return json.dumps(t, ensure_ascii=False)
    return t


def y(v, ind=0):
    """Volcado YAML mínimo y estable (sin dependencias)."""
    sp = "  " * ind
    if isinstance(v, dict):
        if not v:
            return " {}"
        s = ""
        for k, val in v.items():
            r = y(val, ind + 1)
            s += f"\n{sp}{_clave(k)}:{r}"
        return s
    if isinstance(v, list):
        if not v:
            return " []"
        s = ""
        for it in v:
            r = y(it, ind + 1)
            if isinstance(it, (dict, list)):
                r = r.lstrip("\n")
                r = r.replace("\n" + "  " * (ind + 1), "\n" + "  " * (ind + 1))
                s += f"\n{sp}- " + r[len("  " * (ind + 1)):] if r.startswith("  " * (ind + 1)) else f"\n{sp}-{r}"
            else:
                s += f"\n{sp}-{r}"
        return s
    if v is None:
        return " null"
    if isinstance(v, bool):
        return " true" if v else " false"
    if isinstance(v, (int, float)):
        return f" {v}"
    t = str(v)
    if t == "":
        return " ''"
    if "\n" in t or len(t) > 200:
        cuerpo = "\n".join(sp + "  " + ln for ln in t.split("\n"))
        return " >-\n" + cuerpo
    if re.search(r'^[\s>|&*!%@`\-?:\[\]{}#]|[:#]\s|[\'"]|^(true|false|null|yes|no|on|off|~)$|^[\d.+-]+$', t, re.I):
        return " " + json.dumps(t, ensure_ascii=False)
    return " " + t


# ── A. censo ──────────────────────────────────────────────────────────

def censo():
    lex = {k: v for k, v in L.VOCABULARIO_BASE.items()
           if v.get("fuente") in FUENTES_TAINO}
    fuera = {k: v for k, v in getattr(L, "FUERA_DEL_HABLA", {}).items()
             if v.get("fuente") in FUENTES_TAINO}
    hip = {}
    p = os.path.join(SIM, "taino_hipotetico.json")
    if os.path.exists(p):
        hip = json.load(io.open(p, encoding="utf-8"))
    med = []
    pm = os.path.join(RAIZ, "6-fusion", "tainismos_en_medina.yaml")
    if os.path.exists(pm):
        txt = io.open(pm, encoding="utf-8").read()
        med = re.findall(r"^- voz:\s*(\S+)", txt, re.M)
        claves = re.findall(r"^  clave_sugerida:\s*(\S+)", txt, re.M)
    else:
        claves = []
    return lex, fuera, hip, med, claves


# ── B. procedencia ────────────────────────────────────────────────────

# Obras que el repo ya conoce. La clave es lo que se busca en `notas`; el valor,
# el id de 4-fuentes/bibliografia.yaml si lo hay (o null: la obra no está).
OBRAS_EN_PROSA = {
    r"Brinton\s*1871": "brinton-1871",
    r"Alvarado\s*1921": "alvarado-1921",
    r"Las\s*Casas": "las-casas-1875",
    r"van\s*Buurt\s*2014": "van-buurt-2014",
    r"Oviedo": "oviedo-y-valdes-1851",
    r"Pané": "pane-c1498",
    r"Perea": "perea-alonso-1942",
    r"Oliver\s*1989": "oliver-1989",
    r"Schroeder\s*2018": "schroeder-2018",
    r"\bDRAE\b": None,
    r"Medina": "medina-colina-sxx",
}


def procedencia(lex):
    bib = set()
    pb = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")
    if os.path.exists(pb):
        bib = set(re.findall(r"^- id:\s*(\S+)\s*$",
                             io.open(pb, encoding="utf-8").read(), re.M))
    out = {}
    for k, v in lex.items():
        notas = v.get("notas", "") or ""
        citas = []
        for pat, oid in OBRAS_EN_PROSA.items():
            if re.search(pat, notas, re.I):
                citas.append({"obra_en_prosa": re.sub(r"\\s\*", " ", pat).replace("\\b", "").replace("\\", ""),
                              "id_bibliografia": oid,
                              "id_existe": (oid in bib) if oid else False})
        out[k] = {
            "tiene_procedencia_obra": "procedencia" in v,
            "notas_vacias": not notas.strip(),
            "citas_en_prosa": citas,
        }
    return out, sorted(bib)


# ── C. origen en git ──────────────────────────────────────────────────

def lineas_de_las_entradas(claves):
    """La línea del archivo donde se declara cada clave (la primera que la abre
    como llave de diccionario)."""
    txt = io.open(LEXPY, encoding="utf-8").read().split("\n")
    pos = {}
    for i, ln in enumerate(txt, 1):
        m = re.match(r'\s*"([^"]+)":\s*\{', ln)
        if m and m.group(1) in claves and m.group(1) not in pos:
            pos[m.group(1)] = i
    return pos


def blame(pos):
    if not pos:
        return {}
    rel = os.path.relpath(LEXPY, os.path.dirname(RAIZ)).replace("\\", "/")
    args = ["git", "-C", os.path.dirname(RAIZ), "blame", "--line-porcelain"]
    for c, n in pos.items():
        args += ["-L", f"{n},{n}"]
    args += ["HEAD", "--", rel]
    try:
        out = subprocess.run(args, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=600)
    except Exception:
        return {}
    if out.returncode:
        return {}
    por_linea = {}
    sha = autor = fecha = resumen = None
    for ln in out.stdout.split("\n"):
        # porcelain: <sha> <línea original> <línea FINAL> [<n>].  La que nos
        # sirve para volver a la clave es la FINAL: keyear por la original
        # dejaba 35 de 52 entradas sin commit (medido el 2026-09-21).
        m = re.match(r"^([0-9a-f]{40}) (\d+) (\d+)", ln)
        if m:
            sha, orig = m.group(1), int(m.group(3))
            continue
        if ln.startswith("summary "):
            resumen = ln[len("summary "):]
        elif ln.startswith("author-time "):
            import datetime
            fecha = datetime.datetime.fromtimestamp(
                int(ln.split()[1]), datetime.timezone.utc).date().isoformat()
        elif ln.startswith("author "):
            autor = ln[len("author "):]
        elif ln.startswith("\t") and sha:
            por_linea[orig] = {"commit": sha[:8], "fecha": fecha,
                               "autor": autor, "asunto": resumen}
            sha = None
    return {c: por_linea.get(n, {}) for c, n in pos.items()}


# ── D. la puerta del motor ────────────────────────────────────────────

def puerta(lex, hip):
    candidatas = L.voces_de_fuera_posibles()
    por_clave = {c[0]: c for c in candidatas}
    forma_esfera = getattr(L, "FORMA_DE_LA_ESFERA", {})
    sin_forma = set(getattr(L, "SIN_FORMA_DE_LA_ESFERA", ()))
    se_queda = set(getattr(L, "SE_QUEDA_CON_SU_GRAFIA", ()))
    det = {}
    for k, v in lex.items():
        fam = normalize_source_language(v.get("fuente", ""))
        det[k] = {
            "fuente": v.get("fuente"),
            "familia_normalizada": fam,
            "en_esfera_de_contacto": fam in L.ESFERA_DE_CONTACTO,
            "llega_a_voces_de_fuera": k in por_clave,
            "forma_que_se_ensena": por_clave[k][1] if k in por_clave else None,
            "tiene_gemela_indigena": forma_esfera.get(k),
            "en_sin_forma_de_la_esfera": k in sin_forma,
            "en_se_queda_con_su_grafia": k in se_queda,
        }
    # quién lee taino_hipotetico.json
    lectores = []
    try:
        g = subprocess.run(["git", "-C", os.path.dirname(RAIZ), "grep", "-n",
                            "taino_hipotetico"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
        lectores = [l for l in g.stdout.split("\n") if l.strip()]
    except Exception:
        pass
    solapamiento = sorted(set(hip) & set(lex))
    return {
        "n_candidatas_voces_de_fuera_total": len(candidatas),
        "n_candidatas_por_lengua": dict(collections.Counter(c[3] for c in candidatas)),
        "detalle": det,
        "taino_hipotetico_json": {
            "n_entradas": len(hip),
            "referencias_en_el_repo": lectores,
            "claves_tambien_en_el_lexicon": solapamiento,
            "n_claves_tambien_en_el_lexicon": len(solapamiento),
        },
    }


# ── E. uso real ───────────────────────────────────────────────────────

def uso(lex, hip):
    r = {"loanword_uses": None, "barrido_response_text": None}
    filas = psql("SELECT word, forma_dicha, source_language, tier, day, agent_name, run_id "
                 "FROM loanword_uses")
    if filas is None:
        r["loanword_uses"] = "sin_base"
    else:
        tain = [f for f in filas if f["source_language"] == "taíno"]
        por_word = collections.Counter(f["word"] for f in tain)
        por_tier = collections.Counter(f["tier"] for f in tain)
        por_dia = collections.Counter(f["day"] for f in tain)
        formas = collections.Counter((f["word"], f["forma_dicha"]) for f in tain)
        r["loanword_uses"] = {
            "n_filas_total": len(filas),
            "n_filas_taino": len(tain),
            "lenguas": dict(collections.Counter(f["source_language"] for f in filas)),
            "por_voz": dict(por_word.most_common()),
            "por_tier": {str(k): v for k, v in sorted(por_tier.items())},
            "por_dia": {str(k): v for k, v in sorted(por_dia.items())},
            "forma_guardada_vs_dicha": {f"{a} <- {b or '(vacío)'}": n
                                        for (a, b), n in formas.most_common()},
            "runs_distintos": len({f["run_id"] for f in tain}),
            "aviso": ("la tabla nació con la migración 20260916000000: NO es el censo "
                      "del habla, sólo cubre los runs desde entonces"),
        }
    # regla 6: un cero se verifica. Barrido del texto de TODA la base.
    resp = psql("SELECT id, run_id, response_text, tier FROM agent_responses")
    if resp is None:
        r["barrido_response_text"] = "sin_base"
        return r
    textos = [(f["run_id"], f["tier"], (f["response_text"] or "").lower()) for f in resp]
    todo = " \n ".join(t for _, _, t in textos)
    conteo = {}
    for k in sorted(set(lex) | set(hip)):
        pat = re.compile(r"(?<![\w\u00e0-\u00ff-])" + re.escape(k.lower()) + r"(?![\w\u00e0-\u00ff-])")
        n = len(pat.findall(todo))
        nresp = sum(1 for _, _, t in textos if pat.search(t))
        conteo[k] = {"ocurrencias": n, "respuestas": nresp}
    nunca = sorted(k for k in lex if conteo[k]["ocurrencias"] == 0)
    r["barrido_response_text"] = {
        "n_respuestas": len(resp),
        "n_runs": len({f["run_id"] for f in resp}),
        "caracteres": sum(len(t) for _, _, t in textos),
        "metodo": ("frontera de palabra sobre el texto en minúsculas; cuenta la FORMA "
                   "tal cual, sin desafijar: un `maisi-ni` no cuenta como `maisi`"),
        "n_del_lexicon_con_cero_usos": len(nunca),
        "del_lexicon_con_cero_usos": nunca,
        "conteo": conteo,
    }
    return r


# ── F. clase ──────────────────────────────────────────────────────────

# (iv) La sospecha de no ser taíno NO se mide: se declara, con su razón, y la
# decide Miguel. Aquí sólo se listan las que esta campaña pone en duda y por
# qué; el veredicto va en el YAML del inventario, no aquí.
SOSPECHOSAS = {
    "caiman":  "el étimo corriente es caribe (acayouman), no taíno; la nota lo da por «Taíno atestiguado … Brinton 1871» sin página",
    "piragua": "étimo caribe en la lexicografía corriente; la nota sólo dice «Tno. piragua → español piragua»",
    "papaya":  "atribuida tanto al taíno como al caribe según la obra; la nota no cita ninguna",
    "taita":   "voz de crianza panamericana (y romance); «cognado Lok. itti» no la hace taína",
    "maboya":  "más citada como caribe insular (mabuya) que como taína",
    "tabako":  "la forma taína atestiguada es cohiba (que el lexicón TIENE aparte); «tabaco» es la voz que llegó al castellano, de étimo discutido",
    "cacique": "voz taína sin discusión, pero la clave castellana convive con `cacike` y ninguna de las dos cita nada",
    "maíz":    "voz taína sin discusión, pero la clave castellana convive con `maisi` y ninguna de las dos cita nada",
}


def clase(lex, proc):
    out = {}
    for k in lex:
        p = proc[k]
        prim = any(c["obra_en_prosa"].strip() in ("Brinton 1871", "Las Casas", "Oviedo", "Pané")
                   for c in p["citas_en_prosa"])
        sec = bool(p["citas_en_prosa"]) and not prim
        if p["tiene_procedencia_obra"]:
            c = "i-fuente-primaria-localizable"
        elif prim:
            c = "i-fuente-primaria-localizable"
        elif sec:
            c = "ii-solo-fuente-secundaria"
        else:
            c = "iii-sin-fuente-ninguna"
        out[k] = {"clase": c,
                  "deuda": None if p["tiene_procedencia_obra"] else "sin-procedencia",
                  "sospechosa_de_no_ser_taina": SOSPECHOSAS.get(k)}
    return out


# ── G. ¿aguanta la cita que la entrada ya trae? ───────────────────────

# 9 entradas dicen «Taíno atestiguado: X … Brinton 1871». Brinton 1871 es *The
# Arawack Language of Guiana* —una comparativa del LOKONO— pero trae dentro un
# «Vocabulary of the Ancient Language of the Great Antilles», que SÍ es taíno.
# Así que la cita no es absurda: hay que comprobarla forma a forma.
# ⚠️ Esto NO es minar Brinton (parcela de T1/T2): es verificar una cita que ya
# está escrita en el canon. La lectura del pasaje y las entradas nuevas son de
# ellos.
BRINTON = "fuentes_caquetios/Brinton_1871_texto.txt"

# Variantes tolerantes al OCR del .txt («I^as Casas», «Prom this», «k/iiman»).
# Se declara la variante a propósito: un cero con un patrón estrecho mide la
# consulta, no la fuente (regla 6 / skill §2).
VARIANTES_BRINTON = {
    "cai": [r"(?<![A-Za-z])cai(?![A-Za-z])"],
    "caiman": [r"(?<![A-Za-z])caiman(?![A-Za-z])"],
    "casabe": [r"ca[sz][sz]?[ab][ab]?[ie]", r"ca[sz][sz]?ava"],
    "cohiba": [r"co[hlb][il1][bh]a", r"coh[o0]ba"],
    "higuana": [r"[hbl][il1][gq]u?[ai]na", r"(?<![A-Za-z])[yj]guana"],
    "mayani": [r"ma[yi]ani"],
    "taita": [r"(?<![A-Za-z])taita(?![A-Za-z])"],
    "tuna": [r"(?<![A-Za-z])tuna(?![A-Za-z])"],
    "yamosa": [r"[yi]amosa"],
    "cazabi": [r"ca[sz][sz]?[ab][ab]?[ie]"],
    "iwana": [r"(?<![A-Za-z])[il1]wana(?![A-Za-z])"],
    "tabako": [r"tabac[o0]"],
    "kunuku": [r"conuco", r"[ck]unu[ck]"],
    "bixa": [r"(?<![A-Za-z])b[il1][xj]a(?![A-Za-z])"],
    "bejique": [r"be[hjl][il1][qg]ue", r"be[hjl]ique"],
    "aji": [r"(?<![A-Za-z])a[gj][il1](?![A-Za-z])"],
    "areito": [r"are[il1]t[o0]"],
    "batey": [r"bate[yi]"],
    "caney": [r"cane[yi]"],
    "guanin": [r"guanin"],
    "huracan": [r"[hb]uracan"],
    "naboria": [r"nabor[il1]a"],
    "nitaino": [r"n[il1]ta[il1]n"],
    "cacique": [r"ca[cs]i[qc]ue"],
    "cacike": [r"ca[cs]i[qc]ue"],
    "maisi": [r"ma[il1][sz][ie]"],
    "maíz": [r"ma[il1][sz][ie]"],
    "dujo": [r"du[hj][o0]", r"du[hl][il1]?os"],
    "cemi": [r"(?<![A-Za-z])cem[il1](?![A-Za-z])"],
    "maboya": [r"mab[ou]ya"],
    "manati": [r"manat[il1]"],
    "hutia": [r"[hb]ut[il1]a"],
    "cobo": [r"(?<![A-Za-z])cob[o0](?![A-Za-z])"],
    "guabina": [r"guab[il1]na"],
    "manigua": [r"manigua"],
    "piragua": [r"piragua"],
    "papaya": [r"papa[yi]a"],
    "guayaba": [r"gua[yi]a[bh]a"],
    "batata": [r"batata"],
    "bohio": [r"bo[hb][il1][o0]", r"bu[hb][il1][o0]"],
    "bohío": [r"bo[hb][il1][o0]", r"bu[hb][il1][o0]"],
    "yuca": [r"(?<![A-Za-z])[yj]u[ck]a(?![A-Za-z])"],
    "cayo": [r"(?<![A-Za-z])ca[yi]c?o(?![A-Za-z])"],
}


def _contexto(t, m, izq=200, der=200):
    a = max(0, m.start() - izq)
    return re.sub(r"\s+", " ", t[a:min(len(t), m.end() + der)])


def verificar_brinton(lex):
    p = os.path.join(RAIZ, BRINTON)
    if not os.path.exists(p):
        return {"estado": "sin_texto"}
    t = io.open(p, encoding="utf-8", errors="replace").read()
    out = {}
    for k in sorted(lex):
        notas = lex[k].get("notas", "") or ""
        pats = VARIANTES_BRINTON.get(k, [r"(?<![A-Za-z])" + re.escape(k) + r"(?![A-Za-z])"])
        hits, ctx = 0, []
        for pat in pats:
            for m in re.finditer(pat, t, re.I):
                hits += 1
                if len(ctx) < 2:
                    ctx.append(_contexto(t, m))
        out[k] = {
            "la_entrada_cita_a_brinton": bool(re.search(r"Brinton", notas, re.I)),
            "patrones_probados": pats,
            "ocurrencias": hits,
            "contexto": ctx,
        }
    dice_brinton = [k for k, v in out.items() if v["la_entrada_cita_a_brinton"]]
    falla = [k for k in dice_brinton if out[k]["ocurrencias"] == 0]
    return {
        "estado": "medido",
        "que_es_brinton_1871": ("The Arawack Language of Guiana — comparativa del LOKONO, "
                                "pero con un «Vocabulary of the Ancient Language of the "
                                "Great Antilles» dentro, que SÍ es taíno"),
        "n_entradas_que_lo_citan": len(dice_brinton),
        "entradas_que_lo_citan": sorted(dice_brinton),
        "n_citas_que_no_se_verifican": len(falla),
        "citas_que_no_se_verifican": sorted(falla),
        "aviso": ("un cero aquí es del TEXTO PLANO OCR del repo, con los patrones "
                  "declarados arriba, no de la obra impresa; el PDF de Brinton "
                  "pesa 0 bytes. La relectura es de T1/T2"),
        "detalle": out,
    }


# El lema con el que Alvarado entra la voz NO es nuestra clave: él escribe el
# castellano de Venezuela (IGUANA, MAHIZ, BATÉI, BIJA) y nosotros la forma
# fonémica o la taína. La tabla es DECLARADA, no deducida: una clave nueva no
# se empareja sola. `null` = comprobado que Alvarado no la lematiza.
LEMAS_ALVARADO = {
    "aji": ["aji"], "batata": ["batata"], "batey": ["batei"],
    "bohio": ["bohio", "buhio"], "bohío": ["bohio", "buhio"],
    "bixa": ["bija", "bixa"], "cacique": ["cacique"], "cacike": ["cacique"],
    "caiman": ["caiman"], "caney": ["caney"], "casabe": ["casabe", "cazabe"],
    "cazabi": ["casabe", "cazabe"], "cohiba": ["cohiba", "coliiba", "cohoba"],
    "higuana": ["iguana", "yguana"], "iwana": ["iguana", "yguana"],
    "kunuku": ["conuco"], "maisi": ["mahiz", "maiz"], "maíz": ["mahiz", "maiz"],
    "manati": ["manati"], "tabako": ["tabaco"], "yuca": ["yuca"],
    "guayaba": ["guayaba"], "papaya": ["papaya"], "hutia": ["hicotea", "jutia"],
    "guabina": ["guabina"], "piragua": ["piragua"], "manigua": ["manigua"],
    "cayo": ["cayo"], "tuna": ["tuna"],
    # comprobadas ausentes del glosario: Alvarado recoge el español DE
    # VENEZUELA, y la arqueología antillana no está en él
    "areito": None, "cemi": None, "maboya": None, "guanin": None,
    "nitaino": None, "naboria": None, "dujo": None, "bejique": None,
    "huracan": None, "cobo": None, "mayani": None, "taita": None,
    "cai": None, "yamosa": None,
}

_ACENTOS = str.maketrans("áéíóúüàèìòùâêîôûÁÉÍÓÚÜñÑ", "aeiouuaeiouaeiouAEIOUUnN")


def _plano(s: str) -> str:
    """Sin acentos, sin guiones de fin de línea y sin espacios de sobra.

    Los tres hacen falta: el OCR parte «Cai- mán» y «ca- sabe», y buscar
    `cai` sobre el texto crudo casaba con la primera mitad de CAIMÁN — un
    falso positivo del mismo tipo que el `macana` achagua que tumbó un apoyo
    esta misma campaña."""
    s = re.sub(r"-\s+", "", s)
    return re.sub(r"\s+", " ", s.translate(_ACENTOS)).lower()


def verificar_alvarado(lex, ruta_txt=None):
    """Alvarado 1921 marca «Voz taina» en prosa. ¿A cuáles de las nuestras?

    Necesita el texto extraído:
        pdftotext -enc UTF-8 fuentes_caquetios/Alvarado_1921_*.pdf alvarado.txt
    y se le pasa la ruta. Sin él, devuelve `sin_texto` y no inventa nada.
    Desfase medido el 2026-09-21: página impresa = página del pdf − 31.
    """
    if not ruta_txt or not os.path.exists(ruta_txt):
        return {"estado": "sin_texto",
                "como_se_obtiene": ("pdftotext -enc UTF-8 "
                                    "fuentes_caquetios/Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf "
                                    "<salida.txt>; después pasar la ruta con --alvarado")}
    t = io.open(ruta_txt, encoding="utf-8", errors="replace").read()
    pags = t.split("\f")
    marcas = {}
    for i, pg in enumerate(pags, 1):
        for m in re.finditer(r"[Vv]oz ta[ií]na", pg):
            frag = re.sub(r"\s+", " ", pg[max(0, m.start() - 330):m.end() + 60])
            marcas.setdefault(i, []).append(frag)
    # ¿cuál de nuestras claves cae en el fragmento de una marca? Se busca el
    # LEMA de Alvarado, no nuestra clave, y sobre el texto aplanado.
    por_clave, sin_tabla = {}, []
    for k in sorted(lex):
        if k not in LEMAS_ALVARADO:
            sin_tabla.append(k)
            continue
        lemas = LEMAS_ALVARADO[k]
        if not lemas:
            continue
        enc = []
        for pdfp, frags in sorted(marcas.items()):
            for fr in frags:
                pl = _plano(fr)
                if any(re.search(r"(?<![a-z])" + re.escape(lm) + r"(?![a-z])", pl)
                       for lm in lemas):
                    enc.append({"pagina_pdf": pdfp, "pagina_impresa": pdfp - 31,
                                "lemas_probados": lemas, "fragmento": fr[-330:]})
        if enc:
            por_clave[k] = enc[:2]
    return {
        "estado": "medido",
        "metodo": ("se busca el LEMA castellano de Alvarado (tabla declarada "
                   "LEMAS_ALVARADO), no nuestra clave, sobre el texto aplanado "
                   "—sin acentos y sin el guion de fin de línea del OCR—: "
                   "buscar `cai` sobre el crudo casaba con «Cai- mán»"),
        "claves_sin_lema_declarado": sorted(sin_tabla),
        "etiquetas_de_origen_que_usa_la_obra": {
            e: len(re.findall(e, t, re.I)) for e in
            ["voz taina", "voz haitiana", "voz caribe", "voz galibi",
             "voz cumanagota", "voz cháima", "en taino"]},
        "desfase_pdf_a_impresa": -31,
        "n_marcas_voz_taina": sum(len(v) for v in marcas.values()),
        "n_claves_nuestras_con_marca": len(por_clave),
        "claves_nuestras_con_marca": sorted(por_clave),
        "detalle": por_clave,
    }


# ── H. la cuarentena de lo contemporáneo ──────────────────────────────

# La recuperación contemporánea del taíno (Hiwatahia/Higuayagua, Tainonaíki) es
# un esfuerzo cultural legítimo de comunidades vivas. NO es evidencia del s.
# XVI, igual que este proyecto no es evidencia del caquetío. Lo que se mide aquí
# es si alguna de nuestras entradas tiene el PERFIL de venir de ahí.
#
# El criterio es de PERFIL, no de veredicto: marca para mirar, no condena.
CRITERIOS_CUARENTENA = {
    "c1_sin_fuente_anterior_a_1900": (
        "la voz no aparece en ninguna fuente del repo anterior a 1900 y la entrada "
        "no cita ninguna"),
    "c2_concepto_que_ningun_cronista_glosa": (
        "cubre un campo que las crónicas no glosan: números, colores, pronombres "
        "completos, saludos, partes del cuerpo, verbos conjugados"),
    "c3_grafia_del_proyecto_moderno": (
        "la grafía usa convenciones del proyecto moderno (k sistemática por c/qu, "
        "w, dígrafos propios) en vez de la transcripción castellana del XVI"),
    "c4_se_explica_mejor_desde_el_andamio": (
        "la forma se explica mejor desde el lokono / wayuu / garífuna que desde una "
        "transcripción castellana — que es exactamente el método declarado de la "
        "recuperación contemporánea"),
}

# Campos que ningún cronista del XVI glosa en taíno (criterio c2).
CATEGORIAS_SIN_CRONISTA = frozenset({"cuerpo", "gramatica"})


def cuarentena(lex, hip, proc):
    det = {}
    for k, v in lex.items():
        cat = v.get("categoria") or v.get("cat") or ""
        notas = v.get("notas", "") or ""
        c1 = not proc[k]["citas_en_prosa"]
        c2 = cat in CATEGORIAS_SIN_CRONISTA
        c3 = bool(re.search(r"^[kw]|[kw]", k)) and not re.search(r"[cqzáéíóú]", k)
        c4 = bool(re.search(r"desde Lok\.|método comparativo", notas))
        marcas = [n for n, ok in (("c1", c1), ("c2", c2), ("c3", c3), ("c4", c4)) if ok]
        det[k] = {"categoria": cat, "criterios": marcas, "n_criterios": len(marcas)}
    # las de taino_hipotetico.json, con el mismo rasero
    det_hip = {}
    for k, v in hip.items():
        notas = v.get("notas", "") or ""
        cat = v.get("categoria", "")
        marcas = ["c1"]
        if cat in CATEGORIAS_SIN_CRONISTA or cat in ("cuerpo",):
            marcas.append("c2")
        if re.search(r"desde Lok\.|método comparativo", notas):
            marcas.append("c4")
        det_hip[k] = {"categoria": cat, "criterios": marcas, "n_criterios": len(marcas)}
    tres = sorted(k for k, v in det.items() if v["n_criterios"] >= 3)
    return {
        "criterios": CRITERIOS_CUARENTENA,
        "aviso": ("marcar NO es condenar: c4 se cumple también cuando la "
                  "reconstrucción es NUESTRA (reconstruir_taino()), que es el caso "
                  "de las 9 `taíno-reconstruido` y las 26 del JSON. La procedencia "
                  "la decide el commit, no el parecido — ver c_origen_en_git"),
        "lexicon": {
            "n_con_3_o_mas_criterios": len(tres),
            "con_3_o_mas_criterios": tres,
            "por_n_criterios": dict(collections.Counter(
                v["n_criterios"] for v in det.values())),
            "detalle": det,
        },
        "taino_hipotetico_json": {
            "n": len(det_hip),
            "por_n_criterios": dict(collections.Counter(
                v["n_criterios"] for v in det_hip.values())),
            "detalle": det_hip,
        },
    }


# ── main ──────────────────────────────────────────────────────────────

def main():
    lex, fuera, hip, med_voces, med_claves = censo()
    proc, bib = procedencia(lex)
    pos = lineas_de_las_entradas(set(lex))
    org = blame(pos)
    pta = puerta(lex, hip)
    us = uso(lex, hip)
    cls = clase(lex, proc)
    ruta_alv = None
    if "--alvarado" in sys.argv:
        ruta_alv = sys.argv[sys.argv.index("--alvarado") + 1]
    brin = verificar_brinton(lex)
    alv = verificar_alvarado(lex, ruta_alv)
    cuar = cuarentena(lex, hip, proc)

    por_fuente = collections.Counter(v.get("fuente") for v in lex.values())
    con_proc = sum(1 for v in proc.values() if v["tiene_procedencia_obra"])
    con_cita = sum(1 for v in proc.values() if v["citas_en_prosa"])
    sin_notas = sorted(k for k, v in proc.items() if v["notas_vacias"])
    por_commit = collections.Counter(
        f"{v.get('commit')} {v.get('fecha')} {(v.get('asunto') or '')[:70]}"
        for v in org.values())
    por_clase = collections.Counter(v["clase"] for v in cls.values())

    doc = {
        "meta": {
            "medido": "2026-09-21",
            "script": "6-fusion/scripts/medir_taino_inventario.py",
            "campana": "Campaña del Taíno — parcela T3 (inventario y mapa de fuentes)",
            "que_es": ("el censo MEDIDO de lo que el proyecto tiene como taíno: de dónde vino "
                       "cada entrada, si cita algo, si el motor la enseña y si alguien la ha "
                       "dicho alguna vez. No propone fusión: propone que Miguel decida"),
        },
        "a_censo": {
            "lexicon_vocabulario_base": {
                "n": len(lex),
                "por_fuente": dict(por_fuente),
                "claves": sorted(lex),
            },
            "lexicon_fuera_del_habla": {"n": len(fuera), "claves": sorted(fuera)},
            "taino_hipotetico_json": {"n": len(hip), "claves": sorted(hip)},
            "tainismos_en_medina_yaml": {
                "n": len(med_voces),
                "voces": med_voces,
                "claves_sugeridas": med_claves,
                "nota": ("fusionadas el 2026-09-12 como `caquetío-reconstruido`, no como "
                         "taíno: NO cuentan en las 52 y están fuera de este censo salvo "
                         "como precedente"),
            },
        },
        "b_procedencia": {
            "regla": "regla 8 — `procedencia.obra` es clave foránea a 4-fuentes/bibliografia.yaml",
            "n_con_procedencia_obra": con_proc,
            "n_sin_procedencia_obra": len(lex) - con_proc,
            "n_con_cita_en_prosa_en_notas": con_cita,
            "n_con_notas_vacias": len(sin_notas),
            "claves_con_notas_vacias": sin_notas,
            "ids_de_bibliografia_existentes": bib,
            "detalle": proc,
        },
        "c_origen_en_git": {
            "metodo": "git blame --line-porcelain sobre la línea que abre cada entrada",
            "por_commit": dict(por_commit.most_common()),
            "detalle": org,
        },
        "d_puerta_del_motor": pta,
        "e_uso_real": us,
        "f_clase": {"por_clase": dict(por_clase.most_common()), "detalle": cls},
        "g_verificacion_de_las_citas": {"brinton_1871": brin, "alvarado_1921": alv},
        "h_cuarentena_de_lo_contemporaneo": cuar,
    }
    print("# GENERADO por 6-fusion/scripts/medir_taino_inventario.py — no editar a mano")
    print(y(doc).lstrip("\n"))


if __name__ == "__main__":
    main()
