export default function EditionLoading() {
  return (
    <div className="min-h-screen">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Edition Header Skeleton */}
        <header className="mb-16 text-center animate-pulse">
          <div className="h-4 w-24 bg-earth-200 mx-auto mb-4 rounded"></div>
          <div className="h-12 w-3/4 bg-earth-200 mx-auto mb-4 rounded"></div>
          <div className="h-6 w-48 bg-earth-200 mx-auto mb-2 rounded"></div>
          <div className="h-6 w-64 bg-earth-200 mx-auto rounded"></div>
        </header>

        {/* Content Skeleton */}
        <div className="space-y-20 animate-pulse">
          {/* Intro Section Skeleton */}
          <section>
            <div className="space-y-4">
              <div className="h-4 bg-earth-200 rounded w-full"></div>
              <div className="h-4 bg-earth-200 rounded w-5/6"></div>
              <div className="h-4 bg-earth-200 rounded w-4/6"></div>
            </div>
          </section>

          {/* Section Title Skeleton */}
          <section>
            <div className="h-8 w-48 bg-earth-200 rounded mb-8"></div>
            <div className="space-y-4">
              <div className="h-4 bg-earth-200 rounded w-full"></div>
              <div className="h-4 bg-earth-200 rounded w-5/6"></div>
              <div className="h-4 bg-earth-200 rounded w-4/6"></div>
            </div>
          </section>
        </div>

        {/* Loading Message */}
        <div className="text-center mt-16">
          <p className="text-sm text-earth-600 font-sans italic">
            Sintonizando la frecuencia...
          </p>
        </div>
      </div>
    </div>
  );
}
