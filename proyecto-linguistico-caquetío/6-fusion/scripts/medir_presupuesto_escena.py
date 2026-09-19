#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mide cuánto ocupa HOY el prompt de un agente de la era 2, y cuánto costarían
los bloques nuevos que propone la escena por lugar.

    6-fusion/issues-pendientes/existir-en-el-mundo-escena-por-lugar-2026-09-17.md §2

Por qué se mide: **la longitud del prompt predice el score, r = −0,48**
(CLAUDE.md, ANALISIS_BASE_2026-08-06). Todo bloque que se añada se paga, así
que cada uno entra con tope declarado y con su coste medido, no estimado.

NO llama a la API y NO importa `curiana_orchestrator_v2` — importarlo
arrastra `curiana_database`, que hace `load_dotenv()` sobre `curiana_sim/.env`.
El único trozo del orquestador que hace falta (`_IDENTIDAD_LINGUISTICA`) se
saca leyendo el fichero con `ast`, sin ejecutarlo.

    python 6-fusion/scripts/medir_presupuesto_escena.py
"""

import ast
import os
import statistics
import sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.normpath(os.path.join(_AQUI, "..", ".."))
_SIM = os.path.join(_RAIZ, "curiana_sim")

# El elenco se decide ANTES de importar curiana_agents (CLAUDE.md, trampas).
os.environ.setdefault("CURIANA_ELENCO", "era2")
sys.path.insert(0, _SIM)

MOMENTOS = ["amanecer", "mañana", "mediodia", "tarde", "anochecer", "noche"]
PERIODOS = ["viento", "seca_larga", "siembra"]


def _forzar_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:                                   # pragma: no cover
        pass


def constante_del_orquestador(nombre: str):
    """Una constante de curiana_orchestrator_v2, leída del fichero con `ast` y
    sin importarlo: importarlo arrastra curiana_database y su load_dotenv."""
    ruta = os.path.join(_SIM, "curiana_orchestrator_v2.py")
    with open(ruta, encoding="utf-8") as f:
        arbol = ast.parse(f.read())
    for n in arbol.body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == nombre:
            return ast.literal_eval(n.value)
    raise SystemExit(f"no encuentro {nombre} en curiana_orchestrator_v2.py")


def identidad_linguistica() -> str:
    # Vive en `curiana_lexicon` desde el corte de serie del 2026-09-18 (el
    # orquestador la re-exporta). Importar el lexicón no arrastra dotenv.
    from curiana_lexicon import IDENTIDAD_LINGUISTICA
    return IDENTIDAD_LINGUISTICA


# ══════════════════════════════════════════════════════════════════════
# Los bloques que PROPONE la escena. Se escriben enteros aquí para que su
# largo se MIDA, no se cuente a mano. Son ejemplos reales del canon de la
# era 2 (Tacuato, Tiempo de Viento) rendidos como los vería el agente.
# ══════════════════════════════════════════════════════════════════════

BLOQUES_PROPUESTOS = {
    "1 ESTAR — [Aquí estás]": (
        "[Aquí estás]: en la orilla de Tacuato, a la caída del sol, untando los "
        "jachos. Contigo están Birokoa, que sube del salinar, y Chakamba, que "
        "ronda las canoas."
    ),
    "2 OÍR — [Lo que se dijo aquí]": (
        "[Lo que se dijo aquí, en este mismo sitio, hace un momento]:\n"
        "— Birokoa: «taya naa-ka biro-ana» (he raspado la costra de sal).\n"
        "— Chakamba: «pia chaa-da-ma?» (¿no vas a salir tú?).\n"
        "— Waranaro: «wa-kari duna-rua-ana» (nuestro pescado está en el agua honda)."
    ),
    "3 HUELLA — [Lo que hiciste ayer]": (
        "[Ayer]: raspaste el biro de las charcas de Tacuato y lo contaste antes "
        "de que suba al cerro; al anochecer bajaste a la orilla. Dijiste "
        "«biro-ana» dos veces."
    ),
    "3 HUELLA — [Lo que trajo quien vino de fuera]": (
        "[Hoy llegó gente]: Bajari, de Caseto, trajo el llamamiento del cerro y "
        "una palabra que aquí nadie usa: «kashi-kasuta-iro»."
    ),
    "4 POTESTAD — [Puedes ir a]": (
        "[A dónde puedes ir mañana]: la orilla de Tacuato (la tuya), el conuco, "
        "el salinar, o el camino a Moruy, que es un día de ida. A la costa del "
        "oeste no vas: no es tu playa."
    ),
}


def main():
    _forzar_utf8()
    from curiana_agents import ALL_AGENTS, MUNDO
    from curiana_lexicon import vocabulario_para_agente, LexicoComunitario
    from curiana_koine import prompt_emocionar
    from curiana_state import estado_inicial
    from curiana_mundo import bloque_tu_tierra, PRESUPUESTO, PRESUPUESTO_DIRECTOR
    from curiana_perfiles import cargar_perfil

    perfil = cargar_perfil("era2")
    lex = LexicoComunitario()
    ident = identidad_linguistica()
    estado = estado_inicial(MUNDO)

    print("=" * 72)
    print(f"  PRESUPUESTO DEL PROMPT — elenco {os.environ['CURIANA_ELENCO']}, "
          f"mundo {MUNDO}, perfil {perfil.nombre}")
    print("=" * 72)

    # ── las piezas fijas ──────────────────────────────────────────────
    ctx = estado.to_context_string()
    print(f"\n[1] LAS PIEZAS DE HOY (día {estado.dia}, {estado.estacion})")
    print(f"  identidad lingüística (fija, los 63) .......... {len(ident):>6}")
    print(f"  bloque de mundo `to_context_string` ........... {len(ctx):>6}")
    fichas = [len(a.get("system_prompt") or "") for a in ALL_AGENTS.values()]
    print(f"  ficha del agente ({len(fichas)}) ..................... "
          f"{round(statistics.mean(fichas)):>6}   (min {min(fichas)} · max {max(fichas)})")
    for t in (1, 2, 3):
        n = len(vocabulario_para_agente(t, lex, contexto=ctx, capas=perfil.capas))
        print(f"  bloque léxico tier {t} ......................... {n:>6}")
    tierras = [len(bloque_tu_tierra(a.get("sitio"), p, m, agente=nombre, dia=1,
                                    capas=perfil.capas))
               for nombre, a in ALL_AGENTS.items() if a.get("sitio")
               for p in PERIODOS for m in MOMENTOS]
    print(f"  [Tu tierra] ({len(tierras)} combinaciones) ............. "
          f"{round(statistics.mean(tierras)):>6}   (tope {PRESUPUESTO}; "
          f"max medido {max(tierras)})")
    print(f"  [El mundo] del Director ....................... "
          f"{'':>6}   (tope {PRESUPUESTO_DIRECTOR})")

    # ── el prompt entero, como lo arma call_agent ─────────────────────
    # Mismo orden y mismas piezas que curiana_orchestrator_v2.call_agent, sin
    # las tres que dependen de lo que pasó en el run (contagio, competencias,
    # idiolecto) ni de la memoria: son las que la escena NO toca.
    print("\n[2] EL PROMPT ENTERO POR AGENTE (sin contagio/competencias/idiolecto/memoria)")
    por_tier = {1: [], 2: [], 3: []}
    for nombre, a in ALL_AGENTS.items():
        tier = a.get("tier", 2)
        partes = [a.get("system_prompt") or "", "---", ident,
                  prompt_emocionar(nombre, a.get("etnia", "caquetío")),
                  "---", ctx, f"[Tu ubicación]: {a.get('ubicacion_default')}"]
        if a.get("sitio"):
            partes.append(bloque_tu_tierra(a["sitio"], estado.estacion, estado.momento,
                                           agente=nombre, dia=1, capas=perfil.capas))
        partes.append(vocabulario_para_agente(tier, lex, contexto=ctx, capas=perfil.capas))
        por_tier.setdefault(tier, []).append(len("\n".join(p for p in partes if p)))
    todos = [n for v in por_tier.values() for n in v]
    for t in sorted(por_tier):
        v = por_tier[t]
        if v:
            print(f"  tier {t} ({len(v):>2} agentes) ... media {round(statistics.mean(v)):>6}"
                  f"   min {min(v):>6}  max {max(v):>6}")
    media = statistics.mean(todos)
    print(f"  LOS {len(todos)} ............... media {round(media):>6}"
          f"   min {min(todos):>6}  max {max(todos):>6}")

    # ── lo que costaría la escena ─────────────────────────────────────
    print("\n[3] LOS BLOQUES QUE PROPONE LA ESCENA — largo medido y coste")
    t1 = statistics.mean(por_tier[1]) if por_tier[1] else media
    t3 = statistics.mean(por_tier[3]) if por_tier[3] else media
    total = 0
    for nombre, texto in BLOQUES_PROPUESTOS.items():
        n = len(texto)
        total += n
        print(f"  {nombre:<40} {n:>5}   "
              f"+{100*n/media:4.1f}% medio · +{100*n/t1:4.1f}% t1 · +{100*n/t3:4.1f}% t3")
    print(f"  {'LOS CUATRO JUNTOS':<40} {total:>5}   "
          f"+{100*total/media:4.1f}% medio · +{100*total/t1:4.1f}% t1 · "
          f"+{100*total/t3:4.1f}% t3")
    print("\n  Referencia: [Tu tierra] entró con tope 320 y eso fue +7,7 % sobre el")
    print("  prompt medio de entonces (mundo-era2-sitios-y-clima.md §5).")

    print("\n[4] LOS BLOQUES, ENTEROS")
    for nombre, texto in BLOQUES_PROPUESTOS.items():
        print(f"\n  ── {nombre} ({len(texto)} car.)")
        for l in texto.splitlines():
            print(f"     {l}")

    voces_por_escena()


# ══════════════════════════════════════════════════════════════════════
# ¿Tiene la capa OÍR algo que oír? La ventana de 12 no se toca, así que la
# pregunta es cuántos de los 12 que hablan en un turno caen en el MISMO
# lugar. Si caen todos en lugares distintos, «lo que se dijo aquí» está
# siempre vacío y la capa 2 no hace nada.
# ══════════════════════════════════════════════════════════════════════

def voces_por_escena(agentes_por_turno: int = 12, turnos_por_dia: int = 6,
                     dias: int = 6):
    import collections
    import derivar_escena_por_lugar as esc
    from curiana_agents import ALL_AGENTS
    PARTICIPANTES_KOINE = constante_del_orquestador("PARTICIPANTES_KOINE")

    # roster `todos`, replicado de curiana_orchestrator_v2.roster_de_habla()
    # sin importar el orquestador: los del roster koiné primero y luego el
    # resto del elenco, sin foráneos.
    foraneas = {"caribe", "gayón", "guaycarí", "jirajara"}
    def foraneo(a):
        return (a.get("etnia") or "caquetío").lower() in foraneas
    primero = [a for a in PARTICIPANTES_KOINE
               if a in ALL_AGENTS and not foraneo(ALL_AGENTS[a])]
    roster = primero + [a for a, d in ALL_AGENTS.items()
                        if a not in primero and not foraneo(d)]

    fichas = {a["nombre"]: a for a in esc.elenco()}
    print(f"\n[5] VOCES POR ESCENA — la ventana de {agentes_por_turno} sobre el "
          f"roster `todos` ({len(roster)}), sin tocarla")
    print(f"  {'día/turno':<12}{'momento':<11}{'escenas':>8}{'solos':>7}"
          f"{'≥2 voces':>10}{'la mayor':>10}")
    tot_escenas = tot_solos = tot_dos = 0
    tot_voces = [0, 0]
    for dia in range(1, dias + 1):
        for turno in range(1, turnos_por_dia + 1):
            n_turno = (dia - 1) * turnos_por_dia + (turno - 1)
            k = (n_turno * agentes_por_turno) % len(roster)
            ventana = [roster[(k + i) % len(roster)] for i in range(agentes_por_turno)]
            momento = MOMENTOS[((turno - 1) * len(MOMENTOS)) // turnos_por_dia]
            grupos = collections.Counter()
            for nombre in ventana:
                a = fichas.get(nombre)
                if not a:
                    continue
                grupos[esc.lugar_de(a, momento, "viento")] += 1
            solos = sum(1 for v in grupos.values() if v == 1)
            dos = sum(1 for v in grupos.values() if v >= 2)
            tot_escenas += len(grupos); tot_solos += solos; tot_dos += dos
            tot_voces[0] += sum(grupos.values())
            tot_voces[1] += sum(v for v in grupos.values() if v >= 2)
            if dia == 1:
                print(f"  D{dia} T{turno:<9}{momento:<11}{len(grupos):>8}{solos:>7}"
                      f"{dos:>10}{max(grupos.values()):>10}")
    print(f"  ── sumados {dias} días ({dias*turnos_por_dia} turnos): "
          f"{tot_escenas} escenas, {tot_solos} con una sola voz, "
          f"{tot_dos} con dos o más")
    print(f"  o sea: {100*tot_dos/max(1,tot_escenas):.0f} % de las escenas tienen a "
          f"alguien a quien oír.")
    print(f"  y por HABLANTE: {tot_voces[1]} de {tot_voces[0]} intervenciones "
          f"({100*tot_voces[1]/max(1,tot_voces[0]):.0f} %) caen en un lugar donde "
          f"habla alguien más ese mismo turno.")


if __name__ == "__main__":
    main()
