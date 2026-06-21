#!/usr/bin/env python3
"""
patch_integrate_comparative.py
==============================
Integra arahuaco_comparative.py al stack Curiana:

  1. Genera entradas Taíno hipotéticas desde el léxico Lokono
     → para añadir a curiana_lexicon.py (lengua: taino)
  2. Genera reconstrucciones proto-arahuacanas validadas
     → para añadir a curiana_lexicon.py (lengua: proto-arahuaco)
  3. Produce JSON listo para patch: taino_hipotetico.json
     y proto_arahuaco_reconstruido.json

Uso:
    python3 patch_integrate_comparative.py
    # Revisa los JSON generados, luego corre el patch con --apply
    python3 patch_integrate_comparative.py --apply /ruta/curiana_lexicon.py
"""

import json
import re
import sys
import shutil
from pathlib import Path
from arahuaco_comparative import (
    COGNADOS, transducir, reconstruir_taino, reconstruir_caquetio,
    tabla_comparativa
)

# =============================================================================
# 1. RECONSTRUCCIONES TAINO HIPOTETICAS
# Fuente: léxico Lokono completo (lokono_full_lexicon.json si existe,
# o COGNADOS directamente)
# =============================================================================

LOKONO_A_TAINO_EXTRA = {
    # palabras Lokono con buena confianza de reconstrucción Taíno
    "wakusi":    ("ojo",             "cuerpo"),
    "daka":      ("mano",            "cuerpo"),
    "thibisi":   ("diente",          "cuerpo"),
    "aduri":     ("nariz",           "cuerpo"),
    "abari":     ("cabeza",          "cuerpo"),
    "akoa":      ("pie",             "cuerpo"),
    "itime":     ("pez",             "fauna"),
    "kaiman":    ("caimán",          "fauna"),
    "iwana":     ("iguana",          "fauna"),
    "wabulo":    ("tortuga",         "fauna"),
    "siba":      ("piedra",          "geografia"),
    "kairi":     ("isla",            "geografia"),
    "tuna":      ("agua, río",       "geografia"),
    "marisi":    ("maíz",            "flora"),
    "achi":      ("ají",             "flora"),
    "yuka":      ("yuca",            "flora"),
    "kasabi":    ("casabe",          "alimentos"),
    "iuli":      ("tabaco",          "ritual"),
    "piaye":     ("chamán",          "ritual"),
    "aririn":    ("areito, danza ceremonial", "ritual"),
    "akkicyaha": ("espíritu vital",  "ritual"),
    "abba":      ("uno",             "gramatica"),
    "biama":     ("dos",             "gramatica"),
    "ma":        ("no, negación",    "gramatica"),
    "itti":      ("padre",           "parentesco"),
    "uju":       ("madre",           "parentesco"),
}

def generar_taino_hipotetico():
    """Genera dict de entradas Taíno hipotéticas desde Lokono."""
    entradas = {}
    for lok_word, (glosa, categoria) in LOKONO_A_TAINO_EXTRA.items():
        # Verificar si ya hay forma Taína atestiguada en COGNADOS
        for concepto, forms in COGNADOS.items():
            if forms.get("LK") == lok_word and forms.get("TN"):
                # Ya atestiguada — usar la atestiguada
                key = forms["TN"].replace("*", "").replace(" ", "_")
                entradas[key] = {
                    "es": glosa,
                    "fuente": "taino",
                    "notas": f"Taíno atestiguado: {forms['TN']}; cognado Lok. {lok_word}; Brinton 1871",
                    "categoria": categoria
                }
                break
        else:
            # Construir hipotético
            r = reconstruir_taino(lok_word, glosa)
            forma = r["taino_hipotetico"].lstrip("*")
            if forma and len(forma) > 1:
                key = forma.replace(" ", "_").replace("-", "_")
                entradas[key] = {
                    "es": glosa,
                    "fuente": "taino",
                    "notas": (f"Reconstrucción hipotética Taíno desde Lok. {lok_word}; "
                              f"método comparativo arahuacano; {r['nota']}; "
                              f"confianza: {r['confianza']}"),
                    "categoria": categoria
                }
    return entradas


# =============================================================================
# 2. PROTO-ARAHUACANAS RECONSTRUIDAS
# Desde los conjuntos de cognados, extraer todas las formas proto-arahuacanas
# con al menos 2 lenguas atestiguadas (para mayor confianza)
# =============================================================================

def generar_proto_reconstruidos():
    """Genera entradas proto-arahuacanas con soporte de ≥2 lenguas."""
    entradas = {}
    for concepto, forms in COGNADOS.items():
        pa = forms.get("PA")
        if not pa:
            continue
        # Contar cuántas lenguas tienen formas atestiguadas
        atestiguadas = [l for l in ["CQ", "WY", "LK", "TN"] if forms.get(l)]
        if len(atestiguadas) < 2:
            continue  # solo incluir si hay soporte de ≥2 lenguas

        key = pa.lstrip("*").replace(" ", "_").replace("-", "")
        glosa = forms.get("es", concepto)

        # Construir nota de soporte
        soporte = ", ".join(
            f"{l}: {forms[l]}" for l in ["CQ", "WY", "LK", "TN"] if forms.get(l)
        )

        entradas[key] = {
            "es": glosa,
            "fuente": "proto-arahuaco",
            "notas": (f"Proto-arahuaco {pa}; atestiguada en {len(atestiguadas)} lenguas: "
                      f"{soporte}; Payne (1991), Brinton (1871)"),
            "categoria": _inferir_categoria(glosa)
        }
    return entradas


def _inferir_categoria(glosa: str) -> str:
    """Infiere categoría semántica desde la glosa."""
    glosa = glosa.lower()
    if any(w in glosa for w in ["ojo", "mano", "diente", "nariz", "cabeza", "cuerpo", "pie",
                                  "corazón", "hueso", "sangre", "pecho", "vientre"]):
        return "cuerpo"
    if any(w in glosa for w in ["sol", "luna", "firmamento", "cielo", "estrella", "cosmos"]):
        return "cosmos"
    if any(w in glosa for w in ["río", "mar", "isla", "agua", "montaña", "tierra", "sabana",
                                  "piedra", "roca"]):
        return "geografia"
    if any(w in glosa for w in ["pez", "iguana", "caimán", "tortuga", "pájaro", "animal",
                                  "fauna", "mosco"]):
        return "fauna"
    if any(w in glosa for w in ["yuca", "maíz", "ají", "tabaco", "árbol", "palma", "flor",
                                  "fruta", "planta"]):
        return "flora"
    if any(w in glosa for w in ["casabe", "maíz", "pez", "alimento", "comer", "comida"]):
        return "alimentos"
    if any(w in glosa for w in ["chamán", "ritual", "areito", "espíritu", "danza",
                                  "ceremonia"]):
        return "ritual"
    if any(w in glosa for w in ["padre", "madre", "hijo", "hermano", "familia", "parentesco"]):
        return "parentesco"
    if any(w in glosa for w in ["uno", "dos", "tres", "no ", "negación", "prefijo"]):
        return "gramatica"
    if any(w in glosa for w in ["grande", "pequeño", "bueno", "malo"]):
        return "adjetivos"
    if any(w in glosa for w in ["canoa", "hamaca", "flecha", "arco", "casa"]):
        return "utiles"
    return "cosmos"


# =============================================================================
# 3. PATCH A curiana_lexicon.py
# =============================================================================

def build_entry_str(key, data, indent=4):
    """Genera el string Python de una entrada del vocabulario."""
    sp = " " * indent
    es   = data["es"].replace('"', '\\"')
    fnt  = data["fuente"]
    nota = data["notas"].replace('"', '\\"')
    cat  = data["categoria"]
    return (
        f'    "{key}": {{\n'
        f'        "es": "{es}",\n'
        f'        "fuente": "{fnt}",\n'
        f'        "notas": "{nota}",\n'
        f'        "categoria": "{cat}"\n'
        f'    }},\n'
    )

def apply_patch(lexicon_path: str, nuevas_entradas: dict, seccion: str):
    """Aplica las nuevas entradas a curiana_lexicon.py."""
    path = Path(lexicon_path)
    if not path.exists():
        print(f"ERROR: No encontré {lexicon_path}")
        return False

    original = path.read_text(encoding="utf-8")
    marker = "# -- FIN VOCABULARIO_BASE --"
    if marker not in original:
        print(f"ERROR: No encontré marcador '{marker}' en {lexicon_path}")
        return False

    # Detectar claves existentes
    existing = set(re.findall(r'"([^"]+)"\s*:\s*\{', original))
    nuevas = {k: v for k, v in nuevas_entradas.items() if k not in existing}

    if not nuevas:
        print(f"  [{seccion}] Todas las {len(nuevas_entradas)} entradas ya existen. Nada que hacer.")
        return True

    # Construir bloque a insertar
    bloque = f"\n    # --- {seccion} (arahuaco_comparative.py) ---\n"
    for key, data in sorted(nuevas.items()):
        bloque += build_entry_str(key, data)

    # Hacer backup y escribir
    backup = path.with_suffix(".bak")
    shutil.copy(path, backup)
    nuevo = original.replace(marker, bloque + marker)
    path.write_text(nuevo, encoding="utf-8")
    print(f"  [{seccion}] +{len(nuevas)} entradas nuevas de {len(nuevas_entradas)} totales")
    print(f"  Backup guardado en: {backup}")
    return True


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    taino_data    = generar_taino_hipotetico()
    proto_data    = generar_proto_reconstruidos()

    # Guardar JSON para revisión
    out_taino = Path("taino_hipotetico.json")
    out_proto = Path("proto_arahuaco_reconstruido.json")
    out_taino.write_text(json.dumps(taino_data, ensure_ascii=False, indent=2), encoding="utf-8")
    out_proto.write_text(json.dumps(proto_data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== PATCH COMPARATIVO ARAHUACANO ===\n")
    print(f"  Entradas Taíno hipotéticas generadas : {len(taino_data)}")
    print(f"  Entradas proto-arahuaco reconstruidas: {len(proto_data)}")
    print(f"\n  JSON de revisión guardado en:")
    print(f"    {out_taino}")
    print(f"    {out_proto}")

    # Muestreo
    print(f"\n  Muestra Taíno hipotético:")
    for k, v in list(taino_data.items())[:5]:
        print(f"    {k:<20} = {v['es']}")
    print(f"\n  Muestra proto-arahuaco:")
    for k, v in list(proto_data.items())[:5]:
        print(f"    {k:<20} = {v['es']}")

    # Aplicar si se pasa ruta
    if "--apply" in sys.argv:
        idx = sys.argv.index("--apply")
        if idx + 1 < len(sys.argv):
            lex_path = sys.argv[idx + 1]
            print(f"\n  Aplicando patch a: {lex_path}")
            apply_patch(lex_path, taino_data, "Taíno hipotético")
            apply_patch(lex_path, proto_data, "Proto-arahuaco reconstruido")
        else:
            print("ERROR: --apply requiere ruta a curiana_lexicon.py")
    else:
        print("\n  Para aplicar al léxico:")
        print("    python3 patch_integrate_comparative.py --apply /ruta/curiana_lexicon.py")
