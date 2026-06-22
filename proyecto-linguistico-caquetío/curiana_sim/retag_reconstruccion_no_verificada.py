"""
CURIANA — Reetiquetar las reconstrucciones sin verificacion de cognacion
==========================================================================
reconstruir_caquetio_gaps.py + aplicar_reconstruccion.py generaron 441
palabras "caquetío-reconstruido" transduciendo CUALQUIER palabra de los
diccionarios masivos wayunaiki/lokono/taíno que compartiera una glosa,
sin verificar contra COGNADOS (el set de 37 cognados con evidencia real
de parentesco entre lenguas). La mineria de pares de validacion
(minar_pares_validacion.py) mostro que, de los pares objetivos disponibles
(forma caquetia atestiguada + forma hermana para el mismo concepto), un
80% predijo formas completamente alejadas de la real — evidencia de que
muchas de esas 441 palabras no son cognados genuinos, solo transducciones
fonologicas de palabras no relacionadas.

Este script retaguea esas 441 a "hipotetico-no-verificado", EXCLUYENDO las
68 palabras del nucleo fundacional (retag_nucleo_fundacional.py) que son
el vocabulario de trabajo del proyecto desde el inicio, no producto de
este pipeline sin verificacion.

Uso:
    python retag_reconstruccion_no_verificada.py
"""

import re

LEXICON_FILE = "curiana_lexicon.py"

# Las 68 claves del núcleo fundacional (retag_nucleo_fundacional.py) — estas
# se EXCLUYEN del reetiquetado, quedan como caquetío-reconstruido.
NUCLEO_FUNDACIONAL = {
    'ama', 'amana', 'ana', 'anüiki', 'apünüin', 'arima', 'arua', 'awa', 'baba',
    'bana', 'bara', 'bari', 'buri', 'canoa', 'chaa', 'conuco', 'dali', 'duna',
    'habo', 'hamaca', 'jarai', 'ka', 'kaa', 'kabo', 'kali', 'kapua', 'kasha',
    'kashi', 'kaya', 'kira', 'kono', 'kuru', 'ma', 'maa', 'mara', 'masa',
    'naa', 'naba', 'naka', 'naya', 'nii', 'nomi', 'nüma', 'paa', 'panaa',
    'pia', 'piama', 'pienchi', 'puna', 'pütchi', 'raka', 'rua', 'saa', 'sima',
    'suka', 'sulu', 'suna', 'taa', 'taya', 'tüshi', 'waa', 'wana', 'wanee',
    'wanü', 'wara', 'wari', 'waya', 'yama',
}


def main():
    with open(LEXICON_FILE, encoding="utf-8") as f:
        contenido = f.read()

    patron = re.compile(
        r'^(\s*"([^"]+)":\s*\{[^}]*?"fuente":\s*")caquetío-reconstruido(")',
        re.MULTILINE,
    )

    retagueadas = 0
    excluidas = 0

    def reemplazar(m):
        nonlocal retagueadas, excluidas
        clave = m.group(2)
        if clave in NUCLEO_FUNDACIONAL:
            excluidas += 1
            return m.group(0)
        retagueadas += 1
        return m.group(1) + "hipotético-no-verificado" + m.group(3)

    nuevo_contenido = patron.sub(reemplazar, contenido)

    with open(LEXICON_FILE, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)

    print(f"Re-etiquetadas a 'hipotético-no-verificado': {retagueadas}")
    print(f"Excluidas (núcleo fundacional, quedan caquetío-reconstruido): {excluidas}")


if __name__ == "__main__":
    main()
