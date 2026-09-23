---
tipo: fuente
obra: "GBIF — ocurrencias de fauna de tierra en el polígono de la península de Paraguaná y el istmo de los Médanos (consulta por API)"
autor: "GBIF.org (Global Biodiversity Information Facility) y los conjuntos de datos que publica"
anio: 2026
publicacion: "API pública https://api.gbif.org/v1/occurrence/search con facetas, consultada el 2026-09-22; sin descarga (una descarga pide cuenta), así que sin DOI de descarga"
genero: datos
local: "6-fusion/gbif_fauna_tierra_paraguana_2026-09-22.yaml (generado por 6-fusion/scripts/gbif_fauna_tierra_paraguana.py)"
paginas: "— (datos)"
capa_texto: web
acceso: "Libre; cada conjunto de datos tiene su licencia (CC0, CC BY o CC BY-NC), listada en el archivo generado"
estado_minado: minado
cobertura: "clases de tierra (mamíferos, escamados, tortugas, anfibios, arácnidos, ciempiés, insectos y caracoles de familias terrestres) en el polígono; campaña FA1, 2026-09-22"
prioridad: media
verificado: 2026-09-22
minado: 2026-09-22
aliases: ["GBIF Paraguaná", "GBIF 2026", "gbif-paraguana"]
---

# GBIF — la fauna de tierra de Paraguaná que hoy se registra

## Qué es

No es una obra: es una **consulta** a la base mundial de ocurrencias. Casi todo
lo que devuelve es ciencia ciudadana reciente (iNaturalist) y colecciones del
s. XX-XXI: es **censo moderno** (regla 3), útil para decir qué animal vive hoy
en la península, nunca para decir qué había en el s. XV. Y un **cero mide GBIF**
(regla 6): los animales nocturnos, chicos o poco fotografiados faltan.

## Cómo se cita

Las cifras viven en `6-fusion/gbif_fauna_tierra_paraguana_2026-09-22.yaml`,
generado por `6-fusion/scripts/gbif_fauna_tierra_paraguana.py` (regla 1): el
total del polígono, el reparto por clase, las especies de tierra con autoría y
número de ocurrencias, y **la lista de conjuntos de datos con su título, su
publicador y su licencia** — que es como GBIF pide que se cite un dato cuando no
hay DOI de descarga. El polígono (WKT) está en el mismo archivo.

## Qué dio

Especies que el repo no tenía y que la campaña usó: la tarántula azul, el ratón
mochilero de Paraguaná, el tuqueque de Monte Cano, las marmosas, el murciélago
cardonero y los de cueva, *Anolis onca*, los corredores *Cnemidophorus*, la
culebra *Thamnodynastes paraguanae*, el sapito lipón, *Melipona favosa*, el
caracol *Tudora paraguanensis*; y las introducidas de hoy (rata, ratón, viuda
marrón).

## Bitácora

- **2026-09-22** (FA1): primera consulta. Rehacerla es correr el script.
