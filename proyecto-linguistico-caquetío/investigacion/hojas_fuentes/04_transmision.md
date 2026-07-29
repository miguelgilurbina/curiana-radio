# Hoja de fuentes — Sesión 4: Transmisión del saber

Qué se buscó, qué se encontró, qué quedó abierto. Complementa
`investigacion/ensayos/04_transmision_saber.md` y
`curiana_sim/cultura/transmision.yaml`.

## Fuentes internas leídas (obligatorias)

- `curiana_sim/CULTURA_CAQUETIA.md` §5 ("El rol de la lengua" / "Cómo se
  aprende") — punto de partida. Confirma que el aprendizaje lingüístico es
  ya reconstruido como transmisión en el regazo + canciones + trabajo
  compartido, y marca palabras "cargadas" (barsure, pütchi, urari,
  manaure, nombres de muertos) como saber restringido por lengua, no solo
  por contenido.
- `CANON_TIERRA.md` (raíz) — leído completo. Es el documento de diseño
  central de esta sesión: ya propone ritos como mecanismo de transmisión
  medible (concepto explícito, pulso de exposición fuerte vía
  `DifusionLexica`, memoria de largo plazo, registro de eventos por el
  Observer, medición de "eco"). Identifica el hueco de envejecimiento
  (edad/tier estáticos) y las opciones A (acotada) / B (completa). El
  ensayo de esta sesión lo integra y le da marco teórico (Vansina/Ong), no
  lo reemplaza.
- `curiana_sim/curiana_agents.py` — elenco completo de 60 agentes leído.
  Se mapearon todas las díadas maestro-aprendiz visibles en las
  `descripcion` de cada agente (no solo las explícitamente listadas en el
  encargo): además de las 6 mencionadas en el prompt, aparecieron Naure-sha
  (semillas), Corie-ko/Buco-ko→Buco (buco, ya en marcha en un niño T3),
  Tari-ko (rutas, sin heredero), Nubiri-sha (contabilidad social, sin
  heredera), Ita-sha y Moro-ko (saberes intransmisibles por diseño).
- `curiana_sim/curiana_social.py` — leído completo. Confirmó que
  `DifusionLexica` (prestigio × vínculo × co-ubicación) es exactamente la
  maquinaria que el anexo de diseño reutiliza para el pulso ritual, sin
  necesidad de una estructura paralela.
- `curiana_sim/curiana_state.py` — leído completo. Los tres ritos que
  CANON_TIERRA.md menciona (`ceremonia_iniciacion`,
  `ritual_siembra_primeras_lluvias`, `fiesta_cosecha_chicha`) están en
  `EVENTOS_ESTACIONALES`; además se encontraron eventos cotidianos
  relevantes no mencionados en el encargo: `ofrenda_ancestros_anochecer`
  (Bana-mana recitando nombres — el evento clave del anexo de diseño),
  `tejido_y_alfareria` ("el trabajo se enseña mirando", cita literal usada
  en el ensayo), `consulta_piache_sueno`, `duelo_ritual_difunto`.
- `DISENO_KOINE.md` §5 — leído para verificar si `IdiolectoAgente` (la
  "memoria que no expira" que CANON_TIERRA.md pedía) ya existe en código o
  es solo diseño. **Confirmado como código real**: `class IdiolectoAgente`
  existe en `curiana_sim/curiana_koine.py` (línea 179), implementada para
  la koiné léxica. Esto cambia la recomendación del anexo: no hace falta
  construir la estructura, solo conectar el concepto de un rito a ella.

## Fuentes externas — crónicas (`fuentes_caquetios/`)

Minería con `pypdf` (script ad-hoc, no permanente) buscando patrones
`areíto|areyto`, `enseñ*|doctrina|educaci*`, `orator*|elocuen*`,
`memoria|recitar`, `ancianos + enseñ/cuent/refier` sobre el texto extraído
página por página.

- **Jahn (1927), *Los aborígenes del occidente de Venezuela*** —
  **alto rendimiento**. pp. 205-227 (extraídas en texto completo) dieron
  el bloque etnográfico más rico de la sesión: derecho consuetudinario oral
  guajiro (precio de sangre/lágrimas), tabú de nombrar a los muertos
  (severo, a veces capital), adiestramiento masculino temprano en
  arco/monta, reclusión femenina en la pubertad con transmisión densa de
  habilidades domésticas y fiesta de presentación (*ajuitis*),
  matrilinealidad explícita ("antiguamente predominaba la familia
  materna... constituían un definido matriarcado"). Describe guajiros del
  s. XIX-XX, no caquetíos del s. XV — se usa como comparanda arahuaca
  cercana, no como dato directo, siguiendo la misma convención que ya usa
  CULTURA_CAQUETIA.md para Pulowi/Juyá/Wanülüü/Lapü.
- **Anglería (1892 [c.1530]), vol. 4** — **hallazgo puntual de alto
  valor**: p. 236 describe el areíto antillano como genealogía cantada de
  las hazañas del cacique ante toda la comunidad. Comparanda estructural
  directa y atestiguada con `ofrenda_ancestros_anochecer`. Vol. 1 no dio
  nada relevante para este tema (contenido más naturalista/zoológico en
  las páginas muestreadas).
- **Las Casas (1875), *Historia de las Indias*, vol. 1** — **bajo
  rendimiento**. 613 páginas escaneadas por patrón; casi todos los hits de
  "enseñanza/doctrina/oratoria" resultaron ser prólogo apologético sobre
  la historia como género literario, biografía de Colón, o doctrina
  cristiana/catequesis — no pedagogía indígena. No se encontró descripción
  de educación o transmisión de saber entre pueblos indígenas en las
  páginas indexadas por los patrones usados. Coherente con el precedente ya
  documentado en `CLAUDE.md` de que Perea Alonso 1942 tampoco dio
  resultado para la sesión de léxico — no toda fuente del corpus rinde
  para todo tema.
- **Gilij (1782/1782/1783), *Saggio di Storia Americana*** — se intentó
  minar el vol. 3 (arahuacos del Orinoco, relevante en teoría). **Cero
  coincidencias** con los patrones usados (en español; el texto es
  italiano). No se determinó si es ausencia real de contenido relevante o
  falla de extracción de texto (posible capa OCR débil en un facsímil de
  1780s). **Queda abierto**: si se justifica, una pasada dedicada con
  patrones en italiano (`insegna`, `educazione`, `iniziazione`) sobre los
  tres volúmenes de Gilij podría rendir material sobre pedagogía arahuaca
  del Orinoco que esta sesión no alcanzó a extraer.
- **Oviedo y Valdés (1851), *Historia General y Natural de las Indias*,
  vol. 1** — **no se pudo procesar**: el PDF está corrupto o mal formado
  para `pypdf` (`EOF marker not found` / `Stream has ended unexpectedly`,
  incluso con `strict=False`). Es justamente la fuente que Jahn cita como
  autoridad sobre la "puna" como señal de virginidad en las costas de
  Tierra Firme (p. 224 de Jahn) — dato con potencial relevancia directa
  para saberes de género restringidos que no se pudo verificar en la
  fuente primaria. **Queda abierto**: reparar o re-obtener el PDF si se
  quiere minar directamente en sesiones futuras.

## Fuentes externas — web (comparanda wayuu y marco teórico)

- **Jayeechi** (canto narrativo wayuu) — búsqueda directa, resultados
  consistentes entre Academia.edu, ALAI/alainet.org y Radio Nacional de
  Colombia: memoria cantada, aprendizaje por inmersión, rol del
  *jayeechimajachi*. Suficientemente convergente entre fuentes
  independientes como para usarse con confianza razonable pese a no haber
  leído un texto académico completo (solo resúmenes de búsqueda).
- **Ouutsü / piache wayuu y Lapü** — búsqueda directa, resultados
  consistentes (Portal de Lenguas de Colombia/Caro y Cuervo,
  noticialdia.com). Confirma y refina lo que CULTURA_CAQUETIA.md ya tenía
  sobre Lapü citando otras fuentes (blogs de mitología wayuu) — esta
  sesión añade la pieza específica de la **vocación por sueño**, que el
  canon existente no tenía explícita.
- **Amodio, E. y Pérez, L.A. (2006), *Las pautas de crianza del pueblo
  wayuu de Venezuela*** (UNICEF / Ministerio de Educación y Deportes,
  Caracas) — **descargado y leído completo en segunda pasada** (el fetch
  web inicial falló por timeout; la descarga directa del PDF de guao.org
  funcionó — 10 páginas de monografía, texto íntegro extraído con pypdf).
  Resultó la fuente más específica de toda la sesión para el currículo por
  edad, con la ventaja metodológica de que sus datos fueron validados en
  talleres con hombres y mujeres wayuu. Rindió: (1) etapas del desarrollo
  como categorías léxicas nombradas (joüuu/tepichi/jintüloa/jimaüai, más
  la secuencia adulta hasta laulaichon); (2) hitos masculinos con edad
  concreta (5-6 acompaña al tío materno, 8-9 responsabilidades, 10-11
  doma, 12 jinete experto); (3) el tío materno como director de educación
  especializada según aptitud detectada (palabrero, dirigente,
  comerciante); (4) el encierro püülüjütü en detalle curricular (consejo
  de ancianas de madrugada, herencia de plantas medicinales "para dejar a
  sus hijas", telar a los 40 días, duración 3 días-2 años según riqueza)
  y el mito de La Majayura como regulador de la duración del propio rito;
  (5) vocación chamánica por espíritus seyuu/sueños y la historia
  Paurala/Umarala con cambio de nombre al asumir el rol; (6) la
  confirmación casi literal de la premisa del experimento Bana-mana:
  "durante los rituales curativos o los entierros, los niños aprenden los
  cantos y los gestos que tendrán que repetir una vez adultos" (p. 45).
  Generó las entradas transmision-025 a transmision-030 del corpus y la
  reescritura de §2 del ensayo (la matriz de edades pasó de [hipótesis] a
  [reconstruido] con doble comparanda Jahn/Amodio).
- **Vansina, Jan (1985), *Oral Tradition as History*** — no se accedió al
  texto completo (solo resúmenes de motor de búsqueda sobre reseñas y
  fragmentos en Scribd/JSTOR/Internet Archive). La distinción
  "memorizado vs. libre" y el uso de genealogías para datación están
  bien documentados de forma convergente en múltiples reseñas
  independientes, por lo que se cita con confianza razonable, pero es una
  síntesis de segunda mano, no lectura directa del libro.
- **Ong, Walter J. (1982), *Orality and Literacy*** — misma situación que
  Vansina: síntesis de motor de búsqueda sobre reseñas/resúmenes
  (Bookey, blogs académicos, ETEC540), no lectura directa. Los conceptos
  citados (fórmulas, epítetos fijos, pensamiento agregativo) son estándar
  y ampliamente repetidos en la literatura secundaria sobre Ong, por lo
  que el riesgo de tergiversación es bajo, pero de nuevo: de segunda mano.

- **Cuadernillo *Pütchipü'üi, Palabrero Wayuu*** (Mincultura Colombia,
  serie Patrimonio Cultural Inmaterial; basado en la investigación de
  Guerra Curvelo) — **descargado a
  `fuentes_caquetios/GuerraCurvelo_ref_2023_Cuadernillo_Sistema_Normativo_Wayuu_Palabrero.pdf`
  y leído completo en tercera pasada** (22 pp.). Surgió de un lead en la
  bibliografía de Amodio & Pérez: Guerra Curvelo (2002), *La disputa y la
  palabra* (Premio Nacional de Cultura 2001), que resultó ser edición
  impresa sin PDF libre — el cuadernillo es su destilación oficial.
  Rindió: (1) el rol completo del pütchipü'üi (mediador convocado, no
  juez; justicia restitutiva; solo tíos maternos aspiran al oficio;
  etimología pütchi+pü'üi "el que lleva la palabra a todas partes");
  (2) las cinco piezas nombradas del sistema (Anaa Akuaitpaa, Pütchikalü,
  Walaa, Anoutaa, Anajirawaa) y el bastón paliisepai; (3) la ouutsü como
  dualidad complementaria (ojo/visión vs. palabra/oído), las tres
  dimensiones (ii, akuwa'ipa, pulasü) y el ciclo sueño→mito; (4) el
  contraste estructural sociedad segmentaria wayuu vs. cacicazgo
  caquetío ("distan mucho de ser gobernantes autoritarios como los
  caciques"). Generó las entradas transmision-031 a 034 y el
  levantamiento del programa aparte `investigacion/PROGRAMA_WAYUU.md`
  (motivado por la pregunta Manaure-palabrero).

## Lo que quedó abierto

1. **Gilij vol. 3** — pendiente una pasada de minería en italiano;
   potencialmente la fuente más directa sobre pedagogía arahuaca del
   Orinoco de todo el corpus disponible.
2. **Oviedo y Valdés vol. 1** — PDF corrupto, no procesable con las
   herramientas actuales; contiene al menos un dato citado por Jahn
   (la puna como señal de virginidad) con relevancia directa a saberes de
   género restringidos.
3. ~~**Amodio y Pérez, *Pautas de crianza wayuu***~~ — **RESUELTO en
   segunda pasada** (descarga directa + lectura completa, ver arriba).
4. **Vansina y Ong de primera mano** — esta sesión los cita por síntesis
   de reseñas, no por lectura del texto original. Si el proyecto necesita
   apoyarse más fuerte en marco teórico de oralidad (más allá de esta
   sesión), vale la pena conseguir los textos completos.
5. **No se buscó comparanda taína ni lokono específica para transmisión**
   (más allá del areíto antillano, que es genéricamente caribeño/taíno).
   El corpus de Brinton 1871 y Perea Alonso 1942, ya minados en sesiones
   anteriores del proyecto para léxico, no se revisaron de nuevo aquí bajo
   el lente de transmisión — podrían rendir algo distinto si se les
   pregunta específicamente por educación/iniciación.
