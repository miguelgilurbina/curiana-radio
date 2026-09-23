"""Las aves de Paraguaná en GBIF: qué especies, cuántos registros, en qué meses.

Campaña de fauna, parcela FA2 (aves), 2026-09-22. Mide, no opina: el
inventario del YAML `6-fusion/fauna_paraguana_aves_2026-09-22.yaml` cita las
cifras de aquí (regla 1) y nunca las escribe a mano.

Qué hace, con la API abierta de GBIF (sin clave; datos CC0/CC-BY por dataset):

1. Cuenta los registros de la clase Aves (classKey=212) dentro de la caja de
   la península y sus aguas, con el facet de especies y de datasets.
2. Por cada especie: nombre científico, orden y familia (`/v1/species`),
   registros por MES (facet=month) y el primer y último AÑO con registro.
3. Por cada dataset: título, DOI y licencia (`/v1/dataset`).
4. El esfuerzo: registros de TODAS las aves por mes, para que la presencia
   mensual de una especie se pueda leer contra lo que se muestreó.

Y reparte cada especie en los tres períodos del canon de la era 2
(`6-fusion/clima_era2.yaml`): P1 Tiempo de Viento = enero-mayo, P2 la seca
larga = junio-septiembre, P3 Tiempo de Siembra = octubre-diciembre.

⚠️ Lo que NO mide: presencia en el siglo XV (regla 3). GBIF es 1900-2026 y
casi todo eBird de la última década: dice que el ave cabe en este medio hoy,
no que estuviera entonces. Y un cero en un mes mide el esfuerzo de los
observadores tanto como la ausencia del ave (regla 6).

La caja: 11,50-12,22 N / 70,32-69,78 O. Deja fuera Coro (11,40 N) y Aruba
(12,40 N en su punta sur), y dentro el istmo norte, el Golfete y la costa.

Uso:
    python 6-fusion/scripts/medir_gbif_aves_paraguana.py            # escribe el YAML
    python 6-fusion/scripts/medir_gbif_aves_paraguana.py --check    # mide sin escribir
    python 6-fusion/scripts/medir_gbif_aves_paraguana.py --cache DIR # guarda/relee las respuestas
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "6-fusion" / "medicion_gbif_aves_paraguana_2026-09-22.yaml"
API = "https://api.gbif.org/v1"
CAJA = {"decimalLatitude": "11.5,12.22", "decimalLongitude": "-70.32,-69.78"}
AVES = {"classKey": "212"}
PERIODOS = {
    "P1_tiempo_de_viento": [1, 2, 3, 4, 5],
    "P2_seca_larga": [6, 7, 8, 9],
    "P3_tiempo_de_siembra": [10, 11, 12],
}


def _forzar_utf8() -> None:
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


class Cliente:
    def __init__(self, cache: Path | None):
        self.cache = cache
        self.llamadas = 0
        if cache:
            cache.mkdir(parents=True, exist_ok=True)

    def get(self, ruta: str, params: dict | None = None) -> dict:
        qs = urllib.parse.urlencode(params or {}, doseq=True)
        url = f"{API}/{ruta}" + (f"?{qs}" if qs else "")
        if self.cache:
            nombre = urllib.parse.quote(url, safe="")[-180:] + ".json"
            f = self.cache / nombre
            if f.exists():
                return json.loads(f.read_text(encoding="utf-8"))
        for intento in range(4):
            try:
                with urllib.request.urlopen(url, timeout=60) as r:
                    datos = json.loads(r.read().decode("utf-8"))
                break
            except Exception:
                if intento == 3:
                    raise
                time.sleep(2 * (intento + 1))
        self.llamadas += 1
        if self.cache:
            f.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return datos


def _facet(d: dict, campo: str) -> dict:
    for f in d.get("facets", []):
        if f["field"] == campo:
            return {c["name"]: c["count"] for c in f["counts"]}
    return {}


def _por_periodo(meses: dict[int, int]) -> dict:
    return {p: sum(meses.get(m, 0) for m in ms) for p, ms in PERIODOS.items()}


def _restar(a: dict, b: dict) -> dict:
    """a − b por clave, sin dejar ceros ni negativos."""
    return {k: a[k] - b.get(k, 0) for k in a if a[k] - b.get(k, 0) > 0}


def medir(cli: Cliente) -> dict:
    base = {**AVES, **CAJA}
    total = cli.get("occurrence/search", {**base, "limit": 0,
                                          "facet": ["speciesKey", "datasetKey", "month"],
                                          "facetLimit": 1000})
    # 🔴 Las AUSENCIAS disfrazadas de presencia. Medido el 2026-09-22: el
    # dataset de PANGAEA «Detection histories for eight species of Amazona
    # parrots… NeoMaps 2010» publica cada punto de muestreo como una fila
    # `occurrenceStatus: PRESENT` con `organismQuantity: 0`. Son NO-detecciones:
    # las ocho amazonas de Venezuela, a 60 filas cada una en la caja, incluidas
    # A. farinosa y A. mercenaria, que no viven en un cardonal. Se miden aparte
    # y se restan; si no, la cotorra de hombros amarillos «está» en Paraguaná
    # por un cero.
    ceros = cli.get("occurrence/search", {**base, "limit": 0, "organismQuantity": "0",
                                          "facet": ["speciesKey", "datasetKey", "month"],
                                          "facetLimit": 1000})
    ceros_sp = _facet(ceros, "SPECIES_KEY")
    especies = _restar(_facet(total, "SPECIES_KEY"), ceros_sp)
    datasets = _facet(total, "DATASET_KEY")
    ceros_ds = _facet(ceros, "DATASET_KEY")
    esfuerzo = _restar({int(k): v for k, v in _facet(total, "MONTH").items()},
                       {int(k): v for k, v in _facet(ceros, "MONTH").items()})

    fichas_ds = []
    for key, n in sorted(datasets.items(), key=lambda kv: -kv[1]):
        ds = cli.get(f"dataset/{key}")
        fichas_ds.append({
            "datasetKey": key,
            "titulo": ds.get("title"),
            "doi": ds.get("doi"),
            "licencia": ds.get("license"),
            "registros_aves_en_la_caja": n,
            "de_ellos_con_cantidad_cero": ceros_ds.get(key, 0),
        })

    solo_ceros = []
    for key, n in sorted(ceros_sp.items()):
        sp = cli.get(f"species/{key}")
        solo_ceros.append({
            "speciesKey": int(key),
            "cientifico": sp.get("canonicalName") or sp.get("scientificName"),
            "filas_con_cantidad_cero": n,
            "presencias_reales_en_la_caja": especies.get(key, 0),
        })

    filas = []
    for key, n in sorted(especies.items(), key=lambda kv: -kv[1]):
        sp = cli.get(f"species/{key}")
        occ = cli.get("occurrence/search", {**base, "speciesKey": key, "limit": 0,
                                            "facet": ["month", "year"], "facetLimit": 200})
        meses = {int(k): v for k, v in _facet(occ, "MONTH").items()}
        anios = sorted(int(k) for k in _facet(occ, "YEAR"))
        if key in ceros_sp:
            occ0 = cli.get("occurrence/search", {**base, "speciesKey": key, "limit": 0,
                                                 "organismQuantity": "0",
                                                 "facet": ["month", "year"], "facetLimit": 200})
            meses = _restar(meses, {int(k): v for k, v in _facet(occ0, "MONTH").items()})
            anios0 = _facet(occ0, "YEAR")
            anios_tot = _facet(occ, "YEAR")
            anios = sorted(int(k) for k in _restar(anios_tot, anios0))
        filas.append({
            "speciesKey": int(key),
            "cientifico": sp.get("canonicalName") or sp.get("scientificName"),
            "orden": sp.get("order"),
            "familia": sp.get("family"),
            "registros": n,
            "registros_con_mes": sum(meses.values()),
            "meses": {m: meses[m] for m in sorted(meses)},
            "meses_sin_registro": [m for m in range(1, 13) if m not in meses],
            "por_periodo": _por_periodo(meses),
            "anio_primero": anios[0] if anios else None,
            "anio_ultimo": anios[-1] if anios else None,
        })

    return {
        "meta": {
            "medido": time.strftime("%Y-%m-%d"),
            "script": "6-fusion/scripts/medir_gbif_aves_paraguana.py",
            "consulta": f"{API}/occurrence/search?classKey=212&decimalLatitude={CAJA['decimalLatitude']}&decimalLongitude={CAJA['decimalLongitude']}",
            "caja": "11,50-12,22 N / 70,32-69,78 O (península, istmo norte, Golfete y costa; fuera Coro y Aruba)",
            "periodos": {p: ms for p, ms in PERIODOS.items()},
            "regla_3": "GBIF dice que el ave cabe en este medio HOY; no dice que estuviera en el s. XV.",
            "regla_6": "un mes sin registro mide también el esfuerzo de observación: comparar con `esfuerzo_por_mes`.",
            "licencias": "cada dataset declara la suya (lista `datasets`); se citan por DOI.",
        },
        "total_filas_aves_en_gbif": total.get("count"),
        "filas_con_cantidad_cero": ceros.get("count"),
        "total_registros_aves": total.get("count") - ceros.get("count"),
        "especies_distintas": len(especies),
        "especies_solo_o_con_ceros": solo_ceros,
        "esfuerzo_por_mes": {m: esfuerzo[m] for m in sorted(esfuerzo)},
        "esfuerzo_por_periodo": _por_periodo(esfuerzo),
        "datasets": fichas_ds,
        "especies": filas,
    }


def main(argv=None) -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="mide y resume sin escribir")
    ap.add_argument("--cache", type=Path, help="directorio para guardar/releer las respuestas")
    a = ap.parse_args(argv)
    cli = Cliente(a.cache)
    datos = medir(cli)
    print(f"registros de aves en la caja: {datos['total_registros_aves']}")
    print(f"especies distintas:          {datos['especies_distintas']}")
    print(f"datasets:                    {len(datos['datasets'])}")
    print(f"llamadas a la API:           {cli.llamadas}")
    if not a.check:
        SALIDA.write_text(
            "# GENERADO por 6-fusion/scripts/medir_gbif_aves_paraguana.py — no editar a mano.\n"
            + yaml.safe_dump(datos, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8")
        print(f"escrito: {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
