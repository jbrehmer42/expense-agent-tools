---
name: howto
description: Help the user on how to use this repo and get the python tooling working. Use when the user asks "how to", is unsure how to set up or use Python, virtural environments, the PDF converter, or reports errors from tools/pdf_to_text.py (missing pdfplumber, wrong Python, no extractable text).
---

Tell the user how they can use this repository and its tools. Answer their questions if they have any. Guide them through technical setup if they are unsure or encounter issues.


## Python tooling

The tooling of this repo is a simple Python script to get text from PDF files (`tools/pdf_to_text.py`).
It needs a Python virtual environment that has `pdfplumber` installed. It does not matter how that environment was created.

### Rules

- Run commands for the user, but ask for confirmation before installing anything.
- Never modify the system Python. Install packages only into a virtual environment.

### Finding a working environment

1. Check whether the user already has one: ask, or look for an environment (for example `.venv/` in the repo) and test with `<python> -c "import pdfplumber"`.
2. If it works, use that interpreter: `<python> tools/pdf_to_text.py`.
3. If the user has no environment, or is not comfortable with Python and virtual environments, recommend `uv` and offer the setup below.

### Recommended setup for non-technical users: uv

1. Check whether `uv` is installed: `uv --version`.
2. If missing, point the user to [astral docs](https://docs.astral.sh/uv/getting-started/installation/).
3. From the repo root run `uv sync`. This creates `.venv` with `pdfplumber` and, if needed, downloads a suitable Python.

## Troubleshooting

- "pdfplumber is not installed": the Python that ran the script has no `pdfplumber`. Use an environment that has it, or set one up as above.
- "no extractable text": the PDF might be a scanned image. OCR is not supported; ask the user to enter the receipt data manually.
