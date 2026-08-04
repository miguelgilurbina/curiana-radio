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

### 🔴 Shaboro es de Barquisimeto

`coherencia_del_canon()` lo detecta solo, leyendo `curiana_agents.py`:

- La polity **costera** funde poder sagrado y secular: el diao *es* el gran
  chamán (Oliver p. 279; y [[oviedo-y-banos]] describe a Manaure llevado en
  hamaca **a hombros de caciques**, con la etiqueta de un señor sagrado).
- El elenco actual tiene `casa_cacique` (Manaure, Nubiri-sha) y `choza_piache`
  (Shaboro, Buio-sha, Sha) **sin solaparse**: poder político y poder sagrado en
  personas y lugares distintos.
- Eso —incluido el detalle de que el boratio vive en su propia choza fuera de la
  aldea— es literalmente el patrón que Oliver describe para **Barquisimeto**.

No es un error que haya que corregir a la fuerza: es una **decisión de canon**
que nunca se tomó explícitamente, y ahora está a la vista. Las salidas son tres,
y son de Miguel:

1. **Aceptarlo y marcarlo**: la Curiana es costera salvo en esto, por razones
   narrativas (un piache-personaje da mucho más juego que un cacique que también
   profetiza). Basta con decirlo.
2. **Corregir el canon**: Manaure absorbe la función chamánica y Shaboro pasa a
   ser su aprendiz/ejecutor, no un poder paralelo.
3. **Convertirlo en trama**: que la separación sea *reciente* y disputada dentro
   de la ficción — la costa fundía los dos poderes y en Todariquiba se están
   separando. Es la opción que más rendimiento narrativo tiene y la que menos
   contradice la fuente.

### 🟢 El corpus, en cambio, está limpio

Se auditaron los 161 hechos buscando rasgos importados de otra polity sin
marcar. **Siete** mencionan otra formación, y los siete lo hacen bien:

- `parentesco-037` es ejemplar — dice explícitamente que la paramountcy de
  Manaure **no** cubría a todo el mundo caquetío, y cita Barquisimeto y Yaracuy
  como prueba de que existía otra estructura.
- `creencia-015b` trata el Yaracuy como toponimia, no importa rasgos.
- `creencia-004` (la formación del piache por ayuno prolongado) **sí marca** su
  origen —"Nueva Segovia / Barquisimeto"—, pero es el mismo asunto de Shaboro
  visto desde el corpus: es dato de Barquisimeto sosteniendo a un personaje
  costero. Va con la decisión de arriba.

Conclusión honesta del barrido: **la mezcla de polities no está en el corpus,
está en el canon del motor.**

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
