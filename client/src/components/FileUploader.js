// client/src/components/FileUploader.js
import React, { useState } from 'react';

function FileUploader({ onFileChange, onUpload }) {
  const [dragging, setDragging] = useState(false);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileChange({ target: { files: e.dataTransfer.files } });
    }
  };

  return (
    <div className="mb-4">
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center ${
          dragging ? 'border-blue-500 bg-blue-100' : 'border-gray-300 bg-gray-50'
        }`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        <p className="text-gray-700">Arrastra y suelta tus archivos aquí</p>
        <p className="text-gray-500">o</p>
        <input
          type="file"
          multiple
          onChange={onFileChange}
          className="hidden"
          id="fileInput"
        />
        <label
          htmlFor="fileInput"
          className="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded mt-2 inline-block"
        >
          Seleccionar Archivos
        </label>
      </div>
      <button
        onClick={onUpload}
        className="bg-green-500 text-white px-4 py-2 rounded mt-4"
      >
        Subir
      </button>
    </div>
  );
}

export default FileUploader;
