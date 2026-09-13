# -*- coding: utf-8 -*-
"""Fabo 1911, lo achagua: las dos tablas, el pasaje de -are, el texto achagua,
y el cotejo Neira 1762 → Fabo 1911 → Jahn 1927 sobre las 34 voces.

Genera 6-fusion/achagua_fabo_1911.yaml. Regla 5: propone, no fusiona.

Las tablas se transcribieron a mano de la IMAGEN (pdf 110-114 = impresas
108-112, renderizadas con pymupdf): el OCR de archive.org desplaza las
columnas. Las formas del manuscrito salen de la calibración que dejó el
escriba en 6-fusion/achagua_neira_ribero_1762.yaml (transcripción por
visión, verificar antes de citar como exacta).
"""
import io, os, re, sys, yaml
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# p. impresa 108 (pdf 110): CASTELLANO / ACHAGUA / GUARANÍ — «He aquí algunas comparaciones»
TABLA_108 = [
 ("Agua","Chitey","Chity"),("Canoa","Ida","Iga"),("Cabeza","Nurita","Acaujita"),("Colorado","Quirage","Pira"),
 ("Negro","Cachajura","Ju"),("Comer","Gigato","Guicaruabo"),("Cantar","Norracapa","Guiracapacai"),
 ("Duende","Guabaimi","Meboguabi"),("Estrella","Ivisai","Yasi tatá"),("Él","Rae","Hae"),("Flor","Ibinachi","Iboti"),
 ("Fruta","Itasi","Ibá"),("Leña","Ichaba","Ipea ipirú"),("Morir","Mánare","Amano"),("Nosotros","Guaya, guaruyá","Oropetei guazú"),
 ("Plátano","Parata","Pacoba"),("Pescar","Poracá","Poracá"),("Paja","Misi","Capiji"),("Palmera","Cusi","yuyi Cirí"),
 ("Piedra","Iba","Itá"),("Salina","Iquití","Yuquití"),("Sepultura","Nirri","Tibi"),("Sarta","Quiripa","Rizi"),
]
# pp. impresas 111-112 (pdf 113-114): CASTELLANO / ACHAGUA / GUAHIVO
TABLA_111 = [
 ("Agua","Menoa-mena","Merra"),("Allí","Sare","Arremeliego"),("Blanco","Paray","Niojay"),("Casa","Bonisi","Bo"),
 ("Cafuche","Aguicha","Jabuitcha"),("Candela","Isay","Isoto"),("Cazabe","Berri","Perri"),("Dulce","Maná","Baná"),
 ("Dios","Guayguerri","Guey"),("Duende","Guabaimi","Duguatini"),("Estómago","Navarrick","Matabicopene"),("Él","Rae","Arra poni"),
 ("Hombre","Guanacataperri","Pebi"),("Lanza","Chavina","Yavinato"),("Nariz","Mutaco","Pemutaito"),("Nosotros","Guaya","Guajaichi"),
 ("Ojo","Nutoy","Peitajuto"),("Perro","Iduri","Abirri"),("Plátano","Parata","Baratun"),("Pez","Dupay","Dugüey"),
 ("Piedra","Iba","Iboto"),("Tabaco","Sema","Chema"),("Vosotros","Ja","Pajanui"),("Yo","Nuja","Jani"),
]
PASAJE_ARE = (
 "«Una de las terminaciones más empleadas en el achagua es are, como propia y exclusiva, por cuanto ni en el "
 "sáliva ni en el guahivo se ha descubierto; el guahivo termina muchas en arre y en ane, pero una ó dos únicamente "
 "en are; por lo cual creemos que los vocablos, ya sean de significación geográfica ya de usos domésticos, que "
 "subsisten en nuestros días, son reminiscencias de aquella habla. Con muchos de ellos se designan hoy ríos, lo cual "
 "hace sospechar que tal desinencia dice relación á río, agua ó cosas análogas, aunque bien puede sugerir nombres de "
 "tribus que habitaron las comarcas por donde cruzan esos ríos [...]. Dícese que are es raíz caribe y que significa "
 "«la gran sombra de invasión que venía subiendo las aguas del Magdalena... El creador Are vino del otro lado del río "
 "de muy lejanas tierras...» Restrepo Tirado, Invasiones caribes. [...] Casanare, Casiquiare, Guaviare, Tebiare, "
 "Sarrare, Manare, Guanare, Maremare, Atanare, Onocutare, Carare, Purare y otros muchos son nombres de ríos [...]; "
 "otros nombres nos quedan incorporados al castellano, como regionalismos, y son Budare, plancha de hierro para tostar "
 "masas, especialmente cazabe, arepa, cachapa, etc.; Cumare, palmera de fibra textil; y también se llaman así los "
 "chinchorros ó las hamacas que con tal fibra se manufacturan; Curare, una planta de la que se extrae el famoso veneno "
 "con que untan sus flechas y lanzas los indios. Caribabare es un cerro...»")
PASAJE_MENA = (
 "«téngase en cuenta que menoa ó mena quiere decir agua, en achagua, y por eso que hubiese algunos pueblos que "
 "acabaran en mena á orillas de los ríos y que hoy día haya muchos ríos ó quebraditas que tengan tal terminación: "
 "Casimena, Surimena, Tauramena, Iximena, Bujumena, Guachajumena, Guaijuena, Patimena, Tacarimena, Iguamena, "
 "Guariamena, Ypamena, Chitamena, Usamena, Charamena, Masimena.»")
POEMA_115 = [
 "Jainataca Masicatare","Guata miniu guacha","Mata guaibaca girruri","Ribema giarena saicaba","Masicatare guamauca,",
 "¡Neba! caigibe macacha","Cayayi, catabacayi","Carrunatacayi taba","Cayagibe cariani","Lirrico cainabe yaca",
 "Rimedanicaimi Dios","Cagicunabeni Igiagina.","Carruna sichay neni","Carruna mananicai yava","Tanasimi beni ichaba",
 "Caichacai ichaba taba","Lirrico cagicunabeni","Naichaca mayabacaja","Cata queniu debe","Sichai becha machuacaja",
 "Cabaracana lirrico","Ichaba nanacuchajaba","Cata saicabe erri say","Mecucanimiu naucha.","Bitamasi ichaba neni",
 "Eno nenami ibicaubata","Carrunemica ribitama","Coacao ¡neba! nagiaca","Mananicay riani","Coacao yabaja amarra",
 "Machuacayujani neni","Ayyujade machuacaja.",
]

# ── cotejo Neira → Fabo → Jahn ──
J = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "comparandas_jahn_1927.yaml"), encoding="utf-8"))["achagua"]["voces"]
N = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "achagua_neira_ribero_1762.yaml"), encoding="utf-8"))
cal = {c["es"]: c for c in N.get("calibracion_jahn", [])}
def norm(s): return re.sub(r"[^a-z]", "", str(s).lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n"))
fabo = {}
for es, ach, _ in TABLA_108 + TABLA_111:
    fabo.setdefault(norm(es), []).append(ach)
EQUIV = {"cazabe": "cazabe", "casa": "casa", "estrella": "estrella", "piedra": "piedra", "tabaco": "tabaco", "leña": "lena",
         "sepultura": "sepultura", "canoa": "canoa", "cabeza": "cabeza", "nariz": "nariz", "ojo": "ojo", "agua": "agua",
         "pez": "pez", "león": None, "mujer": None}
cotejo = []
for v in J:
    es = v["es"]; jahn = v["achagua"]
    f = fabo.get(norm(es)) or fabo.get(norm(EQUIV.get(es) or "")) or []
    n = cal.get(es, {})
    fila = {"es": es, "jahn_1927": jahn, "fabo_1911": ", ".join(f) if f else None,
            "neira_1762": n.get("manuscrito"), "veredicto_neira_vs_jahn": n.get("veredicto")}
    if f:
        fila["fabo_vs_jahn"] = "coincide" if any(norm(x) == norm(jahn) or norm(jahn) in norm(x) for x in f) else "difiere"
    cotejo.append(fila)
con_fabo = [c for c in cotejo if c["fabo_1911"]]
out = {
 "meta": {
  "obra": "fabo-1911", "generado_por": "6-fusion/scripts/minar_fabo_1911_achagua.py", "minado": "2026-09-12",
  "que_es": ("Lo achagua de Fabo 1911: dos tablas comparativas (pp. 108 y 111-112), el pasaje sobre la terminación -are "
             "(p. 109), la afirmación de que mena = agua (p. 111), noticias bibliográficas (p. 113-114) y un texto achagua "
             "copiado de un manuscrito de pláticas (p. 115). Fabo mismo: «del idioma achagua apenas poseo unas cuantas docenas "
             "de palabras» (p. 108) y «No conozco gramática alguna achagua» (p. 112)."),
  "paginas": "impresas 108-115 = pdf 110-117; transcritas de la imagen, no del OCR (desplaza columnas)",
  "etiqueta_propuesta": "comparanda achagua de SEGUNDA mano (Fabo no da su fuente para las tablas); vale como control de transmisión hacia Jahn, no como atestación",
  "cobertura_medida": {"tabla_108_filas": len(TABLA_108), "tabla_111_filas": len(TABLA_111), "voces_jahn": len(J),
                       "voces_jahn_con_forma_en_fabo": len(con_fabo),
                       "fabo_coincide_con_jahn": sum(1 for c in con_fabo if c.get("fabo_vs_jahn") == "coincide")},
 },
 "hallazgo_principal": {
  "titulo": "El «mena = agua» de Jahn es un error de Fabo, y el manuscrito lo desmiente",
  "cadena": ("Neira y Ribero 1762 (pliego 32): «Agua — Vni»; «Mar — Manoa» (74) → Fabo 1911 p. 111: «menoa ó mena quiere decir "
             "agua» y tabla «Agua — Menoa-mena» → Jahn 1927 p. 377: «agua = mena». Fabo tomó el MAR (manoa) por el agua, y "
             "Jahn lo copió. Verificado en imagen del manuscrito el 2026-09-12 («Aguador — Vni iserri», «Aguacero — Vnia»)."),
  "y_ademas": ("Fabo da DOS formas distintas para «agua» en sus dos tablas: Chitey (p. 108, frente al guaraní chity — sospechoso "
               "de ser guaraní o error) y Menoa-mena (p. 111). Ninguna es la del manuscrito. Los hidrónimos en -mena "
               "(Casimena, Surimena, Tauramena…) que Fabo explica como «agua» piden otra explicación."),
  "consecuencia": "toda comparación caquetío ↔ achagua hecha con las 34 de Jahn hereda este escalón; con el manuscrito delante, Jahn deja de ser la comparanda y pasa a ser control de transmisión",
 },
 "pasaje_are": {"pagina": 109, "texto": PASAJE_ARE,
  "lectura": ("Fabo afirma -are «propia y exclusiva» del achagua, la asocia a hidrónimos de los Llanos (Casanare, Guaviare, Manare, "
              "Guanare…) y a regionalismos (budare, cumare, curare), y recoge —sin hacerla suya— la etimología caribe de Restrepo "
              "Tirado. Medido sobre el manuscrito por el escriba (achagua_neira_ribero_1762.yaml, censo_de_terminaciones): 40 de 2.410 "
              "formas acaban en -re. La exclusividad no se sostiene en el LÉXICO; lo que Fabo vio es un patrón TOPONÍMICO de los "
              "Llanos. Para censo_terminacion_re.yaml: el -are de los ríos llaneros es un comparandum, y budare está en el habla "
              "paraguanera (Medina) y en el dictado con veredicto B."),
  "toca": ["6-fusion/censo_terminacion_re.yaml", "morfema-002", "la hipótesis de Miguel sobre -re / catire"]},
 "pasaje_mena": {"pagina": 111, "texto": PASAJE_MENA},
 "tabla_108_castellano_achagua_guarani": [{"es": a, "achagua": b, "guarani": c} for a, b, c in TABLA_108],
 "tabla_111_castellano_achagua_guahivo": [{"es": a, "achagua": b, "guahivo": c} for a, b, c in TABLA_111],
 "cotejo_34_de_jahn": cotejo,
 "noticias_bibliograficas": [
  {"pagina": 113, "que": "Cita Neira y Rivero 1762 (Arte y vocabulario); el Conde de la Viñaza; y un manuscrito autógrafo de Ezequiel Uricoechea: «Diccionario de la lengua de los achaguas extractado de los escritos de los PP. Juan Rivero y Alonso de Neira en el pueblo de Surmeno [Surimena], año 1762»"},
  {"pagina": 114, "que": "Arístides Rojas, Estudios indígenas: «La oración dominical en lenguas venezolanas», con un Padre Nuestro en achagua tomado de Vergara y Vergara (Historia de la Literatura en Nueva Granada, cap. VI), que también menciona un diccionario achagua autógrafo de un dominico. Lázaro María Girón, «Los antiguos achaguas», en El Papel."},
  {"pagina": "114-115", "que": "Un manuscrito de 425 pp. «Lengua achagua, L. M. J.» (Miscelánea variarum compositionum in exerticiis idiomatis achaguae): pláticas sobre el Decálogo, los Sacramentos, el Credo, y catorce poesías. Fabo lo atribuye con «mucha probabilidad» al P. Rivero o al P. Neira. Empieza «Dios ibanacare yuchamacaje»."},
 ],
 "texto_achagua_115": {"titulo": "Masicatare yarro", "pagina": 115, "versos": POEMA_115,
   "nota": "poesía asonantada copiada del manuscrito L. M. J.; es TEXTO achagua corrido, no lista de voces — material para morfología (nótese carruna-, lirrico, ichaba «leña», Dios, erri «sol»)"},
 "advertencias": [
  "Fabo declara no tener gramática achagua ni más que «unas cuantas docenas de palabras»: sus tablas son de fuente no declarada y con al menos un error grave (agua).",
  "Las tablas se transcribieron de la imagen; la ortografía es la de Fabo (y/i, ck en Navarrick), no la del manuscrito.",
  "El cotejo con el manuscrito usa la transcripción por visión del escriba: verificar la forma exacta en imagen antes de citarla.",
 ],
}
dest = os.path.join(R, "6-fusion", "achagua_fabo_1911.yaml")
io.open(dest, "w", encoding="utf-8", newline="\n").write(yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=110))
print(f"escrito {os.path.relpath(dest, R)}: tabla108 {len(TABLA_108)} · tabla111 {len(TABLA_111)} · cotejo {len(cotejo)} (con Fabo {len(con_fabo)}, coincide {out['meta']['cobertura_medida']['fabo_coincide_con_jahn']})")
for c in cotejo:
    if c["fabo_1911"]: print(f"  {c['es']:10} jahn={c['jahn_1927']:12} fabo={c['fabo_1911']:16} {c.get('fabo_vs_jahn','')}   neira={str(c['neira_1762'])[:40]} [{c['veredicto_neira_vs_jahn']}]")
