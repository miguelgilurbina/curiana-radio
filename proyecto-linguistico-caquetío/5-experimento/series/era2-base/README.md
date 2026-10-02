---
tipo: guion-de-serie
serie: era2-base
corrida: 2026-09-27 → 2026-09-29
---

# La serie `era2-base`: cómo se corrió

Los dos guiones con que se corrió la serie, rescatados el 2026-10-01 de la
carpeta de logs (que vive fuera del repo). Están tal cual corrieron: las rutas
son las de la máquina de Miguel.

- `correr_cadena.sh <escena|control> <desde> <hasta>`: un brazo, día a día, con
  la semilla 100 + día y `--continuar` desde el día 2. Se detiene al primer
  error **o si el árbol de git está sucio**, porque la huella sellaría
  `motor_sucio`. Ojo: `git status --porcelain` también cuenta los archivos sin
  trackear, así que una carpeta nueva en la raíz para la cadena (pasó con un
  `design_handoff_*`).
- `correr_serie.sh`: el brazo con escena del día 2 al 30, guarda su estado
  aparte y corre el control del 1 al 30.

El protocolo, los resultados y lo que pasó al correrla están en
[[BITACORA_RUNS]] (sección de la serie `era2-base`). El análisis está en
`5-experimento/analisis/era2_base_*`. Lo que no viaja en git:

- los logs por día, en `C:/Users/migue/curiana_runs_log/era2-base/`;
- el estado final de cada brazo (`curiana_*.json`), en
  `C:/Users/migue/curiana_estado_backup/era2-base-{escena,control}/`. De ahí lee
  `export_serie_seed.py --estado-escena/--estado-control` la competencia.

El motor es el del tag `base-era2-1`. Para repetirla, se corre desde un
checkout de ese tag, para que `motor_commit` sea el mismo.
