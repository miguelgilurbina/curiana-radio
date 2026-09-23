---
tipo: fuente
obra: "OBIS y GBIF — registros de ocurrencia en la caja marina de Paraguaná (las dos aguas de la era 2)"
autor: "Ocean Biodiversity Information System (IOC-UNESCO) y Global Biodiversity Information Facility (conjuntos de datos de múltiples publicadores)"
anio: "2026"
publicacion: "Consultados vía API (https://api.obis.org/v3/checklist y https://api.gbif.org/v1/occurrence/search) el 2026-09-22. Licencias CC0 o CC-BY según el conjunto de datos"
genero: datos
local: "6-fusion/fauna_mar_caja_obis_gbif_2026-09-22.yaml (generado por 6-fusion/scripts/caja_marina_obis_gbif.py)"
paginas: "— (datos: tres cajas lon/lat, declaradas en el archivo)"
acceso: "Libre. Se regenera con `python 6-fusion/scripts/caja_marina_obis_gbif.py` (usa red)"
capa_texto: datos
estado_minado: minado
cobertura: "FA3 (2026-09-22): checklist de OBIS filtrada a la parcela del mar (peces, tiburones y rayas, tortugas, mamíferos marinos, moluscos, crustáceos, equinodermos, cnidarios, esponjas) y conteo de GBIF para las especies clave"
prioridad: media
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-22
minado: 2026-09-22
aliases: ["OBIS", "GBIF", "caja marina"]
---

# OBIS y GBIF — la caja marina de Paraguaná

> **Qué es.** Una **capa de datos moderna**: registros de ocurrencia
> (colecciones de museo, cruceros de arrastre, ciencia ciudadana) dentro de
> tres cajas —la península con sus dos aguas, el Golfete de Coro y la costa
> oeste—. Un registro dice que alguien vio o colectó la especie allí, hoy o
> en el s. XX. **No es presencia en el s. XV** (regla 3).

## Qué se le preguntó (FA3, 2026-09-22)

¿Qué especies marinas tienen registro en las aguas de GUARANAO y de AMUAY, y
cuáles de las que discute la campaña (tortugas, delfines, ballenas, manatí,
peces de la pesca, moluscos de los conchales) aparecen?

## Qué da

Las cifras las escribe el script en el archivo generado; no se copian aquí
(regla 1). Lo que se lee de ellas:

- La caja es rica en **crustáceos y moluscos** (cruceros de arrastre y
  colecciones) y **pobre en vertebrados grandes**.
- ⚠️ **Cero** registros, en OBIS y en GBIF, de delfines, ballenas, manatí,
  foca monje, pez sierra, mero guasa, tortuga verde y cabezona dentro de la
  caja. Es un cero de **muestreo** (regla 6): Rondón-Médicci 2013 documenta
  nidos de tortuga verde y cabezona en la misma península, y Romero et al.
  1991 un registro de ballena de Bryde en Paraguaná.
- El Golfete de Coro casi no tiene registros: el cero dice lo poco que se ha
  muestreado ahí.

## Qué NO da

- Fechas anteriores al s. XX; abundancias; sonidos; nombres locales.
