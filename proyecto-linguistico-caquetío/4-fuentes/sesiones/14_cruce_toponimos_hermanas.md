---
tipo: sesion
fecha: 2026-10-10
quien: "minero del cruce de topónimos (Claude Opus 5.5), rama vault/cruce-toponimos"
propuesta: 6-fusion/cruce_toponimos_hermanas_2026-10-10.yaml
descripcion: "Ninguna hermana glosa un -ana como 'lugar de'; dos lo glosan como gente (el linaje lokono, el gentilicio kalinago), Guayana es un etnónimo caribe, y el cruce general de los topónimos sin lectura no sale del azar más que por cognados que el canon ya tenía."
---

# El cruce de los topónimos con las hermanas, y el `-ana`

> Fuentes: [[las-casas-apologetica]] · [[las-casas-1875]] · [[oviedo-y-valdes-1851]] · [[goeje-1939]] · [[breton-1665]] · [[brett-1880]] · [[brett-1868]] · [[perea-alonso-1942]] · [[roth-1915]] · [[bachiller-morales-1883]] · [[coll-y-toste-1897]] · [[zayas-1931]] · [[gumilla-1791]] · [[neira-ribero-1762]] · [[fabo-1911]] · [[alvarado-1921]] · [[carvajal-1892]] · [[oliver-1989-cap2]] · [[oliver-1989-cap3]] · [[esteves-1989]]
> Propuesta: `6-fusion/cruce_toponimos_hermanas_2026-10-10.yaml` (la emite `6-fusion/scripts/cruzar_toponimos_hermanas.py`) · decisiones: `6-fusion/issues-pendientes/cruce-toponimos-hermanas-2026-10-10.md`
> Contexto: [[toponimia]] · [[morfologia]] §8 · [[03_descomposicion_toponimica]] · [[13_manaure_colombia]]

Miguel (2026-10-10) aprobó un pase que nunca se había hecho: cruzar los
topónimos caquetíos que no tienen lectura con las lenguas hermanas, para
sacar candidatos a palabra o cognado. Y pidió que entrara la terminación
`-ana` —«hasta el día de hoy está solamente en Chamuriana, Jayana, Curiana,
Cujicana»—, mirando cómo la usan los lokonos, con Guayana, y los taínos. Tres
preguntas: qué hace `-ana` en las hermanas con glosa de fuente; si las raíces
de los topónimos sin lectura tienen pareja de significado en las hermanas; y
la lectura de Miguel de *Manare* como culebra. No se descargó nada; no se tocó
`2-lengua/`, `3-mundo/`, `curiana_sim/` ni el lexicón.

## 1. Método

- **`-ana`, a mano y con página.** Se leyeron los pasajes, no los conteos:
  Las Casas (*Apologética* y la *Historia*), Goeje 1939, Breton (1665 y la
  *Grammaire* de 1667), Brett 1868 y 1880, Perea 1942, Bachiller, Coll y
  Toste, Zayas, Gumilla, el manuscrito achagua y Fabo. Lo contable —cuántas
  voces en `-ana` tiene cada lengua del lexicón, cuántas son de lugar, cómo
  escribe cada obra «Guayana» y en cuántas hay algo con aire de etimología—
  lo cuenta el script (regla 1).
- **Regla 6 antes de contar.** Nueve grafías de Guayana (*Guayana, Guiana,
  Guyana, Guyane, Goyana, Wayana, Guajana, Oayana, Ouajana*) en los 38 textos
  que lo nombran; y para `-ana`, también `-anna`, `-aná` y `-āna`.
- **El cruce.** 250 topónimos de una palabra en nivel C o descartado; a cada
  uno se le quitan las terminaciones de lugar declaradas (de `morfemas.yaml`,
  `TODAS_LAS_REGLAS`, Oliver p. 148 y el castellano `-al`, `-ito`, `-s`) y
  algún prefijo declarado (`a-`, `wa-`, `ka-`, `ma-`). La raíz se compara con
  el lexicón caquetío, las voces de Medina, las hermanas (lokono del lexicón y
  de Perea; la lista maestra taína; el kalinago de Goeje y el habla de
  mujeres) y las primas (achagua, wayuu, paraujano). **Un par sólo cuenta si
  la glosa de la voz cae en el mismo campo que el referente del lugar**
  (cerro, agua dulce, río, mar y costa, salina, llano, monte, piedra, arena,
  barro, viento, camino; árbol, ave, pez y marisco, reptil, mamífero,
  insecto, cultivo). 146 de los 250 tienen un referente que filtra.
- **Controles.** Permutación de glosas dentro de cada lengua y de referentes
  entre topónimos (300 réplicas, semilla fija); una voz por familia, porque
  una lengua con muchas entradas sobre una raíz gana pares que no son
  cognados; y un control positivo: el cruce tiene que encontrar lo que el
  canon ya lee.
- **Lo que se probó y se retiró**: casar por una palabra de contenido común
  entre referente y glosa («especie»). Casaba *hacha*, *libro*, *gente*,
  *origen*: el texto del referente trae la discusión de Esteves. Está escrito
  en el script para que nadie lo vuelva a poner.

## 2. Lo que se halló

1. **Ninguna línea glosa `-ana` como 'lugar de'.** #109 se confirma desde
   fuera. Y [[oliver-1989-cap2]] (pp. 148-149), al listar los sufijos
   toponímicos caquetíos (*-bana, -coa, -oa, -kiva, -(e)bo, -wa*), no lo
   incluye.
2. **`-(a)na` de gente, en dos hermanas.** El linaje lokono toma el nombre de
   la antepasada (*Ebeso-ana* de *Ebesō-tu*, *Demaré-na* de *Demare-du*;
   [[brett-1880]] pp. 178-179) y el gentilicio kalinago es isla + `-ri` /
   isla + `-na` (*Ouâitoucoubouli-na* 'los de Dominica'; [[breton-1665]]
   p. 416 y la *Grammaire*). En las dos el `-na` se separa y la base está
   nombrada.
3. **Guayana es un etnónimo, y caribe.** [[goeje-1939]] p. 5: el país toma
   el nombre del pueblo Guayana, junto a la boca del Caroní, de lengua
   caribe. [[bachiller-morales-1883]] p. 277 lo deriva de Guainía (tercera
   mano). La «tierra de muchas aguas» no está en ninguna obra del repo.
4. **Maguana, por primera vez con su primaria.** [[las-casas-apologetica]]
   cap. VII p. 19: *Magua* 'la vega grande' / *Maguana* «cuasi la Vega
   menor». Un `-na` sobre nombre de lugar con valor de 'menor'. Goeje, Coll y
   Toste y Zayas lo copian.
5. **El achagua no tiene `-ana` de lugar.** De las formas en `-ana` del
   manuscrito ninguna es topónimo glosado; la nota «locativo -ana» de la
   transcripción es el `-na` relacional de *numa* 'boca'
   ([[neira-ribero-1762]], pliegos 42 y 98).
6. **'En medio'.** Taíno *nacan* (Cubanacan, [[las-casas-1875]] lib. I cap.
   XLIV) y lokono *annakan* / *a-nnakù-di* ([[perea-alonso-1942]] p. 647;
   [[brett-1868]] p. 485): dos hermanas para el morfema que le falta al «en
   medio del mar» de Paraguaná. La lectura que lo uniría exige perder `-kan`.
7. **El cruce no sale del azar en las hermanas.** Lokono y taíno, en el
   azar. El kalinago sale por encima, y lo empujan la piedra (*šiba* ~
   *kiba*) y el mar (*balaua*, *barana* ~ *para*), que el canon ya tenía. El
   achagua sale muy por encima con todas sus voces y vuelve al azar con una
   por familia. El caquetío y Medina salen por encima: son el control
   positivo (Paraguaná ~ *para*, Cumaraguas ~ *kumarawa*, Cuiba y Tiquiba ~
   *kiba*, Jurijurebo ~ *juri*). Cifras en el YAML (`cruce.azar_por_lengua`).
8. **Cinco candidatos, los cinco débiles**: Capadare ~ lokono *kabadaro*
   'jaguar' (la glosa es «diente de tigre»); Siraba ~ *siba* 'piedra' de las
   tres hermanas (cerro de petroglifos); Cimiro ~ *sima* 'cerro' + *-iro*;
   Amuay ~ kalinago *šauai* 'acantilado, caverna'; Bajarigua ~ *bagua* /
   *balaua* 'mar'. Ninguno pasa de C.
9. **Fauna en `-re`**: ninguna hermana ni prima tiene la misma raíz para el
   mismo animal. Lo más cerca, taíno *múcaru* 'búho' frente a *chaure*, bajo
   el umbral.
10. **Manare y mapanare.** [[alvarado-1921]] p. 200: «CULEBRA-SAPA manare»,
    pequeña serpiente ponzoñosa que se enrosca (Portuguesa), y una avispa
    manare amarilla nombrada por su nido «a modo de manare». Mapanare
    (p. 205) sin etimología; en achagua *mapanarí* es una palma (pliego 80).

## 3. Lo que no se halló

- Un nombre de lugar en `-ana` con glosa en lokono (Brett, Roth, Brinton,
  Perea) o en kalinago (Breton): cero. Los `-ana` de [[roth-1915]] son
  etnónimos y personajes.
- El origen de *mapanare* en ninguna obra del repo.
- El pasaje de Gumilla que Goeje cita (la lengua de los Guayana «apparentée
  au Kalina»): no se localizó.

## 4. Deuda

- Ver en imagen Breton 1665 p. 416 y la hoja G iij de la *Grammaire*, y Las
  Casas, *Apologética*, p. 19: la capa de texto es pista, no cita.
- Oviedo 1851-1855 se barrió sólo por Maguana y sabana; Gilij (maipure) no se
  leyó.
- Las fuentes a pedir están en `meta.fuentes_a_buscar` del YAML (Williams
  1923, Goeje sobre los nombres caribes, Hilhouse, Goeje 1928, Taylor 1977).
