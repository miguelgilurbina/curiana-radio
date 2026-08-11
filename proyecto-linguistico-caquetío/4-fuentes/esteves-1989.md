---
tipo: fuente
obra: esteves-1989
autor: Juan de la Cruz Esteves
titulo: "Topónimos indígenas de Paraguaná y otros topónimos indígenas del estado Falcón"
lugar_año: "Caracas, 1989"
editor: Refinería de Amuay de Lagoven S.A.
estado_minado: parcial
prioridad: alta
medido: 2026-08-11
sostiene: []
---

# Esteves 1989 — Topónimos indígenas de Paraguaná

> **Qué es.** El gazeteer de Paraguaná que al proyecto le faltaba. 146 páginas
> de entradas topónimo por topónimo, con ubicación, censo y etimología
> propuesta. Es **la fuente que desbloquea [#92](https://github.com/miguelgilurbina/curiana-radio/issues/92)** —
> los poblados de Paraguaná que hoy no se pueden meter en `asentamientos.yaml`.

## Ficha

| | |
|---|---|
| Autor | **Juan de la Cruz Esteves** — cronista, poeta e investigador de Paraguaná |
| Título | *Topónimos indígenas de Paraguaná y otros topónimos indígenas del estado Falcón* |
| Publicación | Caracas, 1989 · patrocinada por la **Refinería de Amuay de Lagoven S.A.** |
| Otra obra suya | *Paraguaná histórica y geográfica* (misma colección) |
| Procedencia | Enviado por Nery R. Gil el 2026-07-27, seis PDF escaneados |

> ⚠️ **La grafía del apellido es `Esteves`, con -s.** El nombre de los archivos
> dice "Estevez"; la portada, la portadilla y la introducción de Lagoven dicen
> **Esteves**. Manda la fuente.

## Estatus epistémico: pista fuerte, autoridad débil

**No es una obra académica.** Esteves es el **cronista** de Paraguaná: recoge de
historiadores y cronistas locales, de archivos parroquiales y de saber
transmitido. Eso le da un valor que ninguna fuente académica del repo tiene
—conoce los lugares y los papeles locales— y una debilidad que hay que declarar:
**sus etimologías son propuestas suyas, no análisis lingüístico.**

Cómo entra cada cosa, entonces:

| Lo que dice | Cómo entra |
|---|---|
| Cita un documento con nombre (censo, visita pastoral, libro de bautizos) | se persigue hasta el documento; ahí sí puede ser `atestiguado` |
| Ubicación de un lugar, censo de casas y vecinos | `atestiguado` con la fecha del censo |
| Etimología propuesta sin cita | `hipotetico` — es una propuesta de un cronista, no un despeje |
| **Corrobora un morfema que ya teníamos** | ⭐ eso es lo que más rinde: segunda atestación independiente |

## 🔑 Las fuentes que Esteves usa — lo que hay que perseguir

Esto es lo más valioso de la obra para el proyecto: **es un puente hacia
documentos de archivo que no tenemos.**

| Fuente que cita | Qué es | Prioridad |
|---|---|---|
| ⭐ **Visita Pastoral del obispo Mariano Martí (1773)** | Fuente **colonial primaria**. Martí recorrió y describió las parroquias de Venezuela. Oliver 1989 ya lo cita como "Martí 1969" (la edición moderna) | **alta** |
| **Censo de 1881** | Casas y vecinos poblado por poblado. Aparece en casi cada entrada | alta |
| **Libros de bautizos parroquiales** — Jadacaquiva, 1835-1842, cura José María Valbuena | Registro nominal local | media |
| **"Antiguos papeles de la posesión de Urupaguaduco"** | Títulos de tierra coloniales | media |
| **Pedro Manuel Arcaya Madriz** | Ya lo tenemos: [[arcaya-1920]]. Esteves señala que la casa de Acaboa fue de sus ascendientes | — |

> **Martí 1773 es el que hay que conseguir.** Es el único de la lista que es
> colonial y primario, y ya está citado por Oliver, así que la edición moderna
> existe y es rastreable.

## ⚠️ Advertencia de época, la de siempre

Las fuentes de Esteves son de **1773, 1835-1842 y 1881**. Eso es *más lejos* del
precontacto que la carta de Bastidas (1538), no más cerca.

**Nada de esta obra puede sostener `precontacto: si`** en
`3-mundo/asentamientos.yaml`. Lo que sí hace, y es mucho, es dar el **inventario
de topónimos** y su ubicación — que es justo lo que [#92](https://github.com/miguelgilurbina/curiana-radio/issues/92)
necesita para dejar de tener a Paraguaná vacía.

## Lo minado hasta ahora — 6 de 146 páginas

> 🔴 **Barrido apenas empezado.** Lo de abajo sale de las páginas 11-12 y 25.

### Morfemas que corroboran el lexicón

| Morfema | Glosa de Esteves | Estado en el repo |
|---|---|---|
| ⭐ **`bacoa`** | 'lugar, paraje' | **CORROBORADO** — el lexicón dice 'bosque, lugar, paraje, sitio fértil'. Es nuestro morfema más productivo (`adabacoa`, `guadabacoa`, `quibacoas`, `yacarebacoa`, `sazaribacoa`) y esta es una **segunda atestación independiente** |
| **`ure`** | 'raíz' — y dice que está *"presente en muchos topónimos indígenas de Paraguaná"* | 🆕 nuevo — candidato a morfema productivo |
| **`bara`** | 'árbol' | 🆕 |
| **`guani`** | 'abeja' (mansa, sin aguijón) | 🆕 |
| **`dabuda`** | 'barro de loza' (greda de cerámica local) | 🆕 |
| **`dara`** | alcaraván, *Charadrius* (ave) | 🆕 |
| **Semeruco** | Esteves lo da como nombre anterior de Camoruco | corrobora `cemirucos → 'Semerucos'` de `toponimos.yaml` |

### Topónimos con ubicación y censo

| Topónimo | Qué es | Dato |
|---|---|---|
| **Abudure** | aldea al SO de Moruy | censo 1881: 6 casas, 50 vecinos. `dabuda`+`ure` = 'sitio de donde se extrae barro de las raíces' |
| **Acaboa** | lugar pecuario, municipio Jadacaquiva | censo 1881: 2 casas, 11 vecinos. **Oratorio en 1773 (Martí)** |
| **Adaro** | Punta de Adaro, costa occidental, Los Taques | de `dara`, con prótesis vocálica y disimilación a>o |
| **Buenibativa** | caserío San Pedro, municipio Adícora | de *Guanibativa*; `bativa` sin explicar |
| **Caibacoa** | sabana al oeste del fundo de Aguaque | `cái` (< *guay*, árbol tipo ceiba) + `bacoa` |
| **Camare** | municipio Pueblo Nuevo | censo 1881: 8 casas, 48 vecinos |
| **Camoruco** | cerca de Caradacagua, oeste de Pueblo Nuevo | antes *Semeruco* |

Y aparecen como referencia geográfica: **Moruy · Jadacaquiva · Los Taques ·
Adícora · Pueblo Nuevo · San Pedro · Aguaque · Caradacagua · Urupaguaduco**.

### 👍 Un punto a favor del método de Esteves

En `Acaboa` **rechaza** la etimología de *Caoba* "porque este árbol no existe en
la flora autóctona de Paraguaná". Es exactamente el tipo de control ecológico
que el proyecto aplica en [[mapa-ecologia]]. No es un cronista que acepte
cualquier cosa.

## Cómo se lee esta fuente

Los PDF **no tienen capa de texto**: son fotos de CamScanner y `pdftotext` solo
devuelve la marca de agua. Se leen extrayendo la imagen embebida de cada página
y mirándola:

```bash
python <scratchpad>/extraer_paginas.py <pdf> <desde> <hasta> <destino>
```

Los seis archivos son **contiguos y sin solapamiento**, por tramos de página del
libro: 1-25 · 25-55 · 55-72 · 72-100 · 100-129 · 129-final.

## Lo que falta

- **140 de 146 páginas.** El barrido completo es el trabajo de #92.
- Comprobar si **`jadicuar`** de `toponimos.yaml` tiene algo que ver con
  **Jadacaquiva**. Parecerse no es evidencia.
- Perseguir a **Martí 1773**.

## Enlaces

[[INDICE_FUENTES]] · [[arcaya-1920]] · [[zavala-reyes-2015]] · [[toponimia]] · [[esfera-de-interaccion]] · [[mapa-ecologia]]
