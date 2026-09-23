# -*- coding: utf-8 -*-
"""D11 · las voces wayuu que quedan (tf.5) — el coste, MEDIDO, de cada opción.

Miguel, 2026-09-23 (tf.5, `6-fusion/decisiones_tanda_final_2026-09-23.yaml`):
«Las 16 voces guayu que quedan. Kashi llama a Zulu Wano [kashi, yama, sulu,
wana…]. Una gente más le busca las sustitutas en el mismo [método].» Y la de
fondo, cc.12: «no podemos seguir teniendo reconstrucciones desde el Wayu».

Este script NO propone formas —eso lo hace
`6-fusion/propuesta_d11_voces_wayuu_2026-09-23.yaml`, con cita—: mide lo que
cuesta cada opción. Es el mismo método que `medir_d11_fase3.py` (#226) aplicado
a las voces léxicas. Sólo LEE: el lexicón, las plantillas, la koiné, la escena,
los tests, las fichas del elenco y, con SELECT, la base local.

Qué mide:

  1. LA LISTA — las voces con «DEUDA D11» en sus notas, cuáles siguen en el
     habla y cuáles enseña alguna plantilla. De ahí salen las de esta campaña:
     las del habla MENOS los cinco pronombres que tf.1 ya decidió.
  2. CADA VOZ VIEJA — uso en `word_uses` (suelta y como segmento del núcleo de
     una forma con guion), en el texto de `agent_responses`, en qué plantillas
     se enseña, en la koiné, la escena, los tests y las fichas; si pasa la
     fonotáctica del caquetío atestiguado; con qué clave comparte esqueleto
     bajo `fonemizar` (el caso `kashi`~`kasi`); y qué formas de la base pasan
     a «raíz de ninguna parte» en la PUERTA si se archiva (una raíz archivada
     no avala: `archivadas_avalan=False`, db.1).
  3. CADA FORMA CANDIDATA — colisiones con `VOCABULARIO_BASE`/`FUERA_DEL_HABLA`
     (exacta, con desambiguador, mismo esqueleto), con las formas que la tanda
     final mete (tf.1-tf.3), con los nombres del elenco (era 1 y era 2), con
     los afijos de `TODAS_LAS_REGLAS`, con el castellano (`ES_STOPWORDS`,
     `RAICES_ESPANOLAS`, `CASTELLANO_CORRIENTE`, y el esqueleto de sus
     palabras); vecinas a UNA letra entre las voces caquetías del habla; la
     fonotáctica; `neologismo_valido`; si ya se dijo en la base; y cuántas
     formas de la base dejan de ser «raíz de ninguna parte» al entrar.
  4. LA TABLA DE COSTE POR OPCIÓN, que es lo que cita la propuesta.

Uso (desde proyecto-linguistico-caquetío/):

    python 6-fusion/scripts/medir_d11_voces_wayuu.py
    python 6-fusion/scripts/medir_d11_voces_wayuu.py --salida 6-fusion/medicion_d11_voces_wayuu_2026-09-23.yaml
    python 6-fusion/scripts/medir_d11_voces_wayuu.py --sin-base     # sin Docker
    python 6-fusion/scripts/medir_d11_voces_wayuu.py --check        # propuesta ↔ medición

⚠️ NO lee `curiana_sim/.env` ni llama a la API. `curiana_database` se importa
(lo necesita la casi-raíz de db.1) con `dotenv` sustituido por un módulo vacío,
así que su `load_dotenv()` no hace nada. A la base sólo le hace SELECT, con
`docker exec supabase_db_curiana_sim psql`. Regla 1: toda cifra de la
propuesta sale de aquí.
"""
from __future__ import annotations

import argparse
import datetime
import io
import re
import subprocess
import sys
import types
from collections import defaultdict
from pathlib import Path

R = Path(__file__).resolve().parents[2]

# ══════════════════════════════════════════════════════════════════════
# LAS OPCIONES QUE SE MIDEN — espejo de la propuesta (--check lo verifica)
# ══════════════════════════════════════════════════════════════════════
# tf.1 (2026-09-23) ya decidió los pronombres: no son de esta campaña.
PRONOMBRES_TF1 = ("taya", "pia", "nüma", "waya", "naya")

# Lo que la tanda final mete (tf.1-tf.3): una candidata no puede chocar con ello.
FORMAS_DE_LA_TANDA_FINAL = ("dai", "bui", "lihi", "tuhu", "waya", "naya",
                            "-kuba", "-ba", "da-")

# voz vieja → {letra: formas}. `[]` = archivar sin sustituta nueva. Una forma
# que YA es clave del lexicón (wasima, baharuko, bana) se mide igual.
OPCIONES = {
    "kashi":  {"A": ["danu"], "B": ["chabaka"], "C": []},
    "yama":   {"A": ["popoi"], "B": ["yaha"], "C": ["wayare"]},
    "sulu":   {"A": ["ruku"], "B": ["loko"], "C": []},
    "wana":   {"A": ["diki"], "B": ["kaba"], "C": []},
    "naba":   {"A": ["kuburuku"], "B": ["ikisi"], "C": []},
    "tüshi":  {"A": ["kasalini"], "B": []},
    "kapua":  {"A": ["mautia"], "B": ["tukamara"], "C": []},
    "anüiki": {"A": [], "B": ["dia"], "C": ["chuani"]},
    "pütchi": {"A": [], "B": ["dia"], "C": ["chuani"]},
    "wanü":   {"A": ["wasima"], "B": ["baharuko"]},
    "bana":   {"A": ["bana"], "B": []},
}
RECOMENDADA = {"kashi": "A", "yama": "A", "sulu": "A", "wana": "A", "naba": "A",
               "tüshi": "A", "kapua": "A", "anüiki": "A", "pütchi": "A",
               "wanü": "A", "bana": "A"}
# La opción que deja la voz como está (sólo cambia la justificación): coste 0.
SE_QUEDA = {("bana", "A")}
# Lo que se declararía de cada candidata al entrar (para la simulación de la puerta).
CAT_CANDIDATA = {"danu": "part", "chabaka": "part", "yaha": "part", "wayare": "part",
                 "ruku": "part", "loko": "part", "diki": "v_raiz", "kaba": "v_raiz",
                 "ikisi": "v_raiz", "kuburuku": "v_raiz", "kasalini": "v_estativo",
                 "mautia": "sust", "tukamara": "sust", "dia": "sust", "chuani": "sust"}

L = "a-záéíóúñüùàèïö"
# Un token no empieza pegado a un guion ni a un `+`: `biro+-bana` es la
# fórmula del locativo, no la palabra `bana`.
TOKEN = re.compile(rf"(?<![{L}\-+])[{L}]+(?:-[{L}]+)*", re.I)
# `nucleo_de_token` del motor; se fija al cargar curiana_lexicon.
_NUCLEO = None
# Los nombres del elenco TAL CUAL se escriben: «nombre o palabra lo decide la
# MAYÚSCULA» (CLAUDE.md) — `Wasima` es la matriarca y `wasima` 'viejo'.
_NOMBRES: frozenset = frozenset()


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(flujo.buffer, encoding="utf-8",
                                                  errors="replace", line_buffering=True))


def _sin_dotenv() -> None:
    """`curiana_database` hace `load_dotenv()` al importarse. Aquí no se lee
    `.env`: se le da un `dotenv` vacío antes de que nadie lo importe."""
    falso = types.ModuleType("dotenv")
    falso.load_dotenv = lambda *a, **k: False
    sys.modules["dotenv"] = falso


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
    respuestas = [(rid.strip("\n"), run, texto) for rid, run, texto in
                  _psql("select id, run_id, coalesce(response_text,'') from agent_responses")]
    total = int(_psql("select count(*) from word_uses")[0][0])
    runs = int(_psql("select count(*) from simulation_runs")[0][0])
    return usos, respuestas, (total, runs)


# ══════════════════════════════════════════════════════════════════════
LENGUAS_DESAMBIGUADORAS = {"achagua", "lokono", "kalinago", "taino", "taíno", "wayuu",
                           "wayunaiki", "paraujano", "caquetio", "caquetío"}


def base_de_clave(k: str) -> str:
    if "-" in k and not k.startswith("-") and k.rsplit("-", 1)[1] in LENGUAS_DESAMBIGUADORAS:
        return k.rsplit("-", 1)[0]
    return k


def contar_palabra(texto: str, forma: str) -> int:
    """Apariciones de la voz como palabra suelta o como segmento del NÚCLEO de
    una forma con guion (`wana-ka`, `kapua-bana`), nunca dentro de otra palabra
    ni como afijo: en `biro-bana` el `-bana` es el locativo (D9), no `bana`
    'hígado' — el núcleo lo da `nucleo_de_token`, el desafijador del motor."""
    f = forma.lower()
    n = 0
    for m in TOKEN.finditer(texto or ""):
        if m.group(0) in _NOMBRES:
            continue
        tok = m.group(0).lower()
        if tok == f or ("-" in tok and f in (_NUCLEO(tok) if _NUCLEO else tok.split("-"))):
            n += 1
    return n


def a_una_letra(a: str, b: str) -> bool:
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


# ══════════════════════════════════════════════════════════════════════
def medir(sim: Path, con_base: bool) -> dict:
    _sin_dotenv()
    sys.path.insert(0, str(sim))
    import curiana_lexicon as CL          # noqa: E402
    import curiana_koine as CK            # noqa: E402
    import curiana_fonotactica as CF      # noqa: E402
    import curiana_agents as AG1          # noqa: E402  (era 1: CURIANA_ELENCO sin fijar)
    import curiana_agents_era2 as AG2     # noqa: E402

    global _NUCLEO
    _NUCLEO = CL.nucleo_de_token
    V, F = CL.VOCABULARIO_BASE, CL.FUERA_DEL_HABLA
    fon = lambda s: CF.fonemizar(s, gu_es_w=True)          # D5c: gu → w
    esqueletos = defaultdict(list)
    for tabla, dic in (("VOCABULARIO_BASE", V), ("FUERA_DEL_HABLA", F)):
        for k, e in dic.items():
            esqueletos[fon(base_de_clave(k))].append((k, e.get("fuente"), tabla))
    nombres = set(AG1.ALL_AGENTS) | set(AG2.ALL_AGENTS)
    global _NOMBRES
    _NOMBRES = frozenset(nombres)
    segmentos_de_nombre = defaultdict(set)
    for n in nombres:
        for s in n.lower().split("-"):
            segmentos_de_nombre[s].add(n)
    fono, _paso = CF.medir()
    castellano = set(CL.ES_STOPWORDS) | set(CL.RAICES_ESPANOLAS) | set(getattr(CL, "CASTELLANO_CORRIENTE", ()))
    esqueleto_castellano = defaultdict(set)
    for w in castellano:
        esqueleto_castellano[fon(w)].add(w)
    caq_vivas = sorted(k for k, e in V.items() if str(e.get("fuente", "")).startswith("caquetío"))

    usos, respuestas, (total, total_runs) = ({}, [], (0, 0))
    if con_base:
        usos, respuestas, (total, total_runs) = cargar_base()

    # ── las plantillas y los demás sitios donde se enseña ────────────────
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
        "FORMAS_SEED": " ".join(" ".join(v) for v in CK.FORMAS_SEED.values()),
        "_NUCLEO_FALLBACK": " ".join(CK._NUCLEO_FALLBACK),
    }
    escena = (sim / "curiana_escena.py").read_text(encoding="utf-8")
    marca = re.search(r"_MARCA_CAQUETIA = re\.compile\(\s*r\"(.*?)\"", escena, re.S)
    marca_txt = marca.group(1) if marca else ""
    eventos_txt = (sim / "curiana_eventos.py").read_text(encoding="utf-8")
    tests = sorted((sim / "tests").glob("test_*.py"))
    textos_tests = {t.name: t.read_text(encoding="utf-8") for t in tests}
    fichas = " ".join((sim / f).read_text(encoding="utf-8")
                      for f in ("curiana_agents.py", "curiana_agents_era2.py") if (sim / f).exists())

    def ensenanza(voz: str) -> dict:
        p = {n: contar_palabra(t, voz) for n, t in plantillas.items()}
        en_tests = {n: contar_palabra(t, voz) for n, t in textos_tests.items()}
        return {
            "plantillas_que_la_ensenan": sum(1 for v in p.values() if v),
            "apariciones_en_plantillas": sum(p.values()),
            "por_plantilla": {n: v for n, v in p.items() if v},
            "en_reglas_del_motor": contar_palabra(reglas_txt, voz),
            "koine": {n: contar_palabra(t, voz) for n, t in koine.items() if contar_palabra(t, voz)},
            "escena_marca_caquetia": bool(re.search(rf"(?<![{L}]){re.escape(voz)}(?![{L}])", marca_txt)),
            "eventos_curiana_eventos": contar_palabra(eventos_txt, voz),
            "apariciones_en_tests": sum(en_tests.values()),
            "tests_que_la_nombran": sorted(n for n, v in en_tests.items() if v),
            "en_fichas_del_elenco": contar_palabra(fichas, voz),
        }

    # ── uso en la base ───────────────────────────────────────────────────
    def uso(forma: str) -> dict:
        if not con_base:
            return {"base": "no medida (sin Docker)"}
        f = forma.lower()
        n, r, u = usos.get(f, (0, 0, 0))
        seg_formas = [w for w in usos if "-" in w and f in CL.nucleo_de_token(w) and w != f]
        conteo = [(rid, run, contar_palabra(t, f)) for rid, run, t in respuestas]
        # sin los nombres del elenco: `Kawa-ni` no es aspecto ni `Yama-X` un deíctico
        con = [(rid, run, c) for rid, run, c in conteo if c]
        return {
            "word_uses_suelta": {"usos": n, "respuestas": r, "runs": u},
            "word_uses_como_nucleo_de_otra_forma": {
                "formas": len(seg_formas), "usos": sum(usos[w][0] for w in seg_formas),
                "ejemplos": sorted(seg_formas, key=lambda w: -usos[w][0])[:6]},
            "texto_de_respuestas": {"apariciones": sum(c for *_x, c in con),
                                    "respuestas": len(con), "runs": len({run for _r, run, _c in con})},
        }

    # ── colisiones de una forma ──────────────────────────────────────────
    def colisiones(forma: str, voz_vieja: str | None = None) -> dict:
        b = forma.lower()
        exacta = [[b, V[b].get("fuente"), (V[b].get("sig") or "")[:60]]] if b in V else []
        archivada = [[b, F[b].get("fuente")]] if b in F else []
        desamb = [[k, V[k].get("fuente")] for k in V if k != b and base_de_clave(k) == b]
        mismo = [list(x) for x in esqueletos.get(fon(b), []) if base_de_clave(x[0]) != b]
        tanda = [t for t in FORMAS_DE_LA_TANDA_FINAL
                 if fon(t.strip("-")) == fon(b)
                 or (t.endswith("-") and b.startswith(t[:-1]) and len(b) > len(t) - 1)
                 or (t.startswith("-") and b.endswith(t[1:]) and len(b) > len(t) - 1)]
        vecinas = [k for k in caq_vivas if len(b) >= 4 and a_una_letra(fon(b), fon(k))
                   and k != voz_vieja]
        ok, motivos = fono.valida(b)
        afijo = [a for a in CL.TODAS_LAS_REGLAS if a.strip("-").lower() == b]
        return {
            "clave_exacta": exacta,
            "archivada": archivada,
            "clave_con_desambiguador": desamb,
            "mismo_esqueleto_fonemico": mismo,
            "choque_con_la_tanda_final": tanda,
            "vecinas_a_una_letra_en_el_caquetio_del_habla": vecinas,
            "nombre_del_elenco": sorted(n for n in nombres if n.lower() == b),
            "segmento_de_nombre": sorted(segmentos_de_nombre.get(b, set())),
            "es_afijo_del_motor": afijo,
            "castellano_en_las_listas": b in castellano,
            "castellano_mismo_esqueleto": sorted(esqueleto_castellano.get(fon(b), set()) - {b}),
            "fonotactica_atestiguada": "pasa" if ok else "; ".join(motivos),
            "neologismo_valido": bool(CL.neologismo_valido(b)),
            "esqueleto": fon(b),
        }

    # ── la puerta: simular archivar / añadir ─────────────────────────────
    formas_base = list(usos)

    def _reset():
        CL._RAICES_CONOCIDAS = None
        CL._RAICES_VIVAS = None
        CL._VIVAS_CAQ_POR_LARGO = None
        CL._RAICES_VERB_CAQ = None

    def veredictos() -> dict:
        _reset()
        return {w: CL.es_raiz_de_ninguna_parte(w, archivadas_avalan=False) for w in formas_base}

    ref = veredictos() if con_base else {}

    def simular(archivar: list[str], nuevas: list[str]) -> dict:
        if not con_base:
            return {"base": "no medida"}
        guard_v, guard_f, guard_rv = dict(V), dict(F), set(CL._RAICES_VERB)
        try:
            for k in archivar:
                if k in V:
                    F[k] = V.pop(k)
                CL._RAICES_VERB.discard(k)
            for s in nuevas:
                if s not in V:
                    cat = CAT_CANDIDATA.get(s, "sust")
                    V[s] = {"sig": "(candidata)", "cat": cat, "fuente": "caquetío-hipotético"}
                    if cat in CL.CATS_VERBALES:
                        CL._RAICES_VERB.add(s)
            nuevo = veredictos()
        finally:
            V.clear(); V.update(guard_v)
            F.clear(); F.update(guard_f)
            CL._RAICES_VERB.clear(); CL._RAICES_VERB.update(guard_rv)
            _reset()
        a_ninguna = [w for w in formas_base if nuevo[w] and not ref[w]]
        de_ninguna = [w for w in formas_base if ref[w] and not nuevo[w]]
        return {
            "formas_que_pasan_a_raiz_de_ninguna_parte": {
                "formas": len(a_ninguna), "usos": sum(usos[w][0] for w in a_ninguna),
                "ejemplos": sorted(a_ninguna, key=lambda w: -usos[w][0])[:8]},
            "formas_que_dejan_de_ser_raiz_de_ninguna_parte": {
                "formas": len(de_ninguna), "usos": sum(usos[w][0] for w in de_ninguna),
                "ejemplos": sorted(de_ninguna, key=lambda w: -usos[w][0])[:8]},
        }

    # ══ 1. la lista ══════════════════════════════════════════════════════
    textos_plantilla = " ".join(plantillas.values())
    d11 = sorted(k for k, e in {**V, **F}.items() if "DEUDA D11" in str(e.get("notas", "")))
    en_habla = [k for k in d11 if k in V]
    ensenadas = [k for k in en_habla if contar_palabra(textos_plantilla, k)]
    campana = [k for k in en_habla if k not in PRONOMBRES_TF1]
    lista = {
        "deuda_d11_total": len(d11),
        "siguen_en_el_habla": len(en_habla),
        "ensenadas_por_alguna_plantilla": len(ensenadas),
        "no_ensenadas": sorted(set(en_habla) - set(ensenadas)),
        "pronombres_ya_decididos_tf1": [k for k in en_habla if k in PRONOMBRES_TF1],
        "las_de_esta_campana": campana,
        "las_de_esta_campana_n": len(campana),
        "fuera_del_habla": [k for k in d11 if k not in V],
        "aviso": ("se cuenta la voz suelta o como segmento de una forma con guion; "
                  "`bana` 'hígado' y el locativo -bana (D9) son dos entradas y el "
                  "sufijo NO se cuenta como la voz"),
    }
    faltan = sorted(set(OPCIONES) ^ set(campana))
    if faltan:
        lista["⚠ desfase_con_OPCIONES"] = faltan

    # ══ 2. las voces viejas ══════════════════════════════════════════════
    voces = {}
    for voz in campana:
        e = V[voz]
        ok, motivos = fono.valida(voz)
        voces[voz] = {
            "glosa": e.get("sig"), "cat": e.get("cat"), "fuente": e.get("fuente"),
            "fonotactica_atestiguada": "pasa" if ok else "; ".join(motivos),
            "comparte_esqueleto_con": [list(x) for x in esqueletos.get(fon(voz), [])
                                       if base_de_clave(x[0]) != voz],
            "segmento_de_nombre_del_elenco": sorted(segmentos_de_nombre.get(voz, set())),
            "uso": uso(voz),
            "ensenanza": ensenanza(voz),
            "si_se_archiva": simular([voz], []),
        }

    # ══ 3. las candidatas ════════════════════════════════════════════════
    candidatas = {}
    for voz, ops in OPCIONES.items():
        for letra, formas in ops.items():
            for f in formas:
                if f not in candidatas:
                    candidatas[f] = {"opciones": [], "colisiones": colisiones(f, voz), "uso_previo": uso(f)}
                candidatas[f]["opciones"].append(f"{voz}.{letra}")
    for f, c in candidatas.items():
        if f in V:
            c["ya_es_clave"] = [f, V[f].get("fuente"), (V[f].get("sig") or "")[:60]]
            c["al_entrar"] = "ya está en el lexicón: no entra nada nuevo"
        else:
            c["al_entrar"] = simular([], [f])

    # ══ 4. la tabla de coste por opción ══════════════════════════════════
    tabla = {}
    total_rec = {"voces_que_cambian": 0, "usos_sueltos": 0, "usos_como_nucleo": 0,
                 "suma_por_voz_de_respuestas_que_la_dicen": 0, "apariciones_en_plantillas": 0,
                 "apariciones_en_reglas_del_motor": 0, "apariciones_en_la_koine": 0,
                 "apariciones_en_tests": 0}
    for voz, ops in OPCIONES.items():
        vv = voces.get(voz, {})
        u = vv.get("uso", {})
        suelta = u.get("word_uses_suelta", {}).get("usos", 0) if con_base else None
        nucleo = u.get("word_uses_como_nucleo_de_otra_forma", {}).get("usos", 0) if con_base else None
        resp = u.get("texto_de_respuestas", {}).get("respuestas", 0) if con_base else None
        ens = vv.get("ensenanza", {})
        fila = {}
        for letra, formas in ops.items():
            se_queda = (voz, letra) in SE_QUEDA
            fila[letra] = {
                "formas": formas or ["(archivar sin sustituta)"],
                "se_queda_la_forma": se_queda,
                "usos_de_la_voz_vieja_que_dejan_de_contar": 0 if se_queda else suelta,
                "usos_como_nucleo_de_otra_forma": 0 if se_queda else nucleo,
                "respuestas_que_la_dicen": 0 if se_queda else resp,
                "plantillas_a_tocar": 0 if se_queda else ens.get("plantillas_que_la_ensenan", 0),
                "apariciones_en_plantillas": 0 if se_queda else ens.get("apariciones_en_plantillas", 0),
                "formas_de_la_base_a_raiz_de_ninguna_parte": (
                    0 if se_queda else vv.get("si_se_archiva", {})
                    .get("formas_que_pasan_a_raiz_de_ninguna_parte", {}).get("formas")),
                "colisiones_de_la_nueva": {
                    f: sum(1 for k, v in candidatas[f]["colisiones"].items()
                           if k in ("clave_exacta", "clave_con_desambiguador", "mismo_esqueleto_fonemico",
                                    "choque_con_la_tanda_final", "nombre_del_elenco", "es_afijo_del_motor")
                           and v and not (se_queda and k == "clave_exacta")
                           and not (k == "clave_exacta" and f in ("wasima", "baharuko", "popoi")))
                    + (1 if candidatas[f]["colisiones"]["castellano_en_las_listas"]
                       or candidatas[f]["colisiones"]["castellano_mismo_esqueleto"] else 0)
                    for f in formas},
                "fonotactica_de_la_nueva": {f: candidatas[f]["colisiones"]["fonotactica_atestiguada"]
                                            for f in formas},
            }
        fila["recomendada"] = RECOMENDADA[voz]
        tabla[voz] = fila
        rec = fila[RECOMENDADA[voz]]
        if not rec["se_queda_la_forma"] and con_base:
            total_rec["voces_que_cambian"] += 1
            total_rec["usos_sueltos"] += rec["usos_de_la_voz_vieja_que_dejan_de_contar"]
            total_rec["usos_como_nucleo"] += rec["usos_como_nucleo_de_otra_forma"]
            total_rec["suma_por_voz_de_respuestas_que_la_dicen"] += rec["respuestas_que_la_dicen"]
            total_rec["apariciones_en_plantillas"] += rec["apariciones_en_plantillas"]
            total_rec["apariciones_en_reglas_del_motor"] += ens.get("en_reglas_del_motor", 0)
            total_rec["apariciones_en_la_koine"] += sum(ens.get("koine", {}).values())
            total_rec["apariciones_en_tests"] += ens.get("apariciones_en_tests", 0)
    if con_base:
        # respuestas con AL MENOS UNA voz que cambia (una respuesta cuenta una vez)
        cambian = [v for v in OPCIONES if (v, RECOMENDADA[v]) not in SE_QUEDA]
        total_rec["respuestas_distintas_con_alguna_voz_que_cambia"] = sum(
            1 for _rid, _run, t in respuestas if any(contar_palabra(t, v) for v in cambian))
        total_rec["agent_responses"] = len(respuestas)
        # toda la recomendación a la vez, en la puerta
        archivar = [v for v in OPCIONES if (v, RECOMENDADA[v]) not in SE_QUEDA]
        nuevas = [f for v in archivar for f in OPCIONES[v][RECOMENDADA[v]] if f not in V]
        total_rec["en_la_puerta_todo_junto"] = simular(archivar, nuevas)

    return {
        "meta": {
            "medido": str(datetime.date.today()),
            "script": "6-fusion/scripts/medir_d11_voces_wayuu.py",
            "motor_medido": _rotulo(),
            "vocabulario_base": len(V), "fuera_del_habla": len(F),
            "todas_las_reglas": len(CL.TODAS_LAS_REGLAS),
            "elenco": {"era1": len(AG1.ALL_AGENTS), "era2": len(AG2.ALL_AGENTS)},
            "base": ({"word_uses": total, "agent_responses": len(respuestas),
                      "simulation_runs": total_runs, "formas_distintas": len(usos)}
                     if con_base else "no medida (sin Docker)"),
            "fonotactica": {"formas_base": len(fono.base),
                            "nota": "el filtro del módulo tal cual (medir()); los esqueletos de colisión usan gu→w (D5c)"},
            "puerta": ("es_raiz_de_ninguna_parte(forma, archivadas_avalan=False) sobre cada forma "
                       "distinta de word_uses, con la voz movida a FUERA_DEL_HABLA (y fuera de "
                       "_RAICES_VERB) y las cachés reiniciadas; se restaura después"),
        },
        "la_lista": lista,
        "voces_viejas": voces,
        "candidatas": candidatas,
        "coste_por_opcion": tabla,
        "coste_de_la_recomendacion": total_rec,
    }


def _rotulo() -> str:
    try:
        r = subprocess.run(["git", "-C", str(R), "log", "-1", "--format=%h %s"],
                           capture_output=True, timeout=30)
        return r.stdout.decode("utf-8", "replace").strip()[:120]
    except Exception:  # noqa: BLE001
        return "desconocido"


def _yaml(obj) -> str:
    import yaml
    return yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=110)


def check() -> int:
    """La propuesta y la medición dicen lo mismo: mismas voces, mismas letras,
    mismas formas y las cifras de `coste_medido` iguales a las de la medición."""
    import yaml
    prop = yaml.safe_load((R / "6-fusion" / "propuesta_d11_voces_wayuu_2026-09-23.yaml").read_text(encoding="utf-8"))
    med = yaml.safe_load((R / "6-fusion" / "medicion_d11_voces_wayuu_2026-09-23.yaml").read_text(encoding="utf-8"))
    malos = []
    voces_prop = {v["voz"]: v for v in prop.get("voces", [])}
    if set(voces_prop) != set(OPCIONES):
        malos.append(f"voces: propuesta {sorted(voces_prop)} / medidas {sorted(OPCIONES)}")
    for voz, v in voces_prop.items():
        if v.get("recomendacion") != RECOMENDADA.get(voz):
            malos.append(f"{voz}: recomendación {v.get('recomendacion')} / {RECOMENDADA.get(voz)}")
        for op in v.get("opciones", []):
            medidas = OPCIONES.get(voz, {}).get(op["letra"])
            if medidas is None or sorted(op.get("formas") or []) != sorted(medidas):
                malos.append(f"{voz}.{op['letra']}: formas {op.get('formas')} / {medidas}")
            cm = op.get("coste_medido") or {}
            fila = med["coste_por_opcion"].get(voz, {}).get(op["letra"], {})
            for campo, valor in cm.items():
                if campo in fila and fila[campo] != valor:
                    malos.append(f"{voz}.{op['letra']}.{campo}: propuesta {valor} / medición {fila[campo]}")
    print("\n".join(malos) if malos else "check: la propuesta y la medición coinciden")
    return 1 if malos else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sim", default=str(R / "curiana_sim"), help="el curiana_sim/ que se mide")
    ap.add_argument("--sin-base", action="store_true", help="no consulta Supabase")
    ap.add_argument("--salida", help="escribe el YAML medido en esta ruta")
    ap.add_argument("--check", action="store_true", help="propuesta ↔ medición")
    args = ap.parse_args(argv)
    if args.check:
        return check()
    out = medir(Path(args.sim), not args.sin_base)
    txt = _yaml(out)
    if args.salida:
        cab = ("# MEDICIÓN — D11 · las voces wayuu que quedan (tf.5): el coste de cada opción.\n"
               "# GENERADO por 6-fusion/scripts/medir_d11_voces_wayuu.py — no se edita a mano (regla 1).\n"
               "# La propuesta que lo usa: 6-fusion/propuesta_d11_voces_wayuu_2026-09-23.yaml\n")
        Path(args.salida).write_text(cab + txt, encoding="utf-8")
        print(f"escrito {args.salida}")
    else:
        print(txt)
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
