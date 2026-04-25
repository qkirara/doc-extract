[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | **[Français](README.fr.md)** | [한국어](README.ko.md)

# Doc Extract

Extrayez le texte des fichiers PDF et EPUB. Détecte automatiquement les PDF numérisés par rapport aux PDF textuels et utilise la méthode d'extraction optimale.

## Fonctionnalités

- **Détection intelligente des PDF** : détecte automatiquement les PDF numérisés par rapport aux PDF basés sur du texte (vérifie les 5 premières pages)
- **OCR local** : RapidOCR pour les PDF numérisés (aucune clé API nécessaire, prend en charge plus de 30 langues)
- **Extraction de texte rapide** : PyMuPDF pour les PDF textuels (instantané)
- **Prise en charge EPUB** : extrait le texte des livres EPUB en conservant la structure des chapitres
- **Mode OCR forcé** : optionnellement forcer l'OCR pour tous les PDF

## Configuration requise

- Python 3.8+

## Installation

```bash
pip install pymupdf rapidocr-onnxruntime ebooklib beautifulsoup4 lxml pillow
```

## Utilisation

```bash
# Détection automatique et extraction
python doc_extract.py document.pdf
python doc_extract.py document.epub

# Spécifier le fichier de sortie
python doc_extract.py document.pdf --output extracted.txt

# Mode OCR forcé (utile pour les PDF contenant du texte intégré et des images)
python doc_extract.py document.pdf --force-ocr

# DPI OCR personnalisé (plus élevé = meilleure qualité mais plus lent)
python doc_extract.py scanned.pdf --ocr-dpi 300
python doc_extract.py scanned.pdf --ocr-dpi 600
```

## Paramètres

| Paramètre | Par défaut | Description |
|-----------|-----------|-------------|
| `--output` | {name}_extracted.txt | Chemin du fichier de sortie |
| `--force-ocr` | false | Forcer l'OCR pour tous les PDF |
| `--ocr-dpi` | 300 | DPI de l'OCR (plus élevé = meilleure qualité mais plus lent) |

## Fonctionnement

```
Fichier d'entrée
  |-- .pdf -> vérifie les 5 premières pages pour du texte intégré
  |   |-- < 50 caractères -> numérisé -> RapidOCR à 300 DPI (~1s/page)
  |   +-- >= 50 caractères -> basé sur du texte -> extraction directe avec PyMuPDF (instantané)
  +-- .epub -> ebooklib + BeautifulSoup (instantané)

Sortie : {nom_original}_extracted.txt dans le même répertoire
```

## Moteur OCR

Utilise [RapidOCR](https://github.com/RapidAI/RapidOCR) (backend ONNX Runtime) :
- Local, gratuit, aucune clé API nécessaire
- Prend en charge le chinois, l'anglais, le japonais, le coréen + 30 langues
- Environ 1 seconde par page à 300 DPI

## Format de sortie

```
=== Page 1 ===
Texte extrait de la page 1...

=== Page 2 ===
Texte extrait de la page 2...
```

Pour les fichiers EPUB :

```
# Titre du livre

Texte du chapitre 1...

Texte du chapitre 2...
```

## Licence

MIT
