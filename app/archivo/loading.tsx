export default function ArchivoLoading() {
  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Page Header Skeleton */}
        <header className="mb-16 text-center animate-pulse">
          <div className="h-4 w-32 bg-earth-200 mx-auto mb-4 rounded"></div>
          <div className="h-12 w-96 bg-earth-200 mx-auto mb-6 rounded"></div>
          <div className="h-4 w-2/3 bg-earth-200 mx-auto rounded"></div>
        </header>

        {/* Editions Grid Skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-pulse">
          {[1, 2, 3].map((i) => (
            <div key={i} className="border-2 border-earth-200 rounded-lg p-6">
              <div className="h-6 w-24 bg-earth-200 mb-4 rounded"></div>
              <div className="h-8 w-full bg-earth-200 mb-3 rounded"></div>
              <div className="h-4 w-5/6 bg-earth-200 mb-4 rounded"></div>
              <div className="space-y-2">
                <div className="h-3 w-full bg-earth-200 rounded"></div>
                <div className="h-3 w-4/6 bg-earth-200 rounded"></div>
              </div>
            </div>
          ))}
        </div>

        {/* Loading Message */}
        <div className="text-center mt-16">
          <p className="text-sm text-earth-600 font-sans italic">
            Cargando transmisiones...
          </p>
        </div>
      </div>
    </div>
  );
}
