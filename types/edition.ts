/**
 * Type definitions for Curiana Radio edition content structure
 */

/**
 * Edition metadata stored in metadata.json
 */
export interface EditionMetadata {
  /** Edition number (e.g., 1, 2, 3) */
  number: number;

  /** Edition title (e.g., "Radio Silence") */
  title: string;

  /** Publication date in ISO format */
  publishedAt: string;

  /** Theme or concept for this edition */
  theme: string;

  /** Brief description for SEO and social sharing */
  description: string;

  /** Spotify playlist ID for this edition */
  spotifyPlaylistId?: string;

  /** Background gradient colors (hex codes) */
  backgroundColors?: {
    start: string;
    middle1: string;
    middle2: string;
    end: string;
  };

  /** Optional Open Graph image path */
  ogImage?: string;
}

/**
 * Section types available in an edition
 */
export type SectionType = 'intro' | 'jai-sounds' | 'hybrid' | 'closing';

/**
 * Individual track in the Jai Sounds section
 */
export interface Track {
  title: string;
  artist: string;
  review: string; // ~80 words
  link?: string; // Optional Spotify track link
}

/**
 * Rabbit Hole (expandable/collapsible content)
 */
export interface RabbitHole {
  title: string;
  icon?: string; // Emoji or icon identifier
  content: string; // MDX content
}

/**
 * Processed section content after MDX compilation
 */
export interface SectionContent {
  type: SectionType;
  mdxSource: any; // MDX compiled source from next-mdx-remote
  frontmatter?: Record<string, any>;
  rabbitHole?: RabbitHole;
}

/**
 * Complete edition data
 */
export interface Edition {
  metadata: EditionMetadata;
  sections: {
    intro?: SectionContent;
    jaiSounds?: SectionContent;
    hybrid?: SectionContent;
    closing?: SectionContent;
  };
  slug: string; // URL slug (e.g., "1", "2")
}

/**
 * Archive item for edition listing
 */
export interface ArchiveItem {
  number: number;
  title: string;
  theme: string;
  publishedAt: string;
  description: string;
  slug: string;
  thumbnail?: string;
}

/**
 * Archive data structure
 */
export interface Archive {
  editions: ArchiveItem[];
}
