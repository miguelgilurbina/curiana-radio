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

---

## Ampliación 2026-08-18 — el lexicón también, y el resultado invierte lo esperado

Se extendió la auditoría a las **1.413 entradas del lexicón**
(`curiana_sim/auditar_polity_lexicon.py`, que queda en el repo para repetirla).

**Resultado: solo 7 entradas mencionan otra polity**, 4 de ellas marcadas
caquetío. Y al leerlas enteras, **las cuatro son casos donde el proyecto YA
razonó bien**:

| Entrada | Qué pasa |
|---|---|
| `mene` | La nota ya advierte que *"la cita de Arcaya sobre la Relación de Barquisimeto NO sostiene la glosa de petróleo — quien la sostiene es Alvarado"* |
| `cumaragua` | **D10 ya adjudicó por localización**: Alvarado p.102 la sitúa en *"costas de Paraguaná"*, y la lectura de Barquisimeto queda registrada como descartada |
| `bariki` | Cita la Relación de Barquisimeto **además** de Zavala y Galeotto Cey |
| `sima` | ⚠️ el único flojo — ver abajo |

> **La inversión**: las entradas que nombran otra polity son **las auditadas**.
> Nombran la región precisamente porque alguien estaba siendo cuidadoso. El
> riesgo no está en esas 7 — está en las **219 `caquetío-atestiguado`
> restantes**, que citan a Zavala, Alvarado u Oviedo **sin decir de qué región
> procede la atestación**.
>
> Es decir: el barrido por texto **no puede medir esto**, porque el dato no está
> escrito. Es el mismo argumento que la sección anterior, ahora con número:
> **7 medibles de 1.413**. Sin un campo obligatorio, la regla 4 seguirá sin ser
> comprobable ni en el corpus ni en el lexicón.

### 🔴 `sima` — la que sí está floja, y toca D9

```python
"sima": {"sig": "cerro, montaña, elevación",
         "fuente": "caquetío-reconstruido",
         "notas": "núcleo fundacional, forma justificada por cognado en
                   lokono/topónimo (Barquisimeto)"}
```

Una palabra del **núcleo fundacional** cuya única justificación toponímica es
**de Barquisimeto**, es decir de la otra polity.

**Y hay una consecuencia que nadie había notado.** El motor enseña este
compuesto en sus prompts y lo usa como ejemplo canónico de acuñación:

```
curiana_lexicon.py:6863   [sima-bana: sima+-bana = orilla del cerro]
curiana_lexicon.py:7548   ídem, en el prompt
curiana_social.py:269-272 Shaboro acuña [sima-bana]; se propaga a Buio-sha
                          — es el fixture del test de contagio léxico
```

`sima-bana` = 'orilla del cerro' **solo funciona si `-bana` significa 'orilla'**.

> ⚠️ **Si D9 (#38) resuelve que `bana` = 'cerro', entonces `sima-bana` =
> 'cerro-cerro'**, y el ejemplo insignia de neologismo del motor —el que además
> usa el test de contagio— deja de tener sentido y hay que reescribirlo.
>
> Añádase al radio de impacto de D9, que ya iba por nueve archivos.
