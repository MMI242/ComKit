# Ollama Setup Guide

This guide explains how to set up Ollama for the ComKit AI recipe generation feature.

## Current Configuration

The system is now configured to use only Ollama as the AI provider:
- **Primary Provider**: Ollama
- **Fallback Provider**: Mock (for development/testing)
- **OpenAI**: Removed from configuration

## Option 1: Install Ollama Locally (Recommended)

### Prerequisites
- macOS, Linux, or Windows with WSL2
- At least 8GB RAM
- 10GB+ free disk space

### Installation Steps

1. **Install Ollama**
   ```bash
   # macOS
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Or download from https://ollama.com/download
   ```

2. **Start Ollama Service**
   ```bash
   ollama serve
   ```

3. **Download a Model**
   ```bash
   # For recipe generation, recommended models:
   ollama pull qwen2.5:7b           # Good balance of size and capability
   ollama pull llama3.1:8b          # Excellent for general tasks
   ollama pull mistral:7b           # Lightweight and fast
   
   # For better quality (requires more resources):
   ollama pull qwen2.5:14b          # Higher quality responses
   ```

4. **Update Configuration**
   
   Edit `.env` file to use the downloaded model:
   ```env
   DEFAULT_OLLAMA_MODEL=qwen2.5:7b
   OLLAMA_API_URL=http://localhost:11434
   ```

5. **Restart the Server**
   ```bash
   # Stop current server (Ctrl+C)
   python main.py
   ```

## Option 2: Use Remote Ollama Server

If you have Ollama running on another server:

1. **Update .env Configuration**
   ```env
   OLLAMA_API_URL=http://your-server-ip:11434
   DEFAULT_OLLAMA_MODEL=your-model-name
   ```

2. **Ensure Firewall Access**
   - Make sure port 11434 is open on the remote server
   - Test connectivity: `curl http://your-server-ip:11434/api/tags`

## Option 3: Use Ollama Cloud Services

Some cloud providers offer Ollama as a service:

1. **Update .env**
   ```env
   OLLAMA_API_URL=https://your-ollama-cloud-provider.com
   DEFAULT_OLLAMA_MODEL=available-model-name
   ```

## Testing the Setup

After installation, test with:

```bash
# Test Ollama directly
curl http://localhost:11434/api/tags

# Test through ComKit API
curl -X POST "http://localhost:8000/ai/recipe" \
  -H "Content-Type: application/json" \
  -H "Cookie: access_token=your-token" \
  -d '{"ingredients": "tomatoes, onions, garlic"}'
```

## Model Recommendations

### For Development/Low Resource:
- `qwen2.5:1.5b` - Very fast, basic responses
- `mistral:7b` - Good balance

### For Production:
- `qwen2.5:7b` - Excellent for recipes, good performance
- `llama3.1:8b` - High quality, widely compatible

### For High Quality (if resources allow):
- `qwen2.5:14b` - Best recipe generation
- `llama3.1:70b` - Superior quality (requires significant resources)

## Troubleshooting

### Ollama Health Check Failed
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama service
ollama serve

# Check available models
ollama list
```

### Connection Issues
```bash
# Test local connection
curl http://localhost:11434/api/tags

# Check if port is accessible
telnet localhost 11434
```

### Memory Issues
- Use smaller models (1.5b, 3b parameters)
- Close other applications
- Consider using a machine with more RAM

## Current Fallback Behavior

When Ollama is not available, the system automatically falls back to a Mock provider that:
- Returns a simple recipe structure
- Ensures the API never fails
- Provides consistent response format
- Is suitable for development and testing

This means your application will work even without Ollama installed!
