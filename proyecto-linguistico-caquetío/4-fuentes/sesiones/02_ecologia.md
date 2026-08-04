---
tipo: hoja-de-fuentes
sesion: 2/4
moc: mapa-ecologia
---

# Hoja de fuentes — Sesión 02: Ecología del Golfete de Coro

> [[mapa-ecologia]] · [[02_ecologia_golfete|ensayo]] · [[INDICE_FUENTES]]
> Fuentes: [[camacho-2011]] · [[antczak-2015-las-aves]] · [[rouse-cruxent-1963]] · [[alvarado-1921]] · [[jahn-1927]]
>
> ⚠️ **Corrección posterior (2026-07-29)**: este documento clasifica a
> [[alvarado-1921]] y [[jahn-1927]] como *"escaneo de imagen sin capa de texto,
> no extraíble sin OCR"*. Eso era un artefacto de `pypdf`: **con `pdftotext`
> ambos extraen texto completo**. Ver [[INDICE_FUENTES]].

*Programa «corpus cultural», sesión 2 de 4. Pregunta guía: ¿Dónde existía el caquetío?*
*Registro de qué se buscó, qué se encontró (ubicación exacta) y qué quedó abierto.*

---

## 1. Lectura de contexto del repo (punto de partida)

| Fuente | Ubicación | Qué aportó |
|---|---|---|
| Canon etnohistórico | `curiana_sim/CULTURA_CAQUETIA.md` | Confirma el hueco: cubre economía (§3) y ciclo seca/lluvias (§2) pero NO el medio físico. |
| Locaciones y eventos | `curiana_sim/curiana_state.py` | Locaciones a las que dar sustancia (orilla, manglar, salinar, conuco, buco, matorral, camino_islas…) y eventos ambientales ya escritos (raspado_salinar, gran_cosecha_sal, crecida_buco, expedicion_perlas…). |
| Lexicón | `curiana_sim/curiana_lexicon.py` (7442 líneas) | Inventario de especies/paisaje ya nombrados; base para detectar huecos léxicos. |
| Nombres de agentes | `curiana_sim/curiana_agents.py` | Reveló que cunaro/guaranaro/bagre son componentes de nombres pero no entradas del lexicón. |

### Inventario léxico ecológico ya presente (verificado por grep)

- **Clima/viento:** joutai (viento), habobrisa (brisa del Golfete), kayawara (tormenta),
  haborü (marejada), madunaka (sequía), kaya (lluvia), kali (sol), kasha (luna).
- **Agua/geografía:** duna (¡AGUA, no médano!), habo (mar), bara/paro/güique (ríos),
  cari (costa), rao (arena), pariri (pantano/ciénaga), tarica (laguna), borojo (salina),
  buco/buko (represa/acequia), sima/quidi (cerro/sierra), sabana, cayo, manigua.
- **Flora:** mankaba (manglar), marawa (palma), coro/kadushi/caduchi (cardón y fruto),
  watapana (dividivi), kukuisa (cocuiza), rülipi (sábila), adoptivo (cují/trupillo),
  saruro, kasiripa (yuca brava), marisi/maisi (maíz), yuri/tabako (tabaco).
- **Fauna:** arima (pez), kanawari (tiburón), manatü/manati (manatí), ukura (cangrejo),
  hikoteya (tortuga), kaiwa (caimán), cobo (botuto/caracol reina), tüma (perla),
  tokoko/chogogo (flamenco), chuchubi (sinsonte), warawara (zamuro), chiriguare (gavilán),
  pauji, tara (venado), cachicamo (armadillo), iwana/iguana, koke (bachaco), tuqueque (gecko),
  kama (tapir — fauna de tierra firme, no local).

---

## 2. PDFs de `fuentes_caquetios/`

Herramienta: extracción con `pypdf` (la ruta contiene «í», que rompe el paso directo;
se resolvió con un script que localiza por glob). El render de páginas de la tool Read
no funcionó (falta poppler/pdftoppm en el entorno).

| PDF | Estado | Qué se extrajo |
|---|---|---|
| **Camacho et al. 2011, Dunas Médanos Falcón** | ✅ Texto OK (13 pp.) | **Fuente estrella.** Geomorfología del Istmo de Médanos, clima (BWi/BSh, ~380 mm, 28 °C, viento ENE todo el año), ambientes sedimentarios (playa/dunas/salinas/pantanos con áreas en km²), dimensiones de dunas, flora colonizadora (cují yaque, Acacia tortuosa, gramíneas), paleogeografía (estabilización ~4000 BP), ríos (Mitare, Coro, Caujarao, Ricoa, Hueque, Tocuyo). Páginas clave: 2 (clima), 3 (tablas), 4 (ambientes), 10 (flora), 10–11 (origen y evolución). |
| **Antczak & Antczak 2015, Las Aves Arqueología** | ✅ Texto OK (38 pp.) | Navegación insular, cerámica dabajuroide/valencioide, botuto (Lobatus/Strombus gigas) en alta densidad, tortugas (223 restos, cabezas cortadas), bobas (Sula sp.) y guano, otros moluscos (Cittarium pica, Codakia orbicularis, Strombus costatus), loro/Scarus, pesca de perlas y armadas esclavistas. Páginas clave: 4 (conch/islas), 13 (tortugas), 21–23 (moluscos, guano, bobas). Es sobre el archipiélago «Las Aves» (topónimo), NO sobre aves como taxón. |
| **Rouse & Cruxent 1963, Venezuelan Archaeology** | ❌ **ARCHIVO VACÍO (0 bytes)** | No se pudo leer. Era la fuente prevista para la cerámica dabajuroide. Sustituida por WebSearch (Atlas del Arte Precolombino) + Antczak & Antczak 2015. **Pendiente: reconseguir el PDF.** |
| **Alvarado 1921, Glosario Voces Indígenas** | ⚠️ Escaneo de imagen sin capa de texto (354 pp., 27 MB; pág. 1 vacía) | No extraíble sin OCR. Sus nombres de especies ya están integrados al lexicón como `caquetío-atestiguado`. No se OCR-eó (fuera de alcance de la sesión). |
| **Jahn 1927, Aborígenes Occidente Venezuela** | ⚠️ Escaneo de imagen sin capa de texto (510 pp., 37 MB; pág. 1 = «IA») | Igual que Alvarado: no extraíble sin OCR; datos ya en el lexicón. |

---

## 3. WebSearch (ciencia natural moderna y arqueología)

| Búsqueda | Hallazgo aprovechado | Fuente |
|---|---|---|
| Ecología del Golfete de Coro / manglares | Mangle rojo (*Rhizophora mangle*, Iguanita) y negro (*Avicennia germinans*, Panamá) en el Golfete O / NE Paraguaná; fauna semiárida (conejo, zorro, cachicamo, iguana, cascabel). | ResearchGate (geoquímica de suelos de mangle); InParques Médanos de Coro. |
| Cerámica dabajuroide | Serie de la costa O de Falcón, ~1300 km hasta las Antillas Neerlandesas, 800–1600 d.C., correlacionada con el caquetío; polícroma sobre engobe blanco, trípodes con base anular calada, bases impresas con tejido, urnas funerarias con figuras. | Atlas del Arte Precolombino Venezolano (serie-dabajuroide). |
| Salinas Las Cumaraguas / producción de sal | Salina natural de Paraguaná; evaporación solar de agua de mar estancada; cosecha artesanal; rosa por *Dunaliella*; 14 km de los Médanos; tercera del país tras Araya y Los Olivitos. | Voz de América; TalCual; Steemit; Últimas Noticias. |
| Río Mitare / clima / hidrología | Mitare ~120 km, principal de la vertiente del Golfo de Venezuela; Coro 417 mm/año, 28.4 °C; clima semiárido de la costa occidental y Paraguaná. | Wikipedia (Estado Falcón); doc. hidrológico de la cuenca. |
| Ictiofauna Golfo de Venezuela | Pargo (Lutjanus), corvina (Cynoscion), mero (Epinephelus), róbalo (Centropomus), bagre marino (Bagre/Arius), en La Vela de Coro. | FAO (perfil pesquero Venezuela); venceya.com; SIAN-INIA. |
| «cunaro» / «guaranaro» como peces | **cunaro** = pargo de altura (*Rhomboplites aurorubens*), confirmado como pez en el Sistema Venezolano de Datos de Biodiversidad. **guaranaro**: no confirmado directamente (posible variante local; ≠ «guaraguara»/corroncho de agua dulce). | SVDB (minec.gob.ve/fauna/cunaro). |
| Alisios / navegación a islas | Alisio ENE→SO todo el año; Aruba a ~25 km al N de Paraguaná, alcanzable/visible; islas ABC pobladas por arahuacos con conexión arqueológica al continente. | Wikipedia (Vientos alisios, Geografía de Aruba, Península de Paraguaná). |

---

## 3-bis. WebSearch de la ampliación v2 (capa biológica y huecos de cobertura)

Motivada por la revisión crítica de la v1, que detectó: `conuco` y `taller_canoas` sin
entradas, el alisio enterrado en una sección miscelánea, y `atestiguado` aplicado a
afirmaciones apoyadas solo en prensa.

| Búsqueda | Hallazgo aprovechado | Fuente |
|---|---|---|
| Fauna de mamíferos del PN Médanos de Coro | **Fauna terrestre escasa por el clima desértico** (cita explícita). Nómina: zorro (*Cerdocyon thous*), oso melero (*Tamandua tetradactyla*), conejo sabanero (*Sylvilagus floridanus*), mapurite (*Conepatus semistriatus*), rabipelado (*Didelphis marsupialis*). Zona de vida: monte espinoso tropical; flora: cují yaque, yabo, espinito, tunas, cardones. | Inparques; sapmcovenezuela; EcuRed (PN Médanos de Coro). |
| Reptiles de Falcón / Paraguaná | Cascabel (*Crotalus durissus*, entre cardones/acacias/cujíes/guayacanes), coral, mapanare, tigra cazadora, lagartijo, mato real, tortuga mordelona. El lagarto más pequeño del mundo (3–5 cm) en la zona. | Falcón «Museo a Cielo Abierto»; Ven a Paraguaná. |
| Fauna marina de Falcón | Tortugas marinas: verde, carey, cardón, cabezón. Delfines. Peces: mero, pargo, corvina, sábalo, róbalo, cazón, sardina, jurel, corocoro. **Las 4 especies de mangle de Venezuela** (rojo, negro, blanco, botoncillo) — confirma lo que la v1 daba por inferencia. | PN Morrocoy (Falcón), usado como análogo del mismo litoral. |
| Agricultura caquetía / conuco | **Hallazgo mayor: los caquetíos desarrollaron un sistema de riego llamado BUCO trazado en las márgenes del río Coro**; los del Valle del Turbio idearon riego desde los ríos. Agricultura desarrollada: maíz, yuca, batata. Lógica del conuco: perturbación y sucesión, tala y quema, cenizas como nutriente, troncos in situ contra erosión, policultivo que previene plagas, seguridad alimentaria familiar. | Aporrea (resistencia indígena y producción de alimentos); Wataniba, *El conuco indígena: más que una parcela agrícola*. |
| Maderas de canoa indígena | Cedro rojo (*Cedrela odorata*), caoba (*Swietenia*), ceiba (*Ceiba pentandra*); ahuecado **con fuego, sin instrumentos de hierro**; clasificación de maderas por peso y dureza. → **Inferencia propia:** esas especies no son del cardonal ⇒ la madera de canoa venía de fuera. | Analitica (*Las formas de la madera en el arte indígena*); documentación sobre canoas caribeñas. |
| Venado caramerudo en Falcón | **Hoy ausente de gran parte del estado Falcón**, por caza indiscriminada y sistemática **moderna**. → Corrige la licencia del §2: la fauna de hoy NO es la del s. XV. | Fundo Flor de Coco; SciELO Venezuela (manejo del venado caramerudo). |

### Cambios de etiqueta aplicados en la v2

- `ecologia-009` (Las Cumaraguas): **atestiguado → reconstruido**. La documentación es
  periodística y describe una operación artesanal de ~80 años, no una continuidad
  precolonial demostrada. El proceso evaporítico en sí es física elemental.
- `ecologia-011` (manglar): **referencia reforzada** — las 4 especies de mangle pasan de
  inferencia a dato confirmado vía PN Morrocoy.
- `ecologia-030` (quema del conuco con alisio): entrada nueva marcada **hipotetico** — es
  la primera entrada del corpus con esa marca, y era necesaria: es una inferencia sin
  respaldo directo.

---

## 4. Qué quedó abierto / pendientes

1. **Rouse & Cruxent 1963 está vacío (0 bytes).** Reconseguir el PDF para verificar de
   primera mano la definición de la tradición dabajuroide (arcillas, seriación, estilos)
   y afinar las entradas ecologia-013/014. Fuente citable pero no leída en esta sesión.
2. **Alvarado 1921 y Jahn 1927 sin OCR.** Son escaneos de imagen. Sus nombres de especies
   ya están en el lexicón, pero una pasada de OCR podría rescatar descripciones de hábitat
   y usos que hoy no están capturadas. Trabajo para una sesión futura de fortalecimiento.
3. **«guaranaro» sin identificación taxonómica firme.** Se usa como nombre de pez en la
   simulación; no se halló la especie exacta. Queda como dato a confirmar (posible nombre
   vernáculo local o variante ortográfica).
4. **Especies de manglar del Golfete:** se confirmaron rojo y negro; mangle blanco
   (*Laguncularia*) y botoncillo (*Conocarpus*) se dan por esperables (marca `reconstruido`),
   no verificados para el Golfete específicamente.
5. **Aves del manglar/Golfete:** no se hizo un inventario ornitológico dedicado (más allá
   de flamenco, bobas, zamuro, gavilán). Un estudio de avifauna del Golfete/La Vela
   afinaría la locación `manglar` y las entradas de fauna.
6. **Hidrología fina de la zona de Coro s. XV:** el carácter efímero de los cauces se
   infiere del clima BSh (marca `reconstruido`); no se halló un estudio paleohidrológico
   específico del entorno inmediato de la Curiana.
7. **Cero entradas `retro-abstraido` en todo el corpus.** La metodología del programa
   prevé la tradición viva local (Paraguaná / Coro) como cuarto canal de conocimiento, y
   esta sesión no aportó ni una entrada por esa vía: todo salió de ciencia natural
   publicada y arqueología. Es un hueco **de método**, no de datos — requeriría fuentes
   de tradición oral, etnografía local o conocimiento de primera mano de la región.
8. **Arqueozoología del área caquetía:** no se halló un estudio de restos faunísticos de
   yacimientos del Golfete/Coro (el de Antczak es insular). Sería la vía para saber **qué
   comían realmente** en vez de inferirlo de la fauna moderna — y para calibrar §10.6.
9. **Zonas sociales sin cubrir (por diseño):** `plaza`, `casa_cacique`, `choza_piache` y
   `perimetro` siguen en cero entradas. No son locaciones ecológicas; corresponden a otras
   sesiones del programa.

---

## 5. Entregables producidos en esta sesión

- Mini-ensayo: [`3-mundo/ensayos/02_ecologia_golfete.md`](../../3-mundo/ensayos/02_ecologia_golfete.md)
  — **v2**: 13 secciones + anexo. Incorpora la capa biológica (§10, con la tesis del
  contraste tierra pobre / mar rico), el alisio como sección propia (§4), el conuco (§6) y
  el taller de canoas (§11.2).
- Corpus YAML: [`3-mundo/corpus/ecologia.yaml`](../../3-mundo/corpus/ecologia.yaml)
  — **38 entradas + 9 huecos léxicos** (47 en total; validado con `yaml.safe_load`).
  Etiquetas: 29 atestiguado / 17 reconstruido / 1 hipotético.
- Mapa ecología ↔ lexicón: [`3-mundo/corpus/ecologia_lexicon_map.md`](../../3-mundo/corpus/ecologia_lexicon_map.md)
  — cross-check por 9 dominios, con los huecos ordenados por presión.
- Diseño del motor ambiental: [`5-experimento/disenos/02_motor_ambiental.md`](../../5-experimento/disenos/02_motor_ambiental.md)
- Índice de cultura: [`3-mundo/corpus/README.md`](../../3-mundo/corpus/README.md)
  (creado en esta sesión; no existía).
- Esta hoja de fuentes.

### Cobertura de locaciones alcanzada

`orilla` 11 · `matorral` 9 · `manglar` 6 · `buco` 3 · `salinar` 3 · `taller_canoas` 3 ·
`bohios` 3 · `camino_islas` 3 · `conuco` 2. Todas las locaciones **ecológicas** de
`curiana_state.py` tienen sustancia; las restantes son sociales.
