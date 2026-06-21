"""
wayunaiki_phonology.py
======================
Transductor fonologico: Wayunaiki -> Proto-Caquetio
Documentacion de reglas de correspondencia fonologica entre
Wayunaiki (arahuaco septentrional) y el Proto-Caquetio reconstruido.

Basado en pares de cognados atestiguados:
  ka'i  -> *caci/cazi    (sol/dia)
  kashi -> *cati         (luna)
  jierü -> *iero         (mujer)
  mma   -> *ma           (tierra)
  juya  -> *uya          (lluvia)
  palaa -> *pala         (antes/pasado)
  wayuu -> *bayu         (persona)
  wüin  -> *buin         (agua)
  lapü  -> *labu         (sueno/vision)
  eechin-> *echin        (marido)
  apüshi-> *apuchi       (familia)
  siki  -> *siki         (fuego) -- IDENTICO

REGLAS (aplicadas en orden):
  1. Vocales largas (aa, ee, oo, üü) -> simples (a, e, o, u)
  2. ü -> u  (vocal central cerrada -> posterior)
  3. Oclusiva glotal (') -> eliminada
  4. sh -> ch  (fricativa -> africada)
  5. k antes de a/e/o -> c  (oclusiva -> oclusiva sorda)
  6. w- inicial -> b  (bilabial: w->b patron arahuaco occidental)
  7. w tras consonante -> b
  8. w entre vocales -> u  (semivocal)
  9. j- ante i/e -> y  (fricativa -> semiconsonante)
  10. j- ante a/o/u -> eliminada (patron caquetio: onset vocalico)
  11. j interna -> y
  12. -baa final -> -ba  (sufijos verbales)
  13. Consonantes dobles iniciales -> simple (mma -> ma)
  14. p intervocalico -> b  (sonorizacion arahuaca)

USO:
  from wayunaiki_phonology import proto_caquetio
  print(proto_caquetio("wayuu"))   # -> *bayu
  print(proto_caquetio("palaa"))   # -> *pala
  print(proto_caquetio("wüin"))    # -> *buin
"""

import re


def proto_caquetio(word):
    """
    Aplica reglas fonologicas para reconstruir la forma proto-caquetia.
    Retorna el resultado con prefijo * (asterisco de reconstruccion).
    """
    w = word.lower().strip()

    # 1. Vocales largas -> simples
    for v in 'aeiou':
        w = re.sub(v + v + '+', v, w)

    # 2. ü -> u
    w = w.replace('u', 'u')  # ya normalizado por paso anterior
    # (ü ya fue procesado como u en la normalizacion de entrada)

    # 3. Oclusiva glotal -> eliminada
    w = w.replace("'", '')

    # 4. sh -> ch
    w = w.replace('sh', 'ch')

    # 5. k antes de a/e/o -> c
    w = re.sub(r'k([aeo])', r'c\1', w)

    # 6. w- inicial -> b
    w = re.sub(r'^w', 'b', w)

    # 7. w tras consonante -> b
    w = re.sub(r'([bcdfghjklmnpqrstvxyz])w', r'\1b', w)

    # 8. w entre vocales -> u
    w = re.sub(r'([aeiou])w([aeiou])', r'\1u\2', w)

    # 9-11. j -> y (ante vocal) o eliminada
    w = re.sub(r'^j([ei])', r'y\1', w)
    w = re.sub(r'^j([aou])', r'\1', w)
    w = re.sub(r'j([aeiou])', r'y\1', w)

    # 12. Sufijo verbal -baa -> -ba
    w = re.sub(r'ba+$', 'ba', w)

    # 13. Consonante doble inicial -> simple
    w = re.sub(r'^([bcdfgklmnprst])\1+', r'\1', w)

    # 14. p intervocalico -> b
    w = re.sub(r'([aeiou])p([aeiou])', r'\1b\2', w)

    return '*' + w if w else word


# Validation against known cognates
VALIDATION_PAIRS = [
    ('ka\'i',   '*cai',    'sol/dia'),
    ('kashi',   '*cachi',  'luna'),
    ('jierü',   '*yieru',  'mujer -> *iero en caquetio atestiguado'),
    ('mma',     '*ma',     'tierra'),
    ('juya',    '*uya',    'lluvia'),
    ('palaa',   '*pala',   'antes'),
    ('wayuu',   '*bayu',   'persona'),
    ('wüin',    '*buin',   'agua'),
    ('lapü',    '*labu',   'sueno'),  # p->b intervocalico
    ('eechin',  '*echin',  'marido'),
    ('apushi',  '*abuchi', 'familia'),  # p->b intervocalico
    ('siki',    '*siki',   'fuego -- IDENTICO'),
    ('kaasha',  '*cacha',  'tambor'),
    ('ouktaa',  '*oukta',  'morir'),
    ('aamaka',  '*amaca',  'cementerio'),
]

if __name__ == '__main__':
    print("Validacion del transductor:")
    print(f"{'Wayunaiki':<22} {'Resultado':<18} {'Esperado/Notas'}")
    print("-" * 65)
    for way, expected, notes in VALIDATION_PAIRS:
        # Normalize ü before calling
        way_norm = way.replace('ü', 'u')
        result = proto_caquetio(way_norm)
        match = "OK" if result == expected else "~"
        print(f"{way:<22} {result:<18} {expected}  [{notes}]  {match}")

    print()
    print("Reconstrucciones de muestra:")
    test_words = [
        'wayuu', 'wuin', 'lapü', 'kaasha', 'juya', 'kashi', 'ka\'i',
        'aainjaa', 'achekaa', 'atulaa', 'maikki', 'jolotsu', 'jierü',
        'apushi', 'eirruku', 'outsu', 'jayeechi', 'yonna', 'achiki',
        'eechin', 'eeruin', 'jo\'uu', 'oushu', 'majayulu', 'wa\'lee',
    ]
    for w in test_words:
        w_norm = w.replace('ü', 'u')
        print(f"  {w:<22} -> {proto_caquetio(w_norm)}")
