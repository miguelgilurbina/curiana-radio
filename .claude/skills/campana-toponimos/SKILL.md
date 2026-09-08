---
name: campana-toponimos
description: Procesar topónimos de la Kaketiana (Paraguaná, Golfete de Coro, Falcón llano, islas ABC) hasta el canon, desde el gazeteer de Esteves 1989, desde el dictado de Medina Colina o desde un barrido del mapa vivo. Usar cuando se pida sumar, resolver, procesar o cerrar topónimos, seguir la cola de Esteves, colgar una lectura de un topónimo, o barrer el mapa topónimo por topónimo.
---

# La campaña de topónimos

Protocolo destilado de los lotes 1 y 2 (2026-09-06/07: 19 topónimos de Esteves
al canon) y de lo que costó llegar a ellos. Complementa a `minar-fuente`: aquel
dice cómo leer una obra; este dice cómo un nombre de lugar entra al canon y
con qué voces. Las reglas de CLAUDE.md mandan; en especial la 1 (cifras
medidas), la 3 (precontacto ≠ colonial), la 5 (minar propone, el humano
fusiona) y la 6 (un cero hay que verificarlo).

## 0. La mesa de trabajo

`proyecto-linguistico-caquetío/6-fusion/TOPONIMOS_POR_FUENTE.md` — generada por
`curiana_sim/juntar_toponimos.py`. Trae todos los topónimos que el proyecto
ha tocado, por obra, con cuatro marcas: ★ en el canon, ≡ en el índice de
Esteves, ◆ en el mapa de Miguel, ⌂ en `asentamientos.yaml`. **Se regenera, no
se edita.** Antes de tocar nada:

```bash
cd proyecto-linguistico-caquetío
python curiana_sim/juntar_toponimos.py
```

Las colas viven en `6-fusion/`: `toponimos_esteves_indice.yaml` (el índice
del libro, `por_procesar` / `ya_registrados`), `toponimia_paraguana_miguel.yaml`
(lecturas y `cola_de_mapa` de Miguel) y lo que el dictado de Medina Colina
manda (`medina_colina_dictado.yaml`, campo `cruce.toponimos` y
`propuesta.toponimo_a_la_cola`).

## 1. Elegir el lote

Un lote son 10-20 nombres con un criterio dicho. Los que funcionaron:
**los que Miguel tiene vistos en el mapa y además están en Esteves** (glosa +
referente vivo), y **los que una pregunta abrió** (los «caribe insular» tras
B.6). Anota el criterio: irá al commit.

## 2. Llegar a la página, y desconfiar de la lectura anterior

Esteves 1989 tiene OCR en el repo (`fuentes_caquetios/Esteves_1989_..._N.ocr.txt`,
marcador `=== pdf N · impresa N ===`). El «impresa» del marcador es el del PDF:
**la página del libro es pdf + 6 (PDF 1), + 25 (PDF 2), + 55 (PDF 3)**. Las
entradas van por orden alfabético, pp. 11-67.

```bash
grep -n -i -A14 "^ *NOMBRE\b" fuentes_caquetios/Esteves_1989_Toponimos_Paraguana_*.ocr.txt
```

- **Un cero mide tu consulta.** Esteves escribe BUCHUHACO donde el mapa dice
  Buchuaco; el OCR da `Giiica` por Güica y `genero>a` por generosa. Probar
  variantes con h, con ü, con vocal interior cambiada; buscar `NOMB` en vez
  de `NOMBRE`.
- **Lee la entrada entera, no la glosa.** Las entradas traen: referente y
  municipio, censo de 1881 (casas y vecinos), forma primitiva en «antiguos
  papeles» (Cocodito 1590, Charaide, Maicuare, Baraivere), una o dos
  etimologías populares que el propio Esteves relativiza, y a veces el
  estrato que él le atribuye. Todo eso entra en la entrada, cada cosa en su
  campo.
- El OCR es pista, no cita: si la glosa va a decidir un nivel, mira la imagen.

Para otras fuentes (Castellanos, Zavala, van Buurt) vale `minar-fuente` §1-3.

## 3. Cruzar antes de segmentar

Con el nombre en la mano, mide:

| Contra | Dónde | Qué te dice |
|---|---|---|
| el canon | `2-lengua/toponimos.yaml` (o la mesa, ★) | si ya existe, es una **lectura** nueva, no una entrada nueva |
| el lexicón | `curiana_lexicon.py` VOCABULARIO_BASE, `lexicon_zavala.py` | morfemas atestiguados con los que cerrar la ecuación |
| los morfemas despejados | `2-lengua/morfemas.yaml` (`-are`, `-bacoa`, `-ebo`, `bana`, `kiba`, `-dito`, `-uco`…) | recurrencia, que es lo que sube de nivel |
| el índice de Esteves | la mesa, ≡ | si está, tiene página |
| los nodos | `3-mundo/asentamientos.yaml`, ⌂ | existencia y época: eso NO se decide aquí |
| el mapa de Miguel | la mesa, ◆ | referente vivo; su lectura va en `lecturas` |

`python curiana_sim/juntar_toponimos.py` ya hace estos cruces; para un nombre
suelto basta `grep -n -i "nombre" 6-fusion/TOPONIMOS_POR_FUENTE.md`.

## 4. Segmentar y decidir el nivel

La escala está en `lexicon_toponimos.py` y en `2-lengua/toponimia.md`; así se
aplicó en los lotes:

| Nivel | Qué hace falta | Ejemplo del lote |
|---|---|---|
| **A** | la fuente segmenta y glosa, y **todos** los morfemas ya estaban atestiguados por otra fuente | Judibana: judi+bana, Esteves y Zavala |
| **B** | un morfema nuevo o despejado, con **recurrencia ≥ 2** y glosa consistente; el resto atestiguado | Abudure (dabuda+ure), Buchuhaco (buche+aco: aco en Guachaco también) |
| **C** | cierra la mitad de la ecuación, o es un fitónimo sin componer, o la fuente da la segmentación con morfemas de otra lengua | Cocodite (-dito sí, coco- no), Caseto (planta), Maitiruma («caribe insular» según Esteves), Supí (dos glosas en pugna) |
| **descartado** | la fuente da referente y anécdota pero **ninguna glosa**, y ningún morfema conocido alinea | Charaima, Jacuque, Elegüey, Maragüey, Jamaica |

- «Descartado» = sin etimología despejable, **no** «no existió». La existencia
  y la época se juzgan en `asentamientos.yaml`.
- **Un nombre que sigue vivo es dato** (Miguel, 2026-09-07). Que Miraca se
  llame igual desde 1538, que Capatárida y Zazárida sigan en el mapa, o que
  Uarayadito conserve en 2026 lo que el censo de 1881 escribió Sarayadite, es
  continuidad de asentamiento aunque no haya etimología: va en `observacion`
  con la cadena de formas fechadas, y el descartado se registra con ella. Y
  a veces el mapa es más fiel que el libro: Yabuquiva conserva la b del étimo
  yabo que la cabecera de Esteves (Yauquiba) perdió.
- **Antes de decir que un nombre del mapa no está en la fuente**, permutar la
  inicial (j~s~u~h: Jarayadito / Sarayadite / Uarayadito), b~v~p (Barunú /
  Parunu), r~b (Guacurebo / Guacubero) y la terminación (Cayeruba / Cayerúa /
  Cayerda), y buscar por la raíz. Los ocho «fuera de Esteves» del lote 4
  estaban todos.
- Un etnónimo con territorio atestiguado (Amuay) entra en C por el etnónimo
  aunque la glosa no valga.
- Los conflictos de glosa entre fuentes **no se resuelven cambiando la glosa**:
  la de la fuente del registro va en `glosa_fuente`, la otra en `lecturas`
  como `glosa-fuente`, y el conflicto se declara (Supí).
- Regla 3: un censo de 1881, un título de composición de 1740 o un papel de
  1590 fechan el **documento**, no el nombre.
- **Y b~h** (2026-09-07): Esteves escribe *Capuhana* lo que Zavala escribe
  *capubana* («con hache intercalada para deshacer el diptongo», p. 26). Y
  el mapa vivo permuta más: Guaydabacos / Guaidabacoa, Cividual / Sibidigual,
  Varacara / Baracara, Sibarigua / Sabarigua. `barrer_mapa.py` aplica la
  permutación laxa y una distancia de 1-2 antes de llamar «nuevo» a un
  nombre; lo que sale como `aproximado` se revisa a mano, no cuenta.

## 5. La tercera voz: `lecturas`

Esquema y reglas en `2-lengua/datos-de-lengua.md` §«La tercera voz». Lo que
decidieron los lotes:

- **Toda etimología popular que Esteves recoge entra**, con `veredicto` y con
  su frase («total desacuerdo con tan expeditivo procedimiento», «un tanto
  fantasiosa», «hilarante»): así nadie la re-investiga.
- **La lectura de Miguel** entra como `testimonio-residente` con su nombre y
  `eje` (`referente` casi siempre: ubicación, rasgo dominante, geolocalización).
  Que un nombre esté en su mapa va en `observacion` («en el mapa vivo»), no en
  una lectura por nombre.
- **Un estrato atribuido por un autor es una lectura suya, no un dato.** Se
  escribe «según Esteves» en `clase` u `observacion`, y si hay evidencia en
  contra se cita (B.6: `6-fusion/oliver_324_caribes.yaml` §5). «Caribe» en
  crónica es categoría política; «caribe insular» es una lengua arahuaca.
- **Nombres transplantados** (Jamaica, la casa grande de una hacienda) se
  descartan con esa razón: no son toponimia indígena local.
- La hipótesis del proyecto va como `hipotesis`, `quien: proyecto`, con lo que
  la haría subir. Nunca sin veredicto o sin condición.

## 6. Escribir la entrada — en el módulo, nunca en el YAML

`2-lengua/toponimos.yaml` es **generado**. Se edita
`curiana_sim/lexicon_toponimos.py` (NIVEL_A / NIVEL_B / NIVEL_C / DESCARTES) y
se regenera; un test lo vigila y la trampa está en CLAUDE.md.

- **`id` explícito, el siguiente libre** (`grep -o 'toponimo-0[0-9][0-9]' curiana_sim/lexicon_toponimos.py | sort | tail -1`). Los ids son estables: otros archivos los citan. Nunca renumerar.
- `fuente` es el id de la bibliografía; `pagina`, la del libro. El migrador
  los mete en `procedencia`.
- Los descartados van en un grupo por razón con `fuente`, `ids` y `paginas`
  del grupo; la glosa o el referente, entre paréntesis dentro de la forma
  (el migrador lo separa a `glosa_fuente`).
- `forma` en minúscula con la tilde de la fuente (supí); la grafía de
  cabecera de Esteves si difiere del mapa se anota en `observacion`.

## 7. Regenerar, validar, cerrar la cola

```bash
cd proyecto-linguistico-caquetío/curiana_sim
python migrar_toponimos.py            # el canon
python compilar_lengua.py --check     # ids, procedencia, niveles, lecturas
python -m pytest tests/test_lengua.py -q
python juntar_toponimos.py            # la mesa
python generar_bandeja.py && python generar_tablero.py --gh
python guardianes.py --rapido
```

Y el índice de Esteves: cada nombre procesado pasa de `por_procesar` a
`ya_registrados` con `canon:` y `lote:`; `meta.ya_en_canon` y
`meta.por_procesar` se recuentan (un script de tres líneas, no a mano).

## 8. Bitácora y commit

En la nota de la fuente (`4-fuentes/esteves-1989.md`), una sección por lote:
qué criterio, qué entró, **qué dejó** (morfemas nuevos con recurrencia,
etimologías populares registradas, datos para otras colas como la auditoría de
tildes). En `1-plan/SIGUIENTE_TANDA.md`, el estado de B.5. En el commit: qué
se preguntó, qué se encontró, qué **no**, y la deuda nueva.

## 9. Lo que viene: el diccionario de Medina Colina, y barrer el mapa

**El diccionario.** *Del Habla Paraguanera* (Medina Colina, 2ª ed. 2013) es un
libro físico de Miguel que entra por **dictado curado**: el protocolo del
dictado, sus filtros y sus criterios están en
`4-fuentes/medina-colina-sxx.md` y el registro en
`6-fusion/medina_colina_dictado.yaml`. De ahí salen topónimos por tres vías,
y las tres desembocan en esta campaña:

1. **Una voz que es topónimo en Esteves** (saruro, chuchube, guachaco): el
   escriba lo anota en `cruce.toponimos` («= SARURO en la cola de Esteves»).
   Al procesar ese nombre, Medina entra como **segunda atestación viva** en
   `lecturas` (`glosa-fuente`, `procedencia: medina-colina-sxx`, página).
2. **Un lugar que Medina nombra y Esteves no** (Las Barisiguas en Dabajuro;
   los pueblos de las Aclaratorias con su escala c. 1900-1950): va a
   `propuesta.toponimo_a_la_cola` o a `lugares_nombrados`, y entra al canon
   con `fuente: medina-colina-sxx`, época **s. XX declarada** (regla 3), y
   casi siempre en C o descartado hasta que otra obra lo nombre.
3. **Una isoglosa** («en Tacuato y Santa Ana dicen gualamo, en el resto
   bisure», mc-mundo-020): no es topónimo, pero es dato de **variación por
   lugar** dentro de la Kaketiana; se registra en `datos_mundo` con
   `lugares:` y alimenta el casting de nodos, no el canon de topónimos.

Cada sesión de dictado cierra con `juntar_toponimos.py`: la mesa muestra lo
que Medina tocó y el cruce Medina ∩ Esteves. Lo que quede con ≡ y sin ★ es el
lote siguiente. Las once ciudades de Castellanos (ya con ficha) y el resto del
índice de Esteves siguen en la cola, a su ritmo.

**El barrido del mapa de la Kaketiana**, topónimo por topónimo. El territorio
es el de la polity costera que el vault define en
`3-mundo/polities-caquetias.md`: «Falcón llano, Paraguaná, el Golfete, y de
ahí a Aruba, Bonaire y Curazao»; en `asentamientos.yaml` son las regiones
`paraguana`, `golfete-de-coro`, `falcon-occidental` e `islas-abc`. El método,
para cuando se haga:

1. **Una lista de nombres del mapa vivo con coordenadas**, por región. Fuentes
   posibles: las fotos de Miguel (como hasta ahora, `cola_de_mapa`), un volcado
   de GeoNames (VE) o de OpenStreetMap filtrado por la caja de cada región.
   Descargar datos es decisión de Miguel; el script que los lea
   (`curiana_sim/barrer_mapa.py`, escrito el 2026-09-07: `--descargar` trae
   OSM vía Overpass, que fue la fuente que Miguel eligió ese día; la ficha es
   `4-fuentes/osm-kaketiana.md`) deja en
   `6-fusion/toponimos_mapa_kaketiana.yaml` una entrada por nombre:
   `{forma, tipo (poblado / cerro / quebrada / punta / bahía…), lat, lon,
   region, fuente_mapa}`.
2. **Cruzar con la mesa**: lo que ya está en el canon o en Esteves se marca;
   **lo que no está en ninguna fuente es lo nuevo**, y entra a la cola con
   `deuda: sin-procedencia` hasta que una obra lo nombre.
3. **Filtrar lo castellano** antes de segmentar (Buena Vista, Pueblo Nuevo, El
   Hato, La Rinconada, Pedregalito): el filtro 1 del protocolo del habla
   paraguanera. Se registran aparte, no se descartan en silencio.
4. Cada nombre indígena o dudoso pasa por §2-§8. Sin glosa de fuente casi
   todos quedarán en C o descartados hasta que Esteves, Zavala, van Buurt o
   una crónica los nombren; la ganancia del barrido es el **inventario con
   coordenadas**, que es lo que `asentamientos.yaml` y el diseño de nodos
   necesitan.
5. Regla 3 y 4 pesan más aquí que en ningún sitio: un nombre vivo en el mapa
   de 2026 es época moderna hasta que un documento lo lleve atrás, y un nombre
   de Falcón occidental no es de la polity costera sin decirlo.

## 10. Las trampas que costaron algo

| Trampa | Qué pasó |
|---|---|
| Editar `toponimos.yaml` a mano | dos commits lo hicieron y la regeneración deshizo 25 entradas; ahora hay test |
| Ids por orden de contenedor | añadir una entrada movía todas las siguientes; ahora son explícitos |
| OCR en el scratchpad | la pasada de Oliver del 08-17 se perdió; el OCR se guarda en `fuentes_caquetios/*.ocr.txt` |
| Cabeceras del libro ≠ mapa | BUCHUHACO / Buchuaco; Elegüey solo en el cementerio viejo de Punta Cardón |
| «Estrato» de un autor tomado como dato | el «caribe insular» de Esteves era fonética (batey, mamey, caney, carey) y nombre de lengua equivocado |
| Tomar la glosa sin leer la entrada | Adaure: la tradición dice Dara, pero Esteves sostiene que es apellido; las dos cosas van en la entrada |
| `generar_tablero.py` sin `--gh` | el gate salió 3/9 en vez de 6/9 por no ver las decisiones cerradas |
