---
tipo: fuente
obra: "Palabras vivas de una lengua muerta: legado arawak-caquetío"
autor: "Zavala Reyes, Miguel Enrique"
anio: 2015
publicacion: "Boletín Antropológico 33(89), enero-junio, pp. 58-76. Universidad de Los Andes, Mérida"
genero: glosario
local: "fuentes_caquetios/Palabras Vivas de una Lengua Muerta.pdf"
paginas: 20
capa_texto: si
estado_minado: parcial
cobertura: "76% (218 de 286 entradas parseadas)"
prioridad: alta
tareas: [F7]
sostiene: {hechos_corpus: 7, entradas_lexicon: 164}
verificado: 2026-07-29
aliases: ["Zavala 2015", "Zavala Reyes 2015", "Palabras Vivas"]
---

# Zavala Reyes 2015 — *Palabras vivas de una lengua muerta*

## Qué es

**La fuente atestiguada central del proyecto.** Un artículo académico de 20
páginas cuyo núcleo es un **glosario caquetío compilado de nueve autores**
(identificados por siglas: PMA = Pedro Manuel Arcaya, HB = Adrián Hernández
Baño, E = Juan Esteves, AM = Angulo Molina, A = Lisandro Alvarado, GC = Galeotto
Cey, CGB = Carlos González Batista, AAM = Antonio Arellano Moreno, HP = Aníbal
Hill Peña). Es, en la práctica, **el único puente masivo** entre el lexicón
activo y una fuente citable.

> El nombre del archivo no delata al autor. Se confirmó por metadata del PDF
> (`/Title`, `/Author`, `/Subject`) en la sesión 5 — hasta entonces el proyecto
> citaba a Zavala sin tener localizado su PDF.

## Estado técnico (verificado 2026-07-29)

| Dato | Valor |
|---|---|
| Tamaño | 594 KB · 20 páginas |
| Capa de texto | **sí**, limpia |
| Receta | `pdftotext -enc UTF-8 "Palabras Vivas de una Lengua Muerta.pdf" out.txt` |
| Entradas numeradas | **286 parseadas** por `minar_zavala_glosario.py` (su docstring dice 288 en el PDF) |

## Qué ha dado

**Lexicón — 164 entradas lo citan** (todas de familia caquetía). Es el 70% de
las 233 `caquetío-atestiguado`. Tras la auditoría del 2026-07-20:

| Tier | n | Destino |
|---|---|---|
| T1 afijos | 8 | `REGLAS_ZAVALA` — `-iro` (diminutivo), `-aima`, `-ima`, `-uco`, `-ubana`, `-uru`… |
| T2 nombres de agente | 8 | `buio`, `bagre`, `cunaro`, `guaranaro`, `dara`, `naure`, `cuna` — **daban nombre a agentes y no puntuaban como caquetío** |
| T3 concreto | 92 | fauna, flora, paisaje, técnica |
| T4 abstracto | 53 | verbos, cualidades |
| T5 topónimos | 45 | `TOPONIMOS_ZAVALA` — **fuera del habla**, referencia de canon |
| T5b antropónimos | 13 | `ANTROPONIMOS_ZAVALA` — idem |
| T6 descartado | 1 | `baquiro` (cumanagoto según el propio Alvarado) |

**Corpus cultural — 7 hechos**: `parentesco-034/035/036` (el vocabulario de
rango *diao* / *apopo* / *boratio*), `geografia_politica-007` ("Curiana:
territorio donde estaban asentados los caquetíos", nota al pie 4),
`geografia_politica-008` (managuanare/managuarire vía González, PLINCODE p. 23),
`creencia-015b` (*Yaracuy* #284 y *Tabicure* #232).

**Correcciones que produjo.** `diao` pasó de "señor de segundo orden" (una
inferencia sin cita) a "señor principal, jefe mayor". `uriacoa` pasó de "título
del cacique mayor" a antropónimo. Ambos son el caso testigo del problema que la
[[PLAN_MAESTRO|auditoría]] persigue.

## Qué falta

1. **F7 — cerrar el resto.** Ojo con la aritmética: el "24% restante" **no son
   68 entradas por parsear**. Son 45 topónimos + 13 antropónimos excluidos **por
   diseño** (están capturados en `lexicon_zavala.py`, solo que fuera del habla),
   1 descartado, y ~2-9 entradas que el regex no capturó. **La tarea real es
   pequeña**: reconciliar 286 parseadas contra las ~288 del PDF.
2. **28 homógrafos con español** (`bagre`, `sabana`, `cana`…) resueltos por
   contexto en `score_linguistico()` — vale una revisión dedicada.
3. **Discrepancia documental**: [[05_geografia_politica_y_sucesion]] §2 dice que
   el glosario tiene **116 entradas**; el PDF tiene ~286-288. Corregir el ensayo.
4. **`guaranaro` estaba resuelto y no nos dimos cuenta**: Zavala lo glosa como
   *"Pez lisa"*, mientras [[02_ecologia]] lo daba por "sin identificación
   taxonómica firme". Igual `cunaro`: Zavala dice *"Pez del golfete de Coro.
   Promicops Guasa"*, frente a la identificación web (*Rhomboplites aurorubens*,
   pargo de altura). Dos glosas distintas para la misma palabra → decidir.
5. **`datihao`** ("padrino de cautivo, el que presta su nombre al esclavo") está
   en el lexicón **sin nota**; hay que ver si viene de aquí y qué relación tiene
   con el *daitiao* de parentesco de [[oliver-1989-cap2]].

## Caveats de método (heredados de la propia fuente)

- Es una **compilación de nueve autores**, no una recolección de campo. Algunos
  fitónimos y zoónimos son voces indígenas de circulación pan-venezolana cuya
  atribución *específicamente caquetía* es más débil que la de un `diao`. Cada
  entrada importada lleva en `notas` el número de glosario y las siglas del
  compilador, para que esa procedencia quede auditable.
- El propio Zavala cita a [[arcaya-1920]], [[alvarado-1921]] y
  [[oviedo-y-banos]] — es decir, buena parte de nuestro "atestiguado" llega
  **de tercera mano**.

## Herramientas

- `curiana_sim/minar_zavala_glosario.py` — parsea, clasifica por tiers, **no
  modifica** el lexicón: emite propuesta.
  - ⚠️ Reporta *"ya presentes: 66 (23%)"* **a propósito**: excluye su propia
    importación para ser idempotente. No es un fallo de la fusión — los 152 sí
    están en `VOCABULARIO_BASE` (verificado).
  - ⚠️ **Bug menor**: revienta con `UnicodeEncodeError` al imprimir los tiers en
    consola Windows (cp1252). Correr con `PYTHONIOENCODING=utf-8`.
- `curiana_sim/lexicon_zavala.py` — generado, no editar a mano.

## Enlaces

[[MOC_geografia_politica]] · [[MOC_creencia]] · [[MOC_motor]] ·
[[05_geografia_politica_y_sucesion]] · [[INDICE_FUENTES]]
