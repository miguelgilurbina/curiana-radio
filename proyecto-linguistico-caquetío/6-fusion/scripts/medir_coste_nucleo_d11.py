# -*- coding: utf-8 -*-
"""D11 fase 3 — cuánto del habla depende del núcleo reconstruido desde el wayuu.

Mide, sin tocar nada:
  1. el coste de re-derivar: de qué dependen `taya`, `pia`, `nüma`, `waya`,
     `naya`, los numerales, los posesivos `ta-`/`wa-` y las marcas `-ka`/`-ni`/
     `-da` — entradas, reglas, prompts, koiné, score, tests y docs;
  2. las colisiones de clave de las candidatas (una forma que ya es clave de
     otra lengua en VOCABULARIO_BASE no se puede añadir como caquetía sin
     renombrar, y hoy PUNTÚA como fuga a otra lengua arahuaca);
  3. las similitudes y proporciones que cita la propuesta, con la métrica del
     cómputo D11 (1 − Levenshtein/longitud máxima sobre esqueleto fonémico).

Alimenta 6-fusion/propuesta_nucleo_d11_fase3.yaml y el borrador
6-fusion/issues-pendientes/decision-d11-fase3-nucleo-lokono-achagua.md.

    python 6-fusion/scripts/medir_coste_nucleo_d11.py

⚠️ El uso en el CORPUS (word_uses) no se mide aquí: necesita Supabase local.
La última medición es la de 5-experimento/analisis/ANALISIS_BASE_2026-08-06.md.
"""
import inspect
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = Path(__file__).resolve().parents[2]
SIM = R / "curiana_sim"
sys.path.insert(0, str(SIM))

import curiana_lexicon as CL  # noqa: E402
import curiana_koine as CK    # noqa: E402

V = CL.VOCABULARIO_BASE
L = "a-záéíóúñü"

# ── Las formas del núcleo actual ────────────────────────────────────────
PRONOMBRES = ["taya", "pia", "nüma", "waya", "naya", "tayamaa"]
NUMERALES = ["wanee", "piama", "apünüin", "pienchi", "jarai", "polo"]
POSESIVOS = ["ta-", "wa-", "pi-", "nü-"]
ASPECTO = ["-ka", "-ni", "-da"]


def patron(forma: str) -> re.Pattern:
    """Frontera de morfema. Palabras: ni letra a ningún lado. Prefijo: sin
    letra ni guion delante (cuenta el uso `ta-barsure` y la mención `ta- (mi)`).
    Sufijo: sin letra detrás (cuenta `naa-ka` y la mención `-ka (hecho)`); los
    nombres de agente con guion se descartan en `contar`."""
    f = re.escape(forma.strip("-"))
    if forma.endswith("-"):
        return re.compile(rf"(?<![{L}\-]){f}-(?![\-])", re.I)   # ta-barsure y también «ta- (mi)»
    if forma.startswith("-"):
        return re.compile(rf"(?<!-)-{f}(?![{L}])", re.I)   # naa-ka y también la mención «-ka (hecho)»
    return re.compile(rf"(?<![{L}]){f}(?![{L}])", re.I)


# Nombres de agente con guion (Kawa-ni, Marokoto-ni, Dare-nu...) no son aspecto.
_textos_nombres = "".join((SIM / m).read_text(encoding="utf-8")
                          for m in ("curiana_agents.py", "curiana_koine.py",
                                    "curiana_orchestrator_v2.py"))
NOMBRES = set(re.findall(rf'"([A-Z][{L}]+-(?:ni|ka|da|ko|sha|nu|bi))"', _textos_nombres))


def contar(texto: str, forma: str) -> int:
    n = 0
    for m in patron(forma).finditer(texto):
        if forma.startswith("-"):
            ini = texto.rfind(" ", 0, m.start()) + 1
            tok = re.split(rf"[^{L}\-A-Z]", texto[ini:m.end()])[-1]
            if tok in NOMBRES or tok.strip("\"'") in NOMBRES:
                continue
        n += 1
    return n


def strings_de(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings_de(v)
    elif isinstance(obj, (list, tuple, set)):
        for v in obj:
            yield from strings_de(v)


# ── 1. VOCABULARIO_BASE ─────────────────────────────────────────────────
def en_vocabulario(forma):
    clave = forma if forma in V else None
    mencion = 0
    ejemplos_con_forma = 0
    for k, e in V.items():
        if k == forma:
            continue
        txt = " ".join(s for kk, s in e.items() if kk not in ("notas",) and isinstance(s, str))
        if contar(txt, forma):
            ejemplos_con_forma += 1
        if contar(str(e.get("notas", "")), forma):
            mencion += 1
    # claves que SON la forma sufijada/prefijada (naa-ka, ta-barsure)
    claves_morf = sum(1 for k in V if (forma.startswith("-") or forma.endswith("-"))
                      and contar(k, forma))
    return clave, claves_morf, ejemplos_con_forma, mencion


# ── 2. Reglas ───────────────────────────────────────────────────────────
def en_reglas(forma):
    es_regla = forma in CL.TODAS_LAS_REGLAS
    usan = [k for k, r in CL.TODAS_LAS_REGLAS.items()
            if k != forma and any(contar(s, forma) for s in strings_de(r))]
    instr = sum(contar(r.get("instruccion_agente", ""), forma)
                for r in CL.TODAS_LAS_REGLAS.values())
    return es_regla, usan, instr


# ── 3. Prompts que el agente recibe ─────────────────────────────────────
orq = (SIM / "curiana_orchestrator_v2.py").read_text(encoding="utf-8")
identidad = re.search(r'_IDENTIDAD_LINGUISTICA = """(.*?)"""', orq, re.S).group(1)
tier3 = re.search(r'else:\s*base = \((.*?)\)\s*\n\s*partes', inspect.getsource(CL.vocabulario_para_agente), re.S).group(1)
PROMPTS = {
    "prompt_reglas_completo (tier I)": CL.prompt_reglas_completo(),
    "prompt_reglas_breve (tier II)": CL.prompt_reglas_breve(),
    "bloque tier III (vocabulario_para_agente)": tier3,
    "_IDENTIDAD_LINGUISTICA (orquestador, TODOS)": identidad,
    "prompt_refuerzo (4 umbrales)": " ".join(CL.prompt_refuerzo(s, []) for s in (1, 3, 5, 6.5)),
    "prompt_rescate_linguistico": CL.prompt_rescate_linguistico("x", 3.0, 2),
}

# ── 4. Koiné y score ────────────────────────────────────────────────────
KOINE = {
    "_NUCLEO_FALLBACK": " ".join(CK._NUCLEO_FALLBACK),
    "FORMAS_SEED": " ".join(" ".join(v) for v in CK.FORMAS_SEED.values()),
    "_ASPECTO_SUFIJO": " ".join(f"x{v}" for v in CK._ASPECTO_SUFIJO.values()),
}
SCORE_SRC = {
    "_aspectos_morfologicos": inspect.getsource(CL._aspectos_morfologicos),
    "score_linguistico.es_arahuaco": inspect.getsource(CL.score_linguistico),
}

# ── 5. Tests, demos y docs (texto crudo) ───────────────────────────────
FICHEROS = {
    "tests": sorted((SIM / "tests").glob("test_*.py")) + [SIM / "test_quick.py", SIM / "test_pipeline.py"],
    "demos/semillas": [SIM / "seed_demo_run.py", SIM / "curiana_observer.py", SIM / "curiana_database.py"],
    "docs": [R / "CLAUDE.md", R / "2-lengua" / "morfologia.md", SIM / "README.md"],
}


def main():
    print("═" * 74)
    print("D11 fase 3 — dependencias del núcleo actual (medido", __import__("datetime").date.today(), ")")
    print(f"VOCABULARIO_BASE: {len(V)} claves · TODAS_LAS_REGLAS: {len(CL.TODAS_LAS_REGLAS)} reglas")
    print(f"nombres de agente excluidos del conteo de sufijos: {len(NOMBRES)}")
    print("═" * 74)
    totales = {}
    for grupo, formas in (("PRONOMBRES", PRONOMBRES), ("NUMERALES", NUMERALES),
                          ("POSESIVOS", POSESIVOS), ("ASPECTO", ASPECTO)):
        print(f"\n── {grupo} " + "─" * (70 - len(grupo)))
        for f in formas:
            clave, claves_morf, ejemplos, mencion = en_vocabulario(f)
            es_regla, usan, instr = en_reglas(f)
            p = {n: contar(t, f) for n, t in PROMPTS.items()}
            k = {n: contar(t, f) for n, t in KOINE.items()}
            s = {n: contar(t, f) if not f.startswith("-") else t.count(f'"{f[1:]}"')
                 for n, t in SCORE_SRC.items()}
            if f.endswith("-"):
                s = {n: t.count(f'"{f[:-1]}"') for n, t in SCORE_SRC.items()}
            fich = {g: sum(contar(pth.read_text(encoding="utf-8"), f) for pth in lst if pth.exists())
                    for g, lst in FICHEROS.items()}
            print(f"\n  {f}")
            print(f"    entrada propia en el lexicón: {'sí' if clave else 'no'}"
                  f"{'  (fuente ' + V[clave].get('fuente', '') + ')' if clave else ''}")
            if f.startswith("-") or f.endswith("-"):
                print(f"    claves del lexicón que la llevan: {claves_morf}")
            print(f"    otras entradas que la usan en sig/es/ejemplos: {ejemplos} · en notas: {mencion}")
            print(f"    regla propia: {'sí' if es_regla else 'no'} · otras reglas que la usan: {len(usan)} {usan[:6]}"
                  f" · usos en instruccion_agente: {instr}")
            print(f"    prompts: " + " · ".join(f"{n.split(' ')[0]}={v}" for n, v in p.items() if v) or "    prompts: 0")
            print(f"      → prompts afectados: {sum(1 for v in p.values() if v)} de {len(p)}, {sum(p.values())} apariciones")
            print(f"    koiné: " + (" · ".join(f"{n}={v}" for n, v in k.items() if v) or "0"))
            print(f"    score (literal en el código): " + (" · ".join(f"{n}={v}" for n, v in s.items() if v) or "0"))
            print(f"    tests={fich['tests']} · demos/semillas={fich['demos/semillas']} · docs={fich['docs']}")
            totales[f] = dict(prompts=sum(1 for v in p.values() if v), apar_prompts=sum(p.values()),
                              reglas=len(usan) + es_regla, instr=instr, koine=sum(k.values()),
                              score=sum(s.values()), tests=fich["tests"], demos=fich["demos/semillas"],
                              docs=fich["docs"], claves_morf=claves_morf, ejemplos=ejemplos)

    print("\n── RESUMEN (una fila por forma) " + "─" * 42)
    print(f"  {'forma':<9}{'prompts':>8}{'apar.':>7}{'reglas':>7}{'instr':>6}{'koiné':>6}{'score':>6}"
          f"{'claves':>7}{'tests':>6}{'demos':>6}{'docs':>5}")
    for f, t in totales.items():
        print(f"  {f:<9}{t['prompts']:>8}{t['apar_prompts']:>7}{t['reglas']:>7}{t['instr']:>6}"
              f"{t['koine']:>6}{t['score']:>6}{t['claves_morf']:>7}{t['tests']:>6}{t['demos']:>6}{t['docs']:>5}")

    # ── Colisiones de las candidatas ─────────────────────────────────────
    print("\n── COLISIONES DE CLAVE DE LAS CANDIDATAS " + "─" * 33)
    candidatas = ["daya", "dai", "de", "bia", "bui", "bu", "ria", "li", "lia", "tuya", "ruya",
                  "ja", "ha", "haya", "waya", "naya", "pana", "gudamuen", "sabuenen", "katarí",
                  "bi", "bo", "pa", "fa", "coa", "kuba"]
    for c in candidatas:
        e = V.get(c)
        stop = " · ⚠️ ES_STOPWORDS (el score la cuenta como ESPAÑOL)" if c in CL.ES_STOPWORDS else ""
        print(f"  {c:<9} → {(e.get('fuente'), (e.get('sig') or e.get('es'))[:44]) if e else 'libre'}{stop}")

    # ── Similitudes y proporciones ───────────────────────────────────────
    def base(s):
        s = unicodedata.normalize("NFD", str(s).lower())
        return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")

    def fon(s):
        s = base(s)
        s = re.sub(r"gu(?=[aeio])", "w", s); s = re.sub(r"qu(?=[ei])", "k", s)
        s = s.replace("tsch", "C").replace("sch", "C").replace("ch", "C").replace("sh", "C")
        s = re.sub(r"c(?=[ei])", "s", s)
        s = s.replace("c", "k").replace("z", "s").replace("v", "b").replace("j", "h").replace("y", "i")
        s = s.replace("kh", "k").replace("th", "t")
        return re.sub(r"(.)\1+", r"\1", re.sub(r"[^a-zC]", "", s))

    def lev(a, b):
        d = list(range(len(b) + 1))
        for i, ca in enumerate(a, 1):
            p = d[:]; d[0] = i
            for j, cb in enumerate(b, 1):
                d[j] = min(p[j] + 1, d[j - 1] + 1, p[j - 1] + (ca != cb))
        return d[-1]

    def sim(a, b):
        A, B = fon(a), fon(b)
        return round(1 - lev(A, B) / max(len(A), len(B)), 2)

    print("\n── SIMILITUDES (métrica del cómputo D11: gana ≥0.50 con margen ≥0.10) " + "─" * 4)
    pares = [("pana", "abba", "LK 1"), ("pana", "abana", "IC 1"), ("apana", "abana", "IC 1"),
             ("gudamuen", "biama", "LK 2"), ("gudamuen", "juchamata", "ACH 2"), ("gudamuen", "piama", "WY 2"),
             ("buiamati", "biama", "LK 2"),
             ("sabuenen", "cabbuhin", "LK 3 (Perea)"), ("sabuenen", "kabyn", "LK 3 (Pet)"),
             ("sabuenen", "mataritai", "ACH 3"), ("sabuenen", "apünüin", "WY 3"),
             ("catari", "bibiti", "LK 4 (Perea)"), ("catari", "bithi", "LK 4 (Pet)"), ("catari", "pienchi", "WY 4"),
             ("waya", "guaya", "ACH 1pl"), ("waya", "wai", "LK 1pl"), ("naya", "naya", "ACH 3pl"),
             ("taya", "dai", "LK 1sg"), ("taya", "nuya", "ACH 1sg"), ("pia", "bii", "LK 2sg"), ("pia", "jia", "ACH 2sg")]
    for a, b, rot in pares:
        print(f"  {a:<9} ~ {b:<10} [{rot:<13}] {sim(a, b):.2f}   ({fon(a)} / {fon(b)})")

    caq = [k for k, e in V.items() if e.get("fuente") == "caquetío-atestiguado"]
    lok = [k for k, e in V.items() if str(e.get("fuente", "")).startswith("lokono")]
    ach = [k for k, e in V.items() if e.get("fuente") == "achagua"]
    print("\n── PROPORCIONES EN LAS CLAVES DEL LEXICÓN (grafía, no fonema: C8) " + "─" * 8)
    for nombre, grupo in (("caquetío-atestiguado", caq), ("lokono", lok), ("achagua", ach)):
        r = sum(base(k).count("r") for k in grupo); l_ = sum(base(k).count("l") for k in grupo)
        print(f"  {nombre:<21} n={len(grupo):<5} r={r:<5} l={l_:<5}"
              f" · inicial b={sum(base(k).startswith('b') for k in grupo)} p={sum(base(k).startswith('p') for k in grupo)}"
              f" · inicial d={sum(base(k).startswith('d') for k in grupo)} t={sum(base(k).startswith('t') for k in grupo)}")


if __name__ == "__main__":
    main()
