# -*- coding: utf-8 -*-
"""F8, el resto: los 23 valores de `fuente` que no son canónicos, medidos uno a
uno y llevados a un conjunto declarado. Corre con --dry-run para ver la tabla
sin tocar nada.

Lo medido el 2026-09-12 (ver la tabla que imprime):

  · `lokono/proto-arawakan` (14) y `lokono/garifuna` (13) NO son lokono. Son
    27 entradas SIN `notas` con glosas como «brisa del golfete», «tormenta
    (kaya+wara)», «marejada (habo+rü)», «perla, cuenta brillante del mar»:
    vocabulario ACUÑADO para la simulación en junio de 2026 y etiquetado con
    un pedigrí que nadie citó. El corpus las usa como caquetías (hikoteya,
    tüma). Contarlas como lokono infla la columna de D11 en 27 y esconde 27
    caquetías inventadas. → `caquetío-hipotético`, con la etiqueta vieja en
    `notas`.
  · `wayunaiki-cogn` (7), `wayunaiki/lokono` (5), `taíno/lokono` (2): formas
    caquetías derivadas de una palabra hermana citada entre paréntesis en la
    glosa («anasa (< anasü Wayunaiki)»). Cuando la glosa cita la forma
    fuente → `caquetío-reconstruido` (y entran en la deuda de D11 fase 3,
    que pasa de 23 a más); cuando no cita nada (mülia, alaain, japü, manatü,
    karükera) → `caquetío-hipotético`.
  · `proto-arawakan` (2): `paratü` «trueque (raíz paa-)», `madunaka` «sequía
    (ma+duna)» — acuñaciones con morfología caquetía, sin notas →
    `caquetío-hipotético`. `proto-arahuaco` (3) con Payne 1991 en notas se
    queda como canónico.
  · `lokono-cogn` (1) `kanua` sin notas → `caquetío-hipotético`.
  · `jirajaroide-contacto` (7) → `jirajaroide`. `kalinago-caribe-overlay` (4)
    → `kalinago`. `taíno/caribe` (1) → `taíno`. `caquetío-hipotético/topónimo`
    (1) → `caquetío-hipotético`. En todos, lo que la etiqueta vieja decía va a
    `notas`.
  · `caribe-cháima`, `caribe-cumanagoto`, `español-colonial`: los puso D10 con
    su razón; son canónicos tal cual.

El conjunto canónico queda declarado en curiana_lexicon.FUENTES_CANONICAS y
un test lo vigila. Ni una forma ni una glosa se toca.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL

DRY = "--dry-run" in sys.argv
V = CL.VOCABULARIO_BASE
CITA_HERMANA = re.compile(r"\(<\s*\S+\s+Wayunaiki\)|\(<\s*\S+\)")

def destino(clave, e):
    f = e.get("fuente"); sig = e.get("sig") or e.get("es") or ""
    if f in ("lokono/proto-arawakan", "lokono/garifuna", "lokono-cogn", "proto-arawakan"):
        return "caquetío-hipotético", f"acuñación para la simulación sin cita, etiquetada `{f}`"
    if f in ("wayunaiki-cogn", "wayunaiki/lokono", "taíno/lokono"):
        if CITA_HERMANA.search(sig):
            return "caquetío-reconstruido", f"forma derivada de la hermana que cita la glosa, etiquetada `{f}`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu)"
        return "caquetío-hipotético", f"forma sin cita ni derivación declarada, etiquetada `{f}`"
    if f == "jirajaroide-contacto":
        return "jirajaroide", "etiqueta vieja `jirajaroide-contacto`: voz de contacto con el área jirajaroide"
    if f == "kalinago-caribe-overlay":
        return "kalinago", "etiqueta vieja `kalinago-caribe-overlay`: forma del registro caribe (overlay) del kalinago"
    if f == "taíno/caribe":
        return "taíno", "etiqueta vieja `taíno/caribe`: la voz circula también en caribe"
    if f == "caquetío-hipotético/topónimo":
        return "caquetío-hipotético", "etiqueta vieja `caquetío-hipotético/topónimo`"
    return None, None

plan = []
for k, e in V.items():
    nuevo, por = destino(k, e)
    if nuevo:
        plan.append((k, e.get("fuente"), nuevo, por))

from collections import Counter
print(f"{'clave':14} {'de':26} → {'a':24}")
for k, f, n, _ in plan:
    print(f"{k:14} {f:26} → {n:24}")
print("\nresumen:")
for (f, n), c in sorted(Counter((f, n) for _, f, n, _ in plan).items()):
    print(f"  {c:3d}  {f:26} → {n}")
if DRY:
    print("\n--dry-run: nada escrito"); sys.exit(0)

p = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
t = io.open(p, encoding="utf-8").read()
assert "FUENTES_CANONICAS" not in t, "ya aplicado"
hechos = 0
for k, f, n, por in plan:
    # la entrada empieza en `"clave": {` y su `"fuente": "..."` es la primera que sigue
    m = re.search(r'^(\s*"%s":\s*\{)' % re.escape(k), t, re.M)
    assert m, k
    ini = m.end()
    mf = re.compile(r'"fuente":\s*"%s"' % re.escape(f)).search(t, ini)
    assert mf and mf.start() - ini < 2500, (k, f)
    huella = f"F8 (2026-09-12): {por}"
    t = t[:mf.start()] + f'"fuente": "{n}"' + t[mf.end():]
    # notas: añadir o crear, dentro de la misma entrada
    fin = t.index("},", mf.start())
    seg = t[mf.start():fin]
    mn = re.search(r'"notas":\s*"', seg)
    if mn:
        i = mf.start() + mn.end()
        t = t[:i] + huella + " · " + t[i:]
    else:
        # ¿notas antes de fuente? buscar hacia atrás en la entrada
        seg2 = t[ini:mf.start()]
        mn2 = re.search(r'"notas":\s*"', seg2)
        if mn2:
            i = ini + mn2.end()
            t = t[:i] + huella + " · " + t[i:]
        else:
            fin = t.index("},", mf.start())
            t = t[:fin] + f', "notas": "{huella}"' + t[fin:]
    hechos += 1

# el conjunto canónico, declarado junto a capa_epistemica
ancla = "def capa_epistemica(fuente: str) -> Optional[str]:"
assert ancla in t
decl = '''# F8 (2026-09-12): el conjunto canónico de `fuente`. Cada valor es UNA lengua o
# UNA capa epistémica caquetía; las mezclas («lokono/garifuna», «wayunaiki-cogn»)
# eran pedigríes sin cita y se resolvieron entrada a entrada — ver
# 6-fusion/scripts/sanear_f8_resto.py, que imprime lo que hizo con cada una.
# Un test vigila que ninguna entrada salga de aquí.
FUENTES_CANONICAS = frozenset({
    "caquetío-atestiguado", "caquetío-reconstruido", "caquetío-hipotético",
    "caquetío-retroabstraido",
    "wayunaiki", "lokono", "taíno", "taíno-reconstruido", "kalinago", "paraujano",
    "jirajaroide", "proto-arahuaco",
    "caribe-cháima", "caribe-cumanagoto", "español-colonial",
})


'''
t = t.replace(ancla, decl + ancla, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print(f"\nre-etiquetadas {hechos} entradas; FUENTES_CANONICAS declarado")

# el test
pt = os.path.join(R, "curiana_sim", "tests", "test_capas_epistemicas.py")
tt = io.open(pt, encoding="utf-8").read()
if "FUENTES_CANONICAS" not in tt:
    tt = tt.rstrip("\n") + '''


def test_ninguna_entrada_sale_del_conjunto_canonico_de_fuentes():
    """F8 (2026-09-12). Había 25 valores de `fuente`; 23 eran mezclas
    («lokono/garifuna», «wayunaiki-cogn») que escondían acuñaciones sin cita
    bajo un pedigrí. Si hace falta un valor nuevo, se declara en
    FUENTES_CANONICAS con su razón — no se inventa en una entrada."""
    import curiana_lexicon as CL
    fuera = sorted({v.get("fuente") for v in CL.VOCABULARIO_BASE.values()} - CL.FUENTES_CANONICAS)
    assert not fuera, f"valores de `fuente` fuera del conjunto canónico: {fuera}"
'''
    io.open(pt, "w", encoding="utf-8", newline="\n").write(tt)
    print("test añadido")
