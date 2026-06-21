#!/usr/bin/env python3
"""
patch_lexicon_jirajaroide.py
============================
Añade vocabulario de zona de frontera Jirajaroide a curiana_lexicon.py.

Fuente: jirajaroide_frontera_lexicon.json
Solo inserta entradas con pendiente=False (las atestiguadas por toponimia).
Las entradas PENDIENTE quedan excluidas hasta verificación directa de Oramas (1916).

Fuente en lexicón: "jirajaroide-contacto"

Idempotente: verifica existencia de "xira" antes de insertar.

Uso:
  python patch_lexicon_jirajaroide.py [ruta_a_curiana_lexicon.py]
"""

import sys, re, json, os

MARKER = "# -- FIN VOCABULARIO_BASE --"

# Entradas atestiguadas hardcodeadas desde jirajaroide_frontera_lexicon.json
# (para evitar dependencia de ruta en tiempo de ejecución de Claude Code)
# Fuentes: Oramas (1916), Jahn (1927), Alcalá (1954), toponimia histórica.
# Nota: doaca/yarosabana/yaruca ya vienen del patch caquetío-atestiguado (Tarea 3).
JIRAJAROIDE_CONTACTO = '''
    # ── JIRAJAROIDE — ZONA DE CONTACTO (toponimia atestiguada; Oramas 1916; Jahn 1927) ──
    # Nota: fuente "jirajaroide-contacto" = término registrado en zona fronteriza
    # caquetío-jirajaroide (Sierra de Coro, Falcón occidental, Lara norte).
    # Las entradas marcadas con [CQ-exónimo] son posiblemente nombres caquetíos
    # para grupos jirajaroide, no autónimos de los propios grupos.
    "xira":        {"es": "raíz del etnónimo Jirajara (probable: serranos, gente de la sierra)", "fuente": "jirajaroide-contacto", "notas": "Raíz de Xirahara/Jirajara; puede ser exónimo caquetío, no autónimo Jirajara; attested en variantes ortográficas coloniales Xirajara, Jirajara, Xiraxara [CQ-exónimo]", "categoria": "etnonimia"},
    "buria":       {"es": "valle aurífero en serranía (topónimo Jirajaroide)", "fuente": "jirajaroide-contacto", "notas": "Buria = valley en Yaracuy/Lara; zona de extracción aurífera prehispánica; posiblemente relacionado con término Jirajaroide para mineral/tierra amarilla; Relaciones Geográficas 1578", "categoria": "geografia"},
    "nirgua":      {"es": "asentamiento Jirajaroide en Yaracuy (topónimo)", "fuente": "jirajaroide-contacto", "notas": "Nirgua = municipio Yaracuy; territorio de frontera caquetío-jirajaroide; origen lingüístico no determinado con certeza entre Jirajara y Ayamán; Jahn 1927", "categoria": "geografia"},
    "churuguara":  {"es": "territorio Gayón en Falcón serrano (topónimo)", "fuente": "jirajaroide-contacto", "notas": "Churuguara = municipio Falcón; corazón del territorio Gayón; Gayones = rama Jirajaroide de Sierra de Coro y Falcón occidental, vecinos DIRECTOS de Curiana; Oramas 1916", "categoria": "geografia"},
    "ayaman":      {"es": "grupo Jirajaroide del Lara-Falcón (etnonimia/topónimo)", "fuente": "jirajaroide-contacto", "notas": "Ayamán = etnónimo y topónimo; municipio Lara; una de las cuatro ramas Jirajaroide conocidas (Jirajara, Ayamán, Gayón, Ajagua); Oramas 1916; Jahn 1927", "categoria": "etnonimia"},
    "ajagua":      {"es": "grupo Jirajaroide (Jirajaroid menor)", "fuente": "jirajaroide-contacto", "notas": "Ajagua = cuarto grupo de la familia Jirajaroide; menos documentado que los otros tres; territorio en zona de contacto Lara-Falcón; Oramas 1916", "categoria": "etnonimia"},
    "quibor":      {"es": "valle agrícola del Lara interior (topónimo)", "fuente": "jirajaroide-contacto", "notas": "Quibor = municipio Lara, valle fértil; zona de frontera caquetío-jirajaroide; origen lingüístico disputado; Alcalá 1954; topónimo clave en ruta de intercambio maíz-sal-conchas", "categoria": "geografia"},
'''


def apply_patch(lexicon_path: str) -> int:
    with open(lexicon_path, "r", encoding="utf-8") as f:
        content = f.read()

    if MARKER not in content:
        print(f"ERROR: marcador '{MARKER}' no encontrado en {lexicon_path}")
        return -1

    # Verificar idempotencia
    check_key = '"xira"'
    if check_key in content:
        print(f"SKIP: '{check_key}' ya existe — patch jirajaroide ya aplicado.")
        return 0

    nuevo_content = content.replace(
        MARKER,
        JIRAJAROIDE_CONTACTO.rstrip() + "\n    " + MARKER
    )

    with open(lexicon_path, "w", encoding="utf-8") as f:
        f.write(nuevo_content)

    nuevas = len(re.findall(r'"[a-záéíóúüñ_]+"\s*:', JIRAJAROIDE_CONTACTO))
    print(f"OK [jirajaroide-contacto]: +{nuevas} entradas insertadas.")
    print()
    print("NOTA: Las 13 entradas PENDIENTES en jirajaroide_frontera_lexicon.json")
    print("quedan EXCLUIDAS hasta verificación directa de Oramas (1916).")
    print("Para añadirlas: editar este script o crear patch_jirajaroide_v2.py")
    print("con los términos verificados.")
    return nuevas


if __name__ == "__main__":
    lexicon = sys.argv[1] if len(sys.argv) > 1 else "curiana_lexicon.py"

    if not os.path.exists(lexicon):
        print(f"ERROR: no se encuentra {lexicon}")
        sys.exit(1)

    n = apply_patch(lexicon)
    if n > 0:
        print(f"\nTotal nuevas entradas Jirajaroide: {n}")
        print("Fuente: jirajaroide-contacto")
