# Services Module

## Responsibility
Executes business logic for citation extraction, text normalization, canonical resolution, end-to-end pipeline execution, and performance evaluation.

## Internal Architecture
- `extraction_service.py`: Finds candidate citation spans and filters non-citation distractors.
- `normalization_service.py`: Standardizes noisy strings, fixes OCR artifacts, and formats identifiers.
- `resolution_service.py`: Matches extracted citations against canonical repository records.
- `pipeline_service.py`: Coordinates the full document analysis lifecycle.
- `evaluation_service.py`: Measures IoU, classification precision/recall/F1, and resolution accuracy.

## Usage Data Flow
- **Input**: Raw document texts and configuration parameters.
- **Output**: Structured predictions and evaluation benchmarks.
