// client/src/components/PdfViewer.js
import React from 'react';

function PdfViewer({ pdfUrl }) {
  if (!pdfUrl) return null;
  return (
    <div className="h-full">
      <iframe 
        src={pdfUrl} 
        title="Reporte PDF" 
        className="w-full h-full" 
        style={{ border: 'none' }}
      />
    </div>
  );
}

export default PdfViewer;
