---
tipo: fuente
obra: "El Diao Manaure o la Disección de un Hombre-Dios"
autor: "Antolínez, Gilberto"
anio: 1944
publicacion: "El Universal, Caracas, sábado 9 de septiembre de 1944"
genero: etnologia
paginas: "— (artículo de prensa; no localizado)"
capa_texto: no
estado_minado: segunda-mano
prioridad: media
tareas: [F12]
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-08-25
aliases: ["Antolínez 1944", "El Diao Manaure", "Disección de un Hombre-Dios"]
---

# Antolínez 1944 — *El Diao Manaure o la Disección de un Hombre-Dios*

## Qué es y dónde está

**Artículo de prensa**, no libro: *El Universal*, Caracas, **sábado 9 de
septiembre de 1944**. La referencia exacta la da [[moron-2012-petroglifos]],
que además lo **transcribe verbatim** — así que el pasaje clave ya está en el
repo y esta obra **no bloquea nada**.

Gilberto Antolínez (San Felipe, Yaracuy, 1908) es uno de los precursores de la
antropología académica en Venezuela.

## 🟢 Lo que aporta, y que el canon ya sostiene

> "Los cronistas españoles nos hablan de 'el Manaure'. **Tengo suficientes
> motivos para establecer que Manaure no es nombre propio de varón, sino el
> nombre de una jerarquía política**, tal como otros de la historia, como Inca,
> Minos, Jerjes (Xchatria), Faraón, Czar."

El canon ya lo dice: `manaure` está en `curiana_lexicon.py` como
**caquetío-atestiguado** = *"título laudatorio del señor principal"*, con
variantes *managuanare* / *managuarire*, y en `geografia_politica-008`. Hoy eso
descansa en una nota al pie de [[zavala-reyes-2015]] citando a
[[gonzalez-batista-nombre-de-coro]] (PLINCODE p. 23). Antolínez es un **segundo
testimonio independiente y setenta años anterior**.

Y `diao` —la otra pieza del título de su artículo— es de lo más sólido que
tiene el proyecto: `caquetío-atestiguado` = 'señor principal, jefe mayor', en
`cognados.yaml` con ancla de [[oliver-1989-cap2]]: *"DIAO: Lord or cacique of
the zaquitios territory"*.

## 🔴 Y lo que NO hay que importar: su etimología

Antolínez descompone *Manaure* en cuatro raíces arahuacas, con dos lecturas:

```
Ma  'grande, elevado'  +  Na  'propuesto'  +  Hu  'alto'  +  Ra  'rito'
    -> "el que ha sido propuesto al alto rito"
    -> "propuesto por su alta procedencia"   (variante, con Ra = 'procedencia')
```

**Contrastado contra el propio lexicón del proyecto, no se sostiene:**

| Raíz | Antolínez | El lexicón |
|---|---|---|
| `ma` | 'grande, elevado' | **prefijo privativo** 'sin, carente de' (`caquetío-reconstruido`) |
| `na` | 'propuesto' | **'como, semejante a'** — partícula comparativa, `caquetío-atestiguado`, Zavala #184 |
| `hu` | 'alto, elevado' | **no existe** |
| `ra` | 'rito' / 'procedencia' | **no existe** |

Cuatro morfemas para explicar una palabra, **ninguno atestiguado
independientemente en caquetío**, uno contradiciendo un privativo `ma-` que es
tipológicamente sólido en arahuaco (lokono, wayuu), y dos que no están en
ninguna parte. Es etimología por descomposición libre, no método comparativo.

⚠️ **`na` acumula ya tres glosas incompatibles**, de tres autores:

| Fuente | Glosa | Estado |
|---|---|---|
| Zavala #184 | 'como, semejante a' | **impresa en el glosario** |
| González Batista | 'tierra' | análisis del autor |
| Antolínez 1944 | 'propuesto' | análisis del autor |

Eso pesa en el issue [#109](https://github.com/miguelgilurbina/curiana-radio/issues/109):
tres lecturas rivales para el mismo formante refuerzan mantener la glosa **en
disputa** y la forma intacta, que es la posición corregida de ese issue.

## ⚠️ Reserva sobre el autor, ya registrada en el vault

[[maria-lionza-culto]] y [[03_creencia_caquetia]] documentan que el culto a
María Lionza fue *"en parte inventado"* por Antolínez **entre 1939 y 1945** —
las cortes de espíritus, la estructura del panteón. Este artículo es de **1944**,
justo dentro de esa ventana, y se titula *"Hombre-Dios"*.

La lectura resultante, y creo que es la justa:

- **Su afirmación documental** —Manaure es un título, no un nombre— es
  valiosa, está corroborada por otra vía y entra.
- **Su etimología** es construcción, y no entra.

Es el mismo reparto que hubo que hacer con [[gonzalez-batista-nombre-de-coro]]:
autoridad sobre unas cosas, no sobre otras.

## Dónde conseguirlo

| Vía | Estado |
|---|---|
| **El Universal**, 9-IX-1944 | hemeroteca — Biblioteca Nacional de Venezuela |
| *Hacia el indio y su mundo. Pensamientos vivos del hombre americano* (1946) | libro de dos años después; probable recopilación de sus piezas de prensa de los 40 |
| *Los ciclos de los dioses. Folklore y mitología de centro-occidente de Venezuela* (1995) | compilación de Orlando Barreto, **Editorial la Oruga Luminosa**, San Felipe (Yaracuy). Es donde encajaría el texto |
| *Retratos y figuras* (1997) · *El agujero de la Serpiente* (1998) | los otros dos tomos de la misma compilación |

Ninguna aparece digitalizada. La editorial es local de San Felipe.

**Pero no urge**: el pasaje que importa ya lo tenemos verbatim vía
[[moron-2012-petroglifos]], con fecha y medio. Conseguir el original serviría
para ver si su argumento para "Manaure = título" es **documental** (crónicas,
variantes del término) o **interpretativo** (el arquetipo del héroe cultural) —
que es justo lo que decide cuánto pesa.

## Qué preguntarle si se consigue

1. ¿De qué fuentes coloniales saca que Manaure es título?
2. ¿Registra más variantes además de *managuanare* / *managuarire*?
3. ¿Dice algo de la **sucesión** al cargo? Toca D4
   ([#35](https://github.com/miguelgilurbina/curiana-radio/issues/35)) — que
   tiene más sentido, no menos, si el cargo es un título.
4. ¿Separa al Manaure histórico de Coro (el de Ampíes) del título genérico?

Índice: [[INDICE_FUENTES]] · propuesta: `6-fusion/petroglifos_y_manaure.yaml`
