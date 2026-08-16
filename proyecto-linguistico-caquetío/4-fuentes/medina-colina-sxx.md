---
tipo: fuente
obra: "Del Habla Paraguanera. Siglo XX"
autor: "Medina Colina, Juan Bautista"
anio: s. XX
genero: lexico-regional
local: "⚠️ FÍSICO — ejemplar de Miguel; entra por dictado curado (+ foto/OCR si hace falta cobertura)"
capa_texto: no
estado_minado: en-curso
prioridad: alta
verificado: 2026-08-15
aliases: ["Medina Colina", "Del Habla Paraguanera", "habla paraguanera"]
---

# Medina Colina — *Del Habla Paraguanera. Siglo XX*

## Qué es, y por qué se esperaba

El diccionario de paraguanerismos que
[[02_protocolo_habla_paraguanera]] llevaba esperando **desde antes de saber su
título** — el protocolo se escribió a ciegas (*"no se pudo confirmar el título
exacto"*) y barajaba a Brett Martínez y Tito Guerra como candidatos. Era este:
**Juan Bautista Medina Colina**. Identificado por Miguel el 2026-08-15; existe
en su biblioteca, en físico.

Los dos bloqueos del protocolo cayeron: el libro apareció, y el OCR se instaló
el 2026-08-14 (tesseract + `ocr_fuente.py`).

## Por qué importa (resumen del protocolo — leerlo entero antes de minar)

1. Es **la fuente `retro-abstraido` canónica**: la marca existe en el programa
   del corpus y tiene **cero entradas** tras dos pasadas.
2. Ataca el **punto ciego estructural** del lexicón: fuerte en mercancías y
   títulos (lo que anotaron los cronistas), mudo en el oficio diario — peces
   por especie, médano, marea, cardumen. Si ese vocabulario sobrevivió, está
   fosilizado en el habla regional.

## ⚠️ El marco: sustrato indígena SIN filiación presunta

Paraguaná no era étnicamente homogénea y hoy eso se discute abiertamente. El
propio repo lo mide: [[esteves-1989]] reparte la toponimia peninsular en
**nueve estratos** (caquetío, taíno/caribe insular, cumanagoto, papiamento…),
y el lexicón ya separa `kalinago`, `jirajaroide-contacto`, etc.

**Ninguna voz de este libro entra como caquetía por defecto.** La cadena es:

```
paraguanerismo → ¿sustrato indígena? → ¿de cuál estrato? → etiqueta
```

y la evaluación de estrato usa el score de factibilidad del protocolo:
cognados en las comparandas (wayuunaiki, lokono, añú), fonotáctica (débil —
#91), atestación previa en el repo, referente ecológico del Golfete, y los
estratos toponímicos de Esteves como mapa de fondo.

## El método de entrada: dictado curado por Miguel

Miguel lee el ejemplar físico y dicta **las voces que su ojo de paraguanero
señala como posible herencia indígena**. Esa criba ES la marca
`retro-abstraido` — intuición informada local. Disciplinas acordadas:

1. **Página siempre** — sin página no hay cita, y sin cita no entra (regla 8).
2. **Glosa del libro tal cual**, corta y textual; el comentario de Miguel va
   aparte. Lo citable es Medina Colina, no la paráfrasis.
3. **Cobertura declarada**: al cerrar cada letra/sección, cuántas voces se
   vieron y cuántas se sacaron ("A: ~120 vistas, 9 dictadas"). Un futuro
   lector tiene que poder distinguir "no hay sustrato" de "no se miró"
   (regla 6).
4. **Colar dudosas**, no solo seguras: calibran el filtro.

### Formato de captura (una entrada)

```yaml
- voz: <forma tal como la escribe Medina Colina>
  glosa_libro: "<textual, corta>"
  pagina: <n>
  campo: <mar / fauna / flora / cuerpo / oficio / casa / clima / otro>
  nota_miguel: "<por qué le suena indígena; opcional>"
  dudosa: <true si va como calibración>
```

Las entradas se acumulan en la propuesta (`lexicon_medina_colina` o el YAML de
la bandeja cuando exista) — **nunca directo al lexicón** (regla 5).

## Qué se hace con cada voz dictada

1. Cruce contra lo que ya hay (lexicón activo, cognados, topónimos, propuestas)
   — como se hizo con la Tabla A-9: la mayoría de lo bueno suele estar ya, y
   entonces la voz vale como **atestación regional viva**, que también suma.
2. Score de factibilidad del protocolo → estrato más probable o "sin filiación".
3. Salida: propuesta con etiqueta (nunca mejor que `hipotetico` desde esta
   fuente sola) o hueco/descarte anotado aquí.

## Lo minado hasta ahora

*Nada aún. El dictado no ha empezado.*

## Enlaces

[[02_protocolo_habla_paraguanera]] · [[esteves-1989]] ·
[[oliver-1989-apendice-a]] · [[metodo-comparativo]] · [[lexicon]]
