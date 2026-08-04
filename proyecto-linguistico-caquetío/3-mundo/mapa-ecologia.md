---
tipo: moc
pregunta: "¿Dónde existía el caquetío?"
sesion: 2/4 — programa corpus cultural
corpus: [ecologia.yaml]
hechos: 54
etiquetas: {atestiguado: 32, reconstruido: 21, hipotetico: 1}
medido: 2026-07-29
---

# MOC — Ecología del Golfete de Coro

> Mapa de contenido de la pregunta 2: **el medio físico** — geografía, clima,
> hidrología, flora y fauna del mundo de la Curiana. Es la sesión con más
> hechos `atestiguado` del corpus, porque la ciencia natural moderna sí publica.

## La respuesta en una frase

**Tierra pobre, mar rico**: un desierto costero (BSh, ~380–417 mm/año, alisio
ENE todo el año) con un ecosistema terrestre escaso pegado a una despensa marina
abundante — y toda la ingeniería social (el *buco*, el conuco, las salinas)
existiendo para salvar esa diferencia.

## Piezas

| Pieza | Qué es |
|---|---|
| [[02_ecologia_golfete]] | El ensayo v2 — 13 secciones + anexo de agentes ecológicos |
| `3-mundo/corpus/ecologia.yaml` | 45 hechos + **9 huecos léxicos** (54 entradas; 32 atestiguado · 21 reconstruido · 1 hipotético) |
| `3-mundo/corpus/ecologia_lexicon_map.md` | Cross-check especie/rasgo → palabra caquetía → hueco, por 9 dominios |
| [[02_ecologia]] | Hoja de fuentes |
| [[02_capas_biosfera]] | Diseño — las 5 capas: la fauna de hoy no es la del s. XV |
| [[02_motor_ambiental]] | Diseño — agentes ecológicos con voz mediada, cadenas causales |
| [[02_protocolo_habla_paraguanera]] | Protocolo escrito por adelantado; **la fuente aún no está en el repo** |

## Las cuatro tesis que carga

1. **El escenario es constante desde ~4000 BP** (geomorfología, clima) pero **el
   elenco animal se vació después del s. XV** → [[02_capas_biosfera]]: extinción
   global (foca monje), colapso de recurso (perlas), extirpación local (venado
   caramerudo, hoy ausente de gran parte de Falcón), sobreexplotación, censo actual.
2. **El alisio del noreste es el hecho ecológico maestro** — no un detalle de
   clima: gobierna navegación, quema del conuco, evaporación de las salinas.
3. **El *buco* no era una acequia de aldea**: era infraestructura regional
   (4-5 mil trabajadores para repararlo) → cruza con [[mapa-geografia-politica]].
4. **La madera de canoa venía de fuera** (cedro, caoba, ceiba no son del
   cardonal) — inferencia propia del ensayo, marcada como tal.

## Fuentes que la sostienen

| Fuente | Peso | Nota |
|---|---|---|
| [[camacho-2011]] | **pilar** — 16 hechos | geomorfología del Istmo, clima, ambientes sedimentarios, ríos |
| [[antczak-2015-las-aves]] | alto — 7 hechos | navegación insular, botuto, tortugas, guano, dabajuroide |
| [[rouse-cruxent-1963]] | **archivo vacío (0 bytes)** | era LA fuente prevista para la cerámica dabajuroide; sustituida por web |
| [[alvarado-1921]] | citado de oído | nombres de especies "ya en el lexicón" — pero **0 entradas del lexicón lo citan** |
| [[jahn-1927]] | idem | mismo caso que Alvarado |
| Ciencia natural moderna (web) | ~20 hechos | Inparques, SVDB, FAO, SciELO, PN Morrocoy como análogo |

> ⚠️ Este es el dominio con más `referencia` que apunta a **literatura web
> general** en vez de a una obra citable con página. No es ilegítimo (la ciencia
> natural moderna es publicada y verificable) pero es el punto más flojo del
> corpus para F10 (verificación de citas).

## Hilos abiertos

- **Rouse & Cruxent 1963 sigue en 0 bytes** — reconseguir el PDF (F9).
- **[[alvarado-1921]] SÍ tiene capa de texto** (verificado 2026-07-29 con
  `pdftotext`; `pypdf` devolvía vacío y por eso se declaró "escaneo sin texto").
  El hueco de OCR que bloqueaba esta sesión **no existe**. → F3.
- «guaranaro» sin identificación taxonómica firme.
- **Cero entradas `retro-abstraido`** en todo el dominio: la tradición viva de
  Paraguaná/Coro no aportó ni una. Hueco de método, no de datos.
- Sin arqueozoología del área caquetía (el estudio de Antczak es insular): no
  sabemos **qué comían realmente**, se infiere de la fauna moderna.

## Los 9 huecos léxicos

Fenómenos que la comunidad vive sin tener palabra — candidatos naturales a
neologismo emergente en un run. Es la conexión directa entre este MOC y
[[mapa-motor]]: `hueco-lex-001` a `009` (médano, ictiofauna, viento ENE
específico, nombres de pez de los agentes, proceso de salina, cauce efímero,
istmo, maderas de fuera, fauna marina).
