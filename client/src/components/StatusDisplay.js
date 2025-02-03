// client/src/components/StatusDisplay.js
import React from 'react';

function StatusDisplay({ status }) {
  // Definición de las etapas del proceso.
  const steps = [
    { label: "Calidad", state: "QUALITY_CHECK" },
    { label: "Clasificación", state: "DR_CLASSIFICATION" },
    { label: "Calificación", state: "DR_GRADING" },
    { label: "Reporte", state: "GENERATING_PDF" }
  ];

  // Determinar el índice de la etapa actual.
  let currentStepIndex = -1;
  if (status && status.status) {
    if (status.status === "COMPLETED") {
      currentStepIndex = steps.length; // Todas las etapas completadas.
    } else {
      const foundIndex = steps.findIndex(step => step.state === status.status);
      currentStepIndex = foundIndex;
    }
  }

  return (
    <div className="w-full">
      <div className="mb-4">
        <h2 className="text-lg font-semibold">Estado del Proceso:</h2>
        {status && (
          <p>
            <strong>Estado:</strong> {status.status}
          </p>
        )}
      </div>

      {/* Contenedor relativo para la barra de progreso */}
      <div className="relative w-full h-16">
        {/* Línea de progreso que se extiende de extremo a extremo */}
        <div
          className="absolute top-1/2 left-0 right-0 h-1 bg-gray-300"
          style={{ transform: "translateY(-50%)" }}
        ></div>

        {steps.map((step, index) => {
          // Determinar el estado de cada paso.
          let stepState;
          if (status && status.status === "COMPLETED") {
            stepState = "completed";
          } else {
            if (index < currentStepIndex) stepState = "completed";
            else if (index === currentStepIndex) stepState = "current";
            else stepState = "pending";
          }
          // Clases base para el círculo.
          let circleClasses =
            "w-6 h-6 rounded-full border-2 flex items-center justify-center";
          if (stepState === "completed") {
            circleClasses += " bg-green-500 border-green-500";
          } else if (stepState === "current") {
            circleClasses += " bg-yellow-500 border-yellow-500";
          } else {
            circleClasses += " bg-white border-gray-300";
          }

          return (
            <div
              key={index}
              className="absolute flex flex-col items-center"
              style={{
                left:
                  steps.length === 1
                    ? "50%"
                    : `${(index / (steps.length - 1)) * 100}%`,
                transform: "translateX(-50%)",
                top: 0,
              }}
            >
              <div className={circleClasses}>
                {stepState === "completed" && (
                  <span className="text-white text-xs">✓</span>
                )}
              </div>
              <div
                className="mt-1 text-xs text-center"
                style={{ width: "4rem" }}
              >
                {step.label}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default StatusDisplay;
