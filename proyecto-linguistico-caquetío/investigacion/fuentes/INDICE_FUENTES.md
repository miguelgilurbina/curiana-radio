---
tipo: indice
ambito: todas las fuentes del proyecto
archivos_en_fuentes_caquetios: 30
obras_distintas: 24
archivos_vacios: 6
medido: 2026-07-29
---

# Índice de fuentes — estado real, medido

> Esta nota es la versión **viva y verificada** de la tabla de
> [[PLAN_MAESTRO]] §1.1. Cada fila se midió el 2026-07-29 abriendo el archivo:
> tamaño, páginas (`pypdf`), capa de texto (`pdftotext -f 1 -l 30`), y cuántos
> hechos del corpus y entradas del lexicón lo citan realmente.
>
> **El nombre de un archivo no es un dato verificado.** Tres de las conclusiones
> de abajo contradicen lo que el proyecto creía.

## Las tres correcciones que salieron de medir

1. **🟢 [[alvarado-1921]] SÍ tiene capa de texto.** Estaba clasificada como
   "escaneo de imagen, no extraíble sin OCR" — eso era `pypdf`. Con `pdftotext`
   salen **704 KB de texto limpio, 354 páginas**. **F3 no está bloqueada.**
   Lo mismo valía ya para [[arcaya-1920]] y [[jahn-1927]].
2. **🟢 [[oviedo-y-banos]] está disponible.** El archivo de 0 bytes es
   `Oviedo_Banhos_1885_...`; el gemelo `Oviedo_Banhos_Conquista_Poblacion_...`
   tiene **519 páginas con texto**. La obra que el programa señaló por su
   cobertura de sucesión cacical **existe y nunca se ha leído**.
3. **🔴 [[schroeder-2018|Un archivo tiene el nombre de otra obra]].**
   `Schroeder_et_al_2018_PNAS_Origins_Caribbean_Taino.pdf` contiene en realidad
   *Early human dispersals within the Americas* (Moreno-Mayar et al., Science
   2018). Nadie lo ha citado — por suerte.

## Inventario medido

### Disponibles y con texto

| Fuente | Pp. | Estado de minado | Sostiene | Prioridad |
|---|---|---|---|---|
| [[zavala-reyes-2015]] | 20 | **parcial (76%)** | 7 hechos · **164 entradas del lexicón** | F7 |
| [[oliver-1989-cap3]] | 113 | parcial (2 sesiones) | **15 hechos** · 2 lex. | barridos restantes |
| [[oliver-1989-cap2]] | 109 | **sin minar** | 1 hecho | **F5 · ALTA** |
| [[arcaya-1920]] | 348 | minado (religión/familia) | **13 hechos** · 1 lex. | media |
| [[jahn-1927]] | 510 | parcial (3 sesiones) | **16 hechos** · 4 lex. | media |
| [[alvarado-1921]] | 354 | **sin minar** | 1 hecho · **0 lex.** | **F3 · ALTA** |
| [[gatschet-1885]] | ~10 (2 txt) | **sin minar** | 0 · **0 lex.** | **F4 · ALTA** |
| [[van-buurt-2014]] | 48 | **sin minar** | 1 hecho · **0 lex.** | **F6 · ALTA** |
| [[oviedo-y-banos]] | 519 | **sin minar** | 1 hecho (vía Zavala) | alta |
| [[camacho-2011]] | 13 | minado | **16 hechos** | hecha |
| [[antczak-2015-las-aves]] | 38 | minado | 7 hechos | hecha |
| [[antczak-2017-cariban]] | 45 | **sin minar** | 0 | media |
| [[adam-1879]] | 27 | minado | 1 hecho | hecha |
| [[angleria-1892]] | 460+492 | parcial (1 dato) | 1 hecho | media |
| [[las-casas-1875]] | 613 | minado — **nulo ×3** | 0 | baja |
| [[guerra-curvelo-palabrero]] | 22 | minado | 4 hechos | hecha |
| [[perea-alonso-1942]] | 926 | **descartada** (gramática lokono) | 0 | descartada |
| [[schroeder-2018]] | 14 | sin minar · **mal nombrada** | 0 | baja |
| [[brinton-1871]] (txt) | — | minado | **84 entradas del lexicón** | hecha |

### Bloqueadas o rotas

| Fuente | Problema | Ruta de salida |
|---|---|---|
| [[gilij-1780-1783]] | **sin capa de texto** (1323 pp. en 3 vols., verificado) | OCR externo, o la traducción de Tovar 1965 |
| [[oviedo-y-valdes-1851]] | **PDF corrupto** — y además es el volumen equivocado (el material está en t. II y t. IV) | F9 · **la deuda documental mayor** |
| [[rouse-cruxent-1963]] | **0 bytes** | F9 |
| [[fernandes-2020]] | **0 bytes** | recuperable (Nature / PMC) |
| [[ramos-perez-1978]] | **0 bytes** | recuperable (Persée) |

### 🔴 Los 6 archivos de 0 bytes

`Brinton_1871_Arawack_Language_Guiana.pdf` (el `.txt` sí existe) ·
`Fernandes_et_al_2020_Nature_Genetic_History_Caribbean.pdf` ·
`Oviedo_Banhos_1885_Conquista_Venezuela.pdf` (duplicado muerto) ·
`Perea_Alonso_1942_Filologia_Comparada_Lenguas_Arawak_TomoI.pdf` (duplicado muerto) ·
`Ramos_Perez_1978_resenia_Persee.pdf` ·
`Rouse_Cruxent_1963_Venezuelan_Archaeology.pdf`

> [[PLAN_MAESTRO]] §1.1 solo registraba **uno** de estos seis.
> **Higiene inmediata**: borrar los dos duplicados muertos (Oviedo y Baños,
> Perea Alonso), que solo generan confusión; los otros cuatro son huecos reales.

### Fuentes externas (sin archivo local)

Sostienen **27 hechos del corpus** — más que ninguna fuente local salvo Jahn y
Camacho. Ninguna está archivada en el repositorio.

| Fuente | Sostiene | Estado |
|---|---|---|
| [[paz-reverol-2017-2018]] | 9 hechos | leídos íntegros · **archivar** (Dialnet) |
| [[amodio-perez-2006]] | 6 hechos | leído íntegro · **archivar** (guao.org) |
| [[perrin-1992-1995]] | 6 hechos | **de segunda mano**, vía Paz Reverol |
| [[maria-lionza-culto]] | 4 hechos (`retro-abstraido`) | 2 de 5 obras leídas |
| [[keegan-1989]] | 2 hechos | **de segunda mano**, vía resúmenes |
| [[vansina-ong]] | 2 hechos | **de segunda mano**, vía reseñas |

Además, ~20 hechos de [[MOC_ecologia]] se apoyan en **literatura web general**
(Inparques, SVDB, FAO, SciELO, Atlas del Arte Precolombino) sin obra citable con
página. Es el punto más flojo del corpus para F10.

## Cobertura real del lexicón — quién sostiene el "atestiguado"

De las **233 entradas `caquetío-atestiguado`**, medidas por citas en `notas`:

| Fuente | Entradas que la citan |
|---|---|
| [[zavala-reyes-2015]] | **164** |
| [[oliver-1989-cap3]] | 2 |
| [[oviedo-y-valdes-1851]] (vía terceros) | 2 |
| Galeotto Cey (vía Zavala) | 2 |
| [[arcaya-1920]] | 1 |
| [[jahn-1927]] | 1 |
| [[alvarado-1921]] · [[van-buurt-2014]] · [[gatschet-1885]] · Las Casas | **0** |
| **sin ninguna nota** | **82 (26% de las 314 de familia caquetía)** |

> `CLAUDE.md` describe `caquetío-atestiguado` como citable a *"Galeotto Cey,
> Oviedo, Las Casas… Zavala Reyes 2015, Oliver 1989, Jahn 1927"*. En el dato,
> **es Zavala y casi nadie más** — y las tres fuentes ALTA sin minar
> (Alvarado, Van Buurt, Gatschet) tienen penetración **cero**.
>
> Ese es, en una tabla, el argumento entero del eje FIDELIDAD.

## Convención de estas notas

Cada nota de fuente declara en su frontmatter: `capa_texto`, `estado_minado`,
`prioridad`, `tareas` (las F# de [[PLAN_MAESTRO]] §1) y `sostiene`
(hechos del corpus / entradas del lexicón). Cuando una tarea F# se ejecute, **se
actualiza la nota de la fuente**, no un markdown suelto — ese es el punto de V1.

## Recetas de extracción que funcionan

```bash
# Regla general: si `pypdf` devuelve vacío, probar pdftotext ANTES de declarar ilegible
pdftotext -enc UTF-8 archivo.pdf salida.txt          # documento entero
pdftotext -enc UTF-8 -f 116 -l 118 archivo.pdf -     # solo unas páginas, a stdout
```

`-enc UTF-8` no es opcional: sin él, `pdftotext` emite Latin-1 y los acentos
llegan rotos.

## Enlaces

[[PLAN_MAESTRO]] · [[DECISIONES_ABIERTAS]] · [[INDICE]] ·
[[MOC_familia]] · [[MOC_ecologia]] · [[MOC_creencia]] · [[MOC_transmision]] ·
[[MOC_geografia_politica]] · [[MOC_motor]]
