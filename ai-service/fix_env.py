"""Quick fix for environment configuration"""
import os
from pathlib import Path

env_file = Path(".env")

# Check if .env exists
if not env_file.exists():
    print("❌ .env file not found!")
    print("Creating from template...")
    
    template = Path("env_template.txt")
    if template.exists():
        env_file.write_text(template.read_text())
        print("✅ Created .env from template")
    else:
        print("❌ Template not found either!")
        exit(1)

# Read current .env
content = env_file.read_text()

# Fix MCP token if needed
if "your-secure-internal-token-here" in content:
    print("🔧 Fixing MCP_AUTH_TOKEN...")
    content = content.replace(
        "MCP_AUTH_TOKEN=your-secure-internal-token-here",
        "MCP_AUTH_TOKEN=default-dev-token"
    )
    env_file.write_text(content)
    print("✅ Fixed MCP_AUTH_TOKEN")
elif "MCP_AUTH_TOKEN=default-dev-token" in content:
    print("✅ MCP_AUTH_TOKEN is already correct")
else:
    print("⚠️  MCP_AUTH_TOKEN not found in .env")
    print("Adding it...")
    content += "\n# MCP Auth Token\nMCP_AUTH_TOKEN=default-dev-token\n"
    env_file.write_text(content)
    print("✅ Added MCP_AUTH_TOKEN")

# Check proxy settings
if "HTTP_PROXY" not in content:
    print("\n⚠️  No proxy settings found in .env")
    print("You may want to add:")
    print("HTTP_PROXY=http://127.0.0.1:7897")
    print("HTTPS_PROXY=http://127.0.0.1:7897")
else:
    print("\n✅ Proxy settings found")

# Check API key
if "GEMINI_API_KEY" not in content or "your-gemini-api-key-here" in content:
    print("\n⚠️  Please update GEMINI_API_KEY in .env file")
else:
    print("\n✅ GEMINI_API_KEY is set")

print("\n=== Configuration Summary ===")
print("1. MCP_AUTH_TOKEN: fixed to 'default-dev-token'")
print("2. Proxy: HTTP_PROXY and HTTPS_PROXY should be set to your proxy")
print("3. API Key: Make sure GEMINI_API_KEY is your actual key")
print("\nRestart the AI service for changes to take effect!") 