---
tipo: nota
pregunta: "¿Qué preguntó este experimento, qué contestó y qué no puede contestar?"
ambito: fase 1 — los 23 runs del 2026-06-21 al 2026-07-06
medido: 2026-08-08
cierra: la primera fase del experimento
---

# Hallazgos de la fase 1 — el marco científico

> **Qué es esta nota.** El cierre de la primera fase. No un resumen de lo hecho
> —eso está en [[LINEA_DE_TIEMPO]]— sino el enunciado de **qué se puede afirmar
> con los datos que hay, y qué no**. Toda cifra viene de
> [[ANALISIS_BASE_2026-08-06]], que es reproducible con `analizar_runs.py --todo`.

---

## 1. La pregunta, bien formulada

La pregunta con la que arrancó el proyecto era **«¿podemos revivir el
caquetío?»**, y la respuesta honesta es **no**. Revivir una lengua exige lo que
el caquetío no tiene: hablantes, o un corpus lo bastante grande para deducir su
gramática. Hay 226 palabras atestiguadas y ni una sola oración documentada.

Pero esa formulación esconde una pregunta que **sí** es contestable, y es la que
el experimento estuvo haciendo sin decirlo:

> **¿Se puede producir un corpus de uso —cientos de miles de formas en
> contexto— a partir de un léxico atestiguado y una morfología reconstruida, de
> modo que la estructura que emerja sea consecuencia de las restricciones
> impuestas y no del relleno del modelo?**

Esa pregunta tiene tres virtudes: es empírica, admite un control, y su respuesta
negativa es tan informativa como la positiva.

**Lo que el experimento es, entonces:** no una resurrección, sino un
**generador de hipótesis estructurales bajo restricción declarada**. El
resultado no es «así hablaban los caquetíos». El resultado es «bajo estas
restricciones explícitas, estas estructuras se estabilizan y estas no» — con
las restricciones auditables una por una.

---

## 2. Lo que la fase 1 sí contestó

Cuatro respuestas. **Dos son sobre el fenómeno y dos sobre el instrumento**, y
las del instrumento son las que más valen, porque son las que nadie iba a mirar.

### 2.1 ¿El mecanismo de contagio hace algo? — Sí

Contraste pareado día a día entre el brazo normal y el de ablación (60 turnos
cada uno):

| Lectura | Δ | p | d de Cohen | Días que gana el normal |
|---|---|---|---|---|
| acumulada | +0.0214 | 3.5e-05 | 0.89 | 26/30 |
| ventana | +0.0290 | 3.1e-04 | 0.75 | 22/30 |
| **emergente** | **+0.0752** | **7.7e-11** | **1.81** | **29/30** |

El brazo normal converge más en las tres lecturas, y la diferencia **crece en la
lectura más exigente**. Sistemático, no un empate con medias distintas.

> ⚠️ **Con n = 1 run por brazo esto es señal, no prueba.** Los 30 días
> comparten agentes, semilla y trayectoria: son pseudo-réplicas. Los p-valores
> contestan «¿difieren estas dos series?», no «¿difieren estas dos
> condiciones?».

### 2.2 ¿La convergencia se acumula? — **No**

Este es el hallazgo negativo, y es el más interesante de los cuatro.

En las tres lecturas la brecha entre brazos es **plana o levemente
decreciente**. El mecanismo produce un desplazamiento **inmediato y sostenido**,
no un efecto acumulativo.

Si la hipótesis de trabajo era *«la koiné se va formando»*, el dato dice otra
cosa: *«el contagio fija una diferencia desde el principio y la mantiene»*. Es
un resultado más modesto y más preciso, y **cambia qué habría que medir en la
fase 2**: no la pendiente, sino el punto de fijación y qué lo mueve.

### 2.3 El instrumento medía en parte a sus autores

**La longitud del `system_prompt` de un agente predice negativamente su score**
(r = −0.481, p = 0.0046; Spearman −0.480, n = 33).

Manaure —el diao, el centro narrativo, el prompt más largo con 834 caracteres—
tiene **el peor score de todo el elenco**. Y el aparente efecto de género (las
agentes femeninas puntúan más alto, p = 0.010) es, casi con seguridad, el mismo
confusor: los prompts masculinos promedian 365 caracteres frente a 289 porque
los protagonistas son hombres.

> **Consecuencia dura:** toda lectura del tipo «el agente X lideró la
> convergencia» puede ser «al agente X le escribimos más texto». No es una ley
> sociolingüística: es una propiedad de cómo escribimos el elenco.

### 2.4 La métrica principal no distinguía nada

`pct_caquetio` tiene el **91% de las respuestas en 1.0** (σ = 0.028 y 0.013 en
los dos brazos). Está saturada por diseño: si el objetivo era que el caquetío
dominara, se cumplió con tanta holgura que ya no queda margen para medir mejora
([#69](https://github.com/miguelgilurbina/curiana-radio/issues/69)).

Y la mitad del corpus estaba mal guardada: **27.641 de 54.936 usos (50,3%)** sin
lengua, y el **100%** de ellos eran formas morfológicamente complejas — justo
las que prueban que los agentes manejan la morfología. Arreglado y rellenado.

---

## 3. Lo que la fase 1 **no** puede afirmar

Aquí es donde hay que ser más estricto que un revisor hostil, porque estas
objeciones se las va a hacer cualquiera y es mejor tenerlas escritas primero.

### 3.1 🔴 La amenaza principal: los agentes ya saben hablar

Los agentes son modelos de lenguaje que **ya conocen el español** y **ya
conocen patrones arahuacos generales** (wayunaiki, lokono y taíno están en sus
datos de entrenamiento; el propio lexicón del proyecto es 769 formas de
wayunaiki y 198 de lokono).

Cuando un agente produce una forma bien construida, **no sabemos por cuál de
dos caminos llegó**:

| Camino | Qué probaría |
|---|---|
| La morfología caquetía atestiguada lo restringió | el experimento funciona |
| El modelo rellenó con lo que sabe de lenguas parecidas | el experimento se mide a sí mismo |

**La ablación no distingue estos dos caminos.** Controla la afirmación sobre
*convergencia* —apaga las inyecciones y compara—, pero ambos brazos usan el
mismo modelo con el mismo conocimiento previo. Es un control del **mecanismo
social**, no del **origen de las formas**.

Esta es, hoy, la amenaza a la validez más seria del proyecto, y la fase 1 no la
resolvió.

### 3.2 Las otras cuatro

1. **n = 1 por brazo.** Ya dicho: pseudo-réplica.
2. **30 días simulados** prueban un mecanismo, no un fenómeno histórico. Una
   koineización real ocurre en generaciones.
3. **Ningún run es plenamente citable.** Hasta [[DINAMICA_DE_RUNS]] no se
   registraba contra qué base corrió cada run; para analizar los seis primeros
   hubo que reconstruirla de git. `huella_de_base.py` cierra esto **a partir de
   ahora**, no hacia atrás.
4. **El curador de citas premia lo breve sin comprobar que sea lengua.** El
   momento de mayor impacto de toda la base es «**Ríe.**» — una acotación
   escénica en español, impacto 9.8.

---

## 4. Qué convierte esto en una fase 2

El instinto correcto es el que ya está sobre la mesa: **quitarle a los agentes
la oportunidad de creer que entienden la lengua.**

Si el problema es que el modelo puede rellenar con arahuaco genérico, la salida
no es pedirle que no lo haga —no es verificable— sino **cerrarle la puerta por
construcción**:

| Restricción | Qué prueba si aun así producen |
|---|---|
| Fonotáctica declarada: solo secuencias atestiguadas | que la forma nueva es compatible con el caquetío, no con «una lengua indígena» |
| Morfología cerrada: solo los afijos del inventario | que la productividad es del sistema, no del modelo |
| Léxico cerrado con hueco explícito | que el agente **acuña** en vez de importar |
| Sin glosa castellana en el prompt del turno | que la forma se usa, no se traduce |

**El diseño clave**: si se cierra el inventario y aun así los agentes producen
formas nuevas bien formadas *y las estabilizan entre ellos*, eso sí es un
resultado. Y si no las producen, también — significa que lo que veíamos era
relleno, y saberlo vale la fase entera.

La segunda pieza es la **morfología productiva como métrica**, ahora medible por
primera vez: hasta el arreglo del `source_language`, las 18.752 formas con
sufijo de aspecto se guardaban sin lengua. «¿Usan más morfología con el tiempo?»
rinde mucho más que «¿hablan caquetío?», a la que todos contestan que sí al 99%.

---

## 5. El error del que se saca provecho

Conviene decirlo sin adornos: **la fase 1 corrió el experimento antes de tener
el instrumento calibrado.** 23 runs y 54.936 usos de palabra produjeron sobre
todo hallazgos sobre la métrica, el confusor y el guardado — no sobre la lengua.

Eso no es un fracaso, es el orden en que suelen ocurrir las cosas cuando por fin
miras los datos en serio. Pero deja una regla para la fase 2:

> **Correr más runs no es lo siguiente. Lo siguiente es que un run sea
> legible.** Mientras la métrica esté saturada y la longitud del prompt sin
> controlar, más runs producen más datos que no se pueden interpretar.

---

## Enlaces

[[ANALISIS_BASE_2026-08-06]] · [[DINAMICA_DE_RUNS]] · [[DISENO_KOINE]] · [[01_que_probaron_los_seis_runs]] · [[LINEA_DE_TIEMPO]] · [[esfera-de-interaccion]] · [[mapa-motor]]
