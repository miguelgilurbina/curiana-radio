#!/usr/bin/env python3
"""LA MORFOLOGÍA, AUDITADA: qué morfemas hay, quién los declara, quién los enseña
y qué hace la gente con ellos.

Encargo de Miguel, 2026-09-20: «echarle una revisada a toda la morfología
arahuaca, para que ajustemos; quiero que tengamos la morfología bien clara».

POR QUÉ. En una sola sesión la morfología apareció tres veces como fuente de
error, y siempre por lo mismo: **algo que el motor enseña sin que nadie lo haya
decidido**.

  1. El ejemplo `kali-bana` de `IDENTIDAD_LINGUISTICA` empujaba una forma
     reconstruida, y el molde `X-bana` se dijo 233 veces sin que ninguna
     plantilla lo enseñara (corte del 2026-09-19).
  2. Una heurística de una línea puso `cat: v_raiz` a 49 de las 144 entradas de
     Zavala, y `score_linguistico()` cuenta como arahuaco todo token cuyo primer
     segmento sea raíz verbal.
  3. Los agentes tienen el mecanismo arahuaco bueno para predicar un nombre
     —`ka-` atributivo, `ma-` privativo— y con el viento usaron la vía mala.

Este script MIDE. No decide nada y no toca el canon ni el motor (regla 5): su
salida es un YAML en `6-fusion/` y las decisiones van al issue que lo cita.

QUÉ MIDE, en cuatro partes:

  1. EL INVENTARIO. Todo morfema que el proyecto usa, de donde esté:
     `curiana_lexicon` (las siete tablas de reglas), `2-lengua/morfemas.yaml`,
     las cinco plantillas estáticas del prompt, los módulos de propuesta
     (`lexicon_van_buurt`, `lexicon_gatschet`, `lexicon_toponimos`) y lo que el
     motor reconoce al puntuar (`_PREFIJOS_CAQ`, `_SUFIJOS_CAQ`,
     `_AFIJOS_SUELTOS`, `_RAICES_VERB`, `_aspectos_morfologicos`).

     Para cada uno: forma, función declarada, capa epistémica, apoyo con cita
     —validada como **clave foránea** contra `4-fuentes/bibliografia.yaml`
     (regla 8); lo que no case se declara `deuda: sin-procedencia`—, dónde está
     escrito y dónde lo enseña el motor.

     Y las TRES PATOLOGÍAS:
       (a) el motor lo ENSEÑA y el canon no lo declara;
       (b) el canon lo declara y el motor NO lo reconoce al puntuar;
       (c) su único apoyo es el andamio wayuu/lokono que D11 mandó retirar.

  2. QUÉ HACE LA GENTE. Sobre `word_uses` de TODA la base, por era y serie:
     uso de cada morfema, cuántas raíces distintas admite, cuáles no usa nadie,
     y **qué combinaciones producen los agentes que el sistema no declara**.

     ⚠️ LA SEGMENTACIÓN ES LA DEL MOTOR, NO UN REGEX DE AQUÍ. Se pela por los
     bordes con las tablas del propio módulo (`_PREFIJOS_CAQ` / `_SUFIJOS_CAQ`)
     y en el mismo orden que `nucleo_de_token()` —prefijos primero, sufijos
     después—, y hay un CONTROL que compara núcleo a núcleo contra
     `L.nucleo_de_token()` sobre las 2.512 formas de la base: si no coinciden
     todas, el script se planta. Lo único que añade la versión de aquí es la
     LISTA de afijos pelados, que el motor descarta.

     Qué cuenta como combinación NO DECLARADA: el campo `uso` de cada regla
     declara UN slot y UN afijo (`VERBO_RAIZ + -ka`, `ta- + SUSTANTIVO`,
     `RAÍZ + -bana`). Ninguna regla del proyecto declara apilamiento. Así que:
       · un afijo sobre una raíz de la categoría equivocada (aspecto sobre
         sustantivo, posesivo sobre verbo) es violación de SLOT, y el slot se
         lee del campo `uso`, no se inventa aquí;
       · dos o más afijos en la misma forma es una combinación que NINGUNA
         regla declara, y se cuenta por patrón de clases.

  3. EL ASPECTO, RAMA A RAMA. `_aspectos_morfologicos()` vale hasta 2 de los 10
     puntos del score (20 %) y acepta `-ka/-ni/-da` sobre cualquier raíz con
     guion de tres o más letras. Se re-ejecuta instrumentado sobre las 3.379
     respuestas de la base para decir por qué rama entró cada aspecto: raíz
     verbal caquetía, raíz verbal de la comparanda, o el comodín de longitud.
     CONTROL: la lista instrumentada tiene que ser idéntica a la que devuelve
     `L._aspectos_morfologicos()` con el lexicón de hoy.

  4. EL CONTRASTE ARAHUACO. Qué rasgo de los que la comparanda del repo
     documenta con cita tiene o no tiene el sistema, comprobado contra el
     canon con una búsqueda declarada (regla 6: un cero se verifica, y aquí se
     dice qué se buscó).

Uso:
    CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 \
        python 6-fusion/scripts/auditar_morfologia.py
    python 6-fusion/scripts/auditar_morfologia.py --sin-base   # sólo 1 y 4

REGLAS DURAS que respeta: no abre `curiana_sim/.env` (stub de `dotenv` antes de
importar el motor), no llama a la API, no escribe en la base (la lee por
`docker exec … psql`), no toca `curiana_lexicon.py` ni `lexicon_zavala.py` ni
`minar_zavala_glosario.py` ni la `cat` de ninguna entrada.
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import os
import re
import subprocess
import sys
import types
import unicodedata

# ── El motor, sin abrir .env ──────────────────────────────────────────────
if "dotenv" not in sys.modules:
    _stub = types.ModuleType("dotenv")
    _stub.load_dotenv = lambda *a, **k: None                  # noqa: E731
    _stub.dotenv_values = lambda *a, **k: {}                  # noqa: E731
    sys.modules["dotenv"] = _stub

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SIM = os.path.join(RAIZ, "curiana_sim")
os.environ.setdefault("CURIANA_ELENCO", "era2")

FECHA = "2026-09-20"
SALIDA = os.path.join(RAIZ, "6-fusion", f"medicion_morfologia_{FECHA}.yaml")
CONTENEDOR = "supabase_db_curiana_sim"
SEPARADOR = "\x1f"
FIN_DE_FILA = "\x1e"


def _forzar_utf8():
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:                                     # noqa: BLE001
            pass


# ══════════════════════════════════════════════════════════════════════
# LA BIBLIOGRAFÍA — citar es una clave foránea (regla 8)
# ══════════════════════════════════════════════════════════════════════
def claves_de_bibliografia() -> dict[str, str]:
    """Cada clave y cada alias de `4-fuentes/bibliografia.yaml`, en minúscula,
    apuntando a la clave canónica. Es contra esto que se valida un apoyo."""
    ruta = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")
    texto = io.open(ruta, encoding="utf-8").read()
    try:
        import yaml
        obras = yaml.safe_load(texto)["obras"]
    except Exception:                                         # noqa: BLE001
        return {}
    mapa: dict[str, str] = {}
    for o in obras:
        clave = o.get("id") or o.get("clave") or ""
        if not clave:
            continue
        mapa[clave.lower()] = clave
        for a in (o.get("aliases") or []):
            mapa[str(a).lower()] = clave
        # El apellido + año, que es como se cita en prosa dentro del motor
        autor = str(o.get("autor") or "")
        apellido = autor.split(",")[0].strip().lower()
        anio = re.search(r"\d{4}", str(o.get("anio") or ""))
        if apellido and anio:
            mapa[f"{apellido} {anio.group()}"] = clave
    return mapa


def _sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn")


def resolver_cita(texto: str, mapa: dict[str, str]) -> list[str]:
    """Qué obras de la bibliografía nombra este apoyo. Lista vacía = deuda."""
    if not texto:
        return []
    plano = _sin_tildes(texto)
    hallados = []
    for alias, clave in mapa.items():
        a = _sin_tildes(alias)
        if len(a) < 5:
            continue
        if a in plano and clave not in hallados:
            hallados.append(clave)
    return sorted(hallados)


# ══════════════════════════════════════════════════════════════════════
# LA BASE (sólo lectura, por docker exec)
# ══════════════════════════════════════════════════════════════════════
def psql(sql: str) -> list[list[str]]:
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d",
         "postgres", "-Atc", sql],
        capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise RuntimeError(f"psql falló: {out.stderr.strip()[:400]}")
    return [ln.split("|") for ln in out.stdout.splitlines() if ln.strip()]


def usos_por_forma() -> list[dict]:
    """`word_uses` entero, agrupado por forma, lengua, era y serie."""
    filas = psql(
        "select w.word, coalesce(w.source_language,''), "
        "coalesce(s.config->>'elenco','era1'), "
        "coalesce(s.config->>'serie','-'), count(*) "
        "from word_uses w join simulation_runs s on s.id = w.run_id "
        "group by 1,2,3,4;")
    return [{"forma": f[0], "lengua": f[1], "era": f[2], "serie": f[3],
             "usos": int(f[4])} for f in filas if f[0]]


def respuestas() -> list[dict]:
    """Las respuestas de toda la base, con lo que el motor guardó de aspecto."""
    sql = (
        "select coalesce(s.config->>'elenco','era1') || '{S}' || "
        "coalesce(s.config->>'serie','-') || '{S}' || "
        "substring(r.run_id::text,1,8) || '{S}' || r.agent_name || '{S}' || "
        "coalesce(array_to_string(r.aspects_used,','),'') || '{S}' || "
        "r.response_text || '{F}' "
        "from agent_responses r join simulation_runs s on s.id = r.run_id"
    ).format(S=SEPARADOR, F=FIN_DE_FILA)
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d",
         "postgres", "-Atc", sql], capture_output=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.decode("utf-8", "replace")[:400])
    filas = []
    for bloque in out.stdout.decode("utf-8").split(FIN_DE_FILA):
        if not bloque.strip("\n"):
            continue
        p = bloque.lstrip("\n").split(SEPARADOR)
        if len(p) < 6:
            continue
        filas.append({"era": p[0], "serie": p[1], "run": p[2], "agente": p[3],
                      "aspectos_guardados": [a for a in p[4].split(",") if a],
                      "texto": p[5]})
    return filas


# ══════════════════════════════════════════════════════════════════════
# LA SEGMENTACIÓN — la del motor, instrumentada
# ══════════════════════════════════════════════════════════════════════
class Segmentador:
    """Pela por los bordes con las tablas del propio `curiana_lexicon`.

    Es `nucleo_de_token()` con la lista de afijos pelados apuntada. El orden
    es el suyo —prefijos primero, sufijos después, y siempre dejando al menos
    un segmento— y `control()` lo comprueba forma a forma contra el motor.
    """

    def __init__(self, L):
        self.L = L
        self.prefijos = frozenset(L._PREFIJOS_CAQ)
        self.sufijos = frozenset(L._SUFIJOS_CAQ)

    def __call__(self, tok: str) -> tuple[list[str], list[str], list[str]]:
        partes = (tok or "").strip().lower().split("-")
        pref: list[str] = []
        suf: list[str] = []
        while len(partes) > 1 and partes[0] + "-" in self.prefijos:
            pref.append(partes[0] + "-")
            partes = partes[1:]
        while len(partes) > 1 and "-" + partes[-1] in self.sufijos:
            suf.insert(0, "-" + partes[-1])
            partes = partes[:-1]
        return pref, partes, suf

    def control(self, formas) -> tuple[int, list[str]]:
        """El núcleo de aquí tiene que ser el núcleo del motor. Siempre."""
        desvios = []
        for f in formas:
            _, nucleo, _ = self(f)
            if nucleo != self.L.nucleo_de_token(f):
                desvios.append(f)
        return len(desvios), desvios[:20]


# ══════════════════════════════════════════════════════════════════════
# EL INVENTARIO
# ══════════════════════════════════════════════════════════════════════
# De qué tabla sale cada morfema y qué CLASE gramatical declara el proyecto.
# Las clases son las de los propios nombres de las tablas de `curiana_lexicon`;
# no se inventa ninguna aquí.
TABLAS = [
    ("REGLAS_ASPECTO",     "aspecto",    "curiana_sim/curiana_lexicon.py"),
    ("REGLAS_LOCATIVAS",   "locativo",   "curiana_sim/curiana_lexicon.py"),
    ("REGLAS_POSESIVAS",   "posesivo",   "curiana_sim/curiana_lexicon.py"),
    ("REGLAS_NUMERO",      "número",     "curiana_sim/curiana_lexicon.py"),
    ("REGLAS_ZAVALA",      "derivativo", "curiana_sim/curiana_lexicon.py"),
    ("REGLAS_TOPONIMICAS", "toponímico", "curiana_sim/curiana_lexicon.py"),
    ("REGLAS_RETIRADAS",   "agentivo",   "curiana_sim/curiana_lexicon.py"),
]

# El slot que cada regla DECLARA en su campo `uso`. Se lee del texto, no se
# decide aquí: «VERBO_RAIZ + -ka» exige verbo, «ta- + SUSTANTIVO» exige
# sustantivo, «RAÍZ + -bana» no exige categoría.
def slot_declarado(uso: str) -> str:
    u = _sin_tildes(uso or "")
    if "verbo_raiz" in u or "verbo raiz" in u:
        return "v_raiz"
    if "sustantivo" in u:
        return "sust"
    if "gentilicio" in u:
        return "gentilicio"
    if "raiz" in u:
        return "cualquiera"
    return "sin-declarar"


def capa_de_regla(regla: dict) -> str:
    """La capa epistémica que la propia entrada declara.

    `atestiguado` con cita → atestiguado. Campo `wayunaiki` y nada más →
    reconstruido-desde-el-andamio (la deuda de D11). `evidencia` que dice
    CANON-SIMULACIÓN → canon-simulación. Lo demás, reconstruido.
    """
    if regla.get("retirada"):
        return "retirada"
    if regla.get("atestiguado"):
        return "atestiguado"
    ev = regla.get("evidencia") or ""
    if "CANON-SIMULACI" in ev.upper():
        return "canon-simulación"
    if ev:
        return "atestiguado" if "Zavala" in ev or "#" in ev else "reconstruido"
    if regla.get("wayunaiki"):
        return "reconstruido-andamio-d11"
    return "sin-declarar"


def apoyo_de_regla(regla: dict) -> str:
    return (regla.get("atestiguado") or regla.get("evidencia")
            or regla.get("wayunaiki") or "")


def morfemas_del_motor(L) -> dict[str, dict]:
    salida: dict[str, dict] = {}
    for nombre, clase, fichero in TABLAS:
        tabla = getattr(L, nombre, {}) or {}
        for afijo, regla in tabla.items():
            salida[afijo] = {
                "forma": afijo,
                "clase": clase,
                "tabla": nombre,
                "fichero": fichero,
                "funcion_declarada": regla.get("nombre", ""),
                "uso_declarado": regla.get("uso", ""),
                "slot_declarado": slot_declarado(regla.get("uso", "")),
                "capa": capa_de_regla(regla),
                "apoyo": apoyo_de_regla(regla),
                "en_TODAS_LAS_REGLAS": afijo in L.TODAS_LAS_REGLAS,
                "solo_wayunaiki": bool(regla.get("wayunaiki")
                                       and not regla.get("atestiguado")
                                       and not regla.get("evidencia")),
            }
    return salida


def morfemas_del_yaml() -> dict[str, dict]:
    """`2-lengua/morfemas.yaml`: el canon de datos de lengua (generado desde
    `lexicon_toponimos.py` por `migrar_toponimos.py`; no se edita a mano)."""
    ruta = os.path.join(RAIZ, "2-lengua", "morfemas.yaml")
    try:
        import yaml
        d = yaml.safe_load(io.open(ruta, encoding="utf-8").read())
    except Exception:                                         # noqa: BLE001
        return {}
    salida = {}
    for m in (d.get("morfemas") or []):
        apoyos = m.get("apoyo_externo") or []
        salida[m["forma"]] = {
            "forma": m["forma"],
            "id": m.get("id"),
            "glosado": bool(m.get("glosado")),
            "glosa": m.get("glosa_inferida", ""),
            "estatus": m.get("estatus", ""),
            "recurrencia": m.get("recurrencia") or m.get("apariciones") or 0,
            "apoyo": " · ".join(str(a) for a in apoyos) or (m.get("nota") or ""),
            "conflicto": m.get("conflicto", ""),
        }
    return salida


def morfemas_propuestos(L) -> dict[str, dict]:
    """Los módulos que `curiana_lexicon.py` NO importa: propuestas, no habla."""
    salida: dict[str, dict] = {}
    try:
        sys.path.insert(0, SIM)
        import lexicon_van_buurt as VB
        for forma, d in (getattr(VB, "MORFEMAS_VAN_BUURT", {}) or {}).items():
            salida[forma] = {"forma": forma, "modulo": "lexicon_van_buurt.py",
                             "glosa": d.get("glosa", ""),
                             "apoyo": d.get("autoridad", ""),
                             "nota": d.get("nota") or ""}
    except Exception as e:                                    # noqa: BLE001
        salida["__error_van_buurt"] = {"forma": "", "error": str(e)}
    try:
        import lexicon_gatschet as GA
        for afijo, toponimos in (getattr(GA, "AFIJOS_EN_TOPONIMOS", {}) or {}).items():
            salida.setdefault(afijo, {"forma": afijo})
            salida[afijo]["control_gatschet"] = list(toponimos)
    except Exception:                                         # noqa: BLE001
        pass
    return salida


# ── Lo que el motor ENSEÑA: se lee de las plantillas, no se copia ─────────
def donde_lo_ensena(L, afijo: str) -> list[str]:
    """En qué plantilla estática aparece literalmente este afijo.

    Se construyen llamando a las plantillas, igual que `FORMAS_DE_PLANTILLA`:
    si mañana cambia el texto, esta lista cambia sola.
    """
    plantillas = {
        "IDENTIDAD_LINGUISTICA": L.IDENTIDAD_LINGUISTICA,
        "prompt_reglas_completo": L.prompt_reglas_completo(),
        "prompt_reglas_breve": L.prompt_reglas_breve(),
        "prompt_refuerzo": "\n".join(L.prompt_refuerzo(s, [])
                                     for s in (1.0, 3.0, 5.0, 6.5)),
        "prompt_rescate_linguistico": "\n".join(
            L.prompt_rescate_linguistico("", 0.0, esp, otro)
            for esp, otro in ((0, [""]), (3, [""]), (3, []))),
    }
    a = afijo.strip("-").lower()
    if afijo.startswith("-"):
        patron = re.compile(r"[-\s]" + re.escape(a) + r"\b")
    else:
        patron = re.compile(r"\b" + re.escape(a) + r"-")
    return [nombre for nombre, texto in plantillas.items()
            if patron.search(texto.lower())]


def donde_lo_reconoce(L, afijo: str) -> list[str]:
    """Por qué puertas del SCORER pasa este afijo."""
    puertas = []
    if afijo in L._PREFIJOS_CAQ:
        puertas.append("_PREFIJOS_CAQ (desafijado de _familia_de_token / nucleo_de_token)")
    if afijo in L._SUFIJOS_CAQ:
        puertas.append("_SUFIJOS_CAQ (desafijado de _familia_de_token / nucleo_de_token)")
    if afijo.strip("-").lower() in L._AFIJOS_SUELTOS:
        puertas.append("_AFIJOS_SUELTOS (suelto cuenta como palabra caquetía)")
    if afijo in getattr(L, "REGLAS_ASPECTO", {}):
        puertas.append("_aspectos_morfologicos (hasta 2 de los 10 puntos del score)")
    if afijo.strip("-") in ("ta", "wa", "ma", "ka") and afijo.endswith("-"):
        puertas.append("score_linguistico.es_arahuaco (prefijo + raíz activa)")
    return puertas


# ══════════════════════════════════════════════════════════════════════
# EL ASPECTO, RAMA A RAMA
# ══════════════════════════════════════════════════════════════════════
MAPA_ASPECTO = {"ka": "completivo", "ni": "continuativo", "da": "prospectivo"}


def aspectos_instrumentado(L, tokens: list) -> tuple[list, list]:
    """`_aspectos_morfologicos()` con la rama apuntada.

    Copia literal de la función del motor (líneas 8111-8128 de
    `curiana_lexicon.py`) con un registro añadido. El CONTROL de abajo compara
    la lista de aspectos con la que devuelve el motor de verdad.
    """
    encontrados = []
    ramas = []
    for tok in tokens:
        if "-" in tok:
            raiz, _, suf = tok.rpartition("-")
            if suf in MAPA_ASPECTO and (raiz in L._RAICES_VERB or len(raiz) >= 3):
                encontrados.append(MAPA_ASPECTO[suf])
                if raiz in L._RAICES_VERB:
                    v = L.VOCABULARIO_BASE.get(raiz, {})
                    from curiana_database import normalize_source_language as _n
                    lengua = _n(v.get("fuente", "")) if v else "sin-entrada"
                    rama = f"raiz_verbal:{lengua}"
                    # El caquetío se parte por CAPA, porque las dos mitades no
                    # son el mismo dato: las reconstruidas del núcleo se
                    # escribieron a mano como verbos; las atestiguadas llevan
                    # su `cat: v_raiz` puesto por la heurística de una línea de
                    # `minar_zavala_glosario.py`, que es lo que otra sesión
                    # está clasificando ahora mismo (49 raíces, estativo /
                    # acción / nombre). Aquí NO se toca ninguna `cat`: se
                    # cuenta cuánto del score depende de esa clasificación.
                    if lengua == "caquetío":
                        rama += (":atestiguada-cat-pendiente"
                                 if v.get("fuente") == "caquetío-atestiguado"
                                 else ":reconstruida-del-nucleo")
                else:
                    rama = "comodin_de_longitud"
                ramas.append((tok, raiz, suf, rama))
            continue
        for raiz in L._RAICES_VERB:
            for suf, nombre in MAPA_ASPECTO.items():
                if tok == raiz + suf:
                    encontrados.append(nombre)
                    ramas.append((tok, raiz, suf, "aglutinado"))
    return list(dict.fromkeys(encontrados)), ramas


# ══════════════════════════════════════════════════════════════════════
# EL CONTRASTE ARAHUACO — rasgos que la comparanda del repo documenta
# ══════════════════════════════════════════════════════════════════════
# Cada rasgo trae: la cita de la comparanda (con clave foránea a
# `4-fuentes/bibliografia.yaml`), y una SONDA declarada sobre el canon, para
# que el cero se pueda verificar (regla 6). La sonda dice qué se buscó.
RASGOS = [
    {
        "rasgo": "clases de verbo: estativo vs. activo",
        "comparanda": ("perea-alonso-1942 pp. 634-640: la 4ª conjugación lokono "
                       "es la de los ESTATIVOS (colores, tamaños, sabores, "
                       "estados) — cule-n «ser rojo», ibe-n «estar lleno», "
                       "hebbe-n «ser viejo» — y lleva el pronombre POSPUESTO; "
                       "p. 598-599 y 608, la teoría de Quandt: cualquier nombre "
                       "o adjetivo se hace verbo con a-/c- y terminación verbal"),
        "yaml": "6-fusion/lokono_gramatica_perea_1942.yaml §verbo_paradigmas",
        "sonda_canon": "cat de VOCABULARIO_BASE: ¿hay alguna que distinga estativo de activo?",
    },
    {
        "rasgo": "alineamiento y marcas de persona (prefijo transitivo / pospuesto estativo)",
        "comparanda": ("perea-alonso-1942 pp. 635 y 652: dos juegos. Prefijados "
                       "d-a-, b-a-, l-a-, t-a-, w-a-, h-a-, n-a- en los "
                       "transitivos; pospuestos de, bu, i, n, u, hu, ye en "
                       "estativos y negativos"),
        "yaml": "6-fusion/lokono_gramatica_perea_1942.yaml §los_dos_juegos_de_pronombres",
        "sonda_canon": "pronombres del canon: taya · pia · nüma · waya · naya, y su fuente",
    },
    {
        "rasgo": "posesión alienable / inalienable",
        "comparanda": ("perea-alonso-1942 p. 587: índices personales sobre el "
                       "nombre (da-si-kua «mi casa») y el índice ABSOLUTO u-/ù- "
                       "«u-si-kua-hù = LA casa, sin poseedor», que es la marca "
                       "de no-poseído; p. 586, posesivos absolutos da-kía «mío»"),
        "yaml": "6-fusion/lokono_gramatica_perea_1942.yaml §afijos.indices_personales",
        "sonda_canon": "¿alguna regla o entrada del canon declara alienable/inalienable o no-poseído?",
    },
    {
        "rasgo": "ka- atributivo / ma- privativo",
        "comparanda": ("van-buurt-2014 §8: ka- localizador «hay, existe(n)» "
                       "(Casibari = «hay rocas duras»); perea-alonso-1942 p. 555: "
                       "par mínimo k-ere-u-ti «casado» / m-ere-u-ti «soltero», "
                       "c-a-nsi-ti «amante» (el que tiene afecto)"),
        "yaml": "6-fusion/lokono_gramatica_perea_1942.yaml §afijos.atributivo_y_privativo",
        "sonda_canon": "REGLAS_POSESIVAS['ka-'] y ['ma-']: función declarada y apoyo",
    },
    {
        "rasgo": "número y colectivo",
        "comparanda": ("perea-alonso-1942 p. 556: plural pospuesto -nu "
                       "(wadi-li-nu «varones»), y los irracionales NO distinguen "
                       "número (keyu «venado, venados», siba «piedra, piedras», "
                       "adda «árbol, árboles»)"),
        "yaml": "6-fusion/lokono_gramatica_perea_1942.yaml §afijos.numero",
        "sonda_canon": "REGLAS_NUMERO: -kana y -naiki, su apoyo y su uso en la base",
    },
    {
        "rasgo": "género / clasificadores",
        "comparanda": ("perea-alonso-1942 p. 554: no hay género gramatical, hay "
                       "VARONIL y NO VARONIL, con sufijos -ti/-tti vr. y "
                       "-tu/-ttu nv., y -nu plural común. neira-ribero-1762 "
                       "(achagua) cambia el número según lo que se cuenta"),
        "yaml": "6-fusion/lokono_gramatica_perea_1942.yaml §afijos.genero",
        "sonda_canon": "¿alguna regla del motor marca género o clase nominal?",
    },
    {
        "rasgo": "nominalización",
        "comparanda": ("perea-alonso-1942 pp. 609-612: nombre de acción -hù "
                       "(a-iyaha-dda-hù «andadura»), -hi en los en -en "
                       "(c-a-nsi-hi «amor»); participios -ti/-tu/-nu; agentivo "
                       "-ha-li-n; p. 561, instrumental y local -na sobre -coa- "
                       "(a-balti-coa-na «asiento»), con el aviso del propio "
                       "Perea: «son pocos los vocablos así formados»"),
        "yaml": "6-fusion/lokono_gramatica_perea_1942.yaml §afijos.instrumental_y_local",
        "sonda_canon": "¿alguna regla del motor deriva un nombre de un verbo?",
    },
    {
        "rasgo": "aspecto de tres marcas -ka / -ni / -da",
        "comparanda": ("el propio canon lo declara wayuu-derivado "
                       "(2-lengua/morfologia.md §2). perea-alonso-1942 p. 606: "
                       "el gramático sospecha que el aparato de TIEMPO de su "
                       "fuente es «uno de los tantos perfeccionamientos a priori "
                       "de los misioneros»; el futuro lokono atestiguado es -pa"),
        "yaml": "6-fusion/lokono_gramatica_perea_1942.yaml §las_tres_marcas_de_aspecto_del_canon",
        "sonda_canon": "¿alguna entrada caquetío-atestiguada del lexicón sostiene -ka, -ni o -da?",
    },
    {
        "rasgo": "reduplicación",
        "comparanda": ("gatschet-1885: topónimos arubanos por duplicación de la "
                       "raíz disílaba; perea-alonso-1942 p. 679: «recurso "
                       "frecuente en nuestro Arawak», a-sucusu-n «lavar» → "
                       "a-sucu-sucu-n «bautizar»"),
        "yaml": "2-lengua/morfologia.md §4 (REDUPLICACION en lexicon_toponimos.py)",
        "sonda_canon": "¿alguna regla del motor produce o reconoce reduplicación?",
    },
    {
        "rasgo": "diminutivo",
        "comparanda": ("zavala-reyes-2015 #166: -iro «desinencia que se usa en "
                       "diminutivo»; van-buurt-2014 §6: -bi segundo diminutivo "
                       "(gobí, kokorobí); perea-alonso-1942 p. 562: lokono -can "
                       "(hia-ru-can «mujercita»)"),
        "yaml": "2-lengua/morfologia.md §1 y §5",
        "sonda_canon": "REGLAS_ZAVALA['-iro'] y el -bi de MORFEMAS_VAN_BUURT",
    },
]


def ejemplos_rancios(L) -> dict:
    """Los EJEMPLOS de cada regla, contrastados con el lexicón de hoy.

    Una regla cuyo ejemplo enseña una forma archivada (`piache + kana`) o una
    voz de la comparanda (`wayuu + kana = wayuukana`) es deuda documental: no
    llega al prompt —`prompt_afijos_atestiguados` sólo renderiza REGLAS_ZAVALA
    y REGLAS_TOPONIMICAS— pero es lo que lee quien venga detrás, y una
    referencia muerta ahí cuesta lo mismo que en el prompt (es la nota que el
    propio módulo ya se escribió para `paa-ka`).
    """
    from curiana_database import normalize_source_language as N
    salida: dict = {"con_forma_archivada": [], "con_voz_de_otra_lengua": [],
                    "con_forma_que_no_esta_en_el_lexicon": []}
    for nombre, _clase, _f in TABLAS:
        for afijo, regla in (getattr(L, nombre, {}) or {}).items():
            for ej in (regla.get("ejemplos") or []):
                for pieza in re.findall(r"[a-záéíóúüñ]{3,}", ej.lower()):
                    if pieza in L.FUERA_DEL_HABLA:
                        salida["con_forma_archivada"].append(
                            {"regla": afijo, "tabla": nombre, "ejemplo": ej,
                             "forma": pieza})
                        break
                    v = L.VOCABULARIO_BASE.get(pieza)
                    if v and N(v.get("fuente", "")) not in ("caquetío", ""):
                        salida["con_voz_de_otra_lengua"].append(
                            {"regla": afijo, "tabla": nombre, "ejemplo": ej,
                             "forma": pieza,
                             "lengua": N(v.get("fuente", ""))})
                        break
    # Y las formas DERIVADAS que la regla presenta como resultado y que el
    # lexicón no tiene con esa grafía: la deuda que D5 dejó en la morfología.
    # Sólo se miran los derivados que de verdad llevan el afijo pegado —si no,
    # lo que se está leyendo es la glosa española («estoy», «lugar»), no una
    # forma caquetía.
    for nombre, _clase, _f in TABLAS:
        for afijo, regla in (getattr(L, nombre, {}) or {}).items():
            desnudo = afijo.strip("-").lower()
            for ej in (regla.get("ejemplos") or []):
                if "=" not in ej:
                    continue
                der = ej.split("=", 1)[1].strip().split()[0].strip(",.;()")
                d = der.lower()
                lleva = (d.endswith(desnudo) if afijo.startswith("-")
                         else d.startswith(desnudo))
                if not (lleva and len(d) > len(desnudo) + 1 and "-" not in d):
                    continue
                if d in L.VOCABULARIO_BASE or d in L.FUERA_DEL_HABLA:
                    continue
                salida["con_forma_que_no_esta_en_el_lexicon"].append(
                    {"regla": afijo, "tabla": nombre, "derivado": der,
                     "ejemplo": ej,
                     "hay_gemela_con_k": (d.replace("c", "k")
                                          in L.VOCABULARIO_BASE)})
    salida["n_archivadas"] = len(salida["con_forma_archivada"])
    salida["n_otra_lengua"] = len(salida["con_voz_de_otra_lengua"])
    salida["n_fuera_del_lexicon"] = len(salida["con_forma_que_no_esta_en_el_lexicon"])
    return salida


def sondar_canon(L) -> dict:
    """Las sondas de RASGOS, corridas contra el canon. Un cero se dice con la
    consulta que lo produjo (regla 6)."""
    from curiana_database import normalize_source_language as N
    cats = collections.Counter(v.get("cat", "") for v in L.VOCABULARIO_BASE.values())
    caq = {k: v for k, v in L.VOCABULARIO_BASE.items()
           if N(v.get("fuente", "")) == "caquetío"}
    pron = {k: {"sig": v.get("sig", ""), "fuente": v.get("fuente", "")}
            for k, v in L.VOCABULARIO_BASE.items()
            if v.get("cat") == "pron" and N(v.get("fuente", "")) == "caquetío"}
    # ¿Alguna entrada ATESTIGUADA sostiene una marca de aspecto?
    aspecto_atestiguado = {
        a: [k for k, v in caq.items()
            if v.get("fuente") == "caquetío-atestiguado"
            and (k == a.strip("-") or k.endswith(a.strip("-")))
            and "aspect" in (v.get("sig", "") + v.get("notas", "")).lower()]
        for a in ("-ka", "-ni", "-da")}
    return {
        "categorias_de_VOCABULARIO_BASE": dict(cats.most_common()),
        "hay_cat_estativo": any("estativ" in c for c in cats),
        "hay_cat_activo": any(c in ("v_act", "v_activo") for c in cats),
        "v_raiz_total": cats.get("v_raiz", 0),
        "v_raiz_por_lengua": dict(collections.Counter(
            N(v.get("fuente", "")) for v in L.VOCABULARIO_BASE.values()
            if v.get("cat") == "v_raiz").most_common()),
        "v_raiz_caquetio": sorted(k for k, v in caq.items()
                                  if v.get("cat") == "v_raiz"),
        "pronombres_caquetios_en_el_lexicon": pron,
        "pronombres_del_prompt": ["taya", "pia", "nüma", "waya", "naya"],
        "pronombres_atestiguados": sorted(
            k for k, v in pron.items()
            if L.VOCABULARIO_BASE[k].get("fuente") == "caquetío-atestiguado"),
        "reglas_que_marcan_genero": sorted(
            a for a, r in L.TODAS_LAS_REGLAS.items()
            if "género" in (r.get("nombre", "") + r.get("desc", "")).lower()
            or "genero" in _sin_tildes(r.get("nombre", "") + r.get("desc", ""))),
        "reglas_que_nominalizan": sorted(
            a for a, r in L.TODAS_LAS_REGLAS.items()
            if slot_declarado(r.get("uso", "")) == "v_raiz"
            and "nombre" in (r.get("desc", "") or "").lower()),
        "reglas_de_reduplicacion": sorted(
            a for a in L.TODAS_LAS_REGLAS if "redup" in a.lower()),
        "reglas_de_posesion_no_poseida": sorted(
            a for a, r in L.TODAS_LAS_REGLAS.items()
            if "alienab" in (r.get("desc", "") or "").lower()
            or "no poseíd" in (r.get("desc", "") or "").lower()),
        "aspecto_con_apoyo_atestiguado": aspecto_atestiguado,
        # ¿De verdad «los pronombres no tienen rival atestiguado»? Es lo que
        # dice la política «manda la atestiguada» (2-lengua/lexicon.md), y se
        # comprueba listando TODO `cat: pron` de familia caquetía con su capa.
        "pronombres_atestiguados_con_glosa": {
            k: {"sig": L.VOCABULARIO_BASE[k].get("sig", ""),
                "notas": (L.VOCABULARIO_BASE[k].get("notas") or "")[:300]}
            for k in sorted(pron)
            if L.VOCABULARIO_BASE[k].get("fuente") == "caquetío-atestiguado"},
        "pronombres_del_prompt_por_capa": {
            k: L.VOCABULARIO_BASE.get(k, {}).get("fuente", "(no está)")
            for k in ("taya", "pia", "nüma", "waya", "naya")},
        # El `-kana` declara «COGNADO DIRECTO con Caquetío» y no dice con qué
        # forma. La sonda: qué claves caquetías del lexicón terminan en -kana.
        "formas_caquetias_en_-kana": sorted(
            k for k in caq if k.endswith("kana") and len(k) > 4),
        "formas_de_cualquier_lengua_en_-kana": sorted(
            k for k in L.VOCABULARIO_BASE if k.endswith("kana") and len(k) > 4)[:20],
        # La colisión ortográfica que D5 dejó en la morfología: los afijos se
        # escriben con `c` y el lexicón migró los lemas a `k`.
        "afijos_con_c_y_gemela_con_k": {
            a: (a.strip("-").replace("c", "k") in L.VOCABULARIO_BASE)
            for a in L.TODAS_LAS_REGLAS if "c" in a},
    }


# ══════════════════════════════════════════════════════════════════════
# YAML (a mano, como el resto de 6-fusion/)
# ══════════════════════════════════════════════════════════════════════
def _y(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if any(c in s for c in ":#{}[]&*!|>'\"%@`,") or s != s.strip() or not s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def volcar(obj, nivel=0, salida=None) -> list[str]:
    salida = salida if salida is not None else []
    ind = "  " * nivel
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                salida.append(f"{ind}{_y(k)}:")
                volcar(v, nivel + 1, salida)
            elif isinstance(v, (dict, list)):
                salida.append(f"{ind}{_y(k)}: {{}}" if isinstance(v, dict)
                              else f"{ind}{_y(k)}: []")
            else:
                salida.append(f"{ind}{_y(k)}: {_y(v)}")
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)) and v:
                salida.append(f"{ind}-")
                volcar(v, nivel + 1, salida)
            else:
                salida.append(f"{ind}- {_y(v)}")
    return salida


# ══════════════════════════════════════════════════════════════════════
def main(argv=None):
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sin-base", action="store_true",
                    help="sin Supabase: sólo el inventario y el contraste")
    ap.add_argument("--json", action="store_true", help="vuelca el doc en JSON")
    args = ap.parse_args(argv)

    sys.path.insert(0, SIM)
    import curiana_lexicon as L                                # noqa: E402
    from curiana_database import normalize_source_language as N  # noqa: E402

    biblio = claves_de_bibliografia()
    doc: dict = {
        "medicion": "morfologia-arahuaca",
        "fecha": FECHA,
        "encargo": ("Miguel, 2026-09-20: «echarle una revisada a toda la "
                    "morfología arahuaca, para que ajustemos; quiero que "
                    "tengamos la morfología bien clara»"),
        "regla_de_segmentacion": (
            "la del motor: se pelan por los bordes los afijos de _PREFIJOS_CAQ "
            "y _SUFIJOS_CAQ, prefijos primero, en el mismo orden que "
            "nucleo_de_token(); el control compara núcleo a núcleo"),
        "obras_en_bibliografia": len({v for v in biblio.values()}),
    }

    # ── 1. EL INVENTARIO ─────────────────────────────────────────────
    motor = morfemas_del_motor(L)
    yaml_canon = morfemas_del_yaml()
    propuestos = morfemas_propuestos(L)

    for afijo, d in motor.items():
        d["ensenado_en"] = donde_lo_ensena(L, afijo)
        d["reconocido_en"] = donde_lo_reconoce(L, afijo)
        d["citas"] = resolver_cita(d["apoyo"], biblio)
        if not d["citas"]:
            d["deuda"] = "sin-procedencia"

    # Las tres patologías.
    # (a) El motor lo ENSEÑA y el canon no lo declara. «Declarar» = estar en
    #     TODAS_LAS_REGLAS con una capa que no sea canon-simulación ni
    #     sin-declarar, o estar en 2-lengua/morfemas.yaml glosado.
    patologia_a = []
    for afijo, d in motor.items():
        if not d["ensenado_en"]:
            continue
        declarado = (d["capa"] in ("atestiguado", "reconstruido",
                                   "reconstruido-andamio-d11")
                     and d["en_TODAS_LAS_REGLAS"])
        if not declarado:
            patologia_a.append({"forma": afijo, "capa": d["capa"],
                                "ensenado_en": d["ensenado_en"],
                                "por_que": ("capa " + d["capa"]
                                            + ("; fuera de TODAS_LAS_REGLAS"
                                               if not d["en_TODAS_LAS_REGLAS"] else ""))})
    # Y el caso que no es de tabla: el afijo sin regla que la plantilla enseña.
    # Se busca en el texto de las plantillas cualquier «-x» o «x-» que no esté
    # en TODAS_LAS_REGLAS. Es literal: sale de llamar a las plantillas.
    textos = {
        "IDENTIDAD_LINGUISTICA": L.IDENTIDAD_LINGUISTICA,
        "prompt_reglas_completo": L.prompt_reglas_completo(),
        "prompt_reglas_breve": L.prompt_reglas_breve(),
    }
    sueltos_en_plantilla = collections.defaultdict(list)
    for nombre, texto in textos.items():
        for m in re.finditer(r"(?<![a-záéíóúüñ])-([a-záéíóúüñ]{2,7})\b",
                             texto.lower()):
            a = "-" + m.group(1)
            if a not in L.TODAS_LAS_REGLAS and a not in L.REGLAS_RETIRADAS:
                sueltos_en_plantilla[a].append(nombre)

    # (b) El canon lo declara y el motor NO lo reconoce al puntuar.
    patologia_b = []
    for forma, d in yaml_canon.items():
        en_motor = forma in L.TODAS_LAS_REGLAS
        if not en_motor:
            patologia_b.append({
                "forma": forma, "id": d.get("id"),
                "glosado": d.get("glosado"), "glosa": d.get("glosa", ""),
                "recurrencia": d.get("recurrencia"),
                "donde": "2-lengua/morfemas.yaml",
                "reconocido_por_el_scorer": donde_lo_reconoce(L, forma) or [],
            })
    # La reduplicación, que morfologia.md §4 declara medida y productiva y que
    # el motor no tiene como regla en ningún sitio.
    patologia_b.append({
        "forma": "REDUPLICACIÓN", "id": "morfologia.md §4",
        "glosado": True,
        "glosa": "pluralidad/abundancia y onomatopeya; 9,0 % del corpus toponímico",
        "donde": "2-lengua/morfologia.md §4 · REDUPLICACION en lexicon_toponimos.py",
        "reconocido_por_el_scorer": [],
    })

    # (c) Declarado con apoyo SÓLO en el andamio wayuu/lokono (deuda D11).
    #     Los ya retirados (-ko, -sha) se cuentan aparte: su problema ya está
    #     decidido y archivado.
    patologia_c = [{"forma": a, "clase": d["clase"],
                    "funcion_declarada": d["funcion_declarada"],
                    "apoyo": d["apoyo"], "ensenado_en": d["ensenado_en"],
                    "usos_de_score": d["reconocido_en"]}
                   for a, d in motor.items()
                   if d["solo_wayunaiki"] and d["capa"] != "retirada"]
    patologia_c_retirados = [a for a, d in motor.items()
                             if d["solo_wayunaiki"] and d["capa"] == "retirada"]

    # (d) La cuarta, que no estaba en el encargo y sale sola de las otras: el
    #     motor lo ENSEÑA y no hay clave foránea a `4-fuentes/bibliografia.yaml`
    #     (regla 8). No es lo mismo que (a) —ahí el canon dice otra cosa— ni
    #     que (c) —ahí el apoyo existe pero es el andamio—: aquí no hay apoyo.
    patologia_d = [{"forma": a, "clase": d["clase"],
                    "funcion_declarada": d["funcion_declarada"],
                    "apoyo_escrito": d["apoyo"] or "(vacío)",
                    "ensenado_en": d["ensenado_en"]}
                   for a, d in motor.items()
                   if d["ensenado_en"] and not d["citas"]]

    doc["inventario"] = {
        "morfemas_en_el_motor": len(motor),
        "en_TODAS_LAS_REGLAS": len(L.TODAS_LAS_REGLAS),
        "retirados": len(getattr(L, "REGLAS_RETIRADAS", {})),
        "en_2-lengua/morfemas.yaml": len(yaml_canon),
        "propuestos_sin_importar": len([k for k in propuestos
                                        if not k.startswith("__")]),
        "por_capa": dict(collections.Counter(
            d["capa"] for d in motor.values()).most_common()),
        "con_cita_valida": sum(1 for d in motor.values() if d["citas"]),
        "sin_procedencia": sorted(a for a, d in motor.items() if not d["citas"]),
        "detalle": [motor[a] for a in sorted(motor)],
    }
    doc["patologias"] = {
        "a_el_motor_ensena_lo_que_el_canon_no_declara": {
            "n": len(patologia_a), "detalle": patologia_a,
            "afijos_sueltos_en_plantilla_sin_regla":
                {k: v for k, v in sorted(sueltos_en_plantilla.items())},
        },
        "b_el_canon_declara_lo_que_el_motor_no_reconoce": {
            "n": len(patologia_b), "detalle": patologia_b},
        "c_apoyo_solo_en_el_andamio_d11": {
            "n": len(patologia_c), "detalle": patologia_c,
            "ya_retirados_por_lo_mismo": patologia_c_retirados},
        "d_ensenado_sin_clave_foranea_a_la_bibliografia": {
            "n": len(patologia_d), "detalle": patologia_d},
    }
    doc["deuda_documental_de_las_reglas"] = ejemplos_rancios(L)
    doc["morfemas_del_canon_de_datos"] = [yaml_canon[f] for f in sorted(yaml_canon)]
    doc["morfemas_propuestos"] = [propuestos[f] for f in sorted(propuestos)
                                  if not f.startswith("__")]

    # ── 4. EL CONTRASTE (no necesita base) ───────────────────────────
    doc["contraste_arahuaco"] = {
        "sondas_sobre_el_canon": sondar_canon(L),
        "rasgos": [{**r, "citas": resolver_cita(r["comparanda"], biblio)}
                   for r in RASGOS],
    }

    if args.sin_base:
        _informe(doc)
        _escribir(doc)
        return 0

    # ── 2. QUÉ HACE LA GENTE ─────────────────────────────────────────
    print("· leyendo word_uses…", file=sys.stderr)
    usos = usos_por_forma()
    seg = Segmentador(L)
    formas = sorted({u["forma"] for u in usos})
    n_desvios, ejemplos = seg.control(formas)
    doc["control_de_segmentacion"] = {
        "formas_comprobadas": len(formas),
        "desvios_contra_nucleo_de_token": n_desvios,
        "ejemplos": ejemplos,
        "verde": n_desvios == 0,
    }
    if n_desvios:
        raise RuntimeError(
            f"la segmentación de aquí no es la del motor en {n_desvios} formas: "
            f"{ejemplos}")

    clase_de = {a: d["clase"] for a, d in motor.items()}
    slot_de = {a: d["slot_declarado"] for a, d in motor.items()}

    def cat_de_nucleo(nucleo: list[str]) -> str:
        for s in nucleo:
            v = L.VOCABULARIO_BASE.get(s)
            if v:
                return v.get("cat", "sin-cat")
        return "raiz-fuera-del-lexicon"

    def lengua_de_nucleo(nucleo: list[str]) -> str:
        for s in nucleo:
            v = L.VOCABULARIO_BASE.get(s)
            if v:
                return N(v.get("fuente", ""))
        return "-"

    por_morfema: dict = collections.defaultdict(
        lambda: {"usos": 0, "formas": set(), "raices": set(),
                 "por_era_serie": collections.Counter(),
                 "cats_de_raiz": collections.Counter()})
    patrones: dict = collections.defaultdict(
        lambda: {"usos": 0, "formas": set(), "ejemplos": set()})
    secuencias: dict = collections.defaultdict(
        lambda: {"usos": 0, "formas": set(), "ejemplos": set()})
    violaciones: dict = collections.defaultdict(
        lambda: {"usos": 0, "formas": set(), "ejemplos": set()})
    violaciones_familia = collections.Counter()
    total_usos = 0
    total_con_afijo = 0
    por_era_serie_total = collections.Counter()

    for u in usos:
        forma, n = u["forma"], u["usos"]
        total_usos += n
        clave_es = f"{u['era']}/{u['serie']}"
        por_era_serie_total[clave_es] += n
        pref, nucleo, suf = seg(forma)
        afijos = pref + suf
        if not afijos:
            continue
        total_con_afijo += n
        cat = cat_de_nucleo(nucleo)
        raiz = "-".join(nucleo)
        for a in afijos:
            d = por_morfema[a]
            d["usos"] += n
            d["formas"].add(forma)
            d["raices"].add(raiz)
            d["por_era_serie"][clave_es] += n
            d["cats_de_raiz"][cat] += n
            # Violación de SLOT: el campo `uso` de la regla exige una categoría
            # y la raíz no la tiene. Sólo se juzga cuando la raíz ESTÁ en el
            # lexicón: de una raíz que no está no se puede decir su categoría.
            slot = slot_de.get(a, "sin-declarar")
            if cat != "raiz-fuera-del-lexicon" and slot in ("v_raiz", "sust"):
                if slot == "v_raiz" and cat != "v_raiz":
                    k = f"{clase_de.get(a, '?')} {a} sobre raíz «{cat}» (la regla pide VERBO_RAIZ)"
                elif slot == "sust" and cat == "v_raiz":
                    k = f"{clase_de.get(a, '?')} {a} sobre raíz verbal (la regla pide SUSTANTIVO)"
                else:
                    k = None
                if k:
                    v = violaciones[k]
                    v["usos"] += n
                    v["formas"].add(forma)
                    if len(v["ejemplos"]) < 8:
                        v["ejemplos"].add(f"{forma} ({raiz})")
                    familia = ("posesivo/atributivo sobre raíz verbal"
                               if slot == "sust" and clase_de.get(a) == "posesivo"
                               else "número sobre raíz verbal"
                               if slot == "sust"
                               else "aspecto sobre raíz no verbal")
                    violaciones_familia[familia] += n
        # COMBINACIÓN NO DECLARADA: dos o más afijos. Ninguna regla del
        # proyecto declara apilamiento — todos los campos `uso` son de un afijo.
        if len(afijos) >= 2:
            patron = " + ".join(
                [clase_de.get(a, "sin-clase") for a in pref]
                + [f"RAÍZ[{cat}]"]
                + [clase_de.get(a, "sin-clase") for a in suf])
            p = patrones[patron]
            p["usos"] += n
            p["formas"].add(forma)
            if len(p["ejemplos"]) < 10:
                p["ejemplos"].add(forma)
            # La misma secuencia sin la categoría de la raíz: es la que se cita
            # en prosa («locativo + aspecto», «aspecto + aspecto»), y se suma
            # aquí para que no la sume nadie a mano (regla 1).
            seq = " + ".join([clase_de.get(a, "sin-clase") for a in pref]
                             + ["RAÍZ"]
                             + [clase_de.get(a, "sin-clase") for a in suf])
            s = secuencias[seq]
            s["usos"] += n
            s["formas"].add(forma)
            if len(s["ejemplos"]) < 10:
                s["ejemplos"].add(forma)

    declarados = sorted(L.TODAS_LAS_REGLAS)
    sin_usar = [a for a in declarados if a not in por_morfema]
    doc["uso"] = {
        "usos_totales_en_word_uses": total_usos,
        "usos_en_formas_con_afijo_declarado": total_con_afijo,
        "formas_distintas": len(formas),
        "por_era_y_serie": dict(por_era_serie_total.most_common()),
        "morfemas_declarados": len(declarados),
        "morfemas_declarados_que_nadie_usa": sin_usar,
        "por_morfema": [
            {"forma": a,
             "clase": clase_de.get(a, "?"),
             "slot_declarado": slot_de.get(a, "?"),
             "usos": d["usos"],
             "formas_distintas": len(d["formas"]),
             "raices_distintas": len(d["raices"]),
             "por_era_y_serie": dict(d["por_era_serie"].most_common()),
             "cat_de_la_raiz": dict(d["cats_de_raiz"].most_common()),
             "muestra": sorted(d["formas"])[:10]}
            for a, d in sorted(por_morfema.items(),
                               key=lambda x: -x[1]["usos"])],
    }
    doc["combinaciones_no_declaradas"] = {
        "nota": ("ninguna regla del proyecto declara apilamiento de afijos: "
                 "los quince campos `uso` de TODAS_LAS_REGLAS son de UN afijo "
                 "sobre UNA raíz. Todo lo de abajo es gramática que la "
                 "comunidad produjo sin que nadie la escribiera"),
        "patrones_distintos": len(patrones),
        "usos": sum(p["usos"] for p in patrones.values()),
        "formas": len({f for p in patrones.values() for f in p["formas"]}),
        "por_secuencia_de_clases": [
            {"secuencia": k, "usos": v["usos"], "formas": len(v["formas"]),
             "ejemplos": sorted(v["ejemplos"])}
            for k, v in sorted(secuencias.items(), key=lambda x: -x[1]["usos"])],
        "detalle": [
            {"patron": k, "usos": v["usos"], "formas": len(v["formas"]),
             "ejemplos": sorted(v["ejemplos"])}
            for k, v in sorted(patrones.items(), key=lambda x: -x[1]["usos"])],
    }
    doc["violaciones_de_slot"] = {
        "nota": ("el slot sale del campo `uso` de cada regla, no se decide "
                 "aquí. Sólo se juzga cuando la raíz está en el lexicón"),
        "casos": len(violaciones),
        "usos": sum(v["usos"] for v in violaciones.values()),
        "por_familia": dict(violaciones_familia.most_common()),
        "detalle": [
            {"caso": k, "usos": v["usos"], "formas": len(v["formas"]),
             "ejemplos": sorted(v["ejemplos"])}
            for k, v in sorted(violaciones.items(), key=lambda x: -x[1]["usos"])],
    }

    # ── 3. EL ASPECTO, RAMA A RAMA ───────────────────────────────────
    print("· re-ejecutando el detector de aspecto sobre las respuestas…",
          file=sys.stderr)
    resp = respuestas()
    ramas = collections.Counter()
    ramas_usos = collections.Counter()
    ejemplos_rama: dict = collections.defaultdict(set)
    desvios_control = 0
    respuestas_con_aspecto = 0
    por_era_rama: dict = collections.defaultdict(collections.Counter)
    # EL PESO EN EL SCORE, que no es el número de detecciones: el score suma
    # `min(len(aspectos) * 1.0, 2.0)` sobre los aspectos DISTINTOS de cada
    # respuesta. Así que se cuentan los puntos, no los tokens.
    puntos_con = puntos_sin = 0.0
    respuestas_que_cambian = 0
    solo_por_comodin = 0
    for r in resp:
        limpio = L._normalizar(r["texto"])
        tokens = L._filtrar_nombres(limpio, L._tokenizar(limpio))
        mios, detalle = aspectos_instrumentado(L, tokens)
        suyos = L._aspectos_morfologicos(tokens)
        if mios != suyos:
            desvios_control += 1
        if detalle:
            respuestas_con_aspecto += 1
        sin_comodin = list(dict.fromkeys(
            MAPA_ASPECTO[s] for _t, _r, s, rama in detalle
            if rama != "comodin_de_longitud"))
        pc = min(len(mios) * 1.0, 2.0)
        ps = min(len(sin_comodin) * 1.0, 2.0)
        puntos_con += pc
        puntos_sin += ps
        if pc != ps:
            respuestas_que_cambian += 1
        if mios and not sin_comodin:
            solo_por_comodin += 1
        for tok, raiz, suf, rama in detalle:
            ramas[rama] += 1
            ramas_usos[(rama, suf)] += 1
            por_era_rama[f"{r['era']}/{r['serie']}"][rama] += 1
            if len(ejemplos_rama[rama]) < 12:
                ejemplos_rama[rama].add(tok)
    doc["aspecto_rama_a_rama"] = {
        "respuestas": len(resp),
        "respuestas_con_aspecto_detectado": respuestas_con_aspecto,
        "control_contra__aspectos_morfologicos": {
            "desvios": desvios_control, "verde": desvios_control == 0},
        "peso_en_el_score": {
            "nota": ("el score suma min(aspectos_distintos, 2) puntos de 10. "
                     "«Sin comodín» = sólo los aspectos que entran por una "
                     "raíz de _RAICES_VERB. No se propone nada aquí: se dice "
                     "cuánto del punto de morfología descansa en la rama que "
                     "no mira si hay verbo"),
            "puntos_de_aspecto_hoy": round(puntos_con, 1),
            "puntos_si_el_comodin_no_contara": round(puntos_sin, 1),
            "media_por_respuesta_hoy": round(puntos_con / (len(resp) or 1), 4),
            "media_sin_comodin": round(puntos_sin / (len(resp) or 1), 4),
            "respuestas_cuyo_punto_de_aspecto_cambia": respuestas_que_cambian,
            "respuestas_cuyo_aspecto_es_SOLO_comodin": solo_por_comodin,
            "de_respuestas": len(resp),
        },
        "detecciones_totales": sum(ramas.values()),
        "por_rama": dict(ramas.most_common()),
        "por_rama_y_sufijo": {f"{r} · -{s}": n
                              for (r, s), n in ramas_usos.most_common()},
        "por_era_y_serie": {k: dict(v.most_common())
                            for k, v in sorted(por_era_rama.items())},
        "ejemplos": {k: sorted(v) for k, v in sorted(ejemplos_rama.items())},
        "_RAICES_VERB": len(L._RAICES_VERB),
        "_RAICES_VERB_por_lengua": dict(collections.Counter(
            N(L.VOCABULARIO_BASE.get(k, {}).get("fuente", ""))
            for k in L._RAICES_VERB).most_common()),
    }

    _informe(doc)
    _escribir(doc)
    if args.json:
        print(json.dumps(doc, ensure_ascii=False, indent=2, default=str))
    return 0


def _informe(doc):
    inv = doc["inventario"]
    print("\n" + "═" * 74)
    print("EL INVENTARIO")
    print("═" * 74)
    print(f"  morfemas en el motor: {inv['morfemas_en_el_motor']} "
          f"({inv['en_TODAS_LAS_REGLAS']} activos + {inv['retirados']} retirados)")
    print(f"  en 2-lengua/morfemas.yaml: {inv['en_2-lengua/morfemas.yaml']} · "
          f"propuestos sin importar: {inv['propuestos_sin_importar']}")
    print(f"  por capa: {inv['por_capa']}")
    print(f"  con cita válida a bibliografia.yaml: {inv['con_cita_valida']} de "
          f"{inv['morfemas_en_el_motor']}")
    print(f"  deuda sin-procedencia: {inv['sin_procedencia']}")

    print("\n" + "═" * 74)
    print("LAS TRES PATOLOGÍAS")
    print("═" * 74)
    p = doc["patologias"]
    a = p["a_el_motor_ensena_lo_que_el_canon_no_declara"]
    print(f"  (a) el motor ENSEÑA y el canon no declara: {a['n']}")
    for d in a["detalle"]:
        print(f"        {d['forma']:<10} {d['por_que']:<40} {d['ensenado_en']}")
    if a["afijos_sueltos_en_plantilla_sin_regla"]:
        print(f"      afijos que la plantilla escribe sin regla detrás: "
              f"{a['afijos_sueltos_en_plantilla_sin_regla']}")
    b = p["b_el_canon_declara_lo_que_el_motor_no_reconoce"]
    print(f"  (b) el canon DECLARA y el scorer no reconoce: {b['n']}")
    for d in b["detalle"]:
        print(f"        {d['forma']:<14} {('glosado' if d['glosado'] else 'sin glosa'):<10} "
              f"{str(d.get('glosa',''))[:52]}")
    c = p["c_apoyo_solo_en_el_andamio_d11"]
    print(f"  (c) apoyo SÓLO en el andamio wayuu/lokono (deuda D11): {c['n']} "
          f"(+ {len(c['ya_retirados_por_lo_mismo'])} ya retirados: "
          f"{c['ya_retirados_por_lo_mismo']})")
    for d in c["detalle"]:
        print(f"        {d['forma']:<10} {d['funcion_declarada']:<34} "
              f"enseñado en {len(d['ensenado_en'])} plantillas")
    dd = p["d_ensenado_sin_clave_foranea_a_la_bibliografia"]
    print(f"  (d) el motor lo ENSEÑA y no hay clave foránea a la "
          f"bibliografía (regla 8): {dd['n']}")
    for d in dd["detalle"]:
        print(f"        {d['forma']:<10} {d['funcion_declarada']:<34} "
              f"«{str(d['apoyo_escrito'])[:44]}»")
    r = doc["deuda_documental_de_las_reglas"]
    print(f"\n  deuda documental de los EJEMPLOS de las reglas: "
          f"{r['n_archivadas']} con forma archivada · {r['n_otra_lengua']} con "
          f"voz de otra lengua · {r['n_fuera_del_lexicon']} con un derivado que "
          f"el lexicón no tiene")
    for d in (r["con_forma_archivada"] + r["con_voz_de_otra_lengua"])[:8]:
        print(f"        {d['regla']:<10} {d['ejemplo'][:62]}")
    for d in r["con_forma_que_no_esta_en_el_lexicon"][:8]:
        print(f"        {d['regla']:<10} derivado «{d['derivado']}» no está; "
              f"¿gemela con k? {d['hay_gemela_con_k']}")

    if "uso" in doc:
        u = doc["uso"]
        print("\n" + "═" * 74)
        print("QUÉ HACE LA GENTE CON ELLOS")
        print("═" * 74)
        print(f"  word_uses: {u['usos_totales_en_word_uses']} usos · "
              f"{u['formas_distintas']} formas distintas")
        print(f"  usos en formas con afijo declarado: "
              f"{u['usos_en_formas_con_afijo_declarado']}")
        print(f"  morfemas declarados que NADIE usa: "
              f"{u['morfemas_declarados_que_nadie_usa']}")
        print(f"\n  {'morfema':<10}{'clase':<12}{'usos':>8}{'formas':>8}"
              f"{'raíces':>8}   cat de la raíz (top)")
        for d in u["por_morfema"]:
            top = list(d["cat_de_la_raiz"].items())[:3]
            print(f"  {d['forma']:<10}{d['clase']:<12}{d['usos']:>8}"
                  f"{d['formas_distintas']:>8}{d['raices_distintas']:>8}   {top}")

        v = doc["violaciones_de_slot"]
        print(f"\n  VIOLACIONES DE SLOT: {v['casos']} casos · {v['usos']} usos")
        for fam, nn in v["por_familia"].items():
            print(f"    {nn:>6}  [{fam}]")
        for d in v["detalle"][:10]:
            print(f"    {d['usos']:>6}  {d['caso']}")
            print(f"            {', '.join(d['ejemplos'][:6])}")

        k = doc["combinaciones_no_declaradas"]
        print(f"\n  COMBINACIONES NO DECLARADAS: {k['patrones_distintos']} "
              f"patrones · {k['usos']} usos · {k['formas']} formas")
        print("  por SECUENCIA de clases (sin la categoría de la raíz):")
        for d in k["por_secuencia_de_clases"][:12]:
            print(f"    {d['usos']:>6}  {d['formas']:>4}f  {d['secuencia']}")
        print("  por patrón completo:")
        for d in k["detalle"][:14]:
            print(f"    {d['usos']:>6}  {d['patron']}")
            print(f"            {', '.join(d['ejemplos'][:5])}")

    if "aspecto_rama_a_rama" in doc:
        asp = doc["aspecto_rama_a_rama"]
        print("\n" + "═" * 74)
        print("EL ASPECTO, RAMA A RAMA (vale 2 de los 10 puntos del score)")
        print("═" * 74)
        ctrl = asp["control_contra__aspectos_morfologicos"]
        print(f"  control: {'VERDE' if ctrl['verde'] else 'ROJO'} "
              f"({ctrl['desvios']} desvíos de {asp['respuestas']})")
        print(f"  _RAICES_VERB: {asp['_RAICES_VERB']} claves · "
              f"{asp['_RAICES_VERB_por_lengua']}")
        pe = asp["peso_en_el_score"]
        print(f"  puntos de aspecto: {pe['puntos_de_aspecto_hoy']} hoy · "
              f"{pe['puntos_si_el_comodin_no_contara']} sin el comodín "
              f"(media {pe['media_por_respuesta_hoy']} → {pe['media_sin_comodin']})")
        print(f"  respuestas cuyo punto de aspecto cambiaría: "
              f"{pe['respuestas_cuyo_punto_de_aspecto_cambia']} de "
              f"{pe['de_respuestas']} · sólo comodín en "
              f"{pe['respuestas_cuyo_aspecto_es_SOLO_comodin']}")
        for rama, n in asp["por_rama"].items():
            print(f"    {rama:<34} {n:>7}   "
                  f"{', '.join(asp['ejemplos'].get(rama, [])[:5])}")

    s = doc["contraste_arahuaco"]["sondas_sobre_el_canon"]
    print("\n" + "═" * 74)
    print("CONTRASTE ARAHUACO — las sondas sobre el canon")
    print("═" * 74)
    print(f"  ¿hay cat estativo? {s['hay_cat_estativo']} · "
          f"¿hay cat activo? {s['hay_cat_activo']}")
    print(f"  v_raiz: {s['v_raiz_total']} claves · {s['v_raiz_por_lengua']}")
    print(f"  pronombres del prompt, por capa: {s['pronombres_del_prompt_por_capa']}")
    print(f"  pronombres caquetíos ATESTIGUADOS: {s['pronombres_atestiguados']}")
    for k, v in s["pronombres_atestiguados_con_glosa"].items():
        print(f"      {k:<10} {v['sig']}")
        print(f"                 {v['notas'][:110]}")
    print(f"  formas caquetías en -kana (el «cognado directo» de REGLAS_NUMERO): "
          f"{s['formas_caquetias_en_-kana']}")
    print(f"  afijos con c y su gemela con k en el lexicón: "
          f"{s['afijos_con_c_y_gemela_con_k']}")
    print(f"  reglas que marcan género: {s['reglas_que_marcan_genero']}")
    print(f"  reglas que nominalizan: {s['reglas_que_nominalizan']}")
    print(f"  reglas de reduplicación: {s['reglas_de_reduplicacion']}")
    print(f"  reglas de posesión alienable/no-poseída: "
          f"{s['reglas_de_posesion_no_poseida']}")


def _serializable(o):
    if isinstance(o, dict):
        return {k: _serializable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_serializable(v) for v in o]
    if isinstance(o, (set, frozenset)):
        return sorted(str(v) for v in o)
    return o


def _escribir(doc):
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# GENERADO por 6-fusion/scripts/auditar_morfologia.py\n")
        fh.write("# No se edita a mano. Ninguna cifra de aquí se escribe dos veces.\n")
        fh.write("\n".join(volcar(_serializable(doc))) + "\n")
    print(f"\n→ {os.path.relpath(SALIDA, RAIZ)}")


if __name__ == "__main__":
    raise SystemExit(main())
