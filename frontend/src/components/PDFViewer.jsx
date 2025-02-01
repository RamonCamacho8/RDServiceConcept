import React from 'react';

const PDFViewer = ({ taskId }) => {
  const reportUrl = `http://localhost:8000/report/${taskId}`;
  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Reporte PDF</h2>
      <iframe src={reportUrl} width="100%" height="600px" title="Reporte PDF" />
    </div>
  );
};

export default PDFViewer;
