import { datosEstacion, N_ESTACIONES } from "@/lib/jai-wiki";

// El tracklist de cada estación, como JSON estático: la batea lo pide al
// pasar de disco (y precarga los vecinos). Se genera en el build; no hay
// base de por medio.
export const dynamic = "force-static";

export function generateStaticParams() {
  return Array.from({ length: N_ESTACIONES }, (_, i) => ({ n: String(i + 1).padStart(2, "0") }));
}

export async function GET(_: Request, { params }: { params: Promise<{ n: string }> }) {
  const { n } = await params;
  const datos = datosEstacion(Number.parseInt(n, 10) - 1);
  if (!datos) return new Response("Esa estación no está en el dial.", { status: 404 });
  return Response.json(datos);
}
