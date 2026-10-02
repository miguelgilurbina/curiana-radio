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
| `rubrica` | `#8F3B26` | tinta roja seca (= `--sim-rubrica`) |
| `arcilla` | `#B8502E` | la espiral de arcilla (de la intro psicodélica, retirada) |

> Para recolorar la marca: edita los `--color-*` en `app/globals.css` **y** el
> espejo en `tailwind.config.ts`.

**v1 · la noche** (solo CSS, `--noche-*` en `:root`; se usan como
`bg-(--noche-fondo)`). El favicon definió el mood de la primera versión
(§8.1): la radio pasa de papel cálido a **noche en movimiento**. Todo texto de
lectura ≥ 4.5:1, apuntando a ≥ 7:1.

| Token | Hex | Rol |
|-------|-----|-----|
| `--noche-fondo` | `#0F1621` | fondo base (= deep-900) |
| `--noche-hondo` | `#07090D` | colofón, intro, velo de entrada |
| `--noche-panel` | `#131C28` | tarjetas y formularios (= `--jai-panel`) |
| `--noche-hueso` | `#EEE6D4` | texto principal y display (≈ 14:1) |
| `--noche-hueso-2` | `#C6CFD9` | texto secundario, overlines, metadatos (≈ 10:1); **nunca más tenue** |
| `--noche-filete` · `--noche-filete-fuerte` | `#3A4B61` · `#5A6D85` | bordes; puntos inactivos |
| `--noche-oro` | `#E0BB66` | el nombre de El Disco, junto al logo |
| gradiente | `#0F1621 → #1F2C3E → #131C28 → #2F425B` | `.noche-gradiente`, 15 s a 135° |

**Superficies de sección** (tokens scoped por atributo, como `data-sim-theme`
y `data-jai-theme`): `[data-galeria-theme="sala"]` → `--gal-*` (la sala
acromática, `#101010`) y `[data-buchibe-theme="telon"]` → `--buc-*` (telón
`#8C2B12`, noche ultramar, oro `#C9A05A`). Los `-faint` son solo para trazos:
el texto usa `-soft` o más claro.

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
| `lockup-bnw.png` | lockup oficial CURIANA/RADIO (1024²), tinta negra | **el logo**; donde haya espacio y resolución, sobre claro |
| `lockup-hueso.png` | el lockup en hueso con alfa (390²) | el logo sobre la noche (barra del hero) |
| `isotipo-espiral.png` | isotipo 1024², tinta sobre transparente | avatar, OG, piezas grandes; **la máscara del revelado de El Disco** |
| `isotipo-hueso.png` | el isotipo en hueso con alfa (512²) | sobre la noche: barra del hero, intro sin WebGL2 |
| `espiral.svg` | trazado vectorial | UI pequeña. NO es la fuente del favicon (§8.1) |
| `isotipo-calco.png` | el PNG original del autor | fuente del calco 3D de la intro psicodélica (retirada) |

Las versiones en hueso salen del PNG por la misma máscara que usan el favicon
y El Disco: alfa = `(255 − lum) × 1.25`, color `#EEE6D4`. **No se invierte con
`filter: invert()`**: eso deja una caja negra alrededor del lockup.

**La espiral 3D** (calco en extrusión del PNG, material "arcilla rúbrica") se
retiró con la intro psicodélica al llegar El Disco. El código queda en la
historia de git (`lib/espiral-3d.ts`, `components/intro/IntroCuriana.tsx`,
commit `3a903b1`) por si vuelve como pieza.

### 8.1 El favicon: "la noche" (decisión de Miguel, 2026-09-28)

Espiral `arte-hueso #F3EAD4` sobre `deep-900 #0F1621`, cuadrado de radio 16%.
De las cuatro opciones del handoff (sello naranja, noche, tinta sin fondo,
remolino índigo/ácido) se eligió esta: es la que mejor lee a 16px (hueso sobre
noche 15:1) y es registro sobrio, no tinta del arte. **La noche define el mood
de esta primera versión de Curiana Radio.** Ya la llevan la intro (§9) y la
landing (§10); el resto del sitio (archivo, ediciones) sigue en papel.

| Archivo en `public/` | Tamaño | Nota |
|---|---|---|
| `favicon.ico` | 16 + 32 + 48 | el que piden los navegadores por defecto |
| `favicon-16x16.png` · `-32x32` · `-48x48` | | canal de la espiral ensanchado ~1.2% (erosión óptica) para que no se empaste |
| `apple-touch-icon.png` | 180 | aplanado sobre `#0F1621`: iOS pinta de negro la transparencia |
| `icon-192.png` · `icon-512.png` | | manifest, `purpose: any`; trazo exacto al 72% |
| `icon-maskable-512.png` | 512 | el 512 a sangre sobre `#0F1621`, para la máscara de Android |

`theme-color` y `background_color` del manifest: `#0F1621`. Fuente de los
píxeles: el PNG original del autor (`isotipo-calco.png`), no `espiral.svg`.
El handoff (`design_handoff_favicon/`) se queda en disco, fuera de git, con
las otras tres opciones por si se cambia la decisión.

---

## 9. La intro v1: El Disco (pantalla de entrada)

`components/intro/` (`IntroDisco.tsx` + `disco-motor.ts` + `disco-shader.ts`).
El visitante llega a un **disco de arena** sobre la noche y está obligado a
interactuar: trazando círculos alrededor del disco, los surcos horizontales
del viento se reorganizan desde el centro hasta formar la espiral del isotipo.
Afinado, la espiral original aparece en hueso y se habilita
**[ SINTONIZAR → ]**, que lleva a la landing (`/inicio`). Handoff:
`design_handoff_intro_v1_disco/` (en disco, fuera de git).

- **Rutas.** `/` es la intro; una vez por sesión (`sessionStorage`
  `curiana:intro-v1 = "visto"`): quien vuelve pasa directo a `/inicio` sin ver
  la interfaz. `/intro` la muestra siempre (noindex). Sin JS: el isotipo y un
  enlace a `/inicio`.
- **Gesto.** Progreso += |Δθ| / (2π·2.2): unas **2.2 vueltas** afinan
  (presionando, ×1.4; cada toque suma 3 %). La frecuencia sube de 87.5 a 88.8
  y la aguja recorre el dial; el patrón pasa de surcos a remolino (>15 %),
  vórtice (>60 %) y espiral. El viento (km/h y rumbo) sale del puntero real.
- **Salida.** 1.7 s smoothstep: los surcos se comprimen al centro, velo negro
  desde el 55 %, y la landing amanece desde `#07090D` en 600 ms.
- **Shader** (WebGL2, un triángulo a pantalla completa, DPR ≤ 2), de fondo a
  frente: noche con granos dorados sueltos → borde de arena derramada (nunca un
  círculo perfecto) → campo de surcos (viento → espiral ovalada `q·(.9, 1.15)`,
  la proporción del isotipo) → ondas de toque y bulto bajo el cursor → domo y
  manchas → **grano aprobado** (fino ±.15, medio ±.11, 2.5 % brillantes, 4 %
  oscuros: no suavizar) → revelado con el PNG como alfa a 0.95R.
- **Paleta.** `--noche-hondo` de fondo; arena oro `#E6B43C` sobre tinta
  `#090806`; texto en hueso/hueso-2 sobre placa sólida (≥ 11:1), **nunca texto
  sobre arena**; el nombre en `--noche-oro`; aguja, punto y cursor en frequency.
- **Accesibilidad.** `prefers-reduced-motion`: el tiempo se congela, arranca
  afinado y SINTONIZAR navega sin transición. Botones reales en el orden
  SALTAR → SINTONIZAR (el foco pasa solo al segundo); "señal encontrada" se
  anuncia con `aria-live`. Sin WebGL2: el isotipo en hueso con el bloque final
  ya visible.
- **El nombre va con el logo** (Miguel, 2026-09-29). «Curiana Radio» ya no es
  una firma de esquina: aparece al afinar, al ritmo del revelado de la espiral,
  como lockup — a la derecha del disco y centrado en él; en pantallas
  verticales, debajo del disco y en una línea. Nunca sobre la arena.
- **Móvil (< 640 px).** Se oculta el bloque de datos de arriba a la derecha.

---

## 10. La landing v1 · la noche (`/inicio`)

`components/landing/` + `app/inicio/page.tsx`. El marco que contiene todas
las aristas. Estructura, copy e interacciones del handoff
(`design_handoff_landing/`); la paleta es la de la noche (§3.1): donde el
prototipo dice papel, aquí manda el README del handoff.

| # | Sección | Superficie |
|---|---|---|
| 01 | Hero · carrusel de aristas | barra (isotipo + lockup en hueso + "88.8 FM · SINTONIZADO") y 5 diapositivas en su superficie |
| 02 | Manifiesto | gradiente noche + grano; capitular, bloque expandible, blockquote |
| 03 | Interludio de arte | sala `#101010`; 3 obras que reservan su color dominante |
| 04 | Las aristas | noche; 4 tarjetas, cada una en su registro |
| 05 | Última transmisión | gradiente noche + grano; portada en `Cenefa` |
| 06 | Archivo y suscripción | noche; ediciones + formulario |
| 07 | Colofón | `--noche-hondo`; burro ASCII, proverbio, badge outline |

- **El hero** arranca sintonizado (la intro ya obligó a interactuar): auto-avance
  cada 5 s que se pausa con hover o foco y **se detiene** al tocar flechas,
  puntos, teclado (←/→) o swipe. Diapositivas inactivas `inert`. Con
  movimiento reducido: sin auto-avance y fundido de 200 ms.
- **Sin nav ni pie globales**: la landing y la intro traen los suyos
  (`components/layout/ShellRadio.tsx` los omite en `/`, `/intro`, `/inicio`).
  El logo de la nav del resto del sitio lleva a `/inicio`.
- **La edición** viene del contenido: `portada`, `sinopsis` y `ficha` en el
  `metadata.json` de cada edición; la landing muestra la última.
- **Suscripción**: envía a `NEXT_PUBLIC_SUSCRIPCION_URL` (POST de formulario
  con `email`). Sin proveedor, el formulario se ve deshabilitado y lo dice.
- **Buchibe** aún no tiene sección: su diapositiva y su tarjeta anuncian el
  telón ("CORRER EL TELÓN · PRONTO") sin enlazar.
- **Contraste** (requisito del cliente, ≥ 4.5:1): los `-faint` de sección se
  subieron a `-soft` en texto; el CTA y la etiqueta del telón van en
  `--buc-luz` (el oro sobre el telón da 3.5:1: vale para el título grande, no
  para texto chico). **Pendiente de decisión:** el botón naranja con texto
  blanco que pide el handoff da 2.8:1.
- Arte en `public/landing/` como WebP pre-generado (480/960 px; portada 640),
  con `<img srcset>` como la galería, sin el optimizador de Next.

---

*MVP — iteraremos. La paleta es provisional y está pensada para cambiarse;
toda la lógica de color ya está centralizada (§3) para hacerlo en minutos.*

---

## 11. Kaketiana (`/kaketiana`)

Handoff: `design_handoff_kaketiana/` (en disco, fuera de git). Kaketiana es la
placa clara, mineral y arqueológica dentro de la v1 nocturna: dirección
**6b «Sal y almagre»**, tipografía **7a · Fraunces WONK + Inter**, hero **1a ·
la palabra se arma**. Reutiliza los tokens `--sim-*` para heredar los
componentes del cronista.

- **Tokens.** `[data-kk-dir="sal"]` en `app/globals.css`: papel `#F2EDE3`,
  hundido `#E4DBC8`, tinta `#241D15`, rúbrica almagre `#9C3A1D`, fuego ocre
  `#B06A1C`, `--kk-extra` salina `#3F7D74` (enlaces, datos vivos). `ink-faint`
  no se usa para texto que se lea. El Acto I del experimento es la tinta
  profunda de `[data-sim-acto="laboratorio"]`: esa inversión es su firma.
- **La escala epistémica** (`components/kaketiana/Etiqueta.tsx`, clases
  `.kk-ep-*`): la certeza es la solidez del trazo. ▮ atestiguado lleno ·
  ◆ reconstruido firme · ◇ hipotético discontinuo · ~ retro-abstraído punteado
  · ◉ canon-simulación doble, **sólo en el experimento**. En prosa se abrevia,
  en tabla es la última columna, en imagen va dentro del marco.
- **Movimiento.** Una curva, `--kk-curva` = `cubic-bezier(0.22, 1, 0.36, 1)`;
  `--kk-t-rapido` 300 ms, `--kk-t-tinta` 600 ms, `--kk-t-umbral` 1200 ms.
  Amanecer (`components/kaketiana/Amanecer.tsx`) una vez por sección; Rúbrica
  en las acciones `.kk-accion`; el **caret es sólo de las voces simuladas**.
  `prefers-reduced-motion` apaga todo.
- **Micro-labels** en mono (`.kk-label`; dentro de `[data-kk]` los `Overline`
  pasan a mono) y **acciones** en registro terminal: `[ CRUZAR AL LABORATORIO → ]`.
- **Aplicado (2026-09-29):** `/kaketiana/experimento` — el umbral §05 (placa
  clara → banda sin texto → laboratorio, con la escala del lado oscuro para que
  las etiquetas se lean), ◉ en la frase simulada y en la tabla de nombres
  (fichas en móvil, sin scroll horizontal), el titular con Amanecer.
- **Aplicado (2026-09-30):** la portada `/kaketiana` (Vistas §01 + hero 1a),
  aligerada a pedido de Miguel: nav de la sección, la ecuación que se arma
  (`components/kaketiana/HeroPalabra.tsx`, una vez por visita), el mapa de los
  topónimos del canon (`export_mapa_seed.py` → `content/wiki/mapa.json`;
  teselas en sepia y el trazo por nivel de lectura: A sólido, B firme, C
  discontinuo), tres cifras, las dos puertas y la franja del experimento. Las
  listas de artículos pasan a `/kaketiana/pueblo` y `/kaketiana/lengua`.
  **El canon manda sobre el handoff** en la etimología: la glosa 'lugar de' de
  *-ana* se retiró (#109) y *kaketiana* es un compuesto nuestro, así que la
  palabra va ◇ hipotética (sin asterisco), no ◆.
- **Aplicado (2026-10-02): el marco de toda la sección.** `app/kaketiana/layout.tsx`
  pone la placa 6b y los micro-labels del manual (`data-kk`) a todas las
  páginas, y una sola navegación (`components/kaketiana/NavKaketiana.tsx`):
  «Kaketiana» · El pueblo · La lengua · Bibliografía en salina ·
  `[ EXPERIMENTO ]` en rúbrica · 88.8 FM; la sección actual con la Rúbrica fija;
  en móvil «Kaketiana · 88.8 · `[ ≡ ]`» (44px). Se retiraron el masthead de la
  era 1 y la cronología lateral de las páginas interiores (`SimShell`); la
  cronología queda sólo en `/kaketiana/experimento/era-1`, que es donde cuenta.
- **Pendiente:** el artículo de pueblo (65ch, capitular, miga con progreso,
  sumario, citas en serif), el de lengua (referencia, ancho completo, tablas →
  fichas), la bibliografía con anclas, separar lectura de cuaderno de trabajo,
  el marco de imagen, el modo oscuro de lectura y los experimentales §07–09.
