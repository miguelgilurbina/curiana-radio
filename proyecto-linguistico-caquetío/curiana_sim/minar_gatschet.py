"""
CURIANA — Minería de Gatschet 1885, *The Aruba Language and the Papiamento Jargon*
==================================================================================

    Gatschet, Albert S. (1885). "The Aruba Language and the Papiamento Jargon".
    Proceedings of the American Philosophical Society, XXII(120), pp. 299-305.
    Leído el 18 de julio de 1884. Material lingüístico recogido por
    Alphonse L. Pinart en Aruba, verano de 1882, de hablantes ancianos.
    → fuentes_caquetios/Gatschet_1885_Aruba_texto.txt      (OCR JSTOR)
    → fuentes_caquetios/Gatschet_1885_biostor_texto.txt    (OCR BioStor)

POR QUÉ IMPORTA: es **vocabulario caquetío insular directo**, y el propio
Gatschet lo ancla al proyecto: *"The Aruban language was probably the same as
that of Curaçao and related to the vernacular of the peninsula of Paraguaná"*.

REGLA CERO (protocolo `investigacion/disenos/02_protocolo_habla_paraguanera.md`):
**una voz de Pinart no es caquetía por defecto.** Aruba llevaba en 1882 unos 80
años hablando papiamento; el competidor #2 del protocolo (papiamento/neerlandés)
es aquí *el más fuerte de todos*. Y van Buurt 2014 dice de esta misma lista que
*"contains several words which are definitely not Indian"*.

MÉTODO
------
1. **Dos OCR en paralelo.** Ambos archivos son el mismo artículo con dos
   digitalizaciones distintas. Donde uno está sucio el otro suele resolver
   (`Oereus` → `Cereus`, `Malividiri` → `Matividiri`, `Shabaruri` → `Shabururi`,
   `,\\-erebete` → `xerebete`). El script extrae las secciones de LOS DOS y
   verifica cada forma curada contra ambos, dejando constancia de qué OCR la
   sostiene. Si una forma no aparece en ninguno, lo grita.
2. **Política D7** (Miguel, 2026-08-03): la taxonomía decimonónica de Gatschet
   se conserva verbatim en `glosa_fuente`; el taxón actual va en
   `identificacion_moderna`. **Ninguna gana.**
3. **Escala A/B/C/D** del protocolo §5, más dos etiquetas propias:
   `T` (topónimo: canon, fuera del habla) y `R` (fórmula ritual: texto no
   traducible, valor ritual, no léxico).

NO modifica `curiana_lexicon.py`: emite propuesta para revisión humana, en la
misma disciplina que `minar_zavala_glosario.py`.

Uso:
    python minar_gatschet.py                      # informe
    python minar_gatschet.py --json out.json
    python minar_gatschet.py --generar-modulo     # escribe lexicon_gatschet.py
"""

import argparse
import difflib
import io
import json
import os
import re
import sys
import unicodedata

# La consola de Windows es cp1252 y revienta con "í", "ú" o "→".
# (minar_zavala_glosario.py NO hace esto y falla al redirigir su salida.)
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_AQUI = os.path.dirname(os.path.abspath(__file__))
OCR_JSTOR = os.path.join(_AQUI, "..", "fuentes_caquetios", "Gatschet_1885_Aruba_texto.txt")
OCR_BIOSTOR = os.path.join(_AQUI, "..", "fuentes_caquetios", "Gatschet_1885_biostor_texto.txt")

FUENTE_CITA = ("Gatschet 1885, Proc. Am. Philos. Soc. XXII(120):299-305 "
               "(material de A. L. Pinart, Aruba 1882)")


# ══════════════════════════════════════════════════════════════════════
# 1. SECCIONES DEL ARTÍCULO
# ══════════════════════════════════════════════════════════════════════
# (clave, regex de inicio, regex de fin). Los dos OCR mantienen los mismos
# encabezados salvo ruido menor, así que un patrón tolerante sirve para ambos.

SECCIONES = [
    ("nombres",   r"Nouns,\s*verbs\s*and\s*sentences",       r"Names\s+given\s+to\s+Aruban\s+mountains"),
    ("montanas",  r"Names\s+given\s+to\s+Aruban\s+mountains", r"Names\s+of\s+Aruban\s+caves"),
    ("cuevas",    r"Names\s+of\s+Aruban\s+caves",             r"Names\s+of\s+Aruban\s+places"),
    ("lugares",   r"Names\s+of\s+Aruban\s+places",            r"Names\s+of\s+Aruban\s+trees"),
    ("arboles",   r"Names\s+of\s+Aruban\s+trees",             r"Names\s+of\s+plants"),
    ("plantas",   r"Names\s+of\s+plants",                     r"Names\s+of\s+fish"),
    ("peces",     r"Names\s+of\s+fish",                       r"Names\s+of\s+birds"),
    ("aves",      r"Names\s+of\s+birds",                      r"Insects\s+and\s+other\s+animals"),
    ("animales",  r"Insects\s+and\s+other\s+animals",         r"Several\s+of\s+these\s+names"),
    ("formulas",  r"conjurer.s\s+formulas",                   r"When\s+A\.?\s*L\.?\s*Pin"),
    ("papiamento", r"The\s+following\s+objects\s+of\s+natural\s+history", r"We\s+add\s+a\s+few"),
]


# ══════════════════════════════════════════════════════════════════════
# 2. TABLA CURADA — la lectura reconciliada de los dos OCR
# ══════════════════════════════════════════════════════════════════════
# Cada entrada: forma reconciliada, sección, glosa VERBATIM de Gatschet
# (política D7), identificación moderna cuando se pudo establecer, veredicto
# A/B/C/D/T/R y su razón, y el cruce con van Buurt 2014 (§6 = "probablemente
# caquetío", §7 = topónimos probablemente caquetíos, §11 = "vínculo menos
# cierto" — el propio autor degrada).

ENTRADAS: list[dict] = [

    # ── Nouns, verbs and sentences ────────────────────────────────────
    {"forma": "adamudu", "sec": "nombres", "glosa_fuente": "rain",
     "nivel": "C", "razon": "sobrevive los seis descartes (no es español, papiamento, "
     "neerlandés, wayuu, taíno ni caribe conocido) pero no tiene ni cognado ni "
     "atestación externa: solo la fonotáctica la sostiene, que es filtro negativo, no positivo"},
    {"forma": "baru xantu uou", "sec": "nombres", "ocr_alt": "baru xantu uqu",
     "glosa_fuente": "to ask for something to eat",
     "nivel": "C", "razon": "frase, no lema; sin segmentación posible. Los dos OCR "
     "difieren en la última palabra (uou / uqu). No es material de léxico"},
    {"forma": "danshikki", "sec": "nombres", "glosa_fuente": "sack, pouch",
     "nivel": "C", "razon": "el grupo /ʃi/ que van Buurt considera marca caquetía está "
     "presente, pero es un objeto de comercio (justo donde el préstamo es más probable) "
     "y no hay cognado"},
    {"forma": "danshebu", "sec": "nombres", "ocr_alt": "dansliebu",
     "glosa_fuente": "sack, pouch (variante de danshikki)",
     "nivel": "C", "razon": "variante de danshikki; mismo veredicto"},
    {"forma": "datie", "sec": "nombres", "glosa_fuente": "be gone!",
     "nivel": "C", "razon": "interjección — la clase de menor rendimiento según el "
     "protocolo §6, y homófona del imperativo español 'date'. A favor: reaparece dentro "
     "de la fórmula infantil (tue daye datie'), lo que la ancla a la lengua extinta"},
    {"forma": "kafa", "sec": "nombres", "glosa_fuente": "devil, wicked spirit",
     "nivel": "C", "razon": "es la ÚNICA correspondencia comparativa que Gatschet creyó "
     "encontrar (goajiro yaria/yarias/yaroja) y no se sostiene: kafa y yaria no comparten "
     "ni una consonante. Además 'diablo' es concepto poscontacto. Reaparece en la fórmula "
     "de maledicción, que es su mejor argumento"},
    {"forma": "kanla", "sec": "nombres", "ocr_alt": "kaula",
     "glosa_fuente": "thing, object (el propio Gatschet duda: '(?kaula)')",
     "nivel": "C", "razon": "abstracto genérico, la peor clase posible; y la propia fuente "
     "no sabe leer su forma"},
    {"forma": "kantie baulete", "sec": "nombres", "glosa_fuente": "give me to eat!",
     "nivel": "C", "razon": "frase, no lema; sin segmentación posible"},
    {"forma": "karebe", "sec": "nombres", "glosa_fuente": "spoon",
     "nivel": "C", "razon": "cultura material; sobrevive los descartes pero sin cognado "
     "ni atestación externa"},
    {"forma": "aba dobo edan guayete", "sec": "nombres",
     "ocr_alt": "aaba dobo^edaa guayete / A aba dobo^edan guayete",
     "glosa_fuente": "sit down!",
     "nivel": "C", "razon": "los DOS OCR están rotos en el mismo punto; la forma no es "
     "reconstruible con confianza. Se registra para que un tercer testimonio la resuelva"},
    {"forma": "tida meo", "sec": "nombres", "ocr_alt": ",tida meo / ^ida meo",
     "glosa_fuente": "good morning!",
     "nivel": "C", "razon": "SOSPECHA ALTA: fórmula de saludo en una isla que llevaba 80 "
     "años hablando papiamento, y va emparejada con 'ute kontabo', que es papiamento "
     "transparente. Las fórmulas de cortesía son la primera capa que se sustituye. "
     "Además el primer carácter difiere entre los dos OCR"},
    {"forma": "xovam", "sec": "nombres", "ocr_alt": "tomoi",
     "glosa_fuente": "phantom, hobgoblin",
     "nivel": "D", "filtro": "forma irreconstruible",
     "razon": "los dos OCR leen cosas incompatibles ('xovam' vs ';tomoi'). No es un "
     "problema de etimología sino de que no sabemos qué palabra es. Inutilizable hasta "
     "ver el facsímil"},
    {"forma": "ute kontabo", "sec": "nombres", "glosa_fuente": "how do you do?",
     "nivel": "D", "filtro": "2 — papiamento/neerlandés",
     "razon": "PAPIAMENTO TRANSPARENTE: 'kontabo' es *kon ta bo* ('¿cómo estás?'), la "
     "fórmula corriente del papiamento, con *(b)o* de segunda persona. Es probablemente "
     "una de las voces que van Buurt tenía en mente al decir que la lista de Pinart "
     "'contains several words which are definitely not Indian'"},
    {"forma": "totumba", "sec": "nombres", "glosa_fuente": "water-gourd",
     "nivel": "D", "filtro": "4 — antillanismo panamericano",
     "razon": "derivado de *totuma*, voz caribe/taína incorporada al español general "
     "(DRAE) y difundida por toda Hispanoamérica. Que se diga en Aruba no prueba "
     "sustrato caquetío local"},
    {"forma": "waidanga", "sec": "nombres", "glosa_fuente": "water-gourd (variante)",
     "nivel": "C", "razon": "a diferencia de totumba no es panamericana; pero la "
     "terminación -nga es sospechosa de bantuismo (cf. mamondenga en esta misma lista) "
     "y van Buurt advierte que hay palabras africanas en la lista de Pinart"},

    # ── Names of Aruban trees ─────────────────────────────────────────
    {"forma": "dabaraida", "sec": "arboles", "glosa_fuente": "a tree (sin taxón en la fuente)",
     "identificacion_moderna": "Pithecellobium unguis-cati (van Buurt 2014 §6, s.v. dabaruida)",
     "van_buurt": "§6 dabaruida/yaga (A)",
     "nivel": "A", "razon": "TRIPLE atestación independiente: van Koolwijk 1880 (dabaroida), "
     "Pinart 1882 (dabaraida), van Buurt 2014 (dabaruida, forma viva). Y etimología "
     "arahuaca con correspondencia: lokono *dabáda* 'uña, garra' + *ida* 'rodeado de, piel' "
     "(De Goeje 1928), con paralelo shebayo de 1594-95 *dabodda/dabádoh* 'uña'. "
     "Es el mejor resultado de esta fuente"},
    {"forma": "hubada", "sec": "arboles", "glosa_fuente": "a tree (parte de 'hubada tarabada')",
     "identificacion_moderna": "Acacia tortuosa (van Buurt 2014 §6)",
     "van_buurt": "§6 hubada (A), hobada (B); topónimo Hubada en Aruba (§7)",
     "nivel": "A", "razon": "voz viva en Aruba y Bonaire, en la sección 6 de van Buurt "
     "(probablemente caquetío) y respaldada por el topónimo homónimo. Planta xerófila "
     "local: el campo semántico más discriminante del protocolo §4.1"},
    {"forma": "tarabada", "sec": "arboles", "glosa_fuente": "segundo elemento de 'hubada tarabada'",
     "nivel": "C", "razon": "van Buurt atestigua *hubada* sola; el segundo elemento no "
     "reaparece en ninguna fuente. Podría ser un epíteto o un error de campo de Pinart. "
     "Cf. el topónimo arubano Tarabana y Taratata/Tatarata"},

    # ── Names of plants ───────────────────────────────────────────────
    {"forma": "dividivi", "sec": "plantas", "glosa_fuente": "fruit of Sapindus coriaria",
     "identificacion_moderna": "Libidibia coriaria (syn. Caesalpinia coriaria) — Gatschet "
     "la puso en Sapindus, género equivocado",
     "van_buurt": "§6 dividivi (A,C,B): originalmente el FRUTO del watapana",
     "nivel": "A", "razon": "van Buurt §6 + topónimo arubano Sividivi + ya en el lexicón "
     "por vía continental (Zavala #112 'dividive'). La pareja fruto/árbol dividivi~watapana "
     "está viva en las tres islas"},
    {"forma": "jobo", "sec": "plantas", "glosa_fuente": "Spondias lutea",
     "identificacion_moderna": "Spondias mombin",
     "nivel": "D", "filtro": "4 — antillanismo panamericano",
     "razon": "*jobo* es taíno incorporado al español general (DRAE) y usado desde Cuba "
     "hasta el Perú. Sin valor probatorio para el caquetío insular"},
    {"forma": "kaduski", "sec": "plantas", "ocr_alt": "kaduslii (biostor)",
     "glosa_fuente": "Oereus laniginosus — OCR corregido a *Cereus laniginosus* por el "
     "OCR de BioStor, que lee 'Cereus' limpio",
     "identificacion_moderna": "Pilosocereus lanuginosus (Cereus lanuginosus es su basiónimo)",
     "van_buurt": "§6 kadushi (C,B) / cadushi (A) = Cereus repandus; §11 foño/funfun (B) "
     "= Pilocereus lanuginosus",
     "nivel": "A", "razon": "la FORMA es caquetío atestiguado triple: continental (caduchi/"
     "caduche en Paraguaná), insular 1882 (Pinart) y viva (van Buurt). Van Buurt además "
     "argumenta que la variante insular con /ʃi/ es más original que la continental. "
     "⚠️ CONFLICTO DE REFERENTE (D7): tres cactus distintos bajo el mismo nombre — "
     "Gatschet=Pilosocereus lanuginosus, van Buurt=Cereus repandus, lexicón del proyecto"
     "=Cereus hexagonus. El nombre es un genérico de cardón, no una especie"},
    {"forma": "kipopo", "sec": "plantas", "glosa_fuente": "Agaricus",
     "identificacion_moderna": "hongo agaricoide, sin especie determinable",
     "nivel": "C", "razon": "sobrevive los descartes; forma reduplicada; pero sin cognado, "
     "sin atestación externa y con un 'taxón' que es solo un género de hongos"},
    {"forma": "lokiloki", "sec": "plantas", "glosa_fuente": "Mimosa unguiscata",
     "identificacion_moderna": "Pithecellobium unguis-cati (Mimosa unguis-cati es sinónimo)",
     "nivel": "C", "razon": "campo semántico local y reduplicación (que el propio Gatschet "
     "señala como rasgo de la lengua), pero sin cognado ni atestación externa. "
     "⚠️ nombra LA MISMA especie que dabaraida en esta misma lista: uno de los dos "
     "registros de campo de Pinart tiene que estar mal"},
    {"forma": "makura", "sec": "plantas", "glosa_fuente": "Abrus precatorius",
     "identificacion_moderna": "Abrus precatorius (identificación correcta y estable)",
     "van_buurt": "§6 makurá (C,B), 'jumby beans'",
     "nivel": "B", "razon": "van Buurt §6 + etimología lokono propuesta (*ikira* 'lágrimas', "
     "*ma-kira* 'sin lágrimas, secar'). Se queda en B y no sube a A porque no hay respaldo "
     "toponímico ni atestación colonial, y la etimología lokono es del propio van Buurt, "
     "marcada por él como posible ('there may exist a relation')"},
    {"forma": "nandu", "sec": "plantas", "glosa_fuente": "Cytisus catjan",
     "identificacion_moderna": "Cajanus cajan (guandú, quinchoncho) — leguminosa del "
     "Viejo Mundo",
     "nivel": "D", "filtro": "5 — africanismo",
     "razon": "DOBLE descarte. (a) La especie es asiático-africana, introducida: no puede "
     "tener nombre precontacto en Aruba. (b) La forma es el papiamento *wandu*, del "
     "kimbundu/bantú *wandu*. Es exactamente el tipo de voz que van Buurt explica cuando "
     "dice que la mezcla temprana con población de origen africano 'can explain some of "
     "the African words found in the Indian wordlist compiled by Pinart in Aruba'"},
    {"forma": "shimaruko", "sec": "plantas", "ocr_alt": "sliimaruko (biostor)",
     "glosa_fuente": "Malpighia glabra",
     "identificacion_moderna": "Malpighia emarginata (semeruco, acerola)",
     "van_buurt": "§6 shimarucu (A), shimaruku (C,B)",
     "nivel": "A", "razon": "van Buurt §6 + forma continental atestiguada (cemaruco, "
     "semerúca en Venezuela) + cognado lokono *seme* 'dulce'. Van Buurt argumenta que "
     "shimaruku es MÁS original que semaruco, porque el español no genera /ʃi/. "
     "Insular + continental + cognado: el patrón completo"},
    {"forma": "surun", "sec": "plantas", "ocr_alt": "Oratera gynandra (JSTOR) / Gratera gynandra (BioStor)",
     "glosa_fuente": "Oratera/Gratera gynandra — reconstruido como *Crateva gynandra* L.",
     "identificacion_moderna": "Crateva tapia (Crateva gynandra es su sinónimo)",
     "van_buurt": "§6 ishiri (B), 'also called Surun'",
     "nivel": "A", "razon": "el taxón, ilegible en los dos OCR por separado, se reconstruye "
     "cruzándolos (*Crateva gynandra*) y **van Buurt lo confirma de forma independiente**: "
     "su entrada ishiri dice literalmente 'also called Surun' y le asigna Crateva tapia, "
     "que es la misma planta. Ejemplo de libro de por qué se usan los dos OCR"},
    {"forma": "takamahak", "sec": "plantas", "glosa_fuente": "Ragara octandra (probable "
     "errata de *Fagara octandra*, hoy Zanthoxylum)",
     "identificacion_moderna": "incierta; el nombre designa resinas de varios géneros "
     "(Calophyllum, Bursera, Protium)",
     "nivel": "D", "filtro": "4 — voz panamericana de circulación europea",
     "razon": "*tacamahaca* es voz náhuatl (*tecomahiyac*) que entró al español, al "
     "francés y a la farmacopea europea del s. XVIII como nombre de resina medicinal. "
     "Llegó a Aruba por el comercio, no por sustrato"},
    {"forma": "tuturutu", "sec": "plantas", "glosa_fuente": "Bobinia/Robinia pulcherrima "
     "— BioStor lee 'Robinia', que es la lectura correcta",
     "identificacion_moderna": "Caesalpinia pulcherrima (clavellino, flamboyán enano)",
     "nivel": "B", "razon": "la forma está atestiguada en el continente por Zavala #264 "
     "('tuturutos', hierba emética usada para cuajar quesos) y aquí en la isla por Pinart. "
     "⚠️ referentes distintos: Zavala describe una hierba, Gatschet un arbusto ornamental. "
     "Coincidencia de forma sin coincidencia de referente = B, no A"},
    {"forma": "watapana", "sec": "plantas", "glosa_fuente": "Sapindus coriaria",
     "identificacion_moderna": "Libidibia coriaria (syn. Caesalpinia coriaria) — el árbol "
     "del dividivi; Gatschet repite aquí el género equivocado (Sapindus)",
     "van_buurt": "§6 watapana (A,C,B), el ÁRBOL; dividivi es su fruto",
     "nivel": "A", "razon": "van Buurt §6 + argumento fonológico suyo (watapana es más "
     "original que el continental *guatapaná*, porque el español sustituye /w/ por /gw/) "
     "+ topónimos falconianos. **Cierra una de las 82 entradas sin cita del lexicón.**"},
    {"forma": "yoroyoro", "sec": "plantas", "glosa_fuente": "Thereiia/Theretia neriflora "
     "— reconstruido como *Thevetia neriifolia*",
     "identificacion_moderna": "Cascabela thevetia (syn. Thevetia peruviana)",
     "nivel": "C", "razon": "reduplicación y campo semántico local, pero sin cognado ni "
     "atestación externa; no aparece en van Buurt"},

    # ── Names of fish ─────────────────────────────────────────────────
    {"forma": "ginga", "sec": "peces", "glosa_fuente": "Diodon atinga",
     "identificacion_moderna": "Diodon hystrix (pez erizo)",
     "nivel": "C", "razon": "sospechosa de ser el propio epíteto *atinga*, que es tupí, "
     "recortado; sin atestación externa"},
    {"forma": "karma-u", "sec": "peces", "glosa_fuente": "Characinus cyprinioides",
     "identificacion_moderna": "incierta; cf. van Buurt karawau = Peprilus paru (palometa)",
     "van_buurt": "§11 karawau (vínculo MENOS cierto)",
     "nivel": "C", "razon": "posible correspondencia con *karawau*, pero van Buurt la pone "
     "en su sección 11 (vínculo menos cierto) y el taxón de Gatschet (un carácido de agua "
     "dulce) es imposible en una isla árida sin ríos: la identificación de 1885 es errónea"},
    {"forma": "kurkur", "sec": "peces", "ocr_alt": "Ohmtodon (JSTOR) / Chcetodon (BioStor)",
     "glosa_fuente": "Chaetodon fromitus (reconstruido cruzando los dos OCR)",
     "identificacion_moderna": "Chaetodon sp. (pez mariposa)",
     "nivel": "C", "razon": "reduplicación onomatopéyica; sin atestación externa"},
    {"forma": "puruntsi", "sec": "peces", "ocr_alt": "purnntsi (biostor); 'purantsi' en la "
     "cita de van Buurt",
     "glosa_fuente": "Serranus variolosus",
     "identificacion_moderna": "Cephalopholis cruentata y Epinephelus fulvus (los dos meros "
     "que hoy se llaman purunchi)",
     "van_buurt": "§11 purunchi (A,C,B) — vínculo MENOS cierto",
     "nivel": "C", "razon": "**es la entrada exacta sobre la que van Buurt formula su "
     "advertencia**: cita a Pinart y añade que 'this list contains several words which are "
     "definitely not Indian'. La voz está viva en las tres islas, pero su propio "
     "compilador moderno la degrada a la sección 11"},

    # ── Names of birds ────────────────────────────────────────────────
    {"forma": "kinikini", "sec": "aves", "glosa_fuente": "Cymindes illigeri",
     "identificacion_moderna": "Falco sparverius (cernícalo americano)",
     "van_buurt": "§11 kinikini — vínculo MENOS cierto",
     "nivel": "C", "razon": "voz viva, reduplicada y onomatopéyica (el cernícalo hace "
     "'kili-kili'), lo que explica igual de bien un origen imitativo independiente. "
     "Van Buurt la degrada a la sección 11"},
    {"forma": "krabete", "sec": "aves", "ocr_alt": "Fuliea (JSTOR) / Falica (BioStor)",
     "glosa_fuente": "Fulica —? (la propia fuente deja la especie sin cerrar)",
     "identificacion_moderna": "Fulica sp. (focha); Aruba carece de humedales permanentes, "
     "así que la identificación es dudosa",
     "nivel": "C", "razon": "grupo consonántico inicial /kr-/ atípico del perfil arahuaco; "
     "la propia fuente no cierra la especie; ninguna atestación posterior. Sospechosa de "
     "romance o neerlandés, sin poder demostrarlo"},
    {"forma": "shushubi", "sec": "aves", "ocr_alt": "shusliubi (biostor)",
     "glosa_fuente": "Orpheus amerieanus — corregido a *Orpheus americanus* (nombre "
     "decimonónico de los sinsontes)",
     "identificacion_moderna": "Mimus gilvus (paraulata llanera / tropical mockingbird)",
     "van_buurt": "§6 chuchubi (A,C,B) = Mimus gilvus",
     "nivel": "A", "razon": "TRIPLE atestación: continental (Zavala #85 'chuchube', "
     "paraulata), insular 1882 (Pinart 'shushubi') y viva (van Buurt 'chuchubi'). "
     "La alternancia sh~ch es exactamente la correspondencia insular/continental que "
     "van Buurt describe. **Cierra `chuchubi` de las 82 sin cita.**"},
    {"forma": "warawara", "sec": "aves", "ocr_alt": "Oathartes (los dos OCR)",
     "glosa_fuente": "Cathartes curasoica",
     "identificacion_moderna": "**Caracara cheriway** (syn. Polyborus plancus), el caracara "
     "crestado — NO un buitre del género Cathartes",
     "van_buurt": "§6 warawara (A,C,B) = crested Caracara; topónimos Warawara (Sero) y "
     "Warawao en Aruba",
     "nivel": "A", "razon": "van Buurt §6 + doble respaldo toponímico + registro en el "
     "propio papiamento de 1885 que Gatschet transcribe ('gavilán → guaraguara'), donde "
     "se ve la w→gu castellanizante. **Cierra `warawara` de las 82.** "
     "⚠️ Y DESTAPA UN ERROR VIVO EN EL LEXICÓN: `warawara` está glosada allí como "
     "'buitre, zamuro (Cathartes curasoica)' — es decir, el proyecto copió la "
     "identificación de Gatschet de 1885 sin saber que venía de él. Es un caracara "
     "(Falconidae), no un zamuro (Cathartidae)"},

    # ── Insects and other animals ─────────────────────────────────────
    {"forma": "dori", "sec": "animales", "ocr_alt": "Rana (JSTOR) / liana (BioStor)",
     "glosa_fuente": "Rana (—?)",
     "identificacion_moderna": "Pleurodema brachyops (sapito lipón / four-eyed frog)",
     "van_buurt": "§6 dori, dori maco (A,C,B)",
     "nivel": "A", "razon": "van Buurt §6, con dato clave: el nombre NACE en Aruba y de "
     "allí pasa a las otras dos islas, y está atestiguado en una copla arubana anotada por "
     "el profesor Martin hacia 1883 — es decir, **testimonio independiente y contemporáneo "
     "de Pinart**. La especie es nativa de Aruba y fue introducida en Curazao (1910) y "
     "Bonaire (1928): la dirección de préstamo confirma el origen insular occidental"},
    {"forma": "guruguru", "sec": "animales", "ocr_alt": "Calandra (JSTOR) / Oalandra (BioStor)",
     "glosa_fuente": "Calandra granaria (a beetle)",
     "identificacion_moderna": "Sitophilus granarius, el gorgojo del granero — insecto del "
     "Viejo Mundo, plaga de grano almacenado",
     "nivel": "D", "filtro": "1 — español / referente introducido",
     "razon": "DOBLE descarte. (a) La especie es paleártica y llega con el grano europeo: "
     "no hay nombre precontacto para ella. (b) La forma es una reduplicación onomatopéyica "
     "que remite al español *gorgojo* (y a *gorgorear*)"},
    {"forma": "hanahana", "sec": "animales", "ocr_alt": "hanakana (biostor) / hanahaua",
     "glosa_fuente": "Formica cephalota",
     "identificacion_moderna": "Atta cephalotes (bachaco cortador) — pero Atta no habita "
     "Aruba, así que la identificación decimonónica es muy dudosa",
     "nivel": "C", "razon": "es la SEGUNDA (y última) analogía comparativa que Gatschet "
     "encuentra, y es con el caribe insular (*hage* 'hormiga', Breton 1665), no con una "
     "lengua arahuaca — apunta a contacto caribe, no a herencia caquetía. Además el "
     "lexicón ya tiene `koke` (Zavala) para Atta spp. en el continente: dos formas "
     "distintas para el mismo referente"},
    {"forma": "kimakima", "sec": "animales", "ocr_alt": "Oassiopea (los dos OCR)",
     "glosa_fuente": "Cassiopea frondosa (a rhizopod)",
     "identificacion_moderna": "Cassiopea frondosa, medusa invertida — **no es un rizópodo**: "
     "el error zoológico es de Gatschet",
     "nivel": "C", "razon": "reduplicación; sin cognado ni atestación externa. Se conserva "
     "porque nombra fauna marina local, que es el campo de mayor rendimiento del protocolo"},
    {"forma": "kumexen", "sec": "animales", "glosa_fuente": "Termes fatalis",
     "identificacion_moderna": "Nasutitermes sp. (comején de nido arbóreo)",
     "nivel": "D", "filtro": "4 — antillanismo panamericano",
     "razon": "es *comején* en la ortografía afrancesada de Pinart (x = /x/). *Comején* es "
     "voz taína incorporada al español general (DRAE) y de uso en toda la Venezuela "
     "hispanohablante. No es evidencia de arubano"},
    {"forma": "lembelembe", "sec": "animales", "ocr_alt": "Conops (JSTOR) / Oonops (BioStor)",
     "glosa_fuente": "Conops sanguisuga (a dipteron)",
     "identificacion_moderna": "incierta; *Conops sanguisuga* no es un nombre aceptado",
     "nivel": "C", "razon": "reduplicación; la raíz *lembe* coincide con el papiamento "
     "*lembe* 'lamer' (de origen portugués/africano), lo que la deja bajo sospecha del "
     "filtro 2/5 sin poder cerrarla"},
    {"forma": "mamondenga", "sec": "animales", "glosa_fuente": "Ichneumon niger",
     "identificacion_moderna": "avispa icneumónida indeterminada",
     "nivel": "D", "filtro": "5 — africanismo",
     "razon": "estructura bantú transparente (prefijo ma- + -ndenga, cf. -nga en waidanga). "
     "Es del grupo que van Buurt explica: mezcla temprana con población de origen africano "
     "en Aruba metió palabras africanas en la lista de Pinart"},
    {"forma": "paluli", "sec": "animales", "glosa_fuente": "Mytilus edulis",
     "identificacion_moderna": "Brachidontes exustus, mejillón de manglar (Mytilus edulis "
     "es una especie del Atlántico norte, imposible en Aruba)",
     "van_buurt": "§6 palúli (C,B)",
     "nivel": "A", "razon": "van Buurt §6 y además **refuta explícitamente** la etimología "
     "romance que se le había propuesto (francés *palourde*), con dos argumentos: en las "
     "Antillas francesas *palourde* designa otro grupo de conchas (Codakia), y casi no hay "
     "nombres de fauna local del papiamento que vengan del francés. Un descarte ya "
     "intentado y fallido por un tercero vale más que un descarte no intentado"},
    {"forma": "waltaka", "sec": "animales", "ocr_alt": "ival taka (biostor)",
     "glosa_fuente": "lizard (sin taxón en la fuente)",
     "identificacion_moderna": "Anolis lineatus (van Buurt 2014 §6, s.v. waltaca)",
     "van_buurt": "§6 waltaca (A) = Anolis lineatus; topónimo Urataka (Sero)",
     "nivel": "A", "razon": "van Buurt §6, con dato de distribución: *waltaca* se usa SOLO "
     "en Aruba (en Curazao el mismo animal es *totèki* o *kaku*). Distribución restringida "
     "= criterio 2 del protocolo §4, el que separa sustrato local de préstamo difundido"},
]

# ── Topónimos (T): canon, NO habla ────────────────────────────────────
# forma reconciliada → (tipo, lectura alternativa del otro OCR, forma viva en
# van Buurt 2014 §7/§8 o "" si no reaparece)
TOPONIMOS: dict[str, tuple] = {
    # montañas y alturas
    "Aiyo":        ("montaña", "", "Ayo"),
    "Behika":      ("montaña", "Beliika", "Behika, Behuko"),
    "Cukuroi":     ("montaña", "", "Kukurui"),
    "Handebirari": ("montaña", "", ""),
    "Kasiaari":    ("montaña", "Kasinari (biostor)", "Kadiwari (?)"),
    "Kibaima":     ("montaña", "", "Kimbaima, Kibaima"),
    "Kodekodektu": ("montaña", "Ivodekodektu (biostor)", "Kodekodectu"),
    "Matividiri":  ("montaña", "Malividiri (JSTOR, errata) / Matlvidiri (biostor)",
                    "Matividiri — y en Paraguaná el cerro y caserío **Matividiro**"),
    "Shabururi":   ("montaña", "Shabaruri (JSTOR) / Sliabururi (biostor)", "Shabururi, Shabiburi"),
    "Shiribana":   ("montaña", "Sbiribana (biostor)", "Shiribana, Siribana, Shishiribana"),
    "Tarabana":    ("montaña", "", "Tarabana"),
    "Wakubana":    ("montaña", "", "Wakubana, Wacobana (mapa de 1825)"),
    "Yabarubari":  ("montaña", "", "Jaburibari (Seru)"),
    "Yamanota":    ("montaña", "", "Yamanota (Sero)"),
    # cuevas
    "Matividiri (cueva)": ("cueva", "", "Matividiri"),
    "Warerukuri":  ("cueva", "Warerfikuri (biostor)", "Warerikiri"),
    "Waririkiri":  ("cueva", "", "Guadirikiri, Wadirikiri (Cueva)"),
    # lugares
    "Antikuri":    ("lugar", "", "Andicuri, Andicouri"),
    "Arikurari":   ("lugar", "", "Avikurari"),
    "Bedui":       ("lugar", "", "Budui (Boca)"),
    "Bushiribani": ("lugar", "Busliiribani (biostor); Gatschet marca '(?)'", "Bushiribana"),
    "Cubari":      ("lugar", "Cnbari (biostor)", "Caburi / Macubari (?)"),
    "Damari":      ("lugar", "Daman (biostor)", "Daimari, Damari (Rooi, Boca)"),
    "Hendieku":    ("lugar", "", ""),
    "Kamakuri":    ("lugar", "", "Camacuri"),
    "Kashiunti":   ("lugar", "Kasliiunti (biostor)", "Cashunti (Baranca)"),
    "Kausheati":   ("lugar", "", "Caushati (Sero)"),
    "Kassibari":   ("lugar", "", "Casibari — van Buurt lo etimologiza ka-siba-rí "
                    "'ahí hay rocas duras'"),
    "Wariruri":    ("lugar", "", "Wariruri"),
    "Weburi":      ("lugar", "AVeburi (biostor)", "Weburi"),
    "Yuditi":      ("lugar", "", "Juditi / Yuwiti, Yuiti / Uditi"),
}

# ── Fórmulas de hechicería (R): texto no traducible, valor ritual ─────
# Pinart insistió a Gatschet en que son citas literales de la lengua arubana
# extinta, no sílabas sin sentido; no consiguió traducción palabra por palabra.
FORMULAS: list[dict] = [
    {"uso": "maledicción", "texto": "xerebete den kafa magolotchi",
     "ocr": "JSTOR lee ',\\-erebete'; BioStor lee 'xerebete' — se toma BioStor",
     "nota": "contiene `kafa` (diablo), que está en la lista de nombres"},
    {"uso": "asustar niños", "texto": "tue daye datie' gidio' dimi gurio yatabo",
     "ocr": "coinciden los dos OCR",
     "nota": "contiene `datie` (¡fuera!), que está en la lista de nombres"},
    {"uso": "sacar espinas de cactus (1)",
     "texto": "una areya rafayete dudrea ebanero abono, caburo copudabo daburi",
     "ocr": "JSTOR 'copudabo' / BioStor 'copudado'; van Buurt cita 'copudado'",
     "nota": "van Buurt 2014 especula que `daburi` designa las espinas del cactus, "
             "por su relación con dabaruida/dabaraida y el lokono dabáda 'uña, garra'. "
             "Es el ÚNICO fragmento de las seis fórmulas con una glosa parcial propuesta"},
    {"uso": "sacar espinas de cactus (2)",
     "texto": "yuni roba rapebo tchaba na aripebo, duda banabo pebo, home daba burvo, "
              "damei bo bakuna, daodao fuda dada",
     "ocr": "JSTOR 'duda' / BioStor 'diida'",
     "nota": "Gatschet observa aquí 'some rhythm resembling assonance'"},
    {"uso": "sacar espinas de pescado de la garganta",
     "texto": "vidie pahidie, maranako tubara tchira deburro, hadiira karara",
     "ocr": "JSTOR 'pahidie/hadiira' / BioStor 'pakidie/liadara'",
     "nota": ""},
    {"uso": "cazar la iguana",
     "texto": "Sako den komanari manadi watapuna fafa na douere sadii na ditieri",
     "ocr": "JSTOR 'f&fa' / BioStor 'fafa'",
     "nota": "contiene `watapuna`, que el propio Gatschet relaciona con `watapana`"},
]

# ── Las 82 entradas del lexicón sin nota/cita: qué resuelve esta fuente ──
# palabra_lexicon → (forma en Gatschet o "", veredicto)
COBERTURA_82: dict[str, tuple[str, str]] = {
    "watapana": ("watapana", "RESUELTA — atestiguada en Aruba, 1882, con taxón"),
    "warawara": ("warawara", "RESUELTA — y con corrección: el taxón del lexicón "
                 "('Cathartes curasoica') es la identificación de Gatschet de 1885; "
                 "hoy es Caracara cheriway"),
    "chuchubi": ("shushubi", "RESUELTA — vía la variante insular con sh-"),
    "kadushi":  ("kaduski", "RESUELTA en la forma; el referente queda ABIERTO "
                 "(tres cactus distintos en tres fuentes)"),
    "kunuku":   ("cunucu", "RESUELTA — pero por la sección de PAPIAMENTO del artículo "
                 "('Muchas en el campo / jopi na cunucu', Guía de Curazao 1876), "
                 "no por la lista arubana"),
    "pauji":    ("pajuis", "NO RESUELTA — 'pauji' aparece como la voz ESPAÑOLA de la "
                 "columna izquierda ('pauji → pajuis'), no como voz arubana. "
                 "No sirve de cita caquetía"),
    "auyama":   ("pampuna", "NO RESUELTA — 'ahullama' aparece como voz española del "
                 "guía de conversación; el papiamento usa pampuna. No sirve de cita"),
    "tuqueque": ("", "NO EN GATSCHET — pero van Buurt 2014 §6 (s.v. waltaca) dice que "
                 "'totèki' deriva de 'tuqueque, tuteque, an Amerindian word used for "
                 "geckos in Venezuela'. Cita disponible, pero de F6, no de F4"),
    "chiriguare": ("", "NO EN GATSCHET como voz arubana; en la sección papiamento el "
                   "'gavilán' es *guaraguara* (= warawara), no *chiriguare*"),
}


# ══════════════════════════════════════════════════════════════════════
# 3. EXTRACCIÓN Y RECONCILIACIÓN DE LOS DOS OCR
# ══════════════════════════════════════════════════════════════════════

def norm(s: str) -> str:
    """minúsculas sin acentos ni signos, para comparar formas entre OCR."""
    s = (s or "").lower().strip()
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 -]", "", s)


def leer(ruta: str) -> str:
    with open(ruta, encoding="utf-8", errors="replace") as f:
        txt = f.read()
    # Los dos OCR parten palabras con guion de fin de línea ("Kodeko-\ndektu",
    # "Ya-\nbarubari"). Sin rejuntarlas, ningún topónimo largo se verifica.
    return re.sub(r"[-­]\s*\n\s*", "", txt)


def secciones(texto: str) -> dict[str, str]:
    """Corta el artículo en sus secciones. Devuelve {clave: texto}."""
    out: dict[str, str] = {}
    for clave, ini, fin in SECCIONES:
        m0 = re.search(ini, texto, re.IGNORECASE)
        if not m0:
            out[clave] = ""
            continue
        resto = texto[m0.end():]
        m1 = re.search(fin, resto, re.IGNORECASE)
        out[clave] = resto[:m1.start()] if m1 else resto[:4000]
    return out


def tokens(bloque: str) -> list[str]:
    """Palabras candidatas de un bloque, ya normalizadas."""
    limpio = re.sub(r"\b(Gatschet|July|PROC|AMER|PHILOS|SOC|PRINTED)\b", " ",
                    bloque, flags=re.IGNORECASE)
    return [norm(t) for t in re.findall(r"[A-Za-z][A-Za-z'^&\-]{2,}", limpio)]


def sostiene(forma: str, toks: list[str], umbral: float = 0.72) -> bool:
    """¿Este OCR sostiene esta forma? Tolerante al ruido (sh/sli, C/O, i/l...)."""
    objetivo = norm(forma).split()
    if not objetivo:
        return False
    cabeza = objetivo[0]
    if cabeza in toks:
        return True
    return any(difflib.SequenceMatcher(None, cabeza, t).ratio() >= umbral for t in toks)


def verificar_ocr() -> dict:
    """Comprueba cada forma curada contra los DOS OCR. Es la red de seguridad:
    si una forma no la sostiene ninguno, es que la transcribí mal."""
    txt_j, txt_b = leer(OCR_JSTOR), leer(OCR_BIOSTOR)
    sec_j, sec_b = secciones(txt_j), secciones(txt_b)
    tok_j = {k: tokens(v) for k, v in sec_j.items()}
    tok_b = {k: tokens(v) for k, v in sec_b.items()}

    res = {"formas": {}, "huerfanas": [], "secciones_vacias": []}
    for k, _, _ in SECCIONES:
        if not sec_j[k].strip() and not sec_b[k].strip():
            res["secciones_vacias"].append(k)

    todo = [(e["forma"], e["sec"]) for e in ENTRADAS]
    todo += [(t.split(" (")[0], {"montaña": "montanas", "cueva": "cuevas",
                                 "lugar": "lugares"}[v[0]])
             for t, v in TOPONIMOS.items()]
    for forma, sec in todo:
        j = sostiene(forma, tok_j.get(sec, []))
        b = sostiene(forma, tok_b.get(sec, []))
        res["formas"][forma] = {"jstor": j, "biostor": b}
        if not (j or b):
            res["huerfanas"].append(forma)
    return res


# ══════════════════════════════════════════════════════════════════════
# 4. CRUCE CON EL LEXICÓN ACTIVO
# ══════════════════════════════════════════════════════════════════════

# Correspondencias ortográficas usadas para comparar Gatschet ↔ lexicón.
# Gatschet/Pinart escriben con convenciones inglesas y francesas del s. XIX.
NORMALIZACION_ORTOGRAFICA = [
    (r"^sh", "ch"),      # shushubi ↔ chuchubi   (van Buurt: la insular con /ʃi/ es la original)
    (r"ski$", "shi"),    # kaduski  ↔ kadushi
    (r"^k", "c"),        # kaduski  ↔ cadushi (grafía arubana)
    (r"u$", "o"),        # tuturutu ↔ tuturutos (continental, Zavala)
    (r"i$", "e"),        # dividivi ↔ dividive  (continental, Zavala)
]


def variantes(forma: str) -> list[str]:
    """Formas ortográficas equivalentes a probar contra el lexicón."""
    base = norm(forma).replace(" ", "")
    out = {base}
    for patron, reemplazo in NORMALIZACION_ORTOGRAFICA:
        out.add(re.sub(patron, reemplazo, base))
    return sorted(out)


def cruzar_lexicon() -> dict:
    try:
        from curiana_lexicon import VOCABULARIO_BASE
    except Exception as exc:                                  # pragma: no cover
        print(f"  ⚠ no se pudo importar el lexicón ({exc}); se omite el cruce")
        return {}
    idx = {norm(w).replace(" ", ""): (w, e) for w, e in VOCABULARIO_BASE.items()}
    out = {}
    for e in ENTRADAS:
        for v in variantes(e["forma"]):
            if v in idx:
                w, ent = idx[v]
                out[e["forma"]] = {
                    "lema_lexicon": w,
                    "sig": ent.get("sig", ""),
                    "fuente": ent.get("fuente", ""),
                    "notas": ent.get("notas", ""),
                    "sin_cita": not ent.get("notas"),
                }
                break
    return out


# ══════════════════════════════════════════════════════════════════════
# 5. ¿VALIDAN LOS TOPÓNIMOS LOS AFIJOS DE ZAVALA?
# ══════════════════════════════════════════════════════════════════════

def afijos_en_toponimos() -> dict:
    """Cuenta los afijos de REGLAS_ZAVALA (+ -bana locativo) en los 31 topónimos
    arubanos. Confirmación cruzada independiente: Zavala compila Falcón
    continental; Pinart recoge Aruba insular."""
    nombres = [t.split(" (")[0] for t in TOPONIMOS]
    sondas = {
        "-iro":   r"iro$",
        "-aima":  r"aima$",
        "-ima":   r"[^a]ima$",
        "-uco":   r"u[ck]o$",
        "-ubana": r"ubana$",
        "-uru":   r"ur[uoi]$|uri$",
        "-bana":  r"bana$|bani$",       # locativo del proyecto (REGLAS_LOCATIVAS)
    }
    out = {}
    for afijo, patron in sondas.items():
        hits = [n for n in nombres if re.search(patron, norm(n))]
        out[afijo] = hits
    # Sufijos frecuentes que el proyecto NO tiene codificados
    extra = {}
    for patron, etiqueta in ((r"kuri$|curi$", "-kuri/-curi"),
                             (r"bari$", "-bari"),
                             (r"[dk]iri$|kiri$", "-kiri/-diri"),
                             (r"ari$", "-ari")):
        hits = [n for n in nombres if re.search(patron, norm(n))]
        if hits:
            extra[etiqueta] = hits
    return {"reglas_del_proyecto": out, "no_codificados": extra}


# ══════════════════════════════════════════════════════════════════════
# 6. INFORME
# ══════════════════════════════════════════════════════════════════════

_ETIQ = {
    "A": "Atestiguada — candidata a `caquetío-atestiguado` tras revisión humana",
    "B": "Fuerte — corpus cultural sí; lexicón activo NO sin decisión explícita",
    "C": "Plausible — solo corpus, marcada; NUNCA al lexicón activo",
    "D": "Descartada — cae en un filtro; se documenta con su razón",
}


def informe():
    ver = verificar_ocr()
    lex = cruzar_lexicon()
    af = afijos_en_toponimos()

    n_lex = len(ENTRADAS)
    print("=" * 78)
    print("  GATSCHET 1885 — *The Aruba Language and the Papiamento Jargon*")
    print("  minado F4 · material de A. L. Pinart, Aruba 1882")
    print("=" * 78)
    print(f"  formas léxicas transcritas : {n_lex}")
    print(f"  topónimos                  : {len(TOPONIMOS)}")
    print(f"  fórmulas de hechicería     : {len(FORMULAS)}  "
          "(Gatschet dice 'six' en prosa y publica seis)")
    print(f"  TOTAL de formas            : {n_lex + len(TOPONIMOS)}")
    print()

    # ── verificación OCR ──
    solo_j = [f for f, v in ver["formas"].items() if v["jstor"] and not v["biostor"]]
    solo_b = [f for f, v in ver["formas"].items() if v["biostor"] and not v["jstor"]]
    print("── verificación contra los dos OCR " + "─" * 42)
    print(f"   sostenidas por ambos     : "
          f"{sum(1 for v in ver['formas'].values() if v['jstor'] and v['biostor'])}")
    print(f"   solo JSTOR               : {len(solo_j)}  {', '.join(solo_j[:6])}")
    print(f"   solo BioStor             : {len(solo_b)}  {', '.join(solo_b[:6])}")
    if ver["huerfanas"]:
        print(f"   ⚠ SIN respaldo en ningún OCR: {', '.join(ver['huerfanas'])}")
    else:
        print("   ✓ ninguna forma curada carece de respaldo en al menos un OCR")
    if ver["secciones_vacias"]:
        print(f"   ⚠ secciones no localizadas: {ver['secciones_vacias']}")
    print()

    # ── veredictos ──
    print("── veredictos (protocolo del habla paraguanera, §5) " + "─" * 26)
    for nivel in "ABCD":
        items = [e for e in ENTRADAS if e["nivel"] == nivel]
        print(f"\n  {nivel} · {len(items):2} formas — {_ETIQ[nivel]}")
        for e in items:
            marca = " ←lexicón" if e["forma"] in lex else ""
            filtro = f"  [filtro {e['filtro']}]" if e.get("filtro") else ""
            print(f"     {e['forma']:22} {e['glosa_fuente'][:40]:42}{marca}{filtro}")
    print()

    # ── cruce con lexicón ──
    print("── cruce con VOCABULARIO_BASE " + "─" * 47)
    if not lex:
        print("   (no disponible)")
    for f, d in sorted(lex.items()):
        estado = "SIN CITA" if d["sin_cita"] else "con nota"
        print(f"   {f:12} → {d['lema_lexicon']:12} [{d['fuente']}] {estado}")
        print(f"                  lexicón: {d['sig'][:60]}")
    print()

    # ── las 82 ──
    resueltas = [k for k, v in COBERTURA_82.items() if v[1].startswith("RESUELTA")]
    print("── cobertura de las 82 entradas sin cita " + "─" * 36)
    print(f"   resueltas por esta fuente: {len(resueltas)}/82  → {', '.join(resueltas)}")
    for p, (forma, ver_) in COBERTURA_82.items():
        if p not in resueltas:
            print(f"   {p:12} {ver_[:70]}")
    print()

    # ── afijos ──
    print("── ¿validan los topónimos arubanos los afijos de REGLAS_ZAVALA? " + "─" * 13)
    for afijo, hits in af["reglas_del_proyecto"].items():
        print(f"   {afijo:8} {len(hits):>3}  {', '.join(hits) if hits else '— sin apoyo'}")
    print("   sufijos frecuentes que el proyecto NO tiene codificados:")
    for etiqueta, hits in af["no_codificados"].items():
        print(f"   {etiqueta:14} {len(hits):2}  {', '.join(hits)}")
    print()

    # ── topónimos vs van Buurt ──
    vivos = [t for t, v in TOPONIMOS.items() if v[2]]
    print("── topónimos: cruce con van Buurt 2014 §7 " + "─" * 35)
    print(f"   siguen vivos y él los da como probablemente caquetíos: "
          f"{len(vivos)}/{len(TOPONIMOS)}")
    print("   los que NO reaparecen: "
          f"{', '.join(t for t, v in TOPONIMOS.items() if not v[2])}")
    print()
    print("=" * 78)


# ══════════════════════════════════════════════════════════════════════
# 7. GENERACIÓN DE LA PROPUESTA
# ══════════════════════════════════════════════════════════════════════

def _q(s: str) -> str:
    return (s or "").replace("\\", "").replace('"', "'")


def generar_modulo(ruta: str):
    lex = cruzar_lexicon()
    ver = verificar_ocr()
    af = afijos_en_toponimos()
    L: list[str] = []
    A = L.append

    A('"""')
    A("CURIANA — Propuesta de importación de Gatschet 1885 (material Pinart 1882)")
    A("=" * 72)
    A("")
    A("GENERADO por `minar_gatschet.py` — no editar a mano: reejecutar el script")
    A("si cambia la curación.")
    A("")
    A("    " + FUENTE_CITA)
    A("")
    A("ESTO NO ES LÉXICO ACTIVO. Es una propuesta con veredicto por forma, para")
    A("revisión humana. Ninguna entrada pasa a VOCABULARIO_BASE por este camino.")
    A("")
    A("Escala (protocolo `investigacion/disenos/02_protocolo_habla_paraguanera.md` §5):")
    A("  A — sobrevive los seis descartes y tiene atestación externa sólida")
    A("  B — sobrevive los descartes, campo local, cognado; corpus sí, lexicón no")
    A("  C — sobrevive los descartes pero con 1-2 criterios positivos; solo corpus")
    A("  D — cae en un filtro de descarte; se documenta la razón para no re-minarla")
    A("  T — topónimo: canon, fuera del habla     R — fórmula ritual: no léxico")
    A("")
    A("POLÍTICA D7 (Miguel, 2026-08-03): `glosa_fuente` conserva VERBATIM lo que")
    A("dice Gatschet, incluida su taxonomía de 1885 y sus erratas de OCR marcadas;")
    A("`identificacion_moderna` da el taxón actual cuando se pudo establecer.")
    A("Ninguna de las dos gana: se registran las dos.")
    A('"""')
    A("")
    A("")
    A("FUENTE = " + json.dumps(FUENTE_CITA, ensure_ascii=False))
    A("")
    A("")
    A("# " + "═" * 70)
    A("# VOCABULARIO — por veredicto")
    A("# " + "═" * 70)
    A("")
    A("GATSCHET_VOCABULARIO: dict[str, dict] = {")
    for nivel in "ABCD":
        items = [e for e in ENTRADAS if e["nivel"] == nivel]
        A("")
        A(f"    # ── nivel {nivel} ({len(items)}) — {_ETIQ[nivel]} ──")
        for e in sorted(items, key=lambda x: x["forma"]):
            v = ver["formas"].get(e["forma"], {})
            ocr = "ambos" if v.get("jstor") and v.get("biostor") else (
                "jstor" if v.get("jstor") else "biostor" if v.get("biostor") else "ninguno")
            A(f'    "{e["forma"]}": {{')
            A(f'        "seccion": "{e["sec"]}",')
            A(f'        "glosa_fuente": "{_q(e["glosa_fuente"])}",')
            if e.get("identificacion_moderna"):
                A(f'        "identificacion_moderna": "{_q(e["identificacion_moderna"])}",')
            if e.get("ocr_alt"):
                A(f'        "lectura_alternativa_ocr": "{_q(e["ocr_alt"])}",')
            A(f'        "ocr_que_la_sostiene": "{ocr}",')
            if e.get("van_buurt"):
                A(f'        "van_buurt_2014": "{_q(e["van_buurt"])}",')
            if e["forma"] in lex:
                d = lex[e["forma"]]
                A(f'        "ya_en_lexicon": "{d["lema_lexicon"]}",')
                A(f'        "lexicon_fuente": "{d["fuente"]}",')
                A(f'        "lexicon_sin_cita": {d["sin_cita"]},')
            A(f'        "nivel": "{e["nivel"]}",')
            if e.get("filtro"):
                A(f'        "filtro_de_descarte": "{_q(e["filtro"])}",')
            A(f'        "razon": "{_q(e["razon"])}",')
            A("    },")
    A("}")
    A("")
    A("")
    A("# " + "═" * 70)
    A("# T — TOPÓNIMOS ARUBANOS: canon y morfología, NO habla")
    A("# " + "═" * 70)
    A("# Un agente no dice 'Yamanota' para decir 'monte'. Se conservan porque son")
    A("# morfología caquetía viva y porque van Buurt 2014 §7 los da, casi todos,")
    A("# como topónimos probablemente caquetíos que siguen en uso.")
    A("")
    A("GATSCHET_TOPONIMOS: dict[str, dict] = {")
    for t, (tipo, alt, vb) in TOPONIMOS.items():
        A(f'    "{t}": {{"tipo": "{tipo}", "lectura_alternativa_ocr": "{_q(alt)}", '
          f'"van_buurt_2014": "{_q(vb)}"}},')
    A("}")
    A("")
    A("")
    A("# " + "═" * 70)
    A("# R — FÓRMULAS DE HECHICERÍA: texto no traducible, valor ritual")
    A("# " + "═" * 70)
    A("# Pinart insistió a Gatschet en que son citas literales de la lengua arubana")
    A("# extinta, y no consiguió traducción palabra por palabra. NO son léxico: no")
    A("# se segmentan, no se glosan y no puntúan. Su valor es para el habla del")
    A("# piache (ver mocs/MOC_creencia.md), como registro ritual opaco.")
    A("")
    A("GATSCHET_FORMULAS: list[dict] = [")
    for f in FORMULAS:
        A("    {")
        A(f'        "uso": "{_q(f["uso"])}",')
        A(f'        "texto": "{_q(f["texto"])}",')
        A(f'        "reconciliacion_ocr": "{_q(f["ocr"])}",')
        A(f'        "nota": "{_q(f["nota"])}",')
        A('        "etiqueta": "ritual-no-traducible",')
        A("    },")
    A("]")
    A("")
    A("")
    A("# " + "═" * 70)
    A("# COBERTURA DE LAS 82 ENTRADAS DEL LEXICÓN SIN CITA (tarea F1)")
    A("# " + "═" * 70)
    A("")
    A("COBERTURA_82: dict[str, dict] = {")
    for p, (forma, verd) in COBERTURA_82.items():
        A(f'    "{p}": {{"forma_en_gatschet": "{_q(forma)}", "veredicto": "{_q(verd)}"}},')
    A("}")
    A("")
    A("")
    A("# " + "═" * 70)
    A("# AFIJOS: ¿confirman los topónimos arubanos a REGLAS_ZAVALA?")
    A("# " + "═" * 70)
    A("# Confirmación cruzada independiente: Zavala compila Falcón continental,")
    A("# Pinart recoge Aruba insular en 1882. Si los mismos afijos aparecen en los")
    A("# dos corpus, el afijo es de la lengua y no del compilador.")
    A("")
    A("AFIJOS_EN_TOPONIMOS: dict[str, list] = {")
    for afijo, hits in af["reglas_del_proyecto"].items():
        A(f'    "{afijo}": {json.dumps(hits, ensure_ascii=False)},')
    A("}")
    A("")
    A("# Sufijos frecuentes en los topónimos que el proyecto NO tiene codificados:")
    A("SUFIJOS_NO_CODIFICADOS: dict[str, list] = {")
    for etiqueta, hits in af["no_codificados"].items():
        A(f'    "{etiqueta}": {json.dumps(hits, ensure_ascii=False)},')
    A("}")
    A("")
    A("")
    A("TOTALES = {")
    for nivel in "ABCD":
        A(f'    "nivel_{nivel}": {sum(1 for e in ENTRADAS if e["nivel"] == nivel)},')
    A(f'    "toponimos": {len(TOPONIMOS)},')
    A(f'    "formulas": {len(FORMULAS)},')
    A(f'    "formas_totales": {len(ENTRADAS) + len(TOPONIMOS)},')
    A("}")
    A("")

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"  → módulo generado: {ruta}")
    for nivel in "ABCD":
        print(f"     nivel {nivel}: {sum(1 for e in ENTRADAS if e['nivel'] == nivel)}")
    print(f"     topónimos: {len(TOPONIMOS)}   fórmulas: {len(FORMULAS)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Minado de Gatschet 1885 (F4)")
    ap.add_argument("--json", metavar="RUTA", help="volcar la clasificación a JSON")
    ap.add_argument("--generar-modulo", nargs="?", const="lexicon_gatschet.py",
                    metavar="RUTA", help="escribir lexicon_gatschet.py con la propuesta")
    args = ap.parse_args()

    if args.generar_modulo:
        ruta = args.generar_modulo
        if not os.path.isabs(ruta):
            ruta = os.path.join(_AQUI, ruta)
        generar_modulo(ruta)
    else:
        informe()

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"fuente": FUENTE_CITA, "entradas": ENTRADAS,
                       "toponimos": TOPONIMOS, "formulas": FORMULAS,
                       "cobertura_82": COBERTURA_82,
                       "verificacion_ocr": verificar_ocr(),
                       "afijos": afijos_en_toponimos(),
                       "cruce_lexicon": cruzar_lexicon()},
                      f, ensure_ascii=False, indent=2)
        print(f"\n  → JSON: {args.json}")
