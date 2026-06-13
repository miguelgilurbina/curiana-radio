"""
test_quick.py — Verificación rápida del stack Curiana
Corre sin llamadas LLM reales. Verifica imports, léxico, DB mock, scoring.
Uso: python test_quick.py
"""

import sys

# Contadores globales de verificación
_OK = 0
_FAIL = 0


def _check(label: str, fn):
    """Ejecuta una verificación, reporta éxito/fallo y acumula contadores."""
    global _OK, _FAIL
    try:
        fn()
        print(f"  ✓ {label}")
        _OK += 1
    except Exception as e:
        print(f"  ✗ {label}  ->  {type(e).__name__}: {e}")
        _FAIL += 1


# ══════════════════════════════════════════════════════════════════════
# 1. IMPORTS
# ══════════════════════════════════════════════════════════════════════

print("\n── 1. Imports de módulos ──")

_MODULES = {}


def _import(name: str):
    def _do():
        mod = __import__(name)
        _MODULES[name] = mod
    return _do


for _mod in (
    "curiana_lexicon",
    "curiana_state",
    "curiana_agents",
    "curiana_observer",
    "curiana_database",
):
    _check(f"import {_mod}", _import(_mod))


# ══════════════════════════════════════════════════════════════════════
# 2. LÉXICO — language_composition
# ══════════════════════════════════════════════════════════════════════

print("\n── 2. Composición de lengua ──")


def _test_composicion():
    from curiana_database import language_composition

    palabras = ["taya", "arima", "bara", "wana"]
    comp = language_composition(palabras)

    assert isinstance(comp, dict), "language_composition debe devolver dict"
    total = sum(comp.values())
    assert abs(total - 1.0) < 0.01, f"proporciones deben sumar ~1.0 (suman {total})"

    print(f"    Input: {palabras}")
    for lang, pct in comp.items():
        bar = "█" * int(round(pct * 20))
        print(f"      {lang:12} {bar:<20} {pct:.1%}")


_check("language_composition(['taya','arima','bara','wana'])", _test_composicion)


# ══════════════════════════════════════════════════════════════════════
# 3. DB MOCK — create_run / save_turn / save_agent_response
# ══════════════════════════════════════════════════════════════════════

print("\n── 3. CurianaDBMock (modo sin Supabase) ──")


def _test_dbmock():
    from curiana_database import CurianaDBMock

    db = CurianaDBMock()

    run_id = db.create_run(model="claude-haiku-4-5-20251001", config={"test": True})
    assert isinstance(run_id, str) and len(run_id) > 0, "create_run debe devolver un id (str)"
    print(f"    create_run            -> {run_id[:8]}...")

    turn_id = db.save_turn(
        run_id=run_id, day=1, turn_num=1, moment="amanecer", season="seca",
        event_description="Shaboro tuvo un sueño.",
    )
    assert isinstance(turn_id, str) and len(turn_id) > 0, "save_turn debe devolver un id (str)"
    print(f"    save_turn             -> {turn_id[:8]}...")

    resp_id = db.save_agent_response(
        turn_id=turn_id, run_id=run_id, agent_name="Shaboro",
        ethnicity="caquetío", tier=1,
        response_text="Taya wana-ka arima wara bara-bana.",
        score=6.0,
        words_used=["taya", "wana", "arima", "bara"],
        aspects_used=["completivo"],
        neologisms_proposed=0,
    )
    assert isinstance(resp_id, str) and len(resp_id) > 0, "save_agent_response debe devolver un id (str)"
    print(f"    save_agent_response   -> {resp_id[:8]}...")


_check("CurianaDBMock: create_run, save_turn, save_agent_response", _test_dbmock)


# ══════════════════════════════════════════════════════════════════════
# 4. SCORING — score_linguistico (caquetío vs español)
# ══════════════════════════════════════════════════════════════════════

print("\n── 4. Scoring lingüístico ──")


def _test_scoring():
    from curiana_lexicon import score_linguistico, LexicoComunitario

    lexico = LexicoComunitario()

    texto_caquetio = (
        "Taya wana-ka arima wara bara-bana. Ta-barsure naba-ni. "
        "Ka biro escaso, mara waya naa-da salinar."
    )
    texto_espanol = (
        "Hoy fui al río muy temprano por la mañana y vi muchos peces. "
        "Mi alma está pensando, pero debemos ir por sal."
    )

    r_caq = score_linguistico(texto_caquetio, lexico)
    r_esp = score_linguistico(texto_espanol, lexico)

    print(f"    Caquetío: score={r_caq['score']:.1f}/10  "
          f"palabras={r_caq['palabras_caquetias']}")
    print(f"    Español : score={r_esp['score']:.1f}/10  "
          f"palabras={r_esp['palabras_caquetias']}")

    assert r_caq["score"] > r_esp["score"], (
        f"el texto caquetío debe puntuar más alto "
        f"(caq={r_caq['score']} vs esp={r_esp['score']})"
    )


_check("score_linguistico: caquetío > español", _test_scoring)


# ══════════════════════════════════════════════════════════════════════
# RESUMEN
# ══════════════════════════════════════════════════════════════════════

_total = _OK + _FAIL
print("\n" + "=" * 50)
if _FAIL == 0:
    print(f"  ✓ {_OK}/{_total} módulos OK")
    print("=" * 50)
    sys.exit(0)
else:
    print(f"  ✗ {_OK}/{_total} módulos OK  ({_FAIL} fallo(s))")
    print("=" * 50)
    sys.exit(1)
