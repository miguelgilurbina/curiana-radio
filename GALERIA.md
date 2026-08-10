# Galería visual

Sección de Curiana Radio junto a Archivo y Simulador. Publica los experimentos
de imagen generados con IA con su prompt y su procedencia a la vista.

- **Índice:** `/galeria` — mosaico justificado, orden aleatorio, lightbox.
- **Ficha:** `/galeria/<slug>` — imagen grande, concepto, prompt, licencia.
- **Fuente de verdad:** [`content/galeria/obras.json`](content/galeria/obras.json)
- **Tipos:** [`types/galeria.ts`](types/galeria.ts) · **Lectura:** [`lib/galeria.ts`](lib/galeria.ts)

## Infraestructura

Cuatro capas, ninguna con coste fijo:

| Capa | Qué | Dónde |
|---|---|---|
| Imágenes | Escalera WebP pre-generada (400/800/nativo) | Vercel Blob público |
| Entrega | El navegador pide al CDN directamente | Edge de Vercel |
| Metadatos | Manifest JSON versionado | git |
| Render | HTML estático generado en el build | — |

### Por qué NO usamos la optimización de imágenes de Vercel

`next/image` con optimización factura una **transformación por cada fallo de
caché**, más lecturas y escrituras de caché, y hace esperar al primer visitante
de cada variante mientras se genera.

Como las imágenes son estáticas y conocidas, la escalera se genera **una vez al
ingerir** y se sirve como archivos planos. Resultado: cero transformaciones
facturables y ninguna espera de generación. Por eso
[`ImagenObra.tsx`](components/galeria/ImagenObra.tsx) es un `<img>` con `srcSet`
y no un `<Image>`.

Medido sobre el volcado real (821 imágenes de Midjourney, 1,72 GB de PNG):

| | Por imagen | Total |
|---|---|---|
| PNG original | ~2.048 KB | 1,72 GB |
| Escalera WebP servida | ~167 KB | ~0,14 GB |

Con eso, el almacenamiento cabe de sobra en lo incluido en cualquier plan y la
transferencia ronda los 750 KB por visita del mosaico.

> **Ojo con el plan.** Hobby está restringido por política a uso personal no
> comercial. En cuanto se vendan licencias o impresiones hace falta Pro. Es un
> tema de contrato, no técnico.

### Peso del payload

Con ~800 obras, el manifest completo serializado al cliente pesaría más que las
imágenes de la primera pantalla. Por eso:

- `ObraGrid` (lo que cruza al cliente) es un tipo aparte del registro completo:
  sin `concepto`, sin `procedencia`, sin `originalKey`.
- El manifest guarda `blobBase` **una vez** y por obra solo los anchos
  disponibles. La URL se compone en el cliente. Guardar URLs completas serían
  ~200 KB de JSON repetido.
- El hueco se reserva con el **color dominante** (7 bytes) en vez de una
  miniatura borrosa en base64 (~400 bytes). A esta escala son 330 KB de
  diferencia antes de ver la primera imagen.
- El mosaico pinta una ventana de 60 piezas y crece al bajar
  ([`Mosaico.tsx`](components/galeria/Mosaico.tsx)).

## Publicar imágenes

### 1. Extraer

Deja los archivos **fuera del repo**:

```bash
Expand-Archive "$env:USERPROFILE\Downloads\midjourney_session_1.zip" -DestinationPath "$env:TEMP\galeria-fuente"
```

### 2. Preparar (local, sin credenciales)

```bash
npm run galeria:preparar -- "$env:TEMP\galeria-fuente" --serie archivo
```

Por cada imagen: extrae el prompt del nombre del archivo, genera la escalera
WebP en `.galeria-trabajo/` (ignorada por git), calcula el color dominante y
añade la obra al manifest. Es reanudable: salta lo que ya generó.

`--limite N` procesa solo las primeras N, para probar.

### 3. Subir

Vercel conecta los stores de Blob con **OIDC** por defecto: el proyecto recibe
`BLOB_STORE_ID` y un `VERCEL_OIDC_TOKEN` corto que rota solo, en vez de un
`BLOB_READ_WRITE_TOKEN` estático. El script acepta las dos vías.

**Con OIDC** (lo normal). En el store → pestaña **Projects** → ⋯ → *Update
Project Connection*, incluye el entorno **Development**. Después:

```bash
vercel env pull "$env:TEMP\curiana-blob.env"
```

```bash
npm run galeria:subir -- --env "$env:TEMP\curiana-blob.env"
```

**Con token estático**, si tu store sí creó `BLOB_READ_WRITE_TOKEN`:

```bash
$env:BLOB_READ_WRITE_TOKEN = Read-Host "Token"; npm run galeria:subir
```

En ambos casos el archivo de credenciales va **fuera del repo**. No uses
`vercel env pull` sin ruta: escribiría `.env.local` en la carpeta del proyecto,
que OneDrive sincroniza aunque esté en `.gitignore`.

La subida apunta `blobBase` al store y marca las obras como publicadas. Lleva
registro en `.galeria-trabajo/subidas.json`, así que reintentar solo sube lo
que faltaba.

### 4. Curar

Lo que el script no puede saber, y queda con valores conservadores:

| Campo | Valor por defecto | Qué hacer |
|---|---|---|
| `licencia` | `reservado` | Decidir obra por obra o por lote |
| `concepto` | vacío | Escribir statement en las que lo merezcan |
| `tags` | `[]` | Sin tags, la faceta «Motivos» no aparece |
| `titulo` | primeras 8 palabras del prompt | Reescribir las destacadas |
| `alt` | el prompt sin parámetros | Suficiente y honesto; mejorable a mano |

## El mosaico

[`lib/mosaico.ts`](lib/mosaico.ts) reparte las obras en **filas justificadas**:
cada fila ocupa el ancho exacto del contenedor y su altura la deciden las
proporciones reales de las imágenes que le tocaron. Solo la última fila queda
corta: no se estira, para no inflar dos imágenes sueltas hasta ocupar toda la
pantalla. Es un módulo puro, sin DOM.

Perillas:

| Dónde | Qué |
|---|---|
| `GAP` en `Mosaico.tsx` | Separación entre piezas (4px: casi seamless) |
| `TANDA` en `Mosaico.tsx` | Piezas por tanda de scroll |
| `alturaObjetivoPara()` en `mosaico.ts` | Altura a la que tienden las filas |
| `ESCALERA` / `CALIDAD` en el script de ingesta | Anchos y compresión |

### Orden aleatorio

La galería se baraja en cada visita, pero la página es **estática**. Barajar en
servidor congelaría el orden en el build; barajar durante el render del cliente
rompería la hidratación. La semilla se modela como dato externo a React
([`lib/semilla-orden.ts`](lib/semilla-orden.ts)) leído con
`useSyncExternalStore`: el HTML prerenderizado sale en orden curatorial
—estable para los rastreadores— y el cliente conmuta al barajado al hidratar.

Después del barajado, `separarHermanas()` aparta las variantes de una misma
generación: Midjourney entrega cuatro imágenes casi idénticas por prompt
(mismo `generacion`, distinto `variante`) y el azar las junta cada tanto.

## Licencias

Cada obra declara `licencia` y `licenciaDetalle.print`. Hoy es informativo: se
muestra en la pieza, en el lightbox y en la ficha, y no hay checkout.

El esquema existe desde ya porque el modelo de datos es lo caro de cambiar
después. Piezas previstas para ese momento, deliberadamente sin implementar:

- `Obra.originalKey` — ruta del máster en un **store privado** de Blob
  (`vercel blob create-store <nombre> --access private`). Se guarda la ruta, no
  una URL firmada, porque el manifest está versionado. Hoy los másteres se
  quedan en disco local, fuera de la plataforma.
- `lib/galeria.ts → getOriginalKey()` — único punto de acceso, solo servidor.
  Que `ObraGrid` sea un tipo aparte hace que ese campo no cruce al cliente por
  descuido.
