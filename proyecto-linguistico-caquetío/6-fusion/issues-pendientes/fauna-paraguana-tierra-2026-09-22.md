# FA1 — La fauna de tierra de Paraguaná en el s. XV, y la tarántula azul primero

**Tercera campaña de minería, parcela FA1 (fauna de tierra). 2026-09-22.**
Rama `campana/fauna-tierra`. PROPUESTA (regla 5): nada de esto toca el lexicón,
el corpus ni el motor. Datos en `6-fusion/fauna_paraguana_tierra_2026-09-22.yaml`.

---

## Lo que de este encargo resultó falso al medirlo

| Lo que decía | Lo medido |
|---|---|
| La tarántula azul «es endémica de la península» (Miguel, db.4; y el Libro Rojo 2015) | **Endémica de Venezuela, no de la península.** De 11 registros verificados, 9 están en la península —su «most important stronghold» y su localidad tipo («Paraguara» = Paraguaná, Strand 1907)—, y los otros en Coro, en el municipio Colina y cerca de Barquisimeto (Sherwood y Gianni-Zurita 2023, *Anartia* 36, pp. 38-41) |
| «Tuvo que ser muy importante» | **Ninguna evidencia**, ni a favor ni en contra: ninguna fuente del repo ni de las nuevas le da nombre indígena, uso o creencia (`6-fusion/scripts/buscar_tarantula_azul.py`). El referente describe al animal y no afirma su importancia |
| Vive «en madrigueras» (fichas divulgativas; el Libro Rojo) | Semiarborícola: su refugio es un **hueco de árbol, tronco caído o grieta de corteza** forrado de seda (Klaas 2003 vía Sherwood y Gianni-Zurita, p. 37) |
| La tarántula está en el repo sólo como «fauna actual del Monumento Natural», fuente Wikipedia | Correcto. Ahora tiene dos fuentes de verdad: Sherwood y Gianni-Zurita 2023 (descargada, CC BY 4.0) y el Libro Rojo 2015 (Colmenares) |
| (de paso) `korie` 'armadillo', caquetío atestiguado (Oliver A-9, Zavala #90) | **Sospecha de mala lectura, sin probar.** Oviedo t. II p. 330 dice «Armados *cories* hay, pero son mayores que los desta isla y el pelage tiénenlo mas áspero y de la forma el pelo de las hardas» (verificado en imagen). En Oviedo `cori` (en cursiva) es el cuy de La Española (t. I, lib. XII, cap. IV, p. 390); «armados» va en la lista justo después del perico ligero, como en el t. I los «encubertados» (cap. XXIII) van junto al perico ligero (cap. XXIV): son, con toda probabilidad, los armadillos, sin coma entre las dos palabras. Un animal «mayor que los desta isla» y con pelo como de ardilla es el cori, no el armadillo. Si la A-9 sacó `corie` de aquí, es la cadena de `datihao` otra vez |

---

## El veredicto en una frase

**La tarántula azul es un animal de este monte y estuvo en el s. XV con
seguridad —por biología, no por documento—, pero nadie dejó escrito cómo la
llamaban ni qué significaba; y el mejor documento de la parcela resultó ser
Oviedo t. II pp. 330-331, que da la fauna de tierra de la provincia hacia 1540
con perros que «no ladran», abejas criadas en calabazos y la langosta `tara`
que se comía asada.**

---

## Las cifras, y de dónde salen

Ninguna está escrita a mano (regla 1).

| Cifra | Valor | De dónde |
|---|---|---|
| Entradas del inventario | 56 (51 nativas + 5 de introducidas) | `verificar_fauna_tierra.py` |
| Presencia en el s. XV | segura 14 · probable 31 · dudosa 6 · excluida 5 | ídem |
| Por grupo (nativas) | mamíferos 18 · reptiles 13 · insectos 11 · arácnidos 3 · anfibios 3 · moluscos 2 · miriápodos 1 | ídem |
| Huecos (sin voz caquetía en el lexicón) | 26 de 51; 22 con presencia segura o probable | ídem |
| Sonido con fuente / onomatopeya de fuente | 8 / **1** (el sapito lipón, `dori`) | ídem |
| Candidatos a referente | 10 | ídem |
| Propuestas a `ecologia.yaml` | 7 | ídem |
| GBIF: ocurrencias en el polígono (sin fósiles) | 46.176 (46.188 con fósiles) | `gbif_fauna_tierra_paraguana.py` → `gbif_fauna_tierra_paraguana_2026-09-22.yaml` |
| GBIF: especies de las clases de tierra | 118, de 53 conjuntos de datos (con título, publicador y licencia) | ídem |
| GBIF: ausencias disfrazadas (organismQuantity 0 / ABSENT) en clases de tierra | 0 en todas (la trampa de NeoMaps es de aves: 480 filas) | ídem, `control_de_ausencias` |
| Inventario sin ocurrencia en el polígono | 21 de 56 (nocturnos, grupos sin identificar, introducidos de hoy): un cero de GBIF mide a los observadores | ídem, `inventario_contra_gbif` |

---

## Lo que NO se encontró

- **Ningún nombre, uso ni creencia de la tarántula**, en ninguna lengua de la
  esfera. Los únicos pasajes con arañas son de fuera (figuras de oro en
  sepulturas, Castellanos ed. 1857 p. 283, regla 4) o interpretativos
  (Antolínez 1946, arañas como símbolo en la cerámica arawak, sin pieza).
- **Ninguna onomatopeya** más que `dori`. xeno-canto pide cuenta para su API y
  bloqueó el buscador web; Macaulay sólo con JavaScript: **no se cita ninguna
  grabación por ID** (crear cuentas no lo hace un agente).
- **Escorpiones**: cero en GBIF y en las fuentes leídas.
- La lista de reptiles de la península (Barrio-Amorós et al. 2008, *Reptilia*
  72) **no es abierta**: se anota, no se baja.

---

## Los candidatos a referente (el borrador está en el YAML, §3)

Por orden: 1 **tarántula azul** (decisión de Miguel) · 2 conejo · 3 cascabel ·
4 sapito lipón · 5 perro de la casa (mudo) · 6 mapurite · 7 araña plateada ·
8 chicharra · 9 zancudo · 10 ciempiés. Cada uno con `desc_referente` (≤ 180) y
`se_oye` (≤ 80). Seis tienen el sonido —o el silencio— de fuente (tarántula,
conejo, cascabel por su nombre, sapito, perro, mapurite por el olor); los de la
chicharra y el zancudo no, y lo dicen.

---

## Lo que tiene que decidir Miguel

**A. El `se_oye` del sapito lipón.** «do-ri» es la onomatopeya de van Buurt y
también el nombre arubano que él da por probablemente caquetío (`dori`, nivel
A). Dárselo a los agentes es casi dictarles el nombre.
- **A1** — con las sílabas («dos notas en la noche de los charcos: do-ri,
  do-ri»). Si convergen en `dori`, no se sabrá si la koiné lo encontró o si lo
  copió.
- **A2** — sin las sílabas (`se_oye_sin_silabas`: «un canto corto de dos notas
  que se repite en los charcos después de la lluvia»). Si aun así sale algo
  como `dori`, eso sí es un dato.
- *Recomendación: A2.*

**B. Qué referentes entran al catálogo.**
- **B1** — los diez, en el orden propuesto.
- **B2** — sólo los seis con sonido o silencio de fuente (tarántula, conejo,
  cascabel, sapito, perro, mapurite).
- **B3** — otro orden o lista.
- *Recomendación: B2 para la base (30 días, 15 referentes a uno cada dos días:
  caben con los novedosos); los otros cuatro, para la era 3.*

**C. `korie` 'armadillo'.**
- **C1** — campaña corta de verificación: leer en imagen de dónde saca Oliver
  cada voz de la Tabla A-9 y qué es la sigla HB de Zavala #90.
- **C2** — dejarlo como está, con una nota que cite Oviedo t. II p. 330.
- *Recomendación: C1. Es barata y el precedente de `datihao` dice que vale.*

**D. Las siete propuestas a `ecologia.yaml`** (tarántula; la fauna de la
provincia en Oviedo; la miel de abejas sin aguijón criadas en calabazos; la
langosta `tara`; los endemismos del cerro; el cardón y su murciélago; las
cabras). **D1** fusionarlas; **D2** sólo las de Oviedo y la tarántula; **D3**
ninguna todavía. *Recomendación: D1* — son hechos de fuente, cada uno con su
capa.

**E. Cuentas en xeno-canto o Macaulay** para citar grabaciones por ID: decide
Miguel, y la abre él.

---

## Lo que se vio de paso y merece otra campaña

- **`surupa` «Blatta orientalis. Cucaracha»** (caquetío atestiguado): esa
  cucaracha es del Viejo Mundo. La voz puede ser caquetía y la identificación
  de la glosa, moderna. Revisar la glosa.
- **El perro mudo** es el único animal doméstico precontacto documentado para la
  provincia y el corpus no lo tiene.
- **La meliponicultura** (Oviedo p. 331) casa con el racimo de la miel de Medina
  (`ruba` negra / `wakukero` amarilla ↔ cera negra / cera amarilla): pide un
  hecho de transmisión u oficio, no sólo de ecología.
- **Alvarado 1921 no tiene barrido de fauna**: sólo entradas sueltas. Una
  pasada por nombres de animales daría etimologías (mapurite < caribe) y alguna
  voz de Coro.
- **Anderson 2003** (*Heteromys oasicus*) está abierto en Zenodo (5373417) y no
  se bajó.
- Una de las cuevas del Santuario de Fauna Silvestre se llama **Jacuque**, como
  la voz caquetía atestiguada `jacuque` 'regar'. Coincidencia de forma, sin
  glosa que la ate.
- Un pholcido de la península se llama ***Chisosa caquetio*** (GBIF): la
  ciencia ya bautizó un bicho con el nombre del pueblo.

---

*Cierre: fichas nuevas `4-fuentes/sherwood-gianni-zurita-2023.md`,
`libro-rojo-fauna-venezolana-2015.md`, `gbif-paraguana-2026.md`; bitácora en
Oviedo 1852-1855, van Buurt 2014 y Alvarado 1921. Scripts:
`gbif_fauna_tierra_paraguana.py`, `verificar_fauna_tierra.py`,
`buscar_tarantula_azul.py`.*
