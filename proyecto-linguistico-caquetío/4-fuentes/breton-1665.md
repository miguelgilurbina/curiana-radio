---
tipo: fuente
obra: "Dictionaire caraibe-françois (1665) · Dictionaire françois-caraibe (1666) · Grammaire caraibe (1667)"
autor: "Breton, Raymond"
anio: 1665
genero: diccionario-colonial
local: ["fuentes_caquetios/Breton_1665_Dictionaire_caraibe_francois.pdf", "fuentes_caquetios/Breton_1665_Dictionaire_caraibe_francois.djvu.txt", "fuentes_caquetios/Breton_1666_Dictionaire_francois_caraibe.pdf", "fuentes_caquetios/Breton_1666_Dictionaire_francois_caraibe.djvu.txt", "fuentes_caquetios/Breton_1667_Grammaire_caraibe.pdf", "fuentes_caquetios/Breton_1667_Grammaire_caraibe.djvu.txt"]
capa_texto: mala
descargado: 2026-09-23
origen_digital: "Internet Archive, digitalización de la John Carter Brown Library (dictionairecarai00bret, dictionairefranc00bret, grammairecaraibe00bret); dominio público"
estado_minado: parcial
cobertura: "2026-09-24 (campaña cosmovisión marina): el mar, los seres, los tabúes, el lambi, el caracoli y la muerte en los tres libros, por la capa de texto por página y unas 40 páginas en imagen. Sin leer: los ~400 pares hombre/mujer del françois-caraïbe, que siguen pendientes"
verificado: 2026-09-24
minado: 2026-09-24
prioridad: media
aliases: ["Breton 1665", "Breton 1666", "Breton 1667"]
---

# Breton 1665-1667 — el kalinago de primera mano

## Qué es

Los tres libros del misionero dominico Raymond Breton, que vivió entre los
kalinago de Dominica y Guadalupe (1635-1654). Son la fuente de todo lo que
sabemos del caribe insular antiguo: Goeje 1939 y Adam 1879 lo leen a él. El
*Dictionaire françois-caraibe* (1666) es el que da, para unas 400 palabras, la
de los hombres y la de las mujeres (Adam 1879 p. 276).

Para este proyecto es **comparanda de la esfera**, no fuente del caquetío.

## Estado técnico (2026-09-23)

| Libro | PDF | texto OCR (djvu) |
|---|---|---|
| 1665 caraïbe-français | 63,5 MB | 0,75 MB |
| 1666 français-caraïbe | 54,4 MB | 0,61 MB |
| 1667 grammaire | 23,1 MB | 0,22 MB |

El OCR es **malo**: tipografía del s. XVII (s larga, ligaduras, cursiva para
el caribe). La marca de las mujeres es «F.» delante de la voz, pero la forma
que la sigue sale rota («lune, nonum, £ câ^.» por «F. cati»). **No se puede
extraer la lista de pares del OCR**: hay que leer la imagen.

Los PDF están en `fuentes_caquetios/` pero **no en git** (141 MB): el texto
OCR sí.

## Qué ha dado

Nada todavía. La campaña del habla de mujeres (2026-09-23) usó a Goeje, que ya
marca hombre/mujer voz a voz siguiendo a Breton.

## Qué falta

- Los ~400 pares del *françois-caraïbe*, leídos en imagen: la única vía a las
  formas de mujeres que Goeje no recoge.

**Cerrado el 2026-09-24** («Ok a todo, que no quede ninguna tarea pendiente»; la
recomendación era leerlos «sólo si hiciera falta más allá de Goeje»). No hace falta
para nada abierto: la transcripción del habla de mujeres de Goeje 1939 (302
entradas, en imagen, `6-fusion/kalinago_mujeres_goeje_2026-09-24.yaml`) es la que
sostiene la tanda de las hermanas, y cada concepto del núcleo se cotejó contra
ella. Breton queda como fuente PRIMARIA disponible (y el mismo día la minó, por el mar, la campaña de la cosmovisión marina: abajo) —los PDF en OneDrive por D8, el
OCR en git— para la era 3 o para verificar una forma concreta de Goeje contra su
original. Si algún día se lee, se hace por página, no entero.

## 2026-09-24 — campaña cosmovisión marina

**Primera minería de la obra.** Se preguntó por el MAR en la vida simbólica
kalinago como COMPARANDA de la esfera (no dato caquetío): cómo se dice «mar»
en el habla de hombres y de mujeres, si hay seres o dueños del mar, tabúes al
navegar, mitos de origen, el lambi y el caracoli, y la muerte y el mar. Lo leyó
un minador auxiliar con la capa de texto de cada PDF (el `.djvu.txt` no tiene
saltos de página y no sirve para citar página) y unas 40 páginas vistas en
imagen. Datos en `6-fusion/cosmovision_marina_2026-09-24.yaml` §comparanda.

**Desfases medidos:** 1665 caraïbe-français, impresa = pdf − 22 · 1666
français-caraïbe, impresa = pdf − 8 · 1667 Grammaire, pdf 27 → p. 21.

**Ocho falsos ceros de grafía**, todos resueltos: `zemi` → `chemijn`;
`oumekou` → `oumêcou`; `Couroumon` → `couloúmon`; `caracoli` → `calloucouli`;
`Savacou` → `chaoüácou` (lectura: Breton avisa, p. 442, de que la s inicial se
pronuncia ch); `écume` → `escume`/`efcume`; «Galibi» y «ancestres», partidos
por el OCR. La marca de mujeres «f.» está verificada en imagen (1666 p. 3).

**Se halló** (todo s. XVII, Guadalupe y Dominica, 1635-1654):
- 'mar': «la mer, balànna, f bálaoüa» (1666 p. 242, imagen): de hombres y de
  mujeres. Es la fuente primaria del `balaua` que el proyecto ya empareja con
  el caquetío `parawa` (vía Goeje p. 55), no una segunda atestación. Y no es
  exclusiva: en dos frases marcadas «f.» las mujeres dicen `balánna` (pp. 58 y
  394). En el tomo de 1665, `bálaoüa` no es entrada.
- Tabú al navegar: el Can Mayor y el Menor «causent les ouragans», y los
  kalinago «se donnent bien de garde de se jetter en mer quand ils la voyent
  lever» (1665 p. 348, imagen). Es el tabú marino mejor atestiguado del corpus.
- Cosmología marina astronómica: el «garzón celeste» (`chaoüâcou`) «se plonge
  en la mer pour sortir & paroistre de l'autre costé» (1665 p. 165), la Osa
  Mayor es «le canot du crabier» (1666 p. 269); estrellas que dan viento
  (`baccámon`, p. 65; `achínnao`, pp. 14 y 69) y una que anuncia el estado del
  mar (`oulíao`, de mujeres `couloúmon`, p. 421).
- Tabú de comida: el manatí no se come porque los hijos tendrían «de petits
  yeux & ronds» (1665 p. 275, imagen); la tortuga se come y se trueca.
- El lambi es bocina de aviso al desembarcar (1665 pp. 407, 467-468): señal,
  no rito. El `calloucouli` es metal en medias lunas, la joya más cara («pour
  un calloucouli vous auriez d'eux un esclave», p. 106): sin vínculo marino.
- Las cabezas de los enemigos, en las cuevas de las rocas de la orilla, para
  que los padres se las muestren a los hijos (1665 pp. 229-230).

**No se halló:** ningún espíritu o dueño del mar (el `oumêcou` es un espíritu
maligno sin lugar, 1665 p. 424); ninguna ofrenda, canto ni conjuro al mar;
ningún mito del origen del mar, de los peces o de las islas (Breton dice que no
conocen «la création», p. 424); ninguna relación de la muerte con el mar salvo
las cabezas en las cuevas. El único tabú de nombrar sobre el agua es de un RÍO
(nombrar el Coyoüini sobre sus aguas trae lluvia, p. 468).

**La sonda de Antolínez 1946** (impresa 231: «Curumón, las olas; Sabácu, las
tempestades»): `couloúmon` existe, pero como constelación y signo del estado
del mar, no como espíritu de las olas; Savacou, 0 con s; Achinaón es pez y
constelación de viento, no de lluvia; Lúcuo y Cualina, 0. La teogonía con
funciones es de La Borde 1674 vía Antolínez: tercera mano, fuera del repo.

**Deuda:** la nota de `barana` en el lexicón («cognado de CQ para») contradice
a Goeje p. 55, que la da como forma de HOMBRES filiada con el kalina/tupí
`parana`; se deja para quien fusione (la propuesta lo levanta).
