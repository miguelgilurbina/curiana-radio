"""¿Se ve la tanda del 21 en la boca de la gente? Cadena vieja (motor e16009d…)
contra la repetida (motor 114c991), mismos brazos y semillas, 216 + 216 cada una.
Cuenta sobre `response_text` —no sobre `word_uses`, que sólo tiene lo que el
scorer reconoce— y da respuestas que lo dicen y usos totales."""
import io
import re
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import os
SIM = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "curiana_sim"))
sys.path.insert(0, SIM)
import curiana_lexicon as L                                       # noqa: E402

CADENAS = {
    "vieja · escena": ["f2741e89", "fcdfa07a", "0313d830"],
    "NUEVA · escena": ["ce7cd2a9", "591d12d8", "59aad1c3"],
    "vieja · control": ["0345840d", "45618069", "e98227eb"],
    "NUEVA · control": ["4e3eef64", "fafdce5b", "104673f6"],
}
SEP = "\x1f"


def respuestas(ids):
    lista = ",".join(f"'{i}'" for i in ids)
    sql = (f"select a.agent_name || '{SEP}' || replace(replace(a.response_text, E'\\n', ' '), E'\\r', ' ') "
           f"from agent_responses a join turns t on t.id=a.turn_id "
           f"where left(t.run_id::text,8) in ({lista});")
    out = subprocess.run(["docker", "exec", "supabase_db_curiana_sim", "psql", "-U", "postgres",
                          "-d", "postgres", "-Atc", sql], capture_output=True).stdout.decode("utf-8", "replace")
    filas = []
    for ln in out.splitlines():
        if SEP in ln:
            ag, txt = ln.split(SEP, 1)
            filas.append((ag, txt))
    return filas


estativos = sorted(k for k, v in L.VOCABULARIO_BASE.items() if v.get("cat") == "v_estativo")
nombres_base = {k for k, v in L.VOCABULARIO_BASE.items()
                if v.get("cat") == "sust" and str(v.get("fuente", "")).startswith("caquetío")}
W = r"[a-záéíóúüñ]+"

PATRONES = {
    "u- (no-poseído, d21.13)": re.compile(rf"(?<![\w-])u-{W}", re.I),
    "-bakoa (d21.14)": re.compile(r"-bakoa\b", re.I),
    "-bacoa (la vieja)": re.compile(r"-bacoa\b", re.I),
    "estativo + aspecto (d21.4)": re.compile(
        rf"(?<![\w-])(?:{'|'.join(map(re.escape, estativos))})-(?:ka|ni|da)\b", re.I),
    "ka-juri": re.compile(r"(?<![\w-])ka-juri\b", re.I),
    "juri-ni/-ka/-da": re.compile(r"(?<![\w-])juri-(?:ni|ka|da)\b", re.I),
    "kudanga / kuté (d21.10)": re.compile(r"\b(?:kudanga|kut[ée])\b", re.I),
    "-naiki (retirado)": re.compile(r"-naiki\b", re.I),
}
KA = re.compile(rf"(?<![\w-])ka-({W})", re.I)
MA = re.compile(rf"(?<![\w-])ma-({W})", re.I)

print("estativos del lexicón:", estativos)
print()
cab = f"{'':32}" + "".join(f"{n:>20}" for n in CADENAS)
print(cab)
datos = {n: respuestas(ids) for n, ids in CADENAS.items()}
print(f"{'respuestas':32}" + "".join(f"{len(datos[n]):>20}" for n in CADENAS))
for etiqueta, pat in PATRONES.items():
    celdas = []
    for n in CADENAS:
        usos = sum(len(pat.findall(t)) for _, t in datos[n])
        resp = sum(1 for _, t in datos[n] if pat.search(t))
        hablantes = len({a for a, t in datos[n] if pat.search(t)})
        celdas.append(f"{usos}u/{resp}r/{hablantes}h")
    print(f"{etiqueta:32}" + "".join(f"{c:>20}" for c in celdas))
for etiqueta, pat in (("ka- + NOMBRE caquetío (d21.5)", KA), ("ma- + NOMBRE caquetío", MA)):
    celdas = []
    for n in CADENAS:
        usos = sum(1 for _, t in datos[n] for m in pat.findall(t) if m.lower() in nombres_base)
        resp = sum(1 for _, t in datos[n] if any(m.lower() in nombres_base for m in pat.findall(t)))
        hablantes = len({a for a, t in datos[n] if any(m.lower() in nombres_base for m in pat.findall(t))})
        celdas.append(f"{usos}u/{resp}r/{hablantes}h")
    print(f"{etiqueta:32}" + "".join(f"{c:>20}" for c in celdas))
print("\n(u = usos · r = respuestas que lo dicen · h = hablantes distintos)")

# las formas concretas de lo nuevo, en la cadena nueva
from collections import Counter


def token_entero(t, m):
    i, j = m.start(), m.end()
    while i > 0 and (t[i - 1].isalnum() or t[i - 1] in "-"):
        i -= 1
    while j < len(t) and (t[j].isalnum() or t[j] in "-"):
        j += 1
    return t[i:j].lower()


salida = {"poblacion": {n: {"runs": ids, "respuestas": len(datos[n])} for n, ids in CADENAS.items()},
          "leyenda": "usos / respuestas que lo dicen / hablantes distintos — sobre response_text",
          "estativos": estativos, "patrones": {}, "formas_en_la_cadena_nueva": {},
          "ejemplos_literales_de_la_plantilla": {}}
for etiqueta, pat in PATRONES.items():
    salida["patrones"][etiqueta] = {
        n: {"usos": sum(len(pat.findall(t)) for _, t in datos[n]),
            "respuestas": sum(1 for _, t in datos[n] if pat.search(t)),
            "hablantes": len({a for a, t in datos[n] if pat.search(t)})} for n in CADENAS}
for etiqueta, pat in (("ka- + NOMBRE caquetío (d21.5)", KA), ("ma- + NOMBRE caquetío", MA)):
    salida["patrones"][etiqueta] = {
        n: {"usos": sum(1 for _, t in datos[n] for m in pat.findall(t) if m.lower() in nombres_base),
            "respuestas": sum(1 for _, t in datos[n]
                              if any(m.lower() in nombres_base for m in pat.findall(t))),
            "hablantes": len({a for a, t in datos[n]
                              if any(m.lower() in nombres_base for m in pat.findall(t))})} for n in CADENAS}
plantillas = L.prompt_reglas_completo() + "\n" + L.prompt_reglas_breve()
for etiqueta in ("u- (no-poseído, d21.13)", "-bakoa (d21.14)", "estativo + aspecto (d21.4)"):
    c = Counter()
    for n in ("NUEVA · escena", "NUEVA · control"):
        for _, t in datos[n]:
            for m in PATRONES[etiqueta].finditer(t):
                c[token_entero(t, m)] += 1
    print(f"\n{etiqueta} — formas en la cadena nueva: {c.most_common(12)}")
    salida["formas_en_la_cadena_nueva"][etiqueta] = {
        "formas_distintas": len(c), "usos": sum(c.values()), "top": dict(c.most_common(15))}
    eco = {f: k for f, k in c.items() if re.search(rf"(?<![\w-]){re.escape(f)}(?![\w-])", plantillas)}
    salida["ejemplos_literales_de_la_plantilla"][etiqueta] = {
        "formas": eco, "usos": sum(eco.values()),
        "pct_de_los_usos": round(100 * sum(eco.values()) / (sum(c.values()) or 1), 1)}
    print(f"   de ellas son EJEMPLO LITERAL de la plantilla: {eco} "
          f"({salida['ejemplos_literales_de_la_plantilla'][etiqueta]['pct_de_los_usos']} % de los usos)")

if "--yaml" in sys.argv:
    import yaml
    destino = os.path.normpath(os.path.join(SIM, "..", "6-fusion",
                                            "medicion_tanda_21_en_la_boca_2026-09-21.yaml"))
    with io.open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write("# GENERADO por 6-fusion/scripts/medir_tanda_en_la_boca.py --yaml — no se edita a mano.\n")
        yaml.safe_dump(salida, f, allow_unicode=True, sort_keys=False, width=100)
    print("\nescrito:", destino)
