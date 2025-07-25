# Chrome Bookmark MCP Server - Installation Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Server Setup](#server-setup)
3. [Chrome Extension Installation](#chrome-extension-installation)
4. [Configuration](#configuration)
5. [Running the System](#running-the-system)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Chrome browser (version 88 or higher)
- Node.js (optional, for development)
- Docker and Docker Compose (optional, for containerized deployment)

### Required Services
- Redis (for caching and session management)
- Elasticsearch (optional, for advanced search features)

## Server Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd 2025.0711_Chrome\ Bookmark\ MCP\ Server
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r server/requirements.txt
```

### 4. Environment Configuration
Copy the example environment file and configure it:
```bash
cp .env.example .env
```

Edit `.env` file with your settings:
```env
# Server Configuration
WEBSOCKET_PORT=8012
LOG_LEVEL=INFO

# Chrome Profile Path (update with your actual path)
# Windows: C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default
# Mac: ~/Library/Application Support/Google/Chrome/Default
# Linux: ~/.config/google-chrome/Default
CHROME_PROFILE_PATH=/path/to/chrome/profile

# Security Keys (generate new ones for production)
JWT_SECRET_KEY=your-secret-key-here
MCP_ENCRYPTION_KEY=your-encryption-key-here

# AI Integration (optional)
CLAUDE_API_KEY=your-claude-api-key
CLAUDE_MODEL=claude-3-opus

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Elasticsearch (optional)
RAG_ENDPOINT=http://localhost:9200

# Performance Settings
MAX_CONCURRENT_REQUESTS=10
CACHE_TTL=3600
BROKEN_LINK_TIMEOUT=5
```

### 5. Generate Security Keys
```python
# Run this Python script to generate secure keys
import secrets
print(f"JWT_SECRET_KEY={secrets.token_urlsafe(32)}")
print(f"MCP_ENCRYPTION_KEY={secrets.token_urlsafe(32)}")
```

### 6. Database Setup (if using SQLite)
The server will automatically create necessary databases on first run.

## Chrome Extension Installation

### 1. Prepare the Extension
Navigate to the extension directory:
```bash
cd chrome-extension
```

### 2. Load Extension in Chrome
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. The extension icon should appear in your toolbar

### 3. Configure Extension
1. Click the extension icon
2. Go to Settings (gear icon)
3. Configure:
   - Server URL: `http://localhost:8012`
   - Auto-organize settings
   - Cleanup preferences
   - Notification preferences

## Configuration

### Server Configuration Options

#### Organization Strategies
- `ai_smart`: AI-powered intelligent organization
- `category`: Category-based organization
- `domain`: Domain-based organization
- `date`: Date-based organization
- `alphabetical`: Alphabetical organization

#### Cleanup Options
- `max_age_days`: Remove bookmarks older than X days
- `check_broken_links`: Verify and archive broken links
- `archive_duplicates`: Archive duplicate bookmarks
- `preserve_starred`: Keep starred bookmarks

### Extension Settings

Access via extension popup → Settings:

```javascript
{
  "autoOrganize": true,
  "organizationStrategy": "ai_smart",
  "organizationThreshold": 5,
  "foldersToSkip": ["Archive", "Trash"],
  "maxDepth": 3,
  "autoClean": true,
  "cleanInterval": 30,
  "preserveStarred": true,
  "checkBrokenLinks": true,
  "notificationsEnabled": true
}
```

## Running the System

### Option 1: Direct Python Execution

1. Start Redis:
```bash
redis-server
```

2. Start the MCP Server:
```bash
cd server
python MCP_Chrome_Server_033025.py
```

### Option 2: Using Docker Compose

1. Build and start all services:
```bash
docker-compose up -d
```

2. View logs:
```bash
docker-compose logs -f mcp-server
```

### Option 3: Production Deployment

For production, use a process manager like systemd or supervisor:

```ini
# /etc/systemd/system/mcp-bookmark-server.service
[Unit]
Description=MCP Chrome Bookmark Server
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/mcp-bookmark-server
Environment="PATH=/opt/mcp-bookmark-server/venv/bin"
ExecStart=/opt/mcp-bookmark-server/venv/bin/python server/MCP_Chrome_Server_033025.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Verification

### 1. Check Server Health
```bash
curl http://localhost:8012/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "redis": true,
    "elasticsearch": true,
    "ai": true
  }
}
```

### 2. Test WebSocket Connection
Open browser console and run:
```javascript
const ws = new WebSocket('ws://localhost:8012/ws');
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Message:', e.data);
```

### 3. Verify Extension Connection
1. Click extension icon
2. Check status indicator (should be green)
3. Try organizing bookmarks

## Troubleshooting

### Common Issues

#### 1. Server Won't Start
- Check if port 8012 is already in use: `netstat -an | grep 8012`
- Verify Python version: `python --version`
- Check error logs: `tail -f mcp_server.log`

#### 2. Extension Can't Connect
- Verify server is running: `curl http://localhost:8012/health`
- Check Chrome console for errors (F12 → Console)
- Ensure CORS is properly configured

#### 3. Redis Connection Failed
- Start Redis: `redis-server`
- Test connection: `redis-cli ping`
- Check Redis URL in `.env`

#### 4. Chrome Profile Access Denied
- Ensure Chrome is closed when accessing profile
- Check file permissions
- Use correct profile path for your OS

#### 5. WebSocket Disconnects
- Check network stability
- Increase timeout settings
- Review server logs for errors

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python server/MCP_Chrome_Server_033025.py
```

### Performance Optimization

For large bookmark collections:
1. Increase `MAX_CONCURRENT_REQUESTS`
2. Enable Redis caching
3. Use Elasticsearch for search
4. Adjust `BATCH_SIZE` in extension

### Security Considerations

1. Always use HTTPS in production
2. Generate new security keys
3. Configure firewall rules
4. Use strong JWT secrets
5. Enable rate limiting

## Support

For additional help:
1. Check server logs: `tail -f server/mcp_server.log`
2. Review extension console logs
3. Consult API documentation
4. Submit issues on GitHub

## Next Steps

1. Configure automated backups
2. Set up monitoring (Prometheus/Grafana)
3. Configure SSL certificates
4. Implement user authentication
5. Set up CI/CD pipeline