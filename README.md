# RunPod Serverless Image Processing Worker

GPU-accelerated image processing tools on RunPod Serverless.

## Available Tools

| Tool | Description | Status |
|------|-------------|--------|
| `rembg` | Background removal (isnet-anime) | ✅ Ready |
| `ping` | Health check | ✅ Ready |
| `upscale` | Image upscaling | 🔲 Planned |
| `face_detect` | Face detection/cropping | 🔲 Planned |

## API Usage

```bash
# Set environment variables
export RUNPOD_API_KEY="your_api_key"
export RUNPOD_ENDPOINT_ID="your_endpoint_id"

# Background removal (default tool)
python remove_background_runpod.py input.png output.png

# Or call API directly with tool parameter
curl -X POST "https://api.runpod.ai/v2/${RUNPOD_ENDPOINT_ID}/run" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"input": {"tool": "rembg", "image_base64": "..."}}'

# Health check
curl -X POST "https://api.runpod.ai/v2/${RUNPOD_ENDPOINT_ID}/run" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -d '{"input": {"tool": "ping"}}'
```

## Deployment

### Via RunPod Console (Recommended)

1. Go to https://www.runpod.io/console/serverless
2. Click "New Endpoint" → "GitHub Repo"
3. Connect: `Yannp27/runpod-rembg-worker`
4. Settings:
   - GPU: RTX 3090 or 4090 (AMPERE_24 / ADA_24)
   - Container Disk: 20GB
   - Min Workers: 0 (or 1 for instant response)
   - Max Workers: 3
   - Idle Timeout: 5s

### Via Docker Hub

```bash
docker build -t your-dockerhub/image-tools-worker:latest .
docker push your-dockerhub/image-tools-worker:latest
```

## Tool Reference

### rembg (Background Removal)

```json
{
  "input": {
    "tool": "rembg",
    "image_base64": "<base64 encoded image>",
    "model": "isnet-anime",
    "alpha_matting": false
  }
}
```

**Models**: `isnet-anime` (default), `u2net`, `u2net_human_seg`, `birefnet-general`

### ping (Health Check)

```json
{"input": {"tool": "ping"}}
```

Returns: `{"status": "ok", "tools": ["rembg", "ping"]}`

## Cost

- ~$0.22/hr on RTX 3090
- ~0.5-1 second per image (inference only)
- ~$0.001-0.002 per image
