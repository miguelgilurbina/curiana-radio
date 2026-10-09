---
tipo: sesion
fecha: 2026-10-09
pueblo: achagua
quien: "minero achagua, minería 2 «esferas de las hermanas» (Claude Opus 5.5), rama vault/hermanas-achagua"
plan: 08_creencia_achagua_que-minar
propuesta: 6-fusion/hermanas_achagua_2026-10-09.yaml
descripcion: "Las cinco esferas de lo achagua (Rivero, Neira, Gumilla) y de lo maipure (Gilij t. II y t. III pp. 30-31), en el esquema único de las hermanas, con la Vía A auditada en las cinco."
---

# Las esferas de la hermana achagua (y de la maipure)

> Plan: [[08_creencia_achagua_que-minar]] · minería 1: [[09_creencia_achagua_mineria]]
> Fuentes: [[gilij-1780-1783]] · [[rivero-1883]] · [[neira-ribero-1762]] · [[gumilla-1791]] · (mapa) [[steward-1948-hsai-4]]
> Mapas: [[mapa-familia]] · [[mapa-geografia-politica]] · [[mapa-creencia]] · [[mapa-ecologia]] · [[mapa-transmision]]
> Propuesta: `6-fusion/hermanas_achagua_2026-10-09.yaml` (esquema de `3-mundo/hermanas/README.md`) · valida con `python curiana_sim/compilar_hermanas.py --check`

Miguel (2026-10-09): «tal cual como armamos estas esferas para los caquetíos,
deberíamos hacerlo para cada una de sus hermanas». La minería 1 preguntó a lo
achagua por la creencia; ésta le pregunta por las cinco esferas, tema a tema de la
lista cerrada del README, y lee por primera vez el t. II de Gilij (*Costumi degli
Orinochesi*) y las pp. 30-31 del t. III. No se descargó nada. No se tocó
`3-mundo/`, `2-lengua/`, el lexicón ni el YAML de la transcripción de Neira. Las
cifras (hechos por esfera, por pueblo, por capa) las da el validador, no esta nota.

## 1. Método

- **Localizar en el texto, citar desde la imagen.** Gilij t. II tiene buena capa de
  texto (pdftotext, una hoja por página; la ſ sale `f`); Rivero, el OCR de
  archive.org; Neira, el YAML de la transcripción, consultado por `castellano` con
  un script; Gumilla, su `.txt`. Lo que decide una capa o lleva una forma indígena
  se vio en imagen (pymupdf a 120-400 ppp; los JPG de Neira a 4,167 px/pt). La lista
  de páginas vistas va en `meta.cobertura` de la propuesta, y cada hecho dice
  `verificado_en_imagen`.
- **Medir la ortografía antes de contar.** Gilij escribe «Maipùri» con 17 variantes
  de OCR (`Maip` da 74 aciertos; `Maipur`, 7); el achagua es «Acciàgua/Acciàgui»
  (tres aciertos en todo el t. II). Rivero escribe «Capitán» y «Cacique», «mirray» y
  «mirraye». Un cero se declara con su sonda (`meta.ceros`).
- **Quién es quién en Gilij.** Habla «degli Orinochesi» y pone el ejemplo tamanaco
  (caribe). Regla escrita en la `meta`: maipure atestiguado sólo si el pasaje nombra a
  los maipures (o a una nación de su lengua matriz, dicha en `donde`); si generaliza,
  `hipotetico` con `areal-orinoco`.
- **Desfase de Gilij t. II.** No es −26/−27 como dice la ficha: −22 en el libro II,
  −26 hacia el pdf 100, −28 en el libro IV, con láminas intercaladas. Se cita la
  cabecera de cada página.
- **Testigos.** Rivero y Neira, uno. Mimbela (la relación de 1696 que Rivero copia,
  pp. 315-330) es otro observador, y el Rivero de 1725 (pp. 414-427) escribe en
  primera persona lo que vio. Gumilla, independiente en lo que vio. Gilij copió a
  Gumilla en lo de los *Ciavinàvi*.

## 2. Lo más fuerte, por esfera

**Parentesco.**
- ⭐ **El yerno va a la casa del suegro** (maipure): «Le donne… non vanno a marito;
  vanno a moglie… gli uomini»; trabaja, pesca y caza para el suegro, y el suegro
  cobra con una fórmula, «Sapàni nutaà piche pianìtu», 'en pago de haberte dado la
  mujer' (Gilij t. II pp. 244-246, imagen). Es la primera primaria arahuaca con
  página de la residencia uxorilocal que el [[mapa-familia]] supone.
- **El cuello de botella matrimonial, en una hermana**: entre maipures y avanis «le
  donne sono ben poche» y los régulos y los viejos «le prendon tutte», diciendo a los
  jóvenes que trabajen para ganárselas (p. 254, imagen). Hasta hoy `parentesco-030`
  sólo tenía antropología comparada no arahuaca.
- **Las parcialidades achaguas con nombre de animal** son de Rivero p. 326
  (Mimbela): la culebra *Amarizán*, el murciélago *Isirri*; y Mimbela añade que el
  nombre es a veces «bufonada ó chanza». Es la primaria que `parentesco-022` no
  cita, y dice menos que él (ver §5).
- **Exogamia de consanguinidad** «aunque el grado sea muy remoto… aunque para
  casarse tengan que ir á pueblos muy distantes» (Rivero p. 326, imagen): segunda
  tradición, con la wayuu, para `parentesco-008`.
- **El ballo Queti** de los maipures: flautas secretas que fingen serpientes, «non
  è permesso di vedere alle donne» «giusta l'antico stile de' nostri vecchi» (Gilij
  pp. 284-293, imagen). Es el complejo de las flautas sagradas del noroeste
  amazónico, sin rastro costero; y es probablemente lo que HSAI atribuye a la Chuvay.

**Geografía política.**
- **Dos escalones de mando**: el Capitán Camuibay remite «al parecer y voto de su
  Cacique… Irrijirre, que vivía en un pueblo… como á un día de camino» (Rivero p. 418,
  imagen, 1725). Ilumina la pareja *apopo* / *diao*.
- **Nobles y plebeyos** en las dos hermanas: el léxico achagua de rango («Hidalgo
  noble — Cabaunicayi», imagen; señor, criado, mandar) y los «plebei e nobili» del
  Orinoco con su asamblea de guerra (Gilij pp. 192-193, imagen); el régulo maipure es
  *Pecanàti*, y «Pecanàti ani canà», 'soy hijo de régulo', es gloria (pp. 194-195).
- **Sin tributo, con convite**: la roza del régulo va primero, «non senza spesa e di
  vitto, e di bevanda pe' lavoratori» (p. 194, imagen); el achagua tiene voz para el
  convite de labranza (*Vnuma*).
- **Lenguas francas**: el maipure «lingua di moda» del Orinoco (Gilij p. 43, imagen)
  y el achagua «tan general» del llano (Rivero p. 325, imagen). Ilumina
  `geografia_politica-020`.
- **El cautivo**: achagua *Macogerri* (de ahí el «maco» del llano; Neira 60 der.,
  imagen), maipure *mero* (Gilij p. 357, imagen), tratado como yerno.

**Creencia** (101+; lo demás lo migra otro agente).
- ⭐ **Las pp. 30-31 del t. III**: los dos lugares del más allá **no son premio
  moral** —«non ho mai inteso veruno… che al delizioso vanno… quei che non rubano»—,
  y «I Maipùri dicono, che i loro Piaci si sottraggono al fuoco col cantare de' versi,
  non colle buone opere» (p. 31, imagen). Corrige la lectura de `mai-cr-03`.
- La **figurita de cica** *Minaritì* con que adivinan los piaches maipures (p. 103,
  imagen): matiza `creencia-008c` como la Chuvay de la minería 1.
- El **fin del luto** maipure: un convocante va por las casas y la fiesta cierra el
  duelo con el corte del pelo (pp. 108-109, imagen). Es la forma del segundo tiempo
  caquetío (`creencia-010c`) sin huesos.
- La **tumba de los capitanes y caciques** achaguas, que se resana cada mañana
  (Gumilla t. I p. 200, imagen): el funeral distingue el rango, como el del díao.
- «Cuando pusiesen huevos las tortugas. **Este es su calendario**» (Rivero p. 421,
  imagen), con los meses maipures por la postura de las tortugas (Gilij p. 229).

**Ecología.**
- **La quiripa sube de valor hacia el mar**: una sarta vale «dos reales» en Casanare,
  «cuatro» en Guayana y «ocho» en Trinidad, donde caribes y araucas la estiman y «no
  la hacen ellos» (Rivero p. 157, imagen). Ilumina `ecologia-105`.
- El **agua de ají con cazabe** en las dos hermanas (la *Tevàca* maipure, Gilij
  p. 226, imagen), **sin sal** en el llano.
- La **casa redonda** del jefe, «para 500 hombres» (Rivero p. 419, imagen), y las
  chozas maipures «subblimi e tonde» (Gilij p. 218, imagen).

**Transmisión.**
- ⭐ **El mirray**: «oración retórica, compuesta en estilo elevado que estudian desde
  niños y la enseñan con mucho cuidado los padres», con el tono, la postura de la
  cabeza y de las manos, en partes que rematan en lamento (Rivero p. 420, imagen).
  Es la tesis del [[mapa-transmision]] (lo formulario se transmite) en una hermana,
  y la enseña la casa, no un especialista.
- **El arco desde los dos o tres años** (Rivero p. 102, imagen): con el wayuu,
  dos tradiciones.
- **Los viejos, único archivo**: «Seppi già molto dal regolo de' Maipùri Caravàna;
  ma sopraggiuntagli… la morte, dovetti… soffrirne la perdita» (Gilij p. 232, imagen).
  El punto único de falla del mapa, atestiguado.
- **Sin genealogías**: «non mi darebbe l'animo di formare una giusta genealogia
  delle lor case» (p. 204, imagen), dos generaciones como mucho.
- **La choza de la menarquia**, *Quita* (p. 133, imagen): con el wayuu, dos
  tradiciones.

## 3. Achagua frente a maipure

Coinciden, cada una con su testigo: poliginia de los jefes; nobles y plebeyos;
lengua franca; cautivo como categoría con nombre; el caldo de ají con cazabe; la
cerveza de cazabe; la roza con convite; la casa redonda; el calendario por las
tortugas; el piache que cura cantando; la memoria en los viejos; *Guabaimi* /
*Vavèmi*, el blanco (forma y sentido).

No coinciden: la regla de matrimonio (el achagua no se casa con pariente «aunque el
grado sea muy remoto»; en el Orinoco se casan los primos cruzados); la guerra (el
achagua «no es gente de guerra», sin exámenes; el maipure azota a los mozos en los
bailes, y vive de guardia contra los guipunavis); el secreto masculino (las flautas
del ballo Queti no tienen par achagua documentado; la Chuvay es de máscaras y
abierta); el llanto (el achagua canta las virtudes; el maipure repite el nombre).

Y los dos jesuitas que saben las dos lenguas se contradicen: para Gilij el achagua
es «un dialetto della Maipùre» (t. II p. 205, imagen); para Gumilla las voces
achaguas del maipure son préstamo «introducidas por el comercio» (t. II p. 32).

## 4. Lo que no salió

Con su sonda, en `meta.ceros`: la sucesión del cacicazgo achagua (20 aciertos de
«hereda…» en Rivero, ninguno achagua); la regla de descendencia (ningún pasaje;
HSAI dice «patrilineal sibs» sin cita); los tíos en el vocabulario (ni tío, ni tía,
ni suegro, ni cuñado); el segundo entierro maipure; la navegación achagua (sólo
léxico); la pintura con significado de linaje. Y de HSAI no se localizaron la casa
de los hombres *daury* ni las «vestales» (`daur` da cero en Rivero y Gumilla).

## 5. Auditoría de la Vía A, en las cinco esferas

Los hechos del corpus caquetío `reconstruido` desde el wayuu, y lo que les hace la
hermana. Nada se degradó: lo que queda con una sola tradición se señala.

| Hecho caquetío (Vía A) | Veredicto | Con qué |
|---|---|---|
| `parentesco-004` (sucesión avuncular) | no toca | Ni Rivero ni Gilij dicen cómo se hereda el cargo |
| `parentesco-005` (linaje y nombre por la madre) | no toca; un indicio | El hijo de Chacuamare se dice achagua por la madre (Rivero p. 41); no es regla |
| `parentesco-006` (el tío materno, autoridad) | no toca | Ningún tío en el vocabulario ni en las crónicas |
| `parentesco-008` (exogamia de clan) | corrobora en parte | Exogamia achagua de consanguinidad y de pueblo (Rivero p. 326): sube a reconstruido la exogamia, no el clan |
| `parentesco-009` (levirato) | corrobora en parte | El Orinoco toma a la viuda del hermano (Gilij p. 251), generalización sin maipure nombrado |
| `parentesco-010` (ofensa a nombrar al muerto) | matiza | En el Orinoco es miedo de verlo en sueños (Gilij p. 204), no ofensa a los parientes |
| `parentesco-011` (tío materno / paterno) | no toca | El vocabulario no tiene tíos |
| `creencia-002`, `-005`, `-006`, `-007`, `-008`, `-010d`, `-011`, `-012` | ver [[09_creencia_achagua_mineria]] | Lo nuevo aquí: `-010d` sigue sin hermana (el luto maipure se cierra sin huesos) |
| `creencia-003` (tabaco y canto) | corrobora en parte | Tercer testigo, maipure: cura con versos y tabaco (Gilij pp. 90, 98) |
| `creencia-009` (tierra de muertos, sin premio ni castigo) | corrobora en parte | Sin premio moral en el maipure (t. III p. 31); el topónimo sigue sólo wayuu |
| `creencia-014` (calendario por estaciones) | corrobora en parte | El año por las tortugas (Rivero p. 421) y por el verano (Gilij p. 229) |
| `transmision-016` (jayeechi, memoria cantada) | matiza | El mirray es forma fija, pero la enseñan los padres, no un especialista |
| `transmision-017` (vocación por sueño) | matiza | En el Orinoco el maestro escoge al aprendiz (Gilij p. 90) |
| `transmision-034` (palabrero sin caciques) | no toca | La hermana tiene caciques y oratoria de todos: no hay palabrero |

Fuera de la Vía A, una corrección que pesa: **`parentesco-022`** (reconstruido,
«analogía achagua: etnografía secundaria, incl. Britannica») tiene su primaria en
Rivero pp. 107 y 326, y la primaria dice menos: nombres de animal, sí; esposas
iguales con conuco propio, sí; «una casa comunal por linaje» y «exogamia de
linaje», no; «las hijas casadas permanecen con sus familias», no en lo achagua (sí
en el maipure). Y el [[mapa-familia]] cuenta a la achagua en «el arco norteño»
matrilineal sin que ninguna fuente achagua lo diga.

## 6. Decisiones para Miguel

1. **¿Achagua y maipure son una tradición o dos?** (heredada de la 09 §7). Esta
   minería la vuelve más pesada: todos los hechos cuya única hermana es la otra
   (achagua de maipure o al revés) salen hoy `hipotetico` por `meta.regla_de_capa`,
   y su nota dice «la misma hermana mientras Miguel no diga dos».
   - *Si son una*: la propuesta queda como está. Suben a `reconstruido` sólo los
     hechos con segunda tradición de otro pueblo (wayuu): exogamia, arco desde niño,
     calendario por el medio, encierro de la menarquia, más allá sin premio moral,
     cura con canto y tabaco.
   - *Si son dos*: además subirían la poliginia de los jefes como acaparamiento
     (con `parentesco-030`), la casa redonda del jefe, la lengua franca, el caldo de
     ají con cazabe, el cautivo como categoría, la memoria en los viejos, la roza con
     convite. A favor de dos: los testigos son distintos, los pueblos estaban lejos
     (Casanare y Orinoco medio) y discrepan en matrimonio, guerra y secreto
     masculino; Gumilla da las voces compartidas por comercio. A favor de una:
     Gilij, que sabía maipure, dice dialecto, y la terminología básica coincide.
2. **`parentesco-022`**: reescribir su procedencia a Rivero pp. 107 y 326 y recortar
   lo que la primaria no dice, o dejarlo con una nota.
3. **El tema `terminologia`** para el parentesco (`meta.temas_propuestos`): la
   terminología de hermanos de la achagua no cabe en los temas cerrados.
4. **La residencia uxorilocal maipure** pide una segunda tradición citable: la
   lokona de `parentesco-023` no tiene página. Si se ancla (Roth 1915, Brett), sube.
5. **La corrección del YAML de Neira** («Mercado» es *Benidacarrun*, 75 der.), que
   regenera `lexicon_achagua.py`.

## Enlaces

[[08_creencia_achagua_que-minar]] · [[09_creencia_achagua_mineria]] ·
[[gilij-1780-1783]] · [[rivero-1883]] · [[neira-ribero-1762]] · [[gumilla-1791]] ·
[[steward-1948-hsai-4]] · [[mapa-familia]] · [[mapa-creencia]] · [[mapa-ecologia]] ·
[[mapa-transmision]] · [[mapa-geografia-politica]] · [[INDICE_FUENTES]]
