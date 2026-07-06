-- Métricas de convergencia adicionales por día (ver curiana_koine.py):
--   distance          → acumulada (histórica; converge por acumulación del
--                       vocabulario base compartido — sesgada a converger)
--   distance_ventana  → sobre los últimos turnos de habla real (sin semillas)
--   distance_emergente→ ventana excluyendo el vocabulario base: solo formas
--                       emergentes (neologismos/adopciones) — la señal de
--                       koineización menos sesgada.
-- NULL = datos insuficientes ese día (< 2 agentes con vocabulario suficiente).

alter table koine_metrics add column if not exists distance_ventana numeric;
alter table koine_metrics add column if not exists distance_emergente numeric;
