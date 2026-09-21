---
tipo: issue-pendiente
titulo: "Campaña del taíno T2 — Las Casas vol. I, Pané y Brinton: 36 de 52 entradas dejan de estar sin procedencia"
labels: [mineria, taino, esfera-de-contacto, decision]
fecha: 2026-09-21
campana: taino-2026-09-21
parcela: T2
propuestas:
  - 6-fusion/taino_las_casas_1875.yaml
  - 6-fusion/taino_pane_c1498.yaml
  - 6-fusion/taino_brinton_1871.yaml
scripts:
  - 6-fusion/scripts/mapa_capitulos_las_casas.py
  - 6-fusion/scripts/medir_taino_t2.py
---

# Campaña del taíno — parcela T2

Tres fuentes: `Las_Casas_1875_Historia_Indias_vol1.pdf`,
`Pane_c1498_Relacion_Antiguedades_Indios_wikisource.txt` y
`Brinton_1871_texto.txt`. Todas las cifras de esta nota salen de
`python 6-fusion/scripts/medir_taino_t2.py` (regla 1).

## 0. Lo que resultó falso al medirlo

| Se daba por bueno | Medido el 2026-09-21 |
|---|---|
| «Brinton 1871 (+ el PDF)» | **el PDF tiene 0 bytes.** Todo sale del `.txt` (87.820 bytes). Ya lo decía la nota desde 2026-07-29 |
| «Las Casas comenta "la penúltima luenga"» | **en el tomo I no aparece: `penultima` = 0.** Lo que hay es «la última sílaba luenga y aguda» ×2 y «la última aguda» ×1. La frase existe, pero es del lib. III, que no tenemos, y la conocemos porque **Brinton la cita** (p. 14, nota 28) |
| «Las Casas distingue tres lenguas (la general, el macorix, el ciguayo)» | en el tomo I dice que macoriges y cyguayos «tenían diversas lenguas de la universal» y a renglón seguido **declara que no se acuerda** de si diferían entre sí. La tripartición limpia está en la *Apologética*, que no tenemos |
| «Brinton compara con el lokono» | **`lokono` = 0 ocurrencias.** Dice siempre `Arawack`, y da el autónimo `lukkunu` |
| «el PDF de Las Casas da página impresa» | es el ebook de Project Gutenberg #49298: su pie de página es un contador propio (coincide con el índice del pdf en 609 de 613 páginas). La paginación de 1875 se recupera **sólo** por el índice original, que sobrevive en pdf 572-596 |
| Pané: «la edición/traducción es la que Wikisource declara» | **Wikisource NO la declara** (consultada el 2026-09-21): da autor, fecha y licencia, y nada más. Y avisa: «La traducción de la obra puede no estar en dominio público» |
| Pané: «45 entradas `taíno` y 9 `taíno-reconstruido`» | 43 + 9 = **52** |
| la nota de Las Casas: «fuente de rendimiento nulo, documentado tres veces» | con la pregunta **taíno** —no caquetío, no corpus cultural— el tomo I da 26 voces con glosa y 10 pasajes metalingüísticos. No era la fuente: era la pregunta |

## 1. Qué se preguntó y qué dio

**Las Casas tomo I** — ¿qué voces da, con qué glosa y página, y qué dice sobre
la lengua misma? Dio 26 voces con glosa verbatim y 10 pasajes
metalingüísticos, incluidos los tres del acento y, sobre todo, el de los
mazoriges y cyguayos y el trío `caona`/`nozay`/`tuob` para 'oro' en tres zonas.
Cubierto pasaje a pasaje: capítulos XL-LXVII (primer viaje y descripción de La
Española). Barrido por patrón: el tomo entero.

**Pané** — leído entero, las 29 subpáginas. 24 voces con glosa, 9 deidades,
8 lugares del mito, 5 ritos, y el único enunciado taíno con glosa de toda la
parcela (`Dios naboria daca`).

**Brinton** — el vocabulario entero (68 entradas, pp. 11-14) con el cronista
que hay detrás de cada una, los 4 numerales, las frases, y la descomposición
toponímica de las pp. 14-15. La tabla de correspondencias queda aparte y
limpia para el agente T4.

## 2. Lo que NO dio

- **Religión taína en Las Casas tomo I: cero.** `cemi`/`zemi`/`çemi`,
  `behique`/`buhiti`, `areito`/`areyto`, `cohoba`, `Yocahu`, `Atabey`,
  `Guabancex`, `bagua`, `duho`, `naboria`, `goeiza` — todos a 0, probados con
  las grafías del XVI. Confirma las tres sesiones previas, ahora con la lista
  completa. Todo eso está en Pané.
- `opia` da 77 en Las Casas y **son todas ruido** (propia, copia). La voz taína
  no está en el tomo I.
- `macana` en Las Casas: 2 ocurrencias y **las dos son la misma línea del
  epígrafe** del cap. LXVII (cabecera + índice). En el cuerpo el arma se
  describe sin nombrarla: «una espada de tabla de palma [...] no aguda, sino
  chata». Es la trampa 1 de la campaña, en la fuente de la campaña.
- Pané no tiene `areíto` en ninguna grafía: describe la ceremonia sin nombrarla.
- 16 de las 52 entradas siguen sin cita: las 8 `taíno-reconstruido` sin
  atestación (`abba`, `acoa`, `aduri`, `agari`, `akcicyaa`, `thigisi`,
  `wacusi`, `wagulo`) y 8 `taíno` (`guabina`, `guayaba`, `maboya`, `manati`,
  `manigua`, `papaya`, `piragua`, `tuna`).

## 3. La cifra

```
entradas taínas en VOCABULARIO_BASE : 52   (43 taíno + 9 taíno-reconstruido)
con procedencia.obra HOY            : 0
con cita PRIMARIA (Las Casas o Pané): 25
sólo por vía SECUNDARIA (Brinton)   : 11
TOTAL con cita tras esta parcela    : 36
siguen sin ninguna                  : 16
```

## 4. Lo que hay que decidir (Miguel)

### D-T2.1 — ¿Se fusionan las procedencias?

Las 36 entradas pueden recibir `procedencia.obra` sin cambiar de capa ni de
glosa: sólo dejan de estar sin fuente (regla 8). Las 25 primarias llevan obra +
libro + capítulo + página; las 11 secundarias llevan `brinton-1871` con
`via:` y el cronista que Brinton cita.

- **(a)** fusionar las 36.
- **(b)** fusionar sólo las 25 primarias y dejar las 11 con
  `deuda: sin-procedencia-primaria`.
- **(c)** no fusionar nada todavía y esperar a que T1/T3/T4 cierren, para
  aplicar una sola tanda.

*Recomendación: **(b)**.* La distinción primaria/secundaria es justo lo que la
skill §8 pide no perder, y escribirla en el lexicón la hace consultable. Las 11
de Brinton se pueden subir a primarias después, sin descargar nada, verificando
contra `Angleria_1892` (ver D-T2.4).

### D-T2.2 — `daca`

Hoy es `taíno-reconstruido`. Pané la atestigua dentro de una oración glosada:
«Dios naboria daca, que quiere decir: yo soy siervo de Dios» (cap. XXV).

- **(a)** subirla a `taíno` atestiguado, **declarando que es de MACORIX**, que
  es la lengua distinta, no la general.
- **(b)** dejarla reconstruida y anotar la atestación en `notas`.

*Recomendación: **(a)** con la declaración.* Pero es de las que mueven canon, y
la regla dice que en duda se degrada: si la etiqueta no admite decir «macorix»,
mejor **(b)**, porque llamarla «taíno» a secas afirma justo lo que la fuente
niega tres párrafos antes.

### D-T2.3 — `taita`

Su único apoyo es Brinton p. 13, y la fuente que Brinton cita es **Richardo,
diccionario provincial cubano del siglo XIX**. No es atestación colonial.

- **(a)** marcarle `deuda: sin-procedencia-colonial` y dejarla.
- **(b)** degradarla de capa.
- **(c)** archivarla.

*Recomendación: **(a)**.* Degradar necesita saber si otra fuente la sostiene, y
eso no lo he medido.

### D-T2.4 — Pedro Mártir está en casa

Doce entradas del vocabulario de Brinton y **la única conversación taína
conocida** (`Teitoca teitoca...`) vienen de Pedro Mártir. `Angleria_1892`
vols. 1 y 4 están en `fuentes_caquetios/`. Verificarlas contra el original
convertiría 12 citas de segunda mano en primarias **sin descargar nada**.

- **(a)** abrir sesión para eso.
- **(b)** dejarlo en el backlog.

*Recomendación: **(a)**.* Es lo de mayor rendimiento por hora que deja esta
parcela.

### D-T2.5 — El nombre «taíno»

Brinton (p. 13) demuestra que «taíno» es el truncamiento de `nitayno` —un
TÍTULO de nobleza: «caballero y señor principal» en Las Casas tomo I cap.
LVIII— que Rafinesque ascendió a nombre de pueblo en 1836, y lo rechaza: «no
hay la menor autoridad para esto». Los autónimos que sí hay son locales:
`lucayos` = «hombres de las islas», `Siboneyes` = «hombres de las rocas».

No propongo renombrar ninguna etiqueta. Propongo que **la nota de la fuente y
el glosario del vault lo digan**, para que el proyecto no afirme de paso lo que
su propia fuente niega — y porque encaja con lo que ya sabemos: no había un
pueblo ni una lengua a los que poner un nombre único.

- **(a)** anotarlo en las notas de fuente y en el glosario.
- **(b)** anotarlo además en la web, donde `/simulador` explica la esfera.
- **(c)** nada.

*Recomendación: **(a)**, y **(b)** cuando toque tocar esa página.*

### D-T2.6 — Voces nuevas candidatas

Las tres propuestas listan candidatas con glosa y cita. Las que más pesan, por
ser de NÚCLEO o de GRAMÁTICA y no de comercio (skill §3):

| forma | glosa | dónde |
|---|---|---|
| `nacan` | 'medio, centro' | Las Casas I.XLIV (con análisis del cronista: `Cuba`+`nacan`) + Brinton p. 13 (`Ar. annakan`) |
| `siba` / `ciba` | 'piedra' | Pané VI + Brinton p. 13 (idéntica en arawack) |
| `turey` | 'cielo' | Las Casas I.LX + Brinton p. 13 |
| `goeiz` / `opia` | 'alma del vivo' / 'alma del muerto' | Pané XIII, en oposición explícita |
| `operito` | 'muerto' | Pané XIII + Brinton p. 13 |
| `mayani` | 'de ningún valor' | Brinton p. 13 (Pedro Mártir) — ya está en el lexicón |
| `hequeti`, `yamosa`, `cauocum`, `yaraoucobre` | 1, 2, 3, 4 | Brinton p. 14 (Las Casas, *Apol.* 204) |
| `bazca` | 'no' — **MACORIX** | Brinton p. 18 (Las Casas) |
| `caona` / `nozay` / `tuob` | 'oro' en tres zonas | Las Casas I.XLV y I.LXVII |

Se fusionan voz a voz, como siempre.

## 5. Deuda que esto genera

1. **No sabemos qué retraducción de Pané tenemos.** Wikisource no lo dice y el
   archivo tampoco. Arrom 1974, la edición crítica, sigue fuera del repo.
2. **La traducción de Pané puede no estar en dominio público** (lo avisa
   Wikisource). Consecuencia práctica: de ese archivo se citan formas y glosas
   cortas, no párrafos largos. Los YAML ya están escritos así.
3. **El PDF de Brinton lleva desde 2026-07-29 con 0 bytes.** Sin él no se
   pueden verificar las páginas 13, 16 y 17, cuyos encabezados perdieron el
   número en el OCR.
4. **Los tomos II-V de Las Casas y la *Apologética* no están.** Brinton cita de
   ellos los caps. 2, 46, 61, 120, 197, 198, 199, 204 y 241 de la
   *Apologética* y el lib. III cap. 21 de la *General*: ahí está el grueso del
   taíno documentado, incluidos los numerales, los tres rangos sociales y «la
   penúltima luenga». **No se descargó nada** (restricción del encargo): queda
   anotado para que lo decida Miguel.
5. **Los diez dobletes de Pané** (`Guaguyona`/`Guahayona`,
   `Basamanaco`/`Ayamanaco`/`Bayamanicoel`, `buhitihu`/`buhuitihu`/`bohutis`,
   `Vaibrama`/`Buyayba`, `Yocahu Vagua Maorocoti`/`Yiocavugama`,
   `Itiba Yauvava`/`Tauvava`, `Matinino`/`Matanino`, `Macorix`/`Marcorix`,
   `Guarionex`/`Guarionel`, `Maviatúe`/`Mahuviativire`) sólo los resuelve una
   edición crítica. Hasta entonces, cada forma se cita como está.
6. **`Bugi` y `Aiba`**, que Brinton atribuye a Pané, **no están en el Pané que
   tenemos** (0 ocurrencias). O es otra edición, o Brinton las sacó de otro
   sitio. Sin resolver.

## 6. Lo que vi de paso y no es de esta parcela

- **La escala social taína está completa y ordenada** entre las tres fuentes:
  `matunheri` (los más altos) › `cacique` (rey) › `bajari` (señor de aldea) ›
  `nitayno` (caballero) › `naboria` (servidor) › `guaoxeri` (la clase más
  baja). Eso es material de `3-mundo/` (geografía política), no del lexicón, y
  da una comparanda articulada para pensar la jerarquía caquetía.
- **La única oración taína conocida por Pedro Mártir** (`Teitoca teitoca...`)
  se puede verificar aquí mismo. Ver D-T2.4.
- **La quema de sabana para cazar hutías** (Las Casas I.LVI) es ecología de
  manejo antillana. No se proyecta a Paraguaná; queda dicha.
- **`-caco` 'ojos' y `ma-` privativo** salen de las dos frases de insulto que
  Brinton recoge (p. 14). El caquetío tiene `ma-` privativo declarado en
  CLAUDE.md con sus dos apoyos (van Buurt §8, Perea p. 555). Un morfema
  gramatical compartido es dato de FILIACIÓN, no de contacto (skill §3): **es
  lo más fuerte que esta parcela pone en la mesa de T4**, y merece su propia
  sesión de cruce.
