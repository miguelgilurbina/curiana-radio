#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verifica la campaña de SITIOS Y CLIMA de la era 2:

    6-fusion/sitios_era2.yaml
    6-fusion/clima_era2.yaml

Regla 1: ninguna cifra a mano. Los conteos que el `meta.medido` de cada YAML
declara los imprime este script; si no coinciden, es un bug del YAML.
Regla 8: `procedencia.obra` es clave foránea a 4-fuentes/bibliografia.yaml.

Comprueba:
  1. toda `procedencia.obra` existe en 4-fuentes/bibliografia.yaml
  2. todo id de hecho citado (ecologia-0NN, creencia-0NN, hueco-lex-00N…)
     existe en 3-mundo/corpus/*.yaml
  3. toda `voz_caquetia` existe en VOCABULARIO_BASE con la capa declarada
     (curiana_lexicon.capa_epistemica)
  4. cada sitio de sitios_era2.yaml está en curiana_agents_era2.SITIOS,
     salvo los declarados `de_fondo: true`
  5. las duraciones de los períodos de clima_era2.yaml suman 120 días
  6. ninguna línea sin `procedencia` carece de `deuda`

No llama a ninguna API, no lee curiana_sim/.env y no toca Supabase: sólo
importa curiana_lexicon y curiana_agents_era2 para leer sus datos.

    python 6-fusion/scripts/verificar_sitios_era2.py
    python 6-fusion/scripts/verificar_sitios_era2.py --conteos   # sólo CONTEOS
"""

import argparse
import collections
import glob
import io
import os
import re
import sys

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIM = os.path.join(RAIZ, "curiana_sim")
sys.path.insert(0, SIM)

SITIOS_YAML = os.path.join(RAIZ, "6-fusion", "sitios_era2.yaml")
CLIMA_YAML = os.path.join(RAIZ, "6-fusion", "clima_era2.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")
CORPUS = os.path.join(RAIZ, "3-mundo", "corpus")

DOMINIOS = ("agua", "mar_y_pesca", "recoleccion", "tierra", "monte_y_caza",
            "sal", "materiales")
ETIQUETAS = ("atestiguado", "reconstruido", "canon-simulacion", "hipotetico",
             "retro-abstraido", "testimonio-miguel")
ESTACIONES_OK = ("seca", "seca larga", "lluvias", "todo el año")
MOMENTOS = ("amanecer", "mañana", "mediodia", "tarde", "anochecer", "noche")
DIAS_DEL_ANIO = 120  # curiana_state: DIAS_POR_ESTACION * 2

# ecologia-037, hueco-lex-004, creencia-013, toponimo-108…
RE_ID_CORPUS = re.compile(
    r"\b((?:ecologia|creencia|parentesco|transmision|genealogia|"
    r"geografia_politica)-\d{3}|hueco-lex-\d{3})\b")

fallos = []
avisos = []


def falla(msg):
    fallos.append(msg)


def avisa(msg):
    avisos.append(msg)


def _forzar_utf8():
    """La consola de Windows es cp1252 y revienta con « o ü."""
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace",
                line_buffering=True))


def cargar(ruta):
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ──────────────────────────────────────────────────────────────────
# Los tres padrones contra los que se valida
# ──────────────────────────────────────────────────────────────────

def padron_obras():
    d = cargar(BIBLIO)
    obras = d.get("obras", [])
    if isinstance(obras, dict):
        return set(obras)
    return {o.get("id") or o.get("clave") for o in obras if isinstance(o, dict)}


def padron_hechos():
    ids = set()
    for ruta in sorted(glob.glob(os.path.join(CORPUS, "*.yaml"))):
        d = cargar(ruta)
        listas = [d] if isinstance(d, list) else [
            v for v in d.values() if isinstance(v, list)]
        for lista in listas:
            for e in lista:
                if isinstance(e, dict) and isinstance(e.get("id"), str):
                    ids.add(e["id"])
    return ids


def padron_lexicon():
    import curiana_lexicon as L
    return {k: L.capa_epistemica(v.get("fuente", ""))
            for k, v in L.VOCABULARIO_BASE.items()}


def padron_sitios_motor():
    """Los SITIOS del módulo generado del elenco de la era 2."""
    try:
        import curiana_agents_era2 as E
    except Exception as e:                      # pragma: no cover
        falla(f"no se pudo importar curiana_agents_era2: {e}")
        return set()
    return set(E.SITIOS)


# ──────────────────────────────────────────────────────────────────
# Recorrido genérico: toda línea con `dato` es una línea de canon
# ──────────────────────────────────────────────────────────────────

def lineas_de(nodo, ruta=""):
    """Rinde (ruta, dict) por cada dict con clave `dato`."""
    if isinstance(nodo, dict):
        if "dato" in nodo:
            yield ruta, nodo
        for k, v in nodo.items():
            yield from lineas_de(v, f"{ruta}.{k}" if ruta else str(k))
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            yield from lineas_de(v, f"{ruta}[{i}]")


def texto_de(nodo):
    """Todo el texto del árbol, para cazar ids de corpus citados en prosa."""
    if isinstance(nodo, str):
        yield nodo
    elif isinstance(nodo, dict):
        for v in nodo.values():
            yield from texto_de(v)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from texto_de(v)


def obras_citadas(nodo):
    """Rinde (ruta, obra) por cada `procedencia.obra` del árbol."""
    if isinstance(nodo, dict):
        pr = nodo.get("procedencia")
        if isinstance(pr, dict) and pr.get("obra"):
            yield pr["obra"]
        elif isinstance(pr, list):
            for p in pr:
                if isinstance(p, dict) and p.get("obra"):
                    yield p["obra"]
        for v in nodo.values():
            yield from obras_citadas(v)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from obras_citadas(v)


def voces_citadas(nodo):
    """Rinde dicts de `voz_caquetia` ({clave, capa}) del árbol."""
    if isinstance(nodo, dict):
        vc = nodo.get("voz_caquetia")
        if isinstance(vc, dict):
            yield vc
        elif isinstance(vc, list):
            for v in vc:
                if isinstance(v, dict):
                    yield v
        for v in nodo.values():
            yield from voces_citadas(v)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from voces_citadas(v)


# ──────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--conteos", action="store_true",
                    help="sólo los conteos y el resultado")
    args = ap.parse_args()

    for ruta in (SITIOS_YAML, CLIMA_YAML):
        if not os.path.exists(ruta):
            falla(f"no existe {os.path.relpath(ruta, RAIZ)}")
    if fallos:
        for m in fallos:
            print(f"  FALLO: {m}")
        return 1

    sitios_doc = cargar(SITIOS_YAML)
    clima_doc = cargar(CLIMA_YAML)
    OBRAS = padron_obras()
    HECHOS = padron_hechos()
    LEX = padron_lexicon()
    SITIOS_MOTOR = padron_sitios_motor()

    # ── 1. procedencia.obra es clave foránea ──────────────────────
    for nombre, doc in (("sitios", sitios_doc), ("clima", clima_doc)):
        for obra in obras_citadas(doc):
            if obra not in OBRAS:
                falla(f"{nombre}: procedencia.obra «{obra}» no está en bibliografia.yaml")

    # ── 2. los ids de hecho citados existen ───────────────────────
    citados = collections.Counter()
    for nombre, doc in (("sitios", sitios_doc), ("clima", clima_doc)):
        for txt in texto_de(doc):
            for m in RE_ID_CORPUS.findall(txt):
                citados[m] += 1
                if m not in HECHOS:
                    falla(f"{nombre}: el hecho «{m}» no existe en 3-mundo/corpus/")

    # ── 3. voz_caquetia existe con la capa declarada ──────────────
    voces = []
    for nombre, doc in (("sitios", sitios_doc), ("clima", clima_doc)):
        for vc in voces_citadas(doc):
            clave = vc.get("clave")
            capa = vc.get("capa")
            voces.append((nombre, clave, capa))
            if clave not in LEX:
                falla(f"{nombre}: la voz «{clave}» no está en VOCABULARIO_BASE")
                continue
            real = LEX[clave]
            if real is None:
                falla(f"{nombre}: la voz «{clave}» no es caquetía "
                      f"(capa_epistemica devuelve None)")
            elif capa != real:
                falla(f"{nombre}: la voz «{clave}» declara capa «{capa}» "
                      f"y el lexicón dice «{real}»")

    # ── 4. cada sitio está en SITIOS del motor, salvo los de fondo ─
    sitios = sitios_doc.get("sitios") or []
    if not isinstance(sitios, list) or not sitios:
        falla("sitios_era2.yaml: falta la lista `sitios`")
        sitios = []
    for s in sitios:
        nom = s.get("sitio")
        if s.get("de_fondo"):
            if nom in SITIOS_MOTOR:
                avisa(f"«{nom}» se declara de_fondo pero SÍ está en "
                      f"curiana_agents_era2.SITIOS")
            continue
        if nom not in SITIOS_MOTOR:
            falla(f"el sitio «{nom}» no está en curiana_agents_era2.SITIOS "
                  f"({', '.join(sorted(SITIOS_MOTOR))})")
    en_yaml = {s.get("sitio") for s in sitios}
    for nom in sorted(SITIOS_MOTOR - en_yaml):
        falla(f"curiana_agents_era2.SITIOS tiene «{nom}» y sitios_era2.yaml no")

    # ── 5. las duraciones de clima suman 120 ──────────────────────
    periodos = clima_doc.get("periodos") or []
    if not isinstance(periodos, list) or not periodos:
        falla("clima_era2.yaml: falta la lista `periodos`")
        periodos = []
    suma = sum(int(p.get("dias_simulados") or 0) for p in periodos)
    if suma != DIAS_DEL_ANIO:
        falla(f"las duraciones de clima suman {suma} y el año del motor "
              f"tiene {DIAS_DEL_ANIO} días simulados")
    suma_meses = sum(int(p.get("meses_n") or 0) for p in periodos)
    if suma_meses != 12:
        falla(f"los meses de los períodos suman {suma_meses} y el año tiene 12")

    # ── 6. toda línea sin procedencia lleva deuda; etiquetas y capas ──
    todas = []
    for nombre, doc in (("sitios", sitios_doc), ("clima", clima_doc)):
        for ruta, ln in lineas_de(doc):
            todas.append((nombre, ruta, ln))
            tiene_proc = bool(ln.get("procedencia"))
            if not tiene_proc and not ln.get("deuda"):
                falla(f"{nombre}:{ruta} — sin procedencia y sin deuda: "
                      f"«{str(ln.get('dato'))[:60]}»")
            if tiene_proc and ln.get("deuda"):
                avisa(f"{nombre}:{ruta} — declara procedencia Y deuda")
            et = ln.get("etiqueta")
            if et not in ETIQUETAS:
                falla(f"{nombre}:{ruta} — etiqueta «{et}» fuera de "
                      f"{list(ETIQUETAS)}")
            est = ln.get("estacion")
            if est is not None:
                base = str(est).split(" — ")[0].strip()
                if base not in ESTACIONES_OK:
                    falla(f"{nombre}:{ruta} — estacion «{est}» fuera de "
                          f"{list(ESTACIONES_OK)}")
            if ln.get("hueco_lexico") and ln.get("voz_caquetia"):
                falla(f"{nombre}:{ruta} — declara hueco_lexico Y voz_caquetia")
            if et == "testimonio-miguel" and not ln.get("que_lo_subiria"):
                falla(f"{nombre}:{ruta} — testimonio de Miguel sin `que_lo_subiria`")

    # ── CONTEOS (regla 1) ─────────────────────────────────────────
    por_sitio = collections.Counter()
    por_dominio = collections.Counter()
    por_sitio_dominio = {}
    for s in sitios:
        nom = s.get("sitio")
        doms = s.get("dominios") or {}
        for dom, lista in doms.items():
            if dom not in DOMINIOS:
                falla(f"«{nom}»: dominio «{dom}» fuera de {list(DOMINIOS)}")
            n = len(lista or [])
            por_sitio[nom] += n
            por_dominio[dom] += n
            por_sitio_dominio.setdefault(nom, collections.Counter())[dom] = n

    por_etiqueta = collections.Counter(ln.get("etiqueta") for _, _, ln in todas)
    por_capa = collections.Counter(ln.get("capa") or "—" for _, _, ln in todas)
    por_estacion = collections.Counter(
        str(ln.get("estacion") or "—").split(" — ")[0] for _, _, ln in todas)
    huecos = [ln for _, _, ln in todas if ln.get("hueco_lexico")]
    testimonios = [ln for _, _, ln in todas
                   if ln.get("etiqueta") == "testimonio-miguel"]
    con_deuda = [ln for _, _, ln in todas if ln.get("deuda")]
    lineas_sitios = [x for x in todas if x[0] == "sitios"]
    lineas_clima = [x for x in todas if x[0] == "clima"]

    medido = {
        "lineas_total": len(todas),
        "lineas_sitios": len(lineas_sitios),
        "lineas_clima": len(lineas_clima),
        "sitios": len(sitios),
        "huecos_lexicos": len(huecos),
        "testimonios_miguel": len(testimonios),
        "lineas_con_deuda": len(con_deuda),
        "voces_caquetias_citadas": len({v[1] for v in voces}),
        "hechos_del_corpus_citados": len(citados),
        "obras_citadas": len(set(obras_citadas(sitios_doc)) |
                             set(obras_citadas(clima_doc))),
        "dias_simulados": suma,
    }

    # el YAML declara lo mismo que este script mide, o es un bug del YAML
    for nombre, doc in (("sitios", sitios_doc), ("clima", clima_doc)):
        decl = ((doc.get("meta") or {}).get("medido") or {})
        for k, v in decl.items():
            if k in medido and medido[k] != v:
                falla(f"{nombre}: meta.medido.{k} dice {v} y se mide {medido[k]}")

    print("── CONTEOS ──")
    for k, v in medido.items():
        print(f"  {k:28} {v}")

    print("\n── LÍNEAS POR SITIO Y DOMINIO ──")
    cab = "  {:22}" + "".join(" {:>12}" for _ in DOMINIOS) + " {:>6}"
    print(cab.format("sitio", *DOMINIOS, "total"))
    for s in sitios:
        nom = s.get("sitio")
        c = por_sitio_dominio.get(nom, collections.Counter())
        print(cab.format(nom[:22], *[str(c.get(d, 0)) for d in DOMINIOS],
                         str(por_sitio[nom])))
    print(cab.format("TOTAL", *[str(por_dominio.get(d, 0)) for d in DOMINIOS],
                     str(sum(por_sitio.values()))))

    print("\n── POR ETIQUETA ──")
    for k, v in por_etiqueta.most_common():
        print(f"  {str(k):20} {v}")
    print("\n── POR CAPA ──")
    for k, v in por_capa.most_common():
        print(f"  {str(k):40} {v}")
    print("\n── POR ESTACIÓN ──")
    for k, v in por_estacion.most_common():
        print(f"  {str(k):20} {v}")

    print("\n── HUECOS LÉXICOS DECLARADOS ──")
    for ln in huecos:
        print(f"  {str(ln.get('concepto') or ln.get('dato'))[:96]}")
    print("\n── TESTIMONIOS DE MIGUEL ──")
    for ln in testimonios:
        print(f"  {str(ln.get('dato'))[:96]}")

    if not args.conteos:
        print("\n── PERÍODOS DEL AÑO ──")
        for p in periodos:
            print(f"  {str(p.get('id')):16} {str(p.get('nombre_canon')):22} "
                  f"{str(p.get('meses')):16} {p.get('meses_n')} meses "
                  f"→ {p.get('dias_simulados')} días simulados")
        print(f"  {'suma':16} {'':22} {'':16} {suma_meses} meses "
              f"→ {suma} días simulados")

        print("\n── VOCES CAQUETÍAS CITADAS ──")
        for clave in sorted({v[1] for v in voces}):
            print(f"  {clave:16} {LEX.get(clave)}")

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
