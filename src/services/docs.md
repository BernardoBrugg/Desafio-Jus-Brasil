# Services Module

## Responsibility
Executes business logic for citation span extraction, OCR text normalization, canonical resolution, end-to-end pipeline execution, and performance evaluation.

## Internal Architecture
- `extraction_service.py`: Orchestrates span extraction over raw text using regular expression catalogs and filters out distractor phrases.
- `extraction_patterns.py`: Defines modular regular expressions for jurisprudential citations (including chained appeals, ordinals, court prefixes, and state suffixes) and legislative citations.
- `distractor_filter.py`: Detects header distractors, metadata, and procedural narrative text to eliminate false positives.
- `normalization_service.py`: Standardizes noisy OCR strings (digit replacements, court/sumula typos) and extracts pure numeric sequences.
- `normative_matcher.py`: Resolves súmulas and statutory provisions to their canonical database IDs.
- `resolution_service.py`: Resolves spans into classifications (REAL, INVENTADA, INCOMPLETA) and matches real citations to canonical IDs using tribunal and appeal-type disambiguation.
- `pipeline_service.py`: Coordinates the full document processing lifecycle and persists output JSON files.
- `evaluation_service.py`: Computes IoU matching, precision, recall, F1, and classification/resolution accuracy against the golden set.

## Usage Data Flow
- **Input**: Document input models containing raw procedural texts.
- **Output**: Validated `DocumentOutput` instances containing classified and resolved citations.
