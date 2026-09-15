# -*- coding: utf-8 -*-
"""
generar_agentes_era2.py — el elenco de la era 2 como módulo del motor.

Lee 6-fusion/elenco_era2.yaml (la propuesta de casting que Miguel decidió el
2026-09-14, #127) y escribe curiana_sim/curiana_agents_era2.py, un módulo
GENERADO con la misma forma que curiana_agents.py (tier, genero, edad, etnia,
ubicacion_default, actividades, system_prompt, descripcion) más lo que la era 2
añade: nodo, casa, sitio, zona_de_pesca, linaje, rol_en_la_casa, oficio,
papel_kapubana, en_roster, alias_era1 y el dossier de fuentes.

Desde la campaña de antropónimos del 2026-09-14 cada agente lleva además su
`alias_era1` —el nombre que tuvo en el casting, antes de que los nombres se
rehicieran con raíces y formantes atestiguados— y el módulo expone
ALIAS_ERA1 = {nombre_era1: nombre_nuevo} para que el corpus, la genealogía y
las bitácoras de los runs de prueba sigan resolviendo.

No se edita el módulo: se corrige el YAML y se regenera. El hook del proyecto
bloquea editarlo a mano. `test_elenco_era2.py` comprueba que el módulo del repo
sea exactamente lo que este script emite.

Uso:
    python 6-fusion/scripts/generar_agentes_era2.py            # escribe el módulo
    python 6-fusion/scripts/generar_agentes_era2.py --check    # 0 si está al día
"""
import io
import os
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
ELENCO = os.path.join(RAIZ, "6-fusion", "elenco_era2.yaml")
SALIDA = os.path.join(RAIZ, "curiana_sim", "curiana_agents_era2.py")

MUNDO = "PARAGUANÁ"


def _etnia(genero: str) -> str:
    return "caquetía" if str(genero).upper() == "F" else "caquetío"


def _prompt_tier3(a: dict) -> str:
    """Los tier 3 no traen system_prompt en el YAML: se arma desde la ficha,
    nombrando nodo, casa y sitio como los demás."""
    return (f"Eres {a['nombre']}, de la casa de {a['casa']}, en {a['ubicacion_default']}, "
            f"nodo {a['nodo']}. ~{a['edad']} años. {_etnia(a['genero']).capitalize()}. "
            f"{a['descripcion']} Responde brevemente en personaje.")


def _sitios(elenco: dict) -> dict:
    sitios = {}
    for c in elenco.get("casas") or []:
        s = c.get("sitio") or {}
        zona = c.get("zona_de_pesca")
        sitios[s.get("nombre")] = {
            "nodo": c.get("nodo"),
            "casa": c.get("casa"),
            "lat": s.get("lat"),
            "lon": s.get("lon"),
            "zona_de_pesca": (zona.split(" ")[0] if isinstance(zona, str) else None),
        }
    # Sitios que no son casa (el Capubana, donde duerme el boratio mayor):
    # entran con el nodo del agente y sin coordenadas, que aquí no se inventan.
    for a in elenco.get("agentes") or []:
        s = a.get("ubicacion_default")
        if s and s not in sitios:
            sitios[s] = {"nodo": a.get("nodo"), "casa": None, "lat": None, "lon": None,
                         "zona_de_pesca": None, "nota": "sitio fuera de las casas"}
    return sitios


def _agente(a: dict) -> dict:
    tier = int(a["tier"])
    d = {
        "tier": tier,
        "genero": a["genero"],
        "edad": int(a["edad"]),
        "etnia": _etnia(a["genero"]),
        "ubicacion_default": a["ubicacion_default"],
        "actividades": [a["oficio"]] if a.get("oficio") else [],
        "system_prompt": (a.get("system_prompt") or _prompt_tier3(a)).rstrip("\n"),
        "descripcion": a["descripcion"],
        # ── lo que la era 2 añade ──
        "nodo": a["nodo"],
        "casa": a["casa"],
        "sitio": a["ubicacion_default"],
        "zona_de_pesca": a.get("zona_de_pesca"),
        "linaje": a["linaje"],
        "rol_en_la_casa": a["rol_en_la_casa"],
        "oficio": a.get("oficio"),
        "papel_kapubana": a.get("papel_kapubana"),
        "en_roster": bool(a.get("en_roster")),
        "origen": a.get("origen"),
        "alias_era1": a.get("alias_era1"),
        "dossier": a.get("dossier") or {},
    }
    return d


def _literal(v, sangria: int) -> str:
    """Un literal Python legible y estable (repr ordenado para los dicts)."""
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
    return repr(v)


def emitir(elenco: dict) -> str:
    agentes = elenco["agentes"]
    por_tier = {1: [], 2: [], 3: []}
    for a in agentes:
        por_tier[int(a["tier"])].append(a)
    meta = elenco.get("meta", {})
    medido = meta.get("medido", {})

    out = io.StringIO()
    w = out.write
    w("# -*- coding: utf-8 -*-\n")
    w('"""\n')
    w("curiana_agents_era2.py — el elenco de la era 2 (Paraguaná).\n\n")
    w("GENERADO por 6-fusion/scripts/generar_agentes_era2.py desde\n")
    w("6-fusion/elenco_era2.yaml (#127, decidido el 2026-09-14). No se edita a mano:\n")
    w("se corrige el YAML y se regenera. test_elenco_era2.py vigila que este\n")
    w("módulo sea lo que el script emite.\n\n")
    w("Misma forma que curiana_agents.py, más nodo, casa, sitio, zona_de_pesca,\n")
    w("linaje, rol_en_la_casa, oficio, papel_kapubana, en_roster, alias_era1 y\n")
    w("dossier. Los nombres se rehicieron el 2026-09-14 con raíces y formantes\n")
    w("atestiguados (campaña de antropónimos); ALIAS_ERA1 traduce del nombre\n")
    w("viejo al nuevo.\n")
    w("Se activa con CURIANA_ELENCO=era2 (o --elenco era2 en el orquestador):\n")
    w("curiana_agents.py lo importa y expone su ALL_AGENTS.\n")
    w('"""\n\n')
    w(f"ERA = 'era2'\n")
    w(f"MUNDO = {MUNDO!r}\n")
    w(f"# Conteos del casting (los mide 6-fusion/scripts/verificar_elenco_era2.py)\n")
    w(f"MEDIDO = {_literal(medido, 0)}\n\n")

    sitios = _sitios(elenco)
    w("# Los sitios de las casas, con su nodo y su zona de pesca\n")
    w(f"SITIOS = {_literal(sitios, 0)}\n\n")

    for tier in (1, 2, 3):
        w("# " + "=" * 60 + "\n")
        w(f"# TIER {'I' * tier if tier < 3 else 'III'} — {len(por_tier[tier])} agentes\n")
        w("# " + "=" * 60 + "\n\n")
        w(f"AGENTS_T{tier} = {{\n\n")
        for a in por_tier[tier]:
            w(f"    {a['nombre']!r}: {_literal(_agente(a), 4)},\n\n")
        w("}\n\n")

    w("ALL_AGENTS = {}\n")
    w("ALL_AGENTS.update(AGENTS_T1)\n")
    w("ALL_AGENTS.update(AGENTS_T2)\n")
    w("ALL_AGENTS.update(AGENTS_T3)\n\n")
    roster = [a["nombre"] for a in agentes if a.get("en_roster")]
    w("# El roster que rota de continuo según el casting (P10: proporcional, 14 y 10);\n")
    w("# el motor con --roster todos hace rotar a todo el elenco.\n")
    w(f"ROSTER_NUCLEO = {_literal(roster, 0)}\n\n")
    alias = {a["alias_era1"]: a["nombre"] for a in agentes if a.get("alias_era1")}
    w("# Del nombre de la era 1 (o del que acuñó el casting) al nombre de la era 2.\n")
    w("# Los tres conservados —Manaure, Kunaro-bana y Dara-bana— se apuntan a sí\n")
    w("# mismos, así que el diccionario cubre a los 63 y resolver es incondicional.\n")
    w(f"ALIAS_ERA1 = {_literal(alias, 0)}\n\n")
    w("\ndef get_agent(nombre):\n")
    w("    return ALL_AGENTS.get(nombre)\n\n")
    w("\ndef resolver_alias(nombre):\n")
    w('    """El nombre de la era 2 de un agente nombrado como en la era 1."""\n')
    w("    return ALIAS_ERA1.get(nombre, nombre)\n")
    return out.getvalue()


def main() -> int:
    elenco = yaml.safe_load(io.open(ELENCO, encoding="utf-8"))
    texto = emitir(elenco)
    if "--check" in sys.argv:
        actual = io.open(SALIDA, encoding="utf-8").read() if os.path.exists(SALIDA) else ""
        if actual == texto:
            print("curiana_agents_era2.py al día")
            return 0
        print("curiana_agents_era2.py NO está al día: regenerar")
        return 1
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    n = len(elenco["agentes"])
    print(f"escrito {os.path.relpath(SALIDA, RAIZ)}: {n} agentes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
