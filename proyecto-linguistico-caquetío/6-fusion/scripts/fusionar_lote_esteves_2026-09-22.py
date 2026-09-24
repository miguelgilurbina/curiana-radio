# -*- coding: utf-8 -*-
"""Lleva al canon de topónimos el lote de Esteves 1989 (Parte I, Paraguaná),
leído entero por la parcela M6 de la tercera minería (#216), por TANDAS.

La decisión (dp.2.08 de #222), registrada en
6-fusion/decisiones_222_mundo_2026-09-24.yaml:

    «Ok a todo, que no quede ninguna tarea pendiente. Lo único pendiente es
    lo que tenga que ver con docker» (Miguel, 2026-09-24)

sobre la recomendación «2-A, por tandas»: primero las A y B más las
correcciones del §2 que tocan entradas del canon; después las C; después los
descartes. Los niveles del lote ya aplican la regla (E) = Esteves (cc.4 → 1-A):
una voz cuya única cita es Zavala (E) no cuenta como segunda fuente.

    python 6-fusion/scripts/fusionar_lote_esteves_2026-09-22.py --tanda 1 [--dry-run]
    python 6-fusion/scripts/fusionar_lote_esteves_2026-09-22.py --tanda 2 [--dry-run]
    python 6-fusion/scripts/fusionar_lote_esteves_2026-09-22.py --tanda 3 [--dry-run]

Qué hace cada tanda (siempre sobre curiana_sim/lexicon_toponimos.py; el canon
2-lengua/toponimos.yaml se REGENERA después con migrar_toponimos.py, nunca a
mano — la trampa de CLAUDE.md):

  1. Las entradas A → al final de NIVEL_A y las B → al final de NIVEL_B, con
     `id` explícito, el siguiente libre. Y dos correcciones del §2 que son
     mudanza de nivel: acaboa (toponimo-153) y aguaque (toponimo-154) SÍ
     tienen etimología en Esteves (pp. 12 y 14) y pasan del grupo de
     descartes del dictado a NIVEL_C con su id de siempre.
  2. Las C → al final de NIVEL_C (menos acaboa y aguaque, ya hechas).
  3. Los tres grupos de descartes → tres grupos nuevos al final de DESCARTES,
     con `ids`, `paginas` y, por forma, `observaciones`, `origenes`,
     `estratos` y `lecturas` (el migrador los emite desde el 2026-09-24).

Y en las tres: los nombres procesados pasan de `por_procesar` a
`ya_registrados` en 6-fusion/toponimos_esteves_indice.yaml, y el `meta` se
recuenta.

Conversión de una entrada del lote a una del módulo: `referente`,
`censo_1881`, `formas_antiguas`, `voces`, `formantes` y `verificado` viajan
como campos propios (skill campana-toponimos §2: «cada cosa en su campo»);
`filiacion_declarada` pasa a `filiacion_segun_autor` (un estrato atribuido es
lectura del autor, §5); `cabecera` va a la observación. Dos tipos de lectura
del lote no están en el vocabulario cerrado de compilar_lengua y se traducen:
`segmentacion-de-autor` → `etimologia-analitica` y `hipotesis-de-autor` →
`hipotesis`; y el eje `filiacion` → `significado`. Las lecturas llevan la fecha del lote (2026-09-23) y, si son de
Esteves o recogidas por él, su procedencia con la página.

Lo que NO hace, y por qué:
  - Las correcciones del §2 que tocan el lexicón (las notas de `kumarawa` y
    de `urupagua` en curiana_lexicon.py) no son de este frente.
  - Carirubana, Coabana y curarí se corrigen a mano en el mismo commit de la
    tanda 1 (una línea cada una), no aquí.
  - Las secciones `fauna` y `flora` del lote no son topónimos: siguen en la
    propuesta.

Idempotente por tanda: si el módulo ya lleva la marca de la tanda, no hace
nada. Imprime entrada por entrada lo que hace y lo que salta, con la razón.
"""
import argparse
import io
import json
import os
import re
import sys
import unicodedata

import yaml

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODULO = os.path.join(R, "curiana_sim", "lexicon_toponimos.py")
LOTE = os.path.join(R, "6-fusion", "toponimos_esteves_lote_2026-09-22.yaml")
INDICE = os.path.join(R, "6-fusion", "toponimos_esteves_indice.yaml")
FECHA_LOTE = "2026-09-23"
DECISION = "dp.2.08 de #222, 2026-09-24"
MARCA = "# ── Lote de Esteves 2026-09-22 (M6, #216), tanda {n} — dp.2.08 de #222 (2026-09-24) ──"
TIPOS = {"segmentacion-de-autor": "etimologia-analitica",
         "hipotesis-de-autor": "hipotesis"}
# `eje` también es cerrado (significado · referente · ambos). La lectura de
# Iticuna habla de la filiación del nombre (una etimología maya), que es un
# eje de significado: se traduce y se declara en la propia lectura.
EJES = {"filiacion": "significado"}
MUDANZAS = {"acaboa": "toponimo-153", "aguaque": "toponimo-154"}
GRUPO_DICTADO = "Dictado de Miguel 2026-09-10: Esteves los registra sin glosarlos"


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn")


def leer(ruta):
    t = io.open(ruta, encoding="utf-8", newline="").read()
    return t.replace("\r\n", "\n"), ("\r\n" in t)


def escribir(ruta, t, crlf):
    io.open(ruta, "w", encoding="utf-8", newline="").write(
        t.replace("\n", "\r\n") if crlf else t)


def lit(v):
    """Un literal de Python con comillas dobles (el estilo del módulo)."""
    def revisar(x):
        if isinstance(x, (bool, type(None))):
            raise ValueError(f"valor no representable como literal: {x!r}")
        if isinstance(x, dict):
            for y in x.values():
                revisar(y)
        if isinstance(x, list):
            for y in x:
                revisar(y)
    revisar(v)
    return json.dumps(v, ensure_ascii=False)


def siguiente_id(texto):
    return max(int(n) for n in re.findall(r"toponimo-(\d{3})", texto)) + 1


def lecturas_de(e):
    salida = []
    for lec in e.get("lecturas") or []:
        lec = dict(lec)
        lec["tipo"] = TIPOS.get(lec.get("tipo"), lec.get("tipo"))
        if lec.get("eje") in EJES:
            lec["lectura"] = f"{lec['lectura']} (en el lote, eje «{lec['eje']}»)"
            lec["eje"] = EJES[lec["eje"]]
        lec.setdefault("fecha", FECHA_LOTE)
        if "esteves" in str(lec.get("quien", "")).lower() and "procedencia" not in lec:
            lec["procedencia"] = {"obra": "esteves-1989", "pagina": e["pagina"]}
        salida.append(lec)
    return salida


def entrada_del_modulo(e, rid):
    d = {"id": rid, "clase": "topónimo", "fuente": "esteves-1989",
         "pagina": e["pagina"]}
    for campo in ("glosa_fuente", "segmentacion", "voces", "formantes",
                  "razon", "referente", "censo_1881", "formas_antiguas"):
        if e.get(campo):
            d[campo] = e[campo]
    if e.get("filiacion_declarada"):
        d["filiacion_segun_autor"] = e["filiacion_declarada"]
    obs = [e["observacion"]] if e.get("observacion") else []
    if e.get("cabecera") and sin_tildes(e["cabecera"]) != sin_tildes(e["forma"]):
        obs.append(f"Cabecera impresa: {e['cabecera']}.")
    if e.get("posible_canon"):
        obs.append(f"El fusionador ({DECISION}) la registra como entrada propia, con "
                   f"la página de Esteves; la identidad con {e['posible_canon']} queda "
                   "como lectura `hipotesis` allí (dp.2.09, P3 A), sin fundirlas.")
    if obs:
        d["observacion"] = " ".join(obs)
    lec = lecturas_de(e)
    if lec:
        d["lecturas"] = lec
    d["verificado"] = str(e.get("verificado"))
    return d


def bloque(entradas, marca):
    L = [f"    {marca}"]
    for forma, d in entradas:
        L.append(f"    {lit(forma)}: {{")
        for k, v in d.items():
            L.append(f"        {lit(k)}: {lit(v)},")
        L.append("    },")
    return "\n".join(L) + "\n"


def insertar_al_final(texto, cabecera_dict, bloque_txt):
    """Inserta antes de la llave que cierra `CABECERA = {` (la primera `}` en
    columna 0 detrás de ella)."""
    ini = texto.index(cabecera_dict)
    fin = texto.index("\n}\n", ini)
    return texto[:fin + 1] + bloque_txt + texto[fin + 1:]


def quitar_del_grupo_dictado(texto, forma):
    """Saca `forma` del grupo de descartes del dictado: su entrada en `ids` y
    su string en `formas`. Tiene id explícito, así que el contador no se
    mueve."""
    ini = texto.index(f'    "{GRUPO_DICTADO}": {{')
    fin = texto.index("\n    },\n", ini)
    g = texto[ini:fin]
    g2 = re.sub(rf'"{forma}": "toponimo-\d{{3}}",\s*', "", g, count=1)
    # la forma, entera, en la lista (puede ocupar varias líneas)
    m = re.search(rf'\n            "{forma} \(.*?\)",', g2, re.S)
    if not m:
        raise SystemExit(f"no encuentro «{forma}» en el grupo del dictado")
    g2 = g2[:m.start()] + g2[m.end():]
    return texto[:ini] + g2 + texto[fin:]


def actualizar_indice(procesados, tanda, cabecera_de):
    """procesados: [(forma_del_lote, id)]. Mueve cada nombre de por_procesar a
    ya_registrados y recuenta el meta."""
    t, crlf = leer(INDICE)
    ini_pp = t.index("\npor_procesar:\n")
    cabeza, cola = t[:ini_pp], t[ini_pp:]
    nuevos, faltan = [], []
    for forma, rid in procesados:
        objetivo = sin_tildes(cabecera_de.get(forma, forma))
        pat = re.compile(r"\n  - \{forma: ([^,}]+), propuesta: lote-2026-09-22\}[^\n]*")
        hallado = None
        for m in pat.finditer(cola):
            if sin_tildes(m.group(1)) in (objetivo, sin_tildes(forma)):
                hallado = m
                break
        if not hallado:
            faltan.append(forma)
            continue
        nombre = hallado.group(1)
        cola = cola[:hallado.start()] + cola[hallado.end():]
        nuevos.append(f"  - {{forma: {nombre}, canon: {rid}, lote: 2026-09-22-tanda-{tanda}}}")
    cabeza = cabeza.rstrip("\n") + "\n" + "\n".join(nuevos) + "\n"
    t = cabeza + cola
    doc = yaml.safe_load(t)
    ya, pp = len(doc["ya_registrados"]), len(doc["por_procesar"] or [])
    t = re.sub(r"(\n  ya_en_canon: )\d+", rf"\g<1>{ya}", t, count=1)
    t = re.sub(r"(\n  por_procesar: )\d+", rf"\g<1>{pp}", t, count=1)
    yaml.safe_load(t)
    return t, crlf, nuevos, faltan, ya, pp


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--tanda", type=int, choices=(1, 2, 3), required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    lote = yaml.safe_load(io.open(LOTE, encoding="utf-8"))
    cabecera_de = {v: k for k, v in (lote["meta"].get("indice_vs_cabecera") or {}).items()}
    texto, crlf = leer(MODULO)
    marca = MARCA.format(n=a.tanda)
    if marca in texto:
        print(f"tanda {a.tanda}: ya aplicada; nada que hacer")
        return 0

    existentes = {sin_tildes(k) for k in re.findall(r'^    "([^"]+)": \{', texto, re.M)}
    rid = siguiente_id(texto)
    procesados, saltados = [], []

    if a.tanda in (1, 2):
        niveles = ("A", "B") if a.tanda == 1 else ("C",)
        por_nivel = {n: [] for n in niveles}
        for e in lote["entradas"]:
            if e["nivel"] not in niveles:
                continue
            if e["forma"] in MUDANZAS:
                continue       # tanda 1, como corrección
            if sin_tildes(e["forma"]) in existentes:
                saltados.append((e["forma"], "colisión: la clave ya existe en el módulo"))
                continue
            ident = f"toponimo-{rid:03d}"
            rid += 1
            por_nivel[e["nivel"]].append((e["forma"], entrada_del_modulo(e, ident)))
            procesados.append((e["forma"], ident))
            print(f"  + {ident}  {e['nivel']}  {e['forma']}  (p. {e['pagina']})")
        for n, lista in por_nivel.items():
            if lista:
                texto = insertar_al_final(texto, f"NIVEL_{n} = {{", bloque(lista, marca))
        if a.tanda == 1:
            mudanzas = []
            for e in lote["entradas"]:
                if e["forma"] in MUDANZAS:
                    ident = MUDANZAS[e["forma"]]
                    d = entrada_del_modulo(e, ident)
                    d["razon"] = (e["razon"] + f" Corrección del §2 del lote, aplicada por "
                                  f"{DECISION}: sale del grupo de descartes del dictado "
                                  "y conserva su id.")
                    mudanzas.append((e["forma"], d))
                    texto = quitar_del_grupo_dictado(texto, e["forma"])
                    print(f"  ↷ {ident}  descartado → C  {e['forma']}  (p. {e['pagina']}; corrección del §2)")
            texto = insertar_al_final(texto, "NIVEL_C = {", bloque(mudanzas, marca))
    else:
        grupos = []
        titulos = {
            "sin_glosa": "Esteves 1989, lote de la cola (2026-09-22): referente sin glosa",
            "no_indigena_segun_esteves": "Esteves 1989, lote de la cola (2026-09-22): no indígena según el autor",
            "estrato_no_caquetio_sin_glosa": "Esteves 1989, lote de la cola (2026-09-22): estrato no caquetío según el autor, sin glosa",
        }
        for clave_g, g in lote["descartes"].items():
            ids, paginas, obs, origenes, estratos, lecturas, formas = {}, {}, {}, {}, {}, {}, []
            for x in g["formas"]:
                f = x["forma"]
                if sin_tildes(f) in existentes:
                    saltados.append((f, "colisión: la clave ya existe en el módulo"))
                    continue
                ident = f"toponimo-{rid:03d}"
                rid += 1
                ids[f] = ident
                paginas[f] = x["pagina"]
                formas.append(f)
                nota = x.get("nota", "")
                if cabecera_de.get(f):
                    nota = (nota + " " if nota else "") + f"El índice escribe {cabecera_de[f]}."
                if nota:
                    obs[f] = nota
                if x.get("clase"):
                    origenes[f] = x["clase"] + " (según Esteves)"
                if x.get("estrato"):
                    estratos[f] = x["estrato"]
                procesados.append((f, ident))
                print(f"  + {ident}  descartado  {f}  (p. {x['pagina']})")
            for lec in g.get("lecturas") or []:
                f = lec["forma"]
                l2 = {k: v for k, v in lec.items() if k != "forma"}
                lecturas.setdefault(f, []).extend(lecturas_de({"lecturas": [l2], "pagina": paginas[f]}))
            d = {"razon": " ".join(str(g["razon"]).split()), "fuente": "esteves-1989",
                 "ids": ids, "paginas": paginas, "formas": formas}
            if g.get("verificado"):
                d["verificado"] = g["verificado"]
            for campo, val in (("observaciones", obs), ("origenes", origenes),
                               ("estratos", estratos), ("lecturas", lecturas)):
                if val:
                    d[campo] = val
            grupos.append((titulos[clave_g], d))
        L = [f"    {marca}"]
        for titulo, d in grupos:
            L.append(f"    {lit(titulo)}: {{")
            for k, v in d.items():
                L.append(f"        {lit(k)}: {lit(v)},")
            L.append("    },")
        texto = insertar_al_final(texto, "DESCARTES = {", "\n".join(L) + "\n")

    # que el módulo nuevo se importe y cuente lo que tiene que contar
    ns = {}
    exec(compile(texto, MODULO, "exec"), ns)
    n_ids = len(set(re.findall(r"toponimo-\d{3}", texto)))

    t_ind, crlf_ind, nuevos, faltan, ya, pp = actualizar_indice(
        procesados + ([(f, i) for f, i in MUDANZAS.items()] if a.tanda == 1 else []),
        a.tanda, cabecera_de)
    for f, razon in saltados:
        print(f"  ✗ {f}: {razon}")
    for f in faltan:
        print(f"  · índice: «{f}» no estaba en por_procesar (ya registrado antes)")
    print(f"tanda {a.tanda}: {len(procesados)} entradas nuevas; ids distintos en el módulo: {n_ids}; "
          f"índice: ya_en_canon {ya}, por_procesar {pp}")
    if a.dry_run:
        print("--dry-run: no se escribe nada")
        return 0
    escribir(MODULO, texto, crlf)
    escribir(INDICE, t_ind, crlf_ind)
    print("escrito: curiana_sim/lexicon_toponimos.py y 6-fusion/toponimos_esteves_indice.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
