# -*- coding: utf-8 -*-
"""
CURIANA — D10: qué se hace con las 16 entradas que la minería contradijo
========================================================================

`auditar_82.py` deja 19 entradas de familia caquetía sin cita. Tres son
SIN_RASTRO real (`kama`, `koke`, `wabarsure`) y se quedan como están. Las
otras **16** tienen una fuente que dice algo en contra, y **no son
homogéneas**: por eso D10 no es una política, son tres.

Este script las aplica. No toca fichas de agente, ni el canon
(`CULTURA_CAQUETIA.md`), ni `cultura/*.yaml`, ni los cuatro módulos de
propuesta. Solo `curiana_lexicon.py`.

    python aplicar_d10.py --dry-run   # informe, no escribe
    python aplicar_d10.py             # aplica

Idempotente: cada cambio comprueba primero si ya está hecho.


GRUPO 1 — la fuente nombra otra lengua → se reasigna `fuente`  (8)
------------------------------------------------------------------
La etiqueta pasa a la lengua que la fuente indica, para que
`score_linguistico()` las trate como ajenas al caquetío (vía
`_familia_de_token` → `normalize_source_language`). **La forma y la entrada se
conservan**: siguen siendo vocabulario del mundo, solo que prestado — igual que
el wayunaiki o el taíno que ya vive en el lexicón.

Dos etiquetas de `fuente` son nuevas y hubo que darlas de alta en
`curiana_database.normalize_source_language()`:

  · `caribe-cháima` / `caribe-cumanagoto` → categoría **`caribe-continental`**
    Nombre elegido por coherencia con las que ya existían: el lexicón ya
    distinguía `kalinago` (caribe insular) y `kalinago-caribe-overlay`. Lo que
    faltaba era el caribe de tierra firme — cháima, cumanagoto, tamanaco —, que
    es de donde Alvarado hace venir estas voces. El sufijo `-continental` es
    justamente lo que lo separa del `kalinago` insular ya presente.

  · `español-colonial` → categoría **`español-colonial`**
    Para las voces que la fuente declara castellanas frente a un nombre
    indígena distinto. No se pueden dejar caer en el `return` por defecto
    (`proto-arahuaco`): serían contadas como arahuacas.

GRUPO 2 — conflicto de glosa → se corrige la glosa, se conserva la palabra (6)
-----------------------------------------------------------------------------
La palabra es caquetía; lo que estaba mal es qué significa. Se aplica **D7**:
la glosa de la fuente, verbatim, va a `glosa_fuente`; la lectura que se
descarta queda registrada en `notas`. Nada se pierde en silencio.

⚠ **Tres no se reescriben** (`tara`, `saruro`, `corie`). Instrucción explícita
de D10: si no aparece fuente para la glosa **actual**, no se la sustituye por
la de Zavala en silencio. Se investigó y **no aparece** — ni en Alvarado, ni en
van Buurt, ni en Gatschet. Pero las tres sostienen material del canon
(`Saruro-sha`, `Korie-ko`, el corpus ecológico), así que la entrada se queda
con la glosa que tiene y una `notas` que deja el conflicto **abierto y
visible**. Un conflicto documentado es mejor que una corrección inventada.

GRUPO 3 — solo bajada de tier → `caquetío-hipotético`  (2)
-----------------------------------------------------------
`tata` y `coro` no cambian de lengua: la fuente no las reasigna, solo retira el
respaldo. La etiqueta nueva `caquetío-hipotético` sigue normalizando a
`caquetío` — eso es deliberado: la **lengua** no se discute, solo baja la
**confianza**. Por eso no se implementó como una categoría nueva de scoring.


El caso aparte: `piache` sale del habla
---------------------------------------
Decisión adicional de Miguel. `piache` es caribe (Alvarado 1921 p.248: *voz
cháima y tamanaca*) y además, en el glosario de Zavala, es la **glosa española**
de `boratio` (#43, AM+HB), que es la voz caquetía atestiguada del mismo oficio.
Así que no basta con reasignarle la lengua: se retira del habla y `boratio`
ocupa su lugar.

«Retirar» aquí significa: **sale de `VOCABULARIO_BASE`** (deja de ser palabra
activa, deja de sembrarse en Supabase, deja de aparecer en los prompts) y
**pasa a `FUERA_DEL_HABLA`**, un diccionario nuevo al final del módulo que
conserva la entrada entera con su procedencia. No se borra: se archiva. Es el
mismo criterio con que Zavala dejó `hay`, `enea` y `guata` fuera del habla.

**Nada del canon se toca.** El rol de Shaboro sigue siendo el de piache y su
ficha no se modifica. Queda pendiente —y se reporta, no se ejecuta— que
`curiana_koine.FORMAS_SEED` siembra la forma «piache» a Shaboro y a Buio-sha.


Lo que este script NO decide
----------------------------
Tres de las 16 llegaron a D10 descritas como «glosa actual sin fuente», y la
verificación mostró que **sí la tienen** (`cumaragua` #93 F, `bureche` #49 F,
`guanepe` #137 F, todas en la sección A de Zavala). La decisión de Miguel se
aplica igual —él adjudica a favor de Alvarado— pero la lectura de Zavala viaja
entera en `notas`, porque D7 exige que las dos queden registradas. Ver el
informe de la sesión.
"""

import argparse
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LEXICON_FILE = os.path.join(AQUI, "curiana_lexicon.py")

# El bloque FUERA_DEL_HABLA se inserta justo antes de esta función, que es el
# último punto de nivel de módulo estable del archivo.
ANCLA_FUERA = "def _familia_de_token(tok: str) -> str:"

A = "Alvarado 1921"
Z = "Zavala Reyes 2015"
VB = "van Buurt 2014"


# ══════════════════════════════════════════════════════════════════════
# GRUPO 1 — reasignación de lengua (la forma y la entrada se conservan)
# ══════════════════════════════════════════════════════════════════════
GRUPO_1 = {
    "ture": {
        "fuente": "caribe-cháima",
        "sig": "asiento pequeño de madera",
        "glosa_fuente": "Asiento pequeño de forma particular. Us. en Cumaná y Margarita. Es lo mismo que el butaque de Occidente. Voz cháima, que Tauste traduce: asiento pequeño de madera [%s p.301 s.v. TURE]" % A,
        "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A CARIBE CONTINENTAL Y GLOSA CORREGIDA. %s p.301 la da como voz cháima (Tauste), usada en Cumaná y Margarita, y con la glosa de asiento, no de vasija. Doble error: lengua y referente. Lectura que se descarta: %s glosario #259 (AM) «Vasija, utensilio», fuerza F — queda registrada aquí por D7, no se pierde" % (A, Z),
    },
    "pauji": {
        "fuente": "caribe-cháima",
        "sig": "árbol espinoso de fruto pequeño (Bumelia buxifolia)",
        "glosa_fuente": "Bumelia buxifolia. Sapotáceas. Árbol espinoso, de hojas elípticas... [%s p.244 s.v. PAUJÍ; cf. p.175 s.v. IGÜÍ: «Bumelia buxifolia, árbol maderable. Paují, Malarmo. Coro»]" % A,
        "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A CARIBE CONTINENTAL Y GLOSA CORREGIDA. En %s p.244 paují es un ÁRBOL derivado del chaima, no el ave. Y %s sección D lo confirma por otra vía: su glosario #197 glosa el caquetío «paugis» como 'paují' — es decir, paují es la palabra ESPAÑOLA y paugis la caquetía (la que lleva la agente Paugis-sha). El ave sigue teniendo nombre propio en el lexicón; lo que sale del caquetío es la forma española" % (A, Z),
    },
    "watapana": {
        "fuente": "caribe-cumanagoto",
        "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A CARIBE CONTINENTAL. %s p.163 s.v. GUATAPANAR: «Caesalpinia coriaria. Dividive. Del cum. araguatapanár, oreja de araguato, por la forma del fruto»; entre los guayuncomos del Alto Orinoco, arauotá-fanári es nombre propio. CONFLICTO DE FILIACIÓN NO CERRADO, y viaja aquí a propósito: %s §6 la lista entre las «words likely to be of Caquetío origin» (islas A/B/C) con etimología arahuaca interna (-apana = hojas, wa-/wu- pluralidad), y Gatschet 1885 (material Pinart, Aruba 1882) la registra con taxón. D10 adjudica a Alvarado para la forma continental; la vertiente insular sigue siendo argumento vivo" % (A, VB),
    },
    "auyama": {
        "fuente": "caribe-cumanagoto",
        "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A CARIBE CONTINENTAL. %s p.16 s.v. AUYAMA: «Voz cum. que Ruiz Blanco traslada 'calabaza'», con variantes ayuyáma y huyáma y la cita de Castellanos (Cabo de la Vela). Familia caribe, no arahuaca. %s no la tiene (su sección E la da por ausente) y Gatschet tampoco: el papiamento usa pampuna, y ahullama aparece solo como voz española del guía de conversación" % (A, Z),
    },
    "kunuku": {
        "fuente": "taíno",
        "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A TAÍNO. %s p.89 s.v. CONUCO: «Voz taina», citando a Las Casas V.307 («esta labranza, en lenguaje de los indios desta isla, se llama conuco»). %s lo dice igual en prosa: kanoa, komehein, kunuku, maïshi, pita y sabana derivan del taíno. Gatschet la trae, pero por la sección de PAPIAMENTO del artículo (Guía de Curazao 1876), no por la lista arubana: kunuku es la forma papiamenta del conuco taíno, no un caquetío insular" % (A, VB),
    },
    "kukuisa": {
        "fuente": "español-colonial",
        "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A ESPAÑOL. %s p.84 s.v. COCUIZA (Furcraea spp.) cita a Caulín I.3: «una especie de pita que los indios llaman CARUATA y los españoles COCUIZA». La fuente separa las dos lenguas en la misma frase: el nombre indígena es caruata (voz cháima; tam. karuatá, cum. karúata) y cocuiza/kukuisa es el castellano. La entrada venía marcada «caquetío/topónimo»: el valor toponímico no se discute y se conserva en esta nota, pero no sostiene la filiación léxica" % A,
    },
    "caraota": {
        "fuente": "español-colonial",
        "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A ESPAÑOL. %s p.58 s.v. CARAOTA la describe como el nombre corriente panvenezolano de las judías (Phaseolus, Canavalia, Pachyrrhizus), sin declararle origen indígena. Y %s sección D la cierra: su glosario #162 glosa el caquetío «icoroata» como 'caraota' — caraota es la GLOSA española, icoroata la voz caquetía" % (A, Z),
    },
}

# `piache` es del grupo 1 en cuanto a lengua, pero además SALE DEL HABLA.
PIACHE = {
    "sig": "chamán, curandero, intermediario espiritual",
    "cat": "sust",
    "fuente": "caribe-cháima",
    "notas": "D10 (2026-08-03) — RETIRADA DEL HABLA; su lugar lo ocupa `boratio`. %s p.248 s.v. PIACHE: «Sacerdote indígena, que, según los casos, era al mismo tiempo brujo, hechicero o herbolario... Voz cháima y tamanaca, con formas afines en otras lenguas caribes» (cita a Aguado I.458). %s lo confirma por otra vía: su glosario #43 (AM+HB) glosa el caquetío «boratio» COMO 'piache, cacique, jefe, sacerdote, médico' — piache es la glosa española, boratio la voz caquetía, ya en el lexicón con su cita (Arcaya 1920:116; Oviedo vía Jahn 1927:213 n.29). La sección D de Zavala la adjudica al cumanagoto y Alvarado al cháima: ambas caribe continental, difieren en cuál. La entrada NO se borra, se archiva aquí con su procedencia. El canon no se toca: Shaboro sigue siendo el piache de la Curiana" % (A, Z),
}


# ══════════════════════════════════════════════════════════════════════
# GRUPO 2 — conflicto de glosa (D7: la lectura descartada queda en `notas`)
# ══════════════════════════════════════════════════════════════════════
GRUPO_2 = {
    "cumaragua": {
        "sig": "caracol de las costas de Paraguaná",
        "glosa_fuente": "Especie de caracol de las costas de Paraguaná [%s p.102 s.v. CUMARAGUA]" % A,
        "notas": "D10 (2026-08-03), grupo 2 — GLOSA CORREGIDA, la palabra sigue siendo caquetía. %s p.102 es la localización más precisa de todo su glosario para una voz de esta lista: costas de Paraguaná. PREMISA CORREGIDA: la glosa anterior NO estaba sin fuente. La lectura que se descarta —%s glosario #93 (HB+E) «Ciruela, espuma rosada», fuerza F, y Arcaya 1920 sobre la Relación de Barquisimeto 1579 («mene y cumaragua nombre de la ciruela»)— queda registrada aquí íntegra por D7. Las dos son fuentes históricas y ninguna es moderna: el conflicto es real y D10 adjudica por localización" % (A, Z),
    },
    "bureche": {
        "sig": "bebida fermentada de casabe",
        "cat": "sust",
        "glosa_fuente": "Bebida fermentada que preparan los indios guayaneses poniendo por cierto tiempo en agua caliente el casabe [%s p.34 s.v. BURECHE]" % A,
        "notas": "D10 (2026-08-03), grupo 2 — GLOSA CORREGIDA y `cat` cambiada de v_raiz a sust: una bebida no toma sufijos de aspecto. PREMISA CORREGIDA: la glosa anterior NO estaba sin fuente — %s glosario #49 (AM) da bureche = «Hacer, realizar» con fuerza F, que es exactamente lo que el lexicón traía; queda registrado aquí por D7. DOS RESERVAS que la sesión reporta y no resuelve: (1) el lexicón ya tiene `buriche` (%s #50, AM: «Licor fermentado»), de modo que esta corrección crea un cuasi-duplicado y habrá que decidir si bureche y buriche son la misma entrada; (2) Alvarado localiza su bureche en GUAYANA, no en Coro" % (Z, Z),
    },
    "guanepe": {
        "glosa_fuente": "Así llaman en Barcelona y Guayana una especie de cabestrillo o charpa en que las madres indígenas llevan sus niños de pecho cuando viajan [%s p.152 s.v. GUANEPE]" % A,
        "notas": "D10 (2026-08-03), grupo 2 — LA GLOSA SE CONSERVA: %s p.152 la CONFIRMA palabra por palabra, y %s glosario #137 (E) la respalda («Cesto para cargar a los niños», fuerza F). Lo que Alvarado desmiente no es el significado sino la GEOGRAFÍA: la localiza en Barcelona y Guayana, oriente caribe, no en Coro. La reserva es geográfica, no semántica, y por eso la entrada no cambia de etiqueta: queda anotada" % (A, Z),
    },
    # — Las tres que NO se reescriben. Solo `notas`. —
    "tara": {
        "notas": "D10 (2026-08-03), grupo 2 — CONFLICTO DE GLOSA ABIERTO, la entrada NO se reescribe. La glosa activa («venado, ciervo») no tiene fuente localizada: no está en %s, ni en %s, ni como lema en %s. En contra hay DOS fuentes independientes que coinciden: %s glosario #238 (HB+PMA+AM) «Langosta, mariposa», y %s p.283, donde tara vale polilla o mariposa (cf. TARÍTA, «mariposa o tara pequeña»). Es el más fuerte de los tres conflictos y el único con doble corroboración. No se toca aquí porque la lectura de venado sostiene material del corpus ecológico (cultura/ecologia.yaml, ensayo 02 §10.6, diseño 02): corregirla obliga a tocar el canon, y eso es decisión de Miguel" % (Z, VB, A, Z, A),
    },
    "saruro": {
        "notas": "D10 (2026-08-03), grupo 2 — CONFLICTO DE GLOSA ABIERTO, la entrada NO se reescribe. La glosa activa («árbol saruro») no tiene fuente localizada: %s no la trae ni como lema ni como mención, %s no la tiene, Gatschet tampoco. Su único rastro en el repo es una lista de Notion (Venezolanismos de Origen Indígena) citada en DISENO_KOINE §8, y allí se usa para confirmar la terminación -aro/-uro, NO para sostener la glosa. En contra: %s glosario #224 (E) «Serpiente no venenosa. Boa constrictora». No se toca aquí porque saruro da nombre a la agente Saruro-sha y aparece en el vocabulario de Shaboro" % (A, VB, Z),
    },
    "corie": {
        "notas": "D10 (2026-08-03), grupo 2 — CONFLICTO DE GLOSA ABIERTO, la entrada NO se reescribe. La glosa activa («choza, habitación») no tiene fuente localizada: ausente de %s (ni lema ni mención) y de %s. En contra, %s glosario #90 (HB) «Armadillo» — y el propio CANON del proyecto ya dice armadillo: cultura/genealogia.yaml da «corie (armadillo)» como tótem del linaje Paugis, y la ficha de Buio-sha usa «corie (armadillo) como elogio». Es decir: la glosa del lexicón contradice a la fuente Y a su propio canon a la vez. No se toca aquí porque corie da nombre a Korie-ko" % (A, VB, Z),
    },
}


# ══════════════════════════════════════════════════════════════════════
# GRUPO 3 — bajada de tier, sin cambio de lengua
# ══════════════════════════════════════════════════════════════════════
GRUPO_3 = {
    "tata": {
        "fuente": "caquetío-hipotético",
        "notas": "D10 (2026-08-03), grupo 3 — BAJA DE TIER, no cambia de lengua. %s la trae en su §11, «words with less certain links to Caquetío» (islas A/B/C, 'father'), NO en su §6 de voces probablemente caquetías: la propia fuente la coloca en la lista de menor confianza. %s glosario #243 (AM) «Padre, papá» la marca con fuerza D porque tata es panhispánico infantil, y %s p.71 solo la registra en 'tata-cuá' (indígenas de Mérida). Ninguna la reasigna a otra lengua; lo que ninguna sostiene es la certeza" % (VB, Z, A),
    },
    "coro": {
        "fuente": "caquetío-hipotético/topónimo",
        "notas": "D10 (2026-08-03), grupo 3 — BAJA DE TIER, no cambia de lengua. La glosa «cardón grande» NO sale de ninguna fuente localizada. %s sección D lo dice explícitamente: su #181 es Koro = «Cotorra» (ya en el lexicón como entrada aparte, con su cita), no cardón. En %s la palabra coro aparece 55 veces y siempre como TOPÓNIMO: no hay lema CORO con glosa de cardón. %s solo la menciona como la ciudad. La entrada NO se borra y el canon NO se toca: coro da nombre a la ciudad de Coro y aparece en todo el sitio público. Lo que se retira es el respaldo de la glosa, no la palabra" % (Z, A, VB),
    },
}


# ══════════════════════════════════════════════════════════════════════
# Mecánica
# ══════════════════════════════════════════════════════════════════════

def _forzar_utf8():
    """La consola de Windows es cp1252 y revienta con « o ü."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


def _entrada(contenido, clave):
    """Span del dict literal de una entrada del lexicón, o None."""
    patron = re.compile(r'^(\s*"' + re.escape(clave) + r'":\s*\{)([^}]*?)(\})',
                        re.MULTILINE)
    return patron.search(contenido)


def _set_campo(cuerpo, campo, valor):
    """Escribe (o reescribe) un campo del dict literal. Devuelve (cuerpo, cambió)."""
    if '"' in valor or "}" in valor:
        raise ValueError("valor con comilla o llave, rompería el módulo: %r" % valor[:40])
    m = re.search(r'"%s":\s*"([^"]*)"' % re.escape(campo), cuerpo)
    if m:
        if m.group(1) == valor:
            return cuerpo, False
        return cuerpo[:m.start(1)] + valor + cuerpo[m.end(1):], True
    nuevo = cuerpo.rstrip()
    if not nuevo.endswith(","):
        nuevo += ","
    return nuevo + ' "%s": "%s"' % (campo, valor), True


def aplicar_campos(contenido, tabla, etiqueta):
    """Aplica un grupo. Devuelve (contenido, cambiadas, sin_cambio, ausentes)."""
    cambiadas, sin_cambio, ausentes = [], [], []
    for clave, campos in sorted(tabla.items()):
        m = _entrada(contenido, clave)
        if not m:
            ausentes.append(clave)
            continue
        cuerpo, toco = m.group(2), False
        for campo, valor in campos.items():
            cuerpo, c = _set_campo(cuerpo, campo, valor)
            toco = toco or c
        if not toco:
            sin_cambio.append(clave)
            continue
        contenido = (contenido[:m.start()] + m.group(1) + cuerpo + m.group(3)
                     + contenido[m.end():])
        cambiadas.append(clave)
    return contenido, cambiadas, sin_cambio, ausentes


def _literal_entrada(clave, campos):
    partes = ", ".join('"%s": "%s"' % (k, v) for k, v in campos.items())
    return '    "%s": {%s},\n' % (clave, partes)


def retirar_piache(contenido):
    """Saca `piache` de VOCABULARIO_BASE y lo archiva en FUERA_DEL_HABLA.

    No es un borrado: la entrada viaja entera, con su `notas`, a un dict
    aparte que documenta por qué salió. Idempotente por doble comprobación
    (la línea ya no está / el bloque ya está).

    ⚠ La búsqueda de la línea a retirar se acota a lo que hay ANTES del bloque
    de archivo: si no, la segunda corrida encuentra la copia archivada —que es
    un dict literal idéntico— y la borra, deshaciendo el archivo.
    """
    hechos = []
    corte = contenido.find("FUERA_DEL_HABLA")
    activo = contenido if corte == -1 else contenido[:corte]

    # 1. Sacarla del vocabulario activo.
    m = _entrada(activo, "piache")
    if m:
        inicio = contenido.rfind("\n", 0, m.start()) + 1
        fin = contenido.find("\n", m.end())
        fin = len(contenido) if fin == -1 else fin + 1
        contenido = contenido[:inicio] + contenido[fin:]
        hechos.append("piache fuera de VOCABULARIO_BASE")

    # 2. Archivarla. Si el bloque existe pero perdió la entrada, se repone.
    if "FUERA_DEL_HABLA" in contenido and not _entrada(contenido, "piache"):
        pos = contenido.find("FUERA_DEL_HABLA")
        abre = contenido.find("{", pos)
        contenido = (contenido[:abre + 1] + "\n" + _literal_entrada("piache", PIACHE)
                     + contenido[abre + 1:].lstrip("\n"))
        hechos.append("piache repuesta en FUERA_DEL_HABLA")
    elif "FUERA_DEL_HABLA" not in contenido:
        bloque = (
            "# ── Formas retiradas del habla (D10, 2026-08-03) ──────────────────────\n"
            "# NO son vocabulario activo: no se siembran en Supabase, no entran en los\n"
            "# prompts y no puntúan. Se conservan con su procedencia porque el proyecto\n"
            "# retira palabras con la misma disciplina con que las admite: se archiva el\n"
            "# porqué, no se borra el rastro. Ver aplicar_d10.py.\n"
            "FUERA_DEL_HABLA: dict[str, dict] = {\n"
            + _literal_entrada("piache", PIACHE) +
            "}\n\n\n"
        )
        pos = contenido.find(ANCLA_FUERA)
        if pos == -1:
            raise RuntimeError("no se encontró el ancla %r en el lexicón" % ANCLA_FUERA)
        contenido = contenido[:pos] + bloque + contenido[pos:]
        hechos.append("FUERA_DEL_HABLA creado con piache")

    return contenido, hechos


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="informa lo que haría, no escribe el lexicón")
    args = ap.parse_args()
    _forzar_utf8()

    with open(LEXICON_FILE, encoding="utf-8") as fh:
        original = fh.read()
    contenido = original

    print("=" * 78)
    print("  D10 — tres políticas para 16 entradas")
    print("=" * 78)

    for titulo, tabla in (("GRUPO 1 · reasigna lengua", GRUPO_1),
                          ("GRUPO 2 · corrige o documenta glosa", GRUPO_2),
                          ("GRUPO 3 · baja de tier", GRUPO_3)):
        contenido, cam, igual, aus = aplicar_campos(contenido, tabla, titulo)
        print("\n  %s  (%d)" % (titulo, len(tabla)))
        print("    aplicadas : %s" % (", ".join(cam) or "—"))
        if igual:
            print("    ya estaban: %s" % ", ".join(igual))
        if aus:
            print("    ⚠ NO ENCONTRADAS: %s" % ", ".join(aus))

    contenido, hechos = retirar_piache(contenido)
    print("\n  PIACHE · sale del habla, boratio ocupa su lugar")
    print("    %s" % ("; ".join(hechos) if hechos else "ya estaba hecho"))

    if args.dry_run:
        print("\n  --dry-run: el lexicón NO se tocó.")
        return 0
    if contenido == original:
        print("\n  Nada que escribir: el lexicón ya estaba al día.")
        return 0

    with open(LEXICON_FILE, "w", encoding="utf-8") as fh:
        fh.write(contenido)
    print("\n  Escrito %s" % LEXICON_FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
