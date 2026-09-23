# La arqueología de las islas y de Falcón: sitios, fauna, movimiento y mar (M8)

**Labels propuestos:** `decision`, `mundo`, `fuentes`
**Propuesta de datos:** `6-fusion/arqueologia_insular_falcon_2026-09-22.yaml`
**Cifras del lado del repo:** `python 6-fusion/scripts/medir_arqueologia_insular_falcon.py`

## Qué se hizo

Tercera campaña de minería, parcela M8. Cuatro obras: Urbina Jiménez 2007 y
2011 (Falcón), Casale et al. 2024 (petrografía de Aruba), Knaf et al. 2021
(jade) y Moreno-Mayar et al. 2018 (genética). Casale y Knaf estaban
«pendientes» porque el editor devolvía 403: las dos tienen copia legal CC-BY
en repositorios universitarios (Lirias, ETH) y se bajaron al repo.

## Lo que resultó falso al medirlo

- **Knaf 2021 no es movilidad humana por isótopos.** Es la procedencia
  geoquímica del JADE (rocas de Guatemala, Cuba y la R. Dominicana; 19 hachas
  de Playa Grande, 3 guatemaltecas). Cero Venezuela y cero ABC, con control.
- **La ficha de Urbina decía «una datación de dabajuroide en 1650».** No
  existe: 1650 es el tope del rango relativo de Oliver para Los Médanos B, y
  Los Médanos no está en El Carrizal. Corregida.
- **T8 cita `urbina-jimenez-2011`**, clave que no existe en la bibliografía
  (es `urbina-jimenez-2007-2011`).

## Lo que dio

1. **Sitios.** Aruba: Tanki Flip (más de 100 personas, trece casas,
   empalizada, enterramientos entre urnas), Ser'i Noka (dos casas, entierros
   en fosa y en urna), Savaneta (muchas urnas y entierros colectivos, hasta Los
   Médanos B). Falcón: tres sitios de El Carrizal sin fecha absoluta; los
   concheros con enterramientos de Falco 286 son de cerámica ANTERIOR a la
   caquetía.
2. **Fauna — casi nada, y eso es el dato.** Ninguna de las cuatro obras trae
   zooarqueología. Una especie nombrada (*Strombus gigas*, El Carrizal, sin
   fecha ni recuento por especie), hueso animal sin identificar, conchas y
   coral sin especie, y la concha como desgrasante de la loza. Va en `fauna:`
   con `epoca: indeterminada` donde el contexto no está fechado. La lista del
   Pleistoceno de Muaco va aparte, para que nadie la proyecte al s. XV.
3. **Movimiento, contra T8.** Casale confirma que Aruba mira a la costa de
   enfrente: su fig. 1 une cada isla con la costa y ninguna isla con otra ni
   con las Antillas; el grupo cerámico decorado no se puede adscribir (la
   receta de la pasta lo impide) y en el cuerpo del artículo no hay ni una
   mención antillana. Knaf cierra la deuda del jade como negativo. Y un dato
   colonial: en 1723 El Carrizal se repobló con caquetíos venidos de Aruba.
4. **Mar.** En la vida sí: comida, loza decorada hecha con arcilla marina y
   concha, concheros, el estrecho de 30 km. En la creencia: **cero medido** en
   las cinco obras. No refuta la tesis de Miguel: estas obras no hablan de
   cosmovisión.

## Para decidir

**D1 — ¿Qué cronología del dabajuroide usa el motor?** Las fuentes no
coinciden y no se promedian.
- **A.** Oliver 1989: Urumaco 1100/1200-1400/1450, Los Médanos desde 1350.
- **B.** Casale 2024, Tabla 1: Urumaco Tardío 1350-1500, Los Médanos A
  1400-1450, B 1450-1515.
- **C.** No fijar ninguna y darle a la ventana las dos lozas (Urumaco Tardío y
  Los Médanos A) como coexistentes.
- *Recomendación: C* — las dos tablas coinciden en que hacia 1400-1450 conviven.

**D2 — ¿Entran las aldeas de Aruba a `asentamientos.yaml`?** (prop-02)
- **A.** Sí, las tres grandes, con lo que da Casale y las discrepancias
  declaradas.
- **B.** Todavía no: esperar a leer Dijkhoff 1997 y Versteeg y Rostain 1997,
  que son la fuente primaria.
- *Recomendación: B* — Casale las resume; la atestación de primera mano está
  a un paso.

**D3 — ¿Se corrige el YAML de T8?** (prop-01: clave de Urbina, subir `cer-02`
a atestiguado, cerrar la deuda de `pie-01`).
- **A.** Sí, en el mismo PR de fusión.
- **B.** No: se deja T8 como está y esta propuesta lo sustituye.
- *Recomendación: A.*

**D4 — ¿Quién busca la fauna de verdad?** Las fuentes están localizadas y no
son de esta parcela: Zavala Reyes 2018, Tabla II (malacofauna caquetía de los
ss. XIV-XVIII, ya en el repo y sin pasar al esquema `fauna:`); Dijkhoff 1997
y Versteeg y Rostain 1997 (Tanki Flip); Antczak 1998 (tesis UCL, abierta,
economía no cerámica de las islas).
- **A.** Un agente de fauna, ahora, con Zavala 2018 primero.
- **B.** Una parcela nueva de zooarqueología en la próxima campaña.
- *Recomendación: A* — Zavala ya está en el repo y es de la ventana.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
