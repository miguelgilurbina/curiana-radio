# -*- coding: utf-8 -*-
"""Auditoría del vault: inventario, frontmatter, grafo (como lo ve Obsidian), convenciones.
Uso: python -I medir_vault.py <VAULT> <salida.json>
"""
import collections, json, os, re, sys, urllib.parse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VAULT = os.path.abspath(sys.argv[1])
OUT = sys.argv[2]

IGN = {"__pycache__", ".obsidian", ".trash", "node_modules", "data", ".git", ".claude", ".next", ".pytest_cache"}
# Lo que Obsidian indexa por defecto (sin "Detect all file extensions")
OBS_NOTA = {".md", ".canvas", ".base"}
OBS_ADJUNTO = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif", ".bmp",
               ".mp3", ".wav", ".m4a", ".ogg", ".flac", ".mp4", ".mov", ".mkv", ".webm", ".ogv"}


def rel(p):
    return os.path.relpath(p, VAULT).replace("\\", "/")


# ---------------- índice de archivos ----------------
todos = []
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in IGN]
    for f in files:
        todos.append(rel(os.path.join(root, f)))
ext_count = collections.Counter(os.path.splitext(f)[1].lower() for f in todos)

obs_files = set(f for f in todos if os.path.splitext(f)[1].lower() in OBS_NOTA | OBS_ADJUNTO)
idx_obs = collections.defaultdict(list)   # clave -> rutas (solo lo que Obsidian ve)
idx_all = collections.defaultdict(list)   # clave -> rutas (todo, como check_vault_links)


def claves(path):
    ext = os.path.splitext(path)[1]
    sin_ext = path[: -len(ext)] if ext else path
    partes = sin_ext.split("/")
    ks = set()
    for i in range(len(partes)):
        ks.add("/".join(partes[i:]))
        ks.add("/".join(partes[i:]) + ext)
    return ks


for f in todos:
    ext = os.path.splitext(f)[1].lower()
    for k in claves(f):
        idx_all[k.lower()].append(f)
        if f in obs_files:
            # Obsidian: un .md se enlaza sin extensión; un adjunto, con extensión
            if ext == ".md" or k.lower().endswith(ext):
                idx_obs[k.lower()].append(f)

md_files = sorted(f for f in todos if f.endswith(".md"))


# ---------------- clasificación ----------------
def categoria(p):
    b = os.path.basename(p)
    top = p.split("/")[0] if "/" in p else "(raiz)"
    if p in ("INDICE.md", "TABLERO.md", "CLAUDE.md"):
        return "raiz"
    if top == "1-plan":
        if re.match(r"(HANDOFF|REVISION)_", b) or re.search(r"\d{4}-\d{2}-\d{2}", b):
            return "plan-fechado"
        if b == "CRONICA.md":
            return "plan-generado"
        return "plan-vivo"
    if b.startswith("mapa-") or b == "INDICE_FUENTES.md":
        return "moc"
    if top == "2-lengua":
        return "canon-lengua"
    if p.startswith("3-mundo/ensayos/"):
        return "ensayo"
    if top == "3-mundo":
        return "canon-mundo"
    if p.startswith("4-fuentes/sesiones/"):
        return "sesion-fuente"
    if top == "4-fuentes":
        return "ficha-fuente"
    if p.startswith("5-experimento/analisis/") or p.startswith("5-experimento/series/"):
        return "analisis-run"
    if p.startswith("5-experimento/disenos/"):
        return "diseno"
    if top == "5-experimento":
        return "canon-experimento"
    if p.startswith("6-fusion/issues-pendientes/publicados/"):
        return "issue-publicado"
    if p.startswith("6-fusion/issues-pendientes/"):
        return "issue-borrador"
    if top == "6-fusion":
        return "fusion-trabajo"
    if top in ("curiana_sim", "fuentes_caquetios"):
        return "doc-codigo"
    return "otro"


FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
KEY = re.compile(r"^([^\s:#\-][^:\n]*?):(?:\s|$)", re.M)
GEN_RX = re.compile(r"<!--\s*GENERADO|Archivo generado|GENERADO por|generado_por|editar_a_mano:\s*no|No se edita a mano", re.I)


def quitar_codigo(t):
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = re.sub(r"~~~.*?~~~", "", t, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", t)


WIKI = re.compile(r"(!?)\[\[([^\[\]]+?)\]\]")
MDLINK = re.compile(r"(!?)\[([^\]\n]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
TAG = re.compile(r"(?:(?<=\s)|^)#([A-Za-zÀ-ÿ_][\w\-/À-ÿ]*)", re.M)

notas = {}
for p in md_files:
    with open(os.path.join(VAULT, p), encoding="utf-8", errors="replace") as fh:
        t = fh.read()
    m = FM.match(t)
    fm_txt = m.group(1) if m else None
    keys = []
    tipo = None
    tags_fm = []
    if fm_txt is not None:
        for km in KEY.finditer(fm_txt):
            keys.append(km.group(1).strip())
        mt = re.search(r"^tipo:\s*(.+)$", fm_txt, re.M)
        if mt:
            tipo = mt.group(1).strip().strip("'\"")
        mtag = re.search(r"^tags:\s*(.*)$", fm_txt, re.M)
        if mtag:
            tags_fm.append(mtag.group(1).strip())
    cuerpo = t[m.end():] if m else t
    limpio = quitar_codigo(cuerpo)
    tags_inline = sorted(set(TAG.findall(limpio)))
    notas[p] = dict(
        ruta=p, carpeta=os.path.dirname(p) or "(raiz)", categoria=categoria(p),
        bytes=os.path.getsize(os.path.join(VAULT, p)), lineas=t.count("\n") + 1,
        frontmatter=fm_txt is not None, claves=keys, tipo=tipo,
        generado=bool(GEN_RX.search(t)),
        tags_fm=tags_fm, tags_inline=tags_inline,
        _texto_links=limpio, _fm=fm_txt or "",
    )


# ---------------- enlaces ----------------
def resolver_wiki(destino):
    k = destino.strip().replace("\\", "/").lstrip("/").lower()
    k2 = k[:-3] if k.endswith(".md") else k
    obs = idx_obs.get(k2) or idx_obs.get(k)
    al = idx_all.get(k2) or idx_all.get(k)
    return obs, al


aristas = []
for p, n in notas.items():
    for donde, txt in (("cuerpo", n["_texto_links"]), ("frontmatter", n["_fm"])):
        for m in WIKI.finditer(txt):
            emb, inner = m.group(1), m.group(2)
            inner = inner.replace("\\|", "|")
            dest = re.split(r"[|#^]", inner, maxsplit=1)[0].rstrip("\\").strip()
            if not dest:
                continue
            obs, al = resolver_wiki(dest)
            if obs:
                tgt = obs[0]
                ext = os.path.splitext(tgt)[1].lower()
                kind = "nota" if ext in OBS_NOTA else "adjunto"
            elif al:
                tgt = al[0]
                kind = "fantasma-no-soportado"
            else:
                tgt = dest
                kind = "roto"
            aristas.append(dict(src=p, tipo="wiki", embed=bool(emb), donde=donde, raw=dest, tgt=tgt, kind=kind,
                                ambiguo=bool(obs and len(set(obs)) > 1)))
        if donde == "frontmatter":
            continue
        for m in MDLINK.finditer(txt):
            emb, texto, url = m.groups()
            if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith("#"):
                continue
            url2 = urllib.parse.unquote(url.split("#")[0].split("?")[0])
            if not url2:
                continue
            base = os.path.dirname(os.path.join(VAULT, p))
            cand = os.path.normpath(os.path.join(base, url2))
            cand_root = os.path.normpath(os.path.join(VAULT, url2.lstrip("/")))
            dentro = None
            for c in (cand, cand_root):
                if os.path.exists(c):
                    dentro = c
                    break
            if dentro is None:
                kind, tgt = "roto", url2
            else:
                r = os.path.relpath(dentro, VAULT).replace("\\", "/")
                if r.startswith(".."):
                    kind, tgt = "fuera-del-vault", r
                elif os.path.isdir(dentro):
                    kind, tgt = "carpeta", r + "/"
                else:
                    ext = os.path.splitext(r)[1].lower()
                    tgt = r
                    if ext in OBS_NOTA:
                        kind = "nota"
                    elif ext in OBS_ADJUNTO:
                        kind = "adjunto"
                    else:
                        kind = "fantasma-no-soportado"
            aristas.append(dict(src=p, tipo="md", embed=bool(emb), donde="cuerpo", raw=url, tgt=tgt, kind=kind, ambiguo=False))

# ---------------- grafo md->md ----------------
out_n = collections.defaultdict(set)
in_n = collections.defaultdict(set)
for a in aristas:
    if a["kind"] == "nota" and a["tgt"].endswith(".md") and a["tgt"] != a["src"]:
        out_n[a["src"]].add(a["tgt"])
        in_n[a["tgt"]].add(a["src"])

FANT = ("fantasma-no-soportado", "roto", "carpeta", "fuera-del-vault")
fantasmas = collections.Counter()
for a in aristas:
    if a["kind"] in FANT:
        fantasmas[(a["kind"], a["tgt"])] += 1

adj = collections.defaultdict(set)
for s, ts in out_n.items():
    for t in ts:
        adj[s].add(t)
        adj[t].add(s)


def componentes(excluir=frozenset()):
    vist = set()
    res = []
    for n0 in md_files:
        if n0 in vist or n0 in excluir:
            continue
        pila = [n0]
        c = []
        vist.add(n0)
        while pila:
            x = pila.pop()
            c.append(x)
            for y in adj[x]:
                if y not in vist and y not in excluir:
                    vist.add(y)
                    pila.append(y)
        res.append(sorted(c))
    res.sort(key=len, reverse=True)
    return res


comps = componentes()
for p, n in notas.items():
    n["in"] = len(in_n[p])
    n["out"] = len(out_n[p])
    n["in_de"] = sorted(in_n[p])
    n["out_a"] = sorted(out_n[p])
    n["links_raw"] = sum(1 for a in aristas if a["src"] == p)
    n["out_fantasma"] = len({a["tgt"] for a in aristas if a["src"] == p and a["kind"] in FANT})

mat = collections.Counter()
for s, ts in out_n.items():
    for t in ts:
        mat[(notas[s]["categoria"], notas[t]["categoria"])] += 1

res = dict(
    vault=VAULT,
    archivos_total=len(todos), ext=ext_count.most_common(),
    md_total=len(md_files),
    notas={p: {k: v for k, v in n.items() if not k.startswith("_")} for p, n in notas.items()},
    aristas=aristas,
    componentes=[len(c) for c in comps],
    componentes_pequenos=[c for c in comps if len(c) < 40],
    componentes_sin_raiz=[len(c) for c in componentes(frozenset({"INDICE.md", "TABLERO.md", "CLAUDE.md"}))],
    fantasmas=[(k[0], k[1], v) for k, v in fantasmas.most_common()],
    matriz=[(a, b, v) for (a, b), v in mat.most_common()],
)
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)

print("archivos (todas las ext, sin ignorados):", len(todos))
print("ext:", ext_count.most_common(14))
print("md:", len(md_files))
cat = collections.Counter(n["categoria"] for n in notas.values())
print("por categoría:", cat.most_common())
kinds = collections.Counter((a["tipo"], a["kind"]) for a in aristas)
print("enlaces por tipo/kind:", kinds.most_common())
print("aristas md->md distintas:", sum(len(v) for v in out_n.values()))
print("componentes:", len(comps), [len(c) for c in comps][:15])
print("componentes sin INDICE/TABLERO/CLAUDE:", res["componentes_sin_raiz"][:15], "n=", len(res["componentes_sin_raiz"]))
print("fantasmas distintos:", len(fantasmas), collections.Counter(k[0] for k in fantasmas).most_common())
