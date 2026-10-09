"""Convert PDF receipts to text files next to the PDFs (x.pdf -> x.txt).

Usage: uv run tools/pdf_to_text.py [PATH ...] [--layout] [--force]
PATH is a PDF file or a directory (searched recursively); default is receipts/.
"""

import argparse
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit(
        "pdfplumber is not installed in this Python environment.\n"
        "Fix: run `uv sync` and start the script with `uv run tools/pdf_to_text.py`,\n"
        "or install it with `pip install pdfplumber` in the environment you use.\n"
        "Ask the agent to run the `howto` skill if you need help."
    )

DEFAULT_DIR = Path(__file__).resolve().parent.parent / "receipts"


def find_pdfs(paths: list[Path]) -> tuple[list[Path], bool]:
    found = []
    missing = False
    for path in paths:
        if path.is_dir():
            found.extend(
                sorted(p for p in path.rglob("*") if p.suffix.lower() == ".pdf")
            )
        elif path.is_file():
            found.append(path)
        else:
            print(f"error: not found: {path}", file=sys.stderr)
            missing = True
    return found, missing


def extract(pdf_path: Path, layout: bool) -> str:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            text = (page.extract_text(layout=layout) or "").strip("\n")
            pages.append(f"--- page {number} ---\n{text}")
    return "\n".join(pages) + "\n"


def has_text(extracted: str) -> bool:
    return any(
        line.strip() and not line.startswith("--- page ")
        for line in extracted.splitlines()
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="PDF files or directories (default: receipts/)",
    )
    parser.add_argument(
        "--layout", action="store_true", help="keep column alignment (wider output)"
    )
    parser.add_argument(
        "--force", action="store_true", help="re-convert even if the .txt is up to date"
    )
    args = parser.parse_args()

    pdfs, missing = find_pdfs(args.paths or [DEFAULT_DIR])
    status = 1 if missing else 0
    for pdf_path in pdfs:
        txt_path = pdf_path.with_suffix(".txt")
        if (
            not args.force
            and txt_path.exists()
            and txt_path.stat().st_mtime >= pdf_path.stat().st_mtime
        ):
            print(f"up to date: {txt_path}")
            continue
        try:
            extracted = extract(pdf_path, args.layout)
        except Exception as e:
            print(f"error: cannot read {pdf_path}: {e}", file=sys.stderr)
            status = 1
            continue
        if not has_text(extracted):
            print(
                f"error: no extractable text in {pdf_path} (OCR is not supported)",
                file=sys.stderr,
            )
            status = 1
            continue
        txt_path.write_text(extracted, encoding="utf-8")
        print(f"wrote: {txt_path}")
    return status


if __name__ == "__main__":
    sys.exit(main())
