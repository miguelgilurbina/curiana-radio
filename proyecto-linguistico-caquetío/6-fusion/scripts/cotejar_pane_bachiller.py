# -*- coding: utf-8 -*-
"""
LA PANÉ DE BACHILLER CONTRA LA PANÉ DE WIKISOURCE — tercera campaña, parcela M5.

LA PREGUNTA
-----------
Bachiller y Morales (1883, sección 2.1, pp. 165-184) publicó una traducción NUEVA de la
*Relación* de Pané y dijo que «restituía» los nombres indios. La parcela T10 lo dejó
anotado sin cotejar. ¿Sus formas coinciden con las del texto que el repo usa
(`Pane_c1498_Relacion_Antiguedades_Indios_wikisource.txt`)? Y si no, ¿por qué?

Lo que Bachiller DECLARA (p. 166, verbatim recortado): que como los nombres indios «han
sufrido grandes alteraciones» procura «restituir lo que alcanzo, teniendo presente á
Oviedo, P. Mártir, Rafinesque y Brasseur de Bourbourg», sobre la edición italiana de
Milán de 1614. O sea: su texto NO es un testigo independiente de Pané; es Ulloa (1571)
más correcciones sacadas de otros autores — Rafinesque entre ellos.

EL MÉTODO (y sus límites, dichos)
---------------------------------
1. Las voces indígenas de Pané son las que ya transcribió la primera campaña
   (`6-fusion/taino_pane_c1498.yaml`: `voces`, `teonimos_y_rito.deidades` y los lugares
   del mito), partidas en palabras.
2. Para cada una se busca en las pp. 165-184 de Bachiller (OCR de archive.org, página
   impresa = pdf − 4) la palabra más parecida (difflib sobre una forma normalizada).
3. Veredicto: `igual` (misma forma normalizada), `variante` (parecido ≥ 0,72), `no-esta`
   (nada parecido). ⚠️ Un `no-esta` puede ser una forma que Bachiller restituyó hasta
   hacerla irreconocible (`Iermaoguacar` → `Gna-cara-pita`): es lo que se quiere medir, y
   por eso se lee a mano (`LEIDO_A_MANO`).

USO
---
    python 6-fusion/scripts/cotejar_pane_bachiller.py [--check]

SALIDA (PROPUESTA, regla 5): 6-fusion/taino3_pane_bachiller_cotejo.yaml
"""
import argparse
import collections
import difflib
import io
import os
import re
import sys
import unicodedata

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACH = os.path.join(R, "fuentes_caquetios", "Bachiller_Morales_1883_Cuba_Primitiva.txt")
PANE_Y = os.path.join(R, "6-fusion", "taino_pane_c1498.yaml")
SALIDA = os.path.join(R, "6-fusion", "taino3_pane_bachiller_cotejo.yaml")
DESFASE = 4                       # impresa = pdf − 4 (medido por la parcela T10 sobre 227 marcas)
PAG_INI, PAG_FIN = 165, 184
UMBRAL = 0.80

# Leído en el texto de Bachiller, no derivado: los casos en que la forma cambió tanto que la
# comparación de cadenas no los empareja, o en que el emparejamiento automático es falso.
LEIDO_A_MANO = {
    "Yocahu Vagua Maorocoti": ("Yocauna-Gua-Maonocon", 167,
                               "restituida: Coll y Toste (p. 260) la cita así de Bachiller"),
    "Atabex, Iermaoguacar, Apito y Zuimaco": ("Atabeira Mamona, Gna-cara-pita, Lidia, Guimasoa", 167,
                                              "cinco nombres, y ninguno igual: `Atabeira` es la forma de "
                                              "Pedro Mártir, no la de Pané-Ulloa"),
    "Dios naboria daca": ("Dio Aboriadacha", 182,
                          "la frase entera en una palabra, y `dacha` por `daca`: es la forma que su "
                          "vocabulario (p. 270) atribuye a Pané"),
    "cemíes": ("semis", 167, "con s-, como en Pedro Mártir; ningún `cemí` en las veinte páginas"),
    "Cacibayagua y Amayauba": ("Caji-Bajagua … Amayauna", 167,
                               "nota de Bachiller: «Pedro Mártir escribe Casi-Baxagua»"),
    "Caonao": ("Caimana", 167, "la provincia de la gruta; Bachiller la restituye como `Caimana`"),
    "Maquetaurie Guayaba": ("Maqnetaurie Guayaría", 172, "el primer nombre igual (con la u leída n "
                            "por el OCR); el segundo, otro"),
    "Opiyelguoviran": ("Epilegaaanita", 180, "🔴 SUSTITUCIÓN DECLARADA: «así lo llama P. Mártir: un "
                       "texto dice Opigielqaouiran que es visible errata». Pone el nombre de Mártir y "
                       "manda el de Pané a la errata"),
    "guabaza": ("guanaba", 173, "🔴 SUSTITUCIÓN DECLARADA: «guanaba (así lo dice Pedro Mártir:) el "
                "texto que traduzco dice guabasa, lo que creo error»"),
    "tona": ("toa, toa (madre, madre) … convertidos en ranas", 170,
             "la voz de la rana (`tona`) no está: queda sólo el grito `toa` de los niños"),
    "Bouhi": ("Bulii [Bohi, ¿casas? ó ¿habitaciones?]", 169,
              "OCR `Bulii`/`BoM`; Bachiller lo glosa él mismo como 'casas', con interrogación: "
              "conjetura suya, no de Pané"),
    "Vaibrama (título: Buyayba)": ("Baidrama … Bujay", 179, "Baidrama por Vaibrama; y `Bujay` como "
                                   "otro nombre del mismo ídolo, que Pané da como título"),
}


def sd(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm(w):
    w = sd(w).lower()
    w = re.sub(r"[^a-zñ]", "", w)
    w = re.sub(r"c(?=[ei])", "s", w)
    w = w.replace("qu", "k").replace("c", "k").replace("v", "b").replace("y", "i")
    w = w.replace("j", "h").replace("x", "h").replace("z", "s").replace("gu", "g")
    return re.sub(r"(.)\1+", r"\1", w)


def paginas_bachiller():
    pp = io.open(BACH, encoding="utf-8").read().split("\f")
    out = {}
    for imp in range(PAG_INI, PAG_FIN + 1):
        out[imp] = pp[imp + DESFASE - 1]
    return out


def tokens_bachiller(pags):
    toks = []
    for imp, txt in pags.items():
        plano = re.sub(r"-\s*\n\s*", "", txt)
        for m in re.finditer(r"[A-Za-zÁÉÍÓÚáéíóúÑñü]+(?:-[A-Za-zÁÉÍÓÚáéíóúÑñü]+)*", plano):
            w = m.group(0)
            if len(norm(w)) >= 3:
                toks.append((w, imp, plano[max(0, m.start() - 70): m.end() + 70].replace("\n", " ")))
    return toks


PALABRAS_VACIAS = set("""y o a de del la las los el en por otro nombre que se su sus""".split())


def formas_pane():
    Y = yaml.safe_load(io.open(PANE_Y, encoding="utf-8"))
    out = []
    for e in Y.get("voces") or []:
        out.append((e["forma_fuente"], e.get("capitulo"), "voz"))
    tr = Y.get("teonimos_y_rito") or {}
    for e in tr.get("deidades") or []:
        out.append((e["forma_fuente"], e.get("capitulo"), "teonimo"))
    for e in tr.get("lugares_y_grutas_del_mito") or []:
        if isinstance(e, dict) and (e.get("forma_fuente") or e.get("forma")):
            out.append((e.get("forma_fuente") or e.get("forma"), e.get("capitulo"), "lugar"))
    return out


INICIAL = {"b": "b", "k": "kgh", "g": "gkh", "h": "hgk", "s": "s", "i": "i"}


def mejor(palabra, toks):
    """El token de Bachiller más parecido, exigiendo la misma inicial (o su alternancia
    gráfica de época: b/v, c/g/h, s/z, i/y): sin eso `naboria` casa con `nabo` y `opia`
    con `copia`."""
    n = norm(palabra)
    best = (0.0, None)
    for w, imp, ctx in toks:
        m = norm(w)
        if not m or not n or m[0] not in INICIAL.get(n[0], n[0]):
            continue
        r = difflib.SequenceMatcher(None, n, m).ratio()
        if r > best[0]:
            best = (r, (w, imp, ctx))
    return best


def construir():
    pags = paginas_bachiller()
    toks = tokens_bachiller(pags)
    filas = []
    cuenta = collections.Counter()
    for forma, cap, tipo in formas_pane():
        if forma in LEIDO_A_MANO:
            b, p, nota = LEIDO_A_MANO[forma]
            filas.append(collections.OrderedDict([
                ("pane_wikisource", forma), ("capitulo", cap), ("tipo", tipo),
                ("bachiller", b), ("pagina_impresa", p), ("veredicto", "difiere-restituida"),
                ("como", "leído a mano"), ("nota", nota)]))
            cuenta["difiere-restituida"] += 1
            continue
        palabras = [w for w in re.split(r"[\s,/();]+", forma)
                    if w and w.lower() not in PALABRAS_VACIAS and len(norm(w)) >= 3
                    and not re.match(r"(?i)^(dios|t[íi]tulo:?|nombre)$", w)]
        for w in palabras:
            r, hit = mejor(w, toks)
            if hit and norm(hit[0]) == norm(w):
                ver = "igual"
            elif hit and r >= UMBRAL:
                ver = "variante"
            else:
                ver = "no-esta"
            cuenta[ver] += 1
            fila = collections.OrderedDict([
                ("pane_wikisource", w), ("en_la_forma", forma if forma != w else None),
                ("capitulo", cap), ("tipo", tipo),
                ("bachiller", hit[0] if hit and ver != "no-esta" else None),
                ("pagina_impresa", hit[1] if hit and ver != "no-esta" else None),
                ("parecido", round(r, 2)),
                ("veredicto", ver),
                ("contexto_en_bachiller", hit[2] if hit and ver != "no-esta" else None),
            ])
            filas.append(fila)
    salida = collections.OrderedDict()
    salida["meta"] = collections.OrderedDict([
        ("pregunta", "¿las formas indígenas de la retraducción de Pané de Bachiller (1883, pp. "
                     "165-184) coinciden con las de la Pané que usa el repo (Wikisource)?"),
        ("medido", "2026-09-23"),
        ("script", "6-fusion/scripts/cotejar_pane_bachiller.py"),
        ("estado", "PROPUESTA (regla 5)"),
        ("lo_que_declara_bachiller",
         "p. 166: traduce de nuevo sobre la edición italiana de Milán (1614) y «restituye» los "
         "nombres indios «teniendo presente á Oviedo, P. Mártir, Rafinesque y Brasseur de "
         "Bourbourg». No vio la edición de Venecia (1571) y rechaza la de Bárcia."),
        ("umbral", UMBRAL),
        ("aviso", "OCR de archive.org sin corregir; `no-esta` puede ser una forma restituida "
                  "hasta no parecerse (ver LEIDO_A_MANO)."),
    ])
    salida["resumen"] = dict(sorted(cuenta.items()))
    salida["filas"] = filas
    return salida


def texto_yaml(d):
    def rep(dumper, data):
        return dumper.represent_dict(data.items())
    yaml.add_representer(collections.OrderedDict, rep, Dumper=yaml.SafeDumper)
    return yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=100)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    nuevo = texto_yaml(construir())
    if a.check:
        viejo = io.open(SALIDA, encoding="utf-8").read() if os.path.exists(SALIDA) else ""
        ok = viejo == nuevo
        print(("✓ %s está al día" if ok else "✗ %s DESFASADO") % os.path.relpath(SALIDA, R))
        return 0 if ok else 1
    io.open(SALIDA, "w", encoding="utf-8", newline="\n").write(nuevo)
    print("✓", os.path.relpath(SALIDA, R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
