"""
CURIANA — Propuesta de importación de Gatschet 1885 (material Pinart 1882)
========================================================================

GENERADO por `minar_gatschet.py` — no editar a mano: reejecutar el script
si cambia la curación.

    Gatschet 1885, Proc. Am. Philos. Soc. XXII(120):299-305 (material de A. L. Pinart, Aruba 1882)

ESTO NO ES LÉXICO ACTIVO. Es una propuesta con veredicto por forma, para
revisión humana. Ninguna entrada pasa a VOCABULARIO_BASE por este camino.

Escala (protocolo `investigacion/disenos/02_protocolo_habla_paraguanera.md` §5):
  A — sobrevive los seis descartes y tiene atestación externa sólida
  B — sobrevive los descartes, campo local, cognado; corpus sí, lexicón no
  C — sobrevive los descartes pero con 1-2 criterios positivos; solo corpus
  D — cae en un filtro de descarte; se documenta la razón para no re-minarla
  T — topónimo: canon, fuera del habla     R — fórmula ritual: no léxico

POLÍTICA D7 (Miguel, 2026-08-03): `glosa_fuente` conserva VERBATIM lo que
dice Gatschet, incluida su taxonomía de 1885 y sus erratas de OCR marcadas;
`identificacion_moderna` da el taxón actual cuando se pudo establecer.
Ninguna de las dos gana: se registran las dos.
"""


FUENTE = "Gatschet 1885, Proc. Am. Philos. Soc. XXII(120):299-305 (material de A. L. Pinart, Aruba 1882)"


# ══════════════════════════════════════════════════════════════════════
# VOCABULARIO — por veredicto
# ══════════════════════════════════════════════════════════════════════

GATSCHET_VOCABULARIO: dict[str, dict] = {

    # ── nivel A (12) — Atestiguada — candidata a `caquetío-atestiguado` tras revisión humana ──
    "dabaraida": {
        "seccion": "arboles",
        "glosa_fuente": "a tree (sin taxón en la fuente)",
        "identificacion_moderna": "Pithecellobium unguis-cati (van Buurt 2014 §6, s.v. dabaruida)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 dabaruida/yaga (A)",
        "nivel": "A",
        "razon": "TRIPLE atestación independiente: van Koolwijk 1880 (dabaroida), Pinart 1882 (dabaraida), van Buurt 2014 (dabaruida, forma viva). Y etimología arahuaca con correspondencia: lokono *dabáda* 'uña, garra' + *ida* 'rodeado de, piel' (De Goeje 1928), con paralelo shebayo de 1594-95 *dabodda/dabádoh* 'uña'. Es el mejor resultado de esta fuente",
    },
    "dividivi": {
        "seccion": "plantas",
        "glosa_fuente": "fruit of Sapindus coriaria",
        "identificacion_moderna": "Libidibia coriaria (syn. Caesalpinia coriaria) — Gatschet la puso en Sapindus, género equivocado",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 dividivi (A,C,B): originalmente el FRUTO del watapana",
        "ya_en_lexicon": "dividive",
        "lexicon_fuente": "caquetío-atestiguado",
        "lexicon_sin_cita": False,
        "nivel": "A",
        "razon": "van Buurt §6 + topónimo arubano Sividivi + ya en el lexicón por vía continental (Zavala #112 'dividive'). La pareja fruto/árbol dividivi~watapana está viva en las tres islas",
    },
    "dori": {
        "seccion": "animales",
        "glosa_fuente": "Rana (—?)",
        "identificacion_moderna": "Pleurodema brachyops (sapito lipón / four-eyed frog)",
        "lectura_alternativa_ocr": "Rana (JSTOR) / liana (BioStor)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 dori, dori maco (A,C,B)",
        "nivel": "A",
        "razon": "van Buurt §6, con dato clave: el nombre NACE en Aruba y de allí pasa a las otras dos islas, y está atestiguado en una copla arubana anotada por el profesor Martin hacia 1883 — es decir, **testimonio independiente y contemporáneo de Pinart**. La especie es nativa de Aruba y fue introducida en Curazao (1910) y Bonaire (1928): la dirección de préstamo confirma el origen insular occidental",
    },
    "hubada": {
        "seccion": "arboles",
        "glosa_fuente": "a tree (parte de 'hubada tarabada')",
        "identificacion_moderna": "Acacia tortuosa (van Buurt 2014 §6)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 hubada (A), hobada (B); topónimo Hubada en Aruba (§7)",
        "nivel": "A",
        "razon": "voz viva en Aruba y Bonaire, en la sección 6 de van Buurt (probablemente caquetío) y respaldada por el topónimo homónimo. Planta xerófila local: el campo semántico más discriminante del protocolo §4.1",
    },
    "kaduski": {
        "seccion": "plantas",
        "glosa_fuente": "Oereus laniginosus — OCR corregido a *Cereus laniginosus* por el OCR de BioStor, que lee 'Cereus' limpio",
        "identificacion_moderna": "Pilosocereus lanuginosus (Cereus lanuginosus es su basiónimo)",
        "lectura_alternativa_ocr": "kaduslii (biostor)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 kadushi (C,B) / cadushi (A) = Cereus repandus; §11 foño/funfun (B) = Pilocereus lanuginosus",
        "ya_en_lexicon": "kadushi",
        "lexicon_fuente": "caquetío-atestiguado",
        "lexicon_sin_cita": True,
        "nivel": "A",
        "razon": "la FORMA es caquetío atestiguado triple: continental (caduchi/caduche en Paraguaná), insular 1882 (Pinart) y viva (van Buurt). Van Buurt además argumenta que la variante insular con /ʃi/ es más original que la continental. ⚠️ CONFLICTO DE REFERENTE (D7): tres cactus distintos bajo el mismo nombre — Gatschet=Pilosocereus lanuginosus, van Buurt=Cereus repandus, lexicón del proyecto=Cereus hexagonus. El nombre es un genérico de cardón, no una especie",
    },
    "paluli": {
        "seccion": "animales",
        "glosa_fuente": "Mytilus edulis",
        "identificacion_moderna": "Brachidontes exustus, mejillón de manglar (Mytilus edulis es una especie del Atlántico norte, imposible en Aruba)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 palúli (C,B)",
        "nivel": "A",
        "razon": "van Buurt §6 y además **refuta explícitamente** la etimología romance que se le había propuesto (francés *palourde*), con dos argumentos: en las Antillas francesas *palourde* designa otro grupo de conchas (Codakia), y casi no hay nombres de fauna local del papiamento que vengan del francés. Un descarte ya intentado y fallido por un tercero vale más que un descarte no intentado",
    },
    "shimaruko": {
        "seccion": "plantas",
        "glosa_fuente": "Malpighia glabra",
        "identificacion_moderna": "Malpighia emarginata (semeruco, acerola)",
        "lectura_alternativa_ocr": "sliimaruko (biostor)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 shimarucu (A), shimaruku (C,B)",
        "nivel": "A",
        "razon": "van Buurt §6 + forma continental atestiguada (cemaruco, semerúca en Venezuela) + cognado lokono *seme* 'dulce'. Van Buurt argumenta que shimaruku es MÁS original que semaruco, porque el español no genera /ʃi/. Insular + continental + cognado: el patrón completo",
    },
    "shushubi": {
        "seccion": "aves",
        "glosa_fuente": "Orpheus amerieanus — corregido a *Orpheus americanus* (nombre decimonónico de los sinsontes)",
        "identificacion_moderna": "Mimus gilvus (paraulata llanera / tropical mockingbird)",
        "lectura_alternativa_ocr": "shusliubi (biostor)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 chuchubi (A,C,B) = Mimus gilvus",
        "nivel": "A",
        "razon": "TRIPLE atestación: continental (Zavala #85 'chuchube', paraulata), insular 1882 (Pinart 'shushubi') y viva (van Buurt 'chuchubi'). La alternancia sh~ch es exactamente la correspondencia insular/continental que van Buurt describe. **Cierra `chuchubi` de las 82 sin cita.**",
    },
    "surun": {
        "seccion": "plantas",
        "glosa_fuente": "Oratera/Gratera gynandra — reconstruido como *Crateva gynandra* L.",
        "identificacion_moderna": "Crateva tapia (Crateva gynandra es su sinónimo)",
        "lectura_alternativa_ocr": "Oratera gynandra (JSTOR) / Gratera gynandra (BioStor)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 ishiri (B), 'also called Surun'",
        "nivel": "A",
        "razon": "el taxón, ilegible en los dos OCR por separado, se reconstruye cruzándolos (*Crateva gynandra*) y **van Buurt lo confirma de forma independiente**: su entrada ishiri dice literalmente 'also called Surun' y le asigna Crateva tapia, que es la misma planta. Ejemplo de libro de por qué se usan los dos OCR",
    },
    "waltaka": {
        "seccion": "animales",
        "glosa_fuente": "lizard (sin taxón en la fuente)",
        "identificacion_moderna": "Anolis lineatus (van Buurt 2014 §6, s.v. waltaca)",
        "lectura_alternativa_ocr": "ival taka (biostor)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 waltaca (A) = Anolis lineatus; topónimo Urataka (Sero)",
        "nivel": "A",
        "razon": "van Buurt §6, con dato de distribución: *waltaca* se usa SOLO en Aruba (en Curazao el mismo animal es *totèki* o *kaku*). Distribución restringida = criterio 2 del protocolo §4, el que separa sustrato local de préstamo difundido",
    },
    "warawara": {
        "seccion": "aves",
        "glosa_fuente": "Cathartes curasoica",
        "identificacion_moderna": "**Caracara cheriway** (syn. Polyborus plancus), el caracara crestado — NO un buitre del género Cathartes",
        "lectura_alternativa_ocr": "Oathartes (los dos OCR)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 warawara (A,C,B) = crested Caracara; topónimos Warawara (Sero) y Warawao en Aruba",
        "ya_en_lexicon": "warawara",
        "lexicon_fuente": "caquetío-atestiguado",
        "lexicon_sin_cita": True,
        "nivel": "A",
        "razon": "van Buurt §6 + doble respaldo toponímico + registro en el propio papiamento de 1885 que Gatschet transcribe ('gavilán → guaraguara'), donde se ve la w→gu castellanizante. **Cierra `warawara` de las 82.** ⚠️ Y DESTAPA UN ERROR VIVO EN EL LEXICÓN: `warawara` está glosada allí como 'buitre, zamuro (Cathartes curasoica)' — es decir, el proyecto copió la identificación de Gatschet de 1885 sin saber que venía de él. Es un caracara (Falconidae), no un zamuro (Cathartidae)",
    },
    "watapana": {
        "seccion": "plantas",
        "glosa_fuente": "Sapindus coriaria",
        "identificacion_moderna": "Libidibia coriaria (syn. Caesalpinia coriaria) — el árbol del dividivi; Gatschet repite aquí el género equivocado (Sapindus)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 watapana (A,C,B), el ÁRBOL; dividivi es su fruto",
        "ya_en_lexicon": "watapana",
        "lexicon_fuente": "caquetío-atestiguado",
        "lexicon_sin_cita": True,
        "nivel": "A",
        "razon": "van Buurt §6 + argumento fonológico suyo (watapana es más original que el continental *guatapaná*, porque el español sustituye /w/ por /gw/) + topónimos falconianos. **Cierra una de las 82 entradas sin cita del lexicón.**",
    },

    # ── nivel B (2) — Fuerte — corpus cultural sí; lexicón activo NO sin decisión explícita ──
    "makura": {
        "seccion": "plantas",
        "glosa_fuente": "Abrus precatorius",
        "identificacion_moderna": "Abrus precatorius (identificación correcta y estable)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§6 makurá (C,B), 'jumby beans'",
        "nivel": "B",
        "razon": "van Buurt §6 + etimología lokono propuesta (*ikira* 'lágrimas', *ma-kira* 'sin lágrimas, secar'). Se queda en B y no sube a A porque no hay respaldo toponímico ni atestación colonial, y la etimología lokono es del propio van Buurt, marcada por él como posible ('there may exist a relation')",
    },
    "tuturutu": {
        "seccion": "plantas",
        "glosa_fuente": "Bobinia/Robinia pulcherrima — BioStor lee 'Robinia', que es la lectura correcta",
        "identificacion_moderna": "Caesalpinia pulcherrima (clavellino, flamboyán enano)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "B",
        "razon": "la forma está atestiguada en el continente por Zavala #264 ('tuturutos', hierba emética usada para cuajar quesos) y aquí en la isla por Pinart. ⚠️ referentes distintos: Zavala describe una hierba, Gatschet un arbusto ornamental. Coincidencia de forma sin coincidencia de referente = B, no A",
    },

    # ── nivel C (25) — Plausible — solo corpus, marcada; NUNCA al lexicón activo ──
    "aba dobo edan guayete": {
        "seccion": "nombres",
        "glosa_fuente": "sit down!",
        "lectura_alternativa_ocr": "aaba dobo^edaa guayete / A aba dobo^edan guayete",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "los DOS OCR están rotos en el mismo punto; la forma no es reconstruible con confianza. Se registra para que un tercer testimonio la resuelva",
    },
    "adamudu": {
        "seccion": "nombres",
        "glosa_fuente": "rain",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "sobrevive los seis descartes (no es español, papiamento, neerlandés, wayuu, taíno ni caribe conocido) pero no tiene ni cognado ni atestación externa: solo la fonotáctica la sostiene, que es filtro negativo, no positivo",
    },
    "baru xantu uou": {
        "seccion": "nombres",
        "glosa_fuente": "to ask for something to eat",
        "lectura_alternativa_ocr": "baru xantu uqu",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "frase, no lema; sin segmentación posible. Los dos OCR difieren en la última palabra (uou / uqu). No es material de léxico",
    },
    "danshebu": {
        "seccion": "nombres",
        "glosa_fuente": "sack, pouch (variante de danshikki)",
        "lectura_alternativa_ocr": "dansliebu",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "variante de danshikki; mismo veredicto",
    },
    "danshikki": {
        "seccion": "nombres",
        "glosa_fuente": "sack, pouch",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "el grupo /ʃi/ que van Buurt considera marca caquetía está presente, pero es un objeto de comercio (justo donde el préstamo es más probable) y no hay cognado",
    },
    "datie": {
        "seccion": "nombres",
        "glosa_fuente": "be gone!",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "interjección — la clase de menor rendimiento según el protocolo §6, y homófona del imperativo español 'date'. A favor: reaparece dentro de la fórmula infantil (tue daye datie'), lo que la ancla a la lengua extinta",
    },
    "ginga": {
        "seccion": "peces",
        "glosa_fuente": "Diodon atinga",
        "identificacion_moderna": "Diodon hystrix (pez erizo)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "sospechosa de ser el propio epíteto *atinga*, que es tupí, recortado; sin atestación externa",
    },
    "hanahana": {
        "seccion": "animales",
        "glosa_fuente": "Formica cephalota",
        "identificacion_moderna": "Atta cephalotes (bachaco cortador) — pero Atta no habita Aruba, así que la identificación decimonónica es muy dudosa",
        "lectura_alternativa_ocr": "hanakana (biostor) / hanahaua",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "es la SEGUNDA (y última) analogía comparativa que Gatschet encuentra, y es con el caribe insular (*hage* 'hormiga', Breton 1665), no con una lengua arahuaca — apunta a contacto caribe, no a herencia caquetía. Además el lexicón ya tiene `koke` (Zavala) para Atta spp. en el continente: dos formas distintas para el mismo referente",
    },
    "kafa": {
        "seccion": "nombres",
        "glosa_fuente": "devil, wicked spirit",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "es la ÚNICA correspondencia comparativa que Gatschet creyó encontrar (goajiro yaria/yarias/yaroja) y no se sostiene: kafa y yaria no comparten ni una consonante. Además 'diablo' es concepto poscontacto. Reaparece en la fórmula de maledicción, que es su mejor argumento",
    },
    "kanla": {
        "seccion": "nombres",
        "glosa_fuente": "thing, object (el propio Gatschet duda: '(?kaula)')",
        "lectura_alternativa_ocr": "kaula",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "abstracto genérico, la peor clase posible; y la propia fuente no sabe leer su forma",
    },
    "kantie baulete": {
        "seccion": "nombres",
        "glosa_fuente": "give me to eat!",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "frase, no lema; sin segmentación posible",
    },
    "karebe": {
        "seccion": "nombres",
        "glosa_fuente": "spoon",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "cultura material; sobrevive los descartes pero sin cognado ni atestación externa",
    },
    "karma-u": {
        "seccion": "peces",
        "glosa_fuente": "Characinus cyprinioides",
        "identificacion_moderna": "incierta; cf. van Buurt karawau = Peprilus paru (palometa)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§11 karawau (vínculo MENOS cierto)",
        "nivel": "C",
        "razon": "posible correspondencia con *karawau*, pero van Buurt la pone en su sección 11 (vínculo menos cierto) y el taxón de Gatschet (un carácido de agua dulce) es imposible en una isla árida sin ríos: la identificación de 1885 es errónea",
    },
    "kimakima": {
        "seccion": "animales",
        "glosa_fuente": "Cassiopea frondosa (a rhizopod)",
        "identificacion_moderna": "Cassiopea frondosa, medusa invertida — **no es un rizópodo**: el error zoológico es de Gatschet",
        "lectura_alternativa_ocr": "Oassiopea (los dos OCR)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "reduplicación; sin cognado ni atestación externa. Se conserva porque nombra fauna marina local, que es el campo de mayor rendimiento del protocolo",
    },
    "kinikini": {
        "seccion": "aves",
        "glosa_fuente": "Cymindes illigeri",
        "identificacion_moderna": "Falco sparverius (cernícalo americano)",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§11 kinikini — vínculo MENOS cierto",
        "nivel": "C",
        "razon": "voz viva, reduplicada y onomatopéyica (el cernícalo hace 'kili-kili'), lo que explica igual de bien un origen imitativo independiente. Van Buurt la degrada a la sección 11",
    },
    "kipopo": {
        "seccion": "plantas",
        "glosa_fuente": "Agaricus",
        "identificacion_moderna": "hongo agaricoide, sin especie determinable",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "sobrevive los descartes; forma reduplicada; pero sin cognado, sin atestación externa y con un 'taxón' que es solo un género de hongos",
    },
    "krabete": {
        "seccion": "aves",
        "glosa_fuente": "Fulica —? (la propia fuente deja la especie sin cerrar)",
        "identificacion_moderna": "Fulica sp. (focha); Aruba carece de humedales permanentes, así que la identificación es dudosa",
        "lectura_alternativa_ocr": "Fuliea (JSTOR) / Falica (BioStor)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "grupo consonántico inicial /kr-/ atípico del perfil arahuaco; la propia fuente no cierra la especie; ninguna atestación posterior. Sospechosa de romance o neerlandés, sin poder demostrarlo",
    },
    "kurkur": {
        "seccion": "peces",
        "glosa_fuente": "Chaetodon fromitus (reconstruido cruzando los dos OCR)",
        "identificacion_moderna": "Chaetodon sp. (pez mariposa)",
        "lectura_alternativa_ocr": "Ohmtodon (JSTOR) / Chcetodon (BioStor)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "reduplicación onomatopéyica; sin atestación externa",
    },
    "lembelembe": {
        "seccion": "animales",
        "glosa_fuente": "Conops sanguisuga (a dipteron)",
        "identificacion_moderna": "incierta; *Conops sanguisuga* no es un nombre aceptado",
        "lectura_alternativa_ocr": "Conops (JSTOR) / Oonops (BioStor)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "reduplicación; la raíz *lembe* coincide con el papiamento *lembe* 'lamer' (de origen portugués/africano), lo que la deja bajo sospecha del filtro 2/5 sin poder cerrarla",
    },
    "lokiloki": {
        "seccion": "plantas",
        "glosa_fuente": "Mimosa unguiscata",
        "identificacion_moderna": "Pithecellobium unguis-cati (Mimosa unguis-cati es sinónimo)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "campo semántico local y reduplicación (que el propio Gatschet señala como rasgo de la lengua), pero sin cognado ni atestación externa. ⚠️ nombra LA MISMA especie que dabaraida en esta misma lista: uno de los dos registros de campo de Pinart tiene que estar mal",
    },
    "puruntsi": {
        "seccion": "peces",
        "glosa_fuente": "Serranus variolosus",
        "identificacion_moderna": "Cephalopholis cruentata y Epinephelus fulvus (los dos meros que hoy se llaman purunchi)",
        "lectura_alternativa_ocr": "purnntsi (biostor); 'purantsi' en la cita de van Buurt",
        "ocr_que_la_sostiene": "ambos",
        "van_buurt_2014": "§11 purunchi (A,C,B) — vínculo MENOS cierto",
        "nivel": "C",
        "razon": "**es la entrada exacta sobre la que van Buurt formula su advertencia**: cita a Pinart y añade que 'this list contains several words which are definitely not Indian'. La voz está viva en las tres islas, pero su propio compilador moderno la degrada a la sección 11",
    },
    "tarabada": {
        "seccion": "arboles",
        "glosa_fuente": "segundo elemento de 'hubada tarabada'",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "van Buurt atestigua *hubada* sola; el segundo elemento no reaparece en ninguna fuente. Podría ser un epíteto o un error de campo de Pinart. Cf. el topónimo arubano Tarabana y Taratata/Tatarata",
    },
    "tida meo": {
        "seccion": "nombres",
        "glosa_fuente": "good morning!",
        "lectura_alternativa_ocr": ",tida meo / ^ida meo",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "SOSPECHA ALTA: fórmula de saludo en una isla que llevaba 80 años hablando papiamento, y va emparejada con 'ute kontabo', que es papiamento transparente. Las fórmulas de cortesía son la primera capa que se sustituye. Además el primer carácter difiere entre los dos OCR",
    },
    "waidanga": {
        "seccion": "nombres",
        "glosa_fuente": "water-gourd (variante)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "a diferencia de totumba no es panamericana; pero la terminación -nga es sospechosa de bantuismo (cf. mamondenga en esta misma lista) y van Buurt advierte que hay palabras africanas en la lista de Pinart",
    },
    "yoroyoro": {
        "seccion": "plantas",
        "glosa_fuente": "Thereiia/Theretia neriflora — reconstruido como *Thevetia neriifolia*",
        "identificacion_moderna": "Cascabela thevetia (syn. Thevetia peruviana)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "C",
        "razon": "reduplicación y campo semántico local, pero sin cognado ni atestación externa; no aparece en van Buurt",
    },

    # ── nivel D (9) — Descartada — cae en un filtro; se documenta con su razón ──
    "guruguru": {
        "seccion": "animales",
        "glosa_fuente": "Calandra granaria (a beetle)",
        "identificacion_moderna": "Sitophilus granarius, el gorgojo del granero — insecto del Viejo Mundo, plaga de grano almacenado",
        "lectura_alternativa_ocr": "Calandra (JSTOR) / Oalandra (BioStor)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "D",
        "filtro_de_descarte": "1 — español / referente introducido",
        "razon": "DOBLE descarte. (a) La especie es paleártica y llega con el grano europeo: no hay nombre precontacto para ella. (b) La forma es una reduplicación onomatopéyica que remite al español *gorgojo* (y a *gorgorear*)",
    },
    "jobo": {
        "seccion": "plantas",
        "glosa_fuente": "Spondias lutea",
        "identificacion_moderna": "Spondias mombin",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "D",
        "filtro_de_descarte": "4 — antillanismo panamericano",
        "razon": "*jobo* es taíno incorporado al español general (DRAE) y usado desde Cuba hasta el Perú. Sin valor probatorio para el caquetío insular",
    },
    "kumexen": {
        "seccion": "animales",
        "glosa_fuente": "Termes fatalis",
        "identificacion_moderna": "Nasutitermes sp. (comején de nido arbóreo)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "D",
        "filtro_de_descarte": "4 — antillanismo panamericano",
        "razon": "es *comején* en la ortografía afrancesada de Pinart (x = /x/). *Comején* es voz taína incorporada al español general (DRAE) y de uso en toda la Venezuela hispanohablante. No es evidencia de arubano",
    },
    "mamondenga": {
        "seccion": "animales",
        "glosa_fuente": "Ichneumon niger",
        "identificacion_moderna": "avispa icneumónida indeterminada",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "D",
        "filtro_de_descarte": "5 — africanismo",
        "razon": "estructura bantú transparente (prefijo ma- + -ndenga, cf. -nga en waidanga). Es del grupo que van Buurt explica: mezcla temprana con población de origen africano en Aruba metió palabras africanas en la lista de Pinart",
    },
    "nandu": {
        "seccion": "plantas",
        "glosa_fuente": "Cytisus catjan",
        "identificacion_moderna": "Cajanus cajan (guandú, quinchoncho) — leguminosa del Viejo Mundo",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "D",
        "filtro_de_descarte": "5 — africanismo",
        "razon": "DOBLE descarte. (a) La especie es asiático-africana, introducida: no puede tener nombre precontacto en Aruba. (b) La forma es el papiamento *wandu*, del kimbundu/bantú *wandu*. Es exactamente el tipo de voz que van Buurt explica cuando dice que la mezcla temprana con población de origen africano 'can explain some of the African words found in the Indian wordlist compiled by Pinart in Aruba'",
    },
    "takamahak": {
        "seccion": "plantas",
        "glosa_fuente": "Ragara octandra (probable errata de *Fagara octandra*, hoy Zanthoxylum)",
        "identificacion_moderna": "incierta; el nombre designa resinas de varios géneros (Calophyllum, Bursera, Protium)",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "D",
        "filtro_de_descarte": "4 — voz panamericana de circulación europea",
        "razon": "*tacamahaca* es voz náhuatl (*tecomahiyac*) que entró al español, al francés y a la farmacopea europea del s. XVIII como nombre de resina medicinal. Llegó a Aruba por el comercio, no por sustrato",
    },
    "totumba": {
        "seccion": "nombres",
        "glosa_fuente": "water-gourd",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "D",
        "filtro_de_descarte": "4 — antillanismo panamericano",
        "razon": "derivado de *totuma*, voz caribe/taína incorporada al español general (DRAE) y difundida por toda Hispanoamérica. Que se diga en Aruba no prueba sustrato caquetío local",
    },
    "ute kontabo": {
        "seccion": "nombres",
        "glosa_fuente": "how do you do?",
        "ocr_que_la_sostiene": "ambos",
        "nivel": "D",
        "filtro_de_descarte": "2 — papiamento/neerlandés",
        "razon": "PAPIAMENTO TRANSPARENTE: 'kontabo' es *kon ta bo* ('¿cómo estás?'), la fórmula corriente del papiamento, con *(b)o* de segunda persona. Es probablemente una de las voces que van Buurt tenía en mente al decir que la lista de Pinart 'contains several words which are definitely not Indian'",
    },
    "xovam": {
        "seccion": "nombres",
        "glosa_fuente": "phantom, hobgoblin",
        "lectura_alternativa_ocr": "tomoi",
        "ocr_que_la_sostiene": "jstor",
        "nivel": "D",
        "filtro_de_descarte": "forma irreconstruible",
        "razon": "los dos OCR leen cosas incompatibles ('xovam' vs ';tomoi'). No es un problema de etimología sino de que no sabemos qué palabra es. Inutilizable hasta ver el facsímil",
    },
}


# ══════════════════════════════════════════════════════════════════════
# T — TOPÓNIMOS ARUBANOS: canon y morfología, NO habla
# ══════════════════════════════════════════════════════════════════════
# Un agente no dice 'Yamanota' para decir 'monte'. Se conservan porque son
# morfología caquetía viva y porque van Buurt 2014 §7 los da, casi todos,
# como topónimos probablemente caquetíos que siguen en uso.

GATSCHET_TOPONIMOS: dict[str, dict] = {
    "Aiyo": {"tipo": "montaña", "lectura_alternativa_ocr": "", "van_buurt_2014": "Ayo"},
    "Behika": {"tipo": "montaña", "lectura_alternativa_ocr": "Beliika", "van_buurt_2014": "Behika, Behuko"},
    "Cukuroi": {"tipo": "montaña", "lectura_alternativa_ocr": "", "van_buurt_2014": "Kukurui"},
    "Handebirari": {"tipo": "montaña", "lectura_alternativa_ocr": "", "van_buurt_2014": ""},
    "Kasiaari": {"tipo": "montaña", "lectura_alternativa_ocr": "Kasinari (biostor)", "van_buurt_2014": "Kadiwari (?)"},
    "Kibaima": {"tipo": "montaña", "lectura_alternativa_ocr": "", "van_buurt_2014": "Kimbaima, Kibaima"},
    "Kodekodektu": {"tipo": "montaña", "lectura_alternativa_ocr": "Ivodekodektu (biostor)", "van_buurt_2014": "Kodekodectu"},
    "Matividiri": {"tipo": "montaña", "lectura_alternativa_ocr": "Malividiri (JSTOR, errata) / Matlvidiri (biostor)", "van_buurt_2014": "Matividiri — y en Paraguaná el cerro y caserío **Matividiro**"},
    "Shabururi": {"tipo": "montaña", "lectura_alternativa_ocr": "Shabaruri (JSTOR) / Sliabururi (biostor)", "van_buurt_2014": "Shabururi, Shabiburi"},
    "Shiribana": {"tipo": "montaña", "lectura_alternativa_ocr": "Sbiribana (biostor)", "van_buurt_2014": "Shiribana, Siribana, Shishiribana"},
    "Tarabana": {"tipo": "montaña", "lectura_alternativa_ocr": "", "van_buurt_2014": "Tarabana"},
    "Wakubana": {"tipo": "montaña", "lectura_alternativa_ocr": "", "van_buurt_2014": "Wakubana, Wacobana (mapa de 1825)"},
    "Yabarubari": {"tipo": "montaña", "lectura_alternativa_ocr": "", "van_buurt_2014": "Jaburibari (Seru)"},
    "Yamanota": {"tipo": "montaña", "lectura_alternativa_ocr": "", "van_buurt_2014": "Yamanota (Sero)"},
    "Matividiri (cueva)": {"tipo": "cueva", "lectura_alternativa_ocr": "", "van_buurt_2014": "Matividiri"},
    "Warerukuri": {"tipo": "cueva", "lectura_alternativa_ocr": "Warerfikuri (biostor)", "van_buurt_2014": "Warerikiri"},
    "Waririkiri": {"tipo": "cueva", "lectura_alternativa_ocr": "", "van_buurt_2014": "Guadirikiri, Wadirikiri (Cueva)"},
    "Antikuri": {"tipo": "lugar", "lectura_alternativa_ocr": "", "van_buurt_2014": "Andicuri, Andicouri"},
    "Arikurari": {"tipo": "lugar", "lectura_alternativa_ocr": "", "van_buurt_2014": "Avikurari"},
    "Bedui": {"tipo": "lugar", "lectura_alternativa_ocr": "", "van_buurt_2014": "Budui (Boca)"},
    "Bushiribani": {"tipo": "lugar", "lectura_alternativa_ocr": "Busliiribani (biostor); Gatschet marca '(?)'", "van_buurt_2014": "Bushiribana"},
    "Cubari": {"tipo": "lugar", "lectura_alternativa_ocr": "Cnbari (biostor)", "van_buurt_2014": "Caburi / Macubari (?)"},
    "Damari": {"tipo": "lugar", "lectura_alternativa_ocr": "Daman (biostor)", "van_buurt_2014": "Daimari, Damari (Rooi, Boca)"},
    "Hendieku": {"tipo": "lugar", "lectura_alternativa_ocr": "", "van_buurt_2014": ""},
    "Kamakuri": {"tipo": "lugar", "lectura_alternativa_ocr": "", "van_buurt_2014": "Camacuri"},
    "Kashiunti": {"tipo": "lugar", "lectura_alternativa_ocr": "Kasliiunti (biostor)", "van_buurt_2014": "Cashunti (Baranca)"},
    "Kausheati": {"tipo": "lugar", "lectura_alternativa_ocr": "", "van_buurt_2014": "Caushati (Sero)"},
    "Kassibari": {"tipo": "lugar", "lectura_alternativa_ocr": "", "van_buurt_2014": "Casibari — van Buurt lo etimologiza ka-siba-rí 'ahí hay rocas duras'"},
    "Wariruri": {"tipo": "lugar", "lectura_alternativa_ocr": "", "van_buurt_2014": "Wariruri"},
    "Weburi": {"tipo": "lugar", "lectura_alternativa_ocr": "AVeburi (biostor)", "van_buurt_2014": "Weburi"},
    "Yuditi": {"tipo": "lugar", "lectura_alternativa_ocr": "", "van_buurt_2014": "Juditi / Yuwiti, Yuiti / Uditi"},
}


# ══════════════════════════════════════════════════════════════════════
# R — FÓRMULAS DE HECHICERÍA: texto no traducible, valor ritual
# ══════════════════════════════════════════════════════════════════════
# Pinart insistió a Gatschet en que son citas literales de la lengua arubana
# extinta, y no consiguió traducción palabra por palabra. NO son léxico: no
# se segmentan, no se glosan y no puntúan. Su valor es para el habla del
# piache (ver mocs/MOC_creencia.md), como registro ritual opaco.

GATSCHET_FORMULAS: list[dict] = [
    {
        "uso": "maledicción",
        "texto": "xerebete den kafa magolotchi",
        "reconciliacion_ocr": "JSTOR lee ',-erebete'; BioStor lee 'xerebete' — se toma BioStor",
        "nota": "contiene `kafa` (diablo), que está en la lista de nombres",
        "etiqueta": "ritual-no-traducible",
    },
    {
        "uso": "asustar niños",
        "texto": "tue daye datie' gidio' dimi gurio yatabo",
        "reconciliacion_ocr": "coinciden los dos OCR",
        "nota": "contiene `datie` (¡fuera!), que está en la lista de nombres",
        "etiqueta": "ritual-no-traducible",
    },
    {
        "uso": "sacar espinas de cactus (1)",
        "texto": "una areya rafayete dudrea ebanero abono, caburo copudabo daburi",
        "reconciliacion_ocr": "JSTOR 'copudabo' / BioStor 'copudado'; van Buurt cita 'copudado'",
        "nota": "van Buurt 2014 especula que `daburi` designa las espinas del cactus, por su relación con dabaruida/dabaraida y el lokono dabáda 'uña, garra'. Es el ÚNICO fragmento de las seis fórmulas con una glosa parcial propuesta",
        "etiqueta": "ritual-no-traducible",
    },
    {
        "uso": "sacar espinas de cactus (2)",
        "texto": "yuni roba rapebo tchaba na aripebo, duda banabo pebo, home daba burvo, damei bo bakuna, daodao fuda dada",
        "reconciliacion_ocr": "JSTOR 'duda' / BioStor 'diida'",
        "nota": "Gatschet observa aquí 'some rhythm resembling assonance'",
        "etiqueta": "ritual-no-traducible",
    },
    {
        "uso": "sacar espinas de pescado de la garganta",
        "texto": "vidie pahidie, maranako tubara tchira deburro, hadiira karara",
        "reconciliacion_ocr": "JSTOR 'pahidie/hadiira' / BioStor 'pakidie/liadara'",
        "nota": "",
        "etiqueta": "ritual-no-traducible",
    },
    {
        "uso": "cazar la iguana",
        "texto": "Sako den komanari manadi watapuna fafa na douere sadii na ditieri",
        "reconciliacion_ocr": "JSTOR 'f&fa' / BioStor 'fafa'",
        "nota": "contiene `watapuna`, que el propio Gatschet relaciona con `watapana`",
        "etiqueta": "ritual-no-traducible",
    },
]


# ══════════════════════════════════════════════════════════════════════
# COBERTURA DE LAS 82 ENTRADAS DEL LEXICÓN SIN CITA (tarea F1)
# ══════════════════════════════════════════════════════════════════════

COBERTURA_82: dict[str, dict] = {
    "watapana": {"forma_en_gatschet": "watapana", "veredicto": "RESUELTA — atestiguada en Aruba, 1882, con taxón"},
    "warawara": {"forma_en_gatschet": "warawara", "veredicto": "RESUELTA — y con corrección: el taxón del lexicón ('Cathartes curasoica') es la identificación de Gatschet de 1885; hoy es Caracara cheriway"},
    "chuchubi": {"forma_en_gatschet": "shushubi", "veredicto": "RESUELTA — vía la variante insular con sh-"},
    "kadushi": {"forma_en_gatschet": "kaduski", "veredicto": "RESUELTA en la forma; el referente queda ABIERTO (tres cactus distintos en tres fuentes)"},
    "kunuku": {"forma_en_gatschet": "cunucu", "veredicto": "RESUELTA — pero por la sección de PAPIAMENTO del artículo ('Muchas en el campo / jopi na cunucu', Guía de Curazao 1876), no por la lista arubana"},
    "pauji": {"forma_en_gatschet": "pajuis", "veredicto": "NO RESUELTA — 'pauji' aparece como la voz ESPAÑOLA de la columna izquierda ('pauji → pajuis'), no como voz arubana. No sirve de cita caquetía"},
    "auyama": {"forma_en_gatschet": "pampuna", "veredicto": "NO RESUELTA — 'ahullama' aparece como voz española del guía de conversación; el papiamento usa pampuna. No sirve de cita"},
    "tuqueque": {"forma_en_gatschet": "", "veredicto": "NO EN GATSCHET — pero van Buurt 2014 §6 (s.v. waltaca) dice que 'totèki' deriva de 'tuqueque, tuteque, an Amerindian word used for geckos in Venezuela'. Cita disponible, pero de F6, no de F4"},
    "chiriguare": {"forma_en_gatschet": "", "veredicto": "NO EN GATSCHET como voz arubana; en la sección papiamento el 'gavilán' es *guaraguara* (= warawara), no *chiriguare*"},
}


# ══════════════════════════════════════════════════════════════════════
# AFIJOS: ¿confirman los topónimos arubanos a REGLAS_ZAVALA?
# ══════════════════════════════════════════════════════════════════════
# Confirmación cruzada independiente: Zavala compila Falcón continental,
# Pinart recoge Aruba insular en 1882. Si los mismos afijos aparecen en los
# dos corpus, el afijo es de la lengua y no del compilador.

AFIJOS_EN_TOPONIMOS: dict[str, list] = {
    "-iro": [],
    "-aima": ["Kibaima"],
    "-ima": [],
    "-uco": [],
    "-ubana": ["Wakubana"],
    "-uru": ["Shabururi", "Warerukuri", "Antikuri", "Kamakuri", "Wariruri", "Weburi"],
    "-bana": ["Shiribana", "Tarabana", "Wakubana", "Bushiribani"],
}

# Sufijos frecuentes en los topónimos que el proyecto NO tiene codificados:
SUFIJOS_NO_CODIFICADOS: dict[str, list] = {
    "-kuri/-curi": ["Warerukuri", "Antikuri", "Kamakuri"],
    "-bari": ["Yabarubari", "Cubari", "Kassibari"],
    "-kiri/-diri": ["Matividiri", "Matividiri", "Waririkiri"],
    "-ari": ["Handebirari", "Kasiaari", "Yabarubari", "Arikurari", "Cubari", "Damari", "Kassibari"],
}


TOTALES = {
    "nivel_A": 12,
    "nivel_B": 2,
    "nivel_C": 25,
    "nivel_D": 9,
    "toponimos": 31,
    "formulas": 6,
    "formas_totales": 79,
}
