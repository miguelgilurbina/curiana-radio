#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — cruzar una voz contra el canon (la herramienta del escriba)
=====================================================================

Para la sesión de dictado de Medina Colina (*Del Habla Paraguanera*, 2013) y
cualquier voz regional que haya que juzgar por el protocolo del habla
paraguanera (02_protocolo_habla_paraguanera §3-5): antes de opinar, mirar qué
dice el canon. Responde en segundos las preguntas del protocolo que SÍ se
pueden automatizar:

    ¿ya está en el lexicón? (y con qué fuente: si es wayunaiki, filtro 3)
    ¿hay cognado registrado?            2-lengua/cognados.yaml
    ¿aparece en topónimos?              2-lengua/toponimos.yaml + cola de Esteves
    ¿está en la columna añú o lokono?   lexicon_a2 (Tabla A-2 de Oliver)
    ¿el caquetío ya tiene palabra para ese referente?   --glosa
    ¿viola la fonotáctica atestiguada?  filtro NEGATIVO (débil en positivo)

Los filtros 1 y 2 del protocolo (andalucismo/canarismo/venezolanismo general;
papiamento/neerlandés) NO se automatizan: son juicio, y son de Miguel.

Compara por esqueleto fonémico (`curiana_fonotactica.fonemizar`, con gu→w),
así `guaca` casa con `waka` y `cuiva` con `kiba`; y con parecido difuso (≈)
para no perder `cardón`~`kardon`. Un cero aquí mide la consulta, no la fuente
(regla 6): si una voz no casa, probar variantes antes de decir «no está».

Uso:
    python cruzar_voz.py medano
    python cruzar_voz.py cardon --glosa "cactus columnar"
    python cruzar_voz.py biro tara bacoa            # varias de una vez
"""

import argparse
import difflib
import io
import os
import re
import sys
import unicodedata

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

from curiana_fonotactica import Fonotactica, fonemizar, _grupos_del_lexicon  # noqa: E402

UMBRAL_DIFUSO = 0.80
_STOP = set("de del la el los las un una y o en con por para que se al lo su "
            "sus es son como muy mas más tipo especie".split())


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def clave(forma: str) -> str:
    """Esqueleto fonémico comparable. gu→w activado: es medición, no decisión."""
    return fonemizar(forma, gu_es_w=True)


def _sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", (s or "").lower())
                   if unicodedata.category(c) != "Mn")


def parecido(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def _grado(ka: str, kb: str) -> str | None:
    """'=' si casan, '≈' si se parecen, None si no."""
    if not ka or not kb:
        return None
    if ka == kb:
        return "="
    if min(len(ka), len(kb)) >= 4 and parecido(ka, kb) >= UMBRAL_DIFUSO:
        return "≈"
    return None


def _formas_de(valor) -> list[str]:
    """Un campo de cognado puede traer '*p-/b-ali-', 'a / b', 'x, y'."""
    if not isinstance(valor, str):
        return []
    out = []
    for trozo in re.split(r"[/,;]", valor):
        t = trozo.strip().strip("*").strip("-").strip()
        if t and not t.startswith("("):
            out.append(t)
    return out


# ══════════════════════════════════════════════════════════════════════
# CARGA DEL CANON
# ══════════════════════════════════════════════════════════════════════

def _yaml(rel: str):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return yaml.safe_load(f)


def _strings(obj) -> list[str]:
    """Todas las formas (str o dict['forma']) de una estructura anidada."""
    out = []
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        if isinstance(obj.get("forma"), str):
            out.append(obj["forma"])
        else:
            for v in obj.values():
                out += _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            out += _strings(v)
    return out


def cargar() -> dict:
    from curiana_lexicon import VOCABULARIO_BASE
    from lexicon_a2 import PARAUJANO_A2, LOKONO_A2

    canon = {"lexicon": VOCABULARIO_BASE, "paraujano": PARAUJANO_A2,
             "lokono": LOKONO_A2}
    canon["cognados"] = _yaml("2-lengua/cognados.yaml").get("cognados", [])
    canon["toponimos"] = _yaml("2-lengua/toponimos.yaml").get("toponimos", [])
    est = _yaml("6-fusion/toponimos_esteves_indice.yaml")
    canon["esteves"] = sorted({s for k, v in est.items() if k != "meta"
                               for s in _strings(v)})
    grupos = _grupos_del_lexicon()
    canon["fono"] = Fonotactica(grupos.get("caquetío atestiguado", []), gu_es_w=True)
    return canon


# ══════════════════════════════════════════════════════════════════════
# EL CRUCE
# ══════════════════════════════════════════════════════════════════════

def cruzar(voz: str, canon: dict, glosa: str | None = None) -> dict:
    k = clave(voz)
    r = {"voz": voz, "clave": k, "lexicon": [], "por_glosa": [], "cognados": [],
         "toponimos": [], "esteves": [], "paraujano": [], "lokono": []}

    # 1. lexicón activo — por forma, por forma_fuente
    for forma, e in canon["lexicon"].items():
        candidatas = [forma] + _formas_de(e.get("forma_fuente", ""))
        g = None
        for c in candidatas:
            g = _grado(k, clave(c))
            if g:
                break
        if g:
            r["lexicon"].append((g, forma, e.get("sig", ""), e.get("fuente", ""),
                                 e.get("forma_fuente", "")))

    # 2. ¿el caquetío ya tiene palabra para ese referente?
    if glosa:
        palabras = [w for w in re.findall(r"[a-záéíóúüñ]{4,}", glosa.lower())
                    if w not in _STOP]
        # Palabra entera (con hasta dos letras de flexión): «cara» no debe
        # traer caracol ni caracara.
        patrones = [re.compile(r"\b" + re.escape(_sin_tildes(w)) + r"\w{0,2}\b")
                    for w in palabras]
        for forma, e in canon["lexicon"].items():
            sig = _sin_tildes(e.get("sig", ""))
            if any(p.search(sig) for p in patrones):
                r["por_glosa"].append((forma, e.get("sig", ""), e.get("fuente", "")))

    # 3. cognados
    for c in canon["cognados"]:
        for lengua, valor in (c.get("formas") or {}).items():
            for f in _formas_de(valor):
                g = _grado(k, clave(f))
                if g:
                    r["cognados"].append((g, c.get("id"), lengua, f, c.get("glosa", "")))

    # 4. topónimos del canon — forma entera, o como morfema dentro
    for t in canon["toponimos"]:
        kt = clave(t.get("forma", ""))
        g = _grado(k, kt)
        if not g and len(k) >= 3 and k in kt:
            g = "⊂"
        if not g:
            for m in (t.get("morfemas") or {}):
                if _grado(k, clave(m)) == "=":
                    g = "morfema"
                    break
        if g:
            r["toponimos"].append((g, t.get("id"), t.get("forma"), t.get("nivel"),
                                   t.get("glosa_fuente", "")))

    # 5. la cola de Esteves (186 nombres sin glosa: solo respaldo toponímico)
    for nombre in canon["esteves"]:
        kn = clave(nombre)
        g = _grado(k, kn)
        if not g and len(k) >= 4 and (k in kn or kn in k):
            g = "⊂"
        if g:
            r["esteves"].append((g, nombre))

    # 6. columnas añú y lokono de la A-2
    for col in ("paraujano", "lokono"):
        for forma, e in canon[col].items():
            g = _grado(k, clave(forma))
            if g:
                r[col].append((g, forma, e.get("sig", "")))

    # 7. fonotáctica (filtro negativo)
    ok, motivos = canon["fono"].valida(voz)
    r["fono"] = (ok, motivos)
    return r


def imprimir(r: dict) -> None:
    print(f"\n━━ {r['voz']}  ⟨{r['clave']}⟩ " + "━" * max(0, 50 - len(r['voz'])))
    def bloque(titulo, filas, fmt):
        print(f"  {titulo}: " + ("—" if not filas else ""))
        for fila in filas[:10]:
            print("     " + fmt(fila))
        if len(filas) > 10:
            print(f"     … y {len(filas) - 10} más")
    bloque("lexicón", r["lexicon"],
           lambda f: f"{f[0]} {f[1]:16} {f[2][:44]:46} [{f[3]}]"
                     + (f" ←{f[4]}" if f[4] else ""))
    if r["por_glosa"]:
        bloque("mismo referente (por glosa)", r["por_glosa"],
               lambda f: f"  {f[0]:16} {f[1][:44]:46} [{f[2]}]")
    bloque("cognados", r["cognados"],
           lambda f: f"{f[0]} {f[1]}  {f[2]}: {f[3]:14} '{f[4][:40]}'")
    bloque("topónimos", r["toponimos"],
           lambda f: f"{f[0]} {f[1]}  {f[2]:18} nivel {f[3]}  '{str(f[4])[:36]}'")
    bloque("cola Esteves", r["esteves"], lambda f: f"{f[0]} {f[1]}")
    bloque("añú (A-2)", r["paraujano"], lambda f: f"{f[0]} {f[1]:14} '{f[2][:40]}'")
    bloque("lokono (A-2)", r["lokono"], lambda f: f"{f[0]} {f[1]:14} '{f[2][:40]}'")
    ok, motivos = r["fono"]
    print(f"  fonotáctica: {'pasa' if ok else 'NO pasa'}"
          + (f" — {'; '.join(motivos)}" if motivos else "")
          + "  (filtro negativo; débil en positivo)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("voces", nargs="+")
    ap.add_argument("--glosa", help="glosa del libro: busca el mismo referente en el lexicón")
    args = ap.parse_args(argv)

    canon = cargar()
    print(f"  canon: lexicón {len(canon['lexicon'])} · cognados {len(canon['cognados'])} · "
          f"topónimos {len(canon['toponimos'])} · Esteves {len(canon['esteves'])} · "
          f"añú {len(canon['paraujano'])} · lokono {len(canon['lokono'])}")
    for voz in args.voces:
        imprimir(cruzar(voz, canon, args.glosa))
    print("\n  filtros 1-2 del protocolo (DRAE/venezolanismo general; papiamento/neerlandés): "
          "no automatizables — juicio.\n")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
