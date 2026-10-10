---
tipo: sesion
fecha: 2026-10-09
pueblo: taino
quien: 'minero taíno de la minería 2 (Claude Opus 5.5), rama vault/hermanas-taino'
plan: 08_creencia_taino_que-minar
propuesta: 6-fusion/hermanas_taino_2026-10-09.yaml
descripcion: "Las cinco esferas de lo taíno minadas en el esquema de las hermanas: la desecación del cacique tiene primaria (Colón cap. LXI), Ulloa corrige tres lecturas de la retraducción, y la sucesión por el hijo de la hermana tiene dos testigos que no dicen lo mismo."
---

# Las esferas de lo taíno (minería 2)

> Plan: [[08_creencia_taino_que-minar]] · Minería 1: [[09_creencia_taino_mineria]] · Esquema: `3-mundo/hermanas/README.md`
> Mapas: [[mapa-familia]] · [[mapa-geografia-politica]] · [[mapa-creencia]] · [[mapa-ecologia]] · [[mapa-transmision]]
> Fichas leídas: [[colon-hernando-1892]] · [[ulloa-1571]] · [[bourne-1906]] · [[oviedo-y-valdes-1851]] · [[las-casas-apologetica]] · [[angleria-1892]] · [[pane-c1498]] · [[steward-1948-hsai-4]] · [[jahn-1927]]
> Propuesta: `6-fusion/hermanas_taino_2026-10-09.yaml` · Cuentas: `python curiana_sim/compilar_hermanas.py`

**En una frase.** Lo que la minería 1 no encontraba estaba en la página de
Colón que precede a Pané: el cacique se desecaba al fuego «para que se conserve
entero», y esa página explica también de dónde salen todas las frases de Rouse
que no tenían primaria; en lo social, las primarias dan rango con nombre
(nitaínos, tres tratamientos), un señor con arbitrio, poliginia del señor y dos
reglas de sucesión que no coinciden.

## 1. Método

- **El encargo:** la lista de temas del README §4, preguntada a cada fuente.
  Lo que no dio nada va a `meta.ceros` con su sonda.
- **El orden:** primero lo que la minería 1 dejó pendiente para las fuentes
  nuevas, después parentesco y geografía política, después lo demás.
- **Cómo se leyó:** se localiza en la capa de texto y se cita desde la imagen
  (pymupdf, recortes de 130-170 ppp). Las Casas se extrajo **por columnas**,
  porque pdftotext entrelaza las dos. En Ulloa la ſ larga y los `Cimi` rotos
  obligan a ver la página.
- **Los desfases**, comprobados en la cabecera: Colón 1892 vol. 1, impresa =
  pdf − 12; Oviedo t. I copia íntegra, impresa = pdf − 120 en los libros V-VII;
  Las Casas, pdf − 14; Ulloa, ver §4.
- **La etiqueta:** dentro de la hermana todo sale `atestiguado`, porque todo
  tiene primaria con página; la capa que importa es `proyeccion.capa`, con la
  regla C de Miguel. Cuántos hechos hay por esfera y por capa lo imprime
  `compilar_hermanas.py` (regla 1).

## 2. Lo más fuerte, por esfera

### Parentesco

1. **Dos reglas de sucesión, de dos testigos que no se copian.** Las Casas:
   suceden «no los hijos de los señores, sino los de sus hermanas», por la
   certeza de la maternidad, y confiesa «del todo punto no lo penetramos» (p.
   521, imagen). Oviedo, «de muchos informado»: hereda el hijo mayor, y sólo si
   éste muere sin hijos pasa «al hijo ó hija de su hermana» (p. 136, imagen).
   El núcleo —el hijo de la hermana puede heredar el señorío— tiene primaria
   taína y el wayuu de Jahn (pp. 171-172) al lado: `reconstruido`
   (taino-parentesco-001). La forma exclusiva de parentesco-004 («no a su
   propio hijo»), no. Y la **razón** es la misma en Las Casas y en Jahn, pero
   Las Casas la da también para Panamá: es un lugar común y no cuenta.
2. **La poliginia es del señor.** Pané (Ulloa f. 145v), Oviedo (p. 133) y Las
   Casas (p. 521), tres testigos: el común una mujer, el señor muchas
   (taino-parentesco-004).
3. **Ni linaje, ni clan, ni residencia.** Cero en todas las primarias (§3). La
   exogamia de clan (parentesco-008) y la residencia avunculocal
   (parentesco-026) no tienen par taíno de primera mano: el incesto se define
   por grados (madre, hija, hermana; Las Casas añade la prima hermana).

### Geografía política

1. **Rango con nombre.** Nitaínos, «nobles y principales», y tres
   tratamientos por grado —Guaoxerí, Baharí, Matunherí— (Las Casas p. 516,
   imagen; taino-geografia_politica-002).
2. **El señor manda sin ley.** «Manu regia … sin leyes» (Las Casas p. 520); el
   cacique decide si al enfermo grave se lo ahoga (Colón p. 280); en los
   Lucayos, «teníase por ley el arbitrio del cacique» y el rey reparte la
   cosecha (Anglería vol. 4 pp. 79-80).
3. **El señorío se gana también.** Caonabó, lucayo, «llegó á ser rey» por sus
   hechos (Las Casas p. 515); y Anacaona manda tanto como su hermano y después
   de él.
4. **La guerra tiene tres causas**: caza y pesca en términos ajenos, y la
   alianza matrimonial rota (Las Casas p. 520).

### Creencia (nueva, de las fuentes nuevas)

1. **La desecación del cacique taíno tiene primaria:** «Abren al Cacique y le
   secan al fuego, para que se conserve entero» (Colón 1892 vol. 1 p. 279;
   Ulloa f. 126r, imagen). Es relato de Colón, no de Pané. Con la efigie, el
   paralelo r3 de Steward pasa a «imagen + desecación» en las dos orillas; el
   destino sigue siendo el contrario: el taíno conserva, el caquetío quema y
   bebe (taino-creencia-101).
2. **Cinco destinos del muerto en una página**, entre ellos quemar la casa con
   el muerto dentro: «nadie quema el cuerpo» (ct-t02) no se sostiene.
3. **La estatua de la carta de Colón lleva nombre, no huesos.** Los huesos los
   pone Las Casas al resumirla (p. 321 frente a Colón pp. 277-278 y Ulloa f.
   125r).
4. **El Coaibai no está «en un extremo».** Ulloa: «in una banda dell'Isola»;
   y Caonabó, en Colón, pone el valle de los muertos en la tierra de cada
   cacique. El núcleo de creencia-009 queda con dos tradiciones; el contraste
   «extremo frente a abajo» cae del lado taíno.

### Transmisión

1. **La ley en canciones, aprendida desde niños por los principales**: «hanno
   la lor legge ridotta in Canzoni antiche; per le quali si reggono … i quali
   da fanciulli imparano» (Ulloa f. 133v, imagen; taino-transmision-001).
2. **El areito como historia**, con guía y corro, genealogías y temporales,
   «fixamente esculpidas en la memoria» (Oviedo pp. 127-128).
3. **Canto de trabajo de las mujeres** que rallan yuca, y baile por sexos (Las
   Casas p. 538).

### Ecología

Lo leído confirma técnicas (canoa de un tronco, siembra de maíz en ala, sal
cociendo agua de mar, pesca con anzuelo de hueso) y añade una creencia de
calendario: se siembra «al prinçipio de la luna» (Oviedo p. 265). Ninguna se
proyecta: la ecología de La Española no es la del cardonal.

## 3. Lo que no salió (con su sonda)

Sondas sobre Oviedo t. I pdf 240-399, Las Casas pp. 320-325, 444-448 y
514-540, Pané-Wikisource y Colón 1892 cap. LXI + Pané I-XVII; las mide
`python 6-fusion/scripts/sondas_hermanas_taino.py`, que imprime el contexto
de cada coincidencia (las que no son taínas se descartan leyéndolas):

- **Residencia:** cero. Ni la avunculocal de Keegan (parentesco-026) ni la
  patrilocal de Rouse tienen primaria.
- **Linaje, clan, parcialidad:** cero taíno.
- **Sociedades de hombres:** cero taíno.
- **Formación del behique:** cero. Lo que hay de aprendizaje es el de los
  principales que aprenden a cantar desde niños.
- **Tributo precolombino en La Española:** sólo la sospecha de Colón.
- **`nitay-` y `nabor-` en Colón 1892 vol. 1:** cero; el vol. 1 no habla de
  jerarquía.

## 4. Correcciones que deja

- **Ulloa trueca hojas.** pdf 293 = f. 123 y pdf 295 = f. 126, en imagen; la
  fórmula (pdf − 45)/2 sólo vale desde el pdf 299. La ficha [[ulloa-1571]]
  lo explica.
- **El vol. 1 de Colón 1892 sí trae Pané I-XVII.**
- **Colón 1892 traduce mal** «lo spirito» y «da fanciulli»; para Pané manda
  Ulloa.
- **Las «cestas» de Rouse son caribes** (Guadalupe, Colón p. 209).

## 5. La Vía A, auditada en las cinco esferas

Una línea por hecho wayuu (`fuente: reconstruido` con comparanda wayuu) que
lo taíno toca. Lo que la minería 1 ya auditó en creencia se cita, no se
repite.

| id | Esfera | Veredicto | Lo taíno que lo decide |
|---|---|---|---|
| parentesco-004 | parentesco | **corrobora en parte** | el hijo de la hermana hereda (Las Casas p. 521), pero para Oviedo va después del hijo (p. 136) |
| parentesco-005 | parentesco | **corrobora en parte** | herencia del señorío por la hermana; nombre y linaje maternos: cero |
| parentesco-006 | parentesco | **matiza** | la sucesión es del señorío, no autoridad doméstica del tío; ninguna primaria taína la da |
| parentesco-008 | parentesco | **matiza** | la prohibición taína es por grados, no por clan |
| parentesco-009, 010, 011 | parentesco | **no toca** | levirato, insulto al muerto, términos de tío: cero |
| creencia-009 | creencia | **corrobora** | Coaibai (Ulloa) y el valle de Caonabó (Colón): segunda tradición; sin «extremo» |
| creencia-010d | creencia | **contradice** | el cacique se deseca para conservarlo entero; la estatua lleva nombre |
| creencia-008 | creencia | **corrobora en parte** | el goeiz que se aparece de noche (Ulloa f. 133r); ya en ct-t04 |
| creencia-005, 011, 014 | creencia | **no toca** | ni sueño, ni manipulador de huesos, ni calendario de dos estaciones (sólo la luna de siembra) |
| creencia-002, 003, 006, 007, 012 | creencia | sin cambio | la minería 1 (09 §Auditoría) |
| transmision-016 | transmisión | **corrobora en parte** | memoria cantada sí, pero de los principales y aprendida desde niños |
| transmision-017 | transmisión | **no toca** | cómo se hace un buhuitihu: cero |
| transmision-034 | transmisión | **corrobora en parte / matiza** | la hermana antillana es cacicazgo con arbitrio; pero el señor de Marien habla por boca de dos viejos |
| geografia_politica-025 | geografía política | **corrobora en parte** | la gente se llama como su tierra (Aiti); el mar, no |

**Lo que sube:** el núcleo de parentesco-004 (con primaria taína) y
creencia-009 (con un segundo testigo taíno). **Lo que baja:** la forma
exclusiva de la sucesión avuncular y todo lo de clan y residencia, que en lo
taíno sólo tiene tercera mano. **Lo que se confirma por contraste:** la
disolución del muerto (creencia-010d) no es arahuaca general.

## Decisiones para Miguel

- **D-h1 — Las capas de proyección.** `reconstruido` para taino-parentesco-001
  (el hijo de la hermana puede heredar) y taino-creencia-105 (la tierra de
  los muertos con nombre). El resto, `lectura`, `hipotetico` o `no-proyecta`
  como dice cada hecho; la cuenta, `compilar_hermanas.py`.
- **D-h2 — parentesco-004 y parentesco-026.** ¿Se reescribe 004 sin el «no a
  su propio hijo», que Oviedo contradice? ¿Y 026, que sólo tiene a Keegan sin
  leer, baja a `hipotetico`? En duda, degradar.
- **D-h3 — Corregir la minería 1 al fusionar:** ct-t02 («nadie quema el
  cuerpo»), ct-t05 («en un extremo») y ct-t01 (los huesos en la estatua) según
  `mineria_1_nota` de taino-creencia-101, 102, 103 y 105.
- **D-h4 — La foliación de Ulloa** y los dos datos de Colón 1892 vol. 1 en sus
  fichas: ya escritos, sólo confirmar.
- **D-h5 — Lo que falta:** la *Historia de las Indias* de Las Casas en la parte
  de La Española y los vols. 2-3 de Anglería, si se quieren los señores con
  nombre y fecha (descargar lo decide Miguel).
