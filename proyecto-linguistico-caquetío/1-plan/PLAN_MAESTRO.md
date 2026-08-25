# Plan maestro — de simulador a base de conocimiento auditada

*Acordado con Miguel el 2026-07-21. Este documento es el mapa; cada sesión de
trabajo desarrolla una pieza y lo actualiza. No es un documento de diseño
técnico (eso va en los DISENO_*.md de cada pieza) sino la hoja de ruta que
las ordena.*

---

## 0. La decisión marco: moratoria de simulaciones

**Las simulaciones quedan EN PAUSA.** Las corridas hasta hoy (6 runs curados,
1489 respuestas) cumplieron su función: construir y depurar el motor. La
auditoría del 2026-07-20 demostró dos cosas a la vez:

1. El motor tenía 5 bugs estructurales que sesgaban todo run (ya arreglados,
   con 13 tests de regresión — commits `9929edf`, `b405729`).
2. La base de conocimiento sobre la que corre tenía huecos de fidelidad
   serios: el glosario de Zavala importado al 23%, etiquetas contradiciendo a
   sus propias fuentes (`diao`, `uriacoa`, `paugis`), "huecos léxicos"
   declarados que estaban atestiguados en PDFs del propio repo.

Correr más simulaciones ahora produciría datos que habría que descartar cuando
la base cambie. Primero la base; después el experimento. El criterio para
levantar la moratoria está en §6.

**El patrón que justifica todo este plan:** cada vez que miramos una pieza en
profundidad (motor, glosario, etiquetas), encontramos deuda. La respuesta no es
mirar menos: es construir la infraestructura para que la deuda sea *visible*
(vault, backlinks, validadores, dashboards de cobertura) en vez de descubrirse
por accidente.

---

## 1. Eje FIDELIDAD — auditar fuentes, lexicón y corpus ("no vender humo")

**Objetivo:** que cada palabra del lexicón y cada hecho del corpus sea
trazable a su fuente con cita verificable, o esté explícitamente marcado como
reconstrucción/hipótesis. Sin excepciones silenciosas.

**Estado medido (2026-07-21):**

- 314 entradas de familia caquetía en el lexicón; **82 sin nota/cita alguna**
  (incluye palabras centrales: `buco`, `piache`, `coro`, `curiana`,
  `chiriguare`, `maure`, `pauji`).
- **9 pares c/k** sospechosos de duplicado con etiquetas de fuente distintas
  (`buco`/`buko`, `cati`/`kati`, `cazi`/`kali`, `canoa`/`kanoa`…).
- 21 valores distintos de `fuente` en el dato crudo (la doc dice 8;
  `normalize_source_language()` los absorbe, pero el dato debería sanearse).
- Cobertura de Zavala 2015: 76% (era 23%). Las demás fuentes: sin medir.

### 1.1 Inventario y estado de minado de las fuentes

> 📌 **La tabla viva de esta sección vive ahora en
> [`4-fuentes/INDICE_FUENTES.md`](../4-fuentes/INDICE_FUENTES.md)**,
> con una nota por obra en `4-fuentes/` (V1, hecho el 2026-07-29).
> Lo de abajo se conserva como el estado *creído* en 2026-07-21; el inventario
> medido corrigió tres cosas de fondo:
>
> 1. **Alvarado 1921 SÍ tiene capa de texto** (704 KB extraíbles con
>    `pdftotext -enc UTF-8`; lo que fallaba era `pypdf`). **F3 no está bloqueada
>    por OCR.** Igual valía ya para Arcaya y Jahn.
> 2. **Oviedo y Baños está disponible**: el archivo de 0 bytes era
>    `Oviedo_Banhos_1885_...` (ya borrado); el gemelo
>    `Oviedo_Banhos_Conquista_Poblacion_...` tiene 519 páginas con texto.
> 3. **Había 6 archivos de 0 bytes, no uno** (Brinton PDF, Fernandes 2020,
>    Oviedo y Baños 1885, Perea Alonso duplicado, Ramos Pérez, Rouse & Cruxent),
>    y un archivo cuyo **nombre no correspondía a su contenido**
>    (`Schroeder_et_al_2018_PNAS_...` era en realidad Moreno-Mayar et al.,
>    *Science* 2018).
>
> El lote de higiene del 2026-08-04 (#53, #54, #55) cerró los tres duplicados
> y el nombre falso: hoy quedan **4 archivos de 0 bytes**, todos huecos reales.
>
> Además, medido sobre el dato: de las 233 entradas `caquetío-atestiguado`,
> **164 citan a Zavala** y las tres fuentes ALTA sin minar (Alvarado, Van Buurt,
> Gatschet) tienen penetración **cero**.

`fuentes_caquetios/` tiene 30 archivos. Estado conocido (2026-07-21):

| Fuente | Tipo | Estado de minado | Prioridad |
|---|---|---|---|
| Zavala Reyes 2015 (*Palabras Vivas…*) | glosario caquetío (286 entradas) | **76%** — `minar_zavala_glosario.py` | cerrar el 24% restante (20 entradas de parseo manual) |
| Alvarado 1921 (*Glosario de voces indígenas*) | glosario nacional | **sin minar** | **ALTA** — es un glosario entero; fuente directa de lexicón |
| Gatschet 1885 (2 txt, Aruba) | vocabulario caquetío de Aruba | citado, no minado sistemáticamente | **ALTA** — vocabulario insular directo |
| Oliver 1989 cap. 2 (Linguistics) | cognados y fonología | parcialmente (daitiao, diao) | **ALTA** — pilar de la Capa 2 |
| Van Buurt 2014 (txt) | palabras caquetías en papiamento | citado, no minado | ALTA — léxico superviviente |
| Jahn 1927 | etnografía + vocabularios comparados | parcial (parentesco, pp. 171-173, 438-9) | media — OCR desigual |
| Oliver 1989 cap. 3 (Ethnohistory) | etnohistoria política | bien minado (sesiones 1 y 5) | media — barridos temáticos restantes |
| Arcaya 1920 | historia de Falcón | vía citas de Zavala; extracción OCR mala | media — requiere OCR externo |
| Brinton 1871 | comparativa arahuaca | **minado** (4 pares LK-TN, bug REGLAS_LK_TN) | hecho |
| Adam 1879 | habla hombres/mujeres caribe | minado (sesión 1, kalinago) | hecho |
| Camacho 2011, Antczak 2015/2017, Rouse & Cruxent 1963 | ciencia natural/arqueología | minados (sesión 2) | hecho |
| Guerra Curvelo (palabrero wayuu) | comparanda normativa | base de PROGRAMA_WAYUU | programa aparte |
| Las Casas 1875, Oviedo y Valdés 1851, Anglería 1892 (v1, v4) | crónicas | apenas tocados | media-baja — barrido dirigido (religión, Curiana, Coro) |
| Gilij 1780/82/83 (3 vols, italiano) | arahuaco del Orinoco | sin minar | baja — comparanda lejana |
| Perea Alonso 1942 (2 copias) | gramática lokono | evaluado: no comparativo | descartado (documentado) |
| Oviedo y Baños 1885 | crónica | **PDF corrupto** ("empty file") | conseguir copia legible |
| Ramos Pérez 1978 (reseña) | reseña | citado vía Oliver | baja |

**Tareas del eje** (cada una es una sesión del tipo "auditoría Zavala"):

1. **F1. Censo de citas del lexicón**: las 82 entradas sin nota → buscar cita
   en las fuentes ya minadas; la que no aparezca se **degrada** de etiqueta
   (misma disciplina que las 441 hipotéticas). Guion: el retag documentado,
   como `retag_nucleo_fundacional.py`.
2. **F2. Resolver los 9 pares c/k**: una política ortográfica única (¿grafía
   colonial c/qu o fonológica k?), un lema canónico por concepto, el otro como
   variante con referencia cruzada — no dos entradas con etiquetas distintas.
3. **F3. Minar Alvarado 1921** (glosario completo, con el protocolo de 6
   filtros de descarte que ya está escrito para el habla paraguanera —
   `5-experimento/disenos/02_protocolo_habla_paraguanera.md` — que aplica casi
   idéntico: la mayor parte de Alvarado NO será caquetío).
4. **F4. Minar Gatschet 1885** (vocabulario de Aruba: caquetío insular directo).
5. **F5. Minar Oliver cap. 2 sistemáticamente** (cognados → alimenta
   `COGNADOS`, hoy 37 entradas, y la validación de la Capa 2).
6. **F6. Minar Van Buurt 2014** (papiamento: léxico caquetío superviviente).
7. **F7. Cerrar Zavala al 100%** (las ~20 entradas de parseo manual).
8. **F8. Sanear los 21 valores de `fuente`** a un conjunto canónico declarado.
9. **F9. Conseguir Oviedo y Baños legible** + OCR externo para Arcaya/Jahn si
   hace falta (el entorno no tiene OCR — limitación conocida).
10. **F10. Verificación de citas del corpus cultural**: los ~156 hechos con
    `referencia` → comprobar que la cita resuelve (página/entrada existe).
    Muestreo primero; exhaustivo donde haya dudas.

**Regla de cierre del eje**: una entrada/hecho está "auditado" cuando su
`referencia` apunta a fuente + localización verificable, o su etiqueta admite
explícitamente que no la tiene. "Auditado" es un estado binario y medible —
el dashboard del vault (§2) lo muestra como % de cobertura.

---

## 2. Eje VAULT — el repo como second brain (Obsidian)

**Objetivo:** control visual de lo construido. Que Miguel pueda VER el corpus,
navegar de un hecho a su fuente y de una fuente a todo lo que sostiene, y
detectar de un vistazo qué está flaco. **Regla arquitectónica: el vault ES el
repo.** Nunca un silo paralelo; git sigue siendo el historial.

**Por qué encaja:** la epistemología del proyecto ya es frontmatter (`fuente`,
`referencia`, `dominios`, `agentes_relacionados`); los backlinks son la cadena
de custodia epistémica en dirección inversa (fuente → hechos que la usan =
cobertura visible, exactamente lo que habría delatado el 23% de Zavala); y el
corpus **aún no lo consume ningún código**, así que reestructurarlo cuesta
cero roturas. Ese timing no vuelve.

**Decisión de herramienta (2026-07-29, pregunta de Miguel: ¿Obsidian o clon
propio?):** Obsidian, y sin costo. Sus productos pagos no tocan este plan —
Sync se reemplaza por git+OneDrive, Publish por nuestro Next.js (que además es
imprescindible para llms.txt/JSON-LD/URLs propias del jardín), y el uso
comercial es gratuito desde 2024. El seguro anti-lock-in no es la herramienta
sino el formato: markdown plano + frontmatter en git, legible por lentes
libres (Foam, SilverBullet, VS Code) sin migración. Un clon propio sería años
de producto ortogonal a la misión; la única "vista propia" que vale la pena
construir es el jardín público (J3), que ya está en el plan y es 100% nuestro.
La lógica crítica (validación) vive en `compilar_corpus.py`, nunca en plugins.

**Fases** (0 y 1 son baratas y sin riesgo; la 2 cambia el formato canónico):

- **V0. Repo como vault** — ✅ **hecho (2026-07-29)**: `.obsidian/` y `.trash/`
  al gitignore (commit `02f4d0d`); nota raíz [`INDICE.md`](../INDICE.md); seis MOCs
  en [`3-mundo/`](../3-mundo/) (familia / ecología / creencia / transmisión / geografía
  política + motor); frontmatter y bloque de navegación con wikilinks en los 5
  ensayos y en las 5 hojas de fuentes.
- **V1. Notas por fuente** — ✅ **hecho (2026-07-29)**: 24 notas en
  [`4-fuentes/`](../4-fuentes/) (18 obras locales + 6
  fuentes externas que sostienen 27 hechos y no están en el repo), más
  [`INDICE_FUENTES.md`](../4-fuentes/INDICE_FUENTES.md) con el estado
  medido de cada una, y la nota viva
  [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision).
  Guardián: `python check_vault_links.py --strict` (581 wikilinks,
  todos resuelven). **Aquí es donde el eje FIDELIDAD escribe sus resultados**:
  cuando F3 mine Alvarado, el resultado va a `fuentes/alvarado-1921.md`, no a un
  markdown nuevo.
- **V2. Atomizar el corpus**: ~156 hechos → una nota por hecho con
  frontmatter; los YAML actuales se retiran cuando el compilador los
  reproduzca. Incluye **`compilar_corpus.py`**: valida frontmatter (etiquetas
  legales, `agentes_relacionados` existentes en `curiana_agents.py`,
  referencias cruzadas resolubles) y emite el YAML fusionado para cuando la
  simulación lo consuma. Con tests. *Hoy nada valida el corpus — este es el
  equivalente cultural de los tests del motor.*
- **V3. Notas agregadoras**: una por agente (ficha + genealogía + hechos que
  lo citan + palabras firma — el "grosor" que buscaba el programa desde el
  inicio), Canvas del árbol de linajes, nota por palabra **solo** para las
  atestiguadas (232, generables desde el lexicón, solo-lectura).
- **V4. Dashboards Dataview**: % auditado por fuente, hechos por etiqueta
  epistémica, huecos léxicos abiertos, decisiones pendientes.

**Dependencia**: V1 es el vehículo de F1-F10. Conviene V0+V1 antes de
arrancar las auditorías en serio, para que sus resultados aterricen en notas
y no en más markdown suelto.

---

## 3. Eje JARDÍN — la presentación pública que sí funcione

**Diagnóstico compartido:** `/kaketiana` está bien construido pero cuenta *el
experimento*. Tras varias vueltas sigue sin sentirse efectivo porque el
experimento es solo una parte — y no la más enlazable — de lo que el proyecto
tiene. **La investigación ES el contenido**: diao/apopo/boratio, Todariquiba,
la genealogía matrilineal, el buco de los 5.000, "por qué Venezuela se llama
Venezuela desde el Golfete", el diccionario atestiguado con su epistemología
de 5 etiquetas. Eso es lo que genera links.

**La tesis del jardín digital:** muchas páginas chicas, densas, interlazadas y
citables — una por palabra atestiguada, por personaje, por hecho, por fuente —
en vez de pocas páginas largas. Ese formato es exactamente el que:

- genera **tráfico humano** de cola larga (búsquedas específicas: "significado
  de Todariquiba", "palabras caquetías en papiamento", "cacique Manaure");
- genera **tráfico e citación de agentes/LLMs**: páginas con estructura
  semántica limpia, fuentes citadas, URLs estables, `llms.txt`, JSON-LD y
  sitemap se convierten en LA referencia que los modelos citan cuando alguien
  pregunta por el caquetío. Hoy esa referencia no existe en la web.

**El pipeline natural:** vault (V2/V3, curado y validado) → generación
estática en el Next.js existente (curiana-radio.vercel.app). Los wikilinks del
vault se vuelven links reales del sitio. La simulación pasa a ser *un capítulo*
del jardín ("¿y si esta lengua volviera a hablarse?"), no la portada.

**Tareas:**

1. **J1. Sesión de diseño editorial** (conversación, no código): mapa del
   jardín — qué tipos de página, qué URL scheme, qué se publica y qué no
   (la genealogía propuesta, p. ej., no se publica hasta el veto). Decidir
   también el papel de imágenes: mapas del área de influencia, Canvas de
   linajes exportado, ilustraciones marcadas como "reconstrucción artística"
   (misma honestidad epistémica: una imagen también lleva etiqueta).
2. **J2. Infraestructura agente-amigable**: llms.txt, JSON-LD, sitemap
   extendido, páginas de fuente citables. (Nota: el problema de egress que
   mató el dashboard viejo no aplica — todo esto es estático.)
3. **J3. Pipeline vault→sitio** (después de V2): generador de páginas desde
   las notas con frontmatter.
4. **J4. Métricas**: Vercel Analytics + Search Console para saber si el
   tráfico llega — sin datos, "efectivo" seguirá siendo una sensación.
5. **J5. Documento de motivo de negocio** (stub aparte, en el repo de Curiana
   Radio, no aquí): autofinanciamiento — donaciones, patrocinio cultural,
   fondos de patrimonio, eventualmente artefactos (un diccionario impreso).
   Solo documentar el motivo; no es tarea de este plan desarrollarlo.

---

## 4. Eje MOTOR — congelado, con dos decisiones pendientes

El motor queda como está (sano, testeado). No se toca salvo:

- **M1 (decisión):** `normalizar_por_dialecto()` — cablearla (y re-correr
  todo cuando se reanuden las simulaciones) o eliminarla. Documentada en
  `curiana_social.py`.
- **M2 (decisión):** persistencia de efectos sin decaimiento (la sal abundante
  se queda abundante) — modelar consumo/regresión a la media o aceptarlo.
- **M3 (mantenimiento):** los 45 tests siguen siendo el guardián; cualquier
  cambio futuro pasa por ellos.

---

## 5. Decisiones abiertas

> ✅ **Movidas a la nota viva [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision)**
> (2026-07-29). Ahí está el estado de cada una, qué necesita Miguel para
> decidirla y qué desbloquea. **D6 está resuelta** (el PR #30 ya estaba mergeado:
> commit `609f9b5`). Dos decisiones nuevas salieron del inventario de fuentes:
> **D7** (¿manda la glosa histórica o la identificación científica moderna
> cuando difieren?) y **D8** (¿el repo archiva copias de las fuentes externas?).
> La tabla de abajo se conserva como el estado original del plan.

| # | Decisión | Contexto | Bloquea |
|---|---|---|---|
| D1 | **Veto de la genealogía** (linajes, Waimo-ko, 14 personas de fondo) | `cultura/genealogia.yaml` | V3 (notas-agente), J1 (qué se publica) |
| D2 | **El nombre "Curiana"** (¿territorio, asentamiento, o ambigüedad documentada? candidato: Todariquiba para el asentamiento) | ensayo 05 §8 | J1 (naming público) |
| D3 | `normalizar_por_dialecto` (M1) | `curiana_social.py` | reanudación de sims |
| D4 | Segundo sobrino de Manaure (pluralidad de candidatos) | `parentesco-039` | D1 |
| D5 | Política ortográfica c/k del lexicón | 9 pares duplicados | F2 |
| D6 | Merge del **PR #30** — la rama acumula corpus + sesión 5 + Zavala + motor; conviene mergear ANTES de arrancar el vault para no seguir apilando | github | todo lo demás |

## 6. Criterios para reanudar simulaciones (el "gate")

> 📌 **Ampliado el 2026-08-03.** El gate de abajo sigue vigente, pero la
> auditoría añadió tres condiciones nuevas (la glosa de `-bana`, el desbalance
> wayunaiki/lokono, y reparar el exportador de runs) y un protocolo experimental
> completo. Ver **[`5-experimento/disenos/04_protocolo_run_1_era_auditada.md`](../5-experimento/disenos/04_protocolo_run_1_era_auditada.md)**.
>
> Y una decisión de encuadre: **los 6 runs existentes quedan formalmente
> declarados pruebas de desarrollo del motor**, no resultados — no son
> comparables entre sí porque el instrumento de medición cambió entre ellos.
> Análisis en [`5-experimento/analisis/01_que_probaron_los_seis_runs.md`](../5-experimento/analisis/01_que_probaron_los_seis_runs.md).

Se reanudan cuando **todas** estas condiciones se cumplan — y el primer run
nuevo será el "run 1 de la era auditada":

1. Lexicón: 0 entradas de familia caquetía sin cita o sin degradar (F1), pares
   c/k resueltos (F2), y las 3 fuentes ALTA minadas (F3, F4, F5).
2. Corpus: validador `compilar_corpus.py` en verde (V2) y citas verificadas
   al menos por muestreo (F10).
3. Decisiones D1, D3 y D5 tomadas.
4. El re-export del sitio se hace DESPUÉS de ese primer run limpio — nunca
   desde los runs pre-auditoría (los actuales quedan como material de
   desarrollo del motor, documentados como tales).

## 7. Orden sugerido de sesiones (backlog para ir tomando)

1. ~~**D6** — mergear PR #30~~ ✅ hecho (commit `609f9b5`).
2. ~~**V0 + V1** — vault mínimo + notas por fuente + DECISIONES ABIERTAS~~
   ✅ hecho el 2026-07-29 (ver §2). **Siguiente paso: F1.**
3. ~~**F3, F4, F6, F7** — minería en paralelo~~ ✅ hecho el 2026-08-03, **antes
   que F1 y no después**: 70 de las 82 entradas sin cita tenían rastro en esas
   fuentes, así que censarlas primero habría degradado palabras con respaldo.
4. **F1** — censo de citas, ahora con evidencia. Corre
   `python curiana_sim/auditar_82.py`: **61 confirman · 13 reclasifican · 3
   conflicto de glosa · 5 sin rastro**, 77 de 82 adjudicables. Incluye aplicar
   las 62 citas de Zavala y decidir D10.
5. **F2 + D5** — política c/k y deduplicación (1 sesión; medido: solo 2
   duplicados reales dentro del caquetío).
6. **F5** — Oliver cap. 2, la **única fuente ALTA del gate que queda**.
7. **J1** — sesión de diseño editorial del jardín (conversación).
8. **V2** — atomización del corpus + validador (1-2 sesiones, revisar antes).
9. **V3 + V4** — notas agregadoras y dashboards.
10. **J2, J3** — jardín público.
11. Gate §6 → reanudar simulaciones → re-export del sitio.

Los ítems 3-7 son paralelizables como las sesiones del programa cultural
(spawn de sesiones independientes, una por fuente, con el patrón triple
entregable que ya funcionó).

---

*Historial: creado 2026-07-21 tras la auditoría del motor y del lexicón
(commits `a84a52d`, `9929edf`, `b405729` en `feat/corpus-cultural`, PR #30).*

*2026-08-03 — **tanda de minería F3/F4/F6/F7 en paralelo**. Zavala cerrado al
100% (288/288); Alvarado, Gatschet y Van Buurt minados por primera vez. Las
cuatro emiten propuesta sin tocar `curiana_lexicon.py`; `auditar_82.py` las
cruza. El saldo tiene dos caras: 61 entradas del lexicón ganan cita, y **13
resultan no ser caquetías** según la fuente que debía sostenerlas — `piache`
entre ellas. Decisiones nuevas: D9 (glosa de `-bana`) y D10 (qué hacer con las
13). Ver `4-fuentes/INDICE_FUENTES.md`.*

*2026-07-29 — **V0 y V1 ejecutados**. El vault existe: `INDICE.md`, 6 MOCs, 24
notas de fuente con estado medido, [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision) y un verificador de
enlaces. El inventario de disponibilidad corrigió tres supuestos del §1.1
(Alvarado legible, Oviedo y Baños disponible, 6 archivos de 0 bytes) y midió la
cobertura real del lexicón por fuente — que es, en una tabla, el argumento del
eje FIDELIDAD. Ver `4-fuentes/INDICE_FUENTES.md`.*
