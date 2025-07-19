"""Simple proxy test for Gemini API"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== Simple Proxy Test ===")
print(f"HTTP_PROXY: {os.getenv('HTTP_PROXY')}")
print(f"HTTPS_PROXY: {os.getenv('HTTPS_PROXY')}")
print(f"API Key exists: {bool(os.getenv('GEMINI_API_KEY'))}")

# Test 1: Basic connectivity
print("\n1. Testing basic connectivity...")
try:
    import httpx
    import asyncio
    
    async def test_google():
        proxy = os.getenv('HTTPS_PROXY') or os.getenv('HTTP_PROXY')
        if proxy:
            print(f"Using proxy: {proxy}")
            async with httpx.AsyncClient(proxies=proxy) as client:
                r = await client.get("https://www.google.com", timeout=10.0)
                print(f"✅ Google.com: {r.status_code}")
        else:
            print("❌ No proxy configured")
    
    asyncio.run(test_google())
except Exception as e:
    print(f"❌ Connection test failed: {e}")

# Test 2: Gemini API
print("\n2. Testing Gemini API...")
try:
    import google.generativeai as genai
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No API key found")
    else:
        genai.configure(api_key=api_key)
        
        # Try to list models
        print("Listing models...")
        for model in genai.list_models():
            if 'gemini' in model.name:
                print(f"  - {model.name}")
                
        # Try to use gemini-2.5-flash
        print("\nTesting gemini-2.5-flash...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content('Say "Hello World"')
        print(f"✅ Response: {response.text}")
        
except Exception as e:
    print(f"❌ Gemini test failed: {e}")
    print("\nTrying with different proxy settings...")
    
    # Try common proxy ports
    for port in [7890, 7897, 1080, 10809]:
        try:
            print(f"\nTrying port {port}...")
            os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{port}'
            os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{port}'
            
            # Quick test
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-flash')  # Try older model
            response = model.generate_content('Hi')
            print(f"✅ Port {port} works!")
            break
        except:
            print(f"❌ Port {port} failed")

print("\n=== Test Complete ===")
print("\nIf all tests failed, please:")
print("1. Check your proxy software is running")
print("2. Find the correct proxy port in your proxy software settings")
print("3. Update HTTP_PROXY and HTTPS_PROXY in .env file") 