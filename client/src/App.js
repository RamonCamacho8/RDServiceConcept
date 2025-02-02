import React, { useState } from 'react';

function App() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);

  // Handle file selection and generate preview URLs.
  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);
    const urls = files.map(file => URL.createObjectURL(file));
    setPreviewUrls(urls);
  };

  // Upload files to the server.
  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;
    const formData = new FormData();
    selectedFiles.forEach(file => {
      formData.append('files', file);
    });
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setJobId(data.job_id);
      pollStatus(data.job_id);
    } catch (error) {
      console.error('Error uploading files', error);
    }
  };

  // Poll the server for pipeline status.
  const pollStatus = (jobId) => {
    const interval = setInterval(async () => {
      const res = await fetch(`http://localhost:8000/status/${jobId}`);
      const data = await res.json();
      console.log(data);
      setStatus(data);
      if (data.status === "SUCCESS" || data.status === "FAILED") {
        clearInterval(interval);
        if (data.status === "SUCCESS") {
          setPdfUrl(`http://localhost:8000/pdf/${jobId}`);
        }
      }
    }, 2000);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Image Upload and Processing</h1>
      <input type="file" multiple onChange={handleFileChange} className="mb-4"/>
      <div className="grid grid-cols-3 gap-4 mb-4">
        {previewUrls.map((url, index) => (
          <img key={index} src={url} alt={`preview ${index}`} className="w-full h-auto"/>
        ))}
      </div>
      <button 
        onClick={handleUpload} 
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Upload
      </button>
      {status && (
        <div className="mt-4">
          <p><strong>Status:</strong> {status.status}</p>
          {status.info && status.info.message && (
            <p><strong>Message:</strong> {status.info.message}</p>
          )}
        </div>
      )}
      {pdfUrl && (
        <div className="mt-4">
          <h2 className="text-xl font-bold">PDF Report</h2>
          <iframe src={pdfUrl} width="100%" height="600px" title="PDF Report"></iframe>
        </div>
      )}
    </div>
  );
}

export default App;
