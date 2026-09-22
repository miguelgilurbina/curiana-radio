#!/usr/bin/env python3
"""¿Qué de la PERSONA cambia cuando cambia la semilla del run?

Una cadena `--continuar` corre cada día con su semilla (la serie C: 21, 22, 23).
`curiana_koine.fijar_semilla()` fija con ella el dado de lo que se DERIVA de la
ficha de cada agente: sus formas-semilla de idiolecto y el aspecto de respaldo
de su emocionar. Eso es un rasgo de la persona, no del día. Este script mide
cuántos agentes cambian de rasgo al cambiar la semilla, y qué lee el agente.

No llama a la API ni a la base. Uso:

    python 6-fusion/scripts/medir_semilla_del_dia.py [--semillas 21 22 23]
"""
import argparse
import io
import os
import sys

os.environ["CURIANA_ELENCO"] = "era2"
SIM = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "curiana_sim"))
sys.path.insert(0, SIM)


def _forzar_utf8():
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(flujo.buffer, encoding="utf-8",
                                                  errors="replace", line_buffering=True))


def foto(K, agentes, semilla):
    K.fijar_semilla(semilla)
    return {
        "bloque [Tu emocionar] (lo que el agente LEE)":
            {n: K.prompt_emocionar(n, a.get("etnia")) for n, a in agentes.items()},
        "formas-semilla del idiolecto":
            {n: tuple(K.formas_semilla(n, K.emocionar_de(n, a.get("etnia"))))
             for n, a in agentes.items()},
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--semillas", nargs="+", type=int, default=[21, 22, 23])
    args = ap.parse_args(argv)

    import curiana_koine as K
    from curiana_agents import ALL_AGENTS

    base, *resto = args.semillas
    fotos = {s: foto(K, ALL_AGENTS, s) for s in args.semillas}
    print(f"elenco: {len(ALL_AGENTS)} agentes · semilla de referencia (día 1): {base}\n")
    for rasgo in fotos[base]:
        for s in resto:
            distintos = [n for n in ALL_AGENTS if fotos[base][rasgo][n] != fotos[s][rasgo][n]]
            print(f"{rasgo}: cambia en {len(distintos)} de {len(ALL_AGENTS)} "
                  f"entre la semilla {base} y la {s}")
        print()
    rasgo = "bloque [Tu emocionar] (lo que el agente LEE)"
    cambian = [n for n in ALL_AGENTS
               if any(fotos[base][rasgo][n] != fotos[s][rasgo][n] for s in resto)]
    print(f"agentes a los que les cambia el bloque: {', '.join(cambian) or '—'}")
    for n in cambian[:3]:
        print(f"\n  {n}")
        for s in args.semillas:
            print(f"    semilla {s}: {fotos[s][rasgo][n]}")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
