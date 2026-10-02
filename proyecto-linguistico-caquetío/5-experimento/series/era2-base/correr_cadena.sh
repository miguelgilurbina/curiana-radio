#!/usr/bin/env bash
# La serie era2-base: 30 días × 2 brazos, mismas semillas (100 + día).
# Ok de Miguel: 2026-09-27 («Mi ok para correr la sim»). Motor: tag base-era2-1.
# Uso: correr_cadena.sh <brazo: escena|control> <día_desde> <día_hasta>
# Se detiene al primer error, o si el árbol de git está sucio (la huella
# sellaría motor_sucio). El estado de cada brazo queda en disco entre días
# (--continuar); al cambiar de brazo se guarda aparte, no se borra.
set -u
BRAZO="$1"; DESDE="$2"; HASTA="$3"
L="/c/Users/migue/curiana_runs_log/era2-base"
SIM="/c/Users/migue/OneDrive/Documents/Desarrollo/Curiana Radio/proyecto-linguistico-caquetío/curiana_sim"
export PYTHONIOENCODING=utf-8
cd "$SIM" || exit 2
BASE=(--elenco era2 --auto 6 --turnos-por-dia 6 --agentes-por-turno 12 --roster todos
      --perfil era2 --reflexion --serie era2-base)
if [ "$BRAZO" = "escena" ]; then EXTRA=(--escena --capubana-cada 3); else EXTRA=(); fi
for d in $(seq "$DESDE" "$HASTA"); do
  if [ -n "$(git status --porcelain)" ]; then
    echo "$(date '+%F %T') ARBOL SUCIO antes del día $d: me detengo" | tee -a "$L/cadena.log"; exit 3
  fi
  S=$((100 + d)); DD=$(printf '%02d' "$d")
  if [ "$d" -eq 1 ]; then CONT=(); else CONT=(--continuar); fi
  echo "$(date '+%F %T') $BRAZO día $d semilla $S — empieza" | tee -a "$L/cadena.log"
  python curiana_orchestrator_v2.py "${BASE[@]}" "${EXTRA[@]}" "${CONT[@]}" --semilla "$S" > "$L/${BRAZO}_d${DD}.log" 2>&1
  RC=$?
  echo "$(date '+%F %T') $BRAZO día $d — exit $RC" | tee -a "$L/cadena.log"
  if [ "$RC" -ne 0 ]; then echo "fallo en $BRAZO día $d: me detengo" | tee -a "$L/cadena.log"; exit "$RC"; fi
done
echo "$(date '+%F %T') $BRAZO días $DESDE-$HASTA: HECHO" | tee -a "$L/cadena.log"
