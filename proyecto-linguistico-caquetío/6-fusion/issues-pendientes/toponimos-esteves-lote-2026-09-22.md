# La cola de Esteves, leída entera — y un Zavala que resulta ser Esteves

**Para que Miguel decida.** Tercera campaña de minería, parcela M6
(2026-09-22/23). Nada se ha aplicado al canon: esto propone. La propuesta,
nombre por nombre, está en `6-fusion/toponimos_esteves_lote_2026-09-22.yaml`
(sin cifras); los recuentos los escribe
`6-fusion/scripts/medir_lote_esteves_2026-09-22.py` en
`6-fusion/medicion_lote_esteves_2026-09-22.yaml` (`--check` dice si está al día).

---

## 0. Lo primero, porque cambia la regla de los niveles

La skill pone Judibana de ejemplo de nivel A: «judi + bana, Esteves y
Zavala». Pero el Zavala de `juri` es **#178 (E)**, y en Zavala p. 64 **E =
Juan Esteves**. Para un topónimo de Esteves, una voz del lexicón cuya única
cita es Zavala (E) no es una segunda fuente: es la misma, copiada
(minar-fuente §8).

Medido: de las voces que este lote usa y tienen cita de Zavala, **27 de 48**
sólo llevan la sigla E. En todo el lexicón, **43 de las 228** voces
caquetío-atestiguadas no tienen más sigla que E (39 si se quitan las que
nombran otra obra en la nota, que puede ser apoyo o no). Entre ellas hay
morfemas que el canon usa para subir niveles: `juri`, `cari`, `ebo`, `ure`,
`tuba`, `rao`, y el afijo `-uco/-uto` (REGLAS_ZAVALA lo cita como #268 (E)).

El lote aplica la regla así: **A** sólo si cada pieza está en otra fuente
(Zavala con otra sigla, Alvarado, Medina, van Buurt, Oliver, Arcaya, Oviedo).
Para B se respetó el precedente del propio canon —Buchuhaco y Abudure: una
pieza independiente más otra sólo de Esteves pero recurrente—. **No se
re-midieron los niveles que el canon ya tiene**: eso es la pregunta 1.

## 1. Qué se hizo

La cola entera de la Parte I (Paraguaná) se leyó en el cuerpo del libro: 83
entradas con glosa y 46 descartes, **82 de las 83 vistas en la imagen**, no en el
OCR. Por nivel propuesto: **A 14 · B 14 · C 55 · descartado 46**. Las A son,
casi todas, fitónimos y zoónimos que otra fuente registra con la misma cosa
(Chuchube, Saruro, Chaure, Isiro, Laguarí, Yacure, Urupagua, Cayude…) y dos
compuestos que cierran enteros: **Buchaquiva** (buche + kiba) y **Guachaco**
(guache + aco).

Los ids no se asignan: hay otras parcelas proponiendo topónimos a la vez.

## 2. Lo que resultó falso al medirlo

- **El topónimo «perdido» entre Tumatey y Tutubacoa no existe.** La p. 65 es
  una foto a página entera; la «entrada sin cabecera» de la p. 66 es la cola
  de TUMATEY. El barrido automático conjeturó «TUCACAS o similar».
- **Carirubana tiene glosa de fuente**, en la p. 28. El canon la trata como
  etimología popular y le da el veredicto de «corroboración independiente de
  bana». No lo es: la divulgación copia a Esteves.
- **Acaboa y Aguaque sí tienen etimología** (pp. 12 y 14), contra la razón del
  grupo de descartes en el que están.
- **cumaragua en Arcaya es «viruela», no «ciruela»** (p. 75, vista en imagen).
  La nota de `kumarawa` lo cita mal. Una voz para la viruela es dato de contacto
  (regla 3).
- **La cita de Chunaure en `tura_la_tesis_de_miguel.yaml` no está en la p. 37**:
  Esteves dice que Chunaure es un apellido y glosa aparte naure 'jojoto'. El
  eslabón tura ~ chunaure se sostiene por otras vías, no por esa cita.
- **La cola del índice estaba desfasada** (tres nombres ya en el canon) y
  tres cabeceras impresas no coinciden con el índice (Buchaquiva,
  Duracuaco, Suriquiba). Corregido en `toponimos_esteves_indice.yaml`.
- **`barrer_mapa.py --lote` sigue diciendo que Paraguaná tiene 8 nombres
  «nuevos»**: los ocho están en el canon desde el lote 7 con la forma de
  Esteves. Y dos aproximados («Cerro Capuana», «Cuabana») caen ahora en
  `capana`, de la Parte II, en vez de en Capuhana y Coabana.

## 3. Lo que el cruce con el mapa vivo resuelve

De los nombres del lote, 50 están tal cual en OSM 2026, 12 sólo de forma
aproximada y 67 no aparecen (un cero en OSM no es un cero en el terreno).
Cuatro descartados del canon que entraron por el mapa «sin fuente» tienen
candidato en Esteves:

| canon | mapa vivo | Esteves | por qué |
|---|---|---|---|
| toponimo-132 | Cumairebo | Curaidebo, p. 35 | justo entre Pueblo Nuevo y El Vínculo, donde lo pone Esteves; r~m |
| toponimo-138 | La Miraba | Niraba, p. 54 | en el municipio Moruy; n~m |
| toponimo-135 | Tabe | Jabe o San José de Tarbes, p. 44 | a unos dos km de Jadacaquiva |
| toponimo-176 | Coduto (dos sitios) | Coduto, p. 31 | caduto ~ Coduto; están los dos lugares de Esteves |

Ninguna permutación de éstas está documentada en la skill: son para revisar.

## 4. Fauna y flora

26 animales en la clave `fauna:` (10 con especie que la fuente permite, 5 con
sonido) y 36 plantas en `flora:`, con el mismo esquema. Lo que más vale para
los agentes de fauna:

- **guacoa**: Alvarado p. 143 dice que las formas del nombre «imitan… el canto
  de esta ave». El nombre es la onomatopeya.
- **dara** (alcaraván): «ave vocinglera», y la tradición que Esteves rechaza en
  Caradacagua la hace «voz onomatopéyica de la estridente dara».
- **chaure**: Alvarado cita un verso sobre cómo «pitan» los chaures de noche, y
  la locución «cantó un chaure» para quien anuncia desgracia.
- **curumu 'zamuro'** (Cumujacoa) tiene cognado caribe: Jahn p. 348, motilón
  «kurumáscho». Puede ser préstamo de la esfera.
- **guache**: Esteves dice zorro; Alvarado dice coatí y lo saca del caribe.

## 5. Las preguntas

**Pregunta 1 — ¿cuenta Zavala (E) como segunda fuente?**

- **A.** No cuenta. Se aplica al lote tal como está y **se re-mide el canon**
  (Judibana y los demás que suben con voces sólo-E) en una tanda aparte.
- **B.** No cuenta, pero sólo de aquí en adelante: el canon existente no se toca.
- **C.** Cuenta, como hasta ahora. Entonces la mitad de las C de este lote
  suben a B y las B a A, y el script lo mide con la regla vieja.

**Pregunta 2 — cómo entra el lote.**

- **A.** Por tandas: primero las 28 A y B más las correcciones del §2 que tocan
  entradas del canon; después las C; después los descartes.
- **B.** Todo de una vez.
- **C.** Sólo las correcciones; el lote se queda en 6-fusion/.

**Pregunta 3 — las cuatro identificaciones con el mapa vivo:** A) cada una
como lectura `hipotesis` en su entrada del canon, sin cambiar nada más; B)
fusionar las que Miguel reconozca sobre el terreno; C) dejarlas en la propuesta.

**Pregunta 4 — el mapa:** que el canon guarde la forma viva con su coordenada
en un campo propio y que `barrer_mapa.py` lo lea (cambio de `curiana_sim/`), o
dejar el informe del mapa como está y leerlo con esta advertencia.

## 6. Mi recomendación

**1-A y 2-A.** La regla (E) es la que decide los niveles, y aplicarla sólo a
lo nuevo haría que dos topónimos idénticos tuvieran niveles distintos según el
mes en que entraron. La primera tanda serían las A y B, que son las que el
motor puede usar, más las correcciones de Carirubana, Acaboa, Aguaque, curarí
y la cita de `kumarawa`. Para la 3, **A**: lecturas `hipotesis` no rompen nada
y dejan las cuatro a la vista. Para la 4, el campo propio: sin él, el informe
del mapa seguirá anunciando como nuevos nombres que ya están.

## 7. Lo que queda sin hacer

- **La Parte II (Falcón)**: 387 entradas ya parseadas en
  `esteves_parte2_falcon.yaml`; sólo las que llegaron por el dictado están en
  el canon. No se tocó.
- **Oboque**: Esteves cita a Alvarado y el texto de Alvarado del repo da cero.
  Hay que verlo en la imagen de Alvarado.
- **Juroguagua**: Esteves remite a Jahn para un homónimo guajiro; en el texto
  de Jahn del repo da cero con cuatro patrones.
- **Tres letras de Sacuragua** («[S…]uragua», p. 58) no se leen ni a 400 dpi.
- **La cola nueva que traen otras parcelas**: Sarasaragua (Castellanos, pueblo
  caquetío de la ruta de Federmann, no de Paraguaná), Norupara (cero en el
  texto de Castellanos del repo), la Coriana de La Ramada (PR #207, toca a
  toponimo-111) y Miraca en Federmann 1530 (PR #210, toca a toponimo-095). En
  la propuesta, §cola_nueva.

## 8. Lo que vi de paso

- **La re-medición del canon con la regla (E)** (pregunta 1-A) merece campaña
  propia: es un script corto sobre las notas del lexicón y los `morfemas` de
  cada entrada.
- **Dos «palomas» que comen peces** (tauta y tigüí) en albuferas: no son
  palomas. Para los agentes de aves.
- **`baba`** 'caño' (Esteves, Babahuro) choca con `baba` 'padre' del lexicón
  (reconstruido): homógrafos a declarar si entra.
- **Pipiacoa** lleva un documento de **1596**, la fecha más antigua del lote
  después del Cocodito de 1590.
