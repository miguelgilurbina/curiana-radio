"""Tests del exportador del índice de runs (issue #42, condición 9 del gate).

`content/simulador/runs/index.json` publicaba `total_turnos: 0` y
`total_dias: 0` para `20091e1f`, que tiene 290 respuestas: el exportador leía
`simulation_runs.total_turns/total_days`, que solo escribe `end_run()` al
terminar el bucle, y ese run lo cortó el teardown. Ahora se MIDEN sobre `turns`.

Sin red y sin base: un cliente falso imita lo que importa de PostgREST, incluida
la trampa — sin `.range()` devuelve como mucho `max_rows` filas, en silencio.
"""

import json

import export_runs_index as eri

RUN_CORTADO = "20091e1f-a06b-4aa3-bad6-486cf1ee3abd"
RUN_COMPLETO = "9bb920eb-fb3e-45c6-82ad-9d614d9a5b97"

# Las claves que consume `RunIndexEntry` en lib/runs.ts. Si cambian, la web rompe.
CLAVES_DEL_INDICE = {
    "id8", "seed_run_id", "categoria", "rol", "pareja", "hito", "started_at",
    "total_dias", "total_turnos", "agentes", "respuestas", "avg_score",
    "pct_caquetio", "neologismos_adoptados", "convergencia", "fijacion",
}


# ══════════════════════════════════════════════════════════════════════
# Cliente falso de PostgREST
# ══════════════════════════════════════════════════════════════════════

class _Respuesta:
    def __init__(self, data):
        self.data = data


class _Query:
    def __init__(self, filas, max_rows):
        self._filas = filas
        self._max_rows = max_rows
        self._columnas = "*"
        self._filtros = []
        self._orden = None
        self._rango = None

    def select(self, columnas="*"):
        self._columnas = columnas
        return self

    def eq(self, columna, valor):
        self._filtros.append((columna, valor))
        return self

    def order(self, columna, desc=False):
        self._orden = (columna, desc)
        return self

    def range(self, desde, hasta):
        # postgrest-py AÑADE offset/limit en cada llamada: reusar el builder apila
        # rangos. El exportador tiene que reconstruir la query por página.
        assert self._rango is None, "range() dos veces sobre el mismo builder"
        self._rango = (desde, hasta)
        return self

    def execute(self):
        filas = [f for f in self._filas
                 if all(f.get(c) == v for c, v in self._filtros)]
        if self._orden:
            columna, desc = self._orden
            filas = sorted(filas, key=lambda f: f[columna], reverse=desc)
        if self._rango:
            desde, hasta = self._rango
            filas = filas[desde:hasta + 1]
        filas = filas[:self._max_rows]          # la truncación silenciosa
        if self._columnas != "*":
            cols = [c.strip() for c in self._columnas.split(",")]
            filas = [{c: f[c] for c in cols if c in f} for f in filas]
        return _Respuesta([dict(f) for f in filas])


class _ClienteFalso:
    def __init__(self, tablas, max_rows):
        self._tablas = tablas
        self._max_rows = max_rows

    def table(self, nombre):
        return _Query(self._tablas.get(nombre, []), self._max_rows)


class _DBFalsa:
    def __init__(self, tablas, max_rows=1000):
        self.client = _ClienteFalso(tablas, max_rows)


# ══════════════════════════════════════════════════════════════════════
# Datos
# ══════════════════════════════════════════════════════════════════════

def _run(run_id, turnos, respuestas, agentes, *, fila_turnos, fila_dias, ended_at,
         neologismos=0, metricas=0, fijadas=0):
    """Tablas de un run como las deja el orquestador en modo --auto."""
    t = [{"id": f"{run_id[:8]}-t{i:06d}", "run_id": run_id,
          "day": i // 2 + 1, "turn_num": i % 2 + 1} for i in range(turnos)]
    r = [{"id": f"{run_id[:8]}-r{k:06d}", "run_id": run_id,
          "turn_id": t[k % turnos]["id"], "agent_name": f"agente{k % agentes}",
          "score": 7.0, "pct_caquetio": 0.99} for k in range(respuestas)]
    return {
        "simulation_runs": [{
            "id": run_id, "started_at": "2026-06-29T21:44:30.07376+00:00",
            "ended_at": ended_at, "total_turns": fila_turnos, "total_days": fila_dias,
        }],
        "turns": t,
        "agent_responses": r,
        "neologisms": [{"id": f"{run_id[:8]}-n{k:06d}", "run_id": run_id,
                        "status": "adoptado" if k % 2 == 0 else "propuesto"}
                       for k in range(neologismos)],
        "koine_metrics": [{"id": f"{run_id[:8]}-m{d:06d}", "run_id": run_id,
                           "day": d, "distance": 0.5 - d * 1e-4}
                          for d in range(1, metricas + 1)],
        "koine_lexicon": [{"id": f"{run_id[:8]}-l{k:06d}", "run_id": run_id,
                           "concepto_id": f"c{k}", "form": f"forma{k}",
                           "fijada_dia": k + 1, "n_variantes": 3}
                          for k in range(fijadas)],
    }


def _juntar(*runs):
    tablas = {}
    for run in runs:
        for nombre, filas in run.items():
            tablas.setdefault(nombre, []).extend(filas)
    return tablas


def _entrada(id8):
    return next(e for e in eri.MANIFIESTO if e["id8"] == id8)


def _cortado():
    """El caso del issue: fila en 0, ended_at NULL, 290 respuestas en 30 turnos."""
    return _run(RUN_CORTADO, turnos=30, respuestas=290, agentes=30,
                fila_turnos=0, fila_dias=0, ended_at=None, metricas=14, fijadas=7)


def _completo():
    return _run(RUN_COMPLETO, turnos=60, respuestas=295, agentes=32,
                fila_turnos=60, fila_dias=30, ended_at="2026-06-29T20:00:00+00:00",
                metricas=30)


# ══════════════════════════════════════════════════════════════════════
# #42 — turnos y días se miden
# ══════════════════════════════════════════════════════════════════════

def test_run_cortado_sale_con_turnos_y_dias_medidos(capsys):
    db = _DBFalsa(_juntar(_cortado(), _completo()))

    fila = eri.resumir_run(db, _entrada("20091e1f"))

    assert fila["total_turnos"] == 30
    assert fila["total_dias"] == 15
    assert fila["respuestas"] == 290
    assert fila["agentes"] == 30
    assert set(fila) == CLAVES_DEL_INDICE     # la forma que consume la web


def test_la_discrepancia_con_la_fila_se_avisa_no_se_tapa(capsys):
    db = _DBFalsa(_juntar(_cortado(), _completo()))
    avisos = []

    eri.resumir_run(db, _entrada("20091e1f"), avisos=avisos)

    salida = capsys.readouterr().out
    assert "total_turns: la fila dice 0, medido 30" in salida
    assert "total_days: la fila dice 0, medido 15" in salida
    assert "ended_at es NULL" in salida
    assert len(avisos) == 3 and all(a.startswith("20091e1f:") for a in avisos)


def test_run_completo_no_da_falsa_alarma(capsys):
    """end_run guarda total_days = state.dia - 1 = max(turns.day): coinciden."""
    db = _DBFalsa(_juntar(_cortado(), _completo()))
    avisos = []

    fila = eri.resumir_run(db, _entrada("9bb920eb"), avisos=avisos)

    assert (fila["total_turnos"], fila["total_dias"]) == (60, 30)
    assert avisos == []
    assert "⚠" not in capsys.readouterr().out


def test_respuestas_sin_turnos_se_avisan():
    run = {"total_turns": 0, "total_days": 0, "ended_at": None}
    avisos = eri.avisos_de_medicion(run, total_turnos=0, total_dias=0, n_resp=290)
    assert any("290 respuestas y ningún turno" in a for a in avisos)


def test_main_escribe_el_indice_con_lo_medido(tmp_path, monkeypatch, capsys):
    db = _DBFalsa(_juntar(_cortado(), _completo()))
    monkeypatch.setattr(eri, "CurianaDB", lambda: db)
    monkeypatch.setattr(eri, "RUNS_DIR", str(tmp_path))

    eri.main()

    indice = json.loads((tmp_path / "index.json").read_text(encoding="utf-8"))
    assert set(indice) == {"version", "generado", "runs"}
    por_id = {r["id8"]: r for r in indice["runs"]}
    assert set(por_id) == {"9bb920eb", "20091e1f"}   # los demás no están en la base
    assert (por_id["20091e1f"]["total_turnos"], por_id["20091e1f"]["total_dias"]) == (30, 15)
    assert por_id["20091e1f"]["fijacion"]["conceptos_fijados"] == 7
    assert "3 aviso(s)" in capsys.readouterr().out


# ══════════════════════════════════════════════════════════════════════
# Paginación — PostgREST trunca a max_rows sin avisar
# ══════════════════════════════════════════════════════════════════════

def _tabla_grande(n):
    return {"x": [{"id": f"f{i:06d}", "v": i} for i in range(n)]}


def test_el_cliente_falso_reproduce_la_truncacion():
    """Sin esto, los tests de paginación podrían pasar sin probar nada."""
    db = _DBFalsa(_tabla_grande(2345))
    assert len(db.client.table("x").select("*").execute().data) == 1000


def test_la_paginacion_junta_mas_de_1000_filas():
    db = _DBFalsa(_tabla_grande(2345))

    filas = eri.todas_las_filas(lambda: db.client.table("x").select("*"))

    assert len(filas) == 2345
    assert len({f["id"] for f in filas}) == 2345      # sin solapes ni duplicados


def test_la_paginacion_no_se_fia_de_la_pagina_corta():
    """Con un max_rows menor que PAGINA, parar en la primera página corta
    volvería a truncar en silencio."""
    db = _DBFalsa(_tabla_grande(2345), max_rows=400)

    filas = eri.todas_las_filas(lambda: db.client.table("x").select("*"))

    assert len(filas) == 2345


def test_resumir_run_pagina_cada_consulta():
    """Todas las tablas que lee el exportador por encima de 1000 filas,
    incluida `simulation_runs` (el run buscado queda fuera de la 1.ª página)."""
    grande = _run(RUN_CORTADO, turnos=1204, respuestas=2500, agentes=40,
                  fila_turnos=1204, fila_dias=602, ended_at="2026-07-01T00:00:00+00:00",
                  neologismos=1100, metricas=1001, fijadas=1001)
    ruido = [{"id": f"00000000-0000-0000-0000-{n:012d}", "started_at": None,
              "ended_at": None, "total_turns": 0, "total_days": 0} for n in range(1500)]
    tablas = _juntar(grande)
    tablas["simulation_runs"] = ruido + tablas["simulation_runs"]
    db = _DBFalsa(tablas)
    avisos = []

    fila = eri.resumir_run(db, _entrada("20091e1f"), avisos=avisos)

    assert fila is not None
    assert (fila["total_turnos"], fila["total_dias"]) == (1204, 602)
    assert fila["respuestas"] == 2500
    assert fila["agentes"] == 40
    assert fila["neologismos_adoptados"] == 550
    assert fila["convergencia"]["dias"] == 1001
    assert fila["fijacion"]["conceptos_fijados"] == 1001
    assert avisos == []
