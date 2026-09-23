# Zayas 1931 en la lista maestra del taíno: cómo engancharlo y qué mueve

> Minería 3, parcela Zayas (2026-09-23). Propuesta, no fusión (regla 5).
> Datos: `6-fusion/taino_zayas_1931.yaml`. Bitácora: `4-fuentes/zayas-1931.md`.
> **No se tocó** `6-fusion/scripts/consolidar_taino.py` (lo está ampliando la
> rama `campana/mineria3-vocabularios`); aquí va el lector para pegarlo.

## Lo que resultó falso al medir

1. **«Goeje apoya cuatro voces taínas en Zayas»**: de las cuatro, sólo **una**
   tiene fuente del XVI en Zayas (`anaiboa`: Relación de Echagoían, c. 1561,
   Documentos Inéditos — ✅ verificada en imagen, t. I p. 37).
   - `anaki`: Zayas la da como **eyerí** de Boriquén (✅ imagen, t. I p. 39), sin
     cronista — la lista de Rafinesque, no taíno. La capa OCR se come la glosa.
   - `anua` 'vautour' **no existe** en Zayas 1931 (cero medido como cabeza y en el
     cuerpo). Lo que hay en la posición alfabética que Goeje cita es `Aura`,
     sin cronista (D'Orbigny la cree de la Guayana). Lectura probable: `anua` es
     `aura` mal leída; la transcripción de Goeje ya la marcaba `ocr: dudoso`.
     Hay que ver Goeje p. 14 en imagen antes de corregir.
   - `manaya`: Zayas la saca de «las tradiciones haitianas» (el relato de
     Caracaracol, que es Pané) sin nombrar a Pané: no añade atestación.
2. **«Zayas es un compilador más»**: Zayas **nombra el cronista** en la mayoría de
   las entradas que se leyeron, y lo cita con la voz dentro del pasaje. Es el
   intermediario que más cadenas cierra de los leídos hasta hoy.

## Cómo engancharlo (cuando la rama de vocabularios esté fusionada)

En `consolidar_taino.py`, un lector más y su fila en `LECTORES`, y
`"zayas-1931"` en `INTERMEDIARIOS`:

```python
def leer_zayas():
    Y = _y("taino_zayas_1931.yaml")
    out = []
    if not Y:
        return out
    for bloque in ("voces_de_goeje", "voces", "voces_sin_cronista_en_la_lista"):
        for e in Y.get(bloque) or []:
            forma = e.get("forma_fuente") + ((" ~ " + e["agrupa_con"]) if e.get("agrupa_con") else "")
            out.append(_reg(forma, e.get("glosa_fuente"),
                            "zayas-1931", "intermediario",
                            pagina=e.get("pagina_impresa"),
                            declara=e.get("fuente_que_declara_el_autor"),
                            variedad=e.get("variedad_o_isla"), campo=e.get("campo"),
                            en_el_lexicon=e.get("en_el_lexicon"),
                            sacada_del_taino=e.get("sacada_del_taino"),
                            aviso=("conjetura del autor"
                                   if e.get("tipo_de_apoyo") == "conjetura-del-autor" else None)))
    return out
```

Tres condiciones, y las tres importan:

- **`declara` sale SÓLO de `fuente_que_declara_el_autor`.** El campo `lectura`
  nombra cronistas para descartarlos (p. ej. «Pedro Mártir, para el objeto, no
  para la voz»): si se pasa como `aviso`, el regex de `CRONISTAS` los contaría.
- **`agrupa_con`**: el lema del script no junta `jagüey`/`xagueye`,
  `jobo`/`hobo`, `cibucán`/`sibukan`, `henequén`/`henequeu`, `jibe`/`hibii`,
  `dujo`/`duho`, `casabe`/`cazabi`, `guabina`/`Guabinas`, `manigua`/`Maniguas`.
  Sin el campo quedan como nueve voces nuevas y las de la lista no suben.
- **«documento de época»**: Zayas cita documentos del XVI que no son de la
  Colección de Documentos Inéditos (Zuazo 1518, Jerónimos 1519, cabildo de La
  Habana 1551, dos sobre Cuba de 1526 y 1580). Para contarlos, el patrón de
  `"Archivo de Indias"` en `CRONISTAS` necesita `|[Dd]ocumento de [ée]poca`
  (la transcripción de Coll y Toste usa la misma etiqueta).

## Lo que mueve (medido con el lector de arriba sobre una copia del script en el scratchpad)

Base (la lista de `main`, re-corrida igual) → con Zayas:

| | base | con Zayas |
|---|---|---|
| voces distintas | 263 | 264 (entra `aura`) |
| i-primaria-del-XVI | 172 | 194 |
| ii-solo-secundaria | 77 | 58 |
| iii-conjetura-moderna | 14 | 12 |
| con 2+ cronistas independientes | 22 | 39 |
| conceptos comparables con el caquetío atestiguado | 12 | 12 |

- **Suben a clase i** 17 voces que no cambian de lema (`anaiboa`, `bahari`,
  `baikua`, `basareke`, `iakua`, `ibuera`, `ikotea`, `ikuaka`, `kabuia`, `koa`,
  `kokuio`, `kuaiakan`, `kuaka`, `kuakamaio`, `kuatiao`, `nikua`, `teitoka`) y
  cinco más al juntarse por `agrupa_con` (henequén, jibe, jobo, jagüey, cibucán).
- **Las 52 claves del lexicón**: la clase no cambia (41 con cronista antes y
  después), pero 22 filas muestran más cronistas — entre ellas `cemi` (Pané),
  `cobo` (Oviedo), `huracan`, `hutia`, `kunuku`, `maisi`, `manati` (Las Casas),
  `batata` (Pedro Mártir), `cacique` (Mártir y Gómara). Ojo: en `bohío` y
  `tabako` el cambio es en parte artefacto — la fila toma la voz con más
  cronistas de las que mencionan la clave, y ahora es otra voz (`caney`, en
  el caso de `bohío`).
- **El número que decide el cruce no se mueve** (12 → 12): lo que Zayas aporta
  son objetos, plantas y animales, no conceptos del caquetío atestiguado.

## Dos subidas que NO hay que creerse sin mirar

- `kuaka` sube por Pedro Mártir, pero Mártir da `guaca` = **'región, comarca'**
  (Guaca-yarima); la glosa de la lista ('vault for storing provisions', Brinton)
  sigue sin cronista. El consolidador agrupa por forma y no ve la diferencia.
- `kuakamaio` sube por Las Casas, pero el pasaje es de **Guadalupe**, isla
  caribe: «que llamaban» no dice quién. En duda, degradar.

## Tres cosas para Miguel

**A. El manatí tiene dos cronistas que se contradicen.** Oviedo (t. I p. 434, ya
aclarado esta semana): el nombre se lo pusieron los cristianos. Las Casas,
citado por Zayas (t. II p. 178): «los que llamaban los indios manatíes, la
penúltima sílaba luenga». Opciones: (a) la voz se queda taína con las dos citas
y el conflicto en `notas`; (b) se degrada hasta leer el pasaje de Las Casas en
la fuente; (c) se da por buena la de Oviedo. Recomiendo (b): es barato y el
pasaje de Las Casas está en `las-casas-1875`.

**B. `cohiba`/`tabako`: cuarta mano.** Las Casas (cohoba = el polvo y la
ceremonia; tabacos = los rollos) y Oviedo (tabaco = el instrumento), vía Zayas,
se suman a Brinton, Goeje y Bachiller contra la pareja del lexicón.

**C. `bagua` 'mar' es del glosario de la Academia**, no de Oviedo — lo dice el
propio Zayas (t. I p. 72). Es la trampa de `datihao` otra vez: la voz sigue sin
cronista aunque dos obras la traigan.

## Lo que NO se hizo

- No se barrió el diccionario entero: sólo las 4 de Goeje, las claves del
  lexicón y las voces sin cronista de la lista que Zayas trae como cabeza.
  Quedan sin leer ≈ 3.000 cabezas, sobre todo topónimos y caciques de los
  repartimientos de 1514 (útiles para toponimia antillana, no para esta pregunta).
- Sólo dos entradas se verificaron en imagen. Las demás citas están
  normalizadas a ojo desde el OCR (c/e, ñ/fi). Las imágenes por página se bajan
  sueltas (≈ 200 KB): `https://ufdcimages.uflib.ufl.edu/AA/00/08/98/31/00001/NNNNN.jpg`
  con NNNNN = página del PDF + 10 en el t. I. En el t. II no se midió el desfase.
- Bernáldez (Cura de los Palacios) y José de Acosta, del XVI y citados por
  Zayas, no están en `CRONISTAS`: no cuentan hasta que alguien lo decida.
