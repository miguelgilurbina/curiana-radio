-- Migración: renombrar pct_arahuacano → pct_proto_arahuaco
-- Ejecutar en Supabase Dashboard → SQL Editor

ALTER TABLE agent_responses
  RENAME COLUMN pct_arahuacano TO pct_proto_arahuaco;

-- Nueva columna: dominio semántico del léxico (eje distinto a category/POS).
-- Poblada por seed_lexicon() desde el campo "categoria" de VOCABULARIO_BASE.
ALTER TABLE lexicon
  ADD COLUMN IF NOT EXISTS semantic_domain TEXT;

-- Recrea las vistas con security_invoker = true para que respeten el RLS
-- del usuario que consulta (no el del creador). Resuelve los warnings
-- "View is defined with the SECURITY DEFINER property" del linter de Supabase.
-- Definición completa idéntica a supabase_schema.sql (incluye moment, season,
-- avg_score y agents_active, que el dashboard espera en LanguageDriftRow).
DROP VIEW IF EXISTS language_drift_by_turn;
CREATE VIEW language_drift_by_turn
WITH (security_invoker = true) AS
SELECT
  t.run_id,
  t.day,
  t.turn_num,
  t.moment,
  t.season,
  ROUND(AVG(ar.pct_caquetio)::NUMERIC,       3) AS avg_caquetio,
  ROUND(AVG(ar.pct_wayunaiki)::NUMERIC,      3) AS avg_wayunaiki,
  ROUND(AVG(ar.pct_lokono)::NUMERIC,         3) AS avg_lokono,
  ROUND(AVG(ar.pct_taino)::NUMERIC,          3) AS avg_taino,
  ROUND(AVG(ar.pct_proto_arahuaco)::NUMERIC, 3) AS avg_proto_arahuaco,
  ROUND(AVG(ar.score)::NUMERIC,              2) AS avg_score,
  COUNT(ar.id)                                  AS agents_active
FROM turns t
JOIN agent_responses ar ON ar.turn_id = t.id
GROUP BY t.run_id, t.day, t.turn_num, t.moment, t.season
ORDER BY t.run_id, t.day, t.turn_num;

DROP VIEW IF EXISTS top_words_by_agent;
CREATE VIEW top_words_by_agent
WITH (security_invoker = true) AS
SELECT
  wu.run_id,
  wu.agent_name,
  wu.word,
  wu.source_language,
  COUNT(*) AS use_count
FROM word_uses wu
GROUP BY wu.run_id, wu.agent_name, wu.word, wu.source_language
ORDER BY wu.run_id, wu.agent_name, use_count DESC;
