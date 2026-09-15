# Los nombres de la era 2, rehechos con lo que hay de caquetío

Miguel, 2026-09-14: *«¿No deberíamos rehacer los nombres en base a lo que
conocemos y tenemos de caquetío?»* → **«Sí a los dos puntos»**; y el mismo
día, sobre los sufijos: **«Sí o sí hay que sacar eso de -ko y -sha. Si es
inventado, tanto de la gramática como de los nombres.»**

Esto es lo que salió. Tres archivos nuevos y el elenco reescrito:

| archivo | qué tiene |
|---|---|
| `6-fusion/antroponimos_caquetios.yaml` | la minería: 48 entradas, 79 formas, con procedencia y etiqueta |
| `6-fusion/sistema_de_nombres_era2.yaml` | las ocho reglas, cada una con su evidencia |
| `6-fusion/mapa_nombres_era2.yaml` | los 63, viejo → nuevo, con raíz, glosa, fuente y razón |
| `6-fusion/elenco_era2.yaml` | aplicado: `nombre`, `alias_era1`, `nombre_nuevo`, `razon_del_nombre` y todas las referencias internas |
| `6-fusion/scripts/medir_antroponimos.py` | mide la campaña (regla 1) |

Ninguna cifra de abajo está escrita a mano: las imprimen
`6-fusion/scripts/verificar_elenco_era2.py` y
`6-fusion/scripts/medir_antroponimos.py`.

---

## 1. Lo minado

Barrido de `fuentes_caquetios/*.txt` y `*.ocr.txt` más el texto extraído con
`pdftotext -layout` de Arcaya 1920, Oviedo y Baños, Oliver 1989 cap. 3 y la
tesis. **48 entradas, 79 formas distintas**: 40 atestiguadas, 4
retro-abstraídas y 4 hipotéticas; 14 con marca de regla 3 y **9 con marca de
regla 4**; 3 sin procedencia, con deuda declarada.

### Lo que no se sabía y ahora sí

| nombre | qué es | dónde | etiqueta |
|---|---|---|---|
| **Naure ~ Anaure** | ⭐ *«un gran cacique que está diez leguas la tierra adentro en la provincia de Coro, y el dicho Cacique se llama Naure o Anaure»* — carta de Ampíes al Rey | Arcaya 1920 **p. 160** | atestiguado |
| **Don Juan Baracoica** | cacique *«que está en las islas y es su pariente y deudo»* (Ampíes) y *«hijo del mismo Manaure»* | Arcaya **pp. 160 y 199**; Zavala #31 lo da de Curazao | atestiguado |
| **Don Sancho Uriacoa** | *«Cacique general» de los caquetíos del Occidente; «sus descendientes usaron como apellido el nombre del célebre caudillo»* | Arcaya **p. 327**; Oliver cap. 3 **pp. 255-256** | atestiguado |
| **Don Luis Caguallo** | hijo de Uriacoa, paramount; «abdicó» en 1636 | Oliver cap. 3 **pp. 255-256** | atestiguado |
| **Boniata / Bonyata** | cacique de Miraca, muerto en la jornada de Federmann — **dos grafías independientes** | Arcaya **p. 220** (por Herrera) y AGI leg. 218 f. 2 (Bastidas 1538) vía Velasco | atestiguado |
| **Barbo de Goyabaco** | cacique llevado por Federmann; el traslado del AGI lee *«verbo»* | Arcaya **p. 220** | atestiguado, forma dudosa |
| **cacique Baltasar de Hurihurebo** | emisario de Manaure hacia Ampíes; segundo cacique documentado de ese pueblo | Oliver cap. 3 **p. 266** | atestiguado (nombre cristiano) |
| **Adaure · Timaure · Yaraure · Chunaure · Manaure** | *«algunos de los apellidos de la gran familia caquetía»* | Esteves **p. 13** | atestiguado |
| **Caguao · Cuauro · Mabo · Guarecuco · Cap[acho] · Cotopo** | apellidos vivos, entrada MORUY | Esteves **p. 53** (el OCR daña la quinta forma) | atestiguado |
| **Caguado · Cauro · Gotopo · Guanipa · Guarecuco · Guariato · Mabo · Manaure · Timaure** | los mismos, dichos por un paraguanero | Medina Colina **p. 328** (mc-mundo-029) | atestiguado |
| **Tumarure** | *«el apellido de un cacique»*; hoy la aldea Tumarusa, municipio Moruy | Esteves **p. 64** | retro-abstraído |
| **Cumare · Mauroa** | dos caciques que sólo sobreviven dentro de un topónimo | Zavala (Cumarebo); Esteves **p. 122** (Mauroa) | retro-abstraído |

### Lo que el encargo daba por bueno y no lo es

🔴 **«La elegía de Coro» no existe.** La línea 52079 de Castellanos sí dice
*«Con otro principal dicho Categue»*, pero está en la **Parte II, Elegía I
(«A la muerte de micer Ambrosio»), Canto II**, y el pasaje narra la entrada de
**Federmann** *«en demanda de los llanos»*: el canto termina *«en un pueblo de
chipas en los llanos»*. Los cuatro nombres que da el guía —**Catimayagua,
Categue, Gecoagua y Badurajara**— son del interior, no de la polity costera:
quedan marcados con **regla 4** y **no se reutilizan**.

Lo que sí vale de ese mismo pasaje: cincuenta versos más abajo,
*«Del cacique **Manaure**, rey de Coro»* — atestación literaria del título,
independiente de Oviedo y Baños y de Arcaya.

### Los ceros (verificados, regla 6)

- **Cero nombres de mujer caquetía.** El patrón `(india|muger|mujer|cacica|
  hija|hermana|vieja|moza|señora|princesa) + (llamada|dicha|nombrada|de
  nombre)` da ocho aciertos en todo el corpus y ninguno es de la esfera: Juana,
  Catalina, Ana, Francisca, Leonor (castellanas), Itiba (taína, Pané) y
  Apacuana (Quiriquires del valle de Caracas). La única mujer caquetía con
  nombre escrito es **Doña Sancha**, y su nombre es castellano.
- **Cero marca de género en el nombre**, en las 62 obras de `bibliografia.yaml`.
- **Cero antropónimos precontacto.** El registro empieza con Ampíes (1521-27).
- **Perea 1942 tomo I no aporta nada**: sus «nombres propios» son chaná y
  charrúa de la Banda Oriental. Gatschet y van Buurt, cero antropónimos (van
  Buurt trae un cacique caquetío que murió en Bruselas, *sin nombre*).

---

## 2. Los formantes, con su recurrencia medida

`recurrencia` = formas distintas del corpus que terminan en él, comparadas con
`fonemizar` para que la ortografía colonial y la lingüística cuenten juntas.

| formante | recurrencia | ejemplos | ¿productivo? |
|---|---|---|---|
| `-aure` | **7** | Adaure, Timaure, Yaraure, Chunaure, Manaure, Anaure, Naure | sí |
| `-ure` | **8** | los siete + Tumarure | sí |
| `-ata` | **4** | Bonyata, Boniata, quiciroata, quiceromata | sí (dos de Barquisimeto: regla 4) |
| `-koa` | **1** | Uriacoa (= `uria` «plantío» + -koa) | sí, por el `-bacoa` toponímico (morfema-001, 4 apoyos) |
| `-oa` | 3 | Mauroa, quiceroaboa, uriakoa | no, se subsume en -koa |
| `-bana` | 2 | Yarosabana (Yaracuy), Judibana (leyenda) | **no**: es morfema toponímico (D9). Se conserva donde ya estaba |
| `-ika` | 1 | Baracoica | no: un solo caso |
| `-allo` | 1 | Caguallo | **no**: `<ll>` es dígrafo castellano. Acuñar en -allo sería acuñar castellano |

`morfemas.yaml` no tenía ninguno: sus once morfemas son toponímicos. `-aure`
entra al proyecto con esta campaña.

---

## 3. El sistema de nombres, en diez líneas

1. La **raíz** es una voz de `VOCABULARIO_BASE` con fuente
   caquetío-atestiguado (preferida) o caquetío-reconstruido. Nunca hipotética,
   nunca comparanda.
2. El **formante** es opcional y sólo puede ser `-aure`, `-ure`, `-koa` o
   `-ata`; `-koa` sólo sobre raíz de cosa o lugar, como en Uriacoa.
3. Vocal + la misma vocal se funde en la juntura (`rua` + `-ata` → Ruata): el
   caquetío atestiguado no tiene vocal doble.
4. Todo nombre pasa el filtro de `curiana_fonotactica.Fonotactica` construido
   con el caquetío atestiguado: inventario, clusters y coda final.
5. Los **títulos son cargos**, no nombres: `diao`, `apopo` y `boratio` viven en
   la ficha. La excepción es **Manaure**, que el registro usa como nombre.
6. **Sin `-ko` ni `-sha`** — ni `-ni`, `-nu`, `-mana`, que eran igual de
   inventados y sin siquiera el pretexto del género. El género vive en el campo
   `genero`.
7. Los diez antropónimos reales atestiguados quedan **declarados y
   reservados**: todos son de personas del contacto o de la colonia (regla 3).
   La única excepción aplicada es **Naure**, que es a la vez voz del lexicón y
   nombre de cacique.
8. **Unicidad ampliada**: ningún nombre choca con otro del elenco, con un
   agente de la era 1 que no sea su alias, con los 17 que quedan fuera, con las
   14 personas de fondo de `genealogia.yaml` ni con la `forma` de un topónimo
   del canon —ni el nombre ni la raíz—; y dos nombres no se distinguen por una
   sola letra (Levenshtein ≥ 2 sobre la forma fonemizada).
9. Se **conservan tres**: Manaure (título), Kunaro-bana y Dara-bana (raíz
   atestiguada, sin `-ko`/`-sha`, y `-bana` tiene una atestación antroponímica
   —Yarosabana— con su regla 4 declarada).
10. Se **evita** como nombre la voz de uso corriente (sol, luna, noche, cabeza)
    porque el motor cuenta formas y no referentes. Reduce el problema; no lo
    resuelve: ver la pregunta 1.

---

## 4. El mapa: los 63, viejo → nuevo

**=** significa «se conserva». Capa: **A** atestiguada, **R** reconstruida.

**los Tacuatos**

| era 1 | era 2 | raíz | glosa | capa | formante | por qué |
|---|---|---|---|---|---|---|
| Kunaro-bana | **=** | `kunaro` | pez del golfete de Coro | A | -bana | El apopo se llama como el pez que persigue en la seca. |
| Pira-sha | Dabuda | `dabuda` | barro loza | A | — | Maestra alfarera: el barro de loza con que se hace lo que ella guarda y enseña. |
| Biro-ko | Birokoa | `biro` | sal | A | -koa | El molde de Uriacoa: «el del sitio de la sal», que es lo que raspa en las charcas. |
| Naure-sha | Naure | `naure` | planta bejucosa / jojoto | A | — | Guarda la semilla de maíz; `naure` es «mazorca tierna» en Esteves. Y es nombre de cacique en la carta de Ampíes. |
| Piri-sha | Uria | `uria` | plantío, siembra | A | — | La más joven, recién casada, que trabaja el conuco de más. Raíz desnuda de Uriacoa. |
| Guare-ko | Duraboa | `duraboa` | conuco sembrado | A | — | Vino de Caseto sabiendo el conuco de interior. |
| Kori-sha | Akaure | `aka` | bejuco | A | -ure | Cordelera; el formante de familia, porque su linaje sigue siendo el de El Cayude. |
| Suba-ko | Urari | `urari` | veneno/medicina vegetal | A | — | Conoce «la planta que cura de la que mata»: eso es urari. |
| Uro-ko | Dichiba | `dichiba` | límite, línea | A | — | El de la buena vara, que mide linderos y dice de quién es la playa. |
| Kawa | Chirwa | `chirwa` | tinaja pequeña | A | — | Aprendiza de alfarería: lo primero que se aprende a hacer. |
| Piri | Ucibo | `ucibo` | cuenta de piedra, chaquira | A | — | Se zambulle donde nadie: lo que sube del fondo. |
| Kori | Chakamba | `chakamba` | ¿cómo? | A | — | La niña que pregunta; la única palabra-pregunta atestiguada del lexicón. |
| Korie-ko | Patapati | `patapati` | anegadizo | A | — | Guardián de los jagüeyes: la tierra que retiene el agua. |

**los Cayudes**

| era 1 | era 2 | raíz | glosa | capa | formante | por qué |
|---|---|---|---|---|---|---|
| Bagre-ko | Jachos | `jachos` | teas para la pesca nocturna | A | — | La glosa de la fuente describe su oficio entero. |
| Tuqa-sha | Wairon | `wairon` | hoguera | A | — | Matriarca que lleva la casa y el fogón. |
| Dara-bana | **=** | `dara` | alcaraván | A | -bana | El vigía que ve primero. |
| Suka-sha | Wache | `wache` | murciélago, zorro blanco | A | — | Ahúma de noche y lee el tiempo: el animal de su hora. |
| Kati-sha | Katiata | `kati` | luna | A | -ata | Sale cuando hay luz de luna; formante de Bonyata. |
| Wari-ko | Dunakoa | `duna` | agua | R | -koa | Dice dónde cavar la charca: «el del sitio del agua». |
| Wama-sha | Wanepe | `wanepe` | cesto para cargar niños | A | — | Cuida a los niños de la casa entera. |
| Waranaro-sha | Waranaro | `waranaro` | pez lisa | A | — | Pescadora de red. Conserva raíz, pierde sufijo. |
| Taku-ko | Ruata | `rua` | cargar, llevar | R | -ata | Carga la hamaca del Manaure cuando sube al cerro. |
| Daru | Chuchubi | `chuchubi` | sinsonte tropical | A | — | Corre los avisos: el pájaro que repite lo que oye. |
| Ita-sha | Cege | `cege` | lechuza | A | — | La vidente de ochenta años: el ave que ve de noche. |
| Sha | Jaiata | `jai` | oír, escuchar | A | -ata | La niña que escucha desde el umbral. |

**casa del Manaure**

| era 1 | era 2 | raíz | glosa | capa | formante | por qué |
|---|---|---|---|---|---|---|
| Manaure | **=** | `manaure` | título laudatorio del señor principal | A | — | Es título atestiguado, no nombre inventado. |
| Nubiri-sha | Karebe | `karebe` | cucharón de media tapara | A | — | Gestiona la redistribución: el instrumento de repartir. |
| Itana-sha | Simaure | `sima` | cerro, montaña | R | -ure | Matriarca del linaje del señor, al pie del Capubana; nombre de estirpe. |
| Jakura-sha | Jakura | `jakura` | guardar, custodiar | A | — | Guarda lo que se entrega y lo que se retiene. |
| Waimo-ko | Apoaure | `apo` | grande | A | -aure | Sobrino candidato; el mismo elemento que hay dentro de `apopo`. |
| Kabo-ni | Humohumo | `humohumo` | el ave que vuela | A | — | Lleva los recados a los apopos de las cuatro casas. |
| Tina-sha | Harifuche | `harifuche` | maíz tostado y miel | A | — | Tuesta el casabe y sirve lo que baja del cerro. |
| Kahu-sha | Hiko | `hiko` | cada cuerda de la hamaca | R | — | Teje las hamacas del señor y las de alianza. |
| Kumarawa-sha | Kumarawa | `kumarawa` | caracol de las costas de Paraguaná | A | — | La cuarta esposa, corubo: lo suyo y lo de su casa. |
| Kali-nu | Wamipa | `wamipa` | hueco, profundidad | A | — | Guardián de la fuente intermitente del cerro. |
| Piru | Dato | `dato` | fruto del cardón | A | — | Niño de siete años: lo que se come de camino. |
| Shaboro | Sawaka | `sawaka` | inframundo, reino de los muertos | A | — | Boratio mayor: con eso trata. |
| Buio-sha | Hayo | `hayo` | coca, hoja masticada ritual | A | — | Ayunante que lee sueños y prepara el urari. |
| Moruy-sha | Buriche | `buriche` | chicha de maíz fermentada | A | — | Maestra del merejuy. Su nombre viejo era el del sitio, que la regla 8 prohíbe. |

**los Guasicures de Caseto**

| era 1 | era 2 | raíz | glosa | capa | formante | por qué |
|---|---|---|---|---|---|---|
| Ita-ko | Tebekoa | `tebe` | lugar de cultivo | A | -koa | Apopo y agricultor mayor: «el del sitio del conuco». |
| Wasima-sha | Wasima | `wasima` | viejo, anciano | A | — | Matriarca que autoriza los matrimonios. |
| Tabri-sha | Tabri | `tabri` | siembra en proceso | A | — | Siembra y cosecha el conuco de Caseto. |
| Tijua-sha | Tijua | `tijua` | paloma de canto onomatopéyico | A | — | Hila y teje el algodón. |
| Wama-ko | Karama | `karama` | ramazón | A | — | Abre conuco nuevo a roza y fuego: lo que él tumba. |
| Tawaka | Kasebo | `kasebo` | poniente, oeste | A | — | Se mudó de El Cayude a la costa del oeste: el nombre dice el viaje. |
| Saruro-sha | Saruro | `saruro` | boa, serpiente no venenosa | A | — | Alfarera principal de AMUAY. Conserva raíz, pierde sufijo. |
| Dipopo-sha | Dipopo | `dipopo` | fibra de cocuiza, cabuya | A | — | Trae a esta casa las cuerdas que no sabía hacer. |
| Suri-bana | Waitiao | `waitiao` | amigo ritual, aliado de alianza | A | — | El papel que le toca entre los dos nodos; su raíz vieja no estaba en el lexicón. |
| Pari-nu | Bajari | `bajarí` | recorrer, caminar | A | — | El más rápido de AMUAY. |
| Bana-mana | Turicha | `turicha` | ave cantadora, flauta | A | — | Cantor de hazañas. |
| Tawi | Siwa | `siwa` | blando | A | — | Modela vasijas a los diez años: el barro antes de secarse. |

**los Corubos**

| era 1 | era 2 | raíz | glosa | capa | formante | por qué |
|---|---|---|---|---|---|---|
| Kiwa-ko | Kiwakoa | `kiwa` | concha de almeja y otros moluscos | A | -koa | La casa de las conchas, con el molde de Uriacoa. |
| Sha-korie | Amaka | `amaka` | sitio de moler | A | — | Una de las que muelen los huesos del díao. |
| Paugis-sha | Paugis | `paugis` | paují, pavón de monte | A | — | Boratia de AMUAY; el tótem de su linaje, que su ficha ya usaba. |
| Dara-ko | Isiro | `isiro` | árbol corpulento sapindáceo | A | — | Maestro de canoas: de donde sale la canoa. |
| Tauta-sha | Tauta | `tauta` | paloma de hábitos ictiófagos | A | — | Salga y seca el pescado de mar grueso. |
| Ebo-ni | Ebokoa | `ebo` | camino, paso, senda | A | -koa | Conoce el camino por tierra de Carirubana a Tacuato. |
| Arika-sha | Arika | `arika` | árbol de jícara o totumo | A | — | Hace y reparte las totumas. |
| Karapa-sha | Mene | `mene` | brea, betún natural | A | — | Calafatea las canoas. Su raíz vieja chocaba a una letra con Karama. |
| Dare-nu | Dakawa | `dakawa` | árbol de madera compacta | A | — | Aprendiz de canoas con su tío materno. |
| Talata-sha | Talata | `talata` | alegría, contento | R | — | La joven en encierro; la ironía del nombre es suya. |
| Moro-ko | Waru | `waru` | ave mayor que el zamuro | A | — | El de los huesos, que sostiene el fuego bajo la hamaca del díao. |
| Nubi | Tigi | `tigi` | paloma que come peces | A | — | Niño de ocho años con un palo por arpón. |

---

## 5. Los conteos

`python 6-fusion/scripts/verificar_elenco_era2.py`

| qué | antes (casting #127) | ahora |
|---|---|---|
| nombres con raíz en el lexicón | **30** de 63 (25 A + 5 R) | **63** de 63 |
| raíces por capa | 25 atestiguada, 5 reconstruida, 33 ausentes | **58 atestiguada, 5 reconstruida, 0 ausente** |
| nombres con `-ko` o `-sha` | **42** | **0** |
| nombres conservados | — | **3** (Manaure, Kunaro-bana, Dara-bana) |
| nombres renombrados | — | **60** |
| formantes usados | X-ko, X-sha, X-bana, X-ni, X-nu, X-mana | raíz sola **50**, `-koa` **5**, `-ata` **3**, `-bana` **2**, `-ure` **2**, `-aure` **1** |
| antropónimos minados | 0 archivos | **48 entradas, 79 formas**; 9 con regla 4, 14 con regla 3 |

Y el conteo incómodo: **49 de los 63 nombres son homógrafos de una clave de
`VOCABULARIO_BASE`**. Ver pregunta 1.

**Estado:** `python -m pytest curiana_sim/tests -q` → **316 en verde**;
`python curiana_sim/guardianes.py --rapido` → **los 7 en verde**;
`python 6-fusion/scripts/generar_agentes_era2.py --check` → al día;
`python 6-fusion/scripts/verificar_elenco_era2.py` → todo en verde;
`python curiana_sim/generar_bandeja.py` → BANDEJA reescrita.

El módulo generado lleva ahora `alias_era1` en cada agente, el diccionario
`ALIAS_ERA1` (63 entradas, los tres conservados apuntándose a sí mismos) y
`resolver_alias()`.

---

## 6. Las preguntas

1. **La homografía.** 49 de 63 nombres son ahora palabras del lexicón
   (`Naure`, `Talata`, `Arika`, `Mene`…). Es consecuencia inevitable de la
   transparencia de esta onomástica, pero el motor cuenta **formas**, no
   referentes: `word_uses`, el contagio léxico, `_FORMAS_EXCLUIDAS` y la
   métrica de emergencia van a ver «Arika» y «arika» como lo mismo. ¿Se añaden
   los nombres del elenco a `_FORMAS_EXCLUIDAS`, se acepta el ruido, o se
   prefiere que más nombres lleven formante para separarlos?
2. **Los apellidos vivos.** Caguao, Cuauro, Mabo, Guarecuco, Cotopo, Guanipa,
   Guariato son apellidos de familias **reales** de Paraguaná (Esteves p. 53,
   Medina p. 328). Quedan declarados y sin usar. ¿Se pueden usar como raíz de
   nombre de personaje, o eso no se hace con el apellido de una familia viva?
3. **`-bana` en nombre de persona.** Se conserva sólo en Kunaro-bana y
   Dara-bana, con su regla 4 declarada (la única atestación antroponímica es
   Yarosabana, del Yaracuy). ¿Se retira también —Kunaro y Dara a secas— para
   que ningún nombre de persona lleve el morfema del cerro?
4. **`naure`: dos glosas cruzadas.** El lexicón lo tiene como «planta bejucosa»
   (Zavala #186) y Esteves dice que eso es `ñaure` y que `naure` es «jojoto,
   mazorca de maíz tierno». Afecta a la entrada del lexicón y a la agente
   Naure. ¿Se abre como colisión de glosa?
5. **Naure/Anaure al lexicón.** `uriakoa` está en `VOCABULARIO_BASE` como
   antropónimo atestiguado; `baracoica` y `naure`-antropónimo no. ¿Suben, con
   su procedencia (Arcaya pp. 160, 199, 327)?
6. **Los cuatro de los llanos.** Categue, Catimayagua, Gecoagua y Badurajara
   son antropónimos atestiguados de **otra** polity. ¿Entran al canon marcados
   con regla 4 —como ya están los cuatro «nombre propio indígena en
   Barquisimeto» de `toponimos.yaml`— o se quedan sólo en la propuesta?
7. **Los dos runs de prueba.** `fec49195` y `81907ae1` tienen 48 y 43 agentes
   con los nombres viejos en Supabase y en `BITACORA_RUNS.md`. ¿Se reescriben
   con `ALIAS_ERA1`, se deja la traducción al lector, o se tiran y se corre de
   nuevo ahora que el elenco cambió de nombres?
8. **El corpus.** `agentes_relacionados` de `3-mundo/corpus/*.yaml` nombra a la
   era 1. La migración ya estaba pendiente (auditoría §7); ahora tiene un
   diccionario que la hace automática. ¿Se migra con `ALIAS_ERA1` o el corpus
   sigue hablando de la era 1, que es la que `compilar_corpus` valida por
   defecto?

**Ya no es pregunta:** los `-ko`/`-sha` de la MORFOLOGÍA que el prompt enseña.
Miguel lo decidió el 2026-09-14 —«Sí o sí hay que sacar eso de -ko y -sha. Si
es inventado, tanto de la gramática como de los nombres»— y el escriba
principal lo aplicó en `curiana_lexicon.py` (`REGLAS_AGENTIVAS` →
`REGLAS_RETIRADAS`, fuera de `TODAS_LAS_REGLAS` y de las plantillas, que ahora
dicen sólo «PLURAL: -kana»). Registro:
`6-fusion/decisiones_tanda_2026-09-14.yaml §antroponimos_era2.gramatica`.
