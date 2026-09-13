---
tipo: fuente
obra: "Del Habla Paraguanera. Siglo XX"
autor: "Medina Colina, Juan Bautista"
anio: 2013
publicacion: "2ª ed., ampliada y corregida. Diseño editorial Maribel Ovalles Miranda; impresión Editorial Miranda. Prefacio de Guillermo de León Calles. (1ª ed.: año no dictado; mención honorífica del CENAL)"
edicion_del_ejemplar: "2ª ed. 2013 (ejemplar físico de Miguel)"
genero: lexico-regional
local: "⚠️ FÍSICO — ejemplar de Miguel; entra por dictado curado (+ foto/OCR si hace falta cobertura)"
capa_texto: no
estado_minado: dictado-terminado  # 2026-09-08; quedan las páginas de la I a la M y las letras E-F sin declarar
prioridad: alta
verificado: 2026-09-01
aliases: ["Medina Colina", "Del Habla Paraguanera", "habla paraguanera"]
---

# Medina Colina — *Del Habla Paraguanera. Siglo XX*

## Qué es, y por qué se esperaba

El diccionario de paraguanerismos que
[[02_protocolo_habla_paraguanera]] llevaba esperando **desde antes de saber su
título** — el protocolo se escribió a ciegas (*"no se pudo confirmar el título
exacto"*) y barajaba a Brett Martínez y Tito Guerra como candidatos. Era este:
**Juan Bautista Medina Colina**. Identificado por Miguel el 2026-08-15; existe
en su biblioteca, en físico.

Los dos bloqueos del protocolo cayeron: el libro apareció, y el OCR se instaló
el 2026-08-14 (tesseract + `ocr_fuente.py`).

## Por qué importa (resumen del protocolo — leerlo entero antes de minar)

1. Es **la fuente `retro-abstraido` canónica**: la marca existe en el programa
   del corpus y tiene **cero entradas** tras dos pasadas.
2. Ataca el **punto ciego estructural** del lexicón: fuerte en mercancías y
   títulos (lo que anotaron los cronistas), mudo en el oficio diario — peces
   por especie, médano, marea, cardumen. Si ese vocabulario sobrevivió, está
   fosilizado en el habla regional.

## ⚠️ El marco: sustrato indígena SIN filiación presunta

Paraguaná no era étnicamente homogénea y hoy eso se discute abiertamente. El
propio repo lo mide: [[esteves-1989]] reparte la toponimia peninsular en
**nueve estratos** (caquetío, taíno/caribe insular, cumanagoto, papiamento…),
y el lexicón ya separa `kalinago`, `jirajaroide-contacto`, etc.

**Ninguna voz de este libro entra como caquetía por defecto.** La cadena es:

```
paraguanerismo → ¿sustrato indígena? → ¿de cuál estrato? → etiqueta
```

y la evaluación de estrato usa el score de factibilidad del protocolo:
cognados en las comparandas (wayuunaiki, lokono, añú), fonotáctica (débil —
#91), atestación previa en el repo, referente ecológico del Golfete, y los
estratos toponímicos de Esteves como mapa de fondo.

## El método de entrada: dictado curado por Miguel

Miguel lee el ejemplar físico y dicta **las voces que su ojo de paraguanero
señala como posible herencia indígena**. Esa criba ES la marca
`retro-abstraido` — intuición informada local. Disciplinas acordadas:

1. **Página siempre** — sin página no hay cita, y sin cita no entra (regla 8).
2. **Glosa del libro tal cual**, corta y textual; el comentario de Miguel va
   aparte. Lo citable es Medina Colina, no la paráfrasis.
3. **Cobertura declarada**: al cerrar cada letra/sección, cuántas voces se
   vieron y cuántas se sacaron ("A: ~120 vistas, 9 dictadas"). Un futuro
   lector tiene que poder distinguir "no hay sustrato" de "no se miró"
   (regla 6).
4. **Colar dudosas**, no solo seguras: calibran el filtro.

### Formato de captura (una entrada)

```yaml
- voz: <forma tal como la escribe Medina Colina>
  glosa_libro: "<textual, corta>"
  pagina: <n>
  campo: <mar / fauna / flora / cuerpo / oficio / casa / clima / otro>
  nota_miguel: "<por qué le suena indígena; opcional>"
  dudosa: <true si va como calibración>
```

Las entradas se acumulan en la propuesta (`lexicon_medina_colina` o el YAML de
la bandeja cuando exista) — **nunca directo al lexicón** (regla 5).

## Qué se hace con cada voz dictada

1. Cruce contra lo que ya hay (lexicón activo, cognados, topónimos, propuestas)
   — como se hizo con la Tabla A-9: la mayoría de lo bueno suele estar ya, y
   entonces la voz vale como **atestación regional viva**, que también suma.
2. Score de factibilidad del protocolo → estrato más probable o "sin filiación".
3. Salida: propuesta con etiqueta (nunca mejor que `hipotetico` desde esta
   fuente sola) o hueco/descarte anotado aquí.

## La ficha y el prefacio (dictados el 2026-09-01)

**Juan B. Medina Colina, *Del Habla Paraguanera. Siglo XX*, 2ª ed. ampliada y
corregida, 2013.** Diseño editorial Maribel Ovalles Miranda; impresión
Editorial Miranda. Prefacio de **Guillermo de León Calles**, compañero de
bachillerato del autor. La 1ª edición (año no dictado) recibió mención
honorífica del Centro Nacional del Libro. Registro completo, con las citas
marcadas `segun_dictado` hasta cotejarlas con el papel:
`6-fusion/medina_colina_dictado.yaml` §ficha y §prefacio.

Lo que el prefacio dice **del método**, y lo que eso cambia aquí:

1. **Cuaderno de un hablante nativo, durante décadas**, con transmisión oral
   de sus ascendientes. No es encuesta con informantes; el prefacio no
   nombra pueblos ni décadas. Es la fuente `retro-abstraido` canónica, tal
   cual la esperaba el protocolo.
2. **El marco etimológico del prefacista no contempla sustrato indígena**:
   habla de creación lugareña, herencia hispánica directa y «fusiones creadas
   por la debilidad misma de sus respectivas pronunciaciones». Ni indígena,
   ni papiamento, ni neerlandés. Consecuencia: **la criba indígena es de
   Miguel, no del libro** — que el libro no marque una voz no le resta; si el
   autor marca origen en alguna entrada, eso se captura aparte
   (`origen_libro`) como atestación suya.
3. Pendiente de preguntar al pasar: si las entradas llevan marca de origen o
   de distribución, y el año de la 1ª edición.

## Las «Aclaratorias al lector» del autor (dictadas el 2026-09-01)

La nota de método del propio Medina Colina. Registro completo en
`6-fusion/medina_colina_dictado.yaml` §aclaratorias_al_lector; lo que cambia
en el protocolo:

1. **El filtro 2 (papiamento/neerlandés) pasa al primer puesto, por boca del
   autor.** Hasta los años 50 la península no tenía carretera a Coro; se
   comunicaba por goletas desde Adícora con Aruba, Curazao, Cuba, Santo
   Domingo y Puerto Rico — *horas* a las islas cercanas, *más de siete días*
   a Maracaibo. Toda voz «rara» tiene a las islas como primer sospechoso.
2. **Los canales del léxico, según el autor, son dos: arrieros (Coro) y
   marinos (Antillas).** Su marco es el del prefacista — español culto
   deformado por un pueblo analfabeto — y declara los patrones: supresión de
   letras en la primera o la última sílaba, cambio de letras. Eso es el
   filtro 1 con instrucciones: **antes de pasar una voz al cruce indígena,
   probar la restitución castellana** (¿es una palabra con la primera sílaba
   comida?). El sustrato indígena no está entre sus canales: la criba es de
   Miguel.
3. **La distribución la formula él en tres niveles** — «la mayoría son
   comunes en otras regiones del país, algunos solo se escucharon en Falcón,
   y los menos son autóctonos de la península» — con polisemia entre
   Paraguaná, el resto de Falcón, Lara y Trujillo. Es el criterio positivo 2
   del protocolo dicho por la fuente; si marca por entrada, se captura
   (`distribucion_libro`).
4. **Grafía fonética**: «escritos fonéticamente, tal cual como lo pronuncia
   nuestra gente». La `voz` se conserva tal cual (es la `forma_fuente`) y el
   cruce va por esqueleto fonémico.

Y alimenta la esfera **mundo** (regla 7): la lista de pueblos de Paraguaná
c. 1900-1950 con su escala (ninguno de 2.000 habitantes; Carirubana, menos de
200 hasta 1926) para la campaña de topónimos y `asentamientos.yaml` (época
s. XX), y el eje marítimo península–ABC como constante estructural — el mismo
de la ruta Cumarebo–Curazao del s. XVI, sin proyectarlo al precontacto (regla
3). Los anexos traen **más de doscientos refranes**: segunda veta, aparte.

## Idea de Miguel (2026-09-01): un transcriptor de dictado

*«Ver cómo trabajamos un transcriptor donde yo pueda ir leyéndote.»* Hoy el
dictado entra por reconocimiento de voz al chat y el escriba lo estructura; las
erratas de oído («del agua» por «del habla») se corrigen a mano y las citas
quedan `segun_dictado` hasta cotejarlas. Un transcriptor con estructura
(voz / glosa / página, con deletreo para las glosas) ahorraría el cotejo.
Queda anotado como idea; si el dictado rinde, merece issue.

## Lo minado hasta ahora

- **2026-09-01** — sesión de dictado iniciada: ficha y prefacio registrados.
  Voces: ver `6-fusion/medina_colina_dictado.yaml` §entradas y §cobertura
  (se actualiza al cerrar cada letra).

## Estado al cierre del dictado (2026-09-08)

Miguel cerró el dictado el 2026-09-08: «ya terminamos el libro, o al menos las
palabras que yo pensé eran caquetías». El registro
(`6-fusion/medina_colina_dictado.yaml`) queda con **177 voces** y el
veredicto del protocolo §5 en cada una: A 20 · B 11 · C 34 · D 112. La
cobertura por letra está declarada en el YAML (E y F sin declarar: el dictado
saltó de la p. 95 a la 127). Las sesiones fueron tres: 2026-09-01 (A-D y G,
ficha, prefacio, aclaratorias), 2026-09-07 (G-H) y 2026-09-08 (I-Z y los
apellidos de la p. 328).

Lo que el libro dio, en corto: veinte A que son atestaciones vivas de voces
que el lexicón ya tenía por Zavala (sibidigua con su saludo, tara como
saltamontes —la segunda fuente de #45—, poporo, yabo, tuturuto…); once B, de
las que cinco son **candidatas al lexicón** (urupagua, budare, maba, isicagua,
totocoro); treinta y ocho C para el corpus cultural (el racimo de la miel, los
frijoles, los cactus, las palomas); y ciento ocho D que dejan datos de mundo
(mc-mundo-013…029), dos isoglosas intrapeninsulares (gualamo/bisure,
siguato) y la lista de sustituciones léxicas (onoto por bariki, zamuro por
curumu). Tres topónimos entraron al canon por esta vía (Guarataro, Guatacare,
Guayacanal).

**Lo que sigue** (decidido con Miguel el 2026-09-08, puntos 1 y 2): segunda
fuente para las C en lo que el repo ya tiene a texto completo (Alvarado ya
pasado: doce hallazgos; luego Perea Alonso 1942, Jahn, Arcaya, Antolínez,
Brinton, Gatschet, van Buurt, Oliver cap. 2), y los diccionarios que faltan
(Captain & Captain 2005 para el wayuu, de Goeje 1928 y Bennett 1989 para el
lokono, Tamayo 1977 para el léxico popular).

**Deuda**: las páginas de la I a la M (dictadas sin página), la de
debudeque y dividive, y si E y F se miraron.

## El nivel C, aplicado al corpus (2026-09-12)

Las 33 voces de nivel C que Miguel falló entre el 10 y el 11 de septiembre
(`6-fusion/issues-pendientes/fallo-miguel-nivel-C-medina.md`) ya están en el
corpus cultural: **31 en `ecologia.yaml`** (flora, fauna, oficio y casa —
incluida `tapirama`, que Miguel añadió de su memoria) y **1 en
`creencia.yaml`** (`seretón`). Todas `hipotetico`, ninguna en el lexicón
activo, cada una con su página, su «por qué C» y el límite de la regla 3
escrito al lado. Lo aplicó `6-fusion/scripts/fusionar_nivel_c_medina.py`;
`chamaco` quedó fuera por el silencio de Alvarado. Seis siguen sin página
(guarero, igüira, mebi, debudeque, guarupepe, machire): están marcadas.

## Enlaces

[[02_protocolo_habla_paraguanera]] · [[esteves-1989]] ·
[[oliver-1989-apendice-a]] · [[metodo-comparativo]] · [[lexicon]]

<!-- CORROBORACIONES-MEDINA -->

### Lo que el dictado corroboró (nivel A, 2026-09)

Estas voces **ya estaban en el canon**: lo que el dictado añade es una
atestación viva del siglo XX y, en varias, el uso. Es el rendimiento real
de la sesión — no vocabulario nuevo, sino entradas que pasan de una fuente
a dos o tres independientes. Las notas del lexicón NO se tocan: catorce de
estas entradas viven en `lexicon_zavala.py`, que es generado.

| Voz dictada | Lema en el canon | Glosa del canon | p. Medina | Lo que dice Medina |
|---|---|---|---|---|
| bisure | `bisure` | lagartija | 130 | [por la entrada gualamo] lagarto; el nombre general en Paraguaná del reptil que en Tacuato y Santa Ana llaman gualamo |
| buche | `buche` | planta xerofita, melocato, cardo globoso, rastrero | 49-50 | es la palabra académica y nuestro pueblo la utilizó en algunas de sus acepciones. En las aves, bolsa formada por el esófago en la que los alimentos pe |
| cachicamo | `kachikamo` | armadillo (Dasypus novemcinctus) | 57 | así denominaron nuestros viejos al animal conocido en otras latitudes como armadillo. |
| cacuro | `kakuro` | pequeña avispa negra | 57 | con este nombre nuestros viejos denominaron a la conocida avispa, y por ser esta muy agresiva cuando se molestaba, por lo general llamaban así a la pe |
| caseto | `kaseto` | planta herbácea | 65 | planta silvestre en nuestros montes, de una altura de no más de dos metros, de ninguna utilidad para el campesino. |
| caujaro | `kaujaro` | árbol de madera blanda, fruta mucilaginosa, del género cordi | 65 | arbusto común en nuestros montes, de fruto comestible y de agradable sabor. |
| chiriguare | `chiriware` | gavilán, ave rapaz grande | — | es un ave de rapiña, de mayor envergadura que el gavilán [dictado: «el rapiño»], casi del tamaño de un zamuro. Era muy temido por los criadores de gal |
| chuchube | `chuchube` | paraulata | 74 | nombre inventado por nuestros viejos para identificar al pájaro que en otras regiones del país conocen con el nombre de paraulata. |
| dara | `dara` | alcaraván | 89 | con este nombre nominó nuestra gente al ave común en nuestros campos y que el resto del país conoce como alcaraván. |
| guacoa | `wakoa` | paloma | 129-130 | fue paloma silvestre en épocas pasadas, muy abundante en nuestro monte, hoy casi extinta. |
| guairón | `wairon` | hoguera | 130 | con este nombre se denominaron los hornos rústicos que se hacían en tierra para calcinar [dictado: «que marcara cuáles»; cotejar] piedras y fabricar c |
| poporo | `poporo` | maza-porra, arma de combate ceremonial | 230 | así denominaron nuestros viejos a la hinchazón propia de aquel que se había golpeado |
| saruro | `saruro` | boa, serpiente no venenosa | 41 | [bajo la entrada «bajear»] la serpiente que en otros lugares del país denominan tragavenados, nuestra gente la conoció como saruro. |
| sibidigua | `sibidiwa` | arbusto euforbiaceo. Jatrofa Gossy Pifolia | 263 | es planta silvestre de aplicación medicinal; aún se encuentra en nuestros escasos montes. Es palabra popular: entre los años 50 y 80 fue frecuente esc |
| tara | `tara` | langosta; tambien mariposa, polilla | 272 | [primera acepción, académica: tara, defecto o enfermedad hereditaria — dictado confuso]; para nuestros paraguaneros, todos los saltamontes y animales  |
| yabo | `yabo` | cercidium Virid. Arbol resinoso | 305 | árbol de madera dura, propio para hacer trompos y elaborar lejía |
