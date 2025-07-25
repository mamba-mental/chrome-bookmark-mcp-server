# ElasticSearch Setup Guide

## Overview

ElasticSearch is used in the MCP Chrome Bookmark Server for advanced search capabilities and RAG (Retrieval Augmented Generation) support.

## Installation

### Using Docker (Recommended)

The docker-compose.yml file includes ElasticSearch configuration:

```yaml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
  container_name: mcp-elasticsearch
  environment:
    - discovery.type=single-node
    - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    - xpack.security.enabled=false
  ports:
    - "9200:9200"
    - "9300:9300"
```

### Manual Installation

1. Download ElasticSearch from https://www.elastic.co/downloads/elasticsearch
2. Extract and run:
   ```bash
   ./bin/elasticsearch
   ```

## Configuration

### Environment Variables

```env
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=chrome_bookmarks
```

### Index Mapping

The server automatically creates the index with appropriate mappings:

```json
{
  "mappings": {
    "properties": {
      "id": {"type": "keyword"},
      "title": {"type": "text"},
      "url": {"type": "keyword"},
      "folder_path": {"type": "keyword"},
      "content_snippet": {"type": "text"},
      "tags": {"type": "keyword"},
      "date_added": {"type": "date"},
      "last_visited": {"type": "date"},
      "visit_count": {"type": "integer"},
      "embedding": {"type": "dense_vector", "dims": 768}
    }
  }
}
```

## Usage

### Health Check

```bash
curl http://localhost:9200/_cluster/health
```

### View Index

```bash
curl http://localhost:9200/chrome_bookmarks/_mapping
```

### Search Example

```bash
curl -X GET "localhost:9200/chrome_bookmarks/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "title": "javascript"
    }
  }
}'
```

## Optimization

### Memory Settings

- Minimum: 512MB
- Recommended: 1GB
- Production: 2GB+

### Performance Tuning

1. Adjust heap size in ES_JAVA_OPTS
2. Enable caching for frequent queries
3. Use appropriate refresh intervals
4. Consider using SSD storage

## Troubleshooting

### Common Issues

1. **Out of Memory**
   - Increase heap size
   - Reduce index size

2. **Slow Queries**
   - Check index mappings
   - Add more memory
   - Optimize queries

3. **Connection Refused**
   - Check if ElasticSearch is running
   - Verify port configuration
   - Check firewall settings

## Security

### Basic Security (Production)

1. Enable X-Pack security:
   ```yaml
   xpack.security.enabled: true
   ```

2. Set up authentication:
   ```bash
   ./bin/elasticsearch-setup-passwords auto
   ```

3. Configure SSL/TLS for production

## Monitoring

### Kibana Integration

Add Kibana to docker-compose.yml:

```yaml
kibana:
  image: docker.elastic.co/kibana/kibana:8.11.0
  container_name: mcp-kibana
  ports:
    - "5601:5601"
  environment:
    - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
```

Access at http://localhost:5601
