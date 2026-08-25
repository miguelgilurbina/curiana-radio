import SimShell from "@/components/simulador/SimShell";

// Chrome compartido de las páginas interiores del simulador (léxico,
// neologismos, personajes): masthead + cronología lateral. El route group
// no toca las URLs; el landing queda fuera porque arma su propio chrome
// por actos.
export default function InteriorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <SimShell>{children}</SimShell>;
}
