## Medición del barrido completo — **no aplicar todavía**

Con Esteves 1989 ya en `main` (#100), medí el patrón sobre los cuatro lotes del
barrido (`4-fuentes/sesiones/06_esteves_1989_barrido_lote3-6.md`) y la nota de
fuente, en vez de contar a mano. Lo dejo escrito para cuando la evidencia esté
más completa; **el cambio no se aplica ahora**.

### `bana` = 'cerro / sitio alto' — 10 topónimos glosados, 0 contraejemplos

| Topónimo | Glosa de Esteves | Referente |
|---|---|---|
| Capuhana | 'el cerro del duende' | cerro, cerca de Misaray |
| Carirubana | 'la orilla del cerro' | costa con peñón |
| Coabana | 'el cerro de las coas' | — |
| Cujíbano | 'el cerro del cují' | variante `-bano` |
| Chichibana | 'el cerro de los achechives' | — |
| Judibana | `judi` viento + `bana` sitio alto | — |
| Tautabana › Tausabana | 'el cerro de las palomas tautas' | **cerro documentado, ~8 km al E del Cerro de Santa Ana** |
| Gibana | 'cerro amarillo' | ⚠️ Parte II |
| Guacabana | 'el cerro de las cotas' | ⚠️ Parte II |
| Caracubana | 'cerro poblado de caracara' | ⚠️ Parte II |

Más `Pipiribana`, que Esteves despacha como onomatopéyico pero cuyo referente
**es un cerro** (vecino al de Tausabana): no cuenta como glosa, sí como terreno.

Dos correcciones a lo que ya estaba escrito:

1. **`4-fuentes/esteves-1989.md` §3 dice `bana` ×8; los lotes sostienen 10.**
   Faltan `Tausabana` y `Caracubana`. Cifra a mano — regla 1.
2. **Tres de los diez son de la Parte II** (pp. 81-144, *otros topónimos del
   estado Falcón*, no Paraguaná): `Gibana`, `Guacabana`, `Caracubana`. Por la
   regla 4 no entran al canon costero sin marcar procedencia geográfica.
   **Paraguaná estricto: 7.**

### ⭐ La objeción de la hache queda resuelta — por el terreno

Lo que mantenía viva esta decisión era que `Capu-hana` (*"con hache intercalada
para deshacer el diptongo"*) es en realidad `capu-ana`, y por tanto la glosa
'cerro' podía pertenecer a **`-ana`**, no a `-bana`.

La prueba independiente del autor que este issue pedía: **los `-ana` sin `b` no
son altos.**

| Topónimo en `-ana` | Accidente según Esteves |
|---|---|
| Guanachana | **quebrada y ciénaga** (Jacura, Dto. Acosta) |
| Capana | **punta costera**, desembocadura del Río Borojó |
| Maipana | lugar de Acurigua |
| Guaguana | aldea (mun. Casigua) |
| Chamuriana · Jayana | aldeas |

`-ana` se comporta como locativo genérico y aparece sobre terreno bajo y húmedo.
`-bana` **no aparece ni una vez sobre terreno bajo**. Los dos morfemas se separan
por geografía, que es independiente de lo que diga el cronista.

### `cari` está mucho menos sostenido que `bana`

Solo **dos** atestaciones toponímicas —`Carirubana`, `Cariguariana`— y las dos
costeras. `Caritibano` **no cuenta**: Esteves dice que es *"un árbol de madera
recia"*.

Ojo con esto al aplicar: si se le pasa a `cari` el locativo de 'orilla' que se le
quita a `-bana`, se está apoyando en 2 casos, no en 10.

### El choque que queda es un solo topónimo

| Fuente | Forma | Glosa |
|---|---|---|
| van Buurt §8 | *Hudishibana* | **'llano ventoso'** |
| Esteves p. 46 | *Judibana* | `judi` viento + **'sitio alto'** |

`hudi` = `judi` = 'viento'. **Es el mismo nombre con dos glosas opuestas**, y es
lo único que decide entre 'llano' y 'cerro'. Se resuelve mirando el terreno, no
comparando autoridades.

### Y una corroboración interna archivada como neutra

`2-lengua/morfologia.md` descarta `capubana` = *'duende del cerro'* como que "no
decide". Pero esa entrada **ya llevaba 'cerro' dentro** antes de Esteves, y
Esteves llega por su cuenta a `Capuhana` = 'el cerro del duende'. Dos
derivaciones independientes en el mismo sitio — la misma clase de coincidencia
que el `capu` del cronista.

### Lo que costaría aplicarlo (por eso no se aplica hoy)

`-bana` no es una fila de una tabla: está **enseñado, con ejemplos, en los
prompts del motor**.

| Dónde | Qué dice |
|---|---|
| `curiana_lexicon.py:6442` | `RAÍZ + -bana → orilla, límite, punto de transición` + 4 ejemplos |
| `curiana_lexicon.py:6817` · `:6892` · `:7548` | reglas de formación · `sima-bana = orilla del cerro` |
| `curiana_orchestrator_v2.py:108` | ejemplo del prompt: `kali-bana = orilla de luz` |
| `curiana_observer.py:674` | `golfete-bana = orilla interior del golfete` |
| `CLAUDE.md:144` · `morfologia.md:66` · `morfemas.yaml` | la chuleta y la ficha |
| `lexicon_van_buurt.py:1217` · `cognados_oliver.py:809` | notas de discrepancia ya escritas |

Nueve archivos, varios de ellos texto que los agentes leen. Cambiar la glosa
**reescribe prompt, no solo dato**: los runs anteriores dejan de ser comparables
en ese morfema. Con las simulaciones en pausa el momento es bueno, pero tiene que
ser deliberado.

### Veredicto propuesto, para cuando se aplique

- `bana` = **'cerro, sitio alto'** entra como **`reconstruido`**, no
  `atestiguado`: sigue siendo **fuente única**, y `Capuhana` es el caso más flojo
  de los siete por la hache. En duda, degradar.
- `cari` = 'orilla' entra como **`hipotético`** (2 casos).
- `-ana` = 'lugar de' se mantiene, ahora con apoyo de referente bajo/húmedo.
- Los tres topónimos de la Parte II se marcan con procedencia geográfica o se
  dejan fuera del canon costero.

### Qué falta para cerrarlo

- [ ] **Resolver Judibana / Hudishibana por el terreno.** Es la prueba decisiva.
- [ ] **Rastrear de dónde salió nuestra glosa 'orilla'** — la hipótesis es que
      alguien analizó `Carirubana` entero y le colgó 'orilla' al elemento
      equivocado, que es lo que Esteves asigna a `cari`.
- [ ] **Segunda fuente para `bana`**, independiente de Esteves. Martí (1773) y
      Castellanos son los candidatos que este mismo barrido destapó.
- [ ] Comprobar si los `-bana` insulares (*Shiribana*, *Tarabana*, *Wakubana*,
      *Bushiribani*) tienen referente alto o llano.

---

## Actualización 2026-08-16 — segunda fuente, y el rumbo que fija Miguel

**Todo lo de arriba se escribió con Esteves como fuente única. Ya no lo es.**
La Tabla A-9 de Oliver 1989 (Apéndice A, p. 593; `6-fusion/tabla_a9_oliver.yaml`)
trae:

> `17. Capubana — kapu-bana — a hill in Paraguaná`

Oliver segmenta **con `b`** y glosa 'colina', trabajando sobre fuentes del XVI —
independiente de Esteves, y justo en el punto débil (la hache de `Capu-hana`).
La propuesta de arriba ("entrar como `reconstruido` por fuente única") **se
quedó corta**: hay dos fuentes independientes.

**Y una corrección de lectura de Miguel que cambia una pieza**: la entrada
`13. cabana` no se transcribe `sabana` con s — es **`çabana` con ç cedilla**
(grafía del XVI para /s/). Confirma que Oliver la trata como **el étimo entero
del castellano "sabana"**: segmentarla en `ca-bana` para sostener `-bana` =
'llano' (morfologia.md §3) es análisis nuestro, no de la fuente.

**El rumbo decidido (Miguel, 2026-08-16):** no se declara una glosa única
todavía. `-ana` y `-bana` **pueden ser morfemas distintos y su valor puede
depender de la palabra** — `-ana` solo también parece locativo (cf. *Paraguaná*,
que pudo ser *Paraguana*). La decisión se toma **después de las dos sesiones de
topónimos** planificadas, evaluando palabra por palabra. Topónimos que Miguel
señala para esa revisión: **Cujicana · Carirubana** (y los que salgan del
gazeteer y de la revisión regional que hará junto al dictado de Medina Colina).

La chuleta del CLAUDE.md ya marca la glosa como EN DISPUTA mientras tanto.

---

## Ampliación 2026-08-18 — `sima-bana`, el ejemplo insignia del motor, depende de esto

La auditoría de polity del lexicón (`curiana_sim/auditar_polity_lexicon.py`)
destapó una consecuencia que no estaba en el radio de impacto de nueve archivos.

El motor **enseña y usa** este compuesto:

```
curiana_lexicon.py:6863   [sima-bana: sima+-bana = orilla del cerro]
curiana_lexicon.py:7548   ídem, dentro del prompt
curiana_social.py:269-272 Shaboro acuña [sima-bana]; se propaga a Buio-sha
                          — es el FIXTURE DEL TEST de contagio léxico
```

Y `sima` está en el lexicón como **'cerro, montaña, elevación'**
(`caquetío-reconstruido`).

> **`sima-bana` = 'orilla del cerro' solo se sostiene si `-bana` es 'orilla'.
> Si D9 resuelve 'cerro', el compuesto pasa a ser 'cerro-cerro'** — y no es un
> ejemplo cualquiera: es el que el motor usa para demostrar cómo se acuña y se
> contagia un neologismo, y el que verifica su test.

Hay que decidirlo junto con la glosa, no después. Y de paso: la nota de `sima`
dice que su forma está *"justificada por cognado en lokono/topónimo
(Barquisimeto)"* — una palabra del núcleo fundacional apoyada en un topónimo de
**la otra polity**. Merece revisión aparte.
