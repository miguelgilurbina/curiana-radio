#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — cuánto taíno hay ya en el motor, y cuánto en el registro del mundo
============================================================================

Campaña del taíno, parcela T5 (2026-09-21). Emite las cifras que cita
`6-fusion/taino_en_la_esfera_2026-09-21.yaml` y su issue. **Ninguna cifra de
esos documentos está escrita a mano** (regla 1): salen de aquí.

Mide cuatro cosas, y las cuatro son lecturas — no escribe nada:

1. **El cero del mundo.** ¿Aparece el taíno en `3-mundo/etnias.yaml`? Se
   comprueba con un barrido de ortografía (regla 6: un `grep` a cero mide tu
   consulta, no la fuente), incluyendo los nombres por los que podría estar
   escondido: «antillano», «arahuaco insular», «isleño», «lucayo», «Española».
   Se barre también `asentamientos.yaml` y `3-mundo/corpus/`, que **no** están
   a cero — y ahí está el punto: el taíno vive en el repo como comparanda y
   como estrato del lexicón, no como vecino.

2. **El taíno en el lexicón.** Cuántas voces lleva la etiqueta, y cuántas de
   ellas son de la `ESFERA_DE_CONTACTO` una vez normalizada la fuente
   (`taíno-reconstruido` normaliza a `taíno`: lo comprueba y lo dice, porque
   si dejara de hacerlo esas voces pasarían a PENALIZAR).

3. **El bloque `[Voces de fuera]`**, que es por donde el taíno entra al
   hablante: qué proporción del catálogo del tier 1 es taína.

4. **Lo que de verdad se dijo**, si el Supabase local está levantado:
   `loanword_uses` por lengua y por forma. Sin base, se salta y lo dice.

Uso:
    python 6-fusion/scripts/medir_taino_en_la_esfera.py
    python 6-fusion/scripts/medir_taino_en_la_esfera.py --sin-base
    python 6-fusion/scripts/medir_taino_en_la_esfera.py --json
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(_AQUI))
sys.path.insert(0, os.path.join(REPO, "curiana_sim"))

CONTENEDOR = "supabase_db_curiana_sim"

# Ortografías por las que el taíno podría estar en el registro del mundo sin
# llamarse «taíno». La lista es el paso 2 de la skill `minar-fuente`: raíz
# corta, sin acentos, y también los nombres de vecindad que usaría un cronista.
SONDAS = [
    "taín", "tain", "taino", "antillan", "antill", "arahuaco insular",
    "arahuacos insulares", "caribe insular", "isleñ", "lucay", "boriqu",
    "borinqu", "españ" + "ola", "hispaniol", "haití", "haiti", "cuba",
    "jamaica", "ostion", "chicoid", "meillac", "guanín", "guanin",
    "gigante", "santo domingo",
]

DIANAS = [
    ("3-mundo/etnias.yaml", "el registro de VECINOS — el que esta parcela dice que está a cero"),
    ("3-mundo/asentamientos.yaml", "el registro de NODOS"),
    ("3-mundo/corpus", "el corpus cultural (5 esferas)"),
]


def _forzar_utf8():
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def _textos(ruta_rel):
    """Devuelve [(ruta, texto)] del archivo o de todo el directorio."""
    ruta = os.path.join(REPO, ruta_rel)
    if os.path.isfile(ruta):
        candidatos = [ruta]
    else:
        candidatos = []
        for base, _, ficheros in os.walk(ruta):
            for f in sorted(ficheros):
                if f.endswith((".yaml", ".yml", ".md")):
                    candidatos.append(os.path.join(base, f))
    salida = []
    for c in candidatos:
        with open(c, encoding="utf-8", errors="replace") as fh:
            salida.append((os.path.relpath(c, REPO).replace("\\", "/"), fh.read()))
    return salida


def barrido_del_mundo():
    """Paso 1: el cero, verificado con ortografías (regla 6)."""
    informe = {}
    for ruta_rel, que_es in DIANAS:
        conteo = {}
        ejemplos = {}
        for ruta, texto in _textos(ruta_rel):
            bajo = texto.lower()
            for sonda in SONDAS:
                n = bajo.count(sonda)
                if n:
                    conteo[sonda] = conteo.get(sonda, 0) + n
                    ejemplos.setdefault(sonda, []).append(ruta)
        informe[ruta_rel] = {
            "que_es": que_es,
            "sondas_con_acierto": conteo,
            "donde": {k: sorted(set(v)) for k, v in ejemplos.items()},
            "total_aciertos": sum(conteo.values()),
        }
    return informe


def taino_en_el_lexicon():
    """Paso 2 y 3: la etiqueta en el lexicón y el bloque del tier 1."""
    import curiana_lexicon as L
    from curiana_database import normalize_source_language as norm

    base = L.VOCABULARIO_BASE
    etiquetas = {}
    for palabra, datos in base.items():
        fuente = str(datos.get("fuente", ""))
        if norm(fuente) == "taíno":
            etiquetas.setdefault(fuente, []).append(palabra)

    esfera = {}
    for palabra, datos in base.items():
        fam = norm(str(datos.get("fuente", "")))
        if fam in L.ESFERA_DE_CONTACTO:
            esfera.setdefault(fam, []).append(palabra)

    voces = L.voces_de_fuera_posibles()
    por_lengua = {}
    for _, forma, glosa, fam in voces:
        por_lengua.setdefault(fam, []).append(forma)

    return {
        "vocabulario_base": len(base),
        "etiquetas_taino": {k: len(v) for k, v in sorted(etiquetas.items())},
        "taino_total": sum(len(v) for v in etiquetas.values()),
        "normaliza_taino_reconstruido": norm("taíno-reconstruido") == "taíno",
        "esfera_de_contacto": sorted(L.ESFERA_DE_CONTACTO),
        "voces_de_esfera_en_base": {k: len(v) for k, v in sorted(esfera.items())},
        "voces_de_esfera_total": sum(len(v) for v in esfera.values()),
        "voces_de_fuera_total": len(voces),
        "voces_de_fuera_por_lengua": {k: len(v) for k, v in sorted(por_lengua.items())},
        "voces_de_fuera_tainas": sorted(por_lengua.get("taíno", [])),
        "forma_de_la_esfera": dict(L.FORMA_DE_LA_ESFERA),
        "sin_forma_de_la_esfera": sorted(L.SIN_FORMA_DE_LA_ESFERA),
    }


def _psql(sql):
    try:
        salida = subprocess.run(
            ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d",
             "postgres", "-t", "-A", "-c", sql],
            capture_output=True, text=True, encoding="utf-8", timeout=45)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return None, f"{type(e).__name__}: {e}"
    if salida.returncode != 0:
        return None, (salida.stderr or "").strip()[:300]
    filas = [l for l in (salida.stdout or "").splitlines() if l.strip()]
    return [f.split("|") for f in filas], None


def lo_que_se_dijo():
    """Paso 4: `loanword_uses`. Un cero aquí también hay que verificarlo."""
    por_lengua, err = _psql(
        "SELECT source_language, count(*), count(DISTINCT word) "
        "FROM loanword_uses GROUP BY 1 ORDER BY 2 DESC;")
    if err is not None:
        return {"disponible": False, "motivo": err}
    por_forma, _ = _psql(
        "SELECT word, source_language, tier, count(*) FROM loanword_uses "
        "GROUP BY 1,2,3 ORDER BY 4 DESC;")
    total, _ = _psql("SELECT count(*), count(DISTINCT run_id) FROM loanword_uses;")
    viejo, _ = _psql(
        "SELECT count(*) FROM word_uses WHERE source_language = 'taíno';")
    return {
        "disponible": True,
        "loanword_uses_filas": int(total[0][0]) if total else None,
        "loanword_uses_runs": int(total[0][1]) if total else None,
        "por_lengua": [{"lengua": f[0], "usos": int(f[1]), "formas": int(f[2])}
                       for f in (por_lengua or [])],
        "por_forma": [{"forma": f[0], "lengua": f[1], "tier": f[2], "usos": int(f[3])}
                      for f in (por_forma or [])],
        "word_uses_taino_residuo": int(viejo[0][0]) if viejo else None,
    }


def imprimir(datos):
    print("═" * 72)
    print("  EL TAÍNO EN LA ESFERA — medición T5, campaña del taíno")
    print("═" * 72)

    print("\n1. EL CERO DEL MUNDO (regla 6: verificado con ortografías)\n")
    for ruta, info in datos["mundo"].items():
        estado = "CERO" if info["total_aciertos"] == 0 else f"{info['total_aciertos']} acierto(s)"
        print(f"  {ruta}  —  {estado}")
        print(f"     ({info['que_es']})")
        for sonda, n in sorted(info["sondas_con_acierto"].items(), key=lambda kv: -kv[1]):
            donde = ", ".join(info["donde"][sonda][:3])
            print(f"       {sonda:22s} {n:4d}   {donde}")
        print()

    lex = datos["lexicon"]
    print("2. EL TAÍNO EN EL LEXICÓN\n")
    print(f"  VOCABULARIO_BASE                {lex['vocabulario_base']}")
    for etiqueta, n in lex["etiquetas_taino"].items():
        print(f"    {etiqueta:26s}  {n}")
    print(f"    {'TOTAL familia taína':26s}  {lex['taino_total']}")
    print(f"  `taíno-reconstruido` normaliza a `taíno`: {lex['normaliza_taino_reconstruido']}")
    print(f"    (si dejara de hacerlo, esas voces saldrían de ESFERA_DE_CONTACTO")
    print(f"     y pasarían a PENALIZAR como fuga a otra lengua arahuaca)")
    print(f"  voces de la esfera en base      {lex['voces_de_esfera_total']}")
    for fam, n in lex["voces_de_esfera_en_base"].items():
        print(f"    {fam:26s}  {n}")

    print("\n3. EL BLOQUE [Voces de fuera] — por donde el taíno llega al tier 1\n")
    print(f"  catálogo                        {lex['voces_de_fuera_total']}")
    for fam, n in sorted(lex["voces_de_fuera_por_lengua"].items(), key=lambda kv: -kv[1]):
        pct = 100.0 * n / lex["voces_de_fuera_total"]
        print(f"    {fam:26s}  {n:3d}   {pct:5.1f} %")
    print(f"  taínas: {', '.join(lex['voces_de_fuera_tainas'])}")
    print(f"  no se enseñan (SIN_FORMA_DE_LA_ESFERA): {', '.join(lex['sin_forma_de_la_esfera'])}")

    base = datos["base"]
    print("\n4. LO QUE SE DIJO (loanword_uses)\n")
    if not base.get("disponible"):
        print(f"  base no disponible — {base.get('motivo')}")
    else:
        print(f"  filas {base['loanword_uses_filas']}  ·  runs {base['loanword_uses_runs']}")
        for f in base["por_lengua"]:
            print(f"    {f['lengua']:22s}  {f['usos']:4d} usos  {f['formas']:3d} formas")
        print(f"  residuo en word_uses con source_language='taíno': "
              f"{base['word_uses_taino_residuo']} (runs anteriores al corte del 2026-09-16)")
    print()


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sin-base", action="store_true",
                    help="no consulta el Supabase local")
    ap.add_argument("--json", action="store_true", help="el informe en JSON")
    args = ap.parse_args()

    datos = {
        "mundo": barrido_del_mundo(),
        "lexicon": taino_en_el_lexicon(),
        "base": {"disponible": False, "motivo": "--sin-base"} if args.sin_base else lo_que_se_dijo(),
    }
    if args.json:
        print(json.dumps(datos, ensure_ascii=False, indent=2))
    else:
        imprimir(datos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
