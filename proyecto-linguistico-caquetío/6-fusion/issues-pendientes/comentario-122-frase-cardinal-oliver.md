# Comentario para #122 — la frase cardinal de Oliver, releída en las dos ediciones

> Borrador del 2026-09-16, **sin publicar**. Va a la issue cerrada
> [#122](https://github.com/miguelgilurbina/curiana-radio/issues/122)
> (decisión del 2026-09-12: salida 4, la lectura de Miguel). La campaña del
> 2026-09-14 dejó la frase cardinal como deuda «por decisión, no por
> descuido». Esto es lo que dice la fuente cuando se lee entera.

## 1. La cita exacta, y dónde está

Es **una sola página con dos paginaciones**, y el repo la venía citando como
si fueran dos: **tesis 1989 p. 275** (`Oliver_1989_Tesis_Arawakan_NW_Venezuela_UCL.pdf`,
pdf 302; sin capa de texto útil, leída en imagen) **= DOC 264** (edición
DOC 2006 del capítulo, `Chapter 3 Ethnohistory.DOC-comprimido.pdf`, pdf 82;
con capa de texto: `pdftotext` con y sin `-layout` dan el mismo texto). La
cita sigue en tesis p. 276 = DOC 264-265.

> «Thanks to historian González Batista (1984) we know that Paraguaná, in
> the XVIth century, was divided into two territories, each occupied by a
> different Caquetío sub-group: the **Amuayes** which controlled the
> **southern** part and the **Guaranaos** who controlled the **northern**
> part of the peninsula. Each sub-group had its own beach heads, entitling
> them to specific fishing grounds, and one could further assume that the
> inland agricultural plots were as equally well defined. However, more
> specific details (i.e. how were these catchment zones distributed,
> managed, or controlled within each sub-group) can not be inferred from
> the available data. As González Batista explained:» (tesis p. 275 = DOC 264)

Y lo que sigue es la cita de González Batista, en inglés en el cuerpo y en
castellano en nota (n. 205 de la tesis, p. 276; n. 113 de la edición DOC):

> «Existe una importante crónica suscrita por Modesto Delmonte, quien parece
> haber manejado estos documentos hoy desaparecidos, o cuando menos recogido
> sus datos de labios conocedores de las tradiciones peninsulares. En ellas
> se menciona la existencia de dos grupos tribales en el siglo XVI: los
> amuayes y los guaranaos, de acuerdo a la misma relación, los amuayes se
> encontraban primero establecidos en el poblado de **Cayerúa** y luego en el
> de **Moruy**, en tanto que los segundos se afincaron en **Santa Ana**. Por
> nuestra parte, hemos podido comprobar que el traslado de los amuayes fue
> algo que sucedió realmente; esto y otras afirmaciones del Sr. Delmonte nos
> ha permitido establecer la credibilidad de su crónica. D. Ventura de
> Bustillos, protector de los indios paraguaneros en 1760, señala que a los
> indios les correspondía 'todo el morui Con todo su Continenti de savanetas
> q[ue] hasta el p[resente] han gozado dhos Yndios, p[or] la posesión de
> [San Juan] de Cayarba [Cayerúa].'» (González Batista 1984: 31-32, en
> Oliver n. 113 / n. 205)

## 2. Lo que dice la fuente que Oliver cita — y lo que no dice

La frase cardinal es **de Oliver**: está antes del «As González Batista
explained:», en su propia voz. Lo que cita de González Batista, literal y en
las dos lenguas, dice **aldeas** —Amuayes en Cayerúa y luego en Moruy;
Guaranaos en Santa Ana— y un documento de 1760 que ata a los indios de Moruy
a «la posesión de Cayarba». **Ni norte ni sur.** Tampoco los «beach heads» y
los «fishing grounds» están en lo citado: van en la misma frase de Oliver.

O sea: el norte/sur está en González Batista 1984: 31-32 **fuera del
fragmento citado**, o es inferencia de Oliver. En el repo no se puede
decidir: González Batista 1984 no está (lo que hay es *El nombre de Coro*,
`gonzalez-batista-nombre-de-coro`, otra obra). Oliver no cita para esta frase
ni a Arcaya ni ningún padrón: «1594» y «padrón» dan **0** en todo el
capítulo; Arcaya (1916, 1977, 1978: 74) aparece para Federmann, los jirajaras
y el pleito de bastardía, no para los clanes.

## 3. Todas las menciones en el capítulo (medido)

`grep -i` de `amuay|guaranao` sobre el texto del capítulo entero, con y sin
`-layout` y con las variantes partidas por guion (`amua-`, `guara-`,
`sub-group`): **4 líneas, todas en este pasaje** (DOC 264-265). «southern
part» / «northern part» junto a los clanes: **una vez**. Las otras menciones
de las aldeas no traen punto cardinal:

| Dónde | Qué dice |
|---|---|
| DOC 262 | «Moruy and Santa Ana in the peninsula» entre las aldeas más grandes del XVI que Oliver localizó arqueológicamente; en Paraguaná «the settlements are concentrated around the Santa Ana (extinct) volcano» |
| DOC ~271 | «The Indians of Santa Ana and Moruy (Paraguaná) were dead set against Martínez Manaure's claims because of the question of bastardy» (Arcaya 1978: 74; A.G.I. 1705-1777) |

## 4. Lo que el repo tiene por su cuenta

Fuentes en `fuentes_caquetios/`, leídas para esta pregunta (Arcaya con
`pdftotext`, páginas impresas medidas por el pie; Esteves en su OCR):

| Fuente | Dice | Qué le hace a la pregunta |
|---|---|---|
| **Arcaya 1920 pp. 275-276** | Pregón de la residencia abierta por el Ldo. Arias de Villasinda (llegó a Coro en julio de **1553**) a los «Indios principales de nación caquetíos… que residían en los pueblos de Cabure, Tomodore, Cumarebo, Miraca, **Santa Ana, Cayaruba (Cayerúa, en Paraguaná)**, Urraque y Hurehurebo» | En 1553 los dos pueblos de indios de Paraguaná son Santa Ana y Cayerúa. **Moruy no aparece.** Es dato dos siglos anterior a Bustillos y tres a Delmonte |
| **Arcaya 1920 pp. 326-327** | «Subsistía y había crecido el pueblo de Caquetíos de Santa Ana de Paraguaná. **A fines del mismo siglo XVI se fundó el de San Nicolás de Moruy con otros Caquetíos que antes ocupaban otros sitios de Paraguaná.**» | El reasentamiento de Delmonte (Cayerúa → Moruy), **con fecha**: Moruy es fundación colonial tardía con gente trasladada. Es exactamente la regla 3 que sostiene la salida 4 |
| Arcaya 1920 p. 22 | Salinas: «las más importantes son las de Guaranao» | Guaranao = suroeste |
| Esteves 1989 p. 14 | AMUAY: bahía y población del municipio Los Taques; «en papeles antiquísimos de la Colonia se menciona a los indios amuayes»; la petición de 1556 al obispo Ballesteros (sin referencia) | Amuay = noroeste; el etnónimo es colonial temprano |
| Esteves 1989 p. 41 | GUARANAO: salina del municipio Punta Cardón | suroeste; nada del clan |
| Esteves 1989 p. 30 | CAYERUBA: aldea del municipio Pueblo Nuevo, precolombina (cerámica, cementerio); la grafía «Cayerúa» del mapa la tiene por «afectada de snobismo» | norte-centro; verificado en imagen el 2026-09-16 |
| OSM 2026 (`toponimos_mapa_kaketiana.yaml`) | Cayerúa 11,986 · Moruy 11,822 · Santa Ana 11,782 · Amuay 11,775 (costa oeste) · Guaranao 11,675 (suroeste) | los homónimos van con las aldeas, no con la frase |

## 5. Lo que sostiene cada lado

**La frase cardinal (Amuayes sur, Guaranaos norte).** Sólo la autoridad de
Oliver. Su fuente declarada, citada por él mismo en dos lenguas, no la
contiene. Ninguna fuente del repo la apoya, y contradice a las tres aldeas
que él cita, a Arcaya y a los homónimos vivos.

**La decisión #122 (salida 4).** Pata norte —Amuayes en Cayerúa y la costa
oeste—: Delmonte vía González Batista; Bustillos 1760 (los indios de Moruy
tienen Moruy «por la posesión de Cayarba», o sea descienden de Cayerúa);
Arcaya 1553 (Cayaruba, pueblo de indios); el homónimo Amuay. Pata sur
—Guaranaos en Santa Ana y la laguna—: Delmonte; Arcaya 1553 (Santa Ana,
pueblo de indios); Arcaya p. 22 (las salinas de Guaranao); el homónimo. Pata
«el Moruy de Delmonte es reasentamiento colonial»: Arcaya pp. 326-327 lo
fecha a fines del XVI y Bustillos 1760 lo ata a Cayerúa. **Esta última es
la mejor sostenida de las tres, y es nueva desde el 12.**

**Lo que sigue sin fuente**: que «Moruy podría ser el centro de los
Guaranaos o Moruyes» en el precontacto. Lo que las fuentes dicen de Moruy es
que fue de los amuayes trasladados (1760) y fundación tardía (Arcaya). Los
«Moruyes» de la tradición popular quedan explicados como amuayes de Moruy,
que es lo que #122 ya decía.

## 6. Recomendación

**Mantener la decisión** y reescribir la deuda, que hoy dice «frase cardinal
de Oliver invertida respecto a sus propias aldeas; verificar en González
Batista 1984» (`paraguana_dos_clanes.yaml`, `verificacion_2026-09-12.deuda`):

1. **La deuda, precisa.** «La frase cardinal (tesis p. 275 = DOC 264) es de
   Oliver; lo que cita de González Batista 1984: 31-32 no dice norte ni sur.
   Verificar en GB 1984: 31-32 si el norte/sur es de GB. Si no lo es, la
   discrepancia se cierra como inferencia de Oliver y la deuda desaparece.»
   Nada de esto reabre la decisión: lo nuevo la apoya.
2. **Apoyos nuevos** para `paraguana_dos_clanes.yaml` (propuesta, regla 5):
   Arcaya 1920 pp. 275-276 (Santa Ana y Cayerúa como pueblos de indios en
   1553; Moruy ausente) y pp. 326-327 (Moruy fundado a fines del XVI con
   caquetíos trasladados). Y que la etiqueta diga dónde está el hueco:
   `reconstruido`, con `deuda: sin-procedencia` **sólo** para la pata «Moruy
   = centro de los Guaranaos».
3. **Una errata a corregir.** Oliver escribe **Cayerúa** en las dos
   ediciones (verificado en la imagen de la tesis, p. 276, y en el texto
   DOC). El «Cayerda / Cayerta / "Coyarna"» de `paraguana_dos_clanes.yaml`,
   de `toponimia_paraguana_miguel.yaml` (l. 107-113: «Oliver mismo vacila en
   la grafía»), de `DISENO_ERA2.md` §2 y del cuerpo de #122 fue **lectura
   nuestra** del 2026-09-01, no vacilación de Oliver. La cadena real de
   formas es Cayaruba (1553, Arcaya) · Cayarba (1760, Bustillos) · Cayeruba
   (Esteves) · Cayerúa (mapa y Oliver): material para la campaña de
   topónimos.
4. **Citar la página como «tesis p. 275 = DOC 264 (pdf 82 del capítulo)»**
   en los tres sitios que hoy dicen «p. 275» o «DOC 264» a secas.

## 7. Lo que no se pudo verificar

- González Batista 1984: 31-32 (no está en el repo; **es lo único que zanja**
  el origen del norte/sur). Delmonte 1883. El documento de Bustillos 1760
  (GB no da signatura en lo citado).
- El «padrón de 1594»: 0 en Oliver cap. 3, 0 en Arcaya 1920 (lo único de
  1594 es Diego Osorio en Coro, en abril, con una galicabra), 0 en `.md` y
  `.yaml` del repo. Si viene de otra fuente, hay que nombrarla antes de
  contar con él.
- Arcaya 1920 no tiene `.txt` en `fuentes_caquetios/` (leer-fuente §1 pide
  guardarlo junto al PDF); se extrajo al scratchpad para esta lectura.
  Guardarlo en el repo lo decide Miguel.

---

*Cómo se midió: `pdftotext -enc UTF-8` (con y sin `-layout`) sobre el PDF
del capítulo (DOC) y `pymupdf` a 130 dpi sobre las pp. 275-276 de la tesis
UCL, leídas en imagen; `grep` con variantes sobre el capítulo entero; Arcaya
1920 con `pdftotext` y páginas impresas por el pie. Regla 6: los ceros de
arriba van con las variantes que se probaron.*
