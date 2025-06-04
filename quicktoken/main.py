import argparse
import sys
from pathlib import Path
import tiktoken
from typing import List, Tuple


def format_number(num):
    """Format numbers with commas for readability."""
    return f"{num:,}"


def get_file_size(file_path):
    """Get file size in bytes."""
    return file_path.stat().st_size


def format_file_size(size_bytes):
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def count_tokens(text, model="gpt-4o"):
    """Count tokens using tiktoken for the specified model."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text, disallowed_special=()))
    except KeyError:
        # Fallback to cl100k_base encoding if model not found
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text, disallowed_special=()))


def is_text_file(file_path: Path) -> bool:
    """Check if a file is likely a text file."""
    text_extensions = {
        '.txt', '.md', '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss',
        '.json', '.yaml', '.yml', '.xml', '.csv', '.sql', '.sh', '.bash', '.zsh',
        '.fish', '.vim', '.lua', '.r', '.rb', '.go', '.rs', '.cpp', '.c', '.h',
        '.hpp', '.java', '.kt', '.swift', '.php', '.pl', '.ps1', '.bat', '.dockerfile',
        '.gitignore', '.gitattributes', '.env', '.ini', '.cfg', '.conf', '.toml',
        '.lock', '.log', '.rst', '.tex', '.bib', '.makefile', '.cmake'
    }
    
    # Check extension
    if file_path.suffix.lower() in text_extensions:
        return True
    
    # Check common files without extensions
    if file_path.name.lower() in {'readme', 'license', 'changelog', 'makefile', 'dockerfile'}:
        return True
    
    # Try to read a small portion to check if it's text
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if not chunk:
                return True  # Empty files are considered text
            # Check for null bytes (common in binary files)
            if b'\x00' in chunk:
                return False
            # Try to decode as UTF-8
            chunk.decode('utf-8')
            return True
    except (UnicodeDecodeError, PermissionError, OSError):
        return False


def find_text_files(directory: Path) -> List[Path]:
    """Recursively find all text files in a directory."""
    # Directories to exclude
    exclude_dirs = {
        '.git', '.venv', 'venv', '__pycache__', '.pytest_cache',
        'node_modules', '.next', 'dist', 'build', '.cache',
        '.DS_Store', '.idea', '.vscode', 'target'
    }
    
    text_files = []
    for file_path in directory.rglob('*'):
        # Skip if any parent directory is in exclude list
        if any(part in exclude_dirs for part in file_path.parts):
            continue
        
        if file_path.is_file() and is_text_file(file_path):
            text_files.append(file_path)
    return sorted(text_files)


def analyze_file(file_path: Path, model: str) -> Tuple[int, int, int, int]:
    """Analyze a single file and return (tokens, chars, lines, size)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError, OSError):
        return 0, 0, 0, 0
    
    token_count = count_tokens(content, model)
    char_count = len(content)
    line_count = content.count('\n') + (1 if content and not content.endswith('\n') else 0)
    file_size = file_path.stat().st_size
    
    return token_count, char_count, line_count, file_size


def print_file_summary(file_path: Path, tokens: int, relative_to: Path = None):
    """Print a single line summary for a file."""
    display_path = file_path.relative_to(relative_to) if relative_to else file_path
    print(f"  {display_path}: \033[1;32m{format_number(tokens)}\033[0m tokens")


def print_directory_summary(directory: Path, total_tokens: int, total_chars: int, 
                          total_lines: int, total_size: int, file_count: int, model: str):
    """Print the total summary for a directory."""
    tokens_per_char = total_tokens / total_chars if total_chars > 0 else 0
    
    print(f"\n📁 \033[1m{directory.name}/ ({file_count} files)\033[0m")
    print("─" * 50)
    print(f"🔢 Tokens:      \033[1;32m{format_number(total_tokens)}\033[0m")
    print(f"📝 Characters:  \033[36m{format_number(total_chars)}\033[0m")
    print(f"📏 Lines:       \033[36m{format_number(total_lines)}\033[0m")
    print(f"💾 Total size:  \033[36m{format_file_size(total_size)}\033[0m")
    print(f"⚖️  Ratio:       \033[33m{tokens_per_char:.3f} tokens/char\033[0m")
    print(f"🤖 Model:       \033[35m{model}\033[0m")
    print()


def print_single_file_summary(file_path: Path, tokens: int, chars: int, lines: int, 
                             file_size: int, model: str):
    """Print detailed summary for a single file."""
    tokens_per_char = tokens / chars if chars > 0 else 0
    
    print(f"\n📄 \033[1m{file_path.name}\033[0m")
    print("─" * 50)
    print(f"🔢 Tokens:      \033[1;32m{format_number(tokens)}\033[0m")
    print(f"📝 Characters:  \033[36m{format_number(chars)}\033[0m")
    print(f"📏 Lines:       \033[36m{format_number(lines)}\033[0m")
    print(f"💾 File size:   \033[36m{format_file_size(file_size)}\033[0m")
    print(f"⚖️  Ratio:       \033[33m{tokens_per_char:.3f} tokens/char\033[0m")
    print(f"🤖 Model:       \033[35m{model}\033[0m")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Count tokens in files or directories using GPT tokenizers",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="Path to the file or directory to analyze")
    parser.add_argument(
        "--model", 
        default="gpt-4o", 
        help="Tokenizer model to use (default: gpt-4o)"
    )
    
    args = parser.parse_args()
    
    target_path = Path(args.path)
    
    if not target_path.exists():
        print(f"❌ Error: Path '{args.path}' not found")
        sys.exit(1)
    
    # Handle single file
    if target_path.is_file():
        if not is_text_file(target_path):
            print(f"❌ Error: '{args.path}' does not appear to be a text file")
            sys.exit(1)
        
        tokens, chars, lines, file_size = analyze_file(target_path, args.model)
        if tokens == 0 and chars == 0:
            print(f"❌ Error: Cannot read '{args.path}' as UTF-8 text")
            sys.exit(1)
        
        print_single_file_summary(target_path, tokens, chars, lines, file_size, args.model)
        return
    
    # Handle directory
    if not target_path.is_dir():
        print(f"❌ Error: '{args.path}' is not a file or directory")
        sys.exit(1)
    
    # Find all text files
    text_files = find_text_files(target_path)
    
    if not text_files:
        print(f"❌ No text files found in '{args.path}'")
        sys.exit(1)
    
    # Analyze all files
    total_tokens = 0
    total_chars = 0
    total_lines = 0
    total_size = 0
    analyzed_files = []
    
    print(f"\n📁 Analyzing {len(text_files)} files in \033[1m{target_path.name}/\033[0m\n")
    
    for file_path in text_files:
        tokens, chars, lines, file_size = analyze_file(file_path, args.model)
        if tokens > 0 or chars > 0:  # Only include files that were successfully read
            total_tokens += tokens
            total_chars += chars
            total_lines += lines
            total_size += file_size
            analyzed_files.append((file_path, tokens))
            print_file_summary(file_path, tokens, target_path)
    
    if not analyzed_files:
        print(f"❌ No readable text files found in '{args.path}'")
        sys.exit(1)
    
    # Print total summary
    print_directory_summary(target_path, total_tokens, total_chars, total_lines, 
                          total_size, len(analyzed_files), args.model)


if __name__ == "__main__":
    main()
