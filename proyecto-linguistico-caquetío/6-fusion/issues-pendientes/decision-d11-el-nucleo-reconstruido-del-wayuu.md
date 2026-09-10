## D11 tiene una consecuencia que no se ejecutó: 23 entradas, y los pronombres enteros, se reconstruyeron desde el wayuu

Miguel, 2026-09-10:

> «Pero ojo, eso de caquetío reconstruido fue cuando lo hicimos desde el wayuu,
> pero luego establecimos que realmente el caquetío como lengua tiene más
> relación con el lokono y el achagua.»

Tiene razón, y corrige mi conclusión. Yo había escrito que la coincidencia
numerales-guajiro era «circular, no vale como prueba». Es verdad, pero se queda
corto: el problema no es solo que la prueba no valga, es que **la entrada misma
se hizo con la hermana que D11 jubiló**.

### Lo medido

De 68 entradas `caquetío-reconstruido`:

| Justificadas por | Cuántas |
|---|---|
| lokono | 26 |
| **wayuu / guajiro** | **23** |
| otra o sin declarar | 16 |
| taíno | 3 |

Las 23 son: `anüiki`, `apünüin`, `bana`, `jarai`, `kapua`, `kasha`, `kashi`,
`kira`, `naba`, `naya`, `nüma`, `pia`, `piama`, `pienchi`, `pütchi`, `sulu`,
`taya`, `tüshi`, `wana`, `wanee`, `wanü`, `waya`, `yama`.

### Y no son entradas cualquiera

Ahí está **el sistema pronominal completo** —`taya` yo, `pia` tú, `nüma`
él/ella, `waya` nosotros, `naya` ellos— y **los cinco numerales**. Son las
piezas que aparecen en *cada frase* que producen los 60 agentes, y las que
CLAUDE.md imprime en su bloque de morfología.

🔴 **No hay ni un solo pronombre caquetío atestiguado.** Los cinco son
reconstruidos, y los cinco son la forma wayuu: `taya`/`pia`/`nüma`/`waya`/`naya`
es, letra por letra, el paradigma del wayuunaiki.

### Qué dice el lokono

Contrastadas las 23 contra la capa lokono del lexicón (275 entradas):

- **apoya: 0**
- **discrepa: 9** — y los numerales son el caso claro: caquetío
  `wanee`/`piama`/`apünüin`/`pienchi` frente a lokono `aba`/`bian`/`kabyn`/
  `bithi`. Son dos sistemas distintos, no dos variantes.
- **el lokono de nuestro lexicón no cubre el concepto: 14**

⚠️ Ese 14 mide **nuestros datos**, no el lokono (regla 6). Para los pronombres
sí hay respuesta: el lexicón ya tiene `de` 'yo', `bi` 'tú', `we` 'nosotros', y
Perea 1942 los confirma (`dai`, `bui`, `wai`, esta última 231 veces).

Así que la elección es concreta:

| | 1ª sg | 2ª sg | 1ª pl |
|---|---|---|---|
| hoy (wayuu) | `taya` | `pia` | `waya` |
| D11 (lokono) | `de` / `dai` | `bi` / `bui` | `we` / `wai` |

### Lo que hay que pesar antes de tocar nada

**A favor de cambiar**: D11 decidió que el wayuu deja de ser la hermana por
defecto. Si el núcleo del habla sigue siendo wayuu, D11 está decidida en el
papel y sin ejecutar en el código. Y los datos nuevos empujan en la misma
dirección: de 381 conceptos del vocabulario guajiro de Jahn, donde se puede
comparar el caquetío casi nunca se parece.

**En contra de cambiar**: el precio es alto y hay que decirlo.

1. **Rompe la comparabilidad con todos los runs anteriores.** Cada
   `agent_response`, cada `word_use`, cada métrica de koiné de la base está
   medida sobre el paradigma actual. Un cambio de pronombres no es una entrada
   más: es otra lengua.
2. **`score_linguistico()` se mueve**, y con él todo el instrumento.
3. **Y no es que la reconstrucción wayuu fuera ilegítima.** Con cero pronombres
   atestiguados, hay que poner algo. El wayuu es una arahuaca del área, vecina
   y bien documentada. Lo que D11 cambia no es que fuera un disparate: es que
   ya no puede ser la opción **por defecto y sin declarar**.

### Tres salidas

1. **Re-etiquetar sin tocar las formas** *(mi recomendación)*. Las 23 entradas
   se quedan como están, pero su `notas` dice qué son: «reconstruida desde el
   wayuu ANTES de D11; el lokono da X; se conserva por continuidad
   experimental». Nadie vuelve a contarlas como evidencia de nada, los runs
   siguen comparables, y la deuda queda visible en vez de enterrada. Cuesta una
   tarde.
2. **Re-derivar el núcleo desde el lokono** y aceptar el corte experimental:
   los runs de antes y los de después no se comparan, y se declara. Es lo
   coherente con D11 llevado hasta el final, y es caro.
3. **Las dos, por perfil.** Ya existe la maquinaria: `perfiles_de_run.yaml`
   controla qué capas ve el agente. Un perfil `lokono` con el núcleo
   re-derivado, frente al `base` actual, convierte la pregunta en un
   experimento medible en vez de en una decisión a ciegas. Es lo más caro de
   montar y lo único que **responde** en vez de elegir.

⚠️ Nota aparte sobre `bana`: está en la lista de las 23, pero hoy Esteves lo
glosó 'cerro' sobre el topónimo Caracubana. Esa entrada puede salir de la deuda
por la vía buena —atestación— antes que por la de la re-derivación.

Medición: `6-fusion/scripts/medir_deuda_d11.py`. Registro:
`6-fusion/jahn_vocabularios_comparados.yaml`.
