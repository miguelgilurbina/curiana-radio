-- ══════════════════════════════════════════════════════════════════════
-- Corrige inconsistencia: el commit e74b413 renombró arahuacano ->
-- proto-arahuaco en supabase_schema.sql, pero nunca se generó la
-- migración correspondiente. agent_responses.pct_arahuacano quedó
-- desincronizada (causaba PGRST204 al guardar respuestas).
-- ══════════════════════════════════════════════════════════════════════

ALTER TABLE agent_responses RENAME COLUMN pct_arahuacano TO pct_proto_arahuaco;

-- Mismo problema con el commit 968ef0b: canonicalizó el lexicon
-- (separó POS de dominio semántico) solo en el doc de referencia.
ALTER TABLE lexicon ADD COLUMN IF NOT EXISTS semantic_domain TEXT;

DROP VIEW IF EXISTS language_drift_by_turn;

CREATE VIEW language_drift_by_turn
WITH (security_invoker = true) AS
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
  ROUND(AVG(ar.pct_proto_arahuaco)::NUMERIC, 3) AS avg_proto_arahuaco,
  ROUND(AVG(ar.score)::NUMERIC,          2) AS avg_score,
  COUNT(ar.id)                              AS agents_active
FROM turns t
JOIN agent_responses ar ON ar.turn_id = t.id
GROUP BY t.run_id, t.day, t.turn_num, t.moment, t.season
ORDER BY t.run_id, t.day, t.turn_num;
