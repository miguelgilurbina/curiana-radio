---
tipo: hoja-de-fuentes
sesion: 5
moc: MOC_geografia_politica
---

# Hoja de fuentes — Sesión 5: Geografía política y sucesión

> [[MOC_geografia_politica]] · [[05_geografia_politica_y_sucesion|ensayo]] · [[INDICE_FUENTES]]
> Fuentes: [[oliver-1989-cap3]] · [[zavala-reyes-2015]] · [[oliver-1989-cap2]] · [[arcaya-1920]] · [[van-buurt-2014]] · [[oviedo-y-banos]] · [[ramos-perez-1978]]

*Programa "corpus cultural". Conversación con Miguel, 2026-07-13 a 2026-07-20. A diferencia de las
sesiones 1-4 (lanzadas como spawn_task independientes), esta sesión se desarrolló en vivo, dentro de
la misma conversación, en respuesta a preguntas concretas de Miguel sobre la sucesión de Manaure y la
escala del mundo caquetío.*

## Qué se buscó

1. El significado exacto del término "diao" que Miguel recordaba de Zavala (2015).
2. Confirmación de que "los caquetíos" tenían asentamientos de avanzada comercial en la Guajira
   (Miguel decía que esto estaba en Oliver).
3. El nombre del asentamiento en el que se basó Coro — Miguel lo recordaba como "Todaraquiba" o
   "Todariquiba", sin estar seguro de la ortografía (y ya lo había mencionado, aún más deformado,
   como "Arakiba"/"Arequiba" al inicio de todo el programa "corpus cultural").
4. El testimonio de Américo Vespucio sobre un poblado de "40 casas" sobre palafitos en lo que hoy se
   entiende como el Golfete de Coro ("Puerto de San Bartolomé").
5. Una crónica (Miguel no recordaba cuál) sobre la reconstrucción de una represa/dique que movilizó a
   miles de caquetíos.

## Cómo se buscó

`fuentes_caquetios/Palabras Vivas de una Lengua Muerta.pdf` resultó ser Zavala Reyes (2015) — el
nombre de archivo no lo delataba (ver memoria: el proyecto ya sabía el autor pero no tenía el PDF
localizado como tal). Se confirmó por metadata del PDF (`/Title`, `/Author`, `/Subject`).

Extracción de texto con `pypdf` (sin OCR de por medio; todos los PDFs consultados en esta sesión
tienen capa de texto extraíble, incluidos los dos capítulos de Oliver 1989 — 109 y 113 páginas
respectivamente, ~330K y ~310K caracteres extraídos):

- `Palabras Vivas de una Lengua Muerta.pdf` (Zavala Reyes 2015) — 20 páginas.
- `Chapter 2 Linguistics- Oliver 1989.pdf` — 109 páginas.
- `Chapter 3 Ethnohistory.DOC-comprimido.pdf` (Oliver 1989) — 113 páginas. La fuente principal de
  esta sesión: casi todos los hallazgos geográficos y políticos vienen de aquí.
- `Arcaya_1920_Historia_Estado_Falcon.pdf` — extracción de mala calidad (texto corrido sin espacios en
  buena parte del documento, típico de OCR desigual); se usó solo tangencialmente vía las citas que
  Zavala 2015 ya hace de Arcaya.
- `Jahn_1927_Aborigenes_Occidente_Venezuela.pdf`, `Angleria_1892_Fuentes_Historicas_Colon_America_
  vol1.pdf` — extraídos pero sin hallazgos nuevos relevantes a esta sesión específica (no se buscó
  exhaustivamente en ellos; quedan como candidatos para sesiones futuras).
- `Oviedo_Banhos_1885_Conquista_Venezuela.pdf` — el PDF está vacío/corrupto (`pypdf` reporta "Cannot
  read an empty file"). Pendiente: verificar si hay una copia legible en otro formato.

Nota técnica: la extracción de "Todariquiba" en Oliver sale sistemáticamente como **"T odariquiba"**
(con un espacio espurio tras la T) — artefacto de kerning/ligadura del PDF original, no un error de
transcripción. Confirmado en las ~6 apariciones del término en el capítulo.

Todos los archivos de texto temporales de extracción se generaron y borraron dentro de la misma
sesión (no quedan en el repo — ver advertencia de secretos/OneDrive, que aplica en general a no dejar
basura de trabajo en el árbol del proyecto).

## Qué se encontró

- **Diao** (Zavala 2015, glosario p. 67, entrada 106, fuentes HB+AM): "Señor principal. Jefe mayor" —
  no "de segundo orden" como tenía el lexicón activo sin cita. Confirmado independientemente en
  Oliver 1989 (cap. 3, p. 251): "the main diao or great cacique, Manaure."
- **Apopo** (Zavala 2015, p. 65, entrada 12, AM): "Nombre de jefe de parcialidad pequeña" — no estaba
  en el lexicón; se añadió.
- **Boratio** (Zavala 2015, p. 66, entrada 43, AM+HB): "Piache, cacique, jefe, sacerdote, médico" —
  cruza con el hallazgo ya existente de la sesión 3 (Jahn 1927, vía Oviedo), con glosa más rica.
- **Guajira como puestos de avanzada**: confirmado literalmente en Oliver 1989, cap. 3, p. 189 —
  Miguel tenía razón, y con cita textual ("avant guarde posts... undoubtedly originated from Coastal
  Falcón").
- **Todariquiba**: confirmado en Oliver 1989, cap. 3, p. 251 (pacto de 1527, residencia de Manaure y
  su hijo Alexandre) y recurrente en registros posteriores (carta de Bastidas 1538; Ponce y Vaccari
  1977). Ubicación exacta sin resolver en la literatura misma — Oliver lo dice explícitamente.
- **La represa/dique de miles**: confirmado en Oliver 1989, cap. 3, pp. 262-263, citando a Ballesteros
  [1550] — cifras exactas: 4-5 mil indios para reparar el buco, población de 14-15 mil en el pico,
  colapso a 400 hacia 1550. Es la misma "buco" ya en `curiana_lexicon.py`.
- **Vespucio/San Bartolomé**: confirmado el lugar (Golfete de Coro, no Maracaibo — Ramos Pérez
  1976: 88, vía Oliver 1989 cap. 3, p. 249) y la conexión con el nombre "Venezuela". **NO confirmado**
  el número de "40 casas" — la única cifra similar hallada (40-50) es la capacidad de una maloca en
  Curazao, un lugar distinto. Oliver además deja abierta la relación entre el poblado palafítico y los
  asentamientos caquetíos de tierra adentro.
- **"Curiana" como nombre territorial**: confirmado en la propia nota (4) de Zavala 2015 — "territorio
  donde estaban asentados los caquetíos". Genera una tensión de nomenclatura con el uso ya establecido
  en todo el proyecto (el asentamiento de los 60 agentes), documentada pero no resuelta.
- **Bonus**: nota (2) de Zavala 2015 da cita (González, Carlos, PLINCODE p. 23) para el dato de
  "managuanare/managuarire" que `curiana_agents.py` ya usa sin fuente en la ficha de Manaure.

## Qué quedó abierto

- El número de casas del poblado de Vespucio en el Golfete de Coro (si existe una cifra específica,
  probablemente esté en las propias *Quator Navigationes*/*Lettera* de Vespucio, no consultadas
  directamente en esta sesión).
- Relación exacta entre el poblado palafítico de San Bartolomé y Todariquiba (¿son el mismo
  asentamiento? ¿comunidades distintas dentro del mismo complejo político?) — Oliver mismo lo deja sin
  resolver.
- Ubicación exacta de Todariquiba (debate historiográfico abierto, citado por Oliver vía Ramos 1978;
  no es tarea de este proyecto resolverlo).
- `Oviedo_Banhos_1885_Conquista_Venezuela.pdf` da error al extraer — pendiente de diagnóstico.
- Un hallazgo colateral, no perseguido a fondo en esta sesión: `curiana_lexicon.py` tiene también la
  entrada `"uriacoa": "título del cacique mayor de Curiana/Coro"`, pero el ensayo 01 (familia) ya cita
  a "Don Sancho Uriacoa" como NOMBRE PROPIO de un sucesor colonial específico (Oliver 1989, cap. 3, pp.
  255-256) — la misma clase de error que tenía "diao" antes de esta sesión (una interpretación sin
  cita, posiblemente equivocada). No se corrigió aquí por estar fuera del alcance de lo que Miguel pidió
  consolidar; queda anotado para una revisión futura del lexicón.
- Decisión sobre el nombre "Curiana" (§8 del ensayo) — explícitamente pendiente de Miguel.
