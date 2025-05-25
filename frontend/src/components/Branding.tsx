'use client';
import Logo from './Logo';
import { useEffect, useState } from 'react';

const rawMessage =
  '¡Entrena mejor, vive mejor!\nConsigue tu plan de entrenamiento GRATIS y personalizado con IA.\nRutinas, recordatorios y motivación para que logres tu mejor versión.';

function highlightKeywords(text: string) {
  return text
    .replace(
      /plan de entrenamiento/g,
      '<span class="text-[#f59e42] font-extrabold text-3xl drop-shadow-[0_2px_6px_rgba(0,0,0,0.25)]">plan de entrenamiento</span>'
    )
    .replace(
      /GRATIS/g,
      '<span class="text-[#f59e42] font-bold drop-shadow-[0_2px_6px_rgba(0,0,0,0.25)]">GRATIS</span>'
    )
    .replace(
      /IA/g,
      '<span class="text-[#f59e42] font-bold drop-shadow-[0_2px_6px_rgba(0,0,0,0.25)]">IA</span>'
    );
}

export default function Branding() {
  const [displayed, setDisplayed] = useState('');
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (displayed.length < rawMessage.length) {
      const timeout = setTimeout(() => {
        setDisplayed(rawMessage.slice(0, displayed.length + 1));
      }, 14);
      return () => clearTimeout(timeout);
    } else {
      setDone(true);
    }
  }, [displayed]);

  return (
    <div className="flex flex-col items-center gap-8 w-full h-full justify-center">
      <div className="mb-4">
        <Logo size={100} />
      </div>
      <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-white drop-shadow-lg mb-6">
        motiv<span className="text-cyan-300">AI</span>
      </h1>
      <div className="flex-1 flex items-center w-full px-4 md:px-12 lg:px-20">
        <p className="text-2xl md:text-3xl font-semibold text-white/90 text-center w-full max-w-2xl min-h-[120px] whitespace-pre-line animate-none" style={{fontFamily: 'Montserrat, sans-serif'}}>
          {done ? (
            <span dangerouslySetInnerHTML={{ __html: highlightKeywords(displayed) }} />
          ) : (
            <>
              {displayed}
              <span className="inline-block w-2 h-7 align-middle bg-white animate-pulse ml-1" />
            </>
          )}
        </p>
      </div>
    </div>
  );
}
