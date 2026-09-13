# -*- coding: utf-8 -*-
"""Vacía el capítulo del verbo de Perea y Alonso 1942 (pp. impresas 609-684).

Genera 6-fusion/lokono_verbos_perea_1942.yaml. Regla 5: propone, no fusiona.

Qué es este capítulo: los paradigmas de conjugación de SCHUMANN (manuscrito de
1755) ordenados por Perea, y —lo que aquí importa— las listas «se conjugan como
X los siguientes», que son el VOCABULARIO VERBAL de Schumann. Es un estrato más
viejo aún que el Fraseario (Schultz 1802).

Método: leído a mano del OCR (`pdftotext`), página por página. No es un vaciado
por regex porque las listas del OCR se desplazan por columnas y mezclan glosas
de verbos vecinos (medido: «a-paù-n = matar ù, a-cakù-dù - navivar» son DOS
verbos). Cada forma lleva su página impresa y, si hace falta, una marca:
  sic    — Perea lo marca (sic) en la fuente
  ?      — Perea pone signo de duda [?]
  Al     — Perea deja la glosa en alemán (Al: ...)
  ocr    — la lectura del OCR es dudosa (vocal caída, glifo raro, etc.)

Ortografía: el OCR lee como `л` (ele cirílica) uno de los glifos de la Clave
Panfonética de Perea. `Cxaлúa` = Charrúa lo fija: `л` = RR española. Aquí se
translitera a `rr` (a-лusu-ttu-n → a-rrusu-ttu-n) y se marca `ocr`.

La lista se cotejó con el lexicón para separar CORROBORACIONES de NUEVAS.
"""
import io, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL
V = CL.VOCABULARIO_BASE

# (forma tal como la da Perea, glosa, página impresa, conjugación, marcas)
VERBOS = [
 # ── 1ª conjugación, 1ª clase: los en -in (modelo a-iyaha-ddi-n «andar, caminar», pp. 609-613)
 ("a-iyaha-ddi-n","andar, caminar",609,"1-in",""),
 ("a-ù-n","llorar",614,"1-in",""),
 ("a-ditti-n","saber, conocer",614,"1-in",""),
 ("a-buli-di-n","escribir, pintar",614,"1-in",""),
 ("a-idi-n","ceñir",614,"1-in",""),
 ("a-calleme-tti-n","encender",614,"1-in",""),
 ("a-m-a-monaica-di-n","enriquecer (lit. hacer no-pobre: m- privativo sobre a-monaica «pobre»)",614,"1-in",""),
 ("a-úyi-n","arrancar, coger",614,"1-in",""),
 ("a-siki-n","dar, poner",614,"1-in",""),
 ("a-iyaon-tti-n","comprar",614,"1-in",""),
 ("a-balti-n","sentarse",614,"1-in",""),
 ("a-budi-di-n","pescar",614,"1-in",""),
 ("a-dibal-di-n","(Al: berbekutten — glosa alemana ilegible en la fuente)",614,"1-in","Al,ocr"),
 ("a-dumki-n","dormir, pernoctar, alojarse",614,"1-in",""),
 ("a-ùki-tti-n","andar en vehículo",614,"1-in",""),
 ("a-man-ti-n","afilar, aguzar",614,"1-in",""),
 ("a-puttùki-di-n","apartarse",614,"1-in",""),
 ("a-tti-n","beber",614,"1-in",""),
 ("ibbekiki-n","(Al: bogairen — glosa alemana ilegible en la fuente)",614,"1-in","Al,ocr"),
 ("a-malli-n","hacer (I: to make)",614,"1-in",""),
 ("a-balli-n","pasar, irse",614,"1-in",""),
 ("a-púsi-ti-n","libertar",614,"1-in",""),
 ("a-diriki-n","afeitar, aderezar",614,"1-in",""),
 ("a-uki-n","montar en vehículo",614,"1-in",""),
 ("a-cui-di-n","escupir",614,"1-in",""),
 ("a-ndi-n","venir",614,"1-in",""),
 ("a-nniki-di-n","elevar, alzar",614,"1-in",""),
 ("a-rdi-n","morder",614,"1-in",""),
 ("a-ttiki-n","cavar, ahondar",614,"1-in",""),
 ("a-ddiki-n","ver",614,"1-in",""),
 ("a-bule-di-n","tirar, echar",614,"1-in",""),
 ("a-bule-he-di-n","arrojar, tirar, echar",614,"1-in",""),
 ("a-yali-di-n","envenenar con tóxico vegetal",614,"1-in",""),
 ("ibitti-n","quemar, encender",614,"1-in",""),
 ("a-llihù-ti-n","ungir, untar",614,"1-in",""),
 ("a-ndi-kitti-n","hacer venir (causativo de a-ndi-n)",614,"1-in",""),
 ("a-cohùn-ti-n","plantar",614,"1-in",""),
 ("a-ri-di-n","nombrar, apellidar",614,"1-in",""),
 # ── 1ª conjugación, 2ª clase: los en -ùn (modelo a-ttuba-ddù-n «zambullir», pp. 615-618)
 ("a-ttuba-ddù-n","zambullir",615,"1-ùn",""),
 ("a-dina-mùn","estar presente",618,"1-ùn",""),
 ("a-bacubù-n","respirar, reposar",618,"1-ùn",""),
 ("a-canabù-n","oír",618,"1-ùn",""),
 ("a-iyaha-dù-n","asar",618,"1-ùn","sic"),
 ("a-ccu-dù-n","arrojar, echar",618,"1-ùn",""),
 ("a-dalli-dù-n","saltar",618,"1-ùn",""),
 ("a-paù-n","matar",618,"1-ùn",""),
 ("a-cakù-dù-n","avivar",618,"1-ùn","ocr"),
 ("a-hurke-dù-n","juntarse, reunirse",618,"1-ùn",""),
 ("a-burùkù-dù-n","golpear, herir",618,"1-ùn",""),
 ("a-ùsa-dù-n","hacer bien",618,"1-ùn","ocr"),
 ("a-iyaca-ttù-n","esconder, ocultar",618,"1-ùn",""),
 ("a-cai-dù-n","romper, quebrar",618,"1-ùn",""),
 ("a-bbunnù-n","plantar",619,"1-ùn",""),
 ("a-ccarku-dù-n","tejer, trenzar",619,"1-ùn",""),
 ("a-patta-dù-n","abofetear",619,"1-ùn",""),
 ("a-húla-dù-n","taladrar, agujerear",619,"1-ùn",""),
 ("a-para-dù-n","cortar madera",619,"1-ùn",""),
 ("a-cartù-n","enterrar, sepultar",619,"1-ùn",""),
 ("a-ttù-dù-n","huir, escaparse",619,"1-ùn",""),
 ("a-yara-dù-n","dar zarpazos",619,"1-ùn",""),
 ("a-kkùù-n","atar, ligar",619,"1-ùn",""),
 ("a-kùn-dù-n","lucir, orillar",619,"1-ùn","ocr"),
 ("a-tia-dù-n","pasar por, introducir",619,"1-ùn",""),
 ("a-ibù-n","dejar, omitir",619,"1-ùn",""),
 ("a-ccabba-tù-n","salar",619,"1-ùn",""),
 ("a-iyacu-n-nua-tia-dù-n","atravesar de parte a parte",619,"1-ùn",""),
 ("a-cula-ttù-n","golpear, herir",619,"1-ùn",""),
 ("a-cúllekù-n","esparcir, desparramar",619,"1-ùn",""),
 ("a-kùttù-n","empujar, chocar",619,"1-ùn",""),
 # ── 1ª conjugación, 3ª clase: los en -un (modelo a-sonnucu-n «verter, derramar», pp. 619-623)
 ("a-sonnucu-n","verter, derramar",619,"1-un",""),
 ("a-iyacusu-n","apagar",623,"1-un",""),
 ("a-ddur-hu-n","tejer, trenzar",623,"1-un",""),
 ("a-iyurucu-n","llevar, conducir",623,"1-un",""),
 ("a-bucu-n","hervir, cocer",623,"1-un",""),
 ("a-sucu-n","cortar, mochar",623,"1-un",""),
 ("a-cu-du-n","ablandar con agua",623,"1-un",""),
 ("a-rrusu-ttu-n","edificar",623,"1-un","ocr"),
 ("a-sucusu-n","lavar",623,"1-un",""),
 ("a-surcu-du-n","emparentar",623,"1-un",""),
 ("a-tullu-du-n","abrir",623,"1-un",""),
 ("a-iyucu-n","cazar",623,"1-un",""),
 ("a-tun-du-n","toser",623,"1-un",""),
 ("a-bucu-ttu-n","coger, asir",623,"1-un",""),
 ("a-cuttu-n","comer",623,"1-un",""),
 ("a-ruru-tu-n","hacer barroso",623,"1-un",""),
 ("a-du-cuttu-n","mostrar, enseñar",623,"1-un",""),
 ("a-cunnu-n","ir",623,"1-un",""),
 ("a-mor-du-n","volar",623,"1-un",""),
 ("a-su-du-n","raspar, raer",623,"1-un",""),
 ("a-púyu-ttu-n","cargar, agravar",623,"1-un",""),
 ("a-ttucu-du-n","bajar, descender",623,"1-un",""),
 ("a-turru-du-n","acostarse, echarse (Al: niederliegen)",623,"1-un","Al,ocr"),
 ("a-sur-tu-n","besar, chupar",623,"1-un",""),
 ("a-ttucu-n","comer chupando",623,"1-un",""),
 ("a-hú-du-n","morir (con u larga acentuada: d-a-hú-da «muero», d-a-hú-du-pa «moriré»)",623,"1-un",""),
 # ── 2ª conjugación: los en -an (modelo a-iyaha-dda-n «arrancar (yuca); desarraigar, exhumar», pp. 624-629)
 ("a-iyaha-dda-n","arrancar (yuca); en el vocabulario, desarraigar, exhumar",624,"2-an",""),
 ("a-haca-n","hablar",628,"2-an",""),
 ("a-iyuca-n","cazar, perseguir",628,"2-an",""),
 ("a-ollasa-n","hender",628,"2-an",""),
 ("a-pana-n","herir (cf. p. 546: pana «matar, herir»)",628,"2-an","ocr"),
 ("a-usa-n","frotar",628,"2-an",""),
 ("a-hùla-da-n","perforar",628,"2-an",""),
 ("a-iyucaia-n","vender",628,"2-an",""),
 ("a-cai-da-n","quebrar, romper",628,"2-an",""),
 ("a-dia-n","decir",628,"2-an",""),
 ("a-suca-n","cortar, tronchar",628,"2-an",""),
 ("a-onnaba-n","responder",628,"2-an",""),
 ("a-purisa-n","raspar la piel",628,"2-an",""),
 ("a-sucusa-n","lavar",628,"2-an",""),
 ("a-ùmaha-n","hostilizar",628,"2-an",""),
 ("a-ca-n","lavarse",628,"2-an",""),
 ("a-canaba-n","oír",628,"2-an",""),
 ("a-ccu-da-n","hilar",628,"2-an",""),
 ("a-carta-n","enterrar",629,"2-an",""),
 ("a-ccura-n","cocer [¿coser?]",629,"2-an","?"),
 ("a-sica-n","creer, oír",629,"2-an",""),
 ("a-muli-da-n","engañar",629,"2-an",""),
 ("a-ddura-n","tejer, trenzar",629,"2-an",""),
 ("ikkia-n","evacuar el cuerpo",629,"2-an",""),
 ("a-sina-n","descaminar",629,"2-an",""),
 ("a-cuyabua-n","golpear, herir",629,"2-an",""),
 ("a-lamma-da-n","tambalearse",629,"2-an",""),
 ("a-manta-n","afilar",629,"2-an",""),
 ("a-nnaca-n","empuñar",629,"2-an",""),
 ("a-tticaha-n","ahogarse",629,"2-an",""),
 ("a-sia-n","pescar con nasa",629,"2-an",""),
 ("a-sa-n","nombrar",629,"2-an",""),
 ("a-ùca-n","casarse",629,"2-an",""),
 ("a-ddaca-n","soltar agua",629,"2-an",""),
 ("a-saca-da-n","encontrar",629,"2-an",""),
 ("a-cuikita-n","retornar, volver",629,"2-an",""),
 ("a-llucu-da-n","exponer, mostrar",629,"2-an",""),
 ("a-mali-cutta-n","enseñar",629,"2-an",""),
 ("a-maroa-da-n","cazar con flechas de madera",629,"2-an",""),
 ("a-mali-cuttu-a-n","aprender",629,"2-an",""),
 ("c-a-bbura-n","ser amplio, vasto (m-a-bbura-n «ser angosto»)",629,"2-an",""),
 # ── 3ª conjugación: los en -un-nua, reflexivos/medios (modelo a-iyuhu-dú-n-nua «pender, estar colgado», pp. 629-634)
 ("a-iyuhu-dú-n-nua","pender, estar colgado (Perea: sólo puede ser «colgarse»; a-iyubu-du-n «colgar, ahorcar» es el transitivo)",629,"3-n-nua",""),
 ("a-bucú-n-nua","cocerse",633,"3-n-nua",""),
 ("a-ùbú-n-nua","cesar, acabar",633,"3-n-nua",""),
 ("a-dittú-n-nua","conocerse",633,"3-n-nua",""),
 ("a-pusi-dú-n-nua","librarse",633,"3-n-nua",""),
 ("a-sikillú-n-nua","ser envuelto (Al: eingewickelt werden)",633,"3-n-nua","Al"),
 ("a-huducullú-n-nua","suicidarse",633,"3-n-nua",""),
 ("a-cu-dú-n-nua","introducirse",633,"3-n-nua",""),
 ("a-idi-kittú-n-nua","ser ceñido",633,"3-n-nua",""),
 ("a-huke-dú-n-nua","perderse",633,"3-n-nua",""),
 ("a-buli-dú-n-nua","pintarse",633,"3-n-nua",""),
 ("a-ddele-dú-n-nua","anclarse",633,"3-n-nua",""),
 ("a-dibaldi-kittú-n-nua","acostumbrarse a dar",633,"3-n-nua","ocr"),
 ("e-besú-n-nua","florecerse",633,"3-n-nua",""),
 ("a-hudú-n-nua","curvarse",633,"3-n-nua",""),
 ("a-huca-dù-n-nua","estar agujereado",633,"3-n-nua",""),
 ("a-iyacusú-n-nua","apagarse",634,"3-n-nua",""),
 ("a-uma-ttú-n-nua","ser malo",634,"3-n-nua",""),
 ("a-iyucú-n-nua","cazarse",634,"3-n-nua",""),
 ("ibi-ttú-n-nua","arder",634,"3-n-nua",""),
 ("a-iyabu-dù-kittú-n-nua","asarse",634,"3-n-nua",""),
 ("a-iyahacú-n-nua","atravesar, pasar por entre",634,"3-n-nua",""),
 ("a-sucú-n-nua","cortarse",634,"3-n-nua",""),
 ("a-ùn-ttú-n-nua","vencer [?]",634,"3-n-nua","?"),
 ("a-rdú-n-nua","envanecerse",634,"3-n-nua",""),
 # ── 4ª conjugación: los en -en, estativos con pronombre POSPUESTO (modelo halli-kebbe-n «alegrarse», pp. 634-639)
 ("halli-kebbe-n","alegrarse, complacerse (halli-kebbe-hi «alegría»; da-halli-kebbe «mi alegría»)",634,"4-en",""),
 ("catti-kebe-n","robar (p. 664: c-a-tti-kebe-n «robar, hurtar»)",638,"4-en","sic"),
 ("haule-n","ser ruin",638,"4-en",""),
 ("ibe-n","estar lleno",638,"4-en",""),
 ("caii-me-n","ser negro",638,"4-en",""),
 ("ereke-n","desherbar, sacar la hierba",638,"4-en",""),
 ("ca-me-n","oler, ser oloroso, dar olor de sí (p. 664: ca-eme-n)",638,"4-en",""),
 ("case-n","estar agusanado",638,"4-en",""),
 ("pere-n","estar furioso, airado",638,"4-en",""),
 ("waikille-n","estar lejos (p. 665: wai-kille-n «ser ancho»)",638,"4-en",""),
 ("m-ake-n","estar desnudo (privativo de c-ake-n «estar vestido»)",638,"4-en",""),
 ("ma-yukehe-n","no estar loco (privativo: *yukehe- «loco»)",638,"4-en",""),
 ("iribe-n","ser impuro",638,"4-en",""),
 ("hehe-n","ser pálido",638,"4-en",""),
 ("ipi-lli-be-n","ser grande (vr.; ipi-ru-be-n nv.)",638,"4-en",""),
 ("c-ake-n","estar vestido, cubierto",638,"4-en",""),
 ("bele-n","ser blando",638,"4-en",""),
 ("sipe-n","ser amargo [?]",638,"4-en","?"),
 ("hebbe-n","ser viejo, anciano",638,"4-en",""),
 ("calli-me-n","lucir, brillar",638,"4-en",""),
 ("ide-n","estar muy cocido",638,"4-en",""),
 ("cule-n","ser rojo, colorado",638,"4-en",""),
 ("were-be-n","estar caliente (p. 665: tere-n)",638,"4-en",""),
 ("subu-le-n","ser verde",638,"4-en",""),
 ("ma-mole-n","no estar ebrio (p. 664: sommole-n «estar ebrio»)",638,"4-en",""),
 ("m-isi-re-n","proceder rectamente (pronombre d-a, b-a… pospuesto)",638,"4-en",""),
 ("yiba-na-n","retrasarse, quedarse atrás",639,"4-en",""),
 ("c-a-monai-ca-n","ser pobre",639,"4-en",""),
 ("c-a-sicoa-n","habitar, residir",639,"4-en",""),
 ("casa-n","engendrar (p. 664: c-a-sa-n; m-a-sa-n «no tener hijos»)",639,"4-en",""),
 ("c-a-ima-n","ser malo (p. 664: c-a-ima-ca-n)",639,"4-en",""),
 ("emelie-n","ser nuevo, reciente (emelia de «soy nuevo»)",639,"4-en",""),
 ("c-a-raiyè-n","aparecer",639,"4-en",""),
 ("yaha-ddi-a-n","estar cerca (p. 639: vaha-di-è-n)",665,"4-en",""),
 ("ùttùa-n","ser sangriento, estar ensangrentado (p. 639: yittùè-n)",665,"4-en",""),
 ("sommole-n","estar ebrio",664,"4-en",""),
 ("k-eme-kebbù-n","trabajar (p. 648: keme-kebbu-n «estar atareado»)",664,"4-en",""),
 ("seme-n","ser dulce",665,"4-en",""),
 ("tere-n","estar caliente",664,"4-en",""),
 ("wuré-n","guiar (Sl: fornicar)",665,"4-en",""),
 ("mihite-n","estar cansado",665,"4-en",""),
 ("wasi-n","ser amplio",665,"4-en",""),
 ("wai-kille-n","ser ancho",665,"4-en",""),
 ("ùsa-n","ser bueno (mù-ùsa-n «no ser bueno»)",665,"4-en",""),
 ("wadi-n","ser amplio (wadi-ke n «es muy amplio»)",679,"4-en",""),
 ("móa-di-n","ser corto",679,"4-en",""),
 # ── 5ª conjugación: presente en -ca, infinitivo en -in (modelos a-mùn-ni-n «estar con, haber, tener» y c-a-nsi-n «amar», pp. 640-646)
 ("a-mùn-ni-n","estar con, haber, tener (Schumann: c-a-mùn-ni-n «haber, tener»; m-a-mùn-ni-n «carecer»)",640,"5-ca",""),
 ("c-a-nsi-n","amar, querer (c-a-nsi-hi «amor, querencia»; c-a-nsi-sia «amado»)",644,"5-ca",""),
 ("cai-n","estar enfermo (cari-ca de «estoy enfermo»)",644,"5-ca",""),
 ("hadubu-tti-n","sudar",647,"5-ca",""),
 ("cakù-n","vivir (cakù-ca de «vivo»)",647,"5-ca",""),
 ("hamaru-n","estar asustado (?) (p. 668: hamma-ru-ca bu «estás con miedo»)",647,"5-ca","?"),
 ("a-boa-n","estar enfermo",647,"5-ca",""),
 ("hiccu-li-n","ser cojo",647,"5-ca",""),
 ("c-a-lluccu-n","no estar vacío",647,"5-ca",""),
 ("a-daiya-hù-n","estar despierto (p. 668: a-daiya-hù-ca bu «eres señor, distinguido»; p. 676: Gott a-daiya-coa-coa-na «el reino de Dios»)",647,"5-ca",""),
 ("a-nnakù-di-n","estar en medio, entre",647,"5-ca",""),
 ("a-bu-luccu-du-n","estar en punta",647,"5-ca",""),
 ("tu-rubu-ddi-n","estar cansado",647,"5-ca",""),
 ("haburù-n","estar avergonzado (haburu-ca de «me avergüenzo»)",648,"5-ca",""),
 ("k-ere-ti-n","estar casada (k-ere-u-n «estar casado»; k-ere-ru-ca «tengo mujer»)",648,"5-ca",""),
 ("c-a-ddibeu-n","ser grueso",648,"5-ca",""),
 ("kebéru-n","ser disimulado (p. 668: k-ebe-ru-ca de «yo oculto»)",648,"5-ca",""),
 ("hammarù-n","estar acobardado (?)",648,"5-ca","?"),
 ("coa-llaba-n","estar al lado",648,"5-ca",""),
 ("a-ni-n","hacer (I: to do); el auxiliar universal",648,"5-ca",""),
 # ── recíprocos (c-a-nse-n u-mon-ne-coa-wa «amarse mutuamente», pp. 648-651)
 ("ebeta-n","retardar",650,"recíproco",""),
 ("ikitta-n","servir, atender",650,"recíproco",""),
 ("a-tteki-da-n","persuadir",650,"recíproco",""),
 # ── verbos con infijo y elípticos (pp. 651, 666-683)
 ("c-a-cubu-ruccu-n","acordarse (m-a-cubu-ruccu-ca de «no me acuerdo»)",666,"5-ca",""),
 ("a-ddica-hitti-n","desear ver (verbo de deseo con -hitti-)",671,"deseo",""),
 ("a-tta-hitti-n","tener sed, gana de beber (m-a-tta-hitti-n «no tener sed»)",672,"deseo",""),
 ("a-dum-ca-rubú-ma-n","sólo dormir (a-dum-ca «dormir» + -rubu- exclusivo)",672,"exclusivo",""),
 ("a-sima-ca-n","gritar, llamar (reduplicado a-sima-sima-ca-n «clamorear», Hechos 19-32)",679,"reduplicación",""),
 ("a-sucu-sucu-n","bautizar (reduplicación de a-sucusu-n «lavar»)",679,"reduplicación",""),
 ("a-dia-dia-n","disertar (reduplicación de a-dia-n «hablar», Hechos 24-25)",679,"reduplicación",""),
 ("a-haca-haca-n","predicar (reduplicación de a-haca-n «decir», Hechos 10-42)",679,"reduplicación",""),
 ("poi! m-a-n","decir ¡ah!, asombrarse (verbo elíptico sobre la interjección poi!)",682,"elíptico",""),
]

# Voces NO verbales que salen de paso en los ejemplos del capítulo.
SUELTAS = [
 ("calli","yuca (kia calli «esta yuca», da-calle «mi yuca»)",628,"sust",""),
 ("barba-coa","cañizo, como parrillas, donde se pone habitualmente a secar o ahumar algo (Perea lo da como ejemplo de -coa «estado, permanencia»)",651,"sust",""),
 ("curru","no (adverbio pospuesto que sustituye a la m- de negación: m-a-nsi d-a = d-a-nsi-ca curru). OCR «cuлu», л = rr",665,"part","ocr"),
 ("make","mucho, con vehemencia (adv.; make d-a «hablo con vehemencia»; infijo intensivo -make-)",676,"part",""),
 ("rubu","sólo; poco; apenas (Perea: «sobre rubu habría mucho que hablar»; Hechos 1-5, 12-18)",651,"part",""),
 ("hitti-ha","gusto, deseo (infijo -hitti- de los verbos de deseo)",651,"sust",""),
 ("lu-luccu-mùn-ti","los que están con él [sus amigos] [?]",666,"sust","?"),
]

SUFIJO_INF = re.compile(r"-(n-nua|nua|n)$")


def clave(forma):
    """La clave propuesta: la forma sin el prefijo verbal a-/c-a- y sin el -n."""
    f = forma.replace("!", "").replace(" ", "-").strip()
    f = SUFIJO_INF.sub("", f)
    for p in ("c-a-", "k-", "m-a-", "ma-", "a-", "e-"):
        if f.startswith(p) and len(f) > len(p) + 1:
            base = f[len(p):]
            # los estativos con atributivo c-/k- conservan la marca para no
            # confundirse con la raíz desnuda (c-a-ima «ser malo» ≠ ima «enemigo»)
            if p in ("c-a-", "k-"):
                return p.rstrip("-") + "-" + base
            if p in ("m-a-", "ma-"):
                return "m-" + base
            return base
    return f


def pelada(s):
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = s.lower().replace("-", "")
    return re.sub(r"(.)\1", r"\1", s)


# índice del lexicón por forma pelada
idx = {}
for k, v in V.items():
    idx.setdefault(pelada(k.replace("-lokono", "")), []).append(k)


def cotejo(cl):
    p = pelada(cl.replace("c-a-", "").replace("k-", "").replace("m-", ""))
    return [k for k in idx.get(p, []) if V[k].get("fuente") == "lokono"]


filas = []
for forma, glosa, pag, conj, marcas in VERBOS:
    cl = clave(forma)
    ya = [k for k in (cl, cl + "-lokono") if k in V]
    fila = {"forma": forma, "clave": cl, "glosa": glosa, "pagina": pag, "conjugacion": conj}
    if marcas:
        fila["marcas"] = marcas.split(",")
    if ya:
        fila["ya_en_lexicon"] = ya[0]
        fila["glosa_lexicon"] = V[ya[0]]["sig"]
    else:
        parecidas = cotejo(cl)
        if parecidas:
            fila["forma_parecida_en_lexicon"] = {k: V[k]["sig"] for k in parecidas}
    filas.append(fila)

sueltas = []
for forma, glosa, pag, cat, marcas in SUELTAS:
    fila = {"forma": forma, "clave": forma, "glosa": glosa, "pagina": pag, "cat": cat}
    if marcas:
        fila["marcas"] = marcas.split(",")
    if forma in V:
        fila["ya_en_lexicon"] = forma
        fila["glosa_lexicon"] = V[forma]["sig"]
    sueltas.append(fila)

# Corroboraciones POR CONCEPTO con la columna lokono que vino de otras fuentes
# (Oliver A-2, Pet 1987, Goeje 1928, Brinton): misma glosa, forma comparable.
CONCEPTO = [
 ("a-dumki-n","donkon","dormir"), ("a-tti-n","ythyn","beber"), ("a-ndi-n","andin","venir"),
 ("a-rdi-n","ridin","morder"), ("a-canaba-n","kanabyn","oír"), ("a-bucu-n","bokon","hervir, cocer"),
 ("a-mor-du-n","morodon","volar"), ("a-paù-n","aparrun","matar"), ("ibitti-n","bithin","quemar, arder"),
 ("a-siki-n","sikin","dar, poner"), ("a-ditti-n","aithin","saber, conocer"), ("a-cuttu-n","khoton","comer"),
 ("emelie-n","emelia","nuevo"), ("a-hú-du-n","huda","morir"), ("a-iyucaia-n","iyucana","vender"),
 ("a-tullu-du-n","tullu-du","abrir"), ("a-balti-n","balti","sentarse"), ("barba-coa","barrahakoa","barbacoa"),
 ("ipi-lli-be-n","firo","grande"), ("were-be-n / tere-n","orebe","caliente"),
]
DIVERGEN = [
 ("cule-n «ser rojo»","roodi «rojo, colorado» (Goeje 1928)","raíces distintas para el mismo concepto"),
 ("caii-me-n «ser negro»","siwi «negro, oscuro» (Goeje 1928)","raíces distintas para el mismo concepto"),
 ("hehe-n «ser pálido»","hehen «amarillo» (Pet 1987)","misma raíz, glosa desplazada: pálido / amarillo"),
 ("calli «yuca»","yuka «yuca, mandioca» (Goeje 1928)","raíces distintas; el lokono moderno da khali/kali para el casabe y la yuca"),
 ("a-cunnu-n «ir»","osyn «ir, caminar» (Pet 1987) · cun-te «ir» (Perea, Fraseario)","cun-te y cunnu son la misma raíz; osyn es otra"),
 ("ipi-lli-be-n «ser grande»","firo «grande» (Pet 1987)","raíces distintas para el mismo concepto"),
]


def dump(obj):
    import yaml
    return yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=110,
                          default_flow_style=False)


nuevas = [f for f in filas if "ya_en_lexicon" not in f]
corrob = [f for f in filas if "ya_en_lexicon" in f]
out = io.StringIO()
out.write("""# ─────────────────────────────────────────────────────────────────────────
# EL VERBO de Perea y Alonso 1942 (parte II, pp. impresas 609-684) —
# los paradigmas de SCHUMANN (ms. 1755) y, dentro de ellos, su vocabulario
# verbal: las listas «se conjugan como X los siguientes».
#
# GENERADO por 6-fusion/scripts/minar_perea_verbos.py — la lista está
# escrita a mano en ese script (leída del OCR página por página), y el
# script sólo la coteja con el lexicón y la ordena. Para corregir una voz,
# corrígela allí y regenera.
#
# Regla 5: propuesta, no fusión. Regla 8: cada voz lleva su página impresa.
# ─────────────────────────────────────────────────────────────────────────
""")
meta = {
 "meta": {
  "generado_por": "6-fusion/scripts/minar_perea_verbos.py",
  "obra": "perea-alonso-1942",
  "parte": "II — Compendio Gramatical, el verbo: pp. impresas 609-684 (pdf 833-912)",
  "minado": "2026-09-12",
  "estrato": ("VOCABULARIO DE SCHUMANN, manuscrito de 1755 (p. 628: «en el vocabulario este verbo "
              "significa...»), ordenado por Perea y ampliado a veces con Schultz 1802. Es el estrato "
              "lokono más antiguo del repo, anterior al Fraseario."),
  "metodo": ("Leído a mano del OCR de pdftotext. NO se vació por regex: las listas del OCR se desplazan "
             "por columnas y pegan la glosa de un verbo al vecino. Cada forma se copió con su página; "
             "las dudosas llevan `marcas` (sic / ? / Al / ocr)."),
  "ortografia": ("Clave Panfonética de Perea (p. impresa CI): c = /k/, cx = ch, x = sh, ù = ü alemana, "
                 "y glifos propios para r suave / RR española / R grasseyé / LL. El OCR lee uno de esos "
                 "glifos como `л`; `Cxaлúa` = Charrúa fija que л = RR. Aquí se translitera a rr."),
  "clave_propuesta": ("la forma de Perea sin el prefijo verbal a- y sin el sufijo de infinitivo -n / "
                      "-n-nua, con sus guiones: a-dumki-n → dumki. Los estativos con atributivo "
                      "c-/k- lo conservan (c-a-ima «ser malo» ≠ ima «enemigo»). Es la misma convención "
                      "que las 173 raíces del Fraseario ya fusionadas."),
  "etiqueta_propuesta": "comparanda lokono atestiguada (Schumann 1755 vía Perea 1942). Ninguna es caquetía.",
  "cobertura_medida": {
    "verbos_listados": len(filas),
    "nuevos_para_el_lexicon": len(nuevas),
    "ya_en_lexicon_misma_clave": len(corrob),
    "corroboraciones_por_concepto_con_otras_fuentes": len(CONCEPTO),
    "divergencias_con_otras_fuentes": len(DIVERGEN),
    "voces_sueltas_no_verbales": len(sueltas),
  },
 }
}
out.write(dump(meta))
out.write("\nadvertencias:\n")
out.write(dump([
 "Perea, pp. 683-684: la gramática de Schumann «puede ser considerada como un simple ensayo» y de la p. 664 en adelante «asume el carácter de un simple borrador». Los paradigmas de negación, recíprocos y con infijo son reconstrucciones de Perea por inducción, marcadas [ ] y [?] en la fuente. Las LISTAS DE VERBOS no: ésas son el vocabulario, y es lo que aquí se propone.",
 "Perea sospecha (p. 606) que el aparato de TIEMPO de los pretéritos es «perfeccionamiento a priori de los misioneros». Los sufijos -bi / -buna / -cuba / -pa se registran como lo que Schumann declara, no como sistema verificado en el habla.",
 "El pronombre va PREFIJADO en los transitivos (d-a-, b-a-, l-a-…) y POSPUESTO en los estativos de la 4ª y 5ª conjugación (halli-kebbe de, cakù-ca de). Perea mismo dice que el empleo de Schumann «es por demás arbitrario» (p. 683).",
 "La misma raíz aparece a veces en dos clases con dos vocales (a-canaba-n / a-canabù-n «oír»; a-sucusa-n / a-sucusu-n «lavar»; a-cai-da-n / a-cai-dù-n «romper»). Perea lo atribuye al cambio de la vocal final «según el tiempo verbal o la presencia del acusativo» (p. 614). Son UNA raíz, no dos.",
 "Homógrafos con el español: casa-n «engendrar», a-carta-n «enterrar», a-manta-n «afilar», a-ca-n «lavarse», a-sa-n «nombrar», ide-n, pere-n, tere-n, case-n, a-usa-n. Si entran al lexicón tienen que ir con clave desambiguada (`-lokono`), porque score_linguistico() cuenta como arahuaco cualquier token igual a una clave y no filtra por fuente.",
]))
out.write("\n# ══ los verbos, por conjugación ══\n")
out.write("verbos:\n" + dump(filas))
out.write("\n# ══ voces no verbales que salen de paso ══\n")
out.write("sueltas:\n" + dump(sueltas))
out.write("\n# ══ corroboraciones POR CONCEPTO con la columna lokono de otras fuentes (segunda atestación, estrato 1755) ══\n")
out.write("corroboraciones_por_concepto:\n" + dump([
    {"perea": a, "lexicon": b, "concepto": c,
     "glosa_lexicon": V[b]["sig"] if b in V else None,
     "de_donde_viene": (V[b].get("notas", "")[:70] if b in V else None)}
    for a, b, c in CONCEPTO]))
out.write("\n# ══ divergencias con la columna lokono de otras fuentes — punto de medida, no error ══\n")
out.write("divergencias:\n" + dump([{"perea": a, "lexicon": b, "lectura": c} for a, b, c in DIVERGEN]))
out.write("""
# ══ lo que este capítulo cubre del hueco que el Fraseario dejaba ══
campo_material_y_ecologico:
  aviso: >-
    La ficha de la fuente decía que el Fraseario «deja intacto el hueco del
    léxico ecológico y material». El vocabulario de Schumann lo cubre en
    parte — no en fauna ni flora, pero sí en las ACCIONES sobre el medio:
  voces:
    - 'a-budi-di-n pescar · a-sia-n pescar con nasa · a-yali-di-n envenenar con tóxico vegetal (pesca con barbasco)'
    - 'a-iyucu-n / a-iyuca-n cazar · a-maroa-da-n cazar con flechas de madera'
    - 'a-cohùn-ti-n / a-bbunnù-n plantar · a-iyaha-dda-n arrancar yuca · ereke-n desherbar · calli yuca'
    - 'a-ccabba-tù-n salar · a-bucu-n hervir · a-iyaha-dù-n asar · barba-coa cañizo para secar o ahumar · ide-n estar muy cocido'
    - 'a-ccu-da-n hilar · a-ddura-n / a-ccarku-dù-n tejer, trenzar · a-rrusu-ttu-n edificar · a-ruru-tu-n hacer barroso'
    - 'colores y cualidades: cule-n rojo · subu-le-n verde · caii-me-n negro · hehe-n pálido · seme-n dulce · sipe-n amargo · bele-n blando · were-be-n caliente · hebbe-n viejo · emelie-n nuevo · ibe-n lleno · ipi-lli-be-n grande · móa-di-n corto · wai-kille-n ancho · ùsa-n bueno · c-a-ima-n malo'
  por_que_importa: >-
    Son conceptos de la lista de Swadesh y del léxico básico que el caquetío
    atestiguado sí cubre en parte (colores, comida, pesca). Es justo el
    material con que una retroabstracción se puede CONTRASTAR en vez de
    inventarse. Con el límite de siempre: esto es lokono de las Guayanas de
    1755, no caquetío.
""")
dest = os.path.join(R, "6-fusion", "lokono_verbos_perea_1942.yaml")
io.open(dest, "w", encoding="utf-8", newline="\n").write(out.getvalue())
print(f"verbos {len(filas)} · nuevos {len(nuevas)} · misma clave ya en lexicón {len(corrob)} · sueltas {len(sueltas)}")
print("ya en lexicón:", [f['clave'] for f in corrob])
