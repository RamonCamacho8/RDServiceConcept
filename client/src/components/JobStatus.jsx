import { useEffect, useState } from 'react'
import { getJobStatus } from '../api'

const JobStatus = ({ jobId }) => {
  const [status, setStatus] = useState('pending')
  
  useEffect(() => {
    const interval = setInterval(async () => {
      const response = await getJobStatus(jobId)
      setStatus(response.data.status)
      if (response.data.status === 'completed') clearInterval(interval)
    }, 2000)
    
    return () => clearInterval(interval)
  }, [jobId])

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-2">Estado del Proceso: {status}</h3>
      <div className="space-y-2">
        <div className={`p-2 rounded ${status === 'processing' ? 'bg-blue-100' : 'bg-gray-100'}`}>
          Procesando imágenes...
        </div>
        {/* Agregar más estados según sea necesario */}
      </div>
    </div>
  )
}

export default JobStatus