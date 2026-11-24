from pathlib import Path
import json

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import numpy as np

try:
    import tensorflow as tf
except ImportError as exc:
    raise RuntimeError("TensorFlow is required for this backend") from exc


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = ROOT / "artifacts" / "models"
TFLITE_PATH = ARTIFACTS_DIR / "model.tflite"
LABELS_PATH = ARTIFACTS_DIR / "labels.json"
WEB_DIR = ROOT / "web"

if not TFLITE_PATH.exists():
    raise RuntimeError(f"TFLite model not found: {TFLITE_PATH}")
if not LABELS_PATH.exists():
    raise RuntimeError(f"Labels file not found: {LABELS_PATH}")

labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
WEB_KEYS = labels["web_keys"]

interpreter = tf.lite.Interpreter(model_path=str(TFLITE_PATH))
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
INPUT_INDEX = input_details[0]["index"]
OUTPUT_INDEX = output_details[0]["index"]
INPUT_HEIGHT = input_details[0]["shape"][1]
INPUT_WIDTH = input_details[0]["shape"][2]

app = FastAPI(title="PlantDoc AI", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "null"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "model": "model.tflite", "classes": WEB_KEYS}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="File must be an image")

    try:
        image = Image.open(file.file).convert("RGB")
        image = image.resize((INPUT_WIDTH, INPUT_HEIGHT))
        pixels = np.asarray(image, dtype=np.float32)
        pixels = np.expand_dims(pixels, axis=0)
        interpreter.set_tensor(INPUT_INDEX, pixels)
        interpreter.invoke()
        probabilities = interpreter.get_tensor(OUTPUT_INDEX)[0]
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to process image: {exc}") from exc

    if len(probabilities) != len(WEB_KEYS):
        raise HTTPException(status_code=500, detail="Model output size does not match labels")

    predictions = {
        key: float(probability)
        for key, probability in zip(WEB_KEYS, probabilities)
    }
    return JSONResponse({"predictions": predictions})


if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
