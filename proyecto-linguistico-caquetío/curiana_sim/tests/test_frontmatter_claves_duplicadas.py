"""Una clave repetida en el frontmatter de una nota de `4-fuentes/` tiene que PARAR.

`yaml.safe_load` no avisa: se queda con la última y sigue, así que la nota se
lee «bien» y dice otra cosa. Pasó el 2026-09-21 al mezclar dos campañas que
escribieron bitácora en la misma obra: `main` no tenía `cobertura`, cada rama la
añadió en una línea distinta, git aceptó las dos SIN conflicto, y
`oliver-1989-cap2` quedó con dos `cobertura` y dos `minado` — con los
guardianes en verde. El chequeo vive en `generar_bibliografia.frontmatter()`
porque es quien ya lee TODAS las notas, así que lo vigila el guardián
«bibliografía al día» sin añadir uno nuevo.

La mitad son negativos, como en `test_lengua.py`: un chequeo que nunca falla y
uno que no mira nada se ven igual desde fuera.
"""
import os

import pytest

from generar_bibliografia import (
    FUENTES,
    ClaveDuplicada,
    claves_duplicadas,
    frontmatter,
    main,
)

LIMPIO = 'tipo: fuente\nobra: "Una obra"\ncobertura: "cap. 1"\nminado: 2026-09-21\n'
# El caso real, tal y como quedó la nota: dos ramas, dos líneas, cero conflicto.
MEZCLADO = ('tipo: fuente\nobra: "Una obra"\n'
            'cobertura: "lo que dijo la rama A"\nprioridad: alta\nminado: 2026-09-21\n'
            'cobertura: "lo que dijo la rama B"\nverificado: 2026-09-21\nminado: 2026-09-21\n')


def test_un_frontmatter_limpio_no_tiene_repetidas():
    assert claves_duplicadas(LIMPIO) == []


def test_detecta_las_dos_claves_del_caso_real_y_en_orden():
    assert claves_duplicadas(MEZCLADO) == ["cobertura", "minado"]


def test_una_clave_anidada_con_el_mismo_nombre_no_cuenta():
    # `sostiene` lleva dentro claves propias; sólo el primer nivel se repite.
    texto = "minado: 2026-09-21\nsostiene:\n  minado: 3\n  cobertura: 1\ncobertura: x\n"
    assert claves_duplicadas(texto) == []


def test_el_valor_no_se_confunde_con_una_clave():
    # Una URL o una hora dentro del valor llevan «:» y no son clave.
    texto = 'acceso: "https://ejemplo.org/obra: tomo 1"\nnota: "cobertura: parcial"\ncobertura: x\n'
    assert claves_duplicadas(texto) == []


def test_frontmatter_se_niega_a_leer_la_nota_mezclada(tmp_path):
    nota = tmp_path / "obra-mezclada.md"
    nota.write_text(f"---\n{MEZCLADO}---\n\ncuerpo\n", encoding="utf-8")
    with pytest.raises(ClaveDuplicada) as e:
        frontmatter(str(nota))
    assert "cobertura" in str(e.value) and "obra-mezclada.md" in str(e.value)


def test_frontmatter_lee_la_nota_limpia_como_siempre(tmp_path):
    nota = tmp_path / "obra-limpia.md"
    nota.write_text(f"---\n{LIMPIO}---\n\ncuerpo\n", encoding="utf-8")
    assert frontmatter(str(nota))["cobertura"] == "cap. 1"


def test_el_guardian_sale_en_rojo_y_dice_que_nota(tmp_path, monkeypatch, capsys):
    import generar_bibliografia as G
    (tmp_path / "obra-mezclada.md").write_text(f"---\n{MEZCLADO}---\n", encoding="utf-8")
    monkeypatch.setattr(G, "FUENTES", str(tmp_path))
    assert main(["--check"]) == 1
    assert "obra-mezclada.md" in capsys.readouterr().out


def test_ninguna_nota_del_repo_trae_una_clave_repetida():
    # El canon de hoy: si esto se pone rojo, una mezcla acaba de duplicar algo.
    malas = {}
    for nombre in sorted(os.listdir(FUENTES)):
        if not nombre.endswith(".md"):
            continue
        with open(os.path.join(FUENTES, nombre), encoding="utf-8") as fh:
            texto = fh.read()
        if not texto.startswith("---"):
            continue
        cab = texto[3:].split("\n---", 1)[0]
        rep = claves_duplicadas(cab)
        if rep:
            malas[nombre] = rep
    assert malas == {}
