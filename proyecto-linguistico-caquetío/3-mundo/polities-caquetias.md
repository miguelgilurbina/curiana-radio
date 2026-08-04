---
tipo: nota
pregunta: "¿Cuántos caquetíos había, y cuál de ellos simulamos?"
motor: curiana_sim/curiana_polities.py
polities: 4
polity_simulada: costera
fuentes: [oliver-1989-cap3, jahn-1927, antczak-2017-cariban, oviedo-y-banos]
medido: 2026-08-04
---

# Las polities caquetías — y cuál es la nuestra

> "To say that the Caquetío are a Theocratic Chiefdom […] explains absolutely
> nothing, and **blurs the differences that make a difference**."
> — Oliver 1989, cap. 3, p. 278

## La respuesta en una frase

Los caquetíos **hablaban una lengua y no tenían una sola sociedad**: había al
menos cuatro formaciones políticas distintas, y la simulación modela **una**, la
costera — cosa que hasta ahora no estaba dicha en ninguna parte.

## Por qué esta nota existe

El proyecto trataba "caquetío" como una cultura homogénea. Oliver dedica su
capítulo 3 a demostrar que no lo era, y enumera **seis ejes** en los que las
formaciones difieren: patrón de asentamiento, densidad de población,
estratificación social, autoridad y liderazgo, presión tierra/población y
actitud ante la guerra. Rechaza el "Cacicazgo Teocrático" de Steward y Faron
justo por aplanar esas diferencias.

[[jahn-1927]] (pp. 200-202), siguiendo el trabajo de archivo inédito de
[[arcaya-1920]], da el mapa completo del pueblo caquetío **desde una base
documental independiente** — y los bloques salen los mismos. Dos fuentes que no
se copiaron entre sí describen la misma geografía.

## Las cuatro

| Polity | Territorio | Autoridad | Lo que la distingue |
|---|---|---|---|
| **costera** ◄ *la nuestra* | Falcón llano, Paraguaná, el Golfete, y de ahí a Aruba, Bonaire y Curazao | Un **diao paramount que es además gran chamán** | Poder secular y sagrado **fundidos en una persona** |
| **barquisimeto** | Valle del Turbio y sabanas de Lara | **Jefe de Paz + Jefe de Guerra**, sin paramount | 23 aldeas fortificadas de ~4.000; el **boratio vive apartado** |
| **yaracuy** | El valle que ellos llamaban **Vararida** | **Confederación elástica** de 2-4 aldeas | Se unen solo si los atacan con fuerza |
| **llanos** | Cojedes, Portuguesa, Apure, hasta Casanare | Militar y secular juntos, pero **poco centralizado** | Único con **esclavitud documentada** (solo bajo Cojedes) |

El detalle, con cita por rasgo y por época, está en el módulo:

```bash
python curiana_sim/curiana_polities.py --contrastar costera barquisimeto
```

## Lo que el modelo destapó

### 🟢 Shaboro y Manaure: el canon estaba bien (y la primera lectura, mal)

La primera versión de esta nota afirmaba que Shaboro era un personaje importado
de Barquisimeto, porque el elenco tiene `casa_cacique` y `choza_piache` en
personas distintas y Oliver describe el poder costero como fundido en el diao.
**Esa inferencia era incorrecta**, y la corrigió minar [[arcaya-1920]] un rato
después.

Lo que Oliver dice que distingue a la costa **no es que no haya boratios**, sino
que allí **el jefe es además gran chamán**, cosa que el jefe de paz de
Barquisimeto no es. Y las dos cosas conviven: Arcaya cita a Oviedo y Valdés
(t. II p. 298) diciendo que **"en cada pueblo principal hay un boratio"**.

El canon del proyecto ya lo tenía bien, y con precisión: Manaure es *"Señor de
la Curiana y piache a la vez: gobierna el cuerpo y el cielo de su pueblo"*, *"el
jefe teocrático: gobernante Y piache en uno"*. Es exactamente el modelo costero.
Que además exista Shaboro como boratio especialista es **lo que la fuente
describe**, no una desviación.

`coherencia_del_canon()` se corrigió en consecuencia: ahora comprueba si el
cacique lleva atributos chamánicos, que es el rasgo diagnóstico, en vez de si
los oficios están repartidos entre personas distintas. Con el canon actual, no
salta.

> La lección que queda: **el eje que separa dos polities no siempre es el que
> parece.** "Hay un piache aparte" no distingue nada; "el jefe también profetiza"
> sí. Distinguir mal es el mismo error de aplanamiento que Oliver denuncia, solo
> que en la otra dirección.

### 🟢 El corpus, en cambio, está limpio

Se auditaron los 161 hechos buscando rasgos importados de otra polity sin
marcar. **Siete** mencionan otra formación, y los siete lo hacen bien:

- `parentesco-037` es ejemplar — dice explícitamente que la paramountcy de
  Manaure **no** cubría a todo el mundo caquetío, y cita Barquisimeto y Yaracuy
  como prueba de que existía otra estructura.
- `creencia-015b` trata el Yaracuy como toponimia, no importa rasgos.
- `creencia-004` (la formación del piache por ayuno prolongado) **sí marca** su
  origen: "Nueva Segovia / Barquisimeto". Y ahora tiene además respaldo costero
  independiente: el boratio de Oviedo y Valdés también manda **ayunar** —a toda
  la casa, con solo `cazá` una vez al día— durante la cura.

Conclusión honesta del barrido: **no hay mezcla de polities sin marcar, ni en el
corpus ni en el canon del motor.** El único hallazgo real fue de higiene (el
campo `etnia`), y la primera sospecha sobre Shaboro no resistió el contraste con
la fuente.

## Qué falta

1. **Yaracuy y Llanos están a medio documentar** (6/8 y 5/8 ejes). Los huecos se
   dejan visibles a propósito; rellenarlos por simetría sería el error que
   Oliver denuncia.
2. **`prompt_polity()` no se inyecta todavía** en el orquestador. Hoy no haría
   nada: los 60 agentes son de la misma polity. Existe para cuando no lo sean.
3. **Dar vida a una segunda polity** es la puerta grande: un contacto con
   Barquisimeto o Yaracuy pondría en escena dos sociedades que hablan la misma
   lengua y organizan el poder al revés. Para la tesis de koiné del proyecto es
   un escenario mejor que el contacto con otra etnia, porque aísla la variable:
   **misma lengua, distinta sociedad**.
4. `etnia` y `polity` son ejes ortogonales y conviene que no se confundan — ver
   la nota de higiene del campo `etnia` en el propio módulo.

## Enlaces

[[oliver-1989-cap3]] · [[jahn-1927]] · [[antczak-2017-cariban]] · [[oviedo-y-banos]] · [[arcaya-1920]] · [[mapa-geografia-politica]] · [[05_geografia_politica_y_sucesion]] · [[mapa-motor]]
