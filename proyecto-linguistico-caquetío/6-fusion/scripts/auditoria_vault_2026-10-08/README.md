# Medidores de la auditoría del vault (2026-10-08)

Los scripts crudos con los que se midió `1-plan/REORGANIZACION_VAULT_2026-10-08.md`.
Sólo leen el vault; escriben un JSON donde se les diga. Uso:

```
python -I medir_vault.py <ruta-del-vault> <salida.json>   # inventario, frontmatter, grafo como lo ve Obsidian
python -I analizar.py <salida.json>                          # las tablas del diagnóstico
python -I simular_objetivo.py <salida.json>                  # la arquitectura objetivo sobre el grafo medido
python -I dependencias.py <ruta-del-vault>                   # qué scripts y páginas web leen rutas fijas del vault
```

El medidor pulido que propone la auditoría (`medir_grafo_vault.py`, que avisa y no falla) llega con el PR 1 de la reorganización.
