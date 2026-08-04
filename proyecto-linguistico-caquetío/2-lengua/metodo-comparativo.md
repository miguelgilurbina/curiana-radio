---
tipo: nota-viva
ambito: reconstrucción por método comparativo
fuente_de_verdad: curiana_sim/arahuaco_comparative.py
cognados_curados: 37
pares_validacion: 18
candidatas_aisladas: 441
medido: 2026-08-04
---

# El método comparativo

> Cómo se reconstruye una palabra caquetía cuando **no hay dato caquetío**. Es
> la Capa 2 del proyecto, y la que más ha fallado — por buenas razones que
> conviene tener escritas.

## Las piezas

`curiana_sim/arahuaco_comparative.py`:

| Pieza | Qué es | n |
|---|---|---:|
| `COGNADOS` | **El único set curado.** Entradas con correspondencia verificada entre lenguas arahuacas. | **37** |
| `CORRESPONDENCIAS` | Tabla de correspondencias fonológicas derivada | 1348 |
| `PARES_VALIDACION` | Pares reales con forma esperada — la suite de regresión | **18** |
| `REGLAS_*` | Nueve juegos de reglas de transducción direccionales | ver abajo |

Los juegos de reglas, con su tamaño:

| Regla | n | | Regla | n |
|---|---:|---|---|---:|
| `REGLAS_WY_CQ` | 15 | | `REGLAS_LK_WY` | 15 |
| `REGLAS_LK_CQ` | 14 | | `REGLAS_WY_LK` | 12 |
| `REGLAS_TN_CQ` | 10 | | `REGLAS_LK_TN` | 12 |
| `REGLAS_LK_KL` | 15 | | `REGLAS_TN_LK` | 6 |
| `REGLAS_KL_LK` | 6 | | | |

## La suite de validación

```bash
cd curiana_sim && python -c "import arahuaco_comparative as A; A.validar()"
# 18/18 pares validados
```

Los 18 pares están en verde. Es una suite de **regresión**, no de descubrimiento:
prueba que las reglas siguen reproduciendo las formas que ya se sabían. Los pares
LK→TN salieron de la minería de [[brinton-1871]], que además **corrigió un bug
en `REGLAS_LK_TN`**. ([[perea-alonso-1942]] no dio nada: es gramática lokono
pura, no comparativa.)

## Las 441 candidatas y el 80 % de fallo

`reconstruir_caquetio_gaps.py` transdujo **cualquier** palabra hermana con la
misma glosa española, **sin verificar cognación** contra `COGNADOS`. Resultado:
441 formas `hipotético-no-verificado`.

`minar_pares_validacion.py` las contrastó contra pares objetivos (caquetío
atestiguado + cognado hermano) y midió **~80 % de fallo**. Están aisladas en
`lexicon_candidatos.py` desde 2026-06-28: fuera del lexicón, fuera de Supabase,
fuera del scoring. Ver [[lexicon]] §candidatas.

**La lección, escrita para no repetirla:** una regla fonológica plausible
aplicada a una glosa coincidente **no es un cognado**. Sin cognación verificada,
la transducción produce una palabra que suena arahuaca y no significa nada. Es
la misma "regla cero" que gobierna la segmentación toponímica ([[toponimia]]).

## Lo que aportó Oliver cap. 2

La minería de [[oliver-1989-cap2]] (`cognados_oliver.py`) es la más productiva y
la más incómoda: **corrigió al proyecto en dos puntos de fondo**.

| Salida | n |
|---|---:|
| `COGNADOS_OLIVER` — sets de cognados | **16** |
| `CORRESPONDENCIAS_OLIVER` — correspondencias fonológicas | **14** |
| `PARES_VALIDACION_OLIVER` — pares nuevos | **10** |
| `NUEVAS_ENTRADAS_CAQUETIO` | 5 (`auri`, `barisi`, `ada`, `adabacoa`, `daitiao`) |
| `REVISIONES_REGLAS` — veredictos sobre reglas existentes | 5 |

### Los 10 pares nuevos: pasan 3

Corridos contra las reglas actuales, **3 de 10** reproducen la forma esperada
(`balisi→palisi`, `bii→pii`, `ada→ada`). Los otros 7 fallan, y **fallan
informativamente**: cada fallo señala una regla mal calibrada. Issue
[#44](https://github.com/miguelgilurbina/curiana-radio/issues/44).

### R13, falsificada

**`REGLAS_LK_CQ` R13 — `^d(?=[aeiou]) → t` — está falsificada.** Issue
[#43](https://github.com/miguelgilurbina/curiana-radio/issues/43).

El dato: CQ `dare` : LK `d-ari` (p.147); CQ `diao`, `datihao`, `dato`
(pp.146-147). Oliver sitúa el prefijo /dA-/ de 1.ª persona en lokono, taíno y
probablemente caquetío (p.136). **El caquetío conserva /d-/**; el paso a /t-/ es
la innovación **guajiro-paraujana**. La regla estaba haciendo caquetío a partir
de wayunaiki y devolviendo formas guajiras.

Otras cuatro revisiones del mismo lote: `REGLAS_LK_CQ` R5/R9 (`b → p`)
**degradada** —hace falta para 'mar' (`para` : LK `bara`) pero produce la forma
guajira en todo lo demás—; `REGLAS_WY_CQ` R4 (`sh → ch`) **sospechosa** —los
fonemas /ch/, /ñ/, /sh/ guajiros son recientes—; `REGLAS_LK_WY` R7 (`r → l`)
**sin fundamento fonológico**, es convención de transcripción; `REGLAS_WY_LK` R9
(`^w → b`) **corregible** a `^w → o`.

## El desbalance wayunaiki / lokono

**La decisión más de fondo del proyecto ahora mismo.** D11 en
[[DECISIONES_ABIERTAS]] · issue
[#39](https://github.com/miguelgilurbina/curiana-radio/issues/39).

### El hecho

El lexicón se construyó sobre la premisa de que el **wayuunaiki** es la hermana
más cercana del caquetío. **Oliver dice lo contrario**, y está en el capítulo
que el proyecto declara su pilar teórico:

> *"it seems reasonable, for the moment, to regard Caquetío as emerging from a
> similar background to that of Lokono rather than from a Guajiro-Paraujano
> ancestry"* — [[oliver-1989-cap2]], p. 150

Sus pilares: (1) el prefijo de 1.ª persona **/dA-/**, que solo lokono y taíno
tienen —el guajiro-paraujano innovó /tA-/—, con evidencia caquetía en `diao`,
`datihao`, `dare`, `dato`; (2) la innovación léxica `auri` 'perro', de
distribución norteña; (3) `kaketío` 'ser vivo' = lokono `kakïtho`; (4) menor: el
sufijo caquetío es **`-bana`, no `-pana`**, como el lokono. Y en negativo: los
topónimos Guajira-Falcón muestran *"far more differences in sound sequences than
similarities"*.

### La composición real, medida el 2026-08-04

| Lengua | Entradas |
|---|---:|
| **wayunaiki** | **781** |
| **lokono** | **227** |
| taíno | 57 |

**3,4 a 1 a favor de la hermana que Oliver considera la más lejana.** Y el sesgo
se repite, amplificado, en las candidatas: **388 de las 441 (88 %) se
transdujeron solo desde wayunaiki**, contra 46 solo desde lokono. Eso explicaría
buena parte del ~80 % de fallo: **se reconstruía desde la lengua equivocada**.

### El error de atribución que esto corrigió

La nota de fuente `oliver-1989-cap2.md` afirmaba —y [[01_familia_caquetia]] §2
se apoyaba en ello— que Oliver *"confirma que las dos hermanas más cercanas del
caquetío son el wayuunaiki y el paraujano"*. **Oliver dice lo contrario.** Lo
que sí dice es que guajiro y paraujano son **entre sí** las dos lenguas
arahuacas más próximas conocidas (64,2 % de vocabulario básico compartido,
separación mínima de 1,0 milenio). Es una afirmación sobre **ellas dos**, no
sobre el caquetío. `ANCLA_ARCO_NORTENO` en `cognados_oliver.py` guarda las citas
con página.

Distancias que Oliver sí mide: lokono–guajiro 31,3 % · 2,6 milenios ·
lokono–achagua 18 % · 3,8 milenios · lokono–island carib 43,7-52,5 %.
**Caquetío: sin medir** — no hay lista de 100 palabras. La posición de Oliver es
cualitativa y explícitamente *"tentative"*.

### Las opciones

- **(a) Reequilibrar hacia el lokono** — lokono como fuente primaria de
  transducción, wayuunaiki como secundaria. Implica re-derivar candidatos y,
  con ellos, buena parte de la Capa 2.
- **(b) Mantener el wayuunaiki como primario** y documentar que es una decisión
  **de disponibilidad** (el wayuu está mucho mejor documentado y vivo), no **de
  filiación**.
- **(c) Ponderar por concepto** — usar el que tenga cognado atestiguado en cada
  caso, con el lokono desempatando.

**Lo que no cambia:** el wayuu sigue siendo la comparanda **etnográfica** central
y bien fundada. Todo el corpus cultural —creencia, transmisión, parentesco— se
apoya en etnografía wayuu, y eso **no depende de la filiación lingüística**. El
arco norteño es matrilineal de punta a punta; el lokono también lo es. Lo que se
mueve es de quién se reconstruye **la lengua**.

## Enlaces

[[lexicon]] · [[morfologia]] · [[toponimia]] · [[DECISIONES_ABIERTAS]] · [[oliver-1989-cap2]] · [[oliver-1989-cap3]] · [[brinton-1871]] · [[perea-alonso-1942]] · [[adam-1879]]
