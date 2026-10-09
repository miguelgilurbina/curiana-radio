import { SITIO } from "@/lib/seo";
import { TEMA, type Tema } from "./suscriptor";

// ── El correo de confirmación ─────────────────────────────────────────
// En la noche de la marca (BRAND_MVP §3.1): fondo #0f1621, hueso #eee6d4, el
// oro de --noche-acento para el único botón (tinta de fondo sobre oro, 10.2:1)
// y #7e93aa sólo para el dato en mono pequeño. Tipografía del sistema, sin
// webfonts. Tablas y estilos en línea porque así lo leen Gmail y Outlook. La
// única imagen es el isotipo, servido desde curianaradio.com; si el cliente
// bloquea imágenes, el correo se entiende igual.

export const ASUNTO = "Confirma tu frecuencia en Curiana Radio";

const NOCHE = {
  fondo: "#0f1621",
  hueso: "#eee6d4",
  hueso2: "#c6cfd9",
  dato: "#7e93aa",
  filete: "#3a4b61",
  acento: "#e6b43c",
};
const SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif";
const SERIF = "Georgia, 'Times New Roman', serif";
const MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace";

function escapar(texto: string): string {
  return texto.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export function correoDeConfirmacion(enlace: string, tema: Tema): { subject: string; html: string; text: string } {
  const recibe = TEMA[tema].recibe;
  const url = escapar(enlace);
  const isotipo = `${SITIO.url}/marca/isotipo-hueso.png`;

  const html = `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="supported-color-schemes" content="dark">
<title>${ASUNTO}</title>
</head>
<body style="margin:0;padding:0;background:${NOCHE.fondo};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">Un clic y quedas en la frecuencia. El enlace vale 48 horas.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="${NOCHE.fondo}" style="background:${NOCHE.fondo};">
<tr><td align="center" style="padding:40px 16px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:520px;">
<tr><td style="padding:0 0 28px;"><img src="${isotipo}" width="56" height="56" alt="Curiana Radio" style="display:block;border:0;width:56px;height:56px;"></td></tr>
<tr><td style="padding:0 0 12px;font-family:${MONO};font-size:11px;letter-spacing:3px;color:${NOCHE.dato};">88.8 FM · CURIANA RADIO</td></tr>
<tr><td style="padding:0 0 20px;font-family:${SERIF};font-size:28px;line-height:1.25;color:${NOCHE.hueso};">Confirma tu frecuencia</td></tr>
<tr><td style="padding:0 0 28px;font-family:${SANS};font-size:16px;line-height:1.6;color:${NOCHE.hueso};">Alguien —esperamos que tú— pidió recibir en este correo ${escapar(recibe)}. Para quedar en la frecuencia, confírmalo:</td></tr>
<tr><td style="padding:0 0 28px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td bgcolor="${NOCHE.acento}" style="background:${NOCHE.acento};border-radius:2px;">
<a href="${url}" style="display:inline-block;padding:14px 26px;font-family:${MONO};font-size:13px;font-weight:700;letter-spacing:3px;color:${NOCHE.fondo};text-decoration:none;">CONFIRMAR →</a>
</td>
</tr></table>
</td></tr>
<tr><td style="padding:0 0 8px;font-family:${SANS};font-size:13px;line-height:1.6;color:${NOCHE.hueso2};">Si el botón no responde, copia este enlace en el navegador:</td></tr>
<tr><td style="padding:0 0 28px;font-family:${MONO};font-size:12px;line-height:1.6;word-break:break-all;"><a href="${url}" style="color:${NOCHE.hueso2};text-decoration:underline;">${url}</a></td></tr>
<tr><td style="padding:20px 0 0;border-top:1px solid ${NOCHE.filete};font-family:${SANS};font-size:13px;line-height:1.6;color:${NOCHE.hueso2};">El enlace vale 48 horas. Si no fuiste tú, ignora este correo: sin confirmar, no te llega nada.</td></tr>
<tr><td style="padding:24px 0 0;font-family:${MONO};font-size:11px;letter-spacing:2px;color:${NOCHE.dato};">88.8 FM — SIEMPRE TRANSMITIENDO · <a href="${SITIO.url}" style="color:${NOCHE.dato};text-decoration:none;">CURIANARADIO.COM</a></td></tr>
</table>
</td></tr>
</table>
</body>
</html>`;

  const text = `Confirma tu frecuencia en Curiana Radio

Alguien —esperamos que tú— pidió recibir en este correo ${recibe}.

Para quedar en la frecuencia, abre este enlace (vale 48 horas):
${enlace}

Si no fuiste tú, ignora este correo: sin confirmar, no te llega nada.

—
Curiana Radio · 88.8 FM
${SITIO.url}
`;

  return { subject: ASUNTO, html, text };
}
