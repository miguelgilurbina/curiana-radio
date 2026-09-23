"""Ensambla y verifica `6-fusion/fauna_paraguana_aves_2026-09-22.yaml` (parcela FA2).

El YAML lo escribe a mano el minador —nombres, fuentes, descripciones,
sonidos—, pero TODA cifra que lleva sale de aquí (regla 1):

1. `gbif` de cada especie: registros, primer y último año, índice por período
   y patrón, leídos de `6-fusion/medicion_gbif_aves_paraguana_2026-09-22.yaml`
   (que genera `medir_gbif_aves_paraguana.py`). Si la especie no está, escribe
   `registros: 0` — y ese cero hay que leerlo con la regla 6.
2. `escuchar_en_la_caja`: los ID de xeno-canto GRABADOS en la península.
3. Topes de largo del encargo: `descripcion_visual` ≤ 220, `desc_referente`
   ≤ 180, `se_oye` ≤ 80. Si alguno se pasa, falla.
4. El `silabeo_propuesto` de cada sonido, contra la fonotáctica del caquetío
   ATESTIGUADO (`curiana_fonotactica.medir()`, la misma que usa el proyecto) y
   contra el lexicón: si al fonemizarlo choca con una clave existente, lo dice.
5. `meta.medido`: cuántas especies, por presencia, cuántos huecos, cuántos
   candidatos, cuántos silabeos pasan.

Uso:
    python 6-fusion/scripts/ensamblar_fauna_aves.py          # reescribe el YAML
    python 6-fusion/scripts/ensamblar_fauna_aves.py --check  # sólo verifica
"""
from __future__ import annotations

import argparse
import io
import sys
from collections import Counter
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
YAML_AVES = RAIZ / "6-fusion" / "fauna_paraguana_aves_2026-09-22.yaml"
MEDICION = RAIZ / "6-fusion" / "medicion_gbif_aves_paraguana_2026-09-22.yaml"
TOPES = {"descripcion_visual": 220, "desc_referente": 180, "se_oye": 80}
CABECERA = (
    "# FAUNA DE PARAGUANÁ — LAS AVES (parcela FA2 de la campaña de fauna, 2026-09-22)\n"
    "# Propuesta sin fusionar. Las cifras (`gbif`, `escuchar_en_la_caja`, `fonotactica`,\n"
    "# `meta.medido`) las escribe 6-fusion/scripts/ensamblar_fauna_aves.py: no se editan a mano.\n"
)


def _forzar_utf8() -> None:
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def _fonotactica():
    sys.path.insert(0, str(RAIZ / "curiana_sim"))
    import curiana_fonotactica as F  # noqa: E402
    import curiana_lexicon as L  # noqa: E402
    fono, _ = F.medir()
    claves = {}
    for tabla in (L.VOCABULARIO_BASE, L.FUERA_DEL_HABLA):
        for k, v in tabla.items():
            claves.setdefault(F.fonemizar(k), []).append(f"{k} ({v.get('fuente')})")
    return F, fono, claves


def ensamblar(datos: dict, med: dict) -> list[str]:
    errores: list[str] = []
    por_nombre = {e["cientifico"]: e for e in med["especies"]}
    ceros = {c["cientifico"]: c for c in med.get("especies_solo_o_con_ceros", [])}
    grab: dict[str, list[str]] = {}
    for g in med.get("grabaciones_xeno_canto_en_la_caja", []):
        grab.setdefault(g["especie"], []).append(g["xc"])
    F, fono, claves = _fonotactica()

    for e in datos["especies"]:
        cien = e.get("cientifico") or []
        cien = cien if isinstance(cien, list) else [cien]
        filas = [por_nombre[c] for c in cien if c in por_nombre]
        if filas:
            e["gbif"] = [{
                "cientifico": f["cientifico"],
                "registros": f["registros"],
                "anios": f"{f['anio_primero']}-{f['anio_ultimo']}",
                "indice_por_periodo": f["indice_por_periodo"],
                "patron": f["patron"],
            } for f in filas]
        else:
            e["gbif"] = [{"cientifico": c, "registros": 0,
                          "nota": ("solo filas de AUSENCIA (organismQuantity 0) en PANGAEA NeoMaps 2010"
                                   if c in ceros else "sin registro en la caja: un cero mide también el esfuerzo (regla 6)")}
                         for c in cien]
        xc = sorted({x for c in cien for x in grab.get(c, [])})
        if e.get("sonido") is not None:
            e["sonido"]["escuchar_en_la_caja"] = xc or None
            sil = (e["sonido"].get("silabeo_propuesto") or {})
            if sil.get("forma"):
                ok, motivos = fono.valida(sil["forma"].replace("-", ""))
                # la forma entera y cada tramo entre guiones: `koro-koro` no es
                # una clave, pero `koro` sí («cotorra»)
                # (tramos de ≥ 3 letras: una sílaba suelta como `wa` o `ka`
                # casa con afijos y no dice nada)
                tramos = [sil["forma"].replace("-", "")] + [
                    t for t in sil["forma"].split("-") if len(F.fonemizar(t)) >= 3]
                choque = sorted({c for t in tramos for c in claves.get(F.fonemizar(t), [])})
                sil["fonotactica"] = {"pasa": ok, "motivos": motivos or None,
                                      "choca_con_el_lexicon": choque or None}
        for campo in ("descripcion_visual",):
            if e.get(campo) and len(e[campo]) > TOPES[campo]:
                errores.append(f"{e['id']}: {campo} tiene {len(e[campo])} > {TOPES[campo]}")

    for c in datos.get("candidatos_referente", {}).get("lista", []):
        for campo in ("desc_referente", "se_oye"):
            if c.get(campo) and len(c[campo]) > TOPES[campo]:
                errores.append(f"{c['id']}: {campo} tiene {len(c[campo])} > {TOPES[campo]}")
        c["largo"] = {"desc_referente": len(c.get("desc_referente") or ""),
                      "se_oye": len(c.get("se_oye") or "")}

    esp = datos["especies"]
    sil = [e["sonido"]["silabeo_propuesto"]["fonotactica"] for e in esp
           if e.get("sonido") and (e["sonido"].get("silabeo_propuesto") or {}).get("fonotactica")]
    datos["meta"]["medido"] = {
        "entradas": len(esp),
        "por_presencia_s_xv": dict(Counter(e["presencia_s_xv"] for e in esp)),
        "es_hueco": sum(1 for e in esp if e.get("es_hueco") is True),
        "con_voz_caquetia_en_el_lexicon": sum(1 for e in esp if (e.get("nombres") or {}).get("caquetio")),
        "con_onomatopeya_documentada": sum(1 for e in esp if e.get("sonido") and e["sonido"].get("onomatopeya_documentada")),
        "con_descripcion_de_fuente": sum(1 for e in esp if (e.get("descripcion_fuente") or {}).get("obra")),
        "candidatos_referente": len(datos.get("candidatos_referente", {}).get("lista", [])),
        "silabeos_propuestos": len(sil),
        "silabeos_que_pasan_la_fonotactica": sum(1 for s in sil if s["pasa"]),
        "silabeos_que_chocan_con_el_lexicon": sum(1 for s in sil if s["choca_con_el_lexicon"]),
        "gbif_total_registros_aves": med["total_registros_aves"],
        "gbif_especies_en_la_caja": med["especies_distintas"],
    }
    return errores


def main(argv=None) -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    datos = yaml.safe_load(YAML_AVES.read_text(encoding="utf-8"))
    med = yaml.safe_load(MEDICION.read_text(encoding="utf-8"))
    errores = ensamblar(datos, med)
    for k, v in datos["meta"]["medido"].items():
        print(f"{k:40s} {v}")
    for e in errores:
        print("ERROR", e)
    if not a.check and not errores:
        texto = CABECERA + yaml.safe_dump(datos, allow_unicode=True, sort_keys=False, width=100)
        YAML_AVES.write_text(texto, encoding="utf-8")
        # comprobar que reparsea igual
        assert yaml.safe_load(YAML_AVES.read_text(encoding="utf-8")) == datos
        print(f"escrito: {YAML_AVES.relative_to(RAIZ)}")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
