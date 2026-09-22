# -*- coding: utf-8 -*-
"""
Cruce TAÍNO <-> CAQUETÍO ATESTIGUADO — campaña del taíno.
T4 (2026-09-21) y **T11, la prueba lingüística del contacto** (2026-09-22).

LA PREGUNTA
-----------
¿Qué comparten de verdad el taíno y el caquetío ATESTIGUADO —en léxico, en
morfología y en onomástica—, y qué de eso es herencia arahuaca común, qué es
préstamo por contacto en la esfera, y qué es casualidad?

LO QUE AÑADE T11 (2026-09-22)
-----------------------------
El encargo de Miguel: «tiene que haber una forma de probar si hubo algún tipo
de contacto… diao y daitiao son las versiones caquetías de la versión taína».
Dicho como test:

    Un cognado HEREDADO y un préstamo por CONTACTO se distinguen.
    El cognado sigue las correspondencias REGULARES de sonido entre las dos
    lenguas —las que se repiten en otras parejas—. El préstamo las VIOLA, o
    llega sin ninguna diferencia porque cruzó hace poco, o cae en un campo
    donde las palabras viajan (alianza, rango, comercio, prestigio).
    Un préstamo prueba CONTACTO; un cognado prueba PARENTESCO.

Cuatro cosas nuevas, en este orden y con el orden como parte del método:

1. **Las transcripciones entran como fuente.** El cruce del 21 leía sólo las
   43 voces taínas del lexicón, que no citan a nadie (regla 8). Desde hoy lee
   además `6-fusion/taino_{oviedo_valdes_1851,las_casas_1875,pane_c1498,
   brinton_1871}.yaml`, que sí traen obra y página. Eso cambia el
   DENOMINADOR: el cero del 21 medía la lista, no la lengua.
2. **Las predicciones se escriben ANTES de mirar las parejas** — por
   transitividad, componiendo las correspondencias caquetío↔lokono que el
   proyecto ya tiene (Oliver cap. 2, C1-C13) con las taíno↔lokono que da
   Brinton 1871. `CORRESPONDENCIAS_PREDICHAS` está más abajo, en el código,
   antes que cualquier función que mire un par.
3. **El test se aplica**, y su resultado es una LETRA: A cognado heredado,
   B préstamo o forma que cruzó sin cambio, C indecidible con lo que hay.
4. **El control es obligatorio.** El mismo test sobre parejas que ya sabemos
   heredadas (caquetío↔lokono con cita) y sobre parejas que ya sabemos
   prestadas (taíno↔castellano). Si el test no separa lo que ya sabemos, no
   sirve para lo que no sabemos, y el YAML lo dice con número.

POR QUÉ SÓLO CONTRA EL CAQUETÍO ATESTIGUADO
-------------------------------------------
Las capas `caquetío-reconstruido` y `caquetío-hipotético` se fabricaron
mirando al wayuu y al lokono (`arahuaco_comparative.REGLAS_*`, las 441
candidatas). Cruzarlas con el taíno mediría **el andamio**, no el caquetío:
el parecido que saliera sería el que nosotros pusimos. Se miden igual y se
emiten aparte, marcadas `circular`, para que el número exista y no para que
decida nada. El resumen de filiación usa **sólo** la capa atestiguada.

Y por la misma razón queda fuera `taíno-reconstruido` (9 entradas): son
formas que `reconstruir_taino()` generó desde el lokono y sus propias `notas`
lo dicen —«no cuenta como dato taíno en cruces»—. Cruzarlas contra el
caquetío mediría dos veces el mismo lokono.

EL MÉTODO, con las tres lecciones de la skill `minar-fuente` en código
----------------------------------------------------------------------
1. FILTRO DE SIGNIFICADO (§2). Se empareja por la glosa castellana, nunca por
   parecido de forma suelto. Medido el 2026-09-10 en el achagua: de 11
   «aciertos» de forma, sólo 2 aguantaron al mirar la glosa.
2. MIRAR LA CAPA (§8). La entrada cuya forma se derivó de otra lengua es
   circular con esa lengua. Y la entrada taína cuyas `notas` se escribieron
   mirando al caquetío («cognado caquetío probable *kali») lleva aviso: la
   forma es real, la nota no es independiente.
3. DESCONFIAR DE LA PROPIA REGLA (§2, §8). Tres controles:
   - MODELO NULO por permutación: para cada concepto se sortean tantas
     entradas al azar de la misma lengua como emparejaron por glosa. Es la
     versión sin sesgo de «barajar las glosas», y además corrige que el
     achagua (3.568 entradas) ofrezca muchos más candidatos que el taíno (43);
   - CONTROL NO ARAHUACO: la misma medida contra el jirajara/ayomán de Jahn
     1927 (`6-fusion/control_jirajarano_jahn_1927.yaml`), que no es pariente;
   - PRUEBA DE PREDICCIÓN dejando fuera: una correspondencia vista en un par
     predice sobre los demás conceptos. Una que sale una vez no es nada.

SALIDA (PROPUESTA, regla 5)
---------------------------
    6-fusion/cruce_taino_caquetio_2026-09-22.yaml

`6-fusion/cruce_taino_caquetio_2026-09-21.yaml` queda como está: es la medición
del día anterior y el script la LEE para emitir el antes/después medido
(`meta.antes_y_despues`). No se reescribe.

No toca `curiana_lexicon.py`, ni `lexicon_*.py`, ni `2-lengua/*`, ni
`3-mundo/corpus/`. Ningún cognado entra a `cognados.yaml` por este script.

    python 6-fusion/scripts/cruce_taino_caquetio.py
    python 6-fusion/scripts/cruce_taino_caquetio.py --check   # ¿está al día?
"""
import argparse
import collections
import difflib
import io
import os
import random
import re
import sys
import time
import unicodedata

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL  # noqa: E402
from curiana_fonotactica import fonemizar, forma_comparable  # noqa: E402

SALIDA = os.path.join(R, "6-fusion", "cruce_taino_caquetio_2026-09-22.yaml")
ANTERIOR = os.path.join(R, "6-fusion", "cruce_taino_caquetio_2026-09-21.yaml")
YAML_CONTROL = os.path.join(R, "6-fusion", "control_jirajarano_jahn_1927.yaml")
YAML_TOPONIMOS = os.path.join(R, "2-lengua", "toponimos.yaml")
YAML_COGNADOS = os.path.join(R, "2-lengua", "cognados.yaml")
YAML_ANTROPONIMOS = os.path.join(R, "6-fusion", "antroponimos_caquetios.yaml")
JSON_TAINO_HIP = os.path.join(R, "curiana_sim", "taino_hipotetico.json")
TXT_BRINTON = os.path.join(R, "fuentes_caquetios", "Brinton_1871_texto.txt")
TXT_PANE = os.path.join(R, "fuentes_caquetios",
                        "Pane_c1498_Relacion_Antiguedades_Indios_wikisource.txt")
FECHA = "2026-09-22"

# ── las transcripciones de T1/T2 (PR #189-#192), que es lo que entra hoy ───
# Cada sección se declara con la obra (clave foránea a 4-fuentes/bibliografia.yaml,
# regla 8) y con si es taíno o NO lo es: `no_taino` de Oviedo y su
# `costa_de_venezuela` son Tierra-Firme, y meterlas en el saco taíno sería
# exactamente la trampa que la regla 4 denuncia.
YAML_TAINO = [
    {"archivo": "taino_oviedo_valdes_1851.yaml", "obra": "oviedo-y-valdes-1851",
     "secciones": {"la_espanola": "taíno", "otras_islas": "taíno",
                   "no_taino": "fuera-no-es-taino",
                   "costa_de_venezuela": "fuera-tierra-firme"}},
    {"archivo": "taino_las_casas_1875.yaml", "obra": "las-casas-1875",
     "secciones": {"voces": "taíno"}},
    {"archivo": "taino_pane_c1498.yaml", "obra": "pane-c1498",
     "secciones": {"voces": "taíno"}},
    {"archivo": "taino_brinton_1871.yaml", "obra": "brinton-1871",
     "secciones": {"vocabulario_antillano.entradas": "taíno"}},
]

# ── parámetros declarados ANTES de mirar resultados ──────────────────────
UMBRAL_PARECIDO = 0.62      # el de cruzar_jahn_guajiro.py y del cruce achagua
UMBRAL_COGNADO = 0.75
UMBRAL_FORMA = 0.75         # el paso SIN filtro de glosa: listón más alto a propósito
MIN_FONEMAS_FORMA = 4       # y forma más larga, porque ahí no hay glosa que sujete
MIN_FONEMAS = 3             # dos letras no son evidencia (el 80 % de las 441)
REPLICAS = 300
SEMILLA = 1492
GU_ES_W = False             # defecto de curiana_fonotactica; True = sensibilidad
GU_TEST = True              # T11: el test de correspondencias corre con ⟨gu⟩ = /w/
                            # (Oliver p. 147), que es lo que deja ver ⟨bagua⟩ = /bawa/
ATESTIGUADO = "caquetío-atestiguado"

LENGUAS = ("taíno", "lokono", "wayunaiki", "achagua")   # las que deciden
INFORMATIVAS = ("kalinago", "paraujano")                # columna extra
CONTROL = "jirajarano"                                  # NO arahuaco
TODAS = LENGUAS + INFORMATIVAS + (CONTROL,)
TOPES = {"taíno": 3, "lokono": 3, "wayunaiki": 2, "achagua": 3,
         "kalinago": 2, "paraujano": 2, "jirajarano": 2}

AFIJOS = {  # (prefijos, sufijos) sobre la forma YA fonemizada
    "taíno": (("wa", "gua", "da", "ma", "ka", "ni"), ()),
    "lokono": (("da", "wa", "li", "to", "bu", "na"), ("n",)),
    "wayunaiki": (("a",), ()),
    "achagua": (("nu", "ri", "ru", "gua", "wa", "ji", "na"), ("si",)),
    "paraujano": (("ta", "a"), ()),
    "kalinago": (("a", "i"), ()),
    "jirajarano": (("a", "i"), ()),
}

SINONIMOS_CRUDOS = {  # declarados: la glosa colonial y la moderna para lo mismo
    "pescado": "pez", "pájaro": "ave", "varón": "hombre", "culebra": "serpiente",
    "demonio": "diablo", "anciano": "viejo", "escuchar": "oír", "jefe": "cacique",
    "maíz": "maiz", "cazabe": "casabe", "jutía": "hutia",
}

# El DOMINIO decide la clase de una pareja, y es la tabla de la skill
# `minar-fuente` §3, que viene de la corrección de Miguel del 2026-09-10:
# «hay palabras que pueden compartirse entre etnias». Lo que decide no es SI
# se comparte, sino QUÉ.
DOMINIO_POR_CATEGORIA = {
    # viajan entre lenguas sin parentesco: préstamo areal, dato de comercio
    "flora": "viajero", "fauna": "viajero", "alimentacion": "viajero",
    "alimentos": "viajero", "comercio": "viajero", "utiles": "viajero",
    "ritual": "viajero", "arquitectura": "viajero", "navegacion": "viajero",
    "jerarquia": "viajero", "materiales": "viajero", "cosmos": "viajero",
    "agricultura": "viajero", "tecnologia": "viajero", "vestimenta": "viajero",
    # casi nunca viajan: si coinciden, es dato de FILIACIÓN
    "cuerpo": "filiacion", "parentesco": "filiacion", "gramatica": "filiacion",
    "pronombres": "filiacion", "numeros": "filiacion",
    # ni lo uno ni lo otro sin mirar el caso
    "geografia": "mixto", "clima": "mixto", "tiempo": "mixto",
    "naturaleza": "mixto", "etnonimia": "mixto",
}
CATS_DE_FILIACION = frozenset({"pron", "num", "interr"})

VOCALES = set("aeiou")

# Sondas de formante: (nombre, patrón sobre la forma en minúsculas).
# Los prefijos se prueban con la grafía colonial Y la fonémica, porque el
# taíno del repo está en grafía castellana y el caquetío en lema fonémico.
SONDAS_PREFIJO = [
    ("ma- privativo", r"^ma"),
    ("ka-/ca- atributivo", r"^(ka|ca)"),
    ("da- 1ª sg.", r"^da"),
    ("gua-/wa-", r"^(gua|wa|hua|gu)"),
    ("ni-", r"^ni"),
]
SONDAS_SUFIJO = [
    ("-bana", r"bana$"),
    ("-coa/-koa/-cua", r"(coa|koa|cua|kua|qua)$"),
    ("-bacoa/-bakoa", r"(bacoa|bakoa|vacoa)$"),
    ("-oa", r"oa$"),
    ("-bo/-abo", r"bo$"),
    ("-ey/-ay", r"([eé]y|[aá]y|g[uü]ey)$"),
    ("-ana", r"ana$"),
    ("-gua", r"gua$"),
    ("-ni/-na", r"(ni|na)$"),
    ("-ío/-yo (gentilicio)", r"([ií]o|yo)$"),
    ("-(h)o nominalizador", r"(ho|o)$"),
    ("-ex final (antropónimo)", r"e[xj]$"),
    ("-el final (antropónimo)", r"[eaoi]l$"),
    # Oliver cap. 2 p. 148 lista -kiva entre los sufijos toponímicos caquetíos
    # y el canon no lo tiene. Se sonda para que el cero (o el no-cero) sea medido.
    ("-kiva/-quiva", r"(kiva|quiva|kiba|quiba)$"),
]

# Castellano y onomástica cristiana que NO debe contar como forma indígena en
# la sonda sobre Pané. Lista DECLARADA: la sonda emite su inventario entero
# para que se pueda auditar.
BLOQUEO_PANE = {
    "dios", "cristo", "jesús", "jesus", "santa", "santo", "san", "juan", "pedro",
    "antonio", "ramón", "ramon", "cristóbal", "cristobal", "colón", "colon",
    "almirante", "virrey", "gobernador", "rey", "reina", "fernando", "isabel",
    "indias", "española", "españa", "castilla", "italia", "magdalena", "isabela",
    "concepción", "concepcion", "ave", "maría", "maria", "credo", "padrenuestro",
    "pater", "noster", "fray", "señor", "señora", "verdad", "ahora", "así", "asi",
    "creo", "dicen", "dice", "entonces", "estando", "todos", "todo", "acabado",
    "pero", "por", "para", "como", "cuando", "esto", "este", "esta", "estos",
    "diremos", "hallándome", "hallandome", "verdaderamente", "capítulo", "capitulo",
    "relación", "relacion", "libro", "primero", "segundo", "tercero", "cuarto",
    "quinto", "sexto", "hombres", "mujeres", "tierra", "cielo", "islas", "isla",
    "los", "las", "una", "uno", "que", "con", "del", "les", "muy", "más", "mas",
    "ayala", "arteaga", "martín", "martin", "ayuno", "fortaleza", "provincia",
    # añadidos DESPUÉS de leer el inventario de la primera pasada (regla 6: el
    # cero y el ruido se auditan mirando la lista, no confiando en el filtro)
    "algunas", "canta", "cómo", "como", "dime", "francisco", "guárdala", "guardala",
    "jerónimo", "jeronimo", "mateo", "mirobalanos", "orden", "pané", "pane", "pues",
    "señoría", "senoria", "subpáginas", "subpaginas", "trae", "vete", "vuestra",
    "wikisource", "borgoña", "borgona", "haití", "haiti",
}


# ═════════════════════════════════════════════════════════════════════════
# T11 · LAS PREDICCIONES, ESCRITAS ANTES DE MIRAR NINGUNA PAREJA
# ═════════════════════════════════════════════════════════════════════════
# No hay ni una correspondencia caquetío↔taíno publicada: nadie la ha
# establecido, y este proyecto no puede establecerla con 4 parejas. Lo que SÍ
# se puede hacer es COMPONER las dos patas que sí existen y ver qué predicen:
#
#   pata A  caquetío ↔ lokono   — Oliver 1989 cap. 2, C1-C13, con página
#   pata B  taíno    ↔ lokono   — Brinton 1871 pp. 11-14, con página
#                                 (recogidas en 6-fusion/taino_brinton_1871.yaml
#                                  §correspondencias_para_T4, que es de T2)
#
# Componerlas da una PREDICCIÓN, no un hecho: si el caquetío y el taíno
# descienden los dos de un fondo como el del lokono, una voz heredada tiene
# que exhibir en cada consonante lo que las dos patas mandan. Una voz que no
# lo exhiba no es heredada por esa vía.
#
# ⚠️ Tres límites, declarados por Oliver y respetados aquí:
#   C8  /r/ ~ /l/ es INDECIDIBLE en todo el corpus: una diferencia r/l no
#       cuenta ni a favor ni en contra.
#   C9  Oliver EXCLUYE las vocales por falta de transcripción fiable: el test
#       puntúa esqueletos CONSONÁNTICOS.
#   ⟨gu⟩ se lee /w/ — Oliver p. 147: «/wa- [gua-]/ is a third person plural
#       marker». Por eso el test corre sobre la fonemización con gu_es_w=True,
#       que es la que hace ⟨bagua⟩ = /bawa/ y deja ver la correspondencia.
CORRESPONDENCIAS_PREDICHAS = [
    {
        "id": "P1",
        "regla": "caquetío /r/  ~  taíno ∅ o /w/  (donde el lokono tiene /r/)",
        "pata_cq_lk": ("el caquetío CONSERVA la /r/ intervocálica del lokono: `dare` : LK `d-ari` "
                       "'diente'; `barisi` : LK `bálisi` 'ceniza'; `para` : LK `bara` 'mar' "
                       "(oliver-1989-cap2 pp. 147, 150; cognado-001, cognado-010)"),
        "pata_tn_lk": ("el taíno la PIERDE o la vuelve /w/: `maisi` : LK `marisi` 'maíz'; "
                       "`cai/cayo` : LK `kairi` 'isla'; `bagua` : LK `bara` 'mar' "
                       "(brinton-1871 pp. 11-13, vía taino_brinton_1871.yaml §clase_B)"),
        "predice": ("una voz heredada tiene /r/ en caquetío y NADA o /w/ en taíno. El par "
                    "canónico es caq `para` ~ taí `bagua` /bawa/ ~ LK `bara`, y Oliver lo escribe "
                    "él mismo (p. 150: taíno `bara-wa` junto al caquetío `para-`)"),
        "la_falsaria": ("una pareja caquetío~taíno con /r/ en los DOS lados y sin otra diferencia. "
                        "Sería la firma de que la palabra cruzó tarde, no de que se heredó"),
        "apoyos": 3, "diagnostica": True,
        "es_diagnostica_porque": ("lo esperado NO es la identidad: el taíno normalmente pierde la "
                                  "/r/. Es la única consonante diagnóstica que el material da, y "
                                  "la única correspondencia que llega al listón de tres apoyos"),
    },
    {
        "id": "P2",
        "regla": "caquetío /b/  ~  taíno /b/   (los dos del lado lokono, frente a wayuu /p/)",
        "pata_cq_lk": ("C3, «two very regular and systematic sound changes»: LK /b/ : WY /p/, y el "
                       "caquetío cae del lado lokono — `barisi` : `bálisi` : WY `palíi`; y el sufijo "
                       "es `-bana` y no `-pana` (oliver-1989-cap2 pp. 147-148)"),
        "pata_tn_lk": "taíno `bagua`/`bara-wa` : LK `bara`; `siba` : LK `siba` (brinton-1871 pp. 11, 13)",
        "predice": "una voz heredada tiene /b/ en los dos lados; un /p/ caquetío frente a /b/ taíno es la excepción declarada",
        "la_falsaria": ("la excepción YA existe y Oliver no la explica: caq `para` 'mar' frente a LK "
                        "`bara` y TN `bara-wa`. Por eso /p/ ~ /b/ se admite como regular y se dice"),
        "apoyos": 2, "diagnostica": False,
        "es_diagnostica_porque": "no lo es: lo esperado ES la identidad, y una identidad esperada no informa",
    },
    {
        "id": "P2b",
        "regla": "caquetío /p/  ~  taíno /b/   (la excepción declarada de `para`)",
        "pata_cq_lk": "caq `para` 'mar' : LK `bara` — oliver-1989-cap2 p. 150, y él mismo la deja sin explicar",
        "pata_tn_lk": "TN `bagua` / `bara-wa` : LK `bara` — brinton-1871 p. 11; oliver-1989-cap2 p. 150",
        "predice": "un /p/ caquetío puede corresponder a un /b/ taíno. Es UNA pareja, así que se admite y se marca",
        "la_falsaria": "que no vuelva a salir en ninguna otra pareja: entonces es un caso suelto y no una regla",
        "apoyos": 1, "diagnostica": False,
        "es_diagnostica_porque": ("no lo es: UN apoyo. Se admite para no llamar violación a lo que "
                                  "Oliver escribe, y no se usa para declarar nada por sí sola"),
    },
    {
        "id": "P3",
        "regla": "caquetío /d-/  ~  taíno /d-/   (1ª persona singular, y /d/ en general)",
        "pata_cq_lk": ("C1: PA */nV-/ → /dA-/ en lokono, taíno y «perhaps Caquetío» → /tA-/ en "
                       "guajiro-paraujano. Evidencia caquetía: `diao`, `datihao`, `dare`, `dato` "
                       "(oliver-1989-cap2 pp. 136, 146-147). Falsificó la regla `^d → t` del "
                       "proyecto (metodo-comparativo, issue #43)"),
        "pata_tn_lk": "taíno `daca` 'yo' (pane-c1498 cap. XXV) y `da-` en `da(i)tia-o` (oliver-1989-cap2 p. 147)",
        "predice": ("una voz heredada tiene /d/ en los dos lados — y por eso mismo **este rasgo NO "
                    "distingue herencia de préstamo entre caquetío y taíno**: separa a los dos "
                    "JUNTOS del wayuu y el paraujano, que tienen /t-/. Es dato de FILIACIÓN y ya "
                    "está contado en D11 por la vía lokono"),
        "la_falsaria": "una forma caquetía con /t-/ donde el taíno tiene /d-/: sería vía guajiro-paraujana",
        "apoyos": 2, "diagnostica": False,
        "es_diagnostica_porque": "no lo es, y ES EL PUNTO: identidad esperada, identidad observada, cero información",
    },
    {
        "id": "P4",
        "regla": "caquetío /t/  ~  taíno /t/   (donde el lokono tiene /th/)",
        "pata_cq_lk": "C4b, CQ /t/ : LK /th/ — `kaketío` : LK `kakïtho` (oliver-1989-cap2 p. 148)",
        "pata_tn_lk": "Taylor 1977:38 vía Oliver: LK /th/ : CAIC /t/, y el taíno va con el insular",
        "predice": "identidad en /t/ entre caquetío y taíno. NO diagnóstica: la identidad no prueba nada",
        "la_falsaria": ("nada la puede falsar con el instrumento de hoy: `fonemizar()` colapsa ⟨th⟩ "
                        "en /t/, así que el contraste lokono se pierde antes de llegar al test. "
                        "Declarado como límite del instrumento, no como resultado"),
        "apoyos": 1, "diagnostica": False,
        "es_diagnostica_porque": "no lo es: el instrumento colapsa el contraste antes de llegar al test",
    },
    {
        "id": "P5",
        "regla": "caquetío /k/, /s/, /m/, /n/, /y/, /j/  ~  las mismas en taíno",
        "pata_cq_lk": "no hay ninguna correspondencia declarada que las mueva (Oliver no las lista)",
        "pata_tn_lk": "Brinton las da idénticas (`siba`~`siba`, `nacan`~`annakan`, `ma-`~`ma-`)",
        "predice": "identidad. NO diagnósticas: una pareja que sólo comparta estas consonantes no decide nada",
        "la_falsaria": "—",
        "apoyos": None, "diagnostica": False,
    },
    {
        "id": "P6",
        "regla": "LA FIRMA DEL PRÉSTAMO: cero diferencia donde una regular tenía que haber",
        "pata_cq_lk": ("Oliver mide lokono–guajiro en 2,6 milenios de separación y lokono–achagua en "
                       "3,8 (p. 97 y ss.). A esa distancia una voz heredada ha tenido tiempo de "
                       "mostrar al menos una de las correspondencias de arriba"),
        "pata_tn_lk": ("y el propio Oliver avisa (p. 151): «one must be careful about some terms "
                       "(e.g. barbacoa) offered by the Spanish as 'native' Caquetío»"),
        "predice": ("si las dos formas tienen el MISMO esqueleto consonántico y ese esqueleto "
                    "contiene al menos una consonante diagnóstica (P1, P2, P2b), la pareja es "
                    "préstamo o transmisión reciente, no herencia"),
        "la_falsaria": ("una pareja idéntica SIN consonante diagnóstica no dice nada: la palabra no "
                        "tiene dónde diferir. Ése es el caso que el test tiene que devolver como C, "
                        "y es exactamente el de `-tiao`"),
        "apoyos": None, "diagnostica": False,
    },
    {
        "id": "P7",
        "regla": "caquetío /k/  ~  taíno /s/   — CANDIDATA, por debajo del listón",
        "⚠️_esta_se_escribio_despues": (
            "y hay que decirlo. Las seis de arriba se escribieron antes de mirar ninguna pareja; "
            "ésta la EXIGIÓ EL CONTROL: al correr el test sobre los cognados caquetío↔lokono que "
            "Oliver da con cita, `koke` ~ `kuse` 'bachaco' salía «viola las correspondencias», o "
            "sea préstamo, y es un cognado que el propio Oliver sostiene (p. 145). El hueco era de "
            "la tabla, no del par. Se añade y se declara cuándo se añadió."),
        "pata_cq_lk": "caq `koke` : LK `kuse` 'bachaco' — oliver-1989-cap2 p. 145, cognado-007",
        "pata_tn_lk": "taíno `siba` : LK `siba` 'piedra' — brinton-1871 p. 13",
        "predice": "que el caquetío `kiba` (forma_fuente `quiva`) 'piedra' y el taíno `siba` serían cognados",
        "la_falsaria": ("que no aparezca un tercer apoyo. Son DOS, y uno de ellos es justo la pareja "
                        "que querríamos juzgar: usarla para decidirla sería circular. Por eso el "
                        "test la trata como CANDIDATA y devuelve C, no A"),
        "apoyos": 2, "diagnostica": False,
        "es_diagnostica_porque": ("no lo es. Y además no llega al listón de tres del propio "
                                  "proyecto («una correspondencia que sale una o dos veces no es "
                                  "nada»), así que baja el veredicto a C en vez de darlo por bueno"),
    },
]

# ── Las tablas EJECUTABLES ────────────────────────────────────────────────
# Cada consonante lleva tres cosas y las tres importan:
#   `admite`      qué consonantes taínas (o lokonas) puede tener enfrente
#   `candidatas`  las que la cadena SUGIERE pero que no llegan al listón del
#                 propio proyecto —tres apoyos— («una correspondencia que sale
#                 una o dos veces no es nada»). Usarlas NO da un cognado: baja
#                 el veredicto a C y lo dice.
#   `diagnostica` True sólo si lo ESPERADO NO es la identidad. Es lo que
#                 permite leer un «cero diferencia» como préstamo: si lo
#                 esperado era cambiar y no cambió, la palabra cruzó tarde.
#
# ⚠️ LA TABLA ES DE UN PAR DE LENGUAS, NO UNIVERSAL. La /r/ es diagnóstica
# entre caquetío y taíno (el taíno la pierde) y NO lo es entre caquetío y
# lokono (los dos la conservan). Aplicar la tabla equivocada fue exactamente lo
# que el control destapó al escribirlo —dos parejas heredadas salían
# «préstamo»— y por eso el control es obligatorio y va en el YAML.
PREDICHO_CQ_TN = {
    # /r/: 3 apoyos en la pata taína (maisi:marisi, cai:kairi, bagua:bara) y el
    # caquetío conservándola en dare, barisi, para. Llega al listón.
    "r": {"admite": {"", "w", "r"}, "candidatas": set(), "diagnostica": True, "apoyos": 3},
    "b": {"admite": {"b"}, "candidatas": set(), "diagnostica": False, "apoyos": 2},
    "p": {"admite": {"b", "p"}, "candidatas": set(), "diagnostica": False, "apoyos": 1},
    "d": {"admite": {"d"}, "candidatas": set(), "diagnostica": False, "apoyos": 2},
    "t": {"admite": {"t"}, "candidatas": set(), "diagnostica": False, "apoyos": 1},
    # /k/ ~ /s/: sale de componer `koke`:`kuse` (Oliver p. 145) con `siba`:`siba`
    # (Brinton p. 13). DOS apoyos, y uno de ellos es la pareja que querríamos
    # juzgar: por debajo del listón, y circular si se usara para decidirla.
    "k": {"admite": {"k"}, "candidatas": {"s"}, "diagnostica": False, "apoyos": 2},
}
# Pata A sola, caquetío ↔ lokono, para el brazo de control del test.
# Aquí NINGUNA consonante es diagnóstica: entre dos hermanas conservadoras lo
# esperado es la identidad, así que un «cero diferencia» no informa.
PREDICHO_CQ_LK = {
    "b": {"admite": {"b"}, "candidatas": set(), "diagnostica": False, "apoyos": 2},
    "p": {"admite": {"b", "p"}, "candidatas": set(), "diagnostica": False, "apoyos": 1},
    "d": {"admite": {"d"}, "candidatas": set(), "diagnostica": False, "apoyos": 4},
    "t": {"admite": {"t"}, "candidatas": set(), "diagnostica": False, "apoyos": 1},
    "r": {"admite": {"r", "l"}, "candidatas": set(), "diagnostica": False, "apoyos": 3},
    "l": {"admite": {"l", "r"}, "candidatas": set(), "diagnostica": False, "apoyos": 3},
    "k": {"admite": {"k"}, "candidatas": {"s"}, "diagnostica": False, "apoyos": 2},
    "s": {"admite": {"s"}, "candidatas": set(), "diagnostica": False, "apoyos": 1},
}
TABLAS = {
    "caquetío↔taíno": {"mapa": PREDICHO_CQ_TN,
                       "de_donde": "composición de las dos patas — ver `las_predicciones`"},
    "caquetío↔lokono": {"mapa": PREDICHO_CQ_LK,
                        "de_donde": "pata A sola: oliver-1989-cap2 C1-C13, con página"},
}
LISTON_DE_APOYOS = 3   # el del propio proyecto, `juicio_regla()` más abajo

# C8: /r/ ~ /l/ no cuenta ni a favor ni en contra. `fonemizar` ya lleva ⟨ll⟩ a y.
PARES_NEUTROS = frozenset({("r", "l"), ("l", "r")})
CONSONANTES = set("bcdfghjklmnpqrstvwxyz")

# Prefijos de PERSONA, que son morfología y no sonido. Si dos formas empiezan
# por prefijos de persona DISTINTOS, la diferencia inicial no es una
# correspondencia violada: es el contraste 1ª sg. / 3ª pl. que Oliver nombra
# (p. 147, «/wa- [gua-]/ is a third person plural marker, and /da-/ … first
# person singular»). El test lo dice en vez de contarlo como violación.
PREFIJOS_DE_PERSONA = {"d": "1ª sg. /dA-/", "w": "3ª pl. /wa- [gua-]/",
                       "t": "1ª sg. guajiro-paraujana /tA-/", "n": "1ª sg. proto-arahuaca /nV-/"}

# Préstamos que YA SABEMOS que lo son: el control positivo del test.
# El taíno se los dio al castellano, y el castellano los repartió por América.
# Si el test no los llama préstamo, el test no sirve.
PRESTAMOS_CONOCIDOS = [
    ("maisi", "maíz", "brinton-1871 p. 13: «Maisi, maize. From this Eng. maize, Sp. maiz»"),
    ("huracan", "huracán", "brinton-1871 p. 13: «Huracan, a hurricane. From this Sp. huraean, Fr. ouragan»"),
    ("canoa", "canoa", "brinton-1871 p. 12 s.v. Canoa; oviedo-y-valdes-1851 p. 170 «los indios llaman canoa»"),
    ("hamaca", "hamaca", "brinton-1871 p. 12; oviedo-y-valdes-1851 p. 131"),
    ("cacike", "cacique", "oviedo-y-valdes-1851 p. 25 «que los indios llaman caçique»; oliver-1989-cap2 p. 151 lo avisa"),
    ("barbacoa", "barbacoa", "brinton-1871 p. 11; oliver-1989-cap2 p. 151 lo avisa por su nombre"),
    ("cazabi", "cazabe", "oviedo-y-valdes-1851 p. 264 «el pan de los indios que se llama caçabi»"),
    ("batata", "batata", "oviedo-y-valdes-1851 p. 273"),
    ("yuca", "yuca", "oviedo-y-valdes-1851 p. 264"),
    ("sabana", "sabana", "brinton-1871 p. 13; oviedo-y-valdes-1851 p. 146 «á la savana ó á lo raso»"),
    ("tabako", "tabaco", "oviedo-y-valdes-1851 p. 130; brinton-1871 p. 13"),
    ("caiman", "caimán", "brinton-1871 p. 12"),
    ("guayaba", "guayaba", "oviedo-y-valdes-1851 p. 305"),
    ("papaya", "papaya", "oviedo-y-valdes-1851 p. 323"),
    ("manati", "manatí", "oviedo-y-valdes-1851 p. 433"),
    ("hutia", "jutía", "oviedo-y-valdes-1851 p. 50"),
    ("iwana", "iguana", "oviedo-y-valdes-1851 p. 50 «sierpes que se llaman yvana»; las-casas-1875 cap. ~314"),
    ("macana", "macana", "brinton-1871 p. 13; las-casas-1875 «Qué cosa es macana»"),
]

# Glosas de Brinton: son INGLESAS y el filtro de significado del script es
# castellano. Tabla DECLARADA y emitida entera en el YAML, para que se audite
# a ojo. Sólo se traduce donde el concepto castellano es inequívoco; lo demás
# se queda sin traducir A PROPÓSITO y se cuenta (una glosa inventada fabrica
# una pareja falsa, que es peor que un hueco).
GLOSA_EN_ES = {
    "red pepper": "ají",
    "dog": "perro",
    "the sea": "mar",
    "a priest": "sacerdote",
    "an island": "isla",
    "an alligator": "caimán",
    "gold": "oro",
    "a conch, a univalve shell": "caracol",
    "a boat": "canoa",
    "a chief": "cacique",
    "a cultivated field": "conuco",
    "low seats (unas baxas sillas)": "asiento",
    "a basket": "cesta",
    "a bed, hammock": "hamaca",
    "a rope, ropes": "soga",
    "height": "altura",
    "a hurricane": "huracán",
    "a lagoon, pond": "laguna",
    "a serpent": "serpiente",
    "a war club": "macana",
    "a plain": "llanura",
    "a plain covered with grass without trees": "llanura",
    "a native drum": "tambor",
    "maize": "maíz",
    "liberal, noble": "noble",
    "servants": "criado",
    "middle, center": "centro",
    "dead": "muerto",
    "a stone": "piedra",
    "father": "padre",
    "heaven. Idols were called «cosas de turey»": "cielo",
    "the native name of tobacco": "tabaco",
    "stony, rocky, rough": "pedregoso",
    "friend, companion": "amigo",
    "the front, forehead; a beginning": "frente",
    "shining, glowing": "brillante",
    "masks or figures": "máscara",
    "a trough": "batea",
    "an ointment": "ungüento",
    "a species of parrot, macrocercus tricolor": "guacamayo",
    "gold, brass, any reddish metal": "oro",
    "gold, used especially in Cuba and on the Bahamas": "oro",
    "gold, probably akin to hobin": "oro",
    "a wood, a spot covered with trees": "bosque",
    # el campo de RANGO, que es donde cae `diao` y por eso se traduce entero:
    # sin esto la pregunta «¿hay un diao taíno?» se contestaría sobre una lista
    # a la que le faltan justo los títulos.
    "a title applied to the highest chiefs": "señor",
    "the title applied to the petty chiefs": "noble",
    "title applied to sub-chiefs ruling villages": "cacique",
    "a term applied to the lowest class of the inhabitants": "plebeyo",
    "an impure sort of gold": "oro",
    "the spirit of the dead": "alma",
    "the spirit of the living": "alma",
    "the divinities worshipped by the natives («Lo mismo que nosotros llamamos Diablo») — Not evil": "ídolo",
    "a song chanted alternately by the priests and the people at their feasts": "canto",
    "a large house holding several hundred persons": "casa",
    "a house of conical shape": "casa",
    "a loft for drying maize": "desván",
    "the breech cloth made of cotton and worn around the middle": "manta",
    "the pipe used in smoking the cohoba": "pipa",
    "a poisonous liquor expressed from the cassava root": "veneno",
    "a vault for storing provisions": "depósito",
    "ornaments for the ears hammered from native gold": "zarcillo",
}

# Cómo se saca la glosa de una cita de crónica. Son las fórmulas que Oviedo,
# Las Casas y Pané usan, y el script emite el inventario entero de lo que
# extrae para que se pueda revisar a ojo (regla 6).
PATRONES_GLOSA_CRONICA = [
    ("que quiere deçir/decir X", r"que\s+quiere\s+de[cçzs]ir[,\s]+(?:en\s+[^,]{3,30},\s*)?([^,;.:»)]{3,40})"),
    ("es/son X", r"^\s*[«\"]?\w+\s+(?:es|son)\s+(?:el|la|los|las|un|una|unos|unas)?\s*([^,;.:»)]{3,40})"),
    ("que es/son X", r"\bque\s+(?:es|son)\s+(?:el|la|los|las|un|una|unos|unas)?\s*([^,;.:»)]{3,40})"),
    ("llaman/nombran … X", r"(?:llaman|nombran|llamaban|llámanla|llámasse)\s+(?:en\s+[^,]{3,30}\s+)?"
                           r"(?:á|a)\s+(?:el|la|los|las|esta|este|aquella)\s+([^,;.:»)]{3,40})"),
]

# Donde el extractor no llega y la voz PESA, la glosa se declara a mano con su
# cita. Tabla corta, emitida entera. (obra, forma) -> glosa castellana.
GLOSA_DECLARADA = {
    ("oviedo-y-valdes-1851", "dalihao"): "señor",
    ("oviedo-y-valdes-1851", "buhití"): "agorero",
    ("oviedo-y-valdes-1851", "hico"): "soga",
    ("oviedo-y-valdes-1851", "buhio"): "casa",
    ("oviedo-y-valdes-1851", "caney"): "casa",
    ("oviedo-y-valdes-1851", "canoa"): "canoa",
    ("oviedo-y-valdes-1851", "hamaca"): "cama",
    ("oviedo-y-valdes-1851", "mahiz"): "maíz",
    ("oviedo-y-valdes-1851", "caçabi"): "pan",
    ("oviedo-y-valdes-1851", "yuca"): "yuca",
    ("oviedo-y-valdes-1851", "axi"): "ají",
    ("oviedo-y-valdes-1851", "batata"): "batata",
    ("oviedo-y-valdes-1851", "guayaba"): "guayaba",
    ("oviedo-y-valdes-1851", "papaya"): "papaya",
    ("oviedo-y-valdes-1851", "manati"): "manatí",
    ("oviedo-y-valdes-1851", "hutia"): "jutía",
    ("oviedo-y-valdes-1851", "yvana"): "iguana",
    ("oviedo-y-valdes-1851", "caçique"): "cacique",
    ("oviedo-y-valdes-1851", "huracan"): "huracán",
    ("oviedo-y-valdes-1851", "tabaco"): "tabaco",
    ("oviedo-y-valdes-1851", "bixa"): "tinte",
    ("oviedo-y-valdes-1851", "naguas"): "manta",
    ("oviedo-y-valdes-1851", "macana"): "macana",
    ("oviedo-y-valdes-1851", "savana"): "llanura",
    ("oviedo-y-valdes-1851", "bexuco"): "bejuco",
    ("oviedo-y-valdes-1851", "mani"): "maní",
    ("oviedo-y-valdes-1851", "naboria"): "criado",
    ("oviedo-y-valdes-1851", "duho"): "asiento",
    ("oviedo-y-valdes-1851", "çemi"): "ídolo",
    ("oviedo-y-valdes-1851", "areyto"): "canto",
    ("oviedo-y-valdes-1851", "guanin"): "oro",
    ("oviedo-y-valdes-1851", "conuco"): "conuco",
    ("las-casas-1875", "cayos"): "isla",
    ("las-casas-1875", "canoas"): "canoa",
    ("las-casas-1875", "cazabí"): "pan",
    ("las-casas-1875", "hamacas"): "cama",
    ("las-casas-1875", "iguana"): "iguana",
    ("las-casas-1875", "bohío"): "casa",
    ("las-casas-1875", "nacan"): "centro",
    ("las-casas-1875", "axí"): "ají",
    ("las-casas-1875", "batatas"): "batata",
    ("las-casas-1875", "caona"): "oro",
    ("las-casas-1875", "nucay"): "oro",
    ("las-casas-1875", "tabacos"): "tabaco",
    ("las-casas-1875", "maíz"): "maíz",
    ("las-casas-1875", "Cacique"): "cacique",
    ("las-casas-1875", "çabanas"): "llanura",
    ("las-casas-1875", "hutias"): "jutía",
    ("las-casas-1875", "turey"): "cielo",
    ("las-casas-1875", "guanin"): "oro",
    ("las-casas-1875", "macana"): "macana",
    ("pane-c1498", "cemíes"): "ídolo",
    ("pane-c1498", "cohoba"): "polvo",
    ("pane-c1498", "buhitihu / buhuitihu / bohutis"): "médico",
    ("pane-c1498", "conucos"): "conuco",
    ("pane-c1498", "cazabi"): "pan",
    ("pane-c1498", "guanines"): "oro",
    ("pane-c1498", "cibas"): "piedra",
    ("pane-c1498", "cobo"): "caracol",
    ("pane-c1498", "operito"): "muerto",
    ("pane-c1498", "opia"): "alma",
    ("pane-c1498", "goeiz"): "alma",
    ("pane-c1498", "yuca"): "yuca",
    ("pane-c1498", "jobos"): "árbol",
    ("pane-c1498", "tona"): "rana",
    ("pane-c1498", "naboria"): "criado",
}

# El campo de RANGO Y ALIANZA, que es donde cae `diao` y donde viajan las
# palabras. Se declara aquí para que el cruce del campo sea auditable y no
# una selección a ojo hecha después de ver el resultado.
CAMPO_DE_RANGO = {
    "glosas": frozenset({"cacique", "senor", "jefe", "principal", "noble", "amigo", "aliado",
                         "criado", "sacerdote", "padre", "rey", "titulo", "pariente"}),
    "cats": frozenset({"título", "titulo"}),
    "categorias": frozenset({"jerarquia", "autoridad", "parentesco", "organizacion-politica"}),
}


# ═════════════════════════════════════════════════════════════════════════
# Glosas castellanas  (el filtro de significado)
# ═════════════════════════════════════════════════════════════════════════
def sin_diacriticos(s, conservar=True):
    out = []
    for ch in unicodedata.normalize("NFD", str(s or "")):
        if unicodedata.category(ch) == "Mn":
            if conservar and ch == "̈" and out and out[-1] in "uU":
                out.append(ch)
            elif conservar and ch == "̃" and out and out[-1] in "nN":
                out.append(ch)
            continue
        out.append(ch)
    return unicodedata.normalize("NFC", "".join(out))


def _norm_es(w):
    """Una palabra castellana, colonial o moderna, a una clave comparable."""
    w = re.sub(r"[^a-zñ]", "", sin_diacriticos(w, False).lower()).replace("ñ", "n")
    if not w:
        return ""
    w = re.sub(r"^h", "", w)
    w = re.sub(r"qu(?=[ao])", "cu", w)
    w = re.sub(r"g(?=[ei])", "j", w)              # muger -> mujer
    w = re.sub(r"c(?=[ei])", "s", w)
    w = w.replace("z", "s").replace("v", "b").replace("x", "j").replace("ll", "y")
    w = re.sub(r"y$", "i", w)
    if len(w) > 4 and w.endswith("es") and w[-3] not in VOCALES:
        w = w[:-2]
    elif len(w) > 3 and w.endswith("s") and w[-2] in VOCALES:
        w = w[:-1]
    return w


SINONIMOS = {_norm_es(a): _norm_es(b) for a, b in SINONIMOS_CRUDOS.items()}
ARTICULOS = {_norm_es(x) for x in "el la los las lo un una unos unas ser estar".split()}
INDEFINIDOS = {_norm_es(x) for x in "un una unos unas".split()}
# Homonimia castellana que el filtro no puede resolver (medida en el cruce achagua).
HOMONIMOS_DE_GLOSA = {_norm_es("este")}


def es_palabra(w):
    n = _norm_es(w)
    return SINONIMOS.get(n, n)


def conceptos(glosa):
    """[(cabeza, exacto, segmento)] de una glosa. `exacto` = una sola palabra."""
    g = str(glosa or "")
    g = re.sub(r"\([^)]*\)", " ", g)
    g = re.sub(r"\([^)]*$", " ", g)
    g = re.sub(r"[,;]\s*-\w+", " ", g)
    g = re.sub(r"«[^»]*»", " ", g)
    g = re.sub(r"\[[^\]]*\]", " ", g)
    g = re.sub(r"\bv\.\s*g\..*$", " ", g, flags=re.I)
    g = re.sub(r"&\s*c\.?", " ", g)
    out = []
    for p in re.split(r"[,;:./¿?¡!=]|\s+(?:o|ó|u|vel)\s+", g):
        ws = [es_palabra(w) for w in p.split()]
        ws = [w for w in ws if w]
        clase = bool(ws) and ws[0] in INDEFINIDOS
        while ws and ws[0] in ARTICULOS:
            ws.pop(0)
        if ws and not (len(ws) == 1 and len(ws[0]) < 2):
            exacto = len(ws) == 1 and not clase and ws[0] not in HOMONIMOS_DE_GLOSA
            out.append((ws[0], exacto, " ".join(ws)))
    return out


# ═════════════════════════════════════════════════════════════════════════
# Formas
# ═════════════════════════════════════════════════════════════════════════
def fon(forma, orto, gu):
    f = sin_diacriticos(forma).lower()
    if orto == "linguistica":
        f = re.sub(r"(?<![cstkp])h", "j", f)
    f = fonemizar(f, gu_es_w=gu).replace("ü", "u")
    return re.sub(r"(.)\1+", r"\1", f)


def radicales(f, lengua):
    """La forma entera primero y luego sus radicales, en orden ESTABLE.

    ⚠️ Devolver un `set` aquí haría el script irreproducible: el hash de las
    cadenas se aleatoriza por proceso, el orden de los candidatos cambiaría
    entre corridas y los empates de `mejor()` se resolverían distinto. Con
    `--check` eso sería ruido puro. Sale lista ordenada, y la forma completa
    siempre en la posición 0.
    """
    pref, suf = AFIJOS.get(lengua, ((), ()))
    otros = set()
    for p in pref:
        if (f.startswith(p) and len(f) - len(p) >= MIN_FONEMAS
                and (len(p) > 1 or f[len(p)] not in VOCALES)):
            otros.add(f[len(p):])
    for g in list(otros) + [f]:
        for s in suf:
            if g.endswith(s) and len(g) - len(s) >= MIN_FONEMAS:
                otros.add(g[: -len(s)])
    otros.discard(f)
    return [f] + sorted(otros)


def dominio_de(v):
    if v.get("cat") in CATS_DE_FILIACION:
        return "filiacion"
    return DOMINIO_POR_CATEGORIA.get(v.get("categoria") or "", "sin-declarar")


# ═════════════════════════════════════════════════════════════════════════
# Carga
# ═════════════════════════════════════════════════════════════════════════
def _estrato(lengua, v):
    n = v.get("notas") or ""
    if lengua == "taíno":
        if "Brinton" in n:
            return "Brinton 1871 (sin `procedencia.obra`)"
        return "sin estrato declarado — 0 de 52 taínas del lexicón tienen procedencia"
    if lengua == "lokono":
        if "Perea" in n:
            return "Perea 1942"
        for m, et in (("Oliver", "Oliver 1989 A-2"), ("Pet 1987", "Pet 1987"),
                      ("Goeje", "Goeje 1928"), ("Brinton", "Brinton 1871")):
            if m in n:
                return et
    if lengua == "paraujano":
        return "Wilbert 1958-59 vía Oliver 1989 A-2"
    if lengua == "achagua" and "Neira" in n:
        return "Neira y Ribero 1762"
    return "sin estrato declarado"


def cargar_comparanda(lengua, gu):
    """Las entradas del lexicón de una lengua hermana o de contacto."""
    entradas = []
    gemelas = set(CL.FORMA_DE_LA_ESFERA)          # clave castellana con gemela indígena
    for k, v in CL.VOCABULARIO_BASE.items():
        if v.get("fuente") != lengua:
            continue
        if lengua == "taíno" and k in gemelas:
            continue    # `maíz` y `maisi` son la MISMA voz: entra la indígena
        base = re.sub(r"-(lokono|achagua|kalinago|wayuu|wayunaiki|paraujano|caribe|\d+)$", "", k)
        formas = [base] + ([v["forma_fuente"]] if v.get("forma_fuente") else [])
        orto = "linguistica" if lengua in ("wayunaiki", "lokono") else "colonial"
        cands = []
        for fm in dict.fromkeys(formas):
            fm2 = forma_comparable(fm, v) if lengua == "lokono" else fm
            fb = fon(fm2, orto, gu)
            if len(fb) < MIN_FONEMAS:
                continue
            for r in radicales(fb, lengua):
                cands.append((r, fm, r != fb))
        ficha = {"forma": base, "glosa": v.get("sig"), "estrato": _estrato(lengua, v)}
        notas = v.get("notas") or ""
        # SESGO INVERSO: la nota se escribió mirando al caquetío.
        mirando_caq = bool(re.search(r"caquet", notas, re.I))
        if mirando_caq:
            ficha["aviso"] = ("la `notas` de esta entrada se escribió comparándola con el caquetío: "
                              "la FORMA es de la fuente, la comparación no es independiente")
        if lengua == "taíno":
            ficha["marca_castellana"] = k in (set(CL.SIN_FORMA_DE_LA_ESFERA)
                                              | set(CL.CASTELLANO_CORRIENTE))
            ficha["dice_paso_al_espanol"] = "español" in notas
        entradas.append({"lengua": lengua, "forma": base, "glosa": v.get("sig"),
                         "clave": k, "cands": cands, "conceptos": conceptos(v.get("sig")),
                         "fon_base": cands[0][0] if cands else "",
                         "ficha": ficha, "dominio": dominio_de(v),
                         "nota_mira_al_caquetio": mirando_caq})
    return entradas


# ═════════════════════════════════════════════════════════════════════════
# T11 · Las transcripciones de T1/T2 como fuente taína (con obra y página)
# ═════════════════════════════════════════════════════════════════════════
def _seccion(Y, ruta):
    o = Y
    for k in ruta.split("."):
        o = (o or {}).get(k)
    return o or []


def glosa_de_cronica(texto, obra, forma):
    """La glosa castellana de una voz, sacada de la cita con reglas declaradas."""
    decl = GLOSA_DECLARADA.get((obra, str(forma)))
    if decl:
        return decl, "declarada"
    t = re.sub(r"\s+", " ", str(texto or ""))
    for nombre, patron in PATRONES_GLOSA_CRONICA:
        m = re.search(patron, t, re.I)
        if m:
            g = m.group(1).strip(" «»\"'")
            g = re.sub(r"\s+(?:que|de|en|á|a|con|por|para)\s+.*$", "", g).strip()
            if 2 < len(g) < 40 and not re.search(r"\d", g):
                return g, nombre
    return None, "sin-glosa-extraible"


def cargar_taino_transcripciones(gu):
    """Las voces taínas de `6-fusion/taino_*.yaml`, con su clave foránea.

    Es lo que el cruce del 21 no leía. Cada entrada trae `obra` y `pagina`, que
    es justo lo que a las 43 del lexicón les falta (regla 8): «Brinton 1871»
    escrito en `notas` no es una clave foránea.
    """
    entradas, bitacora, fuera = [], [], collections.Counter()
    for spec in YAML_TAINO:
        Y = yaml.safe_load(io.open(os.path.join(R, "6-fusion", spec["archivo"]), encoding="utf-8"))
        for ruta, clase in spec["secciones"].items():
            for e in _seccion(Y, ruta):
                if not isinstance(e, dict):
                    continue
                forma = e.get("forma_probable") or e.get("forma_fuente") or e.get("forma")
                if isinstance(forma, list):
                    forma = forma[0] if forma else None
                if not forma:
                    fuera["sin forma"] += 1
                    continue
                if clase != "taíno":
                    fuera[clase] += 1
                    bitacora.append({"forma": str(forma), "obra": spec["obra"], "seccion": ruta,
                                     "glosa": None, "como": f"EXCLUIDA · {clase}"})
                    continue
                cruda = e.get("glosa_fuente") if "glosa_fuente" in e else e.get("glosa")
                if spec["obra"] == "brinton-1871":
                    g = GLOSA_EN_ES.get(str(cruda).strip())
                    como = "GLOSA_EN_ES" if g else "sin-traducir (declarado)"
                else:
                    g, como = glosa_de_cronica(cruda, spec["obra"], forma)
                bitacora.append({"forma": str(forma), "obra": spec["obra"], "seccion": ruta,
                                 "glosa": g, "como": como,
                                 "cita": str(cruda)[:90].replace("\n", " ")})
                if not g:
                    fuera["sin glosa extraíble"] += 1
                    continue
                # la primera forma si la fuente da varias grafías separadas por /
                base = re.split(r"\s*/\s*", str(forma))[0].strip().lower()
                cands = []
                for fm in dict.fromkeys([base] + [x.strip().lower()
                                                  for x in re.split(r"\s*/\s*", str(forma))]):
                    fb = fon(fm, "colonial", gu)
                    if len(fb) < MIN_FONEMAS:
                        continue
                    for r_ in radicales(fb, "taíno"):
                        cands.append((r_, fm, r_ != fb))
                if not cands:
                    fuera["forma de menos de tres fonemas"] += 1
                    continue
                pag = e.get("pagina_impresa") or e.get("pagina") or e.get("capitulo")
                if isinstance(pag, list):
                    pag = ", ".join(str(x) for x in pag)
                estrato = f"{spec['obra']}" + (f" p. {pag}" if pag else "")
                cronista = e.get("cronista")
                if cronista:
                    estrato += f" (quien atestigua: {cronista})"
                entradas.append({
                    "lengua": "taíno", "forma": base, "glosa": g, "clave": f"{base}@{spec['obra']}",
                    "cands": cands, "conceptos": conceptos(g), "fon_base": cands[0][0],
                    "ficha": {"forma": base, "glosa": g, "estrato": estrato,
                              "obra": spec["obra"], "pagina": pag,
                              "de_la_transcripcion": spec["archivo"]},
                    "dominio": "sin-declarar", "nota_mira_al_caquetio": False,
                    "de_transcripcion": True})
    return entradas, bitacora, dict(sorted(fuera.items()))


def fundir_taino(del_lexicon, de_transcripcion):
    """Una lista taína sin duplicar la misma voz, pero sin perder ninguna cita.

    Dos entradas son la misma voz si comparten lema fonémico Y concepto exacto.
    Se conserva la que TIENE obra y página (regla 8) y la otra se apunta en
    `tambien_en`: el dato no se pierde, el denominador no se infla.
    """
    por_llave, fusiones = {}, []
    for e in list(de_transcripcion) + list(del_lexicon):
        cab = tuple(sorted({c for c, ex, _ in e["conceptos"] if ex}))
        llave = (e["fon_base"], cab)
        if llave in por_llave:
            v = por_llave[llave]
            v["ficha"].setdefault("tambien_en", []).append(e["ficha"]["estrato"])
            fusiones.append(f"{e['forma']} «{e['glosa']}» → {v['clave']}")
            continue
        por_llave[llave] = e
    salida = sorted(por_llave.values(), key=lambda e: str(e["clave"]))
    return salida, fusiones


def medir_jirajaroide_frontera():
    """Por qué el control que el encargo sugería no sirve — medido, no dicho."""
    import json
    d = json.load(io.open(os.path.join(R, "curiana_sim", "jirajaroide_frontera_lexicon.json"),
                          encoding="utf-8"))
    v = d["vocabulario"]
    vacias = [e for e in v if str(e.get("forma")).strip() == "?"]
    reales = [e for e in v if e not in vacias]
    caq = [e for e in reales if "caquetio" in str(e.get("lengua", ""))]
    declaradas = (d.get("_estadisticas") or {}).get("pendientes_verificacion")
    out = {
        "archivo": "curiana_sim/jirajaroide_frontera_lexicon.json",
        "por_que_se_miro": "el encargo lo sugería como lista de control no arahuaca",
        "entradas": len(v),
        "ranuras_vacias_con_la_forma_literal_?": len(vacias),
        "entradas_con_forma": len(reales),
        "de_esas_caquetias": len(caq),
        "lenguas_de_las_que_quedan": sorted({str(e.get("lengua")) for e in reales
                                             if "caquetio" not in str(e.get("lengua", ""))}),
        "conceptos_cruzables": 0,
        "veredicto": ("NO SIRVE: lo que queda son topónimos y etnónimos sin glosa léxica, así que "
                      "no hay ni un concepto que cruzar. El control se sacó del vocabulario "
                      "jirajara/ayomán de Jahn 1927, que sí tiene formas con glosa castellana."),
    }
    if declaradas is not None and declaradas != len(vacias):
        out["⚠️_su_propia_estadistica_no_cuadra"] = (
            f"`_estadisticas.pendientes_verificacion` dice {declaradas} y las ranuras con forma «?» "
            f"son {len(vacias)}. Es una cifra escrita a mano dentro del propio archivo (regla 1).")
    return out


def cargar_control(gu):
    """El jirajara/ayomán de Jahn 1927: lengua NO arahuaca."""
    Y = yaml.safe_load(io.open(YAML_CONTROL, encoding="utf-8"))
    entradas = []
    for f in Y["vocabulario"]:
        formas = [x for x in (f.get("jirajara"), f.get("ayoman")) if x]
        cands = []
        for fm in formas:
            for tok in re.split(r"[\s,;]+", str(fm)):
                fb = fon(tok.strip("-!¡?¿"), "colonial", gu)
                if len(fb) < MIN_FONEMAS:
                    continue
                for r in radicales(fb, CONTROL):
                    cands.append((r, tok, r != fb))
        if not cands:
            continue
        entradas.append({"lengua": CONTROL, "forma": formas[0], "glosa": f["castellano"],
                         "clave": f["castellano"], "cands": cands,
                         "conceptos": conceptos(f["castellano"]),
                         "fon_base": cands[0][0],
                         "ficha": {"forma": formas[0], "glosa": f["castellano"],
                                   "estrato": "Jahn 1927 pp. 388-391 (CONTROL, no comparanda)"},
                         "dominio": "sin-declarar", "nota_mira_al_caquetio": False})
    return entradas, Y["meta"]


def derivada_de(v, capa):
    """De qué lengua dicen las `notas` que se sacó la FORMA caquetía."""
    if capa == ATESTIGUADO:
        return []
    n = f"{v.get('notas') or ''} || {v.get('sig') or ''}"
    crudas = set()
    for t in re.findall(r"cognado en ([^\s—;,.]+)", n) + re.findall(r"etiquetada `([^`]+)`", n):
        crudas.update(t.lower().split("/"))
    if re.search(r"desde el WAYUU|<[^)]*Wayunaiki", n) or n.startswith("Way. "):
        crudas.add("wayunaiki")
    if n.startswith("Lok. "):
        crudas.add("lokono")
    out = set()
    for f in crudas:
        f = f.replace("-cogn", "").strip("`() ")
        if f.startswith("wayu"):
            out.add("wayunaiki")
        elif f.startswith("lokono"):
            out.add("lokono")
        elif f.startswith("proto"):
            out.add("proto-arahuaco")
        elif f.startswith("ta"):
            out.add("taíno")
        elif f:
            out.add(f)
    return sorted(out)


def cargar_caquetio(gu):
    out = []
    for k, v in CL.VOCABULARIO_BASE.items():
        capa = CL.capa_epistemica(v.get("fuente"))
        if not capa:
            continue
        base = re.sub(r"-\d+$", "", k)
        orto = "linguistica" if ("reconstru" in capa or "hipot" in capa) else "colonial"
        cands = [(fon(base, orto, gu), base)]
        if v.get("forma_fuente"):
            cands.append((fon(v["forma_fuente"], "colonial", gu), v["forma_fuente"]))
        cands = list({c[0]: c for c in cands if c[0]}.values())
        out.append({"clave": k, "capa": capa, "sig": v.get("sig"), "cat": v.get("cat"),
                    "categoria": v.get("categoria"), "forma_fuente": v.get("forma_fuente"),
                    "notas": v.get("notas") or "", "cands": cands,
                    "conceptos": conceptos(v.get("sig")), "dominio": dominio_de(v),
                    "derivada_de": derivada_de(v, capa)})
    return out


# ═════════════════════════════════════════════════════════════════════════
# Medida
# ═════════════════════════════════════════════════════════════════════════
def indexar(entradas):
    exacto, cualquiera = collections.defaultdict(list), collections.defaultdict(list)
    for e in entradas:
        for cab, ex, _seg in e["conceptos"]:
            if ex:
                exacto[cab].append(e)
            cualquiera[cab].append(e)
    return exacto, cualquiera


def mejor(caq_cands, entradas):
    best = (-1.0, None, None, None)
    for fa, ma in caq_cands:
        sm = difflib.SequenceMatcher(None, autojunk=False)
        sm.set_seq2(fa)
        for e in entradas:
            for fb, mb, rad in e["cands"]:
                sm.set_seq1(fb)
                r = sm.ratio()
                if r > best[0]:
                    best = (r, e, (fb, mb, rad), (fa, ma))
    return best


def emparejar(c, idx_exacto, idx_cualquiera):
    exactas_cabezas = {cab for cab, ex, _ in c["conceptos"] if ex}
    todas_cabezas = {cab for cab, _, _ in c["conceptos"]}
    vistos, exactas, cortas = set(), [], 0
    for cab in sorted(exactas_cabezas):
        for e in idx_exacto.get(cab, []):
            if id(e) not in vistos:
                vistos.add(id(e))
                if e["cands"]:
                    exactas.append(e)
                else:
                    cortas += 1
    cercanas = {id(e) for cab in todas_cabezas for e in idx_cualquiera.get(cab, [])} - vistos
    return exactas, len(cercanas), cortas


def veredicto(sim, n_exactas, n_cercanas, corto, circ, n_cortas=0):
    if corto:
        return "no-comparable", "la forma caquetía tiene menos de tres fonemas"
    if n_exactas == 0:
        if n_cortas:
            return "no-comparable", "la glosa está, pero su forma tiene menos de tres fonemas"
        return "no-comparable", ("solo glosa cercana (hiperónimo o frase)" if n_cercanas
                                 else "el concepto no está en esta lengua")
    if sim >= UMBRAL_PARECIDO and circ:
        return "circular", ("la forma caquetía se derivó de esta lengua (o del proto-arahuaco): "
                            "el parecido es de construcción")
    if sim >= UMBRAL_COGNADO:
        return "cognado-probable", ""
    if sim >= UMBRAL_PARECIDO:
        return "parecido-debil", ""
    return "sin-parecido", ""


def medir(gu, con_nulo=True):
    t0 = time.time()
    lengs = {L: cargar_comparanda(L, gu) for L in LENGUAS + INFORMATIVAS}
    lengs[CONTROL], meta_control = cargar_control(gu)
    # T11: las transcripciones de T1/T2 entran aquí, y sólo aquí. Es el cambio
    # que mueve el denominador del cruce del 21.
    del_lexicon = lengs["taíno"]
    de_transcr, bitacora_tr, fuera_tr = cargar_taino_transcripciones(gu)
    lengs["taíno"], fusiones_tr = fundir_taino(del_lexicon, de_transcr)
    transcripciones = {
        "entradas_del_lexicon": len(del_lexicon),
        "entradas_de_las_transcripciones": len(de_transcr),
        "tras_fundir_la_misma_voz": len(lengs["taíno"]),
        "con_obra_y_pagina": sum(1 for e in lengs["taíno"] if e["ficha"].get("obra")),
        "sin_clave_foranea": sum(1 for e in lengs["taíno"] if not e["ficha"].get("obra")),
        "descartadas_por": fuera_tr,
        "fusiones": fusiones_tr,
        "bitacora_de_glosas": bitacora_tr,
    }
    idx = {L: indexar(es) for L, es in lengs.items()}
    caq = cargar_caquetio(gu)

    res = []
    for c in caq:
        corto = max((len(fa) for fa, _ in c["cands"]), default=0) < MIN_FONEMAS
        por = {}
        for L in TODAS:
            exactas, n_cerc, n_cortas = emparejar(c, *idx[L])
            ranking = []
            if not corto:
                for e in exactas:
                    s, _, cb, ca = mejor(c["cands"], [e])
                    ranking.append((s, e, cb, ca))
                ranking.sort(key=lambda x: (-x[0], x[1]["clave"]))
            sim = ranking[0][0] if ranking else 0.0
            circ = L in c["derivada_de"] or "proto-arahuaco" in c["derivada_de"]
            ver, porque = veredicto(sim, len(exactas), n_cerc, corto, circ, n_cortas)
            por[L] = {"exactas": exactas, "n_cercanas": n_cerc, "n_cortas": n_cortas,
                      "ranking": ranking, "sim": sim, "veredicto": ver, "porque": porque}
        res.append({"c": c, "corto": corto, "por": por})

    # ── modelo nulo sobre la capa atestiguada ──
    rng = random.Random(SEMILLA)
    pool = {L: sorted([e for e in lengs[L] if e["cands"]], key=lambda e: str(e["clave"]))
            for L in TODAS}
    if con_nulo:
        for r in res:
            if r["c"]["capa"] != ATESTIGUADO or r["corto"]:
                continue
            r["nulo"] = {}
            for L in TODAS:
                n = len(r["por"][L]["exactas"])
                if not n or len(pool[L]) <= n:
                    continue
                excl = {id(e) for e in r["por"][L]["exactas"]}
                sims = []
                for _ in range(REPLICAS):
                    muestra, ids = [], set()
                    intentos = 0
                    while len(muestra) < n and intentos < 500:
                        intentos += 1
                        e = pool[L][rng.randrange(len(pool[L]))]
                        if id(e) in excl or id(e) in ids:
                            continue
                        ids.add(id(e))
                        muestra.append(e)
                    sims.append(max(0.0, mejor(r["c"]["cands"], muestra)[0]) if muestra else 0.0)
                r["nulo"][L] = sims
    return {"res": res, "lengs": lengs, "idx": idx, "pool": pool,
            "meta_control": meta_control, "transcripciones": transcripciones,
            "segundos": round(time.time() - t0, 1)}


# ═════════════════════════════════════════════════════════════════════════
# Clase de cada pareja: herencia / préstamo / casualidad / indecidible
# ═════════════════════════════════════════════════════════════════════════
def clase_de_pareja(r, p_nulo):
    """La clase NO la decide el parecido: el parecido sólo abre la candidatura.

    La decide (a) el DOMINIO —la tabla de `minar-fuente` §3: lo que viaja
    entre lenguas sin parentesco y lo que casi nunca viaja— y (b) si el mismo
    concepto se parece también en las hermanas, que es lo que distingue una
    herencia arahuaca común de un encuentro sólo taíno-caquetío.
    """
    c, por = r["c"], r["por"]
    sim = por["taíno"]["sim"]
    if por["taíno"]["veredicto"] in ("no-comparable", "sin-parecido"):
        return None, ""
    if por["taíno"]["veredicto"] == "circular":
        return "circular", "la forma caquetía se derivó del taíno: el parecido es de construcción"
    par = por["taíno"]["ranking"][0]
    corta = min(len(par[2][0]), len(par[3][0])) <= MIN_FONEMAS
    if corta:
        return "casualidad", f"parecido sobre {MIN_FONEMAS} fonemas o menos: barato por construcción"
    if p_nulo is not None and p_nulo > 0.10:
        return "casualidad", (f"el modelo nulo alcanza este parecido en el {p_nulo:.0%} de las "
                              f"réplicas: no hace falta parentesco para producirlo")
    hermanas = [L for L in ("lokono", "wayunaiki", "achagua")
                if por[L]["exactas"] and por[L]["sim"] >= UMBRAL_PARECIDO]
    dominio = c["dominio"]
    if dominio == "viajero":
        return "préstamo-probable", (
            "el dominio es de los que viajan entre lenguas sin parentesco (cultígeno, bicho, "
            "mercancía, utensilio, rito): compartirlo es dato de comercio y vecindad, no de filiación"
            + (f"; y se parece además en {', '.join(hermanas)}" if hermanas else ""))
    if dominio == "filiacion" and len(hermanas) >= 2:
        return "herencia-probable", (
            "vocabulario que casi nunca viaja y el mismo concepto se parece también en "
            + ", ".join(hermanas) + ": arahuaco común, no un lazo taíno-caquetío particular")
    if dominio == "filiacion":
        return "indecidible", (
            "vocabulario de filiación, pero el parecido no se repite en las hermanas: con una sola "
            "pareja no se decide si es innovación compartida o casualidad")
    if len(hermanas) >= 2:
        return "herencia-probable", (
            "el mismo concepto se parece también en " + ", ".join(hermanas)
            + ": patrimonio arahuaco antes que lazo taíno-caquetío")
    return "indecidible", ("dominio sin declarar o ambiguo y sin apoyo en las hermanas: "
                           "la pareja queda abierta")


# ═════════════════════════════════════════════════════════════════════════
# Resumen de la capa atestiguada
# ═════════════════════════════════════════════════════════════════════════
def resumir(M):
    ates = [r for r in M["res"] if r["c"]["capa"] == ATESTIGUADO]
    utiles = [r for r in ates if not r["corto"]]
    por_lengua = {}
    for L in TODAS:
        comp = [r for r in utiles if r["por"][L]["exactas"]]
        obs_p = sum(r["por"][L]["sim"] >= UMBRAL_PARECIDO for r in comp)
        obs_c = sum(r["por"][L]["sim"] >= UMBRAL_COGNADO for r in comp)
        d = {"entradas_de_la_lengua": len(M["lengs"][L]),
             "conceptos_comparables": len(comp),
             "parecidos_ge_umbral": obs_p,
             "cognado_probable_ge_umbral_cognado": obs_c,
             "tasa_parecido": round(obs_p / len(comp), 3) if comp else None,
             "similitud_media": round(sum(r["por"][L]["sim"] for r in comp) / len(comp), 3) if comp else None,
             "candidatos_por_concepto_media": round(
                 sum(len(r["por"][L]["exactas"]) for r in comp) / len(comp), 2) if comp else None}
        con_nulo = [r for r in comp if "nulo" in r and L in r["nulo"]]
        if con_nulo:
            tot_p = [sum(r["nulo"][L][i] >= UMBRAL_PARECIDO for r in con_nulo) for i in range(REPLICAS)]
            tot_c = [sum(r["nulo"][L][i] >= UMBRAL_COGNADO for r in con_nulo) for i in range(REPLICAS)]
            media_nula = sum(sum(r["nulo"][L]) / REPLICAS for r in con_nulo) / len(con_nulo)
            obs_p_n = sum(r["por"][L]["sim"] >= UMBRAL_PARECIDO for r in con_nulo)
            obs_c_n = sum(r["por"][L]["sim"] >= UMBRAL_COGNADO for r in con_nulo)
            d["azar"] = {
                "conceptos_con_modelo_nulo": len(con_nulo),
                "parecidos_observados_en_esos": obs_p_n,
                "parecidos_esperados": round(sum(tot_p) / REPLICAS, 2),
                "cognados_observados_en_esos": obs_c_n,
                "cognados_esperados": round(sum(tot_c) / REPLICAS, 2),
                "similitud_media_esperada": round(media_nula, 3),
                "p_parecidos_ge_observado": round(sum(t >= obs_p_n for t in tot_p) / REPLICAS, 3),
                "p_cognados_ge_observado": round(sum(t >= obs_c_n for t in tot_c) / REPLICAS, 3),
            }
            d["exceso_de_parecidos_sobre_el_azar"] = round(obs_p_n - sum(tot_p) / REPLICAS, 2)
        por_lengua[L] = d
    return {
        "entradas_caquetio_atestiguado": len(ates),
        "formas_de_menos_de_tres_fonemas": len(ates) - len(utiles),
        "con_concepto_en_alguna_de_las_cuatro": len(
            [r for r in utiles if any(r["por"][L]["exactas"] for L in LENGUAS)]),
        "con_concepto_en_las_cuatro": len(
            [r for r in utiles if all(r["por"][L]["exactas"] for L in LENGUAS)]),
        "por_lengua": por_lengua,
    }


def p_nulo_de(r, L):
    if "nulo" not in r or L not in r["nulo"]:
        return None
    s = r["por"][L]["sim"]
    return sum(x >= s for x in r["nulo"][L]) / REPLICAS


# ═════════════════════════════════════════════════════════════════════════
# Correspondencias: una sale una vez y no es nada; tres veces es una regla
# ═════════════════════════════════════════════════════════════════════════
def alinear(a, b):
    m = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag in ("equal", "replace"):
            for d in range(i2 - i1):
                m[i1 + d] = b[j1 + d] if j1 + d < j2 else "∅"
        elif tag == "delete":
            for i in range(i1, i2):
                m[i] = "∅"
    return m


def reglas_de(a, b):
    m = alinear(a, b)
    out = []
    for i, x in enumerate(a):
        if x in VOCALES:
            continue
        y = m.get(i, "∅")
        if y != x:
            out.append((x, y, False))
            if i == 0:
                out.append((x, y, True))
    return out


def nombre_regla(x, y, inicial, lengua="taíno"):
    return f"caq {'#' if inicial else ''}{x} ~ {lengua[:3]} {y}"


def juicio_regla(apoyos, aplicables, tasa, tasa_azar):
    if apoyos < 3:
        return (f"NO es una regla: {apoyos} apoyo(s). Una correspondencia que sale una o dos "
                "veces no es nada (hacen falta tres)")
    if aplicables < 5:
        return "sin casos suficientes para ponerla a predecir (menos de 5 aplicables)"
    if tasa is not None and tasa_azar is not None and tasa >= 0.5 and tasa >= 2 * tasa_azar:
        return "predice por encima del azar"
    return "NO predice: falla o no supera al azar"


def aplica(a, b, x, y, inicial):
    pos = [i for i, c in enumerate(a) if c == x and (not inicial or i == 0)]
    if not pos:
        return None
    m = alinear(a, b)
    return any(m.get(i) == y for i in pos)


def mejor_forma(a, entradas):
    _s, _e, cb, _ca = mejor([(a, a)], entradas)
    return cb[0] if cb else None


def prueba_dejando_fuera(M, lenguas):
    rng = random.Random(SEMILLA + 2)
    out = {"diseño": (
        "Para cada lengua se alinean los pares atestiguados que se parecen (cognado-probable o "
        "parecido-debil) y se anotan sus correspondencias consonánticas no idénticas. Cada una "
        "predice sobre TODOS los demás conceptos atestiguados con glosa exacta en esa lengua "
        "(fuera los que la sugirieron). La tasa por azar repite la prueba con entradas al azar de "
        f"la misma lengua ({REPLICAS} réplicas). Juicio: hacen falta 3 apoyos para llamarla regla, "
        "y 5 casos aplicables para ponerla a predecir.")}
    for L in lenguas:
        base = [r for r in M["res"] if r["c"]["capa"] == ATESTIGUADO and not r["corto"]
                and r["por"][L]["exactas"]]
        base.sort(key=lambda r: r["c"]["clave"])
        pool = M["pool"][L]
        cnt, apoyos, pares = collections.Counter(), collections.defaultdict(list), 0
        for r in base:
            p = r["por"][L]
            if p["veredicto"] not in ("cognado-probable", "parecido-debil"):
                continue
            pares += 1
            _s, _e, cb, ca = p["ranking"][0]
            for regla in set(reglas_de(ca[0], cb[0])):
                cnt[regla] += 1
                apoyos[regla].append((r["c"]["clave"], f"{ca[1]} ~ {cb[1]}"))
        reglas = []
        for regla, n in sorted(cnt.items(), key=lambda kv: (-kv[1], nombre_regla(*kv[0]))):
            x, y, ini = regla
            fuera = {k for k, _ in apoyos[regla]}
            aplicables = aciertos = az_ap = az_ac = 0
            casos = []
            for r in base:
                if r["c"]["clave"] in fuera:
                    continue
                a = r["c"]["cands"][0][0]
                b = mejor_forma(a, r["por"][L]["exactas"])
                h = aplica(a, b, x, y, ini) if b else None
                if h is None:
                    continue
                aplicables += 1
                aciertos += int(h)
                casos.append(f"{r['c']['clave']} ~ {b}: {'acierta' if h else 'falla'}")
                k = len(r["por"][L]["exactas"])
                if len(pool) <= k:
                    continue
                excl = {id(e) for e in r["por"][L]["exactas"]}
                for _ in range(REPLICAS):
                    muestra, ids, intentos = [], set(), 0
                    while len(muestra) < k and intentos < 500:
                        intentos += 1
                        e = pool[rng.randrange(len(pool))]
                        if id(e) in excl or id(e) in ids:
                            continue
                        ids.add(id(e))
                        muestra.append(e)
                    bz = mejor_forma(a, muestra) if muestra else None
                    hz = aplica(a, bz, x, y, ini) if bz else None
                    if hz is not None:
                        az_ap += 1
                        az_ac += int(hz)
            tasa = round(aciertos / aplicables, 3) if aplicables else None
            tasa_azar = round(az_ac / az_ap, 3) if az_ap else None
            reglas.append({"regla": nombre_regla(x, y, ini, L), "apoyos": n,
                           "visto_en": [f"{k}: {par}" for k, par in apoyos[regla]],
                           "aplicables": aplicables, "aciertos": aciertos,
                           "fallos": aplicables - aciertos, "tasa_de_acierto": tasa,
                           "tasa_por_azar": tasa_azar,
                           "juicio": juicio_regla(n, aplicables, tasa, tasa_azar),
                           "casos": casos[:15]})
        out[L] = {"pares_parecidos": pares, "conceptos_con_glosa_exacta": len(base),
                  "correspondencias_distintas": len(reglas),
                  "con_tres_apoyos_o_mas": sum(1 for x in reglas if x["apoyos"] >= 3),
                  "reglas": reglas[:12]}
    return out


# ═════════════════════════════════════════════════════════════════════════
# Auditar el cero: qué se perdió, y qué dice el canon que ya existe
# ═════════════════════════════════════════════════════════════════════════
def bloque_los_comparables(M):
    """Con un denominador de cuatro, los casos SON el resultado: van uno a uno."""
    out = []
    for r in M["res"]:
        if r["c"]["capa"] != ATESTIGUADO or not r["por"]["taíno"]["exactas"]:
            continue
        s, e, cb, ca = r["por"]["taíno"]["ranking"][0]
        out.append({
            "concepto": sorted({cab for cab, ex, _ in r["c"]["conceptos"] if ex}),
            "caquetio": r["c"]["clave"], "glosa_caquetia": r["c"]["sig"],
            "cita_caquetia": (r["c"]["notas"] or "sin nota")[:150],
            "taino": e["forma"], "glosa_taina": e["glosa"],
            "cita_taina": e["ficha"]["estrato"],
            "otros_candidatos_taino": [f"{e2['forma']} ({s2:.2f})"
                                       for s2, e2, _c, _a in r["por"]["taíno"]["ranking"][1:4]],
            "comparado": f"{ca[0]} ~ {cb[0]}", "similitud": round(s, 3),
            "dominio": r["c"]["dominio"],
            "lectura": "sin parecido: las dos lenguas usan palabras distintas para esto",
        })
    out.sort(key=lambda d: -d["similitud"])
    return out


def bloque_glosa_cercana(M):
    """Lo que el filtro de significado descartó, para que el cero sea auditable."""
    out = []
    for r in M["res"]:
        if r["c"]["capa"] != ATESTIGUADO:
            continue
        p = r["por"]["taíno"]
        if not p["exactas"] and p["n_cercanas"]:
            out.append({"caquetio": r["c"]["clave"], "glosa": r["c"]["sig"],
                        "entradas_taínas_con_glosa_cercana": p["n_cercanas"]})
    out.sort(key=lambda d: d["caquetio"])
    return out


ETNONIMOS = frozenset({"caquetio", "kaketio", "taino", "caribe", "karibna", "kalinago"})


def buscar_en_el_lexicon(forma, gu):
    """La forma tal cual, por `forma_fuente`, o por lema fonémico.

    Hace falta por D5: `cognados.yaml` escribe `quiva` y el lexicón lematizó a
    `kiba` con `forma_fuente: quiva`. Buscar sólo por la clave daría un «no
    está» falso, y un cero falso es peor que ninguno.
    """
    if forma in CL.VOCABULARIO_BASE:
        return forma, CL.VOCABULARIO_BASE[forma].get("fuente"), "clave directa"
    if forma in CL.FUERA_DEL_HABLA:
        return forma, CL.FUERA_DEL_HABLA[forma].get("fuente"), "⚠️ en FUERA_DEL_HABLA (archivada)"
    for k, v in CL.VOCABULARIO_BASE.items():
        if v.get("forma_fuente") and str(v["forma_fuente"]).lower() == forma.lower():
            return k, v.get("fuente"), f"por forma_fuente «{v['forma_fuente']}»"
    lema = fon(forma, "colonial", gu)
    if lema:
        for k, v in CL.VOCABULARIO_BASE.items():
            if fon(k, "colonial", gu) == lema:
                return k, v.get("fuente"), f"por lema fonémico «{lema}»"
    return None, None, "no está"


def bloque_cognados_ya_declarados(gu):
    """Los sets de `2-lengua/cognados.yaml` que ya emparejan caquetío con taíno.

    Es lo primero que había que mirar y no estaba mirado: el canon de datos de
    lengua YA tiene parejas CQ~TN. Aquí se auditan una a una, con las tres
    preguntas de la regla 8 y de la skill §8: ¿cita a alguien?, ¿la forma
    caquetía existe en el lexicón?, ¿no serán las dos la misma palabra
    castellana escrita dos veces?
    """
    Y = yaml.safe_load(io.open(YAML_COGNADOS, encoding="utf-8"))
    filas, resumen = [], collections.Counter()
    for c in Y["cognados"]:
        f = c.get("formas") or {}
        if "CQ" not in f or "TN" not in f:
            continue
        cq, tn = str(f["CQ"]), str(f["TN"])
        prim_tn = re.split(r"\s*/\s*", tn)[0].strip()
        a, b = fon(cq, "colonial", gu), fon(prim_tn, "colonial", gu)
        sim = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() if a and b else 0.0
        proc = c.get("procedencia") or {}
        clave_cq, capa_cq, como = buscar_en_el_lexicon(cq, gu)
        identicas = _norm_es(cq) == _norm_es(prim_tn) and bool(_norm_es(cq))
        etnonimo = _norm_es(cq) in {_norm_es(x) for x in ETNONIMOS} or \
                   _norm_es(prim_tn) in {_norm_es(x) for x in ETNONIMOS}
        lado_cq_no_es_caquetio = bool(capa_cq) and not str(capa_cq).startswith("caquetío")
        if proc.get("obra") and c.get("fuente") == "atestiguado":
            ver = "ATESTIGUADO CON CITA"
            porque = f"cita {proc['obra']} p. {proc.get('pagina')}"
        elif lado_cq_no_es_caquetio:
            ver = "EL LADO CAQUETÍO NO ES CAQUETÍO"
            porque = (f"la forma de la columna CQ está en el lexicón etiquetada `{capa_cq}`. "
                      "Un set que empareja una voz taína con otra voz taína no dice nada del "
                      "caquetío")
        elif etnonimo:
            ver = "CIRCULAR: es un etnónimo"
            porque = ("emparejar el nombre de un pueblo con el nombre de otro no es un cognado "
                      "léxico; y `taino` como autónimo ya lo desmiente Brinton p. impresa 14")
        elif identicas:
            ver = "NO ES UN COGNADO: la misma palabra escrita dos veces"
            porque = ("las dos formas son idénticas y el set no cita a nadie. Es el préstamo que el "
                      "castellano tomó del taíno y devolvió a todas partes: lo que prueba es que "
                      "nosotros escribimos la palabra igual en las dos columnas")
        elif not proc.get("obra"):
            ver = "SIN PROCEDENCIA"
            porque = ("regla 8: no hay clave foránea que citar. Se declara `deuda: sin-procedencia`; "
                      "el hueco se admite, callarlo no")
        else:
            ver = "CON CITA, capa reconstruida"
            porque = f"cita {proc['obra']}"
        resumen[ver] += 1
        filas.append({
            "id": c["id"], "glosa": c["glosa"], "cq": cq, "tn": tn,
            "similitud_fonemica": round(sim, 3),
            "capa_declarada": c.get("fuente"), "confianza": c.get("confianza"),
            "procedencia": (f"{proc.get('obra')} p. {proc.get('pagina')}" if proc.get("obra")
                            else None),
            "forma_caquetia_en_el_lexicon": (f"{clave_cq} · {capa_cq} ({como})" if clave_cq
                                             else "NO ESTÁ"),
            "veredicto": ver, "por_que": porque,
        })
    filas.sort(key=lambda d: (d["veredicto"], d["id"]))
    return {
        "que_es": ("los sets de 2-lengua/cognados.yaml que ya emparejan una forma CQ con una TN. "
                   "Existían antes de esta campaña y nadie los había auditado como grupo."),
        "sets_con_CQ_y_TN": len(filas),
        "reparto": dict(sorted(resumen.items())),
        "formas_caquetias_que_no_estan_en_el_lexicon": sorted(
            d["cq"] for d in filas if d["forma_caquetia_en_el_lexicon"] == "NO ESTÁ"),
        "filas": filas,
    }


def bloque_hallazgos_de_etiqueta(gu):
    """Formas taínas que el repo tiene pero NO bajo la etiqueta `taíno`.

    El cero del cruce por glosa no mide las dos lenguas: mide las dos listas.
    Esto cuenta cuánto de ese cero es un problema de etiqueta.
    """
    import json
    hip = json.load(io.open(JSON_TAINO_HIP, encoding="utf-8"))
    declaradas = {k: v for k, v in hip.items()
                  if str(v.get("notas", "")).startswith("Taíno atestiguado")}
    fuera = []
    for k, v in sorted(declaradas.items()):
        ent = CL.VOCABULARIO_BASE.get(k)
        fuente = ent.get("fuente") if ent else None
        if fuente == "taíno":
            continue
        fuera.append({"forma": k, "glosa_en_el_json": v.get("es"),
                      "etiqueta_en_el_lexicon": fuente or "no está en VOCABULARIO_BASE",
                      "lo_que_dice_el_json": str(v.get("notas"))[:120]})
    # ¿hay una voz caquetía atestiguada con la misma glosa normalizada?
    por_glosa = collections.defaultdict(list)
    for k, v in CL.VOCABULARIO_BASE.items():
        if v.get("fuente") != ATESTIGUADO:
            continue
        for cab, ex, _ in conceptos(v.get("sig")):
            if ex:
                por_glosa[cab].append(k)
    for d in fuera:
        for cab, ex, _ in conceptos(d["glosa_en_el_json"]):
            if ex and por_glosa.get(cab):
                cqs = por_glosa[cab]
                a = fon(d["forma"], "colonial", gu)
                mejor_cq, mejor_s = None, 0.0
                for cq in cqs:
                    b = fon(cq, "colonial", gu)
                    s = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
                    if s > mejor_s:
                        mejor_cq, mejor_s = cq, s
                d["pareja_caquetia_que_el_cruce_se_pierde"] = {
                    "caquetio": mejor_cq, "concepto": cab, "similitud": round(mejor_s, 3)}
    return {
        "que_es": ("curiana_sim/taino_hipotetico.json declara 14 formas «Taíno atestiguado». "
                   "Esto mira cuántas de ellas NO llevan la etiqueta `taíno` en el lexicón, y si "
                   "alguna tenía pareja caquetía que el cruce por glosa se pierde por eso."),
        "declaradas_atestiguadas_en_el_json": len(declaradas),
        "de_esas_sin_la_etiqueta_taino_en_el_lexicon": len(fuera),
        "casos": fuera,
        "lo_que_falta_del_todo": {
            "que_es": ("voces taínas que las propias fuentes del repo imprimen, que tienen pareja "
                       "caquetía atestiguada declarada en cognados.yaml, y que NO están en el "
                       "lexicón bajo ninguna etiqueta. Se listan como propuesta para T1/T2; este "
                       "script no las añade (regla 5)."),
            "casos": [
                {"taino": "bagua / bara-wa 'mar'",
                 "donde_esta_en_el_repo": ("2-lengua/cognados.yaml cognado-016 (con cita: "
                                           "oliver-1989-cap2 p. 150) y cognado-019; "
                                           "brinton-1871 p. impresa 11 s.v. Bagua «the sea»"),
                 "pareja_caquetia": "para / parawa 'mar', caquetío-atestiguado",
                 "por_que_importa": ("es la pareja CQ~TN mejor citada que hay, y el lexicón no tiene "
                                     "ninguna entrada taína para 'mar': por eso el cruce por glosa "
                                     "no la ve")},
                {"taino": "siba 'piedra'",
                 "donde_esta_en_el_repo": ("el lexicón la tiene, pero etiquetada `lokono`; "
                                           "taino_hipotetico.json la declara «Taíno atestiguado»; "
                                           "brinton-1871 p. impresa 14 «Siba, a stone»"),
                 "pareja_caquetia": "kiba 'piedra' (forma_fuente `quiva`), caquetío-atestiguado",
                 "por_que_importa": ("el cruce la puntúa 0,75 contra el LOKONO y 0 contra el taíno, "
                                     "y es la misma forma. Es el ejemplo más claro de que el cero "
                                     "mide la etiqueta y no la lengua")},
            ],
        },
    }


def paso_por_forma(M, gu):
    """Cruce por ESQUELETO FONÉMICO, sin filtro de significado.

    El encargo lo pide y hay que hacerlo, pero existe sobre todo para poder
    DESCARTARLO con número: medido el 2026-09-10 sobre el achagua, 7 de 11
    «aciertos» de forma se caen al mirar la glosa. Aquí el listón sube a
    0,75 y se exigen 4 fonemas, y cada pareja dice si las glosas coinciden.
    """
    caq = [r["c"] for r in M["res"] if r["c"]["capa"] == ATESTIGUADO
           and r["c"]["cands"] and len(r["c"]["cands"][0][0]) >= MIN_FONEMAS_FORMA]
    cab_caq = {c["clave"]: {x for x, ex, _ in c["conceptos"] if ex} for c in caq}
    out, por_lengua = [], {}
    for L in TODAS:
        pool = [e for e in M["lengs"][L] if len(e.get("fon_base") or "") >= MIN_FONEMAS_FORMA]
        hits, con_glosa = [], 0
        for c in caq:
            a = c["cands"][0][0]
            sm = difflib.SequenceMatcher(None, autojunk=False)
            sm.set_seq2(a)
            mejor_s, empatadas = 0.0, []
            for e in pool:
                sm.set_seq1(e["fon_base"])
                s = sm.ratio()
                if s > mejor_s + 1e-9:
                    mejor_s, empatadas = s, [e]
                elif abs(s - mejor_s) <= 1e-9:
                    empatadas.append(e)
            # Desempate POR GLOSA, y es importante: el lokono tiene `catti`
            # 'mes' y `kathi` 'luna' con la misma forma fonemizada, y quedarse
            # con la primera daría «las glosas no coinciden» sobre un empate.
            mejor_e = next((e for e in empatadas
                            if cab_caq[c["clave"]] & {x for x, ex, _ in e["conceptos"] if ex}),
                           empatadas[0] if empatadas else None)
            if mejor_s >= UMBRAL_FORMA and mejor_e is not None:
                cab_e = {x for x, ex, _ in mejor_e["conceptos"] if ex}
                coincide = bool(cab_caq[c["clave"]] & cab_e)
                con_glosa += int(coincide)
                hits.append({"lengua": L, "caquetio": c["clave"], "glosa_caquetia": c["sig"],
                             "comparanda": mejor_e["forma"], "glosa_comparanda": mejor_e["glosa"],
                             "similitud": round(mejor_s, 3),
                             "las_glosas_coinciden": coincide})
        por_lengua[L] = {"formas_caquetias_probadas": len(caq), "entradas_de_la_lengua": len(pool),
                         "parejas_de_forma_ge_umbral": len(hits),
                         "de_esas_con_la_glosa_tambien": con_glosa,
                         "ruido": len(hits) - con_glosa}
        if L in ("taíno", CONTROL):
            out.extend(hits)
    out.sort(key=lambda d: (d["lengua"], -d["similitud"]))
    return {
        "diseño": (f"cada forma caquetía atestiguada de {MIN_FONEMAS_FORMA}+ fonemas contra todas "
                   f"las de cada lengua; se listan las de similitud >= {UMBRAL_FORMA}. La columna "
                   "`de_esas_con_la_glosa_tambien` es la que importa: lo demás es ruido, y el "
                   "número dice cuánto."),
        "por_lengua": por_lengua,
        "parejas_taino_y_control": out,
    }


# ═════════════════════════════════════════════════════════════════════════
# T11 · EL TEST: ¿cognado heredado (A), préstamo (B) o indecidible (C)?
# ═════════════════════════════════════════════════════════════════════════
def esqueleto(f):
    """Las consonantes de una forma ya fonemizada. C9: las vocales quedan fuera."""
    return "".join(ch for ch in str(f or "") if ch in CONSONANTES)


def diferencias_consonanticas(a, b):
    """[(consonante caquetía, consonante taína o ∅)] alineando los esqueletos."""
    m = alinear(a, b)
    out = []
    for i, x in enumerate(a):
        y = m.get(i, "∅")
        out.append((x, "" if y == "∅" else y))
    # lo que el taíno TIENE de más también es diferencia
    usados = {m.get(i) for i in range(len(a))}
    sobra = len(b) - len([u for u in usados if u and u != "∅"])
    return out, max(0, sobra)


def juzgar_por_correspondencias(fa, fb, tabla="caquetío↔taíno"):
    """El corazón del test. Devuelve el diagnóstico consonante a consonante."""
    mapa = TABLAS[tabla]["mapa"]
    ca, cb = esqueleto(fa), esqueleto(fb)
    pares, sobra = diferencias_consonanticas(ca, cb)
    identicas, regulares, neutras, violaciones, persona, candidatas = [], [], [], [], [], []
    for i, (x, y) in enumerate(pares):
        et = f"{x} ~ {y or '∅'}"
        d = mapa.get(x)
        if x == y:
            identicas.append(et)
        elif (x, y) in PARES_NEUTROS:
            neutras.append(et + " (C8: /r/~/l/ indecidible)")
        elif d and y in d["admite"]:
            regulares.append(f"{et} ({d['apoyos']} apoyos)")
        elif d and y in d["candidatas"]:
            candidatas.append(f"{et} — sólo {d['apoyos']} apoyos, por debajo del listón de "
                              f"{LISTON_DE_APOYOS} del propio proyecto")
        elif not d and x == y:
            identicas.append(et)
        elif i == 0 and x in PREFIJOS_DE_PERSONA and y in PREFIJOS_DE_PERSONA:
            persona.append(f"{et} — no es sonido, es MORFOLOGÍA: {PREFIJOS_DE_PERSONA[x]} frente a "
                           f"{PREFIJOS_DE_PERSONA[y]} (oliver-1989-cap2 p. 147)")
        else:
            violaciones.append(et)
    diagn = {c for c, d in mapa.items() if d["diagnostica"]}
    return {"tabla": tabla, "esqueleto_caquetio": ca, "esqueleto_taino": cb,
            "identicas": identicas, "regulares_predichas": regulares,
            "candidatas_bajo_el_liston": candidatas,
            "neutras": neutras, "violaciones": violaciones,
            "contraste_de_persona": persona,
            "consonantes_taínas_sin_pareja": sobra,
            "consonantes_diagnosticas_presentes": sorted({x for x, _ in pares} & diagn)}


def test_cognado_o_prestamo(fa, fb, dominio=None, p_nulo=None, campo_de_rango=False,
                            tabla="caquetío↔taíno"):
    """A cognado heredado · B préstamo o cruce reciente · C indecidible.

    El orden importa y está declarado: primero lo que descalifica la pareja
    (forma corta, azar), después la FORMA —que es lo único que distingue
    herencia de préstamo—, y sólo al final el dominio, que pondera pero nunca
    decide solo. «Lo que decide no es SI se comparte, sino QUÉ» vale para la
    clase de la pareja; para el mecanismo, manda el sonido.
    """
    j = juzgar_por_correspondencias(fa, fb, tabla)
    ca, cb = j["esqueleto_caquetio"], j["esqueleto_taino"]
    razones = []
    if len(ca) < 2 or len(cb) < 2:
        return "C", "esqueleto de menos de dos consonantes: no hay dónde medir", j
    if p_nulo is not None and p_nulo > 0.10:
        return "C", (f"el modelo nulo alcanza este parecido en el {p_nulo:.0%} de las réplicas: "
                     "antes de preguntarse cómo llegó la palabra hay que descartar que no haya "
                     "llegado"), j
    if j["contraste_de_persona"] and not j["violaciones"]:
        razones.append("la diferencia inicial es de PERSONA y no de sonido (" +
                       "; ".join(j["contraste_de_persona"]) + ")")
    if j["violaciones"]:
        return "B", ("VIOLA las correspondencias predichas en " + ", ".join(j["violaciones"])
                     + ". Una voz heredada no puede traer sonidos que la cadena caquetío↔lokono↔"
                       "taíno no produce; o cruzó por otra vía, o no es la misma palabra"), j
    if j["contraste_de_persona"]:
        resto_a = ca[1:]
        resto_b = cb[1:]
        if resto_a == resto_b:
            return "C", ("; ".join(razones) + ". Quitado el prefijo, las dos raíces son IDÉNTICAS "
                         f"(/{resto_a}/) y no traen ninguna consonante diagnóstica: la palabra no "
                         "tiene dónde diferir, así que ni la herencia ni el préstamo dejan huella"), j
        return "C", "; ".join(razones) + ". Lo que queda tras el prefijo no basta para decidir", j
    if ca == cb:
        if j["consonantes_diagnosticas_presentes"]:
            return "B", ("CERO diferencia consonántica, y el esqueleto contiene "
                         + ", ".join(f"/{c}/" for c in j["consonantes_diagnosticas_presentes"])
                         + ", donde lo ESPERADO no era la identidad (P1). Si tenía que cambiar y no "
                           "cambió, la palabra cruzó tarde: es la firma del préstamo, no de la "
                           "herencia"), j
        return "C", ("CERO diferencia, pero el esqueleto NO tiene ninguna consonante diagnóstica: "
                     "para todas las que hay (" + ", ".join(f"/{c}/" for c in sorted(set(ca)))
                     + ") lo predicho ES la identidad. La palabra no tiene dónde diferir, así que "
                       "ni la herencia ni el préstamo dejan huella. Ni A ni B: hace falta otro dato"), j
    if j["regulares_predichas"]:
        razones.append("cumple " + ", ".join(j["regulares_predichas"]))
        if campo_de_rango or dominio == "viajero":
            return "A", ("; ".join(razones) + ". ⚠️ pero el campo es de los que viajan (rango, "
                         "alianza, comercio): la forma dice herencia y el campo no la confirma — "
                         "un préstamo TEMPRANO también habría sufrido los cambios posteriores"), j
        return "A", "; ".join(razones) + ": es lo que la transitividad predice para una voz heredada", j
    if j["candidatas_bajo_el_liston"]:
        return "C", ("la diferencia la cubriría " + "; ".join(j["candidatas_bajo_el_liston"])
                     + ". Con menos de tres apoyos eso no es una regla, y usarla para decidir esta "
                       "misma pareja sería circular: queda abierta, y lo que la cerraría es un "
                       "tercer apoyo independiente"), j
    if j["neutras"]:
        return "C", ("la única diferencia es " + ", ".join(j["neutras"])
                     + ", y Oliver declara ese contraste indecidible en todo el corpus (C8)"), j
    return "C", ("hay diferencia pero ninguna correspondencia predicha la cubre ni la prohíbe "
                 f"({j['consonantes_taínas_sin_pareja']} consonante(s) taína(s) sin pareja): "
                 "la pareja queda abierta"), j


def bloque_las_predicciones():
    return {
        "por_que_van_aquí_y_no_al_final": (
            "están escritas ANTES de mirar ninguna pareja, y el orden es parte del método: una "
            "correspondencia inventada después de ver el resultado explica todo y no predice nada. "
            "Viven en el código, en `CORRESPONDENCIAS_PREDICHAS`, por encima de cualquier función "
            "que toque un par."),
        "de_donde_salen": (
            "NADIE ha publicado correspondencias caquetío↔taíno, y este proyecto no puede "
            "establecerlas con cuatro parejas. Lo que se hace es COMPONER las dos patas que sí "
            "existen: caquetío↔lokono (oliver-1989-cap2, C1-C13, con página) y taíno↔lokono "
            "(brinton-1871 pp. 11-14, recogidas por T2 en taino_brinton_1871.yaml "
            "§correspondencias_para_T4). Componer da una PREDICCIÓN, no un hecho."),
        "los_tres_limites_declarados": [
            "C8 — /r/ ~ /l/ es indecidible en todo el corpus (Oliver): una diferencia r/l no cuenta.",
            "C9 — Oliver EXCLUYE las vocales por falta de transcripción fiable: el test puntúa "
            "esqueletos consonánticos, no formas enteras.",
            "⟨gu⟩ = /w/ (Oliver p. 147, «/wa- [gua-]/»): el test corre sobre la fonemización con "
            "gu_es_w=True, que es la que hace ⟨bagua⟩ = /bawa/ y deja ver la correspondencia P1. "
            "El resto del cruce sigue corriendo con el defecto, gu_es_w=False.",
        ],
        "tabla": CORRESPONDENCIAS_PREDICHAS,
        "tablas_ejecutables": {
            nombre: {"de_donde": T["de_donde"],
                     "mapa": {c: {"admite": sorted(d["admite"] or [""]),
                                  "candidatas": sorted(d["candidatas"]),
                                  "apoyos": d["apoyos"], "diagnostica": d["diagnostica"]}
                              for c, d in sorted(T["mapa"].items())}}
            for nombre, T in TABLAS.items()},
        "liston_de_apoyos": LISTON_DE_APOYOS,
        "que_significa_diagnostica": (
            "que lo PREDICHO para esa consonante no es la identidad. Sólo entonces un «cero "
            "diferencia» se puede leer como préstamo: si tenía que cambiar y no cambió, cruzó "
            "tarde. Una pareja sin ninguna consonante diagnóstica no se puede decidir por la "
            "forma, por mucho que se parezca: no tiene dónde diferir. Ése es el caso de `-tiao`, "
            "y por eso el test devuelve C y no A. **Entre caquetío y taíno sólo /r/ es "
            "diagnóstica; entre caquetío y lokono, ninguna.**"),
        "que_significa_candidata": (
            "que la cadena la sugiere pero tiene menos de tres apoyos, que es el listón del propio "
            "proyecto («una correspondencia que sale una o dos veces no es nada»). Usarla no da un "
            "cognado: baja el veredicto a C y el YAML dice qué lo cerraría."),
    }


def medir_tasa_de_erre(M):
    """P1 puesta a prueba sobre el corpus entero, no sobre un par.

    Si el taíno pierde la /r/ que el caquetío conserva, tiene que verse en la
    proporción de /r/ sobre todas las consonantes de cada lista.
    """
    out = {}
    listas = {L: [e["fon_base"] for e in M["lengs"][L] if e.get("fon_base")] for L in TODAS}
    listas["caquetío-atestiguado"] = [r["c"]["cands"][0][0] for r in M["res"]
                                      if r["c"]["capa"] == ATESTIGUADO and r["c"]["cands"]]
    for L, formas in listas.items():
        cons = collections.Counter()
        for f in formas:
            for ch in esqueleto(f):
                cons[ch] += 1
        tot = sum(cons.values())
        out[L] = {"formas": len(formas), "consonantes": tot,
                  "r": cons.get("r", 0),
                  "tasa_de_r": round(cons.get("r", 0) / tot, 4) if tot else None,
                  "l": cons.get("l", 0),
                  "tasa_de_r_mas_l": round((cons.get("r", 0) + cons.get("l", 0)) / tot, 4) if tot else None,
                  "w": cons.get("w", 0),
                  "tasa_de_w": round(cons.get("w", 0) / tot, 4) if tot else None}
    return {
        "que_mide": ("P1 dice que el taíno pierde o glidea la /r/ que el caquetío conserva. Si es "
                     "verdad, tiene que verse SIN mirar ninguna pareja: en la proporción de /r/ "
                     "sobre el total de consonantes de cada lista."),
        "como_leerlo": ("es una prueba de la predicción, no una prueba de parentesco. Y arrastra el "
                        "sesgo de las listas: la caquetía es fitonimia de Zavala y la taína es "
                        "vocabulario de crónica. Una diferencia pequeña no dice nada; una diferencia "
                        "de varias veces, con el control jirajarano en medio, sí."),
        "por_lista": out,
    }


def bloque_control_del_test(M, gu):
    """Obligatorio: el test sobre lo que YA sabemos, heredado y prestado.

    Si no clasifica bien lo conocido, no sirve para lo desconocido. Se emiten
    los aciertos, los fallos y el veredicto — y el veredicto es del TEST, no
    de las parejas.
    """
    Y = yaml.safe_load(io.open(YAML_COGNADOS, encoding="utf-8"))

    # ── (a) HEREDADAS: caquetío ↔ lokono con cita ──────────────────────
    heredadas = []
    for c in Y["cognados"]:
        f = c.get("formas") or {}
        proc = c.get("procedencia") or {}
        if "CQ" not in f or "LK" not in f or not proc.get("obra") or c.get("fuente") != "atestiguado":
            continue
        cq = re.split(r"\s*/\s*", str(f["CQ"]))[0].strip().lstrip("*")
        lk = re.split(r"\s*/\s*", str(f["LK"]))[0].strip().lstrip("*")
        a, b = fon(cq, "colonial", gu), fon(lk.replace("-", ""), "colonial", gu)
        letra, porque, j = test_cognado_o_prestamo(a, b, tabla="caquetío↔lokono")
        heredadas.append({"set": c["id"], "glosa": c["glosa"], "cq": cq, "lk": lk,
                          "cita": f"{proc['obra']} p. {proc.get('pagina')}",
                          "comparado": f"{a} ~ {b}", "esqueletos": f"{j['esqueleto_caquetio']} ~ {j['esqueleto_taino']}",
                          "letra": letra, "por_que": porque,
                          "acierta": letra != "B"})

    # ── (b) PRESTADAS: taíno → castellano, que nadie discute ───────────
    prestadas = []
    for tn, es, cita in PRESTAMOS_CONOCIDOS:
        a, b = fon(es, "colonial", gu), fon(tn, "colonial", gu)
        letra, porque, j = test_cognado_o_prestamo(a, b)
        prestadas.append({"taino": tn, "castellano": es, "cita": cita,
                          "comparado": f"{a} ~ {b}",
                          "esqueletos": f"{j['esqueleto_caquetio']} ~ {j['esqueleto_taino']}",
                          "letra": letra, "por_que": porque,
                          "acierta": letra != "A"})

    # ── (c) NO PARIENTE: caquetío ↔ jirajarano, el control de siempre ──
    nopariente = []
    for r in M["res"]:
        if r["c"]["capa"] != ATESTIGUADO or not r["por"][CONTROL]["ranking"]:
            continue
        s, e, cb, ca = r["por"][CONTROL]["ranking"][0]
        a2, b2 = fon(ca[1], "colonial", gu), fon(cb[1], "colonial", gu)
        letra, porque, _j = test_cognado_o_prestamo(a2, b2)
        nopariente.append({"caquetio": r["c"]["clave"], "jirajarano": cb[1],
                           "glosa": r["c"]["sig"], "similitud": round(s, 3),
                           "letra": letra, "por_que": porque[:140], "acierta": letra != "A"})
    nopariente.sort(key=lambda d: (-d["similitud"], d["caquetio"]))

    def _cuenta(filas):
        c = collections.Counter(x["letra"] for x in filas)
        return {"n": len(filas), "reparto": dict(sorted(c.items())),
                "aciertos": sum(1 for x in filas if x["acierta"]),
                "fallos": sum(1 for x in filas if not x["acierta"])}

    ch, cp, cn = _cuenta(heredadas), _cuenta(prestadas), _cuenta(nopariente)
    sirve = ch["fallos"] == 0 and cp["fallos"] == 0 and cn["fallos"] == 0
    decididas_h = sum(1 for x in heredadas if x["letra"] == "A")
    decididas_p = sum(1 for x in prestadas if x["letra"] == "B")
    return {
        "por_que_es_obligatorio": (
            "«si el test no separa lo que ya sabemos, no sirve para lo que no sabemos». Tres "
            "brazos: parejas que sabemos HEREDADAS (caquetío↔lokono con cita de Oliver), parejas "
            "que sabemos PRESTADAS (taíno→castellano, que el propio Brinton documenta) y un brazo "
            "de lengua NO pariente (jirajara/ayomán de Jahn 1927)."),
        "el_criterio_de_acierto": (
            "el test es SANO si nunca llama préstamo a una heredada ni herencia a una prestada. Es "
            "INCOMPLETO en la medida en que devuelve C, y eso no es un fallo: es la parte del "
            "material que no tiene consonante diagnóstica. Las dos cifras se dan por separado."),
        "a_heredadas_caquetio_lokono": {"resumen": ch, "decididas_como_A": decididas_h,
                                        "filas": heredadas},
        "b_prestadas_taino_castellano": {"resumen": cp, "decididas_como_B": decididas_p,
                                         "filas": prestadas},
        "c_no_pariente_caquetio_jirajarano": {"resumen": cn, "filas": nopariente[:20]},
        "veredicto_del_test": (
            ("SANO: ninguna heredada sale préstamo, ninguna prestada sale herencia y ninguna pareja "
             "con la lengua no pariente sale herencia. "
             if sirve else
             "🔴 NO SANO: el test clasifica mal algo que ya sabíamos; lo que diga sobre lo "
             "desconocido no vale. Ver los `fallos` de cada brazo. ")
            + f"Poder resolutivo: decide {decididas_h} de {ch['n']} heredadas y {decididas_p} de "
              f"{cp['n']} prestadas; el resto queda en C por falta de consonante diagnóstica."),
    }


# ═════════════════════════════════════════════════════════════════════════
# T11 · El caso de prueba: `datihao`, y la pregunta de `diao`
# ═════════════════════════════════════════════════════════════════════════
def _atestaciones_de_tiao(gu):
    """Todo lo que el repo tiene de la familia -tiao, con quién lo dice."""
    filas = []
    for k in ("datihao", "waitiao", "diao", "boratio", "dato", "dare"):
        v = CL.VOCABULARIO_BASE.get(k)
        if not v:
            continue
        filas.append({"lado": "caquetío (lexicón)", "forma": k,
                      "forma_fuente": v.get("forma_fuente"), "glosa": v.get("sig"),
                      "capa": v.get("fuente"),
                      "fonemizada": fon(v.get("forma_fuente") or k, "colonial", gu),
                      "quien_lo_dice": (v.get("notas") or "")[:180]})
    Y = yaml.safe_load(io.open(YAML_COGNADOS, encoding="utf-8"))
    for c in Y["cognados"]:
        if c["id"] not in ("cognado-008", "cognado-009", "cognado-012"):
            continue
        proc = c.get("procedencia") or {}
        filas.append({"lado": "cognados.yaml", "forma": str((c.get("formas") or {}).get("CQ")),
                      "glosa": c["glosa"], "capa": c.get("fuente"),
                      "formas_del_set": c.get("formas"),
                      "quien_lo_dice": f"{proc.get('obra')} p. {proc.get('pagina')} · «{proc.get('ancla')}»",
                      "duda_del_autor": (c.get("duda_del_autor") or "")[:300]})
    O = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "taino_oviedo_valdes_1851.yaml"),
                               encoding="utf-8"))
    for e in O.get("otras_islas", []):
        if "lihao" in str(e.get("forma_fuente", "")) or "tihao" in str(e.get("forma_fuente", "")):
            filas.append({"lado": "taíno (transcripción de T1)", "forma": e.get("forma_fuente"),
                          "forma_probable": e.get("forma_probable"),
                          "glosa": str(e.get("glosa_fuente"))[:140],
                          "fonemizada": fon(str(e.get("forma_fuente")), "colonial", gu),
                          "pagina_impresa": e.get("pagina_impresa"),
                          "atribucion": str(e.get("atribucion"))[:160],
                          "verificacion": e.get("verificacion"),
                          "quien_lo_dice": "oviedo-y-valdes-1851 lib. XVI cap. V"})
    B = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "taino_brinton_1871.yaml"),
                               encoding="utf-8"))
    for e in B["vocabulario_antillano"]["entradas"]:
        if "tiao" in str(e.get("forma", "")).lower():
            filas.append({"lado": "taíno (transcripción de T2)", "forma": e.get("forma"),
                          "glosa": e.get("glosa"), "lokono_de_brinton": e.get("lokono"),
                          "fonemizada": fon(str(e.get("forma")), "colonial", gu),
                          "pagina_impresa": e.get("pagina"),
                          "quien_lo_dice": f"brinton-1871 p. {e.get('pagina')}, cronista: {e.get('cronista')}"})
    return filas


def bloque_datihao(gu):
    """El caso de prueba, con el test aplicado y el test PENDIENTE escrito."""
    cq_da = fon("datihao", "colonial", gu)          # la del lexicón
    cq_wa = fon("guaitiao", "colonial", gu)         # forma_fuente de `waitiao`
    tn_gua = fon("guatiao", "colonial", gu)         # Brinton p. 12
    ov = fon("dalihao", "colonial", gu)             # lo que el OCR de Oviedo da

    pruebas = []
    for et, a, b in (
        ("caq `datihao` (da-) ~ taí `guatiao` (gua-)", cq_da, tn_gua),
        ("caq `guaitiao` (= la forma_fuente de `waitiao`) ~ taí `guatiao`", cq_wa, tn_gua),
    ):
        letra, porque, j = test_cognado_o_prestamo(a, b, campo_de_rango=True)
        pruebas.append({"pareja": et, "comparado": f"{a} ~ {b}",
                        "esqueletos": f"{j['esqueleto_caquetio']} ~ {j['esqueleto_taino']}",
                        "diagnostico": j, "letra": letra, "por_que": porque})
    pruebas.append({
        "pareja": "caq `datihao` ~ lo que el OCR de Oviedo imprime en San Juan (`dalihao`)",
        "comparado": f"{cq_da} ~ {ov}",
        "esqueletos": f"{esqueleto(cq_da)} ~ {esqueleto(ov)}",
        "letra": "NO SE APLICA EL TEST",
        "por_que": ("la diferencia es /t/ ~ /l/ y **no es un dato de lengua**: es la confusión l/t "
                    "del OCR, en cursiva, en una página sin imagen (impresa 473 > 154, el límite que "
                    "declara la propia transcripción). Meterla en el test daría «viola las "
                    "correspondencias» y estaría midiendo al escáner. Se deja fuera y se dice."),
    })
    return {
        "la_pregunta_de_miguel": (
            "«datihao está atestiguada a las DOS orillas por Oviedo». Si las dos formas son "
            "idénticas letra a letra, eso es lo que escribiría un cronista que oye la misma palabra "
            "en dos sitios — o lo que escribiría uno que la conoce de Haití y la proyecta sobre "
            "Venezuela. Si difieren, la diferencia decide: regular → cognado; irregular → préstamo."),
        "lo_primero_y_es_lo_que_rompe_el_caso": {
            "que_se_esperaba": "dos atestaciones de Oviedo, una de San Juan y otra de la Provincia de Venezuela",
            "lo_que_el_repo_tiene": (
                "UNA. El barrido del tomo I entero (3.001.703 caracteres, pymupdf en modo "
                "reparación) da **una sola** ocurrencia de la familia -tiao: `dalihao`, impresa "
                "473, en boca del cacique Agueybana de San Juan. `tiao`, `guatiao`, `guaitiao`, "
                "`diao` y `borat*` dan CERO en el volumen."),
            "y_la_otra_orilla": (
                "no está en el repo. La atestación «de la Provincia de Venezuela» se conoce sólo "
                "por oliver-1989-cap2 n. 42 p. 146, que la parafrasea; Jahn 1927 p. 213 n. 29 la "
                "hacía venir de «el apéndice al tomo IV» de Oviedo, apéndice que el rastreo del "
                "2026-08-14 verificó que NO EXISTE. Y `fuentes_caquetios/"
                "Oviedo_Banhos_Conquista_Poblacion_Venezuela.pdf`, que por el nombre parecía "
                "candidato, es de OTRO autor —José de Oviedo y Baños, 1723— y da cero en las "
                "seis grafías (barrido de 1.195.750 caracteres, 2026-09-22)."),
            "consecuencia": (
                "la comparación letra a letra que el encargo pide **no se puede hacer hoy**: no hay "
                "dos cadenas que comparar, hay una. Y esa una es lectura de OCR sin imagen "
                "(impresa 473 > 154), con la confusión l/t del propio OCR en el sitio exacto donde "
                "está la duda: `dalihao` frente a `datihao`."),
            "y_hay_un_tercer_problema_de_fondo": (
                "los DOS lados caquetíos de la familia -tiao —`datihao` y `waitiao`— citan lo mismo: "
                "oliver-1989-cap2 p. 147 sobre Oviedo y Valdés. No son dos atestaciones, son una "
                "obra leída por un autor. La skill §8 es exactamente esto: Jahn parecía corroborar "
                "y bebe del mismo Oviedo."),
        },
        "lo_que_el_repo_tiene_de_la_familia": _atestaciones_de_tiao(gu),
        "el_test_aplicado_a_lo_que_hay": pruebas,
        "la_respuesta_de_la_transitividad": (
            "P3 predice que un cognado caquetío de taíno `da-` + `-(i)tiao` se dice **`da-tiao`**: "
            "el caquetío conserva /d-/ igual que el lokono y el taíno (Oliver pp. 136, 146-147). Y "
            "eso es exactamente lo que se ve. **Pero el rasgo no decide nada**: /d-/ separa al trío "
            "caquetío-taíno-lokono del par guajiro-paraujano (/t-/), no al caquetío del taíno. Un "
            "préstamo taíno al caquetío habría entrado con su /d-/ intacto. En la raíz `-tiao` no "
            "hay ninguna consonante diagnóstica: /t/ está predicha idéntica en los dos lados (P4) y "
            "no hay /r/, /b/ ni /p/. La palabra **no tiene dónde diferir**."),
        "las_dos_lecturas_con_su_peso": [
            {"letra": "A — cognado heredado",
             "a_favor": ("Oliver lo escribe: «This Taíno term is cognate to Caquetio daitiao» "
                         "(p. 147), y le da etimología en proto-arahuaco: /da-/ 1ª sg. + /-(i)tiao/ "
                         "sobre la raíz de parentesco /atti/, con el lokono `da-tti`/`da-iti` y "
                         "Brinton dando el lokono `ahati` 'companion, playmate' (p. 12). La raíz de "
                         "parentesco es vocabulario de FILIACIÓN, del que casi nunca viaja."),
             "en_contra": ("la forma no exhibe ni una diferencia, y no puede exhibirla: sin "
                           "consonante diagnóstica el argumento formal está vacío. Y la raíz "
                           "/-atti-/ aparece en caquetío en `boratio`, `dato` y `datihao` — o sea "
                           "que su presencia en la lengua no depende de esta voz."),
             "peso": "media — la etimología es buena y la evidencia formal es nula"},
            {"letra": "B — préstamo por contacto",
             "a_favor": ("el campo. `guatiao` no es una palabra de parentesco cualquiera: es el "
                         "nombre de una INSTITUCIÓN de alianza entre señores —el trueque de "
                         "nombres entre Ponce de León y Agüeybaná, Las Casas [1552] 1929 II:291— y "
                         "las instituciones de alianza viajan con los aliados. Oviedo la oye en "
                         "boca de un cacique de Boriquén hablando con españoles, en 1510 y pico. Y "
                         "Oliver DUDA él mismo: «I have no absolute certainty that it belongs to a "
                         "Caquetío language… He could very well have used Taíno», y concluye "
                         "«equally shared by both Taíno and Caquetío» (n. 42, p. 146)."),
             "en_contra": ("«compartida por las dos» no es lo mismo que «prestada»: puede ser "
                           "herencia común que las dos conservaron. Y la etimología de Oliver la "
                           "hace descender del proto-arahuaco, no cruzar el mar."),
             "peso": "media-alta — el campo empuja y el autor de la afirmación duda de su propio dato"},
            {"letra": "C — indecidible con lo que hay",
             "a_favor": ("es lo que el test devuelve, y lo devuelve por una razón concreta y no por "
                         "prudencia: la palabra no tiene consonante diagnóstica. Además falta la "
                         "mitad del dato (la otra orilla) y la mitad que hay es OCR sin imagen."),
             "en_contra": "—",
             "peso": "ALTA — es el veredicto del instrumento"},
        ],
        "el_test_que_queda_escrito_para_cuando_llegue_el_dato": {
            "como_usarlo": ("cuando otro agente traiga la forma del tomo II/IV (o una segunda copia "
                            "de la impresa 473 con imagen), se mete en `GLOSA_DECLARADA` / en la "
                            "transcripción y se re-corre el script. Esta tabla dice de antemano qué "
                            "significa cada resultado, para que no se decida después de verlo."),
            "filas": [
                {"si_la_forma_de_venezuela_es": "idéntica letra a letra a la de San Juan (`datihao` = `datihao`)",
                 "entonces": "B se refuerza mucho",
                 "por_que": ("un cronista con veinte años en La Española escribiendo la MISMA cadena "
                             "en dos orillas es, como poco, indistinguible de un cronista que "
                             "proyecta. Y es justo el escenario que Oliver teme en la n. 42")},
                {"si_la_forma_de_venezuela_es": "`datihao` frente a un taíno `guatiao` — o sea, difiere sólo en el prefijo de persona",
                 "entonces": "sigue siendo C",
                 "por_que": ("es lo que ya tenemos: /da-/ 1ª sg. contra /wa-/ 3ª pl. es MORFOLOGÍA "
                             "compartida, no correspondencia de sonido. Prueba que las dos lenguas "
                             "tienen el mismo juego de prefijos, que es dato de filiación y ya está "
                             "contado en D11")},
                {"si_la_forma_de_venezuela_es": "con /r/ donde el taíno no la tiene (p. ej. *`daritiao`, *`darihao`)",
                 "entonces": "A, y fuerte",
                 "por_que": "sería P1 cumpliéndose en la voz misma: la correspondencia diagnóstica por fin presente"},
                {"si_la_forma_de_venezuela_es": "con /t-/ inicial (*`tatihao`)",
                 "entonces": "A por vía guajiro-paraujana, y falsaría P3",
                 "por_que": "el /tA-/ es la innovación guajiro-paraujana; sería dato contra la tesis lokonoide de Oliver"},
                {"si_la_forma_de_venezuela_es": "otra palabra distinta para lo mismo",
                 "entonces": "B se refuerza",
                 "por_que": "si el caquetío tiene voz propia para el aliado ritual, la -tiao es la importada"},
                {"si_aparece": "una atestación caquetía de la familia -tiao que NO venga de Oviedo",
                 "entonces": "cambia el fondo entero del caso",
                 "por_que": ("las dos entradas caquetías del lexicón (`datihao`, `waitiao`) citan la "
                             "misma página de Oliver sobre el mismo Oviedo. Una fuente "
                             "independiente rompería la circularidad, que es el problema real. "
                             "⚠️ Y **hay una, y estaba en casa**: el `tiao` de los caquetíos de "
                             "Apure que Arcaya 1920 p. 48 atribuye al Padre Carvajal. Ver "
                             "`meta.la_otra_orilla_estaba_en_casa` — pero es de Apure y no de la "
                             "costa, así que la regla 4 manda antes que la alegría")},
            ],
        },
        "⚠️_leer_despues_de_esto": ("`meta.la_otra_orilla_estaba_en_casa`, que se midió después de "
                                    "escribir este bloque y localiza la página que falta en el tomo "
                                    "**II** de Oviedo (pp. 297-300), no en el IV."),
    }


def bloque_diao(M, gu):
    """«diao y daitiao son símiles» — medido, sin forzar el match ni negarlo."""
    # (1) ¿hay en taíno un diao / tiao / -tiao con valor de RANGO?
    corpus_tn = []
    for e in M["lengs"]["taíno"]:
        corpus_tn.append((e["forma"], e["glosa"], e["ficha"]["estrato"]))
    brinton, cita_b = headwords_brinton()
    sonda = {}
    for nombre, patron in (("diao", r"^dia[ho]?$"), ("tiao (en cualquier posición)", r"tia[ho]"),
                           ("-tiao final", r"tia[ho]?$"), ("dia- inicial", r"^dia"),
                           ("d- inicial", r"^d")):
        sonda[nombre] = {
            "en_las_voces_taínas_del_cruce": sorted({f for f, _g, _s in corpus_tn
                                                     if re.search(patron, f, re.I)}),
            "en_los_lemas_de_brinton": sorted({f for f in brinton if re.search(patron, f, re.I)}),
        }
    # (2) el campo de rango, lado a lado
    def _es_rango(glosa, cat=None, categoria=None):
        cabs = {c for c, _ex, _s in conceptos(glosa)}
        if cabs & {_norm_es(x) for x in CAMPO_DE_RANGO["glosas"]}:
            return True
        return (cat in CAMPO_DE_RANGO["cats"]) or (categoria in CAMPO_DE_RANGO["categorias"])

    rango_tn = [{"forma": f, "glosa": g, "fuente": s} for f, g, s in sorted(set(corpus_tn))
                if _es_rango(g)]
    rango_cq = []
    for r in M["res"]:
        c = r["c"]
        if c["capa"] != ATESTIGUADO:
            continue
        if _es_rango(c["sig"], c["cat"], c["categoria"]):
            rango_cq.append({"forma": c["clave"], "glosa": c["sig"],
                             "fonemizada": c["cands"][0][0] if c["cands"] else "",
                             "cita": (c["notas"] or "sin nota")[:120]})
    # (3) el cruce ENTERO del campo, con el test
    cruce = []
    for a in rango_cq:
        fa = fon(a["forma"], "colonial", gu)
        for b in rango_tn:
            fb = fon(b["forma"], "colonial", gu)
            s = difflib.SequenceMatcher(None, fa, fb, autojunk=False).ratio()
            if s < UMBRAL_PARECIDO:
                continue
            letra, porque, j = test_cognado_o_prestamo(fa, fb, campo_de_rango=True)
            cruce.append({"caquetio": a["forma"], "glosa_caquetia": a["glosa"],
                          "taino": b["forma"], "glosa_taina": b["glosa"],
                          "fuente_taina": b["fuente"], "similitud": round(s, 3),
                          "esqueletos": f"{j['esqueleto_caquetio']} ~ {j['esqueleto_taino']}",
                          "letra": letra, "por_que": porque})
    cruce.sort(key=lambda d: -d["similitud"])
    hay_diao = bool(sonda["diao"]["en_las_voces_taínas_del_cruce"]
                    or sonda["diao"]["en_los_lemas_de_brinton"])
    return {
        "lo_que_dice_miguel": ("«diao y daitiao que son símiles son las versiones caquetías de la "
                               "versión Taína. Un cognado que hace match.»"),
        "lo_que_dice_oliver": (
            "que son DOS LEXEMAS y no uno: `diao` = /d-ia(o)/ sobre la raíz lokona /d-ai-/ de "
            "'palabra, lengua' (cognado-008, Oliver p. 146, con el lokono `dai-yana-ho`); "
            "`datihao`/`daitiao` = /da-/ + /-(i)tiao/ sobre la raíz de parentesco /atti/ "
            "(cognado-009, p. 147). La frase «diao is, in many ways, closely related to datihao» "
            "(n. 42) **no es una identificación**: son parientes por compartir el prefijo /d-/ y el "
            "sufijo /-(h)o/, no la raíz. Ya está escrito así en 4-fuentes/oliver-1989-cap2.md."),
        "que_comparten_con_precision": [
            "el prefijo /d-/ de 1ª persona singular — el mismo que `dare` y `dato`, y el pilar de "
            "que el caquetío salga del fondo lokono (C1). Lo comparten con el lokono y con el "
            "taíno, así que NO es un lazo particular entre las dos palabras.",
            "el sufijo /-(h)o/ nominalizador solemne, que Oliver llama «characteristic of both "
            "Taíno and Lokono» (p. 147) y que también lleva `boratio`.",
        ],
        "que_NO_comparten": [
            "la RAÍZ. /-ai-/ 'palabra, lengua' contra /-atti-/ 'pariente'. Dos etimologías "
            "distintas, escritas por el mismo autor en dos páginas seguidas.",
            "la GLOSA. `diao` es 'señor principal, jefe mayor' (Zavala p. 67, atestiguado por vía "
            "caquetía propia); `datihao` es 'padrino de cautivo, el que presta su nombre' (Oliver "
            "sobre Oviedo). Rango contra alianza. Bajo la política del 2026-09-19 —glosa "
            "normalizada idéntica o no hay par— no son el mismo concepto ni de lejos.",
        ],
        "y_la_pregunta_taina_medida": {
            "pregunta": "¿hay en taíno un `diao`, `tiao` o `-tiao` con valor de RANGO?",
            "sonda": sonda,
            "cita_de_los_lemas_de_brinton": cita_b,
            "respuesta": (
                ("SÍ, y hay que mirarlo una a una — ver `sonda`." if hay_diao else
                 "**NO.** En taíno no hay ninguna voz `diao` ni `dia-`. ")
                + " Lo que sí hay es `guatiao` 'friend, companion' (brinton-1871 p. 12, cronista "
                  "Richardo; lokono `ahati`), que es la gemela de `datihao` y NO significa rango "
                  "sino alianza. Los títulos de rango taínos son otros y ninguno se parece a "
                  "`diao`: `casique` 'a chief', `nitainos` 'the title applied to the petty chiefs', "
                  "`matunheri` 'a title applied to the highest chiefs' (Las Casas, Hist. Apol. cap. "
                  "197), `guaoxeri` 'the lowest class', `bajari` 'title applied to sub-chiefs "
                  "ruling villages' — todos en brinton-1871 pp. 11-13."),
            "la_consecuencia": (
                "la frase de Miguel se parte en dos y las dos mitades miden distinto. **`datihao` "
                "SÍ tiene gemela taína** (`guatiao`), con la misma raíz y distinto prefijo de "
                "persona — y ésa es la que el test no puede decidir. **`diao` NO tiene gemela "
                "taína ninguna**: no hay dónde hacer match. Su pareja, la que Oliver le da, es "
                "LOKONA (`dai-yana-ho`), y ésa sí es dato de filiación, que es la columna de D11 y "
                "no la del contacto."),
        },
        "el_campo_de_rango_lado_a_lado": {
            "que_es": ("el cruce completo del campo donde cae `diao`, en vez de esperar a que la "
                       "glosa case palabra por palabra. Es lo que contesta «¿hay algo taíno que se "
                       "le parezca?» sin escoger el candidato después de verlo: el campo se declara "
                       "arriba, en `CAMPO_DE_RANGO`."),
            "caquetio_atestiguado": rango_cq,
            "taino": rango_tn,
            "parejas_sobre_el_umbral_con_el_test_aplicado": cruce,
            "si_sale_vacio": ("no hay ni una pareja de rango caquetío~taíno que pase el umbral de "
                              "parecido. Con los dos inventarios delante, eso es un cero auditable "
                              "y no un cero de consulta (regla 6)."),
        },
    }


def bloque_la_otra_orilla():
    """Lo que el repo YA tenía sobre la otra orilla, y nadie había conectado.

    El barrido de Arcaya 1920 (469.953 caracteres, pymupdf, 2026-09-22) lo
    cambia todo, y lo cambia dos veces: da la página exacta de Oviedo que
    falta —tomo II, no tomo IV— y da una atestación de la familia que **no
    pasa por Oviedo ni por Oliver**.
    """
    return {
        "como_se_midio": ("barrido del PDF de Arcaya que el repo ya tiene "
                          "(`fuentes_caquetios/Arcaya_1920_Historia_Estado_Falcon.pdf`, 348 pp., "
                          "469.953 caracteres extraídos con pymupdf) el 2026-09-22. Conteos: "
                          "`tiao` 1, `diao`/`díao` 8, `datihao` 0, `daitiao` 0, `guaitiao` 0, "
                          "`boratio` 15."),
        "hallazgo_1_la_pagina_que_falta": {
            "que_es": ("la atestación «de la Provincia de Venezuela» que el encargo daba por "
                       "perdida en «el apéndice al tomo IV» **está en el tomo II, y Arcaya da la "
                       "página en nota al pie**."),
            "arcaya_p_impresa_48_nota_33": "Oviedo y Valdez, Historia general y natural de las Indias, tomo 2, pág. 299",
            "arcaya_p_impresa_115_nota_22": "Oviedo y Valdez, obra citada, tomo II, pág. 297",
            "arcaya_p_impresa_116_nota_23": "obra y tomo citados, pág. 300 (el funeral del díao)",
            "y_la_glosa_de_oviedo_que_arcaya_copia": (
                "p. impresa 115: Manaure era un diao, «señor principal que tiene muchos indios y le "
                "son subjetos otros caciques» — la glosa es del propio Oviedo, tomo II p. 297"),
            "consecuencia": (
                "quien vaya a por la otra orilla ya no busca un apéndice inexistente: busca "
                "**Oviedo y Valdés tomo II, pp. 297-300**. Y lo que hay allí es `diao`, no "
                "`datihao`. La deuda documental cambia de forma y de tomo."),
        },
        "hallazgo_2_diao_tiene_una_segunda_fuente_INDEPENDIENTE": {
            "la_frase": ("Arcaya p. impresa 48: los caquetíos de Coro llamaban «díaos» a sus "
                         "caciques principales, «nombre idéntico al de **tiaos**» con que se "
                         "designaba, según el Padre Carvajal, a los **Caquetíos de Apure**"),
            "nota_34_de_arcaya": "«Relación del descubrimiento del Río Apure. Pág. 317» (Jacinto de Carvajal, 1648)",
            "por_que_importa": (
                "es una atestación de la familia que **no pasa por Oviedo ni por Oliver**. Todo lo "
                "demás que el repo tiene de `-tiao` viene de la misma página de Oliver sobre el "
                "mismo Oviedo; esto no. Rompe la circularidad que este mismo cruce denunciaba hace "
                "tres bloques."),
            "y_tambien": ("Arcaya lo enlaza además con el tariana `yatii`/`yaivi` 'médico "
                          "hechicero' vía Koch-Grünberg 1911 — tercera vía, y arahuaca del "
                          "noroeste amazónico"),
            "⚠️_lo_que_NO_prueba": (
                "que `tiao` sea caquetío COSTERO. Es de Apure, y la regla 4 es explícita: «los "
                "caquetíos no eran una sola sociedad», «importar un rasgo de Barquisimeto o los "
                "Llanos sin marcarlo es el error que Oliver denuncia». Se anota como dato de la "
                "esfera caquetía ancha, no de la polity que la simulación modela."),
        },
        "hallazgo_3_y_es_el_que_pesa": {
            "el_hecho": "`díao` en Coro y `tiao` en Apure, y Arcaya los llama «nombre idéntico»",
            "por_que_pesa": (
                "es un contraste /d-/ ~ /t-/ **dentro del caquetío**, entre dos polities. Y /d-/ "
                "frente a /t-/ es EXACTAMENTE la C1 de Oliver: el prefijo de 1ª sg. que sólo "
                "lokono y taíno conservan como /dA-/, mientras el guajiro-paraujano innova /tA-/. "
                "Es el pilar del que cuelga la tesis lokonoide del caquetío, y con ella D11."),
            "las_dos_lecturas": [
                {"lectura": "el contraste es REAL y es dialectal",
                 "entonces": ("«el caquetío conserva /d-/» es una afirmación sobre el caquetío "
                              "COSTERO, no sobre el caquetío. El caquetío de Apure caería del lado "
                              "de la innovación /tA-/, y la posición de Oliver se vuelve más "
                              "local —y más interesante— de lo que está escrita. Sería regla 4 "
                              "mordiendo en la fonología, que es donde nadie la había mirado")},
                {"lectura": "el contraste es de COPISTA",
                 "entonces": ("Carvajal oyó o escribió sin la /d-/ inicial, o Arcaya normalizó. Una "
                              "sola ocurrencia en un texto de 1648 que el repo no tiene no sostiene "
                              "un dialecto")},
            ],
            "que_lo_decidiria": (
                "la p. 317 de la *Relación del descubrimiento del Río Apure* de Jacinto de Carvajal, "
                "que NO está en el repo. Es la misma clase de dato que falta para `datihao`: una "
                "página. Y ésta además es de dominio público y del s. XVII."),
            "lo_que_NO_se_hace_aqui": (
                "tocar D11 ni la ficha de Oliver. Esto PROPONE (regla 5): deja el hallazgo medido y "
                "la página localizada para que Miguel decida si abre una pregunta o no."),
        },
        "hallazgo_4_datihao_no_esta_en_arcaya": {
            "medido": "`datihao` = 0, `daitiao` = 0, `guaitiao` = 0 en las 348 páginas",
            "que_significa": (
                "Arcaya lee a Oviedo con lupa —le cita tomo, página y nota— y **no recoge la voz**. "
                "El único que la lee ahí es Oliver. Eso no la desmiente, pero sí confirma lo que el "
                "test ya decía por otra vía: el lado caquetío de `datihao` es **una lectura de un "
                "autor**, y hoy no hay manera de contrastarla."),
        },
        "y_el_corpus_ya_lo_sabia": (
            "`3-mundo/corpus/creencia.yaml` §creencia-001b lleva escrito desde hace tiempo «el díao "
            "(diao; **tiao entre los caquetíos de Apure**)» con la referencia «Oviedo y Valdés t. II "
            "p.299; Arcaya 1920:48,116,118». El dato estaba; lo que no estaba era la lectura: que "
            "ese `tiao` toca la C1 de Oliver, y que esa referencia es la página que la campaña "
            "andaba buscando en el tomo equivocado."),
    }


def bloque_el_eje_prosodico():
    """El acento como TERCER eje del test — todavía no ejecutable, y ya decisivo.

    Viene de la parcela de la *Apologética* (PR #194, rama
    `campana/taino2-apologetica`, `6-fusion/taino2_las_casas_apologetica.yaml`).
    **No está en main**, así que este script NO lo lee: si lo leyera, `--check`
    fallaría en cuanto alguien corriera el script sin esa rama. Se declara con
    su fuente y se deja el gancho escrito.
    """
    return {
        "estado": ("PENDIENTE de que entre el PR #194. Declarado aquí con su cita, no leído: el "
                   "script sólo lee lo que está en main, para que `--check` no dependa de qué "
                   "ramas tenga cada uno."),
        "que_es": (
            "Las Casas marca el ACENTO de 97 formas taínas en la *Apologética* («la penúltima "
            "sílaba luenga», «la última luenga y aguda»…). Es un rasgo más, y del mejor tipo: el "
            "acento de una forma HEREDADA debería seguir un patrón regular entre las dos lenguas; "
            "el de un PRÉSTAMO no tiene por qué."),
        "lo_que_ya_dice_sobre_diao_sin_necesidad_de_ejecutarlo": {
            "el_hecho": (
                "los TRES títulos de rango taínos que Las Casas acentúa son OXÍTONOS y acaban los "
                "tres en `-í` tónica: `Guaoxerí` «la última sílaba luenga», `Baharí` «la misma "
                "última luenga», `Matunherí` «el acento en la postrera sílaba»"),
            "la_lectura": (
                "no son tres palabras sueltas: son una SERIE. El taíno nombra los grados de señorío "
                "con un molde —raíz + `-í` tónica— y `diao` no tiene ese molde ni de forma ni de "
                "acento (la tradición venezolana lo escribe `díao`, con el acento al principio). "
                "Es una segunda razón, independiente de la forma, para que `diao` no tenga gemela "
                "taína: **no encaja en la serie con la que el taíno hace títulos**."),
            "⚠️_el_limite": (
                "el acento del caquetío no está medido en ninguna parte. La tilde de `díao` es "
                "editorial —Arcaya 1920—, no una marca de cronista como las de Las Casas. Así que "
                "esto es un eje ASIMÉTRICO: sirve para describir el taíno y todavía no para "
                "comparar. Lo que lo cerraría es una fuente que marque acento en caquetío."),
        },
        "y_un_cero_que_pesa_en_el_caso_datihao": (
            "**`guatiao` = 0 en toda la *Apologética***, y la institución del cambio de nombre SÍ "
            "está descrita allí. O sea: Las Casas cuenta el rito y no usa la palabra. Súmese a que "
            "el `Guatiao` de Brinton (p. 12) no viene de un cronista sino de **Richardo, "
            "*Diccionario provincial*** — obra cubana del siglo XIX. El lado taíno de `guatiao` es "
            "más flojo de lo que parecía, igual que el caquetío. **Las dos orillas del caso son "
            "finas.**"),
        "y_daca_gana_un_apoyo": (
            "`daca` 'yo' queda confirmado también en la *Apologética*, además de Pané cap. XXV. "
            "P3 (el /dA-/ de 1ª sg.) gana una atestación independiente — y sigue sin distinguir "
            "herencia de préstamo entre caquetío y taíno, que es lo que P3 ya declara."),
        "cuando_entre_el_PR_194": [
            "leer `6-fusion/taino2_las_casas_apologetica.yaml` §lexico como una fuente más en "
            "`YAML_TAINO` (trae `forma_fuente`, `glosa_fuente`, `pagina_impresa` y `verificado`);",
            "añadir `marca_prosodica` al diagnóstico, como cuarto campo junto a regulares, "
            "candidatas y violaciones;",
            "y antes que nada, buscar una fuente que marque acento en caquetío. Sin eso el eje "
            "describe una lengua y no compara dos.",
        ],
    }


def bloque_morfemas_filiacion_no_contacto(M):
    """Los morfemas compartidos van en la columna de FILIACIÓN, no en la de contacto.

    Un morfema gramatical compartido no prueba que dos pueblos se hablaran:
    prueba que vienen del mismo sitio. La tabla de `morfologia` dice cuál
    comparten; ésta dice en qué columna cuenta cada uno, y lo mide sobre las
    transcripciones que entraron hoy.
    """
    B = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "taino_brinton_1871.yaml"),
                               encoding="utf-8"))
    frases = {str(e.get("forma")): e for e in
              (B["vocabulario_antillano"].get("frases_y_compuestos") or {}).get("entradas", [])}
    formas_tn = sorted({e["forma"] for e in M["lengs"]["taíno"]})
    return {
        "la_regla": (
            "un morfema gramatical compartido es dato de FILIACIÓN (de dónde viene la lengua), no "
            "de CONTACTO (con quién habló el pueblo). Los morfemas casi nunca se prestan; el "
            "léxico de cultígenos, bichos, mercancías y ritos sí. Mezclar las dos columnas es "
            "contar dos veces: el /dA-/ que comparten taíno y caquetío lo comparte el lokono, y por "
            "esa vía ya está contado en D11."),
        "filas": [
            {"morfema": "ma- privativo",
             "taino": ("`mahite` 'you have lost a tooth', brinton-1871 p. 14, cronista Las Casas "
                       "Hist. Apol. cap. 198, contra el lokono «marikata, you have no teeth "
                       "(ma negative, ari tooth)»"),
             "esta_en_las_transcripciones": "mahite" in frases,
             "caquetio": "declarado en CLAUDE.md §morfología: van Buurt 2014 §8 y Perea 1942 p. 555",
             "columna": "FILIACIÓN, y ni siquiera taíno-caquetía",
             "por_que": ("Oliver p. 147 n. 43 declara el privativo /mV-/ común a las lenguas "
                         "MAIPURES. Confirma que el caquetío tiene lo que la familia tiene; no "
                         "acerca el taíno al caquetío más que a cualquier hermana")},
            {"morfema": "da- / d- de 1ª persona singular",
             "taino": "`daca` 'yo' (pane-c1498 cap. XXV, «Dios naboria daca»); `da-` en `da(i)tia-o`",
             "esta_en_las_transcripciones": True,
             "caquetio": "`diao`, `datihao`, `dare`, `dato` — oliver-1989-cap2 pp. 136, 146-147",
             "columna": "FILIACIÓN, y es el pilar de D11",
             "por_que": ("separa al trío caquetío-taíno-lokono del par guajiro-paraujano (/tA-/). "
                         "Contarlo otra vez por la vía taína sería contar dos veces el mismo dato. "
                         "Y para el test del contacto es INÚTIL: un préstamo taíno habría entrado "
                         "con su /d-/ intacto")},
            {"morfema": "-(h)o nominalizador solemne",
             "taino": "oliver-1989-cap2 p. 147: «characteristic of both Taíno and Lokono»",
             "esta_en_las_transcripciones": bool([f for f in formas_tn if f.endswith("o")]),
             "caquetio": "`diao`, `datihao`, `boratio`, `kaket-ío` — el mismo Oliver, pp. 146-148",
             "columna": "FILIACIÓN",
             "por_que": ("lo comparte con el lokono, otra vez. Y es lo ÚNICO que `diao` y `datihao` "
                         "comparten de verdad junto con el /d-/: no la raíz")},
            {"morfema": "gua- / wa- de 3ª plural",
             "taino": "brinton-1871 p. 12 s.v. Gua «a very frequent prefix»; oliver p. 147",
             "esta_en_las_transcripciones": bool([f for f in formas_tn if f.startswith("gua")]),
             "caquetio": "`guaitiao` (forma_fuente de `waitiao`), y los topónimos en gua-",
             "columna": "FILIACIÓN",
             "por_que": ("ojo: el `-gua` LOCATIVO del canon caquetío es otra cosa —sufijo, no "
                         "prefijo— y contarlos juntos sería la trampa de `-kana`. Ver la tabla de "
                         "`morfologia`")},
            {"morfema": "-caco 'ojos'",
             "taino": ("`buticaco` 'you are blue-eyed', `xeyticaco` 'you are black-eyed' — "
                       "brinton-1871 p. 14, Las Casas Hist. Apol. cap. 198, contra el lokono "
                       "`acou`/`akusi`"),
             "esta_en_las_transcripciones": "buticaco" in frases,
             "caquetio": "NADA. El canon caquetío no declara ningún formante de 'ojo'",
             "columna": "ninguna — es hueco caquetío, no pareja",
             "por_que": ("lo trajo T2 ayer junto con `mahite`. Sirve para saber que el taíno tiene "
                         "morfología de posesión inalienable del cuerpo; del caquetío no hay con "
                         "qué compararlo")},
        ],
        "lo_que_esto_significa_para_la_pregunta_de_miguel": (
            "TODO lo que el taíno y el caquetío comparten en morfología cae en la columna de "
            "filiación, y el lokono lo comparte igual. **Ninguno de estos morfemas prueba contacto.** "
            "Lo que probaría contacto es léxico: una voz que viajó. Y para eso hace falta el test "
            "de correspondencias, no el inventario de afijos."),
    }


def bloque_antes_y_despues():
    """El antes/después MEDIDO, leyendo el YAML de ayer. Ninguna cifra a mano."""
    if not os.path.exists(ANTERIOR):
        return {"aviso": f"no está {os.path.relpath(ANTERIOR, R)}: no hay antes que comparar"}
    A = yaml.safe_load(io.open(ANTERIOR, encoding="utf-8"))
    ant = ((A.get("meta") or {}).get("resumen_atestiguado") or {}).get("por_lengua") or {}
    return {"que_es": ("las cifras del cruce del 2026-09-21 leídas de su propio YAML, no copiadas. "
                       "Lo que cambia entre los dos días es SÓLO la lista taína: entran las "
                       "transcripciones de T1/T2 con obra y página."),
            "fuente": os.path.relpath(ANTERIOR, R),
            "por_lengua_el_2026_09_21": {
                L: {k: d.get(k) for k in ("entradas_de_la_lengua", "conceptos_comparables",
                                          "parecidos_ge_umbral",
                                          "cognado_probable_ge_umbral_cognado", "similitud_media")}
                for L, d in ant.items()}}


# ═════════════════════════════════════════════════════════════════════════
# Morfología
# ═════════════════════════════════════════════════════════════════════════
def _sondar(formas, sondas):
    out = {}
    for nombre, patron in sondas:
        hits = sorted({f for f in formas if re.search(patron, f)})
        out[nombre] = {"n": len(hits), "formas": hits[:14]}
    return out


def headwords_brinton():
    """Los lemas de la «Vocabulary of the Ancient Language of the Great Antilles».

    SONDA, no censo. El censo de las fuentes taínas es de otro escriba; aquí
    sólo se cuentan formantes sobre la lista que Brinton 1871 pp. 11-14 imprime.
    """
    txt = io.open(TXT_BRINTON, encoding="utf-8", errors="replace").read()
    i = txt.find("Vocabulary  of  the  Ancient  Language")
    j = txt.find("The  following  numerals  are  given")
    if i < 0 or j < 0:
        return [], "no localizada"
    cuerpo = txt[i:j]
    out = []
    for ln in cuerpo.split("\n"):
        m = re.match(r"^([A-Z][A-Za-zá-úñ]{2,})(?:\s+or\s+([a-zá-úñ]+))?\s*[,.]", ln)
        if m:
            out.append(m.group(1).lower())
            if m.group(2):
                out.append(m.group(2).lower())
    return sorted(set(out)), "Brinton 1871 pp. impresas 11-14"


def onomastica_pane():
    """SONDA de formantes sobre las formas indígenas de Pané.

    Regla declarada y auditable: tokens capitalizados de 4+ letras que no
    estén en BLOQUEO_PANE y que no abran oración tras punto. El inventario
    entero se emite para que se pueda revisar a mano.
    ⚠️ El texto es la retraducción castellana de la versión italiana de Ulloa:
    cada nombre pasó por dos copistas. Sirve para contar formantes, no para
    citar una forma como exacta.
    """
    txt = io.open(TXT_PANE, encoding="utf-8", errors="replace").read()
    txt = re.sub(r"[.!?:;]\s+", " ␞ ", txt)     # marca de inicio de oración
    out = collections.Counter()
    for m in re.finditer(r"(␞\s+)?\b([A-ZÁÉÍÓÚÑ][a-zá-úñ]{3,})\b", txt):
        if m.group(1):
            continue
        w = m.group(2).lower()
        if w in BLOQUEO_PANE:
            continue
        out[w] += 1
    return out


def bloque_morfologia(M, caq_ates, taino_ates):
    """La tabla morfema a morfema. Los apoyos son DECLARADOS con su cita; lo
    que el script mide es cuántas formas del repo los exhiben de verdad."""
    f_caq = sorted({c["clave"] for c in caq_ates} |
                   {c["forma_fuente"] for c in caq_ates if c.get("forma_fuente")})
    f_tno = sorted({e["forma"] for e in taino_ates})
    brinton, cita_brinton = headwords_brinton()
    medido = {
        "caquetio_atestiguado": {"n": len(f_caq), **_sondar(f_caq, SONDAS_PREFIJO + SONDAS_SUFIJO)},
        "taino_atestiguado_del_lexicon": {"n": len(f_tno),
                                          **_sondar(f_tno, SONDAS_PREFIJO + SONDAS_SUFIJO)},
        "taino_lemas_de_brinton": {"n": len(brinton), "cita": cita_brinton,
                                   **_sondar(brinton, SONDAS_PREFIJO + SONDAS_SUFIJO)},
    }

    filas = [
        {
            "morfema_caquetio": "ma- privativo",
            "capa_y_cita_caquetia": ("atestiguado en la nota (2-lengua/morfologia.md §6): van Buurt "
                                     "2014 §8 y el par mínimo lokono de Perea 1942 p. 555. La entrada "
                                     "del motor sigue con `deuda: sin-procedencia`"),
            "candidato_taino": "ma- en mahite 'sin dientes'",
            "que_fuente_lo_afirma": ("brinton-1871 p. impresa 13: mahite «you have lost a tooth»; y "
                                     "compara el arahuaco «marikata, you have no teeth (ma negative, "
                                     "ari tooth)». Oliver 1989 cap. 2 p. 147 n. 43 lo generaliza: el "
                                     "privativo /mV-/ es común a las lenguas maipures"),
            "veredicto": "MISMO MORFEMA, y el paralelo no es taíno-caquetío: es arahuaco común",
            "por_que": ("Brinton segmenta ma- + ari 'diente' y Oliver lo declara maipure general. "
                        "Sirve para confirmar que el caquetío tiene lo que la familia tiene; NO "
                        "acerca el taíno al caquetío más que a cualquier otra hermana."),
        },
        {
            "morfema_caquetio": "ma- privativo",
            "capa_y_cita_caquetia": "igual que la fila de arriba",
            "candidato_taino": "manicato 'fuerte, valiente'",
            "que_fuente_lo_afirma": ("brinton-1871 p. impresa 13, citando a Oviedo. Brinton lo "
                                     "relaciona con un arahuaco «manikade» glosado «I am unhurt, I am "
                                     "unconquered», pero NO lo segmenta"),
            "veredicto": "INDECIDIBLE — el sentido es negativo y encaja, pero nadie lo segmenta",
            "por_que": ("El OCR de la etimología de Brinton («from indn, manin») no es legible y hay "
                        "que verla en imagen antes de citarla. Sin segmentación explícita, contar "
                        "manicato como apoyo de ma- sería la trampa que el proyecto se tragó dos "
                        "veces hoy mismo: macana no sostenía -kana, y el -po de apopo era "
                        "reduplicación. Comparte sílaba; el morfema está sin probar."),
        },
        {
            "morfema_caquetio": "ka- atributivo / existencial",
            "capa_y_cita_caquetia": ("atestiguado en la nota: van Buurt 2014 §8 (Casibari «hay rocas "
                                     "duras») y el par mínimo k-ere-u-ti / m-ere-u-ti de Perea 1942 "
                                     "p. 555. d21.5 → C, 2026-09-21"),
            "candidato_taino": "ka-/ca- inicial (caney, cacique, casabe, caona, caiman…)",
            "que_fuente_lo_afirma": ("NADIE en el repo. Brinton no segmenta ningún ca- taíno como "
                                     "prefijo; Oliver cap. 2 p. 148 da el atributivo /k-/, /kV-/ "
                                     "entre los afijos ARAHUACOS generales, sin ejemplo taíno"),
            "veredicto": "SIN APOYO — la sílaba está, el morfema no está afirmado por ninguna fuente",
            "por_que": ("`caiman` Brinton lo glosa «lit. to be strong» sobre el arahuaco k-aiman, que "
                        "sí sería el atributivo; pero es su lectura del ARAHUACO de Guayana, no del "
                        "taíno, y una sola lectura no hace regla. Queda como pregunta para el minado "
                        "de T1/T2, no como corroboración."),
        },
        {
            "morfema_caquetio": "da- / d- de 1ª persona singular",
            "capa_y_cita_caquetia": ("el motor NO lo tiene como regla: `ta-` (wayuu) es su posesivo de "
                                     "1ª sg. El /dA-/ caquetío es dato de oliver-1989-cap2 pp. 146-147 "
                                     "en diao, dare, dato, datihao — y es el pilar de que el caquetío "
                                     "salga del mismo fondo que el lokono"),
            "candidato_taino": "daca 'yo' (Pané); da- en da(i)tia-o; m-a(h)i-te que sería da-ai",
            "que_fuente_lo_afirma": ("pane-c1498 cap. XXV: «Dios naboria daca» glosado «yo soy siervo "
                                     "de Dios»; oliver-1989-cap2 p. 147: «/da-/ in da(i)tia-o is first "
                                     "person singular marker», y p. 136 sitúa /dA-/ en lokono, taíno y "
                                     "«perhaps Caquetío»"),
            "veredicto": "MISMO MORFEMA — y es el paralelo mejor sostenido de los tres",
            "por_que": ("Es el único de la lista con atestación taína dentro del repo (Pané) y con la "
                        "afirmación explícita de Oliver. ⚠️ Pero es exactamente el argumento de "
                        "filiación que ya sostiene D11, y NO es exclusivo taíno-caquetío: el lokono "
                        "lo tiene igual. Acerca al caquetío al par lokono-taíno frente al "
                        "guajiro-paraujano (/tA-/), no al taíno en particular."),
            "alerta": ("⚠️ CHOQUE CON EL LEXICÓN, y hay que mirarlo: el repo tiene `daca` como "
                       "`taíno-reconstruido` con la glosa 'mano' (desde el lokono daka). La forma que "
                       "Pané atestigua es `daca` 'yo'. No se toca nada aquí —esto propone—, pero el "
                       "par homógrafo tiene que decidirlo Miguel."),
        },
        {
            "morfema_caquetio": "-gua (locativo, 'región')",
            "capa_y_cita_caquetia": ("reconstruido, `deuda: sin-procedencia` (d21.7 → B, 2026-09-21). "
                                     "Su único apoyo escrito es «Topónimos venezolanos de Falcón y "
                                     "Sucre»; el canon lo sostiene con paragua = para 'mar' + -gua"),
            "candidato_taino": "gua- prefijo de nombres propios; y el -wa de bara-wa 'mar'",
            "que_fuente_lo_afirma": ("brinton-1871 p. impresa 12, s.v. Gua: «a very frequent prefix», "
                                     "citando a Pedro Mártir (Decad. p. 285) sobre que casi ningún "
                                     "nombre de rey empieza sin él; oliver-1989-cap2 p. 147: «/wa- "
                                     "[gua-]/ is a third person plural marker». Y p. 150 da el taíno "
                                     "bara-wa 'mar' junto al caquetío para-"),
            "veredicto": ("DOS MORFEMAS DISTINTOS con la misma sílaba — pero el bara-wa taíno es el "
                          "mejor cabo suelto que tiene la campaña de -gua"),
            "por_que": ("El gua- taíno que documentan Brinton y Oliver es un PREFIJO (3ª plural / "
                        "formante de nombres propios); el -gua caquetío del canon es un SUFIJO "
                        "locativo. Misma sílaba, posición contraria, función contraria: contar el uno "
                        "como apoyo del otro sería la trampa de -kana. Lo que SÍ es paralelo real es "
                        "otra cosa: taíno bara-wa 'mar' y caquetío para-gua tienen la misma raíz "
                        "'mar' y el mismo elemento detrás. Eso no prueba la glosa 'región', pero es "
                        "la primera pista independiente que la campaña d21.7 tiene."),
        },
        {
            "morfema_caquetio": "-bana (locativo, 'cerro, sitio alto')",
            "capa_y_cita_caquetia": ("ATESTIGUADO, D9 resuelta con seis apoyos: zavala-reyes-2015 #26, "
                                     "gonzalez-batista-nombre-de-coro, velasco-2015-resistencia"),
            "candidato_taino": "Agüey-bana (antropónimo) y pana-pe(n) 'fruto del pan'",
            "que_fuente_lo_afirma": ("oliver-1989-cap2 p. 148: «Taíno, for example, has pana-pe(n) for "
                                     "'breadfruit' and Agüey-bana as an anthroponym»"),
            "veredicto": "MISMO FORMANTE, GLOSA DISTINTA — y la distinta es la nuestra",
            "por_que": ("Oliver pone el -bana caquetío, el -bana/-pana taíno, el a-pana guajiro 'hoja' "
                        "y el -bana lokono 'techo' bajo una misma glosa: 'rodear, cubrir, extensión'. "
                        "El canon del proyecto le dio a -bana 'cerro, sitio alto' (D9) con apoyo "
                        "caquetío propio. Las dos cosas pueden convivir —la nota ya deja viva la "
                        "lectura 'ancho/llano' de van Buurt para kabana, darubana y guacaubana— pero "
                        "el paralelo taíno NO corrobora D9: empuja al otro lado."),
        },
        {
            "morfema_caquetio": "-coa / -bakoa (postposición toponímica)",
            "capa_y_cita_caquetia": ("-bacoa ATESTIGUADO (morfemas.yaml morfema-001: cinco topónimos "
                                     "glosados de Esteves 1989 + alvarado-1921 vía van-buurt-2014 §10); "
                                     "migra a -bakoa con el corte, d21.14 A"),
            "candidato_taino": "coa 'palo cavador'; barbacoa",
            "que_fuente_lo_afirma": ("oliver-1989-cap2 p. 149: «Taíno has the noun coa for the digging "
                                     "stick»; brinton-1871 p. impresa 11 s.v. Barbacoa: «a loft for "
                                     "drying maize», del arahuaco burrabakoa «a place for storing "
                                     "provisions»"),
            "veredicto": "NO ES EL MISMO MORFEMA — el coa taíno es un NOMBRE, no una postposición",
            "por_que": ("Oliver trae el coa taíno como apoyo SEMÁNTICO de que la postposición arahuaca "
                        "-coa se aplica a lo puntiagudo, no como paralelo morfológico: un palo cavador "
                        "es un sustantivo. Y barbacoa lo avisa el propio Oliver p. 151: «one must be "
                        "careful about some terms (e.g. barbacoa) offered by the Spanish as 'native' "
                        "Caquetío». Es tainismo llegado con el castellano, no herencia compartida."),
        },
        {
            "morfema_caquetio": "-(h)o nominalizador solemne · gentilicio -ío",
            "capa_y_cita_caquetia": ("NO está en TODAS_LAS_REGLAS: el motor no lo tiene. Es dato de "
                                     "oliver-1989-cap2 pp. 146-148, que lo ve en diao, datihao, "
                                     "boratio y en el propio kaket-ío"),
            "candidato_taino": "-hu/-o taíno-lokono; y los gentilicios Luca-yo, Cigüa-yo",
            "que_fuente_lo_afirma": ("oliver-1989-cap2 p. 147: el sufijo nominalizador solemne /-(h)o/ "
                                     "«characteristic of both Taíno and Lokono»; y la n. 44 p. 148 "
                                     "atribuye la serie -ío/-yo a Gary Vescelius, **comunicación "
                                     "personal de 1982**: «Luca-yo, Cigüa-yo, Kaket-ío»"),
            "veredicto": "PLAUSIBLE PARA -(h)o · NO CITABLE PARA -ío/-yo",
            "por_que": ("El nominalizador lo afirma Oliver en su propio texto y con ejemplos de las "
                        "dos lenguas. La serie de gentilicios, en cambio, es una comunicación personal "
                        "en nota al pie: no hay dato publicado detrás, no hay lista, y Lucayo y "
                        "Ciguayo son exónimos coloniales. Es sugerente y NO es evidencia; escribirlo "
                        "como apoyo sería inventar una clave foránea."),
        },
        {
            "morfema_caquetio": "-(i)tiao / -ati de parentesco y alianza",
            "capa_y_cita_caquetia": ("`datihao` está en el lexicón como caquetío-atestiguado; también "
                                     "`boratio` 'chamán' y `dato` 'fruto del cardón'"),
            "candidato_taino": "guatiao / waitiao / watiao 'amigo, aliado'",
            "que_fuente_lo_afirma": ("oliver-1989-cap2 p. 147, citando a Las Casas [1552] 1929 II:291 "
                                     "sobre el trueque de nombres entre Ponce de León y el cacique "
                                     "Agueybana; brinton-1871 p. impresa 12 s.v. Guatiao «friend, "
                                     "companion», del arahuaco ahati"),
            "veredicto": ("MISMO MORFEMA según Oliver — pero es EL caso que la skill §8 manda tratar "
                          "con cuidado"),
            "por_que": ("Oliver escribe «This Taíno term is cognate to Caquetio daitiao». Y en la n. 42 "
                        "de la p. 146 DUDA de que datihao sea caquetío: Oviedo hablaba de «los indios "
                        "de la Provincia de Venezuela» en general y su larga residencia en La Española "
                        "pudo hacerle usar taíno; concluye que probablemente fuera «equally shared by "
                        "both Taíno and Caquetío». O sea: la voz más taína del caquetío puede ser "
                        "taína a secas. Y Jahn, que parecía corroborarla, cita el mismo apéndice de "
                        "Oviedo. El lexicón sigue teniéndola como caquetío-atestiguado sin la reserva."),
        },
        {
            "morfema_caquetio": "ni- / nitaíno (prefijo pronominal)",
            "capa_y_cita_caquetia": "el caquetío no declara ningún ni-",
            "candidato_taino": "nitaíno 'noble, principal'",
            "que_fuente_lo_afirma": "nadie: brinton-1871 p. impresa 14 lo DESMIENTE",
            "veredicto": "🔴 FALSO — la fuente del repo rechaza expresamente el análisis",
            "por_que": ("Brinton, sobre nitainos: «There is not the slightest authority for this, nor "
                        "for supposing, with Von Martius, that the first syllable is a pronominal "
                        "prefix». Lo deriva del arahuaco nuddan 'estar firme, hacer algo bien'. El "
                        "análisis ni- + taíno ya estaba descartado en 1871 por la misma obra de donde "
                        "el lexicón sacó sus voces taínas."),
        },
        {
            "morfema_caquetio": "-bo / -abo (formante toponímico)",
            "capa_y_cita_caquetia": ("Oliver cap. 2 p. 148 lo lista como «(e)-bo» entre los sufijos más "
                                     "comunes de la toponimia caquetía; el canon del proyecto NO lo "
                                     "tiene ni en morfemas.yaml ni en TODAS_LAS_REGLAS"),
            "candidato_taino": "—",
            "que_fuente_lo_afirma": ("nadie lo afirma del taíno en el repo. La sonda sobre los lemas de "
                                     "Brinton dice cuántos acaban en -bo (ver `medido`)"),
            "veredicto": "SIN PAREJA — y además es un hueco del propio canon caquetío",
            "por_que": ("Oliver lo declara para el caquetío y el proyecto nunca lo recogió; el taíno "
                        "no tiene quien lo afirme. La fila existe para que el hueco quede escrito "
                        "(regla 8: el hueco se admite, callarlo no)."),
        },
    ]
    return {"medido": medido, "filas": filas}


# ═════════════════════════════════════════════════════════════════════════
# Onomástica
# ═════════════════════════════════════════════════════════════════════════
def bloque_onomastica():
    T = yaml.safe_load(io.open(YAML_TOPONIMOS, encoding="utf-8"))
    A = yaml.safe_load(io.open(YAML_ANTROPONIMOS, encoding="utf-8"))
    vivos = [t for t in T["toponimos"] if t.get("nivel") != "descartado"]
    descartados = [t for t in T["toponimos"] if t.get("nivel") == "descartado"]
    f_vivos = sorted({str(t["forma"]).lower() for t in vivos})
    f_todos = sorted({str(t["forma"]).lower() for t in T["toponimos"]})
    f_antrop = sorted({str(a["forma"]).lower() for a in A["antroponimos"] if a.get("forma")})
    pane = onomastica_pane()
    f_pane = sorted(pane)

    # el contraste lado a lado, que es lo que contesta la pregunta onomástica
    corpus = [("topónimos caquetíos sin descartar", f_vivos),
              ("antropónimos caquetíos propuestos", f_antrop),
              ("onomástica taína de Pané (sonda)", f_pane)]
    contraste = {}
    for nombre, patron in SONDAS_PREFIJO + SONDAS_SUFIJO:
        fila = {}
        for etiqueta, formas in corpus:
            n = sum(1 for f in formas if re.search(patron, f))
            fila[etiqueta] = (f"{n}/{len(formas)}"
                              + (f" ({n / len(formas):.0%})" if formas else ""))
        contraste[nombre] = fila

    # los topónimos que Esteves atribuye a taíno / «caribe insular»
    atribuidos = sorted({str(t["forma"]) for t in T["toponimos"]
                         if re.search(r"ta[ií]n|caribe insular", str(t.get("clase", "")) +
                                      str(t.get("razon", "")) + str(t.get("observacion", "")), re.I)})
    return {
        "insumos": {
            "toponimos_en_canon": len(T["toponimos"]),
            "toponimos_sin_descartar": len(vivos),
            "toponimos_descartados": len(descartados),
            "antroponimos_propuestos": len(f_antrop),
            "formantes_antroponimicos_declarados": [f["formante"] for f in A["formantes"]],
            "onomastica_de_pane_tokens": len(f_pane),
        },
        "contraste_de_formantes": {
            "que_es": ("la misma sonda sobre los tres corpus onomásticos, lado a lado. Es lo que "
                       "contesta la pregunta: no si un formante existe en los dos sitios —con "
                       "listas de fonología parecida casi todo existe en los dos sitios— sino si "
                       "aparece en la misma proporción."),
            "como_leerlo": ("una proporción parecida no prueba nada por sí sola; una MUY distinta, "
                            "o un cero limpio contra un 20 %, sí dice algo. Y ningún número de aquí "
                            "es un morfema: una sonda cuenta sílabas en posición, y la tabla de "
                            "`morfologia` es la que dice si detrás hay morfema."),
            "⚠️_el_sesgo_que_hay_que_descontar": (
                "los tres corpus no son del mismo género. El caquetío sin descartar es sobre todo "
                "TOPONIMIA (nombres de sitio de Falcón y Paraguaná) y la sonda de Pané es sobre todo "
                "ANTROPONIMIA y nombres de mito de La Española. Parte de la diferencia es de género, "
                "no de lengua: que -bana y -coa —que son formantes de LUGAR— den cero en Pané puede "
                "medir que Pané casi no nombra lugares. La columna de antropónimos caquetíos es la "
                "que sí compara género con género, y es la que da los ceros más limpios: 0 de 48 en "
                "-ex y 0 de 48 en -el contra 6 % y 21 % en Pané."),
            "tabla": contraste,
        },
        "formantes_en_la_toponimia_caquetia": {
            "sin_descartar": _sondar(f_vivos, SONDAS_SUFIJO + SONDAS_PREFIJO),
            "canon_entero_incluidos_descartados": _sondar(f_todos, SONDAS_SUFIJO + SONDAS_PREFIJO),
        },
        "formantes_en_los_antroponimos_caquetios": _sondar(f_antrop, SONDAS_SUFIJO + SONDAS_PREFIJO),
        "sonda_onomastica_taina_sobre_pane": {
            "que_es": ("SONDA de formantes, no censo — el censo de las fuentes taínas es de otro "
                       "escriba. Regla: token capitalizado de 4+ letras que no abra oración y no esté "
                       "en la lista de bloqueo declarada."),
            "advertencia": ("el texto es la retraducción castellana de la versión italiana de Ulloa "
                            "(1571): cada nombre pasó por dos copistas y una imprenta veneciana. Vale "
                            "para contar formantes, no para citar una forma como exacta."),
            "tokens": len(f_pane),
            "los_mas_frecuentes": [f"{w} ×{n}" for w, n in pane.most_common(25)],
            "formantes": _sondar(f_pane, SONDAS_SUFIJO + SONDAS_PREFIJO),
        },
        "el_estrato_taino_de_esteves": {
            "topónimos_del_canon_con_la_atribución": atribuidos,
            "lo_que_ya_dice_el_repo": (
                "4-fuentes/esteves-1989.md §6: la atribución de Amuay, Elegüey, Maragüey, Jamaica y "
                "Maitiruma al «caribe insular»/taíno es de Esteves y sale de PARECIDO DE SONIDO sin "
                "documento — «por su fonética la voz pertenece al caribe insular, como batey, mamey, "
                "caney, carey» (p. 14), y esas cuatro son voces taínas del español general."),
            "lo_que_este_cruce_añade": (
                "la serie -ey de Esteves es del castellano que llegó con los españoles vía La "
                "Española, no de un contacto taíno-caquetío precolonial: batey, mamey, caney y carey "
                "entran en el castellano antillano antes de que nadie escriba un topónimo de "
                "Paraguaná. Es el mismo aviso que Oliver da para maraca, cacique y barbacoa (p. 151). "
                "Un -ey en Paraguaná mide la boca del cronista, no la lengua del sitio."),
            "y_la_etiqueta_esta_mal_puesta": (
                "el caribe insular de Breton es una lengua ARAHUACA (iñeri) con préstamos caribes en "
                "el habla de los hombres, hermana del taíno y del caquetío — ya está escrito en "
                "4-fuentes/esteves-1989.md. Una coincidencia con él es parentesco de familia."),
        },
        "los_gentilicios_en_-io_-yo": {
            "la_afirmacion": "Luca-yo, Cigüa-yo, Kaket-ío comparten un formante de etnónimo",
            "de_donde_sale": ("oliver-1989-cap2 n. 44 p. 148, y Oliver la atribuye a Gary Vescelius, "
                              "**comunicación personal de 1982**"),
            "veredicto": ("NO CITABLE como evidencia. No hay dato publicado detrás, no hay lista, y "
                          "Lucayo y Ciguayo son exónimos coloniales recogidos por cronistas. Que "
                          "`kaketío` sea `kake-` + `-(h)o` sí lo argumenta Oliver aparte, con el "
                          "lokono kakïtho (p. 148) — ese es el apoyo bueno, y no necesita a Vescelius."),
        },
    }


# ═════════════════════════════════════════════════════════════════════════
# La pregunta de clasificación
# ═════════════════════════════════════════════════════════════════════════
def bloque_clasificacion():
    return {
        "advertencia_de_entrada": (
            "El caquetío atestiguado son ~228 entradas de lexicón y ~78 topónimos sin descartar, "
            "casi todo fitonimia y zoonimia de Paraguaná y Coro recogida por Zavala. Del taíno el "
            "repo tiene 43 voces atestiguadas y **ninguna con `procedencia.obra`**. Eso NO da para "
            "una clasificación y este cruce no la intenta. Oliver, que tenía más, llama «tentative» "
            "a la suya y dice que del caquetío no hay medición porque no existe lista de 100 palabras."),
        "posiciones": [
            {"quien": "Oliver 1989 (cap. 2, pp. 150-155)",
             "que_dice": ("el caquetío sale del mismo fondo que el lokono, no de una ascendencia "
                          "guajiro-paraujana; y hace salir a lokono, island carib, taíno y caquetío "
                          "del mismo nodo"),
             "cita": "«strongest affinities with Lokono» (p. 155)",
             "en_que_se_apoya": ("DATOS: el prefijo /dA-/ de 1ª sg. (sólo lokono y taíno lo tienen), "
                                 "la innovación léxica auri 'perro', kaketío = lokono kakïtho, y "
                                 "-bana frente a -pana"),
             "y_en_que_no": ("en GEOGRAFÍA cuando descarta al guajiro: «a preliminary examination of "
                             "selected Guajira-Falcón toponyms» (p. 150) — preliminar, y sin lista"),
             "lo_llama": "«tentative» él mismo"},
            {"quien": "Noble 1965 (vía Oliver p. 97 y Rouse)",
             "que_dice": "el taíno es un vástago directo del proto-arahuaco, aislado",
             "cita": "—",
             "en_que_se_apoya": ("porcentajes de cognados sin lista publicada. Oliver: «Noble does not "
                                 "provide the actual word list(s) for Taíno, a major drawback»"),
             "y_en_que_no": "—",
             "lo_llama": "Oliver lo llama «misleading and ambiguous at the very best»"},
            {"quien": "Taylor 1977 (vía Oliver p. 97)",
             "que_dice": "el taíno deriva del proto-maipure, con 60 palabras comparadas",
             "cita": ("«Taíno appears to have [share] more lexical cognates with Island Carib than "
                      "Arawak [Lokono]», pero «borrowing cannot be excluded»"),
             "en_que_se_apoya": "DATOS, aunque pocos: una lista corta de 60 ítems",
             "y_en_que_no": "—",
             "lo_llama": "el propio Taylor deja abierto el préstamo"},
            {"quien": "Rouse 1986 (citado por Oliver p. 97)",
             "que_dice": "el taíno evolucionó del proto-norteño, como las demás del grupo",
             "cita": "«So little is known about the Taíno language that there is room for disagreement»",
             "en_que_se_apoya": "la opinión de Arróm y la escasez reconocida del dato",
             "y_en_que_no": "—",
             "lo_llama": "él mismo admite el desacuerdo"},
            {"quien": "Vescelius (comunicación personal 1982, en Oliver n. 44 p. 148)",
             "que_dice": "los etnónimos en -ío/-yo (Luca-yo, Cigüa-yo, Kaket-ío) van juntos",
             "cita": "—",
             "en_que_se_apoya": "NADA publicado: es una nota al pie de una conversación",
             "y_en_que_no": "—",
             "lo_llama": "«curious relationship»"},
        ],
        "que_puede_aportar_nuestro_material": [
            "confirmar o no que una voz caquetía atestiguada tiene pareja taína con la MISMA glosa, "
            "y de qué dominio es esa voz (que es lo que decide si el dato vale para filiación o para "
            "comercio);",
            "medir cuántas de esas parejas salen también por azar, que es lo que ninguna de las "
            "posiciones de arriba hizo;",
            "poner sobre la mesa los formantes que Oliver declara para el caquetío y que el canon del "
            "proyecto nunca recogió (-bo, -oa, -kiva), que son hueco propio antes que pregunta taína.",
        ],
        "que_NO_puede": [
            "medir distancia lexicoestadística: no hay lista de 100 palabras ni del caquetío ni del "
            "taíno, y Oliver lo dice de las dos;",
            "decidir dónde cae el caquetío en el árbol. Con 43 voces taínas sin procedencia, cualquier "
            "número que salga de aquí mide nuestras dos listas, no las dos lenguas;",
            "usar el taíno como prueba a favor o en contra de D11: el prefijo /dA-/ que comparten "
            "taíno y caquetío lo comparte también el lokono, y por eso el argumento ya está contado "
            "en D11. Contarlo otra vez por la vía taína sería contar dos veces el mismo dato.",
        ],
    }


# ═════════════════════════════════════════════════════════════════════════
# Salida
# ═════════════════════════════════════════════════════════════════════════
def ficha_de(e, cb, sim):
    d = dict(e["ficha"])
    d["comparado_como"] = cb[0] + (" (radical)" if cb[2] else "")
    d["similitud"] = round(sim, 3)
    return d


def registro(r):
    c, por = r["c"], r["por"]
    p_nulo = p_nulo_de(r, "taíno")
    clase, porque_clase = clase_de_pareja(r, p_nulo)
    reg = {"caquetio": {"forma": c["clave"],
                        **({"forma_fuente": c["forma_fuente"]} if c["forma_fuente"] else {}),
                        "capa": c["capa"], "cat": c["cat"], "categoria": c["categoria"],
                        "dominio": c["dominio"], "glosa": c["sig"],
                        "fonemizada": " / ".join(fa for fa, _ in c["cands"])},
           "conceptos_exactos": sorted({cab for cab, ex, _ in c["conceptos"] if ex})}
    if c["derivada_de"]:
        reg["caquetio"]["forma_derivada_de"] = c["derivada_de"]
    for L in TODAS:
        p = por[L]
        if p["ranking"]:
            reg[L] = [ficha_de(e, cb, s) for s, e, cb, _ca in p["ranking"][: TOPES[L]]]
            if len(p["exactas"]) > TOPES[L]:
                reg[L].append({"mas_entradas_con_la_misma_glosa": len(p["exactas"]) - TOPES[L]})
    reg["similitud"] = {L: (round(por[L]["sim"], 3) if por[L]["ranking"] else None) for L in TODAS}
    reg["veredictos"] = {L: por[L]["veredicto"] for L in TODAS}
    reg["veredicto"] = por["taíno"]["veredicto"]
    if clase:
        reg["clase"] = clase
        reg["por_que_esa_clase"] = porque_clase
    if p_nulo is not None:
        reg["p_por_azar_taino"] = round(p_nulo, 3)
    candidatas = [(por[L]["sim"], L) for L in LENGUAS
                  if por[L]["veredicto"] in ("cognado-probable", "parecido-debil")]
    reg["se_parece_mas_a"] = max(candidatas)[1] if candidatas else "ninguna"
    trozos = []
    for L in TODAS:
        p = por[L]
        if p["ranking"]:
            s, e, cb, ca = p["ranking"][0]
            barato = (" (3 fonemas: parecido barato)"
                      if s >= UMBRAL_PARECIDO and min(len(cb[0]), len(ca[0])) <= MIN_FONEMAS else "")
            trozos.append(f"{L} {cb[1]} «{str(e['glosa'])[:36]}» {s:.2f}{barato}")
        elif p["porque"] and L == "taíno":
            trozos.append(f"{L}: {p['porque']}")
    extra = [f"{L}: {por[L]['porque']}" for L in TODAS if por[L]["veredicto"] == "circular"]
    if any(e["nota_mira_al_caquetio"] for _s, e, _cb, _ca in por["taíno"]["ranking"][:1]):
        extra.append("⚠️ la `notas` de la entrada taína se escribió mirando al caquetío: "
                     "la forma es de la fuente, la comparación no es independiente")
    reg["por_que"] = ("forma caquetía de menos de tres fonemas: no cuenta como evidencia"
                      if r["corto"] else " · ".join(trozos + extra))
    return reg


def construir(M, M2, MT):
    resumen = resumir(M)
    resumen_sens = resumir(M2)
    res = M["res"]
    ates = [r for r in res if r["c"]["capa"] == ATESTIGUADO]

    clases = collections.Counter()
    letras = collections.Counter()
    parejas = []
    for r in ates:
        p_nulo = p_nulo_de(r, "taíno")
        clase, porque = clase_de_pareja(r, p_nulo)
        if not clase:
            continue
        clases[clase] += 1
        s, e, cb, ca = r["por"]["taíno"]["ranking"][0]
        # T11: el test, sobre la MISMA pareja, con ⟨gu⟩ = /w/
        fa = fon(ca[1], "colonial", GU_TEST)
        fb = fon(cb[1], "colonial", GU_TEST)
        letra, porque_t, j = test_cognado_o_prestamo(fa, fb, r["c"]["dominio"], p_nulo)
        letras[letra] += 1
        parejas.append({
            "caquetio": r["c"]["clave"], "glosa_caquetia": r["c"]["sig"],
            "taino": e["forma"], "glosa_taina": e["glosa"],
            "fuente_caquetia": (r["c"]["notas"] or "")[:160] or "sin nota",
            "fuente_taina": e["ficha"]["estrato"],
            "comparado": f"{ca[0]} ~ {cb[0]}",
            "similitud": round(s, 3), "clase": clase, "por_que": porque,
            "dominio": r["c"]["dominio"],
            "p_por_azar": round(p_nulo, 3) if p_nulo is not None else None,
            "test_T11": {"letra": letra, "esqueletos": f"{j['esqueleto_caquetio']} ~ {j['esqueleto_taino']}",
                         "por_que": porque_t,
                         "diagnosticas_presentes": j["consonantes_diagnosticas_presentes"]},
            "tambien_se_parece_en": [L for L in ("lokono", "wayunaiki", "achagua", "kalinago",
                                                 "paraujano", "jirajarano")
                                     if r["por"][L]["exactas"] and r["por"][L]["sim"] >= UMBRAL_PARECIDO],
        })
    parejas.sort(key=lambda p: (p["clase"], -p["similitud"], p["caquetio"]))

    # las circulares (capas reconstruidas): existen y no deciden
    circulares = []
    for r in res:
        for L in TODAS:
            if r["por"][L]["veredicto"] == "circular":
                s, e, cb, _ca = r["por"][L]["ranking"][0]
                circulares.append({"caquetio": r["c"]["clave"], "capa": r["c"]["capa"],
                                   "lengua": L, "comparanda": cb[1], "similitud": round(s, 3),
                                   "forma_derivada_de": r["c"]["derivada_de"]})
    circulares.sort(key=lambda d: (d["lengua"], -d["similitud"], d["caquetio"]))

    por_capa = collections.defaultdict(collections.Counter)
    for r in res:
        if r["por"]["taíno"]["exactas"]:
            por_capa[r["c"]["capa"]][r["por"]["taíno"]["veredicto"]] += 1

    taino_ates = M["lengs"]["taíno"]
    caq_ates = [r["c"] for r in ates]
    n_caq = collections.Counter(r["c"]["capa"] for r in res)
    comparables = [r for r in res if any(r["por"][L]["exactas"] for L in TODAS)]

    meta = {
        "campana": ("la campaña del taíno — T4 (2026-09-21, el cruce) y **T11** (2026-09-22, la "
                    "prueba lingüística del contacto)"),
        "medido": FECHA,
        "script": "6-fusion/scripts/cruce_taino_caquetio.py",
        "estado": ("PROPUESTA (regla 5). No toca el lexicón, ni lexicon_*.py, ni 2-lengua/, ni "
                   "3-mundo/corpus/. Ningún cognado entra a cognados.yaml por este archivo. "
                   "Toda cifra de `meta` la emite el script (regla 1)."),
        "pregunta": ("¿Qué comparten de verdad el taíno y el caquetío ATESTIGUADO —léxico, "
                     "morfología, onomástica—, y qué de eso es herencia arahuaca común, qué "
                     "préstamo por contacto en la esfera, y qué casualidad?"),
        "la_pregunta_de_T11": (
            "un cognado heredado y un préstamo por contacto SE DISTINGUEN: el cognado sigue las "
            "correspondencias regulares de sonido y el préstamo las viola, o llega sin ninguna "
            "diferencia porque cruzó tarde, o cae en un campo donde las palabras viajan. Un "
            "préstamo prueba CONTACTO; un cognado prueba PARENTESCO. Aquí se construye ese test, "
            "se controla contra lo que ya sabemos y se aplica a `datihao` y a `diao`."),
        "lo_que_cambia_respecto_del_2026_09_21": [
            "las transcripciones de T1/T2 entran como fuente taína, con obra y página — el cruce "
            "del 21 leía sólo las 43 voces del lexicón, que no citan a nadie (`insumos.transcripciones`)",
            "hay un TEST con letra (A/B/C) y sus predicciones escritas antes (`las_predicciones`)",
            "hay un CONTROL del test sobre parejas conocidas (`control_del_test`)",
            "`datihao` y `diao` tienen bloque propio y test escrito para el dato que falta",
        ],
        "antes_y_despues": bloque_antes_y_despues(),
        "el_limite_duro": {
            "que_es": ("las 52 entradas taínas del lexicón tienen 0 `procedencia.obra`. Las 43 "
                       "atestiguadas dicen «Brinton 1871» en `notas` y eso NO es una clave foránea "
                       "(regla 8): el validador no lo comprueba."),
            "taino_con_procedencia_obra": sum(
                1 for k, v in CL.VOCABULARIO_BASE.items()
                if str(v.get("fuente", "")).startswith("taíno") and v.get("procedencia")),
            "consecuencia": ("este cruce mide lo que el repo tiene HOY. Cuando entren las "
                             "transcripciones de Oviedo, Las Casas, Pané y Brinton se vuelve a "
                             "correr el script y las cifras cambian. Por eso es un script y no una "
                             "tabla."),
        },
        "por_que_solo_la_capa_atestiguada": (
            "las capas caquetío-reconstruido e -hipotético se fabricaron desde el wayuu y el lokono "
            "(arahuaco_comparative.REGLAS_*, las 441 candidatas con ~80 % de fallo). Cruzarlas con el "
            "taíno mediría el ANDAMIO, no el caquetío. Se miden y se emiten en `circulares`, y no "
            "entran en ningún resumen de filiación. Por la misma razón queda fuera `taíno-reconstruido`: "
            "9 formas que reconstruir_taino() generó desde el lokono, y cuyas propias notas dicen «no "
            "cuenta como dato taíno en cruces»."),
        "insumos": {
            "caquetio_por_capa": dict(sorted(n_caq.items())),
            "transcripciones": dict(
                M["transcripciones"],
                que_es=("lo que entró el 2026-09-21 por los PR #189-#192 y el cruce de ese día no "
                        "leía. `bitacora_de_glosas` es el inventario ENTERO de lo que el extractor "
                        "sacó de cada cita y de lo que no pudo sacar: se audita a ojo (regla 6), "
                        "porque una glosa mal sacada fabrica una pareja falsa."),
                de_donde=[s["archivo"] for s in YAML_TAINO]),
            "taino_atestiguado_usado": len(taino_ates),
            "taino_reconstruido_excluido": sum(
                1 for v in CL.VOCABULARIO_BASE.values() if v.get("fuente") == "taíno-reconstruido"),
            "taino_gemelas_castellanas_fusionadas": sorted(CL.FORMA_DE_LA_ESFERA),
            "taino_con_nota_escrita_mirando_al_caquetio": sorted(
                e["forma"] for e in taino_ates if e["nota_mira_al_caquetio"]),
            "taino_con_marca_castellana_declarada": sorted(
                e["forma"] for e in taino_ates if e["ficha"].get("marca_castellana")),
            **{f"{L}_entradas": len(M["lengs"][L]) for L in LENGUAS[1:] + INFORMATIVAS},
            "control_jirajarano": dict(M["meta_control"],
                                       filas_con_forma_comparable=len(M["lengs"][CONTROL])),
            "lo_que_NO_sirvio_de_control": medir_jirajaroide_frontera(),
        },
        "parametros": {
            "umbral_parecido": UMBRAL_PARECIDO, "umbral_cognado": UMBRAL_COGNADO,
            "min_fonemas": MIN_FONEMAS, "replicas_del_modelo_nulo": REPLICAS, "semilla": SEMILLA,
            "gu_es_w": GU_ES_W,
            "similitud": "difflib.SequenceMatcher.ratio() sobre la forma fonemizada",
            "afijos_probados": {L: {"prefijos": list(p), "sufijos": list(s)}
                                for L, (p, s) in sorted(AFIJOS.items())},
            "sinonimos_de_glosa": SINONIMOS_CRUDOS,
            "dominio_por_categoria": DOMINIO_POR_CATEGORIA,
            "de_donde_sale_la_tabla_de_dominios": (
                "skill minar-fuente §3, que viene de la corrección de Miguel del 2026-09-10: «hay "
                "palabras que pueden compartirse entre etnias». Lo que decide no es SI se comparte, "
                "sino QUÉ: plantas, bichos, mercancías y utensilios viajan entre lenguas sin "
                "parentesco (préstamo areal); pronombres, numerales y morfemas gramaticales casi "
                "nunca (dato de filiación)."),
        },
        "metodo": [
            "FILTRO DE SIGNIFICADO: se empareja por glosa castellana EXACTA (el segmento es una sola "
            "palabra en los dos lados, tras normalizar la ortografía colonial). Un parecido de forma "
            "sin filtro de significado es casi todo ruido: medido 5 falsos de 7 en el achagua.",
            "MIRAR LA CAPA: sólo la capa caquetío-atestiguado decide; las reconstruidas se emiten "
            "aparte como circulares. Y las entradas taínas cuya `notas` se escribió comparándolas con "
            "el caquetío llevan aviso — la forma es de la fuente, la comparación no es independiente.",
            "LA CLASE NO LA DECIDE EL PARECIDO: el parecido sólo abre la candidatura. La clase la "
            "deciden el DOMINIO de la voz y si el mismo concepto se parece también en las hermanas.",
            "DESCONFIAR: modelo nulo por permutación, control no arahuaco (jirajara/ayomán) y prueba "
            "de predicción dejando fuera. Una correspondencia con 1 o 2 apoyos no es una regla.",
        ],
        "capas_de_medicion": [
            "diacríticos fuera salvo ü y ñ (sin esto fonemizar borraba ū, ẽ, ë enteras)",
            "ortografía lingüística (lokono, wayuu, reconstruido): la h suelta pasa a j, porque "
            "fonemizar borra la h castellana",
            "curiana_fonotactica.fonemizar(); OJO: lleva <ch> a k y <sh> a s en todas por igual",
            "forma_comparable() colapsa las geminadas de Perea; se colapsan las repeticiones y ü -> u",
            "las cuatro claves castellanas con gemela indígena (casabe/cazabi, maíz/maisi, "
            "cacique/cacike, bohío/bohio) entran UNA vez, por la indígena: FORMA_DE_LA_ESFERA",
        ],
        "advertencias": [
            "Un parecido de forma con glosa exacta es un CANDIDATO a cognado, no un cognado. Ninguna "
            "de estas parejas ha pasado por correspondencias regulares verificadas.",
            "Las listas son cortas y muy distintas de dominio: el caquetío atestiguado es fitonimia y "
            "zoonimia de Paraguaná y Coro, y la lista taína de Brinton excluye a propósito «nearly "
            "all names of plants and animals» (p. impresa 11). El hueco mide las listas, no las lenguas.",
            "Los tainismos son préstamos panamericanos que llegaron con el castellano vía La Española. "
            "Oliver lo avisa para maraca, cacique y barbacoa (p. 151): «one must be careful about some "
            "terms offered by the Spanish as 'native' Caquetío».",
            "El caquetío atestiguado y el taíno de Brinton están los dos en ortografía castellana "
            "colonial: parte del parecido que salga es del transcriptor español, no de las lenguas. "
            "fonemizar() normaliza lo que puede y no lo resuelve.",
        ],
        "resumen_atestiguado": resumen,
        # ── T11 ─────────────────────────────────────────────────────────
        "las_predicciones": bloque_las_predicciones(),
        "P1_puesta_a_prueba_sobre_el_corpus": medir_tasa_de_erre(MT),
        "control_del_test": bloque_control_del_test(MT, GU_TEST),
        "reparto_por_letra_del_test": dict(sorted(letras.items())) or {
            "sin_parejas": "no hay ninguna pareja que clasificar: ver `auditoria_del_cero`"},
        "el_caso_datihao": bloque_datihao(GU_TEST),
        "la_pregunta_diao": bloque_diao(MT, GU_TEST),
        "morfemas_compartidos_son_filiacion_no_contacto": bloque_morfemas_filiacion_no_contacto(MT),
        "la_otra_orilla_estaba_en_casa": bloque_la_otra_orilla(),
        "el_eje_prosodico_que_viene": bloque_el_eje_prosodico(),
        # ────────────────────────────────────────────────────────────────
        "reparto_por_clase": dict(sorted(clases.items())) or {
            "sin_parejas": ("ninguna voz caquetía atestiguada alcanza el umbral con una voz taína "
                            "de la misma glosa: no hay nada que clasificar. Ver "
                            "`auditoria_del_cero`, que es donde está el resultado.")},
        "auditoria_del_cero": {
            "por_que_este_bloque": (
                "regla 6: un cero mide la consulta hasta que se verifica. Con cuatro conceptos "
                "comparables, los cuatro casos SON el resultado y van uno a uno; y hay que decir "
                "qué descartó el filtro y qué tiene el canon que el cruce no ve."),
            "los_conceptos_comparables_uno_a_uno": bloque_los_comparables(M),
            "descartados_por_glosa_solo_cercana": bloque_glosa_cercana(M),
            "cognados_CQ_TN_ya_declarados_en_el_canon": bloque_cognados_ya_declarados(GU_ES_W),
            "hallazgos_de_etiqueta": bloque_hallazgos_de_etiqueta(GU_ES_W),
            "paso_por_forma_sin_filtro_de_glosa": paso_por_forma(M, GU_ES_W),
        },
        "sensibilidad_gu_es_w_true": {
            L: {k: resumen_sens["por_lengua"][L].get(k)
                for k in ("conceptos_comparables", "parecidos_ge_umbral",
                          "cognado_probable_ge_umbral_cognado")}
            | {"parecidos_esperados": resumen_sens["por_lengua"][L].get("azar", {}).get("parecidos_esperados")}
            for L in TODAS},
        "veredicto_taino_por_capa": {k: dict(sorted(v.items())) for k, v in sorted(por_capa.items())},
        "morfologia": bloque_morfologia(M, caq_ates, taino_ates),
        "onomastica": bloque_onomastica(),
        "clasificacion": bloque_clasificacion(),
        "prueba_de_prediccion": prueba_dejando_fuera(M, ("taíno", "lokono", "wayunaiki", "achagua")),
        "circulares": circulares,
        "registros": {
            "conceptos_con_glosa_exacta_en_alguna_lengua": len(comparables),
            "sin_concepto_en_ninguna_comparanda": len(res) - len(comparables),
        },
    }
    rango = {"cognado-probable": 0, "parecido-debil": 1, "circular": 2,
             "sin-parecido": 3, "no-comparable": 4}
    comparables.sort(key=lambda r: (r["c"]["capa"] != ATESTIGUADO, r["c"]["capa"],
                                    rango[r["por"]["taíno"]["veredicto"]],
                                    -r["por"]["taíno"]["sim"], r["c"]["clave"]))
    return {"meta": meta, "parejas": parejas, "conceptos": [registro(r) for r in comparables]}


CABECERA = (
    "# ══════════════════════════════════════════════════════════════════════\n"
    "# CRUCE TAÍNO <-> CAQUETÍO ATESTIGUADO + LA PRUEBA LINGÜÍSTICA DEL\n"
    "# CONTACTO — campaña del taíno, parcelas T4 (09-21) y T11 (09-22).\n"
    "# PROPUESTA (regla 5). Generado por 6-fusion/scripts/cruce_taino_caquetio.py:\n"
    "# no se edita a mano; se corrige el script o sus insumos y se regenera.\n"
    "# Toda cifra de `meta` la emite el script (regla 1).\n"
    "# Re-ejecutable: cuando llegue la forma de Oviedo tomo II/IV o una segunda\n"
    "# copia de la impresa 473 con imagen, se vuelve a correr y el test de\n"
    "# `meta.el_caso_datihao` se resuelve solo.\n"
    "# El YAML del 2026-09-21 NO se toca: es el «antes», y este script lo lee.\n"
    "# ══════════════════════════════════════════════════════════════════════\n"
)


def texto_yaml(salida):
    buf = io.StringIO()
    buf.write(CABECERA)
    yaml.safe_dump(salida, buf, allow_unicode=True, sort_keys=False, width=110)
    return buf.getvalue()


def consola(salida):
    m = salida["meta"]
    print("\n═══ RESUMEN, capa caquetío-atestiguado ═══")
    for L, d in m["resumen_atestiguado"]["por_lengua"].items():
        az = d.get("azar", {})
        print(f"  {L:<12} entradas {d['entradas_de_la_lengua']:>5} · comparables {d['conceptos_comparables']:>3}"
              f" · parecidos {d['parecidos_ge_umbral']:>2} (azar {az.get('parecidos_esperados')},"
              f" p={az.get('p_parecidos_ge_observado')}) · cognado-probable {d['cognado_probable_ge_umbral_cognado']}"
              f" · sim media {d['similitud_media']} (azar {az.get('similitud_media_esperada')})")
    print(f"\n  reparto por clase: {list(m['reparto_por_clase'])}")
    print("\n═══ PAREJAS TAÍNO ~ CAQUETÍO ATESTIGUADO ═══")
    for p in salida["parejas"]:
        print(f"  [{p['clase']:<18}] {p['caquetio']:<12} «{str(p['glosa_caquetia'])[:26]:<26}» ~ "
              f"{p['taino']:<12} {p['similitud']:.2f}  azar p={p['p_por_azar']}  "
              f"también: {','.join(p['tambien_se_parece_en']) or '—'}")
    aud = m["auditoria_del_cero"]
    print("\n═══ AUDITORÍA DEL CERO ═══")
    for d in aud["los_conceptos_comparables_uno_a_uno"]:
        print(f"  {d['concepto']} · caq {d['caquetio']:<10} ~ tno {d['taino']:<10} {d['similitud']:.2f}")
    print(f"  descartados por glosa sólo cercana: {len(aud['descartados_por_glosa_solo_cercana'])}")
    cg = aud["cognados_CQ_TN_ya_declarados_en_el_canon"]
    print(f"  cognados.yaml ya empareja CQ~TN en {cg['sets_con_CQ_y_TN']} sets: {cg['reparto']}")
    he = aud["hallazgos_de_etiqueta"]
    print(f"  «Taíno atestiguado» en taino_hipotetico.json sin la etiqueta taíno en el lexicón: "
          f"{he['de_esas_sin_la_etiqueta_taino_en_el_lexicon']} de "
          f"{he['declaradas_atestiguadas_en_el_json']}")
    print("  paso por forma (sin filtro de glosa):")
    for L, d in aud["paso_por_forma_sin_filtro_de_glosa"]["por_lengua"].items():
        print(f"    {L:<12} parejas {d['parejas_de_forma_ge_umbral']:>3} · con glosa "
              f"{d['de_esas_con_la_glosa_tambien']:>2} · ruido {d['ruido']:>3}")
    print("\n═══ MORFOLOGÍA ═══")
    for f in m["morfologia"]["filas"]:
        print(f"  {f['morfema_caquetio']:<44} {f['veredicto']}")
    print("\n═══ PREDICCIÓN (dejando fuera) ═══")
    for L in ("taíno", "lokono", "wayunaiki", "achagua"):
        b = m["prueba_de_prediccion"][L]
        print(f"  [{L}] {b['pares_parecidos']} pares parecidos · {b['correspondencias_distintas']} "
              f"correspondencias · {b['con_tres_apoyos_o_mas']} con 3 apoyos o más")
        for rg in b["reglas"][:4]:
            print(f"    {rg['regla']:<18} apoyos {rg['apoyos']} · {rg['aciertos']}/{rg['aplicables']}"
                  f" (tasa {rg['tasa_de_acierto']}, azar {rg['tasa_por_azar']}) · {rg['juicio'][:60]}")

    tr = m["insumos"]["transcripciones"]
    print("\n═══ T11 · LAS TRANSCRIPCIONES QUE ENTRAN HOY ═══")
    print(f"  lexicón {tr['entradas_del_lexicon']} + transcripciones "
          f"{tr['entradas_de_las_transcripciones']} → {tr['tras_fundir_la_misma_voz']} voces taínas"
          f" ({tr['con_obra_y_pagina']} con obra y página, {tr['sin_clave_foranea']} sin)")
    print(f"  descartadas: {tr['descartadas_por']}")

    print("\n═══ T11 · P1 SOBRE EL CORPUS (la tasa de /r/) ═══")
    for L, d in m["P1_puesta_a_prueba_sobre_el_corpus"]["por_lista"].items():
        print(f"  {L:<22} formas {d['formas']:>5} · /r/ {d['r']:>4}/{d['consonantes']:<5} "
              f"= {d['tasa_de_r']} · /w/ {d['tasa_de_w']}")

    c = m["control_del_test"]
    print("\n═══ T11 · CONTROL DEL TEST ═══")
    for k in ("a_heredadas_caquetio_lokono", "b_prestadas_taino_castellano",
              "c_no_pariente_caquetio_jirajarano"):
        r_ = c[k]["resumen"]
        print(f"  {k:<36} n={r_['n']:>3} {r_['reparto']} · aciertos {r_['aciertos']} · fallos {r_['fallos']}")
    print(f"  → {c['veredicto_del_test'][:150]}")

    print("\n═══ T11 · EL CASO datihao ═══")
    for p in m["el_caso_datihao"]["el_test_aplicado_a_lo_que_hay"]:
        print(f"  [{p['letra']}] {p['pareja']}  ({p['esqueletos']})")
    print("\n═══ T11 · LA PREGUNTA diao ═══")
    d = m["la_pregunta_diao"]["y_la_pregunta_taina_medida"]
    print(f"  {d['respuesta'][:220]}")
    cr = m["la_pregunta_diao"]["el_campo_de_rango_lado_a_lado"]
    print(f"  campo de rango: caq {len(cr['caquetio_atestiguado'])} · taí {len(cr['taino'])} · "
          f"parejas sobre el umbral {len(cr['parejas_sobre_el_umbral_con_el_test_aplicado'])}")
    print(f"\n  reparto por letra del test: {m['reparto_por_letra_del_test']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true",
                    help="no escribe: dice si el YAML del repo está al día")
    args = ap.parse_args(argv)

    print("midiendo (gu_es_w=False) ...")
    M = medir(GU_ES_W)
    print(f"  {M['segundos']} s")
    print("midiendo la sensibilidad (gu_es_w=True) ...")
    M2 = medir(not GU_ES_W)
    print(f"  {M2['segundos']} s")
    # el test corre sobre la fonemización con ⟨gu⟩ = /w/
    MT = M2 if GU_TEST == (not GU_ES_W) else M

    salida = construir(M, M2, MT)
    nuevo = texto_yaml(salida)

    if args.check:
        viejo = io.open(SALIDA, encoding="utf-8").read() if os.path.exists(SALIDA) else ""
        if viejo == nuevo:
            print(f"\n✓ {os.path.relpath(SALIDA, R)} está al día")
            return 0
        print(f"\n✗ {os.path.relpath(SALIDA, R)} DESFASADO: re-ejecuta el script sin --check")
        return 1

    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(nuevo)
    consola(salida)
    print(f"\n✓ {os.path.relpath(SALIDA, R)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
