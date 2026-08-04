---
tipo: moc
pregunta: "¿Cómo es el caquetío?"
ambito: lexicón, morfología, toponimia, método comparativo
lexicon_activo: 1413
familia_caquetia: 304
medido: 2026-08-04
---

# Mapa — La lengua

> Mapa de contenido de **la pieza central del proyecto**: el caquetío mismo.
> Hasta el 2026-08-04 esta carpeta no existía: la lengua solo se podía leer
> como 45 archivos `.py`. Estas notas no sustituyen al código —el código sigue
> siendo la fuente de verdad— sino que **lo hacen legible**.

## La respuesta en una frase

Hay **1413 palabras** en el lexicón activo, de las cuales **304 son de familia
caquetía** (226 atestiguadas, 68 reconstruidas); las otras 1109 son lenguas
hermanas o de contacto que sirven de comparanda, **no de habla**. De las 226
atestiguadas, **215 citan a una sola obra** ([[zavala-reyes-2015]]). Ese es a la
vez el logro y la fragilidad de la base documental.

## Las notas de esta carpeta

| Nota | Qué responde |
|---|---|
| [[lexicon]] | ¿Qué palabras hay, de dónde salieron, y quién las sostiene? |
| [[morfologia]] | ¿Cómo se construyen palabras nuevas, y con qué evidencia? |
| [[toponimia]] | ¿Cómo se despejan morfemas de los nombres de lugar? |
| [[metodo-comparativo]] | ¿Cómo se reconstruye cuando no hay dato caquetío? |

## Las tres capas de la lengua

1. **Lo atestiguado** — palabra documentada en una fuente citable. 226 entradas.
   Es lo único que no se discute. → [[lexicon]], [[INDICE_FUENTES]]
2. **Lo reconstruido** — derivado por método comparativo desde una hermana con
   correspondencia fonológica declarada, o despejado de una ecuación toponímica.
   68 entradas del núcleo fundacional. → [[metodo-comparativo]], [[toponimia]]
3. **Lo hipotético** — transducción sin cognación verificada. **441 formas,
   aisladas fuera del habla** desde 2026-06-28 con ~80 % de fallo medido.
   → [[lexicon]] §candidatas

> La regla es la misma que la del corpus cultural: **en duda se degrada a la
> etiqueta más débil**, nunca al revés. Ver [[INDICE]] §etiquetas epistémicas.

## Las tres tensiones abiertas

Cada una tiene issue y argumento en [[DECISIONES_ABIERTAS]].

| Tensión | Dónde se explica | Decisión |
|---|---|---|
| `-bana` 'orilla' sin cita vs. `-ana` 'lugar de' atestiguado | [[morfologia]] §-bana vs -ana | D9 · issue [#38](https://github.com/miguelgilurbina/curiana-radio/issues/38) |
| El lexicón es 3,4:1 wayunaiki sobre lokono; Oliver dice que el caquetío desciende del **lokono** | [[metodo-comparativo]] §el desbalance | D11 · issue [#39](https://github.com/miguelgilurbina/curiana-radio/issues/39) |
| Tres glosas que la fuente contradice (`tara`, `saruro`, `corie`) | [[lexicon]] §conflictos | issues [#45](https://github.com/miguelgilurbina/curiana-radio/issues/45) · [#47](https://github.com/miguelgilurbina/curiana-radio/issues/47) · [#46](https://github.com/miguelgilurbina/curiana-radio/issues/46) |

## Hacia dónde salen estas notas

**A las fuentes** — quién sostiene qué:
[[INDICE_FUENTES]] · [[zavala-reyes-2015]] · [[alvarado-1921]] ·
[[van-buurt-2014]] · [[gatschet-1885]] · [[oliver-1989-cap2]] ·
[[brinton-1871]] · [[perea-alonso-1942]]

**Al experimento** — cómo la lengua se pone a hablar:
[[mapa-motor]] (el código, los tests, el scoring) ·
[[DISENO_KOINE]] (la convergencia entre idiolectos) ·
[[03_descomposicion_toponimica]] (el diseño de F11) ·
[[02_protocolo_habla_paraguanera]] (el protocolo de sustrato regional)

**Al mundo** — qué nombra la lengua:
[[mapa-ecologia]] §huecos léxicos · [[mapa-creencia]] (*boratio*, *díao*) ·
[[mapa-familia]] (vocabulario de parentesco) · [[corpus/README|el corpus cultural]]

## Cómo se miden estos números

Ninguna cifra de esta carpeta se copia de la documentación anterior. Se miden
así, desde `curiana_sim/`:

```bash
python -c "import curiana_lexicon as L; print(len(L.VOCABULARIO_BASE))"
python auditar_82.py --resumen        # entradas de familia caquetía sin cita
python -m pytest tests/ -q            # 45 tests, el guardián del motor
python check_vault_links.py --strict  # (desde la raíz) el guardián del vault
```

Toda cifra lleva su fecha de medición en el frontmatter. Si el código cambió y
la nota no, **la nota está mal** — no el código.
