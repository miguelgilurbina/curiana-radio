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
  - estado_del_dia_cerrado(): la línea de estado del día que se reflexiona.
    Hasta el día 3 de la era 2 (run 0193873d) se le pasaba
    state.to_context_string(), que al cerrar ya apunta al amanecer siguiente
    («Día 4, Turno 1»), y el modelo lo copiaba a su propia cabecera: la
    reflexión del día 3 se tituló «Cierre Día 4, Turno 1».
  - Nada de otro mundo llega al Director de Paraguaná: sus notas, los cierres
    y la línea de estado pasan por curiana_eventos.decir_para_el_mundo()
    (mismo alias y mismas reescrituras que los eventos), y el sistema le dice
    qué pueblos NO hay. En el día 3, con los eventos ya traducidos (#138), el
    Director seguía escribiendo «Los Caquetíos y Guaycarí se juntan…» porque
    su propia nota del día 2 lo decía y nadie la filtraba.
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
from dataclasses import replace
from datetime import datetime
from typing import Optional, Sequence

from curiana_eventos import decir_para_el_mundo
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
            "\nNombra sólo a la gente que el turno te da, la del bloque [La gente que hay hoy]. "
            "Aquí no viven guaycaríes, jirajaras ni gayones, y no hay dos pueblos repartiéndose "
            "la misma orilla: esta tierra es de una sola gente."
        )
    return base


def estado_del_dia_cerrado(state, dia: int) -> str:
    """La línea de estado del DÍA REFLEXIONADO, no la del amanecer siguiente.

    Al cerrar el día el estado ya avanzó, y state.to_context_string() dice
    «Día N+1, Turno 1»: el modelo lo copiaba a la cabecera de su reflexión
    («# REFLEXIÓN DEL DIRECTOR — Cierre Día 4, Turno 1» sobre el día 3, run
    0193873d). Aquí el día es `dia`, el turno el último del día, el momento la
    noche y el período el que le toca a ese día en el calendario del mundo."""
    mundo = getattr(state, "mundo", None) or "CURIANA"
    try:
        cerrado = replace(state, dia=dia, turno=max(1, getattr(state, "turnos_por_dia", 1)),
                          momento="noche", estacion=ESTACION_DE_DIA(dia, mundo))
    except TypeError:                       # un estado que no es dataclass (un doble en tests)
        return state.to_context_string()
    return cerrado.to_context_string()


def reflexion_del_dia(client, state, observer_reporte: str, cierres_del_dia: list,
                      *, dia: Optional[int] = None, gente_en_escena: Optional[Sequence[str]] = None,
                      model: str = MODELO_POR_DEFECTO,
                      max_tokens: int = MAX_TOKENS_REFLEXION) -> str:
    """La reflexión del Director sobre el día que acaba de cerrarse: una llamada.

    Se llama al cierre del día, cuando el estado ya apunta al amanecer
    siguiente: el día reflexionado es state.dia - 1 salvo que se pase `dia`.
    La línea de estado es la del día cerrado (estado_del_dia_cerrado), no la
    del amanecer siguiente. `cierres_del_dia` son los cierres narrativos de
    cada turno (los deja director_narrate en state.cierres_del_dia);
    `observer_reporte`, el reporte medido de observer.reporte_dia();
    `gente_en_escena`, quiénes hablaron hoy (el Director no nombra a nadie
    más). En Paraguaná lleva el mundo del día cerrado (su período, de noche) y
    todo el texto libre pasa por decir_para_el_mundo(): ni un nombre ni un
    marco de la era 1 en boca del Director."""
    dia = state.dia - 1 if dia is None else dia
    mundo = getattr(state, "mundo", None)
    decir = lambda t: decir_para_el_mundo(t, mundo)                      # noqa: E731
    partes = [f"Se cierra el día {dia}. Estado del día que se cierra:\n"
              + decir(estado_del_dia_cerrado(state, dia))]
    if (mundo or "") == "PARAGUANÁ":
        bloque = resumen_del_mundo(state, estacion=ESTACION_DE_DIA(dia, mundo), momento="noche")
        if bloque:
            partes.append(bloque)
    gente = [g for g in (gente_en_escena or []) if g]
    if gente:
        partes.append("[La gente que hay hoy]: " + ", ".join(dict.fromkeys(gente))
                      + ". No nombres a nadie que no esté en esta lista.")
    cierres = [c for c in (decir(c).strip() for c in (cierres_del_dia or []) if c) if c]
    partes.append("[Los cierres del día, turno a turno]:\n"
                  + ("\n".join(f"- {c}" for c in cierres) if cierres
                     else "- (hoy no hubo cierres narrativos)"))
    if observer_reporte and observer_reporte.strip():
        partes.append("[Lo medido por el observador]:\n" + observer_reporte.strip())
    notas = decir(getattr(state, "notas_orquestador", "") or "").strip()
    if notas:
        partes.append("[Lo que dejaste anotado al cerrar el día anterior]: " + notas)
    partes.append(
        f"Escribe la reflexión del Director sobre el día {dia} en 4-6 oraciones: qué cambió hoy, "
        "qué palabra nueva prendió (cuál y en boca de quién, si alguna; si ninguna, dilo) y "
        "qué queda abierto para mañana. En primera persona, como Director; sin lenguaje "
        "romántico ni exótico, y sin nombrar nada que el mundo no tenga. "
        f"Reflexionas sobre el día {dia} y sólo sobre él: si encabezas el texto, que el "
        f"encabezado diga «Día {dia}» y nada más — no escribas ningún otro número de día ni "
        "de turno."
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
