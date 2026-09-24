# El mar caquetío: economía, moneda, camino, parientes y nombre, con fuente; creencia, ninguna. Lo sagrado que las fuentes le ven a esta gente está en el cielo y en el maíz

**Campaña cc.10 — la cosmovisión marina, la última del cierre. 2026-09-24.**
Rama `campana/cosmovision-marina-2026-09-24`.

Miguel, en cc.10 (`6-fusion/decisiones_cierre_2026-09-23.yaml`): *«esa campaña
de Cosmovisión Marina tenemos que dejarla a lo último, efectivamente no hay nada
eh, que tengamos establecido […] es una intuición nuestra por los momentos».* Y
el origen de la intuición, en el encargo de FA3 (2026-09-22): *«el aspecto marino
era esencial en la cosmovisión caquetía»*.

**Ninguna cifra del lado del repo está escrita a mano.** Las imprime

```bash
python 6-fusion/scripts/medir_cosmovision_marina.py --conteos        # el bloque meta.medido
python 6-fusion/scripts/medir_cosmovision_marina.py                  # valida el YAML y compara
python 6-fusion/scripts/medir_cosmovision_marina.py --ventanas DIR   # las ventanas, para leerlas
```

Todo está en `6-fusion/cosmovision_marina_2026-09-24.yaml`: los hechos
candidatos (`hechos_candidatos`, `arqueologia`), la comparanda de los vecinos
(`comparanda`), lo que dicen autores del s. XX sin dato (`interpretaciones_sin_dato`),
los ceros (`lo_que_no_hay`), dónde está escrita la intuición sin fuente
(`la_intuicion_escrita`) y lo que resultó falso al medirlo (`correcciones`).

---

## 0. Lo que resultó falso al medirlo

1. **«Viciosos de comida de carne y pescado» no es de la costa.** FA3 (cm-s3) lo
   usaba para «esta gente»; Pérez de Tolosa lo dice de los caquetíos de los
   **Llanos** («aunque algo difieren en la habla á los de Coro», Fernández Duro
   t. II p. 234; Arcaya p. 46: «los Caquetíos de los Llanos»).
2. **La ficha `haviser-1990` decía «nada de ajuares con procedencia».** Vale para
   los dos entierros directos de 1980; las dos urnas de De Savaan (Curazao) traen
   objetos entre los huesos, y entre ellos **un diente de tiburón cada una**
   (pp. 230-231, en imagen).
3. **Un botuto con la punta rota no es una bocina** (el criterio de cm-n3). En Las
   Aves, 397 botutos dabajuroides tienen la espira agujereada «which facilitated
   the extraction of the animal» (Antczak 2015 p. 9, en imagen).
4. **La «teogonía karibe» con un espíritu de las olas** que Antolínez atribuye a
   La Borde («Curumón, las olas; Sabácu, las tempestades») **no está en Breton**:
   `couloúmon` es una constelación que anuncia el estado del mar.
5. **Rouse y Cruxent 1963 pesa 0 bytes** en el repo.

## 1. Veredicto en una frase

El mar es **esencial en la vida** de los caquetíos de la costa y lo dicen las
fuentes —despensa, moneda, camino a las islas, parientes al otro lado, el nombre
mismo de Paraguaná—; en su **creencia** no aparece nunca, y no por falta de
buscar: donde las crónicas ponen lo sagrado de esta gente lo ponen en el
**cielo** (el Manaure «da los temporales», el boratio adivina «si lloverá») y en
el **maíz** (los ayunos, los funerales y el ajuar son de mazamorra y maçato). La
intuición de Miguel queda como lo que es: **intuición**, ahora con el cero
medido y con una hipótesis más fina que la de antes.

## 2. Dato, inferencia, intuición

**DATO** (atestiguado, de la costa o de las ABC, con su época):

- La comida del rito es de maíz: el ayuno de la cura («magamorra rala de mahiz
  que ellos llaman caça»), el ayuno de la guerra y los dos funerales, con los
  huesos en `maçato` (Oviedo t. II pp. 297, 299, 300, 329) — **cm24-01**.
- El poder sagrado del gran señor es del cielo: «da los temporales» (Ampíes,
  antes de 1527, Fernández Duro t. II p. 212) y hace «las llubias, granizos,
  truenos y relampagos y eladas y secas» (Aguado lib. I cap. I, **primaria nueva
  en el repo**), y vive «diez leguas la tierra adentro» — **cm24-02**, que da a
  creencia-013 la fuente que le faltaba.
- La pesca se adivina con tabaco, como caminar, sembrar, cazar o el amor, y
  «cada uno es boratio» (Oviedo p. 298) — **cm24-03**: el único acto ritual
  atestiguado que toca el mar, y no lo distingue.
- La concha vale lejos del mar: los ayamanes, «tan lejano del mar que no lo
  conocen», se adornan con «conchas marítimas que compran a otras naciones»
  (Federmann p. 45); en la costa, «como de monedas» (Arcaya p. 120) —
  **cm24-05**.
- El otro lado del mar es familia, y se cruza para visitarla: los indios de la
  costa «muchas veces se pasaban allá á holgar» con los de Curazao, Aruba y
  Bonaire, y le mandan a Ampíes «un cacique que se dice D. Juan Baracoica, que
  está en las islas y es su pariente y deudo» (Ampíes p. 212) — **cm24-06**.
- En Curazao, s. XIII-XIV, dos urnas dabajuroides con un diente de tiburón cada
  una, discos de concha, ostra perlera y huesos de pez entre los huesos (Haviser
  1990 pp. 230-231), con el condicional del excavador — **cm24-a01**. En la costa
  de Falcón, junto a la urna, el cuenco para beber (Oliver p. 442) — **cm24-a02**.
- La iconografía dabajuroide: batracio, ave, murciélago, cara, sol; petroglifos
  costeros «geométricos y abstractos» — **cm24-a04**.

**INFERENCIA** (reconstruido: análisis de un dato, o comparanda con su etiqueta):

- La tierra de los muertos está **abajo**: `sawaka`, «baha na sawaka» 'bajar al
  inframundo, morir' en papiamento viejo, atribuida al caquetío por van Buurt
  (p. 35) — **cm24-07**. No mar adentro.
- El mar da nombre a la tierra y a la gente de la esfera: Paraguaná en boca de
  los indios en 1540 (Oviedo t. I p. 205) con `para` 'mar'; los paraujanos,
  «gentes de la orilla del mar» (Jahn p. 191) — **cm24-08**.
- En los vecinos, el mar SÍ entra en la creencia, cada uno a su manera (§3 del
  YAML; nada se proyecta):
  - **kalinago** (Breton, s. XVII, primera minería en el repo): no se echan al
    mar cuando sale el Can Mayor, que trae los huracanes (1665 p. 348); el
    garzón celeste «se plonge en la mer» al ponerse (p. 165); el manatí no se
    come, por los ojos de los hijos (p. 275). En Breton, ningún dueño del mar;
    Goeje (p. 38) da `Umeku` 'espíritu que causa los naufragios', sin decir de
    quién lo toma;
  - **taíno**: el mar nace de la calabaza de Yaya, donde los huesos del hijo se
    volvieron peces que se comen (Pané caps. IX-X); una mujer «en el fondo del
    mar» da las joyas que los reyes tienen por sagradas (Anglería p. 342); al
    reverso se le habla antes de soltarlo contra la tortuga (Oviedo pp.
    435-436). Que el ser supremo, «Yocahu Vagua Maorocoti», lleve el mar en el
    nombre **no lo dice ningún cronista** (Las Casas: «no sé lo que por este
    nombre quisieron significar»): es etimología de Coll y Toste, 1897;
  - **lokono**: Orehu, la mujer de las aguas, da la maraca (Brinton p. 18, que
    lo toma de Brett 1868);
  - **wayuu**: Pulowi y las tortugas, sólo en una tesis que lo cita de terceros;
    Pulowi sale 0 veces en Jahn y en el Cuadernillo. Jepirá es un cabo por el
    que se pasa hacia sabanas con ganado (Jahn p. 184);
  - **achagua** (control, la hermana de los Llanos): su «mar» es la laguna
    (`manoa`), y su rito de pesca es de río: el piache inciensa con tabaco el
    pescado al abrir las pesquerías (Rivero p. 105).

  La rima más fuerte, sólo lectura: el **tabaco antes de pescar** —el caquetío
  lo lee él mismo, el achagua lo pone en manos del piache, el taíno le habla al
  pez—, y la **mujer del agua que da las insignias** (Guabonito, Orehu), que en
  el caquetío no tiene nada que le corresponda.

**INTUICIÓN** (sin fuente):

- Que hubiera un **dueño del mar** al que el pescador pide permiso: no está en
  ninguna fuente caquetía ni en la comparanda del repo. Está escrito en tres
  sitios del proyecto y en **un prompt que el motor enseña** (§4 abajo).
- Que el mar fuera **esencial en la cosmovisión** (mito de origen, rito, deidad
  marina): ninguna fuente caquetía; y las que hay apuntan a otro lado.

La hipótesis que queda, más fina que la de antes y todavía hipótesis: **lo
sagrado caquetío que conocemos es del cielo y de la tierra de labranza; el mar
es lo cotidiano, lo que se trueca y lo que se cruza para ver a los parientes**.
Si el mar tuvo su propio mundo simbólico, las crónicas de la costa no lo vieron,
y la arqueología de la costa tampoco lo muestra.

## 3. Lo que NO se encontró (ceros medidos; ver `lo_que_no_hay`)

- Un dueño, espíritu, madre o ser del mar caquetío. Las voces caquetías de
  creencia y las del mar no comparten ni una glosa.
- Un mito caquetío del origen del mar, de los peces o de las islas.
- Una ofrenda, un canto, un conjuro, un tabú o un día prohibido del mar.
- El alma o el muerto que va al mar.
- El mar en el poder del Manaure.
- Un objeto marino dentro de una urna de la costa de Falcón, una imagen marina
  en la loza o en la piedra caquetía, una bocina de botuto dabajuroide.
- Sirenas o encantos del mar en la tradición paraguanera del s. XX (Esteves,
  Medina).

**Control positivo**: el mismo barrido encuentra creencia × cielo en las mismas
obras (columna de control de `meta.medido`), y la lectura lo confirma.

## 4. La intuición ya está en el motor

`curiana_sim/curiana_agents_era2.py` (generado desde `6-fusion/elenco_era2.yaml`),
el system prompt de **Jachos**, apopo y boratio de pueblo de GUARANAO, tier 1:

> «Nunca botas la canoa sin pedir permiso al dueño del agua. Viste ahogarse a un
> tío por salir un día prohibido.»

Es **la única frase de los 63 prompts de la era 2** que enseña un ser del agua
(medido: frases del system prompt con un término del agua y uno de creencia; las
otras dos son estilo y un sueño). Consecuencia, por la regla de Miguel del
2026-09-23 —*lo que emerge es el producto*—: si un run habla del dueño del agua,
**no es emergencia, lo enseñó el motor**. Y está escrito también, sin fuente, en
`3-mundo/CULTURA_CAQUETIA.md` §1 («[reconstruido] … el mar, los bancos de peces
… Por eso el pescador pide permiso antes de botar la canoa») y §4 («piden
permiso al mar en voz baja»).

## 5. Decisiones para Miguel

**(a) El «dueño del mar» de `CULTURA_CAQUETIA.md` §1.** Está marcado
`[reconstruido]` y la etiqueta exige comparanda citada; no cita ninguna, y del
«pide permiso» no hay nada ni en los vecinos.
- A — bajarlo a `[hipotético]` y sacar «el mar» y «el pescador pide permiso» de
  la lista hasta que haya fuente, dejando los dueños que sí tienen rastro (el
  bosque del cerro, Capó, creencia-021; cerros y salinas, creencia-015,
  retro-abstraído); y §4 se ajusta igual.
- B — dejarlo `[reconstruido]` citando la comparanda del mar de §3.
- C — no tocarlo.
- **Recomiendo A**: en duda, degradar (regla 2), y la comparanda no dice «pedir
  permiso».

**(b) El prompt de Jachos.**
- A — cambiar el dueño del agua por la adivinación atestiguada (cm24-03): *«Nunca
  botas la canoa sin leer el tabaco. Viste ahogarse a un tío por salir un día que
  el tabaco negaba.»* Guarda el personaje (el boratio que decide qué día no se
  sale al agua) y lo ancla en Oviedo p. 298. El prompt se mueve −6 caracteres
  (r = −0,48: se dice aunque sea poco).
- B — dejarlo y declararlo: etiqueta `canon-simulacion` en el elenco, y en los
  análisis «dueño del agua» cuenta como enseñado, no emergente.
- C — quitar la frase sin reemplazo.
- **Recomiendo A**, en el próximo corte de instrumento (no a mitad de serie):
  se genera desde `elenco_era2.yaml` con `generar_agentes_era2.py`.

**(c) Qué pasa al corpus.**
- A — fusionar los atestiguados: cm24-01, cm24-03 y cm24-04 a `creencia.yaml`;
  cm24-02 como `procedencia` de creencia-013 (Ampíes p. 212 + Aguado lib. I cap.
  I); cm24-05 a ecología/comercio; cm24-06 a parentesco; cm24-a01 y cm24-a02 a
  creencia (muerte), acotados; cm24-07 y cm24-08 como `reconstruido`.
- B — sólo cm24-02 (la procedencia de creencia-013) y cm24-01.
- C — nada; que quede en `6-fusion/`.
- **Recomiendo A.**

**(d) La comparanda de los vecinos.**
- A — una sección «comparanda del mar» en `creencia.yaml`, etiquetada por lengua,
  sin proyectar.
- B — dejarla en `6-fusion/` como referencia.
- C — llevar algo al motor (p. ej. el tabú kalinago del Can Mayor como voz de
  fuera).
- **Recomiendo B**: no es del caquetío, y cargarla en el corpus caquetío invita a
  proyectarla. Si un día se simula la esfera, está aquí.

**(e) Dos notas del lexicón que la campaña encontró.**
- `barana` (kalinago): su nota dice «cognado de CQ para, LK bara», y Goeje p. 55
  la da como forma de **hombres**, caribe/tupí (`parana`); la del lado arahuaco
  es la de mujeres, `balaua`. A — corregir la nota (no la glosa); B — anotar
  sólo; C — nada. **Recomiendo A**, por `fusionar-propuesta`.
- `sawaka` es `caquetío-atestiguado` con una voz de papiamento que van Buurt
  atribuye «with a subjective element». Por la regla 2 sería `reconstruido`,
  pero es la raíz del nombre del boratio mayor del elenco (Sawaka), y bajarla
  mueve el elenco. A — degradarla midiendo antes qué arrastra; B — anotar y
  decidir en la próxima tanda del lexicón; C — nada. **Recomiendo B.**

**(g) Las correcciones de cita y de canon que salieron de paso** (§6 y
`correcciones`).
- A — aplicarlas todas por `fusionar-propuesta`: las de página y procedencia
  (creencia-009, transmision-018, lx.13, la ficha de Brinton); añadir a `notas`
  de `huracan` y `cobo` que las primarias dicen «tormenta» y «el cobo es el
  caracol de mar» (sin tocar la glosa: D7); y en `CULTURA_CAQUETIA.md` §1 dar a
  Juyá su procedencia del repo (Cuadernillo pp. 26-27; Jahn p. 362), marcar
  Pulowi como sin primaria y dejar de llamar al wayuu «la lengua hermana» (D11).
- B — sólo las de página y procedencia.
- C — nada.
- **Recomiendo A**: son citas, no glosas; lo único que toca el canon es
  `CULTURA_CAQUETIA` §1, que (a) ya abre.

**(f) Cerrar cc.10.**
- A — cerrar la campaña como **negativa medida**: el mar es vida, no creencia,
  en todo lo que el repo tiene; se reabre sólo si entra una de las obras de
  `lo_que_no_hay.lo_que_no_esta_en_el_repo`.
- B — dejarla abierta y bajar Simón (dominio público) para medir el último cero
  de crónica.
- **Recomiendo A**: Simón copia a Aguado, que ya está medido; lo que podría mover
  el cero es arqueología de las ABC que no es libre o no está publicada.

## 6. Deudas y cosas vistas de paso

- **Aguado entra al repo** (`fuentes_caquetios/Aguado_1918_Historia_Venezuela_t1_gutenberg.txt`,
  dominio público, Project Gutenberg #39947; ficha `aguado-1581`): hda-13 pedía
  su clave. Se cita por libro y capítulo: Gutenberg no guarda la paginación.
- **Breton, primera minería** (estaba `pendiente`): desfases, ocho falsos ceros
  de grafía resueltos y la voz de mujeres `bálaoüa` 'mar' en su página (1666
  p. 242). Los ~400 pares hombre/mujer siguen sin leer.
- **Las copias de Dijkhoff 1997, Haviser 1990 y Mol 2007** sólo están en el
  scratchpad de esta sesión (política del 2026-09-22: no van al repo sin
  licencia). Sus URL y sha256 están en las fichas: se pueden volver a bajar.
- El desfase de Oliver cap. 4 es −27 en §4.7-4.15 y **−26** en el Apéndice C.
- Bitácoras escritas en las fichas barridas (ver el commit).
- **Correcciones de cita que salieron de paso** (propuestas, no aplicadas; ver
  `correcciones` del YAML y la decisión g): creencia-009 cita «Jahn 1927:229»,
  que es la página del PDF (la impresa es 184), y su «pesca» del más allá no
  está en Jahn; transmision-018 y la ficha de Anglería citan el areíto en «vol.
  4, p. 236», que es PDF (impresa 228); `taino2_las_casas_apologetica` lx.13 lee
  «Yagua» donde la imagen dice «Vagua»; la ficha de Brinton decía que no nombra
  al misionero de Orehu, y lo nombra (Brett, nota 49).

🤖 Generado con [Claude Code](https://claude.com/claude-code)
