# D11 fase 3: los pronombres y el aspecto, sacados del wayuu — qué forma entra en cada casilla

Miguel, 2026-09-23 (cc.12):

> «los pronombres y aspectos siguen reconstruidos desde el Wayu. Esto, no
> podemos seguir teniendo reconstrucciones desde el Wayu, tendría que ser desde
> el Locono. O el Taíno […] o el Achagua también, que tienen una relación más
> eh, de parentesco, mucho más grande […] eso sí o sí lo tenemos que hacer»

**La decisión está tomada.** Esto es cómo se aplica: qué forma entra en cada
casilla, con qué cita y cuánto cuesta. Las formas, las citas y las etiquetas
están en `6-fusion/propuesta_d11_fase3_pronombres_aspectos_2026-09-23.yaml`.
Las cifras están en `6-fusion/medicion_d11_fase3_2026-09-23.yaml`, que emite
`6-fusion/scripts/medir_d11_fase3.py`. Se midió contra el motor de
`tanda/base-2026-09-22` (#202), que es sobre el que caería la tanda.

Esta propuesta no toca el motor ni el canon (regla 5). Lo aplica el
coordinador en una tanda, y la mide antes.

---

## Lo corto

1. **Pronombres:** `dai` (yo) · `bui` (tú) · `lihi` (él) / `tuhu` (ella, ello)
   · `waya` (nosotros) · `naya` (ellos).
   - Los tres primeros son lokono tal cual.
   - `waya` y `naya` **se quedan**, porque el achagua los da letra por letra.
   - `kudanga` y `kuté` siguen como están.
2. **Aspecto:**
   - el verbo solo = lo que pasa ahora;
   - **`-kuba`** = ya pasó;
   - **`-ba`** = vendrá.

   `-ka`, `-ni` y `-da` se retiran.
3. **Evidencia:** las seis formas (cinco casillas, con la 3sg partida) tienen
   detrás una forma documentada en una de las tres hermanas.
   - Tres son reconstruidos: `dai`, `waya` y `naya`.
   - Tres son hipotéticos: `bui`, `lihi` y `tuhu`.
   - En el aspecto **no hay nada caquetío, ni taíno**. Las candidatas son
     todas hipotéticas.
4. **Coste:** es el mayor corte de serie que ha tenido el proyecto.
   - `taya` sale en 3.750 de las 3.811 respuestas de la base.
   - Los tres aspectos suman 34.213 usos en 538 formas.
   - No rompe el instrumento si el desafijador sigue pelando los sufijos
     viejos. Así cambian de núcleo 5 formas y ninguna cambia de veredicto.

---

## Primero, lo que resultó falso al medirlo

- **«`daca` 'yo' tiene dos cronistas independientes».** Es falso.
  - Las Casas cita a Pané en la misma página: «Todo esto refiere fray Ramón
    haber de los indios entendido» (*Apologética* p. 447). El episodio es el
    mismo de Pané, cap. XXV.
  - La frase viene de Pané. La glosa «daca quiere decir yo» sí es de Las Casas.
  - La única segunda atestación independiente es la frase de Esquivel que trae
    Goeje 1939, p. 17. Goeje no dice de qué cronista la saca.
  - La nota de `daca` en la tanda de la base y la lista maestra taína lo
    cuentan como dos cronistas.
- **«Los posesivos `ta-`/`wa-` vienen del mismo sitio».** Sólo `ta-`.
  - `wa-` lo dan el lokono, el achagua (`Gua-`), el taíno según Goeje y el
    kalinago.
- **«El `-ka` completivo».** Además de venir del wayuu, el valor está al revés
  del de las hermanas.
  - En lokono, `-ca` vale igual en presente y en los tres pretéritos, y el
    tiempo lo pone el adverbio (Perea p. 628). Es la raíz de «ser, estar»
    (p. 584).
  - En kalinago es «Présent -ka» (Goeje p. 26).
- **«Retirar `-ka`/`-ni`/`-da` es cambiar tres claves».** No es neutro.
  - Si salen del desafijador, 30 formas (351 usos) que hoy son «raíz de
    ninguna parte» pasan a raíz conocida. Pasa con `uyama-ni`, `duka-ni` o
    `güere-ni`.
  - La causa: `ka` y `ni` son claves del lexicón.
- **`wai`, el 'nosotros' lokono, choca.** Bajo `fonemizar` tiene el mismo
  esqueleto que `way`, caquetío atestiguado «árbol parecido a la ceiba»
  (Zavala #147).
- **De paso:**
  - `nüma` no pasa ni el filtro fonotáctico del caquetío atestiguado: la `ü`
    está fuera del inventario.
  - Oliver p. 147 llama a `gua-` «third person plural marker». Eso va contra
    el lokono y contra su propia glosa del mismo párrafo, «my or our
    kinsperson». `NUDO_DAITIAO` lo copia sin aviso.
  - El `gua-` de Goeje está en la p. 16, no en la 17.

---

## Cómo se decidió cada casilla

**El criterio es el de la propuesta del 09-13, con un solo cambio.** El criterio
(a) decía «lokono y achagua concuerdan en el prefijo, y la forma libre está en
una de las dos». cc.12 nombra **tres** hermanas, así que aquí se lee «dos de las
tres». Sólo afecta a la 1sg, donde lokono y taíno concuerdan en `da-`. Si no se
acepta, `dai` baja a hipotético y no se mueve nada más.

**Las correspondencias que se usan son sólo las que el repo ya declara**
(`cognados_oliver.py`):

| Correspondencia | Qué dice | Dónde |
|---|---|---|
| C1 | */nV-/ > /dA-/ en lokono, taíno «and perhaps Caquetío» | Oliver p. 136; traza caquetía en *dare* 'diente', p. 147 |
| C3 | el caquetío tiene la *b* lokona donde el wayuu tiene *p* | Oliver pp. 119, 150 |
| C8 | *r* ~ *l* es indecidible | Oliver p. 105 |
| C9 | las vocales quedan fuera del método | Oliver p. 105 |
| D5c | *gua* = /wa/ | — |

Por C9, la base del pronombre libre (-i, -ka, -ya) **no se deriva**. Se toma
documentada de una hermana. Por eso el paradigma mezcla la -i lokona con la -ya
achagua, y se dice en vez de igualarlo.

El **kalinago** (Goeje 1939) y el **maipure** (Gilij) se citan como apoyo, no
como base: no están entre las tres que nombró Miguel.

---

## Los pronombres

| Casilla | Hoy (wayuu) | Lokono | Taíno | Achagua | Recomiendo |
|---|---|---|---|---|---|
| yo | `taya` | `da-i` (Perea p. 573: «Sg. 1 cm. da- i , da-kia = yo.»; igual en los tres moravos, p. 581) | `daca` (Las Casas p. 447: «daca quiere decir yo») | `Nuya`, `Nu-` (pliego 8, p. 2-3) | **A `dai`** |
| tú | `pia` | `bu-i` (p. 573: «bu-i, bo-kia = tú»; p. 581) | — (sólo Coll y Toste, sin cronista) | `Jia`, `Ji-` (p. 3) | **A `bui`** |
| él / ella | `nüma` | `li-hi` vr. / `tu-hu` nv. (p. 573) | — | `Ria` / `Ruya` (p. 3) | **A `lihi` / `tuhu`** |
| nosotros | `waya` | `wa-i` (p. 573) | `gua-` (Goeje p. 16) | `Guaya` = /waya/ (p. 3) | **A `waya`** |
| ellos | `naya` | `na-i` (p. 573) | — | `Naya` (p. 3) | **A `naya`** |

### Yo

- **A · `dai`** — *reconstruido*.
  - El prefijo `da-` sale de C1: lokono = taíno, con traza caquetía en *dare*.
  - La forma libre está en lokono tal cual.
  - Clave libre, cero colisiones. **Recomendada.**
- **B · `daka`** — *reconstruido*, con el mismo apoyo.
  - Es la forma taína con grafía fonémica.
  - Pero duplica `daca`, voz taína del lexicón con la misma glosa. El agente
    que escriba «daca» sumaría préstamo de esfera, y el que escriba «daka»,
    caquetío.
- **C · `daya`** — *hipotético*.
  - `da-` + la base -ya del achagua. Es composición nuestra (la preferida del
    09-13).
- **D · `daca` tal cual**, marcada como taína.
  - El «yo» dejaría de contar como caquetío en cada frase.
  - Un pueblo no toma prestado su «yo».

### Tú

- **A · `bui`** — *hipotético*.
  - Es la forma lokona tal cual, igual en los tres moravos.
  - La *b* va por C3. Clave libre. **Recomendada.**
- **B · `bia`** — *hipotético*.
  - Es *b* + la base -ia del achagua. Composición.
  - `bia` es clave lokono: hay que renombrarla.
- **C · dejar `pia`.**
  - La única hermana no wayuu que la da es el maipure (Gilij p. 186), que no
    es una de las tres.
  - Además va contra C3.

`kudanga` sigue siendo el trato formal (d21.10).

### Él / ella

Las tres hermanas distinguen el género en el pronombre: lokono, achagua y
kalinago. **Ninguna tiene un 3sg sin género.**

- **A · `lihi` (hombre) / `tuhu` (mujer, animal, cosa)** — *hipotético*. Es el
  par lokono tal cual. **Recomendada**, con tres costes:
  1. **Reabre d21.13** en lo que toca al pronombre. El género de los nombres
     (-ti/-tu) sigue sin importarse.
  2. Hay que renombrar la clave lokono `tuhu`.
  3. El agente tiene que elegir el género.
- **B · sólo `tuhu`** — *hipotético*. Es la forma no varonil, que en lokono es
  la clase amplia (Perea p. 554). Es convención nuestra.
- **C · sólo `lihi`** — *hipotético*. Es convención nuestra.

Recomiendo A porque es la única que no inventa: cualquier forma única es una
convención. Si no se quiere reabrir d21.13, B antes que C.

### Nosotros / ellos

- **`waya` y `naya` se quedan (A).** Lo que cambia es la justificación: el
  achagua da *Guaya* y *Naya* tal cual, y el lokono concuerda en el prefijo.
  Son *reconstruidos*.
- **B** serían las formas lokonas, `wai` y `nai`. `wai` choca con `way`, y las
  dos cambian formas usadas sin ganar evidencia.

---

## El aspecto

**El taíno no tiene ni una marca de aspecto atestiguada.** Es un cero
verificado en la lista maestra y en Goeje §VII. Así que aquí la opción «la forma
de la esfera tal cual» no existe.

**Y las dos gramáticas que dan paradigma dudan de él:**

- Perea, p. 606: «todo el mecanismo temporal de los pretéritos sea tan sólo uno
  de los tantos perfeccionamientos a priori de los misioneros».
- Neira y Ribero, p. 28: «el pres.te de Indicativo es el q.e hace el gasto».

Toda candidata que salga del aparato de tiempo lleva esa sospecha.

| Casilla | Hoy | Lokono | Achagua | Kalinago (apoyo) | Recomiendo |
|---|---|---|---|---|---|
| ahora | `-ni` | presente en -a (p. 605); `-ca` sin tiempo, «por ciertos adverbios» (p. 628) | presente llano, «hace el gasto» (p. 28); gerundio `-cata` (p. 27) | «Présent -ka» (p. 26) | **A: sin marca** |
| ya | `-ka` | `-bi` inmediato (p. 605), `-cuba` remoto (p. 606) | `-mi` «nota de cosa ya pasada» (p. 5) | «Parfait -kuba» (p. 26) | **A `-kuba`** |
| vendrá | `-da` | `-pa` (Schumann, p. 606); `-fa`, `-ba` (Goeje, col. A) | partícula `ba` (pliego 24 der.); `su`/`saba` | «Futur -u-ba» (p. 26) | **A `-ba`** |

### Ahora (hoy `-ni`)

- **A · sin marca.**
  - El verbo solo es lo que pasa. El tiempo lo dice el adverbio.
  - Es lo que las dos gramáticas dicen que hacía el hablante.
  - Quedan dos marcas y el componente de aspecto sigue topando en 2.
  - La koiné pierde su sufijo por defecto (`_ASPECTO_SUFIJO`).
  - **Recomendada.**
- **B · `-kata`**, el gerundio achagua.
  - Conserva las tres marcas. Tiene una sola hermana.
- **C · `-ka` con el valor de las hermanas (presente).**
  - 🔴 La misma forma cambiaría de significado a mitad de serie. Los 8.466
    usos de `-ka` se dijeron como «ya».
- **D · `-bo`**, el lokono de Pet 1987.
  - `bo` es clave lokono.
  - Pet no está en la bibliografía.

### Ya (hoy `-ka`)

- **A · `-kuba`** — lokono `-cuba` = kalinago `-kuba`.
  - Dos hermanas, la misma forma, las dos de pasado. Cuatro letras.
  - Hay que renombrar la clave lokono `kuba`. Si no, el `kuba` suelto se cuenta
    como caquetío.
  - En lokono es el pasado **remoto**.
  - **Recomendada.**
- **B · `-bi`**, el pretérito inmediato lokono, «he andado».
  - Es el valor más cercano, pero tiene una sola hermana.
  - `bi` es clave lokono («tú») y `Raka-bi` es nombre de la era 1.
- **C · `-mi`**, el achagua «cosa ya pasada».
  - El autor lo pone también en los nombres. Es lo único del bloque que no
    sale de la rejilla latina.
  - Una sola hermana. `mi` suelto es la palabra castellana.
  - Es la alternativa si pesa más «aspecto, no tiempo».

### Vendrá (hoy `-da`)

- **A · `-ba`.**
  - Coinciden en la forma el achagua, el kalinago y la columna lokona de Goeje.
  - Es la mejor apoyada del bloque. Se deja en hipotético por las formas
    cortas.
  - **Recomendada.**
- **B · `-pa`**, el Schumann de Perea. Es la más antigua.
- **C · `-su`**, achagua. Es stopword castellana.

---

## Lo que no se nombró y es del mismo origen

No lo decido; lo pongo aparte.

- **El posesivo `ta-` 'mi'.**
  - Su único apoyo es el wayuu.
  - La sustituta por C1 es **`da-`** (lokono *da-si-kua* 'mi casa', p. 587). Se
    etiquetaría reconstruido, con el mismo apoyo que la 1sg.
  - `ta-` tiene 7.590 usos en 299 formas.
  - Si la 1sg pasa a `dai` y se queda `ta-`, el mismo «yo» se enseña con dos
    consonantes.
- **El plural `-kana`.** No tiene sustituta limpia:
  - el lokono usa `-nu` y no da plural a los irracionales;
  - el achagua tampoco pluraliza lo inanimado.

  Merece campaña propia.
- **El resto de las voces wayuu.** De las 23 de la deuda D11, 16 siguen en el
  habla y la plantilla enseña 15. Fuera de los pronombres:
  - **`kashi`** 'ahora', 3.187 usos;
  - **`yama`** 'aquí', 1.814;
  - **`sulu`** 'adentro', 1.577.

  Son palabras gramaticales, y si el presente pasa a no marcado, son justo los
  adverbios que dirían el tiempo. También `wana` 'ver', que está en el ejemplo
  de IDENTIDAD que reciben los 63. Merece otra campaña corta.

---

## Cómo se aplica sin romper el instrumento

Todo esto está medido.

1. **Es corte de serie.** Nada de lo dicho se reescribe, y se declara en
   BITACORA_RUNS.
2. **El desafijador sigue pelando** `-ka`, `-ni`, `-da` y `ta-` aunque ya no se
   enseñen.
   - Con los viejos fuera, cambian de núcleo 498 formas (34.051 usos), y 30
     formas dejan de ser «raíz de ninguna parte».
   - Con los viejos pelados, cambian 5 formas (6 usos) y ningún veredicto.
   - Para `ta-`: si sale, 5 formas (433 usos) pasan a «ninguna parte»; si se
     sigue pelando, cero.
3. **El detector de aspecto se sustituye, no se une.** Con la unión, el scorer
   seguiría premiando `-ni`.
   - Leída con el mapa nuevo, la base vieja tiene aspecto en 1 respuesta de
     3.811 (hoy lo tiene en 3.802).
   - Los runs viejos no se re-leen.
4. **Se archivan** `taya`, `pia` y `nüma` en `FUERA_DEL_HABLA`, con la capa
   intacta. Quedan en la puerta y no se pueden reacuñar.
5. **Se renombran** las claves lokono `tuhu` y `kuba`.
6. **Hay que tocar:**
   - las cinco plantillas;
   - las reglas de aspecto y posesivo;
   - la tupla de `es_arahuaco` y el mapa de `_aspectos_morfologicos`;
   - la koiné (`_NUCLEO_FALLBACK`, `FORMAS_SEED`, `_ASPECTO_SUFIJO`);
   - la marca de `curiana_escena`;
   - los tests: `taya` sale en 20 archivos, `-ka` en 20 y `-ni` en 17;
   - CLAUDE.md y morfologia.md.
7. **No se midió** el score entero con el motor nuevo: hace falta la tanda
   aplicada.

---

## Lo que no sabemos

- **No hay pronombre ni aspecto caquetío atestiguado**, salvo
  `kudanga`/`kuté`. Todo sale de las hermanas.
- **La *d-* de la 1sg** tiene apoyo, pero Oliver escribe «perhaps» (p. 136) y
  duda de que *datihao* sea caquetío (n. 42).
- **La base del pronombre libre** se elige; no se deriva (C9).
- **Los dos juegos de persona:** no sabemos si el caquetío tenía los de lokono
  y achagua. No se importan.
- **El taíno** de la 2sg, la 3sg y los plurales no tiene cronista.
- **La frase de Esquivel:** no sabemos de qué cronista es. Angleria 1892 no
  tiene capa de texto en el repo.
- **El achagua** es la lectura de un solo lector. «Ria» (Neira) contra «Pijà»
  (Gilij) sigue sin decidir.
- **Las columnas «A» de Goeje** no dicen de qué obra lokona salen.
- **Si los tiempos son de la lengua o del misionero:** la sospecha pesa igual
  sobre `-kuba`, `-bi`, `-ba` y `-pa`.

---

## Las preguntas para Miguel, con letra

1. **Yo:** A `dai` · B `daka` · C `daya` · D `daca` como voz taína.
   *(recomiendo A)*
2. **Tú:** A `bui` · B `bia` · C dejar `pia`. *(recomiendo A)*
3. **Él / ella:** A `lihi` / `tuhu` (reabre d21.13) · B sólo `tuhu` · C sólo
   `lihi`. *(recomiendo A)*
4. **Nosotros / ellos:** A se quedan `waya` / `naya` · B `wai` / `nai`.
   *(recomiendo A)*
5. **Ahora:** A sin marca · B `-kata` · C `-ka` como presente · D `-bo`.
   *(recomiendo A)*
6. **Ya:** A `-kuba` · B `-bi` · C `-mi`. *(recomiendo A)*
7. **Vendrá:** A `-ba` · B `-pa` · C `-su`. *(recomiendo A)*
8. **Aparte, sin recomendar ahora:** `ta-` → `da-`; `-kana`; y la campaña de
   `kashi`, `yama`, `sulu` y `wana`.
9. **El criterio:** ¿vale leer (a) como «dos de las tres hermanas de cc.12»?
   Si no, `dai` baja a hipotético.

**Miguel decide.**
