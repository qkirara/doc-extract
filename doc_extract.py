#!/usr/bin/env python3
"""
doc_extract.py - Extract text from PDF and EPUB files.

Supports:
- Text-based PDF (PyMuPDF direct extraction)
- Scanned PDF (RapidOCR local OCR)
- EPUB (ebooklib + BeautifulSoup)

Usage:
    python doc_extract.py document.pdf
    python doc_extract.py document.epub --output extracted.txt
    python doc_extract.py scanned.pdf --force-ocr --ocr-dpi 300
"""

import argparse
import os
import sys
import warnings
from pathlib import Path

import fitz  # PyMuPDF

from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def is_scanned_pdf(pdf_path: str, sample_pages: int = 5) -> bool:
    """Detect if a PDF is scanned (image-only) by checking embedded text."""
    doc = fitz.open(pdf_path)
    total_chars = 0
    for i in range(min(sample_pages, doc.page_count)):
        total_chars += len(doc[i].get_text().strip())
    doc.close()
    return total_chars < 50


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from a text-based PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    texts = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            texts.append(f"=== Page {i + 1} ===\n{text}")
    doc.close()
    return "\n\n".join(texts)


def extract_pdf_ocr(pdf_path: str, dpi: int = 300) -> str:
    """Extract text from a scanned PDF using RapidOCR."""
    import numpy as np
    from PIL import Image
    from rapidocr_onnxruntime import RapidOCR

    ocr_engine = RapidOCR()
    doc = fitz.open(pdf_path)
    texts = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_np = np.array(img)
        result, _ = ocr_engine(img_np)
        if result:
            page_text = "\n".join([line[1] for line in result])
            texts.append(f"=== Page {i + 1} ===\n{page_text}")

    doc.close()
    return "\n\n".join(texts)


def extract_epub(epub_path: str) -> str:
    """Extract text from an EPUB file using ebooklib."""
    import ebooklib
    from ebooklib import epub

    book = epub.read_epub(epub_path)

    # Metadata
    title_meta = book.get_metadata("DC", "title")
    title = title_meta[0][0] if title_meta else ""

    # Extract all chapter text
    texts = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "lxml")
        text = soup.get_text(separator="\n", strip=True)
        if text.strip():
            texts.append(text.strip())

    full_text = "\n\n".join(texts)
    if title:
        full_text = f"# {title}\n\n" + full_text

    return full_text


def extract_text(
    input_path: str,
    output_path: str = None,
    force_ocr: bool = False,
    ocr_dpi: int = 300,
) -> str:
    """Extract text from a PDF or EPUB file.

    Args:
        input_path: Path to the input file (.pdf or .epub)
        output_path: Path to the output file (default: same dir as input, _extracted.txt)
        force_ocr: Force OCR even for text-based PDFs
        ocr_dpi: DPI for OCR processing (default: 300)

    Returns:
        Extracted text content
    """
    input_path = os.path.abspath(input_path)
    if not os.path.isfile(input_path):
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(input_path)[1].lower()

    # Auto-generate output path
    if not output_path:
        stem = Path(input_path).stem
        output_path = os.path.join(os.path.dirname(input_path), f"{stem}_extracted.txt")

    if ext == ".epub":
        print(f"Extracting EPUB: {input_path}")
        text = extract_epub(input_path)
        method = "ebooklib"

    elif ext == ".pdf":
        if force_ocr:
            print(f"Extracting PDF with OCR (forced): {input_path}")
            text = extract_pdf_ocr(input_path, ocr_dpi)
            method = f"RapidOCR ({ocr_dpi} DPI)"
        elif is_scanned_pdf(input_path):
            print(f"Detected scanned PDF, using OCR: {input_path}")
            text = extract_pdf_ocr(input_path, ocr_dpi)
            method = f"RapidOCR ({ocr_dpi} DPI)"
        else:
            print(f"Extracting text PDF: {input_path}")
            text = extract_pdf_text(input_path)
            method = "PyMuPDF"
    else:
        print(f"Error: Unsupported format: {ext}", file=sys.stderr)
        print("Supported formats: .pdf, .epub", file=sys.stderr)
        sys.exit(1)

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Stats
    pages = text.count("=== Page ") if ext == ".pdf" else ""
    print(f"Method: {method}")
    print(f"Characters: {len(text)}")
    if pages:
        print(f"Pages: {pages}")
    print(f"Output: {output_path}")

    return text


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDF and EPUB files"
    )
    parser.add_argument("input", help="Input file path (.pdf or .epub)")
    parser.add_argument("--output", default=None, help="Output file path (default: {input_name}_extracted.txt)")
    parser.add_argument("--force-ocr", action="store_true", help="Force OCR for all PDFs")
    parser.add_argument("--ocr-dpi", type=int, default=300, help="OCR DPI (default: 300)")

    args = parser.parse_args()

    extract_text(
        input_path=args.input,
        output_path=args.output,
        force_ocr=args.force_ocr,
        ocr_dpi=args.ocr_dpi,
    )


if __name__ == "__main__":
    main()
