# -*- coding: utf-8 -*-
"""D11 fase 3 (cc.12) — el coste, MEDIDO, de sacar del wayuu los pronombres y el aspecto.

Miguel, 2026-09-23 (cc.12, `decisiones_cierre_2026-09-23.yaml`): «no podemos
seguir teniendo reconstrucciones desde el Wayu, tendría que ser desde el Locono.
O el Taíno […] o el Achagua». Este script NO propone formas —eso lo hace
`6-fusion/propuesta_d11_fase3_pronombres_aspectos_2026-09-23.yaml`, con cita—:
mide lo que cuesta cada opción de la propuesta. Sólo LEE: el lexicón, las
plantillas, la koiné, los tests y, con SELECT, la base local.

Qué mide, por forma candidata y por forma actual:

  1. USO EN LA BASE — `word_uses` (lo que el scorer reconoció) y el texto de
     `agent_responses` (lo que el agente escribió, lo reconozca o no el scorer).
     Para un afijo: formas y usos que lo llevan como segmento.
  2. COLISIONES — clave de `VOCABULARIO_BASE` o de `FUERA_DEL_HABLA` (exacta, con
     desambiguador de lengua, o con el mismo esqueleto bajo `fonemizar`), nombre
     del elenco (era 1 y era 2), `ES_STOPWORDS`, `CASTELLANO_CORRIENTE`, afijo de
     `TODAS_LAS_REGLAS`, y el AFIJO SUELTO: si un sufijo nuevo entra en
     `TODAS_LAS_REGLAS`, el token pelado que hoy es clave de otra lengua pasa a
     contarse como caquetío (`_AFIJOS_SUELTOS` en `score_linguistico`).
  3. FONOTÁCTICA — `curiana_fonotactica.Fonotactica` construida con el caquetío
     atestiguado, tal cual la usa el módulo.
  4. EL DESAFIJADOR — cuántas formas de la base cambian de núcleo
     (`nucleo_de_token`) y cuántas cambian de veredicto en
     `es_raiz_de_ninguna_parte` si el juego de afijos de cada opción sustituye
     al actual. Es lo que movió `-bacoa`→`-bakoa` y `-gua`→`-wa`: se mide antes.
  5. EL DETECTOR DE ASPECTO — con el mapa de cada opción, cuántas respuestas de
     la base siguen teniendo aspecto (el componente vale 2 de 10 puntos). Mide
     cómo el instrumento nuevo LEERÍA la base vieja, no lo que un run nuevo haría.
  6. LA ENSEÑANZA — en cuántas plantillas estáticas, reglas, koiné, escena,
     tests y elenco aparece cada forma actual: lo que hay que tocar.
  7. EL RESTO DEL NÚCLEO WAYUU — las 23 voces de la deuda D11: cuáles siguen en
     el habla y cuáles enseña alguna plantilla.

Uso (desde proyecto-linguistico-caquetío/):

    python 6-fusion/scripts/medir_d11_fase3.py
    python 6-fusion/scripts/medir_d11_fase3.py --sim RUTA/curiana_sim --rotulo <commit>
    python 6-fusion/scripts/medir_d11_fase3.py --salida 6-fusion/medicion_d11_fase3_2026-09-23.yaml
    python 6-fusion/scripts/medir_d11_fase3.py --sin-base     # sin Docker

`--sim` existe porque la tanda la aplicará el coordinador DESPUÉS de mergear
#202 (tanda de la base): la medición del 2026-09-23 se corrió contra el
`curiana_sim/` de `origin/tanda/base-2026-09-22`, que es el motor sobre el que
caería. Regla 1: todas las cifras de la propuesta salen de aquí.

⚠️ NO lee `curiana_sim/.env`, no importa `curiana_database` y no llama a la API.
A la base sólo le hace SELECT, con `docker exec supabase_db_curiana_sim psql`.
"""
from __future__ import annotations

import argparse
import datetime
import inspect
import io
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

R = Path(__file__).resolve().parents[2]

# ══════════════════════════════════════════════════════════════════════
# LAS OPCIONES QUE SE MIDEN — espejo de la propuesta (--check lo verifica)
# ══════════════════════════════════════════════════════════════════════
PRONOMBRES_ACTUALES = ["taya", "pia", "nüma", "waya", "naya", "kudanga", "kuté"]
AFIJOS_ACTUALES = ["-ka", "-ni", "-da", "ta-", "wa-", "-kana", "u-"]

# casilla → {letra: [formas]}
OPCIONES = {
    "pron-1sg": {"A": ["dai"], "B": ["daka"], "C": ["daya"], "D": ["daca"]},
    "pron-2sg": {"A": ["bui"], "B": ["bia"], "C": ["pia"]},
    "pron-3sg": {"A": ["lihi", "tuhu"], "B": ["tuhu"], "C": ["lihi"]},
    "pron-1pl": {"A": ["waya"], "B": ["wai"]},
    "pron-3pl": {"A": ["naya"], "B": ["nai"]},
    "asp-completivo": {"A": ["-kuba"], "B": ["-bi"], "C": ["-mi"]},
    "asp-continuativo": {"A": [], "B": ["-kata"], "C": ["-ka"], "D": ["-bo"]},
    "asp-prospectivo": {"A": ["-ba"], "B": ["-pa"], "C": ["-su"]},
    "pos-1sg": {"A": ["da-"], "B": ["ta-"]},
}

# Los juegos de aspecto que se comparan en el desafijador y en el detector.
# Una marca ausente = sin marca (el presente no marcado, opción A del
# continuativo): el detector no puede verlo, y el tope del componente sigue
# siendo 2 porque quedan dos marcas.
JUEGOS_DE_ASPECTO = {
    "actual (-ka/-ni/-da)": {"ka": "completivo", "ni": "continuativo", "da": "prospectivo"},
    "recomendado (-kuba/Ø/-ba)": {"kuba": "completivo", "ba": "prospectivo"},
    "tres marcas (-kuba/-kata/-ba)": {"kuba": "completivo", "kata": "continuativo", "ba": "prospectivo"},
    "presente -ka (-kuba/-ka/-ba)": {"kuba": "completivo", "ka": "continuativo", "ba": "prospectivo"},
    "lokono de Schumann y Pet (-bi/-bo/-pa)": {"bi": "completivo", "bo": "continuativo", "pa": "prospectivo"},
    "achagua (-mi/-kata/-su)": {"mi": "completivo", "kata": "continuativo", "su": "prospectivo"},
}
# Cambios de prefijo que se miden aparte (el posesivo de 1sg).
CAMBIOS_DE_PREFIJO = {"ta- → da-": ({"ta-"}, {"da-"})}

L = "a-záéíóúñüùàèïö"


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(flujo.buffer, encoding="utf-8",
                                                  errors="replace", line_buffering=True))


# ══════════════════════════════════════════════════════════════════════
# LA BASE — sólo SELECT
# ══════════════════════════════════════════════════════════════════════
def _psql(sql: str) -> list[list[str]]:
    r = subprocess.run(
        ["docker", "exec", "supabase_db_curiana_sim", "psql", "-U", "postgres", "-d",
         "postgres", "-At", "-F", "\x1f", "-R", "\x1e", "-c", sql],
        capture_output=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "replace")[:400])
    txt = r.stdout.decode("utf-8", "replace")
    return [fila.split("\x1f") for fila in txt.split("\x1e") if fila.strip("\n")]


def cargar_base():
    usos = {}
    for w, n, resp, runs in _psql(
            "select word, count(*), count(distinct response_id), count(distinct run_id) "
            "from word_uses group by word"):
        usos[w.strip("\n")] = (int(n), int(resp), int(runs))
    respuestas = []
    for rid, run, texto in _psql("select id, run_id, coalesce(response_text,'') from agent_responses"):
        respuestas.append((rid.strip("\n"), run, texto))
    total = _psql("select count(*) from word_uses")[0][0]
    return usos, respuestas, int(total)


# ══════════════════════════════════════════════════════════════════════
# CONTAR EN TEXTO — frontera de morfema
# ══════════════════════════════════════════════════════════════════════
def patron(forma: str, mencion: bool = False) -> re.Pattern:
    """USO por defecto (`naa-ka`, `ta-barsure`, `taya`). Con `mencion=True`
    cuenta también la mención metalingüística de un afijo (`-ka = completivo`,
    `ta- = mi`), que en una plantilla ES enseñanza."""
    f = re.escape(forma.strip("-"))
    if forma.endswith("-"):
        cola = "" if mencion else rf"(?=[{L}])"
        return re.compile(rf"(?<![{L}\-]){f}-{cola}", re.I)
    if forma.startswith("-"):
        cabeza = r"(?<!-)" if mencion else rf"(?<=[{L}])"
        return re.compile(rf"{cabeza}-{f}(?![{L}])", re.I)
    # `+` delante es un morfema en una fórmula de plantilla (`sima+bana`): el
    # locativo -bana no es la palabra `bana` 'hígado'.
    return re.compile(rf"(?<![{L}\-+]){f}(?![{L}\-])", re.I)


def contar(texto: str, forma: str, mencion: bool = False) -> int:
    return len(patron(forma, mencion).findall(texto or ""))


# Las claves con desambiguador de lengua (`ja-achagua`, `ba-achagua`): el
# segmento final es el nombre de la lengua, no un morfema.
LENGUAS_DESAMBIGUADORAS = {"achagua", "lokono", "kalinago", "taino", "taíno", "wayuu",
                           "wayunaiki", "paraujano", "caquetio", "caquetío"}


def base_de_clave(k: str) -> str:
    if "-" in k and not k.startswith("-") and k.rsplit("-", 1)[1] in LENGUAS_DESAMBIGUADORAS:
        return k.rsplit("-", 1)[0]
    return k


def segmentos(w: str) -> list[str]:
    return w.lower().split("-")


def usos_de_afijo(usos: dict, afijo: str) -> dict:
    """Formas de `word_uses` que llevan el afijo como segmento. Sufijo: en
    cualquier posición no inicial; prefijo: primer segmento de una forma con guion."""
    a = afijo.strip("-")
    formas, n = 0, 0
    for w, (c, _r, _u) in usos.items():
        s = segmentos(w)
        if len(s) < 2:
            continue
        ok = (a in s[1:]) if afijo.startswith("-") else (s[0] == a)
        if ok:
            formas += 1
            n += c
    return {"formas": formas, "usos": n}


# ══════════════════════════════════════════════════════════════════════
def medir(sim: Path, con_base: bool, rotulo: str) -> dict:
    sys.path.insert(0, str(sim))
    import curiana_lexicon as CL          # noqa: E402
    import curiana_koine as CK            # noqa: E402
    import curiana_fonotactica as CF      # noqa: E402
    import curiana_agents as AG1          # noqa: E402  (era 1: CURIANA_ELENCO sin fijar)
    import curiana_agents_era2 as AG2     # noqa: E402

    V, F = CL.VOCABULARIO_BASE, CL.FUERA_DEL_HABLA
    fon = lambda s: CF.fonemizar(s, gu_es_w=True)          # D5c: gu → w
    esqueletos = defaultdict(list)
    for tabla, dic in (("VOCABULARIO_BASE", V), ("FUERA_DEL_HABLA", F)):
        for k, e in dic.items():
            esqueletos[fon(base_de_clave(k))].append((k, e.get("fuente"), tabla))
    nombres = {n for n in list(AG1.ALL_AGENTS) + list(AG2.ALL_AGENTS)}
    nombres_min = {n.lower() for n in nombres}
    segmentos_de_nombre = defaultdict(set)
    for n in nombres:
        for s in n.lower().split("-"):
            segmentos_de_nombre[s].add(n)
    fono, paso = CF.medir()

    usos, respuestas, total = ({}, [], 0)
    if con_base:
        usos, respuestas, total = cargar_base()

    token_con_guion = re.compile(rf"[{L}]+(?:-[{L}]+)+", re.I)

    def uso_en_texto(forma: str) -> dict:
        """Apariciones en el texto de las respuestas. Para un afijo se cuentan
        las palabras con guion que lo llevan como segmento, sin los nombres del
        elenco (`Kawa-ni`, `Raka-bi` no son aspecto)."""
        if not (forma.startswith("-") or forma.endswith("-")):
            pat = patron(forma)
            conteo = [(r, len(pat.findall(r[2]))) for r in respuestas]
        else:
            a = forma.strip("-").lower()
            conteo = []
            for r in respuestas:
                n = 0
                for m in token_con_guion.finditer(r[2]):
                    tok = m.group(0)
                    if tok.lower() in nombres_min:
                        continue
                    s = tok.lower().split("-")
                    if (a in s[1:]) if forma.startswith("-") else (s[0] == a):
                        n += 1
                conteo.append((r, n))
        resp = [r for r, n in conteo if n]
        return {"respuestas": len(resp), "runs": len({r[1] for r in resp}),
                "apariciones": sum(n for _r, n in conteo)}

    def colisiones(forma: str) -> dict:
        b = forma.strip("-").lower()
        exacta = [(b, V[b].get("fuente"), (V[b].get("sig") or "")[:50])] if b in V else []
        archivada = [(b, F[b].get("fuente"))] if b in F else []
        desamb = [(k, V[k].get("fuente")) for k in V if k != b and base_de_clave(k) == b]
        mismo_esqueleto = [x for x in esqueletos.get(fon(b), []) if base_de_clave(x[0]) != b]
        nombre = sorted(n for n in nombres if n.lower() == b)
        en_nombre = sorted(segmentos_de_nombre.get(b, set()) - set(nombre))
        ok, motivos = fono.valida(b)
        d = {
            "clave_exacta": [list(x) for x in exacta],
            "archivada": [list(x) for x in archivada],
            "clave_con_desambiguador": [list(x) for x in desamb],
            "mismo_esqueleto_fonemico": [list(x) for x in mismo_esqueleto],
            "nombre_del_elenco": nombre,
            "segmento_de_nombre": en_nombre,
            "es_stopword_castellana": b in CL.ES_STOPWORDS,
            "castellano_corriente": b in getattr(CL, "CASTELLANO_CORRIENTE", set()),
            "fonotactica_atestiguada": "pasa" if ok else "; ".join(motivos),
        }
        if forma.startswith("-") or forma.endswith("-"):
            d["ya_es_afijo_del_motor"] = forma in CL.TODAS_LAS_REGLAS
            # El afijo suelto: si el sufijo entra en TODAS_LAS_REGLAS, el token
            # pelado que hoy es clave de OTRA lengua (y no stopword) pasa a
            # contarse caquetío en score_linguistico. Si ya es caquetío, no cambia.
            d["afijo_suelto_reclasifica"] = (
                [b, V[b].get("fuente")]
                if b in V and b not in CL.ES_STOPWORDS
                and not str(V[b].get("fuente", "")).startswith("caquetío")
                and forma not in CL.TODAS_LAS_REGLAS else None)
            ejemplo = ("naa" + b) if forma.startswith("-") else (b + "biro")
            ok2, mot2 = fono.valida(ejemplo)
            d["fonotactica_en_compuesto"] = {ejemplo: "pasa" if ok2 else "; ".join(mot2)}
        return d

    def uso(forma: str) -> dict:
        if not con_base:
            return {"base": "no medida (sin Docker)"}
        if forma.startswith("-") or forma.endswith("-"):
            return {"word_uses_con_el_afijo": usos_de_afijo(usos, forma),
                    "texto_de_respuestas": uso_en_texto(forma)}
        n, r, u = usos.get(forma, (0, 0, 0))
        return {"word_uses": {"usos": n, "respuestas": r, "runs": u},
                "texto_de_respuestas": uso_en_texto(forma)}

    out = {
        "meta": {
            "medido": str(datetime.date.today()),
            "script": "6-fusion/scripts/medir_d11_fase3.py",
            "motor_medido": rotulo,
            "vocabulario_base": len(V), "fuera_del_habla": len(F),
            "todas_las_reglas": len(CL.TODAS_LAS_REGLAS),
            "elenco": {"era1": len(AG1.ALL_AGENTS), "era2": len(AG2.ALL_AGENTS)},
            "base": ({"word_uses": total, "agent_responses": len(respuestas),
                      "formas_distintas": len(usos)} if con_base else "no medida"),
            "fonotactica": {"formas_base": len(fono.base), "gu_es_w": False,
                            "nota": "el filtro del módulo tal cual (medir()); los esqueletos de colisión sí usan gu→w (D5c)"},
        },
    }

    # ── 1-3. Formas actuales y candidatas ────────────────────────────────
    actuales = {}
    for f in PRONOMBRES_ACTUALES + AFIJOS_ACTUALES:
        actuales[f] = {"uso": uso(f), "colisiones": colisiones(f)}
    out["formas_actuales"] = actuales

    candidatas = {}
    for casilla, ops in OPCIONES.items():
        for letra, formas in ops.items():
            for f in formas:
                if f not in candidatas:
                    candidatas[f] = {"casillas": [], "uso": uso(f), "colisiones": colisiones(f)}
                candidatas[f]["casillas"].append(f"{casilla}.{letra}")
    out["formas_candidatas"] = candidatas

    # ── 4. El desafijador ────────────────────────────────────────────────
    pref0, suf0 = set(CL._PREFIJOS_CAQ), set(CL._SUFIJOS_CAQ)

    def recalcular(pref, suf):
        CL._PREFIJOS_CAQ, CL._SUFIJOS_CAQ = frozenset(pref), frozenset(suf)
        try:
            return {w: (tuple(CL.nucleo_de_token(w)), CL.es_raiz_de_ninguna_parte(w))
                    for w in usos if "-" in w}
        finally:
            CL._PREFIJOS_CAQ, CL._SUFIJOS_CAQ = frozenset(pref0), frozenset(suf0)

    desafijador = {}
    if con_base:
        base_ref = recalcular(pref0, suf0)

        def comparar(pref, suf):
            nuevo = recalcular(pref, suf)
            cam_n = [w for w in base_ref if base_ref[w][0] != nuevo[w][0]]
            cam_r = [w for w in base_ref if base_ref[w][1] != nuevo[w][1]]
            a_ninguna = [w for w in cam_r if nuevo[w][1]]
            return {
                "formas_con_guion": len(base_ref),
                "cambian_de_nucleo": {"formas": len(cam_n), "usos": sum(usos[w][0] for w in cam_n)},
                "cambian_de_veredicto_raiz": {
                    "formas": len(cam_r), "usos": sum(usos[w][0] for w in cam_r),
                    "pasan_a_raiz_de_ninguna_parte": len(a_ninguna),
                    "ejemplos": sorted(cam_r, key=lambda w: -usos[w][0])[:8]},
                "ejemplos_de_nucleo": [f"{w} → {'-'.join(nuevo[w][0])} (antes {'-'.join(base_ref[w][0])})"
                                       for w in sorted(cam_n, key=lambda w: -usos[w][0])[:6]],
            }

        viejos = {"-ka", "-ni", "-da"}
        for nombre, mapa in JUEGOS_DE_ASPECTO.items():
            if nombre.startswith("actual"):
                continue
            nuevos = {"-" + s for s in mapa}
            # (1) los viejos SALEN del desafijador (lo que pasaría si sólo se
            # cambian las claves de REGLAS_ASPECTO);
            desafijador[f"{nombre} · los viejos salen"] = comparar(pref0, (suf0 - viejos) | nuevos)
            # (2) los viejos se retiran del habla pero el desafijador los sigue
            # pelando (una tabla de retirados que SÍ desafija).
            desafijador[f"{nombre} · los viejos se siguen pelando"] = comparar(pref0, suf0 | nuevos)
        for nombre, (quitar, poner) in CAMBIOS_DE_PREFIJO.items():
            desafijador[f"{nombre} · ta- sale"] = comparar((pref0 - quitar) | poner, suf0)
            desafijador[f"{nombre} · ta- se sigue pelando"] = comparar(pref0 | poner, suf0)
    out["desafijador"] = desafijador or "no medido (sin base)"

    # ── 5. El detector de aspecto sobre la base existente ────────────────
    detector = {}
    if con_base:
        verbales = CL.raices_verbales_caquetias()

        def aspectos(tokens, mapa):
            enc = []
            for tok in tokens:
                if "-" in tok:
                    raiz, _, suf = tok.rpartition("-")
                    if suf in mapa and raiz.rsplit("-", 1)[-1] in verbales:
                        enc.append(mapa[suf])
                    continue
                for raiz in verbales:
                    for suf, nom in mapa.items():
                        if tok == raiz + suf:
                            enc.append(nom)
            return list(dict.fromkeys(enc))

        tok_por_resp = []
        for _rid, _run, texto in respuestas:
            limpio = CL._normalizar(texto)
            tok_por_resp.append(CL._filtrar_nombres(limpio, CL._tokenizar(limpio)))
        # control: el mapa actual reimplementado = la función del motor, respuesta a respuesta
        desvios = sum(1 for t in tok_por_resp
                      if sorted(aspectos(t, JUEGOS_DE_ASPECTO["actual (-ka/-ni/-da)"]))
                      != sorted(CL._aspectos_morfologicos(t)))
        detector["control_contra_el_motor"] = {"respuestas": len(tok_por_resp), "desvios": desvios}
        juegos = dict(JUEGOS_DE_ASPECTO)
        juegos["unión (actual + recomendado), para una transición"] = {
            **JUEGOS_DE_ASPECTO["actual (-ka/-ni/-da)"], **JUEGOS_DE_ASPECTO["recomendado (-kuba/Ø/-ba)"]}
        for nombre, mapa in juegos.items():
            puntos = [min(len(aspectos(t, mapa)), 2) for t in tok_por_resp]
            detector[nombre] = {
                "respuestas_con_aspecto": sum(1 for p in puntos if p),
                "respuestas_en_el_tope_2": sum(1 for p in puntos if p == 2),
                "media_del_componente": round(sum(puntos) / max(len(puntos), 1), 4),
                "tope_alcanzable": min(len(mapa), 2),
            }
    out["detector_de_aspecto"] = detector or "no medido (sin base)"

    # ── 6. La enseñanza: dónde está cada forma actual ────────────────────
    plantillas = {
        "IDENTIDAD_LINGUISTICA (todos)": CL.IDENTIDAD_LINGUISTICA,
        "prompt_reglas_completo (tier I)": CL.prompt_reglas_completo(),
        "prompt_reglas_breve": CL.prompt_reglas_breve(),
        "prompt_refuerzo (4 tramos)": " ".join(CL.prompt_refuerzo(s, []) for s in (1.0, 3.0, 5.0, 6.5)),
        "prompt_rescate (3 motivos)": " ".join(CL.prompt_rescate_linguistico("", 0.0, e, o)
                                              for e, o in ((0, [""]), (3, [""]), (3, []))),
    }
    reglas_txt = " ".join(str(v) for r in CL.TODAS_LAS_REGLAS.values() for v in r.values())
    koine = {
        "_NUCLEO_FALLBACK": " ".join(CK._NUCLEO_FALLBACK),
        "FORMAS_SEED": " ".join(" ".join(v) for v in CK.FORMAS_SEED.values()),
        "_ASPECTO_SUFIJO": " ".join(f"x{v}" for v in CK._ASPECTO_SUFIJO.values()),
    }
    escena = (sim / "curiana_escena.py").read_text(encoding="utf-8")
    marca = re.search(r"_MARCA_CAQUETIA = re\.compile\(\s*r\"(.*?)\"", escena, re.S)
    marca_txt = marca.group(1) if marca else ""
    src_score = inspect.getsource(CL.score_linguistico)
    src_asp = inspect.getsource(CL._aspectos_morfologicos)
    tupla_pref = re.search(r"for pref in \(([^)]*)\)", src_score)
    mapa_asp = re.search(r"mapa = \{([^}]*)\}", src_asp)
    tests = sorted((sim / "tests").glob("test_*.py"))
    agentes = [sim / "curiana_agents.py", sim / "curiana_agents_era2.py"]
    ensenanza = {}
    for f in PRONOMBRES_ACTUALES + ["-ka", "-ni", "-da", "ta-", "-kana"]:
        b = f.strip("-")
        p = {n: contar(t, f, mencion=True) for n, t in plantillas.items()}
        ensenanza[f] = {
            "plantillas_que_la_ensenan": sum(1 for v in p.values() if v),
            "apariciones_en_plantillas": sum(p.values()),
            "por_plantilla": {n: v for n, v in p.items() if v},
            "en_reglas_del_motor": contar(reglas_txt, f, mencion=True),
            "koine": {n: contar(t, f) for n, t in koine.items() if contar(t, f)},
            "escena_marca_caquetia": bool(re.search(rf"(?<![{L}]){re.escape(b)}(?![{L}])", marca_txt)) if not (f.startswith("-") or f.endswith("-")) else False,
            "cableado_en_el_scorer": (
                (f'"{b}"' in (tupla_pref.group(1) if tupla_pref else "")) if f.endswith("-") else
                (f'"{b}"' in (mapa_asp.group(1) if mapa_asp else "")) if f.startswith("-") else False),
            "apariciones_en_tests": sum(contar(t.read_text(encoding="utf-8"), f, mencion=True) for t in tests),
            "tests_que_la_nombran": sum(1 for t in tests if contar(t.read_text(encoding="utf-8"), f, mencion=True)),
        }
        if not (f.startswith("-") or f.endswith("-")):
            # en las fichas un sufijo con guion es casi siempre un NOMBRE
            # (`Kawa-ni`), así que sólo se cuentan las palabras
            ensenanza[f]["en_fichas_del_elenco"] = sum(
                contar(a.read_text(encoding="utf-8"), f) for a in agentes if a.exists())
    out["ensenanza"] = ensenanza

    # ── 7. El resto del núcleo reconstruido desde el wayuu ───────────────
    textos_plantilla = " ".join(plantillas.values())
    d11 = sorted(k for k, e in {**V, **F}.items() if "DEUDA D11" in str(e.get("notas", "")))
    resto = {}
    for k in d11:
        e = V.get(k) or F.get(k)
        resto[k] = {
            "en_el_habla": k in V,
            "glosa": (e.get("sig") or "")[:48],
            "cat": e.get("cat"),
            "apariciones_en_plantillas": contar(textos_plantilla, k),
            **({"word_uses": usos.get(k, (0, 0, 0))[0]} if con_base else {}),
        }
    out["deuda_d11_las_23"] = {
        "aviso": ("`apariciones_en_plantillas` no cuenta el locativo -bana escrito `sima+bana`: "
                  "`bana` 'hígado' (la de la deuda) y -bana 'cerro' (D9) son dos entradas"),
        "total": len(d11),
        "siguen_en_el_habla": sum(1 for v in resto.values() if v["en_el_habla"]),
        "ensenadas_por_alguna_plantilla": sum(1 for v in resto.values()
                                              if v["en_el_habla"] and v["apariciones_en_plantillas"]),
        "voces": resto,
    }
    return out


def _yaml(obj) -> str:
    import yaml
    return yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=110)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sim", default=str(R / "curiana_sim"), help="el curiana_sim/ que se mide")
    ap.add_argument("--rotulo", default="curiana_sim de este árbol", help="qué motor es (commit, rama)")
    ap.add_argument("--sin-base", action="store_true", help="no consulta Supabase")
    ap.add_argument("--salida", help="escribe el YAML medido en esta ruta")
    ap.add_argument("--check", action="store_true",
                    help="verifica que toda forma de la propuesta está medida aquí")
    args = ap.parse_args(argv)

    if args.check:
        import yaml
        prop = yaml.safe_load((R / "6-fusion" / "propuesta_d11_fase3_pronombres_aspectos_2026-09-23.yaml")
                              .read_text(encoding="utf-8"))
        faltan = []
        for c in prop.get("casillas", []):
            for op in c.get("opciones", []):
                formas = op.get("formas") or []
                medidas = OPCIONES.get(c["id"], {}).get(op["letra"])
                if medidas is None or sorted(formas) != sorted(medidas):
                    faltan.append(f"{c['id']}.{op['letra']}: propuesta {formas} / medidas {medidas}")
        print("\n".join(faltan) if faltan else "check: toda opción de la propuesta está medida aquí")
        return 1 if faltan else 0

    out = medir(Path(args.sim), not args.sin_base, args.rotulo)
    txt = _yaml(out)
    if args.salida:
        cab = ("# MEDICIÓN — D11 fase 3 (cc.12): el coste de sacar del wayuu pronombres y aspecto.\n"
               "# GENERADO por 6-fusion/scripts/medir_d11_fase3.py — no se edita a mano (regla 1).\n"
               "# La propuesta que lo usa: 6-fusion/propuesta_d11_fase3_pronombres_aspectos_2026-09-23.yaml\n")
        Path(args.salida).write_text(cab + txt, encoding="utf-8")
        print(f"escrito {args.salida}")
    else:
        print(txt)
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
