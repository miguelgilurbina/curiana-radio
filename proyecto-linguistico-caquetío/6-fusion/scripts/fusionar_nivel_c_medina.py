# -*- coding: utf-8 -*-
"""Aplica al corpus cultural el fallo de Miguel sobre las 33 voces de nivel C
de Medina Colina (6-fusion/issues-pendientes/fallo-miguel-nivel-C-medina.md).

El fallo se cerró el 2026-09-11 en cuatro tandas: 32 entran como `hipotetico`
(31 del nivel C más `tapirama`, que Miguel añadió de su memoria y resultó
estar en tres fuentes), 1 se descarta (`chamaco`, por el silencio de
Alvarado). Hasta hoy el fallo estaba ESCRITO y no APLICADO.

Dónde va cada una — no se inventa un fichero nuevo:
  flora, fauna, oficio y casa → 3-mundo/corpus/ecologia.yaml, que ya lleva
                                 dominios `oficios`, `ceramica`, `agricultura`
  seretón (folclor)           → 3-mundo/corpus/creencia.yaml

Qué lleva cada hecho:
  - `voz` y la glosa de Medina en `contenido`, con la página del libro;
  - `fuente: hipotetico`, que es el destino que el protocolo §5 declara al
    nivel C y el que el fallo fija — también para tapirama, aunque tenga tres
    fuentes externas: promoverla es decisión aparte, y va anotada;
  - `lectura`: el «por qué C» de la ficha, tal cual;
  - `limite`: Medina describe el siglo XX y la esfera, no Paraguaná sola
    (regla 4 ampliada); nada se proyecta a precontacto sin decisión (regla 3);
  - `palabra_lexicon: null` — ninguna sube al lexicón activo, como dice el fallo.

Idempotente: si el corpus ya lleva la marca, no hace nada.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import yaml

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FALLO = os.path.join(R, "6-fusion", "issues-pendientes", "fallo-miguel-nivel-C-medina.md")
DICTADO = os.path.join(R, "6-fusion", "medina_colina_dictado.yaml")
ECO = os.path.join(R, "3-mundo", "corpus", "ecologia.yaml")
CRE = os.path.join(R, "3-mundo", "corpus", "creencia.yaml")
MARCA = "NIVEL C DE MEDINA COLINA"
DESCARTADAS = {"chamaco"}
TANDA_FIJA = {"machire": 4, "guarupepe": 4}      # falladas en la 4ª, nombradas en la 3ª

# ── 1. las fichas del fallo ──
t = io.open(FALLO, encoding="utf-8").read()
partes = t.split("# FALLO DE MIGUEL")
fichas, campo = {}, None
for m in re.finditer(r"^## (\w[\w y]*) \((\d+)\)|^### (\S+) — p\. (\S+)\n\*(.+?)\*\n\n(Por qué C: .+?)(?=\n\n###|\n\n## |\Z)",
                     partes[0], re.M | re.S):
    if m.group(1):
        campo = m.group(1); continue
    fichas[m.group(3)] = dict(campo=campo, porque=" ".join(m.group(6)[len("Por qué C: "):].split()))
for i, bloque in enumerate(partes[1:], 1):
    for v in fichas:
        if "tanda" not in fichas[v] and re.search(r"`%s`" % re.escape(v), bloque):
            fichas[v]["tanda"] = TANDA_FIJA.get(v, i)

# ── 2. la glosa y la página, del dictado ──
D = yaml.safe_load(io.open(DICTADO, encoding="utf-8"))
voces = {}
def _recoger(nodo):
    if isinstance(nodo, dict):
        if "voz" in nodo and "glosa_libro" in nodo:
            voces[nodo["voz"]] = nodo
        for v in nodo.values(): _recoger(v)
    elif isinstance(nodo, list):
        for v in nodo: _recoger(v)
_recoger(D)

# tapirama: la voz que Miguel añadió; su ficha está en el fallo, no en el nivel C
fichas["tapirama"] = dict(campo="flora", tanda=3, porque=(
    "Añadida por Miguel de su propia memoria y verificada en tres fuentes, ninguna de "
    "ellas Medina: Zavala Reyes 2015 #138 («guaracaro (E): tapirama silvestre»), Esteves "
    "1989 t. 5 s.v. GUARACARO («una tapirama silvestre») y Alvarado 1921 s.v. TAPIRAMO "
    "(«Phaseolus sp., muy usado como legumbre en el país», ref. Gilij I.194). Entra como "
    "hipotético porque el fallo lo fija así para el bloque; promoverla a atestiguada con "
    "esas tres citas es decisión aparte de Miguel."))

faltan = [v for v in fichas if v not in voces and v not in DESCARTADAS]
assert not faltan, f"sin entrada en el dictado: {faltan}"

def limpia(s):
    return " ".join(str(s or "").split())

def hecho(idn, voz, f, d):
    pag = d.get("pagina")
    ref_pag = f"p. {pag}" if pag else "página no dictada (⚠️ pendiente)"
    dom = {"flora": ["ecologia", "flora", "lexico_regional"],
           "fauna": ["ecologia", "fauna", "lexico_regional"],
           "oficio y casa": ["ecologia", "oficios", "cultura_material", "lexico_regional"],
           "otros": ["creencia", "folclor", "lexico_regional"]}[f["campo"]]
    h = {
        "id": idn,
        "voz": voz,
        "contenido": (f"VOZ DEL HABLA PARAGUANERA, nivel C del protocolo: «{voz}» — "
                      f"{limpia(d['glosa_libro'])} (Medina Colina, {ref_pag}; campo: {limpia(d.get('campo'))})."),
        "fuente": "hipotetico",
        "referencia": (f"Medina Colina 2013, Del Habla Paraguanera, {ref_pag} (dictado de Miguel, "
                       f"{d.get('dictado', '2026-09')}); fallo de Miguel del 2026-09-11, tanda {f.get('tanda', '?')} "
                       f"(6-fusion/issues-pendientes/fallo-miguel-nivel-C-medina.md)"),
        "procedencia": {"obra": "medina-colina-sxx", **({"pagina": pag} if pag else {})},
        "dominios": dom,
        "agentes_relacionados": [],
        "palabra_lexicon": None,
        "locacion": None,
        "lectura": f["porque"],
        "limite": ("Medina describe el siglo XX, y lo que recogió en Paraguaná es sedimento de la esfera "
                   "(Kaketiana), no dato exclusivamente paraguanero (regla 4 ampliada, 2026-09-11). No se "
                   "proyecta a precontacto mientras no se decida (regla 3). No sube al lexicón activo."),
    }
    if d.get("identificacion"):
        h["identificacion"] = limpia(d["identificacion"])
    if voz == "seretón":
        h["referencia"] += ("; la mención de Federmann 1530 (Ceretón) y la lectura de tradición oral de Miguel, "
                            "en 6-fusion/ceret_on_hipotesis_miguel.yaml")
    return h

# ── 3. escribir ──
eco_t = io.open(ECO, encoding="utf-8").read()
cre_t = io.open(CRE, encoding="utf-8").read()
if MARCA in eco_t or MARCA in cre_t:
    print("ya aplicado; nada que hacer"); sys.exit(0)

def ultimo_id(texto, prefijo):
    ns = [int(x) for x in re.findall(r"id: %s-(\d+)" % prefijo, texto)]
    return max(ns) if ns else 0

def insertar(texto, prefijo, hechos, titulo):
    """Mete los hechos al FINAL de la lista de `<prefijo>-NNN`, con la sangría
    de esa lista, y antes de cualquier otra clave de nivel 0 que venga después
    (en ecologia.yaml los huecos léxicos cuelgan de otra clave)."""
    lineas = texto.splitlines(True)
    idx = [i for i, l in enumerate(lineas) if re.match(r"^\s*- id: %s-\d+" % prefijo, l)]
    assert idx, f"no hay items {prefijo}-NNN"
    ultimo = idx[-1]
    sangria = len(lineas[ultimo]) - len(lineas[ultimo].lstrip(" "))
    corte = len(lineas)
    for i in range(ultimo + 1, len(lineas)):
        if re.match(r"^[A-Za-z_][\w-]*:\s*(#.*)?$", lineas[i]) or \
           (sangria == 0 and lineas[i].startswith("- ") and not re.match(r"^- id: %s-" % prefijo, lineas[i])):
            corte = i; break
    pad = " " * sangria
    cab = ("\n%s# ── %s — fallo de Miguel 2026-09-11, aplicado 2026-09-12 ──\n"
           "%s# Etiqueta `hipotetico` por protocolo §5. Ver 6-fusion/issues-pendientes/fallo-miguel-nivel-C-medina.md\n"
           % (pad, titulo, pad))
    cuerpo = yaml.safe_dump(hechos, allow_unicode=True, sort_keys=False, width=100, default_flow_style=False)
    cuerpo = "".join(pad + l if l.strip() else l for l in cuerpo.splitlines(True))
    antes = "".join(lineas[:corte]).rstrip("\n") + "\n"
    despues = "".join(lineas[corte:])
    return antes + cab + cuerpo + ("\n" + despues if despues else "")

orden = [v for v in fichas if v not in DESCARTADAS and fichas[v]["campo"] != "otros"]
n_eco = ultimo_id(eco_t, "ecologia")
eco_h = [hecho(f"ecologia-{n_eco + i + 1:03d}", v, fichas[v], voces[v]) for i, v in enumerate(orden)]
n_cre = ultimo_id(cre_t, "creencia")
cre_h = [hecho(f"creencia-{n_cre + 1:03d}", "seretón", fichas["seretón"], voces["seretón"])]

eco_nuevo = insertar(eco_t, "ecologia", eco_h, MARCA + " (flora, fauna, oficio y casa)")
cre_nuevo = insertar(cre_t, "creencia", cre_h, MARCA + " (folclor)")
# que parsee ANTES de escribir, y que las entradas estén donde tienen que estar
for nombre, nuevo, n_esp in (("ecologia", eco_nuevo, len(eco_h)), ("creencia", cre_nuevo, len(cre_h))):
    d = yaml.safe_load(nuevo)
    lista = d["entradas"] if isinstance(d, dict) else d
    ids = [e.get("id") for e in lista]
    assert ids[-n_esp:] == [h["id"] for h in (eco_h if nombre == "ecologia" else cre_h)], f"{nombre}: los hechos no quedaron al final de la lista: {ids[-n_esp-1:]}"
io.open(ECO, "w", encoding="utf-8", newline="\n").write(eco_nuevo)
io.open(CRE, "w", encoding="utf-8", newline="\n").write(cre_nuevo)
print(f"ecologia.yaml: +{len(eco_h)} (ecologia-{n_eco+1:03d}…{n_eco+len(eco_h):03d})   creencia.yaml: +{len(cre_h)} (creencia-{n_cre+1:03d})")
print("descartadas:", sorted(DESCARTADAS), "| sin página:", [v for v in orden if not voces[v].get("pagina")])

# ── 4. dejar dicho en el fallo que ya está aplicado ──
if "Aplicado al corpus el 2026-09-12" not in t:
    t2 = t.replace("## Estado final del bloque\n",
                   "## Estado final del bloque\n\n✅ **Aplicado al corpus el 2026-09-12** por "
                   "`6-fusion/scripts/fusionar_nivel_c_medina.py`: %d hechos en `ecologia.yaml` "
                   "(ecologia-%03d a -%03d) y 1 en `creencia.yaml` (creencia-%03d), todos `hipotetico`.\n"
                   % (len(eco_h), n_eco + 1, n_eco + len(eco_h), n_cre + 1), 1)
    assert t2 != t
    io.open(FALLO, "w", encoding="utf-8", newline="\n").write(t2)
    print("fallo marcado como aplicado")
