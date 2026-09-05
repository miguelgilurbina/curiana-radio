---
tipo: fuente
obra: "Elegías de varones ilustres de Indias (partes I-II)"
autor: "Castellanos, Juan de"
anio: "1857 [c. 1589]"
publicacion: "Biblioteca de Autores Españoles (dir. Buenaventura Carlos Aribau), 2ª ed., Madrid, M. Rivadeneyra, 1857. La parte I se imprimió en 1589; la II quedó inédita hasta la BAE. Otras ediciones que cita el repo: ANH, Caracas 1962 (t. 57 — la de Velasco, cita por versos) y ANH 1987 (la de González Batista, cita por páginas)"
genero: cronica
local: "fuentes_caquetios/Castellanos_1857_Elegias_partes_I-II_texto.txt"
paginas: "— (texto OCR: partes I y II enteras; la de Coro es la parte II, elegía I, desde la p. 185 de la ed. 1857)"
acceso: "Internet Archive (OCR de Google Books); descargado el 2026-08-14 en la sesión 07_rastreo_documental"
capa_texto: si
estado_minado: en-curso
prioridad: alta
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-05
aliases: ["Castellanos", "Castellanos 1589", "Castellanos 1857", "Elegías", "Elegías de varones ilustres de Indias", "Juan de Castellanos", "castellanos-elegias"]
---

# Castellanos 1857 [c. 1589] — *Elegías de varones ilustres de Indias*

## Qué es

La crónica **en verso** del descubrimiento y la conquista — endecasílabos en
octavas reales, miles de ellos — de Juan de Castellanos, que llegó joven a las
Indias, anduvo la costa de Tierra Firme como soldado y acabó de clérigo en
Tunja (biografía corriente, no verificada aquí). Para el proyecto importa
**una sola elegía: Parte II, Elegía I**, la de Coro — Ampiés, los Welser,
Manaure, y la única lista de pueblos caquetíos costeros que trae un texto del
siglo XVI.

Es fuente **colonial** (regla 3): habla de 1525-1540 con décadas de distancia
y con la rima mandando. Vale como testigo de **nombres** y de hechos de
contacto; de precontacto no dice nada por defecto.

## Por qué tiene ficha ahora

Se citaba como `castellanos-elegias` desde el 2026-08-25
(`6-fusion/castellanos_1589_toponimos.yaml`) **sin nota en `4-fuentes/`**: la
regla 8 rota durante once días. Lo detectó `juntar_toponimos.py` el
2026-09-04 al validar cada obra contra la bibliografía. Esta nota cierra la
deuda y de paso mide lo que nadie había medido del archivo.

## Estado técnico (verificado 2026-09-05)

| | |
|---|---|
| Archivo | `fuentes_caquetios/Castellanos_1857_Elegias_partes_I-II_texto.txt` — 3,4 MB, 147.532 líneas |
| Qué contiene | **Parte I** (líneas 761-46824) y **Parte II** (46845-fin). Las partes III-IV NO están |
| Origen | OCR de Google Books («Digitized by Google» en cada corte de página) vía Internet Archive |
| Capa de texto | sí — es un `.txt`; se lee con `grep` y `sed -n 'a,bp'` |
| Páginas impresas | en las cabeceras de página, **poco fiables**: el OCR da «905» por 205 y «109» por 199. La única cabecera limpia de la elegía de Coro es la línea 47693: «PARTE II, INTRODUCCION. 185» |

### Cómo escribe los nombres (medido el 2026-09-05)

La regla del INDICE («las fuentes coloniales no usan la ortografía moderna»)
aquí se cumple **dos veces**: la grafía del siglo XVI y encima la del OCR.

| Lo que buscas | Lo que hay | Veces |
|---|---|---|
| caquetío | `caquetía`, `caquetia`, `caquetíos`, y el OCR `caquetfo` | 6 |
| Curiana | **`Coriana`** (Curiana: 0) | 1 |
| Manaure | `Manaure` | 2 |
| Paraguaná | `Paraguan-` | 5 |
| Ampiés | `Ampiés` 8 · `Ampies` 4 | 12 |
| Todariquiba | **`Todariquibo`** (con -o; -a: 0) | 1 |
| Jurijurebo | **`Hurehurebo`** 1 + el OCR `Hurehurcbo` 1 (jurijur-, hurihur-: 0) | 2 |
| Hurraque | **`Hurraqui`** | 1 |
| Miraca, Cumarebo | tal cual | 1 y 1 |
| Curazao | `Curazao` (Curaçao: 0) | 2 |
| Alfínger | `Alfinger` | 1 |
| Federmann | `Federm-`, `Fedreman`, `Fedeman`: **0** — cómo lo llama está por medir | ? |

### 🔴 Dos ceros falsos, uno por sesión

1. **2026-08-14**: se buscó `jurijureb | hurihureb | jurijure | urihure` → 0, y
   se concluyó que Castellanos no traía el lugar. La forma del texto es
   **Hurehurebo**: h~j se probó, e~i interior no. Revertido el 2026-08-25
   ([[velasco-2015-resistencia]] traía la cita con verso).
2. **2026-09-05**: `grep -i "lengua generosa"` → 0 para el verso de *Coro =
   viento*. El OCR escribe **`genero>a`** (línea 48217). Con `genero.a` sale.

Receta que queda: para un nombre propio, **permutar las vocales interiores**;
para una cita, **aceptar cualquier carácter donde el OCR pudo fallar**
(`.` en vez de la letra). Un cero mide la consulta (regla 6).

## Ediciones y cómo se cita — tres sistemas en el repo

| Edición | Quién la cita | Cómo | Ejemplo |
|---|---|---|---|
| BAE 1857 (esta) | [[arcaya-1920]] vía [[brito-figueroa-poblacion-economia]] | por página | «*Elegías*, p. 185» — y coincide: es la Introducción de la Parte II, la de Coro |
| ANH Caracas 1962, t. 57 | [[velasco-2015-resistencia]] | por verso | «vv. 80-81» = «Señor de la ciudad Hurehurebo» |
| ANH Caracas 1987 | [[gonzalez-batista-nombre-de-coro]] | por página | «p. 175» = *Coro viento / quiere decir en lengua generosa* |

**Convención para esta nota y para el canon**: se cita por **línea del `.txt`**
y, cuando la cabecera es legible, por página de la ed. 1857 — así cualquiera
llega al verso en segundos: `sed -n '48246,48261p'`.

## Lo minado hasta ahora (2026-08-25 · 2026-09-05)

Todo en **Parte II, Elegía I** (Coro). Detalle y valoración en
`6-fusion/castellanos_1589_toponimos.yaml` (sin fusionar); los topónimos,
cruzados con las demás fuentes, en `6-fusion/TOPONIMOS_POR_FUENTE.md`.

1. ⭐⭐ **Las once ciudades** (líneas 48246-48261, p. 185): *«Doce leguas en
   torno del asiento / Había población engrandecida, / Ciudades de grandísimo
   momento, / Como Todariquibo, Zacerida, / […] Carao, Tamadoré, Capatarida, /
   Carona, Guaybacoa, Cumarebo, / Miraca, Hurraqui, Hurehurebo; / Con otros
   que callamos de presente.»* Once topónimos costeros en un pasaje de 1589.
   Cruce medido (2026-09-04): **cinco** están en el índice de Esteves
   (Guaidabacoa, Hurraque, Miraca, Todariquiba, Jurijurebo) y **dos** los
   confirma la carta de Bastidas de 1538 por vía independiente (Miraca,
   Todariquiba). Es la fuente que Arcaya y Brito usaban sin que el proyecto la
   tuviera, y trae demografía para `asentamientos.yaml`
   ([#92](https://github.com/miguelgilurbina/curiana-radio/issues/92)).
2. ⭐ **La casa de Ampiés y el señor de Hurehurebo** (líneas 48146-48175):
   1525, el «mancebo, / Señor de la ciudad Hurehurebo» retenido con «sus
   hijos, su mujer y una su hermana» — bautizados Fernán García, doña Mencía,
   **doña Juana**, y otra cautiva doña Teresa. La hipótesis Juana ↔ Judibana
   (Castellanos + Arcaya p. 167 + tradición local) está en el yaml §3, **no
   demostrada** y con la reserva de que la tradición pudo derivar el nombre
   desde el verso.
3. ⭐ **Coro = 'viento'** (líneas 48214-48219, p. 185) — **verificado hoy**:
   *«[…] pues Coro viento / Quiere decir en lengua generosa, / Y ansí es
   aquella tierra muy ventosa.»* Es etimología de cronista, no glosa
   atestiguada: [[arcaya-1920]] la refuta («esto es un error»), [[esteves-1989]]
   la trae con ironía («verbo retozón»), González Batista la usa contra
   *Coriana*. Entra al esquema `lecturas` del topónimo Coro como
   `etimologia-de-cronista`, nunca a `glosa_fuente`.
4. ⭐ **Manaure, rey de Coro** (líneas 52126-52148, II-1, canto II): el nombre
   como salvoconducto camino de los llanos — «Por ser hermanos de señor tan
   bueno, / Tengo por bien dejaros con la vida». Radio de prestigio del título
   en 1589; yaml §4.
5. **Negativos, medidos**: la expresión literal «Gran Señor de Jurijurebo» no
   está (la atribución es de Esteves); **la muerte por perros** del señor de
   Hurehurebo no está — la línea 49364 («mataba con perros») es caza de
   venados por soldados hambrientos; el «Piache de Todariquiba» que Velasco
   cita como v. 98 **no se localizó** en la ed. 1857 (`Todariquibo` aparece
   una sola vez, en la lista). O está en otra parte de la elegía con otra
   grafía, o la ed. 1962 difiere: probar `piache` + permutaciones.

## Pistas sin minar (líneas medidas el 2026-09-05)

- **55308** — *«Joan de la Puente, / Lengua de caquetíos escelente»*: los
  intérpretes. Se suma al Esteban (Martín) del yaml §4 como «lenguas»
  documentadas — dato para la esfera de transmisión/contacto.
- **58543** — *«Joan Calahuyare, caquetío»*, que defendió a Diego de Montes
  «con valeroso brío»: un **antropónimo caquetío** con nombre cristiano
  delante. Material para la regla de [[velasco-2015-resistencia]]: un nombre
  propio atestigua sus morfemas aunque nombre a una persona.
- **36073** (Parte I) «De gente jaguas y de caquetía»; **47710**
  «Mayormente la gente caquetía»; **51124** «Era guanebucan y caquetia»;
  **52211** «En un pueblo de gente caquetia» — los cuatro contextos restantes
  del etnónimo, sin leer.
- **La Elegía I entera** (líneas ~48636-53100): está *grepeada*, no leída.
  Leerla es la tarea; los cantos van por Ampiés, Alfínger, Federmann y los
  llanos.
- Cómo nombra a los Welser y a Federmann (grafía por medir, ver tabla).

## Estatus epistémico: testigo de nombres, no de glosas

Crónica en verso, colonial, compuesta décadas después por alguien que vivió
en la región. **Primera mano para la toponimia que oyó** (por eso las once
ciudades pesan); segunda mano para 1525-1540; y **cero autoridad lingüística**:
sus glosas de lengua («Coro viento») son etimologías de cronista y así se
etiquetan. La rima deforma nombres (`Todariquibo` por la asonancia con
`Hurehurebo`) — otra razón para permutar vocales al buscar.

## Enlaces

[[esteves-1989]] · [[velasco-2015-resistencia]] · [[gonzalez-batista-nombre-de-coro]] · [[arcaya-1920]] · [[alvarado-1921]] · [[brito-figueroa-poblacion-economia]] · [[01-rastreo-fuentes]] · [[toponimia]] · [[INDICE_FUENTES]]
