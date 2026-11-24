import asyncio
from io import BytesIO
import json
from pathlib import Path
import threading

import numpy as np
from fasthtml.common import *
from PIL import Image, UnidentifiedImageError
from starlette.datastructures import UploadFile
from starlette.requests import Request
from starlette.responses import JSONResponse
from ai_edge_litert.interpreter import Interpreter


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = ROOT / "artifacts" / "models"
TFLITE_PATH = ARTIFACTS_DIR / "model.tflite"
LABELS_PATH = ARTIFACTS_DIR / "labels.json"

labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
WEB_KEYS = labels["web_keys"]
CONFIDENCE_THRESHOLD = 0.62

interpreter = Interpreter(model_path=str(TFLITE_PATH))
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
INPUT_INDEX = input_details[0]["index"]
OUTPUT_INDEX = output_details[0]["index"]
INPUT_HEIGHT = input_details[0]["shape"][1]
INPUT_WIDTH = input_details[0]["shape"][2]
interpreter_lock = threading.Lock()

APP_CSS = """
:root {
    color-scheme: light;
    --background: #f6f9f4;
    --surface: #ffffff;
    --surface-soft: #edf5ee;
    --text: #1c2b22;
    --muted: #607166;
    --border: #d9e5da;
    --primary: #286443;
    --primary-hover: #1f5134;
    --danger: #9b2f2a;
    --danger-background: #fff1f0;
    --radius: 0.875rem;
    --container: 68rem;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: var(--background);
    color: var(--text);
    font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    line-height: 1.6;
}

a {
    color: var(--primary);
}

a:focus-visible,
button:focus-visible,
input:focus-visible,
summary:focus-visible {
    outline: 0.1875rem solid var(--primary);
    outline-offset: 0.1875rem;
}

header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
}

header .container {
    min-height: 4.5rem;
    display: flex;
    align-items: center;
}

nav {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.5rem 1rem;
}

nav a {
    text-decoration: none;
}

nav p {
    margin: 0;
    color: var(--muted);
    font-size: 0.875rem;
}

.container {
    width: min(calc(100% - 2rem), var(--container));
    margin-inline: auto;
}

main.container {
    padding-block: clamp(2rem, 5vw, 4rem);
}

main > section:first-child {
    max-width: 45rem;
    margin-bottom: 2rem;
}

h1,
h2,
h3,
p {
    margin-top: 0;
}

h1 {
    margin-bottom: 1rem;
    font-size: clamp(2rem, 5vw, 3rem);
    line-height: 1.12;
    letter-spacing: -0.03em;
}

h2 {
    margin-bottom: 0.75rem;
    font-size: clamp(1.25rem, 3vw, 1.5rem);
    line-height: 1.3;
}

h3 {
    margin-bottom: 0.5rem;
    font-size: 1.0625rem;
}

p {
    margin-bottom: 1rem;
}

main > .grid {
    display: grid;
    grid-template-columns: minmax(0, 1.6fr) minmax(16rem, 0.8fr);
    gap: 1.5rem;
    align-items: start;
}

article,
aside {
    min-width: 0;
    padding: clamp(1.25rem, 3vw, 2rem);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
}

aside {
    background: var(--surface-soft);
}

hr {
    margin-block: 1.5rem;
    border: 0;
    border-top: 1px solid var(--border);
}

form {
    margin-top: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

input[type="file"] {
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.625rem;
    color: var(--muted);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    font: inherit;
}

input[type="file"]::file-selector-button {
    margin-right: 0.75rem;
    padding: 0.5rem 0.75rem;
    color: var(--primary);
    background: var(--surface-soft);
    border: 1px solid var(--border);
    border-radius: 0.375rem;
    font: inherit;
    font-weight: 600;
    cursor: pointer;
}

button {
    padding: 0.6875rem 1rem;
    color: #ffffff;
    background: var(--primary);
    border: 1px solid var(--primary);
    border-radius: 0.5rem;
    font: inherit;
    font-weight: 600;
    cursor: pointer;
}

button:hover {
    background: var(--primary-hover);
    border-color: var(--primary-hover);
}

article article {
    margin-top: 1.5rem;
    padding: 1.25rem;
    background: var(--surface-soft);
}

[role="alert"] {
    margin-top: 1.5rem;
    padding: 0.875rem 1rem;
    color: var(--danger);
    background: var(--danger-background);
    border: 1px solid #efc5c1;
    border-radius: 0.5rem;
}

progress {
    display: block;
    width: 100%;
    height: 0.5rem;
    overflow: hidden;
    appearance: none;
    background: var(--border);
    border: 0;
    border-radius: 999px;
}

progress::-webkit-progress-bar {
    background: var(--border);
}

progress::-webkit-progress-value {
    background: var(--primary);
    border-radius: 999px;
}

progress::-moz-progress-bar {
    background: var(--primary);
    border-radius: 999px;
}

ul {
    margin-bottom: 0;
    padding-left: 1.25rem;
}

li + li {
    margin-top: 0.5rem;
}

details {
    margin-top: 1rem;
}

summary {
    color: var(--primary);
    font-weight: 600;
    cursor: pointer;
}

details ul {
    margin-top: 1rem;
}

li > div {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
}

li > div p {
    margin-bottom: 0;
    color: var(--muted);
}

main > p:last-child {
    margin-top: 1.5rem;
    margin-bottom: 0;
    color: var(--muted);
    font-size: 0.875rem;
}

@media (max-width: 48rem) {
    header .container {
        padding-block: 0.875rem;
    }

    nav {
        align-items: flex-start;
        flex-direction: column;
        gap: 0;
    }

    main > .grid {
        grid-template-columns: minmax(0, 1fr);
    }
}

@media (prefers-reduced-motion: no-preference) {
    button,
    input[type="file"]::file-selector-button {
        transition: background-color 120ms ease, border-color 120ms ease;
    }
}
"""

app, rt = fast_app(
    hdrs=(Style(APP_CSS), Link(rel="icon", href="data:,")),
    pico=False,
    htmx=False,
    surreal=False,
    htmlkw={"data-theme": "light"},
)

CLASS_NAMES = {
    "healthy": "Tomato — Healthy",
    "early": "Tomato — Early Blight",
    "late": "Tomato — Late Blight",
    "mold": "Tomato — Leaf Mold",
}
DISPLAY_NAMES = {
    "healthy": "Daun sehat",
    "early": "Hawar awal",
    "late": "Hawar lanjut",
    "mold": "Kapang daun",
}


def predict_image(image: Image.Image) -> tuple[dict | None, dict | None]:
    image = image.resize((INPUT_WIDTH, INPUT_HEIGHT))
    pixels = np.asarray(image, dtype=np.float32)

    green_mask = (
        (pixels[:, :, 1] > pixels[:, :, 0] * 1.08)
        & (pixels[:, :, 1] > pixels[:, :, 2] * 1.08)
        & (pixels[:, :, 1] > 55)
    )
    green_ratio = float(np.mean(green_mask))
    if green_ratio < 0.08:
        return None, {
            "code": "NOT_A_LEAF",
            "message": "Gambar tidak terdeteksi sebagai daun tanaman.",
        }

    with interpreter_lock:
        interpreter.set_tensor(INPUT_INDEX, np.expand_dims(pixels, axis=0))
        interpreter.invoke()
        probabilities = interpreter.get_tensor(OUTPUT_INDEX)[0]

    predictions = {
        key: float(probability)
        for key, probability in zip(WEB_KEYS, probabilities)
    }
    top_index = int(np.argmax(probabilities))
    top_key = WEB_KEYS[top_index]
    confidence = float(probabilities[top_index])
    return {
        "top_key": top_key,
        "top_name": CLASS_NAMES[top_key],
        "confidence": confidence * 100,
        "uncertain": confidence < CONFIDENCE_THRESHOLD,
        "predictions": predictions,
    }, None


def read_image(image_bytes: bytes) -> Image.Image:
    return Image.open(BytesIO(image_bytes)).convert("RGB")


def result_section(result: dict | None, error: str | None):
    if error:
        return Article(P(error, role="alert"))
    if result is None:
        return Div()

    confidence = result["confidence"]
    score_items = [
        Li(
            Div(Strong(DISPLAY_NAMES.get(key, key)), P(f"{score:.1%}"), cls="grid"),
            Progress(value=score, max=1),
        )
        for key, score in result["predictions"].items()
    ]
    return Article(
        H2(DISPLAY_NAMES.get(result["top_key"], result["top_name"])),
        P(result["top_name"]),
        P(
            "Perlu foto lebih jelas"
            if result["uncertain"]
            else "Prediksi model"
        ),
        P(Strong("Skor prediksi"), f" {confidence:.1f}%"),
        Progress(value=confidence / 100, max=1),
        P(
            "Skor model masih rendah. Coba foto daun yang lebih fokus dengan "
            "pencahayaan merata."
            if result["uncertain"]
            else "Prediksi ini merupakan informasi awal, bukan diagnosis pasti "
            "kondisi tanaman."
        ),
        Details(Summary("Lihat skor semua kelas"), Ul(*score_items)),
    )


def page(result: dict | None = None, error: str | None = None):
    return (
        Title("PlantDoc AI — Pemeriksaan Daun Tomat"),
        Meta(name="viewport", content="width=device-width, initial-scale=1"),
        Header(
            Div(
                Nav(A(Strong("PlantDoc AI"), href="/"), P("Model berjalan lokal")),
                cls="container",
            )
        ),
        Main(
            Section(
                H1("Kenali kondisi daun, mulai dari fotonya."),
                P(
                    "Unggah foto daun tomat untuk melihat prediksi model dan skor "
                    "dari empat kelas yang dikenali."
                ),
            ),
            Div(
                Article(
                    H2("Mulai pemeriksaan"),
                    P("Pilih satu foto daun tomat yang terlihat jelas."),
                    Form(
                        Label(
                            "Foto daun",
                            Input(
                                type="file",
                                name="file",
                                accept=".jpg,.jpeg,.png,.webp",
                                required=True,
                            ),
                        ),
                        Button("Analisis foto", type="submit"),
                        action="/analyze",
                        method="post",
                        enctype="multipart/form-data",
                    ),
                    P("Foto diproses oleh model lokal dan tidak disimpan aplikasi."),
                    result_section(result, error),
                ),
                Aside(
                    H2("Agar foto lebih mudah dibaca"),
                    P(
                        "Fokuskan kamera pada satu daun, pastikan permukaannya "
                        "terlihat jelas, dan gunakan pencahayaan yang cukup."
                    ),
                    Hr(),
                    H3("Empat kelas yang dikenali"),
                    Ul(*(Li(name) for name in DISPLAY_NAMES.values())),
                ),
                cls="grid",
            ),
            P(
                "Gunakan hasil sebagai informasi awal, bukan pengganti pemeriksaan "
                "ahli tanaman."
            ),
            cls="container",
            lang="id",
        ),
    )


@rt("/", methods=["GET"])
def home():
    return page()


@rt("/analyze", methods=["POST"])
async def analyze(request: Request):
    form = await request.form()
    file = form.get("file")
    if not isinstance(file, UploadFile):
        return page(error="Pilih berkas gambar terlebih dahulu.")

    try:
        image = read_image(await file.read())
    except (UnidentifiedImageError, OSError, ValueError):
        return page(error="Gambar tidak dapat dibaca. Pilih JPG, PNG, atau WEBP.")

    result, error = await asyncio.to_thread(predict_image, image)
    if error:
        return page(error=error["message"])
    return page(result=result)


@rt("/health", methods=["GET"])
def health():
    return JSONResponse(
        {"status": "ok", "model": "model.tflite", "classes": WEB_KEYS}
    )


@rt("/predict", methods=["POST"])
async def predict_api(request: Request):
    form = await request.form()
    file = form.get("file")
    if not isinstance(file, UploadFile):
        return JSONResponse(status_code=400, content={"error": "File gambar diperlukan"})

    try:
        image = read_image(await file.read())
    except (UnidentifiedImageError, OSError, ValueError):
        return JSONResponse(status_code=400, content={"error": "Gambar tidak dapat dibaca"})

    result, error = await asyncio.to_thread(predict_image, image)
    if error:
        return JSONResponse(status_code=422, content={"error": error})
    return JSONResponse({"result": result})


if __name__ == "__main__":
    serve(
        appname="backend.app",
        host="127.0.0.1",
        port=5000,
        reload=False,
    )
