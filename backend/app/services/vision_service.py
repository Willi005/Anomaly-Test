import cv2
from ultralytics import YOLO

class VisionService:
    def __init__(self):
        # Carga el modelo más ligero para pruebas rápidas en CPU/Webcam
        self.model = YOLO('yolov8n.pt') 
        # Define a qué altura de la imagen en píxeles está la "línea de riesgo"
        self.risk_line_y = 300 

    def process_frame(self, frame):
        # Ejecuta inferencia y tracking continuo (persist=True es clave para ByteTrack)
        results = self.model.track(frame, persist=True, tracker="bytetrack.yaml", classes=[0]) # class 0 = persona
        
        # Dibujar la línea de riesgo estática
        cv2.line(frame, (0, self.risk_line_y), (frame.shape[1], self.risk_line_y), (0, 255, 255), 2)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = map(int, box)
                
                # Calcular el centro inferior de la persona (los pies aproximadamente)
                bottom_center_x = int((x1 + x2) / 2)
                bottom_y = y2
                
                # Lógica de anomalía: Si los pies cruzan la línea de riesgo hacia abajo
                is_at_risk = bottom_y > self.risk_line_y

                # Cambiar color si está en riesgo
                color = (0, 0, 255) if is_at_risk else (0, 255, 0)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                if is_at_risk:
                    cv2.putText(frame, "¡ALERTA DE RIESGO!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        return frame