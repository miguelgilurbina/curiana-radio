---
tipo: fuente
obra: "Glosario de voces indígenas de Venezuela"
autor: "Alvarado, Lisandro"
anio: 1921
genero: glosario
local: "fuentes_caquetios/Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf"
paginas: 354
capa_texto: si
estado_minado: sin-minar
prioridad: alta
tareas: [F3]
sostiene: {hechos_corpus: 1, entradas_lexicon: 0}
verificado: 2026-07-29
aliases: ["Alvarado 1921", "Glosario de voces indígenas"]
---

# Alvarado 1921 — *Glosario de voces indígenas de Venezuela*

## Qué es

**Un glosario entero, sin minar** — la fuente grande que el proyecto lleva
citando de oído sin haberla abierto nunca. Lisandro Alvarado es además uno de
los nueve compiladores del glosario de [[zavala-reyes-2015]] (sigla `A`), así
que parte de nuestro "atestiguado" viene de él **de tercera mano**.

## 🔴 Corrección de estado (2026-07-29): SÍ tiene capa de texto

La hoja de fuentes [[02_ecologia]] lo clasificó como *"escaneo de imagen sin
capa de texto (354 pp., 27 MB; pág. 1 vacía) — no extraíble sin OCR"*, y desde
entonces F3 figuraba como bloqueada por una herramienta que el entorno no tiene.

**Eso era un artefacto de `pypdf`.** Verificado hoy:

```bash
pdftotext -enc UTF-8 "fuentes_caquetios/Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf" alvarado.txt
```

| Dato | Valor |
|---|---|
| Tamaño | 26.9 MB · 354 páginas |
| Texto extraído | **704 KB**, completo, con acentos correctos |
| Lemas en mayúscula detectados | **~1165** (regex simple; el total real es mayor) |
| Calidad OCR | buena — legible entrada por entrada, con erratas típicas de escaneo de 1921 |

**F3 no está bloqueada por OCR. Está lista para ejecutarse.** (Mismo caso que
[[arcaya-1920]] y [[jahn-1927]]: cuando `pypdf` devuelve vacío, probar
`pdftotext` antes de declarar un PDF ilegible.)

## Qué ha dado hasta hoy

Prácticamente nada, y conviene decirlo sin adornos:

- **0 entradas del lexicón lo citan** — pese a que [[02_ecologia]] afirma que
  "sus nombres de especies ya están integrados al lexicón como
  `caquetío-atestiguado`". Esa afirmación **no es verificable en el dato**: si
  esas palabras entraron, entraron sin cita, y son parte de las **82 entradas de
  familia caquetía sin `notas`** que F1 tiene que auditar.
- **1 hecho del corpus** lo menciona (`ecologia-019`), y de forma genérica
  ("Lexicón caquetío atestiguado (Alvarado 1921, Jahn 1927)"), sin página.

## Qué falta — **F3, prioridad ALTA**

Una de las 3 fuentes ALTA del gate ([[PLAN_MAESTRO]] §6).

1. **La mayor parte de Alvarado NO será caquetío**: es un glosario *nacional*
   (caribe, taíno, chaima, cumanagoto, guajiro, préstamos antillanos ya
   castellanizados). El protocolo de descarte ya está escrito y aplica casi
   idéntico: [[02_protocolo_habla_paraguanera]] — 6 filtros de descarte, 6
   criterios positivos de plausibilidad caquetía, escala A–D.
2. **Señales de localización** para priorizar el barrido (medidas en el texto):
   `Falcón` ×20, `Coro,` ×9, `caquetío` ×2, `Paraguaná` ×1, `guajiro` ×2,
   `Curazao` ×1. Empezar por ahí, no por la A.
3. Alvarado cita sus propias fuentes con siglas (`Reff.` ×84, `Ov.`, `Cast.`,
   `Cod.`) — la cadena de custodia se puede reconstruir entrada por entrada.
4. Cruzar contra [[zavala-reyes-2015]]: las entradas de sigla `A` en Zavala
   deberían poder rastrearse **a su lugar exacto en este glosario**. Es la
   prueba de fuego más barata para la fiabilidad de toda la Capa 1.

## Enlaces

[[MOC_ecologia]] · [[MOC_motor]] · [[02_protocolo_habla_paraguanera]] ·
[[zavala-reyes-2015]] · [[van-buurt-2014]] · [[gatschet-1885]] · [[INDICE_FUENTES]]
