import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

const FileUpload = ({ onUpload }) => {
  const onDrop = useCallback(acceptedFiles => {
    onUpload(acceptedFiles)
  }, [onUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: 'image/*',
    multiple: true
  })

  return (
    <div 
      {...getRootProps()}
      className={`p-8 border-2 border-dashed rounded-lg text-center cursor-pointer
        ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
    >
      <input {...getInputProps()} />
      <p className="text-gray-600">
        {isDragActive ? 'Suelta las imágenes aquí' : 'Arrastra imágenes o haz clic para seleccionar'}
      </p>
    </div>
  )
}

export default FileUpload