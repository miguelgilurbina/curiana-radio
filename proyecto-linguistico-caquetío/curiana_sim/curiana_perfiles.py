#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""curiana_perfiles.py — los parámetros de cada simulación, declarados.

Diseño: `5-experimento/disenos/05_perfiles_de_run.md`
Datos:  `5-experimento/perfiles_de_run.yaml`

POR QUÉ EXISTE
--------------
Hasta ahora un run se definía por una combinación de flags que había que
recordar, y de la que sólo `--ablacion` quedaba registrada. Un perfil es esa
combinación con nombre, versionada en git y escrita ENTERA en
`simulation_runs.config`: un run de hace seis meses sigue diciendo con qué se
corrió aunque el perfil haya cambiado después.

LOS DOS EJES, que no se mezclan
-------------------------------
  A. `capas_lexicas` — qué capas epistémicas del lexicón VEN los agentes.
  B. `andamiaje`     — si las inyecciones de convergencia están o no.

Y la distinción que sostiene el experimento:

  🔴 `capas_lexicas` varía por perfil. `capas_de_score` NO.

  Si el brazo `suelto` se puntuara contando sus voces retro-abstraídas y el
  `atestiguado` no las tuviera, la diferencia entre brazos sería un artefacto
  del instrumento. Puntuando igual en todos, un run `suelto` que se apoye mucho
  en material intuido puntúa MÁS BAJO — y esa caída es el dato.

Uso:
    from curiana_perfiles import cargar_perfil
    perfil = cargar_perfil("suelto")
    perfil.capas          -> frozenset de etiquetas para el prompt
    perfil.ablacion       -> bool, para el orquestador
    perfil.como_config()  -> dict que va a simulation_runs.config

    python curiana_perfiles.py            # lista los perfiles
    python curiana_perfiles.py suelto     # muestra uno, resuelto
"""

from __future__ import annotations

import io
import os
import sys
from dataclasses import dataclass, field

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FICHERO = os.path.join(RAIZ, "5-experimento", "perfiles_de_run.yaml")

PERFIL_POR_DEFECTO = "base"


def _forzar_utf8():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


@dataclass(frozen=True)
class Perfil:
    nombre: str
    descripcion: str
    capas: frozenset
    andamiaje: str
    capas_de_score: frozenset
    pregunta: str = ""
    version: int = 1

    @property
    def ablacion(self) -> bool:
        """El eje B, traducido al flag que el orquestador ya entiende."""
        return self.andamiaje == "ninguno"

    def como_config(self) -> dict:
        """Lo que se guarda en `simulation_runs.config`: el perfil RESUELTO,
        no su nombre. Listas ordenadas para que dos runs iguales den el mismo
        JSON y se puedan comparar en SQL."""
        return {
            "perfil": self.nombre,
            "perfil_version": self.version,
            "capas_lexicas": sorted(self.capas),
            "capas_de_score": sorted(self.capas_de_score),
            "andamiaje": self.andamiaje,
            "ablacion": self.ablacion,
        }

    def __str__(self) -> str:
        return (f"{self.nombre} — {len(self.capas)} capa(s), "
                f"andamiaje {self.andamiaje}")


def _datos() -> dict:
    if not os.path.exists(FICHERO):
        raise FileNotFoundError(
            f"No está {os.path.relpath(FICHERO, RAIZ)}. Sin él no hay perfiles: "
            "un run sin perfil declarado es un run que dentro de seis meses "
            "nadie sabrá cómo se corrió.")
    return yaml.safe_load(io.open(FICHERO, encoding="utf-8").read())


def nombres() -> list[str]:
    return sorted(_datos()["perfiles"])


def cargar_perfil(nombre: str = PERFIL_POR_DEFECTO) -> Perfil:
    d = _datos()
    perfiles = d["perfiles"]
    if nombre not in perfiles:
        raise KeyError(
            f"No existe el perfil «{nombre}». Los que hay: "
            f"{', '.join(sorted(perfiles))}")

    p = perfiles[nombre]
    conocidas = set(d.get("capas_conocidas") or {})
    capas = list(p.get("capas_lexicas") or [])
    desconocidas = [c for c in capas if c not in conocidas]
    if desconocidas:
        raise ValueError(
            f"El perfil «{nombre}» pide capas que no están declaradas en "
            f"`capas_conocidas`: {desconocidas}. Si la capa es nueva, "
            "decláralas ahí primero — el fichero es la documentación.")

    andamiaje = p.get("andamiaje", "completo")
    if andamiaje not in ("completo", "ninguno"):
        raise ValueError(
            f"El perfil «{nombre}» declara andamiaje «{andamiaje}»; sólo hay "
            "«completo» y «ninguno».")

    return Perfil(
        nombre=nombre,
        descripcion=" ".join(str(p.get("descripcion", "")).split()),
        capas=frozenset(capas),
        andamiaje=andamiaje,
        capas_de_score=frozenset(d["capas_de_score"]),
        pregunta=" ".join(str(p.get("pregunta", "")).split()),
        version=int((d.get("meta") or {}).get("version", 1)),
    )


def main():
    _forzar_utf8()
    # los flags se ignoran: esto lo llama también el orquestador con su propio
    # argv (`--listar-perfiles`), y ahí lo que se quiere es el listado
    sueltos = [a for a in sys.argv[1:] if not a.startswith("-")]
    if sueltos:
        p = cargar_perfil(sueltos[0])
        print(f"── perfil: {p.nombre} ──")
        print(f"  {p.descripcion}")
        if p.pregunta:
            print(f"  pregunta: {p.pregunta}")
        print(f"  capas léxicas ({len(p.capas)}): {', '.join(sorted(p.capas))}")
        print(f"  andamiaje: {p.andamiaje}  (ablacion={p.ablacion})")
        print(f"  capas de score (FIJAS): {', '.join(sorted(p.capas_de_score))}")
        return
    print("── perfiles de run ──")
    for n in nombres():
        p = cargar_perfil(n)
        marca = " ←  por defecto" if n == PERFIL_POR_DEFECTO else ""
        print(f"  {n:<16} {len(p.capas)} capa(s), andamiaje {p.andamiaje}{marca}")
        print(f"                   {p.descripcion[:78]}")


if __name__ == "__main__":
    main()
