#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — generador del tablero de estado
=========================================

Emite `TABLERO.md` en la raíz del vault: **una foto medida** del estado del
proyecto. Nace de una pregunta de Miguel — *"si visualmente no entendemos,
¿cómo vamos a saber que estamos haciendo algo bien?"* — y de la constatación
de que el grafo de Obsidian no la responde: con 78 notas siempre se ve igual,
y un grafo no dice si el lexicón mejoró. Lo que la responde es una tabla de
números medidos y fechados.

**Todo se mide contra el dato.** Ninguna cifra se copia de la documentación:
justo antes de escribir esto circulaban tres tamaños distintos del lexicón
(1416, 1414, 1413) en sitios distintos del repo. La única cifra que este script
*cita* en vez de medir son los hitos históricos de `HITOS` (mediciones pasadas,
ya no recalculables), y van marcadas como tales.

Regla arquitectónica que respeta (PLAN_MAESTRO §2): **la lógica crítica no vive
en plugins de Obsidian.** Nada de Dataview: un generador propio que emite
markdown plano, legible igual en GitHub, en VS Code y en `cat`.

Los seis paneles:

    1. El titular       — cuatro números y el semáforo del gate
    2. El lexicón       — VOCABULARIO_BASE, capas epistémicas, censo de citas
                          (importa `auditar_82.py`, no duplica su lógica)
    3. Las fuentes      — frontmatter de `4-fuentes/*.md` (la nota manda)
    4. El corpus        — YAML de `3-mundo/corpus/`
    5. El gate          — PLAN_MAESTRO §6 + protocolo 04 §2, autocalculado
    6. Decisiones       — DECISIONES_ABIERTAS.md, con su issue

Uso:
    python generar_tablero.py             # escribe TABLERO.md
    python generar_tablero.py --stdout    # lo imprime, no escribe
    python generar_tablero.py --check     # exit 1 si el de disco está viejo
    python generar_tablero.py --sin-tests # no corre pytest (más rápido)
    python generar_tablero.py --gh        # consulta el tablero real (usa red)

Si una medición falla, **sale en el tablero** como fila `⚠️ no medido` y en la
sección «Mediciones que fallaron». Un hueco visible es mejor que un número
inventado.
"""

import argparse
import collections
import datetime
import io
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
SALIDA = os.path.join(REPO, "TABLERO.md")

# Mediciones históricas ya no recalculables (el dato de entonces no existe hoy).
# Son lo único que este script cita en vez de medir; cada una lleva su origen.
HITOS = {
    "sin_cita": (82, "2026-07-21", "PLAN_MAESTRO §1"),
}

FALLOS = []  # [(qué se intentaba medir, excepción)]


def medir(que, fn, defecto=None):
    """Corre una medición y, si revienta, lo anota en vez de tumbar el tablero."""
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001 — el punto es no propagar
        FALLOS.append((que, "%s: %s" % (type(exc).__name__, exc)))
        return defecto


# ══════════════════════════════════════════════════════════════════════
#  Lectura del vault
# ══════════════════════════════════════════════════════════════════════

_FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)


def frontmatter(path):
    """Frontmatter YAML de una nota, como dict. {} si no tiene."""
    import yaml

    with open(path, encoding="utf-8") as fh:
        m = _FM.match(fh.read())
    if not m:
        return {}
    datos = yaml.safe_load(m.group(1))
    return datos if isinstance(datos, dict) else {}


def notas_de_fuente():
    """[(basename, frontmatter)] de 4-fuentes/*.md con `tipo: fuente`."""
    carpeta = os.path.join(REPO, "4-fuentes")
    salida = []
    for f in sorted(os.listdir(carpeta)):
        if not f.endswith(".md"):
            continue
        fm = frontmatter(os.path.join(carpeta, f))
        if fm.get("tipo") == "fuente":
            salida.append((f[:-3], fm))
    return salida


def _lexicon():
    if AQUI not in sys.path:
        sys.path.insert(0, AQUI)
    import curiana_lexicon as L

    return L


# ══════════════════════════════════════════════════════════════════════
#  Panel 2 — el lexicón
# ══════════════════════════════════════════════════════════════════════

def medir_lexicon():
    from curiana_database import normalize_source_language as norm

    L = _lexicon()
    voc = L.VOCABULARIO_BASE
    crudo = collections.Counter(str(v.get("fuente", "")) for v in voc.values())
    normal = collections.Counter(norm(str(v.get("fuente", ""))) for v in voc.values())

    familia = {k: v for k, v in voc.items()
               if "caquet" in str(v.get("fuente", "")).lower()}

    def capa(clave):
        return sorted(k for k, v in familia.items()
                      if clave in str(v.get("fuente", "")).lower())

    atestiguado = capa("atestiguado")
    reconstruido = capa("reconstruido")
    hipotetico = capa("hipot")
    sin_marca = [k for k in familia
                 if k not in set(atestiguado) | set(reconstruido) | set(hipotetico)]

    try:
        import lexicon_candidatos as C
        candidatos = len(C.CANDIDATOS_NO_VERIFICADOS)
    except Exception:
        candidatos = None

    return {
        "total": len(voc),
        "crudo": crudo,
        "normal": normal,
        "familia": familia,
        "atestiguado": atestiguado,
        "reconstruido": reconstruido,
        "hipotetico": hipotetico,
        "sin_marca": sin_marca,
        "fuera_del_habla": getattr(L, "FUERA_DEL_HABLA", {}),
        "candidatos": candidatos,
    }


def medir_censo_citas():
    """Importa `auditar_82.py` — el censo de citas ya está escrito ahí."""
    if AQUI not in sys.path:
        sys.path.insert(0, AQUI)
    import auditar_82

    palabras, voc = auditar_82.censo_actual()
    dichos = auditar_82.leer_propuestas()
    veredictos = {p: auditar_82.veredicto(dichos.get(p, [])) for p in palabras}
    por_clase = collections.Counter(veredictos.values())

    # `auditar_82` cruza cuatro minerías; si a alguna le falta su módulo o su
    # nota, degrada en silencio (imprime a stderr y sigue). Aquí eso se ve.
    brazos_caidos = []
    for nombre in ("lexicon_alvarado", "lexicon_gatschet", "lexicon_van_buurt"):
        if not os.path.exists(os.path.join(AQUI, nombre + ".py")):
            brazos_caidos.append(nombre + ".py")
    if not os.path.exists(auditar_82.NOTA_ZAVALA):
        brazos_caidos.append(os.path.relpath(auditar_82.NOTA_ZAVALA, REPO))

    return {
        "palabras": palabras,
        "veredictos": veredictos,
        "por_clase": por_clase,
        "voc": voc,
        "brazos_caidos": brazos_caidos,
    }


def medir_quien_sostiene(lex):
    """¿Cuántas entradas de familia caquetía cita cada obra en su campo `notas`?

    Los patrones de búsqueda **salen de las propias notas de fuente**
    (`autor` + `aliases`), no de una lista cableada: si mañana se añade una
    obra al vault, aparece sola en esta tabla.
    """
    patrones = []
    for slug, fm in notas_de_fuente():
        claves = set()
        autor = str(fm.get("autor", ""))
        apellido = autor.split(",")[0].strip()
        if len(apellido) >= 4 and apellido.lower() != "varios":
            claves.add(apellido)
        for alias in fm.get("aliases") or []:
            alias = str(alias).strip()
            if len(alias) >= 5:
                claves.add(alias)
        if claves:
            patrones.append((slug, fm.get("obra", slug), claves))

    cuenta = collections.Counter()
    con_notas = 0
    huerfanas = []
    for palabra, v in lex["familia"].items():
        notas = str(v.get("notas", "")) + " " + str(v.get("glosa_fuente", ""))
        if not v.get("notas"):
            continue
        con_notas += 1
        tocada = False
        for slug, _obra, claves in patrones:
            if any(c.lower() in notas.lower() for c in claves):
                cuenta[slug] += 1
                tocada = True
        if not tocada:
            huerfanas.append(palabra)
    return cuenta, con_notas, huerfanas


def medir_colisiones_ck(lex):
    """Pares c/k: formas que colapsan al normalizar k→c (insumo de F2/D5)."""
    voc = _lexicon().VOCABULARIO_BASE
    grupos = collections.defaultdict(list)
    for palabra in voc:
        clave = palabra.lower().replace("qu", "c").replace("k", "c")
        grupos[clave].append(palabra)
    colisiones = {k: v for k, v in grupos.items() if len(v) > 1}
    dentro = {k: formas for k, formas in colisiones.items()
              if all("caquet" in str(voc[f].get("fuente", "")).lower() for f in formas)}
    return colisiones, dentro


# ══════════════════════════════════════════════════════════════════════
#  Panel 4 — el corpus cultural
# ══════════════════════════════════════════════════════════════════════

ETIQUETAS = ["atestiguado", "reconstruido", "canon-simulacion",
             "hipotetico", "retro-abstraido"]


def medir_corpus():
    import yaml

    carpeta = os.path.join(REPO, "3-mundo", "corpus")
    archivos = []
    otras = []          # estructuras que no son hechos etiquetados
    for f in sorted(os.listdir(carpeta)):
        if not f.endswith((".yaml", ".yml")):
            continue
        with open(os.path.join(carpeta, f), encoding="utf-8") as fh:
            datos = yaml.safe_load(fh)
        hechos = []
        if isinstance(datos, list):
            hechos = [h for h in datos if isinstance(h, dict)]
        elif isinstance(datos, dict):
            for clave, valor in datos.items():
                if clave == "entradas" and isinstance(valor, list):
                    hechos = [h for h in valor if isinstance(h, dict)]
                elif isinstance(valor, (list, dict)):
                    otras.append((f, clave, len(valor)))
        if not hechos:
            continue
        cuenta = collections.Counter(str(h.get("fuente", "—")) for h in hechos)
        con_ref = sum(1 for h in hechos if h.get("referencia"))
        archivos.append({"archivo": f, "n": len(hechos),
                         "etiquetas": cuenta, "con_ref": con_ref})
    return archivos, otras


# ══════════════════════════════════════════════════════════════════════
#  Panel 6 — decisiones
# ══════════════════════════════════════════════════════════════════════

FILA_DEC = re.compile(
    r"^\|\s*(?:\[)?(D\d+)(?:\]\((?P<url>[^)]+)\))?\s*\|"
    r"\s*(?P<que>[^|]+?)\s*\|\s*(?P<bloquea>[^|]*?)\s*\|\s*(?P<estado>[^|]+?)\s*\|\s*$")


def medir_decisiones():
    path = os.path.join(REPO, "1-plan", "DECISIONES_ABIERTAS.md")
    filas = []
    with open(path, encoding="utf-8") as fh:
        for linea in fh:
            m = FILA_DEC.match(linea.rstrip("\n"))
            if not m:
                continue
            url = m.group("url") or ""
            issue = url.rstrip("/").rsplit("/", 1)[-1] if "/issues/" in url else None
            estado = m.group("estado")
            filas.append({
                "id": m.group(1),
                "que": m.group("que").strip(),
                "bloquea": m.group("bloquea").strip(),
                "estado": estado.strip(),
                "abierta": "abierta" in estado.lower(),
                "issue": issue,
                "url": url,
            })
    if not filas:
        raise RuntimeError("no se reconoció ninguna fila de decisión en el Panorama")
    return filas


def consultar_gh(filas):
    """Estado real del tablero. Solo con --gh; degrada sin ruido si falla."""
    numeros = [f["issue"] for f in filas if f["issue"]]
    if not numeros:
        return None, "ninguna decisión tiene issue anotado"
    try:
        out = subprocess.run(
            ["gh", "issue", "list", "--repo", "miguelgilurbina/curiana-radio",
             "--state", "all", "--limit", "200", "--json", "number,state,title"],
            capture_output=True, text=True, timeout=25, encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        return None, "gh no se pudo ejecutar (%s)" % type(exc).__name__
    if out.returncode != 0:
        return None, "gh devolvió error: %s" % (out.stderr or "").strip()[:120]
    try:
        datos = json.loads(out.stdout)
    except Exception:  # noqa: BLE001
        return None, "gh devolvió algo que no es JSON"
    return {str(d["number"]): d for d in datos}, None


# ══════════════════════════════════════════════════════════════════════
#  Panel 5 — el gate
# ══════════════════════════════════════════════════════════════════════

MINADA = {"minado", "completo"}

# Etiqueta corta de cada condición, solo para el titular (la condición completa
# se escribe en la tabla del panel 4).
ETIQUETA_GATE = {
    1: "censo de citas (F1)",
    2: "pares c/k (F2 · D5)",
    3: "fuentes ALTA (F3-F5)",
    4: "validador del corpus (V2)",
    5: "citas del corpus (F10)",
    6: "decisiones D1/D3/D5",
    7: "glosa de `-bana` (D9)",
    8: "wayunaiki vs. lokono (D11)",
    9: "exportador de runs",
}


def medir_gate(lex, censo, fuentes, corpus, decisiones):
    """Las 9 condiciones del protocolo 04 §2 (que amplía PLAN_MAESTRO §6).

    Se calcula todo lo calculable. Lo que depende de un criterio humano se
    marca bloqueado por su issue, no se adivina.
    """
    por_id = {d["id"]: d for d in (decisiones or [])}

    def dec(*ids):
        """Estado combinado de un grupo de decisiones."""
        faltan = [i for i in ids if por_id.get(i, {}).get("abierta", True)]
        ref = " · ".join("[%s](%s)" % (i, por_id[i]["url"]) if por_id.get(i, {}).get("url")
                         else i for i in ids)
        return (not faltan), ("abiertas: %s" % ", ".join(faltan) if faltan
                              else "todas tomadas") + " — " + ref

    filas = []

    # 1 — censo de citas
    if censo is None:
        filas.append((1, "Lexicón: 0 entradas de familia caquetía sin cita "
                         "**o sin degradar** (F1)", None, "no medido"))
    else:
        n = len(censo["palabras"])
        filas.append((1, "Lexicón: 0 entradas de familia caquetía sin cita "
                         "**o sin degradar** (F1)", n == 0,
                      "%d sin cita (eran %d el %s)" % (n, HITOS["sin_cita"][0],
                                                       HITOS["sin_cita"][1])))

    # 2 — pares c/k
    ok2, det2 = dec("D5")
    colisiones = medir("colisiones c/k", lambda: medir_colisiones_ck(lex), (None, None))
    extra = ""
    if colisiones[0] is not None:
        extra = " · medido: %d colisiones, %d dentro del caquetío" % (
            len(colisiones[0]), len(colisiones[1]))
    filas.append((2, "Pares c/k resueltos (F2)", ok2, det2 + extra))

    # 3 — las 3 fuentes ALTA del gate (F3, F4, F5), identificadas por `tareas`
    if fuentes is None:
        filas.append((3, "Las 3 fuentes ALTA minadas (F3, F4, F5)", None, "no medido"))
    else:
        trio = []
        for tarea in ("F3", "F4", "F5"):
            hit = [(s, fm) for s, fm in fuentes
                   if tarea in [str(t) for t in (fm.get("tareas") or [])]]
            for slug, fm in hit:
                trio.append((tarea, slug, str(fm.get("estado_minado", "?"))))
        minadas = [t for t in trio if t[2] in MINADA]
        filas.append((3, "Las 3 fuentes ALTA minadas (F3, F4, F5)",
                      len(trio) == 3 and len(minadas) == 3,
                      " · ".join("%s [[%s]] %s" % (t, s, e) for t, s, e in trio)
                      or "ninguna nota lleva las tareas F3/F4/F5"))

    # 4 — validador del corpus
    existe = os.path.exists(os.path.join(AQUI, "compilar_corpus.py")) or \
        os.path.exists(os.path.join(REPO, "compilar_corpus.py"))
    filas.append((4, "`compilar_corpus.py` en verde (V2)", existe,
                  "el archivo existe" if existe else "no existe todavía"))

    # 5 — citas del corpus verificadas (F10)
    if corpus is None:
        filas.append((5, "Citas del corpus verificadas por muestreo (F10)", None,
                      "no medido"))
    else:
        total = sum(a["n"] for a in corpus[0])
        conref = sum(a["con_ref"] for a in corpus[0])
        filas.append((5, "Citas del corpus verificadas por muestreo (F10)", None,
                      "**no automedible**: que la cita *resuelva* (que la página "
                      "exista) es trabajo humano. Medible sí: %d/%d hechos "
                      "**tienen** `referencia`" % (conref, total)))

    # 6, 7, 8 — decisiones
    ok6, det6 = dec("D1", "D3", "D5")
    filas.append((6, "D1, D3 y D5 tomadas", ok6, det6))
    ok7, det7 = dec("D9")
    filas.append((7, "La glosa de `-bana` resuelta", ok7, det7))
    ok8, det8 = dec("D11")
    razon = det8
    if lex:
        n = lex["normal"]
        if n.get("lokono"):
            razon += " · medido: wayunaiki %d vs. lokono %d (%.1f a 1)" % (
                n.get("wayunaiki", 0), n["lokono"],
                n.get("wayunaiki", 0) / float(n["lokono"]))
    filas.append((8, "El desbalance wayunaiki/lokono resuelto", ok8, razon))

    # 9 — exportador
    filas.append((9, "`export_runs_index.py` reparado", None,
                  "**no automedible sin correr un export contra la base** "
                  "(ver [[04_protocolo_run_1_era_auditada]] §2.9)"))
    return filas


# ══════════════════════════════════════════════════════════════════════
#  Mediciones sueltas
# ══════════════════════════════════════════════════════════════════════

def medir_vault():
    """Reusa el indexador de `check_vault_links.py` — el guardián del grafo."""
    if REPO not in sys.path:
        sys.path.insert(0, REPO)
    import check_vault_links as V

    idx, claves_por_ruta = V.indexar()
    total, rotos = 0, set()
    for root, f in V._caminar():
        if not f.endswith(".md"):
            continue
        # El propio tablero se excluye: si sus wikilinks contaran, el número
        # que imprime cambiaría cada vez que cambia el tablero, y `--check`
        # nunca convergería.
        if os.path.abspath(os.path.join(root, f)) == os.path.abspath(SALIDA):
            continue
        with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
            txt = V.sin_codigo(fh.read())
        for m in V.LINK.finditer(txt):
            total += 1
            if m.group(1).strip() not in idx:
                rotos.add(m.group(1).strip())
    # El tablero se descuenta también del índice: si no, la cifra cambiaría
    # entre la primera generación y la segunda, y `--check` daría un falso
    # positivo exactamente una vez.
    notas = len([r for r in claves_por_ruta
                 if os.path.abspath(os.path.join(REPO, r)) != os.path.abspath(SALIDA)])
    return {"wikilinks": total, "rotos": len(rotos), "notas": notas}


def medir_tests():
    out = subprocess.run([sys.executable, "-m", "pytest",
                          os.path.join(AQUI, "tests"), "-q", "--no-header"],
                         capture_output=True, text=True, timeout=300,
                         encoding="utf-8", errors="replace", cwd=REPO)
    texto = (out.stdout or "") + (out.stderr or "")
    m = re.search(r"(\d+) passed", texto)
    fallidos = re.search(r"(\d+) failed", texto)
    if not m and not fallidos:
        raise RuntimeError("pytest no reportó totales (rc=%s)" % out.returncode)
    return {"passed": int(m.group(1)) if m else 0,
            "failed": int(fallidos.group(1)) if fallidos else 0}


# ══════════════════════════════════════════════════════════════════════
#  Composición del markdown
# ══════════════════════════════════════════════════════════════════════

MARCA_FECHA = "<!--GENERADO-->"


def crudo(v):
    """YAML convierte `capa_texto: no` en False. Se devuelve a su forma legible."""
    if v is True:
        return "si"
    if v is False:
        return "no"
    return "—" if v is None else str(v)


def semaforo(ok):
    return {True: "🟢", False: "🔴", None: "⚪"}[ok]


def tabla(cabecera, filas):
    salida = ["| " + " | ".join(cabecera) + " |",
              "|" + "|".join("---" for _ in cabecera) + "|"]
    for f in filas:
        salida.append("| " + " | ".join(str(c) for c in f) + " |")
    return salida


def componer(datos):
    L = []
    a = L.append
    d = datos

    a("---")
    a("tipo: tablero")
    a("generado_por: curiana_sim/generar_tablero.py")
    a("editar_a_mano: no")
    a("---")
    a("")
    a("# Tablero de estado — Curiana")
    a("")
    a("> ⚠️ **Archivo generado. No se edita a mano.** Cada número de abajo se")
    a("> mide contra el dato en el momento de generar; ninguno se copia de la")
    a("> documentación. Para regenerarlo:")
    a("> ```")
    a("> python curiana_sim/generar_tablero.py")
    a("> ```")
    a("")
    a(MARCA_FECHA + " Generado el **%s**." % d["fecha"])
    a("")

    # ── 1. El titular ────────────────────────────────────────────────
    a("## ¿Vamos bien?")
    a("")
    filas = []
    censo, lex, corpus, tests, gate = (d["censo"], d["lex"], d["corpus"],
                                       d["tests"], d["gate"])
    if censo is not None:
        n = len(censo["palabras"])
        filas.append(("Entradas del lexicón **sin cita**",
                      "**%d**" % n,
                      "%d (%s)" % (HITOS["sin_cita"][0], HITOS["sin_cita"][1]),
                      "🟢 −%d" % (HITOS["sin_cita"][0] - n) if n < HITOS["sin_cita"][0]
                      else "🔴"))
    else:
        filas.append(("Entradas del lexicón **sin cita**", "⚠️ no medido", "—", "⚠️"))
    if corpus is not None:
        tot = sum(x["n"] for x in corpus[0])
        ref = sum(x["con_ref"] for x in corpus[0])
        filas.append(("Hechos del corpus **con referencia**",
                      "**%d / %d**" % (ref, tot), "—",
                      "🟢" if ref == tot else "🟡"))
    else:
        filas.append(("Hechos del corpus **con referencia**", "⚠️ no medido", "—", "⚠️"))
    if tests is not None:
        filas.append(("Tests del motor",
                      "**%d en verde**" % tests["passed"],
                      "%d rojos" % tests["failed"] if tests["failed"] else "0 rojos",
                      "🟢" if not tests["failed"] else "🔴"))
    else:
        filas.append(("Tests del motor", "⚠️ no medido", "—", "⚠️"))
    if gate is not None:
        cumplidas = sum(1 for _, _, ok, _ in gate if ok is True)
        filas.append(("Gate para reanudar simulaciones",
                      "**%d de %d** condiciones" % (cumplidas, len(gate)),
                      "faltan %d" % (len(gate) - cumplidas),
                      "🟢" if cumplidas == len(gate) else "🔴"))
    if d["decisiones"] is not None:
        abiertas = sum(1 for x in d["decisiones"] if x["abierta"])
        filas.append(("Decisiones esperando a Miguel", "**%d abiertas**" % abiertas,
                      "%d resueltas" % (len(d["decisiones"]) - abiertas),
                      "🟡" if abiertas else "🟢"))
    L += tabla(["", "Hoy", "Referencia", ""], filas)
    a("")
    if gate is not None:
        rojas = [f for f in gate if f[2] is False]
        grises = [f for f in gate if f[2] is None]
        if rojas:
            a("**Lo que bloquea hoy:** %s."
              % " · ".join(ETIQUETA_GATE.get(f[0], str(f[0])) for f in rojas))
        else:
            a("**Ninguna condición del gate está en rojo.**")
        if grises:
            a("Y %d condición(es) que **nadie puede medir por script**: %s."
              % (len(grises),
                 " · ".join(ETIQUETA_GATE.get(f[0], str(f[0])) for f in grises)))
        a("")
    a("Detalle de cada número: [lexicón](#1-el-lexicón) · "
      "[fuentes](#2-las-fuentes) · [corpus](#3-el-corpus-cultural) · "
      "[gate](#4-el-gate-para-reanudar-simulaciones) · "
      "[decisiones](#5-decisiones-e-issues)")
    a("")
    a("---")
    a("")

    # ── 2. El lexicón ────────────────────────────────────────────────
    a("## 1. El lexicón")
    a("")
    a("Nota: [[lexicon]] · código: `curiana_sim/curiana_lexicon.py`")
    a("")
    if lex is None:
        a("⚠️ **No medido.** Ver «Mediciones que fallaron».")
    else:
        a("**%d entradas activas** en `VOCABULARIO_BASE`." % lex["total"])
        a("")
        a("### Por lengua (categoría normalizada)")
        a("")
        L += tabla(["Lengua (`normalize_source_language()`)", "n", "% del lexicón"],
                   [(k, v, "%.1f%%" % (100.0 * v / lex["total"]))
                    for k, v in lex["normal"].most_common()])
        a("")
        a("<details><summary>Los %d valores de <code>fuente</code> en el dato crudo "
          "(F8 quiere sanearlos)</summary>" % len(lex["crudo"]))
        a("")
        L += tabla(["`fuente` crudo", "n"], lex["crudo"].most_common())
        a("")
        a("</details>")
        a("")
        a("### La familia caquetía por capa epistémica")
        a("")
        fam = len(lex["familia"])
        L += tabla(["Capa", "n", "Qué significa"], [
            ("`caquetío-atestiguado`", len(lex["atestiguado"]),
             "dato histórico citable a fuente concreta"),
            ("`caquetío-reconstruido`", len(lex["reconstruido"]),
             "vocabulario de trabajo del proyecto"),
            ("`caquetío-hipotético`", len(lex["hipotetico"]),
             "baja de tier por D10 — la lengua no se discute, la confianza sí"),
            ("`caquetío` a secas / topónimo", len(lex["sin_marca"]),
             "sin capa declarada en el campo `fuente`"),
            ("**total familia caquetía**", "**%d**" % fam, ""),
        ])
        a("")
        if lex["candidatos"] is not None:
            a("Fuera del habla activa: **%d** candidatas `hipotético-no-verificado` "
              "en `lexicon_candidatos.py` (aisladas el 2026-06-28) y **%d** entrada(s) "
              "en `FUERA_DEL_HABLA` (%s)."
              % (lex["candidatos"], len(lex["fuera_del_habla"]),
                 ", ".join("`%s`" % k for k in lex["fuera_del_habla"]) or "vacío"))
            a("")

    # censo de citas
    a("### Censo de citas — la deuda de F1")
    a("")
    if censo is None:
        a("⚠️ **No medido.** Ver «Mediciones que fallaron».")
    else:
        n = len(censo["palabras"])
        a("Entradas de familia caquetía **sin nada en `notas`**: **%d** "
          "(eran %d el %s, %s). Lo calcula `curiana_sim/auditar_82.py`, "
          "que este tablero importa en vez de duplicar."
          % (n, HITOS["sin_cita"][0], HITOS["sin_cita"][1], HITOS["sin_cita"][2]))
        a("")
        if n:
            L += tabla(["Palabra", "Significado", "Veredicto de las 4 minerías"],
                       [("`%s`" % p,
                         str(censo["voc"][p].get("sig", ""))[:60],
                         "`%s`" % censo["veredictos"][p])
                        for p in censo["palabras"]])
            a("")
            a("Las que quedan **no son deuda de minería sino de decisión**: no "
              "dejan rastro en ninguna de las cuatro fuentes minadas.")
            a("")
        if censo["brazos_caidos"]:
            a("> ⚠️ **El cruce está corriendo cojo.** `auditar_82.py` cruza cuatro "
              "minerías y degrada en silencio si a alguna le falta su archivo. "
              "Hoy no encuentra: %s."
              % ", ".join("`%s`" % b for b in censo["brazos_caidos"]))
            a("")

    a("### Quién sostiene el «atestiguado»")
    a("")
    if d["sostiene"] is None or lex is None:
        a("⚠️ **No medido.** Ver «Mediciones que fallaron».")
    else:
        cuenta, con_notas, huerfanas = d["sostiene"]
        a("Cuántas de las %d entradas de familia caquetía **con `notas`** citan a "
          "cada obra. Los patrones de búsqueda salen del `autor` y los `aliases` "
          "de cada nota de `4-fuentes/`, así que una obra nueva aparece sola aquí."
          % con_notas)
        a("")
        L += tabla(["Obra", "Entradas que la citan", "% de las citadas"],
                   [("[[%s]]" % slug, k, "%.0f%%" % (100.0 * k / max(con_notas, 1)))
                    for slug, k in cuenta.most_common() if k])
        a("")
        a("Las obras que no aparecen tienen **penetración cero** en el lexicón. "
          "Entradas con `notas` que no citan a ninguna obra del vault: **%d**."
          % len(huerfanas))
        a("")

    a("---")
    a("")

    # ── 3. Las fuentes ───────────────────────────────────────────────
    a("## 2. Las fuentes")
    a("")
    a("Índice: [[INDICE_FUENTES]]. **La nota de cada obra es la fuente de verdad**; "
      "esta tabla lee su frontmatter (`estado_minado`, `prioridad`, `capa_texto`, "
      "`sostiene`), no una lista cableada.")
    a("")
    if d["fuentes"] is None:
        a("⚠️ **No medido.** Ver «Mediciones que fallaron».")
    else:
        fuentes = d["fuentes"]
        por_estado = collections.Counter(str(fm.get("estado_minado", "—"))
                                         for _, fm in fuentes)
        a("**%d notas de obra.**" % len(fuentes))
        a("")
        L += tabla(["`estado_minado`", "n"], por_estado.most_common())
        a("")
        pendientes = [(s, fm) for s, fm in fuentes
                      if str(fm.get("prioridad")) == "alta"
                      and str(fm.get("estado_minado")) not in MINADA]
        if pendientes:
            a("**Prioridad ALTA sin minar (%d):** %s."
              % (len(pendientes),
                 ", ".join("[[%s]] (`%s`)" % (s, fm.get("estado_minado"))
                           for s, fm in pendientes)))
        else:
            a("**Ninguna fuente de prioridad ALTA queda sin minar.**")
        a("")
        medidas = d["sostiene"][0] if d["sostiene"] else {}
        a("<details><summary>Las %d notas, una por fila</summary>" % len(fuentes))
        a("")
        filas = []
        for slug, fm in sorted(fuentes,
                               key=lambda x: (-(x[1].get("sostiene") or {}).get("entradas_lexicon", 0),
                                              -(x[1].get("sostiene") or {}).get("hechos_corpus", 0),
                                              x[0])):
            sos = fm.get("sostiene") or {}
            filas.append(("[[%s]]" % slug,
                          crudo(fm.get("estado_minado")),
                          crudo(fm.get("prioridad")),
                          crudo(fm.get("capa_texto")),
                          sos.get("entradas_lexicon", 0),
                          medidas.get(slug, 0),
                          sos.get("hechos_corpus", 0)))
        L += tabla(["Nota", "minado", "prioridad", "capa texto",
                    "lexicón (declarado)", "lexicón (medido)", "hechos corpus"],
                   filas)
        a("")
        a("</details>")
        a("")
        tot_lex = sum((fm.get("sostiene") or {}).get("entradas_lexicon", 0)
                      for _, fm in fuentes)
        tot_cor = sum((fm.get("sostiene") or {}).get("hechos_corpus", 0)
                      for _, fm in fuentes)
        a("Suma declarada en los frontmatter: **%d** entradas de lexicón y "
          "**%d** hechos de corpus sostenidos. La columna *medido* cuenta las "
          "entradas de familia caquetía cuyo campo `notas` nombra a esa obra; "
          "donde las dos columnas difieren, **manda la medida** — el "
          "frontmatter se escribió a mano y envejece." % (tot_lex, tot_cor))
        a("")
    a("---")
    a("")

    # ── 4. El corpus ─────────────────────────────────────────────────
    a("## 3. El corpus cultural")
    a("")
    a("Mapas: [[mapa-familia]] · [[mapa-ecologia]] · [[mapa-creencia]] · "
      "[[mapa-transmision]] · [[mapa-geografia-politica]]. "
      "Dato: `3-mundo/corpus/*.yaml`.")
    a("")
    if corpus is None:
        a("⚠️ **No medido.** Ver «Mediciones que fallaron».")
    else:
        archivos, otras = corpus
        filas = []
        totales = collections.Counter()
        for x in archivos:
            totales.update(x["etiquetas"])
            filas.append(tuple(["`%s`" % x["archivo"], x["n"]]
                               + [x["etiquetas"].get(e, 0) or "" for e in ETIQUETAS]
                               + ["%d/%d" % (x["con_ref"], x["n"])]))
        tot = sum(x["n"] for x in archivos)
        ref = sum(x["con_ref"] for x in archivos)
        filas.append(tuple(["**total**", "**%d**" % tot]
                           + ["**%d**" % totales.get(e, 0) for e in ETIQUETAS]
                           + ["**%d/%d**" % (ref, tot)]))
        L += tabla(["Archivo", "hechos"] + ["`%s`" % e for e in ETIQUETAS]
                   + ["con `referencia`"], filas)
        a("")
        sueltas = set(totales) - set(ETIQUETAS)
        if sueltas:
            a("> ⚠️ Etiquetas fuera de las cinco canónicas: %s."
              % ", ".join("`%s`" % s for s in sorted(sueltas)))
            a("")
        if otras:
            a("Además, estructuras del corpus que **no son hechos etiquetados** "
              "(y por eso no entran en el total): %s."
              % ", ".join("`%s::%s` (%d)" % (f, k, n) for f, k, n in otras))
            a("")
    a("---")
    a("")

    # ── 5. El gate ───────────────────────────────────────────────────
    a("## 4. El gate para reanudar simulaciones")
    a("")
    a("Las simulaciones están **en pausa** ([[PLAN_MAESTRO]] §0). Se reanudan "
      "cuando **todas** estas condiciones se cumplan — [[PLAN_MAESTRO]] §6 más "
      "las tres que añadió [[04_protocolo_run_1_era_auditada]] §2.")
    a("")
    if gate is None:
        a("⚠️ **No medido.** Ver «Mediciones que fallaron».")
    else:
        L += tabla(["#", "", "Condición", "Estado medido"],
                   [(n, semaforo(ok), cond, det) for n, cond, ok, det in gate])
        a("")
        a("🟢 cumplida · 🔴 no cumplida · ⚪ no automedible (necesita criterio "
          "humano o correr algo)")
        a("")
        a("> Y una regla que no es condición sino política ([[PLAN_MAESTRO]] §6.4): "
          "el re-export del sitio se hace **después** del primer run limpio, nunca "
          "desde los runs pre-auditoría.")
        a("")
    a("---")
    a("")

    # ── 6. Decisiones ────────────────────────────────────────────────
    a("## 5. Decisiones e issues")
    a("")
    a("Argumento y evidencia de cada una: [[DECISIONES_ABIERTAS]]. "
      "El **estado** manda desde el "
      "[tablero de GitHub](https://github.com/miguelgilurbina/curiana-radio/issues).")
    a("")
    if d["decisiones"] is None:
        a("⚠️ **No medido.** Ver «Mediciones que fallaron».")
    else:
        gh, gh_error = d["gh"]
        filas = []
        for x in d["decisiones"]:
            issue = "[#%s](%s)" % (x["issue"], x["url"]) if x["issue"] else "—"
            real = ""
            if gh and x["issue"] in gh:
                real = gh[x["issue"]]["state"].lower()
            filas.append((x["id"], x["que"], x["bloquea"], x["estado"], issue, real)
                         if gh else
                         (x["id"], x["que"], x["bloquea"], x["estado"], issue))
        cab = ["#", "Decisión", "Bloquea", "Estado en la nota", "Issue"]
        if gh:
            cab.append("Estado en GitHub")
        L += tabla(cab, filas)
        a("")
        abiertas = sum(1 for x in d["decisiones"] if x["abierta"])
        declaradas = d["dec_declaradas"]
        if declaradas is not None and declaradas != abiertas:
            a("> ⚠️ **Descuadre.** El frontmatter de [[DECISIONES_ABIERTAS]] declara "
              "`abiertas: %s`, pero en su propia tabla de Panorama hay **%d** "
              "marcadas abiertas. Manda la tabla."
              % (declaradas, abiertas))
            a("")
        if gh_error:
            a("> `gh` no se consultó: %s. El tablero **no necesita red**; los "
              "estados de arriba salen de la nota. Para cruzarlos con el tablero "
              "real: `python curiana_sim/generar_tablero.py --gh`." % gh_error)
            a("")
    a("---")
    a("")

    # ── Salud del vault ──────────────────────────────────────────────
    a("## Salud del vault y del motor")
    a("")
    filas = []
    if d["vault"] is not None:
        v = d["vault"]
        filas.append(("Wikilinks", "%d en %d notas indexadas" % (v["wikilinks"], v["notas"]),
                      "🟢 0 rotos" if not v["rotos"] else "🔴 %d rotos" % v["rotos"]))
    else:
        filas.append(("Wikilinks", "⚠️ no medido", "⚠️"))
    if tests is not None:
        filas.append(("Tests (`curiana_sim/tests/`)",
                      "%d passed, %d failed" % (tests["passed"], tests["failed"]),
                      "🟢" if not tests["failed"] else "🔴"))
    else:
        filas.append(("Tests (`curiana_sim/tests/`)",
                      "no corridos (`--sin-tests`) o fallo al correrlos", "⚪"))
    L += tabla(["", "Medido", ""], filas)
    a("")
    a("Guardianes: `python check_vault_links.py --strict` · "
      "`python -m pytest curiana_sim/tests/ -q`")
    a("")

    # ── Fallos ───────────────────────────────────────────────────────
    a("## Mediciones que fallaron")
    a("")
    if not FALLOS:
        a("Ninguna: los seis paneles se midieron completos.")
    else:
        a("Un hueco que se ve es mejor que un número inventado.")
        a("")
        L += tabla(["Qué se intentaba medir", "Error"],
                   [(q, "`%s`" % e.replace("|", "\\|")) for q, e in FALLOS])
    a("")
    a("---")
    a("")
    a("Vuelta al índice: [[INDICE]] · hoja de ruta: [[PLAN_MAESTRO]]")
    return "\n".join(L) + "\n"


def sin_fecha(texto):
    """El cuerpo sin la línea de fecha, para poder comparar en `--check`."""
    return "\n".join(l for l in texto.split("\n") if not l.startswith(MARCA_FECHA))


# ══════════════════════════════════════════════════════════════════════

def recolectar(correr_tests=True, usar_gh=False):
    lex = medir("lexicón (VOCABULARIO_BASE)", medir_lexicon)
    censo = medir("censo de citas (auditar_82.py)", medir_censo_citas)
    fuentes = medir("frontmatter de 4-fuentes/", notas_de_fuente)
    corpus = medir("corpus cultural (3-mundo/corpus/*.yaml)", medir_corpus)
    decisiones = medir("decisiones (DECISIONES_ABIERTAS.md)", medir_decisiones)
    dec_declaradas = medir(
        "frontmatter de DECISIONES_ABIERTAS.md",
        lambda: frontmatter(os.path.join(REPO, "1-plan",
                                         "DECISIONES_ABIERTAS.md")).get("abiertas"))
    sostiene = medir("atribución de citas por obra",
                     lambda: medir_quien_sostiene(lex)) if lex else None
    gate = medir("gate (PLAN_MAESTRO §6 + protocolo 04 §2)",
                 lambda: medir_gate(lex, censo, fuentes, corpus, decisiones))
    vault = medir("wikilinks del vault", medir_vault)
    tests = medir("tests del motor", medir_tests) if correr_tests else None
    gh = consultar_gh(decisiones or []) if usar_gh else (None, "no consultado (sin red por defecto)")
    return {
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "lex": lex, "censo": censo, "fuentes": fuentes, "corpus": corpus,
        "decisiones": decisiones, "dec_declaradas": dec_declaradas,
        "sostiene": sostiene, "gate": gate,
        "vault": vault, "tests": tests, "gh": gh,
    }


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stdout", action="store_true", help="imprimir, no escribir")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 si TABLERO.md está desactualizado "
                         "(no combinar con --sin-tests: la fila de tests "
                         "cambiaría y daría un falso positivo)")
    ap.add_argument("--sin-tests", action="store_true", dest="sin_tests",
                    help="no correr pytest")
    ap.add_argument("--gh", action="store_true",
                    help="cruzar las decisiones con el tablero real (usa red)")
    args = ap.parse_args()

    datos = recolectar(correr_tests=not args.sin_tests, usar_gh=args.gh)
    texto = componer(datos)

    if args.stdout:
        sys.stdout.write(texto)
        return 0

    if args.check:
        if not os.path.exists(SALIDA):
            print("TABLERO.md no existe. Corre: python curiana_sim/generar_tablero.py")
            return 1
        with open(SALIDA, encoding="utf-8") as fh:
            viejo = fh.read()
        if sin_fecha(viejo) != sin_fecha(texto):
            print("TABLERO.md está DESACTUALIZADO respecto de lo medido.")
            print("Regenéralo: python curiana_sim/generar_tablero.py")
            return 1
        print("TABLERO.md al día.")
        return 0

    with open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)
    print("escrito: %s (%d líneas)" % (os.path.relpath(SALIDA, REPO),
                                       texto.count("\n")))
    if FALLOS:
        print("con %d medición(es) fallida(s) — están anotadas en el tablero"
              % len(FALLOS))
    return 0


if __name__ == "__main__":
    # La consola de Windows es cp1252 y revienta con § o ü. Se envuelve SOLO
    # aquí: hacerlo al importar rompería el stdout de quien importe el módulo.
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")
    sys.exit(main())
