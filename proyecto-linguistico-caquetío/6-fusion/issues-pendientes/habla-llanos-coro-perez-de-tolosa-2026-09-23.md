# «Aunque algo difieren en la habla á los de Coro» — ¿a dónde va este testigo?

**Fecha**: 2026-09-23 · **Rama**: `campana/mineria3-perez-de-tolosa`
**Datos**: [`6-fusion/perez_de_tolosa_1546_2026-09-23.yaml`](../perez_de_tolosa_1546_2026-09-23.yaml) §`lengua`, `ptol-16`
**Nota de fuente**: [`4-fuentes/perez-de-tolosa-1546.md`](../../4-fuentes/perez-de-tolosa-1546.md)
**Label propuesto**: `decision`

---

## El pasaje (verificado en imagen)

Pérez de Tolosa, *Relación de las tierras y provincias de la gobernación de
Venezuela* (Tocuyo, octubre de 1546), en Oviedo y Baños, ed. Fernández Duro,
t. II, **p. 234**:

> «…la mayor parte de los ríos entran en el río y golfo de Paria, do es
> gobernador Jirónimo de Ortal, y docientas leguas de tierra, sin entrar en la
> sierra, son los indios de nación Caquetios, aunque algo difieren en la habla
> á los de Coro; es gente bien dispuesta y viciosos de comida de carne y
> pescado; no son grandes labradores»

## Qué gente, qué región, qué polity

- **Quiénes**: los caquetíos de los **llanos**, en la ruta de Espira (1535-38) y
  de Hutten (1541-46): de Barquisimeto diez leguas hasta el llano y luego al sur
  «llevando siempre las sierras á la mano derecha» (p. 233), por ríos que van al
  Orinoco. Es el piedemonte de Portuguesa, Barinas y Apure: la polity **`llanos`**
  de `curiana_polities.py`.
- **Frente a quién**: «los de Coro», la polity **costera**, la que simulamos.
- **De quién es el dato**: de **segunda mano**. Tolosa no hizo esa ruta; su
  relación junta lo que vio y lo que le contaron «personas cuerdas que han
  andado toda la tierra» (p. 223). Esas entradas llevaban porteadores caquetíos
  de Coro en cadenas (interrogatorio, pp. 274-275), pero quién notó la
  diferencia el texto no lo dice.

## Lo que dice y lo que NO dice

**Dice**: en 1546, un informante castellano ve a los caquetíos de los llanos
como la **misma nación** que los de Coro y nota que hablan **«algo»** distinto.
Es el único testigo del s. XVI que conocemos de variación dentro del caquetío.

**No dice**:

1. **en qué** difieren: ni una palabra de ejemplo;
2. nada de variación **dentro de la costa** (Paraguaná, Coro, las islas): el
   contraste es llanos frente a Coro, y no se puede extender al Golfete;
3. **cuánto**: «algo» es la palabra de un castellano;
4. nada de **precontacto**: son dos poblaciones que la trata ya ha desplazado.

Y en la misma frase la economía es otra: «no son grandes labradores», comen
carne y pescado, a diferencia del valle de Barquisimeto («grandes labradores de
maíz», p. 233). Así que es **misma nación, habla algo distinta y sociedad
distinta**.

## A qué toca

- **Regla 4** y `3-mundo/polities-caquetias.md` («hablaban una lengua y no
  tenían una sola sociedad»). El dato matiza el canon sin contradecirlo: una
  lengua, con variedades.
- **`curiana_polities.py`**: la polity `llanos` no tiene rasgo de lengua. Éste
  sería el primero.
- **`curiana_social.DIALECTOS`**: hoy los perfiles dialectales van **por
  etnia**. Este dato es de variación **dentro** de una etnia y **entre
  polities**, que el motor no modela.
- **`5-experimento/DISENO_KOINE.md`**, y `polities-caquetias.md` §«Qué falta» 3:
  el escenario «misma lengua, distinta sociedad» se propone porque **aísla la
  variable**. El testigo de 1546 dice que en la realidad ese contacto traía
  **también** habla algo distinta, así que la variable no queda tan aislada.

## Opciones

- **A — Sólo al canon de polities.** Añadir a `llanos` el rasgo de lengua y el
  de economía con cita (p. 234, de segunda mano), y la línea en
  `polities-caquetias.md`. El motor no se toca. *Recomendada.*
- **B — A + nota de diseño.** Además, una nota en `DISENO_KOINE.md`: si alguna
  vez entra una segunda polity, llega con su **variedad** de lengua, que el
  lexicón no distingue (su campo de lengua es por etnia, no por polity). Sigue
  sin tocar el motor.
- **C — Modelar variedades en `curiana_social`.** Un perfil dialectal por
  polity. **No recomendada ahora**: simulamos una sola polity, la fuente no da ni una
  forma que distinga las variedades, y cualquier perfil sería inventado
  (regla 2).

**Recomendación: A**, y B cuando se diseñe el contacto entre polities. El dato
vale como dato de mundo; para el motor todavía no tiene ninguna forma que
enseñar.
