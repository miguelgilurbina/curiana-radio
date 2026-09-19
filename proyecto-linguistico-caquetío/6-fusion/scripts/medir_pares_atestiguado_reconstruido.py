#!/usr/bin/env python3
"""LOS PARES ATESTIGUADO / RECONSTRUIDO, medidos.

El hallazgo que lo motiva (Miguel, 2026-09-18, de oído): «¿por qué es kali si
sol es kazi?». El lexicón tiene DOS palabras vivas para 'sol' — `kasi`
(atestiguada, Zavala #76, el `cazi` de las fuentes ya fonemizado por D5) y
`kali` (reconstruida, «núcleo fundacional») — y el elenco dice la reconstruida.
Lo mismo con 'luna': `kati` atestiguada y `kasha` reconstruida.

Esto mide TRES cosas y no propone ninguna:

  1. CUÁNTOS PARES hay. Recorre `VOCABULARIO_BASE` quedándose con las entradas
     cuyo `fuente` empieza por `caquetío-`, normaliza la glosa (que es texto
     libre) y busca los significados que tienen a la vez una forma atestiguada
     y otra de una capa derivada. Se dan los dos números: ESTRICTO y LAXO.
  2. EL USO REAL. Cuántas veces dijo el elenco cada forma en TODA la base
     (`word_uses`), por era y por serie, y aparte en la serie C limpia, CON
     sus compuestos.
  3. LA EXPOSICIÓN. Cuánto empuja el instrumento a cada forma: si está en
     `FORMAS_DE_PLANTILLA`, en qué plantilla concreta, en `[Tu tierra]` y
     cuántas veces sale en el muestreo del prompt.

Y separa aparte (§4 del encargo) los pares donde la forma «reconstruida» es en
realidad la MISMA palabra con otra grafía: eso no es una decisión de canon sino
una fusión pendiente de D5.

    python 6-fusion/scripts/medir_pares_atestiguado_reconstruido.py
    python 6-fusion/scripts/medir_pares_atestiguado_reconstruido.py --yaml
    python 6-fusion/scripts/medir_pares_atestiguado_reconstruido.py --sin-base

LO QUE NO HACE, por regla dura del encargo:
  · No toca `curiana_lexicon.py` ni el motor. Propone en 6-fusion/ (regla 5).
  · No llama a la API y no lee `curiana_sim/.env`. El `load_dotenv()` de
    `curiana_database` se neutraliza con un stub de `dotenv` ANTES de importar
    nada del motor: así se puede usar el `normalize_source_language()` de
    verdad —que es la puerta canónica— sin que el fichero de secretos se abra.
  · No escribe en la base. Lee por `docker exec … psql`, que es la vía que
    CLAUDE.md declara para el Supabase local.

CONTROLES (si fallan, lo de abajo no mide nada):
  · La lógica de raíz de los compuestos NO es un regex de este script: es la
    del motor. `_candidatos_motor()` reproduce paso a paso la construcción de
    candidatos de `curiana_lexicon._familia_de_token()` —con SUS tablas de
    afijos (`_PREFIJOS_CAQ`, `_SUFIJOS_CAQ`, `_RAICES_VERB`), no con una
    copia— y el control comprueba, token a token de toda la base, que el
    primer candidato que cae en `VOCABULARIO_BASE` devuelve exactamente la
    misma lengua que `_familia_de_token()`.
  · La serie C limpia se declara por sus tres ids y se VERIFICA que forman una
    cadena `continuado_desde` de tres días.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import random
import subprocess
import sys
import types
import unicodedata
from collections import defaultdict

# ── El motor, sin abrir .env ──────────────────────────────────────────────
# El stub va ANTES de cualquier import del motor: `curiana_database` hace
# `from dotenv import load_dotenv; load_dotenv(...)` al cargarse.
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

import curiana_lexicon as L                                        # noqa: E402
import curiana_agents as A                                         # noqa: E402
import curiana_mundo as M                                          # noqa: E402
import curiana_perfiles as P                                       # noqa: E402
from curiana_database import normalize_source_language             # noqa: E402
from curiana_fonotactica import fonemizar                          # noqa: E402

FECHA = "2026-09-19"
SALIDA = os.path.join(RAIZ, "6-fusion",
                      f"pares_atestiguado_reconstruido_{FECHA}.yaml")
CONTENEDOR = "supabase_db_curiana_sim"
SEMILLA_ENSAYO = 20260919
DRAWS_POR_AGENTE = 20

# La serie C limpia, declarada (los tres runs del encargo) y verificada abajo
# como cadena `continuado_desde`.
SERIE_C_LIMPIA = ("b847944d", "17c2271e", "9a98de67")

CAPAS = {
    "caquetío-atestiguado": "atestiguado",
    "caquetío-reconstruido": "reconstruido",
    "caquetío-retroabstraido": "retroabstraido",
    "caquetío-hipotético": "hipotetico",
}
DERIVADAS = ("reconstruido", "retroabstraido", "hipotetico")


def _forzar_utf8():
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:                                          # noqa: BLE001
            pass


# ══════════════════════════════════════════════════════════════════════
# 1. LA GLOSA: normalización declarada
# ══════════════════════════════════════════════════════════════════════
# La glosa (`sig`) es texto libre: «sol», «luna», «cerro, sitio alto»,
# «alma, esencia vital, fuerza interior», «yo (1ra persona singular)».
# Se normaliza así, y SÓLO así:
#
#   n1. NFC + minúsculas.
#   n2. Fuera lo que va entre paréntesis y entre corchetes —es comentario del
#       curador, no glosa: «(1ra persona singular)», «(< anasü Wayunaiki)».
#   n3. Fuera los diacríticos (á→a, ü→u, ñ→n): las glosas están escritas a
#       mano en veinte tandas y la tilde no es información.
#   n4. Fuera el artículo o el cuantificador inicial (el/la/los/las/un/una/lo)
#       y la puntuación de los extremos; espacios colapsados.
#
# NO se aplica ningún diccionario de sinónimos. Decidir que «cerro» y «loma»
# son la misma glosa es una afirmación sobre el significado, y eso lo decide
# Miguel (regla 2: en duda, degradar). Lo que el encargo llama «sinónimos
# evidentes» se captura en el criterio LAXO, que no inventa equivalencias:
# compara el primer sinónimo que la propia glosa ya separa con una coma.
_ARTICULOS = ("el ", "la ", "los ", "las ", "un ", "una ", "lo ", "unos ", "unas ")


def norm_completa(sig: str) -> str:
    s = unicodedata.normalize("NFC", (sig or "")).lower()
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn")
    s = s.replace("ñ", "n")
    s = re.sub(r"\s+", " ", s).strip(" .,;:—-·")
    s = re.sub(r"\s*([,;])\s*", r"\1", s)
    for art in _ARTICULOS:
        if s.startswith(art):
            s = s[len(art):]
            break
    return s.strip()


def _sin_articulo(s: str) -> str:
    for art in _ARTICULOS:
        if s.startswith(art):
            return s[len(art):].strip()
    return s.strip()


def sinonimos(sig: str) -> list[str]:
    """Los sinónimos que la GLOSA YA SEPARA con coma o punto y coma.

    No es un diccionario de sinónimos: es la lista que el propio curador
    escribió. «cerro, sitio alto» da dos; «sol» da uno.
    """
    return [x for x in (_sin_articulo(t.strip())
                        for t in re.split(r"[,;]", norm_completa(sig))) if x]


def norm_primer(sig: str) -> str:
    """El primer sinónimo: lo que va antes de la primera coma o punto y coma."""
    s = sinonimos(sig)
    return s[0] if s else ""


def _contenida(a: str, b: str) -> bool:
    """¿`a` está contenida en `b` como secuencia de palabras enteras?"""
    if not a or not b or a == b:
        return False
    pa = [t for t in re.split(r"[,;\s]+", a) if t]
    pb = [t for t in re.split(r"[,;\s]+", b) if t]
    if not pa or len(pa) > len(pb):
        return False
    return any(pb[i:i + len(pa)] == pa for i in range(len(pb) - len(pa) + 1))


# ══════════════════════════════════════════════════════════════════════
# 2. LA RAÍZ Y SUS COMPUESTOS: la lógica del motor, no un regex propio
# ══════════════════════════════════════════════════════════════════════
def _candidatos_motor(tok: str) -> list[str]:
    """Los candidatos de raíz que prueba `curiana_lexicon._familia_de_token`.

    Paso a paso lo mismo que el motor, y con SUS tablas: `_PREFIJOS_CAQ` y
    `_SUFIJOS_CAQ` salen de `TODAS_LAS_REGLAS` y `_RAICES_VERB` de las
    entradas `cat: v_raiz` del propio `VOCABULARIO_BASE`. El control de abajo
    comprueba que esta reproducción da la misma lengua que el motor para
    todos los tokens de la base; si no, este script no mide nada.
    """
    candidatos = [tok]
    if "-" in tok:
        partes = tok.split("-")
        nucleo = partes
        if len(nucleo) > 1 and nucleo[0] + "-" in L._PREFIJOS_CAQ:
            nucleo = nucleo[1:]
            candidatos.append("-".join(nucleo))
        while len(nucleo) > 1 and "-" + nucleo[-1] in L._SUFIJOS_CAQ:
            nucleo = nucleo[:-1]
            candidatos.append("-".join(nucleo))
        if partes[0] in L._RAICES_VERB:
            candidatos.append(partes[0])
        candidatos.append(tok.split("-", 1)[1])
        candidatos.append(partes[0])
    return candidatos


def rol_en_la_familia(tok: str, raiz: str) -> str | None:
    """`suelta`, `compuesto` o None.

    Un token es de la familia de `raiz` si ES la raíz, si la lleva como uno de
    sus elementos separados por guion (que es lo que el encargo llama
    «empieza por raíz- o la lleva como segundo elemento»), o si la raíz es uno
    de los candidatos que el motor prueba al deshacer prefijos y sufijos.

    RESIDUO DECLARADO: las formas aglutinadas SIN guion no entran
    (`kali-kasibana` cuenta para `kali` y no para `kasi`, porque su segundo
    elemento es `kasibana`, no `kasi`). El motor tampoco las segmenta: es la
    misma ceguera, no una distinta.
    """
    if tok == raiz:
        return "suelta"
    if "-" in tok and raiz in tok.split("-"):
        return "compuesto"
    if raiz in _candidatos_motor(tok)[1:]:
        return "compuesto"
    return None


# ══════════════════════════════════════════════════════════════════════
# 3. LA BASE
# ══════════════════════════════════════════════════════════════════════
def psql(sql: str) -> list[list[str]]:
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d",
         "postgres", "-Atc", sql],
        capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode != 0:
        raise RuntimeError(f"psql falló: {out.stderr.strip()[:400]}")
    return [ln.split("|") for ln in out.stdout.splitlines() if ln.strip()]


def leer_runs() -> dict:
    filas = psql(
        "select id::text, substring(id::text,1,8), started_at::date::text, "
        "coalesce(total_days,0), coalesce(config->>'elenco',''), "
        "coalesce(config->>'serie',''), coalesce(config->>'continuado_desde','') "
        "from simulation_runs order by started_at, id;")
    runs = {}
    for rid, id8, fecha, dias, elenco, serie, desde in filas:
        if elenco != "era2":
            bloque = "era 1"
        elif serie == "era2-b":
            bloque = "era 2 · serie B"
        elif serie == "era2-c":
            bloque = "era 2 · serie C"
        else:
            bloque = "era 2 · serie A"
        runs[rid] = {"id8": id8, "fecha": fecha, "dias": int(dias),
                     "elenco": elenco, "serie": serie,
                     "continuado_desde": desde, "bloque": bloque}
    return runs


def verificar_serie_c_limpia(runs: dict) -> dict:
    """La serie C limpia es una CADENA de tres días, no tres runs sueltos."""
    por_id8 = {r["id8"]: (rid, r) for rid, r in runs.items()}
    faltan = [i for i in SERIE_C_LIMPIA if i not in por_id8]
    if faltan:
        raise RuntimeError(f"La serie C limpia declara runs que no están: {faltan}")
    ids = [por_id8[i][0] for i in SERIE_C_LIMPIA]
    cadena_ok = (runs[ids[0]]["continuado_desde"] == ""
                 and runs[ids[1]]["continuado_desde"] == ids[0]
                 and runs[ids[2]]["continuado_desde"] == ids[1])
    # `simulation_runs.total_days` es el contador ACUMULADO de la cadena (un
    # run es un día: 1, 2, 3), así que sumarlo daría 6 días donde hay 3. Los
    # días y los turnos se cuentan en `turns`, que es donde están.
    fila = psql(
        "select count(distinct day), count(*) from turns where run_id in ("
        + ", ".join(f"'{i}'::uuid" for i in ids) + ");")[0]
    return {"ids": ids, "id8": list(SERIE_C_LIMPIA), "cadena_ok": cadena_ok,
            "dias": int(fila[0]), "turnos": int(fila[1]),
            "serie": sorted({runs[i]["serie"] for i in ids})}


def leer_usos() -> list[tuple[str, str, int]]:
    filas = psql("select run_id::text, word, count(*) from word_uses "
                 "group by 1,2 order by 1,2;")
    return [(r, w, int(n)) for r, w, n in filas]


def control_de_raiz(tokens) -> dict:
    """El control: ¿mi reproducción de la raíz da la lengua del motor?"""
    malos = []
    for tok in tokens:
        esperado = L._familia_de_token(tok)
        mio = "caquetío"
        for c in _candidatos_motor(tok):
            if c in L.VOCABULARIO_BASE:
                mio = normalize_source_language(
                    L.VOCABULARIO_BASE[c].get("fuente", ""))
                break
        if mio != esperado:
            malos.append(tok)
    return {"tokens": len(tokens), "discrepancias": len(malos),
            "ejemplos": sorted(malos)[:10], "verde": not malos}


# ══════════════════════════════════════════════════════════════════════
# 4. LA EXPOSICIÓN
# ══════════════════════════════════════════════════════════════════════
# ── Qué cuenta como «el instrumento enseña esta forma» ───────────────────
# `curiana_lexicon.formas_en_texto()` —el criterio ANCHO con el que el motor
# construye `FORMAS_DE_PLANTILLA`— coge CUALQUIER token del texto, incluidas
# las palabras castellanas de las glosas. Para la puerta del corte de serie
# eso está bien (de más no sobra: rechazar una acuñación que ya sale escrita
# nunca es un falso negativo). Para la pregunta de ESTE issue —¿a qué forma
# empuja el prompt?— es un falso positivo enorme: `para` sale en «hilo para
# tejer», `coro` en «Coro» y `sol` en «kali (sol)».
#
# El criterio ESTRECHO cuenta la forma en POSICIÓN de voz enseñada:
#   · `kali (sol)`                         voz seguida de su glosa
#   · `katsi→cati`                         los dos lados de una correspondencia
#   · `[kali-bana: kali+-bana = …]`        el ejemplo de acuñación
# y de cada forma con guion cuentan también sus elementos (`kali-bana` enseña
# `kali`). Los dos números se dan por separado y con su nombre.
_PAL = r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9-]*"


def _con_segmentos(formas) -> set[str]:
    out = set()
    for f in formas:
        f = f.strip().lower().strip("-")
        if not f:
            continue
        out.add(f)
        if "-" in f:
            out.update(s for s in f.split("-") if s)
    return out


def _lista_de_formas(contenido: str) -> list[str]:
    """Si el interior de un paréntesis es una LISTA DE VOCES, devuélvela.

    `IDENTIDAD_LINGUISTICA` no sólo enseña con el molde `forma (glosa)`:
    también nombra formas en prosa, «¿existe en caquetío? Casi siempre SÍ
    (kati, para, kanoa, hamaka… todas tienen forma caquetía)». Eso enseña
    cuatro voces y el molde no lo ve.

    La regla, declarada: se corta el contenido en la elipsis, y sólo cuenta
    si quedan DOS O MÁS elementos separados por coma, todos de UNA palabra y
    todos claves de `VOCABULARIO_BASE`. Así entra esa lista y no entra la
    glosa «fibra de algodón, hilo para tejer» (elementos de varias palabras)
    ni «(sol)» (un solo elemento, y `sol` no es clave).
    """
    trozo = re.split(r"\.{2,}|…", contenido or "")[0]
    items = [x.strip() for x in trozo.split(",")]
    if len(items) < 2:
        return []
    if all(x and " " not in x and x.lower() in L.VOCABULARIO_BASE
           for x in items):
        return [x.lower() for x in items]
    return []


def formas_ensenadas(texto: str) -> set[str]:
    """Las formas que un texto ENSEÑA (criterio estrecho, ver arriba)."""
    t = texto or ""
    crudas = set(re.findall(rf"({_PAL})\s*\(", t))
    for a, b in re.findall(rf"({_PAL})\s*[→>]\s*({_PAL})", t):
        crudas.update((a, b))
    crudas.update(re.findall(rf"\[({_PAL})\s*:", t))
    for contenido in re.findall(r"\(([^)]*)\)", t):
        crudas.update(_lista_de_formas(contenido))
    return _con_segmentos(crudas)


def formas_ofrecidas(muestra: str) -> set[str]:
    """Las CLAVES del lexicón que el muestreador puso en el prompt.

    El bloque es `  CATEGORIA: palabra (glosa) · palabra (glosa) · …`: se
    parte por el separador y se toma lo que va ANTES del paréntesis, que es
    la clave. Así `maure (fibra de algodón, hilo para tejer)` cuenta para
    `maure` y no para `para`.
    """
    out = set()
    for linea in (muestra or "").splitlines():
        if ":" not in linea or not linea.startswith("  "):
            continue
        for item in linea.split(":", 1)[1].split("·"):
            m = re.match(rf"\s*({_PAL})\s*\(", item)
            if m:
                out.add(m.group(1).lower())
    return out


def plantillas_etiquetadas() -> list[tuple[str, str]]:
    """Las mismas plantillas que construyen `FORMAS_DE_PLANTILLA`, con nombre.

    Se llaman, no se copian: si el ejemplo de la identidad deja de ser
    `kali-bana`, esto lo ve solo.
    """
    t = [("IDENTIDAD_LINGUISTICA", L.IDENTIDAD_LINGUISTICA),
         ("prompt_reglas_completo", L.prompt_reglas_completo()),
         ("prompt_reglas_breve", L.prompt_reglas_breve())]
    # Los nombres son etiquetas YAML en lista de flujo: sin comas ni corchetes.
    for s in (1.0, 3.0, 5.0, 6.5):
        t.append((f"prompt_refuerzo_score{s}", L.prompt_refuerzo(s, [])))
    for etiqueta, esp, otro in (("fuga_esp0", 0, [""]),
                                ("fuga_esp3_con_otro", 3, [""]),
                                ("fuga_esp3_sin_otro", 3, [])):
        t.append((f"prompt_rescate_{etiqueta}",
                  L.prompt_rescate_linguistico("", 0.0, esp, otro)))
    return t


def exposicion_plantillas(formas: set[str]) -> dict:
    """Plantilla a plantilla, con los dos criterios separados."""
    res = {f: {"ensena": [], "dentro_de_compuesto": [], "solo_como_token": []}
           for f in formas}
    for nombre, texto in plantillas_etiquetadas():
        ensenadas = formas_ensenadas(texto)
        tokens = L.formas_en_texto(texto)
        compuestos = {f: sorted(x for x in ensenadas
                                if "-" in x and f in x.split("-"))
                      for f in formas}
        for f in formas:
            if f in ensenadas:
                res[f]["ensena"].append(nombre)
                if compuestos[f]:
                    res[f]["dentro_de_compuesto"].append(
                        f"{nombre}: {' '.join(compuestos[f])}")
            elif f in tokens:
                res[f]["solo_como_token"].append(nombre)
    return res


def exposicion_tu_tierra(formas: set[str]) -> dict:
    """`[Tu tierra]` para las 126 combinaciones del canon de la era 2.

    Se dan los dos criterios: cuántos bloques ENSEÑAN la forma y en cuántos
    aparece sólo como token (que en un bloque escrito en castellano es casi
    siempre la palabra castellana, no la voz).
    """
    ensena = {f: 0 for f in formas}
    token = {f: 0 for f in formas}
    n = 0
    for sitio, periodo, momento in M.combinaciones():
        bloque = M.bloque_tu_tierra(sitio, periodo, momento,
                                    agente="ensayo", dia=1)
        if not bloque:
            continue
        n += 1
        ens = formas_ensenadas(bloque)
        tok = L.formas_en_texto(bloque)
        for f in formas:
            if f in ens:
                ensena[f] += 1
            if f in tok or f in ens:
                token[f] += 1
    return {"bloques": n, "ensena": ensena, "token": token}


def cubos_del_muestreador() -> dict:
    """El cubo de cada voz y su tamaño, tal como los arma el muestreador.

    `muestra_caquetio_dinamica` agrupa por `categoria || cat` y
    `repartir_cuotas` da UNA voz a cada cubo no vacío antes de repartir el
    resto en proporción. Consecuencia medida, y no menor para la pregunta (b)
    del issue: una voz sola en su cubo sale en CASI TODOS los prompts, y una
    del cubo `sust` (226 voces) sale en uno de cada cuatro. La exposición del
    muestreo la decide el tamaño del cubo, no la capa epistémica.
    """
    perfil = P.cargar_perfil("era2")
    cubo_de, tam = {}, defaultdict(int)
    for palabra, datos in L.VOCABULARIO_BASE.items():
        if normalize_source_language(datos.get("fuente", "")) != "caquetío":
            continue
        if L.capa_epistemica(datos.get("fuente", "")) not in perfil.capas:
            continue
        if not (datos.get("sig") or datos.get("es")):
            continue
        c = datos.get("categoria") or datos.get("cat") or "otros"
        cubo_de[palabra] = c
        tam[c] += 1
    return {"cubo_de": cubo_de, "tamano": dict(tam),
            "voces_del_perfil": sum(tam.values()), "cubos": len(tam)}


def ensayo_de_muestreo(formas: set[str]) -> dict:
    """Cuántas veces sale cada forma en el MUESTREO del prompt.

    Ensayo sin API: para cada uno de los 63 agentes del elenco de la era 2,
    con su tier real y el presupuesto de voces que le manda el orquestador
    (50 / 42 / 20, `vocabulario_para_agente`), se sortean `DRAWS_POR_AGENTE`
    muestras con la `contexto` de su propio `[Tu tierra]` rotando por período
    y momento, las capas del perfil `era2` y el campo léxico vacío (`pesos`
    None: así arranca un día 1). El azar se fija con `random.seed`.

    Se miden DOS cosas distintas:
      · `muestreo`  — el bloque de vocabulario sorteado, que es lo que la
                      pregunta (b) del issue quiere cambiar.
      · `prompt`    — el bloque entero de `vocabulario_para_agente`, que
                      incluye las plantillas: ahí una forma puede salir
                      SIEMPRE sin que el muestreador la haya sorteado nunca.
    """
    perfil = P.cargar_perfil("era2")
    lexico = L.LexicoComunitario()
    combos = M.combinaciones()
    random.seed(SEMILLA_ENSAYO)
    en_muestreo = {f: 0 for f in formas}
    en_prompt = {f: 0 for f in formas}
    n = 0
    for i, (nombre, ficha) in enumerate(sorted(A.ALL_AGENTS.items())):
        try:
            tier = int(str(ficha.get("tier", "2")).strip() or 2)
        except ValueError:
            tier = 2
        sitio = ficha.get("sitio") or ficha.get("ubicacion_default") or ""
        for k in range(DRAWS_POR_AGENTE):
            _s, periodo, momento = combos[(i * DRAWS_POR_AGENTE + k) % len(combos)]
            contexto = M.bloque_tu_tierra(sitio or _s, periodo, momento,
                                          agente=nombre, dia=1 + k) or ""
            n_total = {1: 50, 2: 42}.get(tier, 20)
            muestra = L.muestra_caquetio_dinamica(
                n_por_categoria=20 if tier == 1 else 12, contexto=contexto,
                pesos=None, capas=perfil.capas, n_total=n_total)
            bloque = L.vocabulario_para_agente(
                tier, lexico, contexto=contexto, pesos=None, capas=perfil.capas)
            n += 1
            tm = formas_ofrecidas(muestra)
            tp = formas_ofrecidas(bloque) | formas_ensenadas(bloque)
            for f in formas:
                if f in tm:
                    en_muestreo[f] += 1
                if f in tp:
                    en_prompt[f] += 1
    return {"prompts": n, "semilla": SEMILLA_ENSAYO,
            "en_muestreo": en_muestreo, "en_prompt": en_prompt}


# ══════════════════════════════════════════════════════════════════════
# 5. ¿MISMA PALABRA CON OTRA GRAFÍA?
# ══════════════════════════════════════════════════════════════════════
def variante_ortografica(a: dict, b: dict) -> dict:
    """¿Las dos formas del par son la misma palabra escrita de dos maneras?

    El criterio es el ESQUELETO FONÉMICO del motor
    (`curiana_fonotactica.fonemizar`, el mismo que usa `_es_casi_autoglosa`),
    exigido IDÉNTICO — no «a una edición», como sí hace aquella función. Una
    edición no vale aquí y `kasi`/`kali` es la prueba: difieren en un solo
    carácter y son dos palabras distintas, una atestiguada y otra
    reconstruida. Se prueban los dos valores de la regla abierta `gu_es_w`
    (que este script no decide) y se comparan también las `forma_fuente`,
    que es donde vive la grafía de la fuente desde D5a.

    Las que difieren en UNA edición se listan aparte como `sospechosas`: no
    son un veredicto, son una cola de revisión.
    """
    def esqueletos(d):
        out = set()
        for v in (d["forma"], d.get("forma_fuente") or ""):
            if not v:
                continue
            for gw in (False, True):
                e = fonemizar(v, gw)
                if e:
                    out.add(e)
        return out
    ea, eb = esqueletos(a), esqueletos(b)
    iguales = sorted(ea & eb)
    casi = []
    if not iguales:
        for x in sorted(ea):
            for y in sorted(eb):
                if L._difieren_en_un_caracter(x, y):
                    casi.append(f"{x}~{y}")
    return {"misma_palabra": bool(iguales),
            "esqueleto_comun": iguales[0] if iguales else None,
            "a_una_edicion": sorted(set(casi))[:4]}


# ══════════════════════════════════════════════════════════════════════
# 6. EL CUERPO
# ══════════════════════════════════════════════════════════════════════
def mismo_esqueleto(entradas) -> list[dict]:
    """Atestiguada y derivada que son la MISMA forma con otra grafía.

    §4 del encargo, pero mirado por la FORMA y no por la glosa: dos entradas
    con el mismo esqueleto fonémico son una fusión pendiente de D5a —el lema
    fonémico— y no una decisión de canon, digan lo que digan sus glosas. Son
    las más baratas de arreglar porque no hay nada que decidir: hay que
    elegir cuál es el lema y dónde va la otra grafía (`forma_fuente`).
    """
    por_esq = defaultdict(list)
    for k, v in entradas.items():
        for gw in (False, True):
            e = fonemizar(k, gw)
            if e:
                por_esq[e].append(k)
    out, vistos = [], set()
    for esq, claves in sorted(por_esq.items()):
        claves = sorted(set(claves))
        if len(claves) < 2:
            continue
        att = [k for k in claves if CAPAS[entradas[k]["fuente"]] == "atestiguado"]
        der = [k for k in claves if CAPAS[entradas[k]["fuente"]] in DERIVADAS]
        for a in att:
            for r in der:
                if (a, r) in vistos:
                    continue
                vistos.add((a, r))
                out.append({"esqueleto": esq, "atestiguada": a, "derivada": r,
                            "capa_derivada": CAPAS[entradas[r]["fuente"]],
                            "glosa_atestiguada": " ".join(
                                str(entradas[a].get("sig") or "").split()),
                            "glosa_derivada": " ".join(
                                str(entradas[r].get("sig") or "").split())})
    return out


def candidatas_para_el_ejemplo(entradas, usos_por_token, en_pares,
                               nombres_agentes, sufijo="-bana") -> list[dict]:
    """Qué raíz podría usar el ejemplo de `IDENTIDAD_LINGUISTICA` (pregunta a).

    Hoy el ejemplo es `[kali-bana: kali+-bana = cerro del sol]` y `kali` es la
    forma RECONSTRUIDA de un par. Pase lo que pase, el ejemplo enseña algo: la
    pregunta no es si enseñar, es QUÉ. Las condiciones que se piden, todas
    verificables y verificadas aquí:

      1. la raíz es `caquetío-atestiguado` y TIENE cita (regla 8);
      2. no es homógrafa de un nombre del elenco (la trampa de las 52 voces);
      3. no es ninguna de las dos formas de un par abierto — si no, el ejemplo
         vuelve a poner el pulgar en una balanza que Miguel aún no ha pesado;
      4. el compuesto `raíz-bana` no se ha dicho NUNCA en la base, para que el
         ejemplo no bendiga una forma que ya está compitiendo;
      5. la raíz es sustantivo, como `kali`, para que el molde no cambie.

    Se ordena por uso de la raíz suelta: una raíz que el elenco ya dice es un
    ejemplo que se entiende, y `-bana` está atestiguado (Zavala #26, D9).
    """
    out = []
    for k, v in sorted(entradas.items()):
        if CAPAS[v["fuente"]] != "atestiguado":
            continue
        if not str(v.get("notas") or "").strip():
            continue
        if v.get("cat") != "sust":
            continue
        if k.lower() in nombres_agentes or k in en_pares:
            continue
        if usos_por_token.get(k + sufijo, 0):
            continue
        out.append({"raiz": k, "glosa": " ".join(str(v.get("sig") or "").split()),
                    "cita": " ".join(str(v.get("notas") or "").split())[:200],
                    "forma_fuente": v.get("forma_fuente") or "",
                    "usos_de_la_raiz": usos_por_token.get(k, 0),
                    "compuesto": k + sufijo})
    out.sort(key=lambda d: -d["usos_de_la_raiz"])
    return out


def entradas_caquetias() -> dict[str, dict]:
    """Las entradas cuyo `fuente` empieza por `caquetío-` (criterio del encargo).

    Se cuenta aparte cuántas quedan fuera por llevar `caquetío` a secas, que
    `capa_epistemica()` manda a atestiguado: si aparecieran, el par que
    formaran estaría medido sobre una capa que nadie declaró.
    """
    out, a_secas = {}, []
    for k, v in L.VOCABULARIO_BASE.items():
        f = (v.get("fuente") or "")
        if f in CAPAS:
            out[k] = v
        elif f.strip().lower() in ("caquetío", "caquetio"):
            a_secas.append(k)
    return out, a_secas


def ficha(forma: str, v: dict, nombres_agentes: frozenset,
          choques: frozenset) -> dict:
    notas = " ".join(str(v.get("notas") or "").split())
    return {
        "forma": forma,
        "capa": CAPAS[v["fuente"]],
        "fuente": v["fuente"],
        "cat": v.get("cat") or "",
        "categoria": v.get("categoria") or "",
        "glosa": " ".join(str(v.get("sig") or "").split()),
        "forma_fuente": v.get("forma_fuente") or "",
        "nucleo_fundacional": "nucleo fundacional" in norm_completa(notas),
        "deuda_d11": "DEUDA D11" in (v.get("notas") or ""),
        "sin_cita": not notas,
        "notas": notas,
        "homografa_de_agente": forma.lower() in nombres_agentes,
        "choca_con_el_canon": forma.lower() in choques,
    }


def construir_pares(entradas, nombres_agentes, choques):
    """Los tres niveles, cada uno con su criterio declarado.

    `estricto`  — la glosa normalizada COMPLETA es idéntica.
    `laxo`      — estricto, o las dos glosas comparten un sinónimo de los que
                  ellas mismas separan con coma («cerro, sitio alto» y
                  «cerro»). Incluye el caso «primer sinónimo igual». Es el
                  número que sirve para decidir.
    `contencion`— exploratorio y RUIDOSO: una glosa normalizada entera aparece
                  dentro de la otra como secuencia de palabras («grande» cae
                  dentro de «ave rapaz grande»). Se lista aparte y con el
                  aviso, porque casi todo lo que añade es un modificador
                  compartido, no un par de palabras rivales.
    """
    capa = {k: CAPAS[v["fuente"]] for k, v in entradas.items()}
    norms = {k: norm_completa(v.get("sig") or "") for k, v in entradas.items()}
    sinon = {k: sinonimos(v.get("sig") or "") for k, v in entradas.items()}
    atts = sorted(k for k, c in capa.items() if c == "atestiguado")
    ders = sorted(k for k, c in capa.items() if c in DERIVADAS)

    vistos = {}

    def anotar(nivel, glosa, criterio, a, r):
        clave = (a, r)
        if clave in vistos:
            return
        fa = ficha(a, entradas[a], nombres_agentes, choques)
        fr = ficha(r, entradas[r], nombres_agentes, choques)
        vistos[clave] = {
            "nivel": nivel,
            "glosa_normalizada": glosa,
            "criterio": criterio,
            "capa_derivada": capa[r],
            "atestiguada": fa,
            "derivada": fr,
            "grafia": variante_ortografica(fa, fr),
        }

    for a in atts:
        na, sa = norms[a], set(sinon[a])
        if not na:
            continue
        for r in ders:
            nr, sr = norms[r], set(sinon[r])
            if not nr:
                continue
            if na == nr:
                anotar("estricto", na, "estricto", a, r)
            elif sa & sr:
                comun = sorted(sa & sr, key=len, reverse=True)[0]
                crit = ("laxo:primer-sinonimo"
                        if norm_primer(entradas[a].get("sig") or "")
                        == norm_primer(entradas[r].get("sig") or "")
                        else "laxo:sinonimo-compartido")
                anotar("laxo", comun, crit, a, r)
            elif _contenida(na, nr) or _contenida(nr, na):
                anotar("contencion", na if len(na) <= len(nr) else nr,
                       "contencion:glosa-dentro-de-glosa", a, r)

    return {
        "estricto": [p for p in vistos.values() if p["nivel"] == "estricto"],
        "laxo_solo": [p for p in vistos.values() if p["nivel"] == "laxo"],
        "contencion": [p for p in vistos.values() if p["nivel"] == "contencion"],
    }


def medir_uso(pares_todos, usos, runs, serie_c, extra=()):
    """Uso por forma y por familia, por bloque y en la serie C limpia."""
    raices = sorted({p["atestiguada"]["forma"] for p in pares_todos}
                    | {p["derivada"]["forma"] for p in pares_todos}
                    | set(extra))
    vacio = lambda: {"suelta": 0, "compuestos": 0, "total": 0,          # noqa: E731
                     "formas_compuestas": defaultdict(int)}
    acum = {r: {"todo": vacio(), "bloques": defaultdict(vacio),
                "serie_c_limpia": vacio(), "runs": defaultdict(vacio)}
            for r in raices}
    tokens = sorted({w for _r, w, _n in usos})
    # Índice token → raíces (una pasada sobre los tokens distintos, no sobre
    # los 80.000 usos).
    indice = defaultdict(list)
    for tok in tokens:
        for raiz in raices:
            rol = rol_en_la_familia(tok, raiz)
            if rol:
                indice[tok].append((raiz, rol))
    ids_c = set(serie_c["ids"])
    for rid, tok, n in usos:
        if tok not in indice:
            continue
        bloque = runs.get(rid, {}).get("bloque", "¿?")
        id8 = runs.get(rid, {}).get("id8", rid[:8])
        for raiz, rol in indice[tok]:
            destinos = [acum[raiz]["todo"], acum[raiz]["bloques"][bloque],
                        acum[raiz]["runs"][id8]]
            if rid in ids_c:
                destinos.append(acum[raiz]["serie_c_limpia"])
            for d in destinos:
                d["total"] += n
                if rol == "suelta":
                    d["suelta"] += n
                else:
                    d["compuestos"] += n
                    d["formas_compuestas"][tok] += n
    return acum, tokens


def _limpiar(c):
    d = {"suelta": c["suelta"], "compuestos": c["compuestos"], "total": c["total"]}
    top = sorted(c["formas_compuestas"].items(), key=lambda kv: (-kv[1], kv[0]))
    if top:
        d["compuestas_mas_usadas"] = {k: v for k, v in top[:8]}
    return d


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaml", action="store_true",
                    help="escribe el YAML de propuesta (por defecto también)")
    ap.add_argument("--sin-base", action="store_true",
                    help="no consulta Supabase: sólo el lexicón y la exposición")
    args = ap.parse_args()

    entradas, a_secas = entradas_caquetias()
    nombres = L._nombres_de_agentes()
    choques = L._nombres_que_chocan_con_el_canon()
    pares = construir_pares(entradas, nombres, choques)
    gemelas = mismo_esqueleto(entradas)
    laxo = pares["estricto"] + pares["laxo_solo"]
    todos = laxo + pares["contencion"]

    # Los que son sólo otra grafía salen de la cola de decisión: son una
    # fusión pendiente de D5, no un veredicto de canon.
    variantes = [p for p in todos if p["grafia"]["misma_palabra"]]
    decision = [p for p in laxo if not p["grafia"]["misma_palabra"]]
    exploratorios = [p for p in pares["contencion"]
                     if not p["grafia"]["misma_palabra"]]

    formas = sorted({p["atestiguada"]["forma"] for p in todos}
                    | {p["derivada"]["forma"] for p in todos}
                    | {g[k] for g in gemelas
                       for k in ("atestiguada", "derivada")})
    exp_plant = exposicion_plantillas(set(formas))
    exp_tierra = exposicion_tu_tierra(set(formas))
    cubos = cubos_del_muestreador()
    exp_muestreo = ensayo_de_muestreo(set(formas))

    control = {}
    uso = {}
    serie_c = {}
    runs = {}
    candidatas = []
    if not args.sin_base:
        runs = leer_runs()
        serie_c = verificar_serie_c_limpia(runs)
        usos = leer_usos()
        uso, tokens = medir_uso(
            todos, usos, runs, serie_c,
            extra=[g[k] for g in gemelas for k in ("atestiguada", "derivada")])
        por_token = defaultdict(int)
        for _rid, tok, n in usos:
            por_token[tok] += n
        en_pares = ({p["atestiguada"]["forma"] for p in todos}
                    | {p["derivada"]["forma"] for p in todos})
        candidatas = candidatas_para_el_ejemplo(
            entradas, por_token, en_pares, nombres)
        control = control_de_raiz(tokens)
        control["serie_c_limpia_es_cadena"] = serie_c["cadena_ok"]
        if not control["verde"]:
            print("🔴 CONTROL EN ROJO: la raíz reproducida no coincide con el "
                  f"motor en {control['discrepancias']} tokens "
                  f"({control['ejemplos']}). Lo de abajo no mide nada.")

    # ── Informe ──────────────────────────────────────────────────────
    print("═" * 74)
    print("PARES ATESTIGUADO / DERIVADO EN EL LEXICÓN CAQUETÍO")
    print("═" * 74)
    print(f"Entradas con `fuente` que empieza por «caquetío-»: {len(entradas)}")
    capas_n = defaultdict(int)
    for v in entradas.values():
        capas_n[CAPAS[v["fuente"]]] += 1
    for c in ("atestiguado",) + DERIVADAS:
        print(f"   {c:16} {capas_n[c]}")
    print(f"Entradas con `caquetío` a secas (fuera del criterio): {len(a_secas)}")
    print()
    print(f"PARES — criterio ESTRICTO (glosa normalizada idéntica): "
          f"{len(pares['estricto'])}")
    print(f"PARES — criterio LAXO (+ sinónimo compartido): {len(laxo)}")
    for d in DERIVADAS:
        print(f"   atestiguado × {d:16} "
              f"estricto {sum(1 for p in pares['estricto'] if p['capa_derivada'] == d):3}"
              f"   laxo {sum(1 for p in laxo if p['capa_derivada'] == d):3}")
    print(f"POR CONTENCIÓN (exploratorio, ruidoso — se lista aparte): "
          f"{len(pares['contencion'])}")
    print(f"SÓLO OTRA GRAFÍA, dentro de los pares: {len(variantes)}")
    print(f"MISMO ESQUELETO FONÉMICO, buscando por la FORMA "
          f"(fusión pendiente de D5a): {len(gemelas)}")
    for g in gemelas:
        print(f"   {g['atestiguada']} / {g['derivada']} ({g['capa_derivada']}) "
              f"— {g['esqueleto']}")
    print(f"QUEDAN PARA DECIDIR (laxo menos las de grafía): {len(decision)}")
    print()

    if uso:
        print("─" * 74)
        print("LOS MÁS USADOS (uso de la forma derivada, familia entera, "
              "toda la base)")
        print("─" * 74)
        orden = sorted(decision,
                       key=lambda p: -uso[p["derivada"]["forma"]]["todo"]["total"])
        for p in orden[:12]:
            a, r = p["atestiguada"]["forma"], p["derivada"]["forma"]
            ua, ur = uso[a]["todo"], uso[r]["todo"]
            razon = (ur["total"] / ua["total"]) if ua["total"] else float("inf")
            rz = "∞" if ua["total"] == 0 else f"{razon:.1f}"
            print(f"  {p['glosa_normalizada'][:26]:26} "
                  f"{r} ({p['capa_derivada'][:5]}) {ur['total']:5}  "
                  f"vs  {a} (atest) {ua['total']:5}   ×{rz}")
        print()

    # ── ¿Quién gana, la que la plantilla enseña o la otra? ───────────
    # La pregunta de fondo del issue, contada y no afirmada: cruzar «a quién
    # enseña una plantilla estática» con «quién se dice más». No es causal
    # —nadie ha corrido el contrafactual—, es la tabla que hay.
    cruce = defaultdict(int)
    detalle = []
    if uso:
        for p in decision:
            fa, fr = p["atestiguada"]["forma"], p["derivada"]["forma"]
            ea = bool(exp_plant[fa]["ensena"])
            er = bool(exp_plant[fr]["ensena"])
            ua = uso[fa]["todo"]["total"]
            ur = uso[fr]["todo"]["total"]
            quien = ("atestiguada" if ua > ur else
                     "derivada" if ur > ua else "empate")
            estado = ("sólo la derivada" if er and not ea else
                      "sólo la atestiguada" if ea and not er else
                      "las dos" if ea and er else "ninguna")
            cruce[(estado, quien)] += 1
            detalle.append((p["glosa_normalizada"], fa, fr, estado, quien,
                            ua, ur))
        print("─" * 74)
        print("¿QUIÉN GANA? plantilla que enseña × forma más dicha "
              f"({len(decision)} pares)")
        print("─" * 74)
        for estado in ("sólo la derivada", "sólo la atestiguada",
                       "las dos", "ninguna"):
            fila = [f"{q}: {cruce[(estado, q)]}"
                    for q in ("atestiguada", "derivada", "empate")
                    if cruce[(estado, q)]]
            if fila:
                print(f"  la enseña {estado:22} → gana la "
                      + " · ".join(fila))
        print()

    # ── YAML ─────────────────────────────────────────────────────────
    doc = []
    W = doc.append
    W("# ─────────────────────────────────────────────────────────────────")
    W("# PARES ATESTIGUADO / DERIVADO — MEDICIÓN (no toca el canon, regla 5)")
    W("#")
    W("# GENERADO por 6-fusion/scripts/medir_pares_atestiguado_reconstruido.py")
    W("# No se edita a mano: se regenera. Las opciones para Miguel están en")
    W("# 6-fusion/issues-pendientes/"
      "pares-atestiguado-reconstruido-2026-09-19.md")
    W("# ─────────────────────────────────────────────────────────────────")
    W("meta:")
    W(f"  fecha: '{FECHA}'")
    W("  generado_por: 6-fusion/scripts/medir_pares_atestiguado_reconstruido.py")
    W("  elenco: era2")
    W("  perfil_de_exposicion: era2")
    W("  motivo: >-")
    W("    Miguel, 2026-09-18, de oído: «¿por qué es kali si sol es kazi?». El")
    W("    lexicón tiene dos palabras vivas para 'sol' y el elenco dice la")
    W("    reconstruida 24 a 1.")
    W("criterio_de_glosa:")
    W("  normalizacion: >-")
    W("    NFC + minúsculas; fuera lo que va entre paréntesis y corchetes;")
    W("    fuera los diacríticos (á→a, ü→u, ñ→n); fuera el artículo inicial y")
    W("    la puntuación de los extremos; espacios colapsados. NO se aplica")
    W("    ningún diccionario de sinónimos: decidir que dos glosas distintas")
    W("    significan lo mismo es una afirmación sobre el significado y la")
    W("    decide Miguel (regla 2).")
    W("  estricto: glosa normalizada COMPLETA idéntica")
    W("  laxo: >-")
    W("    estricto, o las dos glosas comparten un sinónimo de los que ellas")
    W("    mismas separan con coma o punto y coma («cerro, sitio alto» y")
    W("    «cerro»). Incluye el caso «primer sinónimo igual». Es el número")
    W("    que sirve para decidir.")
    W("  contencion: >-")
    W("    EXPLORATORIO Y RUIDOSO, listado aparte: una glosa normalizada")
    W("    entera cae dentro de la otra como secuencia de palabras. Casi todo")
    W("    lo que añade es un modificador compartido —«grande» dentro de «ave")
    W("    rapaz grande»—, no un par de palabras rivales. No se cuenta en el")
    W("    número laxo y no entra en la cola de decisión.")
    W("  familia_de_compuestos: >-")
    W("    La raíz la decide el MOTOR, no un regex de este script:")
    W("    `_candidatos_motor()` reproduce la construcción de candidatos de")
    W("    `curiana_lexicon._familia_de_token()` con sus propias tablas de")
    W("    afijos, y el control lo verifica token a token contra el motor.")
    W("    Un token es de la familia si ES la raíz, si la lleva como elemento")
    W("    separado por guion, o si la raíz es candidato tras deshacer")
    W("    prefijos y sufijos. Residuo declarado: las formas aglutinadas sin")
    W("    guion no entran (`kali-kasibana` es de `kali`, no de `kasi`).")
    W("  variante_ortografica: >-")
    W("    Esqueleto fonémico IDÉNTICO (`curiana_fonotactica.fonemizar`, con")
    W("    y sin la regla abierta gu→w, comparando también `forma_fuente`).")
    W("    Una sola edición NO basta: `kasi`/`kali` difieren en un carácter y")
    W("    son dos palabras.")
    W("censo:")
    W(f"  entradas_caquetio_con_capa: {len(entradas)}")
    for c in ("atestiguado",) + DERIVADAS:
        W(f"  {c}: {capas_n[c]}")
    W(f"  caquetio_a_secas_fuera_del_criterio: {len(a_secas)}")
    W(f"  pares_estricto: {len(pares['estricto'])}")
    W(f"  pares_laxo: {len(laxo)}")
    for d in DERIVADAS:
        W(f"  pares_estricto_con_{d}: "
          f"{sum(1 for p in pares['estricto'] if p['capa_derivada'] == d)}")
    for d in DERIVADAS:
        W(f"  pares_laxo_con_{d}: "
          f"{sum(1 for p in laxo if p['capa_derivada'] == d)}")
    W(f"  por_contencion_exploratorio: {len(pares['contencion'])}")
    W(f"  solo_otra_grafia: {len(variantes)}")
    W(f"  mismo_esqueleto_fonemico_por_la_forma: {len(gemelas)}")
    W(f"  quedan_para_decidir: {len(decision)}")
    if control:
        W("control:")
        W(f"  tokens_de_la_base: {control['tokens']}")
        W(f"  discrepancias_con_familia_de_token: {control['discrepancias']}")
        W(f"  verde: {str(control['verde']).lower()}")
        W(f"  serie_c_limpia_es_cadena: {str(serie_c['cadena_ok']).lower()}")
        W(f"  serie_c_limpia_runs: {', '.join(serie_c['id8'])}")
        W(f"  serie_c_limpia_dias: {serie_c['dias']}")
        W(f"  serie_c_limpia_turnos: {serie_c['turnos']}")
    W("exposicion_global:")
    W(f"  prompts_del_ensayo_de_muestreo: {exp_muestreo['prompts']}")
    W(f"  semilla: {exp_muestreo['semilla']}")
    W(f"  bloques_tu_tierra: {exp_tierra['bloques']}")
    W("  # A cuánta gente llega cada plantilla, por tier del elenco activo.")
    W("  # `IDENTIDAD_LINGUISTICA` no depende del tier: el orquestador la")
    W("  # mete en el system prompt de TODOS, cada turno.")
    W(f"  agentes_del_elenco: {len(A.ALL_AGENTS)}")
    W(f"  identidad_linguistica_llega_a: {len(A.ALL_AGENTS)}")
    W(f"  prompt_reglas_completo_llega_a: {len(A.AGENTS_T1)}  # tier 1")
    W(f"  prompt_reglas_breve_llega_a: "
      f"{len(A.AGENTS_T2) + len(A.AGENTS_T3)}  # tiers 2 y 3")
    W("  # El muestreo reparte UNA voz por cubo antes que nada: la exposición")
    W("  # la decide el tamaño del cubo, no la capa. `para` está sola en")
    W("  # `geografia` y sale en todos los prompts; `kasi` comparte `sust`")
    W("  # con otras 225 y sale en uno de cada cinco.")
    W(f"  voces_caquetias_del_perfil_era2: {cubos['voces_del_perfil']}")
    W(f"  cubos_del_muestreador: {cubos['cubos']}")
    W(f"  cubo_mas_grande: {max(cubos['tamano'].values())}")
    W(f"  cubos_de_una_sola_voz: "
      f"{sum(1 for n in cubos['tamano'].values() if n == 1)}")
    if cruce:
        W("quien_gana:")
        W("  # Cruce de «a quién enseña una plantilla estática» con «quién se")
        W("  # dice más» en toda la base, sobre los pares de decisión. NO es")
        W("  # causal: nadie ha corrido el contrafactual. Es la tabla que hay.")
        for estado in ("sólo la derivada", "sólo la atestiguada",
                       "las dos", "ninguna"):
            for q in ("atestiguada", "derivada", "empate"):
                if cruce[(estado, q)]:
                    W(f"  \"la enseña {estado} → gana la {q}\": "
                      f"{cruce[(estado, q)]}")
        W("  detalle:")
        for glosa, fa, fr, estado, quien, ua, ur in detalle:
            W(f"    - {{glosa: \"{glosa}\", atestiguada: {fa}, derivada: {fr}, "
              f"la_enseña: \"{estado}\", gana: {quien}, "
              f"uso: \"{ua}:{ur}\"}}")

    def bloque_par(p, indent="  "):
        o = []
        a, r = p["atestiguada"], p["derivada"]
        o.append(f"{indent}- glosa: \"{p['glosa_normalizada']}\"")
        o.append(f"{indent}  criterio: {p['criterio']}")
        o.append(f"{indent}  capa_derivada: {p['capa_derivada']}")
        o.append(f"{indent}  solo_otra_grafia: "
                 f"{str(p['grafia']['misma_palabra']).lower()}")
        if p["grafia"]["esqueleto_comun"]:
            o.append(f"{indent}  esqueleto_comun: {p['grafia']['esqueleto_comun']}")
        if p["grafia"]["a_una_edicion"]:
            o.append(f"{indent}  a_una_edicion: "
                     f"[{', '.join(p['grafia']['a_una_edicion'])}]")
        for rol, d in (("atestiguada", a), ("derivada", r)):
            o.append(f"{indent}  {rol}:")
            o.append(f"{indent}    forma: {d['forma']}")
            o.append(f"{indent}    fuente: {d['fuente']}")
            o.append(f"{indent}    cat: {d['cat'] or '~'}")
            o.append(f"{indent}    glosa: {json.dumps(d['glosa'], ensure_ascii=False)}")
            if d["forma_fuente"]:
                o.append(f"{indent}    forma_fuente: {d['forma_fuente']}")
            o.append(f"{indent}    nucleo_fundacional: "
                     f"{str(d['nucleo_fundacional']).lower()}")
            if d["deuda_d11"]:
                o.append(f"{indent}    deuda_d11: true")
            if d["sin_cita"]:
                o.append(f"{indent}    sin_cita: true")
            o.append(f"{indent}    homografa_de_agente: "
                     f"{str(d['homografa_de_agente']).lower()}")
            cita = d["notas"][:420] + ("…" if len(d["notas"]) > 420 else "")
            o.append(f"{indent}    notas: {json.dumps(cita, ensure_ascii=False)}")
            ep = exp_plant[d["forma"]]
            f_ = d["forma"]
            o.append(f"{indent}    exposicion:")
            o.append(f"{indent}      forma_de_plantilla: "
                     f"{str(L.es_forma_de_plantilla(f_)).lower()}"
                     "   # toda clave del lexicón lo es: la puerta del corte"
                     " incluye VOCABULARIO_BASE entero")
            o.append(f"{indent}      plantillas_que_la_enseñan: "
                     f"[{', '.join(ep['ensena'])}]")
            if ep["dentro_de_compuesto"]:
                o.append(f"{indent}      la_enseñan_dentro_de_un_compuesto:")
                for x in ep["dentro_de_compuesto"]:
                    o.append(f"{indent}        - {json.dumps(x, ensure_ascii=False)}")
            if ep["solo_como_token"]:
                o.append(f"{indent}      aparece_solo_como_token: "
                         f"[{', '.join(ep['solo_como_token'])}]"
                         "   # criterio ancho: casi siempre la palabra"
                         " castellana de una glosa")
            o.append(f"{indent}      tu_tierra_la_enseña: "
                     f"{exp_tierra['ensena'][f_]}/{exp_tierra['bloques']}")
            o.append(f"{indent}      tu_tierra_como_token: "
                     f"{exp_tierra['token'][f_]}/{exp_tierra['bloques']}")
            o.append(f"{indent}      en_el_muestreo: "
                     f"{exp_muestreo['en_muestreo'][f_]}/"
                     f"{exp_muestreo['prompts']}")
            o.append(f"{indent}      en_el_prompt_entero: "
                     f"{exp_muestreo['en_prompt'][f_]}/"
                     f"{exp_muestreo['prompts']}")
            cb = cubos["cubo_de"].get(f_)
            if cb:
                o.append(f"{indent}      cubo_del_muestreador: "
                         f"{cb} ({cubos['tamano'][cb]} voces)")
            else:
                o.append(f"{indent}      cubo_del_muestreador: "
                         "~   # fuera del perfil era2: no se le enseña nunca")
            if uso:
                u = uso[d["forma"]]
                t = _limpiar(u["todo"])
                o.append(f"{indent}    uso:")
                o.append(f"{indent}      toda_la_base: "
                         f"{{suelta: {t['suelta']}, compuestos: {t['compuestos']}, "
                         f"total: {t['total']}}}")
                sc = _limpiar(u["serie_c_limpia"])
                o.append(f"{indent}      serie_c_limpia: "
                         f"{{suelta: {sc['suelta']}, compuestos: {sc['compuestos']}, "
                         f"total: {sc['total']}}}")
                if sc.get("compuestas_mas_usadas"):
                    o.append(f"{indent}      compuestas_en_la_serie_c_limpia:")
                    for k, v in sc["compuestas_mas_usadas"].items():
                        o.append(f"{indent}        {k}: {v}")
                if u["bloques"]:
                    o.append(f"{indent}      por_bloque:")
                    for b in sorted(u["bloques"]):
                        bb = _limpiar(u["bloques"][b])
                        o.append(f"{indent}        \"{b}\": "
                                 f"{{suelta: {bb['suelta']}, "
                                 f"compuestos: {bb['compuestos']}, "
                                 f"total: {bb['total']}}}")
                if t.get("compuestas_mas_usadas"):
                    o.append(f"{indent}      compuestas_mas_usadas:")
                    for k, v in t["compuestas_mas_usadas"].items():
                        o.append(f"{indent}        {k}: {v}")
        if uso:
            ua = uso[a["forma"]]["todo"]["total"]
            ur = uso[r["forma"]]["todo"]["total"]
            o.append(f"{indent}  razon_derivada_sobre_atestiguada: "
                     f"{'null' if ua == 0 else round(ur / ua, 2)}")
        return o

    if uso:
        orden = sorted(decision,
                       key=lambda p: (-uso[p["derivada"]["forma"]]["todo"]["total"],
                                      p["glosa_normalizada"]))
    else:
        orden = sorted(decision, key=lambda p: p["glosa_normalizada"])

    W("")
    W("# ── Los pares que son una DECISIÓN de canon "
      "(ordenados por uso de la derivada) ──")
    W("pares:")
    for p in orden:
        doc.extend(bloque_par(p))

    W("")
    W("# ── Los pares que son SÓLO OTRA GRAFÍA: fusión pendiente de D5, ──")
    W("# ── no decisión de canon. Son los más baratos de arreglar.      ──")
    W("variantes_ortograficas:")
    if variantes:
        for p in sorted(variantes, key=lambda p: p["glosa_normalizada"]):
            doc.extend(bloque_par(p))
    else:
        W("  []   # ninguna: D5a ya fusionó las que había (cazi→kasi, cati→kati)")

    W("")
    W("# ── Pregunta (a) del issue: si el ejemplo de IDENTIDAD_LINGUISTICA ──")
    W("# ── deja de ser `kali-bana`, ¿con qué raíz? Condiciones en el      ──")
    W("# ── docstring de candidatas_para_el_ejemplo(); las 12 primeras.    ──")
    W("candidatas_para_el_ejemplo_de_la_plantilla:")
    if candidatas:
        for c in candidatas[:12]:
            W(f"  - raiz: {c['raiz']}")
            W(f"    compuesto: {c['compuesto']}")
            W(f"    glosa: {json.dumps(c['glosa'], ensure_ascii=False)}")
            if c["forma_fuente"]:
                W(f"    forma_fuente: {c['forma_fuente']}")
            W(f"    usos_de_la_raiz_en_la_base: {c['usos_de_la_raiz']}")
            W(f"    cita: {json.dumps(c['cita'], ensure_ascii=False)}")
        W(f"  # candidatas que cumplen las cinco condiciones: {len(candidatas)}")
    else:
        W("  []")

    W("")
    W("# ── La misma búsqueda por la FORMA y no por la glosa: entradas    ──")
    W("# ── atestiguada y derivada con el MISMO esqueleto fonémico.      ──")
    W("# ──                                                              ──")
    W("# ── ⚠ CANDIDATAS, NO VEREDICTOS. El esqueleto sólo dice que las  ──")
    W("# ── dos se escriben igual una vez quitada la grafía colonial; si ──")
    W("# ── son la misma PALABRA lo dicen las glosas, que van al lado.   ──")
    W("# ── Un esqueleto compartido puede ser también una COLISIÓN de    ──")
    W("# ── homógrafos, y ésa es de por sí un dato del instrumento.      ──")
    W("mismo_esqueleto_fonemico:")
    if gemelas:
        for g in gemelas:
            W(f"  - esqueleto: {g['esqueleto']}")
            W(f"    atestiguada: {g['atestiguada']}")
            W(f"    glosa_atestiguada: "
              f"{json.dumps(g['glosa_atestiguada'], ensure_ascii=False)}")
            W(f"    derivada: {g['derivada']}")
            W(f"    capa_derivada: {g['capa_derivada']}")
            W(f"    glosa_derivada: "
              f"{json.dumps(g['glosa_derivada'][:180], ensure_ascii=False)}")
            if uso and g["atestiguada"] in uso and g["derivada"] in uso:
                W(f"    uso_total: {{atestiguada: "
                  f"{uso[g['atestiguada']]['todo']['total']}, derivada: "
                  f"{uso[g['derivada']]['todo']['total']}}}")
            for rol, f_ in (("atestiguada", g["atestiguada"]),
                            ("derivada", g["derivada"])):
                ep = exp_plant.get(f_, {})
                W(f"    plantillas_que_enseñan_la_{rol}: "
                  f"[{', '.join(ep.get('ensena', []))}]")
    else:
        W("  []")

    W("")
    W("# ── EXPLORATORIO. Una glosa cae DENTRO de la otra. Ruidoso por    ──")
    W("# ── construcción: casi todo es un modificador compartido, no un   ──")
    W("# ── par rival. No se cuenta en el número laxo ni se decide aquí.  ──")
    W("por_contencion_exploratorio:")
    if exploratorios:
        if uso:
            expl = sorted(exploratorios,
                          key=lambda p: (-uso[p["derivada"]["forma"]]["todo"]["total"],
                                         p["glosa_normalizada"]))
        else:
            expl = sorted(exploratorios, key=lambda p: p["glosa_normalizada"])
        for p in expl:
            a, r = p["atestiguada"], p["derivada"]
            W(f"  - glosa_contenida: \"{p['glosa_normalizada']}\"")
            W(f"    atestiguada: {a['forma']}  "
              f"# {json.dumps(a['glosa'], ensure_ascii=False)}")
            W(f"    derivada: {r['forma']} ({p['capa_derivada']})  "
              f"# {json.dumps(r['glosa'], ensure_ascii=False)}")
            if uso:
                W(f"    uso_total: {{atestiguada: "
                  f"{uso[a['forma']]['todo']['total']}, derivada: "
                  f"{uso[r['forma']]['todo']['total']}}}")
    else:
        W("  []")

    if args.sin_base:
        # Sin base el documento saldría a medias —sin uso, sin control, sin
        # candidatas— y pisaría el bueno. `--sin-base` es para mirar el
        # lexicón y la exposición, no para publicar.
        print(f"⚠ --sin-base: NO se escribe {os.path.relpath(SALIDA, RAIZ)} "
              f"(saldría a medias). Serían {len(doc)} líneas.")
        return
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(doc) + "\n")
    print(f"✓ escrito {os.path.relpath(SALIDA, RAIZ)}  ({len(doc)} líneas)")
    if control:
        print(f"✓ control de raíz: {control['discrepancias']} discrepancias "
              f"en {control['tokens']} tokens · serie C limpia es cadena: "
              f"{serie_c['cadena_ok']}")


if __name__ == "__main__":
    main()
