# Hoja de ruta — limpieza de lint

> **Contexto.** Al reparar el setup de lint (Next 16 eliminó `next lint` → migración a
> ESLint 9 flat config, ver commit `fix(lint): reparar setup roto por Next 16`), el linter
> volvió a correr y afloraron **22 problemas preexistentes** que estuvieron invisibles
> mientras `next lint` estaba roto. Este documento los registra y prioriza.
>
> **Rama:** `chore/lint-cleanup` (apilada sobre `fix/eslint-flat-config`, que trae el config
> funcionando; hacer merge del fix primero, luego rebasar esta rama sobre `main`).
>
> **Estado inicial:** `npm run lint` → **17 errores, 5 warnings** en 7 archivos.
> Meta: `npm run lint` sin errores (warnings a criterio).

## Resumen por regla

| Regla | Cantidad | Sev | Naturaleza |
|---|---|---|---|
| `@typescript-eslint/no-explicit-any` | 9 | error | Tipado |
| `@typescript-eslint/no-unused-vars` | 5 | warn | Limpieza |
| `react/no-unescaped-entities` | 4 | error | JSX / cosmético |
| `@next/next/no-html-link-for-pages` | 1 | error | Navegación (UX real) |
| `react-hooks/immutability` | 1 | error | **Bug real** |
| `react/jsx-no-comment-textnodes` | 1 | error | JSX |
| `react-hooks/static-components` | 1 | error | **Bug real (perf/remount)** |

## Plan por olas (orden sugerido)

### Ola 1 — Bugs reales (no es cosmética; arreglar primero)

- [ ] **`app/not-found.tsx:65` — `react-hooks/immutability`**
      `seleccionarSabiduria` se invoca dentro de un `useEffect` (línea 65) **antes** de
      declararse (línea 68). La captura temprana no se actualiza. Fix: mover la
      declaración de la función arriba del `useEffect`, o envolverla en `useCallback` y
      declararla antes. Verificar que el mensaje aleatorio siga apareceindo al montar.
- [ ] **`components/simulador/LexiconDiccionario.tsx:220` — `react-hooks/static-components`**
      Se crea un componente durante el render (se redefine en cada render → remonta el
      subárbol, pierde estado/foco). Fix: extraer ese componente fuera del componente
      padre (a nivel de módulo) y pasarle props.

### Ola 2 — Correctness / UX (reglas de Next y React)

- [ ] **`app/[edition]/page.tsx:149` — `@next/next/no-html-link-for-pages`**
      `<a href="/archivo/">` → usar `<Link href="/archivo/">` de `next/link` (navegación
      client-side, prefetch).
- [ ] **`app/not-found.tsx:100` — `react/jsx-no-comment-textnodes`**
      Comentario suelto que se renderiza como texto. Envolver en `{/* ... */}` o eliminar.
- [ ] **`react/no-unescaped-entities` (4)** — comillas sin escapar en JSX:
  - `app/not-found.tsx:119` (x2)
  - `app/simulador/personajes/page.tsx:40` (x2)
      Fix: usar `&ldquo;`/`&rdquo;`/`&quot;` o mover el texto a una constante/expresión.

### Ola 3 — Tipado (`no-explicit-any`, 9)

Empezar por el tipo raíz; probablemente cascada al resto.

- [ ] **`types/edition.ts:68`, `:69`** — definir los tipos reales que hoy son `any`.
      Es el archivo de tipos de "edition"; tiparlo bien seguramente arregla varios de los
      `any` de `app/[edition]/page.tsx`.
- [ ] **`app/[edition]/page.tsx:10-15`** (6 `any`) — reemplazar por los tipos de
      `types/edition.ts` una vez definidos.
- [ ] **`lib/content.ts:65`** — tipar el retorno/parámetro que hoy es `any`.

### Ola 4 — Limpieza (warnings, `no-unused-vars`, 5)

- [ ] `app/[edition]/page.tsx:4` — import `Navigation` sin usar → eliminar.
- [ ] `app/[edition]/page.tsx:5` — import `Caption` sin usar → eliminar.
- [ ] `app/not-found.tsx:19` — const `BURRO_ASCII` sin usar → eliminar o usar.
- [ ] `app/not-found.tsx:29` — const `BURRO_PERFIL` sin usar → eliminar o usar.
- [ ] `app/simulador/lexicon/page.tsx:15` — param `_id` sin usar.
      **Decisión de config:** el prefijo `_` sugiere intención de "ignorado". Si es un
      patrón que se repetirá, considerar añadir al flat config
      `argsIgnorePattern: "^_"` / `varsIgnorePattern: "^_"` en las rules de
      `@typescript-eslint/no-unused-vars`, en vez de tocar cada caso.

## Detalle crudo (referencia)

```
app/[edition]/page.tsx
  warn 4:8    no-unused-vars           'Navigation' sin usar
  warn 5:36   no-unused-vars           'Caption' sin usar
  ERR  10:15  no-explicit-any
  ERR  11:15  no-explicit-any
  ERR  12:15  no-explicit-any
  ERR  13:15  no-explicit-any
  ERR  14:14  no-explicit-any
  ERR  15:23  no-explicit-any
  ERR  149:13 no-html-link-for-pages   <a href="/archivo/"> → <Link>

app/not-found.tsx
  warn 19:7   no-unused-vars           'BURRO_ASCII' sin usar
  warn 29:7   no-unused-vars           'BURRO_PERFIL' sin usar
  ERR  65:5   react-hooks/immutability variable usada antes de declararse
  ERR  100:75 jsx-no-comment-textnodes
  ERR  119:13 no-unescaped-entities
  ERR  119:23 no-unescaped-entities

app/simulador/lexicon/page.tsx
  warn 15:44  no-unused-vars           '_id' sin usar

app/simulador/personajes/page.tsx
  ERR  40:15  no-unescaped-entities
  ERR  40:29  no-unescaped-entities

components/simulador/LexiconDiccionario.tsx
  ERR  220:12 react-hooks/static-components  componente creado en render

lib/content.ts
  ERR  65:28  no-explicit-any

types/edition.ts
  ERR  68:14  no-explicit-any
  ERR  69:32  no-explicit-any
```

## Verificación al cerrar

```bash
npm run lint          # objetivo: 0 errores
```
