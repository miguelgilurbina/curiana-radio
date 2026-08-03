---
tipo: fuente
obra: "Chapter 2: Arawakan Historical Linguistics"
autor: "Oliver, José R."
anio: 1989
genero: linguistica-comparativa
local: "fuentes_caquetios/Chapter 2 Linguistics- Oliver 1989.pdf"
paginas: 109
capa_texto: si
estado_minado: sin-minar
prioridad: alta
tareas: [F5]
sostiene: {hechos_corpus: 1, entradas_lexicon: 0}
verificado: 2026-07-29
aliases: ["Oliver 1989 cap. 2", "Oliver cap. 2", "Linguistics"]
---

# Oliver 1989, cap. 2 — Lingüística histórica arahuaca

## Qué es

**El pilar teórico de la Capa 2 del proyecto** (reconstrucción con base real) y,
hoy, su mayor deuda: 109 páginas de cognados y fonología comparada arahuaca de
las que solo se ha extraído **un hallazgo puntual**. Es la fuente que debería
alimentar `COGNADOS` en `arahuaco_comparative.py` — que tiene **37 entradas**.

## Estado técnico (verificado 2026-07-29)

| Dato | Valor |
|---|---|
| Tamaño | 12.3 MB · 109 páginas |
| Capa de texto | **sí** (~330K caracteres extraídos) |
| Receta | `pdftotext -enc UTF-8`; `pypdf` también funciona |
| Artefacto conocido | En varios tramos la extracción sale **una palabra por línea**; se arregla re-uniendo líneas por script. Las tablas de vocabulario **no se reconstruyeron** |

## Qué ha dado

- **p. 147** — el término caquetío atestiguado **`daitiao`**, cognado del taíno
  *daitia-o* y del lokono *da-tti/da-iti*, sobre la raíz de parentesco
  `/-atti-/` (que en lokono cubre 'tío', 'padre' e 'hija' según el prefijo
  posesivo). → `parentesco-012`. **Sigue sin incorporarse al lexicón.**
- Confirmación de que las dos hermanas más cercanas del caquetío son el
  **wayuunaiki** y el **paraujano** — el ancla del "arco norteño" de
  [[01_familia_caquetia]] §2.
- Contribuciones parciales previas a la fonología del proyecto (`daitiao`,
  `diao`).

## Qué falta — **F5, prioridad ALTA**

Es una de las **3 fuentes ALTA** cuyo minado es condición del gate para reanudar
simulaciones ([[PLAN_MAESTRO]] §6).

1. Extraer **sistemáticamente los sets de cognados** y las correspondencias
   fonológicas → alimentar `COGNADOS` (hoy 37) y `REGLAS_*` de
   `arahuaco_comparative.py`.
2. Reconstruir las **tablas de vocabulario comparativo** (numerales, términos
   básicos), que la sesión 1 dejó explícitamente sin hacer por falta de tiempo.
3. Cada cognado real que salga de aquí es munición para **validar o degradar**
   las 441 formas `hipotético-no-verificado` aisladas en `lexicon_candidatos.py`
   (~80% de fallo medido por `minar_pares_validacion.py`).
4. Resolver `daitiao` vs. `datihao` ("padrino de cautivo", en el lexicón sin
   nota, probablemente de [[zavala-reyes-2015]]): ¿dos palabras o una mal copiada?

## Enlaces

[[oliver-1989-cap3]] · [[brinton-1871]] · [[perea-alonso-1942]] ·
[[MOC_motor]] · [[MOC_familia]] · [[INDICE_FUENTES]]
