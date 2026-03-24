import React from 'react';

interface CameraFeedProps {
  streamUrl: string;
  name: string;
  isActive: boolean;
}

export const CameraFeed: React.FC<CameraFeedProps> = ({ streamUrl, name, isActive }) => {
  return (
    <div className={`flex flex-col border rounded-lg overflow-hidden bg-gray-900 ${isActive ? 'border-blue-500' : 'border-gray-700'}`}>
      <div className="bg-gray-800 px-3 py-2 text-sm font-semibold text-white flex justify-between items-center">
        <span>{name}</span>
        <span className={`w-3 h-3 rounded-full ${isActive ? 'bg-green-500' : 'bg-red-500'}`}></span>
      </div>
      {/* El stream en una app real vendrá de un endpoint que retorne un multipart/x-mixed-replace (MJPEG) o WebRTC */}
      <img 
        src={streamUrl} 
        alt={`Transmisión de ${name}`} 
        className="w-full h-auto aspect-video object-cover bg-black"
      />
    </div>
  );
};