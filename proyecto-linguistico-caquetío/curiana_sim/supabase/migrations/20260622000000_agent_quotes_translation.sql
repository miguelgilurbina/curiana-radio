-- ══════════════════════════════════════════════════════════════════════
-- agent_quotes.translation — traducción/glosa al español de cada frase
-- curada. Hasta ahora solo existía `justificacion` (por qué el analista
-- la eligió, no qué significa). Sin esto la sección pública de
-- Personajes no puede mostrar qué dice la frase en caquetío.
-- ══════════════════════════════════════════════════════════════════════

ALTER TABLE agent_quotes ADD COLUMN IF NOT EXISTS translation TEXT;
