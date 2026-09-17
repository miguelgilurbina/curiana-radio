# -*- coding: utf-8 -*-
"""
generar_escena_era2.py — la escena de la era 2 como módulo del motor.

Lee 6-fusion/escena_era2.yaml (la tabla que Miguel decidió el 2026-09-17, sobre
las diez preguntas de §7 del diseño) y escribe
curiana_sim/curiana_escena_era2.py, un módulo GENERADO con la misma forma que
curiana_agents_era2.py: datos literales y dos funciones de lectura.

Lo que el módulo lleva:

    ESCENA      {agente: {periodo: (lugar × 6 momentos)}}  — los 63 × 3 × 6
    LUGARES     {lugar: {tipo, sitio, nodo, lat, lon, glosa, locacion,…}}
    CLASE_DE    {agente: clase de oficio}
    ETIQUETAS   {clase: {etiqueta, fuente}}  — canon con fuente / canon-simulación
    COMPARTIDOS {lugar: por qué está declarado compartido}
    TRAVESIA    la travesía de la alianza (quién cruza el camino y cuándo)
    CAPUBANA    el cerro y qué pasa el día de la convergencia

No se edita el módulo: se corrige la tabla en
6-fusion/scripts/derivar_escena_por_lugar.py, se regenera el YAML con --canon y
se regenera el módulo con este script. `test_escena_era2.py` comprueba que el
módulo del repo sea exactamente lo que este script emite.

Uso:
    python 6-fusion/scripts/generar_escena_era2.py            # escribe el módulo
    python 6-fusion/scripts/generar_escena_era2.py --check    # 0 si está al día
"""
import io
import os
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
TABLA = os.path.join(RAIZ, "6-fusion", "escena_era2.yaml")
SALIDA = os.path.join(RAIZ, "curiana_sim", "curiana_escena_era2.py")

MUNDO = "PARAGUANÁ"


def _literal(v, sangria: int) -> str:
    """Un literal Python legible y estable (el mismo de generar_agentes_era2)."""
    pad = " " * sangria
    if isinstance(v, str) and "\n" in v:
        cuerpo = v.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        return f'"""{cuerpo}"""'
    if isinstance(v, dict):
        if not v:
            return "{}"
        items = [f'{pad}    {k!r}: {_literal(x, sangria + 4)},' for k, x in v.items()]
        return "{\n" + "\n".join(items) + f"\n{pad}}}"
    if isinstance(v, list):
        return "[" + ", ".join(_literal(x, sangria) for x in v) + "]"
    if isinstance(v, tuple):
        cuerpo = ", ".join(_literal(x, sangria) for x in v)
        return f"({cuerpo},)" if len(v) == 1 else f"({cuerpo})"
    return repr(v)


def emitir(tabla: dict) -> str:
    momentos = list(tabla["momentos"])
    periodos = list(tabla["periodos"])
    escena_por_agente = tabla["escena_por_agente"]

    # {agente: {periodo: (lugar × 6)}} — la escena resuelta, sin plantillas:
    # toda plantilla se resolvió al derivar la tabla.
    escena = {
        nombre: {p: tuple(ficha[p]) for p in periodos}
        for nombre, ficha in escena_por_agente.items()
    }
    lugares = tabla["lugares"]
    clase_de = tabla["clase_por_agente"]
    etiquetas = {clase: {"etiqueta": fila["etiqueta"], "fuente": fila["fuente"]}
                 for clase, fila in tabla["tabla"].items()}
    nodo_de_agente = {n: f.get("nodo") for n, f in escena_por_agente.items()}
    sitio_de_agente = {n: f.get("sitio") for n, f in escena_por_agente.items()}

    out = io.StringIO()
    w = out.write
    w("# -*- coding: utf-8 -*-\n")
    w('"""\n')
    w("curiana_escena_era2.py — la escena de la era 2: dónde está cada uno.\n\n")
    w("GENERADO por 6-fusion/scripts/generar_escena_era2.py desde\n")
    w("6-fusion/escena_era2.yaml, que a su vez deriva del elenco con\n")
    w("6-fusion/scripts/derivar_escena_por_lugar.py --canon. No se edita a mano:\n")
    w("se corrige la tabla del derivador, se regenera el YAML y se regenera este\n")
    w("módulo. test_escena_era2.py vigila que sea lo que el script emite.\n\n")
    w("Ninguna fila se escribió agente a agente: la clase de oficio sale de la\n")
    w("ficha por palabras clave declaradas y el lugar sale de una plantilla\n")
    w("resuelta con la ficha. Cambiar el elenco cambia esta tabla sin tocarla.\n\n")
    w("La puerta del motor NO es este módulo sino curiana_escena.py, que lo lee.\n")
    w('"""\n\n')
    w("ERA = 'era2'\n")
    w(f"MUNDO = {MUNDO!r}\n\n")
    w(f"MOMENTOS = {_literal(tuple(momentos), 0)}\n")
    w(f"PERIODOS = {_literal(tuple(periodos), 0)}\n\n")

    w("# Las decisiones de Miguel del 2026-09-17 que esta tabla aplica.\n")
    w(f"DECISIONES = {_literal({str(k): v for k, v in tabla['decisiones_de_miguel'].items()}, 0)}\n\n")

    w("# " + "=" * 60 + "\n")
    w(f"# LOS LUGARES — {len(lugares)}, ninguno sin sitio ni coordenada\n")
    w("# " + "=" * 60 + "\n\n")
    w(f"LUGARES = {_literal(lugares, 0)}\n\n")

    w("# " + "=" * 60 + "\n")
    w(f"# LA ESCENA — {len(escena)} agentes × {len(periodos)} períodos × "
      f"{len(momentos)} momentos\n")
    w("# " + "=" * 60 + "\n\n")
    w(f"ESCENA = {_literal(escena, 0)}\n\n")

    w("# La clase de oficio de cada agente, y con qué se sostiene el día de\n")
    w("# esa clase (canon con fuente / canon-simulación).\n")
    w(f"CLASE_DE = {_literal(clase_de, 0)}\n\n")
    w(f"ETIQUETAS = {_literal(etiquetas, 0)}\n\n")
    w(f"NODO_DE = {_literal(nodo_de_agente, 0)}\n\n")
    w(f"SITIO_DE = {_literal(sitio_de_agente, 0)}\n\n")

    w("# Los lugares que la decisión 2 → B declara compartidos entre los nodos.\n")
    w(f"COMPARTIDOS = {_literal(tabla['compartidos_declarados'], 0)}\n\n")
    w("# El camino de la alianza: quién lo cruza y cuándo (derivado, no escrito).\n")
    w(f"TRAVESIA = {_literal(tabla['travesia_de_la_alianza'], 0)}\n\n")
    w("# El cerro y el día de la convergencia (cadencia: --capubana-cada N).\n")
    w(f"CAPUBANA = {_literal(tabla['capubana'], 0)}\n\n")

    w("\nAGENTES = tuple(sorted(ESCENA))\n\n")
    w("\ndef lugar_de(agente, periodo, momento):\n")
    w('    """El lugar de un agente en un momento de un período, o None."""\n')
    w("    fila = ESCENA.get(agente)\n")
    w("    if not fila or periodo not in fila or momento not in MOMENTOS:\n")
    w("        return None\n")
    w("    return fila[periodo][MOMENTOS.index(momento)]\n\n")
    w("\ndef glosa_de(lugar):\n")
    w('    """Cómo se dice ese lugar en prosa: «la orilla de Tacuato»."""\n')
    w("    return (LUGARES.get(lugar) or {}).get('glosa') or lugar\n")
    return out.getvalue()


def main() -> int:
    tabla = yaml.safe_load(io.open(TABLA, encoding="utf-8"))
    texto = emitir(tabla)
    if "--check" in sys.argv:
        actual = io.open(SALIDA, encoding="utf-8").read() if os.path.exists(SALIDA) else ""
        if actual == texto:
            print("curiana_escena_era2.py al día")
            return 0
        print("curiana_escena_era2.py NO está al día: regenerar")
        return 1
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    n = len(tabla["escena_por_agente"])
    print(f"escrito {os.path.relpath(SALIDA, RAIZ)}: {n} agentes × "
          f"{len(tabla['periodos'])} períodos × {len(tabla['momentos'])} momentos, "
          f"{len(tabla['lugares'])} lugares")
    return 0


if __name__ == "__main__":
    sys.exit(main())
