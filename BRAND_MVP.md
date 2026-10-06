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
| `--noche-acento` | `#E6B43C` | **el acento de la noche** (2a oro de arena, §13): aguja, en vivo, badge, CTA (con tinta `--noche-fondo`, 10.2:1), hover; reemplaza al naranja en la noche |
| `--noche-frecuencia-tinta` | = acento | hover, riel de cita y foco en la piel de la radio (§12); en su claro, `#7E5A1E` |
| `--noche-dato` | `#7E93AA` | overlines y línea legal del shell, sólo mono pequeño (5.7:1) |
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
Afinado, la espiral original aparece en hueso, **la arena se levanta y se
vuelve el sello de Curiana Radio**, y se habilita **[ SINTONIZAR → ]**, que
lleva a la landing (`/inicio`). Handoff: `design_handoff_intro_v1_disco/` (en
disco, fuera de git), rehecho el 2026-10-05 para que la intro esté en sintonía
con el look inicial de la radio: el color sale del logo.

- **Rutas.** `/` es la intro; una vez por sesión (`sessionStorage`
  `curiana:intro-v1 = "visto"`): quien vuelve pasa directo a `/inicio` sin ver
  la interfaz. `/intro` la muestra siempre (noindex). Sin JS: el isotipo y un
  enlace a `/inicio`.
- **Gesto.** Progreso += |Δθ| / (2π·2.2): unas **2.2 vueltas** afinan
  (presionando, ×1.4; cada toque suma 3 %). La frecuencia sube de 87.5 a 88.8
  y la aguja recorre el dial; el patrón pasa de surcos a remolino (>15 %),
  vórtice (>60 %) y espiral. El viento (km/h y rumbo) sale del puntero real.
- **La arena se vuelve sello** (handoff 2026-10-05). Con la espiral a medio
  revelar, 9.400 granos se levantan del disco en un lienzo 2D sobre el shader
  y viajan 3.2 s hacia el sello: 3.200 salen de la espiral de arena y van a la
  espiral del sello; 6.200 salen del resto del disco y van al marco y las
  letras (los de afuera despegan primero, retardo = radio · 0.22). Trayecto
  `easeInOutCubic` con un remolino alrededor del centro y ±5 px de viento. El
  disco se funde al fondo en el primer 28 % (`uFund`) y el sello nítido entra
  entre el 84 % y el 100 %, con su espiral sobre el centro del disco. Los
  destinos salen de la imagen del sello (`sello-curiana-noche`, el mismo del
  shell, §13) en una grilla de 256²; el sello del final es su WebP (300, 600
  y 1200 px). El nombre visible es el sello: el `<h1>` queda para lectores de
  pantalla.
- **Salida.** 1.7 s smoothstep: los surcos se comprimen al centro, el sello
  crece un 25 % y se apaga, velo `#0F1621` desde el 55 %, y la landing amanece
  desde la misma noche en 600 ms.
- **Shader** (WebGL2, un triángulo a pantalla completa, DPR ≤ 2), de fondo a
  frente: noche con granos dorados sueltos → borde de arena derramada (nunca un
  círculo perfecto) → campo de surcos (viento → espiral ovalada `q·(.9, 1.15)`,
  la proporción del isotipo) → ondas de toque y bulto bajo el cursor → domo y
  manchas → **grano aprobado** (fino ±.15, medio ±.11, 2.5 % brillantes, 4 %
  oscuros: no suavizar) → revelado con el PNG como alfa a 0.95R.
- **Paleta** (handoff 2026-10-05: «la arena es hueso sobre noche, sin oro»).
  Fondo `#0F1621`; arena hueso `vec3(.80,.77,.70)` sobre la tinta azulada de
  los valles `vec3(.035,.051,.078)`; el lockup, la espiral revelada y el texto
  en hueso (≈ 14:1), **nunca texto sobre arena**. La aguja, el punto en vivo,
  los hover, el foco y el cursor van en el **acento de la noche**, el oro de
  arena (§13): el prototipo traía el naranja `#FF6B35` y Miguel decidió el
  oro en toda la noche, intro incluida (2026-10-05).
- **Accesibilidad.** `prefers-reduced-motion`: el tiempo se congela, arranca
  afinado y SINTONIZAR navega sin transición. Botones reales en el orden
  SALTAR → SINTONIZAR (el foco pasa solo al segundo); "señal encontrada" se
  anuncia con `aria-live`. Sin WebGL2: el isotipo en hueso con el bloque final
  ya visible.
- **El nombre es el sello.** Desde el 2026-10-05 «Curiana Radio» no aparece
  como texto al costado del disco (la versión del 2026-09-29): lo arma la
  arena, como el sello oficial (marco hueso, espiral original y type 3c).
- **Móvil (< 640 px).** Se oculta el bloque de datos de arriba a la derecha.

---

## 10. La landing v1 · la noche (`/inicio`)

`components/landing/` + `app/inicio/page.tsx`. El marco que contiene todas
las aristas. Estructura, copy e interacciones del handoff
(`design_handoff_landing/`); la paleta es la de la noche (§3.1): donde el
prototipo dice papel, aquí manda el README del handoff.

| # | Sección | Superficie |
|---|---|---|
| 01 | Hero · carrusel de aristas | 5 diapositivas en su superficie; la barra de arriba es la cabecera de la noche (§13) |
| 02 | Manifiesto | gradiente noche + grano; capitular, bloque expandible, blockquote |
| — | Quién transmite | `--noche-hondo`; la ficción dicha como ficción: quién hace la radio, enlace a `/sobre` y al portafolio de Miguel |
| — | Señales (§12) | noche; la última señal destacada y dos más; no sale sin señales |
| 03 | Interludio de arte | sala `#101010`; 3 obras que reservan su color dominante |
| 04 | Las aristas | noche; 4 tarjetas, cada una en su registro |
| 05 | Última transmisión | gradiente noche + grano; portada en `Cenefa` |
| 06 | Archivo y suscripción | noche; ediciones + formulario |
| 07 | Pie de la noche | el pie común del shell (§13): sello, proverbio, estaciones, suscripción, línea legal |

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
- **Kaketiana** (antes «Simulador Caquetío», 2026-10-05): la diapositiva, la
  tarjeta y el menú global dicen Kaketiana, y la diapositiva y la tarjeta van en
  su placa 6b (`data-kk-dir="sal"`, §11), no en el pergamino del Simulador.
- **«Seguir leyendo»** del Manifiesto es `components/landing/SeguirLeyendo.tsx`
  (botón con `aria-expanded`, abre y cierra), no un `<details>` nativo.
- **Contraste** (requisito del cliente, ≥ 4.5:1): los `-faint` de sección se
  subieron a `-soft` en texto; el CTA y la etiqueta del telón van en
  `--buc-luz` (el oro sobre el telón da 3.5:1: vale para el título grande, no
  para texto chico). El botón naranja con texto blanco (2.8:1) quedó resuelto
  con el acento de la noche (§13): oro de arena con tinta de fondo, 10.2:1.
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
- **Aplicado (2026-10-02): el artículo de pueblo** (Vistas §02, móvil en
  Sistema §06; `components/kaketiana/ArticuloEnsayo.tsx`). Miga con progreso
  («KAKETIANA / EL PUEBLO / …» · `07 / 10`; en móvil «← EL PUEBLO»); sumario de
  230px con la sección actual en rúbrica y la Rúbrica, «… N secciones más», y en
  móvil plegado en «EN ESTE ARTÍCULO · N ▾» (`Sumario.tsx`); la `pregunta` del
  frontmatter como título; prosa a 65ch con capitular; «sobre qué se sostiene»
  en dos columnas y la tarjeta «siguiente pregunta». Todo lo que lleva número
  sale del cuerpo (`lib/articulo.ts`). En la prosa de todo el wiki
  (`wiki-mdx.tsx`): los `##` llevan ancla; **la cita de una fuente** (abre con
  comillas) va en serif sobre papel hundido con la « colgada y el pie en mono,
  y en móvil a sangre completa; **nuestras notas** (avisos, correcciones) vuelven
  a sans con un filete, en rúbrica si avisan; enlaces en salina; tablas `.kt`.
  No se aplicó el **índice de certeza**: el manual lo calcula de las etiquetas
  de cada afirmación y los ensayos no las llevan; contado sobre las voces que
  nombran salían de 0 a 5 por ensayo, y eso mide el formato, no la certeza.
  Tampoco se cuentan «citas» por obra: los ensayos citan en prosa y enlazan cada
  obra una vez o ninguna.
- **Pendiente:** el artículo de lengua (referencia, ancho completo, tablas →
  fichas), la bibliografía con anclas, separar lectura de cuaderno de trabajo
  (las líneas de sesión, rutas y hojas de fuentes del vault siguen en los
  ensayos), el marco de imagen, el modo oscuro de lectura, el índice de certeza
  (pide etiquetar las afirmaciones en el vault) y los experimentales §07–09.

---

## 12. Señales (`/senales`)

El blog: lo que Miguel escribe desde acá, firmado, sobre cada arista (issue
#248). La radio transmite desde después; las señales salen del presente. Es
**un solo blog**: cada entrada lleva sus aristas y cada arista muestra las
suyas. Contenido en `content/senales/<slug>.mdx`, lectura en `lib/senales.ts`,
el flujo de publicación en la skill `publicar-entrada`.

- **El motor de pieles** (`components/senales/pieles/` + `globals.css`, «El
  motor de pieles»). Miguel, 2026-10-04: la página es «una máquina estética de
  conceptos». Una plantilla y N pieles: toda señal tiene la misma estructura
  (miga e interruptor, borrador, título, sumario, dato, portada, cuerpo a
  65ch, firma, nota, pie) y la **piel** decide la superficie, las voces, la
  tinta y lo que va sobre la cabecera. **La arista dice dónde aparece una
  señal; la piel, cómo se ve.** Cada arista trae su piel por defecto (la de su
  primera arista; sin arista, la radio) y una señal puede pedir otra con
  `piel:` en el frontmatter: una señal de Kaketiana puede vestirse de telón.
- **Una piel es datos** (design_handoff_senales_luces, 2026-10-05). Su tinta y
  sus voces son un bloque de CSS que mapea los tokens de su sección a un juego
  común de alias `--e-*` (fondo, placa, texto, texto-2, filete, enlace,
  capitular, riel, cita, radios, ancho de figura, familias y ejes de título,
  sumario, cuerpo y cita, tracking y caja del dato, cabecera). La plantilla
  (`app/senales/[slug]`, `components/senales/senal-mdx.tsx`, `voces.ts`) sólo
  lee los alias: ninguna clase nombra una piel. La ficha TS de cada piel dice
  lo que el CSS no puede: concepto, manual, luz nativa, atributos de tema,
  capitular, `Antetitulo`, fuentes y scripts. La columna de 65ch es el
  contenedor del cuerpo, medida con la letra del cuerpo (un `ch` dentro de un
  h2 grande mediría el doble); las figuras salen de ella hasta `--e-figura-max`.

  | Piel | Superficie | Voces |
  |---|---|---|
  | la radio (sin arista) | la noche (§3.1, §10) | Lora 600 / Lora itálica / Inter 1.125rem / dato .24em |
  | Kaketiana | la placa 6b «Sal y almagre» (§11) | Fraunces WONK; Inter 1.02rem/1.8; capitular y riel de cita (3px, papel hundido, radio 0 12 12 0) en almagre; enlaces en salina; figuras con radio 16px; dato .18em |
  | JAI Sounds | el dial (`--jai-noche`) | la Fraunces de JAI (700 opsz 72 · 500 opsz 72 SOFT 30); Inter 17/1.7; enlaces y riel en la señal; dato .3em en minúscula; radios 0; **sin naranja, ni en el foco** |
  | Galería | la sala acromática | Lora e Inter sin color; cita sobre la placa; las figuras salen hasta 72rem; dato .3em |
  | Buchibe | cabecera en el telón con «Curiana Radio presenta» (fija, no cambia de luz), el cuento en la noche ultramar | Fraunces en oro sólo en el título; cuerpo en Lora 1.15/1.85; capitular y riel en `--buc-oro-tinta`; enlaces `--buc-enlace` |

  La fuente de JAI vive en `app/jai-sounds/fraunces-jai.ts` para que la usen
  su sección y sus señales.
- **Crear una piel** (por ejemplo «Noticias Manifiesto», que Miguel tiene en
  mente): (1) nombrarla en `PIELES_IDS` (`lib/senales-comun.ts`); (2) en
  `globals.css`, sus tokens bajo su atributo de tema y su bloque
  `[data-piel="<id>"]` con TODOS los alias `--e-*` (copiar uno vecino); su
  otra luz en `html[data-luz="…"] [data-piel="<id>"]`; (3) su ficha en
  `components/senales/pieles/`; (4) registrarla en `pieles/index.ts`
  (TypeScript no compila mientras falte); (5) una fila en las tablas de aquí,
  con el contraste medido. Una piel nueva necesita su fuente de diseño: el
  motor la recibe, no la inventa. El build falla si una señal pide una piel que
  no existe.
- **Claro y oscuro** (design_handoff_senales_luces, 2026-10-05). Cada vista
  **arranca en su luz nativa** (la identidad de su arista) y **no** sigue
  `prefers-color-scheme`. El lector cambia con el interruptor
  (`components/senales/InterruptorLuz.tsx`): un solo `<button aria-pressed>`
  con las dos luces a la vista, la activa primero, subrayada y en el color del
  texto; los glifos llevan el selector de texto U+FE0E para que iOS no los
  pinte como emoji; 44px de objetivo. La elección vale para todo el sitio
  (`localStorage curiana:luz` → `html[data-luz]`, publicada en el `<head>`
  antes del primer pintado, `lib/luz.ts`) y se borra con «volver a la luz de
  cada sección», en el pie de la noche (`components/shell/LuzNativa.tsx`). La
  otra luz no cambia clases: redefine los tokens de la piel, y los alias los
  toman solos.

  | Piel | Nativo | La otra luz (valores del handoff) |
  |---|---|---|
  | la radio | oscuro | claro: el papel `#F8F6F3` / `#0F1621`; la tinta del acento pasa a `#7E5A1E` (5.8:1) y el riel de cita al 100 % |
  | Kaketiana | claro | oscuro: **tinta parda** `#1C1712` (no la noche azul, que es del Acto I); almagre `#E79277` y salina `#7BC9B9` con su matiz, más claros |
  | JAI Sounds | oscuro | claro: papel blanco; la señal `oklch(0.50 0.13 h)` pasa como texto en toda la rueda (peor matiz 4.9:1) |
  | Galería | oscuro | claro: la sala en positivo, R = G = B, `#F3F3F3` (no blanco, para que una obra blanca no se pierda) |
  | Buchibe | oscuro | claro: sólo el cuerpo (`#F5ECDD`); el telón no se prende |

  Cambios que salen de este handoff y tocan más que Señales: `--kk-extra` en la
  placa 6b pasa de `#3F7D74` (4.1:1, no llegaba a AA) a `#2E655C` en todo
  Kaketiana; Buchibe gana `--buc-luz-2`, `--buc-oro-tinta`, `--buc-enlace` y
  `--buc-panel`; la noche gana `--noche-frecuencia-tinta` (hover, riel de cita
  y foco; en la noche es el acento, §13). El foco de cada piel va en su propia
  tinta (`--e-foco`), nunca naranja dentro de JAI. El claro de la radio usa
  `#7E5A1E` (el oro legible sobre papel del mismo handoff) en vez del
  `#B4441A` que el handoff proponía cuando el acento todavía era naranja.
- **El índice va en la piel de la radio** y sigue la luz del lector: miga
  «Curiana Radio / Señales» e interruptor; «Señales» en Lora 600; los filtros
  *Todas · la radio · Kaketiana · JAI Sounds · Galería · Buchibe* (mono, 36px,
  radio 2px, cada uno con su sello; vacíos dicen que no hay señales todavía);
  cada entrada con el **sello** de su arista alineado a la primera línea, el
  título en Lora 600, el sumario en Lora itálica y el dato en mono. Los sellos
  (`--sello-*`, cuadros de 7px, ≥ 3:1 como trazo) son: radio `#FF6B35`,
  Kaketiana `#B06A1C`, JAI `oklch(0.80 0.15 212)`, Galería `#F0EFEC`, Buchibe
  `#C9A05A`; sobre papel, radio `#D9501C`, JAI `oklch(0.50 0.13 212)`, Galería
  `#2A2A2A`, Buchibe `#8C2B12`.
- **Dónde aparece:** el índice `/senales`; la landing, después del Manifiesto (la última destacada y
  dos más; sin entradas, la sección no sale); y dentro de cada arista
  (`components/senales/SenalesDeArista.tsx`), en el registro de su superficie:
  la placa de Kaketiana, el dial de JAI (sin naranja: §JAI), el papel de la
  Galería. Buchibe tiene etiqueta pero no sección.
- **Kaketiana:** una señal con esa arista lleva al pie que es la voz de su
  autor y enlaza a la investigación. Lo que diga de los caquetíos no es canon.
- **Para compartir:** cada señal genera su tarjeta (`opengraph-image.tsx`,
  1200×630: noche, isotipo, título en Lora, firma, filete en el acento oro). Fuentes
  woff de @fontsource en `app/senales/fuentes/` (next/og no lee woff2).
- **Imágenes** en Vercel Blob (`npm run senales:imagenes`), videos de YouTube
  incrustados con `youtube-nocookie`. Nada de media en el repo.
- **Borradores** (`borrador: true`): se ven en local y en las vistas previas
  de Vercel, nunca en producción (`VERCEL_ENV`).
- **Redes** (`lib/redes.ts`): Instagram y YouTube, @curianaradio, en el pie
  de la noche (§13), el pie de papel, el índice y el pie de cada señal.
- **RSS:** `/senales/rss.xml`.

---

## 13. El shell La Noche (cabecera y pie)

> **Qué está al aire** (Miguel, 2026-10-06): por ahora sólo Curiana Radio
> (la landing, Señales y «Quién transmite»), **Kaketiana** y **JAI Sounds**.
> La Galería, Cuentos de Buchibe y el archivo de ediciones siguen en el
> taller. Una sola fuente: `LIBERADA` en `lib/secciones.ts`, que leen la nav,
> el pie, el hero y las aristas de la landing, «Quién transmite», las
> etiquetas y los filtros de Señales, el pie de JAI y el sitemap. En
> producción sus rutas (`/galeria`, `/archivo`, `/01`…) vuelven a `/inicio`
> (`SIN_LIBERAR` en `next.config.js`); en local y en las vistas previas se
> ven. Liberar una es cambiar su línea en los dos lugares.

Handoff: `design_handoff_senales_luces/shell/` (SHELL.md y `Shell La Noche.dc.html`).
El marco común de la landing (`/inicio`), Señales (`/senales`, `/senales/*`) y
«Quién transmite» (`/sobre`): un mismo sello, un mismo fondo y un reparto de
voces fijo: **el cartel grita** (Archivo Black), **el oráculo susurra** (Lora
itálica), **el dato teclea** (mono). Lo elige `components/layout/ShellRadio.tsx`
para **todas las páginas** menos la intro El Disco (`/`, `/intro`), que va
sin marco. El papel de la radio (la nav, el pie y el fondo animado de antes,
y el badge naranja) se retiró el 2026-10-06.

- **Decisiones de Miguel (2026-10-05):** la opción **1a · El dial**; el acento
  **2a · oro de arena** `#E6B43C` (10.2:1 sobre `#0F1621`); y **SEÑALES en la
  nav**. «Quién transmite» va en el pie, en «La emisora».
- **El acento** (`--noche-acento`) reemplaza al naranja **en toda la noche**: la
  aguja, el punto en vivo, el badge 88.8, los CTA (con tinta `--noche-fondo`
  encima: el naranja con texto blanco daba 2.8:1 y queda resuelto), los hover,
  el filete de la cita del Manifiesto, los puntos del carrusel y el `#01` del
  archivo. `--noche-frecuencia-tinta` apunta a él. El naranja `#FF6B35` sigue
  en el papel de la radio y en el sello de «la radio» del índice.
- **Cabecera** (`components/shell/CabeceraNoche.tsx`): sticky, fondo sólido sin
  vidrio, se esconde al bajar y vuelve al subir. Desde `lg`: 92px; el sello de
  56px; la nav MANIFIESTO · SEÑALES · JAI SOUNDS · KAKETIANA (y GALERÍA ·
  BUCHIBE · ARCHIVO cuando se liberen) en mono 11px .24em, repartida sobre la escala de sintonía,
  con la **aguja** (2×46px, acento) en la estación activa, que se desliza al
  navegar (300ms; sin movimiento con `prefers-reduced-motion`); a la derecha
  AL AIRE con su pulso y el badge **88.8 FM**. La estación activa sale de la
  ruta; en una señal, la de su arista (sin arista, Señales). Buchibe está en el
  dial pero no se sintoniza (sin sección: va en `--noche-dato`, «pronto»).
  Móvil: 72px, el sello de 48px, el badge y `[ DIAL ]`, que abre el menú a
  pantalla completa (Archivo Black 32px sobre la escala vertical, la aguja
  horizontal de 22×2px en la activa, `[ CERRAR × ]` en acento, SINTONIZAR
  AHORA → a la última edición, AL AIRE · 88.8 FM). El menú cierra con Escape,
  devuelve el foco y va fuera de la cabecera (su translate haría de bloque
  contenedor para un `fixed`).
- **Pie** (`components/shell/PieNoche.tsx`): el sello de 150px (96 en móvil) y
  «El viento no borra, reescribe.»; ESTACIONES, LA EMISORA (Manifiesto,
  Señales, Quién transmite, Ver todas las transmisiones →, Spotify, Instagram,
  YouTube) y LA SEÑAL, CADA MES (`Suscripcion` en su variante del pie); la
  escala del dial con la aguja al 52 %; la línea legal (88.8 FM — SIEMPRE
  TRANSMITIENDO · TRANSMISIÓN CULTURAL DESDE ABYA YALA · EDICIÓN #NN · V1 LA
  NOCHE) y, si el lector eligió una luz, «volver a la luz de cada sección».
- **Tokens del shell** (`.shell-noche` en `globals.css`): filetes un paso más
  hondos que los de la landing (`#2B3D52`, `#3A4B61`), `--shell-hueso`
  `#F3EAD4` para el activo, `--noche-dato` `#7E93AA` (5.7:1) sólo para mono
  pequeño. El shell va siempre de noche, aunque la página que enmarca esté en
  claro.
- **El sello** (`components/shell/Sello.tsx`): el PNG del handoff (2048px,
  450 KB) servido como WebP de 112, 192, 300, 600 y 1200px (`public/marca/sello-curiana-noche-*.webp`); el mismo sello que arma la arena en la intro (§9).
- **En la landing**, el shell reemplaza la barra propia del hero (isotipo,
  lockup, SINTONIZADO; el `<h1>` queda para lectores de pantalla) y el
  Colofón 07 (su proverbio pasa al pie; el burro ASCII sigue en el 404).
- **Mientras el archivo esté en el taller:** la landing no muestra la
  última edición ni el archivo (la suscripción vive en el pie), el CTA del
  hero sintoniza el manifiesto, SINTONIZAR AHORA del menú lleva a `/inicio` y
  la línea legal dice sólo «V1 LA NOCHE».
- **Pendiente:** el sello de «la radio» en el índice sigue naranja y el de
  Buchibe es oro, cerca del acento nuevo; las páginas en el taller (archivo,
  ediciones, galería) llevan el shell pero su contenido sigue en papel.

