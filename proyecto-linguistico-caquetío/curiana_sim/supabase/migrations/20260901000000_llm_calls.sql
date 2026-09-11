-- El libro de costos (curiana_costos.py, 2026-09-01). Hasta aquí el motor
-- descartaba `usage`: 23 runs en la base y ninguno sabe cuánto costó. Una fila
-- por llamada al modelo — agente, rescate intra-turno, director, observer —
-- para que el costo por día y por episodio se MIDA (DISENO_ERA2 §8) en vez
-- de estimarse. Los dólares no viven aquí: la vista da tokens y Python los
-- convierte con PRECIOS_USD_POR_MTOK (una tabla con fecha).

create table if not exists llm_calls (
  id                          uuid primary key default uuid_generate_v4(),
  run_id                      uuid references simulation_runs(id) on delete cascade,
  turn_id                     uuid references turns(id) on delete set null,
  tipo                        text not null,     -- agente | rescate | director | observer_*
  agent_name                  text,
  model                       text not null,
  input_tokens                int  not null default 0,
  output_tokens               int  not null default 0,
  cache_read_input_tokens     int  not null default 0,
  cache_creation_input_tokens int  not null default 0,
  day                         int,
  turn_num                    int,
  created_at                  timestamptz default now()
);

create index if not exists idx_llm_calls_run  on llm_calls(run_id);
create index if not exists idx_llm_calls_tipo on llm_calls(run_id, tipo);

alter table llm_calls enable row level security;
drop policy if exists "public read llm_calls" on llm_calls;
create policy "public read llm_calls" on llm_calls for select using (true);
grant select on llm_calls to anon, authenticated;
grant all    on llm_calls to service_role;

-- Tokens por run. Sin dólares a propósito (ver cabecera).
create or replace view run_token_usage
with (security_invoker = true) as
select
  run_id,
  count(*)                                          as llamadas,
  count(*) filter (where tipo = 'rescate')          as rescates,
  sum(input_tokens)                                 as input_tokens,
  sum(output_tokens)                                as output_tokens,
  sum(cache_read_input_tokens)                      as cache_read_input_tokens,
  sum(cache_creation_input_tokens)                  as cache_creation_input_tokens,
  count(distinct day)                               as dias
from llm_calls
group by run_id;
