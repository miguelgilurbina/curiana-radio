# Mapa ecología ↔ lexicón

*Cross-check exhaustivo entre los hechos del ensayo `02_ecologia_golfete.md` /
`ecologia.yaml` y las palabras de `curiana_sim/curiana_lexicon.py`.*
*Objetivo: para cada especie o rasgo del paisaje, decir qué palabra lo nombra, de qué
lengua es la forma, y si es **hueco léxico**. Detectar falsos amigos.*
*(v2 — incorpora la capa biológica: mamíferos, reptiles, fauna marina; y las locaciones
`conuco` y `taller_canoas`.)*

## Cómo leer la columna «estado»

- **caquetío** — forma marcada `caquetío-atestiguado` o `caquetío-reconstruido` (la lengua
  propia de la simulación).
- **hermana** — la palabra existe en el lexicón activo pero es forma wayunaiki / lokono /
  taíno / kalinago (para el *scoring* cuenta como tan ajena como el español; ver CLAUDE.md).
  Sirve de andamio, no de forma caquetía consolidada.
- **HUECO** — no hay palabra para el concepto: candidato a neologismo emergente.
- ⚠️ **falso amigo** — la forma existe pero significa otra cosa.

---

## 1. Agua, geografía, clima

| Concepto | Palabra | Fuente-forma | Estado |
|---|---|---|---|
| mar / aguas grandes | habo · baraha · para · barana | lokono/garífuna + hermanas | caquetío (habo) |
| agua (dulce, bebible) | duna · oniabo · wüin · tuna | garífuna/lokono | caquetío (duna) — ⚠️ **falso amigo: `duna` = AGUA, no médano** |
| lluvia / agua del cielo | kaya | lokono (juya-cogn) | caquetío-reconstr. |
| sol / luna | kali·cazi / kasha·cati | lokono + caquetío atest. | caquetío |
| viento (genérico) | joutai | wayunaiki | caquetío-reconstr. |
| brisa del Golfete | habobrisa | lokono/garífuna | caquetío (compuesto) |
| tormenta / marejada | kayawara / haborü | lokono | caquetío (compuestos) |
| sequía | madunaka | proto-arawakan | caquetío (ma+duna) |
| **alisio (viento NE estructurante)** | — | — | **HUECO** (solo joutai/habobrisa genéricos) |
| río perenne | bara · paro · güique · tutu | caquetío atest. + hermana | caquetío |
| arroyo / quebrada | luwopu | lokono | **hermana**; y **HUECO** para lo *efímero* |
| jagüey / charca | laa · buko · jaguey(v.) | wayuu + caquetío atest. | caquetío (buko); laa hermana |
| laguna | tarica · lamuuna | caquetío atest. + wayuu | caquetío (tarica) |
| pantano / ciénaga | pariri | caquetío atest. | caquetío |
| costa / orilla del mar | cari | caquetío atest. | caquetío |
| arena / arenal | rao | caquetío atest. | caquetío |
| **duna / médano (vivo o fijo)** | — | — | **HUECO** (rasgo definitorio del territorio) |
| **istmo / lengua de arena** | — | — | **HUECO** |
| **marea** | — | — | **HUECO** (real: semidiurna ~50 cm) |
| cerro / sierra | sima · quidi · ori · namüna | lokono/topónimo + caquetío | caquetío |
| sabana / llano | sallaban · sallaba | lokono/proto-arawak | **hermana** |
| isla | kairi · cai | lokono/kalinago | **hermana** |
| cayo / islote | cayo | taíno | **hermana** |
| desembocadura | erne | lokono | **hermana** |

## 2. Salinas

| Concepto | Palabra | Fuente-forma | Estado |
|---|---|---|---|
| sal | biro | caquetío atest. | caquetío |
| salina / lago salado | borojo | caquetío atest. | caquetío |
| **costra de sal (evaporítica)** | — | — | **HUECO** |
| **agua salobre / salitre** | — | — | **HUECO** |

## 3. Agricultura y el conuco

| Concepto | Palabra | Fuente-forma | Estado |
|---|---|---|---|
| conuco / parcela | conuco · gua · kunuku · kabojan · duraboa · tebe | caquetío atest. + taíno | caquetío (repertorio rico) |
| represa / acequia / riego | buco · buko | caquetío atest. | caquetío — **la locación mejor anclada** |
| estancar / represar | jaguey (v.) | caquetío atest. | caquetío |
| regar / irrigar | jacuque (v.) | caquetío atest. | caquetío |
| sembrar / siembra | kono (v.) · tabri · pünajüt | caquetío + wayuu | caquetío |
| yuca brava | kasiripa · yuka · yuca | lokono + taíno | caquetío (kasiripa) |
| maíz | marisi · maisi · mariti | lokono + taíno | caquetío (marisi) |
| batata | batata | taíno | **hermana** |
| auyama / calabaza | auyama · wüirü | caquetío atest. + wayuu | caquetío |
| caraota / frijol | caraota | caquetío | caquetío |
| casabe | cazabi | taíno | **hermana** |
| **tala y quema (la técnica)** | — | — | **HUECO** (acto central del ciclo agrícola) |
| **ceniza como abono** | — | — | **HUECO** |

## 4. Manglar y flora xerófila

| Concepto | Palabra | Fuente-forma | Estado |
|---|---|---|---|
| manglar (genérico) | mankaba | lokono/proto-arawak | caquetío-reconstr. |
| **mangle rojo / negro / blanco / botoncillo** | — | — | **HUECO** (4 spp. reales, 1 palabra genérica) |
| **raíz-zanco del mangle** | — | — | **HUECO** |
| **tanino / corteza curtiente** | — | — | **HUECO** (uso central: teñir redes) |
| cardón (planta / fruto) | coro · kadushi / caduchi | caquetío atest. | caquetío |
| dividivi | watapana | caquetío atest. | caquetío |
| cocuiza / agave | kukuisa · karowa | caquetío/topónimo + wayuu | caquetío (kukuisa) |
| cují / trupillo | adoptivo | wayunaiki | **hermana** |
| sábila / áloe | rülipi | wayunaiki | **hermana** |
| palma | marawa | lokono/garífuna | caquetío-reconstr. |
| árbol / madera (genérico) | kuru · balli · adda | lokono | caquetío (kuru) |
| leña | asema | wayunaiki | **hermana** |
| **yabo, espinito, guayacán, tuna, guamacho** | — | — | **HUECO** (flora dominante del monte espinoso) |

## 5. Fauna terrestre — mamíferos

> Contexto biológico: la fauna terrestre es **escasa** por el clima desértico
> (`ecologia-033`). La caza es complemento, no despensa.

| Concepto | Palabra | Fuente-forma | Estado |
|---|---|---|---|
| venado caramerudo (*Odocoileus*) | tara | caquetío atest. | caquetío — **hoy ausente de gran parte de Falcón: la palabra prueba que estuvo** |
| armadillo / cachicamo | cachicamo | caquetío atest. | caquetío |
| bachaco / hormiga | koke | caquetío atest. | caquetío |
| **zorro común (*Cerdocyon thous*)** | walirü (wayuu) | wayunaiki | **hermana** → hueco caquetío |
| **oso melero (*Tamandua*)** | — | — | **HUECO** (comedor de koke) |
| **conejo sabanero (*Sylvilagus*)** | — | — | **HUECO** (presa menor frecuente) |
| **mapurite (*Conepatus*)** | — | — | **HUECO** |
| **rabipelado (*Didelphis*)** | jawade (lokono) | lokono | **hermana** → hueco caquetío |
| tapir / danta | kama · firobero | caquetío atest. | caquetío — ⚠️ **NO es fauna local** (tierra firme húmeda) |
| jaguar | kabadaro | wayunaiki | **hermana** — ⚠️ tampoco es vecino del istmo |

## 6. Fauna terrestre — reptiles (los dueños del desierto)

| Concepto | Palabra | Fuente-forma | Estado |
|---|---|---|---|
| iguana | iwana · iguana · higuana | taíno/lokono | caquetío (iwana) — **proteína real y accesible** |
| gecko / tuqueque | tuqueque | caquetío atest. | caquetío |
| caimán | kaiwa · kaiman | lokono/proto-arawak | caquetío (kaiwa) |
| tortuga (genérica) | hikoteya · hikolhi · wagulo | lokono/garífuna | caquetío (hikoteya) |
| culebra / boa | wüi · sarulu | wayunaiki | **hermana** |
| **cascabel (*Crotalus durissus*)** | — | — | **HUECO** — ⚠️ *la amenaza mejor fundada del paisaje* |
| **coral, mapanare, tigra cazadora** | — | — | **HUECO** (serpientes venenosas concretas) |
| **mato real, lagartijo** | — | — | **HUECO** |

## 7. Fauna marina — la despensa verdadera

| Concepto | Palabra | Fuente-forma | Estado |
|---|---|---|---|
| pez (genérico) | arima · itime · pira | lokono + hermanas | caquetío (arima) |
| **cardumen / banco de peces** | — | — | **HUECO** (el objeto del oficio de pesca) |
| **cunaro / guaranaro / bagre (especies)** | — | — | **HUECO** (nombres de agente, no de especie) |
| **pargo, corvina, mero, róbalo, lisa, jurel, sábalo, corocoro** | — | — | **HUECO** (la ictiofauna real, sin nombres) |
| tiburón | kanawari | lokono/proto-arawak | caquetío-reconstr. |
| manatí | manatü · manati | taíno/lokono | caquetío (manatü) |
| cangrejo | ukura | lokono/garífuna | caquetío-reconstr. |
| botuto / caracol reina | cobo | taíno | **hermana** |
| perla | tüma | lokono/proto-arawak | caquetío-reconstr. |
| **ostra perlífera (el molusco)** | — | — | **HUECO** (la perla sí tiene nombre; el animal no) |
| **delfín** | — | — | **HUECO** |
| **tortugas marinas (verde, carey, cardón, cabezón)** | — | — | **HUECO** (4 spp. bajo el genérico *hikoteya*) |

## 8. Aves

| Concepto | Palabra | Fuente-forma | Estado |
|---|---|---|---|
| flamenco / ibis rojo | tokoko · chogogo | lokono + caquetío atest. | caquetío |
| gavilán | chiriguare | caquetío atest. | caquetío |
| pavón / pauji | pauji | caquetío atest. | caquetío |
| sinsonte | chuchubi | caquetío atest. | caquetío |
| zamuro / buitre | warawara · samulu | caquetío atest. + wayuu | caquetío (warawara) |
| ave (genérico) | foro · kodibio · wuchii | wayunaiki/lokono | **hermana** |
| colibrí, turpial, cardenal, búho… | bimiti, ului, iisho, monkulonseerü… | wayunaiki | **hermana** (repertorio amplio, no caquetío) |
| **corocora roja, garzas, playeros migratorios** | — | — | **HUECO** (avifauna del humedal) |
| **boba (*Sula*) y guano** | — | — | **HUECO** (recurso insular; señal de pesca) |

## 9. Navegación, pesca y oficios

| Concepto | Palabra | Fuente-forma | Estado |
|---|---|---|---|
| canoa | kanua · canoa · piragua · kannoa | lokono + taíno | caquetío (kanua/canoa) |
| remo | shukua | lokono/garífuna | caquetío-reconstr. |
| red de pesca | atara | lokono/proto-arawak | caquetío-reconstr. |
| arco / flecha | buraka / sipara | lokono | caquetío-reconstr. |
| cuerda / fibra | kürara | lokono/proto-arawak | caquetío-reconstr. |
| vasija / totuma | paugis · ture · aliita | lokono + caquetío atest. | caquetío |
| **madera de canoa foránea** (cedro/caoba/ceiba) | — (solo *kuru* genérico) | — | **HUECO** — el material más valioso del taller |
| **arcilla / engobe / desgrasante** | — | — | **HUECO** (cadena técnica dabajuroide) |

---

## Síntesis: los huecos léxicos por presión

Ordenados por cuán a diario los vive la comunidad sin nombrarlos:

1. **duna / médano** — el rasgo que define el territorio. (⚠️ `duna` ya significa *agua*.)
2. **cardumen / banco de peces** — el objeto del oficio de pesca.
3. **alisio** — el viento estructurante, distinto del genérico *joutai*.
4. **las especies de pez** (cunaro, guaranaro, bagre, pargo, mero, róbalo…) — el mar es la
   despensa y sus habitantes casi no tienen nombre propio caquetío.
5. **marea** — ciclo diario real del Golfete (~50 cm), sin lexema.
6. **cascabel y serpientes venenosas** — la amenaza mejor fundada del paisaje, muda.
7. **madera de canoa foránea** — el bien escaso del taller de Dara-ko.
8. **costra de sal / agua salobre** — el producto y el estado intermedio del salinar.
9. **tala y quema / ceniza** — el acto central del ciclo del conuco.
10. **quebrada / arroyo efímero** — el cauce que solo corre tras la lluvia (BSh).
11. **istmo / lengua de arena** — la geografía que une Paraguaná al continente.
12. **mangle rojo vs. negro, raíz-zanco, tanino** — el detalle del único bosque.
13. **mamíferos menores** (oso melero, conejo, mapurite) y **avifauna del humedal**.
14. **delfín, tortugas marinas por especie, ostra perlífera**.

### Un patrón que salta a la vista

Los huecos **no están repartidos al azar**. El lexicón caquetío atestiguado es fuerte en
**lo que se comercia y lo que significa** (biro, borojo, tüma, watapana, kadushi, tara,
chiriguare) y débil en **lo que simplemente se ve y se trabaja a diario** (los peces por
especie, el médano, el cardumen, la marea, la serpiente). Esto es coherente con cómo se
formó el corpus —lo que los cronistas anotaron fue lo que les interesaba: mercancías,
títulos, topónimos— y explica por qué la simulación tiene tanto espacio para crear: **la
lengua que sobrevivió es la del comercio y el poder; la lengua del oficio cotidiano es
justamente la que se perdió, y la que los agentes pueden volver a inventar.**

> **Nota de método:** no se propone rellenar estos huecos a mano. Su valor para el
> experimento es que **emerjan** en boca de un agente cuando la escena lo empuje, usando la
> morfología viva (locativos `-ana/-bana`, agentivos `-ko/-sha`, composición con raíces
> existentes como `habo`, `rao`, `biro`, `arima`, `joutai`, `kuru`). Esta tabla existe para
> que el diseño sepa *dónde* está la presión, no para resolverla por adelantado.
