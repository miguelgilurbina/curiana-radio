---
tipo: fuente
obra: "OpenStreetMap — el mapa vivo de la Kaketiana (volcado por regiones)"
autor: "OpenStreetMap contributors"
anio: "2026"
publicacion: "OpenStreetMap, consultado vía Overpass API (https://overpass-api.de) el 2026-09-07. Licencia ODbL 1.0."
genero: datos
local: "fuentes_caquetios/osm_kaketiana/*.json (una caja por archivo; la consulta, la caja y la fecha van en `_curiana`)"
paginas: "— (datos: 1.696 nombres con coordenadas en cuatro regiones)"
acceso: "Libre. Se regenera con `python curiana_sim/barrer_mapa.py --descargar`; es decisión de Miguel (2026-09-07: «vamos con OSM»)"
capa_texto: datos
estado_minado: en-curso
prioridad: media
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-07
minado: 2026-09-07
aliases: ["OSM", "OpenStreetMap", "el mapa vivo", "osm-kaketiana", "barrido del mapa"]
---

# OpenStreetMap — el mapa vivo de la Kaketiana

> **Qué es.** No es una obra: es una **capa de datos**. Un nombre aquí prueba
> que el nombre está vivo en 2026 y dónde está, nada más. Sirve para el
> inventario con coordenadas que `asentamientos.yaml` y el diseño de nodos
> necesitan, y para la regla de Miguel: **un nombre que sigue vivo es dato**.
> Lo que no prueba es época (regla 3) ni polity (regla 4): cada entrada lleva
> su región y su deuda.

## Qué se preguntó (2026-09-07)

El barrido del mapa topónimo por topónimo que pide la skill
`campana-toponimos` §9: una lista de nombres del mapa vivo con coordenadas, por
región, cruzada con la mesa de la campaña; lo que no está en ninguna fuente es
lo nuevo. Miguel eligió OSM entre GeoNames, OSM y sus fotos del mapa.

## Cómo se hizo

`curiana_sim/barrer_mapa.py`:

1. **Cajas** por región de `asentamientos.yaml` (paraguana, golfete-de-coro,
   falcon-occidental, islas-abc; las islas son tres cajas). Se descargan
   `nwr["name"]` con `place`, `natural`, `waterway` o `landuse=salt_pond`,
   con `out center` para que vías y relaciones tengan un punto.
2. **Tipo** por etiqueta OSM (poblado, caserío, lugar, cerro, punta, bahía,
   playa, quebrada, salina…). Lo que no cabe se descarta y se cuenta (árboles,
   cuevas, plazas, muelles).
3. **Clase** heurística, transparente y revisable: `castellano` (todas las
   palabras, quitados los genéricos, son castellanas o llevan sufijo
   castellano; o el nombre empieza por San/Santa/Sector/Urbanización…),
   `castellano-con-voz-indigena` (Cardón, Cují, Yabo…: préstamo lexicalizado),
   `neerlandes-papiamento` (solo islas ABC) y **`por-clasificar`**, que es la
   clase que importa.
4. **Cruce** de los `por-clasificar` con la mesa (`toponimos_por_fuente.yaml`)
   por la misma clave que `juntar_toponimos.py`: exacto, parcial (una palabra
   del nombre, «Bajo de Supi» → Supí) o **aproximado** (distancia 1-2 tras la
   permutación laxa de la skill, j~s~u~h, b~v~p, r~b: Jurujurebo ~ jurijurebo,
   Cividual ~ sibidigual). El aproximado es para revisar, no cuenta como
   encontrado.
5. Salida: `6-fusion/toponimos_mapa_kaketiana.yaml` (generado) con resumen por
   región y una entrada por nombre; `--lote` imprime lo nuevo.

## Qué ha dado

El resumen medido vive en el `meta.resumen` del YAML generado; la cifra de
aquí es la del día del volcado y no se mantiene a mano. Lo cualitativo:

- **Paraguaná**: el mapa vivo confirma la regla de las permutaciones — varios
  nombres «nuevos» eran grafías vecinas de nombres de Esteves (Jurujurebo,
  Cerro Capuana = Capuhana, Cuabana = Coabana, Guaydabacos = Guaidabacoa,
  Sisibauco = el «[ilegible …Sisibaúco]» del índice, Cividual = Sibidigual,
  Guacujún = Guacujúa, Curuca = Caruca). Y deja nombres indígenas que no
  están en ninguna fuente del proyecto: candidatos a la cola.
- **Golfete de Coro y Falcón occidental**: casi todo es nuevo para el
  proyecto, porque Esteves solo cubre Paraguaná. Es el inventario que faltaba
  para los nodos de la costa.
- **Islas ABC**: OSM trae cientos de sectores de Willemstad con nombre
  neerlandés; el filtro los aparta. Lo indígena de las islas hay que buscarlo
  en los nombres de cerros, puntas y bahías (Seru, Boka, Punt…), y cruzarlo
  con [[van-buurt-2014]] y [[gatschet-1885]], que ya están en la mesa.

## Qué no da

- Ninguna glosa: todo lo nuevo entra con `deuda: sin-procedencia` hasta que
  una obra lo nombre.
- Ninguna época: un nombre vivo es moderno hasta que un documento lo lleve
  atrás.
- Cobertura desigual: OSM depende de quién haya mapeado cada zona. Un cero en
  OSM no es un cero en el terreno (regla 6).

## Lo que sigue

Procesar los `por-clasificar` nuevos de Paraguaná por §2-§8 de la skill
(permutar, buscar en el cuerpo de Esteves, Medina Colina), confirmar o
descartar los aproximados, y decidir si los inventarios del Golfete y Falcón
occidental se cruzan contra Arcaya y las crónicas antes de entrar a la cola.

## Enlaces

[[INDICE_FUENTES]] · [[esteves-1989]] · [[toponimia]] · [[esfera-de-interaccion]] · [[polities-caquetias]]
