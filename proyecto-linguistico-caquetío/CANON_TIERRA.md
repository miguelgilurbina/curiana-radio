# Ritos como mecanismo de transmisión — propuesta

**Estado:** diseño, nada implementado todavía. No es canon etnohistórico (eso
ya vive en `curiana_sim/CULTURA_CAQUETIA.md`, que es mucho más completo de lo
que yo había escrito aquí la primera vez — esta versión ya no repite esa
parte). Esto es: cómo convertir los ritos que **ya existen como eventos**
en un mecanismo medible, para que correr la simulación durante años permita
observar cómo se traspasa la tradición oral, no solo narrarla.

## El punto de partida: ya existen, solo no hacen nada todavía

`curiana_state.py::EVENTOS_ESTACIONALES` ya tiene tres ritos escritos:

- `ceremonia_iniciacion` — Dare-nu y Daru, con Manaure/Shaboro/Paugis-sha.
- `ritual_siembra_primeras_lluvias` — Shaboro guía, Corie-ko espera la señal.
- `fiesta_cosecha_chicha` — "los viejos cuentan las hazañas de los ancestros".

Hoy, cuando el Director elige uno de estos eventos, lo único que pasa
mecánicamente es: se narra, cambia `nivel_tension`/`nivel_alimentos`, y los
`agentes_involucrados` hablan ese turno. No hay nada que distinga "esto fue
un rito" de "esto fue cualquier otra escena". No se mide si lo dicho ahí
vuelve a aparecer después. Por eso, aunque la lore ya está, **el rito no es
todavía un mecanismo de transmisión** — es una escena suelta.

## Qué le falta para serlo

1. **Un concepto a transmitir, no un guion.** Cada rito apunta a una idea
   (de `CULTURA_CAQUETIA.md` o de la nueva sección "Fuerzas en tensión") —
   ej. `ceremonia_iniciacion` → la responsabilidad del *barsure* y el
   piazgo; `ritual_siembra_primeras_lluvias` → la lógica de reciprocidad con
   la tierra (Pulowi/Juyá). El piache lo dice en sus propias palabras, en
   caquetío — igual que ya improvisa todo lo demás. El canon da el concepto,
   no la frase.
2. **Pulso de exposición fuerte, no incremental.** `DifusionLexica.propagar_uso()`
   ya sube la exposición de los vecinos proporcional a prestigio × vínculo.
   Un rito con `toda_la_comunidad` o varios `agentes_involucrados` a la vez
   debería propagar como si todos fueran vecinos directos del piache ese
   turno — un testigo de la ceremonia no absorbe la idea por ósmosis lenta,
   la recibe de golpe. Cambia la magnitud del pulso, no el mecanismo.
3. **Memoria que no se cae del rolling buffer.** `AgentMemory` hoy es una
   lista corta que rota. Lo visto/oído en un rito necesita un segundo
   compartimento que no expira — para que alguien pueda referenciarlo
   turnos, días o años después. → Este compartimento es el `IdiolectoAgente`
   diseñado en [`DISENO_KOINE.md`](DISENO_KOINE.md) §5: lo que arraiga en la
   memoria larga es lo que se fija en la koiné.
4. **El Observer registra el rito como evento propio**, no como una
   respuesta más: quién lo ofició, qué concepto cargaba, qué neologismo (si
   alguno) se acuñó ahí. Tabla nueva, paralela a `neologisms`.
5. **Medir el eco, no solo el origen.** En turnos/días/años posteriores, el
   Observer puede buscar si otros agentes —sobre todo quienes solo
   *presenciaron*, no oficiaron— repiten o aluden al concepto o la forma
   acuñada. Eso es el dato real: ¿sobrevivió? ¿se simplificó? ¿en quién se
   detuvo la cadena? Es la respuesta concreta a "cómo se traspasa la
   tradición oral", no una metáfora.

## El hueco que encontré al revisar el código: no hay envejecimiento

`edad` y `tier` son estáticos — nada los actualiza con los días simulados.
Eso importa para lo que pides: una transmisión verdaderamente
*generacional* (Daru pasa de niño-testigo a iniciado a, eventualmente,
quien algún día oficia para otro niño) necesitaría que `edad` avance con
`state.dia` y que un agente pueda cruzar de tier 3→2 en algún umbral —
mecánica que hoy no existe en absoluto.

Sin eso, un run de años todavía mide algo real (¿la MISMA gente, con el
tiempo, sigue repitiendo/derivando el mismo concepto?), pero no captura
"un niño se convierte en quien transmite" — la pieza más fuerte de lo que
describes.

## Próximos pasos posibles (sin implementar nada todavía)

- **Opción A — alcance acotado:** construir 1-4 sin envejecimiento. Mide
  fidelidad/deriva de un concepto a través del tiempo entre los agentes que
  ya existen. Más rápido, ya es un resultado real.
- **Opción B — alcance completo:** sumar envejecimiento + promoción de tier
  como prerrequisito, para que la transmisión sea literalmente
  intergeneracional. Más trabajo, pero es lo que de verdad pediste.

## Fuentes

(las de cosmovisión/clima ya se movieron a `curiana_sim/CULTURA_CAQUETIA.md`)
