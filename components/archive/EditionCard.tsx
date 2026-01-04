import Link from 'next/link';
import { Heading, BodyText } from '@/components/ui/Typography';
import type { ArchiveItem } from '@/types';

interface EditionCardProps {
  edition: ArchiveItem;
}

export default function EditionCard({ edition }: EditionCardProps) {
  const publishDate = new Date(edition.publishedAt).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <Link
      href={`/${edition.slug}`}
      className="group block relative overflow-hidden rounded-lg border border-earth-200 hover:border-frequency hover:shadow-xl transition-all duration-300 bg-white"
    >
      {/* Card Content */}
      <div className="p-6">
        {/* Edition Number */}
        <div className="text-sm font-sans tracking-[0.2em] uppercase text-earth-600 mb-3">
          Edición #{edition.number}
        </div>

        {/* Title */}
        <Heading level={3} className="mb-2 group-hover:text-frequency transition-colors">
          {edition.title}
        </Heading>

        {/* Theme */}
        <div className="text-deep-700 font-serif text-base italic mb-4">
          {edition.theme}
        </div>

        {/* Description */}
        <BodyText className="text-deep-600 mb-4 line-clamp-3">
          {edition.description}
        </BodyText>

        {/* Publish Date */}
        <div className="text-earth-600 font-sans text-sm">
          {publishDate}
        </div>
      </div>

      {/* Hover Effect Border */}
      <div className="absolute inset-0 border-2 border-transparent group-hover:border-frequency rounded-lg pointer-events-none transition-colors duration-300" />
    </Link>
  );
}
