**[English](README.md)** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Français](README.fr.md) | [한국어](README.ko.md)

# Doc Extract

Extract text from PDF and EPUB files. Auto-detects scanned vs text PDFs and uses the optimal extraction method.

## Features

- **Smart PDF detection**: auto-detects scanned vs text-based PDF (checks first 5 pages)
- **Local OCR**: RapidOCR for scanned PDFs (no API key needed, supports 30+ languages)
- **Fast text extraction**: PyMuPDF for text-based PDFs (instant)
- **EPUB support**: extract text from EPUB books with chapter structure
- **Force OCR mode**: optionally force OCR for all PDFs

## Requirements

- Python 3.8+

## Installation

```bash
pip install pymupdf rapidocr-onnxruntime ebooklib beautifulsoup4 lxml pillow
```

## Usage

```bash
# Auto-detect and extract
python doc_extract.py document.pdf
python doc_extract.py document.epub

# Specify output file
python doc_extract.py document.pdf --output extracted.txt

# Force OCR mode (useful for PDFs with embedded text + images)
python doc_extract.py document.pdf --force-ocr

# Custom OCR DPI (higher = better quality but slower)
python doc_extract.py scanned.pdf --ocr-dpi 300
python doc_extract.py scanned.pdf --ocr-dpi 600
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output` | {name}_extracted.txt | Output file path |
| `--force-ocr` | false | Force OCR for all PDFs |
| `--ocr-dpi` | 300 | OCR DPI (higher = better but slower) |

## How It Works

```
Input file
  |-- .pdf -> check first 5 pages for embedded text
  |   |-- < 50 chars -> scanned -> RapidOCR at 300 DPI (~1s/page)
  |   +-- >= 50 chars -> text-based -> PyMuPDF direct extraction (instant)
  +-- .epub -> ebooklib + BeautifulSoup (instant)

Output: {original_name}_extracted.txt in same directory
```

## OCR Engine

Uses [RapidOCR](https://github.com/RapidAI/RapidOCR) (ONNX Runtime backend):
- Local, free, no API key needed
- Supports Chinese, English, Japanese, Korean + 30 languages
- Typically ~1 second per page at 300 DPI

## Output Format

```
=== Page 1 ===
Extracted text from page 1...

=== Page 2 ===
Extracted text from page 2...
```

For EPUB files:

```
# Book Title

Chapter 1 text...

Chapter 2 text...
```

## License

MIT
