# Chrome Bookmark MCP Server

A Model Context Protocol (MCP) server implementation that provides seamless integration between Chrome bookmarks and AI assistants. This server enables AI models to access, search, analyze, and manage Chrome bookmarks through a standardized protocol.

## Overview

This project implements an MCP server that bridges Chrome bookmarks with AI assistants, allowing for intelligent bookmark management, search, and analysis. It includes both a Chrome extension for data collection and a Python-based MCP server for processing requests.

## Features

### Core Functionality
- **Bookmark Access**: Read and search through Chrome bookmarks
- **Advanced Search**: Full-text search with ElasticSearch integration
- **Real-time Sync**: Automatic synchronization of bookmark changes via WebSocket
- **Analytics**: Bookmark usage patterns and insights
- **Security**: JWT authentication and secure communication

### Chrome Extension
- Bookmark export and synchronization
- Search interface with advanced filtering
- Usage analytics dashboard
- Real-time updates via WebSocket
- Offline message queuing

### MCP Server
- Standard MCP protocol implementation
- WebSocket support for real-time updates
- RESTful API endpoints
- Redis caching for performance
- ElasticSearch for advanced search
- Docker support for easy deployment

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Chrome Browser  │────▶│  Chrome Ext.    │────▶│   MCP Server    │
│   (Bookmarks)   │     │  (Data Export)  │     │  (Processing)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
                                ┌─────────────────────────┴─────────────┐
                                │                                       │
                        ┌───────▼────────┐                    ┌────────▼───────┐
                        │     Redis      │                    │ ElasticSearch  │
                        │   (Caching)    │                    │   (Search)     │
                        └────────────────┘                    └────────────────┘
```

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Chrome Browser
- Redis (via Docker)
- ElasticSearch (via Docker)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mamba-mental/chrome-bookmark-mcp-server.git
cd chrome-bookmark-mcp-server
```

### 2. Set Up the Server

#### Using Docker (Recommended)
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

#### Manual Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up Redis and ElasticSearch (see docs/REDIS_SETUP.md and docs/ELASTICSEARCH_SETUP.md)
```

### 3. Install Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `chrome-extension` folder from this repository
5. The extension icon should appear in your toolbar

### 4. Configure the Server

Create a `.env` file in the project root:
```env
# Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8012
SECRET_KEY=your-secret-key-here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# ElasticSearch Configuration
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=chrome_bookmarks

# Security
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=3600
```

## Usage

### Starting the Server

#### With Docker
```bash
docker-compose up
```

#### Without Docker
```bash
python server/MCP_Chrome_Server_033025.py
```

### Chrome Extension

1. Click the extension icon in Chrome
2. Use the popup interface to:
   - Export bookmarks to the server
   - Search bookmarks with filters
   - View analytics dashboard
   - Configure settings

### MCP Integration

Connect your AI assistant to the MCP server:
```json
{
  "mcpServers": {
    "chrome-bookmarks": {
      "command": "python",
      "args": ["/path/to/server/MCP_Chrome_Server_033025.py"],
      "env": {
        "PYTHONPATH": "/path/to/project"
      }
    }
  }
}
```

## API Documentation

### MCP Tools

The server provides the following MCP tools:

- `search_bookmarks`: Search bookmarks with advanced filters
- `get_bookmark`: Retrieve a specific bookmark by ID
- `analyze_bookmarks`: Get analytics and insights
- `organize_bookmarks`: Auto-organize bookmarks
- `export_bookmarks`: Export bookmarks in various formats

### REST API Endpoints

- `GET /api/bookmarks`: List all bookmarks
- `GET /api/bookmarks/search`: Search bookmarks
- `GET /api/bookmarks/{id}`: Get specific bookmark
- `POST /api/bookmarks/sync`: Sync bookmarks from Chrome
- `GET /api/analytics/dashboard`: Get analytics data
- `POST /api/auth/login`: Authenticate and get JWT token
- `WS /ws`: WebSocket endpoint for real-time updates

## Development

### Project Structure
```
chrome-bookmark-mcp-server/
├── chrome-extension/       # Chrome extension source
│   ├── manifest.json      # Extension manifest
│   ├── popup.html/js      # Extension popup interface
│   ├── background.js      # Background service worker
│   ├── search.html        # Search interface
│   ├── analysis.html      # Analytics dashboard
│   └── icons/             # Extension icons
├── server/                # MCP server implementation
│   ├── MCP_Chrome_Server_033025.py         # Main server
│   ├── MCP_Chrome_Schemas_033025.py        # Data schemas
│   ├── Security_Module_033025.py           # Security module
│   ├── Advanced_Features_Module_033025.py  # Advanced features
│   └── requirements.txt                    # Python dependencies
├── config/                # Configuration files
├── docs/                  # Documentation
│   ├── ELASTICSEARCH_SETUP.md
│   ├── REDIS_SETUP.md
│   └── MCP_Implementation_Project_Master_Plan_031125.md
├── docker-compose.yml     # Docker configuration
└── requirements.txt       # Root Python dependencies
```

### Running Tests
```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=server tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Considerations

- JWT tokens for authentication
- API rate limiting to prevent abuse
- Secure WebSocket connections (WSS in production)
- Input validation and sanitization
- No storage of sensitive user data

## Troubleshooting

### Common Issues

1. **Extension not connecting to server**
   - Check server is running on port 8012
   - Verify no firewall blocking
   - Check browser console for errors

2. **Search not working**
   - Ensure ElasticSearch is running
   - Check if bookmarks are indexed
   - Verify ElasticSearch connection

3. **WebSocket disconnections**
   - Check network stability
   - Review server logs
   - Ensure proper CORS configuration

For detailed setup instructions, see:
- [Installation Guide](INSTALLATION.md)
- [ElasticSearch Setup](docs/ELASTICSEARCH_SETUP.md)
- [Redis Setup](docs/REDIS_SETUP.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Model Context Protocol specification by Anthropic
- Chrome Extensions API documentation
- Open source libraries and contributors

## Contact

For questions, issues, or contributions, please open an issue on GitHub.

---

**Note**: This is an active development project. Features and APIs may change. Please refer to the latest documentation and release notes.