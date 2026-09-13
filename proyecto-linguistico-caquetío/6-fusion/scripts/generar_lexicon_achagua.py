# -*- coding: utf-8 -*-
"""Genera curiana_sim/lexicon_achagua.py desde 6-fusion/achagua_neira_ribero_1762.yaml.

Miguel, 2026-09-13: «Fusionemos lo que conseguimos achagua». El achagua entra
como COMPARANDA (`fuente: achagua`), como el lokono de Perea y la columna A-2:
vocabulario de comparación, no habla de agentes (el muestreador del prompt
filtra por familia caquetía). Se funde con setdefault, como lexicon_zavala y
lexicon_a2: jamás pisa una clave existente.

Qué entra: el vocabulario castellano→achagua de Neira y Ribero 1762 (la copia
de 1788), los pronombres absolutos del arte, y las entradas con forma de las
«Noticias» del arte (pliegos 23-27). NO entra Fabo 1911: sus tablas son de
segunda mano y con un error medido (agua); quedan como control en
6-fusion/achagua_fabo_1911.yaml.

Clave: la primera forma achagua de la entrada, en minúscula, con dos
normalizaciones de la grafía del copista, y sólo esas dos:
  - V inicial ante consonante = u vocálica («Vni» → uni, «Vregirrayi» → uregirrayi);
  - J inicial ante consonante = i («Jba» → iba).
La grafía del copista se conserva entera en `forma_fuente`. Las variantes
(«Nuisayuba, vel Nuisaiyu») van a `notas`. Si la misma clave sale de varias
entradas castellanas, se funden en una con «(y N acepciones más)».

Homógrafos: si la clave ya existe en VOCABULARIO_BASE, o es palabra española,
o tiene dos letras o menos, entra como `<clave>-achagua` (precedente
`kati-kalinago`, `awa-lokono`): score_linguistico() cuenta como arahuaco
cualquier token igual a una clave y no filtra por fuente.

Toda forma es TRANSCRIPCIÓN POR VISIÓN (dos pasadas del escriba de Opus 5,
2026-09-12): cada `notas` lo dice, y las 38 con corchete de duda llevan
`duda de lectura`. Verificar en imagen antes de citar una forma como exacta.

Regenerable: corrige el YAML y vuelve a correr. No edites el módulo a mano.
"""
import io, json, os, re, sys, yaml
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL

Y = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "achagua_neira_ribero_1762.yaml"), encoding="utf-8"))
V = CL.VOCABULARIO_BASE
ES = {r.lower() for r in CL.RAICES_ESPANOLAS} | set(CL.ES_STOPWORDS) | {
    "casa", "cara", "cama", "capa", "cata", "cana", "mana", "mata", "masa", "misa", "nada", "nena", "pena", "pata",
    "rata", "rima", "sana", "tara", "tela", "tema", "toca", "bata", "bala", "cera", "cita", "coca", "cuna", "dama",
    "duna", "era", "gana", "hora", "isla", "lana", "lata", "loca", "luna", "mesa", "mina", "moda", "mora", "nota",
    "ola", "oro", "para", "pasa", "pesa", "pila", "puma", "pura", "rana", "risa", "roca", "ropa", "rosa", "sala",
    "seca", "seda", "sola", "sopa", "suma", "tapa", "taza", "tira", "toma", "tuna", "una", "uva", "vaca", "vela",
    "vida", "vino", "yema", "zona"}
INF = re.compile(r"^[a-záéíóúñ]{3,}(ar|er|ir)(se|me|le|lo|la)?$")
NUM = {"vno", "vna", "uno", "una", "dos", "tres", "quatro", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
       "diez", "once", "doce", "trece", "catorce", "quince", "veinte", "treinta", "quarenta", "cincuenta", "sesenta",
       "ochenta", "ciento", "cien", "mil", "docientos", "doscientos"}


def clave_de(forma):
    f = re.sub(r"[\[\]]", "", forma).strip().strip(".;:,").lower()
    f = re.sub(r"\s+", " ", f)
    f = re.sub(r"^v(?=[^aeiouáéíóúy\s])", "u", f)
    f = re.sub(r"^j(?=[^aeiouáéíóú\s])", "i", f)
    return f


def formas_de(texto):
    partes = re.split(r"\s*,\s*|\s+vel\s+|\s*;\s*|\s+ó\s+|\s+o\s+", str(texto))
    return [p.strip() for p in partes if p and p.strip()]


def limpio(s):
    return " ".join(str(s or "").replace('"', "'").split())


def categoria(castellano, tipo):
    if tipo == "pron":
        return "pron"
    c = limpio(castellano).lower().rstrip(".").split(",")[0].strip()
    if c in NUM or c.split(" ")[0] in NUM:
        return "num"
    if INF.match(c.split(" ")[0]):
        return "v_raiz"
    return "sust"


acepciones = {}          # clave -> lista de dicts
orden = []

def registrar(forma_texto, castellano, pliego, lado, extra, tipo="voc"):
    formas = formas_de(forma_texto)
    if not formas:
        return
    principal = formas[0]
    clave = clave_de(principal)
    if not clave:
        return
    a = {"castellano": limpio(castellano), "forma": limpio(principal), "variantes": [limpio(x) for x in formas[1:]],
         "pliego": pliego, "lado": lado, "duda": "[" in str(forma_texto), "tipo": tipo, **extra}
    if clave not in acepciones:
        acepciones[clave] = []; orden.append(clave)
    acepciones[clave].append(a)

for e in Y["vocabulario"]:
    registrar(e.get("achagua"), e.get("castellano"), e.get("pliego"), e.get("lado"),
              {k: limpio(e[k]) for k in ("ejemplo", "nota") if e.get(k)})

for pf in Y["arte"]["pronombres"]["absolutos"].get("formas", []):
    registrar(pf.get("forma"), pf.get("castellano"), pf.get("pliego"), pf.get("lado"),
              {"nota": f"pronombre absoluto, {pf.get('persona')}; variante {pf.get('variante')}"}, tipo="pron")

def walk(nodo, seccion=""):
    if isinstance(nodo, dict):
        if "castellano" in nodo and "achagua" in nodo:
            registrar(nodo["achagua"], nodo["castellano"], nodo.get("pliego"), nodo.get("lado"),
                      {k: limpio(nodo[k]) for k in ("ejemplo", "nota", "seccion") if nodo.get(k)} | ({"seccion": seccion} if seccion and not nodo.get("seccion") else {}),
                      tipo="arte")
            return
        for k, v in nodo.items():
            walk(v, k if isinstance(v, (list, dict)) and k not in ("fuente",) else seccion)
    elif isinstance(nodo, list):
        for v in nodo:
            walk(v, seccion)
walk(Y["arte"]["verbos"])

# ── el módulo ──
lineas = []
homografos = []
for clave in orden:
    acs = acepciones[clave]
    princ = acs[0]
    cat = categoria(princ["castellano"], princ["tipo"])
    sig = princ["castellano"]
    if len(acs) > 1:
        sig += f" (y {len(acs) - 1} acepción/es más)"
    k = clave
    pelada = k.split(" ")[0]
    if k in V or (" " not in k and (k in ES or len(k) <= 2)):
        k = clave + "-achagua"; homografos.append(clave)
    notas = (f"Neira y Ribero 1762 (copia de 1788, Real Biblioteca II/2910), vocabulario castellano→achagua"
             f"{' — arte' if princ['tipo'] == 'arte' else ''}: pliego {princ['pliego']} {princ['lado']}, s.v. «{princ['castellano']}».")
    if princ["variantes"]:
        notas += " Variantes en la misma entrada: " + ", ".join(princ["variantes"]) + "."
    if princ.get("ejemplo"):
        notas += f" Ejemplo: {princ['ejemplo']}."
    if princ.get("nota"):
        notas += f" Nota del escriba: {princ['nota']}."
    if princ.get("seccion"):
        notas += f" Sección del arte: {princ['seccion']}."
    if len(acs) > 1:
        notas += " Otras acepciones: " + "; ".join(f"«{a['castellano']}» (pl. {a['pliego']} {a['lado']}{', forma ' + a['forma'] if a['forma'].lower() != princ['forma'].lower() else ''})" for a in acs[1:8]) + "."
    if any(a["duda"] for a in acs):
        notas += " ⚠️ Duda de lectura marcada con corchetes en la transcripción."
    if k != clave:
        notas += f" Clave desambiguada como `{k}` (homógrafo de una clave existente o de una palabra española)."
    notas += (" Transcripción por VISIÓN (escriba Opus 5, dos pasadas, 2026-09-12): verificar en imagen antes de citar la forma como exacta."
              " Clave = forma del copista en minúscula, con V/J iniciales ante consonante leídas como u/i. Comparanda achagua, fase 2 de D11 (#121); fusión 2026-09-13.")
    entrada = {"sig": sig, "cat": cat, "fuente": "achagua", "forma_fuente": princ["forma"], "notas": notas}
    lineas.append(f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(entrada, ensure_ascii=False)},")

cab = f'''# -*- coding: utf-8 -*-
"""
lexicon_achagua.py — comparanda ACHAGUA de Neira y Ribero 1762.

GENERADO por 6-fusion/scripts/generar_lexicon_achagua.py desde
6-fusion/achagua_neira_ribero_1762.yaml. No se edita a mano: se corrige el
YAML (que es la transcripción, verificable pliego a pliego) y se regenera.

Lo importa curiana_lexicon con setdefault, como lexicon_zavala y lexicon_a2:
jamás pisa una clave existente. Es vocabulario de COMPARACIÓN (fase 2 de D11,
#121), no habla de agentes: el muestreador del prompt filtra por familia
caquetía. Toda forma es transcripción por visión: cada `notas` lo dice.

Medido al generar: {len(orden)} claves de {len(Y['vocabulario'])} entradas del
vocabulario + pronombres + noticias del arte; {len(homografos)} desambiguadas
con `-achagua`.
"""

OBRA = "neira-ribero-1762"
LENGUA = "achagua"

COMPARANDA_ACHAGUA: dict[str, dict] = {{
'''
cuerpo = "\n".join(lineas) + "\n}\n\n"
cuerpo += "HOMOGRAFOS_ACHAGUA = " + json.dumps(homografos, ensure_ascii=False) + "\n"
dest = os.path.join(R, "curiana_sim", "lexicon_achagua.py")
io.open(dest, "w", encoding="utf-8", newline="\n").write(cab + cuerpo)
print(f"claves: {len(orden)} · homógrafas: {len(homografos)} · entradas del vocabulario: {len(Y['vocabulario'])}")
from collections import Counter
print("cat:", Counter(categoria(acepciones[k][0]["castellano"], acepciones[k][0]["tipo"]) for k in orden))
print("con espacio:", sum(1 for k in orden if " " in k), "| con duda:", sum(1 for k in orden if any(a["duda"] for a in acepciones[k])))
print("muestra:", orden[:8])
