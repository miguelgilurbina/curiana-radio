# -*- coding: utf-8 -*-
"""El habla de las mujeres kalinago — lo que MIDE la campaña (2026-09-23).

Miguel, 2026-09-23: «si usan las mismas palabras para el Sol y la Luna podrían
compartir más conceptos, obvio no todos pero debe haber una base que
compartan» y «la idea es que nuestro core sea potente para no tener que hacer
más campañas». La propuesta es `6-fusion/kalinago_mujeres_2026-09-23.yaml`;
este script mide lo que ella cita (regla 1). Tres cosas:

  1. LA PRUEBA DE LA BASE COMPARTIDA — cuenta los veredictos de la tabla
     `prueba_de_la_base_compartida` de la propuesta (la lectura concepto a
     concepto es del escriba, con página; aquí sólo se cuenta, para que ninguna
     cifra se escriba a mano).
  2. LAS OCHO VOCES QUE SEGUÍAN SALIENDO DEL WAYUU — la campaña de tf.5 buscó
     «DEUDA D11» en las notas y estas ocho dicen «deuda de D11 fase 3»: no las
     vio. Se reconoce aquí la lista por la ETIQUETA de su nota F8
     (`wayunaiki-cogn` o `wayunaiki/lokono`), no por una cadena, y se miden con
     el MISMO instrumento que tf.5 (`medir_d11_voces_wayuu.medir`): uso en la
     base, enseñanza, colisiones de cada candidata, fonotáctica y la puerta.
  3. LAS ETIQUETAS DE LOS PRONOMBRES si el kalinago cuenta como cuarta hermana
     (sólo qué cambia; la decisión es de Miguel).

Uso (desde proyecto-linguistico-caquetío/):

    python 6-fusion/scripts/medir_kalinago_mujeres.py --salida 6-fusion/medicion_kalinago_mujeres_2026-09-23.yaml
    python 6-fusion/scripts/medir_kalinago_mujeres.py --sin-base   # sin Docker
    python 6-fusion/scripts/medir_kalinago_mujeres.py --check      # propuesta ↔ medición

⚠️ NO lee `curiana_sim/.env` ni llama a la API (hereda `_sin_dotenv` de tf.5).
A la base sólo le hace SELECT.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
R = AQUI.parents[1]
sys.path.insert(0, str(AQUI))
import medir_d11_voces_wayuu as M  # noqa: E402  el instrumento de tf.5, tal cual

PROPUESTA = R / "6-fusion" / "kalinago_mujeres_2026-09-23.yaml"
MEDICION = R / "6-fusion" / "medicion_kalinago_mujeres_2026-09-23.yaml"

# ══════════════════════════════════════════════════════════════════════
# LAS OPCIONES — espejo de la propuesta (--check lo verifica)
# ══════════════════════════════════════════════════════════════════════
OPCIONES = {
    "anasa":    {"A": ["saika"], "B": ["saino"]},
    "mütsia":   {"A": ["wele"], "B": ["uli"]},
    "kasuta":   {"A": ["halira"], "B": ["kasare"]},
    "sünatü":   {"A": ["kule"], "B": []},
    "outa":     {"A": ["huda"], "B": ["hila"]},
    "kataa":    {"A": ["kake"], "B": ["kaku"]},
    "talata":   {"A": ["halikebe"], "B": ["ulabu"]},
    "jashichi": {"A": ["iama"], "B": ["kain"], "C": ["aiima"]},
}
RECOMENDADA = {"anasa": "A", "mütsia": "B", "kasuta": "A", "sünatü": "A",
               "outa": "A", "kataa": "A", "talata": "A", "jashichi": "C"}
CAT_CANDIDATA = {"saika": "v_estativo", "saino": "v_estativo", "wele": "v_estativo",
                 "uli": "v_estativo", "halira": "v_estativo", "kasare": "v_estativo",
                 "kule": "v_estativo", "huda": "v_raiz", "hila": "v_raiz",
                 "kake": "v_raiz", "kaku": "v_raiz", "halikebe": "v_raiz",
                 "ulabu": "v_raiz", "iama": "sust", "kain": "v_estativo",
                 "aiima": "sust"}
# Lo que ya decidió la tanda final y no se toca aquí.
FORMAS_DE_LA_TANDA_FINAL = M.FORMAS_DE_LA_TANDA_FINAL + (
    "danu", "ruku", "diki", "kuburuku", "kasalini", "mautia", "popoi", "wasima")

# La etiqueta F8 que delata una derivación desde el wayuu (nota de la entrada).
ETIQUETA_WAYUU = re.compile(r"etiquetada `wayunaiki(?:-cogn|/lokono)`")


def con_etiqueta_wayuu(V) -> dict[str, str]:
    return {k: e.get("fuente") for k, e in V.items()
            if str(e.get("fuente", "")).startswith("caquetío")
            and ETIQUETA_WAYUU.search(str(e.get("notas", "")))}


def ocho_voces(V) -> list[str]:
    """Las RECONSTRUIDAS: son las que llegan a los agentes (el perfil `era2`
    muestrea la capa reconstruida y deja fuera la hipotética)."""
    return sorted(k for k, f in con_etiqueta_wayuu(V).items() if f == "caquetío-reconstruido")


def medir_voces(con_base: bool) -> dict:
    """Las ocho, con el instrumento de tf.5. Su lista sale de «DEUDA D11» en las
    notas —la búsqueda que NO las vio—, así que se le da la de aquí: se marca
    la nota EN MEMORIA (no se escribe nada) y las voces con «DEUDA D11» que ya
    decidió tf.5 se declaran decididas."""
    M._sin_dotenv()
    sys.path.insert(0, str(R / "curiana_sim"))
    import curiana_lexicon as CL  # noqa: E402
    V = CL.VOCABULARIO_BASE
    lista = ocho_voces(V)
    ya = tuple(k for k, e in V.items() if "DEUDA D11" in str(e.get("notas", "")))
    guarda = {k: V[k].get("notas") for k in lista}
    for k in lista:
        V[k]["notas"] = f"{V[k].get('notas', '')} [DEUDA D11 — marca en memoria del medidor]"
    M.OPCIONES, M.RECOMENDADA, M.SE_QUEDA = OPCIONES, RECOMENDADA, set()
    M.CAT_CANDIDATA, M.PRONOMBRES_TF1 = CAT_CANDIDATA, ya
    M.FORMAS_DE_LA_TANDA_FINAL = FORMAS_DE_LA_TANDA_FINAL
    try:
        out = M.medir(R / "curiana_sim", con_base)
    finally:
        for k, n in guarda.items():
            V[k]["notas"] = n
    out["meta"]["script"] = "6-fusion/scripts/medir_kalinago_mujeres.py (con medir_d11_voces_wayuu.medir)"
    out["la_lista"] = {
        "como_se_reconoce": "la etiqueta F8 de la nota: `wayunaiki-cogn` o `wayunaiki/lokono`",
        "voces": lista, "n": len(lista),
        "por_que_tf5_no_las_vio": ("tf.5 buscó la cadena «DEUDA D11»; estas notas dicen «entra en la "
                                   "deuda de D11 fase 3» (o nada) y la búsqueda distingue mayúsculas"),
        "ya_decididas_por_tf5_con_DEUDA_D11": sorted(ya),
        "hipoteticas_con_la_misma_etiqueta": sorted(k for k, f in con_etiqueta_wayuu(V).items()
                                                    if f != "caquetío-reconstruido"),
        "nota_hipoteticas": "no las muestrea el perfil era2 ni las enseña ninguna plantilla",
    }
    return out


def contar_prueba() -> dict:
    import yaml
    prop = yaml.safe_load(PROPUESTA.read_text(encoding="utf-8"))
    filas = prop["prueba_de_la_base_compartida"]["conceptos"]
    con_par = [f for f in filas if f.get("kalinago_mujeres") and f.get("kalinago_hombres")]
    sin_par = [f for f in filas if f not in con_par]
    ver = lambda fs: dict(Counter(f["veredicto"] for f in fs))
    fuerza = lambda fs: dict(Counter(f.get("fuerza", "—") for f in fs if f["veredicto"] == "con-las-mujeres"))
    return {
        "conceptos_leidos": len(filas),
        "con_forma_de_hombres_y_de_mujeres_distintas": {
            "n": len(con_par), "veredictos": ver(con_par), "fuerza_de_los_que_van_con_las_mujeres": fuerza(con_par),
            "cuales": [f["caquetio"] for f in con_par]},
        "con_una_sola_forma_kalinago": {"n": len(sin_par), "veredictos": ver(sin_par),
                                        "cuales": {f["caquetio"]: f["veredicto"] for f in sin_par}},
        "atestiguadas_caquetias_buscadas_sin_equivalente": len(
            prop["prueba_de_la_base_compartida"].get("sin_equivalente_en_goeje", [])),
    }


def pronombres() -> dict:
    sys.path.insert(0, str(R / "curiana_sim"))
    import curiana_lexicon as CL  # noqa: E402
    V = CL.VOCABULARIO_BASE
    return {k: {"capa_hoy": V[k].get("fuente"),
                "si_el_kalinago_cuenta": ("caquetío-reconstruido" if k in ("bui", "lihi", "tuhu")
                                          else V[k].get("fuente"))}
            for k in ("dai", "bui", "lihi", "tuhu", "waya", "naya") if k in V}


def check() -> int:
    import yaml
    prop = yaml.safe_load(PROPUESTA.read_text(encoding="utf-8"))
    med = yaml.safe_load(MEDICION.read_text(encoding="utf-8"))
    malos = []
    voces = {v["voz"]: v for v in prop["las_ocho_voces_del_wayuu"]["voces"]}
    if set(voces) != set(OPCIONES):
        malos.append(f"voces: propuesta {sorted(voces)} / medidas {sorted(OPCIONES)}")
    for voz, v in voces.items():
        if v.get("recomendacion") != RECOMENDADA.get(voz):
            malos.append(f"{voz}: recomendación {v.get('recomendacion')} / {RECOMENDADA.get(voz)}")
        for op in v.get("opciones", []):
            if sorted(op.get("formas") or []) != sorted(OPCIONES.get(voz, {}).get(op["letra"], ["?"])):
                malos.append(f"{voz}.{op['letra']}: formas {op.get('formas')}")
            fila = med["voces"]["coste_por_opcion"].get(voz, {}).get(op["letra"], {})
            for campo, valor in (op.get("coste_medido") or {}).items():
                if campo in fila and fila[campo] != valor:
                    malos.append(f"{voz}.{op['letra']}.{campo}: propuesta {valor} / medición {fila[campo]}")
    if contar_prueba() != med["prueba"]:
        malos.append("prueba: la tabla de la propuesta cambió desde la medición — re-medir")
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
    out = {"prueba": contar_prueba(), "pronombres": pronombres(), "voces": medir_voces(not a.sin_base)}
    txt = M._yaml(out)
    if a.salida:
        cab = ("# MEDICIÓN — el habla de las mujeres kalinago (2026-09-23).\n"
               "# GENERADO por 6-fusion/scripts/medir_kalinago_mujeres.py — no se edita a mano (regla 1).\n"
               "# La propuesta que lo usa: 6-fusion/kalinago_mujeres_2026-09-23.yaml\n")
        Path(a.salida).write_text(cab + txt, encoding="utf-8")
        print(f"escrito {a.salida}")
    else:
        print(txt)
    return 0


if __name__ == "__main__":
    M._forzar_utf8()
    sys.exit(main())
