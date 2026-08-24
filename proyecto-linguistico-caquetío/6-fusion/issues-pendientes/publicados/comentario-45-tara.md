## Tercera fuente independiente, y dice **langosta**. El conflicto se cierra.

La Tabla A-9 de Oliver 1989 (*Selected Caquetío Vocabulary from the XVIth
Century*, Apéndice A p. 593-594), leída sobre la imagen por Miguel el
2026-08-24:

```
tara | tara | langosta | locust
```

### El marcador queda en tres a cero

La propia nota de la entrada del lexicón ya lo decía todo:

> *"D10 (2026-08-03), grupo 2 — CONFLICTO DE GLOSA ABIERTO, la entrada NO se
> reescribe. La glosa activa («venado, ciervo») **no tiene fuente localizada**:
> no está en Zavala Reyes 2015, ni en van Buurt 2014, ni como lema en Alvarado
> 1921. En contra hay DOS fuentes independientes que coinciden: Zavala #238
> «Langosta, mariposa», y Alvarado p.283, donde tara vale polilla o mariposa.
> **Es el más fuerte de los tres conflictos**."*

| Lectura | Fuentes |
|---|---|
| insecto (langosta / mariposa / polilla) | **Zavala #238 · Alvarado p.283 · Oliver Tabla A-9** |
| venado, ciervo (*Odocoileus virginianus*) | **ninguna localizada** |

Oliver coincide con Zavala palabra por palabra: **langosta**.

## 🔴 Y aquí está el argumento del corpus que el issue avisaba que podía caer

`3-mundo/corpus/ecologia.yaml` usa `tara` dos veces, y la segunda es la grave:

```
:323  "La fauna de caza y de agüero del matorral seco: VENADO (tara), armadillo…"
:624  "La fauna de HOY no es la del siglo XV. El venado caramerudo (Odocoileus
       virginianus) —el 'tara' del lexicón caquetío atestiguado— hoy está
       ausente de gran parte…"
```

Ese segundo hecho es el **ejemplo insignia** de una regla metodológica que el
proyecto aplica en todas partes, formulada en `02_ecologia_golfete.md`:

> *"**No proyectar la fauna moderna hacia atrás.** Cuando el lexicón atestiguado
> nombra un animal hoy ausente (**tara**), la palabra manda sobre el censo
> actual."*

**Si `tara` es una langosta, el ejemplo se cae.** Las langostas no están
ausentes del Golfete, y una langosta no es un venado. La regla sigue siendo
buena — pero pierde su caso demostrativo, y hay que **rehacer el hecho, no solo
la glosa**.

## Qué habría que decidir

1. **Reescribir `tara`** en el lexicón: de "venado, ciervo (*Odocoileus
   virginianus*)" a **langosta** (con 'mariposa/polilla' como acepción de
   Alvarado, a decidir si es la misma palabra o vecina).
2. **Rehacer `ecologia-323` y `ecologia-624`.** El primero pierde el venado de
   su lista de caza; el segundo pierde su ejemplo entero y necesita otro — o
   pasa a enunciar la regla sin caso.
3. **Buscar la palabra caquetía del venado**, que queda huérfana. Puede ser
   hueco léxico declarado, que el corpus admite mejor que un dato inventado.
4. Revisar qué más cuelga de `tara`: hay un agente **Tara-sha** en el elenco.

⚠️ Nótese que este es el mismo patrón que `corie` (#46) y `mene` (#52): **una
glosa activa sin fuente localizada, sostenida contra dos o tres fuentes que
dicen otra cosa**. Merece medirse como categoría, no caso por caso.

Fuente: `6-fusion/tabla_a9_oliver.yaml` · `4-fuentes/oliver-1989-apendice-a.md`
