---
tipo: fuente
obra: "Fuentes Históricas sobre Colón y América (Décadas del Nuevo Mundo), vols. 1 y 4"
autor: "Anglería, Pedro Mártir de"
anio: "1892 [c. 1530]"
genero: cronica
local: ["fuentes_caquetios/Angleria_1892_Fuentes_Historicas_Colon_America_vol1.pdf", "fuentes_caquetios/Angleria_1892_Fuentes_Historicas_Colon_America_vol4.pdf"]
paginas: "460 + 492"
capa_texto: si
estado_minado: parcial
prioridad: media
cobertura: "transmisión del saber, vol. 4 (sesión 4) + la costa y su red de intercambio, vol. 1 (2026-09-21, campaña del taíno T5)"
sostiene: {hechos_corpus: 1, entradas_lexicon: 0}
verificado: 2026-09-21
minado: 2026-09-21
aliases: ["Anglería 1892", "Pedro Mártir", "Décadas"]
---

# Anglería 1892 [c. 1530] — *Fuentes históricas sobre Colón y América*

## Qué es

Crónica temprana (compuesta hacia 1530). Dos volúmenes en el repo, 952 páginas
en total. Rendimiento **muy desigual**: el vol. 4 dio el mejor dato puntual de
la sesión 4; el vol. 1 no dio nada relevante.

## Estado técnico (verificado 2026-07-29)

| Archivo | Tamaño | Páginas | Capa de texto |
|---|---|---|---|
| vol. 1 | 20.3 MB | 460 | **sí** (26K car. en 30 pp.) |
| vol. 4 | 21.0 MB | 492 | **sí** (18K car. en 30 pp.) |

`pdftotext -enc UTF-8`. Escaneo antiguo: OCR con erratas, pero utilizable.

## Qué ha dado

**Vol. 4, p. 236 — el areíto antillano** descrito como genealogía cantada: al
entrar en la ceremonia, los danzantes *"colmaban de maravillosas alabanzas al
zeme, y referían cantando las hazañas de los antepasados del cacique"*.

Es **la comparanda atestiguada más fuerte** de [[04_transmision_saber]]: la
función exacta que `ofrenda_ancestros_anochecer` ya asigna a Bana-mana en
`curiana_state.py` ("los niños escuchan los nombres que un día tendrán que
repetir ellos"). → `transmision-018`.

**Vol. 1**: nada relevante en las páginas muestreadas (contenido más
naturalista/zoológico).

## 2026-09-21 — el vol. 1 preguntado por la COSTA (campaña del taíno, T5)

**Qué se preguntó.** ¿Conecta Anglería la costa de Curiana con las Antillas?
¿Describe una red de intercambio, y en qué dirección? Era uno de los tres
huecos que esta nota declaraba («quedan sin preguntar religión, Curiana/Coro,
comercio»). Extraído con `pdftotext -enc UTF-8` (421 KB).

**Medido**: `Curiana/Curian` 12 · `perlas` 38 · `Paria` 23 · `Cauchie` 5 ·
`Española` 84 · `margaritas` 3 — y **`lucay` 0 · `Hispaniol` 0 · `Gigante` 0 ·
`caquet` 0 · `caiquet` 0 · `Coriana` 0**.

**Qué se halló: la red es continental y de eje este-oeste.** El relato del viaje
de Niño y Guerra (1499-1500):

> *«Preguntados los curianenses de dónde conseguían aquel oro, indicaban que lo
> traen de cierta región llamada **Cauchieto**, que distaba **hacia el
> Occidente**, por costa derecha, **seis soles**, esto es, camino de seis
> días… También éstos llevaban perlas al cuello, pero se les proporcionaban de
> **Curiana á cambio de oro**.»*

Oro del oeste por perlas de la costa, en tramos de seis días de navegación
costera. Y las provincias que enumera son **todas de tierra firme**: *«Paria,
Curiana, Cuchibacoa, Cahuyeto, Laturnia, Caubana, Urabain, Zaraboroa,
Veragua»*. Ni una isla antillana en la lista, ni una mención de tráfico hacia
el norte.

⚠️ **Qué nombra «Curiana» aquí sigue en disputa** (#33; ver
[[gonzalez-batista-nombre-de-coro]]) y esta minería **no lo resuelve**. Lo que
la cita sostiene es la **forma** de la red, no la identificación del lugar.

**Qué NO da**: nada de los lucayos, nada de las islas de los Gigantes, ni una
mención de los caquetíos por su nombre. Es el negativo que la parcela T5
necesitaba: el único relato de primera mano de esa costa antes de que los
españoles la reorganizaran no conoce ninguna ruta hacia las Antillas Mayores.
Ver `6-fusion/taino_en_la_esfera_2026-09-21.yaml` §inventario.

## Qué falta

- **Barrido dirigido a los caquetíos**: queda sin preguntar la religión. La
  transmisión se barrió en la sesión 4 y la **costa/comercio** el 2026-09-21
  (arriba).
- Es una de las crónicas que [[PLAN_MAESTRO]] §1.1 marca como "apenas tocadas",
  junto a [[las-casas-1875]] y [[oviedo-y-valdes-1851]].
- El areíto sale de Anglería para las **Antillas**, no para Coro: se usa como
  comparanda estructural, no como dato caquetío.

## Enlaces

[[04_transmision_saber]] · [[las-casas-1875]]
