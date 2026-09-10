# Handoff: Manual de marca + Intro animada de Curiana Radio

## Overview

Dos entregas de diseño para el repo `miguelgilurbina/curiana-radio` (Next.js 14, App Router):

1. **Decisiones de manual de marca** tomadas en las sesiones de diseño — tipografía display del sistema, uso del lockup, y la regla de aplicación del type de cartel.
2. **La intro animada oficial** de Curiana Radio — pantalla de entrada psicodélica con la espiral del logo en 3D (WebGL/three.js), elegida entre cuatro exploraciones.

**No incluye la landing** — sus heros siguen en exploración y se entregarán aparte cuando se decida la dirección.

## About the Design Files

Los archivos de este bundle son **referencias de diseño creadas en HTML** — prototipos que muestran el look y el comportamiento intencionado, no código de producción para copiar tal cual. La tarea es **recrear estos diseños en el entorno del codebase** (Next.js 14 + React + Tailwind, según los patrones ya establecidos en `app/` y `components/`). El archivo de la intro (`Inicio Curiana Psicodelico.html`) es la excepción parcial: su script de three.js es autocontenido y portable casi directo a un componente cliente de React.

## Fidelity

- **Manual de marca: alta fidelidad.** Valores exactos de tipografía, transforms y colores; listos para tokens.
- **Intro animada: alta fidelidad funcional.** El HTML incluido ES la animación completa y funcional (shader + 3D + UI). Recrear 1:1.

---

## Parte 1 — Decisiones de manual de marca

### 1.1 El display del sistema: "type 3c" (Archivo Black comprimida)

**Decisión:** el registro de cartel del lockup CURIANA/RADIO entra al sistema tipográfico como display para titulares y rótulos, replicado con **Archivo Black comprimida artificialmente**:

```css
/* "type 3c" — display de cartel */
font-family: 'Archivo Black', system-ui, sans-serif;
font-weight: 400;             /* Archivo Black solo tiene 400 */
text-transform: uppercase;
letter-spacing: -0.02em;
transform: scaleX(0.82);      /* la compresión ES la identidad */
transform-origin: left;       /* center cuando el texto va centrado */
display: inline-block;        /* necesario para que el transform aplique */
white-space: nowrap;          /* en rótulos cortos */
```

Para el nombre completo "CURIANA RADIO" en heros el scaleX baja a **0.78**.

**Reglas de uso (importantes):**
- Solo para **rótulos y sellos de 1–3 palabras** (nombres de sección, cabeceras de bloque, títulos de edición). En textos largos que envuelven, la compresión por transform se nota y degrada.
- **El lockup PNG sigue siendo el logo oficial** (`assets/logo/lockup-bnw.png`). El type 3c es la voz de cartel del sistema, no un reemplazo del arte. Donde haya espacio y resolución, usar el PNG.
- Se tinta por superficie: `--deep-900` en la radio, `oklch(0.8 0.15 var(--jai-hue))` en JAI, `--sim-rubrica` en Simulador, `--gal-luz` en Galería, `--buc-oro` en Buchibe.
- Lo oracular NUNCA va en 3c: manifiesto, citas y proverbios siguen en Lora itálica. Los datos siguen en mono. (Regla: el cartel grita, el oráculo susurra, el dato teclea.)
- Carga: `https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap` — o self-host como las demás.

**Alternativas evaluadas y descartadas:** Anton (esqueleto cercano, menos tosco), Oswald 700 (más prensa que cartel — quedó como plan B para titulares largos si el transform diera problemas), Passion One 900 (demasiado retro-cartel). Referencia visual: `Wireframes Landing.dc.html` secciones 3 y 4.

### 1.2 Jerarquía tipográfica resultante

| Voz | Fuente | Uso |
|---|---|---|
| Cartel (display) | Archivo Black + scaleX(0.82) | rótulos de sección, titulares cortos, sellos |
| Oráculo | Lora itálica | manifiesto, citas, proverbios, subtítulos |
| Editorial | Lora 600 | titulares largos, prosa destacada |
| Cuerpo/UI | Inter | párrafos, nav, labels |
| Dato | ui-monospace stack | timestamps, frecuencias, metadatos, ASCII |
| Arte editorial | Fraunces SOFT 0 / WONK 1 | Simulador, JAI, arcos «presenta» |

### 1.3 El isotipo en 3D (nuevo recurso de marca)

La espiral existe ahora como **objeto 3D** generado por calco directo del PNG original (no una reconstrucción paramétrica — fidelidad total a las imperfecciones del dibujo):

**Pipeline de calco** (implementado en `Espiral 3D.html` y reutilizado en la intro):
1. Cargar el PNG del isotipo con `createImageBitmap` (no `img.decode()`, que puede colgarse).
2. Rasterizar a rejilla de 180×180 en canvas; binarizar: pixel sólido = alpha > 120 y suma RGB < 400.
3. **Marching squares** sobre la rejilla → segmentos de contorno con ids enteros precomputados (encadenado lineal, no cuadrático).
4. Encadenar segmentos en lazos cerrados; descartar lazos de < 24 puntos.
5. Suavizar (2 pasadas de promedio ponderado 1-2-1), submuestrear 1 de cada 2, normalizar a ~1 unidad.
6. El lazo de mayor área = contorno del disco; el resto = agujeros (`THREE.Shape` + `shape.holes`).
7. `ExtrudeGeometry`: depth 0.09, bevelThickness 0.012, bevelSize 0.01, bevelSegments 3.

**Material canónico:** "arcilla rúbrica" — `MeshStandardMaterial{ color: 0x8f3b26, roughness ~0.55–0.62, metalness ~0.08–0.12 }` (en la intro se aclara a `0xb8502e` para contraste sobre fondo saturado).

**Exportable:** `Espiral 3D.html` (visor con `three-d-stage.js`) descarga OBJ+MTL y GLB con mallas y materiales nombrados.

---

## Parte 2 — La intro animada (Inicio Curiana Psicodelico.html)

### Concepto

El visitante llega a un **remolino psicodélico serigráfico** — el registro de ARTE de la marca a máxima saturación — con la espiral 3D del logo flotando al frente y un túnel de ecos serigráficos detrás. Al pulsar [ SINTONIZAR → ] el remolino acelera, la cámara entra por el centro y un velo pergamino "amanece" hacia la landing. La intro es lo saturado; la landing que sigue es lo sobrio — la regla de los dos registros hecha secuencia.

### Composición (capas, de atrás hacia adelante)

1. **Fondo shader** (plano fullscreen, `ShaderMaterial`): remolino de bandas espirales en coordenadas polares. Dos ondas interferentes (`sin(a*3 + log(r)*7 − t*0.55)` y `sin(a*5 − log(r)*11 + t*0.4)`), paleta mezclada por smoothstep entre:
   - índigo `#26396A` → vec3(0.149, 0.224, 0.416)
   - ocre `#C36712` → vec3(0.765, 0.404, 0.071)
   - ácido `#C7C91C` → vec3(0.780, 0.788, 0.110)
   - rojo `#B64924` → vec3(0.714, 0.286, 0.141)
   - Viñeta radial hacia índigo oscuro y **posterización a 5 niveles** (`floor(col*5+0.5)/5`) — registro de serigrafía, no degradado.
2. **Túnel de ecos:** 6 copias planas (`MeshBasicMaterial`) de la geometría de la espiral en las tintas del arte (`#C7C91C, #26396A, #C36712, #B64924, #F3EAD4, #2154C5`), escala creciente `1.3 + (i+1)*0.52`, z = `−0.55*(i+1)`, opacidad decreciente `0.85 − i*0.11`, girando en contrafase (pares/impares) con pulso leve de escala.
3. **La espiral protagonista:** el calco 3D extruido (Parte 1.3), color `0xb8502e`, escala 1.35, luces: HemisphereLight `0xf3ead4/0x23224f`, direccional cálida `0xffb08a` (1.7), direccional ácida `0xc7c91c` (0.8).
4. **Overlays DOM:** trama de semitono (radial-gradient 5px, `mix-blend-mode: multiply`, opacidad .5) + scanlines (repeating-linear-gradient 3px, opacidad .14).
5. **UI:** título "CURIANA RADIO" (Inter/mono del sistema, tracking .62em) con **misregistro de imprenta animado** — text-shadow doble `#B64924` / `#26396A` desplazándose en ciclo de 7s; badge 88.8 FM (`#FF6B35`); estado "INTERFERENCIA · SEÑAL DE OTRO TIEMPO" en ácido con punto pulsante; botón [ SINTONIZAR → ] borde ácido que invierte a fondo ácido/texto índigo en hover; proverbio en Lora/Georgia itálica.

### Interacciones y comportamiento

- **Parallax:** `pointermove` inclina la espiral (`rotation.x ±0.12`, `rotation.z ±0.06`).
- **Idle:** espiral gira `0.004 rad/frame`, flota `sin(t*0.8)*0.03`, el shader avanza con `t`.
- **Sintonizar (clic):** 1600ms ease-out-cubic — `velocidad: 1 → 27` (el remolino se dispara), `dolly: 0 → 2.35` (la cámara atraviesa el centro), velo `#F3EAD4` funde a partir del 45%, luego `location.href` a la landing.
- **`prefers-reduced-motion: reduce`:** shader congelado (`marea = 0`), sin giro ni flotación, misregistro estático, el botón navega directo sin animación.
- El botón lleva `white-space: nowrap` (fix de viewport angosto).

### Implementación en el repo

- Portar como componente cliente (`'use client'`) — p. ej. `app/intro/page.tsx` o gate en `app/page.tsx` con estado "ya vista" en `sessionStorage` (mismo patrón que `lib/jai-rotacion.js`).
- three.js ^0.184 como dependencia; el import map del HTML se reemplaza por imports normales.
- El PNG del isotipo debe servirse desde `public/` (el calco hace fetch del archivo).
- El calco corre una vez al montar (~10ms); cachear la geometría si la intro puede remontarse.
- El destino del velo debe ser la landing real (en los prototipos apunta a `Landing Curiana Radio.dc.html`).

## State Management

Intro: `velocidad` (float, 1→27 al sintonizar), `dolly` (float 0→2.35), `mx/my` (parallax), flag `lento` (reduced motion), opacidad del velo. Sin estado global; un `sessionStorage.curianaIntroVista` opcional para no repetirla en la sesión.

## Design Tokens (usados aquí)

- Tintas del arte: ácido `#C7C91C` · índigo `#26396A` · azul eléctrico `#2154C5` · ocre `#C36712` · rojo `#B64924` · hueso `#F3EAD4`
- Interfaz: frequency `#FF6B35` · rúbrica `#8F3B26` · arcilla 3D `#B8502E` · fondo intro `#23224F`
- Timing: hover 300ms `cubic-bezier(0.22,1,0.36,1)` · transición sintonizar 1600ms ease-out-cubic · misregistro 7s · pulso 1.1s steps(2)
- Type 3c: Archivo Black, scaleX(0.82) [0.78 en heros], letter-spacing −0.02em, uppercase

## Assets

- `uploads/Curiana  PNG.png` — **el PNG original subido por el autor: la fuente real del calco 3D** (la intro y el visor hacen fetch de esta ruta exacta — en el repo, moverlo a `public/` y actualizar la ruta)
- `assets/isotipo-espiral.png` — isotipo 1024² del design system
- `assets/lockup-bnw.png` — lockup oficial CURIANA/RADIO
- `assets/espiral.svg` — trazado vectorial (favicon/UI pequeña; NO usado por el calco)
- Fuentes: Archivo Black (nueva), Lora/Inter/Fraunces (ya en el repo)

## Files

- `Inicio Curiana Psicodelico.html` — **la intro elegida**, funcional completa
- `Espiral 3D.html` + `three-d-stage.js` — visor/exportador del isotipo 3D (OBJ/GLB)
- `Wireframes Landing.dc.html` — registro de la exploración tipográfica (secciones 3–4: elección del type 3c)

Exploraciones de intro descartadas (contexto, no implementar): `Inicio Curiana.html` (nocturna sobria), `Inicio Curiana Cimatica.html` (partículas), `Inicio Curiana Amanecer.html` (diurna).
