# Diseño — Capas de biosfera: el mundo animal que ya no está

*Pseudo-diseño e investigación. Complementa `02_ecologia_golfete.md` §10 y el motor
ambiental (`02_motor_ambiental.md`). No implementa nada.*

> **Premisa.** La v2 del ensayo estableció una regla de método: **la fauna de hoy no es la
> del siglo XV** (§10.6). Este documento la lleva a su conclusión. Si el censo moderno
> subestima el mundo animal caquetío, entonces reconstruirlo exige **estratificar la
> biosfera por grado y fecha de pérdida**, y tratar a los animales desaparecidos no como
> notas a pie de página sino como **protagonistas** del paisaje que la Curiana habitaba.

---

## 1. El problema: tres relojes distintos

Cuando decimos «el paisaje de hace 600 años» estamos mezclando cosas que cambian a
velocidades muy distintas:

| Componente | Reloj | ¿Vale la observación moderna? |
|---|---|---|
| **Geomorfología** (dunas, istmo, golfete) | milenios; estable desde ~4000 BP | **Sí** — Camacho et al. 2011 |
| **Clima** (alisio, BSh, pulso de lluvia) | milenios; estable en el Holoceno tardío | **Sí** — datos de Coro |
| **Biosfera** (fauna, bancos, poblaciones) | **décadas**; devastada desde 1500 | **NO** — subestima gravemente |

El error de la v1 fue tratar los tres como un bloque. La corrección: **el escenario es
constante, el elenco no.** Y el elenco se vació en su mayor parte **después** del momento
que la simulación retrata — lo que significa que la Curiana del s. XV vive en un mundo
biológicamente **más rico** que cualquier cosa observable hoy.

---

## 2. Las cinco capas

Propuesta de estratificación, de la pérdida más radical a la menos:

### Capa 0 — Extinción global: lo que ya no existe en ninguna parte

**Protagonista: la foca monje del Caribe** (*Neomonachus tropicalis*).

El **único pinnípedo que habitó el mar Caribe** y la única foca de aguas netamente
tropicales. Su distribución histórica iba de Florida y Puerto Rico **hasta el norte de
Sudamérica: Colombia y Venezuela**, pasando por todas las Antillas. Con la llegada de los
colonos fue cazada por su piel, su grasa y su carne; la sobrepesca regional le quitó además
el alimento. Último avistamiento confirmado: **1952** (isla Serranilla). La UICN la declaró
**extinta en 1994**. **[atestiguado]**

Es el protagonista perfecto de esta capa porque **no hay forma de que un habitante actual de
Paraguaná la haya visto jamás**, y sin embargo era parte plausible del mar caquetío: un
mamífero grande, torpe en tierra, gregario, que descansa en playas e islotes — exactamente
el tipo de animal que una cultura marítima con canoas y rutas insulares encontraría.

> ⚠️ **Cautela de método, importante.** No hay (que esta investigación haya hallado)
> constancia arqueológica de foca monje en yacimientos del Golfete de Coro. Su presencia en
> el mundo caquetío es **`reconstruido`**, por área de distribución, no `atestiguado` para
> la Curiana. Si se usa en la simulación, debe ser como **presencia rara y memorable** —no
> como recurso cotidiano—. La tentación de convertirla en un evento pintoresco es
> justamente lo que hay que resistir.

### Capa 1 — Colapso de recurso: lo que existía en abundancia inimaginable y se aniquiló

**Protagonista: la ostra perlífera** (*Pinctada imbricata*).

Este es el caso mejor documentado y el más relevante para el canon, porque **la perla
(*tüma*) es un bien de prestigio del comercio caquetío** y `expedicion_perlas` es un evento
de la simulación.

Los bancos perlíferos de **Cubagua** sostuvieron la primera empresa extractiva europea de
América. Las cifras son de otro orden: **más de 100 mil millones de ostras cosechadas en 30
años**. Nueva Cádiz —fundada en 1528, el primer asentamiento urbano español del
continente— fue el centro de esa explotación hasta su abandono hacia 1545, entre terremotos
y agotamiento. Es **el primer agotamiento documentado de un recurso natural causado por
europeos en el continente americano**. **[atestiguado — Romero, Chilbert & Eisenhart,
*Journal of Political Ecology*; Romero, «Death and Taxes», *Conservation Biology* 2003]**

Y el detalle que lo vuelve irreversible: bajo el estrés ecológico de la sobreexplotación, el
**mejillón pepitona** (*Arca zebra*) **desplazó competitivamente a la ostra perlífera e
impidió su recuperación**. No fue solo que se las llevaran: es que el ecosistema **cambió de
régimen** y se quedó así. **[atestiguado]**

**Implicación para la simulación, y es fuerte:** los agentes de la Curiana bucean en un mar
cuya riqueza perlífera será destruida **por completo, en treinta años, apenas unas décadas
después del final del marco temporal simulado**. La simulación es precolonial: retrata el
mundo **antes**. Dara-ko y Bagre-ko no lo saben. Nosotros sí. Eso no debe convertirse en
presagios ominosos dentro de la ficción —sería anacronismo barato— pero **sí puede informar
el aparato crítico del proyecto** (la voz del cronista Manaure, las glosas, la página
pública): el lector sabe lo que el personaje no puede saber.

### Capa 2 — Extirpación local: lo que sigue existiendo, pero ya no aquí

**Protagonistas: el venado caramerudo y el manatí.**

- **Venado caramerudo** (*Odocoileus virginianus*) — el **tara** del lexicón caquetío
  atestiguado. Hoy **ausente de gran parte del estado Falcón**; la causa documentada es la
  caza indiscriminada y sistemática **moderna**. La especie vive; el venado de Coro no.
  **[atestiguado]**
- **Manatí** (*Trichechus manatus*) — el **manatü** del lexicón, glosado literalmente como
  «vaca marina **del golfete**». Hoy está **en peligro crítico en Venezuela** y su presencia
  documentada se limita a Maracaibo, el Golfo de Paria y el Delta del Orinoco: **no al
  Golfete de Coro**. **[atestiguado para el estatus; reconstruido para su presencia
  histórica en el Golfete]**

El manatí ilustra el principio central de este documento mejor que ningún otro caso: **la
glosa del propio lexicón lo llama "del golfete", y en el golfete ya no hay.** La lengua
recuerda una biosfera que el censo perdió.

### Capa 3 — Sobreexplotación: lo que queda, pero como sombra

**Protagonistas: el botuto y las tortugas marinas.**

- **Botuto / caracol reina** (*Lobatus gigas*, el **cobo** del lexicón). La arqueología
  insular lo documenta en **densidades altísimas** — en los sitios de Las Aves los
  fragmentos de su concha son literalmente omnipresentes, y las densidades naturales de Los
  Roques estaban **entre las más altas del Caribe**. Hoy es especie sometida a veda y
  protección internacional por sobrepesca. **[atestiguado — Antczak & Antczak 2015]**
- **Tortugas marinas** (verde, carey, cardón, cabezón). Un solo sitio arqueológico insular
  arrojó **223 restos**, con las cabezas cortadas y descartadas fuera del yacimiento — señal
  de consumo sistemático, no anecdótico. Las cuatro especies están hoy amenazadas.
  **[atestiguado — Antczak & Antczak 2015]**

Estas dos entradas son las más útiles para calibrar el **volumen** de la pesca en la
simulación: el caquetío no «pescaba un poquito». Comía tortuga y botuto de forma sistemática
en un mar que los tenía en cantidades que hoy no existen.

### Capa 4 — La fauna actual: el suelo, no el techo

Lo que hoy se censa —zorro, oso melero, conejo, mapurite, rabipelado, iguana, cascabel—
sigue siendo válido: esas especies estaban. Pero **es el mínimo, no el retrato**. La regla
operativa: *la fauna moderna es un piso; la lengua y la arqueología levantan el techo.*

---

## 3. La regla de inferencia (y su límite)

De todo lo anterior sale un principio que ya está en el corpus (`ecologia-037`) y que aquí
se generaliza:

> **Cuando el lexicón caquetío atestiguado nombra un animal que hoy falta localmente, la
> palabra pesa más que el censo moderno.** Que exista *tara* prueba que había venado. Que
> *manatü* se glose «del golfete» prueba que había manatí en el golfete. **Un pueblo no
> acuña una palabra propia para lo que no ve.**

**Pero el principio no se invierte.** Y esto importa, porque el proyecto ya tiene una
cicatriz: las 441 palabras `hipotético-no-verificado` que se generaron transduciendo
cualquier cosa y fallaron ~80 % al validarse (ver `CLAUDE.md`). Aplicado aquí:

- ✅ **Válido:** «hay palabra caquetía atestiguada → el animal estaba» (evidencia positiva).
- ❌ **Inválido:** «el animal estaba en el Caribe → inventemos la palabra caquetía»
  (evidencia fabricada). La foca monje **no debe recibir una forma caquetía inventada**.
- ❌ **Inválido:** «no hay palabra → el animal no estaba» (el corpus léxico es un colador:
  los cronistas anotaron mercancías y títulos, no ictiofauna — ver el patrón detectado en
  `ecologia_lexicon_map.md`).

---

## 4. Qué hace este modelo por la simulación

1. **Calibra la abundancia.** El mar de la Curiana debe narrarse **rico**, no al nivel de un
   mar sobrepescado del s. XXI. La pesca abundante es la línea base; la mala pesca es la
   anomalía que exige explicación religiosa (y es exactamente lo que el motor ambiental
   propone).
2. **Da protagonistas concretos y verificables** a las escenas de mar e islas: botuto en
   cantidades enormes, tortugas de cuatro clases, manatí en el propio golfete, ostras
   perlíferas en bancos intactos.
3. **Alimenta el aparato crítico, no la ficción.** La ironía trágica —bucear perlas en
   bancos que serán aniquilados en 30 años, cazar un venado que la escopeta borrará— es
   material para las **glosas del cronista** y la página pública, no para presagios dentro
   del mundo. Los agentes viven en su presente.
4. **Refuerza los huecos léxicos.** Si el manatí, el delfín y las tortugas por especie casi
   no tienen nombre caquetío pese a ser fauna real y consumida (`hueco-lex-009`), la presión
   para nombrarlos es aún mayor de lo que parecía.

## 5. Pendiente crítico

**Falta arqueozoología del área caquetía continental.** Todo el material faunístico
arqueológico de esta sesión es **insular** (Antczak & Antczak 2015, archipiélago Las Aves).
No se halló un estudio de restos de fauna de yacimientos del Golfete / Coro / Paraguaná, que
es lo único que diría **qué comían realmente** en vez de inferirlo de la distribución
moderna. Es la vía más prometedora para convertir buena parte de este documento de
`reconstruido` a `atestiguado`, y para poblar la Capa 2 con datos duros en vez de con
razonamiento.

---

*Entradas de corpus derivadas: `ecologia-039` a `ecologia-044` en
`curiana_sim/cultura/ecologia.yaml`.*
