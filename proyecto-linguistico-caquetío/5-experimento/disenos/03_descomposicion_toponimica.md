---
tipo: diseño
tarea: F11
ambito: descomposición del corpus toponímico y antroponímico
fuentes: [zavala-reyes-2015, gatschet-1885, van-buurt-2014, alvarado-1921]
salidas: [curiana_sim/minar_toponimos.py, curiana_sim/lexicon_toponimos.py]
toca_lexicon: false
fecha: 2026-08-03
---

# Descomposición toponímica — los topónimos como ecuaciones bilingües

*Método y resultados de F11. **No modifica `curiana_lexicon.py`**: emite una
propuesta (`curiana_sim/lexicon_toponimos.py`) para revisión humana, en la
misma disciplina que las cuatro minerías del 2026-08-03 (ver
[[INDICE_FUENTES]]).*

---

## 1. La idea

El proyecto venía archivando los topónimos como **canon inerte**.
`minar_zavala_glosario.py` los excluye del habla activa —45 topónimos y 14
antropónimos, *"fuera del habla por diseño"*— y las otras tres minerías hacen
lo mismo. La exclusión es correcta para el *habla*: un agente no debería decir
«Bariquisimeto». Pero tuvo un efecto colateral que nadie vio:

> **Los topónimos vienen con su traducción. Son ecuaciones bilingües de las que
> se puede despejar el morfema.**

El caso que lo destapó:

| Pieza | Estado antes de F11 |
|---|---|
| `juri` = "viento, ventarrón" | ✅ en el lexicón, `caquetío-atestiguado` |
| `ebo` = "camino, paso, senda" | ✅ en el lexicón, `caquetío-atestiguado` |
| **`jurijurebo`** = **"Paso de los vientos"** | ⛔ en `TOPONIMOS_ZAVALA`, fuera del habla, marcado *"glosa incierta"* |

El topónimo descompone limpio en dos morfemas **ya atestiguados**, y la glosa
lo confirma. Más aún: `juri~juri` es **reduplicación**, y [[gatschet-1885]]
documenta ese proceso explícitamente para el arubano — un proceso que **no
estaba en `REGLAS_ZAVALA`**. Un solo topónimo confirma dos palabras y sugiere
una regla morfológica que el proyecto no tenía.

El proyecto ya sabía que esto era posible y no lo había explotado:
[[02_protocolo_habla_paraguanera]] §4, criterio positivo nº 5, dice
literalmente que *los topónimos son el reservorio más fiable de sustrato*.

---

## 2. El método

Criptoanálisis con texto plano conocido: se tiene **la forma** y se tiene **el
significado**; se despejan las partes.

1. **Segmentar** cada topónimo contra el inventario de morfemas ya conocido
   (`AFIJOS_ZAVALA`, `MORFEMAS_VAN_BUURT`, y las 314 formas de familia caquetía
   de `VOCABULARIO_BASE`).
2. **Alinear** los segmentos con las partes de la glosa española.
3. **Despejar** el morfema desconocido cuando todos los demás encajan.
4. **Validar por recurrencia**: un morfema en un solo topónimo es conjetura; en
   tres o cuatro con glosa consistente es un hallazgo. **La frecuencia es el
   principal control de calidad.**

### 2.1 Regla cero, y cómo está implementada

> **Una segmentación que "suena bien" no es evidencia.**

El proyecto ya pagó ese precio: 441 formas transducidas sin verificar
cognación, ~80 % de fallo medido, hoy aisladas en `lexicon_candidatos.py`.
Segmentar topónimos tiene **la misma tentación**: cortar donde convenga hasta
que cuadre. Tres defensas, y la primera no es retórica sino una decisión de
arquitectura del minador:

- **La glosa manda sobre la forma.** `minar_toponimos.py` enumera *todas* las
  segmentaciones posibles y **deja que la glosa elija**. Una primera versión
  elegía la óptima *por la forma* (máxima cobertura, mínimos segmentos) y luego
  miraba la glosa: sacaba `Casibari` = `kasi`+`bari` —dos palabras del lexicón,
  cobertura perfecta, cero residuos— en vez del `ka-siba-rí` 'hay rocas duras'
  que [[van-buurt-2014]] documenta. **Ambas cubren los ocho caracteres; solo la
  segunda reconstruye la traducción.** Si la forma decide primero, el método se
  convierte en la trampa que dice evitar.
- **Recurrencia mínima ≥2** topónimos independientes, y hay que decir cuáles.
  Los residuos de menos de 3 caracteres no cuentan: cualquier bigrama recurre
  en medio corpus.
- **Los topónimos coloniales, las glosas circulares y las meramente
  referenciales se apartan**, con la razón escrita.

### 2.2 Tres decisiones técnicas que valen la pena

**Normalización ortográfica.** El corpus está en tres tradiciones: Zavala
escribe a la española, [[gatschet-1885]] a la anglo-alemana, [[van-buurt-2014]]
a la papiamentu/neerlandesa. Sin normalizar, `quibacoa` ≠ `kibakoa`,
`Guadirikiri` ≠ `Wadirikiri` y `barici` ≠ `barisi`, y la recurrencia —que es el
control de calidad de todo el método— sale artificialmente baja. Ojo con el
detalle que costó una pasada entera: en español **`c` ante `e`/`i` es /s/, no
/k/**; tratarla como /k/ desconectaba `barici` de `barisi`.

**Campos semánticos explícitos.** `adabacoa` = "Todo arboleda" no alinea con
`bacoa` = 'bosque' por comparación de cadenas: ningún stemmer sabe que
*arboleda* y *bosque* son lo mismo. Hay una tabla de 16 campos
(`CAMPOS_SEMANTICOS`) con las equivalencias **escritas una por una y
auditables**, no un embedding opaco. Criterio de admisión: solo sinonimia de
diccionario en el campo del paisaje; ninguna equivalencia "de conveniencia"
para hacer cuadrar un topónimo concreto.

**Genéricos fuera.** *sitio*, *lugar*, *punto*, *paraje* están en la lista de
palabras vacías. Aparecen en casi toda glosa de topónimo **y** en casi toda
glosa de morfema, así que alinean con cualquier cosa. No son evidencia.

---

## 3. El material, y la asimetría que lo condiciona

| Fuente | Formas | ¿Glosa? |
|---|---|---|
| [[zavala-reyes-2015]] `TOPONIMOS_ZAVALA` | 45 | ✅ **glosa descriptiva española** |
| [[zavala-reyes-2015]] `ANTROPONIMOS_ZAVALA` | 14 | ✅ (casi siempre referencial) |
| [[van-buurt-2014]] §8-10 `ETIMOLOGIAS_TOPONIMOS` | 15 | ✅ comentario del autor, en inglés |
| [[gatschet-1885]] `GATSCHET_TOPONIMOS` | 31 | ❌ |
| [[van-buurt-2014]] §7 `TOPONIMOS_VAN_BUURT` | 176 (213 variantes) | ❌ |

**Los 244 topónimos insulares sin glosa no rinden ecuación.** No hay
significado que despejar. Solo sirven como **control de recurrencia** de los
morfemas despejados en los 74 que sí la tienen. Conviene decirlo de entrada
porque cambia la expectativa: el material real de trabajo son **45 topónimos
continentales**, no 300.

> Nota de procedimiento: la §7 de [[van-buurt-2014]] (≈180 topónimos) y los
> comentarios de §8-10 **ya estaban extraídos** por `minar_van_buurt.py` en
> `TOPONIMOS_VAN_BUURT` y `ETIMOLOGIAS_TOPONIMOS`. F11 los consume, no los
> vuelve a extraer.

---

## 4. Resultados

```
74 topónimos/antropónimos glosados procesados
   A  6   ·   B  8   ·   C 13   ·   D 47
244 formas insulares usadas como control de recurrencia
```

### 4.1 Nivel A — segmentación confirmada

| Topónimo | Glosa de la fuente | Segmentación |
|---|---|---|
| **jurijurebo** | Paso de los vientos | `juri~juri` + `ebo` |
| **yacarebacoa** | Pueblo del bosque | `yacare` + `bacoa` |
| **quibacoas** | Bosques pedregosos | `quiba` + `(b)acoa` |
| **cumarebo** | Camino del cacique Cumare | `Cumare` + `ebo` |
| **guacaubana** | Río escondido | `guaca`/`waka` + `-ubana` |
| **barisi** | Región de tierras coloradas | = `barici` (identidad, corrobora) |

`quibacoas` resuelve de paso un problema del lexicón: hay una entrada `quiba` =
'ayuda' y otra `quiva`/`cuiva` = 'piedra'; la glosa *"Bosques **pedregosos**"*
y [[van-buurt-2014]] §8 (*siba* o *quiba* = 'roca') confirman 'piedra'.

`guacaubana` es **A con reserva**: 'escondido' ← `waka` 'bajo tierra' alinea
limpio y el compuesto recurre en Aruba (**Wakubana / Wacobana**, mapa de 1825,
y [[gatschet-1885]] lo registra igual) — pero `-ubana` sigue sin glosa, así que
la parte 'río' de la traducción no queda explicada.

### 4.2 Los morfemas despejados

| Morfema | Glosa inferida | Apoyos | Estatus |
|---|---|---|---|
| **`-bacoa`** | bosque, arboleda; formante de 'paraje cubierto de' | adabacoa · guadabacoa · quibacoas · yacarebacoa · (sazaribacoa) | corroborado; nuevo es el **uso sufijal** |
| **`-are`** | sitio de, paraje de | bobare · cabudare · dabudare · pachacuare · taratarare | **NUEVO** |
| **`ada-`** | árbol | adabacoa · guadabacoa | **NUEVO** |
| **`yacare`** | pueblo | yacare · yacarebacoa | **NUEVO** |
| **`bari-`** | rojizo, turbio | barisi · bariquisimeto | reagrupación |
| **`wa-`** | prefijo de pluralidad | adabacoa ↔ guadabacoa · guamabatriba | corroborado |

**`-bacoa` es el mejor resultado del ejercicio**: 5 topónimos glosados, 4 de
ellos con 'bosque/arboleda' en la traducción, más el apoyo independiente de
[[alvarado-1921]] (`-baca` 'grupo, matorral, espesura', vía van Buurt §10,
topónimos *Yatu Bacu* y *Dauguaraubaca*) y dos ecos insulares (*Barbacoa* en
Aruba, *Maniguacoa* en Curaçao). El contraejemplo se registra: `sazaribacoa` =
"Río de los maizales" no menciona bosque, y encaja mejor con la otra acepción
de la misma entrada, 'sitio fértil'.

**`-are`** es el hallazgo más limpio de los nuevos: cuatro topónimos glosados
literalmente *"Sitio de X"*. El caso decisivo es `dabudare` = "Sitio de
extracción de barro", porque su base `dabuda` 'barro loza' **ya está en el
lexicón como `caquetío-atestiguado`**: la ecuación despeja el sufijo contra un
morfema conocido, no contra un hueco. De 7 apariciones finales con glosa
descriptiva, 5 denotan un lugar; los dos fallos (`guasare` 'Árbol cactáceo',
`chunare` 'Mazorca tierna') quedan anotados.

**`ada-` viene con una advertencia honesta**: el despeje no es forzoso. Si
`-bacoa` ya vale 'arboleda' por sí solo, `ada-` podría ser cualquier cosa. Lo
que lo sostiene no es la ecuación sino el **cognado lokono `ada` 'árbol'** —
que es sólido, pero es evidencia de otra clase.

### 4.3 Los descartes (47), por qué

| Motivo | Nº | Ejemplo |
|---|---|---|
| glosa meramente referencial | 22 | *baracoica* = "Cacique de Curazao" |
| van Buurt §8-10 sin contenido segmentable | 13 | *Curaçao* (discusión histórica, no etimología) |
| opacos: ningún morfema conocido alinea | 8 | *acatute* = "Pueblo entre valles" |
| glosa circular | 2 | *cemirucos* = "Semerucos" |
| glosa mutilada en la fuente | 1 | *coroque* = "Árbol de ¿?" |
| castellanización moderna | 1 | *zamurano* ← esp. *zamuro* |

La categoría dominante —**glosa meramente referencial**— no es un fallo del
método sino un hecho sobre la fuente: cuando Zavala anota un topónimo, unas
veces lo traduce y otras solo dice dónde queda o de quién era.

### 4.4 Prueba de humo, no hallazgo

Cinco de las etimologías de [[van-buurt-2014]] §8-10 (*Casibari*,
*Hudishibana*, *Balashi*, *Onima*, *Cariatávo*) las reproduce el segmentador
tal cual. **Eso valida el procedimiento, no aporta información**: los morfemas
del inventario salieron precisamente de esas etimologías. Se registran como
nivel C con la etiqueta explícita, para que nadie los cuente como hallazgo.

Vale la pena un detalle: `hudi` 'viento' de *Hudishibana* (Aruba) y `juri`
'viento' de *jurijurebo* (Golfete) son la misma raíz en dos ortografías. **La
palabra para 'viento' aparece en un topónimo continental y en uno insular.**

---

## 5. Las tres preguntas, respondidas

### 5.1 ¿Cuántas palabras del lexicón quedan corroboradas?

**Diez**, con independencia alta o media:

`bacoa` · `ebo` · `juri` · `quiva/quiba` · `barici` · `bariki` · `dabuda` ·
`dare` · `para/paragua` · `gua`

Corroboración = la palabra aparece dentro de un topónimo cuya glosa es
consistente con la suya, y son **dos listados distintos** de la fuente
(glosario vs. toponimia). Es evidencia barata e independiente para el eje
FIDELIDAD: no hubo que minar ninguna fuente nueva.

Otras **seis** (`siba`, `ka-`, `rí`, `bana`, `cari`, `bala`) aparecen
"confirmadas" por topónimos de [[van-buurt-2014]] §8-10, pero **la
independencia es nula**: el mismo autor derivó el morfema *de* ese topónimo.
Se listan aparte para no inflar la cuenta.

Además, `ebo` viene con dos contraejemplos (`guacurebo` "Quebrada que crece",
`turijerebo` "Lugar de descanso"): 2 aciertos y 2 glosas divergentes. La
corroboración es real pero no es perfecta, y así queda anotado.

### 5.2 ¿La reduplicación es un proceso productivo del caquetío?

**Sí**, y esta vez hay control cuantitativo. Aplicando el mismo detector
(unidad ≥3 caracteres) a poblaciones distintas del propio lexicón:

| Población | Tasa |
|---|---|
| toponimia del corpus (287 formas) | **9 %** |
| léxico caquetío (210 formas ≥5 car.) | **4,3 %** |
| léxico wayunaiki (703) | 3,1 % |
| léxico lokono (138) | 0,7 % |
| léxico taíno (40) | 0 % |

El método de detección es idéntico para todas, así que la diferencia no es un
artefacto. **Valores semánticos, en orden de apoyo:**

1. **Onomatopeya (fauna) — dominante.** 7 de las 9 reduplicaciones del léxico
   son animales y 5 de ellas aves: `warawara` 'caracara', `chuchubi`
   'sinsonte', `chuchube` 'paraulata', `querequere` 'ave pequeña', `humohumo`
   'el ave que vuela', `chogogo` 'flamenco', `tuqueque` 'gecko'. Es exactamente
   lo que afirma [[gatschet-1885]].
2. **Pluralidad / abundancia — sostenido por el mejor caso del corpus.**
   `jurijurebo` glosa *"Paso de los **vientos**"* con `juri` 'viento' en
   singular. Y **Shishiribana** frente a **Shiribana / Siribana**: el mismo
   topónimo, con y sin reduplicación de la sílaba inicial, en Bonaire y en
   Aruba.
3. **Especificación / intensidad — plausible, sin glosa que lo pruebe.**
   `barabara` 'árbol de madera **dura**' ← `bara` 'árbol' (van Buurt §5);
   `quibaquibi` 'baquiano, conocedor'; `patapati` 'anegadizo'.
4. **Diminutivo — sin apoyo.** Gatschet lo menciona; **ni un solo caso del
   corpus lo sostiene**. El diminutivo caquetío documentado es afijal: `-iro`
   (Zavala #166) y `-bi` (van Buurt §6). Es un punto donde el dato disponible
   contradice a la fuente, y hay que decirlo.

### 5.3 ¿Los antropónimos rinden igual que los topónimos?

**No, y por una razón estructural.** Un topónimo se glosa **describiendo** el
lugar ("Río escondido"); un antropónimo se glosa **identificando** a la persona
("Cacique de Curazao"). La ecuación bilingüe existe solo cuando la fuente
traduce, y con los nombres de persona Zavala casi nunca traduce: ubica.

```
antropónimos:  1 de 14 con glosa utilizable   ·  0 descompuestos
topónimos:    20 de 45 con glosa utilizable   ·  11 con algún resultado
```

El único con contenido léxico es `chunare` = *"Apellido. Mazorca tierna"*, y ni
así segmenta (nivel C). **Conclusión: no vale la pena buscar más antropónimos
con este método.** Sí vale la pena que las minerías futuras registren la glosa
*completa* cuando la haya — `chunare` demuestra que a veces la hay, y una
versión anterior del filtro lo descartaba entero por empezar con "Apellido".

---

## 6. Qué le propone esto a `REGLAS_ZAVALA`

Tres cosas, en orden de confianza. Ninguna se aplica aquí: son propuestas para
revisión humana (ver [[mapa-motor]] y [[DECISIONES_ABIERTAS]]).

**1. Reduplicación** — regla nueva.

```
X + X      → X~X       (total)
X + X(-V)  → X~X'      (con haplología de la vocal final de la 2.ª copia)
Valor: (a) formación de nombres de animales por onomatopeya
       (b) pluralidad o abundancia del referente
Ejemplo canónico: juri 'viento' → juri~jur-ebo 'paso de los vientos'
```

⚠ El valor (a) es **formación léxica, no morfología viva**: un agente no
debería reduplicar para "inventar un ave". El valor (b) sí es candidato a regla
productiva en el habla.

**2. `-are` locativo** — afijo nuevo, 'sitio de, paraje de'. Es el que más
amplía lo que los agentes pueden *construir*: hoy `REGLAS_ZAVALA` tiene `-ana`
'lugar de' y `-bana` 'orilla/borde', pero ningún sufijo para 'sitio donde se
hace X'. Cuatro topónimos lo glosan literalmente así.

**3. `-bacoa` colectivo/locativo** — 'paraje cubierto de'. El morfema ya está
en el lexicón como palabra (`bacoa` 'bosque'); lo que falta es registrar su
**uso sufijal productivo**, que es lo que muestran los cinco topónimos.

---

## 7. Conflictos que este análisis abre

Para [[DECISIONES_ABIERTAS]] y para la tarea F1 del censo de citas:

| Conflicto | Evidencia |
|---|---|
| **`quiba`** 'ayuda' vs. 'piedra' | `quibacoas` "Bosques **pedregosos**" + van Buurt §8 apoyan 'piedra'. Probable homógrafo mal fusionado. |
| **`guaca`** 'ave, cotorra' vs. `waka` 'subterráneo' | `guacaubana` "Río **escondido**" apoya 'subterráneo'. Dos morfemas distintos bajo la misma grafía castellana. |
| **`-are`** 'sitio de' vs. **`-ure`** 'raíz' | Evidencia toponímica contra Cruz Esteves 1989 vía van Buurt §5. Hermana de la D9 de `-bana`. |
| **`barici` / `bariki`** | Dos entradas con glosas solapadas y una raíz probable `bari-`; `barisi` y `bariquisimeto` conservan las dos variantes. |

---

## 8. Lo que queda abierto

**El formante `-shi`/`-chi` es el más frecuente del corpus insular —22
apariciones— y nadie lo ha glosado.** Ni [[gatschet-1885]], ni
[[van-buurt-2014]], ni [[zavala-reyes-2015]]. *Balashi, Hudishibana, Arashi,
Bushiri, Cadushi, Canashito, Cashunti, Catashi, Cudishi, Macoshi, Tibushi,
Teishi, Sasarawichi, Angochi, Anamichi*… Es el objetivo nº 1 de cualquier
minería futura de toponimia ABC.

También quedan `-ari`/`-ri` (7, glosado solo dentro de *Casibari*) y
`-kuri`/`-curi` (3, ya señalado en `SUFIJOS_NO_CODIFICADOS` de
`lexicon_gatschet`).

Y quedan **ocho topónimos opacos con glosa perfectamente utilizable** —
*aburi*, *acatute*, *alcaboa*, *aricula*, *guanajo*, *guasare*, *siguruba*,
*tarai*— que hoy no descomponen porque el inventario de morfemas no da. Una
segunda pasada, después de que F1 aplique las 62 citas recuperadas y de que se
minen [[oliver-1989-cap2]] y [[oviedo-y-banos]], podría resolver alguno.

---

## 9. La expectativa realista, con números

Igual que [[02_protocolo_habla_paraguanera]] §7, conviene poner la cifra antes
de que alguien la infle:

**De 45 topónimos continentales con glosa salieron 6 descomposiciones
confirmadas, 3 morfemas nuevos y 10 corroboraciones del lexicón.** Es un
rendimiento del orden del 25 % sobre el material realmente utilizable, y del
5 % sobre las 318 formas del corpus toponímico total. Los 244 topónimos
insulares aportaron **cero ecuaciones** — solo recurrencia.

No es un filón. Es un método barato que exprime material que ya estaba en el
repositorio y que estaba marcado como inerte, y que de paso encontró una regla
morfológica que faltaba y cuatro conflictos del lexicón. Contado así, y no de
otra manera.

---

## Enlaces

[[02_protocolo_habla_paraguanera]] · [[DECISIONES_ABIERTAS]] · [[PLAN_MAESTRO]] · [[zavala-reyes-2015]] · [[gatschet-1885]] · [[van-buurt-2014]] · [[alvarado-1921]] · [[oliver-1989-cap2]] · [[oviedo-y-banos]]
