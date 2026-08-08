---
tipo: nota
pregunta: "¿Se puede contar esto desde dentro sin inventarlo?"
motor: curiana_sim/curiana_cronista.py
sustituciones: 8
medido: 2026-08-06
---

# El cronista — contar desde dentro sin inventar

> `python curiana_sim/curiana_cronista.py --glosario` · `--check` verifica la
> tabla contra el lexicón y la bibliografía.

## El problema, y no es ideológico

Todo lo que sabemos del caquetío llega en la lengua y las categorías de quien
vino a conquistarlo. Eso no es una queja: es medible, y este proyecto ya se lo
venía encontrando de frente sin llamarlo por su nombre.

- **Oviedo y Valdés describe la cura del boratio y llama truco al paso final**
  (*"sin que ninguno lo vea"*, *"para hacerlo creer al enfermo"*). La extracción
  del objeto patógeno está documentada en medio continente. El dato del rito es
  utilizable; **el juicio sobre el rito, no** — eso ya estaba escrito en
  [[arcaya-1920]] antes de que existiera esta nota.
- **Oliver compara Barquisimeto con el *Big Man* melanesio**, y él mismo rechaza
  el "Cacicazgo Teocrático" de Steward y Faron porque *"blurs the differences
  that make a difference"*: una tipología occidental aplanando lo que quería
  describir.
- **Las palabras mismas.** `piache` es voz cháima y tamanaca que difundieron los
  españoles ([[jahn-1927]] n.28, corroborando a [[alvarado-1921]]); `cacique` es
  taína. Ninguna de las dos es caquetía. Las suyas son `boratio`, `diao`,
  `apopo` — y el proyecto ya las tenía.
- **Y las glosas del propio lexicón arrastran el marco**: `capu` se glosa como
  *"demonio"*, que es la palabra de Oviedo; `buio` como *"diablo, dios del mal"*,
  que son categorías cristianas.

Ese último punto es el que más dice: **guardábamos las palabras correctas y las
explicábamos con el vocabulario del colonizador.**

## Lo que este cronista NO es

**No recupera la voz caquetía.** No se puede: la lengua está extinta y no existe
un solo texto escrito por un caquetío. Lo que hay es lo que escribieron sus
conquistadores. Cualquiera que diga que entrega "la mirada caquetía" está
fabricando, y este proyecto no hace eso — es justo lo que lo separa de la
fanfiction.

## Lo que sí hace, y es comprobable

1. **Nombrar con sus palabras** donde las tenemos atestiguadas.
2. **Quitar el juicio del observador** y quedarse con lo observado.
3. **Poner en el centro sus preguntas** —la lluvia, la sal, el agua, el linaje
   de la madre, dónde queda el `barsure` de los muertos— en vez de las del
   cronista español: el oro, la sumisión, la idolatría.
4. **Decir cuándo no sabemos.** «No sé», «se cuenta que» y «los viejos dicen»
   significan tres cosas distintas, y el cronista las distingue.

Y una cosa más, que es la única continuidad real que existe: **Paraguaná**. No
es la voz de ellos, pero es la misma tierra, el mismo mar, y voces que
sobrevivieron en el habla de la región. Ver
[[02_protocolo_habla_paraguanera]].

## La tabla, que es lo operativo

Ocho sustituciones, cada una con de dónde viene la palabra ajena y quién lo
dice. **`--check` verifica que la palabra propuesta exista en el lexicón, que la
ajena no esté en el habla activa como caquetía, y que la obra citada esté en la
bibliografía.** Sin esa verificación sería una opinión; con ella es una
afirmación sobre el dato que se cae sola si el dato cambia.

| La fuente dice | Nosotros decimos | Por qué |
|---|---|---|
| piache | **boratio** | voz cháima y tamanaca, difundida por los españoles |
| cacique | **diao** (y `apopo`) | voz taína; «cacique» aplana dos cargos en uno |
| demonio | **capu** | categoría cristiana. Y le dieron ese nombre **a los españoles también** |
| hechicero, brujería | **boratio** | juicio del cronista sobre un oficio de médico y adivino |
| ídolo, idolatría | *(no hay)* | Arcaya mismo anota que no había culto comunal ni templos |
| tribu, cacicazgo teocrático | **polity** (4) | tipología de Steward y Faron que Oliver rechaza |
| vasallo, súbdito | *(no hay)* | a Manaure lo llevaban «en hombros de caciques»: señores, no criados |
| el desierto, la tierra estéril | **biro · para · duna** | veredicto agrícola español. Para quien vive de la sal y del mar, esa costa es rica |

La última fila es la que más rinde narrativamente: **la pobreza estaba en los
ojos de quien buscaba trigo.**

## El límite duro

> **Lo que el cronista dice NUNCA es un dato.** Es una lectura. No entra al
> corpus, no se cita como fuente, no asciende de etiqueta.

Si algo que dijo el cronista acaba en `3-mundo/corpus/` como `atestiguado`, el
proyecto pierde lo que lo hacía investigación. Hay tests que fijan esa regla en
el prompt, incluido uno que comprueba que **no promete recuperar la voz
caquetía**.

Y una prohibición más, que no es epistémica sino de tono: **no romantizar**. Hay
hambre, hay raids que se llevan mujeres, hay muertos. Contar desde dentro no es
contar bonito — es la misma regla anti-romantización que ya tenía
[[CULTURA_CAQUETIA]] §7.

## Por dónde seguir

1. **Cablearlo al motor.** Hoy el prompt existe y nadie lo invoca; el sitio
   natural es un reporte de fin de run que cuente el año desde dentro, al lado
   del reporte analítico que ya existe.
2. **Ampliar la tabla** conforme aparezcan más marcos importados. Candidatos que
   ya se han visto: «naboria», «provincia», «señor de vasallos».
3. **Limpiar las glosas del lexicón.** `capu` = "demonio" y `buio` = "diablo,
   dios del mal" siguen escritas en el marco ajeno. Es una decisión de canon,
   porque toca 1413 entradas y el scoring.
4. **La sesión de Paraguaná**, que es la continuidad real y sigue pendiente.

## Enlaces

[[CULTURA_CAQUETIA]] · [[polities-caquetias]] · [[arcaya-1920]] · [[jahn-1927]] · [[02_protocolo_habla_paraguanera]] · [[mapa-creencia]]
