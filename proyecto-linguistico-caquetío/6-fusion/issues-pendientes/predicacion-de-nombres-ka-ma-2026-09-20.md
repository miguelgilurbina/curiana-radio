# `juri-ni` no es caquetío: un nombre se predica con `ka-`, no con aspecto

**Para que Miguel decida.** El corte de la clase de la raíz ya está aplicado y
medido: `juri` 'viento' deja de ser `cat: v_raiz` y por tanto `juri-ni` deja de
contar como arahuaco. Lo que queda abierto son **dos cosas distintas** que
conviene no confundir:

1. **La regla positiva**: declarar que la predicación de un sustantivo va por
   `ka-` (atributivo/existencial) y `ma-` (privativo). Hoy no está escrita en
   ninguna parte del canon de morfología, aunque los dos afijos sí están.
2. **Qué hacer con lo ya dicho**: los **227** usos de `juri-*` con aspecto que
   la base ya tiene.

---

## 1. El mecanismo, que el repo ya tiene y no usa para esto

[[van-buurt-2014]] §8 da `ka-` como localizador: *«hay, existe(n)»*, con
*Casibari* = 'hay rocas duras'. `morfologia.md` §2 ya lo registra («`ka-`
posesivo genérico / asociativo», con el apoyo insular independiente de van
Buurt) y `ma-` como «negativo / privativo», cognado directo del wayuu. La
achagua de [[neira-ribero-1762]] los usa igual: `macarray` 'seco',
`macarracataní` 'seco, estando seco', `mabayisa` 'desalado, sin sal',
`mairrenayisa` 'sin sangre'.

Lo que falta es la frase que ata las dos puntas: **para decir «hay viento» o «es
ventoso», un nombre no toma aspecto — toma `ka-`**. `ka-juri` 'hay viento',
`ma-juri` 'sin viento'.

## 2. Los agentes agarraron la vía mala, y está medido

Los agentes usan `ka-` y `ma-` **mucho** en general: 102 formas / 564 usos con
`ka-`, 190 formas / 2.195 usos con `ma-` en toda la base (`ma-biro` 112,
`ka-biro` 99). Pero **casi nunca sobre estos treinta nombres**:

| vía, sobre los 30 nombres/adverbios reclasificados | formas | usos |
|---|---:|---:|
| **aspecto** (nombre + `-ka`/`-ni`/`-da`) | 70 | **617** |
| `ma-` | 12 | 57 |
| `ka-` | 4 | **6** |

`ka-juri` **3** usos contra `juri-ni` **157**. Con el viento —el recurso que da
nombre al Tiempo de Viento de la era 2— la comunidad eligió el molde equivocado.

**Y no es culpa del agente: el instrumento se lo permitía.** `juri` llevaba
`cat: v_raiz` por la heurística del cajón de resto, así que `juri-ni` puntuaba
como arahuaco y `juri-bana`, `juri-uco`, `juri-aima` también, todos por tener
una «raíz verbal» delante.

## 3. Lo que el motor YA hace bien, sin tocar nada

`es_arahuaco()` acepta los cuatro prefijos `ta-`, `wa-`, `ma-`, `ka-` sobre
cualquier forma activa. Comprobado token a token con el scorer, **después** del
corte:

| token | ¿cuenta como arahuaco? |
|---|---|
| `juri` | sí |
| `ka-juri`, `ma-juri`, `ta-juri` | **sí** |
| `juri-ni`, `juri-ka`, `juri-bana` | no |
| `biro`, `kasi` (nombres atestiguados) | sí |
| `biro-bana`, `kasi-bana` | no |
| `apo-ni`, `usera-ka`, `were-ni` (estativos y verbos) | sí |

**El corte cierra la puerta mala y deja abierta la buena.** Y enseña otra cosa:
`biro-bana` y `kasi-bana` tampoco contaban antes — un nombre con sufijo
locativo **nunca** contó, salvo para las 49 que llevaban `v_raiz` por accidente.
Así que esto no le pone a `juri` una penalización nueva: **le quita un
privilegio que ningún otro nombre del lexicón tenía**.

> ⚠️ Residuo declarado, que es OTRA pregunta: el scorer tampoco cuenta
> `biro-bana` 'cerro de la sal', que es el **ejemplo literal** de
> `IDENTIDAD_LINGUISTICA` desde el 2026-09-19. Si nombre+locativo debe contar
> es una decisión de diseño del scorer, no del minador, y no se toca aquí —
> `score_linguistico()` no se movió en esta tanda.

## 4. Qué hacer con los 227

`juri-*` con aspecto: **227 usos** en tres formas (`juri-ni` 157, `juri-ka` 37,
`juri-da` 33), repartidos así:

| serie | usos |
|---|---:|
| era 1 (sin serie) | 45 |
| era 2 serie B | 26 |
| **era 2 serie C** | **156** |

Contando todos los sufijos y no sólo el aspecto, la familia `juri-*` son **47
formas y 407 usos** que dejan de contar. Sobre las 29 reclasificadas como
nombre, 265 formas y 999 usos; con `popoi` (adverbio) aparte, 15 y 119. En
total, **280 formas y 1.118 usos** dejan de contar como arahuacos.

**Tres salidas:**

- **(a) Dejarlo.** Es lo que el proyecto ha hecho en los cuatro cortes
  anteriores («los runs ya corridos no se reescriben»), y el corte queda
  declarado en la bitácora para quien compare.
- **(b) Releerlo.** Una bandera como `analizar_runs.py --raices`: la base **no**
  se reescribe, pero se puede preguntar cuántos usos guardados tienen hoy otra
  lectura. No destruye nada y hace medible el agujero.
- **(c) Marcarlo.** Reescribir `source_language` de esas filas a un valor que no
  sea una lengua, como se hizo el 2026-09-20 con `desconocida` y `acuñada`.

**Recomendación del escriba: (a) o (b), no (c).** El caso no es el mismo que el
de `lumina`. Una raíz latina **no era caquetía nunca**, y por eso decir
«desconocida» era corregir una mentira sobre la lengua. `juri` **sí** es
caquetío atestiguado (Zavala #178, compilador Esteves): la fila dice la verdad
sobre la lengua y miente sobre la **morfología**. Meter las dos cosas en la
misma columna la haría ilegible.

## 5. Qué pide esta propuesta

- [ ] **La regla**: ¿se declara en `morfologia.md` que la predicación de un
      sustantivo va por `ka-`/`ma-` y no por aspecto? (Va junto con la sección
      de la clase estativa: `la-clase-estativa-2026-09-20.md`.)
- [ ] **¿Se enseña?** Si se declara, ¿entra en `prompt_reglas_completo`? Eso
      cambia lo que el agente lee y es un corte de serie aparte, con su propia
      medición de longitud de prompt (r = −0,48).
- [ ] **Los 227**: (a) dejar, (b) releer o (c) marcar.

Datos: `6-fusion/clases_de_raiz_zavala_2026-09-20.yaml` §2.
Números: `6-fusion/medicion_clases_de_raiz_2026-09-20.yaml` §`juri_y_los_nombres`
y §`paradigma_en_la_base`.
Corte declarado: punto 12 del «Cambio de instrumento» de
`5-experimento/BITACORA_RUNS.md`.
