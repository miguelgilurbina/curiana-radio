---
tipo: fuente
obra: "Relación acerca de las antigüedades de los indios"
autor: "Pané, fray Ramón"
anio: 1498
genero: cronica
publicacion: "Escrita c. 1494-1498 en La Española por encargo de Colón. El original se perdió; sobrevive en la traducción italiana de Ulloa (1571) dentro de la Historia de Fernando Colón, y en los extractos de Anglería y Las Casas. El texto del repo es la retraducción castellana que publica Wikisource"
local: "fuentes_caquetios/Pane_c1498_Relacion_Antiguedades_Indios_wikisource.txt (29 subpáginas, ~8.300 palabras)"
paginas: "29 capítulos"
capa_texto: si
estado_minado: minado
cobertura: "las 29 subpáginas, leídas enteras (2026-09-21)"
prioridad: alta
tareas: [D11-fase-2]
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-21
descargado: 2026-09-12
origen_digital: "es.wikisource.org; la OBRA es de dominio público pero la RETRADUCCIÓN no consta y Wikisource avisa que puede no serlo (verificado 2026-09-21). Marcado wiki retirado por script el 2026-09-12"
aliases: ["Pané", "Ramón Pané", "Pané 1498", "Relación de Pané", "Antigüedades de los indios"]
---

# Pané c. 1498 — *Relación acerca de las antigüedades de los indios*

## Por qué está aquí

Es **la fuente primaria del taíno**: el primer texto etnográfico del Nuevo
Mundo, y de donde salen la mayoría de las voces taínas de mito y rito que
circulan de segunda mano (`cemí`, `behique`, `Yocahu`, `guanín`, los nombres
de los héroes). El lexicón tiene 45 entradas `taíno` y 9 `taíno-reconstruido`
sin una sola procedencia a Pané. Comparanda del eje lokono-taíno (D11).

Descargado el 2026-09-12 con autorización de Miguel, desde Wikisource.

## ⚠️ Lo que hay que saber antes de citarlo

**No existe el original.** Lo que se lee es castellano ← italiano (Ulloa
1571) ← castellano perdido (Pané). Cada nombre taíno pasó por dos copistas y
una imprenta veneciana: las grafías (`Yocahu`/`Yocahuguama`, `Guahayona`,
`Itiba Tauvava`) son las de esa cadena, no las del fraile. Para cualquier
forma hay que decir por qué vía se cita. Arrom 1974 es la edición crítica de
referencia; no está en el repo.

## Qué es (medido al descargar)

29 subpáginas / capítulos, ~8.300 palabras. `cemí` 41 veces, `cacique` 17,
`yuca` 5, `Yocahu` 1, `guanín` 1; `behique`, `bohío`, `casabe` y `areíto` **no
aparecen con esa grafía** — la retraducción usa otras (por medir: `buhuitihu`,
`bohío`→?). Lo primero que hay que hacer es un censo de las formas indígenas
tal como las escribe ESTA versión.

## Minado — campaña del taíno, 2026-09-21 (parcela T2)

Leído **entero**, las 29 subpáginas. Propuesta en
`6-fusion/taino_pane_c1498.yaml`; cola de decisión en
`6-fusion/issues-pendientes/taino-lascasas-pane-brinton-2026-09-21.md`.

### ⚠️ Lo que había que verificar y no se había verificado

**Wikisource NO declara la edición ni el traductor.** Consultada el
2026-09-21: da autor (Ramón Pané), fecha (1498) y licencia, y nada más. La
frase de este archivo —«la edición/traducción es la que Wikisource declara en
cada subpágina»— era falsa: el dato no se perdió al quitar el marcado wiki, no
existe en origen. **Citamos esta fuente sin saber qué retraducción es.**

Y Wikisource añade: *«La traducción de la obra puede no estar en dominio
público»*. Consecuencia práctica (regla de copyright del proyecto): de este
archivo se citan **formas indígenas y glosas cortas**, no párrafos largos. Los
YAML de la propuesta están escritos así.

### La deformación de la cadena, MEDIDA

El texto trae **diez nombres con grafía inestable** en 8.343 palabras, tres de
ellos con tres formas distintas:

| forma A | forma B | forma C | quién |
|---|---|---|---|
| `Guaguyona` (5) | `Guahayona` (10) | | el héroe que se lleva a las mujeres |
| `Basamanaco` (1) | `Ayamanaco` (1) | `Bayamanicoel` (1) | el abuelo del cazabi — **los tres en el mismo capítulo XI** |
| `buhitihu` (10) | `buhuitihu` (2) | `bohutis` (1) | el médico |
| `Itiba Yauvava` (1) | `Itiba Tauvava` (1) | | la madre de los cuatrillizos |
| `Vaibrama` (3) | `Buyayba` (1) | | un cemí — el título dice una, el cuerpo la otra |
| `Yocahu Vagua Maorocoti` (1) | `Yiocavugama` (1) | | el ser inmortal del cielo |
| `Matinino` (1) | `Matanino` (1) | | la isla de las mujeres |
| `Macorix` (2) | `Marcorix` (1) | | la provincia y su lengua |
| `Guarionex` (11) | `Guarionel` (1) | | el cacique |
| `Maviatúe` (2) | `Mahuviativire` (1) | | el cacique de la última jornada |

En un texto de este tamaño eso no es descuido puntual: **es la firma de la
cadena castellano → italiano → castellano**. Cada entrada que cite a Pané lleva
`transmision: via-italiano`.

Y un desajuste que es su mejor ilustración: el proemio dice que la madre del
ser del cielo tiene **cinco nombres** y enumera **cuatro** (`Atabex`,
`Iermaoguacar`, `Apito`, `Zuimaco`). No se puede saber si el error es de Pané,
de Ulloa, de la imprenta o del retraductor.

### Qué dio

- **24 voces con glosa del propio Pané**, entre ellas `conuco` «que quiere
  decir posesiones, que eran de una herencia», `ciba` 'piedra', `cobo` «el
  caracol de mar», `guanara` 'lugar apartado', `operito` 'muerto', y la pareja
  `goeiz` (alma del vivo) / `opia` (alma del muerto) en una sola frase.
- **`Dios naboria daca`, «que quiere decir: yo soy siervo de Dios»** (cap.
  XXV). La única oración taína con glosa de toda la parcela, y por tanto el
  dato gramatical más caro que hay: pronombre de 1.ª pospuesto y predicado
  nominal sin cópula. **Es de MACORIX**, no de la lengua general.
- **9 deidades, 8 lugares del mito y 5 ritos** para la esfera de creencia,
  como comparanda antillana.
- **`inriri`, y «antiguamente `inrire cahuvayal`»** (cap. VIII): el único dato
  de profundidad temporal interna a la lengua que da la fuente.

### La evidencia de que el taíno no era una sola lengua

Es el hallazgo mayor, y es de primera mano. Cap. XXV:

> Entonces el señor Almirante me dijo que Macorix, provincia de la Magdalena,
> tenía lengua distinta de la otra, y que no era usado su idioma en toda la
> isla

> «Señor, ¿cómo quiere Vuestra Señoría que yo vaya a estar con Guarionex, no
> sabiendo más lengua que la de Macorix? Déme Vuestra Señoría licencia para que
> venga conmigo alguno de los del Nuhuirci [...] y sabían las dos lenguas»

Pané **había aprendido macorix** y necesitó intérprete bilingüe para pasar a la
lengua general, dentro de la misma isla, en 1495. Sesenta años antes que
[[las-casas-1875]], y **sin depender de él**: el pasaje de los mazoriges del
cap. LXVII del tomo I es recuerdo personal de Las Casas, no resumen de Pané.
Dos atestaciones independientes de verdad (skill §8).

### Qué NO dio

- **`areíto` no aparece en ninguna grafía**: la ceremonia se describe (cap.
  XIV, con el instrumento `mayohavau` y «su ley expuesta en canciones
  antiguas») pero no se nombra.
- `bohío` como 'casa' tampoco: lo que hay es `Bouhi`, nombre antiguo de las
  islas.
- `behique` no, pero la voz SÍ está, con tres grafías (arriba).
- `casabe` no, `cazabi` sí (3 veces).

### Qué falta

1. **Saber qué retraducción es.** Sin eso, toda cita a Pané arrastra una
   incógnita.
2. **Arrom 1974**, la edición crítica, sigue fuera del repo. Es la que resolvería
   los diez dobletes. No se descargó nada.
3. [[brinton-1871]] cita «Pane, pp. 443-444»: es otra edición, así que sus
   citas no se pueden cotejar con este archivo por página, sólo por contenido.
   Y las dos formas que atribuye a Pané, `Bugi` y `Aiba`, **no están aquí**
   (0 ocurrencias).
4. El paralelo behique ↔ boratio se **señala y se deja abierto**: ninguna
   fuente del canon lo afirma, y dos pueblos arahuacos vecinos con especialista
   ritual no prueban nada por sí solos.

## Enlaces

[[oviedo-y-valdes-1851]] · [[angleria-1892]] · [[brinton-1871]]

## Bitácora 2026-09-22 — fauna del mar (FA3)

Se le preguntó por el mar. **Caps. IX-X**: el origen del mar de la calabaza de
Yaya, con los huesos de Yayael vueltos peces. Va como comparanda de la esfera
(no caquetía) en `6-fusion/fauna_paraguana_mar_2026-09-22.yaml`
§cosmovision_marina (cm-c2), con la rima con la bebida de los huesos caquetía
marcada como lectura.

---

## Bitácora: cohoba y la *manaia* (2026-09-23, cc.7)

- cap. XI: «la cohoba es cierto polvo que ellos toman algunas veces para
  purgarse». Es el POLVO, no el tabaco (lo mismo que ya decía §pv04 de
  `6-fusion/taino_pane_c1498.yaml`).
- cap. XI, Caracaracol: la retraducción de Wikisource dice «tomando una hacha
  de piedra, se la abrieron». Bachiller 1883 p. 192, que lee la versión
  italiana, dice «tomando una *manaia*». `manaya` sale de ahí, y es
  probablemente el italiano *mannaia* 'hacha'. Sin el original ni Arrom 1974
  no se puede decidir más.

Detalle: `6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml` §zayas.

## 2026-09-24 — campaña cosmovisión marina (comparanda)

**Se preguntó** por el mar en la creencia taína. **Se halló:** el mar es uno de
los saberes de origen (proemio: «cómo se hizo el mar»); el mito de Yaya (caps.
IX-X, cm-c2 verificado) con dos precisiones: Yaya MATA al hijo, y los huesos
vueltos peces SE COMEN; Guahayona y la mujer que deja «en el mar», Guabonito,
que le da guanines y cibas (caps. II-VI); el cobo, «el caracol de mar» (cap.
V); peces llevados al cemí en los días solemnes y el mal mandado «a la montaña,
o al mar» (cap. XVI); los cemíes del agua son de lluvia y viento (Guabancex,
cemí mujer de la tormenta, de un cacique; caps. XI, XV, XXIII). «Yocahu Vagua
Maorocoti» está en el proemio, sin glosa. **No se halló:** ningún cemí del mar;
«huracán» 0 (la tormenta es Guabancex).

COMPARANDA, no dato caquetío. Detalle en `6-fusion/cosmovision_marina_2026-09-24.yaml` §comparanda.
