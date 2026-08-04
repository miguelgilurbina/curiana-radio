"""
CURIANA — Minería del *Glosario de voces indígenas de Venezuela* (Alvarado 1921)
===============================================================================

    Alvarado, Lisandro (1921). "Glosario de voces indígenas de Venezuela".
    Ediciones Victoria, Caracas. 354 pp.
    → fuentes_caquetios/Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf

REGLA CERO (protocolo `investigacion/disenos/02_protocolo_habla_paraguanera.md`):

    **Una voz de Alvarado NO es caquetía por defecto.** Alvarado compila voces
    indígenas de TODA Venezuela: caribe, cumanagoto, chaima, tamanaca, taíno,
    guajiro, quechua, nahua, y antillanismos ya castellanizados. La mayor parte
    NO es caquetío. Este script se juzga por el rigor de su filtro de descarte,
    no por el número de hallazgos.

El proyecto ya cometió el error contrario: 441 formas generadas sin verificar
cognación, ~80% falsas, hubo que aislarlas en `lexicon_candidatos.py`.

QUÉ HACE ESTE SCRIPT
--------------------
1. Extrae el glosario del PDF con `pdftotext` (NO con pypdf: pypdf devuelve
   vacío en este archivo, y por eso F3 figuró un año como "bloqueada por falta
   de OCR"). Devuelve ~1568 lemas con su **página impresa**.
2. Aplica los **6 filtros de descarte** del protocolo §3, apoyándose sobre todo
   en el propio metalenguaje de Alvarado: él marca la lengua de origen
   ("Voz cum.", "voz cháima", "Del guajiro…", "Voz taina", "Del azt.") y cita
   sus fuentes con siglas (`Ov.`=Oviedo, `Cast.`=Castellanos, `Carv.`=Carvajal,
   `Cas.`=Las Casas, `Cod.`=Codazzi).
3. Puntúa los **criterios positivos** (§4) y emite el nivel **A/B/C/D** (§5).
   La señal positiva más fuerte es geográfica: `Coro`, `Falcón`, `Paraguaná`,
   `Occ.` (= Zulia, Falcón, Lara, Yaracuy, según la propia tabla de
   abreviaturas, p. XVIII) y la mención explícita de los Caquetíos.
4. **Adjudica las 82 entradas de familia caquetía sin cita** del lexicón
   (tarea F1): las busca en Alvarado y dice si la fuente las **confirma**, las
   **reclasifica** o es **no concluyente**.

POLÍTICA D7 (decidida 2026-08-03): cuando la glosa histórica y la
identificación moderna difieren, se registran LAS DOS en campos separados
(`glosa_fuente` verbatim + `identificacion_moderna`). Ninguna gana; el
conflicto queda visible.

NO modifica `curiana_lexicon.py`. Emite propuesta (`lexicon_alvarado.py`) para
revisión humana, en la misma disciplina que `minar_zavala_glosario.py`.

Uso:
    python minar_alvarado_glosario.py                    # informe
    python minar_alvarado_glosario.py --82               # solo la auditoría F1
    python minar_alvarado_glosario.py --json out.json
    python minar_alvarado_glosario.py --generar-modulo   # → lexicon_alvarado.py
"""

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

# La consola de Windows es cp1252 y este glosario está lleno de acentos y de
# comillas tipográficas del OCR de 1921. Sin esto el script revienta con
# UnicodeEncodeError (bug conocido de minar_zavala_glosario.py).
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PDF_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "fuentes_caquetios",
    "Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf",
)

# El cuerpo del glosario empieza en la página 31 del PDF, que lleva impreso el
# número 1. Verificado en 4 puntos (pdf 101→71, 201→171, 301→271, 346→316).
OFFSET_PAGINA = 30

MAY = "A-ZÁÉÍÓÚÑÜ"
_HEADER = re.compile(
    r"GLOSARIO\s+D[EÉ]\s+VOCES\s+IND[IÍ]GENAS|^\s*DE\s+VENEZUELA\s*$", re.M)
_LEMA = re.compile(
    rf"(?:(?<=^)|(?<=[.\s]))\*?([{MAY}][{MAY}ÏÜ'’\-]{{2,20}}(?:,\s*[AO])?)\.\s+"
    rf"(?=[A-ZÁÉÍÓÚÑÜa-záéíóúñü\"“(])")
_NO_LEMA = {"glosario", "venezuela", "voces", "indigenas", "sin", "sinn", "ref",
            "reff", "vease", "id", "ibid", "cf", "dt", "ut", "vg", "esp", "ver"}


# ══════════════════════════════════════════════════════════════════════
# §3 — LOS SEIS FILTROS DE DESCARTE (en orden de aplicación)
# ══════════════════════════════════════════════════════════════════════
# Cada filtro se apoya en lo que **la propia fuente declara**. No se adivina
# el origen de una voz: se lee la atribución de Alvarado.

FILTROS = [
    ("F1_espanol", re.compile(
        r"\bdel ant\.|voz castellana|voz espa[ñn]ola|del espa[ñn]ol\b|"
        r"andaluz|canari[ao]|del lat[íi]n|voz latina|del portugu[ée]s", re.I)),
    ("F2_papiamento_neerlandes", re.compile(
        r"papiamento|holand[ée]s|neerland[ée]s|\bCurazao\b|\bAruba\b|\bBonaire\b", re.I)),
    ("F3_wayuu_guajiro", re.compile(
        r"\bdel guaj[íi]ro\b|\bguaj[íi]ro\b|\bgoaj[íi]ro\b|\bGuag[íi]ro", re.I)),
    ("F4_taino_panamericano", re.compile(
        r"voz taina|voz ta[íi]na|\bta[íi]n[oa]\b|del quichua|voz quichua|"
        r"del azt\.|azteca|mejicano|guaran[íi]|del quechua|\ben Cuba\b|"
        r"\bAntillas\b|Espa[ñn]ola\b|Hait[íi]|del ar[áa]bigo|ar[áa]big[ao]", re.I)),
    ("F5_africanismo", re.compile(
        r"africa|de negros|baile de negros|congo|mandinga|bant[úu]", re.I)),
    ("F6_caribe_jirajaroide", re.compile(
        r"\bvoz cum\.|\bcum\.\s|voz ch[áa]ima|\bch\.\s|chaima|cumanagot|"
        r"tamanac|\bcar\.\s|lengua caribe|lenguas caribes|voz caribe|"
        r"origen caribe|\bcal[íi]nago|\bcalina\b|galibi|\bkal\.\s|\btam\.\s|"
        r"ayam[áa]n|gay[óo]n|jiraj|\bar[ée]c\.|arecuna|\bmaip\.|s[áa]liba|"
        r"\bbar[ée]\b|macusi|acavayo|guam[oa]s\b", re.I)),
]

# ══════════════════════════════════════════════════════════════════════
# §4 — CRITERIOS POSITIVOS
# ══════════════════════════════════════════════════════════════════════

# Criterio 2 (distribución restringida) — la señal más discriminante que
# ofrece Alvarado. `Occ.` = Zulia, Falcón, Lara, Yaracuy (tabla de
# abreviaturas, p. XVIII): incluye territorio caquetío pero también jirajaroide
# y motilón, así que vale MENOS que "Coro" o "Paraguaná".
SENAL_NUCLEO = re.compile(r"\bCoro\b|\bFalc[óo]n\b|\bParaguan[áa]\b|Cumaragua|"
                          r"Adicora|\bMoruy\b|coriano", re.UNICODE)
SENAL_AMPLIA = re.compile(r"\bOcc\.|Occidente\b", re.UNICODE)
# Criterio 6 (atestación colonial temprana) — siglas de cronista en la entrada.
SENAL_COLONIAL = re.compile(r"\(Ov\.|\(Cast\.|\(Carv\.|\(Cas\.\s|\(Gum\.|"
                            r"Oviedo|Castellanos|Carvajal|Las Casas|Aguado|Cisn\.", re.I)
# Mención explícita del pueblo caquetío: la evidencia más fuerte posible.
SENAL_CAQUETIA = re.compile(r"Caquet[íi]o", re.UNICODE)
# Criterio 1 (campo semántico local e intraducible): fauna, flora, paisaje,
# técnica. Alvarado marca con "indeterminado/a" justo las voces que la ciencia
# de 1921 NO pudo traducir a un taxón — es decir, las MENOS castellanizables.
CAMPO_CONCRETO = re.compile(
    r"[áa]rbol|arbusto|planta|yerba|hierba|palmera|cact|cardón|cardo|fruto|"
    r"semilla|fibra|madera|ave\b|p[áa]jaro|paloma|pez|peces|caracol|molusco|"
    r"insecto|avispa|abeja|hormiga|zorro|lagart|saurio|serpiente|animal|"
    r"r[íi]o|quebrada|cerro|sima|salina|arena|m[ée]dano|costa|mar\b|monte|"
    r"vasija|tinaja|asiento|cesto|bebida|licor|comida|tinte|tint[óo]re", re.I)
INDETERMINADO = re.compile(r"indeterminad[oa]|no bien determinad|"
                           r"especie indeterminada|\(\s*\?\s*\)", re.I)

# ══════════════════════════════════════════════════════════════════════
# CURACIÓN MANUAL — leídas entrada por entrada (2026-08-03)
# ══════════════════════════════════════════════════════════════════════
# La heurística tria; el veredicto final de estas lo puso una lectura humana.
# Formato: forma → (nivel, razón). Documentar el descarte vale tanto como el
# hallazgo: evita que alguien re-mine la misma voz dentro de seis meses.

VEREDICTOS_CURADOS: dict[str, tuple[str, str]] = {
    # ── A — atestación colonial o atribución caquetía explícita ──
    "poporo": ("A", "Alvarado la atribuye EXPLÍCITAMENTE a los antiguos Caquetíos "
                    "(y a los Guajiros), citando a Castellanos. Es la única voz de todo "
                    "el glosario con atribución caquetía directa."),
    "mene": ("A", "Atestación colonial de primera (Oviedo II.301) + localización en Coro "
                  "y Maracaibo (Codazzi). Campo semántico local e intraducible."),
    "maure": ("A", "Atestada por Carvajal y Castellanos como faja/tejido, y viva en Coro "
                   "en 1921 con la acepción de 'pieza de dril'. Doble anclaje: colonial "
                   "y coriano."),
    # ── B — sobrevive a los 6 filtros + señal de Coro/Falcón/Paraguaná ──
    "cumaragua": ("B", "Única voz del glosario localizada en PARAGUANÁ. Campo semántico "
                       "local (fauna marina). ⚠ CONFLICTO DE GLOSA con el lexicón: "
                       "ver identificacion_moderna."),
    "aiton": ("B", "'Sima profunda' del E. Falcón: término de PAISAJE, exactamente el "
                   "hueco léxico que ecologia_lexicon_map.md daba por vacío. Sin "
                   "competidor identificado en ninguno de los 6 filtros."),
    "tocororo": ("B", "'Tallo leñoso del cirio o cardón' (Lara, Falcón): nombra una parte "
                      "del cardón, planta central del paisaje caquetío. Sin filtro."),
    "urupagua": ("B", "Árbol de Coro, indeterminado en 1921 (la ciencia no supo darle "
                      "taxón: señal de voz local no castellanizable)."),
    "urupaguita": ("B", "Diminutivo de urupagua, Coro. Confirma que la raíz es productiva "
                        "en el habla local."),
    "cusuca": ("B", "Árbol frutal silvestre de Coro. Indeterminado. Sin filtro."),
    "manata": ("B", "Árbol indeterminado de Coro. Sin filtro."),
    "mapuare": ("B", "Árbol indeterminado de Coro. Sin filtro."),
    "pirota": ("B", "Árbol indeterminado de Coro. Sin filtro."),
    "isicagua": ("B", "Árbol medicinal de Coro (Ernst conjetura Protium). Sin filtro."),
    "achichive": ("B", "Árbol indeterminado de Coro. Sin filtro."),
    "aripino": ("B", "Árbol indeterminado de Coro. Sin filtro."),
    "camare": ("B", "Arbusto indeterminado de Coro. Sin filtro."),
    "boque": ("B", "Árbol indeterminado de Coro. Sin filtro."),
    "chiguare": ("B", "Árbol indeterminado de Coro (var. chihuare). Sin filtro. "
                      "⚠ No confundir con el chiriguare (ave carroñera) del lexicón."),
    "guacuaro": ("B", "Palo de tinte de Coro. Técnica local (tintorería). Sin filtro."),
    "sibucaro": ("B", "Ceiba de Coro cuya corteza se usa en cordelería: técnica local."),
    "cuaguaro": ("B", "Árbol maderable del E. Falcón. Sin filtro."),
    "chiriga": ("B", "Árbol de construcción del E. Falcón. Sin filtro."),
    "guaitoco": ("B", "Árbol de construcción del E. Falcón. Sin filtro."),
    "maque": ("B", "Árbol maderable del E. Falcón. Sin filtro."),
    "lauadri": ("B", "Árbol indeterminado del E. Falcón (var. laguadrí). Sin filtro."),
    "araguan": ("B", "Árbol maderable de Lara y Falcón. Sin filtro."),
    "barisigua": ("B", "Árbol indeterminado de Coro y Zulia. Sin filtro."),
    "barimiso": ("B", "Árbol indeterminado de Lara, Coro y Zulia. Sin filtro."),
    "anuano": ("B", "Árbol indeterminado de Coro y Yaracuy. Sin filtro."),
    "ipunano": ("C", "'Alfarda', usada en Coro y Barcelona. La coocurrencia con Barcelona "
                     "(oriente caribe) debilita la atribución local."),
    # ── C — sobrevive pero solo con señal `Occ.`, o campo semántico flojo ──
    "bariqui": ("C", "Planta tintórea de Occ.; pero Alvarado la asocia al tinte de los "
                     "indios AYAMANES (jirajaroide) → roza el filtro 6."),
    "canoito": ("C", "Árbol de Occ. útil en construcción, pero el mismo nombre existe en "
                     "el Guárico: distribución NO restringida."),
    "pororo": ("C", "Árbol de fruto comestible de Occ., sin más precisión."),
    "camburito": ("C", "Cactus de las sabanas septentrionales de Coro, pero el lema es un "
                       "diminutivo romance de 'cambur': formación local moderna, no sustrato."),
    "capadare": ("C", "Es un topónimo de Falcón usado como marca comercial de tabaco, no "
                      "una voz del habla. Valor de canon toponímico, no léxico."),
    # ── D — cae en un filtro ──
    "auyama": ("D", "F4/F6: Alvarado la marca 'Voz cum.' (cumanagota, familia caribe) y "
                    "cita a Ruiz Blanco. Además es panvenezolana."),
    "guatapanar": ("D", "F6: Alvarado deriva la forma del cum. 'araguatapanár' (oreja de "
                        "araguato). Es la voz que el lexicón registra como watapana."),
    "dividive": ("D", "F4: nombre panvenezolano/pancaribeño de Caesalpinia coriaria; "
                      "Alvarado registra además 'Guatapaná, en Cuba'."),
    "conuco": ("D", "F4: 'Voz taina' explícita (Las Casas). Es el étimo del kunuku del "
                    "lexicón, vía español."),
    "piache": ("D", "F6: 'Voz cháima y tamanaca, con formas afines en otras lenguas "
                    "caribes'. NO es arahuaca."),
    "ture": ("D", "F6: 'Voz cháima' (Tauste), usada en Cumaná y Margarita — oriente "
                  "caribe, no Coro. Además la glosa es 'asiento pequeño', no 'vasija'."),
    "butaque": ("D", "F6: el equivalente occidental del ture chaima; voz de circulación "
                     "nacional."),
    "duro": ("D", "F6: Alvarado lo identifica con el 'dure de los Caribes' (Carvajal)."),
    "pauji": ("D", "F6: Alvarado deriva el fitónimo del chaima. Además la glosa es un "
                   "ÁRBOL (Bumelia buxifolia), no un ave."),
    "guacoa": ("D", "F6: del calínago 'uahikua', cum. 'huakúa', ch. 'guakúa'."),
    "camuro": ("D", "F3: 'Del guajiro amuru, árbol de las calabazas' (A. Rojas)."),
    "tequiara": ("D", "F3: 'Del guajiro tekiara, lo mismo'."),
    "chapapote": ("D", "F4: 'Del azt. chapápotl' — nahuatlismo, pese a citarse en la "
                       "Costa de Coro."),
    "guaca": ("D", "F4: 'Voz taina' en la acepción de tesoro escondido."),
    "curiara": ("D", "F6: 'Voz de origen caribe' (kuliála / kuriara / kuliára)."),
    "hamaca": ("D", "F4: antillanismo panamericano; Alvarado discute taíno vs. caribe y "
                    "señala que fue aceptada 'en todos los idiomas civilizados'."),
    "manare": ("D", "F6: voz de circulación nacional documentada por Caulín en misiones "
                    "caribes; no hay anclaje coriano."),
    "chimbanquele": ("D", "F5: baile afrodescendiente en honor de S. Benito (Coro y Zulia). "
                          "Es cultura colonial afro, no sustrato indígena."),
    "chimbique": ("D", "F5: variante de chimbánguele; mismo descarte."),
    "tamunango": ("D", "F5: 'Baile de negros en Coro, en honor de San Antonio'."),
    "adorote": ("D", "F6: documentado por Carvajal en el Apure; 'Us. en Occ.' es difusión, "
                     "no origen."),
    "chirgua": ("D", "F6: 'Usábanla los indios Guamos' y 'en sáliba chírua'."),
    "dibibe": ("D", "F6: 'Voz ayamán o gayón' — jirajaroide, no arahuaco."),
    "dispopo": ("D", "F6: 'Créese que es voz ayamán-gayón'."),
    "tura": ("D", "F6: el baile de Tura es de tradición ayamán/gayón (Churuguara, Falcón), "
                  "jirajaroide. Localización correcta, filiación equivocada."),
    "cipote": ("D", "F1/F4: Alvarado la compara con el chipote nicaragüense (Gagini); "
                    "circulación centroamericana."),
    "capucero": ("D", "F1: epíteto político venezolano de 1858, formación romance moderna."),
    "garitear": ("D", "F1: verbo romance derivado de 'carite'."),
    "guarear": ("D", "F1: verbo romance derivado de 'guaro'."),
    "cujisal": ("D", "F1: colectivo romance en -al sobre 'cují'."),
    "hicaquito": ("D", "F1: diminutivo romance de 'hicaco' (antillanismo)."),
    "nopal": ("D", "F4: 'Del azt. nopal' (Gómara); la mención de Coro es descriptiva."),
    "caucho": ("D", "F4: voz amazónica de circulación panamericana; la entrada no toca "
                    "Coro (falso positivo del regex por 'Occ.')."),
    "chimo": ("D", "F1/F6: producto andino-venezolano; el urao remite a Mérida, no a Coro."),
    "chorote": ("D", "F1: voz de circulación nacional; la mención de Occidente es de "
                     "difusión ('cerrero en Occidente'), no de origen."),
    "purupuru": ("D", "F4: Alvarado la compara con el piripiri peruano; además crece en "
                      "montañas de Occ. y Carabobo — distribución no restringida."),
    "guaro": ("D", "F6: Alvarado dice explícitamente que la voz NO se usa en Occ. "
                   "('uarro es loro en carúsana')."),
    "guagua": ("D", "F4: 'guagua' es voz quechua/antillana de amplísima difusión; la "
                    "acepción de haba coriana no basta."),
    "guairon": ("D", "F1: aumentativo romance de 'guaira'."),
    "mulato": ("D", "F1: voz romance; la entrada es un fitónimo descriptivo."),
    "maruto": ("D", "F1/F4: acepciones dispersas (Alto Llano, Aragua, Coro) sin unidad; "
                    "distribución no restringida."),
    "choi": ("D", "F1: 'Us. en Mérida' — andina, no coriana (falso positivo por 'Occidente' "
                  "en la entrada contigua CHOLA)."),
    "cipero": ("D", "F1: la entrada no localiza en Falcón; falso positivo del regex."),
    "caimoni": ("D", "F1: la entrada no localiza en Falcón; falso positivo del regex."),
    "parcpta": ("D", "OCR corrupto de PARCHITA; voz de circulación nacional."),
    "bobo": ("D", "artefacto de parseo (la entrada arrastra GUÁL/GUACHITO); no evaluable."),
    "tococo": ("D", "F1: pelícano, voz de circulación costera nacional (Codazzi)."),
    "tuque": ("D", "F1: crece en Carabobo, Cojedes, Lara y Falcón — distribución amplia."),
    "chachipo": ("D", "F6: el arecuna kasipa está citado en la propia entrada."),
    "cachipo": ("D", "F6: 'arec. kasipa' en la propia entrada; la acepción coriana "
                     "('colérico') es un uso secundario, no el origen."),
    "carebe": ("D", "F6: el propio Alvarado dice que es 'voz tomada de algún dialecto "
                    "andino' (cf. guagibo kariepa) y que en Oriente se desconoce."),
    "cobalonga": ("D", "F4: nuez de lauríneas amazónicas (Licaria/Ocotea), de circulación "
                       "comercial por arriería; 'Occidente y la Cordillera' es difusión."),
    "mojanazo": ("D", "F6/F1: derivado romance de *mohán*, voz andina; la localización en "
                      "Occidente es de uso, no de origen."),
    "piritu": ("D", "F6: 'En car. piritu, en cum. piríchu, lo mismo'. Crece en Lara, Coro y "
                    "Yaracuy, pero la voz es caribe. ⚠ El lexicón la tiene como `caquetío` "
                    "(vía Zavala #—, sigla A): candidata a reetiquetar en F1."),
    "guaraba": ("C", "Brownea guaraba Pittier, 'Occidente'. Sobrevive a los 6 filtros pero "
                     "la única señal es la amplia (Occ.), sin anclaje coriano."),
    "surupa": ("C", "Blatta orientalis (cucaracha). Alvarado la compara con el guajibo "
                    "*cucaréicha* y con CHIRÍPA; la señal es de familia, no local. ⚠ En esta "
                    "entrada 'curiana' aparece como palabra ESPAÑOLA para cucaracha."),
    "caquetillo": ("C", "'Árbol de construcción del Zulia. ¿Voz afín de caquetío?' — la "
                        "pregunta es del propio Alvarado, y queda sin responder. Se registra "
                        "por su interés etnonímico, no como voz del habla."),
    "turupia": ("B", "'Especie de acacia o cují de Coro'. Campo semántico local (flora "
                     "xerófila), sin filtro."),
}

# ══════════════════════════════════════════════════════════════════════
# F1 — LAS 82 ENTRADAS DE FAMILIA CAQUETÍA SIN CITA
# ══════════════════════════════════════════════════════════════════════
# El siguiente paso del backlog (F1) tiene que auditarlas. Este script busca
# cada una en Alvarado y adjudica. `confirma` / `reclasifica` / `no-concluyente`.
# El veredicto es curado a mano; la EVIDENCIA (página + texto verbatim) la
# extrae el script, de modo que siempre se puede volver a comprobar.

LAS_82 = """amaca apana ateri auyama bajarí barici bariki borojo buco buiamati buko bureche
buriche cachicamo caduchi caraota cari catarí cati cazebo cazi cazicure cazá chacamba chiriguare
chogogo chuchubi corie coro cudan cudanga cumaragua curiana cuté dare datihao duraboa eroa
garabal gua guaitiao guanepe gudamuen güere güique humocaro iero jacuque jacura jaguey jai
kadushi kama koke kukuisa kunuku maure mazato mene na pariri paro pauji piache poporo quidi
rao sabuenen saruro sawaka tabri tara tarica tata tebe tuqueque ture ucibo urapa wabarsure
warawara watapana""".split()

# forma_lexicon → (veredicto, forma_en_alvarado_o_None, razón)
ADJUDICACION_82: dict[str, tuple[str, str | None, str]] = {
    "poporo": ("confirma", "POPORO",
               "Alvarado la atribuye a los antiguos Caquetíos y cita a Castellanos. "
               "La glosa del lexicón ('maza-porra, arma de combate') coincide. "
               "→ `caquetío-atestiguado` queda JUSTIFICADO, con cita."),
    "mene": ("confirma", "MÉNE",
             "Oviedo II.301 ('betún a manera de brea') + Codazzi localiza los "
             "yacimientos en Coro y Maracaibo. Glosa del lexicón compatible."),
    "maure": ("confirma", "MÁURE",
              "Carvajal 168 y Castellanos la registran como faja/tejido; en Coro vivía "
              "en 1921 como 'pieza de dril'. La glosa del lexicón ('fibra, hilo para "
              "tejer') es compatible."),
    "tuqueque": ("confirma", "TUQUEQUE",
                 "Glosa idéntica (geco: Thecadactylus rapicaudus / Gonatodes albogularis). "
                 "Pero Alvarado NO da origen ni localiza en Coro: confirma la GLOSA, "
                 "no la filiación caquetía."),
    "cachicamo": ("confirma", "CACHICAMO",
                  "Glosa idéntica (Dasypus). Voz de circulación nacional, sin origen "
                  "declarado: confirma la glosa, no la filiación."),
    "mazato": ("confirma", "MAZATO",
               "Oviedo II.297,300 ('magato… brevaje'). Confirma la glosa. La forma es "
               "panamericana (masato peruano): filiación caquetía NO confirmada."),
    "buco": ("confirma", "BUCO",
             "'Caz, acequia' — la glosa del lexicón ('represa, canal') es compatible. "
             "⚠ Alvarado la localiza en Lara y sugiere origen romance ('¿del ant. buca, "
             "boca?'): confirma la glosa, DUDA de la filiación."),
    "guanepe": ("reclasifica", "GUANEPE",
                "Confirma la glosa ('cabestrillo en que las madres llevan sus niños') "
                "pero la localiza en BARCELONA y GUAYANA — oriente caribe, no Coro. "
                "La atribución caquetía pierde su base geográfica."),
    "cumaragua": ("reclasifica", "CUMARAGUA",
                  "CONFLICTO DE GLOSA (D7): Alvarado = 'especie de caracol de las costas "
                  "de Paraguaná'; el lexicón = 'ciruela, Spondias mombin'. La localización "
                  "es la mejor de todo el glosario, pero la glosa del lexicón no se sostiene."),
    "auyama": ("reclasifica", "AUYAMA",
               "'Voz cum.' (cumanagota) según Ruiz Blanco, con variantes ayuyáma / huyáma. "
               "Familia CARIBE, no arahuaca: la etiqueta `caquetío-atestiguado` es errónea."),
    "piache": ("reclasifica", "PIACHE",
               "'Voz cháima y tamanaca, con formas afines en otras lenguas caribes'. "
               "Es la palabra para chamán: el error es visible en toda la simulación."),
    "ture": ("reclasifica", "TURE",
             "Doble reclasificación: la glosa es 'asiento pequeño' (no 'vasija de barro') "
             "y la lengua es cháima (Tauste), usada en Cumaná y Margarita."),
    "pauji": ("reclasifica", "PAUJÍ",
              "CONFLICTO DE GLOSA (D7): en Alvarado paují es un ÁRBOL (Bumelia buxifolia, "
              "Sapotáceas; cf. IGÜÍ p.175 'Paují… Coro'), derivado del chaima. El lexicón "
              "lo glosa como ave ('pavo de monte')."),
    "watapana": ("reclasifica", "GUATAPANAR",
                 "Alvarado registra la forma venezolana GUATAPANAR y la deriva del cum. "
                 "'araguatapanár' (oreja de araguato). La forma *watapana* del lexicón es "
                 "la papiamenta de las islas ABC (→ van-buurt-2014), no un caquetío "
                 "atestiguado en tierra firme."),
    "kunuku": ("reclasifica", "CONUCO",
               "Alvarado: 'Voz taina' (Las Casas V.307). *kunuku* es la forma papiamenta "
               "del español *conuco*, taíno de origen. Filtro 4."),
    "kukuisa": ("reclasifica", "COCUIZA",
                "La forma venezolana atestiguada es COCUIZA (Furcraea spp.), de circulación "
                "nacional. Peor aún: Alvarado cita a Caulín (I.3) — 'una especie de pita que "
                "los indios llaman CARUATA y los españoles COCUIZA' (voz chaima; tam. "
                "karuatá, cum. karúata). Es decir, *cocuiza* es el nombre del lado ESPAÑOL. "
                "*kukuisa* es su forma papiamenta."),
    "caraota": ("reclasifica", "CARAOTA",
                "Alvarado la describe como nombre corriente panvenezolano de las judías, "
                "sin origen indígena declarado. Filtro 4: no prueba nada local."),
    "bureche": ("reclasifica", "BURECHE",
                "CONFLICTO DE GLOSA (D7): en Alvarado es una BEBIDA fermentada de los "
                "indios guayaneses; el lexicón lo registra como verbo 'hacer, fabricar'. "
                "La glosa de bebida coincide en cambio con *buriche* del propio lexicón."),
    "cuté": ("no-concluyente", "CUTÉ",
             "El lema existe (p.110) pero solo remite a CARATE (enfermedad de la piel). "
             "Homógrafo: no dice nada sobre el pronombre dativo del lexicón."),
    "amaca": ("no-concluyente", "HAMACA",
              "Solo aparece como variante de *hamaca* (antillanismo). No hay rastro de la "
              "glosa del lexicón ('sitio de moler maíz')."),
    "apana": ("no-concluyente", "ÑAPA",
              "Solo aparece como quichua *apana* 'añadidura' (étimo de ñapa). Homógrafo: "
              "nada que ver con 'una luna'."),
    "curiana": ("no-concluyente", None,
                "No es lema. Aparece UNA vez, y como palabra ESPAÑOLA para cucaracha "
                "(s.v. SURÚPA). El topónimo Curiana no está en el glosario."),
    "coro": ("no-concluyente", None,
             "'Coro' aparece 55 veces, siempre como TOPÓNIMO. No hay lema CORO con la "
             "glosa 'cardón' que le da el lexicón."),
    "tara": ("no-concluyente", None,
             "No es lema autónomo. En el glosario 'tara' aparece como polilla/mariposa "
             "(cf. TARÍTA 'mariposa o tara pequeña'), no como venado."),
    "tata": ("no-concluyente", None,
             "Solo en 'tata-cuá' (indígenas de Mérida) y en 'patata'. 'Tata' = padre es "
             "panamericano y romance-infantil: no sirve como evidencia."),
    "chiriguare": ("no-concluyente", None,
                   "No es lema, pero aparece dos veces en refranes ('Después que samuro "
                   "come, chiriguare roe'), lo que CONFIRMA la glosa de ave carroñera. "
                   "Sin origen ni localización: no adjudica la filiación."),
    "cari": ("no-concluyente", None,
             "No es lema; solo aparecen CARICARE, CARITE, CARITIVÁ. Sin evidencia."),
    "cati": ("no-concluyente", None,
             "Único hit es el latín 'Unguis Cati' en un nombre científico. Sin evidencia."),
    "cazá": ("no-concluyente", None,
             "Los hits son la palabra española 'caza'. Sin evidencia."),
    "gua": ("no-concluyente", None,
            "Solo aparece dentro de compuestos (guaca, guacamaya…). Sin evidencia."),
    "güere": ("no-concluyente", None,
              "Único hit: el río Güere del E. Anzoátegui — topónimo oriental. Sin "
              "evidencia para la glosa 'dar, entregar'."),
    "dare": ("no-concluyente", None,
             "Único hit dentro de 'budare'. Sin evidencia."),
    "na": ("no-concluyente", None,
           "Los hits son la elisión coloquial de 'nada'. Sin evidencia."),
    # Las papiamentas y las que no dejan rastro ninguno.
    "kadushi": ("no-concluyente", None,
                "AUSENTE del glosario, y también su equivalente castellano no aparece "
                "como lema. Consistente con un origen papiamento (islas ABC) → F2, no "
                "con un caquetío de tierra firme documentado en 1921."),
    "chuchubi": ("no-concluyente", None, "AUSENTE. Igual que kadushi: forma papiamenta."),
    "chogogo": ("no-concluyente", None, "AUSENTE. Igual que kadushi: forma papiamenta."),
    "warawara": ("no-concluyente", None,
                 "AUSENTE (Alvarado registra GUARAGUAO como nombre del samuro en "
                 "Margarita, no *warawara*)."),
}
# El resto de las 82 no deja rastro alguno en Alvarado.
_SIN_RASTRO_RAZON = ("AUSENTE del glosario: ni como lema ni como mención. Alvarado no "
                     "adjudica ni a favor ni en contra.")


# ══════════════════════════════════════════════════════════════════════
# Extracción
# ══════════════════════════════════════════════════════════════════════

def norm(s: str) -> str:
    """minúsculas sin acentos, para comparar formas."""
    s = (s or "").lower().strip()
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _texto_pdf(pdf_path: str) -> str:
    """Extrae con pdftotext. pypdf devuelve VACÍO en este PDF (ver docstring)."""
    if not os.path.exists(pdf_path):
        sys.exit(f"No encuentro el PDF: {pdf_path}")
    exe = shutil.which("pdftotext")
    if not exe:
        sys.exit("Falta `pdftotext` (poppler). Es imprescindible: pypdf no lee este PDF.")
    tmp = os.path.join(tempfile.gettempdir(), "curiana_alvarado_1921.txt")
    if not os.path.exists(tmp) or os.path.getmtime(tmp) < os.path.getmtime(pdf_path):
        subprocess.run([exe, "-enc", "UTF-8", pdf_path, tmp], check=True)
    with open(tmp, encoding="utf-8") as f:
        return f.read()


def extraer(pdf_path: str = PDF_PATH) -> list[dict]:
    """Devuelve [{lema, pag, texto}] — `pag` es la página IMPRESA del glosario."""
    entradas = []
    for i, cruda in enumerate(_texto_pdf(pdf_path).split("\f")):
        pag = i + 1 - OFFSET_PAGINA
        if pag < 1:
            continue
        cuerpo = re.sub(r"-\n", "", cruda)          # une palabras cortadas
        cuerpo = _HEADER.sub(" ", cuerpo)           # quita encabezados repetidos
        cuerpo = re.sub(r"\s+", " ", cuerpo.replace("\n", " ")).strip()
        hits = list(_LEMA.finditer(cuerpo))
        for j, m in enumerate(hits):
            lema = m.group(1).rstrip(".,")
            if norm(lema).replace(",", "").strip() in _NO_LEMA:
                continue
            fin = hits[j + 1].start() if j + 1 < len(hits) else len(cuerpo)
            texto = cuerpo[m.end():fin].strip()
            if texto:
                entradas.append({"lema": lema, "pag": pag, "texto": texto})
    return entradas


def indexar(entradas: list[dict]) -> dict[str, dict]:
    """forma normalizada → la entrada más larga con ese lema."""
    idx: dict[str, dict] = {}
    for e in entradas:
        k = norm(e["lema"]).split(",")[0].strip()
        if k not in idx or len(e["texto"]) > len(idx[k]["texto"]):
            idx[k] = e
    return idx


# ══════════════════════════════════════════════════════════════════════
# Clasificación
# ══════════════════════════════════════════════════════════════════════

def filtros_que_disparan(texto: str) -> list[str]:
    return [nombre for nombre, rx in FILTROS if rx.search(texto)]


def evaluar(e: dict) -> dict:
    """Aplica descartes (§3), criterios positivos (§4) y nivel A/B/C/D (§5)."""
    t = e["texto"]
    forma = norm(e["lema"]).split(",")[0].strip()
    disparan = filtros_que_disparan(t)
    positivos = []
    if SENAL_CAQUETIA.search(t):
        positivos.append("atribución caquetía explícita")
    if SENAL_NUCLEO.search(t):
        positivos.append("localización Coro/Falcón/Paraguaná")
    elif SENAL_AMPLIA.search(t):
        positivos.append("localización Occ. (amplia)")
    if SENAL_COLONIAL.search(t):
        positivos.append("atestación colonial")
    if CAMPO_CONCRETO.search(t):
        positivos.append("campo semántico local")
    if INDETERMINADO.search(t):
        positivos.append("sin taxón en 1921 (no castellanizable)")

    # nivel automático
    if disparan:
        nivel, razon = "D", "descartada por " + ", ".join(disparan)
    elif "atribución caquetía explícita" in positivos or (
            "atestación colonial" in positivos and
            "localización Coro/Falcón/Paraguaná" in positivos):
        nivel, razon = "A", "atestación fuerte: " + "; ".join(positivos)
    elif ("localización Coro/Falcón/Paraguaná" in positivos and
          "campo semántico local" in positivos):
        nivel, razon = "B", "sobrevive a los 6 filtros; " + "; ".join(positivos)
    elif positivos:
        nivel, razon = "C", "sobrevive pero señal débil: " + "; ".join(positivos)
    else:
        nivel, razon = "D", "sin ninguna señal positiva de localización"

    curado = VEREDICTOS_CURADOS.get(forma)
    if curado:
        nivel, razon = curado[0], curado[1] + "  [curación humana]"

    return {**e, "forma": forma, "nivel": nivel, "razon": razon,
            "filtros": disparan, "positivos": positivos,
            "curado": bool(curado)}


def separar_glosa(texto: str) -> tuple[str, str]:
    """Política D7: separa la glosa verbatim de la identificación científica.

    Alvarado abre muchísimas entradas con el binomio latino. Ese binomio es la
    `identificacion_moderna`; el resto en castellano es la `glosa_fuente`, que
    es la que un agente hablaría.
    """
    m = re.match(r"\s*([A-ZÁÉÍÓÚ][a-zé]+(?:\s+[a-z][a-zé\-]+){1,2}\.?"
                 r"(?:\s*(?:sp\.(?:\s*pl\.)?|spp\.))?)\s*[.,]\s*", texto)
    ident, resto = "", texto
    if m and re.search(r"[a-z]{4}", m.group(1)):
        ident, resto = m.group(1).strip(" ."), texto[m.end():]
    # familia botánica/zoológica inmediatamente después
    m2 = re.match(r"\s*([A-ZÁÉÍÓÚ][a-zé]+(?:áceas|idos|ídeos|áceos))\.\s*", resto)
    if m2:
        ident = (ident + ", " + m2.group(1)).strip(", ")
        resto = resto[m2.end():]
    return " ".join(resto.split())[:240], ident


def clasificar(entradas: list[dict]) -> dict:
    """Triage completo. Solo evalúa a fondo lo que tiene señal geográfica."""
    con_senal = [e for e in entradas
                 if SENAL_NUCLEO.search(e["texto"]) or SENAL_AMPLIA.search(e["texto"])
                 or SENAL_CAQUETIA.search(e["texto"])
                 or norm(e["lema"]).split(",")[0].strip() in VEREDICTOS_CURADOS]
    evaluadas = [evaluar(e) for e in con_senal]
    # dedupe por forma, quedándose con el veredicto de mayor nivel
    orden = {"A": 0, "B": 1, "C": 2, "D": 3}
    mejor: dict[str, dict] = {}
    for e in evaluadas:
        if e["forma"] not in mejor or orden[e["nivel"]] < orden[mejor[e["forma"]]["nivel"]]:
            mejor[e["forma"]] = e
    res = {n: [] for n in "ABCD"}
    for e in sorted(mejor.values(), key=lambda x: x["forma"]):
        g, ident = separar_glosa(e["texto"])
        res[e["nivel"]].append({**e, "glosa_fuente": g, "identificacion_moderna": ident})
    return {"total_lemas": len(indexar(entradas)), "con_senal": len(mejor), "niveles": res}


# ══════════════════════════════════════════════════════════════════════
# Auditoría F1 — las 82 sin cita
# ══════════════════════════════════════════════════════════════════════

def auditar_82(entradas: list[dict]) -> list[dict]:
    idx = indexar(entradas)
    plano = " ".join(f"[{e['pag']}] {e['lema']}. {e['texto']}" for e in entradas)
    plano_n = norm(plano)
    filas = []
    for w in LAS_82:
        n = norm(w)
        veredicto, forma_alv, razon = ADJUDICACION_82.get(
            w, ("no-concluyente", None, _SIN_RASTRO_RAZON))
        e = idx.get(n) or (idx.get(norm(forma_alv)) if forma_alv else None)
        if e:
            aparece, pag, cita = "lema", e["pag"], e["texto"][:300]
        else:
            m = re.search(rf"\b{re.escape(n)}\b", plano_n)
            if m:
                frag = plano[max(0, m.start() - 100):m.start() + 160]
                pm = re.findall(r"\[(\d+)\]", plano[:m.start()])
                aparece, pag, cita = "mención", int(pm[-1]) if pm else None, " ".join(frag.split())
            else:
                aparece, pag, cita = "no", None, ""
        filas.append({"palabra": w, "aparece": aparece, "pagina": pag,
                      "forma_alvarado": forma_alv or (e["lema"] if e else None),
                      "cita": cita, "veredicto": veredicto, "razon": razon})
    return filas


# ══════════════════════════════════════════════════════════════════════
# Cadena de custodia — Zavala sigla `A` → su lugar exacto en Alvarado
# ══════════════════════════════════════════════════════════════════════
# La nota de fuente lo llamaba "la prueba de fuego más barata para la
# fiabilidad de toda la Capa 1": Lisandro Alvarado es el compilador `A` del
# glosario de Zavala Reyes 2015, así que toda entrada del lexicón con sigla `A`
# tiene que poder rastrearse a una página concreta de ESTE glosario. Si no
# aparece, la cita de Zavala es de tercera mano y no verificable.

# Variantes ortográficas confirmadas a mano (Zavala ↔ Alvarado).
_VARIANTES_ZAVALA_ALVARADO = {
    "laguari": "lauadri",      # Alvarado p.184: "D. t. Laguadrí"
    "quiguagua": "guagua",     # Alvarado p.261: "haba de Coro, grande y blanca"
    "paugis": "pauji",
}
# Presentes en Alvarado pero invisibles al índice por culpa del OCR de 1921.
# Se documentan aquí para que la métrica no se lea como "sin rastro".
_PERDIDAS_POR_OCR = {
    "guay": "p.145, leído por el OCR como 'GUÁL. Bombax sp. Ceiba. Voz usada en Coro'",
    "cocuy": "p.84, dentro del bloque COCUY/COCUIZA que el OCR fusionó "
             "('D. t. cucúi, que es la forma primitiva')",
}


def cadena_de_custodia(entradas: list[dict]) -> dict:
    """Rastrea las entradas del lexicón con sigla `A` (Alvarado) hasta su página."""
    from curiana_lexicon import VOCABULARIO_BASE
    idx = indexar(entradas)
    trazadas, perdidas = [], []
    for w, d in VOCABULARIO_BASE.items():
        notas = d.get("notas", "") or ""
        if "Zavala" not in notas:
            continue
        m = re.search(r"\(([^)]*)\)", notas)
        if not m or "A" not in m.group(1).split("+"):
            continue
        clave = _VARIANTES_ZAVALA_ALVARADO.get(norm(w), norm(w))
        e = idx.get(clave)
        (trazadas if e else perdidas).append(
            {"forma": w, "glosa_lexicon": d.get("sig", ""),
             "pagina": e["pag"] if e else None,
             "lema_alvarado": e["lema"] if e else None,
             "texto_alvarado": e["texto"][:200] if e else "",
             "ocr": _PERDIDAS_POR_OCR.get(norm(w), "")})
    return {"total": len(trazadas) + len(perdidas),
            "trazadas": trazadas, "perdidas": perdidas}


# ══════════════════════════════════════════════════════════════════════
# Salidas
# ══════════════════════════════════════════════════════════════════════

def informe(cls: dict, filas: list[dict]):
    print("=" * 78)
    print("  ALVARADO 1921 — Glosario de voces indígenas de Venezuela · minado F3")
    print("=" * 78)
    print(f"  lemas parseados del PDF            : {cls['total_lemas']}")
    print(f"  con señal de localización/curación : {cls['con_senal']}")
    print()
    etiq = {"A": "atestación colonial o atribución caquetía explícita",
            "B": "sobrevive a los 6 filtros + Coro/Falcón/Paraguaná",
            "C": "sobrevive con señal débil (solo Occ., o campo flojo)",
            "D": "DESCARTADA (cae en un filtro o sin señal)"}
    for n in "ABCD":
        items = cls["niveles"][n]
        print(f"── nivel {n}: {len(items):3}  {etiq[n]}")
        for e in items[: (30 if n != "D" else 12)]:
            print(f"     {e['forma']:14} p.{e['pag']:>3}  {e['glosa_fuente'][:52]}")
        if len(items) > (30 if n != "D" else 12):
            print(f"     … y {len(items) - (30 if n != 'D' else 12)} más")
        print()
    print("=" * 78)
    print("  F1 — las 82 entradas de familia caquetía SIN cita")
    print("=" * 78)
    cnt: dict[str, int] = {}
    for f in filas:
        cnt[f["veredicto"]] = cnt.get(f["veredicto"], 0) + 1
    for k, v in sorted(cnt.items()):
        print(f"  {k:18} {v}")
    print()
    for f in filas:
        if f["veredicto"] != "no-concluyente" or f["aparece"] != "no":
            pag = f"p.{f['pagina']}" if f["pagina"] else "—"
            print(f"  {f['palabra']:12} {f['aparece']:8} {pag:>6}  {f['veredicto']}")


def _py(s: str) -> str:
    return (s or "").replace("\\", "").replace('"', "'")


def generar_modulo(cls: dict, filas: list[dict], ruta: str, cadena: dict | None = None):
    L = ['"""',
         "CURIANA — Propuesta de minado de Alvarado 1921 (tarea F3)",
         "=" * 60, "",
         "GENERADO por `minar_alvarado_glosario.py` — no editar a mano.",
         "",
         "    Alvarado, Lisandro (1921). Glosario de voces indígenas de Venezuela.",
         "    Ediciones Victoria, Caracas. → fuentes_caquetios/",
         "",
         "⚠ NADA DE ESTE ARCHIVO ENTRA A `VOCABULARIO_BASE` SIN REVISIÓN HUMANA.",
         "Alvarado es un glosario NACIONAL: caribe, cumanagoto, chaima, taíno,",
         "guajiro, nahua y antillanismos castellanizados. La mayor parte no es",
         "caquetío. Los niveles siguen la escala del protocolo",
         "`investigacion/disenos/02_protocolo_habla_paraguanera.md` §5:",
         "",
         "    A — atestación colonial o atribución caquetía explícita",
         "    B — sobrevive a los 6 filtros + localización Coro/Falcón/Paraguaná",
         "    C — sobrevive pero con señal débil",
         "    D — descartada (documentada con su razón, para no re-minarla)",
         "",
         "POLÍTICA D7: `glosa_fuente` es lo que dice Alvarado, verbatim — es la",
         "que un agente hablaría. `identificacion_moderna` es el taxón, como nota",
         "auditable. Cuando difieren, el conflicto queda visible, no resuelto.",
         '"""', "", ""]

    for n, titulo in (("A", "NIVEL A — atestación colonial / atribución caquetía explícita"),
                      ("B", "NIVEL B — sobreviven a los 6 filtros, localizadas en Coro/Falcón/Paraguaná"),
                      ("C", "NIVEL C — plausibles, señal débil")):
        L.append("# " + "=" * 66)
        L.append(f"# {titulo}")
        L.append("# " + "=" * 66)
        L.append(f"CANDIDATOS_{n}: dict[str, dict] = {{")
        for e in cls["niveles"][n]:
            L.append(f'    "{e["forma"]}": {{')
            L.append(f'        "glosa_fuente": "{_py(e["glosa_fuente"])[:200]}",')
            L.append(f'        "identificacion_moderna": "{_py(e["identificacion_moderna"])}",')
            L.append(f'        "pagina": {e["pag"]},')
            L.append(f'        "lema_alvarado": "{_py(e["lema"])}",')
            L.append(f'        "nivel": "{e["nivel"]}",')
            L.append(f'        "razon": "{_py(e["razon"])[:300]}",')
            L.append("    },")
        L.append("}")
        L.append("")
        L.append("")

    L.append("# " + "=" * 66)
    L.append("# DESCARTES RAZONADOS — nivel D")
    L.append("# " + "=" * 66)
    L.append("# Documentar el descarte vale tanto como el hallazgo: evita que alguien")
    L.append("# re-mine la misma voz dentro de seis meses.")
    L.append("DESCARTES: dict[str, dict] = {")
    for e in cls["niveles"]["D"]:
        L.append(f'    "{e["forma"]}": {{"pagina": {e["pag"]}, '
                 f'"glosa_fuente": "{_py(e["glosa_fuente"])[:120]}", '
                 f'"razon": "{_py(e["razon"])[:260]}"}},')
    L.append("}")
    L.append("")
    L.append("")

    L.append("# " + "=" * 66)
    L.append("# F1 — AUDITORÍA DE LAS 82 ENTRADAS DE FAMILIA CAQUETÍA SIN CITA")
    L.append("# " + "=" * 66)
    L.append("# veredicto ∈ {confirma, reclasifica, no-concluyente}")
    L.append("AUDITORIA_82: dict[str, dict] = {")
    for f in filas:
        L.append(f'    "{f["palabra"]}": {{')
        L.append(f'        "aparece": "{f["aparece"]}",')
        L.append(f'        "pagina": {f["pagina"]},')
        L.append(f'        "forma_alvarado": {repr(f["forma_alvarado"])},')
        L.append(f'        "cita": "{_py(f["cita"])[:280]}",')
        L.append(f'        "veredicto": "{f["veredicto"]}",')
        L.append(f'        "razon": "{_py(f["razon"])[:400]}",')
        L.append("    },")
    L.append("}")
    L.append("")
    L.append("")

    if cadena:
        L.append("# " + "=" * 66)
        L.append("# CADENA DE CUSTODIA — sigla `A` de Zavala → página de Alvarado 1921")
        L.append("# " + "=" * 66)
        L.append("# Lisandro Alvarado es el compilador `A` del glosario de Zavala Reyes")
        L.append("# 2015. Toda entrada del lexicón con esa sigla debe poder rastrearse a")
        L.append("# una página concreta de ESTE glosario, o la cita es de tercera mano.")
        L.append(f"# Resultado: {len(cadena['trazadas'])}/{cadena['total']} rastreadas.")
        L.append("CADENA_CUSTODIA_ZAVALA_A: dict[str, dict] = {")
        for t in sorted(cadena["trazadas"], key=lambda x: x["forma"]):
            L.append(f'    "{t["forma"]}": {{"pagina": {t["pagina"]}, '
                     f'"lema_alvarado": "{_py(t["lema_alvarado"])}", '
                     f'"texto": "{_py(t["texto_alvarado"])[:150]}"}},')
        for t in cadena["perdidas"]:
            L.append(f'    "{t["forma"]}": {{"pagina": None, "lema_alvarado": None, '
                     f'"texto": "{_py(t["ocr"]) or "no localizada"}"}},')
        L.append("}")
        L.append("")
        L.append("")

    cnt: dict[str, int] = {}
    for f in filas:
        cnt[f["veredicto"]] = cnt.get(f["veredicto"], 0) + 1
    L.append("TOTALES = {")
    L.append(f'    "lemas_parseados": {cls["total_lemas"]},')
    L.append(f'    "evaluados": {cls["con_senal"]},')
    for n in "ABCD":
        L.append(f'    "nivel_{n}": {len(cls["niveles"][n])},')
    for k, v in sorted(cnt.items()):
        L.append(f'    "f1_{k.replace("-", "_")}": {v},')
    if cadena:
        L.append(f'    "cadena_zavala_A_total": {cadena["total"]},')
        L.append(f'    "cadena_zavala_A_trazadas": {len(cadena["trazadas"])},')
    L.append("}")
    L.append("")

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"  → módulo generado: {ruta}")
    print(f"     A={len(cls['niveles']['A'])} B={len(cls['niveles']['B'])} "
          f"C={len(cls['niveles']['C'])} D={len(cls['niveles']['D'])}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Minado de Alvarado 1921 (tarea F3)")
    ap.add_argument("--json", metavar="RUTA", help="volcar todo a JSON")
    ap.add_argument("--82", dest="solo82", action="store_true",
                    help="solo la auditoría de las 82 entradas sin cita")
    ap.add_argument("--cadena", action="store_true",
                    help="rastrear las entradas de sigla `A` de Zavala hasta su página")
    ap.add_argument("--generar-modulo", nargs="?", const="lexicon_alvarado.py",
                    metavar="RUTA", help="escribir lexicon_alvarado.py")
    args = ap.parse_args()

    entradas = extraer()
    cls = clasificar(entradas)
    filas = auditar_82(entradas)

    if args.cadena:
        c = cadena_de_custodia(entradas)
        print(f"  entradas del lexicón con sigla A (Alvarado) vía Zavala: {c['total']}")
        print(f"  rastreadas a su página en Alvarado 1921: {len(c['trazadas'])}")
        for t in sorted(c["trazadas"], key=lambda x: x["forma"]):
            print(f"    {t['forma']:14} p.{t['pagina']:>3}  {t['texto_alvarado'][:64]}")
        print(f"  NO localizadas por el índice ({len(c['perdidas'])}):")
        for t in c["perdidas"]:
            print(f"    {t['forma']:14} lex='{t['glosa_lexicon'][:44]}'"
                  f"{'  → SÍ está, ' + t['ocr'] if t['ocr'] else ''}")
    elif args.generar_modulo:
        ruta = args.generar_modulo
        if not os.path.isabs(ruta):
            ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta)
        generar_modulo(cls, filas, ruta, cadena_de_custodia(entradas))
    elif args.solo82:
        for f in filas:
            pag = f"p.{f['pagina']}" if f["pagina"] else "—"
            print(f"{f['palabra']:12} {f['aparece']:8} {pag:>6}  {f['veredicto']:15} {f['razon'][:90]}")
    else:
        informe(cls, filas)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"clasificacion": cls, "auditoria_82": filas}, f,
                      ensure_ascii=False, indent=2)
        print(f"\n  → JSON: {args.json}")
