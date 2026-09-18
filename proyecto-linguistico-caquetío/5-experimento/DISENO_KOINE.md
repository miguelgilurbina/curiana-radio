# Diseño: Koiné Emergente — Maturana, Cynefin y el Emocionar

**Estado:** diseño + implementación en curso (rama `feat/koine-emergente`).
Espejo técnico de la página Notion *"Koiné Emergente — Maturana, Cynefin y el
Emocionar"* (hija del Marco Teórico). La página de Notion lleva el marco
teórico; este archivo lleva las estructuras de datos, las métricas y la
mecánica. Mantener ambos en consonancia.

> Relación con lo existente: el Marco Teórico (§1) define **cómo se reconstruye
> la forma** (método comparativo). Esto agrega un eje perpendicular: **cómo el
> uso converge en una norma**. No reemplaza nada; responde las preguntas
> abiertas §9 de Notion ("¿se puede medir el drift?" y "toponimia generativa").

---

## 1. El problema que resuelve

El análisis del run `2e729f3f` (30 turnos, 15 días) mostró que la lengua llega
a su equilibrio (92% caquetío) el **día 1** y se queda plana. No hay deriva.
Causa estructural, no de tuning:

1. **Sin variación** — los 48 agentes activos reciben la misma identidad y la
   misma muestra de léxico. La única variación es por etnia (gruesa, estática).
2. **Sin transmisión con memoria** — la memoria son 3 snippets de texto crudo;
   no acumula un perfil lingüístico que sesgue el futuro del agente.
3. **Sin retroalimentación que componga en el tiempo** — lo único que cruza el
   tiempo es "últimos 15 neologismos adoptados" + contagio, que converge y se
   congela (adopción con 2 agentes, sin competencia entre variantes).

Sin esos tres no hay motor de cambio acumulativo.

## 2. El objetivo: una koiné caquetía emergente

Formar, por convergencia, una **koiné** anclada en el caquetío atestiguado/
reconstruido — y luego usarla como lente para "leer" topónimos reales del
territorio (fase posterior, ver §8).

> **Una koiné es un *dominio consensual* en el sentido de Maturana**:
> coordinaciones recurrentes de conducta que se estabilizan entre seres que
> conviven. Ese es el marco teórico que vuelve legítimo el experimento.

### El arco: diverso → converge

Una koiné solo se forma —y solo es **visible/medible**— si hay variación
inicial que converja. Por eso el run debe empezar *diverso a propósito*:

```
DÍA 1: caquetío nuclear + guaycarí + jirajara + insular aruba, cada facción
        con su sesgo de habla  →  ALTA distancia idiolectal
   ↓   (innovación + contagio + prestigio + frecuencia + coordinación)
DÍA N: una norma compartida anclada en caquetío  →  BAJA distancia idiolectal
```

Consecuencia: **activar a los agentes foráneos/periféricos no es opcional** —
son los aportantes de la mezcla que después se asienta.

## 3. Los tres paradigmas → mecánica medible

| Paradigma | Qué aporta | Mecanismo medible |
|---|---|---|
| Maturana — lenguajear/coordinar | *por qué* converge | estímulos de coordinación; `EMOCIONAR` por agente |
| Maturana — dominio consensual | *qué es* la koiné | fijación de variantes; contracción de distancia idiolectal |
| Cynefin (galés: pertenencia a la tierra) | mente *emplazada* | paisaje nombrado; idiolecto de tierra; topónimos emergentes |
| Préstamos venezolanos (cunaro/guaranaro/saruro) | anclaje + validación | fonología koiné + set de validación contra dato real |

**Disciplina:** los paradigmas moldean **escena, identidad y emocionar**
(los inputs). Los agentes nunca *hablan de* autopoiesis ni de emociones — su
emocionar moldea *cómo* lenguajean. Las **métricas** (§7) son la espina
dorsal que mantiene el experimento honesto y falsable.

## 4. El emocionar sembrado (semilla de idiolecto)

No se inventan personalidades: se **extrae el emocionar ya latente** en los
`system_prompt` y se vuelve una palanca de datos. Ej. ya escrito hoy:
Manaure "formas completivas constantemente"; Dare-nu/Dara-ko "presente y
aspecto continuativo"; Shaboro "metáforas de animales y agua".

Estructura nueva (por agente, en `curiana_agents.py` o módulo aparte):

```python
EMOCIONAR["Manaure"] = {
    "disposicion":  "contención vigilante — la carga del que sostiene el cielo",
    "sesgo_lexico": ["jerarquia", "cosmos", "biro"],   # dominios que alcanza primero
    "sesgo_morfo":  {"aspecto": "completivo", "afijos": ["-ka"]},
    "registro":     {"frase": "corta/definitiva", "metafora": "baja"},
}
```

Dos efectos (los dos importan):

1. **Sesga el prompt** — una línea `[Tu emocionar]: ...` reemplaza al genérico.
2. **Pre-carga el `Counter` de idiolecto** — cada agente arranca con SUS formas
   favoritas ya "entrenadas" → distancia idiolectal alta el día 1. Sin esta
   pre-carga, todos arrancan iguales y "convergencia" no significa nada.

Cynefin se suma como `sesgo_lexico` enraizado en lugar (topónimos y
palabras-de-tierra del trozo del Golfete de cada agente).

### ⚠️ La pre-carga se había perdido con los nombres nuevos (2026-09-16)

`FORMAS_SEED` y `EMOCIONAR_SEED` están indexados por los nombres de la **era
1**, y la campaña de antropónimos (2026-09-14) renombró a 60 de 63 agentes. El
orquestador sembraba con el nombre NUEVO y sin pasar por `ALIAS_ERA1`, así que
en la era 2 sólo Manaure —el único que conserva su nombre— encontraba su
semilla. Medido con `python curiana_koine.py`:

| | era 1 (60) | era 2 (63) antes | era 2 después |
|---|---|---|---|
| semilla escrita propia | 20 | 1 | 1 |
| escrita, por alias | — | 0 | 10 |
| derivada de la ficha | — | 0 | 52 |
| núcleo compartido (todos igual) | 40 | 62 | 0 |
| **vectores-semilla distintos** | **21 de 60** | **2 de 63** | **63 de 63** |

O sea: los tres días corridos de la era 2 arrancaron con 62 de 63 agentes
diciendo exactamente lo mismo. Por eso su convergencia no se puede leer como
koineización — la precondición no estaba.

**Qué se arregló.** `formas_seed_de()` y `emocionar_de()` resuelven el nombre
por `ALIAS_ERA1` (lo expone `curiana_agents`, que es el único que sabe qué
elenco está activo), y quien no tiene semilla escrita recibe una **derivada de
su propia ficha**, en tres piezas:

1. **Lo que su ficha ya dice** — las voces caquetías que aparecen literalmente
   en su `system_prompt`, su `oficio` y su `descripcion`. Es el mismo principio
   con que se escribieron las semillas de la era 1 (la línea «Vocabulario que
   usas» de su prompt).
2. **El campo semántico de su oficio** — sin tabla nueva: se reusa
   `curiana_lexicon.categorias_relevantes()`, la heurística de palabras clave
   que ya prioriza el lexicón del prompt, aplicada **dos veces**: al oficio del
   agente (qué hace) y a la glosa de cada voz del lexicón (qué significa). La
   semilla sale de la intersección — pesca → voces de mar y orilla, alfarería →
   barro y vasija, boratio → cosmos y ritual. El `categoria` declarado del
   lexicón no basta: sólo 28 de 401 voces caquetías lo traen.
3. **El aspecto de su emocionar** sobre dos raíces verbales suyas, que es la
   firma morfológica que las semillas escritas también llevan (`naa-ka`,
   `wana-ni`…).

El sorteo dentro del campo es **determinista**: `blake2b(semilla del run,
nombre, etiqueta)`. Ni el RNG global —el motor lo comparte con eventos,
muestreo y nombramientos— ni `hash()`, que va salado por proceso
(`PYTHONHASHSEED`) y no repetiría un run. `--semilla N` mueve las derivadas y
no toca las escritas.

**Residuos declarados.**
- La capa **hipotética** no entra en una semilla derivada: 35 de sus 38 voces
  son formas que el proyecto acuñó para la simulación, y el perfil `era2` las
  esconde a propósito. Sembrarlas adelantaría justo lo que se quiere ver
  acuñar. Las otras tres capas sí, que es de donde salen las escritas (medido:
  88 reconstruido, 31 atestiguado, 3 retroabstraído, 0 hipotético).
- Los **homógrafos de nombres del elenco** tampoco (49 de los 63 nombres lo
  son): el bloque «sueles decir: …» del prompt sale de aquí, y sembrar `karebe`
  le diría al agente que suele decir el nombre de su vecina. Se puede seguir
  aprendiendo en juego —el scorer la cuenta en minúscula—, pero no se siembra.
- El oficio de **1 de los 63** (Chirwa, «aprendiza de alfarería con Dabuda») no
  dispara ninguna categoría: su semilla sale del caquetío sembrable entero.
- **La era 1 no cambia, byte a byte.** `ALIAS_ERA1` está vacío allí y la
  derivación exige `oficio`, campo que sólo trae el módulo generado de la era
  2. Sus 40 agentes sin semilla siguen en el núcleo compartido (deuda abierta:
  ahí la precondición sigue a medias).

**⚠️ `--continuar` no recupera una pre-carga que nunca hubo.** `cargar_koine`
reconstruye los idiolectos con `peso_semilla=0` a propósito (las frecuencias
guardadas ya traen la semilla del día 1), así que una cadena que arrancó sin
pre-carga no la gana por seguir encadenando. El motor lo mide al continuar
(`agentes_sin_precarga()`) y avisa; la única salida es **re-correr la cadena
desde el día 1**.

## 5. Memoria e idiolecto (estado nuevo por run)

### `IdiolectoAgente` (por agente)
- `frecuencias: Counter[str]` — formas que el agente produjo (entrenchment).
  Se actualiza cada turno desde `registro.palabras_caquetias` + neologismos.
  Se **pre-carga** con el `sesgo_lexico` del emocionar.
- `acunaciones: set[str]` — formas que él inventó.
- `adopciones: set[str]` — formas que tomó de otros.

> ⚠️ **La forma acuñada no quedaba en `word_uses` en boca de quien la acuña
> (2026-09-16).** El idiolecto sí la registraba (`registrar(formas, neos)`),
> pero `words_used` es `palabras_caquetias`, y `score_linguistico()` sólo
> reconoce `lexico.palabras_activas()` (base + **adoptados**): una acuñación
> recién propuesta no está ahí. Resultado: el primer uso que constaba en
> `word_uses` era el del **ADOPTANTE**, que puede ser del otro nodo — 29 de 40
> acuñaciones de la era 2 (72,5 %, medido por `analizar_nodos.py`). Eso
> **invierte las rutas de contagio** que se leen de esa tabla. Desde ahora el
> orquestador pasa las formas acuñadas aparte (`save_agent_response(...,
> coined_words=…)`) y la capa de base les escribe su fila con
> `source_language='caquetío'` declarado —no está en el lexicón y
> `word_source_language()` la dejaría en NULL—. El scorer **no se toca**, así
> que ni `score` ni `pct_caquetio` se mueven a mitad de serie
> (`language_composition()` sólo cuenta `VOCABULARIO_BASE`).

### Inyección "tu manera de hablar"
Reemplaza los 3 snippets de texto por un bloque compacto derivado del perfil:
*"sueles decir X, Y; acuñaste Z; tu aspecto es -ka"*. Esto cierra el lazo de
entrenchment: lo que dijiste, lo repetís → deriva individual que compone.

> Consonancia con `CANON_TIERRA.md`: el "segundo compartimento de memoria que no
> expira" que pediste para los ritos **es** este `IdiolectoAgente`. Lo que se
> transmite en un rito y arraiga en la memoria larga es lo que se fija en la
> koiné.

## 6. El motor de convergencia: selección hasta fijación

### Campo de frecuencia comunitario (`CampoLexico`, por run)
- `Counter[str]` global de todas las formas usadas.
- `muestra_caquetio_dinamica()` pasa de muestreo aleatorio a **ponderado por
  frecuencia** (rich-get-richer → curvas S de adopción).
- **Decaimiento**: formas no usadas en N turnos pierden peso → recambio léxico
  (deja que cosas mueran).

### Competencia y fijación de variantes  ✅ IMPLEMENTADO (`CompetenciaLexica`)

> **Hallazgo (run 9bb920eb):** la competencia NO ocurre sola. Agrupar por glosa
> dio CERO competencia — cada agente acuña para un concepto distinto (46
> neologismos → 46 conceptos). Una koiné nace de una **necesidad referencial
> compartida**: algo nuevo que VARIOS deben nombrar. Por eso la fijación vino en
> dos piezas, no una.

**(1) Inductor — eventos de nombramiento.** `REFERENTES_NOVEDOSOS` (10 cosas sin
palabra caquetía: cuentas de vidrio, cometa, eclipse, metal amarillo, marea
roja, bestia varada…). Cada ~4 turnos el orquestador presenta un referente a
TODOS los agentes activos con el mismo `concepto_id` → acuñan formas rivales
para el MISMO concepto.

**(2) `CompetenciaLexica` — resolución.**
- Cada variante acumula soporte = `frecuencia × prestigio` de quienes la usan
  (`proponer` al acuñar, `registrar_uso` al reusar; los agentes de prestigio
  anclan la norma).
- `prompt_competencias()` surface las competencias abiertas en el prompt →
  empuja a REUSAR una forma rival en vez de inventar otra (así una se impone).
- Una variante se **fija** cuando domina su concepto (≥55% del soporte, soporte
  mínimo). El conjunto de fijadas = el **diccionario koiné**, persistido en
  `koine_lexicon`.
- Validado (run dd1d0c9c): `cuentas_vidrio` → `kali-pica` fijada de 3 rivales.

### Guardarraíl (prerrequisito, no opcional)
Si se refuerza frecuencia sin filtrar, la koiné fija basura española
(`suave-bana-ni`) tan eficientemente como fija aciertos. La **compuerta de
calidad de neologismos** (quick-win #3) debe estar activa: rechazar raíces
no-caquetías y morfología inválida antes de que una forma pueda competir.

## 7. Medición — cómo probamos que la koiné se formó

Esto vuelve el resultado defendible en vez de anecdótico. Tabla nueva
`koine_metrics` (o vista) por run/día:

- **Distancia idiolectal media** entre agentes (coseno/Jaccard sobre vectores
  de frecuencia de formas). **Debe contraerse** en el tiempo → firma de la
  koineización. Si no se contrae, no hubo koiné.
  - ⚠️ **Corrección metodológica (2026-07-04):** la versión acumulada de esta
    métrica converge por mera acumulación del vocabulario base compartido
    (artefacto matemático), no por koineización. Desde entonces se miden TRES
    lecturas por día (`koine_metrics.distance / distance_ventana /
    distance_emergente`): acumulada (histórica), **ventana** (últimos
    `VENTANA_TURNOS` de habla real, sin formas-semilla) y **emergente**
    (ventana excluyendo el vocabulario base: solo neologismos/adopciones).
    El veredicto de convergencia se emite sobre la más exigente con datos.
    Verificado en un run corto: la acumulada "convergía" mientras ventana y
    emergente divergían — el artefacto era real.
  - 🔗 **La unidad del veredicto es la CADENA, no el run (2026-09-16):** en la
    era 2 un run es UN día (`--continuar`), así que su serie tiene un punto y
    el veredicto decía siempre «datos insuficientes» aunque los días
    encadenados ya mostraran la caída. `curiana_cadena.py` sube por
    `simulation_runs.config->continuado_desde` hasta la raíz, une las
    `koine_metrics` de toda la cadena y emite **el mismo criterio** (la función
    `veredicto()` es la extracción del bloque del orquestador, no un criterio
    nuevo: el motor la llama en los dos sitios). Un run interrumpido —sin
    `ended_at` o con `total_turns` 0— sigue EN la cadena, porque hay que poder
    subir a través de él, pero sus métricas no entran: la unidad de la serie es
    el **día cerrado**. Si dos runs de una cadena midieron el mismo día, gana el
    más cercano a la hoja. Se lee al cerrar cada run continuado, con
    `python curiana_cadena.py` y con `analizar_runs.py --koine`.
    Medido sobre `c6837386` → `89fc1744`: emergente 0.8995 → 0.8203 (−8,8%) →
    CONVERGE; ventana 0.6038 → 0.4665; **la acumulada SUBE** (0.1993 → 0.2295),
    que es justamente por lo que el veredicto no se emite sobre ella.
  - ⚗ **Run de control (`--ablacion`):** apaga las tres inyecciones de prompt
    que empujan la convergencia (sugerencias de contagio, competencias
    abiertas, muestreo ponderado). La evidencia de koineización emergente es
    la DIFERENCIA entre un run normal y su ablación, no el run normal solo.
- **Variantes por significado → 1** (tasa de fijación).
- **Curvas de frecuencia** de las formas ganadoras (forma de S esperada).
- **Supervivencia de neologismos** (nace → vive → muere / se fija).
- **Diccionario koiné extraíble** al cierre del run (forma fijada por glosa +
  afijos ganadores + tendencias fonológicas).

### El ámbito: las cuatro vías dejan de ser globales (2026-09-17) ✅ capa 2

Hasta hoy las cuatro vías por las que una forma circulaba eran **de toda la
comunidad**, y por eso los dos nodos nombraban a la vez. Con `--escena` el
ámbito de lo que un agente ve es **el lugar donde está ahora**, y la puerta es
una sola: `curiana_escena.ambito_de(agente, state)` (diseño §2, decisiones p5,
p6, p9 de la tanda del 2026-09-17). Ninguna de las cuatro lee el nodo por su
cuenta; con `ambito=None` —la era 1, o la era 2 sin el flag— las cuatro son
byte a byte las de siempre.

| vía | dónde | qué filtra el ámbito |
|---|---|---|
| **V1** propuestas en evaluación | `prompt_pendientes_evaluacion(lexico, ambito)` | sólo lo propuesto **aquí** (`Neologismo.ambito`) |
| **V2** adoptadas de la comunidad | `prompt_lexico_activo(lexico, ambito)` | sólo lo adoptado **aquí** (`Neologismo.adoptado_en`) |
| **V3** competencias abiertas | `CompetenciaLexica.prompt_competencias(ambito=…)` | sólo las formas rivales propuestas **aquí** |
| **V4** muestreo rich-get-richer | `CampoLexico.pesos_de(ambito)` | el campo del lugar; el global es la **suma** de los lugares |

**La oficialización sabe dónde pasó, y declara por qué vía.** Sigue haciendo
falta lo mismo —dos adoptantes distintos— pero `Neologismo.via` dice si fueron
del mismo lugar (`un-ambito`) o de dos (`dos-ambitos`). La segunda es la vía
que la escena hace posible y la que hay que ver nacer: para adoptar una forma
en otro lugar alguien tuvo que llevarla, porque el bloque de propuestas que
ese lugar ve está filtrado por su propio ámbito. Sale medida en el diccionario
de cierre (`LexicoComunitario.reporte_linguistico`) y en
`adoptados_en_dos_ambitos()`. **La FIJACIÓN no se parte**: el soporte de una
forma rival suma venga del ámbito que venga, porque el ámbito cambia lo que el
agente VE, nunca con qué se le mide (la misma regla que gobierna los perfiles).

**`[Lo que se dijo aquí]`** es el bloque nuevo: las ≤ 3 intervenciones del
MOMENTO ANTERIOR dichas en este lugar, ≤ 280 caracteres, con el nombre y la
frase caquetía sin su glosa (`curiana_escena.bloque_lo_que_se_dijo_aqui`). Del
momento anterior y no del mismo turno: con el mismo turno el orden de habla
vuelve a ser destino, que es el mecanismo de V1 que produjo los tres cruces de
Δturnos = 0 del día 1 de la serie B.

Medido en el ensayo sin API de seis turnos (`tests/test_escena_oir.py`, mismo
doble de cliente, RNG fijado, sin día de Capubana), contra el mismo ensayo sin
el brazo:

```
                                   sin escena   con escena   día de Capubana
V1 formas por prompt                   4,12        1,71           4,10
V2 formas por prompt                   0,97        0,06           0,97
V3 formas por prompt                   3,86        0,81           3,86
prompts con [Lo que se dijo aquí]      0/72       17/72          60/72
ámbitos con léxico                        0          21              1
prompt medio (caracteres)             8.111       7.840          7.919
```

El día de Capubana los 63 están en el cerro: **un solo ámbito, y las tres vías
del prompt vuelven a los números de la comunidad entera** — que es exactamente
lo que la convergencia significa, y lo que debería producir el diente de
sierra de la brecha intra/entre (§5.1 del diseño de la escena). El coste en el
prompt es **negativo** (−3,3 %): lo que el bloque de oír añade es menos que lo
que el filtro de V1/V2/V3 quita.

⚠ **Y eso no pasaba solo: hubo que arreglarlo** (2026-09-18, día 1 de la serie
C). En el ensayo de arriba los seis turnos corrían EN el cerro, así que todo lo
propuesto estaba en `"Capubana"` y las vías «volvían» sin hacer nada. En una
cadena de verdad el día 3 llega con dos días de léxico repartido por 28 lugares
y `"Capubana"` es **un lugar más**, con el léxico de sus dos ocupantes del día 1
(Sawaka y Hayo, 71 formas): V2 vacía y las tres rivales de «las cuentas» a 0.
Desde entonces hay **dos puertas**: `ambito_de` (dónde ESTÁ: el registro,
`[Aquí estás]`, `presencias`, el campo — ese día `"Capubana"`) y
`ambito_visible_de` (qué VE: las cuatro vías y el bloque de oír — ese día
`None`, la unión de todos los ámbitos). Ver la trampa homónima en `CLAUDE.md`.

⚠ **La FIJACIÓN tampoco duraba.** `CompetenciaLexica` no se persistía y
`auto_mode` creaba una nueva en cada run, mientras `referentes_introducidos`
impedía volver a presentar el referente: en la era 2, donde **un run es un
día**, ninguna competencia podía durar más de un día ni llegar nunca al 55 %.
Desde el 2026-09-18 viaja en `curiana_koine.json` junto a los idiolectos y el
campo, y `--continuar` la recupera entera (referentes abiertos y fijados,
variantes con su soporte, el ámbito de cada proponente).

⚠ **17 de 72**: el bloque de oír sale poco, y se sabe por qué. Pide que alguien
haya hablado **en tu lugar** en el momento anterior, y por turno hablan 12 de
63 en 8-27 lugares distintos (§3.3). Con la ventana de 12 sin tocar (decisión
p4 → A) eso es el techo. Si Miguel quiere más, las palancas declaradas son la
cadencia del Capubana y la capa 3 (el cierre de ayer en ese lugar, opción B de
la pregunta 5), no cambiar quién habla.

## 8. Fase posterior: topónimos (no en este PR)

La koiné da: (a) inventario fonológico + reglas de sonido, (b) set de morfemas
ganadores (-bana, -ana, -ko...), (c) léxico preferido. Con eso se "lee" un
corpus de topónimos reales del territorio.

- **Set de validación ya existe** en Notion (*Venezolanismos de Origen
  Indígena* §I y §VI): `cunaro/guaranaro/saruro` confirman la terminación
  -aro/-uro; los morfemas -gua/-bana/-cuy ya están documentados.
- **Honestidad epistémica** (consonancia con el Marco Epistemológico): el
  parsing koiné de un topónimo es *"así lo rendiría la koiné de la Curiana"*,
  una **lente construida**, NO "la etimología real". Etiquetar como tal. Los
  topónimos son reales; la lectura koiné es una construcción.
- ⚠️ Verificar la familia de cada préstamo antes de usarlo como evidencia
  caquetía: muchos venezolanismos son Caribe/Taíno (p.ej. *tapara* suele darse
  como cumanagoto), no caquetío.

## 9. Orden de implementación

1. ✅ `EMOCIONAR` por agente + inyección en el prompt.
2. ✅ `IdiolectoAgente` + `CampoLexico` (estado por run) + pre-carga desde el emocionar.
3. ✅ Inyección "tu manera de hablar" (reemplaza los snippets).
4. ✅ Muestreo ponderado por frecuencia + decaimiento (`CampoLexico.pesos` →
   `muestra_caquetio_dinamica`, Efraimidis-Spirakis con base 1.0 para mantener
   exploración → rich-get-richer).
5. ✅ Competencia/fijación — vía eventos de nombramiento (no por glosa; ver §6).
6. ✅ Métricas (distancia idiolectal + fijación) + persistencia (`koine_metrics`,
   `koine_lexicon`).
7. ✅ Población constante de participantes en el loop (`PARTICIPANTES_KOINE`).
8. ✅ Compuerta de neologismos (fonotáctica: blocklist + marcadores + bigramas).
9. ✅ El ÁMBITO: las cuatro vías por lugar y `[Lo que se dijo aquí]` (capa 2 de
   la escena, `--escena`; ver arriba). Es un BRAZO: sin el flag nada cambia, y
   una cadena no puede cambiar de brazo a la mitad (`curiana_cadena` tampoco
   mezcla los días de dos brazos).

## 10. Referencias

- Maturana, H. & Varela, F. — *El árbol del conocimiento* (1984); Maturana,
  *Biología del lenguajear* y *Emociones y lenguaje en educación y política*.
- Cynefin (concepto cultural galés de pertenencia a la tierra/los ancestros);
  no confundir con el framework homónimo de Snowden.
- Documentos internos: Notion *Marco Teórico y Metodológico*, *Marco
  Epistemológico*, *Venezolanismos de Origen Indígena*; repo `CANON_TIERRA.md`,
  [[CULTURA_CAQUETIA]], `ANALISIS_RUN_30T_2026-06-22.md`.
