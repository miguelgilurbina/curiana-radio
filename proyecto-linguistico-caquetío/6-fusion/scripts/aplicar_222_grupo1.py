# -*- coding: utf-8 -*-
"""APLICAR EL GRUPO 1 DE #222 que quedaba abierto (dp.1.04-06, dp.1.08-12) y
`bagua`, al lexicón.

Decisión de Miguel, 2026-09-24: «Ok a todo, que no quede ninguna tarea
pendiente. Lo único pendiente es lo que tenga que ver con docker». Se aplica
la recomendación del recopilador de cada entrada
(6-fusion/issues-pendientes/decisiones-pendientes-2026-09-23.md §Grupo 1);
registro en 6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml §th.14-th.23.
dp.1.01-03 y dp.1.07 los cerró la tanda final (tf.1-3, tf.6).

Qué hace en curiana_sim/curiana_lexicon.py:
  · dp.1.04 — `cacike` y `naboria` dejan de enseñarse en [Voces de fuera]
    (LLEGARON_CON_EL_ESPANOL); el scorer no se toca.
  · dp.1.05 — `kumarawa`: la cita de Arcaya corregida («viruela») y las
    cuatro lecturas en `notas`; la glosa no se reescribe (minar-fuente §8).
  · dp.1.06 — `korie`: la nota C2 (Oviedo t. II p. 330).
  · dp.1.08 — `busera` entra (atestiguada, Oviedo t. II p. 300); notas en
    `kama` y `datihao`; `auri` no se mueve.
  · dp.1.09 — `ka-`: el «hay X» impersonal se declara extensión del proyecto.
  · dp.1.10 — las 8 kalinago sin apoyo en Goeje, con su deuda; `hiñaru` →
    'mujer'.
  · dp.1.11 — `taita` y `yamosa` anotadas; `piragua` y `maboya` a kalinago;
    `bejique` y `guabina` con su nota.
  · dp.1.12 — `-oa` y `-bo` entran al desafijador (REGLAS_OLIVER, no se
    enseñan); `-kiva` se declara y NO se pela: en grafía fonémica es `kiba`.
  · bagua — 'mar', taíno, con su cronista (Oviedo t. I p. 436).

Idempotente (marca MARCA); `--dry-run` imprime y no escribe.
Uso:  python 6-fusion/scripts/aplicar_222_grupo1.py [--dry-run]
"""
import argparse
import ast
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
MARCA = "# dp.1.04 (#222, «B recortada antes de la base»"
DEC = "«Ok a todo, que no quede ninguna tarea pendiente» (Miguel, 2026-09-24)"

ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
ARGS = ap.parse_args()

src = open(P, "rb").read().decode("utf-8")
if MARCA in src:
    print("ya aplicado; nada que hacer")
    sys.exit(0)
EOL = "\r\n" if "\r\n" in src else "\n"
t = src.replace(EOL, "\n")
hechos = []


def q(v):
    return json.dumps(v, ensure_ascii=False) if isinstance(v, str) else repr(v)


def linea_de(clave):
    m = [m for m in re.finditer(r'^    "' + re.escape(clave) + r'":\s*\{.*\},\s*$', t, re.M)]
    ini = t.index("VOCABULARIO_BASE: dict[str, dict] = {")
    fin = t.index("\n}\n", ini)
    m = [x for x in m if ini < x.start() < fin]
    assert len(m) == 1, (clave, len(m))
    return m[0]


def tocar(clave, cambios=None, nota=None, nueva_clave=None):
    """Edita una entrada de UNA línea: `cambios` pisa campos, `nota` se añade."""
    global t
    m = linea_de(clave)
    linea = m.group(0)
    k, e = next(iter(ast.literal_eval("{" + linea.strip().rstrip(",") + "}").items()))
    e = dict(e)
    for c, v in (cambios or {}).items():
        e[c] = v
    if nota:
        e["notas"] = (e.get("notas", "") + " · " + nota).lstrip(" ·")
    cabeza = linea[:linea.index("{")]
    nueva = cabeza + "{" + ", ".join(f'"{c}": {q(v)}' for c, v in e.items()) + "},"
    t = t[:m.start()] + nueva + t[m.end():]
    hechos.append(clave)


def tocar_bloque(clave, nota):
    """Añade a la `notas` de una entrada de VARIAS líneas."""
    global t
    ini = t.index(f'\n    "{clave}": {{\n') + 1
    fin = t.index("\n    },\n", ini)
    bloque = t[ini:fin]
    m = re.search(r'("notas": )(".*?")(,?)$', bloque, re.M)
    viejo = json.loads(m.group(2))
    nuevo = bloque[:m.start()] + m.group(1) + q(viejo + " · " + nota) + m.group(3) + bloque[m.end():]
    t = t[:ini] + nuevo + t[fin:]
    hechos.append(clave)


def insertar_tras(clave, lineas):
    global t
    m = linea_de(clave)
    t = t[:m.end()] + "\n" + "\n".join(lineas) + t[m.end():]


# ── dp.1.04 ────────────────────────────────────────────────────────────
a = "SIN_FORMA_DE_LA_ESFERA = frozenset({"
i = t.index(a)
bloque_dp104 = f'''{MARCA}; {DEC}): las
# voces taínas que sólo llegaron a Venezuela en boca del español —las que Oliver
# nombra así, `cacike` y `naboria` (#192, T5 §6)— no se enseñan en
# [Voces de fuera]. El SCORER NO SE TOCA: dichas, siguen contando como préstamo
# de la esfera. La auditoría voz por voz del resto de las taínas (la opción B
# entera) se hizo después: ver 6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml.
LLEGARON_CON_EL_ESPANOL = frozenset({{"cacike", "naboria"}})

'''
t = t[:i] + bloque_dp104 + t[i:]
a = "        forma = forma_de_la_esfera(forma)\n        if forma in vistas:\n            continue\n"
assert t.count(a) == 1
t = t.replace(a, "        forma = forma_de_la_esfera(forma)\n"
                 "        if forma in LLEGARON_CON_EL_ESPANOL:   # dp.1.04\n            continue\n"
                 "        if forma in vistas:\n            continue\n")
hechos.append("[Voces de fuera] sin cacike/naboria")

# ── dp.1.05 y dp.1.08 (kumarawa) ────────────────────────────────────────
tocar("kumarawa", nota=(
    f"dp.1.05 y dp.1.08 de #222 ({DEC}), la reapertura de D10, CERRADA SIN MOVER LA GLOSA "
    "(minar-fuente §8: si una fuente contradice, se anota; no se reescribe). CITA CORREGIDA: "
    "Arcaya 1920 p. 75 (vista en imagen, #216 M6) escribe «viruela», no «ciruela» —la "
    "«ciruela» de Zavala #93 es una mala lectura de ella—, y la Tabla A-9 de Oliver (#25, "
    "vista en imagen, #213 M1) también da 'viruela / smallpox'. Ojo, regla 3: la viruela "
    "llegó con los españoles (1518 en La Española), así que esa acepción es COLONIAL por "
    "construcción y la voz pudo nombrar otra cosa antes. Cuarta lectura: Esteves 1989 p. 33 "
    "s.v. CUMARAGUAS, «un pequeño cangrejo de caparazón rosada», 'espuma rosada' (#208 FA3) "
    "— la costa de Paraguaná otra vez, pero es la etimología de un topónimo, que cc.4 deja "
    "hipotética. Se queda la de Alvarado (costas de Paraguaná), la única atestación "
    "localizada de la voz."))

# ── dp.1.06 (korie) ─────────────────────────────────────────────────────
tocar("korie", nota=(
    f"dp.1.06 de #222 ({DEC}), opción C2: se deja atestiguada con esta nota. Oviedo t. II "
    "p. 330 (visto en imagen, #211 FA1): «Armados cories hay, pero son mayores que los desta "
    "isla» — y en Oviedo `cori` es el CUY (t. I p. 390), así que la voz de Zavala #90 (HB) "
    "puede venir de una mala lectura de ese pasaje. La Tabla A-9 de Oliver (fila 24) la da "
    "sin fuente (#213 M1). Falta ver la obra de Hernández Baño detrás de la sigla HB "
    "(dp.3.02): la consulta a Zavala está redactada en 6-fusion/issues-pendientes/"))

# ── dp.1.08 (busera, kama, datihao) ─────────────────────────────────────
insertar_tras("kumarawa", [
    '    "busera":     {"sig": "jagua, tinte negro-azulado con que se pinta el cuerpo (Genipa americana)", '
    '"cat": "sust", "fuente": "caquetío-atestiguado", "forma_fuente": "busera", "notas": ' + q(
        f"dp.1.08 de #222 ({DEC}), opción A: la Tabla A-9 de Oliver verificada (#213 M1). Oviedo "
        "t. II p. 300 (oviedo-y-valdes-1852-1855, visto en imagen): «embixados y pintados de bixa "
        "y de xagua, que allí llaman busera» — la XAGUA (negro), con la bixa (rojo) al lado como "
        "otra cosa. UNA sola atestación: la A-9 de Oliver (n.º 12, buxera, «pintura "
        "negra-Genipa») bebe del mismo Oviedo (tesis pp. 283-284). La glosa 'rojo, bija' de la "
        "n. 213 del cap. 3 de Oliver es la del EDITOR de Oviedo (t. IV p. 595): la trampa de "
        "datihao. Polity: Oliver ASUME que el funeral del díao que describe Oviedo es el de la "
        "costa (tesis p. 283: «it is reasonable to assume…»); suposición declarada, no dato. "
        "Época: contacto temprano (regla 3). Antes no estaba en el lexicón bajo ninguna grafía "
        "(busera, buxera, bujera: 0, medido por M1)") + "},",
])
tocar("kama", nota=(
    f"dp.1.08 de #222 ({DEC}): NO es «SIN_RASTRO». La fila existe en la Tabla A-9 de Oliver "
    "(#15, «cama | K-ama | danta | tapir», vista en imagen, #213 M1) y el cap. 2 p. 142 da la "
    "fuente: la Relación de BARQUISIMETO de 1579 (Arellano Moreno 1964 p. 183), «cama» o "
    "«çama». Regla 4: es de Barquisimeto, no de la polity costera; hay huesos de tapir en los "
    "fogones de Túcua (cap. 4 p. 439). NO SUBE de capa hasta tener la Relación (dp.3.01): "
    "Oliver la cita sin transcribir la página"))
tocar("datihao", nota=(
    f"dp.1.08 de #222 ({DEC}): la A-9 de Oliver (n.º 32, «señor / lesser chief») no suma "
    "atestación: su glosa sale de la entrada del glosario del editor de Oviedo (1855)"))

# ── dp.1.10 (las 8 kalinago y hiñaru) ───────────────────────────────────
OTRA_VOZ = {
    "kasabi-kalinago": "el casabe es aleiba / ereba",
    "yuka-kalinago": "la yuca es kiere / key",
    "hamaka-kalinago": "la hamaca es akat / ekera",
    "ikoa": "la casa es mana, ubana, obogne… (~ lokono sikoa)",
    "kasaku": "(~ lokono kassaku)",
    "pira": "el pez es aoto",
    "baruwa": "el par real es uekeli / eyeri 'hombre' y uele / inharu 'mujer'; baruwa no aparece",
    "amourou": "la guerra es ualime",
}
for k, otra in OTRA_VOZ.items():
    tocar(k, nota=(
        f"dp.1.10 de #222 ({DEC}), opción B — deuda: sin-procedencia. Goeje 1939 no la da: "
        f"{otra} (#219 M5; 6-fusion/kalinago_goeje_1939.yaml §cruce_con_el_lexicon). Es el "
        "patrón de las nueve «taíno-reconstruido»: una voz vecina con la etiqueta cambiada"))
tocar("hiñaru", cambios={"es": "mujer (registro femenino kalinago)"}, nota=(
    f"dp.1.10 de #222 ({DEC}): la glosa era 'persona, ser humano'; Goeje 1939 la da como "
    "'mujer' en el habla de mujeres (uele / inharu), #219 M5. Es la inharu de Adam p. 289 "
    "que la tanda de las hermanas cita junto a iero"))

# ── dp.1.11 (las taínas que db.3 no cubrió) ─────────────────────────────
tocar_bloque("taita", (
    f"dp.1.11 de #222 ({DEC}), T2.3 (a) — deuda: sin-procedencia-colonial. Su único apoyo es "
    "Brinton 1871 p. 13, que cita a Pichardo (diccionario provincial cubano del s. XIX); "
    "Bachiller 1883 la pone en su apéndice (C) de voces que pasan por indígenas y vienen de "
    "otra parte (propone el vascuence aita); Goeje 1939: 0 (#198 T10). Se deja, anotada"))
tocar_bloque("yamosa", (
    f"dp.1.11 de #222 ({DEC}), T9 D2 (B): se deja y se anota — Brinton lee `yamosa`, la "
    "Apologética de Las Casas en NBAE 13 p. 538 (verificada en imagen, #194 T9) lee «yamocá»"))
for k, fam, nota in (
    ("piragua", "kalinago",
     "Goeje 1939 la pone en el caribe insular (y sospecha del español «vela»); Bachiller p. "
     "389 la lista como de Borinquen («Bote, Piraguas, B.»), no eyeri: DOS apoyos, no tres "
     "(M5 C corrige a T10). Y Goeje avisa de que piragua, kanoa y hamaka viajaron a otras "
     "lenguas indígenas por vía del español. Ninguna fuente la llama taína"),
    ("maboya", "kalinago",
     "Goeje 1939 la da como caribe de Honduras (ma-poya) y Bachiller la publica en la lista "
     "eyeri; su único apoyo taíno era Rafinesque. La voz taína para el espíritu del muerto es "
     "`hupia`"),
):
    tocar(k, cambios={"fuente": fam}, nota=(
        f"dp.1.11 de #222 ({DEC}), T10 A con M5 C: pasa de `taíno` a `{fam}`. {nota} (#198 "
        "T10, #219 M5). Sigue en la esfera de contacto: el cambio es de etiqueta"))
tocar("bejique", nota=(
    f"dp.1.11 de #222 ({DEC}), T10 A: la duda, anotada — Goeje 1939 da `behiko` como caribe "
    "insular usado en Haití y `buhuitihu` como el taíno; Bachiller la da de Cuba y las "
    "Lucayas con cita de Las Casas, Apologética p. 436. Los dos intermediarios discrepan "
    "(#198 T10)"))
tocar("guabina", nota=(
    f"dp.1.11 de #222 ({DEC}), T10 A: sube de «sin apoyo» a «atestiguada, libro por "
    "localizar» — Bachiller 1883 p. 267 la da dentro de la enumeración de peces de nombre "
    "indio de Las Casas (#198 T10); la página de Las Casas no se ha visto"))

# ── bagua ───────────────────────────────────────────────────────────────
insertar_tras("guabina", [
    '    "bagua":      {"es": "mar", "fuente": "taíno", "categoria": "geografia", "notas": ' + q(
        f"Entra el 2026-09-24 ({DEC}), cerrando lo que tf.6 dejó abierto («manatí, tabaco y bagua "
        "según su cronista»). Oviedo, Historia general t. I, lib. XIII, cap. IX, p. 436 "
        "(oviedo-y-valdes-1851, verificado en imagen, 6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml "
        "§bagua): «Llaman los indios de aquesta Isla Española á la mar bagua (no digo baygua, "
        "porque baygua es aquel barbasco […] sino bagua es el nombre de la mar en esta isla)». "
        "El glosario del editor (t. IV p. 594, «BAGUA: mar, piélago. (Lengua de Haiti.)») y Zayas "
        "la copian de ahí. Variedad: La Española. El caquetío dice `para` (atestiguado): esto es "
        "la voz de la esfera, no un sinónimo") + "},",
])

# ── dp.1.09 (ka-) ───────────────────────────────────────────────────────
a = '''        "wayunaiki": "ka- (prefijo atributivo); el cognado existe, pero el apoyo que "
                     "se cita es el insular y el lokono, no el andamio",'''
assert t.count(a) == 1
t = t.replace(a, a + '''
        # dp.1.09 de #222 («Ok a todo», 2026-09-24), opción C: el valor con fuente.
        "valor": "«tiene X / que tiene X», con apoyo de las tres hermanas (lokono "
                 "k-ere-u-ti 'casado', Perea p. 555; achagua Ca-barruani «estoi rico», "
                 "Neira y Ribero vía #215; kalinago k-açae-ti-na 'tengo una olla', Adam pp. "
                 "300-301). El «hay X» impersonal es EXTENSIÓN DEL PROYECTO (d21.5 C, el "
                 "ejemplo ka-juri): el achagua dice el hay con otras piezas («Hay mucho "
                 "calor = Amo ayusamí», «No hay = Quenia»). Se sigue enseñando, declarado",''')
hechos.append("ka- valor")

# ── dp.1.12 (-oa, -bo; -kiva declarado) ─────────────────────────────────
a = "TODAS_LAS_REGLAS = {"
i = t.index(a)
bloque_oliver = f'''# dp.1.12 de #222 ({DEC}), opción J: los formantes de topónimo que Oliver
# 1989 cap. 2 pp. 147-148 lista como «the most common suffixes in Caquetío
# toponyms» (-bana, -coa/-koa, -oa, -kiva, (e)-bo, -wa) y el canon no tenía:
# `-oa` y `-bo`. Van al DESAFIJADOR y NO se enseñan (no están en
# AFIJOS_ATESTIGUADOS): Oliver no les da valor. `-kiva` se declara y NO se pela:
# en el lema fonémico de D5 es `-kiba`, la voz atestiguada `kiba` 'piedra', y
# pelarla partiría compuestos con una palabra real (la reserva de J: «-kiva
# puede ser el lexema kiba 'piedra' en composición»). La recomendación era
# «después de la base»; entra en el corte de antes, que es donde no parte la
# serie, y se mide con la base (medir_tanda_hermanas.py --con-base).
REGLAS_OLIVER: dict[str, dict] = {{
    "-oa": {{"nombre": "formante de topónimo (sin valor anotado)",
            "atestiguado": "Oliver 1989 cap. 2 pp. 147-148 (oliver-1989-cap2)"}},
    "-bo": {{"nombre": "formante de topónimo, (e)-bo (sin valor anotado)",
            "atestiguado": "Oliver 1989 cap. 2 pp. 147-148 (oliver-1989-cap2); Esteves "
                           "lo glosa 'paso' en topónimos (Jurijurebo, p. 47), análisis suyo"}},
}}
FORMANTES_DECLARADOS_SIN_PELAR = {{
    "-kiva": "Oliver 1989 cap. 2 pp. 147-148; en grafía fonémica es `kiba` 'piedra' (atestiguada)",
}}

'''
t = t[:i] + bloque_oliver + t[i:]
a = "    **REGLAS_TOPONIMICAS,\n"
i2 = t.index(a, t.index("TODAS_LAS_REGLAS = {"))
t = t[:i2] + a + "    **REGLAS_OLIVER,        # dp.1.12: se pelan, no se enseñan\n" + t[i2 + len(a):]
hechos.append("REGLAS_OLIVER")

ast.parse(t)
print("tocadas:", ", ".join(hechos))
if ARGS.dry_run:
    print("--dry-run: no se escribe")
    sys.exit(0)
open(P, "wb").write(t.replace("\n", EOL).encode("utf-8"))
print("✓ curiana_sim/curiana_lexicon.py")
