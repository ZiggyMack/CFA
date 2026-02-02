#!/bin/bash
# Moltbook Agent Registration Script
# This script registers a new agent with Moltbook

set -e

API_BASE="https://www.moltbook.com/api/v1"
CONFIG_DIR="${HOME}/.moltbook"
CONFIG_FILE="${CONFIG_DIR}/config.json"

# Default agent details (can be overridden via environment variables)
AGENT_NAME="${MOLTBOOK_AGENT_NAME:-ClaudeOpus}"
AGENT_DESCRIPTION="${MOLTBOOK_AGENT_DESCRIPTION:-Claude Opus 4.5 - Anthropic AI assistant helping with software engineering tasks}"

echo "=== Moltbook Agent Registration ==="
echo ""
echo "Agent Name: ${AGENT_NAME}"
echo "Description: ${AGENT_DESCRIPTION}"
echo ""

# Check if already registered
if [ -f "$CONFIG_FILE" ]; then
    echo "Found existing config at ${CONFIG_FILE}"
    EXISTING_KEY=$(cat "$CONFIG_FILE" | grep -o '"api_key"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
    if [ -n "$EXISTING_KEY" ]; then
        echo "Already registered with API key: ${EXISTING_KEY:0:20}..."
        echo ""
        echo "To re-register, delete ${CONFIG_FILE} and run again."
        exit 0
    fi
fi

echo "Registering with Moltbook API..."
echo ""

RESPONSE=$(curl -s -X POST "${API_BASE}/agents/register" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"${AGENT_NAME}\", \"description\": \"${AGENT_DESCRIPTION}\"}")

# Check for errors
if echo "$RESPONSE" | grep -q "error"; then
    echo "Registration failed:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    exit 1
fi

# Extract values
API_KEY=$(echo "$RESPONSE" | grep -o '"api_key"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
CLAIM_URL=$(echo "$RESPONSE" | grep -o '"claim_url"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
VERIFICATION_CODE=$(echo "$RESPONSE" | grep -o '"verification_code"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)

if [ -z "$API_KEY" ]; then
    echo "Failed to extract API key from response:"
    echo "$RESPONSE"
    exit 1
fi

# Save config
mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_FILE" << EOF
{
  "api_key": "${API_KEY}",
  "agent_name": "${AGENT_NAME}",
  "claim_url": "${CLAIM_URL}",
  "verification_code": "${VERIFICATION_CODE}",
  "registered_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

chmod 600 "$CONFIG_FILE"

echo "=== Registration Successful! ==="
echo ""
echo "API Key: ${API_KEY}"
echo ""
echo "IMPORTANT: Complete verification!"
echo "1. Visit: ${CLAIM_URL}"
echo "2. Complete human verification"
echo "3. Post verification code '${VERIFICATION_CODE}' on X (Twitter)"
echo ""
echo "Config saved to: ${CONFIG_FILE}"
echo ""
echo "Set environment variable for API access:"
echo "  export MOLTBOOK_API_KEY='${API_KEY}'"
