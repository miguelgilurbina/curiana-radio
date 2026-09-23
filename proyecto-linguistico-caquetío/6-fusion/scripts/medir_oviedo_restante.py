#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mide `6-fusion/oviedo_restante_2026-09-22.yaml` (parcela M3) y escribe
`meta.cobertura` y `meta.sondas_medidas`. Ninguna cifra se escribe a mano
(regla 1).

    python 6-fusion/scripts/medir_oviedo_restante.py            # mide y escribe
    python 6-fusion/scripts/medir_oviedo_restante.py --check    # mide y no escribe
    python 6-fusion/scripts/medir_oviedo_restante.py --sin-pdf  # sólo la cobertura del YAML

`sondas_medidas` lee los cuatro PDF de Oviedo con pymupdf (el tomo I en la
copia íntegra de archive.org, y también en la truncada para comparar) y cuenta,
con el guion de fin de línea deshecho: la familia de `guaitiao`, las sondas de
ortografía dentro del libro XIX y el desfase pdf → impresa de la copia íntegra.
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YAML = os.path.join(RAIZ, '6-fusion', 'oviedo_restante_2026-09-22.yaml')
FUENTES = os.path.join(RAIZ, 'fuentes_caquetios')
PDFS = {
    'I': 'Oviedo_Valdes_1851_Historia_General_Indias_vol1_completo.pdf',
    'I_truncado': 'Oviedo_Valdes_1851_Historia_General_Indias_vol1.pdf',
    'II': 'Oviedo_Valdes_1852_Historia_General_Indias_vol2.pdf',
    'III': 'Oviedo_Valdes_1853_Historia_General_Indias_vol3.pdf',
    'IV': 'Oviedo_Valdes_1855_Historia_General_Indias_vol4.pdf',
}
# el libro XIX en la copia íntegra: pdf 705 (impresa 586) a 733 (impresa 614)
LIBRO_XIX_PDF = (705, 733)

SONDAS_GUAITIAO = {
    'g-u-a-(i)-t-i-a-o': r'g\w?[uún][aáo]?[iy]?[tlíif1][iíl1]?[aá]o',
    '…tiao': r'\w*tiao\w*',
    '…tihao': r'\w*tihao\w*',
    '…lihao': r'\w*lihao\w*',
}
SONDAS_XIX = {
    'çaquitio': r'\b[çcgfzrs]a[qg][uüi]{0,2}[i1íltj]{1,2}t[i1íl]o',
    'Coro': r'\bCoro\b',
    'Paraguaná': r'Paragu?[aá]n|Paragoan',
    'Quiquibacoa/Coquibacoa': r'[CQ]u?[io]qu?[iíy]bacoa',
    'Curiana/Coriana': r'C[uo]r[iy]ana',
    'Corazao/Curaçao': r'C[ou]ra[çcgfz]a[on]|Coraza?n[tl]e',
    'Aruba': r'\bA[rn][uüi]ba\b',
    'Boynare/Bonaire': r'Bo[yi]j?n[aá]r[ec]|Bonai?re',
    'Manaure': r'Mana[uv]re',
    'Veneçuela': r'Vene[çcgfzr5]u?e?la|Venez?uela',
    'Cubagua': r'Cubagua',
    'Cumaná': r'C\.?[uú]man[aá]',
}


def _forzar_utf8() -> None:
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass


def cargar():
    import yaml
    with io.open(YAML, encoding='utf-8') as fh:
        return yaml.safe_load(fh)


def _lista(v):
    if v is None:
        return []
    return list(v) if isinstance(v, list) else [v]


def _paginas(e) -> list:
    p = e.get('pagina_impresa')
    if isinstance(p, dict):
        out = []
        for v in p.values():
            out += _lista(v)
        return [x for x in out if isinstance(x, int)]
    return [x for x in _lista(p) if isinstance(x, int)]


def _tomos(e) -> list:
    t = e.get('tomo')
    if t is not None:
        return [str(x) for x in _lista(t)]
    obra = e.get('obra', '')
    return ['I'] if obra == 'oviedo-y-valdes-1851' else ['?']


# ── cobertura del YAML ───────────────────────────────────────────────
def medir_yaml(d: dict) -> dict:
    fauna = [e for e in (d.get('fauna') or []) if isinstance(e, dict)]
    con_sonido = [e for e in fauna if e.get('sonido')]
    comparacion = [e for e in fauna if e.get('solo_comparacion')]
    por_ver = Counter(str(e.get('verificacion', 'sin-declarar')).split(' ')[0] for e in fauna)
    por_tomo = Counter(t for e in fauna for t in _tomos(e))

    voces, voces_ver = [], Counter()
    for sec in ('voces_de_tierra_firme', 'voces_tainas_nuevas'):
        for e in d.get(sec) or []:
            fs = _lista(e.get('forma_fuente'))
            voces += [(sec, str(f)) for f in fs]
            voces_ver[str(e.get('verificacion', '')).split(' ')[0]] += len(fs)

    paginas = {}
    for sec in ('fauna', 'voces_de_tierra_firme', 'voces_tainas_nuevas'):
        for e in d.get(sec) or []:
            for t in _tomos(e):
                paginas.setdefault(t, set()).update(_paginas(e))

    return {
        'fauna_entradas': len(fauna),
        'fauna_con_sonido': len(con_sonido),
        'fauna_solo_comparacion_la_espanola': len(comparacion),
        'fauna_por_verificacion': dict(sorted(por_ver.items())),
        'fauna_por_tomo': dict(sorted(por_tomo.items())),
        'voces_formas': len(voces),
        'voces_de_tierra_firme': sum(1 for s, _ in voces if s == 'voces_de_tierra_firme'),
        'voces_tainas_nuevas': sum(1 for s, _ in voces if s == 'voces_tainas_nuevas'),
        'voces_por_verificacion': dict(sorted(voces_ver.items())),
        'paginas_impresas_citadas_por_tomo': {k: len(v) for k, v in sorted(paginas.items())},
        'correcciones': len(d.get('correcciones') or []),
    }


# ── sondas sobre los PDF ─────────────────────────────────────────────
def _dehyph(t: str) -> str:
    t = re.sub(r'(\w)[-¬]\s*\n\s*(\w)', r'\1\2', t)
    return re.sub(r'[ \t]+', ' ', t.replace('\n', ' '))


def _paginas_pdf(clave: str) -> list:
    import pymupdf
    ruta = os.path.join(FUENTES, PDFS[clave])
    if not os.path.exists(ruta):
        return []
    doc = pymupdf.open(ruta)
    return [_dehyph(doc[i].get_text()) for i in range(doc.page_count)]


_FIX = str.maketrans({'O': '0', 'o': '0', 'l': '1', 'I': '1', 'i': '1', 'S': '5',
                      'B': '8', 'G': '6', 'g': '9', 'Z': '2', 'z': '2'})


def _numeros_de_cabecera(txt: str) -> list:
    cab = txt[:90]
    out = []
    for tok in re.findall(r'\b[0-9OolIiSBGgZz]{2,3}\b', cab):
        if re.search(r'\d', tok):
            s = tok.translate(_FIX)
            if s.isdigit():
                out.append(int(s))
    return out


def medir_pdfs() -> dict:
    textos = {k: _paginas_pdf(k) for k in PDFS}
    res = {'paginas_pdf': {k: len(v) for k, v in textos.items()}}

    g = {}
    for k, pags in textos.items():
        if not pags:
            continue
        todo = ' '.join(pags)
        g[k] = {n: len(re.findall(p, todo, re.I)) for n, p in SONDAS_GUAITIAO.items()}
        # la familia -iao entera: qué palabras hay, para que el cero se vea
        pal = Counter(w.lower() for w in re.findall(r'\b\w*[iíy1l][aá][o0]s?\b', todo)
                      if len(w) >= 5 and not w.lower().endswith('ciao'))
        g[k]['palabras_en_-iao'] = sorted(pal)
    res['guaitiao'] = g

    # datihao / dalihao en las dos copias del t. I
    res['datihao_vs_dalihao'] = {
        k: {'datihao': sum(len(re.findall(r'\bdatihao\b', p, re.I)) for p in textos[k]),
            'dalihao': sum(len(re.findall(r'\bdalihao\b', p, re.I)) for p in textos[k])}
        for k in ('I', 'I_truncado') if textos.get(k)}

    # tatara / talara (el OCR miente; la imagen dice tatara)
    res['tatara_vs_talara_ocr'] = {
        k: {'tatara': sum(len(re.findall(r'\btatara\b', p, re.I)) for p in textos[k]),
            'talara': sum(len(re.findall(r'\btalara\b', p, re.I)) for p in textos[k])}
        for k in ('I', 'I_truncado') if textos.get(k)}

    # sondas dentro del libro XIX (copia íntegra)
    a, b = LIBRO_XIX_PDF
    xix = ' '.join(textos['I'][a:b + 1]) if textos.get('I') else ''
    res['libro_XIX_sondas'] = {n: len(re.findall(p, xix, re.I if n not in ('Coro',) else 0))
                               for n, p in SONDAS_XIX.items()}

    # desfase de la copia íntegra del t. I (cuerpo: pdf 119-733)
    c, legibles = Counter(), 0
    for i in range(119, 734):
        nums = [n for n in _numeros_de_cabecera(textos['I'][i]) if 1 <= n <= 640]
        if nums:
            legibles += 1
            c[i - nums[0]] += 1
    moda, veces = c.most_common(1)[0] if c else (None, 0)
    res['desfase_tomo_I_copia_integra'] = {
        'impresa_igual_a_pdf_menos': moda,
        'encabezados_que_lo_dan': veces,
        'encabezados_legibles': legibles,
        'nota': 'el resto son cifras mal leídas por el OCR (419, 179, 319…), no otro desfase',
    }
    return res


def escribir(clave: str, valor: dict) -> None:
    import yaml
    with io.open(YAML, encoding='utf-8') as fh:
        texto = fh.read()
    bloque = yaml.safe_dump({clave: valor}, allow_unicode=True,
                            default_flow_style=False, sort_keys=False, width=100)
    bloque = ''.join('  ' + l if l.strip() else l for l in bloque.splitlines(keepends=True))
    patron = r'\n  %s:(?: \{\}|\n(?:    .*\n|  - .*\n)*)' % re.escape(clave)
    nuevo = re.sub(patron, lambda m: '\n' + bloque, texto, count=1)
    if nuevo == texto:
        raise SystemExit('no encontré dónde escribir `%s:` en %s' % (clave, YAML))
    with io.open(YAML, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(nuevo)


def _imprimir(titulo: str, d: dict) -> None:
    print('── %s' % titulo)
    for k, v in d.items():
        print('  %-40s %s' % (k, v))


def main() -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='mide sin escribir')
    ap.add_argument('--sin-pdf', action='store_true', help='no abre los PDF')
    args = ap.parse_args()

    cob = medir_yaml(cargar())
    _imprimir('cobertura del YAML', cob)
    son = None
    if not args.sin_pdf:
        son = medir_pdfs()
        _imprimir('sondas sobre los PDF', son)

    if not args.check:
        escribir('cobertura', cob)
        if son is not None:
            escribir('sondas_medidas', son)
        print('\n→ escrito en meta de %s' % os.path.relpath(YAML, RAIZ))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
