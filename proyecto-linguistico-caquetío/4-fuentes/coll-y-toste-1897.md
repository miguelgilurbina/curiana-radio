---
tipo: fuente
obra: "Prehistoria de Puerto Rico (con el Vocabulario indo-antillano)"
autor: "Coll y Toste, Cayetano"
anio: 1897
genero: etnohistoria-vocabulario
local: ["fuentes_caquetios/CollYToste_1897_Prehistoria_Puerto_Rico.pdf", "fuentes_caquetios/CollYToste_1897_Prehistoria_Puerto_Rico.ocr.txt"]
capa_texto: no
descargado: 2026-09-22
origen_digital: "Internet Archive (prehistoriapepuertoRicocolltoste); el texto es el OCR del propio ítem"
estado_minado: parcial
cobertura: "los dos vocabularios transcritos AUTOMÁTICAMENTE sobre el OCR de archive.org (cap. XII, 721 entradas; cap. X, 304) con autoridad y tipo de apoyo por regla; muestra de 20 cotejada en imagen (M5, 2026-09-23). Sin revisar a mano entrada a entrada"
prioridad: media
verificado: 2026-09-23
aliases: ["Coll y Toste 1897", "Vocabulario indo-antillano"]
minado: 2026-09-23
---

# Coll y Toste 1897 — *Prehistoria de Puerto Rico*

## Qué es

La *Prehistoria de Puerto Rico* con su **Vocabulario indo-antillano**:
probablemente la colección de voces taínas más extensa de su época, y la que más
circula hoy por la web — casi siempre **reeditada y sin aparato**.

El mapa de fuentes de la primera campaña avisaba de eso: la versión que se
encuentra en internet (taino-tribe.org) es la de *Clásicos de Puerto Rico* 1972
y **no cita por entrada de qué cronista sale cada voz**. Lo que se ha descargado
aquí es el **original de 1897**, que es lo que hay que usar.

## Estado técnico ⚠️

| Cosa | Medido |
|---|---|
| PDF | 35,3 MB · sha256 `efbe9dd1…4af2eaa9c` |
| **Capa de texto** | **NO.** `pdftotext` devuelve **273 bytes**. Es un escaneo de imagen |
| Texto disponible | el **OCR del ítem de archive.org**, 489 KB, guardado como `.ocr.txt` |
| Derechos | dominio público (1897) |

🔴 **El `.ocr.txt` es OCR ajeno, no una cita.** Vale para localizar la página y
para medir; una glosa que vaya a decidir una capa se verifica en imagen
(`leer-fuente` §3). Es el mismo estatuto que el OCR de Fabo 1911.

Si en algún momento hace falta OCR propio: `curiana_sim/ocr_fuente.py --lang spa`.

## Qué se le preguntó al descargar (medido, sin minar)

| Consulta | Ocurrencias |
|---|---|
| `indo-antillano` | 101 |
| `Las Casas` | 178 |
| `Oviedo` | 118 |
| `Bachiller` | 38 |
| `Pane` | 34 |
| `Pichardo` | 32 |
| `Colon` | 19 |
| `Brinton` | 5 |
| **`Rafinesque`** | **0** |

Lo que dice el conteo: Coll y Toste **no usa a Rafinesque** —el compilador del
que [[goeje-1939]] avisa que mezcla caribe— y sí usa mucho a los cronistas y a
[[bachiller-morales-1883]]. Eso lo coloca, a priori, en mejor sitio de la cadena
de custodia que las reediciones que circulan con su nombre. **A priori: no está
leído.**

## Qué falta

Todo. Minarlo entrada por entrada, con dos preguntas concretas:

1. ¿cita por entrada de qué cronista sale cada voz? (si no, la lista entera
   entra en la cuarentena c5 del mapa de fuentes);
2. ¿qué dice de las voces que las otras fuentes **sacan** del taíno —`piragua`,
   `maboya`, `bejique`, `huracan`— siendo él puertorriqueño y por tanto vecino
   del eyeri?

## Ver también

[[bachiller-morales-1883]] · [[goeje-1939]] · [[pichardo-1862]] ·
`6-fusion/taino_lista_maestra_2026-09-22.yaml`

## Bitácora 2026-09-23 — tercera campaña, parcela M5

**🔴 Lo primero: no es la edición de 1897.** El escaneo es la **2.ª edición**
(Isabel Cuchí Coll, Bilbao, Editorial Vasco Americana, s. f., «todos los
derechos reservados»), con un apéndice fotográfico del Instituto de Cultura
Puertorriqueña (fundado en 1955); el texto cita obras de 1907. 1897 es el año
del premio. Las páginas que se citan son las de esa edición (el desfase pdf →
impresa **no es constante**: +7 hacia la p. 157, +9 en el cap. XII; y la p. 153
está duplicada en el escaneo). El texto del autor (†1930) es de dominio público;
el prólogo y el apéndice de la edición, no.

**Qué se preguntó.** ¿Cita por entrada el cronista? ¿Qué hace con las voces que
otros sacan del taíno?

**Qué ha dado** (`6-fusion/taino3_coll_y_toste_1897.yaml`, emitido por
`6-fusion/scripts/transcribir_coll_y_toste.py --check`):

- **Sí cita por entrada** en buena parte del cap. XII (el recuento por tipo de
  apoyo lo da el script: documentada / secundaria / afirmada sin fuente /
  conjetura / sacada). Cita además documentos de época —el Repartimiento de
  1514, el Informe de 1582— que el repo no tiene.
- El **cap. X** es un vocabulario al revés (castellano → boriqueño) que compara
  cada voz con el caribe insular (`Ci.`), el caribe continental y el aruaca: es
  la lista de glosas castellanas de una palabra que el cruce necesitaba, y de él
  salen casi todos los conceptos nuevos de la lista maestra.
- Saca del indo-antillano voces que circulan como taínas (`achiote`, `aguacate`,
  `cacao`, `batea`, `coco`, `papagayo`, `tomate`…), diciendo de dónde vienen.

**Qué NO.** Revisión entrada a entrada: la transcripción es automática y la
muestra de 20 dio 2 errores de segmentación y 1 de clasificación. Ver el issue
`vocabularios-antillanos-2-2026-09-22.md`.

## Bitácora: la tradición viva, leída como dato (2026-09-24)

Miguel: «los cronistas no son la fuente principal… la tradición oral prela
por encima». Lo afirmado sin fuente y lo secundario de esta obra (topónimos,
plantas y animales en uso en Puerto Rico y Cuba) se propone como «taíno de
tradición viva», separado de lo conjeturado por el autor. Cruzado nombre
contra nombre con el caquetío vivo, da ocho parejas con el mismo significado,
cinco de ellas de aquí: jagüey, bahareque, guaco, guaraguao, sigua. Y el
vocabulario español-boriqueño del cap. X (el único básico) NO es tradición
oral: es análisis del autor. Detalle: `6-fusion/taino_tradicion_viva_2026-09-24.yaml`.

**✅ Aplicado el 2026-09-24** (tanda de las hermanas, `6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml`): la tradición viva cuenta como dato taíno con su propia etiqueta (T1; entra en los cruces cuando se vuelva a correr T11, después de la corrida base) y la pareja taína está anotada en `jagey`, `bajareke`, `wako`, `warawara` y `kiwa` (T4). `kiba` se fundió en `siba` en la lista maestra (T3).

## 2026-09-24 — campaña cosmovisión marina (comparanda)

**Se halló (visto en imagen):** Coll es quien junta el nombre del dios con el
mar: «Bagua, que en el habla indo-antillana equivale a la mar» y «Yucajú Bagua
Maorocotí equivale a Yuca Blanca, grande y poderosa, como el mar y la montaña»
(pp. 106-107). Es interpretación del s. XIX (el «-hú» 'blanco' lo toma de
Rafinesque), no dato taíno.

COMPARANDA, no dato caquetío. Detalle en `6-fusion/cosmovision_marina_2026-09-24.yaml` §comparanda.
