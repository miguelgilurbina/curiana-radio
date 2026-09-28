# -*- coding: utf-8 -*-
"""APLICAR LA TANDA DE LAS HERMANAS (2026-09-24) al lexicón.

Decisión de Miguel, 2026-09-24: «Acepto todo lo recomendado» — las tres
propuestas abiertas en 6-fusion/ (kalinago_mujeres_2026-09-23.yaml,
nucleo_fundacional_hermanas_2026-09-24.yaml y taino_tradicion_viva_2026-09-24.yaml).
Registro: 6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml.

Qué hace en curiana_sim/curiana_lexicon.py, entrada a entrada:
  · archiva 40 voces —el núcleo fundacional (th.7), las ocho que seguían
    saliendo del wayuu (D2, th.2), alaain y japü (D3, th.3)— en
    FUERA_DEL_HABLA, con su capa INTACTA y el campo `archivada`;
  · pone en su sitio la voz de las hermanas con la capa que le da N1 (dos
    hermanas con la misma forma o con la correspondencia regular declarada =
    reconstruida; una = hipotética) y su cita en `notas`;
  · re-etiqueta bui, lihi, tuhu, diki y marisi (→ reconstruido) y kaa, maa,
    suka, ama, bari y puna (→ hipotético), con la huella en `notas`;
  · anota la pareja taína de kiba, waitiao, jagey y warawara (T4);
  · renombra las claves lokono huda, kia y wunabu a `<clave>-lokono`.

Lo demás de la tanda (plantillas, koiné, generados, corpus, mundo y tests) se
editó a mano y va en el mismo commit. Los módulos generados se regeneran con
sus scripts: minar_a2_swadesh.py, 6-fusion/scripts/generar_lexicon_achagua.py,
minar_zavala_glosario.py y migrar_toponimos.py.

Reglas: 2 (en duda, degradar: todo lo de una sola hermana es hipotético), 5
(la decisión es de Miguel y está citada), 8 (cada voz nueva cita obra y
página). Medido: 6-fusion/medicion_tanda_hermanas_2026-09-24.yaml.

Idempotente: si FUERA_DEL_HABLA ya tiene el bloque de la tanda, sale sin tocar
nada. `--dry-run` imprime lo que haría y no escribe.

Uso:  python 6-fusion/scripts/aplicar_tanda_hermanas.py [--dry-run]
"""
import argparse
import ast
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
MARCA = "# ── Tanda de las hermanas (2026-09-24): «Acepto todo lo recomendado»"

_ap = argparse.ArgumentParser(description="la tanda de las hermanas, al lexicón")
_ap.add_argument("--dry-run", action="store_true", help="imprime y no escribe")
ARGS = _ap.parse_args()

src = open(P, "rb").read().decode("utf-8")
if MARCA in src:
    print("ya aplicado; nada que hacer")
    sys.exit(0)
EOL = "\r\n" if "\r\n" in src else "\n"
lines = src.split(EOL)

DEC = "6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml"
PN = "6-fusion/nucleo_fundacional_hermanas_2026-09-24.yaml"
PK = "6-fusion/kalinago_mujeres_2026-09-23.yaml"
PT = "6-fusion/taino_tradicion_viva_2026-09-24.yaml"
FRASE = "«Acepto todo lo recomendado»"

# ── utilidades ──────────────────────────────────────────────────────────
def linea_de(clave, desde=0, hasta=None):
    pat = re.compile(r'^    "' + re.escape(clave) + r'":\s*\{')
    idx = [i for i, l in enumerate(lines) if pat.match(l)]
    if hasta is not None:
        idx = [i for i in idx if desde <= i < hasta]
    return idx


def parse(linea):
    d = ast.literal_eval("{" + linea.strip().rstrip(",") + "}")
    assert len(d) == 1
    return next(iter(d.items()))


def emit(clave, e):
    orden = ["sig", "cat", "fuente", "forma_fuente", "archivada", "notas"]
    ks = [k for k in orden if k in e] + [k for k in e if k not in orden]
    cuerpo = ", ".join(f'"{k}": {q(e[k])}' for k in ks)
    pad = " " * max(1, 13 - len(clave))
    return f'    "{clave}":{pad}{{{cuerpo}}},'


def q(v):
    import json
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    return repr(v)


_ini = next(i for i, l in enumerate(lines) if l.startswith("VOCABULARIO_BASE: dict"))
FIN_BASE = next(i for i in range(_ini, len(lines)) if lines[i].startswith("}"))
# VOCABULARIO_BASE acaba bastante antes; el bloque de arriba (≈ 47-330) es
# donde viven las voces del núcleo. Las claves lokono están en ≈ 6300-6460.

# ── las voces que se archivan y lo que las sustituye ───────────────────
N = {  # núcleo: vieja -> (nueva|None, capa, cat, sig, derivación, grupo)
    # grupo 1: la atestiguada ya lo dice
    "kono":  (None, None, None, None, "`jusual` (Zavala #180 (AM), «sembrar, siembra, sembradío. Conuco»), caquetío atestiguado, cubre el concepto (d19.c)", "1"),
    "sima":  (None, None, None, None, "`kidi` (Zavala #212 (AM), «Cerro, altura»), caquetío atestiguado, cubre el concepto (d19.c); estaba abierta en 6-fusion/curacion_glosas_pares_2026-09-19.yaml", "1"),
    "nomi":  (None, None, None, None, "`ateri` (Zavala #17 (GC), «Hombre»), caquetío atestiguado; y ateri va con el eyeri de las mujeres kalinago", "1"),
    "wari":  (None, None, None, None, "`iero` (Zavala #163 (GC), «Mujer»), caquetío atestiguado; iero va con lokono hiaeru / mujeres inharu (Adam 1879 p. 289)", "1"),
    "arua":  (None, None, None, None, "`ako` (Zavala #4 (E+AM), «comida»), caquetío atestiguado", "1"),
    "buri":  (None, None, None, None, "`dare` (Zavala #103, «diente; hijo (extensión metafórica)»), caquetío atestiguado, que ya lleva 'hijo'", "1"),
    # grupo 2: dos hermanas con la misma forma (N1 → A: reconstruida)
    "chaa":  ("ani", "R", "v_raiz", None, "Goeje 1939 p. 94 (visto en imagen): «faire h ani, aniro, anikua, A ani» — lokono y kalinago, la misma forma (en el kalinago es la de los hombres y la común, sigla 1 am 139, de origen arahuaco; las mujeres dicen ateka, p. 109); Perea Alonso 1942 A-NI-SIA 'lo hecho' (p. 346)", "2"),
    "masa":  ("aeke", "R", "v_raiz", None, "lokono «Aeke, manger» → mujeres kalinago «aica» (Adam 1879 p. 288, visto en imagen); Goeje 1939 p. 78 (imagen): «manger f aika … A aeke, eke». La forma lokona", "2"),
    "awa":   ("ati", "R", "v_raiz", None, "lokono «Atti-n, boire» → mujeres kalinago «ata-ca» (Adam 1879 p. 289, visto en imagen); Perea Alonso 1942 M-A-TTI-N 'no bebió' (p. 250); Goeje 1939 p. 107 (imagen): «boire f ata … A ata, ato». La raíz lokona, sin la geminada; `ata` tiene vecinas en el lexicón y no se usa", "2"),
    "suna":  ("dunku", "R", "v_raiz", None, "Goeje 1939 p. 101 (visto en imagen): «dormir f aromanka … A adunku»; Adam 1879 p. 288: lokono «Adum-ki-n» → mujeres «aroman-ca». Lokono d = kalinago r (Adam pp. 288-289). La forma lokona sin el a- del infinitivo", "2"),
    "panaa": ("aita", "R", "v_raiz", None, "Goeje 1939 p. 101 (visto en imagen): «se mémorer aritaga … A aitoa, connaître A adita, aita»: lokono aita, kalinago aritaga (d = r)", "2"),
    "kabo":  ("isi", "R", "sust", None, "Goeje 1939 p. 32 (visto en imagen): «tête … išik, išöke … A iši»; Adam 1879 p. 289: lokono «Issihi, tête» → mujeres «ichic»; Goeje p. 105 «graine, tête A isi». La raíz de las dos", "2"),
    "nii":   ("akusi", "R", "sust", None, "lokono «Aku-ssi, œil» → mujeres kalinago «n-acou» (Adam 1879 p. 288, visto en imagen); Goeje 1939 p. 33: f aku, A ako. La forma lokona", "2"),
    "wara":  ("kibe", "R", "part", None, "Goeje 1939 p. 71 (visto en imagen): «beaucoup f k-ibe … très A k-ibi, k-ibe-n» — las mujeres kalinago y el lokono. ⚠️ Queda a una letra de `kiba` 'piedra'", "2"),
    "kuru":  ("ada", "R", "sust", None, "lokono «Ada, bois, arbre, forêt» → kalinago «ara-bou, dans le bois» (Adam 1879 p. 288, visto en imagen): d = r; y el lokono ada de la Tabla A-2 de Oliver (fila 23 'tree'), cuya clave pasa a COLISIONES_A2. Mantiene la CONVIVENCIA DECLARADA de d21.16: `ada` es el árbol vivo, `bara` el palo. Pista, no atestación: el topónimo caquetío «Adabacoa» 'todo arboleda' (lexicon_zavala.TOPONIMOS_ZAVALA) — una etimología de topónimo no atestigua (tf.0, 3-a)", "2"),
    "duna":  ("uni", "R", "sust", None, "achagua «Vni, Agua» (Neira y Ribero 1762, pliego 32 izq.; V inicial = u) y lokono wuini / oni-abo: la raíz arahuaca *uni en dos de las tres hermanas que Miguel nombró. La clave achagua `uni` pasa a `uni-achagua`. `duna` era además el tuna kalina, caribe de hombres (inventario del 2026-09-23)", "2"),
    "kaya":  ("unia", "R", "sust", None, "achagua «Vnia, Lluvia» (Neira y Ribero 1762, pliego 73 der.) y lokono oni 'lluvia': la misma raíz del agua. La clave achagua `unia` pasa a `unia-achagua`. ⚠️ A una letra de `uria` 'plantío'", "2"),
    "taa":   ("butu", "R", "v_raiz", None, "Goeje 1939 p. 74 (visto en imagen, sigla fhA): «cueillir (a)bula-ka, abutu … travailler abutu, cueillir … A abuti … prendre A abutu» — el kalinago (los dos registros) y el lokono, la misma raíz; sin el prefijo a- del infinitivo, como `diki`. Hallada en la transcripción del habla de mujeres del 2026-09-24", "2"),
    # grupo 3: una hermana (N1 → A: hipotética, llega por plantilla)
    "naa":   ("kunu", "H", "v_raiz", None, "lokono cunnu 'ir' (Perea Alonso 1942 p. 623, vocabulario de Schumann) y A-CUN-TE (Fraseario p. 362, cuatro atestaciones), sin la geminada", "3"),
    "waa":   ("sile", "H", "v_raiz", None, "mujeres kalinago «venir, arriver, advenir f šile» (Goeje 1939 p. 105, visto en imagen, sigla f am: de origen arahuaco)", "3"),
    "raka":  ("hiti", "H", "v_raiz", None, "Goeje 1939 p. 110 (visto en imagen): «désirer A hiti, hite»; p. 109 «vouloir, disposé à A ahite(-ka)»; Perea Alonso 1942 -HITTI desiderativo (L-A-KI-N-HITTI-CU-MA 'quiso comer', p. 258)", "3"),
    "rua":   ("kudu", "H", "v_raiz", None, "lokono KÙDDÙ 'carga' (Perea Alonso 1942 p. 253) y cudu-cutta 'llevar' (p. 378); Goeje 1939 p. 98 «pesant A kudu»", "3"),
    "amana": ("hikihi", "H", "sust", None, "lokono HIKKI-HI 'fuego' (Perea Alonso 1942 p. 46), la forma entera: `hiki` quedaba a una letra de `diki` 'ver'", "3"),
    "arima": ("hime", "H", "sust", None, "lokono hime (Oliver 1989, Apéndice A, Tabla A-2, fila 19 'fish') e itime (Brinton). La clave lokono de la A-2 pasa a COLISIONES_A2", "3"),
    "dali":  ("wunabu", "H", "sust", None, "lokono WUNABU 'tierra' (Perea Alonso 1942 pp. 95, 70, 96; siete atestaciones). La clave lokono pasa a `wunabu-lokono`", "3"),
    "baba":  ("iti", "H", "sust", None, "lokono L-ITTI 'su padre' (Perea Alonso 1942 p. 123) y Goeje 1939 p. 42 «père A iti». `baba` se leía ba-ba (el -ba de lo que vendrá) y era caribe de hombres", "3"),
    "ka":    ("badia", "H", "part", "y, también, además (conector aditivo)", "lokono BADDIA 'y, también' (Perea Alonso 1942 p. 538; ocho atestaciones), sin la geminada. La glosa pierde el 'con' que traía `ka`: la fuente no lo da. `ka` era además homógrafa del prefijo atributivo ka-", "3"),
    "mara":  ("ika", "H", "part", None, "lokono ICCA 'pero' (Perea Alonso 1942 p. 528) y 'entonces' (p. 513)", "3"),
    "saa":   ("bena", "H", "part", "cuando, al momento de (temporal)", "lokono BENNA 'cuando' (Perea Alonso 1942 p. 504; cinco atestaciones), sin la geminada. La glosa pierde el 'si' condicional que traía `saa`: la fuente da 'cuando'. ⚠️ A una letra de `bana`", "3"),
    "naka":  ("kia", "H", "part", None, "lokono KIA 'después' (Perea Alonso 1942 p. 508; cuatro atestaciones). La clave lokono pasa a `kia-lokono`", "3"),
}
# D2 (#234): las ocho del wayuu. N1 decide la etiqueta (th.2).
K = {
    "anasa":    ("saika", "H", "v_estativo", "bueno, bien, bello", "achagua «Saica» (Neira y Ribero 1762, pliegos 43d-44i: «Saicauní, Bueno está», «Saicay, Buena casa»); en el lokono la segmentación de Perea aísla SA en la palabra que traduce BIEN (Perea Alonso 1942 p. 499, «Ú-SA-NÚ-wai … has hecho BIEN»). Dos hermanas en la raíz, la forma de una. Estativo: el estado es verbo (d21.4)"),
    "mütsia":   ("uli", "H", "v_estativo", "negro, oscuro", "kalinago «uli» 'noir', moderno wiri (Goeje 1939 p. 53, sigla 1 am 133: de origen arahuaco), con el lokono «uele-hi» 'être noir' (Goeje p. 86, columna A) detrás por la misma raíz. El kalinago tal cual: `wele` quedaba a una letra de `were` 'dar'. Estativo (d21.4)"),
    "kasuta":   ("halira", "H", "v_estativo", "blanco, claro, luminoso", "lokono «arira, hallira» 'blanc' (Goeje 1939 p. 53, columna A) y el kalinago de MUJERES «alu» (misma línea, sigla f 1 am 132 E; los hombres dicen tamone, caribe). La forma lokona en grafía fonémica. Estativo (d21.4)"),
    "sünatü":   ("kule", "H", "v_estativo", "rojo, color de la sangre", "lokono «CULE-RU Bara = el Mar BERMEJO» (Perea Alonso 1942 p. 108) y achagua «Quirrayi, Colorado» (Neira y Ribero 1762, pliego 49 izq.): l ~ r, el par que C8 declara indecidible. La forma lokona. Las mujeres kalinago dicen pona / lokono bonaro (Goeje p. 77), pero pona queda a una letra de puna y de pana. Estativo (d21.4)"),
    "outa":     ("huda", "R", "v_raiz", "morir, muerte", "lokono «huda» MORIR (Perea Alonso 1942 p. 390, siete atestaciones) y kalinago «hila» 'muerto', «hilaro» 'mourir' (Goeje 1939 p. 86, sigla fhA: arahuaco, en los dos registros). Lokono d = kalinago l es la correspondencia regular (Adam 1879 pp. 288-289): dos hermanas por N1. Verbo que es también su nombre (dc.3). La clave lokono pasa a `huda-lokono`"),
    "kataa":    ("kake", "R", "v_raiz", "vivir, vida", "kalinago de MUJERES «kakê» 'vif, vivre' y lokono «kake, koke» (Goeje 1939 p. 79, sigla fA; visto en imagen); Adam 1879 p. 290: lokono «Kaku-n, vivre» → mujeres «kake-keili, il vit encore». Dos hermanas, la MISMA forma. Verbo que es también su nombre (dc.3)"),
    "talata":   ("halikebe", "H", "v_raiz", "alegrarse, alegría, contento", "lokono «halli-kebbe» ALEGRAR, GOZAR, DICHOSO (Perea Alonso 1942 pp. 231, 336, 112; cinco atestaciones), el mismo «ahali-kibi» de Goeje 1939 (p. 86, columna A) y el «hallikebe-de, je me réjouis» de Adam 1879 (p. 298). Una hermana, tres fuentes; la kalinago (a)ulabu no comparte forma. Verbo que es también su nombre (dc.3)"),
    "jashichi": ("aiima", "H", "sust", "rabia, ira, enojo", "el lokono TAL CUAL: «k-aiima» 'fâché' sin el atributivo (Goeje 1939 p. 116, columna A), la misma raíz que Perea Alonso 1942 segmenta en A-IMA-TTU-NNUA IRA (p. 56) y que el kalinago de mujeres dice iam. Dos hermanas en la raíz, la forma de una. Con el atributivo, «ka-aiima» 'tiene enojo' es el lokono k-aiima. `ima` y `aima` no se pueden usar: son sufijos del motor (REGLAS_ZAVALA)"),
}

ARCH_NUC = "2026-09-24 · tanda de las hermanas · núcleo fundacional (th.7, grupo {g})"
ARCH_K = "2026-09-24 · tanda de las hermanas · D2 (th.2): derivada del wayuu"

archivadas = {}      # clave -> entrada con archivada + nota
reemplazos = {}      # índice de línea -> texto nuevo (o None = borrar)

for vieja, (nueva, capa, cat, sig, der, g) in N.items():
    idx = linea_de(vieja, 0, FIN_BASE)
    assert len(idx) == 1, (vieja, idx)
    k, e = parse(lines[idx[0]])
    assert k == vieja
    e = dict(e)
    if nueva is None:
        motivo = f"la atestiguada ya lo dice: {der}"
        manda = der.split("`")[1]
        e["archivada"] = ARCH_NUC.format(g=g) + f" · manda `{manda}`"
    else:
        motivo = f"la sustituye `{nueva}`, de las hermanas"
        e["archivada"] = ARCH_NUC.format(g=g) + f" · la sustituye `{nueva}`"
    e["notas"] = (f"{e.get('notas', '')} · ARCHIVADA DEL HABLA 2026-09-24 (tanda de las "
                  f"hermanas, {FRASE}): citaba un cognado sin obra ni página y casi "
                  f"ninguna hermana le daba pareja (6-fusion/inventario_nucleo_fundacional_2026-09-23.yaml); "
                  f"{motivo}. LA CAPA NO SE TOCA. Propuesta: {PN}")
    archivadas[vieja] = e
    if nueva is None:
        reemplazos[idx[0]] = None
    else:
        fuente = "caquetío-reconstruido" if capa == "R" else "caquetío-hipotético"
        cuantas = ("Dos hermanas con la misma forma o con la correspondencia regular declarada (N1 → A): reconstruida"
                   if capa == "R" else
                   "Una hermana (N1 → A): hipotética; el perfil era2 no la muestrea y llega por plantilla")
        nota = (f"Tanda de las hermanas (2026-09-24, {FRASE}), núcleo fundacional grupo {g}. "
                f"{der}. {cuantas}. Sustituye a `{vieja}` ('{e['sig']}'), que citaba «cognado» sin obra. "
                f"Propuesta: {PN}; decisión: {DEC}")
        nuevo = {"sig": sig or e["sig"], "cat": cat or e["cat"], "fuente": fuente, "notas": nota}
        reemplazos[idx[0]] = emit(nueva, nuevo)

for vieja, (nueva, capa, cat, sig, der) in K.items():
    idx = linea_de(vieja, 0, FIN_BASE)
    assert len(idx) == 1, (vieja, idx)
    k, e = parse(lines[idx[0]])
    e = dict(e)
    e["archivada"] = ARCH_K + f" · la sustituye `{nueva}`"
    e["notas"] = (f"{e.get('notas', '')} · ARCHIVADA DEL HABLA 2026-09-24 (tanda de las hermanas, "
                  f"D2, {FRASE}): la reconstruyeron desde el wayuu y la campaña de las voces "
                  f"wayuu no la vio (su nota decía «deuda de D11», no «DEUDA D11»); la sustituye "
                  f"`{nueva}`. LA CAPA NO SE TOCA. Propuesta: {PK}")
    archivadas[vieja] = e
    fuente = "caquetío-reconstruido" if capa == "R" else "caquetío-hipotético"
    cuantas = ("Dos hermanas (N1 → A, th.2): reconstruida" if capa == "R" else
               "Menos de dos hermanas con la misma forma (N1 → A, th.2): hipotética; el perfil era2 no la muestrea y la enseña la plantilla breve (línea VOCES)")
    nota = (f"Tanda de las hermanas (2026-09-24, {FRASE}), D2 de #234: las voces que seguían "
            f"saliendo del wayuu. {der}. {cuantas}. Sustituye a `{vieja}` ('{e['sig']}'). "
            f"Propuesta: {PK}; decisión: {DEC}")
    reemplazos[idx[0]] = emit(nueva, {"sig": sig, "cat": cat, "fuente": fuente, "notas": nota})

# D3: alaain y japü
for vieja, nueva in (("alaain", None), ("japü", "aburi")):
    idx = linea_de(vieja, 0, FIN_BASE)
    assert len(idx) == 1, (vieja, idx)
    k, e = parse(lines[idx[0]])
    e = dict(e)
    if nueva:
        e["archivada"] = "2026-09-24 · tanda de las hermanas · D3 (th.3): etiquetada wayuu, sin cita · la sustituye `aburi`"
        mot = "la sustituye `aburi` 'tener vergüenza', de dos hermanas"
    else:
        e["archivada"] = "2026-09-24 · tanda de las hermanas · D3 (th.3): etiquetada wayuu, sin cita · sin sustituta"
        mot = ("sin sustituta: 'amar' es mujeres kalinago inši / lokono ansi (Goeje 1939 p. 95), "
               "dos hermanas, pero el grupo ns no pasa la fonotáctica atestiguada")
    e["notas"] = (f"{e.get('notas', '')} · ARCHIVADA DEL HABLA 2026-09-24 (tanda de las hermanas, "
                  f"D3, {FRASE}): {mot}. LA CAPA NO SE TOCA. Propuesta: {PK}")
    archivadas[vieja] = e
    if nueva:
        nota = (f"Tanda de las hermanas (2026-09-24, {FRASE}), D3 de #234. Goeje 1939 p. 74 (visto en "
                f"imagen): «avoir honte f aburi … A (h)aburi» — las mujeres kalinago y el lokono, la misma "
                f"forma: reconstruida (N1 → A). Verbo que es también su nombre (dc.3). Sustituye a `japü` "
                f"('{e['sig']}'). ⚠️ HOMÓGRAFO DECLARADO: `aburi` es también una grafía del glosario de "
                f"Zavala como TOPÓNIMO («Para designar las aguas de un río lleno de arena», "
                f"lexicon_zavala.TOPONIMOS_ZAVALA), fuera del habla y fuera de 2-lengua/toponimos.yaml: "
                f"no choca en VOCABULARIO_BASE. Propuesta: {PK}; decisión: {DEC}")
        reemplazos[idx[0]] = emit("aburi", {"sig": "tener vergüenza; vergüenza, pudor", "cat": "v_raiz",
                                            "fuente": "caquetío-reconstruido", "notas": nota})
    else:
        reemplazos[idx[0]] = None

# ── re-etiquetas y notas en entradas que se quedan ─────────────────────
def anotar(clave, nota, fuente=None, desde=0, hasta=None):
    idx = linea_de(clave, desde, FIN_BASE if hasta is None else hasta)
    assert len(idx) == 1, (clave, idx)
    i = idx[0]
    if i in reemplazos:
        raise SystemExit(f"{clave} ya tocada")
    k, e = parse(lines[i])
    e = dict(e)
    if fuente:
        e["fuente_antes"] = e["fuente"]
        e["fuente"] = fuente
    antes = e.pop("fuente_antes", None)
    extra = f" (era `{antes}`)" if antes and antes != e["fuente"] else ""
    e["notas"] = f"{e.get('notas', '')} · {nota}{extra}"
    # conservar el orden original de claves
    _, orig = parse(lines[i])
    e2 = {kk: e[kk] for kk in orig if kk in e}
    e2.update({kk: v for kk, v in e.items() if kk not in e2})
    reemplazos[i] = "    " + lines[i].strip().split(":", 1)[0] + ": " + "{" + ", ".join(
        f'"{kk}": {q(v)}' for kk, v in e2.items()) + "},"

D1 = (f"D1 de la tanda de las hermanas (2026-09-24, {FRASE}): el habla de MUJERES kalinago "
      f"cuenta como hermana (es la capa arahuaca: Adam 1879 pp. 279-280) y dice la misma forma que "
      f"el lokono — {{f}} (Goeje 1939 p. 24; Adam 1879 pp. 277-279). Dos hermanas con la misma forma: "
      f"pasa a RECONSTRUIDO (N1 → A). Propuesta: {PK} §decision_d1")
anotar("bui", D1.format(f="lokono bu-, kalinago b(u)-, boukoya 'tú'"), "caquetío-reconstruido")
anotar("lihi", D1.format(f="lokono li-hi, kalinago l(i)- (común), likia 'él'"), "caquetío-reconstruido")
anotar("tuhu", D1.format(f="lokono tu-hu, kalinago t(u)- (común), tokoya 'ella'"), "caquetío-reconstruido")
anotar("dai", (f"D1 de la tanda de las hermanas (2026-09-24): el habla de mujeres kalinago NO apoya "
               f"esta forma — dice n(u)-, noukoya 'yo' (Goeje 1939 p. 24; Adam 1879 p. 278), como el "
               f"achagua nu-. Dos hermanas contra dos: `dai` se queda por lokono + taíno (tf.1). Propuesta: {PK}"))
anotar("diki", (f"N1 de la tanda de las hermanas (2026-09-24, {FRASE}): gana la segunda hermana — "
                f"mujeres kalinago «arika», A adika (Goeje 1939 p. 100, visto en imagen; lokono d = "
                f"kalinago r, Adam 1879 pp. 288-289): pasa a RECONSTRUIDO. Propuesta: {PN}"),
       "caquetío-reconstruido")
anotar("marisi", (f"N1 de la tanda de las hermanas (2026-09-24, {FRASE}): la forma tiene dos hermanas "
                  f"— «maïs … f mariši, A mariši» (Goeje 1939 p. 65, visto en imagen), la MISMA en las "
                  f"mujeres kalinago y en el lokono: pasa a RECONSTRUIDO y deja de ser una acuñación "
                  f"sin cita. Propuesta: {PN}"),
       "caquetío-reconstruido")
G4 = {
    "kaa":  "se queda y se DEGRADA: ninguna hermana da una cópula que se parezca, y cambiarla tocaría toda la gramática enseñada",
    "maa":  "se queda con cita: achagua «Numau, Decir» = nu-ma-u (Neira y Ribero 1762, pliego 55 der.), una hermana",
    "suka": "se queda con cita: lokono CA-SACCU-DA 'de noche' (Perea Alonso 1942 p. 71), una hermana",
    "ama":  "se queda y se degrada: voz infantil que casi toda lengua tiene; no es evidencia de parentesco",
    "bari": "se queda y se degrada: ninguna hermana le da pareja",
    "puna": "se queda y se degrada: ninguna hermana le da pareja",
}
for k, t in G4.items():
    anotar(k, (f"Tanda de las hermanas (2026-09-24, {FRASE}), núcleo fundacional grupo 4: {t}. "
               f"Pasa a HIPOTÉTICO (N1 → A: no llega a dos hermanas); el perfil era2 no la muestrea y "
               f"llega por plantilla. Propuesta: {PN}"),
           "caquetío-hipotético")

# T4: la pareja taína en las voces que viven en curiana_lexicon
T4 = {
    "kiba":     "taíno «siba, Ciba» 'piedra' (Pané; Las Casas vía Coll y Toste 1897 p. 209), de cronista del XVI. Es una de las tres parejas k ~ s (kiba/siba, kabana/sabana, kiwa/sigua) que T11 dejó en «indecidible» con dos apoyos: se vuelve a correr después de la corrida base (T5)",
    "waitiao":  "taíno «guaitiao, guatiao» 'amigo' (Herrera vía Coll y Toste 1897 p. 219; Brinton p. 12), de cronista; la pareja que T11 ya estudió (diao/daitiao)",
    "jagey":    "taíno «jagüey» 'depósito de agua dulce' (Coll y Toste 1897 p. 232) y T xagueye 'citerne naturelle' (Goeje 1939 p. 57), de la tradición viva de Puerto Rico",
    "warawara": "taíno «guaraguao» 'ave de rapiña' (Coll y Toste 1897 pp. 223, 156), de la tradición viva: rapaz, y voz imitativa",
}
# jagey, waitiao y warawara están fuera del bloque del núcleo: buscar en todo VOCABULARIO_BASE
for k, t in T4.items():
    idx = linea_de(k, 0, FIN_BASE)
    assert len(idx) == 1, (k, idx)
    anotar(k, (f"T4 de la tanda de las hermanas (2026-09-24, {FRASE}): pareja en la ESFERA — {t}. "
               f"Comparanda de la esfera, no evidencia de préstamo ni de parentesco por sí sola; no "
               f"cambia glosa ni capa. Propuesta: {PT} §el_cruce"))

# ── renombres de claves lokono (Perea) ─────────────────────────────────
for vieja, voz in (("huda", "'morir, muerte' (D2, th.2)"), ("kia", "'después' (núcleo, grupo 3)"),
                   ("wunabu", "'tierra' (núcleo, grupo 3)")):
    idx = [i for i in linea_de(vieja) if i < FIN_BASE]
    lok = [i for i in idx if '"fuente": "lokono"' in lines[i]]
    assert len(lok) == 1, (vieja, idx)
    i = lok[0]
    k, e = parse(lines[i])
    e = dict(e)
    e["notas"] = (f"CLAVE CAMBIADA 2026-09-24 (tanda de las hermanas): era `{vieja}`; la voz sin "
                  f"etiqueta es ahora la caquetía {voz}, que sale de esta misma forma lokona · " + e["notas"])
    reemplazos[i] = emit(f"{vieja}-lokono", e)

# ── escribir ───────────────────────────────────────────────────────────
nuevas_lineas = []
for i, l in enumerate(lines):
    if i in reemplazos:
        if reemplazos[i] is not None:
            nuevas_lineas.append(reemplazos[i])
        continue
    nuevas_lineas.append(l)
    if l.startswith("FUERA_DEL_HABLA: dict"):
        pass

txt = "\n".join(nuevas_lineas)

# el bloque de archivo, al final de FUERA_DEL_HABLA
bloque = ["    # ── Tanda de las hermanas (2026-09-24): «Acepto todo lo recomendado» ──────",
          "    # El núcleo fundacional rehecho desde el lokono y el habla de mujeres",
          "    # kalinago (th.7), las ocho voces que seguían saliendo del wayuu (D2, th.2)",
          "    # y alaain/japü (D3, th.3). LA CAPA NO SE TOCA. Decisiones en",
          f"    # {DEC}."]
for k, e in archivadas.items():
    bloque.append(emit(k, e))
cierre = "\n}"
i_fuera = txt.index("FUERA_DEL_HABLA: dict[str, dict] = {")
i_cierre = txt.index("\n}", i_fuera)
txt = txt[:i_cierre] + "\n" + "\n".join(bloque) + txt[i_cierre:]

for vieja, e in archivadas.items():
    print(f"  archivada   {vieja:10} {e['fuente']:24} {e['archivada']}")
nuevas = [l.strip().split(":", 1)[0] for i, l in sorted(reemplazos.items()) if l]
print(f"  escritas    {len(nuevas)} entradas: {', '.join(k.strip(chr(34)) for k in nuevas)}")
print(f"archivadas: {len(archivadas)} | líneas tocadas: {len(reemplazos)}")
if ARGS.dry_run:
    print("--dry-run: no se escribe nada")
    sys.exit(0)
open(P, "wb").write(txt.replace("\n", EOL).encode("utf-8"))
print("✓ curiana_sim/curiana_lexicon.py")
