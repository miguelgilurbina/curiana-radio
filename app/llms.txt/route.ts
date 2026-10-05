import { llmsTxt } from "@/lib/llms";

// El índice del sitio para agentes (llmstxt.org). Estático: se arma al compilar.
export const dynamic = "force-static";

export async function GET() {
  return new Response(await llmsTxt(), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
