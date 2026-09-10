# -*- coding: utf-8 -*-
"""Decision de Miguel 2026-09-10: RE-ETIQUETAR las 23 entradas reconstruidas
desde el wayuu, sin tocar las formas.

NO cambia forma, sig, cat ni fuente. Solo `notas`. Los runs siguen
comparables y score_linguistico() no se mueve.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
p = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
t = io.open(p, encoding="utf-8").read()

# lo que da el lokono para cada una, medido con medir_deuda_d11.py
LOKONO = {
 "anüiki":  "lokono `adija` 'hablar, decir; palabra' — otra raíz",
 "apünüin": "lokono `kabyn` 'tres' — otro sistema",
 "bana":    "el lokono del lexicón no cubre 'hígado'",
 "jarai":   "el lokono del lexicón no cubre 'cinco'",
 "kapua":   "el lokono del lexicón no cubre 'amanecer'",
 "kasha":   "lokono `kathi` 'luna' — PARECIDA; esta entrada ya declaraba apoyo lokono además del wayuu",
 "kashi":   "el lokono del lexicón no cubre 'ahora'",
 "kira":    "el lokono del lexicón no cubre 'escuchar'",
 "naba":    "el lokono del lexicón no cubre 'pensar'",
 "naya":    "lokono `na-` 3pl",
 "nüma":    "lokono `li`/`tho` 3sg",
 "pia":     "lokono `bi`/`bui` 2sg — en el lexicón y en Perea 1942",
 "piama":   "lokono `bian` 'dos' — PARECIDA (p~b)",
 "pienchi": "lokono `bithi` 'cuatro' — otra raíz",
 "pütchi":  "el lokono del lexicón no cubre 'mensaje'",
 "sulu":    "el lokono del lexicón no cubre 'adentro'",
 "taya":    "lokono `de`/`dai` 1sg — en el lexicón y en Perea 1942",
 "tüshi":   "el lokono del lexicón no cubre 'frío'",
 "wana":    "el lokono del lexicón no cubre 'ver'",
 "wanee":   "lokono `aba` 'uno' — otra raíz",
 "wanü":    "el lokono del lexicón no cubre 'anciano'",
 "waya":    "lokono `we`/`wai` 1pl — PARECIDA; `wai` sale 231 veces en Perea",
 "yama":    "el lokono del lexicón no cubre 'aquí'",
}

SELLO = ("⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): "
         "forma reconstruida desde el WAYUU **antes** de D11, que retiró al "
         "wayuunaiki como hermana por defecto. %s. SE CONSERVA LA FORMA por "
         "continuidad experimental —cambiarla partiría en dos la "
         "comparabilidad de todos los runs de la base y movería "
         "score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier "
         "coincidencia de esta entrada con el wayuu es circular. Ver "
         "6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md")

hechas, saltadas = [], []
for clave, lok in LOKONO.items():
    # localizar la entrada y su campo notas
    m = re.search(r'("%s":\s*\{)' % re.escape(clave), t)
    if not m:
        saltadas.append(clave); continue
    ini = m.end()
    # el cierre de la entrada: la llave que casa
    prof, i = 1, ini
    while prof and i < len(t):
        if t[i] == "{": prof += 1
        elif t[i] == "}": prof -= 1
        i += 1
    cuerpo = t[ini:i - 1]
    if "DEUDA D11" in cuerpo:
        saltadas.append(clave); continue
    sello = SELLO % lok
    mn = re.search(r'"notas":\s*(".*?[^\\]")(?=\s*[,}])', cuerpo, re.S)
    if mn:
        viejo = mn.group(1)
        nuevo = viejo[:-1] + ' — ' + sello.replace('"', "'") + '"'
        cuerpo2 = cuerpo[:mn.start(1)] + nuevo + cuerpo[mn.end(1):]
    else:
        cuerpo2 = cuerpo.rstrip().rstrip(",") + ', "notas": "%s"' % sello.replace('"', "'")
    t = t[:ini] + cuerpo2 + t[i - 1:]
    hechas.append(clave)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print(f"re-etiquetadas {len(hechas)}: {', '.join(sorted(hechas))}")
if saltadas: print(f"saltadas {len(saltadas)}: {', '.join(saltadas)}")
