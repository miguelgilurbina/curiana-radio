# -*- coding: utf-8 -*-
"""
Los xaguas de Carora y Pedregal: las cifras de la minería del 2026-10-09.

Dos mediciones, para que ninguna cifra de 6-fusion/xaguas_achaguas_falcon_2026-10-09.yaml
se escriba a mano (regla 1):

1. SONDAS (minar-fuente §2): cuántas veces sale cada grafía del etnónimo
   (xagua, axagua, ajagua, achagua, jagua) y cada lugar de la pregunta en las
   fuentes del repo que se leyeron. Los PDF con capa de texto se pasan por
   pdftotext (a un directorio temporal: nada se escribe en fuentes_caquetios/);
   los .txt y .ocr.txt se leen tal cual. Un cero aquí mide la sonda, no la
   fuente: por eso se cuentan todas las grafías y no sólo una.

2. EL AZAR DE LOS NOMBRES DE ALDEA. Las únicas «palabras» xaguas que da una
   fuente del repo son dos nombres de aldea SIN GLOSA (Federmann 1557 [44]-[45]:
   Coary y Cacaridi). Sin glosa no hay concepto, y sin concepto no hay cruce
   (minar-fuente §2). Lo que sí se puede medir es cuánto se «parecen» al
   achagua de Neira y Ribero por pura forma, y compararlo con lo que se parecen
   los nombres de aldea de los OTROS pueblos de la misma crónica (jirajaras,
   ayamanes, caquetíos), que nadie propone como achaguas. Si los xaguas no se
   parecen más que el control, el parecido no dice nada. Mismo instrumento que
   el cruce del 09-13 (fon, copista, radicales y umbrales de
   cruzar_achagua_caquetio.py), importado, no copiado.

3. DÓNDE. Las coordenadas de los lugares de la pregunta (OSM: el volcado del
   repo o Nominatim, con su id) y su distancia en km al pueblo de Mitare y a
   Pedregal, para que «cerca de Mitare» se pueda leer con cifra.

Salida: 6-fusion/medicion_xaguas_achaguas_2026-10-09.yaml (PROPUESTA, regla 5).

    python 6-fusion/scripts/medir_xaguas_2026-10-09.py
"""
import difflib
import io
import os
import re
import statistics
import subprocess
import sys
import tempfile

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
import cruzar_achagua_caquetio as CX  # noqa: E402

F = os.path.join(R, "fuentes_caquetios")
SALIDA = os.path.join(R, "6-fusion", "medicion_xaguas_achaguas_2026-10-09.yaml")
FECHA = "2026-10-09"

FUENTES = {  # obra (clave de bibliografia.yaml) -> archivo del repo
    "federmann-1916 (Arcaya, trad.)": "Federmann_1916_Narracion_Primer_Viaje_Arcaya.txt",
    "federmann-1916 (Klüpfel 1859, alemán)": "Federmann_Kluepfel_1859_Reisen_texto_aleman.txt",
    "oliver-1989-cap3-vecinos (tesis, OCR §3.3)": "Oliver_1989_cap3_s33_falcon_lara.ocr.txt",
    "oliver-1989-cap3 (DOC 2006)": "Chapter 3 Ethnohistory.DOC-comprimido.pdf",
    "jahn-1927": "Jahn_1927_Aborigenes_Occidente_Venezuela.pdf",
    "arcaya-1920": "Arcaya_1920_Historia_Estado_Falcon.pdf",
    "perez-de-tolosa-1546 (Fernández Duro t. II)": "Oviedo_Banos_1885_FernandezDuro_t2_Documentos.txt",
    "aguado-1581": "Aguado_1918_Historia_Venezuela_t1_gutenberg.txt",
    "rivero-1883": "Rivero_1883_Historia_Misiones_Casanare.txt",
    "urbina-jimenez-2007-2011 (2011)": "Urbina_2011_Archaeological_Survey_Coastal_Falcon_UCL.txt",
    "esteves-1989 (seis partes, OCR)": "Esteves_1989_Toponimos_Paraguana_{1..6}.ocr.txt",
}

# Grafías del etnónimo, como palabra (no dentro de otra): «jagua» sola no
# cuenta dentro de «ajagua». Se cuentan también las partidas por el OCR.
ETNONIMO = {
    "xagua": r"(?<![a-zñ])xaguas?\b",
    "axagua": r"(?<![a-zñ])axaguas?\b",
    "ajagua": r"(?<![a-zñ])aj\s?aguas?\b",
    "achagua": r"(?<![a-zñ])acha?guas?\b",
    "jagua": r"(?<![a-zñ])jaguas?\b",
    "achagual": r"(?<![a-zñ])achagual\b",
}
LUGARES = ["mitare", "pedregal", "carora", "baragua", "barragua", "siruma", "ciruma",
           "empalado", "cariagua", "mapiare", "sibur[uú]a", "utaquire", "autaquire",
           "acurigua", "quiragua", "avaria|abar[ií]a", "tupure", "coary", "cacaridi|cocaride"]

# ── el control del azar: nombres de aldea de la misma crónica (Federmann 1530) ──
XAGUAS = ["Coary", "Cacaridi"]
CONTROL = {  # pueblo -> nombres de aldea o de provincia que da la misma crónica
    "jirajara": ["Hittova"],
    "ayamán": ["Carohana"],
    "caquetío (Barquisimeto y Llanos)": ["Vararida", "Itabana", "Variquecemeto"],
    "caquetío (costa, otras crónicas del repo)": ["Todariquiba", "Mitare", "Capatarida",
                                                  "Zazarida", "Cumarebo", "Guaibacoa",
                                                  "Moruy", "Miraca"],
}


# ── 3. dónde: coordenadas con su origen (OSM, ODbL) y distancias medidas ──
# «volcado» = fuentes_caquetios/osm_kaketiana (osm-kaketiana, 2026-09-07);
# «nominatim» = consulta a nominatim.openstreetmap.org el 2026-10-09 (mismo OSM).
COORD = {
    "Mitare (pueblo)": (11.3499199, -70.0327014, "volcado: node 3948744958"),
    "Agua Clara": (11.1602136, -69.9690056, "nominatim: node 9087415620"),
    "Pedregal": (11.0237511, -70.1166009, "volcado: node 3948666957"),
    "Pecaya": (11.0769628, -69.8649275, "nominatim: node 3948667760"),
    "Parroquia Avaria (centroide)": (10.7898035, -70.4165066, "nominatim: relation 11050822"),
    "San Luis (Cariagua, según Esteves y Oliver)": (11.1203301, -69.6843215, "nominatim: node 5327484731"),
    "Acurigua": (11.30491, -69.4613565, "volcado: node 3942824345"),
    "Quiragua (la de Miranda/Zamora del volcado)": (11.443864, -69.3448556, "volcado: node 5878373894"),
    "Churuguara (Mapiare, según Esteves)": (10.8116686, -69.5382564, "nominatim: node 1616158444"),
    "Baragua (capital de la parroquia Xaguas)": (10.5832137, -69.9484037, "nominatim: node 5334941552"),
    "Parroquia Xaguas (centroide)": (10.5798039, -70.0624958, "nominatim: relation 11073231"),
    "Siquisique": (10.5742281, -69.7027348, "nominatim: node 5334939689"),
    "Río Tocuyo (pueblo)": (10.2695086, -69.9358819, "nominatim: node 5333399379"),
    "Aregue": (10.2399757, -70.0339392, "nominatim: node 5227096721"),
    "Carora": (10.1695340, -70.0728483, "nominatim: node 2612573805"),
}


def km(a, b):
    import math
    (la1, lo1), (la2, lo2) = a[:2], b[:2]
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(lo2 - lo1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * 6371.0088 * math.asin(math.sqrt(h)), 1)


def lugares():
    mit, ped = COORD["Mitare (pueblo)"], COORD["Pedregal"]
    return {n: {"lat": c[0], "lon": c[1], "origen": c[2],
                "km_a_Mitare": km(c, mit), "km_a_Pedregal": km(c, ped)}
            for n, c in COORD.items()}


def texto(archivo, tmp):
    if "{1..6}" in archivo:
        return "\n".join(texto(archivo.replace("{1..6}", str(i)), tmp) for i in range(1, 7))
    ruta = os.path.join(F, archivo)
    if archivo.endswith(".pdf"):
        out = os.path.join(tmp, re.sub(r"\W+", "_", archivo) + ".txt")
        subprocess.run(["pdftotext", "-enc", "UTF-8", ruta, out], check=True)
        ruta = out
    return io.open(ruta, encoding="utf-8", errors="replace").read()


def sondas():
    res = {}
    with tempfile.TemporaryDirectory() as tmp:
        for obra, arch in FUENTES.items():
            t = re.sub(r"\s+", " ", texto(arch, tmp)).lower()
            res[obra] = {
                "archivo": arch,
                "etnonimo": {k: len(re.findall(p, t)) for k, p in ETNONIMO.items()},
                "lugares": {k.split("|")[0]: len(re.findall(r"(?<![a-zñ])(?:%s)" % k, t)) for k in LUGARES},
            }
    return res


def parecido(nombre, entradas):
    fa = CX.fon(CX.copista(nombre), "colonial", CX.GU_ES_W)
    sm = difflib.SequenceMatcher(None, autojunk=False)
    sm.set_seq2(fa)
    best, ge_p, ge_c = (-1.0, None, None), 0, 0
    for e in entradas:
        mejor_e = -1.0
        for fb, mb, _rad in e["cands"]:
            sm.set_seq1(fb)
            r = sm.ratio()
            if r > mejor_e:
                mejor_e = r
            if r > best[0]:
                best = (r, mb, e["glosa"])
        ge_p += mejor_e >= CX.UMBRAL_PARECIDO
        ge_c += mejor_e >= CX.UMBRAL_COGNADO
    return {"forma_fonemizada": fa, "mejor_similitud": round(best[0], 3),
            "mejor_achagua": best[1], "su_glosa": best[2][:60] if best[2] else None,
            "entradas_ge_umbral_parecido": ge_p, "entradas_ge_umbral_cognado": ge_c}


def azar():
    entradas, n_vocab = CX.cargar_achagua(CX.GU_ES_W)
    comparables = [e for e in entradas if e["cands"]]
    x = {n: parecido(n, comparables) for n in XAGUAS}
    c = {}
    for pueblo, nombres in CONTROL.items():
        for n in nombres:
            c[n] = dict(parecido(n, comparables), pueblo=pueblo)
    ctrl_sim = [v["mejor_similitud"] for v in c.values()]
    ctrl_ge = [v["entradas_ge_umbral_parecido"] for v in c.values()]
    resumen = {
        "entradas_neira_con_forma_comparable": len(comparables),
        "entradas_del_vocabulario": n_vocab,
        "umbral_parecido": CX.UMBRAL_PARECIDO, "umbral_cognado": CX.UMBRAL_COGNADO,
        "control_n_nombres": len(c),
        "control_mejor_similitud_media": round(statistics.mean(ctrl_sim), 3),
        "control_mejor_similitud_min_max": [min(ctrl_sim), max(ctrl_sim)],
        "control_entradas_ge_umbral_parecido_mediana": statistics.median(ctrl_ge),
        "control_nombres_con_alguna_entrada_ge_umbral_cognado": sum(
            v["entradas_ge_umbral_cognado"] > 0 for v in c.values()),
        "xaguas_mejor_similitud": {n: v["mejor_similitud"] for n, v in x.items()},
        "xaguas_por_encima_del_maximo_del_control": [
            n for n, v in x.items() if v["mejor_similitud"] > max(ctrl_sim)],
    }
    return {"resumen": resumen, "xaguas": x, "control": c}


def main():
    S = sondas()
    A = azar()
    doc = {
        "meta": {
            "medido": FECHA,
            "script": "6-fusion/scripts/medir_xaguas_2026-10-09.py",
            "estado": "PROPUESTA (regla 5). Cifras emitidas por el script; no se editan a mano.",
            "propuesta": "6-fusion/xaguas_achaguas_falcon_2026-10-09.yaml",
            "aviso_sondas": ("conteo sin distinguir mayúsculas sobre el texto con los blancos colapsados; "
                             "«achagua» incluye «achaga» (Gumilla, Arcaya); «ajagua» incluye «aj agua» "
                             "partido por pdftotext; «jagua» cuenta la palabra suelta: en Aguado y "
                             "Oviedo es el TINTE (Genipa), no el pueblo — leer el pasaje."),
            "aviso_azar": ("NO es un cruce: los dos nombres xaguas no tienen glosa. Mide cuánto se "
                           "parece CUALQUIER nombre de aldea de la crónica al achagua de Neira por "
                           "pura forma, para que nadie lea un parecido de Coary o Cacaridi como "
                           "indicio."),
        },
        "sondas": S,
        "azar_nombres_de_aldea": A,
        "lugares": lugares(),
    }
    with io.open(SALIDA, "w", encoding="utf-8") as fh:
        fh.write("# Generado por 6-fusion/scripts/medir_xaguas_2026-10-09.py — no se edita a mano.\n")
        yaml.safe_dump(doc, fh, allow_unicode=True, sort_keys=False, width=110)
    r = A["resumen"]
    print("═══ SONDAS (etnónimo) ═══")
    for obra, v in S.items():
        print(f"  {obra:<46} " + " ".join(f"{k}={n}" for k, n in v["etnonimo"].items()))
    print("\n═══ AZAR: nombres de aldea contra Neira y Ribero ═══")
    for n, v in list(A["xaguas"].items()) + list(A["control"].items()):
        print(f"  {n:<14} {v['forma_fonemizada']:<14} mejor {v['mejor_similitud']:.3f} ~ {v['mejor_achagua']!s:<14}"
              f" «{(v['su_glosa'] or '')[:24]}»  ≥{CX.UMBRAL_PARECIDO}: {v['entradas_ge_umbral_parecido']:>3}"
              f"  ≥{CX.UMBRAL_COGNADO}: {v['entradas_ge_umbral_cognado']:>2}  {v.get('pueblo', 'XAGUA')}")
    print(f"\n  control: media {r['control_mejor_similitud_media']}, rango {r['control_mejor_similitud_min_max']};"
          f" xaguas por encima del máximo del control: {r['xaguas_por_encima_del_maximo_del_control']}")
    print(f"\n✓ {os.path.relpath(SALIDA, R)}")


if __name__ == "__main__":
    main()
