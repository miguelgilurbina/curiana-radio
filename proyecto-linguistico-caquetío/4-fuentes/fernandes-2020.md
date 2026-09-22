---
tipo: fuente
obra: "A genetic history of the pre-contact Caribbean"
autor: "Fernandes, Daniel M.; Sirak, Kendra A. et al."
anio: 2020
publicacion: "Nature 590, pp. 103-110 (2021); publicado online el 23-XII-2020. doi:10.1038/s41586-020-03053-2"
genero: genetica
local:
  - "fuentes_caquetios/Fernandes_et_al_2020_Nature_Genetic_History_Caribbean.pdf"
  - "fuentes_caquetios/Fernandes_et_al_2020_biorxiv_preprint_CCBYNCND.pdf"
paginas: 8
capa_texto: si   # vía el fullTextXML de Europe PMC y el suplemento del Reich Lab; el PDF de Nature sigue en 0 bytes
acceso: >-
  Texto completo publicado, libre: Europe PMC / PMC7864882 —
  https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7864882/fullTextXML
  (licencia de Nature: se puede ver, imprimir, copiar y minar para
  investigación académica; NO es CC, no se redistribuye).
  Material suplementario, abierto y completo:
  https://reich.hms.harvard.edu/sites/reich.hms.harvard.edu/files/inline-files/2020_FernandesSirak_Nature_Caribbean_Supplement.pdf
  Preprint de bioRxiv, CC-BY-NC-ND 4.0, SÍ en el repo:
  https://www.biorxiv.org/content/10.1101/2020.06.01.126730v1.full.pdf
  (sha256 eb0b507028851675737d3ff7c45dbb287bcc2c9afefb60130a739131e3d13fd4,
  5.228.503 bytes, descargado el 2026-09-22).
  ⚠️ El PDF de PMC devuelve una página HTML «Preparing to download»: no se
  obtuvo, y el archivo de Nature del repo **sigue en 0 bytes a propósito**.
estado_minado: minado
prioridad: alta
verificado: 2026-09-22
minado: 2026-09-22
aliases: ["Fernandes et al. 2020", "Fernandes et al. 2021", "genética Caribe precontacto"]
---

# Fernandes et al. 2020 — Historia genética del Caribe precontacto

## Lo primero: el archivo seguía vacío y la obra ya no

El PDF de Nature del repo **sigue en 0 bytes**, verificado hoy. Pero el texto
publicado y su material suplementario **sí son accesibles**, y la campaña del
taíno (T8, 2026-09-22) los abrió. La versión anterior de esta nota decía «no
disponible»: era cierto del archivo, no de la obra.

Lo que entra al repo es el **preprint de bioRxiv**, que lleva licencia
CC-BY-NC-ND impresa en cada página. ⚠️ **No es el mismo texto**: es de junio
de 2020, no tiene el yacimiento de Santa Cruz, no tiene el subclado
`*LesserAntilles_Ceramic` y, sobre todo, **no tiene el material suplementario
donde está el hallazgo de esta nota**. Para citar lo que sigue hay que ir a la
versión publicada y a su suplemento, por las vías del frontmatter.

## Qué es

ADN de genoma completo de **174 individuos** de las Bahamas, La Española
(Haití y República Dominicana), Puerto Rico, **Curazao** y **Venezuela**, que
vivieron entre ~3.100 y ~400 años antes del presente, coanalizados con 89
individuos ya publicados y con los 93 de Nägele et al. 2020. 45 fechas de
radiocarbono nuevas.

## ⭐⭐ El hallazgo que cambia esta parcela: Curazao

**Los individuos de Curazao son caquetíos.** El suplemento lo dice sin
rodeos: proceden de **dos poblados caquetíos** —de Savaan (C-0021) y Santa
Cruz (C-0004)— «asociados arqueológicamente con grandes cantidades de
cerámica dabajuroide». Del segundo, los españoles informaron que era el
pueblo de un cacique caquetío. Fechas de contexto: **de Savaan 1160-1500
d.C.**, **Santa Cruz 1443-1522 d.C.** — la ventana que el motor simula.

Y su genoma no es continental puro:

| Modelo (qpAdm) | Fuente antillana | Fuente continental | p |
|---|---|---|---|
| clados mayores | `*Caribbean_Ceramic` 68,0 ± 5,1 % | `*Venezuela_Ceramic` 32,0 ± 5,1 % | 0,298 |
| con competencia de modelos | `*LesserAntilles_Ceramic` **74,5 ± 3,7 %** | `*Venezuela_Ceramic` 25,5 ± 3,7 % | 0,362 |

El componente continental lo asocian a la llegada de la cerámica dabajuroide
hacia 500 d.C. (`*Venezuela_Ceramic` es el yacimiento de Las Locas, valle de
Quíbor, ~2.350 a.p.). El antillano, a algo posterior:

> «major gene flow from the Antilles that affected Curaçao in the centuries
> after the arrival of Dabajuroid pottery»
> — Supplementary Information, SI2 «Curaçao»

Y dejan la tarea escrita: identificar el correlato arqueológico de esos
eventos es, en sus palabras, un tema importante para la investigación futura.

## 🔴 Y lo que el mismo hallazgo cierra

**La ancestría es de las Antillas MENORES, no de las Mayores.** El texto
principal es explícito: el reparto de ancestría se da entre los individuos de
Curazao y los de las Antillas Menores *«but not the Greater Antilles»*, y lo
usa como apoyo de una trayectoria de sur a norte en peldaños. Las dos
poblaciones de referencia del subclado son **Anse à la Gourde** (Guadalupe) y
**Lavoutte** (Santa Lucía).

⚠️ **Con un matiz que hay que degradar en duda**: en el modelo de grafo
(qpGraph, SI12), la mejor fuente de mezcla para `*Curacao_Ceramic` es «una
población entre las poblaciones cerámicas de las Antillas Mayores y las
Menores». El texto principal dice «Menores y no Mayores»; el grafo dice
«entre las dos». Las dos lecturas están en la misma obra.

## La otra dirección: nada

- **Ninguna migración continental posterior entró en las Antillas.** El
  resumen lo dice del cambio cultural: no lo movió gente genéticamente
  distinta del continente, sino interacciones dentro de un mundo caribeño
  interconectado.
- Probaron expresamente la hipótesis de una **migración caribe desde el
  occidente de Venezuela hacia 1.150 años atrás** (Ross et al., morfología
  craneofacial) y no encontraron ancestría nueva, con una potencia declarada
  de detección de tan poco como **~2-8 %** usando `Venezuela_Ceramic`,
  `LesserAntilles_Ceramic` o los arara actuales como sustitutos. ⚠️ No
  descartan migración de «un grupo continental no muestreado» más parecido a
  la gente cerámica caribeña que esos sustitutos.
- **Ninguna asociación entre los subclados genéticos y las tipologías
  cerámicas** (saladoide, ostionoide, meillacoide, chicoide). Los estilos
  cambian sin que cambie la gente.

## Qué NO da (y hay que decirlo, porque tienta)

1. **No hay fecha para la mezcla de Curazao.** SI14 lo declara: no pudieron
   obtener estimaciones viables para los individuos de Curazao (sí para
   Haití: 16,5 ± 3,3 generaciones). «En los siglos posteriores a la llegada
   del dabajuroide» es la lectura de los autores, no una medición. El evento
   cabe en cualquier punto entre c. 500 y c. 1300 d.C.
2. **No hay número de individuos de Curazao en el texto.** Está en
   Supplementary Data 1, un `.xlsx` que PMC no sirve a una descarga
   automática. El preprint, antes de que se añadiera Santa Cruz, listaba 2 de
   de Savaan. No se escribe un total a mano (regla 1).
3. **`*Curacao_Ceramic` es un clado marginal**: de Savaan y Santa Cruz forman
   clado entre sí sólo «marginally» (p = 0,011).
4. **Ni una palabra de lengua.** Ancestría no es lengua, y en esta obra ni
   siquiera se insinúa.
5. **No hay ADN antiguo de Paraguaná ni de Falcón costero.** `Venezuela_Ceramic`
   es Quíbor, tierra adentro, y del comienzo de la Edad Cerámica.

## 🔴 Una discrepancia de fechas que no se promedia

[[haviser-1990]] da para los dos esqueletos de de Savaan exhumados en 1980 un
C-14 sobre hueso de **1.500 ± 200 a.p.** Esta obra da para el yacimiento un
contexto de **1160-1500 d.C.** (~790-450 a.p.). No son la misma fecha ni de
lejos. O los individuos secuenciados no son los de 1980, o hay dos fechados
del mismo sitio sin conciliar. Quien quiera afinar la época del hallazgo tiene
que resolverlo — probablemente con Haviser 1987, que es la fuente de las
fechas de contexto y no está en abierto.

## Qué corrige de lo que el repo tenía

- **Cierra a medias la pregunta abierta de [[schroeder-2018]]**: si el estrato
  «taíno» de Paraguaná parecía préstamo y no población, porque los linajes
  maternos arubeños MODERNOS no son los del taíno antiguo. Con ADN antiguo de
  Curazao hay población de origen antillano en las islas, y mucha — pero de
  las Antillas Menores. Y Curazao no es Paraguaná.
- ⚠️ **No es corroboración independiente de [[martinez-cruzado-2003]]**: esta
  obra CITA ese mismo artículo (Toro-Labrador, Wever & Martínez-Cruzado 2003)
  como apoyo de la hipótesis de que los arahuacos se partieron hacia el
  Orinoco y hacia la costa occidental venezolana. Misma fuente, mismo uso
  (skill §8).
- Corrige el `gen-03` de `6-fusion/taino_en_la_esfera_2026-09-21.yaml`, que la
  daba por inaccesible.

## Enlaces

[[schroeder-2018]] · [[martinez-cruzado-2003]] · [[nagele-2020]] ·
[[dijkhoff-1997]] · [[haviser-1990]] · [[rouse-cruxent-1963]] ·
[[esfera-de-interaccion]]
