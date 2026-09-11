---
tipo: nota
pregunta: "¿Dónde viven los cognados y los topónimos, y por qué ahí?"
datos: [cognados.yaml, toponimos.yaml, morfemas.yaml]
validador: curiana_sim/compilar_lengua.py
medido: 2026-08-06
---

# Los datos de lengua — cognados, topónimos, morfemas

> Todo lo de aquí se comprueba con `python curiana_sim/compilar_lengua.py`.

## El cambio de fondo: citar pasa a ser comprobable

Hasta ahora una cita era **texto libre**: `"Oliver 1989, cap. 3, p. 255"`. Nadie
verificaba que esa obra existiera, ni que dos entradas que citan lo mismo lo
escribieran igual.

Con [[bibliografia|4-fuentes/bibliografia.yaml]], `procedencia.obra` es una
**clave foránea** y el validador la comprueba. La cita deja de ser una promesa y
pasa a ser una comprobación.

```yaml
procedencia: {obra: oliver-1989-cap2, pagina: 142, ancla: "the toponym bari-si-ki-meto"}
```

Y cuando no hay fuente, **hay que decirlo**:

```yaml
procedencia: null
deuda: sin-procedencia
```

Un hueco declarado es dato; un hueco callado es una cita que no existe. El
validador rechaza lo segundo.

## Cognados: había dos almacenes, y el bueno no se usaba

| | `COGNADOS` | `COGNADOS_OLIVER` |
|---|---|---|
| entradas | 37 | 16 |
| procedencia | **ninguna, 0 de 37** | página, ancla, confianza, duda del autor |
| lo usaba el motor | **sí** | no |

El set que alimentaba `transducir()` y `reconstruir_caquetio()` no citaba nada;
el que traía la página de Oliver —y hasta un campo para las dudas del propio
Oliver— solo lo leía su minador. Estaba al revés.

Ahora es uno: `cognados.yaml`, **51 cognados**, 16 con procedencia y 35 con la
deuda declarada.

### Tres decisiones de forma

1. **Las lenguas son un mapa abierto**, no casillas fijas. Antes había `KL` en
   un almacén, `PJ`/`CAIC` en el otro, y un dict `otros` como vía de escape para
   todo lo demás: tres soluciones al mismo problema. Ahora hay una.

   La distinción que sí importa es otra: los **códigos en mayúscula** (PA, CQ,
   WY, LK, TN, KL, PJ, CAIC) son el núcleo sobre el que existen reglas de
   transducción, y uno inventado ahí rompería `transducir()` en silencio — el
   validador los vigila. Los **nombres en minúscula** son comparanda citada
   (maipure, baré, wapishana, tariana… unas 24 lenguas arahuacas) y son libres a
   propósito: cerrar esa lista obligaría a tocar el esquema cada vez que una
   fuente cita una lengua nueva.

2. **El id no es la glosa española.** Antes la clave era la glosa, y por eso
   existía `rojo_almagre`: un desempate inventado para no chocar con `rojo`.

3. **Lo que no es un cognado, no se llama cognado.** Dos entradas tenían una
   sola lengua, así que no son relaciones. No se borraron —van a
   `no_son_cognados` con su diagnóstico— porque no son el mismo caso:
   - `baruwa` (KL, 'hombre') **ya está en `VOCABULARIO_BASE`**: aquí sobra.
   - `quiripa` (CQ, concha-moneda) **no está en ninguna otra parte**: este
     registro es su única constancia en el repo. Retirarlo perdería el dato.

### Lo que queda abierto

**`para` ('mar') estaba en los dos almacenes**, y las dos versiones son
complementarias, no idénticas:

| | Oliver (`cognado-016`) | curado (`cognado-019`) |
|---|---|---|
| aporta | procedencia (p.150), `TN bara-wa` | `LK bara`, `KL barana` |
| dice del taíno | `bara-wa` | `bagua` |

La propia nota de Oliver lo señala: *"Oliver aporta TN bara-wa, más cercano a
bara que bagua"*. **Fusionarlas exige decidir cuál forma taína vale**, y eso es
filología, no script. El validador lo reporta como aviso y ahí se queda.

## Topónimos: el nivel era un campo disfrazado de tres contenedores

`lexicon_toponimos.py` tenía **doce contenedores** para tres entidades y un poco
de prosa. Para listar todos los topónimos había que unir `NIVEL_A`, `NIVEL_B` y
`NIVEL_C`; añadir un nivel significaba crear un contenedor.

Ahora: `toponimos.yaml` con **74 topónimos** y `nivel` como campo
(A=6, B=8, C=13, descartado=47), más `morfemas.yaml` con los 10 formantes.

Dos cosas que salieron al desarmarlo:

- **`ANTROPONIMOS` no contenía antropónimos**: contenía `total`,
  `con_glosa_descriptiva`, `resueltos`, un `detalle` anidado con los datos y dos
  campos de prosa (`veredicto`, `consecuencia`). Dato, recuento y opinión en la
  misma estructura. La prosa se queda en [[toponimia]]; un YAML no es sitio para
  un veredicto.
- **`TOTALES` declaraba `nivel_D: 47`** y ningún contenedor se llamaba así. El
  número era correcto —47 es lo que expande `DESCARTES`—, pero apuntaba a un
  nombre inexistente. Que la migración reproduzca los totales declarados
  (74 procesados, 6/8/13/47) confirma que es fiel.

Y el módulo entero, 739 líneas de análisis curado, **no lo importaba nadie**.

## Qué sostiene cada obra, y la asimetría que enseña

`medir_sostiene.py` cuenta el rastro de cada obra en las **cuatro esferas**:
lexicón, corpus, cognados y topónimos.

| Esferas que alimenta | Obras |
|---|---|
| tres | 2 — `oliver-1989-cap2`, `zavala-reyes-2015` |
| dos | 6 |
| **una sola** | **18** |
| ninguna | 4 |

**Dieciocho de treinta obras dejan rastro en una sola esfera.** Parte es real
—un paper de genética no da topónimos— pero parte es que la minería se hacía
con el lexicón en la cabeza y lo demás caía donde cayera.

Y el `sostiene` del frontmatter, que se mantiene a mano, **ha derivado en 17 de
30 obras**. Ejemplos: Alvarado declara 0 entradas de lexicón y se miden 22; van
Buurt declara 0 y se miden 14; Oliver cap. 2 declara 2 hechos de corpus y se
miden 16.

> ⚠️ Esas dos columnas se miden por coincidencia del apellido sobre texto libre,
> así que fallan **en las dos direcciones**: por defecto si la cita está escrita
> de otra forma, por exceso si el apellido sale en prosa sin ser cita. Son
> estimación, no cuenta. Cognados y topónimos sí son exactos, porque van por
> clave foránea — que es justamente el argumento para migrar también corpus y
> lexicón a `procedencia.obra`.

## El corpus, a medio migrar — y por qué a medias a propósito

`migrar_corpus_procedencia.py` derivó la obra desde la `referencia` en prosa de
los 161 hechos. Resultado:

| | n | Qué pasa |
|---|---|---|
| citan **una** obra → migrados | **58** | `procedencia: {obra: …}` añadida |
| citan **varias** → sin decidir | 38 | es la cadena de custodia, ver abajo |
| sin obra reconocible | 65 | web, analogías, reconstrucciones |

Los 38 ambiguos **no son un fallo del script**: son la cadena de custodia real
del proyecto. `creencia-001` cita Arcaya, Jahn **y** Oviedo y Valdés porque el
dato es de Oviedo y llega *vía* los otros dos. Elegir una por frecuencia
falsearía justo lo que el proyecto más cuida. Necesitan un `procedencia` con
`obra` + `via`, y decidir cuál es cuál es lectura, no script.

> 📌 **La `referencia` en prosa no se toca, y no es transitorio.** Dice cosas
> que un id no puede: la página, la cita textual, el «vía tal». Los dos campos
> conviven — uno es para leer, el otro para comprobar.

⚠️ Nota de método: la primera versión de la migración cargaba y volvía a volcar
el YAML con `yaml.safe_dump`, y **reformateaba los archivos enteros** — los
bloques `>` de `contenido` se volvían cadenas entrecomilladas y los comentarios
de cabecera desaparecían. Sobre datos de investigación curados eso es
inaceptable. La versión buena inserta el bloque **como texto**: el diff son 58
inserciones y **cero borrados**.

## Topónimos: la tercera voz — `lecturas` (2026-09-05)

Un topónimo tenía dos voces: `glosa_fuente` (lo impreso en la fuente del
registro) y `segmentacion` + `glosa_reconstruida` (nuestro análisis). Lo que un
residente, la tradición del sitio, un cronista o un autor con etimología propia
dicen del nombre no cabía en ninguna de las dos sin mentir, y se aparcaba en
`6-fusion/` sin colgar del topónimo al que pertenece. Desde el 2026-09-05
cuelga de él:

```yaml
- id: toponimo-001
  forma: jurijurebo
  # ... glosa_fuente, segmentacion, razon: intactos ...
  lecturas:
    - tipo: etimologia-analitica
      lectura: "hure 'arena' -> hurehure 'arenal' -> hurehurebo 'lugar de muchos arenales'"
      quien: González Batista
      fecha: 2026-08-25
      eje: significado
      procedencia: {obra: gonzalez-batista-nombre-de-coro}
      veredicto: "descartada como lectura principal (2026-08-25): Zavala tiene glosa impresa…"
    - tipo: testimonio-residente
      lectura: "Jurijurebo está en Judibana; judi y juri son la misma palabra deformada"
      quien: Miguel Gil Urbina, residente en Judibana
      fecha: 2026-08-25
      eje: referente
  definicion_aceptada_simulacion:      # solo cuando la simulación lo necesita
    definicion: "…"
    quien: Miguel
    fecha: 2026-09-01
    etiqueta: canon-simulacion         # nunca atestiguado: el validador lo rechaza
    validacion: "(Claude) la probabilidad, y por qué"
```

### Los tipos, con su peso declarado

| `tipo` | Qué es | Peso |
|---|---|---|
| `glosa-fuente` | otra fuente impresa con glosa distinta a la del registro | el más alto |
| `etimologia-analitica` | segmentación con morfemas atestiguados, nuestra o de un autor | según sus apoyos |
| `etimologia-de-cronista` | la glosa que da un cronista (Castellanos: «Coro viento quiere decir») | pista, no atestación |
| `testimonio-residente` | hablante o residente actual, con nombre | categoría propia, como el dictado curado |
| `tradicion-local` | lo que la comunidad del sitio dice (Morón, cronistas locales) | `retro-abstraido` |
| `etimologia-popular` | recibida sin fuente citable (Wikipedia, blogs) | la más baja; se registra para no re-investigarla |
| `hipotesis` | una lectura propuesta para validar; la validación queda como rastro | la que le dé la validación |

### Las reglas

0. **Significado ≠ referente** (principio de Miguel, 2026-08-25): qué significa
   el nombre y a qué o a quién nombra son ejes independientes. Cada lectura
   puede declararlo en `eje` (`significado`, `referente`, `ambos`).
1. **Ninguna lectura pisa a otra.** Es una lista; conviven.
2. **Toda lectura declara `quien` y `fecha`; si cita, `procedencia.obra` se
   comprueba contra la bibliografía.** Sin autor no entra: es la regla 8
   aplicada a opiniones.
3. **`glosa_fuente` no cambia de significado**: sigue siendo solo lo impreso
   en la fuente primaria del registro.
4. **Cuando dos lecturas chocan, las dos quedan**, con el `veredicto` si ya se
   falló (jurijurebo: 'paso de los vientos' vs. 'lugar de arenales').
5. **`definicion_aceptada_simulacion` lleva `etiqueta: canon-simulacion`
   obligatoria.** Es la capa de decisión (Miguel, 2026-09-01): una lengua
   muerta exige posturas y el proyecto las declara, sin llamarlas atestiguadas.

### Dónde se escriben y quién las lee

Se escriben en `curiana_sim/lexicon_toponimos.py`, la propuesta curada a mano,
de donde `migrar_toponimos.py` las vuelca a `toponimos.yaml` y las cuenta en
`meta`. `compilar_lengua.py` las valida (tipos cerrados, autor y fecha, obra
citada). `juntar_toponimos.py` las muestra en `6-fusion/TOPONIMOS_POR_FUENTE.md`
junto a las demás fuentes, firmadas por quien las hizo. Una lectura que
rehabilita un `descartado` se registra al subirlo de nivel, que es la decisión.
Las lecturas que todavía viven en `6-fusion/` sin colgar de su topónimo se
listan en `issues-pendientes/issue-esquema-lecturas-toponimos.md`.

## Lo que falta

1. **Los 38 ambiguos**, con un `procedencia` que exprese la cadena
   (`obra` + `via`).
2. **El lexicón a `procedencia.obra`.** Es el que más entradas tiene (1413) y
   el que peor se mide hoy por apellido.
3. **Cambiar los consumidores.** `arahuaco_comparative.COGNADOS` todavía
   alimenta `transducir()` desde el Python; el YAML existe pero nadie lo lee aún.
   Antes de cambiarlo hay que congelar la salida actual con un test.
4. **Decidir el caso `para`** y qué hacer con `quiripa`.

## Enlaces

[[lexicon]] · [[toponimia]] · [[metodo-comparativo]] · [[oliver-1989-cap2]] · [[ARQUITECTURA]] · [[HARNESS]]
