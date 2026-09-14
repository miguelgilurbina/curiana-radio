---
name: leer-fuente
description: Sacar el texto de una fuente del proyecto lingüístico caquetío venga como venga — PDF con capa de texto, PDF escaneado (OCR con tesseract), página que hay que ver en imagen, tabla que el extractor desordena, o manuscrito que sólo se lee con visión (Neira y Ribero). Usar cuando se pida extraer, pasar a texto, hacer OCR, transcribir, renderizar o verificar en imagen una página, leer un manuscrito, descargar una obra (archive.org, IIIF, Wikisource) o decidir dónde se guarda. Qué preguntarle a la fuente una vez leída está en minar-fuente.
---

# Leer una fuente

Esta skill es la **técnica de extracción**: cómo pasar de un PDF, un escaneo o
una imagen a un texto del que uno se pueda fiar, y dónde dejarlo. Lo que se le
pregunta a ese texto, cómo se mide la ortografía antes de contar y a qué esfera
va cada hallazgo están en **`minar-fuente`**, y no se repiten aquí. Para los
topónimos de Esteves, **`campana-toponimos`** §2.

Cada paso está porque saltárselo costó un error que aquí se nombra. Las reglas
de `CLAUDE.md` mandan; en especial la 1 (ninguna cifra a mano), la 5 (nada
valioso muere en el scratchpad) y la 6 (un cero hay que verificarlo).

## 0. Diagnóstico: ¿qué tienes delante?

| Lo que llega | Herramienta | Qué sale y dónde |
|---|---|---|
| PDF con capa de texto | `pdftotext` (Poppler, en `/mingw64/bin`) | `fuentes_caquetios/OBRA.txt` |
| PDF escaneado sin capa | `curiana_sim/ocr_fuente.py` (tesseract) | `fuentes_caquetios/OBRA.ocr.txt` |
| Tabla, glosa que decide un nivel, forma que se va a citar | `pymupdf`: renderizar la página (§3) | un PNG desechable; la **lectura** va a `6-fusion/` |
| Manuscrito o cursiva sin OCR posible | `pymupdf` + visión, recorte a recorte (§4) | un YAML de transcripción en `6-fusion/` |
| Texto ya publicado en la web (Wikisource) | descarga + limpieza por script (§6) | `fuentes_caquetios/OBRA_wikisource.txt` |

En esta máquina **no hay `pdftoppm`**: lo anotaron las sesiones de ecología y
creencia y el handoff del 2026-09-11. Para ver una página se usa `pymupdf`, que
sí está (`import pymupdf`; `import fitz` funciona, pero avisa de que está
deprecado).

Para saber si un PDF tiene capa, extrae una página del cuerpo y mírala:
`pdftotext -f 40 -l 40 -enc UTF-8 fuentes_caquetios/OBRA.pdf -`. Ojo: que
`pypdf` devuelva vacío no quiere decir que no haya capa.

## 1. PDF con capa de texto

```bash
pdftotext -enc UTF-8 "fuentes_caquetios/OBRA.pdf" "fuentes_caquetios/OBRA.txt"
pdftotext -layout -enc UTF-8 -f 438 -l 439 "fuentes_caquetios/OBRA.pdf" -   # tablas
```

- **`pdftotext`, no `pypdf`.** Arcaya sale vacío con `pypdf` y da 467 KB con
  `pdftotext`, y `pypdf` parte `Todariquiba` en `T odariquiba` las siete veces.
  La medición entera está en `minar-fuente` §1.
- **Guarda el `.txt` junto al PDF**, en `fuentes_caquetios/` y con el mismo
  nombre, como están Perea y Fabo. Un texto que se extrajo en el scratchpad
  obliga a la sesión siguiente a extraerlo otra vez, y a veces con otro
  extractor que da otro texto.
- **Las tablas se extraen dos veces**, con y sin `-layout`, y se comparan. Así
  se recuperaron `tapári`/`tarágla` en Jahn pp. 438-439.
- **Una tabla de tres columnas se desplaza por filas, no sólo por columnas, y
  sigue pareciendo una tabla válida.** En el apéndice de Jahn la columna de
  comparandas baja una fila desde «Piedra», e `iba` cae bajo «Estrella» (commit
  `9125021`). Lo delata esto: **si una forma sale repetida en dos columnas, hay
  desfase** mientras la imagen no diga lo contrario. Pasó con `gagáp` en la
  p. 390, donde el OCR se había comido `shoh` (commit `32fae51`). Nada de una
  tabla así se cita sin verla en imagen.
- **Si parseas columnas, corta por el hueco de dos espacios, no por la
  posición.** La cabecera va centrada sobre su columna, y cortar por posición
  partía las palabras (`teitschir|u`, commit `bed4ec4`).
- **Una lista de varias columnas le pega la glosa al vecino.** En el verbo de
  Perea, «a-paù-n = matar ù, a-cakù-dù - navivar» son **dos** verbos. Por eso
  `6-fusion/scripts/minar_perea_verbos.py` se leyó a mano, página por página, y
  no con regex: cuando la lista se desplaza, el regex mezcla entradas sin avisar.
- **Cuenta la página impresa, no la del PDF.** Si el desfase es constante se
  calcula una vez (Antczak: pdf + 130; Esteves: + 6, + 25 o + 55 según el
  tomo). Si el escaneo **repite o salta pliegos**, el desfase deriva y ya no se
  puede sumar una constante. A Perea le faltan 29 páginas y repite otras dos y
  tres veces, así que se lee el número impreso de cada página.

## 2. PDF escaneado: OCR

```bash
cd proyecto-linguistico-caquetío
python curiana_sim/ocr_fuente.py fuentes_caquetios/OBRA.pdf --lang spa
python curiana_sim/ocr_fuente.py fuentes_caquetios/OBRA.pdf --lang ita --paginas 40-60 --offset -8
```

- **La salida va sola a `fuentes_caquetios/OBRA.ocr.txt`**, con un marcador
  `=== pdf N · impresa N ===` por página. No la mandes al scratchpad: la pasada
  de Oliver del 2026-08-17 se quedó en uno y se perdió, y hubo que repetir el
  OCR («esta vez guardado en el repo»).
- **Con `--offset`, el marcador ya dice la página impresa.** Mide el desfase
  antes, con dos o tres páginas numeradas.
- **`--rotar auto` viene activado, y no se quita sin una razón.** El Apéndice E
  de Oliver tenía páginas invertidas: dieron 2.850 caracteres de basura y cero
  códigos de sitio. La pista fue leer `YNYNOVUVd` como `PARAGUANA` del revés.
- **`--psm 4` o `--psm 6`** para las listas a dos columnas; **`--dpi 400`**
  para la letra chica. `--lang` admite varios idiomas a la vez (`spa+eng`).
- Al terminar, el script lista las páginas **casi vacías**. Míralas antes de
  concluir que la fuente no dice nada: puede ser una portadilla o un render
  fallido (regla 6).
- tesseract no está en el PATH, y el script lo busca en `Program Files`. Si no
  lo encuentra, dice cómo instalarlo. Instalarlo es cosa de Miguel.

⚠️ **El OCR es una pista, no una cita**, y lo dice la cabecera del script. Los
errores caen justo en lo que importa: en Esteves, `Giiica` por Güica y
`genero>a` por generosa. **Y el OCR se come el paréntesis de cierre**: por eso
el extractor de glosas de Esteves perdía seis, entre ellas el «Borojó es
chibcha» que acabó en un issue (commit `ba31481`). Si una glosa va a decidir un
nivel, una capa o una decisión, **se mira la imagen** (§3). Borojó se verificó
en la p. 90 antes de publicar la decisión.

El OCR hecho por otros cuenta igual. El `.txt` de archive.org de Fabo 1911 se
lee, pero trae `CASTEEEANO` y `Eeña` y **desplaza las columnas**: la tabla de la
p. 100 sale como tres listas seguidas, y las de las pp. 108 y 111-112 se
transcribieron de la imagen (`6-fusion/scripts/minar_fabo_1911_achagua.py`).

## 3. Ver una página en imagen (pymupdf)

Hace falta para verificar una forma antes de citarla, para leer una tabla que
el OCR desordena y para transcribir lo que no tiene OCR.

```python
import pymupdf

doc = pymupdf.open(ruta)          # un PDF, o un JPG abierto como documento
pagina = doc[i]                   # índice 0-based del PDF, no la página impresa

# Escala. En un PDF: dpi / 72. En un JPG: píxeles / puntos de la página:
#   factor = pymupdf.Pixmap(ruta).width / pagina.rect.width
factor = 300 / 72

r = pagina.rect                   # coordenadas en PUNTOS, no en píxeles
cuarto = pymupdf.Rect(r.x0, r.y0, r.x0 + r.width / 2, r.y0 + r.height / 2)
pix = pagina.get_pixmap(matrix=pymupdf.Matrix(factor, factor), clip=cuarto)
pix.save(salida_png)
```

- **Recorta a resolución nativa, no reduzcas la página entera.** Una página
  entera al tamaño de la pantalla no deja leer los diacríticos; un recorte
  (`clip`) al factor nativo, sí. En Neira y Ribero el factor medido es
  **4,167 px/pt**: 2787 px sobre 668,88 pt, porque el JPG declara 300 ppp. El
  factor se calcula, no se da por supuesto.
- **`clip` va en puntos de la página.** Si calculas el recorte en píxeles de la
  imagen, divídelo por el factor, o recortarás el cuarto equivocado.
- **El PNG se tira; la lectura no.** El recorte puede vivir en el scratchpad,
  porque se regenera en un segundo desde la fuente. Lo que leíste en él va al
  YAML de `6-fusion/` o a la nota de la fuente, con su página.
- **Deja constancia de lo verificado**: «✅ Verificado en imagen, p. 90» en el
  commit o en la entrada. Y declara también lo que se citó sin verlo: la
  revisión pre-era 2 pudo contar con un grep las correspondencias de Jahn
  «sin ver en imagen» porque estaban escritas así.

## 4. Manuscritos por visión

Protocolo destilado de Neira y Ribero 1762: 102 pliegos JPG con la cursiva de un
copista de 1788 y sin OCR posible, que un escriba (agente Opus 5) leyó en dos
pasadas el 2026-09-12. La ficha `4-fuentes/neira-ribero-1762.md` y la cabecera
de `6-fusion/achagua_neira_ribero_1762.yaml` son el ejemplo completo.

1. **Primero el índice, con hojas de contacto.** Son miniaturas de muchos
   pliegos en una imagen, y sirven para localizar las secciones y las cabeceras
   de letra, no para leer. De ahí salió un índice de pliegos (tapas 1-5, arte
   7-27, vocabulario 28-98, cabeceras B 40 · C 44 · D 52…), que va a la ficha
   **antes** de transcribir nada. Y se corrige cuando la lectura lo desmiente:
   la L no empezaba en el 73 sino al pie del 71, y esta copia **no trae** la
   parte achagua-castellano que anuncia la portada.
2. **Busca la clave de lectura en la propia fuente.** El copista escribe la `r`
   con un glifo que parece una `z`, y lo dice él mismo en «Pronunciación»
   (pliego 7): *«la R no la hacen erre, sino r como los Españoles»*. Dar con eso
   costó media hora; sin saberlo, se transcribe `Vregizzayi` por `Vregirrayi`.
   La clave va a `meta.ortografia_del_copista` antes de la primera entrada.
3. **Un recorte de media página a resolución nativa**, unas doce entradas por
   recorte: cuatro recortes por pliego, porque cada JPG trae dos páginas. Si una
   línea no se decide, otro recorte a 2-3× sobre esa línea.
4. **Calibra contra formas conocidas antes de transcribir el resto.** Las 34
   voces achagua de Jahn/Fabo se buscaron primero, una a una, con veredicto
   `coincide` / `difiere` / `no-esta`. La calibración mide a la vez al lector y
   la cadena de transmisión, y fue lo que destapó que Jahn tenía *agua* y *río*
   corridos un escalón («Agua — Vni», «Mar — Manoa»).
5. **Transcribe con ancla y con la duda a la vista.** Cada entrada lleva pliego y
   lado. La grafía del copista va entera: normalizar es otro paso, y se declara.
   Una lectura dudosa va entre `[corchetes]`, y cada duda con nombre entra en una
   lista `dudas` con su campo `resuelta:` (`sí` / `parcialmente`). Después, el
   generador del lexicón convirtió los corchetes en «⚠️ duda de lectura» dentro
   de `notas`.
6. **Dos pasadas.** La segunda cierra los huecos, vuelve sobre las dudas y
   corrige a la primera. Pasó con «Diente»: la primera pasada lo dio por ausente
   «verificado en 52, 53, 56 y 57», pero los pliegos 54 y 55 no se habían leído,
   y estaba en el 55. Un «no está» sólo vale si la letra entera está leída
   (regla 6 al revés: ese cero medía la lectura, no la fuente).
7. **La cobertura la mide un ensamblador, no la escribes tú.**
   `6-fusion/scripts/ensamblar_achagua_neira_ribero.py` cuenta los pliegos
   leídos, los **huecos** entre el primero y el último, las entradas por letra,
   la calibración y las dudas, y lo reescribe en `meta.cobertura`. Mide los
   huecos en vez de creerse la lista de pliegos leídos. Tiene `--check`, que
   mide sin escribir, y al guardar comprueba que el YAML reparsea con las mismas
   entradas. La ficha de la fuente **apunta** a esas cifras en vez de copiarlas
   (regla 1).
8. **Toda forma queda marcada como transcripción por visión**: en la cabecera
   del YAML, en la ficha y en cada `notas` del lexicón, con «verificar en imagen
   antes de citar la forma como exacta».

Una transcripción larga la puede hacer un agente aparte, como el escriba de
Neira y Ribero, que se lanzó así a petición de Miguel. Pero escribe en el YAML
de `6-fusion/`, no en su scratchpad, y el commit lo declara. Un servicio de HTR
externo (Transkribus tiene modelos para la cursiva española del XVIII) obliga a
subir las imágenes fuera del repo: eso lo decide Miguel.

## 5. Claves ortográficas ya medidas, por autor

Antes de leer una obra de esta lista, lee su clave. Antes de leer una obra
nueva, búscale la suya (§4.2) y añádela aquí.

| Fuente | Qué hay que saber | De dónde |
|---|---|---|
| **Perea y Alonso 1942** | Clave panfonética (p. CI): `c` = /k/ siempre, `q` = k, `ù` = ü alemana, `x` = sh, `cx` = ch, `w` inglesa. **El OCR lee como `л` (ele cirílica) uno de sus glifos, y `л` = RR**: `Cxaлúa` = Charrúa, `cuлu` = `curru` 'no'. **Las geminadas no tienen valor** (p. 546: l/ll, d/dd y t/tt «alternan sin motivo aparente»). Y la r/l alterna: `-ruccu ~ -luccu` 'en' choca con `luccu` 'persona' | ficha; commit `e1aa50f` |
| ↳ lo que costó | `fonemizar()` no tenía la `ù` en su clase de letras y **la borraba**; con eso y las geminadas, Perea pasaba el filtro fonotáctico al 52 %. Se arregló **en el instrumento y sólo para Perea**, porque en wayuu la geminada contrasta | `curiana_fonotactica.py`, `tests/test_fonotactica.py` |
| **Neira y Ribero 1762** | Glifo tipo `z`/`x` = `r`, y doble = `rr`. `ʃ` = s. `V` y `J` iniciales ante consonante = `u` e `i` (`Vni` = uni). `y` e `i` alternan. Tildes prosódicas puestas a bulto. Tilde nasal por n/m omitida. `q.` = que, `p.a` = para, `vel` = o | `meta.ortografia_del_copista` del YAML |
| **Fabo 1911** | El OCR de archive.org desplaza las columnas de las tablas, que se transcriben de la imagen (pdf 110-114 = impresas 108-112). La ortografía es la de Fabo (`y`/`i`, `ck`), no la del manuscrito. Y es de segunda mano, con un error medido (su *mena* 'agua' es el mar) | ficha; `minar_fabo_1911_achagua.py` |
| **Jahn 1927** | Capa OCR buena en el cuerpo e ilegible en el frontispicio. Las tablas a dos columnas se desalinean entre saltos de página, y el apéndice comparado se desplaza **por filas** (§1) | `4-fuentes/jahn-1927.md` |
| **Esteves 1989** | OCR propio en el repo; `ü` sale `ii`, el paréntesis de cierre desaparece, y la cabecera no coincide con el mapa (BUCHUHACO / Buchuaco) | `campana-toponimos` §2 |
| **Antczak 2017**, **Oviedo y Baños** | Acentos descompuestos (`Caquet´ıo`); `caiquetía`, `Coriana` | `minar-fuente` §2 |
| **Pané c. 1498** | No hay original: castellano ← italiano (Ulloa 1571) ← castellano perdido. Las grafías son las de esa cadena, y `behique`, `bohío` o `areíto` no salen con esa forma | `4-fuentes/pane-c1498.md` |

Los `fonemizar()` de los scripts de barrido sirven para **buscar**, no para
hacer lemas: colapsan `ce→se`, al revés que el lema fonémico canónico de D5
(commit `3c0a1ce`). El lema de una entrada se fija en la fusión
(`fusionar-propuesta` §5).

## 6. Descargar, y dónde se guarda

**Descargar lo decide Miguel.** Las comparandas del 2026-09-12 entraron después
de su «adelante con la descarga». Hasta entonces, la obra se localiza (URL,
tamaño, si tiene OCR) y se anota en la revisión o en el handoff.

| Origen | Cómo se hizo | Lo que salió mal, o conviene saber |
|---|---|---|
| **archive.org** | El PDF y el texto OCR del ítem (Fabo: `b24853616`) | El OCR del ítem sirve para localizar, no para leer las tablas (§2) |
| **IIIF** (Real Biblioteca) | Imagen a imagen desde el manifiesto (102 lienzos), a resolución completa, y montadas en PDF con `pymupdf` | La copia de la Library of Congress dio 403. Se leen las imágenes de resolución completa: no bajes miniaturas |
| **Wikisource** | Las subpáginas (los 29 capítulos de Pané), con el marcado wiki quitado por script | La ficha dice qué edición o traducción publica Wikisource |
| **Detrás de una verificación de navegador, o un servidor que rechaza la conexión** | No se fuerza | Meléndez Lozano 1997 (IAI) y el libro de la UNEFM quedaron para que Miguel los baje a mano |
| **De pago** | Se anota «comprar» | de Goeje 1928, Granberry & Vescelius 2004 |

**Dónde vive (D8, #37, cerrada el 2026-09-12).** Lo de acceso abierto y poco
peso va a git, en `fuentes_caquetios/`: Fabo con su PDF y su `.txt`, y Pané.
**Lo pesado vive en OneDrive**, con su línea en `.gitignore` (Neira y Ribero:
200 MB de JPG y PDF), y **la ficha lo dice** en `local:` («SOLO EN ONEDRIVE, no
en git»). El nombre del fichero es `Autor_Año_Titulo_Corto.pdf`, con el `.txt`
o el `.ocr.txt` al lado.

Cuando entra la obra:

1. **La ficha en `4-fuentes/<slug>.md`**, con `local`, `capa_texto`,
   `descargado`, `origen_digital` y `estado_minado: sin-minar`, y dos secciones
   que la sesión siguiente agradece: **«Qué preguntarle»** y **«Cómo se lee»**.
2. **Comprueba que `local:` apunta a un fichero que existe.** El handoff del
   2026-09-11 encontró tres fichas (Brinton, Perea y el apéndice A de Oliver)
   cuyo `local:` no resolvía aunque el PDF estaba en el repo.
3. **`python curiana_sim/generar_bibliografia.py`.** Si no, el guardián
   «bibliografía al día» se pone en rojo. Pasó con el índice de Neira y Ribero,
   y costó un commit aparte (`5da70ba`).
4. **Lo que midas al descargar, márcalo como tal.** Si cuentas algo («`achagua`
   100 veces», una frase sobre `-are`), escribe **«medido al descargar, sin leer
   todavía»**. La `-are` «propia y exclusiva» de Fabo resultó ser, leída, un
   patrón toponímico.

## 7. Las trampas que costaron algo

| Trampa | Qué pasó |
|---|---|
| `pypdf` en vez de `pdftotext` | Arcaya salió vacío y `Todariquiba`, partido |
| Tabla leída sin mirar la imagen | filas desplazadas desde «Piedra» en Jahn; `gagáp` en dos columnas; la `kapauje` «flecha» era «flecha con hierro» |
| OCR tomado como cita | el paréntesis de cierre desaparecido escondía seis glosas de Esteves |
| OCR en el scratchpad | la pasada de Oliver del 2026-08-17, perdida |
| Páginas invertidas | Apéndice E de Oliver: basura con forma de texto |
| Regex sobre una lista desplazada | glosas pegadas al verbo vecino en Perea |
| Clave de lectura sin buscar | el glifo `z` = `r` de Neira; la `л` = `rr` de Perea |
| «No está» sin leer la letra entera | «Diente» estaba en el pliego 55 |
| Desfase pdf→impresa sumado a ciegas | Perea repite y salta pliegos, y el desfase deriva |
| Obra nueva sin regenerar la bibliografía | guardián en rojo; commit `5da70ba` |
| `local:` sin comprobar | tres fichas apuntaban a un PDF inexistente |
