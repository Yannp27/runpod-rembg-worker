# RunPod Serverless Background Removal

GPU-accelerated background removal using rembg on RunPod.

## Deployment

1. **Build and push Docker image:**
```bash
cd Tools/runpod_rembg
docker build -t your-dockerhub/rembg-worker:latest .
docker push your-dockerhub/rembg-worker:latest
```

2. **Create RunPod Serverless Endpoint:**
   - Go to https://www.runpod.io/console/serverless
   - Click "New Endpoint"
   - Select your Docker image
   - Choose GPU type (RTX 3090 recommended for speed)
   - Set min/max workers (0/3 for auto-scale)

3. **Get your endpoint ID and API key:**
   - Endpoint ID: shown in endpoint URL
   - API Key: https://www.runpod.io/console/user/settings

## Usage

```bash
# Set environment variables
export RUNPOD_API_KEY="your_api_key"
export RUNPOD_ENDPOINT_ID="your_endpoint_id"

# Run
python Tools/remove_background_runpod.py input.png output.png
```

## Cost

- ~$0.0004/sec on RTX 3090
- ~2-5 seconds per image
- ~$0.001-0.002 per image

## Models Available

- `isnet-anime` (default) — Best for anime/illustrations
- `u2net` — General purpose
- `u2net_human_seg` — Optimized for humans
- `birefnet-general` — Highest quality, slower
