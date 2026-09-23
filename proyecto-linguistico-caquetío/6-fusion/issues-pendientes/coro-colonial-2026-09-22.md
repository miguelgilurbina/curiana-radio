# La Coro colonial en Castellanos y González Batista — y lo que no se sostuvo

**Para que Miguel decida.** Tercera campaña de minería, parcela M7
(2026-09-22). Nada se ha aplicado. Datos, versos y páginas en
`6-fusion/coro_colonial_castellanos_brito_gonzalez_2026-09-22.yaml`; la
página de cada verso de Castellanos la calcula
`6-fusion/scripts/castellanos_pagina.py`, que se comprueba solo.

---

## 0. Lo que resultó falso al medirlo

1. **La paginación de la ficha de Castellanos.** Colgaba de la cabecera
   «185» de la línea 47693, que es un 183 mal leído. Las citas del canon que
   dicen «p. 185» (once ciudades, Coro = viento, doña Juana) aciertan de
   casualidad; las islas de los Gigantes son la p. 183.
2. **«Las partes III-IV no están».** La III está entera en el archivo.
3. **`poporo` caquetío con apoyo de Castellanos.** El pasaje al que remite
   Alvarado es el de Boronata, «indio guanebucán», en el río de la Hacha
   (p. 202). En las otras apariciones del archivo, el poporo es el calabacito
   de la cal que va con el hayo (Parte III). Castellanos no pone el poporo en
   manos de ningún caquetío.
4. **El Coriana de Castellanos no es Coro.** Es una aldea de La Ramada
   (costa guanebucana, entre la Sierra Nevada y el río de la Hacha), junto a
   «Paraguanil» (p. 264). De ahí sale el «Coria-na / Paragua-nil» de Oliver,
   y el canon (toponimo-111) lo sitúa en Punta Espada–Chichibacoa, a unos
   250 km.

## 1. Lo que Miguel recordaba (d21.15)

> «curiana era realmente Coriana y venía de espina porque Coro era un bosque
> tupido de cardones»

- **Coriana y 'espina'**: sí, de González Batista, *El nombre de Coro*, por
  las capturas del 2026-08-25. **Sin página**: la obra no se consigue por vía
  legítima (sólo Scribd).
- **«Bosque tupido de cardones»**: no está literal en lo transcrito del autor.
  Donde sí está la imagen, con fecha, es **Castellanos 1589, p. 185**: Coro
  «es tierra de fructíferos cardones / Con que gran parte della se embaraza».
  Es la misma página que González Batista cita en otra edición.
- **Nuevo a favor de la FORMA Coriana** (no de la etimología): 1526, «el
  cacique de Coro y Coriana»; 1646, Coro «que los Yndios diçen coriana»
  (Díez de la Calle, verificado en imagen); 1723, «provincia de Coriana».
  Todo vía González Batista 2002, que se descargó hoy.

## 2. Decisiones

### D-a · `poporo` (lexicón: caquetío-atestiguado, 'maza-porra, arma de combate ceremonial')

- **A.** Se queda atestiguado y se corrigen las `notas`: Alvarado dice
  «caquetíos y guajiros», pero el verso que cita es guanebucán; y se quita
  «ceremonial», que no tiene fuente.
- **B.** Se degrada a `caquetío-reconstruido` o pasa a voz de la esfera
  (guanebucán/Guajira) hasta que haya un caquetío con poporo.
- **C.** Antes de decidir, bajar la Parte IV (Historia del Nuevo Reino, ed.
  Paz y Meliá 1886, dominio público) y leer las pp. 46 y 65 del t. I, la otra
  referencia de Alvarado.

**Recomendación: C y luego A o B según lo que salga.** Mientras tanto,
quitar «ceremonial» cuesta poco.

### D-b · «Coro = viento» en la disputa de `coro`

El lexicón (d21.15) cuenta tres lecturas en disputa: 'espina', 'avispa o
lagartija' y 'viento'. La tercera no es indígena: Castellanos dice que el
nombre viene del **río**, «que siempre se llamó desta manera», y que «le viene
bien» porque *coro* es viento «en lengua generosa»; el castellano culto de
1582 ya tenía *coro* 'viento del noroeste', del latín (DICTER).

- **A.** Sacar 'viento' de `lectura_en_disputa` de `coro` y dejarla sólo como
  `etimologia-de-cronista` en toponimo-111, como ya está.
- **B.** Dejarla como está.

**Recomendación: A.**

### D-c · Coro, nombre de río

Ballesteros 1550 y Castellanos 1589, independientes, dicen que la ciudad
tomó el nombre del río Coro. ¿Se añade como `glosa-fuente` de referente a
toponimo-111 (el topónimo nombra primero un río)? **Recomendación: sí.**

### D-d · ¿Dónde vivía Manaure? (asentamientos.yaml nodo-001)

El canon dice que Manaure residió en Todariquiba, «el mejor candidato a la
Curiana». González Batista 2002 lo discute: Manaure estaba en el pueblo de
**Coro**, en una casa grande que luego fue iglesia (Cey, 1545); y la
tradición de 1680 le pone allí su «corte». Según él, Todariquiba fue un
refugio a una legua, en 1529.

- **A.** Declarar el conflicto en nodo-001, sin cambiar el candidato.
- **B.** Cambiar el candidato a Coro.
- **C.** No tocar nada.

**Recomendación: A.** Las dos lecturas son de documentos coloniales, y
ninguna es precontacto.

### D-e · Topónimos nuevos → cola de `campana-toponimos`

- **Sarasaragua**: pueblo caquetío del interior, 1531 (Castellanos p. 201).
  Además es un `-gua` caquetío con fecha para la campaña de d21.7.
- **Norupara**: poblado junto al puerto de Coro (González Batista 2002
  p. 162, vía ANH 1988).
- **Buinare** (Bonaire), grafía de 1589.

### D-f · Curaciones baratas (no cambian el scorer)

1. toponimo-111: el «Coria-na» de Oliver está en **La Ramada**, no en Punta
   Espada.
2. geografia_politica-008 (*managuanare*): el documento debajo es la
   **probanza de 1680** (AHC, Fondo Arcaya, t. VII), no sólo «González,
   PLINCODE». Sube la cadena y deja claro que las formas son de 1680.
3. `matakán`: la cita «conejos y venados» de Castellanos que el lexicón pone
   en Coro está bien (p. 185). Pero la otra, «que mataba con perros», es de
   Maracaibo (p. 189).

## 3. Cruce con otra parcela

Pérez de Tolosa 1546 (Fernández Duro, t. II, p. 234): los caquetíos de los
llanos «algo difieren en la habla á los de Coro». Castellanos no lo
contradice. Dice que los caquetíos «estiéndense por tierras muy distantes»
(p. 185), y Espira lleva a su jornada de los llanos a Joan de la Puente,
«lengua de caquetíos» (p. 211). Hay caquetíos en el interior (pp. 200-201)
y, en los llanos, junto a los jaguas (Parte I, p. 137). Son dos testigos de
una lengua común con variación.

## 4. Lo que queda pendiente

- **Brito Figueroa 1962**: no se pudo minar (sin texto legítimo). El catálogo
  de la BNV dice 48 páginas y «Región Nororiental». La escala del mundo se
  contestó con Castellanos, González Batista 2002 y el Ballesteros que ya está
  en el corpus (§escala_del_mundo del YAML). Ninguna fuente dice cuánta gente
  vivía en **un** poblado.
- **González Batista, *El nombre de Coro***: sin año, editorial ni página.
- Castellanos: verificar en imagen los versos que se citen (sólo hay `.txt`),
  y la Parte IV.
- El PDF de González Batista 2002 está en `fuentes_caquetios/` **sin
  commitear**: es obra con derechos y el repo es público. Se vuelve a bajar de
  HEVILA (URL y sha256 en la ficha).
