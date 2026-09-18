#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — la cadena de runs encadenados (`--continuar`)
=======================================================

POR QUÉ ESTE MÓDULO EXISTE
--------------------------
En la era 2 un run **es un día**: seis turnos, se cierra, y el día siguiente
arranca otro run con `--continuar`, que hereda estado, memoria, lexicón y koiné
del anterior y deja en `simulation_runs.config` la clave `continuado_desde`.

`koine_metrics` guarda **una fila por día y por run**. El veredicto de
convergencia del orquestador miraba sólo la serie del run en curso, que en la
era 2 tiene UN punto — y por eso imprimía «datos insuficientes (ningún par de
días comparable)» al cerrar cada día, aunque la serie de la cadena entera ya
tuviera dos o más (medido el 2026-09-16 sobre `c6837386` → `89fc1744`).
`analizar_runs.py` tampoco seguía la cadena: la serie de dos días de la bitácora
se armó a mano juntando los dos runs.

Aquí la cadena es código: se sube por `continuado_desde` hasta la raíz, se unen
las `koine_metrics` de todos sus runs y se emite **el mismo veredicto** que emite
el orquestador — `veredicto()` es la extracción literal de ese bloque, no un
criterio nuevo: elige la lectura más exigente con al menos dos días
(emergente > ventana > acumulada) y la pasa por
`curiana_koine.veredicto_convergencia`.

QUÉ ES UN RUN QUE NO CUENTA
---------------------------
Un run interrumpido —sin `ended_at` o con `total_turns` 0— sigue estando EN la
cadena (hay que poder subir a través de él), pero sus `koine_metrics` se saltan
con aviso: la unidad de la serie es un día cerrado. Pasó con `06482296`, el día
3 del 2026-09-16, que murió a los 2 turnos.

EL LECTOR
---------
El módulo no sabe de Supabase ni de psql: habla con cualquier objeto que
ofrezca tres métodos (`CurianaDB` los tiene; `analizar_runs.py` los sirve por
`docker exec psql`; un test los falsea en diez líneas):

    get_run(run_id)        -> dict | None
    koine_metrics(run_id)  -> list[dict]   (day, distance, distance_ventana,
                                            distance_emergente, n_agents)
    runs_encadenados()     -> list[dict]   (todos los runs, para descubrir
                                            las cadenas; opcional)

Uso:
    python curiana_cadena.py          # las cadenas de la base, medidas
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional

from curiana_koine import veredicto_convergencia

# Una cadena de mil días sería un ciclo, no una cadena.
LIMITE_CADENA = 500

# Las tres lecturas de la distancia idiolectal, de la MÁS exigente a la menos.
# El orden es el del veredicto; el de impresión es el inverso (ver `lineas_de_serie`).
LECTURAS = (("emergente", 3), ("ventana", 2), ("acumulada", 1))

# Una serie es una lista de (día, acumulada, ventana, emergente). Es la misma
# forma que `serie_distancia` en el orquestador, a propósito: el veredicto de la
# cadena y el del run se calculan con la misma función sobre la misma estructura.
Serie = list[tuple[int, Optional[float], Optional[float], Optional[float]]]


# ══════════════════════════════════════════════════════════════════════
# I. LEER UN RUN
# ══════════════════════════════════════════════════════════════════════

def config_de(run: dict) -> dict:
    """La `config` de un run como dict.

    Llega como objeto jsonb desde supabase-py y como texto desde psql; y un
    lector que ya aplanó las claves (SELECT config->>'continuado_desde') no
    trae `config` en absoluto. Los tres casos son válidos."""
    cfg = run.get("config")
    if isinstance(cfg, dict):
        return cfg
    if isinstance(cfg, str) and cfg.strip():
        try:
            cargado = json.loads(cfg)
            return cargado if isinstance(cargado, dict) else {}
        except (ValueError, TypeError):
            return {}
    return {}


def _valor(run: dict, clave: str) -> Any:
    """Busca una clave en la config o, si el lector la aplanó, en la fila."""
    cfg = config_de(run)
    if cfg.get(clave) is not None:
        return cfg[clave]
    return run.get(clave)


def continuado_desde(run: dict) -> Optional[str]:
    """El run del que éste continúa, o None si es raíz de cadena."""
    padre = _valor(run, "continuado_desde")
    if padre is None:
        return None
    padre = str(padre).strip()
    return padre or None


def dia_inicial(run: dict) -> Optional[int]:
    dia = _valor(run, "dia_inicial")
    try:
        return int(dia)
    except (TypeError, ValueError):
        return None


# ══════════════════════════════════════════════════════════════════════
# I-b. EL BRAZO — una cadena con escena y otra sin ella no se unen
# ══════════════════════════════════════════════════════════════════════
# «Una escena no puede entrar a mitad de cadena: es una serie nueva desde el
# día 1» (diseño §5.4). El orquestador ya se niega a continuar cambiando de
# brazo (`comprobar_brazo_de_escena`), pero la base viene de antes que esa
# comprobación y un run de la era 2 anterior a hoy ni siquiera declara la
# clave. Aquí se lee lo que la config dice y, si una cadena mezcla, el
# veredicto AVISA y no mezcla las métricas: la evidencia es la diferencia
# entre dos cadenas completas con la misma semilla, no una media de las dos.

def brazo_de(run: dict) -> tuple:
    """`(escena, capubana_cada)` tal como lo selló la config del run.

    Un run anterior a la escena no trae la clave: entonces es `(False, 0)`, y
    es un hecho, no un supuesto — antes del 2026-09-17 la escena no existía."""
    cfg = config_de(run)
    escena = cfg.get("escena")
    if escena is None:
        escena = run.get("escena")
    escena = bool(escena)
    cada = cfg.get("capubana_cada")
    if cada is None:
        cada = run.get("capubana_cada")
    try:
        cada = int(cada or 0)
    except (TypeError, ValueError):                     # pragma: no cover
        cada = 0
    return (escena, cada if escena else 0)


def texto_de_brazo(brazo: tuple) -> str:
    escena, cada = brazo
    if not escena:
        return "sin escena"
    return "con escena" + (f", Capubana cada {cada}" if cada else ", sin Capubana")


def brazos_de_cadena(cadena: list[dict]) -> dict:
    """`{brazo: [run_id, …]}` — cuántos brazos distintos hay en una cadena."""
    por_brazo: dict = {}
    for run in cadena or []:
        por_brazo.setdefault(brazo_de(run), []).append(id_de(run))
    return por_brazo


def es_interrumpido(run: dict) -> bool:
    """Un run sin `ended_at` o con `total_turns` 0 no cerró ningún día.

    Sigue en la cadena (se sube a través de él), pero sus métricas no entran en
    la serie: la unidad es el día cerrado, no el run."""
    fin = run.get("ended_at")
    if fin is None or (isinstance(fin, str) and not fin.strip()):
        return True
    try:
        return int(run.get("total_turns") or 0) == 0
    except (TypeError, ValueError):
        return True


def id_de(run: dict) -> str:
    return str(run.get("id") or "")


def corto(run_id: Optional[str]) -> str:
    return (run_id or "?")[:8]


# ══════════════════════════════════════════════════════════════════════
# II. LA CADENA
# ══════════════════════════════════════════════════════════════════════

def cadena_de_runs(db: Any, run_id: str) -> list[dict]:
    """Sube por `continuado_desde` hasta la raíz. Devuelve raíz→hoja.

    Incluye los runs interrumpidos (saltarlos rompería la cadena por el medio).
    Un padre que no está en la base corta el ascenso: se devuelve lo que se pudo
    reconstruir. Sin base (o con un lector que no sabe leer runs) devuelve []."""
    leer = getattr(db, "get_run", None)
    if db is None or not callable(leer) or not run_id:
        return []
    cadena: list[dict] = []
    vistos: set[str] = set()
    actual: Optional[str] = str(run_id)
    while actual and actual not in vistos and len(cadena) < LIMITE_CADENA:
        vistos.add(actual)
        run = leer(actual)
        if not run:
            break
        cadena.append(run)
        actual = continuado_desde(run)
    cadena.reverse()
    return cadena


def serie_koine_de_cadena(db: Any, run_id: str,
                          avisos: Optional[list[str]] = None,
                          cadena: Optional[list[dict]] = None) -> Serie:
    """Une las `koine_metrics` de toda la cadena, ordenadas por día.

    - Los runs interrumpidos se saltan con aviso (ver `es_interrumpido`).
    - **Los runs de OTRO BRAZO se saltan con aviso** (ver `brazo_de`): una
      cadena con escena y otra sin ella no se unen, y una cadena que cambió de
      brazo a la mitad no se promedia. Manda el brazo de la HOJA, que es el
      run desde el que se pregunta.
    - Un día que aparece en dos runs de la cadena no se duplica: gana el run
      más avanzado (el más cercano a la hoja), que es el que lo volvió a medir
      sobre el estado heredado.
    - `avisos`, si se pasa, recibe las líneas de lo que se saltó. El módulo no
      imprime: quien llama decide dónde va el aviso.
    - `cadena`, si ya se reconstruyó, ahorra volver a subirla.
    """
    leer_metricas = getattr(db, "koine_metrics", None)
    if cadena is None:
        cadena = cadena_de_runs(db, run_id)
    if not cadena or not callable(leer_metricas):
        return []
    brazo_hoja = brazo_de(cadena[-1])
    por_dia: dict[int, tuple] = {}
    for run in cadena:                       # raíz→hoja: el último gana
        rid = id_de(run)
        if brazo_de(run) != brazo_hoja:
            if avisos is not None:
                avisos.append(
                    f"run {corto(rid)} corrió {texto_de_brazo(brazo_de(run))} y "
                    f"la hoja {texto_de_brazo(brazo_hoja)}: NO se mezclan. La "
                    f"evidencia es la diferencia entre dos cadenas completas "
                    f"con la misma semilla, no una cadena mitad y mitad")
            continue
        if es_interrumpido(run):
            if avisos is not None:
                avisos.append(
                    f"run {corto(rid)} interrumpido (sin ended_at o 0 turnos): "
                    f"sus métricas no entran en la serie")
            continue
        for fila in leer_metricas(rid) or []:
            dia = fila.get("day")
            if dia is None:
                continue
            por_dia[int(dia)] = (
                int(dia),
                _num(fila.get("distance")),
                _num(fila.get("distance_ventana")),
                _num(fila.get("distance_emergente")),
            )
    return [por_dia[d] for d in sorted(por_dia)]


def _num(valor: Any) -> Optional[float]:
    """psql devuelve `numeric` como texto y los nulos como NaN en pandas."""
    if valor is None or valor == "":
        return None
    try:
        f = float(valor)
    except (TypeError, ValueError):
        return None
    return None if f != f else f        # NaN


def cadenas_en_la_base(db: Any) -> list[list[dict]]:
    """Todas las cadenas de ≥ 2 runs, de la más antigua a la más reciente.

    Una cadena se identifica por su HOJA: el run del que nadie continúa. Un run
    suelto (sin padre ni hijos) no es cadena y no se devuelve."""
    listar = getattr(db, "runs_encadenados", None)
    if not callable(listar):
        return []
    runs = list(listar() or [])
    padres = {continuado_desde(r) for r in runs}
    padres.discard(None)
    cadenas = []
    for run in runs:
        rid = id_de(run)
        if rid in padres:
            continue                     # no es hoja: alguien continúa de él
        cadena = cadena_de_runs(db, rid)
        if len(cadena) > 1:
            cadenas.append(cadena)
    return cadenas


# ══════════════════════════════════════════════════════════════════════
# III. EL VEREDICTO — el mismo que emite el orquestador
# ══════════════════════════════════════════════════════════════════════

def veredicto(serie: Serie) -> tuple[Optional[str], str, str,
                                     Optional[float], Optional[float]]:
    """El veredicto de convergencia sobre una serie de días.

    Es el bloque «KOINÉ — convergencia» de `auto_mode` extraído tal cual, para
    que el run y su cadena no puedan juzgarse con criterios distintos:

      1. Se elige la lectura MÁS EXIGENTE con al menos dos días comparables:
         emergente > ventana > acumulada. (La acumulada converge casi siempre
         por mera acumulación del vocabulario base — no es evidencia sola.)
      2. Esa lectura pasa por `curiana_koine.veredicto_convergencia`, que mira
         la caída total (>5%) Y la pendiente del último tercio (>2%), para
         separar convergencia sostenida de un plateau.

    Devuelve (etiqueta, codigo, mensaje, d_inicio, d_fin). Sin dos días
    comparables en ninguna lectura: (None, "insuficiente", …, None, None).
    """
    for etiqueta, idx in LECTURAS:
        puntos = [(p[0], p[idx]) for p in serie if p[idx] is not None]
        if len(puntos) >= 2:
            codigo, mensaje = veredicto_convergencia(puntos)
            return etiqueta, codigo, mensaje, puntos[0][1], puntos[-1][1]
    return (None, "insuficiente",
            "datos insuficientes (ningún par de días comparable)", None, None)


def texto_veredicto(serie: Serie) -> str:
    """La línea de veredicto, sin sangría. Quien imprime decide la sangría."""
    etiqueta, _codigo, mensaje, d_ini, d_fin = veredicto(serie)
    if etiqueta is None:
        return f"Veredicto: {mensaje}"
    return f"Veredicto [{etiqueta}]: inicio {d_ini} → fin {d_fin}  →  {mensaje}"


def lineas_de_serie(serie: Serie) -> list[str]:
    """Las tres trayectorias, una por lectura, sin sangría."""
    fmt = lambda v: "s/d" if v is None else v
    lineas = []
    for etiqueta, idx in (("acumulada", 1), ("ventana  ", 2), ("emergente", 3)):
        traj = " → ".join(f"D{p[0]}:{fmt(p[idx])}" for p in serie)
        lineas.append(f"{etiqueta}: {traj}")
    return lineas


def resumen_de_cadena(cadena: list[dict]) -> str:
    """`c6837386 → 89fc1744 → 06482296 ⚠` — la cadena en una línea."""
    partes = []
    for run in cadena:
        marca = " ⚠" if es_interrumpido(run) else ""
        dia = dia_inicial(run)
        dia_txt = f"(D{dia})" if dia is not None else ""
        partes.append(f"{corto(id_de(run))}{dia_txt}{marca}")
    return " → ".join(partes)


def linea_de_brazo(cadena: list[dict]) -> str:
    """El brazo con que corrió la cadena, y el aviso si mezcla."""
    por_brazo = brazos_de_cadena(cadena)
    if not por_brazo:                                   # pragma: no cover
        return ""
    if len(por_brazo) == 1:
        return f"brazo: {texto_de_brazo(next(iter(por_brazo)))}"
    detalle = " · ".join(
        f"{texto_de_brazo(b)} ({', '.join(corto(r) for r in runs)})"
        for b, runs in por_brazo.items())
    return (f"⚠ ESTA CADENA MEZCLA {len(por_brazo)} BRAZOS: {detalle}. "
            f"Sólo cuentan los días del brazo de la hoja")


# ══════════════════════════════════════════════════════════════════════
# IV. UN LECTOR QUE NO NECESITA CREDENCIALES
# ══════════════════════════════════════════════════════════════════════

class LectorSQL:
    """Lector de la base local por `docker exec psql`, sin supabase-py.

    El orquestador ya tiene su `CurianaDB` y usa ése. Esto es para el tooling
    (`analizar_runs.py`, el CLI de aquí), que corre sin `.env`: mismo criterio
    de la casa —«no usa psycopg2: habla con Postgres por docker exec y lee
    CSV»— y ojo con el otro Supabase de la máquina (fintech), por eso el
    contenedor va por nombre y no por puerto."""

    CONTENEDOR = "supabase_db_curiana_sim"
    # Los ids vienen de la propia base; el patrón es un cinturón, no un traje.
    _UUID = re.compile(r"^[0-9a-fA-F-]{36}$")

    def __init__(self, contenedor: Optional[str] = None):
        self.contenedor = contenedor or self.CONTENEDOR
        self._cache_runs: dict[str, Optional[dict]] = {}

    def _consulta(self, sql: str) -> list[dict]:
        import csv
        import io as _io
        import subprocess
        out = subprocess.run(
            ["docker", "exec", self.contenedor, "psql", "-U", "postgres",
             "-d", "postgres", "--csv", "-c", sql],
            capture_output=True, text=True, encoding="utf-8", timeout=180)
        if out.returncode != 0:
            raise RuntimeError(f"psql falló:\n{out.stderr.strip()[:300]}")
        filas = list(csv.DictReader(_io.StringIO(out.stdout)))
        return [{k: (v if v not in ("", None) else None) for k, v in f.items()}
                for f in filas]

    def get_run(self, run_id: str) -> Optional[dict]:
        if run_id in self._cache_runs:
            return self._cache_runs[run_id]
        if not self._UUID.match(str(run_id)):
            return None
        filas = self._consulta(
            "SELECT id::text AS id, started_at, ended_at, total_turns, "
            "config::text AS config FROM simulation_runs "
            f"WHERE id = '{run_id}'")
        run = filas[0] if filas else None
        self._cache_runs[run_id] = run
        return run

    def runs_encadenados(self) -> list[dict]:
        return self._consulta(
            "SELECT id::text AS id, started_at, ended_at, total_turns, "
            "config::text AS config FROM simulation_runs ORDER BY started_at")

    def koine_metrics(self, run_id: str) -> list[dict]:
        if not self._UUID.match(str(run_id)):
            return []
        return self._consulta(
            "SELECT day, distance, distance_ventana, distance_emergente, "
            f"n_agents FROM koine_metrics WHERE run_id = '{run_id}' ORDER BY day")

    def prestamos(self, run_ids: list[str]) -> list[dict]:
        """Usos de la esfera de contacto (`loanword_uses`) de varios runs.

        `forma_dicha` (migración 20260918) trae lo que el agente escribió;
        en las filas anteriores es NULL y se rellena con `word`, que allí ES
        lo que se dijo. Quien lee normaliza `word` a la forma de la esfera:
        los runs viejos no se reescriben.
        """
        ids = [r for r in run_ids if self._UUID.match(str(r))]
        if not ids:
            return []
        lista = ", ".join(f"'{r}'" for r in ids)
        return self._consulta(
            "SELECT run_id::text AS run_id, day, tier, word, "
            "coalesce(forma_dicha, word) AS forma_dicha, "
            "source_language AS lengua, agent_name "
            f"FROM loanword_uses WHERE run_id IN ({lista}) "
            "ORDER BY day, tier, word")


# ══════════════════════════════════════════════════════════════════════
# CLI — las cadenas de la base, medidas
# ══════════════════════════════════════════════════════════════════════

def _forzar_utf8() -> None:
    import io
    import sys
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def informe(db: Any) -> int:
    """Imprime todas las cadenas con su serie y su veredicto. Devuelve cuántas."""
    cadenas = cadenas_en_la_base(db)
    if not cadenas:
        print("  (ninguna cadena: ningún run continúa de otro)")
        return 0
    for cadena in cadenas:
        hoja = id_de(cadena[-1])
        avisos: list[str] = []
        serie = serie_koine_de_cadena(db, hoja, avisos=avisos, cadena=cadena)
        print(f"\n  cadena: {resumen_de_cadena(cadena)}  ({len(cadena)} runs)")
        brazo = linea_de_brazo(cadena)
        if brazo:
            print(f"    {brazo}")
        for aviso in avisos:
            print(f"    ⚠ {aviso}")
        if not serie:
            print("    (sin días medidos)")
            continue
        for linea in lineas_de_serie(serie):
            print(f"    {linea}")
        print(f"    {texto_veredicto(serie)}")
    return len(cadenas)


if __name__ == "__main__":
    _forzar_utf8()
    print(f"\n{'═' * 72}\n  CADENAS DE RUNS — los días encadenados con --continuar\n{'═' * 72}")
    n = informe(LectorSQL())
    print(f"\n  {n} cadena(s).")
