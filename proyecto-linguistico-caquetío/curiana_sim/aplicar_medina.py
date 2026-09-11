#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aplicar_medina.py — fusiona al canon lo que el dictado de Medina Colina ganó.

Autorizado por Miguel el 2026-09-09. Registro de la propuesta:
`6-fusion/medina_colina_dictado.yaml`; protocolo y escala de veredicto en
`5-experimento/disenos/02_protocolo_habla_paraguanera.md` §5.

QUÉ HACE, Y QUÉ NO
------------------
1. SANEA la estructura de la propuesta. Treinta voces con veredicto A, B o C
   quedaron archivadas bajo `descartes` porque las tandas de días distintos se
   fueron pegando en la lista equivocada. Se mueven a `entradas`, que es donde
   dicen sus propios veredictos que van. No cambia ningún veredicto.

2. AÑADE al lexicón las voces de nivel A que NO estaban, ni por su forma ni por
   su lema fonémico. Medido: son DOS. El resto de las 21 voces A ya estaban —
   `guacoa` es `wakoa`, `cacuro` es `kakuro`, `arifuque` es `harifuche`,
   `chirigua` es `chirwa`—, así que el dictado no añadió vocabulario ahí: añadió
   atestación.

3. ESCRIBE LA TABLA DE CORROBORACIÓN en la bitácora de la fuente,
   `4-fuentes/medina-colina-sxx.md`. Es el rendimiento real del dictado: subir
   entradas de «una fuente» a «dos o tres independientes».

   NO se tocan las `notas` del lexicón, y hay un motivo medido: catorce de esas
   dieciséis entradas no viven en `curiana_lexicon.py` sino en
   `lexicon_zavala.py`, que es GENERADO por `minar_zavala_glosario.py` y que
   CLAUDE.md marca como trampa —regenerarlo cambia `score_linguistico()`—.
   Editarlas a mano sería escribir en algo que la próxima regeneración borra.
   La bitácora de `4-fuentes/` es, por la regla 7, el sitio donde vive «qué se
   preguntó, qué se halló».

NO toca los niveles B ni C. El protocolo §5 es explícito: B va al corpus
cultural y **al lexicón activo no**, salvo decisión explícita; C sólo al corpus.
Meter formas no verificadas en VOCABULARIO_BASE es lo que produjo los falsos
positivos de `score_linguistico`, y el propio protocolo lo dice.

    python aplicar_medina.py --dry-run
    python aplicar_medina.py
"""

import argparse
import io
import os
import re
import sys
import unicodedata

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DICTADO = os.path.join(RAIZ, "6-fusion", "medina_colina_dictado.yaml")
LEXICON = os.path.join(AQUI, "curiana_lexicon.py")
MARCA = "    # -- FIN VOCABULARIO_BASE --"


def _forzar_utf8():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


def fonemizar(s):
    """El lema fonémico de D5: `guacoa` y `wakoa` son la misma palabra."""
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"gu(?=[aeio])", "w", s)
    s = re.sub(r"qu(?=[ei])", "k", s)
    s = re.sub(r"c(?=[ei])", "s", s)
    s = s.replace("ch", "C").replace("c", "k").replace("z", "s").replace("v", "b")
    s = re.sub(r"[^a-zC]", "", s)
    return re.sub(r"(.)\1+", r"\1", s)


# ── Las dos entradas nuevas. Escritas a mano porque cada una lleva su
#    procedencia y su reserva, que no se derivan del YAML. ────────────────
NUEVAS = {
    "karebe": {
        "sig": "cuchara, cucharón de media tapara con mango de madera",
        "cat": "sust",
        "fuente": "caquetío-atestiguado",
        "categoria": "casa",
        "notas": (
            "DOS atestaciones independientes a los dos lados del Golfete y con "
            "128 años entre ellas: Gatschet 1885 la recoge en ARUBA como «karebe "
            "spoon» (lista de voces arahuacas de la isla), y Medina Colina 2013 "
            "p. 64 la da viva en PARAGUANÁ — «una especie de cucharón que se "
            "hacía con media tapara, atravesada por sus bordes por un mango de "
            "madera; era utilizado para servir comida» (dictado de Miguel, "
            "2026-09-01). Alvarado 1921 p. 62 describe el mismo objeto («de "
            "forma oval, a la que sirve de mango la parte más angosta del óvalo; "
            "fabrícala del fruto del totumo y úsala en Occidente») pero le "
            "atribuye origen andino (cf. guahibo kariepa) y dice que en Oriente "
            "se desconoce — RESERVA DECLARADA: la atestación insular es lo que "
            "la hace caquetía, no la etimología, que Alvarado disputa. El objeto "
            "es precontacto (la totuma como cucharón es pancaribeña)."),
    },
    "urupagua": {
        "sig": ("arbusto espinoso usado para cercar conucos; y árbol de la "
                "serranía coriana de fruto amargo comestible tras larga cocción"),
        "cat": "sust",
        "fuente": "caquetío-atestiguado",
        "categoria": "flora",
        "notas": (
            "TRES fuentes independientes y DOS topónimos. Alvarado 1921 p. 305 "
            "URUPÁGUA: «Árbol indeterminado de Coro. Fruto elipsoide, cuando "
            "seco, de 1½ pulgada de largo, con cáscara dura y un contenido "
            "libre, compacto, harinoso, amarillento» — que la ciencia no supiera "
            "darle taxón es señal de voz local no castellanizable. Esteves 1989 "
            "da los topónimos URUPAGUADUCO «la quebrada de las urupaguas» (p. 71) "
            "y Urupagua. Medina Colina 2013 p. 292 la da viva en Paraguaná y "
            "distingue las DOS clases: el arbusto espinoso de las cercas "
            "(Paraguaná) y el árbol de la sierra de fruto amargo, con refrán "
            "dentro — «tiene más coraje que el que se comió la primera "
            "urupagua» (dictado de Miguel, 2026-09-08). Distribución restringida "
            "a la Curiana. La etiqueta descansa en la vía toponímica: no hay "
            "atestación en boca caquetía, sí convergencia de tres testigos y el "
            "topónimo. Deuda: procesar Urupagua y Urupaguaduco en la campaña de "
            "topónimos con esta voz como lectura."),
    },
}


def cargar_dictado():
    return yaml.safe_load(io.open(DICTADO, encoding="utf-8").read())


# ── 1. sanear la estructura de la propuesta ─────────────────────────────
# Por CIRUGÍA DE TEXTO, no reescribiendo el YAML: el cuerpo tiene 104
# comentarios —notas de método, citas de Miguel, referencias a las reglas— y
# un `safe_dump` los borraría todos. Los bloques se mueven tal cual están.

def _bloques(lineas, ini, fin):
    """Parte una sección en bloques `  - voz: ...`. Devuelve (voz, i, j)."""
    marcas = [n for n in range(ini, fin) if lineas[n].startswith("  - voz:")]
    for k, n in enumerate(marcas):
        m = marcas[k + 1] if k + 1 < len(marcas) else fin
        voz = lineas[n].split("voz:", 1)[1].strip().strip('"\'')
        yield voz, n, m


def sanear_estructura(seco):
    texto = io.open(DICTADO, encoding="utf-8").read()
    lineas = texto.splitlines(keepends=True)
    n_ent = next(n for n, l in enumerate(lineas) if l.startswith("entradas:"))
    n_des = next(n for n, l in enumerate(lineas) if l.startswith("descartes:"))

    mover = []
    for voz, a, b in _bloques(lineas, n_des + 1, len(lineas)):
        bloque = "".join(lineas[a:b])
        for linea in bloque.splitlines():
            if linea.strip().startswith("veredicto:"):
                if linea.split("veredicto:", 1)[1].strip().strip('"\'')[:1] in "ABC":
                    mover.append((voz, a, b))
                break

    if not mover:
        print("  estructura: ya saneada (0 voces A/B/C bajo descartes)")
        return
    print(f"  estructura: {len(mover)} voces A/B/C archivadas bajo `descartes` "
          f"-> se mueven a `entradas`")
    print("    " + ", ".join(sorted(v for v, _, _ in mover)))
    if seco:
        return

    bloques = ["".join(lineas[a:b]) for _, a, b in mover]
    # el comentario que precede a `descartes:` se queda con descartes
    corte = n_des
    while corte > 0 and (lineas[corte - 1].startswith("#")
                         or not lineas[corte - 1].strip()):
        corte -= 1

    aviso = ("\n  # ── Movidas aquí el 2026-09-09 (aplicar_medina.py): estas voces\n"
             "  # llevaban veredicto A, B o C y estaban archivadas bajo `descartes`\n"
             "  # porque las tandas de días distintos se pegaron en la lista\n"
             "  # equivocada. Ni un veredicto cambió: sólo su sitio.\n")

    nuevas_lineas = (lineas[:corte] + [aviso] + bloques + lineas[corte:])
    fuera = {id(b) for b in bloques}
    salida, saltar = [], set()
    for _, a, b in mover:
        saltar |= set(range(a, b))
    # reconstruir: la parte de descartes sin los bloques movidos
    final = "".join(nuevas_lineas[:len(lineas[:corte]) + 1 + len(bloques)])
    resto = "".join(l for n, l in enumerate(lineas[corte:], start=corte)
                    if n not in saltar)
    texto_nuevo = final + resto

    yaml.safe_load(texto_nuevo)          # VALIDAR antes de escribir
    d = yaml.safe_load(texto_nuevo)
    assert not [e for e in d["descartes"]
                if str(e.get("veredicto", ""))[:1] in "ABC"], "quedaron A/B/C en descartes"
    io.open(DICTADO, "w", encoding="utf-8", newline="\n").write(texto_nuevo)
    print(f"  escrito: 6-fusion/medina_colina_dictado.yaml "
          f"(entradas {len(d['entradas'])}, descartes {len(d['descartes'])})")


# ── 2 y 3. el lexicón ───────────────────────────────────────────────────
def _entrada_py(clave, e):
    campos = ", ".join(f'"{k}": "{str(v).replace(chr(92), chr(92)*2).replace(chr(34), chr(92) + chr(34))}"'
                       for k, v in e.items())
    return f'    "{clave}": {{{campos}}},\n'


def aplicar_lexicon(seco):
    sys.path.insert(0, AQUI)
    from curiana_lexicon import VOCABULARIO_BASE as V

    texto = io.open(LEXICON, encoding="utf-8").read()
    por_fonema = {}
    for k in V:
        por_fonema.setdefault(fonemizar(k), k)

    # — 2. las nuevas —
    nuevas = {k: e for k, e in NUEVAS.items() if k not in V}
    ya = [k for k in NUEVAS if k in V]
    if ya:
        print(f"  nuevas: {', '.join(ya)} ya estaban (idempotente)")
    if nuevas:
        print(f"  nuevas: {len(nuevas)} entradas -> {', '.join(nuevas)}")
        bloque = "".join(_entrada_py(k, e) for k, e in nuevas.items())
        cabecera = ("\n    # ── Dictado de Medina Colina (Miguel, 2026-09) — nivel A ──\n"
                    "    # Las únicas dos voces del dictado que NO estaban ya en el\n"
                    "    # lexicón por su lema fonémico. Ver 6-fusion/medina_colina_dictado.yaml\n")
        if not seco:
            texto = texto.replace(MARCA, cabecera + bloque + "\n" + MARCA, 1)

    if seco:
        print("  --dry-run: el lexicón no se toca")
    else:
        compile(texto, LEXICON, "exec")   # VALIDAR antes de escribir
        io.open(LEXICON, "w", encoding="utf-8", newline="\n").write(texto)
        print("  escrito: curiana_sim/curiana_lexicon.py")

    return por_fonema


# ── 3. la tabla de corroboración, a la bitácora de la fuente ────────────
BITACORA = os.path.join(RAIZ, "4-fuentes", "medina-colina-sxx.md")
ANCLA = "<!-- CORROBORACIONES-MEDINA -->"


def escribir_corroboraciones(por_fonema, seco):
    sys.path.insert(0, AQUI)
    from curiana_lexicon import VOCABULARIO_BASE as V

    d = cargar_dictado()
    todas = list(d["entradas"]) + list(d.get("descartes") or [])
    filas = []
    for e in sorted(todas, key=lambda x: str(x.get("voz", ""))):
        if str(e.get("veredicto", ""))[:1] != "A":
            continue
        voz = e["voz"]
        clave = voz if voz in V else por_fonema.get(fonemizar(voz))
        if not clave or clave in NUEVAS:
            continue
        glosa = " ".join(str(e.get("glosa_libro", "")).split())[:150]
        filas.append((voz, clave, V[clave].get("sig") or V[clave].get("es") or "",
                      e.get("pagina") or "—", glosa))

    print(f"  bitácora: {len(filas)} corroboraciones de nivel A")
    if seco:
        print("  --dry-run: la bitácora no se toca")
        return

    lineas = [ANCLA, "",
              "### Lo que el dictado corroboró (nivel A, 2026-09)", "",
              "Estas voces **ya estaban en el canon**: lo que el dictado añade es una",
              "atestación viva del siglo XX y, en varias, el uso. Es el rendimiento real",
              "de la sesión — no vocabulario nuevo, sino entradas que pasan de una fuente",
              "a dos o tres independientes. Las notas del lexicón NO se tocan: catorce de",
              "estas entradas viven en `lexicon_zavala.py`, que es generado.", "",
              "| Voz dictada | Lema en el canon | Glosa del canon | p. Medina | Lo que dice Medina |",
              "|---|---|---|---|---|"]
    for voz, clave, sig, pag, glosa in filas:
        lineas.append(f"| {voz} | `{clave}` | {sig[:60]} | {pag} | {glosa} |")
    lineas.append("")

    texto = io.open(BITACORA, encoding="utf-8").read()
    bloque = "\n".join(lineas)
    if ANCLA in texto:
        ini = texto.index(ANCLA)
        fin = texto.find("\n## ", ini)
        fin = fin if fin > 0 else len(texto)
        texto = texto[:ini] + bloque + texto[fin:]
    else:
        texto = texto.rstrip() + "\n\n" + bloque + "\n"
    io.open(BITACORA, "w", encoding="utf-8", newline="\n").write(texto)
    print("  escrito: 4-fuentes/medina-colina-sxx.md")


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    print("── aplicar el dictado de Medina Colina ──")
    sanear_estructura(args.dry_run)
    por_fonema = aplicar_lexicon(args.dry_run)
    escribir_corroboraciones(por_fonema, args.dry_run)
    print("\nNiveles B (11) y C (33) NO se tocan: el protocolo §5 los manda al "
          "corpus cultural, no al lexicón activo.")


if __name__ == "__main__":
    main()
