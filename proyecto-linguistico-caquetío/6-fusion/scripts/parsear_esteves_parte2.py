# -*- coding: utf-8 -*-
"""Vacía la PARTE II de Esteves 1989: «Otros topónimos indígenas del estado
Falcón» (pp. impresas 81-144, tomos 4-6).

Formato de entrada, constante:
    NOMBRE   Aldea del municipio X, Distrito Y. Glosa/etimología.
Con variantes: I - ... II - ... para varios referentes del mismo nombre.
"""
import io, os, re, sys, glob, json, unicodedata, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"

# La Parte II arranca en el tomo 4, pdf 9. Antes va el Apéndice (pp. 73-80).
INICIO = ("4", 9)

paginas = []
for f in sorted(glob.glob(os.path.join(R, "fuentes_caquetios", "Esteves_1989_*_[456].ocr.txt"))):
    tomo = f.split("_")[-1][0]
    t = io.open(f, encoding="utf-8").read()
    trozos = re.split(r"=== pdf (\d+) · impresa \d+ ===", t)
    for i in range(1, len(trozos), 2):
        paginas.append((tomo, int(trozos[i]), trozos[i + 1]))

# quedarse desde el arranque de la Parte II
arranque = [k for k, (tm, pd, _) in enumerate(paginas) if (tm, pd) == INICIO]
paginas = paginas[arranque[0]:] if arranque else paginas
print(f"páginas de la Parte II: {len(paginas)}")

texto = "\n".join(c for _, _, c in paginas)
texto = texto.replace("CamScanner", " ")

# el nombre de entrada: MAYÚSCULAS al principio de línea, 3+ letras
ENTRADA = re.compile(
    r"^[ \t]*([A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ' \-]{2,30})[ \t]*(?=\n|\s)", re.MULTILINE)

MUNI = re.compile(r"municipio\s+([A-ZÁÉÍÓÚÑ][\wáéíóúñ]+)", re.I)
DIST = re.compile(r"Distrito\s+([A-ZÁÉÍÓÚÑ][\wáéíóúñ]+)", re.I)
TIPO = re.compile(r"\b(Aldea|Caser[ií]o|Pueblo|R[ií]o|Quebrada|Cerro|Sitio|Punta|"
                  r"Ensenada|Laguna|Sabana|Fila|Serran[ií]a|Valle|Playa|Bah[ií]a|"
                  r"Poblado|Casa|Hacienda|Fundo|Sector|Isla)\b", re.I)

ms = list(ENTRADA.finditer(texto))
print(f"marcadores de entrada en bruto: {len(ms)}")

entradas = {}
for k, m in enumerate(ms):
    nombre = " ".join(m.group(1).split())
    if len(nombre) < 3 or nombre in ("CAPITULO", "INDICE", "PARTE", "OTROS",
                                     "APENDICE", "II", "III"):
        continue
    fin = ms[k + 1].start() if k + 1 < len(ms) else len(texto)
    cuerpo = " ".join(texto[m.end():fin].split())
    if len(cuerpo) < 12:            # cabeceras sueltas
        continue
    if nombre in entradas and len(entradas[nombre]["cuerpo"]) >= len(cuerpo):
        continue
    mu, di, ti = MUNI.search(cuerpo), DIST.search(cuerpo), TIPO.search(cuerpo)
    entradas[nombre] = {
        "cuerpo": cuerpo[:600],
        "municipio": mu.group(1) if mu else None,
        "distrito": di.group(1) if di else None,
        "tipo": ti.group(1).lower() if ti else None,
    }

print(f"entradas parseadas: {len(entradas)}")
con_muni = sum(1 for e in entradas.values() if e["municipio"])
print(f"  con municipio identificado: {con_muni}")
print(f"  con distrito: {sum(1 for e in entradas.values() if e['distrito'])}")

dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parte2.json")
json.dump(entradas, io.open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrito:", dest)
print()
for n in list(entradas)[:12]:
    e = entradas[n]
    print(f"  {n:<16} [{e['tipo']}/{e['municipio']}/{e['distrito']}] {e['cuerpo'][:90]}")
