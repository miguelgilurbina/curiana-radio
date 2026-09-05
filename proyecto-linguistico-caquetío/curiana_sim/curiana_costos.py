#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — el libro de costos: qué gasta cada llamada al modelo
===============================================================

Hasta el 2026-09-01 el motor tiraba `resp.usage` a la basura: hay 23 runs en
la base y ninguno sabe cuánto costó. La era 2 (DISENO_ERA2.md §7-8) tiene
regla de parada con techo de presupuesto, y sin medición no hay techo: por eso
el modelo de costos es el primer ladrillo.

QUÉ HACE
--------
- `LibroDeCostos` recibe el `usage` de cada llamada (agente, rescate
  intra-turno, director, observer) y lo acumula por tipo. `run_turn` le dice
  en qué turno está (`situar`) y vuelca las filas nuevas a `llm_calls`.
- Los precios viven en UNA tabla con fecha. Los dólares se calculan aquí,
  nunca en SQL: la vista de Supabase da tokens, este módulo los convierte.
- Funciona sin base: en modo JSON el libro se queda en memoria y se imprime
  al cerrar el run.

LO QUE NO ES
------------
No es una estimación. `usage` es lo que la API cobró. Para los runs viejos,
que no lo registraron, está `costos_runs.py` — y ese sí estima, y lo dice.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional


# ══════════════════════════════════════════════════════════════════════
# PRECIOS — la única cifra externa del módulo, con fecha
# ══════════════════════════════════════════════════════════════════════

# USD por millón de tokens. Tomados de la referencia `claude-api` del harness
# (tabla cacheada el 2026-06-24); caché: lectura ≈ 0.1× la entrada, escritura
# ≈ 1.25×. Antes de citar un dólar en un informe, verificar contra
# https://www.anthropic.com/pricing — un precio cambia sin avisar al repo.
PRECIOS_FECHA = "2026-06-24"
PRECIOS_USD_POR_MTOK: dict[str, dict[str, float]] = {
    "claude-haiku-4-5": {
        "input": 1.00, "output": 5.00, "cache_read": 0.10, "cache_write": 1.25,
    },
}


def _familia(modelo: str) -> str:
    """`claude-haiku-4-5-20251001` → `claude-haiku-4-5` (la tabla va sin fecha)."""
    partes = modelo.split("-")
    if partes and partes[-1].isdigit() and len(partes[-1]) == 8:
        partes = partes[:-1]
    return "-".join(partes)


def precio_de(modelo: str) -> dict[str, float]:
    fam = _familia(modelo)
    if fam not in PRECIOS_USD_POR_MTOK:
        raise KeyError(
            f"sin precio para {modelo!r} ({fam}); añadirlo a PRECIOS_USD_POR_MTOK "
            f"con su fecha — no se inventa")
    return PRECIOS_USD_POR_MTOK[fam]


def costo_usd(modelo: str, input_tokens: int = 0, output_tokens: int = 0,
              cache_read: int = 0, cache_write: int = 0) -> float:
    """Dólares de una llamada (o de una suma de llamadas) a `modelo`.

    `input_tokens` en la API de Anthropic NO incluye los tokens de caché: son
    tres cantidades separadas y se cobran a tres precios. Sumarlas al precio
    de entrada sobrecontaría la caché (o la infracontaría, según el lado).
    """
    p = precio_de(modelo)
    return (input_tokens * p["input"] + output_tokens * p["output"]
            + cache_read * p["cache_read"] + cache_write * p["cache_write"]) / 1e6


# ══════════════════════════════════════════════════════════════════════
# EL LIBRO
# ══════════════════════════════════════════════════════════════════════

# Tipos de llamada. `agente` es la 1ª pasada de call_agent; `rescate` la 2ª
# (D3: solo si el score normalizado cae bajo el umbral y no es ablación).
TIPOS = ("agente", "rescate", "director",
         "observer_analisis", "observer_reporte", "observer_perfil")


def usage_de(resp) -> dict[str, int]:
    """Extrae los cuatro contadores de un `Message` (o de su `.usage`).

    Los campos de caché vienen como None cuando no hubo caché: se normalizan a
    0 para que la aritmética no explote y la fila de la base quede completa.
    """
    u = getattr(resp, "usage", resp)
    def n(campo):
        v = getattr(u, campo, None)
        if v is None and isinstance(u, dict):
            v = u.get(campo)
        return int(v or 0)
    return {
        "input_tokens": n("input_tokens"),
        "output_tokens": n("output_tokens"),
        "cache_read_input_tokens": n("cache_read_input_tokens"),
        "cache_creation_input_tokens": n("cache_creation_input_tokens"),
    }


@dataclass
class Llamada:
    tipo: str
    model: str
    agent_name: Optional[str]
    input_tokens: int
    output_tokens: int
    cache_read_input_tokens: int
    cache_creation_input_tokens: int
    turn_id: Optional[str] = None
    day: Optional[int] = None
    turn_num: Optional[int] = None

    @property
    def usd(self) -> float:
        return costo_usd(self.model, self.input_tokens, self.output_tokens,
                         self.cache_read_input_tokens,
                         self.cache_creation_input_tokens)


class LibroDeCostos:
    """Acumula las llamadas de un run y sabe cuánto costaron.

    Se pasa por los mismos sitios que `difusion` o `competencia`: quien hace
    la llamada registra; quien cierra el turno vuelca; quien cierra el run
    imprime. Un `None` en cualquier punto desactiva la contabilidad sin
    romper nada (los tests del orquestador corren sin él).
    """

    def __init__(self) -> None:
        self._llamadas: list[Llamada] = []
        self._pendientes: list[Llamada] = []
        self._turn_id: Optional[str] = None
        self._dia: Optional[int] = None
        self._turno: Optional[int] = None

    # ── contexto ───────────────────────────────────────────────────────
    def situar(self, turn_id: Optional[str], dia: Optional[int],
               turno: Optional[int]) -> None:
        """Dónde estamos: las llamadas siguientes se cuelgan de este turno."""
        self._turn_id, self._dia, self._turno = turn_id, dia, turno

    # ── registro ───────────────────────────────────────────────────────
    def registrar(self, tipo: str, resp, modelo: str,
                  agente: Optional[str] = None) -> Llamada:
        if tipo not in TIPOS:
            raise ValueError(f"tipo de llamada desconocido: {tipo!r} (∉ {TIPOS})")
        u = usage_de(resp)
        ll = Llamada(tipo=tipo, model=modelo, agent_name=agente,
                     turn_id=self._turn_id, day=self._dia, turn_num=self._turno,
                     **u)
        self._llamadas.append(ll)
        self._pendientes.append(ll)
        return ll

    # ── volcado ────────────────────────────────────────────────────────
    def filas_pendientes(self) -> list[dict]:
        """Las llamadas aún no volcadas, como filas de `llm_calls`. Las marca
        como volcadas: si la escritura falla, el caller las cuenta en
        `db_fallos` como con cualquier otra tabla."""
        filas = [asdict(ll) for ll in self._pendientes]
        self._pendientes = []
        return filas

    # ── lectura ────────────────────────────────────────────────────────
    def llamadas(self, tipo: Optional[str] = None) -> list[Llamada]:
        return [ll for ll in self._llamadas if tipo is None or ll.tipo == tipo]

    def totales(self, tipo: Optional[str] = None) -> dict[str, float]:
        lls = self.llamadas(tipo)
        t = {
            "llamadas": len(lls),
            "input_tokens": sum(ll.input_tokens for ll in lls),
            "output_tokens": sum(ll.output_tokens for ll in lls),
            "cache_read_input_tokens": sum(ll.cache_read_input_tokens for ll in lls),
            "cache_creation_input_tokens": sum(ll.cache_creation_input_tokens for ll in lls),
        }
        t["usd"] = sum(ll.usd for ll in lls)
        return t

    def dias(self) -> int:
        return len({ll.day for ll in self._llamadas if ll.day is not None})

    def reporte(self) -> str:
        """El resumen que se imprime al cerrar el run."""
        tot = self.totales()
        if not tot["llamadas"]:
            return "  (sin llamadas registradas)"
        lineas = [f"  {'tipo':18} {'llamadas':>8} {'entrada':>10} {'salida':>9} {'USD':>9}"]
        for tipo in TIPOS:
            t = self.totales(tipo)
            if t["llamadas"]:
                lineas.append(f"  {tipo:18} {t['llamadas']:>8} {t['input_tokens']:>10,} "
                              f"{t['output_tokens']:>9,} {t['usd']:>9.4f}")
        lineas.append(f"  {'TOTAL':18} {tot['llamadas']:>8} {tot['input_tokens']:>10,} "
                      f"{tot['output_tokens']:>9,} {tot['usd']:>9.4f}")
        cache = tot["cache_read_input_tokens"] + tot["cache_creation_input_tokens"]
        if cache:
            lineas.append(f"  caché: {tot['cache_read_input_tokens']:,} leídos · "
                          f"{tot['cache_creation_input_tokens']:,} escritos")
        d = self.dias()
        if d:
            lineas.append(f"  por día simulado: {tot['usd'] / d:.4f} USD "
                          f"({d} día(s); precios del {PRECIOS_FECHA})")
        return "\n".join(lineas)
