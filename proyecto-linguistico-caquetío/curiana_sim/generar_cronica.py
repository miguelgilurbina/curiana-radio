"""Genera 1-plan/CRONICA.md — el registro crudo de cambios, desde git.

La LINEA_DE_TIEMPO es la narrativa curada (las eras, las lecciones); esta
crónica es el registro completo: cada cambio que llegó a main, con su fecha,
regenerable en cualquier momento. Existe porque el registro se mantenía a mano
dentro de la línea de tiempo ("commits: 78, actualizado 2026-08-03") y murió
por deriva — la enfermedad exacta que la regla 1 existe para curar.

    python generar_cronica.py
"""

import io
import subprocess
import sys
from collections import OrderedDict
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "1-plan" / "CRONICA.md"
SEP = "\x1f"  # separador que no aparece en mensajes de commit


def _forzar_utf8():
    """La consola de Windows es cp1252 y revienta con « o ü."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


def commits_de_main():
    """[(fecha, hash, asunto)] de main, primer padre (= nivel PR)."""
    r = subprocess.run(
        ["git", "log", "--first-parent", "--date=format:%Y-%m-%d",
         f"--pretty=%ad{SEP}%h{SEP}%s", "main"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=RAIZ, check=True,
    )
    filas = []
    for linea in r.stdout.splitlines():
        partes = linea.split(SEP, 2)
        if len(partes) == 3:
            filas.append(tuple(partes))
    return filas


def main():
    filas = commits_de_main()
    if not filas:
        print("✗ git log no devolvió nada")
        sys.exit(1)

    por_mes = OrderedDict()  # git log ya viene de nuevo → viejo
    for fecha, h, asunto in filas:
        por_mes.setdefault(fecha[:7], []).append((fecha, h, asunto))

    primera, ultima = filas[-1][0], filas[0][0]

    L = [
        "---",
        "tipo: cronica",
        "generado_por: curiana_sim/generar_cronica.py",
        "editar_a_mano: no",
        "---",
        "",
        "# Crónica — todo lo que llegó a main, con fecha",
        "",
        "> ⚠️ **Archivo generado. No se edita a mano.** Este es el registro",
        "> crudo; la narrativa curada (las eras, qué significó cada tramo) vive",
        "> en [[LINEA_DE_TIEMPO]]. Regenerar:",
        "> ```",
        "> python curiana_sim/generar_cronica.py",
        "> ```",
        "",
        f"<!--GENERADO--> Generado el **{date.today()}**. "
        f"**{len(filas)} cambios** en main, del {primera} al {ultima}.",
        "",
    ]

    for mes, items in por_mes.items():
        L.append(f"## {mes} — {len(items)} cambio(s)")
        L.append("")
        for fecha, h, asunto in items:
            L.append(f"- **{fecha}** `{h}` {asunto}")
        L.append("")

    SALIDA.write_text("\n".join(L), encoding="utf-8")
    print(f"  → 1-plan/CRONICA.md: {len(filas)} cambios, "
          f"{len(por_mes)} meses ({primera} → {ultima})")


if __name__ == "__main__":
    _forzar_utf8()
    main()
