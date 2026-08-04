---
tipo: fuente
obra: "Caquetío Indians on Curaçao during colonial times and Caquetío words in the Papiamentu Language — Some names of Animals and Plants in Papiamentu"
autor: "van Buurt, Gerard"
anio: 2014
publicacion: "Edición propia, Curaçao (ISBN 978-99904-2-348-8); base en van Buurt & Joubert, *Stemmen uit het Verleden*, 1997"
genero: glosario-etnohistoria
local: "VanBuurt_2014_CaquetioWords_Papiamentu.txt"
paginas: 48
capa_texto: si
estado_minado: minado
cobertura: "§6 88/88 entradas, §11 29/29, §7 180 topónimos, §8-10 15 etimologías, 19 morfemas; propuesta en curiana_sim/lexicon_van_buurt.py, sin tocar el lexicón activo"
prioridad: alta
tareas: [F1]
sostiene: {hechos_corpus: 1, entradas_lexicon: 0, citas_recuperadas_82: 8, reclasificadas_abajo_82: 3}
propone: {s6_A: 29, s6_B: 53, s6_C: 3, s11_C: 29, toponimos: 180, morfemas: 19}
verificado: 2026-08-03
aliases: ["Van Buurt 2014", "Caquetío words in Papiamentu"]
---

# Van Buurt 2014 — Palabras caquetías en el papiamento

## Qué es

**El léxico caquetío superviviente**, tal como sobrevive dentro del papiamento
de Curazao, Aruba y Bonaire — y, metodológicamente, **la fuente más afín al
espíritu de este proyecto**: van Buurt separa explícitamente lo que es
"probablemente caquetío" de lo que tiene "vínculos menos ciertos", y explica por
qué esa distinción es necesaria.

> Su §12 contiene una autocrítica que este proyecto haría bien en leer dos
> veces: la edición de 1997 presentaba la evidencia **sin decidir** qué palabra
> era caquetía y cuál llegó vía español, taíno o guajiro, para dejar que el
> lector concluyera. *"This has turned out to be a major mistake, leaving room
> for totally erroneous interpretations."* — La ambigüedad no marcada no es
> neutral: se lee como afirmación.

Y de su propia §6 advierte: *"the following listing has a subjective element"*.
Esa advertencia viaja en el campo `notas` de **cada** entrada importada.

## Estado técnico (verificado 2026-08-03)

| Dato | Valor |
|---|---|
| Formato | **.txt de 92 KB**, extraído del PDF de tiboko.com — vive en la **raíz del proyecto**, no en `fuentes_caquetios/` |
| Capa de texto | sí, limpia; conserva acentos y diacríticos |
| Estructura | 12 secciones numeradas, localizables por `grep -nE "^\s*[0-9]{1,2}\. [A-Z]"` |
| Minador | `curiana_sim/minar_van_buurt.py` (patrón de `minar_zavala_glosario.py`) |
| Propuesta | `curiana_sim/lexicon_van_buurt.py` — **no se importa en `curiana_lexicon.py`** |

📌 **Nota de orden**: sigue siendo la única fuente del corpus que no está en
`fuentes_caquetios/`. El minador la busca en la raíz; si se mueve, hay que
actualizar `TXT_PATH`.

## Qué ha dado (minado 2026-08-03, tarea F6)

| Sección | Contenido | Extraído |
|---|---|---|
| 2-4 | Etnohistoria: llegada del hombre, contactos insulares, **caquetíos en Curazao colonial** | leído; propuesta abajo para [[mapa-geografia-politica]] |
| 5 | Cómo entran las palabras caquetías al papiamento; análisis fonológico | 19 morfemas |
| **6** | **Palabras probablemente caquetías** | **88 entradas** (85 + 3 remisiones cruzadas) |
| **7** | **Topónimos probablemente caquetíos** | **180** (A=119, C=20, B=41) |
| 8-10 | Etimología comentada de topónimos | 15 |
| **11** | **Palabras con vínculo menos cierto** | **29 entradas** |

### La escala epistémica viene regalada — y se respeta

`lexicon_van_buurt.py` mantiene **dos diccionarios separados**, `VAN_BUURT_S6` y
`VAN_BUURT_S11`. Fusionarlos sería repetir exactamente el error que el autor
confiesa haber cometido en 1997.

Dentro de la §6 se aplicó además la escala del
[[02_protocolo_habla_paraguanera]] §5:

| Nivel | N | Criterio |
|---|---|---|
| **A — atestiguado** | **29** | §6 + atestación colonial/decimonónica, coincidencia con [[gatschet-1885]] o respaldo toponímico de §7 |
| **B — fuerte** | **53** | §6 sin respaldo externo adicional |
| **C — plausible** (dentro de §6) | **3** | `wayaká`, `wimpiri`, `shirishiri`: **el autor desmonta la atribución en el cuerpo de su propia entrada**. La sección dice una cosa y el argumento otra; manda el argumento |
| **C — plausible** (§11) | **29** | tier degradado por el propio autor |

Las 29 de nivel A: `bushi, catashi, chuchubi, dabaruida, dividivi, dori, fofoti,
hubada, huliba, ishiri, kadushi, kamari, karawara, koubati, mahoso, makurá,
mashibari, palúli, patalewa, sawaka, shimarucu, tarabara, teishi, waltaca,
warashi, warawara, warwacowa, watapana, yuana`.

> ⚠ **Nada de esto entra a `VOCABULARIO_BASE` por este camino.** Regla de oro 1
> del protocolo: hace falta decisión humana explícita. El minador **no toca**
> `curiana_lexicon.py`.

### Política D7 aplicada desde el primer registro

Cada entrada lleva `glosa_fuente` (van Buurt verbatim, con sección) e
`identificacion_moderna` (el taxón) en **campos separados**, más la marca de
isla (A/B/C) como dato de distribución. Ninguna gana. La discrepancia más
jugosa la produjo el cruce con Gatschet (ver abajo): `warawara` es
*Cathartes curasoica* (zamuro) para Gatschet y *Caracara cheriway* para van
Buurt — y **el lexicón trae hoy la lectura de Gatschet sin saber que la trae**.

### Morfología: 19 morfemas, y uno confirma REGLAS_ZAVALA

`MORFEMAS_VAN_BUURT` se transcribió **a mano** (van en prosa argumentada, no en
lista). Los de mayor valor:

- **`-ima` / `nima` 'húmedo'** (Cruz Esteves 1989, vía el topónimo Onima) —
  **confirmación independiente** del `-ima` de `REGLAS_ZAVALA` ('humedad,
  quebrada'). Dos fuentes distintas, mismo afijo, misma glosa.
- **`-bi` 'pequeño'** (gobí, gogorobí, kokorobí, lobi, makambí) — **segundo
  diminutivo documentado**, junto al `-iro` de Zavala.
- **`-ure` / `-huri` / `-uri` 'raíz'**, **`-apana` 'hoja'**, **`bara`/`bari`
  'árbol'**, **`-utu` 'pez'**, **`wa-` pluralidad/posesión**, **`ka-`
  localizador**, **`siba` 'piedra'**, **`bala` 'mar'**, **`hudi` 'viento'**,
  **`cari` 'costa'**, **`abo` 'lugar'**, **`tabo` 'confluencia'**,
  **`waka` 'subterráneo'**, **`-ato` parentesco**, **`-baca` 'matorral'**
  (vía [[alvarado-1921]]).
- ⚠ **`-bana` discrepa**: el lexicón lo usa como locativo 'orilla/borde'; van
  Buurt documenta 'ancho, llano' (Hudishibana = 'llano ventoso') y 'cubierto'
  (wakaubana, vía Oliver). **Resolver.**

### Cruce con [[gatschet-1885]] — 16 coincidencias verificadas

Dos recolecciones **independientes** separadas por 130 años; ninguna cita a la
otra. El minador genera candidatos (`--gatschet-candidatos`) y la tabla final se
curó **leyendo el texto de Gatschet**, porque el cruce automático miente.

| van Buurt | Gatschet 1885 (Pinart 1882) | Tipo | Nota |
|---|---|---|---|
| `dividivi` | dividivi | exacta | mismo taxón |
| `watapana` | watapana | exacta | *Sapindus coriaria* = *Caesalpinia coriaria* |
| `warawara` | warawara | exacta | ⚠ taxón distinto (ver D7 arriba) |
| `makurá` | makura | exacta | mismo taxón (*Abrus precatorius*) |
| `palúli` | paluli | exacta | mejillón en las dos |
| `dori` | dori | exacta | *Rana* |
| `hubada` | hubada | exacta | árbol arubano |
| `kadushi` | kaduski | variante | ⚠ el taxón de Gatschet es el del `kadushi pushi` |
| `chuchubi` | shushubi | variante | sinsonte en las dos |
| `shimarucu` | shimaruko | variante | *M. glabra* ~ *M. emarginata* |
| `waltaca` | waltaka | variante | lagarto |
| `dabaruida` | dabaraida | variante | **el propio van Buurt cita la coincidencia** |
| `tarabara` | tarabada | variante (probable) | d/r alterna; no confundir con el monte Tarabana |
| `koubati` | Kausheati | variante | coincidencia a nivel de topónimo |
| **`purunchi`** | **puruntsi** | variante | **está en §11**, no en §6 |
| **`kinikini`** | **kinikini** | exacta | **está en §11**, no en §6 |

Las dos últimas son el hallazgo incómodo del cruce: **coinciden en dos fuentes
independientes y aun así van Buurt las mantiene en el tier degradado.** La
coincidencia sube la confianza en que la *forma* es indígena arubana; no
resuelve si es caquetía.

### ¿Qué palabras de Pinart son *"definitely not Indian"*?

**El texto no las nombra.** La frase aparece una sola vez, en §11 s.v.
`purunchi`, y remite al libro de 1997: *"this list contains several words which
are definitely not Indian (see van Buurt and Joubert, 1997)"*. En §4 sí da el
**mecanismo**: los indios de Aruba se mezclaron temprano con población africana
y europea, *"This can explain some of the African words found in the Indian
wordlist compiled by Pinart in Aruba"*.

> **Consecuencia para F4:** la respuesta a "¿cuáles?" **no está en esta fuente**.
> Habría que conseguir *Stemmen uit het Verleden* (1997). Mientras tanto, lo
> operativo es el mecanismo: sospechar de las voces de Pinart con aire
> afro-caribeño, y apoyarse en las 16 coincidencias de arriba como el subconjunto
> con doble aval.

### Etnohistoria de §4 — propuesta para [[mapa-geografia-politica]]

No se volcó al corpus YAML (no me corresponde). Lo que aporta, con cita:

1. **La deportación de 1634 no vació Curazao.** Tras ella quedaban **tres
   poblados indígenas**: Rancho Indian (cerca de Brievengat), Codoko (cerca de
   Bartoolbaai) y "Pueblo Nuevo de la Asunción" (cerca de Seru Bientu / San
   Hieronymus), este último documentado vivo en el libro de bautismos de **1677**
   y probablemente hasta principios del s. XVIII.
2. **El vínculo dinástico con Manaure sobrevive hasta 1698.** El padre Schabel
   ("Notitia", 1705) viajó con un cacique caquetío *"ex illius Magni Manaure
   [...] ab nepotibus et posteris"* — descendiente del Gran Manaure — que era
   caquetío *"lingue et natione"* y por eso podía conseguir cualquier cosa entre
   los indios de Curazao. **Dato directo para el eje de sucesión.**
3. **1743**: los indígenas restantes de Curazao se trasladan a **Coro**, ya no en
   sus propias canoas sino en un barco holandés. **1747**: Van Laar (WIC) reporta
   aún **1300 indios** en Curazao (cifra que el propio van Buurt considera
   sospechosa o inclusiva de mestizos). Hacia fin del s. XVIII, absorción
   completa.
4. **El área de influencia insular era operativa, no nominal.** La *Relación de
   Antonio Barbudo* (~1570) recoge que los indios de Curazao conocían bien
   Coquibacoa (La Guajira). Existía un **"Puerto de los Indios Curaçao"** al este
   de Puerto Cumarebo, punto de partida documentado hacia la isla (Hartog 1968).
   Los indios de Alto Vista (Aruba) mantenían contacto regular con el pueblo de
   Santa Ana en **Paraguaná** hasta el s. XIX.
5. **Aruba/Bonaire ≠ Curazao.** En Curazao los indígenas quedaron "swamped" por
   un acervo africano mucho mayor; en Aruba y Bonaire mantuvieron identidad
   separada más tiempo (ADN mitocondrial arubano: mayoritariamente indígena).
   **Esto explica por qué tantas voces de §6 están marcadas (A) o (B) y no (C).**

## Descartes razonados

Documentar el descarte vale tanto como el hallazgo: evita re-minarlo.

**Del cruce con Gatschet** (candidatos automáticos, rechazados al leer el texto):

| Candidato | Por qué se cae |
|---|---|
| `shoco` ~ *Choco* | "Choco" solo aparece en *"Prayer to Christ in the Sambu dialect of Choco, Columbian States"*: es una región de Colombia |
| `kiberi` ~ *quiere* | castellano, de la parte del artículo sobre el papiamento |
| `katana` ~ *catjan* | epíteto latino de *Cytisus catjan*, la planta que Gatschet llama `nandu` |
| `makuaku` ~ *macacu* | "mono macacu" está en la lista de papiamento, no en el vocabulario arubano |
| `warwarú` ~ *warawara* | `warawara` ya cruza consigo mismo; el parecido es casual |

**De la cobertura de las 82** (menciones en prosa que NO son respaldo léxico):

- **`cati`** — falso positivo: matchea *Pithecellobium unguis-**cati*** (latín).
- **`coro`** — van Buurt solo nombra la **ciudad** de Coro. Ninguna mención de
  `coro` = 'cardón'. Sin respaldo.
- **`na`** — matchea la preposición papiamenta de *baha na sawaka*. No sostiene
  el `na` = 'partícula comparativa' del lexicón.
- **`gua`** — matchea la discusión del **prefijo** `gua-` (§5: el español
  sustituye /w/ por /gw/). Es evidencia morfológica útil, **no** apoyo al `gua`
  = 'conuco' del lexicón.

**Descartes del propio van Buurt**, que conviene respetar:

- Excluye de §7 los topónimos con **Sabana** y los tipo *Playa Kaketío* (nombran
  un asentamiento caquetío, no son topónimos caquetíos).
- Marca con `?` **Malmok**, **Paradera** y **Skepou** (Malmok podría ser
  neerlandés *malle mok*). El minador conserva la marca en `dudoso`.
- Dice que **`pita`** "is very likely not Caquetío, since Caquetío used `kokuy`".
- Dice que **`indju`** (el otro nombre curazoleño del *Prosopis*) "is definitely
  not Caquetío and came via Spanish".
- Atribuye a **taíno vía español**: `casabí, kanoa, komehein, kunuku, maïshi,
  pita, sabana` (matizando que algunas pudieron existir también en caquetío).

**Duplicado interno de la fuente:** `huliba` aparece **en §6 y en §11** (como
*Capparis indica*). Van Buurt se contradice a sí mismo; el minador lo marca con
`duplicada_en_ambas_secciones`. **Por prudencia debe leerse como §11.**

## Cobertura de las 82 sin cita

De las 82 entradas de familia caquetía del lexicón sin nota ni cita
(tarea F1), van Buurt toca **16**; el resto no deja rastro.

| palabra | ¿aparece? | §6 o §11 | cita | veredicto |
|---|---|---|---|---|
| `chogogo` | sí | **§6** | §6 s.v. *chogogo* (A,B,C) "the greater flamingo (*Phoenicopterus ruber*)" | ✅ **cita recuperada** |
| `chuchubi` | sí | **§6** | §6 s.v. *chuchubi* (A,B,C) "the tropical mockingbird (*Mimus gilvus*)" | ✅ **cita recuperada** + cruza con Gatschet (*shushubi*) |
| `kadushi` | sí | **§6** | §6 s.v. *kadushi* (C,B) / *cadushi* (A), con la *Relación de Nueva Segovia* de 1579 | ✅ **cita recuperada, nivel A** — ⚠ el lexicón dice *Cereus hexagonus*, van Buurt *Cereus repandus* (D7) |
| `sawaka` | sí | **§6** | §6 s.v. *sawaka* (C) "the underworld, the realm of the dead" | ✅ **cita recuperada** — coincide con la glosa del lexicón al pie de la letra |
| `warawara` | sí | **§6** | §6 s.v. *warawara* (A,B,C) "the crested Caracara" | ✅ **cita recuperada** — ⚠ el lexicón dice *Cathartes curasoica*: **es la lectura de Gatschet 1885**, no la de van Buurt |
| `watapana` | sí | **§6** | §6 s.v. *watapana* (A,B,C) "*Caesalpinia coriaria*" | ✅ **cita recuperada, nivel A** (Gatschet + topónimo) |
| `caduchi` | sí | prosa (§6 s.v. *kadushi*) | *Relación de Nueva Segovia*, 1579: *"llamanla en lengua de indio **Caduchi**"* | ✅ **cita recuperada** — atestación colonial directa, y confirma la glosa 'fruto' del lexicón |
| `cari` | sí | prosa (§9, *Cariatávo*) | *"cari means 'coast', 'shore' (Cruz Esteves, 1989)"* | ✅ **cita recuperada** — coincide exactamente con la glosa del lexicón |
| `tata` | sí | **§11** | §11 s.v. *tata* (A,B,C) "father" | ⚠️ **RECLASIFICADA HACIA ABAJO** — el lexicón la tiene como `caquetío-atestiguado`; van Buurt la pone en el tier *"less certain links"* |
| `tuqueque` | sí | prosa (§6 s.v. *waltaca*) | *"totèki is related to, or derived from **tuqueque**, tuteque an Amerindian word used for geckos in Venezuela and parts of Colombia"* | ⚠️ **RECLASIFICADA HACIA ABAJO** — distribución pan-venezolana (filtro 4 del protocolo); y `totèki`, la forma insular, está en **§11** |
| `kunuku` | sí | prosa (§5) | *"casabí, kanoa, komehein, **kunuku**, maïshi, pita and sabana all derive from Taíno"* | ⚠️ **RECLASIFICADA HACIA ABAJO** — van Buurt la da como **taíno vía español**, aunque admite que pudo existir también en caquetío |
| `apana` | sí | prosa (§5, §6 s.v. *watapana*) | *"–apana refers to leaves"* | ⚠️ **DISCREPANCIA DE GLOSA** — el lexicón dice 'una luna (~30 días)'. Van Buurt documenta 'hoja'. Puede ser homonimia; hay que decidirlo |
| `cati` | mención | — | *Pithecellobium unguis-**cati*** | ❌ falso positivo (latín) |
| `coro` | mención | — | solo la **ciudad** de Coro | ❌ no es respaldo léxico |
| `gua` | mención | — | discusión del prefijo `gua-` en §5 | ❌ respalda morfología, no la glosa 'conuco' |
| `na` | mención | — | *baha **na** sawaka* (preposición papiamenta) | ❌ falso positivo |
| **las otras 66** | **no** | — | — | **sin rastro en van Buurt 2014** |

**Balance honesto: 8 citas recuperadas, 3 reclasificaciones hacia abajo, 1
discrepancia de glosa, 4 falsos positivos, 66 siguen sin cita.** El pago real de
esta fuente no está en las 82 (van Buurt trabaja el corpus **insular**, y las 82
son mayoritariamente continentales): está en las 82+29 entradas nuevas, los 180
topónimos y los 19 morfemas.

## Qué falta

1. **Decisión humana sobre `VAN_BUURT_S6`** (85 entradas): qué nivel A/B entra al
   lexicón y con qué etiqueta. La propuesta ya trae `fuente_propuesta` por
   entrada; nadie la ha aprobado.
2. **Resolver `-bana`**: el lexicón dice 'orilla/borde'; van Buurt, 'ancho/llano'
   y 'cubierto'. Afecta a `REGLAS_ZAVALA` y a los neologismos de los agentes.
3. **Resolver las tres reclasificaciones** (`tata`, `tuqueque`, `kunuku`) y la
   discrepancia de `apana`. Es trabajo de F1, no de F6.
4. **Los 180 topónimos siguen sin explotar** como validación de morfología
   (`-bana`, `-bari`, `-kuri`, `-ima`, `wa-`): son el reservorio más fiable de
   sustrato y hoy no alimentan nada.
5. **Conseguir *Stemmen uit het Verleden* (1997)** si se quiere saber qué voces
   de Pinart son *"definitely not Indian"*. Sin él, F4 se queda con el mecanismo
   pero sin la lista.
6. **Higiene**: mover el .txt de la raíz a `fuentes_caquetios/` y actualizar
   `TXT_PATH` en el minador.

## Enlaces

[[gatschet-1885]] · [[alvarado-1921]] · [[zavala-reyes-2015]] ·
[[oliver-1989-cap2]] · [[02_protocolo_habla_paraguanera]] ·
[[mapa-geografia-politica]] · [[mapa-motor]] · [[INDICE_FUENTES]]
