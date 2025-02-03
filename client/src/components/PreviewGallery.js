// client/src/components/PreviewGallery.js
import React, { useState } from 'react';

function PreviewGallery({ previewUrls }) {
  const IMAGES_PER_PAGE = 5;
  const [currentPage, setCurrentPage] = useState(0);
  const [selectedImage, setSelectedImage] = useState(null);

  const totalPages = Math.ceil(previewUrls.length / IMAGES_PER_PAGE);
  const paginatedImages = previewUrls.slice(
    currentPage * IMAGES_PER_PAGE,
    (currentPage + 1) * IMAGES_PER_PAGE
  );

  const nextPage = () => {
    if (currentPage < totalPages - 1) setCurrentPage(currentPage + 1);
  };

  const prevPage = () => {
    if (currentPage > 0) setCurrentPage(currentPage - 1);
  };

  return (
    <div className="mb-4">
      {previewUrls.length > 0 ? (
        <>
          <div className="grid grid-cols-5 gap-2">
            {paginatedImages.map((url, index) => (
              <div key={index} className="w-full aspect-square overflow-hidden rounded-lg border cursor-pointer"
                   onClick={() => setSelectedImage(url)}>
                <img src={url} alt={`preview ${index}`} className="w-full h-full object-cover" />
              </div>
            ))}
          </div>

          {totalPages > 1 && (
            <div className="flex justify-center items-center mt-2 space-x-2">
              <button
                onClick={prevPage}
                disabled={currentPage === 0}
                className={`px-3 py-1 rounded ${currentPage === 0 ? 'bg-gray-300 cursor-not-allowed' : 'bg-blue-500 text-white'}`}
              >
                ⬅️
              </button>
              <span className="text-gray-700">
                Página {currentPage + 1} de {totalPages}
              </span>
              <button
                onClick={nextPage}
                disabled={currentPage === totalPages - 1}
                className={`px-3 py-1 rounded ${currentPage === totalPages - 1 ? 'bg-gray-300 cursor-not-allowed' : 'bg-blue-500 text-white'}`}
              >
                ➡️
              </button>
            </div>
          )}

          {selectedImage && (
            <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
              <div className="relative p-4 bg-white rounded-lg shadow-lg max-w-3xl">
                <button
                  onClick={() => setSelectedImage(null)}
                  className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded-full"
                >
                  ✖️
                </button>
                <img src={selectedImage} alt="Vista previa" className="max-w-full max-h-[80vh] mx-auto" />
              </div>
            </div>
          )}
        </>
      ) : (
        <p className="text-gray-500 text-center">No hay imágenes seleccionadas.</p>
      )}
    </div>
  );
}

export default PreviewGallery;
