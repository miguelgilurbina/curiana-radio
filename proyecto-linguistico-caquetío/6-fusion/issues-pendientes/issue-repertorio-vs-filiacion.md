El lexicón responde "¿de qué lengua es esta palabra?" y lo usamos como si respondiera "¿la usaba un caquetío?"

## El problema, en una palabra

`caney` está en `VOCABULARIO_BASE` como **`fuente: taíno`**. Eso es correcto: el étimo es taíno.

Pero el proyecto lo lee como *"no es caquetío, fuera"*. Y [[antolinez-1946-hacia-el-indio]] dice, describiendo la vivienda:

> "el **caney** o casa de dos aguas, algunas veces en piernas y otras con paredes deleznables, es **la forma corriente entre los kaketío** y akáwa de las regiones bajas."

Las dos cosas son verdad a la vez. **Son preguntas distintas y el campo `fuente` solo contesta una:**

| Pregunta | Qué contesta hoy |
|---|---|
| ¿De qué lengua viene esta palabra? | ✅ `fuente` |
| ¿La tenía un hablante caquetío en su repertorio? | ❌ **nada** |

El campo hace filiación etimológica. Lo usamos como si hiciera adscripción de uso. Eso no es un detalle de etiquetado: es la diferencia entre reconstruir una lengua y reconstruir a un hablante.

## Por qué importa: la evidencia ya está en el repo

No hace falta suponerlo. Todo esto entró al vault en la sesión del 2026-08-25, de fuentes distintas, sin que nadie lo estuviera buscando:

- **Corresidencia**: en Hacarigua, caquetíos y **cuibas** —familia guahibo, ni arahuaca ni caribe— *"viven junto y entremezclados"* (Federmann).
- **Mercado interétnico**: caquetíos y guayqueríes *"en paz en el mismo territorio porque se necesitan mutuamente"*, cambiando pescado por frutas (Federmann).
- **Circulación antillana**: los kaketíos *"habitaron las Antillas, Curazao, Aruba y Bonaire, y **comerciaron en grande con la restante zona taína**"* (Antolínez 1946).
- **Deportación forzada**: indios de la gobernación llevados *"a Puerto Rico e a la ciudad de Santo Domingo"* (Relación de Nueva Segovia).
- **Retorno**: los cautivos rescatados por Juan de Ampíes en Santo Domingo *"luego, en su mayoría regresarían a Curazao y Paraguaná"* (Brito Figueroa).
- **Continuo dialectal vecino**: los achaguas, *"más de veinte naciones o provincias bajo un mismo idioma"* (Rivero).
- **Bilingüismo documentado en la otra dirección**: tres españoles salieron *"lenguas excelentes"* del trato con caquetíos (Castellanos).

Un pueblo de comerciantes, en un archipiélago de contacto, con deportaciones y retornos hacia y desde las Antillas taínas. **La hipótesis por defecto no puede ser el monolingüismo.**

## 🔴 Y la consecuencia que va más allá del lexicón

Esto no toca solo etiquetas. Toca la métrica central del experimento.

`CLAUDE.md` describe `score_linguistico()` así:

> "El objetivo del proyecto es que el caquetío **DOMINE** — no basta con 'no hablar español'; **hablar wayunaiki en vez de caquetío también es una fuga**, solo que más sutil."

Si el argumento de arriba es correcto, **eso no es una fuga: es la norma histórica**. La métrica codifica pureza monolingüe como objetivo, y la sociedad que modelamos no funcionaba así.

Toca directamente:
- **#69** — `pct_caquetio` saturada al 91 % y `avg_score` plana. Puede que el problema no sea solo de calibración: puede que esté midiendo la variable equivocada.
- **D11 (#39)** — el desbalance wayunaiki/lokono deja de ser un defecto y pasa a ser una pregunta distinta: ¿qué proporción del **repertorio** de un hablante era de cada lengua?
- **[[DISENO_KOINE]]** — si la convergencia se mide contra un caquetío puro que nunca existió, el veredicto de koineización mide nuestra idealización.

⚠️ **Contra-argumento honesto, y hay que ponerlo**: el experimento estudia la *emergencia de una variedad*. Si los agentes hablan una mezcla libre, no hay convergencia medible y no hay experimento. Simplificar hacia la pureza puede ser una **decisión de modelado legítima** — pero entonces debe estar **declarada como decisión**, no dada por hecho histórico. Hoy `CLAUDE.md` la enuncia como si fuera lo segundo.

## Propuesta: separar los dos ejes

**Un campo nuevo, `repertorio`, junto al que ya existe.**

```yaml
caney:
  etimo: taíno              # lo que hoy hace `fuente` — de dónde viene
  repertorio: caquetio-probable   # NUEVO — si un hablante caquetío la usaba
  repertorio_razon: >-
    Antolínez 1946 la reporta como la vivienda corriente entre los kaketío de
    las tierras bajas. Circulación antillana documentada en ambos sentidos.
```

Marcas de `repertorio`, con la misma disciplina epistémica del resto:

| Marca | Qué significa |
|---|---|
| `caquetio-atestiguado` | una fuente dice que los caquetíos la usaban |
| `caquetio-probable` | contacto documentado + el referente existe en su mundo |
| `caquetio-posible` | contacto plausible, sin evidencia directa |
| `ajeno` | no hay motivo para pensar que entrara |

**Nada se pierde y nada se relaja**: `fuente`/`etimo` conserva su rigor intacto. Lo que se gana es poder decir *"taíno de origen, caquetío de uso"* sin mentir en ninguno de los dos campos.

## La línea editorial que esto implica

Una regla, en dos mitades:

> **Rigor sobre lo que la fuente dice. Generosidad sobre lo que el hablante pudo usar.**

Son dos pruebas distintas y no deben mezclarse. Hemos estado aplicando el rigor del primer eje para hacer exclusiones en el segundo, que es donde no corresponde.

## ⚠️ Lo que esto NO autoriza

Y conviene fijarlo, porque el riesgo de la puerta abierta es real:

1. **No baja el listón de la atestación.** Que Antolínez sea académico no convierte sus deducciones en datos. Hoy mismo se le refutaron dos afirmaciones —`ma` = 'grande', el étimo tupí de `Capo`— y no con autoridades rivales, sino **con las fuentes que él mismo cita**. Lo mismo pasó con González Batista (`hure` = 'arena', `corocoro` = 'espinas'). El método no es *autoridad contra autoridad*: es **atestación contra inferencia**. Una glosa impresa de un informante es otra clase de evidencia que una deducción, la firme quien la firme. Esa distinción es lo único que permite a un proyecto pequeño corregir a un catedrático — si se abandona, se pierde lo único que sostiene la fidelidad.
2. **No borra la regla 4.** Que las sociedades fueran mixtas no vuelve intercambiables las polities. Barquisimeto sigue sin ser el Golfete. Lo que cambia es que el préstamo entre ellas deja de ser anomalía y pasa a ser esperable — pero **declarado**, no silencioso.
3. **No convierte "es de otra lengua" en "entra igual".** `repertorio` exige su propia justificación, entrada por entrada. Es un campo más que llenar, no un campo menos.

## Trabajo que implica

- Añadir `repertorio` + `repertorio_razon` al esquema del lexicón.
- Decidir si `score_linguistico()` puntúa contra repertorio o contra filiación — y si lo hace contra repertorio, qué pasa con la tesis de koineización.
- Poblar `repertorio` en las ~1.100 entradas no-caquetías. Es grande, pero se puede empezar por las que ya tienen contacto documentado (taíno 57, lokono 227).
- Revisar la redacción de `CLAUDE.md` sobre "hablar wayunaiki es una fuga".

Relacionado: #69 · #39 (D11) · #36 (D5) · [[DISENO_KOINE]]
