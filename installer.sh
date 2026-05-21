#!/bin/sh
set -e

# 1. Install uv if missing
if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# 2. Install genie
echo "Installing genie..."
uv tool install git+https://github.com/doragiannul-del/genie.git

# 3. Check .env for existing config
ENV_FILE=".env"
if [ -f "$ENV_FILE" ] && grep -q "API_KEY" "$ENV_FILE" && grep -q "API_BASE_URL" "$ENV_FILE" && grep -q "AI_MODEL" "$ENV_FILE"; then
    echo "Found existing config in .env — skipping setup."
    echo "genie is ready!"
    exit 0
fi

# 4. Prompt user and write ~/.genie/config.toml
echo ""
echo "Let's set up your config."
printf "API key: "
read -r api_key
printf "Base URL (e.g. https://openrouter.ai/api/v1): "
read -r base_url
printf "Model (e.g. deepseek/deepseek-v4-flash:free): "
read -r model

mkdir -p "$HOME/.genie"
cat > "$HOME/.genie/config.toml" <<EOF
[genie]
api_key = "$api_key"
base_url = "$base_url"
ai_model = "$model"
EOF

echo ""
echo "genie is ready! Try: genie list all files modified in the last 3 days"
