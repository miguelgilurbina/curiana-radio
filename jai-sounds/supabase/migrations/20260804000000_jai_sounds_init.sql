-- JAI Sounds · esquema inicial del catálogo
-- ---------------------------------------------------------------------
-- Qué vive aquí y qué NO:
--   AQUÍ  → el catálogo: lo que Spotify afirma sobre pistas, artistas y
--           playlists. Datos, volumen, re-sincronizables. Si se pierden se
--           recuperan corriendo la ingesta otra vez.
--   EN GIT → la taxonomía: moods, cruces de género, notas curatoriales.
--           Criterio, no dato. Vive en content/jai-sounds/moods.json porque
--           se revisa en un diff, como se revisa un texto.
--
-- El puente entre ambos es jai_curation (abajo) y el array `playlists` de
-- cada mood en el JSON.
--
-- Nota histórica: Spotify deprecó /audio-features el 2024-11-27 (403 para
-- toda app nueva). Por eso NO hay columnas valence/energy/danceability: no
-- son recuperables y fingir que existen sería mentirle al esquema.

-- ── Artistas ─────────────────────────────────────────────────────────
create table if not exists jai_artists (
  id              text primary key,              -- Spotify artist id
  name            text not null,
  spotify_genres  text[],                        -- lo que AFIRMA Spotify; puede venir vacío
  popularity      int,
  image_url       text,
  synced_at       timestamptz not null default now()
);

-- ── Pistas ───────────────────────────────────────────────────────────
create table if not exists jai_tracks (
  id                      text primary key,      -- Spotify track id
  name                    text not null,
  album_name              text,
  album_image_url         text,
  -- Spotify da precisión variable: '1998', '1998-04' o '1998-04-12'. Se
  -- guarda como texto + su precisión en vez de forzar una date falsa.
  release_date            text,
  release_date_precision  text check (release_date_precision in ('year','month','day')),
  duration_ms             int,
  isrc                    text,                  -- identidad estable entre plataformas
  popularity              int,
  spotify_url             text,
  synced_at               timestamptz not null default now()
);

create index if not exists jai_tracks_isrc_idx on jai_tracks (isrc);
-- Búsqueda por título en la UI (sin extensiones extra: to_tsvector simple).
create index if not exists jai_tracks_name_idx on jai_tracks using gin (to_tsvector('simple', name));

-- ── Pista ↔ artista (N:M; el orden distingue principal de feat.) ─────
create table if not exists jai_track_artists (
  track_id   text not null references jai_tracks (id) on delete cascade,
  artist_id  text not null references jai_artists (id) on delete cascade,
  position   int  not null default 0,
  primary key (track_id, artist_id)
);

create index if not exists jai_track_artists_artist_idx on jai_track_artists (artist_id);

-- ── Playlists ────────────────────────────────────────────────────────
create table if not exists jai_playlists (
  id           text primary key,                 -- Spotify playlist id
  name         text not null,
  description  text,
  image_url    text,
  track_count  int,
  -- snapshot_id cambia cuando la playlist cambia: permite saltar la
  -- re-ingesta de las que no se tocaron.
  snapshot_id  text,
  synced_at    timestamptz not null default now()
);

create table if not exists jai_playlist_tracks (
  playlist_id  text not null references jai_playlists (id) on delete cascade,
  track_id     text not null references jai_tracks (id) on delete cascade,
  position     int  not null,
  added_at     timestamptz,
  primary key (playlist_id, track_id)
);

create index if not exists jai_playlist_tracks_track_idx on jai_playlist_tracks (track_id);

-- ── Capa curatorial en base de datos ─────────────────────────────────
-- Solo lo que es POR PISTA (una nota sobre una canción concreta). La
-- taxonomía general sigue en git. mood_slug no tiene FK a propósito: su
-- fuente de verdad es el JSON, y el script de ingesta valida contra él.
create table if not exists jai_curation (
  track_id    text primary key references jai_tracks (id) on delete cascade,
  mood_slug   text,
  nota        text,
  destacado   boolean not null default false,
  updated_at  timestamptz not null default now()
);

create index if not exists jai_curation_mood_idx on jai_curation (mood_slug);

-- ── Vista de conteos ─────────────────────────────────────────────────
-- La portada necesita "cuántas pistas por playlist" sin traerse 12k filas.
create or replace view jai_playlist_counts as
  select playlist_id, count(*)::int as total
  from jai_playlist_tracks
  group by playlist_id;

-- ── RLS ──────────────────────────────────────────────────────────────
-- La anon key es PÚBLICA (va en el bundle del cliente vía NEXT_PUBLIC_*).
-- Por eso: lectura abierta para anon, escritura solo para service_role —
-- que es la que usa el script de ingesta y nunca toca el navegador.
alter table jai_artists         enable row level security;
alter table jai_tracks          enable row level security;
alter table jai_track_artists   enable row level security;
alter table jai_playlists       enable row level security;
alter table jai_playlist_tracks enable row level security;
alter table jai_curation        enable row level security;

do $$
declare t text;
begin
  foreach t in array array[
    'jai_artists','jai_tracks','jai_track_artists',
    'jai_playlists','jai_playlist_tracks','jai_curation'
  ] loop
    execute format(
      'drop policy if exists %I on %I', 'lectura_publica_' || t, t
    );
    execute format(
      'create policy %I on %I for select to anon, authenticated using (true)',
      'lectura_publica_' || t, t
    );
  end loop;
end $$;

-- La vista hereda el RLS de la tabla base (security_invoker) en vez de
-- correr con los permisos del dueño.
alter view jai_playlist_counts set (security_invoker = on);
