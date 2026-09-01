---
tipo: diseño
ambito: la era 2 — la simulación multi-nodo de Paraguaná
estado: diseño aprobado en conversación (2026-09-01); ingeniería sin empezar
decidido: 6-fusion/decisiones_tanda_2026-09-01.yaml §rumbo_era2 y siguientes
---

# DISEÑO ERA 2 — Dos clanes, un cerro sagrado, una koiné

> **La visión de Miguel** (2026-09-01): *"nodos que conversen entre sí...
> distintos nodos culturales, con overlaps obvios, pensando en cómo estaba
> estructurada la sociedad según las fuentes y siguiendo el orden
> geográfico."* Este documento es el paso 2 de la ruta aprobada: el diseño
> ANTES del código. Nada de aquí está implementado.

---

## 1 · La pregunta, y por qué necesita dos nodos

La fase 1 dejó escrito su límite: dentro de UNA comunidad, la convergencia
"desplaza de entrada y sostiene" — no se acumula, así que no hay proceso que
observar. Una koiné no se forma dentro de una unidad homogénea: se forma
donde **nodos distintos tienen que entenderse**.

La era 2 construye esa condición: **dos comunidades de habla con semillas
léxicas parcialmente distintas, un canal de contacto con geografía real, y
la métrica puesta en el CRUCE** — cuántas formas atraviesan la frontera y se
fijan en ambos lados.

**Sembrar divergencia para medir convergencia.** Sin semillas distintas por
nodo, dos nodos son decorado. Con ellas, cada forma que cruza es un evento
observable con ruta (quién la dijo, dónde, quién la adoptó).

Resultados posibles, ambos válidos: plateau de cruce **alto** = koiné;
plateau **bajo** = diglosia estable. El instrumento detecta estabilidad; el
nivel al estabilizarse dice qué pasó.

## 2 · Los nodos — calcados, no inventados

| Pieza | Fuente |
|---|---|
| Dos sub-grupos caquetíos con territorios y pesca excluyentes: **Amuayes** y **Guaranaos** | Oliver 1989 pp. 275-276, citando González Batista 1984 |
| Asentamientos: Amuayes en Cayerda→Moruy; Guaranaos en Santa Ana | Delmonte 1883 vía González Batista (cadena declarada) |
| Un jefe supra-aldea por clan; ambos bajo el polity costero (Manaure) | Oliver p. 276 |
| Fronteras inter-aldea por **matrimonio y parentesco** | Oliver p. 275 (modelo cacicazgo taíno) |
| Cabecera religiosa del polity en Paraguaná | Salas vía Antolínez 1944 |
| El Capubana (Cerro Santa Ana) como morada de Capo | D9; Velasco 2015 (Cerro de Capú) |
| Merejuy: fermento de la chicha ritual, hecho en Moruy | tradición local vía Miguel (deuda: sin-procedencia) |
| El agua de Chamuriana, el manantial de Maitiruma, el bosque xerófito | Miguel sobre el mapa vivo, 2026-09-01; Esteves (Maitiruma) |

**El modelo espacial** (canon-simulación, síntesis nuestra sobre esas piezas):

- **Nodo GUARANAO** y **nodo AMUAY** — territorios de clan a escala
  península, no pueblos-punto (el pueblo-punto es categoría colonial:
  Santa Ana es fundación franciscana, veredicto de Miguel). La asignación
  norte/sur queda EN VERIFICACIÓN: los homónimos modernos (Amuay al NO,
  bahía de Guaranao al sur) parecen invertidos respecto a Oliver.
- **El conglomerado del CAPUBANA como centro sagrado COMPARTIDO** — no es
  capital de ningún clan: es donde los dos convergen. Sitios con función:
  **Moruy** (el merejuy, la chicha ritual), **Chamuriana** (el agua que
  baja del cerro), **Cayerúa** al norte; el manantial de **Maitiruma** al
  pie este. Cuatro capas independientes apuntan al mismo cerro: asiento
  religioso (Salas) + morada de Capo (D9) + fermento ritual (merejuy) +
  anomalía de agua y bosque xerófito (mapa).
- Registro completo de lecturas y probabilidades:
  `6-fusion/toponimia_paraguana_miguel.yaml` y
  `6-fusion/paraguana_dos_clanes.yaml`.

## 3 · El elenco — por arquetipos, no por número

Directiva: *"tenemos que tener a todos los arquetipos de la familia;
teniendo el arquetipo mínimo de familias armamos los dos nodos."*

La plantilla ya existe — es el **grupo residencial creíble** de
`genealogia.yaml` (D1): **matriarca + hermanas con hijos + hermanos adultos
+ esposos de otros linajes**. Derivación:

- ~8-10 personas por linaje completo (2-3 adultas de núcleo, 1-2 hermanos,
  esposos entrantes, niños tier-3);
- **2 linajes por nodo** (4 de los 6 linajes de D1, reasignados a clanes;
  los otros 2 quedan de reserva de expansión);
- **esposos exogámicos cruzados** entre nodos (2-3 por lado) — por
  matrilocalidad, el esposo vive en el nodo de ella: son los **portadores
  permanentes** de formas;
- total estimado: **35-40 agentes** (~la mitad del elenco viejo, para el
  doble de días al mismo costo).

**Bibliografía base por participante** (directiva: *"sí o sí"*): cada
agente del elenco nuevo lleva su dossier — qué hechos del corpus, qué
linaje de D1 y qué obras lo sostienen. Es la tarea V3 (notas por agente)
elevada a requisito del casting: **nadie entra al elenco sin sus fuentes.**
Las tres puertas de la sucesión (parentesco-038) son regla del modelo, y la
pluralidad de candidatos (parentesco-039) por fin se ejecuta: el linaje del
diao entra con más de un sobrino elegible.

## 4 · El contacto — el canal que la fuente escribió

1. **Los esposos exogámicos** — contacto continuo, de baja intensidad:
   cada uno habla su variante de origen dentro del nodo del cónyuge.
2. **Las ceremonias del Capubana** — contacto periódico, de alta
   intensidad: escenas en el centro sagrado donde asisten delegaciones de
   ambos clanes (la chicha de merejuy, el agua, el rito). Frecuencia de
   diseño: por definir en implementación (candidata: estacional/lunar, que
   el calendario de curiana_state ya modela).
3. **Sin canal artificial**: nada de "mercados" inventados — el comercio
   real del polity (sal, pescado, rutas de biro) puede montarse en las
   ceremonias, que es donde las fuentes lo soportan.

## 5 · La campaña episódica — un mundo, por entregas

Directiva: *"cada run por partes... espacios intermedios, pero cuando
hacemos un run sigue de alguna forma la narrativa del primero."*

- La era 2 es **UNA campaña**: un solo mundo persistente, ejecutado en
  **episodios** (runs encadenados).
- Entre episodios, el estado completo persiste: mundo (día, estación,
  eventos), **memorias biográficas**, idiolectos, koiné emergida,
  relaciones.
- **Los espacios intermedios son donde se cura**: análisis del episodio,
  fusión de lo emergido (los neologismos que cruzaron → ¿entran al
  léxico del episodio siguiente?), ajustes DECLARADOS (nada cambia en
  silencio entre episodios), y el reporte.
- El episodio siguiente **retoma la narrativa**: mismos personajes, sus
  recuerdos, sus deudas y alianzas.

## 6 · La memoria — dos capas por agente

1. **Lingüística** (ya existe): el idiolecto acumulado de curiana_koine —
   cómo hablas, qué formas arraigaste.
2. **Biográfica** (nueva): el **diario consolidado** — cada N días
   simulados, una pasada barata por agente resume sus decisiones,
   convicciones y relaciones cambiadas; el resumen se inyecta en sus
   prompts siguientes y persiste entre episodios. Directiva: *"que pueda
   recordar sus decisiones, convicciones, etc."* En una campaña de meses
   simulados, esto separa personajes que evolucionan de loros con contexto.

## 7 · La medición y la regla de parada

- **Métricas por nodo**: convergencia *dentro* de cada nodo (se espera
  rápida — fase 1) y **entre nodos** (la estrella: formas cruzadas y
  fijadas, con ruta de contagio).
- **Regla de parada por plateau** (directiva del sweet spot): piso de
  **una estación completa** + detector de plateau en la métrica
  entre-nodos (pendiente ~0 sobre ventana de N días) + techo de
  presupuesto. El plateau se evalúa en los espacios intermedios, no
  en caliente.
- **La mini-ablación de compañía** (aprobada: *"sería nuestro
  comparativo"*): 10-15 días, mismo setup y semillas, inyecciones de
  convergencia apagadas — incluido el rescate (D3: en ablación no hay
  rescate). Es la vara contra la que se lee la señal del run grande.
- **D3 aplicada rige el scoring**: el score almacenado es CRUDO siempre;
  el rescate usa el umbral normalizado por dialecto. Los perfiles
  dialectales por nodo se definen con las semillas (dos variantes
  caquetías, no las etnias foráneas de la era 1).
- Estatus epistémico declarado: **piloto exploratorio** (n=1 campaña +
  comparativo corto). Mide si el instrumental multi-nodo funciona y si
  hay señal; no confirma la tesis por sí solo.

## 8 · La ingeniería que falta (el costo real del diseño)

| Pieza | Dónde | Tamaño |
|---|---|---|
| Pertenencia agente→nodo y nodo→territorio/sitios | curiana_state, curiana_agents | medio |
| Escenas inter-nodo (ceremonias del Capubana) en el calendario | curiana_state | medio |
| Semillas léxicas divergentes por nodo | curiana_koine (FORMAS_SEED por nodo) | chico |
| Métricas dentro/entre nodo + detector de plateau | curiana_koine, curiana_observer | medio-grande |
| Columna `nodo` en el esquema (turns/agent_responses/word_uses) | curiana_database, Supabase | chico |
| Serialización/reanudación de campaña (episodios) | curiana_orchestrator_v2, curiana_database | grande |
| Diario consolidado por agente | curiana_observer o módulo nuevo | medio |
| Elenco nuevo desde los linajes, con bibliografía base (V3) | curiana_agents + 3-mundo | grande, y es curaduría con Miguel |
| Modelo de costos por episodio (medir contra los runs viejos) | analizar_runs + Supabase local | chico |

Orden sugerido: costos → esquema/pertenencia → semillas y métricas →
episodios → diario → elenco (lo último porque es curaduría, no solo
código — y puede avanzar en paralelo con Miguel).

## 9 · Lo que este diseño NO decide

- La asignación norte/sur de los clanes (verificación de mapa pendiente —
  la inversión Amuay/Guaranao respecto a Oliver).
- La frecuencia exacta de las ceremonias y el N del diario/plateau
  (implementación, con el modelo de costos delante).
- Qué neologismos cruzados entran al canon entre episodios (curaduría por
  episodio, regla 5).
- D15 (#90) — este diseño lo responde de facto (el par es
  Guaranao+Amuay con centro compartido); falta cerrarlo en GitHub con
  este documento como evidencia.

---

*Relacionado: [[DISENO_KOINE]] · [[ARQUITECTURA]] · [[esfera-de-interaccion]] ·
[[polities-caquetias]] · decisiones_tanda_2026-09-01.yaml ·
paraguana_dos_clanes.yaml · toponimia_paraguana_miguel.yaml*
