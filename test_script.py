#!/usr/bin/env python3
"""
Test script for LocalAIHub API
"""

import requests
import json
import time

API_URL = "http://localhost:5000"

def test_health():
    """Check if the server is up and running."""
    print("🔍 Checking server health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"✅ Server is healthy: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_status():
    """Check the server's status and system info."""
    print("🔍 Checking server status...")
    try:
        response = requests.get(f"{API_URL}/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ Server status:")
            print(f"   - Running for: {status.get('uptime_seconds', 0):.1f} seconds")
            print(f"   - Memory used: {status.get('memory_usage_percent', 0):.1f}%")
            print(f"   - Ollama: {'Running' if status.get('ollama_available') else 'Not running'}")
            return True
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status check failed: {e}")
        return False

def test_generate():
    """Test sending questions to the AI."""
    print("🔍 Testing AI responses...")
    
    test_questions = [
        "Hi, who are you?",
        "What is 2 + 2?",
        "Tell me a joke",
    ]
    
    success_count = 0
    
    for question in test_questions:
        try:
            print(f"   📝 Asking: '{question}'")
            
            start_time = time.time()
            response = requests.post(
                f"{API_URL}/generate",
                json={"prompt": question},
                timeout=30
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Got answer ({duration:.2f}s): {result.get('response', '')[:100]}...")
                print(f"      Model used: {result.get('model', 'unknown')}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"📊 AI response tests: {success_count}/{len(test_questions)} passed")
    return success_count == len(test_questions)

def test_error_handling():
    """Test how the server handles bad inputs."""
    print("🔍 Testing error handling...")
    
    # Test empty question
    try:
        response = requests.post(f"{API_URL}/generate", json={"prompt": ""}, timeout=5)
        if response.status_code == 400:
            print("✅ Empty question caught correctly")
        else:
            print(f"❌ Empty question not caught: {response.status_code}")
    except Exception as e:
        print(f"❌ Empty question test failed: {e}")
    
    # Test missing question
    try:
        response = requests.post(f"{API_URL}/generate", json={}, timeout=5)
        if response.status_code == 400:
            print("✅ Missing question caught correctly")
        else:
            print(f"❌ Missing question not caught: {response.status_code}")
    except Exception as e:
        print(f"❌ Missing question test failed: {e}")
    
    # Test wrong endpoint
    try:
        response = requests.get(f"{API_URL}/invalid", timeout=5)
        if response.status_code == 404:
            print("✅ Wrong endpoint caught correctly")
        else:
            print(f"❌ Wrong endpoint not caught: {response.status_code}")
    except Exception as e:
        print(f"❌ Wrong endpoint test failed: {e}")

def main():
    """Run all LocalAIHub tests."""
    print("🧪 Starting LocalAIHub API Tests")
    print("=" * 50)
    
    # Check if the server is running
    if not test_health():
        print("\n❌ Server isn't running. Start it with: python app.py")
        return
    
    print()
    test_status()
    print()
    test_generate()
    print()
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("✅ All tests done!")
    print("\n💡 Check logs/ai_hub_log.jsonl for interaction logs")

if __name__ == "__main__":
    main()