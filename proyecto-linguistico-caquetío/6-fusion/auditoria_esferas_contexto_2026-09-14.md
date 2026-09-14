---
tipo: auditoría (propuesta, regla 5 — no fusiona nada)
fecha: 2026-09-14
pregunta: «¿cómo están interactuando las distintas esferas de contexto con la SIM?» (Miguel, antes de diseñar la era 2)
quien: escriba (Claude), a pedido de Miguel
motor_medido: rama feat/era2-arranque, HEAD 7c5f96b, árbol limpio al empezar (git status de la sesión)
medido_con: scripts del apéndice (sin API, sin .env, sin Supabase)
---

# Auditoría de esferas de contexto — qué llega al agente y qué mide el motor

## 0 · La respuesta corta

1. **Al correr, el motor no lee ningún fichero de `3-mundo/` ni ningún YAML de `2-lengua/`.** El único YAML que carga la simulación es `5-experimento/perfiles_de_run.yaml` (`curiana_perfiles.cargar_perfil`). El corpus toca la SIM por dos vías, y ninguna es de contenido. Una es un **sello**: `huella_de_base.py` guarda `corpus_hash` y `corpus_n` en `simulation_runs.config`. La otra es una **validación inversa**: `compilar_corpus.py` comprueba contra el motor los nombres de agentes, locaciones y palabras. El mundo que ve un agente está escrito a mano dentro del motor, en `curiana_agents.py`, `curiana_state.py` y `curiana_orchestrator_v2.py`.
2. **El prompt es sobre todo LENGUA.** En el turno 1, la plantilla de identidad, las reglas del tier y la muestra del lexicón suman el 84,9 % del system prompt de Manaure, el 82,8 % del de Tariwa (tier 2) y el 85,9 % del de Buko-ko (tier 2). La ficha del personaje aporta entre el 3,7 % y el 8,6 %, y el estado del mundo entre el 3,8 % y el 6,6 % (§3).
3. **`prompt_chars = 15657` no es el tamaño de un prompt.** Es la suma de los `system_prompt` de las 60 fichas (`huella_de_base.py:126-127`); se midió y da exactamente esa cifra. Solo el system prompt de Manaure en el turno 1 mide de media 9671 caracteres, y su ficha pesa 833. Hoy la huella **no sella las plantillas**, que son la mayor parte del prompt. Solo las cubre `motor_commit`.
4. **La priorización del diccionario por contexto casi no opera.** El muestreador agrupa por `categoria || cat`. Las 216 voces con `cat = sust` caen en un solo cubo que nunca es «relevante», y un prompt tier 1 recibe 3 de esas 216 (un tier 2, 2). Además, 26 voces salen enteras en **todos** los prompts tier 1 (20 en tier 2), porque sus categorías son más chicas que el goteo (§5).
5. **Ninguna voz, regla ni plantilla llega con su etiqueta epistémica.** La plantilla tier I trae 5 formas que no están en el lexicón y una retirada (`piache`), y enseña `-ana = lugar de`, glosa retirada en #109. El scorer no cuenta esas 5 formas (§4.4).
6. **Para la era 2 no existe ninguna pieza consciente del nodo.** En el texto fijo que puede llegar a un prompt, Guaranao, Amuay, Capubana, Tacuato, Carirubana, merejuy, diao y apopo dan 0 menciones, y «Curiana» da 58 (§7).

## 1 · Método — cómo se midió cada cifra

- **Trazas de código**, leídas en el código y no en la documentación. Cada afirmación lleva `fichero:línea`.
- **`medir_esferas.py`** (apéndice A) importa el motor con `dotenv` sustituido por un stub, para no leer `curiana_sim/.env`. Sustituye `curiana_orchestrator_v2._invoke` por una función que **captura** `(system, user)` y devuelve un texto fijo. Llama al `call_agent` real y parte el system prompt por los marcadores que el propio código escribe (`[TU LENGUA MATERNA…`, `[CURIANA —`, `[VOCABULARIO CAQUETÍO ADICIONAL…`, etc.). Construye K = 60 prompts por agente, porque la muestra léxica es aleatoria, y la semilla es `20260914`.
  - **Escenario A** es el turno 1 real: `estado_inicial_test()`, sin historia y con el perfil `base`.
  - **Escenario B** son 24 turnos corridos con el `run_turn` real, con nombramientos cada 4 turnos como en `auto_mode`, y **respuestas sintéticas**. Los tamaños de los bloques emergentes (memoria, contagio, competencias, neologismos) dependen de esas respuestas: sirven para ver **qué bloques aparecen y su orden de magnitud**, no para describir un run real.
  - **Modelo de probabilidad de la muestra**: 1104 contextos, el roster por las 2 estaciones y por {amanecer, tarde, cada evento del pool}, con muestreo uniforme (sin pesos del `CampoLexico`, que es lo que ve el brazo `control`).
- **`medir_esferas_2.py`** y **`medir_esferas_3.py`** (apéndices B y C) miden las plantillas contra el lexicón, las voces fijas, los campos muertos del estado, las etnias, las implicaciones del corpus y las glosas.
- Los porcentajes agregados por esfera de §3 son **aritmética sobre las medias medidas**, y las sumas cuadran con los totales.
- **No se midió** ninguna respuesta de un LLM ni ningún run guardado en Supabase.

## 2 · La tabla: esfera × canal × momento × tamaño × filtros × problemas

Momento, abreviado: **P** = en el prompt de cada llamada de agente · **E** = en la selección de eventos o estímulos del director · **S** = en el scoring u observer · **H** = sellado en la huella del run · **V** = solo en validadores o guardianes · **∅** = en ninguno.

### 2.1 LENGUA

| Fichero / dato | Canal real (función) | Momento | Tamaño medido | Filtros | Problemas |
|---|---|---|---|---|---|
| `VOCABULARIO_BASE` (`curiana_lexicon.py` + `lexicon_zavala`, `lexicon_a2` y `lexicon_achagua` fusionados con `setdefault`, `curiana_lexicon.py:6790-6831`) | `vocabulario_para_agente` (`:8121`) → `muestra_caquetio_dinamica` (`:8055`), llamada desde `call_agent` (`orchestrator:230`) | P (tiers 1 y 2) | Muestra: 3052 chars y 50 voces (T1); 2675 chars y 42 voces (T2); 0 en T3 | Familia normalizada = caquetío; capa ∈ perfil; `sig` no vacío; palabras clave del contexto; pesos del `CampoLexico` (salvo ablación) | 216 `sust` → 3 (T1) o 2 (T2) por prompt; 26 o 20 voces fijas; sin marca epistémica; 9 glosas citan otra lengua; 6 voces distintas con marcas de época o región modernas (§4.3) |
| `VOCABULARIO_BASE` entero (5513 claves, 5 familias) | `score_linguistico` → `lexico.palabras_activas()` (`:7733`); `_familia_de_token` (`:7693`) | S (cada respuesta) | 5513 claves | Ninguno para decidir «arahuaco»; la familia separa caquetío de otra lengua | Por diseño: el score cuenta todas las capas (`capas_de_score` fijo) |
| Plantilla tier I `prompt_reglas_completo` (`:7347`) | `vocabulario_para_agente` | P (T1) | 3908 chars, 71 formas léxicas fijas | Ninguno | Sin etiquetas; «VOCABULARIO DISPONIBLE [5513 palabras]», cuando las caquetías muestreables en `base` son 352; 5 formas ausentes y 1 retirada; `-ana = lugar de` (#109); ejemplo `buco-ana` |
| Plantilla tier II `prompt_reglas_breve` (`:7325`) | ídem | P (T2) | 866 chars | Ninguno | `-ana (lugar de)` retirada; `-gua` con «evidencia: Topónimos venezolanos de Falcón y Sucre», sin cita |
| Plantilla tier III (literal en `:8142-8149`) | ídem | P (T3; solo en modo interactivo, §6.8) | 222 chars | Ninguno | — |
| `_IDENTIDAD_LINGUISTICA` (`orchestrator:104-119`) | `call_agent`, `system_parts` (`:253`) | P (todos los tiers) | 1251 chars | Ninguno | La frase modelo «Taya wana-ka arima wara kari. Ta-barsure naba-ni.» es la que el diccionario koiné de `db946685` mide como habla; afirma que «hamaca» «tiene forma caquetía», pero en el lexicón está `hamaka` y no `hamaca` |
| `prompt_refuerzo` (`:7858`), vía `observer.feedback_para_agente` (`observer:256`) | `call_agent` (`:235`, `:278`) | P, si el score anterior es < 7 | 193 / 175 / 150 / 81 / 0 chars con score 1.0 / 3.0 / 5.0 / 6.5 / 7.0 | Por score del agente | Sugiere a todos las **mismas** listas fijas de verbos, conectores y sustantivos; **no se apaga en ablación** |
| `prompt_rescate_linguistico` (`:7898`) | Segunda llamada (`orchestrator:295-307`) | P, reintento si `necesita_rescate` | 888 chars (fuga al español) y 1190 (fuga a otra lengua), con un texto fallido de 200 chars dentro | Umbral normalizado por dialecto; nada en ablación | — |
| `TODAS_LAS_REGLAS` (`:7140`) | Solo `neologismo_valido` y `extraer_neologismos_del_texto` (`:7507`, `:7565`) | S | 20 afijos; 13 aparecen en las plantillas | — | `-iro`, `-aima`, `-ima`, `-uco`, `-ubana`, `-uru` (Zavala) y `-naiki` **nunca se enseñan**, aunque el extractor los reconoce |
| `2-lengua/cognados.yaml` | Ninguno (lo usan `migrar_cognados` y `compilar_lengua`) | ∅ / V | 51 cognados; 30 con forma CQ, de las cuales 15 están en `VOCABULARIO_BASE` | — | Hueco (§6) |
| `2-lengua/toponimos.yaml` y `lexicon_toponimos.py` | Ninguno en el motor | ∅ / V | 180 topónimos (A 10, B 16, C 52, descartado 102); 5 formas en `VOCABULARIO_BASE`; el módulo tiene 136 claves fuera | — | Hueco |
| `2-lengua/morfemas.yaml` | Ninguno | ∅ / V | 11 morfemas; solo `wa-` y `-ana` coinciden con las reglas del motor | — | `-bacoa` («el morfema mejor sostenido», 5 apoyos) y `-are` no llegan |
| `lexicon_candidatos`, `lexicon_alvarado`, `lexicon_gatschet`, `lexicon_van_buurt`, `lexicon_perea` | No importados | ∅ | Claves distintas fuera de `VOCABULARIO_BASE`: 438, 135, 95, 181 y 1 | — | `candidatos` queda fuera por diseño; el resto son propuestas |

### 2.2 MUNDO

| Fichero / dato | Canal real | Momento | Tamaño medido | Filtros | Problemas |
|---|---|---|---|---|---|
| `3-mundo/corpus/*.yaml` (198 hechos) | `huella_de_base` → `compilar_corpus.compilar()` (`huella:107-117`); `compilar_corpus._universo_del_motor` (`:524`) valida agentes, locaciones y `palabra_lexicon` | H, V | 198 hechos; 142 con `implicacion_simulacion`; 133 con `agentes_relacionados`; 48 con `locacion`; 62 con `palabra_lexicon` | — | **Ninguna implicación la lee el código de la SIM.** La conexión va del corpus al motor para validar, nunca del motor al corpus para cargar |
| `genealogia.yaml` | `compilar_corpus.validar_genealogia` | V | 6 linajes; 60 agentes con ficha; 14 personas de fondo | — | El grafo social del motor (`curiana_social.VINCULOS`, `:101`) está escrito a mano aparte y no deriva de los linajes |
| `3-mundo/asentamientos.yaml` | Ninguno (lo usa `compilar_asentamientos`) | ∅ / V | 31 nodos: precontacto `si` 6, `probable` 4, `desconocido` 21 | — | 0 nombres de nodo aparecen en el texto fijo del motor |
| `3-mundo/etnias.yaml` | Ninguno (lo usa `compilar_etnias`) | ∅ / V | 8 etnias: `llanos` 2, `yaracuy` 1, `occidental` 4, `costera` 1 | — | La etnia del elenco no se cruza con el registro (regla 4, §4.5) |
| `3-mundo/CULTURA_CAQUETIA.md` | Ninguno | ∅ | 19019 bytes | — | Hueco |
| `curiana_polities.py` | `POLITY_SIMULADA` sellado en la huella (`huella:133-137`); `coherencia_del_canon` en los guardianes; `prompt_polity` (`:463`) **no lo llama nadie** («Hoy no se inyecta», dice su docstring) | H, V | `prompt_polity("costera")` = 629 chars sin usar | — | Código muerto que la era 2 podría revivir por nodo |
| Estado del mundo (literal en `curiana_state.py`) | `ComunidadState.to_context_string` (`:153`) | P (todas las llamadas) y el narrador | 366 chars (A, con evento); 209 (B, sin evento) | Estación → nombre y clima; los efectos de eventos → niveles | `tensiones_activas` (4 pares), `historial_eventos`, `notas_orquestador`, `ACTIVIDADES_POR_MOMENTO`, `ESTACIONES.descripcion`, `actividades_primarias` y `meses_equiv`: **0 usos** fuera de `curiana_state` |
| `EVENTOS_COTIDIANOS` y `EVENTOS_ESTACIONALES` (25 eventos) | `director_select_event` (`orchestrator:342`) → `evento_del_turno` (entra en el contexto y el estímulo), `agentes_involucrados` (quién habla), `efecto` (niveles) | E, P | 25 eventos; 19 sin clave `estacion` | Estación | El corpus cita por id 10 de los 25 eventos (grep de los ids en `3-mundo/corpus/*.yaml`: `ecologia.yaml` y `transmision.yaml`; p. ej. ecologia-017, «Sostén del evento expedicion_perlas»). El enlace va del corpus al motor, escrito a mano, y el motor no lo lee: el evento no lleva `procedencia` |
| `LOCACIONES` (13) y `ubicacion_default` | `[Tu ubicación]` (`orchestrator:259`); palabras clave del muestreo; co-ubicación del contagio (`social:117-155`) | P | 21-30 chars | — | 6 de 13 no activan ninguna categoría léxica (§4.2); `ubicaciones_override` no lo escribe nadie |
| `MOMENTOS_ESTIMULO` (6) | Estímulo cuando no hay evento (`orchestrator:480`) | E, P | 62 chars (amanecer) | Momento | **4 de 6 son inalcanzables**: `avanzar_turno` solo alterna amanecer y tarde (`state:103-111`) |
| Fichas `system_prompt` T1/T2 (`curiana_agents.py`) | Persona, primer bloque del system (`orchestrator:209`) | P | 833 (Manaure), 253 (Tariwa), 205 (Buko-ko); suma de las 60 = 15657 | Por agente | 33 de 33 fichas T2 piden estilo «Español …»; 47 de 48 dicen «Curiana» |
| `descripcion` T1/T2 | Solo `observer.analizar_agente_curado` (`observer:480`), que va a los perfiles publicados | S (al cerrar el run) | — | — | La de Manaure dice «Heredó de su padre» (parentesco-001: «NO USAR» como norma precontacto); la de Nubiri-sha y la de Chiri-ko dicen «matrilineal». Llegan al Observer, **nunca al agente** |
| `descripcion` T3 | Persona T3 (`orchestrator:204-207`) | P (solo interactivo) | 304 (Kori) | — | — |

### 2.3 EXPERIMENTO

| Fichero / dato | Canal real | Momento | Tamaño medido | Filtros | Problemas |
|---|---|---|---|---|---|
| `5-experimento/perfiles_de_run.yaml` | `cargar_perfil` → `capas` (muestra) y `ablacion` (`orchestrator:857-869`) | P (filtro), H (config) | 3 capas en `base` | — | El modo interactivo **no pasa `capas`** (`orchestrator:711`, `:733`): ahí se ven también las retroabstraídas |
| `curiana_koine.EMOCIONAR_SEED` y `_DISPOSICION_ETNIA` | `prompt_emocionar` (`:368`) | P | 117-144 chars | Agente y etnia | — |
| `curiana_koine.FORMAS_SEED` | Precarga de `IdiolectoAgente` → `prompt_idiolecto` (`:377`) «sueles decir» | P | 69-136 chars | Agente | 122 apariciones: 31 atestiguadas, 88 reconstruidas, **3 retroabstraídas, que llegan en `base` sin pasar por el filtro de capas** |
| `REFERENTES_NOVEDOSOS` (10) y `CompetenciaLexica` | Estímulo de nombramiento cada 4 turnos (`orchestrator:466-472`); `prompt_competencias` (`koine:476`) | E, P | Competencias: 721 chars en B | Se apaga en ablación | Dos referentes nombran «el golfete» |
| `CampoLexico` | Pesos del muestreo (`orchestrator:229`) y diccionario koiné (`:1012`) | P, S | — | Se apaga en ablación | Global: una sola comunidad |
| `DifusionLexica`, `PRESTIGIO`, `VINCULOS` (`curiana_social`) | `sugerencias_para` → `[Has oído…]` (`orchestrator:242-249`) | P | 110-145 chars en B | Se apaga en ablación | Co-ubicación por **nombre** de locación, que en la era 2 uniría nodos distintos |
| `DIALECTOS` (`social:216`) | `prompt_rasgos_dialectales`; umbral del rescate | P, S | 123 chars (Tariwa) | Etnia | Perfiles por etnia foránea, no por nodo caquetío |
| `LexicoComunitario` (neologismos) | `prompt_lexico_activo` (`:7424`, últimos 15) y `prompt_pendientes_evaluacion` (`:7435`, T1/T2) | P | 421 y 331 chars en B | **Ninguno, tampoco en ablación** | Adoptar exige 2 agentes de cualquier lado: global |
| `AgentMemory` (`orchestrator:138`) | `[Tu memoria reciente]` | P | 99-260 chars en B | Agente | 3 notas × 70 chars |
| `PARTICIPANTES_KOINE` (`orchestrator:88`) | Rotación de 6 por turno (`:449-453`) | E | 23 (15 T1, 8 T2) | — | 9 de 23 son de etnias no caquetías (§4.5) |
| `DIRECTOR_SYSTEM` y `director_narrate` | Solo se imprime con `verbose`; **no vuelve a ningún agente** | ∅ para el agente | — | — | — |

## 3 · Composición medida del prompt

### 3.1 Escenario A — turno 1 (`estado_inicial_test`, perfil `base`, K = 60)

Estímulo (user message): 207 chars, el sueño de Shaboro. Cada celda es media en chars (% del system); entre corchetes, la esfera.

| Sección [esfera] | Manaure T1 | Tariwa T2 (guaycarí) | Buko-ko T2 | Kori T3 |
|---|---|---|---|---|
| Persona / ficha [EXP, mundo a mano] | 834 (8,6) | 254 (4,4) | 206 (3,7) | 304 (12,8) |
| Separadores | 8 | 8 | 8 | 8 |
| Identidad lingüística [LENGUA plantilla] | 1251 (12,9) | 1251 (21,6) | 1251 (22,4) | 1251 (52,9) |
| Emocionar [EXP] | 140 (1,4) | 144 (2,5) | 117 (2,1) | 117 (4,9) |
| Rasgos dialectales [EXP] | — | 123 (2,1) | — | — |
| Estado del mundo [MUNDO a mano] | 366 (3,8) | 366 (6,3) | 366 (6,6) | 366 (15,5) |
| Ubicación [EXP] | 29 (0,3) | 23 (0,4) | 21 (0,4) | 30 (1,3) |
| Reglas del tier [LENGUA plantilla] | 3908 (40,4) | 866 (15,0) | 866 (15,5) | 222 (9,4) |
| Muestra del lexicón [LENGUA datos] | 3052 (31,6) | 2676 (46,2) | 2675 (47,9) | — |
| Idiolecto [EXP semillas] | 83 (0,9) | 77 (1,3) | 69 (1,2) | 69 (2,9) |
| **Total system** (mín.-máx.) | **9671** (9594-9746) | **5788** (5693-5886) | **5579** (5494-5669) | **2367** |
| Voces en la muestra | 50 | 42 | 42 | 0 |
| **LENGUA** (identidad + reglas + muestra) | **84,9 %** | **82,8 %** | **85,9 %** | **62,2 %** |
| **Ficha** | 8,6 % | 4,4 % | 3,7 % | 12,8 % |
| **Mundo** | 3,8 % | 6,3 % | 6,6 % | 15,5 % |
| **Resto de EXPERIMENTO** | 2,7 % | 6,5 % | 3,9 % | 9,5 % |

### 3.2 Escenario B — tras 24 turnos (run_turn real, respuestas sintéticas; día 13, amanecer)

Estímulo: 62 chars («Amanece en la Curiana…»). Hablaron 34 agentes; hay 110 neologismos en el léxico comunitario, 55 de ellos adoptados.

| Sección | Manaure | Tariwa | Buko-ko | Kori |
|---|---|---|---|---|
| Persona | 834 (7,3) | 254 (3,4) | 206 (2,9) | 304 (8,8) |
| Identidad lingüística | 1251 (10,9) | 1251 (16,9) | 1251 (17,5) | 1251 (36,1) |
| Emocionar / rasgos / ubicación / idiolecto | 140 / — / 29 / 136 | 144 / 123 / 23 / 109 | 117 / — / 21 / 93 | 117 / — / 30 / 69 |
| Estado del mundo | 209 (1,8) | 209 (2,8) | 209 (2,9) | 209 (6,0) |
| Reglas del tier | 3908 (34,2) | 866 (11,7) | 866 (12,1) | 222 (6,4) |
| Muestra del lexicón | 3034 (26,6) | 2648 (35,8) | 2670 (37,4) | — |
| Neologismos adoptados / pendientes | 421 / 331 | 421 / 331 | 421 / 331 | 421 / — |
| Contagio / competencias / memoria | 145 / 721 / 260 | 110 / 721 / 179 | 120 / 721 / 99 | 114 / 721 / — |
| **Total system** (mín.-máx.) | **11427** (11321-11509) | **7397** (7310-7460) | **7133** (7041-7218) | **3466** |
| **LENGUA** | **71,7 %** | **64,4 %** | **67,1 %** | **42,5 %** |
| **Emergente del run** (neologismos + contagio + competencias + memoria) | 16,4 % | 23,8 % | 23,7 % | 36,2 % |
| **Mundo** | 1,8 % | 2,8 % | 2,9 % | 6,0 % |

**Lectura.** Aun con historia, lo que el agente sabe de su mundo cabe en 209-366 chars: estación, tres niveles y, si lo hay, el evento. Todo lo demás de la esfera MUNDO que ve un agente es su ficha, escrita a mano. Los prompts completos de ejemplo se pueden regenerar con el script (A), que los escribe en `prompts_ejemplo.txt` del scratchpad.

## 4 · Filtros

### 4.1 Por agente
Filtran por agente: la plantilla y el tamaño de la muestra (según tier), la etnia (rasgos, emocionar de respaldo, umbral del rescate), la ficha, el idiolecto, la memoria y el contagio. **No** hay filtro de lo que el agente *sabría* por su oficio, su linaje o su lugar, porque el corpus (133 hechos con `agentes_relacionados`) no se lee.

### 4.2 Por locación y estación
- La locación entra como **nombre** y como palabras clave para `categorias_relevantes` (`:7974`). Medido: `manglar`, `plaza`, `buco`, `bohios`, `perimetro` y `matorral` no activan ninguna categoría. `casa_cacique` activa `jerarquia`, que **no existe** entre las categorías del lexicón muestreable, y tampoco existen `parentesco`, `alimentos`, `tiempo` ni el `verbos` de `CATEGORIAS_BASE`.
- Solo 27 de las 352 voces muestreables tienen `categoria` semántica. El resto se agrupa por `cat` gramatical (`sust` 216, `v_raiz` 75…). El efecto máximo del contexto sobre la muestra es de **47 a 50 voces en T1 y de 38 a 43 en T2**.
- `categorias_relevantes` corta en las 4 primeras **en el orden del dict**, así que `ritual`, `alimentos`, `jerarquia` y `tiempo` pierden contra `geografia`, `fauna` y `flora` cuando coinciden. En los 1104 contextos modelados, `cosmos` salió relevante en 1104, `geografia` en 928, `ritual` en 128 y `jerarquia` en 37.
- Estación: el contexto base de la seca activa `comercio`, `cosmos` y `tiempo`; el de lluvias, `cosmos`, `fauna`, `flora` y `geografia`. De los 25 eventos, 6 tienen estación.

### 4.3 Por etiqueta epistémica — ¿llegan hipotéticos como hechos?
**Sí.** El perfil filtra capas **solo en la muestra** (`:8091`). No filtran ni marcan:
- **Las voces de la muestra**: ninguna lleva marca, y las 38 hipotéticas muestreables llegan igual que las atestiguadas (`kama`, `tüma`, `coro`, `manatü`…).
- **La plantilla tier I**: de sus 71 formas léxicas, 56 son reconstruidas, 9 atestiguadas, 5 ausentes y 1 retirada, y todas se presentan como «VOCABULARIO DISPONIBLE». Pronombres y verbos base son reconstrucción desde el wayuu (deuda D11) sin decirlo.
- **Las reglas**: `-ana = lugar de X`, en T1 y T2, con glosa retirada el 2026-09-07 (#109; `morfemas.yaml` la da como «glosa retirada»); `-gua = región de X`, sin cita; `-kana` justificado como «COGNADO DIRECTO» con el wayunaiki.
- **`FORMAS_SEED`**: 3 apariciones retroabstraídas en `base`. Ejemplo: `chiriware`, en la semilla y en la ficha de Manaure.
- **Glosas que viajan con la voz** (`sig`, que es lo que imprime la muestra):
  - 9 de las 352 citan otra lengua (`mütsia` «(< mütsiisü Wayunaiki)», `sünatü`, `anasa`, `jashichi`, `joutai`, `kasuta`, `kataa`, `outa`, `talata`), dentro del mismo bloque que dice que el wayunaiki «NO es tu lengua».
  - 4 llevan marca de época moderna (`niwa` «hoy desaparecida», `yawasa` «hoy extinguida en la península», `wayakán`, `hikotea`) y 4 marca regional moderna (`siwato`, `kumarawa`, `wayakán`, `yawasa`): 6 voces distintas.
  - 16 muestreables en `base` citan a Medina Colina (14 reconstruidas y 2 atestiguadas, por la decisión del 2026-09-12 sobre los tainismos), y **9 de las 26 voces fijas de T1** están entre ellas. La etiqueta es una decisión tomada; el problema es que la glosa lleva la época (s. XX) al agente, en el perfil que excluye lo retroabstraído.

### 4.4 Lo que la plantilla enseña y el scorer no cuenta
La plantilla tier I enseña `buco`, `corie (choza)`, `canoa`, `hamaca`, `conuco` y `piache (chamán)`. En el lexicón están `buko` (atestiguado), `korie` = **armadillo** (#46), `kanoa`, `hamaka` y `konuko`, y `piache` está en `FUERA_DEL_HABLA` (D10; su lugar lo ocupa `boratio`). Medido con `score_linguistico`: en «taya buco canoa corie conuco hamaca piache» solo cuenta `taya`, y en «taya buko kanoa korie konuko boratio» cuentan las 6. La plantilla empuja formas que el instrumento lee como no arahuacas.

### 4.5 Por polity — ¿llegan datos coloniales o de otras polities sin marca?
- **No hay filtro por polity en tiempo de ejecución**: `POLITY_SIMULADA` solo se sella en la huella.
- **Regla 4 en el elenco.** En `PARTICIPANTES_KOINE` hay caquetío 9, caquetía 4, caquetío_aruba 1, caribe 1, guaycarí 4, guaycarí_caquetío 1, jirajara 2 y gayón 1. En `etnias.yaml` solo `etnia-008` («caribe del elenco», `canon-simulacion`) declara la polity `costera`. `etnia-002` (guayquerí) es **hipotético**, de los **llanos** y de familia **caribe**; jirajara y gayón **no tienen entrada**. Son 8 agentes del roster sin declaración costera.
- **Regla 3.** La descripción de Manaure («Heredó de su padre») contradice parentesco-001 («NO USAR como evidencia de la norma precontacto»). Llega al prompt del Observer que cura los perfiles publicados, no al agente. Con el patrón `colonial|NO USAR|no proyectar|precontacto`, 11 implicaciones del corpus hacen advertencias de ese tipo, y el motor no puede aplicarlas porque no las lee.
- **La ablación no apaga todo lo que empuja a converger.** `call_agent` solo condiciona a `ablacion` los pesos, el contagio y las competencias (`:229`, `:242`, `:266`). Siguen activos la lista de adoptados («Palabras nuevas de la comunidad», iguales para todos), los pendientes («¿las adoptas o rechazas?»), el refuerzo con listas fijas y las dos frases modelo. Afecta a cómo se lee la diferencia normal − control.

## 5 · El diccionario

**Función y parámetros.** `vocabulario_para_agente(tier, lexico, contexto, pesos, capas)` → `muestra_caquetio_dinamica(n_por_categoria = 20 en T1 o 12 en T2, contexto, pesos, capas)`. El goteo es `max(2, n // 6)`: 3 en T1 y 2 en T2. La categoría es `categoria || cat`, y las relevantes son `CATEGORIAS_BASE ∪ categorias_relevantes(contexto, max_extra = 4)`. Las categorías relevantes reciben `n` voces, y las demás el goteo. El muestreo usa `_muestra_ponderada` (Efraimidis-Spirakis, con peso = 1 + peso del `CampoLexico`; uniforme en ablación). El tier 3 no recibe muestra.

**De dónde salen las voces (perfil `base`).**

| Medida | Valor |
|---|---|
| Claves de `VOCABULARIO_BASE` | 5513 |
| Por familia normalizada | proto-arahuaco 3571 · wayunaiki 769 · lokono 638 · **caquetío 400** · taíno 52 · paraujano 47 · kalinago 23 · jirajaroide 7 · caribe-continental 4 · español-colonial 2 |
| Caquetío por capa | atestiguado 228 · reconstruido 86 · hipotético 38 · retroabstraído 48 |
| Muestreables en `base` (capas del perfil, con `sig`) | 352 (sin `sig`: 0) |
| Voces por prompt (escenario A) | T1 50 · T2 42 · T3 0 |
| Voces por prompt (1104 contextos, sin pesos) | T1 media 48,5 (47-50) · T2 media 40,6 (38-43) |
| `sust` (216 voces) | 3 por prompt en T1, 2 en T2 · probabilidad media por prompt 0,012 |
| `v_raiz` (75 voces) | 3 en T1, 2 en T2 · probabilidad media 0,035 |
| Voces fijas (categorías de tamaño ≤ goteo, salen enteras siempre) | **T1: 26** · **T2: 20** |
| Voces con probabilidad media por prompt < 0,02 | 216 de 352 |
| Voces con probabilidad media por prompt < 0,05 | 291 de 352 |
| Modelo: voces que se esperaría no ver nunca en 154 prompts (el n de `db946685`) | 33 |

Las 26 voces fijas de T1: `ana`, `bana`, `barsure`, `biro`, `chakamba`, `curiana`, `gudamuen`, `hamaka`, `hayo`, `hiko`, `kanoa`, `karebe`, `katarí`, `kati`, `koa`, `ma`, `macana`, `magey`, `nagua`, `pana`, `para`, `sabuenen`, `siwato`, `urari`, `urupagua`, `wayakán`. Las de T2 son 20: las mismas sin los tres numerales `gudamuen`, `sabuenen` y `katarí` ni la flora `magey`, `urupagua` y `wayakán`. A cada prompt tier I se le suman las **71 formas fijas de la plantilla** y las dos frases modelo. Lo que un agente T1 ve igual en todos los turnos pesa bastante más que lo que rota: el núcleo `sust` y `v_raiz` (291 voces) aporta 6 por prompt.

**Qué parte del lexicón disponible en `base` nunca puede llegar a un prompt:**
1. **5113 claves de comparanda** (las familias no caquetías). Es por diseño, y se mide en `medicion_contaminacion_score_2026-09-09.yaml`.
2. **48 retroabstraídas**, excluidas por el perfil. Se cuelan por otra puerta: 3 apariciones en `FORMAS_SEED` y `chiriware` en la ficha de Manaure.
3. **Módulos que el motor no importa**, con claves distintas fuera de `VOCABULARIO_BASE`: `lexicon_toponimos` 136, `lexicon_candidatos` 438 (por diseño), `lexicon_alvarado` 135, `lexicon_gatschet` 95, `lexicon_van_buurt` 181 y `lexicon_perea` 1. Estos conteos pueden solaparse entre módulos.
4. **Los YAML de lengua**: 175 de los 180 topónimos, 15 de las 30 formas CQ de `cognados.yaml` y 9 de los 11 morfemas de `morfemas.yaml` no están en el motor.
5. **7 afijos de `TODAS_LAS_REGLAS`** que ninguna plantilla enseña (`-iro` y `-aima`, atestiguados por Zavala, entre ellos).
6. **Todo en el tier 3**, que no recibe muestra y además no habla en modo auto (§6.8).

Dentro de lo alcanzable, la mayoría de las voces es **casi inalcanzable**: 216 de 352 tienen menos del 2 % de probabilidad por prompt.

## 6 · Huecos: datos que existen y no llegan nunca a la simulación

1. **Corpus cultural.** Tiene 198 hechos (creencia 27, ecología 85, geografía política 13, parentesco 39, transmisión 34) y 142 `implicacion_simulacion`, y **0 las lee el código de la SIM**. De esas 142 (con patrones declarados en el apéndice B): 114 nombran agentes, 26 hablan de locación, 25 de evento, ritual o escena, 11 advierten la regla 3, 8 hablan de prompt o ficha, 7 de estación y 5 de hueco léxico o sembrado; 4 coinciden con el patrón «ya aplicado / ya está en el canon / ya existe». Por etiqueta, 65 son atestiguadas, 48 reconstruidas, 4 retroabstraídas, 11 hipotéticas y 14 canon-simulación. De las 54 `palabra_lexicon` distintas, 19 son muestreables en `base` y 35 están en el lexicón pero fuera de lo muestreable. Tariwa y Kawa-ni, del roster, no tienen ningún hecho relacionado.
2. **Genealogía.** 6 linajes y 14 personas de fondo. Nada entra en prompts, prestigio ni vínculos.
3. **Asentamientos.** 31 nodos (6 `precontacto: si`), y ningún nombre aparece en el texto fijo del motor.
4. **Etnias.** 8 registros que no se cruzan con `ALL_AGENTS[*].etnia` (§4.5).
5. **Lengua.** `toponimos.yaml`, `morfemas.yaml` y `cognados.yaml` quedan fuera (§5). El prompt T1 promete «…y más en tu memoria — topónimos, etnónimos, títulos», que no existe.
6. **Estado muerto.** `tensiones_activas` (4 pares), `historial_eventos`, `notas_orquestador`, `ACTIVIDADES_POR_MOMENTO`, `ESTACIONES.descripcion`, `actividades_primarias`, `meses_equiv` y el campo `actividades` de cada agente se escriben y no los lee nadie.
7. **Tiempo.** 4 de los 6 `MOMENTOS_ESTIMULO` son inalcanzables. Tampoco se fija la semilla, como ya anotó la bitácora de `db946685`.
8. **Agentes que no hablan en modo auto.** Los 12 T3 (`run_turn` los salta en `:488-489`, incluidos Daru, Kawa, Piri y Tawi cuando un evento los llama) y 4 agentes T1/T2 que no están en el roster ni en ningún evento: Buko-ni, Kunaro-bana, Suri-bana y Uro-ko. Alcanzables en auto: 44.
9. **`prompt_polity`** (629 chars) y **`CULTURA_CAQUETIA.md`** (19019 bytes) no tienen consumidor.
10. **Las descripciones T1/T2**, con la biografía y la matrilinealidad, solo las ve el Observer. El agente habla desde una ficha de 205-833 chars.
11. **`6-fusion/estructura_social_era2.yaml`** (subgrupos con coordenadas, zonas ZG2 y ZA1, Capubana, merejuy) no tiene consumidor. Es lo esperable antes de fusionar, y queda anotado porque la era 2 depende de él.

## 7 · La era 2: qué tendría que volverse consciente del nodo

Diseño en `DISENO_ERA2.md` §2-4 y §7-8, y en `estructura_social_era2.yaml § decision_creativa_2026-09-14`: dos nodos (GUARANAO y AMUAY), dos subgrupos por nodo, zonas de pesca exclusivas (ZG2 el Golfete; ZA1 la costa oeste hasta Carirubana y Punta Cardón) y el Capubana como centro compartido.

| Pieza actual (qué asume) | Medido | Qué habría que volver consciente | Dónde |
|---|---|---|---|
| Cabecera del mundo `[CURIANA — …]`; estímulos «Amanece en la Curiana», «El sol cae sobre el Golfete»; base T3 «comunidad caquetía del Golfete de Coro» | «Curiana» 58 y «Golfete» 11 menciones en el texto fijo; 47 de 48 fichas T1/T2 dicen «Curiana» | El nodo, el sitio del subgrupo y **su** mar: AMUAY no pesca el Golfete | `curiana_state.ComunidadState.to_context_string`; `curiana_orchestrator_v2.MOMENTOS_ESTIMULO` y la base T3 en `call_agent`; `curiana_koine.REFERENTES_NOVEDOSOS` (2 mencionan el golfete); fichas del elenco nuevo |
| 13 `LOCACIONES` genéricas, un solo pueblo | 6 no activan ningún léxico | Locación = (nodo, sitio): Moruy, Tacuato, El Cayude, Caseto, Carirubana, el Capubana; zona de pesca como atributo | `curiana_state.LOCACIONES`; `ubicacion_default` |
| Contagio por co-ubicación con **nombre** de locación | — | Clave (nodo, locación), o «orilla» uniría ZG2 con ZA1; el cruce solo por esposos y ceremonias (§4 del diseño) | `curiana_social.vecinos`, `_agentes_en` |
| 25 eventos del elenco de la era 1 | 0 eventos del Capubana, del merejuy o de pesca por zona | Eventos por nodo y escena inter-nodo en el calendario, con `procedencia` al hecho del corpus que los sostiene | `curiana_state.EVENTOS_*`; `orchestrator.director_select_event` (filtrar por nodo) |
| Roster, prestigio, vínculos, emocionar, semillas y dialectos | Roster de 23 con 9 no caquetíos; `DIALECTOS` por etnia foránea | Por nodo y subgrupo: «dos variantes caquetías, no las etnias foráneas» (§7 del diseño) | `PARTICIPANTES_KOINE`; `curiana_social.PRESTIGIO`, `VINCULOS`, `DIALECTOS`; `curiana_koine.EMOCIONAR_SEED`, `FORMAS_SEED` |
| **Semillas divergentes solo en `FORMAS_SEED`** | El idiolecto pesa 69-136 chars frente a 4793-8211 de LENGUA **idéntica para todos**; 26 voces fijas en T1 y 71 formas de plantilla iguales en ambos nodos | Si la divergencia se siembra solo en el idiolecto, la ahoga la plantilla compartida. Hace falta **muestra o lista por nodo**, y frases modelo que roten o se retiren | `curiana_lexicon.muestra_caquetio_dinamica` (parámetro de nodo), `prompt_reglas_*`; `orchestrator._IDENTIDAD_LINGUISTICA` |
| `CampoLexico`, `CompetenciaLexica` y `LexicoComunitario` globales; se adopta con 2 agentes de cualquier lado | La lista de adoptados se inyecta a todos, también en ablación | Campo y adopción por nodo, con las métricas de cruce del diseño (§7) | `curiana_koine`; `curiana_lexicon.LexicoComunitario.adoptar`, `prompt_lexico_activo` |
| Estado sin memoria de relaciones | `tensiones_activas` con 0 usos | Tensión o alianza entre nodos: la tensión declarada de la laguna de Guaranao | `curiana_state` e inyección en `to_context_string` |
| `prompt_polity` muerto | 629 chars | Revivirlo como bloque de polity + nodo + subgrupo con presupuesto fijo | `curiana_polities.prompt_polity`; `call_agent` |
| Corpus que nombra al elenco de la era 1 | 114 implicaciones con agentes; 133 hechos con `agentes_relacionados` | Plan de migración: al cambiar el elenco, `compilar_corpus.validar_agentes` va a fallar | `3-mundo/corpus/*` (Miguel), `compilar_corpus.py` |
| Huella | Sella lexicón, corpus (sin uso), fichas, polity y commit | Sellar también plantillas, ficheros del mundo de la era 2 y un `prompt_chars` real | `huella_de_base.huella` |

## 8 · Recomendaciones priorizadas (antes de la era 2)

Todas son propuestas (regla 5). Cambiar lo que el agente ve rompe la comparabilidad con la era 1: conviene hacerlo en la frontera de era y declararlo en la huella.

### P0 — sin esto la era 2 mide la plantilla y no el cruce

1. **Separar lo que el prompt enseña de lo que la koiné mide.** Rotar o retirar las frases modelo o, como mínimo, excluir sus formas del diccionario koiné y de la métrica emergente (punto 2 de la bitácora de `db946685`). → `curiana_orchestrator_v2._IDENTIDAD_LINGUISTICA`; `curiana_lexicon.prompt_reglas_completo` (el ejemplo); `curiana_koine.CampoLexico.top` y `_FORMAS_BASE` en el orquestador.
2. **Arreglar el muestreo por categoría.** Hay dos caminos, y los dos son decisión: poblar `categoria` semántica, que hoy tienen 27 de 352 voces (datos del lexicón, fusión con Miguel), o muestrear proporcional al tamaño del cubo y deduplicar entre categorías. Sin eso, las 216 `sust` reciben 3 voces por prompt. Corregir `CATEGORIAS_BASE` (`verbos` no existe) y el sesgo de orden de `max_extra`. → `curiana_lexicon.muestra_caquetio_dinamica`, `categorias_relevantes`, `CATEGORIAS_BASE`, `PALABRAS_CLAVE_CATEGORIA`.
3. **Poner la plantilla de acuerdo con el canon.** `buco` → `buko`, `corie (choza)` → `korie (armadillo)` (y `ta-corie`), `canoa` → `kanoa`, `hamaca` → `hamaka`, `conuco` → `konuko`, `piache` → `boratio`; quitar «lugar de» de `-ana` en T1 y T2 y el ejemplo `buco-ana`; cambiar «[5513 palabras]» por las voces caquetías realmente disponibles. → `curiana_lexicon.prompt_reglas_completo`, `prompt_reglas_breve`; `orchestrator._IDENTIDAD_LINGUISTICA` («hamaca»).
4. **Dar al nodo el rango de dimensión.** Añadir `nodo` y `subgrupo` a agentes, locaciones, eventos, contagio, campo, competencia, adopción y registro del Observer (tabla §7; «ingeniería que falta» del diseño). → `curiana_agents`, `curiana_state`, `curiana_social`, `curiana_koine`, `curiana_lexicon.LexicoComunitario`, `curiana_observer.RegistroInteraccion`, `curiana_database`.
5. **Completar la huella.** Hash de las plantillas (identidad, reglas, refuerzo, rescate) y de los ficheros del mundo que la era 2 cargue; `prompt_chars` medido sobre prompts reales, por ejemplo la media del roster en el turno 1, o renombrar el actual a `fichas_chars`; semilla fija. → `huella_de_base.huella`; `curiana_orchestrator_v2.auto_mode`.

### P1 — reglas 2, 3 y 4 dentro del prompt

6. **Aplicar el filtro de capas en todas las puertas.** Hoy solo lo aplica la muestra. Filtrar también `FORMAS_SEED`, las fichas y la plantilla, y decidir si las 38 hipotéticas se muestran con marca o no se muestran. → `curiana_koine.formas_semilla` (recibir `capas`); `curiana_lexicon.muestra_caquetio_dinamica`.
7. **Separar la glosa de prompt de la nota.** Una `sig` corta para el agente, sin «< Wayunaiki», «hoy extinguida» ni «península»: 9 glosas citan otra lengua y 6 voces distintas llevan marca moderna. → Campo nuevo en `VOCABULARIO_BASE` (fusión, Miguel) y su uso en `muestra_caquetio_dinamica`.
8. **Regla 4 en el elenco.** Hay 8 agentes del roster con etnias sin declaración costera en `etnias.yaml`. Para la era 2, decidir si entran foráneos. Si entran, ficha en `etnias.yaml` con decisión costera; si no, retirar los `DIALECTOS` foráneos del roster. → `3-mundo/etnias.yaml` (Miguel); `curiana_social.DIALECTOS`; `curiana_agents`.
9. **Regla de casting para el elenco nuevo.** Nada de «Español …» en la ficha (hoy 33 de 33 T2); todo agente alcanzable (roster o evento) o declarado de fondo (hoy son 16 los que no hablan en auto); descripciones sin datos que el corpus marca «NO USAR» («Heredó de su padre»). → `curiana_agents.py` de la era 2; `compilar_corpus` podría validarlo.
10. **Declarar qué apaga la ablación.** O apagar también la lista de adoptados, los pendientes y el refuerzo con listas fijas, o declararlos como andamiaje residual en `perfiles_de_run.yaml`. → `curiana_orchestrator_v2.call_agent`; `curiana_lexicon.vocabulario_para_agente`; `5-experimento/perfiles_de_run.yaml`.

### P2 — cablear el mundo, con presupuesto medido

11. **Un cargador de mundo de solo lectura**, sobre canon ya fusionado: asentamientos, estructura de la era 2 y corpus filtrado por etiqueta (hipotético marcado o fuera). Que alimente un bloque de nodo, sitio, zona de pesca y estación con **presupuesto de caracteres fijo y medido**, porque la longitud del prompt predice el score (r = −0,48, CLAUDE.md). → Módulo nuevo (p. ej. `curiana_mundo.py`), consumido por `ComunidadState.to_context_string` y `curiana_polities.prompt_polity`.
12. **Eventos desde el corpus.** Las 25 implicaciones que hablan de evento, ritual o escena y las 26 de locación, convertidas en eventos con `procedencia`: la ceremonia del Capubana, la pesca por zona, el merejuy (hoy `hipotético`, deuda `sin-procedencia`). → `curiana_state.EVENTOS_*` (o un YAML de eventos); `director_select_event`.
13. **Limpiar el estado muerto.** Inyectar `tensiones_activas` o borrarlo; hacer alcanzables los momentos o recortar `MOMENTOS_ESTIMULO` a los dos que existen. → `curiana_state.avanzar_turno`; `orchestrator.MOMENTOS_ESTIMULO`.
14. **Decidir qué morfología atestiguada se enseña.** `-iro` y `-aima` (Zavala) y `-bacoa` (`morfemas.yaml`, 5 apoyos) hoy no llegan. Es decisión de Miguel. → `curiana_lexicon.prompt_reglas_*`.
15. **Modo interactivo.** Pasar `capas`, `campo` y `competencia` en `run_turn` y en `habla` (`orchestrator:711`, `:733`), o dejar escrito que ese modo no respeta el perfil.

---

*Relacionado: [[DISENO_ERA2]] · [[BITACORA_RUNS]] (`db946685`) · [[ARQUITECTURA]] · [[mapa-motor]] · `estructura_social_era2.yaml` · `medicion_contaminacion_score_2026-09-09.yaml` · `perfiles_de_run.yaml`*

## Apéndice — scripts de medición

Se corren desde cualquier carpeta fuera del repo (escriben ahí sus salidas) con `env -u ANTHROPIC_API_KEY PYTHONIOENCODING=utf-8 python <script> <salida.txt>`. No llaman a la API, no leen `.env` (el stub de `dotenv` va antes de importar el motor) y no tocan Supabase.

### A · medir_esferas.py (prompts reales por sección, alcanzabilidad, filtros, diccionario, esferas fuera del motor)

```python
# -*- coding: utf-8 -*-
"""Auditoría de esferas de contexto — mide qué llega al prompt y al motor.

Sin API: `_invoke` se sustituye por una función que captura (system, user).
Sin .env: `dotenv` se reemplaza por un stub antes de importar el motor.
Uso: python medir_esferas.py <salida.txt>
"""
import io, os, re, sys, json, types, random, statistics
from collections import Counter, defaultdict

_stub = types.ModuleType("dotenv"); _stub.load_dotenv = lambda *a, **k: False
sys.modules["dotenv"] = _stub

REPO = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
SIM = os.path.join(REPO, "curiana_sim")
sys.path.insert(0, SIM)
OUT = open(sys.argv[1], "w", encoding="utf-8")
def p(*a):
    print(*a, file=OUT)

SEMILLA = 20260914
random.seed(SEMILLA)

import yaml
import curiana_orchestrator_v2 as orch
from curiana_agents import ALL_AGENTS, AGENTS_T1, AGENTS_T2, AGENTS_T3
from curiana_state import (estado_inicial_test, LOCACIONES, EVENTOS_COTIDIANOS,
                           EVENTOS_ESTACIONALES, ESTACIONES, ComunidadState)
import curiana_lexicon as L
from curiana_lexicon import (VOCABULARIO_BASE, LexicoComunitario, capa_epistemica,
                             categorias_relevantes, CATEGORIAS_BASE, PALABRAS_CLAVE_CATEGORIA,
                             FUERA_DEL_HABLA, TODAS_LAS_REGLAS)
from curiana_database import normalize_source_language
from curiana_observer import ObserverAgent
from curiana_social import DifusionLexica, DIALECTOS
from curiana_koine import (IdiolectoAgente, CampoLexico, CompetenciaLexica, emocionar_de,
                           REFERENTES_NOVEDOSOS, FORMAS_SEED, EMOCIONAR_SEED)
from curiana_perfiles import cargar_perfil
import curiana_polities

PERFIL = cargar_perfil("base")
CAPAS = PERFIL.capas

# ════════════════════════════════════════════════════════════════════
# 0. Referencias
# ════════════════════════════════════════════════════════════════════
p("== 0. REFERENCIAS")
p("semilla random:", SEMILLA)
p("VOCABULARIO_BASE claves:", len(VOCABULARIO_BASE))
suma_fichas = sum(len(a.get("system_prompt") or "") for a in ALL_AGENTS.values())
p("suma len(system_prompt) de ALL_AGENTS (huella_de_base.prompt_chars):", suma_fichas)
p("agentes:", len(ALL_AGENTS), "T1", len(AGENTS_T1), "T2", len(AGENTS_T2), "T3", len(AGENTS_T3))
p("perfil base capas:", sorted(CAPAS), "andamiaje:", PERFIL.andamiaje)

# ════════════════════════════════════════════════════════════════════
# 1. Construcción de prompts reales
# ════════════════════════════════════════════════════════════════════
CAPTURA = []
RESP = ["Taya wana-ka arima wara kari. Suka kaa-ni ka kali naa-da kapua. Ta-barsure maa-ni: Manaure naa-da kashi."]
def fake_invoke(client, system, user):
    CAPTURA.append((system, user))
    return RESP[0]
orch._invoke = fake_invoke

MARCAS = [
    ("[TU LENGUA MATERNA ES EL CAQUETÍO]", "identidad_linguistica"),
    ("[Tu emocionar", "emocionar"),
    ("[Tu habla, por tu origen", "rasgos_dialectales"),
    ("[CURIANA —", "mundo_estado"),
    ("[Tu ubicación]", "ubicacion"),
    ("[IDENTIDAD LINGÜÍSTICA — FUNDAMENTAL]", "reglas_tier"),
    ("[LENGUA CAQUETÍA — Identidad y reglas]", "reglas_tier"),
    ("[Lengua nativa — caquetío]", "reglas_tier"),
    ("[VOCABULARIO CAQUETÍO ADICIONAL", "muestra_lexicon"),
    ("[Palabras nuevas de la comunidad]", "neologismos_adoptados"),
    ("[Palabras propuestas en evaluación", "neologismos_pendientes"),
    ("[Has oído estas palabras", "contagio"),
    ("[La comunidad aún busca nombre", "competencias"),
    ("[Tu manera de hablar]", "idiolecto"),
    ("[Tu memoria reciente]", "memoria"),
    ("[⚠ ALERTA", "feedback"), ("[Refuerzo", "feedback"),
]
ESFERA = {
    "persona": "EXPERIMENTO: curiana_agents (system_prompt / descripcion T3) — mundo escrito a mano",
    "separador": "(---)",
    "identidad_linguistica": "LENGUA plantilla: orchestrator._IDENTIDAD_LINGUISTICA",
    "emocionar": "EXPERIMENTO: curiana_koine.EMOCIONAR_SEED / _DISPOSICION_ETNIA",
    "rasgos_dialectales": "EXPERIMENTO: curiana_social.DIALECTOS (por etnia)",
    "mundo_estado": "MUNDO a mano: curiana_state.to_context_string",
    "ubicacion": "EXPERIMENTO: ubicacion_default",
    "reglas_tier": "LENGUA plantilla: curiana_lexicon.prompt_reglas_*",
    "muestra_lexicon": "LENGUA datos: VOCABULARIO_BASE muestreado",
    "neologismos_adoptados": "EXPERIMENTO emergente: LexicoComunitario",
    "neologismos_pendientes": "EXPERIMENTO emergente: LexicoComunitario",
    "contagio": "EXPERIMENTO emergente: DifusionLexica",
    "competencias": "EXPERIMENTO emergente: CompetenciaLexica (+REFERENTES_NOVEDOSOS)",
    "idiolecto": "EXPERIMENTO: IdiolectoAgente (+FORMAS_SEED)",
    "memoria": "EXPERIMENTO emergente: AgentMemory",
    "feedback": "EXPERIMENTO: observer.feedback_para_agente",
}

def secciones(system):
    out = Counter(); actual = "persona"; voces = 0
    for linea in system.split("\n"):
        if linea == "---":
            actual = "separador"
        else:
            for m, nombre in MARCAS:
                if linea.startswith(m):
                    actual = nombre; break
        out[actual] += len(linea) + 1
        if actual == "muestra_lexicon" and linea.startswith("  ") and ": " in linea:
            voces += len(linea.split(": ", 1)[1].split(" · "))
        if actual == "separador":
            actual = "separador"
    out[list(out)[-1]] -= 1  # el último no lleva \n
    return out, voces

def construir(nombre, state, lexico, observer, stimulus, mem, difusion, idiolectos,
              competencia, campo, capas=CAPAS, ablacion=False):
    CAPTURA.clear()
    orch.call_agent(None, nombre, state, lexico, observer, stimulus, mem,
                    difusion=difusion, idiolectos=idiolectos, competencia=competencia,
                    campo=campo, ablacion=ablacion, capas=capas)
    system, user = CAPTURA[0]
    return system, user, len(CAPTURA)

def mundo_fresco():
    state = estado_inicial_test()
    lexico = LexicoComunitario()
    observer = ObserverAgent(None, lexico)
    difusion = DifusionLexica()
    idiolectos = {nm: IdiolectoAgente(nm, emocionar_de(nm, a.get("etnia"))) for nm, a in ALL_AGENTS.items()}
    return dict(state=state, lexico=lexico, observer=observer, difusion=difusion,
                idiolectos=idiolectos, campo=CampoLexico(), competencia=CompetenciaLexica(),
                memory=orch.AgentMemory())

AGENTES_MUESTRA = ["Manaure", "Tariwa", "Buko-ko", "Kori"]
K = 60

def informe_prompts(etiqueta, w, stimulus):
    p(f"\n== 1. PROMPTS — escenario: {etiqueta}  (K={K} construcciones por agente; la muestra léxica es aleatoria)")
    p("estímulo (user message):", len(stimulus), "chars ->", stimulus[:110].replace("\n", " "))
    ejemplo = {}
    for nm in AGENTES_MUESTRA:
        tot, secs, voces, llamadas = [], defaultdict(list), [], []
        for _ in range(K):
            s, u, n = construir(nm, w["state"], w["lexico"], w["observer"], stimulus,
                                w["memory"].get(nm), w["difusion"], w["idiolectos"],
                                w["competencia"], w["campo"])
            c, v = secciones(s)
            tot.append(len(s)); voces.append(v); llamadas.append(n)
            for k in set(list(c) + list(secs)):
                secs[k].append(c.get(k, 0))
        ejemplo[nm] = s
        a = ALL_AGENTS[nm]
        p(f"\n-- {nm} (tier {a['tier']}, etnia {a.get('etnia','(sin etnia)')}, ubicacion {a.get('ubicacion_default')})")
        p(f"   system total chars: media {statistics.mean(tot):.0f}  min {min(tot)}  max {max(tot)} | "
          f"ficha system_prompt {len(a.get('system_prompt') or '')} | user {len(stimulus)}")
        p(f"   voces en muestra_lexicon por prompt: media {statistics.mean(voces):.1f} min {min(voces)} max {max(voces)}")
        orden = ["persona","separador","identidad_linguistica","emocionar","rasgos_dialectales","mundo_estado",
                 "ubicacion","reglas_tier","muestra_lexicon","neologismos_adoptados","neologismos_pendientes",
                 "contagio","competencias","idiolecto","memoria","feedback"]
        m_tot = statistics.mean(tot)
        for k in orden:
            if k in secs and any(secs[k]):
                m = statistics.mean(secs[k])
                p(f"   {k:24} media {m:7.0f}  ({100*m/m_tot:4.1f}%)  min {min(secs[k])} max {max(secs[k])}  · {ESFERA[k]}")
    return ejemplo

# ── Escenario A: turno 1 del run (estado_inicial_test) ──
wA = mundo_fresco()
stimA = f"[Situación]: {wA['state'].evento_del_turno}. ¿Cómo reaccionas?"
ejA = informe_prompts("A · turno 1 (estado_inicial_test, sin historia)", wA, stimA)

# ── Escenario B: tras 24 turnos sintéticos con run_turn real ──
wB = mundo_fresco()
def resp_sintetica(system, user):
    m = re.match(r"Eres ([^,\.\n]+?)[,\.]", system)
    nm = m.group(1).strip() if m else "?"
    semillas = FORMAS_SEED.get(nm) or ["kuru", "arima", "biro"]
    raiz = random.choice([s for s in semillas if "-" not in s] or ["kuru"])
    return (f"Taya wana-ka {raiz} wara kari. Nüma naa-ni. Ta-barsure naba-ni. "
            f"[{raiz}-iro: {raiz}+-iro = {raiz} pequeño]")
def fake_invoke_B(client, system, user):
    CAPTURA.append((system, user))
    return resp_sintetica(system, user)
orch._invoke = fake_invoke_B
referentes = list(REFERENTES_NOVEDOSOS)
hablaron = Counter()
for t in range(24):
    naming = referentes.pop(0) if (referentes and t > 0 and t % 4 == 0) else None
    inter = orch.run_turn(None, wB["state"], wB["memory"], wB["lexico"], wB["observer"], verbose=False,
                          db=None, run_id=None, difusion=wB["difusion"], idiolectos=wB["idiolectos"],
                          campo=wB["campo"], competencia=wB["competencia"], naming_referente=naming,
                          ablacion=False, capas=CAPAS)
    hablaron.update(i["agent"] for i in inter)
orch._invoke = fake_invoke
stB = wB["state"]
stimB = orch.MOMENTOS_ESTIMULO.get(stB.momento, "¿Qué haces ahora?")
ejB = informe_prompts(f"B · tras 24 turnos sintéticos (run_turn real, respuestas sintéticas; día {stB.dia}, momento {stB.momento})", wB, stimB)
p("\n   agentes que hablaron en los 24 turnos sintéticos:", len(hablaron), "->", dict(hablaron))
p("   neologismos en LexicoComunitario:", len(wB["lexico"]._neologismos),
  "adoptados", len(wB["lexico"].neologismos_adoptados()))

# Guardar ejemplos completos
EJ = os.path.join(os.path.dirname(sys.argv[1]), "prompts_ejemplo.txt")
with open(EJ, "w", encoding="utf-8") as f:
    for esc, ej in (("A", ejA), ("B", ejB)):
        for nm, s in ej.items():
            f.write(f"\n\n######## ESCENARIO {esc} — {nm} ({len(s)} chars) ########\n{s}\n")
p("\nprompts completos de ejemplo en:", EJ)

# ════════════════════════════════════════════════════════════════════
# 2. Quién puede hablar en modo auto
# ════════════════════════════════════════════════════════════════════
p("\n== 2. ALCANZABILIDAD DE AGENTES (modo auto)")
roster = [a for a in orch.PARTICIPANTES_KOINE if a in ALL_AGENTS]
ev_ag = set()
for e in EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES:
    ev_ag.update(a for a in e.get("agentes_involucrados", []) if a in ALL_AGENTS)
alcanzables = {a for a in set(roster) | ev_ag | set(estado_inicial_test().agentes_en_escena)
               if ALL_AGENTS[a]["tier"] != 3}
p("roster PARTICIPANTES_KOINE:", len(roster), "| tiers:", Counter(ALL_AGENTS[a]["tier"] for a in roster))
p("agentes invocables por eventos (en ALL_AGENTS):", len(ev_ag))
p("T3 en eventos (se saltan en run_turn):", sorted(a for a in ev_ag if ALL_AGENTS[a]["tier"] == 3))
p("alcanzables en auto (T1/T2):", len(alcanzables))
p("T1/T2 NUNCA alcanzables en auto:", sorted(a for a in ALL_AGENTS if ALL_AGENTS[a]["tier"] != 3 and a not in alcanzables))
p("momentos alcanzables por avanzar_turno: amanecer/tarde; MOMENTOS_ESTIMULO define:", list(orch.MOMENTOS_ESTIMULO))

# ════════════════════════════════════════════════════════════════════
# 3. Filtros: ubicación/estación -> categorías relevantes
# ════════════════════════════════════════════════════════════════════
p("\n== 3. FILTROS POR CONTEXTO (categorias_relevantes)")
for loc in LOCACIONES:
    p(f"   ubicacion {loc:14} -> {sorted(categorias_relevantes(loc))}")
for est, d in ESTACIONES.items():
    s = ComunidadState(estacion=est, clima=d["clima_base"], evento_del_turno=None)
    p(f"   estacion {est:8} contexto base -> {sorted(categorias_relevantes(s.to_context_string()))}")

# ════════════════════════════════════════════════════════════════════
# 4. Diccionario
# ════════════════════════════════════════════════════════════════════
p("\n== 4. DICCIONARIO")
fam = Counter(normalize_source_language(d.get("fuente", "")) for d in VOCABULARIO_BASE.values())
p("VOCABULARIO_BASE por familia normalizada:", dict(fam.most_common()))
caq = {k: d for k, d in VOCABULARIO_BASE.items() if normalize_source_language(d.get("fuente", "")) == "caquetío"}
capa = Counter(capa_epistemica(d.get("fuente", "")) for d in caq.values())
p("caquetío por capa:", dict(capa))
en_base = {k: d for k, d in caq.items() if capa_epistemica(d.get("fuente", "")) in CAPAS}
sin_sig = [k for k, d in en_base.items() if not (d.get("sig") or d.get("es"))]
mues = {k: d for k, d in en_base.items() if (d.get("sig") or d.get("es"))}
p("en capas del perfil base:", len(en_base), "| sin sig (filtradas):", len(sin_sig), sin_sig[:10],
  "| muestreables:", len(mues))
fuera_capa = [k for k, d in caq.items() if capa_epistemica(d.get("fuente", "")) not in CAPAS]
p("caquetío fuera de capas base (retroabstraido etc.):", len(fuera_capa))
cats = Counter((d.get("categoria") or d.get("cat") or "otros") for d in mues.values())
p("categorías (clave categoria||cat) de las muestreables:", dict(cats.most_common()))
p("CATEGORIAS_BASE presentes como categoría?:", {c: (c in cats) for c in CATEGORIAS_BASE})
p("claves de PALABRAS_CLAVE_CATEGORIA presentes?:", {c: (c in cats) for c in PALABRAS_CLAVE_CATEGORIA})

def voces_y_p(contexto, tier):
    n = 20 if tier == 1 else 12
    goteo = max(2, n // 6)
    rel = CATEGORIAS_BASE | categorias_relevantes(contexto)
    total = 0; prob = {}
    for cat, size in cats.items():
        ne = n if (not contexto or cat in rel) else goteo
        k = min(ne, size); total += k
        for w, d in mues.items():
            pass
        prob[cat] = k / size
    return total, prob, rel

# contextos reales posibles: roster × {amanecer, tarde, cada evento}
ctxs = []
for nm in roster:
    a = ALL_AGENTS[nm]
    for est in ("seca", "lluvias"):
        for mom in ("amanecer", "tarde"):
            s = ComunidadState(estacion=est, momento=mom, clima=ESTACIONES[est]["clima_base"], evento_del_turno=None)
            stim = orch.MOMENTOS_ESTIMULO[mom]
            ctxs.append((a["tier"], f"{s.to_context_string()} {a['ubicacion_default']} {stim}"))
        for e in EVENTOS_COTIDIANOS + [x for x in EVENTOS_ESTACIONALES if x.get("estacion") in (None, est)]:
            s = ComunidadState(estacion=est, clima=ESTACIONES[est]["clima_base"], evento_del_turno=e["descripcion"],
                               eventos_activos=[e["id"]])
            stim = f"[Situación]: {e['descripcion']}. ¿Cómo reaccionas?"
            ctxs.append((a["tier"], f"{s.to_context_string()} {a['ubicacion_default']} {stim}"))
vt = defaultdict(list); pw = defaultdict(float); relc = Counter()
for tier, c in ctxs:
    tot, prob, rel = voces_y_p(c, tier)
    vt[tier].append(tot); relc.update(rel)
    for w, d in mues.items():
        pw[w] += prob[(d.get("categoria") or d.get("cat") or "otros")]
for w in pw: pw[w] /= len(ctxs)
p("contextos modelados:", len(ctxs), "(roster × estación × {amanecer, tarde, eventos del pool})")
for tier in sorted(vt):
    p(f"   tier {tier}: voces por prompt (uniforme, sin pesos) media {statistics.mean(vt[tier]):.1f} min {min(vt[tier])} max {max(vt[tier])}")
p("   frecuencia de categorías tratadas como relevantes:", dict(relc.most_common()))
ps = sorted(pw.values())
for umbral in (0.01, 0.02, 0.05, 0.10, 0.5):
    p(f"   voces con prob. media por prompt < {umbral}: {sum(1 for x in ps if x < umbral)} de {len(ps)}")
N_PROMPTS = 154
esperado_nunca = sum((1 - x) ** N_PROMPTS for x in pw.values())
p(f"   modelo: voces esperadas que NUNCA aparecen en {N_PROMPTS} prompts (n de db946685, prob. media, sin pesos): {esperado_nunca:.0f}")
por_cat_p = defaultdict(list)
for w, d in mues.items():
    por_cat_p[(d.get("categoria") or d.get("cat") or "otros")].append(pw[w])
for cat in sorted(por_cat_p, key=lambda c: -cats[c]):
    p(f"   cat {cat:14} tamaño {cats[cat]:4}  prob. media por prompt {statistics.mean(por_cat_p[cat]):.3f}")

# formas fijas de las plantillas
def buscar(tok):
    t = tok.lower().strip(".,;:()[]\"'")
    cands = [t]
    if "-" in t:
        cands += [t.split("-", 1)[1], t.split("-")[0]]
    for c in cands:
        if c in VOCABULARIO_BASE:
            d = VOCABULARIO_BASE[c]
            return c, d.get("fuente"), (d.get("sig") or "")[:50]
        if c in FUERA_DEL_HABLA:
            return c, "FUERA_DEL_HABLA:" + str(FUERA_DEL_HABLA[c].get("fuente")), (FUERA_DEL_HABLA[c].get("sig") or "")[:50]
    return t, None, ""

p("\n-- formas «forma (glosa)» en prompt_reglas_completo (Tier I)")
t1 = L.prompt_reglas_completo()
pares = re.findall(r"([A-Za-zÀ-ÿüÜ'\-]+) \(([^)]{1,40})\)", t1)
fcount = Counter(); vistos = set()
for forma, glosa in pares:
    if forma in vistos: continue
    vistos.add(forma)
    base, fuente, sig = buscar(forma)
    capa_ = capa_epistemica(fuente or "") if fuente and not str(fuente).startswith("FUERA") else fuente
    fcount[str(capa_) if fuente else "AUSENTE"] += 1
    p(f"   {forma:14} prompt:({glosa[:28]:28}) lexicón:{base:10} {str(fuente):28} sig:{sig}")
p("   resumen capas de formas del ejemplo T1:", dict(fcount))
p("\n-- tokens del ejemplo _IDENTIDAD_LINGUISTICA y conectores T2/T3")
toks = re.findall(r"[a-zü][a-zü\-]+", "taya wana-ka arima wara kari ta-barsure naba-ni kali-bana kali kati para kanoa hamaca "
                  "ka mara saa naka kashi wara suna masa naa kuru-bana")
for tk in dict.fromkeys(toks):
    base, fuente, sig = buscar(tk)
    p(f"   {tk:12} -> {base:10} {str(fuente):28} {sig}")
p("\n-- FORMAS_SEED (llegan como «sueles decir»)")
fs = Counter()
for nm, lst in FORMAS_SEED.items():
    for f_ in lst:
        base, fuente, _ = buscar(f_)
        fs[str(capa_epistemica(fuente) if fuente and not str(fuente).startswith('FUERA') else fuente)] += 1
p("   capas de las formas-semilla (con repetición):", dict(fs))
aus = sorted({f_ for lst in FORMAS_SEED.values() for f_ in lst if buscar(f_)[1] is None})
p("   formas-semilla ausentes del lexicón:", aus)
p("\n-- vocabulario nombrado en fichas T1/T2 (línea 'Vocabulario')")
for nm, a in list(AGENTS_T1.items()) + list(AGENTS_T2.items()):
    m = re.search(r"Vocabulario[^:]*:\s*([^\n]+)", a.get("system_prompt", ""))
    if m:
        ws = re.findall(r"[A-Za-zÀ-ÿü\-]+", m.group(1).split(".")[0])
        res = [(w, buscar(w)[1]) for w in ws if len(w) > 2]
        p(f"   {nm:12} " + "; ".join(f"{w}:{(capa_epistemica(f) if f and not str(f).startswith('FUERA') else f)}" for w, f in res))
n_esp = sum(1 for a in AGENTS_T2.values() if re.search(r"Español|Española", a.get("system_prompt", "")))
p(f"\n   fichas T2 que piden estilo en 'Español ...': {n_esp} de {len(AGENTS_T2)}")

# ════════════════════════════════════════════════════════════════════
# 5. Esferas no cargadas: corpus, asentamientos, etnias, lengua yaml
# ════════════════════════════════════════════════════════════════════
p("\n== 5. ESFERAS FUERA DEL MOTOR")
texto_motor_prompt = "\n".join(
    [a.get("system_prompt", "") for a in ALL_AGENTS.values() if a["tier"] != 3]
    + [a.get("descripcion", "") for a in AGENTS_T3.values()]
    + [e["descripcion"] for e in EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES]
    + [d["descripcion"] + " " + d["nombre"] for d in ESTACIONES.values()]
    + [estado_inicial_test().evento_del_turno] + list(orch.MOMENTOS_ESTIMULO.values())
    + [orch._IDENTIDAD_LINGUISTICA, L.prompt_reglas_completo(), L.prompt_reglas_breve()]
    + [r["desc"] for r in REFERENTES_NOVEDOSOS] + [e["disposicion"] for e in EMOCIONAR_SEED.values()]
    + list(orch.MOMENTOS_ESTIMULO.values()))
p("texto fijo que puede llegar a un prompt (fichas T1/T2, desc T3, eventos, estaciones, estímulos, plantillas, referentes, emocionar):",
  len(texto_motor_prompt), "chars")
low = texto_motor_prompt.lower()
for w in ("curiana", "golfete", "coro", "paraguaná", "aruba", "bonaire", "moruy", "guaranao", "amuay", "capubana", "kapubana",
          "santa ana", "cayerúa", "tacuato", "carirubana", "merejuy", "boratio", "diao", "apopo", "piache", "matrilineal",
          "taíno", "caribe", "guaycarí", "jirajara", "gayón", "perla", "casabe", "chicha", "budare", "sebucán"):
    p(f"   menciones '{w}': {len(re.findall(r'(?<![a-záéíóúñü])' + re.escape(w), low))}")

from compilar_corpus import cargar
hechos, gen, _ = cargar()
p("\ncorpus hechos:", len(hechos), "por archivo:", dict(Counter(h.get("_archivo") for h in hechos)))
p("   por fuente (etiqueta):", dict(Counter(h.get("fuente") for h in hechos)))
con_impl = [h for h in hechos if h.get("implicacion_simulacion")]
p("   con implicacion_simulacion:", len(con_impl), "| con agentes_relacionados:",
  sum(1 for h in hechos if h.get("agentes_relacionados")), "| con locacion:",
  sum(1 for h in hechos if h.get("locacion")), "| con palabra_lexicon:", sum(1 for h in hechos if h.get("palabra_lexicon")),
  "| hueco_lexico:", sum(1 for h in hechos if h.get("hueco_lexico")))
ag_corpus = Counter(a for h in hechos for a in (h.get("agentes_relacionados") or []))
p("   agentes más citados en corpus:", dict(ag_corpus.most_common(12)))
p("   agentes del roster sin ningún hecho relacionado:", sorted(a for a in roster if a not in ag_corpus))
no_usar = [h for h in con_impl if re.search(r"NO USAR|no usar|NO proyectar|no proyectar|no se proyecta|NO se proyecta|no debe|NO debe", str(h["implicacion_simulacion"]))]
p("   implicaciones con prohibición explícita (NO USAR / no proyectar / no debe):", len(no_usar))
if isinstance(gen, dict):
    p("genealogia: linajes", len(gen.get("linajes") or {}), "agentes", len(gen.get("agentes") or {}),
      "personas_de_fondo", len(gen.get("personas_de_fondo") or {}))
DUMP = os.path.join(os.path.dirname(sys.argv[1]), "implicaciones.txt")
with open(DUMP, "w", encoding="utf-8") as f:
    for h in con_impl:
        f.write(f"{h.get('id')} [{h.get('fuente')}] agentes={h.get('agentes_relacionados')} loc={h.get('locacion')}\n"
                f"   C: {' '.join(str(h.get('contenido','')).split())[:220]}\n"
                f"   I: {' '.join(str(h['implicacion_simulacion']).split())[:300]}\n")
p("   volcado de implicaciones en:", DUMP)

A = yaml.safe_load(open(os.path.join(REPO, "3-mundo", "asentamientos.yaml"), encoding="utf-8"))
nodos = A.get("nodos") or []
p("\nasentamientos nodos:", len(nodos), "precontacto:", dict(Counter(n.get("precontacto") for n in nodos)),
  "etiqueta:", dict(Counter(n.get("etiqueta") for n in nodos)))
mencionados = [n.get("nombre") for n in nodos if n.get("nombre") and n["nombre"].lower() in low]
p("   nodos cuyo nombre aparece en el texto fijo del motor:", mencionados)
E = yaml.safe_load(open(os.path.join(REPO, "3-mundo", "etnias.yaml"), encoding="utf-8"))
ets = E.get("etnias") or []
p("etnias:", len(ets), "polity_caquetia:", dict(Counter(e.get("polity_caquetia") for e in ets)))
etn_ag = Counter(a.get("etnia") for a in ALL_AGENTS.values())
p("   etnias del elenco:", dict(etn_ag))
for e in ets:
    nombres = {e.get("nombre", "").lower()} | {v.lower() for v in (e.get("variantes") or [])}
    if any(any(n and n in (ea or "") for n in nombres) for ea in etn_ag):
        p(f"   {e['id']} {e['nombre']}: polity_caquetia={e.get('polity_caquetia')} etiqueta={e.get('etiqueta')} intensidad={e.get('intensidad')}")
T = yaml.safe_load(open(os.path.join(REPO, "2-lengua", "toponimos.yaml"), encoding="utf-8"))
tops = T.get("toponimos") or []
p("\ntoponimos.yaml:", len(tops), "nivel:", dict(Counter(t.get("nivel") for t in tops)))
p("   formas en VOCABULARIO_BASE:", sum(1 for t in tops if str(t.get("forma", "")).lower() in VOCABULARIO_BASE))
p("   formas mencionadas en el texto fijo del motor:", sorted({t["forma"] for t in tops if len(str(t.get('forma',''))) > 3
                                                              and re.search(r'(?<![a-zü])' + re.escape(str(t['forma']).lower()) + r'(?![a-zü])', low)}))
C = yaml.safe_load(open(os.path.join(REPO, "2-lengua", "cognados.yaml"), encoding="utf-8"))
cogs = C.get("cognados") or []
cq = [str((c.get("formas") or {}).get("CQ", "")).lower() for c in cogs if (c.get("formas") or {}).get("CQ")]
p("cognados.yaml:", len(cogs), "con forma CQ:", len(cq), "CQ en VOCABULARIO_BASE:", sum(1 for f_ in cq if f_ in VOCABULARIO_BASE))
M = yaml.safe_load(open(os.path.join(REPO, "2-lengua", "morfemas.yaml"), encoding="utf-8"))
mors = M.get("morfemas") or []
t12 = (L.prompt_reglas_completo() + L.prompt_reglas_breve() + orch._IDENTIDAD_LINGUISTICA)
p("morfemas.yaml:", len(mors), [m_["forma"] for m_ in mors])
p("   en TODAS_LAS_REGLAS:", [m_["forma"] for m_ in mors if m_["forma"] in TODAS_LAS_REGLAS])
p("   en plantillas T1/T2:", [m_["forma"] for m_ in mors if m_["forma"] in t12])
p("TODAS_LAS_REGLAS claves:", list(TODAS_LAS_REGLAS), "| en plantillas T1/T2:", [k for k in TODAS_LAS_REGLAS if k in t12])
p("CULTURA_CAQUETIA.md bytes:", os.path.getsize(os.path.join(REPO, "3-mundo", "CULTURA_CAQUETIA.md")))
p("prompt_polity('costera') chars (código muerto):", len(curiana_polities.prompt_polity("costera")))

p("\n-- módulos lexicon_* que el motor NO importa (tamaño de sus dicts de nivel superior, y solapamiento con VOCABULARIO_BASE)")
import importlib
for modn in ("lexicon_toponimos", "lexicon_candidatos", "lexicon_alvarado", "lexicon_gatschet", "lexicon_perea", "lexicon_van_buurt"):
    try:
        mod = importlib.import_module(modn)
        dd = {k: v for k, v in vars(mod).items() if k.isupper() and isinstance(v, dict)}
        claves = set().union(*[set(v) for v in dd.values()]) if dd else set()
        p(f"   {modn}: " + ", ".join(f"{k}={len(v)}" for k, v in dd.items())
          + f" | claves distintas {len(claves)}, fuera de VOCABULARIO_BASE {len([c for c in claves if str(c).lower() not in VOCABULARIO_BASE])}")
    except Exception as ex:
        p(f"   {modn}: error {ex}")
OUT.close()
```

### B · medir_esferas_2.py (voces fijas, plantilla tier I contra el lexicón, estado muerto, etnias, implicaciones)

```python
# -*- coding: utf-8 -*-
"""Segunda pasada: afina el diccionario, las plantillas y las esferas."""
import os, re, sys, types, statistics
from collections import Counter, defaultdict
_stub = types.ModuleType("dotenv"); _stub.load_dotenv = lambda *a, **k: False
sys.modules["dotenv"] = _stub
REPO = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
sys.path.insert(0, os.path.join(REPO, "curiana_sim"))
OUT = open(sys.argv[1], "w", encoding="utf-8")
def p(*a): print(*a, file=OUT)

import yaml
import curiana_orchestrator_v2 as orch
import curiana_lexicon as L
from curiana_lexicon import VOCABULARIO_BASE, capa_epistemica, categorias_relevantes, CATEGORIAS_BASE, FUERA_DEL_HABLA, LexicoComunitario, score_linguistico
from curiana_database import normalize_source_language
from curiana_agents import ALL_AGENTS, AGENTS_T1, AGENTS_T2, AGENTS_T3
from curiana_state import ComunidadState, ESTACIONES, EVENTOS_COTIDIANOS, EVENTOS_ESTACIONALES
from curiana_perfiles import cargar_perfil
CAPAS = cargar_perfil("base").capas

caq = {k: d for k, d in VOCABULARIO_BASE.items() if normalize_source_language(d.get("fuente", "")) == "caquetío"
       and capa_epistemica(d.get("fuente", "")) in CAPAS and (d.get("sig") or d.get("es"))}
cat_of = lambda d: d.get("categoria") or d.get("cat") or "otros"
cats = Counter(cat_of(d) for d in caq.values())
p("== A. muestreables base:", len(caq), "| entradas con `categoria` semántica explícita:",
  sum(1 for d in caq.values() if d.get("categoria")))
p("   categoría (clave usada) por capa:")
cc = defaultdict(Counter)
for d in caq.values(): cc[cat_of(d)][capa_epistemica(d["fuente"])] += 1
for c in sorted(cc, key=lambda c: -cats[c]): p(f"     {c:14} {dict(cc[c])}")

# voces siempre presentes (p = 1 en TODO contexto) por tier
for tier, n in ((1, 20), (2, 12)):
    goteo = max(2, n // 6)
    siempre = [c for c, s in cats.items() if s <= goteo]
    nunca_rel_max = {c: min(goteo, s) for c, s in cats.items()}
    fijas = [k for k, d in caq.items() if cat_of(d) in siempre]
    p(f"\n== B. tier {tier}: n_por_categoria={n}, goteo={goteo}")
    p(f"   categorías que se muestran ENTERAS en todo prompt (tamaño <= goteo): {len(siempre)} -> {sum(cats[c] for c in siempre)} voces fijas")
    p("   voces fijas y su capa:", ", ".join(f"{k}({capa_epistemica(VOCABULARIO_BASE[k]['fuente']).split('-')[1][:4]})" for k in sorted(fijas)))
    p(f"   sust: {min(goteo, cats['sust'])} de {cats['sust']} por prompt; v_raiz: {min(goteo, cats['v_raiz'])} de {cats['v_raiz']}")
    # techo: voces si TODAS las categorías semánticas presentes fueran relevantes
    base_total = sum(min(goteo, s) for s in cats.values())
    p(f"   voces por prompt sin ninguna categoría relevante: {base_total}; "
      f"máximo si todas las semánticas presentes fueran relevantes: "
      f"{sum(min(n if c in ('geografia','fauna','flora','cosmos','comercio','ritual','cuerpo','gramatica') else goteo, s) for c, s in cats.items())}")

# plantilla Tier I: listas de VOCABULARIO DISPONIBLE
t1 = L.prompt_reglas_completo()
p("\n== C. plantilla Tier I — «VOCABULARIO DISPONIBLE [N palabras]»:",
  re.search(r"VOCABULARIO DISPONIBLE \[(\d+) palabras\]", t1).group(1))
cap = Counter(); detalle = []
for etiqueta in ("PRONOMBRES", "VERBOS", "NATURALEZA", "PERSONAS", "COSAS", "CONECTORES", "CUERPO", "NÚMEROS"):
    linea = re.search(rf"  {etiqueta}:\s+([^\n]+)", t1).group(1)
    for forma, glosa in re.findall(r"([^\s·()]+) \(([^)]+)\)", linea):
        d = VOCABULARIO_BASE.get(forma)
        if d is None and forma in FUERA_DEL_HABLA:
            k = "RETIRADA (FUERA_DEL_HABLA)"; sig = FUERA_DEL_HABLA[forma]["sig"]
        elif d is None:
            k = "AUSENTE del lexicón"; sig = ""
        else:
            k = capa_epistemica(d["fuente"]) or normalize_source_language(d["fuente"]); sig = d.get("sig", "")
        cap[k] += 1
        if not k.startswith("caquetío") or glosa.split("/")[0].split(",")[0].strip() not in sig:
            detalle.append(f"{etiqueta}:{forma} prompt=({glosa}) -> {k} lexicón=«{sig[:60]}»")
p("   formas léxicas listadas:", sum(cap.values()), dict(cap))
for x in detalle: p("   ·", x)
for alt in ("buko", "kanoa", "korie", "konuko", "amaka", "hamaka", "boratio", "corie", "buco", "conuco", "canoa", "hamaca", "piache"):
    d = VOCABULARIO_BASE.get(alt)
    p(f"   ¿{alt} en VOCABULARIO_BASE? {bool(d)}" + (f" {d['fuente']} «{d.get('sig','')[:50]}»" if d else ""))
lc = LexicoComunitario()
for frase in ("taya buco canoa corie conuco hamaca piache", "taya buko kanoa korie konuko boratio"):
    m = score_linguistico(frase, lc)
    p(f"   score_linguistico('{frase}') -> arahuacas {m['palabras_arahuacas']} caquetias {m['palabras_caquetias']}")
p("   ejemplo T1 usa 'buco-ana' y enseña '-ana = lugar de X';  -ana en prompt_reglas_breve:", "-ana (lugar de)" in L.prompt_reglas_breve())
p("   evidencia de -gua en REGLAS_LOCATIVAS:", L.REGLAS_LOCATIVAS["-gua"]["evidencia"])
p("   -kana en REGLAS_NUMERO (wayunaiki):", L.REGLAS_NUMERO["-kana"]["wayunaiki"])
p("   las plantillas llevan etiqueta epistémica? 'reconstruido' en T1:", "reconstru" in t1, "| 'hipot' en T1:", "hipot" in t1,
  "| 'atestigu' en T1:", "atestigu" in t1)
# muestra: ¿lleva etiqueta por voz?
m = L.muestra_caquetio_dinamica(n_por_categoria=20, contexto="orilla", capas=CAPAS)
p("   la muestra dinámica marca capa por voz?:", any(s in m for s in ("reconstru", "hipot", "atestig")))
hip = [k for k, d in caq.items() if capa_epistemica(d["fuente"]) == "caquetío-hipotético"]
p("   voces hipotéticas muestreables sin marca:", len(hip), sorted(hip)[:40])

# ═══ D. estado: campos que nunca llegan al prompt
p("\n== D. curiana_state — qué campos usa to_context_string")
import inspect, curiana_state
src = inspect.getsource(ComunidadState.to_context_string)
for campo in ("dia", "turno", "momento", "clima", "nivel_alimentos", "nivel_sal", "nivel_tension", "evento_del_turno",
              "eventos_activos", "historial_eventos", "agentes_en_escena", "ubicaciones_override", "tensiones_activas",
              "notas_orquestador", "estacion"):
    p(f"   {campo:22} en to_context_string: {('self.'+campo) in src}")
motor_src = "".join(open(os.path.join(REPO, "curiana_sim", f), encoding="utf-8").read() for f in
                    ("curiana_orchestrator_v2.py", "curiana_social.py", "curiana_koine.py", "curiana_observer.py", "curiana_lexicon.py"))
for sym in ("tensiones_activas", "historial_eventos", "notas_orquestador", "ACTIVIDADES_POR_MOMENTO", "actividades_primarias",
            "meses_equiv", '"actividades"', "ubicaciones_override[", "ubicaciones_override.get", "descripcion\"", "edad", "genero"):
    p(f"   uso de {sym} fuera de curiana_state (orq/social/koine/observer/lexicon): {motor_src.count(sym)}")
p("   ESTACIONES campos:", {k: list(v) for k, v in ESTACIONES.items()}["seca"])
p("   eventos: total", len(EVENTOS_COTIDIANOS) + len(EVENTOS_ESTACIONALES),
  "| sin clave estacion:", sum(1 for e in EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES if "estacion" not in e))
# campos por agente que no llegan al prompt de T1/T2
p("   campos de agente:", sorted({k for a in ALL_AGENTS.values() for k in a}))

# ═══ E. menciones de 'Curiana' por fuente del texto fijo
p("\n== E. ancla geográfica fija ('Curiana' / 'Golfete') por pieza")
piezas = {
    "fichas T1 system_prompt": "\n".join(a["system_prompt"] for a in AGENTS_T1.values()),
    "fichas T2 system_prompt": "\n".join(a["system_prompt"] for a in AGENTS_T2.values()),
    "descripciones T1/T2 (observer curado)": "\n".join(a["descripcion"] for a in list(AGENTS_T1.values()) + list(AGENTS_T2.values())),
    "descripciones T3": "\n".join(a["descripcion"] for a in AGENTS_T3.values()),
    "eventos": "\n".join(e["descripcion"] for e in EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES),
    "MOMENTOS_ESTIMULO": "\n".join(orch.MOMENTOS_ESTIMULO.values()),
    "to_context_string": inspect.getsource(ComunidadState.to_context_string),
    "call_agent (base T3)": inspect.getsource(orch.call_agent),
    "DIRECTOR_SYSTEM": orch.DIRECTOR_SYSTEM,
    "OBSERVER_SYSTEM + curado": inspect.getsource(__import__("curiana_observer")),
    "REFERENTES_NOVEDOSOS": "\n".join(r["desc"] for r in __import__("curiana_koine").REFERENTES_NOVEDOSOS),
}
for k, v in piezas.items():
    p(f"   {k:38} Curiana={len(re.findall('Curiana', v))} Golfete/golfete={len(re.findall('[Gg]olfete', v))}")
p("   fichas T1/T2 con 'Curiana':", sum(1 for a in list(AGENTS_T1.values()) + list(AGENTS_T2.values()) if "Curiana" in a["system_prompt"]),
  "de", len(AGENTS_T1) + len(AGENTS_T2))

# ═══ F. etnias
E = yaml.safe_load(open(os.path.join(REPO, "3-mundo", "etnias.yaml"), encoding="utf-8"))
p("\n== F. etnias.yaml")
for e in E["etnias"]:
    p(f"   {e['id']} {e.get('nombre')} var={e.get('variantes')} fam={e.get('familia_linguistica')} polity={e.get('polity_caquetia')} "
      f"etiq={e.get('etiqueta')} contacto={e.get('tipo_de_contacto')}")
p("   etnias del elenco:", sorted({str(a.get('etnia')) for a in ALL_AGENTS.values()}))
from curiana_social import DIALECTOS
p("   DIALECTOS (densidad objetivo):", {k: v["densidad_objetivo"] for k, v in DIALECTOS.items()})

# ═══ G. corpus: implicaciones que piden algo al motor
sys.path.insert(0, os.path.join(REPO, "curiana_sim"))
from compilar_corpus import cargar
hechos, gen, _ = cargar()
impl = [h for h in hechos if h.get("implicacion_simulacion")]
pat = {
    "nombra agente": lambda t, h: bool(h.get("agentes_relacionados")),
    "habla de evento/ritual/escena": lambda t, h: bool(re.search(r"evento|escena|ritual|ceremonia", t, re.I)),
    "habla de prompt/ficha/system": lambda t, h: bool(re.search(r"prompt|ficha|system_prompt|personaje", t, re.I)),
    "habla de estación/calendario": lambda t, h: bool(re.search(r"estaci[oó]n|seca|lluvias|calendario", t, re.I)),
    "habla de locación/lugar": lambda t, h: bool(h.get("locacion")) or bool(re.search(r"locaci[oó]n|LOCACIONES", t)),
    "advierte regla 3 (colonial/no proyectar)": lambda t, h: bool(re.search(r"colonial|NO USAR|no proyectar|precontacto", t, re.I)),
    "hueco léxico / sembrar": lambda t, h: bool(h.get("hueco_lexico")) or bool(re.search(r"sembr|hueco", t, re.I)),
    "dice 'ya aplicado'": lambda t, h: bool(re.search(r"ya aplicad|ya est[aá] en el canon|ya existe", t, re.I)),
}
p("\n== G. corpus — implicaciones:", len(impl))
for k, f in pat.items():
    p(f"   {k:42} {sum(1 for h in impl if f(str(h['implicacion_simulacion']), h))}")
p("   por etiqueta (fuente) de los hechos con implicacion:", dict(Counter(h.get("fuente") for h in impl)))
p("   hipotético/canon-simulacion con implicacion:", sum(1 for h in impl if h.get("fuente") in ("hipotetico", "canon-simulacion")))
locs = Counter(h.get("locacion") for h in hechos if h.get("locacion"))
p("   locaciones citadas por el corpus:", dict(locs))
pl = [h.get("palabra_lexicon") for h in hechos if h.get("palabra_lexicon")]
p("   palabra_lexicon citadas:", len(pl), "distintas", len(set(pl)), "| de ellas muestreables en base:", sum(1 for w in set(pl) if w in caq),
  "| retroabstraidas/fuera:", sum(1 for w in set(pl) if w in VOCABULARIO_BASE and w not in caq))
for h in impl:
    t = str(h["implicacion_simulacion"])
    if re.search(r"NO USAR|no proyectar|NO proyectar|no debe|NO debe", t):
        p(f"   PROHIBICIÓN {h['id']} [{h.get('fuente')}] agentes={h.get('agentes_relacionados')}: {' '.join(t.split())[:260]}")
OUT.close()
```

### C · medir_esferas_3.py (glosas que viajan al prompt, voces de Medina, etnias del roster)

```python
# -*- coding: utf-8 -*-
import os, re, sys, types
from collections import Counter
_s = types.ModuleType("dotenv"); _s.load_dotenv = lambda *a, **k: False; sys.modules["dotenv"] = _s
REPO = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
sys.path.insert(0, os.path.join(REPO, "curiana_sim"))
import curiana_orchestrator_v2 as orch
from curiana_lexicon import VOCABULARIO_BASE, capa_epistemica
from curiana_database import normalize_source_language
from curiana_agents import ALL_AGENTS
from curiana_perfiles import cargar_perfil
CAPAS = cargar_perfil("base").capas
out = open(sys.argv[1], "w", encoding="utf-8")
def p(*a): print(*a, file=out)
caq = {k: d for k, d in VOCABULARIO_BASE.items() if normalize_source_language(d.get("fuente","")) == "caquetío"
       and capa_epistemica(d.get("fuente","")) in CAPAS and d.get("sig")}
pats = {
 "sig cita otra lengua (wayunaiki/wayuu/lokono/taíno/<)": r"[Ww]ayunaiki|wayuu|[Ll]okono|[Tt]a[ií]no|<",
 "sig con marca de época moderna (hoy/extint/desaparecid/actual/resto del país)": r"\bhoy\b|extint|desaparecid|actual|resto del pa[ií]s",
 "sig con marca regional moderna (península/oriente/occidente/Paraguaná/Falcón)": r"pen[ií]nsula|\boriente\b|\boccidente\b|Paraguan|Falc[oó]n",
}
for k, rx in pats.items():
    hits = sorted(w for w, d in caq.items() if re.search(rx, d["sig"]))
    p(f"{k}: {len(hits)} de {len(caq)} -> {hits[:30]}")
med = [w for w, d in caq.items() if re.search(r"Medina", str(d.get("notas","")) + str(d.get("glosa_fuente","")))]
p("muestreables base cuyas notas/glosa_fuente citan a Medina:", len(med), "por capa:",
  dict(Counter(capa_epistemica(caq[w]["fuente"]) for w in med)), sorted(med)[:30])
for w in ("niwa","jején","hikotea","yawasa","komején","jaiba","siwato","wayakán","magey","mütsia","sünatü","curiana","hayo","ana","bana"):
    d = VOCABULARIO_BASE.get(w)
    if d: p(f"  {w:9} {d['fuente']:24} cat={d.get('categoria') or d.get('cat')} notas={' '.join(str(d.get('notas','')).split())[:150]}")
roster = [a for a in orch.PARTICIPANTES_KOINE if a in ALL_AGENTS]
p("roster por etnia:", dict(Counter(ALL_AGENTS[a].get("etnia") for a in roster)))
p("descripcion de Manaure contiene 'Heredó de su padre':", "Heredó de su padre" in ALL_AGENTS["Manaure"]["descripcion"])
p("descripciones con 'matrilineal':", [n for n, a in ALL_AGENTS.items() if "matrilineal" in a.get("descripcion","")])
out.close()
```
