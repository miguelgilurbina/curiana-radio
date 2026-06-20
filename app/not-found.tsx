'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';

const SABIDURIA_ANCESTRAL = [
  "El viento no borra, reescribe. Tu error es un nuevo borrador.",
  "En la sequía, la raíz busca más profundo. Tú también.",
  "Perderse es la única forma de encontrar lo que no buscabas.",
  "El médano avanza, la memoria sostiene.",
  "No hay caminos errados en el desierto, solo nuevas rutas hacia el mar.",
  "El código, como el tejido, se repara con paciencia.",
  "Escucha el silencio. Algo en este error te está llamando.",
  "Cayerúa mira el horizonte. Tú miras una pantalla. Ambos buscan lo mismo.",
  "Lo que fue invisibilizado vuelve a brotar aquí.",
  "Has llegado al borde del mapa. Aquí comienzan los dragones (y los burros)."
];

const BURRO_ASCII = `
      /\_/\
     ( o.o )
      > ^ <
     /     \
    (       )
    (___)___)
`;

// O una versión más "de perfil" mirando al usuario
const BURRO_PERFIL = `
        _  _ 
       ( \/ ) 
        \  / 
        /  \    //
       /    \__//
      /      \ /
     /   _    |
    (   / \   |
     \_/   \_/
`;

// Versión Minimalista Desierto
const PAISAJE_ASCII = `
           ,
        _.-""-._
      _/-.____.-'\_
     /             \
    (   _  _        )
     \ ( \/ )      /
      \ \  /      /
       \/  \    //
       /    \__//
      /      \ /
     /   _    |
    (   / \   |   
     \_/   \_/
~~~~~~~~~~~~~~~~~~~~~~~
`;

export default function GlobalNotFound() {
  const [mensaje, setMensaje] = useState<string>("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    seleccionarSabiduria();
  }, []);

  const seleccionarSabiduria = () => {
    const indice = Math.floor(Math.random() * SABIDURIA_ANCESTRAL.length);
    setMensaje(SABIDURIA_ANCESTRAL[indice]);
  };

  const handleSeguirPerdido = () => {
    // Pequeña animación de recarga "mental"
    setMensaje("Escuchando al viento...");
    setTimeout(() => {
      seleccionarSabiduria();
    }, 600);
  };

  if (!mounted) return null;

  return (
    <div className="min-h-screen bg-earth-900 text-earth-100 font-mono flex flex-col items-center justify-center p-6 selection:bg-frequency selection:text-white overflow-hidden relative">
      
      {/* Elementos de fondo "Viento" */}
      <div className="absolute inset-0 opacity-10 pointer-events-none">
        <div className="absolute top-10 left-10 text-xs animate-pulse">~ ~ ~</div>
        <div className="absolute bottom-20 right-20 text-xs animate-pulse delay-700">~ ~ ~</div>
        <div className="absolute top-1/2 left-1/4 text-xs animate-pulse delay-300">. . .</div>
      </div>

      <main className="z-10 max-w-2xl w-full text-center space-y-12 border-l-2 border-frequency/30 pl-6 md:pl-12 md:border-l-4">
        
        {/* El Error como Título */}
        <header className="space-y-2 text-left">
          <h1 className="text-6xl md:text-8xl font-bold text-earth-300 opacity-50 tracking-tighter">
            404
          </h1>
          <p className="text-frequency text-sm tracking-widest uppercase">
            // Ruta del Extravío
          </p>
        </header>

        {/* El Guardián ASCII */}
        <div className="py-8 my-8 relative group">
          <pre className="text-[10px] md:text-xs leading-none text-earth-200 whitespace-pre font-bold mx-auto transition-all duration-1000 group-hover:text-frequency">
            {PAISAJE_ASCII}
          </pre>
          <div className="absolute -bottom-4 left-0 w-full text-center opacity-0 group-hover:opacity-100 transition-opacity duration-500 text-xs text-earth-400">
            (El burro te observa con calma)
          </div>
        </div>

        {/* La Ofrenda (Mensaje) */}
        <div className="space-y-6 text-left min-h-[120px]">
          <div className="h-px w-12 bg-frequency mb-6"></div>
          <p className="text-xl md:text-2xl text-earth-50 font-serif italic leading-relaxed">
            "{mensaje}"
          </p>
        </div>

        {/* Controles de Navegación */}
        <div className="flex flex-col sm:flex-row gap-6 pt-8 text-sm items-start">
          <button 
            onClick={handleSeguirPerdido}
            className="group flex items-center gap-2 hover:text-frequency transition-colors text-earth-300"
          >
            <span>[ SEGUIR PERDIDO ]</span>
            <span className="opacity-0 group-hover:opacity-100 transition-opacity">↻</span>
          </button>

          <Link 
            href="/"
            className="group flex items-center gap-2 hover:text-frequency transition-colors text-earth-300"
          >
            <span>[ VOLVER AL ORIGEN ]</span>
            <span className="opacity-0 group-hover:opacity-100 transition-opacity">→</span>
          </Link>
        </div>

      </main>

      {/* Footer Minimalista */}
      <footer className="absolute bottom-6 text-xs text-earth-700">
        Sintra v4 :: Sistema de Memoria :: Curiana Radio
      </footer>
    </div>
  );
}
