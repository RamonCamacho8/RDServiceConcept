import { useEffect, useState } from 'react'
import { getJobStatus } from '../api'

const JobStatus = ({ jobId, onComplete }) => {
  const [status, setStatus] = useState('pending');
  
  useEffect(() => {
    const interval = setInterval(async () => {
      const response = await getJobStatus(jobId);
      const currentStatus = response.data.status;
      setStatus(currentStatus);
      if (currentStatus === 'completed') {
        clearInterval(interval);
        // Asumir que el endpoint devuelve o se conoce la URL del reporte, o se usa el jobId para obtenerlo.
        onComplete(jobId); // O bien: onComplete(response.data.pdf_url)
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, [jobId, onComplete]);

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-2">Estado del Proceso: {status}</h3>
      <div className="space-y-2">
        <div className={`p-2 rounded ${status === 'processing' ? 'bg-blue-100' : 'bg-gray-100'}`}>
          Procesando imágenes...
        </div>
      </div>
    </div>
  );
};

export default JobStatus