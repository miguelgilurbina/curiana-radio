# -*- coding: utf-8 -*-
"""¿Cuánto mueve el score la comparanda no caquetía del lexicón?

Tres mediciones sobre las 1.227 respuestas guardadas en
curiana_sim/curiana_observer.json (historial), que traen el texto completo y
el score con que se guardaron.

  A. Composición: cuánto del lexicón NO es caquetío, y cuántas de esas claves
     son homógrafas de una palabra española (pueden dispararse en el match por
     token de score_linguistico).
  B. El score recalculado con y sin las claves no caquetías en
     `palabras_activas()`. Diferencia media, mediana y distribución.
  C. detectar_uso_vocabulario(), que casa por SUBCADENA: cuántos falsos
     positivos mete sobre esos mismos textos.
"""
import io, json, os, re, sys, statistics, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
sys.path.insert(0, os.path.join(R, "curiana_sim"))

import curiana_lexicon as CL
from curiana_lexicon import (VOCABULARIO_BASE as V, LexicoComunitario,
                             score_linguistico, detectar_uso_vocabulario)
from curiana_database import normalize_source_language as nsl

CAQ = {k for k, e in V.items() if nsl(e.get("fuente", "")) == "caquetío"}
NOCAQ = set(V) - CAQ

# ── A. composición y homógrafos del español ──────────────────────────────
print("=" * 72)
print("A. COMPOSICIÓN DEL LEXICÓN")
print("=" * 72)
print(f"  claves totales: {len(V)}")
print(f"  caquetío:       {len(CAQ)}  ({100*len(CAQ)/len(V):.1f}%)")
print(f"  NO caquetío:    {len(NOCAQ)}  ({100*len(NOCAQ)/len(V):.1f}%)")

hist = json.load(io.open(os.path.join(R, "curiana_sim", "curiana_observer.json"),
                         encoding="utf-8"))["historial"]
print(f"  respuestas guardadas: {len(hist)}")

# vocabulario español de referencia: las palabras que aparecen en las glosas
# del propio lexicón + las stopwords que el motor ya declara
ES = set(CL.ES_STOPWORDS) | set(getattr(CL, "RAICES_ESPANOLAS", set()))
for e in V.values():
    for w in re.findall(r"[a-záéíóúñ]{2,}", (e.get("sig") or e.get("es") or "").lower()):
        ES.add(w)
homog = sorted(k for k in NOCAQ if k in ES)
print(f"\n  claves NO caquetías que son homógrafas de una palabra española: {len(homog)}")
print("   ", ", ".join(homog[:40]))

# ── B. el score con y sin la comparanda ──────────────────────────────────
print()
print("=" * 72)
print("B. EL SCORE CON Y SIN LAS CLAVES NO CAQUETÍAS")
print("=" * 72)

lex = LexicoComunitario()

def rescorar(filtrar):
    orig = LexicoComunitario.palabras_activas
    if filtrar:
        LexicoComunitario.palabras_activas = lambda self: [
            k for k in orig(self) if k in CAQ or k not in V]
    try:
        return [score_linguistico(h["texto"], lex) for h in hist]
    finally:
        LexicoComunitario.palabras_activas = orig

con = rescorar(False)
sin = rescorar(True)

guardado = [h["score"] for h in hist]
s_con = [r["score"] for r in con]
s_sin = [r["score"] for r in sin]

iguales = sum(1 for a, b in zip(guardado, s_con) if abs(a - b) < 0.05)
print(f"  control: el recálculo reproduce el score guardado en "
      f"{iguales}/{len(hist)} respuestas ({100*iguales/len(hist):.1f}%)")

dif = [a - b for a, b in zip(s_con, s_sin)]
cambian = [d for d in dif if abs(d) > 0.001]
print(f"\n  media  CON comparanda: {statistics.mean(s_con):.3f}")
print(f"  media  SIN comparanda: {statistics.mean(s_sin):.3f}")
print(f"  diferencia media:      {statistics.mean(dif):+.3f}")
print(f"  mediana de la dif.:    {statistics.median(dif):+.3f}")
print(f"  respuestas que cambian: {len(cambian)}/{len(hist)} "
      f"({100*len(cambian)/len(hist):.1f}%)")
if cambian:
    print(f"  de las que cambian — media {statistics.mean(cambian):+.3f}, "
          f"máx {max(cambian):+.3f}, mín {min(cambian):+.3f}")
    tramos = collections.Counter()
    for d in cambian:
        tramos[f"{int(abs(d)//0.5)*0.5:.1f}-{int(abs(d)//0.5)*0.5+0.5:.1f}"] += 1
    print("  distribución del |cambio|:", dict(sorted(tramos.items())))

# qué palabras no caquetías son las que están contando
usadas_nocaq = collections.Counter()
for r in con:
    for t in r.get("palabras_otro_arahuaco", []) or []:
        usadas_nocaq[t] += 1
print(f"\n  voces NO caquetías realmente usadas por los agentes: {len(usadas_nocaq)}")
for t, n in usadas_nocaq.most_common(15):
    print(f"    {t:<16} x{n}  [{V.get(t,{}).get('fuente','?')}]")

# ── C. el match por subcadena ────────────────────────────────────────────
print()
print("=" * 72)
print("C. detectar_uso_vocabulario() — match por SUBCADENA")
print("=" * 72)
falsos = collections.Counter()
tot_det = tot_tok = 0
for h in hist:
    det = detectar_uso_vocabulario(h["texto"], lex)
    tot_det += len(det)
    toks = set(re.findall(r"[a-záéíóúñü\-]+", h["texto"].lower()))
    tot_tok += len(toks)
    for p in det:
        if p not in toks:                     # sólo casó por dentro de otra palabra
            dentro = [t for t in toks if p in t and p != t]
            if dentro:
                falsos[(p, dentro[0])] += 1
print(f"  detecciones totales: {tot_det}")
n_falsos = sum(falsos.values())
print(f"  detecciones que sólo casan DENTRO de otra palabra: {n_falsos} "
      f"({100*n_falsos/max(tot_det,1):.1f}%)")
print("  los quince peores (clave → palabra donde se metió):")
for (p, d), n in falsos.most_common(15):
    fam = V.get(p, {}).get("fuente", "?")
    print(f"    {p:<12} dentro de «{d:<18}» x{n}  [{fam}]")
