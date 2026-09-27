#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Las ediciones del lexicón que pide el grupo 3 de #222, escritas para que las
aplique el frente del lexicón (este corte no toca curiana_lexicon.py ni los
lexicon_*.py generados).

DECISIÓN
    Miguel, 2026-09-24: «Ok a todo, que no quede ninguna tarea pendiente. Lo
    único pendiente es lo que tenga que ver con docker». Registro por entrada:
    6-fusion/decisiones_222_documentacion_2026-09-24.yaml.

QUÉ EMITE — 6-fusion/para_el_frente_del_lexicon_222_grupo3_2026-09-24.yaml
    - dp.3.03 + dp.3.15: la procedencia de las voces taínas desde la lista
      maestra de T10 (6-fusion/taino_lista_maestra_2026-09-22.yaml), clave por
      clave, con la línea exacta que se añade a `notas`. Las citas de Oviedo
      t. I llevan la verificación que les puso T1
      (6-fusion/taino_oviedo_valdes_1851.yaml): por T1 A1 sólo se cita lo
      verificado en imagen; lo que T1 dejó `ocr-sin-imagen` va aparte, en
      `pendiente_de_imagen` (dp.3.21: la verificación entra con dp.3.03).
    - dp.3.08: las citas de Goeje 1939 y el registro (hombres/mujeres) de las
      voces kalinago con apoyo, y la fusión de `kalinagu`/`kalínagu`
      (6-fusion/kalinago_goeje_1939.yaml §cruce_con_el_lexicon y §propuesta).
    - dp.3.07 P2, dp.3.10 y dp.3.23: ediciones escritas a mano abajo
      (constantes MANUALES), cada una con su fuente.

QUÉ MIDE ANTES DE PROPONER
    Lee el lexicón vivo (import de curiana_lexicon, sin escribir nada) para
    no proponer lo que ya está: si `notas` ya lleva la cita con página, lo
    dice (`ya_cita_en_prosa`). Corrige de paso una clave foránea: la lista
    maestra escribe `oviedo-valdes-1851`, que NO está en
    4-fuentes/bibliografia.yaml; la obra es `oviedo-y-valdes-1851`.

Uso:
    python 6-fusion/scripts/proponer_ediciones_lexicon_222_grupo3.py            # escribe
    python 6-fusion/scripts/proponer_ediciones_lexicon_222_grupo3.py --dry-run  # imprime
No toca el lexicón: lo importa para leerlo.
"""
import argparse
import collections
import io
import os
import re
import sys

import yaml

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))

SALIDA = os.path.join(R, "6-fusion", "para_el_frente_del_lexicon_222_grupo3_2026-09-24.yaml")
LISTA = os.path.join(R, "6-fusion", "taino_lista_maestra_2026-09-22.yaml")
T1 = os.path.join(R, "6-fusion", "taino_oviedo_valdes_1851.yaml")
KALINAGO = os.path.join(R, "6-fusion", "kalinago_goeje_1939.yaml")
BIBLIO = os.path.join(R, "4-fuentes", "bibliografia.yaml")

DECISION = "«Ok a todo, que no quede ninguna tarea pendiente. Lo único pendiente es lo que tenga que ver con docker» (Miguel, 2026-09-24)"
CORRIGE_CLAVE = {"oviedo-valdes-1851": "oviedo-y-valdes-1851"}

# dp.3.21 — lo que T1 dejó `ocr-sin-imagen`, mirado en la copia ÍNTEGRA el
# 2026-09-24 con las láminas de 6-fusion/scripts/recortes_oviedo_t1_integra.py
# (lectura por visión del escriba, página por página). Clave: (lema de la
# lista maestra, página impresa) → la forma que se ve.
VISTO_EN_LA_INTEGRA = {
    ("konoko", "143"): "conucos", ("konoko", "149"): "conucos", ("konoko", "163"): "conucos",
    ("konoko", "269"): "conuco", ("konoko", "370"): "conucos",
    ("batai", "163"): "batey", ("batai", "165"): "batey (título del cap. II)", ("batai", "471"): "batey",
    ("buhio", "163"): "buhio", ("buhio", "164"): "buhio", ("buhio", "165"): "buhios", ("buhio", "167"): "buhios",
    ("kanei", "164"): "caney", ("kanei", "165"): "caney",
    ("kanoa", "170"): "canoas (título del cap. IV)", ("kanoa", "171"): "canoas",
    ("pirakua", "170"): "piraguas (título del cap. IV)", ("pirakua", "344"): "piraguas",
    ("iuka", "264"): "yuca", ("iuka", "268"): "yuca (título del cap. II)", ("iuka", "269"): "yuca",
    ("iuka", "270"): "yuca", ("iuka", "271"): "yuca", ("iuka", "272"): "yuca",
    ("kakabi", "264"): "caçabi", ("kakabi", "268"): "caçabi (título del cap. II)",
    ("kakabi", "271"): "caçabi", ("kakabi", "272"): "caçabi",
    ("mahis", "264"): "mahiz", ("mahis", "265"): "mahiz", ("mahis", "266"): "mahizales",
    ("mahis", "267"): "mahizales, mahiz", ("mahis", "268"): "mahiz",
    ("batata", "273"): "batatas (título del cap. IV)", ("batata", "274"): "batatas", ("batata", "279"): "batatas",
    ("asi", "275"): "axi (título del cap. VII)", ("asi", "279"): "axi", ("asi", "308"): "axì",
    ("kuaiaba", "305"): "guayaba, guayabo", ("papaia", "323"): "papaya (título del cap. XXXIII)",
    ("manati", "433"): "manati (título del cap. IX)",
    ("naboria", "471"): "naboria", ("naboria", "472"): "naborias", ("naboria", "473"): "naboria",
    ("kuanin", "480"): "guanin", ("kuanin", "507"): "guanines", ("kuanin", "514"): "gua-nin",
}
NO_SE_CITA = {
    ("kemi", "50"): ("la p. 50 dice «quemis», «otros animales que llaman mohuy» — el roedor, no el cemí: la lista "
                     "maestra fundió `çemi` y `quemí` en el lema `kemi`"),
    ("kuaiaba", "530"): "«guayaba» no aparece en la copia íntegra (pp. 528-532, capa de texto): no se localiza",
}
# Citas de compiladores que la fusión `kemi` (çemi + quemí) arrastra a `cemi` y
# que son del animal (glosas «El güimo de Puerto Rico», «animalejos comibles»).
EXCLUIR_VIA = {("cemi", "coll-y-toste-1897", "210"), ("cemi", "coll-y-toste-1897", "250")}
CRONISTAS_EN_PROSA = ("Oviedo", "Las Casas", "Pané", "Mártir", "Anglería", "Colón", "Chanca", "Herrera")


def cargar(p):
    return yaml.safe_load(io.open(p, encoding="utf-8"))


def paginas(p):
    if p is None:
        return []
    return [str(x) for x in (p if isinstance(p, list) else [p])]


def fmt_pag(ps):
    ps = [x for x in ps if x]
    if not ps:
        return "s. p."
    if all(not x.lstrip("~")[:1].isdigit() for x in ps):   # «cap. XIX», «cap. proemio»
        return ", ".join(ps)

    def num(x):
        m = re.match(r"~?(\d+)", x)
        return int(m.group(1)) if m else 10 ** 6
    ps = sorted(ps, key=num)
    return ("p. " if len(ps) == 1 else "pp. ") + ", ".join(ps)


def claves_en(texto, claves):
    return [k for k in claves if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(k), str(texto))]


def indice_de_voces(voces, claves):
    """Replica el índice de consolidar_taino.py: una voz toca las claves del
    lexicón que su `en_el_lexicon` nombra."""
    ind = collections.defaultdict(list)
    for v in voces:
        for c in (v.get("en_el_lexicon") or []):
            piezas = claves_en(c, claves)
            if not piezas:
                piezas = [re.split(r"\s+[—-]\s+|\s*\(", p)[0].strip()
                          for p in re.split(r"\s*[·,]\s*", str(c))]
            for p in piezas:
                if p:
                    ind[p].append(v)
    return ind


def ya_cita(notas):
    return any(c in notas for c in CRONISTAS_EN_PROSA) and bool(re.search(r"\bpp?\. ?\d", notas))


def dp303(CL, obras):
    lm = cargar(LISTA)
    det = {d["clave"]: d for d in lm["las_claves_tainas_del_lexicon"]["detalle"]}
    claves = sorted(det)
    ind = indice_de_voces(lm["voces"], claves)

    t1 = cargar(T1)
    t1_ent = []
    for sec in ("costa_de_venezuela", "la_espanola", "otras_islas", "no_taino"):
        t1_ent += t1.get(sec) or []
    t1_por_clave = collections.defaultdict(list)
    for e in t1_ent:
        for k in claves_en(e.get("en_el_lexicon") or "", claves):
            t1_por_clave[k].append(e)

    salida, pendientes = [], []
    for k in claves:
        d = det[k]
        e = CL.VOCABULARIO_BASE.get(k, {})
        notas = e.get("notas") or ""
        unicas = {}
        for v in ind.get(k, []):                         # una voz puede nombrar la clave dos veces
            unicas.setdefault(v["lema"], v)
        voces = sorted(unicas.values(), key=lambda v: -v["atestaciones_independientes"])
        reg = {"clave": k, "fuente_en_el_lexicon": e.get("fuente"),
               "clase_en_la_lista_maestra": d["clase"],
               "cronistas_independientes": d.get("cronistas") or []}
        if not voces:
            reg["edicion"] = ("ninguna: la lista maestra no recoge la voz (sin-voz-en-la-lista). "
                              + ("Sus `notas` ya citan con página." if ya_cita(notas) else
                                 "Queda como está; si no cita a nadie, `deuda: sin-procedencia` es otra decisión."))
            salida.append(reg)
            continue

        prim, via = collections.OrderedDict(), collections.OrderedDict()
        pend, integra, excluidas = [], [], []
        verif_t1 = {}
        for t in t1_por_clave.get(k, []):
            for p in paginas(t.get("pagina_impresa")):
                verif_t1[p] = (t.get("verificacion"), t.get("forma_fuente"), t.get("libro"), t.get("capitulo"))
        for v in voces:
            for c in v["cadena_de_custodia"]:
                obra = CORRIGE_CLAVE.get(c["obra"], c["obra"])
                assert obra in obras, f"{k}: la obra {obra} no está en la bibliografía"
                ps = paginas(c.get("pagina"))
                if c["tipo"] == "primaria":
                    if obra == "oviedo-y-valdes-1851":
                        buenas = []
                        for p in ps:
                            ver = verif_t1.get(p, (None,))[0]
                            if (v["lema"], p) in NO_SE_CITA:
                                excluidas.append({"obra": obra, "pagina": p, "forma": v["lema"],
                                                  "por_que": NO_SE_CITA[(v["lema"], p)]})
                            elif ver in ("imagen", "parcial"):
                                buenas.append(p if ver == "imagen" else p + " (verificación parcial)")
                            elif (v["lema"], p) in VISTO_EN_LA_INTEGRA:
                                buenas.append(p)
                                integra.append({"pagina": p, "forma": v["lema"],
                                                "se_ve": VISTO_EN_LA_INTEGRA[(v["lema"], p)]})
                            else:
                                pend.append({"obra": obra, "pagina": p, "forma": v["lema"],
                                             "verificacion_en_T1": ver or "no está en T1"})
                        if buenas:
                            prim.setdefault(obra, []).extend(x for x in buenas if x not in prim.get(obra, []))
                    else:
                        prim.setdefault(obra, []).extend(x for x in ps if x not in prim.get(obra, []))
                else:
                    cron = ", ".join(c.get("cronista_que_declara") or []) or "sin cronista declarado"
                    lst = via.setdefault(obra, [])
                    for p in ps:
                        if (k, obra, p) in EXCLUIR_VIA:
                            excluidas.append({"obra": obra, "pagina": p, "forma": v["lema"],
                                              "por_que": "glosa del roedor quemí, no del cemí (fusión de lema en la lista maestra)"})
                            continue
                        if (p, cron) not in lst:
                            lst.append((p, cron))

        partes = []
        # los «lemas» de más de 14 letras son frases o listas que el OCR pegó
        # (diosnaboriadaka, nombresdearboles…): sus citas valen, su nombre no
        cortos = sorted({v["lema"] for v in voces if len(v["lema"]) <= 14})
        largos = len({v["lema"] for v in voces}) - len(cortos)
        lema = ", ".join(cortos) + (f" (+ {largos} registro(s) de frase o lista)" if largos else "")
        cr = reg["cronistas_independientes"]
        cab = (f"PROCEDENCIA (dp.3.03 de #222, 2026-09-24, desde la lista maestra de T10: "
               f"6-fusion/taino_lista_maestra_2026-09-22.yaml, voz `{lema}`): clase {d['clase']}")
        cab += (f", {len(cr)} cronista(s) independiente(s): {', '.join(cr)}" if cr else ", ningún cronista del XVI")
        partes.append(cab)
        if prim:
            trozos = []
            for o, ps in prim.items():
                t = f"{o} {fmt_pag(ps)}"
                if o == "oviedo-y-valdes-1851":
                    ig = sorted({x["pagina"] for x in integra}, key=int)
                    t += (" (t. I, verificado en imagen"
                          + (f"; {fmt_pag(ig)} en la copia íntegra, 2026-09-24, dp.3.21" if ig else " por T1")
                          + ")")
                trozos.append(t)
            partes.append("primarias: " + " · ".join(trozos))
        if via:
            trozos = []
            for o, lst in via.items():
                pags = [p for p, _ in lst][:4]
                crons = sorted({c for _, c in lst})
                trozos.append(f"{o} {fmt_pag(pags)}{' …' if len(lst) > 4 else ''} (cita: {'; '.join(crons)})")
            partes.append("vía compiladores (no son atestaciones aparte, skill minar-fuente §8): " + " · ".join(trozos))
        sac = [v.get("sacada_del_taino") for v in voces if v.get("sacada_del_taino")]
        if sac:
            partes.append(f"⚠️ alguna fuente la saca del taíno ({'; '.join(map(str, sac))}): eso es la opción A de T10, no se decide aquí")
        if pend:
            partes.append("Oviedo t. I sin verificar en imagen: " + ", ".join(f"p. {x['pagina']}" for x in pend)
                          + " (pendiente de imagen: no se cita hasta verlo)")
        reg["ya_cita_en_prosa"] = ya_cita(notas)
        reg["edicion"] = {
            "archivo": "curiana_sim/curiana_lexicon.py",
            "dict": "VOCABULARIO_BASE",
            "clave": k,
            "campo": "notas",
            "operacion": ("añadir al FINAL de `notas`, precedido de « · »" if notas
                          else "crear `notas` con este texto (hoy la entrada no tiene)"),
            "texto": ". ".join(partes) + ".",
        }
        if pend:
            reg["pendiente_de_imagen"] = pend
            pendientes += [dict(clave=k, **x) for x in pend]
        if integra:
            reg["verificado_en_la_integra"] = integra
        if excluidas:
            reg["no_se_cita"] = excluidas
        salida.append(reg)
    return salida, pendientes


def dp308(CL, obras):
    kal = cargar(KALINAGO)
    assert "goeje-1939" in obras
    registro = {"kati-kalinago": "mujeres (hombres: nonum)", "marisi-kalinago": "mujeres (hombres: aoasi)",
                "hiñaru": "mujeres", "barana": "hombres (mujeres: balaua ~ arawak bara)",
                "kalinagu": "hombres (mujeres: Kaliponam)", "kalínagu": "hombres (mujeres: Kaliponam)"}
    out = []
    for f in kal["cruce_con_el_lexicon"]:
        if f["veredicto"] != "apoyo":
            continue
        k = f["clave"]
        e = CL.VOCABULARIO_BASE.get(k)
        notas = (e or {}).get("notas") or ""
        texto = (f"PROCEDENCIA (dp.3.08 de #222, 2026-09-24): goeje-1939 p. {f['pagina_impresa']}, "
                 f"verificado en imagen (6-fusion/kalinago_goeje_1939.yaml §cruce_con_el_lexicon). "
                 f"Propuesta de cita de M5: «{f['propuesta_de_cita']}»")
        if k in registro:
            texto += f". REGISTRO: habla de {registro[k]}, según Goeje; el lexicón no lo decía"
        out.append({
            "clave": k,
            "existe_en_el_lexicon": e is not None,
            "ya_cita_goeje": "Goeje" in notas or "goeje-1939" in notas,
            "edicion": {"archivo": "curiana_sim/curiana_lexicon.py", "dict": "VOCABULARIO_BASE",
                        "clave": k, "campo": "notas",
                        "operacion": "añadir al FINAL de `notas`, precedido de « · »",
                        "texto": texto + "."},
        })
    fusion = {
        "que": "fundir `kalinagu` y `kalínagu` (k5 de M5): son dos claves para la misma línea de Goeje p. 43",
        "edicion": (
            "Propuesta: se queda `kalinagu` (Goeje imprime la forma sin tilde, «Kalinago», p. 43; la elección es "
            "del frente, que mide antes cuál de las dos cita el resto del repo) y "
            "`kalínagu` pasa a FUERA_DEL_HABLA con su entrada entera y esta huella al principio de `notas`: "
            "«Fundida en `kalinagu` (dp.3.08 de #222, 2026-09-24): la misma voz de Goeje 1939 p. 43.» "
            "La glosa de `kalinagu` gana, al final de sus `notas`: «Variante con tilde `kalínagu` archivada "
            "(dp.3.08); su glosa decía 'Caribe, autónimo del pueblo Caribe insular'.»"),
        "medir_antes": ("¿alguna de las dos está entre las candidatas de [Voces de fuera] o en sitios/clima "
                        "(6-fusion/scripts/verificar_sitios_era2.py)? Si lo está, archivarla mueve el prompt: "
                        "se mide antes, como en cualquier archivo (CLAUDE.md, «El mundo nombra voces del lexicón»)."),
        "estado_actual": {k: (CL.VOCABULARIO_BASE.get(k) or {}).get("sig") for k in ("kalinagu", "kalínagu")},
    }
    return out, fusion


MANUALES = {
    "dp.3.07_P2_gumilla_en_neira": {
        "decision": "P2 A: las voces achaguas de Gumilla que corroboran a Neira y Ribero van como notas de sus entradas; «se corrige el YAML de Neira y se regenera»",
        "por_que_es_del_frente": "el generador de curiana_sim/lexicon_achagua.py (6-fusion/scripts/generar_lexicon_achagua.py) lee `nota` del `vocabulario`: tocar el YAML obliga a regenerar el módulo, y regenerarlo mueve el score (CLAUDE.md, «generados Y se importan»)",
        "archivo": "6-fusion/achagua_neira_ribero_1762.yaml",
        "como": "en cada entrada de `vocabulario` localizada por (castellano, pliego, lado), añadir al final de `nota` (o crear `nota`) el texto; después `python 6-fusion/scripts/generar_lexicon_achagua.py`, comprobar que sólo cambian esas `notas` del módulo, y `python 6-fusion/scripts/ensamblar_achagua_neira_ribero.py --check`",
        "fuente": "6-fusion/gumilla_1791_2026-09-23.yaml §achagua.voces (verificadas en imagen donde lo dice)",
        "aviso_de_independencia": "Gumilla y Neira salen del mismo medio jesuita: «segunda mano del mismo taller», no dos atestaciones ciegas. Por eso va en notas y no cambia ninguna capa",
        "ediciones": [
            {"entrada": {"castellano": "Linage de tigre", "pliego": 72, "lado": "der"},
             "texto": "Gumilla 1791 t. I p. 112 da «Chavi» = Tigre (misma voz; Gumilla y Neira, mismo medio jesuita; dp.3.07 de #222)"},
            {"entrada": {"castellano": "Vibrar la lanza", "pliego": 97, "lado": "der"},
             "texto": "Gumilla 1791 t. I p. 112 da «Chavina» = Lanza (misma voz; dp.3.07 de #222)"},
            {"entrada": {"castellano": "Caribe", "pliego": 46, "lado": "izq"},
             "texto": "Gumilla 1791 t. I p. 112 da «Chavinavi» = Caribe, con dos etimologías achaguas («oriundo de Tigre» / «hijos de Tigres con Lanzas»); coincide con el plural Chabinabi de aquí (dp.3.07 de #222)"},
            {"entrada": {"castellano": "Arbol", "pliego": 37, "lado": "der"},
             "texto": "Gumilla 1791 t. I p. 114 (verificado en imagen) da «Aycubaverrenais», los que «se fingen hijos de los Troncos»: aycuba-berrenai 'linaje del árbol', la misma formación que Chabiberraenay (pl. 72 der.). Apoyo a los linajes con nombre (dp.3.07 de #222)"},
            {"entrada": {"castellano": "Agua", "pliego": 32, "lado": "izq"},
             "texto": "Gumilla 1791 t. I p. 114 (verificado en imagen) da «Univerrenais», los que «idean su estirpe de los rios»: uni-berrenai 'linaje del agua'. Tercer testigo de que `uni` es agua (dp.3.07 de #222)"},
            {"entrada": {"castellano": "Demonio, Diablo", "pliego": 53, "lado": "izq"},
             "texto": "Gumilla 1791 t. II pp. 23-24: «Los Indios Achaguas le llaman Tanasimi» — idéntica (dp.3.07 de #222)"},
            {"entrada": {"castellano": "Cinco", "pliego": 48, "lado": "izq"},
             "texto": "Gumilla 1791 t. II p. 283 (verificado en imagen) da «Abacáje» = cinco, «los dedos de la mano» (dp.3.07 de #222)"},
            {"entrada": {"castellano": "Diez", "pliego": 55, "lado": "der"},
             "texto": "Gumilla 1791 t. II p. 283 (verificado en imagen) da «Juchamacáje» = diez, «los dedos de ambas manos»: la forma analítica de esta (dp.3.07 de #222)"},
            {"entrada": {"castellano": "Veinte", "pliego": 96, "lado": "der"},
             "texto": "Gumilla 1791 t. II p. 283 da «Abacaytacáy» = veinte, «los dedos de piés y manos» (dp.3.07 de #222)"},
            {"entrada": {"castellano": "Cuarenta", "pliego": 51, "lado": "der"},
             "texto": "Gumilla 1791 t. II p. 283 da «Juchámatatacáy» = cuarenta, «los dedos de dos hombres»: confirma la base veinte, tacay = los dedos de un hombre (dp.3.07 de #222)"},
            {"entrada": {"castellano": "Quarenta", "pliego": 87, "lado": "izq"},
             "texto": "Gumilla 1791 t. II p. 283 da «Juchámatatacáy» = cuarenta (dp.3.07 de #222)"},
        ],
        "no_entran": "Manóa (difiere en la glosa: laguna / mar), la frase de «matata» (aprisa / poco a poco), catena y arabata (no están en Neira): P2 A dice «las que corroboran»",
    },
    "dp.3.10_togogo_tokoko_chogogo": {
        "decision": "F2.4 A, F2.6 A y la nota de `chogogo` con lo de Goeje (M5 §7)",
        "fuente": "6-fusion/fauna_paraguana_aves_2026-09-22.yaml (ave-040, ave-041; FA2, #205) y 6-fusion/issues-pendientes/vocabularios-antillanos-2-2026-09-22.md §7 (M5, #219)",
        "ediciones": [
            {"archivo": "curiana_sim/curiana_lexicon.py", "dict": "VOCABULARIO_BASE", "clave": "chogogo", "campo": "notas",
             "operacion": "añadir al FINAL de `notas`, precedido de « · »",
             "texto": ("VARIANTE DE TIERRA FIRME (dp.3.10 F2.4 A de #222, 2026-09-24): «togogo», con t- donde las islas tienen ch-, "
                       "en dos fuentes independientes del s. XX verificadas en imagen: Alvarado 1921 p. 292 («¿Es el TOGOGO de Coro?») "
                       "y Esteves 1989 p. 134 (lema TOGOCO, «Togogo: ave ansérida»). Si es la misma voz, chogogo deja de ser sólo insular. "
                       "Y Goeje 1939 p. 60 la da como caribe: «flamant tuguku, K tokoko, dialecte de Bonaire chogogo» (M5 §7): si Goeje "
                       "tiene razón, el flamenco de las islas lleva nombre caribe. No cambia la capa: es evidencia en conflicto, escrita")},
            {"archivo": "curiana_sim/curiana_lexicon.py", "dict": "VOCABULARIO_BASE", "clave": "tokoko", "campo": "notas",
             "operacion": "añadir al FINAL de `notas`, precedido de « · »",
             "texto": ("PROCEDENCIA COMPARADA (dp.3.10 F2.6 A de #222, 2026-09-24): alvarado-1921 p. 292 da la cadena gal. tokoka, "
                       "car. tokóko, ar. tukkuku (verificado en imagen, FA2 ave-041). Es comparanda caribe/arahuaca: la entrada NO sube "
                       "de capa, sigue caquetío-hipotético (acuñación de la simulación)")},
        ],
        "sin_edicion": "`togogo` no es clave del lexicón y no se crea: F2.4 A la registra en `notas` de `chogogo`",
    },
    "dp.3.23_taino_hipotetico_json": {
        "decision": "moverlo a 6-fusion/ con su fecha, no borrarlo",
        "por_que_es_del_frente": "vive en curiana_sim/ y dos scripts de campaña lo leen por esa ruta: la orden del corte es no moverlo si algo lo lee",
        "lectores": [
            "6-fusion/scripts/cruce_taino_caquetio.py — JSON_TAINO_HIP = os.path.join(R, \"curiana_sim\", \"taino_hipotetico.json\")",
            "6-fusion/scripts/medir_taino_inventario.py — p = os.path.join(SIM, \"taino_hipotetico.json\")",
        ],
        "ediciones": [
            "git mv curiana_sim/taino_hipotetico.json 6-fusion/taino_hipotetico_2026-06-21.json   # la fecha es la de su único commit, 573719a",
            "6-fusion/scripts/cruce_taino_caquetio.py: JSON_TAINO_HIP = os.path.join(R, \"6-fusion\", \"taino_hipotetico_2026-06-21.json\")",
            "6-fusion/scripts/medir_taino_inventario.py: p = os.path.join(RAIZ_DE_6_FUSION, \"taino_hipotetico_2026-06-21.json\") — con la variable de ruta que ese script ya use para 6-fusion/",
            "una línea en el JSON no se puede poner (no admite comentarios): la huella va en el mensaje del commit y en 6-fusion/decisiones_222_documentacion_2026-09-24.yaml",
        ],
        "medir_despues": "los dos scripts corren igual que antes (--check o su salida por defecto) y `git grep taino_hipotetico` ya no apunta a curiana_sim/",
    },
}


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    import curiana_lexicon as CL  # sólo lectura
    obras = {o["id"] for o in cargar(BIBLIO)["obras"]}

    taino, pendientes = dp303(CL, obras)
    kal, fusion = dp308(CL, obras)

    # cada localizador de dp.3.07 tiene que existir en el YAML de Neira
    neira = cargar(os.path.join(R, "6-fusion", "achagua_neira_ribero_1762.yaml"))["vocabulario"]
    for ed in MANUALES["dp.3.07_P2_gumilla_en_neira"]["ediciones"]:
        loc = ed["entrada"]
        n = sum(1 for e in neira if e.get("castellano") == loc["castellano"]
                and e.get("pliego") == loc["pliego"] and e.get("lado") == loc["lado"])
        assert n == 1, f"dp.3.07: {loc} aparece {n} veces en el vocabulario de Neira"

    con_edicion = [r for r in taino if isinstance(r.get("edicion"), dict)]
    doc = {
        "meta": {
            "fecha": "2026-09-24",
            "decision": DECISION,
            "registro": "6-fusion/decisiones_222_documentacion_2026-09-24.yaml",
            "generado_por": "6-fusion/scripts/proponer_ediciones_lexicon_222_grupo3.py (no se edita a mano: se corrige el script y se regenera)",
            "que_es": ("las ediciones del grupo 3 de #222 que tocan curiana_sim/curiana_lexicon.py, un lexicon_*.py "
                       "generado o su regeneración. Este corte no toca esos archivos; las aplica el frente del lexicón"),
            "como_aplicar": [
                "cada edición dice archivo, dict, clave, campo, operación y el texto exacto",
                "nunca cambian forma, `sig`, `cat` ni `fuente`: son `notas` (no llegan al prompt: verificado en db.5 y dc.1)",
                "comprobar después: las mismas claves activas antes y después, sólo esas `notas` cambiadas (skill fusionar-propuesta §3)",
                "guardianes.py en verde y, si se archiva algo (dp.3.08 k5), verificar_sitios_era2.py",
            ],
            "clave_corregida": ("la lista maestra de T10 escribe `oviedo-valdes-1851`, que NO está en 4-fuentes/bibliografia.yaml "
                                "(regla 8); aquí se escribe `oviedo-y-valdes-1851`. El generador de la lista "
                                "(6-fusion/scripts/consolidar_taino.py, PRIMARIAS) sigue con la clave vieja: no se toca en este corte"),
            "cifras": {
                "dp303_claves_tainas": len(taino),
                "dp303_con_edicion": len(con_edicion),
                "dp303_sin_voz_en_la_lista": len(taino) - len(con_edicion),
                "dp303_ya_citan_en_prosa": sum(1 for r in con_edicion if r.get("ya_cita_en_prosa")),
                "dp303_citas_de_oviedo_pendientes_de_imagen": len(pendientes),
                "dp321_paginas_vistas_en_la_integra": len(VISTO_EN_LA_INTEGRA),
                "dp321_paginas_que_no_se_citan": len(NO_SE_CITA),
                "dp303_claves_con_alguna_cita_excluida": sum(1 for r in taino if r.get("no_se_cita")),
                "dp308_voces_kalinago_con_apoyo": len(kal),
                "dp308_ya_citan_goeje": sum(1 for r in kal if r["ya_cita_goeje"]),
            },
        },
        "dp.3.03_y_dp.3.15_procedencia_de_las_voces_tainas": {
            "decision": "T10 C (la del recopilador): una sola pasada con la lista maestra; T3 A3 NO (movería el prompt). dp.3.15: `areito` entra en esta pasada con la cita de Oviedo que T1 verificó en imagen",
            "claves": taino,
        },
        "dp.3.21_pendientes_de_imagen": {
            "pares_mirados_en_la_integra": (
                [{"forma": f, "pagina": p, "se_ve": s} for (f, p), s in sorted(VISTO_EN_LA_INTEGRA.items(), key=lambda x: (int(x[0][1]), x[0][0]))]
                + [{"forma": f, "pagina": p, "no_se_cita": s} for (f, p), s in sorted(NO_SE_CITA.items())]),
            "que_es": ("las citas de Oviedo t. I que la pasada propondría y T1 no vio en imagen (verificación "
                       "`ocr-sin-imagen`): por T1 A1 no se citan hasta verlas. El 2026-09-24 se miraron en la copia "
                       "íntegra (`pares_mirados_en_la_integra`: lo que se ve, o por qué no se cita); `citas` es lo que "
                       "quedó sin mirar. La copia íntegra está en el repo "
                       "(fuentes_caquetios/Oviedo_Valdes_1851_Historia_General_Indias_vol1_completo.pdf): impresa = pdf − 120 "
                       "contando las páginas desde 1 (M3 escribe «− 119» porque cuenta desde 0; comprobado en las cabeceras "
                       "de las impresas 143, 265, 471 y 530). Recortes para mirarlas: 6-fusion/scripts/recortes_oviedo_t1_integra.py"),
            "citas": pendientes,
        },
        "dp.3.08_kalinago_de_goeje": {
            "decision": "A: citas (goeje-1939 con página) y registro en `notas` de las voces con apoyo; fundir `kalinagu`/`kalínagu`",
            "voces": kal,
            "fusion_kalinagu": fusion,
            "no_entra": "k3 (la glosa de `hiñaru` 'persona' → 'mujer') y k4 (las ocho sin apoyo) son la opción B de M5, no la A",
        },
    }
    doc.update(MANUALES)

    texto = ("# " + "=" * 70 + "\n"
             "# GENERADO por 6-fusion/scripts/proponer_ediciones_lexicon_222_grupo3.py — no se edita a mano.\n"
             "# Las ediciones del lexicón del grupo 3 de #222, para el frente del lexicón.\n"
             "# " + "=" * 70 + "\n")
    class SinAlias(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True
    texto += yaml.dump(doc, Dumper=SinAlias, allow_unicode=True, sort_keys=False, width=110)
    yaml.safe_load(texto)
    c = doc["meta"]["cifras"]
    print("\n".join(f"  {k}: {v}" for k, v in c.items()))
    if a.dry_run:
        print("--dry-run: no se escribió nada")
        return 0
    io.open(SALIDA, "w", encoding="utf-8", newline="\n").write(texto)
    print(f"escrito {os.path.relpath(SALIDA, R)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
