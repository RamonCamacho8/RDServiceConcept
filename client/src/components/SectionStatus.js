// client/src/components/SectionStatus.js
import React from 'react';
import StatusDisplay from './StatusDisplay';

function SectionStatus({ status, onRetry, onReview }) {
  return (
    <div>
      <StatusDisplay status={status} />
      {status && status.status === "FAILED" && (
        <div className="mt-4">
          <button
            onClick={onRetry}
            className="bg-red-500 text-white px-4 py-2 rounded"
          >
            Volver a intentar
          </button>
        </div>
      )}
      {status && status.status === "COMPLETED" && (
        <div className="mt-4">
          <button
            onClick={onReview}
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            Revisar reporte
          </button>
        </div>
      )}
    </div>
  );
}

export default SectionStatus;
