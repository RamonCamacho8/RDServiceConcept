// client/src/App.js
import React, { useState } from 'react';
import SectionUpload from './components/SectionUpload';
import SectionStatus from './components/SectionStatus';
import SectionPdf from './components/SectionPdf';

function App() {
  const [currentSection, setCurrentSection] = useState("upload");
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);
    setPreviewUrls(files.map((file) => URL.createObjectURL(file)));
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;
    setCurrentSection("status"); // Ir a la sección de estado.
    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append('files', file));

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setJobId(data.job_id);
      pollStatus(data.job_id);
    } catch (error) {
      console.error("Error al subir archivos", error);
      setCurrentSection("upload");
    }
  };

  const pollStatus = (jobId) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/status/${jobId}`);
        const data = await res.json();
        setStatus(data);

        // Cuando se completa, se establece la URL del PDF pero no se redirige automáticamente.
        if (data.status === "COMPLETED" && data.info && data.info.pdf_path) {
          clearInterval(interval);
          setPdfUrl(`http://localhost:8000/pdf/${jobId}`);
          // Permanece en la sección "status" hasta que el usuario presione "Revisar reporte".
        }
        if (data.status === "FAILED") {
          clearInterval(interval);
        }
      } catch (error) {
        console.error("Error al consultar estado", error);
        clearInterval(interval);
        setCurrentSection("upload");
      }
    }, 2000);
  };

  // Reinicia la aplicación para iniciar otro proceso.
  const handleRestart = () => {
    setSelectedFiles([]);
    setPreviewUrls([]);
    setJobId(null);
    setStatus(null);
    setPdfUrl(null);
    setCurrentSection("upload");
  };

  // Al presionar "Revisar reporte", se cambia a la sección del PDF.
  const handleReview = () => {
    setCurrentSection("pdf");
  };

  const handleRetry = () => {
    handleRestart();
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-3xl bg-white shadow-md rounded-lg p-6 flex flex-col h-full">
        <h1 className="text-2xl font-bold text-center">
          Subida y Procesamiento de Imágenes
        </h1>

        {currentSection === "upload" && (
          <SectionUpload
            previewUrls={previewUrls}
            onFileChange={handleFileChange}
            onUpload={handleUpload}
          />
        )}

        {currentSection === "status" && (
          <SectionStatus
            status={status}
            onRetry={handleRetry}
            onReview={handleReview}
          />
        )}

        {currentSection === "pdf" && (
          <SectionPdf pdfUrl={pdfUrl} onRestart={handleRestart} />
        )}
      </div>
    </div>
  );
}

export default App;
