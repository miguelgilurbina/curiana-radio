# El poporo no es caquetío, `coro` no es 'viento' y las voces de Zayas, decididas por la fuente

**Para que Miguel decida lo que queda.** Las tres decisiones son suyas
(`6-fusion/decisiones_cierre_2026-09-23.yaml` §cc.3, §cc.6, §cc.7). Aquí van
la cita y la página que faltaban, y las pocas elecciones que abre. Todo el
detalle, con los textos verbatim, está en
`6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml`.

---

## Lo que resultó falso al medirlo

1. **«El poporo es el arma caquetía atestiguada»** (nota de `macana`; `poporo`
   caquetío-atestiguado). Alvarado 1921 p. 255 lo afirma y cita tres páginas
   de Castellanos. Ninguna de las tres tiene un caquetío: la de las Elegías
   (BAE p. 202) es el guanebucán Boronata en el río de la Hacha, y las dos del
   *Nuevo Reino* (la «parte 4», bajada hoy: t. I pp. 46 y 65) son los muiscas.
   En todas las fuentes que lo definen, el poporo es el **calabacito de la
   cal** para mascar hayo.
2. **«Coro = viento es de Oviedo»**. Es de Castellanos (BAE p. 185), y él no
   la da como voz indígena: el nombre lo pusieron los españoles tomándolo del
   río, y «Coro viento / Quiere decir en lengua generosa», el latín
   *cōrus/caurus*, que el castellano de 1582 tenía como el viento del
   noroeste. Ni Oviedo y Valdés ni Oviedo y Baños traen la etimología.
3. **«`bagua` 'mar' es del glosario de la Academia»** (#220). Está en el
   **cuerpo** de Oviedo, t. I p. 436: «Llaman los indios de aquesta Isla
   Española á la mar *bagua*». El OCR se come la cursiva.
4. **«`anua` no está en Zayas»**. `anua` no existe en ninguna parte: Goeje
   p. 14 escribe ***aura*** (verificado en imagen), y la transcripción del repo
   la leyó mal.
5. **«`cohiba` … Brinton 1871»** (lexicón). Brinton escribe *Cohóba*. La
   forma `cohiba`, y la glosa 'la planta del tabaco', salen del glosario del
   editor de Oviedo (1855) y de Pichardo (1862). Ningún cronista las da.

## A. `poporo` (cc.3)

- **A (recomendada)**: sale del habla. Pasa a `FUERA_DEL_HABLA` con
  `fuente: español-colonial`, como caraota y kukuisa en D10, con la glosa
  'calabacito de la cal para mascar hayo' y la historia en `notas`.
- **B**: sale del habla con la capa intacta (caquetío-atestiguado). No se
  recomienda: la etiqueta es falsa, y archivarla sin corregirla la conserva.
- **C**: se queda degradada a caquetío-hipotético. No hay dato caquetío de la
  voz.

Y en cualquier caso, la nota de **`macana`** se corrige (texto en el YAML
§poporo.cambio_propuesto.macana). El caquetío no tiene voz atestiguada para
el garrote. Lo que sí hay es la **cosa**: Castellanos p. 200, el cacique
Uriorebuí de un pueblo caquetío del **interior** (1530) pelea «con dos
terribles golpes de macana». Es la palabra del cronista.

## B. `coro` (cc.6)

Sin opciones: la decisión está tomada. Sale 'viento' de `lectura_en_disputa`
(compiten dos, espina y avispa/lagartija) y queda en `notas` como
DESCARTADA, con el porqué (texto en el YAML §coro). En `toponimo-111`, el
veredicto de la lectura de Arcaya deja de listar «viento» entre las que
compiten; eso se edita en `lexicon_toponimos.py`, no en el YAML generado.

## C. Las voces de Zayas (cc.7)

| Voz | Etiqueta | Por qué (fuente primaria) | Lexicón |
|---|---|---|---|
| `manati` | **taíno** | Las Casas, Apologética p. 27: «los que llamaban los indios manatíes, la penúltima sílaba luenga». Oviedo t. I p. 434 lo contradice con una etimología castellana (las manos), sin dar el nombre indio | sólo la nota |
| `tabako` | **taíno** | el rollo encendido (Las Casas, Apologética p. 181; Historia I cap. XLVI), el cañuto y la ahumada (Oviedo t. I pp. 130-131, 143); y Oviedo t. IV p. 96: «en lengua desta isla de Hayti ó Española se diçe *tabaco*» | glosa ampliada con el rollo |
| `cohiba` | **del editor** (1855) y del XIX | la voz de los cronistas es `cohoba`: el polvo y el rito (Pané cap. XI; Las Casas pp. 445-446), la ahumada (Oviedo p. 143) y un árbol de vainas (Oviedo p. 347) | ver abajo |
| `bagua` | **taíno** | Oviedo t. I p. 436, en el cuerpo | nada obligado; sube en la lista maestra |
| `anaki` | **no atestiguada** | sólo en la lista de Rafinesque («eyerí», Zayas t. I p. 39) y en Adam 1879 p. 303; su pariente es el kalinago femenino *akani* | nada |
| `anua` | **no existe** (es `aura`, sin cronista) | Goeje p. 14 en imagen | nada; corregir la transcripción de Goeje |
| `manaya` | **no atestiguada** | sólo en la traducción italiana de Pané (Bachiller p. 192: *manaia*); *mannaia* es 'hacha' en italiano | nada; baja a clase iii en la lista |

**`cohiba`, tres opciones:**

- **A (recomendada)**: `cohiba` 'tabaco' pasa a `FUERA_DEL_HABLA` con su
  historia y entra **`cohoba`**, taíno, 'polvo que se aspira por la nariz en
  el rito, y el rito mismo', en `SE_QUEDA_CON_SU_GRAFIA` como hoy `cohiba`.
  Aplica «la atestiguada manda».
- **B**: se queda la clave `cohiba` con la glosa corregida. Es más barata,
  pero enseña una forma que ningún cronista escribió.
- **C**: sólo se corrige la nota. No se recomienda: sigue enseñando 'tabaco'.

Ningún cronista del repo da el nombre taíno de la **planta**: Las Casas y
Oviedo dicen «yerba», «hierva».

## Visto de paso (para campañas cortas, no de esta parcela)

1. 🔴 **`baperon` y `raporon` son caquetío-ATESTIGUADO en
   `lexicon_zavala.py`**, que el motor importa (Zavala 2015 #27 y #220,
   sigla HB). En el cuerpo de Oviedo (t. II pp. 286 y 294, verificado en
   imagen) es el calabazo de la cal de los **pemenos** del sur de la laguna de
   Maracaibo. La etiqueta «(Lengua de Venezuela)» es del glosario del editor
   (t. IV p. 594). Es la trampa de `datihao` otra vez: el mismo patrón que
   sacó a `datihao` del caquetío.
2. **El PDF de Brinton 1871 está commiteado vacío** en `main` y en esta rama
   (blob `e69de29`, 0 bytes). #220 lo repone (2.179.167 bytes).
3. **La transcripción de Goeje** (`6-fusion/taino_goeje_1939.yaml`) tiene
   `anua` por `aura`, y la **lista maestra** hereda el error. La misma lista
   debería subir `bakua` a clase i (Oviedo), bajar `manaia` a iii y agrupar
   `kohiba` como `kohoba`.
4. **#220** (`taino_zayas_1931.yaml` §Bagua) tiene que corregir su `lectura`
   («la voz sigue sin cronista») y su `efecto_en_la_lista`.
5. **`6-fusion/medina_colina_dictado.yaml` §poporo** (p. 230) dio veredicto A
   «porque la palabra ya es caquetío-atestiguada». Sin eso, 'chichón' es
   castellano venezolano general.
6. `lexicon_alvarado.py` y `minar_alvarado_glosario.py` dan el poporo como
   «confirma → caquetío-atestiguado JUSTIFICADO». Es lo que Alvarado afirma,
   no lo que sus referencias sostienen. Si se regeneran, que lo digan.

## Lo que no se hizo

- No se leyó la *Historia del Nuevo Reino* entera: sólo las páginas de
  Alvarado y un barrido de `popor-`, `caqu-`, `guanebuc-` y `macana` en los
  dos tomos.
- La edición crítica de Pané (Arrom 1974) y el t. I de Hernando Colón, que
  decidirían `manaya`, no están en el repo.
- «Yocahu Vagua Maorocoti» de Las Casas, que llevaría `bagua` a un segundo
  cronista, se conoce por Bachiller y Coll y Toste; no se buscó en la
  Apologética.
- No se re-midió el cruce taíno-caquetío con `bagua` en clase i.
