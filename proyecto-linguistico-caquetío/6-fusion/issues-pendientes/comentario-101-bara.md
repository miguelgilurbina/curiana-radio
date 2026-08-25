## Zavala también dice 'árbol' — y es el #29 de su glosario

Este issue registraba que el lexicón dice `bara` = 'río' mientras Esteves y
van Buurt dicen 'árbol'. Falta el tercero, y es el que más pesa: **Zavala Reyes
2015 dice 'árbol' también.**

```
29. Bara     (E): Palo, árbol.
30. Barabara (A): Árbol de madera dura y pesada. Olivo.
```

### El estado actual del lexicón es insostenible

| entrada | capa | glosa | procedencia |
|---|---|---|---|
| `bara` | `caquetío-reconstruido` | **río, corriente fluvial** | "núcleo fundacional, forma justificada por cognado en proto-arawakan/topónimo" |
| `barabara` | `caquetío-atestiguado` | **árbol de madera dura y pesada. Olivo** | Zavala Reyes 2015 #30 (A) |

O sea: ya tenemos como **atestiguada** la forma reduplicada glosada 'árbol', y
mantenemos la base como **reconstruida** glosada 'río'. Las dos no pueden ser
correctas a la vez, y la que tiene fuente es la de 'árbol'.

Marcador: son **tres fuentes independientes** ('árbol') contra **una
reconstrucción por cognado** ('río').

### 🔴 El problema de higiene detrás

`4-fuentes/zavala-reyes-2015.md` declara `estado_minado: completo`. La entrada
#29 del glosario nunca llegó al lexicón. "Completo" está sobredicho, y esto abre
la pregunta de cuántas entradas más del glosario no se levantaron: el TABLERO
mide 223 entradas del lexicón que citan a Zavala, sobre un glosario de ~290.

### Propuesta

1. `bara` pasa a `caquetío-atestiguado` = 'palo, árbol', citando Zavala #29 +
   Esteves + van Buurt.
2. La lectura 'río' se conserva como lectura descartada (D7), con su cognado
   proto-arawakan, para que no se pierda el razonamiento.
3. Auditar el glosario completo de Zavala contra el lexicón — entrada por
   entrada— y medir cuántas faltan. Es barato: la obra está en el repo con capa
   de texto.

---
*Verificado contra `fuentes_caquetios/Palabras Vivas de una Lengua Muerta.pdf`
(`pdftotext -enc UTF-8 -layout`).*
