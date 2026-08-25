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

<!--GENERADO--> Generado el **2026-08-24**.

**1267 ítems propuestos** en 9 propuestas, más **1 issue(s)/comentario(s) redactados sin publicar**.

## Propuestas de datos (`6-fusion/*.yaml`)

| Archivo | Obra | Ítems | Aviso |
|---|---|---|---|
| `nodos_oliver_apendice_e.yaml` | oliver-1989-cap4 | 134 |  |
| `tabla15_c14_oliver.yaml` | ? | 0 | ⚠️ no parsea: mapping values are not allowed here
  in "<unicode string>", line 27, column 26:
      - lab: ISGS-1173, sitio: "Túcua",              bp: "110 ... 
                             ^ |
| `tabla_a8_jirajarano.yaml` | oliver-1989-apendice-a | 33 |  |
| `tabla_a9_oliver.yaml` | oliver-1989-cap2 | 49 |  |

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
| `issue-pdfs-fuentes-aporte.md` | Servir los PDF del vault desde `/simulador/fuentes`, tras un aporte voluntario |

---

*Al fusionar una propuesta: mover el dato a su esfera con
`procedencia.obra`, borrar o vaciar el archivo de la bandeja, y
regenerar esto y el TABLERO.*
