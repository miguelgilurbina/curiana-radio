---
tipo: nota
pregunta: "¿Se puede cerrar la forma de la palabra para que el modelo no rellene?"
medido: 2026-08-09
herramienta: curiana_sim/curiana_fonotactica.py
base: las 234 formas caquetío-atestiguado del lexicón
---

# La fonotáctica — un resultado negativo, y por qué vale

> **La respuesta corta:** no. Cerrar la fonotáctica **no** impide que el modelo
> rellene con arahuaco genérico, porque el arahuaco genérico ya satisface la
> fonotáctica caquetía. Lo que sí hace es detectar castellano.

---

## 1. Lo que se quería y lo que salió

[[HALLAZGOS_FASE_1]] §3.1 nombró la amenaza principal de la fase 1: los agentes
son modelos que ya saben español y ya conocen patrones arahuacos, así que
cuando producen una forma bien construida no sabemos si los restringió el
caquetío o los rellenó su conocimiento previo.

La idea era **cerrarles la puerta por construcción**: derivar un filtro de forma
solo del caquetío atestiguado y rechazar lo que no lo cumpla.

Se construyó el filtro y se midió qué deja pasar de cada fuente:

| Fuente | Pasa | |
|---|---|---|
| caquetío atestiguado (control) | 100.0 % | ██████████████████████████████ |
| caquetío reconstruido | 98.5 % | █████████████████████████████ |
| taíno | 94.4 % | ████████████████████████████ |
| **wayunaiki** | **86.3 %** | █████████████████████████ |
| lokono | 79.8 % | ███████████████████████ |
| **castellano** (control externo) | **44.7 %** | █████████████ |

> **Bloquea el 55 % del castellano y solo el 14 % del wayunaiki.**

El wayunaiki es la fuente de contaminación que preocupaba —769 de las 1413
entradas del lexicón, y una lengua viva bien representada en los datos de
entrenamiento del modelo— y el filtro apenas lo toca.

**La razón es estructural, no un fallo de implementación**: caquetío y
wayunaiki son las dos abrumadoramente CV (86.8 % y 81.4 % de formas
estrictamente CV) y, tras normalizar la ortografía, sus inventarios difieren en
dos letras. No hay nada que discriminar.

## 2. Qué sí sirve, entonces

**El filtro se queda, con su función rebajada y dicha**: es un detector de
castellano. El castellano ES una vía de contaminación real —los agentes piensan
en castellano— y detectarlo cuesta nada.

**El control de validez de la fase 2 tiene que ser otro.** Las dos vías que
quedan, y ambas son más prometedoras que ésta:

| Vía | Por qué puede funcionar |
|---|---|
| **Morfología cerrada** | el inventario de afijos caquetíos es específico (`-ka`/`-ni`/`-da`, `ta-`/`pi-`/`nü-`, los seis de `REGLAS_ZAVALA`). El wayunaiki NO comparte ese paradigma, así que aquí sí hay contraste |
| **Léxico cerrado con hueco declarado** | si falta la palabra, el agente tiene que **acuñar** en vez de importar. Es la prueba directa de productividad |

## 3. 🔴 Dos problemas del dato que salieron al medir

### 3.1 La ortografía estaba midiendo al transcriptor

En la primera pasada, sin normalizar, el inventario "atestiguado" tenía **29
letras** —incluidas `c`, `q`, `z`, `f`, `v`, `á`, `é`, `í`— y el del wayunaiki
21, ninguna de ésas. Las iniciales más frecuentes eran `c:48, q:11` en el
atestiguado y `k:11` en el reconstruido.

Eso no es fonología: **el caquetío atestiguado está transcrito en ortografía
castellana colonial y el reconstruido en ortografía lingüística moderna.** Sin
normalizar, lo que se mide es quién escribió, no qué lengua es.

`fonemizar()` lo normaliza con diez reglas, cada una con su porqué en el código.

### 3.2 El conjunto atestiguado tiene residuo castellano

Al inspeccionar qué formas aportan los clusters raros al inventario:

| Forma | Glosa | Problema |
|---|---|---|
| `caquetillo` | 'árbol, madera de construcción' | **diminutivo castellano `-illo`** |
| `casquito` | 'agrio, fermentado' | **diminutivo castellano `-ito`** |
| `bagre` | 'pez' | palabra castellana |
| `barbasco` | 'hierba de borrachera' | palabra castellana |
| `despopo` | 'fuerza' | prefijo `des-` castellano |

Cada una mete su cluster (`ll`, `sk`, `gr`, `sp`) en el inventario
"atestiguado" y **hace el filtro más permisivo**. Es residuo que se hereda: una
palabra con morfología castellana no puede ser caquetío atestiguado.

## 4. 🔴 D5 no es cosmética: decide si el filtro discrimina

El hallazgo con más consecuencias de toda la medición.

`gua`/`güe` en transcripción colonial puede valer **/gwa/** o simplemente
**/wa/**. `guaitiao` es el taíno *waitiao*, donde `<gu>` es claramente /w/. Y de
las 50 formas atestiguadas con `<g>`, la mayoría son `gua-`/`güe-`.

Aplicando la regla `<gu>` → /w/ y volviendo a medir:

| | sin la regla | con la regla |
|---|---|---|
| wayunaiki pasa | 86.3 % | **65.4 %** |
| castellano pasa | 44.7 % | 44.7 % |
| caquetío reconstruido pasa | 98.5 % | 91.2 % ⚠️ |

**Una sola decisión ortográfica multiplica por 2,5 el poder discriminante del
filtro contra el wayunaiki.** Eso convierte
[D5 (#36)](https://github.com/miguelgilurbina/curiana-radio/issues/36) —hoy
catalogada como política ortográfica c/k y bloqueante del gate— en una decisión
con consecuencias directas sobre el experimento.

> ⚠️ Y con un aviso: la regla también hace caer el caquetío **reconstruido** de
> 98.5 % a 91.2 %, porque al convertir `gü` en `w` desaparece la `ü` del
> inventario atestiguado y las formas reconstruidas que la llevan empiezan a
> fallar. No es gratis.

**Deliberadamente no se aplica por defecto.** Activarla sería decidir D5 por la
puerta de atrás. Queda medible con `--gu-es-w`.

## 5. Reproducirlo

```bash
python curiana_sim/curiana_fonotactica.py            # el informe
python curiana_sim/curiana_fonotactica.py --gu-es-w  # con la regla abierta
python curiana_sim/curiana_fonotactica.py --json
```

12 tests en `tests/test_fonotactica.py`. Dos de ellos protegen el **resultado
negativo**: si el wayunaiki empieza a no pasar, no es una mejora automática —
hay que mirar si el filtro se volvió más estricto por buenas razones o si el
lexicón cambió debajo.

## Enlaces

[[HALLAZGOS_FASE_1]] · [[morfologia]] · [[lexicon]] · [[metodo-comparativo]] · [[mapa-lengua]] · [[esfera-de-interaccion]]
