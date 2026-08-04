---
tipo: fuente
obra: "Historia general y natural de las Indias, vol. I"
autor: "Fernández de Oviedo y Valdés, Gonzalo"
anio: "1851 [s. XVI]"
genero: cronica
local: "fuentes_caquetios/Oviedo_Valdes_1851_Historia_General_Indias_vol1.pdf"
paginas: "— (no legible)"
capa_texto: no
estado_minado: no-disponible
prioridad: alta
tareas: [F9]
sostiene: {hechos_corpus: 7, entradas_lexicon: 2}
verificado: 2026-07-29
aliases: ["Oviedo y Valdés", "Oviedo 1851", "Historia general y natural"]
---

# Oviedo y Valdés — *Historia general y natural de las Indias*

## Qué es

**La deuda documental más grande del proyecto.** Oviedo es la fuente última de
los datos caquetíos más citados del corpus — el funeral del díao, el apéndice de
voces caquetías — y **el proyecto no tiene ni una página suya legible**. Todo lo
que usamos de Oviedo llega citado por [[arcaya-1920]] y [[jahn-1927]].

## Estado técnico (verificado 2026-07-29) — 🔴 corrupto

| Dato | Valor |
|---|---|
| Tamaño | 37.8 MB (el archivo pesa, pero…) |
| `pypdf` | falla: `Stream has ended unexpectedly` / `EOF marker not found` |
| `pdftotext` | extrae **0 caracteres** |
| Veredicto | **no procesable con las herramientas actuales** |

Y aunque funcionara, **sería el volumen equivocado**: el material caquetío está
en el **tomo II** (funerales, pp. 299-300 y 329) y en el **apéndice de voces
caquetías del tomo IV** — ninguno de los dos está en el repositorio.

## Qué sostiene hoy (todo de segunda mano)

| Entrada | Qué afirma | Vía |
|---|---|---|
| `creencia-001` | *borattio* = "adivino o sacerdote"; *datihao/diao* = "señor" (apéndice t. IV) | [[jahn-1927]] p. 213 n.29 |
| `creencia-001b` | El díao como jefe cuyos poderes mágicos lo hacen jefe | [[arcaya-1920]] pp. 48, 116, 118 |
| `creencia-010`, `010b`, `010c` | **El funeral del díao**: desecación sobre brasas, casa abandonada, años de espera, "beber los huesos" en vino de maíz (t. II, 299-300) | [[arcaya-1920]] pp. 116-118 |
| `creencia-004b` | Ayuno ritual antes de guerra (t. II, 329) | [[arcaya-1920]] p. 118 |
| Lexicón | 2 entradas lo citan | vía Jahn/Arcaya |

También es la fuente que Jahn cita sobre la *puna* como señal de virginidad —
dato con relevancia directa para saberes de género restringidos
([[mapa-transmision]]) que **no se pudo verificar en la fuente primaria**.

## Qué falta — **F9, y es más importante de lo que parece**

Todo el bloque `atestiguado` de [[mapa-creencia]] descansa sobre una cadena de
tres eslabones (Oviedo → Arcaya/Jahn → nosotros) sin poder verificar el primero.
No es un defecto fatal —Arcaya cita casi verbatim— pero es **exactamente el tipo
de dependencia invisible** que la auditoría de fidelidad existe para hacer visible.

1. Conseguir **tomo II** en copia legible (el funeral del díao).
2. Conseguir el **apéndice de voces del tomo IV** — podría contener más términos
   religiosos además de *boratio*, y es fuente directa de lexicón.
3. Reparar o reemplazar este vol. I.

## Enlaces

[[arcaya-1920]] · [[jahn-1927]] · [[oviedo-y-banos]] · [[03_creencia_caquetia]]
