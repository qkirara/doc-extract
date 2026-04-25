[English](README.md) | [简体中文](README.zh-CN.md) | **[日本語](README.ja.md)** | [Français](README.fr.md) | [한국어](README.ko.md)

# Doc Extract

PDF および EPUB ファイルからテキストを抽出します。スキャン PDF とテキスト PDF を自動判定し、最適な抽出方法を選択します。

## 機能

- **スマート PDF 検出**：スキャン PDF とテキスト PDF を自動判定（最初の 5 ページを確認）
- **ローカル OCR**：スキャン PDF には RapidOCR を使用（API キー不要、30 以上の言語に対応）
- **高速テキスト抽出**：テキスト PDF には PyMuPDF を使用（瞬時に完了）
- **EPUB サポート**：EPUB 電子書籍から章構造を保持したままテキストを抽出
- **強制 OCR モード**：すべての PDF に対して OCR を強制的に有効化可能

## 動作環境

- Python 3.8+

## インストール

```bash
pip install pymupdf rapidocr-onnxruntime ebooklib beautifulsoup4 lxml pillow
```

## 使い方

```bash
# 自動判定して抽出
python doc_extract.py document.pdf
python doc_extract.py document.epub

# 出力ファイルを指定
python doc_extract.py document.pdf --output extracted.txt

# 強制 OCR モード（埋め込みテキストと画像が混在する PDF に便利）
python doc_extract.py document.pdf --force-ocr

# OCR DPI をカスタマイズ（高くするほど品質が向上しますが、処理は遅くなります）
python doc_extract.py scanned.pdf --ocr-dpi 300
python doc_extract.py scanned.pdf --ocr-dpi 600
```

## パラメータ

| パラメータ | デフォルト | 説明 |
|-----------|-----------|------|
| `--output` | {name}_extracted.txt | 出力ファイルパス |
| `--force-ocr` | false | すべての PDF で OCR を強制有効化 |
| `--ocr-dpi` | 300 | OCR の DPI（高くするほど品質向上、処理は低速化） |

## 仕組み

```
入力ファイル
  |-- .pdf -> 最初の 5 ページで埋め込みテキストを確認
  |   |-- < 50 文字 -> スキャン PDF -> RapidOCR で 300 DPI 処理（約 1 秒/ページ）
  |   +-- >= 50 文字 -> テキスト PDF -> PyMuPDF で直接抽出（瞬時に完了）
  +-- .epub -> ebooklib + BeautifulSoup（瞬時に完了）

出力：同じディレクトリに {元のファイル名}_extracted.txt
```

## OCR エンジン

[RapidOCR](https://github.com/RapidAI/RapidOCR)（ONNX Runtime バックエンド）を使用：
- ローカルで動作、無料、API キー不要
- 中国語、英語、日本語、韓国語 + 30 言語に対応
- 300 DPI で通常 1 ページあたり約 1 秒

## 出力形式

```
=== ページ 1 ===
1 ページ目の抽出テキスト...

=== ページ 2 ===
2 ページ目の抽出テキスト...
```

EPUB ファイルの場合：

```
# 書籍タイトル

第 1 章のテキスト...

第 2 章のテキスト...
```

## ライセンス

MIT
