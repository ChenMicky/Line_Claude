# LINE Bot with Claude AI Wiki

A FastAPI-based LINE chatbot integrated with Claude AI via OpenRouter, with wiki functionality.

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/ChenMicky/Line_Claude.git
cd Line_Claude

# 2. Copy environment configuration
cp .env.example .env

# 3. Configure your API key
# Edit .env and add your OpenRouter API key:
# OPENROUTER_API_KEY=your_api_key_here
```

## Configuration

### Required: OpenRouter API Key

1. Get a free API key from [OpenRouter](https://openrouter.ai/)
2. Edit `.env` file:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Optional: LINE Bot Configuration

If you want to use a real LINE Bot (optional for local testing):

```bash
# Get from LINE Developers Console
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
LINE_CHANNEL_SECRET=your_channel_secret

# User ID to send messages to
DESTINATION_USER_ID=your_user_id
```

## Running the Application

### Option A: Docker (Recommended)

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

The app will be available at `http://localhost:8000`

### Option B: Local Python

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | Your OpenRouter API key |
| `OPENROUTER_BASE_URL` | No | Default: `https://openrouter.ai/api/v1` |
| `OPENROUTER_MODEL` | No | Default: `openrouter/free` |
| `WIKI_PATH` | No | Path to wiki directory |
| `PORT` | No | Server port, default: `8000` |
| `HOST` | No | Server host, default: `0.0.0.0` |
| `MAX_TOKENS` | No | Max response tokens, default: `4096` |
| `LINE_CHANNEL_ACCESS_TOKEN` | No | For LINE bot functionality |
| `LINE_CHANNEL_SECRET` | No | For LINE bot functionality |

## API Endpoints

- `GET /` - Health check
- `GET /docs` - API documentation (Swagger UI)
- `POST /webhook` - LINE webhook endpoint

## Project Structure

```
.
├── app/
│   ├── main.py           # FastAPI application
│   ├── routers/
│   │   └── webhook.py    # LINE webhook handler
│   └── services/
│       ├── claude_client.py   # OpenRouter/Claude integration
│       └── wiki_loader.py     # Wiki content loader
├── Claude_wiki/          # Wiki content (Obsidian vault)
├── docker-compose.yml   # Docker configuration
├── Dockerfile           # Container image definition
└── requirements.txt     # Python dependencies
```

## Troubleshooting

### "OPENROUTER_API_KEY not set"

Make sure you've copied `.env.example` to `.env` and added your API key.

### Port already in use

Change the port in `.env` or docker-compose.yml:
```bash
PORT=8000
```

### Docker permission issues

```bash
sudo chown -R $(id -u):$(id -g) .
```

## License

MIT