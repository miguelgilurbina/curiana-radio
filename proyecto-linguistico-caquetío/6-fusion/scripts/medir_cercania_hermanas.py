# -*- coding: utf-8 -*-
"""¿Qué hermana está más cerca del caquetío ATESTIGUADO? — con el kalinago
partido en habla de mujeres y habla de hombres (2026-09-23).

Miguel, 2026-09-23: «¿Kalinago femenino es el habla más cercana y con más
parentesco comprobado de todos? Si es así creo que preferiría usarlo de
referencia, cambiando todo lo que tenemos lokono por Kalinago, o al menos
poder medirlo».

Es el cómputo A de D11 (`curiana_sim/computo_d11.py`, 2026-08-31: las 24
formas atestiguadas de concepto directo contra la Tabla A-2 de Oliver) con
cuatro columnas más:

  - `kal_mujeres` y `kal_hombres`: Goeje 1939 (que sigue a Breton) leído en
    imagen. En la A-2 el caribe insular de Oliver no separa registros y marca
    «CARIB» donde la voz corriente es caribe: por eso el 31-08 no vio el `kaši`
    de las mujeres. Aquí cada columna es lo que DICE ese registro: su forma
    propia si la tiene, y la común si no (entonces las dos columnas coinciden y
    ninguna gana).
  - `achagua` (Neira y Ribero 1762) y `taino` (lista maestra, sólo con
    cronista): dos de las tres hermanas que Miguel nombró, que la A-2 no trae.

La métrica es la del 31-08, tal cual: similitud = 1 − Levenshtein/longitud
máxima sobre la fonemización D5, la mejor variante de cada celda. Aquí NO se
elige «ganadora» por margen (con dos columnas kalinago que coinciden en la voz
común el margen se anula y el desempate dependía del orden de las columnas):
se cuenta, por lengua, en cuántos conceptos tiene forma, en cuántos se parece
(≥ 0,50) y la media; y el cara a cara de cada hermana contra el kalinago de
mujeres, concepto por concepto.

Uso (desde proyecto-linguistico-caquetío/):
    python 6-fusion/scripts/medir_cercania_hermanas.py --salida 6-fusion/medicion_cercania_hermanas_2026-09-23.yaml
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import unicodedata
from pathlib import Path

R = Path(__file__).resolve().parents[2]


# ── fonemización D5 y similitud: las de computo_d11.py, copiadas tal cual ──
def fonemizar(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z]", "", s)
    s = re.sub(r"gu(?=[aeio])", "w", s)
    s = re.sub(r"qu(?=[ei])", "k", s)
    s = re.sub(r"c(?=[ei])", "s", s)
    s = s.replace("ch", "C")
    s = s.replace("c", "k").replace("C", "ch")
    s = s.replace("z", "s").replace("v", "b")
    s = s.replace("kh", "k").replace("th", "t").replace("dh", "d")
    return s


def variantes(celda: str) -> list[str]:
    if not celda or celda.startswith(("---", "SPANISH", "CARIB", "KARIB", "AFRICANISM", "vid")):
        return []
    celda = re.sub(r"\([^)]*\)", "", celda)
    out = []
    for trozo in re.split(r"[/·]", celda):
        t = trozo.strip().strip("*").strip("-")
        t = re.sub(r"^(nu|n|hu|ua|wa|p|t)-", "", t)
        t = t.replace("'", "").replace("^", "")
        t = fonemizar(t)
        if len(t) >= 2:
            out.append(t)
    return out


def lev(a: str, b: str) -> int:
    m, n = len(a), len(b)
    fila = list(range(n + 1))
    for i in range(1, m + 1):
        prev, fila[0] = fila[0], i
        for j in range(1, n + 1):
            prev, fila[j] = fila[j], min(fila[j] + 1, fila[j - 1] + 1, prev + (a[i - 1] != b[j - 1]))
    return fila[n]


def sim(a: str, b: str) -> float:
    return 0.0 if not a or not b else 1.0 - lev(a, b) / max(len(a), len(b))


# ── la Tabla A-2 (Oliver 1989 pp. 561-565), las celdas que usó computo_d11 ──
A2 = {
 "moon":     {"guajiro": "kashi'", "paraujano": "keichare", "lokono": "kathi", "ic_oliver": "hati", "maipure": "keyapi"},
 "sun":      {"guajiro": "kai'", "paraujano": "kai/kei", "lokono": "hadali", "ic_oliver": "CARIB", "maipure": "kie"},
 "stone":    {"guajiro": "ipa", "paraujano": "ipah", "lokono": "siba/-siban", "ic_oliver": "CARIB", "maipure": "kipa"},
 "sand":     {"guajiro": "jasai/wule'shi/muaku", "paraujano": "mo", "lokono": "mothoko", "ic_oliver": "CARIB", "maipure": "kaina"},
 "woman":    {"guajiro": "erruni/jie'rru/eiyetse", "paraujano": "hniere/ñerika/añukar", "lokono": "hiaro", "ic_oliver": "hiaru", "maipure": "---"},
 "man":      {"guajiro": "tolo/achini/t-echin", "paraujano": "eichire", "lokono": "oadili", "ic_oliver": "eieri/*iñeri", "maipure": "kayarrikini"},
 "tooth":    {"guajiro": "aiua/ali", "paraujano": "tai", "lokono": "arii/-ari/*dari", "ic_oliver": "-ari", "maipure": "n-ati"},
 "path":     {"guajiro": "wopu'/apu'na", "paraujano": "wobu", "lokono": "oaboroko/abonaha", "ic_oliver": "CARIB", "maipure": "anepu"},
 "one":      {"guajiro": "wane", "paraujano": "manei", "lokono": "aba-", "ic_oliver": "abana", "maipure": "piau/pakiata"},
 "two":      {"guajiro": "piama", "paraujano": "pimu/pimi", "lokono": "biama/bian", "ic_oliver": "biama", "maipure": "pina"},
 "root":     {"guajiro": "ourrala", "paraujano": "---", "lokono": "iikirahi/-ikira", "ic_oliver": "-ilagola", "maipure": "---"},
 "hear":     {"guajiro": "apa", "paraujano": "---", "lokono": "kanabon/*kanabun", "ic_oliver": "agaba", "maipure": "---"},
 "blood":    {"guajiro": "asha/isha'", "paraujano": "---", "lokono": "ithihi/-china", "ic_oliver": "hitao/-ita", "maipure": "---"},
 "big":      {"guajiro": "muleu", "paraujano": "youghe", "lokono": "firo/fili-", "ic_oliver": "uairi", "maipure": "---"},
 "mountain": {"guajiro": "uchi/kochooshi/kamu'nashi", "paraujano": "utschi", "lokono": "hororo", "ic_oliver": "CARIB", "maipure": "yapa"},
 "water":    {"guajiro": "wuin", "paraujano": "win/winkari", "lokono": "oniabo/-nia", "ic_oliver": "CARIB", "maipure": "ueni"},
 "tree":     {"guajiro": "ouulia/mojui/wunuu", "paraujano": "jinghi/jiki", "lokono": "ada/kunnuku", "ic_oliver": "---", "maipure": "aa/aama"},
 "thou":     {"guajiro": "pia'", "paraujano": "pia", "lokono": "bii", "ic_oliver": "hu-guia", "maipure": "p-ia"},
}

# ── las columnas nuevas, con su página (cada celda leída; ver la propuesta) ──
# Goeje 1939, verificado en imagen salvo donde se dice. `---` = el registro no
# tiene forma legible para el concepto.
KAL_MUJERES = {
 "moon": "kati",        # p. 54
 "sun": "kaši",         # p. 54, f 1 am 62
 "stone": "šiba",       # p. 57, f 1 am 75
 "sand": "šakao",       # p. 57, común (K)
 "woman": "inharu",     # p. 40, f 1 am 32
 "man": "eyeri",        # p. 40, f 1 am 30
 "tooth": "ari",        # p. 33, f 1 am 19
 "path": "ema",         # p. 56, común (K)
 "one": "aban",         # Adam p. 281, común (arrouague abba)
 "two": "biama",        # Adam p. 281, Goeje p. 30, común
 "root": "---",
 "hear": "akambo",      # p. 79, fA
 "blood": "ita",        # p. 32, f 1 am 1
 "big": "uairi",          # p. 114 (imagen): «grand f uairi … A wadi»
 "mountain": "---",
 "water": "tona",       # p. 55, común (K tuna); Adam p. 288 «C. tonê»
 "tree": "huehue",      # p. 63, común (K)
 "thou": "bukuya",      # Adam p. 278, «boukoya», de mujeres
}
KAL_HOMBRES = dict(KAL_MUJERES, **{
 "moon": "nonum",       # p. 54, hK
 "sun": "hueyu",        # p. 54, hK
 "stone": "tebu",       # p. 57, K
 "woman": "uele",       # p. 40, hK
 "man": "uekeli",       # p. 39, hK
 "tooth": "ie",         # p. 33, hK
 "hear": "akugnuku",    # p. 84 (capa de texto), sin sigla
 "blood": "moena",      # p. 32, hK
 "big": "ubuto",         # p. 74 (imagen): «grand, gros, puissant h, f ubuto, K poto» (hfK)
 "thou": "amanle",      # Adam p. 278, de hombres (galibi)
})
# Neira y Ribero 1762. Ortografía del copista (su §ortografia_del_copista):
# «Vn» por «Un» (V inicial = u) y J/Y/I alternan: se normaliza a u e i.
ACHAGUA = {
 "moon": "kerri",                   # «Querri» Luna, pl. 73 izq.
 "sun": "erri",                     # «Erri» Sol, pl. 92 izq.
 "stone": "iba/kejeda",             # «Jba, quejeda» Piedra, pl. 83 der.
 "sand": "kaina",                   # «Caina» Arena, pl. 37 der.
 "woman": "ineretua/imuri",         # «Yneretua, Ymurí» Muger, pl. 76 der.
 "man": "wanarikaberri",            # «Guanaricaberrí» Varon, pl. 96 der.
 "tooth": "eri",                    # «Erí» Diente, pl. 55 der.
 "path": "iasubasi/anisuba",        # «Jasubasi, anisuba» Camino, pl. 45 der.
 "one": "---",
 "two": "iuchamata",                # «Juchamata» Dos, pl. 56 der.
 "root": "baririba/irrisi",         # «Baririba, Yrrisí» Raiz, pl. 87 der.
 "hear": "nuemmiuyu/nuemiu",        # «Nuemmiuyu, Nuemiu» Oir, pl. 78 der.
 "blood": "irrai",                  # «Yrraí» Sangre, pl. 90 der.
 "big": "manunayi",                 # «Manunayi» Grande arbol, pl. 66 izq.
 "mountain": "areberritai/mumidukui/muririui/kerrebe",  # Cerro pl. 48 izq.; Serrania pl. 91 der.
 "water": "uni",                    # «Vni» Agua, pl. 32 izq.
 "tree": "aikuba",                  # «Aicuba» Arbol, pl. 37 der.
 "thou": "gia/giya/girra",          # «Gia, Giya, Girra» tu, pl. 96 izq.
}
# Lista maestra taína, sólo voces con cronista y glosa de definición.
TAINO = {
 "moon": "mona",        # Colón
 "stone": "kiba/siba",  # kiba: Las Casas; siba: Pané
 "one": "ekiti",        # Las Casas
 "two": "iamoka",       # Las Casas
}

LENGUAS = ["guajiro", "paraujano", "lokono", "ic_oliver", "maipure",
           "achagua", "taino", "kal_mujeres", "kal_hombres"]


def celda(lengua: str, concepto: str) -> str:
    if lengua in A2[concepto]:
        return A2[concepto][lengua]
    return {"achagua": ACHAGUA, "taino": TAINO, "kal_mujeres": KAL_MUJERES,
            "kal_hombres": KAL_HOMBRES}[lengua].get(concepto, "---")


# Las 24 curadas del 31-08 (computo_d11.CURADAS), en la grafía de la fuente.
CURADAS = [
 ("cati", "luna", "moon"), ("cazi", "sol", "sun"), ("quiva", "piedra", "stone"),
 ("cuiva", "piedra", "stone"), ("rao", "arena", "sand"), ("jajato", "lugar de arena", "sand"),
 ("iero", "mujer", "woman"), ("ateri", "hombre", "man"), ("dare", "diente", "tooth"),
 ("ebo", "camino", "path"), ("darubana", "camino (comp.)", "path"), ("pana", "uno", "one"),
 ("gudamuen", "dos", "two"), ("buiamati", "dos lunas", "two"), ("ure", "raíz", "root"),
 ("jai", "oír", "hear"), ("quiricias", "sangre", "blood"), ("apo", "grande", "big"),
 ("quidi", "cerro", "mountain"), ("bana", "cerro (morfema)", "mountain"),
 ("para", "mar/agua grande", "water"), ("bara", "árbol", "tree"),
 ("cudanga", "usted (2ª)", "thou"), ("apana", "una luna", "moon"),
]
UMBRAL = 0.50


def medir() -> dict:
    filas, por_lengua = [], {l: {"con_forma": 0, "se_parece": 0, "suma": 0.0} for l in LENGUAS}
    for forma, glosa, concepto in CURADAS:
        fq = fonemizar(forma)
        mejores = {}
        for l in LENGUAS:
            vs = variantes(celda(l, concepto))
            if not vs:
                mejores[l] = None
                continue
            mejores[l] = round(max(sim(fq, v) for v in vs), 2)
            por_lengua[l]["con_forma"] += 1
            por_lengua[l]["suma"] += mejores[l]
            por_lengua[l]["se_parece"] += mejores[l] >= UMBRAL
        filas.append({"caquetio": forma, "glosa": glosa, "concepto": concepto, "fonemizada": fq,
                      "similitud": mejores})
    resumen = {}
    for l, d in por_lengua.items():
        resumen[l] = {"conceptos_con_forma": d["con_forma"], "se_parece_(>=0.50)": d["se_parece"],
                      "media_de_similitud": round(d["suma"] / d["con_forma"], 3) if d["con_forma"] else None}

    def cara_a_cara(a: str, b: str) -> dict:
        gana_a = gana_b = empate = sin_dato = 0
        detalle = {"gana_" + a: [], "gana_" + b: []}
        for f in filas:
            x, y = f["similitud"][a], f["similitud"][b]
            if x is None or y is None:
                sin_dato += 1
            elif x > y:
                gana_a += 1; detalle["gana_" + a].append(f["caquetio"])
            elif y > x:
                gana_b += 1; detalle["gana_" + b].append(f["caquetio"])
            else:
                empate += 1
        return {a: gana_a, b: gana_b, "empate": empate, "sin_dato_en_alguna": sin_dato, **detalle}

    return {
        "meta": {
            "medido": "2026-09-23",
            "script": "6-fusion/scripts/medir_cercania_hermanas.py",
            "instrumento": "el cómputo A de D11 (computo_d11.py, 2026-08-31): 24 atestiguadas de concepto directo, "
                           "fonemización D5, similitud = 1 − Levenshtein/longitud máxima, mejor variante",
            "umbral_de_parecido": UMBRAL,
            "fuentes_de_las_columnas": {
                "guajiro/paraujano/lokono/ic_oliver/maipure": "Oliver 1989, Tabla A-2 (tabla_a2_transcripcion.yaml)",
                "kal_mujeres/kal_hombres": "Goeje 1939 (sigue a Breton), leído en imagen; Adam 1879 pp. 278 y 281",
                "achagua": "Neira y Ribero 1762 (achagua_neira_ribero_1762.yaml)",
                "taino": "taino_lista_maestra_2026-09-22.yaml, sólo con cronista",
            },
        },
        "por_lengua": resumen,
        "cara_a_cara": {
            "kal_mujeres_contra_kal_hombres": cara_a_cara("kal_mujeres", "kal_hombres"),
            "kal_mujeres_contra_lokono": cara_a_cara("kal_mujeres", "lokono"),
            "kal_mujeres_contra_achagua": cara_a_cara("kal_mujeres", "achagua"),
            "kal_mujeres_contra_guajiro": cara_a_cara("kal_mujeres", "guajiro"),
            "lokono_contra_guajiro": cara_a_cara("lokono", "guajiro"),
        },
        "filas": filas,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    import yaml
    txt = yaml.safe_dump(medir(), allow_unicode=True, sort_keys=False, width=110)
    if a.salida:
        cab = ("# MEDICIÓN — ¿qué hermana está más cerca del caquetío atestiguado? (2026-09-23)\n"
               "# GENERADO por 6-fusion/scripts/medir_cercania_hermanas.py — no se edita a mano (regla 1).\n")
        Path(a.salida).write_text(cab + txt, encoding="utf-8")
        print(f"escrito {a.salida}")
    else:
        print(txt)
    return 0


if __name__ == "__main__":
    for nombre in ("stdout", "stderr"):
        f = getattr(sys, nombre)
        if hasattr(f, "buffer") and (f.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(f.buffer, encoding="utf-8", errors="replace"))
    sys.exit(main())
