# Repositories Module

## Responsibility
Encapsulates data persistence and retrieval layers for SQLite canonical database, golden set, and input text files.

## Internal Architecture
- `canonical_repository.py`: Connects to `desafio1_bracis.db`, indexes headers and normative texts, and executes fast lookups.
- `document_repository.py`: Reads and parses `.txt` files from input directories.
- `goldenset_repository.py`: Loads and parses `goldenset.xlsx` / `goldenset.csv`.

## Usage Data Flow
- **Input**: File paths or SQL query parameters.
- **Output**: Domain entities and typed schema collections.
