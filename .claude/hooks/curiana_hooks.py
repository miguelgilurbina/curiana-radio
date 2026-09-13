#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Hooks de proyecto-linguistico-caquetío — instalados el 2026-09-13 (Miguel: «instalemos los hooks»).
Diseño, razones y descartes: .claude/skills/HOOKS_PROPUESTOS.md.

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
