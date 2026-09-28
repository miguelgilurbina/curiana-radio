---
tipo: analisis
serie: era2-base
brazo: con escena (Capubana cada 3)
cadena: dd680e49 → 720d1ef1 (30 días)
fecha: 2026-09-28
fuentes: [simulation_runs/agent_responses/koine_lexicon/neologisms de la base local, estado guardado del brazo en C:/Users/migue/curiana_estado_backup/era2-base-escena/, logs por día en C:/Users/migue/curiana_runs_log/era2-base/]
---

# era2-base, brazo con escena: la competencia por los nombres y lo que narró el Director

Relectura sin API de los 30 días (pedida por Miguel el 2026-09-28). Todas las
cifras salen de la base local o del estado guardado; nada es predicción. El
veredicto de la cadena y el análisis por nodo están en `5-experimento/BITACORA_RUNS.md`
(§serie `era2-base`) y en `era2_base_escena_nodos_2026-09-28.txt`.

## 1. La competencia: un referente cada dos días, y dos clases de disputa

El motor presenta un referente nuevo **cada dos días** (días impares): 15 en 30
días. Al día 30, **7 fijados y 8 en disputa**; las disputas abiertas pasan de
4 (día 15) a 8 (día 30): llegan más rápido de lo que se resuelven.

| referente | entra | fijado | tardó | forma | variantes |
|---|---:|---:|---:|---|---:|
| delfín | 5 | 5 | 0 | `punu-dunku` | 4 |
| cardumen | 11 | 13 | 2 | `saka-ruku` | 5 |
| cometa | 13 | 14 | 1 | `diki-pui-bana` | 6 |
| conejo | 15 | 15 | 0 | `sona-koro-iro` | 4 |
| eclipse | 21 | 21 | 0 | `kasi-uli-kiba` | 2 |
| cardenal | 9 | 24 | 15 | `halira-iro` | 5 |
| gaviota | 25 | 27 | 2 | `diki-kiba` | 6 |
| tarántula azul | 1 | — | 29+ | `kule-biro-iro` 31,9 · `oto-biro-oto` 31,0 | 10 |
| guacharaca | 3 | — | 27+ | `tuke-jai` 28,2 · `jai-ubana-kida` 24,4 | 4 |
| cascabel | 7 | — | 23+ | `biro-saka` 78,6 · `sona-iro` 34,3 | 10 |
| corocoro | 17 | — | 13+ | `kule-pui-tara` 29,3 · `jai-tara` 26,1 | 9 |
| tortugas de mar | 19 | — | 11+ | `mau-diki` 52,3 · `kibe-piko-buio` 45,5 | 10 |
| perro mudo | 23 | — | 7+ | `sile-ubana` 7,0 · `ada-iro` 5,6 | 7 |
| metal amarillo | 27 | — | 3+ | `halira-despopo` 32,2 · `mara-biro-kule` 21,8 | 4 |
| ballena | 29 | — | 1+ | (soporte ≤ 1,4) | 3 |

Lectura: **o se fijan casi en el acto (0-2 días) o se quedan semanas.** Las que
se quedan tienen muchas variantes (10) o dos rivales parejas: la tarántula lleva
29 días en empate (31,9 contra 31,0), y el cascabel tiene la forma con MÁS
soporte de toda la serie (`biro-saka`, 78,6) sin fijarse, porque la regla pide
el 55 % del soporte y diez variantes se lo reparten. La acumulación de disputas
coincide con la subida de la distancia emergente desde el día 15 (bitácora).

## 2. Fijar no es vivir

Respuestas que dicen la forma, antes y después de fijarse:

| forma | fijada | antes | después |
|---|---:|---:|---:|
| `saka-ruku` | 13 | 64 | **104** (16 días) |
| `punu-dunku` | 5 | 6 | **82** (18 días) |
| `diki-pui-bana` | 14 | 8 | **75** (14 días) |
| `kasi-uli-kiba` | 21 | 14 | 28 (7 días) |
| `sona-koro-iro` | 15 | 7 | 14 (7 días) |
| `halira-iro` | 24 | **74** | 5 (3 días) |
| `diki-kiba` | 27 | 15 | 3 (1 día) |

Tres palabras siguen vivas después de fijarse; `halira-iro` (el cardenal) se
fijó cuando ya se apagaba (pico de 22 respuestas el día 12). La fijación es un
umbral del instrumento, no el momento en que la palabra entra en la lengua.

## 3. Raíces que salen del sonido

Las formas de animales traen raíces que no están en el lexicón y que el motor
dejó entrar por la puerta onomatopéyica (tanda de la base, db.6): `tuke` (el
grito de la guacharaca: `tuke-jai`, «el grito-que-oye, el llamador»), `punu` y
`pui-pui` (el resoplido del delfín: «el que sopla-suena»), `saka` (el raspado:
`biro-saka`, «la que resuena como la sal siendo raspada»). Y hay deriva de
sentido: `saka-ruku` nació el día 7 para el cascabel («lo que suena adentro») y
el día 13 quedó fijada para el cardumen («la mancha en el mar que hierve»).
`mau-diki` es a la vez la variante líder de las tortugas y, en boca de Sawaka el
día 24, «mal-ver» (lo que el piache vio en el sueño).

⚠️ **Para revisar**: `sona` quedó registrada como raíz onomatopéyica el día 7
(«pequeño sonido que canta») y se parece al castellano *sonar*; de ahí
`sona-koro-iro` (fijada) y `sona-iro`.

## 4. Defectos del instrumento vistos al leer (no se tocan hasta que cierre el control)

- Variantes con asteriscos de markdown pegados: `**kasi-uli-kiba`,
  `**karuhu-puhi-puhi-kibe**`, `**butu-koro-saka**` — reparten soporte con la
  forma limpia.
- Una variante con espacio y pronombre dentro: `tuhu bari-saka-ruku`.
- El motor está congelado (tag `base-era2-1`) hasta que el brazo de control
  tenga sus 30 días: arreglarlo ahora rompería la comparación.

## 5. Lo que narró el Director (30 reflexiones)

Texto entero: `era2_base_escena_reflexiones_director_2026-09-28.txt`.

**Los arcos.**

- **Hambre, sospecha y una palabra para la rabia (días 1-10).** La sal baja,
  las redes vuelven vacías (6-8) y en Carirubana empiezan «los susurros sobre
  Sawaka y Hayo, sobre algo que no hicieron bien en el cerro Capubana, como si
  la gente necesitara una boca donde poner el hambre» (día 2). El día 8 Waru
  acuña `aiima-raku`, «rabia-profunda», y se extiende a Manaure, Talata,
  Chuchubi; el día 9 «pasó de ser sentimiento suelto a ser parte del trabajo,
  parte del ritual».
- **Los muertos con nombre (día 4).** Turicha nombra a los muertos en Punta
  Cardón —Makuariwa, Dakura, Bikatua—, que «se asentaron como parte de lo que
  hay que guardar, igual que el casabe y la sal».
- **La fiebre del muchacho y el silencio de Manaure (15-17).** «La fiebre del
  muchacho fue el quiebre»; baja al día siguiente, y «Manaure sigue callado en
  Moruy, pero su silencio ya no ocupa el centro».
- **La abundancia y el vocabulario de lo que sostiene (16-20).** Con comida, la
  lengua pasa a nombrar lo de adentro: `barsure-ruku` («esa fuerza adentro»),
  `kuburuku-ima-bana`, `kaa-ruku-bana`; y el trabajo: `manteka-kunaro` (la grasa
  de las antorchas), `jacu-iro` (las antorchas pequeñas).
- **El eclipse y la grieta entre oficios (21-23).** `kasi-uli-kiba` se dice «juntos
  para que fuera real»; el buko no sube y «antes del alba habrá que decidir quién
  come primero —el que pesca o el que siembra».
- **El piache ve (24).** Sawaka acuña `mau-diki`, «malo-ver», para lo que vio en
  el sueño: agua turbia donde debería estar clara.
- **La iniciación y el cierre (29-30).** Manaure convoca; Dakawa y Chuchubi
  «atravesaron lo que debían atravesar»; el día 30 vuelve un niño con fiebre, con
  Siwa y sus hierbas, y Amaka propone `ani-saka`, «hacer-resonancia, invocar».

**Lo que no está bien (el instrumento hablando por la boca del Director).**

- Habla del **observador** («Sawaka vio algo que el observador no midió», día 5;
  «las otras dos que el observador marcó como adoptadas», día 17): la medición se
  cuela en la ficción.
- **Treinta días de alisio firme del este**: el Tiempo de Viento dura 50 días y
  la serie entera cae dentro. Es el calendario (decisión 2026-09-15), no un error,
  pero la narración se repite.
- Voces fuera del canon en su prosa castellana: *piache* (archivada, D10),
  *caney*, *macanas*, *chicha*; y erratas (*salt*, *múculos*, *tiemblar*).
- `manteka-kunaro` lleva *manteca*, que es castellano; viene del propio canon
  (el corpus dice «la manteca de los jachos» del cunaro). Queda para revisar,
  como `sona`.
- Afirma que palabras «prendieron» con más soltura de lo que la medición
  sostiene: la narración del Director no es dato de adopción.
