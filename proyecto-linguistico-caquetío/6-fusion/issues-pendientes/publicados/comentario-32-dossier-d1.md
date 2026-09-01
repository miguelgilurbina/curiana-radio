## ✅ DECIDIDA — opción B (Miguel, 2026-09-01) y APLICADA

**Veredicto**: *«el que era el heredero ahora es básicamente candidato... y sí o sí me gustaría que siguiéramos las tres puertas: la sangre matrilineal, el reconocimiento político de los otros diaos, y la legitimación espiritual del boratio»*.

Aplicado por `aplicar_tanda_09_01.py` (idempotente, `--dry-run`): los **6 linajes** y las **~14 personas de fondo** entran como `canon-simulacion`; **Waimo-ko degradado de "sucesor natural" a CANDIDATO ELEGIBLE (puerta 1 de 3)**; las tres puertas de parentesco-038 son **regla del modelo de sucesión** (el hecho sigue `hipotetico` como reconstrucción histórica); la pluralidad de candidatos (parentesco-039) queda como expansión aprobada, sin ejecutar. Registro completo: `6-fusion/decisiones_tanda_2026-09-01.yaml`.

Contexto que abarató la decisión: la simulación se re-arma para la era acotada (rumbo era 2 — un clan de Paraguaná primero) y los linajes son exactamente las unidades de casting que esa expansión necesita.

El dossier que la sirvió, para el registro:

---

## Primero, el refresco (el issue apunta a rutas de otra era)

La propuesta vive hoy en **`3-mundo/corpus/genealogia.yaml`** (no `curiana_sim/cultura/`), el ensayo es **`3-mundo/ensayos/01_familia_caquetia.md`**, y `DECISIONES_ABIERTAS.md` se retiró el 2026-08-06. El validador del corpus la cruza contra `ALL_AGENTS` en cada corrida de guardianes (6 linajes · 60 agentes · 14 personas de fondo).

## Qué proponía exactamente

1. **Seis linajes matrilineales**: Buio (piache/visión), Chiriware (guerra), Corie (agricultura), Paugis (medicina/partería), y dos sin tótem fijado — **Kaira** (linaje materno de Manaure) y **Warana** (el de Nubiri-sha). Cada uno con su `capacidad_de_expansion` escrita: la lista de casting para crecer el elenco.
2. **La sucesión de Manaure**: hermana propuesta **Itana-sha** (fondo) y su hijo **Waimo-ko**, "sobrino uterino y sucesor natural" (fondo — NO es agente).
3. **~14 personas de fondo** que dan consistencia sin inflar el elenco.
4. `curiana_agents.py` **no se toca**: propuesta en datos, regla 5.

## La evidencia nueva desde que el issue se escribió

- **El canon matrilineal quedó asentado** (sesión 1/4 del corpus): el precontacto es matrilineal; el dato patrilineal de Oliver es del cacicazgo **colonial**. La ficha de Manaure carga un dato patrilineal del propio canon ("heredó de su padre las rutas de biro") — declarado como tensión, no escondido.
- **Manaure es un título, no un nombre** — cuatro testigos independientes (Antolínez 1944, Acosta Saignes, Dupouy, González Batista). "Suceder a Manaure" es suceder a un CARGO. El matiz patrilineal de Acosta Saignes queda para D4 (#35).
- **parentesco-038**: la sucesión del diao tiene TRES puertas — elegibilidad matrilineal, ratificación política, legitimación espiritual. Heredar la puerta 1 no da las otras dos.
- **parentesco-039** (comparanda ashanti/taína): un heredero único es una simplificación — lo documentado es pluralidad de candidatos, y el poder real está en elegir entre ellos.
- El dato estructural más cargado, en el linaje Warana: los hijos de Manaure con Nubiri-sha son del linaje de ELLA — la casa del cacique cría hijos que no heredan.

## Las opciones que se sirvieron

**A** aprobar tal cual (canoniza al heredero único que el propio corpus corrigió) · **B** aprobar estructura y degradar al sucesor a candidato ← **elegida** · **C** linajes sí, sucesión fuera hasta D4 (deja vacío el linaje del diao) · **D** veto total (bloquea V3/J1 y la expansión).

Con esto y D3 (#34), la **condición 6 del gate queda cerrada**. Se cierra el issue.
