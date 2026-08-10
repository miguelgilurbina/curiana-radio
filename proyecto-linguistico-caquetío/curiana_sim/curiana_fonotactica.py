#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — fonotáctica del caquetío atestiguado
==============================================

Deriva un filtro de forma **solo** del subconjunto atestiguado del lexicón y
mide cuánto deja pasar de cada otra fuente. Es la primera mitad del issue #91
("cerrar el inventario"), y su resultado principal es **negativo**.

EL RESULTADO, ANTES QUE NADA
----------------------------
#91 quería cerrar la fonotáctica para impedir que el modelo "rellenara" con
arahuaco genérico. **No sirve para eso.** Medido:

    CQ-ATT (control)   100.0 % pasa
    caquetío-reconstr.  98.5 %
    taíno               94.4 %
    wayunaiki           86.3 %   <-- la fuente de contaminación principal
    lokono              79.8 %
    castellano          44.7 %

El filtro bloquea **el 55 % del castellano y solo el 14 % del wayunaiki**. Es
un **detector de castellano**, no de arahuaco genérico: el wayunaiki ya
satisface la fonotáctica caquetía porque ambas lenguas son abrumadoramente CV.

Sigue valiendo la pena tenerlo —el castellano ES una vía de contaminación
real y barata de detectar— pero **el control de validez de la fase 2 tiene que
ser morfológico y léxico**, no fonotáctico. Ver `2-lengua/fonotactica.md`.

DOS ADVERTENCIAS SOBRE EL DATO
------------------------------
1. **La ortografía no es la fonología.** El caquetío atestiguado está
   transcrito en ortografía castellana colonial (`c`, `qu`, `z`, `gua`) y el
   reconstruido en ortografía lingüística (`k`, `w`, `ü`). Sin normalizar, lo
   que se mide es el transcriptor. `fonemizar()` normaliza; sus reglas están
   abajo, cada una con su porqué, y **no** pretenden resolver D5 (#36).

2. **El conjunto atestiguado tiene residuo castellano**, y ensancha el filtro:
   `caquetillo` y `casquito` llevan diminutivo castellano (`-illo`, `-ito`);
   `bagre` y `barbasco` son palabras castellanas. Cada una mete su cluster
   (`sk`, `gr`, `ll`) en el inventario "atestiguado" y hace el filtro más
   permisivo. Limpiarlas lo haría más estricto — ver el issue de fidelidad.

Uso:
    python curiana_fonotactica.py            # el informe medido
    python curiana_fonotactica.py --json
"""

import argparse
import io
import json
import re
import sys
import unicodedata
from collections import Counter

VOCALES = frozenset("aeiouü")

# ── Normalización ortográfica ────────────────────────────────────────────
# El mínimo para poder comparar dos corpus escritos con convenciones
# distintas. NO es una decisión sobre la ortografía del proyecto (D5, #36):
# es una capa de medición, y se aplica a todo por igual.
REGLAS_ORTOGRAFICAS = [
    (r"qu(?=[ei])", "k",  "castellano: <qu> ante e/i vale /k/"),
    (r"gu(?=[ei])", "g",  "castellano: <gu> ante e/i vale /g/"),
    (r"c(?=[ei])",  "s",  "castellano: <ce>/<ci> vale /s/ (seseo americano)"),
    (r"c",          "k",  "el resto de <c> vale /k/"),
    (r"q",          "k",  "<q> sin <u> también es /k/"),
    (r"z",          "s",  "seseo: <z> no contrasta con <s> en América"),
    (r"v",          "b",  "betacismo: <v> y <b> no contrastan"),
    (r"h",          "",   "<h> castellana es muda"),
    (r"y(?![aeiou])", "i", "<y> sin vocal detrás es vocálica"),
    (r"x",          "sh", "<x> colonial suele valer /ʃ/"),
]

_TILDES = str.maketrans("áéíóú", "aeiou")

# ⚠️ CUESTIÓN ABIERTA, deliberadamente NO resuelta aquí.
# `gua`/`güe` en transcripción colonial puede valer /gwa/ o simplemente /wa/:
# `guaitiao` es el taíno *waitiao*, y ahí <gu> es claramente /w/. De las 50
# formas atestiguadas con <g>, la mayoría son `gua-`/`güe-`. Si la regla
# fuera <gu> → /w/, el fonema /g/ casi desaparecería del inventario.
# Se deja medible con `gu_es_w=True` en vez de decidirlo por la puerta de atrás.
GU_ES_W = (r"g[uü](?=[aeio])", "w")


def fonemizar(forma: str, gu_es_w: bool = False) -> str:
    """Lleva una forma escrita a un esqueleto fonémico comparable.

    `gu_es_w` activa la regla abierta de arriba. Por defecto **no** se aplica:
    cambiar el inventario por una regla no decidida sería exactamente el tipo
    de decisión silenciosa que el proyecto evita.
    """
    f = unicodedata.normalize("NFC", (forma or "").lower())
    f = re.sub(r"[^a-záéíóúüïöñ]", "", f).translate(_TILDES)
    f = f.replace("ï", "i").replace("ö", "o")
    if gu_es_w:
        f = re.sub(GU_ES_W[0], GU_ES_W[1], f)
    for patron, reemplazo, _porque in REGLAS_ORTOGRAFICAS:
        f = re.sub(patron, reemplazo, f)
    return f


def clusters(forma: str):
    """Los grupos de dos o más consonantes seguidas."""
    return [m.group() for m in re.finditer(r"[^aeiouü]{2,}", forma)]


# ── El filtro ────────────────────────────────────────────────────────────

class Fonotactica:
    """Inventario, clusters y codas derivados de un conjunto de formas.

    Se construye **solo** con el caquetío atestiguado: si se entrenara con
    todo el lexicón, el 55 % sería wayunaiki y el filtro no diría nada sobre
    el caquetío.
    """

    def __init__(self, formas, gu_es_w: bool = False):
        self.gu_es_w = gu_es_w
        self.base = [f for f in (fonemizar(x, gu_es_w) for x in formas) if f]
        self.inventario = frozenset(c for f in self.base for c in f)
        self.clusters = frozenset(c for f in self.base for c in clusters(f))
        self.codas = frozenset(f[-1] for f in self.base if f[-1] not in VOCALES)

    def valida(self, forma: str):
        """Devuelve `(ok, motivos)`. `motivos` es una lista, no un bool."""
        f = fonemizar(forma, self.gu_es_w)
        motivos = []
        if not f:
            return False, ["vacía tras normalizar"]

        fuera = sorted(set(f) - self.inventario)
        if fuera:
            motivos.append(f"letras fuera del inventario: {', '.join(fuera)}")

        malos = sorted({c for c in clusters(f) if c not in self.clusters})
        if malos:
            motivos.append(f"clusters no atestiguados: {', '.join(malos)}")

        if f[-1] not in VOCALES and f[-1] not in self.codas:
            motivos.append(f"coda final no atestiguada: -{f[-1]}")

        return not motivos, motivos

    def tasa_de_violacion(self, formas):
        """La métrica que la fase 2 quiere: qué fracción viola el inventario.

        Aplicada a la salida de un agente, dice cuánto está inventando fuera
        de la forma caquetía. Aplicada a otra lengua, dice cuánto discrimina
        el filtro — que es como se midió el resultado negativo de arriba.
        """
        formas = [f for f in formas if f]
        if not formas:
            return 0.0
        malas = sum(1 for f in formas if not self.valida(f)[0])
        return malas / len(formas)


# ── Medición contra el lexicón ───────────────────────────────────────────

FAMILIAS = {
    "caquetío-atestiguado": "caquetío atestiguado",
    "caquetío": "caquetío atestiguado",
    "caquetío-reconstruido": "caquetío reconstruido",
    "wayunaiki": "wayunaiki",
    "lokono": "lokono",
    "taíno": "taíno",
    "taino": "taíno",
}

# Control externo: castellano corriente. No es una muestra representativa del
# idioma, es un termómetro — si el filtro no distingue esto, no distingue nada.
CASTELLANO = (
    "casa perro tierra hombre mujer agua fuego viento noche dia sol luna mar "
    "rio monte piedra arbol flor pescado carne sangre corazon cabeza mano pie "
    "padre madre hijo hermano pueblo camino trabajo palabra verdad muerte vida "
    "grande pequeno blanco negro rojo verde comer beber dormir andar hablar"
).split()


def _grupos_del_lexicon():
    from curiana_lexicon import VOCABULARIO_BASE
    grupos = {}
    for forma, entrada in VOCABULARIO_BASE.items():
        familia = FAMILIAS.get(entrada.get("fuente"))
        if familia:
            grupos.setdefault(familia, []).append(forma)
    return grupos


def medir(gu_es_w: bool = False):
    """Construye el filtro con lo atestiguado y mide qué deja pasar."""
    grupos = _grupos_del_lexicon()
    atestiguado = grupos.get("caquetío atestiguado", [])
    fono = Fonotactica(atestiguado, gu_es_w=gu_es_w)

    paso = {}
    for familia, formas in grupos.items():
        paso[familia] = 1.0 - fono.tasa_de_violacion(formas)
    paso["castellano (control)"] = 1.0 - fono.tasa_de_violacion(CASTELLANO)
    return fono, paso


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace",
                line_buffering=True))


def informe(gu_es_w: bool = False) -> None:
    fono, paso = medir(gu_es_w)
    print(f"\n── fonotáctica del caquetío atestiguado ── "
          f"{len(fono.base)} formas base"
          f"{'  [gu→w activado]' if gu_es_w else ''}\n")
    print(f"  inventario ({len(fono.inventario)}): "
          f"{''.join(sorted(fono.inventario))}")
    print(f"  clusters ({len(fono.clusters)}): {', '.join(sorted(fono.clusters))}")
    print(f"  codas finales: {', '.join(sorted(fono.codas)) or '(ninguna)'}")

    print("\n  cuánto deja pasar:\n")
    for familia, pct in sorted(paso.items(), key=lambda kv: -kv[1]):
        barra = "█" * int(pct * 30)
        print(f"    {familia:24} {100*pct:5.1f}%  {barra}")

    wy = paso.get("wayunaiki", 0)
    es = paso.get("castellano (control)", 0)
    print(f"\n  Bloquea el {100*(1-es):.0f}% del castellano y solo el "
          f"{100*(1-wy):.0f}% del wayunaiki.")
    print("  → es un detector de castellano, no de arahuaco genérico.")
    print("  → el control de validez de la fase 2 tiene que ser "
          "morfológico y léxico.\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="el informe en JSON")
    ap.add_argument("--gu-es-w", action="store_true",
                    help="aplica la regla abierta <gu> → /w/ y remide")
    args = ap.parse_args(argv)

    if args.json:
        fono, paso = medir(args.gu_es_w)
        print(json.dumps({
            "formas_base": len(fono.base),
            "inventario": sorted(fono.inventario),
            "clusters": sorted(fono.clusters),
            "codas": sorted(fono.codas),
            "pasa": {k: round(v, 4) for k, v in paso.items()},
        }, ensure_ascii=False, indent=2))
    else:
        informe(args.gu_es_w)
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.path.insert(0, __file__.rsplit("curiana_fonotactica.py", 1)[0] or ".")
    sys.exit(main())
