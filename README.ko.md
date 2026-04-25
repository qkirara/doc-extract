[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Français](README.fr.md) | **한국어**

# Doc Extract

PDF 및 EPUB 파일에서 텍스트를 추출합니다. 스캔 PDF와 텍스트 PDF를 자동으로 감지하여 최적의 추출 방식을 선택합니다.

## 기능

- **스마트 PDF 감지**: 스캔 PDF와 텍스트 PDF를 자동 감지 (처음 5페이지 확인)
- **로컬 OCR**: 스캔 PDF에 RapidOCR 사용 (API 키 불필요, 30개 이상 언어 지원)
- **빠른 텍스트 추출**: 텍스트 PDF에 PyMuPDF 사용 (즉시 완료)
- **EPUB 지원**: EPUB 전자책에서 챕터 구조를 유지한 채 텍스트 추출
- **강제 OCR 모드**: 모든 PDF에 대해 OCR을 강제로 활성화 가능

## 요구 사항

- Python 3.8+

## 설치

```bash
pip install pymupdf rapidocr-onnxruntime ebooklib beautifulsoup4 lxml pillow
```

## 사용법

```bash
# 자동 감지 및 추출
python doc_extract.py document.pdf
python doc_extract.py document.epub

# 출력 파일 지정
python doc_extract.py document.pdf --output extracted.txt

# 강제 OCR 모드 (내장 텍스트와 이미지가 혼합된 PDF에 유용)
python doc_extract.py document.pdf --force-ocr

# 사용자 지정 OCR DPI (높을수록 품질 향상, 속도 저하)
python doc_extract.py scanned.pdf --ocr-dpi 300
python doc_extract.py scanned.pdf --ocr-dpi 600
```

## 매개변수

| 매개변수 | 기본값 | 설명 |
|---------|--------|------|
| `--output` | {name}_extracted.txt | 출력 파일 경로 |
| `--force-ocr` | false | 모든 PDF에 OCR 강제 적용 |
| `--ocr-dpi` | 300 | OCR DPI (높을수록 품질 향상, 속도 저하) |

## 작동 방식

```
입력 파일
  |-- .pdf -> 처음 5페이지에서 내장 텍스트 확인
  |   |-- < 50자 -> 스캔 PDF -> RapidOCR로 300 DPI 처리 (~1초/페이지)
  |   +-- >= 50자 -> 텍스트 PDF -> PyMuPDF로 직접 추출 (즉시 완료)
  +-- .epub -> ebooklib + BeautifulSoup (즉시 완료)

출력: 동일 디렉토리에 {원본_파일명}_extracted.txt
```

## OCR 엔진

[RapidOCR](https://github.com/RapidAI/RapidOCR) (ONNX Runtime 백엔드) 사용:
- 로컬 실행, 무료, API 키 불필요
- 중국어, 영어, 일본어, 한국어 등 30개 이상 언어 지원
- 300 DPI에서 일반적으로 페이지당 약 1초

## 출력 형식

```
=== 1페이지 ===
1페이지에서 추출된 텍스트...

=== 2페이지 ===
2페이지에서 추출된 텍스트...
```

EPUB 파일의 경우:

```
# 도서 제목

1장 텍스트...

2장 텍스트...
```

## 라이선스

MIT
