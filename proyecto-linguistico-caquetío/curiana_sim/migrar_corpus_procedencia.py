#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — llevar el corpus de `referencia` en prosa a `procedencia.obra`
========================================================================

Los 161 hechos de `3-mundo/corpus/` citan su fuente en un campo de **texto
libre**:

    referencia: "Oliver 1989, cap. 3, pp. 255-256, 268 (\"the office of chief…\")"

Eso no se puede comprobar. Cognados y topónimos ya usan `procedencia.obra`, una
clave foránea contra `4-fuentes/bibliografia.yaml`, y el validador la verifica.
El corpus es la esfera grande que falta.

CÓMO LO DEDUCE, Y POR QUÉ NO SE FÍA
-----------------------------------
Busca en la `referencia` los patrones de cada obra (apellido del autor + sus
`aliases`, tomados de la bibliografía). Y entonces:

- **exactamente una obra coincide** → propone `procedencia: {obra: <id>}`
- **varias coinciden** → NO decide. Una referencia como *"Oviedo y Baños 1855:27,
  vía Zavala Reyes 2015 p.60"* cita dos obras con papeles distintos (la fuente
  última y el intermediario), y elegir por frecuencia sería inventar.
- **ninguna coincide** → lo deja y lo cuenta

**El campo `referencia` no se toca.** La prosa dice cosas que un id no puede
—página, cita textual, "vía tal"— y se conserva entera. `procedencia` se añade
al lado: uno es para leer, el otro para comprobar.

Uso:
    python migrar_corpus_procedencia.py            # simulacro
    python migrar_corpus_procedencia.py --aplicar
    python migrar_corpus_procedencia.py --ambiguos # los que citan varias obras
"""

import argparse
import io
import os
import re
import sys
from collections import Counter, defaultdict

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
CORPUS = os.path.join(REPO, "3-mundo", "corpus")
BIBLIOGRAFIA = os.path.join(REPO, "4-fuentes", "bibliografia.yaml")

# Un patrón de menos de 5 caracteres engancha con cualquier cosa. Medido: con
# umbral 4, "Adam" aparecía dentro de otras palabras.
MIN_PATRON = 5


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def patrones_por_obra():
    with open(BIBLIOGRAFIA, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    salida = {}
    for o in doc["obras"]:
        claves = set()
        apellido = str(o.get("autor", "")).split(",")[0].strip()
        if len(apellido) >= MIN_PATRON and apellido.lower() != "varios":
            claves.add(apellido)
        for alias in o.get("aliases") or []:
            alias = str(alias).strip()
            if len(alias) >= MIN_PATRON:
                claves.add(alias)
        if claves:
            salida[o["id"]] = claves
    return salida


def obras_citadas(texto: str, patrones) -> list:
    if not texto:
        return []
    bajo = texto.lower()
    return sorted(oid for oid, claves in patrones.items()
                  if any(k.lower() in bajo for k in claves))


def recorrer(datos):
    """Genera (contenedor, indice, hecho) para cualquier forma de raíz."""
    if isinstance(datos, list):
        for i, h in enumerate(datos):
            if isinstance(h, dict):
                yield datos, i, h
    elif isinstance(datos, dict):
        for valor in datos.values():
            if isinstance(valor, list):
                for i, h in enumerate(valor):
                    if isinstance(h, dict):
                        yield valor, i, h


def analizar():
    patrones = patrones_por_obra()
    resultado = defaultdict(list)   # archivo -> [(id, obras_citadas)]
    for nombre in sorted(os.listdir(CORPUS)):
        if not nombre.endswith(".yaml") or nombre == "genealogia.yaml":
            continue
        with open(os.path.join(CORPUS, nombre), encoding="utf-8") as fh:
            datos = yaml.safe_load(fh)
        for _, _, h in recorrer(datos):
            if "fuente" not in h:
                continue
            citadas = obras_citadas(str(h.get("referencia", "")), patrones)
            resultado[nombre].append((h.get("id"), citadas, h.get("procedencia")))
    return resultado


# Inicio de una entrada del corpus: "- id: parentesco-001"
_RE_ID = re.compile(r"^(\s*)-\s+id:\s*(\S+)\s*$")
# Cualquier clave al nivel de la entrada: "  fuente: …", "  dominios:"
_RE_CLAVE = re.compile(r"^(\s*)([a-z_]+):")


def aplicar():
    """Inserta `procedencia` **como texto**, sin round-trip de YAML.

    Cargar y volver a volcar con `yaml.safe_dump` reformatea el archivo entero:
    los bloques `>` de `contenido` se vuelven cadenas entrecomilladas y los
    comentarios de cabecera desaparecen. Sobre datos de investigación curados
    eso es inaceptable — el YAML se lee, no solo se parsea.

    Así que se localiza la línea de `referencia:` de cada entrada migrable y se
    inserta el bloque justo después de que termine, respetando la indentación y
    dejando el resto del archivo byte a byte.
    """
    patrones = patrones_por_obra()
    tocados = Counter()

    for nombre in sorted(os.listdir(CORPUS)):
        if not nombre.endswith(".yaml") or nombre == "genealogia.yaml":
            continue
        ruta = os.path.join(CORPUS, nombre)
        with open(ruta, encoding="utf-8") as fh:
            datos = yaml.safe_load(fh)
        with open(ruta, encoding="utf-8") as fh:
            lineas = fh.read().splitlines(keepends=True)

        # id → obra, solo para los inequívocos y sin procedencia previa.
        destino = {}
        for _, _, h in recorrer(datos):
            if "fuente" not in h or h.get("procedencia") is not None:
                continue
            citadas = obras_citadas(str(h.get("referencia", "")), patrones)
            if len(citadas) == 1:
                destino[h.get("id")] = citadas[0]
        if not destino:
            continue

        salida = []
        actual = None       # id de la entrada que se está recorriendo
        sangria = "  "
        i = 0
        while i < len(lineas):
            linea = lineas[i]
            salida.append(linea)

            m = _RE_ID.match(linea.rstrip("\n"))
            if m:
                actual = m.group(2)
                sangria = m.group(1) + "  "
                i += 1
                continue

            if actual in destino:
                mc = _RE_CLAVE.match(linea)
                if mc and mc.group(2) == "referencia":
                    # Consumir el valor completo: puede ocupar varias líneas si
                    # es un bloque o una cadena continuada.
                    j = i + 1
                    while j < len(lineas):
                        siguiente = lineas[j]
                        if not siguiente.strip():
                            break
                        mk = _RE_CLAVE.match(siguiente)
                        if mk and len(mk.group(1)) <= len(mc.group(1)):
                            break
                        if _RE_ID.match(siguiente.rstrip("\n")):
                            break
                        salida.append(siguiente)
                        j += 1
                    salida.append(f"{sangria}procedencia: {{obra: {destino[actual]}}}\n")
                    tocados[nombre] += 1
                    del destino[actual]
                    i = j
                    continue
            i += 1

        with open(ruta, "w", encoding="utf-8", newline="") as fh:
            fh.writelines(salida)
    return tocados


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--ambiguos", action="store_true")
    args = ap.parse_args(argv)

    resultado = analizar()
    unica = ambigua = ninguna = ya = 0
    ambiguos = []
    sin = []
    for archivo, filas in resultado.items():
        for hid, citadas, proc in filas:
            if proc:
                ya += 1
            elif len(citadas) == 1:
                unica += 1
            elif len(citadas) > 1:
                ambigua += 1
                ambiguos.append((archivo, hid, citadas))
            else:
                ninguna += 1
                sin.append((archivo, hid))

    total = unica + ambigua + ninguna + ya
    print(f"\n── Corpus: {total} hechos ──")
    print(f"  ya tienen procedencia      {ya:4d}")
    print(f"  citan UNA obra → migrables {unica:4d}")
    print(f"  citan VARIAS → decisión    {ambigua:4d}")
    print(f"  no citan obra conocida     {ninguna:4d}")

    if args.ambiguos:
        print("\n── Los que citan varias obras ──")
        print("  Casi siempre es «fuente última, vía intermediario»: son dos")
        print("  papeles distintos y elegir uno por frecuencia sería inventar.\n")
        for archivo, hid, citadas in ambiguos:
            print(f"  {hid:26} {', '.join(citadas)}")
        return 0

    if not args.aplicar:
        print("\n  ── SIMULACRO ── no se ha escrito nada.")
        print("     Aplicar:  python migrar_corpus_procedencia.py --aplicar")
        print("     Ver los ambiguos:  --ambiguos")
        if sin:
            print(f"\n  sin obra reconocible ({len(sin)}), muestra:")
            for archivo, hid in sin[:8]:
                print(f"     {hid}")
        return 0

    tocados = aplicar()
    print("\n  aplicado:")
    for archivo, n in sorted(tocados.items()):
        print(f"     {archivo:28} +{n}")
    print(f"\n  total migrados: {sum(tocados.values())}")
    print("  `referencia` NO se ha tocado: la prosa dice cosas que un id no puede.")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
