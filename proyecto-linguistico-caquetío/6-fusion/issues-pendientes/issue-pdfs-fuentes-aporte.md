Servir los PDF del vault desde `/simulador/fuentes`, tras un aporte voluntario

## De dónde sale esto

La wiki de fuentes (`/simulador/fuentes`, 62 páginas) publica **lo que
resolvimos y minamos de cada obra**, pero no la obra. Miguel lo señaló el
2026-08-24 con la pregunta obvia: *"pero no las tenemos en el mismo
proyecto?"*.

Sí las tenemos. `fuentes_caquetios/` son **38 PDF reales, 429 MB, los 42
archivos versionados en git** (4 están en 0 bytes y no cuentan). Hoy la ficha
enlaza a Internet Archive o al editor cuando el rastreo documental de
2026-08-14 encontró una URL — **14 de 40 fuentes**. Las otras 26 no ofrecen
ninguna vía de lectura, aunque el PDF esté en el repo.

## Por qué servir nuestra copia es mejor que enlazar afuera

No es solo comodidad. **Las notas citan la paginación de nuestro ejemplar**:

```
oliver-1989-apendice-a.md   "impresas 559-594 = pdf 586-621 (offset -27)"
alvarado-1921.md            "glosario impreso 1-318; offset PDF = +30"
01-rastreo-fuentes.md       "Tamers 1970, las tres relevantes, todas en la p. 512"
```

Un enlace externo puede llevar a **otra edición con otra paginación**, y
entonces la cita deja de ser verificable — que es justo lo contrario de lo que
`bibliografia.yaml` logró al volver `procedencia.obra` una clave foránea.

## 🔴 El reparto por copyright, medido

La carpeta se parte casi por mitad, y la mitad de arriba es la que más se cita:

| | MB | Obras |
|---|---|---|
| **Dominio público** (publicación pre-1930) | **213** | Adam 1879 · Alvarado 1921 · Anglería 1892 (vols. 1 y 4) · Arcaya 1920 · Gilij 1780/1782/1783 · Jahn 1927 · Las Casas 1875 · Oviedo y Baños · Oviedo y Valdés 1851 |
| **Modernas con copyright** | **216** | Antczak 2015 y 2017 · Camacho 2011 · Esteves 1989 (6 partes) · Guerra Curvelo 2023 · Martínez Cruzado 2003 · Moreno-Mayar 2018 (*Science*) · Oliver 1989 (tesis + caps. 2 y 3) · Perea Alonso 1942 · Schroeder 2018 (*PNAS*) · Urbina 2007 y 2011 · Zavala Reyes 2015 y 2018 |

**Las 12 de dominio público son republicables sin más.** Las modernas no: son
artículos de revista con editor, tesis y monografías. Publicarlas en abierto
bajo el dominio de Curiana Radio es redistribución.

⚠️ **Pero el segundo grupo no es homogéneo** y hay que mirarlo obra por obra
antes de descartarlo entero. Al menos cuatro parecen tener licencia que sí
permite redistribuir, según el rastreo de 2026-08-14:

- **Oliver 1989** — depositada por el propio autor en UCL Discovery, acceso abierto
- **Zavala Reyes 2015** — *Boletín Antropológico* (ULA)
- **van Buurt 2014** — el autor la distribuye libremente
- **Antczak et al. 2017** — el informe la anota como *"open access (CC)"*

Ninguna de esas cuatro licencias se verificó leyendo los términos. Es trabajo
pendiente, no un hecho.

## Lo que Miguel decidió el 2026-08-24

1. **Los PDF van detrás de un aporte voluntario**, no en abierto. La wiki
   (nuestro análisis) sigue libre; el acceso a los documentos es lo que pide
   el aporte.
2. **Presentación: visor embebido + descarga.** Hojear sin salir del sitio,
   poder ir directo a la página citada, y un botón para bajar el archivo.
3. **No se construye todavía.** Esto queda como issue.

## Lo que queda por decidir

- **Qué entra tras el aporte.** Si el dominio público se sirve libre y el
  aporte cubre solo curaduría/infraestructura, o si todo el visor va detrás
  del aporte por igual. Cobrar por obras de dominio público es legal, pero es
  una decisión editorial que conviene tomar a conciencia.
- **Las 20 modernas con copyright.** Un paywall **no** resuelve el problema
  legal — redistribuir cobrando es peor, no mejor. La opción realista es
  seguir enlazando afuera para esas, y servir solo lo que podemos.
- **Verificar las 4 licencias abiertas** de arriba, leyendo los términos.
- **Pasarela de pago.** El proyecto no tiene ninguna. Coincide con la
  monetización pendiente de `/galeria` (V1 salió sin checkout) — conviene
  resolverlo una sola vez para las dos aristas.
- **Coste.** 213 MB en Vercel Blob es trivial en almacenamiento; el gasto real
  es el ancho de banda de PDF de 20-37 MB. El pre-redimensionado que hizo la
  galería no aplica: un PDF no se sirve en escalera.

## Precedente de infraestructura que ya existe

- `scripts/galeria-ingesta.mjs` ya sube a Vercel Blob con `put()`.
- `types/galeria.ts` ya modela **licencia por obra** (`TipoLicencia`,
  `LicenciaObra`) — el mismo problema, ya pensado para imágenes. Vale la pena
  reusar ese esquema en vez de inventar otro para documentos.
- `content/wiki/**/*.json` ya lleva `lectura_url` por página, extraído del
  campo `acceso` del frontmatter. Añadir un `pdf_url` al lado es una línea en
  `export_wiki_seed.py`.

## Alcance mínimo si se retoma

1. Verificar licencia de las 4 candidatas de acceso abierto.
2. Subir a Blob las 12 de dominio público (+ las que sobrevivan al paso 1).
3. `pdf_url` en el seed del wiki, junto a `lectura_url`.
4. Visor embebido + descarga en la ficha, tras el muro de aporte.
5. Las modernas con copyright: se quedan con enlace externo, y la ficha dice
   por qué — que es información útil, no una carencia que esconder.
