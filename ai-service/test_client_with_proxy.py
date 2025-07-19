"""Test script for Gemini client with proxy support"""
import os
import sys
import asyncio
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

async def test_proxy_configuration():
    """Test 1: Check proxy configuration"""
    print("\n=== Test 1: Proxy Configuration ===")
    
    # Check environment variables
    http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    
    print(f"HTTP_PROXY: {http_proxy}")
    print(f"HTTPS_PROXY: {https_proxy}")
    
    if http_proxy or https_proxy:
        print("✅ Proxy is configured")
        
        # Test proxy connectivity
        import httpx
        try:
            print("\nTesting proxy connectivity...")
            async with httpx.AsyncClient(proxies={"https://": https_proxy or http_proxy}) as client:
                response = await client.get("https://www.google.com", timeout=10.0)
                print(f"✅ Proxy test successful: {response.status_code}")
        except Exception as e:
            print(f"❌ Proxy test failed: {e}")
    else:
        print("❌ No proxy configured")
    
    return http_proxy or https_proxy

async def test_gemini_direct():
    """Test 2: Direct Gemini API connection"""
    print("\n=== Test 2: Direct Gemini API Test ===")
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found")
            return False
        
        print(f"API Key length: {len(api_key)}")
        print(f"API Key prefix: {api_key[:10]}...")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test listing models
        print("\nListing available models...")
        try:
            models = list(genai.list_models())
            print(f"✅ Found {len(models)} models")
            for i, model in enumerate(models[:3]):
                print(f"   Model {i+1}: {model.name}")
        except Exception as e:
            print(f"❌ Failed to list models: {e}")
            return False
        
        # Test model initialization
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        print(f"\nTesting model: {model_name}")
        try:
            model = genai.GenerativeModel(model_name)
            print(f"✅ Model {model_name} initialized successfully")
            
            # Test simple generation
            print("\nTesting generation...")
            response = model.generate_content("Say 'Hello, I am working!'")
            print(f"✅ Generation successful: {response.text[:50]}...")
            return True
        except Exception as e:
            print(f"❌ Model test failed: {e}")
            
            # Try fallback model
            print("\nTrying fallback model: gemini-1.5-flash")
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content("Say 'Hello, I am working!'")
                print(f"✅ Fallback model works: {response.text[:50]}...")
                return True
            except Exception as e2:
                print(f"❌ Fallback also failed: {e2}")
                return False
                
    except ImportError as e:
        print(f"❌ Failed to import google.generativeai: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_gemini_client():
    """Test 3: Test the actual GeminiClient"""
    print("\n=== Test 3: GeminiClient Test ===")
    
    try:
        from app.gemini.client_with_proxy import GeminiClient
        from app.models import ChatMessage, MessageRole
        
        print("Creating GeminiClient instance...")
        client = GeminiClient()
        
        if client.use_fallback:
            print("⚠️  Client is using fallback mode")
        else:
            print("✅ Client initialized with Gemini")
        
        # Test chat
        print("\nTesting chat functionality...")
        messages = [
            ChatMessage(role=MessageRole.USER, content="你好，请回复'我正在工作'")
        ]
        
        response, tool_calls = await client.chat(messages)
        print(f"Response: {response[:100]}...")
        print(f"Tool calls: {len(tool_calls)}")
        
        return True
        
    except Exception as e:
        print(f"❌ GeminiClient test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_mcp_connection():
    """Test 4: Test MCP connection"""
    print("\n=== Test 4: MCP Connection Test ===")
    
    try:
        from app.mcp.client import MCPClient
        
        print("Creating MCP client...")
        mcp = MCPClient()
        
        print(f"MCP URL: {mcp.base_url}")
        print(f"MCP Token: {mcp.auth_token[:20]}...")
        
        # Test tools endpoint
        print("\nTesting MCP tools endpoint...")
        tools = await mcp.get_available_tools()
        
        if tools:
            print(f"✅ Found {len(tools)} tools")
            for tool in tools[:3]:
                print(f"   - {tool['name']}: {tool['description'][:50]}...")
        else:
            print("❌ No tools found or connection failed")
            
        return True
        
    except Exception as e:
        print(f"❌ MCP test failed: {e}")
        return False

async def test_fallback_client():
    """Test 5: Test fallback client"""
    print("\n=== Test 5: Fallback Client Test ===")
    
    try:
        from app.gemini.fallback_client import FallbackChatClient
        from app.models import ChatMessage, MessageRole
        
        print("Creating FallbackChatClient...")
        client = FallbackChatClient()
        
        # Test basic greeting
        messages = [
            ChatMessage(role=MessageRole.USER, content="你好")
        ]
        response, _ = await client.chat(messages)
        print(f"Greeting response: {response}")
        
        # Test command recognition
        messages = [
            ChatMessage(role=MessageRole.USER, content="起飞到10米")
        ]
        response, tool_calls = await client.chat(messages)
        print(f"Command response: {response}")
        print(f"Tool calls: {tool_calls}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("=== Gemini Client Diagnostic Tests ===")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.executable}")
    
    # Run tests
    proxy = await test_proxy_configuration()
    gemini_ok = await test_gemini_direct()
    
    # If Gemini direct test fails with proxy, suggest solutions
    if not gemini_ok and proxy:
        print("\n⚠️  Gemini API failed with proxy configured.")
        print("Possible solutions:")
        print("1. The proxy might not support Google APIs")
        print("2. Try using a different proxy or VPN")
        print("3. Check if Cherry Studio uses a special proxy configuration")
    
    await test_gemini_client()
    await test_mcp_connection()
    await test_fallback_client()
    
    print("\n=== Test Summary ===")
    print("Check the results above to identify the issue.")
    print("\nRecommendations:")
    if not gemini_ok:
        print("- Gemini API is not accessible. Check proxy settings or use fallback mode.")
    print("- For MCP 401 error, ensure the main backend service is running on port 8000")
    print("- The fallback client should work as a backup option")

if __name__ == "__main__":
    asyncio.run(main()) 