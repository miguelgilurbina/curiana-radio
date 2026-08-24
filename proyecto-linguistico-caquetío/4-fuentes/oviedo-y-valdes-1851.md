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
los datos caquetíos más citados del corpus — el funeral del díao, y lo que
Jahn cita como "apéndice de voces caquetías" del tomo IV — y **el proyecto no
tiene ni una página suya legible**. Todo lo que usamos de Oviedo llega citado
por [[arcaya-1920]] y [[jahn-1927]].

> ⚠️ **El "apéndice de voces" del tomo IV no existe — verificado 2026-08-14**
> ([[01-rastreo-fuentes]]): en la edición Amador de los Ríos (tomo IV, 1855,
> libre en [Internet Archive](https://archive.org/details/historiageneral04fernguat)),
> las 16 apariciones de "vocabulario" son una **bibliografía de obras ajenas en
> la p. 626**, no un glosario de voces caquetías. Esto ya estaba anotado como
> pendiente en [[SIGUIENTE_TANDA]] (#61, "medido" pero sin editar); esta nota
> lo cierra. Consecuencia: *borattio* / *datihao-diao* (`creencia-001`, vía
> Jahn p. 213 n.29) **no se puede verificar en esta edición** — Jahn cita "el
> apéndice al tomo IV", pero esa pieza no existe en el volumen que el proyecto
> puede consultar. No implica que Jahn invente el dato; puede venir de otra
> edición o impresión de Oviedo. Sí implica que la cadena de cita
> (Oviedo → Jahn → nosotros) tiene un eslabón que hoy no se puede cerrar, y que
> "conseguir el apéndice" deja de ser una tarea con sentido tal como estaba
> planteada — **prioridad bajada**, según el rastreo.

## Estado técnico (verificado 2026-07-29) — 🔴 corrupto

| Dato | Valor |
|---|---|
| Tamaño | 37.8 MB (el archivo pesa, pero…) |
| `pypdf` | falla: `Stream has ended unexpectedly` / `EOF marker not found` |
| `pdftotext` | extrae **0 caracteres** |
| Veredicto | **no procesable con las herramientas actuales** |

Y aunque funcionara, **sería el volumen equivocado**: el material caquetío está
en el **tomo II** (funerales, pp. 299-300 y 329) — ninguno de los dos tomos que
hacen falta (II y IV) está en el repositorio, pero **los dos son de descarga
libre** en la ed. Amador de los Ríos, verificado 2026-08-14: [tomo
II](https://archive.org/details/historiageneral01fernguat) · [tomo
IV](https://archive.org/details/historiageneral04fernguat) — este último **sin
el apéndice de voces que se buscaba** (ver advertencia arriba).

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

1. ~~Conseguir tomo II en copia legible~~ — **ya no hace falta reparar nada**:
   está libre en Internet Archive (enlace arriba). Falta bajarlo y extraer las
   pp. 299-300 y 329.
2. ~~Conseguir el apéndice de voces del tomo IV~~ — **no existe en esta
   edición**; tarea cerrada, ver advertencia arriba.
3. Verificar si *borattio*/*datihao-diao* aparece en el **tomo II** (que sí
   existe) en vez del IV — Jahn pudo confundir el volumen, o citar otra
   edición. Es la única vía que queda para no dejar `creencia-001` colgando de
   una cita irreproducible.
4. Reparar o reemplazar este vol. I, si sigue haciendo falta una vez resueltos
   los tomos II y IV.

## Enlaces

[[arcaya-1920]] · [[jahn-1927]] · [[oviedo-y-banos]] · [[03_creencia_caquetia]]
