import React, { useState } from 'react';

const UploadForm = ({ setTaskId }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [previews, setPreviews] = useState([]);

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);

    const previewsArray = files.map(file => URL.createObjectURL(file));
    setPreviews(previewsArray);
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;

    const formData = new FormData();
    selectedFiles.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (data.task_id) {
        setTaskId(data.task_id);
      }
    } catch (error) {
      console.error("Error al subir imágenes", error);
    }
  };

  return (
    <div className="mb-4">
      <input type="file" multiple onChange={handleFileChange} />
      <div className="mt-2 grid grid-cols-3 gap-2">
        {previews.map((src, index) => (
          <img key={index} src={src} alt={`preview-${index}`} className="h-32 object-cover border" />
        ))}
      </div>
      <button
        onClick={handleUpload}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Enviar imágenes
      </button>
    </div>
  );
};

export default UploadForm;
