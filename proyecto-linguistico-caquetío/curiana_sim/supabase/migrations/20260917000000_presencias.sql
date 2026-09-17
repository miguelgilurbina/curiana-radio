-- La ESCENA: dónde está cada agente en cada momento del día.
--
-- Decisión de Miguel (2026-09-17, `6-fusion/issues-pendientes/
-- existir-en-el-mundo-escena-por-lugar-2026-09-17.md` §2 capa 1): la escena
-- pone a los 63 agentes en un lugar cada momento del día, no sólo a los 12 que
-- hablan. Esta tabla es lo que hace posible el visor de repetición sobre el
-- mapa (§5b, PR 10): «un mapa con 12 de 63 no es un mundo».
--
-- Lo que había hasta hoy, medido en §1.7 sobre este mismo Postgres: ni
-- `agent_responses` ni `turns` tienen columna de lugar, así que el único modo
-- de saber dónde estaba alguien era mirar su `ubicacion_default` en el módulo
-- generado — y como `ubicaciones_override` tiene cuatro lectores y CERO
-- escrituras (§1.1), esa respuesta es exacta y es inútil: nadie se mueve nunca.
--
-- Una fila por agente y turno: 63 × 6 momentos = 378 filas por día (§2 capa 1).
-- `momento` y `nodo` van puestos, aunque se puedan deducir por join con `turns`
-- y por el elenco generado, porque son las dos columnas por las que se lee la
-- tabla —ocupación por lugar y momento, y lugares donde coinciden los dos
-- nodos— y el elenco es un módulo que se regenera: el nodo que valía el día del
-- run se congela aquí, como `loanword_uses` congela el tier.
--
-- Lo que NO lleva, y por qué:
--   · `lat`/`lon` — el diseño los proponía (§2 capa 1, opción 2), pero los 41
--     puntos del canon están en `sitios_era2.yaml`, `elenco_era2.yaml`,
--     `estructura_social_era2.yaml` y el `mapa_vivo` de `toponimos.yaml` (§5b):
--     copiarlos aquí sería un segundo canon que se desincroniza con el primero.
--     El exportador del visor los resuelve al exportar.
--   · `hablo` — se lee con un join a `agent_responses` por (turn_id,
--     agent_name), que es justo lo que mide «escenas con más de un hablante».
--
-- Y `agent_responses.lugar` queda desnormalizado a propósito (§2 capa 1, «las
-- dos»): es la columna que evita que toda consulta de lengua —`word_uses` ×
-- `turns`— tenga que unir además con `presencias`.

create table if not exists presencias (
  id          uuid primary key default uuid_generate_v4(),
  run_id      uuid references simulation_runs(id) on delete cascade,
  turn_id     uuid references turns(id) on delete cascade,
  day         int,
  turn_num    int,
  momento     text,               -- amanecer · mañana · mediodía · tarde · anochecer · noche
  agent_name  text,
  lugar       text,               -- «Tacuato», «Tacuato:orilla», «ZG2», «camino:Moruy»…
  nodo        text,               -- GUARANAO · AMUAY — el del elenco ACTIVO del run
  created_at  timestamptz default now()
);

create index if not exists idx_presencias_run   on presencias(run_id);
create index if not exists idx_presencias_turn  on presencias(turn_id);
-- La consulta de `analizar_nodos.py --lugar`: ocupación por lugar y día.
create index if not exists idx_presencias_lugar on presencias(run_id, lugar, day);

alter table presencias enable row level security;
drop policy if exists "public read presencias" on presencias;
create policy "public read presencias" on presencias for select using (true);
grant select on presencias to anon, authenticated;
grant all    on presencias to service_role;

-- El lugar de quien SÍ habló, al lado de su respuesta.
alter table agent_responses add column if not exists lugar text;
