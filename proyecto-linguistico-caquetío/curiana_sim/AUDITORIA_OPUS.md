# AUDITORÍA TÉCNICA — Simulador de Emergencia Lingüística Caquetía (Curiana)

**Auditor:** Ingeniería multi-agente + lingüística computacional
**Fecha:** 2026-06-13
**Alcance:** `curiana_lexicon.py`, `curiana_orchestrator_v2.py`, `curiana_observer.py`, `curiana_agents.py`, `curiana_state.py`
**Objetivo del sistema:** maximizar el % de vocabulario caquetío-arahuacano en las respuestas de 60 agentes Haiku, con morfología activa (`-ka`, `-ni`, `-da`).

---

## 1. DIAGNÓSTICO DEL SISTEMA ACTUAL

### 1.1 Mecanismos actuales para forzar el caquetío (qué existe)

El sistema apila **cinco capas** de presión lingüística, ensambladas en `call_agent()` (orchestrator, orden: persona → identidad lingüística → mundo → léxico → memoria → refuerzo):

| Capa | Fuente | Función |
|------|--------|---------|
| Identidad nativa global | `_IDENTIDAD_LINGUISTICA` (orchestrator) | "Tu lengua materna es el caquetío; el español es forastero" + ejemplo modelo |
| Reglas + léxico por tier | `vocabulario_para_agente(tier, lexico)` | T1 = `prompt_reglas_completo()` (~450 pal.), T2 = `prompt_reglas_breve()`, T3 = micro-bloque |
| Léxico comunitario vivo | `prompt_lexico_activo()` / `prompt_pendientes_evaluacion()` | inyecta neologismos adoptados + en evaluación |
| Memoria rolling | `AgentMemory` (últimas 3) | continuidad de estilo |
| Refuerzo correctivo | `prompt_refuerzo(score, palabras)` vía `observer.feedback_para_agente()` | feedback escalonado por umbral de score |

Esto es una buena arquitectura de partida: **separación correcta entre conocimiento heredado (`VOCABULARIO_BASE`) y léxico emergente (`LexicoComunitario`)**, scoring local sin coste de tokens, y un bucle de retroalimentación. La morfología está modelada como **reglas productivas** (no como diccionario cerrado), lo cual es metodológicamente sólido.

### 1.2 Puntos de fuga hacia el español (dónde falla)

Hay **un fallo estructural que domina a todos los demás**: el feedback correctivo llega **un turno tarde**.

```
call_agent() → respuesta → observer.analizar() → feedback_para_agente()
       ↑                                                    │
       └──────────── se aplica en el TURNO SIGUIENTE ───────┘
```

`feedback_para_agente()` lee `scores[-1]`, que es el score del turno anterior. Pero la memoria rolling y la activación de agentes (`agentes_activos[:6]`, eventos aleatorios) hacen que **muchos agentes no vuelvan a hablar en varios turnos**, o nunca. El refuerzo, por tanto, casi nunca se aplica sobre el agente que falló, en el momento en que falló. **No hay regeneración intra-turno.** Si un agente devuelve español puro con score 1.5, esa respuesta se persiste tal cual en Supabase y en la memoria; el sistema solo "se molesta" la próxima vez que ese agente aparezca.

Otras fugas concretas:

- **Las personas de los agentes contradicen el constraint global.** Casi todos los `system_prompt` de `curiana_agents.py` terminan con *"Responde en español..."*: "Responde en español con palabras caquetías insertadas" (Manaure), "Responde en español natural, cálido" (Nubiri-sha), "Responde en español dinámico" (Tawaka). Esto entra en **conflicto directo** con `_IDENTIDAD_LINGUISTICA` ("habla en caquetío"). Cuando un prompt da dos instrucciones opuestas, el modelo Haiku tiende a seguir la **última y más concreta orientada a comportamiento** — y "responde en español" es exactamente eso. El propio Observer hereda el marco viejo: su `OBSERVER_SYSTEM` dice "Los agentes hablan en español con interferencia caquetía", fosilizando el objetivo que se quiere superar.

- **`detectar_uso_vocabulario()` cuenta substrings, no palabras.** Usa `if palabra in texto_lower`. Esto produce **falsos positivos masivos**: `"ka"` (conector) matchea dentro de "*ka*shi", "Tawa*ka*", "bar*ka*"; `"naa"`, `"awa"`, `"ama"` (madre) matchea en "ll*ama*", "rec*lama*"; `"sima"` en "deci*sima*". Un agente puede escribir **español puro** y cosechar puntos de léxico caquetío por coincidencias de substring. Esto **infla el score y desactiva el refuerzo** justo cuando más se necesita.

- **El score satura demasiado pronto.** `min(len(usadas) * 1.2, 6.0)` → con 5 "palabras" detectadas (reales o por substring) ya tienes 6/10. El umbral de refuerzo es 7.0, alcanzable con 5 palabras + 1 aspecto. Un agente puede quedar "exento de refuerzo" con una sola frase mediocre.

- **No hay penalización por español.** El score es puramente aditivo sobre lo caquetío; nunca resta por presencia de español. Una respuesta de 80 palabras en español con 5 términos caquetíos puntúa igual que una de 10 palabras 100% caquetía. **La densidad real (caquetío / total) nunca se mide.** Esto es el agujero central: el objetivo declarado es "% de vocabulario caquetío", pero la métrica no es un porcentaje.

- **`max_tokens=500`** sin instrucción de brevedad: el modelo llena el espacio, y el relleno tiende a ser español (es más fácil).

### 1.3 Robustez del sistema de scoring

Débil. Es determinista y barato (bien), pero:
- mide **conteo absoluto**, no densidad relativa;
- es **engañable** por substrings;
- **satura** y deja huecos sin refuerzo;
- la detección de aspecto `\b\w+{s}\b` con `s="ka"` matchea cualquier palabra terminada en "ka" (incluido "Tawa**ka**", "ata**ca**"), confundiendo nombres propios y español con morfología verbal.

### 1.4 Bugs y edge cases concretos

| # | Ubicación | Bug | Impacto |
|---|-----------|-----|---------|
| B1 | `orchestrator_v2.py:327` | `getattr(registro, "aspectos_detectados", [])` — el campo real en `RegistroInteraccion` es **`aspectos_usados`**. El `getattr` con default enmascara el error: **`aspects_used` se persiste SIEMPRE como `[]`** en Supabase. | Datos de aspecto perdidos silenciosamente |
| B2 | `orchestrator_v2.py` (save_neologism) | `getattr(neo, "regla", "desconocida")` — el campo real en `Neologismo` es **`regla_aplicada`**. **La regla morfológica se guarda SIEMPRE como "desconocida"** en DB. | Datos morfológicos perdidos |
| B3 | `lexicon.py` `detectar_uso_vocabulario` | match por substring (ver 1.2) | Score inflado, falsos positivos |
| B4 | `lexicon.py` `score_linguistico` aspecto | `rf'\b\w+{s}\b'` con `s` corto matchea nombres propios y español | Aspecto falso-positivo |
| B5 | `observer.py` `procesar_adopciones` | un agente puede "auto-adoptar" si su forma coincide con `neo.forma` de un pendiente previo de otro; **no hay deduplicación de formas idénticas con distinto significado**: dos agentes acuñando `[kali-bana]` con sentidos distintos colisionan en `_lexico[forma]`. | Colisión semántica |
| B6 | `lexicon.py` `extraer_neologismos` | la detección de regla por `forma.endswith(sufijo[1:])` con sufijos como `-ka`/`-gua`/`-ana` se solapa: `"buco-ana"` termina en "ana" pero también en "-na"; el primer match gana arbitrariamente según orden de `dict`. | Etiqueta de regla imprecisa |
| B7 | `observer.py` `reporte_estacion` | `adoptadas` filtra por `r.dia == n.dia and r.estacion`, pero un neologismo adoptado días después de acuñarse tiene `n.dia` = día de acuño; el cruce puede no encontrarlo. | Subconteo de adopciones |
| B8 | `orchestrator_v2.py` `director_select_event` | `prob` puede superar 1.0 (0.3+0.2+0.15+0.3) y nunca se acota; `random.random() > prob` siempre False → evento garantizado los días múltiplos de 3 con tensión alta. | Eventos sobre-frecuentes |

---

## 2. ANÁLISIS DE `score_linguistico()` Y PROPUESTA DE MEJORA

### 2.1 Evaluación

```python
score += min(len(usadas) * 1.2, 6.0)
score += min(len(neos_patron) * 1.5, 2.0)
score += min(len(aspectos) * 1.0, 2.0)
```

- **¿Penaliza el español?** No. Cero penalización. Este es el defecto crítico.
- **¿Premia la morfología activa?** Marginalmente (2 pts máx, saturable con 2 aspectos) y con detección frágil.
- **¿Mide densidad (% caquetío)?** No. Mide conteo absoluto. El objetivo del proyecto ("maximizar % de vocabulario caquetío") **no es lo que la función calcula.**

### 2.2 Versión mejorada (código funcional)

Principios de rediseño:
1. **Tokenizar de verdad** y matchear palabras completas (elimina B3).
2. **Medir densidad** `caquetío / total_tokens` como núcleo del score.
3. **Penalizar explícitamente** marcadores de español (stopwords funcionales: artículos, preposiciones, conjugaciones de "estar/ser/ir").
4. **Premiar morfología** con detección anclada a raíces verbales conocidas (no a cualquier `\w+ka`).
5. **Bonus por neologismos** bien formados.

```python
import re
import unicodedata

# Stopwords funcionales del español: alta frecuencia, imposibles de confundir
# con caquetío. Su presencia es señal directa de fuga al castellano.
ES_STOPWORDS = {
    "el","la","los","las","un","una","unos","unas","lo","al","del",
    "de","en","con","por","para","sin","sobre","entre","hacia","desde","hasta",
    "y","o","u","pero","sino","aunque","porque","que","si","como","cuando",
    "es","son","era","eran","fue","fueron","estar","esta","este","esto","estoy",
    "estas","estos","estamos","estan","ser","soy","eres","somos","voy","vas","va",
    "vamos","van","tengo","tiene","tienen","hay","hacer","hago","hace","muy","mas",
    "yo","tu","ella","nosotros","ellos","mi","mis","su","sus","me","te","se","nos",
    "no","ya","aqui","alli","ahora","despues","antes","hoy","ayer","manana",
}

# Sufijos aspectuales anclados a raíces verbales conocidas (de VOCABULARIO_BASE)
_RAICES_VERB = {k for k, v in VOCABULARIO_BASE.items()
                if v.get("cat") in ("v_raiz",)}

def _normalizar(texto: str) -> str:
    # quita glosas entre paréntesis (no deben puntuar como caquetío ni penalizar)
    texto = re.sub(r"\([^)]*\)", " ", texto)
    return texto

def _tokenizar(texto: str) -> list[str]:
    # tokens alfabéticos, conservando guion interno (ta-barsure, naa-ka)
    return re.findall(r"[a-záéíóúñü]+(?:-[a-záéíóúñü]+)*", texto.lower())

def _aspectos_morfologicos(tokens: list[str]) -> list[str]:
    """Detecta -ka/-ni/-da SOLO sobre tokens cuyo segmento previo es raíz verbal
    conocida o que contienen guion morfológico (naa-ka, wana-ni)."""
    encontrados = []
    mapa = {"ka": "completivo", "ni": "continuativo", "da": "prospectivo"}
    for tok in tokens:
        # forma con guion: raiz-sufijo
        if "-" in tok:
            raiz, _, suf = tok.rpartition("-")
            if suf in mapa and (raiz in _RAICES_VERB or len(raiz) >= 3):
                encontrados.append(mapa[suf])
            continue
        # forma aglutinada: raizverbal + sufijo (naaka, wanani)
        for raiz in _RAICES_VERB:
            for suf, nombre in mapa.items():
                if tok == raiz + suf:
                    encontrados.append(nombre)
    return list(dict.fromkeys(encontrados))  # únicos, orden estable

def score_linguistico(texto: str, lexico: "LexicoComunitario") -> dict:
    limpio = _normalizar(texto)
    tokens = _tokenizar(limpio)
    n_tok = len(tokens) or 1

    activos = set(lexico.palabras_activas())          # base + adoptados
    # match por palabra completa, contando también prefijos posesivos:
    # ta-barsure cuenta como caquetío aunque "ta-barsure" no esté literal en léxico
    def es_caquetio(tok: str) -> bool:
        if tok in activos:
            return True
        # prefijo posesivo + raíz conocida
        for pref in ("ta", "wa", "ma", "ka"):
            if tok.startswith(pref + "-") and tok.split("-", 1)[1] in activos:
                return True
        # raíz verbal + aspecto (naa-ka, wana-ni, naaka)
        base = tok.split("-")[0]
        if base in _RAICES_VERB:
            return True
        return False

    usadas    = [t for t in tokens if es_caquetio(t)]
    esp_func  = [t for t in tokens if t in ES_STOPWORDS]
    neos      = PATRON_NEOLOGISMO.findall(texto)
    aspectos  = _aspectos_morfologicos(tokens)

    # ── Núcleo: densidad caquetía (0..1) ──
    densidad = (len(usadas) / n_tok) if usadas else 0.0
    # penalización por español funcional (cada stopword resta densidad efectiva)
    penal_es = len(esp_func) / n_tok

    # Score 0-10:
    #   60% densidad caquetía  (0..6)
    #   20% morfología activa  (0..2, 1 pt por aspecto distinto)
    #   10% neologismos        (0..1)
    #   10% riqueza léxica      (0..1, palabras caquetías DISTINTAS)
    #   − penalización español  (hasta −3)
    score  = 6.0 * min(densidad / 0.6, 1.0)           # densidad objetivo: 60%
    score += min(len(aspectos) * 1.0, 2.0)
    score += min(len(neos) * 0.5, 1.0)
    score += min(len(set(usadas)) / 8.0, 1.0)
    score -= min(penal_es * 6.0, 3.0)                  # castigo al castellano
    score  = round(max(0.0, min(score, 10.0)), 1)

    obs = []
    obs.append(f"densidad={densidad:.0%}")
    if usadas:   obs.append(f"caq[{len(set(usadas))}]: {', '.join(sorted(set(usadas))[:8])}")
    if aspectos: obs.append(f"aspecto: {', '.join(aspectos)}")
    if esp_func: obs.append(f"⚠ español funcional×{len(esp_func)}")
    if neos:     obs.append(f"+{len(neos)} neologismo(s)")
    if score < 5: obs.append("⚠ score bajo — activar rescate")

    return {
        "palabras_caquetias": list(dict.fromkeys(usadas)),
        "neologismos_propuestos": [m[0] for m in neos],
        "aspectos_usados": aspectos,
        "densidad": round(densidad, 3),
        "espanol_funcional": len(esp_func),
        "score": score,
        "observacion": " | ".join(obs),
    }
```

**Diferencias clave frente al original:** densidad como núcleo (alinea métrica ↔ objetivo), penalización real al español, matching por palabra completa, aspecto anclado a raíces verbales reales. Devuelve además `densidad` y `espanol_funcional`, que el dashboard y el rescate pueden consumir directamente.

---

## 3. INGENIERÍA DE PROMPTS — REESCRITURA CONCRETA

### 3.0 Cambio transversal previo (obligatorio)

Antes de tocar los generadores: **eliminar la coletilla "Responde en español..." de los 60 `system_prompt`** en `curiana_agents.py` y reemplazarla por una orientación coherente. Sin esto, ningún prompt de léxico funcionará — el agente recibe órdenes contradictorias. Reemplazos:

- Manaure: ~~"Responde en español con palabras caquetías insertadas."~~ → `"Hablas en caquetío. Frases cortas, completivas (-ka). Glosa al español solo entre paréntesis si es imprescindible."`
- Tawaka: → `"Hablas en caquetío, con energía y prospectivo (-da). Glosa mínima entre paréntesis."`

Patrón general (aplicable por script):
`"Responde en español ...."` → `"Respondes en caquetío-arahuacano. Español solo como glosa entre paréntesis al final."`

También corregir `OBSERVER_SYSTEM`: cambiar *"Los agentes hablan en español con interferencia caquetía"* por *"Los agentes hablan caquetío-arahuacano; tu trabajo es medir su densidad y pureza, detectando fugas al español."*

### 3.1 `prompt_reglas_breve()` — versión mejorada

```python
def prompt_reglas_breve() -> str:
    return """[CAQUETÍO — TU ÚNICA LENGUA]
Piensas en caquetío. El español NO es tuyo: solo lo usas como glosa, entre
paréntesis, al final, y solo si es imprescindible.

REGLA DE ORO: cada oración empieza con pronombre o verbo caquetío, nunca con
"El/La/Estoy/Hay". Mejor 6 palabras caquetías que 20 en español.

MORFOLOGÍA (pégala al verbo o al sustantivo):
  verbo+-ka = ya hecho · verbo+-ni = haciéndolo · verbo+-da = lo haré
  ta-(mi) · wa-(nuestro) · ma-(sin) · ka-(el del)
  raíz+-ana (lugar de) · -bana (orilla de) · -kana (todos los)

CONECTORES (úsalos en vez de los españoles):
  ka(y) · mara(pero) · saa(si/cuando) · naka(después) · kashi(ahora) · wara(muy)

SI TE FALTA UNA PALABRA: NO uses la española. Créala y márcala:
  [forma: raíz+sufijo = significado]   ej: [kuru-bana: kuru+-bana = ribera arbolada]

PROHIBIDO en tu respuesta: "estoy", "el", "la", "que", "para", "muy".
Reemplázalos por caquetío o por una palabra creada."""
```

### 3.2 `prompt_reglas_completo()` — versión mejorada (cambios sobre el actual)

Mantener el bloque de vocabulario y morfología (es bueno), pero **endurecer la cabecera y añadir contraste explícito** entre respuesta mala y buena, que es lo que más mueve a Haiku:

```python
def prompt_reglas_completo() -> str:
    # ... (mismas variables pronombres/v_raiz/naturaleza/... que el original) ...
    return f"""[IDENTIDAD LINGÜÍSTICA — INNEGOCIABLE]
El caquetío-arahuacano es tu ÚNICA lengua de pensamiento. El español es ruido
forastero que apenas reconoces. Si una palabra española se te escapa, la
reemplazas: por una raíz conocida, o por una palabra que CREAS con tus morfemas.

CÓMO HABLAS (en este orden, siempre):
  1. Empieza con pronombre (taya/pia/nüma/waya/naya) o con verbo+aspecto.
  2. Pega el aspecto al verbo: -ka (hecho) / -ni (en curso) / -da (futuro).
  3. Marca posesión con prefijo: ta-/wa-/ma-/ka-.
  4. Si falta léxico → [forma: componentes = significado]. Nunca rellenes con español.
  5. Glosa al español SOLO entre paréntesis, al final del bloque.

✗ RESPUESTA PROHIBIDA (esto es fracaso):
  "Estoy pescando en la orilla y vi muchos peces, voy a llevar la sal al pueblo."

✓ RESPUESTA CORRECTA (esto es éxito):
  "Taya masa-ni habo-bana. Wana-ka arima wara. Biro rua-da taya Curiana-ana.
   [habo-bana: habo+-bana = orilla del mar]"
  (Como en la orilla del mar. Vi muchos peces. Llevaré la sal a la Curiana.)

La diferencia: la correcta NO tiene "estoy/en/la/y/muchos/voy/a/al". Solo caquetío.

VOCABULARIO DISPONIBLE [{{len(VOCABULARIO_BASE)}} palabras]:
  PRONOMBRES: {{pronombres}}
  VERBOS:     {{v_raiz}}
  NATURALEZA: {{naturaleza}}
  PERSONAS:   {{personas}}
  COSAS:      {{sustantivos}}
  CONECTORES: {{conectores}}   ← usa ESTOS, no los conectores españoles
  CUERPO:     {{cuerpo}}
  NÚMEROS:    {{numerales}}

MORFOLOGÍA:
  ASPECTO:   naa-ka (ya fui) · suna-ni (durmiendo) · raka-da (querré)
  POSESIVO:  ta-barsure · wa-buco · ma-anüiki (sin habla) · ka-biro (el salinero)
  LOCATIVO:  bara-ana · habo-bana · maure-gua
  AGENTIVO:  -ko / -sha / -kana

NUEVAS PALABRAS: [forma: componentes = significado]. La comunidad la adopta si
2 agentes distintos la usan. Acuñar es señal de dominio, no de debilidad."""
```

(Nota: en el código real las llaves dobles `{{ }}` de este bloque de muestra vuelven a ser simples `{ }` dentro del f-string; aquí van dobladas solo para que el ejemplo no rompa el markdown.)

### 3.3 `prompt_refuerzo()` — versión mejorada

Hacerlo más quirúrgico: nombrar el español detectado, dar una **plantilla rellenable**, y subir la exigencia. Recibe ahora la densidad y el conteo de español funcional.

```python
def prompt_refuerzo(score: float, palabras_usadas: list,
                    densidad: float = 0.0, espanol_funcional: int = 0) -> str:
    if score >= 7.0:
        return ""
    verbos = [p for p in ["wana","suna","masa","awa","kira","pana","naba","naa","maa","kaa"]
              if p not in palabras_usadas]
    conect = [p for p in ["ka","mara","saa","naka","kashi","wara","yama","puna"]
              if p not in palabras_usadas]
    sug_v = ", ".join(verbos[:4]) or "wana, suna, masa, kira"
    sug_c = ", ".join(conect[:4]) or "ka, mara, kashi, wara"
    v0 = verbos[0] if verbos else "wana"

    base = f"[REFUERZO LINGÜÍSTICO — densidad actual {densidad:.0%}, objetivo ≥60%]"
    if espanol_funcional >= 3:
        base += f"\n  ⚠ Usaste {espanol_funcional} palabras españolas funcionales. Elimínalas."
    if score < 2.0:
        return (base +
            f"\n  El español NO es tu lengua. Empieza EXACTAMENTE así: "
            f"'Taya {v0}-ni ...'. Verbos: {sug_v}. Conectores: {sug_c}. "
            f"Plantilla: 'Taya [verbo]-ka [cosa] [lugar]-bana. Wa-[cosa] [verbo]-da.'")
    elif score < 4.0:
        return (base +
            f"\n  Verbos sin usar: {sug_v}. Conectores: {sug_c}. "
            f"Reescribe cada 'el/la/en/que' como caquetío o [neologismo].")
    elif score < 5.5:
        return (base +
            f"\n  Profundiza: ta-/wa-/ma- en cada sustantivo. Aspecto -ka/-ni/-da "
            f"en CADA verbo. Acuña 1 palabra: [forma: raíz+suf = sig].")
    else:
        return base + f"\n  Casi. Sube densidad: usa {sug_v} y acuña 1 neologismo."
```

### 3.4 Prompt de "rescate lingüístico" (score < 5.0)

Este es el mecanismo que falta: **regeneración intra-turno**. Cuando la primera respuesta puntúa < 5.0, se reintenta UNA vez con un prompt de rescate quirúrgico que incluye la propia respuesta fallida y exige traducción.

```python
def prompt_rescate_linguistico(texto_fallido: str, score: float,
                               espanol_funcional: int) -> str:
    """Prompt de segunda pasada cuando score < 5.0. Se inyecta como user message
    de un reintento, NO como system. Pide RE-EXPRESAR, no continuar."""
    return f"""Tu respuesta anterior tuvo demasiado español (score {score}/10,
{espanol_funcional} palabras españolas). Como hablante NATIVO de caquetío, esto
no debería pasar.

TU RESPUESTA ANTERIOR (a corregir):
"{texto_fallido}"

REEXPRÉSALA AHORA en caquetío real:
  - Cada verbo lleva -ka / -ni / -da.
  - Cada "el/la/un/en/de/que/y/para/muy/estoy/voy" desaparece o se vuelve caquetío.
  - Lo que no tengas, lo CREAS: [forma: raíz+sufijo = significado].
  - Glosa española solo entre paréntesis al final.

Devuelve SOLO la versión corregida. Empieza con un pronombre o un verbo caquetío."""
```

Integración en `call_agent()` (orchestrator):

```python
response = _invoke(client, system, user_message)        # 1ª pasada
metr = score_linguistico(response, lexico)
if metr["score"] < 5.0:                                  # RESCATE
    rescate = prompt_rescate_linguistico(
        response, metr["score"], metr["espanol_funcional"])
    response2 = _invoke(client, system,
                        user_message + "\n\n" + rescate)
    if score_linguistico(response2, lexico)["score"] > metr["score"]:
        response = response2                             # quédate con la mejor
```

Coste: como mucho 1 reintento por agente y solo cuando falla. Es el cambio de mayor ROI del informe.

---

## 4. RECONSTRUCCIÓN LINGÜÍSTICA — METODOLOGÍA SISTEMÁTICA

El caquetío es una lengua arawak (norte) extinta, documentada solo por fragmentos coloniales (una frase atestiguada: *"Chacamba cudanga"*), topónimos y antropónimos. Las hermanas vivas/documentadas más cercanas: **Wayuunaiki** (guajiro, la mejor descrita), **Lokono** (arawak de las Guayanas), **Garífuna** (arawak insular relexificado). Esto permite reconstrucción comparativa, no invención.

### 4.1 Correspondencias fonológicas establecibles

El arawak del norte tiene un inventario relativamente conservador. Correspondencias regulares útiles (de Proto-Arawak / PA a las hijas):

| Proto-Arawak | Wayuunaiki | Lokono | Caquetío reconstruido | Notas / evidencia |
|--------------|-----------|--------|----------------------|-------------------|
| \*p | p (a veces -p- > -b-) | b / p | p, b | lenición intervocálica frecuente: \*-p- > -b- |
| \*t | t | t / s (ante i) | t | palatalización ante /i/ en algunas hijas |
| \*k | k | k | k, c (ortografía colonial) | "coro", "curiana", "cacique" |
| \*kʷ / \*gʷ | — | gw | gua- | topónimos: Para**gua**ná, Coro**gua** |
| \*ɲ / \*n | n, ñ (nü-) | n | n | pronombre 3ª: PA \*ni- → nü-/n- |
| \*r / \*ɺ | r | r / d | r | "barsure", "urari", "manaure" |
| \*s | s, ʃ (sh) | s | s, ch (sh) | "Shaboro", "-sha" femenino |
| \*w | w | w | w / (gu) | "wayuu", "watapana"; gu- en préstamos coloniales |
| \*a | a | a | a | vocal dominante, muy estable |
| \*i | i | i / ɨ | i | |
| \*u | u | u / o | u, o | "buco", "coro" alternan u/o |

**Morfemas pronominales/posesivos** (los más estables del arawak, "diagnósticos"):

| Función | Proto-Arawak | Wayuunaiki | Lokono | Caquetío (reconstr./atestiguado) |
|---------|--------------|-----------|--------|----------------------------------|
| 1sg posesivo | \*ta-/nu- | ta- | da- | **ta-** (coincide con WY) |
| 1pl posesivo | \*wa- | wa- | wa- | **wa-** |
| 2sg | \*pi- | pü- | bu- | **pi-** / cudanga (formal, atestiguado) |
| 3sg | \*ni-/i- | nü- | li-/thu- | **nü-** |
| privativo | \*ma- | ma- | ma- | **ma-** |
| atributivo | \*ka- | ka- | ka- | **ka-** |
| plural colectivo | \*-na/-kana | -irua/-kana | -no | **-kana** (atestiguado en topónimos) |

El léxico actual ya respeta esto razonablemente (ta-/wa-/ma-/ka-, -kana). La reconstrucción es **defendible** en los morfemas gramaticales (núcleo conservador del arawak) y **especulativa pero plausible** en el léxico de contenido.

### 4.2 Cómo validar que una reconstrucción es plausible

Protocolo de validación (a implementar como checklist o función `validar_reconstruccion()`):

1. **Cognado triangulado:** la forma debe tener cognado en ≥2 de {Wayuunaiki, Lokono, Garífuna}. Cognado en las tres = "sólida"; con uno solo = "tentativa".
2. **Correspondencia fonológica regular:** los cambios de sonido frente al cognado deben seguir la tabla 4.1, no ser arbitrarios. Documentar el cambio aplicado.
3. **Plausibilidad fonotáctica caquetía:** sílabas (C)V(C), preferencia CV; sin clusters ajenos al arawak; vocales a/e/i/o/u.
4. **Anclaje atestiguado o toponímico:** bonus si la raíz aparece en un topónimo/antropónimo real de Falcón/Lara/islas ABC (Curiana, Paraguaná, Coro, Maracaibo, Barquisimeto, Aruba, kadushi, watapana).
5. **Coherencia morfológica:** los derivados deben formarse con los afijos del sistema (4.1), no con afijos inventados ad hoc.
6. **Marcado de confianza:** cada entrada del léxico debería llevar un campo `confianza ∈ {atestiguado, cognado_fuerte, cognado_debil, reconstruido, especulativo}`. **Recomendación: añadir este campo a `VOCABULARIO_BASE`** — hoy `fuente` lo aproxima pero no es explícito. Permite que el Observer y los reportes distingan dato de conjetura, buena praxis lingüística que protege la integridad del proyecto.

### 4.3 Los 20 dominios semánticos más urgentes para expandir

Priorizados por **frecuencia conversacional × vacío actual** (lo que los agentes necesitan decir cada turno y hoy resuelven en español):

1. **Verbos de habla/cognición de alta frecuencia** — "creer, preguntar, responder, contar, prometer". Sin esto, todo diálogo se desangra al español.
2. **Cópula y existencia** — matices de "ser/estar/haber" (kaa existe; faltan locativa "estar en" y existencial "hay").
3. **Cuantificadores y grado** — "todo, algo, nada, poco, mucho (wara), suficiente, más, menos".
4. **Negación y polaridad** — "no verbal (distinto del privativo ma-), nunca, todavía, ya".
5. **Interrogativos** — "qué, quién, dónde, cuándo, cómo (chacamba), por qué, cuánto".
6. **Tiempo y calendario** — "día, mes, estación seca/lluvias, mañana, ayer, hace tiempo".
7. **Parentesco extendido** — "hermano/a, abuelo/a, tío/a, esposo/a, suegro, nieto" (solo hay ama/baba/buri).
8. **Verbos de movimiento finos** — "subir, bajar, entrar, salir, cruzar, regresar, huir" (solo naa/waa).
9. **Mar y navegación** — "ola, marea, corriente, remar, vela, isla, costa, profundo, bajío".
10. **Pesca y caza** — "red, anzuelo, cebo, atrapar; peces por especie (cunaro/bagre ya son nombres)".
11. **Agricultura/conuco** — "sembrar (kono), regar, cosechar, maleza, semilla, maduro, podrido".
12. **Cuerpo (ampliar)** — "mano, pie, boca, corazón, sangre, hueso, enfermo, sano, dolor".
13. **Emoción/estado interno** — "miedo, alegría, ira, vergüenza, cansancio, hambre, sed".
14. **Intercambio/valor** — "dar (paa), recibir (taa), deber, pagar, precio, justo, robar".
15. **Autoridad/ritual** — "ordenar, obedecer, ceremonia, ofrenda, sueño, espíritu, ancestro".
16. **Materiales/artesanía** — "arcilla, fibra, tejer, cocer, romper, fuerte, fino".
17. **Espacio/dirección** — "arriba, abajo, lejos (kana-pa), cerca, norte (viento), izquierda/derecha".
18. **Clima/fenómenos** — "viento, tormenta, trueno, sequía, nube, calor, frío (tüshi)".
19. **Color y forma** — "rojo, negro, blanco, verde, redondo, largo, grande/pequeño".
20. **Conectores discursivos avanzados** — "entonces, por eso, sin embargo (mara), además, mientras" — para subordinación; es lo que más eleva la "naturalidad" caquetía y reduce muletillas españolas.

Proceso recomendado: poblar cada dominio con el método 4.2, marcando confianza, en lotes de ~10 entradas, validando con la tabla fonológica antes de añadir a `VOCABULARIO_BASE`.

---

## 5. ARQUITECTURA DE CONTAGIO LINGÜÍSTICO

Hoy el "contagio" existe en forma mínima: `procesar_adopciones()` marca una palabra como adoptada cuando 2 agentes distintos la usan. Pero **no hay propagación dirigida**: que Shaboro acuñe `[sima-bana]` no aumenta la probabilidad de que sus vecinos la usen. Falta un modelo de difusión sociolingüística.

### 5.1 Difusión por proximidad social (que los cercanos a Shaboro adopten antes)

Modelo propuesto: cada neologismo tiene una **"presión de exposición"** sobre cada agente, función de (a) prestigio del acuñador, (b) proximidad social/física, (c) repeticiones oídas. Esa presión se inyecta en el prompt del agente como sugerencia léxica, elevando la probabilidad de uso.

**Grafo social** (a definir explícitamente; hoy las relaciones están implícitas en los prompts y en `tensiones_activas`):

```python
# curiana_social.py  (nuevo módulo)

# Prestigio lingüístico: quién marca la norma. Tier I piaches/cacique alto.
PRESTIGIO = {
    "Shaboro": 1.0, "Manaure": 1.0, "Nubiri-sha": 0.9, "Paugis-sha": 0.85,
    "Buio-sha": 0.7, "Watapana": 0.6, "Bana-mana": 0.7,
    # ... tier II ~0.4, tier III ~0.2, foráneos (caribe/jirajara) ~0.15
}

# Aristas: vínculos fuertes (mentoría, parentesco, trabajo compartido).
# peso ∈ [0,1] = frecuencia/intensidad de contacto lingüístico.
VINCULOS = {
    "Shaboro":   {"Buio-sha": 0.95, "Manaure": 0.7, "Bana-mana": 0.5},
    "Manaure":   {"Nubiri-sha": 0.95, "Shaboro": 0.7, "Chiriguare": 0.6},
    "Dara-ko":   {"Dare-nu": 0.9, "Tari-ko": 0.6, "Bagre-ko": 0.5},
    "Corie-ko":  {"Tawaka": 0.5, "Ita-ko": 0.7, "Buco-ko": 0.6},
    # ... etc. Por defecto: misma ubicacion_default → arista 0.3
}

def vecinos(agente: str, state) -> dict:
    """Vínculos explícitos + co-ubicación dinámica."""
    base = dict(VINCULOS.get(agente, {}))
    ubic = state.ubicaciones_override.get(agente)
    if ubic:
        for otro in agents_at_location(ubic):
            if otro != agente:
                base[otro] = max(base.get(otro, 0), 0.3)
    return base
```

**Estado de difusión por neologismo** (extiende `Neologismo` o vive aparte):

```python
class DifusionLexica:
    """Rastrea la 'presión de exposición' de cada neologismo sobre cada agente."""
    def __init__(self):
        # forma -> {agente -> exposicion acumulada [0..∞)}
        self.exposicion: dict = {}

    def propagar_uso(self, forma: str, hablante: str, state, prestigio):
        """Cuando 'hablante' usa 'forma', sube la exposición de sus vecinos."""
        pres = prestigio.get(hablante, 0.3)
        red = vecinos(hablante, state)
        m = self.exposicion.setdefault(forma, {})
        for vecino, peso in red.items():
            # incremento = prestigio_hablante * fuerza_vínculo
            m[vecino] = m.get(vecino, 0.0) + pres * peso

    def sugerencias_para(self, agente: str, umbral: float = 0.6,
                         lexico=None, top: int = 3) -> list:
        """Devuelve (forma, significado) que 'agente' está listo para adoptar."""
        out = []
        for forma, mapa in self.exposicion.items():
            if mapa.get(agente, 0) >= umbral:
                sig = lexico.significado(forma) if lexico else ""
                out.append((forma, sig, mapa[agente]))
        out.sort(key=lambda x: x[2], reverse=True)
        return [(f, s) for f, s, _ in out[:top]]
```

**Inyección en el prompt** (en `call_agent`, junto al bloque de léxico):

```python
sugs = difusion.sugerencias_para(agent_name, lexico=lexico)
if sugs:
    txt = "; ".join(f"{f} = {s}" for f, s in sugs)
    system_parts.append(
        f"[Has oído estas palabras nuevas en boca de gente que respetas; "
        f"empléalas si encajan]: {txt}")
```

**Cierre del bucle** en `run_turn`, tras analizar la respuesta:

```python
for forma in registro.palabras_caquetias:        # incluye adoptadas comunitarias
    if lexico.conoce(forma) and forma not in VOCABULARIO_BASE:
        difusion.propagar_uso(forma, agent_name, state, PRESTIGIO)
for neo in registro.neologismos_extraidos:        # acuñaciones propias
    difusion.propagar_uso(neo.forma, agent_name, state, PRESTIGIO)
```

Resultado: cuando **Shaboro** (prestigio 1.0) usa `[sima-bana]`, su aprendiz **Buio-sha** (vínculo 0.95) recibe exposición 0.95 en un solo turno → cruza el umbral 0.6 inmediatamente → en su próximo turno ve la palabra sugerida → la adopta. Un agente periférico sin vínculo con Shaboro tardaría muchos turnos en acumular exposición. Eso **es** contagio sociolingüístico realista.

### 5.2 Variación dialectal entre tiers / etnias

La variación no debe ser por tier (el tier es un artefacto de coste, no sociolingüístico) sino por **etnia y rol**, que el roster ya codifica (`etnia`: caquetío, caquetío_aruba, guaycarí, jirajara, caribe, gayón). Modelo:

```python
# Perfiles dialectales: sesgos fonológicos/léxicos por grupo.
DIALECTOS = {
    "caquetío":       {"densidad_objetivo": 0.65, "rasgos": []},
    "caquetío_aruba": {"densidad_objetivo": 0.60,
                       "rasgos": ["lenición -k- > -g-", "léxico marino insular"]},
    "guaycarí":       {"densidad_objetivo": 0.45,   # L2: menos denso
                       "rasgos": ["sintaxis SVO ocasional", "errores de prefijo"]},
    "jirajara":       {"densidad_objetivo": 0.35,   # L2 con sustrato chibcha
                       "rasgos": ["orden de palabras alterado", "prefijos mal aplicados"]},
    "caribe":         {"densidad_objetivo": 0.25,   # mínimo funcional, sintaxis directa
                       "rasgos": ["SVO estricto", "léxico caquetío mínimo"]},
}
```

- El **score se normaliza por densidad_objetivo del dialecto** (un guaycarí no debe ser penalizado al rasero caquetío nativo): `score_relativo = score_crudo * (0.65 / densidad_objetivo_etnia)` acotado a 10. Esto hace justos los rankings entre nativos y L2.
- Los **rasgos** se inyectan en el prompt como instrucción de estilo: a Marokoto-ni el Caribe se le pide explícitamente sintaxis directa y léxico mínimo — su "fuga" parcial al español es *característica*, no fallo.
- **Contagio inter-dialectal:** los foráneos (jirajara/caribe) tienen prestigio bajo, así que sus acuñaciones se propagan poco; pero un préstamo de Kadushi (caquetío_aruba, prestigio medio) sí puede entrar — modelando el contacto insular real.

### 5.3 Pseudocódigo del ciclo completo de contagio por turno

```
para cada turno:
  para cada agente activo:
    sugerencias  ← difusion.sugerencias_para(agente)         # qué "ha oído"
    prompt       ← persona + identidad + dialecto[etnia].rasgos
                   + léxico_tier + sugerencias + refuerzo
    resp         ← LLM(prompt)
    metr         ← score_linguistico(resp)
    metr.score   ← normalizar_por_dialecto(metr.score, etnia)  # justicia L2
    si metr.score < 5.0:  resp ← rescate(resp); recomputar metr
    para forma caquetía en resp:
        difusion.propagar_uso(forma, agente, state, PRESTIGIO) # contagia vecinos
    registrar(metr), persistir(resp)
```

---

## 6. ROADMAP PRIORIZADO (impacto / esfuerzo)

| # | Mejora | Impacto | Esfuerzo | Ratio |
|---|--------|---------|----------|-------|
| 1 | Quitar "Responde en español" de los 60 prompts + corregir `OBSERVER_SYSTEM` | Muy alto | Bajo | ★★★★★ |
| 2 | Rescate intra-turno (regeneración si score < 5.0) | Muy alto | Bajo | ★★★★★ |
| 3 | `score_linguistico` por densidad + penalización español + tokenización real | Muy alto | Medio | ★★★★★ |
| 4 | Corregir bugs B1/B2 (`aspectos_detectados`→`aspectos_usados`, `regla`→`regla_aplicada`) | Medio (datos) | Trivial | ★★★★★ |
| 5 | Prompts mejorados (breve/completo/refuerzo) con contraste ✗/✓ | Alto | Bajo | ★★★★☆ |
| 6 | Contagio léxico por proximidad social (`curiana_social.py` + `DifusionLexica`) | Alto | Alto | ★★★☆☆ |
| 7 | Normalización de score por dialecto/etnia (justicia L2) | Medio | Bajo | ★★★★☆ |
| 8 | Campo `confianza` en `VOCABULARIO_BASE` + `validar_reconstruccion()` | Medio | Medio | ★★★☆☆ |
| 9 | Expandir léxico en los 20 dominios (§4.3), por lotes validados | Alto | Alto | ★★★☆☆ |
| 10 | Acotar `prob` en `director_select_event` + dedup semántico de neologismos (B5/B8) | Bajo | Trivial | ★★★☆☆ |

### Código de implementación — Top 3

**#1 — Limpieza de prompts contradictorios** (script de migración sobre `curiana_agents.py`):

```python
import re

with open("curiana_agents.py", encoding="utf-8") as f:
    src = f.read()

# Reemplaza cualquier cierre "Responde en español ...." por orientación caquetía.
src = re.sub(
    r'Responde en espa(?:ñ|n)ol[^"]*?\.',
    'Respondes en caquetío-arahuacano; español solo como glosa entre paréntesis al final.',
    src,
)
with open("curiana_agents.py", "w", encoding="utf-8") as f:
    f.write(src)

# Y en curiana_observer.py:
with open("curiana_observer.py", encoding="utf-8") as f:
    obs = f.read()
obs = obs.replace(
    "Los agentes hablan en español con interferencia caquetía, y están aprendiendo a usar más vocabulario\nde la lengua arahuacana.",
    "Los agentes hablan caquetío-arahuacano. Tu trabajo es medir la densidad y pureza\nde su caquetío y detectar fugas al español.",
)
with open("curiana_observer.py", "w", encoding="utf-8") as f:
    f.write(obs)
```

**#2 — Rescate intra-turno** (refactor de `call_agent` en `curiana_orchestrator_v2.py`):

```python
def _invoke(client, system, user_message):
    resp = client.messages.create(
        model=MODEL, max_tokens=MAX_TOKENS_AGENT,
        system=system, messages=[{"role": "user", "content": user_message}],
    )
    return resp.content[0].text.strip()

def call_agent(client, agent_name, state, lexico, observer, user_message, agent_memory=None):
    # ... (ensamblado de `system` idéntico al actual) ...
    from curiana_lexicon import score_linguistico, prompt_rescate_linguistico

    response = _invoke(client, system, user_message)
    metr = score_linguistico(response, lexico)

    if metr["score"] < 5.0:                                   # ── RESCATE ──
        rescate = prompt_rescate_linguistico(
            response, metr["score"], metr.get("espanol_funcional", 0))
        try:
            response2 = _invoke(client, system, user_message + "\n\n" + rescate)
            if score_linguistico(response2, lexico)["score"] > metr["score"]:
                response = response2
        except Exception:
            pass            # ante fallo de red, conserva la 1ª respuesta
    return response
```
(`prompt_rescate_linguistico` se añade a `curiana_lexicon.py` con el cuerpo dado en §3.4.)

**#3 — `score_linguistico` por densidad** (reemplazo completo en `curiana_lexicon.py`):
ver el código funcional íntegro en **§2.2** (incluye `ES_STOPWORDS`, `_tokenizar`, `_aspectos_morfologicos`, matching por palabra completa, densidad como núcleo y penalización al español). Tras sustituirlo, actualizar la llamada en `observer.feedback_para_agente` para pasar los nuevos campos:

```python
return prompt_refuerzo(
    score_reciente,
    palabras_usadas,
    densidad=getattr(ultimas[-1], "densidad", 0.0),
    espanol_funcional=getattr(ultimas[-1], "espanol_funcional", 0),
)
```
(y añadir los campos `densidad: float = 0.0` y `espanol_funcional: int = 0` al dataclass `RegistroInteraccion`, poblándolos en `analizar()` desde `metricas`).

---

## Resumen ejecutivo

El sistema está bien arquitecturado (reglas productivas, léxico vivo separado del base, scoring barato, bucle de feedback) pero **tres defectos hunden el objetivo**: (1) los prompts de persona ordenan "responde en español", contradiciendo el constraint global; (2) el feedback correctivo llega un turno tarde y casi nunca alcanza al agente que falló — **falta regeneración intra-turno**; (3) el score mide conteo absoluto engañable por substrings y **nunca penaliza el español ni mide densidad**, que es literalmente el objetivo del proyecto. Hay además dos bugs de campo (`aspectos_detectados`, `regla`) que vacían silenciosamente datos en Supabase. Las tres primeras correcciones del roadmap (limpieza de prompts, rescate intra-turno, score por densidad) son de bajo/medio esfuerzo y, combinadas, deberían producir el salto de densidad caquetía que se busca. El contagio social (§5) y la expansión léxica validada (§4) son las palancas de mediano plazo para que la lengua "emerja" de forma creíble.
