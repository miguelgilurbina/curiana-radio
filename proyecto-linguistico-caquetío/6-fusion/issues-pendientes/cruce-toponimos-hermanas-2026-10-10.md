# El cruce de los topónimos con las hermanas, y qué hace `-ana` fuera del caquetío

**Para que Miguel decida.** El 2026-10-10 Miguel aprobó un pase que nunca se
había hecho —cruzar los topónimos caquetíos sin lectura con las lenguas
hermanas— y pidió que entrara `-ana`: «hasta el día de hoy está solamente en
Chamuriana, Jayana, Curiana, Cujicana también. Pero si vamos a compararlo con
el lokono, el lokono también tiene Guayana o Guyana… podríamos tener más
referencias sobre cómo lo utilizan los lokonos o los taínos». Todo el detalle,
con obra, página y cita corta, está en
`6-fusion/cruce_toponimos_hermanas_2026-10-10.yaml`, que emite
`6-fusion/scripts/cruzar_toponimos_hermanas.py` (lo leído a mano va en sus
constantes; lo contado lo cuenta el script). La bitácora es
`4-fuentes/sesiones/14_cruce_toponimos_hermanas.md`. No se descargó nada y no
se tocó `2-lengua/`, `3-mundo/`, `curiana_sim/` ni el lexicón.

Para leer las decisiones: **hermana** = línea lokonoide (taíno, lokono,
kalinago por su sustrato iñeri); **prima** = achagua, maipure, wayuu,
paraujano. La regla para reconstruir con una prima sigue sin decidir: aquí
cada candidato dice de qué línea viene, y nada más.

---

## Lo que se halló, en ocho líneas

1. **Nadie glosa un `-ana` como 'lugar de'.** Ni las hermanas ni las primas.
   La retirada de #109 se confirma desde fuera.
2. **Lo que sí recurre es un `-(a)na` de GENTE**, en dos hermanas y con fuente
   primaria: el linaje matrilineal lokono toma su nombre de la antepasada
   (*Ebesō-tu* → *Ebeso-ana*, *Demare-du* → *Demaré-na*; Brett 1880
   pp. 178-179) y el gentilicio kalinago es isla + `-ri` 'un habitante' / isla
   + `-na` 'los habitantes' (*Ouâitoucoubouli-na* 'los de Dominica',
   *caloucaera-na* 'los de Guadalupe'; Breton 1665 p. 416 y la Grammaire de
   1667: «Les pluriers terminez en a»).
3. **Guayana no es un `-ana` lokono.** En el repo nadie da la «tierra de
   muchas aguas». Goeje 1939 (p. 5) dice que el país toma el nombre de un
   pueblo, los Guayana, junto a la boca del Caroní, y que su lengua era
   caribe; Bachiller 1883 (p. 277) lo deriva de Guainía, de tercera mano. Es
   un etnónimo pasado al país: lo mismo que el punto 2, visto desde fuera,
   pero de un pueblo caribe.
4. **El taíno da un caso, y otro valor**: «Llamaban los indios á la Vega
   grande Magua […] y á esta provincia decían con adición Maguana, cuasi la
   Vega menor» (Las Casas, *Apologética*, cap. VII, p. 19). `-na` = 'la
   menor'. Es la primaria que la lista maestra taína no tenía (allí era
   «ii-solo-secundaria»).
5. **El achagua no ayuda.** Su «locativo -ana» de la transcripción es el `-na`
   relacional de *numa* 'boca' (*Casanare Numana* 'boca de Casanare', *Vní
   numāna* 'boca del río'), no un sufijo de lugar.
6. **El cruce general no saca nada por encima del azar en las hermanas.**
   De 250 topónimos, 146 tienen un referente con el que filtrar. Lokono: 11
   topónimos con par frente a 9,4 por azar; taíno: 68 frente a 63,2. El
   kalinago (25 frente a 14,9) sí sale por encima, pero lo empujan dos
   cognados que el canon **ya tiene** —la piedra (*šiba* ~ *kiba*) y el mar
   (*balaua*, *barana* ~ *para*)—. El achagua (45 frente a 27,4) vuelve al
   azar con una voz por familia (16 frente a 11,1). El método funciona: en el
   propio caquetío recupera 39 lecturas que el canon ya tenía.
7. **Fauna en `-re`**: ninguna hermana ni prima tiene la misma raíz para el
   mismo animal (bisure, chaure, chiriware, bayure, yakure…). Todo bajo el
   umbral.
8. **Mapanare**: ninguna fuente del repo da su origen. Pero **sí hay una
   culebra llamada manare**: Alvarado 1921 p. 200, «CULEBRA-SAPA manare.
   Pequeña serpiente […] hecha un rollo […] Es mui ponzoñosa» (Portuguesa).

---

## Las decisiones

### D1 · La glosa de `-ana` (la principal)

- **A.** Dejarlo como está: forma atestiguada **sin glosa** (#109, d21.6). El
  pase confirma que 'lugar de' no tiene base en ninguna línea y no aporta una
  glosa caquetía.
- **B (recomendada).** Registrar un **candidato**: `-ana` 'los de X, la gente
  de X' (colectivo de gente, gentilicio), **capa hipotética**, línea
  lokonoide (lokono + kalinago). El topónimo sería el nombre de una gente
  pasado al lugar, como Guayana. Encaja con Curiana, que nombra «el pueblo» y
  «la costa» a la vez (Arcaya p. 169), y con *Coria-na* y *Paragua-nil* como
  nombres de aldea en La Ramada (Castellanos p. 264). No se enseña con glosa
  todavía: se cuelga como lectura en los cinco nombres y en `morfema-011`.
  - **Por qué no reconstruido**: el caquetío no tiene un solo `-ana`
    glosado, y el paso de gentilicio a topónimo es inferencia nuestra
    (regla 2). Lo subiría un `-ana` caquetío que una fuente use como nombre
    de GENTE, o una de las 27 familias lokonas de Hilhouse en `-ana` con su
    epónimo.
  - **Contra**: el único caso taíno (Maguana) da otro valor, 'la menor'.
- **C.** Esperar a dos fuentes que el repo no tiene: Williams 1923 («The
  name “Guiana”») y Hilhouse 1832/1834 (las familias lokonas).

Si eliges B, la glosa se escribe en `morfemas.yaml` por su generador y el
prompt sigue diciendo «sin glosa» hasta que decidas si los agentes la ven
(es un corte de serie, como d21.6).

### D2 · Las lecturas de la campaña

Ninguna sube un nombre por encima de C. Si te parecen, la campaña las cuelga
(`lecturas` en `lexicon_toponimos.py`):

| Topónimo | Hoy | Propuesta | Lectura | Línea | Por qué débil |
|---|---|---|---|---|---|
| **manare** (239) | C | C | la tuya (culebra de ojos amarillos) + Alvarado p. 200 (culebra-sapa manare) | — | la culebra de Alvarado es llanera y sin color de ojos |
| **capadare** (016) | C | C | ~ lokono *kabadaro* 'jaguar': la palabra entera, y «diente de tigre» relectura de *-dare* | hermana, con reserva (el lexicón lo da por préstamo del caribe insular) | una lengua, y préstamo |
| **siraba** (285) | descartado | C si aceptas media ecuación | *si(ra)ba* 'piedra' (taíno *ciba*, lokono *siba*, kalinago *šiba*) en el cerro de los petroglifos | hermana, las tres | queda un *-ra-* |
| **cimiro** (298) | descartado | C | *sim(a)* 'cerro' + *-iro* 'cerrito' | propia (sima reconstruido) | dos piezas de capa baja; Esteves: «no parece voz indígena» |
| **amuay** (090) | C | C | ~ kalinago (mujeres) *šauai* 'acantilado, caverna' | hermana | m- frente a š- |
| **bajarigua** (264) | descartado | descartado | ~ taíno *bagua* / kalinago *balaua* 'mar' | hermana | el campo 'mar' es el que más da por azar |
| **paraguaná** (018) | C | C | -ná como resto de *naka(n)* 'en medio' (taíno *nacan*, lokono *annakan*): el «en medio del mar» de Esteves con morfema | hermana | exige perder -kan |

Opciones: **A** colgarlas todas como `hipotesis` (la de Miguel como
`testimonio-residente`, la de Alvarado como `glosa-fuente`); **B** sólo
manare y capadare; **C** ninguna.

### D3 · Una palabra para el lexicón: *nakan* 'en medio, centro'

Dos hermanas la tienen: taíno *nacan* «medio ó en medio» (Las Casas,
*Historia*, lib. I cap. XLIV, por Cubanacan) y lokono *annakan* 'centro' /
*a-nnakù-di* 'estar en medio' (Perea p. 647). Por la regla de la tanda de las
hermanas (dos hermanas = reconstruida), sería **reconstruida**, y cubre un
hueco: el caquetío no tiene voz para 'en medio'. La forma es nuestra (el
segmento común). **A** proponerla a `fusionar-propuesta`; **B** dejarla en
`6-fusion/` hasta que algo caquetío la toque (Paraguaná, si D2 pasa).

### D4 · Fuentes a pedir (lo decides tú)

1. **J. Williams 1923**, «The name “Guiana”», *Journal de la Société des
   Américanistes* XV — la discusión de la etimología que circula.
2. **C. H. de Goeje**, «Guayana and Carib tribal names» (XXI Congreso de
   Americanistas) — la base de su p. 5.
3. **W. Hilhouse 1832/1834** (*Journal of the Royal Geographical Society*) —
   las 27 familias lokonas de Brett, con sus nombres.
4. **Goeje 1928** y **Pet 1987** — la fuente de *kabadaro* 'jaguar'.
5. **D. Taylor 1977**, *Languages of the West Indies* — el gentilicio
   `-ri`/`-na` del caribe insular, con su estrato.
6. Un **diccionario de venezolanismos con etimología** para *mapanare*.

---

## De paso

- **Capadare y el felino.** La razón del canon dice «el lexicón no tiene
  ninguna palabra para felino»: la tiene, como comparanda lokona
  (*kabadaro*). Corregir la frase no depende de D2.
- **Carvajal escribe «manaures»** por *manares* (los cernidores) en 1647, y
  Alvarado lo corrige (p. 199): ya está en la sesión de los Manaure de
  Colombia, y la culebra-sapa y la avispa manare de la p. 200, no.
- **Achagua**: *chamanare* es la iguana (pliego 69) y *manari-* 'calamidad,
  perderse' (pliegos 31, 47, 82); *mapanarí* es una **palma** (pliego 80). Si
  alguien vuelve a tentar *mapanare* por el achagua, que lea primero esto.
- **La esfera en la toponimia**: Pitajaya y Guayacanal casan enteros con
  voces taínas de planta que el castellano trajo (*pitajaya*, *guayacán*,
  atestiguadas por Las Casas y Oviedo). Son producto de la esfera, no
  caquetío, y el canon ya los tiene por fitónimos.
