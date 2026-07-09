// El umbral: la bisagra entre el instrumento y la crónica. Vive FUERA del
// wrapper del laboratorio, así sus tokens son los del cronista: banda de
// tinta parda entre la cabina oscura y el pergamino — el scroll "amanece".
// El efecto de entrada (.sim-umbral) es scroll-driven CSS puro con fallback
// estático; ver globals.css.
export default function Umbral({ texto }: { texto: string }) {
  return (
    <section aria-label="Umbral entre el experimento y la crónica" className="bg-(--sim-ink)">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 md:py-24 lg:px-8">
        <div className="sim-umbral mx-auto max-w-[52ch] text-center">
          <span
            aria-hidden="true"
            className="mx-auto mb-6 block h-px w-16 bg-(--sim-fuego)/70"
          />
          <p className="font-serif text-xl italic leading-relaxed text-(--sim-paper) md:text-2xl">
            {texto}
          </p>
          <span
            aria-hidden="true"
            className="mx-auto mt-6 block h-px w-16 bg-(--sim-fuego)/70"
          />
        </div>
      </div>
    </section>
  );
}
