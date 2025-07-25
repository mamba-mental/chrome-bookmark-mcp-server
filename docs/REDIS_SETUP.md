# Redis Setup Guide

## Overview

Redis is used in the MCP Chrome Bookmark Server for:
- Caching bookmark data
- Session management
- Real-time message queuing
- Rate limiting

## Installation

### Using Docker (Recommended)

The docker-compose.yml file includes Redis configuration:

```yaml
redis:
  image: redis:7-alpine
  container_name: mcp-redis
  ports:
    - "6379:6379"
  volumes:
    - redis-data:/data
  command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
```

### Manual Installation

#### Windows
1. Download Redis from https://github.com/microsoftarchive/redis/releases
2. Extract and run redis-server.exe

#### macOS
```bash
brew install redis
brew services start redis
```

#### Linux
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

## Configuration

### Environment Variables

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # Optional, for production
REDIS_URL=redis://localhost:6379
```

### Redis Configuration File

Create a `redis.conf` for custom settings:

```conf
# Memory Management
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
appendonly yes

# Security (Production)
requirepass your_secure_password

# Performance
tcp-backlog 511
timeout 0
tcp-keepalive 300
```

## Usage

### Basic Commands

#### Connect to Redis CLI
```bash
redis-cli
```

#### Test Connection
```bash
redis-cli ping
# Should return: PONG
```

#### View All Keys
```bash
redis-cli keys *
```

#### Get Specific Key
```bash
redis-cli get "bookmark:cache:12345"
```

#### Monitor Real-time Commands
```bash
redis-cli monitor
```

### Cache Patterns Used

1. **Bookmark Cache**
   - Key: `bookmark:cache:{bookmark_id}`
   - TTL: 3600 seconds (1 hour)

2. **Search Results**
   - Key: `search:{query_hash}`
   - TTL: 300 seconds (5 minutes)

3. **User Sessions**
   - Key: `session:{session_id}`
   - TTL: 86400 seconds (24 hours)

4. **Rate Limiting**
   - Key: `rate:{user_id}:{endpoint}`
   - TTL: 60 seconds

## Performance Optimization

### Memory Optimization

1. **Set appropriate maxmemory**
   ```bash
   redis-cli config set maxmemory 512mb
   ```

2. **Choose eviction policy**
   - `allkeys-lru`: Evict any key using LRU
   - `volatile-lru`: Evict keys with TTL using LRU
   - `allkeys-lfu`: Evict any key using LFU (Redis 4.0+)

3. **Enable compression**
   ```bash
   redis-cli config set list-compress-depth 1
   ```

### Connection Pooling

The server uses connection pooling for efficiency:

```python
redis_pool = aioredis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    decode_responses=True
)
```

## Monitoring

### Redis INFO Command

```bash
redis-cli info
```

Key metrics to monitor:
- `used_memory_human`: Current memory usage
- `connected_clients`: Active connections
- `instantaneous_ops_per_sec`: Operations per second
- `keyspace_hits/misses`: Cache hit ratio

### Redis Monitoring Tools

1. **RedisInsight** (Official GUI)
   ```bash
   docker run -p 8001:8001 redislabs/redisinsight
   ```

2. **redis-stat** (Terminal monitoring)
   ```bash
   gem install redis-stat
   redis-stat
   ```

## Backup and Recovery

### Manual Backup

```bash
# Save snapshot
redis-cli bgsave

# Copy dump file
cp /var/lib/redis/dump.rdb ./backup/
```

### Automated Backup

Add to crontab:
```bash
0 2 * * * redis-cli bgsave && cp /var/lib/redis/dump.rdb /backup/redis-$(date +\%Y\%m\%d).rdb
```

### Restore from Backup

1. Stop Redis
2. Replace dump.rdb with backup
3. Start Redis

## Security Best Practices

### 1. Set a Password

```bash
redis-cli config set requirepass "strong_password_here"
```

### 2. Disable Dangerous Commands

In redis.conf:
```conf
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS ""
rename-command CONFIG ""
```

### 3. Bind to Localhost Only

```conf
bind 127.0.0.1 ::1
```

### 4. Enable SSL/TLS (Production)

```conf
tls-port 6380
port 0
tls-cert-file /path/to/cert.pem
tls-key-file /path/to/key.pem
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if Redis is running: `ps aux | grep redis`
   - Verify port: `netstat -an | grep 6379`
   - Check bind address in config

2. **Out of Memory**
   - Check memory usage: `redis-cli info memory`
   - Adjust maxmemory setting
   - Review eviction policy

3. **Slow Performance**
   - Monitor slow queries: `redis-cli slowlog get`
   - Check for blocking operations
   - Review client connection count

4. **Data Loss**
   - Ensure persistence is enabled
   - Check disk space for dumps
   - Review save/appendonly settings

## Useful Commands Reference

```bash
# Flush all data (careful!)
redis-cli flushall

# Get database size
redis-cli dbsize

# Get configuration
redis-cli config get *

# Set configuration
redis-cli config set parameter value

# Save data immediately
redis-cli save

# Background save
redis-cli bgsave

# Get last save time
redis-cli lastsave

# Monitor commands in real-time
redis-cli monitor
```
