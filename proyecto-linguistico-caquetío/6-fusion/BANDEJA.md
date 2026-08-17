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

<!--GENERADO--> Generado el **2026-08-17**.

**1206 ítems propuestos** en 7 propuestas, más **5 issue(s)/comentario(s) redactados sin publicar**.

## Propuestas de datos (`6-fusion/*.yaml`)

| Archivo | Obra | Ítems | Aviso |
|---|---|---|---|
| `nodos_oliver_apendice_e.yaml` | oliver-1989-cap4 | 134 |  |
| `tabla_a9_oliver.yaml` | oliver-1989-cap2 | 21 |  |

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
| `comentario-51-kadushi.md` | `kadushi`: testimonio regional de Miguel, y la salida por especies |
| `comentario-52-mene.md` | `mene`: la evidencia de Oliver, la decisión, y una aclaración de género |
| `comentario-d9-issue38.md` | Medición del barrido completo — **no aplicar todavía** |
| `issue-caraota.md` | `caraota`: el corpus atribuye la palabra al caquetío, y Oliver marca su étimo como foráneo |
| `issue-hayo.md` | `hayo` = 'coca' está como `caquetío-atestiguado`, y Oliver lo marca como préstamo de Santa |

---

*Al fusionar una propuesta: mover el dato a su esfera con
`procedencia.obra`, borrar o vaciar el archivo de la bandeja, y
regenerar esto y el TABLERO.*
