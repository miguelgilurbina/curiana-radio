# -*- coding: utf-8 -*-
"""¿Qué hay de verdad en `loanword_uses`? El hispanismo que no es préstamo.

El día 1 de la serie B de la era 2 (run 3973d317, 2026-09-17) la tabla
registró 7 usos y los 7 eran castellano: «Las manos ocupadas limpiando yuca»,
«Maíz, yuca ta-kana», «Casabe kaa-ni wara amana-ni». Esto lo mide sobre TODA
la base, no sobre el día.

Cinco mediciones:

  A. `loanword_uses` tal como está: qué guardó, con qué lengua y qué tier.
     Son pocas filas porque la tabla nació el 2026-09-16 (migración
     20260916000000); los runs viejos no la tienen.
  B. Re-puntuar las 2.515 respuestas de `agent_responses` con el scorer de hoy:
     qué voces de la esfera SALDRÍAN, con qué frecuencia, lengua y tier.
     Es la medida buena — la tabla sólo ve los tres últimos runs.
  C. Dónde cae cada uso: dentro de la frase caquetía, en la glosa castellana,
     o dentro de un paréntesis (invisible al scorer, que los borra).
  D. ¿Tiene el caquetío voz propia para casabe / maíz / yuca? Se busca por la
     GLOSA (`sig`, o `es` en las entradas viejas).
  E. ¿De dónde le llega al agente la palabra castellana? Del bloque
     [Voces de fuera] y, sobre todo, de la GLOSA del propio diccionario.

Uso:  python 6-fusion/scripts/medir_hispanismos_loanword_uses.py
      CURIANA_ELENCO=era2 python 6-fusion/scripts/medir_…   (la era 2)
      (necesita el Supabase local en Docker; ver CLAUDE.md)

⚠ TARDA. `score_linguistico()` cuesta ~113 ms por llamada —`_aspectos_morfoló-
gicos` prueba las 1.426 raíces verbales contra cada token sin guion— y aquí se
llama tres veces por respuesta. La era 2 (444 respuestas) son ~3 minutos; la
era 1 (2.071) pasa del cuarto de hora. No está colgado.
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

import curiana_lexicon as L                                    # noqa: E402
from curiana_database import normalize_source_language          # noqa: E402

LEX = L.LexicoComunitario()
ACTIVOS = set(LEX.palabras_activas())


def psql(sql: str) -> list:
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d", "postgres",
         "-c", f"COPY ({sql}) TO STDOUT WITH CSV HEADER"],
        capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        raise RuntimeError(out.stderr.strip())
    return list(csv.DictReader(io.StringIO(out.stdout)))


# ── C. ¿dentro de la frase caquetía o en la glosa? ─────────────────────

def _es_arahuaco(tok: str) -> bool:
    if tok in L.ES_STOPWORDS or tok in L.CASTELLANO_CORRIENTE:
        return False
    if tok in ACTIVOS:
        return True
    for pref in ("ta", "wa", "ma", "ka"):
        if tok.startswith(pref + "-") and tok.split("-", 1)[1] in ACTIVOS:
            return True
    return tok.split("-")[0] in L._RAICES_VERB


def _segmentos(texto: str) -> list:
    out = []
    for m in re.finditer(r"[^\n]+", texto):
        for s in re.finditer(r"[^.!?—–]+[.!?]*", m.group()):
            if s.group().strip():
                out.append((m.start() + s.start(), s.group()))
    return out


def donde_cae(texto: str, palabra: str) -> list:
    """Clase de cada ocurrencia. El scorer BORRA los paréntesis antes de
    tokenizar (`_normalizar`), así que lo que va ahí ni siquiera se ve; lo
    demás se decide por el peso del vecindario."""
    parens = [(m.start(), m.end()) for m in re.finditer(r"\([^)]*\)", texto)]
    pat = re.compile(r"(?<![\wáéíóúñü-])" + re.escape(palabra) + r"(?![\wáéíóúñü-])",
                     re.IGNORECASE)
    clases = []
    for m in pat.finditer(texto):
        i = m.start()
        if any(a <= i < b for a, b in parens):
            clases.append("parentesis_no_contado")
            continue
        seg = next((s for off, s in _segmentos(texto) if off <= i < off + len(s)), "")
        toks = L._tokenizar(seg)
        n_ara = sum(1 for t in toks if t != palabra.lower() and _es_arahuaco(t))
        n_es = sum(1 for t in toks if t in L.ES_STOPWORDS)
        clases.append("frase_caquetia" if n_ara > n_es else
                      "glosa_castellana" if n_es > n_ara else "mixto")
    return clases


# ══════════════════════════════════════════════════════════════════════

def medir_a() -> dict:
    filas = psql("SELECT word, source_language, tier, agent_name, day, "
                 "run_id::text AS run FROM loanword_uses ORDER BY created_at")
    por_voz = collections.Counter(f["word"] for f in filas)
    return {"filas": len(filas), "por_voz": dict(por_voz.most_common()),
            "runs": sorted({f["run"][:8] for f in filas}),
            "detalle": [{k: (v[:8] if k == "run" else v) for k, v in f.items()}
                        for f in filas]}


def medir_b_y_c(elenco: str) -> dict:
    """`score_linguistico` filtra los nombres del ELENCO ACTIVO, así que cada
    era se mide con el suyo: este proceso ve el que diga CURIANA_ELENCO."""
    filas = psql(
        "SELECT r.id, r.run_id::text AS run, "
        "coalesce(s.config->>'elenco','era1') AS elenco, r.agent_name, "
        "coalesce(r.tier,0) AS tier, r.response_text "
        "FROM agent_responses r LEFT JOIN simulation_runs s ON s.id = r.run_id")
    filas = [f for f in filas if f["elenco"] == elenco]
    voces: dict = {}
    n_con = 0
    for f in filas:
        m = L.score_linguistico(f["response_text"], LEX)
        pres = m["prestamos_de_esfera"] + m.get("hispanismos_de_esfera", [])
        if not pres:
            continue
        n_con += 1
        for tok in pres:
            d = voces.setdefault(tok, {
                "familia": L._familia_de_token(tok), "respuestas": 0,
                "tiers": collections.Counter(), "runs": set(),
                "usos": collections.Counter()})
            d["respuestas"] += 1
            d["tiers"][f["tier"]] += 1
            d["runs"].add(f["run"][:8])
            d["usos"].update(donde_cae(f["response_text"], tok))
    return {"elenco": elenco, "respuestas": len(filas), "con_prestamo": n_con,
            "voces": {k: {"familia": v["familia"], "respuestas": v["respuestas"],
                          "tiers": dict(sorted(v["tiers"].items())),
                          "runs": len(v["runs"]), "usos": dict(v["usos"])}
                      for k, v in sorted(voces.items(),
                                         key=lambda kv: -kv[1]["respuestas"])}}


def medir_score_no_se_mueve(elenco: str) -> dict:
    """La lista vacía reproduce el comportamiento anterior byte a byte: si no
    cambia ningún campo del score, la lista no toca el instrumento."""
    filas = psql(
        "SELECT coalesce(s.config->>'elenco','era1') AS elenco, r.response_text "
        "FROM agent_responses r LEFT JOIN simulation_runs s ON s.id = r.run_id")
    filas = [f for f in filas if f["elenco"] == elenco]
    campos = ("score", "densidad", "pct_caquetio_especifico", "otro_arahuaco",
              "espanol_funcional", "palabras_caquetias", "palabras_arahuacas",
              "palabras_otro_arahuaco", "aspectos_usados")
    real = L.HISPANISMOS_DE_ESFERA
    lados = {}
    try:
        for etiqueta, conjunto in (("antes", frozenset()), ("despues", real)):
            L.HISPANISMOS_DE_ESFERA = conjunto
            lado = []
            for f in filas:
                m = L.score_linguistico(f["response_text"], LEX)
                lado.append({k: m[k] for k in campos}
                            | {"pres": m["prestamos_de_esfera"]})
            lados[etiqueta] = lado
    finally:
        L.HISPANISMOS_DE_ESFERA = real
    difs = {k: sum(1 for a, d in zip(lados["antes"], lados["despues"])
                   if a[k] != d[k]) for k in campos}
    return {"elenco": elenco, "respuestas": len(filas),
            "campos_que_cambian": difs,
            "respuestas_con_prestamo_antes":
                sum(1 for a in lados["antes"] if a["pres"]),
            "respuestas_con_prestamo_despues":
                sum(1 for d in lados["despues"] if d["pres"])}


def medir_d() -> dict:
    """¿Tiene el caquetío voz propia? Se busca por la glosa, que vive en `sig`
    o —en las entradas viejas— en `es`."""
    def glosa(v):
        return v.get("sig") or v.get("es") or ""
    salida = {}
    for etiqueta, patron in (("casabe", r"casabe|cazabe|pan de yuca"),
                             ("maíz", r"\bma[ií]z\b"),
                             ("yuca", r"yuca|mandioca")):
        filas = []
        for k, v in sorted(L.VOCABULARIO_BASE.items()):
            if re.search(patron, glosa(v), re.I):
                fam = normalize_source_language(v.get("fuente", ""))
                filas.append({"forma": k, "familia": fam,
                              "fuente": v.get("fuente", ""), "glosa": glosa(v)[:70]})
        salida[etiqueta] = {"caquetio": [f for f in filas if f["familia"] == "caquetío"],
                            "otras": [f for f in filas if f["familia"] != "caquetío"]}
    return salida


def medir_e() -> dict:
    # El muestreador del prompt sortea (`prompt_voces_de_fuera`, y el propio
    # `vocabulario_para_agente`): sin semilla la cifra baila. Se fija para que
    # el número del YAML se pueda volver a sacar.
    import random
    random.seed(20260917)
    ctxs = ["conuco siembra comida", "canoa islas trueque", "sal pesca mar",
            "casa familia noche", "fiesta ritual palabra"]
    voces = ["casabe", "maíz", "yuca", "batata", "papaya", "watapana", "ture"]
    N = 40
    vistas = {v: {} for v in voces}
    for tier in (1, 2, 3):
        prompts = [L.vocabulario_para_agente(tier, LEX, ctxs[i % len(ctxs)])
                   for i in range(N)]
        for v in voces:
            pat = re.compile(r"(?<![\wáéíóúñü-])" + re.escape(v) + r"(?![\wáéíóúñü-])",
                             re.I)
            vistas[v][tier] = sum(1 for p in prompts if pat.search(p))
    catalogo = L.voces_de_fuera_posibles()
    return {"prompts_por_tier": N, "apariciones": vistas,
            "voces_de_fuera_posibles": len(catalogo),
            "hispanismos_en_el_catalogo":
                sorted(p for p, _f, _g, _fam in catalogo
                       if p in L.HISPANISMOS_DE_ESFERA)}


if __name__ == "__main__":
    elenco = os.environ.get("CURIANA_ELENCO", "era1")
    salida = {
        "elenco_activo": elenco,
        "A_loanword_uses": medir_a(),
        "B_C_repuntuado": medir_b_y_c("era2" if elenco == "era2" else "era1"),
        "score_no_se_mueve": medir_score_no_se_mueve(
            "era2" if elenco == "era2" else "era1"),
        "D_voz_propia_caquetia": medir_d(),
        "E_de_donde_le_llega": medir_e(),
    }
    print(json.dumps(salida, ensure_ascii=False, indent=1))
