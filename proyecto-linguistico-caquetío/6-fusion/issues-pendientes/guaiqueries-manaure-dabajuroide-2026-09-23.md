# El asiento de Manaure, los guaiqueríes y la cronología dabajuroide (cc.5)

**Labels propuestos:** `decision`, `mundo`, `fuentes`
**Datos, con cita, página, época y etiqueta:** `6-fusion/guaiqueries_manaure_dabajuroide_2026-09-23.yaml`
**Lo que se mide:** `python 6-fusion/scripts/medir_cronologia_dabajuroide.py`

Campaña corta del 2026-09-23, por la decisión cc.5: *«donde se sentaba Manaure
donde ubicar los guaqueríes […] la cronología de [dab]ajuroide […] Ferman
identificó […] que había un poblado de guayquerías con caquetíos»*. Son tres
preguntas y cada una tiene su veredicto. Nada se ha aplicado.

Cierra tres opciones de la lista consolidada (#222, `ya_decididas`): **#203 M8
D1** (la cronología), **#207 M7 D-d con #213 M1 §1.5** (dónde vivía Manaure) y
**#214 HSAI (d)** (los guaycaríes del elenco). También toca dp.2.03 y dp.2.04
(`etnias.yaml`) y el «Paragrachoa» de los vistos de paso.

---

## 0. Lo que resultó falso al medirlo

1. **«El propio texto dice que los expedicionarios "supusieron eran
   Guayqueríes"»** (`etnias.yaml`, etnia-002). Federmann no supone nada:
   nombra a los guaycaríes sin dudarlo (1916 p. 84; Klüpfel p. 55). El
   «supusieron» venía de Brito Figueroa, por donde llegó la cita. Lo que es
   conjetura es otra cosa: que esos guaycaríes sean los guaiqueríes de
   Margarita.
2. **«El cacique Charaima de la Isla de Margarita, el abuelo del guayquerí
   Francisco Fajardo»** (toponimo-082, por Esteves p. 35). Según Oviedo y Baños
   (p. 168, visto en imagen), Charayma era cacique del **valle de Maya, en la
   provincia de Caracas**, y **bisabuelo** de Fajardo. Con eso se corta el
   único hilo que unía un topónimo de Paraguaná con los guaiqueríes.
3. **«La cerámica dabajuroide está correlacionada con una única unidad étnica:
   el caquetío»** (ecologia-013). Oliver (p. 424, visto en imagen) sólo
   correlaciona las sub-tradiciones Dabajurana, Bachaquerana y Tierrana con las
   polities caquetías. La tradición dabajuroide incluye además la Campomana,
   que está en Cumaná, Barcelona y **Margarita** (p. 427).
4. **Un «poblado de guaiqueríes con caquetíos».** Federmann no habla de un
   poblado mixto. El alemán dice que las dos naciones viven *«vnthereinander
   gemischt»* (mezcladas en el territorio), pero *«iede in sondern Pueblos»*
   (cada una en sus propios pueblos). Lo que comparten es una pesquería
   guaycarí de pocas casas que sirve de mercado. Y esto pasa en los **llanos**,
   junto al Cojedes.

## 1. Dónde se sentaba Manaure

**Veredicto.** Ninguna fuente dice dónde tenía su asiento antes de 1527, y
ninguna lo pone en Paraguaná.

- **c. 1526, Ampíes**, que no había estado allí: el gran cacique *«está diez
  leguas la tierra adentro en la provincia de Coro»* (Fernández Duro t. II
  p. 212). Esto no es ni la costa ni la península.
- **1527, Oliver:** el pacto con Ampíes lo **reasienta** junto a Coro, en
  Todariquiba (DOC p. 251). Es una lectura historiográfica, sin el documento
  que la respalde.
- **1531, Federmann:** Coro es *«la tierra del cacique Manuaury»*.
- **1538, Bastidas:** Todariquiba es el pueblo de **Don Alexandre**, a
  *«dos leguas»* de Coro (Velasco p. 33). En otra carta rectifica a una legua
  (González Batista vía M7).
- **1545, Cey:** Manaure vivía en el pueblo de Coro, en una casa grandísima.
- **Oliver, como corazonada suya:** la sede estaba en Caçicure / Pueblo Viejo,
  cerca de Mitare (DOC pp. 265-266). Choca con el «tierra adentro» de Ampíes.
- **El «gran señor de Paraguaná»** sale de Salas, a través de Antolínez y de
  Morón: es historiografía del s. XX con tres eslabones.

El canon de la era 2 le pone casa en **Moruy, al pie del Capubana**. Es una
decisión creativa (2026-09-14) sin fuente. No choca con ningún dato del s. XV,
porque no existe ninguno. Lo que sí está mal es que `nodo-001` y
`geografia_politica-003` den por **atestiguada** la residencia de Manaure en
Todariquiba: es reconstruida.

- **A.** Declarar y no cambiar nada. En nodo-001 y geografia_politica-003, la
  residencia de Manaure pasa a `reconstruido`, con estas precisiones: 1527-1531,
  Don Alexandre en 1538, a «una o dos leguas», y Coro según Cey. En el elenco,
  la casa de Moruy lleva `canon-simulacion` y `deuda: sin-procedencia`. El
  motor no se toca.
- **B.** Hacer A y además sacar la casa de Manaure de Paraguaná (sería la
  opción c de P1). Obliga a rehacer elenco, escena y día 1.
- **C.** Llevar su asiento a Caçicure siguiendo a Oliver. Es una corazonada
  suya.
- **D.** No tocar nada.

**Recomiendo A.**

## 2. Los guaiqueríes

**Veredicto.** Hay **dos** grupos que llevan el mismo nombre, y ninguno está
documentado en la costa de Falcón.

**El pasaje de Federmann** (enero-febrero de 1531, junto al río Coaheri, que es
el Cojedes, en tierra de Itabana; lo he visto en imagen en la edición de 1916 y
en la de 1557):

> «Allí hacen mercado con los Caquetíos, que cambian frutas y otros víveres por
> pescado, porque es la pesca su única industria y hanse adueñado del río. Viven
> estas dos naciones en paz en el mismo territorio porque se necesitan
> mutuamente, pero cada una habita aldeas distintas.» — 1916 pp. 89-90 = 1557
> [77]-[78]

Y en la p. 94 = [83]: *«zwen Indios Guaycaries … die auch der Caquetios sprach
kundten, dann dise zwo Nation vndereinander … wonen»*, es decir, dos guaycaríes
que sabían la lengua de los caquetíos porque las dos naciones viven mezcladas.
Hay además una pesquería guaycarí de pocas casas a la que acude mucha gente a
comprar pescado (p. 95), y una alianza de guerra entre el cacique guaycarí y un
cacique caquetío (p. 100). El alemán dice más que la traducción de 1916: los
caquetíos viven *a los dos lados* del río, y el territorio está *mezclado*.
Todo esto pertenece a la polity de los **llanos** (regla 4).

**Los guaiqueríes de Margarita.** Vivían en Cumaná, Margarita, Coche, Cubagua
y parte de Trinidad; eran pescadores de perlas y canoeros (HSAI pp. 399 y 406).
Desde 1550 aparecen como aliados de Fajardo, Losada y Juan de Salas (Oviedo y
Baños pp. 177, 222, 280, 312). Su élite estaba emparentada con los caciques de
la costa de **Caracas** (p. 168).

**¿Son el mismo pueblo?** Arcaya no lo sabe (nota de la p. 89). Oliver cree
probable que estén emparentados con *«the Carib-speaking Guayquerí of
Margarita»* (DOC p. 281). Para Kirchhoff, los de Federmann son guamos del oeste
y «Guaikeri» era un nombre que se daba a los pueblos pescadores en general
(HSAI p. 464). No los fundo en uno.

**Lengua.** En el repo no hay ninguna palabra guaiquerí.
- **Caribe:** Oliver, con McCorkle 1952; el área que describe Kirchhoff en la
  p. 481; Zavala vía Molina. Castellanos (p. 24) cuenta que unos caribes de las
  islas *«bien entienden»* la «lengua guayqueri».
- **Warao:** la nota de Arcaya, y Antolínez con signos de interrogación.
- **Arahuaca:** ninguna fuente del repo lo propone.

La etiqueta que propongo es `desconocida`.

**Trampa: Paraguachoa.** Hoy se cita como el nombre guaiquerí de Margarita.
Pero en Ampíes, en Oviedo (t. IV p. 531) y en Oliver (DOC pp. 261-262) es un
lugar del **Falcón oriental**, y es el límite este de la costa caquetía. Ni
Margarita ni Paraguaná.

**La era 1 y la era 2.** Los guaycaríes de la era 1, en la orilla de la Curiana
cambiando pescado por sal, son `canon-simulación` sin fuente en la costa. Lo
documentado es pescado a cambio de *frutas y víveres*, y en los llanos. La
era 2 ya los dejó fuera, y las fuentes le dan la razón: no hay guaiqueríes en
Paraguaná en ninguna época. **No hay que reescribir nada en los eventos**
(`REESCRITURAS_ERA2`, `MARCOS_FUERA_ERA2` y la frase del Director están bien).

- **A.** Corregir etnia-002 con la fuente primaria: la 1916 p. 90 y el alemán,
  quitando el «supusieron». El contacto en los llanos queda `atestiguado`; la
  identidad con Margarita y la familia lingüística quedan como hipótesis
  (`desconocida`). El lugar es el Cojedes, 1531.
- **B.** Hacer A y abrir además una ficha «guaiquerí de Margarita», que sería el
  vecino de la esfera que no toca ninguna polity. Para eso `compilar_etnias.py`
  necesita un valor de polity nuevo, `ninguna` o `fuera`.
- **C.** Hacer A y B y llevarlos también al motor. No lo recomiendo: no hay
  ningún contacto documentado con la costa occidental.
- **D.** No tocar `etnias.yaml`.
- **E.** Por separado de lo anterior: corregir toponimo-082 (Charayma, valle
  de Maya) con Oviedo y Baños p. 168.

**Recomiendo A + B + E**, en la misma tanda que dp.2.03 (el campo `epoca`).

## 3. La cronología dabajuroide

| Esquema | Complejo | Fechas d.C. | Región | Fuente |
|---|---|---|---|---|
| Oliver 1989 | Túcua | 800 – 1100/1200 | costa de Falcón, Paraguaná, ABC | cap. 4 p. 422 |
| Oliver 1989 | Urumaco (Temprano y Tardío) | 1100/1200 – 1400/1450 | ídem | p. 422 |
| Oliver 1989 | Los Médanos (A prehistórico, B histórico) | 1350 – 1600/1650 | ídem | p. 422 |
| Oliver 1989 | Supidebo/Antúnez (Bachaquerana) | 1300 – 1450 | Falcón occidental (Borojó) | p. 423 |
| Oliver 1989 | Bachaquero · Las Minas | 1300–1600 · ca. 1300–1500 | Maracaibo | p. 423 |
| Oliver 1989 | Playa Guacuco · Punta Arenas · Guaraguao (Campomana) | ca. 1000 – 1500 | costa oriental, **Margarita** | pp. 423, 427 |
| Oliver 1989 | Tierra de los Indios · San Pablo (Tierroide) | ca. 1000 – poscontacto | Barquisimeto, Yaracuy | p. 423 |
| Casale 2024 | Túcua | 850 – 1200 | Aruba | Tabla 1, p. 3 |
| Casale 2024 | Urumaco Temprano | 1200 – 1350 | Aruba | p. 3 (el texto dice 950-1250 para Tanki Flip) |
| Casale 2024 | Urumaco Tardío | 1350 – 1500 | Aruba | p. 3 |
| Casale 2024 | Los Médanos A · B | 1400–1450 · 1450–1515 | Aruba | p. 3 |
| Arvelo y López 2004 | Ocupación Dabajuro | 800 – 1492 | El Carrizal | vía Urbina 2007 p. 65 |

Qué se mide con el script:

- De las dataciones de la Tabla 15, 12 de 23 tocan la ventana. En Paraguaná
  sólo lo hacen las de Santa Ana: el Urumaco Tardío, con la fecha terminal
  cal. 1415 (IVIC-14, obtenida por Zucchi), una cerámica que todavía era
  *«lavishly decorated»*.
- El Los Médanos A de Cayerúa y Moruy es posible, pero Oliver no lo asegura
  (pp. 471-472) y no tiene ninguna fecha.
- Hasta 1450 los dos esquemas coinciden. Entre 1450 y 1500 divergen: según
  Oliver sólo queda Los Médanos; según Casale siguen el Urumaco Tardío y Los
  Médanos B.

Lo que no he podido consultar: **Rouse y Cruxent 1963** (en el repo es un
archivo de 0 bytes y en archive.org sólo está en préstamo controlado),
**Cruxent y Rouse 1958** (sólo lo conozco a través de Oliver; HathiTrust
devolvió 403 y no sé si está en vista completa), y **Arvelo** y **Zucchi**, que
sólo aparecen citados por otros.

- **A.** Seguir a Oliver 1989.
- **B.** Seguir a Casale 2024.
- **C.** No fijar ninguna de las dos: en la ventana conviven el Urumaco Tardío
  y Los Médanos A.
- **C regional.** C, pero dicho lugar por lugar: en Paraguaná, Urumaco Tardío
  fechado (Santa Ana) y Los Médanos A posible (Cayerúa, Moruy); en Coro, los
  dos (FAL-100 y FAL-101); en las islas, según Casale.

**Recomiendo C regional.** Aparte de esa decisión, que no depende de la letra
que se elija: ecologia-013 debería citar a Oliver pp. 422-424 en vez del Atlas
web, y decir «dabajurana» donde hoy dice que dabajuroide equivale a caquetío.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
