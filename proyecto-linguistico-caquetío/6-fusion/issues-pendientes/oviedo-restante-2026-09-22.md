# Tercera campaña de minería — M3: Oviedo y Valdés, lo que quedaba de los cuatro tomos

**Fecha**: 2026-09-22 · **Rama**: `campana/mineria3-oviedo`
**Datos**: [`6-fusion/oviedo_restante_2026-09-22.yaml`](../oviedo_restante_2026-09-22.yaml)
(cifras en `meta.cobertura` y `meta.sondas_medidas`, que emite
`python 6-fusion/scripts/medir_oviedo_restante.py`)
**Notas de fuente**: [`oviedo-y-valdes-1851`](../../4-fuentes/oviedo-y-valdes-1851.md) ·
[`oviedo-y-valdes-1852-1855`](../../4-fuentes/oviedo-y-valdes-1852-1855.md)

> Ninguna cifra de este texto está escrita a mano: las que aparecen se leen del
> YAML, que las recibe del script (regla 1).

---

## 0. Lo que resultó falso al medirlo

Las correcciones están en `correcciones:` del YAML (cuántas: `meta.cobertura.correcciones`). Las que pesan:

1. **El libro XIX no es «Tierra Firme» ni llega a la 618.** Es «de las islas de
   Cubagua é la Margarita», impresas 586-**614** (el índice empieza en la 615,
   en las dos copias). No trae Coro, Paraguaná, Coquibacoa, Curiana, las islas
   ABC, Manaure ni Ampíes: `meta.sondas_medidas.libro_XIX_sondas`, y el libro
   está leído entero, así que el cero es de la fuente.
2. **`dalihao` era el OCR. La página dice `datihao`**, con t (t. I p. 473, copia
   íntegra, con zoom). Se cierra lo que T1 y T7 dejaron «bloqueado hasta ver la
   imagen».
3. **`comoho` no tiene dos atestaciones independientes.** Oviedo dice en el t. II
   p. 331 que los capítulos de frutas de Venezuela del t. I los AÑADIÓ él con esa
   misma información; el de los cardones (`dactos`) nombra al informante, el
   obispo Bastidas. Es una sola cadena (minar-fuente §8): vale para `comoho`,
   `dato`, `mamón` y `semeruco`.
4. **El «cero lengua» del naufragio del t. IV no es cero**: desembarca en
   Paraguaná (1534) y trae Miraca por segunda vía, un paraguanero que dice
   «Capitan», la pesca, el manglar, la falta de agua y la mesa de Miraca.
5. **«Oviedo nunca empareja una voz venezolana con una antillana»** vale para los
   tomos II-IV. En el I lo hace una vez: `trocar` = `serra` (La Española) =
   `uchibican` (los chacopati de junto a Araya).
6. **`talara` es `tatara`** (el pez de Cubagua): el OCR miente en las dos copias.
7. **`Curiana` no son 2 menciones en un pasaje sino 3 en dos**, y la segunda
   dice de dónde sale: «la carta moderna del cosmógrapho Alonso de Chaves» (t. II
   p. 270). El río Curiana de Oviedo es de la carta, no de un testigo.
8. **`waitiao`**: la nota del lexicón dice que Oviedo describe el pacto de
   guaitiao «para el área circuncaribe». Oviedo no usa la palabra y lo cuenta
   sólo en San Juan. Ver §B.

---

## A. Para los agentes de fauna (lo primero que se empujó)

`fauna:` del YAML, con el esquema del preámbulo más `tomo`, `libro`,
`capitulo` y `verificacion`. Las entradas con sonido las cuenta
`meta.cobertura.fauna_con_sonido`; las de La Española, que sólo sirven de
comparación, van con `solo_comparacion: true`.

**Los sonidos que Oviedo sí describe, por cercanía a la Kaketiana:**

| Animal | Lugar | Lo que dice | p. |
|---|---|---|---|
| flamenco | Cubagua | «Graznan como ánsares é crian çerca de los lagos» | t. I 592 (imagen) |
| cascabel | Margarita | «suenan como proprios é verdaderos cascabeles sordos» | t. I 209 (imagen) |
| perro indígena | Santa Marta | «no se quexaban sino con çierto gruñir secreto ó baxo que apenas se oye» | t. II 355 (imagen) |
| perro indígena | Venezuela | «son mudos, que no ladran» | t. II 331 (imagen) |
| pavas | Santa Marta | «pavas de las grasnaderas prietas y de las leonadas» | t. II 354 (imagen) |
| aves marinas en cría | la «isla de las aves», al poniente de Coro | «el estruendo é resonançia del cherriar é graznar de las aves» | t. IV 525 |
| lobo marino | islas y costas de Tierra Firme | «roncan tan reçio, que desde lexos se oyen» | t. I 428 |
| pecarí (`baquira`) | Tierra Firme | «baten las quixadas … como suelen las cigüeñas sonar el pico, dando tabletadas» | t. I 409 |
| bivana | Paria | «anda silvando en un tono baxo» | t. I 417 |
| perico ligero | Darién (el nombre «pereza» es de Venezuela) | seis notas descendentes, «ha… ha… ha… ha… ha… ha…», sólo de noche | t. I 413 |
| monos negros | Castilla del Oro | «dan voçes que paresçe que se apellidan … gritando» | t. I 415 |
| aves zancudas | Orinoco | «graznan mucho y recio de noche, é óyense de muy lexos» | t. II 222 |
| caracol marino | Orinoco | trompetas «que se oyen é suenan mucho» | t. II 219 |
| roncadores | Pacífico de Nicaragua | «su mucho gruñir ó roncar» | t. III 111; t. IV 12 |

**Lo que no hay** (regla 6): ningún canto de ave de la costa venezolana fuera
del flamenco y las pavas; las aves que cantan en Oviedo son de La Española. El
capítulo de ranas y sapos no dice cómo suenan.

**Paraguaná misma**: sólo el naufragio de 1534 — perdices, conejos frescos y
salados, pan de maíz, un hombre y su hija que bajan a pescar, dos canoas
varadas, manglar. Ni un sonido.

---

## B. Decisión: `waitiao` y `datihao`

**Medido** (YAML §4): 0 formas de la familia `guaitiao` en las capas de los
cuatro tomos (las dos copias del t. I); y en la **imagen** de los pasajes donde
Oviedo cuenta el intercambio de nombres (t. I pp. 467, 472, 473 — San Juan) la
palabra no está. La única voz que Oviedo da para esa institución es `datihao`,
«mi señor, ó el que, como yo, se nombra», y es de San Juan.

`waitiao` es hoy `caquetío-atestiguado` con una nota que atribuye a Oviedo algo
que Oviedo no dice.

- **(a)** Corregir sólo la nota: quitar «lo describe Oviedo para el área
  circuncaribe» y citar a Las Casas (la cita de `cognado-009`), dejando la
  etiqueta. *Coste*: la etiqueta caquetía queda sin atestación caquetía.
- **(b)** Degradar `waitiao` a `taíno-atestiguado` (Las Casas, San Juan / La
  Española), con nota de que Oliver 1989 cap. 2 lo analiza como el mismo lexema
  que `datihao` con otro prefijo. *Coste*: el caquetío pierde la voz; la
  etimología de Oliver queda intacta como hipótesis.
- **(c)** `caquetío-hipotético`: la reconstrucción de Oliver es lo único que lo
  ata al caquetío.

**Recomiendo (b)**, y en el mismo gesto la opción (a) de T6 para `datihao`: las
dos voces de la familia `-tiao` que el lexicón tiene como caquetías son, en la
fuente primaria, de San Juan. En duda, degradar (regla 2); el concepto no se
pierde, porque `diao` sí está en Venezuela (T6).

---

## C. Voces y hechos que esperan fusión

Todos en el YAML, con página y verificación. Los que más valen:

- **`dactos` / `dacto`** (t. I pp. 311-312, imagen) — primera fuente primaria de
  `dato`, con estación de fruto (abril-mayo) y «críanse çerca de la costa».
  El lexicón lo tiene sólo por Zavala.
- **`mamon`** (p. 327, imagen: «llaman allí los indios», Venezuela) y el pan de
  hambre de su semilla.
- **`çimirucos`** (p. 328, imagen) — el semeruco, «dos veçes en el año».
- **`thenocas` y `coçixas`** (p. 591, imagen) — las perlas en la costa de
  Cubagua; el OCR las daba `Ihenocas`/`corixas`.
- **`uchibican`** (chacopati, 'trocar') frente a **`serra`** (taíno): el único
  par de la obra, y un rito de intercambio generalizado entre pueblos cuando hay
  eclipse de luna (pp. 208, 385). Araya, no el Golfete (regla 4).
- **`bagua`** 'la mar' en La Española (p. 436, imagen) — el lexicón sólo la
  tiene como comparanda sin cita.
- **Miraca**, segunda atestación independiente (t. IV p. 533) → campaña de
  topónimos.
- **Hallazgos de mundo** para `creencia` (incienso en la sepultura de los
  señores de Venezuela, pp. 203-204, que convive con el endocanibalismo de los
  çaquitios de la p. 297 del t. II sin fundirse; la rémora a la que se le habla)
  y para `ecologia` (meliponicultura en calabazas, cecina de palomas y de
  conejos, caza con fuego, vino de tuna).

---

## D. Lo que NO se hizo (y queda declarado)

- **Las formas `ocr-sin-imagen` de T1** (cuántas: `meta.cobertura.por_verificacion`
  de `taino_oviedo_valdes_1851.yaml`) se pueden verificar ya en la copia
  íntegra: no se tocaron, porque son parcela de T1 y su YAML no se reescribe
  desde aquí. Es una tarea mecánica, página a página.
- **Libros no leídos** (ver `meta.libros_leidos.no_leidos`): las plantas de La
  Española de los libros VIII-XI, los insectos del XV, el t. III y los libros
  del t. II y el IV que no tocan la costa. Sólo sondados.
- **`maperiti`, `bivana`, `pauxi`, `coches`**: sólo OCR limpio, sin imagen.
- **Qué isla es la «isla de las aves»** del naufragio de 1534 (Las Aves, Los
  Roques…): la fuente no lo dice y aquí no se decide.
- El PDF truncado del t. I **no se borra** (lo citan las propuestas de T1 por su
  paginación de PDF). Retirarlo es decisión de Miguel.

---

## Vista de paso (para otra campaña)

- El libro VI («de los depósitos») del t. I es el cajón de sastre de Oviedo y
  está casi sin leer: allí están los chacopati, las culebras de Margarita y
  Cubagua. Merece una lectura entera.
- `baquira` / `váquira` / `chuche` es una voz areal de la costa de Tierra Firme
  con tres atestaciones en Oviedo; si el proyecto quiere un nombre de la esfera
  para el pecarí, está aquí.
- El eclipse está en la cola de referentes de la simulación: el trueque ritual
  de los chacopati es la única conducta ante un eclipse documentada en la costa
  venezolana en Oviedo (Araya, no Paraguaná).
