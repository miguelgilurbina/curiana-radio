#!/usr/bin/env python3
"""¿Tiene `3-mundo/corpus/ecologia.yaml` todos los animales y plantas que el
proyecto tiene registrados? Y de ellos, ¿cuáles LLEGAN al agente?

Pregunta de Miguel, 2026-09-22: «¿me confirmas si ecología tiene acceso a todos
los animales y plantas que tenemos registrados?» — hecha a propósito de la
tarántula azul, que él propone como uno de los primeros referentes a nombrar.

Qué mide, por registro:
  (a) el lexicón: entradas de capa caquetía (las cuatro) cuya glosa es fauna o
      flora — por `categoria` o por la glosa (palabras de fauna/flora, o un
      binomio latino entre paréntesis) —, y cuántas tiene ecología (la clave es
      `palabra_lexicon` de un hecho, o aparece en su texto);
  (b) el canon de sitios de la era 2 (`6-fusion/sitios_era2.yaml`): los datos de
      los dominios de monte, pesca, recolección y materiales, y cuántos citan un
      hecho de ecología en `apoyo_en_repo`;
  (c) el dictado de Medina Colina (`6-fusion/medina_colina_dictado.yaml`):
      las entradas cuyo campo es fauna o flora, y cuántas tiene ecología;
  (d) y lo que llega al agente: [Tu tierra] sale del canon de sitios, no de
      ecología; ecología entra al prompt sólo por las restricciones del Director.

Es una medición por palabras clave: sirve para ver el orden de magnitud y la
lista, no para contar especies. Uso:

    python 6-fusion/scripts/medir_fauna_flora.py [--yaml]
"""
import io
import os
import re
import sys

import yaml

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))

FAUNA = r"\b(animal|p[aá]jaro|\bave\b|aves|pez\b|peces|pescado|tortuga|venado|culebra|serpiente|boa|iguana|lagart|mono\b|cangrejo|caracol|concha|molusco|insecto|hormiga|abeja|avispa|ara[ñn]a|tar[aá]ntula|alacr[aá]n|escorpi|mariposa|murci[eé]lago|conejo|zorro|rata|rat[oó]n|sapo|rana|garza|loro|perico|guacharaca|paloma|gavil[aá]n|zamuro|pel[ií]cano|flamenco|tiburón|raya\b|delf[ií]n|ballena|manat|jaguar|tigre|puma|cachicamo|armadillo|zarig[uü]eya|rabipelado|lombriz|gusano|mosca|mosquito|chivo|langosta|camar[oó]n|ostra|pulpo|lisa\b|sardina|bagre|jurel|mero)"
FLORA = r"\b(planta\b|plantas|[aá]rbol|arbusto|hierba|yerba|cactus|card[oó]n|tuna\b|cuj[ií]|palma|bejuco|flor\b|fruta|fruto|semilla|ra[ií]z comestible|yuca|ma[ií]z|batata|auyama|ají\b|aj[ií]\b|frijol|caraota|algod[oó]n|tabaco|mangle|dividivi|yabo|guayac[aá]n|madera|resina|hoja\b|corteza|le[ñn]a|agave|maguey|cocuy|totuma|calabaza|onoto|bixa)"
BINOMIO = r"\(([A-Z][a-z]+ [a-z]{3,})"
CAPAS = ("caquetío-atestiguado", "caquetío-reconstruido", "caquetío-retroabstraido", "caquetío-hipotético")


def clase(texto: str, categoria: str = "") -> str | None:
    c = (categoria or "").lower()
    if c in ("fauna", "animales"):
        return "fauna"
    if c in ("flora", "plantas"):
        return "flora"
    if re.search(r"\bcolor\b|\bsembrar\b|\bcorral\b", texto, re.I):
        return None
    if re.search(FAUNA, texto, re.I):
        return "fauna"
    if re.search(FLORA, texto, re.I) or re.search(BINOMIO, texto):
        return "flora"
    return None


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = argv or sys.argv[1:]
    import curiana_lexicon as L

    eco = yaml.safe_load(io.open(os.path.join(R, "3-mundo", "corpus", "ecologia.yaml"), encoding="utf-8"))
    hechos = (eco.get("entradas") or []) + (eco.get("huecos_lexicos") or [])
    texto_eco = "\n".join(yaml.safe_dump(h, allow_unicode=True) for h in hechos).lower()
    en_eco_pl = {str(h.get("palabra_lexicon")).lower() for h in hechos if h.get("palabra_lexicon")}
    eco_ids = {h.get("id") for h in hechos}
    eco_fauna_flora = [h.get("id") for h in hechos
                       if set(h.get("dominios") or []) & {"fauna", "flora", "pesca", "manglar"}]

    def en_ecologia(*formas):
        for f in formas:
            f = (f or "").lower().strip()
            if not f:
                continue
            if f in en_eco_pl or re.search(rf"(?<![\w-]){re.escape(f)}(?![\w-])", texto_eco):
                return True
        return False

    # (a) el lexicón
    lex = {"fauna": [], "flora": []}
    for k, v in L.VOCABULARIO_BASE.items():
        if v.get("fuente") not in CAPAS:
            continue
        glosa = str(v.get("sig") or v.get("es") or "")
        c = clase(glosa, str(v.get("categoria") or ""))
        if c:
            lex[c].append({"clave": k, "capa": v.get("fuente"), "glosa": glosa[:80],
                           "en_ecologia": en_ecologia(k, v.get("forma_fuente"))})

    # (b) el canon de sitios
    sitios = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "sitios_era2.yaml"), encoding="utf-8"))
    datos_sitios = []
    for s in sitios.get("sitios") or []:
        for dom, lineas in (s.get("dominios") or {}).items():
            if dom not in ("monte_y_caza", "mar_y_pesca", "recoleccion", "materiales", "tierra"):
                continue
            for l in lineas or []:
                t = str(l.get("dato", ""))
                if not clase(t):
                    continue
                apoyo = [a for a in (l.get("apoyo_en_repo") or []) if a in eco_ids]
                datos_sitios.append({"sitio": s.get("sitio"), "dominio": dom, "dato": re.sub(r"\s+", " ", t)[:110],
                                     "cita_ecologia": apoyo})

    # (c) Medina
    med = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "medina_colina_dictado.yaml"), encoding="utf-8"))
    medina = []
    for e in (med.get("entradas") or []):
        campo = str(e.get("campo") or "")
        if re.search(r"fauna|flora|planta|animal|pesca|ave|\bpez", campo, re.I):
            medina.append({"voz": e.get("voz"), "campo": campo, "veredicto": e.get("veredicto"),
                           "en_ecologia": en_ecologia(e.get("voz"))})

    res = {
        "medido": "2026-09-22",
        "ecologia": {"hechos": len(hechos), "de_fauna_flora_pesca_manglar": len(eco_fauna_flora),
                     "con_palabra_lexicon": len(en_eco_pl)},
        "lexicon_caquetio": {c: {"total": len(v), "en_ecologia": sum(x["en_ecologia"] for x in v),
                                 "fuera_de_ecologia": [f"{x['clave']} ({x['capa'].split('-')[1]}): {x['glosa']}"
                                                       for x in v if not x["en_ecologia"]]}
                             for c, v in lex.items()},
        "canon_de_sitios": {"datos_de_fauna_flora": len(datos_sitios),
                            "citan_un_hecho_de_ecologia": sum(1 for d in datos_sitios if d["cita_ecologia"]),
                            "sin_hecho_de_ecologia": [f"{d['sitio']}/{d['dominio']}: {d['dato']}"
                                                      for d in datos_sitios if not d["cita_ecologia"]]},
        "medina": {"entradas_fauna_flora": len(medina), "en_ecologia": sum(m["en_ecologia"] for m in medina),
                   "fuera": [f"{m['voz']} ({m['campo']}, {m['veredicto']})" for m in medina if not m["en_ecologia"]]},
        "lo_que_llega_al_agente": (
            "[Tu tierra] sale del canon de SITIOS (6-fusion/sitios_era2.yaml), 1-2 líneas por agente y día, "
            "con prioridad agua > dominio principal > resto; ecología entra al prompt sólo por las tres "
            "restricciones del Director (curiana_mundo.RESTRICCIONES_DEL_DIRECTOR). Un dato de fauna del "
            "dominio monte_y_caza de un sitio sin pesca cae en «resto», y sólo lo lee quien vive allí."),
    }
    print(f"ecología: {res['ecologia']}")
    for c in ("fauna", "flora"):
        x = res["lexicon_caquetio"][c]
        print(f"lexicón caquetío, {c}: {x['total']} · en ecología {x['en_ecologia']} · fuera {len(x['fuera_de_ecologia'])}")
    cs = res["canon_de_sitios"]
    print(f"canon de sitios: {cs['datos_de_fauna_flora']} datos de fauna/flora · citan ecología {cs['citan_un_hecho_de_ecologia']}")
    print(f"Medina: {res['medina']['entradas_fauna_flora']} entradas de fauna/flora · en ecología {res['medina']['en_ecologia']}")
    if "--yaml" in argv:
        dest = os.path.join(R, "6-fusion", "medicion_fauna_flora_2026-09-22.yaml")
        with io.open(dest, "w", encoding="utf-8", newline="\n") as f:
            f.write("# GENERADO por 6-fusion/scripts/medir_fauna_flora.py --yaml — no se edita a mano.\n")
            yaml.safe_dump(res, f, allow_unicode=True, sort_keys=False, width=110)
        print("escrito:", os.path.relpath(dest, R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
