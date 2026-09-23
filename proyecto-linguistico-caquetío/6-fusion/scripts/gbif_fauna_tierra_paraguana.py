# -*- coding: utf-8 -*-
"""La fauna de TIERRA de Paraguaná en GBIF: cuántas ocurrencias, de qué especies
y de qué conjuntos de datos, dentro de un polígono que cubre la península y el
istmo de los Médanos (campaña de fauna FA1, 2026-09-22).

Regla 1 del proyecto: ninguna cifra a mano. Las cuentas de GBIF que cita
`6-fusion/fauna_paraguana_tierra_2026-09-22.yaml` salen de aquí y viven en el
archivo que este script escribe; el inventario no las copia.

Qué mide:
  A. El total de ocurrencias del polígono y su reparto por CLASE.
  B. Para las clases de tierra (mamíferos, escamados, tortugas, anfibios,
     arácnidos, ciempiés, insectos y los caracoles de tierra), la lista de
     especies con su autoría (GBIF Backbone) y su número de ocurrencias.
  C. Los CONJUNTOS DE DATOS de donde vienen esas ocurrencias, con su título,
     su publicador y su licencia — para citar el dato como pide GBIF.
  D. Cada especie del inventario (`especies[].cientifico`) contra el polígono:
     su clave en el Backbone y cuántas ocurrencias tiene dentro. Un 0 aquí mide
     GBIF, no la península (regla 6): casi todo lo de GBIF es ciencia ciudadana
     reciente y alrededor de caminos.

Sin descarga: usa la API pública de búsqueda (`/occurrence/search` con
facetas), que no pide cuenta. Por eso no hay DOI de descarga: la cita es la
consulta, con su fecha, y la lista de conjuntos de datos.

Uso:
    python 6-fusion/scripts/gbif_fauna_tierra_paraguana.py            # escribe el YAML
    python 6-fusion/scripts/gbif_fauna_tierra_paraguana.py --check    # mide sin escribir
"""
import datetime
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

import yaml

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INVENTARIO = os.path.join(R, "6-fusion", "fauna_paraguana_tierra_2026-09-22.yaml")
SALIDA = os.path.join(R, "6-fusion", "gbif_fauna_tierra_paraguana_2026-09-22.yaml")
API = "https://api.gbif.org/v1"

# La península (con su costa) y el istmo de los Médanos hasta ~11,45° N, sin la
# ciudad de Coro (11,40° N). Vértices lon/lat, a mano y con margen de mar: el
# filtro por clase quita lo marino que caiga dentro.
POLIGONO = ("POLYGON((-70.32 11.60,-70.05 11.55,-69.86 11.52,-69.72 11.42,-69.62 11.47,"
            "-69.72 11.62,-69.70 11.90,-69.78 12.15,-70.05 12.25,-70.32 12.12,-70.32 11.60))")

# Las clases de TIERRA (claves del GBIF Backbone). Los caracoles van aparte
# porque Gastropoda mezcla mar y tierra: se quedan sólo sus familias terrestres.
CLASES_TIERRA = {
    359: "Mammalia",
    11592253: "Squamata",
    11418114: "Testudines",
    131: "Amphibia",
    367: "Arachnida",
    360: "Chilopoda",
    216: "Insecta",
}
GASTROPODA = 225
FAMILIAS_CARACOL_DE_TIERRA = {
    "Annulariidae", "Helicinidae", "Subulinidae", "Achatinidae", "Streptaxidae",
    "Cerionidae", "Pleurodontidae", "Camaenidae", "Urocoptidae", "Succineidae",
    "Veronicellidae", "Bulimulidae", "Orthalicidae", "Neocyclotidae", "Pupillidae",
    "Megalobulimidae", "Strophocheilidae", "Amphibulimidae", "Simpulopsidae",
    "Euconulidae", "Helicarionidae", "Charopidae", "Spiraxidae", "Oleacinidae",
    "Ferussaciidae", "Streptaxidae",
}

# Todo lo que no es fósil: observación, espécimen de colección, muestra, cita.
BASES_VIVAS = ["HUMAN_OBSERVATION", "OBSERVATION", "MACHINE_OBSERVATION", "PRESERVED_SPECIMEN",
               "MATERIAL_SAMPLE", "LIVING_SPECIMEN", "OCCURRENCE", "MATERIAL_CITATION"]

_cache = {}


def _get(ruta, params=None):
    url = API + ruta + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    if url in _cache:
        return _cache[url]
    for intento in range(4):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                _cache[url] = json.load(r)
                return _cache[url]
        except Exception:  # red intermitente: reintenta con espera
            if intento == 3:
                raise
            time.sleep(2 * (intento + 1))


def _especie(clave):
    s = _get(f"/species/{clave}")
    return {"clave": int(clave), "nombre": s.get("canonicalName"),
            "autoria": s.get("authorship") or None, "familia": s.get("family"),
            "orden": s.get("order")}


def _facetas(params, faceta, limite=1000):
    p = dict(params, limit=0, facet=faceta, facetLimit=limite)
    d = _get("/occurrence/search", p)
    filas = (d.get("facets") or [{}])[0].get("counts", [])
    # las claves de taxón son enteros; las de conjunto de datos, UUID
    return [(int(f["name"]) if str(f["name"]).isdigit() else f["name"], f["count"]) for f in filas]


def _clave_de(nombre):
    """Clave del Backbone para un nombre del inventario, o None. Sólo vale un
    acierto de rango especie (o género si el nombre es «Género sp.») cuyo
    género coincida: el emparejador de GBIF, con «Atta sp.», devolvía el
    filo Arthropoda y contaba 1.551 ocurrencias que no eran hormigas."""
    nombre = str(nombre).strip()
    if any(c in nombre for c in "(/,") or "indet" in nombre:
        return None
    genero_solo = nombre.endswith(" sp.")
    consulta = nombre[:-4] if genero_solo else nombre
    m = _get("/species/match", {"name": consulta, "strict": "true"})
    if m.get("matchType") in (None, "NONE", "HIGHERRANK"):
        return None
    if (m.get("canonicalName") or "").split(" ")[0] != consulta.split(" ")[0]:
        return None
    if m.get("rank") not in (("GENUS",) if genero_solo else ("SPECIES", "SUBSPECIES")):
        return None
    return m.get("usageKey")


def medir():
    # Sin fósiles: el Paleobiology Database pone en el polígono ocurrencias del
    # Mioceno (la formación Cantaure) que no son fauna viva. Se cuentan aparte.
    total_bruto = _get("/occurrence/search", {"geometry": POLIGONO, "limit": 0})["count"]
    base = {"geometry": POLIGONO, "basisOfRecord": BASES_VIVAS}
    total = _get("/occurrence/search", dict(base, limit=0))["count"]
    por_clase = {}
    for clave, n in _facetas(base, "classKey", 200):
        por_clase[_especie(clave)["nombre"] or str(clave)] = n

    # Trampa medida por la campaña de aves (PR #205): NeoMaps 2010 (PANGAEA)
    # marca cada punto de muestreo PRESENT con organismQuantity = 0 — ausencias
    # disfrazadas (480 filas de aves en este polígono). Antes de contar se mide
    # cuántas filas así hay en cada clase de tierra; si alguna tiene, las cifras
    # de abajo NO sirven y el script lo dice y sale con error.
    control = {}
    for clave, nombre in list(CLASES_TIERRA.items()) + [(GASTROPODA, "Gastropoda")]:
        cero = _get("/occurrence/search", dict(base, limit=0, classKey=clave, organismQuantity=0))["count"]
        ausente = _get("/occurrence/search", dict(base, limit=0, classKey=clave, occurrenceStatus="ABSENT"))["count"]
        control[nombre] = {"organismQuantity_0": cero, "occurrenceStatus_ABSENT": ausente}
    contaminadas = [k for k, v in control.items() if v["organismQuantity_0"] or v["occurrenceStatus_ABSENT"]]

    especies = {}
    for clave, nombre in CLASES_TIERRA.items():
        filas = []
        for sp, n in _facetas(dict(base, classKey=clave), "speciesKey"):
            e = _especie(sp)
            e["ocurrencias"] = n
            filas.append(e)
        especies[nombre] = filas
    caracoles = []
    for sp, n in _facetas(dict(base, classKey=GASTROPODA), "speciesKey"):
        e = _especie(sp)
        if e["familia"] in FAMILIAS_CARACOL_DE_TIERRA:
            e["ocurrencias"] = n
            caracoles.append(e)
    especies["Gastropoda (familias de tierra)"] = caracoles

    datasets = []
    vistos = {}
    for clave in list(CLASES_TIERRA) + [GASTROPODA]:
        for ds, n in _facetas(dict(base, classKey=clave), "datasetKey", 300):
            vistos[ds] = vistos.get(ds, 0) + n
    for ds, n in sorted(vistos.items(), key=lambda x: -x[1]):
        d = _get(f"/dataset/{ds}")
        org = d.get("publishingOrganizationKey")
        pub = _get(f"/organization/{org}").get("title") if org else None
        datasets.append({"clave": ds, "titulo": d.get("title"), "publicador": pub,
                         "licencia": d.get("license"), "doi": d.get("doi"),
                         "ocurrencias_de_tierra": n})

    inventario = []
    if os.path.exists(INVENTARIO):
        inv = yaml.safe_load(io.open(INVENTARIO, encoding="utf-8")) or {}
        for e in inv.get("especies") or []:
            nombre = e.get("gbif_nombre") or e.get("cientifico")
            if not nombre or " " not in str(nombre).strip():
                continue
            clave = _clave_de(nombre)
            n = (_get("/occurrence/search", dict(base, limit=0, taxonKey=clave))["count"]
                 if clave else None)
            inventario.append({"id": e.get("id"), "cientifico": nombre,
                               "clave_gbif": clave, "ocurrencias_en_poligono": n})

    return {
        "generado_por": "6-fusion/scripts/gbif_fauna_tierra_paraguana.py — no se edita a mano",
        "consultado": datetime.date.today().isoformat(),
        "api": API + "/occurrence/search (facetas, sin descarga)",
        "poligono_wkt": POLIGONO,
        "aviso": ("Sin DOI de descarga: la API de búsqueda no lo da y una descarga pide cuenta. "
                  "Se cita la consulta con su fecha y los conjuntos de datos de abajo. Casi todo es "
                  "ciencia ciudadana (iNaturalist) y colecciones del s. XX-XXI: es censo MODERNO, "
                  "no del s. XV (regla 3), y un 0 mide GBIF, no la península (regla 6)."),
        "control_de_ausencias": {
            "por_clase": control,
            "clases_contaminadas": contaminadas,
            "lectura": ("Las facetas no se pueden filtrar por «distinto de cero», así que se mide antes: "
                        "si una clase de tierra tuviera filas con organismQuantity 0 u occurrenceStatus "
                        "ABSENT, sus cifras habría que rehacerlas por registro. En aves (fuera de esta "
                        "parcela) son 480 filas de NeoMaps 2010."),
        },
        "total_ocurrencias_poligono_con_fosiles": total_bruto,
        "total_ocurrencias_poligono": total,
        "bases_de_registro_contadas": BASES_VIVAS,
        "por_clase": por_clase,
        "especies_de_tierra": especies,
        "conjuntos_de_datos": datasets,
        "inventario_contra_gbif": inventario,
    }


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = argv or sys.argv[1:]
    d = medir()
    n_sp = sum(len(v) for v in d["especies_de_tierra"].values())
    print(f"total del polígono: {d['total_ocurrencias_poligono']}")
    for k, v in d["especies_de_tierra"].items():
        print(f"  {k}: {len(v)} especies, {sum(e['ocurrencias'] for e in v)} ocurrencias")
    print(f"especies de tierra: {n_sp}; conjuntos de datos: {len(d['conjuntos_de_datos'])}")
    ceros = [e["cientifico"] for e in d["inventario_contra_gbif"] if not e["ocurrencias_en_poligono"]]
    print(f"inventario: {len(d['inventario_contra_gbif'])} especies; sin ocurrencia en el polígono: {len(ceros)}")
    cont = d["control_de_ausencias"]["clases_contaminadas"]
    print(f"control de ausencias (organismQuantity 0 / ABSENT): {'LIMPIO' if not cont else 'CONTAMINADAS: ' + ', '.join(cont)}")
    if cont:
        print("⚠️ Hay ausencias disfrazadas en clases de tierra: las cifras por faceta no valen. No se escribe.")
        return 1
    if "--check" in argv:
        return 0
    with io.open(SALIDA, "w", encoding="utf-8") as f:
        f.write("# GENERADO por 6-fusion/scripts/gbif_fauna_tierra_paraguana.py — no se edita a mano.\n")
        yaml.safe_dump(d, f, allow_unicode=True, sort_keys=False, width=100)
    print(f"escrito: {os.path.relpath(SALIDA, R)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
