# -*- coding: utf-8 -*-
"""La parte del CORPUS de la campaña de la cosmovisión marina (cc.10).

Miguel, 2026-09-24: «Ok a todo, que no quede ninguna tarea pendiente». Se aplica
lo recomendado en 6-fusion/issues-pendientes/cosmovision-marina-2026-09-24.md:

  (c) A — los atestiguados al corpus: cm24-01, -03, -04 a creencia; cm24-05 a
      ecología (comercio); cm24-06 a parentesco; cm24-a01 y -a02 a creencia
      (muerte), acotados; cm24-07 (creencia) y cm24-08 (geografía política)
      como `reconstruido`. cm24-02 NO se añade: es la procedencia de
      creencia-013, y dp.2.07 de #222 ya la escribió (Ampíes p. 212 y Aguado).
  (g) A — las correcciones de cita: creencia-009 (Jahn, impresa 184),
      transmision-018 (Anglería, impresa 228), lx.13 de la Apologética
      («Vagua»), la bitácora de Brinton (Brett 1868, n. 49) y las tres de FA3
      (cm-s3, cm-n3, cm-c3), anotadas en su propuesta.
      Las de `huracan`, `cobo`, `barana` y CULTURA_CAQUETIA §1 ya entraron
      (aplicar_cosmovision_marina_lexicon.py, 11f1fdd).

Cada hecho nuevo lleva en `nota` de qué candidato sale; el `procedencia` del
corpus es un dict, así que va la primera obra y todas en `referencia`; la época
y la polity del candidato van en `limite` (geografía política tiene campos
propios). Idempotente; `--dry-run` no escribe.
"""
import argparse
import os
import sys

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
C = os.path.join(R, "3-mundo", "corpus")
PROP = os.path.join(R, "6-fusion", "cosmovision_marina_2026-09-24.yaml")
HUELLA = "cc.10 (c) A, cosmovisión marina («Ok a todo», Miguel, 2026-09-24)"
ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
ARGS = ap.parse_args()

P = yaml.safe_load(open(PROP, encoding="utf-8"))
CAND = {x["id"]: x for x in P["hechos_candidatos"] + P["arqueologia"]}
DESTINO = {"cm24-01": "creencia", "cm24-03": "creencia", "cm24-04": "creencia",
           "cm24-a01": "creencia", "cm24-a02": "creencia", "cm24-07": "creencia",
           "cm24-05": "ecologia", "cm24-06": "parentesco", "cm24-08": "geografia_politica"}
ORDEN = ["id", "contenido", "fuente", "referencia", "procedencia", "dominios",
         "agentes_relacionados", "epoca", "polity", "implicacion_simulacion", "lectura",
         "limite", "nota"]
escrito = {}


def leer(nombre):
    p = os.path.normpath(os.path.join(C, nombre + ".yaml"))
    b = open(p, "rb").read().decode("utf-8")
    eol = "\r\n" if "\r\n" in b else "\n"
    return p, b.replace(eol, "\n"), eol


def ref(p):
    pag = p.get("pagina")
    return p["obra"] + (f", p. {pag}" if pag not in (None, "") else "")


def a_corpus(cid, destino, nuevo_id):
    x = CAND[cid]
    procs = x["procedencia"] if isinstance(x["procedencia"], list) else [x["procedencia"]]
    e = {"id": nuevo_id, "contenido": x["contenido"], "fuente": x["fuente"],
         "referencia": "; ".join(ref(p) for p in procs),
         "procedencia": dict(procs[0]), "dominios": list(x.get("dominios", [])),
         "agentes_relacionados": []}
    for k in ("implicacion_simulacion", "lectura"):
        if x.get(k):
            e[k] = x[k]
    if destino == "geografia_politica":
        e["epoca"] = x.get("epoca")
        e["polity"] = "costera"
        e["limite"] = f"polity del candidato: {x.get('polity')}"
    else:
        e["limite"] = f"Época: {x.get('epoca')}. Polity: {x.get('polity')}."
    if x.get("restringido"):
        e["limite"] += " Restringido (el candidato lo marca: saber de boratio o de señor)."
    e["nota"] = f"Fusionado de 6-fusion/cosmovision_marina_2026-09-24.yaml `{cid}` por {HUELLA}"
    return {k: e[k] for k in ORDEN if k in e}


def bloque(e, sangria):
    s = yaml.safe_dump(e, allow_unicode=True, sort_keys=False, width=110, default_flow_style=False)
    ls = s.rstrip("\n").split("\n")
    return "\n".join([sangria + "- " + ls[0]] + [sangria + "  " + x for x in ls[1:]])


textos = {}
for destino in sorted(set(DESTINO.values())):
    p, t, eol = leer(destino)
    d = yaml.safe_load(t)
    hs = d if isinstance(d, list) else d["entradas"]
    if any("cosmovision_marina_2026-09-24.yaml `cm24-" in " ".join(str(h.get("nota", "")).split()) for h in hs):
        print(f"  {destino}: ya aplicado")
        continue
    pref = hs[0]["id"].rsplit("-", 1)[0]
    libre = max(int(h["id"].rsplit("-", 1)[1]) for h in hs if h["id"].rsplit("-", 1)[1].isdigit()) + 1
    nuevos = []
    for cid in [c for c in DESTINO if DESTINO[c] == destino]:
        e = a_corpus(cid, destino, f"{pref}-{libre:03d}")
        libre += 1
        nuevos.append(e)
        print(f"  + {e['id']}  ({e['fuente']})  ← {cid}")
    if destino == "ecologia":
        corte = t.index("\nhuecos_lexicos:")
        t = t[:corte].rstrip("\n") + "\n" + "\n".join(bloque(e, "  ") for e in nuevos) + "\n" + t[corte:]
    else:
        t = t.rstrip("\n") + "\n" + "\n".join(bloque(e, "") for e in nuevos) + "\n"
    yaml.safe_load(t)
    textos[p] = (t, eol)


# ── (g) las correcciones de cita ────────────────────────────────────────
def corregir(ruta, viejo, nuevo, marca):
    p = os.path.normpath(os.path.join(R, ruta))
    t, eol = textos.get(p) or leer_crudo(p)
    if marca in t:
        return
    assert t.count(viejo) == 1, (ruta, viejo[:50], t.count(viejo))
    textos[p] = (t.replace(viejo, nuevo), eol)
    print(f"  · {ruta}")


def leer_crudo(p):
    b = open(p, "rb").read().decode("utf-8")
    eol = "\r\n" if "\r\n" in b else "\n"
    return b.replace(eol, "\n"), eol


G = "(cc.10 (g) A, 2026-09-24)"
corregir("3-mundo/corpus/creencia.yaml",
         '  referencia: "Paz Reverol 2018; Jahn 1927:229 (Jepira/Cabo de la Vela, guajiro)"\n',
         '  referencia: "Paz Reverol 2018; Jahn 1927 p. 184 (Jepira/Cabo de la Vela, guajiro; decía «1927:229», '
         f'que es la página del PDF) {G}"\n'
         "  procedencia: {obra: jahn-1927, pagina: '184'}\n"
         '  aviso: "En Jahn Jepira es el Cabo de la Vela por donde el alma PASA hacia «espléndidas sabanas»; la '
         '«pesca» del más allá no está en Jahn (6-fusion/cosmovision_marina_2026-09-24.yaml cm24-c-w02). ' + G + '"\n',
         "Jahn 1927 p. 184 (Jepira")
corregir("3-mundo/corpus/transmision.yaml",
         '  referencia: "Anglería, Fuentes Históricas sobre Colón y América (1892 [c.1530]), vol. 4, p. 236"\n'
         "  procedencia: {obra: angleria-1892}\n",
         '  referencia: "Anglería, Fuentes Históricas sobre Colón y América (1892 [c.1530]), vol. 4, p. 228 (impresa; '
         f'decía «p. 236», que es la del PDF) {G}"\n'
         "  procedencia: {obra: angleria-1892, pagina: '228'}\n",
         "vol. 4, p. 228 (impresa")
corregir("4-fuentes/brinton-1871.md",
         "(lokono de Guayana, s. XIX; Brinton no dice de qué misionero\nlo toma)",
         "(lokono de Guayana, s. XIX; lo toma de Brett, *Indian Tribes of Guiana*, 1868:\n"
         f"lo dice en la nota 49 de la p. 18 — antes esta línea decía que no lo decía {G})",
         "lo toma de Brett")
corregir("6-fusion/taino2_las_casas_apologetica.yaml",
         "  forma_fuente: Yocahu Yagua Maorocotí",
         f"  forma_fuente: Yocahu Vagua Maorocotí  # la imagen de la p. 321 dice «Vagua»; «Yagua» era la capa de texto {G}",
         "Yocahu Vagua Maorocotí  #")

# FA3: las tres correcciones, anotadas en su propuesta
FA3 = "6-fusion/fauna_paraguana_mar_2026-09-22.yaml"
for cid, texto in [
    ("cm-s3", "«viciosos de comida de carne y pescado» es de los caquetíos de los LLANOS (Pérez de Tolosa en "
              "Fernández Duro 1885 t. II p. 234; Arcaya p. 46); las otras dos citas sí son de la costa"),
    ("cm-n3", "en Las Aves la espira agujereada es para sacar la carne (cm24-a05): lo que subiría la bocina es "
              "un ápice cortado y pulido como embocadura, fuera de contexto alimentario"),
    ("cm-c3", "no es atestiguado: en el repo descansa en una tesis que lo cita de terceros y Pulowi sale 0 veces "
              "en Jahn y en el Cuadernillo; es `reconstruido` como mucho (cm24-c-w01)"),
]:
    p = os.path.normpath(os.path.join(R, FA3))
    t, eol = textos.get(p) or leer_crudo(p)
    linea = f"    - id: {cid}\n"
    if f"corregido_cc10: " in t[t.index(linea):t.index(linea) + 4000].split("\n    - id: ")[0]:
        continue
    i = t.index(linea) + len(linea)
    t = t[:i] + "      corregido_cc10: " + yaml.safe_dump(
        f"CORREGIDO {G}: " + texto, allow_unicode=True, width=10**6).strip().removesuffix("...").strip() + "\n" + t[i:]
    textos[p] = (t, eol)
    print(f"  · {FA3} {cid}")
yaml.safe_load((textos.get(os.path.normpath(os.path.join(R, FA3))) or ("{}",))[0])

if ARGS.dry_run:
    print("--dry-run: no se escribe")
    sys.exit(0)
for p, (t, eol) in textos.items():
    open(p, "wb").write(t.replace("\n", eol).encode("utf-8"))
print(f"✓ {len(textos)} archivos")
