# Diseño: Koiné Emergente — Maturana, Cynefin y el Emocionar

**Estado:** diseño + implementación en curso (rama `feat/koine-emergente`).
Espejo técnico de la página Notion *"Koiné Emergente — Maturana, Cynefin y el
Emocionar"* (hija del Marco Teórico). La página de Notion lleva el marco
teórico; este archivo lleva las estructuras de datos, las métricas y la
mecánica. Mantener ambos en consonancia.

> Relación con lo existente: el Marco Teórico (§1) define **cómo se reconstruye
> la forma** (método comparativo). Esto agrega un eje perpendicular: **cómo el
> uso converge en una norma**. No reemplaza nada; responde las preguntas
> abiertas §9 de Notion ("¿se puede medir el drift?" y "toponimia generativa").

---

## 1. El problema que resuelve

El análisis del run `2e729f3f` (30 turnos, 15 días) mostró que la lengua llega
a su equilibrio (92% caquetío) el **día 1** y se queda plana. No hay deriva.
Causa estructural, no de tuning:

1. **Sin variación** — los 48 agentes activos reciben la misma identidad y la
   misma muestra de léxico. La única variación es por etnia (gruesa, estática).
2. **Sin transmisión con memoria** — la memoria son 3 snippets de texto crudo;
   no acumula un perfil lingüístico que sesgue el futuro del agente.
3. **Sin retroalimentación que componga en el tiempo** — lo único que cruza el
   tiempo es "últimos 15 neologismos adoptados" + contagio, que converge y se
   congela (adopción con 2 agentes, sin competencia entre variantes).

Sin esos tres no hay motor de cambio acumulativo.

## 2. El objetivo: una koiné caquetía emergente

Formar, por convergencia, una **koiné** anclada en el caquetío atestiguado/
reconstruido — y luego usarla como lente para "leer" topónimos reales del
territorio (fase posterior, ver §8).

> **Una koiné es un *dominio consensual* en el sentido de Maturana**:
> coordinaciones recurrentes de conducta que se estabilizan entre seres que
> conviven. Ese es el marco teórico que vuelve legítimo el experimento.

### El arco: diverso → converge

Una koiné solo se forma —y solo es **visible/medible**— si hay variación
inicial que converja. Por eso el run debe empezar *diverso a propósito*:

```
DÍA 1: caquetío nuclear + guaycarí + jirajara + insular aruba, cada facción
        con su sesgo de habla  →  ALTA distancia idiolectal
   ↓   (innovación + contagio + prestigio + frecuencia + coordinación)
DÍA N: una norma compartida anclada en caquetío  →  BAJA distancia idiolectal
```

Consecuencia: **activar a los agentes foráneos/periféricos no es opcional** —
son los aportantes de la mezcla que después se asienta.

## 3. Los tres paradigmas → mecánica medible

| Paradigma | Qué aporta | Mecanismo medible |
|---|---|---|
| Maturana — lenguajear/coordinar | *por qué* converge | estímulos de coordinación; `EMOCIONAR` por agente |
| Maturana — dominio consensual | *qué es* la koiné | fijación de variantes; contracción de distancia idiolectal |
| Cynefin (galés: pertenencia a la tierra) | mente *emplazada* | paisaje nombrado; idiolecto de tierra; topónimos emergentes |
| Préstamos venezolanos (cunaro/guaranaro/saruro) | anclaje + validación | fonología koiné + set de validación contra dato real |

**Disciplina:** los paradigmas moldean **escena, identidad y emocionar**
(los inputs). Los agentes nunca *hablan de* autopoiesis ni de emociones — su
emocionar moldea *cómo* lenguajean. Las **métricas** (§7) son la espina
dorsal que mantiene el experimento honesto y falsable.

## 4. El emocionar sembrado (semilla de idiolecto)

No se inventan personalidades: se **extrae el emocionar ya latente** en los
`system_prompt` y se vuelve una palanca de datos. Ej. ya escrito hoy:
Manaure "formas completivas constantemente"; Dare-nu/Dara-ko "presente y
aspecto continuativo"; Shaboro "metáforas de animales y agua".

Estructura nueva (por agente, en `curiana_agents.py` o módulo aparte):

```python
EMOCIONAR["Manaure"] = {
    "disposicion":  "contención vigilante — la carga del que sostiene el cielo",
    "sesgo_lexico": ["jerarquia", "cosmos", "biro"],   # dominios que alcanza primero
    "sesgo_morfo":  {"aspecto": "completivo", "afijos": ["-ka"]},
    "registro":     {"frase": "corta/definitiva", "metafora": "baja"},
}
```

Dos efectos (los dos importan):

1. **Sesga el prompt** — una línea `[Tu emocionar]: ...` reemplaza al genérico.
2. **Pre-carga el `Counter` de idiolecto** — cada agente arranca con SUS formas
   favoritas ya "entrenadas" → distancia idiolectal alta el día 1. Sin esta
   pre-carga, todos arrancan iguales y "convergencia" no significa nada.

Cynefin se suma como `sesgo_lexico` enraizado en lugar (topónimos y
palabras-de-tierra del trozo del Golfete de cada agente).

## 5. Memoria e idiolecto (estado nuevo por run)

### `IdiolectoAgente` (por agente)
- `frecuencias: Counter[str]` — formas que el agente produjo (entrenchment).
  Se actualiza cada turno desde `registro.palabras_caquetias` + neologismos.
  Se **pre-carga** con el `sesgo_lexico` del emocionar.
- `acunaciones: set[str]` — formas que él inventó.
- `adopciones: set[str]` — formas que tomó de otros.

### Inyección "tu manera de hablar"
Reemplaza los 3 snippets de texto por un bloque compacto derivado del perfil:
*"sueles decir X, Y; acuñaste Z; tu aspecto es -ka"*. Esto cierra el lazo de
entrenchment: lo que dijiste, lo repetís → deriva individual que compone.

> Consonancia con `CANON_TIERRA.md`: el "segundo compartimento de memoria que no
> expira" que pediste para los ritos **es** este `IdiolectoAgente`. Lo que se
> transmite en un rito y arraiga en la memoria larga es lo que se fija en la
> koiné.

## 6. El motor de convergencia: selección hasta fijación

### Campo de frecuencia comunitario (`CampoLexico`, por run)
- `Counter[str]` global de todas las formas usadas.
- `muestra_caquetio_dinamica()` pasa de muestreo aleatorio a **ponderado por
  frecuencia** (rich-get-richer → curvas S de adopción).
- **Decaimiento**: formas no usadas en N turnos pierden peso → recambio léxico
  (deja que cosas mueran).

### Competencia y fijación de variantes  ✅ IMPLEMENTADO (`CompetenciaLexica`)

> **Hallazgo (run 9bb920eb):** la competencia NO ocurre sola. Agrupar por glosa
> dio CERO competencia — cada agente acuña para un concepto distinto (46
> neologismos → 46 conceptos). Una koiné nace de una **necesidad referencial
> compartida**: algo nuevo que VARIOS deben nombrar. Por eso la fijación vino en
> dos piezas, no una.

**(1) Inductor — eventos de nombramiento.** `REFERENTES_NOVEDOSOS` (10 cosas sin
palabra caquetía: cuentas de vidrio, cometa, eclipse, metal amarillo, marea
roja, bestia varada…). Cada ~4 turnos el orquestador presenta un referente a
TODOS los agentes activos con el mismo `concepto_id` → acuñan formas rivales
para el MISMO concepto.

**(2) `CompetenciaLexica` — resolución.**
- Cada variante acumula soporte = `frecuencia × prestigio` de quienes la usan
  (`proponer` al acuñar, `registrar_uso` al reusar; los agentes de prestigio
  anclan la norma).
- `prompt_competencias()` surface las competencias abiertas en el prompt →
  empuja a REUSAR una forma rival en vez de inventar otra (así una se impone).
- Una variante se **fija** cuando domina su concepto (≥55% del soporte, soporte
  mínimo). El conjunto de fijadas = el **diccionario koiné**, persistido en
  `koine_lexicon`.
- Validado (run dd1d0c9c): `cuentas_vidrio` → `kali-pica` fijada de 3 rivales.

### Guardarraíl (prerrequisito, no opcional)
Si se refuerza frecuencia sin filtrar, la koiné fija basura española
(`suave-bana-ni`) tan eficientemente como fija aciertos. La **compuerta de
calidad de neologismos** (quick-win #3) debe estar activa: rechazar raíces
no-caquetías y morfología inválida antes de que una forma pueda competir.

## 7. Medición — cómo probamos que la koiné se formó

Esto vuelve el resultado defendible en vez de anecdótico. Tabla nueva
`koine_metrics` (o vista) por run/día:

- **Distancia idiolectal media** entre agentes (coseno/Jaccard sobre vectores
  de frecuencia de formas). **Debe contraerse** en el tiempo → firma de la
  koineización. Si no se contrae, no hubo koiné.
- **Variantes por significado → 1** (tasa de fijación).
- **Curvas de frecuencia** de las formas ganadoras (forma de S esperada).
- **Supervivencia de neologismos** (nace → vive → muere / se fija).
- **Diccionario koiné extraíble** al cierre del run (forma fijada por glosa +
  afijos ganadores + tendencias fonológicas).

## 8. Fase posterior: topónimos (no en este PR)

La koiné da: (a) inventario fonológico + reglas de sonido, (b) set de morfemas
ganadores (-bana, -ana, -ko...), (c) léxico preferido. Con eso se "lee" un
corpus de topónimos reales del territorio.

- **Set de validación ya existe** en Notion (*Venezolanismos de Origen
  Indígena* §I y §VI): `cunaro/guaranaro/saruro` confirman la terminación
  -aro/-uro; los morfemas -gua/-bana/-cuy ya están documentados.
- **Honestidad epistémica** (consonancia con el Marco Epistemológico): el
  parsing koiné de un topónimo es *"así lo rendiría la koiné de la Curiana"*,
  una **lente construida**, NO "la etimología real". Etiquetar como tal. Los
  topónimos son reales; la lectura koiné es una construcción.
- ⚠️ Verificar la familia de cada préstamo antes de usarlo como evidencia
  caquetía: muchos venezolanismos son Caribe/Taíno (p.ej. *tapara* suele darse
  como cumanagoto), no caquetío.

## 9. Orden de implementación

1. ✅ `EMOCIONAR` por agente + inyección en el prompt.
2. ✅ `IdiolectoAgente` + `CampoLexico` (estado por run) + pre-carga desde el emocionar.
3. ✅ Inyección "tu manera de hablar" (reemplaza los snippets).
4. ✅ Muestreo ponderado por frecuencia + decaimiento (`CampoLexico.pesos` →
   `muestra_caquetio_dinamica`, Efraimidis-Spirakis con base 1.0 para mantener
   exploración → rich-get-richer).
5. ✅ Competencia/fijación — vía eventos de nombramiento (no por glosa; ver §6).
6. ✅ Métricas (distancia idiolectal + fijación) + persistencia (`koine_metrics`,
   `koine_lexicon`).
7. ✅ Población constante de participantes en el loop (`PARTICIPANTES_KOINE`).
8. ✅ Compuerta de neologismos (fonotáctica: blocklist + marcadores + bigramas).

## 10. Referencias

- Maturana, H. & Varela, F. — *El árbol del conocimiento* (1984); Maturana,
  *Biología del lenguajear* y *Emociones y lenguaje en educación y política*.
- Cynefin (concepto cultural galés de pertenencia a la tierra/los ancestros);
  no confundir con el framework homónimo de Snowden.
- Documentos internos: Notion *Marco Teórico y Metodológico*, *Marco
  Epistemológico*, *Venezolanismos de Origen Indígena*; repo `CANON_TIERRA.md`,
  `CULTURA_CAQUETIA.md`, `ANALISIS_RUN_30T_2026-06-22.md`.
