# La costa occidental en las crónicas del primer contacto (1499-1502)

**Tercera campaña de minería, parcela M2 (2026-09-22/23)** · rama
`campana/mineria3-cronicas` · datos y citas en
`6-fusion/cronicas_contacto_costa_occidental_2026-09-22.yaml` (los `m2.*` de
abajo son sus ids).

Regla 5: esto **propone**. No se tocó `curiana_lexicon.py`, `2-lengua/`,
`3-mundo/` ni `curiana_sim/`. **Ninguna cifra de conteo está escrita a mano**:
las imprime

```bash
python 6-fusion/scripts/medir_cronicas_costa_occidental.py
python 6-fusion/scripts/medir_cronicas_costa_occidental.py --contexto curiana --obra navarrete-t3
```

---

## Qué se preguntó

Las cuatro obras —Anglería 1892 (vols. 1 y 4), Navarrete 1829 t. III (viajes
menores y Vespucio), Navarrete 1858 t. I (viajes de Colón) y Hernando Colón
vol. 2— ya las había leído la campaña del taíno (T7), pero **sólo** para el
contacto con las Antillas. La pregunta de esta parcela era la otra: ¿qué
cuentan de la **costa de Tierra Firme occidental** —Coquibacoa, el cabo de San
Román, Paraguaná, Coro, las dos Curianas, las islas de los Gigantes— y de su
gente, esfera por esfera, y qué animales y qué mar aparecen?

## 0. Lo que resultó falso al medirlo

1. **«La Curiana de Niño y Guerra 1499 está en Cumaná» (T7).** Es cierto que no
   es la de Coro. Lo de «en Cumaná» es la glosa de Navarrete: Anglería la pone
   **pasado** Cumaná y Manacapana (vol. 1, p. 303, verificado en imagen), y el
   documento que manda —la capitulación de Hojeda (Navarrete p. 86) y el
   requerimiento al veedor de marzo de 1502 (pp. 103-105)— la define como la
   franja «dende el parage de los Frailes… hasta el Farallón». Costa
   centro-oriental, entre Maracapana y el cabo Codera.
2. 🔴 **«El guanín de Curiana… era moneda de rescate (pp. 16-17, 34)» (ficha de
   Navarrete, T7) mezcla las dos Curianas.** El rescate de las indias «por
   guanines» es de la Curiana **occidental** de 1502 —«una tierra de riego que
   los indios llamaban Curiana y él nombró Valfermoso» (p. 32)— y está en la
   **p. 33**. Y la frase de los guanines «que indicaban venirles de…
   Cauchieto» (p. 16) es de Navarrete: Anglería, su fuente, no escribe guanín ni
   una vez en el vol. 1.
3. **«El único hombre que en toda la costa entiende a los indios en 1502 es un
   español» (T7, t7.l4).** La armada de 1502 llevaba una **intérprete indígena
   de Tierra Firme, Isabel**, capturada según Navarrete en el viaje de 1499
   (p. 36 n. 1), y la instrucción de Hojeda del 20 de mayo de 1502 la pone a
   trabajar «costa á costa hablando á los indios» (doc. XX, pp. 107-108). El
   cero de `intérprete` medía la palabra, no la práctica.
4. **El canon (`geografia_politica-006`, nodo-008) llama «Puerto de San
   Bartolomé» al palafito de Vespucio y deja pendiente «40 casas».** En
   Navarrete son dos sitios: el poblado sobre estacas de la costa oriental del
   golfo, sin nombre (p. 8), y el lago de San Bartolomé, donde «tomamos las
   indias» (doc. XVIII, p. 105). Y la Lettera dice **«veinte grandes casas, con
   corta diferencia»** (p. 219). Las 40 no están ahí.
5. **Anglería no narra el viaje de Hojeda de 1499** en los volúmenes del repo:
   `Cuchibacoa` sólo sale en listas de provincias.

## 1. El veredicto, en una frase

La Kaketiana entra en las crónicas por **dos viajes de Hojeda** (agosto de
1499 y abril-mayo de 1502), y casi todo lo que se sabe de su gente en ese
momento viene de **los papeles de Hojeda que Navarrete imprime**, no de ningún
cronista: un poblado de «veinte» casas sobre estacas en la costa oriental del
golfo de Coquibacoa, una isla de los Gigantes con casas en una hondonada, una
«tierra de riego que los indios llamaban Curiana» donde se pagaba rescate en
guanines, y una intérprete cautiva; de la lengua de esa costa no quedó
apuntada ni una palabra, y de Paraguaná sólo su perfil desde el mar.

## 2. Las dos Curianas

| | La oriental | La occidental |
|---|---|---|
| Qué es | el nombre castellano de la franja del rescate de perlas | «tierra de riego que los indios llamaban Curiana» |
| Dónde | de los Frailes al Farallón (cabo Codera); Anglería: pasado Cumaná y Manacapana | entre Codera y Coquibacoa; **Coro según Navarrete** (p. 8 n. 3, sobre Pedro Simón) |
| Cuándo | Niño y Guerra 1499-1500; Hojeda la costea en 1499 | Hojeda, abril de 1502 («Fecho en Valfermoso», doc. XIX) |
| Documento | capitulación (p. 86); requerimiento (pp. 103-105) | instrucción a Vergara (pp. 106-107); la narración, pp. 32-34 |
| Qué trae | la red con Cauchieto; galitas, tenoras | el rescate en guanines; hamacas, ollas, cántaros, algodón |

⚠️ Que Valfermoso sea Coro es inferencia de Navarrete, y su propio itinerario
la tensa (de Valfermoso Hojeda va a Puerto Flechado, que él pone en
Chichiriviche, al este, y de allí a Curazao). Y el nombre «Curiana» para
Valfermoso es frase de Navarrete sobre los autos del pleito, que no están en el
repo. **Con PR #207 hay una tercera**: el «Coriana» de Castellanos, aldea de La
Ramada junto a «Paraguanil» (p. 264), que coincide con la «Coria-na» junto a «Paragua-nil» que Oliver lee entre las aldeas wanebucán de la Guajira (cap. 3 p. 207).

## 3. Lo que sí hay, por esfera

- **Geografía y topónimos.** Paraguaná aparece como «una que juzgaron ser
  isla» con el cabo de San Román (p. 8), y eso explica que la gobernación se
  llamara «**isla** de Coquibacoa». La capitulación manda a Hojeda a «la isla é
  las otras que allí están cerca della… **donde están las piedras verdes**, de
  las cuales trugistes muestra» (p. 86): si la «isla» es Paraguaná, eso es el
  corazón de la Kaketiana (hipótesis mía, m2.g3). «**Los indios le llamaban
  Golfo de Coquibacoa**» (p. 8). Las grafías de los papeles de 1500-1515 —la
  capitulación, el nombramiento, una cédula de 1501, los testimonios de Hojeda,
  Morales y Toro— las lista el medidor con su folio; ⚠️ **todas del OCR, sin
  ver en imagen**: la de la capitulación (`Qoiquevacoa`) tiene las letras de
  *Quiquevacoa*, la forma reduplicada sin nasal, y el canon (`toponimo-034`)
  la cita como *Quinquevacoa* por Otte 1963. Hay que cotejar.
- **Casas y pueblos.** Palafito de «veinte grandes casas… á modo de campanas»,
  sobre «sólidas y fuertes estacas», con puentes levadizos (m2.c1). Los
  Gigantes: cinco casas en una hondonada a una legua de la playa (m2.c2; cf.
  Federmann 1530, PR #210: una aldehuela de tres casas).
- **Comida.** «**Tierra de riego**» en Valfermoso, 1502 (m2.c3): sería la
  primera mención de regadío en esa costa, y el buco del canon no tiene fecha
  de fuente. ⚠️ El OCR dice «rieeo»; lo sostiene la nota de la misma página
  sobre «regar las tierras» en Santa Marta. Verificar.
- **Pesca y mar.** Canoas monóxilas, nadadores con la lanza bajo el agua, los
  Gigantes saltando al mar mientras disparan (m2.p2). Y la **isla de las
  hierbas**: pescadores sin agua dulce que mascaban hierba con polvo blanco de
  una calabacita (m2.p1). Navarrete la tiene por Marajó, pero es la isla
  inmediatamente anterior a la de los Gigantes: si fuera Bonaire, sería la
  observación más temprana del hayo con cal en la esfera. **Hipótesis**, no
  dato.
- **Metales.** 🔴 **El rescate «á precio de guanines»** en la Curiana
  occidental, 1502 (m2.m1). 🔴 **La cédula de 1501**: los españoles sacaban
  guanines «de las islas de la Paria é de Caquibacoa» y «los han traído é traen
  á vender á los dichos indios de la dicha isla Española» (pp. 518-519, m2.m2).
  Es el vector castellano del guanín **documentado en el acto**: todo guanín
  antillano posterior a 1499 deja de servir como prueba de contacto
  precolombino. Aviso directo para dc.4 y T7.
- **Lengua.** Isabel (m2.l1). Ninguna voz de la costa occidental; las únicas de
  Tierra Firme al oeste de Paria son orientales —*galitas* (canoas),
  *tenoras* (perlas) en Curiana y *corixas* (perlas) en Cauchieto, verificadas
  en imagen (m2.l2)—: dos palabras para «perla» a seis días de distancia. Y
  dos voces que **son del editor**, no de la costa: los «guanines» y las
  «macanas» de Navarrete, donde Anglería escribe «oro aunque no puro» y
  «armados á su modo» (m2.l4).
- **Trato y guerra.** El primer año ya hay capturas: las indias del lago de San
  Bartolomé (1499) y las de Valfermoso (1502). El «miedo a la trata» que
  Federmann ve en Paraguaná en 1530 tiene treinta años de historia documentada.
- **Fauna** (clave `fauna:`, esquema común): el conejo de Coquibacoa, «semejante
  á los de Castilla» (1502); lo que Hojeda le enseñó a Roldán en 1499
  —«ciervos, conejos, pieles y garras de tigres y guaninis» (Hernando p. 115)—;
  las tortugas y los peces de la isla de las hierbas; una iguana inconfundible
  en un pasaje de Vespucio sin lugar; y, **separados porque son de la costa
  oriental**, los animales de la Curiana de Niño y Guerra, entre ellos los
  «**mugidos horrendos**» nocturnos de «animales grandes pero inofensivos» —el
  único sonido animal de estos pasajes de Tierra Firme (la atribución al jaguar es
  del traductor de 1892).

## 4. Lo que NO se encontró

- **Paraguaná** por su nombre: cero en las cuatro obras. Ni una casa ni una
  persona de la península en 1499-1502 (cf. Pérez de Tolosa 1546, PR #209:
  «cuatro poblezuelos»).
- **Aruba, Bonaire**: cero por su nombre. **Caquetíos, Manaure**: cero.
- **Ninguna palabra** de la lengua de la costa occidental.
- **Navarrete t. I y Hernando**: la costa occidental no sale, salvo el regreso
  de Hojeda (Hernando p. 115).
- **Los autos del pleito Hojeda–Vergara–Ocampo** (Colección diplomática t. II)
  no están en el repo: decidirían dónde está Valfermoso, si hubo oro en Curazao
  y qué dijo el escribano de la Curiana occidental.

## 5. Cobertura por obra

| Obra | Leído a mano | Barrido con el medidor | Queda |
|---|---|---|---|
| Navarrete t. III | Sección 1.ª pp. 3-41; docs. X, XI, XVII-XX; suplemento XLVII; pleitos pp. 543-545 y 590; Vespucio pp. 210-262 | el volumen entero | Sección 3.ª (Darién); resto de los pleitos |
| Anglería vol. 1 | libro VIII (pp. 301-318) y la nota de la p. 39 | entero | vols. 2-3 fuera del repo |
| Anglería vol. 4 | — | entero | no narra esta costa |
| Navarrete t. I | — | entero | nada de esta costa |
| Hernando vol. 2 | cap. LXXXIV (pp. 113-118) | entero | vol. 1 fuera del repo |

## 6. Para Miguel

- **A.** Registrar la separación de las Curianas (oriental / occidental, más la
  tercera de PR #207) donde el canon la necesita. Toca #33.
- **B.** Llevar al corpus, con `epoca: contacto-temprano` y su regla 3, los tres
  hechos más firmes: el rescate en guanines (m2.m1), la cédula de 1501 (m2.m2)
  y el palafito de «veinte» casas (m2.c1, que además corrige
  `geografia_politica-006` y nodo-008).
- **C.** Verificar en imagen las pp. 32, 86-89, 518 y 544 de Navarrete
  (archive.org `bub_gb_HFzXrEyoeCAC`, dominio público): «riego» y las grafías de
  Coquibacoa. Sin eso, m2.c3 y m2.g2 no se citan.
- **D.** Isabel como hecho de contacto y transmisión, y como corrección de
  t7.l4.
- **E.** La isla de las hierbas, en espera hasta cotejar la arqueología de las
  ABC.

**Recomendación: C primero, luego A + B; D como nota; E en espera.**
