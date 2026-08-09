-- JAI Sounds · esquema inicial del catálogo
-- ---------------------------------------------------------------------
-- Qué vive aquí y qué NO:
--   AQUÍ  → el catálogo: lo que Spotify entrega sobre pistas, álbumes,
--           artistas y playlists. Datos re-sincronizables: si se pierden,
--           se recuperan corriendo la ingesta otra vez.
--   EN GIT → la taxonomía: moods, cruces de género, notas curatoriales.
--           Criterio, no dato. Vive en content/jai-sounds/moods.json.
--
-- ---------------------------------------------------------------------
-- IMPORTANTE — este esquema solo tiene columnas que Spotify REALMENTE
-- devuelve a una app registrada hoy. Verificado contra la API en vivo el
-- 2026-08-09 con la app de este proyecto. Lo que NO está y no es olvido:
--
--   popularity      /tracks?ids= y /artists?ids= dan 403; el objeto
--                   embebido en las playlists no trae el campo.
--   generos         /artists?ids= da 403, y /artists/{id} responde 200
--                   pero YA NO incluye `genres`. No hay forma de obtener
--                   géneros de Spotify. Si el proyecto los quiere, salen
--                   de la curaduría o de otra fuente (MusicBrainz por
--                   ISRC, que sí guardamos).
--   valence/energy  /audio-features deprecado el 2024-11-27, 403.
--
-- Una columna que nunca se puede llenar es una mentira en el esquema.
-- ---------------------------------------------------------------------

-- ── Artistas ─────────────────────────────────────────────────────────
-- Se construyen de lo EMBEBIDO en cada pista: id y nombre. No hay una
-- llamada a /artists que aporte más.
create table if not exists jai_artists (
  id         text primary key,               -- Spotify artist id
  name       text not null,
  synced_at  timestamptz not null default now()
);

-- ── Álbumes ──────────────────────────────────────────────────────────
-- /albums/{id} da 404, pero el objeto álbum viene completo dentro de
-- cada pista, así que la tabla se llena igual sin pedir nada extra.
create table if not exists jai_albums (
  id                      text primary key,
  name                    text not null,
  album_type              text,              -- album | single | compilation
  -- Spotify da precisión variable: '1985', '1985-06' o '1985-06-24'. Se
  -- guarda como texto + su precisión en vez de forzar una date falsa.
  release_date            text,
  release_date_precision  text check (release_date_precision in ('year','month','day')),
  total_tracks            int,
  image_url               text,
  synced_at               timestamptz not null default now()
);

create index if not exists jai_albums_anio_idx on jai_albums (left(release_date, 4));

-- ── Pistas ───────────────────────────────────────────────────────────
create table if not exists jai_tracks (
  id            text primary key,
  name          text not null,
  album_id      text references jai_albums (id) on delete set null,
  disc_number   int,
  track_number  int,
  duration_ms   int,
  -- Identidad estable entre plataformas: es la llave para enriquecer con
  -- MusicBrainz/Discogs si algún día hacen falta géneros o créditos.
  isrc          text,
  explicit      boolean,
  spotify_url   text,
  synced_at     timestamptz not null default now()
);

create index if not exists jai_tracks_isrc_idx on jai_tracks (isrc);
create index if not exists jai_tracks_album_idx on jai_tracks (album_id);
-- Búsqueda por título en la UI (sin extensiones extra).
create index if not exists jai_tracks_name_idx on jai_tracks using gin (to_tsvector('simple', name));

-- ── Relaciones N:M (el orden distingue principal de featuring) ───────
create table if not exists jai_track_artists (
  track_id   text not null references jai_tracks (id) on delete cascade,
  artist_id  text not null references jai_artists (id) on delete cascade,
  position   int  not null default 0,
  primary key (track_id, artist_id)
);
create index if not exists jai_track_artists_artist_idx on jai_track_artists (artist_id);

create table if not exists jai_album_artists (
  album_id   text not null references jai_albums (id) on delete cascade,
  artist_id  text not null references jai_artists (id) on delete cascade,
  position   int  not null default 0,
  primary key (album_id, artist_id)
);

-- ── Playlists ────────────────────────────────────────────────────────
create table if not exists jai_playlists (
  id           text primary key,
  name         text not null,
  description  text,
  image_url    text,
  track_count  int,
  -- Cambia cuando la playlist cambia: permite saltar la re-ingesta de las
  -- que no se tocaron.
  snapshot_id  text,
  colaborativa boolean,
  publica      boolean,
  es_propia    boolean,                      -- distingue curada de seguida
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

-- ── Canciones guardadas ──────────────────────────────────────────────
-- "Canciones que te gustan" NO es una playlist y no tiene id: fingir que
-- lo es obligaría a inventar una fila falsa en jai_playlists. Tabla propia.
create table if not exists jai_saved_tracks (
  track_id  text primary key references jai_tracks (id) on delete cascade,
  added_at  timestamptz
);
create index if not exists jai_saved_tracks_added_idx on jai_saved_tracks (added_at desc);

-- ── Capa curatorial ──────────────────────────────────────────────────
-- Solo lo que es POR PISTA. La taxonomía general sigue en git; mood_slug
-- no lleva FK a propósito: su fuente de verdad es moods.json.
create table if not exists jai_curation (
  track_id    text primary key references jai_tracks (id) on delete cascade,
  mood_slug   text,
  nota        text,
  destacado   boolean not null default false,
  updated_at  timestamptz not null default now()
);
create index if not exists jai_curation_mood_idx on jai_curation (mood_slug);

-- ── Vistas de conteo ─────────────────────────────────────────────────
-- La portada necesita totales sin traerse 12k filas.
create or replace view jai_playlist_counts as
  select playlist_id, count(*)::int as total
  from jai_playlist_tracks
  group by playlist_id;

-- ── RLS ──────────────────────────────────────────────────────────────
-- La anon key es PÚBLICA (va en el bundle del cliente vía NEXT_PUBLIC_*).
-- Lectura abierta para anon; escritura solo para service_role, que es la
-- que usa el script de ingesta y nunca toca el navegador.
do $$
declare t text;
begin
  foreach t in array array[
    'jai_artists','jai_albums','jai_tracks','jai_track_artists',
    'jai_album_artists','jai_playlists','jai_playlist_tracks',
    'jai_saved_tracks','jai_curation'
  ] loop
    execute format('alter table %I enable row level security', t);
    execute format('drop policy if exists %I on %I', 'lectura_publica_' || t, t);
    execute format(
      'create policy %I on %I for select to anon, authenticated using (true)',
      'lectura_publica_' || t, t
    );
  end loop;
end $$;

-- La vista hereda el RLS de la tabla base en vez de correr con los
-- permisos del dueño.
alter view jai_playlist_counts set (security_invoker = on);
