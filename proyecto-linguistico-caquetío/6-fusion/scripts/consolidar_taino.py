# -*- coding: utf-8 -*-
"""
LA LISTA MAESTRA DEL TAÍNO — segunda campaña del taíno, parcela T10 (2026-09-22).

LA PREGUNTA
-----------
El cruce taíno↔caquetío del 2026-09-21 midió **4 conceptos comparables y 0
parejas**, y el agente que lo hizo escribió: «el cero mide la lista, no la
lengua». La lista taína del repo son productos (casabe, maíz, canoa) porque
entró en bloque en junio sin cita. Esta pregunta es doble:

  (1) ¿cuántas voces taínas tiene el proyecto cuando se juntan TODAS las
      transcripciones —las cuatro de la primera campaña y las dos de ésta—,
      y cuál es la CADENA DE CUSTODIA de cada una hasta el cronista del XVI?
  (2) ¿cuántos CONCEPTOS comparables con el caquetío atestiguado aporta esa
      lista nueva? Ese número decide si el cruce se puede re-correr con
      sentido.

LO QUE ESTE SCRIPT NO HACE
--------------------------
No fusiona nada. No toca `curiana_sim/`, `2-lengua/`, `3-mundo/` ni el canon.
Lee el lexicón **de sólo lectura** para saber qué clave toca cada voz y para
medir los conceptos del caquetío atestiguado.

LA REGLA DE INDEPENDENCIA (skill `minar-fuente` §8)
---------------------------------------------------
**La atestación es del cronista, no del compilador.** Brinton (1871), Goeje
(1939) y Bachiller (1883) no oyeron hablar taíno a nadie: son intermediarios.
Dos obras que citan al MISMO cronista son UNA atestación. Por eso el conteo
que manda aquí es `atestaciones_independientes` = número de **cronistas
distintos del s. XV-XVI** detrás de la voz, no el número de obras que la traen.

LAS CLASES
----------
  (i)   `primaria-del-XVI` — al menos un cronista del XV-XVI la atestigua.
  (ii)  `solo-secundaria`  — la trae un compilador del XIX-XX y ninguno dice
        de qué cronista sale. Existe, pero no está atestiguada.
  (iii) `conjetura-moderna` — su única existencia es la reconstrucción o la
        conjetura de un autor moderno. **NO ENTRA.** Aquí caen las nueve
        `taíno-reconstruido` que este proyecto generó con
        `reconstruir_taino()`, y lo que un compilador propone sin apoyo.

  Y una cuarta marca transversal, `sacada_del_taino`: voces que una fuente
  asigna explícitamente a OTRA lengua (caribe insular, eyeri, español,
  tupí, africano). No es una clase de custodia: es un aviso de etiqueta.

USO
---
    python 6-fusion/scripts/consolidar_taino.py
    python 6-fusion/scripts/consolidar_taino.py --check   # ¿el YAML está al día?

SALIDA (PROPUESTA, regla 5)
---------------------------
    6-fusion/taino_lista_maestra_2026-09-22.yaml
"""
import argparse
import collections
import io
import os
import re
import sys
import unicodedata

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
sys.path.insert(0, os.path.dirname(__file__))
import curiana_lexicon as CL                      # noqa: E402  (sólo lectura)
from cruce_taino_caquetio import conceptos, _norm_es   # noqa: E402  LA MISMA normalización

FECHA = "2026-09-22"
SALIDA = os.path.join(R, "6-fusion", "taino_lista_maestra_%s.yaml" % FECHA)
ATESTIGUADO = "caquetío-atestiguado"

# ── Los cronistas que cuentan como atestación primaria ───────────────────
# Todos escriben en el s. XV-XVI (o son documento administrativo de época).
CRONISTAS = {
    "Oviedo": r"Oviedo",
    "Las Casas": r"Las\s*Casas|Casas,|Hist\.?\s*Apol|Apolog",
    "Pané": r"\bPan[ée]\b|\bPane\b|Rom[áa]n\b",
    "Pedro Mártir": r"P(et|edro)?\.?\s*M[áa]rt[iy]r|Martyr|Angler[íi]a|Decad",
    "Colón": r"\bCol[óo]n\b|Colomb|Almirante|Diario del primer viaje",
    "Chanca": r"Chanca",
    "Gómara": r"G[óo]mara",
    "Herrera": r"Herrera",
    "Benzoni": r"Benzoni",
    "Archivo de Indias": r"Documentos In[ée]ditos|Archivo de Indias|c[ée]dula|"
                         r"Documento de [ée]poca|Repartimiento",
    # M5 (2026-09-23): dos cronistas del XVI que Coll y Toste cita y la tabla no tenía
    "Enciso": r"Enciso",
    "Echagoian": r"Echagoi?an",
}
# Compiladores e intermediarios: NO atestiguan, sólo transmiten.
INTERMEDIARIOS = ("brinton-1871", "goeje-1939", "bachiller-morales-1883",
                  "pichardo-1862", "coll-y-toste-1897", "rafinesque-1836")
PRIMARIAS = ("oviedo-valdes-1851", "las-casas-1875", "pane-c1498")

# Marcas de conjetura moderna dentro de la glosa o de la nota de la fuente.
CONJETURA = re.compile(
    r"conjetura|reconstru|probablement|prob\.|¿|\?|mot italien|mot espagnol|"
    r"palabra espa[ñn]ola|del espa[ñn]ol|Rafinesque|no me parece ind[íi]gena|"
    r"pasan por ind[íi]genas|vascuence", re.I)

# Voces que una fuente saca del taíno, con la lengua a la que la manda.
# Se construye leyendo los YAML; esto es sólo el vocabulario de lenguas.
OTRAS_LENGUAS = re.compile(
    r"caribe insular|kalinago|eyeri|caribe de Honduras|gar[íi]funa|"
    r"espa[ñn]ol|tup[íi]|africano|maya|azteca|quechua|kechua|vascuence|"
    r"lokono|arawak de Guayana|goajira", re.I)

# ═════════════════════════════════════════════════════════════════════════
# COTEJOS DE CADENA — donde el intermediario contradice al primario
#
# Esto NO se deriva: se DECLARA, porque exige leer la fuente primaria y
# compararla letra a letra con lo que el intermediario dice que copió. Cada
# fila dice quién midió cada lado, porque no todo lo midió esta parcela.
# ═════════════════════════════════════════════════════════════════════════
COTEJOS_DE_CADENA = [
    {
        "voz": "los numerales taínos",
        "el_eslabon": "Brinton 1871 p. 14 → Las Casas, *Apologética Historia* cap. 204",
        "lo_que_dice_el_intermediario": {
            "verbatim": ("«The following numerals are given by Las Casas (Hist. Apol. cap. 204). "
                         "1 hequeti. 2 yamosa. 3 cauocum. 4 yaraoucobre»"),
            "quien_lo_midio": ("esta parcela, sobre `fuentes_caquetios/Brinton_1871_texto.txt`, "
                               "2026-09-22"),
        },
        "lo_que_dice_el_primario": {
            "fuente": "Las Casas, *Apologética Historia* (NBAE 13), p. 177 impresa",
            "formas": ["yamocá (2)", "canocúm (3)", "yamoncobre (4)"],
            "quien_lo_midio": ("el agente de la Apologética de esta misma campaña, 2026-09-22. "
                               "⚠️ DATO RECIBIDO, no verificado por esta parcela: el repo NO "
                               "tiene la *Apologética*."),
        },
        "el_tercero_independiente": {
            "fuente": "Goeje 1939 p. 17",
            "formas": ["heketi (1)", "yamoka (2)", "kanokum (3)", "yamonko-bre (4)"],
            "quien_lo_midio": "esta parcela",
        },
        "veredicto": (
            "🔴 **LA CADENA ESTÁ ROTA EN BRINTON, y en 3 de los 4 numerales.** En los tres, "
            "Goeje —que no copia a Brinton aquí— coincide con la *Apologética* y Brinton es "
            "el que se sale: `yamosa` contra `yamocá`/`yamoka`, `cauocum` contra "
            "`canocúm`/`kanokum`, `yaraoucobre` contra `yamoncobre`/`yamonko-bre`. El 1 "
            "(`hequeti` ~ `heketi`) es el único que aguanta."),
        "la_prueba_interna": (
            "y no hace falta la *Apologética* para verlo: **Brinton se contradice a sí mismo**. "
            "Escribe que el 4 «evidently formed from yamosa» — pero su propia forma, "
            "`yaraoucobre`, no contiene `yamosa` por ningún lado, mientras que la forma real, "
            "`yamoncobre`, sí empieza por `yamo-`. El análisis es correcto y la transcripción "
            "no: Brinton leyó bien y copió mal. Esa frase estaba en el repo desde el "
            "2026-07-29 y nadie la había puesto a prueba contra sí misma."),
        "lo_que_toca_en_el_canon": (
            "la clave `yamosa` del lexicón —una de las 52— viene de la lectura mala. La forma "
            "atestiguada es `yamocá`, con `yamoka` de Goeje al lado. **Es un caso de la "
            "política «donde hay forma atestiguada, manda la atestiguada», sólo que aquí la "
            "rival no es una reconstrucción nuestra: es una errata de 1871.** Lo decide Miguel."),
        "y_lo_general": (
            "si Brinton falla en 3 de 4 donde se le puede cotejar, **las 68 entradas de su "
            "vocabulario antillano y las 84 entradas del lexicón que lo citan quedan bajo "
            "sospecha de transcripción**, no de existencia. La voz existe; la letra hay que "
            "verificarla contra el cronista. Es la razón de ser de esta lista maestra."),
    },
    {
        "voz": "macana",
        "el_eslabon": "Las Casas, *Apologética Historia* (NBAE 13), p. 177 impresa — directo",
        "lo_que_dice_el_primario": {
            "verbatim": "«vocablo desta isla y no de la Tierra Firme»",
            "quien_lo_midio": ("el agente de la Apologética de esta misma campaña, 2026-09-22. "
                               "⚠️ DATO RECIBIDO, no verificado por esta parcela."),
        },
        "lo_que_dice_el_intermediario": {
            "fuente": "Brinton 1871",
            "formas": [],
            "quien_lo_midio": ("esta parcela: **`macana` aparece 0 veces en "
                               "`Brinton_1871_texto.txt`**. Brinton no la trae."),
        },
        "el_tercero_independiente": {
            "fuente": "Goeje 1939 p. 11",
            "formas": ["makána 'sabre en bois, massue'; A sapakana, G guaika, achagua bakaba"],
            "quien_lo_midio": "esta parcela",
        },
        "veredicto": (
            "🔴 **ATRIBUCIÓN EXPLÍCITA DEL CRONISTA, y es de las que casi no hay.** Las Casas "
            "no glosa la voz: declara **de dónde es**, y dice que es de la isla y NO de Tierra "
            "Firme. Con Oviedo detrás (la lista maestra ya le da dos cronistas) es la voz mejor "
            "documentada de esta parcela en cuanto a origen."),
        "lo_que_toca_en_el_canon": (
            "toca `6-fusion/propuesta_macana_etiqueta_2026-09-21.yaml` y toca la esfera: si "
            "`macana` es antillana por declaración del cronista, su presencia en tierra firme "
            "es **préstamo**, y Bachiller p. 239 documenta la vía (Gumilla la registra en uso "
            "en el Orinoco, con el castellano de por medio, en el s. XVIII). ⚠️ NO confundir "
            "con `matacán` 'venado' (`6-fusion/matacan_venado_2026-09-14.yaml`): son dos "
            "palabras distintas y sólo se parecen de lejos."),
    },
]


# ═════════════════════════════════════════════════════════════════════════
# Normalizar una forma taína para agrupar
# ═════════════════════════════════════════════════════════════════════════
def sin_diacriticos(s):
    return unicodedata.normalize(
        "NFC", "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                       if unicodedata.category(c) != "Mn"))


def _lema1(f):
    f = re.sub(r"\([^)]*\)", " ", f)
    f = re.sub(r"[^a-zñ\- ]", "", f)
    f = f.replace("-", "").replace(" ", "")
    if not f:
        return ""
    f = re.sub(r"^h", "", f)                 # hobo ~ obo
    f = f.replace("qu", "k").replace("c", "k").replace("z", "s")
    f = f.replace("x", "s").replace("j", "s").replace("g", "k")
    f = f.replace("v", "b").replace("w", "u").replace("y", "i")
    f = re.sub(r"(.)\1+", r"\1", f)
    return f


def lemas(forma):
    """TODAS las variantes de una entrada, normalizadas.

    Las fuentes escriben `Dulios / duohos`, `naitano ó nitaino`,
    `hupia ~ opia ~ operito`. Si sólo se toma la primera, la misma voz queda
    partida en dos y el conteo de atestaciones baja: es el error que este
    script existe para no cometer.

    ⚠️ Esto agrupa, NO lematiza el canon. El lema canónico de una entrada se
    fija en la fusión (`fusionar-propuesta` §5), no aquí.
    """
    f = sin_diacriticos(forma).lower().strip()
    partes = re.split(r"\s*[~/,;]\s*|\s+[óo]\s+|\s+y\s+", f)
    out = []
    for p in partes:
        L = _lema1(p)
        if L and L not in out:
            out.append(L)
    return out


def lema(forma):
    L = lemas(forma)
    return L[0] if L else ""


# ═════════════════════════════════════════════════════════════════════════
# Lectores — uno por transcripción, porque cada una tiene su esquema
# ═════════════════════════════════════════════════════════════════════════
def _y(nombre):
    p = os.path.join(R, "6-fusion", nombre)
    if not os.path.exists(p):
        return None
    return yaml.safe_load(io.open(p, encoding="utf-8"))


def _reg(forma, glosa, obra, clase_obra, **kw):
    d = {"forma_fuente": str(forma), "glosa_fuente": str(glosa or ""),
         "obra": obra, "tipo_de_obra": clase_obra}
    d.update({k: v for k, v in kw.items() if v not in (None, "", [])})
    return d


def leer_brinton():
    Y = _y("taino_brinton_1871.yaml")
    out = []
    if not Y:
        return out
    for e in Y["vocabulario_antillano"]["entradas"]:
        out.append(_reg(e.get("forma"), e.get("glosa"), "brinton-1871", "intermediario",
                        pagina=e.get("pagina"), declara=e.get("cronista"),
                        comparanda_lokono=e.get("lokono"),
                        en_el_lexicon=e.get("en_el_lexicon"),
                        aviso=e.get("ojo") or e.get("nota_de_brinton")))
    return out


def leer_oviedo():
    Y = _y("taino_oviedo_valdes_1851.yaml")
    out = []
    if not Y:
        return out
    for bloque in ("costa_de_venezuela", "la_espanola", "otras_islas"):
        for e in Y.get(bloque) or []:
            out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                            "oviedo-valdes-1851", "primaria",
                            pagina=e.get("pagina_impresa"),
                            declara="Oviedo",
                            variedad=e.get("variedad_declarada") or e.get("atribucion"),
                            campo=e.get("campo"), en_el_lexicon=e.get("en_el_lexicon"),
                            bloque=bloque))
    for e in Y.get("no_taino") or []:
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "oviedo-valdes-1851", "primaria",
                        pagina=e.get("pagina_impresa"), declara="Oviedo",
                        variedad=e.get("lengua"), campo=e.get("campo"),
                        en_el_lexicon=e.get("en_el_lexicon"),
                        sacada_del_taino="la fuente la declara de otra lengua: %s"
                                         % e.get("lengua")))
    return out


def leer_las_casas():
    Y = _y("taino_las_casas_1875.yaml")
    out = []
    if not Y:
        return out
    for e in Y.get("voces") or []:
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "las-casas-1875", "primaria",
                        pagina=e.get("pagina_impresa"), declara="Las Casas",
                        variedad=e.get("atribucion"), campo=e.get("campo"),
                        en_el_lexicon=e.get("en_el_lexicon")))
    return out


def leer_pane():
    Y = _y("taino_pane_c1498.yaml")
    out = []
    if not Y:
        return out
    for e in Y.get("voces") or []:
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "pane-c1498", "primaria",
                        pagina=("cap. %s" % e.get("capitulo")) if e.get("capitulo") else None,
                        declara="Pané", variedad=e.get("atribucion"),
                        campo=e.get("campo"), en_el_lexicon=e.get("en_el_lexicon")))
    for e in (Y.get("teonimos_y_rito") or {}).get("deidades") or []:
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "pane-c1498", "primaria",
                        pagina=("cap. %s" % e.get("capitulo")) if e.get("capitulo") else None,
                        declara="Pané", campo="creencia",
                        en_el_lexicon=e.get("en_el_lexicon")))
    return out


def leer_goeje():
    Y = _y("taino_goeje_1939.yaml")
    out = []
    if not Y:
        return out
    for e in Y.get("vocabulario") or []:
        if not isinstance(e, dict):
            continue
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "goeje-1939", "intermediario",
                        pagina=e.get("pagina_impresa"),
                        declara=e.get("fuente_que_declara_el_autor"),
                        variedad=e.get("variedad_o_isla"),
                        campo=e.get("campo"),
                        comparanda_lokono=e.get("correspondencia_lokono"),
                        en_el_lexicon=e.get("en_el_lexicon"),
                        aviso=e.get("nota")))
    sacadas = Y.get("lo_que_goeje_saca_del_taino") or {}
    for bloque, etiqueta in (("mots_taino_d_origine_espagnole", "no indígena, según Goeje"),
                             ("voces_que_pasan_al_caribe_insular", "caribe insular, según Goeje")):
        b = sacadas.get(bloque) or {}
        for e in b.get("entradas") or []:
            out.append(_reg(e.get("forma"), e.get("glosa"), "goeje-1939", "intermediario",
                            declara=e.get("que_dice_goeje"),
                            en_el_lexicon=e.get("en_el_lexicon"),
                            sacada_del_taino=etiqueta))
    return out


def leer_bachiller():
    Y = _y("taino_bachiller_morales_1883.yaml")
    out = []
    if not Y:
        return out
    A = Y.get("apendice_a_rafinesque") or {}
    for e in A.get("entradas_que_tocan_el_lexicon") or []:
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "bachiller-morales-1883", "intermediario",
                        pagina=A.get("pagina_impresa"),
                        declara=(e.get("nota") or "") + " || vía Rafinesque",
                        variedad=e.get("variedad_o_isla"),
                        en_el_lexicon=e.get("en_el_lexicon"),
                        aviso="la lista de origen es la de Rafinesque, de quien Goeje "
                              "avisa que mezcla caribe"))
    E = A.get("el_bloque_eyeri") or {}
    marcas = marcas_del_bloque_eyeri()
    for e in E.get("voces_eyeri_que_tocan_el_lexicon") or []:
        forma = str(e.get("forma") or "")
        es_b = marcas.get(forma.split("/")[0].strip().lower()) == "B"
        out.append(_reg(forma, e.get("glosa_en_la_lista"),
                        "bachiller-morales-1883", "intermediario",
                        pagina=A.get("pagina_impresa"), declara="Rafinesque, vía Rochefort",
                        variedad="Borinquen (marca B.)" if es_b else "eyeri (Borinquen)",
                        en_el_lexicon=e.get("en_el_lexicon"),
                        aviso=("T10 la leyó como eyeri en el OCR; en la imagen lleva la marca B. "
                               "(M5, 2026-09-23)") if es_b else None,
                        sacada_del_taino=None if es_b else
                        "eyeri (caribe insular), en la lista de Bachiller"))
    for e in (Y.get("apendice_c") or {}).get("entradas_que_tocan_el_lexicon") or []:
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "bachiller-morales-1883", "intermediario",
                        pagina=e.get("pagina_impresa"),
                        declara=e.get("fuente_que_declara_el_autor"),
                        en_el_lexicon=e.get("en_el_lexicon"),
                        sacada_del_taino="el propio Bachiller la pone entre las que "
                                         "pasan por indígenas y vienen de otras partes"))
    for e in Y.get("entradas_decisivas") or []:
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "bachiller-morales-1883", "intermediario",
                        pagina=e.get("pagina_impresa"),
                        declara=e.get("fuente_que_declara_el_autor"),
                        variedad=e.get("variedad_o_isla"), campo=e.get("campo"),
                        en_el_lexicon=e.get("en_el_lexicon"),
                        aviso=e.get("lectura")))
    return out


# ═════════════════════════════════════════════════════════════════════════
# Tercera campaña, parcela M5 (2026-09-23): lo que T10 dejó a medias
# ═════════════════════════════════════════════════════════════════════════
ISLA = {"C": "Cuba", "J": "Jamaica", "L": "Lucayas", "C y L": "Cuba y Lucayas"}


def marcas_del_bloque_eyeri():
    """{forma en minúsculas: 'E' | 'B' | 'N'} leído en la IMAGEN de Bachiller p. 389."""
    Y = _y("taino3_bachiller_morales_1883.yaml") or {}
    return {str(e["forma"]).lower(): str(e.get("marca"))
            for e in Y.get("fragmentos_eyeri_y_borinquen") or []}


def leer_bachiller_m5():
    """El apéndice (A) ENTERO y el bloque eyeri ENTERO (M5), leídos en imagen."""
    Y = _y("taino3_bachiller_morales_1883.yaml")
    out = []
    if not Y:
        return out
    for e in Y.get("apendice_a_completo") or []:
        for f in e.get("formas") or []:
            out.append(_reg(f.get("forma"), e.get("concepto_fuente"),
                            "bachiller-morales-1883", "intermediario",
                            pagina=e.get("pagina_impresa"),
                            declara=((e.get("cronista_que_nombra") or "") +
                                     " || lista de Rafinesque (apéndice A)"),
                            variedad=ISLA.get(str(f.get("isla")), f.get("isla")),
                            aviso=" ".join(x for x in (e.get("bachiller"), e.get("nota")) if x)
                            or None))
    for e in Y.get("fragmentos_eyeri_y_borinquen") or []:
        marca = str(e.get("marca"))
        out.append(_reg(e.get("forma"), e.get("concepto_fuente"),
                        "bachiller-morales-1883", "intermediario",
                        pagina=389, declara="lista de Rafinesque, vía Rochefort",
                        variedad="eyeri (Borinquen)" if marca == "E" else "Borinquen (marca %s.)" % marca,
                        aviso=" ".join(x for x in (e.get("bachiller"), e.get("nota")) if x) or None,
                        sacada_del_taino=("eyeri = habla de mujeres del caribe insular "
                                          "(Bachiller p. 389; Goeje 1939)") if marca == "E" else None))
    return out


def leer_coll_y_toste():
    """Coll y Toste, caps. XII y X — transcripción AUTOMÁTICA sobre OCR ajeno (M5).
    El tipo de apoyo lo decidió `transcribir_coll_y_toste.py`; aquí sólo se traduce a
    las marcas de este consolidador."""
    Y = _y("taino3_coll_y_toste_1897.yaml")
    out = []
    if not Y:
        return out
    for e in Y.get("voces") or []:
        tipo = e.get("tipo_de_apoyo")
        aviso = {"conjetura-del-autor": "conjetura del autor (%s)" % (e.get("marca") or ""),
                 "secundaria": "sólo autoridades del XVII-XIX"}.get(tipo)
        isla = e.get("variedad_o_isla")
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "coll-y-toste-1897", "intermediario",
                        pagina=e.get("pagina_impresa"),
                        declara=e.get("fuente_que_declara_el_autor"),
                        variedad=", ".join(isla) if isinstance(isla, list) else None,
                        campo=e.get("campo"), en_el_lexicon=e.get("en_el_lexicon"),
                        aviso=aviso,
                        sacada_del_taino=("el propio Coll y Toste la saca: «%s»" % e.get("marca"))
                        if tipo == "sacada-por-el-autor" else None))
    for e in Y.get("vocabulario_espanol_boriqueno") or []:
        out.append(_reg(e.get("forma_fuente"), e.get("glosa_fuente"),
                        "coll-y-toste-1897", "intermediario",
                        pagina=e.get("pagina_impresa"),
                        declara="no-declarada (cap. X, vocabulario inverso: la cita va en el cap. XII)",
                        en_el_lexicon=e.get("en_el_lexicon")))
    return out


LECTORES = [("brinton-1871", leer_brinton), ("oviedo-valdes-1851", leer_oviedo),
            ("las-casas-1875", leer_las_casas), ("pane-c1498", leer_pane),
            ("goeje-1939", leer_goeje), ("bachiller-morales-1883", leer_bachiller),
            ("bachiller-morales-1883 (M5)", leer_bachiller_m5),
            ("coll-y-toste-1897 (M5)", leer_coll_y_toste)]


# ═════════════════════════════════════════════════════════════════════════
# Cadena de custodia
# ═════════════════════════════════════════════════════════════════════════
def cronistas_de(reg):
    """Qué cronistas del XV-XVI respaldan ESTE registro."""
    if reg["tipo_de_obra"] == "primaria":
        return {reg["declara"]} if reg.get("declara") else set()
    texto = " ".join(str(reg.get(k) or "") for k in ("declara", "aviso"))
    return {n for n, rx in CRONISTAS.items() if re.search(rx, texto)}


def clase_de(voz):
    if voz["atestaciones_independientes"] >= 1:
        return ("i-primaria-del-XVI",
                "la atestigua%s %s" % ("n" if voz["atestaciones_independientes"] > 1 else "",
                                       ", ".join(voz["cronistas_independientes"])))
    if voz["solo_conjetura"]:
        return ("iii-conjetura-moderna",
                "ninguna obra dice de qué cronista sale, y todo lo que la sostiene lleva "
                "marca de conjetura moderna (reconstrucción, duda del autor, o la lista de "
                "Rafinesque, de la que Goeje 1939 avisa que mezcla caribe). NO ENTRA.")
    return ("ii-solo-secundaria",
            "la trae%s %s y ninguna dice de qué cronista sale: existe, pero no está "
            "atestiguada" % ("n" if voz["obras_que_la_traen_n"] > 1 else "",
                             ", ".join(voz["obras_que_la_traen"])))


# ═════════════════════════════════════════════════════════════════════════
# Conceptos comparables con el caquetío atestiguado
# ═════════════════════════════════════════════════════════════════════════
def cabezas_exactas(glosa):
    """Las cabezas de concepto de una glosa, sólo las de UNA palabra."""
    return {cab for cab, exacto, _seg in conceptos(glosa) if exacto}


GLOSAS_FR_ES = {
    # La lista taína nueva trae glosas en FRANCÉS (Goeje). Para poder cruzarla
    # con el caquetío hay que traducirlas, y la traducción se DECLARA aquí,
    # palabra a palabra, en vez de esconderse en un diccionario implícito.
    # Sólo se traduce lo que es una palabra sola: lo demás no es comparable
    # ni en castellano.
    "front": "frente", "mamelle": "pecho", "fesses": "nalgas", "galeux": "sarnoso",
    "ciel": "cielo", "noir": "negro", "ouragan": "huracán", "forêt": "bosque",
    "savane": "sabana", "pierre": "piedra", "île": "isla", "iguane": "iguana",
    "luciole": "cocuyo", "tortue": "tortuga", "caïman": "caimán",
    "ananas": "piña", "arachide": "maní", "calebasse": "calabaza",
    "goyave": "guayaba", "liane": "bejuco", "papaye": "papaya",
    "piment": "ají", "maison": "casa", "rame": "remo", "hamac": "hamaca",
    "corde": "cuerda", "panier": "cesto", "godet": "vaso", "masque": "máscara",
    "âme": "alma", "un": "uno", "deux": "dos", "trois": "tres", "quatre": "cuatro",
    "rien": "nada", "seigneur": "señor", "ennemi": "enemigo", "bataille": "batalla",
    "or": "oro", "mer": "mar", "grelots": "cascabeles", "chaussure": "calzado",
    "perroquet": "loro", "pivert": "carpintero", "palmier": "palma",
    "maïs": "maíz", "esprit": "espíritu", "sang": "sangre", "nez": "nariz",
    # M5 (2026-09-23): lo que el vocabulario KALINAGO de Goeje glosa con una palabra y
    # el caquetío atestiguado tiene. Se añadió mirando la lista de conceptos caquetíos,
    # así que es una tabla DIRIGIDA: sirve para no perder un par, no para inflar el
    # total (una glosa francesa sin par caquetío no cuenta aunque esté aquí).
    "soleil": "sol", "lune": "luna", "femme": "mujer", "homme": "hombre",
    "serpent": "serpiente", "poisson": "pez", "dent": "diente", "singe": "mono",
    "vent": "viento", "chemin": "camino", "sel": "sal", "arbre": "árbol",
    "rivière": "río", "sable": "arena", "chauve-souris": "murciélago",
    "hibou": "lechuza", "pigeon": "paloma", "sauterelle": "langosta",
    "cuiller": "cuchara", "flûte": "flauta", "grand": "grande", "vieux": "viejo",
    "fils": "hijo", "donner": "dar", "entendre": "oír", "semer": "sembrar",
    "marcher": "caminar", "garder": "guardar", "lagune": "laguna", "côte": "costa",
    "montagne": "sierra", "blatte": "cucaracha",
}


def a_castellano(glosa):
    """Glosa comparable: si viene en francés y es una palabra de la tabla, se
    traduce; si no, se deja como está. Lo que no se pueda traducir NO se
    inventa — se queda fuera del conteo, que es lo honesto."""
    g = str(glosa or "").strip().lower()
    g = re.sub(r"\s*\(.*$", "", g).strip()
    clave = re.sub(r"^(le|la|les|un|une|l')\s*", "", g)
    if clave in GLOSAS_FR_ES:
        return GLOSAS_FR_ES[clave]
    return glosa


def medir_conceptos_comparables(voces):
    """El número que decide si el cruce se puede re-correr.

    Usa la MISMA normalización de glosa que `cruce_taino_caquetio.py`
    (`conceptos()`, importado de ahí), para que las dos cifras sean del mismo
    instrumento. No se re-implementa: se importa.
    """
    # las cabezas de concepto de la capa caquetía ATESTIGUADA
    caq = {}
    for k, v in CL.VOCABULARIO_BASE.items():
        if CL.capa_epistemica(v.get("fuente")) != ATESTIGUADO:
            continue
        for cab in cabezas_exactas(v.get("sig")):
            caq.setdefault(cab, []).append(k)
    # las cabezas de la lista taína NUEVA
    tn = {}
    for voz in voces:
        if voz["clase"] == "iii-conjetura-moderna":
            continue
        for g in voz["glosas_verbatim"]:
            for cab in cabezas_exactas(a_castellano(g)):
                tn.setdefault(cab, set()).add(voz["lema"])
    comunes = sorted(set(caq) & set(tn))
    # la lista VIEJA: sólo las entradas taínas del lexicón
    tn_viejo = {}
    gemelas = set(CL.FORMA_DE_LA_ESFERA)
    for k, v in CL.VOCABULARIO_BASE.items():
        if v.get("fuente") != "taíno" or k in gemelas:
            continue
        for cab in cabezas_exactas(v.get("sig")):
            tn_viejo.setdefault(cab, set()).add(k)
    comunes_viejo = sorted(set(caq) & set(tn_viejo))
    return {
        "metodo": (
            "la MISMA normalización de glosa que `cruce_taino_caquetio.py`: se importa "
            "`conceptos()` de ese script, no se reimplementa. Cuenta un concepto cuando "
            "la cabeza de glosa es de UNA palabra en las dos lenguas (el solapamiento "
            "parcial no cuenta, igual que en la política del atestiguado)."),
        "glosas_en_frances": (
            "Goeje glosa en francés. Se traducen las glosas de UNA palabra con una tabla "
            "DECLARADA en el script (`GLOSAS_FR_ES`, %d entradas); lo que no está en la "
            "tabla no se traduce ni se inventa, y por tanto NO cuenta. La cifra de abajo "
            "es un SUELO, no un techo." % len(GLOSAS_FR_ES)),
        "conceptos_del_caquetio_atestiguado": len(caq),
        "conceptos_de_la_lista_TAINA_VIEJA_solo_lexicon": len(tn_viejo),
        "conceptos_de_la_lista_MAESTRA_nueva": len(tn),
        "comparables_con_la_lista_vieja": len(comunes_viejo),
        "comparables_con_la_lista_MAESTRA": len(comunes),
        "los_comparables_uno_a_uno": [
            {"concepto": c,
             "caquetio": sorted(caq[c]),
             "taino_lista_maestra": sorted(tn[c])[:6],
             "ya_estaba_en_la_lista_vieja": c in comunes_viejo}
            for c in comunes],
        "los_que_solo_aporta_la_lista_nueva": sorted(set(comunes) - set(comunes_viejo)),
    }


def medir_kalinago(caq_cabezas):
    """El cruce de las voces kalinago del lexicón con Goeje (M5) y cuántos conceptos del
    caquetío atestiguado tienen voz kalinago transcrita. Lee
    `6-fusion/kalinago_goeje_1939.yaml`; los veredictos son lecturas en imagen, aquí sólo
    se CUENTAN (regla 1)."""
    Y = _y("kalinago_goeje_1939.yaml")
    if not Y:
        return None
    filas = [f for f in Y.get("cruce_con_el_lexicon") or [] if isinstance(f, dict) and f.get("veredicto")]
    por = collections.Counter(f["veredicto"] for f in filas)
    claves_lex = sorted(k for k, v in CL.VOCABULARIO_BASE.items() if v.get("fuente") == "kalinago")
    cruzadas = {f["clave"] for f in filas}
    kal = {}
    for e in Y.get("vocabulario") or []:
        g = str(e.get("glosa_fuente") or "")
        if g.startswith("id."):
            continue
        for cab in cabezas_exactas(a_castellano(g)):
            kal.setdefault(cab, set()).add(str(e.get("forma_fuente")))
    for f in filas:          # las líneas leídas en imagen para el cruce cuentan también
        for cab in cabezas_exactas(f.get("glosa_en_el_lexicon")):
            if f["veredicto"] != "sin-apoyo":
                kal.setdefault(cab, set()).add(f["clave"])
    comunes = sorted(set(caq_cabezas) & set(kal))
    return {
        "que_mide": (
            "las voces kalinago del lexicón leídas contra Goeje 1939 (veredictos escritos a "
            "mano en `kalinago_goeje_1939.yaml` §cruce, leídos en imagen) y los conceptos del "
            "caquetío atestiguado que tienen voz kalinago en lo transcrito. ⚠️ El vocabulario "
            "kalinago está transcrito a medias (ver su §tramos): es un SUELO."),
        "claves_kalinago_en_el_lexicon": len(claves_lex),
        "cruzadas": len(cruzadas & set(claves_lex)),
        "sin_cruzar": sorted(set(claves_lex) - cruzadas),
        "por_veredicto": dict(sorted(por.items())),
        "entradas_de_vocabulario_transcritas": len(Y.get("vocabulario") or []),
        "conceptos_kalinago_transcritos": len(kal),
        "comparables_con_el_caquetio_atestiguado": len(comunes),
        "los_comparables": [{"concepto": c, "kalinago": sorted(kal[c])[:6]} for c in comunes],
    }


# ═════════════════════════════════════════════════════════════════════════
# Construir
# ═════════════════════════════════════════════════════════════════════════
def construir():
    registros = []
    por_obra = {}
    for nombre, fn in LECTORES:
        rs = fn()
        por_obra[nombre] = len(rs)
        registros.extend(rs)

    # ── agrupar por lema, uniendo por CUALQUIER variante (union-find) ──
    padre = {}

    def raiz(x):
        padre.setdefault(x, x)
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    def unir(a, b):
        ra, rb = raiz(a), raiz(b)
        if ra != rb:
            padre[rb] = ra

    sin_lema = 0
    lemas_por_reg = []
    for r in registros:
        if not str(r.get("forma_fuente") or "").strip() or \
                str(r["forma_fuente"]).strip().lower() == "none":
            sin_lema += 1
            lemas_por_reg.append([])
            continue
        Ls = lemas(r["forma_fuente"])
        if not Ls:
            sin_lema += 1
            lemas_por_reg.append([])
            continue
        for L in Ls:
            raiz(L)
        for L in Ls[1:]:
            unir(Ls[0], L)
        lemas_por_reg.append(Ls)

    grupos = collections.defaultdict(list)
    for r, Ls in zip(registros, lemas_por_reg):
        if Ls:
            grupos[raiz(Ls[0])].append(r)

    voces = []
    for L in sorted(grupos):
        rs = grupos[L]
        cron = set()
        for r in rs:
            cron |= cronistas_de(r)
        obras = sorted({r["obra"] for r in rs})
        glosas = []
        for r in rs:
            g = r["glosa_fuente"].strip()
            if g and g not in glosas:
                glosas.append(g)
        conj = [r for r in rs
                if CONJETURA.search(" ".join(str(r.get(k) or "")
                                             for k in ("glosa_fuente", "declara", "aviso")))]
        sacadas = [r for r in rs if r.get("sacada_del_taino")]
        variedades = sorted({str(r["variedad"]) for r in rs if r.get("variedad")})
        claves = sorted({str(r["en_el_lexicon"]) for r in rs
                         if r.get("en_el_lexicon") and str(r["en_el_lexicon"]).lower()
                         not in ("null", "none", "no")})
        voz = {
            "lema": L,
            "formas_atestiguadas": sorted({r["forma_fuente"] for r in rs}),
            "glosas_verbatim": glosas,
            "obras_que_la_traen": obras,
            "cadena_de_custodia": [
                {"obra": r["obra"], "tipo": r["tipo_de_obra"],
                 "pagina": r.get("pagina"),
                 "cronista_que_declara": sorted(cronistas_de(r)) or None,
                 "lo_que_dice_la_obra": (str(r.get("declara"))[:220]
                                         if r.get("declara") else None)}
                for r in rs],
            "cronistas_independientes": sorted(cron),
            "atestaciones_independientes": len(cron),
            "obras_que_la_traen_n": len(obras),
            "variedad_o_isla": variedades or ["no-declarada"],
            "en_el_lexicon": claves or None,
            "solo_conjetura": bool(conj) and len(conj) == len(rs),
            "comparanda_lokono": sorted({str(r["comparanda_lokono"]) for r in rs
                                         if r.get("comparanda_lokono")}) or None,
        }
        if sacadas:
            voz["sacada_del_taino"] = sorted({str(r["sacada_del_taino"]) for r in sacadas})
        voz["clase"], voz["por_que_esta_clase"] = clase_de(voz)
        if voz["obras_que_la_traen_n"] > voz["atestaciones_independientes"]:
            voz["aviso_de_independencia"] = (
                "%d obras la traen y sólo %d cronista(s) distinto(s) la atestigua(n): "
                "copiar no es atestiguar (skill §8)"
                % (voz["obras_que_la_traen_n"], voz["atestaciones_independientes"]))
        voces.append(voz)

    # ── las 52 del lexicón: qué clase les toca ahora ──
    claves_lexicon = sorted(k for k, v in CL.VOCABULARIO_BASE.items()
                            if str(v.get("fuente") or "").startswith("taíno"))
    indice = {}
    for voz in voces:
        for c in (voz["en_el_lexicon"] or []):
            # las transcripciones escriben la clave de mil maneras: «dujo»,
            # «cacique (taíno) · cacike (taíno)», «sí — `naboria`, glosa …».
            # Se cogen TODAS las claves del lexicón que aparezcan en el texto,
            # y si no aparece ninguna, las piezas separadas por · o coma.
            piezas = [k for k in claves_lexicon
                      if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(k), c)]
            if not piezas:
                piezas = [re.split(r"\s+[—-]\s+|\s*\(", p)[0].strip()
                          for p in re.split(r"\s*[·,]\s*", c)]
            for pieza in piezas:
                if pieza:
                    indice.setdefault(pieza, []).append(voz)
    cobertura = []
    for k in claves_lexicon:
        tocan = indice.get(k) or []
        mejor = None
        for voz in tocan:
            if mejor is None or voz["atestaciones_independientes"] > mejor["atestaciones_independientes"]:
                mejor = voz
        cobertura.append({
            "clave": k,
            "capa_en_el_lexicon": CL.VOCABULARIO_BASE[k].get("fuente"),
            "en_la_lista_maestra": bool(tocan),
            "clase": mejor["clase"] if mejor else "sin-voz-en-la-lista",
            "atestaciones_independientes": mejor["atestaciones_independientes"] if mejor else 0,
            "cronistas": mejor["cronistas_independientes"] if mejor else [],
            "sacada_del_taino": (mejor.get("sacada_del_taino") if mejor else None),
        })

    conteo_clase = collections.Counter(v["clase"] for v in voces)
    conteo_cob = collections.Counter(c["clase"] for c in cobertura)
    con_cita = [c for c in cobertura if c["atestaciones_independientes"] >= 1]
    conceptos_med = medir_conceptos_comparables(voces)
    caq_cab = set()
    for k, v in CL.VOCABULARIO_BASE.items():
        if CL.capa_epistemica(v.get("fuente")) == ATESTIGUADO:
            caq_cab |= cabezas_exactas(v.get("sig"))
    kalinago_med = medir_kalinago(caq_cab)
    por_campo = collections.Counter()
    for v in voces:
        campos = set()
        for r in grupos[v["lema"]]:
            c = r.get("campo")
            for x in (c if isinstance(c, list) else [c]):
                if x:
                    campos.add(str(x))
        for c in (campos or {"sin-campo"}):
            por_campo[c] += 1

    salida = {
        "meta": {
            "campana": "Segunda campaña del taíno — parcela T10 (los vocabularios antillanos)",
            "medido": FECHA,
            "script": "6-fusion/scripts/consolidar_taino.py",
            "estado": "PROPUESTA (regla 5). No toca curiana_sim/, 2-lengua/, 3-mundo/ ni el canon.",
            "pregunta": (
                "que el proyecto tenga UNA lista de voces taínas donde cada voz lleve su "
                "cadena de custodia hasta el cronista del s. XVI, y saber cuántos conceptos "
                "comparables con el caquetío atestiguado aporta."),
            "por_que": (
                "el cruce del 2026-09-21 midió 4 conceptos comparables y 0 parejas, y su "
                "autor escribió «el cero mide la lista, no la lengua». Esta lista es la "
                "lista nueva."),
            "la_regla_que_manda": (
                "la atestación es del CRONISTA, no del compilador (skill `minar-fuente` §8). "
                "Brinton, Goeje y Bachiller son intermediarios: dos obras que citan al mismo "
                "cronista son UNA atestación. Por eso `atestaciones_independientes` cuenta "
                "cronistas distintos, no obras."),
            "insumos": por_obra,
            "registros_leidos": len(registros),
            "registros_sin_forma_utilizable": sin_lema,
            "aviso_de_lema": (
                "`lema` agrupa grafías coloniales y fonémicas para poder contar; NO es el "
                "lema canónico de una entrada, que se fija en la fusión "
                "(`fusionar-propuesta` §5)."),
        },
        "resumen": {
            "voces_distintas": len(voces),
            "por_clase": dict(sorted(conteo_clase.items())),
            "con_dos_o_mas_cronistas_independientes":
                sum(1 for v in voces if v["atestaciones_independientes"] >= 2),
            "con_un_cronista": sum(1 for v in voces if v["atestaciones_independientes"] == 1),
            "sin_cronista_pero_en_una_obra":
                sum(1 for v in voces if v["atestaciones_independientes"] == 0),
            "con_variedad_o_isla_declarada":
                sum(1 for v in voces if v["variedad_o_isla"] != ["no-declarada"]),
            "sacadas_del_taino_por_alguna_fuente":
                sum(1 for v in voces if v.get("sacada_del_taino")),
            "con_aviso_de_independencia":
                sum(1 for v in voces if v.get("aviso_de_independencia")),
            "por_campo_declarado": dict(sorted(por_campo.items())),
            "aviso_de_campo": (
                "una voz cuenta en cada campo que alguna fuente le declara; `toponimo` y "
                "`antroponimo` salen casi todos de Coll y Toste (M5), cuyo campo lo pone una "
                "heurística sobre la glosa"),
        },
        "las_52_del_lexicon": {
            "que_mide": (
                "para cada clave taína del lexicón, qué clase le toca en la lista maestra. "
                "`sin-voz-en-la-lista` significa que ninguna de las seis transcripciones "
                "la recoge: ni atestiguada ni desmentida, simplemente ausente."),
            "claves": len(claves_lexicon),
            "con_al_menos_un_cronista": len(con_cita),
            "por_clase": dict(sorted(conteo_cob.items())),
            "detalle": cobertura,
        },
        "cadenas_cotejadas": {
            "que_es": (
                "los eslabones donde se ha podido comparar lo que el intermediario dice que "
                "copió con lo que la fuente primaria dice de verdad. Es lo único que convierte "
                "una cadena de custodia en una comprobación. **No se deriva: se declara**, "
                "porque exige leer las dos fuentes, y cada fila dice quién midió cada lado."),
            "cuantas": len(COTEJOS_DE_CADENA),
            "filas": COTEJOS_DE_CADENA,
        },
        "conceptos_comparables_con_el_caquetio_atestiguado": conceptos_med,
        "kalinago_de_goeje": kalinago_med,
        "voces": voces,
    }
    return salida


def texto_yaml(d):
    return yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=100,
                          default_flow_style=False)


def consola(s):
    print("\n── LISTA MAESTRA DEL TAÍNO ──")
    print("  voces distintas:", s["resumen"]["voces_distintas"])
    for k, v in s["resumen"]["por_clase"].items():
        print("    %-24s %s" % (k, v))
    print("  con 2+ cronistas independientes:",
          s["resumen"]["con_dos_o_mas_cronistas_independientes"])
    print("  con variedad o isla declarada:", s["resumen"]["con_variedad_o_isla_declarada"])
    print("  sacadas del taíno por alguna fuente:",
          s["resumen"]["sacadas_del_taino_por_alguna_fuente"])
    c = s["las_52_del_lexicon"]
    print("\n── las claves taínas del lexicón ──")
    print("  claves:", c["claves"], "· con al menos un cronista:", c["con_al_menos_un_cronista"])
    for k, v in c["por_clase"].items():
        print("    %-24s %s" % (k, v))
    print("\n── cadenas cotejadas contra el primario ──")
    for f in s["cadenas_cotejadas"]["filas"]:
        print("  %-22s %s" % (f["voz"], f["el_eslabon"][:70]))
    m = s["conceptos_comparables_con_el_caquetio_atestiguado"]
    print("\n── EL NÚMERO QUE DECIDE ──")
    print("  conceptos del caquetío atestiguado:", m["conceptos_del_caquetio_atestiguado"])
    print("  comparables con la lista VIEJA:   ", m["comparables_con_la_lista_vieja"])
    print("  comparables con la lista MAESTRA: ", m["comparables_con_la_lista_MAESTRA"])
    print("  los que sólo aporta la nueva:", ", ".join(m["los_que_solo_aporta_la_lista_nueva"]) or "—")
    k = s.get("kalinago_de_goeje")
    if k:
        print("\n── KALINAGO (Goeje 1939) ──")
        print("  claves kalinago del lexicón:", k["claves_kalinago_en_el_lexicon"],
              "· cruzadas:", k["cruzadas"], "·", k["por_veredicto"])
        print("  conceptos caquetíos atestiguados con voz kalinago:",
              k["comparables_con_el_caquetio_atestiguado"])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true",
                    help="no escribe: dice si el YAML del repo está al día")
    args = ap.parse_args(argv)

    salida = construir()
    nuevo = texto_yaml(salida)
    if args.check:
        viejo = io.open(SALIDA, encoding="utf-8").read() if os.path.exists(SALIDA) else ""
        if viejo == nuevo:
            print("✓ %s está al día" % os.path.relpath(SALIDA, R))
            return 0
        print("✗ %s DESFASADO: re-ejecuta el script sin --check" % os.path.relpath(SALIDA, R))
        return 1
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(nuevo)
    consola(salida)
    print("\n✓ %s" % os.path.relpath(SALIDA, R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
