# Corpus cultural — Curiana

Datos culturales estructurados en YAML, complementarios a `CULTURA_CAQUETIA.md` (la guía narrativa en
prosa). Producidos por el programa de investigación "corpus cultural" (4 sesiones temáticas). Esta
carpeta es **datos de propuesta**: no se consume todavía desde ningún script de la simulación; es
material para que Miguel revise, vete o apruebe antes de integrarlo a prompts o mecánica.

## Índice de archivos

| Archivo | Sesión | Contenido |
|---|---|---|
| `parentesco.yaml` | 1/4 — Familia | Hechos culturales sobre parentesco, matrilinealidad, matrimonio, sucesión, terminología |
| `genealogia.yaml` | 1/4 — Familia | Propuesta de árbol genealógico para los 60 agentes + personas de fondo |

*(Las sesiones 2-4 del programa añadirán sus propios archivos aquí — no reescribir este índice, añadir
filas.)*

## Esquema de `parentesco.yaml` (y de los corpus temáticos futuros)

Cada entrada es un hecho cultural discreto, etiquetado con **una sola** fuente de las cuatro
posibles. Nunca mezclar categorías en una misma entrada; en caso de duda, degradar a la etiqueta más
débil.

```yaml
- id: parentesco-001
  contenido: >
    El hecho cultural, 1-4 frases.
  fuente: atestiguado | reconstruido | retro-abstraido | hipotetico
  referencia: "Oliver 1989, cap. 3, p. 268" / "analogía wayuu: Jahn 1927, p. 172" / "intuición local (Paraguaná)"
  dominios: [parentesco]
  agentes_relacionados: [Nubiri-sha, Chiri-ko]
  implicacion_simulacion: >
    Cómo debería reflejarse en prompts o mecánica (opcional).
```

### Las cuatro etiquetas de `fuente`

- **`atestiguado`** — citable a una crónica o trabajo académico concreto, con página/capítulo. El nivel
  más fuerte.
- **`reconstruido`** — inferido por método comparativo desde un pueblo arahuaco hermano (wayuu, lokono,
  taíno), con la comparanda y su fuente citadas en `referencia`.
- **`retro-abstraido`** — abstraído de una tradición viva posterior (espiritismo venezolano, cultura
  popular falconiana) o de intuición local informada, no de la etnohistoria precolonial directa.
- **`hipotetico`** — licencia narrativa plausible, sin respaldo documental ni comparativo directo.
  El nivel más débil; úsese cuando ninguna de las tres anteriores aplica limpiamente.

## Esquema de `genealogia.yaml`

Un registro por cada uno de los 60 agentes de `curiana_agents.py` (no se modifica ese archivo), más
las personas de fondo mencionadas que no son agentes (marcadas `fondo: true`, con nombre propio
inventado para esta propuesta).

```yaml
Nombre-del-agente:
  madre: "Nombre de la madre (o null si no se propone)"
  linaje: "Nombre del linaje materno"
  conyuge: "Nombre del cónyuge (o null)"
  relaciones_atestiguadas_en_descripcion:
    - "Relación ya implícita en curiana_agents.py, con la cita exacta o casi exacta"
  relaciones_propuestas:
    - "Relación nueva propuesta por esta sesión, para que Miguel revise/vete"

Nombre-de-persona-de-fondo:
  fondo: true
  descripcion: "Quién es y por qué se propone"
  relaciones_propuestas:
    - "..."
```

## Advertencia del repo

Nunca escribir API keys, tokens ni secretos en archivos de este proyecto — ni siquiera en archivos
gitignored — porque el proyecto sincroniza a OneDrive.
