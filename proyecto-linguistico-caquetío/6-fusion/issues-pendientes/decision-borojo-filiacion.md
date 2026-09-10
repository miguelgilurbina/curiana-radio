## Borojó: Esteves dice que es **chibcha** y que es un **árbol frutal**

Salió el 2026-09-10, arreglando un bug del extractor de glosas de la Parte II
de Esteves. La entrada verbatim:

> «BOROJÓ. […] (**Borojó es chibcha: un árbol frutal**)»

Y esto choca de frente con el lexicón, que tiene:

```python
"borojo": {"sig": "salina, lago salado de Coro", "cat": "sust",
           "fuente": "caquetío-atestiguado",
           "notas": "Zavala Reyes 2015, glosario #44 (AM):
                     «Salina de Coro, comercio de la sal»"}
```

No coinciden **ni en la lengua ni en el referente**.

### Por qué importa más de lo que parece

Casi todas las mineras **añaden** al lexicón. Esta puede **quitar**: si Esteves
acierta, `borojo` no es voz caquetía y sale de la capa `caquetío-atestiguado`.
Sería la primera baja por filiación desde que la capa existe.

Y no es una entrada cualquiera. `borojo` sostiene el **comercio de la sal**,
que es uno de los hechos económicos que el corpus da por buenos, y Borojó es
además municipio, río y el nombre de la desembocadura donde está Punta Capana.

### Lo que hay a cada lado

| | Zavala #44 (AM = Angulo Molina) | Esteves 1989, Parte II |
|---|---|---|
| lengua | caquetío (implícito: el glosario es de caquetío) | **chibcha**, declarado |
| referente | salina, lago salado, comercio de la sal | **árbol frutal** |
| independencia | no cita a Esteves | no cita a Angulo Molina |

Las dos son de primera mano y ninguna transmite a la otra: es un **conflicto
real**, no un artefacto de cadena.

### La lectura que las salvaría — y por qué no la propongo

Se podría decir que el árbol da nombre al sitio y que el sitio es donde está la
salina. Encaja, y es exactamente el patrón que esta campaña ha medido una y
otra vez en Falcón (Adaro < `dara` el alcaraván, Buchuaco < `buche` el cardo,
Cayude < el guanábano silvestre). Pero:

1. Es **conjetura mía**, no dato de ninguna de las dos fuentes.
2. **No salva la filiación**: aunque el árbol nombre el sitio, si el nombre del
   árbol es chibcha, la voz sigue sin ser caquetía.

Los chibchas no son vecinos disparatados: Jahn los sitúa al oeste, y Aroa lleva
una glosa chibchense circulando por la divulgación. Pero eso es contexto, no
prueba.

### Lo que hace falta antes de decidir

- 🔴 **Verificar la entrada en la IMAGEN.** Esta glosa se perdía justamente
  porque el OCR maltrata esa página: se comió el paréntesis de cierre. Antes de
  mover nada del lexicón hay que ver el original.
- Mirar si Esteves razona la atribución chibcha en algún otro sitio, o si la
  suelta sin argumento (que es como la suelta aquí).
- Buscar el árbol: si existe un frutal llamado borojó en la zona, la glosa se
  sostiene sola. ⚠️ Ojo con el falso amigo: el *borojó* del Chocó
  (*Alibertia patinoi*) es colombiano y de selva húmeda — nada que ver con
  Falcón, y confundirlos sería el error de siempre.

### Qué decide Miguel

1. **Esperar** a la verificación en imagen antes de tocar nada (mi recomendación).
2. **Degradar ya** `borojo` a `caquetío-hipotético` por la regla 2 —en duda,
   degradar— y resolver después.
3. **Dejarla como está** y anotar el conflicto en `notas`, que es lo que el
   protocolo hace por defecto cuando una fuente contradice al lexicón.

Registro completo en `6-fusion/esteves_parte2_falcon.yaml`,
sección `glosas_recuperadas_2026_09_10`.
