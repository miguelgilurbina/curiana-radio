## D5 son tres decisiones, no una — y solo la tercera toca el experimento

Sesión de trabajo del 2026-08-25. Todo lo de abajo está medido contra
`curiana_lexicon.py` y el glosario de [[zavala-reyes-2015]].

### D5a · La política de lema

Medido sobre las 304 entradas de familia caquetía:

| Capa | c- / qu- | k- |
|---|---|---|
| `caquetío-atestiguado` | **48** | 4 |
| `caquetío-reconstruido` | 2 | **11** |

Las dos capas codifican **quién transcribió**, no cómo suena la lengua.

**Rumbo acordado: lema fonémico**, con `forma_fuente` como campo obligatorio.
El razonamiento de Miguel: el caquetío es una lengua 100 % de tradición oral, así
que la grafía colonial no es el dato — es ruido de transmisión de un escribano
castellano sin formación lingüística. Conservarla no es "no decidir": es heredar
**su** análisis fonológico en vez del nuestro, que está hecho con cognados y con
reglas escritas y testeadas.

Contrapartida que se acepta a cambio: hoy la forma literal de la fuente está
enterrada en la prosa del campo `notas`. Pasar a lema fonémico **obliga** a
promoverla a campo propio, lo que mejora la trazabilidad (regla 8), no la degrada.

**Topónimos: dentro de la política, no exceptuados.** Son la mayor masa de
fonología caquetía superviviente, precisamente porque sobrevivieron en boca
castellana. Su grafía oficial es `forma_fuente`; el lema es la forma fonémica.

### Cuánto de la migración es controvertido — medido

Separando las 10 reglas de `REGLAS_ORTOGRAFICAS` por cuánto **afirman**, sobre
las 226 formas atestiguadas:

| | formas |
|---|---|
| Ninguna regla las toca (ya son fonémicas) | 91 |
| Solo tocan reglas seguras | ~89 |
| Bloqueadas por una regla que es una tesis | ~46 |

### 🔴 Corrección: `h` → ∅ NO es una regla segura

En la primera pasada clasifiqué `<h>` castellana muda como regla segura, y toca
**31 formas**. La evidencia la contradice:

```
Hurehurebo  ~  Jurijurebo    (Arcaya, el mismo poblado de Paraguaná)  -> h ~ j
Hacarigua   ~  Acarigua      (Federmann, llanos)                      -> h ~ ∅
```

La misma grafía hace dos trabajos: en un caso alterna con `j` (= /h/ o /x/, un
sonido real), en otro es muda. Borrarla a ciegas **destruye un fonema en la mitad
de los casos**. `h` baja a regla disputada; hay que decidirla por posición o por
serie, no en bloque.

### D5b · Los tres pares c/k — resueltos al medirlos

- **`buco`/`buko` → fusionar.** La nota de `buko` ya dice *"misma palabra que
  buco, aquí con grafía k"*. Ambas citan Zavala #46. Y `buco` es una de las
  entradas **sin capa epistémica declarada** (`fuente: caquetío`), así que
  fusionar arregla dos cosas.

  🎯 **Y ahora hay fuente mucho mejor**: [[ballesteros-1550]], Obispo de Coro,
  transmitido verbatim por [[arcaya-1920]] p. 170 — *"Los indios antiguamente,
  una legua del río arriba tenían hecha una presa **que ellos llaman buco**"*.
  Atestación de **1550**, en el río de Coro, dentro de la polity costera. Mata
  la reserva que la nota registraba (*"Alvarado… sugiere origen romance, duda
  del origen indígena"*): en 1550 un obispo dice que así lo llaman los indios.

- **`barici`/`bariki` → NO fusionar.** Son entradas distintas de la fuente:
  Zavala **#34** «Agua turbia» y **#35** «Barique» «Arcilla roja. Almagre».
  Colisionan solo al normalizar. Merecen referencia cruzada, no fusión.

- **`coro`/`koro` → no tocar.** Falso positivo confirmado: cardón
  (hipotético/topónimo, ya degradado por D10) vs. cotorra (Zavala #181).

**F2 se cierra con 1 fusión, 1 referencia cruzada y 1 no-problema.** La cifra de
"9 pares c/k" de [[PLAN_MAESTRO]] §1 está vieja.

### D5c · `gu` → /w/

El argumento que la sostiene **no es sobre el caquetío, es sobre el escribano**:
el castellano no tenía grafema para [w], y la misma sustitución aparece en toda
lengua indígena transcrita por españoles (náhuatl *wei* → `Huey`, taíno
*waitiao* → `guaitiao`, *wanin* → `guanín`). Eso es independiente de la Tabla A-7
de Oliver, que respondería otra pregunta (los reflejos de *w del protoarahuaco).

Reparto de las 42 formas afectadas: **24 en inicial**, **18 en medial**.

⚠️ **La distinción inicial/medial probablemente no se sostiene**, y conviene
decirlo: si `Paraguaná` es `para` + `gua` + `ná` (ver el issue de segmentación),
entonces `gua` 'terreno cercado' **es un morfema que aparece en medial dentro de
compuestos**. Un mismo morfema no puede valer /wa/ en inicial y /gwa/ en medial.
Si esa segmentación se acepta, la regla debe aplicarse **uniforme**.

### Lo que queda abierto tras esto

1. `<ce>/<ci>` → /s/ — 5 formas; asume que el escribano seseaba.
2. **`h`** — 31 formas, recién degradada a disputada (arriba).
3. El orden núcleo/modificador en los compuestos, que decide D5c por la vía de
   la segmentación.

### Efecto colateral que se resuelve solo

Si entra `gu`→/w/: `güere` → `were`, `güique` → `wike`, y **desaparece el choque
de la diéresis** — la `ü` queda libre para significar solo /ɨ/ en las 6 formas
tomadas del wayunaiki (`anüiki`, `apünüin`, `nüma`, `pütchi`, `tüshi`, `wanü`).

### ⏱️ Por qué decidirlo ahora

`score_linguistico()` empareja tokens contra las claves de `VOCABULARIO_BASE`,
así que renombrar lemas cambia el scoring. Con las simulaciones en pausa y sin
ningún run post-auditoría, **este es el momento más barato que va a haber**.
Después del primer run limpio, invalidaría comparaciones.

### 🔴 Alcance real: el pipeline, no 226 palabras

La [[BANDEJA]] tiene ~1.296 ítems en grafía colonial (`lexicon_alvarado` 217,
`van_buurt` 231, `gatschet` 88, `toponimos` 74, `candidatos` 441). Si la política
de lema es fonémica, **la fusión necesita el paso de normalización incorporado**,
o la cola seguirá reinyectando grafía colonial para siempre.
