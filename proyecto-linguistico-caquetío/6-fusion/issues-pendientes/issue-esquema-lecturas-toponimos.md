El registro de topónimos necesita una tercera voz: la de la tradición

## El problema

`2-lengua/toponimos.yaml` define cada topónimo con dos voces:

1. **`glosa_fuente`** — lo que la fuente impresa dice (Zavala, Esteves).
2. **`segmentacion` + `glosa_reconstruida`** — nuestro análisis morfémico.

**No hay dónde poner la tercera voz: lo que la etimología culta y la
coloquialidad local reconocen y comentan.** Todo lo que la sesión del
2026-08-25 acumuló de esa clase quedó huérfano en YAMLs de `6-fusion/`, sin
colgar del topónimo al que pertenece:

- González Batista sobre *Coriana* = 'tierra de las espinas' y *Paraguaná* =
  'tierra rodeada de mar';
- el testimonio de Miguel como residente sobre *Judibana* = 'el cerro del
  viento';
- las tradiciones que recoge Morón (Piedras de Martín, La Cuiba);
- la etimología caribe insular de *Maitiruma* = 'manantial azul' (Esteves);
- las etimologías populares tipo Wikipedia ("conuco entre el mar").

Cada una tiene valor distinto y **ninguna puede ocupar `glosa_fuente`** sin
mentir. El resultado: o se pierden, o contaminan un campo que no les toca.

## La propuesta: campo `lecturas` (lista, opcional)

```yaml
- id: toponimo-XXX
  forma: judibana
  # ... campos actuales intactos ...
  lecturas:
    - tipo: etimologia-analitica
      lectura: "judi (~juri 'viento', Zavala #178) + bana ('cerro', Zavala #26) = 'el cerro del viento'"
      quien: proyecto
      fecha: 2026-08-25
      apoyo: "alternancia j~ju documentada en la fórmula de Mitare (cudan~judan)"
    - tipo: testimonio-residente
      lectura: "el viento es el rasgo dominante del sitio; judi y juri son la misma palabra deformada"
      quien: "Miguel Gil Urbina, residente"
      fecha: 2026-08-25
    - tipo: tradicion-local
      lectura: "..."
      quien: "..."
      procedencia: {obra: ...}
```

### Los tipos, con su peso declarado

| `tipo` | Qué es | Peso |
|---|---|---|
| `glosa-fuente` | duplicado explícito de `glosa_fuente` cuando hay más de una fuente con glosas distintas | el más alto |
| `etimologia-analitica` | segmentación con morfemas atestiguados (la nuestra o la de un autor) | según sus apoyos |
| `testimonio-residente` | hablante/residente actual, con nombre | categoría propia, como el dictado curado |
| `tradicion-local` | lo que la comunidad del sitio dice (Morón, cronistas locales) | `retro-abstraido` |
| `etimologia-popular` | tradición recibida sin fuente citable (Wikipedia, blogs) | la más baja; se registra para no re-investigarla |

### Las reglas

1. **Ninguna lectura pisa a otra.** Conviven; el campo es una lista.
2. **Toda lectura declara `quien` y, si existe, `procedencia`.** Sin autor no
   entra — es la regla 8 aplicada a opiniones.
3. **`glosa_fuente` no cambia de significado**: sigue siendo solo lo impreso
   en la fuente primaria del registro.
4. Cuando dos lecturas chocan (como *Jurijurebo* 'paso de los vientos' vs.
   'lugar de arenales'), **las dos quedan** — con el veredicto en `razon` si
   ya se falló, como se hizo el 2026-08-25.

## Por qué ahora

La campaña de clasificación de topónimos de Falcón (decidida el 2026-08-25)
va a producir lecturas de las tres clases en volumen: Esteves tiene **186
nombres en su índice y solo 4 están en el canon**
(`6-fusion/toponimos_esteves_indice.yaml`), Brett Martínez viene en camino con
etimologías locales, y González Batista ya dejó una docena. Sin el campo,
cada una habrá que aparcarla en un YAML suelto y perderá la conexión con su
topónimo — que es exactamente lo que pasó hoy.

Es el mismo movimiento que el issue de repertorio-vs-filiación, aplicado a
topónimos: **varias voces, cada una etiquetada, ninguna silenciada.**

## Trabajo que implica

1. Añadir `lecturas` al esquema y a la validación de `compilar_lengua.py`
   (campo opcional — no rompe nada existente).
2. Retro-poblar las lecturas de la sesión del 2026-08-25 (~15 lecturas ya
   escritas en `6-fusion/toponimia_coro_espina.yaml`,
   `lengua_toponimia_quibacoa.yaml` y `petroglifos_y_manaure.yaml`).
3. Usarlo como formato de salida de la campaña de Falcón.

Relacionado: #109 · #38 (D9) · #92 · el issue de repertorio-vs-filiación.
