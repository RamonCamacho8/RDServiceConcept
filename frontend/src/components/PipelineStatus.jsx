import React, { useEffect, useState } from 'react';

const PipelineStatus = ({ taskId, setReportAvailable }) => {
  const [status, setStatus] = useState("En espera...");
  const [details, setDetails] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      fetch(`http://localhost:8000/status/${taskId}`)
        .then(res => res.json())
        .then(data => {
          setStatus(data.status);
          if (data.meta) {
            setDetails(`${data.meta.step}: ${data.meta.detail}`);
          }
          if (data.status === "SUCCESS") {
            setReportAvailable(true);
            clearInterval(interval);
          }
          if (data.status === "FAILED") {
            clearInterval(interval);
          }
        })
        .catch(err => console.error(err));
    }, 2000);

    return () => clearInterval(interval);
  }, [taskId, setReportAvailable]);

  return (
    <div className="mb-4">
      <h2 className="text-xl font-semibold">Estado del Pipeline</h2>
      <p>Estado: {status}</p>
      <p>Detalle: {details}</p>
    </div>
  );
};

export default PipelineStatus;
