#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — compilador y validador del corpus cultural
====================================================

El equivalente cultural de los tests del motor. Hasta hoy los YAML de
`3-mundo/corpus/` no los validaba nadie: nada comprobaba que las etiquetas
epistémicas fueran legales, que los `agentes_relacionados` existieran de verdad
en `curiana_agents.py`, ni que las referencias cruzadas entre hechos
resolvieran. 161 hechos sostenidos por la buena fe de quien los escribió.

Es la condición 4 del gate (`1-plan/PLAN_MAESTRO.md` §6.2) y la V2 del plan.

QUÉ VALIDA
----------
1. **Estructura** — campos obligatorios presentes y no vacíos, `id` con la
   forma `<dominio>-NNN`, `id` único en todo el corpus, y el dominio del `id`
   coincidiendo con el archivo que lo contiene.
2. **Etiquetas epistémicas** — `fuente` es una de las cinco del README, ni una
   más. Es la regla que sostiene toda la disciplina del proyecto: si
   `retro-abstraido` se cuela como `reconstruido`, el corpus miente sin que
   nadie lo note.
3. **`agentes_relacionados`** — cada nombre existe en el elenco activo
   (`curiana_agents.ALL_AGENTS`: la era 1 por defecto, la era 2 con
   `CURIANA_ELENCO=era2`). El corpus nombra a la gente como en la era 1 y es
   canon: **no se reescribe**. Se resuelve al leer, con el `ALIAS_ERA1` que el
   elenco activo expone (`agentes_de_hecho()` es la única puerta por la que un
   consumidor debe leer el campo). Un nombre de la era 1 que el elenco activo
   deja fuera es **aviso** (`agente-sin-equivalente`), no error: darle alias o
   declararlo persona de fondo es decisión de Miguel, y el informe lo lista con
   sus hechos. Si no existe pero sí está en `genealogia.yaml` como persona de
   fondo, también es aviso: son propuestas todavía sin veto, y el corpus las
   cita a propósito. Cualquier otro nombre es error — es un typo o un fantasma.
4. **Referencias cruzadas** — todo token `<dominio>-NNN` que aparezca en
   `contenido`, `referencia` o `implicacion_simulacion` tiene que resolver a un
   hecho real del corpus.
5. **Rutas citadas** — ninguna referencia puede apuntar a `curiana_sim/cultura/`,
   que es donde vivía el corpus antes del refactor del vault (2026-08-04) y ya
   no existe.
6. **Enganche con el motor** — `locacion` ∈ `curiana_state.LOCACIONES`,
   `palabra_lexicon` ∈ `curiana_lexicon.VOCABULARIO_BASE`. Son los dos puntos
   por donde el corpus toca el código, y por donde se romperá en silencio si
   alguien renombra una locación.
7. **`genealogia.yaml`** — esquema propio (un registro por persona): los
   linajes citados existen, y madres/cónyuges resuelven a alguien conocido.

QUÉ EMITE
---------
El YAML fusionado (`--fusionar`), para cuando la simulación consuma el corpus:
un solo documento con los 161 hechos normalizados, cada uno con su `archivo` y
`seccion` de origen, más la genealogía y un bloque `meta` con el censo por
etiqueta. Hoy nada lo consume todavía — igual que los YAML mismos, es material
de propuesta; pero el gate pide que exista y que **valide**.

Uso:
    python compilar_corpus.py                    # informe completo
    python compilar_corpus.py --check            # exit 1 si hay errores (CI)
    python compilar_corpus.py --fusionar out.yaml
    python compilar_corpus.py --json             # el informe en JSON
    python compilar_corpus.py --avisos           # incluye los avisos en --check

No modifica los YAML: valida y emite. Misma disciplina que los minadores.
"""

import argparse
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

import yaml

_AQUI = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(_AQUI, "..", "3-mundo", "corpus")

# Las cinco del README de `3-mundo/corpus/`. Una entrada lleva exactamente una.
ETIQUETAS_FUENTE = (
    "atestiguado",
    "reconstruido",
    "canon-simulacion",
    "retro-abstraido",
    "hipotetico",
)

# Campos que toda entrada del corpus debe traer, con contenido.
CAMPOS_OBLIGATORIOS = ("id", "contenido", "fuente", "referencia", "dominios",
                       "agentes_relacionados")

# `agentes_relacionados` puede estar vacío a propósito (hechos sin persona
# concreta detrás), así que no se exige contenido — solo que la clave exista.
CAMPOS_QUE_PUEDEN_IR_VACIOS = ("agentes_relacionados", "dominios")

# `genealogia.yaml` tiene esquema propio (un registro por persona, no un hecho
# con `fuente`/`referencia`), así que se valida aparte.
ARCHIVO_GENEALOGIA = "genealogia.yaml"

# Un token de referencia cruzada: `parentesco-034`, `geografia_politica-003`,
# `hueco-lex-001`, `creencia-010b`. El prefijo va en minúsculas (puede llevar
# guion bajo o guion interno), el número siempre a tres cifras, y admite un
# sufijo de una letra: es la convención con que el corpus intercala una entrada
# junto a la que ya existía sin renumerar las 30 siguientes.
RE_REFERENCIA = re.compile(r"\b([a-z][a-z_]*(?:-[a-z]+)*)-(\d{3})([a-z]?)\b")

# Espacios de nombres de `id` que no coinciden con el nombre del archivo. Hoy
# solo uno: `ecologia.yaml` guarda sus huecos léxicos en una sección aparte
# (`huecos_lexicos`) y los numera en su propia serie, porque no son hechos
# sobre el mundo sino ausencias en la lengua.
NAMESPACES_EXTRA = {
    "ecologia": {"hueco-lex"},
}

# La ruta donde vivía el corpus antes del refactor del vault del 2026-08-04.
RUTA_MUERTA = "curiana_sim/cultura/"

# Campos de texto libre donde pueden aparecer referencias cruzadas.
CAMPOS_TEXTO = ("contenido", "referencia", "implicacion_simulacion", "nota_abierta")


def _forzar_utf8() -> None:
    """La consola de Windows usa cp1252 y este informe imprime "─", "⚠", "í"…

    Se llama solo al ejecutarlo como script: reasignar sys.stdout al importarlo
    como módulo le rompería el stdout a quien lo importa.
    """
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


# ══════════════════════════════════════════════════════════════════════
# PROBLEMAS
# ══════════════════════════════════════════════════════════════════════

class Problema:
    """Un hallazgo de la validación.

    `nivel` es "error" (rompe el gate) o "aviso" (queda anotado). La distinción
    importa: el corpus tiene deuda deliberada — personas propuestas y sin veto
    de Miguel — y confundirla con un typo haría el validador inútil.
    """

    def __init__(self, nivel: str, codigo: str, donde: str, mensaje: str):
        self.nivel = nivel
        self.codigo = codigo
        self.donde = donde
        self.mensaje = mensaje

    def __repr__(self) -> str:
        return f"{self.nivel.upper()} [{self.codigo}] {self.donde}: {self.mensaje}"

    def como_dict(self) -> dict:
        return {"nivel": self.nivel, "codigo": self.codigo,
                "donde": self.donde, "mensaje": self.mensaje}


def _error(codigo, donde, mensaje):
    return Problema("error", codigo, donde, mensaje)


def _aviso(codigo, donde, mensaje):
    return Problema("aviso", codigo, donde, mensaje)


# ══════════════════════════════════════════════════════════════════════
# ELENCO
# ══════════════════════════════════════════════════════════════════════

class Elenco:
    """El elenco activo visto desde el corpus.

    `agentes` son los nombres que valen hoy; `alias`, la traducción de un
    nombre de la era 1 al del elenco activo (vacía en la era 1, donde los
    nombres son los suyos); `sin_equivalente`, los nombres de la era 1 que el
    elenco activo no tiene ni por alias. El corpus es canon y nombra a la
    gente como en la era 1: la resolución se hace aquí, al leer, nunca
    reescribiendo los YAML.
    """

    def __init__(self, agentes, alias=None, sin_equivalente=(), era="era1"):
        self.agentes = set(agentes)
        self.alias = dict(alias or {})
        self.sin_equivalente = set(sin_equivalente)
        self.era = era

    @classmethod
    def de(cls, agentes):
        """Un `Elenco` tal cual, o uno sin alias a partir de un set de nombres."""
        return agentes if isinstance(agentes, cls) else cls(agentes)

    def resolver(self, nombre: str) -> str:
        return self.alias.get(nombre, nombre)


def elenco_activo() -> Elenco:
    """El elenco que `curiana_agents` decidió al importarse (`CURIANA_ELENCO`)."""
    sys.path.insert(0, _AQUI)
    import curiana_agents as ag
    return Elenco(ag.ALL_AGENTS, ag.ALIAS_ERA1, ag.FUERA_DEL_ELENCO, ag.ELENCO)


def agentes_de_hecho(hecho: dict, elenco) -> list:
    """Los `agentes_relacionados` de un hecho con el nombre que tienen en el
    elenco activo: resueltos por alias, en su orden, sin repetidos y sólo los
    que el elenco tiene.

    Es la única puerta por la que un consumidor debe leer ese campo: quien
    busque «los hechos de Birokoa» encuentra los que el corpus escribió como
    `Biro-ko`. Lo que el elenco no tiene (persona de fondo, sin equivalente,
    fantasma) no sale de aquí; eso lo reporta `validar_agentes`. No toca el
    hecho: `huella_de_base` lo hashea tal como se leyó.
    """
    elenco = Elenco.de(elenco)
    relacionados = hecho.get("agentes_relacionados") or []
    if isinstance(relacionados, str):
        return []
    salida = []
    for nombre in relacionados:
        resuelto = elenco.resolver(nombre)
        if resuelto in elenco.agentes and resuelto not in salida:
            salida.append(resuelto)
    return salida


def censo_de_elenco(hechos: list, elenco) -> dict:
    """Cómo cae el corpus sobre el elenco activo, medido: cuántas menciones
    resuelven por alias y qué nombres se quedan sin equivalente, con sus
    hechos. Es lo que el informe imprime y `--json` emite bajo `elenco`."""
    elenco = Elenco.de(elenco)
    por_alias = 0
    sin_equivalente = defaultdict(list)
    for hecho in hechos:
        relacionados = hecho.get("agentes_relacionados") or []
        if isinstance(relacionados, str):
            continue
        for nombre in relacionados:
            resuelto = elenco.resolver(nombre)
            if resuelto != nombre and resuelto in elenco.agentes:
                por_alias += 1
            elif nombre in elenco.sin_equivalente:
                sin_equivalente[nombre].append(hecho.get("id"))
    return {
        "era": elenco.era,
        "agentes": len(elenco.agentes),
        "menciones_por_alias": por_alias,
        "sin_equivalente": dict(sorted(sin_equivalente.items(),
                                       key=lambda kv: (-len(kv[1]), kv[0]))),
        "fuera_del_elenco_no_citados": sorted(elenco.sin_equivalente - set(sin_equivalente)),
    }


# ══════════════════════════════════════════════════════════════════════
# CARGA
# ══════════════════════════════════════════════════════════════════════

def cargar(directorio: str = CORPUS_DIR):
    """Lee los YAML del corpus y aplana los hechos a una sola lista.

    Devuelve `(hechos, genealogia, problemas_de_carga)`.

    Los archivos no tienen todos la misma forma de raíz: unos son una lista de
    hechos, `ecologia.yaml` es un dict con `entradas` y `huecos_lexicos`. Se
    normaliza aquí, guardando de dónde salió cada hecho (`archivo`, `seccion`)
    para que el informe pueda señalar el sitio exacto.
    """
    hechos, problemas = [], []
    genealogia = None

    if not os.path.isdir(directorio):
        problemas.append(_error("corpus-ausente", directorio,
                                "el directorio del corpus no existe"))
        return hechos, genealogia, problemas

    for nombre in sorted(os.listdir(directorio)):
        if not nombre.endswith(".yaml"):
            continue
        ruta = os.path.join(directorio, nombre)
        try:
            with open(ruta, encoding="utf-8") as f:
                datos = yaml.safe_load(f)
        except yaml.YAMLError as e:
            problemas.append(_error("yaml-invalido", nombre, f"no parsea: {e}"))
            continue

        if nombre == ARCHIVO_GENEALOGIA:
            genealogia = datos
            continue

        if isinstance(datos, list):
            secciones = {None: datos}
        elif isinstance(datos, dict):
            secciones = datos
        else:
            problemas.append(_error("raiz-inesperada", nombre,
                                    f"la raíz es {type(datos).__name__}, "
                                    "se esperaba lista o dict"))
            continue

        for seccion, entradas in secciones.items():
            if not isinstance(entradas, list):
                problemas.append(_error("seccion-inesperada", f"{nombre}:{seccion}",
                                        f"es {type(entradas).__name__}, se esperaba lista"))
                continue
            for i, entrada in enumerate(entradas):
                if not isinstance(entrada, dict):
                    problemas.append(_error("entrada-inesperada", f"{nombre}:{seccion}[{i}]",
                                            f"es {type(entrada).__name__}, se esperaba dict"))
                    continue
                hecho = dict(entrada)
                hecho["_archivo"] = nombre
                hecho["_seccion"] = seccion
                hechos.append(hecho)

    return hechos, genealogia, problemas


def _dominio_de_archivo(nombre: str) -> str:
    """`geografia_politica.yaml` → `geografia_politica`."""
    return nombre[:-len(".yaml")] if nombre.endswith(".yaml") else nombre


def _donde(hecho: dict) -> str:
    return f"{hecho.get('_archivo', '?')}#{hecho.get('id', '(sin id)')}"


# ══════════════════════════════════════════════════════════════════════
# VALIDACIONES
# ══════════════════════════════════════════════════════════════════════

def validar_estructura(hechos: list) -> list:
    """Campos obligatorios, forma del `id`, unicidad, dominio coherente."""
    problemas = []
    vistos = defaultdict(list)

    for hecho in hechos:
        donde = _donde(hecho)

        for campo in CAMPOS_OBLIGATORIOS:
            if campo not in hecho:
                problemas.append(_error("campo-falta", donde, f"falta `{campo}`"))
            elif (campo not in CAMPOS_QUE_PUEDEN_IR_VACIOS
                    and not str(hecho[campo]).strip()):
                problemas.append(_error("campo-vacio", donde, f"`{campo}` está vacío"))

        hid = hecho.get("id")
        if not hid:
            continue
        vistos[hid].append(hecho.get("_archivo"))

        m = re.fullmatch(RE_REFERENCIA, str(hid))
        if not m:
            problemas.append(_error("id-malformado", donde,
                                    f"`{hid}` no tiene la forma <dominio>-NNN"))
            continue

        dominio_id = m.group(1)
        dominio_archivo = _dominio_de_archivo(hecho.get("_archivo", ""))
        permitidos = {dominio_archivo} | NAMESPACES_EXTRA.get(dominio_archivo, set())
        if dominio_id not in permitidos:
            problemas.append(_error("id-dominio-cruzado", donde,
                                    f"el id dice `{dominio_id}` pero está en "
                                    f"{hecho['_archivo']} (permitidos: "
                                    f"{', '.join(sorted(permitidos))})"))

    for hid, archivos in vistos.items():
        if len(archivos) > 1:
            problemas.append(_error("id-duplicado", hid,
                                    f"aparece {len(archivos)} veces: "
                                    f"{', '.join(archivos)}"))

    return problemas


def validar_etiquetas(hechos: list) -> list:
    """`fuente` es una de las cinco del README. Ni una más, ni una variante."""
    problemas = []
    for hecho in hechos:
        fuente = hecho.get("fuente")
        if fuente is None:
            continue                     # ya lo reporta validar_estructura
        if fuente not in ETIQUETAS_FUENTE:
            problemas.append(_error("etiqueta-ilegal", _donde(hecho),
                                    f"`fuente: {fuente}` no es legal "
                                    f"(legales: {', '.join(ETIQUETAS_FUENTE)})"))
    return problemas


def validar_agentes(hechos: list, agentes, fondo: set) -> list:
    """Cada `agentes_relacionados`, resuelto por alias, existe en el elenco activo.

    `agentes` es el `Elenco` activo (o un set de nombres: un elenco sin alias).
    Un nombre que no resuelve tiene tres salidas:
      - es de la era 1 y el elenco activo lo deja fuera
        (`elenco.sin_equivalente`): aviso `agente-sin-equivalente` — el corpus
        es canon y la decisión (alias o persona de fondo) es de Miguel;
      - está en `genealogia.yaml` como persona de fondo: aviso
        `agente-de-fondo` — propuestas sin veto todavía, citadas a sabiendas;
      - lo demás: error `agente-fantasma`.
    """
    elenco = Elenco.de(agentes)
    problemas = []
    for hecho in hechos:
        relacionados = hecho.get("agentes_relacionados") or []
        if isinstance(relacionados, str):
            problemas.append(_error("agentes-no-lista", _donde(hecho),
                                    "`agentes_relacionados` es una cadena, "
                                    "se esperaba lista"))
            continue
        validos = set(agentes_de_hecho(hecho, elenco))
        for nombre in relacionados:
            if elenco.resolver(nombre) in validos:
                continue
            if nombre in elenco.sin_equivalente:
                problemas.append(_aviso("agente-sin-equivalente", _donde(hecho),
                                        f"`{nombre}` es de la era 1 y el elenco "
                                        f"{elenco.era} no lo tiene ni por alias"))
            elif nombre in fondo:
                problemas.append(_aviso("agente-de-fondo", _donde(hecho),
                                        f"`{nombre}` no es agente de "
                                        f"curiana_agents.py; es persona de fondo "
                                        f"propuesta en {ARCHIVO_GENEALOGIA}"))
            else:
                problemas.append(_error("agente-fantasma", _donde(hecho),
                                        f"`{nombre}` no existe ni en "
                                        f"curiana_agents.py ni en "
                                        f"{ARCHIVO_GENEALOGIA}"))
    return problemas


def _textos_de(hecho: dict):
    for campo in CAMPOS_TEXTO:
        valor = hecho.get(campo)
        if isinstance(valor, str):
            yield campo, valor


def validar_referencias_cruzadas(hechos: list) -> list:
    """Todo token `<dominio>-NNN` en texto libre resuelve a un hecho real."""
    problemas = []
    ids = {h.get("id") for h in hechos if h.get("id")}
    dominios = set()
    for h in hechos:
        dominio = _dominio_de_archivo(h["_archivo"])
        dominios.add(dominio)
        dominios |= NAMESPACES_EXTRA.get(dominio, set())

    for hecho in hechos:
        for campo, texto in _textos_de(hecho):
            for m in RE_REFERENCIA.finditer(texto):
                token = m.group(0)
                if token in ids:
                    continue
                # Solo se exige que resuelvan los tokens cuyo dominio es del
                # corpus: así "Oliver 1989" o una fecha no disparan falsos
                # positivos, pero un `parentesco-999` sí.
                if m.group(1) in dominios:
                    problemas.append(_error("referencia-rota", _donde(hecho),
                                            f"`{campo}` cita `{token}`, que no "
                                            f"existe en el corpus"))
    return problemas


def _obras_de_la_bibliografia():
    """Los ids de `4-fuentes/bibliografia.yaml`, o None si no existe."""
    ruta = os.path.join(_AQUI, "..", "4-fuentes", "bibliografia.yaml")
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}
    return {o["id"] for o in doc.get("obras", []) if o.get("id")}


def validar_procedencia(hechos: list, obras) -> list:
    """`procedencia.obra` es una clave foránea contra la bibliografía.

    El campo es **opcional** todavía: 58 de los 161 hechos lo tienen (los que
    citaban una sola obra de forma inequívoca). Los demás siguen con la
    `referencia` en prosa, que no se toca — dice cosas que un id no puede
    (página, cita textual, "vía tal").

    Lo que sí se comprueba es que, cuando está, apunte a una obra real. Sin
    esto, migrar el corpus a ids habría cambiado un texto libre por otro.
    """
    problemas = []
    if obras is None:
        return [_aviso("sin-bibliografia", "4-fuentes/bibliografia.yaml",
                       "no existe: las citas del corpus no se pueden comprobar. "
                       "Genérala con `python curiana_sim/generar_bibliografia.py`")]

    for hecho in hechos:
        proc = hecho.get("procedencia")
        if proc is None:
            continue
        donde = _donde(hecho)
        if not isinstance(proc, dict):
            problemas.append(_error("procedencia-mal-formada", donde,
                                    f"es {type(proc).__name__}, se esperaba dict"))
            continue
        obra = proc.get("obra")
        if not obra:
            problemas.append(_error("procedencia-sin-obra", donde,
                                    "`procedencia` sin campo `obra`"))
        elif obra not in obras:
            problemas.append(_error(
                "obra-fantasma", donde,
                f"cita la obra `{obra}`, que no está en la bibliografía"))
    return problemas


def validar_rutas(hechos: list) -> list:
    """Nadie puede citar `curiana_sim/cultura/`: ya no existe."""
    problemas = []
    for hecho in hechos:
        for campo, texto in _textos_de(hecho):
            if RUTA_MUERTA in texto:
                problemas.append(_error("ruta-muerta", _donde(hecho),
                                        f"`{campo}` cita `{RUTA_MUERTA}`, ruta "
                                        f"anterior al refactor del vault; hoy "
                                        f"el corpus vive en 3-mundo/corpus/"))
    return problemas


def validar_enganche_motor(hechos: list, locaciones: set, lexico: set) -> list:
    """`locacion` y `palabra_lexicon`: los dos puntos donde el corpus toca código."""
    problemas = []
    for hecho in hechos:
        loc = hecho.get("locacion")
        if loc and loc not in locaciones:
            problemas.append(_error("locacion-desconocida", _donde(hecho),
                                    f"`locacion: {loc}` no está en "
                                    f"curiana_state.LOCACIONES"))

        palabra = hecho.get("palabra_lexicon")
        if palabra and palabra not in lexico:
            problemas.append(_error("palabra-desconocida", _donde(hecho),
                                    f"`palabra_lexicon: {palabra}` no está en "
                                    f"VOCABULARIO_BASE"))

        # Un hueco léxico es, por definición, un fenómeno SIN palabra caquetía.
        # Si trae una, o el hueco ya no es hueco o la palabra está mal puesta.
        if hecho.get("hueco_lexico") and palabra:
            problemas.append(_aviso("hueco-con-palabra", _donde(hecho),
                                    f"marcado `hueco_lexico` pero trae "
                                    f"`palabra_lexicon: {palabra}`"))
    return problemas


def _parece_nombre(valor) -> bool:
    """¿Este campo trae un nombre suelto, o una explicación en prosa?

    `genealogia.yaml` mezcla las dos cosas en el mismo campo a propósito:
    `linaje: Kaira` frente a `linaje: no asignado — nota: si se modela una rama
    insular…`. Solo lo primero es comprobable; lo segundo es la fuente diciendo
    que el dato no existe, que es información y no deuda.
    """
    if not isinstance(valor, str):
        return False
    valor = valor.strip()
    if not valor:
        return False
    return not (" " in valor or "—" in valor or "(" in valor)


def validar_genealogia(genealogia, agentes) -> list:
    """Esquema propio: linajes citados existen, madres y cónyuges resuelven.

    `agentes` es el `Elenco` activo (o un set de nombres). La genealogía
    nombra como la era 1, así que se resuelve por alias antes de comparar.
    """
    elenco = Elenco.de(agentes)
    agentes = elenco.agentes
    problemas = []
    if genealogia is None:
        problemas.append(_aviso("genealogia-ausente", ARCHIVO_GENEALOGIA,
                                "no se encontró el archivo"))
        return problemas
    if not isinstance(genealogia, dict):
        problemas.append(_error("genealogia-raiz", ARCHIVO_GENEALOGIA,
                                f"la raíz es {type(genealogia).__name__}"))
        return problemas

    linajes = set(genealogia.get("linajes") or {})
    personas = dict(genealogia.get("agentes") or {})
    personas.update(genealogia.get("personas_de_fondo") or {})
    conocidos = set(personas) | agentes

    for nombre, registro in personas.items():
        donde = f"{ARCHIVO_GENEALOGIA}#{nombre}"
        if not isinstance(registro, dict):
            problemas.append(_error("genealogia-registro", donde,
                                    f"es {type(registro).__name__}, se esperaba dict"))
            continue

        # `linaje`, `madre` y `conyuge` son texto libre en este archivo: la
        # mitad de los registros explican en prosa por qué el dato NO está
        # ("no asignado", "no nombrada — se propone Kaira-sha (fondo)"), y esa
        # honestidad es deliberada, no un hueco que haya que llenar. Así que
        # solo se comprueban los valores que parecen un nombre suelto.
        linaje = registro.get("linaje")
        if _parece_nombre(linaje) and linaje.strip() not in linajes:
            problemas.append(_error("linaje-desconocido", donde,
                                    f"`linaje: {linaje}` no está declarado en "
                                    f"`linajes`"))

        for campo in ("madre", "conyuge"):
            valor = registro.get(campo)
            if (_parece_nombre(valor) and valor.strip() not in conocidos
                    and elenco.resolver(valor.strip()) not in conocidos):
                problemas.append(_aviso("pariente-desconocido", donde,
                                        f"`{campo}: {valor}` no resuelve a "
                                        f"ninguna persona conocida"))

        for campo, texto in list(registro.items()):
            if isinstance(texto, str) and RUTA_MUERTA in texto:
                problemas.append(_error("ruta-muerta", donde,
                                        f"`{campo}` cita `{RUTA_MUERTA}`, ruta "
                                        f"anterior al refactor del vault"))

    # Un agente de la simulación sin ficha genealógica no es un error, pero sí
    # una laguna que conviene ver medida. Las fichas llevan el nombre de la
    # era 1: se resuelven antes de restar, o bajo la era 2 saldrían todos.
    con_ficha = {elenco.resolver(n) for n in (genealogia.get("agentes") or {})}
    sin_ficha = agentes - con_ficha
    if sin_ficha:
        problemas.append(_aviso("agente-sin-ficha", ARCHIVO_GENEALOGIA,
                                f"{len(sin_ficha)} agentes sin ficha: "
                                f"{', '.join(sorted(sin_ficha))}"))
    return problemas


# ══════════════════════════════════════════════════════════════════════
# COMPILACIÓN
# ══════════════════════════════════════════════════════════════════════

def _universo_del_motor():
    """El elenco activo, las locaciones y el léxico, leídos del código.

    Se importa aquí y no arriba para que el módulo se pueda cargar (y testear)
    aunque el motor no esté importable; si falla, se devuelve vacío y las
    validaciones que dependen del motor quedan anotadas como no ejecutadas.
    """
    sys.path.insert(0, _AQUI)
    from curiana_state import LOCACIONES
    from curiana_lexicon import VOCABULARIO_BASE
    return elenco_activo(), set(LOCACIONES), set(VOCABULARIO_BASE)


def compilar(directorio: str = CORPUS_DIR, universo=None):
    """Carga, valida y devuelve `(hechos, genealogia, problemas)`.

    Los hechos vuelven tal como se leyeron: `agentes_relacionados` conserva
    los nombres de la era 1 aunque el elenco activo sea la era 2 (la
    resolución es `agentes_de_hecho`, y `huella_de_base` hashea esto).
    """
    hechos, genealogia, problemas = cargar(directorio)

    if universo is None:
        try:
            universo = _universo_del_motor()
        except Exception as e:                              # noqa: BLE001
            problemas.append(_aviso("motor-no-importable", "curiana_sim",
                                    f"no se pudo leer el motor ({e}); las "
                                    f"validaciones de agentes, locación y "
                                    f"léxico NO se corrieron"))
            universo = (set(), set(), set())
    elenco, locaciones, lexico = universo
    elenco = Elenco.de(elenco)

    fondo = set()
    if isinstance(genealogia, dict):
        fondo = set(genealogia.get("personas_de_fondo") or {})

    problemas += validar_estructura(hechos)
    problemas += validar_etiquetas(hechos)
    problemas += validar_referencias_cruzadas(hechos)
    problemas += validar_rutas(hechos)
    problemas += validar_procedencia(hechos, _obras_de_la_bibliografia())
    if elenco.agentes:
        problemas += validar_agentes(hechos, elenco, fondo)
        problemas += validar_genealogia(genealogia, elenco)
    if locaciones or lexico:
        problemas += validar_enganche_motor(hechos, locaciones, lexico)

    return hechos, genealogia, problemas


def fusionar(hechos: list, genealogia, problemas: list) -> dict:
    """El documento único que consumirá la simulación cuando llegue el momento."""
    censo = Counter(h.get("fuente") for h in hechos)
    por_archivo = Counter(h.get("_archivo") for h in hechos)

    limpios = []
    for hecho in hechos:
        salida = {k: v for k, v in hecho.items() if not k.startswith("_")}
        salida["archivo"] = hecho.get("_archivo")
        if hecho.get("_seccion"):
            salida["seccion"] = hecho["_seccion"]
        limpios.append(salida)

    return {
        "meta": {
            "generado_por": "curiana_sim/compilar_corpus.py",
            "hechos": len(limpios),
            "por_etiqueta": {k: censo[k] for k in ETIQUETAS_FUENTE if censo[k]},
            "por_archivo": dict(sorted(por_archivo.items())),
            "errores": sum(1 for p in problemas if p.nivel == "error"),
            "avisos": sum(1 for p in problemas if p.nivel == "aviso"),
        },
        "hechos": limpios,
        "genealogia": genealogia,
    }


# ══════════════════════════════════════════════════════════════════════
# INFORME
# ══════════════════════════════════════════════════════════════════════

def informe(hechos, genealogia, problemas, censo_elenco=None) -> None:
    errores = [p for p in problemas if p.nivel == "error"]
    avisos = [p for p in problemas if p.nivel == "aviso"]

    print("\n── Corpus cultural ──")
    print(f"  hechos: {len(hechos)}")
    por_archivo = Counter(h.get("_archivo") for h in hechos)
    for archivo, n in sorted(por_archivo.items()):
        print(f"     {archivo:<28} {n:>4}")

    print("\n── Etiquetas epistémicas ──")
    censo = Counter(h.get("fuente") for h in hechos)
    for etiqueta in ETIQUETAS_FUENTE:
        if censo[etiqueta]:
            pct = 100.0 * censo[etiqueta] / max(len(hechos), 1)
            print(f"     {etiqueta:<20} {censo[etiqueta]:>4}  {pct:>5.1f}%")
    ilegales = {k: v for k, v in censo.items() if k not in ETIQUETAS_FUENTE}
    if ilegales:
        print(f"     ⚠ ilegales: {ilegales}")

    if genealogia:
        print("\n── Genealogía ──")
        for seccion in ("linajes", "agentes", "personas_de_fondo"):
            print(f"     {seccion:<20} {len(genealogia.get(seccion) or {}):>4}")

    # `censo` (arriba) es el de etiquetas; este es el del elenco activo.
    ce = censo_elenco
    if ce:
        print("\n── Elenco ──")
        print(f"     {'era':<20} {ce['era']:>4}")
        print(f"     {'agentes':<20} {ce['agentes']:>4}")
        sin = ce["sin_equivalente"]
        if ce["menciones_por_alias"] or sin:
            print(f"     {'por alias (menciones)':<24} {ce['menciones_por_alias']:>4}")
            n_hechos = len({i for ids in sin.values() for i in ids})
            print(f"     sin equivalente en {ce['era']}: {len(sin)} nombres "
                  f"en {n_hechos} hechos — decisión pendiente (alias o fondo)")
            for nombre, ids in sin.items():
                print(f"        {nombre:<14} {len(ids):>3}  {', '.join(ids)}")
            if ce["fuera_del_elenco_no_citados"]:
                print(f"     fuera del elenco y sin cita en el corpus: "
                      f"{', '.join(ce['fuera_del_elenco_no_citados'])}")

    def _bloque(titulo, lista):
        print(f"\n── {titulo}: {len(lista)} ──")
        por_codigo = defaultdict(list)
        for p in lista:
            por_codigo[p.codigo].append(p)
        for codigo, items in sorted(por_codigo.items()):
            print(f"  [{codigo}] × {len(items)}")
            for p in items[:8]:
                print(f"     {p.donde}: {p.mensaje}")
            if len(items) > 8:
                print(f"     … y {len(items) - 8} más")

    if errores:
        _bloque("ERRORES", errores)
    if avisos:
        _bloque("Avisos", avisos)

    print("\n" + "=" * 60)
    if errores:
        print(f"  ✗ {len(errores)} error(es), {len(avisos)} aviso(s)")
    else:
        print(f"  ✓ corpus válido — {len(hechos)} hechos, {len(avisos)} aviso(s)")
    print("=" * 60)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Valida y compila el corpus cultural")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 si hay errores (para CI / el gate)")
    ap.add_argument("--avisos", action="store_true",
                    help="con --check, los avisos también fallan")
    ap.add_argument("--fusionar", metavar="RUTA",
                    help="escribe el YAML fusionado en RUTA")
    ap.add_argument("--json", action="store_true",
                    help="emite el informe en JSON en vez de en prosa")
    ap.add_argument("--corpus", default=CORPUS_DIR,
                    help="directorio del corpus (por defecto 3-mundo/corpus/)")
    args = ap.parse_args(argv)

    hechos, genealogia, problemas = compilar(args.corpus)
    errores = [p for p in problemas if p.nivel == "error"]
    avisos = [p for p in problemas if p.nivel == "aviso"]
    try:
        censo = censo_de_elenco(hechos, elenco_activo())
    except Exception:                                       # noqa: BLE001
        censo = None                     # ya lo anotó compilar(): motor-no-importable

    if args.fusionar:
        documento = fusionar(hechos, genealogia, problemas)
        with open(args.fusionar, "w", encoding="utf-8") as f:
            yaml.safe_dump(documento, f, allow_unicode=True, sort_keys=False,
                           default_flow_style=False, width=100)
        if not args.json:
            print(f"  → fusionado: {args.fusionar} ({len(hechos)} hechos)")

    if args.json:
        print(json.dumps({
            "hechos": len(hechos),
            "por_etiqueta": dict(Counter(h.get("fuente") for h in hechos)),
            "elenco": censo,
            "errores": [p.como_dict() for p in errores],
            "avisos": [p.como_dict() for p in avisos],
        }, ensure_ascii=False, indent=2))
    else:
        informe(hechos, genealogia, problemas, censo)

    if args.check:
        if errores or (args.avisos and avisos):
            return 1
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
