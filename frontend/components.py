from fasthtml.common import *


DISPLAY_NAMES = {
    "healthy": "Daun sehat",
    "early": "Hawar awal",
    "late": "Hawar lanjut",
    "mold": "Kapang daun",
    "unknown": "Bukan daun tomat / unknown",
}


def score_items(result: dict):
    return [
        Li(
            Div(Strong(DISPLAY_NAMES.get(key, key)), P(f"{score:.1%}"), cls="grid"),
            Progress(value=score, max=1),
        )
        for key, score in result["predictions"].items()
    ]


def result_section(result: dict | None, error: str | None):
    if error:
        return Article(P(error, role="alert"))
    if result is None:
        return Div()

    confidence = result["confidence"]
    if result["rejected"]:
        return Article(
            H2("Bukan daun tomat"),
            P(
                "Model memasukkan gambar ke kelas unknown. Coba foto satu daun "
                "tomat yang terlihat jelas."
            ),
            P(Strong("Skor unknown"), f" {confidence:.1f}%"),
            Progress(value=confidence / 100, max=1),
            Details(Summary("Lihat skor semua kelas"), Ul(*score_items(result))),
        )

    return Article(
        H2(DISPLAY_NAMES.get(result["top_key"], result["top_name"])),
        P(result["top_name"]),
        P("Perlu foto lebih jelas" if result["uncertain"] else "Prediksi model"),
        P(Strong("Skor prediksi"), f" {confidence:.1f}%"),
        Progress(value=confidence / 100, max=1),
        P(
            "Skor model masih rendah. Coba foto daun yang lebih fokus dengan "
            "pencahayaan merata."
            if result["uncertain"]
            else "Prediksi ini merupakan informasi awal, bukan diagnosis pasti "
            "kondisi tanaman."
        ),
        Details(Summary("Lihat skor semua kelas"), Ul(*score_items(result))),
    )


def page(result: dict | None = None, error: str | None = None, model_info: dict | None = None):
    model_info = model_info or {}
    class_keys = model_info.get("classes", [])
    scope_message = (
        "Model memiliki kelas unknown untuk menolak gambar di luar cakupan, tetapi "
        "penolakan tetap bergantung pada data dan hasil evaluasi."
        if model_info.get("supports_unknown")
        else "Model saat ini belum memiliki kelas unknown; penolakan non-daun masih "
        "menggunakan filter heuristik."
    )
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
                    "dari kelas yang dikenali."
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
                    H3(f"{len(class_keys)} kelas yang dikenali"),
                    Ul(*(Li(DISPLAY_NAMES.get(key, key)) for key in class_keys)),
                    P(scope_message),
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
