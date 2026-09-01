# Borrador — comentario para #39 (D11): el primer incremento del rebalanceo

> Publicar con:
> `gh issue comment 39 --body-file 6-fusion/issues-pendientes/comentario-39-primer-incremento.md`
> (quitando esta cabecera)

---

## El rumbo fijado el 2026-08-31, implementado — primer incremento

**La columna añú existe.** El lexicón tenía CERO entradas del pariente
costero más cercano; hoy tiene **46 paraujano** (Wilbert 1958-59, Sinamaica,
vía Oliver 1989 Tabla A-2) más **48 lokono nuevas** de la misma tabla
(227 → 275). Pipeline: `6-fusion/tabla_a2_transcripcion.yaml` →
`minar_a2_swadesh.py` → `lexicon_a2.py` (generado e importado, disciplina
zavala: `setdefault`, jamás pisa claves).

**La medición nueva**: con la categoría `paraujano` canónica, el filtro
fonotáctico entrenado en el caquetío atestiguado da

| columna | pasa |
|---|---|
| lokono | **82.9%** (subió de 79.3 con las 48 nuevas) |
| **paraujano (añú)** | **73.9%** |
| wayunaiki | 65.4% |
| castellano (control) | 44.7% |

El orden **lokono > añú > wayuu** es la señal B del cómputo, ahora con tres
puntos: el vecino geográfico inmediato queda en medio, y el parecido
estructural máximo sigue siendo con el lokono. (n añú = 46: leer con esa
reserva.)

**Colisiones como dato areal** (12, en `COLISIONES_A2`): el paraujano
comparte `pia` con el núcleo reconstruido, y 10 formas lokono de la A-2 ya
estaban importadas (biama, siba, hime, oniabo...) — la columna corrobora la
capa existente. Curación declarada: solo formas libres y limpias; ligadas,
reconstrucciones (*) y dudosas quedan en `REFERENCIA_A2` con motivo. Todo
con el caveat en notas: transcripción a ojo pendiente de segunda pasada.

## Lo que falta para cerrar D11

1. **Escala diccionario del lokono**: Pet 1987, Bennett 1989 y de Goeje 1928
   NO están en el repo (las 227 actuales los citan). Candidato interno sin
   minar: Perea Alonso 1942 (*Filología Comparada Arawak*, ya en
   `fuentes_caquetios/`).
2. **La A-1 entera**: el vocabulario añú completo de Wilbert (manuscrito,
   pdf ≤587) — la columna paraujano hoy es solo el Swadesh.
3. **Marie-France Patte** (adquisición) y la segunda pasada de Miguel sobre
   la A-2.
4. Las opciones (b) re-etiquetar y (c) repertorio del comentario anterior
   siguen abiertas; (a) rebalancear está en marcha.
