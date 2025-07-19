"""Test environment variable loading timing"""
import os
import sys
from dotenv import load_dotenv

print("=== Environment Variable Timing Test ===")
print(f"PID: {os.getpid()}")

# Check initial state
print("\n1. Initial environment state:")
print(f"   HTTP_PROXY: {os.getenv('HTTP_PROXY', 'NOT SET')}")
print(f"   GEMINI_API_KEY exists: {bool(os.getenv('GEMINI_API_KEY'))}")

# Load .env
print("\n2. Loading .env file...")
load_dotenv()

# Check after loading
print("\n3. After loading .env:")
print(f"   HTTP_PROXY: {os.getenv('HTTP_PROXY', 'NOT SET')}")
print(f"   GEMINI_API_KEY exists: {bool(os.getenv('GEMINI_API_KEY'))}")

# Test with subprocess (simulating uvicorn)
print("\n4. Testing in subprocess (like uvicorn)...")
import subprocess
code = """
import os
print(f"   Subprocess PID: {os.getpid()}")
print(f"   HTTP_PROXY in subprocess: {os.getenv('HTTP_PROXY', 'NOT SET')}")
"""
subprocess.run([sys.executable, "-c", code])

# Test import timing
print("\n5. Testing module import timing...")
print("   Before import: proxy is", os.getenv('HTTP_PROXY', 'NOT SET'))

# Set a test variable
os.environ['TEST_IMPORT_TIME'] = 'BEFORE_IMPORT'

# Import a test module
code2 = """
import os
print(f"   During import: TEST_IMPORT_TIME = {os.getenv('TEST_IMPORT_TIME', 'NOT SET')}")
print(f"   During import: HTTP_PROXY = {os.getenv('HTTP_PROXY', 'NOT SET')}")
"""
with open('test_import_module.py', 'w') as f:
    f.write(code2)

import test_import_module

# Clean up
os.remove('test_import_module.py')

print("\n=== Diagnosis ===")
print("If proxy is NOT SET in subprocess, that explains the uvicorn issue.")
print("Solution: Ensure environment variables are set before starting uvicorn.") 