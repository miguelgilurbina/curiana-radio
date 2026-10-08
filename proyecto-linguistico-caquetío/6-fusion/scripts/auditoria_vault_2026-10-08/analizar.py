# -*- coding: utf-8 -*-
import collections, json, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
d = json.load(open(sys.argv[1], encoding="utf-8"))
N = d["notas"]
A = d["aristas"]
cat = {p: n["categoria"] for p, n in N.items()}


def tabla(titulo, filas):
    print("\n## " + titulo)
    for f in filas:
        print("  ", f)


# 1. Inventario por carpeta
por_carpeta = collections.defaultdict(lambda: [0, 0, 0, 0])
for p, n in N.items():
    c = n["carpeta"]
    por_carpeta[c][0] += 1
    por_carpeta[c][1] += n["bytes"]
    por_carpeta[c][2] += 1 if n["frontmatter"] else 0
    por_carpeta[c][3] += 1 if n["generado"] else 0
tabla("carpeta: n, KB, con_fm, generadas", [(c, v[0], round(v[1] / 1024), v[2], v[3]) for c, v in sorted(por_carpeta.items())])
tot_b = sum(n["bytes"] for n in N.values())
print("total KB:", round(tot_b / 1024))

# por categoría
pc = collections.defaultdict(lambda: [0, 0, 0, 0, 0, 0, 0])
for p, n in N.items():
    c = n["categoria"]
    pc[c][0] += 1
    pc[c][1] += n["bytes"]
    pc[c][2] += 1 if n["frontmatter"] else 0
    pc[c][3] += 1 if n["generado"] else 0
    pc[c][4] += 1 if n["in"] == 0 else 0
    pc[c][5] += 1 if n["out"] == 0 else 0
    pc[c][6] += 1 if (n["in"] == 0 and n["out"] == 0) else 0
tabla("categoria: n, KB, con_fm, gen, huerfanas(in0), sumideros(out0), aisladas", [(c, v[0], round(v[1] / 1024), v[2], v[3], v[4], v[5], v[6]) for c, v in sorted(pc.items(), key=lambda x: -x[1][0])])

# 2. frontmatter
kc = collections.Counter()
for n in N.values():
    for k in set(n["claves"]):
        kc[k] += 1
print("\nnotas con frontmatter:", sum(1 for n in N.values() if n["frontmatter"]), "/", len(N))
tabla("claves de frontmatter (top 45)", kc.most_common(45))
for k in ["tipo", "pregunta", "fuentes", "medido", "descripcion", "estado", "aliases", "tags", "fecha", "actualizado", "estado_minado", "generado_por"]:
    print("  clave", k, "=", kc.get(k, 0))
tc = collections.Counter(n["tipo"] for n in N.values() if n["tipo"])
tabla("valores de tipo", tc.most_common())
# tipo por categoria
tpc = collections.defaultdict(collections.Counter)
for n in N.values():
    tpc[n["categoria"]][n["tipo"] or "(sin tipo)"] += 1
tabla("tipo por categoria", [(c, dict(v)) for c, v in sorted(tpc.items())])
# tags
con_tags_fm = [p for p, n in N.items() if n["tags_fm"]]
con_tags_in = [p for p, n in N.items() if n["tags_inline"]]
print("\nnotas con tags en fm:", len(con_tags_fm), "con #tags inline:", len(con_tags_in))
tic = collections.Counter(t for n in N.values() for t in n["tags_inline"])
print("tags inline más comunes:", tic.most_common(15))

# generadas
gen = sorted(p for p, n in N.items() if n["generado"])
tabla("generadas o con bloque generado (%d)" % len(gen), gen)

# 3. grafo
print("\naristas md->md:", sum(n["out"] for n in N.values()))
top_in = sorted(N.items(), key=lambda x: -x[1]["in"])[:25]
tabla("top in-degree", [(p, n["in"], n["out"], cat[p]) for p, n in top_in])
top_out = sorted(N.items(), key=lambda x: -x[1]["out"])[:25]
tabla("top out-degree", [(p, n["out"], n["in"], cat[p], "gen" if n["generado"] else "") for p, n in top_out])
top_tot = sorted(N.items(), key=lambda x: -(x[1]["out"] + x[1]["in"]))[:20]
tabla("top grado total", [(p, n["in"] + n["out"], n["in"], n["out"], cat[p]) for p, n in top_tot])

aisl = sorted(p for p, n in N.items() if n["in"] == 0 and n["out"] == 0)
tabla("aisladas (%d) por categoria" % len(aisl), collections.Counter(cat[p] for p in aisl).most_common())
print("  ", [p for p in aisl if cat[p] not in ("issue-borrador", "issue-publicado")])
huerf = sorted(p for p, n in N.items() if n["in"] == 0)
tabla("huerfanas in=0 (%d) por categoria" % len(huerf), collections.Counter(cat[p] for p in huerf).most_common())
print("   no-issue:", [p for p in huerf if cat[p] not in ("issue-borrador", "issue-publicado")])
sumid = sorted(p for p, n in N.items() if n["out"] == 0)
tabla("sumideros out=0 (%d) por categoria" % len(sumid), collections.Counter(cat[p] for p in sumid).most_common())

# matriz
tabla("matriz categoria->categoria (aristas distintas)", d["matriz"][:40])
# aristas por categoria origen
src_c = collections.Counter()
dst_c = collections.Counter()
for p, n in N.items():
    src_c[cat[p]] += n["out"]
    dst_c[cat[p]] += n["in"]
tabla("aristas que SALEN por categoria", src_c.most_common())
tabla("aristas que ENTRAN por categoria", dst_c.most_common())
gen_out = sum(N[p]["out"] for p in gen)
print("aristas que salen de notas generadas:", gen_out)
for p in ["TABLERO.md", "INDICE.md", "CLAUDE.md", "4-fuentes/INDICE_FUENTES.md", "6-fusion/BANDEJA.md", "1-plan/CRONICA.md", "6-fusion/TOPONIMOS_POR_FUENTE.md"]:
    if p in N:
        print("  ", p, "out", N[p]["out"], "in", N[p]["in"], "raw", N[p]["links_raw"])

# componentes
print("\ncomponentes:", len(d["componentes"]), d["componentes"][:5])
print("componentes sin raiz:", len(d["componentes_sin_raiz"]), d["componentes_sin_raiz"][:6])

# fantasmas
tabla("fantasmas", d["fantasmas"])

# enlaces crudos: repetición
raw_por_src = collections.Counter(a["src"] for a in A)
print("\nenlaces crudos totales:", len(A), " en frontmatter:", sum(1 for a in A if a["donde"] == "frontmatter"),
      " embeds:", sum(1 for a in A if a["embed"]), " ambiguos:", sum(1 for a in A if a["ambiguo"]))
amb = collections.Counter(a["raw"] for a in A if a["ambiguo"])
print("ambiguos:", amb.most_common(10))
# multi-aristas: misma src->tgt repetida
rep = collections.Counter((a["src"], a["tgt"]) for a in A if a["kind"] == "nota")
print("pares src->tgt con >1 enlace:", sum(1 for v in rep.values() if v > 1), " enlaces redundantes:", sum(v - 1 for v in rep.values() if v > 1))

# 4. índices duplicados
idx_notes = ["INDICE.md", "TABLERO.md", "CLAUDE.md", "4-fuentes/INDICE_FUENTES.md", "6-fusion/BANDEJA.md",
             "1-plan/PLAN_MAESTRO.md", "1-plan/SIGUIENTE_TANDA.md", "1-plan/CRONICA.md",
             "2-lengua/mapa-lengua.md", "3-mundo/mapa-familia.md", "3-mundo/mapa-ecologia.md", "3-mundo/mapa-creencia.md",
             "3-mundo/mapa-transmision.md", "3-mundo/mapa-geografia-politica.md", "5-experimento/mapa-motor.md",
             "3-mundo/corpus/README.md", "2-lengua/datos-de-lengua.md", "6-fusion/issues-pendientes/publicados/README.md"]
sets = {p: set(N[p]["out_a"]) for p in idx_notes if p in N}
print("\n## solapamiento entre índices (|A∩B|, jaccard)")
ks = list(sets)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        a, b = sets[ks[i]], sets[ks[j]]
        inter = len(a & b)
        if inter >= 5:
            print("  ", ks[i], "x", ks[j], inter, round(inter / len(a | b), 2))
cubre = collections.Counter()
for p, s in sets.items():
    for t in s:
        cubre[t] += 1
print("destinos enlazados desde >=3 índices:", sum(1 for v in cubre.values() if v >= 3))
print("destinos enlazados desde >=2 índices:", sum(1 for v in cubre.values() if v >= 2))

# fichas de fuente: quién las enlaza
ff = [p for p in N if cat[p] == "ficha-fuente"]
solo_tablero = [p for p in ff if set(N[p]["in_de"]) <= {"TABLERO.md", "4-fuentes/INDICE_FUENTES.md"}]
print("\nfichas de fuente:", len(ff), " enlazadas SOLO desde TABLERO/INDICE_FUENTES:", len(solo_tablero))
ff_in = sorted(((N[p]["in"], p) for p in ff), reverse=True)
print("  fichas in-degree top:", ff_in[:8])
print("  fichas con in<=2:", sum(1 for x, _ in ff_in if x <= 2))
ff_out = collections.Counter()
for p in ff:
    for t in N[p]["out_a"]:
        ff_out[cat[t]] += 1
print("  fichas enlazan a (por categoria):", ff_out.most_common())

# MOCs: a qué enlazan
for p in [x for x in N if cat[x] == "moc"]:
    oc = collections.Counter(cat[t] for t in N[p]["out_a"])
    ic = collections.Counter(cat[t] for t in N[p]["in_de"])
    print("  MOC", p, "out", N[p]["out"], dict(oc), "| in", N[p]["in"], dict(ic))

# canon: ¿enlaza a su MOC?
print("\n## canon -> MOC")
mocs = {x for x in N if cat[x] == "moc"}
for p in sorted(N):
    if cat[p] in ("canon-lengua", "canon-mundo", "ensayo", "canon-experimento", "diseno", "plan-vivo"):
        a_moc = sorted(set(N[p]["out_a"]) & mocs)
        de_moc = sorted(set(N[p]["in_de"]) & mocs)
        print("  ", p, "-> MOC:", [x.split("/")[-1] for x in a_moc], " MOC->:", [x.split("/")[-1] for x in de_moc], " in", N[p]["in"], "out", N[p]["out"])

# sesiones / handoffs / issues: dirección de enlaces
print("\n## dirección trabajo<->canon")
trabajo = {"sesion-fuente", "issue-borrador", "issue-publicado", "plan-fechado", "fusion-trabajo", "analisis-run"}
canon = {"canon-lengua", "canon-mundo", "ensayo", "canon-experimento", "diseno", "moc", "ficha-fuente", "plan-vivo"}
c2t = collections.Counter()
t2c = 0
for p, n in N.items():
    for t in n["out_a"]:
        if cat[p] in canon and cat[t] in trabajo:
            c2t[(p, t)] += 1
        if cat[p] in trabajo and cat[t] in canon:
            t2c += 1
print("trabajo->canon:", t2c, " canon->trabajo:", len(c2t))
cc = collections.Counter(cat[t] for (p, t) in c2t)
print("  canon->trabajo por categoria destino:", cc.most_common())
cs = collections.Counter(p for (p, t) in c2t)
print("  canon->trabajo por nota origen:", cs.most_common(20))

# 5. nombres
def clase_nombre(b):
    s = b[:-3]
    rasgos = []
    if re.search(r"\d{4}-\d{2}-\d{2}", s):
        rasgos.append("fecha")
    if re.match(r"^\d\d[_-]", s):
        rasgos.append("prefijo-num")
    if re.search(r"[^\x00-\x7f]", s):
        rasgos.append("no-ascii")
    base = re.sub(r"\d{4}-\d{2}-\d{2}", "", s)
    if base and base == base.upper() and re.search(r"[A-Z]", base):
        rasgos.append("MAYUS")
    elif re.search(r"[A-Z]", base):
        rasgos.append("Mixto")
    if "_" in s and "-" in base.replace("_", ""):
        rasgos.append("mezcla_-")
    elif "_" in s:
        rasgos.append("snake")
    elif "-" in s:
        rasgos.append("kebab")
    return rasgos


nc = collections.Counter()
ncc = collections.defaultdict(collections.Counter)
for p in N:
    b = p.split("/")[-1]
    for r in clase_nombre(b):
        nc[r] += 1
        ncc[cat[p]][r] += 1
tabla("rasgos de nombre", nc.most_common())
tabla("rasgos de nombre por categoria", [(c, dict(v)) for c, v in sorted(ncc.items())])
bn = collections.Counter(p.split("/")[-1] for p in N)
print("basenames repetidos:", [(b, v) for b, v in bn.items() if v > 1])
largos = sorted(N, key=lambda p: -len(p.split("/")[-1]))[:8]
print("nombres más largos:", [(p.split("/")[-1], len(p.split("/")[-1])) for p in largos])

# tamaños
big = sorted(N.items(), key=lambda x: -x[1]["bytes"])[:15]
tabla("15 notas más grandes (KB)", [(p, round(n["bytes"] / 1024), cat[p]) for p, n in big])
