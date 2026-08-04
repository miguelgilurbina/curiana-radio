# -*- coding: utf-8 -*-
"""
CURIANA — aplicar al lexicón las citas recuperadas para las 82 sin nota (F1)
============================================================================

Las entradas de familia caquetía de `VOCABULARIO_BASE` **sin campo `notas`**
eran 82 al abrir el vault: palabras marcadas como caquetío sin una sola cita
detrás (PLAN_MAESTRO.md §1, tarea F1). `auditar_82.py` cruza las cuatro
minerías del 2026-08-03 y clasifica cada una; **este script aplica la clase
`CONFIRMA`**, escribiendo la cita en `notas`.

Es trabajo de PROCEDENCIA, no de contenido: no cambia glosas ni etiquetas de
`fuente`. La única excepción está documentada abajo (`warawara`).

De dónde sale cada bloque de citas
----------------------------------
1. **Zavala Reyes 2015 (F7)** — `investigacion/fuentes/zavala-reyes-2015.md`,
   sección «Cobertura de las 82 sin cita»:
     · A (52) entrada directa del glosario → nº de entrada + siglas del
       compilador (AM = Angulo Molina, GC = Galeotto Cey, HB, PMA, E, CGB, HP)
       + glosa verbatim. Aquí se aplican 44: las otras 8 quedan bloqueadas.
     · B (3) entrada con variante ortográfica (`bariki`<Barique,
       `buko`<Buco, `chuchubi`<Chuchube) → se cita la variante.
     · C (7) prosa y notas al pie, no glosario → p. 73 (la fórmula de saludo
       recogida por Arcaya, única frase caquetía conservada), notas al pie
       (3) y (4), y p. 62.
2. **Alvarado 1921 (F3)** — `lexicon_alvarado.AUDITORIA_82`, veredicto
   `confirma` → página y lema del *Glosario de voces indígenas de Venezuela*.
   Cierra 4 que Zavala no tiene (`cachicamo`, `mazato`, `poporo`) y corrobora
   otras 4 (`buco`, `maure`, `mene`, `tuqueque`).
3. **Gatschet 1885 (F4)** — `lexicon_gatschet.COBERTURA_82` (material Pinart,
   Aruba 1882) → sección del vocabulario y forma insular. Nunca cierra sola:
   siempre entra como corroboración de van Buurt o Zavala.
4. **van Buurt 2014 (F6)** — `lexicon_van_buurt.COBERTURA_82` y
   `VAN_BUURT_S6` → §6 «words likely to be of Caquetío origin», con marca de
   isla (A=Aruba, B=Bonaire, C=Curaçao). Cierra 4 de la vertiente insular
   (`chogogo`, `kadushi`, `sawaka`, `warawara`).
5. **Oliver 1989 cap. 2 (vía Oviedo y Valdés)** — `datihao` y `guaitiao`,
   que las cuatro minerías dan por SIN_RASTRO pero tienen fuente firme:
   p. 147, raíz de parentesco `/-atti-/`.

Lo que este script NO toca — y por qué
--------------------------------------
- Las **13 de clase RECLASIFICA** (`piache`, `ture`, `pauji`, `watapana`,
  `kunuku`, `auyama`, `caraota`, `kukuisa`, `cumaragua`, `guanepe`,
  `bureche`, `tata`, `coro`): la fuente dice que son de OTRA lengua o que la
  voz caquetía es otra. Degradarlas es la **decisión D10**, de Miguel.
- Las **3 de clase CONFLICTO_GLOSA** (`tara`, `saruro`, `corie`): la fuente
  las tiene con otro significado, así que citarlas sería fabricar respaldo.
  También D10.
- `kama`, `koke`, `wabarsure`: SIN_RASTRO real, se quedan como están.

Marca de fuerza
---------------
Cuando la fuente marca la atribución como **débil** (columna «fuerza» = D en
Zavala: fitónimos y zoónimos de circulación pan-venezolana; o cuando Alvarado
confirma la GLOSA pero no la filiación caquetía), eso viaja literalmente en la
nota como `[atribución débil: ...]`. Una cita que no distingue fuerte de débil
no sirve para auditar.

Uso
---
    python aplicar_citas_82.py --dry-run   # informe, no escribe
    python aplicar_citas_82.py             # aplica

Idempotente: una entrada que ya tiene `notas` se salta (se informa como
`ya-tenía`). Correrlo dos veces no duplica nada.
"""

import argparse
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LEXICON_FILE = os.path.join(AQUI, "curiana_lexicon.py")

Z = "Zavala Reyes 2015"

# --------------------------------------------------------------------------
# BLOQUE 1 — Zavala Reyes 2015, sección A: entrada directa del glosario (44)
# nº de entrada + siglas del compilador + glosa verbatim.
# --------------------------------------------------------------------------
CITAS_ZAVALA_A = {
    "amaca":      "%s, glosario #9 (AM): «Sitio de moler maíz»" % Z,
    "apana":      "%s, glosario #10 (GC): «Una luna. Medición de tiempo»" % Z,
    "ateri":      "%s, glosario #17 (GC): «Hombre»" % Z,
    "bajarí":     "%s, glosario #25 (AM): «Recorrer, caminar»" % Z,
    "barici":     "%s, glosario #34 (HB): «Agua turbia»" % Z,
    "borojo":     "%s, glosario #44 (AM): «Salina de Coro, comercio de la sal»" % Z,
    "buiamati":   "%s, glosario #47 (GC): «dos lunas. Medición de tiempo»" % Z,
    "buriche":    "%s, glosario #50 (AM): «Licor fermentado»" % Z,
    "caduchi":    "%s, glosario #55 (HB): «Higo, breva» [atribución débil: la fuente da la glosa española del fruto, no el referente local (cardón)]" % Z,
    "catarí":     "%s, glosario #70 (PMA): «Número cuatro»" % Z,
    "cati":       "%s, glosario #71 (CGB): «Luna [catire: persona de tez blanca]»" % Z,
    "cazá":       "%s, glosario #74 (HB): «Puche de maíz»" % Z,
    "cazebo":     "%s, glosario #75 (GC): «Poniente»" % Z,
    "cazi":       "%s, glosario #76 (GC): «Sol»" % Z,
    "cazicure":   "%s, glosario #77 (GC): «Parte del levante»" % Z,
    "chiriguare": "%s, glosario #84 (HB): «Gavilán» [atribución débil: voz zoonímica panvenezolana]" % Z,
    "dare":       "%s, glosario #103 (HB): «Diente»; Oliver 1989 la confirma en Paraguaná" % Z,
    "duraboa":    "%s, glosario #115 (AM): «Conuco, sembrado»" % Z,
    "eroa":       "%s, glosario #119 (AM): «Empezar, crear»" % Z,
    "garabal":    "%s, glosario #121 (AM): «Tierra de crianza o tierra de pasto»" % Z,
    "gua":        "%s, glosario #122 (HP): «Conuco, heredad, terreno cercado con algo»" % Z,
    "gudamuen":   "%s, glosario #148 (PMA): «Numero dos»" % Z,
    "güere":      "%s, glosario #149 (AM): «Dar, entregar»" % Z,
    "güique":     "%s, glosario #152 (AM): «Río navegable»" % Z,
    "humocaro":   "%s, glosario #159 (GC): «Mujer bella»" % Z,
    "iero":       "%s, glosario #163 (GC): «Mujer»" % Z,
    "jacuque":    "%s, glosario #170 (AM): «Regar, regadío»" % Z,
    "jacura":     "%s, glosario #171 (AM): «Guardar»" % Z,
    "jaguey":     "%s, glosario #174 (AM): «Establecer, estancar» [atribución débil: jagüey es panamericano, de origen taíno]" % Z,
    "jai":        "%s, glosario #175 (AM): «Oír, escuchar»" % Z,
    "na":         "%s, glosario #184 (HP): «Partícula equivalente a como o semejante»" % Z,
    "pariri":     "%s, glosario #194 (AM): «Pantano, ciénaga»" % Z,
    "paro":       "%s, glosario #195 (AM): «Río»" % Z,
    "quidi":      "%s, glosario #212 (AM): «Cerro, altura»" % Z,
    "rao":        "%s, glosario #219 (E): «Arena»" % Z,
    "sabuenen":   "%s, glosario #222 (PMA): «Número tres»" % Z,
    "tabri":      "%s, glosario #234 (AM): «Conuco, siembra»" % Z,
    "tarica":     "%s, glosario #242 (AM): «Laguna»" % Z,
    "tebe":       "%s, glosario #245 (AM): «Lugar de cultivo»" % Z,
    "ucibo":      "%s, glosario #267 (AM): «Cuenta de piedras»" % Z,
    "urapa":      "%s, glosario #269 (AM): «Sitio de cría de animales»" % Z,
    # Corroboradas por Alvarado 1921: la cita cruzada es el activo, va entera.
    "buco":       "%s, glosario #46 (AM+CGB): «Chorro de agua, presa de agua»; Alvarado 1921, p.34 s.v. BUCO: «caz, acequia» [atribución débil de la filiación: Alvarado la localiza en Lara y sugiere origen romance, confirma la glosa pero duda del origen indígena]" % Z,
    "cari":       "%s, glosario #66 (E): «Orilla del mar»; Cruz Esteves 1989 vía van Buurt 2014 §9 (topónimo Cariatávo), cari/kari = costa, orilla" % Z,
    "tuqueque":   "%s, glosario #257 (E+A+PMA): «Lagarto casero»; Alvarado 1921, p.300 s.v. TUQUEQUE (geco: Thecadactylus rapicaudus / Gonatodes albogularis); van Buurt 2014 §6 s.v. waltaca deriva el papiamento totèki de «tuqueque, tuteque, an Amerindian word used for geckos in Venezuela» [atribución débil: voz venezolana corriente, ninguna fuente la localiza en Coro]" % Z,
}

# --------------------------------------------------------------------------
# BLOQUE 2 — Zavala Reyes 2015, sección B: variante ortográfica (3)
# --------------------------------------------------------------------------
CITAS_ZAVALA_B = {
    "bariki":   "%s, glosario #35 «Barique» (AM+HB): «Arcilla roja. Almagre. Galeotto Cey indica Bariquizi o bija»; Arcaya la cita también en la Relación de Barquisimeto 1579" % Z,
    "buko":     "%s, glosario #46 «Buco» (AM+CGB): «Chorro de agua, presa de agua» (misma palabra que buco, aquí con grafía k)" % Z,
    "chuchubi": "%s, glosario #85 «Chuchube» (HB): «Paraulata»; Gatschet 1885 (material Pinart, Aruba 1882), sección aves, «shushubi» = Orpheus americanus; van Buurt 2014 §6 «chuchubi» (islas A/B/C) = Mimus gilvus. Triple atestación continental-insular-viva; la alternancia sh~ch es la correspondencia que describe van Buurt" % Z,
}

# --------------------------------------------------------------------------
# BLOQUE 3 — Zavala Reyes 2015, sección C: prosa y notas al pie (7)
# No salen del glosario, así que se cita la página, no el nº de entrada.
# --------------------------------------------------------------------------
CITAS_ZAVALA_C = {
    "chacamba": "%s, p.73, citando a Arcaya (1995): «fórmula de saludo: chacamba cudanga (¿Cómo está usted?)», recogida a una anciana de Mitare. Es la única frase caquetía conservada" % Z,
    "cudanga":  "%s, p.73, citando a Arcaya (1995): «chacamba cudanga (¿Cómo está usted?)»" % Z,
    "cudan":    "%s, p.73, citando a Arcaya (1995): «cudan de cuté (para servir a usted)»; variante de 1905: «judan de cuteo»" % Z,
    "cuté":     "%s, p.73, citando a Arcaya (1995): «cudan de cuté (para servir a usted)»" % Z,
    "curiana":  "%s, nota al pie (4): «Curiana: territorio donde estaban asentados los caquetíos»" % Z,
    "maure":    "%s, nota al pie (3): «Maure: fibra de algodón con la que tejían las hamacas»; Alvarado 1921, p.216 s.v. MÁURE (Carvajal 168 y Castellanos la registran como faja o tejido; en Coro vivía en 1921 como pieza de dril)" % Z,
    # Caso mixto: Zavala NO sostiene la glosa; Alvarado sí. Ver informe de F1.
    "mene":     "Alvarado 1921, p.218 s.v. MÉNE, citando Oviedo II.301 («betún a manera de brea») y a Codazzi, que localiza los yacimientos en Coro y Maracaibo; %s, p.62, cita a Arcaya (1920) sobre la Relación de Barquisimeto 1579 («mene y cumaragua nombre de la ciruela») [advertencia: la sintaxis de Arcaya es ambigua y esa cita NO sostiene la glosa de petróleo o rezumadero — quien la sostiene es Alvarado]" % Z,
}

# --------------------------------------------------------------------------
# BLOQUE 4 — Alvarado 1921, únicas fuentes de su entrada (3)
# Ausentes del glosario de Zavala (su sección E).
# --------------------------------------------------------------------------
CITAS_ALVARADO = {
    "cachicamo": "Alvarado 1921, p.41 s.v. CACHICAMO: glosa idéntica (Dasypus) [atribución débil de la filiación: voz de circulación nacional, Alvarado no declara origen ni la localiza en Coro]",
    "mazato":    "Alvarado 1921, p.217 s.v. MAZATO, citando Oviedo II.297 y 300 («magato… brevaje») [atribución débil de la filiación: la forma es panamericana (masato peruano), la glosa sí está confirmada]",
    "poporo":    "Alvarado 1921, p.255 s.v. POPORO: la atribuye explícitamente a los antiguos Caquetíos y cita a Castellanos",
}

# --------------------------------------------------------------------------
# BLOQUE 5 — van Buurt 2014 §6, vertiente insular (4)
# «Words likely to be of Caquetío origin». El propio autor advierte que la
# lista «has a subjective element»: esa advertencia viaja en la nota.
# --------------------------------------------------------------------------
_S6 = ("van Buurt 2014 §6 «words likely to be of Caquetío origin» "
       "(el autor advierte que la lista «has a subjective element»)")
CITAS_VAN_BUURT = {
    "chogogo": "%s, islas A/B/C: «the greater flamingo (Phoenicopterus ruber)»" % _S6,
    "sawaka":  "%s, isla C: «the underworld, the realm of the dead, the beyond»; en papiamento antiguo la expresión baha na sawaka = descender al inframundo, morir; paralelos en taíno y lokono" % _S6,
    "kadushi": "%s, islas A/B/C: «a columnar cactus (Cereus repandus)», var. cadushi (Aruba); Gatschet 1885 (material Pinart, Aruba 1882), sección plantas, «kaduski» = Cereus lanuginosus; respaldo toponímico van Buurt §7 (cadushi) [referente ABIERTO por D7: tres cactus distintos bajo el mismo nombre — Gatschet Pilosocereus lanuginosus, van Buurt Cereus repandus, el lexicón Cereus hexagonus; el nombre es un genérico de cardón, no una especie]" % _S6,
    # warawara lleva además corrección de glosa: ver GLOSAS_CORREGIDAS.
    "warawara": "%s, islas A/B/C: «the crested Caracara (Caracara cheriway syn. Polyborus plancus)»; respaldo toponímico §7 (Sero Warawara, Warawao, Aruba). La glosa anterior del lexicón («buitre, zamuro (Cathartes curasoica)») era, palabra por palabra, la identificación de Gatschet 1885 (material Pinart 1882), heredada sin saber de dónde venía: Cathartes es Cathartidae (zamuros) y Caracara es Falconidae. D7 registra las dos lecturas: la de 1885 queda aquí, la moderna pasa a la glosa activa" % _S6,
}

# --------------------------------------------------------------------------
# BLOQUE 6 — Oliver 1989 cap. 2 (vía Oviedo y Valdés) (2)
# Las cuatro minerías las dan por SIN_RASTRO, pero tienen fuente firme.
# NO se citan a Zavala: su sección E las excluye explícitamente.
# --------------------------------------------------------------------------
CITAS_OLIVER = {
    "datihao":  "Oliver 1989, cap. 2, p.147, sobre Oviedo y Valdés: forma atestiguada «daitiao», cognada del taíno daitia-o y del lokono da-tti / da-iti, sobre la raíz de parentesco /-atti-/, que en lokono cubre tío, padre e hija según el prefijo posesivo [pendiente: la forma del lexicón es datihao y la de Oliver daitiao — ¿metátesis de copia o dos formas?]",
    "guaitiao": "Oliver 1989, cap. 2, p.147, sobre Oviedo y Valdés: mismo lexema que datihao sobre la raíz de parentesco /-atti-/, con distinto prefijo de persona; el pacto de guaitiao (intercambio de nombres entre aliados) lo describe Oviedo para el área circuncaribe",
}

CITAS = {}
for _bloque in (CITAS_ZAVALA_A, CITAS_ZAVALA_B, CITAS_ZAVALA_C,
                CITAS_ALVARADO, CITAS_VAN_BUURT, CITAS_OLIVER):
    CITAS.update(_bloque)

# --------------------------------------------------------------------------
# Corrección de glosa — la única. Política D7: las dos lecturas se registran,
# la moderna manda en la glosa activa y la histórica queda en `notas`.
# --------------------------------------------------------------------------
GLOSAS_CORREGIDAS = {
    "warawara": ("buitre, zamuro (Cathartes curasoica)",
                 "caracara, ave rapaz carroñera (Caracara cheriway)"),
}


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


def aplicar(contenido):
    """Devuelve (contenido_nuevo, aplicadas, ya_tenian, no_encontradas)."""
    aplicadas, ya_tenian, no_encontradas = [], [], []

    for clave, nota in sorted(CITAS.items()):
        m = _entrada(contenido, clave)
        if not m:
            no_encontradas.append(clave)
            continue
        cuerpo = m.group(2)
        if '"notas"' in cuerpo:
            ya_tenian.append(clave)
            continue
        if '"' in nota or "}" in nota:
            raise ValueError("nota con comilla o llave, rompería el módulo: %s" % clave)
        cuerpo_nuevo = cuerpo.rstrip()
        if not cuerpo_nuevo.endswith(","):
            cuerpo_nuevo += ","
        cuerpo_nuevo += ' "notas": "%s"' % nota
        contenido = (contenido[:m.start()] + m.group(1) + cuerpo_nuevo + m.group(3)
                     + contenido[m.end():])
        aplicadas.append(clave)

    return contenido, aplicadas, ya_tenian, no_encontradas


def corregir_glosas(contenido):
    """Aplica GLOSAS_CORREGIDAS **solo sobre el campo `sig`**.

    Sustituir sobre el cuerpo entero mordía la propia `notas`, que cita la
    glosa vieja verbatim para documentar la corrección (D7): la nota acababa
    diciendo que la glosa anterior era la nueva. Idempotente.
    """
    hechas, ya_estaban = [], []
    for clave, (vieja, nueva) in GLOSAS_CORREGIDAS.items():
        m = _entrada(contenido, clave)
        if not m:
            continue
        cuerpo = m.group(2)
        sig = re.search(r'"sig":\s*"([^"]*)"', cuerpo)
        if not sig:
            print("  ⚠ %s: no se encontró el campo sig, no se toca" % clave)
            continue
        if sig.group(1) == nueva:
            ya_estaban.append(clave)
            continue
        if sig.group(1) != vieja:
            print("  ⚠ %s: la glosa esperada ya no está, no se toca" % clave)
            continue
        cuerpo_nuevo = cuerpo[:sig.start(1)] + nueva + cuerpo[sig.end(1):]
        contenido = (contenido[:m.start()] + m.group(1) + cuerpo_nuevo + m.group(3)
                     + contenido[m.end():])
        hechas.append(clave)
    return contenido, hechas, ya_estaban


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="informa lo que haría, no escribe el lexicón")
    args = ap.parse_args()
    _forzar_utf8()

    with open(LEXICON_FILE, encoding="utf-8") as fh:
        original = fh.read()

    contenido, aplicadas, ya_tenian, no_encontradas = aplicar(original)
    contenido, glosas, glosas_ya = corregir_glosas(contenido)

    bloques = [("Zavala 2015 §A (glosario)", CITAS_ZAVALA_A),
               ("Zavala 2015 §B (variante ortográfica)", CITAS_ZAVALA_B),
               ("Zavala 2015 §C (prosa y notas al pie)", CITAS_ZAVALA_C),
               ("Alvarado 1921 (única fuente)", CITAS_ALVARADO),
               ("van Buurt 2014 §6 (vertiente insular)", CITAS_VAN_BUURT),
               ("Oliver 1989 cap.2 (vía Oviedo)", CITAS_OLIVER)]
    print("=" * 74)
    print("  CITAS POR BLOQUE")
    print("=" * 74)
    for titulo, bloque in bloques:
        nuevas = [k for k in bloque if k in aplicadas]
        print("  %-42s %2d cita(s)  · aplica %d" % (titulo, len(bloque), len(nuevas)))

    print("\n  Aplicadas ahora : %d" % len(aplicadas))
    print("  Ya tenían nota  : %d %s" % (len(ya_tenian), ya_tenian or ""))
    if no_encontradas:
        print("  NO ENCONTRADAS  : %d %s" % (len(no_encontradas), no_encontradas))
    print("  Glosas corregidas (D7): %s%s"
          % (glosas or "ninguna", " (ya estaban: %s)" % glosas_ya if glosas_ya else ""))

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
