#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mide la cobertura de `6-fusion/taino_oviedo_valdes_1851.yaml` y la escribe
en `meta.cobertura`.

Ninguna cifra de esa propuesta se escribe a mano (regla 1): se emiten aquí.

    python 6-fusion/scripts/medir_taino_oviedo.py            # mide y escribe
    python 6-fusion/scripts/medir_taino_oviedo.py --check    # mide y no escribe

Además cruza las formas contra las 52 entradas taínas de `curiana_lexicon.py`
(solo lectura) para responder la pregunta del encargo: cuántas de esas 52
quedan con cita gracias a Oviedo.
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YAML = os.path.join(RAIZ, '6-fusion', 'taino_oviedo_valdes_1851.yaml')
LEXICON = os.path.join(RAIZ, 'curiana_sim', 'curiana_lexicon.py')

SECCIONES = ('costa_de_venezuela', 'la_espanola', 'otras_islas', 'no_taino')


def _forzar_utf8() -> None:
    """La consola de Windows es cp1252 (trampa de CLAUDE.md)."""
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass


def cargar():
    import yaml
    with io.open(YAML, encoding='utf-8') as fh:
        return yaml.safe_load(fh)


# ── el lexicón, solo lectura ─────────────────────────────────────────
RX_CLAVE = re.compile(r'"([^"\n]{1,48})"\s*:\s*\{')


def _bloque(texto: str, i: int) -> str:
    prof, j = 0, i
    while j < len(texto):
        ch = texto[j]
        if ch == '"':
            j += 1
            while j < len(texto) and texto[j] != '"':
                j += 2 if texto[j] == '\\' else 1
        elif ch == '{':
            prof += 1
        elif ch == '}':
            prof -= 1
            if prof == 0:
                return texto[i:j + 1]
        j += 1
    return texto[i:]


def claves_tainas() -> set:
    with io.open(LEXICON, encoding='utf-8') as fh:
        texto = fh.read()
    fuera = set()
    for m in RX_CLAVE.finditer(texto):
        cuerpo = _bloque(texto, m.end() - 1)
        if re.search(r'"fuente"\s*:\s*"ta[ií]no[^"]*"', cuerpo):
            fuera.add(m.group(1))
    return fuera


# ── medir ────────────────────────────────────────────────────────────
def formas_de(entrada) -> list:
    f = entrada.get('forma_fuente')
    if f is None:
        return []
    return [str(x) for x in f] if isinstance(f, list) else [str(f)]


def esta_en_el_lexicon(entrada) -> bool:
    """⚠️ `en_el_lexicon: no` lo lee YAML como el booleano False, no como
    la cadena 'no'. Sin esto el recuento de voces nuevas salía 1."""
    v = entrada.get('en_el_lexicon')
    if v is None or v is False:
        return False
    return str(v).strip().lower().startswith(('sí', 'si'))


def paginas_de(entrada) -> list:
    p = entrada.get('pagina_impresa')
    if p is None:
        return []
    return [int(x) for x in p] if isinstance(p, list) else [int(p)]


def medir(datos: dict) -> dict:
    formas, paginas = [], set()
    por_seccion, por_verificacion, por_campo = {}, {}, {}
    citadas_del_lexicon = set()
    lexicon = claves_tainas()

    for sec in SECCIONES:
        entradas = [e for e in (datos.get(sec) or []) if isinstance(e, dict)]
        n = 0
        for e in entradas:
            fs = formas_de(e)
            if not fs:
                continue          # las entradas de método no son voces
            n += len(fs)
            formas += fs
            paginas.update(paginas_de(e))
            v = e.get('verificacion', 'sin-declarar')
            por_verificacion[v] = por_verificacion.get(v, 0) + len(fs)
            campos = e.get('campo', [])
            campos = campos if isinstance(campos, list) else [campos]
            for c in campos:
                por_campo[str(c)] = por_campo.get(str(c), 0) + 1
            if esta_en_el_lexicon(e):
                for clave in re.findall(r'`([^`]+)`', str(e.get('en_el_lexicon'))):
                    if clave in lexicon:
                        citadas_del_lexicon.add(clave)
        por_seccion[sec] = n

    cuerpo = sorted(p for p in paginas if 1 <= p <= 618)
    con_imagen = [p for p in cuerpo if p <= 154]

    return {
        'formas_transcritas': len(formas),
        'formas_distintas': len(set(f.lower() for f in formas)),
        'por_seccion': por_seccion,
        'por_verificacion': por_verificacion,
        'campos_tocados': len(por_campo),
        'paginas_impresas_citadas': len(cuerpo),
        'paginas_citadas_con_imagen': len(con_imagen),
        'paginas_citadas_solo_ocr': len(cuerpo) - len(con_imagen),
        'rango_de_paginas': ('%d-%d' % (cuerpo[0], cuerpo[-1])) if cuerpo else '—',
        'entradas_taínas_del_lexicon': len(lexicon),
        'de_esas_con_cita_de_oviedo': len(citadas_del_lexicon),
        'cuales': sorted(citadas_del_lexicon),
        'de_esas_sin_cita_todavía': sorted(lexicon - citadas_del_lexicon),
        'voces_nuevas_no_en_el_lexicon':
            sum(len(formas_de(e)) for sec in SECCIONES
                for e in (datos.get(sec) or [])
                if isinstance(e, dict) and formas_de(e) and not esta_en_el_lexicon(e)),
    }


def escribir(cob: dict) -> None:
    """Reemplaza la línea `cobertura: {}` (o el bloque ya escrito) por el medido."""
    import yaml
    with io.open(YAML, encoding='utf-8') as fh:
        texto = fh.read()
    bloque = yaml.safe_dump({'cobertura': cob}, allow_unicode=True,
                            default_flow_style=False, sort_keys=False, width=100)
    bloque = ''.join('  ' + l if l.strip() else l
                     for l in bloque.splitlines(keepends=True))
    nuevo = re.sub(r'\n  cobertura:(?: \{\}|\n(?:    .*\n|  - .*\n)*)',
                   '\n' + bloque, texto, count=1)
    if nuevo == texto:
        raise SystemExit('no encontré dónde escribir `cobertura:` en %s' % YAML)
    with io.open(YAML, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(nuevo)


def main() -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='mide sin escribir')
    args = ap.parse_args()

    cob = medir(cargar())
    ancho = max(len(k) for k in cob)
    for k, v in cob.items():
        if isinstance(v, list):
            print('%-*s : %d  (%s)' % (ancho, k, len(v), ', '.join(v[:12]) +
                                       ('…' if len(v) > 12 else '')))
        elif isinstance(v, dict):
            print('%-*s : %s' % (ancho, k, ', '.join('%s=%s' % kv for kv in v.items())))
        else:
            print('%-*s : %s' % (ancho, k, v))

    if not args.check:
        escribir(cob)
        print('\n→ escrito en meta.cobertura de %s' % os.path.relpath(YAML, RAIZ))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
