#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — la arqueología de las islas y de Falcón (M8), medida
===============================================================

Tercera campaña de minería, parcela M8 (2026-09-22). Emite las cifras del
lado del REPO que cita `6-fusion/arqueologia_insular_falcon_2026-09-22.yaml`
y su issue (regla 1). Sólo lee; no escribe nada.

1. **Sondas** sobre el `pdftotext` de las cinco obras de la parcela: cultura
   material antillana (la lista de T8), región (Venezuela y las ABC),
   creencia (para el cero de la pregunta 4) y mar/fauna (el control de que
   el barrido funciona). Raíz corta, sin acentos (skill minar-fuente §2).
   Los aciertos de creencia se imprimen con su contexto: un acierto en la
   bibliografía no es un dato.
2. **La Tabla 4 de Casale 2024**, transcrita en el YAML: recuento por grupo
   petrográfico, decorados por grupo y sitio de las no agrupadas, contra lo
   que el texto del artículo declara.
3. **La Tabla 7 de Urbina 2007**: que la suma dé el total declarado.
4. **Tamaño y sha256** de los PDF bajados hoy.

Uso:
    python 6-fusion/scripts/medir_arqueologia_insular_falcon.py
"""

import collections
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

import yaml

_AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(_AQUI))
PROPUESTA = os.path.join(REPO, "6-fusion", "arqueologia_insular_falcon_2026-09-22.yaml")

OBRAS = [
    ("urbina-2007", "fuentes_caquetios/Urbina_2007_El_Carrizal_UCV.pdf"),
    ("urbina-2011", "fuentes_caquetios/Urbina_2011_Archaeological_Survey_Coastal_Falcon_UCL.pdf"),
    ("casale-2024", "fuentes_caquetios/Casale_et_al_2024_Geoarchaeology_Petrografia_Aruba_CCBY.pdf"),
    ("knaf-2021", "fuentes_caquetios/Knaf_et_al_2021_JAS_Jade_Circum_Caribbean_CCBY.pdf"),
    ("moreno-mayar-2018", "fuentes_caquetios/MorenoMayar_et_al_2018_Science_Early_Human_Dispersals.pdf"),
]
DESCARGADOS = [OBRAS[2][1], OBRAS[3][1]]

# Regex sobre el texto en minúsculas y sin diacríticos.
SONDAS = {
    "antillana": [r"ostionoid", r"chicoid", r"meillacoid", r"elenoid", r"palmetto",
                  r"guanin", r"tumbaga", r"jadeit", r"\bcemi", r"\bzemi", r"guaiza",
                  r"\bduho", r"trigonolit", r"antillas mayores", r"greater antilles",
                  r"hispaniol", r"\btaino", r"lucay", r"antill"],
    "region": [r"venezuel", r"\baruba", r"curacao|curazao", r"bonaire", r"paragua",
               r"falcon", r"guajira", r"\bcoro\b", r"caquet", r"dabajur"],
    "creencia": [r"cosmo", r"\bbelie", r"creenc", r"ritual", r"sacred", r"sagrad",
                 r"ceremon", r"religi", r"\bmyth", r"\bmito", r"ofrend", r"offering",
                 r"\bdeit", r"deidad", r"\bidol", r"shaman", r"chaman", r"piache",
                 r"ajuar funerario", r"grave goods"],
    "mar_y_fauna": [r"\bmar\b", r"\bsea\b", r"marin", r"coast|costa", r"shell|concha|conch",
                    r"strombus|lobatus|botuto", r"\bfish(?!er)|pesca|\bpez\b|peces", r"tortug|turtle",
                    r"coral", r"hueso|\bbone", r"\botolit", r"mangrov|manglar"],
}


def _forzar_utf8():
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def plano(texto):
    desc = unicodedata.normalize("NFD", texto.lower().replace("‐", "-"))
    return re.sub(r"\s+", " ", "".join(c for c in desc if unicodedata.category(c) != "Mn"))


def texto_de(pdf, cache):
    ruta = os.path.join(REPO, pdf)
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        return None
    destino = os.path.join(cache, os.path.basename(pdf) + ".txt")
    subprocess.run(["pdftotext", "-enc", "UTF-8", ruta, destino], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(destino, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def sondas(textos):
    print("=" * 72)
    print("1. SONDAS POR OBRA (regex sobre el pdftotext, sin acentos)")
    print("=" * 72)
    for clave, bruto in textos.items():
        if bruto is None:
            print(f"\n🔴 {clave}: SIN TEXTO")
            continue
        s = plano(bruto)
        print(f"\n▸ {clave} — {len(bruto):,} caracteres")
        for familia, lista in SONDAS.items():
            cuenta = {p: len(re.findall(p, s)) for p in lista}
            aciertos = {p: n for p, n in cuenta.items() if n}
            total = sum(cuenta.values())
            detalle = ", ".join(f"{p}={n}" for p, n in aciertos.items()) or "CERO"
            print(f"  {familia:12} total={total:<5} {detalle}")
            if familia == "creencia" and aciertos:
                for p in aciertos:
                    for m in re.finditer(p, s):
                        a, b = max(0, m.start() - 70), m.end() + 70
                        print(f"      · [{p}] …{s[a:b]}…")


def tabla4_casale(d):
    print("\n" + "=" * 72)
    print("2. CASALE 2024, TABLA 4 (transcrita y verificada en imagen) contra el texto")
    print("=" * 72)
    t4 = d["casale_tabla4"]
    filas = t4["filas"]
    decl = t4["declarado_en_el_texto"]

    def familia(g):
        g = str(g)
        return "no_agrupadas" if g == "Ungrouped" else f"grupo_{g[0]}"

    por_familia = collections.Counter(familia(f[5]) for f in filas)
    sub3a = sum(1 for f in filas if str(f[5]) == "3a")
    print(f"  muestras en la tabla: {len(filas)}  (el texto declara {decl['total_muestras']})")
    for k in ("grupo_1", "grupo_2", "grupo_3", "no_agrupadas"):
        marca = "✓" if por_familia[k] == decl[k] else "✗ NO CUADRA"
        print(f"  {k:13} tabla={por_familia[k]:<3} texto={decl[k]:<3} {marca}")
    marca = "✓" if sub3a == decl["grupo_3a"] else "✗ NO CUADRA"
    print(f"  {'grupo_3a':13} tabla={sub3a:<3} texto={decl['grupo_3a']:<3} {marca}")
    print(f"  suma según el texto: "
          f"{decl['grupo_1'] + decl['grupo_2'] + decl['grupo_3'] + decl['no_agrupadas']}")

    for k in ("grupo_1", "grupo_2", "grupo_3"):
        fs = [f for f in filas if familia(f[5]) == k]
        dec = sum(1 for f in fs if str(f[3]).startswith("Decorated"))
        print(f"  decorados en {k}: {dec} de {len(fs)}")
    dec_fuera = [f[1] for f in filas if str(f[3]).startswith("Decorated")
                 and familia(f[5]) != "grupo_3"]
    print(f"  decorados FUERA del grupo 3: {len(dec_fuera)} ({', '.join(dec_fuera)})")

    na = [f for f in filas if familia(f[5]) == "no_agrupadas"]
    print("  no agrupadas por sitio: " +
          ", ".join(f"{f[1]} ({f[0]})" for f in na))
    fuera = [f[1] for f in na if f[0] not in decl["no_agrupadas_solo_de"]]
    print(f"  no agrupadas FUERA de {decl['no_agrupadas_solo_de']}: "
          f"{len(fuera)} {fuera if fuera else ''}")


def cuerpo_sin_bibliografia(bruto, marca):
    s = plano(bruto)
    i = s.rfind(plano(marca))
    return s[:i] if i > 0 else s


def tabla7_urbina(d):
    print("\n" + "=" * 72)
    print("3. URBINA 2007, TABLA 7 (p. 123)")
    print("=" * 72)
    t7 = d["urbina_2007_tabla7"]
    suma = sum(f[1] for f in t7["filas"])
    print(f"  suma de fragmentos: {suma}  total declarado: {t7['total_declarado']}  "
          f"{'✓' if suma == t7['total_declarado'] else '✗'}")
    malos = [f[0] for f in t7["filas"]
             if abs(100 * f[1] / t7["total_declarado"] - f[2]) > 0.01]
    print(f"  porcentajes que no cuadran al 0,01: {malos if malos else 'ninguno'}")


def descargados():
    print("\n" + "=" * 72)
    print("4. PDF BAJADOS HOY")
    print("=" * 72)
    for pdf in DESCARGADOS:
        ruta = os.path.join(REPO, pdf)
        with open(ruta, "rb") as fh:
            datos = fh.read()
        print(f"  {os.path.basename(pdf)}\n    {len(datos):,} bytes · "
              f"sha256 {hashlib.sha256(datos).hexdigest()} · md5 {hashlib.md5(datos).hexdigest()}")


def main():
    _forzar_utf8()
    if not shutil.which("pdftotext"):
        print("🔴 pdftotext no está en el PATH: no se mide nada (regla 6).")
        return 1
    with open(PROPUESTA, encoding="utf-8") as fh:
        d = yaml.safe_load(fh)
    cache = tempfile.mkdtemp(prefix="curiana_m8_")
    try:
        textos = {clave: texto_de(pdf, cache) for clave, pdf in OBRAS}
    finally:
        shutil.rmtree(cache, ignore_errors=True)
    sondas(textos)
    # Casale: ¿alguna «Antill-» FUERA de la bibliografía?
    cuerpo = cuerpo_sin_bibliografia(textos["casale-2024"], "REFERENCES")
    en_cuerpo = {p: len(re.findall(p, cuerpo)) for p in SONDAS["antillana"]}
    print(f"\n  Casale SIN la bibliografía: sondas antillanas = {sum(en_cuerpo.values())} "
          f"{ {p: n for p, n in en_cuerpo.items() if n} or ''}")
    tabla4_casale(d)
    tabla7_urbina(d)
    descargados()
    return 0


if __name__ == "__main__":
    sys.exit(main())
