# -*- coding: utf-8 -*-
"""El taíno de TRADICIÓN VIVA: de dónde vienen las 1.039 voces y qué comparten
con el caquetío, nombre contra nombre (2026-09-24).

Miguel, 2026-09-24: «Pero si tenemos mil y tantas voces. Esas otras de donde
vienen? Recuerda que los cronistas no son la fuente principal.. es como el
Caquetio. La tradición Oral prela por encima.» — y «Dale».

La propuesta es `6-fusion/taino_tradicion_viva_2026-09-24.yaml`; este script
mide lo que ella cita (regla 1):

  1. LA PROCEDENCIA de las voces de la lista maestra: clase, obra, y en Coll y
     Toste el tipo de apoyo que su transcripción ya declara, por campo.
  2. EL CRUCE NOMBRE CONTRA NOMBRE: el caquetío atestiguado y retroabstraído
     (la tradición viva de Paraguaná: Zavala, Medina) contra el taíno sin
     conjetura ni lista de Rafinesque. Similitud ≥ 0,75 sobre la fonemización
     D5 abre la candidatura; decide la glosa, leída a mano y escrita en la
     propuesta (`parejas_con_el_mismo_significado`), que aquí sólo se cuenta.
  3. LA FUGA de Venezuela: voces de la sección `costa_de_venezuela` de Oviedo
     que la lista maestra cuenta como taínas.

Uso (desde proyecto-linguistico-caquetío/):
    python 6-fusion/scripts/medir_taino_tradicion_viva.py --salida 6-fusion/medicion_taino_tradicion_viva_2026-09-24.yaml
"""
from __future__ import annotations

import argparse
import io
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import yaml

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "curiana_sim"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from medir_cercania_hermanas import fonemizar, sim  # noqa: E402

UMBRAL = 0.75


def _y(nombre):
    return yaml.safe_load((R / "6-fusion" / nombre).read_text(encoding="utf-8"))


def _n(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn")


def rafinesque(e) -> bool:
    return any("afinesque" in str(c.get("lo_que_dice_la_obra")) for c in e.get("cadena_de_custodia", []))


def medir() -> dict:
    T = _y("taino_lista_maestra_2026-09-22.yaml")["voces"]
    C = _y("taino3_coll_y_toste_1897.yaml")
    import curiana_lexicon as CL  # noqa: E402

    # 1. procedencia
    por_clase = Counter(e["clase"] for e in T)
    obras_ii = Counter(o for e in T if e["clase"] == "ii-solo-secundaria" for o in set(e.get("obras_que_la_traen", [])))
    iii_rafinesque = sum(1 for e in T if e["clase"] == "iii-conjetura-moderna" and rafinesque(e))
    tab = Counter((e["tipo_de_apoyo"], e["campo"]) for e in C["voces"])
    tipos = sorted({t for t, _c in tab})
    campos = sorted({c for _t, c in tab}, key=lambda c: -sum(v for (t, cc), v in tab.items() if cc == c))
    coll = {c: {t: tab.get((t, c), 0) for t in tipos} for c in campos}

    # 3. la fuga de Venezuela
    O = _y("taino_oviedo_valdes_1851.yaml")
    venez = [e.get("forma_fuente") for e in O.get("costa_de_venezuela") or [] if e.get("forma_fuente")]
    fuga = sorted(e["lema"] for e in T
                  if {_n(x) for x in (e.get("formas_atestiguadas") or [])} & {_n(f) for f in venez}
                  and set(e.get("obras_que_la_traen", [])) == {"oviedo-valdes-1851"})

    # 2. el cruce
    V = CL.VOCABULARIO_BASE
    caq = [(k, e) for k, e in V.items() if e.get("fuente") in ("caquetío-atestiguado", "caquetío-retroabstraido")]
    tai = [e for e in T if e["clase"] != "iii-conjetura-moderna" and not rafinesque(e) and e["lema"] not in fuga]
    candidatas = 0
    for k, _e in caq:
        fk = fonemizar(k.split("-")[0])
        if len(fk) < 3:
            continue
        for t in tai:
            formas = {t["lema"]} | set(t.get("formas_atestiguadas") or [])
            if max((sim(fk, fonemizar(f)) for f in formas if len(fonemizar(f)) >= 3), default=0) >= UMBRAL:
                candidatas += 1
    prop = _y("taino_tradicion_viva_2026-09-24.yaml")
    iguales = prop["el_cruce"]["parejas_con_el_mismo_significado"]
    return {
        "meta": {"medido": "2026-09-24", "script": "6-fusion/scripts/medir_taino_tradicion_viva.py",
                 "umbral_de_similitud": UMBRAL},
        "procedencia": {
            "voces_de_la_lista_maestra": len(T),
            "por_clase": dict(por_clase),
            "clase_ii_por_obra": dict(obras_ii),
            "clase_iii_que_viene_de_rafinesque": iii_rafinesque,
            "coll_y_toste_tipo_de_apoyo_por_campo": coll,
            "coll_y_toste_cap_X_vocabulario_espanol_boriqueno": len(C.get("vocabulario_espanol_boriqueno") or []),
        },
        "fuga_de_venezuela": {"voces": fuga, "n": len(fuga)},
        "el_cruce": {
            "caquetio_atestiguado_y_retroabstraido": len(caq),
            "taino_sin_conjetura_ni_rafinesque_ni_venezuela": len(tai),
            "parejas_candidatas_por_la_forma": candidatas,
            "con_el_mismo_significado_leidas_a_mano": len(iguales),
            "de_ellas_por_clase": dict(Counter(p["clase"] for p in iguales)),
        },
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    txt = yaml.safe_dump(medir(), allow_unicode=True, sort_keys=False, width=110)
    if a.salida:
        cab = ("# MEDICIÓN — el taíno de tradición viva (2026-09-24).\n"
               "# GENERADO por 6-fusion/scripts/medir_taino_tradicion_viva.py — no se edita a mano (regla 1).\n")
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
