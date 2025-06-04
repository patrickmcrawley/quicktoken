# QuickToken

A fast, beautiful CLI tool to count tokens in files using GPT tokenizers.

## Installation

```bash
# Clone the repository
git clone https://github.com/patrickmcrawley/quicktoken.git
cd quicktoken

# Install with uv (recommended)
uv sync
uv pip install -e .
```

## Usage

```bash
# Count tokens in a file
quicktoken my-file.md

# Use a different model tokenizer
quicktoken --model gpt-3.5-turbo my-file.txt

# Get help
quicktoken --help
```

## Example Output

```
📄 example.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔢 Tokens:      1,234
📝 Characters:  5,678
📏 Lines:       42
💾 File size:   5.5 KB
⚡ Ratio:       0.217 tokens/char
🤖 Model:       gpt-4o
```

## Features

- ⚡ Fast token counting using tiktoken
- 🎨 Beautiful, colorized output
- 📊 Comprehensive file statistics
- 🤖 Support for different model tokenizers
- 💻 Works on macOS and Linux
- 📄 Handles any UTF-8 text file

## Supported Models

- `gpt-4o` (default)
- `gpt-4`
- `gpt-3.5-turbo`
- And any other model supported by tiktoken

## Requirements

- Python 3.12+
- tiktoken

## Development

This project uses `uv` for dependency management:

```bash
# Install dependencies
uv sync

# Run the CLI locally
uv run python -m quicktoken.main <file>
```
