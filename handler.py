"""
RunPod Serverless Worker for rembg background removal.

Deploy this to RunPod as a Docker container.
See: https://docs.runpod.io/serverless/workers/development

Dockerfile:
-----------
FROM python:3.12-slim
WORKDIR /app
RUN pip install runpod rembg[cpu] pillow
COPY handler.py .
CMD ["python", "-u", "handler.py"]
"""

import runpod
import base64
import io
from PIL import Image
from rembg import remove, new_session

# Pre-load model for faster inference
print("Loading isnet-anime model...")
SESSION = new_session("isnet-anime")
print("Model loaded!")


def handler(event):
    """
    RunPod serverless handler.
    
    Input (event["input"]):
        image_base64: Base64 encoded input image
        model: Optional model name (default: isnet-anime)
        alpha_matting: Optional bool (default: False)
    
    Output:
        image_base64: Base64 encoded PNG with transparent background
    """
    try:
        input_data = event.get("input", {})
        
        # Decode input image
        image_b64 = input_data.get("image_base64")
        if not image_b64:
            return {"error": "No image_base64 provided"}
        
        image_bytes = base64.b64decode(image_b64)
        img = Image.open(io.BytesIO(image_bytes))
        
        # Get options
        model = input_data.get("model", "isnet-anime")
        use_matting = input_data.get("alpha_matting", False)
        
        # Use pre-loaded session or create new one
        session = SESSION if model == "isnet-anime" else new_session(model)
        
        # Remove background
        if use_matting:
            result = remove(
                img,
                session=session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=270,
                alpha_matting_background_threshold=5,
                alpha_matting_erode_size=3
            )
        else:
            result = remove(img, session=session)
        
        # Encode result
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        result_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        return {"image_base64": result_b64}
    
    except Exception as e:
        return {"error": str(e)}


# Start RunPod serverless worker
runpod.serverless.start({"handler": handler})
