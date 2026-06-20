# Curiana Radio · Manual de Marca (MVP UI)

Guía mínima viable para mantener consistencia visual en **Curiana Radio** y su
**Simulador**. Pensada para que el equipo (y el código) hable un solo lenguaje.
Los colores son **intercambiables** sin tocar componentes — ver §3.

---

## 1. Esencia

> **Transmisión cultural desde Abya Yala.** 88.8 FM.

Editorial, cálido y telúrico. Tipografía con voz (serif) sobre una interfaz
limpia (sans). El acento *naranja frecuencia* es la chispa de "radio". El
Simulador es el **laboratorio lingüístico** de la misma marca: mismo sistema,
con foco en datos.

**Principios UI**
1. **Una sola familia visual.** El simulador NO es un panel aparte: vive dentro
   de la radio y usa sus tokens.
2. **Jerarquía por tipografía y espacio**, no por cajas y bordes pesados.
3. **Color con intención.** Cada color significa algo (marca, lengua, estado).
4. **Contenido primero.** Superficies sobrias, datos legibles, nada decorativo
   que compita con la información.

---

## 2. Tipografía

| Rol | Fuente | Uso |
|-----|--------|-----|
| **Display / Títulos** | **Lora** (serif) | h1–h4, números de métrica, voz editorial |
| **Interfaz / Cuerpo** | **Inter** (sans) | labels, tablas, botones, párrafos UI |
| **Mono** | system mono | componentes morfológicos, código |

- Headings siempre `font-serif` + `text-deep-900`.
- **Overline** (etiqueta de sección): Inter, `0.7rem`, `tracking-[0.18em]`,
  `uppercase`, `text-earth-600`. Componente: `<Overline>`.
- Escala (definida en `tailwind.config.ts`): `display 3.5rem`, `intro 2rem`,
  `body 1.125rem`. Line-height de lectura `1.75`, ancho óptimo `65ch`.
- Componentes existentes: `components/ui/Typography.tsx`
  (`Heading`, `BodyText`, `Quote`, `Caption`, `SectionTitle`).

---

## 3. Color (tokens intercambiables)

Hay **dos fuentes de verdad**. Cambiar un color = editar un solo lugar.

### 3.1 Paleta de marca → `app/globals.css` (+ `tailwind.config.ts`)
Se usan como utilidades Tailwind (`text-earth-600`, `bg-earth-50`, `text-frequency`…).

| Token | Hex | Rol |
|-------|-----|-----|
| `earth-50 … 900` | `#f8f6f3 → #4f3e35` | neutros cálidos: fondos, bordes, texto suave |
| `deep-50 … 900` | `#f0f4f8 → #0f1621` | azul profundo: títulos, texto fuerte, datos |
| `frequency` | `#FF6B35` | **acento**: CTA, "en vivo", resaltados, foco |

> Para recolorar la marca: edita los `--color-*` en `app/globals.css` **y** el
> espejo en `tailwind.config.ts`.

### 3.2 Color de datos / semántico del Simulador → `lib/sim-theme.ts`
Única fuente para todo lo que el simulador pinta con color "de significado".

| Grupo | Tokens | Nota |
|-------|--------|------|
| **Lenguas** (`LANGS`) | caquetío `#C47A2B` · wayunaiki `#2E7D4F` · lokono `#5B4FCF` · taíno `#B04040` · proto-arahuaco `#6D8A9E` | colores de DATOS; el orden = pila del chart |
| **Estados neologismo** (`NEO_STATUS`) | propuesto `#6D8A9E` · adoptado `#2E7D4F` · rechazado `#B04040` · ignorado `#9d7f66` | |
| **Semánticos** (`SEMANTIC`) | success `#2E7D4F` · warning `#C47A2B` · danger `#B04040` | usados por `scoreColor()` |

> Para recolorar el simulador: edita `lib/sim-theme.ts`. Propaga a chart, feed,
> pills, tablas y badges automáticamente (ningún componente hardcodea estos hex).

### 3.3 Contraste / accesibilidad
- Texto cuerpo: `text-deep-800` / `text-earth-700` sobre superficies claras.
- Texto apagado mínimo `text-earth-600` (evitar `earth-400/500` para texto).
- Foco visible global: outline `frequency` (definido en `globals.css`).

---

## 4. Espacio, radio y elevación

- **Ritmo de espaciado:** múltiplos de 4 — `gap-4`, `p-5/6`, `mt-6`, `mb-8`.
- **Contenedor:** `max-w-6xl mx-auto px-4 sm:px-6 lg:px-8` (simulador).
- **Radios:** tarjetas `rounded-2xl`; pills `rounded-full`; inputs `rounded-lg`.
- **Elevación:** `shadow-sm` en reposo, `hover:shadow-md` en tarjetas
  interactivas. Sin sombras duras.
- **Bordes:** `border-earth-200/70` (sutiles), nunca negros.

---

## 5. Componentes (inventario)

Primitivas del simulador en `components/simulador/ui.tsx`:

| Componente | Uso |
|------------|-----|
| `Card` | superficie base (cream translúcido, borde sutil, sombra) |
| `StatCard` | métrica: overline + número serif grande + sub |
| `Overline` | etiqueta de sección |
| `ScoreGauge` | barra 0–10 con color por umbral (`scoreColor`) |
| `LangPill` | pastilla de lengua/estado con su color |
| `LiveDot` | indicador en vivo / conectando / sin conexión |
| `Skeleton` | placeholder de carga |
| `EmptyState` | estado vacío con copy |
| `SubNav` | pestañas con estado activo (subrayado `frequency`) |

**Patrones**
- **Loading:** siempre `Skeleton`, nunca texto "Cargando…".
- **Vacío:** `EmptyState` con título serif + pista en sans.
- **Botón primario:** `bg-frequency text-white` (o variante outline en CTA
  secundarios). Mayúsculas con `tracking-[0.2em]` para CTAs editoriales.

---

## 6. Voz y tono

- Español neutro, cálido, culto sin ser solemne.
- Títulos evocadores ("Voces de la Curiana", "Palabras nuevas"); labels
  funcionales y cortos.
- Respetar la lengua: *caquetío-arahuaco*, *Golfete de Coro*, s. XIV–XV.

---

## 7. Checklist de revisión (antes de hacer merge de UI)

- [ ] ¿Títulos en `font-serif`? ¿overlines como `<Overline>`?
- [ ] ¿Colores desde tokens (`sim-theme.ts` / utilidades Tailwind), sin hex sueltos?
- [ ] ¿`Card` para superficies y `rounded-2xl`/`shadow-sm` consistentes?
- [ ] ¿Estados de carga (`Skeleton`) y vacío (`EmptyState`)?
- [ ] ¿Contraste suficiente del texto apagado?
- [ ] ¿Responsive? (grids colapsan, tablas con scroll, nav envuelve)
- [ ] ¿Foco visible en interactivos?

---

*MVP — iteraremos. La paleta es provisional y está pensada para cambiarse;
toda la lógica de color ya está centralizada (§3) para hacerlo en minutos.*
