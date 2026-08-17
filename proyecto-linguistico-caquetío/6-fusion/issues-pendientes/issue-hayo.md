`hayo` = 'coca' está como `caquetío-atestiguado`, y Oliver lo marca como préstamo de Santa Marta.

## Qué dice hoy el lexicón

`curiana_sim/curiana_lexicon.py:322`:

```python
"hayo": {"es": "hayo, coca (Erythroxylum coca), hoja masticada ritual",
         "fuente": "caquetío-atestiguado",
         "notas": "Zavala Reyes 2015 #156 (HB): 'hierba quita sed'; cf. #154 hay (E) = coca. "
                  "Forma taína hayo documentada en Oviedo. RE-ETIQUETADO 2026-07-20: estaba "
                  "como taíno pese a figurar en el glosario caquetío",
         "categoria": "ritual"}
```

La entrada **estaba etiquetada como taíno** y la auditoría del 2026-07-20 la
ascendió a `caquetío-atestiguado`, con el argumento de que figura en el glosario
caquetío de Zavala.

## Qué dice Oliver

La **Tabla A-9 del Apéndice A** de Oliver 1989 —*"Selected Caquetío Vocabulary
from the XVIth Century"*, pp. impresas 593-594— incluye `hayo`, pero **en
cursiva**. Y cierra con esta nota al pie:

> *"(words in italics are probably not Caquetío, but from the Santa Marta area
> [chibchan?])"*

De las ~50 entradas de la tabla, **solo tres van en cursiva**: `icoroata`
(> caraota), `hayo` (la coca) y `raporón` (el calabacín con cal). Verificado
leyendo las páginas, no por OCR — el OCR no conserva cursivas.

**Las tres forman un paquete cultural coherente**: la coca, el recipiente de cal
para mascarla (el *poporo*) y una leguminosa. Es el complejo de la Sierra Nevada
de Santa Marta, que es justo la zona que Oliver nombra.

## Por qué la corroboración Zavala↔Oliver es aparente

Zavala #156 glosa `hayo` como *"hierba quita sed"*. Oliver glosa la cursiva
igual. **Coinciden en la glosa y discrepan en la filiación**: no es una segunda
atestación caquetía, es la misma palabra con dos juicios distintos sobre de
dónde viene. Que aparezca "en el glosario caquetío" de Zavala no la hace
caquetía si la fuente más autorizada la marca como préstamo.

## Por qué importa más de lo que parece

- La entrada es **`categoria: ritual`**: alimenta comportamiento ritual en la
  simulación, no es vocabulario decorativo.
- Es **exactamente el error de la regla 4** del CLAUDE.md — un rasgo de otra
  región entrando al canon costero sin marcarse.
- Y demuestra que **una cursiva puede pasar años dentro del canon sin que nadie
  la note**: el ascenso de julio fue en la dirección contraria a la evidencia.

## El marco correcto: préstamo EN el caquetío, no palabra ajena AL caquetío

Ojo con la conclusión fácil. **Las tres cursivas están dentro de un vocabulario
caquetío del s. XVI**: si Oliver las encontró ahí, es porque las fuentes las
recogieron *de boca caquetía*. La región era multilingüe con documentación
directa —Federmann 1530 necesitó **cinco traducciones encadenadas** con sus
intérpretes caquetíos (Jahn cap. V), y Esteves atribuye la toponimia de
Paraguaná a **nueve estratos**—, así que lo esperable es exactamente esto:
hablantes que manejaban varias lenguas según su zona, y palabras circulando
entre ellas.

**`hayo` probablemente se decía en caquetío. Lo que está en duda es su pedigrí,
no su uso.** La cuestión no es expulsarla del lexicón sino etiquetarla bien —
y el lexicón ya tiene precedente para esto: `jirajaroide-contacto` (7 formas),
`kalinago-caribe-overlay` (4).

## Qué habría que decidir

1. Qué etiqueta de préstamo le corresponde (¿`chibcha-contacto`? ¿algo tipo
   `santa-marta-overlay`? — coordinar con el cierre del vocabulario de `fuente`,
   #93). **No se propone retirarla del lexicón**: se propone que deje de contar
   como evidencia de léxico patrimonial caquetío.
2. ¿Se conserva en `categoria: ritual`? Argumento a favor: si los caquetíos
   usaban la palabra, el rasgo cultural pudo circular con ella — pero entonces
   el corpus de creencia debería registrar el complejo de la coca como rasgo
   **de contacto**, no patrimonial (y nótese que `raporón`, el poporo, no está
   en el repo: se absorbió la palabra suelta, no el complejo).
3. ¿Se revisa el resto de lo que tocó el re-etiquetado del 2026-07-20 con el
   mismo criterio? El criterio que falló fue "figura en el glosario caquetío de
   Zavala, luego es caquetío" — figurar en un glosario mide que el compilador
   la recogió, no la filiación.

Fuente: `4-fuentes/oliver-1989-apendice-a.md`.

---

**DECISIÓN (Miguel, 2026-08-16): se mantiene en el lexicón**, entendida como
**producto que venía de afuera** — como el oro: un bien del contacto chibcha
que circulaba en boca caquetía. Queda pendiente solo la etiqueta concreta
(¿`chibcha-contacto`, espejo de `jirajaroide-contacto`?), a coordinar con el
cierre del vocabulario de `fuente` (#93). Autorizada también la **revisión del
criterio del re-etiquetado 2026-07-20** (punto 3 de arriba).
