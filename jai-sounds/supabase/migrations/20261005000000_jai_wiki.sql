-- JAI Sounds · el wiki: el dial, MusicBrainz, lo que dice el internet y
-- las reseñas
-- ---------------------------------------------------------------------
-- Cada canción, álbum y artista del dial tiene su página. Esta migración
-- le da a cada uno lo que esa página necesita, en tres capas que no se
-- mezclan:
--
--   DATO        Spotify (ya estaba) + MusicBrainz por ISRC: géneros,
--               primera edición, créditos, país, miembros, enlaces.
--   EL INTERNET Lo que dicen otros (hoy: Wikipedia), siempre citado y
--               enlazado. Nunca se presenta como voz de JAI.
--   JAI         La reseña propia. Se escribe en Obsidian, fuera del repo
--               (que es público), y solo sube la que está `publicada`.
--
-- Igual que la migración inicial: todo vive en `jai`, lectura pública,
-- escritura solo para jai_ingest. La excepción son las reseñas: el
-- público lee únicamente las publicadas, aunque por error suba un
-- borrador.
-- ---------------------------------------------------------------------

-- ── El dial ──────────────────────────────────────────────────────────
-- Qué playlists son estaciones públicas. La lista vive en git
-- (content/jai-sounds/playlists.json); la ingesta con --dial la marca
-- aquí, junto con el slug, para que el wiki pueda filtrar por ella.
alter table jai.playlists add column if not exists en_dial boolean not null default false;
alter table jai.playlists add column if not exists slug text;
create unique index if not exists playlists_slug_idx on jai.playlists (slug) where slug is not null;

-- ── Slugs: las URLs del wiki ─────────────────────────────────────────
-- Se asignan una vez y no cambian (scripts/slugs.mjs): un enlace que
-- alguien guardó tiene que seguir llevando a la misma página aunque el
-- nombre en Spotify cambie de mayúsculas.
alter table jai.artists add column if not exists slug text;
alter table jai.albums  add column if not exists slug text;
alter table jai.tracks  add column if not exists slug text;
create unique index if not exists artists_slug_idx on jai.artists (slug) where slug is not null;
create unique index if not exists albums_slug_idx  on jai.albums  (slug) where slug is not null;
create unique index if not exists tracks_slug_idx  on jai.tracks  (slug) where slug is not null;

-- ── MusicBrainz ──────────────────────────────────────────────────────
-- Spotify ya no da géneros ni créditos; MusicBrainz sí, por ISRC (y por
-- título + artista cuando el ISRC no está registrado allá).
alter table jai.artists add column if not exists mbid uuid;
create index if not exists artists_mbid_idx on jai.artists (mbid);
alter table jai.albums add column if not exists mb_release_group uuid;

create table if not exists jai.mb_recordings (
  track_id         text primary key references jai.tracks (id) on delete cascade,
  -- null = se buscó y MusicBrainz no la tiene. Se guarda igual, para no
  -- volver a preguntar en cada corrida.
  mbid             uuid,
  via              text check (via in ('isrc', 'busqueda')),
  -- La fecha de Spotify suele ser la del reissue o la compilación
  -- («The Sound of Silence», 1968 en Spotify; salió en 1966).
  primera_edicion  text,
  generos          text[] not null default '{}',
  tags             text[] not null default '{}',
  creditos         jsonb  not null default '[]',  -- [{rol, atributos[], nombre, mbid}]
  obras            jsonb  not null default '[]',  -- [{titulo, mbid}]
  ediciones        jsonb  not null default '[]',  -- release groups: [{id, titulo, tipo, fecha}]
  consultado_en    timestamptz not null default now()
);

create table if not exists jai.mb_artists (
  mbid            uuid primary key,
  nombre          text not null,
  tipo            text,           -- Person, Group, Orchestra…
  pais            text,
  area            text,
  origen          text,           -- begin-area: dónde nació o se formó
  inicio          text,
  fin             text,
  desambiguacion  text,
  generos         text[] not null default '{}',
  tags            text[] not null default '{}',
  miembros        jsonb  not null default '[]',  -- [{nombre, mbid, desde, hasta}]
  integrante_de   jsonb  not null default '[]',  -- [{nombre, mbid}]
  wikidata        text,
  wikipedia       text,
  discogs         text,
  bandcamp        text,
  web             text,
  consultado_en   timestamptz not null default now()
);

-- ── Esto dice el internet ────────────────────────────────────────────
create table if not exists jai.internet (
  entidad        text not null check (entidad in ('artista', 'album', 'cancion')),
  entidad_id     text not null,   -- id de Spotify de la entidad
  fuente         text not null,   -- 'wikipedia'
  idioma         text,
  titulo         text,
  extracto       text not null,
  url            text not null,
  licencia       text,            -- 'CC BY-SA 4.0'
  consultado_en  timestamptz not null default now(),
  primary key (entidad, entidad_id, fuente)
);

-- ── La reseña JAI ────────────────────────────────────────────────────
create table if not exists jai.resenas (
  entidad         text not null check (entidad in ('artista', 'album', 'cancion')),
  entidad_id      text not null,
  cuerpo          text not null,  -- markdown, tal como está en la nota
  estado          text not null default 'borrador' check (estado in ('borrador', 'publicada')),
  publicada_en    timestamptz,
  actualizada_en  timestamptz not null default now(),
  nota            text,           -- ruta de la nota dentro del vault, para volver a ella
  primary key (entidad, entidad_id)
);

-- ── RLS ──────────────────────────────────────────────────────────────
do $$
declare t text;
begin
  foreach t in array array['mb_recordings', 'mb_artists', 'internet'] loop
    execute format('alter table jai.%I enable row level security', t);
    execute format('drop policy if exists %I on jai.%I', 'lectura_publica', t);
    execute format('create policy %I on jai.%I for select to anon, authenticated using (true)', 'lectura_publica', t);
    execute format('drop policy if exists %I on jai.%I', 'escritura_ingesta', t);
    execute format('create policy %I on jai.%I for all to jai_ingest using (true) with check (true)', 'escritura_ingesta', t);
  end loop;
end $$;

alter table jai.resenas enable row level security;
drop policy if exists lectura_publicadas on jai.resenas;
create policy lectura_publicadas on jai.resenas
  for select to anon, authenticated using (estado = 'publicada');
drop policy if exists escritura_ingesta on jai.resenas;
create policy escritura_ingesta on jai.resenas
  for all to jai_ingest using (true) with check (true);

grant select on jai.mb_recordings, jai.mb_artists, jai.internet, jai.resenas to anon, authenticated;
grant select, insert, update, delete on jai.mb_recordings, jai.mb_artists, jai.internet, jai.resenas to jai_ingest;

-- ── service_role: la llave de los scripts ────────────────────────────
-- Los scripts escriben por la API con la service_role key. Esa llave se
-- salta la RLS, pero NO los permisos: en un esquema propio (no `public`)
-- Supabase no se los concede solo, y sin esto la primera escritura da
-- «permission denied for schema jai».
grant usage on schema jai to service_role;
grant all on all tables in schema jai to service_role;
alter default privileges in schema jai grant all on tables to service_role;
