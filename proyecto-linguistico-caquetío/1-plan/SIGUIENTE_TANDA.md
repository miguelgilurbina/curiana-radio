---
tipo: nota-viva
ambito: qué hacer a continuación, y con qué contexto arrancar en frío
preparado: 2026-08-17
tablero: TABLERO.md
bandeja: 6-fusion/BANDEJA.md
---

# Siguiente tanda

> **Para una sesión que arranca en frío.** Antes de nada:
> ```
> python curiana_sim/generar_tablero.py    # el canon, medido
> python curiana_sim/generar_bandeja.py    # la cola de fusión
> python curiana_sim/guardianes.py         # los 6 en verde antes de cerrar nada
> ```
> Los números de esta nota pueden haber envejecido. Los de los generados, no.

## Dónde estamos (2026-08-17)

Tres días de minería intensa dejaron el proyecto con **más hallazgos de los que
se han fusionado**. La bandeja mide esa distancia: **~1.256 ítems en cola** y
**6 issues redactados sin publicar**. El motor no se ha tocado; el canon
tampoco. Todo lo nuevo vive en `6-fusion/` esperando decisión humana.

Lo que cambió de fondo en estos días:

- **Hay OCR** (`ocr_fuente.py`), y con él dejaron de estar bloqueadas Gilij y
  todo escaneo. Ver las trampas al final: es una herramienta que miente si no
  se la usa bien.
- **Está la tesis completa de Oliver** en `fuentes_caquetios/`, 801 páginas.
  Contiene los capítulos que el repo no tenía (1 y 4) y **los apéndices**, que
  eran #62.
- **`6-fusion/` existe**: la etapa entre minar y canon, con su BANDEJA medida.
  Nada valioso debe volver a morir en el scratchpad de una sesión.

---

## A · Lo que espera a Miguel (bloquea todo lo demás)

### A.1 · Publicar los 6 issues redactados

Están en `6-fusion/issues-pendientes/`. El classifier de las sesiones no puede
publicarlos; se hace a mano:

```bash
gh issue create --title "..." --label fidelidad,datos --body-file "6-fusion/issues-pendientes/ARCHIVO.md"
gh issue comment 38 --body-file "6-fusion/issues-pendientes/comentario-d9-issue38.md"
```

| Archivo | Qué es |
|---|---|
| `comentario-d9-issue38.md` | D9: la segunda fuente (`kapu-bana` = *a hill*) y el rumbo que fijó Miguel |
| `issue-hayo.md` | `hayo` está como caquetío-atestiguado y Oliver lo marca de Santa Marta |
| `issue-caraota.md` | ídem con `icoroata` |
| `comentario-52-mene.md` | #52: la glosa es **brea** ("pez derretida" = la pez, no un pescado) |
| `comentario-51-kadushi.md` | #51: la salida es léxico **por especies**; en Punto Fijo el fruto es `dato` |
| `issue-polity-en-el-corpus.md` | 🔴 el corpus dice cuánta certeza, no certeza **sobre quién** |

### A.2 · Decisiones de canon pendientes

1. **D9 (#38)** — no se declara glosa única hasta las dos sesiones de
   topónimos. En la lista de revisión: **Cujicana, Carirubana, Mene Mauroa**
   (y "Tropicana", que Miguel dictó y hay que confirmar).
2. **Etiqueta de préstamo** para `hayo` y `caraota` — se mantienen como bienes
   de contacto; falta el valor concreto, a coordinar con **#93**.
3. **#92 · los 15 nodos del foco** — `6-fusion/nodos_foco_92.yaml`. Un
   candidato a `precontacto: si` (FAL-101 La Maternidad), 5 `probable`.
   Y aparte: confirmar el criterio de `borde` para los 83 sitios de la costa
   occidental (¿misma polity?).
4. **Campo `polity`** en el corpus (el issue A.1 lo argumenta).
5. **#61** — ✅ editado 2026-08-14: el "apéndice de voces" del tomo IV de
   Oviedo **no existe** en la ed. Amador de los Ríos (16 hits de "vocabulario"
   = bibliografía ajena, p. 626). Aplicado en [[oviedo-y-valdes-1851]],
   [[jahn-1927]] y [[03_creencia_caquetia]]. Tomo II **y** tomo IV están
   libres en IA (enlaces en la nota). Falta cerrar el issue #61 en GitHub y
   bajar el tomo II para intentar localizar *borattio* ahí en vez de en el IV.
6. **`esteves-1989.md`** — el frontmatter dice `parcial` y "10 de 146 páginas";
   el barrido cerró a 154.

---

## B · La cola de minería, por rendimiento

### B.1 · Oliver §3.2.4 — los caribes  ← **lo siguiente**

pp. impresas 223-230 = **pdf 250-257**. Es el estrato que Esteves atribuye a
`Amuay`, `Elegüey`, `Maragüey`, `Jamaica` y `Maitiruma` — topónimos **de
Paraguaná** en lengua no caquetía. El lexicón ya tiene `kalinago` (19 formas) y
`kalinago-caribe-overlay` (4) donde encajarían. Pregunta concreta: ¿qué grupos
caribes, dónde, y con qué contacto documentado?

Pista suelta que espera: en la Tabla A-8, la entrada de 'luna' lleva la
anotación **"Tamanaco"** — lengua caribe — dentro del vocabulario jirajarano.

### B.2 · Las tablas de C-14 del capítulo 4

**Table 15** es la de fechas dabajuroides (citada junto a `ISGS-1184`). Está
por la zona de 4.12, impresas 435-473 = pdf 462-500. Ya se leyeron las del
texto corrido (p. 440):

```
ISGS-1173  Túcua           A.D.  783-[944]-998
ISGS-1255  Urumaco Temp.   A.D. 1164-[1257]-1279
ISGS-1257  Urumaco Tardío  A.D. 1278-[1336]-1393
```

Faltan **ISGS-1253, 1423 y 1424** (FAL-100), que son las que convertirían el
primer `precontacto: si` continental en algo que no dependa de una muestra de
superficie.

### B.3 · La Tabla A-9 completa (Apéndice A, #62)

Vocabulario caquetío del XVI, pp. impresas **593-594** = pdf 620-621.
Transcritas 21 de ~50 entradas en `6-fusion/tabla_a9_oliver.yaml`. **El resto
hay que leerlo a ojo**: el OCR no da la columna de formas con fiabilidad, y las
**cursivas** (= no caquetío) no sobreviven. Miguel ya identificó las tres que
hay: `icoroata`, `hayo`, `raporón`.

### B.4 · La Tabla A-7 — léxico arahuaco comparado

Mismo apéndice, ~impresas 585-590. Swadesh comparado con **Baure, Terena,
Kinikinao, Campa, Machiguenga, Piro-Ipurina**, cada una con ubicación. Es la
base que le falta al método comparativo del proyecto. Sin extraer.

### B.5 · Cruzar la Tabla A-8 con Jahn

`6-fusion/tabla_a8_jirajarano.yaml` tiene 33 entradas de jirajara/ayomán/cuyón.
**Jahn 1927 cap. V** trae vocabularios de los últimos hablantes **ayamán y
gayón** (~1880-1910). Son **dos registros independientes de las mismas lenguas
separados por décadas**: se pueden contrastar.

### B.6 · Oliver §3.2.3 (chibchas), lo que falta

Extraído y minado solo en parte. Queda §3.3.2 (jirajaranos fuera de la esfera)
y §3.3.3 (los chipas de Aroa).

### B.7 · Campañas grandes, cuando haya hueco

- **Topónimos**: los 413 de Esteves + los **134 sitios FAL** (que son topónimos
  *con afiliación arqueológica*) + Codazzi 1841. Parsear con morfemas
  atestiguados → predecir referente → verificar contra terreno. Resuelve D9.
- **Fauna/flora contra ecología**: `ecologia_lexicon_map.md` tiene **30 HUECO**.
  Fuentes ya minadas para cruzar: van Buurt (~100 voces con identificación
  científica), el inventario del informante **Manaure** en Esteves, Alvarado.
- **Dictado de Medina Colina** — protocolo y bitácora listos
  (`4-fuentes/medina-colina-sxx.md`). Miguel lo hará junto a una revisión de
  topónimos regionales.

---

## C · Adquisiciones pendientes

| Obra | Por qué | Estado |
|---|---|---|
| **van Koolwijk 1884**, *Bijdrage tot de taal der oude Indianen* | vocabulario indígena de las ABC recogido en campo **antes de 1900** — el mejor lead que hay | sin localizar |
| **Martí 1969**, *Visita Pastoral* (7 tomos) | censó Paraguaná pueblo por pueblo en 1773 | solo papel |
| **Galeoto Cey** (ed. 1995) | crónica 1539-53 con Manaure y "caquetíos = buena gente" | agotada; Miguel la compra |
| **Tamers 1965** | fecha FAL-111 y FAL-154 (distinta de la de 1970, que sí tenemos) | sin localizar |
| **Hartog 1961** | deportaciones de Aruba 1515/1526 | restringido en IA |
| **Antczak, *Los ídolos de las islas prometidas*** | solo tenemos **la portada** (1 página) | buscar |
| Oramas 1916 · Arcaya 1977 · Oliver 1984 | citados por las tablas jirajaranas y de C-14 | sin localizar |

---

## D · Trampas medidas estos días (leer antes de minar)

**El OCR miente si no se le exige.** Tres fallos silenciosos, los tres ya
resueltos en la herramienta pero que hay que saber que existen:

1. **Páginas rotadas.** El Apéndice E devolvió 2.850 caracteres y **cero
   sitios** porque la página venía a 90°. Un cero puede estar midiendo la
   *orientación*, no el contenido. `--rotar auto` (por defecto) lo detecta y
   **dice qué páginas giró**.
2. **Tablas a dos columnas.** Sin `--psm 6`, glosas y formas se desalinean y
   la mitad de las filas se pierden. Pasó con la lista de sitios y con la
   Tabla A-8.
3. **Más dpi no siempre es mejor.** A 600 se recuperó la cabecera de la Tabla
   A-9 pero se perdieron filas que sí salían a 400. **Correr las dos y fundir.**

**El OCR localiza la página; la cita se saca de la imagen.** Sobre todo en
nombres propios, topónimos y palabras indígenas — que es donde falla más y
donde el proyecto no puede permitirse el error.

### Desfases calibrados (no recalcular)

| Fuente | offset | Comprobado en |
|---|---|---|
| Tesis de Oliver (UCL) | **−27** | pdf 586 = impresa 559 |
| Gilij vol. 1 | **−52** | pdf 120 = impresa 68 |

⚠️ Los vols. 3 y 4 de Gilij **no están calibrados**: repetir por volumen.

### Otras

- **Los seis PDF de Esteves no tienen capa de texto** (250-450 chars/archivo).
  El barrido de agosto se hizo por lectura de imagen; queda pendiente una
  pasada de OCR de verificación.
- **La ſ larga sale como `f`** en Gilij: buscar con la clase `[fs]`.
- **`Caquet´ıo`** con acentos descompuestos en PDF de ResearchGate: `grep
  Caquetío` da cero, `grep -i caquet` da 19.

---

## E · Lo que NO hay que hacer

- **No tocar** `curiana_lexicon.py`, `3-mundo/corpus/*.yaml` ni
  `asentamientos.yaml` en una minería. Propuesta a `6-fusion/` (regla 5).
- **No mover los `lexicon_*.py`** de `curiana_sim/`: el tooling los importa
  (`generar_tablero`, `auditar_82`, `migrar_toponimos`).
- **No traer material mesoamericano ni andino** sin vínculo arahuaco explícito.
  Ya se descartó un lote entero por eso: la carpeta externa
  `Curiana Radio/Fuentes` se trió el 2026-08-14 y de ~27 obras solo valían dos,
  que ya están dentro. Lo que queda ahí no hay que volver a abrirlo.
- **No dar por caquetío** lo que salga de Barquisimeto, Yaracuy o los Llanos:
  Oliver §3.8 documenta que son polities distintas. Es el issue A.1 abierto.

## Enlaces

[[TABLERO]] · [[BANDEJA]] · [[CRONICA]] · [[PLAN_MAESTRO]] ·
[[oliver-1989-cap3-vecinos]] · [[oliver-1989-apendice-a]] · [[esteves-1989]]
