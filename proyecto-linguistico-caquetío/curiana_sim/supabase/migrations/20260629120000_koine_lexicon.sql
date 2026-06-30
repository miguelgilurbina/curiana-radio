-- ══════════════════════════════════════════════════════════════════════
-- KOINE_LEXICON — diccionario koiné por fijación de competencia
-- Cuando varios agentes acuñan formas rivales para un MISMO referente nuevo
-- (evento de nombramiento) y la comunidad fija una por frecuencia × prestigio,
-- esa entrada se guarda aquí: el concepto, la forma ganadora, y de cuántas
-- variantes salió. Es el producto del motor koiné — y el insumo de la fase de
-- topónimos (un topónimo es un referente compartido que necesita nombre).
-- ══════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS koine_lexicon (
  id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  run_id       UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
  concepto_id  TEXT NOT NULL,        -- referente (cometa, metal_amarillo, ...)
  descripcion  TEXT,                 -- qué es el referente
  form         TEXT NOT NULL,        -- la forma koiné fijada
  fijada_dia   INT,                  -- día simulado en que se fijó
  soporte      FLOAT,                -- soporte acumulado (frecuencia × prestigio)
  n_variantes  INT,                  -- de cuántas formas rivales salió
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (run_id, concepto_id)
);

CREATE INDEX IF NOT EXISTS idx_koine_lexicon_run ON koine_lexicon(run_id);

ALTER TABLE koine_lexicon ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public read koine_lexicon" ON koine_lexicon FOR SELECT USING (true);

GRANT ALL    ON koine_lexicon TO service_role;
GRANT SELECT ON koine_lexicon TO anon, authenticated;
