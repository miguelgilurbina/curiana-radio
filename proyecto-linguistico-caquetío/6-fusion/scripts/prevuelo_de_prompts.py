#!/usr/bin/env python3
"""PRE-VUELO DE PROMPTS: leer lo que el agente va a recibir ANTES de gastar un día.

Nació el 2026-09-21, antes de repetir la serie C con la tanda del 21 dentro
(«siempre falta un detalle que termina costándonos una corrida», Miguel).
Las listas DEBE / NO_DEBE son las de ESE corte: al cambiar el instrumento se
cambian aquí, y el script falla (exit 1) si algo no cuadra. Última puesta al
día: la tanda de la base (2026-09-23), que añade además un cuarto caso — el
turno en que se NOMBRA a un animal (el mensaje, no sólo el system prompt).

Uso:  python 6-fusion/scripts/prevuelo_de_prompts.py [--volcar]


Monta el system prompt ENTERO de los 63 con el `run_turn` de verdad y `_invoke`
espiado (patrón de `medir_tanda_21.py::_ensayo_de_prompt`), en los tres casos
que la cadena va a correr: control, con escena, y el día de Capubana.
No llama a la API ni a la base. Comprueba CONTENIDO, no sólo largos.
"""
import io
import random
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os
SIM = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "curiana_sim"))
sys.path.insert(0, SIM)

import curiana_lexicon as L                                # noqa: E402
import curiana_agents_era2 as _era2                        # noqa: E402
import curiana_orchestrator_v2 as orch                     # noqa: E402
from curiana_observer import ObserverAgent                 # noqa: E402
from curiana_perfiles import cargar_perfil                 # noqa: E402
from curiana_state import estado_inicial                   # noqa: E402

RESPUESTA = "Taya wana-ka arima wara kari. Ta-barsure naba-ni."


def ensayo(escena: bool, capubana_cada: int, dia: int, turnos: int = 2,
           nombrar: dict | None = None):
    elenco = dict(_era2.ALL_AGENTS)
    perfil = cargar_perfil("era2")
    roster = list(elenco)
    random.seed(21)
    capturas: list[tuple[str, str]] = []
    _invoke, _agentes = orch._invoke, orch.ALL_AGENTS
    _narrar, _evento = orch.director_narrate, orch.director_select_event
    orch._invoke = lambda c, system, user: (capturas.append((system, user)) or RESPUESTA)
    orch.director_narrate = lambda *a, **k: "(narración)"
    orch.director_select_event = lambda s: None
    orch.ALL_AGENTS = elenco
    try:
        state = estado_inicial("PARAGUANÁ")
        state.turnos_por_dia = 6
        state.escena = escena
        state.capubana_cada = capubana_cada
        state.dia = dia
        state.evento_del_turno = None
        lexico = L.LexicoComunitario()
        observer = ObserverAgent(None, lexico)
        memoria = orch.AgentMemory()
        competencia = orch.CompetenciaLexica()
        for _ in range(turnos):
            orch.run_turn(None, state, memoria, lexico, observer,
                          verbose=False, agentes_por_turno=len(roster),
                          roster=list(roster), capas=perfil.capas,
                          competencia=competencia, naming_referente=nombrar)
        # la puerta onomatopéyica vale UN turno (db.6)
        assert lexico.puerta_onomatopeyica is None, "la puerta quedó abierta"
    finally:
        orch._invoke, orch.ALL_AGENTS = _invoke, _agentes
        orch.director_narrate, orch.director_select_event = _narrar, _evento
    return capturas


# Lo que TIENE que estar en los 63 (la tanda del 21 y la de la base) y lo que
# NO puede estar.
DEBE = {
    "el estado es verbo (d21.4)": r"UN ESTADO ES UN VERBO|ESTADO: un estado se predica",
    "ka- atributivo (d21.5)": r"ka-biro|ATRIBUTIVO: ka-",
    "u- no-poseído (d21.13)": r"(?<![\w-])u- ",
    "-bakoa": r"-bakoa",
    "ejemplo biro-bana": r"biro-bana",
    "derivación cero (dc.3)": r"jusual es sembrar",
    "-wa sin glosa (dc.2)": r"-wa y -ana",
}
NO_DEBE = {
    "-naiki (retirado d21.9)": r"-naiki\b",
    "-bacoa (migrado d21.14)": r"-bacoa\b",
    "kali-bana (ejemplo viejo)": r"kali-bana",
    "-gua (migrado dc.2)": r"(?<![\w])-gua\b",
    "región de (glosa sin fuente)": r"región de",
    "buko-ana (d21.6)": r"buko-ana",
    "gallina (europea)": r"gallina",
    "ka-biro = el salinero": r"ka-biro\s*=\s*el salinero",
    "Shaboro (era 1)": r"Shaboro",
    "Buio-sha (era 1)": r"Buio-sha",
    "Golfete de Coro (era 1)": r"Golfete de Coro",
}


def palabras_archivadas():
    """Las formas de FUERA_DEL_HABLA: no deben ENSEÑARSE como entrada léxica.

    Se busca el patrón de entrada del bloque de vocabulario (`forma = glosa` o
    `forma (`), no la subcadena: `kali` vive dentro de otras palabras."""
    fuera = getattr(L, "FUERA_DEL_HABLA", {})
    return sorted(fuera) if isinstance(fuera, dict) else sorted(fuera)


def revisar(nombre, capturas):
    sistemas = [s for s, _ in capturas]
    largos = sorted(len(s) for s in sistemas)
    print(f"\n=== {nombre}: {len(sistemas)} prompts · medio "
          f"{sum(largos)/len(largos):.1f} · min {largos[0]} · max {largos[-1]}")
    ok = True
    for etiqueta, patron in DEBE.items():
        n = sum(1 for s in sistemas if re.search(patron, s, re.S))
        marca = "ok " if n == len(sistemas) else "FALTA"
        if n != len(sistemas):
            ok = False
        print(f"  [{marca}] debe: {etiqueta:<28} {n}/{len(sistemas)}")
    for etiqueta, patron in NO_DEBE.items():
        n = sum(1 for s in sistemas if re.search(patron, s))
        marca = "ok " if n == 0 else "ESTÁ"
        if n:
            ok = False
        print(f"  [{marca}] no debe: {etiqueta:<25} {n}/{len(sistemas)}")
    # archivadas enseñadas como entrada de vocabulario
    fuera = palabras_archivadas()
    golpes = {}
    for f in fuera:
        pat = re.compile(rf"(?<![\w-]){re.escape(f)}(?![\w-])\s*(=|\()")
        n = sum(1 for s in sistemas if pat.search(s))
        if n:
            golpes[f] = n
    print(f"  [{'ok ' if not golpes else 'ESTÁ'}] archivadas enseñadas como entrada: "
          f"{len(golpes)} de {len(fuera)} {dict(list(golpes.items())[:8]) if golpes else ''}")
    if golpes:
        ok = False
    formal = sum(1 for s in sistemas if re.search(r"TRATO FORMAL.*kudanga", s))
    print(f"  [inf] TRATO FORMAL (sólo tier 1, d21.10): {formal}/{len(sistemas)}")
    vacios = sum(1 for _, u in capturas if not u.strip())
    print(f"  [{'ok ' if not vacios else 'MAL'}] user_message vacío: {vacios}")
    if nombre.startswith("con escena") or nombre.startswith("Capubana"):
        aqui = sum(1 for s in sistemas if "[Aquí estás]" in s)
        ubic = sum(1 for s in sistemas if "[Tu ubicación]" in s)
        oir = sum(1 for s in sistemas if "[Lo que se dijo aquí," in s)
        print(f"  [{'ok ' if aqui == len(sistemas) and ubic == 0 else 'MAL'}] "
              f"[Aquí estás] {aqui} · [Tu ubicación] {ubic} · [Lo que se dijo aquí] {oir}")
        if aqui != len(sistemas) or ubic:
            ok = False
    else:
        aqui = sum(1 for s in sistemas if "[Aquí estás]" in s)
        print(f"  [{'ok ' if aqui == 0 else 'MAL'}] control sin [Aquí estás]: {aqui}")
        if aqui:
            ok = False
    return ok, sistemas


if __name__ == "__main__":
    todo_ok = True
    muestras = {}
    for nombre, kw in (
        ("control (sin escena), día 1", dict(escena=False, capubana_cada=0, dia=1)),
        ("con escena, día 1", dict(escena=True, capubana_cada=3, dia=1)),
        ("Capubana, día 3", dict(escena=True, capubana_cada=3, dia=3)),
    ):
        caps = ensayo(**kw)
        ok, sistemas = revisar(nombre, caps)
        todo_ok &= ok
        muestras[nombre] = sistemas[0]

    # EL TURNO DE NOMBRAMIENTO (db.4, db.6): el MENSAJE es lo que cambia. Se
    # nombra a la guacharaca —hueco, animal, con sonido— y se lee lo que los
    # 63 reciben DESPUÉS de pasar por `decir_para_el_mundo`.
    from curiana_koine import REFERENTES_ERA2
    guacharaca = next(r for r in REFERENTES_ERA2 if r["id"] == "guacharaca")
    caps = ensayo(escena=False, capubana_cada=0, dia=1, turnos=1, nombrar=guacharaca)
    mensajes = [u for _, u in caps]
    print(f"\n=== nombramiento (guacharaca, día 1): {len(mensajes)} mensajes")
    comprobaciones = {
        "molde del hueco": r"^\[LO QUE VES SIEMPRE, EN PARAGUANÁ\]",
        "[Lo que se oye]": r"\[Lo que se oye\]: un grito fuerte",
        "invita a nombrar por la voz": r"por cómo suena",
        "no dice ALGO NUEVO": None,
    }
    for etiqueta, patron in comprobaciones.items():
        if patron is None:
            n = sum(1 for u in mensajes if "ALGO NUEVO" not in u)
        else:
            n = sum(1 for u in mensajes if re.search(patron, u))
        marca = "ok " if n == len(mensajes) else "MAL"
        todo_ok &= n == len(mensajes)
        print(f"  [{marca}] {etiqueta:<30} {n}/{len(mensajes)}")
    print(f"  [inf] largo del mensaje: {len(mensajes[0]) if mensajes else 0} caracteres")
    muestras["nombramiento (mensaje)"] = mensajes[0] if mensajes else ""
    print("\n" + ("PRE-VUELO VERDE" if todo_ok else "PRE-VUELO ROJO"))
    if "--volcar" in sys.argv:
        for n, s in muestras.items():
            print(f"\n\n######## {n}\n{s}")
    sys.exit(0 if todo_ok else 1)
