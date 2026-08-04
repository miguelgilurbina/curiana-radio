---
tipo: nota-viva
ambito: decisiones que solo Miguel puede tomar
abiertas: 7
resueltas: 3
tablero: https://github.com/miguelgilurbina/curiana-radio/issues
actualizado: 2026-08-03
---

# Decisiones abiertas

> Nota viva. Sustituye a la tabla de [[PLAN_MAESTRO]] §5 — el plan sigue siendo
> el mapa, pero **el razonamiento de cada decisión se lleva aquí**.
>
> **Desde el 2026-08-03 hay dos registros, y cada uno tiene su trabajo:**
>
> | Dónde | Qué guarda |
> |---|---|
> | **[GitHub Issues](https://github.com/miguelgilurbina/curiana-radio/issues)** | el **estado**: qué está abierto, qué se cerró, qué bloquea a qué |
> | **Esta nota** | el **argumento**: la evidencia, las opciones y el porqué |
>
> No se duplican: el issue enlaza aquí para el razonamiento, y aquí se anota el
> número de issue. **El tablero manda sobre el estado; esta nota manda sobre el
> porqué.**
>
> Al resolver una: cerrar el issue, mover la decisión a *Resueltas* con fecha y
> una línea de por qué, y actualizar el archivo que quedaba bloqueado. No borrar.

## Panorama

| # | Decisión | Bloquea | Estado |
|---|---|---|---|
| [D1](https://github.com/miguelgilurbina/curiana-radio/issues/32) | Veto de la genealogía | V3, J1 | 🔴 abierta |
| [D2](https://github.com/miguelgilurbina/curiana-radio/issues/33) | El nombre "Curiana" | J1, naming público | 🔴 abierta |
| [D3](https://github.com/miguelgilurbina/curiana-radio/issues/34) | `normalizar_por_dialecto()` (M1) | reanudar simulaciones | 🔴 abierta |
| [D4](https://github.com/miguelgilurbina/curiana-radio/issues/35) | Segundo sobrino de Manaure | D1 | 🔴 abierta |
| [D5](https://github.com/miguelgilurbina/curiana-radio/issues/36) | Política ortográfica c/k | F2 | 🔴 abierta |
| D6 | Merge del PR #30 | todo lo demás | ✅ **resuelta** (2026-07-29) |
| D7 | Prelación entre glosa histórica e identificación científica | F3, F4, F6 | ✅ **resuelta** (2026-08-03) |
| [D8](https://github.com/miguelgilurbina/curiana-radio/issues/37) | ¿El repo archiva copias de las fuentes externas? | F10, trazabilidad | 🟡 abierta |
| [D9](https://github.com/miguelgilurbina/curiana-radio/issues/38) | La glosa de `-bana` — **y el hallazgo de `-ana`** | morfología, neologismos | 🟡 abierta |
| D10 | Qué hacer con las 13 entradas reclasificadas | F1, canon | ✅ **resuelta** (2026-08-03) |
| [D11](https://github.com/miguelgilurbina/curiana-radio/issues/39) | **El desbalance wayunaiki/lokono del lexicón** | base de la reconstrucción | 🟠 **abierta, de fondo** |

---

## D1 — Veto de la genealogía propuesta

**Qué hay que decidir.** `3-mundo/corpus/genealogia.yaml` propone linajes
matrilineales, un sucesor (**Waimo-ko**, sobrino uterino de Manaure), su madre
(**Itana-sha**) y ~14 personas de fondo que hoy no existen en el elenco. Nada de
eso es canon hasta que Miguel lo apruebe, rechace o modifique.

**Por qué está abierta.** Elegir genealogías hoy es elegir **qué grupos
familiares existirán mañana**: los linajes son las unidades de expansión del
elenco ([[01_familia_caquetia]] §6.1). No es una decisión estética.

**Qué bloquea.** V3 (notas por agente con genealogía) y J1 (qué se publica — la
genealogía propuesta **no se publica hasta el veto**).

**Qué necesita Miguel para decidir.** Leer `genealogia.yaml` y
[[01_familia_caquetia]] §6. Las opciones no son sí/no: puede aprobar los linajes
y rechazar a Waimo-ko, o al revés.

🔗 [[mapa-familia]]

---

## D2 — El nombre "Curiana"

**Qué hay que decidir.** [[zavala-reyes-2015]], en su nota al pie (4), define
*"Curiana: territorio donde estaban asentados los caquetíos"* — un nombre
**territorial**. Todo el proyecto (código, sitio público, 60 fichas de agente)
lo usa para **el asentamiento**.

**Tres caminos** ([[05_geografia_politica_y_sucesion]] §8):

1. **Dejarlo como está** y dar un nombre de trabajo aparte —marcado como no
   atestiguado— a la confederación/territorio.
2. **Corregir hacia la fuente**: "Curiana" pasa a nombrar el territorio y el
   asentamiento recibe nombre propio — candidato natural, **Todariquiba**. Más
   fiel, pero toca decenas de archivos Python y todo el sitio público.
3. **Aceptar la ambigüedad** ya asentada en meses de contenido y solo
   documentarla.

**Qué bloquea.** J1 (el naming público del jardín). Y crece con el tiempo: cada
mes de contenido nuevo encarece la opción 2.

🔗 [[mapa-geografia-politica]]

---

## D3 — `normalizar_por_dialecto()` (M1)

**Qué hay que decidir.** La función existe en `curiana_social.py` y **no está
cableada**. Dos salidas: cablearla (y re-correr todo cuando se reanuden las
simulaciones) o eliminarla.

**Por qué está abierta.** Código muerto que documenta una intención. Mientras
siga ahí sin decidirse, cualquiera que lea el módulo tiene que preguntarse si
la variación dialectal está modelada o no.

**Qué bloquea.** Condición explícita del gate para reanudar simulaciones
([[PLAN_MAESTRO]] §6.3).

🔗 [[mapa-motor]]

---

## D4 — Segundo sobrino de Manaure

**Qué hay que decidir.** `parentesco-039` recomienda **pluralidad de candidatos**
a la sucesión: un solo sobrino elegible (Waimo-ko) es una simplificación que
elimina justo lo interesante — la **ratificación política** como puerta real, no
como trámite. La corrección no está ejecutada en `genealogia.yaml`; el linaje
Kaira solo anota la dirección en su `capacidad_de_expansion`.

**Qué bloquea.** Es hija de D1: no tiene sentido resolverla antes.

🔗 [[mapa-familia]] · [[mapa-geografia-politica]]

---

## D5 — Política ortográfica c/k del lexicón

**Qué hay que decidir.** ¿Grafía colonial (c/qu) o fonológica (k)? Un lema
canónico por concepto; el otro como variante con referencia cruzada. Hoy hay
pares con **etiquetas de fuente distintas**, lo que hace que la misma palabra
puntúe distinto según cómo la escriba un agente.

**Estado medido (2026-07-29): 10 colisiones**, no 9:

| Normalizado | Formas | Veredicto |
|---|---|---|
| `buco` | `buco` [caquetío] · `buko` [caquetío-atestiguado] | **duplicado real** |
| `barici` | `barici` · `bariki` (ambas atestiguadas) | **duplicado real** |
| `canoa` | `canoa` [reconstruido] · `kanoa` [proto-arahuaco] | duplicado inter-lengua |
| `cati` | `cati` [atestiguado] · `kati` [proto-arahuaco] | duplicado inter-lengua |
| `hamaca` | `hamaca` [reconstruido] · `hamaka` [proto-arahuaco] | duplicado inter-lengua |
| `cacique` | `cacique` · `cacike` (ambas taíno) | duplicado real |
| `caiman` | `caiman` [taino] · `kaiman` [lokono] | inter-lengua |
| `wacusi` | `wakusi` [lokono] · `wacusi` [taino] | inter-lengua |
| `yuca` | `yuca` [taíno] · `yuka` [lokono] | inter-lengua |
| `coro` | `coro` (cardón) · `koro` (**cotorra**) | ⚠️ **falso positivo — no tocar** |

**Matiz importante**: la mayoría son pares **entre lenguas distintas**
(caquetío vs. proto-arahuaco vs. lokono), donde tener dos formas es correcto.
Los duplicados *dentro* del caquetío son pocos: `buco`/`buko` y `barici`/`bariki`.
La decisión real es más pequeña de lo que parecía — pero incluye **cómo se
escribe el caquetío del proyecto**, que sí es una decisión de fondo con
consecuencias públicas.

**Qué bloquea.** F2.

🔗 [[mapa-motor]]

---

## D8 — 🟡 ¿El repositorio archiva copias de las fuentes externas?

*(nueva, 2026-07-29 — surgida del inventario de [[INDICE_FUENTES]])*

**Qué hay que decidir.** **27 hechos del corpus** se apoyan en fuentes que
**no están en el repositorio**: [[paz-reverol-2017-2018]] (9),
[[amodio-perez-2006]] (6), [[perrin-1992-1995]] (6), [[maria-lionza-culto]] (4),
[[keegan-1989]] (2), [[vansina-ong]] (2). Varias son PDF de acceso abierto que se
descargaron, se leyeron y no se guardaron.

**El argumento a favor de archivarlas**: si el enlace cae, el corpus pierde la
capacidad de verificar sus propias citas — justo lo que F10 quiere garantizar.

**El argumento en contra**: `fuentes_caquetios/` ya pesa **~280 MB** y esto es
OneDrive: cada archivo sincroniza. Y hay una cuestión de licencia (Dialnet y
Redalyc son abiertos; Perrin y Keegan no lo serían).

**Opción intermedia** (recomendada): archivar solo los de **acceso abierto y
carga liviana** (Paz Reverol ×2, Amodio y Pérez, Ferrándiz, Fernández Quintana —
todos artículos, no libros) y dejar los demás como referencia bibliográfica con
DOI/URL en la nota de fuente.

---

## D9 — 🟡 La glosa del locativo `-bana`

*(nueva, 2026-08-03 — la levantaron [[gatschet-1885]] y [[van-buurt-2014]] a la vez)*

**Qué hay que decidir.** El proyecto usa `-bana` como locativo *"orilla/borde"*
(está en `CLAUDE.md`, en las reglas morfológicas, y los agentes lo usan para
acuñar neologismos). Las dos minerías insulares dan otra cosa:

| Fuente | Glosa | Evidencia |
|---|---|---|
| Proyecto | 'orilla, borde' | sin cita |
| [[van-buurt-2014]] | **'ancho, llano'** | Hudishibana = 'llano ventoso' |
| [[van-buurt-2014]] vía Oliver | **'cubierto'** | wakaubana = 'cubierto por lo subterráneo' |

**La forma del afijo está confirmada** por cuatro topónimos arubanos
(Shiribana, Tarabana, Wakubana, Bushiribani) — **su significado, no.**

**Por qué no es cosmético.** `-bana` es productivo: los agentes lo usan para
construir palabras nuevas en cada run. Si la glosa es incorrecta, cada
neologismo que lo lleve queda mal formado — y los runs futuros lo propagan.
Es de las pocas decisiones que **contamina hacia adelante**.

**Opciones.** (a) Corregir a 'ancho/llano' siguiendo a van Buurt; (b) mantener
'orilla/borde' y documentar que es lectura del proyecto, no atestiguada;
(c) admitir polisemia y dejar las dos, como hace el lexicón con otros casos.

🔗 [[mapa-motor]] · [[INDICE_FUENTES]]

---

## D10 — 🟡 Qué hacer con las 13 entradas reclasificadas

*(nueva, 2026-08-03 — resultado de la tanda de minería)*

**Qué hay que decidir.** Trece entradas hoy marcadas `caquetío-atestiguado`
tienen ahora una fuente que dice que son de **otra lengua**: `piache` y `ture`
(cháima), `pauji` (chaima, y además es un árbol), `watapana` y `auyama`
(cumanagoto), `kunuku` y `caraota` (taíno), `kukuisa`, `cumaragua`, `guanepe`,
`bureche`, `tata`, `coro`. Corre `python curiana_sim/auditar_82.py` para la
lista viva.

**El caso duro es `piache`**: es la palabra para chamán, aparece en el canon, en
fichas de agente y en el sitio público. [[alvarado-1921]] p.248 la da como
*"voz cháima y tamanaca, con formas afines en otras lenguas caribes"* — y
[[zavala-reyes-2015]] confirma por otra vía que en su glosario *piache* es la
**glosa española** de `boratio`, no una voz caquetía.

**Cautela justa antes de decidir**: Alvarado 1921 es el juicio de un filólogo,
no un veredicto definitivo, y una palabra puede circular entre familias
lingüísticas. Pero **el peso de la prueba se invirtió**: hoy estas entradas no
tienen ninguna cita a favor y sí una en contra.

**Opciones.** (a) Degradar las 13 a la etiqueta de la lengua que la fuente
indica (`caribe`, `taíno`, `cumanagoto`…) y dejar que `score_linguistico` las
trate como ajenas; (b) degradarlas a `hipotético` conservando la forma;
(c) caso por caso — probablemente lo correcto, porque `piache` (con sustituto
atestiguado, `boratio`) no es lo mismo que `tata` (que van Buurt solo baja de
tier, no reasigna de lengua).

**Ojo con el efecto colateral**: varias dan nombre o rol a agentes del elenco.
`piache` → el oficio de Shaboro; `watapana`, `kadushi` → nombres de agente.
Degradar la etiqueta **no** obliga a renombrar a nadie, pero conviene decidirlo
a la vez.

🔗 [[mapa-motor]] · [[INDICE_FUENTES]] · [[alvarado-1921]]

---

## D11 — 🟠 El desbalance wayunaiki/lokono del lexicón

*(nueva, 2026-08-03 — la levantó la minería F5 de [[oliver-1989-cap2]]. **Es la
decisión más de fondo del proyecto en este momento.**)*

**El hecho.** El lexicón se construyó sobre la premisa de que el wayuunaiki es
la hermana más cercana del caquetío. **Oliver dice lo contrario**, y está en el
capítulo que el proyecto declara su pilar teórico:

> *"All things considered, it seems reasonable, for the moment, to regard
> Caquetío as emerging from a similar background to that of **Lokono rather than
> from a Guajiro-Paraujano ancestry**."* (cap. 2: 150)

Lo apoya en tres cosas: el prefijo de 1.ª persona `/dA-/` (*"only the Lokono and
Taíno are known to have the same personal prefix"*), postposiciones como
`-bana` **en vez de** `-pana`, y que los topónimos Guajira-Falcón muestran *"far
more differences in sound sequences than similarities"*.

**La composición actual del lexicón, medida:**

| Lengua | Entradas |
|---|---|
| **wayunaiki** (+cogn) | **776** |
| **lokono** (+variantes) | **225** |
| taíno | 53 |

**3,4 a 1 a favor de la hermana que Oliver considera más lejana.** Y las 441
formas `hipotético-no-verificado` de `lexicon_candidatos.py` se transdujeron
mayoritariamente desde wayunaiki — lo que explicaría parte del ~80% de fallo
medido: se reconstruía desde la lengua equivocada.

**Qué hay que decidir.** No es "borrar el wayuu". Es de qué lengua se reconstruye
cuando no hay dato caquetío:

- (a) **Reequilibrar hacia el lokono** — hacer del lokono la fuente primaria de
  transducción y del wayuunaiki una secundaria. Implica re-derivar candidatos y,
  con ellos, buena parte de la Capa 2.
- (b) **Mantener el wayuunaiki como primario** y documentar explícitamente que
  es una decisión *de disponibilidad* (el wayuu está mucho mejor documentado y
  vivo), no *de filiación*.
- (c) **Ponderar por concepto**: usar el que tenga cognado atestiguado en cada
  caso, con el lokono desempatando.

**Lo que NO cambia.** El wayuu sigue siendo la comparanda **etnográfica** central
y bien fundada: todo el corpus cultural (creencia, transmisión, parentesco) se
apoya en etnografía wayuu, y eso no depende de la filiación lingüística. El arco
norteño sigue siendo matrilineal de punta a punta — el lokono también lo es.
Lo que se mueve es de quién se reconstruye **la lengua**.

**Cautela.** Oliver es explícitamente tentativo (*"for the moment"*,
*"tentatively"*, *"aknowledging the lack of further evidence"*). No es un
veredicto cerrado. Pero es la única autoridad que el proyecto cita para esto, y
va en dirección contraria a lo que se asumió.

**Bloquea**: cualquier re-derivación de la Capa 2, y conviene resolverla **antes**
del primer run de la era auditada — es exactamente el tipo de cambio de base que
obliga a repetir corridas.

🔗 [[oliver-1989-cap2]] · [[01_familia_caquetia]] · [[mapa-motor]] · [[mapa-familia]]

---

## Resueltas

### ✅ D7 — Prelación entre glosa histórica e identificación científica *(2026-08-03)*

**Decisión de Miguel: se registran las dos, en campos separados.**

Cuando una fuente histórica y una identificación científica moderna difieren
sobre la misma palabra, **ninguna gana**: van en campos distintos.

- **`glosa_fuente`** — lo que dice la fuente histórica, verbatim, con su cita.
  **Es la que el agente habla**: el caquetío del s. XV nombraba lo que sus
  hablantes veían, no un taxón linneano.
- **`identificacion_moderna`** — el taxón actual, cuando exista, como nota
  auditable. No sustituye a la glosa; la sitúa.

**Por qué así.** Es la misma disciplina que ya rige el lexicón entero: el
conflicto queda **visible** en vez de resuelto en silencio, y nadie pierde
información. Zanjarlo a favor de uno de los dos habría borrado dato real en
cualquiera de las dos direcciones.

**Casos que la estrenan** (los dos que la provocaron, de [[zavala-reyes-2015]]):

| Palabra | `glosa_fuente` | `identificacion_moderna` |
|---|---|---|
| `cunaro` | "Pez del golfete de Coro. Promicops Guasa" (Zavala #—) | *Rhomboplites aurorubens*, pargo de altura (SVDB) |
| `guaranaro` | "Pez lisa" (Zavala) | sin resolver — probablemente *Mugil* sp. |

**Consecuencia operativa.** Las minerías F3/F4/F6/F7 aplican esta política desde
el primer registro. Los tres son glosarios con identificación taxonómica, así que
el campo doble es la norma, no la excepción.

---

### ✅ D6 — Merge del PR #30 *(2026-07-29)*

Estaba mergeado antes de que arrancara el vault: commit `609f9b5`, *"Merge pull
request #30 from miguelgilurbina/feat/corpus-cultural"*, ya en `main`. La rama
traía corpus cultural + sesión 5 + Zavala + arreglos del motor. Era el
prerrequisito de todo lo demás ([[PLAN_MAESTRO]] §7.1) y está cumplido.

---

## Pendientes de higiene (no son decisiones — solo hay que hacerlos)

Salidos del inventario de [[INDICE_FUENTES]]. Ninguno necesita criterio de nadie:

- [ ] Borrar los dos **duplicados muertos de 0 bytes**:
      `Oviedo_Banhos_1885_Conquista_Venezuela.pdf` y
      `Perea_Alonso_1942_Filologia_Comparada_Lenguas_Arawak_TomoI.pdf`.
- [ ] **Renombrar** `Schroeder_et_al_2018_PNAS_Origins_Caribbean_Taino.pdf` →
      `MorenoMayar_et_al_2018_Science_Early_Human_Dispersals.pdf` (el contenido
      no es lo que dice el nombre).
- [ ] Mover `VanBuurt_2014_CaquetioWords_Papiamentu.txt` de la raíz a
      `fuentes_caquetios/`, o documentar por qué vive fuera.
- [x] ~~Corregir [[05_geografia_politica_y_sucesion]] §2: dice que el glosario
      de Zavala tiene **116 entradas**~~ — corregido a 288 (F7, 2026-08-03).
- [x] ~~`minar_zavala_glosario.py` revienta con `UnicodeEncodeError`~~ —
      arreglado (F7). ⚠️ **`test_quick.py` tiene el mismo bug** y sigue abierto:
      revienta sin `PYTHONIOENCODING=utf-8`. Misma línea de arreglo.
- [ ] Recuperar los 4 archivos de 0 bytes que sí son huecos reales
      ([[rouse-cruxent-1963]], [[fernandes-2020]], [[ramos-perez-1978]],
      el PDF de [[brinton-1871]]).

## Enlaces

[[INDICE]] · [[PLAN_MAESTRO]] · [[INDICE_FUENTES]] · [[mapa-motor]]
