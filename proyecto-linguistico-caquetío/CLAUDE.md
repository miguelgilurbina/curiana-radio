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
   marcarlo es el error que Oliver denuncia.
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
| **Cada entrypoint carga su `.env`** | Leer `os.environ` no basta: `load_dotenv(...)` al inicio del módulo o falla por credenciales |
| **`pypdf` ≠ `pdftotext`** | Producen texto distinto del mismo PDF. Arcaya sale **vacío** con pypdf; `pdftotext` da 467 KB. Y pypdf parte `Todariquiba` en `T odariquiba` |
| **Tablas a dos columnas** | Se desalinean sin `-layout`. Extraer las dos veces y comparar |
| **`lexicon` en PostgREST** | `max_rows`=1000 y hay ~1400 palabras: toda query sin `.range()` se trunca **en silencio**. Ver `loadLexicon()` |
| **`lexicon_zavala.py` es generado Y se importa** | Regenerarlo **cambia `score_linguistico()`**. ⚠️ Los otros `lexicon_*.py` NO los importa el motor, pero **sí el tooling** (`generar_tablero`, `auditar_82`, `migrar_toponimos` — medido 2026-08-15): no se pueden mover de `curiana_sim/` sin romperlo |
| **La consola de Windows es cp1252** | Todo script que imprima `─`, `✓` o acentos necesita `_forzar_utf8()` bajo `__main__` |
| **`pct_caquetio` está saturada** | 91% de las respuestas en 1.0. **No la uses para comparar agentes** — usa `score`. Issue #69 |
| **La longitud del prompt predice el score** | r = −0.48. Cualquier análisis por agente tiene que controlarla, o estarás midiendo cuánto escribiste tú. Ver `ANALISIS_BASE_2026-08-06.md` |

---

## Comandos

```bash
cd curiana_sim
pip install -r requirements.txt

python guardianes.py              # los 8 en verde antes de cerrar nada
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
python compilar_corpus.py --check # valida 3-mundo/corpus/
python compilar_asentamientos.py  # los nodos de la esfera: existencia y época
python curiana_polities.py --canon

supabase start                    # Docker local (ver puertos arriba)
python curiana_database.py seed   # siembra el lexicón activo
```

### Correr simulación

```bash
python curiana_orchestrator_v2.py --auto 30 --perfiles --reporte
#   --perfiles  perfiles curados por agente al cerrar (agent_profiles/quotes)
#   --reporte   reporte anual LLM al completar cada año simulado
#   --ablacion  run de CONTROL: apaga las inyecciones que empujan convergencia.
#               La evidencia de koineización es la DIFERENCIA normal vs. ablación
```

---

## Dónde está cada cosa

```
INDICE.md          la puerta del vault
TABLERO.md         el estado medido (generado — no se edita a mano)
1-plan/            ¿qué hacemos y qué falta?
2-lengua/          ¿cómo es el caquetío?  lexicon · morfologia · toponimia · metodo-comparativo
                   datos: cognados.yaml · toponimos.yaml · morfemas.yaml (ver datos-de-lengua)
3-mundo/           ¿cómo era ese pueblo?  5 mapas · polities-caquetias · corpus/ · ensayos/
                   esfera-de-interaccion · asentamientos.yaml (los nodos)
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
| `curiana_social` | contagio léxico, prestigio, variación dialectal |
| `curiana_state` | día, estación, locaciones, eventos |
| `curiana_observer` | scoring, análisis, perfiles curados |
| `curiana_database` | Supabase + LangSmith |
| `curiana_polities` | las 4 polities atestiguadas; cuál simulamos |

**Los wikilinks resuelven por basename**, así que mover una nota no rompe
enlaces; lo que se rompe son los enlaces markdown relativos.

---

## Morfología (lo mínimo para leer el output)

```
Orden: pronombre + verbo-aspecto + complemento
Pronombres: taya (yo), pia (tú), nüma (él/ella), tayamaa (nosotros)
Aspectos:   -ka (completivo), -ni (continuativo), -da (prospectivo)
Posesivos:  ta- (mi), pi- (tu), nü- (su)
Locativos:  -bana (cerro, sitio alto — D9 resuelta 2026-08-31, seis apoyos;
            homónimo de bana 'hígado' reconstruido), -ana (forma atestiguada,
            glosa 'lugar de' EN DISPUTA — #109), -ko (interior de)
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
simulation_runs → turns → agent_responses → word_uses
                                          → neologisms
                       → agent_profiles → agent_quotes
                       → koine_metrics · koine_lexicon
lexicon
```

⚠️ `word_uses.source_language` se resuelve con `_familia_de_token()`, que
deshace prefijos y sufijos. Si vuelve a hacerse con un lookup pelado, **la mitad
del corpus se guarda sin lengua** (pasó: 27.641 de 54.936 usos).
