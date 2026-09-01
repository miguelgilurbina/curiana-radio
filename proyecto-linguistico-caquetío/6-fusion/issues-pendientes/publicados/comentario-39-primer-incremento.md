## El rumbo fijado el 2026-08-31, implementado — primer incremento (y verificado)

**La columna añú existe.** El lexicón tenía CERO entradas del pariente
costero más cercano; hoy tiene **47 paraujano** (Wilbert 1958-59, Sinamaica,
vía Oliver 1989 Tabla A-2) más **49 lokono nuevas** (227 → 276) de la misma
tabla. Pipeline: `6-fusion/tabla_a2_transcripcion.yaml` →
`minar_a2_swadesh.py` → `lexicon_a2.py` (generado e importado, disciplina
zavala: `setdefault`, jamás pisa claves).

**La transcripción quedó VERIFICADA por Miguel contra la imagen el
2026-09-01** (segunda pasada, celda por celda): sus correcciones —
`abonaba` por `ahonaha`, `-thina` por `-china`, cuatro «(?)» resueltos —
liberaron además tres entradas (`ithihi` 'sangre', `kougdo` 'grasa'). El
estado de verificación vive en el meta de la transcripción y todas las
notas del módulo lo heredan al regenerar.

**La medición nueva**: con la categoría `paraujano` canónica, el filtro
fonotáctico entrenado en el caquetío atestiguado da

| columna | pasa |
|---|---|
| lokono | **83.0%** (subió de 79.3 con las nuevas) |
| **paraujano (añú)** | **72.3%** |
| wayunaiki | 65.4% |
| castellano (control) | 44.7% |

El orden **lokono > añú > wayuu** es la señal B del cómputo, ahora con tres
puntos: el vecino geográfico inmediato queda en medio, y el parecido
estructural máximo sigue siendo con el lokono. (n añú = 47: leer con esa
reserva.)

**Colisiones como dato areal** (12, en `COLISIONES_A2`): el paraujano
comparte `pia` con el núcleo reconstruido, y 10 formas lokono de la A-2 ya
estaban importadas (biama, siba, hime, oniabo...) — la columna corrobora la
capa existente. Curación declarada: solo formas libres y limpias; ligadas,
reconstrucciones (*) y dudosas quedan en `REFERENCIA_A2` con motivo (125
fragmentos preservados).

## Lo que falta para cerrar D11

1. **Escala diccionario del lokono**: Pet 1987, Bennett 1989 y de Goeje 1928
   NO están en el repo (las actuales los citan). Candidato interno sin
   minar: Perea Alonso 1942 (*Filología Comparada Arawak*, ya en
   `fuentes_caquetios/`).
2. **La A-1 entera**: el vocabulario añú completo de Wilbert (manuscrito,
   pdf ≤587) — la columna paraujano hoy es solo el Swadesh.
3. **Marie-France Patte** (adquisición) — LA especialista del añú.
4. Las opciones (b) re-etiquetar y (c) repertorio del comentario anterior
   siguen abiertas; (a) rebalancear está en marcha.
