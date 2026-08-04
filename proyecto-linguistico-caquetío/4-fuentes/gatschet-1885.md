---
tipo: fuente
obra: "The Aruba Language and the Papiamento Jargon"
autor: "Gatschet, Albert S. (material recogido por Alphonse L. Pinart, 1882)"
anio: 1885
publicacion: "Proceedings of the American Philosophical Society XXII(120), pp. 299-305 (leído el 18 de julio de 1884)"
genero: vocabulario
local: ["fuentes_caquetios/Gatschet_1885_Aruba_texto.txt", "fuentes_caquetios/Gatschet_1885_biostor_texto.txt"]
paginas: "7 (pp. 299-305; dos OCR del mismo artículo)"
capa_texto: si
estado_minado: minado
prioridad: alta
tareas: [F4]
sostiene: {hechos_corpus: 0, entradas_lexicon: 4}
verificado: 2026-08-03
minado: 2026-08-03
minador: "curiana_sim/minar_gatschet.py"
propuesta: "curiana_sim/lexicon_gatschet.py"
aliases: ["Gatschet 1885", "Pinart 1882", "The Aruba Language"]
---

# Gatschet 1885 — *The Aruba Language and the Papiamento Jargon*

## Qué es

**Vocabulario caquetío insular directo**, recogido en 1882 por Alphonse Pinart
*de hablantes ancianos de Aruba* cuando la lengua ya estaba extinguiéndose
(los arubanos habían abandonado su lengua por el papiamento hacia 1800). Gatschet
lo publica con su propio análisis comparativo.

Su relevancia para el proyecto está en una sola frase del artículo: *"The Aruban
language was probably the same as that of Curaçao and **related to the vernacular
of the peninsula of Paraguaná**"* — es decir, el caquetío del Golfete.

## Estado técnico (verificado 2026-07-29)

| Dato | Valor |
|---|---|
| Formato | **dos .txt** (18 KB y 17 KB): **el mismo artículo**, dos OCR distintos (JSTOR Early Journal Content y BioStor) |
| Capa de texto | sí — es texto plano |
| Artefacto | Ambos arrancan a mitad de **otro** artículo (química de aceites de 1884); el contenido útil empieza en *"THE ARUBA LANGUAGE AND THE PAPIAMENTO JARGON"* (línea 77 del archivo Aruba) |
| Recomendación | Usar los **dos** en paralelo: donde uno tiene OCR sucio, el otro suele resolver |

---

## Qué ha dado (minado 2026-08-03, tarea F4)

**79 formas transcritas y reconciliadas** entre los dos OCR: 48 léxicas
+ 31 topónimos, más **6** fórmulas de hechicería (no cinco: Gatschet anuncia
*"six sorcerer's formulas"* en la prosa y publica seis). El minador
(`curiana_sim/minar_gatschet.py`) verifica cada forma contra ambos OCR y grita
si alguna no tiene respaldo; **77 están sostenidas por los dos**, `xovam` y
`Kodekodektu` solo por JSTOR, ninguna huérfana.

Veredictos según [[02_protocolo_habla_paraguanera]] §5 — la propuesta completa,
con la razón de cada uno, está en `curiana_sim/lexicon_gatschet.py`:

| Nivel | N.º | Qué son |
|---|---|---|
| **A** — atestiguada | **12** | `dabaraida`, `hubada`, `dividivi`, `kaduski`, `shimaruko`, `surun`, `watapana`, `shushubi`, `warawara`, `dori`, `paluli`, `waltaka` |
| **B** — fuerte | **2** | `makura`, `tuturutu` |
| **C** — plausible | **25** | todo el bloque de "nouns, verbs and sentences" salvo tres, más `kipopo`, `lokiloki`, `yoroyoro`, `ginga`, `karma-u`, `kurkur`, `puruntsi`, `kinikini`, `krabete`, `hanahana`, `kimakima`, `lembelembe` |
| **D** — descartada | **9** | ver *Descartes razonados* abajo |
| **T** — topónimo | **31** | canon y morfología, fuera del habla |
| **R** — fórmula ritual | **6** | texto no traducible, valor ritual, **no léxico** |

**14 de 48 formas léxicas (29 %) sobreviven en A o B.** Para una lista que su
propio compilador moderno acusa de contener palabras *"definitely not Indian"*,
es un rendimiento alto — pero conviene decir de dónde sale: **todas las A menos
una tienen atestación externa en [[van-buurt-2014]] §6**. Sin van Buurt, Gatschet
solo sostendría nivel C. La fuerza de esta fuente no está en lo que dice sola,
sino en que **coincide con dos corpus independientes**.

### Lo mejor que dio: la triple atestación

Cinco formas quedan atestiguadas por tres vías independientes —
**continental** ([[zavala-reyes-2015]], Falcón), **insular 1882** (Pinart) y
**viva** (van Buurt 2014). Eso es exactamente lo que la frase de Gatschet sobre
Paraguaná predice, y ahora está medido y no supuesto:

| Forma | Continental (Zavala) | Insular 1882 (Pinart) | Viva (van Buurt) |
|---|---|---|---|
| paraulata | `chuchube` #85 | `shushubi` | `chuchubi` |
| cardón | `caduchi`/`caduche` | `kaduski` | `kadushi`/`cadushi` |
| dividivi | `dividive` #112 | `dividivi` | `dividivi` |
| semeruco | `cemaruco`/`semerúca` | `shimaruko` | `shimarucu` |
| clavellino | `tuturutos` #264 | `tuturutu` | — |

La alternancia **sh~ch / ski~shi** entre columnas no es ruido: van Buurt
argumenta que la forma insular con /ʃi/ es **la más original**, porque el español
no genera ese grupo. La correspondencia queda documentada en el minador
(`NORMALIZACION_ORTOGRAFICA`) para que el cruce sea reproducible.

### Dos hallazgos que no se buscaban

1. **`warawara` está mal glosada en el lexicón, y la culpa es de esta fuente.**
   La entrada dice *"buitre, zamuro (Cathartes curasoica)"* — que es, palabra por
   palabra, la identificación de Gatschet de 1885. El proyecto la heredó sin
   saber de dónde venía. **Es un caracara** (*Caracara cheriway*, Falconidae),
   no un zamuro (Cathartidae). Caso de manual para la política **D7**: la glosa
   de 1885 se conserva en `glosa_fuente`, la moderna en `identificacion_moderna`,
   pero **el lexicón activo debe corregirse**.
2. **`surun` se resolvió cruzando los dos OCR.** JSTOR lee *"Oratera gynandra"*
   y BioStor *"Gratera gynandra"*: ninguno de los dos es un género real. Juntos
   reconstruyen ***Crateva gynandra*** L. — y van Buurt confirma
   independientemente, en su entrada `ishiri`, *"also called Surun"*, con el
   taxón moderno *Crateva tapia*, del que *C. gynandra* es sinónimo. Es el
   argumento más limpio de por qué se usan los dos OCR en paralelo.

### Los 31 topónimos: el resultado más sólido

**29 de los 31 siguen vivos en Aruba** y [[van-buurt-2014]] §7 los da como
topónimos probablemente caquetíos. Solo `Handebirari` y `Hendieku` no reaparecen.
La reconciliación de OCR arregló varios: `Malividiri` (JSTOR) es errata de
**Matividiri**, y `Shabaruri` es **Shabururi** (BioStor). Y `Matividiri` tiene
gemelo continental: van Buurt registra **Matividiro**, cerro y caserío de
**Paraguaná** — el vínculo isla↔península que Gatschet postuló, en un topónimo
concreto.

### ¿Validan los topónimos los afijos de `REGLAS_ZAVALA`? Parcialmente

Confirmación cruzada real, porque Zavala compila el continente y Pinart la isla:

| Afijo del proyecto | Apoyo insular | Lectura |
|---|---|---|
| `-aima` | **Kibaima** | 1 caso; débil pero limpio |
| `-ubana` | **Wakubana** | 1 caso, y van Buurt lo etimologiza (`waka` subterráneo + `-bana` 'cubierto'), corroborando el afijo |
| `-uru` | **6** (Shabururi, Warerukuri, Antikuri, Kamakuri, Wariruri, Weburi) | el más frecuente, en la variante `-uri` |
| `-bana` (locativo) | **4** (Shiribana, Tarabana, Wakubana, Bushiribani) | forma validada, **glosa en disputa** (ver abajo) |
| `-iro`, `-ima`, `-uco` | **0** | los topónimos arubanos no los sostienen |

Dos matices que el minado obliga a registrar, y que son decisiones abiertas:

- **`-bana`**: el proyecto lo glosa *"orilla/borde"*. Van Buurt da dos lecturas
  distintas y ninguna es esa: *'wide, plain'* (Hudishibana = 'llanura ventosa')
  y, vía Oliver, *'cubierto'*. La **forma** del afijo queda confirmada por cuatro
  topónimos insulares; **su significado, no**.
- **`-uri`/`-uru`**: Zavala lo registra como *"desinencia de valor no precisado"*.
  Van Buurt propone que el papiamento `-uri/-huri` equivale al caquetío
  continental `-ure` = **'raíz'** (Cruz Esteves 1989). Seis topónimos arubanos lo
  sostienen. Sería la primera glosa disponible para ese afijo.
- **`-bari` no es un afijo.** Aparece en tres topónimos (Yabarubari, Cubari,
  Kassibari) y tienta, pero van Buurt descompone `Casibari` como
  **ka-siba-rí** = 'ahí hay rocas duras'. Es `siba` 'piedra' + `-rí`, no `-bari`.
  Anotado para que nadie lo "descubra" dentro de seis meses.

### Las 6 fórmulas de hechicería

Registradas en `GATSCHET_FORMULAS` con etiqueta `ritual-no-traducible`: **no se
segmentan, no se glosan, no puntúan**. Pinart le insistió a Gatschet en que son
citas literales de la lengua arubana extinta y no sílabas sin sentido, pero no
consiguió traducción palabra por palabra. Material de primer orden para el habla
del piache ([[mapa-creencia]]) precisamente por ser **opaco**.

Un único fragmento tiene glosa parcial propuesta, y es de van Buurt: en la
primera fórmula para sacar espinas de cactus, `daburi` podría designar las
espinas, por su parentesco con `dabaraida`/`dabaruida` y el lokono *dabáda*
'uña, garra'. Tres palabras de las fórmulas reaparecen en las listas —
`kafa`, `datie` y `watapuna` (cf. `watapana`) —, que es el mejor argumento
disponible a favor de la tesis de Pinart.

---

## Descartes razonados

Documentar el descarte vale tanto como el hallazgo: evita re-minarlas.

| Forma | Glosa de Gatschet | Filtro | Razón |
|---|---|---|---|
| `ute kontabo` | how do you do? | 2 — papiamento | **Papiamento transparente**: `kontabo` es *kon ta bo* '¿cómo estás?', con *bo* de 2.ª persona. Probablemente una de las voces que van Buurt tenía en mente. |
| `totumba` | water-gourd | 4 — antillanismo | Derivado de *totuma*, voz caribe/taína ya en el DRAE y usada en toda Hispanoamérica. |
| `jobo` | Spondias lutea | 4 — antillanismo | Taíno panamericano, del DRAE. |
| `kumexen` | Termes fatalis | 4 — antillanismo | Es ***comején*** en la ortografía afrancesada de Pinart. Voz taína del español general. |
| `takamahak` | "Ragara octandra" | 4 — voz de circulación europea | *Tacamahaca*, del náhuatl *tecomahiyac*; entró a la farmacopea europea del s. XVIII. Llegó por comercio, no por sustrato. |
| `nandu` | Cytisus catjan | 5 — africanismo | **Doble descarte**: la especie (*Cajanus cajan*, quinchoncho) es del Viejo Mundo, introducida — no puede tener nombre precontacto; y la forma es el papiamento *wandu*, del kimbundu. |
| `mamondenga` | Ichneumon niger | 5 — africanismo | Estructura bantú (ma- + -ndenga). |
| `guruguru` | Calandra granaria | 1 — español / referente introducido | *Sitophilus granarius* es plaga paleártica del grano europeo; y la forma remite a *gorgojo*. |
| `xovam` | phantom, hobgoblin | forma irreconstruible | JSTOR lee `xovam`, BioStor lee `;tomoi`. No es un problema de etimología: no sabemos qué palabra es. |

> Van Buurt explica el patrón: la mezcla temprana de la población indígena
> arubana con población de origen africano *"can explain some of the African
> words found in the Indian wordlist compiled by Pinart in Aruba"*. Los dos
> africanismos y los cuatro antillanismos son, casi con seguridad, las
> *"several words which are definitely not Indian"* de su crítica.

⚠️ Y una advertencia que la fuente se pone a sí misma: **la única correspondencia
comparativa que Gatschet creyó encontrar no se sostiene.** Comparó `kafa`
'diablo' con el goajiro *yaria/yarias/yaroja* — dos formas que no comparten ni
una consonante. Su segunda analogía (`hanahana` ~ caribe insular *hage* 'hormiga')
apunta además a **contacto caribe, no a herencia arahuaca**. El propio Gatschet
lo atribuye a lo raro de la selección de términos, su escasez y su probable
deformación en boca de hablantes no instruidos.

---

## Cobertura de las 82 entradas del lexicón sin cita (insumo para F1)

**5 resueltas de 82.**

| Palabra | ¿Aparece? | Forma en Gatschet | Cita | Veredicto |
|---|---|---|---|---|
| `watapana` | **sí** | `watapana` | *"Names of plants: … watapana Sapindus coriaria"* (p. 301) | **RESUELTA**. Añadir cita; corregir el taxón a *Libidibia coriaria* (Gatschet puso el género equivocado). |
| `warawara` | **sí** | `warawara` | *"Names of birds: … warawara Oathartes [Cathartes] curasoica"* (p. 302) | **RESUELTA — y con corrección**: la glosa del lexicón *es* esta identificación de 1885. Hoy: *Caracara cheriway*. |
| `chuchubi` | **sí** | `shushubi` | *"shushubi Orpheus amerieanus [americanus]"* (p. 302) | **RESUELTA** vía la variante insular con sh-. Triple atestación con Zavala #85 y van Buurt §6. |
| `kadushi` | **sí** | `kaduski` | *"kaduski Oereus [Cereus] laniginosus"* (p. 301) | **RESUELTA en la forma**; el **referente queda abierto**: Gatschet dice *Pilosocereus lanuginosus*, van Buurt *Cereus repandus*, el lexicón *Cereus hexagonus*. Es un genérico de cardón, no una especie. |
| `kunuku` | **sí, pero** | `cunucu` | *"Muchas en el campo — jopi na cunucu"* (guía de conversación de Curazao, 1876, citada p. 304) | **RESUELTA** — pero la cita es de la sección de **papiamento**, no de la lista arubana. Atestigua circulación insular, no origen. |
| `pauji` | **no** | `pajuis` | *"pauji pajuis"* (p. 303) | **NO RESUELTA**: `pauji` está ahí como la voz **española** de la columna izquierda; el papiamento es *pajuis*. No sirve de cita caquetía. |
| `auyama` | **no** | `pampuna` | *"ahullama pampuna"* (p. 303) | **NO RESUELTA**: igual que `pauji`, aparece como voz española del guía. |
| `chiriguare` | **no** | — | En la sección papiamento el 'gavilán' es *guaraguara* (= `warawara` con w→gu castellanizante), no *chiriguare*. | **NO RESUELTA**. |
| `tuqueque` | **no en Gatschet** | — | van Buurt §6 s.v. `waltaca`: *totèki* deriva de *"tuqueque, tuteque, an Amerindian word used for geckos in Venezuela"*. | Cita **disponible**, pero es de F6, no de F4. |

Las 73 restantes de las 82 no tienen rastro en esta fuente. Gatschet cubre
**fauna, flora y toponimia insulares**; el lexicón sin cita es mayoritariamente
vocabulario continental de parentesco, tiempo, agricultura y política
(`buiamati`, `datihao`, `cazicure`, `duraboa`, `guaitiao`…), que esta fuente no
toca. Para esas, las candidatas son [[zavala-reyes-2015]], [[alvarado-1921]] y
[[oliver-1989-cap3]].

---

## Qué falta

1. **Decisión humana sobre las 12 de nivel A** — ninguna entra a
   `VOCABULARIO_BASE` por este camino sin revisión explícita (protocolo §5,
   regla de oro). Ocho de las doce **no están en el lexicón** (`dabaraida`,
   `hubada`, `shimaruko`, `surun`, `shushubi`, `dori`, `paluli`, `waltaka`) y
   cierran huecos de fauna y flora insulares.
2. **Corregir `warawara` en el lexicón** (*Caracara cheriway*, no *Cathartes*)
   y añadir cita a las cuatro que ya están. Es la parte accionable inmediata.
3. **Resolver el referente de `kadushi`**: tres cactus en tres fuentes. Decidir
   si la entrada se reglosa como genérico ('cardón columnar') en vez de fijar
   una especie.
4. **Las dos decisiones de afijo** (`-bana` con glosa en disputa, `-uri/-uru`
   con glosa nueva propuesta por Cruz Esteves vía van Buurt) son para
   `DECISIONES_ABIERTAS.md`, no para este minado.
5. **Facsímil de las pp. 299-305** para cerrar `xovam` y el imperativo
   `?aba dobo…guayete`, que los dos OCR rompen en el mismo punto. Es lo único
   que un tercer testimonio digital resolvería.
6. **Cruce pendiente con [[van-buurt-2014]] completo (F6)**: aquí se usó su
   glosario como control externo, no se minó. Al minarlo, su §6 y §11 darán la
   escala epistémica ya construida por el propio autor.

## Enlaces

[[van-buurt-2014]] · [[zavala-reyes-2015]] · [[alvarado-1921]] ·
[[oliver-1989-cap3]] · [[02_protocolo_habla_paraguanera]] ·
[[mapa-creencia]] · [[mapa-motor]] · [[mapa-geografia-politica]] · [[INDICE_FUENTES]]
