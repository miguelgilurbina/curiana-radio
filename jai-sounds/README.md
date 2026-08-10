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

### 2. Registrar la app en Spotify

En <https://developer.spotify.com/dashboard> → **Create app**:

| Campo | Valor |
|---|---|
| App name | `JAI Sounds` (cualquiera) |
| Redirect URI | `http://127.0.0.1:8888/callback` |
| API | marcar **Web API** |

> **`localhost` NO sirve.** Spotify prohíbe ese hostname como redirect URI
> desde abril de 2025 y exige el literal de loopback `127.0.0.1`. Usar
> `localhost` da `INVALID_CLIENT: Insecure redirect URI` y es el error más
> común al montar esto.

Después, en *Settings*, copiar el Client ID y el Client secret.

### 3. Credenciales, fuera de OneDrive

```bash
export SPOTIFY_CLIENT_ID=...
export SPOTIFY_CLIENT_SECRET=...
export SUPABASE_URL=...
export SUPABASE_SERVICE_ROLE_KEY=...
```

> **No escribir estos valores en ningún archivo del repo**, ni en un `.env`
> gitignoreado: el proyecto vive dentro de OneDrive y cualquier archivo se
> sincroniza a la nube igual. Un sitio seguro es `~/.secrets/jai.env`, que
> queda fuera del árbol sincronizado.

### 4. Iniciar sesión (una sola vez)

```bash
node jai-sounds/scripts/ingest_spotify.mjs --login
```

Imprime una URL, la abres, aceptas, y el script recoge el callback en
`127.0.0.1:8888`. El `refresh_token` queda en `~/.secrets/jai-spotify-token.json`
—nunca en el repo— y a partir de ahí todo funciona sin volver a pedirlo.

Scopes: `playlist-read-private`, `playlist-read-collaborative`,
`user-library-read`. Solo lectura: el script no puede modificar nada en la
cuenta.

### 5. Ver qué hay

```bash
node jai-sounds/scripts/ingest_spotify.mjs --listar
```

Lista **todas** las playlists de la cuenta —incluidas privadas y
colaborativas— con nombre, id y nº de pistas, sin escribir nada. De aquí
salen los moods reales para `content/jai-sounds/moods.json`.

### 6. Ingesta

```bash
node jai-sounds/scripts/ingest_spotify.mjs --sync --todas --dry-run
```

```bash
node jai-sounds/scripts/ingest_spotify.mjs --sync --todas
```

Modos de `--sync`:

| Forma | Qué ingesta |
|---|---|
| `--sync` | Las playlists declaradas en `moods.json` |
| `--sync <url\|id> …` | Solo esas |
| `--sync --todas` | Todas las de la cuenta |
| `--sync --guardadas` | Añade "Canciones que te gustan" (`/me/tracks`) |

Salta las playlists que no cambiaron comparando `snapshot_id`; `--force` las
re-ingesta igual. `--dry-run` no escribe nada.

---

## Sin sesión de usuario

Si no se corre `--login`, el script cae a **Client Credentials**: solo lee
playlists públicas por id, y `--listar`, `--todas` y `--guardadas` no están
disponibles (no hay usuario del que hablar). Sirve para inspeccionar listas
ajenas, no para ingestar un archivo propio.

---

## Estado

- [x] Esquema del catálogo + RLS
- [x] Script de ingesta (listar / inspect / sync / dry-run / snapshot)
- [x] Login de usuario (Authorization Code) para leer privadas y `/me/*`
- [x] Portada del dial en `/jai-sounds`
- [x] Propuestas de UI sobre datos de muestra en `/jai-sounds/muestra`
- [ ] Taxonomía real (hoy hay seis moods de andamio, marcados `borrador`)
- [ ] Páginas de mood `/jai-sounds/[mood]`
- [ ] Fichas de artista y navegación por cruces de género
- [ ] Notas curatoriales por pista (`jai_curation`)
