# La semilla del DÍA mueve rasgos de la PERSONA

> Hallado el 2026-09-21, al perseguir un aviso falso de la serie C repetida.
> **No está arreglado**: el arreglo cambia lo que el agente lee, así que es corte
> de serie y va con la próxima tanda, medido. Aquí queda para que no se pierda.

## Qué pasa

Una cadena `--continuar` corre cada día con su semilla — la serie C usa 21, 22 y
23. `curiana_koine.fijar_semilla(semilla)` fija con ella el dado de lo que se
**deriva de la ficha** de cada agente (blake2b sobre semilla + nombre): sus
formas-semilla de idiolecto y el aspecto de respaldo de su emocionar. Pero eso
no es del día: es de la persona. Y al cambiar la semilla, cambia.

Medido con `6-fusion/scripts/medir_semilla_del_dia.py` sobre el elenco de la era 2:

| rasgo | semilla 21 → 22 | semilla 21 → 23 |
|---|---|---|
| bloque `[Tu emocionar]`, lo que el agente LEE | cambia en **7 de 63** | cambia en **7 de 63** |
| formas-semilla del idiolecto | cambia en 52 de 63 | cambia en 52 de 63 |

Entre los tres días son **diez** los agentes a los que el prompt les dice otra
cosa de sí mismos: Naure, Uria, Wache, Katiata, Jakura, Buriche, Tabri, Tijua,
Karama y Tauta. Uria lee «Tu aspecto natural es `-ni`» el día 1 y «es `-ka`» los
días 2 y 3.

## Dos efectos, de distinto peso

1. **Conducta (el que importa).** A uno de cada seis agentes el bloque de
   disposición le cambia de un día a otro dentro de la misma cadena. Es ruido en
   la continuidad del idiolecto, que es justo lo que la koiné mide.
2. **Diagnóstico (el que lo destapó).** `agentes_sin_precarga()` deriva las
   formas-semilla con la semilla DE HOY y las busca en un idiolecto sembrado con
   la DEL DÍA 1, así que avisa en falso: «cadena sin pre-carga de idiolectos: 2
   de 63…» el día 2 y «3 de 63» el día 3, en los DOS brazos. Comprobado sobre el
   estado guardado del brazo con escena: con la semilla 21 → **0** agentes sin
   pre-carga; con 22 → 2; con 23 → 2. La cadena está bien sembrada; el aviso
   miente — y dice «hay que re-correr la cadena desde el día 1», que cuesta una
   hora de API si alguien le hace caso.

Las formas-semilla que cambian (52 de 63) **no** llegan al habla en una cadena:
`cargar_koine` reconstruye con `peso_semilla=0` y sólo se re-siembra a un agente
nuevo. Lo que sí llega es el bloque del emocionar, que se monta en cada
`call_agent`.

## Qué NO invalida

**La comparación entre brazos se sostiene**: los dos corren con las mismas
semillas, así que a los mismos diez agentes les cambia lo mismo el mismo día.
Lo que se resiente es la lectura de la continuidad de esos diez dentro de una
cadena, en cualquier brazo.

## Opciones

- **A — la semilla de la persona es la de la CADENA.** `guardar_koine` escribe
  con qué semilla se sembró (`semilla_de_precarga`), `cargar_koine` la recupera,
  y en `--continuar` el dado de la ficha se fija con ésa mientras
  `random.seed()` sigue con la del día. Un JSON viejo sin la llave cae en lo de
  hoy, con el aviso suavizado. Arregla los dos efectos con un cambio. **Es corte
  de serie** (cambia el prompt de esos agentes en los días 2+): se mide antes,
  va con la tanda, y la serie se repite una vez. *Recomendada.*
- **B — sólo el diagnóstico.** Se corrige el aviso y el emocionar se deja como
  está. No es corte, pero deja el ruido dentro.
- **C — la semilla de la persona no depende de ningún run.** Blake2b sólo sobre
  el nombre: dos cadenas con semillas distintas tendrían el mismo elenco. Más
  limpio conceptualmente; cambia TODAS las cadenas, también el día 1.

## Ligado a

`5-experimento/BITACORA_RUNS.md`, «La serie C repetida con la tanda del 21
dentro», punto 1 de «Dos cosas del instrumento»; la fila «La pre-carga de
idiolectos va indexada por los nombres de la ERA 1» de `CLAUDE.md`, que es de
donde sale el dado.
