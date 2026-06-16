-- ══════════════════════════════════════════════════════════════════════
-- CURIANA — Schema Supabase (PostgreSQL)
-- Pegar en el SQL Editor de Supabase y ejecutar completo.
-- ══════════════════════════════════════════════════════════════════════

-- UUID extension (ya activa en Supabase, incluida por si acaso)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ─────────────────────────────────────────────────────────────────────
-- 1. LEXICON
--    Vocabulario base + cognados con etimología completa.
--    Se seed-ea desde VOCABULARIO_BASE de curiana_lexicon.py.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lexicon (
  id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  word           TEXT NOT NULL UNIQUE,
  meaning        TEXT NOT NULL,
  category       TEXT,                        -- sust, v_raiz, pron, num, part, adj, interr, topón, título
  source_language TEXT NOT NULL DEFAULT 'desconocido',
                                              -- caquetío | wayunaiki | lokono | taíno | arahuacano
  attested       BOOLEAN DEFAULT FALSE,       -- documentado en fuentes coloniales (Zavala, Jahn, Alvarado)
  source_ref     TEXT,                        -- "Zavala Reyes 2015", "Wayunaiki (Álvarez 2017)", etc.
  cognates       TEXT[],                      -- formas cognadas en otras lenguas
  etymological_note TEXT,                     -- nota libre de etimología/morfología
  created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────────────
-- 2. SIMULATION_RUNS
--    Cada vez que se corre el orquestador.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS simulation_runs (
  id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  started_at     TIMESTAMPTZ DEFAULT NOW(),
  ended_at       TIMESTAMPTZ,
  total_turns    INT DEFAULT 0,
  total_days     INT DEFAULT 0,
  model          TEXT DEFAULT 'claude-haiku-4-5-20251001',
  langsmith_project TEXT,                     -- nombre del proyecto en LangSmith para este run
  config         JSONB                        -- max_tokens, agents, etc.
);

-- ─────────────────────────────────────────────────────────────────────
-- 3. TURNS
--    Cada media jornada (2 turnos = 1 día simulado).
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS turns (
  id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  run_id         UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
  day            INT NOT NULL,
  turn_num       INT NOT NULL,
  moment         TEXT,                        -- amanecer | mañana | mediodia | tarde | anochecer | noche
  season         TEXT,                        -- seca | lluvias
  event_description TEXT,
  created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────────────
-- 4. AGENT_RESPONSES
--    Una fila por agente por turno. El corazón del análisis.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_responses (
  id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  turn_id        UUID REFERENCES turns(id) ON DELETE CASCADE,
  run_id         UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,

  agent_name     TEXT NOT NULL,
  ethnicity      TEXT,
  tier           INT,                         -- 1, 2 o 3

  response_text  TEXT NOT NULL,
  score          FLOAT,                       -- 0-10 densidad lingüística

  -- Composición por lengua fuente (% de palabras reconocidas, suma ≈ 1.0)
  pct_caquetio   FLOAT DEFAULT 0,             -- caquetío atestiguado + reconstruido
  pct_wayunaiki  FLOAT DEFAULT 0,
  pct_lokono     FLOAT DEFAULT 0,
  pct_taino      FLOAT DEFAULT 0,
  pct_arahuacano FLOAT DEFAULT 0,             -- proto-arawakan / compartido

  -- Morfología activa
  aspects_used   TEXT[],                      -- completivo | continuativo | prospectivo
  words_used     TEXT[],                      -- todas las palabras reconocidas
  neologisms_proposed INT DEFAULT 0,

  -- Trazabilidad
  langsmith_trace_url TEXT,

  created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────────────
-- 5. WORD_USES
--    Granular: cada uso de cada palabra caquetía en cada respuesta.
--    Permite calcular frecuencia, difusión entre agentes, etc.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS word_uses (
  id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  response_id    UUID REFERENCES agent_responses(id) ON DELETE CASCADE,
  run_id         UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
  turn_id        UUID REFERENCES turns(id) ON DELETE CASCADE,

  word           TEXT NOT NULL,
  source_language TEXT,                       -- de lexicon.source_language
  agent_name     TEXT,
  day            INT,
  turn_num       INT,

  created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────────────
-- 6. NEOLOGISMS
--    Palabras nuevas propuestas durante la simulación.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS neologisms (
  id                 UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  run_id             UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,

  form               TEXT NOT NULL,           -- la nueva palabra
  components         TEXT,                    -- "sima + -bana"
  meaning            TEXT,
  morphological_rule TEXT,                    -- -ana | -bana | -ko | -sha | etc.

  proposed_by        TEXT NOT NULL,
  proposed_turn_id   UUID REFERENCES turns(id),
  proposed_day       INT,

  status             TEXT DEFAULT 'propuesto', -- propuesto | adoptado | rechazado | ignorado
  adopted_by         TEXT[],
  adopted_turn_id    UUID REFERENCES turns(id),
  rejected_by        TEXT[],

  created_at         TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────────────
-- 7. PHRASE_ETYMOLOGIES
--    Análisis palabra-por-palabra de frases notables.
--    Se pueden insertar automáticamente o curar manualmente.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS phrase_etymologies (
  id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  response_id      UUID REFERENCES agent_responses(id) ON DELETE SET NULL,

  phrase           TEXT NOT NULL,             -- la frase completa
  word_breakdown   JSONB,                     -- [{word, source_language, meaning, is_neologism, note}]
  lang_composition JSONB,                     -- {caquetío: 0.4, wayunaiki: 0.35, ...}

  -- Curación manual opcional
  etymological_note TEXT,
  curated_by        TEXT,                     -- "manual" | "auto" | nombre del curador
  is_notable        BOOLEAN DEFAULT FALSE,    -- marcar frases destacadas

  created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────────────
-- INDEXES
-- ─────────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_agent_responses_run      ON agent_responses(run_id);
CREATE INDEX IF NOT EXISTS idx_agent_responses_agent    ON agent_responses(agent_name);
CREATE INDEX IF NOT EXISTS idx_agent_responses_turn     ON agent_responses(turn_id);
CREATE INDEX IF NOT EXISTS idx_word_uses_word           ON word_uses(word);
CREATE INDEX IF NOT EXISTS idx_word_uses_agent          ON word_uses(agent_name);
CREATE INDEX IF NOT EXISTS idx_word_uses_run            ON word_uses(run_id);
CREATE INDEX IF NOT EXISTS idx_neologisms_status        ON neologisms(status);
CREATE INDEX IF NOT EXISTS idx_neologisms_run           ON neologisms(run_id);
CREATE INDEX IF NOT EXISTS idx_turns_run                ON turns(run_id);
CREATE INDEX IF NOT EXISTS idx_lexicon_source           ON lexicon(source_language);

-- ─────────────────────────────────────────────────────────────────────
-- REAL-TIME (habilitar para las tablas que el dashboard observa en vivo)
-- ─────────────────────────────────────────────────────────────────────
ALTER PUBLICATION supabase_realtime ADD TABLE agent_responses;
ALTER PUBLICATION supabase_realtime ADD TABLE neologisms;
ALTER PUBLICATION supabase_realtime ADD TABLE turns;

-- ─────────────────────────────────────────────────────────────────────
-- ROW LEVEL SECURITY (RLS)
--    Para Vercel/público: read-only sin autenticar.
--    El orquestador Python usa la service_role key (bypassa RLS).
-- ─────────────────────────────────────────────────────────────────────
ALTER TABLE lexicon            ENABLE ROW LEVEL SECURITY;
ALTER TABLE simulation_runs    ENABLE ROW LEVEL SECURITY;
ALTER TABLE turns              ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_responses    ENABLE ROW LEVEL SECURITY;
ALTER TABLE word_uses          ENABLE ROW LEVEL SECURITY;
ALTER TABLE neologisms         ENABLE ROW LEVEL SECURITY;
ALTER TABLE phrase_etymologies ENABLE ROW LEVEL SECURITY;

-- Políticas de lectura pública (anon puede SELECT)
CREATE POLICY "public read lexicon"            ON lexicon            FOR SELECT USING (true);
CREATE POLICY "public read simulation_runs"    ON simulation_runs    FOR SELECT USING (true);
CREATE POLICY "public read turns"              ON turns              FOR SELECT USING (true);
CREATE POLICY "public read agent_responses"    ON agent_responses    FOR SELECT USING (true);
CREATE POLICY "public read word_uses"          ON word_uses          FOR SELECT USING (true);
CREATE POLICY "public read neologisms"         ON neologisms         FOR SELECT USING (true);
CREATE POLICY "public read phrase_etymologies" ON phrase_etymologies FOR SELECT USING (true);

-- ─────────────────────────────────────────────────────────────────────
-- VISTA: language_drift_by_turn
--    Promedio de composición lingüística por turno (para el chart principal).
-- ─────────────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW language_drift_by_turn AS
SELECT
  t.run_id,
  t.day,
  t.turn_num,
  t.moment,
  t.season,
  ROUND(AVG(ar.pct_caquetio)::NUMERIC,   3) AS avg_caquetio,
  ROUND(AVG(ar.pct_wayunaiki)::NUMERIC,  3) AS avg_wayunaiki,
  ROUND(AVG(ar.pct_lokono)::NUMERIC,     3) AS avg_lokono,
  ROUND(AVG(ar.pct_taino)::NUMERIC,      3) AS avg_taino,
  ROUND(AVG(ar.pct_arahuacano)::NUMERIC, 3) AS avg_arahuacano,
  ROUND(AVG(ar.score)::NUMERIC,          2) AS avg_score,
  COUNT(ar.id)                              AS agents_active
FROM turns t
JOIN agent_responses ar ON ar.turn_id = t.id
GROUP BY t.run_id, t.day, t.turn_num, t.moment, t.season
ORDER BY t.run_id, t.day, t.turn_num;

-- ─────────────────────────────────────────────────────────────────────
-- VISTA: top_words_by_agent
--    Palabras más usadas por cada agente (para los perfiles).
-- ─────────────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW top_words_by_agent AS
SELECT
  wu.run_id,
  wu.agent_name,
  wu.word,
  wu.source_language,
  COUNT(*) AS use_count
FROM word_uses wu
GROUP BY wu.run_id, wu.agent_name, wu.word, wu.source_language
ORDER BY wu.run_id, wu.agent_name, use_count DESC;

-- ─────────────────────────────────────────────────────────────────────
-- GRANTS para los roles del Data API (el Supabase local nuevo NO los
-- auto-otorga). El service_role escribe desde el backend Python; anon /
-- authenticated solo leen (las policies RLS controlan el acceso por fila).
-- ─────────────────────────────────────────────────────────────────────
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT ALL    ON ALL TABLES    IN SCHEMA public TO service_role;
GRANT ALL    ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT SELECT ON ALL TABLES    IN SCHEMA public TO anon, authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL    ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO anon, authenticated;
