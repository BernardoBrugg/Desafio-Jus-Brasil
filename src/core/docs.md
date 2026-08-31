# Core Module

## Responsibility
Manages application configuration, environment settings, and custom domain exceptions.

## Internal Architecture
- `config.py`: Environment variable schema and loader using pydantic-settings.
- `exceptions.py`: Custom application exceptions.

## Usage Data Flow
- **Input**: Environment variables from `.env` or system environment.
- **Output**: Typed `Settings` instance accessible throughout the application.
