# Decisión — Los dos clanes de Paraguaná: ¿manda la frase de Oliver o mandan las aldeas?

> Borrador para el tablero (label `decision`). Lo publica Miguel (regla 10).
> Toca [[DISENO_ERA2]] §2 y §9, y `6-fusion/paraguana_dos_clanes.yaml`.

## El problema, medido el 2026-09-12

[[DISENO_ERA2]] §2 dejó la asignación norte/sur de los clanes «EN
VERIFICACIÓN» porque los homónimos modernos parecían invertidos respecto a
Oliver. Ahora está medido con las coordenadas del barrido OSM
(`6-fusion/toponimos_mapa_kaketiana.yaml`), y **la inversión no está entre la
fuente y el mapa: está dentro del propio pasaje de Oliver.**

Oliver 1989 cap. 3 pp. 275-276 (vía González Batista 1984 y Delmonte 1883;
verificado en imagen el 2026-09-01) dice dos cosas:

1. La **frase cardinal**: «the Amuayes which controlled the **southern** part
   and the Guaranaos who controlled the **northern** part of the peninsula».
2. Las **aldeas** de Delmonte: los Amuayes «first established in the village
   of **Cayerda** and later in **Moruy**», los Guaranaos «settled in **Santa
   Ana**».

Las aldeas, en el mapa:

| Aldea | Clan (Delmonte) | Latitud N | Dónde cae |
|---|---|---|---|
| Cayerúa | Amuayes (primero) | **11,986** | costa norte |
| Moruy | Amuayes (después) | **11,822** | centro-norte |
| Santa Ana | Guaranaos | **11,782** | centro-sur, al pie del cerro |
| *Amuay* (homónimo moderno) | — | 11,775 | costa oeste |
| *Guaranao* (homónimo moderno) | — | 11,675 | suroeste |

Las tres aldeas que Delmonte nombra ponen a los **Amuayes al norte** y a los
**Guaranaos al sur** — lo contrario de la frase cardinal, y **lo mismo que los
homónimos modernos**. O sea: el mapa concuerda con las aldeas; lo que
discrepa es la frase de Oliver (o de González Batista, a quien resume).

## Lo que Miguel recuerda (2026-09-12)

> «Hay una diferencia Guaranaos y Amuayes, pero en otros casos se mencionan
> Amuayes y **Moruyes**, y también se mencionan en otros casos **subgrupos**
> de las tribus.»

- **Moruyes**: la tradición popular que recogió el barrido web
  (`toponimia_paraguana_miguel.yaml`, s.v. amuay) dice que «sus primeros
  habitantes pertenecieron a la tribu AMUAYES, quienes poblaron la Península
  junto con los MORUYES». Con Delmonte delante, «Moruyes» son con toda
  probabilidad **los Amuayes ya reasentados en Moruy** — el mismo clan
  nombrado por su aldea nueva — y no un tercer grupo. Es hipótesis; se
  verificaría con Delmonte 1883 o González Batista 1984, que no están en el
  repo.
- **Subgrupos**: es la palabra de Oliver («sub-group», «sub-groups»). No
  aparece ningún cuarto nombre en lo que el repo tiene: Esteves nombra Moruy
  y Santa Ana sólo como municipios.

## Las tres salidas

1. **Mandan las aldeas** *(recomendación del escriba)*: Amuayes ↔ Moruy
   (norte), Guaranaos ↔ Santa Ana (sur). Son el dato concreto; la frase
   cardinal es la capa interpretativa, y contradice a sus propias aldeas. Los
   homónimos modernos quedan como corroboración, no como fuente. Se anota la
   discrepancia en `paraguana_dos_clanes.yaml` con `deuda: frase cardinal de
   Oliver invertida respecto a sus aldeas; verificar en González Batista 1984`.
2. **Manda la frase**: Amuayes sur, Guaranaos norte, y las aldeas se tratan
   como error de Delmonte. Es la lectura más débil: son tres topónimos
   concordantes contra una frase.
3. **No se decide hasta tener a González Batista 1984** — y los nodos de la
   era 2 se siembran sin cardinal, sólo con aldea (Moruy / Santa Ana), que es
   lo único que el motor necesita de verdad.

La 3 es compatible con la 1 y no bloquea nada: el diseño dice «nodos
calcados, no inventados», y las aldeas están calcadas.
