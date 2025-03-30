# Voice Typing Project

## About the project

- Voice-to-text application for keyboard-free typing

## Tech stack

- Docker compose
  - Whisper speech recognition service
- Pyton script
  - Records audio, tiggered using a key combination
  - Sends the audio to the whisper service
  - Types the result out using keyboard emulation

## Coding guidelines

- Follow Domain-Driven Design
- Test Driven Development : write the test before the implmentation
- Test often : test after each modifiction of tests or code
- Separation of Concerns, each component has a single responsibility
- Short functions : if a function is more than 20 lines, refactor to extract small, pure functions
- Functional programming principles, avoid stateful classes and mutations
- Don't add comments or docstrings, use meaningful names instead
- Clean Code principles from Uncle Bob
- Avoid complexity, use simple and robust solutions
- Follow python black formatting style
- Use type hints

## Available Commands

```bash
# Quality check
poetry run pre-commit run --all-files
```
