## El último de la categoría — pero con menos evidencia que sus hermanos

Contexto medido el 2026-08-24 (`curiana_sim/auditar_glosas_sin_fuente.py`,
que queda en el repo): en las **1.413 entradas del lexicón**, las que tienen una
nota admitiendo *"glosa sin fuente localizada"* o *"conflicto de glosa abierto"*
son **exactamente tres**:

| Entrada | Glosa activa | Estado |
|---|---|---|
| `tara` | venado, ciervo | resuelta — [#45](https://github.com/miguelgilurbina/curiana-radio/issues/45), tres fuentes dicen **langosta** |
| `corie` | choza, habitación | resuelta — [#46](https://github.com/miguelgilurbina/curiana-radio/issues/46), tres fuentes dicen **armadillo** |
| **`saruro`** | árbol saruro | **este issue — el último que queda** |

D10 las llamó *"los tres conflictos"* y eran literalmente tres. Cerrando este,
**la categoría queda en cero**.

## ⚠️ Pero aquí la evidencia es más fina, y conviene decirlo

`tara` y `corie` se resolvieron con **tres fuentes independientes** cada una.
`saruro` no tiene eso:

- **Comprobado el 2026-08-24: `saruro` NO aparece en la Tabla A-9 de Oliver**
  (*Selected Caquetío Vocabulary from the XVIth Century*), leída entera. Oliver
  **no aporta nada** a este caso.
- Sigue siendo **Zavala #224 (E) «Serpiente no venenosa. Boa constrictora»**
  contra una glosa activa cuyo único rastro, según su propia nota, es *"una
  lista de Notion citada en DISENO_KOINE §8, y allí se usa para confirmar la
  terminación `-aro/-uro`, **NO para sostener la glosa**"*.

El marcador no es 3-0 sino **1-0**. Una fuente sigue siendo infinitamente más
que ninguna, pero la decisión no es tan automática como las otras dos, y el
issue merece cerrarse sabiéndolo.

## Un apoyo lateral que sí es nuevo

La lectura completa de la Tabla A-9 dio **tres palabras en `-ure` que nombran
seres vivos u objetos, no lugares**: `bisure` (lagartija), `chaure` (búho),
`maure` (tejido de algodón). Se suman a los contraejemplos que `morfemas.yaml`
ya declaraba (`guasare` árbol, `chunare` mazorca).

`saruro` comparte esa terminación. Eso **no dice qué significa**, pero sí que
la terminación es compatible con un animal — y la lectura 'boa' deja de ser
morfológicamente rara. (El uso que hace `DISENO_KOINE` §8 de la palabra, para
confirmar `-aro/-uro`, sigue siendo válido con cualquiera de las dos glosas:
ese argumento no depende de qué significa.)

Y ecológicamente no hay obstáculo: la boa constrictora existe en las zonas
áridas del noroccidente venezolano.

## Qué habría que decidir

1. ¿Se reescribe la glosa a **'boa, serpiente no venenosa'** (Zavala #224), o
   se degrada la actual a `hipotetico` a la espera de una segunda fuente?
2. La razón por la que D10 no la tocó —*"saruro da nombre a la agente
   **Saruro-sha** y aparece en el vocabulario de Shaboro"*— es de coste, no de
   evidencia. Vale aquí lo mismo que en #46: **el personaje se llama igual con
   cualquiera de las dos glosas**. Lo que cambia es qué significa su nombre — y
   "la del árbol" frente a "la de la boa" no son equivalentes para un
   personaje.
3. Si se cambia: revisar el vocabulario de Shaboro y la ficha de Saruro-sha
   para que nombre y significado digan lo mismo.
4. Y si se conserva 'árbol': hay que **decir de dónde sale**, porque hoy el
   propio lexicón admite que no lo sabe.

Fuente de la medición: `curiana_sim/auditar_glosas_sin_fuente.py`
