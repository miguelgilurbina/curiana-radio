---
tipo: fuente
obra: "The Aruba Language and the Papiamento Jargon"
autor: "Gatschet, Albert S. (material recogido por Alphonse L. Pinart, 1882)"
anio: 1885
publicacion: "Proceedings of the American Philosophical Society (leído el 18 de julio de 1884)"
genero: vocabulario
local: ["fuentes_caquetios/Gatschet_1885_Aruba_texto.txt", "fuentes_caquetios/Gatschet_1885_biostor_texto.txt"]
paginas: "~10 (dos OCR del mismo artículo)"
capa_texto: si
estado_minado: sin-minar
prioridad: alta
tareas: [F4]
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-07-29
aliases: ["Gatschet 1885", "Pinart 1882", "The Aruba Language"]
---

# Gatschet 1885 — *The Aruba Language and the Papiamento Jargon*

## Qué es

**Vocabulario caquetío insular directo**, recogido en 1882 por Alphonse Pinart
*de hablantes ancianos de Aruba* cuando la lengua ya estaba extinguiéndose
(los arubanos habían abandonado su lengua por el papiamento hacia 1800). Gatschet
lo publica con su propio análisis comparativo.

Su relevancia para el proyecto está en una sola frase del artículo: *"The Aruban
language was probably the same as that of Curaçao and **related to the vernacular
of the peninsula of Paraguaná**"* — es decir, el caquetío del Golfete.

## Estado técnico (verificado 2026-07-29)

| Dato | Valor |
|---|---|
| Formato | **dos .txt** (18 KB y 17 KB): **el mismo artículo**, dos OCR distintos (JSTOR Early Journal Content y BioStor) |
| Capa de texto | sí — es texto plano |
| Artefacto | Ambos arrancan a mitad de **otro** artículo (química de aceites de 1884); el contenido útil empieza en *"THE ARUBA LANGUAGE AND THE PAPIAMENTO JARGON"* (línea 77 del archivo Aruba) |
| Recomendación | Usar los **dos** en paralelo: donde uno tiene OCR sucio, el otro suele resolver |

## Qué contiene (inventariado hoy, nunca minado)

- **~13 nombres, verbos y frases**: `kafa` (devil/espíritu maligno), `datie!`
  (be gone!), `karebe` (spoon), `kanla` (thing), `totumba`/`waidanga` (water
  gourd), `danshikki`/`danshebu` (sack), `xovam` (phantom), fórmulas de saludo
  (*tida meo!* "good morning", *ute kontabo?* "how do you do?").
- **31 topónimos**: 14 montañas (Yamanota, Tarabana, Shiribana, Wakubana,
  Kibaima…), 3 cuevas, 14 lugares (Arikurari, Kamakuri, Kassibari…).
- **13 plantas con identificación taxonómica**: `dividivi`, `kaduski`,
  `watapana`, `shimaruko`, `jobo`, `makura`, `nandu`, `lokiloki`…
- **4 peces, 4 aves, 9 insectos y otros animales**: `warawara`, `shushubi`,
  `kinikini`, `dori`, `kumexen`, `waltaka`…
- **5 fórmulas de hechicería** (maledicción; asustar niños; sacar espinas de
  cactus ×2; sacar espinas de pescado; cazar la iguana). Pinart insistió a
  Gatschet en que son **citas literales de la lengua arubana extinta**, no
  sílabas sin sentido — aunque no consiguió traducción palabra por palabra.

> 🔎 **Varias de estas formas ya están en `curiana_lexicon.py`** llegadas por
> otra vía (`watapana`, `kadushi`, `warawara`, `chuchubi`, `dividivi`). Que una
> fuente independiente de 1882 las atestigüe **en Aruba** es exactamente el tipo
> de confirmación cruzada que el eje FIDELIDAD busca — y hoy **ninguna entrada
> del lexicón cita a Gatschet**.

## El caveat que la propia fuente pone (y hay que respetar)

Gatschet intentó clasificar el arubano dentro de alguna familia lingüística
vecina **y falló**: comparándolo con goajiro, guamaco, arawak, tupí y el caribe
insular de Breton (1665), *"all the other terms differed entirely from Aruba"*.
Solo dos correspondencias: `kafa` (diablo) ~ goajiro *yaria/yarias*, y
`hanahana` (hormiga) ~ caribe insular *hage*. Atribuye el fracaso a lo raro de
la selección de términos, a su escasez y a su probable deformación en boca de
hablantes no instruidos.

Y [[van-buurt-2014]] añade una crítica directa: la lista de Pinart *"contains
several words which are definitely not Indian"*. **Minar esta fuente sin filtro
sería el error clásico del proyecto.** Etiquetar con la misma disciplina de
[[02_protocolo_habla_paraguanera]].

## Qué falta — **F4, prioridad ALTA**

1. Transcribir las listas a estructura (`forma / glosa / taxón / categoría`).
2. Cruzar contra `VOCABULARIO_BASE`: qué ya está (y debería citar aquí), qué
   falta, qué contradice.
3. Cruzar contra [[van-buurt-2014]] (que trabaja el mismo corpus insular 130
   años después) y marcar las que él considera "definitely not Indian".
4. Decidir qué hacer con los **topónimos arubanos**: son morfología caquetía
   viva (`-bana`, `-bari`, `-kuri`, `-ima`) y podrían validar `REGLAS_ZAVALA`.
5. Las **5 fórmulas** son material de primer orden para [[MOC_creencia]] y para
   el habla del piache — con etiqueta prudente: texto no traducible.

## Enlaces

[[van-buurt-2014]] · [[alvarado-1921]] · [[zavala-reyes-2015]] ·
[[MOC_motor]] · [[MOC_geografia_politica]] · [[INDICE_FUENTES]]
