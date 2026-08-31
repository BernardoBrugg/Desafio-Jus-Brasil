# Guidelines and Architecture for Autonomous Agents

## 1. Core Principles
- Expressive Code: Code must be completely self-explanatory without in-code comments.
- Zero Tolerance for Comments: Never include inline, block, or docstring comments in source code.
- File Size Limitation: No source file may exceed 200 lines of code. Split files into cohesive, smaller units.
- Service Layer Pattern: Strict separation of concerns across schemas, repositories, services, and CLI entry points.
- Directory Documentation: Every directory must maintain an up-to-date docs.md file detailing responsibility, internal architecture, and data flow.
- Security and Configuration: Environment variables must be loaded through centralized settings via pydantic-settings.

## 2. Directory Architecture
- src/core: Centralized configuration, environment variables, and custom exception definitions.
- src/schemas: Pydantic schemas defining contracts for citations, documents, resolutions, and evaluation metrics.
- src/repositories: Data access layer handling SQLite database queries, memory caches, and file loaders.
- src/services: Pure business logic organized into discrete, testable services (extraction, normalization, resolution, evaluation).
- src/cli: Command line interfaces and application entry points.

## 3. Data Flow
1. Input documents (.txt) are ingested by DocumentRepository.
2. ExtractionService identifies citation spans, texts, and types, filtering distractor tokens.
3. NormalizationService cleans and standardizes noisy citations (OCR artifacts, abbreviations, CNJ patterns).
4. ResolutionService matches normalized queries against CanonicalRepository.
5. PipelineService coordinates extraction, normalization, and resolution to produce output JSON files.
6. EvaluationService computes metrics (IoU matching, classification F1, canonical ID accuracy) against the golden set.
