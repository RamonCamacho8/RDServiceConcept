import React from 'react';

export const ProgressStepper = ({ progress, stage }) => (
    <div className="w-full bg-gray-200 rounded-full h-4">
        <div 
            className="bg-blue-600 h-4 rounded-full transition-all duration-500" 
            style={{ width: `${progress}%` }}
        >
            <div className="text-center text-white text-sm pt-1">
                {Math.round(progress)}% - {stage}
            </div>
        </div>
    </div>
);