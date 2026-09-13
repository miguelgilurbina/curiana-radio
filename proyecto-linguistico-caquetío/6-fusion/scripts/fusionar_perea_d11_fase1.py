# -*- coding: utf-8 -*-
"""Fase 1 de D11: las 173 raices lokono de Perea 1942 entran al lexicon.

Es la ULTIMA condicion en rojo del gate. El lexicon esta 781 wayuu contra
275 lokono (2,8 a 1); con estas quedaria 1,7 a 1.

Reglas que se respetan:
- los 4 HOMOGRAFOS no pisan nada: van con clave `<forma>-lokono`, que es el
  precedente que el lexicon ya usa (`kati-kalinago`).
- `cat` se INFIERE de la glosa y se declara: infinitivo castellano -> v_raiz,
  el resto -> sust. No se inventa mas gramatica de la que la fuente da.
- cada entrada lleva pagina y numero de atestaciones. Regla 8.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import lexicon_perea as P
import curiana_lexicon as CL

V = CL.VOCABULARIO_BASE
HOM = set(P.HOMOGRAFOS_CON_EL_LEXICON)
INFINITIVO = re.compile(r"^[a-záéíóúñ]{3,}(ar|er|ir)$")

def limpio(s):
    return str(s).replace('"', "'").replace("\\", "").strip()

filas, saltadas = [], []
for raiz in sorted(P.COMPARANDA_LOKONO):
    d = P.COMPARANDA_LOKONO[raiz]
    ac = [a for a in d.get("acepciones", []) if a.get("glosa")]
    if not ac:
        saltadas.append((raiz, "sin acepciones")); continue
    ac = sorted(ac, key=lambda a: -int(a.get("atestaciones") or 0))
    principal = limpio(ac[0]["glosa"])
    if len(principal) < 2 or not re.search(r"[a-záéíóúñ]", principal.lower()):
        saltadas.append((raiz, f"glosa ilegible: {principal!r}")); continue

    clave = f"{raiz}-lokono" if raiz in HOM else raiz
    if clave in V:
        saltadas.append((raiz, f"la clave {clave} ya existe")); continue

    cat = "v_raiz" if INFINITIVO.match(principal.lower().split(",")[0].strip()) else "sust"
    otras = "; ".join(f"{limpio(a['glosa'])} (p.{a.get('pagina','?')})" for a in ac[1:6])
    sig = principal if len(ac) == 1 else f"{principal} (y {len(ac)-1} acepción/es más)"

    notas = (f"Perea Alonso 1942, Filología Comparada Arawak, tomo I — "
             f"{P.ESTRATO}. Raíz `{raiz}` con {d.get('total','?')} atestaciones; "
             f"acepción principal «{principal}» (p. {ac[0].get('pagina','?')}, "
             f"{ac[0].get('atestaciones','?')} atestaciones).")
    if otras:
        notas += f" Otras acepciones: {otras}."
    if raiz in HOM:
        e = V[raiz]
        notas += (f" ⚠️ HOMÓGRAFO: la clave `{raiz}` ya existía en el lexicón "
                  f"como {e['fuente']} «{limpio(e['sig'])[:46]}», así que esta "
                  f"entra desambiguada como `{clave}` y NO la pisa — el "
                  f"precedente es `kati-kalinago`.")
    notas += (" `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, "
              "resto → sust): la fuente no da categoría gramatical.")
    notas += " Fusión fase 1 de D11, 2026-09-11."

    filas.append((clave, sig, cat, notas))

print(f"a fusionar: {len(filas)}   saltadas: {len(saltadas)}")
for r, por in saltadas: print(f"   · {r}: {por}")

# ── escribir, justo antes del cierre del dict ──
p = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
t = io.open(p, encoding="utf-8").read()
assert "D11 FASE 1" not in t

# 🔴 El ancla tiene que estar ACOTADA a VOCABULARIO_BASE. La primera version
# buscaba la ultima entrada del FICHERO y las 171 raices cayeron dentro de
# FUERA_DEL_HABLA — el dict de palabras RETIRADAS del habla. El sintoma fue
# que el total de entradas activas no se movio: 1503 antes y despues.
ini = t.index("VOCABULARIO_BASE: dict[str, dict] = {")
fin = t.index("REGLAS_ASPECTO", ini)          # el dict siguiente
region = t[ini:fin]
ancla = None
for m in re.finditer(r'^\s*"[a-z0-9ñáéíóúü\-]+":\s*\{.*\},\s*$', region, re.M):
    ancla = m
assert ancla, "no encuentro la última entrada de VOCABULARIO_BASE"


class _Ancla:                                   # posiciones absolutas
    def __init__(self, m, off): self._e = m.end() + off
    def end(self): return self._e


ancla = _Ancla(ancla, ini)

bloque = ["\n", "    # ══════════════════════════════════════════════════════\n",
          "    # D11 FASE 1 (2026-09-11) — las raíces lokono de Perea 1942.\n",
          "    # Comparanda, NO caquetío: rebalancea el eje que D11 decidió.\n",
          "    # ══════════════════════════════════════════════════════\n"]
for clave, sig, cat, notas in filas:
    bloque.append(f'    "{clave}": {{"sig": "{sig}", "cat": "{cat}", '
                  f'"fuente": "lokono", "notas": "{notas}"}},\n')
t = t[:ancla.end()] + "".join(bloque) + t[ancla.end():]
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print(f"\nescritas {len(filas)} entradas lokono")
