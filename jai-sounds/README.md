# JAI Sounds

Tercera arista de Curiana Radio, junto a las ediciones y al simulador: una
curaduría musical de ~12.000 pistas que cruzan géneros, organizada en un
**dial de moods**.

Esta carpeta es la tubería de datos (esquema + ingesta). La cara pública vive
en `app/jai-sounds/`, la capa de datos en `lib/jai-sounds.ts` y la taxonomía
en `content/jai-sounds/moods.json`.

---

## La decisión que ordena todo

**La taxonomía va en git. El catálogo va en Supabase.**

| | Qué | Dónde | Por qué |
|---|---|---|---|
| Curaduría | moods, cruces de género, notas | `content/jai-sounds/moods.json` | Es criterio, no dato. Se revisa en un diff, como un texto. |
| Catálogo | pistas, artistas, playlists | Supabase (`jai_*`) | Es volumen re-sincronizable. Si se pierde, se recupera corriendo la ingesta. |

El puente es el campo `playlists` de cada mood (qué colecciones de Spotify lo
alimentan) y la tabla `jai_curation` (notas sobre pistas concretas).

### Por qué el mood no puede salir de Spotify

El 27 de noviembre de 2024 Spotify deprecó `/audio-features`,
`/audio-analysis`, `/recommendations`, `/related-artists` y las playlists
destacadas. Cualquier app registrada después de esa fecha recibe **403**, sin
lista de espera ni ruta de acceso. En mayo de 2025 además exigió 250K usuarios
mensuales para el modo extendido.

O sea: `valence`, `energy`, `danceability` y `tempo` **no existen** para este
proyecto, y por eso no hay columnas para ellos en el esquema. No es una
carencia — es la premisa. El mood lo pone el oído y queda escrito.

Lo que sí sigue disponible: `/playlists/{id}`, `/playlists/{id}/tracks`,
`/tracks`, `/artists` — nombre, duración, ISRC, portada, popularidad y el
array `genres` del artista.

---

## Puesta en marcha

### 1. Crear las tablas

Aplicar `supabase/migrations/20260804000000_jai_sounds_init.sql` sobre el
proyecto `curiana-produccion`, desde el SQL Editor de Supabase o con la CLI.

La migración deja lectura pública (anon) y escritura solo para `service_role`,
porque la anon key viaja en el bundle del navegador.

### 2. Credenciales

Registrar una app en <https://developer.spotify.com/dashboard> y exportar las
variables **en la sesión del shell**:

```bash
export SPOTIFY_CLIENT_ID=...
export SPOTIFY_CLIENT_SECRET=...
export SUPABASE_URL=https://edygyxlcvvgnvdsqxnsm.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=...
```

> **No escribir estos valores en ningún archivo del repo**, ni en un `.env`
> gitignoreado: el proyecto vive dentro de OneDrive y cualquier archivo se
> sincroniza a la nube igual.

### 3. Descubrir las playlists reales

```bash
node jai-sounds/scripts/ingest_spotify.mjs --inspect https://open.spotify.com/playlist/XXXX
```

Imprime nombre, id y nº de pistas sin escribir nada. Con esa lista se arman
los moods de verdad en `content/jai-sounds/moods.json` y se pone
`"borrador": false`.

### 4. Ingesta

```bash
node jai-sounds/scripts/ingest_spotify.mjs --sync --dry-run
```

```bash
node jai-sounds/scripts/ingest_spotify.mjs --sync
```

Sin argumentos sueltos, lee las playlists declaradas en la taxonomía. Salta
las que no cambiaron (compara `snapshot_id`); `--force` las re-ingesta.

---

## Límite conocido del flujo actual

La ingesta usa **Client Credentials**: lee playlists públicas por id, pero no
puede listar `/me/playlists` ni abrir colecciones privadas — eso exige
Authorization Code con redirect y navegador. Si parte del archivo es privado,
hacerlo público un momento o levantar el flujo de usuario en otro PR.

---

## Estado

- [x] Esquema del catálogo + RLS
- [x] Script de ingesta (inspect / sync / dry-run / snapshot)
- [x] Portada del dial en `/jai-sounds`
- [ ] Taxonomía real (hoy hay seis moods de andamio, marcados `borrador`)
- [ ] Páginas de mood `/jai-sounds/[mood]`
- [ ] Fichas de artista y navegación por cruces de género
- [ ] Notas curatoriales por pista (`jai_curation`)
