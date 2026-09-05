"""Genera 6-fusion/BANDEJA.md — la cola de entrada al canon, medida.

El TABLERO mide el canon; esto mide lo que espera para entrar en él. Un
minador propone (regla 5) y la propuesta se queda en algún sitio hasta que el
humano fusiona. Antes de la bandeja ese "algún sitio" era invisible: propuestas
en curiana_sim/, hallazgos en notas, borradores en el scratchpad de una sesión.

Escanea:
  6-fusion/*.yaml                  propuestas de datos (nodos, tablas)
  6-fusion/issues-pendientes/*.md  issues/comentarios redactados sin publicar
  curiana_sim/lexicon_*.py         propuestas léxicas — SE QUEDAN AHÍ porque el
                                   tooling las importa (generar_tablero,
                                   auditar_82, migrar_toponimos); medido
                                   2026-08-15. Se indexan en su sitio.

    python generar_bandeja.py
"""

import io
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUSION = RAIZ / "6-fusion"
SIM = RAIZ / "curiana_sim"

# Propuestas léxicas vivas en curiana_sim/ y por qué no se mueven.
# lexicon_zavala.py NO está: es generado Y lo importa el motor (trampa
# documentada en CLAUDE.md) — ya es canon-adyacente, no cola.
LEXICON_PROPUESTAS = {
    "lexicon_alvarado.py": ("alvarado-1921", "lo importan generar_tablero y auditar_82"),
    "lexicon_gatschet.py": ("gatschet-1885", "lo importan generar_tablero y auditar_82"),
    "lexicon_van_buurt.py": ("van-buurt-2014", "lo importan generar_tablero y auditar_82"),
    "lexicon_toponimos.py": ("varias (F11)", "lo importa migrar_toponimos"),
    "lexicon_candidatos.py": ("aisladas 2026-06-28", "lo importa generar_tablero"),
}

ENTRADA_PY = re.compile(r'^\s*"[^"]+":\s*\{', re.MULTILINE)


def _forzar_utf8():
    """La consola de Windows es cp1252 y revienta con « o ü."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


def contar_yaml(ruta):
    """(n_items, obra, aviso). Cuenta los ítems de la lista principal."""
    import yaml
    try:
        d = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    except Exception as e:
        return 0, "?", f"⚠️ no parsea: {e}"
    if not isinstance(d, dict):
        return 0, "?", "⚠️ estructura inesperada"
    meta = d.get("meta", {}) if isinstance(d.get("meta"), dict) else {}
    obra = str(meta.get("obra", "?"))
    listas = [(k, v) for k, v in d.items() if isinstance(v, list)]
    n = max((len(v) for _, v in listas), default=0)
    incompletos = meta.get("incompletos")
    aviso = f"{incompletos} incompletos" if incompletos else ""
    return n, obra, aviso


def es_vista(ruta):
    """El `generado_por` de la meta, si el YAML es una vista generada; si no, None."""
    import yaml
    try:
        d = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    except Exception:
        return None
    meta = d.get("meta", {}) if isinstance(d, dict) and isinstance(d.get("meta"), dict) else {}
    return meta.get("generado_por") or None


def titulo_md(ruta):
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        s = linea.strip().lstrip("#").strip()
        if s:
            return s[:90]
    return ruta.name


def main():
    if not FUSION.is_dir():
        print(f"✗ no existe {FUSION}")
        sys.exit(1)

    filas_datos = []
    filas_vistas = []
    for y in sorted(FUSION.glob("*.yaml")):
        n, obra, aviso = contar_yaml(y)
        # Una vista generada (meta.generado_por) junta lo que ya está en otras
        # propuestas: contarla sería contar dos veces. Se lista aparte.
        if es_vista(y):
            filas_vistas.append((y.name, es_vista(y)))
            continue
        filas_datos.append((y.name, obra, n, aviso))

    filas_issues = []
    pend = FUSION / "issues-pendientes"
    if pend.is_dir():
        for m in sorted(pend.glob("*.md")):
            filas_issues.append((m.name, titulo_md(m)))

    filas_lex = []
    for nombre, (obra, motivo) in LEXICON_PROPUESTAS.items():
        ruta = SIM / nombre
        if ruta.is_file():
            n = len(ENTRADA_PY.findall(ruta.read_text(encoding="utf-8")))
            filas_lex.append((nombre, obra, n, motivo))

    total = sum(f[2] for f in filas_datos) + sum(f[2] for f in filas_lex)

    L = [
        "---",
        "tipo: bandeja",
        "generado_por: curiana_sim/generar_bandeja.py",
        "editar_a_mano: no",
        "---",
        "",
        "# Bandeja de fusión — lo que espera para entrar al canon",
        "",
        "> ⚠️ **Archivo generado. No se edita a mano.** El TABLERO mide el canon;",
        "> esto mide la cola. Cada propuesta cita su obra (regla 8) y espera",
        "> fusión humana (regla 5). Regenerar:",
        "> ```",
        "> python curiana_sim/generar_bandeja.py",
        "> ```",
        "",
        f"<!--GENERADO--> Generado el **{date.today()}**.",
        "",
        f"**{total} ítems propuestos** en {len(filas_datos) + len(filas_lex)} "
        f"propuestas, más **{len(filas_issues)} issue(s)/comentario(s) redactados "
        "sin publicar**.",
        "",
        "## Propuestas de datos (`6-fusion/*.yaml`)",
        "",
        "| Archivo | Obra | Ítems | Aviso |",
        "|---|---|---|---|",
    ]
    for nombre, obra, n, aviso in filas_datos:
        L.append(f"| `{nombre}` | {obra} | {n} | {aviso} |")
    if filas_vistas:
        L += ["", "Vistas generadas en `6-fusion/` (no cuentan: juntan lo que ya está arriba):", ""]
        for nombre, gen in filas_vistas:
            L.append(f"- `{nombre}` — generado por `{gen}`")
    L += [
        "",
        "## Propuestas léxicas (`curiana_sim/lexicon_*.py` — indexadas en su sitio)",
        "",
        "Se quedan en `curiana_sim/` porque **el tooling las importa** (medido",
        "2026-08-15; la línea del CLAUDE.md que decía que no se importaban era",
        "falsa y se corrigió). Entradas contadas por patrón de dict.",
        "",
        "| Módulo | Obra | Entradas | Quién lo importa |",
        "|---|---|---|---|",
    ]
    for nombre, obra, n, motivo in filas_lex:
        L.append(f"| `{nombre}` | {obra} | {n} | {motivo} |")
    L += [
        "",
        "## Redactado y sin publicar (`6-fusion/issues-pendientes/`)",
        "",
        "El classifier de la sesión no puede publicar issues; se publican a mano",
        "con `gh issue create --body-file` / `gh issue comment --body-file`.",
        "",
        "| Archivo | Qué es |",
        "|---|---|",
    ]
    for nombre, titulo in filas_issues:
        L.append(f"| `{nombre}` | {titulo} |")
    L += [
        "",
        "---",
        "",
        "*Al fusionar una propuesta: mover el dato a su esfera con",
        "`procedencia.obra`, borrar o vaciar el archivo de la bandeja, y",
        "regenerar esto y el TABLERO.*",
        "",
    ]

    destino = FUSION / "BANDEJA.md"
    destino.write_text("\n".join(L), encoding="utf-8")
    print(f"  → 6-fusion/BANDEJA.md: {total} ítems en cola, "
          f"{len(filas_issues)} issue(s) sin publicar")


if __name__ == "__main__":
    _forzar_utf8()
    main()
