---
tipo: revision
fecha: 2026-09-12
encargo_de_miguel: >-
  «Hacer una revisión de todo nuestro proyecto para revisar que no tengamos
  ningún agujero previo a la era 2.»
sustituye_en_parte_a: HANDOFF_2026-09-11.md
---

# Revisión pre-era 2 — 2026-09-12

> **Cómo se midió.** Todo lo que lleva número sale de correr, hoy:
> `guardianes.py` (9 en verde), `generar_tablero.py --gh`, `curiana_fonotactica.py`,
> y cuatro mediciones ad hoc que se citan donde tocan. **No copiar cifras de
> aquí a otro sitio**: las del tablero envejecen con cada commit; las ad hoc
> son de hoy.

## 0. Lo que esta sesión cerró antes de revisar

| Qué | Commit | Efecto medido |
|---|---|---|
| El verbo de Perea (pp. 609-684): 239 verbos de Schumann 1755, 218 fusionados | `e1aa50f` | lexicón 1.676 → 1.894; wayuu:lokono de 1,7:1 a **1,2:1** |
| El filtro fonotáctico leía mal a Perea (`ù` borrada, geminadas) | `e1aa50f` | lokono pasa del 64 % al 86 %; wayuu sigue en 65 % |
| F8, parte taíno: 9 formas generadas por regla re-etiquetadas `taíno-reconstruido` | `032e5f4` | el taíno atestiguado pasa al 98 %; el reconstruido al 78 % |
| El fallo del nivel C, aplicado: 32 voces de Medina al corpus | `1395163` | corpus 166 → **198 hechos**, 0 errores |

La rama `feat/perea-fase1-d11-y-flecos` va por 14 commits sobre `main`, empujada, sin PR.

## 1. El gate, hoy

7 🟢 · 1 🔴 · 2 ⚪. La roja es la 8 (D11 #39) y está roja **porque el issue
sigue abierto**, no por trabajo: el ratio es 1,2 a 1 y la fase 1 entera está
en el habla. Las ⚪ son F10 (muestreo humano de citas) y el exportador (#42),
que sólo se miden corriéndolos.

## 2. Los agujeros, medidos y ordenados por lo que bloquean

### A · Lo que la era 2 usa directamente

**A1 · Los clanes están invertidos respecto a Oliver, y ahora está medido.**
[[DISENO_ERA2]] §2 lo dejó «EN VERIFICACIÓN». Oliver cap. 3 p. 275 (vía
González Batista): *Amuayes* = SUR, *Guaranaos* = NORTE. El barrido OSM
(`6-fusion/toponimos_mapa_kaketiana.yaml`) da **Amuay 11,775 N / Guaranao
11,675 N**: el homónimo moderno de los Amuayes está **11 km al norte** del de
los Guaranaos. Y Delmonte 1883 sitúa a los Amuayes reasentados en **Moruy**
(11,822 N), más al norte todavía. Los topónimos modernos y los territorios
de Oliver no coinciden. **Decisión de Miguel antes de sembrar los nodos**:
qué manda, el territorio de la fuente o el nombre del mapa. No es chico:
sembrar al revés invierte las isoglosas de A3.

**A2 · El exportador (#42) sigue sin verificar.** `export_runs_index.py`
lee `total_turns` de `simulation_runs` en vez de contar turnos; es coherente
con el síntoma conocido («0 turnos con 290 respuestas»). Sólo se cierra
corriendo un export contra la base. Es la condición 9 del gate.

**A3 · Las semillas léxicas por nodo existen, pero seis no tienen página.**
Las isoglosas del dictado (`gualamo`/`bisure`, `siguato`) están; del nivel C
recién fusionado, `guarero`, `igüira`, `mebi`, `debudeque`, `guarupepe` y
`machire` entraron con «página no dictada (⚠️ pendiente)». Y el dictado
entero tiene **43** voces con `pagina: null`. Trabajo de Miguel con el libro
en la mano.

**A4 · Repertorio o filiación (#119): sin decidir.** Sigue siendo el punto 3
de SIGUIENTE_TANDA §A. Sin esa línea, el run 1 se mide con una vara que
después puede parecer equivocada.

### B · El lexicón

**B1 · 🔴 La categoría gramatical de la columna wayuu es ficticia.** Medido
hoy sobre `VOCABULARIO_BASE`: de 769 entradas wayuunaiki, **764 son `sust`**
y 5 `num`; **193** tienen por glosa un infinitivo castellano (`aa'inmajaa`
'cuidar', `ajütaa` 'enviar'…). En lokono, **39** más, casi todas de la tabla
A-2 de Oliver y de Pet (`andyn`, `bokon`, `aparrun`). Consecuencia: cualquier
cruce **por categoría** —que es lo primero que pide una retroabstracción
(«dame los verbos de las tres comparandas para este concepto»)— es imposible
sin re-etiquetar. Es la columna que D11 jubiló, así que puede que no valga
la pena arreglarla entera; pero hay que saberlo antes de contar con ella.

**B2 · F8: quedan 23 valores de `fuente`** sin conjunto canónico declarado
(`lokono/proto-arawakan` 14, `lokono/garifuna` 13, `wayunaiki-cogn` 7,
`kalinago-caribe-overlay` 4, `caquetío-hipotético/topónimo` 1…). La parte
taíno se hizo hoy. El resto es una tarde, pero es una tarde de decidir, no
de programar: cada valor raro es una etiqueta epistémica que alguien puso
por algo.

**B3 · La columna lokono mezcla cinco estratos sin campo que lo diga.**
Schumann 1755 (Perea), Schultz 1802 (Perea), Brinton 1871, Goeje 1928, Pet
1987, Oliver A-2. Hoy se sabe por `notas`. Medido de paso: «rojo» es `cule-n`
en 1755 y `roodi` en 1928; «negro», `caii-me-n` / `siwi`; «yuca», `calli` /
`yuka`. Para cruzar con el caquetío colonial (s. XVI) el estrato importa, y
un campo `estrato` (o un `procedencia.obra` en el lexicón, que hoy no existe)
lo haría medible.

**B4 · D11 fase 3: el núcleo del habla sigue siendo wayuu.** Pronombres,
numerales y las tres marcas de aspecto (`-ka`/`-ni`/`-da`) están
re-etiquetadas pero son wayuu letra por letra
(`decision-d11-el-nucleo-reconstruido-del-wayuu.md`). Con el verbo de Perea
vaciado, el lokono tiene ahora paradigma pronominal completo y futuro `-pa`
para re-derivar si se decide (salidas 2 o 3). No es agujero: es decisión.

**B5 · Menudencias medidas.** `cognado-016` y `cognado-019` son el mismo
«mar» (`*para`) en dos fichas. Cuatro correspondencias de Jahn, dos
topónimos del barrido web y una entrada de Alvarado siguen «sin ver en
imagen» (grep en los tres YAML). Ninguna toca el canon.

### C · Las fuentes

**C1 · 13 obras `no-disponible`, cuatro de prioridad alta:**
`arcaya-obra-inedita-1995`, `federmann-1916`, `oviedo-y-valdes-1851`,
`perez-de-tolosa-1546`. Federmann es la fuente del `Ceretón` que hoy está en
el corpus por una mención de segunda mano (mi barrido); Pérez de Tolosa 1546
es la carta que ata el maíz de la sierra con Coro. Las dos son de las que
más se citan sin tenerse.

**C2 · Seis de prioridad alta a medias** (`parcial`): Esteves (los seis
tomos, con la campaña cerrada pero el glosario no agotado), Oliver apéndice
A, cap. 3-vecinos, cap. 4, Urbina Jiménez. Y cuatro `en-curso`: Brito
Figueroa, Castellanos, González Batista, OSM.

**C3 · Las comparandas que Miguel encargó — encontradas.**

| Obra | Dónde | Estado |
|---|---|---|
| ⭐⭐⭐ Neira y Ribero 1762, *Arte y vocabulario de la lengua achagua* | Real Biblioteca (RBPR II/2910, copia de 1788): **102 imágenes IIIF**, descarga PDF/ZIP desde la ficha; también Library of Congress (2021667801) | libre; **falta descargar** |
| ⭐⭐ Fabo 1911, *Idiomas y etnografía de la región oriental de Colombia* | archive.org `b24853616`: **PDF 11,4 MB + texto OCR 637 KB**, 306 pp. | libre; **falta descargar** |
| Pané, *Relación acerca de las antigüedades de los indios* | Wikisource / Ciudad Seva, texto completo | libre; **falta descargar** |
| Meléndez Lozano 1997, el estudio del *Arte* achagua | IAI Berlín (PDF tras verificación de navegador) / Dialnet (sin texto) | a mano |
| de Goeje 1928 | sólo reimpresión de pago (Cambridge, Lincom) y sitios pirata | **comprar** |
| Bennett 1989, Brett 1849 | catálogos (HathiTrust, U. Guyana); sin PDF | biblioteca o compra |
| Granberry & Vescelius 2004 | U. Alabama Press | **comprar** |

Descargar es decisión de Miguel (D8 #37 sigue abierta sobre si el repo
archiva copias). El orden que propongo: Fabo primero (tiene OCR: se mina en
una tarde y convierte la tabla de Jahn de transmisión en atestación), Neira
y Ribero después (manuscrito del XVIII: hay que leerlo en imagen, y son 102
páginas).

### D · El corpus y el tablero

**D1 · F10** (muestreo humano de 15-20 citas) sigue siendo de Miguel; ahora
son 198 hechos, todos con `referencia`.

**D2 · Siete borradores sin publicar** en `6-fusion/issues-pendientes/`:
dos comentarios para D11 (#39), uno para #45, las decisiones de Borojó, del
núcleo wayuu y de `era2-retroabstraido`, y el fallo del nivel C (ya aplicado;
va como registro). Regla 10: las decisiones viven en el tablero.

**D3 · Diez decisiones abiertas** en el tablero, cuatro de las cuales tocan
la era 2 directamente: D11 (#39), D14 (#83, la segunda polity), #119
(repertorio), y la de los clanes (A1), que aún no tiene issue.

## 3. Orden propuesto

1. **Miguel decide A1** (clanes) y **A4** (repertorio) — son de una línea cada
   una y sin ellas los nodos se siembran a ciegas.
2. **Miguel autoriza las descargas de C3** → Fabo se mina esa misma tarde
   (achagua, fase 2 de D11) → Neira y Ribero en imagen.
3. **B1** se decide, no se arregla: si la columna wayuu es comparanda
   jubilada, se declara y se deja; si se va a usar en la retroabstracción,
   se re-etiqueta por lote (193 + 39, con `notas` intactas).
4. **A2** (exportador) y **F10**: las dos ⚪ del gate. Chico y humano.
5. **B2** (F8 resto) y **B3** (`estrato`) antes de la retroabstracción, no
   antes del run 1.
6. **D2**: publicar los siete borradores. Y **cerrar D11** si 1,2 a 1 basta.

Lo que **no** es agujero aunque lo parezca: el tomo I de Perea está
agotado; el lexicón no tiene entradas caquetías sin cita; los 9 guardianes
están en verde; y el material de las isoglosas para los dos nodos existe y
está localizado.
