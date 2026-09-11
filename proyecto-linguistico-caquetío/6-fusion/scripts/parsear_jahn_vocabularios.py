# -*- coding: utf-8 -*-
"""Las 19 paginas de ESPANOL | GUAJIRO | PARAUJANO de Jahn, parseadas por
posicion de columna — que es lo unico que aguanta en una tabla a tres bandas."""
import io, os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = os.path.dirname(os.path.abspath(__file__))
T = io.open(os.path.join(S, "jahn_layout.txt"), encoding="utf-8",
            errors="replace").read().split("\f")

filas, paginas = [], []
for n in range(434, 453):                      # pdf 435-453
    pg = T[n]
    m = re.search(r"^(\s*)ESPA[NÑ]OL(\s+)GUAJIRO(\s+)PARAUJANO", pg, re.M)
    if not m:
        m = re.search(r"^(\s*)ESPA[NÑ]OL(\s+)GUAJIRO", pg, re.M)
        if not m: continue
    linea = pg[m.start():pg.index("\n", m.start())]
    c_gua = linea.find("GUAJIRO")
    c_par = linea.find("PARAUJANO")
    # la pagina impresa, de la cabecera
    mp = re.search(r"^\s*(\d{3})\s+LOS ABOR|DEL OCCIDENTE DE VENEZUELA\s+(\d{3})", pg, re.M)
    imp = (mp.group(1) or mp.group(2)) if mp else "?"
    paginas.append((n + 1, imp))
    for ln in pg[pg.index("\n", m.start()) + 1:].split("\n"):
        if not ln.strip() or len(ln) < 6: continue
        if re.match(r"\s*(ESPA|\d{3}\s|DEL OCC|LOS ABOR)", ln): continue
        # la cabecera esta CENTRADA sobre su columna y los datos alineados a
        # la izquierda: cortar por posicion parte las palabras ("teitschir|u").
        # Se corta por hueco de 2+ espacios, que es lo que separa columnas.
        campos = [c for c in re.split(r"\s{2,}", ln.strip()) if c]
        if len(campos) < 2: continue
        esp, gua = campos[0].strip(" ."), campos[1].strip()
        par = campos[2].strip() if len(campos) > 2 else ""
        # una fila util tiene concepto en espanol y al menos una forma
        if not esp or not re.search(r"[a-záéíóúñ]", esp.lower()): continue
        if not (gua or par): continue
        if len(esp) > 34: continue
        filas.append({"esp": esp, "guajiro": gua, "paraujano": par,
                      "pdf": n + 1, "impresa": imp})

print(f"páginas leídas: {len(paginas)}  |  filas: {len(filas)}")
print("rango impreso:", paginas[0][1], "→", paginas[-1][1], "\n")
for f in filas[:18]:
    print(f"  {f['esp']:<24} {f['guajiro']:<22} {f['paraujano']}")
print("  ...")
json.dump(filas, io.open(os.path.join(S, "jahn_guajiro.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito jahn_guajiro.json")
