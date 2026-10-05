// Datos estructurados (schema.org) para buscadores y agentes. Un <script> de
// datos no se ejecuta, así que la CSP no lo toca; el escape de «<» es para que
// ningún texto del contenido pueda cerrar la etiqueta.
export default function JsonLd({ datos }: { datos: object }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(datos).replace(/</g, "\\u003c") }}
    />
  );
}
