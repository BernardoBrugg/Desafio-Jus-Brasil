# Repositories Module

## Responsibility
Encapsulates data persistence and retrieval layers for SQLite canonical database, golden set records, and input document text files.

## Internal Architecture
- `canonical_indexer.py`: Utility functions for extracting digits, CNJ standard sequences, and candidate process numbers.
- `canonical_repository.py`: Connects to `desafio1_bracis.db`, performs hierarchical indexing (header-priority CNJ mapping, full-text CNJ mapping, and deduplicated process numbers), and executes fast indexed lookups with tribunal and appeal-type disambiguation.
- `document_repository.py`: Loads and parses `.txt` files from input directories into `DocumentInput` schema objects.
- `goldenset_repository.py`: Loads and parses official benchmark evaluation items from XLSX spreadsheets.

## Usage Data Flow
- **Input**: Database file paths, directory paths, or lookup keys (CNJ digits, process numbers, tribunal hints).
- **Output**: Typed schema models and canonical record matches.
