-- ══════════════════════════════════════════════════════════════════════
-- KOINE_METRICS — métrica de convergencia por run/día
-- La distancia idiolectal media (1 - coseno entre pares de agentes que
-- realmente hablaron). Firma de la koineización: debe CONTRAERSE en el tiempo.
-- Antes solo se imprimía y se perdía; ahora se persiste para analizar/graficar.
-- ══════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS koine_metrics (
  id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  run_id       UUID REFERENCES simulation_runs(id) ON DELETE CASCADE,
  day          INT NOT NULL,
  distance     FLOAT,           -- distancia idiolectal media (0..1)
  n_agents     INT,             -- agentes considerados (los que hablaron)
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (run_id, day)
);

CREATE INDEX IF NOT EXISTS idx_koine_metrics_run ON koine_metrics(run_id);

ALTER TABLE koine_metrics ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public read koine_metrics" ON koine_metrics FOR SELECT USING (true);

GRANT ALL    ON koine_metrics TO service_role;
GRANT SELECT ON koine_metrics TO anon, authenticated;
