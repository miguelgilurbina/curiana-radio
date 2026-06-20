"use client";

import type { CSSProperties, ReactNode } from "react";
import { LANG_COLORS } from "@/lib/supabase";
import { PREFIX_RULES, SUFFIX_RULES } from "@/lib/morphology";

export interface LexiconLookup {
  source_language: string;
  meaning: string;
}

interface Props {
  text: string;
  lexicon: Map<string, LexiconLookup>;
}

// Separa el texto en tokens de "palabra" (letras/acentos/guion/apóstrofe)
// y tokens de "separador" (espacios, puntuación, paréntesis, asteriscos).
const TOKEN_RE = /[\p{L}\p{M}'-]+|[^\p{L}\p{M}'-]+/gu;

function normalize(s: string): string {
  return s.toLowerCase();
}

// Cada palabra del texto puede venir compuesta de raíz(es) + afijos unidos
// por guiones, ej. "ta-barsure-bana". Coloreamos cada morfema reconocido
// por separado y dejamos en gris lo que no se reconoce (típicamente español).
function renderWord(word: string, key: string, lexicon: Map<string, LexiconLookup>) {
  const parts = word.split("-");

  return (
    <span key={key}>
      {parts.map((part, i) => {
        const norm = normalize(part);
        const entry = lexicon.get(norm);
        const isFirst = i === 0;
        const isOnly = parts.length === 1;

        const node: ReactNode = part;
        let title: string | undefined;
        let color = "#9C8A6E"; // gris apagado = no reconocido (probable español)
        let style: CSSProperties = { color };

        if (entry) {
          color = LANG_COLORS[entry.source_language] ?? "#F5EDD6";
          title = `${part} — ${entry.source_language}: ${entry.meaning}`;
          style = { color, fontWeight: 600, borderBottom: `1px dotted ${color}88`, cursor: "help" };
        } else if (!isOnly && isFirst && PREFIX_RULES[norm]) {
          const rule = PREFIX_RULES[norm];
          title = `${part}- — ${rule.gloss} (${rule.desc})`;
          style = { color: "#C9A876", borderBottom: "1px dotted #C9A87688", cursor: "help" };
        } else if (!isOnly && !isFirst && SUFFIX_RULES[norm]) {
          const rule = SUFFIX_RULES[norm];
          title = `-${part} — ${rule.gloss} (${rule.desc})`;
          style = { color: "#C9A876", borderBottom: "1px dotted #C9A87688", cursor: "help" };
        }

        return (
          <span key={i}>
            {i > 0 && <span style={{ color: "#6B5B45" }}>-</span>}
            <span title={title} style={style}>
              {node}
            </span>
          </span>
        );
      })}
    </span>
  );
}

export default function HighlightedText({ text, lexicon }: Props) {
  const tokens = Array.from(text.matchAll(TOKEN_RE)).map((m) => m[0]);
  const isWordToken = (t: string) => /[\p{L}\p{M}]/u.test(t);

  return (
    <p className="text-sm leading-relaxed" style={{ color: "#F5EDD6" }}>
      {tokens.map((tok, idx) =>
        isWordToken(tok) ? (
          renderWord(tok, String(idx), lexicon)
        ) : (
          <span key={idx} style={{ color: "#9C8A6E" }}>
            {tok}
          </span>
        )
      )}
    </p>
  );
}
