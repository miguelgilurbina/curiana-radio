# -*- coding: utf-8 -*-
"""Da a cada topónimo del canon que tiene forma viva en el mapa su campo
propio, `forma_viva`, con la coordenada — para que barrer_mapa.py deje de
anunciar como «nuevos» nombres que ya están (dp.2.09 de #222, P4).

La decisión, registrada en 6-fusion/decisiones_222_mundo_2026-09-24.yaml:

    «Ok a todo, que no quede ninguna tarea pendiente» (Miguel, 2026-09-24)

sobre la recomendación del agente del lote de Esteves (M6, #216, pregunta 4):
«que el canon guarde la forma viva con su coordenada en un campo propio y que
barrer_mapa.py lo lea antes del aproximado». Sin él, el informe del mapa
seguía diciendo que Paraguaná tenía ocho nombres «en ninguna fuente» (Azaro,
Bajo Aroa, Cividual, Guaquira Abajo y Arriba, Nueva Jayama, Teteguacure,
Villa Real) que estaban en el canon desde el lote 7 con la forma de Esteves,
y dos aproximados («Cerro Capuana», «Cuabana») caían en `capana` en vez de en
Capuhana y Coabana.

DE DÓNDE SALE CADA COORDENADA: de la prosa de la PROPIA entrada, que la
escribió el lote 7 (2026-09-07) desde el volcado de OpenStreetMap
(`osm-kaketiana`). Este script no mira el mapa: pasa a un campo lo que el
canon ya decía en `observacion`, `mapa_vivo` o el paréntesis de un descarte.
Sólo entran las formas que la entrada da por el mismo lugar; donde la entrada
dice «probablemente» (Chiguaral) va con `nota`. Las cuatro identificaciones
que el lote de Esteves deja «a revisar» (Cumairebo, La Miraba, Tabe, Coduto)
NO se funden aquí: son lecturas `hipotesis` (P3 A) y lo que decida Miguel
sobre el terreno (P3 B).

Dónde escribe (curiana_sim/lexicon_toponimos.py; el canon se regenera con
migrar_toponimos.py):
  - en una entrada de NIVEL_A/B/C: `"forma_viva": [{forma, tipo, lat, lon,
    fuente}]`, que el migrador copia tal cual;
  - en un grupo de DESCARTES: `"formas_vivas": {forma: [...]}`, que el
    migrador reparte por forma (desde el 2026-09-24).

    python 6-fusion/scripts/formas_vivas_al_canon.py [--dry-run]

Idempotente: si una entrada ya tiene su campo, la salta.
"""
import argparse
import io
import json
import os
import re
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODULO = os.path.join(R, "curiana_sim", "lexicon_toponimos.py")


def fv(forma, tipo, lat, lon, nota=None):
    d = {"forma": forma, "tipo": tipo, "lat": lat, "lon": lon, "fuente": "osm-kaketiana"}
    if nota:
        d["nota"] = nota
    return d


# clave del módulo → formas vivas (de la prosa de la propia entrada)
ENTRADAS = {
    "bariquí": [fv("El Variquí", "lugar", 12.013, -70.079)],
    "guadabacoa": [fv("Guaydabacos", "lugar", 12.041, -70.065)],
    "abudure": [fv("Abudare", "lugar", 11.803, -70.015)],
    "jurijurebo": [fv("Jurujurebo", "poblado", 12.049, -69.940)],
    "cumujacoa": [fv("Cumajacoa", "lugar", 11.823, -70.181)],
    "coabana": [fv("Cuabana", "sector", 11.940, -69.928)],
    "guacuira": [fv("Guaquira Abajo", "poblado", 11.932, -69.893),
                 fv("Guaquira Arriba", "poblado", 11.940, -69.887)],
    "caruca": [fv("Curuca", "lugar", 12.096, -69.953)],
    "bibuche": [fv("Chivuche", "lugar", 12.026, -70.033)],
    "bajabaroa": [fv("Bajo Aroa", "lugar", 12.186, -70.033)],
    "pitajaya": [fv("La Pitahaya", "poblado", 11.870, -69.923)],
    "sabarigua": [fv("Sibarigua", "lugar", 11.991, -69.879)],
    "sibidigual": [fv("Cividual", "lugar", 11.753, -69.806)],
    "chiguaral": [fv("El Chiguare", "lugar", 11.979, -70.158,
                     nota="la entrada dice «probablemente el mismo»")],
    "oripopo": [fv("Oropopo", "lugar", 11.884, -70.203)],
    "asaro": [fv("Azaro", "poblado", 11.969, -69.960)],
    "baracara": [fv("Varacara", "poblado", 11.798, -69.974)],
    "capuhana": [fv("Cerro Capuana", "cerro", 11.844, -69.896,
                    nota="la entrada declara la tensión: o son dos Capubana o el nombre bajó del cerro grande al pequeño")],
}

# título del grupo de DESCARTES → {forma: formas vivas}
GRUPOS = {
    "castellano: nombres del mapa vivo en español": {
        "villa real": [fv("Villa Real", "lugar", 12.054, -69.982)],
        "golfete de coro": [fv("Golfete de Coro", "bahía", 11.556, -69.974)],
        "la macolla": [fv("La Macolla", "lugar", 12.090, -70.204),
                       fv("Punta Macolla", "punta", 12.083, -70.217)],
        "buchal": [fv("Buchal", "poblado", 11.960, -69.842)],
    },
    "Esteves 1989: sin glosa en la fuente y ningún morfema conocido alinea": {
        "jayana": [fv("Nueva Jayama", "poblado", 11.794, -70.198)],
        "guacujúa": [fv("Guacujún", "poblado", 11.827, -70.073)],
        "tequeguacare": [fv("Teteguacure", "lugar", 11.811, -70.062)],
        "sisibauco": [fv("Sisibauco", "lugar", 11.875, -69.847)],
    },
    "mapa vivo (OSM 2026): nombre indígena o dudoso sin fuente impresa": {
        "cumairebo": [fv("Cumairebo", "lugar", 12.003, -69.920)],
        "divacoa": [fv("Divacoa", "poblado", 11.783, -69.936)],
        "gusimu": [fv("Gusimu", "lugar", 12.098, -70.178)],
        "tabe": [fv("Tabe", "lugar", 11.917, -70.104)],
        "urumare": [fv("Urumare", "lugar", 11.924, -70.152)],
        "pilancón": [fv("Pilancón", "poblado", 11.833, -69.927)],
        "la miraba": [fv("La Miraba", "poblado", 11.834, -70.054),
                      fv("Cerro La Miraba", "cerro", 11.850, -70.046)],
    },
}


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    raw = io.open(MODULO, encoding="utf-8", newline="").read()
    crlf = "\r\n" in raw
    t = raw.replace("\r\n", "\n")
    hechos = saltados = 0
    for clave, formas in ENTRADAS.items():
        m = re.search(rf'^    {re.escape(json.dumps(clave, ensure_ascii=False))}: \{{\n', t, re.M)
        if not m:
            raise SystemExit(f"no encuentro la entrada «{clave}»")
        fin = t.index("\n    },\n", m.end())
        if '"forma_viva":' in t[m.end():fin]:
            saltados += 1
            print(f"  = {clave}: ya tenía forma_viva")
            continue
        linea = f'        "forma_viva": {json.dumps(formas, ensure_ascii=False)},\n'
        t = t[:m.end()] + linea + t[m.end():]
        hechos += 1
        print(f"  + {clave}: {', '.join(f['forma'] for f in formas)}")
    for titulo, por_forma in GRUPOS.items():
        m = re.search(rf'^    {re.escape(json.dumps(titulo, ensure_ascii=False))}: \{{\n', t, re.M)
        if not m:
            raise SystemExit(f"no encuentro el grupo «{titulo}»")
        fin = t.index("\n    },\n", m.end())
        if '"formas_vivas":' in t[m.end():fin]:
            saltados += 1
            print(f"  = [{titulo[:40]}…]: ya tenía formas_vivas")
            continue
        linea = f'        "formas_vivas": {json.dumps(por_forma, ensure_ascii=False)},\n'
        t = t[:m.end()] + linea + t[m.end():]
        hechos += 1
        print(f"  + [{titulo[:40]}…]: {', '.join(por_forma)}")
    ns = {}
    exec(compile(t, MODULO, "exec"), ns)
    print(f"{hechos} escritos, {saltados} ya estaban")
    if a.dry_run:
        print("--dry-run: no se escribe nada")
        return 0
    io.open(MODULO, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
