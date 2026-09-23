# D11 · las voces wayuu que quedan en el habla — qué pasa con cada una

Miguel, 2026-09-23 (tf.5):

> «Las 16 voces guayu que quedan. Kashi llama a Zulu Wano. Una gente más le
> busca las sustitutas en el mismo. Sí, me parece eso. Eso está bien.»

**La decisión está tomada** y entra en la tanda final. Esto es cómo se aplica.
Las formas, las citas y las etiquetas están en
`6-fusion/propuesta_d11_voces_wayuu_2026-09-23.yaml`. Las cifras, en
`6-fusion/medicion_d11_voces_wayuu_2026-09-23.yaml`, que emite
`6-fusion/scripts/medir_d11_voces_wayuu.py` (medido contra main en 4f20c14 y
la base local). `--check` confirma que la propuesta y la medición dicen lo
mismo. El método es el de D11 fase 3 (#226).

---

## Primero, lo que resultó falso al medirlo

- **No son 16, son 11.** Cinco de las 16 son los pronombres que tf.1 ya
  decidió (`taya`, `pia`, `nüma`, `waya`, `naya`).
- **Las más cargadas no son `kashi`, `yama` y `sulu`.** Por la palabra suelta
  sí. Pero `wana` 'ver' y `naba` 'pensar' casi nunca salen sueltas:
  - `wana`: 5.274 usos como núcleo de 95 formas (`wana-ka`…), en 3.335 de 3.811
    respuestas.
  - `naba`: 3.863 usos en 66 formas.
  - Y `naba` también está en el ejemplo de IDENTIDAD («Ta-barsure naba-ni»).
- **`bana` 'hígado' no es sólo wayuu.** Goeje 1939 p. 34 (visto en imagen):
  «foie u-bana, 6, A id.». El lokono dice lo mismo. Se queda la forma.
- **Dos tienen atestiguada que las cubre**, con otra glosa (por eso d19.b no las
  tocó):
  - `wanü` → `wasima` «Viejo, anciano» (Zavala #145, p. 68).
  - `yama` → `popoi` «Ahí. Adverbio de lugar» (Zavala #201, p. 70). Ya se dice
    397 veces.
- **La forma lokona choca en tres casos:**
  - `yaha` 'aquí' tiene el esqueleto del wayuu `yaa`.
  - `luccu` 'dentro' choca con `lukku` 'hombre' (lo avisa Perea, p. 546).
  - `dia` 'palabra' es el castellano «día».
- **De paso:**
  - El lokono `bute` del lexicón no es «ahora»: Brinton lo llama «nota
    praesentis», una marca del verbo.
  - Cuatro de las once no pasan la fonotáctica del caquetío atestiguado (la
    `ü`).

---

## La tabla

**Ninguna llega a reconstruido.** El criterio pide dos de las tres hermanas, y
en ninguna concuerdan consonante y vocal. El taíno no da ninguna con
cronista.

| Voz vieja | Glosa | Recomendada | Etiqueta | De dónde |
|---|---|---|---|---|
| `kashi` | ahora | **`danu`** | hipotético | lokono `dannu-hu` 'ahora', Perea pp. 492-493 |
| `yama` | aquí | **`popoi`** (se archiva `yama`) | atestiguado | Zavala #201 «Ahí» |
| `sulu` | adentro | **`ruku`** | hipotético | lokono `ruccu` (Perea p. 546), achagua `Yrrico` |
| `wana` | ver | **`diki`** | hipotético | lokono `a-ddiki-n`, Perea p. 479 |
| `naba` | pensar | **`kuburuku`** | hipotético | lokono `cubu-ruccu-a`, Perea p. 413 |
| `tüshi` | frío | **`kasalini`** | hipotético | achagua `Casalinibe`, pliego 64 der. |
| `kapua` | amanecer | **`mautia`** | hipotético | lokono `mauttia` 'la mañana', Perea p. 520 |
| `anüiki` | habla, lengua | **archivar**: lo cubre `maa` | — | dc.3: el verbo es su nombre |
| `pütchi` | palabra sagrada | **archivar**: lo cubren `maa` y `barsure` | — | era la voz wayuu del palabrero |
| `wanü` | anciano | **`wasima`** (se archiva `wanü`) | atestiguado | Zavala #145 «Viejo, anciano» |
| `bana` | hígado | **se queda** | baja a hipotético | lokono de Goeje, p. 34 |

**Se archivan sin sustituta nueva:** `anüiki` y `pütchi`.

**Se archivan en favor de una atestiguada que ya está en el canon:** `yama` y
`wanü`.

`sulu` es la mejor apoyada: el lokono y el achagua comparten r-k; les fallan
las vocales.

---

## El coste de la recomendación, medido

Cambian 10 voces (`bana` no cambia).

- **En la base:** 8.315 usos sueltos y 11.043 como núcleo de otra forma. 3.797
  de las 3.811 respuestas tienen al menos una de las diez.
- **En la puerta:** 164 formas (18.307 usos) pasan a «raíz de ninguna parte»
  (una raíz archivada no avala). Ninguna forma de la base se libera.
- **Formas nuevas:** entran seis (`danu`, `ruku`, `diki`, `kuburuku`,
  `kasalini`, `mautia`), las seis con clave libre y sin colisión de clave. La
  única marca es de lectura: `danu` empieza por el `da-` de tf.3.
- **Claves lokono:** no hay que renombrar ninguna si se aceptan las
  recomendadas.
- **Lo que hay que tocar:**
  - 25 apariciones en plantillas, 8 en las reglas, 10 en la koiné y 105 en tests
    (57 son de `wana`);
  - el evento «tüshi-juri»;
  - las LISTAS de `prompt_refuerzo`, que enseña por recorte y la medición
    estática no ve.
- **La capa:** las seis nuevas son hipotéticas. El perfil `era2` no muestra esa
  capa en el muestreador, así que allí sólo llegan por la plantilla. Hay que
  medirlo en la tanda.

---

## Las preguntas para Miguel, con letra

1. **kashi (ahora):** A `danu` · B `chabaka` · C archivar. *(recomiendo A)*
2. **yama (aquí):** A `popoi` · B `yaha` · C `wayare`. *(recomiendo A; B si
   quieres el contraste aquí/ahí, con sus dos choques)*
3. **sulu (adentro):** A `ruku` · B `loko` · C archivar. *(recomiendo A)*
4. **wana (ver):** A `diki` · B `kaba` · C archivar. *(recomiendo A)*
5. **naba (pensar):** A `kuburuku` · B `ikisi` · C archivar. *(recomiendo A)*
6. **tüshi (frío):** A `kasalini` · B archivar. *(recomiendo A)*
7. **kapua (amanecer):** A `mautia` · B `tukamara` · C archivar. *(recomiendo
   A; B si pesa más el concepto exacto que la hermana)*
8. **anüiki (habla, lengua):** A archivar · B `dia` · C `chuani`. *(recomiendo A)*
9. **pütchi (palabra sagrada):** A archivar · B `dia` · C `chuani`. *(recomiendo A)*
10. **wanü (anciano):** A `wasima` · B `baharuko`. *(recomiendo A)*
11. **bana (hígado):** A se queda, en hipotético · B archivar. *(recomiendo A)*

**Miguel decide.**
