import cv2
import numpy as np
from ultralytics import YOLO
import logging

from app.config import MODEL_PATH, CONFIDENCE_THRESHOLD, FRAME_WIDTH, FRAME_HEIGHT

logger = logging.getLogger(__name__)

_model: YOLO | None = None


def load_model() -> YOLO:
    global _model
    if _model is None:
        logger.info(f"Loading YOLOv8 model from {MODEL_PATH}")
        _model = YOLO(MODEL_PATH)
        logger.info("Model loaded successfully")
    return _model


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (FRAME_WIDTH, FRAME_HEIGHT))
    return img


def detect_product(image_bytes: bytes) -> dict | None:
    model = load_model()
    img = preprocess_image(image_bytes)
    results = model(img, conf=CONFIDENCE_THRESHOLD, verbose=False)
    result = results[0]
    if len(result.boxes) == 0:
        return None
    top_box = result.boxes[0]
    class_id = int(top_box.cls[0])
    label = result.names[class_id]
    confidence = float(top_box.conf[0])
    x1, y1, x2, y2 = top_box.xyxy[0].tolist()
    return {
        "label": label,
        "confidence": confidence,
        "bbox": [x1, y1, x2, y2],
    }
