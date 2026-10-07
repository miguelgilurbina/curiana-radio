#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Minería de van Koolwijk 1882, «De Indianen Caraïben van het eiland Aruba».

    Koolwijk, A. J. van (1882). Tijdschrift van het Aardrijkskundig
    Genootschap VI, pp. 222-229 + una lámina fuera de texto (n.º 7).
    → fuentes_caquetios/vanKoolwijk_1882_Indianen_Caraiben_Aruba.pdf (17 pp. de PDF)

Encargo de Miguel (2026-10-05): minarla «de una». Cinco preguntas: el
vocabulario, los topónimos de Aruba, la independencia frente a van Buurt (y
Gatschet), la lámina y lo demás por esferas.

LO QUE LA LECTURA CAMBIÓ DEL ENCARGO
------------------------------------
La lista larga de las pp. 227-229 (`töna` 'water', `wato` 'vuur', `kwai`,
`toëkoëwari`, `porkoe`…) NO es de Aruba: es el kari'ña (caribe) de Surinam,
ríos Tibiti y Wojambo, que el autor apuntó en 1870 y pone ahí «om aan te
toonen, dat deze taal geheel verschilt van die der Caraïben van Aruba»
(p. 227). Lo arubano es la lista corta de la p. 227. Y `kwai` es 'kalebas',
no 'pijl': el par lo había corrido pdftotext.

DE DÓNDE SALE CADA COSA
-----------------------
- La TRANSCRIPCIÓN está aquí, como datos: se leyó en IMAGEN, página por página,
  con recortes de pymupdf a la resolución nativa del escaneo (8,35 px/pt;
  2576 px sobre 309 pt), porque la capa de texto del PDF es parcial (las pp.
  222 y 229 casi no tienen) y desordena las columnas de la p. 228.
- Los CRUCES los calcula el script contra el repo: el lexicón
  (VOCABULARIO_BASE + FUERA_DEL_HABLA), el canon de topónimos
  (2-lengua/toponimos.yaml, generado), lexicon_gatschet.py (las listas de
  Pinart ya reconciliadas entre los dos OCR), el texto de van Buurt 2014 y las
  citas de «Koolwijk» en todas las fuentes de texto del repo.
- Las PROPUESTAS (etiqueta, nivel, veredicto) son del minador, van en cada
  entrada y son eso: propuestas (regla 5). Nada de aquí toca el canon.

LOS CRUCES DE FORMA son de BÚSQUEDA (skill leer-fuente §5): `fon()` colapsa la
ortografía neerlandesa (oe→u, j→y, sj→sh…) para encontrar, no para hacer
lemas. Y un parecido de forma sin filtro de significado es casi todo ruido
(minar-fuente §2): por eso cada voz se cruza también POR GLOSA, y el
veredicto lo dice la lectura, no el ratio.

No llama a ninguna API, no lee curiana_sim/.env, no toca la base.

    python 6-fusion/scripts/minar_van_koolwijk_1882.py            # resumen medido
    python 6-fusion/scripts/minar_van_koolwijk_1882.py --escribir # (re)escribe el YAML
    python 6-fusion/scripts/minar_van_koolwijk_1882.py --check    # ¿el YAML está al día?
"""

import argparse
import difflib
import io
import os
import re
import sys
import unicodedata

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIM = os.path.join(RAIZ, "curiana_sim")
FUENTES = os.path.join(RAIZ, "fuentes_caquetios")
SALIDA = os.path.join(RAIZ, "6-fusion", "van_koolwijk_1882_aruba_2026-10-05.yaml")
CANON_TOP = os.path.join(RAIZ, "2-lengua", "toponimos.yaml")
MORFEMAS = os.path.join(RAIZ, "2-lengua", "morfemas.yaml")
VAN_BUURT_TXT = os.path.join(FUENTES, "VanBuurt_2014_CaquetioWords_Papiamentu.txt")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")

sys.path.insert(0, SIM)

OBRA = "van-koolwijk-1882"
# pdf → página impresa. Medido: pdf 5 lleva «223», pdf 6 «224», … pdf 11 «229»;
# pdf 4 es la primera del artículo (sin número) y Wagenaar Hummelinck 1953
# (bibliografía, línea «1882 KOOLWIJK…») da «p. 222-229, tab. excl.».
PDF_A_IMPRESA = {4: 222, 5: 223, 6: 224, 7: 225, 8: 226, 9: 227, 10: 228, 11: 229}
LAMINA_PDF = (12, 13)
PAGINAS_SIN_ARTICULO = {1: "tapa", 2: "guarda", 3: "guarda con la ficha de préstamo de la biblioteca",
                        14: "guarda en blanco", 15: "guarda en blanco", 16: "contratapa",
                        17: "hoja de licencia CC BY 4.0 de la Biblioteca Nacional Aruba"}
FACTOR_NATIVO = "8,35 px/pt: 2576 px de imagen sobre 309 pt de página"


# ═════════════════════════════════════════════════════════════════════════
# 1. LA TRANSCRIPCIÓN (leída en imagen; ver la cabecera)
# ═════════════════════════════════════════════════════════════════════════
# Convención: el macrón y la breve se copian donde caen. El macrón sobre el
# dígrafo neerlandés «oe» (= /u/) se escribe sobre la o: «ōe». Una letra que
# el tipo roto no deja decidir va entre [corchetes].

# ── 1a. Lo arubano: p. 227 (pdf 9), col. izquierda, y una nota de la p. 224 ──
# kw = palabras de la glosa castellana con que se cruza el lexicón por SIGNIFICADO.
VOCES_ARUBA = [
    dict(id="vk-aru-01", gatschet='tida meo', forma="hida of hida meeuw", formas=["hida", "hida meeuw"],
         nl="Hoe gaat het?", es="¿cómo estás? (saludo)", kw=["saludo"],
         lengua="indeterminada", escala="C",
         veredicto="nueva-en-el-repo-como-glosa (la forma ya estaba vía Gatschet)",
         propuesta="No entra al lexicón. Resuelve la lectura de Gatschet: «tida meo» (JSTOR) / «^ida meo» (BioStor) es «hida meeuw»; y la glosa de la fuente primaria es «¿cómo estás?», no «good morning». La sospecha de Gatschet minado (saludo en isla papiamentera) sigue en pie."),
    dict(id="vk-aru-02", gatschet=None, forma="auw", formas=["auw"],
         nl="Antw. Goed", es="bien (respuesta al saludo)", kw=["bien", "bueno"],
         lengua="indeterminada", escala="C", veredicto="nueva",
         propuesta="No entra al lexicón: interjección de respuesta, la clase de menor rendimiento (protocolo §6). Sólo la da van Koolwijk."),
    dict(id="vk-aru-03", gatschet='aba dobo edan guayete', forma="hafe dōbo danwajēte", formas=["hafe dobo danwajete", "danwajete", "dobo", "hafe"],
         nl="Ga zitten («danwajēte moet stoel beteekenen»)", es="siéntate («danwajēte debe de significar silla», dice el autor)",
         kw=["sentar", "silla", "asiento", "banco"],
         lengua="indeterminada", escala="C",
         veredicto="nueva-como-lectura: resuelve una forma que Gatschet dejaba irreconstruible",
         propuesta="No entra al lexicón. Resuelve «aba dobo edan guayete», que lexicon_gatschet registra «para que un tercer testimonio la resuelva» (los dos OCR rotos en el mismo punto): la fuente primaria imprime «hafe dōbo danwajēte» y segmenta distinto. Ojo: no es un testimonio INDEPENDIENTE (ver `independencia`), es el original. La glosa 'silla' es una inferencia del propio autor («moet … beteekenen»), no una traducción del informante."),
    dict(id="vk-aru-04", gatschet='kantie baulete', forma="Cautje baulēte", formas=["cautje baulete", "baulete"],
         nl="Geef mij te eten", es="dame de comer", kw=["comer", "comida"],
         lengua="indeterminada", escala="C", veredicto="confirma-lectura (Gatschet «kantie baulete»: n por u)",
         propuesta="No entra al lexicón. Corrige la lectura de Gatschet: «kantie» es «Cautje» (confusión n/u de copista; ver `independencia.confusiones_n_u`)."),
    dict(id="vk-aru-05", gatschet='datie', forma="dat jē", formas=["dat je", "datje"],
         nl="Ga weg", es="¡vete!", kw=["irse", "ir"],
         lengua="indeterminada", escala="C", veredicto="confirma-lectura (Gatschet «datie»)",
         propuesta="No entra al lexicón. Dos palabras en la fuente primaria («dat jē»), una en Gatschet («datie»). Homógrafa del neerlandés «dat je» ('que tú'): el autor la da por indígena, y reaparece dentro de la fórmula «para asustar niños» de Pinart; se registra la homografía para que nadie la use como dato de filiación."),
    dict(id="vk-aru-06", gatschet=None, forma="mimānta", formas=["mimanta"],
         nl="Ik ben verschrokken", es="me asusté, estoy asustado", kw=["miedo", "susto", "asust", "espant"],
         lengua="indeterminada", escala="C", veredicto="nueva",
         propuesta="No entra al lexicón: sólo la da van Koolwijk, sin cognado medido. Registrada para que una segunda fuente la pueda subir."),
    dict(id="vk-aru-07", gatschet='karebe', forma="carēbe", formas=["carebe"],
         nl="Een eetlepel", es="una cuchara (de comer)", kw=["cuchara", "cucharón"],
         lengua="caquetío (por el lexicón)", escala="A",
         veredicto="confirma-atestiguada (karebe) — pero es la MISMA cadena que Gatschet, no una tercera atestación",
         propuesta="karebe ya es caquetío-atestiguado con DOS atestaciones independientes: Aruba (Gatschet 1885) y Paraguaná (Medina Colina 2013 p. 64). Van Koolwijk no suma una tercera: es la FUENTE PRIMARIA del lado arubano (fechada el 20-XI-1881, antes de la visita de Pinart). Propuesta: añadir a `notas` que la atestación arubana es van Koolwijk 1882 p. 227 «carēbe 'eetlepel'» y que Gatschet 1885 repite esa cadena. No cambia ni glosa ni capa."),
    dict(id="vk-aru-08", gatschet='totumba · waidanga', forma="totoēmba of waidānga", formas=["totoemba", "waidanga"],
         nl="Een calbas om uit te eten", es="una totuma (tapara) para comer", kw=["totuma", "tapara", "taparo", "calabaza", "totumo", "jícara"],
         lengua="totoēmba: castellano/caribe (totuma); waidānga: indeterminada", escala="totoēmba D · waidānga C",
         veredicto="confirma-lectura (Gatschet «totumba, waidanga water-gourd»)",
         propuesta="No entra al lexicón. totoēmba es la «totuma» del castellano general (Gatschet minado ya la descartó, D). waidānga: misma forma que Gatschet y que de Goeje 1939 p. 15 (que la toma de Gatschet; 6-fusion/kalinago_goeje_1939.yaml §aruba). Con van Koolwijk la cadena es una sola: van Koolwijk → Pinart/Gatschet → de Goeje. Glosa de la fuente primaria: 'para comer', no 'water-gourd'."),
    dict(id="vk-aru-09", gatschet='danshikki · danshebu', forma="daūchikki of dousēbou", formas=["dauchikki", "dousebou"],
         nl="Een zak", es="un saco, una bolsa", kw=["saco", "bolsa", "mochila", "morral"],
         lengua="indeterminada", escala="C", veredicto="confirma-lectura (Gatschet «danshikki, danshebu»: n por u)",
         propuesta="No entra al lexicón. Corrige a Gatschet: «dan-» es «daū-» (n/u) y la segunda forma es «dousēbou», no «danshebu»."),
    dict(id="vk-aru-10", gatschet=None, forma="bouserānja", formas=["bouseranja"],
         nl="Huismeubelen", es="los enseres de la casa", kw=["enseres", "mueble", "utensilio", "trastos"],
         lengua="indeterminada", escala="C", veredicto="nueva",
         propuesta="No entra al lexicón: sólo van Koolwijk."),
    dict(id="vk-aru-11", gatschet='kanla', forma="caula", formas=["caula"],
         nl="Een ding", es="una cosa", kw=["cosa", "objeto"],
         lengua="indeterminada", escala="C", veredicto="confirma-lectura (resuelve el «kanla (?kaula)» de Gatschet)",
         propuesta="No entra al lexicón (abstracto genérico). Resuelve la duda que el propio Gatschet imprimió: es «caula», con u."),
    dict(id="vk-aru-12", gatschet='adamudu', forma="adamōedoe", formas=["adamoedoe"],
         nl="Regen", es="lluvia", kw=["lluvia", "llover"],
         lengua="indeterminada", escala="C", veredicto="confirma-lectura (Gatschet «adamudu»)",
         propuesta="No entra al lexicón: misma voz que Gatschet, misma cadena; sin cognado medido (ver `cruce.lexicon_por_glosa`)."),
    dict(id="vk-aru-13", gatschet='baru xantu uou', forma="bāroe hāntoe wōu", formas=["baroe hantoe wou"],
         nl="Gebed na het eten", es="oración (rezo) después de comer", kw=["oración", "rezo", "rezar"],
         lengua="indeterminada", escala="C",
         veredicto="conflicto-de-glosa con Gatschet («to ask for something to eat»)",
         propuesta="No entra al lexicón. Resuelve la última palabra que los OCR de Gatschet daban «uou»/«uqu»: es «wōu». Y declara un CONFLICTO DE GLOSA: la fuente primaria dice 'oración después de comer', Gatschet 'pedir algo de comer'. Se registran las dos; no se elige (campana-toponimos §4, regla de Supí, aplicada a una voz)."),
    dict(id="vk-aru-14", gatschet=None, forma="kajappa", formas=["kajappa"],
         nl="Arbeiders om te planten", es="trabajadores para sembrar (la cuadrilla de siembra)", kw=["sembrar", "siembra", "faena", "trabajo"],
         lengua="indeterminada", escala="C", veredicto="nueva",
         propuesta="No entra al lexicón: sólo van Koolwijk. Es la única voz de la lista del campo de la siembra (trabajo colectivo): candidata a corpus (transmisión / trabajo) si otra fuente la recoge."),
    dict(id="vk-aru-15", gatschet=None, forma="marākka", formas=["marakka"],
         nl="Een calbas met steenen om te ratelen", es="maraca (tapara con piedras para sonar)", kw=["maraca", "sonaja"],
         lengua="taíno / panantillana (la voz que el castellano difundió)", escala="D",
         veredicto="comparanda-de-la-esfera (no es dato caquetío)",
         propuesta="No entra como caquetío. La voz no está en el lexicón en ninguna capa (por glosa sólo sale la wayuu isira 'maraca'), y Oliver 1989 cap. 2 (6-fusion/taino_en_la_esfera_2026-09-21.yaml) ya advierte que «maraca» llegó probablemente con los españoles desde La Española. Reaparece en la nota 1 de la p. 224 («het ratelen der marakka»). Si alguna vez se quiere como voz de la esfera, es decisión aparte (FORMA_DE_LA_ESFERA)."),
    dict(id="vk-aru-16", gatschet=None, forma="aboūssoe", formas=["aboussoe"],
         nl="Een maïskoek", es="una torta (arepa) de maíz", kw=["maíz", "arepa", "torta", "bollo"],
         lengua="indeterminada", escala="C", veredicto="nueva",
         propuesta="No entra al lexicón: sólo van Koolwijk. Candidata a corpus (alimentos) con la etiqueta retro-abstraido si otra fuente la recoge; el maíz en Aruba está atestiguado arqueológicamente, la palabra no."),
    dict(id="vk-aru-17", gatschet=None, forma="pekinini", formas=["pekinini"],
         nl="Een kind", es="un niño", kw=["niño", "criatura", "hijo"],
         lengua="criollo (portugués «pequenino»; cf. el «pikin» del neger-engels que el autor conocía de Surinam)", escala="D",
         veredicto="criollo — descartada",
         propuesta="Descartada como indígena: es criollo. Se registra el descarte para que nadie la re-descubra (protocolo §5)."),
]

# Plantas y animales: p. 227 (pdf 9), col. derecha. Sin glosa individual en
# las plantas: el autor sólo dice «nombres indios de árboles y plantas».
PLANTAS_Y_ANIMALES = [
    dict(id="vk-aru-18", gatschet='dabaraida', forma="Dabaroīda", formas=["dabaroida"], nl="(boomen en planten)", es="(árbol o planta; sin glosa individual)",
         kw=[], lengua="indeterminada (voz viva en papiamento: dabaruida)", escala="A según Gatschet minado",
         veredicto="confirma-lectura — y desmiente la «TRIPLE atestación independiente» de lexicon_gatschet",
         propuesta="lexicon_gatschet.py da a dabaraida «TRIPLE atestación independiente: van Koolwijk 1880, Pinart 1882, van Buurt 2014». Medido: van Koolwijk y Pinart/Gatschet son UNA cadena (ver `independencia`), y van Buurt cita a van Koolwijk vía Hartog 1953 y a Pinart. Lo que queda es una cadena histórica (1881-82) más la forma viva del papiamento (van Buurt §6). Va en el issue."),
    dict(id="vk-aru-19", gatschet='hubada', forma="Hoebădā", formas=["hoebada"], nl="(boomen en planten)", es="(árbol o planta; sin glosa individual)",
         kw=[], lengua="indeterminada (voz viva: hubada, Acacia tortuosa, van Buurt §6)", escala="A según Gatschet minado",
         veredicto="confirma-lectura (Gatschet «hubada»)", propuesta="Sin cambio de nivel: misma cadena que Gatschet; lo que la sostiene es la forma viva de van Buurt."),
    dict(id="vk-aru-20", gatschet='tarabada', forma="Tarabada", formas=["tarabada"], nl="(boomen en planten)", es="(árbol o planta; sin glosa individual)",
         kw=[], lengua="indeterminada", escala="C",
         veredicto="resuelve una duda de Gatschet: es un nombre de planta propio",
         propuesta="lexicon_gatschet registra «hubada tarabada» y sospecha que tarabada sea «un epíteto o un error de campo de Pinart». La fuente primaria la da como planta SEPARADA, entre comas, en una lista de cinco. Duda resuelta: es un nombre propio de planta (sin identificar). Distinto del cerro Tarabana."),
    dict(id="vk-aru-21", gatschet=None, forma="Takkitākki", formas=["takkitakki"], nl="(boomen en planten)", es="(árbol o planta; sin glosa individual)",
         kw=[], lengua="indeterminada", escala="C", veredicto="nueva (no está en Gatschet)",
         propuesta="No entra al lexicón: sólo van Koolwijk, sin identificar. Reduplicada, como lokkilokki: anotar en la serie de reduplicación (lexicon_toponimos.REDUPLICACION) si se reabre."),
    dict(id="vk-aru-22", gatschet='lokiloki', forma="Lokkilōkki", formas=["lokkilokki"], nl="(boomen en planten)", es="(árbol o planta; sin glosa individual)",
         kw=[], lengua="indeterminada", escala="C", veredicto="confirma-lectura (Gatschet «lokiloki», Mimosa unguiscata)",
         propuesta="Misma cadena que Gatschet; sin cambio."),
    dict(id="vk-aru-23", gatschet='dori', forma="Dori", formas=["dori"], nl="Kikvorsch (y nota 1 de la p. 224: «inl. benaming: dori»)", es="rana",
         kw=["rana", "sapo"], lengua="voz del papiamento arubano (van Buurt §6: nace en Aruba, onomatopeya)", escala="A según Gatschet minado",
         veredicto="confirma-lectura (Gatschet «dori»)",
         propuesta="Misma cadena que Gatschet. Lo que la fuente añade es el contexto: la rana sólo vive en Aruba (no en Curazao ni Bonaire, en 1881) y es el motivo de las vasijas (ver `mundo`). La anotación más antigua de la palabra es ésta (1881)."),
    dict(id="vk-aru-24", gatschet='waltaka', forma="Waltakka", formas=["waltakka"], nl="Hagedis", es="lagartija",
         kw=["lagartija", "lagarto"], lengua="voz del papiamento arubano (van Buurt: waltaca, Anolis lineatus, sólo en Aruba)", escala="A según Gatschet minado",
         veredicto="confirma-lectura (Gatschet «waltaka»)", propuesta="Misma cadena que Gatschet; sin cambio."),
]

CONJURA = dict(
    id="vk-aru-25", pagina=227, pdf=9,
    forma="sako den comanari marīa di watapōena fafa na douére sodji na ditiéri",
    nl="Eene bezwering, bij het vangen van de leguana in gebruik",
    es="un conjuro que se usa al cazar la iguana",
    lengua="mixta: papiamento («den», «di», «na») con voces sin traducir",
    escala="R (fórmula ritual: no léxico)",
    veredicto="confirma-lectura (Gatschet «Sako den komanari manadi watapuna fafa na douere sadii na ditieri»)",
    propuesta=("No es léxico. La fuente primaria segmenta «marīa di watapōena» —en papiamento, «María "
               "de [el] watapana»— donde Gatschet imprime «manadi watapuna». Con eso «watapuna» no es una "
               "voz suelta: es «watapōena», el árbol watapana en grafía neerlandesa (oe = u). Va al corpus "
               "(creencia) como fórmula de caza, retro-abstraido, época moderna; nunca al habla."),
)

# ── 1b. Los topónimos: p. 227 (pdf 9), col. izquierda ──
# El orden es el de la fuente. «Wari-roēri», «Han-debirāri», «Hen-djēkoe» y
# «Barba-kw̄a» van partidos a fin de línea; se juntan.
TOP_LUGARES = ["Bedōēi", "Damāri", "Antikōeri", "Kamakōeri", "Webōeri", "Boebāri", "Wariroēri",
               "Arikoērāri", "Arāsje", "Joudīti", "Casjoēnti", "Causjāti", "Hendjēkoe", "Lacōn",
               "Jāra", "Cassibāri", "Boechiseribāni"]
TOP_CERROS = ["Behīca", "Handebirāri", "Oeratakka", "Jaboeroebāri", "Jamanōta", "Codecodēctoe",
              "Chirabāna", "Ajō", "Chaboerōoeri", "Cassiwāri", "Matibidīroe", "Parabostē", "Joediti",
              "Tarabana", "Boekoerōi", "Hendjēkoe", "Barbakw̄a", "Wakoebāna", "Kibāima", "Jāra"]
TOP_GRUTAS = ["Wareroekōeri", "Matibidiroe", "Waririkīri"]

# Lecturas y propuestas por nombre (lo que no se calcula). `nivel` propuesto con
# la escala de campana-toponimos §4; sin glosa de fuente no se pasa de C.
NOTAS_TOPONIMO = {
    "Chirabāna": dict(nivel="C", propuesta="Cierra la MITAD de la ecuación: -bana 'cerro, sitio alto' (D9) sobre un nombre que la fuente lista entre los CERROS. La raíz chira- no tiene glosa. Sitio con arte rupestre (Wagenaar Hummelinck 1962, «Siribana», A 24-26)."),
    "Tarabana": dict(nivel="C", propuesta="Ídem: -bana sobre un cerro; tara- sin glosa. No confundir con la planta Tarabada de la misma página."),
    "Wakoebāna": dict(nivel="C", propuesta="-bana sobre un cerro. Dos lecturas de la raíz, sin elegir: waka 'subterráneo' (van Buurt §6 vía Oliver; es la que usa toponimo-005 guacaubana, que ya cita a Wakubana como recurrencia insular) y waka 'ave, cotorra' (lexicón, caquetío-atestiguado). Van Koolwijk lo pone entre los CERROS, no entre las grutas. Atestaciones de la forma: mapa de 1825 «Wacobana» (vía van Buurt), van Koolwijk 1881 «Wakoebāna», Gatschet 1885 «Wakubana» — las dos últimas, una cadena."),
    "Kibāima": dict(nivel="C", propuesta="Hipótesis del proyecto, con las dos piezas ya atestiguadas por otras fuentes: kiba 'piedra' (lexicón, caquetío-atestiguado) + -aima 'abundancia' (REGLAS_ZAVALA, Zavala #6) = 'el pedregal, donde abunda la piedra', y la fuente lo lista entre los CERROS. Sin glosa de fuente no sube de C: lo subiría una fuente que lo glose. Va como `lecturas` tipo hipotesis, quien: proyecto."),
    "Cassibāri": dict(nivel="C (sin cambio)", propuesta="Ya en el canon (toponimo-026, C, sin procedencia). Van Koolwijk da la atestación impresa más antigua del NOMBRE (1881, como lugar). Propuesta, con el precedente de Paraguaná (T2b): procedencia para la FORMA, no para la glosa 'hay rocas duras', que sigue siendo de van Buurt §8."),
    "Cassiwāri": dict(nivel="descartado", propuesta="Cerro. Corrige el «Kasiaari»/«Kasinari» del OCR de Gatschet (la mesa lo cruzaba con «Kadiwari (?)»). Distinto en la fuente de Cassibāri (lugar): b~w es permutación declarada, pero el autor los pone en listas distintas y no se funden."),
    "Matibidīroe": dict(nivel="descartado (sin cambio)", propuesta="Ya en el canon (toponimo-069, descartado, sin procedencia). Dos aportes: (1) procedencia de la forma, van Koolwijk 1881, como cerro y como gruta; (2) la terminación de la fuente primaria, -roe (= -ru), está más cerca del Matividiro de Paraguaná (toponimo-275, Esteves p. 51: «cerro de menos de 250 m y aldea») que el -ri de Gatschet. Un nombre de cerro a los dos lados del mar: dato para la esfera, no glosa."),
    "Matibidiroe": dict(nivel="descartado (sin cambio)", propuesta="La gruta del mismo nombre que el cerro (toponimo-069)."),
    "Arāsje": dict(nivel="descartado (sin cambio)", propuesta="Ya en el canon como Arashi (descartado, sin procedencia). Procedencia de la forma: van Koolwijk 1881. La hipótesis de van Buurt §8 (arashi ~ warashi 'macabí') sigue siendo de van Buurt. Formante -shi (morfema-007, sin glosa)."),
    "Boebāri": dict(nivel="descartado", propuesta="Corrige el «Cubari» de Gatschet (OCR: B leída C). Es Bubali, nombre vivo en Aruba (van Buurt §7). Afecta a morfemas.yaml: «Cubari» figura como ejemplo de -ari (morfema-008) y -bari (morfema-010). Va en el issue."),
    "Boekoerōi": dict(nivel="descartado", propuesta="Corrige el «Cukuroi» de Gatschet (la mesa lo cruzaba con Kukurui). Es «Boegoeroei, Bucurui (Sero)» de van Buurt. El parecido con Bucuruy (Paraguaná, toponimo de Esteves p. 24) es SÓLO de forma y Esteves da aquel por castellano (de «buco»): no cuenta."),
    "Barbakw̄a": dict(nivel="descartado", propuesta="Es el Barbacoa que morfemas.yaml cita como apoyo insular sin glosa de -bacoa (morfema-001); van Koolwijk da la forma más antigua (1881). Dos lecturas en pugna y ninguna cierra: bar- + -bakoa 'arboleda', o la voz «barbacoa» entera, que Oliver 1989 cap. 2 avisa que los españoles difundieron como «nativa». El macrón cae sobre la w."),
    "Boechiseribāni": dict(nivel="descartado", propuesta="Es la Bushiribana viva (van Buurt §7; Gatschet «Bushiribani (?)»). La fuente primaria tiene una sílaba más (bu-chi-se-ri-bani) y termina en -bāni; es un LUGAR, no un cerro."),
    "Waririkīri": dict(nivel="descartado", propuesta="Gruta. Es la cueva de Guadirikiri/«Quadirikiri» (van Buurt §7; Wagenaar Hummelinck 1962, A 28, con arte rupestre)."),
    "Oeratakka": dict(nivel="descartado", propuesta="Cerro que no está en Gatschet. Es «Urataka (Sero)» de van Buurt §7."),
    "Parabostē": dict(nivel="descartado", propuesta="Cerro que no está ni en Gatschet ni en van Buurt: sólo esta fuente."),
    "Joediti": dict(nivel="descartado", propuesta="Cerro; el lugar de la misma lista se escribe Joudīti. Gatschet sólo trae el lugar (Yuditi). Cerro que no está en Gatschet."),
    "Lacōn": dict(nivel="descartado", propuesta="Lugar que no está ni en Gatschet ni en van Buurt: sólo esta fuente. Podría no ser indígena; sin más datos no se decide."),
    "Jāra": dict(nivel="descartado", propuesta="Lugar y cerro a la vez en la fuente. No está en Gatschet; es «Yara» de van Buurt §7."),
    "Hendjēkoe": dict(nivel="descartado", propuesta="Lugar y cerro a la vez. Gatschet sólo trae el lugar (Hendieku)."),
    "Ajō": dict(nivel="descartado", propuesta="Ayo, la formación de bloques de diorita con pinturas (Wagenaar Hummelinck 1953, «Ajó», A 2). La coincidencia con hayo (toponimo-205, Paraguaná) es SÓLO de forma —allí es un árbol, según Esteves—: no cuenta."),
    "Chaboerōoeri": dict(nivel="descartado", propuesta="Shabururi, sitio con arte rupestre (Wagenaar Hummelinck 1962, A 22-23)."),
    "Jamanōta": dict(nivel="descartado", propuesta="Yamanota, nombre vivo del cerro (van Buurt §7, «Yamanota (Sero)»)."),
    "Codecodēctoe": dict(nivel="descartado", propuesta="Reduplicado (kode-kode-), como señala Gatschet de varios nombres arubanos; van Buurt «Kodekodectu»."),
}

# Topónimos que salen en la PROSA (pp. 222-226). Sólo se anotan: clase, página
# y lo que el texto dice del sitio.
TOP_EN_PROSA = [
    dict(forma="Parawana", pagina=222, pdf=4, clase="indígena (Paraguaná)",
         texto="«De nabijheid van de vaste kust van Venezuela (van Parawana) op vijf geographische mijlen afstand van Aruba…»; y «aan de noordzijde van Aruba ter plaatse Parawana geheeten, een opschrift, waarop een luiaard … schijnt afgebeeld»",
         propuesta="DOS referentes con el mismo nombre en 1881: la península y un lugar del norte de Aruba. Para toponimo-018 (paraguaná): una `lecturas`/`observacion` con la forma «Parawana» (grafía neerlandesa) y la noticia de su homónimo arubano, que es el sitio «Paraguana» (A 30) de Wagenaar Hummelinck 1962. No toca la glosa (#109)."),
    dict(forma="Fontein", pagina=226, pdf=8, clase="neerlandés (la fuente de agua dulce que nace en la gruta)",
         texto="gruta en caliza, entrada alta y abovedada, galerías; «indiaansche opschriften zijn er talrijk aanwezig»; de una galería «vloeit nog heden eene verfrisschende bron van zoet water, waaraan zij in latere tijden den naam Fontein ontleend heeft»",
         propuesta="No es topónimo indígena. Va al catálogo de petroglifos (sitio con pinturas) y a `mundo` (agua dulce)."),
    dict(forma="Carachito", pagina=226, pdf=8, clase="indeterminada (¿castellano?)",
         texto="cerro al sur del Hooiberg, con cuatro grutas; una con huesos de ocho a diez personas y la tradición de la matanza (ver `mundo`)",
         propuesta="Probablemente el actual Seroe Canashito (al sur del Hooiberg, con dos grutas en caliza y pinturas: Wagenaar Hummelinck 1953 A 4-5). Identificación del minador, sin verificar: va como hipótesis."),
    dict(forma="Seroe die Casjoe", pagina=223, pdf=5, clase="papiamento ('cerro del merey')",
         texto="«Vergelijk indiaansch opschrift van den berg Seroe die Casjoe op Aruba»", propuesta="No es indígena. Sitio con inscripción (para el catálogo)."),
    dict(forma="Tunnel (berg)", pagina=223, pdf=5, clase="indeterminada",
         texto="«Op den berg Tunnel (zoo genaamd volgens de traditie naar een indiaansch opperhoofd) hebben de Indianen eene roode verfaarde opgedolven»",
         propuesta="Tradición: el cerro lleva el nombre de un jefe indio. Dato para antroponimos_caquetios.yaml (retro-abstraido, tradición oral de 1881), no para el canon de topónimos."),
    dict(forma="Santa Cruz (Santa Croes)", pagina=223, pdf=5, clase="castellano (papiamento entre paréntesis)",
         texto="campamento indio al SE del Hooiberg; tiestos pintados, conchas de Strombus, urnas", propuesta="No es indígena. Sitio arqueológico (ver `mundo` y `lamina`)."),
    dict(forma="Savonet", pagina=225, pdf=7, clase="indeterminada (es la Savaneta de hoy; Gatschet «Saboneta»)",
         texto="campamento junto a la Commandeursbaai, en una altura; entierros en vasijas «tot in het begin dezer eeuw»", propuesta="No es indígena. Sitio arqueológico."),
    dict(forma="Hooiberg", pagina=223, pdf=5, clase="neerlandés", texto="«eenen der voornaamste bergen van Aruba»", propuesta="Referencia geográfica."),
    dict(forma="Commandeursbaai", pagina=225, pdf=7, clase="neerlandés", texto="primer desembarcadero y residencia de los comandantes", propuesta="Referencia geográfica."),
    dict(forma="Oranjestad", pagina=223, pdf=5, clase="neerlandés", texto="cerca hay tierra blanca para pintar", propuesta="Referencia geográfica."),
    dict(forma="orua / oruba", pagina=222, pdf=4, clase="nombre de la isla",
         texto="nota 1: «In Spaansche handschriften van het midden der vorige eeuw: orua en oruba»",
         propuesta="Para toponimo-051 (aruba → 'Oruba. Oruma. Oirubae', descartado): añadir «orua» y «oruba» como formas que el autor dice leer en manuscritos españoles de mediados del s. XVIII. No sube el nivel (no es una glosa)."),
]

# ── 1c. El kari'ña de Surinam (1870): pp. 227-229 ──
# (nl, forma, es). «(neger-engelsch)» y «(spaansch)» son marcas del autor.
CARIBE_SURINAM = [
    # p. 227, col. derecha
    (227, "ik", "au", "yo"), (227, "gij", "amōre", "tú"), (227, "hij", "mosē", "él"),
    (227, "wij", "ana", "nosotros"), (227, "gij (pl.)", "kēko", "vosotros"), (227, "zij", "kīko", "ellos"),
    (227, "God", "tamōesi", "Dios"), (227, "een mensch", "kālīnān", "una persona"),
    (227, "een goed mensch", "ōeme mānā", "una persona buena"), (227, "een slecht mensch", "torokēne mānā", "una persona mala"),
    (227, "een oud mensch", "tanpōko", "un viejo"), (227, "eene oude vrouw", "nonpōko", "una vieja"),
    (227, "een Indiaan", "kālīnan", "un indio"), (227, "een Blanke", "planakīri", "un blanco"),
    (227, "een Zwarte", "mēkōllo", "un negro"), (227, "een opperhoofd", "wāpātōre", "un jefe"),
    (227, "een dokter", "poejé, poejāsi, piaīman", "un curandero, un chamán"), (227, "eene dienstmaagd", "emeāle", "una criada"),
    (227, "de vader", "pāpa, joēmo", "el padre"), (227, "de moeder", "tāta, husāna", "la madre"),
    (227, "de grootmoeder", "pīpi", "la abuela"), (227, "de broeder", "sērvo", "el hermano"),
    (227, "de zuster (de jongste)", "m[ī]a", "la hermana menor"), (227, "de vrouw", "wāwa", "la mujer, la esposa"),
    (227, "het kind", "kīen", "el niño"),
    # p. 228, col. izquierda
    (228, "een klein kind", "pīto", "un niño pequeño"), (228, "de ziel", "akălī", "el alma"),
    (228, "het lichaam", "jāmoe", "el cuerpo"), (228, "het hoofd", "joupōpe", "la cabeza"),
    (228, "het hoofdhaar", "jousētte", "el cabello"), (228, "de oogen", "ennōere", "los ojos"),
    (228, "de neus", "mōre", "la nariz"), (228, "de mond", "potāri", "la boca"),
    (228, "de ooren", "panāri", "las orejas"), (228, "de arm", "apōli", "el brazo"),
    (228, "de handen", "jajāri", "las manos"), (228, "de voeten", "papōroe", "los pies"),
    (228, "de kuiten", "sēida", "las pantorrillas"), (228, "de buik", "joewēmbo", "el vientre"),
    (228, "de borst", "manāta", "el pecho"), (228, "het kind de borst geven", "mana teke kepāko", "dar el pecho al niño"),
    (228, "het kamp", "pataīaa", "el campamento"), (228, "het huis", "hāfto", "la casa"),
    (228, "ik ga naar huis", "hāfto a mī sa", "voy a casa"), (228, "eene bank", "moelē", "un banco"),
    (228, "een stoel", "stoeloe (neger-engelsch)", "una silla"), (228, "eene tafel", "tafla (neger-engelsch)", "una mesa"),
    (228, "eene vork", "sakka", "un tenedor"), (228, "een mes", "mārīā", "un cuchillo"),
    (228, "een houwer", "soubārā", "un machete"), (228, "een geweer", "arakka poūssa", "un fusil"),
    (228, "een pijl", "prīwa", "una flecha"), (228, "een kalebas", "kwāi", "una totuma, una calabaza"),
    (228, "vuur", "wāto", "fuego"), (228, "water", "tōna", "agua"),
    (228, "eene plaat voor cassave te bakken", "alīn jătoe", "el budare (plancha para cocer el casabe)"),
    (228, "eene groote waterkan", "toēkoēwāri", "una tinaja grande"),
    (228, "hout", "wēwĕ", "leña, madera"), (228, "asch", "weroēno", "ceniza"),
    (228, "vleesch", "tjāko", "carne"), (228, "spek", "tenōme", "tocino, grasa"),
    (228, "bakkeljaauw", "ăkĭtī", "bacalao"), (228, "visch", "wāto", "pescado"),
    (228, "eene krab", "koūssa", "un cangrejo"), (228, "cassave", "arēpa", "casabe"),
    (228, "bananne", "păroēre", "plátano"), (228, "ananas", "nānā", "piña"),
    (228, "papaia", "kapaīa", "papaya"), (228, "een vogel", "krotōkko", "un pájaro"),
    (228, "eene eend", "opōno", "un pato"), (228, "eene slang", "ŏkŏjōe", "una serpiente"),
    (228, "een varken", "porkoe (spaansch)", "un cerdo"),
    # p. 228, col. derecha
    (228, "een hond", "pēroe (spaansch)", "un perro"), (228, "geld", "plāta (spaansch)", "dinero"),
    (228, "een tijger", "katoēsi", "un jaguar («tigre»)"), (228, "een kleine aap", "karapāne", "un mono pequeño"),
    (228, "muskieten", "siwilīri", "mosquitos"), (228, "eene vlieg", "wēre wēre", "una mosca"),
    (228, "een wortel ook pees", "mīti", "una raíz; también tendón"), (228, "roode verf", "koēsŏwē", "pintura roja"),
    (228, "zwarte verf", "tapoērīpo", "pintura negra"), (228, "cassave drank", "rookoe topāne", "bebida de yuca"),
    (228, "roode drank", "casīri", "bebida roja (cachirí)"), (228, "zwarte drank", "pajouwāroe", "bebida negra (payahuarú)"),
    (228, "de hemel", "kāpōu", "el cielo"), (228, "de zon", "wĕjōu", "el sol"),
    (228, "de maan", "nōuno", "la luna"), (228, "de sterren", "serīko", "las estrellas"),
    (228, "het onweer", "knomēro mōli", "la tormenta"), (228, "de aardbeving", "tetēite", "el terremoto"),
    (228, "de zee", "plāna", "el mar"), (228, "de rivier", "rōne", "el río"),
    (228, "de grond", "nōno", "la tierra, el suelo"), (228, "het bosch", "ītĕrōen", "el bosque"),
    (228, "een moeras", "tjāpo", "un pantano"), (228, "zeebanken", "pōtrī", "bancos de arena del mar"),
    (228, "de regen", "knōpo", "la lluvia"), (228, "het regent", "kōnōpōnŏmē of knossa", "llueve"),
    (228, "stelen", "mānāmŏmāna", "robar"), (228, "een dief", "mŏnŏmān", "un ladrón"),
    (228, "iemand die altijd steelt", "monameneman", "el que siempre roba"), (228, "liefhebben, willen", "sĕwā", "amar, querer"),
    (228, "ik wil", "sēwā", "yo quiero"), (228, "zingen", "walé", "cantar"),
    (228, "dansen", "dĭărōko", "bailar"), (228, "een ander slaan", "iwōmāko", "pegarle a otro"),
    (228, "iemand vermoorden", "ĭwĭāko", "matar a alguien"), (228, "slapen", "onĕkō", "dormir"),
    (228, "eten", "enāko", "comer"), (228, "vechten", "kawāi", "pelear"),
    (228, "schieten", "īpīŏkōkō", "disparar"), (228, "hooren", "panāritan", "oír"),
    (228, "schudden", "tĕkōtē kano", "sacudir"), (228, "boomen vellen", "kūto", "tumbar árboles"),
    (228, "kapt hem", "kutōko", "¡córtalo!"), (228, "zal ik hem kappen", "ams kētokan", "¿lo corto?"),
    (228, "ik ben", "manda", "yo soy, yo estoy"), (228, "gij zijt", "mandŏman", "tú eres"),
    (228, "wij zijn", "mandonāne", "nosotros somos"), (228, "ik heb honger", "kamōra", "tengo hambre"),
    # p. 229, col. izquierda
    (229, "het is goed", "doēpā", "está bien"), (229, "God is goed", "tamōesi pāpōlĭman", "Dios es bueno"),
    (229, "wij zijn zeer goed", "ana joe pāpōlĭman", "somos muy buenos"), (229, "Ik ben een kind van God", "oŭtē tamōesi mepōli", "soy hijo de Dios"),
    (229, "de zonde, het kwaad", "tālĭkī", "el pecado, el mal"), (229, "waar zijt gij?", "koempoua?", "¿dónde estás?"),
    (229, "ik zal u laten zien", "konē takirāpa", "te lo mostraré"), (229, "hij is ziek", "jētōmme", "está enfermo"),
    (229, "waarom?", "ōtonōme", "¿por qué?"), (229, "daarenboven", "koeponāka", "además"),
    (229, "het is vloed", "itjoumāi", "hay marea alta"), (229, "het is ebbe", "tāpa", "hay marea baja"),
    (229, "het water is gevallen", "eronēma tapāna", "el agua bajó"), (229, "van daag", "ĕrōme", "hoy"),
    (229, "morgen", "kolōppe", "mañana"), (229, "overmorgen", "mōnĭngrōpo", "pasado mañana"),
    (229, "Ja", "hahā", "sí"), (229, "neen", "owā", "no"),
    (229, "ik weet het niet", "hŏhō", "no sé"), (229, "wat wilt gij?", "ōtse kŏmān", "¿qué quieres?"),
    (229, "kom hier", "okonēto", "¡ven acá!"),
]
# Lectura de las coincidencias de forma y glosa que el script encuentra (se
# leen una a una: minar-fuente §2). Clave = forma_fuente.
LECTURA_COINCIDENCIAS_SURINAM = {
    "tōna": "real: tuna 'agua' es voz caribe y taína a la vez (préstamo o areal antiguo); NO dice nada de Aruba, porque tōna no es arubana",
    "casīri": "real: kasiri/cachirí, voz areal de la bebida de yuca (lokono, caribe)",
    "poejé, poejāsi, piaīman": "real: el «piache» areal (lokono piayeman)",
    "nānā": "real: nana 'piña', voz areal (achagua nanana)",
    "plāta (spaansch)": "real pero castellana: el autor la marca «spaansch», y el lokono platta es el mismo préstamo",
    "wāwa": "ruido: nagua 'falda' no es 'mujer'",
    "wāto": "ruido: siwato 'desganado' no es 'pescado' (y wāto 'pescado' es probable errata)",
    "pēroe (spaansch)": "ruido: es el castellano «perro» (marca del autor); el wayuu erü es otra voz",
}
DUDAS_SURINAM = {
    "m[ī]a": "el tipo de la i está roto (pdf 9, recorte a 14×): se lee m-macrón-a; la i es conjetura",
    "wāto": "«visch» se imprime wāto, IGUAL que «vuur»: probable errata del impresor (en kari'ña el pez es otra palabra); se copia como está",
    "kīko": "la k y la i van separadas por un blanco en la impresión («k īko»)",
}

PADRENUESTRO = ("Ana Pāpa kapoutānĕ, ajēte kōlŏ santo nānjĕ; a kon de leri kōlō nonĕ, o se nōle kōlō nēnjĕ "
                "nōnŏ, koēpo kāpoe tāno wāl, ĕlāpo eroēpa nānje āna, ĕlĕpāli īkō ĕrŏmē, āna wa pārdōn īkŏ "
                "ērŏ wālă erăpā; āna tāsa kāli wa kēnītān; ŏlīkoē wīnjī nānā ĕmīmāko ōlīkoē wīnjŏ. Hēpŏlōme.")
MANDAMIENTOS = [
    "Piēnjatākoe Tamōesie papolōto kontyōppo amkōlo ĕrŏpătōne.",
    "Ĕrŏnōme lōnge Tamoesi kōlo jātotōkko.",
    "(Neger-engelsch) Joe sa meki santa Tamoesi dei.",
    "Pīnja tāko pāpa sana mēratāta.",
    "Tēwo kolo ewanōme kōsi winkōlo.",
    "Jawāssi takōlo.",
    "Monawāi kōlo.",
    "Oūdrŏtēn sjatōkko.",
    "Ămŏlīri pāko te kolākte.",
    "Ham te kōn pāko kolākte.",
]

# ── 1d. La lámina (pdf 12-13), identificada por el TEXTO (pp. 223-224) ──
LAMINA = [
    dict(figs="1, 2", donde_en_la_lamina="pdf 12", pagina_texto=223, que_es="motivo pintado en tiestos: «eene uit rechte lijnen en rechte hoeken gevormde figuur» (greca de líneas rectas y ángulos rectos)", tipo="cerámica pintada"),
    dict(figs="3", donde_en_la_lamina="pdf 12-13 (en el pliegue)", pagina_texto=223, que_es="«eene afbeelding van het klaverblad» (trébol) en tiestos", tipo="cerámica pintada"),
    dict(figs="4", donde_en_la_lamina="pdf 13", pagina_texto=223, que_es="«eene kronkelende lijn» (línea ondulante, el «zigzag») en tiestos", tipo="cerámica pintada"),
    dict(figs="5a, 5b", donde_en_la_lamina="pdf 13", pagina_texto=223, que_es="«eene in zich keerende ronde lijn» (espiral) en tiestos", tipo="cerámica pintada"),
    dict(figs="6", donde_en_la_lamina="pdf 13", pagina_texto=223, que_es="«eene uit driehoeken bestaande randversiering» (cenefa de triángulos) en tiestos", tipo="cerámica pintada"),
    dict(figs="7", donde_en_la_lamina="pdf 12", pagina_texto=223, que_es="«een grieksch kruis» en tiestos", tipo="cerámica pintada"),
    dict(figs="8", donde_en_la_lamina="pdf 12", pagina_texto=223, que_es="«een halve cirkel» (semicírculos concéntricos) en tiestos", tipo="cerámica pintada"),
    dict(figs="9, 10", donde_en_la_lamina="pdf 12 (9) y 13 (10)", pagina_texto=223, que_es="«eene met stippeltjes versierde lijn» (línea con puntos; la 10 es un rombo con punto) en tiestos", tipo="cerámica pintada"),
    dict(figs="11, 12, 13", donde_en_la_lamina="pdf 13", pagina_texto=224, que_es="ranas y cabezas de rana en relieve en las vasijas pintadas: «Somtijds zijn ten onrechte aan de koppen der kikvorschen ooren toegevoegd: Plaat, fig. 11, 12 en 13» (la 11, la rana entera; la 12, la cabeza con orejas que parece de mono; la 13, la cara de «ojos y cejas»)", tipo="cerámica en relieve"),
    dict(figs="14a, 14b, 14c", donde_en_la_lamina="pdf 12", pagina_texto=224, que_es="asas en forma de botones pequeños redondos y largos, rectos y curvos", tipo="cerámica: asas"),
    dict(figs="15a, 15b", donde_en_la_lamina="pdf 12-13 (15a en el pliegue) y 13", pagina_texto=224, que_es="«ronde en vierkante ooren» (asas-oreja redondas y cuadradas)", tipo="cerámica: asas"),
    dict(figs="16", donde_en_la_lamina="pdf 13", pagina_texto=224, que_es="las dos clases de asa juntas", tipo="cerámica: asas"),
    dict(figs="17a-17f", donde_en_la_lamina="pdf 12 (17b, c, d, f) y 13 (17a, e)", pagina_texto=224, que_es="asas puestas arriba, en el borde, en forma de botones, caras, anillos, hojas", tipo="cerámica: asas"),
    dict(figs="18", donde_en_la_lamina="pdf 12", pagina_texto=224, que_es="una segunda asa añadida más abajo", tipo="cerámica: asas"),
    dict(figs="19", donde_en_la_lamina="pdf 13", pagina_texto=224, que_es="pico o vertedera, que «door het volk niet zelden voor indiaansche pijpen zijn gehouden»", tipo="cerámica: pico"),
    dict(figs="20", donde_en_la_lamina="pdf 13", pagina_texto=224, que_es="vasija con un reborde bajo de 2-3 cm sujeto por cabezas de animal en forma de máscara", tipo="cerámica: vasija"),
    dict(figs="21", donde_en_la_lamina="pdf 13", pagina_texto=224, que_es="la forma de la urna funeraria de Santa Cruz (≈ 1 m de alto, borde ondulado), reconstruida de un fondo que el autor vio", tipo="cerámica: urna"),
]

# ── 1e. Lo demás, por esferas (minar-fuente §4) ──
MUNDO = [
    dict(id="vk-mundo-01", esfera="geografía política / esfera de interacción", pagina=222, pdf=4,
         dato="Un arubano que vivió cinco años en «Parawana» (Paraguaná) asegura que desde allí, con tiempo claro, se ven muy bien los cerros principales de Aruba; la costa está a «vijf geographische mijlen».",
         etiqueta="atestiguado (testimonio de 1881)", epoca="moderna",
         propuesta="Para geografía política / esfera-de-interaccion.md: la intervisibilidad Aruba–Paraguaná, dicha por un testigo. Proyectarla al s. XV es reconstruido (la geografía no cambió), y esa proyección la decide quien fusione."),
    dict(id="vk-mundo-02", esfera="geografía política / esfera de interacción", pagina=222, pdf=4,
         dato="El autor deriva a los indios de Aruba de Parawana: por la cercanía, por la intervisibilidad y porque en un lugar del norte de Aruba llamado Parawana hay una inscripción que parece un perezoso, animal de tierra firme y no de la isla.",
         etiqueta="hipotetico (lectura del autor, 1882)", epoca="—",
         propuesta="Es una LECTURA, no un dato: va con su autor. Choca con la lectura de Wagenaar Hummelinck 1962 del mismo sitio («Paraguana», A 30: un pájaro, tortugas o iguanas). No se fusiona como hecho."),
    dict(id="vk-mundo-03", esfera="ecología / subsistencia", pagina=223, pdf=5,
         dato="Según la tradición, los primeros habitantes vivían en parte en grutas y bajo los bloques de granito, cultivaban poco y se dedicaban más a la pesca «en veeteelt»; limpiaban y trabajaban la tierra con un gancho de madera y sembraban al pie de los cerros o entre los bloques, donde se junta el agua.",
         etiqueta="retro-abstraido (tradición oral de 1881)", epoca="colonial/moderna",
         propuesta="Para ecología: la técnica (palo-gancho, siembra donde se junta el agua al pie del cerro) es plausible precontacto y se puede proponer así. La «veeteelt» (ovejas y cabras) es colonial: NO se proyecta (regla 3)."),
    dict(id="vk-mundo-04", esfera="ecología / alimentos", pagina=223, pdf=5,
         dato="En la seca comían mariscos, las semillas del totumo (Crescentia cujete), las hojas de la «Koeki di Indian» (Agave) y los tallos de la «bringa mosa» (Janipha urens).",
         etiqueta="retro-abstraido (tradición oral de 1881)", epoca="colonial/moderna",
         propuesta="Para ecología (alimentos de seca, hambruna). Los taxones son del autor (1882); el nombre actual va aparte, como en la política D7."),
    dict(id="vk-mundo-05", esfera="cultura material / vivienda y vestido", pagina=223, pdf=5,
         dato="Los que no vivían bajo los bloques cubrían sus chozas con cañas de maíz u hojas de cocotero y pieles; las mujeres vestían un manto largo («manta»), «dat nog door de Indianen op de vaste kust wordt gedragen».",
         etiqueta="retro-abstraido", epoca="colonial/moderna",
         propuesta="El cocotero es poscontacto: no se proyecta. La manta como prenda que en 1881 todavía llevaban los indios de tierra firme es dato de la esfera (comparar con el vestido wayuu)."),
    dict(id="vk-mundo-06", esfera="creencia / muerte", pagina=224, pdf=6,
         dato="Entierro en urna hasta comienzos del s. XIX: un anciano de Savonet vio de niño enterrar a una india en cuclillas dentro de una urna, con la cabeza fuera; muchos invitados, se mataron ovejas y cabras. En Santa Cruz la urna de abajo aparece a menudo tapada con otra, que protegía la cabeza. El carbón en la capa de arriba le hace suponer al autor que se quemaban armas o enseres del muerto sobre la tumba. Nunca halló oro ni monedas en las urnas.",
         etiqueta="atestiguado (testigo, comienzos del s. XIX) / retro-abstraido para el s. XV", epoca="colonial",
         propuesta="Para creencia (ritos de muerte). ⚠️ Gatschet 1885 cuenta la MISMA anécdota (el viejo de «Saboneta»): no es una segunda atestación. La quema de enseres es inferencia del autor: va como su lectura."),
    dict(id="vk-mundo-07", esfera="ecología / creencia", pagina=224, pdf=6,
         dato="Nota 1: la rana («dori») sólo vive en Aruba, no en Curazao ni en Bonaire. El autor supone que los indios la preferían porque su croar sólo se oye en lluvias y anuncia la buena estación, y compara el croar con el sonido de la marakka.",
         etiqueta="atestiguado (la distribución, 1881) · hipotetico (la preferencia, lectura del autor)", epoca="moderna",
         propuesta="La distribución la confirma van Buurt (Pleurodema brachyops, llevada a Curazao en 1910 y a Bonaire en 1928). La lectura simbólica es del autor: no se fusiona como hecho."),
    dict(id="vk-mundo-08", esfera="técnica / pigmentos", pagina=223, pdf=5,
         dato="Pinturas minerales: tierra parda (¿ocre?) excavada en la gruta de Fontein; tierra roja sacada del cerro Tunnel, donde quedan hoyos rectangulares rellenos de piedra y muchas piedras trabajadas en cuña; tierra blanca cerca de Oranjestad y en la costa norte; tierra amarilla en Santa Cruz. Una tradición dice que los caribes usaban como aglutinante una savia viscosa de cactus. El negro pardo lo supone sacado de la tinta del calamar.",
         etiqueta="atestiguado (las canteras y hallazgos, 1881) · retro-abstraido (la savia de cactus, tradición)", epoca="moderna",
         propuesta="Para transmisión/técnica o ecología: las canteras de pigmento con nombre de lugar. Lo del calamar es conjetura del autor."),
    dict(id="vk-mundo-09", esfera="arte rupestre", pagina=226, pdf=8,
         dato="Las inscripciones están en grutas de caliza (Fontein, Carachito) o bajo bloques de granito (todas al suroeste). Rojo y pardo son los colores más comunes, el blanco no es raro, el negro sólo lo vio dos veces. Según la tradición, algunas figuras bajo los bloques señalan a los antiguos dueños o habitantes del sitio.",
         etiqueta="atestiguado (la observación, 1881) · retro-abstraido (lo de los dueños, tradición)", epoca="moderna",
         propuesta="Para el catálogo de petroglifos y para creencia/territorio: la tradición de que una figura marca al dueño del lugar. La lectura del autor sobre el significado de los colores (rojo = indios, blanco = blancos, negro = africanos) y el parentesco con los griegos y la Atlántida (p. 225) es especulación: se registra y no se fusiona."),
    dict(id="vk-mundo-10", esfera="memoria / geografía política", pagina=226, pdf=8,
         dato="Tradición de Carachito: los indios se defendieron allí de los franceses; los últimos, escondidos en una gruta más alta, fueron delatados por un perro que se quedó atrás y asesinados. En esa gruta circular hay huesos de hombres y de niños: el autor calcula entre ocho y diez personas.",
         etiqueta="retro-abstraido (tradición oral) · atestiguado (los huesos, 1881)", epoca="colonial",
         propuesta="Memoria oral de un episodio colonial. No es precontacto."),
    dict(id="vk-mundo-11", esfera="lengua (sociolingüística)", pagina=227, pdf=9,
         dato="«De Caraïbische taal wordt thans op Aruba niet meer gesproken»: la desplazó el papiamento. El autor sacó las voces «met moeite» de unos viejos, y las comparó con el caribe de Surinam y con el guajiro de la costa: «geheel verschilt» de los dos.",
         etiqueta="atestiguado (el estado de la lengua, 1881)", epoca="moderna",
         propuesta="Para 2-lengua (historia externa). La comparación con el guajiro es de aficionado y no pesa como dato de filiación; se registra porque es la primera que se hizo."),
    dict(id="vk-mundo-12", esfera="población", pagina=222, pdf=4,
         dato="En 1880-81, sobre todo en el sureste de Aruba, el autor ve un tipo físico indio «vrij zuiver»; en Curazao ha desaparecido y en Bonaire sólo se reconoce aquí y allá.",
         etiqueta="atestiguado (la observación de 1881, con el sesgo racial de su época)", epoca="moderna",
         propuesta="Contexto de la población, no dato del s. XV. Las valoraciones morales del autor (p. 222) no se fusionan."),
]


# ═════════════════════════════════════════════════════════════════════════
# 2. HERRAMIENTAS DE CRUCE
# ═════════════════════════════════════════════════════════════════════════

def llano(s):
    """Sin diacríticos, minúsculas, sin corchetes."""
    s = unicodedata.normalize("NFD", s.replace("ı", "i"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[\[\]]", "", s).lower()


def fon(s):
    """Clave de BÚSQUEDA (no lema): colapsa ortografías neerlandesa, inglesa y
    castellana para que Bedōēi, Bedui y Budui se encuentren. Palabra a
    palabra: un dígrafo no cruza el espacio («dat jē» no es «da-tj-e»)."""
    palabras = re.findall(r"[a-z]+", llano(s))
    if len(palabras) > 1:
        return "".join(fon(p) for p in palabras)
    s = palabras[0] if palabras else ""
    for a, b in (("sch", "sk"), ("oe", "u"), ("ou", "u"), ("tch", "S"), ("tj", "S"), ("sj", "S"),
                 ("sh", "S"), ("ch", "S"), ("dj", "di"), ("qu", "k"), ("ph", "f"),
                 ("gua", "wa"), ("gue", "we"), ("gui", "wi")):
        s = s.replace(a, b)
    s = s.replace("j", "y").replace("x", "").replace("h", "").replace("z", "s").replace("v", "b")
    s = re.sub(r"c(?=[eiy])", "s", s).replace("c", "k")
    s = re.sub(r"(.)\1+", r"\1", s)
    return s


def ratio(a, b):
    return round(difflib.SequenceMatcher(None, a, b).ratio(), 2)


def mejores(clave, candidatos, umbral, n=3):
    """candidatos: lista de (forma_original, clave_fon). Devuelve [(forma, ratio)]."""
    out = []
    for forma, c in candidatos:
        if not c:
            continue
        r = ratio(clave, c)
        if r >= umbral:
            out.append((forma, r))
    out.sort(key=lambda x: (-x[1], x[0]))
    vistos, res = set(), []
    for f, r in out:
        if f not in vistos:
            vistos.add(f)
            res.append((f, r))
        if len(res) >= n:
            break
    return res


def _sin_tilde(s):
    return llano(s)


# ── el lexicón ──
_ETIQUETAS_LENGUA = ("kalinago", "achagua", "caribe", "taino", "lokono", "wayuu", "paraujano",
                     "jirajara", "goeje", "perea", "zavala", "cumanagoto", "chaima", "medina")


def cargar_lexicon():
    import curiana_lexicon as L
    entradas = []
    for nombre, d in (("VOCABULARIO_BASE", L.VOCABULARIO_BASE), ("FUERA_DEL_HABLA", L.FUERA_DEL_HABLA)):
        for k, v in d.items():
            base = k
            partes = k.rsplit("-", 1)
            if len(partes) == 2 and any(partes[1].startswith(t) for t in _ETIQUETAS_LENGUA):
                base = partes[0]
            entradas.append(dict(clave=k, base=base, fon=fon(base), donde=nombre,
                                 fuente=v.get("fuente", "?"), sig=str(v.get("sig", ""))))
    return entradas


def lexicon_por_forma(formas, lex, umbral=0.85):
    res = []
    for f in formas:
        cf = fon(f)
        if len(cf) < 3:
            continue
        for e in lex:
            if not e["fon"]:
                continue
            if e["fon"] == cf or (len(cf) >= 4 and ratio(cf, e["fon"]) >= umbral):
                res.append(f"{e['clave']} [{e['fuente']}; {e['donde']}] '{e['sig'][:70]}' (≈ {f}, {ratio(cf, e['fon'])})")
    return sorted(set(res))


_LENGUAS_GLOSA = ("caquetío", "taíno", "lokono", "kalinago", "caribe", "wayunaiki", "paraujano", "achagua", "jirajaroide")


def lexicon_por_glosa(kws, lex, por_lengua=2):
    if not kws:
        return {}
    pats = [re.compile(r"\b" + re.escape(_sin_tilde(k)), re.I) for k in kws]
    grupos = {}
    for e in lex:
        sig = _sin_tilde(e["sig"])
        if any(p.search(sig) for p in pats):
            fam = next((l for l in _LENGUAS_GLOSA if e["fuente"].startswith(l)), None)
            if fam is None:
                continue
            clave = e["fuente"] if fam == "caquetío" else fam
            grupos.setdefault(clave, []).append(f"{e['clave']} '{e['sig'][:60]}'")
    return {k: sorted(v)[:por_lengua] + ([f"… y {len(v) - por_lengua} más"] if len(v) > por_lengua else [])
            for k, v in sorted(grupos.items())}


# ── Gatschet (lexicon_gatschet.py: las listas de Pinart ya reconciliadas) ──
def cargar_gatschet():
    import lexicon_gatschet as G
    voc = [(k, fon(k)) for k in G.GATSCHET_VOCABULARIO]
    top = {k: str(v.get("tipo", "")) for k, v in G.GATSCHET_TOPONIMOS.items()}
    formulas = [f["texto"] for f in G.GATSCHET_FORMULAS]
    return G, voc, top, formulas


def seccion_gatschet(nombre, tipo):
    """lexicon_gatschet marca cada topónimo con `tipo`: montaña / cueva / lugar."""
    return {"montaña": "cerros", "cueva": "grutas", "lugar": "lugares"}[tipo]


# ── van Buurt ──
def cargar_van_buurt():
    txt = open(VAN_BUURT_TXT, encoding="utf-8").read()
    i = txt.index("Anabui (Seru)")
    j = txt.index("Adicoura (Klein Curaçao)")
    lista_aruba = []
    for linea in txt[i:j].splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("Opmaak") or linea in ("Curaçao", "42"):
            continue
        nombre = re.sub(r"\s*\(.*?\)\s*", " ", linea).strip()
        for parte in re.split(r",\s*", nombre):
            parte = parte.replace("?", "").strip()
            if parte:
                lista_aruba.append((linea, fon(parte)))
    tokens = sorted(set(re.findall(r"[A-Za-zÀ-ÿ]{3,}", txt)))
    return txt, lista_aruba, [(t, fon(t)) for t in tokens]


# ── el canon de topónimos y los morfemas ──
def cargar_canon():
    d = yaml.safe_load(open(CANON_TOP, encoding="utf-8"))
    out = []
    for t in d["toponimos"]:
        forma = str(t.get("forma", "")).split("→")[0].strip()
        out.append(dict(id=t.get("id"), forma=forma, nivel=t.get("nivel"), fon=fon(forma),
                        procedencia=(t.get("procedencia") or {}).get("obra") if isinstance(t.get("procedencia"), dict) else None,
                        deuda=t.get("deuda")))
    return out


FORMANTES = [
    # (terminación en clave fon, qué es, dónde lo dice el canon)
    ("bana", "-bana 'cerro, sitio alto'", "TODAS_LAS_REGLAS['-bana'] (D9, #38, aprobada 2026-08-30)"),
    ("bani", "-bani (¿variante de -bana?)", "no está en el canon"),
    ("aima", "-aima 'abundancia'", "REGLAS_ZAVALA (Zavala #6, AM+PMA)"),
    ("ima", "-ima 'humedad, quebrada'", "REGLAS_ZAVALA (Zavala #165)"),
    ("bakwa", "-bakoa 'bosque, arboleda'", "morfemas.yaml morfema-001; REGLAS_TOPONIMICAS"),
    ("bari", "-bari", "morfemas.yaml morfema-010 (sin glosa; «no es un afijo», van Buurt: bara/bari 'árbol')"),
    ("kuri", "-kuri / -curi", "morfemas.yaml morfema-009 (sin glosa)"),
    ("ari", "-ari / -ri", "morfemas.yaml morfema-008 (sin glosa; van Buurt glosa rí 'duro' sólo en Casibari)"),
    ("iri", "-kiri / -diri", "lexicon_gatschet.SUFIJOS_NO_CODIFICADOS (sin glosa)"),
    ("iru", "-iru / -iro", "REGLAS_ESTEVES -iro 'diminutivo' (leído en topónimos)"),
    ("uri", "-uri / -ure", "morfemas.yaml morfema-002, conflicto: van Buurt §5 -ure/-uri 'raíz' (Cruz Esteves)"),
    ("Si", "-shi / -chi", "morfemas.yaml morfema-007 (sin glosa; «el formante más frecuente del corpus insular»)"),
    ("Se", "-shi / -chi", "morfemas.yaml morfema-007 (sin glosa)"),
]


def formantes_de(nombre):
    """La terminación más larga que el canon declara (‑bari antes que ‑ari,
    ‑aima antes que ‑ima, ‑kuri antes que ‑uri) y la reduplicación inicial."""
    c = fon(nombre)
    hallados = []
    for term, que, donde in FORMANTES:
        if c.endswith(term) and len(c) > len(term) + 1 and not any(h[0].endswith(term) for h in hallados):
            hallados.append((term, que, donde))
    m = re.match(r"^([a-zS]{2,4})\1", c)
    if m:
        hallados.append((m.group(1) * 2, "reduplicación", "lexicon_toponimos.REDUPLICACION"))
    return [f"{que} — {donde}" for _, que, donde in hallados]


# ── las citas de «Koolwijk» en las fuentes de texto del repo ──
def citas_koolwijk():
    res = {}
    for f in sorted(os.listdir(FUENTES)):
        if f.endswith(".txt") and not f.startswith("vanKoolwijk"):
            try:
                t = open(os.path.join(FUENTES, f), encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            n = len(re.findall(r"koolw", t, re.I))
            if n:
                res[f] = n
    return res


def n_por_u(a, b):
    """¿Hay una posición donde `a` (van Koolwijk) tiene u y `b` (Gatschet) tiene n?"""
    a2, b2 = llano(a).replace("c", "k"), llano(b).replace("c", "k")
    sm = difflib.SequenceMatcher(None, a2, b2)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "replace" and "u" in a2[i1:i2] and "n" in b2[j1:j2]:
            return True
    return False


# ═════════════════════════════════════════════════════════════════════════
# 3. EL ENSAMBLADO
# ═════════════════════════════════════════════════════════════════════════

def construir():
    lex = cargar_lexicon()
    G, g_voc, g_top, g_formulas = cargar_gatschet()
    vb_txt, vb_aruba, vb_tokens = cargar_van_buurt()
    canon = cargar_canon()
    canon_c = [(f"{c['id']} {c['forma']} [{c['nivel']}]", c["fon"]) for c in canon]

    # ── vocabulario arubano ──
    vocab = []
    vb_tokens4 = [(t, c) for t, c in vb_tokens if len(c) >= 4]
    for e in VOCES_ARUBA + PLANTAS_Y_ANIMALES:
        # La pareja con Gatschet es una LECTURA (la del minador, con las dos
        # páginas delante); el script comprueba que existe en lexicon_gatschet
        # y mide cuánto se parecen. Sin pareja leída, se dice cuál sería el
        # mejor candidato por forma y que no es la misma voz.
        if e["gatschet"]:
            claves = [k.strip() for k in e["gatschet"].split("·")]
            for k in claves:
                assert k in G.GATSCHET_VOCABULARIO, f"{e['id']}: «{k}» no está en lexicon_gatschet"
            g_cruce = dict(pareja_leida=e["gatschet"],
                           ratio=max(ratio(fon(f), fon(k)) for f in e["formas"] for k in claves),
                           glosa_gatschet=" · ".join(str(G.GATSCHET_VOCABULARIO[k].get("glosa_fuente")) for k in claves),
                           nivel_en_la_mineria_de_gatschet=" · ".join(str(G.GATSCHET_VOCABULARIO[k].get("nivel")) for k in claves))
        else:
            cand = []
            for f in e["formas"]:
                cand += mejores(fon(f), g_voc, 0.6, n=1)
            g_cruce = ("no está" + (f" (mejor candidato por forma: {max(cand, key=lambda x: x[1])[0]}, "
                                     f"ratio {max(cand, key=lambda x: x[1])[1]} — no es la misma voz)" if cand else ""))
        vb = []
        for f in e["formas"]:
            if len(fon(f)) >= 4:
                vb += mejores(fon(f), vb_tokens4, 0.88, n=3)
        vb = sorted(set(vb), key=lambda x: (-x[1], x[0]))[:4]
        vocab.append(dict(
            id=e["id"], pagina=227 if e["id"] != "vk-aru-23" else "227 (y nota 1 de la p. 224)", pdf=9,
            forma_fuente=e["forma"], forma_llana=llano(e["forma"]), glosa_nl=e["nl"], glosa_es=e["es"],
            verificado_en_imagen=f"sí — pdf 9 a resolución nativa ({FACTOR_NATIVO})",
            lengua_propuesta=e["lengua"], escala_protocolo=e["escala"],
            cruce=dict(
                lexicon_por_forma_sin_filtro_de_glosa=lexicon_por_forma(e["formas"], lex) or "ninguna coincidencia",
                lexicon_por_glosa=((lexicon_por_glosa(e["kw"], lex) or "ninguna entrada con esa glosa")
                                   if e["kw"] else "sin glosa individual en la fuente"),
                gatschet_1885=g_cruce,
                van_buurt_2014_por_forma=[f"{f} ({r})" for f, r in vb] or "no está",
            ),
            veredicto=e["veredicto"], propuesta=e["propuesta"],
        ))
    conj = dict(CONJURA)
    gform = max(((t, ratio(fon(CONJURA["forma"]), fon(t))) for t in g_formulas), key=lambda x: x[1])
    conj["verificado_en_imagen"] = f"sí — pdf 9 ({FACTOR_NATIVO})"
    conj["cruce"] = dict(gatschet_1885=f"{gform[0]} (ratio {gform[1]})")

    # ── topónimos ──
    def top_entrada(nombre, lista, pos):
        c = fon(nombre)
        g = mejores(c, [(k, fon(k)) for k in g_top], 0.72, n=2)
        vb = mejores(c, vb_aruba, 0.72, n=2)
        can = mejores(c, canon_c, 0.85, n=2)
        nota = NOTAS_TOPONIMO.get(nombre, {})
        otras = [l for l, ns in (("lugares", TOP_LUGARES), ("cerros", TOP_CERROS), ("grutas", TOP_GRUTAS))
                 if l != lista and any(fon(x) == c for x in ns)]
        return dict(
            forma_fuente=nombre, forma_llana=llano(nombre), lista=lista, orden_en_la_lista=pos,
            pagina=227, pdf=9, verificado_en_imagen=f"sí — pdf 9 a resolución nativa ({FACTOR_NATIVO})",
            tambien_en=otras or None,
            cruce=dict(
                canon_toponimos=[f"{f} ({r})" for f, r in can] or "no está",
                gatschet_1885=[f"{f} ({r})" for f, r in g] or "no está",
                van_buurt_2014_s7=[f"{f} ({r})" for f, r in vb] or "no está",
            ),
            formantes=formantes_de(nombre) or "ninguno del canon",
            glosa_de_la_fuente="ninguna (el autor sólo da la lista)",
            nivel_propuesto=nota.get("nivel", "descartado"),
            propuesta=nota.get("propuesta", "Sin glosa de fuente y sin morfema que alinee: descartado (= sin lectura, no «no existió»). Lo que aporta es la forma fechada en 1881."),
        )

    toponimos = {
        "lugares": [top_entrada(n, "lugares", i + 1) for i, n in enumerate(TOP_LUGARES)],
        "cerros": [top_entrada(n, "cerros", i + 1) for i, n in enumerate(TOP_CERROS)],
        "grutas": [top_entrada(n, "grutas", i + 1) for i, n in enumerate(TOP_GRUTAS)],
    }
    for t in toponimos["lugares"] + toponimos["cerros"] + toponimos["grutas"]:
        if t["tambien_en"] is None:
            del t["tambien_en"]

    # ── independencia: van Koolwijk ↔ Gatschet ↔ van Buurt ──
    g_por_sec = {"lugares": [], "cerros": [], "grutas": []}
    for k, sec in g_top.items():
        g_por_sec[seccion_gatschet(k, sec)].append(k)
    mapa = {"lugares": TOP_LUGARES, "cerros": TOP_CERROS, "grutas": TOP_GRUTAS}
    solape = {}
    for sec, nombres_vk in mapa.items():
        unicos_vk = {fon(n): n for n in nombres_vk}
        g_list = g_por_sec[sec]
        g_en_vk = [k for k in g_list if mejores(fon(k.replace(" (cueva)", "")), [(v, f) for f, v in unicos_vk.items()], 0.72, n=1)]
        vk_en_g = [v for f, v in unicos_vk.items() if mejores(f, [(k, fon(k.replace(" (cueva)", ""))) for k in g_list], 0.72, n=1)]
        solape[sec] = dict(
            van_koolwijk=len(unicos_vk), gatschet=len(g_list),
            de_gatschet_que_estan_en_van_koolwijk=len(g_en_vk),
            de_van_koolwijk_que_estan_en_gatschet=len(vk_en_g),
            solo_en_van_koolwijk=sorted(v for f, v in unicos_vk.items() if v not in vk_en_g),
            solo_en_gatschet=sorted(k for k in g_list if k not in g_en_vk),
        )
    # (el resumen de los que Gatschet no trae en NINGUNA de sus tres listas va en
    # `independencia.nombres_que_gatschet_no_trae`)
    voc_vk_en_g = [e["id"] for e in vocab if isinstance(e["cruce"]["gatschet_1885"], dict)]
    sin_pareja_vk = [e["forma_fuente"] for e in vocab if e["id"] not in voc_vk_en_g]
    n_formulas_g = len(G.GATSCHET_FORMULAS)
    todos_g = [(k, fon(k.replace(" (cueva)", ""))) for k in g_top]
    solo_vk_en_ninguna = sorted({n for n in TOP_LUGARES + TOP_CERROS + TOP_GRUTAS
                                 if not mejores(fon(n), todos_g, 0.72, n=1)}, key=fon)
    n_solo_vk_top = len({fon(n) for n in solo_vk_en_ninguna})
    subconjunto = "; ".join(f"{sec}: {v['de_gatschet_que_estan_en_van_koolwijk']} de {v['gatschet']}"
                            for sec, v in solape.items())
    assert all(not v["solo_en_gatschet"] for v in solape.values()), "Gatschet ya no es subconjunto: revisar el veredicto"
    pares_nu = [("caula", "kanla"), ("Cautje", "kantie"), ("daūchikki", "danshikki")]
    confusiones = [dict(van_koolwijk=a, gatschet=b, n_por_u=n_por_u(a, b)) for a, b in pares_nu]
    n_nu = sum(1 for c in confusiones if c["n_por_u"])

    independencia = dict(
        pregunta="¿Van Koolwijk 1882 es una segunda atestación independiente de lo que ya dicen Gatschet 1885 (Pinart) y van Buurt 2014?",
        fechas=dict(
            van_koolwijk="firmado «Aruba, 20 November 1881» (p. 227, verificado en imagen); publicado en 1882; el autor llegó a Aruba el 20-XI-1880 (p. 222)",
            pinart="visitó las islas «in the summer of 1882» (Gatschet 1885 p. 300) — después de que van Koolwijk firmara",
            gatschet="leído el 18-VII-1884, publicado en 1885",
            contacto="Wagenaar Hummelinck 1953 (WagenaarHummelinck_1953_Rotstekeningen_I.txt, línea 287): Pinart es «door VAN KOOLWIJK als een in oudheden belangstellende bezoeker van Aruba genoemd» — se conocían",
        ),
        solape_de_topónimos=solape,
        solape_de_vocabulario=dict(
            voces_de_van_koolwijk=len(vocab), con_pareja_en_gatschet=len(voc_vk_en_g),
            sin_pareja=sorted(e["forma_fuente"] for e in vocab if e["id"] not in voc_vk_en_g),
            nota="La pareja es una lectura del minador con las dos fuentes delante; el script comprueba que la voz existe en lexicon_gatschet y mide el parecido (cruce.gatschet_1885.ratio de cada voz)."),
        nombres_que_gatschet_no_trae=solo_vk_en_ninguna,
        misma_anecdota="el entierro en urna con la cabeza fuera, contado por un viejo de Savonet / «Saboneta» (van Koolwijk p. 224; Gatschet p. 300)",
        misma_formula=f"el conjuro de la iguana, palabra por palabra (ratio {gform[1]} sobre la clave fon)",
        confusiones_n_u=dict(
            pares=confusiones,
            lectura=f"{n_nu} veces donde la fuente impresa trae u, Gatschet trae n — y en una el propio Gatschet duda («kanla (?kaula)»). Es la confusión típica de quien copia de un manuscrito, no de quien oye."),
        citas_de_koolwijk_en_el_repo=citas_koolwijk(),
        van_buurt=("Cita a van Koolwijk dos veces: (1) entre las listas de voces indígenas «in use in Aruba in the late "
                   "19th century» (junto a Pinart); (2) s.v. dabaruida: «In a list from 1880 with Indian words from Aruba "
                   "made by Father van Koolwijk we find dabaroida (Hartog, 1953)». Lo lee A TRAVÉS de Hartog. Y cita a "
                   "Pinart (como «1890») para Wakubana, purantsi y la fórmula de las espinas. Su lista de topónimos (§7) "
                   "no dice de dónde sale cada nombre."),
        zayas_y_hartog="Zayas 1931 no cita a van Koolwijk (0 menciones en los dos tomos). Hartog 1953/1968 no está en el repo: sólo llega citado por van Buurt.",
        veredicto=(
            "Van Koolwijk 1882 NO es una segunda atestación independiente de lo que dicen Gatschet y van Buurt: es "
            "la FUENTE PRIMARIA DE LA CADENA. Firmó en noviembre de 1881, antes de que Pinart pisara la isla; las "
            f"listas de topónimos de Gatschet son un subconjunto de las suyas ({subconjunto}); la anécdota y la "
            f"fórmula son las mismas; y {n_nu} confusiones n/u delatan copia de un escrito. Van Buurt, a su vez, lo "
            "lee vía Hartog y cita a Pinart. La cadena es van Koolwijk 1881 → Pinart 1882 / Gatschet 1885 → "
            "(Hartog 1953) → van Buurt 2014. Lo que sí es independiente: el mapa de 1825 (Wacobana), los nombres "
            "VIVOS que van Buurt registra en el papiamento y en el mapa de hoy, y lo que sólo trae uno de los dos "
            f"(Pinart: kafa, tomoi, sus plantas, peces, aves e insectos y {n_formulas_g - 1} fórmulas más; van "
            f"Koolwijk: {', '.join(sin_pareja_vk)} y {n_solo_vk_top} topónimos que Gatschet no trae en ninguna lista)."),
        consecuencias=[
            "karebe: sus DOS atestaciones independientes siguen siendo dos (Aruba y Paraguaná), pero la del lado arubano es van Koolwijk 1882 p. 227; Gatschet es la misma cadena.",
            "dabaraida (lexicon_gatschet.py): la «TRIPLE atestación independiente» es una cadena histórica más la forma viva de van Buurt.",
            "Toda voz o topónimo arubano que hoy se apoye en «Gatschet + van Buurt» como dos fuentes debe revisarse con esta cadena delante.",
        ],
    )

    # ── kari'ña de Surinam ──
    sur = []
    lex_glosa_cache = {}
    for pag, nl, forma, es in CARIBE_SURINAM:
        f_base = re.sub(r"\s*\(.*?\)", "", forma)
        kws = [w for w in re.findall(r"[a-záéíóúñ]{4,}", es.lower())
               if w not in ("persona", "nosotros", "alguien", "otro", "también", "siempre", "quieres", "mostraré", "pasado")][:2]
        coincide = []
        for kw in kws:
            if kw not in lex_glosa_cache:
                pat = re.compile(r"\b" + re.escape(_sin_tilde(kw)), re.I)
                lex_glosa_cache[kw] = [e for e in lex if pat.search(_sin_tilde(e["sig"]))]
            for e in lex_glosa_cache[kw]:
                for parte in re.split(r",\s*|\s+of\s+", f_base):
                    if e["fon"] and len(fon(parte)) >= 3 and ratio(fon(parte), e["fon"]) >= 0.75:
                        coincide.append(f"{e['clave']} [{e['fuente']}] '{e['sig'][:50]}'")
        ent = dict(pagina=pag, glosa_nl=nl, forma_fuente=forma, glosa_es=es)
        if forma in DUDAS_SURINAM or forma.split(" ")[0] in DUDAS_SURINAM:
            ent["duda"] = DUDAS_SURINAM.get(forma, DUDAS_SURINAM.get(forma.split(" ")[0]))
        if nl == "visch":
            ent["duda"] = DUDAS_SURINAM["wāto"]
        if coincide:
            ent["coincide_en_forma_y_glosa"] = sorted(set(coincide))[:4]
            ent["lectura_de_la_coincidencia"] = LECTURA_COINCIDENCIAS_SURINAM.get(forma, "SIN LEER — revisar")
        if "(spaansch" in forma or "(neger-engelsch" in forma:
            ent["marca_del_autor"] = "castellano" if "spaansch" in forma else "neger-engels (sranan)"
        sur.append(ent)

    # ── meta y cobertura ──
    cuenta = dict(
        voces_aruba=len(VOCES_ARUBA), plantas_y_animales_aruba=len(PLANTAS_Y_ANIMALES), conjuros=1,
        toponimos_por_lista={k: len(v) for k, v in toponimos.items()},
        toponimos_menciones=sum(len(v) for v in toponimos.values()),
        toponimos_formas_distintas=len({fon(x) for x in TOP_LUGARES + TOP_CERROS + TOP_GRUTAS}),
        toponimos_en_prosa=len(TOP_EN_PROSA),
        caribe_surinam_entradas=len(CARIBE_SURINAM),
        caribe_surinam_con_coincidencia_forma_y_glosa=sum(1 for s in sur if "coincide_en_forma_y_glosa" in s),
        filas_de_la_lamina=len(LAMINA),
        figuras_numeradas_en_la_lamina=max(int(n) for f in LAMINA for n in re.findall(r"\d+", f["figs"])),
        datos_de_mundo=len(MUNDO),
    )
    meta = dict(
        obra=OBRA,
        minado="2026-10-05",
        encargo="Miguel, 2026-10-05: minarla «de una» (rama fuentes/arte-rupestre). Propuesta, no fusión (regla 5).",
        generado_por="6-fusion/scripts/minar_van_koolwijk_1882.py — no se edita a mano: se corrige el script y se regenera",
        paginas=dict(
            articulo="pdf 4-11 = pp. impresas 222-229 (pdf + 218); lámina fuera de texto en pdf 12-13 («N° 7»)",
            sin_articulo=PAGINAS_SIN_ARTICULO,
        ),
        cobertura=dict(
            leido_en_imagen=(f"pdf {min(PDF_A_IMPRESA)}-{max(LAMINA_PDF)} enteros (las {len(PDF_A_IMPRESA)} páginas del "
                             "artículo y las dos mitades de la lámina): la prosa por medias columnas a 6×, las listas "
                             "a resolución nativa y las dudas a 12-16×"),
            capa_de_texto="parcial: pdf 4 y 11-16 casi sin texto, y la p. 228 con las columnas corridas — por eso se leyó en imagen y no se usó el .txt para nada que se cite",
            conteos=cuenta,
        ),
        no_leido=[
            "van Koolwijk 1881 (Curazao, TAG 5 pp. 57-68) y 1885 («Indiaansche opschriften te Aruba», Études Leemans pp. 183-184): no están en el repo (Wagenaar Hummelinck 1953 los cita)",
            "Pinart 1890 sobre Aruba: no está en el repo (Wagenaar Hummelinck tampoco lo encontró)",
            "Hartog 1953/1968: no está en el repo; sólo llega por van Buurt",
        ],
        lo_que_cambia_el_encargo=(
            f"La lista larga (töna, wato, kwai, toëkoëwari, porkoe…; {len(CARIBE_SURINAM)} entradas) es el kari'ña "
            "de SURINAM (1870), no arubano: el autor la pone para mostrar que es otra lengua. Lo arubano son "
            f"{len(VOCES_ARUBA)} voces y frases, {len(PLANTAS_Y_ANIMALES)} nombres de plantas y animales y un "
            "conjuro (p. 227). Y kwai es 'kalebas', no 'pijl': el par lo había corrido pdftotext."),
        convencion=(
            "forma_fuente copia el macrón y la breve donde caen; el macrón sobre el dígrafo «oe» (= /u/) se escribe "
            "«ōe»; [corchetes] = letra rota. forma_llana quita los diacríticos. Los diacríticos se leyeron a "
            "resolución nativa, pero en tipo de 9 pt pueden fallar letra a letra: antes de citar una forma como "
            "exacta, mirar la imagen."),
    )

    return dict(
        meta=meta,
        independencia=independencia,
        vocabulario_aruba=vocab,
        conjuro=conj,
        toponimos=toponimos,
        toponimos_en_prosa=TOP_EN_PROSA,
        caribe_surinam_1870=dict(
            que_es=("kari'ña (caribe) de Surinam, ríos Tibiti y Wojambo, apuntado por el autor en 1870 (p. 227). "
                    "NO es arubano ni caquetío. Etiqueta propuesta: comparanda caribe continental, FUERA de la esfera "
                    "(Surinam); no entra al lexicón. Sirve para dos cosas: separar lo arubano de lo que no lo es, y "
                    "como control caribe (como el jirajara de Jahn)."),
            pagina="227-229 (pdf 9-11)",
            verificado_en_imagen=f"sí — las tres páginas a resolución nativa ({FACTOR_NATIVO})",
            nota_del_cruce=("coincide_en_forma_y_glosa = una entrada del lexicón con la misma glosa y forma parecida "
                            "(ratio ≥ 0,75). Es un indicio de préstamo areal o de parentesco caribe, no una prueba "
                            "(minar-fuente §2)."),
            entradas=sur,
            padrenuestro=dict(pagina=229, texto=PADRENUESTRO, nota="kari'ña con préstamos («santo», «pardon», «Pāpa») y una frase que parece criolla («a kon de leri»)"),
            diez_mandamientos=dict(pagina=229, texto=MANDAMIENTOS, nota="el 3.º lo marca el autor como neger-engels"),
        ),
        lamina=dict(
            veredicto=("NINGUNA figura de la lámina es un signo rupestre. El texto (pp. 223-224) las identifica todas "
                       "como cerámica de los campamentos de Santa Cruz y Savonet: motivos pintados en tiestos (1-10, que "
                       "el autor compara con vasos griegos), ranas en relieve (11-13), asas (14-18), un pico (19), una "
                       "vasija (20) y la urna (21). Las inscripciones de las grutas las describe con palabras (pp. "
                       "225-226) pero no las dibuja. Las primeras figuras publicadas de inscripciones arubanas son de "
                       "Martin 1885 (Fontein y Canashito), según Wagenaar Hummelinck 1953; no está en el repo."),
            corrige="el catálogo 6-fusion/petroglifos_imagenes_2026-10-05.yaml, que leía zigzag, espirales, rana y cara como signos rupestres",
            figuras=LAMINA,
        ),
        mundo=MUNDO,
    )


def volcar(datos):
    cab = (
        "# ─────────────────────────────────────────────────────────────────────────\n"
        "# Van Koolwijk 1882, «De Indianen Caraïben van het eiland Aruba» — PROPUESTA\n"
        "# de minería (regla 5: minar propone, el humano fusiona). Nada de esto toca\n"
        "# el lexicón, el corpus ni el canon de topónimos.\n"
        "#\n"
        "# GENERADO por 6-fusion/scripts/minar_van_koolwijk_1882.py: la transcripción\n"
        "# (leída en imagen) y las propuestas viven en el script; los cruces y las\n"
        "# cifras los calcula él. No se edita a mano: se corrige el script y se corre\n"
        "# con --escribir. `--check` dice si este archivo está al día.\n"
        "# ─────────────────────────────────────────────────────────────────────────\n"
    )
    return cab + yaml.safe_dump(datos, allow_unicode=True, sort_keys=False, width=110, default_flow_style=False)


def validar_obras():
    """Regla 8: las obras que este YAML nombra como clave existen en la bibliografía."""
    bib = yaml.safe_load(open(BIBLIO, encoding="utf-8"))
    ids = {e["id"] for e in (bib if isinstance(bib, list) else bib.get("obras", bib.get("fuentes", [])))}
    faltan = [o for o in (OBRA, "gatschet-1885", "van-buurt-2014", "wagenaar-hummelinck-1953",
                          "wagenaar-hummelinck-1962", "esteves-1989", "oliver-1989-cap2", "zayas-1931") if o not in ids]
    return faltan


def main():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--escribir", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    faltan = validar_obras()
    if faltan:
        print("✗ obras que no están en 4-fuentes/bibliografia.yaml:", faltan)
        sys.exit(1)
    datos = construir()
    texto = volcar(datos)
    if a.check:
        # newline="" para leer el archivo tal cual; se compara sin CR porque git
        # puede devolverlo con CRLF en Windows (core.autocrlf).
        actual = open(SALIDA, encoding="utf-8", newline="").read() if os.path.exists(SALIDA) else ""
        if actual.replace("\r\n", "\n") != texto:
            print("✗ el YAML no está al día: corre con --escribir")
            sys.exit(1)
        print("✓ el YAML está al día")
        return
    if a.escribir:
        with open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto)
        assert yaml.safe_load(open(SALIDA, encoding="utf-8"))["meta"]["obra"] == OBRA
        print(f"✓ escrito {os.path.relpath(SALIDA, RAIZ)}")
    c = datos["meta"]["cobertura"]["conteos"]
    print(yaml.safe_dump(dict(conteos=c, solape=datos["independencia"]["solape_de_topónimos"],
                              vocabulario=datos["independencia"]["solape_de_vocabulario"],
                              n_u=datos["independencia"]["confusiones_n_u"]["pares"],
                              formula=datos["independencia"]["misma_formula"],
                              citas=datos["independencia"]["citas_de_koolwijk_en_el_repo"]),
                         allow_unicode=True, sort_keys=False))


if __name__ == "__main__":
    main()
