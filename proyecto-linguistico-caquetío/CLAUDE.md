# Curiana — Simulador de Emergencia Lingüística Caquetía

Investigación + experimento computacional: 60 agentes históricos (pueblo
Caquetío, Golfete de Coro, s. XIV-XV) hablan en caquetío-arahuaco reconstruido,
inventan palabras y se contagian entre sí. La deriva se registra en Supabase, se
cura y se publica en Curiana Radio (`/kaketiana`).

> **Este archivo dice cómo trabajar aquí, no qué sabemos.** Lo que sabemos está
> medido en `TABLERO.md` y explicado en el vault. Si buscas una cifra y la
> encuentras escrita a mano en este archivo, es un bug: repórtalo.

---

## Las reglas que no se rompen

1. **Ninguna cifra a mano.** Se mide (`generar_tablero.py`) o no se dice. Han
   circulado tres tamaños distintos del lexicón a la vez; el corpus tenía dos
   censos (152 y 161) que no coincidían.
2. **Etiqueta epistémica en todo.** Lexicón y corpus distinguen atestiguado /
   reconstruido / hipotético. Una sola por entrada; **en duda, degradar**. Es lo
   que hace que esto sea investigación y no fanfiction.
3. **Precontacto ≠ colonial.** Casi todo el dato es de crónica del s. XVI. La
   simulación es del XIV-XV. No se proyecta sin decidirlo explícitamente.
4. **Los caquetíos no eran una sola sociedad.** Modelamos la polity **costera**
   (`curiana_polities.py`). Importar un rasgo de Barquisimeto o los Llanos sin
   marcarlo es el error que Oliver denuncia. Y el reverso, que cuesta más ver
   (Miguel, 2026-09-11): **la unidad de análisis es la esfera, no una comarca
   moderna**. La fuente puede ser paraguanera —Medina lo es— pero la conclusión
   es de la Kaketiana, «un área cultural con muchas etnias conviviendo e
   intercambiando». Escribir «los frijoles paraguaneros» aplana igual que
   escribir «los caquetíos», solo que con etiqueta regional en vez de étnica.
   Ver `3-mundo/esfera-de-interaccion.md`.
5. **Minar propone, el humano fusiona.** Un minador **nunca** toca
   `curiana_lexicon.py` ni `3-mundo/corpus/`. Deja su propuesta en `6-fusion/`
   (datos en YAML; issues redactados en `issues-pendientes/`) y regenera la
   BANDEJA. Nada valioso muere en el scratchpad de una sesión.
6. **Un cero hay que verificarlo.** Un `grep` sin resultados mide tu consulta,
   no la fuente. Ver la skill `minar-fuente` §2 — pasó tres veces en una noche.
7. **Minar alimenta la esfera que toque, no solo el lexicón.** Lengua (léxico,
   cognados, topónimos) y mundo (parentesco, ecología, creencia, transmisión,
   geografía política). La nota de `4-fuentes/` es la **bitácora** —qué se
   preguntó, qué se halló, qué no—, no el almacén. La mayoría de las obras
   dejan rastro en una sola esfera por sesgo del minador, no de la fuente —
   se mide con `medir_sostiene.py --esferas`.
8. **Citar es una clave foránea, no prosa.** `procedencia.obra` apunta a
   `4-fuentes/bibliografia.yaml` y el validador lo comprueba. Si no hay fuente,
   se declara `deuda: sin-procedencia`: el hueco se admite, **callarlo no**.
9. **Nunca secretos en archivos del proyecto** — ni gitignored: el repo
   sincroniza a OneDrive.
10. **Las decisiones viven en el tablero de GitHub** (label `decision`), no en
    markdown. `DECISIONES_ABIERTAS.md` se retiró el 2026-08-06.

---

## Trampas medidas (cada una costó un error real)

| Trampa | Qué pasa |
|---|---|
| **Supabase local, no cloud** | El cloud llegó a 8.17 GB de egress. Puertos **64321/64322**, no los 54321 por defecto (esos son de otro proyecto, fintech). Para consultar: `docker exec supabase_db_curiana_sim psql -U postgres -d postgres` |
| **`supabase migration up` no aplica la migración nueva** | La base local tiene 4 versiones en `supabase_migrations.schema_migrations` y `supabase/migrations/` tiene 10: la CLI ve las viejas sin registrar, se planta y pide `--include-all`, que las re-aplicaría (y `20260620000000` crea políticas sin `drop if exists`, así que revienta). Lo que funciona, y es como entraron `loanword_uses` y `presencias`: `docker cp` el `.sql` al contenedor, `psql -v ON_ERROR_STOP=1 -f`, y registrar la versión a mano en `schema_migrations`. Verificar después con `information_schema.columns` |
| **Cada entrypoint carga su `.env`** | Leer `os.environ` no basta: `load_dotenv(...)` al inicio del módulo o falla por credenciales |
| **`pypdf` ≠ `pdftotext`** | Producen texto distinto del mismo PDF. Arcaya sale **vacío** con pypdf; `pdftotext` da 467 KB. Y pypdf parte `Todariquiba` en `T odariquiba` |
| **Tablas a dos columnas** | Se desalinean sin `-layout`. Extraer las dos veces y comparar |
| **`lexicon` en PostgREST** | `max_rows`=1000 y hay ~1400 palabras: toda query sin `.range()` se trunca **en silencio**. Ver `loadLexicon()` |
| **`lexicon_zavala.py`, `lexicon_a2.py` y `lexicon_achagua.py` son generados Y se importan** | Regenerarlos **cambia `score_linguistico()`** (zavala: habla; a2: columnas de comparación paraujano/lokono, D11; achagua: la comparanda de Neira y Ribero 1762, generada desde el YAML de la transcripción — se corrige el YAML, no el módulo). ⚠️ Los otros `lexicon_*.py` NO los importa el motor, pero **sí el tooling** (`generar_tablero`, `auditar_82`, `migrar_toponimos` — medido 2026-08-15): no se pueden mover de `curiana_sim/` sin romperlo |
| **`curiana_agents_era2.py` es generado Y es el elenco activo si `CURIANA_ELENCO=era2`** | Se genera desde `6-fusion/elenco_era2.yaml` con `6-fusion/scripts/generar_agentes_era2.py` (#127). `curiana_agents.py` lo importa al cargarse si la variable está puesta, y todos los módulos hacen `from curiana_agents import ALL_AGENTS`: el elenco se decide ANTES de importar (`--elenco era2` lo fija). Los guardianes corren con la era 1 por defecto. El corpus nombra a la gente como en la era 1 y es canon: **no se reescribe**. `compilar_corpus` resuelve cada `agentes_relacionados` con el `ALIAS_ERA1` que `curiana_agents` expone para el elenco activo (`agentes_de_hecho()` es la única puerta) y valida contra el elenco resuelto; los nombres de la era 1 que la era 2 deja fuera (`FUERA_DEL_ELENCO`) pasan como aviso `agente-sin-equivalente`, no error, y el informe los lista con sus hechos. Darles alias o declararlos personas de fondo es decisión de Miguel |
| **Los eventos están escritos para la era 1** | `EVENTOS_COTIDIANOS`/`EVENTOS_ESTACIONALES` (`curiana_state.py`) nombran a Biro-ko, Shaboro o Tina-sha y traen el marco étnico de la Curiana (guaycaríes en la orilla, el Jirajara de la sierra). `run_turn` filtraba `agentes_involucrados` con `a in ALL_AGENTS` sin resolver `ALIAS_ERA1`, así que en la era 2 casi ningún evento traía a sus protagonistas y el Director narró «Biro-ko» y «los Guaycarí» en Paraguaná (runs c6837386 y 89fc1744, 2026-09-16). Desde entonces `director_select_event()` pasa por `curiana_eventos.evento_para_elenco()`: alias con guiones y mayúsculas, sin foráneos, tabla de reescrituras declarada (`REESCRITURAS_ERA2`) y `llegada_nabaraka` no cae en la era 2 (el evento ES el foráneo). Un evento nuevo se escribe con nombres de la era 1; si un nombre no se puede traducir, el evento cae entero antes que decirse mal — `python curiana_eventos.py` lo mide. **El catálogo no era la única puerta**: el día 3 (run `0193873d`), con los eventos ya traducidos, el Director volvió a escribir «Los Caquetíos y Guaycarí se juntan…» copiando su PROPIA nota del día 2 (`state.notas_orquestador`), que nadie filtraba. Desde el 2026-09-16 todo el texto libre que le llega —la línea de estado, las intervenciones, los cierres y sus notas— pasa por `decir_para_el_mundo()`: mismo alias y mismas reescrituras, y las frases que aún llevan un nombre sin traducción o un marco que la era 2 no tiene se caen **frase a frase** (una reflexión son seis oraciones, no se tira entera por una). El bloque del mundo del prompt del agente también pasa por ahí. **Y el MENSAJE, no sólo el system prompt**: el estímulo de un turno con evento es «[Situación]: {evento}» y se mandaba crudo, así que el evento semilla de la era 1 entró por esa puerta (run `b06f57ea`: 23 de 72 respuestas del día 1 dicen «Shaboro», 16 «Buio-sha», 12 de 12 en el turno 2, mientras el Director decía «Sawaka»). Desde el 2026-09-17 `call_agent` traduce también `user_message`, y si no sobrevive ninguna frase manda el momento del día antes que un mensaje vacío |
| **`estado_inicial_test()` es de la ERA 1 y abría TODO run** | El estado semilla —«Shaboro salió de su choza… Buio-sha lo vio desde lejos», `agentes_en_escena` y `tensiones_activas` de la Curiana, `estacion="seca"`— arrancaba también los runs de la era 2. Desde el 2026-09-17 el motor llama a **`estado_inicial(MUNDO)`** (`curiana_state.py`): CURIANA devuelve `estado_inicial_test()` byte a byte y PARAGUANÁ devuelve el día 1 del Tiempo de Viento, con su evento escrito desde el canon (`clima_era2.yaml` P1 + `sitios_era2.yaml`), la escena leída del módulo GENERADO (el Manaure y un apopo por casa) y las cuatro tensiones que `elenco_era2.yaml` declara, cada una con su línea. Dos avisos: **nadie lee `tensiones_activas`** (0 usos fuera de `curiana_state`, auditoría 2026-09-14) y `agentes_en_escena` es la escena del día 1 que nadie actualiza — quien habló de verdad sale de `hizo_hoy`. Y en PARAGUANÁ **el evento dura UN turno**: el día tiene seis momentos y `run_turn` lo archiva y lo apaga al cerrar el turno; repetirlo es decisión del Director. Antes duraba hasta que él eligiera otro (3 turnos en `b06f57ea`, 3 en `89fc1744`). `turns.event_description` se escribe **después** de que el Director decida (antes guardaba el del turno anterior) y ya dicho para el mundo activo |
| **`2-lengua/toponimos.yaml` no se edita a mano** | Es generado desde `lexicon_toponimos.py` por `migrar_toponimos.py`. Dos commits (2026-08-30/31) lo editaron directo y la siguiente regeneración deshizo 25 entradas. Se edita el módulo y se regenera; `test_el_canon_de_toponimos_es_lo_que_emite_el_migrador` lo vigila |
| **La consola de Windows es cp1252** | Todo script que imprima `─`, `✓` o acentos necesita `_forzar_utf8()` bajo `__main__` |
| **`pct_caquetio` está saturada** | 91% de las respuestas en 1.0. **No la uses para comparar agentes** — usa `score`. Issue #69 |
| **`palabras_caquetias` no era lo que decía su nombre** | Devolvía TODAS las voces arahuacas, y de ahí comen el contagio léxico, la competencia de formas, el idiolecto, el campo léxico de la koiné y `words_used`: una voz wayuu o lokono se habría propagado como propia. Arreglado el 2026-09-09 (`palabras_arahuacas` guarda la lista completa). Antes de tocar un campo, mirar quién lo consume — el nombre miente |
| **El 80% del lexicón no es caquetío** | 1.201 de 1.500 claves son comparanda (wayuu, lokono, taíno...). No llega al hablante porque el muestreador del prompt SÍ filtra por `fuente`, pero `palabras_activas()` no filtra: cualquier consumidor que la use está viendo las cinco lenguas. Medido en `6-fusion/medicion_contaminacion_score_2026-09-09.yaml` |
| **Nombre o palabra lo decide la MAYÚSCULA** | 52 voces del canon son homógrafas de un nombre del elenco (`buko`, `hayo`, `mene`, `karebe`, `jachos`…). El filtro de nombres del 2026-09-14 comparaba en minúsculas y las borraba del conteo: palabras que el motor enseñaba y no contaba. Desde el 2026-09-16, `Karebe` es la persona y `karebe` el cucharón. Residuo elegido: una voz del canon que abra frase no cuenta — inflar `palabras_caquetias` es peor, porque de ahí comen el contagio y el idiolecto |
| **El préstamo de esfera no es una fuga** | `ESFERA_DE_CONTACTO` (taíno, kalinago, paraujano, caribe-continental, jirajaroide) se mide aparte en `prestamos_de_esfera` y NO penaliza (decisión 2026-09-15). Hablar wayuu o lokono sí penaliza: son el andamio de la reconstrucción, y verlos haría circular la medición. Sólo el tier 1 recibe el bloque `[Voces de fuera]`. Se persiste en `loanword_uses` (con tier y día), NO en `word_uses`, que es sólo caquetío y ningún lector suyo filtra por lengua (run c6837386, 2026-09-16); se lee con `analizar_runs.py --prestamos` |
| **La pre-carga de idiolectos va indexada por los nombres de la ERA 1** | `curiana_koine.FORMAS_SEED`/`EMOCIONAR_SEED` usan los nombres viejos, y la era 2 renombró a 60 de 63: sin resolver `ALIAS_ERA1`, 62 de 63 agentes arrancaban con el MISMO vector-semilla (2 distintos de 63, medido el 2026-09-16) y «convergencia» no significaba nada (DISENO_KOINE §4). Desde entonces `formas_seed_de()`/`emocionar_de()` resuelven el alias y quien no tiene semilla escrita recibe una DERIVADA de su ficha (oficio → campo semántico, sorteo determinista con blake2b sobre semilla+nombre, nunca el RNG global ni `hash()`). La era 1 queda byte a byte: allí `ALIAS_ERA1` está vacío y la derivación exige `oficio`. **`--continuar` NO recupera una semilla que nunca hubo** (`cargar_koine` reconstruye con `peso_semilla=0`): hay que re-correr la cadena desde el día 1 — el motor lo mide y avisa |
| **El prestigio y los vínculos van indexados por los nombres de la ERA 1** | Misma trampa que la fila de arriba, en `curiana_social.py`: `PRESTIGIO` y `VINCULOS` usan los nombres viejos y en la era 2 **1 de 63 claves estaba viva** (Manaure), con sus tres destinos fuera del elenco. El prestigio medido era `1.0×1 · 0.5×16 · 0.4×36 · 0.2×10` —el TIER con otro nombre— y es el que pondera la fijación de la koiné (`CompetenciaLexica._prestigio`). Desde el 2026-09-17 se lee por **dos puertas**: `prestigio_de()` y `vinculos_de()`, que resuelven `ALIAS_ERA1` (5 entradas de cada tabla vuelven así) y, para quien no tiene entrada escrita, **derivan una de su ficha** — el papel (`rol_en_la_casa`/`oficio`) colocado en la banda de su equivalente de la era 1, y los vínculos con la cabeza de su casa, la mayor de su linaje fuera de ella y la casa del sitio del que lo trajeron. Sin `hash()` ni RNG global. Medido: 63 de 63 con prestigio propio (15 valores, los tres tiers solapados), 0 aristas a fantasmas, 110 entre nodos donde había 0, nadie aislado. `VINCULOS`/`PRESTIGIO` **no se leen directo**. La era 1 queda byte a byte (`ALIAS_ERA1` vacío, la derivación exige `rol_en_la_casa`) y `test_social.py` compara la tabla entera. Antes/después: `6-fusion/medicion_prestigio_vinculos_era2_2026-09-17.yaml`; lo mide `python curiana_sim/curiana_social.py`. ⚠️ Esto **no** diseña la frontera entre nodos (issue `frontera-entre-nodos-2026-09-17.md`): sólo restituye los vínculos que el canon ya había escrito |
| **Una forma recién acuñada no es una `palabra_activa`** | `score_linguistico()` sólo reconoce `lexico.palabras_activas()` (base + **adoptados**), así que la acuñación no entraba en `palabras_caquetias` → ni en `words_used` → ni en `word_uses`: el primer usuario registrado de una forma era el ADOPTANTE, que puede ser del otro nodo (29 de 40 acuñaciones, 72,5%, `analizar_nodos.py` 2026-09-16), y las rutas de contagio salían invertidas. Se pasa aparte (`save_agent_response(..., coined_words=…)`) y se escribe con `source_language='caquetío'` declarado. El scorer no se toca: `score` y `pct_*` no se mueven a mitad de serie |
| **La competencia léxica repetía el mismo referente cada día** | `auto_mode` empezaba `REFERENTES_NOVEDOSOS` de cero en cada run, y un día de seis turnos sólo llega al primero (turno 5): los tres días de la serie A volvieron a nombrar «las cuentas brillantes» (10 de 12 respuestas en el turno 5 de CADA día) y los otros nueve referentes no salieron nunca. «La koiné sobrevivió la noche» era en parte el instrumento re-enseñando el referente. Desde el 2026-09-17 el estado guarda `referentes_introducidos` y `--continuar` sigue la secuencia (día 2: el cometa, día 3: el eclipse…); `referentes_pendientes_de(state)` es la única puerta. Un run nuevo sí la empieza de cero |
| **La longitud del prompt predice el score** | r = −0.48. Cualquier análisis por agente tiene que controlarla, o estarás midiendo cuánto escribiste tú. Ver `ANALISIS_BASE_2026-08-06.md` |

---

## Comandos

```bash
cd curiana_sim
pip install -r requirements.txt

python guardianes.py              # los 9 en verde antes de cerrar nada
python guardianes.py --rapido     # sin los tests (más rápido)

# Los datos de lengua y la bibliografía
python generar_bibliografia.py    # 4-fuentes/bibliografia.yaml (generado)
python compilar_lengua.py         # valida cognados, topónimos, morfemas
python compilar_lengua.py --deuda # qué no cita a nadie todavía
python medir_sostiene.py --esferas  # qué esfera alimenta cada obra
python ocr_fuente.py <pdf> --lang spa  # fuentes escaneadas sin capa de texto
                                  # (localiza la página; la cita se saca de la imagen)

python generar_tablero.py         # reescribe TABLERO.md (medido)
python generar_tablero.py --gh    # + decisiones del tablero (usa red)
python generar_bandeja.py         # reescribe 6-fusion/BANDEJA.md — la cola de fusión
python generar_cronica.py         # reescribe 1-plan/CRONICA.md — cada cambio de main, con fecha

python analizar_runs.py --todo    # análisis de los runs en la base
python analizar_nodos.py --run <id8>  # la era 2 por nodo (GUARANAO/AMUAY): formas
                                  # normalizadas por hablantes posibles, cruce entre
                                  # nodos y distancia idiolectal intra/entre. Sube la
                                  # cadena por `continuado_desde`; `--todo` las cadenas
python analizar_nodos.py --run <id8> --lugar   # la ESCENA (tabla `presencias`):
                                  # ocupación por lugar y momento, cuántas escenas
                                  # tuvieron más de un hablante, y el cruce de las formas
                                  # por LUGAR además de por nodo — con qué lugares tocan
                                  # los dos nodos EN EL MISMO TURNO. Sin la bandera el
                                  # informe es el de siempre; sobre un run anterior a la
                                  # escena avisa y sigue
python compilar_corpus.py --check # valida 3-mundo/corpus/
python compilar_asentamientos.py  # los nodos de la esfera: existencia y época
python compilar_etnias.py         # los vecinos: con quién, y de qué polity (regla 4)
python barrer_mapa.py --lote      # el mapa vivo (OSM) cruzado con la mesa de topónimos
python curiana_polities.py --canon

supabase start                    # Docker local (ver puertos arriba)
python curiana_database.py seed   # siembra el lexicón activo
```

### Correr simulación

```bash
python curiana_orchestrator_v2.py --auto 30 --perfil base --perfiles --reporte
#   --perfil    QUÉ capas del lexicón ven los agentes y si hay andamiaje.
#               base · atestiguado · suelto · control · suelto-control
#               Se guarda RESUELTO en simulation_runs.config. Por defecto: base
#   --listar-perfiles   los perfiles disponibles, con su pregunta
#   --perfiles  perfiles curados por agente al cerrar (agent_profiles/quotes)
#   --reporte   reporte anual LLM al completar cada año simulado
#   --ablacion  atajo al perfil `control`. La evidencia de koineización es la
#               DIFERENCIA normal vs. ablación
#
# Era 2 (2026-09-14): el día largo y los días encadenados
#   --turnos-por-dia 6      un día = los seis momentos (la era 1 corría con 2)
#   --agentes-por-turno 12  la ventana que habla por turno (la era 1: 6)
#   --roster todos          todos los no foráneos, tier 3 incluidos (era 1: `koine`, 23 fijos)
#   --semilla N             fija el azar del motor y se sella en la huella
#   --continuar             arranca del estado, memoria, lexicón y koiné del run anterior
#                           (curiana_*.json en curiana_sim/); la config dice de qué run viene
#                           (`continuado_desde`). Al cerrar, el motor imprime ADEMÁS la serie
#                           y el veredicto de la CADENA entera (curiana_cadena.py): la serie
#                           del run solo tiene un día y siempre diría «datos insuficientes».
#                           Un run interrumpido sigue en la cadena pero sus métricas no entran
#   --perfil era2           base sin la capa hipotética y CON la retroabstraída (voces vivas:
#                           matakán y las de Medina; decisiones 2026-09-14); un run = un día
#   --elenco era2           el elenco de Paraguaná (63, generado desde 6-fusion/elenco_era2.yaml);
#                           el prompt nombra nodo, casa y sitio; el mundo pasa a PARAGUANÁ, y con él
#                           el calendario (viento 50 / seca larga 40 / siembra 30, decisión 2026-09-15)
#                           y el bloque [Tu tierra] (curiana_mundo.py: el canon de sitios y clima de
#                           6-fusion/, ≤ 320 caracteres, rotando por agente y día; test de las 126).
#                           El Director también cambia de mundo (curiana_director.py): «de Paraguaná»,
#                           y cada cierre de turno lleva [El mundo] (≤ 400: la frase del período, la del
#                           momento y las restricciones del corpus, ecologia-007/018/032: cardonal, sin
#                           ríos ni ceibas). Los eventos se dicen para el elenco (curiana_eventos.py)
#   --reflexion             al cerrar cada día, UNA llamada más: el Director, con el mundo, lee los
#                           cierres del día y el reporte medido y escribe 4-6 oraciones (qué cambió,
#                           qué palabra prendió, qué queda abierto). Va al log como
#                           `# REFLEXIÓN DEL DIRECTOR — Día N`, a state.notas_orquestador (el día
#                           siguiente la ve con --continuar) y a curiana_director.json (junto a los
#                           otros curiana_*.json; un run que no continúa empieza el archivo de cero).
#                           La línea de estado que se le pasa es la del DÍA CERRADO
#                           (estado_del_dia_cerrado: «Día N, Turno último (noche)»), no la del
#                           amanecer siguiente: el día 3 el modelo copió el «Día 4, Turno 1» del
#                           estado a su propia cabecera. Recibe además el elenco que habló hoy.
#                           Apagado por defecto: cuesta API
#   --escena                LA ESCENA POR LUGAR (2026-09-17, curiana_escena.py): cada turno, cada
#                           uno de los 63 —no sólo los 12 que hablan— está en UN LUGAR que deciden
#                           su oficio y la hora (6-fusion/escena_era2.yaml → curiana_escena_era2.py,
#                           generados). `run_turn` lo escribe en state.ubicaciones_override, que
#                           llevaba cuatro lectores y cero escrituras; el prompt cambia
#                           [Tu ubicación] por [Aquí estás] (dónde estás, qué momento y quién está
#                           contigo, ≤ 200 car.); y el Director recibe las intervenciones AGRUPADAS
#                           POR LUGAR, con cero llamadas más (decisión 6 → A). Es un BRAZO, no un
#                           parche: apagado por defecto, y sin el flag el prompt de la era 2 es
#                           byte a byte el de hoy (y el de la era 1, siempre). Se sella en
#                           simulation_runs.config con `capubana_cada`, sale en la cabecera del run
#                           y **una cadena --continuar no puede cambiar de brazo a la mitad**: el
#                           motor avisa y se niega (la evidencia es la DIFERENCIA entre dos cadenas
#                           completas con la misma semilla, §5.4 del diseño)
#   --capubana-cada N       cada cuántos días convergen los dos nodos en el cerro; ese día los 63
#                           están en el Capubana los seis momentos. Por defecto 3 (decisión 7 → A:
#                           el ciclo mayor del canon cae en los días 55-58 de la seca y una cadena
#                           de ocho no llega, así que la cadencia es un parámetro declarado, como
#                           el perfil). 0 = sin convergencia. Sólo cuenta con --escena
python curiana_mundo.py                                   # las 126 combinaciones de [Tu tierra], con su largo
python curiana_escena.py                                  # las 1.134 escenas de [Aquí estás] (63 × 6 × 3), con su largo
python curiana_escena.py --capubana                       # y el día de la convergencia
python curiana_eventos.py                                 # el catálogo de eventos medido y dicho para la era 2
python curiana_cadena.py                                  # las cadenas `--continuar`: serie de koiné y veredicto por cadena
                                                          # (un run es UN día: su serie sola nunca tiene dos puntos)
#   --serie era2-b          etiqueta del SET de runs dentro de la era, sellada en la config: los tres
#                           días del 2026-09-16 son la serie A (pruebas, sin pre-carga de idiolectos);
#                           lo que cuenta arranca en la B (decisión de Miguel, 2026-09-16)
python curiana_orchestrator_v2.py --elenco era2 --auto 6 --turnos-por-dia 6 --agentes-por-turno 12 --roster todos --perfil era2 --semilla 1
python curiana_orchestrator_v2.py --elenco era2 --auto 6 --agentes-por-turno 12 --roster todos --perfil era2 --semilla 2 --continuar --reflexion
python 6-fusion/scripts/generar_agentes_era2.py --check   # ¿el módulo generado está al día?
python 6-fusion/scripts/derivar_escena_por_lugar.py --canon  # reescribe 6-fusion/escena_era2.yaml
python 6-fusion/scripts/generar_escena_era2.py --check    # ¿curiana_escena_era2.py está al día?
```

⚠️ Los perfiles cambian lo que el agente **ve**, nunca con qué se le **puntúa**:
`capas_de_score` es fijo en todos y hay un test que lo vigila. Si el score se
moviera con el perfil, la diferencia entre brazos sería un artefacto del
instrumento. Diseño en `5-experimento/disenos/05_perfiles_de_run.md`.

---

## Dónde está cada cosa

```
INDICE.md          la puerta del vault
TABLERO.md         el estado medido (generado — no se edita a mano)
1-plan/            ¿qué hacemos y qué falta?
2-lengua/          ¿cómo es el caquetío?  lexicon · morfologia · toponimia · metodo-comparativo
                   datos: cognados.yaml · toponimos.yaml · morfemas.yaml (ver datos-de-lengua)
3-mundo/           ¿cómo era ese pueblo?  5 mapas · polities-caquetias · corpus/ · ensayos/
                   esfera-de-interaccion · asentamientos.yaml (los nodos) · etnias.yaml (los vecinos)
4-fuentes/         ¿de dónde lo sabemos?  una nota por obra + INDICE_FUENTES
5-experimento/     ¿qué probamos?  mapa-motor · ARQUITECTURA · DISENO_KOINE · analisis/
6-fusion/          la cola de entrada al canon: propuestas de datos + issues sin
                   publicar + BANDEJA.md (generado). Un minador deja aquí lo que
                   propone; nada valioso muere en el scratchpad de una sesión
curiana_sim/       el motor + tests/ (+ lexicon_*.py: propuestas que el tooling
                   importa — se indexan en la BANDEJA pero viven aquí)
fuentes_caquetios/ los PDF (se citan, no se editan)
```

**El motor** (`5-experimento/ARQUITECTURA.md` lo mide entero):

| Módulo | Qué hace |
|---|---|
| `curiana_orchestrator_v2` | el bucle; importa a los otros seis |
| `curiana_lexicon` | vocabulario + reglas + prompts + `score_linguistico()` |
| `curiana_agents` | los 60 personajes |
| `curiana_koine` | idiolectos, competencia léxica, métricas de convergencia |
| `curiana_cadena` | la cadena `continuado_desde`: serie de koiné y veredicto sobre TODOS los días encadenados, no sobre el run suelto |
| `curiana_social` | contagio léxico, prestigio, variación dialectal. Las tablas están escritas con los nombres de la era 1: se leen por `prestigio_de()` y `vinculos_de()`, que resuelven el alias y derivan de la ficha lo que no está escrito (`python curiana_social.py` mide el grafo del elenco activo) |
| `curiana_state` | día, estación, locaciones, eventos (escritos para la era 1) y el **estado inicial por mundo** (`estado_inicial(MUNDO)`). Desde el 2026-09-17 lleva además el brazo de la escena (`escena`, `capubana_cada`, `escena_del_turno`), que `--continuar` hereda |
| `curiana_eventos` | los eventos dichos para el elenco activo: alias, sin foráneos, reescrituras declaradas. Y el **texto libre** que llega al Director y al agente (`decir_para_el_mundo`) |
| `curiana_mundo` | el mundo de la era 2: `[Tu tierra]` para el agente y `[El mundo]` para el Director, desde 6-fusion/ y el corpus |
| `curiana_escena` | **dónde está cada uno** (era 2, `--escena`). Una puerta: `ambito_de(agente, state)` devuelve el lugar —una cadena, no un booleano: mañana será adónde se movió por potestad— y `None` sin escena. Lee `curiana_escena_era2.py` (GENERADO desde `6-fusion/escena_era2.yaml`, que deriva del elenco). Determinista: no toca el RNG del motor |
| `curiana_director` | el Director por mundo y su reflexión del día (`--reflexion`, `curiana_director.json`) |
| `curiana_observer` | scoring, análisis, perfiles curados |
| `curiana_database` | Supabase + LangSmith |
| `curiana_polities` | las 4 polities atestiguadas + la occidental (futura esfera, Coquibacoa); cuál simulamos |

**Los wikilinks resuelven por basename**, así que mover una nota no rompe
enlaces; lo que se rompe son los enlaces markdown relativos.

---

## Morfología (lo mínimo para leer el output)

```
Orden: pronombre + verbo-aspecto + complemento
Pronombres: taya (yo), pia (tú), nüma (él/ella), waya (nosotros), naya (ellos)
            — reconstruidos desde el wayuu: deuda de D11 fase 3
Aspectos:   -ka (completivo), -ni (continuativo), -da (prospectivo)
Posesivos:  ta- (mi), wa- (nuestro), ma- (sin/no), ka- (el/la del)
Locativos:  -bana (cerro, sitio alto — D9 resuelta 2026-08-31, seis apoyos;
            homónimo de bana 'hígado' reconstruido), -ana (forma atestiguada,
            glosa 'lugar de' RETIRADA el 2026-09-07 — #109; el motor la
            conserva solo como convención canon-simulación), -ko (interior de)
Neologismos: [forma: componentes = significado]
```

`REGLAS_ZAVALA` añade seis afijos atestiguados: `-iro` (diminutivo), `-aima`,
`-ima`, `-uco`, `-ubana`, `-uru`. El detalle y su evidencia, en
`2-lengua/morfologia.md`.

---

## Modelo y entorno

`claude-haiku-4-5-20251001` para todos los agentes. El cliente se crea en
`curiana_database.py::get_anthropic_client()`; si `LANGSMITH_API_KEY` está en el
entorno, se wrappea solo.

```bash
# curiana_sim/.env  (ver .env.example)
ANTHROPIC_API_KEY=sk-ant-...          # obligatorio
SUPABASE_URL=http://127.0.0.1:64321   # local. Sin esto, modo JSON
SUPABASE_SERVICE_KEY=eyJ...           # service_role local (`supabase status`)
LANGSMITH_API_KEY=...                 # opcional
```

---

## Esquema de datos

```
simulation_runs → turns → agent_responses → word_uses       (sólo caquetío: palabras_caquetias + lo que esa respuesta ACUÑA)
                                          → loanword_uses   (la esfera de contacto, aparte; con tier y día)
                                          → neologisms
                        → presencias                        (la ESCENA: dónde estaba CADA uno de los 63 en cada
                                                             momento del día, no sólo los 12 que hablaron)
                       → agent_profiles → agent_quotes
                       → koine_metrics · koine_lexicon
lexicon
```

`presencias` (migración `20260917000000`, decisión de Miguel del 2026-09-17) es
la capa 1 de la escena: una fila por agente y turno —**63 × 6 momentos = 378 por
día**— con `lugar`, `momento` y el `nodo` congelado del elenco que corrió. Es lo
que hace posible el visor de repetición sobre el mapa, porque «un mapa con 12 de
63 no es un mundo», y lo que lee `analizar_nodos.py --lugar`. Se escribe con
`curiana_database.save_presencias(run_id, turn_id, dia, turno, momento, escena)`,
**una inserción por lote** y no 63 llamadas; sus fallos se cuentan en
`db_fallos["presencias"]` como los de cualquier otra tabla. Un run sin escena
—la era 1, o `--sin-escena`— pasa `{}` y no escribe nada. `agent_responses.lugar`
va desnormalizado al lado de la respuesta para que las consultas de lengua no
tengan que unir una cuarta tabla; sin escena la columna ni se menciona en el
insert. ⚠️ `presencias` pasa del `max_rows`=1000 de PostgREST en tres días: sus
lectores (`presencias_de`, `presencias_de_cadena`) paginan, y cualquier otro
tiene que hacerlo.

⚠️ `word_uses.source_language` se resuelve con `_familia_de_token()`, que
deshace prefijos y sufijos. Si vuelve a hacerse con un lookup pelado, **la mitad
del corpus se guarda sin lengua** (pasó: 27.641 de 54.936 usos).
