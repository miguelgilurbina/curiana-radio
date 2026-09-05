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
estado_minado: en-curso
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

## Enlaces

[[02_protocolo_habla_paraguanera]] · [[esteves-1989]] ·
[[oliver-1989-apendice-a]] · [[metodo-comparativo]] · [[lexicon]]
