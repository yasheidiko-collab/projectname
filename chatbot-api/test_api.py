"""
Test client for Chatbot API
Run: python test_api.py
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

def test_health():
    print("\n🏥 Testing Health Check...")
    response = requests.get(f"{API_URL}/v1/health")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Uptime: {response.json()['uptime_seconds']:.0f}s")

def test_streaming():
    print("\n🌊 Testing Streaming Chat...")
    
    payload = {
        "messages": [{"role": "user", "content": "Write a haiku about AI"}],
        "temperature": 0.8,
        "stream": True
    }
    
    print("   Response: ", end="", flush=True)
    
    response = requests.post(f"{API_URL}/v1/chat", json=payload, stream=True)
    
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if 'content' in data:
                    print(data['content'], end="", flush=True)
                elif data.get('event') == 'done':
                    print(f"\n   Metrics: {data['metrics']['total_time_ms']:.0f}ms, {data['metrics']['token_count']} tokens")

def test_non_streaming():
    print("\n📝 Testing Non-Streaming Chat...")
    
    payload = {
        "messages": [{"role": "user", "content": "What is Python?"}],
        "stream": False,
        "max_tokens": 100
    }
    
    response = requests.post(f"{API_URL}/v1/chat", json=payload)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Response: {data['content'][:100]}...")
        print(f"   Tokens: {data['usage']['total_tokens']}")

def test_conversation_memory():
    print("\n💬 Testing Conversation Memory...")
    
    session_id = "test_session_123"
    
    payload1 = {
        "messages": [{"role": "user", "content": "My name is Alex"}],
        "session_id": session_id,
        "stream": False
    }
    response1 = requests.post(f"{API_URL}/v1/chat", json=payload1)
    
    payload2 = {
        "messages": [{"role": "user", "content": "What's my name?"}],
        "session_id": session_id,
        "stream": False
    }
    response2 = requests.post(f"{API_URL}/v1/chat", json=payload2)
    
    if response2.status_code == 200:
        print(f"   Assistant remembers: {response2.json()['content']}")

def test_rate_limiting():
    print("\n🚦 Testing Rate Limiting...")
    
    payload = {"messages": [{"role": "user", "content": "Hi"}], "stream": False}
    
    for i in range(35):
        response = requests.post(f"{API_URL}/v1/chat", json=payload)
        if response.status_code == 429:
            print(f"   Rate limited after {i+1} requests")
            break

def test_metrics():
    print("\n📊 Testing Metrics...")
    response = requests.get(f"{API_URL}/v1/metrics")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total requests: {data['total_requests']}")