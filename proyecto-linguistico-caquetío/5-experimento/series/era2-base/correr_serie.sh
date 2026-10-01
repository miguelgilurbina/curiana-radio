#!/usr/bin/env bash
# La serie era2-base entera, después del día 1 del brazo con escena (dd680e49,
# revisado a mano el 2026-09-28): escena días 2-30, se guarda su estado aparte
# (no se borra) y control días 1-30. Mismas semillas (100 + día).
set -u
L="/c/Users/migue/curiana_runs_log/era2-base"
SIM="/c/Users/migue/OneDrive/Documents/Desarrollo/Curiana Radio/proyecto-linguistico-caquetío/curiana_sim"
bash "$L/correr_cadena.sh" escena 2 30 || exit $?
B="/c/Users/migue/curiana_estado_backup/era2-base-escena"
mkdir -p "$B"
mv "$SIM"/curiana_director.json "$SIM"/curiana_koine.json "$SIM"/curiana_lexico.json \
   "$SIM"/curiana_memory.json "$SIM"/curiana_observer.json "$SIM"/curiana_state.json "$B"/ || exit 4
echo "$(date '+%F %T') estado del brazo con escena guardado en $B" | tee -a "$L/cadena.log"
bash "$L/correr_cadena.sh" control 1 30 || exit $?
echo "$(date '+%F %T') SERIE era2-base COMPLETA" | tee -a "$L/cadena.log"
