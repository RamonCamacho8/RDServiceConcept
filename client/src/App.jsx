// File: client/src/App.jsx
import { useState } from 'react'
import FileUpload from './components/FileUpload'
import JobStatus from './components/JobStatus'
import PdfViewer from './components/PdfViewer'
import { uploadImages } from './api'

function App() {
  const [files, setFiles] = useState([])
  const [jobId, setJobId] = useState(null)
  const [pdfUrl, setPdfUrl] = useState(null)

  // Función que se invoca al seleccionar archivos
  const handleFilesSelected = (selectedFiles) => {
    setFiles(selectedFiles)
  }

  // Función para enviar imágenes al servidor
  const handleSubmit = async () => {
    if (!files || files.length === 0) return;
    try {
      const response = await uploadImages(files)
      console.log('Upload successful:', response)
      setJobId(response.data.job_id)
    } catch (error) {
      console.error('Upload failed:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-gray-800">DR Analysis Pipeline</h1>
        
        <FileUpload onFilesSelected={handleFilesSelected} />
        
        {files.length > 0 && (
          <>
            <div className="grid grid-cols-3 gap-4">
              {files.map((file, index) => (
                <img
                  key={index}
                  src={URL.createObjectURL(file)}
                  alt={`Preview ${index}`}
                  className="h-32 w-full object-cover rounded-lg shadow"
                />
              ))}
            </div>
            <button
              className="px-4 py-2 bg-blue-500 text-white rounded"
              onClick={handleSubmit}
            >
              Procesar Imágenes
            </button>
          </>
        )}

        {jobId && <JobStatus jobId={jobId} onComplete={setPdfUrl} />}
        {pdfUrl && <PdfViewer pdfUrl={pdfUrl} />}
      </div>
    </div>
  )
}

export default App
