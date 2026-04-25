[English](README.md) | **[简体中文](README.zh-CN.md)** | [日本語](README.ja.md) | [Français](README.fr.md) | [한국어](README.ko.md)

# Doc Extract

从 PDF 和 EPUB 文件中提取文本。自动识别扫描版与文本版 PDF，并选择最优的提取方式。

## 功能特性

- **智能 PDF 检测**：自动识别扫描版与文本版 PDF（检查前 5 页）
- **本地 OCR**：使用 RapidOCR 处理扫描版 PDF（无需 API 密钥，支持 30+ 种语言）
- **快速文本提取**：使用 PyMuPDF 提取文本版 PDF（即时完成）
- **EPUB 支持**：从 EPUB 电子书中提取文本，保留章节结构
- **强制 OCR 模式**：可选择对所有 PDF 强制使用 OCR

## 环境要求

- Python 3.8+

## 安装

```bash
pip install pymupdf rapidocr-onnxruntime ebooklib beautifulsoup4 lxml pillow
```

## 使用方法

```bash
# 自动检测并提取
python doc_extract.py document.pdf
python doc_extract.py document.epub

# 指定输出文件
python doc_extract.py document.pdf --output extracted.txt

# 强制 OCR 模式（适用于同时包含嵌入文本和图片的 PDF）
python doc_extract.py document.pdf --force-ocr

# 自定义 OCR DPI（数值越高，识别质量越好，但速度越慢）
python doc_extract.py scanned.pdf --ocr-dpi 300
python doc_extract.py scanned.pdf --ocr-dpi 600
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output` | {name}_extracted.txt | 输出文件路径 |
| `--force-ocr` | false | 对所有 PDF 强制使用 OCR |
| `--ocr-dpi` | 300 | OCR 分辨率（数值越高识别效果越好，但速度越慢） |

## 工作原理

```
输入文件
  |-- .pdf -> 检查前 5 页是否包含嵌入文本
  |   |-- < 50 字符 -> 扫描版 -> RapidOCR 以 300 DPI 处理（约 1 秒/页）
  |   +-- >= 50 字符 -> 文本版 -> PyMuPDF 直接提取（即时完成）
  +-- .epub -> ebooklib + BeautifulSoup（即时完成）

输出：同目录下的 {原文件名}_extracted.txt
```

## OCR 引擎

使用 [RapidOCR](https://github.com/RapidAI/RapidOCR)（ONNX Runtime 后端）：
- 本地运行，免费，无需 API 密钥
- 支持中文、英文、日文、韩文等 30+ 种语言
- 300 DPI 下通常每页约 1 秒

## 输出格式

```
=== 第 1 页 ===
第 1 页的提取文本...

=== 第 2 页 ===
第 2 页的提取文本...
```

EPUB 文件输出格式：

```
# 书名

第 1 章文本...

第 2 章文本...
```

## 许可证

MIT
