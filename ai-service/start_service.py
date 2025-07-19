"""Start AI service with proper environment setup"""
import os
import sys
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

print("=== Starting AI Service ===")

# 1. Load environment variables FIRST
logger.info("Loading environment variables from .env...")
load_dotenv(override=True)  # override=True ensures .env values take precedence

# 2. Verify critical environment variables
env_vars = {
    'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
    'HTTP_PROXY': os.getenv('HTTP_PROXY'),
    'HTTPS_PROXY': os.getenv('HTTPS_PROXY'),
    'MCP_AUTH_TOKEN': os.getenv('MCP_AUTH_TOKEN'),
}

logger.info("Environment variables loaded:")
for key, value in env_vars.items():
    if value:
        if key == 'GEMINI_API_KEY':
            logger.info(f"  {key}: ***{value[-4:]}")
        else:
            logger.info(f"  {key}: {value}")
    else:
        logger.warning(f"  {key}: NOT SET")

# 3. Ensure proxy is in environment
if env_vars['HTTP_PROXY']:
    os.environ['http_proxy'] = env_vars['HTTP_PROXY']
    os.environ['HTTP_PROXY'] = env_vars['HTTP_PROXY']
if env_vars['HTTPS_PROXY']:
    os.environ['https_proxy'] = env_vars['HTTPS_PROXY']
    os.environ['HTTPS_PROXY'] = env_vars['HTTPS_PROXY']

# 4. Start uvicorn programmatically
logger.info("\nStarting uvicorn server...")
import uvicorn

if __name__ == "__main__":
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Service error: {e}")
        sys.exit(1) 