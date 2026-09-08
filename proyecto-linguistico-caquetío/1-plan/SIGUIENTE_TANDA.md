---
tipo: nota-viva
ambito: qué hacer a continuación, y con qué contexto arrancar en frío
preparado: 2026-08-31
tablero: TABLERO.md
bandeja: 6-fusion/BANDEJA.md
---

# Siguiente tanda

> **Para una sesión que arranca en frío.** Antes de nada:
> ```
> python curiana_sim/generar_tablero.py    # el canon, medido
> python curiana_sim/generar_bandeja.py    # la cola de fusión
> python curiana_sim/guardianes.py         # los 9 en verde antes de cerrar nada
> ```
> Los números de esta nota pueden haber envejecido. Los de los generados, no.

## Dónde estamos (2026-08-31)

La sesión del 25-31 de agosto fue la más grande del proyecto: **el gate pasó
de 2 a 5 condiciones en verde**. Miguel resolvió cinco decisiones —F1, D5
(entera), D9, #101 y #109— en una tanda formal cuyo registro completo, con la
evidencia de cada una, vive en `6-fusion/decisiones_tanda_2026-08-30.yaml`, y
que aplicó al canon `curiana_sim/aplicar_tanda_08_30.py` (idempotente, con
`--dry-run`; el patrón a seguir para futuras tandas).

Lo que cambió de fondo:

- **`-bana` = 'cerro, sitio alto', atestiguado** (D9 resuelta, seis apoyos).
  `-ana` quedó al revés: forma atestiguada, glosa 'lugar de' EN DISPUTA (#109
  abierto apuntando al censo de Esteves).
- **D5 decidida entera Y la fase 2 ejecutada** (2026-08-31): lema fonémico
  con `forma_fuente` en toda la familia caquetía — 31 renombres en el literal
  (`aplicar_fase2_d5.py`) y 80 en el generado (el miner de Zavala normaliza
  al emitir). Las colisiones se decidieron el mismo día (fusionar: la grafía
  española es grafía, el lema fonémico es la palabra) y 10 agentes se
  renombraron a grafía fonémica (`aplicar_colisiones_d5.py`). Queda el paso
  de normalización del pipeline de fusión (ver B.2).
- **La bibliografía pasó de 39 a 55 obras.** Entraron al repo con PDF: Morón
  2012 (petroglifos), Antolínez 1946 (*Hacia el indio y su mundo*), Velasco
  2015 (*Historia de una Resistencia*) y el texto de Castellanos ed. 1857.
- **Aparecieron los primeros PRIMARIOS del s. XVI**: las cartas de Ampíes
  (~1520) y Bastidas (1538) vía Velasco —Todariquiba, Hurihurebo, Myraca,
  Gorybacoa, y Manaure que "se haze adorar... dando a entender que el da los
  temporales"— y la **lista de las once ciudades** de Castellanos 1589
  (`6-fusion/castellanos_1589_toponimos.yaml`).
- **La única frase caquetía conocida estaba en el repo** sin que nadie la
  viera como frase: la fórmula de salutación de Mitare (Zavala p. 73, dos
  versiones). Su expediente: `6-fusion/frase_saludo_mitare.yaml`.
- **La campaña de topónimos de Falcón quedó montada**: bug de `forma`
  arreglado (glosa_fuente 27→51 de 74), índice de Esteves como cola (182 por
  procesar), esquema `lecturas` propuesto con la regla 0 de Miguel
  (significado ≠ referente).
- **Dos issues de método publicables**: repertorio-vs-filiación (el `caney`:
  el lexicón contesta filiación y lo usamos como uso) y esquema-lecturas.
- El colofón involuntario: **el caquetío atestiguado tiene CERO términos de
  color** (`6-fusion/colores_caquetios.yaml`) — objetivo de minería definido.

El gate hoy: **1 🟢 · 2 🟢 · 3 🟢 · 4 🟢 · 7 🟢** — faltan **6** (D1 y D3, sin
preparar), **8** (D11, espera la A-7), y las dos no automedibles (**5** el
muestreo F10 de Miguel, **9** el exportador #42).

---

## A · Lo que espera a Miguel (nada bloquea, todo suma)

1. **El muestreo F10** — verificar ~15-20 citas del corpus al azar (que la
   página exista y diga lo que el hecho afirma). Es la condición 5 del gate y
   es trabajo humano por definición.
2. ~~Publicar los borradores de `6-fusion/issues-pendientes/`~~ **hecho el
   2026-09-07**: #119 (repertorio vs. filiación), #120 (PDF tras aporte), el
   comentario de #109 (cerrado) y el de D14 (#83); el de lecturas se archivó
   como implementado. La cola de borradores está en cero.
3. **La decisión de una línea sobre repertorio** para el protocolo del run 1:
   *"el run 1 se mide contra filiación, como decisión de modelado declarada;
   repertorio queda para la era 2"* — o lo contrario. Sin esa línea, el run
   queda medido con una vara que después puede parecer equivocada.
4. **Compras físicas** (ver C).

## A-bis · El plan de arranque de la simulación (2026-09-08)

> Miguel preguntó qué falta para empezar a montar la simulación. Esto es la
> respuesta, medida contra el gate de `TABLERO.md` §4 y la ingeniería de
> [[DISENO_ERA2]] §8. **Nada de aquí es nuevo trabajo de investigación**: la
> minería que cerró el 2026-09-08 (Medina Colina, la campaña de topónimos,
> B.6) dejó el insumo puesto.

### Lo que bloquea el gate: tres cosas

| # | Qué | De quién | Tamaño |
|---|---|---|---|
| 8 | ~~**D11**~~ **DECIDIDA el 2026-09-08**: rebalancear hacia el eje lokono-taíno, con achagua más adelante (`6-fusion/decisiones_tanda_2026-09-08.yaml`). El gate se levanta cuando la **fase 1** esté aplicada, no al decidir | escriba: minar Perea Alonso 1942, ya en el repo y sin minar | medio |
| 5 | **F10** — muestreo de 15-20 citas del corpus al azar | **Miguel**: es trabajo humano por definición | una tarde |
| 9 | **El exportador** (`export_runs_index.py`, #42): exporta 0 turnos con 290 respuestas | escriba | chico |

Las otras seis condiciones están en verde y medidas. El re-export del sitio va
DESPUÉS del primer run limpio, nunca antes (PLAN_MAESTRO §6.4).

### Lo que la minería ya resolvió, y conviene no volver a comprar

- **Las semillas léxicas divergentes por nodo**, que [[DISENO_ERA2]] §1 declara
  condición de que los dos nodos no sean decorado, ya existen **atestiguadas**:
  las dos isoglosas intrapeninsulares del dictado — `gualamo`/`bisure` (Tacuato
  y Santa Ana frente al resto, mc-mundo-020) y `siguato` (oriente = el ánimo
  caído, occidente entre pescadores = el pescado pasado, mc-mundo-027). La
  segunda reparte además por OFICIO, que es justo el eje playa/conuco de los
  dos nodos.
- **La toponimia de los nodos con coordenadas**: 145 topónimos en canon y el
  barrido OSM (`6-fusion/toponimos_mapa_kaketiana.yaml`), con Moruy, Chamuriana,
  Cayerúa, Maitiruma y el Capubana localizados.
- **El registro de vecinos** (`3-mundo/etnias.yaml`, 9.º guardián) y la quinta
  polity (`occidental`, futura) para cuando el contacto salga de la península.

### El orden de arranque

1. **Arreglar el exportador** (escriba, chico). Desbloquea la condición 9 y es
   lo único del gate que no depende de Miguel.
2. **F10** (Miguel) y la **fase 1 de D11** (escriba: minar Perea Alonso 1942,
   926 pp. con texto, ya en el repo). Con eso el gate queda en verde.
3. **Verificar la asignación norte/sur de los clanes** ([[DISENO_ERA2]] §2 la
   marca EN VERIFICACIÓN: los homónimos modernos parecen invertidos respecto a
   Oliver). Ahora se puede: el barrido OSM tiene las coordenadas. Chico, y hay
   que hacerlo antes de sembrar los nodos o se siembran al revés.
4. **Un run corto de la era 1 con la base sellada**, para tener la vara contra
   la que leer la era 2 (protocolo `04_protocolo_run_1_era_auditada`).
5. **Las cuatro piezas chicas de la era 2**, en el orden que el propio diseño
   sugiere: modelo de costos → columna `nodo` en el esquema y pertenencia
   agente→nodo → semillas por nodo (las isoglosas de arriba) → métricas
   dentro/entre nodos con detector de meseta.
6. **Lo grande, después**: episodios serializables, diario por agente y el
   elenco nuevo desde los linajes. El elenco no es código, es curaduría con
   Miguel, y puede avanzar en paralelo desde el principio.

### Lo que este plan NO decide

Si el run 1 se mide contra filiación o contra repertorio (#119). Sin esa línea
escrita, el run queda medido con una vara que después puede parecer
equivocada — es el punto 3 de la sección A, y sigue esperando.

## B · La cola de trabajo, por rendimiento

### B.1 · La serie Swadesh de Oliver (A-1 a A-7)  ← **arrancada el 2026-08-31**

**Progreso**: no era una tabla, eran **siete** — A-1 es el vocabulario añú
completo de Wilbert (1958-59); **A-2 es LA tabla de D11**
(guajiro·paraujano·lokono·island-carib·maipure); A-3..A-7 cubren el resto de
la familia. Las filas clave están minadas por OCR (todas las páginas venían
giradas 90°; `--rotar auto` las salvó): ver
`6-fusion/tabla_a1_a7_swadesh.yaml`.

- ✅ **La fila 53 (liver) VERIFICÓ el cognado de `bana₂`** — lokono `ebana`,
  island-carib `*bana`, y la serie panarahuaca `*pana` entera.
- ✅ **El paraujano de 1958 ya decía SPANISH** en verde/amarillo/blanco/negro:
  la pérdida de los colores, documentada en el pariente costero más cercano.
- 🔴 **El tapir NO está** (el Swadesh-100 no lo trae): la ruta de `kama` se
  corrigió — candidatos: la A-1 completa, la fauna de van Buurt, Payne.

**La A-2 ya está transcrita entera y RINDE** (2026-08-31): el cómputo de D11
salió de ella, y el **primer incremento del rumbo de D11 está implementado**
— `minar_a2_swadesh.py` → `lexicon_a2.py` (generado E importado, como
zavala): **46 entradas paraujano** (la columna añú abrió — estaba en CERO) y
**48 lokono** nuevas. La categoría `paraujano` es canónica y el filtro
fonotáctico ya la mide: **73.9%, entre lokono (82.9%) y wayuu (65.4%)** — el
pariente costero más cercano pasa a tasa intermedia. 12 colisiones
registradas como dato areal (pia, biama, siba...). Tests en
`tests/test_d11_a2.py`.

✅ **La segunda pasada de Miguel sobre la A-2 está hecha (2026-09-01)**:
correcciones en el YAML (abonaba, -thina, cuatro «(?)» resueltos) que
liberaron tres entradas más (ithihi 'sangre', kougdo 'grasa') — el estado de
verificación vive en el meta de la transcripción y todas las notas del
módulo lo heredan al regenerar.

**Queda**: la extensión de la A-1 (hacia atrás de pdf 584) y su transcripción
completa — es EL vocabulario añú de Wilbert; la cabecera de la A-5; y la
escala diccionario del lokono (ver C: Pet 1987, Bennett 1989, de Goeje 1928 —
⚠️ NO están en el repo; candidato interno ya en `fuentes_caquetios/`:
**Perea Alonso 1942**, *Filología Comparada Arawak* Tomo I, sin minar).

### B.2 · Fase 2 de D5 — la migración de lemas ✅ ejecutada (2026-08-31)

Hecha en dos mitades: el **literal** (31 renombres, `aplicar_fase2_d5.py`,
mapa en `6-fusion/migracion_lemas_fase2.yaml`) y el **generado** (80
renombres: `minar_zavala_glosario.py` normaliza al emitir, casa por
`forma_fuente` — eso cerró de paso la fusión del #89 y dedupicó `barique`).
Los tests de fonotáctica ahora GUARDAN el estado decidido (lokono 79.3% >
wayuu 65.4% con la base entera migrada).

**Las colisiones se decidieron y aplicaron el mismo día** (Miguel: la grafía
española es grafía; el lema fonémico es la palabra; homónimos se declaran —
patrón D9): kati y kiba quedaron atestiguadas (kiba con la grafía k IMPRESA
en Zavala #92 «Cuiva. Kiba» de Arcaya), kanoa/hamaka reconstruidas, siwa con
homónimos declarados. Y los 10 agentes en grafía colonial se renombraron
(Buko, Chiriware, Korie-ko, Sha-korie...). Registro:
`6-fusion/decisiones_colisiones_d5_2026-08-31.yaml`; aplicador:
`aplicar_colisiones_d5.py`. **Lo que queda de B.2**:

- El **paso de normalización en el pipeline de fusión** (sin él, la BANDEJA
  reinyecta grafía colonial) y la wiki `/kaketiana` mostrando ambas formas.
- `naure` #185/#186 (dos glosas, mismo lema — no es colisión de grafías):
  sigue visible en `COLISIONES_D5` del generado.
- Los IDs de locación (`buco`, `conuco`) siguen en grafía vieja: etiquetas
  de registro, decisión aparte si se quiere.

### B.3 · Dossiers de D1 y D3 — la próxima tanda de decisiones

Prepararlas como se preparó D5: evidencia servida, opciones con contra, y
Miguel decide una por una. D1 = el veto de la genealogía propuesta (#32);
D3 = `normalizar_por_dialecto()`: cablearla o eliminarla (#34). Son lo único
que queda de la condición 6.

### B.4 · El exportador de runs (#42)

`export_runs_index.py` da 0 turnos para `20091e1f` con 290 respuestas.
Sesión técnica contra Supabase local (puertos 64321/64322). Condición 9.

### B.5 · La campaña de topónimos

La mesa de trabajo es `6-fusion/TOPONIMOS_POR_FUENTE.md` (generada por
`juntar_toponimos.py`, 2026-09-04): todos los topónimos que el proyecto ha
tocado, por obra, cruzados contra el canon, Esteves, los nodos y el mapa de
Miguel. Se regenera; no se edita. El protocolo completo es la skill
`campana-toponimos`. Lotes hechos: 1 (2026-09-06, los del mapa de Miguel en
Esteves, 15), 2 (2026-09-07, los «caribe insular», 4), 3 (las once ciudades de
Castellanos, 8 entradas nuevas) y 4 (los ocho del mapa «fuera de Esteves», que
estaban con otra grafía) y 5 (Moruy, Chamuriana y Adícora: los nodos de la era 2,
con las procedencias que les faltaban a las lecturas de Miguel). Siguientes, por
las dos vías de la skill §9: **el diccionario de Medina Colina** (cada sesión
de dictado cierra con `juntar_toponimos.py`; lo que quede ≡ sin ★ es el lote)
y el **barrido del mapa vivo de la Kaketiana** (lista con coordenadas por
región → cruce con la mesa → lo nuevo a la cola con deuda declarada). El resto del índice de Esteves, a su ritmo (la cuenta, en el propio índice).

~~Implementar `lecturas` en el esquema + `compilar_lengua.py`~~ (hecho el
2026-09-05, con `definicion_aceptada_simulacion`; ver datos-de-lengua.md); retro-poblar
las ~20 lecturas de la sesión (están en `toponimia_coro_espina.yaml`,
`lengua_toponimia_quibacoa.yaml`, `petroglifos_y_manaure.yaml`,
`velasco_primarios_agi.yaml`); y procesar la cola de 182 de
`toponimos_esteves_indice.yaml`, cruzada con las once ciudades de Castellanos
y los cinco de Bastidas. ~~La auditoría de tildes va aquí (es lo que
distinguiría `-ana` de `-aná` y decide #109).~~ Hecha el 2026-09-07 contra
Esteves y Zavala: tres correcciones (`paraguaná`, `caquetío`, `aburí`). Y el
censo de -ana en Esteves, mismo día: ninguna forma glosada 'lugar de'
(`6-fusion/censo_ana_esteves_109.yaml`; borrador de comentario en
`issues-pendientes/comentario-109-censo-ana-esteves.md`). **#109 decidido
(B, Miguel, mismo día)**: la glosa 'lugar de' se retira, `-ana` es
`morfema-011` sin glosa, la lista de -ana queda viva en el censo y Jayana
entra al canon (`toponimo-110`). Comentario publicado y #109 cerrado.

**Mismo día, tarde**: las lecturas del 25 de agosto están fusionadas (Miguel:
«que no quede nada pendiente por ahí sin guardar o fusionar»): `curiana` es
`toponimo-111` (C, seis lecturas: González Batista, Arcaya, Castellanos, la
hipótesis curi ~ juri, el Coria-na de Oliver), `quiquiba` se rehabilitó a C con
su id 034, `la cuiba` es `toponimo-112` (C), `capuhana` es `toponimo-113` (B, con
el centro sagrado de Miguel como lectura), los cuatro *Quicer-* son antropónimos
de Barquisimeto, y el cognado 'piedra' tiene CQ quiva. Y el **barrido del mapa
vivo** está hecho con OSM (`barrer_mapa.py`, `6-fusion/toponimos_mapa_kaketiana.yaml`,
ficha `osm-kaketiana`). Y el **lote 7** (mismo día, «dale, procésalo»): los 36
del barrido de Paraguaná procesados — Bariquí (B), trece C, cuatro descartados
de Esteves (Sisibauco era el «ilegible» del índice), siete del mapa sin fuente
con coordenadas, cuatro castellanos; ids 114-142. Índice de Esteves: 54 en
canon, 133 en cola. El dictado de Medina sigue en paralelo (debudeque C,
dividive D + mc-mundo-021; disey ya estaba).

### B.6 · Oliver §3.2.4 — los caribes ✅ (minado el 2026-09-07)

pp. impresas 223-230 = pdf 250-257. Respuesta en
`6-fusion/oliver_324_caribes.yaml`: los grupos de lengua caribe (bubure,
burede, pemeno, kirikire) están al sur y oeste de Maracaibo; el único contacto
con caquetíos son los enclaves de la esfera occidental en Juruara. **Paraguaná
no aparece** y ninguno de los cinco de Esteves tampoco (0/5, medido): el
«estrato caribe insular» es inferencia fonética suya, y la etiqueta nombra una
lengua arahuaca. Fusionado el mismo día por decisión de Miguel: los cinco hechos
son `geografia_politica-009..013`, los cuatro grupos están en `3-mundo/etnias.yaml`
(registro canon nuevo, con el caribe del elenco como canon-simulación), Amuay
resuelto a favor de la etnohistoria, Miraca es `nodo-031`.

### B.7 · Campañas grandes, cuando haya hueco

- **Auditoría del glosario de Zavala** entrada-por-entrada contra el lexicón
  (el #29 `bara` se había escapado de un minado "completo"; medir cuántas
  más). Barata: capa de texto en el repo.
- **Fauna/flora contra ecología**: `ecologia_lexicon_map.md` tiene 30 HUECO.
- **El filón del Boletín Antropológico** (ULA, nos. 50-101, acceso abierto):
  ya localizados Zavala sobre los petroglifos de Chirache-Buenevara y el
  "Panorama" de Morón. La vía de adquisición más barata que existe.
- **La esfera ARTE** (`arte.yaml` + compilar_corpus): decidida el 08-25,
  sin implementar. Material listo en `petroglifos_y_manaure.yaml` §7.

## C · Adquisiciones pendientes

| Obra | Por qué | Estado |
|---|---|---|
| **Arcaya, *Obra inédita y dispersa*** (CIHPMA-UNEFM 1995), **p. 247** | las DOS versiones originales de la fórmula de Mitare — el único fragmento de habla | vía CIHPMA/UNEFM; objetivo = una página |
| **Brett Martínez, *Aquella Paraguaná*** (1971/1998) | etimologías locales de los pueblos de la península | ejemplar físico en Iberlibro (ficha en la nota) |
| **Antczak & Antczak, *Los ídolos de las islas prometidas*** | la ruta de atestación de los cemíes (choque Antolínez↔Arcaya declarado) | solo tenemos la portada — prioridad subió |
| **Galeoto Cey** (ed. 1995) | "esta lengua caquetía es la más bella... con muchos derivativos" — juicio morfológico de testigo | Miguel la compra |
| **Acosta Saignes, *Estudios de etnología antigua*** (UCV 1961) | Manaure-como-dinastía con peso académico; ⚠️ verificar el matiz "de padres a hijos" (¿colonial?) | localizable |
| **Antolínez, *Los ciclos de los dioses*** (1995) | donde encajaría "El Diao Manaure" completo | Oruga Luminosa, San Felipe |
| **G. Morón, *Los orígenes históricos de Venezuela*** (1954) · *Los cronistas y la historia* (1957) | el siglo XVI con aparato; crítica de fuentes sobre Castellanos/Oviedo y Baños | bibliotecas |
| **Mosonyi, *Hablemos… Idiomas Indígenas*** (2007) · **Bidó, *Voces del Bohío*** (2010) | lingüística moderna para D11; vocabulario taíno para repertorio | localizables |
| **Pet 1987 (*Lokono Dian*)** · **Bennett 1989 (*Arawak-English Dictionary*)** · **de Goeje 1928** | la escala diccionario del rebalanceo lokono (D11 #39) — las 227+48 actuales citan a los tres pero ninguno está en el repo | Pet: SIL, suele haber PDF; Bennett: Walter Roth Museum |
| **Marie-France Patte** (¿*Parlons Añun*?) + material de revitalización de Sinamaica | LA especialista del añú — la columna paraujano hoy descansa solo en Wilbert 1958-59 vía Oliver | por localizar |
| **C. Morón, *Manaure: al filo de la eternidad*** (2007) · **Esteves 1988** · **Acasio 2013** | el libro entero sobre Manaure; el segundo Esteves; los petroglifos de Siraba | Casa Blanca/Lagoven/Punto Fijo |
| van Koolwijk 1884 · Martí 1969 (7 t.) · Tamers 1965 · Hartog 1961 | (de la tanda anterior, siguen vigentes) | sin localizar / papel |

## D · Trampas medidas esta tanda (leer antes de minar)

1. **Un cero sobre nombre propio colonial exige permutar TODAS las vocales
   interiores, no solo las iniciales.** El grep del 08-14 probó
   `jurijureb/hurihureb/jurijure/urihure` y concluyó que Castellanos no traía
   el topónimo. La grafía real era `Hurehurebo` — con **e** — y estaba, con
   la lista de once ciudades al lado. La conclusión vivió 11 días siendo
   falsa. (El mismo error ocultó `coques` detrás de `koke`.)
2. **El merge de un PR congela la rama en ese commit.** El #110 se mergeó a
   mitad de sesión y los 10 commits empujados después quedaron fuera de main
   — y el checkout posterior los borró del disco. Nada se perdió (estaban en
   la rama), pero costó un rescate. Si se sigue trabajando tras abrir un PR,
   avisar antes de mergear.
3. **Autores regionales: la cita documental entra, la deducción no.** A
   González Batista se le refutaron `hure`='arena' y `corocoro`='espinas'; a
   Antolínez, `ma`='grande' y el étimo de Capo — siempre con las fuentes que
   ellos mismos citan. El método es atestación contra inferencia, no
   autoridad contra autoridad.
4. **La consola y los guardas del harness**: el guard de PowerShell bloquea
   comandos cuyo TEXTO contenga rutas tipo `/s/` o `/w/` (aunque sean glosas
   fonémicas en un here-string) — para contenido con fonémica, escribir a
   archivo con Write y pasar `--body-file`. Y el Bash puede perder el PATH a
   mitad de sesión: PowerShell es el plan B.

## E · Lo que NO hay que hacer

- **No tocar el canon fuera de un aplicador.** El patrón que funcionó:
  decisiones registradas en `6-fusion/decisiones_tanda_*.yaml` → un
  `aplicar_tanda_*.py` idempotente con `--dry-run` → guardianes → commit.
- **No aplicar `h`→∅ ni `ce/ci`→/s/**: quedaron DISPUTADAS en D5
  (`Hurehurebo`~`Jurijurebo` da h~j pero `Hacarigua`~`Acarigua` da h~∅).
- ~~No regenerar `lexicon_zavala.py` sin fusionar/excluir el #89~~ **resuelto
  2026-08-31**: el miner casa por `forma_fuente` y el #89 (y `barique`) quedan
  como YA_EN_LEXICON; la regeneración ya no resucita duplicados.
- **No importar el matiz patrilineal de Acosta Saignes sin resolverlo**
  contra el canon matrilineal (regla 3; ver antolinez-1944-manaure.md).
- **No dar por caquetío** lo de Barquisimeto, Yaracuy o los Llanos: el
  material de Brito Figueroa/Federmann vive en
  `polities_no_costeras_federmann.yaml` con su `polity` declarada, y ahí se
  queda salvo decisión.
- Las trampas de OCR y desfases de la tanda anterior siguen vigentes
  (offset Oliver **−27**, Gilij vol.1 **−52**, `--psm 6`, dos dpi y fundir).

## Enlaces

[[TABLERO]] · [[BANDEJA]] · [[CRONICA]] · [[PLAN_MAESTRO]] ·
`6-fusion/decisiones_tanda_2026-08-30.yaml` ·
[[velasco-2015-resistencia]] · [[gonzalez-batista-nombre-de-coro]] ·
[[moron-2012-petroglifos]] · [[antolinez-1946-hacia-el-indio]]
