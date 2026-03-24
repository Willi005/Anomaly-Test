from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
from app.services.vision_service import VisionService
app = FastAPI()

# Configuración CORS vital para que React en el puerto 5173 pueda hablar con FastAPI en el 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciamos tu servicio de visión una sola vez
vision_service = VisionService()

def generate_frames():
    # cv2.VideoCapture(0) abre la cámara web por defecto de tu notebook
    camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Pasamos el frame crudo por tu algoritmo de YOLO
        processed_frame = vision_service.process_frame(frame)
        
        # Codificamos la imagen procesada a formato JPEG
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        # "yield" emite el frame continuamente en un formato que HTML entiende nativamente
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Este es el endpoint que pusimos en tu Dashboard.tsx
@app.get("/api/video/feed/0")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")