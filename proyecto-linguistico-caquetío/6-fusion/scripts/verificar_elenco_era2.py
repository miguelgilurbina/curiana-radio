#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verifica la propuesta de casting 6-fusion/elenco_era2.yaml.

Regla 1: ninguna cifra a mano. Lo que el bloque `medido` del YAML dice, lo
imprime este script; si no coinciden, es un bug del YAML.

No llama a ninguna API, no lee curiana_sim/.env y no toca Supabase. Importa
curiana_agents (los 60 nombres), curiana_lexicon (VOCABULARIO_BASE) y
curiana_fonotactica (fonemizar) sólo para leer datos.

    python 6-fusion/scripts/verificar_elenco_era2.py
    python 6-fusion/scripts/verificar_elenco_era2.py --conteos   # sólo CONTEOS
"""

import argparse
import collections
import io
import os
import re
import sys

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIM = os.path.join(RAIZ, "curiana_sim")
sys.path.insert(0, SIM)

ELENCO = os.path.join(RAIZ, "6-fusion", "elenco_era2.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")
TOPONIMOS = os.path.join(RAIZ, "2-lengua", "toponimos.yaml")
CORPUS = os.path.join(RAIZ, "3-mundo", "corpus")
GENEALOGIA = os.path.join(CORPUS, "genealogia.yaml")

CASAS_ESPERADAS = {
    "los Tacuatos": 12,
    "los Cayudes": 12,
    "casa del Manaure": 13,
    "los Guasicures de Caseto": 12,
    "los Corubos": 12,
}
UBICACIONES = {"Moruy", "Tacuato", "El Cayude", "Caseto", "Carirubana", "Capubana"}
ZONAS = {"ZG2", "ZA1", None}
ETIQUETAS = ("atestiguado", "reconstruido", "canon-simulacion", "hipotetico",
             "retro-abstraido")
FUENTES_DE_RAIZ = {"caquetío-atestiguado", "caquetío-reconstruido"}

fallos = []
avisos = []


def falla(msg):
    fallos.append(msg)


def avisa(msg):
    avisos.append(msg)


def _forzar_utf8():
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace",
                line_buffering=True))


def cargar(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def ids_del_corpus():
    """Todos los ids de hecho de 3-mundo/corpus/*.yaml."""
    ids = set()
    for nombre in sorted(os.listdir(CORPUS)):
        if not nombre.endswith(".yaml"):
            continue
        datos = cargar(os.path.join(CORPUS, nombre))
        entradas = None
        if isinstance(datos, list):
            entradas = datos
        elif isinstance(datos, dict) and isinstance(datos.get("entradas"), list):
            entradas = datos["entradas"]
        if not entradas:
            continue
        for h in entradas:
            if isinstance(h, dict) and h.get("id"):
                ids.add(h["id"])
    return ids


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--conteos", action="store_true", help="sólo la sección CONTEOS")
    args = ap.parse_args(argv)

    from curiana_agents import ALL_AGENTS
    from curiana_lexicon import VOCABULARIO_BASE
    from curiana_fonotactica import fonemizar

    elenco = cargar(ELENCO)
    agentes = elenco["agentes"]
    casas = elenco["casas"]
    fuera = elenco["fuera_del_elenco"]

    biblio = cargar(BIBLIO)["obras"]
    if isinstance(biblio, dict):
        obras_validas = set(biblio)
    else:
        obras_validas = {o["id"] for o in biblio if isinstance(o, dict) and o.get("id")}
    hechos_validos = ids_del_corpus()
    toponimos = {fonemizar(t["forma"]) for t in cargar(TOPONIMOS)["toponimos"]}
    fondo_genealogia = set(cargar(GENEALOGIA).get("personas_de_fondo") or {})

    nombres = [a["nombre"] for a in agentes]

    # ── NOMBRES ──────────────────────────────────────────────────────────
    dup = [n for n, c in collections.Counter(nombres).items() if c > 1]
    if dup:
        falla(f"nombres repetidos en el elenco: {dup}")

    nuevos = [a for a in agentes if a.get("origen") == "nuevo"]
    for a in nuevos:
        n = a["nombre"]
        fon = fonemizar(n)
        raiz = n.split("-")[0]
        fraiz = fonemizar(raiz)
        if n in ALL_AGENTS:
            falla(f"{n}: choca con un agente de la era 1")
        if n in fondo_genealogia:
            falla(f"{n}: choca con una persona de fondo de genealogia.yaml")
        if fon in toponimos:
            falla(f"{n}: el nombre coincide con un topónimo del canon")
        if fraiz in toponimos:
            falla(f"{n}: la raíz «{raiz}» coincide con un topónimo del canon")
        meta = a.get("nombre_nuevo") or {}
        declarada = meta.get("raiz")
        if declarada != raiz.lower():
            falla(f"{n}: nombre_nuevo.raiz dice «{declarada}» y la raíz del nombre es «{raiz.lower()}»")
        entrada = VOCABULARIO_BASE.get(declarada)
        if entrada is None:
            falla(f"{n}: la raíz «{declarada}» no está en VOCABULARIO_BASE")
        elif entrada.get("fuente") not in FUENTES_DE_RAIZ:
            falla(f"{n}: la raíz «{declarada}» es {entrada.get('fuente')}, no caquetío atestiguado ni reconstruido")
        elif entrada.get("fuente") != meta.get("fuente"):
            falla(f"{n}: nombre_nuevo.fuente dice «{meta.get('fuente')}» y el lexicón dice «{entrada.get('fuente')}»")

    reutilizados = [a for a in agentes if str(a.get("origen", "")).startswith("era1:")]
    for a in reutilizados:
        citado = str(a["origen"]).split(":", 1)[1].split(" ")[0]
        if citado != a["nombre"]:
            falla(f"{a['nombre']}: origen cita «{citado}»")
        if a["nombre"] not in ALL_AGENTS:
            falla(f"{a['nombre']}: dice ser de la era 1 y no está en curiana_agents.ALL_AGENTS")

    de_fondo = [a for a in agentes if str(a.get("origen", "")).startswith("fondo:")]
    for a in de_fondo:
        citado = str(a["origen"]).split(":", 1)[1].split(" ")[0]
        if citado not in fondo_genealogia:
            falla(f"{a['nombre']}: no es persona de fondo de genealogia.yaml")

    # ── FICHAS ───────────────────────────────────────────────────────────
    for a in agentes:
        n = a["nombre"]
        for campo in ("nodo", "casa", "tier", "genero", "edad", "rol_en_la_casa",
                      "oficio", "en_roster", "ubicacion_default", "parentesco",
                      "origen", "etiqueta", "descripcion", "dossier"):
            if campo not in a:
                falla(f"{n}: falta el campo `{campo}`")
        if a.get("ubicacion_default") not in UBICACIONES:
            falla(f"{n}: ubicacion_default «{a.get('ubicacion_default')}» fuera de la lista")
        if a.get("zona_de_pesca") not in ZONAS:
            falla(f"{n}: zona_de_pesca «{a.get('zona_de_pesca')}» fuera de la lista")
        if a.get("tier") not in (1, 2, 3):
            falla(f"{n}: tier inválido")
        if not str(a.get("etiqueta", "")).startswith(ETIQUETAS):
            falla(f"{n}: etiqueta «{a.get('etiqueta')}» no empieza por una del vocabulario")
        papel = a.get("papel_kapubana")
        if papel is not None and not re.fullmatch(r"of-\d{2}", str(papel)):
            falla(f"{n}: papel_kapubana «{papel}» no tiene la forma of-XX")

        sp = a.get("system_prompt")
        if a["tier"] == 3:
            if sp:
                falla(f"{n}: tier 3 no lleva system_prompt (sólo descripción)")
        else:
            if not sp:
                falla(f"{n}: tier {a['tier']} sin system_prompt")
            else:
                if "Español" in sp or "español" in sp:
                    falla(f"{n}: el system_prompt nombra el español")
                if "Curiana" in sp or "curiana" in sp:
                    falla(f"{n}: el system_prompt dice «Curiana»")
                if a["casa"] not in sp and a["nodo"] not in sp:
                    falla(f"{n}: el system_prompt no nombra ni su casa ni su nodo")
                if a["nodo"] not in sp:
                    falla(f"{n}: el system_prompt no nombra su nodo")
                sitio = a.get("ubicacion_default")
                if sitio not in sp:
                    falla(f"{n}: el system_prompt no nombra su sitio ({sitio})")

        d = a.get("dossier") or {}
        for clave in ("hechos", "obras", "decisiones"):
            if not d.get(clave):
                falla(f"{n}: dossier.{clave} vacío")
        for h in d.get("hechos") or []:
            if h not in hechos_validos:
                falla(f"{n}: hecho «{h}» no existe en 3-mundo/corpus/")
        for o in d.get("obras") or []:
            if o not in obras_validas:
                falla(f"{n}: obra «{o}» no existe en 4-fuentes/bibliografia.yaml")

    # ── CASAS ────────────────────────────────────────────────────────────
    por_casa = collections.Counter(a["casa"] for a in agentes)
    for casa, esperado in CASAS_ESPERADAS.items():
        if por_casa.get(casa, 0) != esperado:
            falla(f"casa «{casa}»: {por_casa.get(casa, 0)} agentes, se esperaban {esperado}")
    for casa in por_casa:
        if casa not in CASAS_ESPERADAS:
            falla(f"casa «{casa}» no está en las cinco decididas")
    for c in casas:
        ap_ = c.get("apopo")
        if ap_ and not str(ap_).startswith("no aplica") and ap_ not in nombres:
            falla(f"casa «{c['casa']}»: el apopo «{ap_}» no está en el elenco")
        if c.get("agentes") != por_casa.get(c["casa"]):
            falla(f"casa «{c['casa']}»: declara {c.get('agentes')} agentes y tiene {por_casa.get(c['casa'])}")

    # ── FUERA DEL ELENCO ─────────────────────────────────────────────────
    fuera_nombres = []
    for bloque in fuera.values():
        if isinstance(bloque, dict) and isinstance(bloque.get("agentes"), list):
            for x in bloque["agentes"]:
                fuera_nombres.append(x["nombre"])
    for n in fuera_nombres:
        if n not in ALL_AGENTS:
            falla(f"fuera_del_elenco: «{n}» no es un agente de la era 1")
        if n in nombres:
            falla(f"«{n}» está a la vez dentro y fuera del elenco")
    cubiertos = {a["nombre"] for a in reutilizados} | set(fuera_nombres)
    sin_destino = sorted(set(ALL_AGENTS) - cubiertos)
    if sin_destino:
        falla(f"agentes de la era 1 sin destino declarado: {sin_destino}")

    # ── CONTEOS ──────────────────────────────────────────────────────────
    def origen_clase(a):
        o = str(a.get("origen", ""))
        if o.startswith("era1:"):
            return "era1 (reutilizado)"
        if o.startswith("fondo:"):
            return "fondo (promovido de genealogia.yaml)"
        return "nuevo"

    def linaje_clase(a):
        l = a.get("linaje")
        if not l:
            return "sin linaje de D1"
        for d1 in ("Buio", "Chiriware", "Corie", "Paugis", "Kaira", "Warana"):
            if str(l).startswith(d1):
                return d1
        return "sin linaje de D1"

    roster = [a for a in agentes if a.get("en_roster")]
    conteos = {
        "total_agentes": len(agentes),
        "por_nodo": dict(collections.Counter(a["nodo"] for a in agentes)),
        "por_casa": dict(por_casa),
        "por_tier": dict(collections.Counter(str(a["tier"]) for a in agentes)),
        "por_linaje": dict(collections.Counter(linaje_clase(a) for a in agentes)),
        "por_origen": dict(collections.Counter(origen_clase(a) for a in agentes)),
        "en_roster": len(roster),
        "roster_por_nodo": dict(collections.Counter(a["nodo"] for a in roster)),
        "portadores_entre_nodos_en_el_roster": sum(
            1 for a in roster if "entrante del otro nodo" in a["rol_en_la_casa"]
            or "del otro nodo" in a["rol_en_la_casa"]
            or a["nombre"] == "Nubiri-sha"),
        "era1_fuera_del_elenco": len(fuera_nombres),
        "nombres_nuevos_acunados": len(nuevos),
    }
    for a in roster:
        if not a.get("razon_roster"):
            falla(f"{a['nombre']}: en_roster sin razon_roster")

    print("── CONTEOS ──")
    for k, v in conteos.items():
        print(f"  {k}: {v}")

    declarado = elenco["meta"]["medido"]
    for k, v in conteos.items():
        if k in declarado and declarado[k] != v:
            falla(f"meta.medido.{k} dice {declarado[k]} y se mide {v}")
    if fuera.get("medido", {}).get("total") != len(fuera_nombres):
        falla(f"fuera_del_elenco.medido.total dice {fuera.get('medido', {}).get('total')} y se mide {len(fuera_nombres)}")

    if args.conteos:
        return 0 if not fallos else 1

    print("\n── NOMBRES NUEVOS ──")
    for a in nuevos:
        m = a["nombre_nuevo"]
        print(f"  {a['nombre']:14} < {m['raiz']} «{m['glosa']}» [{m['fuente']}]")

    print("\n── ROSTER ──")
    for a in sorted(roster, key=lambda x: (x["nodo"], x["casa"], x["nombre"])):
        print(f"  {a['nodo']:8} {a['casa']:26} {a['nombre']:14} T{a['tier']}  {a['rol_en_la_casa']}")

    print("\n── FUERA ──")
    print(f"  {len(fuera_nombres)} agentes de la era 1: {', '.join(sorted(fuera_nombres))}")

    print("\n── RESULTADO ──")
    for m in avisos:
        print(f"  aviso: {m}")
    if fallos:
        for m in fallos:
            print(f"  FALLO: {m}")
        print(f"\n  {len(fallos)} fallo(s).")
        return 1
    print("  todo en verde.")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
