#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
El test de dependencia de OVIEDO A LAS DOS ORILLAS (minería del taíno para
la creencia caquetía, 2026-10-09):

    6-fusion/creencia_taino_2026-10-09.yaml

La pregunta (nota de decisión 4-fuentes/sesiones/08_creencia_taino_que-minar.md
§4, 1.º): cuando Oviedo describe el rito de los indios de Venezuela (t. II,
lib. XXV, cap. IX), ¿lo describe con la plantilla que ya había escrito para
La Española (t. I, lib. V)?

El instrumento es un SOLAPAMIENTO DE BIGRAMAS de palabras de contenido entre
cada tramo y el de La Española, con dos CONTROLES del mismo autor y del mismo
tomo: el cap. XII del lib. XXIV (los piaches de Camanagoto, gente caribe:
otro pueblo descrito con el mismo molde) y el cap. X del lib. XXV (la entrada
de Jorge Espira: narración militar, sin rito). Si el tramo venezolano
comparte con La Española más que la narración y lo mismo que Camanagoto, lo
que se comparte es del cronista, no de los pueblos. Además cuenta, tramo por
tramo, las voces de La Española que Oviedo usa y las veces que alega a Plinio
sobre el «arte mágico».

Un recuento NO es un hallazgo: los pasajes se leyeron y se vieron en imagen,
y el veredicto va en el YAML (`oviedo_dos_orillas`). Este script da las
cifras (regla 1) y valida el YAML (regla 8: toda `fuente` existe en
4-fuentes/bibliografia.yaml; todo id de `via_a` existe en
3-mundo/corpus/creencia.yaml).

No llama a ninguna API, no lee curiana_sim/.env, no toca la base. Necesita
PyMuPDF (`import pymupdf`) y PyYAML.

    python 6-fusion/scripts/medir_plantilla_oviedo.py            # valida el YAML y compara con meta.medido
    python 6-fusion/scripts/medir_plantilla_oviedo.py --conteos  # imprime el bloque medido (YAML)
"""

import argparse
import io
import os
import re
import sys
import unicodedata

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
FUENTES = os.path.join(RAIZ, "fuentes_caquetios")
PROPUESTA = os.path.join(RAIZ, "6-fusion", "creencia_taino_2026-10-09.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")
CREENCIA = os.path.join(RAIZ, "3-mundo", "corpus", "creencia.yaml")

T1 = "Oviedo_Valdes_1851_Historia_General_Indias_vol1_completo.pdf"
T2 = "Oviedo_Valdes_1852_Historia_General_Indias_vol2.pdf"

# Desfase medido sobre las cabeceras impresas (2026-10-09), índice 0 del PDF:
#   t. I copia íntegra: índice = impresa + 119  (pdf 245 = impresa 125)
#   t. II:              índice = impresa + 13   (pdf 311 = impresa 297)
TRAMOS = {
    "t1_lib5_la_espanola": (T1, 119, 125, 139,
                            "t. I lib. V caps. I-III: çemi, buhití, areyto, tabaco, entierro del cacique, oráculo"),
    "t2_lib25_cap9_venezuela": (T2, 13, 297, 301,
                                "t. II lib. XXV cap. IX: funeral de los çaquitios, boratio, tabaco, cura, díao"),
    "t2_lib24_cap12_camanagoto": (T2, 13, 254, 256,
                                  "control 1, t. II lib. XXIV cap. XII: los piaches de Camanagoto (caribes)"),
    "t2_lib25_cap10_espira": (T2, 13, 302, 305,
                              "control 2, t. II lib. XXV cap. X: la entrada de Espira (narración, sin rito)"),
}
REFERENCIA = "t1_lib5_la_espanola"

# Voces de La Española (raíces normalizadas con la misma función de abajo).
# Las variantes de OCR medidas en estas páginas van en el patrón: la capa del
# t. I lee `çemi` como `remi`/`ceniies` y `buhío` como `buliiu`; la h- inicial
# ya la quitó normalizar() (hamaca → amaca).
VOCES_ISLA = {
    "buhio": r"\bbu[h]?io|\bbuliiu",
    "tabaco": r"\btabac",
    "ahumada": r"\bahumad",
    "cemi": r"\b[cr]emi(es|s)?\b|\bceniies\b",
    "areito": r"\bareit|\barcit|\bareil",
    "duho": r"\bduho|\bdulio",
    "hamaca": r"\bamac|\bamic",
    "macana": r"\bmacan",
}
# Plinio alegado sobre la medicina y el arte mágico (Nat. Hist. XXX, 1): se
# cuenta la mención de Plinio a menos de 400 caracteres de «magic»/«medicin».
PLINIO_MAGIA = r"plinio"
VENTANA_PLINIO = 400

VACIAS = set("""
aquel aquella aquellas aquellos aqueste aquesta aquesto assi alguna algunas
alguno algunos alli antes aunque cada como cosa cosas cual cuales dellas dellos
desde despues dice dicen dicho dixo donde ellas ellos entre esta estas este
estos esto estaba estan estar fuese fueron hace hacen hacer hasta mismo mismos
mucho muchos mucha muchas nuestra nuestro otra otras otro otros para pero porque
puede quando quanto quel quien quiere segun sobre solo suelen sus tambien tanto
tenia tenian tiene tienen todas todos toda todo tres veces vez cual quales
dicha dichas dichos manera parte partes
""".split())


def _forzar_utf8():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def normalizar(texto):
    """Misma ortografía para los dos tomos: la capa OCR del t. II lee la ç como
    `g` y la del t. I como `c`; se deshace el guion de fin de línea antes."""
    t = re.sub(r"-\s*\n\s*", "", texto)
    t = t.lower().replace("ç", "c")
    t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    t = re.sub(r"g(?=[ei])", "c", t)        # hager → hacer (OCR de la ç en el t. II)
    t = t.replace("z", "c").replace("v", "b").replace("y", "i").replace("ss", "s")
    t = re.sub(r"\bh(?=[aeiou])", "", t)    # haçer/açer, hombre/ombre: se quita la h- inicial
    t = re.sub(r"[^a-zñ\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def leer_tramo(nombre):
    import pymupdf
    pdf, desfase, desde, hasta, _ = TRAMOS[nombre]
    doc = pymupdf.open(os.path.join(FUENTES, pdf))
    return "\n".join(doc[i + desfase].get_text() for i in range(desde, hasta + 1))


def bigramas(texto_norm):
    palabras = [p for p in texto_norm.split() if len(p) >= 4 and p not in VACIAS]
    return {(a, b) for a, b in zip(palabras, palabras[1:])}


def medir():
    textos = {n: normalizar(leer_tramo(n)) for n in TRAMOS}
    ref = bigramas(textos[REFERENCIA])
    medido = {}
    for n, (pdf, desfase, desde, hasta, que) in TRAMOS.items():
        b = bigramas(textos[n])
        fila = {
            "impresas": f"{desde}-{hasta}",
            "que_es": que,
            "palabras": len(textos[n].split()),
            "voces_de_la_espanola": {v: len(re.findall(p, textos[n])) for v, p in VOCES_ISLA.items()},
            "plinio_sobre_el_arte_magico": sum(
                1 for m in re.finditer(PLINIO_MAGIA, textos[n])
                if re.search(r"magic|medicin", textos[n][max(0, m.start() - VENTANA_PLINIO):m.end() + VENTANA_PLINIO])),
        }
        if n != REFERENCIA:
            comunes = sorted(" ".join(x) for x in (b & ref))
            fila["bigramas_propios"] = len(b)
            fila["bigramas_compartidos_con_la_espanola"] = len(comunes)
            fila["proporcion_compartida"] = round(len(comunes) / len(b), 4) if b else 0.0
            fila["los_compartidos"] = comunes
        medido[n] = fila
    return medido


def contar_capas(prop):
    """{bloque: {capa: n}} sobre los hechos de la propuesta (regla 1)."""
    cuenta = {}
    for bloque in ("hechos_taino", "lado_caqueti"):
        c = {}
        for h in prop.get(bloque) or []:
            c[h.get("capa")] = c.get(h.get("capa"), 0) + 1
        cuenta[bloque] = dict(sorted(c.items()))
    return cuenta


def validar():
    import yaml
    errores = []
    with open(PROPUESTA, encoding="utf-8") as f:
        prop = yaml.safe_load(f)
    if (prop.get("meta") or {}).get("cuenta_por_capa") != contar_capas(prop):
        errores.append("meta.cuenta_por_capa no coincide con los hechos: regenerar con --conteos")
    with open(BIBLIO, encoding="utf-8") as f:
        ids_biblio = {o["id"] for o in yaml.safe_load(f)["obras"]}
    with open(CREENCIA, encoding="utf-8") as f:
        ids_creencia = {h["id"] for h in yaml.safe_load(f)}
    capas = {"atestiguado", "reconstruido", "hipotetico", "lectura", "no-se-propone"}
    vistos = set()
    n = 0
    for bloque in ("hechos_taino", "lado_caqueti"):
        for h in prop.get(bloque) or []:
            n += 1
            hid = h.get("id")
            if hid in vistos:
                errores.append(f"id repetido: {hid}")
            vistos.add(hid)
            if h.get("capa") not in capas:
                errores.append(f"{hid}: capa «{h.get('capa')}» no es una de {sorted(capas)}")
            for campo in ("fuente", "pagina", "pueblo", "proyeccion", "via_a", "epoca"):
                if campo not in h:
                    errores.append(f"{hid}: falta `{campo}`")
            fuentes = h.get("fuente")
            fuentes = fuentes if isinstance(fuentes, list) else [fuentes]
            for fu in fuentes:
                if fu not in ids_biblio:
                    errores.append(f"{hid}: fuente «{fu}» no está en 4-fuentes/bibliografia.yaml")
            for vid in h.get("via_a") or []:
                if vid not in ids_creencia:
                    errores.append(f"{hid}: via_a «{vid}» no existe en creencia.yaml")
    medido_yaml = (prop.get("meta") or {}).get("medido")
    medido = medir()
    resumen = {k: {kk: vv for kk, vv in v.items() if kk != "los_compartidos"} for k, v in medido.items()}
    if medido_yaml is not None:
        resumen_yaml = {k: {kk: vv for kk, vv in v.items() if kk != "los_compartidos"}
                        for k, v in medido_yaml.items()}
        if resumen_yaml != resumen:
            errores.append("meta.medido no coincide con lo que mide el script: regenerar con --conteos")
    return n, errores


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--conteos", action="store_true", help="imprime el bloque meta.medido en YAML")
    args = ap.parse_args()
    if args.conteos:
        import yaml
        salida = {}
        if os.path.exists(PROPUESTA):
            with open(PROPUESTA, encoding="utf-8") as f:
                salida["cuenta_por_capa"] = contar_capas(yaml.safe_load(f))
        salida["medido"] = medir()
        print(yaml.safe_dump(salida, allow_unicode=True, sort_keys=False, width=100))
        return 0
    n, errores = validar()
    if errores:
        print(f"✗ {len(errores)} problema(s) en {os.path.relpath(PROPUESTA, RAIZ)}:")
        for e in errores:
            print("  -", e)
        return 1
    print(f"✓ {n} hechos válidos; fuentes en la bibliografía; via_a en creencia.yaml; meta.medido al día")
    return 0


if __name__ == "__main__":
    sys.exit(main())
