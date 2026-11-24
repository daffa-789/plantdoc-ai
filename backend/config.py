from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = ROOT / "artifacts" / "models"
TFLITE_PATH = ARTIFACTS_DIR / "model.tflite"
LABELS_PATH = ARTIFACTS_DIR / "labels.json"
CONFIDENCE_THRESHOLD = 0.62
HOST = "127.0.0.1"
PORT = 5000
