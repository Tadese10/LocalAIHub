LocalAIHub
A simple, privacy-focused local REST API for running AI language models offline, ensuring your data stays on your device.
🌟 Why LocalAIHub?

🏠 Completely Offline: Works without an internet connection for maximum privacy
🤖 Real AI Power: Uses Ollama for local AI model processing
📝 Detailed Logs: Keeps track of all interactions in logs/ai_hub_log.jsonl
💻 Easy CLI Tool: Comes with a user-friendly command-line interface
📈 System Insights: Check server status, memory usage, and more
🐳 Docker Support: Quick setup with Docker for hassle-free deployment
🛡️ Smart Error Handling: Smoothly handles issues with friendly fallback responses

🚀 Get Started
Option 1: Python Setup (Great for Development)
# Grab the code and set up
git clone <repository>
cd local-ai-hub

# Run the setup script
chmod +x setup.sh  # On Windows, skip this and run setup directly (see below)
./setup.sh

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Start the server
python app.py

Option 2: Docker Setup
# Easiest: Use Docker Compose
docker-compose up --build

# Or use Docker directly
docker build -t local-ai-hub .
docker run -p 5000:5000 -v $(pwd)/logs:/app/logs local-ai-hub

📡 API Endpoints
POST /generate
Ask the AI a question or give it a task.
Request:
{
  "prompt": "Hi, who are you?",
  "model": "llama2"  // optional
}

Response:
{
  "response": "I'm LocalAIHub, your offline AI assistant running on your computer!",
  "model": "llama2",
  "time_taken_seconds": 1.234,
  "offline": true,
  "request_id": 1
}

GET /status
Check how the server is doing.
Response:
{
  "status": "running",
  "uptime_seconds": 3661.2,
  "requests_handled": 15,
  "memory_usage_percent": 45.2,
  "memory_available_gb": 8.24,
  "ollama_running": true,
  "log_file": "logs/ai_hub_log.jsonl",
  "timestamp": "2025-07-26T16:15:00.123456"
}

GET /health
Quick check to see if the server is up.
💻 Using the CLI
The included command-line tool makes it easy to interact with the API:
# Activate the Python environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Ask a single question
python cli.py ask "Hi, who are you?"

# Check server status
python cli.py status

# Start a chat session
python cli.py chat

# See all options
python cli.py --help

CLI Examples
# Ask a question
$ python cli.py ask "What's Python in one sentence?"
🤖 Sending your question to LocalAIHub...

✅ Got a response (took 0.85s):
📝 Model used: llama2
🎯 AI says:
Python is a simple, readable programming language used for all kinds of projects.

# Chat mode
$ python cli.py chat
🚀 Welcome to LocalAIHub Chat Mode!
Type 'quit', 'exit', or press Ctrl+C to stop

You: Hi there!
🤖 Sending your question to LocalAIHub...

✅ Got a response (took 0.12s):
📝 Model used: fallback-response
🎯 AI says:
Hi! I'm your local AI (llama2) running offline on your computer.
--------------------------------------------------
You: quit
👋 See you later!

🤖 Using Real AI Models (Ollama)
To use real AI models instead of fallback responses:

Install Ollama: Head to ollama.com and follow their setup guide.

Download a model:
ollama pull llama2
# or for a smaller, faster model:
ollama pull llama2:7b


Start the Ollama server:
ollama serve


Run LocalAIHub (in another terminal):
python app.py



Now your API will use real AI models via Ollama for smarter responses!
📁 Project Layout
local-ai-hub/
├── app.py              # Main API server
├── cli.py              # Command-line tool
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker setup
├── docker-compose.yml  # Docker Compose setup
├── setup.sh            # Setup script
├── test_api.py         # API tests
├── README.md           # This guide
└── logs/               # Where logs are saved
    └── ai_hub_log.jsonl  # Interaction logs

📝 Logging
Every question and answer is saved to logs/ai_hub_log.jsonl in an easy-to-read JSONL format:
{"timestamp": "2025-07-26T16:15:00.123456", "user_input": "Hi!", "ai_response": "Hey there!", "model": "llama2", "time_taken_seconds": 0.856, "error": null, "request_id": 1}
