#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mide y valida la campaña de la COSMOVISIÓN MARINA (2026-09-24):

    6-fusion/cosmovision_marina_2026-09-24.yaml

La pregunta: ¿qué dicen las fuentes del repo sobre el MAR en la vida
simbólica, ritual y cosmológica de los caquetíos de la costa?

El instrumento es una COOCURRENCIA, y se dice lo que es: para cada obra se
buscan los términos de CREENCIA (rito, sacrificio, ídolo, diablo, piache,
boratio, alma, entierro, leyenda...) y se mira si a ±300 caracteres hay un
término del MAR (mar, pescado, perla, concha, tortuga, tiburón...). Las
ventanas que se solapan se funden. Como CONTROL POSITIVO se hace lo mismo con
el CIELO (lluvia, trueno, sol, luna, tempestad...): si el método encuentra
creencia × cielo donde la hay, un cero de creencia × mar no es un cero del
método. En las obras que cubren toda América (Castellanos, Anglería,
Navarrete, el Handbook) se cuenta aparte cuántas ventanas tienen un nombre de
la costa occidental (Coro, Paraguaná, Curazao, caquetío, Manaure...) a ±2000
caracteres: ésas son las que se leyeron una a una.

Un recuento de ventanas NO es un hallazgo: cada ventana se lee. El veredicto
de la lectura va en el YAML (`meta.lectura_de_las_ventanas`); este script
sólo da las cifras (regla 1) y valida el YAML (regla 8: toda `obra` existe
en 4-fuentes/bibliografia.yaml).

No llama a ninguna API, no lee curiana_sim/.env, no toca la base. Necesita
PyMuPDF (`import pymupdf`) para los PDF.

    python 6-fusion/scripts/medir_cosmovision_marina.py              # valida y compara con meta.medido
    python 6-fusion/scripts/medir_cosmovision_marina.py --conteos    # imprime el bloque medido (YAML)
    python 6-fusion/scripts/medir_cosmovision_marina.py --ventanas DIR   # escribe las ventanas para leerlas
"""

import argparse
import io
import os
import re
import sys
import unicodedata

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
F = os.path.join(RAIZ, "fuentes_caquetios")
YAML_CM = os.path.join(RAIZ, "6-fusion", "cosmovision_marina_2026-09-24.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")

V = 300          # ventana alrededor de cada término de creencia
V_OESTE = 2000   # radio para decidir si la ventana habla de la costa occidental

# clave: (archivo, idioma, obra de la bibliografía, (pdf_desde, pdf_hasta) o None, qué es)
FUENTES = {
    # ── la costa caquetía en las crónicas (el DATO posible) ──
    "oviedo_t2_lib25": ("Oviedo_Valdes_1852_Historia_General_Indias_vol2.pdf", "es", "oviedo-y-valdes-1852-1855", (282, 346), "t. II lib. XXV, la provincia de Venezuela (impresas 269-332, pdf − 13)"),
    "aguado_t1": ("Aguado_1918_Historia_Venezuela_t1_gutenberg.txt", "es", "aguado-1581", None, "Historia de Venezuela t. I (escrita 1581; ed. Bécker 1918)"),
    "fd_t2_documentos": ("Oviedo_Banos_1885_FernandezDuro_t2_Documentos.txt", "es", "perez-de-tolosa-1546", None, "Fernández Duro 1885 t. II: Oviedo y Baños + apéndice (Ampíes, Pérez de Tolosa)"),
    "oviedo_banos": ("Oviedo_Banhos_Conquista_Poblacion_Venezuela.pdf", "es", "oviedo-y-banos", None, "Oviedo y Baños 1723"),
    "castellanos": ("Castellanos_1857_Elegias_partes_I-II_texto.txt", "es", "castellanos-elegias", None, "Elegías, partes I-II entero (c. 1589)"),
    "federmann1916": ("Federmann_1916_Narracion_Primer_Viaje_Arcaya.txt", "es", "federmann-1916", None, "Federmann 1530, trad. Arcaya"),
    "federmann1859": ("Federmann_Kluepfel_1859_Reisen_texto_aleman.txt", "de", "federmann-1916", None, "Federmann en alemán (ed. 1859; el tomo trae además a Staden)"),
    "angleria_v1": ("Angleria_1892_Fuentes_Historicas_Colon_America_vol1.txt", "es", "angleria-1892", None, "Anglería vol. 1"),
    "angleria_v4": ("Angleria_1892_Fuentes_Historicas_Colon_America_vol4.txt", "es", "angleria-1892", None, "Anglería vol. 4"),
    "navarrete1829": ("Navarrete_1829_Coleccion_Viages_t3_Viages_Menores_Vespucio.txt", "es", "navarrete-1829-viages-menores", None, "viajes menores 1499-1502"),
    # ── síntesis y estudios que leen esas crónicas ──
    "arcaya": ("Arcaya_1920_Historia_Estado_Falcon.pdf", "es", "arcaya-1920", None, "Arcaya 1920"),
    "jahn": ("Jahn_1927_Aborigenes_Occidente_Venezuela.pdf", "es", "jahn-1927", None, "Jahn 1927"),
    "steward1948": ("Steward_1948_HSAI_vol4_Circum-Caribbean_Tribes.txt", "en", "steward-1948-hsai-4", None, "Handbook vol. 4 entero"),
    "oliver_cap2": ("Chapter 2 Linguistics- Oliver 1989.pdf", "en", "oliver-1989-cap2", None, "Oliver cap. 2"),
    "oliver_cap3_doc": ("Chapter 3 Ethnohistory.DOC-comprimido.pdf", "en", "oliver-1989-cap3", None, "Oliver cap. 3 (DOC)"),
    "oliver_cap3_s33": ("Oliver_1989_cap3_s33_falcon_lara.ocr.txt", "en", "oliver-1989-cap3", None, "Oliver §3.3"),
    "oliver_cap4": ("Oliver_1989_cap4_s47_s415_dabajuroide.ocr.txt", "en", "oliver-1989-cap4", None, "Oliver cap. 4 (dabajuroide)"),
    # ── s. XX: tradición local, léxico, interpretación ──
    "antolinez1946": ("Antolinez_1946_Hacia_el_indio_y_su_mundo.pdf", "es", "antolinez-1946-hacia-el-indio", None, "Antolínez 1946"),
    "alvarado1921": ("Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf", "es", "alvarado-1921", None, "Alvarado 1921"),
    "zavala2015": ("Palabras Vivas de una Lengua Muerta.pdf", "es", "zavala-reyes-2015", None, "Zavala Reyes 2015 (lexicón caquetío)"),
    "esteves_1": ("Esteves_1989_Toponimos_Paraguana_1.ocr.txt", "es", "esteves-1989", None, "Esteves, parte 1"),
    "esteves_2": ("Esteves_1989_Toponimos_Paraguana_2.ocr.txt", "es", "esteves-1989", None, "Esteves, parte 2"),
    "esteves_3": ("Esteves_1989_Toponimos_Paraguana_3.ocr.txt", "es", "esteves-1989", None, "Esteves, parte 3"),
    "esteves_4": ("Esteves_1989_Toponimos_Paraguana_4.ocr.txt", "es", "esteves-1989", None, "Esteves, parte 4"),
    "esteves_5": ("Esteves_1989_Toponimos_Paraguana_5.ocr.txt", "es", "esteves-1989", None, "Esteves, parte 5"),
    "esteves_6": ("Esteves_1989_Toponimos_Paraguana_6.ocr.txt", "es", "esteves-1989", None, "Esteves, parte 6"),
    "medina_dictado": (os.path.join("..", "6-fusion", "medina_colina_dictado.yaml"), "es", "medina-colina-sxx", None, "el dictado de Medina Colina (6-fusion)"),
    "velasco2015": ("Velasco_2015_Historia_de_una_Resistencia.pdf", "es", "velasco-2015-resistencia", None, "Velasco 2015"),
    "van_buurt2014": ("VanBuurt_2014_CaquetioWords_Papiamentu.txt", "en", "van-buurt-2014", None, "van Buurt 2014 (ABC)"),
    "gatschet1885": ("Gatschet_1885_Aruba_texto.txt", "en", "gatschet-1885", None, "Gatschet 1885 (Aruba)"),
    # ── arqueología de la costa ──
    "zavala2018": ("ZavalaReyes_et_al_2018_Arqueologia_Medanos_Coro.pdf", "es", "zavala-reyes-2018", None, "Médanos de Coro"),
    "urbina2007": ("Urbina_2007_El_Carrizal_UCV.txt", "es", "urbina-jimenez-2007-2011", None, "El Carrizal"),
    "urbina2011": ("Urbina_2011_Archaeological_Survey_Coastal_Falcon_UCL.txt", "en", "urbina-jimenez-2007-2011", None, "Falcón costero"),
    "antczak2017": ("Antczak_et_al_2017_Cariban_Migration_Orinoco.pdf", "en", "antczak-2017-cariban", None, "Antczak et al. 2017"),
    "moron2012": ("Moron_2012_Petroglifos_Falcon.pdf", "es", "moron-2012-petroglifos", None, "petroglifos de Falcón"),
}

MAR = {
    "es": r"\bmar\b|\bmares\b|marin[oa]s?\b|mariti|pescad|\bpesca|perla|concha|caracol|botuto|guarura|tortuga|tibur|manati|\bolas?\b|oleaje|\bplaya|marea|naveg|\bislen",
    "en": r"\bsea\b|\bseas\b|marine|maritime|\bocean|\bfish|\bshells?\b|\bconch|\bturtle|\bshark|\bpearl|\bwaves?\b|\bbeach|\btide|\bnavigat|\bseafar",
    "de": r"\bmeer|\bfisch|muschel|perle|schildkr|\bwelle",
}
CREENCIA = {
    "es": r"diablo|demonio|\bidol|\bydol|adora[rnd]|sacrific|ofrend|\britos?\b|ceremon|\bculto|\bdios(es)?\b|espiritu|\balmas?\b|sagrad|sacerdot|piache|boratio|mohan|hechicer|aguer|adivin|supersti|\bmitos?\b|mitolog|leyenda|encant|sirena|fantasma|espanto|aparecid|sepult|enterra|entierro|funer|\btabu|religi|creenc|cosmo|sobrenatural|duende|\bbruj|malefic|conjur|oracul|\bmagi[ac]",
    "en": r"devil|\bidol|worship|sacrific|offering|ritual|\brites?\b|ceremon|\bcult\b|\bgods?\b|\bdeit|spirit|\bsouls?\b|sacred|\bholy|priest|shaman|piache|boratio|sorcer|\bmagic|\bmyth|legend|belief|religio|burial|\bgraves?\b|funer|taboo|supernatural|cosmolog|mortuary|cemet",
    "de": r"teufel|g[oö]tze|abgott|opfer|priester|zauber|\bgeist|\bseele|heilig|begr[aä]b|\bgott",
}
CIELO = {
    "es": r"lluvi|llover|llueve|trueno|relampag|\brayos?\b|\bsol\b|\bluna\b|estrella|\bcielo|tempest|tormenta|temporal|granizo",
    "en": r"\brain|thunder|lightning|\bsun\b|\bmoon|\bstars?\b|\bsky\b|storm|\bhail\b|drought",
    "de": r"regen|donner|blitz|sonne|\bmond|stern|himmel|sturm|hagel",
}
OESTE = (r"coquibaco|quiquibaco|curiana|coriana|curaza|curaca|coraza|gigantes|aruba|oruba|buinar|bonaire|"
         r"paraguan|venezuel|venecuel|maracaib|cabo de (la )?vela|\bcoro\b|caquet|caquit|zaquit|manaure|anaure|"
         r"todariquiba|golfete|los roques")

ETIQUETAS = {"atestiguado", "reconstruido", "hipotetico", "retro-abstraido"}


def _forzar_utf8():
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def plano(s):
    """Sin diacríticos y con ç→c (la ç del s. XVI), mismo largo que el original."""
    out = []
    for c in s:
        if c in "çÇ":
            out.append("c")
            continue
        d = unicodedata.normalize("NFD", c)
        base = "".join(x for x in d if unicodedata.category(x) != "Mn")
        out.append(base[:1] if base else c)
    return "".join(out)


def leer(clave):
    archivo, lang, obra, rango, _ = FUENTES[clave]
    ruta = os.path.normpath(os.path.join(F, archivo))
    if ruta.lower().endswith(".pdf"):
        import pymupdf
        doc = pymupdf.open(ruta)
        a, b = rango if rango else (0, len(doc))
        paginas = [(i, doc[i].get_text()) for i in range(a, min(b, len(doc)))]
    else:
        with open(ruta, encoding="utf-8", errors="replace") as fh:
            paginas = [(None, fh.read())]
    trozos, marcas = [], []
    pos = 0
    for i, t in paginas:
        t = re.sub(r"-\r?\n\s*", "", t)   # la caja parte las palabras a fin de línea
        marcas.append((pos, i))
        trozos.append(t)
        pos += len(t)
    return "".join(trozos), marcas


def pagina(marcas, pos):
    pg = None
    for p, i in marcas:
        if p <= pos:
            pg = i
        else:
            break
    return pg


def ventanas(p, pat_creencia, pat_otro):
    fus = []
    for m in re.finditer(pat_creencia, p, re.I):
        a, b = max(0, m.start() - V), min(len(p), m.end() + V)
        if not re.search(pat_otro, p[a:b], re.I):
            continue
        if fus and a <= fus[-1][1]:
            fus[-1] = (fus[-1][0], max(fus[-1][1], b))
        else:
            fus.append((a, b))
    return fus


def medir(dir_ventanas=None):
    res = {}
    for clave, (archivo, lang, obra, rango, que) in FUENTES.items():
        texto, marcas = leer(clave)
        p = plano(texto)
        wm = ventanas(p, CREENCIA[lang], MAR[lang])
        wc = ventanas(p, CREENCIA[lang], CIELO[lang])
        oeste = [w for w in wm if re.search(OESTE, p[max(0, w[0] - V_OESTE):w[1] + V_OESTE], re.I)]
        res[clave] = {
            "obra": obra,
            "caracteres": len(texto),
            "terminos_mar": len(re.findall(MAR[lang], p, re.I)),
            "terminos_creencia": len(re.findall(CREENCIA[lang], p, re.I)),
            "terminos_cielo": len(re.findall(CIELO[lang], p, re.I)),
            "ventanas_creencia_x_mar": len(wm),
            "ventanas_creencia_x_mar_costa_occidental": len(oeste),
            "ventanas_creencia_x_cielo_control": len(wc),
        }
        if dir_ventanas:
            os.makedirs(dir_ventanas, exist_ok=True)
            with open(os.path.join(dir_ventanas, clave + ".txt"), "w", encoding="utf-8") as fh:
                for (a, b) in wm:
                    marca = "OESTE " if (a, b) in oeste else ""
                    pg = pagina(marcas, a)
                    fh.write("--- %s[pdf %s] %s\n" % (marca, "" if pg is None else pg + 1,
                                                        re.sub(r"\s+", " ", texto[a:b])))
    return res


def bloque_yaml(res):
    tot = {k: sum(r[k] for r in res.values()) for k in
           ("ventanas_creencia_x_mar", "ventanas_creencia_x_mar_costa_occidental", "ventanas_creencia_x_cielo_control")}
    return {"por_obra": res, "total": {"textos_barridos": len(res),
                                      "obras_distintas": len({r["obra"] for r in res.values()}), **tot}}


def validar(medido):
    errores, avisos = [], []
    with open(BIBLIO, encoding="utf-8") as fh:
        bib = yaml.safe_load(fh)
    ids_bib = {o["id"] for o in (bib.get("obras") if isinstance(bib, dict) else bib)} if bib else set()
    for clave, (_, _, obra, _, _) in FUENTES.items():
        if obra not in ids_bib:
            errores.append("la fuente %s cita una obra que no está en la bibliografía: %s" % (clave, obra))
    if not os.path.exists(YAML_CM):
        errores.append("no existe %s" % YAML_CM)
        return errores, avisos
    with open(YAML_CM, encoding="utf-8") as fh:
        d = yaml.safe_load(fh)
    vistos = set()

    def recorrer(x, ruta=""):
        if isinstance(x, dict):
            if "id" in x and isinstance(x["id"], str):
                if x["id"] in vistos:
                    errores.append("id repetido: %s" % x["id"])
                vistos.add(x["id"])
                if "fuente" in x and x["fuente"] not in ETIQUETAS:
                    errores.append("%s: fuente «%s» no es una etiqueta epistémica" % (x["id"], x["fuente"]))
            for k, v in x.items():
                if k == "obra" and isinstance(v, str) and v not in ids_bib:
                    errores.append("%s: obra «%s» no está en la bibliografía" % (ruta, v))
                recorrer(v, ruta + "/" + str(k))
        elif isinstance(x, list):
            for i, v in enumerate(x):
                recorrer(v, ruta + "[%d]" % i)
    recorrer(d)
    for h in d.get("hechos_candidatos", []):
        for campo in ("id", "contenido", "fuente", "procedencia", "dominios", "restringido", "implicacion_simulacion", "epoca", "polity"):
            if campo not in h:
                errores.append("%s: falta «%s»" % (h.get("id"), campo))
    en_yaml = (d.get("meta") or {}).get("medido")
    if en_yaml is None:
        avisos.append("meta.medido no está en el YAML: pégalo con --conteos")
    elif en_yaml != medido:
        errores.append("meta.medido no coincide con lo que mide este script (regla 1): regenéralo con --conteos")
    return errores, avisos


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--conteos", action="store_true")
    ap.add_argument("--ventanas", metavar="DIR")
    a = ap.parse_args()
    res = medir(a.ventanas)
    medido = bloque_yaml(res)
    if a.conteos:
        print(yaml.safe_dump({"medido": medido}, allow_unicode=True, sort_keys=False, width=120))
        return 0
    print("%-22s %9s %6s %6s %6s | %8s %8s %8s" % ("obra", "chars", "mar", "cre", "cielo", "cre×mar", "…oeste", "cre×cielo"))
    for k, r in res.items():
        print("%-22s %9d %6d %6d %6d | %8d %8d %8d" % (k, r["caracteres"], r["terminos_mar"], r["terminos_creencia"],
                                                      r["terminos_cielo"], r["ventanas_creencia_x_mar"],
                                                      r["ventanas_creencia_x_mar_costa_occidental"],
                                                      r["ventanas_creencia_x_cielo_control"]))
    print("total", medido["total"])
    errores, avisos = validar(medido)
    for w in avisos:
        print("AVISO:", w)
    for e in errores:
        print("ERROR:", e)
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
