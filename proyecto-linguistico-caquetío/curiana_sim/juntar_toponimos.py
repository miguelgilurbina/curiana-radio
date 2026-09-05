#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — juntar los topónimos: todos, por fuente
=================================================

Hasta el 2026-09-04 los topónimos del proyecto vivían repartidos en doce
sitios: el canon (2-lengua/toponimos.yaml), el índice de Esteves como cola,
las once ciudades de Castellanos, los cinco de Bastidas vía Velasco, las
lecturas de González Batista y de Arcaya, las estaciones de petroglifos de
Morón, los que el dictado de Medina Colina mandó a la cola, los de Gatschet
y van Buurt en las islas, la asignación de clanes de Delmonte vía Oliver, el
mapa de Miguel y el registro de nodos. Para procesar la cola había que abrir
todo. Este script los junta en UN registro, agrupados por obra (regla 8: la
obra es clave foránea a bibliografia.yaml; lo que no tiene obra lo dice), y
cruza cada forma contra el canon, contra Esteves, contra los nodos y contra
el mapa de Miguel.

QUÉ NO ES: no es canon ni propuesta de fusión. Es una VISTA generada para
trabajar la campaña de topónimos (SIGUIENTE_TANDA §B.5). No se edita a mano:
se edita la fuente y se regenera. Las cifras salen medidas (regla 1).

    python juntar_toponimos.py

Escribe:
    6-fusion/toponimos_por_fuente.yaml    los datos (por_fuente + indice_de_formas)
    6-fusion/TOPONIMOS_POR_FUENTE.md      la vista para leer
"""

from __future__ import annotations

import io
import re
import sys
import unicodedata
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass, field, asdict
from datetime import date
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
SIM = RAIZ / "curiana_sim"
FUSION = RAIZ / "6-fusion"
sys.path.insert(0, str(SIM))

SALIDA_YAML = FUSION / "toponimos_por_fuente.yaml"
SALIDA_MD = FUSION / "TOPONIMOS_POR_FUENTE.md"

# Lo que no tiene obra en la bibliografía se declara así (regla 8): el hueco
# se admite, callarlo no.
TESTIMONIO = "testimonio-miguel"


def _forzar_utf8():
    """La consola de Windows es cp1252 y revienta con « o ü."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def leer_yaml(rel: str):
    return yaml.safe_load((RAIZ / rel).read_text(encoding="utf-8"))


# ══════════════════════════════════════════════════════════════════════
# LA MENCIÓN — una forma, en una fuente, con lo que esa fuente dice de ella
# ══════════════════════════════════════════════════════════════════════

@dataclass
class Mencion:
    forma: str                 # tal como la escribe la fuente
    fuente: str                # id de bibliografia.yaml, o testimonio-miguel
    tipo: str                  # canon | indice | primario-1538 | lista-1589 | lectura | mapa | ...
    donde: str                 # archivo/sección de donde sale (para volver)
    dato: str = ""             # glosa / nota / lectura, corta
    ref: str = ""              # página, id, nivel
    identificado_con: str = "" # forma moderna o canónica que la propia nota declara
    variantes: list = field(default_factory=list)
    epoca: str = ""            # solo cuando la fuente la declara (regla 3)


ARTICULOS = re.compile(r"^(el|la|los|las)\s+", re.I)
PARENTESIS = re.compile(r"\s*\([^)]*\)")


def clave(forma: str) -> str:
    """Clave de cruce: sin tildes, sin artículo, solo letras. `El Supí` y
    `supi` caen juntos; `Todariquibo` y `Todariquiba` NO (la identificación
    la declara la nota, no el algoritmo)."""
    f = PARENTESIS.sub("", forma).strip()
    f = ARTICULOS.sub("", f)
    f = unicodedata.normalize("NFD", f.lower())
    f = "".join(c for c in f if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", f)


def partir_variantes(texto: str) -> list[str]:
    """`Andicuri, Andicouri` · `Cayerda / Cayerúa` → lista de formas."""
    return [v.strip() for v in re.split(r"\s*[,/]\s*", texto) if v.strip()]


def corto(texto, n=110) -> str:
    t = " ".join(str(texto or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


# ══════════════════════════════════════════════════════════════════════
# LOS EXTRACTORES — uno por sitio donde viven topónimos
# ══════════════════════════════════════════════════════════════════════

def canon() -> list[Mencion]:
    """2-lengua/toponimos.yaml — 74 entradas. La procedencia formal la tienen
    14; para el resto, la fuente la declara la propuesta curada
    (lexicon_toponimos.py) o se infiere por cruce con los glosarios de origen
    (Zavala, van Buurt, Gatschet) — y se etiqueta como inferida."""
    import lexicon_toponimos as lt
    import lexicon_zavala as lz
    import lexicon_van_buurt as vb
    import lexicon_gatschet as lg

    declarada: dict[str, str] = {}
    for nombre in ("NIVEL_A", "NIVEL_B", "NIVEL_C"):
        for forma, e in getattr(lt, nombre).items():
            if isinstance(e, dict) and e.get("fuente"):
                declarada[clave(forma)] = e["fuente"]

    en_zavala = {clave(f) for f in lz.TOPONIMOS_ZAVALA} | {clave(f) for f in lz.ANTROPONIMOS_ZAVALA}
    en_vb_etim = {clave(f) for f in vb.ETIMOLOGIAS_TOPONIMOS}
    en_vb_s7 = {clave(v) for isla in vb.TOPONIMOS_VAN_BUURT.values()
                for t in isla for v in partir_variantes(t["toponimo"])}
    en_gatschet = {clave(f) for f in lg.GATSCHET_TOPONIMOS}

    def obra_de(fuente_txt: str) -> str:
        return fuente_txt.split(" ")[0].strip()

    out = []
    for t in leer_yaml("2-lengua/toponimos.yaml")["toponimos"]:
        # El campo `forma` del canon arrastra restos como «aruba → 'Oruba…'»
        # (bug-campo-forma, lengua_toponimia_quibacoa.yaml §higiene): la forma
        # es lo de antes de la flecha; el resto se conserva como dato.
        cruda = str(t["forma"])
        forma = re.split(r"\s*[→←]\s*", cruda)[0].strip()
        resto = cruda[len(forma):].strip()
        k = clave(forma)
        proc = (t.get("procedencia") or {}).get("obra")
        if proc:
            fuente, como = proc, "procedencia"
        elif k in declarada:
            fuente, como = obra_de(declarada[k]), "declarada-en-lexicon_toponimos"
        elif k in en_vb_etim or k in en_vb_s7:
            fuente, como = "van-buurt-2014", "inferida-por-cruce"
        elif k in en_gatschet:
            fuente, como = "gatschet-1885", "inferida-por-cruce"
        elif k in en_zavala:
            fuente, como = "zavala-reyes-2015", "inferida-por-cruce"
        else:
            fuente, como = "sin-procedencia", "deuda"
        glosa = t.get("glosa_fuente") or t.get("glosa_reconstruida") or ""
        out.append(Mencion(
            forma=forma, fuente=fuente, tipo="canon",
            donde="2-lengua/toponimos.yaml",
            dato=corto(f"{resto} {glosa}".strip()),
            ref=f"{t['id']} · nivel {t['nivel']} · {t.get('clase', '')} · fuente {como}",
        ))
    return out


def esteves() -> list[Mencion]:
    """El índice 'Topónimos compilados' (pp. 68-69): la cola de la campaña."""
    d = leer_yaml("6-fusion/toponimos_esteves_indice.yaml")
    out = []
    for e in d.get("ya_registrados", []):
        out.append(Mencion(e["forma"], "esteves-1989", "indice",
                           "6-fusion/toponimos_esteves_indice.yaml §ya_registrados",
                           ref=e.get("canon", "")))
    for e in d.get("por_procesar", []):
        dato = "estrato no caquetío según Esteves" if e.get("estrato") else ""
        out.append(Mencion(e["forma"], "esteves-1989", "indice",
                           "6-fusion/toponimos_esteves_indice.yaml §por_procesar", dato=dato))
    return out


IGUAL = re.compile(r"=\s*([A-Za-zÁÉÍÓÚÑáéíóúñ]+(?:/[A-Za-zÁÉÍÓÚÑáéíóúñ]+)*)")


def castellanos() -> list[Mencion]:
    """Las once ciudades (Elegías, II-1, 1589)."""
    d = leer_yaml("6-fusion/castellanos_1589_toponimos.yaml")
    out = []
    obra = d.get("meta", {}).get("obra", "castellanos-elegias")
    for t in d["lista_de_ciudades"]["toponimos"]:
        nota = t.get("nota", "")
        m = IGUAL.search(nota)
        alts = m.group(1).split("/") if m else []
        out.append(Mencion(t["forma_1589"], obra, "lista-1589",
                           "6-fusion/castellanos_1589_toponimos.yaml §lista_de_ciudades",
                           dato=corto(nota), ref="II, Elegía 1",
                           identificado_con=alts[0] if alts else "", variantes=alts[1:],
                           epoca="colonial (1589)"))
    return out


def bastidas() -> list[Mencion]:
    """Los cinco pueblos de la carta de Bastidas (AGI, 8-X-1538), vía Velasco 2015."""
    d = leer_yaml("6-fusion/velasco_primarios_agi.yaml")
    out = []
    for a in d["toponimos_primarios"]["atestaciones"]:
        m = IGUAL.search(a.get("valor", ""))
        out.append(Mencion(a["forma_1538"], "velasco-2015-resistencia", "primario-1538",
                           "6-fusion/velasco_primarios_agi.yaml §toponimos_primarios",
                           dato=corto(a.get("dato", "")), ref="AGI, Legajo 218, f. 2",
                           identificado_con=m.group(1).split("/")[0] if m else "",
                           epoca="colonial (1538)"))
    # y el testimonio de Miguel sobre Judibana vive en el mismo archivo
    j = d.get("judibana_tradicion", {}).get("testimonio", {})
    if j:
        out.append(Mencion("Judibana", TESTIMONIO, "testimonio-residente",
                           "6-fusion/velasco_primarios_agi.yaml §judibana_tradicion",
                           dato="nombre de la hija de Manaure, unida al señor de Jurijurebo (tradición local viva); etimología judi+bana 'el cerro del viento'",
                           ref=j.get("quien", "")))
    return out


def gonzalez_batista() -> list[Mencion]:
    """Las lecturas de González Batista (toponimia_coro_espina.yaml) — con
    cautela declarada (veredicto-cautela-general)."""
    d = leer_yaml("6-fusion/toponimia_coro_espina.yaml")
    OBRA, DONDE = "gonzalez-batista-nombre-de-coro", "6-fusion/toponimia_coro_espina.yaml"
    out = []
    for p in d.get("plural", []):
        for c in p.get("casos_del_autor", []) or []:
            out.append(Mencion(c["forma"], OBRA, "lectura", f"{DONDE} §{p['id']}",
                               dato=f"{c.get('base', '')} → {c.get('glosa', '')}", ref="plural por reduplicación"))
        c = p.get("caso_del_autor")
        if c:
            out.append(Mencion(c["forma"], OBRA, "lectura", f"{DONDE} §{p['id']}",
                               dato=corto(c.get("glosa") or c.get("analisis_del_autor", "")),
                               ref=p["mecanismo"] if isinstance(p.get("mecanismo"), str) else "",
                               variantes=[c["forma_antigua"]] if c.get("forma_antigua") else []))
    for fam in d.get("familia_coro", []):
        if fam["id"] == "coro-espina":
            out.append(Mencion("Coro", OBRA, "lectura", f"{DONDE} §coro-espina",
                               dato="coro = 'espina' (el autor); choca con Alvarado, donde coro es siempre topónimo"))
        if fam["id"] == "coriana-tierra-de-espinas":
            out.append(Mencion("Coriana", OBRA, "lectura", f"{DONDE} §coriana-tierra-de-espinas",
                               dato="'tierra de las espinas' — depende de na = 'tierra' (choca con Zavala #184)",
                               variantes=["Curiana"]))
            out.append(Mencion("Paraguaná", OBRA, "lectura", f"{DONDE} §coriana-tierra-de-espinas",
                               dato="paragua 'mar' + na 'tierra' = 'la tierra rodeada de mar' (misma dependencia)"))
    for m in d.get("morfemas_del_autor", []):
        caso = m.get("caso", "")
        if " = " in caso:
            izq = caso.split(" = ")[0]
            formas = partir_variantes(izq)
            out.append(Mencion(formas[0], OBRA, "lectura", f"{DONDE} §morfemas_del_autor",
                               dato=corto(caso), ref=f"morfema {m['forma']} = '{m['glosa']}'",
                               variantes=formas[1:]))
    return out


def arcaya() -> list[Mencion]:
    """Arcaya 1920: Quiquibacoa/Coquibacoa (p. 130), Curiana (p. 169) y la
    serie Coro-/Curi- (p. 170) — citados en dos propuestas de 6-fusion."""
    OBRA = "arcaya-1920"
    out = []
    q = leer_yaml("6-fusion/lengua_toponimia_quibacoa.yaml")
    for t in q.get("toponimos", []):
        if t["id"] == "rehabilitar-quiquiba":
            out.append(Mencion("Quiquibacoa", OBRA, "lectura",
                               "6-fusion/lengua_toponimia_quibacoa.yaml §rehabilitar-quiquiba",
                               dato=f"{t['segmentacion_propuesta']} = '{t['glosa_reconstruida']}'",
                               ref=f"p. {t['procedencia']['pagina']}", variantes=["Coquibacoa", "Quiquiba"]))
        if t["id"] == "escalado-sitio-region":
            out.append(Mencion("Curiana", OBRA, "lectura",
                               "6-fusion/lengua_toponimia_quibacoa.yaml §escalado-sitio-region",
                               dato="el pueblo indígena de Coro, y 'la costa vecina' — sitio → región (¿quién extendió qué? D2)",
                               ref="p. 169", variantes=["Coro"]))
    c = leer_yaml("6-fusion/toponimia_coro_espina.yaml")
    for fam in c.get("familia_coro", []):
        apoyo = fam.get("apoyo_de_arcaya", "")
        m = re.search(r"la antigua ([^\"”]+)", apoyo)
        if m:
            for f in partir_variantes(m.group(1)):
                out.append(Mencion(f, OBRA, "serie", "6-fusion/toponimia_coro_espina.yaml §apoyo_de_arcaya",
                                   dato="serie Coro-/Curi- de Arcaya (él propone koori 'avispa' o kuru 'lagartija', no 'espina')",
                                   ref="p. 170"))
    return out


def moron() -> list[Mencion]:
    """Morón 2012: La Cuiba y ~20 estaciones de arte rupestre de Falcón."""
    d = leer_yaml("6-fusion/petroglifos_y_manaure.yaml")
    OBRA, DONDE = "moron-2012-petroglifos", "6-fusion/petroglifos_y_manaure.yaml §toponimia"
    out = []
    for t in d.get("toponimia", []):
        if t["id"] == "la-cuiba-piedra":
            out.append(Mencion(t["forma"], OBRA, "lectura", DONDE,
                               dato="cuiva/quiva 'piedra': el sitio tiene cristales de cuarzo a ras del suelo",
                               variantes=partir_variantes(t.get("tambien", "").replace(" · ", ", "))))
        if t["id"] == "estaciones-de-petroglifos":
            for zona in ("costa", "sabana_arida", "sierra_de_san_luis", "otras"):
                for f in t.get(zona, []) or []:
                    out.append(Mencion(f, OBRA, "estacion-rupestre", DONDE,
                                       dato=f"estación de arte rupestre — {zona.replace('_', ' ')}"))
    return out


CRUCE_TOP = re.compile(r"([=≈⊂])\s*([A-Za-zÁÉÍÓÚÑáéíóúñ][\wÁÉÍÓÚÑáéíóúñ]*)")
RELACION = {"=": "igual a", "≈": "parecido a", "⊂": "contenido en"}


def medina_colina() -> list[Mencion]:
    """Lo que el dictado de Medina Colina toca en toponimia: voces que son
    topónimo en Esteves, las que se mandaron a la cola, y los lugares que el
    autor nombra (época s. XX, declarada)."""
    d = leer_yaml("6-fusion/medina_colina_dictado.yaml")
    OBRA, DONDE = "medina-colina-sxx", "6-fusion/medina_colina_dictado.yaml"
    out = []
    for seccion in ("entradas", "descartes"):
        for e in d.get(seccion, []) or []:
            voz, pag = e.get("voz", "?"), e.get("pagina", "")
            tx = str((e.get("cruce") or {}).get("toponimos") or "")
            ref = f"p. {pag}" if pag else ""
            for rel, forma in CRUCE_TOP.findall(tx):
                if forma.lower() in ("nada", "nada;"):
                    continue
                forma = forma.capitalize() if forma.isupper() else forma  # el escriba gritaba en el cruce
                out.append(Mencion(forma, OBRA, "referido-por-voz", f"{DONDE} §{seccion}:{voz}",
                                   dato=f"{RELACION[rel]} la voz «{voz}» (veredicto {e.get('veredicto', '?')})",
                                   ref=ref))
            cola = (e.get("propuesta") or {}).get("toponimo_a_la_cola")
            if cola:
                forma = cola.split("→")[0].split("(")[0].strip()
                out.append(Mencion(forma, OBRA, "a-la-cola", f"{DONDE} §{seccion}:{voz}",
                                   dato=corto(cola), ref=ref))
    lug = d["aclaratorias_al_lector"]["la_poblacion_y_los_pueblos"].get("lugares_nombrados", {})
    for grupo in ("centros_poblados", "otros"):
        for f in lug.get(grupo, []):
            out.append(Mencion(f, OBRA, "lugar-s-xx", f"{DONDE} §aclaratorias_al_lector",
                               dato="centro poblado de Paraguaná según el autor (ninguno llegaba a 2.000 hab.)"
                               if grupo == "centros_poblados" else "nombrado por el autor",
                               epoca=lug.get("epoca", "s. XX")))
    for m in d.get("datos_mundo", []) or []:
        for f in m.get("lugares", []) or []:
            out.append(Mencion(f, OBRA, "isoglosa", f"{DONDE} §datos_mundo:{m['id']}",
                               dato=corto(m.get("hecho", "")), ref=f"p. {m.get('pagina', '')}", epoca="s. XX"))
    return out


def oliver_delmonte() -> list[Mencion]:
    """Los asientos de los dos clanes según Delmonte 1883, vía Oliver cap. 3."""
    d = leer_yaml("6-fusion/paraguana_dos_clanes.yaml")
    OBRA, DONDE = "oliver-1989-cap3", "6-fusion/paraguana_dos_clanes.yaml §paraguana-clanes-asentamientos"
    ok = any(h.get("id") == "paraguana-clanes-asentamientos" for h in d.get("hechos_propuestos", []))
    if not ok:
        return []
    return [
        Mencion("Cayerda", OBRA, "asiento-de-clan", DONDE, dato="primer asiento de los Amuayes (Delmonte 1883); grafías Cayerta/'Coyarna'", ref="p. 276", epoca="colonial"),
        Mencion("Moruy", OBRA, "asiento-de-clan", DONDE, dato="reasentamiento de los Amuayes (confirmado por Oliver)", ref="p. 276", epoca="colonial"),
        Mencion("Santa Ana", OBRA, "asiento-de-clan", DONDE, dato="asiento de los Guaranaos (Delmonte 1883)", ref="p. 276", epoca="colonial"),
        Mencion("Amuay", OBRA, "clan", DONDE, dato="nombre del clan del sur; Esteves lo atribuye a estrato caribe (conflicto declarado)", ref="pp. 275-276"),
        Mencion("Guaranao", OBRA, "clan", DONDE, dato="nombre del clan del norte", ref="pp. 275-276"),
    ]


def van_buurt() -> list[Mencion]:
    """van Buurt 2014 §7 (topónimos ABC sin glosa) y §8-10 (15 etimologías)."""
    import lexicon_van_buurt as vb
    out = []
    for isla, lista in vb.TOPONIMOS_VAN_BUURT.items():
        for t in lista:
            formas = partir_variantes(t["toponimo"])
            gen = f"{t['generico']} " if t.get("generico") else ""
            out.append(Mencion(formas[0], "van-buurt-2014", "indice-abc", f"curiana_sim/lexicon_van_buurt.py TOPONIMOS_VAN_BUURT[{isla}]",
                               dato=f"{isla}{' · genérico ' + t['generico'] if t.get('generico') else ''}{' · dudoso' if t.get('dudoso') else ''}",
                               ref="§7", variantes=formas[1:]))
    for forma, etim in vb.ETIMOLOGIAS_TOPONIMOS.items():
        out.append(Mencion(forma, "van-buurt-2014", "lectura", "curiana_sim/lexicon_van_buurt.py ETIMOLOGIAS_TOPONIMOS",
                           dato=corto(etim), ref="§8-10"))
    return out


def gatschet() -> list[Mencion]:
    """Gatschet 1885 (material de Pinart, Aruba 1882): 31 topónimos de Aruba."""
    import lexicon_gatschet as lg
    out = []
    for forma, e in lg.GATSCHET_TOPONIMOS.items():
        dato = e.get("tipo", "") if isinstance(e, dict) else ""
        vb = e.get("van_buurt_2014") if isinstance(e, dict) else None
        out.append(Mencion(forma, "gatschet-1885", "indice-aruba", "curiana_sim/lexicon_gatschet.py GATSCHET_TOPONIMOS",
                           dato=corto(f"{dato}{' · van Buurt: ' + str(vb) if vb else ''}"), ref="Pinart 1882"))
    return out


def miguel() -> list[Mencion]:
    """La investigación coloquial de Miguel (2026-09-01): lecturas, hipótesis y
    la cola de mapa. Sin obra: deuda sin-procedencia, declarada en el archivo."""
    d = leer_yaml("6-fusion/toponimia_paraguana_miguel.yaml")
    DONDE = "6-fusion/toponimia_paraguana_miguel.yaml"
    out = []
    for l in d.get("lecturas", []):
        formas = partir_variantes(PARENTESIS.sub("", l["toponimo"]))
        out.append(Mencion(formas[0], TESTIMONIO, str(l.get("tipo", "lectura")), f"{DONDE} §lecturas",
                           dato=corto(l.get("lectura", "")), ref=l.get("deuda", ""), variantes=formas[1:]))
        if "CHAMURIANA" in str(l.get("lectura", "")):
            out.append(Mencion("Chamuriana", TESTIMONIO, "tradicion-local", f"{DONDE} §lecturas:{l['toponimo']}",
                               dato="nombre nativo del sitio de Santa Ana, por el agua dulce que baja del cerro", ref=l.get("deuda", "")))
    for h in d.get("hipotesis_estructural", []):
        if h["id"] == "capubana-centro-sagrado":
            out.append(Mencion("Capubana", TESTIMONIO, "hipotesis", f"{DONDE} §{h['id']}",
                               dato="el Cerro Santa Ana = Cerro de Capú (D9); centro sagrado con Moruy, Chamuriana, Cayerúa y Maitiruma en órbita",
                               ref="canon-simulacion (validación de probabilidad)"))
    cola = d.get("cola_de_mapa", {})
    for f in cola.get("candidatos", []):
        out.append(Mencion(f, TESTIMONIO, "mapa", f"{DONDE} §cola_de_mapa",
                           dato="topónimo vivo en las fotos del mapa (sector del Capubana)", ref="2026-09-01"))
    return out


def nodos() -> dict[str, dict]:
    """3-mundo/asentamientos.yaml — el registro de nodos, para el cruce."""
    d = leer_yaml("3-mundo/asentamientos.yaml")
    out = {}
    for n in d.get("nodos", []):
        formas = [n["forma"]] + list(n.get("variantes") or [])
        for f in formas:
            out.setdefault(clave(str(f)), {"id": n["id"], "forma": n["forma"], "etiqueta": n.get("etiqueta"),
                                           "precontacto": n.get("precontacto"),
                                           "obra": (n.get("procedencia") or {}).get("obra")})
    return out


# ══════════════════════════════════════════════════════════════════════
# JUNTAR
# ══════════════════════════════════════════════════════════════════════

# Sin cifras a mano (regla 1): las cuentas van en la tabla, medidas.
DESCRIPCION = OrderedDict([
    ("zavala-reyes-2015", "el glosario (TOPONIMOS_ZAVALA y ANTROPONIMOS_ZAVALA, con glosa española) — la base del canon"),
    ("esteves-1989", "el índice 'Topónimos compilados' de Paraguaná (pp. 68-69): la cola de la campaña"),
    ("castellanos-elegias", "las 'ciudades de grandísimo momento' en torno a Coro (II, Elegía 1, 1589)"),
    ("velasco-2015-resistencia", "los pueblos de la carta de Bastidas al rey (AGI, 1538) — primarios"),
    ("gonzalez-batista-nombre-de-coro", "lecturas etimológicas del autor — con cautela declarada; cada una se juzga contra Zavala"),
    ("arcaya-1920", "Quiquibacoa/Coquibacoa, Curiana y la serie Coro-/Curi-"),
    ("moron-2012-petroglifos", "La Cuiba y las estaciones de arte rupestre de Falcón"),
    ("oliver-1989-cap3", "los asientos de los dos clanes de Paraguaná según Delmonte 1883"),
    ("medina-colina-sxx", "lo que el dictado toca: voces que son topónimo en Esteves, lo mandado a la cola, y los pueblos del autor (s. XX)"),
    ("gatschet-1885", "topónimos de Aruba (material de Pinart, 1882), sin glosa"),
    ("van-buurt-2014", "§7 topónimos de Aruba, Bonaire y Curazao sin glosa; §8-10 las etimologías del autor"),
    (TESTIMONIO, "Miguel Gil Urbina: lecturas de investigación coloquial, tradición local, mapa vivo — deuda sin-procedencia, por diseño"),
    ("sin-procedencia", "entradas del canon cuya fuente no se pudo declarar ni inferir — deuda"),
])


def juntar():
    bib = leer_yaml("4-fuentes/bibliografia.yaml")
    ids_bib = {o["id"] for o in bib["obras"]}

    menciones: list[Mencion] = []
    for extractor in (canon, esteves, castellanos, bastidas, gonzalez_batista, arcaya,
                      moron, oliver_delmonte, medina_colina, gatschet, van_buurt, miguel):
        menciones += extractor()

    avisos = []
    for obra in {m.fuente for m in menciones}:
        if obra not in ids_bib and obra not in (TESTIMONIO, "sin-procedencia"):
            avisos.append(f"⚠️ obra sin ficha en bibliografia.yaml: {obra}")

    # ── el índice de formas: una entrada por clave, con todas sus fuentes ──
    indice: dict[str, dict] = {}
    for m in menciones:
        claves = [clave(m.forma)] + [clave(v) for v in m.variantes]
        if m.identificado_con:
            claves.append(clave(m.identificado_con))
        claves = [k for k in claves if k]
        if not claves:
            continue
        # una identificación declarada (Todariquibo = Todariquiba) une las claves
        k0 = claves[0]
        destino = None
        for k in claves:
            if k in indice:
                destino = indice[k]
                break
        if destino is None:
            destino = {"forma": m.forma, "variantes": [], "fuentes": [], "menciones": []}
        for k in claves:
            indice[k] = destino
        for v in [m.forma] + m.variantes + ([m.identificado_con] if m.identificado_con else []):
            if v and v != destino["forma"] and v not in destino["variantes"]:
                destino["variantes"].append(v)
        if m.fuente not in destino["fuentes"]:
            destino["fuentes"].append(m.fuente)
        destino["menciones"].append(m)

    entradas = []
    vistos = set()
    for k, e in indice.items():
        if id(e) in vistos:
            continue
        vistos.add(id(e))
        entradas.append(e)

    nodo_por_clave = nodos()

    def cruces(e):
        ks = {clave(e["forma"])} | {clave(v) for v in e["variantes"]}
        can = next((m for m in e["menciones"] if m.tipo == "canon"), None)
        nodo = next((nodo_por_clave[k] for k in ks if k in nodo_por_clave), None)
        return {
            "en_canon": can.ref.split(" · ")[0] + " · " + can.ref.split(" · ")[1] if can else None,
            "en_esteves": any(m.fuente == "esteves-1989" for m in e["menciones"]),
            "en_mapa_miguel": any(m.tipo == "mapa" for m in e["menciones"]),
            "en_nodos": f"{nodo['id']} ({nodo['etiqueta']}, precontacto {nodo['precontacto']})" if nodo else None,
        }

    for e in entradas:
        e["cruces"] = cruces(e)

    entradas.sort(key=lambda e: clave(e["forma"]))
    # toda clave (forma, variante o identificación) → su entrada del índice
    return menciones, entradas, avisos, ids_bib, indice


# ══════════════════════════════════════════════════════════════════════
# ESCRIBIR
# ══════════════════════════════════════════════════════════════════════

MARCA = {"canon": "★", "esteves": "≡", "mapa": "◆", "nodo": "⌂"}


def marcas(e) -> str:
    c = e["cruces"]
    return "".join([MARCA["canon"] if c["en_canon"] else "", MARCA["esteves"] if c["en_esteves"] else "",
                    MARCA["mapa"] if c["en_mapa_miguel"] else "", MARCA["nodo"] if c["en_nodos"] else ""])


def escribir(menciones, entradas, avisos, ids_bib, indice):
    por_fuente = OrderedDict()
    for obra in DESCRIPCION:
        ms = [m for m in menciones if m.fuente == obra]
        if not ms:
            continue
        formas = {clave(m.forma) for m in ms}
        por_fuente[obra] = {"obra": obra, "en_bibliografia": obra in ids_bib,
                            "descripcion": DESCRIPCION[obra], "menciones": len(ms), "formas": len(formas),
                            "toponimos": [{k: v for k, v in asdict(m).items() if v not in ("", [], None) and k != "fuente"} for m in ms]}
    for obra in {m.fuente for m in menciones} - set(por_fuente):
        ms = [m for m in menciones if m.fuente == obra]
        por_fuente[obra] = {"obra": obra, "en_bibliografia": obra in ids_bib, "descripcion": "",
                            "menciones": len(ms), "formas": len({clave(m.forma) for m in ms}),
                            "toponimos": [{k: v for k, v in asdict(m).items() if v not in ("", [], None) and k != "fuente"} for m in ms]}

    entrada_por_clave = indice  # incluye variantes e identificaciones (Cayerúa → la entrada de Cayerda)

    def formas_de(obra):
        return {clave(m.forma) for m in menciones if m.fuente == obra}

    def cruce(a, b):
        ea = {id(entrada_por_clave.get(k)) for k in formas_de(a) if k in entrada_por_clave}
        eb = {id(entrada_por_clave.get(k)) for k in formas_de(b) if k in entrada_por_clave}
        return sorted(e["forma"] for e in entradas if id(e) in ea & eb)

    mapa = [e for e in entradas if e["cruces"]["en_mapa_miguel"]]
    solo_cola = [e for e in entradas if not e["cruces"]["en_canon"] and not e["cruces"]["en_nodos"]]
    resumen = {
        "menciones": len(menciones),
        "formas_distintas": len(entradas),
        "fuentes": len(por_fuente),
        "por_fuente": OrderedDict((o, {"menciones": v["menciones"], "formas": v["formas"]}) for o, v in por_fuente.items()),
        "en_canon": sum(1 for e in entradas if e["cruces"]["en_canon"]),
        "en_nodos": sum(1 for e in entradas if e["cruces"]["en_nodos"]),
        "sin_canon_ni_nodo": len(solo_cola),
        "cruces": {
            "mapa_de_miguel_en_esteves": sorted(e["forma"] for e in mapa if e["cruces"]["en_esteves"]),
            "mapa_de_miguel_fuera_de_esteves": sorted(e["forma"] for e in mapa if not e["cruces"]["en_esteves"]),
            "castellanos_1589_en_esteves": cruce("castellanos-elegias", "esteves-1989"),
            "castellanos_1589_y_bastidas_1538": cruce("castellanos-elegias", "velasco-2015-resistencia"),
            "bastidas_1538_en_esteves": cruce("velasco-2015-resistencia", "esteves-1989"),
            "medina_colina_en_esteves": cruce("medina-colina-sxx", "esteves-1989"),
            "medina_colina_en_canon": sorted(e["forma"] for e in entradas if e["cruces"]["en_canon"] and "medina-colina-sxx" in e["fuentes"]),
            "en_mas_de_dos_fuentes": sorted(f"{e['forma']} ({len(e['fuentes'])})" for e in entradas if len(e["fuentes"]) >= 3),
        },
    }

    doc = OrderedDict([
        ("meta", OrderedDict([
            ("generado_por", "curiana_sim/juntar_toponimos.py"),
            ("generado", str(date.today())),
            ("editar_a_mano", "no — se edita la fuente y se regenera"),
            ("que_es", "vista: todos los topónimos del proyecto, agrupados por obra y cruzados entre sí. No es canon ni propuesta de fusión."),
            ("marcas", "★ en el canon · ≡ en el índice de Esteves · ◆ en el mapa de Miguel · ⌂ en asentamientos.yaml"),
            ("resumen", resumen),
            ("avisos", avisos),
        ])),
        ("por_fuente", list(por_fuente.values())),
        ("indice_de_formas", [OrderedDict([
            ("forma", e["forma"]), ("variantes", e["variantes"]), ("fuentes", e["fuentes"]),
            ("cruces", e["cruces"]),
            ("menciones", [f"{m.fuente} · {m.tipo}" + (f" · {m.ref}" if m.ref else "") for m in e["menciones"]]),
        ]) for e in entradas]),
    ])

    yaml.add_representer(OrderedDict, lambda d, data: d.represent_dict(data.items()))
    SALIDA_YAML.write_text(
        "# GENERADO por curiana_sim/juntar_toponimos.py — no editar a mano.\n"
        "# Vista de todos los topónimos del proyecto por fuente; la campaña se\n"
        "# trabaja desde aquí, pero el canon sigue siendo 2-lengua/toponimos.yaml.\n"
        + yaml.dump(doc, allow_unicode=True, sort_keys=False, width=110, default_flow_style=False),
        encoding="utf-8", newline="\n")

    # ── la vista en markdown ──
    L = [
        "---", "tipo: vista", "generado_por: curiana_sim/juntar_toponimos.py", "editar_a_mano: no", "---", "",
        "# Topónimos por fuente — la campaña, junta",
        "",
        "> ⚠️ **Archivo generado. No se edita a mano.** Junta todos los topónimos",
        "> que el proyecto ha tocado, agrupados por obra (regla 8) y cruzados entre",
        "> sí. No es canon (eso es `2-lengua/toponimos.yaml`) ni propuesta de fusión:",
        "> es la mesa de trabajo de la campaña (SIGUIENTE_TANDA §B.5). Regenerar:",
        "> ```", "> python curiana_sim/juntar_toponimos.py", "> ```",
        "",
        f"<!--GENERADO--> Generado el **{date.today()}**. Marcas: ★ canon · ≡ Esteves · ◆ mapa de Miguel · ⌂ nodo.",
        "",
        f"**{resumen['formas_distintas']} formas distintas** en **{resumen['menciones']} menciones** de "
        f"**{resumen['fuentes']} fuentes**. En el canon: {resumen['en_canon']}. En el registro de nodos: "
        f"{resumen['en_nodos']}. Sin canon ni nodo (la cola pura): {resumen['sin_canon_ni_nodo']}.",
        "",
    ]
    if avisos:
        L += ["> " + a for a in avisos] + [""]
    L += ["## Resumen por fuente", "", "| Fuente | Qué es | Menciones | Formas | ★ canon | ≡ Esteves | ⌂ nodo |", "|---|---|---|---|---|---|---|"]
    for obra, v in por_fuente.items():
        ks = formas_de(obra)
        es = [entrada_por_clave[k] for k in ks if k in entrada_por_clave]
        L.append(f"| `{obra}`{'' if v['en_bibliografia'] else ' (sin ficha)'} | {v['descripcion']} | {v['menciones']} | {v['formas']} | "
                 f"{sum(1 for e in es if e['cruces']['en_canon'])} | {sum(1 for e in es if e['cruces']['en_esteves'])} | "
                 f"{sum(1 for e in es if e['cruces']['en_nodos'])} |")
    c = resumen["cruces"]
    L += ["", "## Los cruces que importan", ""]
    L += [f"- **Mapa de Miguel ∩ índice de Esteves ({len(c['mapa_de_miguel_en_esteves'])})**: {', '.join(c['mapa_de_miguel_en_esteves']) or '—'}. "
          f"Los que Esteves no tiene ({len(c['mapa_de_miguel_fuera_de_esteves'])}): {', '.join(c['mapa_de_miguel_fuera_de_esteves']) or '—'}."]
    L += [f"- **Castellanos 1589 ∩ Esteves ({len(c['castellanos_1589_en_esteves'])})**: {', '.join(c['castellanos_1589_en_esteves']) or '—'}."]
    L += [f"- **Castellanos 1589 ∩ Bastidas 1538 ({len(c['castellanos_1589_y_bastidas_1538'])})**: {', '.join(c['castellanos_1589_y_bastidas_1538']) or '—'}."]
    L += [f"- **Bastidas 1538 ∩ Esteves ({len(c['bastidas_1538_en_esteves'])})**: {', '.join(c['bastidas_1538_en_esteves']) or '—'}."]
    L += [f"- **Medina Colina ∩ Esteves ({len(c['medina_colina_en_esteves'])})**: {', '.join(c['medina_colina_en_esteves']) or '—'}; "
          f"en el canon ({len(c['medina_colina_en_canon'])}): {', '.join(c['medina_colina_en_canon']) or '—'}."]
    L += [f"- **En tres fuentes o más ({len(c['en_mas_de_dos_fuentes'])})**: {', '.join(c['en_mas_de_dos_fuentes']) or '—'}."]
    L += ["", "## Por fuente", ""]
    for obra, v in por_fuente.items():
        L += [f"### `{obra}` — {v['formas']} formas, {v['menciones']} menciones", "", f"{v['descripcion']}.", ""]
        ms = [m for m in menciones if m.fuente == obra]
        if len(ms) > 40:
            trozos = []
            for m in ms:
                e = entrada_por_clave.get(clave(m.forma))
                extra = f" ({m.dato})" if m.dato and m.tipo != "indice-abc" else ""
                trozos.append(f"{m.forma}{marcas(e) if e else ''}{extra}")
            L += [", ".join(trozos), ""]
        else:
            L += ["| Forma | Tipo | Lo que dice la fuente | Ref. | Cruces |", "|---|---|---|---|---|"]
            for m in ms:
                e = entrada_por_clave.get(clave(m.forma)) or (entrada_por_clave.get(clave(m.identificado_con)) if m.identificado_con else None)
                cr = []
                if e:
                    if e["cruces"]["en_canon"]:
                        cr.append("★ " + e["cruces"]["en_canon"])
                    if e["cruces"]["en_esteves"]:
                        cr.append("≡")
                    if e["cruces"]["en_mapa_miguel"]:
                        cr.append("◆")
                    if e["cruces"]["en_nodos"]:
                        cr.append("⌂ " + e["cruces"]["en_nodos"].split(" ")[0])
                forma = m.forma + (f" ~ {', '.join(m.variantes)}" if m.variantes else "") + (f" (= {m.identificado_con})" if m.identificado_con else "")
                L.append(f"| {forma} | {m.tipo} | {m.dato.replace('|', '/')} | {m.ref} | {' '.join(cr)} |")
            L.append("")
    L += ["## Índice de formas (todas, con sus fuentes)", "",
          "Una línea por forma; las variantes e identificaciones declaradas van juntas.", "",
          "| Forma | Variantes | Fuentes | ★ | ≡ | ◆ | ⌂ |", "|---|---|---|---|---|---|---|"]
    for e in entradas:
        cr = e["cruces"]
        L.append(f"| {e['forma']} | {', '.join(e['variantes'])} | {', '.join(e['fuentes'])} | {cr['en_canon'] or ''} | "
                 f"{'≡' if cr['en_esteves'] else ''} | {'◆' if cr['en_mapa_miguel'] else ''} | {cr['en_nodos'].split(' ')[0] if cr['en_nodos'] else ''} |")
    SALIDA_MD.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    return resumen


def main():
    menciones, entradas, avisos, ids_bib, indice = juntar()
    r = escribir(menciones, entradas, avisos, ids_bib, indice)
    print(f"✓ {SALIDA_YAML.relative_to(RAIZ)} y {SALIDA_MD.relative_to(RAIZ)}")
    print(f"  {r['formas_distintas']} formas · {r['menciones']} menciones · {r['fuentes']} fuentes · "
          f"{r['en_canon']} en canon · {r['en_nodos']} en nodos · {r['sin_canon_ni_nodo']} sin canon ni nodo")
    for obra, v in r["por_fuente"].items():
        print(f"  {obra:34} {v['formas']:4} formas  {v['menciones']:4} menciones")
    for a in avisos:
        print(" ", a)


if __name__ == "__main__":
    _forzar_utf8()
    main()
