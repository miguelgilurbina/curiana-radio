# Bitácora de Runs — Simulación Curiana

Registro de cada corrida de la simulación con sus hallazgos. Documento vivo,
**más reciente arriba**. Espejo en Notion (*Bitácora de Runs*). Análisis
detallados por run en archivos `ANALISIS_RUN_*.md` enlazados.

> Cómo se reproduce el análisis: los datos viven en Supabase local (curiana,
> puerto 64321 / DB 64322). Consultar con `docker exec -i supabase_db_curiana_sim
> psql -U postgres -d postgres`. La distancia idiolectal se recomputa desde
> `word_uses` (join con `turns` para el día — `word_uses.day` quedó sin poblar).

> ⚠️ **Corrección metodológica (2026-07-04):** la "convergencia" reportada en
> runs previos usa la distancia idiolectal ACUMULADA, que converge en parte
> por mera acumulación del vocabulario base compartido (artefacto matemático).
> Desde 07-04 `koine_metrics` guarda además `distance_ventana` (habla reciente
> real) y `distance_emergente` (solo formas emergentes), y existe `--ablacion`
> para runs de control sin las inyecciones de prompt que empujan la
> convergencia. En los smokes de verificación (`b0cbb3b8`), la acumulada
> "convergía" mientras ventana y emergente divergían — las cifras de
> convergencia históricas deben releerse con esa reserva. Ver DISENO_KOINE.md §7.

## Registro

| Fecha | Run (id8) | Turnos/Días | Agentes | Score | Caquetío | Estado / hito |
|---|---|---|---|---|---|---|
| 07-06 | `038d7b9d` + `bdc54134` | 60 / 30 c/u | 38 / 34 | 7.3 | **99%** | **Experimento normal vs. ablación** — emergente −17.9% vs −6.6%: la koiné sobrevive parcialmente sin andamiaje |
| 07-04 | `b0cbb3b8` + `2d4e67ad` | 4 / 2 c/u | 15-16 | ~7.5 | 99% | smokes de la métrica corregida (normal + `--ablacion`, descartables) |
| 06-29 | `20091e1f` | 57 / 29 | 30 | 7.4 | **99%** | **Fijación por competencia** — diccionario koiné de 7 conceptos |
| 06-29 | `9bb920eb` | 60 / 30 | 32 | 7.5 | **99%** | Run largo — población constante, métrica persistida, convergencia −44% |
| 06-29 | `f8ef263d` | 30 / 15 | 28 | 7.5 | **99%** | Primer run koiné — convergencia confirmada |
| 06-22 | `2e729f3f` | 30 / 15 | 20 | 7.2 | 92% | Primer run largo calibrado (ver `ANALISIS_RUN_30T_2026-06-22.md`) |
| 06-29 | `8a4f9da4` | 2 / 1 | 7 | 7.1 | 100% | smoke de persistencia (descartable) |
| 06-21 | `bdead490` y otros | 1–2 | 6–13 | 6–7 | 8–31% | runs de desarrollo pre-calibración (baseline) |

---

## 2026-07-06 · Runs `038d7b9d` (normal) + `bdc54134` (ablación) — El experimento de control

**Comandos:** `python curiana_orchestrator_v2.py --auto 60` y `--auto 60 --ablacion`,
misma configuración, corridos el mismo día en secuencia. Runs bien apareados:
300 vs 294 respuestas, score 7.31 vs 7.30, caquetío 99.1% vs 99.7%, 0 fallos de DB.

**Pregunta:** ¿cuánta convergencia sobrevive sin las tres inyecciones de prompt
(sugerencias de contagio, competencias abiertas, muestreo ponderado)? Si la
ablación converge igual, la koineización era andamiaje, no emergencia.

### Resultado (distancia idiolectal, día 1 → día 30)

| Lectura | Normal `038d7b9d` | Ablación `bdc54134` | Diferencia |
|---|---|---|---|
| **emergente** (la exigente) | 0.6997 → 0.5746 (**−17.9%**) | 0.6957 → 0.6499 (**−6.6%**) | **2.7×** más convergencia con andamiaje |
| ventana | 0.5631 → 0.4243 (−24.6%) | 0.5704 → 0.4573 (−19.8%) | moderada |
| acumulada | 0.6331 → 0.3536 (−44.1%) | 0.6317 → 0.3751 (−40.6%) | **casi nula** — confirma el artefacto |
| fijación (conceptos) | **6/10** fijados | 4/10 fijados | |
| neologismos adoptados | 63 | 39 | |

### Lectura

- **La evidencia de koineización emergente existe y es la diferencia:** en la
  lectura emergente el run normal converge 2.7× más que su control. La
  acumulada, en cambio, es casi idéntica en ambos (−44% vs −41%) — converge
  por acumulación del léxico base compartido sin importar el mecanismo, tal
  como diagnosticó la corrección metodológica del 07-04.
- **Forma de las curvas:** la ablación cae los primeros ~7 días (esa parte es
  intrínseca al mundo compartido, no al andamiaje) y luego se **aplana en
  ~0.64–0.65 desde el día ~16**, con leve subida al final. La normal muestra
  un rebote (días 12–17, entrada de formas nuevas) y **sigue convergiendo**
  hasta 0.575. El andamiaje no solo acelera: sostiene la convergencia después
  del equilibrio inicial.
- ⚠️ **El veredicto impreso de la ablación dice "CONVERGE ✓"** porque compara
  inicio vs fin de forma naive (−6.6% es negativo). Es correcto pero engañoso
  leído solo: la trayectoria es plateau, no convergencia sostenida. El
  veredicto binario debería considerar la pendiente reciente, no solo los
  extremos — anotado como ajuste pendiente.
- **La ablación aún fija conceptos (4/10):** los eventos de nombramiento
  siguen ocurriendo (solo se apagan las inyecciones de prompt), así que hay
  fijación residual genuina — los agentes reusan variantes que oyeron en el
  diálogo mismo. Eso es la señal emergente "pura" más interesante del run.

### Implicaciones para calibración (punto 3 del plan)

Con −17.9% en 30 días y 4/10 conceptos aún en disputa en el run normal, la
cadencia de nombramientos y los umbrales de fijación se ven razonables — la
competencia no resuelve trivialmente. Si se quiere más señal por run: más días
antes que más presión (la pendiente emergente del normal seguía negativa al
día 30).

**Comando:** `python curiana_orchestrator_v2.py --auto 60 --perfiles` (el proceso
se cortó en el turno 57/60 por teardown de sesión; analíticamente completo —
llegó al día 29).
**Contexto:** primer run con el motor de **fijación por competencia** (eventos
de nombramiento + `CompetenciaLexica`).

### El diccionario koiné emergente (7 conceptos fijados)

La pieza que faltaba: la koiné ahora **selecciona un nombre por concepto** a
partir de variantes rivales. Persistido en `koine_lexicon`:

| concepto | forma koiné fijada | (significado) | de N rivales | día |
|---|---|---|---|---|
| eclipse | **`ma-kali-bana`** | "orilla donde falta el sol" | 4 | 10 |
| cometa | **`kali-subo`** | "luz que corre" | 3 | 5 |
| metal amarillo | **`sulu-pana`** | | 3 | 14 |
| fiebre con manchas | `ka-bari-tüshi-kali` | | 2 | 9 |
| tambor caribe | `mana-koto` | | 2 | 17 |
| marea roja | `duna-kali-biji` | | 2 | 18 |
| planta que quema | `tüshi-mana-bana` | | 2 | 20 |

**La competencia es genuina:** para "cometa", Paugis-sha y Corie-ko acuñaron
`kali-subo` de forma **independiente** → convergieron. Para "eclipse" compitieron
`ma-kali`, `kali-suka`, `kali-suka-biji` y `ma-kali-bana`; ganó la última por
reuso convergente. Formas morfológicamente caquetías y semánticamente poéticas.
3 de 10 referentes quedaron en disputa (no toda competencia resuelve — realista).

### Resto

- Caquetío **99%**, score 7.4, 30 agentes, **41 neologismos adoptados**.
- Convergencia (koine_metrics): `0.6325 → 0.3509` (**−45%**), monótona.
- Compuerta fonotáctica: sin fugas españolas.

### Pendiente

- Muestreo ponderado por frecuencia (conectar `CampoLexico` a
  `muestra_caquetio_dinamica`) — único ⏳ del diseño koiné.
- El diccionario koiné (`koine_lexicon`) es ahora el **insumo de la fase de
  topónimos**: un topónimo es un referente compartido que necesita nombre.

---

## 2026-06-29 · Run `9bb920eb` — Run largo (60T / 30 días)

**Comando:** `python curiana_orchestrator_v2.py --auto 60 --perfiles`
**Contexto:** primer run con los arreglos posteriores al run koiné: población
constante (`PARTICIPANTES_KOINE`, 24 agentes rotados por ventana), métrica de
convergencia persistida (`koine_metrics`) y compuerta de neologismos fonotáctica.

### Convergencia: limpia y −44% (confirmada por dos métricas)

- **`koine_metrics` persistida** (población real, recomputable desde la tabla):
  `día 1: 0.6465 → día 30: 0.3898` (−40%). Con población constante desde el día
  16 (32 agentes), el tramo final es **monótono** — desaparece el repunte del
  medio que confundía el run anterior.
- **Cohorte fijo** (19 agentes activos desde el día ≤3, recomputado desde
  `word_uses`): `0.5467 → 0.3047` (**−44.3%**), monótona, sin bumps. El cohorte
  es ahora 19 agentes (vs 7 en el run de 30T) gracias a la población constante.

### Léxico y neologismos

- Caquetío **99%**, score 7.45, 295 respuestas, **32 agentes** (6 etnias).
- **40 neologismos adoptados** (vs 28 en el run de 30T), 6 propuestos.
- **0 formas con marcador español** — la compuerta fonotáctica funcionó en
  producción. Adoptados limpios: `tüshi-bana`, `chaa-bana-ni`, `naba-ana-bana`,
  `nii-bana-da`, `katu-puri-bana`, `paa-bana-da`…

### Pendiente

- **Fijación por competencia de variantes** (DISENO_KOINE §6): la adopción sigue
  siendo "2 agentes la usan → adoptada", sin resolver qué variante *gana* un
  significado cuando compiten. Todos los adoptados tienen exactamente 2
  adoptantes. Es el próximo mecanismo de koiné a implementar.

---

## 2026-06-29 · Run `f8ef263d` — Primer run koiné

**Comando:** `python curiana_orchestrator_v2.py --auto 30 --perfiles`
**Contexto:** primer run con el motor de koiné emergente (emocionar sembrado,
idiolecto pre-cargado, campo léxico, rotación de foráneos) + los fixes de
scoring (prioridad de stopwords, homógrafo `para`, compuerta de neologismos).

### Hallazgo central: la koiné CONVERGE ✓

Distancia idiolectal del **cohorte fijo** (7 agentes presentes desde el día 1,
control que elimina el ruido de entrada de agentes), recomputada desde `word_uses`:

```
día  1: 0.45   día  5: 0.33   día 10: 0.28   día 15: 0.26     (−43%, monótona)
```

Contracción sostenida sin un solo repunte → koineización genuina: hablantes
que arrancan divergentes y convergen en una norma compartida.

### Comparación con el run calibrado anterior

| métrica | `2e729f3f` (06-22) | `f8ef263d` (06-29) |
|---|---|---|
| Caquetío | 92% | **99–100%** |
| Agentes participando | 20 (~6 activos reales) | **28, 6 etnias** |
| Foráneos | casi nulos | **guaycarí 3 ag / 38 resp / score 8.0** |
| Neologismos con raíz española | `suave-bana-ni`, `tension-bana-chi` adoptados | **0 — los 28 adoptados son caquetíos** |
| Falsos positivos español (word_uses) | 222 (`la`/`de`/`para`…) | barridos (4 `para`=mar, bien desambiguado) |

Neologismos que entraron a la lengua: `kali-bana`, `sima-tüshi`, `tüshi-wana`,
`kuru-arua`, `masa-bana`, `barsure-ana`, `biro-sunu`…

### Limitaciones y acciones

- **Confound de la métrica EN VIVO:** la población entra gradual (7→28 vía
  `_KOINE_ROTACION`), lo que infla la distancia *whole-population* en el medio
  del run (sube 0.35→0.54 días 4–10) y hace que el "día 1 vs día 15" naive
  diga falsamente "no converge". El cohorte fijo lo desmiente. **Acción:**
  activar todos los agentes desde el día 1 (población constante).
- **Métrica no persistida:** la distancia solo se imprime (se perdió al cerrar
  el proceso). **Acción:** tabla `koine_metrics` por run/día.
- **Bug menor:** `word_uses.day` se guarda vacío (hay que joinear con `turns`).
- **Compuerta de neologismos heurística** (blocklist): atrapó las raíces vistas
  pero es whack-a-mole; falta lista de palabras españolas o filtro fonotáctico.

---

## 2026-06-22 · Run `2e729f3f` — Primer run largo calibrado

Detalle completo en [`ANALISIS_RUN_30T_2026-06-22.md`](ANALISIS_RUN_30T_2026-06-22.md).

**Resumen:** caquetío 92%, score 7.2, 155 respuestas, 20 agentes; 28 neologismos
propuestos / 20 adoptados; 20 perfiles curados.

**Hallazgos suplementarios** (análisis posterior, esta sesión, que motivaron el
trabajo de koiné):
- **Deriva plana:** caquetío ~92% desde el día 1, sin evolución temporal. El
  sistema alcanzaba equilibrio inmediato — no había emergencia, solo dominancia.
- **Concentración:** ~6 agentes tier-1 produjeron casi todo; los foráneos casi
  no participaron (sin contacto dialectal).
- **222 falsos positivos** de palabras españolas contadas como vocabulario
  (`la`→hipotética, `de`/`una`→lokono) — motivó el aislamiento de las 441 y el
  fix de prioridad de stopwords.
- **Neologismos con raíz española adoptados** (`suave-bana-ni`,
  `tension-bana-chi`, `boca-pana`) — motivó la compuerta de calidad.

---

## 2026-06-21 · Runs de desarrollo (pre-calibración)

`bdead490`, `adbf6a89`, `c238b9d9`, `38f2e8d7`, `946f7fbb`, `40073c8b`,
`ec63a264`, `800fe7c0`, `ac70737c`, `c19426ab` — runs cortos (1–2 días) durante
la calibración del pipeline. Caquetío entre **8% y 31%** en la mayoría: el
estado *antes* de retaguear el núcleo fundacional, penalizar la fuga a lenguas
hermanas y endurecer la identidad lingüística. Sirven como **baseline** del
punto de partida (sin valor analítico individual; no documentados en detalle).
