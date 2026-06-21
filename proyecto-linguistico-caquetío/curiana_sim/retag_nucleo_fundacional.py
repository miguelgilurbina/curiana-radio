"""
CURIANA — Re-etiquetar el núcleo fundacional como caquetío
=============================================================
Las ~68 palabras de mayor frecuencia del proyecto (pronombres, numerales,
verbos básicos, conectores — el vocabulario que prompt_reglas_completo() y
prompt_reglas_breve() presentan a los agentes como SU lengua) estaban
etiquetadas por la lengua del cognado que justificó su forma (wayunaiki,
lokono, proto-arahuaco...), no como caquetío. Eso hacía que la nueva
penalización por "fuga a otra lengua arahuaca" castigara exactamente las
palabras que el proyecto siempre trató como caquetío de trabajo.

Este script cambia su "fuente" a "caquetío-reconstruido", preservando la
fuente original como nota etimológica.

Uso:
    python retag_nucleo_fundacional.py
"""

import re

LEXICON_FILE = "curiana_lexicon.py"

CLAVES = [
    'ama', 'amana', 'ana', 'anüiki', 'apünüin', 'arima', 'arua', 'awa', 'baba',
    'bana', 'bara', 'bari', 'buri', 'canoa', 'chaa', 'conuco', 'dali', 'duna',
    'habo', 'hamaca', 'jarai', 'ka', 'kaa', 'kabo', 'kali', 'kapua', 'kasha',
    'kashi', 'kaya', 'kira', 'kono', 'kuru', 'ma', 'maa', 'mara', 'masa',
    'naa', 'naba', 'naka', 'naya', 'nii', 'nomi', 'nüma', 'paa', 'panaa',
    'pia', 'piama', 'pienchi', 'puna', 'pütchi', 'raka', 'rua', 'saa', 'sima',
    'suka', 'sulu', 'suna', 'taa', 'taya', 'tüshi', 'waa', 'wana', 'wanee',
    'wanü', 'wara', 'wari', 'waya', 'yama',
]


def main():
    with open(LEXICON_FILE, encoding="utf-8") as f:
        contenido = f.read()

    retagueadas = 0
    ya_caquetio = 0
    no_encontradas = []

    for clave in CLAVES:
        patron = re.compile(
            r'(^\s*"' + re.escape(clave) + r'":\s*\{[^}]*?"fuente":\s*")([^"]+)(")',
            re.MULTILINE,
        )
        m = patron.search(contenido)
        if not m:
            no_encontradas.append(clave)
            continue

        fuente_original = m.group(2)
        if "caquet" in fuente_original.lower():
            ya_caquetio += 1
            continue

        nueva_linea = m.group(1) + "caquetío-reconstruido" + m.group(3)
        # Inserta nota etimológica antes de "fuente" si hay "notas"; si no, la añade.
        inicio, fin = m.span()
        bloque = contenido[inicio:fin]
        if '"notas"' in bloque:
            contenido = contenido[:inicio] + nueva_linea + contenido[fin:]
        else:
            # Insertar "notas" justo antes de "fuente" para no perder la procedencia
            nueva_linea_con_nota = (
                m.group(1).rsplit('"fuente"', 1)[0]
                + f'"notas": "núcleo fundacional, forma justificada por cognado en {fuente_original}", '
                + '"fuente": "'
                + "caquetío-reconstruido"
                + m.group(3)
            )
            contenido = contenido[:inicio] + nueva_linea_con_nota + contenido[fin:]
        retagueadas += 1

    with open(LEXICON_FILE, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"Re-etiquetadas: {retagueadas}")
    print(f"Ya eran caquetío: {ya_caquetio}")
    if no_encontradas:
        print(f"No encontradas en el lexicón ({len(no_encontradas)}): {no_encontradas}")


if __name__ == "__main__":
    main()
