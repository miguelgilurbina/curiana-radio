-- JAI Sounds · esquema inicial del catálogo
-- ---------------------------------------------------------------------
-- Vive en su PROPIO esquema `jai`, no en `public`, aunque comparta base de
-- datos con el simulador. El motivo no es el orden sino el privilegio:
--
--   Los datos del simulador son irreemplazables (salieron de correr agentes
--   contra un modelo). Los de JAI son desechables: se rebajan de Spotify en
--   minutos. Una ingesta masiva y desatendida no tiene por qué correr con
--   una llave capaz de tocar lo primero.
--
-- Con esquema propio, el rol de ingesta recibe permisos SOLO sobre `jai` y
-- se vuelve incapaz de escribir en `public.lexicon` o `public.word_uses`
-- aunque el script tenga un bug. Además `pg_dump -n public` y
-- `pg_dump -n jai` separan limpiamente lo caro de lo reproducible.
--
-- ---------------------------------------------------------------------
-- Qué vive aquí y qué NO:
--   AQUÍ  → el catálogo que entrega Spotify.
--   EN GIT → la taxonomía (moods, cruces, notas): criterio, no dato.
--            content/jai-sounds/moods.json
--
-- ---------------------------------------------------------------------
-- Solo hay columnas que Spotify REALMENTE devuelve a una app registrada
-- hoy. Verificado contra la API en vivo el 2026-08-09. Lo que NO está y no
-- es olvido:
--   popularity   los endpoints por lote de tracks y artists dan 403.
--   generos      el de artista responde 200 pero ya no incluye `genres`.
--                Si el proyecto los quiere, salen de la curaduría o de
--                MusicBrainz por ISRC, que sí guardamos al 100%.
--   valence      audio-features deprecado el 2024-11-27.
-- Una columna que nunca se puede llenar es una mentira en el esquema.
-- ---------------------------------------------------------------------

create schema if not exists jai;

-- ── Artistas ─────────────────────────────────────────────────────────
-- Se construyen de lo EMBEBIDO en cada pista: id y nombre. No hay llamada
-- a artistas que aporte más.
create table if not exists jai.artists (
  id         text primary key,
  name       text not null,
  synced_at  timestamptz not null default now()
);

-- ── Álbumes ──────────────────────────────────────────────────────────
-- El endpoint de álbum suelto da 404, pero el objeto viene completo dentro
-- de cada pista: la tabla se llena sin pedir nada extra.
create table if not exists jai.albums (
  id                      text primary key,
  name                    text not null,
  album_type              text,
  -- Precisión variable: '1985', '1985-06' o '1985-06-24'. Se guarda como
  -- texto + su precisión en vez de forzar una date falsa.
  release_date            text,
  release_date_precision  text check (release_date_precision in ('year','month','day')),
  total_tracks            int,
  image_url               text,
  synced_at               timestamptz not null default now()
);

create index if not exists albums_anio_idx on jai.albums (left(release_date, 4));

-- ── Pistas ───────────────────────────────────────────────────────────
create table if not exists jai.tracks (
  id            text primary key,
  name          text not null,
  album_id      text references jai.albums (id) on delete set null,
  disc_number   int,
  track_number  int,
  duration_ms   int,
  -- Identidad estable entre plataformas: la llave para enriquecer con
  -- MusicBrainz cuando hagan falta géneros o créditos.
  isrc          text,
  explicit      boolean,
  spotify_url   text,
  synced_at     timestamptz not null default now()
);

create index if not exists tracks_isrc_idx on jai.tracks (isrc);
create index if not exists tracks_album_idx on jai.tracks (album_id);
create index if not exists tracks_name_idx on jai.tracks using gin (to_tsvector('simple', name));

-- ── Relaciones N:M (el orden distingue principal de featuring) ───────
create table if not exists jai.track_artists (
  track_id   text not null references jai.tracks (id) on delete cascade,
  artist_id  text not null references jai.artists (id) on delete cascade,
  position   int  not null default 0,
  primary key (track_id, artist_id)
);
create index if not exists track_artists_artist_idx on jai.track_artists (artist_id);

create table if not exists jai.album_artists (
  album_id   text not null references jai.albums (id) on delete cascade,
  artist_id  text not null references jai.artists (id) on delete cascade,
  position   int  not null default 0,
  primary key (album_id, artist_id)
);

-- ── Playlists ────────────────────────────────────────────────────────
create table if not exists jai.playlists (
  id           text primary key,
  name         text not null,
  description  text,
  image_url    text,
  track_count  int,
  snapshot_id  text,                        -- cambia cuando cambia la lista
  colaborativa boolean,
  publica      boolean,
  es_propia    boolean,                     -- distingue curada de seguida
  synced_at    timestamptz not null default now()
);

create table if not exists jai.playlist_tracks (
  playlist_id  text not null references jai.playlists (id) on delete cascade,
  track_id     text not null references jai.tracks (id) on delete cascade,
  position     int  not null,
  added_at     timestamptz,
  primary key (playlist_id, track_id)
);
create index if not exists playlist_tracks_track_idx on jai.playlist_tracks (track_id);

-- ── Canciones guardadas ──────────────────────────────────────────────
-- "Canciones que te gustan" NO es una playlist y no tiene id: fingir que
-- lo es obligaría a inventar una fila falsa en playlists.
create table if not exists jai.saved_tracks (
  track_id  text primary key references jai.tracks (id) on delete cascade,
  added_at  timestamptz
);
create index if not exists saved_tracks_added_idx on jai.saved_tracks (added_at desc);

-- ── Capa curatorial ──────────────────────────────────────────────────
-- Solo lo que es POR PISTA. La taxonomía general sigue en git; mood_slug
-- no lleva FK a propósito: su fuente de verdad es moods.json.
create table if not exists jai.curation (
  track_id    text primary key references jai.tracks (id) on delete cascade,
  mood_slug   text,
  nota        text,
  destacado   boolean not null default false,
  updated_at  timestamptz not null default now()
);
create index if not exists curation_mood_idx on jai.curation (mood_slug);

-- ── Vista de conteo ──────────────────────────────────────────────────
create or replace view jai.playlist_counts as
  select playlist_id, count(*)::int as total
  from jai.playlist_tracks
  group by playlist_id;

-- ── Rol de ingesta ───────────────────────────────────────────────────
-- Se crea ANTES que las políticas, porque una de ellas lo nombra: en una
-- base limpia, `create policy … to jai_ingest` falla si el rol no existe.
-- Sin contraseña: se fija aparte (`alter role jai_ingest password '…'`) y
-- vive en ~/.secrets/, nunca en el repo — que se sincroniza a OneDrive.
do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'jai_ingest') then
    create role jai_ingest login;
  end if;
end $$;

-- ── RLS: lectura pública, escritura solo para la ingesta ─────────────
-- La anon key viaja en el bundle del navegador: lectura abierta, y ninguna
-- política de escritura para anon/authenticated, así que por PostgREST no
-- escribe nadie.
--
-- Ojo con el reverso: RLS también se aplica al rol de ingesta, que no es
-- dueño de las tablas. Sin una política explícita de escritura, sus INSERT
-- fallan con "new row violates row-level security policy". Se concede aquí
-- —acotada a jai_ingest y escrita en el esquema— en vez de darle el
-- atributo global BYPASSRLS, que valdría para toda la base.
do $$
declare t text;
begin
  foreach t in array array[
    'artists','albums','tracks','track_artists','album_artists',
    'playlists','playlist_tracks','saved_tracks','curation'
  ] loop
    execute format('alter table jai.%I enable row level security', t);

    execute format('drop policy if exists %I on jai.%I', 'lectura_publica', t);
    execute format(
      'create policy %I on jai.%I for select to anon, authenticated using (true)',
      'lectura_publica', t
    );

    execute format('drop policy if exists %I on jai.%I', 'escritura_ingesta', t);
    execute format(
      'create policy %I on jai.%I for all to jai_ingest using (true) with check (true)',
      'escritura_ingesta', t
    );
  end loop;
end $$;

alter view jai.playlist_counts set (security_invoker = on);

-- Para que PostgREST sirva este esquema hay que exponerlo además en la
-- config del proyecto (`[api] schemas` en config.toml / API settings).
grant usage on schema jai to anon, authenticated;
grant select on all tables in schema jai to anon, authenticated;
alter default privileges in schema jai
  grant select on tables to anon, authenticated;

-- ── Permisos de la ingesta: el punto de todo esto ────────────────────
-- Puede escribir en `jai` y en ningún otro sitio.
grant usage on schema jai to jai_ingest;
grant select, insert, update, delete on all tables in schema jai to jai_ingest;
alter default privileges in schema jai
  grant select, insert, update, delete on tables to jai_ingest;

-- Y explícitamente NADA sobre el simulador. `public` concede USAGE a
-- PUBLIC por defecto en muchas instalaciones: se revoca a propósito para
-- que este rol no pueda ni mirar lo que no le toca.
revoke all on schema public from jai_ingest;
revoke all privileges on all tables in schema public from jai_ingest;
