# PlantDoc AI

Local PlantVillage tomato leaf classifier built with MobileNetV2 transfer learning.

## Structure

- `backend/` - FastAPI inference server
- `web/` - static responsive web interface
- `artifacts/models/` - trained `model.tflite`, `best.keras`, and `labels.json`
- `notebooks/` - Colab training notebook
- `docs/` - project documentation and presentation sources
- `slides/` - rendered presentation assets

## Run locally

```powershell
py -m pip install -r requirements.txt
py -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`.
