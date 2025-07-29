
#!/usr/bin/env python3
"""
LocalAIHub Server
A simple local REST API for running AI language models offline.
"""

import os
import json
import time
import psutil
import requests
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from typing import Dict, Any, Optional

# Setup
OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_AI_MODEL = "llama2"  # Backup model if none specified
LOG_FOLDER = Path("logs")
LOG_FILE = LOG_FOLDER / "ai_hub_log.jsonl"

# Create logs folder if it doesn't exist
LOG_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)

class LocalAIHub:
    """Handles local AI model interactions and logging."""
    
    def __init__(self):
        self.start_time = time.time()
        self.total_requests = 0
        
    def _save_interaction(self, user_input: str, ai_response: str, model: str, time_taken: float, error: Optional[str] = None):
        """Saves the user input and AI response to a log file."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response,
            "model": model,
            "time_taken_seconds": round(time_taken, 3),
            "error": error,
            "request_id": self.total_requests
        }
        
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as file:
                file.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Could not save log: {e}")
    
    def _query_ollama(self, user_input: str, model: str = DEFAULT_AI_MODEL) -> tuple[str, Optional[str]]:
        """Sends a request to the Ollama API to generate a response."""
        try:
            request_data = {
                "model": model,
                "prompt": user_input,
                "stream": False
            }
            
            response = requests.post(
                OLLAMA_API_URL,
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response generated"), None
            else:
                return None, f"Ollama API error: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return None, "Ollama isn't running - please start it!"
        except requests.exceptions.Timeout:
            return None, "Request took too long"
        except Exception as e:
            return None, f"Something went wrong: {str(e)}"
    
    def _create_fallback_response(self, user_input: str) -> str:
        """Generates a simple response when Ollama isn't available."""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["hello", "hi", "hey"]):
            return f"Hi there! I'm your local AI ({DEFAULT_AI_MODEL}) running offline on your computer."
        elif any(word in input_lower for word in ["who", "what are you"]):
            return f"I'm LocalAIHub, your offline AI assistant using the {DEFAULT_AI_MODEL} model."
        elif any(word in input_lower for word in ["help", "what can you do"]):
            return "I can answer questions and help with tasks, all offline for privacy and speed."
        elif "time" in input_lower:
            return f"It's currently {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        else:
            return f"I'm your offline AI ({DEFAULT_AI_MODEL}). You said: '{user_input[:50]}...' - I'm handling this locally for privacy."
    
    def generate_response(self, user_input: str, model: str = DEFAULT_AI_MODEL) -> Dict[str, Any]:
        """Generates a response to the user's input."""
        start_time = time.time()
        self.total_requests += 1
        
        # Try to get a response from Ollama
        response, error = self._query_ollama(user_input, model)
        
        # If Ollama fails, use a fallback response
        if response is None:
            response = self._create_fallback_response(user_input)
            model_used = "fallback-response"
        else:
            model_used = model
            error = None
        
        time_taken = time.time() - start_time
        
        # Log the interaction
        self._save_interaction(user_input, response, model_used, time_taken, error)
        
        return {
            "response": response,
            "model": model_used,
            "time_taken_seconds": round(time_taken, 3),
            "offline": True,
            "request_id": self.total_requests
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Returns information about the system's status."""
        uptime = time.time() - self.start_time
        memory = psutil.virtual_memory()
        
        # Check if Ollama is running
        ollama_running = False
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            ollama_running = response.status_code == 200
        except:
            pass
        
        return {
            "status": "running",
            "uptime_seconds": round(uptime, 1),
            "requests_handled": self.total_requests,
            "memory_usage_percent": memory.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "ollama_running": ollama_running,
            "log_file": str(LOG_FILE),
            "timestamp": datetime.utcnow().isoformat()
        }

# Start the AI hub
ai_hub = LocalAIHub()

@app.route('/generate', methods=['POST'])
def generate():
    """Handles user prompts and returns AI responses."""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Please include a 'prompt' in your request"}), 400
        
        user_input = data['prompt']
        model = data.get('model', DEFAULT_AI_MODEL)
        
        if not user_input.strip():
            return jsonify({"error": "Prompt cannot be empty"}), 400
        
        result = ai_hub.generate_response(user_input, model)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500

@app.route('/status', methods=['GET'])
def status():
    """Shows system status and performance details."""
    try:
        status_info = ai_hub.get_system_status()
        return jsonify(status_info)
    except Exception as e:
        return jsonify({"error": f"Could not fetch status: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Quick check to confirm the server is running."""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "This endpoint doesn't exist"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Something broke on our end"}), 500

if __name__ == '__main__':
    print("🌟 Starting LocalAIHub Server...")
    print(f"📝 Logs will be saved to: {LOG_FILE}")
    print("🔗 Available endpoints:")
    print("   POST /generate - Send a prompt to get an AI response")
    print("   GET /status    - Check system status and stats")
    print("   GET /health    - Quick server health check")
    print("\n💡 Tip: Make sure Ollama is running with: ollama serve")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )