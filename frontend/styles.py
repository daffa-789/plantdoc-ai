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
