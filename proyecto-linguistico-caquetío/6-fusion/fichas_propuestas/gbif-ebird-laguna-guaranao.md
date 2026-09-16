---
tipo: fuente
obra: "Ocurrencias de GBIF en el polígono de la laguna de Guaranao (eBird / Cornell Lab of Ornithology; Museo de Ciencias Naturales de la Universidad Simón Bolívar; otros)"
autor: "GBIF (agregador); Cornell Lab of Ornithology, «EOD – eBird Observation Dataset» (2025, doi 10.15468/aomfnb); Caribbean OBIS Node, «Crustáceos del Museo de Ciencias Naturales de la Universidad Simón Bolívar» (doi 10.15468/a2cxch)"
anio: "1988-2024 (consulta 2026-09-16)"
publicacion: "API de GBIF, consulta de ocurrencias en 11,66-11,71 N / −70,23 a −70,16 O, facetas por especie, dataset y año; consulta de Phoenicopterus ruber; consultas de Crocodylus acutus y Caiman crocodilus en la península"
genero: datos
local: ""
paginas: "— (API; 787 registros)"
acceso: "Libre. https://api.gbif.org/v1/occurrence/search?decimalLatitude=11.66,11.71&decimalLongitude=-70.23,-70.16&limit=0&facet=scientificName&facetLimit=60"
capa_texto: web
estado_minado: propuesto
prioridad: media
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-16
propuesto_por: "barrido web 2026-09-16 (6-fusion/barrido_web_cerro_laguna_2026-09-16.yaml, h25 y h19)"
aliases: ["GBIF Guaranao", "eBird Guaranao", "gbif-ebird-laguna-guaranao"]
---

# GBIF / eBird — el inventario medido de la laguna de Guaranao

> **Qué es.** No es una obra: es una **capa de datos moderna** (regla 3),
> de la misma naturaleza que [[osm-kaketiana]]. Lo que la ciencia ciudadana
> con curaduría (eBird, Cornell) y una colección de museo (MCN-USB) han
> subido a GBIF dentro de un polígono de ~5 × 7 km que cubre la laguna, la
> ensenada y el puerto de Guaranao. Es el único inventario con autoría,
> fecha y coordenadas que existe en línea para el sitio del nodo GUARANAO;
> la deuda de [[laguna-guaranao-parque]] pedía «un inventario con
> autoría»: esto es lo que hay.

## Qué se le preguntó

¿Qué animales están registrados en la laguna de Guaranao? ¿Hay
cocodrilianos? ¿Flamencos?

## Qué da

| Dato | Texto (registros) | Etiqueta |
|---|---|---|
| Tamaño y procedencia | 787 registros; 692 de eBird (Cornell), 30 de crustáceos del MCN-USB, el resto de datasets menores; el 76 % de 2020-2022 | atestiguado (moderno) |
| **Aves de la laguna** | garzas: *Egretta thula* 4, *Egretta tricolor* 2, *Ardea alba* 2, *Butorides striata* 2; cormorán *Nannopterum brasilianum* 22; pelícano *Pelecanus occidentalis* 18; águila pescadora *Pandion haliaetus* 16; playeros *Actitis macularius* 9, *Tringa flavipes* 3; cigüeñuela *Himantopus mexicanus* 2; gaviota *Leucophaeus atricilla* 10 | atestiguado (moderno) |
| **El flamenco** | *Phoenicopterus ruber*: **1** registro, mayo de 2024, localidad «Paraguaná--Laguna de Guaranao» (11,675508 −70,20955), eBird | atestiguado (moderno) — ocasional, no «población» |
| Aves de monte y pueblo | *Mimus gilvus* 45, *Columbina passerina* 28, *Melanerpes rubricapillus* 26, *Sicalis flaveola* 22, *Cardinalis phoeniceus* 15, *Leucippus fallax* 11, *Eupsittula pertinax* 19, *Coragyps atratus* 34 (52 especies de aves en total) | atestiguado (moderno) |
| Aves de la costa y el puerto (fuera de la laguna) | *Fregata magnificens* 46, *Thalasseus maximus* 17, *Sula leucogaster* 9 | atestiguado (moderno), pero del polígono, no de la laguna |
| Otros | anfípodos *Hyale pygmaea* 15 y afines (MCN-USB, ensenada); **abeja *Melipona favosa* 11** (la «maba» de Medina); caracoles *Gradiconus* | atestiguado (moderno) |
| **Cocodrilianos** | *Crocodylus acutus* → 0; *Caiman crocodilus* → 0 — y en toda la península (11,5-12,3 N / −70,4 a −69,6 O) también 0 y 0; iNaturalist directo, radio 45 km: 0 y 0 | cero verificado con variantes |

## Lo que vale para el proyecto

- **Mide lo que la prosa afirmaba.** «Refugio de aproximadamente el 70 %
  de las aves caribeñas migratorias» (Wikipedia, venaparaguana) no tiene
  fuente; lo que hay son garzas, cormoranes, pelícanos, playeros y un
  flamenco ocasional. Para el bloque [Tu tierra] del nodo: «garza, pelícano
  y cormorán en la ensenada», no «flamencos».
- **El cero de los cocodrilianos**, medido en dos bases, dos especies y dos
  geometrías, es la segunda pata (con el Libro Rojo,
  `seijas-2015-caiman-libro-rojo`) para degradar *C. acutus* en Guaranao.
- **Melipona favosa en Guaranao** suma una localidad a `maba`
  (`barrido_web_medina_2026-09-09.yaml`).

## Qué no da

- No distingue laguna de ensenada: el polígono incluye el puerto. Las aves
  marinas son de fuera.
- No es un inventario de flora: 3 registros de plantas.
- Es ciencia ciudadana: mide esfuerzo de observación tanto como fauna. Un
  cero aquí es cero de registro.
- Nada precontacto, y además el ecosistema es post-1985
  (`aular-leal-2014-guaranao`).

## Deuda

- Repetir la consulta con el polígono estricto de la laguna (OSM
  `water=lake`, 11,6825 −70,1959) para separar laguna de ensenada.
- Las listas completas de eBird del hotspot, si existe, con fecha.

## Enlaces

[[laguna-guaranao-parque]] · [[osm-kaketiana]] · `6-fusion/sitios_era2.yaml` (§laguna de Guaranao) · `6-fusion/barrido_web_medina_2026-09-09.yaml` (maba) · `6-fusion/barrido_web_cerro_laguna_2026-09-16.yaml`
