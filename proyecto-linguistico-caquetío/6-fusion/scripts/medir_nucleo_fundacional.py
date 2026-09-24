# -*- coding: utf-8 -*-
"""El núcleo fundacional rehecho desde las hermanas — el coste, MEDIDO (2026-09-24).

Miguel, 2026-09-23/24: «preferiría usarlo [el kalinago de mujeres] de
referencia […] o al menos poder medirlo y poder usar lo más posible» y, ante la
propuesta de rehacer el núcleo desde el lokono y el kalinago de mujeres juntos:
«Dale».

La propuesta es `6-fusion/nucleo_fundacional_hermanas_2026-09-24.yaml`; el
inventario de partida, `6-fusion/inventario_nucleo_fundacional_2026-09-23.yaml`.
Este script mide lo que la propuesta cita (regla 1), con el MISMO instrumento
que tf.5 y la campaña del habla de mujeres (`medir_d11_voces_wayuu.medir`): uso
de cada voz vieja en la base, en qué plantillas, koiné, escena y tests se
enseña, qué formas pasan a «raíz de ninguna parte» si se archiva, y las
colisiones, la fonotáctica y la puerta de cada candidata.

Uso (desde proyecto-linguistico-caquetío/):
    python 6-fusion/scripts/medir_nucleo_fundacional.py --salida 6-fusion/medicion_nucleo_fundacional_2026-09-24.yaml
    python 6-fusion/scripts/medir_nucleo_fundacional.py --check

⚠️ NO lee `curiana_sim/.env` ni llama a la API. A la base sólo le hace SELECT.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
R = AQUI.parents[1]
sys.path.insert(0, str(AQUI))
import medir_d11_voces_wayuu as M  # noqa: E402  el instrumento de tf.5, tal cual

PROPUESTA = R / "6-fusion" / "nucleo_fundacional_hermanas_2026-09-24.yaml"
MEDICION = R / "6-fusion" / "medicion_nucleo_fundacional_2026-09-24.yaml"

# ══════════════════════════════════════════════════════════════════════
# LAS OPCIONES — espejo de la propuesta (--check lo verifica).
# `[]` = archivar sin sustituta nueva; una forma que YA es clave caquetía del
# lexicón (jusual, kidi, ako…) no entra nueva. SE_QUEDA = la voz se queda
# (cambian su etiqueta y su nota, no la forma): coste 0 en el habla.
# ══════════════════════════════════════════════════════════════════════
OPCIONES = {
    # verbos
    "naa":   {"A": ["kunu"], "B": ["naa"]},
    "waa":   {"A": ["sile"], "B": ["andi"], "C": ["waa"]},
    "kaa":   {"A": ["kaa"]},
    "maa":   {"A": ["maa"], "B": ["dia"]},
    "taa":   {"A": ["butu"], "B": ["nika"], "C": ["taa"]},
    "chaa":  {"A": ["ani"], "B": ["chaa"]},
    "suna":  {"A": ["dunku"], "B": ["dumki"]},
    "masa":  {"A": ["aeke"], "B": ["aika"]},
    "awa":   {"A": ["ati"], "B": ["ata"]},
    "panaa": {"A": ["aita"], "B": ["diti"]},
    "kono":  {"A": ["jusual"], "B": ["abuna"]},
    "raka":  {"A": ["hiti"], "B": ["raka"]},
    "rua":   {"A": ["kudu"], "B": ["rua"]},
    # nombres
    "duna":  {"A": ["uni"]},
    "amana": {"A": ["hikihi"], "B": ["hiki"], "C": ["wairon"]},
    "kaya":  {"A": ["unia"], "B": ["oya"]},
    "kuru":  {"A": ["ada"], "B": ["bara"]},
    "arima": {"A": ["hime"], "B": ["arima"]},
    "dali":  {"A": ["wunabu"], "B": ["dali"]},
    "suka":  {"A": ["suka"]},
    "sima":  {"A": ["kidi"]},
    "ama":   {"A": ["ama"], "B": ["kusu"]},
    "baba":  {"A": ["iti"], "B": ["kusi"], "C": ["baba"]},
    "buri":  {"A": ["dare"], "B": ["diti"]},
    "nomi":  {"A": ["ateri"]},
    "wari":  {"A": ["iero"]},
    "kabo":  {"A": ["isi"], "B": ["isihi"]},
    "nii":   {"A": ["akusi"], "B": ["aku"]},
    "bari":  {"A": ["bari"], "B": ["ulakae"]},
    "arua":  {"A": ["ako"]},
    # partículas
    "ka":    {"A": ["badia"], "B": ["ka"]},
    "mara":  {"A": ["ika"], "B": ["mara"]},
    "saa":   {"A": ["bena"], "B": ["saa"]},
    "naka":  {"A": ["kia"], "B": ["naka"]},
    "puna":  {"A": ["puna"]},
    "wara":  {"A": ["kibe"], "B": ["wara"]},
}
RECOMENDADA = {v: "A" for v in OPCIONES}
SE_QUEDA = {(v, l) for v, ops in OPCIONES.items() for l, fs in ops.items() if fs == [v]}
CAT_CANDIDATA = {
    "kunu": "v_raiz", "butu": "v_raiz", "andi": "v_raiz", "sile": "v_raiz", "dia": "v_raiz", "nika": "v_raiz",
    "ani": "v_raiz", "dunku": "v_raiz", "dumki": "v_raiz", "aeke": "v_raiz", "aika": "v_raiz",
    "ati": "v_raiz", "ata": "v_raiz", "aita": "v_raiz", "diti": "v_raiz", "abuna": "v_raiz",
    "hiti": "v_raiz", "kudu": "v_raiz", "uni": "sust", "hiki": "sust", "hikihi": "sust", "unia": "sust", "oya": "sust",
    "ada": "sust", "hime": "sust", "wunabu": "sust", "kusu": "sust", "iti": "sust", "kusi": "sust",
    "isi": "sust", "isihi": "sust", "akusi": "sust", "aku": "sust", "ulakae": "sust",
    "badia": "part", "ika": "part", "bena": "part", "kia": "part", "kibe": "part",
}
FORMAS_DE_LA_TANDA_FINAL = M.FORMAS_DE_LA_TANDA_FINAL + (
    "danu", "ruku", "diki", "kuburuku", "kasalini", "mautia", "popoi", "wasima",
    # lo que propone la campaña del habla de mujeres (#234)
    "saika", "uli", "halira", "kule", "huda", "kake", "halikebe", "aiima")


def medir_voces(con_base: bool) -> dict:
    M._sin_dotenv()
    sys.path.insert(0, str(R / "curiana_sim"))
    import curiana_lexicon as CL  # noqa: E402
    V = CL.VOCABULARIO_BASE
    lista = [v for v in OPCIONES if v in V]
    ya = tuple(k for k, e in V.items() if "DEUDA D11" in str(e.get("notas", "")))
    guarda = {k: V[k].get("notas") for k in lista}
    for k in lista:   # el instrumento arma su lista con «DEUDA D11»: se marca en memoria
        V[k]["notas"] = f"{V[k].get('notas', '')} [DEUDA D11 — marca en memoria del medidor]"
    M.OPCIONES, M.RECOMENDADA, M.SE_QUEDA = OPCIONES, RECOMENDADA, SE_QUEDA
    M.CAT_CANDIDATA, M.PRONOMBRES_TF1 = CAT_CANDIDATA, ya
    M.FORMAS_DE_LA_TANDA_FINAL = FORMAS_DE_LA_TANDA_FINAL
    try:
        out = M.medir(R / "curiana_sim", con_base)
    finally:
        for k, n in guarda.items():
            V[k]["notas"] = n
    out["meta"]["script"] = "6-fusion/scripts/medir_nucleo_fundacional.py (con medir_d11_voces_wayuu.medir)"
    out["la_lista"] = {"voces": lista, "n": len(lista),
                       "fuera_del_lexicon": [v for v in OPCIONES if v not in V]}
    return out


def check() -> int:
    import yaml
    prop = yaml.safe_load(PROPUESTA.read_text(encoding="utf-8"))
    med = yaml.safe_load(MEDICION.read_text(encoding="utf-8"))
    malos = []
    voces = {v["voz"]: v for g in prop["grupos"] for v in g["voces"]}
    if set(voces) != set(OPCIONES):
        malos.append(f"voces: propuesta {sorted(set(voces) ^ set(OPCIONES))}")
    for voz, v in voces.items():
        if v.get("recomendacion") != RECOMENDADA.get(voz):
            malos.append(f"{voz}: recomendación {v.get('recomendacion')} / {RECOMENDADA.get(voz)}")
        for op in v.get("opciones", []):
            if sorted(op.get("formas") or []) != sorted(OPCIONES.get(voz, {}).get(op["letra"], ["?"])):
                malos.append(f"{voz}.{op['letra']}: formas {op.get('formas')}")
            fila = med["coste_por_opcion"].get(voz, {}).get(op["letra"], {})
            for campo, valor in (op.get("coste_medido") or {}).items():
                if campo in fila and fila[campo] != valor:
                    malos.append(f"{voz}.{op['letra']}.{campo}: propuesta {valor} / medición {fila[campo]}")
    print("\n".join(malos) if malos else "check: la propuesta y la medición coinciden")
    return 1 if malos else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sin-base", action="store_true")
    ap.add_argument("--salida")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return check()
    txt = M._yaml(medir_voces(not a.sin_base))
    if a.salida:
        cab = ("# MEDICIÓN — el núcleo fundacional rehecho desde las hermanas (2026-09-24).\n"
               "# GENERADO por 6-fusion/scripts/medir_nucleo_fundacional.py — no se edita a mano (regla 1).\n"
               "# La propuesta que lo usa: 6-fusion/nucleo_fundacional_hermanas_2026-09-24.yaml\n")
        Path(a.salida).write_text(cab + txt, encoding="utf-8")
        print(f"escrito {a.salida}")
    else:
        print(txt)
    return 0


if __name__ == "__main__":
    M._forzar_utf8()
    sys.exit(main())
