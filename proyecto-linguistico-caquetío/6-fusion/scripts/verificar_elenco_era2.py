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
import itertools
import os
import re
import sys

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIM = os.path.join(RAIZ, "curiana_sim")
sys.path.insert(0, SIM)

ELENCO = os.path.join(RAIZ, "6-fusion", "elenco_era2.yaml")
SISTEMA = os.path.join(RAIZ, "6-fusion", "sistema_de_nombres_era2.yaml")
MAPA = os.path.join(RAIZ, "6-fusion", "mapa_nombres_era2.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")
TOPONIMOS = os.path.join(RAIZ, "2-lengua", "toponimos.yaml")
CORPUS = os.path.join(RAIZ, "3-mundo", "corpus")
GENEALOGIA = os.path.join(CORPUS, "genealogia.yaml")

CASAS_ESPERADAS = {
    "los Tacuatos": 13,       # 12 + Korie-ko reanclado (Miguel, 2026-09-14, P2)
    "los Cayudes": 12,
    "casa del Manaure": 14,   # 13 + la cuarta esposa (Miguel, 2026-09-14, P6)
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


def levenshtein(a, b):
    """Distancia de edición. La regla f pide ≥ 2 entre dos nombres del elenco."""
    previa = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        actual = [i]
        for j, cb in enumerate(b, 1):
            actual.append(min(previa[j] + 1, actual[j - 1] + 1,
                              previa[j - 1] + (ca != cb)))
        previa = actual
    return previa[-1]


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
    from curiana_fonotactica import fonemizar, Fonotactica

    elenco = cargar(ELENCO)
    agentes = elenco["agentes"]
    casas = elenco["casas"]
    fuera = elenco["fuera_del_elenco"]

    sistema = cargar(SISTEMA)
    reglas = {r["id"]: r for r in sistema["reglas"]}
    formantes_productivos = {f["formante"] for f in reglas["b"]["formantes_productivos"]}
    conservados = {c["nombre"]: c for c in reglas["g"]["conservados"]}

    biblio = cargar(BIBLIO)["obras"]
    if isinstance(biblio, dict):
        obras_validas = set(biblio)
    else:
        obras_validas = {o["id"] for o in biblio if isinstance(o, dict) and o.get("id")}
    hechos_validos = ids_del_corpus()
    toponimos = {fonemizar(t["forma"]) for t in cargar(TOPONIMOS)["toponimos"]}
    fondo_genealogia = set(cargar(GENEALOGIA).get("personas_de_fondo") or {})

    nombres = [a["nombre"] for a in agentes]
    alias = {a["nombre"]: a.get("alias_era1") for a in agentes}

    # ── NOMBRES ──────────────────────────────────────────────────────────
    # Campaña de antropónimos del 2026-09-14 (Miguel: «Sí a los dos puntos» y
    # «Sí o sí hay que sacar eso de -ko y -sha»). Las reglas están declaradas
    # en 6-fusion/sistema_de_nombres_era2.yaml y se comprueban TODAS aquí,
    # sobre los 63, no sólo sobre los nombres que el casting acuñó.
    dup = [n for n, c in collections.Counter(nombres).items() if c > 1]
    if dup:
        falla(f"nombres repetidos en el elenco: {dup}")

    atestiguado = [k for k, e in VOCABULARIO_BASE.items()
                   if e.get("fuente") == "caquetío-atestiguado"]
    fonotactica = Fonotactica(atestiguado)

    for a in agentes:
        n = a["nombre"]
        meta = a.get("nombre_nuevo") or {}
        raiz = meta.get("raiz")
        formante = meta.get("formante")

        # (e) sin -ko ni -sha
        if n.endswith("-ko") or n.endswith("-sha"):
            falla(f"{n}: lleva -ko o -sha, retirados por decisión del 2026-09-14")

        # (a) la raíz es una voz del lexicón, atestiguada o reconstruida
        entrada = VOCABULARIO_BASE.get(raiz)
        if not raiz:
            falla(f"{n}: sin nombre_nuevo.raiz")
        elif entrada is None:
            falla(f"{n}: la raíz «{raiz}» no está en VOCABULARIO_BASE")
        elif entrada.get("fuente") not in FUENTES_DE_RAIZ:
            falla(f"{n}: la raíz «{raiz}» es {entrada.get('fuente')}, "
                  f"no caquetío atestiguado ni reconstruido")
        elif entrada.get("fuente") != meta.get("fuente"):
            falla(f"{n}: nombre_nuevo.fuente dice «{meta.get('fuente')}» "
                  f"y el lexicón dice «{entrada.get('fuente')}»")

        # el nombre ES la raíz más el formante, comparados fonemizados.
        # En la juntura, vocal + la misma vocal se funde en una (rua + -ata →
        # Ruata): el caquetío atestiguado no tiene vocal doble. Regla b del
        # sistema de nombres, §elision_en_la_juntura.
        if raiz:
            fr, ff = fonemizar(raiz), fonemizar((formante or "").lstrip("-"))
            posibles = {fr + ff}
            if fr and ff and fr[-1] == ff[0]:
                posibles.add(fr + ff[1:])
            if fonemizar(n) not in posibles:
                falla(f"{n}: no es raíz + formante ({raiz} + {formante or 'ø'} "
                      f"daría {sorted(posibles)} y se fonemiza «{fonemizar(n)}»)")

        # (b) el formante está declarado en el sistema de nombres
        if formante and formante not in formantes_productivos and n not in conservados:
            falla(f"{n}: el formante «{formante}» no es productivo en "
                  f"sistema_de_nombres_era2.yaml y el nombre no está entre los conservados")
        if formante and n in conservados and formante != conservados[n].get("formante", formante):
            avisa(f"{n}: conservado con formante «{formante}»")

        # (b) fonotáctica del caquetío atestiguado
        ok, motivos = fonotactica.valida(n)
        if not ok:
            falla(f"{n}: fonotáctica — {'; '.join(motivos)}")

        # (f) unicidad ampliada
        if fonemizar(n) in toponimos:
            falla(f"{n}: el nombre coincide con un topónimo del canon")
        if raiz and fonemizar(raiz) in toponimos:
            falla(f"{n}: la raíz «{raiz}» coincide con un topónimo del canon")
        if n in ALL_AGENTS and alias[n] != n:
            falla(f"{n}: choca con un agente de la era 1 que no es su alias")
        if n in fondo_genealogia and alias[n] != n:
            falla(f"{n}: choca con una persona de fondo de genealogia.yaml")

        if not a.get("razon_del_nombre"):
            falla(f"{n}: sin razon_del_nombre")

    # (f) dos nombres no se distinguen por una sola letra
    for x, y in itertools.combinations(sorted(set(nombres)), 2):
        if levenshtein(fonemizar(x), fonemizar(y)) < 2:
            falla(f"«{x}» y «{y}» se distinguen por una sola letra")

    # (g) los conservados declarados están y no cambiaron
    for n in conservados:
        if n not in nombres:
            falla(f"sistema_de_nombres_era2.yaml declara «{n}» conservado y no está en el elenco")
        elif alias[n] != n:
            falla(f"{n}: declarado conservado y su alias_era1 dice «{alias[n]}»")

    # ── ALIAS ────────────────────────────────────────────────────────────
    acunados_por_el_casting = {
        a.get("alias_era1") for a in agentes if a.get("origen") == "nuevo"}
    for a in agentes:
        n, al = a["nombre"], a.get("alias_era1")
        if not al:
            falla(f"{n}: sin alias_era1")
            continue
        if al not in ALL_AGENTS and al not in fondo_genealogia and al not in acunados_por_el_casting:
            falla(f"{n}: alias_era1 «{al}» no es agente de la era 1, ni persona "
                  f"de fondo, ni nombre acuñado por el casting")
    dup_alias = [x for x, c in collections.Counter(
        a.get("alias_era1") for a in agentes).items() if c > 1]
    if dup_alias:
        falla(f"alias_era1 repetidos: {dup_alias}")

    nuevos = [a for a in agentes if a.get("origen") == "nuevo"]

    reutilizados = [a for a in agentes if str(a.get("origen", "")).startswith("era1:")]
    for a in reutilizados:
        citado = str(a["origen"]).split(":", 1)[1].split(" ")[0]
        if citado != a.get("alias_era1"):
            falla(f"{a['nombre']}: origen cita «{citado}» y alias_era1 dice «{a.get('alias_era1')}»")
        if citado not in ALL_AGENTS:
            falla(f"{a['nombre']}: dice venir de la era 1 y «{citado}» no está en curiana_agents.ALL_AGENTS")

    de_fondo = [a for a in agentes if str(a.get("origen", "")).startswith("fondo:")]
    for a in de_fondo:
        citado = str(a["origen"]).split(":", 1)[1].split(" ")[0]
        if citado not in fondo_genealogia:
            falla(f"{a['nombre']}: no es persona de fondo de genealogia.yaml")
        if citado != a.get("alias_era1"):
            falla(f"{a['nombre']}: origen cita «{citado}» y alias_era1 dice «{a.get('alias_era1')}»")

    # ── EL MAPA ──────────────────────────────────────────────────────────
    mapa = {f["nombre_era1"]: f for f in cargar(MAPA)["nombres"]}
    if set(mapa) != {a.get("alias_era1") for a in agentes}:
        falla("mapa_nombres_era2.yaml y los alias_era1 del elenco no cubren el mismo conjunto")
    for a in agentes:
        fila = mapa.get(a.get("alias_era1"))
        if not fila:
            continue
        esperado = fila.get("nombre") if fila["nombre_nuevo"] == "se conserva" else fila["nombre_nuevo"]
        if esperado != a["nombre"]:
            falla(f"{a['nombre']}: el mapa dice «{esperado}» para el alias «{a.get('alias_era1')}»")
        if fila.get("raiz") != (a.get("nombre_nuevo") or {}).get("raiz"):
            falla(f"{a['nombre']}: el mapa declara raíz «{fila.get('raiz')}» y la ficha «{(a.get('nombre_nuevo') or {}).get('raiz')}»")

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
    # Los 60 de la era 1 tienen destino declarado: o entraron al elenco (y se
    # los reconoce por su alias_era1, no por su nombre nuevo) o están fuera.
    cubiertos = {a.get("alias_era1") for a in reutilizados} | set(fuera_nombres)
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
        "nombres_conservados": sum(1 for a in agentes if a["nombre"] == a.get("alias_era1")),
        "nombres_renombrados": sum(1 for a in agentes if a["nombre"] != a.get("alias_era1")),
        "raices_por_capa": dict(collections.Counter(
            (a.get("nombre_nuevo") or {}).get("fuente") for a in agentes)),
        "formantes_usados": dict(collections.Counter(
            (a.get("nombre_nuevo") or {}).get("formante") or "(raíz sola)"
            for a in agentes)),
        "nombres_con_ko_o_sha": sum(
            1 for a in agentes if a["nombre"].endswith(("-ko", "-sha"))),
        "nombres_homografos_del_lexicon": sum(
            1 for a in agentes if a["nombre"].lower() in VOCABULARIO_BASE),
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

    print("\n── NOMBRES (viejo → nuevo, raíz y formante) ──")
    for a in agentes:
        m = a["nombre_nuevo"]
        flecha = "=" if a["nombre"] == a.get("alias_era1") else "→"
        capa = "A" if m["fuente"] == "caquetío-atestiguado" else "R"
        print(f"  {a.get('alias_era1'):14} {flecha} {a['nombre']:14} "
              f"< {m['raiz']}{m['formante'] or ''} [{capa}] «{m['glosa']}»")

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
