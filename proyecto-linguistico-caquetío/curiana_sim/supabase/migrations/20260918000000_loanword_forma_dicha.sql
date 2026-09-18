-- «La etiqueta manda» (Miguel, 2026-09-18): la voz de la esfera se registra
-- con su FORMA INDÍGENA, y lo que el agente escribió se guarda al lado.
--
-- Contexto: casabe, yuca, maíz, batata o papaya son voces taínas del lexicón
-- que el castellano también usa. Cuentan como préstamo de esfera —el producto
-- de la esfera ES la esfera, decisión del 2026-09-17— pero no tienen por qué
-- circular por el motor con la grafía castellana. Desde hoy `word` guarda la
-- forma de la esfera (`curiana_lexicon.FORMA_DE_LA_ESFERA`: casabe → cazabi,
-- maíz → maisi, cacique → cacike, bohío → bohio) y `forma_dicha` la forma
-- literal que el agente usó.
--
-- Son dos preguntas distintas y las dos hacen falta: `word` agrupa la VOZ
-- («casabe» y «cazabi» son la misma y su difusión tier 1 → 2/3 es una sola
-- serie) y `forma_dicha` conserva el HECHO OBSERVADO, que es que el agente
-- escribió «casabe». Perder la segunda sería reescribir el dato; perder la
-- primera es lo que hacía que la misma voz saliera dos veces en la tabla.
--
-- Los runs YA CORRIDOS no se reescriben (mismo principio que el 2026-09-17:
-- «una fila de loanword_uses es un hecho observado; lo que significa lo decide
-- quien lee»). En esas filas `forma_dicha` queda NULL y `word` conserva la
-- grafía de entonces; `analizar_runs.py --prestamos` normaliza al LEER.
--
-- El scorer NO se toca: `score_linguistico()` sigue devolviendo la clave
-- castellana en `prestamos_de_esfera`, `score` y `pct_*` quedan byte a byte.
--
-- Ver 6-fusion/descastellanizar_esfera_2026-09-18.yaml y la entrada
-- `descastellanizar_esfera` de 6-fusion/decisiones_tanda_2026-09-17.yaml.
--
-- ⚠ Se aplica como entraron `loanword_uses` y `presencias` (ver CLAUDE.md):
--     docker cp <este .sql> supabase_db_curiana_sim:/tmp/
--     docker exec supabase_db_curiana_sim psql -U postgres -d postgres \
--       -v ON_ERROR_STOP=1 -f /tmp/20260918000000_loanword_forma_dicha.sql
--     insert into supabase_migrations.schema_migrations(version) …
--   `supabase migration up` se planta con las versiones sin registrar.

alter table loanword_uses add column if not exists forma_dicha text;

comment on column loanword_uses.word is
  'La forma de la ESFERA: la clave indígena cuando el lexicón la tiene (cazabi, maisi, cacike, bohio). Es por la que se agrupa la voz.';
comment on column loanword_uses.forma_dicha is
  'Lo que el agente escribió de verdad (casabe, maíz…). NULL en las filas anteriores al 2026-09-18, que no se reescriben.';

create index if not exists idx_loanword_uses_dicha on loanword_uses(run_id, forma_dicha);
