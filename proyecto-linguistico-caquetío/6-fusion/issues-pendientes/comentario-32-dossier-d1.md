# Dossier D1 — el veto de la genealogía propuesta

> Borrador de comentario para [#32]. Publicar con:
> `gh issue comment 32 --body-file 6-fusion/issues-pendientes/comentario-32-dossier-d1.md`
> (quitando esta cabecera). Preparado 2026-08-31 para la tanda de decisiones.

---

## Primero, el refresco (el issue apunta a rutas de otra era)

La propuesta vive hoy en **`3-mundo/corpus/genealogia.yaml`** (no
`curiana_sim/cultura/`), el ensayo es **`3-mundo/ensayos/01_familia_caquetia.md`**,
y `DECISIONES_ABIERTAS.md` se retiró el 2026-08-06. El validador del corpus
la cruza contra `ALL_AGENTS` en cada corrida de guardianes (hoy: 6 linajes ·
60 agentes · 14 personas de fondo, todo en verde).

## Qué propone exactamente (para vetar con precisión)

1. **Seis linajes matrilineales** como estructura: Buio (piache/visión),
   Chiriware (guerra), Corie (agricultura), Paugis (medicina/partería), y dos
   sin tótem fijado — **Kaira** (linaje materno de Manaure) y **Warana** (el
   de Nubiri-sha). Cada uno con su `capacidad_de_expansion` escrita: es la
   lista de casting para crecer el elenco.
2. **La sucesión de Manaure**: hermana propuesta **Itana-sha** (fondo) y su
   hijo **Waimo-ko**, "sobrino uterino y sucesor natural" (fondo — NO es
   agente).
3. **~14 personas de fondo** (madres, esposas, la fundadora Kaira-sha) que
   dan consistencia sin inflar el elenco.
4. `curiana_agents.py` **no se toca**: es propuesta en datos, regla 5.

## Lo que cambió desde que el issue se escribió (la evidencia nueva)

- **El canon matrilineal quedó asentado** (sesión 1/4 del corpus): el
  precontacto es matrilineal; el dato patrilineal de Oliver es del cacicazgo
  **colonial**. Pero ojo: la ficha de Manaure ya carga un dato patrilineal
  del propio canon ("heredó de su padre el control de las rutas de biro") —
  la propuesta lo declara como **tensión deliberada**, no lo esconde.
- **Manaure es un título, no un nombre** — cuatro testigos independientes
  (Antolínez 1944, Acosta Saignes, Dupouy, González Batista). "Suceder a
  Manaure" es suceder a un CARGO. Y el matiz de Acosta Saignes ("de padres a
  hijos") sigue sin resolver — es material de D4 (#35), no de D1.
- **parentesco-038 (hipotético)**: la sucesión del diao tiene TRES puertas —
  elegibilidad matrilineal, ratificación política de los apopos/diaos, y
  legitimación espiritual (boratio). Heredar la puerta 1 no da las otras dos.
- **parentesco-039 (hipotético, con comparanda ashanti/taíno)**: un
  **heredero único es una simplificación** — lo documentado es pluralidad de
  candidatos (varias hermanas con hijos) y el poder real está en ELEGIR
  entre ellos. La poligamia atestiguada de Manaure (parentesco-015) lo hace
  plausible. La propuesta actual tiene UN candidato: contradice su propio
  corpus.
- **El dato estructural más cargado** está en el linaje Warana: los hijos de
  Manaure con Nubiri-sha son del linaje de ELLA — la casa del cacique cría
  hijos que no heredan. Es la matrilinealidad haciendo drama sola.
- **El contexto de hoy** (decisión de Miguel, 2026-08-31): la simulación se
  extenderá a más nodos y lo desarrollado por los personajes de las primeras
  tandas no se reutiliza. Eso ABARATA aprobar: los linajes son exactamente
  las unidades de expansión que esa extensión necesita, y no hay historia
  vieja que proteger.

## Los cuatro ejes de la decisión (no es sí/no)

| Eje | Qué se decide |
|---|---|
| 1 · Los linajes | ¿Los 6 como estructura canon-simulación? (incluye fijar o delegar tótem/nombre de Kaira y Warana) |
| 2 · El sucesor | ¿Waimo-ko como "sucesor natural" — o degradado a "candidato elegible (puerta 1 de 3)"? |
| 3 · El fondo | ¿Las ~14 personas de fondo entran como canon-simulación? |
| 4 · La etiqueta | Todo entra como `canon-simulacion`, nunca atestiguado — la genealogía es diseño nuestro sobre patrón atestiguado |

## Las opciones, con su contra

**A · Aprobar tal cual.**
- Contra: canoniza al heredero único que parentesco-039 ya corrigió, y
  "sucesor natural" afirma lo que parentesco-038 dice que son tres
  reconocimientos distintos.

**B · Aprobar estructura, degradar al sucesor** *(recomendada)*: los 6
linajes y las 14 personas de fondo entran; Waimo-ko se queda pero su línea
cambia de "sucesor natural" a **"candidato elegible (puerta 1 de 3;
pluralidad de candidatos pendiente por parentesco-039)"**. No se inventa el
segundo sobrino hoy: queda como expansión aprobada.
- A favor: alinea la genealogía con su propio corpus; deja la sucesión como
  material dramático abierto (que es lo que las fuentes soportan); cierra D1
  sin esperar D4.
- Contra: el linaje Kaira queda con un solo candidato nombrado un tiempo
  más — aceptable porque es fondo, no agente.

**C · Aprobar linajes, rechazar toda la rama de sucesión** (Itana-sha,
Waimo-ko, Kaira-sha fuera hasta que D4 resuelva el matiz patrilineal).
- Contra: deja al linaje del diao vacío — justo el que la extensión a nodos
  necesita poblado — y D4 no tiene fecha.

**D · Veto total.**
- Contra: bloquea V3 (notas por agente) y J1 (qué se publica), y desarma la
  unidad de expansión en el momento en que se decidió expandir.

## Qué implica aplicar (si sale B)

Un cambio de UNA línea en `genealogia.yaml` (la redacción de Waimo-ko) vía
aplicador de tanda, y el resto es marcar la decisión: los linajes pasan de
"propuesta" a canon-simulación en el encabezado del archivo. La condición 6
del gate queda a falta solo de D3.
