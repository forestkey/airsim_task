"""Test connections to various services"""
import os
import sys
import httpx
import asyncio
from dotenv import load_dotenv

# Add the app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

async def test_connections():
    """Test connections to various services"""
    
    # Test 1: Check if main backend is running
    print("1. Testing main backend connection...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            print(f"   Main backend health check: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Failed to connect to main backend: {e}")
    
    # Test 2: Check MCP endpoint with auth
    print("\n2. Testing MCP endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": "Bearer default-dev-token",
                "Content-Type": "application/json"
            }
            response = await client.get("http://localhost:8000/api/v1/mcp/tools", headers=headers)
            print(f"   MCP tools endpoint: {response.status_code}")
            if response.status_code == 200:
                print(f"   Available tools: {len(response.json())} tools")
    except Exception as e:
        print(f"   ❌ Failed to connect to MCP endpoint: {e}")
    
    # Test 3: Test Google connectivity (simplified)
    print("\n3. Testing Google API connectivity...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://www.google.com")
            print(f"   Google connectivity: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Failed to connect to Google: {e}")
    
    # Test 4: Check environment variables
    print("\n4. Checking environment variables...")
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"   ✅ GEMINI_API_KEY is set (length: {len(api_key)})")
        print(f"   First 10 chars: {api_key[:10]}...")
    else:
        print(f"   ❌ GEMINI_API_KEY is not set")
    
    # Test 5: Check proxy settings
    print("\n5. Checking proxy settings...")
    http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    if http_proxy:
        print(f"   HTTP_PROXY: {http_proxy}")
    if https_proxy:
        print(f"   HTTPS_PROXY: {https_proxy}")
    if not http_proxy and not https_proxy:
        print("   No proxy configured")
    
    # Test 6: Try Gemini API directly
    print("\n6. Testing Gemini API directly...")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Try to list models
            models = genai.list_models()
            model_count = 0
            for model in models:
                model_count += 1
                if model_count <= 3:  # Show first 3 models
                    print(f"   Model: {model.name}")
            print(f"   ✅ Successfully connected to Gemini API ({model_count} models available)")
        except Exception as e:
            print(f"   ❌ Failed to connect to Gemini API: {e}")
            print(f"   Error type: {type(e).__name__}")

if __name__ == "__main__":
    print("=== Service Connection Test ===\n")
    asyncio.run(test_connections())
    print("\n=== Test Complete ===") 