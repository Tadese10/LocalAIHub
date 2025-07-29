#!/usr/bin/env python3
"""
LocalAIHub CLI - A friendly command-line tool for chatting with your local AI
"""

import requests
import json
import sys
import time
import argparse
from typing import Optional

# Default API setup
DEFAULT_API_URL = "http://localhost:5000"

class LocalAIHubCLI:
    """A simple command-line tool to interact with your local AI server."""
    
    def __init__(self, api_url: str = DEFAULT_API_URL):
        self.api_url = api_url.rstrip('/')
    
    def _send_request(self, endpoint: str, method: str = "GET", data: Optional[dict] = None) -> tuple[bool, dict]:
        """Sends a request to the LocalAIHub server."""
        url = f"{self.api_url}{endpoint}"
        
        try:
            if method == "POST":
                response = requests.post(url, json=data, timeout=30)
            else:
                response = requests.get(url, timeout=10)
            
            return response.status_code == 200, response.json()
            
        except requests.exceptions.ConnectionError:
            return False, {"error": "Can't reach the LocalAIHub server. Is it running?"}
        except requests.exceptions.Timeout:
            return False, {"error": "The request took too long"}
        except Exception as e:
            return False, {"error": f"Something went wrong: {str(e)}"}
    
    def ask_ai(self, user_input: str, model: str = "llama2") -> None:
        """Sends your question to the AI and prints the response."""
        print(f"🤖 Sending your question to LocalAIHub...")
        
        start_time = time.time()
        success, result = self._send_request("/generate", "POST", {
            "prompt": user_input,
            "model": model
        })
        
        if success:
            print(f"\n✅ Got a response (took {result.get('duration_seconds', time.time() - start_time):.2f}s):")
            print(f"📝 Model used: {result.get('model', 'unknown')}")
            print(f"🎯 AI says:\n{result.get('response', 'No response')}")
            
            if result.get('model') == 'fallback-response':
                print("\n⚠️  Note: Using a backup response (Ollama isn't available)")
        else:
            print(f"\n❌ Oops: {result.get('error', 'Something went wrong')}")
    
    def check_status(self) -> None:
        """Shows the status of the LocalAIHub server."""
        print("📊 Checking LocalAIHub status...")
        
        success, result = self._send_request("/status")
        
        if success:
            print("\n✅ LocalAIHub Status:")
            print(f"🟢 Status: {result.get('status', 'unknown')}")
            print(f"⏰ Running for: {result.get('uptime_seconds', 0):.1f} seconds")
            print(f"📈 Questions answered: {result.get('requests_served', 0)}")
            print(f"💾 Memory usage: {result.get('memory_usage_percent', 0):.1f}%")
            print(f"💽 Free memory: {result.get('memory_available_gb', 0):.2f} GB")
            print(f"🔗 Ollama running: {'✅ Yes' if result.get('ollama_available') else '❌ No'}")
            print(f"📁 Logs saved to: {result.get('log_file', 'unknown')}")
        else:
            print(f"\n❌ Oops: {result.get('error', 'Something went wrong')}")
    
    def chat_mode(self) -> None:
        """Starts an interactive chat with the AI."""
        print("🚀 Welcome to LocalAIHub Chat Mode!")
        print("Type 'quit', 'exit', or press Ctrl+C to stop\n")
        
        try:
            while True:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 See you later!")
                    break
                
                if not user_input:
                    continue
                
                print()  # Add some space
                self.ask_ai(user_input)
                print("-" * 50)
                
        except KeyboardInterrupt:
            print("\n\n👋 See you later!")
        except EOFError:
            print("\n\n👋 See you later!")

def main():
    parser = argparse.ArgumentParser(
        description="LocalAIHub CLI - Chat with your local AI from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ask "Hello, who are you?"
  %(prog)s status
  %(prog)s chat
  %(prog)s ask "Tell me about Python" --model llama2
        """
    )
    
    parser.add_argument(
        '--api-url', 
        default=DEFAULT_API_URL,
        help=f'Server URL (default: {DEFAULT_API_URL})'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Ask command
    ask_parser = subparsers.add_parser('ask', help='Ask the AI a question')
    ask_parser.add_argument('prompt', help='Your question or prompt')
    ask_parser.add_argument('--model', default='llama2', help='AI model to use (default: llama2)')
    
    # Status command
    subparsers.add_parser('status', help='Check server status')
    
    # Chat command
    subparsers.add_parser('chat', help='Start interactive chat mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = LocalAIHubCLI(args.api_url)
    
    try:
        if args.command == 'ask':
            cli.ask_ai(args.prompt, args.model)
        elif args.command == 'status':
            cli.check_status()
        elif args.command == 'chat':
            cli.chat_mode()
    except Exception as e:
        print(f"❌ Something broke: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()