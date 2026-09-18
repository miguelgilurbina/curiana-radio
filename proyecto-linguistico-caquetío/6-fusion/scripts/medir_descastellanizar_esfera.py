# -*- coding: utf-8 -*-
"""«La etiqueta manda»: qué voces de la esfera circulan con grafía castellana.

Decisión de Miguel (2026-09-18): des-castellanizar las voces de la esfera de
contacto. `casabe`, `yuca`, `maíz`, `batata` o `papaya` son voces taínas del
lexicón que el castellano también usa; cuentan como préstamo de esfera —el
producto de la esfera ES la esfera, 2026-09-17— pero no tienen por qué circular
por el motor con la grafía castellana.

Cinco mediciones:

  A. CENSO. Cuántas voces de la esfera hay y cuántas llevan marca de grafía
     castellana (tilde, ⟨c⟩, ⟨z⟩, ⟨qu⟩, ⟨ll⟩, ⟨ñ⟩ — lo que la retroabstracción
     de `matakán` quita), sobre las tres bases posibles: todas, las de
     categoría prestable, y las 50 candidatas de [Voces de fuera].
  B. LA TABLA. Para cada marcada: familia, categoría, nota, gemela fonémica en
     el lexicón y la clase que le tocó (atestiguado / atestiguada-sin-clave /
     retroabstraido-propuesto / se-queda).
  C. [Voces de fuera] ANTES y DESPUÉS: cuántas candidatas, cuáles cambian de
     forma, cuáles se caen y cuáles conservan su marca por decisión.
  D. EL SCORER NO SE MUEVE. Se carga el `curiana_lexicon.py` de HEAD como
     módulo aparte y se compara `score`, `pct_caquetio_especifico`, `densidad`
     y `prestamos_de_esfera` frase a frase con el de ahora.
  E. LA BASE. Cuántas filas de `loanword_uses` se leen con otra forma al
     normalizar (los runs viejos NO se reescriben).

Uso:  python 6-fusion/scripts/medir_descastellanizar_esfera.py
      python 6-fusion/scripts/medir_descastellanizar_esfera.py --sin-base

E necesita el Supabase local en Docker (ver CLAUDE.md); sin él, `--sin-base`.
D necesita git (lee `HEAD:curiana_sim/curiana_lexicon.py`).
"""
import argparse
import collections
import importlib.util
import io
import os
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIM = os.path.join(RAIZ, "curiana_sim")
sys.path.insert(0, SIM)
CONTENEDOR = "supabase_db_curiana_sim"

import curiana_lexicon as L                                      # noqa: E402
from curiana_database import normalize_source_language            # noqa: E402

# Las frases con que se comprueba que el scorer no se movió. Salen de la
# medición del 2026-09-17 (medicion_hispanismos_loanword_uses): las dos voces
# que más pesan en la base, dentro de la frase caquetía y en la glosa.
FRASES = [
    "Casabe kaa-ni wara amana-ni",
    "Wara masa-da buri-kana saa casabe kaa-ni",
    "Maíz, yuca ta-kana",
    "Taya naa-ka casabe wana-ni, ta-casabe para-ko",
    "Las manos ocupadas limpiando yuca",
    "El cacique dijo que el maíz del bohío es de todos",
    "Taya wana-ni watapana, ka-watapana saa",
    "Pia naa-ka maisi, cazabi kaa-ni wara",
]

CLAVES = ("score", "densidad", "pct_caquetio_especifico", "otro_arahuaco",
          "espanol_funcional", "palabras_caquetias", "palabras_arahuacas",
          "palabras_otro_arahuaco", "aspectos_usados", "prestamos_de_esfera")

# Lo que espera decisión de Miguel. El motor sólo sabe que estas claves no se
# enseñan (`SIN_FORMA_DE_LA_ESFERA`); la etiqueta fina es canon y vive en el
# YAML. La forma propuesta NO se escribe a mano: para las retroabstraídas es el
# lema fonémico D5 (`fonemizar`), la misma convención con que entró `matakán`;
# para la atestiguada es la forma literal que trae la nota del lexicón.
ATESTIGUADAS_SIN_CLAVE = {"huracan": "hurakán"}     # nota: «Tno. hurakán → español huracán»
RETROABSTRAIDAS = ("cayo", "caney", "cobo", "cemi", "bejique")


def titulo(t):
    print(f"\n{'=' * 72}\n  {t}\n{'=' * 72}")


def esfera_del_lexicon(mod):
    return {k: d for k, d in mod.VOCABULARIO_BASE.items()
            if normalize_source_language(d.get("fuente", "")) in mod.ESFERA_DE_CONTACTO}


# ══════════════════════════════════════════════════════════════════════
# A. Censo
# ══════════════════════════════════════════════════════════════════════

def censo():
    titulo("A. CENSO — las voces de la esfera y su grafía")
    esfera = esfera_del_lexicon(L)
    prestables = {k: d for k, d in esfera.items()
                  if (d.get("categoria") or d.get("cat") or "") not in L._CAT_NO_PRESTABLE}
    candidatas = L.voces_de_fuera_posibles()

    for nombre, claves in (("todas las voces de la esfera", esfera),
                           ("de categoría prestable", prestables)):
        marcadas = {k: L.marcas_castellanas(k) for k in claves}
        marcadas = {k: v for k, v in marcadas.items() if v}
        print(f"\n  {nombre}: {len(claves)}  ·  con marca castellana: {len(marcadas)}")
        por_marca = collections.Counter(m for v in marcadas.values() for m in v)
        print(f"    marcas: {dict(sorted(por_marca.items()))}")
        print(f"    {sorted(marcadas)}")

    print(f"\n  candidatas de [Voces de fuera] HOY: {len(candidatas)}")
    con_marca = sorted({c[1] for c in candidatas if L.marcas_castellanas(c[1])})
    print(f"    formas que aún llevan marca (todas declaradas `se-queda`): {con_marca}")

    # ── Reconciliación con la cifra que traía Miguel («19 de 113») ──────
    # No se reproduce tal cual y se dice: el lexicón tiene 133 voces de la
    # esfera, no 113 (lo mismo que ya dice el docstring de `_glosa_util`).
    # El 19 sí sale, con un criterio MÁS GRUESO que el declarado: contando
    # ⟨ch⟩ como ⟨c⟩ y contando la etiqueta de lengua de la clave
    # (`achi-kalinago`, `kanawa-caribe`) como parte de la voz.
    import re as _re
    def _grueso(k):
        kk = k.lower()
        return bool(_re.search(r"[áéíóú]|qu|c|z|ll|ñ", kk))
    print("\n  reconciliación con «19 de 113»:")
    print(f"    voces de la esfera: {len(esfera)} (no 113; `_glosa_util` ya decía 133)")
    print(f"    criterio grueso (⟨ch⟩ cuenta, la etiqueta de lengua cuenta)"
          f" sobre las {len(prestables)} prestables: "
          f"{sum(1 for k in prestables if _grueso(k))}")
    print(f"    criterio declarado aquí sobre las {len(prestables)} prestables: "
          f"{sum(1 for k in prestables if L.marcas_castellanas(k))}")
    print(f"    criterio grueso sobre las {len(esfera)}: "
          f"{sum(1 for k in esfera if _grueso(k))}")
    return esfera, prestables, candidatas


# ══════════════════════════════════════════════════════════════════════
# B. La tabla de decisión
# ══════════════════════════════════════════════════════════════════════

def lema_d5(clave):
    """El lema fonémico con que entró `matakán`: k por c/qu, z→s, sin tildes."""
    from curiana_fonotactica import fonemizar
    return fonemizar(clave, False)


def clase_de(clave):
    if clave in L.FORMA_DE_LA_ESFERA:
        return "atestiguado", L.FORMA_DE_LA_ESFERA[clave]
    if clave in ATESTIGUADAS_SIN_CLAVE:
        return "atestiguada-sin-clave · NO APLICADA", ATESTIGUADAS_SIN_CLAVE[clave]
    if clave in RETROABSTRAIDAS:
        return "retroabstraida-propuesta · NO APLICADA", lema_d5(clave)
    if clave in L.SE_QUEDA_CON_SU_GRAFIA:
        return "se-queda", clave
    return "SIN DECIDIR", ""


def gemelas(clave):
    """Claves del lexicón con el mismo esqueleto fonémico (D5)."""
    from curiana_fonotactica import fonemizar
    fuera = set()
    for gu in (False, True):
        objetivo = fonemizar(clave, gu)
        if not objetivo:
            continue
        for k in L.VOCABULARIO_BASE:
            if k != clave and fonemizar(k, gu) == objetivo:
                fuera.add(k)
    return sorted(fuera)


def tabla(esfera):
    titulo("B. LA TABLA — voz a voz")
    marcadas = sorted(k for k in esfera if L.marcas_castellanas(k))
    cuenta = collections.Counter()
    for k in marcadas:
        d = esfera[k]
        clase, destino = clase_de(k)
        cuenta[clase] += 1
        fam = normalize_source_language(d.get("fuente", ""))
        cat = d.get("categoria") or d.get("cat") or ""
        gem = [g for g in gemelas(k)
               if normalize_source_language(L.VOCABULARIO_BASE[g].get("fuente", ""))
               in L.ESFERA_DE_CONTACTO]
        flecha = f" → {destino}" if destino and destino != k else ""
        print(f"\n  {k}{flecha}   [{clase}]")
        print(f"      familia={fam} · categoría={cat} · marcas={L.marcas_castellanas(k)}")
        print(f"      sig: {(d.get('sig') or d.get('es') or '')[:100]}")
        if gem:
            print(f"      gemelas fonémicas en la esfera: {gem}")
        nota = (d.get("notas") or "").split("·")[0].strip()
        if nota:
            print(f"      nota: {nota[:150]}")
    print(f"\n  RESUMEN: {dict(sorted(cuenta.items()))}  (total {len(marcadas)})")

    # Las propuestas, contra la fonotáctica atestiguada — como se midió
    # `matakán` el 2026-09-14. NO decide nada: sólo dice si la forma cabe.
    from curiana_fonotactica import Fonotactica
    atestiguado = [k for k, d in L.VOCABULARIO_BASE.items()
                   if str(d.get("fuente", "")).startswith("caquetío")]
    fono = Fonotactica(atestiguado)
    print("\n  las propuestas, contra la fonotáctica del caquetío del lexicón:")
    for clave in list(ATESTIGUADAS_SIN_CLAVE) + list(RETROABSTRAIDAS):
        _clase, forma = clase_de(clave)
        ok, motivos = fono.valida(forma)
        choca = forma in L.VOCABULARIO_BASE
        print(f"    {clave:10} → {forma:10} válida={ok} {motivos if motivos else ''}"
              f"{'  ⚠ la clave YA existe en el lexicón' if choca else ''}")
    return cuenta


# ══════════════════════════════════════════════════════════════════════
# C/D. Antes y después (el módulo de HEAD)
# ══════════════════════════════════════════════════════════════════════

def lexicon_de_head():
    """Carga `HEAD:curiana_sim/curiana_lexicon.py` como módulo aparte."""
    # `./` = relativo al cwd de git, que aquí es la carpeta del proyecto
    # dentro del repo (el repo es la web entera, no sólo el proyecto).
    out = subprocess.run(["git", "-C", RAIZ, "show", "HEAD:./curiana_sim/curiana_lexicon.py"],
                         capture_output=True, encoding="utf-8")
    if out.returncode != 0:
        return None
    tmp = os.path.join(tempfile.mkdtemp(), "curiana_lexicon_head.py")
    with io.open(tmp, "w", encoding="utf-8") as f:
        f.write(out.stdout)
    spec = importlib.util.spec_from_file_location("curiana_lexicon_head", tmp)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def voces_de_fuera_antes_y_despues(antes):
    titulo("C. [VOCES DE FUERA] — antes y después")
    if antes is None:
        print("  (sin git: no se puede leer el módulo de HEAD)")
        return
    a = {p: f for p, f, _g, _fam in antes.voces_de_fuera_posibles()}
    d = {p: f for p, f, _g, _fam in L.voces_de_fuera_posibles()}
    print(f"\n  candidatas: {len(a)} → {len(d)}")
    cambian = {p: (a[p], d[p]) for p in a if p in d and a[p] != d[p]}
    caen = sorted(set(a) - set(d))
    print(f"\n  cambian de forma ({len(cambian)}):")
    for p, (x, y) in sorted(cambian.items()):
        print(f"      {x} → {y}")
    print(f"\n  se caen ({len(caen)}): {caen}")
    for p in caen:
        motivo = ("colapsa en la misma forma que otra clave"
                  if L.forma_de_la_esfera(p) in set(d.values())
                  else "castellana sin gemela: espera decisión de Miguel")
        print(f"      {p}: {motivo}")
    marcadas_antes = sorted({f for f in a.values() if L.marcas_castellanas(f)})
    marcadas_despues = sorted({f for f in d.values() if L.marcas_castellanas(f)})
    print(f"\n  formas con marca castellana: {len(marcadas_antes)} → {len(marcadas_despues)}")
    print(f"      antes:   {marcadas_antes}")
    print(f"      después: {marcadas_despues}")
    sin_declarar = [f for f in marcadas_despues if f not in L.SE_QUEDA_CON_SU_GRAFIA]
    print(f"      sin declarar `se-queda`: {sin_declarar or 'ninguna'}")


def el_scorer_no_se_mueve(antes):
    titulo("D. EL SCORER — antes y después, frase a frase")
    if antes is None:
        print("  (sin git: no se puede leer el módulo de HEAD)")
        return
    lex_a, lex_d = antes.LexicoComunitario(), L.LexicoComunitario()
    distintas = 0
    for frase in FRASES:
        ra = antes.score_linguistico(frase, lex_a)
        rd = L.score_linguistico(frase, lex_d)
        difs = [k for k in CLAVES if ra.get(k) != rd.get(k)]
        marca = "≠ " + ", ".join(difs) if difs else "="
        distintas += bool(difs)
        print(f"\n  «{frase[:60]}»")
        print(f"      score {ra['score']} → {rd['score']} · "
              f"densidad {ra['densidad']:.3f} → {rd['densidad']:.3f} · "
              f"pct_caq {ra['pct_caquetio_especifico']:.3f} → "
              f"{rd['pct_caquetio_especifico']:.3f}")
        print(f"      prestamos_de_esfera: {ra['prestamos_de_esfera']} → "
              f"{rd['prestamos_de_esfera']}   [{marca}]")
    print(f"\n  frases con alguna diferencia en {list(CLAVES)}: {distintas} de {len(FRASES)}")


# ══════════════════════════════════════════════════════════════════════
# E. La base
# ══════════════════════════════════════════════════════════════════════

def la_base():
    titulo("E. loanword_uses — qué se lee distinto (los runs viejos no se reescriben)")
    sql = ("select coalesce(forma_dicha, word) as dicha, word, count(*) "
           "from loanword_uses group by 1,2 order by 3 desc")
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d", "postgres",
         "-Atc", sql], capture_output=True, encoding="utf-8")
    if out.returncode != 0:
        print(f"  (sin base: {out.stderr.strip()[:160]})")
        return
    total = cambian = 0
    print()
    for linea in out.stdout.strip().splitlines():
        if not linea:
            continue
        dicha, word, n = linea.split("|")
        voz = L.forma_de_la_esfera(word)
        total += int(n)
        if voz != dicha:
            cambian += int(n)
        flecha = f"  →  se lee «{voz}»" if voz != dicha else ""
        print(f"    {dicha:16} × {n}{flecha}")
    print(f"\n  filas: {total} · se leen con otra forma: {cambian}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sin-base", action="store_true",
                    help="salta la medición E (no necesita Docker)")
    a = ap.parse_args(argv)

    esfera, _prestables, _cands = censo()
    tabla(esfera)
    antes = lexicon_de_head()
    voces_de_fuera_antes_y_despues(antes)
    el_scorer_no_se_mueve(antes)
    if not a.sin_base:
        la_base()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
