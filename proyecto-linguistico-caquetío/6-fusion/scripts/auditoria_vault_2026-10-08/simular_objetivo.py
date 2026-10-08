# -*- coding: utf-8 -*-
"""Simula el grafo DESPUÉS de los PR 1-4 propuestos (sin tocar el vault) y mide las vistas B y C."""
import collections, json, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
d = json.load(open(sys.argv[1], encoding="utf-8"))
N = {p: dict(n) for p, n in d["notas"].items()}
cat = {p: n["categoria"] for p, n in N.items()}
E = set()
for p, n in N.items():
    for t in n["out_a"]:
        E.add((p, t))

MUNDO, PLAN = "3-mundo/mapa-mundo.md", "1-plan/mapa-plan.md"
IDX, LEN, MOT, IND = "4-fuentes/INDICE_FUENTES.md", "2-lengua/mapa-lengua.md", "5-experimento/mapa-motor.md", "INDICE.md"
for nuevo, c in ((MUNDO, "moc"), (PLAN, "moc")):
    N[nuevo] = {"categoria": c}
    cat[nuevo] = c

# PR1: INDICE = hub de hubs; mapa-mundo y mapa-plan; MOCs completos (bajada)
E = {(a, b) for a, b in E if a != IND}
for h in (MUNDO, PLAN, IDX, LEN, MOT, "1-plan/SIGUIENTE_TANDA.md"):
    E.add((IND, h))
for m in ("3-mundo/mapa-familia.md", "3-mundo/mapa-ecologia.md", "3-mundo/mapa-creencia.md", "3-mundo/mapa-transmision.md",
          "3-mundo/mapa-geografia-politica.md", "3-mundo/polities-caquetias.md", "3-mundo/esfera-de-interaccion.md",
          "3-mundo/horizonte-de-contacto.md", "3-mundo/cronista.md", "3-mundo/CULTURA_CAQUETIA.md", "3-mundo/corpus/README.md"):
    E.add((MUNDO, m))
for p in ("1-plan/PLAN_MAESTRO.md", "1-plan/SIGUIENTE_TANDA.md", "1-plan/HARNESS.md", "1-plan/LINEA_DE_TIEMPO.md",
          "1-plan/CRONICA.md", "1-plan/HANDOFF_2026-10-01.md", "1-plan/F10_muestreo_2026-09-12.md"):
    E.add((PLAN, p))
bajada = {
    LEN: ["2-lengua/datos-de-lengua.md", "2-lengua/fonotactica.md"],
    "3-mundo/mapa-ecologia.md": ["3-mundo/corpus/ecologia_lexicon_map.md"],
    MOT: ["5-experimento/ARQUITECTURA.md", "5-experimento/DINAMICA_DE_RUNS.md", "5-experimento/DISENO_ERA2.md",
          "5-experimento/HALLAZGOS_FASE_1.md", "5-experimento/analisis/01_que_probaron_los_seis_runs.md",
          "5-experimento/analisis/ANALISIS_BASE_2026-08-06.md", "5-experimento/analisis/ANALISIS_NODOS_ERA2_2026-09-16.md",
          "5-experimento/analisis/era2_base_escena_competencia_y_director_2026-09-28.md",
          "5-experimento/analisis/serie_c_dia1_b7bc51dc.md", "5-experimento/disenos/04_protocolo_run_1_era_auditada.md",
          "5-experimento/disenos/05_perfiles_de_run.md", "5-experimento/series/era2-base/README.md"],
}
for m, ls in bajada.items():
    for x in ls:
        E.add((m, x))
# PR2: subida canon -> MOC (frontmatter moc:)
sube = {"2-lengua": LEN, "3-mundo/ensayos": None, "5-experimento": MOT, "3-mundo": MUNDO}
for p in list(N):
    c = cat[p]
    if c in ("canon-lengua",):
        E.add((p, LEN))
    elif c in ("canon-experimento", "diseno", "analisis-run"):
        E.add((p, MOT))
    elif c == "canon-mundo":
        E.add((p, MUNDO))
    elif c == "plan-vivo":
        E.add((p, PLAN))
for m in ("3-mundo/mapa-familia.md", "3-mundo/mapa-ecologia.md", "3-mundo/mapa-creencia.md", "3-mundo/mapa-transmision.md",
          "3-mundo/mapa-geografia-politica.md"):
    E.add((m, MUNDO))
for h in (MUNDO, PLAN, IDX, LEN, MOT):
    E.add((h, IND))
# PR3: cada ficha -> INDICE_FUENTES
for p in N:
    if cat[p] == "ficha-fuente":
        E.add((p, IDX))
# PR4: archivo (se van del grafo) — IDEA_PERFILES, MIGRACION, HANDOFF_09-11, REVISION
ARCH = {"5-experimento/IDEA_PERFILES_AGENTES.md", "5-experimento/MIGRACION_RUNS_EVOLUCION.md",
        "1-plan/HANDOFF_2026-09-11.md", "1-plan/REVISION_PRE_ERA2_2026-09-12.md"}


def fuera(p):
    b = p.split("/")[-1]
    return (p in ARCH or p.startswith(("6-fusion/", "4-fuentes/sesiones/", "curiana_sim/", "fuentes_caquetios/"))
            or b.startswith(("TABLERO", "CLAUDE", "CRONICA", "HANDOFF_", "REVISION_", "F10_muestreo")))


def medir(nombre, excl):
    ns = [p for p in N if not excl(p)]
    s = set(ns)
    es = {(a, b) for a, b in E if a in s and b in s and a != b}
    g = collections.Counter()
    adj = collections.defaultdict(set)
    for a, b in es:
        g[a] += 1
        g[b] += 1
        adj[a].add(b)
        adj[b].add(a)
    vis = set()
    comps = []
    for n0 in ns:
        if n0 in vis:
            continue
        st = [n0]
        vis.add(n0)
        k = 0
        while st:
            x = st.pop()
            k += 1
            for y in adj[x]:
                if y not in vis:
                    vis.add(y)
                    st.append(y)
        comps.append(k)
    ais = [p for p in ns if g[p] == 0]
    inn = collections.Counter(b for a, b in es)
    print(f"{nombre}: nodos {len(ns)} · aristas {len(es)} · aisladas {len(ais)} · componentes {len(comps)} · top in {[(p.split('/')[-1], v) for p, v in inn.most_common(6)]}")
    if ais:
        print("   aisladas:", ais)


medir("B objetivo (sin trabajo/generados/código)", fuera)
medir("C objetivo (esqueleto, sin fichas)", lambda p: fuera(p) or (p.startswith("4-fuentes/") and p != IDX))
