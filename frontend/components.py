from fasthtml.common import *


DISPLAY_NAMES = {
    "healthy": "Daun sehat",
    "early": "Hawar awal",
    "late": "Hawar lanjut",
    "mold": "Kapang daun",
    "unknown": "Bukan daun tomat / unknown",
}


def score_items(result: dict):
    items = []
    for key, score in result["predictions"].items():
        name = DISPLAY_NAMES.get(key, key)
        items.append(
            Li(
                Div(Strong(name, cls="score-name"), Span(f"{score:.1%}", cls="score-value")),
                Progress(
                    value=score,
                    max=1,
                    cls="score-bar",
                    aria_label=f"Skor {name}",
                ),
                cls="score-item",
            )
        )
    return items


def result_section(result: dict | None, error: str | None):
    if error:
        return Section(
            Article(
                Div(
                    H2("Hasil pemeriksaan", id="result-heading"),
                    Span("Belum selesai", cls="result-badge is-error"),
                    cls="result-heading",
                ),
                H3("Foto belum bisa dianalisis"),
                P(error, role="alert"),
                P("Coba foto daun tomat yang jelas, atau pilih JPG, PNG, atau WEBP lain."),
                cls="result-card is-error",
            ),
            cls="results",
            aria_labelledby="result-heading",
        )

    if result is None:
        return Div()

    confidence = result["confidence"]
    if result["rejected"]:
        return Section(
            Article(
                Div(
                    H2("Hasil pemeriksaan", id="result-heading"),
                    Span("Di luar cakupan", cls="result-badge is-rejected"),
                    cls="result-heading",
                ),
                Div(
                    Div(
                        H3("Kemungkinan di luar cakupan"),
                        P(result["top_name"], cls="result-subtitle"),
                    ),
                    Div(
                        P(Strong("Skor unknown"), cls="confidence-label"),
                        P(f"{confidence:.1f}%", cls="confidence-value"),
                        Progress(
                            value=confidence / 100,
                            max=1,
                            aria_label="Skor unknown",
                        ),
                        cls="confidence",
                    ),
                    cls="result-summary",
                ),
                P(
                    "Kelas unknown mendapat skor tertinggi. Coba foto satu daun "
                    "tomat yang terlihat jelas.",
                    cls="result-message",
                ),
                Details(
                    Summary("Lihat skor semua kelas"),
                    Ul(*score_items(result), cls="score-list"),
                ),
                cls="result-card is-rejected",
            ),
            cls="results",
            aria_labelledby="result-heading",
        )

    uncertain = result["uncertain"]
    state_class = "is-uncertain" if uncertain else "is-prediction"
    badge_text = "Perlu foto lebih jelas" if uncertain else "Prediksi tersedia"
    message = (
        "Skor model masih rendah. Coba foto daun yang lebih fokus dengan "
        "pencahayaan merata."
        if uncertain
        else "Prediksi ini merupakan informasi awal, bukan diagnosis pasti "
        "kondisi tanaman."
    )
    return Section(
        Article(
            Div(
                H2("Hasil pemeriksaan", id="result-heading"),
                Span(badge_text, cls=f"result-badge {state_class}"),
                cls="result-heading",
            ),
            Div(
                Div(
                    H3(DISPLAY_NAMES.get(result["top_key"], result["top_name"])),
                    P(result["top_name"], cls="result-subtitle"),
                ),
                Div(
                    P(Strong("Skor prediksi"), cls="confidence-label"),
                    P(f"{confidence:.1f}%", cls="confidence-value"),
                    Progress(
                        value=confidence / 100,
                        max=1,
                        aria_label="Skor prediksi",
                    ),
                    cls="confidence",
                ),
                cls="result-summary",
            ),
            P(message, cls="result-message"),
            Details(
                Summary("Lihat skor semua kelas"),
                Ul(*score_items(result), cls="score-list"),
            ),
            cls=f"result-card {state_class}",
        ),
        cls="results",
        aria_labelledby="result-heading",
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
        Meta(
            name="description",
            content="Pemeriksaan awal kondisi daun tomat dengan model PlantDoc yang berjalan lokal.",
        ),
        Meta(name="theme-color", content="#f4f6f1"),
        Header(
            Div(
                Nav(
                    A(
                        Svg(
                            Path(
                                d="M19.5 4.5c-7.2.2-12.4 2.8-13.8 7.8-1 3.6 1.8 6.7 5.3 6.2 5-.7 7.6-6.1 8.5-14Z",
                                fill="none",
                                stroke="currentColor",
                                stroke_width="1.8",
                                stroke_linecap="round",
                                stroke_linejoin="round",
                            ),
                            Path(
                                d="M4 20c2.8-5.1 6.3-8.6 11-11.3",
                                fill="none",
                                stroke="currentColor",
                                stroke_width="1.8",
                                stroke_linecap="round",
                                stroke_linejoin="round",
                            ),
                            viewBox="0 0 24 24",
                            cls="brand-mark",
                            aria_hidden="true",
                        ),
                        Strong("PlantDoc AI"),
                        href="/",
                        cls="brand",
                    ),
                    aria_label="Navigasi utama",
                ),
                P(
                    Span(cls="status-dot", aria_hidden="true"),
                    "Model berjalan lokal",
                    cls="model-status",
                ),
                cls="container header-inner",
            )
        ),
        Main(
            Section(
                H1("Periksa kondisi daun tomat."),
                P(
                    "Unggah satu foto daun untuk memperoleh prediksi kelas dan skor "
                    "keyakinan model."
                ),
                cls="intro",
            ),
            Div(
                Article(
                    H2("Unggah foto daun"),
                    P("Gunakan foto yang jelas agar model memiliki cukup detail untuk dianalisis."),
                    Form(
                        Div(
                            Label("Foto daun", For="leaf-photo"),
                            Input(
                                type="file",
                                name="file",
                                id="leaf-photo",
                                accept=".jpg,.jpeg,.png,.webp",
                                aria_describedby="file-help",
                                required=True,
                            ),
                            P("JPG, PNG, atau WEBP.", id="file-help", cls="field-help"),
                            cls="field",
                        ),
                        Button(
                            Span("Analisis foto"),
                            Svg(
                                Path(
                                    d="M5 12h14m-5-5 5 5-5 5",
                                    fill="none",
                                    stroke="currentColor",
                                    stroke_width="1.8",
                                    stroke_linecap="round",
                                    stroke_linejoin="round",
                                ),
                                viewBox="0 0 24 24",
                                cls="button-icon",
                                aria_hidden="true",
                            ),
                            type="submit",
                            cls="primary-button",
                        ),
                        action="/analyze",
                        method="post",
                        enctype="multipart/form-data",
                    ),
                    P(
                        "Foto diproses oleh model lokal dan tidak disimpan aplikasi.",
                        cls="privacy-note",
                    ),
                    cls="panel",
                ),
                Aside(
                    H2("Agar hasil lebih stabil"),
                    Ul(
                        Li(Strong("Satu daun per foto"), P("Jangan sertakan daun lain di dalam frame.")),
                        Li(Strong("Fokus tajam"), P("Detail permukaan daun harus terlihat.")),
                        Li(Strong("Cahaya merata"), P("Hindari bayangan kuat dan cahaya dari belakang.")),
                        cls="tip-list",
                    ),
                    Hr(),
                    H3(f"{len(class_keys)} kelas yang dikenali"),
                    Ul(*(Li(DISPLAY_NAMES.get(key, key)) for key in class_keys), cls="class-list"),
                    P(scope_message, cls="scope-note"),
                    cls="guidance",
                ),
                cls="workspace",
            ),
            result_section(result, error),
            cls="container",
            lang="id",
        ),
        Footer(
            P(
                "Gunakan hasil sebagai informasi awal, bukan pengganti pemeriksaan "
                "ahli tanaman."
            ),
            cls="container disclaimer",
        ),
    )
