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

Seis voces, cada una con un trabajo. Regla corta: **el cartel grita, el
oráculo susurra, el dato teclea.**

| Voz | Fuente | Uso |
|-----|--------|-----|
| **Cartel (display)** | **Archivo Black** + `scaleX(0.82)` | rótulos de sección, titulares cortos, sellos, títulos de edición |
| **Oráculo** | **Lora** itálica | manifiesto, citas, proverbios, subtítulos |
| **Editorial** | **Lora** 600 | titulares largos, prosa destacada; h1–h4 por defecto |
| **Cuerpo / UI** | **Inter** | párrafos, nav, labels, tablas, botones |
| **Dato** | system mono (`ui-monospace` stack) | timestamps, frecuencias, metadatos, ASCII, componentes morfológicos |
| **Arte editorial** | **Fraunces** `SOFT 0 / WONK 1` | Simulador, JAI Sounds, arcos «presenta» (`.sim-display`) |

### 2.1 El cartel: "type 3c" (decisión de las sesiones de diseño, 2026-09)

El registro de cartel del lockup CURIANA/RADIO entra al sistema como display,
replicado con **Archivo Black comprimida artificialmente**. La compresión ES
la identidad: sin ella es otra fuente.

```css
/* globals.css */
.cartel { font-family: var(--font-cartel); font-weight: 400; text-transform: uppercase;
          letter-spacing: -0.02em; transform: scaleX(0.82); transform-origin: left;
          display: inline-block; white-space: nowrap; }
.cartel-hero     { transform: scaleX(0.78); }  /* "CURIANA RADIO" completo en heros */
.cartel-centrado { transform-origin: center; }
```

Componente: `<Cartel as="h2" hero centrado>` en `components/ui/Typography.tsx`.
La fuente se self-hostea con `next/font` (`--font-archivo-black`, `app/layout.tsx`).

**Reglas de uso**
- Solo **rótulos y sellos de 1–3 palabras**. En textos largos que envuelven, la
  compresión por transform se nota y degrada → Lora 600 (plan B para titulares
  largos si el transform diera problemas: Oswald 700).
- **El lockup PNG sigue siendo el logo oficial** (`public/marca/lockup-bnw.png`).
  El cartel es la voz de cartel del sistema, no un reemplazo del arte: donde
  haya espacio y resolución, va el PNG.
- **Se tinta por superficie** (cableado en `globals.css`): `deep-900` en la
  radio · `--sim-rubrica` en Kaketiana/Simulador · `--jai-senal` en JAI.
  Galería (`--gal-luz`) y Buchibe (`--buc-oro`) entran cuando esas superficies
  existan como tema.
- **Lo oracular NUNCA va en cartel**: manifiesto, citas y proverbios siguen en
  Lora itálica. Los datos siguen en mono.
- El transform no cambia el layout: la caja mide el ancho sin comprimir. Para
  centrar, `centrado`; para alinear a la derecha, `transform-origin: right`.

Descartadas: Anton (esqueleto cercano, menos tosco), Oswald 700 (más prensa
que cartel), Passion One 900 (demasiado retro-cartel).

### 2.2 Detalles heredados
- Headings por defecto `font-serif` + `text-deep-900` (voz editorial).
- **Overline** (etiqueta de sección): Inter, `0.7rem`, `tracking-[0.18em]`,
  `uppercase`, `text-earth-600`. Componente: `<Overline>`.
- Escala (`tailwind.config.ts`): `display 3.5rem`, `intro 2rem`, `body 1.125rem`.
  Line-height de lectura `1.75`, ancho óptimo `65ch`.
- Componentes: `components/ui/Typography.tsx` (`Heading`, `BodyText`, `Quote`,
  `Caption`, `SectionTitle`, `Cartel`).

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
| `arte-acido` · `arte-indigo` · `arte-electrico` · `arte-ocre` · `arte-rojo` · `arte-hueso` | `#C7C91C` · `#26396A` · `#2154C5` · `#C36712` · `#B64924` · `#F3EAD4` | **tintas del arte**: el registro saturado/serigráfico (intro, carteles, ecos). Nunca para UI de lectura |
| `rubrica` | `#8F3B26` | tinta roja seca: material canónico del isotipo 3D (= `--sim-rubrica`) |
| `arcilla` | `#B8502E` | la espiral 3D sobre fondo saturado (intro) |
| `--color-intro` | `#23224F` | la noche ultramar: fondo de la intro (solo CSS) |

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
- [ ] ¿Rótulos cortos en `<Cartel>` y nada oracular (citas, proverbios) en cartel?
- [ ] ¿Colores desde tokens (`sim-theme.ts` / utilidades Tailwind), sin hex sueltos?
- [ ] ¿`Card` para superficies y `rounded-2xl`/`shadow-sm` consistentes?
- [ ] ¿Estados de carga (`Skeleton`) y vacío (`EmptyState`)?
- [ ] ¿Contraste suficiente del texto apagado?
- [ ] ¿Responsive? (grids colapsan, tablas con scroll, nav envuelve)
- [ ] ¿Foco visible en interactivos?

---

## 8. Isotipo, lockup y la espiral en bulto

Activos en `public/marca/`:

| Archivo | Qué es | Uso |
|---------|--------|-----|
| `lockup-bnw.png` | lockup oficial CURIANA/RADIO (1024²) | **el logo**; donde haya espacio y resolución |
| `isotipo-espiral.png` | isotipo 1024² | avatar, OG, piezas grandes |
| `espiral.svg` | trazado vectorial | favicon, UI pequeña. NO es la fuente del 3D |
| `isotipo-calco.png` | el PNG original del autor | **la fuente del calco 3D**: la intro lo carga en runtime |

**La espiral 3D** (`lib/espiral-3d.ts`) no es una curva paramétrica: es un
calco directo del PNG — rejilla 180², binarizado (alpha > 120 y RGB < 400),
marching squares, lazos < 24 puntos descartados, suavizado 1-2-1 ×2,
submuestreo 1/2, extrusión `depth 0.09 / bevel 0.012 · 0.01 · 3`. Fidelidad
total a las imperfecciones del dibujo. El lazo de mayor área es el disco; el
resto, agujeros (el canal espiral).

Material canónico **"arcilla rúbrica"**: `MeshStandardMaterial{ color: rubrica,
roughness ~0.55–0.62, metalness ~0.08–0.12 }`. En la intro se aclara a
`arcilla` (`roughness 0.5, metalness 0.12`) para contrastar con el fondo
saturado. La geometría se calcula una vez (~10 ms) y queda cacheada por URL.

El visor/exportador OBJ+GLB del handoff (`Espiral 3D.html`) no se portó: es
herramienta de diseño, no producto. Si hace falta un GLB, se genera desde ahí.

---

## 9. La intro (pantalla de entrada)

`components/intro/` — el visitante llega a un remolino serigráfico con la
espiral 3D al frente y un túnel de seis ecos detrás. Al pulsar
**[ SINTONIZAR → ]** el remolino se dispara (velocidad 1 → 27), la cámara
atraviesa el centro (dolly 0 → 2.35) en 1600 ms ease-out-cubic, y un velo
`arte-hueso` amanece hacia la landing. **La intro es lo saturado; la landing
que sigue es lo sobrio**: la regla de los dos registros hecha secuencia.

- Se ve **una vez por sesión** en `/` (`IntroGate`, `sessionStorage.curianaIntroVista`).
  En `/intro` se puede volver a ver (noindex).
- `prefers-reduced-motion`: shader congelado, sin giro ni flotación,
  misregistro estático; el botón entra directo sin animación.
- Sin WebGL (o sin JS) la intro degrada: índigo + UI con el botón funcionando,
  o directamente no tapa la landing.
- three.js se carga en su propio chunk, solo cuando la intro va a mostrarse.
- Capas, de atrás hacia adelante: shader (remolino posterizado a 5 niveles) →
  6 ecos planos en las tintas del arte → la espiral en arcilla con luz cálida
  `#FFB08A` y ácida → trama de semitono + scanlines (DOM) → UI (nombre en mono
  con misregistro rojo/índigo, badge 88.8, estado en ácido, botón, proverbio
  en Lora itálica) → velo.
- Timing: hover 300 ms `cubic-bezier(.22,1,.36,1)` · sintonizar 1600 ms ·
  misregistro 7 s · pulso 1.1 s `steps(2)` · amanecer 900 ms.

---

*MVP — iteraremos. La paleta es provisional y está pensada para cambiarse;
toda la lógica de color ya está centralizada (§3) para hacerlo en minutos.*
