# ¿Puede un pueblo inventar una raíz nueva? — lo conservador YA está aplicado

**Para que Miguel decida.** El arreglo de la raíz de ninguna parte está escrito,
medido y aplicado, con su corte declarado en el punto 11 del «Cambio de
instrumento» de `BITACORA_RUNS.md`. Lo que queda abierto es **una consecuencia
de diseño** que el arreglo toma por defecto y que no es obvia. Mientras no se
decida, rige lo conservador: **la raíz inventada queda fuera**.

---

## 1. Qué se arregló, en una línea

`curiana_lexicon._familia_de_token()` decía «caquetío» de cualquier raíz que no
encontrara en el lexicón. Eso es correcto para `kasi-nii-bana` —raíz
atestiguada + dos afijos declarados— y es un agujero para `lumina-bana-iro`, del
latín *lumina*, que en el brazo de control de la serie C fue la segunda forma
más fuerte de la disputa de las cuentas y cuya hermana `lumina-bana-uco`
**fijó** el cometa en el diccionario koiné. Uno de los agentes lo escribió él
mismo en la glosa:

> `lumina`: cosa-que-brilla **(del español, pero transformada en caquetío)** +
> `bana`: del lugar alto + `uco`: lo que fluye/viaja

Desde el corte, una forma cuya **raíz** no esté en ninguna tabla del lexicón
—`VOCABULARIO_BASE`, `FUERA_DEL_HABLA`, `_RAICES_VERB`— no se registra, no
compite, no cuenta como forma emergente y no se guarda como «caquetío».

## 2. La pregunta

**¿Un pueblo no puede inventar una raíz nueva?**

Porque eso es lo que la regla dice hoy, y dicho así suena mal: las lenguas
inventan raíces. Lo que la regla acierta es el caso que la destapó —una raíz
LATINA entrando vestida de caquetío— y lo que arrastra de paso es el caso
legítimo: un agente que acuña `duma` 'tierra-seca' de la nada.

**El coste está medido, no estimado.** De las acuñaciones distintas de cada
cadena de la serie C:

| cadena | acuñaciones | con raíz de ninguna parte | de ellas, adoptadas |
|---|---|---|---|
| con escena (`f2741e89`→`fcdfa07a`→`0313d830`) | 53 | 9 (17,0 %) | 1 |
| control (`0345840d`→`45618069`→`e98227eb`) | 32 | 11 (34,4 %) | 5 |
| serie C limpia (la cadena anterior) | 52 | 6 (11,5 %) | 1 |
| toda la base | 644 | 131 (20,3 %) | — |

O sea: entre el 11 % y el 34 % de lo que un agente propone como palabra nueva
lleva una raíz que no sale del lexicón, y uno de cada cinco en toda la base. No
es un caso raro.

**Y hay un subcaso que duele más que el general**: la casi-raíz. `pütshi-bana`
se rechaza porque la clave del lexicón es `pütchi`, no `pütshi` — el agente
escribió mal una raíz que sí conoce. La regla de hoy no perdona un carácter.

## 3. Las tres opciones

**A — Lo que está aplicado (conservador).** La raíz tiene que estar en el
lexicón. Simple, medible, y deja fuera tanto `lumina` como `duma`.

**B — La glosa avala la raíz.** Se admite una raíz inventada **si el agente la
declara en su glosa `[forma: componentes = significado]` y los componentes que
nombra son conocidos**. Es la regla que el propio prompt ya enseña: quien acuña
tiene que decir de qué está hecha su palabra. Contra: en el caso `lumina` el
agente TAMBIÉN declaró su glosa, y declaró que era del español — habría que
exigir que **todos** los componentes nombrados sean claves del lexicón, y
entonces `lumina + bana + uco` cae igual (`lumina` no lo es), que es el
resultado que queremos. A favor: una acuñación como `duma` (sin componentes
conocidos, glosa `duma = duma → tierra-seca`) seguiría cayendo, así que B es
**casi** A. Lo que B añade de verdad es poco.

**C — La casi-raíz se perdona.** Se admite la raíz que difiera en un carácter
de una clave del lexicón (`_difieren_en_un_caracter` ya existe en el módulo,
para otra cosa). Recupera `pütshi-bana` y no recupera `lumina`. Es
independiente de A/B y se puede tomar sola. Contra: una lengua reconstruida con
disciplina ortográfica no debería normalizar en silencio; habría que decidir si
la forma se guarda como la escribió el agente o como la clave.

## 4. Lo que el escriba recomienda, y por qué no lo decide

**A + C**: la regla de pertenencia para la raíz, y el perdón de un carácter
para la casi-raíz. B no añade casi nada sobre A porque los casos que B
admitiría son los que ya admite A (componentes conocidos = raíz conocida).

No lo decide porque **C mueve el score**: perdonar `pütshi-bana` la devuelve al
habla y a `palabras_caquetias`. Si se toma, hay que medirlo y declararlo, igual
que se declaró el corte del punto 11.

## 5. Lo que ya está hecho y no espera a nadie

- `curiana_lexicon.es_raiz_de_ninguna_parte()` / `nucleo_de_token()` — la regla.
- `_familia_de_token()` devuelve `"desconocida"`; `save_agent_response` guarda
  `"acuñada"` para lo que la respuesta declaró.
- `LexicoComunitario.registrar_neologismo()` y `CompetenciaLexica.proponer()`
  rechazan, y el rechazo se cuenta aparte (`rechazos_de_raiz`) y se dice al
  cerrar el run.
- `PUERTA_DEL_RECUENTO` — la misma puerta para el motor y para `analizar_nodos`.
- `analizar_runs.py --raices` y `analizar_nodos.py` leen los runs viejos con el
  dato, sin reescribir la base.
- Medición: `6-fusion/medicion_raices_de_ninguna_parte_2026-09-20.yaml`
  (`6-fusion/scripts/medir_raices_de_ninguna_parte.py`).
- Tests: `curiana_sim/tests/test_raiz_de_ninguna_parte.py`.
