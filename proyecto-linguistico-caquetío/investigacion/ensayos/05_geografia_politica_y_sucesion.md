---
tipo: ensayo
sesion: 5 — seguimiento del programa corpus cultural
pregunta: "¿Cuál era el área de influencia de Manaure, y qué asentamiento real reconstruimos?"
moc: MOC_geografia_politica
corpus: [geografia_politica.yaml, parentesco.yaml]
fuentes: [oliver-1989-cap3, zavala-reyes-2015, van-buurt-2014, arcaya-1920, ramos-perez-1978, oviedo-y-banos]
decisiones: [D2, D4]
---

# La geografía política de Manaure: quién era un diao, y qué asentamiento reconstruimos

*Sesión 5 del programa "corpus cultural" — Curiana, Golfete de Coro, siglos XIV-XV.*
*Surge de una conversación con Miguel (2026-07-13 a 2026-07-20) sobre la sucesión de Manaure y la
escala real del mundo caquetío. No repite el canon existente (CULTURA_CAQUETIA.md §6, "Política y
jerarquía"; el ensayo 01, "familia caquetía"): lo precisa con vocabulario atestiguado y geografía
concreta.*

> **Mapa** · [[MOC_geografia_politica]] — [[05_geografia_politica|hoja de fuentes]] — `geografia_politica.yaml`
> **Fuentes** · [[oliver-1989-cap3]] · [[zavala-reyes-2015]] · [[van-buurt-2014]] · [[arcaya-1920]] · [[ramos-perez-1978]] · [[oviedo-y-banos]]
> **Decisiones que deja abiertas** · [[DECISIONES_ABIERTAS|D2 (el nombre "Curiana")]] · [[DECISIONES_ABIERTAS|D4 (segundo sobrino)]]
> **Sigue de** · [[01_familia_caquetia]]

---

## 1. El problema de partida

El canon ya dice que la Curiana es *"un cacicazgo jerarquizado dentro de una red mayor de cacicazgos
caquetíos del noroeste venezolano"* (CULTURA_CAQUETIA.md:218), y que Manaure gobierna *"redistribuyendo,
no solo ordenando"*. Pero esa "red mayor" quedaba sin nombre, sin escala y sin vocabulario propio.
Esta sesión responde tres preguntas que Miguel planteó en cadena:

1. ¿Es el mismo mecanismo de sucesión para un jefe de linaje que para Manaure, que además funde
   autoridad política y religiosa (el rol de *boratio*)?
2. ¿Qué pasa si hay más de un sobrino elegible?
3. ¿Cuál es, en concreto, el área de influencia política de Manaure — y qué asentamiento real
   corresponde al "la Curiana" que la simulación modela?

## 2. Vocabulario atestiguado de rango: *apopo*, *diao*, *boratio*

Zavala Reyes (2015), la fuente central de todo el proyecto para el lexicón atestiguado, tiene un
glosario de 288 entradas compiladas por nueve autores (identificados por iniciales: PMA = Pedro
Manuel Arcaya, HB = Adrián Hernández Baño, E = Juan Esteves, AM = Angulo Molina, A = Lisandro
Alvarado, GC = Galeotto Cey, CGB = Carlos González Batista, AAM = Antonio Arellano Moreno, HP =
Aníbal Hill Peña). Tres entradas dan un sistema de rango de tres niveles:

- **Apopo** (p. 65, entrada 12, AM): *"Nombre de jefe de parcialidad pequeña."* — cabeza de un
  subgrupo o linaje pequeño, dentro de un solo asentamiento.
- **Diao** (p. 67, entrada 106, HB+AM): *"Señor principal. Jefe mayor."* — no "de segundo orden",
  como tenía `curiana_lexicon.py` sin cita hasta esta sesión.
- **Boratio** (p. 66, entrada 43, AM+HB): *"Piache, cacique, jefe, sacerdote, médico."* — una sola
  palabra que funde autoridad política, religiosa y médica, más rica que el "adivino o sacerdote"
  que la sesión 3 (creencia) ya había encontrado vía Jahn (1927: 213, n. 29, citando a Oviedo).

Y en el cuerpo del propio artículo de Zavala (p. 60), dos crónicas se citan una junto a otra
describiendo, aparentemente, la misma figura: Oviedo y Baños (1855: 27) sobre *"el Manaure
coriano"*, *"señor de toda aquella provincia... a quien rendían vasallaje algunas circunvecinas"*;
y Ramos (1978: 237), sobre *"el Diao"*, *"poderoso para todo y... casado con hijas de los dichos
caribes"*. La lectura más simple no es que "Diao" sea sinónimo exclusivo de Manaure, sino que
**Manaure ES un diao** — el de Coro — además de tener un estatus adicional (ver §4).

Esta lectura se confirma, de forma independiente, en el propio Oliver (1989, cap. 3, p. 251), quien
narra el pacto de 1527 con Ampíes y escribe: *"the stage was set for a series of dialogues... between
Ampíes and the main diao or great cacique, Manaure."* Dos fuentes académicas distintas (Zavala/Ramos
y Oliver), sin relación entre sí que sepamos, coinciden en llamar a Manaure **"el diao principal"** —
no el único diao, el principal entre varios.

## 3. El modelo de tres niveles

Con ese vocabulario, la jerarquía queda así:

| Nivel | Escala | Ejemplo en el elenco |
|---|---|---|
| **Apopo** | cabeza de parcialidad/linaje pequeño, dentro de un asentamiento | Corie-ko, Chiriguare, Paugis-sha/Sha-corie, cada uno cabeza de su linaje |
| **Diao** | señor principal de un asentamiento o polity entero | Manaure, diao de Coro/Todariquiba — y, por el mismo título, presumiblemente cualquier otro asentamiento caquetío importante (Barquisimeto, Yaracuy) tendría el suyo |
| **Paramountcy** | reconocimiento, NO automático, de un diao como principal entre diaos vecinos | Manaure sobre "algunas circunvecinas" (Oviedo y Baños 1855: 27) |

La pieza que hay que calibrar con cuidado es la escala de la paramountcy. Miguel propuso inicialmente
que Manaure "reunía" a los diaos de Barquisimeto y Yaracuy. Los datos disponibles apuntan a algo más
modesto y más preciso: la mención de Barquisimeto y Yaracuy que tenemos (Arcaya 1920: 27-28, vía
Zavala 2015 p. 60) es un elogio de **carácter moral compartido** a lo largo de toda la diáspora
caquetía (Curazao y Aruba, Barquisimeto y Yaracuy, los llanos de Barinas y Apure, Casanare) — evidencia
de una esfera **cultural** amplia, no de que esas poblaciones concretas rindieran vasallaje político a
Manaure. Barquisimeto y Yaracuy están demasiado lejos tierra adentro para ser las "algunas
circunvecinas" de Oviedo, que describe algo local: comunidades cercanas al Golfete/Paraguaná.

**Conclusión de diseño:** *diao* es un título genérico, atestiguado para cualquier señor principal a
lo largo de toda la esfera caquetía — Coro tiene el suyo, y es razonable que Barquisimeto y Yaracuy
tuvieran los propios, sin relación de vasallaje entre ellos. Manaure es el diao de Coro que además
logró (no heredó automáticamente) el reconocimiento de unas pocas comunidades vecinas cercanas — un
paramount regional, no pancaquetío.

## 4. El área de influencia real: ABC, Paraguaná, Guajira

Con la paramountcy acotada a escala regional, ¿cuál es esa escala? Tres piezas geográficas quedan
bien ancladas:

- **ABC (Aruba, Bonaire, Curazao)** — presencia caquetía atestiguada, con el caso de Curazao
  documentado en detalle, incluyendo préstamos léxicos caquetíos que sobreviven en el papiamento
  (Van Buurt 2014, ya en `fuentes_caquetios/`). Ya asumido por el elenco: Kadushi es "caquetío de
  Aruba", Watapana viaja regularmente ahí.
- **Paraguaná** — núcleo geográfico ya central del proyecto.
- **Guajira** — Oliver (1989, cap. 3, p. 189) es explícito: *"The Caquetío settlements were, in all
  probability, avant guarde posts that traded with the Wanebucán and Coanao... The Caquetío of the
  Guajira undoubtedly originated from Coastal Falcón."* Puestos de avanzada comercial —sal por oro y
  bienes de Valledupar y la Sierra Nevada— fundados desde la misma costa de Falcón que Coro. Confirma
  directamente la intuición de Miguel, con cita exacta.

## 5. Todariquiba: el asentamiento real que estamos reconstruyendo

La pieza que cierra el círculo. Oliver (1989, cap. 3, p. 251) narra que, tras el pacto de 1527,
*"Manaure agreed to ally himself with Ampíes... and to resettle near what is today Coro (a village
called Todariquiba)"* — y su hijo/sucesor Don Alexandre también residió ahí. El nombre recurre en la
carta de 1538 del obispo Rodrigo de Bastidas a Carlos V (junto a Guaibacoa, Cumarebo, Tomodore,
Caujarao, Zazárida, Capatárida) y en registros administrativos posteriores del período Welser (Ponce
y Vaccari 1977: 94, 179-80, 238-40, 451) — no es una mención aislada.

Su ubicación exacta sigue en debate: Oliver mismo dice que no se ha hallado un sitio arqueológico de
tamaño correspondiente en la periferia de Coro, y sospecha que quedó bajo la expansión urbana moderna
o más allá de las 4.5-6 km que sugieren las crónicas. Eso es una ventaja para la simulación, no un
problema: no hace falta fijar coordenadas que la propia arqueología no ha fijado.

**Todariquiba es, con la mejor evidencia disponible, el asentamiento real que "la Curiana" de la
simulación reconstruye.** Es casi con certeza la misma palabra que Miguel recordaba al principio de
este programa de investigación como "Arakiba" o "Arequiba" — dos intentos de recordar el mismo nombre
en dos momentos distintos.

## 6. La escala real: miles, no sesenta

Dos datos de la misma carta de Ballesteros (1550) fijan la magnitud que Miguel viene señalando desde
el inicio del programa:

> *"...los indios habían construido a través del río una represa que los indios llaman **buco**. Y
> frente a la represa hay un canal de dos leguas... Cada temporada de lluvias el canal se atasca... y
> se rompe dos o tres veces, de forma que se requerían **cuatro o cinco mil indios** para repararlo.
> En los días en que Coro y sus alrededores tenían **catorce o quince mil indios**, en tres o cuatro
> días el canal quedaba arreglado..."* (Ballesteros [1550] en Bécker 1950 [1]: 688, vía Oliver 1989,
> cap. 3, pp. 262-263)

Oliver interpreta: 4-5 mil trabajadores implican coordinación entre **más de 30 poblados** (asumiendo
150-200 personas por poblado de todas las edades). El *buco* que ya es central en el canon —Corie-ko,
Buco-ko— no era una acequia de aldea: era infraestructura regional, y su mantenimiento movilizaba a un
tercio de toda la población del área. El núcleo de 60 agentes de la simulación es, y siempre fue
narrativamente, **una fracción pequeña** de la población real de Todariquiba y su región — consistente
con la idea ya establecida de que los linajes son "unidades de expansión" del elenco (parentesco-025),
no con que 60 personas agoten el asentamiento.

La misma carta documenta el colapso: para 1550 —23 años después del pacto de 1527— solo quedaban
*"hasta cuatrocientos indios"* en seis poblados alrededor de Coro. De 14-15 mil a 400 en una
generación. Dato que no es material para la Curiana precontacto que la simulación modela hoy, pero
que fija la magnitud real de lo que el propio Zavala (2015: 60) llama *"el éxodo que dirigía el
Manaure"*.

## 7. Vespucio, San Bartolomé, y el nombre de Venezuela

Pieza adicional, confirmada solo en parte. El "Puerto de San Bartolomé" que describió Américo
Vespucio hacia 1500 —un poblado de viviendas sobre estacas (palafitos) que le recordó a Venecia y dio
origen al nombre "Venezuela"— ha sido identificado por el historiador Demetrio Ramos Pérez (1976: 88)
como ubicado **en el Golfete de Coro**, no en el área del Lago de Maracaibo, donde suele situarse la
leyenda (Oliver 1989, cap. 3, p. 249). Si se confirma, el propio nombre del país se ancla a un poblado
del Golfete.

Lo que esta sesión **no pudo confirmar** es el número de "40 casas" que Miguel recordaba para ese
poblado: la única cifra de esa magnitud encontrada en Oliver (40-50 individuos) corresponde a la
capacidad de una maloca en **Curazao**, un dato distinto. Oliver además sugiere (cap. 3, ~p. 265) que
las viviendas sobre estacas podrían pertenecer a una comunidad pesquera especializada, de relación aún
no establecida con los asentamientos caquetíos de tierra adentro como Todariquiba — es decir, ni
siquiera está claro que San Bartolomé y Todariquiba sean, o dependan, del mismo poblado. Queda
marcado como abierto en el corpus (`geografia_politica.yaml`, `nota_abierta`).

## 8. El nombre "Curiana": una corrección pendiente de decisión

Zavala (2015), en su propia nota al pie (4), define: *"Curiana: territorio donde estaban asentados
los caquetíos."* No es el nombre de un asentamiento puntual — es un nombre **territorial**. Esto es
más fiel a la fuente que el uso que todo el proyecto le ha dado hasta ahora: `curiana_agents.py`,
`curiana_state.py` y el sitio público usan "la Curiana" para el asentamiento específico de los 60
agentes.

Esta sesión NO resuelve la tensión — la deja explícita para que Miguel decida, con tres caminos
razonables:

1. **Dejar "la Curiana" como está** (el asentamiento) y dar un nombre de trabajo aparte, marcado
   como no atestiguado, a la confederación/territorio completo.
2. **Corregir hacia la fuente**: "Curiana" pasa a nombrar el territorio; el asentamiento de los 60
   agentes recibe nombre propio — candidato natural, **Todariquiba** (§5). Más fiel a Zavala, pero
   toca referencias en decenas de archivos Python y en todo el sitio público.
3. **Aceptar la ambigüedad ya asentada** en meses de contenido y solo documentar la imprecisión aquí,
   sin tocar nada existente.

## 9. Decisiones de diseño para la simulación

1. **Vocabulario de rango**: `apopo`, `diao` (corregido) y `boratio` ya se incorporaron a
   `curiana_lexicon.py` como `caquetío-atestiguado`, con cita. Corie-ko, Chiriguare y Paugis-sha/
   Sha-corie son, propiamente, *apopos* de sus linajes — no "diaos".
2. **Modelo de sucesión de tres puertas** (elegibilidad matrilineal + ratificación política +
   legitimación espiritual como *boratio*) — ver `parentesco.yaml#parentesco-038`. Heredar la
   posición de Manaure no es un solo evento genealógico.
3. **Pluralidad de candidatos** como corrección recomendada a `genealogia.yaml` (un solo sobrino,
   Waimo-ko, es una simplificación) — ver `parentesco.yaml#parentesco-039`. No ejecutada todavía:
   el linaje Kaira ya anota esta dirección de crecimiento en su `capacidad_de_expansion`.
4. **Escala real**: los 60 agentes representan una fracción de una población de miles (14-15 mil en
   el pico, según Ballesteros 1550) distribuida en 30+ poblados — refuerza, con cifra exacta, que los
   linajes son las unidades de expansión futuras del elenco (parentesco-025), no que 60 agotan
   Todariquiba.
5. **Nombre "Curiana"**: decisión abierta y explícitamente sin resolver (§8) — no tomar ninguna de
   las tres vías sin que Miguel elija.
6. **San Bartolomé/Venezuela**: dato interesante pero con una pieza sin verificar (el número de
   casas) y una relación con Todariquiba todavía no establecida en la fuente — no usar como hecho
   cerrado hasta una verificación adicional.

## Fuentes citadas

- Zavala Reyes, Miguel Enrique (2015). "Palabras vivas de una lengua muerta: legado arawak-caquetío."
  *Boletín Antropológico*, año 33, n.º 89 (enero-junio), pp. 58-76. Universidad de Los Andes, Mérida.
  (`fuentes_caquetios/Palabras Vivas de una Lengua Muerta.pdf`)
- Oliver, José R. (1989). *The Archaeological, Linguistic and Ethnohistorical Evidence for the
  Expansion of Arawakan into Northwestern Venezuela.* Cap. 3, "XVI Century Ethnic Boundaries &
  Caquetío Polities." (`fuentes_caquetios/Chapter 3 Ethnohistory.DOC-comprimido.pdf`)
- Arcaya, Pedro Manuel (1920). *Historia del Estado Falcón*, citado vía Zavala Reyes 2015.
- Van Buurt, Gerard (2014). "Caquetío Indians on Curaçao during colonial times and Caquetío words in
  the Papiamentu language." (`VanBuurt_2014_CaquetioWords_Papiamentu.txt`)
- Ballesteros [1550], carta al Rey, en Bécker (1950), citado vía Oliver 1989.
- Ramos Pérez, Demetrio (1976, 1978, 1981), citado vía Zavala Reyes 2015 y Oliver 1989.
