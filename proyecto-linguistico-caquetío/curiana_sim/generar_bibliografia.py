#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — la bibliografía, generada desde las notas de fuente
=============================================================

Emite `4-fuentes/bibliografia.yaml`: **un registro por obra**, con su id
estable, y nada más que lo que hace falta para citarla.

POR QUÉ
-------
Hasta ahora las notas de `4-fuentes/` eran dos cosas a la vez: la ficha de la
obra **y** el almacén de todo lo que se le había sacado. Eso ordena el
conocimiento por *de dónde vino* en lugar de por *de qué trata*, y tiene dos
consecuencias feas:

1. Un hallazgo de ecología acaba viviendo en `oliver-1989-cap3.md` en vez de en
   ecología, así que para saber qué sabemos de ecología hay que leer las 30
   notas.
2. No hay forma de comprobar que una cita apunta a una obra que existe: la
   `referencia` es texto libre.

Con la bibliografía separada, **`obra` pasa a ser una clave foránea**: cada
hecho del corpus, cada entrada del lexicón, cada cognado y cada topónimo pueden
citar un id, y el validador comprueba que resuelva. La cita deja de ser una
promesa y pasa a ser una comprobación.

QUÉ NO HACE
-----------
No borra ni adelgaza las notas. Se genera **desde** su frontmatter, así que no
inventa nada y no se pierde nada. Las notas siguen siendo la bitácora de la
minería —qué se preguntó, qué se halló, qué no— que es prosa y debe seguir
siéndolo.

`sostiene` **no se copia**: es un campo que se mantenía a mano y derivaba.
Lo calcula `medir_sostiene.py` contando lo que cada obra cita de verdad.

Uso:
    python generar_bibliografia.py            # escribe el YAML
    python generar_bibliografia.py --stdout
    python generar_bibliografia.py --check    # exit 1 si el de disco está viejo
"""

import argparse
import io
import os
import re
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
FUENTES = os.path.join(REPO, "4-fuentes")
SALIDA = os.path.join(FUENTES, "bibliografia.yaml")

_FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)

# Lo que se copia de la nota, en este orden. Todo lo demás —cobertura, tareas,
# prioridad, estado de minado— es *estado de trabajo*, no cita, y se queda en
# la nota.
CAMPOS_CITA = ("obra", "autor", "anio", "publicacion", "edicion_del_ejemplar",
               "genero", "local", "paginas", "acceso", "aliases")


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        m = _FM.match(fh.read())
    if not m:
        return {}
    datos = yaml.safe_load(m.group(1))
    return datos if isinstance(datos, dict) else {}


def recolectar():
    """Un registro por nota con `tipo: fuente`, ordenados por id."""
    obras = []
    for nombre in sorted(os.listdir(FUENTES)):
        if not nombre.endswith(".md") or nombre == "INDICE_FUENTES.md":
            continue
        fm = frontmatter(os.path.join(FUENTES, nombre))
        if fm.get("tipo") != "fuente":
            continue

        registro = {"id": nombre[:-3]}
        for campo in CAMPOS_CITA:
            if campo in fm and fm[campo] not in (None, "", []):
                registro[campo] = fm[campo]

        # `local` puede ser cadena o lista; se normaliza a lista para que el
        # consumidor no tenga que preguntarse cuál de las dos le tocó.
        if "local" in registro and isinstance(registro["local"], str):
            registro["local"] = [registro["local"]]

        # Una obra sin archivo en el repo es una obra citable igual: se marca
        # en vez de omitirla, porque 27 hechos del corpus dependen de esas.
        registro["en_repo"] = bool(registro.get("local"))
        obras.append(registro)
    return obras


def documento(obras):
    return {
        "meta": {
            "generado_por": "curiana_sim/generar_bibliografia.py",
            "obras": len(obras),
            "en_repo": sum(1 for o in obras if o["en_repo"]),
            "solo_citadas": sum(1 for o in obras if not o["en_repo"]),
            "nota": ("Generado desde el frontmatter de 4-fuentes/*.md. No editar "
                     "a mano: se edita la nota y se regenera. El `id` es la clave "
                     "que citan el corpus, el lexicón, los cognados y los topónimos."),
        },
        "obras": obras,
    }


def volcar(doc) -> str:
    return yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                          default_flow_style=False, width=100)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 si el archivo de disco no coincide")
    args = ap.parse_args(argv)

    obras = recolectar()
    texto = volcar(documento(obras))

    if args.stdout:
        print(texto)
        return 0

    if args.check:
        if not os.path.exists(SALIDA):
            print("  ✗ bibliografia.yaml no existe")
            return 1
        with open(SALIDA, encoding="utf-8") as fh:
            if fh.read() != texto:
                print("  ✗ bibliografia.yaml está viejo — regenéralo")
                return 1
        print(f"  ✓ bibliografia.yaml al día ({len(obras)} obras)")
        return 0

    with open(SALIDA, "w", encoding="utf-8") as fh:
        fh.write(texto)
    en_repo = sum(1 for o in obras if o["en_repo"])
    print(f"  → {os.path.relpath(SALIDA, REPO)}: {len(obras)} obras "
          f"({en_repo} con archivo, {len(obras) - en_repo} solo citadas)")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
