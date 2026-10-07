import { MetadataRoute } from 'next';
import { SITIO } from '@/lib/seo';

// La política de rastreo (decisión de Miguel, 2026-10-04): buscadores sí,
// entrenamiento no. Los buscadores clásicos y los agentes que buscan para
// responder (y citan con enlace) leen todo; los que recolectan para entrenar
// modelos quedan fuera. Se puede abrir después; lo ya entrenado no se retira,
// y un modelo que aprende caquetío de aquí no tiene por qué conservar la marca
// de atestiguado, reconstruido o hipotético que lleva cada voz.
//
// robots.txt es un pedido, no una cerca: los bots que no lo respetan se
// bloquean en el Firewall de Vercel (reglas para bots de IA), no aquí.

// Buscan para responder una pregunta concreta y citan la fuente.
const BUSCADORES_IA = [
  'OAI-SearchBot', // ChatGPT Search
  'ChatGPT-User', // ChatGPT cuando un usuario le pide abrir una página
  'Claude-SearchBot',
  'Claude-User',
  'PerplexityBot',
  'Perplexity-User',
];

// Recolectan para entrenar modelos. Google-Extended y Applebot-Extended no
// son rastreadores aparte: son la exclusión de entrenamiento de Googlebot y
// Applebot, que siguen indexando para el buscador (y las respuestas con IA de
// Google salen del índice de Googlebot, no de esto).
const ENTRENAMIENTO_IA = [
  'GPTBot',
  'ClaudeBot',
  'anthropic-ai',
  'Google-Extended',
  'Applebot-Extended',
  'CCBot',
  'Meta-ExternalAgent',
  'Bytespider',
  'Amazonbot',
  'cohere-training-data-crawler',
  'Diffbot',
  'AI2Bot',
];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      // /jai-sounds/muestra ya no va aquí: lleva noindex, y para que un
      // buscador lea el noindex tiene que poder rastrearla.
      { userAgent: '*', allow: '/' },
      { userAgent: BUSCADORES_IA, allow: '/' },
      { userAgent: ENTRENAMIENTO_IA, disallow: '/' },
    ],
    sitemap: `${SITIO.url}/sitemap.xml`,
  };
}
