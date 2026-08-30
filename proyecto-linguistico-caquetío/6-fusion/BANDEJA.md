---
tipo: bandeja
generado_por: curiana_sim/generar_bandeja.py
editar_a_mano: no
---

# Bandeja de fusión — lo que espera para entrar al canon

> ⚠️ **Archivo generado. No se edita a mano.** El TABLERO mide el canon;
> esto mide la cola. Cada propuesta cita su obra (regla 8) y espera
> fusión humana (regla 5). Regenerar:
> ```
> python curiana_sim/generar_bandeja.py
> ```

<!--GENERADO--> Generado el **2026-08-30**.

**1512 ítems propuestos** en 18 propuestas, más **3 issue(s)/comentario(s) redactados sin publicar**.

## Propuestas de datos (`6-fusion/*.yaml`)

| Archivo | Obra | Ítems | Aviso |
|---|---|---|---|
| `antolinez_1946_capo_y_ortografia.yaml` | antolinez-1946-hacia-el-indio | 3 |  |
| `colores_caquetios.yaml` | ? | 4 |  |
| `etnias_en_contacto.yaml` | ? | 3 |  |
| `frase_saludo_mitare.yaml` | ? | 2 |  |
| `lengua_toponimia_quibacoa.yaml` | ? | 3 |  |
| `nodos_oliver_apendice_e.yaml` | oliver-1989-cap4 | 134 |  |
| `petroglifos_y_manaure.yaml` | moron-2012-petroglifos | 4 |  |
| `polities_no_costeras_federmann.yaml` | ? | 16 |  |
| `tabla15_c14_oliver.yaml` | oliver-1989-cap4 | 23 |  |
| `tabla_a8_jirajarano.yaml` | oliver-1989-apendice-a | 33 |  |
| `tabla_a9_oliver.yaml` | oliver-1989-cap2 | 49 |  |
| `toponimia_coro_espina.yaml` | gonzalez-batista-nombre-de-coro | 5 |  |
| `toponimos_esteves_indice.yaml` | esteves-1989 | 182 |  |

## Propuestas léxicas (`curiana_sim/lexicon_*.py` — indexadas en su sitio)

Se quedan en `curiana_sim/` porque **el tooling las importa** (medido
2026-08-15; la línea del CLAUDE.md que decía que no se importaban era
falsa y se corrigió). Entradas contadas por patrón de dict.

| Módulo | Obra | Entradas | Quién lo importa |
|---|---|---|---|
| `lexicon_alvarado.py` | alvarado-1921 | 217 | lo importan generar_tablero y auditar_82 |
| `lexicon_gatschet.py` | gatschet-1885 | 88 | lo importan generar_tablero y auditar_82 |
| `lexicon_van_buurt.py` | van-buurt-2014 | 231 | lo importan generar_tablero y auditar_82 |
| `lexicon_toponimos.py` | varias (F11) | 74 | lo importa migrar_toponimos |
| `lexicon_candidatos.py` | aisladas 2026-06-28 | 441 | lo importa generar_tablero |

## Redactado y sin publicar (`6-fusion/issues-pendientes/`)

El classifier de la sesión no puede publicar issues; se publican a mano
con `gh issue create --body-file` / `gh issue comment --body-file`.

| Archivo | Qué es |
|---|---|
| `issue-esquema-lecturas-toponimos.md` | El registro de topónimos necesita una tercera voz: la de la tradición |
| `issue-pdfs-fuentes-aporte.md` | Servir los PDF del vault desde `/kaketiana/fuentes`, tras un aporte voluntario |
| `issue-repertorio-vs-filiacion.md` | El lexicón responde "¿de qué lengua es esta palabra?" y lo usamos como si respondiera "¿la |

---

*Al fusionar una propuesta: mover el dato a su esfera con
`procedencia.obra`, borrar o vaciar el archivo de la bandeja, y
regenerar esto y el TABLERO.*
