# Tests Module

## Responsibility
Provides unit and integration tests to verify schemas, normalizers, canonical matchers, and pipeline services.

## Internal Architecture
- `test_schemas.py`: Tests schema serialization and validation constraints.
- `test_normalization.py`: Tests OCR noise removal, digit extraction, and text formatting.
- `test_normative_matcher.py`: Tests deterministic resolution for súmulas and statutory provisions.
- `test_resolution.py`: Tests resolution logic against synthetic test cases.

## Usage Data Flow
- **Input**: Test assertions and fixtures.
- **Output**: Unit test pass/fail results.
