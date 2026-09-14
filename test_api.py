"""
Test script for Chronosphere Chatbot API
Run this after starting the server: python main.py
"""

import requests
import json
from typing import Dict

API_URL = "http://localhost:8000"

class ChatbotTester:
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
        self.conversation_id = "test_session"
    
    def print_response(self, title: str, response: Dict):
        """Pretty print response"""
        print(f"\n{'='*60}")
        print(f"TEST: {title}")
        print(f"{'='*60}")
        print(json.dumps(response, indent=2))
    
    def test_health(self):
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health")
            self.print_response("Health Check", response.json())
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_root(self):
        """Test root endpoint"""
        try:
            response = requests.get(f"{self.base_url}/")
            self.print_response("Root Endpoint", response.json())
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Root endpoint failed: {e}")
            return False
    
    def test_chat(self, message: str):
        """Test chat endpoint"""
        try:
            payload = {
                "message": message,
                "conversation_id": self.conversation_id
            }
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload
            )
            self.print_response(f"Chat: {message}", response.json())
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Chat failed: {e}")
            return False
    
    def test_list_conversations(self):
        """Test list conversations endpoint"""
        try:
            response = requests.get(f"{self.base_url}/conversations")
            self.print_response("List Conversations", response.json())
            return response.status_code == 200
        except Exception as e:
            print(f"❌ List conversations failed: {e}")
            return False
    
    def test_clear_conversation(self):
        """Test clear conversation endpoint"""
        try:
            response = requests.delete(
                f"{self.base_url}/conversations/{self.conversation_id}"
            )
            self.print_response("Clear Conversation", response.json())
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Clear conversation failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("CHRONOSPHERE CHATBOT API TEST SUITE")
        print("="*60)
        
        results = {
            "Health Check": self.test_health(),
            "Root Endpoint": self.test_root(),
            "Chat - Question 1": self.test_chat("What is Chronosphere Lab?"),
            "Chat - Question 2": self.test_chat("Tell me about courses"),
            "Chat - Follow-up": self.test_chat("What about careers?"),
            "List Conversations": self.test_list_conversations(),
            "Clear Conversation": self.test_clear_conversation(),
        }
        
        # Print summary
        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}")
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        print(f"{'='*60}\n")
        
        return passed == total

if __name__ == "__main__":
    tester = ChatbotTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
