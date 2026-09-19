---
tipo: bitacora
era: desarrollo del motor (2026-06-22 → 2026-07-06)
runs: 6
respuestas: 1489
estatus: cerrada — ningún run corrió sobre la base actual
---

# Bitácora de Runs — Simulación Curiana

> 🔒 **Los seis runs de esta bitácora son PRUEBAS DE DESARROLLO DEL MOTOR, no
> resultados del experimento.** Decisión de Miguel, 2026-08-03.
>
> **No son comparables entre sí.** Entre corrida y corrida cambió el motor **y**
> el instrumento que los mide: el lexicón pasó de ~1717 a ~1276 entradas entre
> el baseline y el primer koiné (el aislamiento de las 441 hipotéticas, commit
> `3b490b7`), y esa misma madrugada se tocó `score_linguistico` dos veces. El
> salto de 92.2% a 99.2% de caquetío **no es atribuible a una sola causa**.
>
> **La única evidencia limpia** es el par de ablación del 2026-07-06
> (`038d7b9d` vs `bdc54134`): mismo motor, mismo día, una sola variable.
>
> El análisis completo está en [[01_que_probaron_los_seis_runs]]; la historia,
> en [[LINEA_DE_TIEMPO]]; y el protocolo para que la próxima tanda sí sea
> analizable, en [[04_protocolo_run_1_era_auditada]].
>
> **Estos runs se conservan y no se borran** — documentan cómo se construyó el
> motor. Pero el sitio público no re-exporta desde ellos, y cualquier cita de
> sus números lleva esta advertencia.

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

## Era auditada

> Desde aquí, los runs corren con la **base sellada** (`huella_de_base`, #68).
> Cada fila guarda el commit del motor, si estaba sucio y los hashes del
> lexicón, el corpus y el elenco. Protocolo: [[04_protocolo_run_1_era_auditada]].

### Era 2 · serie C — la escena por lugar, en dos brazos (desde el 2026-09-18)

> Miguel, 2026-09-17: «si no se mueven, ¿cómo podemos hacer que hagan cosas y
> "existan" en el mundo que les describimos?». El diseño está en
> `6-fusion/issues-pendientes/existir-en-el-mundo-escena-por-lugar-2026-09-17.md`
> y sus diez decisiones en `6-fusion/decisiones_tanda_2026-09-17.yaml`: el
> ámbito de lo que un agente ve es el LUGAR donde está (oficio × momento,
> `6-fusion/escena_era2.yaml`), oye lo que se dijo allí el momento anterior,
> y el Capubana (cada 3 días) mezcla a los 63. Va como brazo: la misma
> cadena con `--escena` y sin ella, mismas semillas 21/22/23. Motor de la
> serie: #157 (ESTAR), #155 (presencias), #159 (OÍR + control), #156
> (prestigio por alias), #154 (`{tu agua}`), #163 (la etiqueta manda),
> #158 (el mapa). «Lanza cuando lo tengas listo» (Miguel, 2026-09-18).
>
> ⚠️ **La cadena de abajo (`76ecf45c → 96b22194`) queda del OTRO lado del corte
> de serie del punto 8** («dale pues con A», 2026-09-18): en esos dos días el
> ejemplo del prompt todavía podía registrarse como acuñación, y de hecho
> `kali-bana` lideraba «las cuentas» 15,8 contra 3,1 el día 2. **La serie C se
> re-corre entera desde el día 1** con la puerta puesta; estos dos días se
> conservan como la medición que la encontró, no como los días 1 y 2 de la
> serie.

| Fecha | Run (id8) | Turnos/Días | Agentes | Score | Caquetío | Estado / hito |
|---|---|---|---|---|---|---|
| 09-18 | `b7bc51dc` | 6 / 1 | **63** | 7.4 | 100% | **Día 1 de la serie C, brazo CON escena** (motor `5770de6`, semilla 21, `--escena --capubana-cada 3 --reflexion`; 11 min, 0 avisos). 72 respuestas, 61 agentes, **0 residuos** de la era 1; score 7,43 (tier 1: 7,11 · tier 2: 7,48 · tier 3: 8,26). **La escena existe en la base**: 378 presencias (63 × 6), 28 lugares; 91 escenas en el día, 40 con alguna voz, 18 con dos o más; 50 de 72 intervenciones (69 %) hablaron con compañía en su lugar. Un solo lugar compartido entre nodos, el camino Moruy–Caseto (Humohumo y Bajari), con los dos nodos a la vez en 3 turnos. **La predicción del diseño se cumple en lo inmediato**: cruces de forma «en el mismo turno» **3 → 0**; Δturnos hasta salir del lugar mediana 1 → **2**; de 231 formas emergentes, 72 salieron de su lugar, **149 murieron en él** y 29 nacieron en varios a la vez (el evento de nombramiento sigue yendo a los 12 del turno: capa 3). Koiné: acumulada 0,7809, ventana 0,6269, **emergente 0,9608** (serie B día 1: 0,906 — lo nuevo converge menos, que es lo que un ámbito por lugar debe hacer). Acuñaciones: **39 propuestas, sólo 6 adoptadas** (serie B: 18/12): la adopción ahora es por ámbito. La competencia por las cuentas **no se fija el día 1** (en disputa: `kali-uco-aima` 3,6 · `ucibo-kali-duruco` 3,5 · `kali-boro` 2,8); y la primera forma **adoptada en DOS ámbitos**: `kali-bana` «la cumbre del sol», nacida en Moruy (GUARANAO) y adoptada también en Carirubana:taller_canoas (AMUAY), Δ4 turnos — ¿viajó o se re-acuñó? (agente midiendo). Préstamos: 2, ya con la forma de la esfera y la dicha aparte (`maisi` ← «maíz», `aji`). El mundo: sal 47 de 72, viento 38, cerro 37, venado 2. GUARANAO habló el 71 % (censo 62 %). Reflexión del Director sin residuos, citada abajo. Mapa exportado (`content/simulador/escena/b7bc51dc.json`): por primera vez con gente. **Deudas del día**: `agent_responses.lugar` quedó vacío (0 de 72: el orquestador no pasa `lugar` a `save_agent_response`; `presencias` lo cubre); el exportador lee la tabla propuesta y no `escena_era2.yaml`, así que el camino Moruy–Caseto sale sin coordenada; y la página del mapa tiene que poder elegir el run |
| 09-18 | `76ecf45c` | 6 / 1 | **63** | 7.5 | 100% | **Día 1 de la serie C, REPETIDO con el motor arreglado — el que cuenta** (motor `55c0299`, semilla 21, mismos flags; `b7bc51dc` queda como prueba de la escena). Entraron entre uno y otro: la competencia que sobrevive la noche y el Capubana que junta ámbitos (#167), el lugar en cada respuesta y el mapa con la tabla decidida (#166). 72 respuestas, 61 agentes, score 7,49; **`agent_responses.lugar` 72 de 72**, 21 lugares, 0 discrepancias con `presencias`. La escena, igual de poblada: 378 presencias en 28 lugares, 91 escenas, 40 con voz, 18 con dos o más, 69 % de las intervenciones con compañía; el único lugar de contacto vuelve a ser el camino Moruy–Caseto, 3 turnos con los dos nodos. Formas emergentes 218: **150 murieron en su lugar**, 55 salieron (mediana 1 turno), 29 nacieron en varios a la vez, **0 cruces en el mismo turno**; 14 pasaron por un lugar compartido (antes 8). Koiné: acumulada 0,787 · ventana 0,649 · **emergente 0,9485**. Acuñaciones 30, adoptadas 5, y **dos formas adoptadas en dos ámbitos**: `siwato-ni` «estoy desganado» (Tacuato + Tacuato:matorral — dos ámbitos del mismo sitio, o sea el contacto que la escena sí permite) y `kali-bana` otra vez (El Cayude + ZG2). ⚠️ **`kali-bana` ya no sólo se registra: compite.** El ejemplo de la plantilla entró como rival de «las cuentas» (`brilu-uco` 2,9 · `kali-bana` 2,8 · `kali-iro-bana` 2,0), así que el falso neologismo de plantilla ahora contamina la métrica de koiné, no sólo el conteo — la decisión de `6-fusion/issues-pendientes/publicados/formas-de-plantilla-en-la-registracion-2026-09-18.md` deja de ser cosmética (y se tomó al día siguiente: punto 8 del cambio de instrumento). La competencia **queda abierta y persistida** en `curiana_koine.json` (por primera vez): el día 2 la hereda. Préstamos: 0. El mundo: sal 42 de 72, cerro 37, viento 33, venado 1. Un único «residuo» y es legítimo: Ebokoa dice «Tacuato-ana… Curiana-ana» nombrando tierras lejanas, y `curiana` es topónimo del canon al otro lado del golfo |

| 09-18 | `96b22194` | 6 / 1 | **63** | 7.4 | 100% | **Día 2 de la serie C** (`--continuar --semilla 22`, mismos flags). **El arreglo de la competencia funciona**: la cabecera dice «competencias heredadas, aún en disputa: cuentas_vidrio (9 variantes)» — por primera vez una disputa cruza la noche. Y el día 2 recibe su referente propio (el cometa), como manda `referentes_introducidos`. 72 respuestas, 60 agentes, score 7,42, `lugar` en 72 de 72 (22 lugares), 378 presencias. Koiné: acumulada 0,787 → **0,648**, ventana 0,649 → **0,517**, emergente 0,9485 → **0,903**; el veredicto de la cadena dice «NO converge» porque exige >5 % de caída y la emergente cayó 4,8 % — con dos días es «todavía no», no un resultado. Tres formas adoptadas en dos ámbitos, y la tercera es la primera que cruza de verdad entre nodos: `naa-ni` «estoy yendo» (Capubana + Caseto). ⚠️ **Y el hallazgo que para la cadena: `kali-bana` va ganando la competencia de «las cuentas» 15,8 contra 3,1 y 2,9** — es el ejemplo literal de la plantilla que los 63 leen en su system prompt cada turno. Medido: día 1, 2 usos de 2 agentes; **día 2, 12 usos de 11 agentes**, en 10 lugares y en los DOS nodos, mientras las rivales de verdad se apagan (`brilu-uco` 0 usos el día 2, `kali-iro-bana` 1, las tres del día 1 a 0). Un aviso más de la cadena: 3 de 63 agentes heredan idiolecto sin formas-semilla (vienen de un run anterior al 09-16). **El día 3 NO se lanzó**: es el de Capubana, donde todos ven todo, y habría fijado `kali-bana` como la palabra de la koiné para las cuentas — el titular de la serie habría sido un artefacto del prompt. La cadena `76ecf45c → 96b22194` queda cerrada en dos días |

**Lo que piensa el Director del día 1 repetido** (`76ecf45c`, escrito por el motor):

> El viento del este sopló sin pausa y la gente se movió en torno a lo que
> falta: alimento, sal baja, agua que no alcanza. Manaure convocó al cerro
> cuando algo brilló en el agua clara de Carirubana, y eso cambió el ritmo
> del día —de la dispersión en sombras al llamado. Las palabras nuevas
> vinieron de varios lados: Birokoa nombró dos veces lo que el agua cargada
> hace, Jachos buscó nombres para lo que se va sin fuerza, y al final fueron
> cinco las que prendieron en la lengua común: *siwato-ni* para la desgana
> que camina aquí, *brilu-uco* para ese brillo en el agua que nadie sabía
> cómo decir, *kali-bana* para lo que vieron en el cerro. […] Mañana sabremos
> si Kunaro-bana y Jachos traen pesca de los jachos encendidos, o si ese
> brillo en el agua sigue siendo sin nombre claro.

Lectura del escriba: «de la dispersión en sombras al llamado» es la escena
contada desde fuera, y es exacta. Pero *kali-bana* no es una palabra que
prendiera: es el ejemplo del prompt, y el Director la celebra porque el
registro se la dio como acuñación. Es el mejor argumento para decidir el
filtro de formas de plantilla.

**Lo que pensó el Director del día 1 de prueba** (`b7bc51dc`, escrito por el motor):

> El viento del este sopló firme todo el turno y la gente bajó a pescar con
> los jachos encendidos, pero el hambre está en los gestos antes que en el
> habla. Vimos cómo la tensión creció sin necesidad de gritos: en los conucos
> secos, en las manos que trabajan la sal baja, en Manaure cuando convocó
> desde la piedra del Capubana. Prendieron bien las palabras nuevas sobre lo
> que brilla —*ucibo-kali-duruco*, *kali-uco-aima*— como si la gente
> necesitara nombrar lo que ve en el agua clara para no pensar en lo que
> falta en los vientres. Ninguna palabra brotó natural del hambre o la
> sequía; todas las nuevas fueron sobre luz y dureza, sobre lo que el alisio
> permite ver. Mañana el viento sigue y el agua sigue clara, pero la sal
> escasea de verdad y alguien tendrá que hablar de eso sin rodeos, o la
> tensión quiebra lo que hoy apenas sostiene.

Lectura del escriba: el Director ve la escena («en los conucos secos, en las
manos que trabajan la sal baja, en Manaure… desde la piedra del Capubana»)
porque recibe las intervenciones agrupadas por lugar. «Prendieron bien» las
dos formas de las cuentas es generoso: ninguna se fijó; están en disputa, y
por primera vez la disputa tiene geografía.

### Era 2 · serie B — el instrumento completo (desde el 2026-09-17)

> Miguel, 2026-09-16: «recorramos nuevamente con este cambio; dejemos esos 3
> runs como pruebas; volvamos a empezar desde 0». Los tres días del 16
> (`c6837386`, `89fc1744`, `0193873d`) quedan como **serie A: pruebas del
> motor de la era 2, sin pre-carga de idiolectos** (62 de 63 agentes
> arrancaban iguales). La serie B corre con `--serie era2-b` sellado en la
> config, la pre-carga de #145, el Director con mundo (#138, #143), los
> préstamos en la base (#133), el scorer corregido (#142) y la cadena de
> días (#141). No se compara con la serie A más que como «antes/después del
> instrumento».

| Fecha | Run (id8) | Turnos/Días | Agentes | Score | Caquetío | Estado / hito |
|---|---|---|---|---|---|---|
| 09-17 | `b06f57ea` | 6 / 1 | **63** | 7.5 | 100% | **Día 1 de la serie B, desde cero** (motor `7ab8c2b` limpio, semilla 11, `--reflexion`). Pre-carga: **63 de 63 vectores-semilla distintos** (la serie A: 2). Por eso la acumulada arranca en 0,803 donde la serie A arrancaba en 0,199: ahora hay de dónde converger. Ventana 0,660, emergente 0,944. 18 acuñaciones (9 adoptadas, 11 formas); la competencia por «las cuentas brillantes» —que es un concepto que el motor pone a nombrar, no una necesidad espontánea— se fija en `kari-uro-bana` el día 1 (en la serie A fue `kali-iro-pabu`, mismo turno 5). La forma acuñada ya queda en boca del acuñador (0 de 18 perdidas; en la serie A, 29 de 40). Préstamos: 0, y ya sin falsos. El mundo: cerro en 31 de 72, viento 19, sitio 18, y **el venado nombrado por primera vez (2 respuestas)**. Reflexión del Director escrita por el motor, sin residuos de la era 1. ⚠️ **Deuda del día, y no es menor**: el evento semilla de `estado_inicial_test()` («Shaboro salió de su choza… Buio-sha lo vio») abre todo run nuevo, dura tres turnos, se guarda crudo en `turns.event_description` y **llegó a los agentes**: 23 de 72 respuestas dicen «Shaboro» y 16 «Buio-sha» — el traductor de #143 cubre la puerta del Director (que dijo «Sawaka») pero no la vía por la que el evento entra al prompt del agente. Este día 1 de la serie B queda contaminado por la era 1 en un tercio de sus respuestas; agente con Opus en curso (estado inicial propio de Paraguaná + cerrar esa vía), y toca decidir si el día 1 de la serie B se repite limpio antes de encadenar el 2 |
| 09-17 | `3973d317` | 6 / 1 | **63** | 7.6 | 100% | **Día 1 de la serie B, limpio — el que cuenta** (motor `340f4fd`, semilla 21, `--reflexion --serie era2-b`; el `b06f57ea` queda como prueba contaminada). Revisión previa sin API: ensayo en seco de los 78 prompts (0 residuos de la era 1, 63 de 63 semillas, `[Tu tierra]` ≤ 320 en 72/72, `[Voces de fuera]` sólo tier 1, Director de Paraguaná con `[El mundo]` 6/6) y el hallazgo de la competencia repetida (punto 5 del cambio de instrumento, #149). Medido en la base: 72 respuestas, 59 agentes (24 de tier 1, 42 de tier 2, 6 de tier 3), **0 «Shaboro», 0 «Buio-sha», 0 «Guaycarí», 0 «Curiana»**; score 7,64. Koiné: acumulada 0,7955, ventana 0,678, emergente 0,906 (59 agentes). 18 acuñaciones (12 adoptadas, 0 perdidas en boca del acuñador); la competencia por las cuentas se fija en `kashi-kasuta-iro` de 4 variantes (turno 5: 9 de 12 hablan de cuentas; turno 6: 4). Diccionario emergente: `biro-ana` «salina» (22,2) por encima de la forma de la competencia (17,1), `duna-rua-bana` «manantial alto» (14,6): **la sal es el tema del día** (44 de 72 respuestas dicen salina/biro-ana; 53 nombran la sal) — el mundo de Guaranao (sal y ensenada, Arcaya p. 22) sí llega. Cerro en 34 de 72, viento en 33, venado en 0. Por nodo (`analizar_nodos.py`): brecha intra/entre 0,015 (ventana) y 0,006 (emergente); de 54 formas clasificables 31 cruzaron de nodo (mediana 1 turno), 13 nacieron en los dos a la vez, 10 no cruzaron — **el motor no tiene frontera entre nodos**: pregunta de diseño abierta (agente proponiendo). Préstamos: 7 registrados y los 7 son hispanismos de origen indígena usados como castellano (`casabe` ×2, `yuca` ×3, `maíz`, `ture`; agente midiendo toda la base). El Director cerró con «las canoas volverán al Golfete» (2 respuestas también): canon de Tacuato (P1), no la costa oeste de los nodos (agente proponiendo). Estado en disco: día 2, `referentes_introducidos = [cuentas_vidrio]` → el día 2 recibirá el cometa |

**Lo que piensa el Director del día 1 limpio de la serie B** (`3973d317`, escrito por el motor):

> El viento del este sostuvo todo: la sal brilló en los biros, el casabe se
> coció parejo, y la gente trabajó sin pelear. La tensión que ardía a media
> mañana —cuando Isiro hablaba de lo que falta y Saruro clavaba el coa en
> tierra seca— se disolvió cuando cayeron los jachos y Harifuche levantó el
> ritmo del budare. Lo que cambió fue el hambre: dejó de ser lo único que se
> decía en voz baja para convertirse en trabajo, en manos que rallan,
> exprimen, tuestan. La palabra que prendió fue **kashi-kasuta-iro**, la
> cuenta brillante —salió de muchas bocas hoy, de Manaure y Buriche y otros,
> cada uno viendo algo distinto en esa cosa que brilla y pesa—, y eso sucede
> cuando la gente toca lo mismo y busca el nombre juntos. Mañana el juri
> seguirá fuerte desde el este, las canoas volverán al Golfete, y habrá que
> ver si la sal y el casabe sostienen la calma o si la escasez vuelve a
> abrir la boca.

Lectura del escriba: sin residuos de la era 1; la tensión que cuenta
(Isiro/Saruro, el hambre → el trabajo) es la de los agentes de hoy; «la
palabra que prendió» es la del evento de nombramiento (el motor la puso a
nombrar), y lo dice bien: «la gente toca lo mismo y busca el nombre juntos».
«Las canoas volverán al Golfete» es canon de Paraguaná (Tacuato, P1 del
clima), pero no la costa de estos dos nodos, que miran al oeste — deuda
abierta abajo.

**Lo que pensó el Director del día 1 contaminado** (`b06f57ea`, no cuenta):

> El juri no paró en toda la jornada y la pesca llegó abundante: eso cambió
> el peso del hambre en la plaza. Sawaka se fue al amanecer con algo que no
> dijo, y aunque Hayo esperó, nadie volvió a mencionarlo cuando los cestos
> llegaron llenos. La palabra que prendió fue **mira-ni** en boca de Karebe
> mientras contaba los trueques —mirar y contar son lo mismo aquí, y él
> necesitaba ese verbo para nombrar lo que hace con las manos abiertas de
> Birokoa y Tauta. El biro sigue bajo pero nadie reclama: con carne seca y
> cerámica que entra de fuera, la lengua descansa. Mañana sabremos si Sawaka
> regresa o si lo que vio en la oscuridad del turno 1 aún habla en algún
> rincón sin luz.

### Era 2 · serie A — pruebas del motor (2026-09-14 → 16)

> ⚠️ **Cambio de instrumento (2026-09-16 → 09-18), declarado.** Ocho cambios,
> en el orden en que se decidieron. Los dos primeros son de
> `score_linguistico()` y pasaron DESPUÉS de los runs de abajo, así que los del
> 09-14 no son estrictamente comparables con los que vengan:
> 1. **El filtro de nombres se arregló.** El del 09-14 comparaba en minúsculas
>    y descartaba del conteo **52 voces del canon** homógrafas de un nombre del
>    elenco (`buko`, `hayo`, `mene`, `saruro`, `jachos`, `karebe`…), todas
>    visibles en el prompt: los runs de abajo midieron sin ellas, en el score y
>    en la koiné. Desde el 09-16 la mayúscula decide: `Karebe` es la persona,
>    `karebe` el cucharón.
> 2. **El préstamo de esfera dejó de penalizar** (decisión de Miguel del 09-15):
>    las voces de `ESFERA_DE_CONTACTO` —taíno, kalinago, paraujano,
>    caribe-continental, jirajaroide— salen en `prestamos_de_esfera` y no
>    restan; y el tier 1 recibe un bloque `[Voces de fuera]` de tres voces. La
>    fuga a wayuu/lokono/achagua sigue restando igual.
>
> 3. **El scorer deja de confundir castellano corriente, glotónimo y raíz
>    partida con préstamo o fuga** (cierre del día 2, aplicado la noche del
>    16, después del día 3 `0193873d`). Medido sobre las 144 respuestas de
>    los días 1-2: 9 de los 11 «préstamos/fugas» eran falsos (`cacique`,
>    `taita`, `dia`, `lokono` como glotónimo, `juri-ima`/`lawari-ima`/`maa-to`
>    partidos por el tokenizador). Arreglo: `CASTELLANO_CORRIENTE` neutro
>    (como los homógrafos de Zavala, no stopword), la raíz decide la familia
>    de un token con afijos (`_familia_de_token`: `juri-ima` es caquetío;
>    `sucu-bana`, `bucu-ana`, `iri-ka` —raíz lokono con afijo caquetío— dejan
>    de pasar por caquetío), y los glotónimos se resuelven por contexto.
>    Efecto: canon puro Δ 0,00; las 144 respuestas 7,350 → 7,347; las 2.371 de
>    toda la base 6,9728 → 6,9722 (22 cambian, |Δ| máx 0,40). Como
>    `_familia_de_token` es también `word_uses.source_language`, los runs
>    posteriores clasifican tres formas de raíz lokono como fuga donde los
>    del 16 las contaban como caquetío. `[Voces de fuera]`: 54 → 50 voces
>    posibles y 13 glosas que antes no enseñaban nada ahora sí.
>
> 4. **La pre-carga de idiolectos vuelve a existir en la era 2** (cierre del
>    día 3, aplicado la noche del 16, DESPUÉS de los tres días de la cadena):
>    `formas_seed_de()` y `emocionar_de()` resuelven el nombre por
>    `ALIAS_ERA1`, y los 52 agentes sin semilla escrita la derivan de su ficha
>    (voces caquetías de su `system_prompt`/oficio), del campo semántico de su
>    oficio (`categorias_relevantes` aplicada al oficio y a la glosa de cada
>    voz) y de su emocionar, con sorteo determinista (`blake2b` de la semilla
>    del run y el nombre). Medido: vectores-semilla distintos en la era 2
>    **2 de 63 → 63 de 63** (origen: escrita 1, por alias 10, derivada 52); la
>    era 1 byte a byte igual (21 de 60). Y la forma acuñada queda registrada
>    en boca de su acuñador (`coined_words`). **Los tres días de la cadena
>    `c6837386 → 89fc1744 → 0193873d` corrieron con 62 de 63 agentes
>    arrancando iguales**: `--continuar` no recupera una pre-carga que nunca
>    hubo (el motor ahora lo avisa con `agentes_sin_precarga`); la única
>    salida es re-correr desde el día 1. `score` y `pct_*` no cambian.
>
> 5. **La competencia léxica deja de repetir el mismo referente cada día**
>    (revisión previa al día 1 limpio de la serie B, 2026-09-17). `auto_mode`
>    empezaba `REFERENTES_NOVEDOSOS` de cero en cada run y un día de seis
>    turnos sólo llega al primero: en la serie A el turno 5 de CADA día
>    volvió a poner «las cuentas brillantes» delante (respuestas sobre cuentas
>    en el turno 5: 10 de 12 el día 2, 10 de 12 el día 3, y 4 de 12 el día 1),
>    y `kuri-bana-iro-pabu` se re-acuñó los días 2 y 3. Lo que se leyó como
>    «la koiné sobrevivió la noche» era en parte el instrumento re-enseñando
>    el referente. Desde ahora el estado guarda `referentes_introducidos` y
>    `--continuar` sigue la secuencia (día 2: el cometa; día 3: el eclipse).
>    En la serie B, que una forma fijada el día 1 aparezca el día 2 sin que
>    nadie vuelva a mostrar la cosa es señal de verdad.
>
> 6. **Las voces de la esfera dejan de enseñarse con grafía castellana**
>    («la etiqueta manda», decisión de Miguel del 2026-09-18). El día
>    anterior se había decidido lo contrario de lo que parecía: el producto
>    de la esfera ES la esfera, así que casabe, yuca o maíz siguen contando
>    como préstamo. Lo que cambia es la GRAFÍA con que circulan. Si el
>    lexicón tiene la forma indígena atestiguada, es la que el tier 1 ve y la
>    que se registra (`FORMA_DE_LA_ESFERA`: casabe→cazabi, maíz→maisi,
>    cacique→cacike, bohío→bohio); si no la tiene, la voz **no se enseña**
>    hasta que Miguel fusione la forma propuesta
>    (`6-fusion/descastellanizar_esfera_2026-09-18.yaml`). Medido: de las 133
>    voces de la esfera, 24 llevan marca de grafía castellana (4 con gemela,
>    6 esperando a Miguel, 14 que se quedan porque la grafía ES la
>    transcripción de la fuente). **`[Voces de fuera]` pasa de 50 candidatas
>    a 43**, y de 13 formas con marca castellana a 5, todas declaradas. En la
>    base, `word` guarda la forma de la esfera y `forma_dicha` lo que el
>    agente escribió (migración `20260918000000`); los runs viejos NO se
>    reescriben y `analizar_runs.py --prestamos` normaliza al leer (5 de sus
>    11 filas). **El scorer no se movió**: `prestamos_de_esfera` sigue
>    devolviendo la clave castellana y 0 de 8 frases de control cambian en
>    `score`, `densidad`, `pct_*` ni en ninguna de las diez claves medidas.
>
>    **Desde qué run aplica**: cambia lo que el TIER 1 VE, así que no entra a
>    mitad de cadena. **Aplica desde la serie C, que no ha empezado**; la
>    serie B (run `3973d317` y lo que continúe de él) queda del lado de
>    antes, como ya quedó con `golfete_frase_tarde`. Los runs de la serie A y
>    B no son comparables con los de la C en la difusión de préstamos.
>
> 7. **La disputa sobrevive la noche, y el Capubana junta ÁMBITOS y no sólo
>    cuerpos** (los dos defectos que midió el día 1 de la serie C, run
>    `b7bc51dc`; ver `analisis/serie_c_dia1_b7bc51dc.md`). **La serie C se
>    repite desde el día 1 con esto**: el `b7bc51dc` queda como la medición que
>    los encontró, no como el día 1 de la serie.
>
>    - **`CompetenciaLexica` se persiste** (`curiana_koine.guardar_koine` /
>      `cargar_koine`, dentro de `curiana_koine.json`: referentes abiertos y
>      fijados, variantes con su soporte, el ámbito de cada proponente y el
>      umbral del run). Hasta ahora `auto_mode` creaba una nueva en cada run
>      —y un run de la era 2 es UN día— mientras `referentes_introducidos` (que
>      sí se heredaba) impedía volver a presentar el referente: **ninguna
>      competencia podía durar más de un día**, y por competencia no podía
>      fijarse jamás una entrada de koiné en una cadena de runs de un día. La
>      disputa de «las cuentas» del `b7bc51dc` lo enseña: 16 variantes en 7
>      ámbitos, `kali-uco-aima` 3,65 sólo en Tacuato, `ucibo-kali-duruco` 3,45 y
>      `kali-boro` 2,80 sólo en Carirubana, y el líder con el 12,2 % contra un
>      umbral del 55 % — muerta al amanecer. Con `--continuar` la competencia se
>      recupera y la fijación se sigue evaluando al cerrar cada día; sin
>      `--continuar` empieza vacía, como siempre. Un `curiana_koine.json` de la
>      serie B no trae la llave y carga con la competencia vacía.
>    - **El día de Capubana deja de ser un lugar más.** Con `--capubana-cada 3`,
>      el día 3 `ambito_de` devolvía `"Capubana"` para los 63 y eso es UN LUGAR,
>      cuyo léxico era el de sus dos ocupantes del día 1 (Sawaka y Hayo, 71
>      formas): V2 vacía y las tres rivales de las cuentas a 0 — exactamente lo
>      contrario de lo que dicen el diseño §4 y la decisión p7. Ahora hay dos
>      puertas y dicen cosas distintas: `ambito_de` = **dónde ESTÁ** (el
>      registro, `[Aquí estás]`, `presencias`, el campo — ese día, `"Capubana"`,
>      para que `adoptados_en_dos_ambitos` y el mapa lo vean) y
>      `ambito_visible_de` = **qué VE** (las cuatro vías y `[Lo que se dijo
>      aquí]` — ese día, `None`, que es lo que las cuatro ya entienden como «sin
>      filtro»: la unión de todos los ámbitos, sin un parámetro nuevo en
>      `LexicoComunitario`, `CampoLexico` ni `CompetenciaLexica`). Ensayo sin
>      API de 18 turnos (días 2-3-4, `tests/test_escena_oir.py`): el día 3
>      V1/V2/V3 traen **exactamente lo mismo** que el mismo run sin escena, y el
>      día 4 vuelve el filtro por lugar.
>
>    **Lo que NO se aplicó ese día, y por qué**: el día 1 registró dos
>    «acuñaciones» que no lo son —`kali-bana`, que es el ejemplo literal de
>    `_IDENTIDAD_LINGUISTICA` y va en el system prompt de los 63 todos los
>    turnos, y `warawara`, que está en `VOCABULARIO_BASE`— y `kali-bana` salió
>    además como «adoptada en dos ámbitos». Rechazarlas en
>    `LexicoComunitario.registrar_neologismo` con la lista que el motor ya tiene
>    (`_FORMAS_EXCLUIDAS`, 5.898 formas) **mueve el instrumento**: re-puntuadas
>    las 72 respuestas del `b7bc51dc` con y sin el filtro (el replay reproduce
>    la base en 72 de 72), `neologisms_proposed` no cambia en ninguna pero
>    `score` cambia en **4** —Buriche d1t4 8,7 → 8,5, Chuchubi d1t5 8,0 → 7,6,
>    Karebe d1t6 5,4 → 5,3, Apoaure d1t6 5,5 → 5,4— porque `kali-bana` se
>    oficializa durante el día y una forma adoptada entra en `palabras_activas`,
>    que es justo lo que el scorer reconoce. Quedó medido en
>    `6-fusion/medicion_formas_de_plantilla_2026-09-18.yaml`, para que decidiera
>    Miguel — **y lo decidió al día siguiente: es el punto 8**.
>
> 8. **Lo que la plantilla ENSEÑA deja de poder registrarse como acuñación**
>    («Dale pues con A», decisión de Miguel del 2026-09-18, opción A del issue
>    `6-fusion/issues-pendientes/publicados/formas-de-plantilla-en-la-registracion-2026-09-18.md`,
>    entrada `formas_de_plantilla` de `6-fusion/decisiones_tanda_2026-09-17.yaml`).
>    Es **el único de
>    los ocho que mueve `score`**, y por eso se declara como corte: no se aplica
>    porque no mueva nada, se aplica porque el corte está declarado.
>
>    - **Qué cambia.** Una forma que está en `VOCABULARIO_BASE` o que es un
>      ejemplo de una plantilla del prompt **no se registra** como neologismo:
>      no entra en competencia (`CompetenciaLexica.proponer`), no puede
>      adoptarse, no pasa a `palabras_activas()` y no sale en el diccionario de
>      cierre. El rechazo **se cuenta y se dice** al cerrar el run («N
>      acuñaciones rechazadas por estar en el prompt: …»), no se silencia.
>    - **Una puerta y no dos.** La lista se construye desde las propias
>      plantillas —nunca a mano— y vive en `curiana_lexicon.FORMAS_DE_PLANTILLA`,
>      que importan el orquestador (`_FORMAS_EXCLUIDAS` es ella misma) y
>      `analizar_nodos.formas_excluidas()`. Antes eran dos cosas: la del
>      análisis existía y la del registro no, así que `kali-bana` se descontaba
>      de la métrica emergente **y a la vez** se registraba, se adoptaba y
>      competía. Mira además el **refuerzo** y el **rescate**, que también
>      enseñan formas y quedaban fuera: la puerta pasa de 5.898 a **5.945**
>      formas y entran `ma-arua`, `wa-duna`, `wana-ni` y `cati`. No mira los
>      bloques que le devuelven al agente lo que la comunidad dijo (V1, V2, V3,
>      `[Lo que se dijo aquí]`, `[Tu manera de hablar]`) — ésos son el mecanismo
>      que se mide — ni los que no enseñan ninguna forma (`[Tu tierra]`: 293
>      formas, 0 caquetías fuera de la puerta).
>    - **Medido sobre las 144 respuestas de los dos días** (`76ecf45c` y
>      `96b22194`, encadenados como los corrió `--continuar`;
>      `6-fusion/medicion_formas_de_plantilla_corte_2026-09-18.yaml`). Control:
>      el replay SIN la puerta reproduce la base en **144 de 144** y reproduce
>      la competencia que anotó esta bitácora (`kali-bana` 15,85 ·
>      `kali-iro-bana` 3,1 · `brilu-uco` 2,9). Con la puerta:
>      `neologisms_proposed` cambia en **0**, **`score` en 8 de 144** (|Δ| máx
>      0,30), `palabras_caquetias` en 14. Rechaza **2**: `kali-bana` (Chirwa,
>      d1t5) y `naa-ni` (Apoaure, d2t6), que es el ejemplo del bloque de
>      morfología. Neologismos 66 → 64, adoptados 11 → 9, y **adoptadas en dos
>      ámbitos `['siwato-ni', 'kali-bana', 'naa-ni']` → `['siwato-ni']`**: dos
>      de las tres eran copia del prompt, incluida la que el día 2 se celebró
>      como «la primera que cruza de verdad entre nodos». Sin `kali-bana`, «las
>      cuentas» las lidera **`kali-iro-bana` (3,1)** sobre `brilu-uco` (2,9) y
>      `kara-ucibo` (2,4), y ninguna se acerca al umbral del 55 %. Y el
>      diccionario emergente pierde su cabeza: **`wana-ni` (50,0)**, que es la
>      línea que el refuerzo escribe.
>    - **El scorer no se tocó.** `score_linguistico()`, `pct_*` y
>      `capas_de_score` son los mismos, y `extraer_neologismos_del_texto()`
>      tampoco cambia (por eso `neologisms_proposed` no se mueve). `score` se
>      mueve porque una forma adoptada entra en `palabras_activas()` y
>      rechazarla se la quita a `palabras_caquetias` en las respuestas
>      posteriores que la dicen. `curiana_observer` tampoco se tocó: la puerta
>      está dentro de `registrar_neologismo`, que es a quien él llama.
>
>    **Desde qué run aplica**: desde el próximo. **La serie C se re-corre entera
>    desde el día 1**; `76ecf45c` y `96b22194` quedan como los dos días con el
>    prompt contaminando la competencia, no como los días 1 y 2 de la serie. Los
>    runs ya corridos no se reescriben.
>
> Ninguno de los ocho toca `capas_de_score`.

> ⚠️ **Dos artefactos del instrumento descubiertos al cerrar el día 3
> (análisis por nodo, `analizar_nodos.py`, 2026-09-16), que afectan a los
> tres días de la cadena `c6837386 → 89fc1744 → 0193873d`:**
> 1. **La pre-carga de idiolectos se perdió con los nombres nuevos.**
>    `FORMAS_SEED` y `EMOCIONAR_SEED` (`curiana_koine.py`) están indexados por
>    nombres de la era 1; la campaña de antropónimos renombró a 60 de 63 y el
>    orquestador siembra con el nombre nuevo sin pasar por `ALIAS_ERA1`.
>    Medido: **1 de 63** con semilla propia (Manaure), 10 la tendrían vía
>    alias, 52 no tienen ninguna. `DISENO_KOINE.md` §4 llama a esa pre-carga
>    precondición: «sin esta pre-carga, todos arrancan iguales y convergencia
>    no significa nada». **El veredicto CONVERGE de la cadena del 16 no es
>    evidencia hasta arreglar la siembra y volver a correr los tres días.**
> 2. **La forma acuñada no queda en `word_uses` en boca de quien la acuña**:
>    al acuñar no está en el léxico activo y `palabras_caquetias` no la
>    reconoce; 29 de 40 acuñaciones (72,5 %) sólo aparecen usadas por el
>    adoptante, que puede ser del otro nodo — y lo fue. Invierte las rutas de
>    contagio que se lean de `word_uses` (la tabla `neologisms` sí guarda al
>    acuñador).
>
> Y la lectura por nodo, normalizada por hablantes posibles (GUARANAO 39,
> AMUAY 24): `kali-iro-pabu` la acuñaron cinco agentes de los DOS nodos en el
> mismo turno (razón 1,01); `tüshi-juri` es compartida (1,41), no inclinada;
> `kuri-bana-iro-pabu` inclinada a GUARANAO (2,15) y `biro-kali` (2,62, acuñada
> en AMUAY). Distancia intra-nodo vs entre nodos: brecha del 1-3 % que el día
> 3 se invierte en la emergente. **No hay evidencia de koiné entre nodos, ni
> de diglosia: los dos nodos nunca estuvieron separados** — con la reserva de
> que el instrumento medía sin su media pieza. Detalle en
> `analisis/ANALISIS_NODOS_ERA2_2026-09-16.md`.

| Fecha | Run (id8) | Turnos/Días | Agentes | Score | Caquetío | Estado / hito |
|---|---|---|---|---|---|---|
| 09-16 | `0193873d` | 6 / 1 (día 3) | **63** | 7.6 | 100% | **Día 3 con mundo, encadenado desde `89fc1744`** (semilla 3, motor `1be0d52` limpio: eventos de la era 2, Director con mundo, `loanword_uses`, `--reflexion`). Sin encadenar el 4: Miguel cierra aquí. **La koiné se consolida**: `kali-iro-pabu` 20 usos, `tüshi-juri` 19, `sima-maa` 19, `nii-bana` 18, `kuri-bana-iro-pabu` 17, `sima-pabu` 14; sólo 4 acuñaciones nuevas (26 y 10 los días anteriores) — el léxico se asienta. ⭐ **Por nodo** (hablantes distintos en tres días; GUARANAO tiene 39 posibles y AMUAY 24): `kali-iro-pabu` 18 GUA / 11 AMU (compartida), `tüshi-juri` 16 / 7, `kuri-bana-iro-pabu` 21 / 6 (inclinada a GUARANAO), y la variante nueva del día 3 `kuri-sima-pabu` 1 / 3 (Kasebo y Saruro de Caseto, Kiwakoa de Carirubana: inclinada a AMUAY). Distancias por la cadena: ventana 0,604 → 0,467 → 0,375; emergente 0,900 → 0,820 → 0,725 — tres días bajando; el motor sigue diciendo «datos insuficientes» (agente en curso). Préstamos: la tabla nueva guarda 2 filas (`bohío` Chirwa T3, `cacique` Uria T2), las mismas dos que da la re-puntuación — funciona, y las dos son castellano corriente: **tres días y ningún préstamo real** en el tier 1. El mundo: viento en 51 de 72, cerro en 49, sitio en 25, jachos en 4; manglar y caimán en Guaranao: 0 (la corrección funciona). Residuos de la era 1 que quedan: el Director dijo «Caquetíos y Guaycarí» en el cierre 6 y en la reflexión, y un agente «Biro-ko» — la reflexión del día 2 que el escriba le inyectó traía «los Guaycarí» (agente en curso); y la cabecera de la reflexión copia «Día 4, Turno 1» |
| 09-16 | `06482296` | 2 / — (día 3, **interrumpido**) | 12 resp. | — | — | Día 3 lanzado a las 19:36 con todo lo del cierre del día 1 ya en `main` (préstamos a la base, eventos de la era 2, Director con mundo, `--reflexion`) y **detenido en el turno 1 a petición de Miguel** («no lances aún el día 3; cerremos el día 2 y listo»). No cuenta: 2 turnos, 12 respuestas, sin cerrar. El estado en disco quedó al final del día 2 (día 3, turno 1, `run_anterior` 89fc1744): el próximo día 3 arranca de ahí con `--continuar` |
| 09-16 | `89fc1744` | 6 / 1 (día 2) | **63** | 7.6 | 100% | **Día 2 con mundo, encadenado con `--continuar`** desde `c6837386` (semilla 2, motor `cb389991`): los seis turnos en el Tiempo de Viento. La koiné de ayer sobrevivió a la noche: `kali-iro-pabu` 14 usos hoy y una variante larga, `kuri-bana-iro-pabu`, le disputa el concepto (20 usos, «en disputa»); `kua-siwato` 15, `nii-bana` 9, `biro-kali` 6. `sima` «cerro» se extiende (`sima-pabu` «cerro ardiente», adoptada). ⭐ **Primera palabra del tiempo**: `tüshi-juri` «viento frío del este» (Hayo, adoptada) — el período empieza a nombrarse solo (decisión p2). El viento/`juri` aparece en 57 de 72 respuestas (`juri` 29 usos), el cerro en 45, el sitio en 15. Distancias entre días: ventana 0,604 → 0,467, emergente 0,900 → 0,820 (el veredicto del motor dice «datos insuficientes» porque no sigue la cadena `continuado_desde`: deuda conocida). Préstamos de esfera reales: 0 (dos falsos: `cacique`, `taita`, castellano leído como taíno). ⚠️ Deudas que delata el Director: los eventos de `curiana_state.py` son de la era 1 (nombran 29 veces a agentes viejos y a «los Guaycarí», foráneos que la era 2 dejó fuera) y el Director no recibe el mundo (dice «la Curiana», inventa un ceibo: ecologia-032) |
| 09-16 | `c6837386` | 6 / 1 | **63** | 7.5 | 100% | **Primer día de la era 2 CON MUNDO** (motor `c69e042` limpio, tras el merge de #130; `--perfil era2 --semilla 1`): el año de tres períodos (los seis turnos en el Tiempo de Viento, los seis momentos), `[Tu tierra]` por sitio y `[Voces de fuera]` en tier 1. Medido: el sitio se nombra en 22 de 72 respuestas, el cerro en 37, el viento/`juri` en 12, los jachos en 7, el jagüey en 4; 26 acuñaciones (19 adoptadas), tres con `sima` «cerro» (wana-sima, amana-sima, sima-naa) y una competencia de once agentes por nombrar «las cuentas duras que brillan como el sol» que trae la canoa de las islas, fijada en `kali-iro-pabu`; ninguna acuñación del período ni del venado. **Préstamos de esfera: 0** en tier 1 (re-puntuado sobre las 72 respuestas), fugas 7. Emergente D1 0,90. ⚠️ No comparable con los del 14 (instrumento cambiado el 16) y **deuda de instrumento**: `word_uses` sólo guarda `palabras_caquetias`, un préstamo usado no llegaría a la base — se mide re-puntuando `response_text` hasta que se guarde aparte |
| 09-14 | `aafc5c32` | 6 / 1 | **63** | 7.7 | 100% | **Primer día con el elenco de la era 2** (`--elenco era2`, perfil `era2`, mundo PARAGUANÁ, motor `19b0e16` limpio): hablaron los 63, tier 3 incluidos; prueba de tubería, no evidencia |
| 09-14 | `81907ae1` | 6 / 1 (día 2) | 47 | 7.5 | 100% | **Día 2, encadenado con `--continuar`** desde `fec49195`: memoria, lexicón y koiné heredados; emergente 0,8124 → 0,7199 entre días |

### 2026-09-16 · Lo que piensa el Director de los días 1 y 2

Miguel pidió saber «qué es lo que el director piensa del día 1». El Director
del motor sólo escribía cierres por turno; desde #138 existe
`reflexion_del_dia()` (`curiana_director.py`, flag `--reflexion`, una llamada
al cerrar cada día). Las dos reflexiones de abajo se generaron **después** de
los runs, con el mismo código y los mismos insumos que tendría en el flujo
(los seis cierres del día y el reporte medido del observer, entero), y quedan
en `curiana_director.json` (gitignored) y aquí. En una primera pasada, con el
reporte recortado a 3.500 caracteres por el escriba, el Director dijo del día
2 que «ninguna palabra nueva prendió»: la adopción de `tüshi-juri` había
quedado fuera del recorte. Se regeneró con el reporte entero; es lo que sigue.

**Día 1 (`c6837386`):**

> El nieto de Simaure ardía ayer, arde más hoy, y eso cambió todo: la sal
> quedó en segundo plano. Vimos a Manaure levantar esa piedra pequeña que
> brilla —**kali-iro-pabu**— hacia el cielo oscuro, y nadie necesitó que
> nadie explicara qué estaba pasando; el gesto viajó por toda la ranchería
> más rápido que cualquier palabra. Lo que prendió no fue una palabra nueva,
> sino una forma de nombrar lo que ya todos veían: Tauta, Talata, Ucibo,
> cada uno dijo lo que vio en esa piedra brillante, y aunque usaron distintos
> sonidos, la comunidad entera entendió que estaban hablando de lo mismo.
> Kadushi llegó con noticias de afuera —enfermedad en Aruba, barcos
> españoles al norte— y eso bajó la tensión un poco, porque la gente
> necesitaba saber que el mundo sigue existiendo fuera de la fiebre. Mañana
> tenemos que ver si Simaure busca al piache, si el pozo sigue bajando, y qué
> hace la comunidad cuando la medicina del alma —**barsure-duni**— es lo que
> más falta.

**Día 2 (`89fc1744`):**

> El alisio no aflojó y los peces tampoco vinieron. Lo que cambió fue el
> miedo —pasó de sospecha a ruido en la oscuridad, y eso dividió las
> explicaciones: los Guaycarí culpan el calor, los Caquetíos el rezo
> faltante. La palabra que prendió fue **tüshi-juri**, viento frío del este,
> acuñada por Hayo cuando el polvo salino le quemaba los ojos —otros la
> repitieron porque nombra lo que todos sienten. Queda abierto si mañana al
> amanecer Chiriware tendrá que repartir hombres entre la defensa del
> perímetro y la pesca, porque nadie duerme bien cuando el viento trae ruido
> de remos. Y queda sin resolver si el hambre va a romper antes que la sal se
> venda.

**Día 3 (`0193873d`)** — ésta la escribió el motor al cerrar el día, con
`--reflexion`, no el escriba:

> El alisio no cedió pero la red mojada tocó agua esta vez, y eso cambió el
> peso del silencio: ya no es miedo puro sino trabajo compartido, aunque los
> vientres sigan vacíos. La palabra que prendió hoy fue **tüshi-juri** de
> nuevo —Manaure la levantó anoche como aviso, no como culpa, y eso abrió
> grieta en la división: Caquetíos y Guaycarí pescaron juntos bajo los jachos
> porque el hambre que nombra el viento no distingue de qué lado duermes. Lo
> que quedó sin resolver es si la pesca de esta noche trae pescado o sólo
> trae manos mojadas y más hambre mañana, y si Manaure puede sostener el rezo
> compartido cuando la tensión vuelva a subir. La sal sigue blanca sin usar
> mientras el mercader no regresa.

(«Caquetíos y Guaycarí» le llegó por la reflexión del día 2, que el escriba
había puesto en `notas_orquestador` para imitar el flujo: el residuo se
propaga por ahí. Deuda del cierre del día 3, ya con agente.)

Lo que las dos delatan, y ya está corregido en `main` para el día 3: «los
Guaycarí» y «Chiriware» vienen de los eventos de la era 1 (#138 los tradujo;
Chiriware es linaje en la era 2, no persona), y «barcos españoles al norte»
es un anacronismo del cierre del turno 6 del día 1 —el Director de entonces
no tenía mundo ni restricciones—, que el Director con mundo ya no debería
repetir. Deuda de instrumento menor: la cabecera que el modelo pone a la
reflexión copia «Día N+1, Turno 1» del estado al cerrar; el prompt debería
fijar el día reflexionado.

**Deudas del día 2, para su cierre** (no despachadas todavía): el veredicto
de la koiné no sigue la cadena `continuado_desde` («datos insuficientes» con
dos días encadenados y las distancias bajando); el scorer lee `cacique` y
`taita` como préstamo taíno y «dia» como fuga (castellano corriente que
coincide con claves de comparanda); tres casi-autoglosas en `[Voces de fuera]`
(cazabi = cazabe, bohio = bohío, guanin = guanín).

### 2026-09-14 · Run `aafc5c32` — el elenco de la era 2 habla por primera vez

**Comando:** `python curiana_orchestrator_v2.py --elenco era2 --auto 6
--turnos-por-dia 6 --agentes-por-turno 12 --roster todos --perfil era2
--semilla 20260916 --silencioso` (10 min 01 s). La config del run dice
`elenco: era2`, `mundo: PARAGUANÁ`, `agentes_n: 63`, `roster_n: 63`, perfil
`era2` (sin la capa hipotética), motor `19b0e16` limpio.

**Qué midió** (Supabase local):
- **72 respuestas de 63 agentes: hablaron todos**, los 10 tier 3 incluidos
  (con las reglas breves y su muestra de 20). Ningún evento del director cayó
  en los seis turnos, así que la rotación sola cubrió el elenco entero.
- Score medio **7,73** (7,55 el día 1 de la era 1 en este motor). Encabezan
  el ranking Sha-korie, Piri, Karapa-sha, Nubiri-sha, Tawaka, Biro-ko,
  Itana-sha y Waimo-ko: dos nuevas, tres reancladas y dos promovidas de fondo.
- **El mundo cambió de nombre en boca de los agentes:** Moruy 4 respuestas,
  Carirubana 4, Tacuato 3, Amuay 3, Caseto 2, Capubana 2, Guaranao 1;
  «Golfete» 0 y «Curiana» 3 (residuo de textos de la era 1 que todavía
  llegan al prompt).
- Afijos: `-aima` en 18, `-iro` en 13, `-bacoa` en 12. La copia de la frase
  modelo baja a **9 de 72 (12,5 %)**.
- **14 neologismos adoptados y 13 propuestos.** El diccionario emergente lo
  encabezan *tüshi-bana*, *sima-nii*, *chakamba-barsure* y *mütsia-biri-bana*.
- Emergente del día 0,8394 (un solo día: sin veredicto).

**Lo que este run no dice:** nada sobre la koiné entre nodos. Es la prueba de
que el elenco generado, el conmutador, el bloque [Tu gente] y el estímulo con
el sitio funcionan de punta a punta. Los nombres del elenco están en revisión
(30 de 63 raíces no son caquetías; ver la campaña de antropónimos), así que el
primer run citable de la era 2 va después de renombrar.
| 09-14 | `fec49195` | 6 / 1 | 48 | 7.6 | 100% | **Día 1 de la era 2 en el motor**: 6 turnos por día, 12 por turno, roster `todos` (52), semilla 20260914, motor `db7d053` limpio |

### 2026-09-14 · Run `81907ae1` — el día 2, encadenado

**Comando:** `python curiana_orchestrator_v2.py --auto 6 --agentes-por-turno 12
--roster todos --semilla 20260915 --perfil base --silencioso --continuar`
(9 min 16 s). La config del run dice `continuado_desde: fec49195` y
`dia_inicial: 2`; heredó del disco el estado (día 2, turno 1), la memoria, el
lexicón, el observer y la koiné (idiolectos y campo). Cerró como día 2, con 6
turnos.

**Lo que prueba el encadenado:**
- **Los agentes se acuerdan.** 43 agentes llevan la nota del día 1 y la del
  día 2 en su memoria; en Manaure la nota «D1: hablé al amanecer, mañana,
  anochecer; acuñé barsure-duna, kali-biro…» sobrevivió a sus tres turnos del
  día 2.
- **Lo acuñado el día 1 vuelve el día 2:** 13 formas adoptadas el día 1 se
  usaron 140 veces el día 2. *kali-biro-duna-iro* (el nombre de las cuentas
  brillantes, con el diminutivo atestiguado) sube de 14,3 a 49,1 de peso en
  el diccionario emergente y lo acuñan o repiten Shaboro, Nubiri-sha, Manaure
  y Bagre-ko.
- **Todos hablaron en dos días:** los 4 mudos del día 1 hablaron dos veces
  cada uno el día 2; 52 idiolectos con habla real. 72 respuestas de 47
  agentes, score medio 7,50; 9 neologismos adoptados y 4 propuestos.
- **La distancia idiolectal baja entre días:** acumulada 0,3617 → 0,3203,
  ventana 0,5386 → 0,4012, **emergente 0,8124 → 0,7199** (−11%). Es la
  primera vez que la emergente se mueve así en dos días, y la primera vez que
  se mide sobre formas que la plantilla no enseña. Dos días no son evidencia
  de koiné: son la vara de que la tubería encadenada mide.

**Lo que el instrumento no hace todavía:**
- Cada run ve un solo día y su veredicto dice «datos insuficientes»; la
  serie de dos días de arriba se armó con `koine_metrics` de los dos runs.
  `analizar_runs.py` tendría que seguir la cadena `continuado_desde`.
  → **Cerrado el 2026-09-16** con `curiana_cadena.py`: el motor imprime al
  cerrar un run continuado la serie y el veredicto de la cadena entera, y
  `analizar_runs.py --koine` (y `--prestamos`) tienen vista por cadena. El
  veredicto es el mismo criterio, extraído del orquestador. Sobre esta cadena
  (`fec49195` → `81907ae1`) dice CONVERGE por la emergente.
- No se heredan la difusión social ni las competencias abiertas: la
  competencia de «cuentas brillantes» del día 1 (`kali-biro-duna-iro` 19,4
  contra dos rivales) arrancó de cero el día 2.
- El evento del director sigue durando hasta el cambio de día: la gran
  cosecha de sal ocupó los turnos 3, 4 y 5.
| 09-14 | `db946685` | 30 / 15 | 27 | 6.9 | 100% (saturada, #69) | **H2, calibración de la tubería.** Perfil `base`, motor `cacafc4` limpio. Emergente −3,3%: no converge |

### 2026-09-14 · Run `fec49195` — el día largo con todo el elenco

**Comando:** `python curiana_orchestrator_v2.py --auto 6 --turnos-por-dia 6
--agentes-por-turno 12 --roster todos --semilla 20260914 --perfil base
--silencioso` (9 min 56 s, de `started_at` a `ended_at`).

**Qué cambió respecto a `db946685`** (todo en el commit `db7d053`, con
tests): 6 turnos por día, ventana de 12 sobre los 52 caquetíos (tier 3
incluidos, foráneos fuera), muestreo proporcional por cubo, los siete afijos
atestiguados en las plantillas, la plantilla T1 con las formas del canon,
semilla sellada, memoria del día y las formas de plantilla fuera de la
métrica emergente.

**Qué midió** (Supabase local):
- **72 respuestas de 48 agentes**; los 12 tier 3 hablaron (13 respuestas).
  Los 4 que no hablaron (Piri-sha, Wari-ko, Kunaro-bana, Bagre-ko) perdieron
  su ranura en el turno con evento, que pone primero a los que el evento
  nombra: entran en la rotación del día siguiente.
- Score medio **7,55** (6,90 en `db946685`), con respuestas de 980
  caracteres.
- **Los afijos nuevos se usan el mismo día:** `-iro` en 19 respuestas,
  `-bacoa` en 13, `-aima` en 12, `-ubana`/`-uru` en 15. Numerales: *pana* 25,
  *gudamuen* 23.
- **19 neologismos adoptados y 7 propuestos** en un día (36 y 29 en los 15
  días de `db946685`).
- **Diccionario, a igual tamaño** (las primeras 72 respuestas de `db946685`
  contra estas 72): lemas base distintos 117 → 125; atestiguadas distintas
  41 → 52; usos de atestiguadas 16% → 18% de los usos base. Mejora, pero
  chica: el top-20 sigue concentrando el 62%, y ese top-20 es el bloque fijo
  de la plantilla (pronombres, conectores, los 17 verbos). La palanca que
  queda es ese bloque, no la muestra.
- **La copia de la frase modelo subió:** «ta-barsure naba-ni» en 21 de 72
  (29%; era 17,5%). Ya no contamina la métrica, pero sigue en el prompt:
  rotar o retirar la frase modelo queda pendiente.
- **El diccionario emergente ya es emergente:** lo encabezan *siwato-bana*,
  *kali-barsure*, *barsure-duna* y *kali-biro-duna-iro* (con el diminutivo
  recién enseñado), no *taya* ni *wana-ka*.
- **Lo que dejó en disco para encadenar:** estado en el día 2, turno 1, con
  `run_anterior`; memoria con la nota del día para los 48 que hablaron
  («D1: hablé al amanecer, mañana, anochecer; acuñé barsure-duna, kali-biro,
  kali-biro-duna» en Manaure); koiné con 60 idiolectos y 310 formas de campo.

**Hallazgo del calendario:** el evento del director se limpia solo al
cambiar de día, así que la iniciación de Dare-nu y Daru (turno 3) quedó como
«situación del turno» en los turnos 4, 5 y 6. Con 2 turnos por día era una
tarde; con 6 es toda la jornada. Decidir si un evento dura un turno o un día.

### 2026-09-14 · Run `db946685` — H2, la tubería de la era auditada

**Comando:** `python curiana_orchestrator_v2.py --auto 30 --perfil base --silencioso`
(21 minutos).

**Base** (de `simulation_runs.config`):
- motor `cacafc4`, rama `feat/era2-arranque`, `motor_sucio: false`;
- lexicón de 5513 claves y corpus de 198 hechos;
- 60 agentes;
- prompt de 15657 caracteres.

**Qué verificó:**
- **La fila se cierra.** Tiene `ended_at`, 30 turnos y 15 días: el arreglo del
  exportador (#42) funciona en un run vivo.
- **La huella está incompleta.** Tiene 5 de los 6 campos del protocolo; **falta
  la semilla**. `huella_de_base()` la acepta, pero el orquestador no la pasa ni
  fija `random.seed`, y sin semilla las réplicas de H3 no se pueden repetir.
- **Los numerales nuevos entran.** Respuestas con *pana*: 59 (cuenta también
  compuestos como *biro-pana*); con *gudamuen*: 42; con *sabuenen*: 18; con
  *katarí*: 5. Con *wanee*, *piama* o *jarai*: ninguna.

**Qué midió.** Hay 154 respuestas de 27 agentes y 65 neologismos (36 adoptados
y 29 propuestos).

La distancia idiolectal por métrica:

| Métrica | Día 1 | Día 15 |
|---|---|---|
| Acumulada | 0,6112 | 0,3482 |
| Ventana | 0,4885 | 0,3443 |
| **Emergente** | **0,5068** | **0,4903** (no converge) |

- **El «diccionario koiné» mide sobre todo la plantilla.** Lo encabezan formas
  del núcleo base (*nüma*, *mara*, *kashi*, *pia*, *yama*) y de las dos frases
  modelo del prompt: *taya*, *wana-ka*, *wara*, *ta-barsure*, *naba-ni* y
  *kaa-ni*, que vienen de `_IDENTIDAD_LINGUISTICA` y del ejemplo Tier I. *taya*
  sale en las 154 respuestas y *wana-ka* en 121.
- **La copia es un piso constante, no convergencia.** La frase entera no se
  copia nunca, pero «ta-barsure naba-ni» sale en 27 respuestas (17,5%), sin
  tendencia por día. En el run de ablación de julio (`bdc54134`) salía en 60 de
  294 (20%). Por eso bajan la acumulada y la ventana y apenas se mueve la
  emergente, que excluye el vocabulario base.

**Qué queda para la era 2:**
1. Poner la semilla en el orquestador y en la huella antes de H3.
2. Que el diccionario koiné filtre las formas de las frases modelo, o que las
   frases modelo roten, para que la lista no mida la plantilla.
3. El veredicto se sigue leyendo con la emergente (DISENO_KOINE §7).

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
- ✅ **El veredicto impreso de la ablación decía "CONVERGE ✓"** porque comparaba
  inicio vs fin de forma naive (−6.6% es negativo). Era correcto pero engañoso
  leído solo: la trayectoria es plateau, no convergencia sostenida. **Resuelto**
  (`veredicto_convergencia()` en `curiana_koine.py`, 2026-07-08): el veredicto
  mira ahora la pendiente del último tercio y distingue `converge` /
  `plateau` / `diverge`. La ablación pasó a imprimir "SE ESTABILIZA ~".
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

Detalle completo en [`ANALISIS_RUN_30T_2026-06-22.md`](analisis/ANALISIS_RUN_30T_2026-06-22.md).

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
