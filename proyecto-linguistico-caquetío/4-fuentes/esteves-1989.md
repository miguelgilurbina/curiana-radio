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

## Lo minado hasta ahora — 10 de 146 páginas

> 🔴 **Barrido en curso.** Lo de abajo sale de las páginas 11-16 y 25 del libro.

### ⭐ Los cuatro hallazgos que ya cambian algo

**1. `jadicuar` resuelto — y contra la hipótesis que teníamos.**

`toponimos.yaml` tiene `jadicuar` sin glosa, y yo lo había marcado como posible
variante de **Jadacaquiva**. Es falso. Esteves (p. 14):

> ADÍCORA — *"El nombre primitivo era **Jadícuar**, que quiere decir: jajatal,
> sitio donde abunda el jajato, hierba halófila de terrenos salobres. Este
> Jadícuar, por uno de esos curiosos procesos de selección eufónica, ha venido
> cambiando de Jadícuar a Jadícora, de Jadícora a Jatícora, hasta llegar al
> sugestivo y poético Adícora de hoy."*

Es **el nombre indígena de Adícora**, con la cadena de cambio completa. Sirve
para subir `nodo-012` en `3-mundo/asentamientos.yaml`, que hoy está como
`reconstruido` porque solo teníamos el nombre.

**2. Una serie morfológica de apellidos caquetíos — con Manaure dentro.**

Esteves (p. 13) lista *"algunos de los apellidos de la gran familia caquetía"*:

> **Adaure · Timaure · Yaraure · Chunaure · Manaure**

Cinco formas en `-aure`. `toponimos.yaml` ya tenía `timaure` ('Apellido') y
`tumarure` ('Apellido de un cacique') sueltos y sin explicar; ahora hay serie.
Toca directamente al personaje central del elenco.

> ⚠️ Esteves **no** analiza `-aure` como morfema ni da su significado. La serie
> es suya; el análisis sería nuestro y sería `hipotetico`.

**3. 🔴 Amuay no sería caquetío: Esteves lo atribuye al caribe insular.**

> AMUAY (p. 16) — *"La voz da la idea de cavidad subterránea, haitón, cueva
> grande… **Por su fonética la voz pertenece al caribe insular**, como batey,
> mamey, caney, carey"*.

Es un topónimo **de Paraguaná** atribuido a otro estrato lingüístico. Va
directo a [[esfera-de-interaccion]]: la sociedad no era monoétnica y la lengua
no era homogénea. El lexicón ya tiene las categorías `kalinago` (19) y
`kalinago-caribe-overlay` (4) donde esto encajaría.

**4. Un documento de 1556 con voz indígena, citado textual.**

Petición de los **indios amuayes** al obispo Gerónimo de Ballesteros pidiendo
cambiar de santo patrono:

> *"A vos, Gerónimo, que sos nuestro Obispo y Amo, te pedimos dos cosas. La
> primera: es un buen santo para nuestro Patrón, pues nosotros no queremos a
> San Juan, pues como está desnudo, no va a querer que llueva para no tener
> frío. La segunda: Danos otro cura, que no sea cobarde como el que tenemos,
> que en cuanto vio venir el verano se largó…"*

**Ballesteros es el mismo obispo cuya carta de 1550 ya citamos** vía Oliver
(`geografia_politica-004/005`, el canal del `buco` y los 14-15 mil indios).
Esteves añade que fue el **segundo obispo de Coro** y que murió allí en 1558.

> ⚠️ Esteves **no da la referencia de esta petición**. Menciona la compilación
> del Coronel José Félix Blanco, *Documentos para la Historia del Libertador*
> (1875), pero en la frase siguiente y aplicada al dato de la lápida. **Hay que
> perseguir la fuente antes de usarla**: una cita sin procedencia de un texto
> tan bueno es exactamente donde conviene desconfiar.

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
| **Adaure** | aldea al oeste de Buenavista | censo 1881: **87 casas, 522 vecinos** — mayor que muchas cabeceras de municipio. **Martí 1773 citado textual**. Aníbal Hill Peña los da como "tribu belicosa" |
| **Adícora** | capital de municipio, costa oriental | ⭐ antes **Jadícuar** = 'jajatal' (ver arriba) |
| **Aguaque** | fundo a dos leguas al norte de Pueblo Nuevo | de *guaco*, portulácea. Casa natal de Josefa Camejo; Monumento Histórico desde 1982 |
| **Amaraya** | aldea al sur de Jadacaquiva | censo 1881 (como *Amaralla*): 16 casas, 108 vecinos. ¿de *maracaya*, el "güirito", gato silvestre? |
| **Amuay** | bahía y población, municipio Los Taques | censo 1881: 8 casas, 60 vecinos → ~400 casas y 3.000 hab. al escribir. 🔴 **atribuido al caribe insular** |
| **Antuni** | lugar pecuario al norte de Jadacaquiva | Esteves **duda que sea indígena** |
| **Buenibativa** | caserío San Pedro, municipio Adícora | de *Guanibativa*; `bativa` sin explicar |
| **Caibacoa** | sabana al oeste del fundo de Aguaque | `cái` (< *guay*, árbol tipo ceiba) + `bacoa` |
| **Camare** | municipio Pueblo Nuevo | censo 1881: 8 casas, 48 vecinos |
| **Camoruco** | cerca de Caradacagua, oeste de Pueblo Nuevo | antes *Semeruco* |

Y aparecen como referencia geográfica: **Moruy · Jadacaquiva · Los Taques ·
Adícora · Pueblo Nuevo · San Pedro · Aguaque · Caradacagua · Urupaguaduco ·
Buenavista**.

### Más fuentes que cita, según avanza el barrido

| Fuente | Dónde | Qué aporta |
|---|---|---|
| **Aníbal Hill Peña**, historiador | p. 13 | los adaures como "tribu belicosa"; Esteves dice tener papeles de sus peleas contra los españoles |
| **José Félix Blanco (Cor.)**, *Documentos para la Historia del Libertador* (1875) | p. 16 | compilación por decreto de Guzmán Blanco |
| **Obispo Gerónimo de Ballesteros** | p. 16 | 2.º obispo de Coro, † Coro 1558. **El mismo de la carta de 1550** que ya citamos vía Oliver |

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

- **136 de 146 páginas.** El barrido completo es el trabajo de #92.
- ✅ ~~Comprobar `jadicuar` ↔ Jadacaquiva~~ — **resuelto y descartado**: es el
  nombre primitivo de **Adícora**.
- Perseguir a **Martí 1773** y a la petición de 1556, que Esteves cita sin dar
  procedencia.
- Hay un **Apéndice** con un artículo "Sobre el Nombre de Adícora" (remitido
  desde la p. 14). Localizarlo — probablemente en el archivo 6.

## Enlaces

[[INDICE_FUENTES]] · [[arcaya-1920]] · [[zavala-reyes-2015]] · [[toponimia]] · [[esfera-de-interaccion]] · [[mapa-ecologia]]
