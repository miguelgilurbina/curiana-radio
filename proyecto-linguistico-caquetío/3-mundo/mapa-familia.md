---
tipo: moc
pregunta: "¿Cómo era la familia caquetía?"
sesion: 1/4 — programa corpus cultural
corpus: [parentesco.yaml, genealogia.yaml]
hechos: 39
etiquetas: {atestiguado: 14, reconstruido: 18, hipotetico: 7}
medido: 2026-07-29
---

# MOC — Familia, parentesco y sucesión

> Mapa de contenido de la pregunta 1 del programa cultural: **matrilinealidad,
> matrimonio, sucesión y sociedades masculinas** en la Curiana del Golfete,
> siglos XIV–XV. Un MOC no argumenta: enruta. El argumento está en el ensayo.

## La respuesta en una frase

**La familia caquetía de la simulación es un fuego con nombre de animal,
gobernado por sus mujeres, defendido por sus tíos, ampliado por sus matrimonios
y heredado por sus sobrinos** ([[01_familia_caquetia]] §7).

## Piezas

| Pieza | Qué es |
|---|---|
| [[01_familia_caquetia]] | El ensayo — 7 secciones, cinco rondas de trabajo acumuladas |
| `3-mundo/corpus/parentesco.yaml` | 39 hechos etiquetados (14 atestiguado · 18 reconstruido · 7 hipotético) |
| `3-mundo/corpus/genealogia.yaml` | Linajes, agentes y personas de fondo propuestas — **pendiente de veto**, ver [[DECISIONES_ABIERTAS]] D1 |
| [[01_familia]] | Hoja de fuentes — qué se buscó, qué se encontró, qué quedó abierto |
| `curiana_sim/CULTURA_CAQUETIA.md` §6 | El canon que este ensayo profundiza, no duplica |

## Las cuatro tesis que carga

1. **Precontacto = matrilineal, sin ambigüedad.** El registro patrilineal de
   Oliver es del cacicazgo **colonial** de Coro (s. XVI–XVIII) y prueba otra
   cosa. De aquí salió la regla de método: *nunca tratar dato de crónica
   post-contacto como norma precontacto sin que el canon ya decida proyectarlo*.
2. **Avunculado**: hereda el hijo de la hermana, no el hijo. El propio Oliver
   duda de "hijo" vs. "sobrino clasificatorio" en el registro colonial
   (1989: 262) — la duda de la fuente es la base de la propuesta.
3. **El cluster manda**: la matrilinealidad no descansa en una analogía sino en
   todo el arco norteño (wayuu, taíno, kalinago, lokono, achagua). El
   contraejemplo baniwa/curripaco (patrilineal) delimita el alcance.
4. **El cuello de botella matrimonial** (poligamia + exogamia) como motor
   narrativo del tier 2, y como lectura porosa de "caribe" (`hipotetico` puro).

## Fuentes que la sostienen

| Fuente | Peso | Nota |
|---|---|---|
| [[oliver-1989-cap3]] | **pilar** — 15 hechos del corpus | sucesión, poligamia de Manaure, bastardía en Paraguaná, achagua-caquetío |
| [[jahn-1927]] | alto — comparanda guajira | matriarcado, exogamia, levirato, tío-sobrino |
| [[arcaya-1920]] | medio | "nada nos dicen los cronistas"; poligamia por analogía; tatuaje y clanes |
| [[adam-1879]] | puntual, decisivo | doble registro kalinago como fósil de estructura matrimonial |
| [[oliver-1989-cap2]] | puntual | *daitiao*, raíz de parentesco /-atti-/ |
| [[keegan-1989]] | comparanda taína | avunculocalidad de élite — **no leído en texto completo** |
| [[las-casas-1875]] | nulo para este tema | revisado sin hallazgos (documentado) |
| [[oviedo-y-banos]] | **sin revisar** | 519 pp. con capa de texto, señalado por el propio programa |

## Hilos abiertos

- **D1 — veto de la genealogía** ([[DECISIONES_ABIERTAS]]): bloquea V3 y J1.
- **D4 — segundo sobrino de Manaure** (`parentesco-039`): pluralidad de
  candidatos, no ejecutada en `genealogia.yaml`.
- `daitiao` (Oliver 1989: 147) **sigue sin incorporarse** al lexicón. Ojo: existe
  `datihao` "padrino de cautivo" (Zavala), sin nota y **sin relación semántica
  clara** con el *daitiao* de parentesco — dos palabras parecidas, dos glosas
  distintas. Candidato de F1.
- La tabla de parentesco guajiro/paraujano de [[jahn-1927]] (pp. 438-439) no se
  reconstruyó palabra por palabra (columnas desalineadas en la extracción).
- ~35 agentes siguen con `linaje`/`madre`/`conyuge` en null.

## Salidas hacia otras preguntas

- El linaje como **unidad residencial** → [[mapa-ecologia]] (bohíos, fogón) y
  [[mapa-geografia-politica]] (apopo = cabeza de linaje).
- La transmisión **por la línea materna** (el tío enseña quién eres) →
  [[mapa-transmision]].
- El segundo entierro y el osario del matrilinaje → [[mapa-creencia]].
- Los `rol_*` componibles propuestos (§6.6) → [[mapa-motor]], sin implementar.
