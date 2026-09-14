# Hooks propuestos — proyecto lingüístico caquetío

> **INSTALADOS el 2026-09-13** (Miguel: «instalemos los hooks»), tal cual se
> describen abajo: `.claude/settings.json` + `.claude/hooks/curiana_hooks.py`.
> Pipe-test de los cinco modos en verde, y el hook de Bash probado en vivo. Este
> documento queda como el diseño: por qué cada hook, y qué se descartó.

Miguel, 2026-09-12: *«podríamos tener distintas skills para distintos procesos
[…] o no sé si serían hooks, para seguir mejorando el harness»*. Las skills
cubren lo que requiere juicio (`leer-fuente`, `fusionar-propuesta`,
`cerrar-sesion`). Un hook sirve para lo contrario: lo que **no puede depender de
que alguien se acuerde** y se puede comprobar con un script. Es el principio de
`proyecto-linguistico-caquetío/1-plan/HARNESS.md`.

## La tensión con HARNESS.md, dicha primero

`HARNESS.md` dice: *«Nada de hooks que bloqueen. […] hay estados intermedios
legítimos (minar una fuente rompe el tablero hasta regenerarlo). Los guardianes
se corren; no vigilan.»* Esta propuesta lo respeta así:

- **Sólo bloquea donde no hay estado intermedio legítimo.** Nunca hace falta
  editar a mano un fichero generado: los generadores escriben desde Python, no
  con la herramienta Edit, así que el bloqueo no les estorba. Y `git add -A`
  tiene siempre la alternativa de añadir por ruta.
- **Todo lo demás avisa y no bloquea.** Los guardianes corren **después** del
  commit y le dicen a Claude lo que salió en rojo, sin impedir nada.
- **No hay hook en `Stop`.** Se dispara al final de cada turno, y correr ahí
  guardianes o revisar el scratchpad es exactamente el incordio que HARNESS.md
  describe. El cierre es la skill `cerrar-sesion`, que se invoca cuando toca.

## Los cinco hooks

| # | Evento · matcher | Qué hace | ¿Bloquea? | El error real que evita |
|---|---|---|---|---|
| 1 | `PreToolUse` · `Edit\|Write` | Rechaza editar a mano un fichero generado, y dice cómo se cambia | **sí** (exit 2) | Dos commits (2026-08-30/31) editaron `2-lengua/toponimos.yaml` directamente, y la regeneración siguiente deshizo 25 entradas. `lexicon_achagua.py` tiene la misma trampa: se corrige el YAML |
| 2 | `PreToolUse` · `Bash` | Rechaza `git add -A` / `git add .`, y escribir por shell (`>`, `>>`, `tee`, `sed -i`) en un generado | **sí** (exit 2) | `git add -A` desde la raíz metió dos veces `design_handoff_marca_e_intro` (`67a0f53`, `65a14c1`). La parte de shell cierra el agujero del hook 1: el modo automático escribe con Bash, no con Edit |
| 3 | `PostToolUse` · `Bash` | Si `generar_tablero.py` corrió sin `--gh` (y sin `--stdout`/`--check`), avisa | no | Sin red, el gate salió 3/9 en vez de 6/9 (`051c746`), 3/9 en vez de 7/9 (`09545d8`), y otra vez el 2026-09-13 |
| 4 | `PostToolUse` · `Bash` | Tras un `git commit` que toca `proyecto-linguistico-caquetío/`, corre `guardianes.py --rapido --silencio`; si sale rojo, lo dice | no | Que un rojo pase inadvertido a la siguiente sesión. Ejemplo: la bibliografía sin regenerar tras el índice de Neira y Ribero, que costó el commit `5da70ba` |
| 5 | `PostToolUse` · `Bash` | Tras `6-fusion/scripts/{fusionar,sanear,aplicar,generar_lexicon,tainismos}_*.py` (sin `--dry-run`), recuerda la secuencia de cierre | no | El fallo del nivel C estuvo un día escrito y sin aplicar, y la fase 1 de D11 dejó el tablero diciendo «sin fusionar» lo que ya estaba dentro (`7f9a1ba`) |

## Lo que va en `.claude/settings.json`

El directorio del proyecto para Claude Code es `Curiana Radio/` (donde vive
`.claude/`). El script iría en `.claude/hooks/curiana_hooks.py`. La ruta lleva un
espacio y el proyecto una `í`: **siempre entre comillas**.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/curiana_hooks.py\" generado" }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/curiana_hooks.py\" bash" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/curiana_hooks.py\" tablero" },
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/curiana_hooks.py\" commit", "timeout": 300 },
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/curiana_hooks.py\" post_fusion" }
        ]
      }
    ]
  }
}
```

`settings.json` y no `settings.local.json`: HARNESS.md (capa 4) quiere lo del
proyecto en el fichero compartido y lo personal en el local.

## El script

Probado el 2026-09-13 desde el scratchpad, con entradas JSON como las que manda
Claude Code (rutas de Windows con barras invertidas y `í` incluidas), en 10
casos. Bloquea `TABLERO.md` y `lexicon_achagua.py` por Edit, un `echo >>` a
`TABLERO.md` y `git add .`. Deja pasar `curiana_lexicon.py`, una `SKILL.md`,
`git add -p` por ruta y `generar_tablero.py --gh`. El modo `commit` corrió los
guardianes rápidos, que tardan unos 2 s. Una entrada vacía o mal formada sale
con 0.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Hooks propuestos para proyecto-linguistico-caquetío (PROPUESTA, no instalado).

Un solo script con cinco modos; cada entrada de settings.json lo llama con uno:

    generado     PreToolUse  Edit|Write   bloquea editar a mano un fichero generado
    bash         PreToolUse  Bash         bloquea `git add -A` y escribir por shell en un generado
    tablero      PostToolUse Bash         avisa si generar_tablero.py corrió sin --gh
    commit       PostToolUse Bash         guardianes --rapido tras un commit que toca el proyecto
    post_fusion  PostToolUse Bash         recuerda la secuencia de cierre tras un script de fusión

Bloquear = exit 2 con el motivo en stderr. Avisar = exit 0 con
hookSpecificOutput.additionalContext. Cualquier fallo interno del propio hook
sale con 0 y en silencio: un hook roto no debe parar el trabajo.
"""
import json
import os
import re
import subprocess
import sys

for _flujo in (sys.stdout, sys.stderr):          # la consola de Windows es cp1252
    try:
        _flujo.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

PROY = "proyecto-linguistico-caquetío"
RAIZ = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

# fichero generado (ruta dentro de PROY) -> cómo se regenera
GENERADOS = {
    "TABLERO.md": "python curiana_sim/generar_tablero.py --gh",
    "6-fusion/BANDEJA.md": "python curiana_sim/generar_bandeja.py",
    "1-plan/CRONICA.md": "python curiana_sim/generar_cronica.py",
    "6-fusion/TOPONIMOS_POR_FUENTE.md": "python curiana_sim/juntar_toponimos.py",
    "6-fusion/toponimos_por_fuente.yaml": "python curiana_sim/juntar_toponimos.py",
    "2-lengua/toponimos.yaml": "edita curiana_sim/lexicon_toponimos.py y corre migrar_toponimos.py",
    "4-fuentes/bibliografia.yaml": "edita el frontmatter de la nota en 4-fuentes/ y corre generar_bibliografia.py",
    "curiana_sim/lexicon_achagua.py": "corrige 6-fusion/achagua_neira_ribero_1762.yaml y corre 6-fusion/scripts/generar_lexicon_achagua.py",
    "curiana_sim/lexicon_zavala.py": "corre curiana_sim/minar_zavala_glosario.py",
    "curiana_sim/lexicon_a2.py": "corrige 6-fusion/tabla_a2_transcripcion.yaml y corre curiana_sim/minar_a2_swadesh.py",
    "curiana_sim/lexicon_perea.py": "corre curiana_sim/minar_perea.py",
}


def _entrada():
    crudo = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    return json.loads(crudo or "{}")


def _cmd(d):
    return (d.get("tool_input") or {}).get("command", "") or ""


def _bloquear(texto):
    sys.stderr.write(texto + "\n")
    sys.exit(2)


def _contexto(evento, texto):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": evento,
                                             "additionalContext": texto}},
                     ensure_ascii=False))


def _generado_de(ruta):
    ruta = ruta.replace("\\", "/")
    for rel, como in GENERADOS.items():
        if ruta.endswith(f"{PROY}/{rel}"):
            return rel, como
    return None, None


def generado(d):
    rel, como = _generado_de((d.get("tool_input") or {}).get("file_path", "") or "")
    if rel:
        _bloquear(f"`{rel}` es GENERADO y no se edita a mano: la próxima regeneración "
                  f"deshace el cambio (pasó con toponimos.yaml: 25 entradas perdidas). "
                  f"Cómo se cambia: {como}.")


def bash(d):
    cmd = _cmd(d)
    if re.search(r"\bgit\s+add\s+(-A\b|--all\b|\.(\s|$))", cmd):
        _bloquear("`git add -A` / `git add .` barrió dos veces una carpeta sin trackear "
                  "(design_handoff_marca_e_intro: commits 67a0f53 y 65a14c1). "
                  "Añade por ruta: git add <ruta> <ruta>…")
    for rel, como in GENERADOS.items():
        nombre = re.escape(rel.split("/")[-1])
        escritura = (rf"(>>?|\btee\s+(-a\s+)?)\s*[\"']?[^\s\"'|;&]*{nombre}"
                     rf"|\bsed\s+-i[^|;&]*{nombre}")
        if re.search(escritura, cmd):
            _bloquear(f"El comando escribe en `{rel}`, que es GENERADO. Cómo se cambia: {como}.")


def tablero(d):
    cmd = _cmd(d)
    if ("generar_tablero.py" in cmd and "--gh" not in cmd
            and not re.search(r"--(stdout|check)\b", cmd)):
        _contexto("PostToolUse",
                  "generar_tablero.py corrió SIN --gh: el panel de decisiones sale «no medido» "
                  "y el gate cuenta como abiertas las decisiones cerradas en GitHub (051c746, "
                  "09545d8, y otra vez el 2026-09-13). Vuelve a correrlo con --gh antes de "
                  "commitear TABLERO.md.")


def commit(d):
    cmd = _cmd(d)
    if not re.search(r"\bgit\b[^|;&]*\bcommit\b", cmd) or "--dry-run" in cmd:
        return
    tocados = subprocess.run(
        ["git", "-c", "core.quotepath=false", "diff", "--name-only", "HEAD~1", "HEAD"],
        cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    if PROY not in tocados:
        return
    proy = os.path.join(RAIZ, PROY)
    r = subprocess.run(
        [sys.executable, os.path.join(proy, "curiana_sim", "guardianes.py"), "--rapido", "--silencio"],
        cwd=proy, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=280,
        env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if r.returncode != 0:
        _contexto("PostToolUse",
                  "El commit ya está hecho, pero guardianes.py --rapido sale en ROJO:\n"
                  + (r.stdout + r.stderr)[-1500:]
                  + "\nArréglalo en un commit nuevo antes de seguir, o decláralo en el handoff "
                    "si es un estado intermedio legítimo (1-plan/HARNESS.md).")


def post_fusion(d):
    cmd = _cmd(d)
    m = re.search(r"6-fusion[/\\]scripts[/\\]((?:fusionar|sanear|aplicar|generar_lexicon|tainismos)_\w+)\.py", cmd)
    if m and "--dry-run" not in cmd:
        _contexto("PostToolUse",
                  f"Acaba de correr {m.group(1)}. Cierre de la fusión (skill fusionar-propuesta §10): "
                  "guardianes.py · generar_tablero.py --gh · generar_bandeja.py · "
                  "generar_bibliografia.py si entró una obra · y marcar la propuesta y la tanda como aplicadas.")


MODOS = {"generado": generado, "bash": bash, "tablero": tablero,
         "commit": commit, "post_fusion": post_fusion}

if __name__ == "__main__":
    try:
        MODOS[sys.argv[1]](_entrada())
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
```

## Detalles que se decidieron, y por qué

- **`git -c core.quotepath=false`** en el modo `commit`. Sin eso, git escribe la
  ruta como `proyecto-linguistico-caquet\303\255o` (se ve en cualquier
  `git show --stat` de este repo), y la comprobación de «¿toca el proyecto?»
  nunca acertaría.
- **Los guardianes en su modo `--rapido --silencio`**, que es para lo que
  existe: la cabecera de `guardianes.py` dice que sale con código ≠ 0 «para que
  se pueda colgar de un hook o de CI». Los tests completos quedan para
  `cerrar-sesion`.
- **La lista de generados sale de las cabeceras `generado_por` / `editar_a_mano:
  no` / «GENERADO … no se edita a mano», leídas el 2026-09-13.** Quedan fuera,
  a propósito:
  - `2-lengua/cognados.yaml` y `2-lengua/morfemas.yaml` declaran `generado_por`,
    pero hay commits de fusión que los tocan (`e1aa50f` modifica
    `cognados.yaml`). Hay que verificar si hoy se editan a mano antes de
    bloquearlos.
  - `6-fusion/achagua_neira_ribero_1762.yaml` lleva la cabecera del ensamblador,
    pero su cuerpo **es** la transcripción a mano. Sólo `meta.cobertura` es
    generada, y un hook por fichero no distingue secciones.
  - `6-fusion/lokono_perea_1942.yaml` y los demás YAML de propuesta generados
    por un minador: son cola, no canon, y regenerarlos es decisión del minador.
- **El modo `bash` es un filtro de texto, no un analizador de shell.** Atrapa
  `>`, `>>`, `tee` y `sed -i` hacia un generado. No atrapa un
  `python -c "open('TABLERO.md','w')…"`. Para `toponimos.yaml` sigue estando el
  test `test_el_canon_de_toponimos_es_lo_que_emite_el_migrador`, que es la red
  de verdad.
- **No hay hook para «anclar dentro de `VOCABULARIO_BASE`».** La trampa de
  `FUERA_DEL_HABLA` ocurre dentro de un script de Python, invisible para un
  hook. La defensa es la de `fusionar-propuesta` §3: medir el total de entradas
  activas antes y después.

## Antes de instalar, verificar

Contrastado con `https://code.claude.com/docs/en/hooks` el 2026-09-13:

- `matcher` compara con el **nombre de la herramienta** (`Edit|Write`, `Bash`).
- En `PreToolUse`, exit 2 **bloquea** la llamada y su stderr le llega a Claude.
- `$CLAUDE_PROJECT_DIR` está disponible.
- En Windows con Git Bash, el comando corre en `bash`.

Lo que no quedó del todo claro y hay que probar al instalar:

1. **Que `additionalContext` en `PostToolUse` le llegue a Claude** como se
   espera. Si no, la alternativa documentada es exit 2 con el mensaje en stderr.
2. **El campo `if`** (`"if": "Bash(git commit*)"`), que filtraría por comando
   sin arrancar Python en cada Bash. La doc lo describe para eventos de
   herramienta, pero no se probó aquí. Hoy el filtro va dentro del script, que
   es más lento pero seguro.
3. **Que cada hook falle una vez a propósito** antes de darlo por bueno, como
   pide HARNESS.md para los guardianes: editar `TABLERO.md` con Edit, correr
   `generar_tablero.py` sin `--gh`, y hacer un commit con un guardián roto
   adrede.

## Descartados

| Idea | Por qué no |
|---|---|
| Guardianes en `PreToolUse` de `git commit`, bloqueando | HARNESS.md: bloquearía los estados intermedios legítimos. El modo `commit` avisa después |
| Guardianes o revisión del scratchpad en `Stop` | Se dispara en cada turno; es ruido. Es trabajo de `cerrar-sesion` |
| Bloquear la edición manual de `curiana_lexicon.py` | Se edita a mano legítimamente (entradas sueltas como `catire`). Las fusiones grandes van por script |
| Hook que publique borradores en GitHub | Publicar necesita el visto bueno de Miguel (regla 10 y `fusionar-propuesta` §11); no se automatiza |
