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

## Lo que falta

1. **Migrar `corpus` y `lexicón` a `procedencia.obra`.** Es lo que haría exactas
   las cuatro columnas y cerraría el círculo.
2. **Cambiar los consumidores.** `arahuaco_comparative.COGNADOS` todavía
   alimenta `transducir()` desde el Python; el YAML existe pero nadie lo lee aún.
   Antes de cambiarlo hay que congelar la salida actual con un test.
3. **Decidir el caso `para`** y qué hacer con `quiripa`.

## Enlaces

[[lexicon]] · [[toponimia]] · [[metodo-comparativo]] · [[oliver-1989-cap2]] · [[ARQUITECTURA]] · [[HARNESS]]
