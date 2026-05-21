# genie

Turn plain English into shell commands.

## Install

```sh
curl -sSL https://raw.githubusercontent.com/doragiannul-del/genie/main/installer.sh | sh
```

## Usage

```sh
genie find all PDFs modified in the last 7 days
# find . -name "*.pdf" -mtime -7

# Breakdown:
# find .        → search from current directory
# -name "*.pdf" → match PDF files
# -mtime -7     → modified in the last 7 days
```

```sh
genie compress all images in this folder to under 500kb
# convert *.jpg -quality 60 -define jpeg:extent=500kb ./compressed/

# Breakdown:
# convert *.jpg               → process all JPG files
# -quality 60                 → reduce quality to ~60%
# -define jpeg:extent=500kb   → set max file size target
# ./compressed/               → save output to compressed/ folder
```

## Configuration

**Option 1 — environment variables** (via shell or `.env` file):

```sh
API_KEY=...
API_BASE_URL=...
AI_MODEL=...
```

**Option 2 — config file** at `~/.genie/config.toml`:

```toml
[genie]
api_key = "..."
base_url = "..."
ai_model = "..."
```

Use `--linux` to generate Linux commands instead of macOS ones.
