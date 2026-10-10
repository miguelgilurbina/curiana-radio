---
tipo: esquema
ambito: las esferas de los pueblos hermanos — un corpus por pueblo, con el mismo molde que el caquetío
propuesto: 2026-10-09
estado: propuesta (la estructura la decide Miguel; los datos entran por 6-fusion/)
guardian: curiana_sim/compilar_hermanas.py
descripcion: "Taíno, lokono, kalinago, achagua (y el wayuu de la Vía A) dejan de ser notas al pie del corpus caquetío y pasan a tener sus propias cinco esferas, en un solo esquema, para poder compararlas tema a tema."
---

# `3-mundo/hermanas/` — las esferas de las hermanas

> **Por qué existe.** Miguel, 2026-10-09: «la idea es tal cual como armamos
> estas esferas de creencia, sociedad, etc. para los caquetíos, deberíamos
> hacerlo para cada una de sus hermanas». Hasta hoy lo que sabíamos de las
> hermanas vivía disperso: en `referencia:` de los hechos caquetíos («Perrin
> 1995, analogía wayuu»), en `etnias.yaml` (sólo el CONTACTO), y en cuatro
> propuestas de creencia de la minería 1 (`6-fusion/creencia_<pueblo>_2026-10-09.yaml`)
> **cada una con su esquema** (21 claves en la kalinago, otras en la taína, otras
> en la lokono). Así no se puede abstraer nada. Este directorio da un molde
> único, y un script que lo valida y lo cruza.

## 1. Qué es y qué no es

- **Es** un corpus cultural por pueblo hermano, con las **mismas cinco esferas**
  que el caquetío (`3-mundo/corpus/`): parentesco, creencia, ecología,
  transmisión, geografía política. Un hecho = lo que las fuentes de ESE pueblo
  dicen de ESE pueblo, con su página y su época.
- **Es** la capa de comparación: cada hecho lleva un `tema` de vocabulario
  cerrado, y `compilar_hermanas.py --matriz` cruza tema × pueblo (caquetío
  incluido). Esa matriz es la abstracción que Miguel pide: ver de un vistazo
  qué sabemos del segundo entierro en cinco pueblos, y con qué fuente.
- **No es** el lugar de la lengua: léxico, cognados y topónimos siguen yendo a
  sus propuestas (`lexicon_*.py`, `2-lengua/`). Si un hecho trae una palabra,
  la escribe en `grafia:` y la propone aparte.
- **No es** el corpus caquetío. Lo que una hermana autoriza a decir DEL
  CAQUETÍO se declara en `proyeccion:` y se fusiona, si Miguel lo decide, en
  `3-mundo/corpus/`. Las dos capas no se mezclan: un hecho taíno sigue siendo
  taíno aunque ilumine un hecho caquetío.

## 2. Dónde vive cada cosa

```
3-mundo/hermanas/<pueblo>/<esfera>.yaml     canon (tras fusión; hoy vacío)
6-fusion/hermanas_<pueblo>_<fecha>.yaml     propuesta: el MISMO esquema + meta
3-mundo/hermanas/COMPARADA.md               generado por --matriz (no se edita)
```

Pueblos (`pueblo:`): `taino`, `lokono`, `kalinago`, `achagua`, `maipure`,
`wayuu`, `paraujano`. Una propuesta lleva en `meta.pueblo` el principal y puede
traer hechos de otro (la minería achagua trae maipure de Gilij): cada hecho
dice el suyo.

**Qué es cada pueblo para el caquetío** (Miguel, 2026-10-09). El validador lo
lleva en `RELACION` y `LINEA`, y la matriz lo escribe junto a cada pueblo.

| Relación | Línea | Pueblos | Por qué |
|---|---|---|---|
| hermana | lokonoide | taíno, lokono, kalinago (su sustrato iñeri) | comparten con el caquetío la 1.ª persona /dA-/ (Oliver 1989 cap. 2 p. 150) |
| prima | guajiro-paraujana | wayuu, paraujano (añú) | rama que innovó /tA-/: «prima lejana», de otra esfera cultural |
| prima | orinoco-llanos | achagua, maipure | «una línea maipuriana aparte de los caquetíos»: conserva Nu- |
| vecina | otras familias | jirajara, ayomán, gayón, caribes, guahibo… | entran cuando se mine el primero; cada una con sus cinco esferas |

La regla para reconstruir hacia el caquetío con una prima (¿cuenta como
segunda tradición o sólo como comparanda?) **sigue sin decidir**. Una vecina
nunca reconstruye: se describe por sí misma.

Esferas (`esfera:`): `parentesco` · `creencia` · `ecologia` · `transmision` ·
`geografia_politica`. En la propuesta conviven en un archivo; al fusionar se
reparten por esfera.

## 3. El esquema de un hecho

```yaml
meta:
  pueblo: kalinago
  recogido: '2026-10-09'
  estado: sin-fusionar            # sin-fusionar | fusionada | canon
  quien: 'minero kalinago, minería 2 (Claude Opus 5.5), rama vault/hermanas-kalinago'
  plan: 4-fuentes/sesiones/08_creencia_kalinago_que-minar.md
  fuentes_leidas: [breton-1665, rochefort-1658, du-tertre-1667]
  cobertura: {rochefort-1658: 'pp. 410-460 en imagen', du-tertre-1667: 'pp. 356-420 en imagen'}
  no_leido: ['...']

hechos:
  - id: kalinago-creencia-001       # <pueblo>-<esfera>-NNN[a-z]? — único en todo el corpus
    esfera: creencia
    tema: especialista              # vocabulario cerrado (§4)
    contenido: >-
      1-4 frases. Lo que la fuente dice, con la cita corta entre comillas
      latinas y la grafía de la fuente.
    cita: >-                        # opcional: la cita larga literal
    grafia: 'boyé, boyez'           # las formas tal como las escribe la fuente
    pueblo: kalinago
    donde: 'Guadalupe y Dominica'   # polity, isla o región del testimonio
    epoca: '1635-1654'              # cuándo es el testimonio (regla 3)
    etiqueta: atestiguado           # atestiguado | hipotetico
    testigo: vio                    # vio | oyo | lexico | tercera-mano
    procedencia: {obra: breton-1665, pagina: '1665 p. 283 (imagen)'}
    procedencia_extra:              # segundas atestaciones INDEPENDIENTES
      - {obra: du-tertre-1667, pagina: 'p. 365 (imagen)', independiente: false, nota: 'misma misión que Breton'}
    como_se_escribio: >-            # el sesgo de quien escribe
      Misionero que catequiza con estas palabras.
    capa_colonial: >-               # qué parte del hecho es del cronista (opcional)
    sustrato: arahuaco              # arahuaco | caribe | colonial | sin-decidir (kalinago; opcional en otros)
    hermanas:                       # el mismo tema en otra hermana
      - {pueblo: taino, id: taino-creencia-004}
      - {pueblo: lokono, obra: roth-1915, pagina: 'p. 337', que: 'el semechichi recibe su espíritu al iniciarse'}
    caquetio: [creencia-004, creencia-025]   # ids del corpus caquetío que toca
    proyeccion:
      capa: lectura                 # reconstruido | hipotetico | lectura | comparanda-esfera | no-proyecta
      nota: >-
        Por qué esa capa (regla C, §5).
    via_a: {creencia-002: corrobora-en-parte}   # auditoría de los hechos wayuu del corpus
    tierra: [dueno-del-lugar, limite-de-uso]   # si responde la pregunta de §4b (opcional)
    dominios: [creencia, medicina]  # libre
    id_origen: ck09-02              # si migra de una propuesta anterior
    implicacion_simulacion: >-      # opcional, como en el corpus caquetío
```

Obligatorios: `id`, `esfera`, `tema`, `contenido`, `pueblo`, `epoca`,
`etiqueta`, `testigo`, `procedencia` (con `obra` clave foránea de
`4-fuentes/bibliografia.yaml`; `pagina` obligatoria si `atestiguado`),
`proyeccion.capa`. Lo demás, cuando haya.

### Las dos etiquetas de la hermana

Dentro de la hermana sólo hay dos: **`atestiguado`** (una fuente primaria o
contemporánea, con página, dice esto de este pueblo) e **`hipotetico`** (lo
dice un compilador de tercera mano sin primaria en el repo —Rouse, Steward,
Brinton copiando a Brett—, o es la hipótesis de un autor moderno). `testigo:
tercera-mano` obliga a `hipotetico`: un reconstruido nunca se apoya sólo en
Rouse (minería 1, las cuatro notas). `reconstruido` no existe dentro de una
hermana: reconstruir es lo que se hace HACIA el caquetío, y vive en
`proyeccion`.

## 4. Los temas (vocabulario cerrado)

El `tema` es lo que permite cruzar pueblos. Es cerrado a propósito: si un
hecho no cabe, se propone el tema nuevo en la bandeja (`meta.temas_propuestos`)
y el validador lo avisa, no lo acepta. `dominios` queda libre para lo demás.

| Esfera | Temas |
|---|---|
| `parentesco` | `descendencia` (matri/patri) · `residencia` · `matrimonio` (alianza, poliginia, exogamia) · `sucesion-herencia` · `linaje-clan` · `roles-de-genero` · `infancia-nombre` · `sociedades-masculinas` · `hogar-casa` |
| `geografia_politica` | `jefatura` (qué es el jefe, cómo se accede) · `jerarquia-rango` (títulos, estamentos) · `sucesion-politica` · `territorio-asentamiento` · `escala-poblacion` · `guerra` · `alianza-intercambio` · `tributo-trabajo` · `cautivos-esclavitud` · `justicia-norma` |
| `creencia` | `espiritu-tutelar` · `alma` · `muerte-entierro` · `segundo-entierro` · `especialista` (piache, behique, boyé, semechichi) · `iniciacion-especialista` · `enfermedad-cura` · `cosmos-origen` · `tiempo-calendario` · `ofrenda-fiesta` · `tabu` · `sueno-vision` · `lugar-sagrado` |
| `ecologia` | `medio-fisico` · `cultivo` · `pesca` · `caza-recoleccion` · `vivienda` · `tecnologia-objetos` · `comida-bebida` · `comercio-rutas` · `navegacion` |
| `transmision` | `curriculo-edad` · `especialista-formacion` · `saber-restringido` · `narracion-mito` · `lengua-registro` (habla de mujeres, registro formal) · `canto-baile` · `escritura-marca` (petroglifos, pintura corporal) · `nombre-propio` |

«Estructura social y jerarquía» (Miguel) se reparte entre `parentesco`
(descendencia, residencia, linaje) y `geografia_politica` (jefatura, rango,
sucesión, guerra, cautivos): es el mismo reparto que hizo el corpus caquetío
en las sesiones 1 y 5.

## 4b. La pregunta a cada pueblo: ¿cuál era su relación con la tierra?

> Miguel, 2026-10-09: «la Kaketiana dejó de ser solamente sobre los caquetíos,
> sino sobre la filosofía que ellos tenían con su relación con la tierra […]
> qué es lo que podemos realmente aprender de ellos»; y «puede ser una pregunta
> a cada pueblo. Nuestro centro es el de los caquetíos, pero es importante
> darle voz a cada pueblo».

Es la pregunta que se le hace a **todos** los pueblos, y atraviesa las cinco
esferas: la responde un hecho de creencia (el dueño del cerro), de geografía
política (quién es dueño de la tierra), de ecología (qué no se caza) o de
transmisión (cómo se aprende el monte). Por eso no es un `tema` más: es un
campo aparte, `tierra`, con uno o varios aspectos de este vocabulario cerrado.

| Aspecto | Qué pregunta | Un ejemplo ya minado |
|---|---|---|
| `dueno-del-lugar` | ¿Tienen dueño el monte, el cerro, el agua, los animales? | el Capo que no deja cortar los árboles del Capubana (creencia-021) |
| `tenencia` | ¿De quién es la tierra: común, del jefe, de la casa? ¿Se hereda? | entre maipures, «non hanno delle terre private» (Gilij t. II p. 212) |
| `limite-de-uso` | ¿Qué no se corta, no se caza, no se toma, y cuándo? | al venado echado no se le tira |
| `reciprocidad-ofrenda` | ¿Qué se devuelve a la tierra o a sus espíritus? | la ofrenda de casabe al espíritu que da la yuca (kalinago) |
| `lugar-sagrado` | ¿Qué lugares tienen valor ritual? | el Coaibai taíno, el cerro de los caquetíos |
| `calendario-del-medio` | ¿Se cuenta el tiempo por lo que hace el medio? | «cuando pusiesen huevos las tortugas», el calendario achagua |
| `saber-del-medio` | ¿Qué saber del medio se guarda y se enseña? | el cerro como aguja de marear |
| `muertos-y-tierra` | ¿Vuelven los muertos a la tierra o al agua? | los huesos y la lluvia (creencia-012) |
| `origen-en-la-tierra` | ¿Sale la gente de la tierra, de un árbol, de un río? | achaguas «hijos de los troncos» y «de los ríos» |

Reglas:

- **Darle voz a cada pueblo** quiere decir que la respuesta de un pueblo se
  escribe con su fuente y en sus términos, no como variante de la caquetía.
  Las etiquetas y la regla 3 valen igual: una tradición viva del s. XX
  responde la pregunta, pero con su capa (`hipotetico` o retroabstraída).
- **El lado caquetío** no se escribe en el corpus (es canon): se propone en
  `6-fusion/relacion_con_la_tierra_<fecha>.yaml`, sección `caquetio`, una
  entrada por hecho: `{id, tierra: [...], nota}`. El validador comprueba que el
  id exista en el corpus y que los aspectos sean legales.
- Un aspecto que falte se propone en la bandeja; no se fuerza.

## 5. Las reglas que no se rompen aquí

1. **Regla 3 por fecha, en cada hecho.** `epoca` dice de cuándo es el
   testimonio. Breton es 1635-1654 (140 años después del contacto); Roth es
   1915; Pané es 1494-1498. Nada de eso es el s. XIV-XV de nadie: proyectarlo
   es decisión, y se declara en `proyeccion.nota`.
2. **Hermana no es vecino.** `etnias.yaml` dice con quién convivieron los
   caquetíos; esto dice qué creían y cómo vivían los pueblos de la misma
   familia. Un hecho de aquí NUNCA se escribe como «lo que se hacía en la
   costa».
3. **La regla C de Miguel (2026-10-09) para `proyeccion.capa`.** Lo NUEVO para
   el caquetío entra `reconstruido` sólo con **dos tradiciones arahuacas
   independientes** (`hermanas` con dos pueblos distintos y fuentes que no se
   copian); con una sola, `hipotetico`; si sólo ilumina un hecho caquetío ya
   atestiguado, `lectura`; la capa caribe o lo que sirve a un personaje de la
   esfera, `comparanda-esfera`; la capa colonial o el nombre que no se
   caquetiza, `no-proyecta`. El validador exige, para `reconstruido`, al menos una
   entrada de OTRO pueblo en `hermanas` (el hecho es la primera tradición; la
   hermana, la segunda). Lo wayuu de la Vía A se queda como comparanda y se audita en
   `via_a`.
4. **Independencia.** Du Tertre, Breton y Rochefort no son tres testigos
   (misión compartida y copia); Jahn que cita a Oviedo no es un segundo
   testigo de Oviedo. `procedencia_extra[].independiente` lo dice en cada
   caso, y sólo lo independiente cuenta para la regla C.
5. **En duda, degradar.** Igual que en el lexicón y en el corpus.

## 6. Cómo se usa

```bash
python curiana_sim/compilar_hermanas.py            # valida canon + propuestas, informe
python curiana_sim/compilar_hermanas.py --check    # exit 1 si hay errores
python curiana_sim/compilar_hermanas.py --matriz   # tema × pueblo, con el caquetío al lado
python curiana_sim/compilar_hermanas.py --matriz --escribir   # reescribe COMPARADA.md
```

La matriz abre con la pregunta de §4b: aspecto × pueblo, con el caquetío
primero.

Minar una hermana es `minar-fuente` con este esquema de salida: la pregunta
sale de la nota `08_creencia_<pueblo>_que-minar` y de las fichas de sus
fuentes («Qué preguntarle»); la bitácora va a la ficha de cada obra; la
propuesta va a `6-fusion/hermanas_<pueblo>_<fecha>.yaml`; nada toca
`3-mundo/`. La fusión (`fusionar-propuesta`) reparte los hechos por esfera en
`3-mundo/hermanas/<pueblo>/` y, los que lleven `proyeccion.capa` reconstruido
o hipotetico, los lleva además al corpus caquetío con su etiqueta.

## 7. Lo que migra

Las cuatro propuestas de la minería 1 (`6-fusion/creencia_<pueblo>_2026-10-09.yaml`)
se reescriben a este esquema por el minero de cada pueblo en la minería 2,
hecho a hecho y conservando `id_origen`, sin releer las fuentes salvo duda.
Las propuestas viejas no se borran hasta que Miguel fusione: son la
procedencia de la migración.

## Enlaces

[[esfera-de-interaccion]] · [[mapa-creencia]] · [[mapa-familia]] · [[mapa-geografia-politica]] · [[12_relacion_con_la_tierra]] (§4b, la primera vuelta) · `3-mundo/corpus/README.md` · `3-mundo/etnias.yaml` · `6-fusion/BANDEJA.md`
