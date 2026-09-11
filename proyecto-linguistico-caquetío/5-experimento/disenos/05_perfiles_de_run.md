---
tipo: diseno
ambito: parametrizar cada simulación como un objeto declarado
estado: propuesta
fecha: 2026-09-09
pedido_por: Miguel
---

# Perfiles de run: que cada simulación diga con qué se corrió

> **Miguel, 2026-09-09:** *«Sería interesante que nuestra arquitectura pueda
> dejar definido los parámetros de cada simulación. Porque así como podemos
> hacer una run base, luego podemos hacer una run con palabras atestiguadas y
> otra más suelta con palabras intuidas o no atestiguadas pero que entran dentro
> de la fonemia caquetía y que conseguimos por coloquialidad.»*

## Lo primero: esto disuelve una decisión abierta

Ayer dejé en el tablero un dossier —`decision-era2-retroabstraido.md`— que
preguntaba si las voces retro-abstraídas de Medina deben entrar al habla, con
tres opciones y una recomendación.

**La pregunta estaba mal planteada, y esta idea lo enseña.** Si la capa léxica
es un *parámetro de run*, no hay que decidir de una vez si las voces intuidas
entran: se corre un brazo con ellas y otro sin ellas, **y se mide la
diferencia**. Que es exactamente lo que el proyecto ya hace con `--ablacion`
para el andamiaje de convergencia.

La decisión pasa de ser *«¿las metemos?»* a *«¿qué queremos medir con ellas?»*,
que es una pregunta mucho mejor y que además produce un resultado publicable.

## Lo que ya existe, y es más de lo que parece

| Pieza | Estado |
|---|---|
| `simulation_runs.config` como **jsonb consultable** | ✅ existe, y con la corrección ya hecha de guardarlo como objeto y no como string (`config->>'clave'` funciona en SQL) |
| Un brazo de control declarado (`--ablacion`) | ✅ existe, y con su razón escrita: separar convergencia emergente de inducida |
| Seis flags de CLI (`--auto`, `--anio`, `--reporte`, `--silencioso`, `--perfiles`, `--ablacion`) | ✅ existen, pero **sueltos**: hay que acordarse de la combinación |
| El filtro de capa léxica | ❌ **no existe**. El muestreador del prompt tiene cableado `!= "caquetío"`, y ahí se acaba |

O sea: falta poco, y lo que falta es lo importante.

## El diseño

### 1. Dos ejes ortogonales, y no mezclarlos

Esto es lo que hay que ver antes de escribir una línea:

- **Eje A — qué lengua ven los agentes.** Qué capas epistémicas del lexicón
  entran al prompt. Es lo que Miguel propone.
- **Eje B — cuánto andamiaje de convergencia hay.** Sugerencias de contagio,
  competencias abiertas, muestreo ponderado. Es lo que hoy apaga `--ablacion`.

Son independientes y **hay que poder cruzarlos**: un run `suelto` con andamiaje
y otro `suelto` sin él son dos experimentos distintos. Si se colapsan en un solo
flag, se pierde la mitad del diseño experimental.

### 2. Los perfiles, en datos y no en código

`5-experimento/perfiles_de_run.yaml`. Datos, versionados en git, diffeables en
PR — la misma lógica con que `ARQUITECTURA.md` pide sacar el lexicón a YAML.

```yaml
perfiles:
  base:
    descripcion: "Como se corrió la era 1. La línea de comparación."
    capas_lexicas: [caquetío-atestiguado, caquetío-reconstruido, caquetío-hipotético]
    andamiaje: completo

  atestiguado:
    descripcion: "El brazo duro: sólo lo que una fuente colonial o toponímica sostiene."
    capas_lexicas: [caquetío-atestiguado]
    andamiaje: completo

  suelto:
    descripcion: >-
      El brazo de la coloquialidad: suma lo que la tradición oral sostiene
      aunque no podamos atestiguarlo como caquetío. Medina.
    capas_lexicas: [caquetío-atestiguado, caquetío-reconstruido,
                    caquetío-hipotético, caquetío-retroabstraido]
    andamiaje: completo

  control:
    descripcion: "Ablación: base sin las inyecciones que empujan convergencia."
    capas_lexicas: [caquetío-atestiguado, caquetío-reconstruido, caquetío-hipotético]
    andamiaje: ninguno
```

Y `--perfil <nombre>`, que se resuelve y **se escribe entero en
`simulation_runs.config`**. No el nombre: el perfil resuelto. Así un run de hace
seis meses sigue diciendo con qué se corrió aunque el perfil haya cambiado
después.

### 3. Lo único que hay que construir

El **filtro de capa léxica**. Hoy el muestreador del prompt tiene esto cableado:

```python
if normalize_source_language(datos.get("fuente", "")) != "caquetío":
    continue
```

Pasa a consultar las capas activas del perfil. Es un cambio pequeño y en un solo
sitio — que es justamente lo que la medición del 2026-09-09 dejó claro: **el
muestreador es el único punto por donde el vocabulario llega al hablante**. Por
eso las 1.201 entradas de comparanda no contaminan nada.

### 4. 🔴 La trampa: el score tiene que medirse igual en todos los brazos

Si el brazo `suelto` cuenta las retro-abstraídas como caquetío y el brazo
`atestiguado` no las tiene, **los scores no son comparables** y la diferencia
que midamos será un artefacto del instrumento, no del habla.

La salida es separar el vocabulario que el agente **ve** del vocabulario con que
se le **puntúa**:

- `capas_lexicas` → qué entra al prompt (varía por perfil).
- `capas_de_score` → contra qué se puntúa (**fijo en todos los perfiles**).

Con eso, un run `suelto` que use muchas voces retro-abstraídas puntuará *más
bajo* que uno `atestiguado`, y esa caída **es el dato**: dice cuánto del habla
emergente se apoya en material que no podemos atestiguar. Si en cambio dejamos
que el score se mueva con el perfil, esa señal desaparece dentro del instrumento.

Es la misma lección de la fase 1 que ya está escrita en el repo: *«el instrumento
medía en parte a sus autores»*.

### 5. El guardián

Un test que exija que **todo run publicado tenga su perfil resuelto en
`config`**. Sin eso, dentro de seis meses habrá runs de los que nadie sepa con
qué lexicón se corrieron — que es exactamente el problema que este diseño viene
a evitar.

## Qué habilita, en concreto

Tres runs de la era 2 con la misma semilla y los mismos nodos:

| Brazo | Pregunta que responde |
|---|---|
| `atestiguado` | ¿Alcanza el caquetío que podemos probar para que una comunidad hable? |
| `base` | ¿Qué cambia al añadir lo reconstruido por método comparativo? |
| `suelto` | ¿Qué cambia al añadir lo que sólo sostiene la tradición oral? |

Y la comparación entre el segundo y el tercero es, literalmente, **la medida del
aporte de Medina Colina al habla**. Que es la pregunta que el dictado abrió y
que hasta ahora no teníamos cómo contestar.

## Coste

Medio día para el filtro, el cargador de perfiles y el test. El grueso ya está:
el `config` jsonb, el precedente de `--ablacion` y el punto único de filtrado.

## Orden sugerido

1. Este diseño, porque define la forma del resto.
2. El refactor del lexicón a `lexicon/*.yaml` por capa epistémica
   (`ARQUITECTURA.md` ítem 3) — que con este diseño deja de ser higiene y pasa a
   ser el habilitador: si las capas son ficheros, el perfil es una lista de
   ficheros.
3. Las nueve piezas de la era 2.

## Enlaces

[[ARQUITECTURA]] · [[DISENO_ERA2]] · [[04_protocolo_run_1_era_auditada]] · [[BITACORA_RUNS]]
