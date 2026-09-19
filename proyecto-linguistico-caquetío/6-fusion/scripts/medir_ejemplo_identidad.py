#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""El ejemplo de `IDENTIDAD_LINGUISTICA`: de `kali-bana` a `biro-bana`.

Decisión de Miguel del 2026-09-19 («Vale» a la recomendación de §7(a) del
issue `pares-atestiguado-reconstruido-2026-09-19.md`). Este script MIDE el
corte; no decide nada y no toca el canon (regla 5). Escribe
`6-fusion/medicion_ejemplo_identidad_2026-09-19.yaml`.

Qué mide, en orden:

  1. **Qué plantilla enseña qué forma de par ABIERTO.** Los 19 pares de §6
     siguen sin decidir: la pregunta no es sólo dónde sale `kali-bana`, es
     cuántas plantillas empujan a una de las dos formas de un par que Miguel
     aún no ha pesado. El criterio de «enseñar» es el ESTRECHO del script de
     pares (`formas_ensenadas`: voz seguida de glosa, los dos lados de una
     correspondencia `a→b`, y el ejemplo `[forma: … = …]`), no el ancho de
     `formas_en_texto()`, que cogería `para` dentro de «hilo para tejer».
     Las plantillas se LLAMAN, nunca se copian.

  2. **La puerta se mueve sola.** `FORMAS_DE_PLANTILLA` se construye llamando
     a las plantillas: al cambiar el ejemplo, `kali-bana` tiene que salir de
     la lista y `biro-bana` entrar, sin tocar la lista. Se mide el diff entero.

  3. **El largo del system prompt, antes y después**, en un ensayo SIN API
     sobre los 63 del elenco de la era 2 (la longitud predice el score,
     r = −0,48). El «antes» se construye sustituyendo la línea del EJEMPLO por
     la vieja —con `assert` de que la sustitución encontró algo—, así que los
     dos brazos salen del mismo motor y la única diferencia es el ejemplo.

  4. **Qué pasa con `kali-bana` al salir de la puerta**: vuelve a poder
     registrarse como acuñación. Se mide en la base quién la dijo, en qué
     runs, y cuántas veces se dijo el MOLDE `kali-…-bana` que el corte de #169
     nunca tocó. El contrafactual («¿la diría alguien sin el ejemplo
     delante?») no se puede correr sin API: lo que se da son los números que
     lo acotan.

  5. **El ejemplo nuevo es morfológicamente correcto y del mundo**: las dos
     piezas en el lexicón con su capa y su cita, `biro` fuera de todo par
     abierto y no homógrafa de un nombre del elenco, el compuesto nunca dicho
     en la base, y cuántos bloques `[Tu tierra]` de la era 2 hablan de la sal.

No abre `curiana_sim/.env` (stub de `dotenv` antes de importar el motor) y no
llama a la API. La base local se lee en SÓLO LECTURA con `docker exec psql`.

    CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 \
        python 6-fusion/scripts/medir_ejemplo_identidad.py
"""
import importlib.util
import os
import random
import re
import sys
import types
from collections import defaultdict

# ── El motor, sin abrir .env ──────────────────────────────────────────────
if "dotenv" not in sys.modules:
    _stub = types.ModuleType("dotenv")
    _stub.load_dotenv = lambda *a, **k: None          # noqa: E731
    _stub.dotenv_values = lambda *a, **k: {}          # noqa: E731
    sys.modules["dotenv"] = _stub

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIM = os.path.join(RAIZ, "curiana_sim")
if SIM not in sys.path:
    sys.path.insert(0, SIM)
os.environ.setdefault("CURIANA_ELENCO", "era2")

import curiana_agents as A                                          # noqa: E402
import curiana_lexicon as L                                         # noqa: E402
import curiana_mundo as M                                           # noqa: E402

FECHA = "2026-09-19"
SALIDA = os.path.join(RAIZ, "6-fusion", f"medicion_ejemplo_identidad_{FECHA}.yaml")
SEMILLA_ENSAYO = 20260919

# La línea que cambia, en sus dos versiones. El «antes» no es una cifra a
# mano: es el texto anterior, y la sustitución se comprueba con assert.
LINEA_VIEJA = ('EJEMPLO: "Taya wana-ka arima wara kari. Ta-barsure naba-ni. '
               '[kali-bana: kali+-bana = cerro del sol]."')
LINEA_NUEVA = ('EJEMPLO: "Taya wana-ka arima wara kari. Ta-barsure naba-ni. '
               '[biro-bana: biro+-bana = cerro de la sal]."')
FORMA_VIEJA = "kali-bana"
FORMA_NUEVA = "biro-bana"

# El script hermano trae el criterio ESTRECHO de «enseñar», las plantillas
# etiquetadas y el acceso de sólo lectura a la base. Se importa por ruta
# porque el nombre lleva guiones bajos y vive en el mismo directorio.
_spec = importlib.util.spec_from_file_location(
    "_medir_pares",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "medir_pares_atestiguado_reconstruido.py"))
PAR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PAR)


def _forzar_utf8():
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:                                           # noqa: BLE001
            pass


# ══════════════════════════════════════════════════════════════════════
# 0. LOS PARES ABIERTOS — se leen del YAML medido, no se copian
# ══════════════════════════════════════════════════════════════════════
def pares_abiertos() -> list[dict]:
    """Los pares de §6 que Miguel aún NO ha decidido.

    Se leen de `6-fusion/pares_atestiguado_reconstruido_2026-09-19.yaml`
    (`para_decidir`), que es lo que genera el script hermano. No se parsea con
    PyYAML para no añadir dependencia: el bloque tiene una forma fija y se lee
    con dos expresiones. El control es que salgan tantos pares como dice
    `censo.quedan_para_decidir` en el mismo fichero.
    """
    ruta = os.path.join(RAIZ, "6-fusion",
                        f"pares_atestiguado_reconstruido_{FECHA}.yaml")
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    declarado = int(re.search(r"^\s*quedan_para_decidir:\s*(\d+)\s*$",
                              texto, re.M).group(1))
    bloque = texto.split("\npares:\n", 1)[1]
    bloque = re.split(r"\n[a-z_]+:\n", bloque, maxsplit=1)[0]
    pares = []
    for i, trozo in enumerate(re.split(r"(?m)^  - glosa:", bloque)[1:], start=1):
        glosa = trozo.split("\n", 1)[0].strip().strip("'\"")
        att = re.search(r"^    atestiguada:\n      forma:\s*(\S+)",
                        trozo, re.M).group(1)
        der = re.search(r"^    derivada:\n      forma:\s*(\S+)",
                        trozo, re.M).group(1)
        pares.append({"n": i, "glosa": glosa,
                      "atestiguada": att, "derivada": der})
    assert len(pares) == declarado, (len(pares), declarado)
    return pares


# ══════════════════════════════════════════════════════════════════════
# 1. QUÉ PLANTILLA ENSEÑA QUÉ FORMA DE PAR ABIERTO
# ══════════════════════════════════════════════════════════════════════
def plantillas_y_pares(pares) -> dict:
    """Plantilla a plantilla: qué formas de par abierto enseña.

    Dos criterios, separados y con su nombre:
      · `ensena`   — criterio ESTRECHO (la forma en posición de voz enseñada)
      · `compuesto`— la forma dentro de un compuesto que la plantilla enseña
                     (`kali-bana` enseña `kali`); es lo que el corte de #169
                     no tocó.
    """
    formas = {}
    for p in pares:
        for lado in ("atestiguada", "derivada"):
            formas.setdefault(p[lado], []).append((p["n"], p["glosa"], lado))
    out = {"formas_de_pares_abiertos": len(formas), "plantillas": {}}
    for nombre, texto in PAR.plantillas_etiquetadas():
        ensenadas = PAR.formas_ensenadas(texto)
        compuestas = {x for x in ensenadas if "-" in x}
        dentro = defaultdict(list)
        for c in compuestas:
            for elem in c.split("-"):
                if elem in formas:
                    dentro[elem].append(c)
        ense = sorted(f for f in formas if f in ensenadas)
        out["plantillas"][nombre] = {
            "ensena_formas_de_par_abierto": ense,
            "detalle": [
                {"forma": f, "lado": formas[f][0][2],
                 "pares": sorted({n for n, _g, _l in formas[f]}),
                 "glosa": formas[f][0][1],
                 "dentro_de": sorted(dentro.get(f, []))}
                for f in ense],
            "moldes_con_forma_de_par": sorted(
                {c for cs in dentro.values() for c in cs}),
        }
    con = [n for n, d in out["plantillas"].items()
           if d["ensena_formas_de_par_abierto"]]
    out["plantillas_que_ensenan_alguna"] = sorted(con)
    out["n_plantillas"] = len(out["plantillas"])
    out["n_plantillas_que_ensenan_alguna"] = len(con)
    return out


def donde_sale_la_forma(forma: str) -> dict:
    """En qué plantillas sale una forma concreta, con los dos criterios."""
    ensena, token = [], []
    for nombre, texto in PAR.plantillas_etiquetadas():
        if forma in PAR.formas_ensenadas(texto):
            ensena.append(nombre)
        elif forma in L.formas_en_texto(texto):
            token.append(nombre)
    return {"ensena": ensena, "solo_como_token": token}


# ══════════════════════════════════════════════════════════════════════
# 2. LA PUERTA SE MUEVE SOLA
# ══════════════════════════════════════════════════════════════════════
def puerta_antes_y_despues(identidad_vieja: str) -> dict:
    """`FORMAS_DE_PLANTILLA` con el ejemplo viejo y con el nuevo.

    La lista se construye llamando a las plantillas, así que el «antes» se
    obtiene rehaciéndola con el texto viejo de la identidad — exactamente como
    el motor la haría — y no copiando nada.
    """
    def construir(identidad):
        textos = [identidad] + PAR.plantillas_etiquetadas()[1:]
        textos = [identidad] + [t for _n, t in PAR.plantillas_etiquetadas()[1:]]
        return frozenset(L.VOCABULARIO_BASE).union(
            *(L.formas_en_texto(t) for t in textos))

    antes = construir(identidad_vieja)
    despues = frozenset(L.FORMAS_DE_PLANTILLA)
    # control: la lista de HOY es la que el motor construye desde las
    # plantillas de HOY (si esto falla, el script no está midiendo el motor)
    assert despues == construir(L.IDENTIDAD_LINGUISTICA)
    return {"antes": len(antes), "despues": len(despues),
            "salen": sorted(antes - despues), "entran": sorted(despues - antes),
            "kali_bana_antes": FORMA_VIEJA in antes,
            "kali_bana_despues": FORMA_VIEJA in despues,
            "biro_bana_antes": FORMA_NUEVA in antes,
            "biro_bana_despues": FORMA_NUEVA in despues,
            "kali_sigue_en_la_puerta": "kali" in despues,
            "biro_sigue_en_la_puerta": "biro" in despues}


# ══════════════════════════════════════════════════════════════════════
# 3. EL LARGO DEL SYSTEM PROMPT — ensayo sin API sobre los 63
# ══════════════════════════════════════════════════════════════════════
def ensayo_de_prompt(identidad_vieja: str, era: str = "era2") -> dict:
    """Los system prompts del elenco, con el ejemplo viejo y con el nuevo.

    Se monta el turno de verdad (`orch.run_turn` con `_invoke` espiado, el
    patrón de `tests/test_formas_de_plantilla`), no una aproximación: entra el
    ensamblado entero —persona, identidad, mundo, `[Tu tierra]`, muestra del
    lexicón, memoria—. Los dos brazos se corren con la MISMA semilla del RNG
    global, que es de donde sale la muestra del lexicón.

    `era="era1"` corre la Curiana con el elenco viejo: la identidad es UNA
    constante y los dos mundos la leen, así que el corte la toca también y
    conviene medirlo en vez de suponerlo.

    No llama a la API: `_invoke` devuelve una respuesta fija y el Director
    está mudo.
    """
    import curiana_agents_era2 as _era2                             # noqa: F401
    import curiana_orchestrator_v2 as orch
    from curiana_observer import ObserverAgent
    from curiana_perfiles import cargar_perfil
    from curiana_state import estado_inicial, estado_inicial_test

    respuesta = "Taya wana-ka arima wara kari. Ta-barsure naba-ni."
    if era == "era2":
        elenco = dict(_era2.ALL_AGENTS)
        perfil = cargar_perfil("era2")
    else:
        # La era 1: el elenco de la Curiana, que `curiana_agents` sigue
        # teniendo en sus tres tiers aunque el activo sea el de Paraguaná.
        elenco = {**A.AGENTS_T1, **A.AGENTS_T2, **A.AGENTS_T3}
        assert set(elenco) == set(A.AGENTES_ERA1), "el elenco de la era 1 no cuadra"
        perfil = cargar_perfil("base")
    roster = list(elenco)

    def una_pasada(identidad):
        random.seed(SEMILLA_ENSAYO)
        orch._IDENTIDAD_LINGUISTICA = identidad
        capturas = []
        _invoke, _agentes = orch._invoke, orch.ALL_AGENTS
        _narrar, _evento = orch.director_narrate, orch.director_select_event
        orch._invoke = lambda c, system, user: (capturas.append(system)
                                                or respuesta)
        orch.director_narrate = lambda *a, **k: "(narración)"
        orch.director_select_event = lambda s: None
        orch.ALL_AGENTS = elenco
        try:
            if era == "era2":
                state = estado_inicial("PARAGUANÁ")
                state.turnos_por_dia = 6
            else:
                state = estado_inicial_test()
            state.escena = False
            state.capubana_cada = 0
            state.evento_del_turno = None
            lexico = L.LexicoComunitario()
            observer = ObserverAgent(None, lexico)
            orch.run_turn(None, state, orch.AgentMemory(), lexico, observer,
                          verbose=False, agentes_por_turno=len(roster),
                          roster=list(roster), capas=perfil.capas)
        finally:
            orch._invoke, orch.ALL_AGENTS = _invoke, _agentes
            orch.director_narrate, orch.director_select_event = _narrar, _evento
            orch._IDENTIDAD_LINGUISTICA = L.IDENTIDAD_LINGUISTICA
        return capturas

    antes = una_pasada(identidad_vieja)
    despues = una_pasada(L.IDENTIDAD_LINGUISTICA)
    assert len(antes) == len(despues) == len(roster), (len(antes), len(despues))

    def stats(xs):
        ns = sorted(len(x) for x in xs)
        return {"n": len(ns), "medio": round(sum(ns) / len(ns), 1),
                "mediana": ns[len(ns) // 2], "min": ns[0], "max": ns[-1]}

    deltas = [len(d) - len(a) for a, d in zip(antes, despues)]
    return {
        "prompts": len(antes),
        "antes": stats(antes), "despues": stats(despues),
        "delta_caracteres_por_prompt": sorted(set(deltas)),
        "delta_medio": round(sum(deltas) / len(deltas), 2),
        "identidad_antes_caracteres": len(identidad_vieja),
        "identidad_despues_caracteres": len(L.IDENTIDAD_LINGUISTICA),
        "identidad_delta": len(L.IDENTIDAD_LINGUISTICA) - len(identidad_vieja),
        "dice_kali_bana_antes": sum(1 for p in antes if FORMA_VIEJA in p),
        "dice_kali_bana_despues": sum(1 for p in despues if FORMA_VIEJA in p),
        "dice_biro_bana_despues": sum(1 for p in despues if FORMA_NUEVA in p),
    }


# ══════════════════════════════════════════════════════════════════════
# 4. LA BASE: `kali-bana`, el molde, y el compuesto nuevo
# ══════════════════════════════════════════════════════════════════════
def base_de_la_forma(runs) -> dict:
    """Quién dijo `kali-bana`, dónde, y cuánto pesa el MOLDE que sigue vivo.

    `word_uses` sólo tiene lo que el scorer reconoce, y una forma de plantilla
    no entra ahí desde el corte de #169: el conteo se hace sobre el TEXTO de
    `agent_responses`, con frontera de palabra, que es como lo contó el
    análisis del run `b7bc51dc`.
    """
    def contar(patron):
        filas = PAR.psql(
            "select r.run_id::text, count(*) from agent_responses r "
            f"where r.response_text ~* '{patron}' group by 1;")
        return {rid: int(n) for rid, n in filas}

    # `\m`/`\M` son las fronteras de palabra de Postgres; el guion SÍ es
    # frontera de palabra, así que la frontera sola no basta: se pide además
    # que lo que rodea al compuesto no sea guion ni letra. Así `kali-bana-iro`
    # y `ma-kali-bana` NO cuentan para `kali-bana`, igual que en el análisis
    # del run b7bc51dc.
    kb = contar(r"(^|[^a-zü-])kali-bana([^a-zü-]|$)")
    molde = contar(r"(^|[^a-zü-])kali(-[a-zü]+)+-bana([^a-zü-]|$)")
    bb = contar(r"(^|[^a-zü-])biro-bana([^a-zü-]|$)")
    agentes = PAR.psql(
        "select count(distinct agent_name) from agent_responses "
        "where response_text ~* '(^|[^a-zü-])kali-bana([^a-zü-]|$)';")[0][0]

    def por_bloque(d):
        out = defaultdict(int)
        for rid, n in d.items():
            out[runs.get(rid, {}).get("bloque", "?")] += n
        return dict(sorted(out.items()))

    return {
        "kali_bana_respuestas_en_texto": sum(kb.values()),
        "kali_bana_runs": len(kb),
        "kali_bana_agentes_distintos": int(agentes),
        "kali_bana_por_bloque": por_bloque(kb),
        "molde_kali_X_bana_respuestas": sum(molde.values()),
        "molde_kali_X_bana_por_bloque": por_bloque(molde),
        "biro_bana_respuestas_en_texto": sum(bb.values()),
        "biro_bana_runs": len(bb),
    }


def condicion_del_compuesto_nunca_dicho() -> list[dict]:
    """La condición 5 de §7(a), con los DOS criterios separados.

    El script del issue la midió sobre `word_uses` —«el compuesto no se ha
    dicho nunca en la base»— y ahí las tres candidatas dan 0. Pero
    `word_uses` sólo tiene lo que el scorer RECONOCE: una forma nueva que
    nadie adopta no llega nunca a esa tabla (es la trampa «una forma recién
    acuñada no es una `palabra_activa`»). Sobre el TEXTO de las respuestas el
    número es otro, y conviene que esté escrito: las tres se han dicho.

    Lo que sigue en pie para `biro-bana`: 0 en `word_uses`, 0 en
    `neologisms`, 0 en la competencia — no está compitiendo por ningún
    referente. Lo que cambia: no es verdad que no se haya dicho nunca.
    """
    serie = ("select id from simulation_runs where substring(id::text,1,8) "
             "in ('b847944d','17c2271e','9a98de67')")
    filas = PAR.psql(
        "with c(w) as (values ('biro-bana'),('kari-bana'),('maure-bana'),"
        "('kali-bana')) select c.w, "
        "(select count(*) from agent_responses r where r.response_text ~* "
        "('(^|[^a-zü-])'||c.w||'([^a-zü-]|$)')), "
        "(select count(distinct r.agent_name) from agent_responses r where "
        "r.response_text ~* ('(^|[^a-zü-])'||c.w||'([^a-zü-]|$)')), "
        "(select count(*) from word_uses u where u.word=c.w), "
        "(select count(*) from neologisms n where n.form=c.w), "
        f"(select count(*) from agent_responses r where r.run_id in ({serie}) "
        "and r.response_text ~* ('(^|[^a-zü-])'||c.w||'([^a-zü-]|$)')) "
        "from c order by 1;")
    return [{"compuesto": w, "respuestas_en_texto": int(a),
             "agentes_distintos": int(b), "word_uses": int(c),
             "neologisms": int(d), "serie_c_limpia_respuestas": int(e)}
            for w, a, b, c, d, e in filas]


# ══════════════════════════════════════════════════════════════════════
# 5. EL EJEMPLO NUEVO: morfología, capa y mundo
# ══════════════════════════════════════════════════════════════════════
def ficha_del_ejemplo(pares) -> dict:
    """Las cinco condiciones, verificadas aquí otra vez."""
    en_pares = {p[l] for p in pares for l in ("atestiguada", "derivada")}
    nombres = frozenset(n.lower() for n in A.ALL_AGENTS)
    biro = L.VOCABULARIO_BASE.get("biro") or {}
    # `-bana` es un afijo de las reglas del motor, no una clave del lexicón:
    # se verifica contra la tabla de sufijos con la que el motor segmenta.
    sufijos = {a.lower() for a in L.TODAS_LAS_REGLAS}
    sal = sum(1 for s, p, m in M.combinaciones()
              if "sal" in (M.bloque_tu_tierra(s, p, m) or "").lower())
    total = sum(1 for _ in M.combinaciones())
    return {
        "raiz": "biro",
        "capa": biro.get("fuente"),
        "cat": biro.get("cat"),
        "glosa": biro.get("sig"),
        "cita": " ".join(str(biro.get("notas") or "").split())[:240],
        "sufijo": "-bana",
        "sufijo_en_las_reglas_del_motor": "-bana" in sufijos,
        "raiz_en_un_par_abierto": "biro" in en_pares,
        "raiz_homografa_de_un_nombre_del_elenco": "biro" in nombres,
        "compuesto_es_clave_del_lexicon": FORMA_NUEVA in L.VOCABULARIO_BASE,
        "bloques_tu_tierra_totales": total,
        "bloques_tu_tierra_que_hablan_de_sal": sal,
    }


# ══════════════════════════════════════════════════════════════════════
def main():
    _forzar_utf8()
    identidad_vieja = L.IDENTIDAD_LINGUISTICA.replace(LINEA_NUEVA, LINEA_VIEJA)
    assert identidad_vieja != L.IDENTIDAD_LINGUISTICA, (
        "la línea del EJEMPLO no es la esperada: revisa LINEA_NUEVA")
    assert LINEA_VIEJA in identidad_vieja

    pares = pares_abiertos()
    plant = plantillas_y_pares(pares)
    puerta = puerta_antes_y_despues(identidad_vieja)
    ens = ensayo_de_prompt(identidad_vieja, era="era2")
    ens1 = ensayo_de_prompt(identidad_vieja, era="era1")
    ficha = ficha_del_ejemplo(pares)
    runs = PAR.leer_runs()
    base = base_de_la_forma(runs)
    cond5 = condicion_del_compuesto_nunca_dicho()
    vieja = donde_sale_la_forma(FORMA_VIEJA)
    nueva = donde_sale_la_forma(FORMA_NUEVA)

    print()
    print("═" * 72)
    print("EL EJEMPLO DE IDENTIDAD_LINGUISTICA — corte del 2026-09-19")
    print("═" * 72)
    print(f"Pares ABIERTOS de §6 (sin decidir): {len(pares)}")
    print(f"Formas distintas en esos pares: {plant['formas_de_pares_abiertos']}")
    print(f"Plantillas estáticas medidas: {plant['n_plantillas']}")
    print("Plantillas que enseñan alguna forma de par abierto: "
          f"{plant['n_plantillas_que_ensenan_alguna']}")
    for nombre in plant["plantillas_que_ensenan_alguna"]:
        d = plant["plantillas"][nombre]
        detalle = " · ".join(
            f"{x['forma']} ({x['lado'][:3]}, par {','.join(map(str, x['pares']))})"
            for x in d["detalle"])
        print(f"   {nombre}: {detalle}")
        if d["moldes_con_forma_de_par"]:
            print(f"      moldes: {' '.join(d['moldes_con_forma_de_par'])}")
    print()
    print(f"`{FORMA_VIEJA}` la enseñan ahora: {vieja['ensena'] or '—'}"
          f"   (sólo como token: {vieja['solo_como_token'] or '—'})")
    print(f"`{FORMA_NUEVA}` la enseñan ahora: {nueva['ensena'] or '—'}")
    print()
    print("LA PUERTA (FORMAS_DE_PLANTILLA)")
    print(f"   antes {puerta['antes']} · después {puerta['despues']}")
    print(f"   salen: {puerta['salen'] or '—'}")
    print(f"   entran: {puerta['entran'] or '—'}")
    print(f"   `kali` sigue dentro (es clave del lexicón): "
          f"{puerta['kali_sigue_en_la_puerta']}")
    print()
    print(f"EL PROMPT, ensayo sin API sobre {ens['prompts']} agentes")
    print(f"   antes:   medio {ens['antes']['medio']} car. · mediana "
          f"{ens['antes']['mediana']} · min {ens['antes']['min']} · max "
          f"{ens['antes']['max']}")
    print(f"   después: medio {ens['despues']['medio']} car. · mediana "
          f"{ens['despues']['mediana']} · min {ens['despues']['min']} · max "
          f"{ens['despues']['max']}")
    print(f"   Δ por prompt: {ens['delta_caracteres_por_prompt']} caracteres "
          f"(medio {ens['delta_medio']})")
    print(f"   prompts que decían `{FORMA_VIEJA}`: {ens['dice_kali_bana_antes']} "
          f"→ {ens['dice_kali_bana_despues']}; dicen `{FORMA_NUEVA}`: "
          f"{ens['dice_biro_bana_despues']}")
    print()
    print(f"LA ERA 1 TAMBIÉN LO LEE — la identidad es UNA constante "
          f"({ens1['prompts']} agentes de la Curiana)")
    print(f"   antes:   medio {ens1['antes']['medio']} car. · mediana "
          f"{ens1['antes']['mediana']}")
    print(f"   después: medio {ens1['despues']['medio']} car. · mediana "
          f"{ens1['despues']['mediana']}")
    print(f"   Δ por prompt: {ens1['delta_caracteres_por_prompt']} caracteres; "
          f"prompts que decían `{FORMA_VIEJA}`: {ens1['dice_kali_bana_antes']} "
          f"→ {ens1['dice_kali_bana_despues']}")
    print("   ⇒ la era 1 DEJA DE SER BYTE A BYTE con los runs de la Curiana.")
    print()
    print("LA BASE")
    print(f"   `{FORMA_VIEJA}` en {base['kali_bana_respuestas_en_texto']} "
          f"respuestas de {base['kali_bana_agentes_distintos']} agentes en "
          f"{base['kali_bana_runs']} runs: {base['kali_bana_por_bloque']}")
    print(f"   el MOLDE `kali-…-bana` (que #169 no tocó): "
          f"{base['molde_kali_X_bana_respuestas']} respuestas "
          f"{base['molde_kali_X_bana_por_bloque']}")
    print()
    print("CONDICIÓN 5 DE §7(a) — «el compuesto no se ha dicho nunca», los dos")
    print("criterios: `word_uses` (lo que el scorer reconoce) vs. el TEXTO")
    print(f"   {'compuesto':<12} {'texto':>6} {'agentes':>8} {'word_uses':>10} "
          f"{'neolog':>7} {'serie C':>8}")
    for c in cond5:
        print(f"   {c['compuesto']:<12} {c['respuestas_en_texto']:>6} "
              f"{c['agentes_distintos']:>8} {c['word_uses']:>10} "
              f"{c['neologisms']:>7} {c['serie_c_limpia_respuestas']:>8}")
    print("   ⚠ sobre `word_uses` las tres candidatas dan 0 —es lo que midió el")
    print("     issue—, pero sobre el TEXTO las tres se han dicho. Lo que sigue")
    print("     en pie para `biro-bana`: 0 en word_uses, 0 en neologisms, 0 en")
    print("     la competencia. Lo que NO: que no se haya dicho nunca.")
    print()
    print("EL EJEMPLO NUEVO")
    print(f"   biro: {ficha['capa']} · {ficha['cat']} · «{ficha['glosa']}»")
    print(f"   -bana en las reglas del motor: "
          f"{ficha['sufijo_en_las_reglas_del_motor']}")
    print(f"   biro en un par abierto: {ficha['raiz_en_un_par_abierto']} · "
          f"homógrafa de un nombre: "
          f"{ficha['raiz_homografa_de_un_nombre_del_elenco']}")
    print(f"   [Tu tierra] habla de la sal en "
          f"{ficha['bloques_tu_tierra_que_hablan_de_sal']} de "
          f"{ficha['bloques_tu_tierra_totales']} bloques")
    print()

    doc = []
    W = doc.append
    W("# ─────────────────────────────────────────────────────────────────")
    W("# EL EJEMPLO DE `IDENTIDAD_LINGUISTICA` — MEDICIÓN DEL CORTE")
    W("#")
    W("# GENERADO por 6-fusion/scripts/medir_ejemplo_identidad.py")
    W("# No se edita a mano: se regenera. La decisión está en")
    W("# 6-fusion/decisiones_tanda_2026-09-19.yaml (d19.a).")
    W("# ─────────────────────────────────────────────────────────────────")
    W("meta:")
    W(f"  fecha: '{FECHA}'")
    W("  generado_por: 6-fusion/scripts/medir_ejemplo_identidad.py")
    W("  elenco: era2")
    W("  perfil_de_exposicion: era2")
    W("  decision: >-")
    W("    Miguel, 2026-09-19: «Vale» a la recomendación de §7(a) del issue")
    W("    pares-atestiguado-reconstruido-2026-09-19.md. El ejemplo de")
    W("    IDENTIDAD_LINGUISTICA deja de usar kali-bana y pasa a biro-bana.")
    W("  linea_vieja: >-")
    W(f"    {LINEA_VIEJA}")
    W("  linea_nueva: >-")
    W(f"    {LINEA_NUEVA}")
    W("pares_abiertos:")
    W(f"  n: {len(pares)}   # los 19 de §6: NINGUNO está decidido todavía")
    W(f"  formas_distintas: {plant['formas_de_pares_abiertos']}")
    W("  # Miguel decidió (a) — el ejemplo — y NO los pares. Lo que una")
    W("  # plantilla enseñe de un par abierto se anota y no se toca.")
    W("plantillas:")
    W(f"  n: {plant['n_plantillas']}")
    W(f"  que_ensenan_forma_de_par_abierto: {plant['n_plantillas_que_ensenan_alguna']}")
    W("  detalle:")
    for nombre in sorted(plant["plantillas"]):
        d = plant["plantillas"][nombre]
        W(f"    {nombre}:")
        W(f"      ensena_formas_de_par_abierto: [{', '.join(d['ensena_formas_de_par_abierto'])}]")
        if d["moldes_con_forma_de_par"]:
            W(f"      moldes_con_forma_de_par: [{', '.join(d['moldes_con_forma_de_par'])}]")
        if d["detalle"]:
            W("      formas:")
            for x in d["detalle"]:
                W(f"        - forma: {x['forma']}")
                W(f"          lado: {x['lado']}")
                W(f"          pares: [{', '.join(str(n) for n in x['pares'])}]")
                W(f"          glosa: '{x['glosa']}'")
                if x["dentro_de"]:
                    W(f"          dentro_de: [{', '.join(x['dentro_de'])}]")
    W("donde_sale_cada_forma:")
    for etiqueta, d in ((FORMA_VIEJA, vieja), (FORMA_NUEVA, nueva)):
        W(f"  {etiqueta}:")
        W(f"    ensena: [{', '.join(d['ensena'])}]")
        W(f"    solo_como_token: [{', '.join(d['solo_como_token'])}]")
    W("puerta_formas_de_plantilla:")
    W(f"  antes: {puerta['antes']}")
    W(f"  despues: {puerta['despues']}")
    W(f"  salen: [{', '.join(puerta['salen'])}]")
    W(f"  entran: [{', '.join(puerta['entran'])}]")
    W(f"  kali_bana_antes: {str(puerta['kali_bana_antes']).lower()}")
    W(f"  kali_bana_despues: {str(puerta['kali_bana_despues']).lower()}")
    W(f"  biro_bana_antes: {str(puerta['biro_bana_antes']).lower()}")
    W(f"  biro_bana_despues: {str(puerta['biro_bana_despues']).lower()}")
    W(f"  kali_sigue_en_la_puerta: {str(puerta['kali_sigue_en_la_puerta']).lower()}"
      "   # es clave del lexicón: la puerta incluye VOCABULARIO_BASE entero")
    W(f"  biro_sigue_en_la_puerta: {str(puerta['biro_sigue_en_la_puerta']).lower()}")
    W("largo_del_prompt:")
    W("  # Ensayo SIN API: un turno con el elenco entero, sin escena, misma")
    W("  # semilla del RNG global en los dos brazos (de ahí sale la muestra")
    W("  # del lexicón). El ensamblado es el de verdad: `orch.run_turn` con")
    W("  # `_invoke` espiado, no una aproximación.")
    W(f"  semilla: {SEMILLA_ENSAYO}")
    for etiqueta, e, perfil_txt in (("era2", ens, "era2, 63 agentes de Paraguaná"),
                                    ("era1", ens1, "base, 60 agentes de la Curiana")):
        W(f"  {etiqueta}:")
        W(f"    perfil: {perfil_txt}")
        W(f"    prompts: {e['prompts']}")
        for lado in ("antes", "despues"):
            W(f"    {lado}:")
            for k, v in e[lado].items():
                W(f"      {k}: {v}")
        W(f"    delta_caracteres_por_prompt: [{', '.join(str(d) for d in e['delta_caracteres_por_prompt'])}]")
        W(f"    delta_medio: {e['delta_medio']}")
        W(f"    prompts_que_decian_kali_bana: {e['dice_kali_bana_antes']}")
        W(f"    prompts_que_dicen_kali_bana: {e['dice_kali_bana_despues']}")
        W(f"    prompts_que_dicen_biro_bana: {e['dice_biro_bana_despues']}")
    W(f"  identidad_antes_caracteres: {ens['identidad_antes_caracteres']}")
    W(f"  identidad_despues_caracteres: {ens['identidad_despues_caracteres']}")
    W(f"  identidad_delta: {ens['identidad_delta']}")
    W("  lectura: >-")
    W("    La longitud del prompt predice el score (r = −0,48), así que un")
    W("    cambio de ejemplo hay que medirlo aunque parezca cosmético. Aquí")
    W(f"    el prompt se mueve {ens['delta_medio']} caracteres de media sobre")
    W(f"    ~{ens['despues']['medio']:.0f} en la era 2 (y")
    W(f"    {ens1['delta_medio']} sobre ~{ens1['despues']['medio']:.0f} en la")
    W("    era 1): es ruido frente a la variación entre agentes (min/max")
    W("    arriba, cuatro mil caracteres de rango), pero queda escrito.")
    W("  era_1: >-")
    W("    `IDENTIDAD_LINGUISTICA` es UNA constante y los dos mundos la leen:")
    W("    el corte toca también la Curiana. No se parte en dos plantillas")
    W("    —sería una decisión de diseño que nadie ha tomado, y `biro` 'sal'")
    W("    es tan del Golfete de Coro como de Paraguaná: la sal ES el recurso")
    W("    de Coro—. Consecuencia declarada: LA ERA 1 DEJA DE SER BYTE A BYTE.")
    W("    Los runs viejos no se reescriben; lo que se pierde es poder")
    W("    re-correr la era 1 y comparar carácter a carácter contra ellos.")
    W("base:")
    for k, v in base.items():
        if isinstance(v, dict):
            W(f"  {k}:")
            for kk, vv in v.items():
                W(f"    '{kk}': {vv}")
        else:
            W(f"  {k}: {v}")
    W("condicion_5_el_compuesto_nunca_dicho:")
    W("  # §7(a) pedía que el compuesto del ejemplo no se hubiera dicho nunca.")
    W("  # El script del issue lo midió sobre `word_uses`, que sólo tiene lo")
    W("  # que el SCORER reconoce: una forma que nadie adopta no llega ahí")
    W("  # (trampa «una forma recién acuñada no es una palabra_activa»). Sobre")
    W("  # el TEXTO de las respuestas el número es otro. Los dos, aquí.")
    W("  candidatas:")
    for c in cond5:
        W(f"    - compuesto: {c['compuesto']}")
        W(f"      respuestas_en_texto: {c['respuestas_en_texto']}")
        W(f"      agentes_distintos: {c['agentes_distintos']}")
        W(f"      word_uses: {c['word_uses']}")
        W(f"      neologisms: {c['neologisms']}")
        W(f"      serie_c_limpia_respuestas: {c['serie_c_limpia_respuestas']}")
    W("  lectura: >-")
    W("    Sobre `word_uses` las tres candidatas dan 0 y la condición se daba")
    W("    por cumplida. Sobre el texto, las tres se han dicho y `biro-bana`")
    W("    es la más dicha de las tres. Lo que sigue en pie —y es lo que la")
    W("    condición quería evitar— es que el ejemplo bendiga a una forma que")
    W("    ya COMPITE: `biro-bana` tiene 0 en `word_uses`, 0 en `neologisms` y")
    W("    no es variante de ningún referente abierto. Queda escrito para que")
    W("    la próxima medición no vuelva a decir «nunca» midiendo otra cosa.")
    W("  lo_que_deja_a_miguel: >-")
    W("    Si la condición que quería era la del TEXTO, la candidata que la")
    W("    cumple en la serie C limpia es `maure-bana` (0 respuestas allí, 29")
    W("    en toda la base). No se ha cambiado nada: la decisión dice")
    W("    `biro-bana` y eso es lo aplicado.")
    W("que_pasa_con_kali_bana_al_salir_de_la_puerta:")
    W("  lectura: >-")
    W("    Al salir de la puerta, `kali-bana` vuelve a poder registrarse como")
    W("    acuñación. Lo que la base acota: todos sus usos son de runs que")
    W("    tenían el ejemplo delante, así que no hay contrafactual. Pero el")
    W("    MOLDE `kali-…-bana` —que el corte de #169 nunca tocó— sí se dijo")
    W("    sin que ninguna plantilla lo enseñara, y `kali` sigue siendo clave")
    W("    del lexicón y voz del muestreador: la forma es componible y puede")
    W("    volver. Si debe quedar vetada por haber sido ejemplo histórico, es")
    W("    una decisión de Miguel y NO está implementada.")
    W("ejemplo_nuevo:")
    for k, v in ficha.items():
        if isinstance(v, bool):
            W(f"  {k}: {str(v).lower()}")
        elif isinstance(v, int):
            W(f"  {k}: {v}")
        else:
            W(f"  {k}: '{str(v).replace(chr(39), chr(39) * 2)}'")
    W("")
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(doc))
    print(f"✓ escrito {os.path.relpath(SALIDA, RAIZ)}  ({len(doc)} líneas)")


if __name__ == "__main__":
    main()
