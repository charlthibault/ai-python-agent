# AI Coding Agent with Google Gemini

An autonomous AI coding agent powered by Google's Gemini 2.5 Pro that performs coding tasks through natural language instructions. The agent can read, write, and execute code within a secure sandbox environment.

## Features

- **Autonomous Operation**: Independently plans and executes multi-step tasks
- **File Management**: Read, write, and list files
- **Code Execution**: Run Python scripts and shell commands
- **Security Sandboxing**: All operations restricted to working directory
- **Function Calling**: Native integration with Gemini's function calling API

## Quick Start

### Prerequisites

- Python 3.11+
- [Google Gemini API Key](https://aistudio.google.com/apikey)
- [UV package manager](https://docs.astral.sh/uv/getting-started/installation/)

### Installation

```bash
# Create virtual environment and install dependencies
uv sync

# Install with dev dependencies (includes Ruff)
uv sync --extra dev

# Set API key
export GEMINI_API_KEY="your-api-key-here"
```

### Usage

```bash
# Basic usage
uv run main.py "Your instruction here"

# Verbose mode
uv run main.py "Your instruction" --verbose
```

### Example Commands

```bash
# Analyze code
uv run main.py "Read the calculator code and explain what it does"

# Add features
uv run main.py "Add a square root function to the calculator"

# Run tests
uv run main.py "Run the test suite and report the results"

# Refactor code
uv run main.py "Add type hints to all functions"
```

## Available Functions

The agent has access to 5 tools:

1. **`get_files_info(path)`** - List directory contents
2. **`get_file_content(file_path)`** - Read file contents (max 10K chars)
3. **`write_file(file_path, content)`** - Create or overwrite files
4. **`run_python_file(file_path, args)`** - Execute Python scripts
5. **`run_command_in_terminal(command)`** - Run shell commands

## Project Structure

```
ai-agent-python/
├── main.py                 # Agent entry point
├── config.py               # Configuration
├── prompts.py              # System prompt
├── call_function.py        # Function router
├── functions/              # Tool implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   ├── run_python_file.py
│   └── run_command_in_terminal.py
├── tests/                  # Unit tests
└── calculator/             # Sandbox (working directory)
```

## Security

All operations are sandboxed to the `calculator/` directory with:
- Path traversal prevention
- 10K character file read limit
- 30-second command timeout
- 100 iteration maximum per request

## Development

### Linting and Formatting

The project uses [Ruff](https://docs.astral.sh/ruff/) for fast linting and formatting.

```bash
# Check code style and lint issues
make check

# Auto-fix linting issues
make lint

# Format code
make format

# Run all (lint + format)
make lint && make format
```

### Testing

```bash
# Test agent functions
make test

# Or use pytest directly
uv run pytest tests/ -v

# Test calculator project
cd calculator && make test
```

## Configuration

Edit `config.py` to customize:
```python
MAX_FILE_SIZE = 10000      # Max chars to read
WORKING_DIR = "calculator"  # Sandbox directory
```

## Troubleshooting

**API Key Error**: Ensure `GEMINI_API_KEY` is set in `.env` or environment

**Permission Error**: Run `chmod -R u+w calculator/`

**Import Error**: Reinstall with `uv sync`

## Development Workflow

```bash
# 1. Install dependencies
uv sync --extra dev

# 2. Make changes to code

# 3. Check and format code
make check      # Check for issues
make format     # Format code
make lint       # Fix linting issues

# 4. Run tests
make test

# 5. Test with the agent
uv run main.py "Your test prompt"
```

## Tips

- Be specific with instructions
- Use `--verbose` to see agent reasoning
- Let the agent explore the codebase first
- Break complex tasks into smaller steps

---

## Credits

This project was built following [Build an AI Agent with Python](https://www.boot.dev/courses/build-ai-agent-python) course from Boot.dev.

**Educational project demonstrating AI agent development with Google Gemini**
