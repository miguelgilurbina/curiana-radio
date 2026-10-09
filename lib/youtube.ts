// El id de un video de YouTube, para el <Video> de las señales
// (components/senales/senal-mdx.tsx). Lo que devuelve va directo al `src`
// del iframe, así que sólo sale de aquí un id de verdad: 11 caracteres de
// [A-Za-z0-9_-], suelto o sacado de una URL de YouTube. Cualquier otra cosa
// es null y el iframe no se arma. La CSP ya limita frame-src a
// youtube-nocookie.com (next.config.js): esto es defensa en profundidad.

const ID = /^[\w-]{11}$/;

const HOSTS = new Set([
  "youtube.com",
  "www.youtube.com",
  "m.youtube.com",
  "music.youtube.com",
  "youtu.be",
  "youtube-nocookie.com",
  "www.youtube-nocookie.com",
]);

/** El id venga como id o como cualquiera de sus URL: watch?v=, youtu.be/, embed/, shorts/, live/. */
export function idYouTube(valor: unknown): string | null {
  const texto = String(valor ?? "").trim();
  if (ID.test(texto)) return texto;

  let url: URL;
  try {
    // «youtu.be/…» pegado sin el https:// también vale
    url = new URL(/^[a-z][a-z\d+.-]*:/i.test(texto) ? texto : `https://${texto}`);
  } catch {
    return null;
  }
  if ((url.protocol !== "https:" && url.protocol !== "http:") || !HOSTS.has(url.hostname)) return null;

  const candidato =
    url.hostname === "youtu.be"
      ? url.pathname.split("/")[1]
      : (url.searchParams.get("v") ?? url.pathname.match(/^\/(?:embed|shorts|live|v)\/([^/]+)/)?.[1]);
  return candidato && ID.test(candidato) ? candidato : null;
}
