APP_CSS = """
:root {
    color-scheme: light;
    --background: #f4f6f1;
    --surface: #ffffff;
    --surface-soft: #edf3e9;
    --text: #17251c;
    --muted: #59695e;
    --border: #d5ded1;
    --primary: #245b3a;
    --primary-hover: #19462c;
    --primary-soft: #e3eee1;
    --warning: #865513;
    --warning-background: #fff3dc;
    --danger: #932d28;
    --danger-background: #fff0ee;
    --radius: 0.875rem;
    --container: 70rem;
    --shadow: 0 1rem 2.5rem rgba(23, 37, 28, 0.07);
}

* {
    box-sizing: border-box;
    scrollbar-width: thin;
    scrollbar-color: #b7c4b3 transparent;
}

::-webkit-scrollbar {
    width: 0.625rem;
    height: 0.625rem;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #b7c4b3;
    border: 0.125rem solid var(--background);
    border-radius: 999px;
}

::selection {
    color: var(--text);
    background: #d8e8d3;
}

body {
    margin: 0;
    color: var(--text);
    background: var(--background);
    font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    line-height: 1.55;
}

a {
    color: var(--primary);
    text-underline-offset: 0.18em;
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

.header-inner {
    min-height: 4.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.brand {
    display: inline-flex;
    align-items: center;
    gap: 0.625rem;
    color: var(--text);
    font-size: 1.0625rem;
    letter-spacing: -0.01em;
    text-decoration: none;
}

.brand-mark {
    width: 1.75rem;
    height: 1.75rem;
    color: var(--primary);
}

.model-status {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0;
    color: var(--muted);
    font-size: 0.875rem;
}

.status-dot {
    width: 0.5rem;
    height: 0.5rem;
    flex: 0 0 auto;
    background: var(--primary);
    border-radius: 50%;
    box-shadow: 0 0 0 0.1875rem var(--primary-soft);
}

.container {
    width: min(calc(100% - 2rem), var(--container));
    margin-inline: auto;
}

main.container {
    padding-block: 2.75rem 3rem;
}

.intro {
    max-width: 46rem;
    margin-bottom: 2rem;
}

h1,
h2,
h3,
p {
    margin-top: 0;
}

h1 {
    margin-bottom: 0.875rem;
    font-size: 2.5rem;
    line-height: 1.15;
    letter-spacing: -0.035em;
    text-wrap: balance;
}

h2 {
    margin-bottom: 0.625rem;
    font-size: 1.25rem;
    line-height: 1.3;
    letter-spacing: -0.015em;
    text-wrap: balance;
}

h3 {
    margin-bottom: 0.375rem;
    font-size: 1rem;
    line-height: 1.4;
}

p {
    margin-bottom: 1rem;
}

.workspace {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 19rem;
    gap: 1.5rem;
    align-items: start;
}

.panel,
.guidance,
.result-card {
    min-width: 0;
    border: 1px solid var(--border);
    border-radius: var(--radius);
}

.panel {
    padding: 2rem;
    background: var(--surface);
    box-shadow: var(--shadow);
}

.guidance {
    padding: 1.5rem;
    background: var(--surface-soft);
}

form {
    margin-top: 1.5rem;
}

.field {
    margin-bottom: 1.25rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-size: 0.9375rem;
    font-weight: 650;
}

input[type="file"] {
    width: 100%;
    min-width: 0;
    margin: 0;
    padding: 0.5rem;
    color: var(--muted);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 0.625rem;
    font: inherit;
    font-size: 0.9375rem;
}

input[type="file"]::file-selector-button {
    margin-right: 0.75rem;
    padding: 0.5625rem 0.75rem;
    color: var(--primary);
    background: var(--primary-soft);
    border: 1px solid #c8d8c4;
    border-radius: 0.5rem;
    font: inherit;
    font-weight: 650;
    cursor: pointer;
}

input[type="file"]::file-selector-button:hover {
    background: #d7e7d4;
}

.field-help {
    margin: 0.5rem 0 0;
    color: var(--muted);
    font-size: 0.8125rem;
}

.primary-button {
    min-height: 2.75rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.6875rem 1rem;
    color: #ffffff;
    background: var(--primary);
    border: 1px solid var(--primary);
    border-radius: 0.625rem;
    box-shadow: 0 0.375rem 0.875rem rgba(36, 91, 58, 0.16);
    font: inherit;
    font-weight: 650;
    cursor: pointer;
    transition: background-color 150ms ease, border-color 150ms ease, box-shadow 150ms ease;
}

.primary-button:hover {
    background: var(--primary-hover);
    border-color: var(--primary-hover);
    box-shadow: 0 0.5rem 1rem rgba(36, 91, 58, 0.2);
}

.primary-button:active {
    background: var(--primary-hover);
    box-shadow: 0 0.125rem 0.375rem rgba(36, 91, 58, 0.18);
}

.primary-button:disabled {
    color: #e5ebe3;
    background: #75857a;
    border-color: #75857a;
    box-shadow: none;
    cursor: not-allowed;
}

.button-icon {
    width: 1.125rem;
    height: 1.125rem;
    flex: 0 0 auto;
}

.privacy-note {
    margin: 1rem 0 0;
    color: var(--muted);
    font-size: 0.875rem;
}

.tip-list {
    margin: 0;
    padding: 0;
    list-style: none;
}

.tip-list li {
    padding-block: 0.75rem;
    border-top: 1px solid #d8e2d3;
}

.tip-list li:first-child {
    padding-top: 0;
    border-top: 0;
}

.tip-list li:last-child {
    padding-bottom: 0;
}

.tip-list strong {
    display: block;
    font-size: 0.9375rem;
}

.tip-list p {
    margin: 0.125rem 0 0;
    color: var(--muted);
    font-size: 0.875rem;
}

hr {
    margin-block: 1.5rem;
    border: 0;
    border-top: 1px solid #d8e2d3;
}

.class-list {
    margin: 0;
    padding-left: 1.125rem;
    font-size: 0.9375rem;
}

.class-list li + li {
    margin-top: 0.25rem;
}

.scope-note {
    margin: 1rem 0 0;
    padding-top: 1rem;
    color: var(--muted);
    border-top: 1px solid #d8e2d3;
    font-size: 0.8125rem;
    line-height: 1.5;
}

.results {
    margin-top: 1.5rem;
}

.result-card {
    padding: 1.75rem 2rem;
    background: var(--surface);
    border-top: 0.1875rem solid var(--primary);
    box-shadow: var(--shadow);
}

.result-card.is-uncertain {
    border-top-color: var(--warning);
}

.result-card.is-rejected {
    border-top-color: var(--danger);
}

.result-card.is-error {
    border-top-color: var(--danger);
}

.result-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.25rem;
}

.result-heading h2 {
    margin: 0;
}

.result-badge {
    display: inline-flex;
    align-items: center;
    flex: 0 0 auto;
    padding: 0.25rem 0.5625rem;
    color: var(--primary);
    background: var(--primary-soft);
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 650;
    line-height: 1.4;
}

.result-badge.is-uncertain {
    color: var(--warning);
    background: var(--warning-background);
}

.result-badge.is-rejected,
.result-badge.is-error {
    color: var(--danger);
    background: var(--danger-background);
}

.result-summary {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(10rem, 14rem);
    gap: 2rem;
    align-items: center;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
}

.result-summary h3 {
    margin-bottom: 0.25rem;
    font-size: 1.5rem;
    line-height: 1.25;
    letter-spacing: -0.02em;
}

.result-subtitle {
    margin: 0;
    color: var(--muted);
    font-size: 0.9375rem;
}

.confidence {
    min-width: 0;
    text-align: right;
}

.confidence-label {
    margin: 0;
    color: var(--muted);
    font-size: 0.8125rem;
}

.confidence-value {
    margin: 0.25rem 0 0.5rem;
    font-size: 2rem;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.03em;
    line-height: 1.1;
}

progress {
    display: block;
    width: 100%;
    height: 0.5rem;
    overflow: hidden;
    appearance: none;
    background: #e2e8de;
    border: 0;
    border-radius: 999px;
}

progress::-webkit-progress-bar {
    background: #e2e8de;
    border-radius: 999px;
}

progress::-webkit-progress-value {
    background: var(--primary);
    border-radius: 999px;
}

progress::-moz-progress-bar {
    background: var(--primary);
    border-radius: 999px;
}

.is-uncertain progress::-webkit-progress-value,
.is-uncertain progress::-moz-progress-bar {
    background: var(--warning);
}

.is-rejected progress::-webkit-progress-value,
.is-rejected progress::-moz-progress-bar {
    background: var(--danger);
}

.result-message {
    max-width: 65ch;
    margin: 1rem 0 0;
    color: #3f5044;
}

details {
    margin-top: 1rem;
    padding-top: 0.875rem;
    border-top: 1px solid var(--border);
}

summary {
    width: fit-content;
    color: var(--primary);
    font-weight: 650;
    cursor: pointer;
}

.score-list {
    display: grid;
    gap: 0.75rem;
    margin: 0.875rem 0 0;
    padding: 0;
    list-style: none;
}

.score-item {
    min-width: 0;
}

.score-item > div {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
}

.score-name {
    font-size: 0.9375rem;
    font-weight: 600;
}

.score-value {
    color: var(--muted);
    font-size: 0.875rem;
    font-variant-numeric: tabular-nums;
}

.score-bar {
    height: 0.375rem;
    margin-top: 0.375rem;
}

.result-card.is-error h3 {
    margin-top: 1rem;
    font-size: 1.125rem;
}

.result-card.is-error [role="alert"] {
    margin: 0.75rem 0;
    padding: 0.75rem 0.875rem;
    color: var(--danger);
    background: var(--danger-background);
    border: 1px solid #efc5c1;
    border-radius: 0.5rem;
}

.result-card.is-error > p:last-child {
    margin-bottom: 0;
    color: var(--muted);
    font-size: 0.875rem;
}

.disclaimer {
    margin: 0;
    padding-bottom: 2rem;
    color: var(--muted);
    font-size: 0.8125rem;
}

@media (max-width: 48rem) {
    .header-inner {
        min-height: 4.25rem;
    }

    main.container {
        padding-block: 2rem 2.5rem;
    }

    h1 {
        font-size: 2rem;
    }

    .workspace {
        grid-template-columns: minmax(0, 1fr);
    }

    .panel,
    .guidance,
    .result-card {
        padding: 1.25rem;
    }

    .result-summary {
        grid-template-columns: minmax(0, 1fr);
        gap: 1rem;
    }

    .confidence {
        text-align: left;
    }

    .confidence-value {
        font-size: 1.75rem;
    }
}

@media (max-width: 30rem) {
    .container {
        width: min(calc(100% - 1.25rem), var(--container));
    }

    .header-inner {
        gap: 0.5rem;
    }

    .brand {
        gap: 0.5rem;
        font-size: 1rem;
    }

    .brand-mark {
        width: 1.5rem;
        height: 1.5rem;
    }

    .model-status {
        gap: 0.375rem;
        font-size: 0.75rem;
    }

    h1 {
        font-size: 1.875rem;
    }

    .intro {
        margin-bottom: 1.5rem;
    }

    .primary-button {
        width: 100%;
    }

    .result-heading {
        align-items: flex-start;
        flex-direction: column;
        gap: 0.625rem;
    }
}

@media (prefers-reduced-motion: no-preference) {
    .primary-button,
    input[type="file"]::file-selector-button {
        transition: background-color 150ms ease, border-color 150ms ease, box-shadow 150ms ease;
    }
}

@media (forced-colors: active) {
    .status-dot {
        background: CanvasText;
        box-shadow: none;
    }

    progress {
        border: 1px solid CanvasText;
    }
}
"""
