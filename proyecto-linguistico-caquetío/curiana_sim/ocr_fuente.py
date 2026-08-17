"""OCR de una fuente escaneada, con la página impresa como ancla.

Las fuentes sin capa de texto (Gilij #60, Los Ídolos) no se pueden minar con
`pdftotext`: no tienen letras, tienen píxeles. Este script las convierte.

Rinde texto **por página**, con marcador explícito, porque el protocolo de
minería cita por página impresa y no por página del PDF. El desfase entre una y
otra se calcula una vez y se pasa con `--offset`.

    python ocr_fuente.py ../fuentes_caquetios/OBRA.pdf --lang spa
    python ocr_fuente.py ../fuentes_caquetios/Gilij_1780_vol1.pdf --lang ita \
        --paginas 40-60 --offset -8

⚠️ El texto que sale de aquí es **OCR, no transcripción**. Una glosa leída de
este texto sin mirar la imagen de la página no vale: los errores de OCR caen
justo en lo que más importa (nombres propios, topónimos, diacríticos). Trátalo
como pista para llegar a la página, nunca como cita.
"""

import argparse
import io
import os
import re
import sys
from pathlib import Path

# Dónde suele quedar el binario en Windows; pytesseract no lo encuentra solo
# porque el instalador no lo mete en PATH.
_CANDIDATOS_TESSERACT = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
]


def _forzar_utf8():
    """La consola de Windows es cp1252 y revienta con « o ü."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


def localizar_tesseract():
    """Devuelve la ruta al binario, o None con el motivo escrito."""
    import shutil
    en_path = shutil.which("tesseract")
    if en_path:
        return en_path
    for ruta in _CANDIDATOS_TESSERACT:
        if Path(ruta).is_file():
            return ruta
    return None


def idiomas_disponibles(binario):
    import subprocess
    try:
        salida = subprocess.run([binario, "--list-langs"], capture_output=True,
                                text=True, timeout=30)
        return [l.strip() for l in salida.stdout.splitlines()[1:] if l.strip()]
    except Exception:
        return []


def orientar(imagen, modo, pytesseract):
    """Grados que hay que girar la página para enderezarla (0 si nada).

    Un escaneo con páginas invertidas no falla ruidosamente: devuelve texto
    con la forma correcta y el contenido destruido. Pasó con el Apéndice E de
    Oliver — las páginas de Paraguaná dieron 2.850 caracteres y CERO códigos
    de sitio, y la pista fue leer `YNYNOVUVd` como `PARAGUANA` del revés.
    """
    if modo in ("0", "no", "none"):
        return 0
    if modo != "auto":
        try:
            return int(modo) % 360
        except ValueError:
            return 0
    try:
        osd = pytesseract.image_to_osd(imagen)
        m = re.search(r"Rotate:\s*(\d+)", osd)
        return int(m.group(1)) % 360 if m else 0
    except Exception:
        # OSD falla en páginas con poco texto; no es motivo para abortar
        return 0


def rango(spec, total):
    """'40-60' o '12' → lista de índices 0-based del PDF."""
    if not spec:
        return list(range(total))
    if "-" in spec:
        ini, fin = spec.split("-", 1)
        return list(range(int(ini) - 1, min(int(fin), total)))
    return [int(spec) - 1]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", help="ruta al PDF escaneado")
    ap.add_argument("--lang", default="spa",
                    help="idioma tesseract: spa, ita, eng, lat (por defecto spa)")
    ap.add_argument("--paginas", default=None,
                    help="rango de páginas del PDF, p.ej. 40-60")
    ap.add_argument("--offset", type=int, default=0,
                    help="página impresa = página del PDF + offset")
    ap.add_argument("--dpi", type=int, default=300,
                    help="resolución de render (300 va bien; 400 para letra chica)")
    ap.add_argument("--salida", default=None, help="archivo .txt de salida")
    ap.add_argument("--psm", type=int, default=None,
                    help="modo de segmentación de tesseract. 3=auto (por defecto), "
                         "4=columna única de tamaños variables, 6=bloque uniforme. "
                         "Las listas a dos columnas suelen necesitar 4 o 6")
    ap.add_argument("--rotar", default="auto",
                    help="'auto' detecta la orientación con OSD y endereza (por "
                         "defecto) · '0' la desactiva · 90/180/270 fuerza el giro. "
                         "Los escaneos antiguos traen páginas invertidas: sin esto "
                         "salen 2.000 caracteres de basura y CERO datos, que es "
                         "peor que una página vacía porque no se nota")
    args = ap.parse_args()

    binario = localizar_tesseract()
    if not binario:
        print("✗ No encuentro tesseract.exe.")
        print("  Instálalo con (requiere permisos de administrador):")
        print("      winget install --id UB-Mannheim.TesseractOCR")
        print("  y marca los paquetes de idioma Spanish e Italian.")
        sys.exit(1)

    import pypdfium2 as pdfium
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = binario

    # tesseract acepta varios idiomas a la vez con '+' (p.ej. spa+eng), útil en
    # los formularios bilingües. Hay que validar pieza por pieza.
    disponibles = idiomas_disponibles(binario)
    faltan = [l for l in args.lang.split("+") if disponibles and l not in disponibles]
    if faltan:
        print(f"✗ Idioma(s) no instalado(s): {', '.join(faltan)}")
        print(f"  Hay: {', '.join(disponibles)}")
        print("  Reejecuta el instalador de Tesseract y añade el paquete.")
        sys.exit(1)

    ruta = Path(args.pdf)
    if not ruta.is_file():
        print(f"✗ No existe: {ruta}")
        sys.exit(1)

    salida = Path(args.salida) if args.salida else ruta.with_suffix(".ocr.txt")
    doc = pdfium.PdfDocument(str(ruta))
    indices = rango(args.paginas, len(doc))
    escala = args.dpi / 72

    print(f"  fuente   {ruta.name}")
    print(f"  motor    {binario}  ·  idioma {args.lang}  ·  {args.dpi} dpi")
    print(f"  páginas  {len(indices)} de {len(doc)}")

    vacias, girada = [], []
    with open(salida, "w", encoding="utf-8") as f:
        for n, i in enumerate(indices, 1):
            imagen = doc[i].render(scale=escala).to_pil()
            giro = orientar(imagen, args.rotar, pytesseract)
            if giro:
                imagen = imagen.rotate(-giro, expand=True)
                girada.append((i + 1, giro))
            cfg = f"--psm {args.psm}" if args.psm else ""
            texto = pytesseract.image_to_string(imagen, lang=args.lang, config=cfg)
            impresa = i + 1 + args.offset
            f.write(f"\n=== pdf {i + 1} · impresa {impresa} ===\n")
            f.write(texto)
            if len(texto.strip()) < 20:
                vacias.append(i + 1)
            if n % 10 == 0 or n == len(indices):
                print(f"    {n}/{len(indices)}")

    chars = salida.stat().st_size
    print(f"  → {salida.name}: {chars:,} bytes")

    if girada:
        detalle = ", ".join(f"{p}({g}°)" for p, g in girada[:10])
        print(f"  ↻ {len(girada)} página(s) enderezada(s): {detalle}"
              f"{' …' if len(girada) > 10 else ''}")

    # Una página en blanco puede ser real (portadilla) o un fallo de render.
    # Decirlo evita el error de la regla 6: un cero hay que verificarlo.
    if vacias:
        print(f"  ⚠ {len(vacias)} página(s) casi sin texto: "
              f"{', '.join(map(str, vacias[:12]))}"
              f"{' …' if len(vacias) > 12 else ''}")
        print("    Míralas antes de concluir que la fuente no dice nada.")


if __name__ == "__main__":
    _forzar_utf8()
    main()
