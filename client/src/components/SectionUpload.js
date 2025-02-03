// client/src/components/SectionUpload.js
import React from 'react';
import FileUploader from './FileUploader';
import PreviewGallery from './PreviewGallery';

function SectionUpload({ previewUrls, onFileChange, onUpload }) {
  return (
    <div>
      <FileUploader onFileChange={onFileChange} onUpload={onUpload} />
      <PreviewGallery previewUrls={previewUrls} />
    </div>
  );
}

export default SectionUpload;
