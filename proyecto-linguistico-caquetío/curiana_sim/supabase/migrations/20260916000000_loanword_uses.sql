-- Los préstamos de la esfera de contacto, medidos aparte (decisión de Miguel
-- 2026-09-15, 6-fusion/decisiones_tanda_2026-09-15.yaml §p3b: «se debe medir
-- aparte»). Desde entonces score_linguistico() separa la voz taína, kalinago,
-- paraujana, caribe continental o jirajaroide (`prestamos_de_esfera`) de la
-- fuga a wayunaiki/lokono, y no la penaliza. Pero la base no la guardaba:
-- `word_uses` es la huella de `palabras_caquetias` —sólo caquetío desde el
-- 2026-09-09— y ningún lector suyo filtra por lengua; y `words_used` alimenta
-- las columnas pct_* de agent_responses, que no se mueven a mitad de serie.
-- Medido en el run c6837386 (2026-09-16): un préstamo usado por un tier 1
-- jamás llegaba a la base, y la difusión (¿pasa del tier 1, el único que ve el
-- bloque [Voces de fuera], al 2 y al 3?) había que leerla re-puntuando
-- response_text a mano. Una fila por voz y respuesta; tier, día y turno van
-- puestos (en word_uses quedan NULL) porque son la pregunta de la tabla.

create table if not exists loanword_uses (
  id              uuid primary key default uuid_generate_v4(),
  response_id     uuid references agent_responses(id) on delete cascade,
  run_id          uuid references simulation_runs(id) on delete cascade,
  turn_id         uuid references turns(id) on delete cascade,
  word            text not null,
  source_language text,              -- la lengua REAL de la voz (taíno, kalinago…)
  agent_name      text,
  tier            int,
  day             int,
  turn_num        int,
  created_at      timestamptz default now()
);

create index if not exists idx_loanword_uses_run  on loanword_uses(run_id);
create index if not exists idx_loanword_uses_word on loanword_uses(run_id, word);
create index if not exists idx_loanword_uses_tier on loanword_uses(run_id, tier, day);

alter table loanword_uses enable row level security;
drop policy if exists "public read loanword_uses" on loanword_uses;
create policy "public read loanword_uses" on loanword_uses for select using (true);
grant select on loanword_uses to anon, authenticated;
grant all    on loanword_uses to service_role;
