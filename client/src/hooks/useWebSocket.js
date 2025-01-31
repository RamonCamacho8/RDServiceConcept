import { useEffect, useState } from 'react';

export const useWebSocket = (taskId) => {
    const [progress, setProgress] = useState({ percent: 0, stage: '' });
    
    useEffect(() => {
        if (!taskId) return;
        
        const ws = new WebSocket(`ws://localhost:8000/ws/${taskId}`);
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.progress) {
                setProgress({
                    percent: data.progress,
                    stage: data.stage
                });
            }
        };

        return () => ws.close();
    }, [taskId]);

    return progress;
};