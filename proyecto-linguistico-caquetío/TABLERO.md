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

<!--GENERADO--> Generado el **2026-08-25 21:33**.

## ¿Vamos bien?

|  | Hoy | Referencia |  |
|---|---|---|---|
| Entradas del lexicón **sin cita** | **3** | 82 (2026-07-21) | 🟢 −79 |
| Hechos del corpus **con referencia** | **161 / 161** | — | 🟢 |
| Tests del motor | **197 en verde** | 0 rojos | 🟢 |
| Gate para reanudar simulaciones | **2 de 9** condiciones | faltan 7 | 🔴 |

**Lo que bloquea hoy:** censo de citas (F1) · pares c/k (F2 · D5) · decisiones D1/D3/D5 · glosa de `-bana` (D9) · wayunaiki vs. lokono (D11).
Y 2 condición(es) que **nadie puede medir por script**: citas del corpus (F10) · exportador de runs.

Detalle de cada número: [lexicón](#1-el-lexicón) · [fuentes](#2-las-fuentes) · [corpus](#3-el-corpus-cultural) · [gate](#4-el-gate-para-reanudar-simulaciones) · [decisiones](#5-decisiones-e-issues)

---

## 1. El lexicón

Nota: [[lexicon]] · código: `curiana_sim/curiana_lexicon.py`

**1413 entradas activas** en `VOCABULARIO_BASE`.

### Por lengua (categoría normalizada)

| Lengua (`normalize_source_language()`) | n | % del lexicón |
|---|---|---|
| wayunaiki | 781 | 55.3% |
| caquetío | 304 | 21.5% |
| lokono | 227 | 16.1% |
| taíno | 57 | 4.0% |
| kalinago | 19 | 1.3% |
| proto-arahuaco | 8 | 0.6% |
| jirajaroide-contacto | 7 | 0.5% |
| caribe-continental | 4 | 0.3% |
| kalinago-caribe-overlay | 4 | 0.3% |
| español-colonial | 2 | 0.1% |

<details><summary>Los 25 valores de <code>fuente</code> en el dato crudo (F8 quiere sanearlos)</summary>

| `fuente` crudo | n |
|---|---|
| wayunaiki | 769 |
| caquetío-atestiguado | 226 |
| lokono | 198 |
| caquetío-reconstruido | 68 |
| taíno | 36 |
| kalinago | 19 |
| taino | 18 |
| lokono/proto-arawakan | 14 |
| lokono/garifuna | 13 |
| caquetío | 8 |
| wayunaiki-cogn | 7 |
| jirajaroide-contacto | 7 |
| proto-arahuaco | 6 |
| wayunaiki/lokono | 5 |
| kalinago-caribe-overlay | 4 |
| español-colonial | 2 |
| caribe-cháima | 2 |
| taíno/lokono | 2 |
| proto-arawakan | 2 |
| caribe-cumanagoto | 2 |
| caquetío-hipotético/topónimo | 1 |
| taíno/caribe | 1 |
| lokono-cogn | 1 |
| proto-arawakan/lokono | 1 |
| caquetío-hipotético | 1 |

</details>

### La familia caquetía por capa epistémica

| Capa | n | Qué significa |
|---|---|---|
| `caquetío-atestiguado` | 226 | dato histórico citable a fuente concreta |
| `caquetío-reconstruido` | 68 | vocabulario de trabajo del proyecto |
| `caquetío-hipotético` | 2 | baja de tier por D10 — la lengua no se discute, la confianza sí |
| `caquetío` a secas / topónimo | 8 | sin capa declarada en el campo `fuente` |
| **total familia caquetía** | **304** |  |

Fuera del habla activa: **441** candidatas `hipotético-no-verificado` en `lexicon_candidatos.py` (aisladas el 2026-06-28) y **1** entrada(s) en `FUERA_DEL_HABLA` (`piache`).

### Censo de citas — la deuda de F1

Entradas de familia caquetía **sin nada en `notas`**: **3** (eran 82 el 2026-07-21, PLAN_MAESTRO §1). Lo calcula `curiana_sim/auditar_82.py`, que este tablero importa en vez de duplicar.

| Palabra | Significado | Veredicto de las 4 minerías |
|---|---|---|
| `kama` | tapir, danta (Tapirus terrestris) | `SIN_RASTRO` |
| `koke` | bachaco, hormiga grande (Atta spp.) | `SIN_RASTRO` |
| `wabarsure` | alma colectiva, espíritu del pueblo (wa+barsure) | `SIN_RASTRO` |

Las que quedan **no son deuda de minería sino de decisión**: no dejan rastro en ninguna de las cuatro fuentes minadas.

### Quién sostiene el «atestiguado»

Cuántas de las 301 entradas de familia caquetía **con `notas`** citan a cada obra. Los patrones de búsqueda salen del `autor` y los `aliases` de cada nota de `4-fuentes/`, así que una obra nueva aparece sola aquí.

| Obra | Entradas que la citan | % de las citadas |
|---|---|---|
| [[zavala-reyes-2015]] | 223 | 74% |
| [[zavala-reyes-2018]] | 223 | 74% |
| [[alvarado-1921]] | 14 | 5% |
| [[oliver-1989-apendice-a]] | 10 | 3% |
| [[oliver-1989-cap2]] | 10 | 3% |
| [[oliver-1989-cap3-vecinos]] | 10 | 3% |
| [[oliver-1989-cap3]] | 10 | 3% |
| [[oliver-1989-cap4]] | 10 | 3% |
| [[van-buurt-2014]] | 10 | 3% |
| [[arcaya-1920]] | 8 | 3% |
| [[arcaya-obra-inedita-1995]] | 8 | 3% |
| [[gatschet-1885]] | 3 | 1% |
| [[oviedo-y-valdes-1851]] | 2 | 1% |
| [[jahn-1927]] | 1 | 0% |
| [[brinton-1871]] | 1 | 0% |

Las obras que no aparecen tienen **penetración cero** en el lexicón. Entradas con `notas` que no citan a ninguna obra del vault: **68**.

---

## 2. Las fuentes

Índice: [[INDICE_FUENTES]]. **La nota de cada obra es la fuente de verdad**; esta tabla lee su frontmatter (`estado_minado`, `prioridad`, `capa_texto`, `sostiene`), no una lista cableada.

**49 notas de obra.**

| `estado_minado` | n |
|---|---|
| minado | 21 |
| no-disponible | 11 |
| parcial | 6 |
| segunda-mano | 4 |
| en-curso | 3 |
| sin-minar | 2 |
| descartada | 1 |
| completo | 1 |

**Prioridad ALTA sin minar (12):** [[arcaya-obra-inedita-1995]] (`no-disponible`), [[ballesteros-1550]] (`segunda-mano`), [[brito-figueroa-poblacion-economia]] (`en-curso`), [[esteves-1989]] (`parcial`), [[fuente-toponimia-coriana-sin-identificar]] (`en-curso`), [[medina-colina-sxx]] (`en-curso`), [[oliver-1989-apendice-a]] (`parcial`), [[oliver-1989-cap3-vecinos]] (`parcial`), [[oliver-1989-cap4]] (`parcial`), [[oviedo-y-valdes-1851]] (`no-disponible`), [[perez-de-tolosa-1546]] (`no-disponible`), [[urbina-jimenez-2007-2011]] (`parcial`).

<details><summary>Las 49 notas, una por fila</summary>

| Nota | minado | prioridad | capa texto | lexicón (declarado) | lexicón (medido) | hechos corpus |
|---|---|---|---|---|---|---|
| [[zavala-reyes-2015]] | completo | alta | si | 164 | 223 | 7 |
| [[brinton-1871]] | minado | hecha | si | 84 | 1 | 0 |
| [[jahn-1927]] | minado | media | si | 4 | 1 | 16 |
| [[gatschet-1885]] | minado | alta | si | 4 | 3 | 0 |
| [[oliver-1989-cap3]] | minado | media | si | 2 | 10 | 15 |
| [[oviedo-y-valdes-1851]] | no-disponible | alta | no | 2 | 2 | 7 |
| [[oliver-1989-cap2]] | minado | alta | parcial | 2 | 10 | 2 |
| [[arcaya-1920]] | minado | media | si | 1 | 8 | 13 |
| [[ballesteros-1550]] | segunda-mano | alta | no | 1 | 0 | 0 |
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
| [[van-buurt-2014]] | minado | alta | si | 0 | 10 | 1 |
| [[antczak-2017-cariban]] | minado | media | si | 0 | 0 | 0 |
| [[arcaya-obra-inedita-1995]] | no-disponible | alta | no | 0 | 8 | 0 |
| [[brito-figueroa-poblacion-economia]] | en-curso | alta | no | 0 | 0 | 0 |
| [[esteves-1989]] | parcial | alta | no | 0 | 0 | 0 |
| [[federmann-1916]] | no-disponible | media | no | 0 | 0 | 0 |
| [[fernandes-2020]] | no-disponible | baja | archivo-vacio | 0 | 0 | 0 |
| [[fuente-toponimia-coriana-sin-identificar]] | en-curso | alta | no | 0 | 0 | 0 |
| [[gilij-1780-1783]] | sin-minar | baja | no | 0 | 0 | 0 |
| [[gumilla-1791]] | no-disponible | baja | no | 0 | 0 | 0 |
| [[las-casas-1875]] | minado | baja | si | 0 | 0 | 0 |
| [[martinez-cruzado-2003]] | minado | alta | si | 0 | 0 | 0 |
| [[medina-colina-sxx]] | en-curso | alta | no | 0 | 0 | 0 |
| [[moreno-mayar-2018]] | sin-minar | baja | si | 0 | 0 | 0 |
| [[nueva-segovia-1579]] | no-disponible | media | no | 0 | 0 | 0 |
| [[oliver-1989-apendice-a]] | parcial | alta | no | 0 | 10 | 0 |
| [[oliver-1989-cap3-vecinos]] | parcial | alta | no | 0 | 10 | 0 |
| [[oliver-1989-cap4]] | parcial | alta | si | 0 | 10 | 0 |
| [[perea-alonso-1942]] | descartada | descartada | si | 0 | 0 | 0 |
| [[perez-de-tolosa-1546]] | no-disponible | alta | no | 0 | 0 | 0 |
| [[ramos-perez-1978]] | no-disponible | baja | archivo-vacio | 0 | 0 | 0 |
| [[rivero-1883]] | no-disponible | media | no | 0 | 0 | 0 |
| [[rouse-cruxent-1963]] | no-disponible | media | archivo-vacio | 0 | 0 | 0 |
| [[schroeder-2018]] | minado | media | si | 0 | 0 | 0 |
| [[steward-1949]] | no-disponible | baja | no | 0 | 0 | 0 |
| [[urbina-jimenez-2007-2011]] | parcial | alta | si | 0 | 0 | 0 |
| [[zavala-reyes-2018]] | minado | alta | si | 0 | 223 | 0 |

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
| 1 | 🔴 | Lexicón: 0 entradas de familia caquetía sin cita **o sin degradar** (F1) | 3 sin cita (eran 82 el 2026-07-21) |
| 2 | 🔴 | Pares c/k resueltos (F2) | abiertas: D5 — D5 · medido: 10 colisiones, 3 dentro del caquetío |
| 3 | 🟢 | Las 3 fuentes ALTA minadas (F3, F4, F5) | F3 [[alvarado-1921]] minado · F4 [[gatschet-1885]] minado · F5 [[oliver-1989-cap2]] minado |
| 4 | 🟢 | `compilar_corpus.py` en verde (V2) | **161 hechos, 0 errores, 0 avisos** |
| 5 | ⚪ | Citas del corpus verificadas por muestreo (F10) | **no automedible**: que la cita *resuelva* (que la página exista) es trabajo humano. Medible sí: 161/161 hechos **tienen** `referencia` |
| 6 | 🔴 | D1, D3 y D5 tomadas | abiertas: D1, D3, D5 — D1 · D3 · D5 |
| 7 | 🔴 | La glosa de `-bana` resuelta | abiertas: D9 — D9 |
| 8 | 🔴 | El desbalance wayunaiki/lokono resuelto | abiertas: D11 — D11 · medido: wayunaiki 781 vs. lokono 227 (3.4 a 1) |
| 9 | ⚪ | `export_runs_index.py` reparado | **no automedible sin correr un export contra la base** (ver [[04_protocolo_run_1_era_auditada]] §2.9) |

🟢 cumplida · 🔴 no cumplida · ⚪ no automedible (necesita criterio humano o correr algo)

> Y una regla que no es condición sino política ([[PLAN_MAESTRO]] §6.4): el re-export del sitio se hace **después** del primer run limpio, nunca desde los runs pre-auditoría.

---

## 5. Decisiones e issues

**El argumento y la evidencia de cada una viven en su issue.** `1-plan/el tablero de decisiones` se retiró del repo el 2026-08-06: mantener el razonamiento en markdown y el estado en el tablero producía dos copias que se desviaban. Hoy hay una sola fuente — [los issues con label `decision`](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision).

⚠️ **No medido**: este panel lee el tablero y necesita red. Córrelo con `python curiana_sim/generar_tablero.py --gh`.
---

## Salud del vault y del motor

|  | Medido |  |
|---|---|---|
| Wikilinks | 1006 en 278 notas indexadas | 🟢 0 rotos |
| Tests (`curiana_sim/tests/`) | 197 passed, 0 failed | 🟢 |
| Canon ↔ polity simulada | 2 aviso(s) — ver abajo | 🟡 |

**Avisos de `curiana_polities.py::coherencia_del_canon()`:**

- el campo `etnia` usa 'caquetío' y 'caquetía' como valores distintos (concuerdan con el género de la persona, no con el pueblo). Hoy no rompe nada porque las tablas que lo consumen duplican la entrada, pero cualquier agrupación nueva por etnia contará dos pueblos donde hay uno.
- 12 agentes sin campo `etnia`; caen al defecto 'caquetío' en el orquestador: Buco, Daru, Ita-sha, Jiru-ko, Kawa, Kori …

Guardianes: `python check_vault_links.py --strict` · `python -m pytest curiana_sim/tests/ -q` · `python curiana_sim/compilar_corpus.py --check` · `python curiana_sim/curiana_polities.py --canon`

## Mediciones que fallaron

Un hueco que se ve es mejor que un número inventado.

| Qué se intentaba medir | Error |
|---|---|
| decisiones (issues con label `decision`) | `no consultado: necesita red, pásale --gh` |

---

Vuelta al índice: [[INDICE]] · hoja de ruta: [[PLAN_MAESTRO]]
