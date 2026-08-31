# Schemas Module

## Responsibility
Defines standard Pydantic models for data interchange, input/output contracts, and validation.

## Internal Architecture
- `enums.py`: Enumerations for citation types, classes, and document natures.
- `citation.py`: Models for extracted citations, canonical resolutions, and predictions.
- `document.py`: Models for raw input text files and canonical repository records.
- `evaluation.py`: Models for golden set items and metric evaluation scores.

## Usage Data Flow
- **Input**: Raw text dictionaries, database rows, or parsed JSON payloads.
- **Output**: Strongly typed and validated Pydantic objects.
