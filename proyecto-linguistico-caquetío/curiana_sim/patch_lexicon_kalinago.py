#!/usr/bin/env python3
"""
patch_lexicon_kalinago.py
=========================
Añade vocabulario Kalinago/Garifuna (6ª lengua arahuaca) a curiana_lexicon.py.

Dos capas:
  - fuente "kalinago"               → sustrato arahuaco (Breton 1665, Garifuna moderno)
  - fuente "kalinago-caribe-overlay"→ overlay caribe (vocabulario masculino/de combate)

Idempotente: verifica existencia de "buyei" antes de insertar.

Uso:
  python patch_lexicon_kalinago.py [ruta_a_curiana_lexicon.py]
"""

import sys, re

MARKER = "# -- FIN VOCABULARIO_BASE --"

# ── SUSTRATO ARAHUACO del Kalinago (COGNADOS[KL] del módulo comparativo) ──
# Fuentes: Breton (1665) Dictionnaire caraïbe-français;
#          Taylor (1951) The Black Carib of British Honduras;
#          Hoff (1968) The Carib Language; Garifuna moderno documentado.
KALINAGO_ARAHUACO = '''
    # ── KALINAGO — SUSTRATO ARAHUACO (Breton 1665; Taylor 1951; Hoff 1968) ──
    "kati":     {"es": "luna, mes", "fuente": "kalinago", "notas": "Breton (1665) kati/mois; cognado directo de CQ cati, LK katsi, PA *kati", "categoria": "cosmos"},
    "barana":   {"es": "mar, agua extensa", "fuente": "kalinago", "notas": "Garifuna barana = gran cuerpo de agua; cognado de CQ para, LK bara, PA *para", "categoria": "geografia"},
    "kasabi":   {"es": "casabe, pan de yuca", "fuente": "kalinago", "notas": "Kalinago kasabi; idéntico a LK kasabi, CQ casabe; término central de la identidad cultural", "categoria": "alimentos"},
    "buyei":    {"es": "chamán, curandero ritual", "fuente": "kalinago", "notas": "Breton (1665) buyei; cognado irregular de LK piaye (p→b, ia→u, ye→ei); figura ritual paralela al piache caquetío", "categoria": "cosmos"},
    "iwana":    {"es": "iguana (Iguana iguana)", "fuente": "kalinago", "notas": "Garifuna iwana; conservado igual que LK iwana, WY iwana, PA *iwana", "categoria": "fauna"},
    "kairi":    {"es": "isla, cayo", "fuente": "kalinago", "notas": "Garifuna kairi; conservado igual que LK kairi, CQ cairi; Cairi = nombre arahuaco de Trinidad", "categoria": "geografia"},
    "yuka":     {"es": "yuca, mandioca (Manihot esculenta)", "fuente": "kalinago", "notas": "Garifuna yuka; idéntico a LK yuka, CQ yuca, PA *yuka; base alimentaria de la cultura Kalinago", "categoria": "flora"},
    "marisi":   {"es": "maíz (Zea mays)", "fuente": "kalinago", "notas": "Garifuna marisi; cognado de LK marisi, TN maisi (→ esp. maíz), PA *marisi", "categoria": "flora"},
    "achi":     {"es": "ají, pimienta (Capsicum sp.)", "fuente": "kalinago", "notas": "Garifuna achi; idéntico a LK achi; cognado de TN aji, PA *achi", "categoria": "flora"},
    "kalinagu": {"es": "Kalinago, gente propia (autónimo)", "fuente": "kalinago", "notas": "Autónimo Kalinago: kalina (Carib: gente del lugar) + -gu (arahuaco: gente/colectivo); compuesto híbrido que refleja la naturaleza de contacto de la lengua", "categoria": "parentesco"},
    "ikoa":     {"es": "casa, vivienda", "fuente": "kalinago", "notas": "Garifuna ikoa; LK sikoa → ikoa (pérdida s- inicial); PA *isikoa", "categoria": "arquitectura"},
    "duna":     {"es": "agua, río", "fuente": "kalinago", "notas": "Garifuna duna; LK tuna → duna (sonorización t→d inicial); CQ tuy, PA *tuna", "categoria": "geografia"},
    "hamaka":   {"es": "hamaca, cama colgante", "fuente": "kalinago", "notas": "Garifuna hamaka; conservado igual que PA *hamaka, CQ hamaca, LK hamaha; préstamo pan-arahuaco al español", "categoria": "utiles"},
    "aban":     {"es": "uno", "fuente": "kalinago", "notas": "Garifuna aban; LK abba → aban (bb→b + nasal final); WY aba, PA *aba", "categoria": "numerales"},
    "biama":    {"es": "dos", "fuente": "kalinago", "notas": "Garifuna biama; conservado igual que LK biama, PA *biama", "categoria": "numerales"},
    "ma":       {"es": "no, negación (prefijo)", "fuente": "kalinago", "notas": "Pan-arahuaco: KL ma, WY ma, LK ma, TN mayani; base gramatical conservada en todos los grupos", "categoria": "gramatica"},
    "kasaku":   {"es": "firmamento, bóveda celeste", "fuente": "kalinago", "notas": "Garifuna kasaku; LK kassaku → kasaku (ss→s); sustrato arahuaco en cosmología Kalinago", "categoria": "cosmos"},
    "hiñaru":   {"es": "persona, ser humano (registro femenino Kalinago)", "fuente": "kalinago", "notas": "Breton (1665) registro femenino/neutro; LK hianaro; refleja la gramática arahuaca del Kalinago; el 'registro de las mujeres' documentado por los misioneros", "categoria": "parentesco"},
    "kalínagu": {"es": "Caribe, kalínagu (autónimo del pueblo Caribe insular)", "fuente": "kalinago", "notas": "El autónimo del pueblo que los españoles llamaron 'Caribes'; raíz de 'Kalinago' y del moderno 'Garifuna'; cognado arahuaco: CQ karibna, LK karibna", "categoria": "parentesco"},
'''

# ── OVERLAY CARIBE del Kalinago (vocabulario masculino/de combate) ──
# Documentado por Breton (1665) como "palabras de los hombres"
KALINAGO_CARIBE = '''
    # ── KALINAGO — OVERLAY CARIBE (vocabulario masculino; Breton 1665) ──
    "baruwa":   {"es": "hombre (registro masculino Kalinago)", "fuente": "kalinago-caribe-overlay", "notas": "Breton (1665) registro masculino; origen caribe; contraparte de hiñaru (arahuaco); la dualidad baruwa/hiñaru es evidencia del proceso de contacto que generó el Kalinago", "categoria": "parentesco"},
    "kanawa":   {"es": "canoa (forma caribe del Kalinago)", "fuente": "kalinago-caribe-overlay", "notas": "Forma caribe que desplazó al arahuaco kanoa/kannoa en contexto náutico-masculino; ambas formas coexistieron en distintos registros del Kalinago según Breton (1665)", "categoria": "navegacion"},
    "pira":     {"es": "pez, pescado (forma caribe del Kalinago)", "fuente": "kalinago-caribe-overlay", "notas": "Origen caribe; cf. piraña = pira + aña (diente en Tupí); el overlay caribe dominó el vocabulario de pesca en el registro masculino Kalinago; contrasta con el arahuaco LK itime", "categoria": "fauna"},
    "amourou":  {"es": "guerra, combate", "fuente": "kalinago-caribe-overlay", "notas": "Breton (1665); vocabulario bélico casi exclusivamente caribe en Kalinago; ausencia del término arahuaco equivalente en registro masculino", "categoria": "guerra"},
'''


def apply_patch(lexicon_path: str, nuevas_entradas: str, seccion: str) -> int:
    with open(lexicon_path, "r", encoding="utf-8") as f:
        content = f.read()

    if MARKER not in content:
        print(f"ERROR: marcador '{MARKER}' no encontrado en {lexicon_path}")
        return -1

    # Verificar idempotencia
    check_key = '"buyei"'
    if check_key in content:
        print(f"SKIP [{seccion}]: '{check_key}' ya existe — patch ya aplicado.")
        return 0

    nuevo_content = content.replace(
        MARKER,
        nuevas_entradas.rstrip() + "\n    " + MARKER
    )

    with open(lexicon_path, "w", encoding="utf-8") as f:
        f.write(nuevo_content)

    nuevas = len(re.findall(r'"[a-záéíóúüñ_]+"\s*:', nuevas_entradas))
    print(f"OK [{seccion}]: +{nuevas} entradas insertadas.")
    return nuevas


if __name__ == "__main__":
    import os
    lexicon = sys.argv[1] if len(sys.argv) > 1 else "curiana_lexicon.py"

    if not os.path.exists(lexicon):
        print(f"ERROR: no se encuentra {lexicon}")
        sys.exit(1)

    n1 = apply_patch(lexicon, KALINAGO_ARAHUACO, "kalinago-sustrato")
    n2 = apply_patch(lexicon, KALINAGO_CARIBE,   "kalinago-caribe-overlay")

    if n1 >= 0 and n2 >= 0:
        total = n1 + n2
        print(f"\nTotal nuevas entradas Kalinago: {total}")
        print("Fuentes:")
        print("  kalinago                  (sustrato arahuaco)")
        print("  kalinago-caribe-overlay   (vocabulario masculino/combate)")
