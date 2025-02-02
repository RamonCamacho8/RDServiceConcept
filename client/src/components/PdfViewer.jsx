import { useEffect, useState } from 'react'
import { getReport } from '../api'

const PdfViewer = ({ pdfUrl }) => {
  const [pdfData, setPdfData] = useState(null)

  useEffect(() => {
    const fetchPdf = async () => {
      try {
        const response = await getReport(pdfUrl)
        const blob = new Blob([response.data], { type: 'application/pdf' })
        setPdfData(URL.createObjectURL(blob))
      } catch (error) {
        console.error('Error loading PDF:', error)
      }
    }
    fetchPdf()
  }, [pdfUrl])

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Reporte Generado</h2>
      {pdfData ? (
        <iframe
          src={pdfData}
          className="w-full h-96 border rounded-lg"
          title="PDF Report"
        />
      ) : (
        <p>Cargando reporte...</p>
      )}
    </div>
  )
}

export default PdfViewer