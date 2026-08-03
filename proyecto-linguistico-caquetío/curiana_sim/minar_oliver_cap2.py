"""
CURIANA — Minería de Oliver 1989, cap. 2 (*Arawakan Historical Linguistics*)
=============================================================================

Fuente:
    Oliver, José R. (1989). "Chapter 2: Arawakan Historical Linguistics".
    → fuentes_caquetios/Chapter 2 Linguistics- Oliver 1989.pdf (109 pp.)

Este script NO modifica `curiana_lexicon.py` ni `arahuaco_comparative.py`.
Emite una propuesta y la VERIFICA: todo lo que afirma `cognados_oliver.py`
lleva un ancla textual y una página, y este script comprueba que el ancla
existe en el PDF y que la página declarada coincide con el pie de página real.
Misma disciplina que `minar_zavala_glosario.py` y `minar_pares_validacion.py`.

MOTIVO (F5, 2026-08-03): de 109 páginas de fonología comparada arahuaca el
proyecto solo había extraído un hallazgo puntual (`daitiao`, p. 147). El
capítulo es el pilar teórico de la Capa 2 y la fuente natural de `COGNADOS`
(37 entradas) y de las `REGLAS_*` de transducción.

Uso:
    python minar_oliver_cap2.py                 # informe completo
    python minar_oliver_cap2.py --verificar     # solo verificación de anclas
    python minar_oliver_cap2.py --artefactos    # calidad de la extracción
    python minar_oliver_cap2.py --adjudicar     # las 441 contra Oliver
    python minar_oliver_cap2.py --pares         # pares nuevos contra el motor actual
    python minar_oliver_cap2.py --json out.json
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata


# ---------------------------------------------------------------------------
# Consola Windows (cp1252) vs. informe con «─», «→», «ï»…
# Solo al ejecutar como script: reasignar sys.stdout al importarlo rompería
# el stdout de quien importe el módulo.
# ---------------------------------------------------------------------------
def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


AQUI = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(AQUI, "..", "fuentes_caquetios",
                        "Chapter 2 Linguistics- Oliver 1989.pdf")

# El pie de página de la tesis: el número aparece al final de cada plana,
# seguido del encabezado corrido de la siguiente. Es el único ancla de
# paginación fiable: el PDF no tiene numeración interna utilizable.
_MARCADOR_PAGINA = re.compile(
    r"\n\s{20,}(\d{2,3})\s*\nChapter 2: Arawakan Historical Linguistics[^\n]*\n")

PAGINA_MINIMA, PAGINA_MAXIMA = 52, 160   # rango real del capítulo en la tesis


# ===========================================================================
# 1. EXTRACCIÓN
# ===========================================================================

def extraer_texto(pdf: str = PDF_PATH, cache: bool = True) -> str:
    """Extrae el texto del PDF preservando la disposición de las columnas.

    `pdftotext -layout` es lo que hay que usar aquí, NO el modo por defecto:
    con el modo plano, la extracción de este PDF cae en tramos de **una
    palabra por línea** (14.2% de las líneas frente al 3.9% con -layout), y
    las tabulaciones de las tablitas inline se pierden. Cae a `pypdf` si
    poppler no está disponible, con la advertencia de que ahí sí habrá que
    re-unir líneas.
    """
    if not os.path.exists(pdf):
        raise FileNotFoundError(f"No se encuentra el PDF: {pdf}")

    destino = os.path.join(tempfile.gettempdir(), "curiana_oliver2_layout.txt")
    if cache and os.path.exists(destino) and \
            os.path.getmtime(destino) > os.path.getmtime(pdf):
        with open(destino, encoding="utf-8") as fh:
            return fh.read()

    try:
        subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout", pdf, destino],
                       check=True, capture_output=True)
        with open(destino, encoding="utf-8") as fh:
            texto = fh.read()
    except (FileNotFoundError, subprocess.CalledProcessError):
        try:
            from pypdf import PdfReader
        except ImportError as exc:                       # pragma: no cover
            raise RuntimeError(
                "Ni pdftotext ni pypdf disponibles. Instala poppler-utils "
                "o `pip install pypdf`.") from exc
        lector = PdfReader(pdf)
        texto = reunir_lineas_partidas(
            "\n".join(p.extract_text() or "" for p in lector.pages))
        with open(destino, "w", encoding="utf-8") as fh:
            fh.write(texto)
    return texto


def reunir_lineas_partidas(texto: str, umbral: int = 4) -> str:
    """Repara los tramos donde la extracción sale a **una palabra por línea**.

    Artefacto documentado de este PDF. Heurística: `umbral` o más líneas
    consecutivas de una sola palabra que no terminan en signo de puntuación
    fuerte se re-unen en un párrafo. Se respetan las líneas que parecen
    encabezados, pies de página o entradas tabuladas.
    """
    lineas = texto.split("\n")
    salida: list[str] = []
    buffer: list[str] = []

    def _es_palabra_suelta(linea: str) -> bool:
        s = linea.strip()
        if not s or len(s.split()) != 1:
            return False
        if s.isdigit():                       # pie de página
            return False
        if s.endswith((".", ":", "?", "!")):  # fin de oración: probablemente real
            return False
        return True

    def _volcar() -> None:
        if not buffer:
            return
        salida.append(" ".join(buffer) if len(buffer) >= umbral else "\n".join(buffer))
        buffer.clear()

    for linea in lineas:
        if _es_palabra_suelta(linea):
            buffer.append(linea.strip())
        else:
            _volcar()
            salida.append(linea)
    _volcar()
    return "\n".join(salida)


def mapa_paginas(texto: str) -> list[tuple[int, str]]:
    """[(número_de_página, cuerpo_normalizado_de_esa_página), ...] en orden.

    El cuerpo de la página `n` es todo lo que va desde el final del marcador
    anterior hasta el inicio del marcador que lleva el número `n` — el número
    está al PIE, no en la cabecera.
    """
    paginas: list[tuple[int, str]] = []
    previo = 0
    for m in _MARCADOR_PAGINA.finditer(texto):
        paginas.append((int(m.group(1)), _normalizar(texto[previo:m.start()])))
        previo = m.end()
    if previo < len(texto):
        paginas.append((-1, _normalizar(texto[previo:])))
    return paginas


def _normalizar(s: str) -> str:
    """Colapsa espacios, tabuladores, saltos de línea y anchos-cero.

    El PDF mete U+200B entre celdas de las tablitas y parte las oraciones en
    mitad de un sintagma, así que la comparación literal no sirve.
    """
    s = s.replace("​", " ").replace("­", "")
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s).strip()


def pagina_de(texto: str, paginas: list[tuple[int, str]], ancla: str) -> int | None:
    """Página de la tesis en la que aparece `ancla`.

    Busca dentro de cada plana ya normalizada. Si el ancla cruza un salto de
    página (pasa: el PDF corta oraciones a mitad), reintenta sobre pares de
    planas consecutivas y la atribuye a la primera.
    """
    objetivo = _normalizar(ancla)
    for pagina, cuerpo in paginas:
        if objetivo in cuerpo:
            return pagina
    for (pag_a, cuerpo_a), (_, cuerpo_b) in zip(paginas, paginas[1:]):
        if objetivo in f"{cuerpo_a} {cuerpo_b}":
            return pag_a
    return None


# ===========================================================================
# 2. VERIFICACIÓN DE LA PROPUESTA
# ===========================================================================

def _anclas_declaradas() -> list[tuple[str, str, str, int]]:
    """[(bloque, clave, ancla, pagina_declarada), ...] de cognados_oliver.py."""
    from cognados_oliver import COGNADOS_OLIVER, CORRESPONDENCIAS_OLIVER
    items: list[tuple[str, str, str, int]] = []
    for clave, datos in COGNADOS_OLIVER.items():
        if datos.get("ancla"):
            items.append(("COGNADOS_OLIVER", clave, datos["ancla"], datos["pagina"]))
    for corr in CORRESPONDENCIAS_OLIVER:
        if corr.get("ancla"):
            items.append(("CORRESPONDENCIAS_OLIVER", corr["id"],
                          corr["ancla"], corr["pagina"]))
    return items


def verificar(texto: str) -> dict:
    """Comprueba ancla-a-ancla que la propuesta esté sostenida por el PDF."""
    marcadores = mapa_paginas(texto)
    resultados = []
    for bloque, clave, ancla, pag_decl in _anclas_declaradas():
        pag_real = pagina_de(texto, marcadores, ancla)
        if pag_real is None:
            estado = "NO ENCONTRADA"
        elif pag_real == pag_decl:
            estado = "OK"
        else:
            estado = f"PAGINA {pag_real} != {pag_decl}"
        resultados.append({
            "bloque": bloque, "clave": clave, "ancla": ancla,
            "pagina_declarada": pag_decl, "pagina_real": pag_real, "estado": estado,
        })
    ok = sum(1 for r in resultados if r["estado"] == "OK")
    return {"total": len(resultados), "ok": ok, "detalle": resultados}


# ===========================================================================
# 3. CALIDAD DE LA EXTRACCIÓN (artefactos conocidos)
# ===========================================================================

def artefactos(texto: str) -> dict:
    """Mide el artefacto de 'una palabra por línea' y localiza las páginas
    que son solo pie de figura/tabla — es decir, imágenes sin capa de texto."""
    lineas = texto.split("\n")
    sueltas = [l for l in lineas if l.strip() and len(l.strip().split()) == 1]

    marcadores = list(_MARCADOR_PAGINA.finditer(texto))
    solo_pie, previo = [], 0
    for m in marcadores:
        cuerpo = texto[previo:m.start()].strip()
        if len(cuerpo) < 400:
            solo_pie.append({
                "pagina": int(m.group(1)),
                "caracteres": len(cuerpo),
                "primera_linea": _normalizar(cuerpo)[:90],
            })
        previo = m.end()

    return {
        "lineas": len(lineas),
        "lineas_de_una_palabra": len(sueltas),
        "pct_una_palabra": round(100 * len(sueltas) / max(len(lineas), 1), 1),
        "paginas_detectadas": len(marcadores),
        "paginas_solo_pie": solo_pie,
        "diagnostico": (
            "Con `pdftotext -layout` el artefacto de una-palabra-por-línea baja a "
            "~4% y no afecta a §2.8. Las páginas listadas en `paginas_solo_pie` son "
            "figuras y tablas embebidas como imagen: NO tienen capa de texto y no se "
            "pueden reconstruir por extracción. Incluyen la Tabla 3 (reflejos "
            "fonémicos, p.104) y la Tabla 8 (lexicoestadística, p.130), que son las "
            "dos que más se buscaban."
        ),
    }


# ===========================================================================
# 4. ADJUDICACIÓN DE LAS 441 FORMAS `hipotético-no-verificado`
# ===========================================================================

# "Lok. dakuty → tacuty" · "Way. aanükü → anucu" · "Taíno bejique → peyiche"
_DERIVACION = re.compile(
    r"(Lok\.|Way\.|Taíno|Taino)\s+([^\s→]+)\s*→\s*([^\s;]+)")

_PALATALES_WY = ("sh", "ch", "ñ")

# Conceptos para los que Oliver da forma caquetía atestiguada (clave A4).
_CUBIERTOS_POR_OLIVER = {
    "perro": "auri",
    "ceniza": "barisi",
    "árbol": "ada", "arbol": "ada",
    "diente": "dare",
    "tapir": "kama", "danta": "kama",
    "calabaza": "auyama",
    "hormiga": "koke", "bachaco": "koke",
    "mar": "para",
}


def _derivaciones(notas: str) -> list[tuple[str, str, str]]:
    """[(lengua, forma_origen, forma_reconstruida), ...]"""
    return [(m.group(1).rstrip("."), m.group(2).lower(), m.group(3).lower())
            for m in _DERIVACION.finditer(notas or "")]


def adjudicar() -> dict:
    """Aplica las claves A1-A5 de cognados_oliver.py a lexicon_candidatos.py."""
    from lexicon_candidatos import CANDIDATOS_NO_VERIFICADOS as C

    veredictos: dict[str, list[str]] = {k: [] for k in ("A1", "A2", "A3", "A4", "A5")}
    detalle: dict[str, dict] = {}

    for forma, datos in C.items():
        notas = datos.get("notas", "")
        glosa = (datos.get("es") or "").lower()
        claves: list[str] = []
        derivs = _derivaciones(notas)

        for lengua, origen, reconstruida in derivs:
            if lengua == "Lok":
                if origen.startswith("d") and reconstruida.startswith("t"):
                    claves.append("A1")
                if origen.startswith("b") and reconstruida.startswith("p"):
                    claves.append("A2")
            if lengua == "Way" and any(p in origen for p in _PALATALES_WY):
                claves.append("A3")

        for concepto, atestiguada in _CUBIERTOS_POR_OLIVER.items():
            # Límite de palabra solo a la izquierda: la glosa del candidato
            # suele estar en plural ("dientes", "árboles") o modificada.
            if re.search(rf"\b{re.escape(concepto)}", glosa):
                claves.append("A4")
                detalle.setdefault(forma, {})["sustituir_por"] = atestiguada
                break

        # A5: solo difiere en vocales de todas sus fuentes → Oliver no puede juzgar.
        if derivs and not claves:
            solo_vocales = all(
                re.sub(r"[aeiouáéíóúüïö]", "", o) == re.sub(r"[aeiouáéíóúüïö]", "", r)
                for _, o, r in derivs)
            if solo_vocales:
                claves.append("A5")

        if claves:
            claves = sorted(set(claves))
            detalle.setdefault(forma, {}).update(
                {"claves": claves, "glosa": datos.get("es"), "notas": notas})
            for k in claves:
                veredictos[k].append(forma)

    adjudicables = sorted({f for lista in veredictos.values() for f in lista})
    accionables = sorted({f for k in ("A1", "A2", "A3", "A4")
                          for f in veredictos[k]})
    return {
        "total_candidatos": len(C),
        "por_clave": {k: len(v) for k, v in veredictos.items()},
        "adjudicables": len(adjudicables),
        "accionables": len(accionables),   # A5 no es una adjudicación, es un límite
        "pct_accionables": round(100 * len(accionables) / max(len(C), 1), 1),
        "formas": veredictos,
        "detalle": detalle,
    }


# ===========================================================================
# 5. PARES DE VALIDACIÓN NUEVOS CONTRA EL MOTOR ACTUAL
# ===========================================================================

def probar_pares() -> dict:
    """Corre PARES_VALIDACION_OLIVER contra `transducir()` SIN tocar el motor.

    Los fallos son el punto: dicen qué reglas hay que cambiar. No se "arregla"
    el par para que pase — eso sería circular.
    """
    from arahuaco_comparative import transducir, PARES_VALIDACION
    from cognados_oliver import PARES_VALIDACION_OLIVER

    filas = []
    for palabra, orig, dest, esperado, concepto in PARES_VALIDACION_OLIVER:
        obtenido = transducir(palabra, orig, dest, asterisk=False)
        pasa = bool(obtenido) and obtenido.replace("*", "") == esperado
        filas.append({"par": f"{orig}:{palabra} → {dest}", "esperado": esperado,
                      "obtenido": obtenido, "pasa": pasa, "concepto": concepto})
    return {
        "suite_actual": len(PARES_VALIDACION),
        "pares_nuevos": len(filas),
        "suite_propuesta": len(PARES_VALIDACION) + len(filas),
        "pasan_con_el_motor_de_hoy": sum(1 for f in filas if f["pasa"]),
        "detalle": filas,
    }


# ===========================================================================
# 6. INFORME
# ===========================================================================

def _linea(car: str = "─", n: int = 78) -> str:
    return car * n


def informe(texto: str) -> dict:
    from cognados_oliver import (COGNADOS_OLIVER, CORRESPONDENCIAS_OLIVER,
                                 NUEVAS_ENTRADAS_CAQUETIO, AFIJOS_OLIVER,
                                 NUDO_DAITIAO, ANCLA_ARCO_NORTENO,
                                 REVISIONES_REGLAS, NO_DISPONIBLE)

    ver = verificar(texto)
    art = artefactos(texto)
    adj = adjudicar()
    par = probar_pares()

    print(_linea("═"))
    print("  MINERÍA DE OLIVER 1989, CAP. 2 — Arawakan Historical Linguistics")
    print(_linea("═"))

    print(f"\n[1] EXTRACCIÓN")
    print(f"  caracteres            : {len(texto):,}")
    print(f"  páginas detectadas    : {art['paginas_detectadas']} "
          f"(pie de página de la tesis)")
    print(f"  líneas de una palabra : {art['lineas_de_una_palabra']} "
          f"({art['pct_una_palabra']}%)")
    print(f"  páginas solo-pie      : {len(art['paginas_solo_pie'])} "
          f"→ figuras y tablas SIN capa de texto")
    for p in art["paginas_solo_pie"]:
        if "Table" in p["primera_linea"]:
            print(f"      p.{p['pagina']:>4}  {p['primera_linea'][:66]}")

    print(f"\n[2] VERIFICACIÓN DE LA PROPUESTA (cognados_oliver.py)")
    print(f"  anclas comprobadas contra el PDF: {ver['ok']}/{ver['total']}")
    for r in ver["detalle"]:
        if r["estado"] != "OK":
            print(f"    {r['estado']:<22} {r['bloque']}[{r['clave']}]")
            print(f"      ancla: {r['ancla'][:64]}")

    print(f"\n[3] LO QUE SALIÓ")
    alta = [k for k, v in COGNADOS_OLIVER.items() if v["confianza"] == "alta"]
    media = [k for k, v in COGNADOS_OLIVER.items() if v["confianza"] == "media"]
    baja = [k for k, v in COGNADOS_OLIVER.items() if v["confianza"] == "baja"]
    print(f"  sets de cognados con caquetío : {len(COGNADOS_OLIVER)}")
    print(f"      confianza alta  : {len(alta):>2}  {', '.join(sorted(alta))}")
    print(f"      confianza media : {len(media):>2}  {', '.join(sorted(media))}")
    print(f"      confianza baja  : {len(baja):>2}  {', '.join(sorted(baja))}")
    con_duda = sum(1 for v in COGNADOS_OLIVER.values() if v.get("oliver_duda"))
    print(f"      con reserva textual del propio Oliver : {con_duda}")
    print(f"  correspondencias fonológicas  : {len(CORRESPONDENCIAS_OLIVER)}"
          f"  ({', '.join(c['id'] for c in CORRESPONDENCIAS_OLIVER)})")
    print(f"  afijos documentados           : {len(AFIJOS_OLIVER)}")
    print(f"  entradas caquetías nuevas     : {len(NUEVAS_ENTRADAS_CAQUETIO)}"
          f"  ({', '.join(NUEVAS_ENTRADAS_CAQUETIO)})")
    print(f"  revisiones al motor propuestas: {len(REVISIONES_REGLAS)}")
    for r in REVISIONES_REGLAS:
        print(f"      {r['veredicto']:<26} {r['regla']}")

    print(f"\n[4] PARES DE VALIDACIÓN")
    print(f"  suite actual   : {par['suite_actual']}")
    print(f"  pares nuevos   : {par['pares_nuevos']}  (fuente externa: Oliver/Taylor)")
    print(f"  suite propuesta: {par['suite_propuesta']}")
    print(f"  de los nuevos, pasan con el motor de HOY: "
          f"{par['pasan_con_el_motor_de_hoy']}/{par['pares_nuevos']}")
    for f in par["detalle"]:
        marca = "OK    " if f["pasa"] else "FALLA "
        print(f"    {marca} {f['par']:<20} → {str(f['obtenido']):<12} "
              f"(esperado {f['esperado']:<10}) {f['concepto'][:34]}")
    print("  Los fallos NO se corrigen forzando la regla: son la lista de reglas")
    print("  a revisar (ver REVISIONES_REGLAS).")

    print(f"\n[5] ADJUDICACIÓN DE LAS 441 `hipotético-no-verificado`")
    print(f"  candidatos en lexicon_candidatos.py : {adj['total_candidatos']}")
    for clave, n in adj["por_clave"].items():
        from cognados_oliver import CLAVES_ADJUDICACION
        meta = CLAVES_ADJUDICACION[clave]
        print(f"    {clave}  {n:>4}  {meta['veredicto']:<18} {meta['nombre']}")
    print(f"  ACCIONABLES (A1-A4, sin duplicar): {adj['accionables']} "
          f"= {adj['pct_accionables']}% de las 441")
    print(f"  A5 no es una adjudicación: es el límite metodológico de Oliver "
          f"(excluye vocales).")

    print(f"\n[6] NUDO daitiao / datihao / diao")
    print(f"  {NUDO_DAITIAO['veredicto']}")
    print(f"  páginas: {NUDO_DAITIAO['paginas']}")
    print(f"  {_normalizar(NUDO_DAITIAO['confirma_a_zavala'])[:200]}")

    print(f"\n[7] ANCLA DEL «ARCO NORTEÑO»")
    print(f"  {ANCLA_ARCO_NORTENO['veredicto']}")
    for pagina, cita in ANCLA_ARCO_NORTENO["citas"][:2]:
        print(f"    p.{pagina}: \"{cita[:100]}…\"")

    print(f"\n[8] LO QUE ESTE CAPÍTULO NO DA")
    for clave in ("tablas_comparativas", "apendice_A"):
        print(f"  · {_normalizar(NO_DISPONIBLE[clave])[:300]}")

    print("\n" + _linea("═"))
    print("  Propuesta en cognados_oliver.py. NADA se ha modificado en el motor.")
    print(_linea("═"))

    return {"verificacion": ver, "artefactos": art,
            "adjudicacion": adj, "pares": par}


def main() -> None:
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verificar", action="store_true")
    ap.add_argument("--artefactos", action="store_true")
    ap.add_argument("--adjudicar", action="store_true")
    ap.add_argument("--pares", action="store_true")
    ap.add_argument("--json", metavar="ARCHIVO")
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args()

    texto = extraer_texto(cache=not args.no_cache)
    parciales = args.verificar or args.artefactos or args.adjudicar or args.pares

    datos: dict = {}
    if args.verificar:
        datos["verificacion"] = v = verificar(texto)
        print(f"anclas verificadas: {v['ok']}/{v['total']}")
        for r in v["detalle"]:
            print(f"  {r['estado']:<22} {r['bloque']}[{r['clave']}] "
                  f"p.{r['pagina_declarada']}")
    if args.artefactos:
        datos["artefactos"] = a = artefactos(texto)
        print(json.dumps({k: v for k, v in a.items() if k != "paginas_solo_pie"},
                         ensure_ascii=False, indent=2))
        for p in a["paginas_solo_pie"]:
            print(f"  p.{p['pagina']:>4}  {p['caracteres']:>4} car.  "
                  f"{p['primera_linea'][:70]}")
    if args.adjudicar:
        datos["adjudicacion"] = d = adjudicar()
        print(json.dumps({k: v for k, v in d.items()
                          if k not in ("formas", "detalle")},
                         ensure_ascii=False, indent=2))
        for clave, formas in d["formas"].items():
            print(f"\n  {clave} ({len(formas)}): {', '.join(formas[:24])}"
                  f"{' …' if len(formas) > 24 else ''}")
    if args.pares:
        datos["pares"] = p = probar_pares()
        print(json.dumps(p, ensure_ascii=False, indent=2))

    if not parciales:
        datos = informe(texto)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(datos, fh, ensure_ascii=False, indent=2)
        print(f"\n→ {args.json}")


if __name__ == "__main__":
    main()
