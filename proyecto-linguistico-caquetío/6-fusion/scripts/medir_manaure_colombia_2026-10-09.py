# -*- coding: utf-8 -*-
"""
Los Manaure de Colombia: las cifras de la minería del 2026-10-09.

Para que ninguna cifra de 6-fusion/manaure_colombia_2026-10-09.yaml se escriba
a mano (regla 1). Cuatro mediciones:

1. SONDAS (minar-fuente §2, regla 6). Cuántas veces sale cada grafía del
   nombre (Manaure, Manavre, Manahure, Manaore, Managuare, Managuanare,
   Managuarire, Mauaure) en CADA texto de fuentes_caquetios/. Los PDF que no
   tienen .txt al lado se pasan por pdftotext a un directorio temporal (nada se
   escribe en fuentes_caquetios/). Normalización NFD sin diacríticos. Aparte, la
   voz homógrafa «manare» (el cernidor; Alvarado 1921 p. 199 dice que Carvajal
   la escribe «incorrectamente manaure»): se cuenta sola para que no infle la
   cuenta del nombre.

2. EL OESTE. Cada aparición del nombre que tenga a menos de 600 caracteres una
   palabra de la esfera occidental (Guajira, Hacha, Cabo de la Vela, Maracaibo,
   Upar, Perijá, Coquibacoa, bubures, buredes, coanaos…). Es la lista que hay
   que leer a mano: un acierto aquí NO es un Manaure occidental, es un pasaje
   que hay que mirar.

3. LA FAMILIA -AURE. Toda palabra de la forma X-aure (con u o v, con o sin h)
   en las mismas fuentes, cuántas veces, y en cuántas obras sale cerca de una
   palabra de la esfera occidental. Es el barrido que encontró «Mapaure, tierra
   de Xuduara» en Oviedo y Valdés.

4. DÓNDE. Coordenadas de OSM (con su id y si vienen de Nominatim o de Overpass,
   consultados el 2026-10-09) y distancias en km entre los Manaure y los lugares
   que la pregunta toca.

Salida: 6-fusion/medicion_manaure_colombia_2026-10-09.yaml (PROPUESTA, regla 5).

    python 6-fusion/scripts/medir_manaure_colombia_2026-10-09.py
"""
import collections
import io
import math
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(AQUI, "..", ".."))
F = os.path.join(R, "fuentes_caquetios")
SALIDA = os.path.join(R, "6-fusion", "medicion_manaure_colombia_2026-10-09.yaml")
FECHA = "2026-10-09"

# ── 1. las grafías del nombre ──
GRAFIAS = {
    "manaure": r"\bmanaures?\b",
    "manavre": r"\bmanavres?\b",
    "manahure": r"\bmanahures?\b",
    "manaore": r"\bmanaores?\b",
    "managuare": r"\bmanaguares?\b",
    "managuanare|managuarire": r"\bmanagua(?:nare|rire)s?\b",
    "mauaure (OCR de Castellanos 1857)": r"\bmauaures?\b",
}
HOMOGRAFA = {"manare (homógrafa: casi siempre el cernidor; Morón la da también como «Arco Manare»)": r"\bmanares?\b"}
NOMBRE = re.compile(r"\bmana(?:[uv]h?re|ore|guare|guanare|guarire)s?\b|\bmauaure\b")

# ── 2. la esfera occidental ──
OESTE = re.compile(
    r"guajir|goajir|guagir|rio ?(?:de ?la ?)?hacha|riohacha|rio-hacha|cabo de la vela|maracaib|maracayb|"
    r"\bupar\b|valledupar|perij|"
    r"coquiba|quoquiba|santa marta|cesar\b|cezar|rancher[ií]a|bubur|bugur|bobur|bured|"
    r"coanao|guanebuc|wanebuc|juruara|xuduara|axuduara|churuar|pemen|quiriqu|onoto")
VENTANA = 600

# ── 3. la familia -aure ──
FAMILIA = re.compile(r"\b([a-z]{1,12}a[uv]h?re)s?\b")
NO_INDIGENAS = {"laure", "faure", "taure", "restaure", "centaure", "cadaure"}  # francés/OCR


def norm(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def textos(tmp):
    """(archivo, texto normalizado) de cada fuente con capa de texto del repo."""
    out = []
    nombres = sorted(os.listdir(F))
    for a in nombres:
        ruta = os.path.join(F, a)
        if a.endswith(".txt"):
            out.append((a, norm(io.open(ruta, encoding="utf-8", errors="replace").read())))
        elif a.endswith(".pdf"):
            base = a[:-4]
            if base + ".txt" in nombres or base + ".ocr.txt" in nombres:
                continue
            dest = os.path.join(tmp, "%03d.txt" % len(out))
            # cwd=F y nombre relativo: el pdftotext de esta máquina no abre rutas con «í»
            r = subprocess.run(["pdftotext", "-enc", "UTF-8", a, dest], cwd=F,
                               capture_output=True)
            if r.returncode == 0 and os.path.exists(dest):
                out.append((a, norm(io.open(dest, encoding="utf-8", errors="replace").read())))
            else:
                out.append((a + " [pdftotext falló]", ""))
    return out


def sondas(ts):
    por_obra, total = {}, collections.Counter()
    for a, t in ts:
        fila = {k: len(re.findall(p, t)) for k, p in GRAFIAS.items()}
        fila.update({k: len(re.findall(p, t)) for k, p in HOMOGRAFA.items()})
        if any(fila.values()):
            por_obra[a] = {k: v for k, v in fila.items() if v}
        total.update(fila)
    return {"total_por_grafia": dict(total), "por_obra": por_obra,
            "obras_leidas": len(ts),
            "obras_sin_texto": [a for a, t in ts if not t]}


def oeste(ts):
    hits = []
    for a, t in ts:
        for m in NOMBRE.finditer(t):
            v = t[max(0, m.start() - VENTANA):m.end() + VENTANA]
            ks = sorted(set(k.group(0) for k in OESTE.finditer(v)))
            if ks:
                frag = re.sub(r"\s+", " ", t[max(0, m.start() - 160):m.end() + 160])
                hits.append({"obra": a, "forma": m.group(0), "posicion": m.start(),
                             "palabras_del_oeste": ks, "fragmento": frag})
    return {"ventana_caracteres": VENTANA, "n": len(hits), "aciertos": hits}


def familia(ts):
    cnt, obras, obras_oeste = collections.Counter(), collections.defaultdict(set), collections.defaultdict(set)
    for a, t in ts:
        for m in FAMILIA.finditer(t):
            w = m.group(1).replace("v", "u")
            if w in NO_INDIGENAS:
                continue
            cnt[w] += 1
            obras[w].add(a)
            if OESTE.search(t[max(0, m.start() - VENTANA):m.end() + VENTANA]):
                obras_oeste[w].add(a)
    filas = []
    for w, n in cnt.most_common():
        if n < 2 and w not in obras_oeste:
            continue
        filas.append({"forma": w, "veces": n, "obras": len(obras[w]),
                      "obras_con_contexto_occidental": sorted(obras_oeste.get(w, []))})
    return {"excluidas_por_no_indigenas": sorted(NO_INDIGENAS),
            "formas_distintas": len(cnt),
            "formas_con_contexto_occidental": sorted(obras_oeste),
            "tabla_(veces>=2_o_occidental)": filas}


# ── 4. dónde ──
COORD = {
    "Manaure (La Guajira)": (11.7771128, -72.4469366, "overpass: node 313909383 (place=town)"),
    "Manaure Balcón del Cesar": (10.3910411, -73.0270699, "overpass: node 468769318 (place=town)"),
    "Río Manaure (Cesar), un tramo": (10.3876865, -73.0526320, "overpass: way 279294636 (centro)"),
    "La Paz (Cesar), municipio": (10.3866045, -73.1710014, "nominatim: relation 11890104 (centroide)"),
    "Cabo de la Vela (el cabo)": (12.2071342, -72.1802153, "nominatim: node 1181556217"),
    "Coro": (11.4055796, -69.6679115, "nominatim: way 1374792076"),
    "Yaracal (cabecera del municipio Cacique Manaure, Falcón)": (10.9749340, -68.5452435, "nominatim: way 1426715582"),
    "Bobures (Zulia, costa sur del lago)": (9.2396047, -71.1728089, "nominatim: node 930222815"),
}
PARES = [
    ("Manaure (La Guajira)", "Coro"),
    ("Manaure (La Guajira)", "Cabo de la Vela (el cabo)"),
    ("Manaure Balcón del Cesar", "Coro"),
    ("Manaure Balcón del Cesar", "La Paz (Cesar), municipio"),
    ("Manaure Balcón del Cesar", "Bobures (Zulia, costa sur del lago)"),
    ("Manaure (La Guajira)", "Manaure Balcón del Cesar"),
    ("Coro", "Yaracal (cabecera del municipio Cacique Manaure, Falcón)"),
]
OVERPASS_OESTE = {
    "consultado": FECHA,
    "servidor": "overpass.kumi.systems (el de overpass-api.de dio 504)",
    "caja_s_o_n_e": [8.5, -74.5, 12.6, -70.9],
    "consultas": [
        'node[place][name~"aure",i](caja)',
        '(node[name~"aure",i][natural](caja); way[name~"aure",i][waterway](caja); node[name~"ure$",i][place](caja))',
    ],
    "respuesta_literal": [
        "Manaure | node 313909383 | 11.7771128, -72.4469366 | town",
        "Manaure Balcón del Cesar | node 468769318 | 10.3910411, -73.0270699 | town",
        "Los Laureles | node 703271144 | locality", "El Laurel | node 703272754 | locality",
        "Cashaurechon | node 703381222 | locality", "Juguey Maurepa | node 703382683 | locality",
        "Los Laureles | node 703490444 | locality", "Finca Los Laureles | node 9142959540 | isolated_dwelling",
        "Mauren | node 10563311320 | hamlet",
        "Atasure | node 703380690 | locality", "Merrure | node 703382313 | locality",
        "Río Manaure | way 279294636 | river", "Río Manaure | way 871531038 | river",
    ],
}


def km(a, b):
    (la1, lo1), (la2, lo2) = a[:2], b[:2]
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(lo2 - lo1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * 6371.0088 * math.asin(math.sqrt(h)), 1)


def donde():
    # un nombre cuenta si ALGUNA de sus palabras acaba en -aure («Río Manaure» sí, «Los Laureles» no)
    con_palabra_en_aure = sorted({l.split(" | ")[0] for l in OVERPASS_OESTE["respuesta_literal"]
                                  if re.search(r"aure\b", l.split(" | ")[0], re.I)})
    return {"lugares": {n: {"lat": c[0], "lon": c[1], "origen": c[2]} for n, c in COORD.items()},
            "distancias_km": [{"de": a, "a": b, "km": km(COORD[a], COORD[b])} for a, b in PARES],
            "overpass_oeste": dict(OVERPASS_OESTE,
                                   nombres_con_una_palabra_en_aure=con_palabra_en_aure,
                                   n_nombres_distintos=len(con_palabra_en_aure))}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        ts = textos(tmp)
    doc = {
        "meta": {
            "fecha": FECHA,
            "script": "6-fusion/scripts/medir_manaure_colombia_2026-10-09.py",
            "propuesta": "6-fusion/manaure_colombia_2026-10-09.yaml",
            "aviso": "Medición, no canon (regla 5). Un acierto de sonda lleva a un pasaje; el dato está en el pasaje.",
        },
        "sondas": sondas(ts),
        "oeste": oeste(ts),
        "familia_aure": familia(ts),
        "donde": donde(),
    }
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# GENERADO por 6-fusion/scripts/medir_manaure_colombia_2026-10-09.py — no editar a mano.\n")
        yaml.safe_dump(doc, fh, allow_unicode=True, sort_keys=False, width=110)
    s = doc["sondas"]
    print("obras leídas:", s["obras_leidas"], "| sin texto:", len(s["obras_sin_texto"]))
    print("grafías:", s["total_por_grafia"])
    print("aciertos con contexto occidental:", doc["oeste"]["n"])
    print("-aure con contexto occidental:", doc["familia_aure"]["formas_con_contexto_occidental"])
    for d in doc["donde"]["distancias_km"]:
        print("  %s -> %s: %s km" % (d["de"], d["a"], d["km"]))
    print("escrito:", os.path.relpath(SALIDA, R))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
