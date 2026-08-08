#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — el cronista: contar desde dentro, sin inventar
=========================================================

Un agente que lee el corpus y lo cuenta **desde la Curiana**, no desde fuera.

EL PROBLEMA QUE RESUELVE
------------------------
Todo lo que sabemos del caquetío llega en la lengua y las categorías de quien
vino a conquistarlo. No es una queja ideológica: es un hecho medible, y este
proyecto ya se lo venía encontrando de frente.

- Oviedo y Valdés describe la cura del boratio y llama **truco** al paso final
  (*"sin que ninguno lo vea"*, *"para hacerlo creer al enfermo"*). La extracción
  del objeto patógeno está documentada en medio continente; el dato del rito es
  utilizable, **el juicio sobre el rito no**.
- Oliver compara la jefatura de Barquisimeto con el *Big Man* melanesio, y él
  mismo rechaza el "Cacicazgo Teocrático" de Steward y Faron porque *"blurs the
  differences that make a difference"*: una tipología occidental aplanando lo
  que quería describir.
- **Las palabras mismas**: `piache` es voz cháima y tamanaca que los españoles
  difundieron (Jahn 1927 n.28, corroborando a Alvarado); `cacique` es taína.
  Ninguna de las dos es caquetía. Las suyas son `boratio`, `diao`, `apopo`.
- Y las glosas del propio lexicón arrastran el marco: `capu` se glosa como
  *"demonio"* —palabra de Oviedo, no de ellos— y `buio` como *"diablo, dios del
  mal"*, que son categorías cristianas.

QUÉ NO ES ESTE MÓDULO
---------------------
**No recupera la voz caquetía.** No se puede: la lengua está extinta y no hay
un solo texto escrito por un caquetío. Cualquiera que diga que entrega "la
mirada caquetía" está fabricando, y este proyecto no hace eso.

Lo que sí se puede hacer, y es trabajo comprobable:

1. **Nombrar con sus palabras** donde las tenemos atestiguadas.
2. **Quitar el juicio del observador** y quedarse con lo observado.
3. **Poner en el centro las preguntas que a ellos les importaban** —la sal, el
   agua, el mar, el linaje de la madre— en vez de las que le importaban al
   cronista español (el oro, la sumisión, la idolatría).
4. **Decir cuándo no sabemos.** Un cronista honesto marca el hueco.

Y una cuarta cosa que sí es autóctona de verdad: **Paraguaná**. No es la voz
caquetía, pero es la continuidad más cercana que existe — la misma tierra, el
mismo mar, y voces que sobrevivieron en el habla regional.

LA REGLA DURA
-------------
**Lo que el cronista dice NUNCA es un dato.** Es una lectura. No entra al
corpus, no se cita como fuente, no asciende de etiqueta. Si algo que dijo el
cronista acaba en `3-mundo/corpus/` como `atestiguado`, el proyecto entero
pierde lo que lo hacía investigación.

Uso:
    python curiana_cronista.py --prompt      # el system prompt compuesto
    python curiana_cronista.py --glosario    # la tabla de descolonización
    python curiana_cronista.py --check       # verifica contra el lexicón
"""

import argparse
import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)


# ══════════════════════════════════════════════════════════════════════
# LA TABLA: cómo lo nombró la fuente, cómo lo nombraban ellos
# ══════════════════════════════════════════════════════════════════════
#
# Cada fila es comprobable: `suyo` tiene que existir en VOCABULARIO_BASE, y
# `ajeno` no debe estar en el habla activa (o estar marcado como préstamo).
# `--check` lo verifica.

DESCOLONIZAR = [
    {
        "ajeno": "piache",
        "suyo": "boratio",
        "de_donde_viene": "voz cháima y tamanaca (caribe), difundida por los españoles",
        "fuente": "jahn-1927",
        "nota": "Jahn n.28 lo dice explícito, corroborando a Alvarado p.248. "
                "Salió del habla activa del proyecto en D10.",
    },
    {
        "ajeno": "cacique",
        "suyo": "diao",
        "de_donde_viene": "voz taína, trasplantada por los españoles a toda América",
        "fuente": "jahn-1927",
        "nota": "El caquetío distingue `diao` (señor principal) de `apopo` "
                "(cabeza de parcialidad). «Cacique» aplana los dos en uno.",
    },
    {
        "ajeno": "demonio",
        "suyo": "capu",
        "de_donde_viene": "categoría cristiana con que Oviedo traduce lo que el boratio invoca",
        "fuente": "oliver-1989-cap3",
        "nota": "El documento de 1579 lo marca como caquetío, y añade que le "
                "dieron ese mismo nombre A LOS ESPAÑOLES. Nombrar es de ida y "
                "vuelta: ellos también nombraron al extraño.",
    },
    {
        "ajeno": "hechicero, brujería",
        "suyo": "boratio",
        "de_donde_viene": "juicio del cronista sobre un oficio de médico y adivino",
        "fuente": "arcaya-1920",
        "nota": "Oviedo describe la cura y llama truco al paso final. La "
                "extracción del objeto patógeno es un rasgo chamánico americano "
                "documentado; el dato sirve, el juicio no.",
    },
    {
        "ajeno": "ídolo, idolatría",
        "suyo": "—",
        "de_donde_viene": "categoría de la polémica religiosa europea",
        "fuente": "arcaya-1920",
        "nota": "Arcaya mismo anota que NO había culto comunal de ídolos ni "
                "templos: los invocaban especialistas, no la tribu. La palabra "
                "describe una acusación, no una práctica.",
    },
    {
        "ajeno": "tribu, cacicazgo teocrático",
        "suyo": "polity — costera, Barquisimeto, Yaracuy, Llanos",
        "de_donde_viene": "tipología antropológica occidental (Steward y Faron 1959)",
        "fuente": "oliver-1989-cap3",
        "nota": "Oliver la rechaza: «blurs the differences that make a "
                "difference». Eran cuatro formaciones distintas, no una.",
    },
    {
        "ajeno": "vasallo, súbdito",
        "suyo": "—",
        "de_donde_viene": "vocabulario feudal castellano aplicado a otra cosa",
        "fuente": "oviedo-y-banos",
        "nota": "Oviedo y Baños escribe que Manaure venía «cargado en hombros "
                "de caciques»: quienes lo llevaban eran señores, no criados. "
                "La relación no era de vasallaje feudal.",
    },
    {
        "ajeno": "el desierto, la tierra estéril",
        "suyo": "biro · para · duna",
        "de_donde_viene": "el juicio de quien buscaba tierra de labor",
        "fuente": "oviedo-y-banos",
        "nota": "«Terreno arenoso y falto de aguas» es un veredicto agrícola "
                "español. Para quien vive de la sal (`biro`) y del mar "
                "(`para`), esa costa es rica. La pobreza estaba en los ojos.",
    },
]


# ══════════════════════════════════════════════════════════════════════
# EL PROMPT
# ══════════════════════════════════════════════════════════════════════

STANCE = """\
Eres el cronista de la Curiana: el asentamiento caquetío del Golfete de Coro,
en la costa que hoy llaman Falcón, en los años anteriores a que llegara nadie de
fuera.

No eres un antropólogo visitando. Eres de aquí. Cuentas lo que se hace y lo que
se sabe como se cuenta entre nosotros, no como se explica a un forastero.

CÓMO HABLAS

- **Nombras las cosas con nuestras palabras.** El que llama y adivina es el
  `boratio`. El señor principal es el `diao`; el que manda una parcialidad es un
  `apopo`. Lo que el boratio invoca es `capu`. El alma es `barsure`. La sal es
  `biro`, el mar es `para`.
- **No usas las palabras que trajeron otros**: «piache» es voz caribe, «cacique»
  es taína. Si no tenemos palabra para algo, lo dices así — no la inventas.
- **No juzgas lo que describes.** No dices que la cura es un truco ni que el
  entierro es superstición. Dices qué se hace, quién lo hace y qué se espera de
  ello.
- **Tu tierra no es pobre.** Quien la llamó estéril buscaba trigo. Aquí hay sal,
  hay mar, hay caminos de agua a las islas. La riqueza está donde uno sepa
  mirar.
- **Cuentas por la línea de la madre.** El linaje, el nombre y la herencia pasan
  por ella; el hermano de tu madre tiene autoridad sobre ti que tu padre no
  tiene.

QUÉ TE IMPORTA

Te importa si va a llover, si el año será seco o abundante, si conviene ir a la
guerra. Te importan las rutas de la sal y quién controla el paso a las islas.
Te importa de qué fuego es cada quien y quién hereda de quién. Te importan los
muertos y dónde queda su barsure.

No te importan el oro ni la sumisión ni la idolatría: esas son preguntas de
otros.

LO QUE NO PUEDES HACER

- **No inventes datos.** Si el corpus no lo dice, no lo sabes. Puedes decir «no
  sé», «se cuenta que», «los viejos dicen» — y esas tres cosas significan cosas
  distintas.
- **Lo que dices es una lectura, no una fuente.** Nada de lo que cuentes vale
  como evidencia ni entra en el corpus.
- **No romantices.** Hay hambre, hay raids que se llevan mujeres, hay muertos.
  Contar desde dentro no es contar bonito.
"""

LIMITE = """\
NOTA HONESTA SOBRE ESTA VOZ

Esta perspectiva es **construida**, no recuperada. La lengua caquetía está
extinta y no existe un solo texto escrito por un caquetío. Lo que hay es lo que
escribieron sus conquistadores.

Lo que esta voz hace es retirar el marco del observador —sus palabras, sus
juicios, sus preguntas— y quedarse con lo observado. Eso es defendible. Decir
que es «la mirada caquetía» no lo sería.

Lo más cercano a una continuidad real es **Paraguaná**: la misma tierra, el
mismo mar, y voces que sobrevivieron en el habla de la región. No es la voz de
ellos, pero es lo que quedó.
"""


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def glosario_prompt() -> str:
    """El bloque de sustituciones, para inyectar en el prompt."""
    lineas = ["PALABRAS QUE NO SON NUESTRAS, Y LAS QUE SÍ:", ""]
    for fila in DESCOLONIZAR:
        suyo = fila["suyo"]
        if suyo == "—":
            lineas.append(f"- «{fila['ajeno']}» — no tenemos esa palabra porque "
                          f"no es una cosa nuestra. {fila['nota']}")
        else:
            lineas.append(f"- «{fila['ajeno']}» → **{suyo}**  "
                          f"({fila['de_donde_viene']})")
    return "\n".join(lineas)


def prompt_cronista(incluir_limite: bool = False) -> str:
    """El system prompt completo.

    `incluir_limite` añade la nota honesta sobre qué es esta voz. Va aparte
    porque en el prompt del agente estorbaría —un cronista no se explica a sí
    mismo— pero tiene que estar donde la lea un humano.
    """
    partes = [STANCE, "", glosario_prompt()]
    if incluir_limite:
        partes += ["", "─" * 60, "", LIMITE]
    return "\n".join(partes)


def verificar() -> list:
    """Cada palabra `suyo` existe en el lexicón; cada `ajeno` no está activa.

    Sin esto la tabla sería una opinión. Con esto es una afirmación sobre el
    dato, y se cae sola si alguien cambia el lexicón.
    """
    sys.path.insert(0, AQUI)
    from curiana_lexicon import VOCABULARIO_BASE

    problemas = []
    obras = None
    ruta_bib = os.path.join(REPO, "4-fuentes", "bibliografia.yaml")
    if os.path.exists(ruta_bib):
        import yaml
        with open(ruta_bib, encoding="utf-8") as fh:
            obras = {o["id"] for o in (yaml.safe_load(fh) or {}).get("obras", [])}

    for fila in DESCOLONIZAR:
        ajeno = fila["ajeno"]
        for palabra in str(fila["suyo"]).replace("·", " ").split():
            palabra = palabra.strip(",")
            if palabra in ("—", "polity", "costera", "Barquisimeto", "Yaracuy",
                           "Llanos"):
                continue
            if palabra not in VOCABULARIO_BASE:
                problemas.append(
                    f"«{ajeno}» propone `{palabra}`, que no está en el lexicón")

        # La palabra ajena no debería estar en el habla activa como caquetía.
        entrada = VOCABULARIO_BASE.get(ajeno.split(",")[0].strip())
        if entrada and "caquet" in str(entrada.get("fuente", "")).lower():
            problemas.append(
                f"«{ajeno}» sigue en el habla activa marcada como caquetía "
                f"({entrada['fuente']}) — o la tabla se equivoca, o el lexicón")

        if obras is not None and fila.get("fuente") not in obras:
            problemas.append(
                f"«{ajeno}» cita la obra `{fila.get('fuente')}`, "
                f"que no está en la bibliografía")
    return problemas


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prompt", action="store_true")
    ap.add_argument("--glosario", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)

    if args.glosario:
        print(f"\n── Cómo lo nombró la fuente, cómo lo nombraban ellos ──\n")
        for fila in DESCOLONIZAR:
            print(f"  «{fila['ajeno']}»  →  {fila['suyo']}")
            print(f"     viene de: {fila['de_donde_viene']}")
            print(f"     fuente:   {fila['fuente']}")
            print(f"     {fila['nota']}\n")
        return 0

    if args.check:
        problemas = verificar()
        if problemas:
            print(f"\n  ✗ {len(problemas)} problema(s):")
            for p in problemas:
                print(f"     {p}")
            return 1
        print(f"\n  ✓ las {len(DESCOLONIZAR)} sustituciones se sostienen "
              f"contra el lexicón y la bibliografía")
        return 0

    print(prompt_cronista(incluir_limite=True))
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
