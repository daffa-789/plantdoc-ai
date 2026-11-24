import json
import threading
from io import BytesIO

import numpy as np
from ai_edge_litert.interpreter import Interpreter
from PIL import Image

from backend.config import CONFIDENCE_THRESHOLD, LABELS_PATH, TFLITE_PATH


CLASS_NAMES = {
    "healthy": "Tomato — Healthy",
    "early": "Tomato — Early Blight",
    "late": "Tomato — Late Blight",
    "mold": "Tomato — Leaf Mold",
    "unknown": "Unknown — Bukan daun tomat",
}


class PlantDocModel:
    def __init__(self, model_path=TFLITE_PATH, labels_path=LABELS_PATH):
        self.labels = json.loads(labels_path.read_text(encoding="utf-8"))
        self.web_keys = self.labels["web_keys"]
        self.interpreter = Interpreter(model_path=str(model_path))
        self.interpreter.allocate_tensors()
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        if len(input_details) != 1 or len(output_details) != 1:
            raise ValueError("Model harus memiliki satu input dan satu output")
        self.input_index = input_details[0]["index"]
        self.output_index = output_details[0]["index"]
        self.input_shape = input_details[0]["shape"].tolist()
        self.output_shape = output_details[0]["shape"].tolist()
        if len(self.input_shape) != 4 or self.input_shape[0] != 1:
            raise ValueError(f"Bentuk input model tidak didukung: {self.input_shape}")
        if len(self.output_shape) != 2 or self.output_shape[1] != len(self.web_keys):
            raise ValueError("Jumlah kelas labels.json tidak sesuai dengan output model")
        if input_details[0]["dtype"] != np.float32:
            raise ValueError("Model PlantDoc harus menggunakan input float32")
        self.input_height = self.input_shape[1]
        self.input_width = self.input_shape[2]
        self.interpreter_lock = threading.Lock()
        self.supports_unknown = "unknown" in self.web_keys

    def metadata(self):
        return {
            "model": "model.tflite",
            "classes": self.web_keys,
            "input_shape": self.input_shape,
            "output_shape": self.output_shape,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
            "supports_unknown": self.supports_unknown,
            "rejection_mode": "learned_unknown" if self.supports_unknown else "green_heuristic",
        }

    def predict_image(self, image: Image.Image) -> tuple[dict | None, dict | None]:
        image = image.convert("RGB").resize((self.input_width, self.input_height))
        pixels = np.asarray(image, dtype=np.float32)

        if not self.supports_unknown:
            green_mask = (
                (pixels[:, :, 1] > pixels[:, :, 0] * 1.08)
                & (pixels[:, :, 1] > pixels[:, :, 2] * 1.08)
                & (pixels[:, :, 1] > 55)
            )
            if float(np.mean(green_mask)) < 0.08:
                return None, {
                    "code": "NOT_A_LEAF",
                    "message": "Gambar tidak terdeteksi sebagai daun tanaman.",
                }

        with self.interpreter_lock:
            self.interpreter.set_tensor(self.input_index, np.expand_dims(pixels, axis=0))
            self.interpreter.invoke()
            probabilities = self.interpreter.get_tensor(self.output_index)[0]

        predictions = {
            key: float(probability)
            for key, probability in zip(self.web_keys, probabilities)
        }
        top_index = int(np.argmax(probabilities))
        top_key = self.web_keys[top_index]
        confidence = float(probabilities[top_index])
        rejected = top_key == "unknown"
        return {
            "top_key": top_key,
            "top_name": CLASS_NAMES.get(top_key, top_key),
            "confidence": confidence * 100,
            "uncertain": not rejected and confidence < CONFIDENCE_THRESHOLD,
            "rejected": rejected,
            "rejection_code": "UNKNOWN_INPUT" if rejected else None,
            "status": "rejected" if rejected else "prediction",
            "predictions": predictions,
        }, None


def read_image(image_bytes: bytes) -> Image.Image:
    with Image.open(BytesIO(image_bytes)) as image:
        return image.convert("RGB")


model = PlantDocModel()
