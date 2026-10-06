import { ARISTAS, getSenales } from "@/lib/senales";

// El RSS de Señales: para quien sigue el sitio con un lector, y para que las
// automatizaciones (redes, correo) tengan de dónde leer. Se genera en el build.
export const dynamic = "force-static";

const BASE = "https://curianaradio.com";

const escapar = (s: string) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

export function GET() {
  const senales = getSenales().filter((s) => !s.borrador);
  const items = senales
    .map((s) => {
      const url = `${BASE}/senales/${s.slug}`;
      const categorias = s.aristas.map((a) => `      <category>${escapar(ARISTAS[a].nombre)}</category>`).join("\n");
      return `    <item>
      <title>${escapar(s.titulo)}</title>
      <link>${url}</link>
      <guid isPermaLink="true">${url}</guid>
      <pubDate>${new Date(`${s.fecha}T12:00:00Z`).toUTCString()}</pubDate>
      <dc:creator>${escapar(s.autor)}</dc:creator>
      <description>${escapar(s.sumario)}</description>
${categorias}
    </item>`;
    })
    .join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Señales — Curiana Radio</title>
    <link>${BASE}/senales</link>
    <description>Lo que escribe Miguel Gil Urbina sobre cada arista de Curiana Radio.</description>
    <language>es</language>
    <atom:link href="${BASE}/senales/rss.xml" rel="self" type="application/rss+xml" />
${items}
  </channel>
</rss>
`;
  return new Response(xml, { headers: { "Content-Type": "application/rss+xml; charset=utf-8" } });
}
