import React, { useState } from 'react';

import PipelineStatus from './components/PipelineStatus';
import PDFViewer from './components/PDFViewer';
import UploadForm from './components/UploadForm';

function App() {
  const [taskId, setTaskId] = useState(null);
  const [reportAvailable, setReportAvailable] = useState(false);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Proyecto POC - Pipeline de Imágenes</h1>
      {!taskId && (
        <UploadForm setTaskId={setTaskId} />
      )}
      {taskId && (
        <div>
          <PipelineStatus taskId={taskId} setReportAvailable={setReportAvailable} />
          {reportAvailable && <PDFViewer taskId={taskId} />}
        </div>
      )}
    </div>
  );
}

export default App;
