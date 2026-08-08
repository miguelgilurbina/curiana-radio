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

<!--GENERADO--> Generado el **2026-08-08 02:52**.

## ¿Vamos bien?

|  | Hoy | Referencia |  |
|---|---|---|---|
| Entradas del lexicón **sin cita** | **3** | 82 (2026-07-21) | 🟢 −79 |
| Hechos del corpus **con referencia** | **161 / 161** | — | 🟢 |
| Tests del motor | **149 en verde** | 0 rojos | 🟢 |
| Gate para reanudar simulaciones | **2 de 9** condiciones | faltan 7 | 🔴 |
| Decisiones esperando a Miguel | **12 abiertas** | 0 resueltas | 🟡 |

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
| [[zavala-reyes-2015]] | 224 | 74% |
| [[alvarado-1921]] | 15 | 5% |
| [[van-buurt-2014]] | 12 | 4% |
| [[arcaya-1920]] | 8 | 3% |
| [[oliver-1989-cap2]] | 5 | 2% |
| [[oliver-1989-cap3]] | 5 | 2% |
| [[gatschet-1885]] | 4 | 1% |
| [[oviedo-y-valdes-1851]] | 3 | 1% |
| [[jahn-1927]] | 2 | 1% |
| [[brinton-1871]] | 1 | 0% |

Las obras que no aparecen tienen **penetración cero** en el lexicón. Entradas con `notas` que no citan a ninguna obra del vault: **68**.

---

## 2. Las fuentes

Índice: [[INDICE_FUENTES]]. **La nota de cada obra es la fuente de verdad**; esta tabla lee su frontmatter (`estado_minado`, `prioridad`, `capa_texto`, `sostiene`), no una lista cableada.

**30 notas de obra.**

| `estado_minado` | n |
|---|---|
| minado | 18 |
| no-disponible | 4 |
| segunda-mano | 3 |
| parcial | 1 |
| bloqueada | 1 |
| sin-minar | 1 |
| descartada | 1 |
| completo | 1 |

**Prioridad ALTA sin minar (1):** [[oviedo-y-valdes-1851]] (`no-disponible`).

<details><summary>Las 30 notas, una por fila</summary>

| Nota | minado | prioridad | capa texto | lexicón (declarado) | lexicón (medido) | hechos corpus |
|---|---|---|---|---|---|---|
| [[zavala-reyes-2015]] | completo | alta | si | 164 | 224 | 7 |
| [[brinton-1871]] | minado | hecha | si | 84 | 1 | 0 |
| [[jahn-1927]] | minado | media | si | 4 | 2 | 16 |
| [[gatschet-1885]] | minado | alta | si | 4 | 4 | 0 |
| [[oliver-1989-cap3]] | minado | media | si | 2 | 5 | 15 |
| [[oviedo-y-valdes-1851]] | no-disponible | alta | no | 2 | 3 | 7 |
| [[oliver-1989-cap2]] | minado | alta | parcial | 2 | 5 | 2 |
| [[arcaya-1920]] | minado | media | si | 1 | 8 | 13 |
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
| [[alvarado-1921]] | minado | media | si | 0 | 15 | 1 |
| [[angleria-1892]] | parcial | media | si | 0 | 0 | 1 |
| [[oviedo-y-banos]] | minado | baja | si | 0 | 0 | 1 |
| [[van-buurt-2014]] | minado | alta | si | 0 | 12 | 1 |
| [[antczak-2017-cariban]] | minado | media | si | 0 | 0 | 0 |
| [[fernandes-2020]] | no-disponible | baja | archivo-vacio | 0 | 0 | 0 |
| [[gilij-1780-1783]] | bloqueada | baja | no | 0 | 0 | 0 |
| [[las-casas-1875]] | minado | baja | si | 0 | 0 | 0 |
| [[moreno-mayar-2018]] | sin-minar | baja | si | 0 | 0 | 0 |
| [[perea-alonso-1942]] | descartada | descartada | si | 0 | 0 | 0 |
| [[ramos-perez-1978]] | no-disponible | baja | archivo-vacio | 0 | 0 | 0 |
| [[rouse-cruxent-1963]] | no-disponible | media | archivo-vacio | 0 | 0 | 0 |

</details>

Suma declarada en los frontmatter: **263** entradas de lexicón y **121** hechos de corpus sostenidos. La columna *medido* cuenta las entradas de familia caquetía cuyo campo `notas` nombra a esa obra; donde las dos columnas difieren, **manda la medida** — el frontmatter se escribió a mano y envejece.

---

## 3. El corpus cultural

Mapas: [[mapa-familia]] · [[mapa-ecologia]] · [[mapa-creencia]] · [[mapa-transmision]] · [[mapa-geografia-politica]]. Dato: `3-mundo/corpus/*.yaml`.

| Archivo | hechos | `atestiguado` | `reconstruido` | `canon-simulacion` | `hipotetico` | `retro-abstraido` | con `referencia` |
|---|---|---|---|---|---|---|---|
| `creencia.yaml` | 26 | 11 | 11 |  |  | 4 | 26/26 |
| `ecologia.yaml` | 54 | 32 | 21 |  | 1 |  | 54/54 |
| `geografia_politica.yaml` | 8 | 8 |  |  |  |  | 8/8 |
| `parentesco.yaml` | 39 | 14 | 18 |  | 7 |  | 39/39 |
| `transmision.yaml` | 34 | 13 | 5 | 14 | 2 |  | 34/34 |
| **total** | **161** | **78** | **55** | **14** | **10** | **4** | **161/161** |

Además, estructuras del corpus que **no son hechos etiquetados** (y por eso no entran en el total): `genealogia.yaml::linajes` (6), `genealogia.yaml::agentes` (60), `genealogia.yaml::personas_de_fondo` (14).

---

## 4. El gate para reanudar simulaciones

Las simulaciones están **en pausa** ([[PLAN_MAESTRO]] §0). Se reanudan cuando **todas** estas condiciones se cumplan — [[PLAN_MAESTRO]] §6 más las tres que añadió [[04_protocolo_run_1_era_auditada]] §2.

| # |  | Condición | Estado medido |
|---|---|---|---|
| 1 | 🔴 | Lexicón: 0 entradas de familia caquetía sin cita **o sin degradar** (F1) | 3 sin cita (eran 82 el 2026-07-21) |
| 2 | 🔴 | Pares c/k resueltos (F2) | abiertas: D5 — [D5](https://github.com/miguelgilurbina/curiana-radio/issues/36) · medido: 10 colisiones, 3 dentro del caquetío |
| 3 | 🟢 | Las 3 fuentes ALTA minadas (F3, F4, F5) | F3 [[alvarado-1921]] minado · F4 [[gatschet-1885]] minado · F5 [[oliver-1989-cap2]] minado |
| 4 | 🟢 | `compilar_corpus.py` en verde (V2) | **161 hechos, 0 errores, 0 avisos** |
| 5 | ⚪ | Citas del corpus verificadas por muestreo (F10) | **no automedible**: que la cita *resuelva* (que la página exista) es trabajo humano. Medible sí: 161/161 hechos **tienen** `referencia` |
| 6 | 🔴 | D1, D3 y D5 tomadas | abiertas: D1, D3, D5 — [D1](https://github.com/miguelgilurbina/curiana-radio/issues/32) · [D3](https://github.com/miguelgilurbina/curiana-radio/issues/34) · [D5](https://github.com/miguelgilurbina/curiana-radio/issues/36) |
| 7 | 🔴 | La glosa de `-bana` resuelta | abiertas: D9 — [D9](https://github.com/miguelgilurbina/curiana-radio/issues/38) |
| 8 | 🔴 | El desbalance wayunaiki/lokono resuelto | abiertas: D11 — [D11](https://github.com/miguelgilurbina/curiana-radio/issues/39) · medido: wayunaiki 781 vs. lokono 227 (3.4 a 1) |
| 9 | ⚪ | `export_runs_index.py` reparado | **no automedible sin correr un export contra la base** (ver [[04_protocolo_run_1_era_auditada]] §2.9) |

🟢 cumplida · 🔴 no cumplida · ⚪ no automedible (necesita criterio humano o correr algo)

> Y una regla que no es condición sino política ([[PLAN_MAESTRO]] §6.4): el re-export del sitio se hace **después** del primer run limpio, nunca desde los runs pre-auditoría.

---

## 5. Decisiones e issues

**El argumento y la evidencia de cada una viven en su issue.** `1-plan/el tablero de decisiones` se retiró del repo el 2026-08-06: mantener el razonamiento en markdown y el estado en el tablero producía dos copias que se desviaban. Hoy hay una sola fuente — [los issues con label `decision`](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision).

| # | Decisión | Estado | Issue |
|---|---|---|---|
| D1 | Veto de la genealogia propuesta | 🔴 abierta | [#32](https://github.com/miguelgilurbina/curiana-radio/issues/32) |
| D2 | El nombre "Curiana": ¿territorio o asentamiento? | 🔴 abierta | [#33](https://github.com/miguelgilurbina/curiana-radio/issues/33) |
| D3 | `normalizar_por_dialecto()`: cablearla o eliminarla | 🔴 abierta | [#34](https://github.com/miguelgilurbina/curiana-radio/issues/34) |
| D4 | Pluralidad de candidatos a la sucesion de Manaure | 🔴 abierta | [#35](https://github.com/miguelgilurbina/curiana-radio/issues/35) |
| D5 | Politica ortografica c/k del lexicon | 🔴 abierta | [#36](https://github.com/miguelgilurbina/curiana-radio/issues/36) |
| D8 | ¿El repo archiva copias de las fuentes externas? | 🔴 abierta | [#37](https://github.com/miguelgilurbina/curiana-radio/issues/37) |
| D9 | La glosa de `-bana` y el hallazgo de `-ana` | 🔴 abierta | [#38](https://github.com/miguelgilurbina/curiana-radio/issues/38) |
| D11 | El desbalance wayunaiki/lokono del lexicon | 🔴 abierta | [#39](https://github.com/miguelgilurbina/curiana-radio/issues/39) |
| D12 | La etiqueta de `parentesco-032`: una entrada `atestiguado` con material sin fuente | 🔴 abierta | [#81](https://github.com/miguelgilurbina/curiana-radio/issues/81) |
| D13 | El hueco léxico de "tío materno": la palabra que le falta a la tesis central | 🔴 abierta | [#82](https://github.com/miguelgilurbina/curiana-radio/issues/82) |
| D14 | Qué segunda polity se pone en escena | 🔴 abierta | [#83](https://github.com/miguelgilurbina/curiana-radio/issues/83) |
| — | `tara`: ¿venado o mariposa? — puede tumbar un argumento del corpus | 🔴 abierta | [#45](https://github.com/miguelgilurbina/curiana-radio/issues/45) |

**12 abiertas** de 12. Medido contra el tablero, no contra una nota.

---

## Salud del vault y del motor

|  | Medido |  |
|---|---|---|
| Wikilinks | 774 en 189 notas indexadas | 🟢 0 rotos |
| Tests (`curiana_sim/tests/`) | 149 passed, 0 failed | 🟢 |
| Canon ↔ polity simulada | 2 aviso(s) — ver abajo | 🟡 |

**Avisos de `curiana_polities.py::coherencia_del_canon()`:**

- el campo `etnia` usa 'caquetío' y 'caquetía' como valores distintos (concuerdan con el género de la persona, no con el pueblo). Hoy no rompe nada porque las tablas que lo consumen duplican la entrada, pero cualquier agrupación nueva por etnia contará dos pueblos donde hay uno.
- 12 agentes sin campo `etnia`; caen al defecto 'caquetío' en el orquestador: Buco, Daru, Ita-sha, Jiru-ko, Kawa, Kori …

Guardianes: `python check_vault_links.py --strict` · `python -m pytest curiana_sim/tests/ -q` · `python curiana_sim/compilar_corpus.py --check` · `python curiana_sim/curiana_polities.py --canon`

## Mediciones que fallaron

Ninguna: los seis paneles se midieron completos.

---

Vuelta al índice: [[INDICE]] · hoja de ruta: [[PLAN_MAESTRO]]
