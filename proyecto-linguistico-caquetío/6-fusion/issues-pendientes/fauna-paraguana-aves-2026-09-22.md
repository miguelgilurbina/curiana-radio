# FA2 — Las aves de Paraguaná: qué se ve, qué se oye y cuáles no tienen nombre

**Campaña de fauna (tercera minería), parcela FA2. 2026-09-22.**
Rama `campana/fauna-aves`. PROPUESTA (regla 5): nada de esto toca el canon.
Datos en `6-fusion/fauna_paraguana_aves_2026-09-22.yaml` (ensamblado y verificado
por `6-fusion/scripts/ensamblar_fauna_aves.py`); medición moderna en
`6-fusion/medicion_gbif_aves_paraguana_2026-09-22.yaml`
(`6-fusion/scripts/medir_gbif_aves_paraguana.py`). Las cifras de aquí salen de
esos dos scripts (`meta.medido` y la cabecera de la medición).

Las aves marinas y costeras son de esta parcela; FA3 las cita por su id
(`ave-040` a `ave-059`).

---

## Lo que de este encargo resultó falso al medirlo

| Lo que se daba por hecho | Lo medido |
|---|---|
| La cotorra de hombros amarillos está en GBIF en la península (60 filas) | Las 60 filas son **ausencias**: el dataset NeoMaps 2010 de PANGAEA publica cada punto de muestreo como `PRESENT` con `organismQuantity: 0`, y salen igual las ocho amazonas de Venezuela, incluidas dos de selva. Presencias reales: **0**. Y sin embargo la especie SÍ estuvo: extinta en Paraguaná hacia 1950 (Ferrer-Paris et al. 2014, vía Wikipedia) y recordada como «cota» (Medina p. 82) |
| El alcaraván, ave de todos los días | GBIF: **0** registros de *Burhinus bistriatus* en la caja. Es un cero del observador (ave nocturna de sabana; eBird se hace de día en la costa), no del ave: Medina (p. 89), Esteves (p. 12) y Bisbal 1990 la dan |
| «Togogo» es error de OCR por Tococo (`esteves_parte2_falcon.yaml` §conflictos) | **Al revés**, verificado en imagen: Esteves p. 134 dice «TOGOCO … (Togogo: ave ansérida)»; el OCR leyó TOCOCO |
| Maraquita: «su canto reza: tii-tu-cú» (pdftotext) | La imagen dice ***tu-tu-cú***. Y la guacharaca no es «ííízchará-cá» sino ***ua-chará-cá*** (Alvarado p. 143). El OCR falla justo en la cursiva |
| La laguna de Guaranao como hábitat de aves del XV | Laguna y manglar son de **1985** (corrección del 2026-09-16 en `laguna-guaranao-parque`). El manglar que se proyecta es el de Tiraya / Boca de Caño |
| Los candidatos del encargo: cardenal, cotorra, turpial, alcaraván, guacharaca, salinas | **La cotorra y el alcaraván NO son huecos**: el canon tiene `koro`/`waka` «cotorra» y `dara` «alcaraván», atestiguadas. Y el flamenco tampoco (`chogogo`). Los otros tres sí lo son |

---

## El veredicto en una frase

**El caquetío ya nombra buena parte de las aves que se oyen a diario, y casi
siempre por su voz —dara, wakoa, chuchubi, warawara, chogogo, tijua—; los huecos
de verdad son diez aves concretas, y de seis de ellas hay onomatopeya o nombre
imitativo (cuatro en una fuente leída, dos vía Wikipedia).**

---

## Las cifras (de `meta.medido` y de la medición)

- GBIF, caja de la península y sus aguas: **35.828 registros de aves, 230
  especies**, tras restar **480 filas de ausencia**; casi todo es eBird (el reparto por dataset, en la medición).
- **39 grabaciones de xeno-canto hechas en la península** (Santa Ana/Machuruca
  y Montecano), citadas por su ID en cada ave (`escuchar_en_la_caja`).
- El YAML: **51 entradas** (algunas agrupan especies), **12 de presencia
  segura, 33 probable, 3 dudosa y 3 excluidas** (gorrión, paloma doméstica,
  garcita reznera). **33 son huecos**; **18 tienen voz caquetía** en el lexicón.
- **9 onomatopeyas documentadas**; cinco verificadas en imagen (guacharaca, maraquita, titirijí, corocoro y las formas de la guacoa).
- **9 silabeos propuestos** (hipotéticos): **8 pasan** la fonotáctica del
  caquetío atestiguado y **2 chocan con el lexicón** (abajo).

---

## Los diez candidatos a referente

Ordenados por la fuerza de la evidencia del sonido. `desc_referente` ≤ 180 y
`se_oye` ≤ 80 los mide el ensamblador.

| id | ave | se_oye (borrador) | de dónde sale el sonido |
|---|---|---|---|
| ref-aves-03 | guacharaca | «ua-chará-cá», grito de tráquea al amanecer | Alvarado p. 143, **imagen** |
| ref-aves-09 | corocoro | «coró, coró» | Alvarado p. 92, **imagen** |
| ref-aves-06 | colibrí | el zumbido de las alas | Alvarado p. 279 («sunsún», sin imagen) |
| ref-aves-04 | pitirre | trino agudo que dice su nombre | Alvarado p. 255 (sin imagen) |
| ref-aves-08 | gaviota guanaguare | grito que suena a risa | Birds of the World vía Wikipedia |
| ref-aves-01 | cardenal coriano | silbidos claros repetidos | xeno-canto XC220411 vía Wikipedia; grabado en la caja |
| ref-aves-07 | alcatraz | no canta: el golpe contra el agua | Alvarado p. 292 (cita a Codazzi) |
| ref-aves-02 | turpial | silbidos largos y sonoros | Medina p. 288 («ave canora»); sin transcripción |
| ref-aves-05 | carpintero | golpes de pico en la madera | Medina p. 67; sin transcripción |
| ref-aves-10 | chirito | hilo de voz fino desde lo alto | Medina p. 73; sin transcripción |

Reserva (hueco visible, sin sonido de fuente): los playeros migratorios —que
son el «reloj» de ecologia-038—, la tijereta de mar, el zamuro y las garzas.

---

## Lo que se encontró de paso y pesa

1. **El referente onomatopéyico choca con la puerta de las raíces.** Un
   pueblo que nombra un ave por su voz INVENTA una raíz (`wacharaka`,
   `pitiri`): ninguna está en el lexicón, así que `es_raiz_de_ninguna_parte`
   rechazaría la acuñación. Y el dato de esta parcela dice que así nombró el
   caquetío a sus aves. Es evidencia directa para el issue abierto
   `raiz-inventada-puede-un-pueblo-inventar-una-raiz-2026-09-20.md`: **sí, por
   onomatopeya.** No se decide aquí.
2. **`togogo`, hermana de tierra firme de `chogogo`.** Alvarado 1921 p. 292 («¿Es
   el TOGOGO de Coro?») y Esteves 1989 p. 134 («Togogo: ave ansérida»),
   independientes y verificados en imagen. Si es el flamenco, `chogogo` deja de
   ser sólo insular y la alternancia t ~ ch entra en juego.
3. **`tokoko` encuentra su cadena.** El lexicón la tiene como acuñación
   hipotética «sin cita» (F8). Alvarado p. 292 da gal. *tokoka* «flamenco», car.
   *tokóko* y ar. *tukkuku* «corocoro»: es comparanda caribe/arahuaca, no
   caquetío atestiguado, pero ya tiene de dónde viene.
4. **`tigi` y `tauta`, las «palomitas que comen peces».** Son caquetío
   atestiguado (Zavala #247, #244, sigla E) y Esteves las pone en Tausabana, en
   bandadas sobre las albuferas (p. 62), y en Ticuí (p. 63). Una paloma no
   pesca: son otra ave. Tres lecturas, ninguna probada: la gaviotica
   (*Sternula antillarum*, que cría en la seca larga), un playero pequeño (cf.
   TIGÜITÍGÜE de Alvarado p. 290) o la tigua (*Tachybaptus dominicus*). **Si es
   la primera, el reloj de la seca larga ya tiene nombre caquetío.**
5. **Dos silabeos chocan con el lexicón**: el del corocoro (`koro-koro`) cae
   sobre `koro` «cotorra», y el de la gaviota (`kia-ja-ja`) sobre `kia` (lokono).
   Por eso el silabeo es hipotético y no se propone como nombre.
6. **`chaure`, dos lecturas**: Zavala #81 la da como la lechuza que anida en
   la arena (conducta del mochuelo de hoyo, cuya voz insular es `shoco`) y
   Alvarado p. 116 como *Strix flammea*, la lechuza de campanario.
7. **La guacoa**: Medina la da «hoy casi extinta» (pp. 129-130) y eBird la
   registra común. O se recuperó o la de Medina es otra paloma.
8. **Homógrafo**: la clave `samuro` del lexicón es «punta hacia el mar», no el
   zamuro.
9. **Para FA1 y FA3**: cualquier consulta de GBIF del proyecto tiene que
   restar `organismQuantity=0`.

---

## Opciones para Miguel

**F2.1 — Los referentes de aves.**
- **A.** Los diez de la tabla, tal cual, a una lista de referentes de fauna.
- **B.** Ahora los seis con sonido escrito —los cuatro de fuente leída
  (guacharaca, corocoro, colibrí, pitirre) y los dos vía Wikipedia (gaviota,
  cardenal)—; los otros cuatro cuando haya transcripción.
- **C.** Esperar a FA1 y FA3 y elegir de las tres parcelas juntas.
- *Recomiendo* **B, y luego C**: empezar por donde el «se oye» tiene cita.

**F2.2 — ¿El `se_oye` lleva la onomatopeya escrita?**
- **A.** Sí, entre comillas («ua-chará-cá»).
- **B.** No: se describe el sonido y la transcripción se queda en el YAML.
- **C.** Sí, pero pasada por la fonotáctica caquetía (el silabeo hipotético).
- *Recomiendo* **B** mientras F2.3 no se decida: con la transcripción delante
  el agente copia, y dos de ellas son casi el nombre castellano (guacharaca,
  pitirre). Es la misma trampa que `kali-bana`: el prompt enseñando la forma.

**F2.3 — La acuñación onomatopéyica y la puerta de las raíces** (punto 1).
- **A.** Una acuñación que imita el sonido del referente puede crear raíz
  (excepción declarada a `es_raiz_de_ninguna_parte`, sólo en referentes de
  fauna).
- **B.** No: se nombra con raíces del lexicón (`kerekere`, `humohumo`, `waka`
  como base).
- **C.** Decidirlo en el issue de la raíz inventada, con este dato.
- *Recomiendo* **C**.

**F2.4 — `togogo`.**
- **A.** Registrarla como variante de tierra firme de `chogogo` (lectura en
  `notas`, con las dos citas).
- **B.** Sólo anotarla en el corpus de ecología como propuesta (ecologia-P-aves-05).
- **C.** Nada hasta una tercera fuente.
- *Recomiendo* **A**: son dos fuentes independientes verificadas en imagen.

**F2.5 — La corrección de `esteves_parte2_falcon.yaml`** («Togogo» no es error
de OCR). **A.** corregir la `lectura` del conflicto; **B.** dejarla y anotar.
*Recomiendo* **A**.

**F2.6 — `tokoko`.** **A.** Darle `procedencia` Alvarado p. 292 como comparanda
caribe/arahuaca, sin subirla de capa; **B.** dejarla como está.
*Recomiendo* **A**.

---

## Lo que NO se cubrió

- **Nombres taínos de ave de Oviedo** (Libro XIV de la *Historia general*, en
  el repo): no se minaron. Sólo `yaguasa` (vía el lexicón y Alvarado p. 310) y
  el `inriri` de Pané (vía `taino_lista_maestra`).
- **Nombres lokono de ave** de Goeje 1939 y Perea 1942: no se barrieron; sólo
  los que ya están en el lexicón (`bimiti`, `kodibio`) y `wakokwa` (van Buurt).
- **Barnes y Phelps 1940**, «Las aves de la península de Paraguaná»: la obra
  fundacional, no localizada en acceso abierto. Tampoco el original de Bisbal
  1990 (se leyó por Wikipedia).
- **La voz de los playeros** y del turpial: ninguna fuente abierta leída la
  transcribe. eBird y Avibase bloquearon el acceso automático y no se forzó.
- **Descripciones visuales sin fuente**: sólo 23 de las 51 entradas tienen
  descripción de fuente (`meta.medido`); las demás describen con conocimiento
  general y lo declaran (`deuda: sin-procedencia`), o son las excluidas.
- Aves pelágicas y de las islas (bobas que crían en Aves, Los Monjes): fuera de
  la caja; son de FA3 si las quiere.
- Las voces de Medina `chamaco` (carpintero) y `cota` (cotorra) se citan, pero
  no se evaluaron para el lexicón.
