# Scripts Module

## Responsibility
Contains utility scripts for submission conversion, output packaging, and data preparation.

## Internal Architecture
- `json_to_submission.py`: Aggregates individual document JSON outputs into a single consolidated `submission.csv`.
- `package_submission.py`: Validates JSON schema adherence and packages outputs into a leaderboard-ready `submission.zip`.

## Usage Data Flow
- **Input**: Directory containing output `.json` files.
- **Output**: `submission.csv` and `submission.zip`.
