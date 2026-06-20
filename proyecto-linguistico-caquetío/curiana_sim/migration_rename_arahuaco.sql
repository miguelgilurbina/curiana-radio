-- Migración: renombrar pct_arahuacano → pct_proto_arahuaco
-- Ejecutar en Supabase Dashboard → SQL Editor

ALTER TABLE agent_responses
  RENAME COLUMN pct_arahuacano TO pct_proto_arahuaco;

-- Nueva columna: dominio semántico del léxico (eje distinto a category/POS).
-- Poblada por seed_lexicon() desde el campo "categoria" de VOCABULARIO_BASE.
ALTER TABLE lexicon
  ADD COLUMN IF NOT EXISTS semantic_domain TEXT;

DROP VIEW IF EXISTS language_drift_by_turn;
CREATE VIEW language_drift_by_turn AS
SELECT
  t.run_id,
  t.day,
  t.turn_num,
  AVG(ar.pct_caquetio)       AS avg_caquetio,
  AVG(ar.pct_wayunaiki)      AS avg_wayunaiki,
  AVG(ar.pct_lokono)         AS avg_lokono,
  AVG(ar.pct_taino)          AS avg_taino,
  AVG(ar.pct_proto_arahuaco) AS avg_proto_arahuaco
FROM turns t
JOIN agent_responses ar ON ar.turn_id = t.id
GROUP BY t.run_id, t.day, t.turn_num
ORDER BY t.run_id, t.day, t.turn_num;
