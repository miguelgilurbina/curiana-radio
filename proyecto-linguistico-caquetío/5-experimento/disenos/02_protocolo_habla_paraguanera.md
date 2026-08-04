# Protocolo — Minado de *El Habla Paraguanera* (y de cualquier léxico regional paraguanero)

*Diseño metodológico. Preparado ANTES de tener la fuente, para que el minado no se
improvise. No implementa nada.*

---

## 0. Estado de la fuente: NO DISPONIBLE

> ⚠️ **El libro no está en el repositorio.** Se buscó en todo el árbol (`find` por
> *habla* / *paraguan*) y en `fuentes_caquetios/` (30 archivos, inventario en la hoja de
> fuentes): no está. Tampoco se pudo **confirmar el título exacto** por búsqueda web.
>
> Obras paraguaneras/falconianas que **sí** aparecen y que podrían ser la que se busca, o
> fuentes adyacentes útiles:
> - **Alí Brett Martínez, *Aquella Paraguaná*** (1971; 2.ª ed. 1998) — crónica del poblamiento
>   y los personajes de la península. Periodista de Carirubana, autor de crónicas históricas
>   y regionales de Falcón.
> - **Tito Guerra, *Repertorio popular de palabras falconianas*** (Nuevo Día, Falcón, 2013)
>   — este sí es explícitamente un repertorio léxico regional.
>
> **Lo que necesito para ejecutar este protocolo:** el PDF/escaneo del libro en
> `fuentes_caquetios/`, o su referencia completa (autor, año, editorial). Si es escaneo de
> imagen, aplica la misma limitación que Alvarado 1921 y Jahn 1927: **este entorno no tiene
> OCR** (sin `tesseract`, `poppler` ni PyMuPDF), así que haría falta una capa de texto o una
> herramienta externa.

Mientras tanto, este documento define **cómo** se minaría y —lo más importante— **cómo se
mide la factibilidad** de que una voz paraguanera sea sustrato caquetío.

---

## 1. Por qué esta fuente importa tanto

Dos razones, y la segunda es la buena:

1. **Cierra un hueco de método declarado.** El programa «corpus cultural» define cuatro
   marcas, y una es **`retro-abstraido`**: *tradición viva local / intuición informada de
   Paraguaná*. Tras dos pasadas de investigación, el corpus de ecología tiene **cero
   entradas de esa marca** — todo salió de ciencia publicada y arqueología. Un diccionario
   del habla paraguanera es **exactamente la fuente retro-abstraída canónica**.

2. **Ataca el punto ciego estructural del lexicón.** El cross-check
   (`ecologia_lexicon_map.md`) reveló un patrón: el caquetío atestiguado es fuerte en *lo
   que se comercia y lo que significa* (biro, tüma, watapana, tara) y **mudo en lo que se
   ve y se trabaja a diario** (los peces por especie, el médano, el cardumen, la marea, la
   serpiente). ¿Por qué? Porque los cronistas anotaron mercancías y títulos. **¿Y dónde
   sobreviviría el vocabulario del oficio cotidiano, si sobrevivió en algún sitio? En el
   habla popular de la región, fosilizado dentro del español local.** El habla paraguanera
   es el candidato natural a conservar justo lo que a las crónicas no les interesó.

Es decir: la fuente no es «más vocabulario». Es potencialmente **el complemento exacto del
sesgo del corpus existente**.

---

## 2. El riesgo: por qué esto puede salir muy mal

El proyecto **ya cometió este error una vez**. Según `CLAUDE.md`: 441 palabras
`hipotético-no-verificado` se generaron transduciendo fonológicamente *cualquier* palabra
wayunaiki/lokono/taíno con la misma glosa, **sin verificar cognación real**; la minería de
pares objetivos mostró **~80 % de fallos** contra datos reales, y hubo que aislarlas del
léxico activo porque contaminaban el `score_linguistico`.

El minado de un léxico regional tiene **exactamente la misma tentación**: encontrar una
palabra bonita que suene indígena y declararla caquetía. La diferencia entre hacer esto bien
y repetir el desastre es **el rigor del filtro de descarte**, no el entusiasmo del hallazgo.

**Regla cero:** *una voz paraguanera no es caquetía por defecto. Es española hasta que se
demuestre lo contrario.*

---

## 3. Los competidores (filtros de descarte, en orden de aplicación)

Paraguaná es una de las zonas de contacto lingüístico más densas del Caribe. Antes de
atribuir una voz al caquetío hay que descartar, **en este orden**:

| # | Competidor | Por qué es fortísimo aquí | Cómo se descarta |
|---|---|---|---|
| **1** | **Español andaluz / canario** | Base del español venezolano costeño; la mayor parte del «habla regional» de cualquier región americana es dialectalismo peninsular conservado. | ¿Está en el DRAE, en repertorios andaluces/canarios, o en el *Diccionario de venezolanismos*? → **descartar**. |
| **2** | **Papiamento / neerlandés** | ⚠️ **El competidor que más se subestima.** Aruba está a **~25 km** de Paraguaná. Siglos de contrabando, migración pendular y trabajo en las refinerías (Punta Cardón / Amuay) inyectaron papiamento y neerlandés en el habla paraguanera. Una voz «rara» en Paraguaná es *a priori* tan probable de venir de Oranjestad como de un sustrato de 500 años. | Contrastar con diccionarios de papiamento y con neerlandés. → **descartar**. |
| **3** | **Wayuunaiki** | La Guajira está cerca y hay migración wayuu histórica y actual. Una voz arahuaca en Paraguaná puede ser **préstamo wayuu moderno**, no herencia caquetía. | Contrastar con `VOCABULARIO_BASE` (781 entradas wayuu ya en el lexicón) y con Captain & Captain 2005. → **marcar como wayuu, no caquetío**. |
| **4** | **Taíno / antillanismos panamericanos** | canoa, hamaca, maíz, batata, cacique, conuco… entraron al español **general** desde el Caribe insular y volvieron a Venezuela vía español. No prueban nada local. | Si la voz es panhispánica o pancaribeña → **no es evidencia de caquetío local**. |
| **5** | **Africanismos** | Vía trata y presencia afrodescendiente en la costa falconiana. | Contrastar con repertorios de afronegrismos americanos. |
| **6** | **Caribe / jirajaroide** | Lenguas de contacto documentadas en la frontera (el lexicón ya tiene 7 entradas jirajaroide-contacto). | Contrastar. → **marcar como contacto**. |

**Solo lo que sobrevive a los seis filtros pasa a evaluación positiva.**

---

## 4. Criterios positivos de plausibilidad caquetía

Una voz que superó los descartes gana puntos por:

1. **Campo semántico local e intraducible.** ¿Nombra algo que el español **no traía en el
   equipaje**? Fauna, flora, accidente del terreno, técnica local, fenómeno del paisaje.
   Un nombre de planta xerófila o de pez local es **mucho** más plausible que un verbo
   abstracto o un insulto (los insultos y las interjecciones son casi siempre romances).
   → **Este criterio es el más discriminante, y además apunta exactamente a los huecos
   léxicos del corpus.**
2. **Distribución restringida.** Si se dice en Paraguaná/Falcón y **no** en el resto de
   Venezuela ni en Canarias → indicio de sustrato local. Si se dice en toda Venezuela →
   probablemente no es caquetío específico.
3. **Fonotáctica arahuaca.** ¿Encaja con el perfil del caquetío atestiguado (estructura
   silábica, inventario consonántico, terminaciones)? Útil como **filtro negativo** (si
   viola la fonotáctica, fuera), **débil como filtro positivo** — es justo la trampa en la
   que cayeron las 441.
4. **Cognado en lengua hermana con la misma glosa.** Paralelo en wayuunaiki/lokono →
   refuerza el origen arahuaco. ⚠️ **Pero si es *idéntico* al wayuunaiki, sospechar préstamo
   wayuu directo (filtro 3), no herencia.** El punto dulce es el **cognado con
   correspondencia fonológica regular**, no la identidad.
5. **Respaldo toponímico.** Los topónimos son el reservorio más fiable de sustrato. Si la
   raíz aparece en topónimos de Falcón/Paraguaná (Curiana, Coro, Cumaraguas, Moruy,
   Jadacaquiva, Amuay…) → fuerte.
6. **Atestación colonial temprana.** Si la voz aparece en Oviedo, Las Casas, Castellanos o
   Galeotto Cey aplicada a la zona → deja de ser retro-abstraída y **sube a `atestiguado`**.

---

## 5. Escala de factibilidad y política de etiquetado

Propuesta de veredicto por voz, con **destino explícito** para cada nivel:

| Nivel | Condición | Marca | Destino |
|---|---|---|---|
| **A — Atestiguado** | Sobrevive a los 6 descartes **y** tiene atestación colonial o toponímica sólida | `atestiguado` | Candidata a `caquetío-atestiguado` en el lexicón, tras revisión |
| **B — Fuerte** | Sobrevive a los 6 descartes, campo semántico local, distribución restringida, cognado con correspondencia regular | `retro-abstraido` | **Corpus cultural sí; lexicón activo NO** (salvo decisión explícita) |
| **C — Plausible** | Sobrevive a los descartes pero solo cumple 1–2 criterios positivos | `hipotetico` | Solo corpus, marcada; **nunca** al lexicón activo |
| **D — Descartada** | Cae en cualquier filtro de descarte | — | Se documenta el descarte **y su razón** (tiene valor: evita re-minarla) |

**Dos reglas de oro:**

- **Ninguna voz entra al `VOCABULARIO_BASE` por este camino sin revisión humana explícita.**
  El destino natural de este minado es **el corpus cultural** (`cultura/*.yaml`) y, como
  mucho, una lista de candidatas — *no* el léxico activo. Meter formas no verificadas en
  `VOCABULARIO_BASE` es literalmente lo que produjo el problema de los falsos positivos en
  `score_linguistico`.
- **Documentar los descartes es tan valioso como los hallazgos.** Un «*busaca* → papiamento,
  descartada» ahorra que alguien la re-descubra dentro de seis meses.

---

## 6. Procedimiento de ejecución (cuando llegue la fuente)

1. **Extraer** el listado de voces (requiere capa de texto; ver §0).
2. **Pre-filtrar por campo semántico**: quedarse primero con fauna, flora, paisaje, clima,
   pesca, técnica — **los dominios de los huecos léxicos**. Ignorar de entrada insultos,
   interjecciones, fraseología: rendimiento bajísimo. Esto reduce el trabajo drásticamente y
   apunta donde el corpus lo necesita.
3. **Aplicar los 6 descartes** a cada voz superviviente.
4. **Puntuar** con los 6 criterios positivos → nivel A/B/C/D.
5. **Volcar** A y B al corpus cultural con marca y referencia; C aparte; D a una lista de
   descartes razonados.
6. **Cruzar con los huecos léxicos** de `ecologia_lexicon_map.md`: ¿alguna voz paraguanera
   nombra el médano, el cardumen, la marea, la costra de sal, el arroyo efímero? **Ese sería
   el hallazgo grande**, y es la razón por la que vale la pena todo el ejercicio.

---

## 7. La expectativa realista

Conviene decirlo antes de empezar, para que el resultado no decepcione: **la tasa de acierto
será baja.** La mayor parte de un diccionario de habla regional es español dialectal,
papiamento y creación local moderna. Si de varios cientos de voces salen **diez o quince**
con plausibilidad caquetía real, el minado habrá sido **un éxito rotundo** — sobre todo si
alguna de ellas cae en un hueco léxico.

La pregunta que este protocolo responde no es «¿cuántas palabras caquetías podemos añadir?»
sino **«¿cuáles de estas voces resisten un intento honesto de descartarlas?»**. Es la misma
disciplina que llevó a aislar las 441 — aplicada esta vez *antes* y no *después*.
