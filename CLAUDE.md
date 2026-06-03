# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based LINE chatbot integrated with Claude AI via OpenRouter, designed to provide responses using context from an Obsidian wiki. The application primarily receives webhooks from n8n workflows, processes user queries with Claude AI using wiki context, and returns intelligent responses.

## Architecture

### Core Components

1. **FastAPI Application** (`app/main.py`)
   - Main application entry point
   - Configures CORS middleware for cross-origin requests
   - Includes webhook router and health check endpoints
   - Loads wiki path configuration on startup

2. **Webhook Handler** (`app/routers/webhook.py`)
   - `/webhook/n8n` endpoint for processing n8n webhook requests
   - Handles message requests with optional conversation history
   - Integrates with ClaudeClient for AI processing
   - Returns structured responses with metadata

3. **Claude Client** (`app/services/claude_client.py`)
   - Manages communication with OpenRouter API (Anthropic-compatible)
   - Builds system prompts incorporating wiki content
   - Handles API errors, timeouts, and rate limits
   - Tracks token usage for cost monitoring

4. **Wiki Loader** (`app/services/wiki_loader.py`)
   - Loads all Markdown files from the Obsidian wiki directory
   - Combines all wiki content with file headers for context
   - Supports custom wiki paths via configuration
   - Logs file loading operations for debugging

### Data Flow

1. n8n sends webhook request to `/webhook/n8n` endpoint
2. Wiki content is loaded from the configured directory (default: `Claude_wiki/`)
3. ClaudeClient builds system prompt with wiki context
4. OpenRouter API processes the request with conversation history
5. Response is returned with usage metadata

## Configuration

### Required Environment Variables

- `OPENROUTER_API_KEY`: OpenRouter API key for Claude access
- `OPENROUTER_MODEL`: Model to use (e.g., "openrouter/free")

### Optional Environment Variables

- `WIKI_PATH`: Path to wiki directory (default: "/app/Claude_wiki")
- `MAX_TOKENS`: Maximum response tokens (default: 4096)
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: "0.0.0.0")

### LINE Bot Configuration (Optional)

- `LINE_CHANNEL_ACCESS_TOKEN`: For real LINE bot functionality
- `LINE_CHANNEL_SECRET`: For real LINE bot functionality
- `DESTINATION_USER_ID`: User ID to send messages to

## Development Commands

### Running the Application

**Docker (Recommended):**
```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**Local Python:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

### Testing

**Health Check:**
```bash
curl http://localhost:8000/health
curl http://localhost:8000/webhook/n8n/health
```

**Test Webhook:**
```bash
curl -X POST http://localhost:8000/webhook/n8n \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

## Wiki Integration

The application loads all Markdown files from the configured wiki directory and includes them as context in Claude's system prompt. Each file is prefixed with its relative path for reference. The wiki is mounted as a Docker volume for live updates without container rebuilds.

## Notes

- The application is designed to work with n8n workflows but can be used with any webhook-capable system
- All wiki content is loaded on every request - for large wikis, consider implementing caching
- OpenRouter requires HTTP-Referer and X-Title headers in API requests
- The application uses UTF-8 encoding for all file operations