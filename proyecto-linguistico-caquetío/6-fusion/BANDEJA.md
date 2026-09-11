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

<!--GENERADO--> Generado el **2026-09-11**.

**2133 ítems propuestos** en 47 propuestas, más **6 issue(s)/comentario(s) redactados sin publicar**.

## Propuestas de datos (`6-fusion/*.yaml`)

| Archivo | Obra | Ítems | Aviso |
|---|---|---|---|
| `antolinez_1946_capo_y_ortografia.yaml` | antolinez-1946-hacia-el-indio | 3 |  |
| `auditoria_a2_perea.yaml` | ? | 18 |  |
| `bachaco_y_gu_es_w.yaml` | alvarado-1921 | 0 |  |
| `barrido_toponimos_web_2026-09-10.yaml` | ? | 9 |  |
| `barrido_web_medina_2026-09-09.yaml` | ? | 13 |  |
| `castellanos_1589_toponimos.yaml` | castellanos-elegias | 0 |  |
| `censo_ana_esteves_109.yaml` | esteves-1989 | 13 |  |
| `censo_terminacion_re.yaml` | ? | 3 |  |
| `ceret_on_hipotesis_miguel.yaml` | ? | 3 |  |
| `colores_caquetios.yaml` | ? | 4 |  |
| `comparandas_jahn_1927.yaml` | jahn-1927 | 0 |  |
| `computo_d11_2026-08-31.yaml` | ? | 4 |  |
| `decisiones_colisiones_d5_2026-08-31.yaml` | ? | 3 |  |
| `decisiones_tanda_2026-08-30.yaml` | ? | 0 |  |
| `decisiones_tanda_2026-09-01.yaml` | ? | 0 |  |
| `decisiones_tanda_2026-09-08.yaml` | ? | 0 |  |
| `esteves_parte2_falcon.yaml` | esteves-1989 | 16 |  |
| `frase_saludo_mitare.yaml` | ? | 2 |  |
| `jahn_vocabularios_comparados.yaml` | jahn-1927 | 4 |  |
| `lengua_toponimia_quibacoa.yaml` | ? | 3 |  |
| `lokono_gramatica_perea_1942.yaml` | perea-alonso-1942 | 6 |  |
| `medicion_contaminacion_score_2026-09-09.yaml` | ? | 0 |  |
| `medina_colina_dictado.yaml` | ? | 111 |  |
| `migracion_lemas_fase2.yaml` | ? | 79 |  |
| `nodos_oliver_apendice_e.yaml` | oliver-1989-cap4 | 134 |  |
| `oliver_324_caribes.yaml` | ? | 0 | ⚠️ no parsea: mapping values are not allowed here
  in "<unicode string>", line 83, column 81:
     ... os bubures» (Oviedo y Valdés [6]: 33); «basically the same natio ... 
                                         ^ |
| `paraguana_dos_clanes.yaml` | oliver-1989-cap3 | 5 |  |
| `pendientes_en_alvarado_y_arcaya.yaml` | ? | 0 |  |
| `petroglifos_y_manaure.yaml` | moron-2012-petroglifos | 4 |  |
| `polities_no_costeras_federmann.yaml` | ? | 16 |  |
| `tabla15_c14_oliver.yaml` | oliver-1989-cap4 | 23 |  |
| `tabla_a1_a7_swadesh.yaml` | oliver-1989-apendice-a | 4 |  |
| `tabla_a2_transcripcion.yaml` | oliver-1989-apendice-a | 101 |  |
| `tabla_a8_jirajarano.yaml` | oliver-1989-apendice-a | 33 |  |
| `tabla_a9_oliver.yaml` | oliver-1989-cap2 | 49 |  |
| `toponimia_coro_espina.yaml` | gonzalez-batista-nombre-de-coro | 5 |  |
| `toponimia_paraguana_miguel.yaml` | ? | 5 |  |
| `toponimos_esteves_indice.yaml` | esteves-1989 | 130 |  |
| `tura_la_tesis_de_miguel.yaml` | ? | 0 |  |
| `velasco_primarios_agi.yaml` | velasco-2015-resistencia | 4 |  |
| `voces_de_miguel_2026-09-10.yaml` | ? | 7 |  |

Vistas generadas en `6-fusion/` (no cuentan: juntan lo que ya está arriba):

- `lokono_perea_1942.yaml` — generado por `curiana_sim/minar_perea.py`
- `toponimos_mapa_kaketiana.yaml` — generado por `curiana_sim/barrer_mapa.py`
- `toponimos_por_fuente.yaml` — generado por `curiana_sim/juntar_toponimos.py`

## Propuestas léxicas (`curiana_sim/lexicon_*.py` — indexadas en su sitio)

Se quedan en `curiana_sim/` porque **el tooling las importa** (medido
2026-08-15; la línea del CLAUDE.md que decía que no se importaban era
falsa y se corrigió). Entradas contadas por patrón de dict.

| Módulo | Obra | Entradas | Quién lo importa |
|---|---|---|---|
| `lexicon_alvarado.py` | alvarado-1921 | 217 | lo importan generar_tablero y auditar_82 |
| `lexicon_gatschet.py` | gatschet-1885 | 88 | lo importan generar_tablero y auditar_82 |
| `lexicon_van_buurt.py` | van-buurt-2014 | 231 | lo importan generar_tablero y auditar_82 |
| `lexicon_toponimos.py` | varias (F11) | 169 | lo importa migrar_toponimos |
| `lexicon_candidatos.py` | aisladas 2026-06-28 | 441 | lo importa generar_tablero |
| `lexicon_perea.py` | perea-alonso-1942 | 173 | comparanda lokono; el motor NO lo importa a propósito (ver su cabecera) |

## Redactado y sin publicar (`6-fusion/issues-pendientes/`)

El classifier de la sesión no puede publicar issues; se publican a mano
con `gh issue create --body-file` / `gh issue comment --body-file`.

| Archivo | Qué es |
|---|---|
| `comentario-39-d11-rebalanceo.md` | D11 decidida: se rebalancea hacia el eje lokono-taíno, con achagua más adelante |
| `comentario-45-tara-medina.md` | Segunda fuente, y viva: para un paraguanero del siglo XX, las taras son los saltamontes |
| `decision-borojo-filiacion.md` | Borojó: Esteves dice que es **chibcha** y que es un **árbol frutal** |
| `decision-d11-el-nucleo-reconstruido-del-wayuu.md` | D11 tiene una consecuencia que no se ejecutó: 23 entradas, y los pronombres enteros, se re |
| `decision-era2-retroabstraido.md` | Decisión de modelo para la era 2: el habla que no se puede atestiguar |
| `fallo-miguel-nivel-C-medina.md` | Las 33 voces de nivel C — esperan tu fallo |

---

*Al fusionar una propuesta: mover el dato a su esfera con
`procedencia.obra`, borrar o vaciar el archivo de la bandeja, y
regenerar esto y el TABLERO.*
