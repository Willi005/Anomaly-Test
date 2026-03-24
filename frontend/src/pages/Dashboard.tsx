import React from 'react';
import { CameraFeed } from '../components/CameraFeed';

export const Dashboard: React.FC = () => {
  // Simulación de múltiples fuentes. 
  // En tu prototipo, 'Cámara 1' apuntará a tu endpoint de Python que lee tu webcam.
  const cameras = [
    { id: 1, name: 'Webcam Local (Andén 1)', streamUrl: 'http://localhost:8000/api/video/feed/0', isActive: true },
    { id: 2, name: 'Cámara IP (Andén 2)', streamUrl: '/placeholder-stream.jpg', isActive: false },
  ];

  return (
    <div className="min-h-screen bg-gray-950 p-6">
      <h1 className="text-2xl font-bold text-white mb-6">Monitor de Seguridad</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {cameras.map((cam) => (
          <CameraFeed 
            key={cam.id} 
            streamUrl={cam.streamUrl} 
            name={cam.name} 
            isActive={cam.isActive} 
          />
        ))}
      </div>
    </div>
  );
};