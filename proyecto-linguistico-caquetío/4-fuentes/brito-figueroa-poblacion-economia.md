---
tipo: fuente
obra: "Población y economía en el pasado indígena venezolano"
autor: "Brito Figueroa, Federico"
anio: 1962
genero: historiografia
publicacion: "Caracas, [Ediciones Historia], 1962. 48 pp., con mapa; 22 cm; bibliografía pp. 47-48 (catálogo BNV, koha.bnv.gob.ve, biblionumber 677)"
paginas: "— (leída por Miguel en Scribd)"
capa_texto: no
estado_minado: no-disponible  # 2026-09-22: sin texto en el repo ni copia de acceso legítimo; lo minado es lo que Miguel leyó en Scribd el 2026-08-25
cobertura: "sólo los pasajes que Miguel leyó el 2026-08-25 (6-fusion/polities_no_costeras_federmann.yaml): Barquisimeto, Yaracuy, llanos, Caracas. Nada de la costa de Coro. La pregunta de la demografía de Coro se contestó con otras fuentes (6-fusion/coro_colonial_castellanos_brito_gonzalez_2026-09-22.yaml §escala_del_mundo)"
minado: 2026-09-22
prioridad: alta
tareas: [F12]
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-22
aliases: ["Brito Figueroa", "Población y economía en el pasado indígena venezolano"]
---

# Brito Figueroa — *Población y economía en el pasado indígena venezolano*

## Qué es, y por qué importa el matiz

Es la obra que Miguel estuvo leyendo el **2026-08-25** en Scribd, y de la que
salió todo el lote de `6-fusion/polities_no_costeras_federmann.yaml`.

**No es una crónica: es historiografía del s. XX** que cita crónicas. La cadena
real de cada dato es:

```
crónica del s. XVI  →  Brito Figueroa  →  este repo
```

Por eso ninguna de las citas recogidas puede entrar al canon como
`atestiguado` sin ir al original. Lo que sí da, y es muchísimo, es el **mapa de
qué documento dice qué y en qué página** — es un aparato de notas excelente.

## 🎯 Lo que rindió: siete fuentes localizadas por sus notas

Todas estas notas de obra nacieron de su aparato crítico:

| Fuente | La referencia que dio |
|---|---|
| [[perez-de-tolosa-1546]] | *en Oviedo y Baños, **Doc., pp. 255-256*** |
| [[ballesteros-1550]] | el pasaje del `buco`, verificado luego en [[arcaya-1920]] p. 170 |
| [[federmann-1916]] | ed. 1916; pp. 62-63, 85, 90, 109-110 |
| [[nueva-segovia-1579]] | *Bol. del Centro Histórico Larense, Nº 11, año 1942* |
| [[rivero-1883]] | p. 21 — el continuo dialectal achagua |
| [[gumilla-1791]] | I, p. 127 |
| [[steward-1949]] | *Handbook of South American Indians*, Vol. V, pp. 665-668 |

Más otras que aún no tienen nota: **López de Velasco 1894** (p. 159),
**Lope de las Varillas 1569** (en Oviedo y Baños, Doc. pp. 303-320),
**Carvajal 1892** (p. 197), **Castellanos** (*Elegías*, p. 185, vía Arcaya).

## ⚠️ Sesgo declarado: maximalismo demográfico

Brito Figueroa **discute a [[steward-1949]] por bajo**: dice que sus propias
premisas "pueden conducir a cómputos superiores a 500.000 habitantes". Esa
inclinación a la cifra alta es una posición historiográfica conocida del autor,
y se ve en el mismo pasaje que la enuncia.

No invalida nada — pero al leerlo hay que separar **la cita documental** (que es
lo valioso, y verificable) de **su lectura demográfica** (que es interpretación
de escuela). El proyecto se queda con lo primero.

## 🔴 Aviso de polity, que atraviesa toda la obra

El libro cubre **toda Venezuela**. Casi nada de lo recogido es de la polity
costera del Golfete: hay Barquisimeto, Yaracuy, El Tocuyo, los llanos, los valles
centrales de lengua Caraca, cumanagotos, guayqueríes, achaguas. Por eso el lote
entero vive en `6-fusion/` con el campo `polity` declarado en cada hecho, y no en
`3-mundo/corpus/`.

Ver [[polities-caquetias]] y la regla 4 del CLAUDE.md.

## Pendiente

- ~~Editorial y edición~~: **[Ediciones Historia], Caracas, 1962; 48 pp. con
  mapa** (catálogo de la Biblioteca Nacional de Venezuela, consultado el
  2026-09-22; el sello va entre corchetes: lo pone el catalogador).
- Decidir si se archiva copia — toca la decisión **D8**
  ([#37](https://github.com/miguelgilurbina/curiana-radio/issues/37): si el repo
  archiva copias de fuentes externas).

## Bitácora 2026-09-22 — tercera campaña de minería (parcela M7)

**Qué se preguntó**: la demografía de la región de Coro en el XVI (gente,
pueblos, encomiendas de caquetíos, saca de esclavos a las islas) y la
economía indígena (sal, pesca, trueque), para la escala del mundo simulado.

**No se pudo preguntar a la obra.** No hay texto en el repo; no está en
archive.org (búsqueda por autor: tres ítems, ninguno éste) ni en HEVILA; el
autor murió en 2000 y la obra tiene derechos; la copia de Scribd no es
acceso abierto legítimo. **Dato nuevo del catálogo**: 48 páginas para toda
Venezuela, y la BNV la clasifica en «Región Nororiental»: es improbable que
traiga la demografía de Coro con detalle. Su valor sigue siendo el aparato de
notas.

**La pregunta se contestó con lo que sí hay** (Castellanos, González Batista
2002 y Ballesteros ya en el corpus), con `epoca` y qué se puede proyectar al
XV: `6-fusion/coro_colonial_castellanos_brito_gonzalez_2026-09-22.yaml`
§escala_del_mundo.

**Deuda**: si Miguel quiere el libro, la BNV tiene cinco ejemplares.

Índice: [[INDICE_FUENTES]]
