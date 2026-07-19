# Diseño — Motor ambiental y agentes ecológicos

*Pseudo-diseño, NO implementación. Expande el anexo del ensayo
`02_ecologia_golfete.md` a un boceto concreto, con base en la ecología real
investigada (ver `curiana_sim/cultura/ecologia.yaml`).*

> **Estado:** propuesta de diseño para discusión. No toca `curiana_state.py` ni ningún
> `.py`. Si se adoptara, reemplazaría el catálogo estático de eventos por un motor
> causal. Aquí solo se describe la lógica.

---

## 1. Problema

Hoy `curiana_state.py` elige eventos ambientales de listas fijas
(`EVENTOS_COTIDIANOS`, `EVENTOS_ESTACIONALES`). Es robusto pero **estático**: los eventos
no se causan entre sí, no responden al viento ni a la estación de forma continua, y no
generan la presión comunicativa que haría emerger neologismos. La ecología real del
Golfete (clima BSh, alisio ENE constante, evaporación, cardúmenes móviles, pulso de lluvia
oct–dic) es una **cadena causal**, no una baraja de tarjetas.

## 2. Principio: agentes ecológicos con voz mediada

Modelar el medio como un pequeño elenco de **agentes ecológicos** —procesos con estado, no
personajes que hablan—: **Alisio, Golfete, Salinar, Buco, Manglar**. Regla de oro:

> **El estado de un agente ecológico NUNCA llega como dato crudo al agente humano.**
> Llega solo por canales culturalmente verosímiles: resultado de pesca, sabor del agua,
> comportamiento de los animales, sueño del piache, presagio.

Esto preserva lo que hace interesante a la simulación: la comunidad **interpreta** el mundo
con su cosmología (dueños espirituales, wanülüü, presagios), no lee un sensor.

## 3. Las tres capas (traducción en cascada)

Cada señal ecológica se traduce en tres pasos antes de tocar a un humano:

| Capa | Qué es | Quién la «ve» | Ejemplo |
|---|---|---|---|
| **1. Hecho ecológico** | estado numérico del agente ambiental | nadie (interno) | `alisio=fuerte → golfete_claridad=alta → cardumen_cunaro se desplaza a bajíos del norte` |
| **2. Experiencia** | efecto perceptible, sin causa explícita | los agentes humanos | Bagre-ko pesca poco 3 días en el sitio de siempre; las bobas vuelan al norte; el agua sabe distinta |
| **3. Interpretación** | lectura cultural/religiosa | los agentes, en su habla y actos | Shaboro sueña que «el dueño del mar se llevó los peces»; se ofrenda *sakana*; los Guaycarí culpan al calor, los caquetíos al mal ritual |

La causa real (el viento movió el cardumen) **jamás se enuncia**. Emerge como teología y como
tensión social — exactamente como el evento actual `pesca_mala` ya insinúa, pero de forma
sistemática.

## 4. Variables de estado (boceto)

Cada agente ecológico mantiene un puñado de variables continuas (0–1 salvo indicación):

```
Alisio:     intensidad        # sube en seca, baja en lluvias; ruido diario
            (dirección fija ENE — constante, no se modela)
Golfete:    claridad_agua     # alta con alisio fuerte + poca lluvia
            temperatura       # inversa a claridad en la práctica
            corriente_tarde   # crece con el viento del día (hasta ~1 m/s real)
            posicion_cardumen # {sur, centro, norte, disperso} por especie
Salinar:    costra            # se acumula con sol+viento en seca, se disuelve con lluvia
Buco:       nivel_agua        # sube con pulso de lluvia, baja por evaporación/uso
            integridad_pared  # baja con crecida brusca; se repara con trabajo
Manglar:    productividad     # moluscos/aves/madera; alta y estable todo el año
            aves_migratorias  # pico estacional (reloj natural)
```

## 5. Cadenas causales (el corazón del motor)

En vez de «elegir un evento», cada turno el motor **propaga** la estación y el viento por la
cadena y **lee umbrales**:

```
estación ──► Alisio.intensidad ──► Golfete.claridad_agua
                    │                      │
                    │                      ├─► Golfete.posicion_cardumen
                    │                      └─► pesca_resultado ──► nivel_alimentos ──► nivel_tension
                    │                                                                      │
                    ├─► Salinar.costra ──► cosecha_biro ──► poder_redistributivo(Manaure)  │
                    │                                                                      ▼
                    └─► navegabilidad ──► ventana de expedición a islas          prob. sueño/presagio (piache)

pulso_lluvia(oct–dic) ──► Buco.nivel_agua ──► estado_conucos ──► cosecha
                     └──► Buco.integridad_pared (riesgo de crecida brusca)
```

Los «eventos» de hoy dejan de ser tarjetas y pasan a ser **lecturas del estado al cruzar un
umbral**:

| Evento actual | Se dispara cuando… |
|---|---|
| `pesca_abundante` / `pesca_mala` | `pesca_resultado` supera / cae bajo un umbral |
| `gran_cosecha_sal` / `raspado_salinar` | `Salinar.costra` alta **y** estación=seca |
| `crecida_buco` | `Buco.nivel_agua` alto **y** `integridad_pared` bajo tras pulso de lluvia |
| `expedicion_perlas` | `Golfete.claridad_agua` alta **y** estación=seca (agua clara) |
| `sequia_inicio` | `Buco.nivel_agua` bajo sostenido |
| `consulta_piache_sueno` | `prob. sueño` cruza umbral (más probable en mala pesca/tensión) |

## 6. Ejemplo trazado (un cardumen que se fue)

1. **Hecho:** entra la seca → `Alisio.intensidad ↑` → `Golfete.claridad_agua ↑` →
   `posicion_cardumen[cunaro]: centro → norte`.
2. **Experiencia:** `pesca_resultado` de Bagre-ko cae 3 turnos seguidos en su sitio habitual.
   Señal secundaria emitida al mundo: «las bobas vuelan hacia el norte» (Capa 2).
3. **Interpretación:** sube `nivel_tension`; sube `prob. sueño` de Shaboro → sueña con el
   dueño del mar; se ofrenda *sakana*; Tariwa (Guaycarí) culpa al calor, Biro-ko al ritual.
4. **Presión lingüística:** el objeto «el banco de peces que se desplazó» **no tiene palabra**
   (hueco léxico #2). Un pescador, presionado por describirlo, puede acuñar
   `[forma: componentes = 'los peces juntos que se mueven']` con la morfología viva. Ese
   neologismo es el dato valioso del experimento.

## 7. Por qué esto sirve al experimento lingüístico

El motor convierte los **huecos léxicos** de `ecologia_lexicon_map.md` de una lista en
**situaciones jugables**. La cadena crea la necesidad (un médano nuevo que cruzar, una costra
de sal que describir, una marea que anticipar, un cardumen sin nombre) y la lengua responde.
Los huecos con más «presión» (duna, cardumen, alisio, marea) son justamente los que el motor
toca cada turno — así que son los más probables de gatillar acuñación.

## 8. Alcance y cautelas

- **No implementar sin acordar el alcance.** Un motor continuo cambia la dinámica de tensión y
  podría afectar la comparación normal vs. ablación (ver CLAUDE.md). Convendría un flag para
  correr con motor / con catálogo estático y comparar.
- **Mantener la Capa 1 oculta de verdad:** si el estado ecológico se filtra al prompt del
  agente, se rompe el mecanismo (el agente «sabría» la causa física). Solo deben inyectarse
  señales de Capa 2.
- **Empezar mínimo:** una sola cadena (Alisio → Golfete → pesca → tensión → sueño) ya
  demuestra el patrón antes de modelar Salinar/Buco/Manglar.
- **Reusar lo existente:** los textos ricos de los eventos actuales de `curiana_state.py`
  siguen sirviendo como *plantillas de narración* cuando un umbral se cruza; el motor decide
  *cuándo*, el texto existente dice *cómo se cuenta*.

---

*Fundamento ecológico de cada variable: `curiana_sim/cultura/ecologia.yaml`
(entradas 005–010 clima/hidrología/salinas; 015–017 pesca/cardúmenes; 020–021 y 026–027
viento/corrientes/marea; 022 aves migratorias). Huecos léxicos: `ecologia_lexicon_map.md`.*
