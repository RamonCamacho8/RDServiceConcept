// client/src/components/SectionPdf.js
import React from 'react';
import PdfViewer from './PdfViewer';

function SectionPdf({ pdfUrl, onRestart }) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1">
        <PdfViewer pdfUrl={pdfUrl} />
      </div>
      <div className="mt-4">
        <button 
          onClick={onRestart} 
          className="bg-green-500 text-white px-4 py-2 rounded"
        >
          Iniciar nuevo proceso
        </button>
      </div>
    </div>
  );
}

export default SectionPdf;
