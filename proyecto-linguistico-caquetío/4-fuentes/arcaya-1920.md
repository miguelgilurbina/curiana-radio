---
tipo: fuente
obra: "Historia del Estado Falcón, tomo I"
autor: "Arcaya, Pedro Manuel"
anio: 1920
genero: cronica-historia-regional
local: "fuentes_caquetios/Arcaya_1920_Historia_Estado_Falcon.pdf"
paginas: 348
capa_texto: si
estado_minado: minado
prioridad: media
cobertura: "religion/familia (sesion 3) + pp. 97-100, el oficio del boratio (2026-08-04)"
sostiene: {hechos_corpus: 13, entradas_lexicon: 1, ritos_documentados: 3}
verificado: 2026-08-04
minado: 2026-08-04
aliases: ["Arcaya 1920", "Historia del Estado Falcón"]
---

# Arcaya 1920 — *Historia del Estado Falcón*

## Qué es

**La fuente falconiana más directa.** Historia regional de 1920 cuyo capítulo
sobre religión trata específicamente a **los caquetíos de Coro** y cita a Oviedo
y Valdés casi verbatim — lo que la convierte, en la práctica, en nuestro acceso
a un Oviedo que **no tenemos legible** ([[oviedo-y-valdes-1851]]).

## Estado técnico (verificado 2026-07-29)

| Dato | Valor |
|---|---|
| Tamaño | 15.4 MB · 348 páginas |
| Capa de texto | **sí** (OCR desigual pero utilizable; 467K caracteres) |
| Receta | **`pdftotext -enc UTF-8`** — `pypdf` devuelve vacío en este archivo |

> 📌 **Lección técnica del proyecto, nacida aquí**: cuando `pypdf` devuelva
> vacío, **probar `pdftotext` antes de declarar un PDF ilegible**. Este archivo
> estuvo clasificado como "extracción de mala calidad / requiere OCR externo"
> hasta que la sesión 3 lo minó íntegro con Poppler.

## Qué ha dado — 13 hechos, el pilar de [[mapa-creencia]]

- **pp. 48, 116, 118** — **`boratio`** (médico-hechicero) y **`díao`/`diao`**
  (*tiao* en Apure): el cacique principal que es a la vez boratio, *"cuyos
  poderes mágicos le daban el carácter de jefe de la tribu"*. Arcaya lee ahí una
  **"monarquía teocrática" en formación** → respaldo documental directo del
  modelo de Manaure, independiente del dato de las tormentas.
- **pp. 116-118** (citando Oviedo t. II, 299-300) — **el segundo entierro
  caquetío atestiguado**: al cacique común lo lloran cantando sus hazañas, lo
  queman, muelen los huesos y los beben en mazamorra de maíz; al **díao**, rito
  de dos tiempos — desecación sobre brasas en hamaca, casa abandonada, años de
  espera hasta que "el cuerpo se descoyunta", y luego "llamamiento general" para
  **"beber los huesos del díao"** en vino de maíz, pintados de bija y jagua.
- **p. 101** — el piache se forma *"mediante prolongado ayuno"* y se reconoce
  por *"los cabellos muy largos como una mujer"* (Relación de Nueva Segovia).
- **p. 118** (Oviedo t. II, 329) — ayuno ritual antes de guerra o empresa grave.
- **pp. 103, 110** — **sin culto comunal de ídolos ni templos**: los invocan
  especialistas, no la tribu.
- **pp. 104-117** — muertos temidos, muerte por brujería, alma que ronda la
  sepultura; ajuar funerario *"para que no le falte nada en la otra vida"*.
- **pp. 119, 127-128** — *"Respecto de las instituciones familiares de los
  indios de Coro, **nada nos dicen los cronistas**"*; poligamia inferida "al
  estilo de sus afines de Casanare y el Meta" (= los achagua); bodas cacicales
  con grandes fiestas; el tatuaje como posible marca de **clan**, no de rango.

## Las pp. 97-100, que el primer minado no registró (2026-08-04)

La sesión 3 sacó de aquí 13 hechos, pero citó pp. 48, 101, 103-118 y **saltó el
bloque de pp. 97-100**, que es la descripción de oficio más detallada que el
proyecto tiene de nada. Arcaya cita ahí, casi verbatim y en extenso, a **Oviedo
y Valdés, *Historia General y Natural de las Indias*, t. II p. 298** — el
volumen que el repo no tiene legible.

### El boratio como oráculo

- *"Estos boratios son como sacerdotes suyos, y **en cada pueblo principal hay
  un boratio**"*, a quien todos acuden.
- **Qué se le pregunta**: si lloverá, si el año será seco o abundante, si deben
  ir a la guerra contra sus enemigos o dejarlo de hacer, y —ya en 1500— *"si los
  christianos son buenos, o si los matarán"*.
- **Cómo responde**: se encierra **solo en un buhío** y toma *"unas ahumadas que
  llaman tabaco con tales hierbas que le sacan el sentido"*; está **uno, dos,
  tres días o más** sin salir, y al salir dice *"aquesto me dixo el diablo"*.
- **Cobra**: *"por este trabajo le dan alguna joya de oro e otras cosas"*.
- **Iconografía**: *"pintan su figura en sus joyas y en madera […] y en todas
  las cosas y partes que más estiman"*.

### 🟢 "Cada uno es boratio" — la adivinación doméstica

El hallazgo con más rendimiento para la simulación. Para las preguntas
pequeñas —si caminarán o irán a pescar o sembrarán, si matarán caza, **"si su
muger los quiere bien"**— no hace falta especialista: *"cada uno es boratio"*.

El procedimiento: se envuelven hojas de tabaco alrededor de una **mazorca de
maíz**, se enciende un extremo, se mete lo que arde en la boca y se sopla hacia
fuera. A la mitad, se lee la ceniza:

| La quemadura queda… | Significa |
|---|---|
| **curva, "hecha a manera de hoz"** | lo que se quiere saber sucederá bien |
| **recta** | al revés de lo que desea, "y que es malo lo que había de ser bueno" |

Y lo creen tan firmemente *"que no basta nadie ni razón alguna a le hacer creer
otra cosa; antes les pesa mucho con quien los desengaña"*.

> Es un rito **que cualquier agente puede ejecutar**, con objetos que el mundo
> de la simulación ya tiene (tabaco, mazorca, fuego), sobre preguntas que los
> agentes ya se hacen. De todo lo minado esta noche, es lo más directamente
> jugable.

### La cura, paso a paso

1. Pregunta qué le duele **y si el enfermo cree que él puede sanarlo, "porque es
   muy buen boratio"**. Si el enfermo dice que no, **el boratio se va y no lo
   cura**. La fe del paciente es condición de entrada.
2. Manda **ayunar a toda la casa**: solo *"mazamorra rala de mahiz que ellos
   llaman **cazá**"*, una vez al día. ← confirma y contextualiza la entrada
   `cazá` del lexicón: es la comida del ayuno.
3. Pasa las manos abriéndolas y cerrándolas sobre el miembro dolorido, *"como
   quien quiere juntar otra cosa"*, y dice que **"le allega el alma a un cabo"**
   — le junta el alma en un punto. ← la palabra caquetía para eso es
   `barsure` ('alma, esencia vital'), ya en el lexicón.
4. Cierra el puño, sopla y dice: **"allá irás mal"**.
5. Grita y chilla sobre el enfermo **hasta quedar ronco**, dos horas o más.
6. Si sigue el dolor, **chupa** el miembro con la boca, escupiendo cada tanto,
   durante cinco o seis días.
7. Al final saca de la boca una **espina, piedra o palo** que llevaba escondido
   y lo muestra: **"Cata aquí lo que te mataba y causó el mal que tenías"**.
   Cobra y se despide.

⚠️ **Oviedo es un observador hostil** y describe el paso 7 explícitamente como
truco (*"sin que ninguno lo vea"*, *"para hacerlo creer al enfermo"*). El dato
del rito es utilizable; **el juicio sobre el rito, no**. La extracción del objeto
patógeno es un rasgo chamánico americano ampliamente documentado, no una estafa
local.

### Lo que esto corrige del modelo de polities

Que la costa tenga **boratios de pueblo** no contradice que su diao sea gran
chamán: **son dos niveles del mismo sistema**, y la fuente los describe juntos.
Lo que distingue a la costa de Barquisimeto es que allí el jefe *también*
profetiza — no que no haya especialistas. Ver [[polities-caquetias]]; el rasgo
`religion` de la polity costera se reescribió con esto.

## Qué falta

- **Barrido no religioso ni familiar**: economía, sal, guerra, comercio. Se minó
  íntegro *a texto*, pero solo se le hicieron preguntas de dos sesiones.
- Arcaya es a la vez fuente y **compilador citado por [[zavala-reyes-2015]]** —
  al verificar citas (F10) hay que distinguir qué llega directo y qué de tercera
  mano.
- Solo **1 entrada del lexicón lo cita**, pese a ser fuente de siglas (PMA) en
  el glosario de Zavala.

## Enlaces

[[03_creencia_caquetia]] · [[oviedo-y-valdes-1851]] · [[jahn-1927]] · [[zavala-reyes-2015]]
