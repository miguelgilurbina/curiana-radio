---
tipo: fuente
obra: "Cuba primitiva. Origen, lenguas, tradiciones e historia de los indios de las Antillas Mayores y las Lucayas"
autor: "Bachiller y Morales, Antonio"
anio: 1883
genero: etnohistoria-vocabulario
local: ["fuentes_caquetios/Bachiller_Morales_1883_Cuba_Primitiva.pdf", "fuentes_caquetios/Bachiller_Morales_1883_Cuba_Primitiva.txt"]
paginas: 399
capa_texto: si
descargado: 2026-09-22
origen_digital: "Internet Archive, ejemplar de la University of North Carolina at Chapel Hill (cubaprimitivaori00bach)"
estado_minado: parcial
cobertura: "sección 2ª barrida (47 consultas, T10); apéndice (A) y bloque eyeri ENTEROS leídos en imagen, y su retraducción de Pané (sección 2.1) cotejada con la de Wikisource (M5, 2026-09-23). Sin leer: la sección 3ª y la primera parte"
prioridad: alta
verificado: 2026-09-23
minado: 2026-09-23
aliases: ["Bachiller y Morales 1883", "Cuba primitiva"]
---

# Bachiller y Morales 1883 — *Cuba primitiva*

## Qué es

La obra mayor de la tradición cubana sobre las lenguas antillanas: 2ª edición,
399 páginas, presentada al Congreso de Americanistas. Su valor para este
proyecto **no es que añada voces**, sino que dice de quién sale cada una y
**corrige a quien se equivoca**, incluido Rafinesque, que es la raíz envenenada
de toda la tradición antillana del XIX (lo dice [[goeje-1939]] p. 5).

Alvarado 1921 la cita por página como autoridad, así que ya estaba actuando
sobre nuestro lexicón **a dos saltos de distancia**. Cerrar ese salto era barato
y ya está hecho.

## Estado técnico

| Cosa | Medido |
|---|---|
| PDF | 36,8 MB · sha256 `460d4f85…6841dcda` |
| Texto | `pdftotext -enc UTF-8`, 928 KB, 409 páginas de PDF |
| Página impresa | **pdf − 4**, medido sobre 227 marcas «— N —» |
| Derechos | dominio público (1883): copia literal permitida |

## Cómo se lee

1. **El OCR mueve el guion de las entradas de sitio.** El vocabulario está
   escrito `Palabra.— texto`, y el OCR lo devuelve también como
   `Palabra. texto` o `— Palabra. texto`. 🔴 Segmentar por ese patrón dio
   **5 de 51** claves del lexicón; buscar la palabra suelta sobre el texto
   aplanado da **37 de 47**. Fue un cero de la consulta, no de la fuente:
   la regla 6 en vivo, por tercera vez en este repo.
2. **Las secciones 3ª y los apéndices van a dos columnas** y el OCR las
   entrelaza línea a línea. Nada de ahí se cita sin verlo.
3. Errores sistemáticos del OCR: `easique` por casique, `cerní` por cemí,
   `Bafinesque` por Rafinesque, `Eojas` por Rojas.
4. 🔴 **La sección importa.** La 2ª (pp. 185-354) es la lista histórica de los
   taínos; la **3ª (pp. 355-387) es el cubano moderno del s. XIX**. Lo que sólo
   aparece en la 3ª no es taíno atestiguado. `manigua` es de ésas.

## Qué se le preguntó

Qué voces taínas trae, de quién dice que salen, y si separa el taíno del caribe
insular.

## Qué ha dado

- **El apéndice (A), p. 388**: publica la lista de Rafinesque **con la isla
  marcada** —Cuba, Jamaica, Lucayas— y **rectifica sus errores uno a uno**.
  De ahí salen asignaciones de variedad para `cayo` (lucaya/yucaya, apoyada
  dos veces), `hutia` (Lucayas), `tuna` (Cuba, y es la Opuntia), `bejique`
  (Cuba y Lucayas), `bohio`, `maisi`, `cacique`, `caiman`, `nucay`.
- **El bloque EYERI de Borinquen**, inmediatamente después y separado:
  `Mabuya`, `Uragan`, `Piraguas`, `Ditaino`, `Boyez` y `Chemin` están **ahí**,
  no en la lista taína. Es la línea taíno/caribe insular trazada en 1883.
- **El apéndice (C), p. 394**: las voces que pasan por indígenas y vienen de
  otras partes. Ahí está **`taita`**, con Bachiller corrigiendo a Pichardo —que
  es la única autoridad detrás de nuestra entrada, vía Brinton— y proponiendo
  el vascuence `aita`.
- **`daca`** (p. 270): dice que expresa el ser o la existencia, y que **Las
  Casas escribe `daca` y Pané `dacha`**. Tercera mano independiente.
- **`cohiba` / `tabako`** (p. 256): `cohiba` es la planta y `tabaco` el
  instrumento. Tercera fuente independiente que lo dice, y el lexicón los
  tiene al revés.
- **`guabina`** (p. 267): aparece su cita primaria — Las Casas enumera los peces
  de nombre indio y `guabina` está entre ellos.
- **`siba`** (p. 210): piedra en Haití **y** entre los araguas de Demerara,
  citando a Irving y a Brett.
- **La esfera documentada** (p. 239): Gumilla registra nueve voces antillanas
  **en uso en el Orinoco** (`bija`, `macana`, `cabuya`, `jobo`, `caimán`,
  `yuca`…). Ojo: es el s. XVIII y con el castellano de por medio.

## Qué NO ha dado

- **`mayani`, `yamosa` y `abba`/`hequeti`: cero las tres.** Los numerales y la
  negación taínos siguen colgando de Las Casas *Apologética* cap. 204 y 241,
  que el repo **no tiene**.
- **Cero las siete voces que este proyecto reconstruyó desde el lokono**
  (`acoa`, `aduri`, `agari`, `akcicyaa`, `thigisi`, `wacusi`, `wagulo`). Dos
  vocabularios antillanos independientes y ninguno las tiene.
- Ni una glosa caquetía.

## Deuda que deja

1. Su **retraducción de la Relación de Pané** (sección 2.1, pp. 165-184) sin
   leer: hay que cotejarla con `6-fusion/taino_pane_c1498.yaml`.
2. El pasaje de Las Casas donde enumera los peces —incluido `guabina`— **sin
   libro ni capítulo**. Localizarlo en el tomo que tenemos.
3. La sección 3ª entera (el cubano moderno), que es el material para separar
   tainismo panhispánico de voz antillana atestiguada.

## Ver también

[[goeje-1939]] · [[brinton-1871]] · [[pichardo-1862]] ·
`6-fusion/taino_bachiller_morales_1883.yaml`

## Bitácora 2026-09-23 — tercera campaña, parcela M5

**Qué se preguntó.** La lista de Rafinesque con las islas y el bloque eyeri,
enteros; y si su retraducción de Pané coincide con la del repo.

**Qué ha dado.**

- El apéndice (A) y el bloque «eyeri» **enteros, leídos en imagen** (pp.
  388-389): `6-fusion/taino3_bachiller_morales_1883.yaml`. 🔴 El bloque tiene
  **dos marcas**, `E.` (eyeri) y `B.` (sin definir; por el contenido,
  Borinquen): `Piraguas` y `Ditaino` son **B.**, no eyeri, como leyó T10 en el
  OCR. Correcciones menores: `Alco` (no Aleo), `cusi` (no casi), `Opoyun`, y
  `hutia` es de Cuba y de las Lucayas.
- El «eyeri», cruzado con [[goeje-1939]], es el **habla de mujeres del caribe
  insular** (Eyeri, Inara, Kati, Kachi, Ubec, Nekera, Boyez…).
- **Su Pané no es testigo de Pané**: `6-fusion/taino3_pane_bachiller_cotejo.yaml`
  (script `cotejar_pane_bachiller.py`) — 12 de 49 formas restituidas, dos por
  sustitución declarada con Pedro Mártir (`guanaba` por `guabasa`,
  `Epilegaaanita` por `Opigielqaouiran`). Su método (p. 166) nombra a Oviedo,
  Mártir, Rafinesque y Brasseur.

**Qué NO.** La sección 3ª (cubano del XIX) y la primera parte siguen sin leer.
