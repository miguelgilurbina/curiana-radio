# -*- coding: utf-8 -*-
"""¿Qué código del repo nombra rutas de notas o carpetas del vault?
Uso: python -I dependencias.py <REPO> <medida.json>
Busca, en archivos de código y configuración (no .md), el nombre de archivo de cada nota
(con .md) y las carpetas del vault; informa quién lee y quién escribe.
"""
import collections, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.abspath(sys.argv[1])
med = json.load(open(sys.argv[2], encoding="utf-8"))
VAULT_NAME = "proyecto-linguistico-caquetío"
IGN = {"node_modules", ".next", ".git", "__pycache__", ".pytest_cache", "worktrees", ".obsidian", ".trash", "data"}
EXT = {".py", ".ts", ".tsx", ".js", ".mjs", ".cjs", ".json", ".yaml", ".yml", ".toml", ".sh", ".ps1"}

codigo = []
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in IGN]
    for f in files:
        if os.path.splitext(f)[1].lower() in EXT:
            p = os.path.join(root, f)
            try:
                if os.path.getsize(p) > 3_000_000:
                    continue
                txt = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            codigo.append((os.path.relpath(p, REPO).replace("\\", "/"), txt))

notas = list(med["notas"].keys())
por_nota = collections.defaultdict(list)
for n in notas:
    b = os.path.basename(n)
    stem = b[:-3]
    pat_b = re.compile(re.escape(b))
    pat_stem = re.compile(r"[\"'/]" + re.escape(stem) + r"[\"'.]")
    for ruta, txt in codigo:
        if ruta.endswith(".json") and ("content/" in ruta or "/content/" in ruta):
            continue  # salidas generadas (seeds) no son dependencias de lectura
        hits = len(pat_b.findall(txt))
        hits_stem = len(pat_stem.findall(txt)) if hits == 0 else 0
        if hits or hits_stem:
            por_nota[n].append((ruta, hits, hits_stem))

print("## notas del vault nombradas desde código/config (%d de %d)" % (len(por_nota), len(notas)))
for n in sorted(por_nota, key=lambda x: (-len(por_nota[x]), x)):
    refs = por_nota[n]
    print("  %s  <- %s" % (n, "; ".join("%s(%d%s)" % (r, h, "+stem%d" % s if s else "") for r, h, s in refs[:8]) + (" …+%d" % (len(refs) - 8) if len(refs) > 8 else "")))

print("\n## carpetas del vault nombradas desde código/config")
carpetas = ["1-plan", "2-lengua", "3-mundo", "3-mundo/corpus", "3-mundo/ensayos", "4-fuentes", "4-fuentes/sesiones",
            "5-experimento", "5-experimento/analisis", "5-experimento/disenos", "5-experimento/series",
            "6-fusion", "6-fusion/issues-pendientes", "issues-pendientes/publicados", "6-fusion/scripts",
            "6-fusion/fichas_propuestas", "6-fusion/fusionados", "fuentes_caquetios"]
for c in carpetas:
    refs = [(r, txt.count(c)) for r, txt in codigo if c in txt and not (r.endswith(".json") and "content/" in r)]
    refs.sort(key=lambda x: -x[1])
    print("  %-34s %3d archivos  %s" % (c, len(refs), ", ".join("%s(%d)" % x for x in refs[:6])))

print("\n## código fuera del vault que nombra el vault")
for r, txt in codigo:
    if not r.startswith(VAULT_NAME) and VAULT_NAME in txt:
        print("  ", r, txt.count(VAULT_NAME))

print("\n## escritores de .md (open(..., 'w') o write_text sobre una ruta .md)")
wr = re.compile(r"(TABLERO|BANDEJA|CRONICA|TOPONIMOS_POR_FUENTE|INDICE_FUENTES|lexicon|morfologia|README|DINAMICA_DE_RUNS|MIGRACION_RUNS_EVOLUCION|esteves-1989|gbif-paraguana-2026|obis-gbif-caja-marina|CLAUDE)\.md")
for r, txt in codigo:
    if r.endswith(".py"):
        ms = set(wr.findall(txt))
        if ms and re.search(r"open\([^)]*[\"']w|write_text|\.write\(", txt):
            print("  ", r, sorted(ms))
