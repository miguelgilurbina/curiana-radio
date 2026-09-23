# Las fuentes que faltan: siete obras entran, diez siguen fuera — y qué hace falta de Miguel

> Campaña minería 3, parcela F1 (2026-09-22). Tabla completa en
> `6-fusion/fuentes_que_faltan_2026-09-22.yaml`. Rama
> `campana/mineria3-fuentes-que-faltan`.

## Lo que entró (dominio público, descargado y en git)

| Obra | Edición | Encargo de minero |
|---|---|---|
| **Federmann** | Arcaya 1916 + original de 1557 + Klüpfel 1859 | `encargo-mineria-federmann.md` |
| **Pérez de Tolosa 1546** | Oviedo y Baños, ed. Fernández Duro, t. II (1885), pp. 219-258 | `encargo-mineria-perez-de-tolosa.md` |
| **Rivero 1883** | Bogotá 1883 (sólo imagen; OCR de archive.org paginado) | `encargo-mineria-rivero.md` |
| **HSAI 4** (ficha nueva) y **HSAI 5** (extracto) | BAE Bulletin 143, 1948 y 1949 | `encargo-mineria-steward-hsai.md` |
| **Gumilla 1791** | Barcelona 1791, 2 t. | `encargo-mineria-gumilla.md` (prioridad baja) |
| **Zayas 1931** (ficha nueva) | 2ª ed., dLOC; **sólo los .txt en git** (PDF de 381 y 441 MB) | `encargo-mineria-zayas.md` (no prioritaria) |
| **Brinton 1871** | rellena el PDF que estaba en 0 bytes | — (ya minado) |

**No se lanzó ningún minero** (cambio del coordinador tras el corte por
límite de uso): los encargos quedan redactados para la tanda siguiente.

## Lo que resultó distinto de lo que se creía

1. **La Federmann de 1916 no se tradujo del alemán**, sino de la francesa de
   Ternaux (1837): lo dice Arcaya (p. 20). Las formas indígenas se cotejan con
   el alemán.
2. **Pérez de Tolosa trae una frase que el vault no tenía**: los caquetíos de
   los llanos «algo difieren en la habla á los de Coro» (p. 234). Y el pasaje
   de las «cuatrocientas casas» no sale con una búsqueda simple.
3. **Rivero nombra caquetíos con lengua propia en el Casanare** (Pauto, s.
   XVIII): posible tercera polity caquetía.
4. **El HSAI que habla de los caquetíos es el vol. 4, no el 5**.
5. **«Ramos 1978» es un libro**, *La fundación de Venezuela. Ampíes y Coro*;
   el PDF de Persée era una reseña de él.
6. **Zayas sí estaba en dLOC con texto**: la aplicación no lo muestra, pero el
   servidor de imágenes sirve el PDF completo.
7. **Angulo Molina no tiene obra identificable**: Zavala no lo pone en su
   bibliografía, y tampoco a Esteves, Alvarado, Arellano Moreno ni Hill Peña.

## Qué necesita de Miguel (opciones)

**A. Angulo Molina — el verbo caquetío entero depende de él.**
- A1. Escribirle a Miguel Enrique Zavala Reyes y preguntar de qué obra sacó a AM
  (vía el *Boletín Antropológico* de la ULA). *Recomendado: es lo más corto.*
- A2. Conseguir Hernández Baño 1984, *Los Caquetíos de Falcón* (INCUDEF,
  Coro), por donde probablemente le llegó la lista a Zavala.
- A3. Dejarlo como está: los diecinueve verbos siguen citando a Zavala, con la
  reserva «de segunda mano, compilador sin obra identificada».

**B. Nueva Segovia 1579.**
- B1. Comprar *Relaciones y descripciones sobre Venezuela y la Nueva Granada,
  siglo XVI* (Sindéresis 2023, 15-40 €), después de confirmar el índice.
- B2. Arellano Moreno 1964 en préstamo.
- B3. Buscar el manuscrito del AGI en PARES y transcribirlo por visión.
- *Recomendación: B1, si el índice la trae; si no, B3.*

**C. Arcaya, *Obra inédita y dispersa* (1995), p. 247** (la única frase
caquetía conocida): pedir un escaneo de esa página al CIHPMA-UNEFM.

**D. Los PDF de Zayas (381 y 441 MB).** Hoy sólo están los `.txt` en git.
- D1. Dejarlo así, y bajar de dLOC la página que haga falta. *Recomendado.*
- D2. Guardarlos en OneDrive con una línea en `.gitignore`, como Neira y Ribero
  (D8). Esto toca `.gitignore`, que este agente no editó.
- Y los derechos: dLOC no certifica dominio público. La ficha argumenta que es
  libre (Zayas †1934; Cuba vida + 50), pero es una lectura, no un dictamen.

**E. Compras o préstamos que siguen pendientes** (sin cambios hoy): Rouse &
Cruxent 1963, Ramos Pérez 1978 (el libro), Brett Martínez, Morón, Nägele 2020,
Oliver 2000, Granberry y Vescelius 2004.

## Lo que quedó sin hacer

- No se lanzó ningún minero.
- No se buscaron las imágenes de la Relación de Nueva Segovia en PARES.
- La reseña de Ramos está detrás de un captcha: se puede bajar a mano desde el
  navegador.
- Fuera de la parcela, pero a la vista: la ficha `oviedo-y-banos` describe el
  ejemplar moderno. El t. II de Fernández Duro (ya en el repo) trae además la
  carta de Ampíes, la relación anónima de gobernadores y el interrogatorio
  contra los Welser. Nadie los ha minado, y el encargo de Pérez de Tolosa
  los incluye.
