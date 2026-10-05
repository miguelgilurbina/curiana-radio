import { llmsFullTxt } from "@/lib/llms";

// El diccionario y los artículos de Kaketiana en un solo texto, para que un
// agente los lea sin rastrear cuatrocientas páginas. Estático.
export const dynamic = "force-static";

export function GET() {
  return new Response(llmsFullTxt(), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
