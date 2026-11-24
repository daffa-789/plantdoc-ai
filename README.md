# PlantDoc AI

Local PlantVillage tomato leaf classifier built with MobileNetV2 transfer learning and FastHTML. The interface is composed from Python FastTags and server-rendered routes; the project does not define separate HTML, CSS, or JavaScript frontend files. The stylesheet is embedded in Python, so the web interface loads without CDN assets.

## Structure

- `backend/` - FastHTML application and model inference
- `artifacts/models/` - trained `model.tflite`, `best.keras`, and `labels.json`
- `notebooks/` - Colab training notebook
- `docs/` - project documentation and presentation sources
- `slides/` - rendered presentation assets

## Run locally

Install dependencies into the selected global Python installation:

```powershell
python -m pip install -r requirements.txt
python -m backend.app
```

Open `http://127.0.0.1:5000`.
