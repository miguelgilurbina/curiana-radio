---
tipo: fuente
obra: "Registros de aves de la península de Paraguaná en GBIF (eBird, xeno-canto, iNaturalist y colecciones de museo), consulta del 2026-09-22"
autor: "GBIF.org; Cornell Lab of Ornithology (EOD – eBird Observation Dataset); Xeno-canto Foundation; iNaturalist; MNHN, MCZ, FMNH, UMMZ"
anio: "1896-2026"
publicacion: "API abierta de GBIF, https://api.gbif.org/v1/occurrence/search?classKey=212&decimalLatitude=11.5,12.22&decimalLongitude=-70.32,-69.78 — cada dataset con su DOI y su licencia en 6-fusion/medicion_gbif_aves_paraguana_2026-09-22.yaml (eBird: doi 10.15468/aomfnb, CC BY 4.0; xeno-canto: doi 10.15468/qv0ksn, CC BY-NC 4.0; iNaturalist: doi 10.15468/ab3s5x, CC BY-NC 4.0)"
genero: datos
local: "6-fusion/medicion_gbif_aves_paraguana_2026-09-22.yaml (medición, no descarga)"
paginas: "— (datos)"
acceso: "Libre en línea, sin clave. Reproducible con python 6-fusion/scripts/medir_gbif_aves_paraguana.py"
capa_texto: datos
estado_minado: minado
prioridad: alta
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
cobertura: "clase Aves en la caja 11,50-12,22 N / 70,32-69,78 O: especies, meses, años, datasets, grabaciones de xeno-canto y especímenes de museo (2026-09-22). NO: otras clases (fauna de tierra y mar, parcelas FA1 y FA3)"
verificado: 2026-09-22
minado: 2026-09-22
aliases: ["GBIF aves Paraguaná", "eBird Paraguaná", "gbif-aves-paraguana-2026"]
---

# GBIF — las aves de la península, medidas

> **Qué es.** Una **capa de datos moderna** (regla 3): lo que observadores y
> museos registraron en la península entre 1896 y 2026, casi todo eBird de la
> última década. Dice qué aves **caben** hoy en el cardonal, el cerro, la
> salina y la costa, y en qué meses; no dice qué había en el s. XV. Se abrió el
> 2026-09-22 para la parcela FA2 de la campaña de fauna (encargo de Miguel:
> describir los animales y dar su onomatopeya a los agentes).

## Qué se le preguntó

¿Qué aves hay en Paraguaná y sus aguas, cuáles se van y cuándo (en los tres
períodos del canon de la era 2), y qué grabaciones hechas AQUÍ se pueden
citar como «lo que se oye»?

## Qué da

Las cifras están en `6-fusion/medicion_gbif_aves_paraguana_2026-09-22.yaml`
(regla 1: no se copian aquí). Lo que vale:

- **El inventario moderno**, con el mes de cada registro y un índice por
  período corregido por el esfuerzo de observación (eBird muestrea febrero
  mucho más que junio: un mes vacío no es un ave ausente).
- **Las grabaciones de xeno-canto hechas en la caja** (Santa Ana/Machuruca y
  Montecano), con su ID XC: son la referencia de «lo que se oye» de cada ave.
  No se descargó audio.
- **Los especímenes viejos**: caricare y garza rojiza de 1896 (MNHN, «Paraguaná
  Peninsula»), perdiz de Moruy de 1938 (MCZ), carpintero y canarito de Adícora
  de 1941 (FMNH, MCZ). Lo más antiguo que hay: el umbral de «segura» para
  varias especies del YAML de aves.

## 🔴 La trampa: ausencias publicadas como presencias

El dataset de PANGAEA «Detection histories for eight species of Amazona
parrots in Venezuela during the NeoMaps bird surveys in 2010» (Ferrer-Paris)
publica cada punto de muestreo como una fila `occurrenceStatus: PRESENT` con
`organismQuantity: 0`. Son **no-detecciones**. En la caja salen las ocho
amazonas de Venezuela con el mismo número de filas —incluidas especies de
selva que jamás pisaron un cardonal—, y sin restarlas la cotorra de hombros
amarillos «vive» en Paraguaná por un cero. El script las mide aparte y las
resta. Lección para cualquier consulta de GBIF del proyecto: filtrar
`organismQuantity=0`.

## Qué no da

- **Nada del s. XV.** Las aves perdidas en el s. XX (la cotorra cabeciamarilla,
  la yaguaza de Medina) no están o están poco: la regla de ecologia-037 manda.
- **Las nocturnas y las de sabana, casi nada**: la dara (Burhinus bistriatus)
  da 0 registros en la caja y la lechuza de campanario 0 incluso en una caja
  más ancha. Ceros de observador, no de ave (regla 6).
- **Los 8 registros de la Paleobiology Database** son aves del Mioceno de la
  formación Cantaure: no sirven para nada de esto.

## Deuda

- Repetir la consulta con una caja por ambiente (cerro, salinas, istmo) para
  separar la costa del monte.
- Pedir a xeno-canto (con clave) las descripciones de las grabaciones de la
  caja: la API v3 exige clave, que no se pone en archivos (regla 9).

## Enlaces

`6-fusion/fauna_paraguana_aves_2026-09-22.yaml` · [[monumento-cerro-santa-ana]] · [[laguna-guaranao-parque]] · [[bisbal-1990]] · [[aves-punteros-web-2026]]
