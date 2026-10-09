import fs from 'fs';
import path from 'path';
import { leerFrontmatter } from './frontmatter';
import type { EditionMetadata, SectionType, SectionContent, Edition, ArchiveItem } from '@/types';

const CONTENT_DIR = path.join(process.cwd(), 'content', 'editions');
const SLUG_VALIDO = /^[a-z0-9-]+$/i;

/**
 * Get all edition numbers (folder names) from the content directory
 */
export function getAllEditionSlugs(): string[] {
  try {
    // Check if content directory exists
    if (!fs.existsSync(CONTENT_DIR)) {
      console.error(`Content directory does not exist: ${CONTENT_DIR}`);
      return [];
    }

    const editions = fs.readdirSync(CONTENT_DIR);
    return editions.filter((edition) => {
      const editionPath = path.join(CONTENT_DIR, edition);
      return fs.statSync(editionPath).isDirectory();
    });
  } catch (error) {
    console.error('Error reading editions directory:', error);
    return [];
  }
}

/**
 * Get metadata for a specific edition
 */
export async function getEditionMetadata(slug: string): Promise<EditionMetadata | null> {
  // El slug llega de la URL y se vuelve ruta de disco: sólo letras, cifras y
  // guiones, para que «..» o una barra codificada no salgan de content/.
  if (!SLUG_VALIDO.test(slug)) return null;
  try {
    const metadataPath = path.join(CONTENT_DIR, slug, 'metadata.json');
    const metadataContent = fs.readFileSync(metadataPath, 'utf-8');
    const metadata: EditionMetadata = JSON.parse(metadataContent);
    return metadata;
  } catch (error) {
    console.error(`Error reading metadata for edition ${slug}:`, error);
    return null;
  }
}

/**
 * Load and compile MDX content for a specific section
 */
async function loadSection(
  slug: string,
  sectionName: string
): Promise<SectionContent | null> {
  if (!SLUG_VALIDO.test(slug)) return null;
  try {
    const sectionPath = path.join(CONTENT_DIR, slug, `${sectionName}.mdx`);

    // Check if file exists
    if (!fs.existsSync(sectionPath)) {
      return null;
    }

    const fileContent = fs.readFileSync(sectionPath, 'utf-8');
    const { content, data } = leerFrontmatter(fileContent);

    // Return raw MDX content for RSC rendering
    return {
      type: sectionName as SectionType,
      mdxSource: content, // Raw MDX string for next-mdx-remote/rsc
      frontmatter: data,
    };
  } catch (error) {
    console.error(`Error loading section ${sectionName} for edition ${slug}:`, error);
    return null;
  }
}

/**
 * Get complete edition data including all sections
 */
export async function getEditionBySlug(slug: string): Promise<Edition | null> {
  try {
    const metadata = await getEditionMetadata(slug);
    if (!metadata) {
      return null;
    }

    // Load all sections
    const [intro, jaiSounds, hybrid, closing] = await Promise.all([
      loadSection(slug, 'intro'),
      loadSection(slug, 'jai-sounds'),
      loadSection(slug, 'hybrid'),
      loadSection(slug, 'closing'),
    ]);

    return {
      metadata,
      sections: {
        intro: intro || undefined,
        jaiSounds: jaiSounds || undefined,
        hybrid: hybrid || undefined,
        closing: closing || undefined,
      },
      slug,
    };
  } catch (error) {
    console.error(`Error loading edition ${slug}:`, error);
    return null;
  }
}

/**
 * Get all editions for archive page
 */
export async function getAllEditions(): Promise<ArchiveItem[]> {
  const slugs = getAllEditionSlugs();

  const editions = await Promise.all(
    slugs.map(async (slug): Promise<ArchiveItem | null> => {
      const metadata = await getEditionMetadata(slug);
      if (!metadata) return null;

      return {
        number: metadata.number,
        title: metadata.title,
        theme: metadata.theme,
        publishedAt: metadata.publishedAt,
        description: metadata.description,
        slug,
        thumbnail: metadata.ogImage,
        portada: metadata.portada,
        sinopsis: metadata.sinopsis,
        ficha: metadata.ficha,
      };
    })
  );

  // Filter out null values and sort by number (descending)
  const validEditions = editions.filter((edition): edition is ArchiveItem => edition !== null);
  return validEditions.sort((a, b) => b.number - a.number);
}

/**
 * Check if an edition exists
 */
export function editionExists(slug: string): boolean {
  const editionPath = path.join(CONTENT_DIR, slug);
  return fs.existsSync(editionPath) && fs.statSync(editionPath).isDirectory();
}
