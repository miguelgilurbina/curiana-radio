"""Tests del motor léxico: scoring, compuerta de neologismos, extracción
y ciclo de adopción (curiana_lexicon.py)."""

from curiana_lexicon import (
    LexicoComunitario,
    score_linguistico,
    neologismo_valido,
    extraer_neologismos_del_texto,
)


def _lexico():
    return LexicoComunitario()


# ── score_linguistico ─────────────────────────────────────────────────

def test_score_caquetio_supera_espanol():
    lex = _lexico()
    caq = ("Taya wana-ka arima wara bara-bana. Ta-barsure naba-ni. "
           "Ka biro escaso, mara waya naa-da salinar.")
    esp = ("Hoy fui al río muy temprano por la mañana y vi muchos peces. "
           "Mi alma está pensando, pero debemos ir por sal.")
    assert score_linguistico(caq, lex)["score"] > score_linguistico(esp, lex)["score"]


def test_score_glosas_no_penalizan():
    """Lo que va entre paréntesis es glosa: no puntúa ni penaliza."""
    lex = _lexico()
    con_glosa = "Taya wana-ka arima bara-bana. (Vi peces en la orilla del río.)"
    sin_glosa = "Taya wana-ka arima bara-bana."
    assert (score_linguistico(con_glosa, lex)["espanol_funcional"]
            == score_linguistico(sin_glosa, lex)["espanol_funcional"] == 0)


def test_homografo_para_segun_contexto():
    lex = _lexico()
    # rodeada de caquetío → "para" es el mar (léxico caquetío)
    r_caq = score_linguistico("Taya naa-ni para-bana, wana-ka para wara arima.", lex)
    assert "para" in r_caq["palabras_caquetias"]
    # rodeada de español → es la preposición
    r_esp = score_linguistico("Esto es para que vayas mañana temprano.", lex)
    assert "para" not in r_esp["palabras_caquetias"]
    assert r_esp["espanol_funcional"] > 0


# ── neologismo_valido (compuerta anti-español) ────────────────────────

def test_bloquea_ofensores_observados_en_runs():
    for forma in ("suave-bana-ni", "tension-bana-chi", "boca-pana",
                  "carrera-kata", "guardia-bana", "lanza-sara", "temblor-bana"):
        assert not neologismo_valido(forma), forma


def test_acepta_composiciones_caquetias():
    for forma in ("sima-bana", "kali-dusha", "kuru-bana", "arima-ana", "wa-buco"):
        assert neologismo_valido(forma), forma


# ── extraer_neologismos_del_texto ─────────────────────────────────────

def test_extraccion_y_regla_de_afijo_mas_largo():
    texto = "Taya wana-ka [sima-bana: sima+-bana = orilla del cerro]."
    neos = extraer_neologismos_del_texto(texto, "Shaboro", dia=1, turno=1)
    assert len(neos) == 1
    assert neos[0].forma == "sima-bana"
    # "-bana" debe ganar sobre "-ana" (afijo más largo)
    assert neos[0].regla_aplicada == "-bana"


def test_extraccion_descarta_neologismo_espanol():
    texto = "Naba-ni [guardia-bana: guardia+-bana = puesto de vigilancia]."
    assert extraer_neologismos_del_texto(texto, "Tawaka", dia=1, turno=1) == []


# ── ciclo de adopción en LexicoComunitario ────────────────────────────

def _neo(lex, forma="kali-dusha"):
    neos = extraer_neologismos_del_texto(
        f"[{forma}: kali+dusha = estrella con cola]", "Manaure", dia=3, turno=1)
    lex.registrar_neologismo(neos[0])
    return neos[0]


def test_adopcion_requiere_dos_agentes_y_registra_dia():
    lex = _lexico()
    _neo(lex)
    assert lex.adoptar("kali-dusha", "Shaboro", turno=2, dia=4) is None  # 1er adoptante
    oficial = lex.adoptar("kali-dusha", "Tawaka", turno=1, dia=5)        # 2do → oficializa
    assert oficial is not None and oficial.estado == "adoptado"
    assert oficial.dia_resolucion == 5      # día de ADOPCIÓN, no de propuesta
    assert oficial.dia == 3
    assert "kali-dusha" in lex.palabras_activas()


def test_adopcion_repetida_mismo_agente_no_oficializa():
    lex = _lexico()
    _neo(lex)
    assert lex.adoptar("kali-dusha", "Shaboro", turno=1, dia=4) is None
    assert lex.adoptar("kali-dusha", "Shaboro", turno=2, dia=4) is None


# ── word_source_language debe entender morfología ─────────────────────

def test_word_source_language_resuelve_formas_flexionadas():
    """Lo que se guarda en `word_uses.source_language` tiene que reconocer las
    formas con prefijo posesivo y sufijo de aspecto.

    Antes era un lookup pelado contra VOCABULARIO_BASE, así que `wana-ka` o
    `ta-barsure` se guardaban con NULL. Medido sobre la base local el
    2026-08-06: **27.641 de 54.936 usos (50,3%) sin lengua, y el 100% de ellos
    formas morfológicamente complejas** — justo los usos que prueban que los
    agentes manejan la morfología del proyecto.
    """
    from curiana_database import word_source_language

    for forma in ("wana-ka", "naba-ni", "kaa-ni", "ta-barsure", "pi-barsure"):
        assert word_source_language(forma) is not None, (
            f"{forma} debería resolver a una lengua, no a None")


def test_word_source_language_conserva_la_lengua_hermana():
    """Descomponer no puede convertirlo todo en caquetío: una palabra wayunaiki
    o lokono tiene que seguir siendo suya, que es de lo que vive el scoring.

    Se comprueba sobre TODO el lexicón, no sobre una muestra: si una sola
    entrada cambiara de lengua al pasar por aquí, la composición por lengua de
    los runs quedaría falseada.
    """
    from curiana_database import normalize_source_language, word_source_language
    from curiana_lexicon import VOCABULARIO_BASE

    discrepantes = []
    for palabra, entrada in VOCABULARIO_BASE.items():
        esperada = normalize_source_language(entrada.get("fuente", ""))
        obtenida = word_source_language(palabra)
        if obtenida != esperada:
            discrepantes.append((palabra, esperada, obtenida))

    assert not discrepantes, (
        f"{len(discrepantes)} entradas cambian de lengua al resolverse; "
        f"primeras: {discrepantes[:5]}")


def test_word_source_language_vacio_es_none():
    from curiana_database import word_source_language
    assert word_source_language("") is None


# ── cables trampa de la tanda 2026-09-09 ──────────────────────────────
# Los dos defectos que encontró la medición de contaminación del score
# (6-fusion/medicion_contaminacion_score_2026-09-09.yaml).

def test_palabras_caquetias_no_incluye_otra_lengua_arahuaca():
    """El campo alimenta el contagio léxico, la competencia de formas, el
    idiolecto y `words_used`: todos lo tratan como caquetío. Si vuelve a
    devolver `usadas` entero, una voz wayuu o lokono se propagaría como
    propia."""
    from curiana_lexicon import VOCABULARIO_BASE, score_linguistico

    intruso = next(
        (k for k, e in VOCABULARIO_BASE.items()
         if e.get("fuente") == "lokono" and len(k) >= 5 and "-" not in k),
        None)
    assert intruso, "no hay ninguna entrada lokono con la que probar"

    lex = _lexico()
    r = score_linguistico(f"Taya wana-ka {intruso} bara-bana.", lex)
    assert intruso in r["palabras_arahuacas"], (
        "la voz lokono debe contarse como arahuaca (densidad)")
    assert intruso not in r["palabras_caquetias"], (
        f"'{intruso}' es lokono y se coló en palabras_caquetias")
    assert intruso in r["palabras_otro_arahuaco"]


def test_debe_es_castellano_y_no_fuga_a_otra_lengua_arahuaca():
    """Run c6837386 (2026-09-16): «debe» salía en `palabras_otro_arahuaco`
    porque colisiona con la clave achagua `debe` 'medicina' de la comparanda,
    que se normaliza a proto-arahuaco. Medido antes del arreglo: «taya debe
    buko» → score 4,9 con fuga ×1. Es castellano: cuenta como español
    funcional, y la comparanda no se toca."""
    from curiana_lexicon import ES_STOPWORDS, VOCABULARIO_BASE, score_linguistico

    assert "debe" in ES_STOPWORDS
    assert "debe" in VOCABULARIO_BASE, "la entrada achagua sigue en la comparanda"
    r = score_linguistico("taya debe buko", _lexico())
    assert r["palabras_otro_arahuaco"] == [] and r["otro_arahuaco"] == 0
    assert "debe" not in r["palabras_arahuacas"]
    assert r["espanol_funcional"] == 1
    assert r["palabras_caquetias"] == ["taya", "buko"]


# ── los falsos positivos del cierre del día 2 de la era 2 (2026-09-16) ──
# Re-puntuar las 144 respuestas de los runs c6837386 y 89fc1744 sacó cuatro
# familias de falso positivo. Cada test fija una.

def test_el_castellano_corriente_no_es_prestamo_ni_fuga():
    """`cacique` ×2 y `taita` ×1 salían como préstamo taíno, y `dia` («día»
    sin tilde) como fuga al lokono. Las tres son clave de la comparanda Y
    castellano corriente: el agente escribía en castellano, no tomaba
    prestado. Medido: «…la esencia que sopla el cacique irá al capubana…»
    (todo el entorno es castellano) y «Taita Dabuda naa», que el propio
    agente glosa «Mi abuela dice»."""
    from curiana_lexicon import CASTELLANO_CORRIENTE, VOCABULARIO_BASE

    lex = _lexico()
    for voz in ("cacique", "taita", "dia"):
        assert voz in CASTELLANO_CORRIENTE
        assert voz in VOCABULARIO_BASE, "la comparanda NO se toca"
        r = score_linguistico(f"taya buko {voz} wana-ka", lex)
        assert voz not in r["prestamos_de_esfera"], voz
        assert voz not in r["palabras_otro_arahuaco"], voz
        assert voz not in r["palabras_arahuacas"], voz


def test_el_castellano_corriente_es_neutro_y_no_castiga_como_una_stopword():
    """Se decidió NEUTRO, como `HOMOGRAFOS_ZAVALA`, y no stopword como «debe»
    (#133): «cacique» es palabra de contenido, no el andamiaje gramatical del
    castellano. No es gratis —sigue contando en n_tok, así que diluye la
    densidad—, pero no pesa lo que pesa «el/la/de»."""
    lex = _lexico()
    neutro = score_linguistico("taya buko cacique wana-ka", lex)
    stopword = score_linguistico("taya buko porque wana-ka", lex)
    assert neutro["espanol_funcional"] == 0
    assert stopword["espanol_funcional"] == 1
    assert neutro["score"] > stopword["score"]
    # y diluye: la misma frase sin la voz castellana puntúa más
    limpia = score_linguistico("taya buko wana-ka", lex)
    assert limpia["densidad"] > neutro["densidad"]


def test_el_castellano_corriente_es_solo_la_forma_pelada():
    """`ta-bohío` («descanso en mi hamaca en el bohío», run 89fc1744) lleva el
    posesivo caquetío: ahí la lengua está haciendo algo con la raíz, que es la
    pinta de un préstamo de verdad. Sigue contando como préstamo de esfera."""
    lex = _lexico()
    r = score_linguistico("nüma hamaka-ni ta-bohío kashi", lex)
    assert r["prestamos_de_esfera"] == ["ta-bohío"]
    assert r["palabras_otro_arahuaco"] == []


# ── el hispanismo de origen indígena (día 1 de la serie B, 2026-09-17) ──

def test_el_hispanismo_de_origen_indigena_no_es_prestamo_de_esfera():
    """`loanword_uses` registró 7 usos el día 1 de la serie B (run 3973d317)
    y los 7 eran castellano: «Las manos ocupadas limpiando yuca» (Harifuche),
    «Maíz, yuca ta-kana» (Hiko), «Casabe kaa-ni wara amana-ni» (Kunaro-bana).
    El agente no toma prestada una voz de las islas: escribe la palabra que el
    castellano tomó prestada hace cinco siglos y usa como propia."""
    from curiana_lexicon import (ESFERA_DE_CONTACTO, HISPANISMOS_DE_ESFERA,
                                 VOCABULARIO_BASE, _familia_de_token)

    lex = _lexico()
    for voz in ("casabe", "maíz", "yuca"):
        assert voz in HISPANISMOS_DE_ESFERA
        assert voz in VOCABULARIO_BASE, "la comparanda NO se toca"
        assert _familia_de_token(voz) in ESFERA_DE_CONTACTO
        r = score_linguistico(f"taya buko {voz} wana-ka", lex)
        assert r["prestamos_de_esfera"] == [], voz
        assert r["hispanismos_de_esfera"] == [voz], voz
        assert r["palabras_otro_arahuaco"] == [], voz


def test_el_hispanismo_no_mueve_el_score():
    """La lista hace lo MÍNIMO: sólo saca la voz de `prestamos_de_esfera`, que
    no entra en el score. Si se hubiera ampliado `CASTELLANO_CORRIENTE` —su
    sitio natural— la voz dejaría de ser arahuaca y bajaría la `densidad`, que
    pesa 6 de los 10 puntos: 147 de las 2.515 respuestas de la base habrían
    cambiado de score a mitad de la serie B. Medido en
    6-fusion/medicion_hispanismos_loanword_uses_2026-09-17.yaml: Δ = 0 en
    score, densidad, pct_caquetio_especifico, otro_arahuaco y espanol_funcional
    en las 2.515."""
    import curiana_lexicon as L

    lex = _lexico()
    frase = "taya buko casabe yuca wana-ka maíz"
    real = L.HISPANISMOS_DE_ESFERA
    try:
        L.HISPANISMOS_DE_ESFERA = frozenset()
        antes = score_linguistico(frase, lex)
        L.HISPANISMOS_DE_ESFERA = real
        despues = score_linguistico(frase, lex)
    finally:
        L.HISPANISMOS_DE_ESFERA = real
    for campo in ("score", "densidad", "pct_caquetio_especifico",
                  "otro_arahuaco", "espanol_funcional", "palabras_caquetias",
                  "palabras_arahuacas", "palabras_otro_arahuaco"):
        assert antes[campo] == despues[campo], campo
    assert len(antes["prestamos_de_esfera"]) == 3
    assert despues["prestamos_de_esfera"] == []
    # residuo declarado: sigue sumando densidad arahuaca
    assert "casabe" in despues["palabras_arahuacas"]


def test_el_hispanismo_es_solo_la_forma_pelada():
    """`ta-casabe` («Paa-ka ta-casabe, paa-ka ta-chicha», 4 respuestas de la
    base) lleva el posesivo caquetío encima de la raíz ajena: la lengua está
    haciendo algo con ella, que es la pinta de un préstamo de verdad. Misma
    regla que `CASTELLANO_CORRIENTE` con `ta-bohío`."""
    lex = _lexico()
    r = score_linguistico("nüma wana-ka ta-casabe ta-yuca kashi", lex)
    assert sorted(r["prestamos_de_esfera"]) == ["ta-casabe", "ta-yuca"]
    assert r["hispanismos_de_esfera"] == []


def test_la_voz_indigena_sigue_siendo_prestamo_aunque_su_hispanismo_no_lo_sea():
    """El criterio es la ORTOGRAFÍA de la clave, y el lexicón ya lo tenía
    escrito: `maisi` dice «→ español maíz» y `cazabi` «→ español cazabe». Ahí
    la clave es la forma indígena y el castellano es OTRA palabra: escribir
    `maisi` sí es hablar taíno. Y `watapana` no es castellano en ninguna
    grafía —el castellano dice dividivi—, así que sigue entero como préstamo
    (29 respuestas de la base)."""
    from curiana_lexicon import HISPANISMOS_DE_ESFERA

    lex = _lexico()
    for voz in ("maisi", "cazabi", "watapana"):
        assert voz not in HISPANISMOS_DE_ESFERA, voz
        r = score_linguistico(f"taya buko {voz} wana-ka", lex)
        assert r["prestamos_de_esfera"] == [voz], voz


def test_todo_hispanismo_declarado_es_una_clave_de_la_esfera():
    """Una voz que no sea clave del lexicón con familia de la esfera no puede
    salir nunca en `prestamos_de_esfera`: declararla aquí sería una lista
    muerta que nadie ve envejecer."""
    from curiana_database import normalize_source_language
    from curiana_lexicon import (ESFERA_DE_CONTACTO, HISPANISMOS_DE_ESFERA,
                                 VOCABULARIO_BASE)

    assert HISPANISMOS_DE_ESFERA
    for voz in HISPANISMOS_DE_ESFERA:
        assert voz in VOCABULARIO_BASE, voz
        fam = normalize_source_language(VOCABULARIO_BASE[voz].get("fuente", ""))
        assert fam in ESFERA_DE_CONTACTO, (voz, fam)


def test_las_dos_listas_de_castellano_no_se_pisan():
    """`CASTELLANO_CORRIENTE` y `HISPANISMOS_DE_ESFERA` tratan la misma
    intuición con dos fuerzas distintas —la primera neutraliza del todo y MUEVE
    el score, la segunda sólo deja de llamarlo préstamo—. Que una voz esté en
    las dos escondería cuál de las dos la está resolviendo."""
    from curiana_lexicon import CASTELLANO_CORRIENTE, HISPANISMOS_DE_ESFERA

    assert not (CASTELLANO_CORRIENTE & HISPANISMOS_DE_ESFERA)


def test_la_raiz_decide_la_lengua_del_token_con_guion():
    """`juri-ima` y `lawari-ima` —raíces caquetías + el sufijo ATESTIGUADO
    `-ima` de REGLAS_ZAVALA— salían LOKONO por la clave `ima` 'enemigo' de la
    comparanda, porque `_familia_de_token` quitaba siempre el primer segmento
    como si fuera prefijo. Y el defecto tenía su reverso: `sucu-bana`,
    `bucu-ana` e `iri-ka` (raíces LOKONO + afijo caquetío) se contaban como
    caquetío porque ganaba la clave del afijo. La raíz decide en los dos
    sentidos."""
    from curiana_lexicon import _familia_de_token

    for tok in ("juri-ima", "lawari-ima", "maa-to"):
        assert _familia_de_token(tok) == "caquetío", tok
    for tok in ("sucu-bana", "bucu-ana", "iri-ka"):
        assert _familia_de_token(tok) == "lokono", tok
    # el prefijo caquetío sobre raíz ajena NO vuelve propia la raíz
    assert _familia_de_token("ka-to") == "lokono"
    assert _familia_de_token("ta-bohío") == "taíno"
    # y lo que ya resolvía bien sigue resolviendo bien
    assert _familia_de_token("ta-barsure") == "caquetío"
    assert _familia_de_token("wana-ka") == "caquetío"


def test_un_afijo_atestiguado_suelto_no_es_otra_lengua():
    """«…tüshi-ima tüshi ima agua fría de quebrada…» (run 89fc1744, tier 1):
    el agente descompone su propio compuesto y escribe el sufijo suelto.
    `-ima` es afijo atestiguado (REGLAS_ZAVALA); que la comparanda tenga una
    clave `ima` 'enemigo' (lokono) con la misma forma no lo vuelve lokono.

    La corrección vive en la lectura del TEXTO, no en el diccionario: la
    entrada `ima` sigue siendo lokono y `word_source_language` la devuelve
    así (ver test_word_source_language_conserva_la_lengua_hermana)."""
    from curiana_database import word_source_language
    from curiana_lexicon import TODAS_LAS_REGLAS, _familia_de_token

    assert "-ima" in TODAS_LAS_REGLAS
    assert _familia_de_token("ima") == "lokono" == word_source_language("ima")
    r = score_linguistico("taya wana-ka tüshi-ima tüshi ima", _lexico())
    assert r["palabras_otro_arahuaco"] == []
    assert "ima" in r["palabras_caquetias"]


def test_nombrar_la_lengua_no_es_hablarla():
    """«Wayunaiki no. Lokono no. Ta lengua, caquetío.» (run c6837386, tier 3)
    salía como fuga al lokono — cuando el agente decía justamente lo
    contrario. Es una mención metalingüística de un nombre propio.

    Pero el etnónimo es HOMÓGRAFO del sustantivo 'persona' de su propia
    lengua, así que no puede ser neutro de oficio: con un vecino arahuaco
    vuelve a ser la palabra y vuelve a penalizar, que es lo que impide que la
    medición anticircular se quede ciega."""
    from curiana_lexicon import GLOTONIMOS_DE_LA_COMPARANDA, VOCABULARIO_BASE

    assert "lokono" in GLOTONIMOS_DE_LA_COMPARANDA
    assert "lokono" in VOCABULARIO_BASE, "la comparanda NO se toca"
    lex = _lexico()
    mencion = score_linguistico("wayunaiki no lokono no ta lengua caquetío", lex)
    assert mencion["palabras_otro_arahuaco"] == []
    assert "lokono" not in mencion["palabras_arahuacas"]
    uso = score_linguistico("taya buko lokono wana-ka", lex)
    assert uso["palabras_otro_arahuaco"] == ["lokono"]


def test_el_arreglo_no_toca_una_frase_de_canon_puro():
    """La comparabilidad de los runs del 16 depende de esto: el arreglo sólo
    puede moverse donde hay castellano, glotónimo o un token partido. En canon
    puro no dispara ninguna de las tres cosas, y toda voz usada sigue siendo
    caquetía. Medido sobre seis frases de canon: Δ score = 0,00 (y sobre las
    2.371 respuestas de la base, Δ medio = −0,0005)."""
    from curiana_lexicon import (CASTELLANO_CORRIENTE,
                                 GLOTONIMOS_DE_LA_COMPARANDA, _tokenizar)

    lex = _lexico()
    canon = [
        "Taya wana-ka ta-barsure. Waya naa-ni para-bana.",
        "Pia suna-da wa-duna kashi. Nüma masa-ka arima-kana.",
        "Taya maa-ni: saa kali-bana wara tüshi-ni, naka waya naa-da para.",
        "Wa-para-ubana juri wana-ka. Taya kaa-ni hayo, naba-ni boratio.",
        "Nüma panaa-ni chakamba. Kanoa-kana, pia wana-ka?",
    ]
    for frase in canon:
        tokens = set(_tokenizar(frase))
        assert not (tokens & CASTELLANO_CORRIENTE), frase
        assert not (tokens & GLOTONIMOS_DE_LA_COMPARANDA), frase
        r = score_linguistico(frase, lex)
        assert r["palabras_otro_arahuaco"] == [], frase
        assert r["prestamos_de_esfera"] == [], frase
        assert r["palabras_caquetias"] == r["palabras_arahuacas"], frase
        assert r["score"] >= 7.5, (frase, r["score"])


def test_deteccion_de_vocabulario_respeta_el_limite_de_morfema():
    """Casaba por subcadena en cualquier posición: `li` disparaba dentro de
    `kali-taro` y `bi` dentro de `biro`, 409 veces cada una."""
    from curiana_lexicon import detectar_uso_vocabulario

    lex = _lexico()
    hallado = set(detectar_uso_vocabulario("kali-taro biro sima-bana", lex))
    assert "kali" in hallado and "sima" in hallado and "bana" in hallado, (
        "los morfemas de un compuesto SÍ deben detectarse")
    assert "li" not in hallado, "'li' casó dentro de 'kali-taro'"
    assert "bi" not in hallado, "'bi' casó dentro de 'biro'"
