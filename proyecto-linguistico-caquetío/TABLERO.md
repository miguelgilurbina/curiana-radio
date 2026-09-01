---
tipo: tablero
generado_por: curiana_sim/generar_tablero.py
editar_a_mano: no
---

# Tablero de estado — Curiana

> ⚠️ **Archivo generado. No se edita a mano.** Cada número de abajo se
> mide contra el dato en el momento de generar; ninguno se copia de la
> documentación. Para regenerarlo:
> ```
> python curiana_sim/generar_tablero.py
> ```

<!--GENERADO--> Generado el **2026-09-01 12:23**.

## ¿Vamos bien?

|  | Hoy | Referencia |  |
|---|---|---|---|
| Entradas del lexicón **sin cita** | **0** | 82 (2026-07-21) | 🟢 −82 |
| Hechos del corpus **con referencia** | **161 / 161** | — | 🟢 |
| Tests del motor | **206 en verde** | 0 rojos | 🟢 |
| Gate para reanudar simulaciones | **6 de 9** condiciones | faltan 3 | 🔴 |
| Decisiones esperando a Miguel | **9 abiertas** | 4 resueltas | 🟡 |

**Lo que bloquea hoy:** wayunaiki vs. lokono (D11).
Y 2 condición(es) que **nadie puede medir por script**: citas del corpus (F10) · exportador de runs.

Detalle de cada número: [lexicón](#1-el-lexicón) · [fuentes](#2-las-fuentes) · [corpus](#3-el-corpus-cultural) · [gate](#4-el-gate-para-reanudar-simulaciones) · [decisiones](#5-decisiones-e-issues)

---

## 1. El lexicón

Nota: [[lexicon]] · código: `curiana_sim/curiana_lexicon.py`

**1500 entradas activas** en `VOCABULARIO_BASE`.

### Por lengua (categoría normalizada)

| Lengua (`normalize_source_language()`) | n | % del lexicón |
|---|---|---|
| wayunaiki | 781 | 52.1% |
| caquetío | 299 | 19.9% |
| lokono | 275 | 18.3% |
| taíno | 57 | 3.8% |
| paraujano | 47 | 3.1% |
| kalinago | 19 | 1.3% |
| jirajaroide-contacto | 7 | 0.5% |
| proto-arahuaco | 5 | 0.3% |
| caribe-continental | 4 | 0.3% |
| kalinago-caribe-overlay | 4 | 0.3% |
| español-colonial | 2 | 0.1% |

<details><summary>Los 25 valores de <code>fuente</code> en el dato crudo (F8 quiere sanearlos)</summary>

| `fuente` crudo | n |
|---|---|
| wayunaiki | 769 |
| lokono | 247 |
| caquetío-atestiguado | 222 |
| caquetío-reconstruido | 68 |
| paraujano | 47 |
| taíno | 36 |
| kalinago | 19 |
| taino | 18 |
| lokono/proto-arawakan | 14 |
| lokono/garifuna | 13 |
| wayunaiki-cogn | 7 |
| jirajaroide-contacto | 7 |
| caquetío | 6 |
| wayunaiki/lokono | 5 |
| kalinago-caribe-overlay | 4 |
| proto-arahuaco | 3 |
| español-colonial | 2 |
| caribe-cháima | 2 |
| taíno/lokono | 2 |
| proto-arawakan | 2 |
| caquetío-hipotético | 2 |
| caribe-cumanagoto | 2 |
| caquetío-hipotético/topónimo | 1 |
| taíno/caribe | 1 |
| lokono-cogn | 1 |

</details>

### La familia caquetía por capa epistémica

| Capa | n | Qué significa |
|---|---|---|
| `caquetío-atestiguado` | 222 | dato histórico citable a fuente concreta |
| `caquetío-reconstruido` | 68 | vocabulario de trabajo del proyecto |
| `caquetío-hipotético` | 3 | baja de tier por D10 — la lengua no se discute, la confianza sí |
| `caquetío` a secas / topónimo | 6 | sin capa declarada en el campo `fuente` |
| **total familia caquetía** | **299** |  |

Fuera del habla activa: **441** candidatas `hipotético-no-verificado` en `lexicon_candidatos.py` (aisladas el 2026-06-28) y **1** entrada(s) en `FUERA_DEL_HABLA` (`piache`).

### Censo de citas — la deuda de F1

Entradas de familia caquetía **sin nada en `notas`**: **0** (eran 82 el 2026-07-21, PLAN_MAESTRO §1). Lo calcula `curiana_sim/auditar_82.py`, que este tablero importa en vez de duplicar.

### Quién sostiene el «atestiguado»

Cuántas de las 299 entradas de familia caquetía **con `notas`** citan a cada obra. Los patrones de búsqueda salen del `autor` y los `aliases` de cada nota de `4-fuentes/`, así que una obra nueva aparece sola aquí.

| Obra | Entradas que la citan | % de las citadas |
|---|---|---|
| [[zavala-reyes-2015]] | 222 | 74% |
| [[zavala-reyes-2018]] | 222 | 74% |
| [[alvarado-1921]] | 14 | 5% |
| [[oliver-1989-apendice-a]] | 14 | 5% |
| [[oliver-1989-cap2]] | 14 | 5% |
| [[oliver-1989-cap3-vecinos]] | 14 | 5% |
| [[oliver-1989-cap3]] | 14 | 5% |
| [[oliver-1989-cap4]] | 14 | 5% |
| [[van-buurt-2014]] | 13 | 4% |
| [[arcaya-1920]] | 10 | 3% |
| [[arcaya-obra-inedita-1995]] | 10 | 3% |
| [[brinton-1871]] | 4 | 1% |
| [[gatschet-1885]] | 3 | 1% |
| [[oviedo-y-valdes-1851]] | 2 | 1% |
| [[jahn-1927]] | 1 | 0% |
| [[ballesteros-1550]] | 1 | 0% |

Las obras que no aparecen tienen **penetración cero** en el lexicón. Entradas con `notas` que no citan a ninguna obra del vault: **64**.

---

## 2. Las fuentes

Índice: [[INDICE_FUENTES]]. **La nota de cada obra es la fuente de verdad**; esta tabla lee su frontmatter (`estado_minado`, `prioridad`, `capa_texto`, `sostiene`), no una lista cableada.

**55 notas de obra.**

| `estado_minado` | n |
|---|---|
| minado | 24 |
| no-disponible | 13 |
| parcial | 6 |
| segunda-mano | 5 |
| en-curso | 3 |
| sin-minar | 2 |
| descartada | 1 |
| completo-con-reserva | 1 |

**Prioridad ALTA sin minar (13):** [[arcaya-obra-inedita-1995]] (`no-disponible`), [[ballesteros-1550]] (`segunda-mano`), [[brito-figueroa-poblacion-economia]] (`en-curso`), [[esteves-1989]] (`parcial`), [[gonzalez-batista-nombre-de-coro]] (`en-curso`), [[medina-colina-sxx]] (`en-curso`), [[oliver-1989-apendice-a]] (`parcial`), [[oliver-1989-cap3-vecinos]] (`parcial`), [[oliver-1989-cap4]] (`parcial`), [[oviedo-y-valdes-1851]] (`no-disponible`), [[perez-de-tolosa-1546]] (`no-disponible`), [[urbina-jimenez-2007-2011]] (`parcial`), [[zavala-reyes-2015]] (`completo-con-reserva`).

<details><summary>Las 55 notas, una por fila</summary>

| Nota | minado | prioridad | capa texto | lexicón (declarado) | lexicón (medido) | hechos corpus |
|---|---|---|---|---|---|---|
| [[zavala-reyes-2015]] | completo-con-reserva | alta | si | 164 | 222 | 7 |
| [[brinton-1871]] | minado | hecha | si | 84 | 4 | 0 |
| [[jahn-1927]] | minado | media | si | 4 | 1 | 16 |
| [[gatschet-1885]] | minado | alta | si | 4 | 3 | 0 |
| [[oliver-1989-cap3]] | minado | media | si | 2 | 14 | 15 |
| [[oviedo-y-valdes-1851]] | no-disponible | alta | no | 2 | 2 | 7 |
| [[oliver-1989-cap2]] | minado | alta | parcial | 2 | 14 | 2 |
| [[arcaya-1920]] | minado | media | si | 1 | 10 | 13 |
| [[ballesteros-1550]] | segunda-mano | alta | no | 1 | 1 | 0 |
| [[camacho-2011]] | minado | hecha | si | 0 | 0 | 16 |
| [[paz-reverol-2017-2018]] | minado | hecha | — | 0 | 0 | 9 |
| [[antczak-2015-las-aves]] | minado | hecha | si | 0 | 0 | 7 |
| [[amodio-perez-2006]] | minado | hecha | — | 0 | 0 | 6 |
| [[perrin-1992-1995]] | segunda-mano | media | — | 0 | 0 | 6 |
| [[guerra-curvelo-palabrero]] | minado | hecha | si | 0 | 0 | 4 |
| [[maria-lionza-culto]] | minado | baja | — | 0 | 0 | 4 |
| [[keegan-1989]] | segunda-mano | media | — | 0 | 0 | 2 |
| [[vansina-ong]] | segunda-mano | baja | — | 0 | 0 | 2 |
| [[adam-1879]] | minado | hecha | si | 0 | 0 | 1 |
| [[alvarado-1921]] | minado | media | si | 0 | 14 | 1 |
| [[angleria-1892]] | parcial | media | si | 0 | 0 | 1 |
| [[oviedo-y-banos]] | minado | baja | si | 0 | 0 | 1 |
| [[van-buurt-2014]] | minado | alta | si | 0 | 13 | 1 |
| [[antczak-2017-cariban]] | minado | media | si | 0 | 0 | 0 |
| [[antolinez-1944-manaure]] | segunda-mano | media | no | 0 | 0 | 0 |
| [[antolinez-1946-hacia-el-indio]] | minado | alta | si | 0 | 0 | 0 |
| [[arcaya-obra-inedita-1995]] | no-disponible | alta | no | 0 | 10 | 0 |
| [[brett-martinez-aquella-paraguana]] | no-disponible | media | no | 0 | 0 | 0 |
| [[brito-figueroa-poblacion-economia]] | en-curso | alta | no | 0 | 0 | 0 |
| [[esteves-1989]] | parcial | alta | no | 0 | 0 | 0 |
| [[federmann-1916]] | no-disponible | media | no | 0 | 0 | 0 |
| [[fernandes-2020]] | no-disponible | baja | archivo-vacio | 0 | 0 | 0 |
| [[gilij-1780-1783]] | sin-minar | baja | no | 0 | 0 | 0 |
| [[gonzalez-batista-nombre-de-coro]] | en-curso | alta | no | 0 | 0 | 0 |
| [[gumilla-1791]] | no-disponible | baja | no | 0 | 0 | 0 |
| [[las-casas-1875]] | minado | baja | si | 0 | 0 | 0 |
| [[martinez-cruzado-2003]] | minado | alta | si | 0 | 0 | 0 |
| [[medina-colina-sxx]] | en-curso | alta | no | 0 | 0 | 0 |
| [[moreno-mayar-2018]] | sin-minar | baja | si | 0 | 0 | 0 |
| [[moron-2012-petroglifos]] | minado | alta | si | 0 | 0 | 0 |
| [[moron-guillermo-historia-venezuela]] | no-disponible | media | no | 0 | 0 | 0 |
| [[nueva-segovia-1579]] | no-disponible | media | no | 0 | 0 | 0 |
| [[oliver-1989-apendice-a]] | parcial | alta | no | 0 | 14 | 0 |
| [[oliver-1989-cap3-vecinos]] | parcial | alta | no | 0 | 14 | 0 |
| [[oliver-1989-cap4]] | parcial | alta | si | 0 | 14 | 0 |
| [[perea-alonso-1942]] | descartada | descartada | si | 0 | 0 | 0 |
| [[perez-de-tolosa-1546]] | no-disponible | alta | no | 0 | 0 | 0 |
| [[ramos-perez-1978]] | no-disponible | baja | archivo-vacio | 0 | 0 | 0 |
| [[rivero-1883]] | no-disponible | media | no | 0 | 0 | 0 |
| [[rouse-cruxent-1963]] | no-disponible | media | archivo-vacio | 0 | 0 | 0 |
| [[schroeder-2018]] | minado | media | si | 0 | 0 | 0 |
| [[steward-1949]] | no-disponible | baja | no | 0 | 0 | 0 |
| [[urbina-jimenez-2007-2011]] | parcial | alta | si | 0 | 0 | 0 |
| [[velasco-2015-resistencia]] | minado | alta | si | 0 | 0 | 0 |
| [[zavala-reyes-2018]] | minado | alta | si | 0 | 222 | 0 |

</details>

Suma declarada en los frontmatter: **264** entradas de lexicón y **121** hechos de corpus sostenidos. La columna *medido* cuenta las entradas de familia caquetía cuyo campo `notas` nombra a esa obra; donde las dos columnas difieren, **manda la medida** — el frontmatter se escribió a mano y envejece.

---

## 3. El corpus cultural

Mapas: [[mapa-familia]] · [[mapa-ecologia]] · [[mapa-creencia]] · [[mapa-transmision]] · [[mapa-geografia-politica]]. Dato: `3-mundo/corpus/*.yaml`.

| Archivo | hechos | `atestiguado` | `reconstruido` | `canon-simulacion` | `hipotetico` | `retro-abstraido` | con `referencia` |
|---|---|---|---|---|---|---|---|
| `creencia.yaml` | 26 | 11 | 11 |  |  | 4 | 26/26 |
| `ecologia.yaml` | 54 | 31 | 22 |  | 1 |  | 54/54 |
| `geografia_politica.yaml` | 8 | 8 |  |  |  |  | 8/8 |
| `parentesco.yaml` | 39 | 14 | 18 |  | 7 |  | 39/39 |
| `transmision.yaml` | 34 | 13 | 5 | 14 | 2 |  | 34/34 |
| **total** | **161** | **77** | **56** | **14** | **10** | **4** | **161/161** |

Además, estructuras del corpus que **no son hechos etiquetados** (y por eso no entran en el total): `genealogia.yaml::linajes` (6), `genealogia.yaml::agentes` (60), `genealogia.yaml::personas_de_fondo` (14).

---

## 4. El gate para reanudar simulaciones

Las simulaciones están **en pausa** ([[PLAN_MAESTRO]] §0). Se reanudan cuando **todas** estas condiciones se cumplan — [[PLAN_MAESTRO]] §6 más las tres que añadió [[04_protocolo_run_1_era_auditada]] §2.

| # |  | Condición | Estado medido |
|---|---|---|---|
| 1 | 🟢 | Lexicón: 0 entradas de familia caquetía sin cita **o sin degradar** (F1) | 0 sin cita (eran 82 el 2026-07-21) |
| 2 | 🟢 | Pares c/k resueltos (F2) | todas tomadas — [D5](https://github.com/miguelgilurbina/curiana-radio/issues/36) · medido: 7 colisiones, 2 dentro del caquetío |
| 3 | 🟢 | Las 3 fuentes ALTA minadas (F3, F4, F5) | F3 [[alvarado-1921]] minado · F4 [[gatschet-1885]] minado · F5 [[oliver-1989-cap2]] minado |
| 4 | 🟢 | `compilar_corpus.py` en verde (V2) | **161 hechos, 0 errores, 0 avisos** |
| 5 | ⚪ | Citas del corpus verificadas por muestreo (F10) | **no automedible**: que la cita *resuelva* (que la página exista) es trabajo humano. Medible sí: 161/161 hechos **tienen** `referencia` |
| 6 | 🟢 | D1, D3 y D5 tomadas | todas tomadas — [D1](https://github.com/miguelgilurbina/curiana-radio/issues/32) · [D3](https://github.com/miguelgilurbina/curiana-radio/issues/34) · [D5](https://github.com/miguelgilurbina/curiana-radio/issues/36) |
| 7 | 🟢 | La glosa de `-bana` resuelta | todas tomadas — [D9](https://github.com/miguelgilurbina/curiana-radio/issues/38) |
| 8 | 🔴 | El desbalance wayunaiki/lokono resuelto | abiertas: D11 — [D11](https://github.com/miguelgilurbina/curiana-radio/issues/39) · medido: wayunaiki 781 vs. lokono 275 (2.8 a 1) |
| 9 | ⚪ | `export_runs_index.py` reparado | **no automedible sin correr un export contra la base** (ver [[04_protocolo_run_1_era_auditada]] §2.9) |

🟢 cumplida · 🔴 no cumplida · ⚪ no automedible (necesita criterio humano o correr algo)

> Y una regla que no es condición sino política ([[PLAN_MAESTRO]] §6.4): el re-export del sitio se hace **después** del primer run limpio, nunca desde los runs pre-auditoría.

---

## 5. Decisiones e issues

**El argumento y la evidencia de cada una viven en su issue.** `1-plan/el tablero de decisiones` se retiró del repo el 2026-08-06: mantener el razonamiento en markdown y el estado en el tablero producía dos copias que se desviaban. Hoy hay una sola fuente — [los issues con label `decision`](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision).

| # | Decisión | Estado | Issue |
|---|---|---|---|
| D1 | Veto de la genealogia propuesta | ✅ resuelta | [#32](https://github.com/miguelgilurbina/curiana-radio/issues/32) |
| D2 | El nombre "Curiana": ¿territorio o asentamiento? | 🔴 abierta | [#33](https://github.com/miguelgilurbina/curiana-radio/issues/33) |
| D3 | `normalizar_por_dialecto()`: cablearla o eliminarla | ✅ resuelta | [#34](https://github.com/miguelgilurbina/curiana-radio/issues/34) |
| D4 | Pluralidad de candidatos a la sucesion de Manaure | 🔴 abierta | [#35](https://github.com/miguelgilurbina/curiana-radio/issues/35) |
| D5 | Politica ortografica c/k del lexicon | ✅ resuelta | [#36](https://github.com/miguelgilurbina/curiana-radio/issues/36) |
| D8 | ¿El repo archiva copias de las fuentes externas? | 🔴 abierta | [#37](https://github.com/miguelgilurbina/curiana-radio/issues/37) |
| D9 | La glosa de `-bana` y el hallazgo de `-ana` | ✅ resuelta | [#38](https://github.com/miguelgilurbina/curiana-radio/issues/38) |
| D11 | El desbalance wayunaiki/lokono del lexicon | 🔴 abierta | [#39](https://github.com/miguelgilurbina/curiana-radio/issues/39) |
| D12 | La etiqueta de `parentesco-032`: una entrada `atestiguado` con material sin fuente | 🔴 abierta | [#81](https://github.com/miguelgilurbina/curiana-radio/issues/81) |
| D13 | El hueco léxico de "tío materno": la palabra que le falta a la tesis central | 🔴 abierta | [#82](https://github.com/miguelgilurbina/curiana-radio/issues/82) |
| D14 | Qué segunda polity se pone en escena | 🔴 abierta | [#83](https://github.com/miguelgilurbina/curiana-radio/issues/83) |
| D15 | Qué nodo se simula primero: Coro, Paraguaná, o un par desde el principio | 🔴 abierta | [#90](https://github.com/miguelgilurbina/curiana-radio/issues/90) |
| — | `tara`: ¿venado o mariposa? — puede tumbar un argumento del corpus | 🔴 abierta | [#45](https://github.com/miguelgilurbina/curiana-radio/issues/45) |

**9 abiertas** de 13. Medido contra el tablero, no contra una nota.

---

## Salud del vault y del motor

|  | Medido |  |
|---|---|---|
| Wikilinks | 1042 en 320 notas indexadas | 🟢 0 rotos |
| Tests (`curiana_sim/tests/`) | 206 passed, 0 failed | 🟢 |
| Canon ↔ polity simulada | 2 aviso(s) — ver abajo | 🟡 |

**Avisos de `curiana_polities.py::coherencia_del_canon()`:**

- el campo `etnia` usa 'caquetío' y 'caquetía' como valores distintos (concuerdan con el género de la persona, no con el pueblo). Hoy no rompe nada porque las tablas que lo consumen duplican la entrada, pero cualquier agrupación nueva por etnia contará dos pueblos donde hay uno.
- 12 agentes sin campo `etnia`; caen al defecto 'caquetío' en el orquestador: Buko, Daru, Ita-sha, Jiru-ko, Kawa, Kori …

Guardianes: `python check_vault_links.py --strict` · `python -m pytest curiana_sim/tests/ -q` · `python curiana_sim/compilar_corpus.py --check` · `python curiana_sim/curiana_polities.py --canon`

## Mediciones que fallaron

Ninguna: los seis paneles se midieron completos.

---

Vuelta al índice: [[INDICE]] · hoja de ruta: [[PLAN_MAESTRO]]
