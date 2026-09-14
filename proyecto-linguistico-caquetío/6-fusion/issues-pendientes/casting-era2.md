# Casting de la era 2: 61 agentes en cinco casas, con dossier por agente

<!-- issue sin publicar · labels: decision, motor · 2026-09-14 · estado: sin-fusionar
     datos: 6-fusion/elenco_era2.yaml
     verificación: 6-fusion/scripts/verificar_elenco_era2.py -->

> Propuesta de un escriba (regla 5). No toca `curiana_agents.py`, el motor, el
> lexicón ni `3-mundo/corpus/`. Los datos están en
> `6-fusion/elenco_era2.yaml`; esto es el resumen para vetar o aprobar.
>
> Aplica lo decidido el 2026-09-14: dos subgrupos por nodo con zonas de pesca
> exclusivas, la casa del Manaure en Moruy, familias grandes en tres capas,
> ~61 agentes con roster de ~24, poligamia de jefes, foráneos fuera.
> Lo que queda por decidir son las diez preguntas del final.

## 0 · Lo medido

Todas las cifras las imprime `python 6-fusion/scripts/verificar_elenco_era2.py`.
No hay ninguna a mano.

| | |
|---|---|
| agentes | **61** |
| por nodo | GUARANAO **37** · AMUAY **24** |
| por casa | Tacuatos 12 · Cayudes 12 · casa del Manaure 13 · Caseto 12 · Corubos 12 |
| por tier | T1 **16** · T2 **35** · T3 **10** |
| por linaje | Buio 15 · Corie 14 · Warana 13 · Paugis 11 · Kaira 5 · sin linaje de D1 3 |
| por origen | reutilizados de la era 1 **42** · de fondo promovidos **4** · nuevos **15** |
| roster que rota | **24** (GUARANAO 14, AMUAY 10) |
| portadores entre nodos dentro del roster | **6** de 24 |
| agentes de la era 1 que no entran | **18** (T1 5 · T2 11 · T3 2) |
| nombres nuevos acuñados | **15** |

El script comprueba además: unicidad de nombres; que ningún nombre nuevo ni su
raíz colisione con los 60 de `curiana_agents.ALL_AGENTS`, con las 14 personas de
fondo de `genealogia.yaml` ni con la `forma` de un topónimo del canon
(normalizando con `curiana_fonotactica.fonemizar`); que la raíz de cada nombre
nuevo esté en `VOCABULARIO_BASE` como caquetío atestiguado o reconstruido; que
cada agente lleve dossier con hechos, obras y decisiones; que todos los ids de
obra existan en `bibliografia.yaml` y todos los de hecho en `3-mundo/corpus/`;
que ningún `system_prompt` diga «Curiana» ni nombre el español y que todos
nombren su nodo y su sitio; y que los 60 de la era 1 tengan destino declarado.
**Hoy sale todo en verde.**

## 1 · Los linajes de D1, con su razón

Cinco casas, cinco linajes, uno de reserva.

| casa | nodo · sitio · pesca | linaje | por qué | alternativa marcada |
|---|---|---|---|---|
| los Tacuatos | GUARANAO · Tacuato · ZG2 | **Corie** | el subgrupo que «constituye» la tribu en la tradición, el pueblo «muy antiguo» del Resguardo de Salinas (Esteves p. 62): la casa que trata con los de afuera. Corie es el linaje de «lo común» y el más poblado de D1 | Buio |
| los Cayudes | GUARANAO · El Cayude · ZG2 | **Buio** | lleva nombre de árbol (`kayude`, voz atestiguada), queda monte adentro de la orilla, y de ahí sube el boratio mayor al cerro: of-02 exige que NO sea de Kaira | Paugis |
| casa del Manaure | GUARANAO · Moruy · sin playa | **Kaira** | decidido por Miguel el 2026-09-14; élite avunculocal (Keegan): el sobrino-heredero vive con el tío materno | ninguna (P1 resuelta) |
| los Guasicures de Caseto | AMUAY · Caseto · ZA1 | **Warana** | es el linaje de Nubiri-sha y tiene que estar en AMUAY para que el matrimonio del paramount sea alianza entre clanes. Va en Caseto y no en Carirubana porque Caseto está a ~8 km de Moruy contra ~25: ese camino corto **es** la alianza | Paugis en Caseto y Warana en Carirubana |
| los Corubos | AMUAY · Carirubana · ZA1 | **Paugis** | las ancianas que cuidan el ayuno del heredero y muelen los huesos del díao son del OTRO clan (of-09): sin Paugis en AMUAY ningún clan necesita al otro para hacer Manaure. Y corubo es «caparazón de moluscos» (Esteves p. 34; `ecologia-061`): la casa de las conchas es la casa de los huesos | **Chiriware**, la costa que mira al mar abierto |
| — reserva — | de fondo en Cayerúa | **Chiriware** | Oliver: la polity costera carecía de «an effective military organization» y la norma ante el conflicto era alzarse (pdf 107). Vuelve con el nodo caribe (era 3) | — |

## 2 · Las cinco casas

#### los Tacuatos — GUARANAO, Tacuato (11.708, −69.841), ZG2, linaje **Corie**

| agente | rol en la casa | tier | linaje | origen | roster |
|---|---|---:|---|---|:-:|
| **Kunaro-bana** | apopo | 1 | Corie | era 1 | X |
| **Pira-sha** | matriarca | 2 | Corie | era 1 | X |
| **Biro-ko** | hermano adulto | 1 | Corie | era 1 | X |
| **Naure-sha** | hermana con hijos | 2 | Corie | era 1 |  |
| **Piri-sha** | hermana | 2 | Corie | era 1 |  |
| **Guare-ko** | esposo entrante del otro nodo | 2 | Warana (de fuera) | fondo |  |
| **Kori-sha** | esposa del apopo (del otro subgrupo del mismo nodo) | 2 | Buio (de fuera) | era 1 |  |
| **Suba-ko** | esposa del apopo (del otro nodo) | 2 | Paugis (de fuera) | era 1 | X |
| **Uro-ko** | anciano con oficio (tío materno mayor) | 2 | Corie | era 1 |  |
| **Kawa** | joven | 3 | Corie | era 1 |  |
| **Piri** | joven | 3 | Corie | era 1 |  |
| **Kori** | niña | 3 | Corie | era 1 |  |

Oficios del cerro en esta casa: **of-10** (pintura ritual, Pira-sha) y **of-13**
(el de la buena vara, Uro-ko, un HUECO que se cierra). La cuñadez atestiguada
Naure-sha ↔ Piri-sha se conserva entera: sus maridos, Guare-ko y Tawa-ko, son
dos hermanos venidos de Caseto, uno en escena y otro de fondo.

#### los Cayudes — GUARANAO, El Cayude (11.701, −69.957), ZG2, linaje **Buio**

| agente | rol en la casa | tier | linaje | origen | roster |
|---|---|---:|---|---|:-:|
| **Bagre-ko** | apopo | 1 | Buio | era 1 | X |
| **Tuqa-sha** | matriarca | 2 | Buio | fondo | X |
| **Dara-bana** | hermano adulto | 2 | Buio | era 1 |  |
| **Suka-sha** | hermana con hijos | 2 | Buio | nuevo |  |
| **Kati-sha** | hermana con hijos | 2 | Buio | nuevo |  |
| **Wari-ko** | esposo entrante del otro nodo | 2 | Warana (de fuera) | era 1 | X |
| **Wama-sha** | esposa del apopo (del otro subgrupo del mismo nodo) | 2 | Corie (de fuera) | era 1 |  |
| **Waranaro-sha** | esposa del apopo (del otro nodo) | 2 | Paugis (de fuera) | era 1 | X |
| **Taku-ko** | joven | 2 | Buio | era 1 |  |
| **Daru** | joven | 3 | Buio | era 1 |  |
| **Ita-sha** | anciana acogida (sin linaje) | 3 | sin linaje | era 1 |  |
| **Sha** | niña | 3 | Buio | era 1 |  |

Oficios: **of-03** (boratio de pueblo de GUARANAO, Bagre-ko — el apopo es a la
vez boratio, que es lo que dice Arcaya: «el diao es boratio»), **of-11**
(séquito de la hamaca, Taku-ko) y **of-12** (mensajero de GUARANAO, Daru).
Tuqa-sha, que `genealogia.yaml` daba por «posiblemente fallecida», se promueve a
matriarca viva: era el hueco que el propio archivo señalaba para Buio.

#### casa del Manaure — GUARANAO, Moruy (11.822, −69.983), sin zona de pesca, linaje **Kaira**

| agente | rol en la casa | tier | linaje | origen | roster |
|---|---|---:|---|---|:-:|
| **Manaure** | Manaure (diao paramount) | 1 | Kaira | era 1 | X |
| **Nubiri-sha** | esposa principal (del otro nodo) | 1 | Warana (de fuera) | era 1 | X |
| **Itana-sha** | hermana mayor, matriarca de Kaira | 1 | Kaira | fondo | X |
| **Jakura-sha** | hermana menor | 2 | Kaira | nuevo |  |
| **Waimo-ko** | sobrino candidato (hijo de la hermana mayor) | 1 | Kaira | fondo | X |
| **Kabo-ni** | sobrino candidato (hijo de la hermana menor) | 2 | Kaira | nuevo | X |
| **Tina-sha** | esposa del Manaure (de Tacuato) | 2 | Corie (de fuera) | era 1 |  |
| **Kahu-sha** | esposa del Manaure (de El Cayude) | 2 | Buio (de fuera) | era 1 |  |
| **Kali-nu** | hijo que no hereda | 2 | Warana (de fuera) | nuevo |  |
| **Piru** | hijo que no hereda (niño) | 3 | Corie (de fuera) | era 1 |  |
| **Shaboro** | boratio mayor | 1 | Buio (de fuera) | era 1 | X |
| **Buio-sha** | ayunante | 1 | Buio (de fuera) | era 1 |  |
| **Moruy-sha** | maestra del merejuy (titular) | 2 | Corie (de fuera) | era 1 |  |

Es la única casa sin playa: **no pesca, recibe**, y esa asimetría es el
mecanismo de redistribución. Oficios: **of-01** (Manaure), **of-02** (Shaboro,
que duerme en el Capubana y es de El Cayude por sangre, nunca de Kaira),
**of-04** (Buio-sha), **of-05** (Itana-sha), **of-06** (Kali-nu, HUECO cerrado)
y **of-07** (Moruy-sha, HUECO cerrado). Seis de sus trece no son Kaira: la casa
del señor es la más mezclada de las cinco, que es lo que la poligamia produce.

**La pluralidad de candidatos (parentesco-039) por fin se ejecuta**: dos
sobrinos elegibles, y el de la hermana *menor* es tres años *mayor* que el de la
mayor. La comparanda taína dice que hereda el hijo mayor de la hermana mayor;
los años dicen otra cosa. Ver P7.

#### los Guasicures de Caseto — AMUAY, Caseto (11.762, −70.017), ZA1, linaje **Warana**

| agente | rol en la casa | tier | linaje | origen | roster |
|---|---|---:|---|---|:-:|
| **Ita-ko** | apopo | 1 | Warana | era 1 | X |
| **Wasima-sha** | matriarca | 2 | Warana | nuevo |  |
| **Tabri-sha** | hermana con hijos | 2 | Warana | nuevo |  |
| **Tijua-sha** | hermana con hijos | 2 | Warana | nuevo |  |
| **Wama-ko** | hermano adulto | 2 | Warana | era 1 |  |
| **Tawaka** | esposo entrante del otro nodo | 1 | Buio (de fuera) | era 1 | X |
| **Saruro-sha** | esposa del apopo (de Cayerúa) | 1 | propio | era 1 | X |
| **Dipopo-sha** | esposa del apopo (del otro nodo) | 2 | Buio (de fuera) | nuevo |  |
| **Suri-bana** | joven | 2 | Warana | era 1 |  |
| **Pari-nu** | joven | 2 | Warana | era 1 | X |
| **Bana-mana** | anciano con oficio (tío materno mayor) | 2 | Warana | era 1 | X |
| **Tawi** | niña | 3 | propio (de su madre) | era 1 |  |

Ita-ko es hermano mayor de Nubiri-sha: la casa que dio la esposa principal.
Oficios: **of-08** (Bana-mana, el cantor de AMUAY), **of-10** (Saruro-sha) y
**of-11** (Suri-bana), más **of-12** (Pari-nu). El of-08 de GUARANAO queda
HUECO a propósito: su contrapartida en escena es la memoria **pintada** de
Pira-sha frente a la memoria **cantada** de Bana-mana. Dos versiones del pasado
que ni siquiera usan el mismo soporte.

#### los Corubos — AMUAY, Carirubana (11.694, −70.218), ZA1, linaje **Paugis**

| agente | rol en la casa | tier | linaje | origen | roster |
|---|---|---:|---|---|:-:|
| **Kiwa-ko** | apopo | 1 | Paugis | nuevo | X |
| **Sha-korie** | matriarca | 2 | Paugis | era 1 | X |
| **Paugis-sha** | hermana de la matriarca | 1 | Paugis | era 1 | X |
| **Dara-ko** | hermano adulto | 1 | Paugis | era 1 | X |
| **Tauta-sha** | hermana con hijos | 2 | Paugis | nuevo |  |
| **Ebo-ni** | esposo entrante del otro nodo | 2 | Corie (de fuera) | nuevo | X |
| **Arika-sha** | esposa del apopo (del mismo nodo) | 2 | Warana (de fuera) | nuevo |  |
| **Karapa-sha** | esposa del apopo (del otro nodo) | 2 | Buio (de fuera) | nuevo |  |
| **Dare-nu** | joven | 1 | Paugis | era 1 |  |
| **Talata-sha** | joven (en encierro puberal) | 2 | Paugis | nuevo |  |
| **Moro-ko** | anciano con oficio (tío materno mayor) | 3 | Paugis | era 1 |  |
| **Nubi** | niño | 3 | Paugis | era 1 |  |

Oficios: **of-03** (Paugis-sha, boratia de pueblo de AMUAY — HUECO cerrado, y
la propuesta más expuesta del casting: ver P4) y **of-09** (Sha-korie y
Moro-ko). Aquí también se cierra el hueco de la **muchacha en encierro puberal**
(Talata-sha, `transmision-020` y `transmision-028`). Y `transmision-002`
mejora: Dara-ko ya no enseña a Dare-nu «como a un hijo prestado» sino como su
**tío materno**, que es lo que el sistema matrilineal manda.

## 3 · Cómo se enlazan las casas

Dos canales, como manda la decisión, y los dos con nombre y apellido.

**Esposos entrantes (gente común, matrilocal)** — cuatro cruces, dos por lado:

- Guare-ko (Warana, de Caseto) → los Tacuatos
- Wari-ko (Warana, de Caseto) → los Cayudes
- Tawaka (Buio, de El Cayude) → Caseto
- Ebo-ni (Corie, de Tacuato) → los Corubos

**Esposas de jefes (élite, al revés)** — cinco cruces entre nodos:

- Suba-ko (Paugis, de Carirubana) → los Tacuatos
- Waranaro-sha (Paugis, de Carirubana) → los Cayudes
- Dipopo-sha (Buio, de El Cayude) → Caseto
- Karapa-sha (Buio, de El Cayude) → los Corubos
- Nubiri-sha (Warana, de Caseto) → la casa del Manaure

Y cinco más dentro del nodo (Kori-sha, Wama-sha, Arika-sha, Tina-sha y
Kahu-sha, más Saruro-sha desde Cayerúa).

**La tensión que se deja puesta:** los Corubos son la única casa sin mujer en la
casa del Manaure. Las tres esposas cubren Caseto, Tacuato y El Cayude; la casa
más lejana, la de la boratia que le disputa la palabra al boratio mayor, queda
fuera de la alianza matrimonial. Es material de conflicto, no un descuido (P6).

## 4 · El roster de 24

Jefes, esposas principales, herederos y oficios, como pide la decisión. Seis de
los 24 son portadores permanentes entre nodos: es la cuarta parte de las voces
que rotan, y es el motor de la pregunta de la koiné.

| nodo | casa | agentes |
|---|---|---|
| GUARANAO | casa del Manaure | Manaure, Nubiri-sha, Itana-sha, Waimo-ko, Kabo-ni, Shaboro |
| GUARANAO | los Tacuatos | Kunaro-bana, Biro-ko, Pira-sha, Suba-ko |
| GUARANAO | los Cayudes | Bagre-ko, Tuqa-sha, Waranaro-sha, Wari-ko |
| AMUAY | los Guasicures de Caseto | Ita-ko, Saruro-sha, Tawaka, Pari-nu, Bana-mana |
| AMUAY | los Corubos | Kiwa-ko, Paugis-sha, Sha-korie, Dara-ko, Ebo-ni |

Reparto 14 / 10, proporcional a los 37 y 24 agentes de cada nodo. Ver P10 si se
prefiere 12 / 12 para que la métrica de cruce tenga la misma base.

Primer candidato a entrar si el roster crece: **Dare-nu**, el único agente
criado con un padre de un nodo y una madre del otro, que pregunta en voz alta
cuál de los dos nombres es el verdadero.

## 5 · Lo reutilizado y lo retirado

**42 de los 60 de la era 1 vuelven**, casi todos reanclados. Los reanclajes que
cambian algo de fondo:

- **Manaure** pierde «Heredó de su padre el control de las rutas de biro»: es
  dato de la sucesión colonial que `parentesco-001` marca NO USAR (regla 3).
- **Nubiri-sha** deja de tener un «linaje materno» sin nombre: es Warana, de
  Caseto, en AMUAY. Su matrimonio pasa a ser la alianza entre los dos clanes.
- **Shaboro** y **Buio-sha** viven donde el oficio (Moruy y el cerro) y no donde
  la sangre (El Cayude), igual que el heredero vive con el tío materno.
- **Paugis-sha** pasa de curandera a **boratia de pueblo de AMUAY**, con la
  rivalidad con Shaboro que Antolínez 1946 pide.
- **Dara-ko** se vuelve el tío materno de Dare-nu: `transmision-002` deja de ser
  «casi un padre» y pasa a ser lo que la matrilinealidad manda.
- **Tawaka** deja el perímetro y cruza a AMUAY como esposo entrante. Su afecto
  no correspondido por Buio-sha queda mejor explicado que antes: los dos son
  Buio, y la exogamia de parcialidad los separaba de todos modos.
- **Uro-ko** pasa de pescador retirado a **el de la buena vara** (of-13).
- **Kunaro-bana**, **Bagre-ko** e **Ita-ko** suben a apopo (tier 1).

**Cuatro personas de fondo de `genealogia.yaml` se promueven a agente**:
Itana-sha, Waimo-ko, Tuqa-sha y Guare-ko. Era el paso que el propio archivo
señalaba como natural para Kaira y para Buio.

**18 de la era 1 no entran:**

| grupo | agentes | destino |
|---|---|---|
| foráneos (decisión del 2026-09-14) | Marokoto-ni, Tariwa, Kawa-ni, Piru-sha, Tari-ko | era 3 |
| foráneos serranos | Nabaraka, Raka-bi, Chorota | de fondo |
| el buco (no hay ríos en Paraguaná) | Korie-ko, Buko-ko, Buko, Buko-ni | retirados / de fondo — **ver P2** |
| linaje de reserva | Chiriware, Chiri-ko | de fondo en Cayerúa — **ver P1** |
| la ruta insular está fuera de escena | Watapana, Kadushi | de fondo — **ver P3** |
| identidad sin sitio | Wata-ni (sin guaycaríes), Jiru-ko (sin serranos) | era 3 / de fondo |

## 6 · Los 15 nombres nuevos

Todos con raíz caquetía atestiguada o reconstruida, con los patrones del elenco
actual, y todos verificados contra los 60 nombres, las 14 personas de fondo y
los 180 topónimos del canon.

| nombre | raíz | glosa | capa |
|---|---|---|---|
| Jakura-sha | jakura | guardar, conservar, custodiar | atestiguado |
| Kabo-ni | kabo | cabeza, mente, lo alto de | reconstruido |
| Kali-nu | kali | sol | reconstruido |
| Suka-sha | suka | noche, oscuridad | reconstruido |
| Kati-sha | kati | luna | atestiguado |
| Dipopo-sha | dipopo | fibra de cocuiza, cabuya | atestiguado |
| Wasima-sha | wasima | viejo, anciano | atestiguado |
| Tabri-sha | tabri | siembra, plantación en proceso | atestiguado |
| Tijua-sha | tijua | paloma de canto onomatopéyico | atestiguado |
| Kiwa-ko | kiwa | concha de almeja y otros moluscos | atestiguado |
| Arika-sha | arika | árbol de jícara o totumo | atestiguado |
| Karapa-sha | karapa | árbol resinoso | atestiguado |
| Tauta-sha | tauta | pequeña paloma de hábitos ictiófagos | atestiguado |
| Ebo-ni | ebo | camino, paso, senda | atestiguado |
| Talata-sha | talata | alegría, contento, gozo | reconstruido |

Siete candidatos se descartaron **por colisión medida**, no por gusto:
`Karuka-sha` (caruca es topónimo del canon), `Kiba-ko` (la raíz abre
*quibacoas*), `Dabuda-sha` (abre *dabudare*), `Tara-sha` (abre *tarai*,
*taratarare*, *Taratata*), `Bisure-sha` (es toponimo-179), `Kapua-sha` (se
confunde con *kapu* / *kapo* / *kapubana*) y `Ure-ko` (se confunde con el agente
Uro-ko).

## 7 · Las reglas de casting de la auditoría, aplicadas

De `auditoria_esferas_contexto_2026-09-14.md` §8 punto 9:

- **cero** fichas dicen «Español …» (hoy son 33 de 33 en T2);
- **cero** `system_prompt` dicen «Curiana»: los 51 de tier 1 y 2 nombran su
  nodo y su sitio, que es lo que la era 2 tiene que volver consciente;
- todo agente es alcanzable: el roster `todos` de la era 2 llega a los 61,
  tier 3 incluidos, y 24 rotan;
- se retira el dato que el corpus marca NO USAR («heredó de su padre»).

## 8 · Lo que este casting NO decide

Las semillas léxicas divergentes por nodo, el prestigio y los vínculos de
`curiana_social`, y la migración de `agentes_relacionados` del corpus al elenco
nuevo — al cambiar el elenco, `compilar_corpus.validar_agentes` **va a fallar**,
y eso es trabajo de fusión, no de casting.

## 9 · Diez preguntas

1. **¿Se aprueba el reparto de linajes** (Corie–Tacuato, Buio–El Cayude,
   Kaira–Moruy, Warana–Caseto, Paugis–Carirubana) con Chiriware de reserva? La
   alternativa es Chiriware en Carirubana y Paugis a la reserva; el costo es que
   se cae la ratificación del heredero por ancianas del otro clan, que es el
   rito que obliga a converger.
2. **¿Korie-ko, Buko-ko y Buko se retiran con el buco, o se reanclan al
   jagüey?** Oliver p. 252 describe el riego con charcas artificiales para esta
   costa y el lexicón tiene `jagey` y `jakuke` atestiguados. Reanclarlos
   devolvería un tier 1 y la cadena padre-hijo de `transmision-011`.
3. **¿Watapana y Kadushi quedan de fondo** mientras la costa norte y la ruta
   insular estén fuera de escena? Forzar su entrada sin mercado inventado
   (§4.3 del diseño lo prohíbe) los deja casi sin oficio.
4. **¿Paugis-sha puede ser boratia de AMUAY (of-03)?** La sostienen la ouutsü
   wayuu (`transmision-030`, `transmision-033`) y la glosa de `boratio` sin
   marca de género (`parentesco-036`). No hay ni un dato caquetío de mujer
   boratio: es la propuesta más expuesta. Si se veta, el puesto vuelve a estar
   HUECO y hay que acuñar un varón.
5. **¿«2 esposas traídas de otro subgrupo» se lee como una del mismo nodo y otra
   del otro?** Así hay cuatro portadoras de élite más; si no, el único cruce de
   élite sería Nubiri-sha.
6. **¿Los Corubos se quedan sin esposa en la casa del Manaure**, como tensión, o
   Manaure toma una cuarta esposa corubo (la decisión permite «3-4»)? Cerrarlo
   aplana la política y sube esa casa a 14.
7. **¿Kabo-ni (24, hijo de la hermana menor) contra Waimo-ko (21, hijo de la
   mayor)?** La comparanda taína favorece a Waimo-ko; la edad a Kabo-ni. ¿Se
   deja abierto como trama o se decide ya?
8. **¿Ita-sha se queda sin linaje**, acogida por los Cayudes, como manda
   `genealogia.yaml`, o se le asigna Buio?
9. **¿Saruro-sha y Tawi entran con linaje propio sin nombre, traído de
   Cayerúa?** `genealogia.yaml` la declara independiente de los seis; respetarlo
   obliga a darle casa natal fuera de escena.
10. **¿El roster va 14/10 (proporcional) o 12/12 (mismo instrumento por nodo)?**
    Con 12 agentes por turno, ese reparto decide cuántas voces de cada lado
    entran en la ventana. Es decisión de diseño experimental, no de mundo.

---

*Datos: `6-fusion/elenco_era2.yaml` · Verificación:
`6-fusion/scripts/verificar_elenco_era2.py` · Relacionado: `DISENO_ERA2.md`
§3-§6 · `estructura_social_era2.yaml` (#126) ·
`decisiones_tanda_2026-09-14.yaml` · `genealogia.yaml` (D1) ·
`auditoria_esferas_contexto_2026-09-14.md` §8*
