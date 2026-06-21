-- ══════════════════════════════════════════════════════════════════════
-- CURIANA — Perfiles de agentes
--    Análisis narrativo por personaje: rol, resumen de su arco en la
--    simulación, y frases célebres seleccionadas por impacto.
--    Generado por curiana_perfilador.py tras correr una simulación.
-- ══════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────────
-- 8. AGENT_PROFILES
--    Una fila por agente por run: snapshot del análisis narrativo.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_profiles (
  id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  run_id           UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,

  agent_name       TEXT NOT NULL,
  tier             INT,
  rol_comunidad    TEXT,                       -- rol narrativo corto, ej. "Señor de la Curiana"
  resumen_arco     TEXT,                       -- 2-3 frases: cómo evolucionó el personaje en el run

  total_respuestas INT DEFAULT 0,
  avg_score        FLOAT,
  neologismos_propuestos INT DEFAULT 0,
  neologismos_adoptados  INT DEFAULT 0,

  generated_by     TEXT DEFAULT 'claude-haiku-4-5-20251001',
  created_at       TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE (run_id, agent_name)
);

-- ─────────────────────────────────────────────────────────────────────
-- 9. AGENT_QUOTES
--    Frases célebres curadas por el agente analista, con justificación.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_quotes (
  id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  profile_id       UUID REFERENCES agent_profiles(id) ON DELETE CASCADE,
  response_id      UUID REFERENCES agent_responses(id) ON DELETE SET NULL,

  run_id           UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
  agent_name       TEXT NOT NULL,

  quote            TEXT NOT NULL,               -- la frase en caquetío (+ glosa si la trae)
  justificacion     TEXT,                       -- por qué el agente analista la eligió
  impacto_score     FLOAT,                      -- 0-10, ranking de impacto asignado por el analista
  day               INT,
  turn_num          INT,

  created_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_profiles_run    ON agent_profiles(run_id);
CREATE INDEX IF NOT EXISTS idx_agent_profiles_agent  ON agent_profiles(agent_name);
CREATE INDEX IF NOT EXISTS idx_agent_quotes_profile  ON agent_quotes(profile_id);
CREATE INDEX IF NOT EXISTS idx_agent_quotes_run      ON agent_quotes(run_id);
CREATE INDEX IF NOT EXISTS idx_agent_quotes_agent    ON agent_quotes(agent_name);

ALTER TABLE agent_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_quotes   ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read agent_profiles" ON agent_profiles FOR SELECT USING (true);
CREATE POLICY "public read agent_quotes"   ON agent_quotes   FOR SELECT USING (true);

-- ─────────────────────────────────────────────────────────────────────
-- REAL-TIME (el dashboard puede mostrar perfiles a medida que se generan)
-- ─────────────────────────────────────────────────────────────────────
ALTER PUBLICATION supabase_realtime ADD TABLE agent_profiles;
ALTER PUBLICATION supabase_realtime ADD TABLE agent_quotes;
