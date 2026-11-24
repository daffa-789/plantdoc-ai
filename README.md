# PlantDoc AI

Local PlantVillage tomato leaf classifier built with MobileNetV2 transfer learning, LiteRT, and FastHTML. The interface is composed from Python FastTags and server-rendered routes; the project does not define separate HTML, CSS, or JavaScript frontend files. The stylesheet is embedded in Python, so the web interface loads without CDN assets.

## Structure

- `main.py` - localhost entry point
- `backend/` - FastHTML routes, configuration, and LiteRT inference
- `frontend/` - Python UI components and offline stylesheet
- `artifacts/models/` - trained `model.tflite`, `best.keras`, and `labels.json`
- `notebooks/` - Colab training notebook
- `docs/` - project documentation and presentation sources
- `slides/` - rendered presentation assets

## Run locally

Install dependencies into the selected global Python installation:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Open `http://127.0.0.1:5000`.

## Unknown class

The Colab notebook trains five classes: four tomato conditions plus `unknown`. Unknown examples combine out-of-scope PlantVillage images with CIFAR-10 non-plant objects. After training, copy the exported `model.tflite` and `labels.json` into `artifacts/models/`.

The backend reads `labels.json` at startup. When `unknown` is present, a top-1 unknown prediction is rejected and `POST /predict` returns HTTP 422. The currently committed four-class model still uses the legacy green-pixel heuristic until it is replaced by the five-class export.
