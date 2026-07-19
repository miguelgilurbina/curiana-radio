# Programa de investigación: la sociedad wayuu a fondo

*Levantado el 2026-07-19, al cierre de la sesión 4 del corpus cultural.
Estado: **planificado, no iniciado**. Este documento es el andamiaje del
programa, no su resultado.*

## Por qué

El corpus cultural de Curiana usa a los wayuu como la comparanda arahuaca
más pesada (lengua hermana más documentada, 781 palabras wayunaiki en el
lexicón, mitología Pulowi/Juyá/Lapü ya en el canon), pero hasta ahora la
hemos consultado **por fragmentos**: un mito aquí, un rito allá, según lo
pedía cada sesión temática. Tres hallazgos de la sesión 4 justifican una
investigación dedicada:

1. **El sistema normativo wayuu es un sistema completo**, no un dato
   suelto: ley (Anaa Akuaitpaa), palabra (Pütchikalü), compensación
   simbólica (Walaa), reequilibrio (Anoutaa), reconciliación (Anajirawaa),
   con dos oficios complementarios — pütchipü'üi (palabrero, la palabra/el
   oír) y ouutsü (visionaria, el ojo/el ver). Patrimonio Inmaterial de la
   Humanidad (UNESCO 2010). Merece estudio estructural, no minería puntual.
2. **La pregunta Manaure-palabrero.** El Manaure histórico ejerció el
   repertorio del palabrero (negociar, compensar, pactar — Castellanos lo
   retrata como estadista) pero desde la autoridad cacical, no desde la
   neutralidad. La sociedad wayuu no tiene caciques; la caquetía fue un
   cacicazgo. ¿Qué pasa con la función mediadora cuando una sociedad
   arahuaca se jerarquiza? Esta es LA pregunta comparativa del programa —
   y decide si el elenco necesita un personaje nuevo (ver
   `curiana_sim/cultura/transmision.yaml`, entrada transmision-034).
3. **El ciclo sueño → mito.** "Muchos de los mitos e historias más
   importantes para los Wayuu han sido extraídos de sueños comunicados por
   las mujeres Ouutsü" (cuadernillo Mincultura). La tradición oral wayuu no
   solo conserva — PRODUCE relato desde el sueño interpretado en público.
   Para una simulación que quiere ver emerger cultura, este es el
   mecanismo generativo más prometedor que hemos encontrado.

## Sub-preguntas

- **Organización social:** clanes matrilineales (sibs) tendencialmente
  endogámicos, linajes matrilocales, el apüshi (parentela uterina), la
  "carne" vs. la "sangre" (concarnidad vs. consanguinidad), el talaula
  (tío materno) como autoridad no-autoritaria. ¿Qué de esto proyecta el
  canon caquetío hacia atrás y qué NO debe proyectar (ver advertencia
  metodológica)?
- **El sistema normativo completo:** tipología de ofensas y compensaciones,
  formación del palabrero (¿cómo se aprende el oficio? — conecta con la
  sesión 4 de transmisión), el duelo de oradores, el papel de las mujeres
  en las disputas. Fuente central: Guerra Curvelo 2002 (libro impreso, no
  hay PDF libre — ver hoja de fuentes 04).
- **Ouutsü, sueños y producción de mitología:** Lapü, los seyuu, el ciclo
  sueño-interpretación-relato-arquetipo, la relación ouutsü/palabrero como
  dualidad ver/oír.
- **Economía y territorio:** qué es precontacto (pesca, sal, horticultura,
  intercambio) y qué es colonial (¡el pastoralismo entero!: chivos,
  caballos, la dote en ganado). El wayuu etnográfico es un pueblo PASTOR
  — el caquetío del siglo XV no pudo serlo. Cada análisis del programa
  debe pasar por este filtro.
- **Léxico:** el wayunaiki como cantera comparativa ya se usa en
  `arahuaco_comparative.py`; ¿qué campos semánticos del sistema normativo
  (pütchi, walaa, anoutaa...) tienen cognados caquetíos plausibles?

## Fuentes identificadas (por prioridad)

1. **Guerra Curvelo, W. (2002), *La disputa y la palabra: la ley en la
   sociedad wayuu*** — Ministerio de Cultura, Bogotá. 327 pp. Premio
   Nacional de Cultura 2001. **Impreso, sin PDF libre** (catálogos:
   Stanford, ICANH, WorldCat). Sustitutos ya descargados/localizados:
   - `fuentes_caquetios/GuerraCurvelo_ref_2023_Cuadernillo_Sistema_Normativo_Wayuu_Palabrero.pdf`
     (Mincultura, 22 pp., **ya minado en sesión 4**).
   - Catálogo "Pütchipü'ü: el oficio de la palabra entre los wayuu"
     (Cervantes Virtual / Museo del Oro 2014, del propio Guerra Curvelo).
   - Guerra Curvelo relata el mito del pájaro Utta, primer palabrero
     (Cervantes Virtual, "La paz se cuenta" nº 2).
2. **Perrin, M. (1980), *El camino de los indios muertos*** — Monte Ávila,
   Caracas. La monografía clásica sobre mitología y sueño wayuu (en la
   bibliografía de Amodio & Pérez).
3. **Goulet, J. (1981), "El universo social y religioso guajiro"**,
   Montalbán 11 — la etnografía social de referencia en Venezuela.
4. **Saler, B. (1988), "Los Wayú (Guajiro)"**, en Lizot (ed.), *Los
   Aborígenes de Venezuela*, t. III, Fundación La Salle.
5. **Jusayú, M. (1977), *Diccionario de la Lengua Guajira*** (2 tomos,
   UCAB) — para la pata léxica.
6. **Amodio & Pérez (2006)** — ya leído completo (sesión 4); su
   bibliografía es el semillero de todo lo anterior.
7. Repositorios académicos con PDF libre sobre el palabrero (Uniguajira,
   UAC, redalyc) — localizados en la búsqueda de sesión 4, sin leer aún.

## Advertencia metodológica (no negociable)

Rige [[feedback_precontacto-vs-colonial]] y la práctica de las 4 sesiones
del corpus: **el wayuu etnográfico (s. XIX-XXI) no es el caquetío del
s. XV.** El pastoralismo, el caballo, la dote en ganado, el contrabando y
la dualidad binacional son todos post-contacto. Lo que se compara es la
**estructura** (matrilinealidad, mediación, compensación, sueño) y no el
**contenido material** (chivos, rifles, bolívares). Toda entrada que salga
de este programa se etiqueta con el esquema de 4 niveles del corpus
cultural, y en duda, se degrada.

## Forma propuesta

Mismo formato que el corpus cultural: sesiones temáticas con mini-ensayo +
corpus YAML (`curiana_sim/cultura/wayuu_*.yaml` o integrando a los
existentes) + hoja de fuentes. Estimación: 2-3 sesiones (1: sistema
normativo y palabrero; 2: ouutsü/sueños/mitopoiesis; 3 opcional: síntesis
comparativa cacicazgo vs. sociedad segmentaria → decisión de diseño sobre
el personaje mediador).
