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

<!--GENERADO--> Generado el **2026-09-24 13:04**.

## ¿Vamos bien?

|  | Hoy | Referencia |  |
|---|---|---|---|
| Entradas del lexicón **sin cita** | **0** | 82 (2026-07-21) | 🟢 −82 |
| Hechos del corpus **con referencia** | **210 / 210** | — | 🟢 |
| Tests del motor | **1101 en verde** | 0 rojos | 🟢 |
| Gate para reanudar simulaciones | **7 de 9** condiciones | faltan 2 | 🔴 |
| Decisiones esperando a Miguel | **9 abiertas** | 12 resueltas | 🟡 |

**Ninguna condición del gate está en rojo.**
Y 2 condición(es) que **nadie puede medir por script**: citas del corpus (F10) · exportador de runs.

Detalle de cada número: [lexicón](#1-el-lexicón) · [fuentes](#2-las-fuentes) · [corpus](#3-el-corpus-cultural) · [gate](#4-el-gate-para-reanudar-simulaciones) · [decisiones](#5-decisiones-e-issues)

---

## 1. El lexicón

Nota: [[lexicon]] · código: `curiana_sim/curiana_lexicon.py`

**5488 entradas activas** en `VOCABULARIO_BASE`.

### Por lengua (categoría normalizada)

| Lengua (`normalize_source_language()`) | n | % del lexicón |
|---|---|---|
| proto-arahuaco | 3572 | 65.1% |
| wayunaiki | 769 | 14.0% |
| lokono | 636 | 11.6% |
| caquetío | 379 | 6.9% |
| paraujano | 47 | 0.9% |
| taíno | 46 | 0.8% |
| kalinago | 23 | 0.4% |
| jirajaroide-contacto | 7 | 0.1% |
| caribe-continental | 6 | 0.1% |
| español-colonial | 3 | 0.1% |

<details><summary>Los 16 valores de <code>fuente</code> en el dato crudo (F8 quiere sanearlos)</summary>

| `fuente` crudo | n |
|---|---|
| achagua | 3569 |
| wayunaiki | 769 |
| lokono | 636 |
| caquetío-atestiguado | 184 |
| caquetío-retroabstraido | 75 |
| caquetío-hipotético | 75 |
| paraujano | 47 |
| taíno | 46 |
| caquetío-reconstruido | 45 |
| kalinago | 23 |
| jirajaroide | 7 |
| español-colonial | 3 |
| proto-arahuaco | 3 |
| caribe-cháima | 2 |
| caribe-cumanagoto | 2 |
| caribe-pemeno | 2 |

</details>

### La familia caquetía por capa epistémica

| Capa | n | Qué significa |
|---|---|---|
| `caquetío-atestiguado` | 184 | dato histórico citable a fuente concreta |
| `caquetío-reconstruido` | 45 | vocabulario de trabajo del proyecto |
| `caquetío-hipotético` | 75 | baja de tier por D10 — la lengua no se discute, la confianza sí |
| `caquetío` a secas / topónimo | 75 | sin capa declarada en el campo `fuente` |
| **total familia caquetía** | **379** |  |

Fuera del habla activa: **441** candidatas `hipotético-no-verificado` en `lexicon_candidatos.py` (aisladas el 2026-06-28) y **76** entrada(s) en `FUERA_DEL_HABLA` (`piache`, `wanee`, `piama`, `apünüin`, `pienchi`, `jarai`, `kali`, `kasha`, `habo`, `paa`, `kira`, `joutai`, `mülia`, `abba`, `acoa`, `aduri`, `agari`, `akcicyaa`, `thigisi`, `wacusi`, `wagulo`, `taya`, `pia`, `nüma`, `kashi`, `yama`, `sulu`, `wana`, `naba`, `tüshi`, `kapua`, `anüiki`, `pütchi`, `wanü`, `poporo`, `cohiba`, `kono`, `sima`, `nomi`, `wari`, `arua`, `buri`, `chaa`, `masa`, `awa`, `suna`, `panaa`, `kabo`, `nii`, `wara`, `kuru`, `duna`, `kaya`, `taa`, `naa`, `waa`, `raka`, `rua`, `amana`, `arima`, `dali`, `baba`, `ka`, `mara`, `saa`, `naka`, `anasa`, `mütsia`, `kasuta`, `sünatü`, `outa`, `kataa`, `talata`, `jashichi`, `alaain`, `japü`).

### Censo de citas — la deuda de F1

Entradas de familia caquetía **sin nada en `notas`**: **0** (eran 82 el 2026-07-21, PLAN_MAESTRO §1). Lo calcula `curiana_sim/auditar_82.py`, que este tablero importa en vez de duplicar.

### Quién sostiene el «atestiguado»

Cuántas de las 379 entradas de familia caquetía **con `notas`** citan a cada obra. Los patrones de búsqueda salen del `autor` y los `aliases` de cada nota de `4-fuentes/`, así que una obra nueva aparece sola aquí.

| Obra | Entradas que la citan | % de las citadas |
|---|---|---|
| [[zavala-reyes-2015]] | 217 | 57% |
| [[zavala-reyes-2018]] | 217 | 57% |
| [[medina-colina-sxx]] | 62 | 16% |
| [[goeje-1939]] | 31 | 8% |
| [[perea-alonso-1942]] | 29 | 8% |
| [[alvarado-1921]] | 21 | 6% |
| [[oliver-1989-apendice-a]] | 18 | 5% |
| [[oliver-1989-cap2]] | 18 | 5% |
| [[oliver-1989-cap3-vecinos]] | 18 | 5% |
| [[oliver-1989-cap3]] | 18 | 5% |
| [[oliver-1989-cap4]] | 18 | 5% |
| [[oliver-2000-guanin]] | 18 | 5% |
| [[adam-1879]] | 15 | 4% |
| [[van-buurt-2014]] | 14 | 4% |
| [[arcaya-1920]] | 13 | 3% |
| [[arcaya-obra-inedita-1995]] | 13 | 3% |
| [[neira-ribero-1762]] | 10 | 3% |
| [[brinton-1871]] | 9 | 2% |
| [[castellanos-elegias]] | 7 | 2% |
| [[castellanos-nuevo-reino-1886]] | 7 | 2% |
| [[coll-y-toste-1897]] | 7 | 2% |
| [[gatschet-1885]] | 6 | 2% |
| [[las-casas-1875]] | 5 | 1% |
| [[las-casas-apologetica]] | 5 | 1% |
| [[oviedo-y-valdes-1851]] | 4 | 1% |
| [[angulo-molina]] | 3 | 1% |
| [[pane-c1498]] | 3 | 1% |
| [[jahn-1927]] | 2 | 1% |
| [[gonzalez-batista-2002-fundacion]] | 2 | 1% |
| [[gonzalez-batista-nombre-de-coro]] | 2 | 1% |
| [[oviedo-y-banos]] | 1 | 0% |
| [[ballesteros-1550]] | 1 | 0% |
| [[federmann-1916]] | 1 | 0% |
| [[monumento-cerro-santa-ana]] | 1 | 0% |

Las obras que no aparecen tienen **penetración cero** en el lexicón. Entradas con `notas` que no citan a ninguna obra del vault: **38**.

---

## 2. Las fuentes

Índice: [[INDICE_FUENTES]]. **La nota de cada obra es la fuente de verdad**; esta tabla lee su frontmatter (`estado_minado`, `prioridad`, `capa_texto`, `sostiene`), no una lista cableada.

**104 notas de obra.**

| `estado_minado` | n |
|---|---|
| minado | 52 |
| parcial | 22 |
| no-disponible | 11 |
| minada-parcial | 7 |
| segunda-mano | 5 |
| puntual | 2 |
| pendiente | 1 |
| dictado-terminado | 1 |
| en-curso | 1 |
| sin-minar | 1 |
| completo-con-reserva | 1 |

**Prioridad ALTA sin minar (20):** [[angleria-1892]] (`parcial`), [[angulo-molina]] (`no-disponible`), [[arcaya-obra-inedita-1995]] (`no-disponible`), [[bachiller-morales-1883]] (`parcial`), [[ballesteros-1550]] (`segunda-mano`), [[brito-figueroa-poblacion-economia]] (`no-disponible`), [[castellanos-elegias]] (`parcial`), [[esteves-1989]] (`parcial`), [[fabo-1911]] (`minada-parcial`), [[federmann-1916]] (`parcial`), [[goeje-1939]] (`parcial`), [[gonzalez-batista-nombre-de-coro]] (`parcial`), [[medina-colina-sxx]] (`dictado-terminado`), [[navarrete-1829-viages-menores]] (`parcial`), [[navarrete-1859-viages-colon]] (`parcial`), [[oliver-1989-apendice-a]] (`parcial`), [[oliver-1989-cap4]] (`parcial`), [[oviedo-y-valdes-1851]] (`minada-parcial`), [[oviedo-y-valdes-1852-1855]] (`minada-parcial`), [[zavala-reyes-2015]] (`completo-con-reserva`).

<details><summary>Las 104 notas, una por fila</summary>

| Nota | minado | prioridad | capa texto | lexicón (declarado) | lexicón (medido) | hechos corpus |
|---|---|---|---|---|---|---|
| [[zavala-reyes-2015]] | completo-con-reserva | alta | si | 164 | 217 | 7 |
| [[brinton-1871]] | minado | hecha | si | 84 | 9 | 0 |
| [[jahn-1927]] | minado | media | si | 4 | 2 | 16 |
| [[gatschet-1885]] | minado | alta | si | 4 | 6 | 0 |
| [[oliver-1989-cap3]] | minado | media | si | 2 | 18 | 15 |
| [[oliver-1989-cap2]] | minado | alta | parcial | 2 | 18 | 2 |
| [[arcaya-1920]] | minado | media | si | 1 | 13 | 13 |
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
| [[adam-1879]] | minado | hecha | si | 0 | 15 | 1 |
| [[alvarado-1921]] | minado | media | si | 0 | 21 | 1 |
| [[angleria-1892]] | parcial | alta | si | 0 | 0 | 1 |
| [[oviedo-y-banos]] | minado | baja | si | 0 | 1 | 1 |
| [[van-buurt-2014]] | minado | alta | si | 0 | 14 | 1 |
| [[angulo-molina]] | no-disponible | alta | no | 0 | 3 | 0 |
| [[antczak-2017-cariban]] | minado | media | si | 0 | 0 | 0 |
| [[antolinez-1944-manaure]] | segunda-mano | media | no | 0 | 0 | 0 |
| [[antolinez-1946-hacia-el-indio]] | minado | alta | si | 0 | 0 | 0 |
| [[arcaya-obra-inedita-1995]] | no-disponible | alta | no | 0 | 13 | 0 |
| [[avendano-castillo-2014-erythrina]] | puntual | baja | si | 0 | 0 | 0 |
| [[aves-punteros-web-2026]] | minado | baja | web | 0 | 0 | 0 |
| [[bachiller-morales-1883]] | parcial | alta | si | 0 | 0 | 0 |
| [[barrios-garrido-2018]] | parcial | media | si | 0 | 0 | 0 |
| [[bisbal-1990]] | parcial | media | web | 0 | 0 | 0 |
| [[breton-1665]] | pendiente | media | mala | 0 | 0 | 0 |
| [[brett-martinez-aquella-paraguana]] | no-disponible | media | no | 0 | 0 | 0 |
| [[brito-figueroa-poblacion-economia]] | no-disponible | alta | no | 0 | 0 | 0 |
| [[casale-2024]] | minado | alta | si | 0 | 0 | 0 |
| [[castellanos-elegias]] | parcial | alta | si | 0 | 7 | 0 |
| [[castellanos-nuevo-reino-1886]] | minada-parcial | baja | si | 0 | 7 | 0 |
| [[coll-y-toste-1897]] | parcial | media | no | 0 | 7 | 0 |
| [[colon-hernando-1892]] | parcial | media | si | 0 | 0 | 0 |
| [[cook-forrest-2005]] | minado | baja | si | 0 | 0 | 0 |
| [[dijkhoff-1997]] | minado | alta | si | 0 | 0 | 0 |
| [[esteves-1989]] | parcial | alta | ocr | 0 | 0 | 0 |
| [[fabo-1911]] | minada-parcial | alta | si | 0 | 0 | 0 |
| [[federmann-1916]] | parcial | alta | si | 0 | 1 | 0 |
| [[fernandes-2020]] | minado | alta | si | 0 | 0 | 0 |
| [[fishbase-sealifebase]] | minado | media | web | 0 | 0 | 0 |
| [[fishsounds]] | parcial | media | web | 0 | 0 | 0 |
| [[gbif-aves-paraguana-2026]] | minado | alta | datos | 0 | 0 | 0 |
| [[gbif-paraguana-2026]] | minado | media | web | 0 | 0 | 0 |
| [[gilij-1780-1783]] | parcial | baja | no | 0 | 0 | 0 |
| [[goeje-1939]] | parcial | alta | si | 0 | 31 | 0 |
| [[gonzalez-batista-2002-fundacion]] | minado | media | si | 0 | 2 | 0 |
| [[gonzalez-batista-nombre-de-coro]] | parcial | alta | no | 0 | 2 | 0 |
| [[granberry-vescelius-2004]] | no-disponible | media | no | 0 | 0 | 0 |
| [[gumilla-1791]] | minada-parcial | baja | si | 0 | 0 | 0 |
| [[haviser-1990]] | minado | media | si | 0 | 0 | 0 |
| [[knaf-2021]] | minado | baja | si | 0 | 0 | 0 |
| [[laguna-guaranao-parque]] | minado | media | web | 0 | 0 | 0 |
| [[las-casas-1875]] | minado | media | si | 0 | 5 | 0 |
| [[las-casas-apologetica]] | minado | alta | si | 0 | 5 | 0 |
| [[libro-rojo-fauna-venezolana-2015]] | parcial | media | web | 0 | 0 | 0 |
| [[martinez-cruzado-2003]] | minado | alta | si | 0 | 0 | 0 |
| [[martinon-torres-2012]] | minado | alta | si | 0 | 0 | 0 |
| [[medina-colina-sxx]] | dictado-terminado | alta | no | 0 | 62 | 0 |
| [[mol-2007]] | minado | media | si | 0 | 0 | 0 |
| [[montecano-reserva]] | minado | media | web | 0 | 0 | 0 |
| [[monumento-cerro-santa-ana]] | minado | alta | web | 0 | 1 | 0 |
| [[moreno-mayar-2018]] | minado | baja | si | 0 | 0 | 0 |
| [[moron-2012-petroglifos]] | minado | alta | si | 0 | 0 | 0 |
| [[moron-guillermo-historia-venezuela]] | no-disponible | media | no | 0 | 0 | 0 |
| [[nagele-2020]] | no-disponible | media | no-disponible | 0 | 0 | 0 |
| [[navarrete-1829-viages-menores]] | parcial | alta | si | 0 | 0 | 0 |
| [[navarrete-1859-viages-colon]] | parcial | alta | si | 0 | 0 | 0 |
| [[neira-ribero-1762]] | minado | alta | no | 0 | 10 | 0 |
| [[nueva-segovia-1579]] | no-disponible | media | no | 0 | 0 | 0 |
| [[obis-gbif-caja-marina]] | minado | media | datos | 0 | 0 | 0 |
| [[oliver-1989-apendice-a]] | parcial | alta | no | 0 | 18 | 0 |
| [[oliver-1989-cap3-vecinos]] | minado | alta | ocr | 0 | 18 | 0 |
| [[oliver-1989-cap4]] | parcial | alta | ocr | 0 | 18 | 0 |
| [[oliver-2000-guanin]] | no-disponible | media | no-disponible | 0 | 18 | 0 |
| [[osm-kaketiana]] | en-curso | media | datos | 0 | 0 | 0 |
| [[oviedo-y-valdes-1851]] | minada-parcial | alta | si | 0 | 4 | 0 |
| [[oviedo-y-valdes-1852-1855]] | minada-parcial | alta | si | 0 | 0 | 0 |
| [[pane-c1498]] | minado | alta | si | 0 | 3 | 0 |
| [[perea-alonso-1942]] | minado | alta | si | 0 | 29 | 0 |
| [[perez-de-tolosa-1546]] | minado | alta | si | 0 | 0 | 0 |
| [[pichardo-1862]] | sin-minar | media | si | 0 | 0 | 0 |
| [[polar-el-maiz-glosario]] | puntual | baja | si | 0 | 0 | 0 |
| [[queffelec-2024]] | minado | media | si | 0 | 0 | 0 |
| [[ramos-perez-1978]] | no-disponible | baja | archivo-vacio | 0 | 0 | 0 |
| [[rivero-1883]] | parcial | media | no — el PDF es sólo imagen; el .txt es el OCR del ítem de archive.org (djvu.xml) pasado a texto con un salto de página por hoja, así que la página del PDF se cuenta como con pdftotext | 0 | 0 | 0 |
| [[romero-mayayo-agudo-1991]] | parcial | media | no (escaneo); se leyó con OCR (ocr_fuente.py --lang spa --offset 168) y las páginas citadas se verificaron en imagen. El OCR tampoco se sube: es el texto entero de una obra con derechos | 0 | 0 | 0 |
| [[rondon-medicci-2013]] | minado | alta | si | 0 | 0 | 0 |
| [[rouse-cruxent-1963]] | no-disponible | media | archivo-vacio | 0 | 0 | 0 |
| [[schroeder-2018]] | minado | media | si | 0 | 0 | 0 |
| [[sherwood-gianni-zurita-2023]] | minado | alta | si | 0 | 0 | 0 |
| [[steward-1948-hsai-4]] | minada-parcial | media | si | 0 | 0 | 0 |
| [[steward-1949]] | minada-parcial | baja | si | 0 | 0 | 0 |
| [[urbina-jimenez-2007-2011]] | minado | alta | si | 0 | 0 | 0 |
| [[velasco-2015-resistencia]] | minado | alta | si | 0 | 0 | 0 |
| [[wikipedia-es-fauna-marina]] | parcial | baja | web | 0 | 0 | 0 |
| [[zavala-reyes-2018]] | minado | alta | si | 0 | 217 | 0 |
| [[zayas-1931]] | parcial | media | si | 0 | 0 | 0 |

</details>

Suma declarada en los frontmatter: **262** entradas de lexicón y **114** hechos de corpus sostenidos. La columna *medido* cuenta las entradas de familia caquetía cuyo campo `notas` nombra a esa obra; donde las dos columnas difieren, **manda la medida** — el frontmatter se escribió a mano y envejece.

---

## 3. El corpus cultural

Mapas: [[mapa-familia]] · [[mapa-ecologia]] · [[mapa-creencia]] · [[mapa-transmision]] · [[mapa-geografia-politica]]. Dato: `3-mundo/corpus/*.yaml`.

| Archivo | hechos | `atestiguado` | `reconstruido` | `canon-simulacion` | `hipotetico` | `retro-abstraido` | con `referencia` |
|---|---|---|---|---|---|---|---|
| `creencia.yaml` | 30 | 12 | 11 |  | 3 | 4 | 30/30 |
| `ecologia.yaml` | 93 | 39 | 22 |  | 32 |  | 93/93 |
| `geografia_politica.yaml` | 13 | 10 | 1 |  | 2 |  | 13/13 |
| `parentesco.yaml` | 39 | 14 | 18 |  | 7 |  | 39/39 |
| `transmision.yaml` | 35 | 14 | 5 | 14 | 2 |  | 35/35 |
| **total** | **210** | **89** | **57** | **14** | **46** | **4** | **210/210** |

Además, estructuras del corpus que **no son hechos etiquetados** (y por eso no entran en el total): `genealogia.yaml::linajes` (6), `genealogia.yaml::agentes` (60), `genealogia.yaml::personas_de_fondo` (14).

---

## 4. El gate para reanudar simulaciones

Las simulaciones están **en pausa** ([[PLAN_MAESTRO]] §0). Se reanudan cuando **todas** estas condiciones se cumplan — [[PLAN_MAESTRO]] §6 más las tres que añadió [[04_protocolo_run_1_era_auditada]] §2.

| # |  | Condición | Estado medido |
|---|---|---|---|
| 1 | 🟢 | Lexicón: 0 entradas de familia caquetía sin cita **o sin degradar** (F1) | 0 sin cita (eran 82 el 2026-07-21) |
| 2 | 🟢 | Pares c/k resueltos (F2) | todas tomadas — [D5](https://github.com/miguelgilurbina/curiana-radio/issues/36) · medido: 13 colisiones, 2 dentro del caquetío |
| 3 | 🟢 | Las 3 fuentes ALTA minadas (F3, F4, F5) | F3 [[alvarado-1921]] minado · F4 [[gatschet-1885]] minado · F5 [[oliver-1989-cap2]] minado |
| 4 | 🟢 | `compilar_corpus.py` en verde (V2) | **210 hechos, 0 errores, 0 avisos** |
| 5 | ⚪ | Citas del corpus verificadas por muestreo (F10) | **no automedible**: que la cita *resuelva* (que la página exista) es trabajo humano. Medible sí: 210/210 hechos **tienen** `referencia` |
| 6 | 🟢 | D1, D3 y D5 tomadas | todas tomadas — [D1](https://github.com/miguelgilurbina/curiana-radio/issues/32) · [D3](https://github.com/miguelgilurbina/curiana-radio/issues/34) · [D5](https://github.com/miguelgilurbina/curiana-radio/issues/36) |
| 7 | 🟢 | La glosa de `-bana` resuelta | todas tomadas — [D9](https://github.com/miguelgilurbina/curiana-radio/issues/38) |
| 8 | 🟢 | El desbalance wayunaiki/lokono resuelto | todas tomadas — [D11](https://github.com/miguelgilurbina/curiana-radio/issues/39) · medido: wayunaiki 769 vs. lokono 636 (1.2 a 1) · fase 1 de D11 FUSIONADA: 173 de 173 raíces de Perea ya están en el habla |
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
| D8 | ¿El repo archiva copias de las fuentes externas? | ✅ resuelta | [#37](https://github.com/miguelgilurbina/curiana-radio/issues/37) |
| D9 | La glosa de `-bana` y el hallazgo de `-ana` | ✅ resuelta | [#38](https://github.com/miguelgilurbina/curiana-radio/issues/38) |
| D11 | El desbalance wayunaiki/lokono del lexicon | ✅ resuelta | [#39](https://github.com/miguelgilurbina/curiana-radio/issues/39) |
| D12 | La etiqueta de `parentesco-032`: una entrada `atestiguado` con material sin fuente | 🔴 abierta | [#81](https://github.com/miguelgilurbina/curiana-radio/issues/81) |
| D13 | El hueco léxico de "tío materno": la palabra que le falta a la tesis central | 🔴 abierta | [#82](https://github.com/miguelgilurbina/curiana-radio/issues/82) |
| D14 | Qué segunda polity se pone en escena | 🔴 abierta | [#83](https://github.com/miguelgilurbina/curiana-radio/issues/83) |
| D15 | Qué nodo se simula primero: Coro, Paraguaná, o un par desde el principio | ✅ resuelta | [#90](https://github.com/miguelgilurbina/curiana-radio/issues/90) |
| — | Decisión — Los nombres del elenco de la era 2: la campaña de antropónimos, el sistema declarado y el mapa viejo → nuevo | 🔴 abierta | [#129](https://github.com/miguelgilurbina/curiana-radio/issues/129) |
| — | Decisión — El casting de la era 2: 61 agentes en cinco casas, con dossier por agente | ✅ resuelta | [#127](https://github.com/miguelgilurbina/curiana-radio/issues/127) |
| — | Decisión — Era 2: la estructura social de Paraguaná antes del elenco (dos subgrupos por nodo decididos; quedan preguntas) | 🔴 abierta | [#126](https://github.com/miguelgilurbina/curiana-radio/issues/126) |
| — | Decisión de modelo para la era 2: el habla que no se puede atestiguar (la capa retroabstraída) | ✅ resuelta | [#124](https://github.com/miguelgilurbina/curiana-radio/issues/124) |
| — | Decisión — Borojó: Esteves lo da como chibcha y árbol frutal; ¿sale de la capa atestiguada? | ✅ resuelta | [#123](https://github.com/miguelgilurbina/curiana-radio/issues/123) |
| — | Decisión — Los dos clanes de Paraguaná: ¿manda la frase de Oliver, mandan las aldeas, o la lectura de Miguel? | ✅ resuelta | [#122](https://github.com/miguelgilurbina/curiana-radio/issues/122) |
| — | Servir los PDF del vault desde `/kaketiana/fuentes`, tras un aporte voluntario | 🔴 abierta | [#120](https://github.com/miguelgilurbina/curiana-radio/issues/120) |
| — | El lexicón responde "¿de qué lengua es esta palabra?" y lo usamos como si respondiera "¿la usaba un caquetío?" | ✅ resuelta | [#119](https://github.com/miguelgilurbina/curiana-radio/issues/119) |
| — | `tara`: ¿venado o mariposa? — puede tumbar un argumento del corpus | 🔴 abierta | [#45](https://github.com/miguelgilurbina/curiana-radio/issues/45) |

**9 abiertas** de 21. Medido contra el tablero, no contra una nota.

---

## Salud del vault y del motor

|  | Medido |  |
|---|---|---|
| Wikilinks | 1532 en 824 notas indexadas | 🟢 0 rotos |
| Tests (`curiana_sim/tests/`) | 1101 passed, 0 failed | 🟢 |
| Canon ↔ polity simulada | 2 aviso(s) — ver abajo | 🟡 |

**Avisos de `curiana_polities.py::coherencia_del_canon()`:**

- el campo `etnia` usa 'caquetío' y 'caquetía' como valores distintos (concuerdan con el género de la persona, no con el pueblo). Hoy no rompe nada porque las tablas que lo consumen duplican la entrada, pero cualquier agrupación nueva por etnia contará dos pueblos donde hay uno.
- 12 agentes sin campo `etnia`; caen al defecto 'caquetío' en el orquestador: Buko, Daru, Ita-sha, Jiru-ko, Kawa, Kori …

Guardianes: `python check_vault_links.py --strict` · `python -m pytest curiana_sim/tests/ -q` · `python curiana_sim/compilar_corpus.py --check` · `python curiana_sim/curiana_polities.py --canon`

## Mediciones que fallaron

Ninguna: los seis paneles se midieron completos.

---

Vuelta al índice: [[INDICE]] · hoja de ruta: [[PLAN_MAESTRO]]
