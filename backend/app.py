import asyncio

from fasthtml.common import *
from PIL import Image, UnidentifiedImageError
from starlette.datastructures import UploadFile
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.inference import model, read_image
from frontend.components import page
from frontend.styles import APP_CSS


app, rt = fast_app(
    hdrs=(Style(APP_CSS), Link(rel="icon", href="data:,")),
    pico=False,
    htmx=False,
    surreal=False,
    htmlkw={"data-theme": "light"},
)


@rt("/", methods=["GET"])
def home():
    return page(model_info=model.metadata())


@rt("/analyze", methods=["POST"])
async def analyze(request: Request):
    form = await request.form()
    file = form.get("file")
    if not isinstance(file, UploadFile):
        return page(error="Pilih berkas gambar terlebih dahulu.", model_info=model.metadata())

    try:
        image = read_image(await file.read())
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        return page(
            error="Gambar tidak dapat dibaca. Pilih JPG, PNG, atau WEBP.",
            model_info=model.metadata(),
        )

    result, error = await asyncio.to_thread(model.predict_image, image)
    if error:
        return page(error=error["message"], model_info=model.metadata())
    return page(result=result, model_info=model.metadata())


@rt("/health", methods=["GET"])
def health():
    return JSONResponse({"status": "ok", **model.metadata()})


@rt("/predict", methods=["POST"])
async def predict_api(request: Request):
    form = await request.form()
    file = form.get("file")
    if not isinstance(file, UploadFile):
        return JSONResponse(status_code=400, content={"error": "File gambar diperlukan"})

    try:
        image = read_image(await file.read())
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        return JSONResponse(status_code=400, content={"error": "Gambar tidak dapat dibaca"})

    result, error = await asyncio.to_thread(model.predict_image, image)
    if error:
        return JSONResponse(status_code=422, content={"error": error, "result": result})
    if result["rejected"]:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": result["rejection_code"],
                    "message": "Gambar tidak terdeteksi sebagai daun tomat.",
                },
                "result": result,
            },
        )
    return JSONResponse({"result": result})


if __name__ == "__main__":
    raise SystemExit("Gunakan python main.py untuk menjalankan aplikasi")
