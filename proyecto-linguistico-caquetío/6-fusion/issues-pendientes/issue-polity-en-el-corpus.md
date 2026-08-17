El corpus etiqueta la *certeza* de cada hecho pero no *de qué polity* es

## Lo que destapó §3.8 de Oliver

La regla 4 dice que los caquetíos no eran una sola sociedad y que modelamos la
**costera**. Oliver la argumenta en §3.8 (pp. impresas 290-294), y las
diferencias no son de matiz:

| | Costero (el que simulamos) | Barquisimeto-Yaracuy |
|---|---|---|
| Jefatura | **tenía jefe paramount** (el diao) | *"clearly had **no** paramount chief"* |
| Guerra | menos beligerante | *"extremely bellicose"* |
| Riqueza | redistribuida | acumulada, no redistribuida |

Y advierte de un rito cuya descripción menciona el río de Barquisimeto: *"this
is probably a **Barquisimeto Caquetío** ritual"*. O sea: **hay material en las
crónicas que es de la otra polity y no viene etiquetado como tal**.

## La auditoría: 7 de 112 hechos mencionan otra polity

Barrido de los seis archivos de `3-mundo/corpus/` buscando Barquisimeto, Nueva
Segovia, Yaracuy, Turbio, Nirgua, El Tocuyo, Carora, Quíbor, Llanos, Apure y
otros topónimos que §3.7-3.8 asigna fuera de la costa:

| Archivo | Hechos marcados |
|---|---|
| creencia | 4 de 26 |
| parentesco | 3 de 39 |
| transmisión, genealogía, geografía política, ecología | 0 |

## 🔴 El caso claro: `creencia-004`

```yaml
- id: creencia-004
  contenido: >
    El piache se forma con ayuno prolongado. En la región (Nueva Segovia /
    Barquisimeto) el médico-hechicero adquiría su carácter "mediante prolongado
    ayuno" y se reconocía porque traía "los cabellos muy largos como una mujer".
  fuente: atestiguado
  referencia: "Arcaya 1920:101 (Relación de Nueva Segovia); Perrin 1995"
  implicacion_simulacion: >
    Refuerza el arco de Buio-sha ... y da rasgo físico atestiguado: el piache
    lleva el pelo muy largo.
```

**Nueva Segovia es Barquisimeto.** El hecho es honesto —lo dice en su propio
contenido— pero está marcado `atestiguado` y su `implicacion_simulacion` lo
aplica a la costa como *"rasgo físico atestiguado"*. Un detalle ritual de la
polity que Oliver describe como políticamente distinta se convirtió en rasgo
del piache costero.

## Y el caso que lo hace bien: `parentesco-037`

```
... Barquisimeto y Yaracuy son evidencia de una esfera CULTURAL caquetía
amplia, NO de vasallaje político directo a Manaure ...
fuente: reconstruido
```

Distingue polities explícitamente y se degrada a `reconstruido`. **Alguien lo
hizo bien a mano.** Ese es justo el problema.

## El diagnóstico: falta una dimensión en el esquema

El corpus tiene etiqueta epistémica (`atestiguado`/`reconstruido`/`hipotetico`/
`retro-abstraido`) que responde **"¿cuánta certeza?"**. No tiene ninguna que
responda **"¿certeza sobre QUIÉN?"**.

`atestiguado` no distingue hoy entre:
- atestiguado **para la polity costera** — utilizable directo;
- atestiguado **para otra polity caquetía** — importable solo declarándolo;
- atestiguado **para otro pueblo** (wayuu, achagua, jirajarano) — comparanda.

Es el mismo hueco que tenía la bibliografía antes de que `procedencia.obra` se
volviera clave foránea: el dato estaba, pero no se podía validar ni medir.

## Propuesta

1. **Campo `polity`** en los hechos del corpus:
   `costera` · `barquisimeto-yaracuy` · `llanos` · `insular` · `pan-caquetio`
   · `otro-pueblo`. Por defecto **nada**, para que `compilar_corpus.py --check`
   pueda contar cuántos hechos no lo declaran, como se hizo con las citas.
2. **Revisar los 7 marcados**, empezando por `creencia-004`: ¿se degrada a
   `reconstruido` (proyectado desde otra polity), se conserva `atestiguado`
   marcando `polity: barquisimeto-yaracuy`, o se retira de la simulación?
3. **Revisar `parentesco-021`** aparte: es sobre los caquetíos **llaneros** y
   se usa para legitimar la etnografía achagua como comparanda de primer orden
   de "la familia caquetía". El argumento es de familia lingüística (Jahn) y
   puede valer igual, pero cruza polities y conviene decirlo.
4. Cuando el campo exista, medirlo en el TABLERO como se mide la deuda de citas.

## Por qué esto importa más que los 7 hechos

Se encontraron 7 buscando topónimos en el texto. **Los peligrosos son los que
no mencionan la región**: material de Barquisimeto que las crónicas no
geolocalizan y que entró como caquetío a secas. Sin un campo que obligue a
declarar la polity, no hay forma de medir cuántos son — y la regla 4 seguirá
siendo una advertencia en el CLAUDE.md en vez de una restricción comprobable.

Fuente: `4-fuentes/oliver-1989-cap3-vecinos.md` §3.8.
