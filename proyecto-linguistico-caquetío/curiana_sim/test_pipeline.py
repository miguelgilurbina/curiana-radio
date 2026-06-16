"""
CURIANA — Test de pipeline lingüístico (sin API key, sin Docker)
================================================================

Valida la maquinaria que NO necesita el LLM ni Supabase:
  - score_linguistico v2 (densidad + penalización español, BUG 2)
  - detección de aspecto anclada a raíces verbales
  - extracción de neologismos con regla_aplicada correcta (BUG 3)
  - language_composition (suma de proporciones)
  - contagio sociolingüístico (curiana_social)
  - prompt de rescate intra-turno
  - BUG 1: ningún system_prompt ordena "Responde en español"
  - BUG 3: campos reales de RegistroInteraccion / Neologismo

Uso:  PYTHONUTF8=1 python test_pipeline.py
"""

import sys

PASS, FAIL = 0, 0


def check(nombre, cond, detalle=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✓ {nombre}")
    else:
        FAIL += 1
        print(f"  ✗ {nombre}  {detalle}")


# ── 1. score_linguistico v2 ───────────────────────────────────────────
def test_scoring():
    print("\n── 1. score_linguistico v2 (densidad + penalización) ──")
    from curiana_lexicon import score_linguistico, LexicoComunitario
    lex = LexicoComunitario()

    caq = ("Taya wana-ka arima wara bara-bana. Ta-barsure naba-ni. "
           "Biro rua-da taya. [kali-bana: kali+-bana = orilla de luz]")
    esp = ("Estoy pescando en la orilla del mar y vi muchos peces, "
           "voy a llevar la sal al pueblo para la fiesta de hoy.")

    m_caq = score_linguistico(caq, lex)
    m_esp = score_linguistico(esp, lex)

    check("caquetío puntúa alto (>=7)", m_caq["score"] >= 7.0, f"score={m_caq['score']}")
    check("español puro puntúa bajo (<=2)", m_esp["score"] <= 2.0, f"score={m_esp['score']}")
    check("caquetío > español", m_caq["score"] > m_esp["score"])
    check("densidad caquetía > 0.4", m_caq["densidad"] > 0.4, f"densidad={m_caq['densidad']}")
    check("español detecta funcionales", m_esp["espanol_funcional"] >= 5,
          f"esp_func={m_esp['espanol_funcional']}")
    check("aspecto detectado en caquetío", len(m_caq["aspectos_usados"]) >= 1,
          f"aspectos={m_caq['aspectos_usados']}")
    check("neologismo extraído del patrón", "kali-bana" in m_caq["neologismos_propuestos"],
          f"neos={m_caq['neologismos_propuestos']}")

    # No-falsos-positivos: el español NO debe cosechar palabras caquetías por substring
    check("sin falsos positivos de substring en español",
          len(m_esp["palabras_caquetias"]) <= 1,
          f"palabras={m_esp['palabras_caquetias']}")


# ── 2. Extracción de neologismos + regla_aplicada ─────────────────────
def test_neologismos():
    print("\n── 2. extracción de neologismos (regla_aplicada, BUG 3) ──")
    from curiana_lexicon import extraer_neologismos_del_texto
    txt = "Nüma suna-ni. [habo-bana: habo+-bana = orilla del mar] dijo el piache."
    neos = extraer_neologismos_del_texto(txt, autor="Shaboro", dia=1, turno=2)
    check("extrajo 1 neologismo", len(neos) == 1, f"n={len(neos)}")
    if neos:
        n = neos[0]
        check("campo regla_aplicada existe y no vacío",
              hasattr(n, "regla_aplicada") and n.regla_aplicada,
              f"regla={getattr(n,'regla_aplicada','<falta>')}")
        check("forma normalizada a minúsculas", n.forma == "habo-bana", f"forma={n.forma}")
        check("autor preservado", n.autor == "Shaboro")


# ── 3. language_composition ───────────────────────────────────────────
def test_composition():
    print("\n── 3. language_composition ──")
    from curiana_database import language_composition
    comp = language_composition(["taya", "arima", "bara", "wana", "ka"])
    total = sum(comp.values())
    check("proporciones suman ~1.0", abs(total - 1.0) < 0.01, f"suma={total}")
    check("5 categorías presentes", len(comp) == 5, f"keys={list(comp)}")
    vacia = language_composition([])
    check("lista vacía no rompe", isinstance(vacia, dict))


# ── 4. Contagio sociolingüístico ──────────────────────────────────────
def test_contagio():
    print("\n── 4. contagio (curiana_social) ──")
    from curiana_social import (DifusionLexica, prestigio_de,
                                normalizar_por_dialecto, vecinos)
    d = DifusionLexica()
    d.propagar_uso("sima-bana", "Shaboro")
    exp = d.exposicion_de("Buio-sha", "sima-bana")
    check("aprendiz cruza umbral tras 1 uso de mentor", exp >= 0.6, f"exp={exp:.2f}")
    sugs = d.sugerencias_para("Buio-sha")
    check("se sugiere la palabra al aprendiz", any(f == "sima-bana" for f, _ in sugs))
    check("periférico sin vínculo no adopta",
          len(d.sugerencias_para("Marokoto-ni")) == 0)
    check("no se re-sugiere lo ya usado por el hablante",
          all(f != "sima-bana" for f, _ in d.sugerencias_para("Shaboro")))

    check("prestigio cacique = 1.0", prestigio_de("Manaure") == 1.0)
    check("prestigio foráneo bajo", prestigio_de("Marokoto-ni") < 0.3)
    check("normalización L2 favorece al caribe",
          normalizar_por_dialecto(4.5, "caribe") > normalizar_por_dialecto(4.5, "caquetío"))
    check("vecinos devuelve dict no vacío para cacique",
          isinstance(vecinos("Shaboro"), dict) and len(vecinos("Shaboro")) > 0)


# ── 5. Rescate intra-turno ────────────────────────────────────────────
def test_rescate():
    print("\n── 5. prompt de rescate intra-turno ──")
    from curiana_lexicon import prompt_rescate_linguistico
    p = prompt_rescate_linguistico("Estoy en la orilla", 2.3, 4)
    check("incluye la respuesta fallida", "Estoy en la orilla" in p)
    check("menciona el score", "2.3" in p)
    check("pide reexpresar en caquetío", "caquetío" in p.lower())


# ── 6. BUG 1: ningún prompt ordena español ────────────────────────────
def test_bug1_prompts():
    print("\n── 6. BUG 1 — sin 'Responde en español' en prompts ──")
    import re
    from curiana_agents import ALL_AGENTS
    ofensores = [n for n, a in ALL_AGENTS.items()
                 if re.search(r"[Rr]esponde en espa", a.get("system_prompt", ""))]
    check("ningún system_prompt ordena responder en español",
          not ofensores, f"ofensores={ofensores}")


# ── 7. BUG 3: nombres de campo reales ─────────────────────────────────
def test_bug3_fields():
    print("\n── 7. BUG 3 — nombres de campo en orquestador ──")
    from curiana_observer import RegistroInteraccion, Neologismo
    import dataclasses
    rcampos = {f.name for f in dataclasses.fields(RegistroInteraccion)}
    ncampos = {f.name for f in dataclasses.fields(Neologismo)}
    check("RegistroInteraccion.aspectos_usados existe", "aspectos_usados" in rcampos)
    check("RegistroInteraccion.palabras_caquetias existe", "palabras_caquetias" in rcampos)
    check("Neologismo.regla_aplicada existe", "regla_aplicada" in ncampos)


if __name__ == "__main__":
    print("=" * 58)
    print("  CURIANA — Test de pipeline (sin API key / sin Docker)")
    print("=" * 58)
    test_scoring()
    test_neologismos()
    test_composition()
    test_contagio()
    test_rescate()
    test_bug1_prompts()
    test_bug3_fields()
    print("\n" + "=" * 58)
    print(f"  RESULTADO: {PASS} OK, {FAIL} fallos")
    print("=" * 58)
    sys.exit(1 if FAIL else 0)
