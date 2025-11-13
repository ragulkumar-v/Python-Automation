#!/usr/bin/env python3
"""
Batch PDF → Word converter (no CLI args).

Simply configure INPUT_FOLDER and OUTPUT_FOLDER below,
then run:

    python pdf_to_word.py
"""

from pathlib import Path
from pdf2docx import Converter

# === Configuration: set your folders here ===
INPUT_FOLDER = Path(r"C:\RA work\SEC Rule 606 Datasets\9july\Wolverine\pdf")
OUTPUT_FOLDER = Path(
    r"C:\RA work\SEC Rule 606 Datasets\9july\Wolverine\word")
# ===========================================


def convert_pdf_to_docx(pdf_path: Path, docx_path: Path) -> bool:
    """
    Convert a single PDF to DOCX. Returns True on success.
    """
    try:
        conv = Converter(str(pdf_path))
        conv.convert(str(docx_path), start=0, end=None)
        conv.close()
        return True
    except Exception as e:
        print(f"⚠️ Warning: Failed to convert '{pdf_path.name}': {e}")
        return False


def main():
    # Ensure output directory exists, create if missing
    if not OUTPUT_FOLDER.exists():
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        print(f"ℹ️ Created output folder: '{OUTPUT_FOLDER}'")

    pdf_files = sorted(INPUT_FOLDER.glob("*.pdf"))
    if not pdf_files:
        print(f"❗ Caution: No PDF files found in '{INPUT_FOLDER}'")
        return

    for pdf in pdf_files:
        docx_file = OUTPUT_FOLDER / f"{pdf.stem}.docx"
        success = convert_pdf_to_docx(pdf, docx_file)

        if success and docx_file.exists() and docx_file.stat().st_size > 0:
            print(f"✅ Converted '{pdf.name}' → '{docx_file.name}'")
        else:
            print(f"⚠️ Warning: '{pdf.name}' was not converted successfully.")


if __name__ == "__main__":
    main()
