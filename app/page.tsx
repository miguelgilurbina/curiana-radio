export default function Home() {
  return (
    <main className="min-h-screen gradient-bg flex items-center justify-center p-8">
      <div className="text-center animate-fade-in">
        <h1 className="text-6xl md:text-8xl font-serif text-deep-900 mb-4">
          Curiana Radio
        </h1>
        <p className="text-2xl md:text-3xl text-deep-700 mb-6">
          88.8 FM
        </p>
        <p className="text-lg text-earth-700 max-w-2xl mx-auto mb-8">
          Transmisión Cultural desde Abya Yala
        </p>
        <div className="inline-block px-6 py-3 border-2 border-frequency text-frequency font-sans text-sm tracking-wider hover:bg-frequency hover:text-white transition-colors cursor-pointer">
          PRÓXIMAMENTE
        </div>
      </div>
    </main>
  );
}
