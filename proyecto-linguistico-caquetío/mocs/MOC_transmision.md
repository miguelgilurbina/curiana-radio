---
tipo: moc
pregunta: "¿Cómo sabía el caquetío lo que sabía?"
sesion: 4/4 — programa corpus cultural
corpus: [transmision.yaml]
hechos: 34
etiquetas: {atestiguado: 13, reconstruido: 5, canon-simulacion: 14, hipotetico: 2}
medido: 2026-07-29
---

# MOC — Transmisión oral del saber

> Mapa de contenido de la pregunta 4, la que cierra el ciclo: familia es la
> estructura por la que viaja el saber, ecología su contenido, creencia su
> marco — **esta es el mecanismo**. Es también el único dominio del corpus con
> etiqueta `canon-simulacion` (14 de 34): describe el elenco tanto como el mundo.

## La respuesta en una frase

**La fidelidad de un saber no depende de su importancia sino de su forma**: lo
formulaico (canción, genealogía recitada) sobrevive casi literal; lo libre
(consejo, prosa) deriva; y lo que no tiene heredero designado **no se degrada,
desaparece entero**.

## Piezas

| Pieza | Qué es |
|---|---|
| [[04_transmision_saber]] | El ensayo + **anexo de diseño** (del rito a la medición del eco) |
| `curiana_sim/cultura/transmision.yaml` | 34 entradas (13 atestiguado · 5 reconstruido · 14 canon-simulación · 2 hipotético) |
| [[04_transmision]] | Hoja de fuentes |
| [[CANON_TIERRA]] | El documento de diseño que esta sesión enmarca teóricamente, no reemplaza |
| [[PROGRAMA_WAYUU]] | Programa aparte levantado por esta sesión (pregunta Manaure-palabrero) |

## Las cuatro tesis que carga

1. **Currículo por edad sin aula**: 7 tramos, del "imita con un palo" al
   "archivo viviente". Subió de `[hipótesis]` a `[reconstruido]` cuando
   [[amodio-perez-2006]] confirmó etapas *nombradas* (joüuu/tepichi/jintüloa/
   jimaüai) e hitos con edad concreta.
2. **Fidelidad diferencial por forma**: canción > genealogía recitada >
   iniciación > imitación de oficio > consejo libre. La métrica de eco del
   Observer debería ser sensible a `forma_transmision` **desde el principio**.
3. **Puntos únicos de falla**: Bana-mana (71, historia oral, sin heredero) y
   Tari-ko (41, rutas de agua abierta, sin heredero) son **extinción**;
   Pira-sha es **degradación**. Son fenómenos distintos y señales distintas.
4. **El acceso restringido no se guarda por escasez sino por riesgo** — urari
   mal dosificado mata, un diseño mal copiado "borra" un ancestro. Y la
   restricción más severa del corpus no protege una técnica sino **una palabra**
   (el nombre de los muertos).

## Fuentes que la sostienen

| Fuente | Peso | Nota |
|---|---|---|
| [[jahn-1927]] | **pilar** — pp. 205-227 | derecho consuetudinario oral, tabú de nombrar muertos, reclusión femenina |
| [[amodio-perez-2006]] | 6 hechos, leído completo | el currículo por edad con datos validados en talleres wayuu |
| [[angleria-1892]] | 1 hecho, decisivo | vol. 4, p. 236: el areíto como genealogía cantada — comparanda exacta de `ofrenda_ancestros_anochecer` |
| [[guerra-curvelo-palabrero]] | 4 hechos | el pütchipü'üi; abrió [[PROGRAMA_WAYUU]] |
| [[vansina-ong]] | 2 hechos, marco teórico | **ambos de segunda mano** (reseñas, no texto completo) |
| [[las-casas-1875]] | nulo | 613 pp. barridas: apologética de Colón y catequesis, no pedagogía indígena |
| [[gilij-1780-1783]] | cero coincidencias | patrones en español sobre texto italiano **sin capa de texto** |
| [[oviedo-y-valdes-1851]] | no procesable | contiene el dato de la *puna* que Jahn cita; PDF corrupto |

## El experimento que este MOC le pide al motor

**El caso Bana-mana.** Su rol de oficiante en `ofrenda_ancestros_anochecer` ya lo
pone frente a testigos infantiles. La hipótesis medible: *¿algún agente que solo
presenció vuelve a nombrar a esos ancestros en un turno posterior sin que
Bana-mana esté presente?* Si sí, el run **produjo** un heredero en vez de
narrarlo. Si no, queda registrado el turno exacto en que el saber murió.

El ciclo completo (concepto → rito → pulso de exposición → eco medido por rol)
está diseñado en el anexo de [[04_transmision_saber]] sobre maquinaria que **ya
existe**: `DifusionLexica.propagar_uso()` y `IdiolectoAgente` (`curiana_koine.py`).
Falta la tabla de eventos rituales del Observer. → [[MOC_motor]].

## Hilos abiertos

- **Ningún equivalente adulto de Wama-sha**: nadie *canta la historia*, solo
  arrulla niños. Hueco de rol real en el elenco de 60.
- Vansina y Ong de primera mano si el proyecto quiere apoyarse más fuerte en el
  marco de oralidad.
- Brinton 1871 y Perea Alonso 1942 no se releyeron **bajo el lente de
  transmisión** — se minaron solo para léxico.
- [[PROGRAMA_WAYUU]] entero está sin arrancar.
