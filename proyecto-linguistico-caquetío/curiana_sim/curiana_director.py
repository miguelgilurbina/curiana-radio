"""
CURIANA — El Director con mundo: su voz por era y su reflexión al cerrar el día.

Hasta el 2026-09-16 el Director era «de la Curiana» aunque el elenco fuera el
de Paraguaná, y sólo veía el estado y las intervenciones del turno: en el
segundo día de la era 2 (run 89fc1744) inventó «la sombra del ceibo», que el
cardonal no tiene (ecologia-032). Aquí:

  - director_system(mundo): el sistema del Director, «de la Curiana» o «de
    Paraguaná». El texto de la era 1 es el de siempre, byte a byte.
  - reflexion_del_dia(): UNA llamada al cerrar cada día (--reflexion, apagado
    por defecto: cuesta API). El Director, con el mundo (curiana_mundo.
    resumen_del_mundo), lee los cierres del día y el reporte medido del
    observer y escribe 4-6 oraciones: qué cambió hoy, qué palabra nueva
    prendió, qué queda abierto para mañana. Miguel, 2026-09-16: «qué piensa el
    Director del día».
  - guardar_reflexion()/cargar_reflexiones(): el archivo local
    curiana_director.json, junto a los otros curiana_*.json. La config del run
    en la base es inmutable, así que la reflexión no va ahí; el estado guarda
    la última en notas_orquestador para que el día siguiente (--continuar) la
    vea.

El modelo se pasa desde el orquestador (MODEL); el valor por defecto de aquí
es el mismo para que el módulo se pueda probar solo.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from curiana_mundo import resumen_del_mundo
from curiana_state import ESTACION_DE_DIA

MODELO_POR_DEFECTO = "claude-haiku-4-5-20251001"
MAX_TOKENS_REFLEXION = 700
RUTA_DIRECTOR = "curiana_director.json"      # relativo al cwd, como curiana_state.json

_NOMBRE_DEL_MUNDO = {"CURIANA": "la Curiana", "PARAGUANÁ": "Paraguaná"}


def nombre_del_mundo(mundo: Optional[str]) -> str:
    m = (mundo or "CURIANA").upper()
    return _NOMBRE_DEL_MUNDO.get(m, m.title())


def director_system(mundo: Optional[str]) -> str:
    """El sistema del Director para `mundo`. La era 1 conserva su texto; la
    era 2 lo ata al bloque [El mundo] que director_narrate() le pasa."""
    base = (
        f"Eres el Director de la simulación comunitaria de {nombre_del_mundo(mundo)}.\n"
        "Estilo: conciso, sensorial, presente. Crónica oral caquetía.\n"
        "No uses lenguaje romántico ni exótico. Describe lo que un habitante vería y sentiría."
    )
    if (mundo or "").upper() == "PARAGUANÁ":
        base += (
            "\nCuenta sólo con lo que el mundo tiene: el bloque [El mundo] manda sobre lo "
            "que sepas de otras tierras. No inventes árboles, ríos ni gente que no estén ahí."
        )
    return base


def reflexion_del_dia(client, state, observer_reporte: str, cierres_del_dia: list,
                      *, dia: Optional[int] = None, model: str = MODELO_POR_DEFECTO,
                      max_tokens: int = MAX_TOKENS_REFLEXION) -> str:
    """La reflexión del Director sobre el día que acaba de cerrarse: una llamada.

    Se llama al cierre del día, cuando el estado ya apunta al amanecer
    siguiente: el día reflexionado es state.dia - 1 salvo que se pase `dia`.
    `cierres_del_dia` son los cierres narrativos de cada turno (los deja
    director_narrate en state.cierres_del_dia); `observer_reporte`, el
    reporte medido de observer.reporte_dia(). En Paraguaná lleva el mundo del
    día cerrado (su período, de noche)."""
    dia = state.dia - 1 if dia is None else dia
    partes = [f"Se cierra el día {dia}. Estado al cerrar: {state.to_context_string()}"]
    if getattr(state, "mundo", "") == "PARAGUANÁ":
        mundo = resumen_del_mundo(state, estacion=ESTACION_DE_DIA(dia, state.mundo), momento="noche")
        if mundo:
            partes.append(mundo)
    cierres = [c.strip() for c in (cierres_del_dia or []) if c and c.strip()]
    partes.append("[Los cierres del día, turno a turno]:\n"
                  + ("\n".join(f"- {c}" for c in cierres) if cierres
                     else "- (hoy no hubo cierres narrativos)"))
    if observer_reporte and observer_reporte.strip():
        partes.append("[Lo medido por el observador]:\n" + observer_reporte.strip())
    if getattr(state, "notas_orquestador", ""):
        partes.append("[Lo que dejaste anotado al cerrar el día anterior]: "
                      + state.notas_orquestador.strip())
    partes.append(
        "Escribe la reflexión del Director sobre el día en 4-6 oraciones: qué cambió hoy, "
        "qué palabra nueva prendió (cuál y en boca de quién, si alguna; si ninguna, dilo) y "
        "qué queda abierto para mañana. En primera persona, como Director; sin lenguaje "
        "romántico ni exótico, y sin nombrar nada que el mundo no tenga."
    )
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=director_system(getattr(state, "mundo", None)),
        messages=[{"role": "user", "content": "\n\n".join(partes)}],
    )
    return resp.content[0].text.strip()


def cargar_reflexiones(path: str = RUTA_DIRECTOR) -> list[dict]:
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except FileNotFoundError:
        return []
    return list(d.get("reflexiones") or [])


def guardar_reflexion(dia: int, texto: str, run_id: Optional[str] = None,
                      path: str = RUTA_DIRECTOR, *, nuevo: bool = False) -> list[dict]:
    """Añade la reflexión del día al archivo (o lo empieza si `nuevo`: un run
    que no continúa a otro no hereda reflexiones ajenas). Devuelve la lista."""
    reflexiones = [] if nuevo else cargar_reflexiones(path)
    reflexiones.append({
        "dia": dia,
        "run_id": run_id,
        "texto": texto,
        "guardada": datetime.now().isoformat(timespec="seconds"),
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"reflexiones": reflexiones}, f, ensure_ascii=False, indent=2)
    return reflexiones
