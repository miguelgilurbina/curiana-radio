# Falsos neologismos que son la plantilla: medido, y NO aplicado

> ✅ **CERRADO el 2026-09-18 con la opción A** («Dale pues con A», Miguel).
> El filtro está aplicado como **corte de serie declarado**: la puerta vive en
> `curiana_lexicon.FORMAS_DE_PLANTILLA` y rechaza en
> `LexicoComunitario.registrar_neologismo()` y en
> `CompetenciaLexica.proponer()`. La serie C **se re-corre entera desde el día
> 1**; `76ecf45c` y `96b22194` quedan como los dos días con el prompt
> contaminando la competencia. Lo medido sobre esos dos días —144 respuestas,
> control 144/144— está en
> `6-fusion/medicion_formas_de_plantilla_corte_2026-09-18.yaml`, y el corte
> está declarado en el punto 8 del «Cambio de instrumento» de
> `BITACORA_RUNS.md`. Lo de abajo es el argumento tal como se le presentó a
> Miguel, y se conserva por eso.
>
> Lo que la decisión NO cierra: la §4, la pregunta de si la adopción debe
> exigir que el adoptante pudiera VER la propuesta. Sigue abierta.

**Para que Miguel decida.** El arreglo está escrito y medido; **el motor no se
tocó** porque mover `score` a mitad de serie no se hace. Esto es la medición y
la propuesta.

> El día 1 de la serie C (run `b7bc51dc`) registró como acuñaciones dos formas
> que el propio prompt enseña:
>
> - **`kali-bana`** es el **ejemplo literal** del bloque
>   `_IDENTIDAD_LINGUISTICA` que va en el system prompt de los 63 todos los
>   turnos (`curiana_sim/curiana_orchestrator_v2.py:161`):
>   `EJEMPLO: "Taya wana-ka arima wara kari. Ta-barsure naba-ni. [kali-bana:
>   kali+-bana = cerro del sol]."`
> - **`warawara`** es una voz de `VOCABULARIO_BASE`.
>
> Y `kali-bana` no se quedó en el registro: salió como **«adoptada en dos
> ámbitos»**, que es justamente la vía que la capa 2 de la escena hace posible
> y la que hay que ver nacer. El análisis del día
> (`5-experimento/analisis/serie_c_dia1_b7bc51dc.md` §1) demuestra que no viajó:
> sonó en dos lugares en el turno 1 y el primero en decirla lo hizo **antes** de
> que existiera la propuesta.

---

## 1. El motor ya sabe cuáles son

`_FORMAS_EXCLUIDAS` (`curiana_orchestrator_v2.py:178-183`) son **5.898 formas**:
`VOCABULARIO_BASE` + `formas_en_texto()` de las tres plantillas
(`_IDENTIDAD_LINGUISTICA`, `prompt_reglas_completo()`, `prompt_reglas_breve()`).
Se descuentan de la métrica emergente y del diccionario koiné **precisamente
para que copiar el prompt no cuente como koiné**. Lo que no hacen es impedir
que la forma se REGISTRE como neologismo, entre en evaluación, se adopte y
declare una vía.

`registrar_neologismo()` (`curiana_lexicon.py:7346`) la llama el **Observer**
(`curiana_observer.py:178`), que no se toca: es el registro de la medición. Por
eso el filtro tendría que ir dentro de `LexicoComunitario.registrar_neologismo`,
con una lista declarada `FORMAS_DE_PLANTILLA` construida desde las propias
plantillas — nunca escrita a mano.

## 2. La medición: sí mueve el instrumento

```bash
CURIANA_ELENCO=era2 python 6-fusion/scripts/medir_formas_de_plantilla.py
CURIANA_ELENCO=era2 python 6-fusion/scripts/medir_formas_de_plantilla.py --yaml
```

Re-ejecuta el pipeline del Observer sobre las **72 respuestas** del `b7bc51dc`,
en su orden, dos veces —con el filtro y sin él— y compara respuesta a respuesta.
No llama a la API ni importa el orquestador (`_IDENTIDAD_LINGUISTICA` se saca
con `ast`). Control: el replay reproduce lo que la base guardó en **72 de 72**.

Resultado (`6-fusion/medicion_formas_de_plantilla_2026-09-18.yaml`):

| | hoy | con el filtro |
|---|---|---|
| `neologisms_proposed` | — | **cambia en 0** respuestas |
| `score` | — | **cambia en 4** respuestas |
| `palabras_caquetias` | — | cambia en 7 |
| neologismos registrados | 39 | 37 |
| adoptados | 6 | 5 |
| adoptados en dos ámbitos | `['kali-bana']` | `[]` |

Las cuatro que se mueven: Buriche d1t4 **8,7 → 8,5**, Chuchubi d1t5
**8,0 → 7,6**, Karebe d1t6 **5,4 → 5,3**, Apoaure d1t6 **5,5 → 5,4**. Las cuatro
dicen `kali-bana`.

**Por qué se mueve.** `neologisms_proposed` sale de
`extraer_neologismos_del_texto()`, que es anterior al registro, y por eso no se
mueve nunca. `score` sí: `kali-bana` se **oficializa** durante el día (dos
adoptantes), y una forma adoptada entra en `lexico.palabras_activas()`, que es
justo lo que `score_linguistico()` reconoce. Rechazarla en la registración se la
quita a `palabras_caquetias` en las respuestas posteriores que la dicen.

## 3. La decisión que queda

**Regla dura: el scorer no se toca.** Así que el filtro **no se aplicó**. Las
opciones, para Miguel:

- **A.** Aplicarlo **en el corte de serie** (como `FORMA_DE_LA_ESFERA`, punto 6
  del cambio de instrumento): la serie C arranca con él y los días de la B
  quedan del otro lado. Cuesta: `score` de 4 de 72 respuestas del run de
  prueba, y `_FORMAS_EXCLUIDAS` deja de poder colarse por la puerta del
  registro.
- **B.** No aplicarlo y **medir la ausencia**: un guardián barato que afirme que
  ningún neologismo registrado está en `_FORMAS_EXCLUIDAS` fallaría hoy, así que
  sería un **aviso** al cerrar el run («N acuñaciones del día son formas que la
  plantilla enseña: …») en vez de un rechazo. No mueve nada y deja el dato a la
  vista.
- **C.** Dejarlo como está y descontarlo **en el análisis**, que es donde
  `_FORMAS_EXCLUIDAS` ya se aplica. Lo que sigue roto entonces es
  `adoptados_en_dos_ambitos()`: `via = "dos-ambitos"` puede nacer de una copia
  del prompt, y esa etiqueta es la evidencia que la escena tenía que producir.

## 4. Y una pregunta abierta que no es ésta

`curiana_observer.procesar_adopciones` recorre `lexico.neologismos_pendientes()`
**sin ámbito** (`curiana_lexicon.py:7418-7426`), y está declarado a propósito:
«lo que el ámbito filtra es lo que el agente VE (V1), no lo que puede adoptar».
Eso **no se cambió** y no se propone cambiarlo aquí. Pero es lo que permite que
`via = "dos-ambitos"` se escriba sin que nadie haya llevado nada: en el
`b7bc51dc`, Dakawa dijo `kali-bana` en `Carirubana:taller_canoas` por su cuenta
—V1 vacía, V2 vacía, campo 0,0, nada que oír, contagio 0,000— y quedó como
adoptante 1 de una propuesta de Moruy.

**La pregunta para Miguel**: ¿debe la adopción exigir que el adoptante
**pudiera ver** la propuesta (V1 en su ámbito, el bloque de oír, o el contagio),
y registrarse como **coincidencia** —una tercera vía, que es un dato y no un
error— cuando no la veía? Es la §1.6.5 del análisis del día 1, y es
independiente del filtro de plantilla: con el filtro aplicado, este run no
tendría el caso, pero el mecanismo seguiría ahí.

---

*Relacionado: `5-experimento/analisis/serie_c_dia1_b7bc51dc.md` (el análisis del
día 1; aún no está en `main`) · [[existir-en-el-mundo-escena-por-lugar-2026-09-17]]
· [[DISENO_KOINE]] · [[BITACORA_RUNS]] ·
`6-fusion/medicion_formas_de_plantilla_2026-09-18.yaml` ·
`6-fusion/scripts/medir_formas_de_plantilla.py`*
