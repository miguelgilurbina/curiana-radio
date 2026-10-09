#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Censo de la CREENCIA en el vocabulario achagua de Neira y Ribero 1762, y
validador de la propuesta de la minería del 2026-10-09:

    6-fusion/creencia_achagua_2026-10-09.yaml

La pregunta (4-fuentes/sesiones/08_creencia_achagua_que-minar.md, 2º): ¿qué
campo léxico de la creencia registra el vocabulario, qué lemas pidió el
jesuita para la DOCTRINA y cuáles nombran algo INDÍGENA? El plan pide que el
censo lo emita un script y no una lista escrita a mano (regla 1).

Qué hace:

1. Lee `vocabulario` de 6-fusion/achagua_neira_ribero_1762.yaml (la
   transcripción por visión del 2026-09-12; no la corrige).
2. Asigna cada lema castellano al PRIMER campo cuya expresión regular casa
   (dioses_y_seres, alma_y_persona, especialista, muerte, fiesta_y_ayuno,
   cielo, sueno). Un lema cuenta una sola vez.
3. Le pone una marca a cada lema: `doctrina` si casa con la regla de
   doctrina y no con la indígena, `indigena` al revés, `dudoso` si casan las
   dos o ninguna. ES UNA REGLA ESCRITA AQUÍ, no un juicio entrada por
   entrada: sirve para orientar. Los hechos de la propuesta se juzgan uno a
   uno, con la imagen delante.
4. Cuenta las voces con `-minari` (y `-minarro`) en la columna achagua o en
   el ejemplo, para medir si «dueño» es una categoría religiosa o un sufijo
   de uso general.
5. Valida la propuesta: ids únicos, campos obligatorios, `fuente` en
   4-fuentes/bibliografia.yaml (regla 8), y valores permitidos de `medio` y
   `capa`.

El censo vive en la propuesta entre las marcas `# >>> censo_neira` y
`# <<< censo_neira`; no se edita a mano.

    python 6-fusion/scripts/censo_creencia_neira_ribero.py            # valida y comprueba que el censo está al día
    python 6-fusion/scripts/censo_creencia_neira_ribero.py --escribir # reescribe el bloque del censo
    python 6-fusion/scripts/censo_creencia_neira_ribero.py --imprimir # imprime el censo, sin tocar nada

No llama a ninguna API ni a la red, y no toca la base.
"""

import argparse
import io
import os
import re
import sys
import unicodedata

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NEIRA = os.path.join(RAIZ, "6-fusion", "achagua_neira_ribero_1762.yaml")
PROPUESTA = os.path.join(RAIZ, "6-fusion", "creencia_achagua_2026-10-09.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")

MARCA_INI = "# >>> censo_neira"
MARCA_FIN = "# <<< censo_neira"

# Orden = prioridad: un lema va al primer campo que casa.
CAMPOS = [
    ("dioses_y_seres", r"\bdios|\bydol|\bidol|demoni|diablo|duende|criador|criar de nada|gentil|"
                       r"\bangel|infierno|dueno del|blanc[oa] espa"),
    ("alma_y_persona", r"\balma\b|\banima\b|espiritu|\bsombra|parasism|revivir|resucit|"
                       r"bolver en si|desmay"),
    ("especialista", r"brujo|bruger|hechi|encant|ensalm|aguer|agurar|adivin|\bmedic|yerbat|"
                     r"veneno|tabaco|sahum"),
    ("muerte", r"difunt|muert|cadaver|sepult|enterr|antepasad|ofrenda|honras|\bllant|\bllor|"
               r"luto|viud|\bhueso"),
    ("fiesta_y_ayuno", r"ayun|abstin|borrach|embriag|bebeson|\bbail|\bdanz|mudanza|flauta|"
                       r"convite|\bboda\b|fiesta|\bchicha\b|disfra|mascara"),
    ("cielo", r"cielo|estrella|lucero|cabrilla|santiago|cometa|eclips|trueno|\brayo|relampag|"
              r"diluvio|\bluna\b|^sol\b|tempestad|crucero|temblor"),
    ("sueno", r"sueñ|soñ"),
]

DOCTRINA = re.compile(
    r"^dios\b(?!es de los)|criar de nada|ser dios|dar el alma|confiar|infierno|gloria|pecad|"
    r"bautis|confes|sacrament|\bsant[oa]\b|\bangel|gentil|ydolatr|idolatr|blasfem|cristian|"
    r"\bmisa\b|iglesia|resucit|^alma$|^espiritu|demonio|diablo|criador|rezar|rezo")
INDIGENA = re.compile(
    r"de los achaguas|^diosas|^ydolo$|brujo|bruger|encant|ensalm|hechizo del|hechizar|aguer|"
    r"agurar|ofrenda de difuntos|honras de|convite|^boda|cabrillas|santiago|carro del cielo|"
    r"crucero|lucero|cometa|eclipse|duende|blanc[oa] espa|anima en el cuerpo|yerbatero|^medico|"
    r"borrach|bebeson|flauta|mudanza|diluvio|trueno|^rayo|relampago|tempestad|tabaco|sahumar|"
    r"ayuno tal|antepasado|sepult|enterrar|desenterrar|llanto|llorar|lloron|dueno del cielo|"
    r"bolver en si|desmayarse|revivir|parasismo|^cielo$|^luna$|^sol$|^estrella$")

MEDIOS = {"proyectable", "no-proyectable"}
CAPAS = {"reconstruido", "hipotetico", "lectura", "no-se-proyecta"}
OBLIGATORIOS = ("id", "contenido", "cita", "fuente", "pagina", "verificado_en_imagen", "pueblo",
                "describe", "medio", "capa", "proyeccion", "via_a")


def _forzar_utf8():
    """La consola de Windows es cp1252 y revienta con « o ñ."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def normalizar(s, conservar_enie=False):
    """Minúsculas y sin diacríticos; la ñ se conserva si se pide (soñar ≠ sonar)."""
    s = str(s or "").lower()
    if conservar_enie:
        s = s.replace("ñ", "\x00")
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return s.replace("\x00", "ñ")


def marca(lema):
    n = normalizar(lema)
    d, i = bool(DOCTRINA.search(n)), bool(INDIGENA.search(n))
    if i and not d:
        return "indigena"
    if d and not i:
        return "doctrina"
    return "dudoso"


def etiqueta(e):
    return f"{e.get('pliego')} {e.get('lado')}"


def censar():
    d = yaml.safe_load(open(NEIRA, encoding="utf-8"))
    voc = d["vocabulario"]
    por_campo = {c: [] for c, _ in CAMPOS}
    for e in voc:
        lema = normalizar(e.get("castellano"), conservar_enie=True)
        for campo, pat in CAMPOS:
            if re.search(pat, lema):
                por_campo[campo].append(e)
                break
    minari = [e for e in voc
              if "minar" in normalizar(f"{e.get('achagua', '')} {e.get('ejemplo', '')}")]
    # La cobertura del ensamblador mide huecos por PLIEGO; aquí se mide por LADO,
    # porque cada JPG trae dos páginas y una sola puede faltar.
    lados = {}
    for e in voc:
        clave = (e.get("pliego"), e.get("lado"))
        lados[clave] = lados.get(clave, 0) + 1
    pliegos = sorted({p for p, _ in lados if isinstance(p, int)})
    sin_entradas = [f"{p} {l}" for p in range(pliegos[0], pliegos[-1] + 1)
                    for l in ("izq", "der") if lados.get((p, l), 0) == 0]
    en_creencia = {id(e) for lista in por_campo.values() for e in lista}

    resumen = {}
    entradas = {}
    for campo, lista in por_campo.items():
        marcas = [marca(e.get("castellano")) for e in lista]
        resumen[campo] = {
            "lemas": len(lista),
            "doctrina": marcas.count("doctrina"),
            "indigena": marcas.count("indigena"),
            "dudoso": marcas.count("dudoso"),
        }
        entradas[campo] = [
            f"{etiqueta(e)} · {e.get('castellano')} = {e.get('achagua')} · {m}"
            for e, m in zip(lista, marcas)
        ]
    return {
        "fuente": "6-fusion/achagua_neira_ribero_1762.yaml, `vocabulario` (transcripción por visión, 2026-09-12)",
        "generado_por": "6-fusion/scripts/censo_creencia_neira_ribero.py",
        "como_se_lee": (
            "Cada lema va a un solo campo (el primero que casa). La marca doctrina/indigena/dudoso "
            "es una regla escrita en el script, no un juicio entrada por entrada. Las formas son "
            "las del YAML de la transcripción: las que cita la propuesta se vieron en imagen y, "
            "donde la imagen difiere, lo dice el hecho."),
        "vocabulario_entradas": len(voc),
        "lados_sin_entradas": {
            "que_mide": ("páginas (lado izq/der de cada JPG) del tramo del vocabulario sin ninguna "
                         "entrada en el YAML. El 28 izq es el final del arte y el 98 der está en "
                         "blanco (meta.estructura_del_manuscrito_medida); las demás son páginas "
                         "sin transcribir."),
            "lados": sin_entradas,
        },
        "por_campo": resumen,
        "lemas_de_creencia": sum(r["lemas"] for r in resumen.values()),
        "minari": {
            "entradas": len(minari),
            "de_ellas_en_lemas_de_creencia": sum(1 for e in minari if id(e) in en_creencia),
            "lista": [f"{etiqueta(e)} · {e.get('castellano')} = {e.get('achagua')}" for e in minari],
        },
        "entradas": entradas,
    }


def bloque(censo):
    texto = yaml.safe_dump({"censo_neira": censo}, allow_unicode=True, sort_keys=False, width=100)
    return f"{MARCA_INI} (generado por {censo['generado_por']}; no se edita a mano)\n{texto}{MARCA_FIN}\n"


def partes(texto):
    i = texto.find(MARCA_INI)
    j = texto.find(MARCA_FIN)
    if i < 0 or j < 0 or j < i:
        return None
    fin = texto.find("\n", j)
    fin = len(texto) if fin < 0 else fin + 1
    return texto[:i], texto[i:fin], texto[fin:]


def validar(propuesta):
    errores = []
    obras = {o["id"] for o in yaml.safe_load(open(BIBLIO, encoding="utf-8"))["obras"]}
    ids = set()
    secciones = [("hechos", propuesta.get("hechos") or [])]
    for nombre, lista in secciones:
        for h in lista:
            hid = h.get("id", "?")
            for k in OBLIGATORIOS:
                if k not in h:
                    errores.append(f"{hid}: falta `{k}`")
            if hid in ids:
                errores.append(f"{hid}: id repetido")
            ids.add(hid)
            fuentes = h.get("fuente")
            for f in fuentes if isinstance(fuentes, list) else [fuentes]:
                if f not in obras:
                    errores.append(f"{hid}: la fuente `{f}` no está en 4-fuentes/bibliografia.yaml")
            if h.get("medio") not in MEDIOS:
                errores.append(f"{hid}: medio `{h.get('medio')}` no es {sorted(MEDIOS)}")
            if h.get("capa") not in CAPAS:
                errores.append(f"{hid}: capa `{h.get('capa')}` no es {sorted(CAPAS)}")
    for h in propuesta.get("fuera_del_encargo") or []:
        hid = h.get("id", "?")
        if hid in ids:
            errores.append(f"{hid}: id repetido")
        ids.add(hid)
        f = h.get("fuente")
        if f not in obras:
            errores.append(f"{hid}: la fuente `{f}` no está en 4-fuentes/bibliografia.yaml")
    return errores, len(ids)


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--escribir", action="store_true", help="reescribe el bloque del censo en la propuesta")
    ap.add_argument("--imprimir", action="store_true", help="imprime el censo y sale")
    a = ap.parse_args()

    censo = censar()
    nuevo = bloque(censo)
    if a.imprimir:
        print(nuevo)
        return 0

    texto = open(PROPUESTA, encoding="utf-8").read()
    p = partes(texto)
    if p is None:
        print(f"✗ no encuentro las marcas `{MARCA_INI}` / `{MARCA_FIN}` en {PROPUESTA}")
        return 1
    antes, viejo, despues = p
    if a.escribir:
        texto = antes + nuevo + despues
        with open(PROPUESTA, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto)
        print(f"✓ censo escrito en {os.path.relpath(PROPUESTA, RAIZ)}")
    elif viejo != nuevo:
        print("✗ el censo de la propuesta no es el que mide el script: corre con --escribir")
        return 1

    propuesta = yaml.safe_load(texto)
    errores, n = validar(propuesta)
    for e in errores:
        print("✗", e)
    if errores:
        return 1
    r = censo["por_campo"]
    print(f"✓ propuesta válida: {n} ids; censo al día "
          f"({censo['lemas_de_creencia']} lemas de creencia en {len(r)} campos; "
          f"{censo['minari']['entradas']} voces con -minari)")
    # Los recuentos de la nota de sesión salen de aquí (regla 1).
    hechos = propuesta.get("hechos") or []
    for clave in ("capa", "medio", "pueblo"):
        cuenta = {}
        for h in hechos:
            cuenta[h.get(clave)] = cuenta.get(h.get(clave), 0) + 1
        print(f"  hechos por {clave}: " + " · ".join(f"{k} {v}" for k, v in sorted(cuenta.items())))
    cruce = {}
    for h in hechos:
        k = (h.get("capa"), h.get("medio"))
        cruce[k] = cruce.get(k, 0) + 1
    print("  capa × medio: " + " · ".join(f"{c}/{m} {v}" for (c, m), v in sorted(cruce.items())))
    print(f"  fuera del encargo: {len(propuesta.get('fuera_del_encargo') or [])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
