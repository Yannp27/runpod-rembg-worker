"""
RunPod Serverless Multi-Tool Worker for Image Processing.

Supports multiple tools via the 'tool' parameter:
- rembg: Background removal (default)
- (future) upscale: Image upscaling
- (future) face_detect: Face detection/cropping

Deploy to RunPod as a Docker container.
"""

import runpod
import base64
import io
from PIL import Image

# ============================================================================
# TOOL: rembg - Background Removal
# ============================================================================
from rembg import remove, new_session

print("Loading isnet-anime model...")
REMBG_SESSION = new_session("isnet-anime")
print("Model loaded!")


def rembg_handler(input_data: dict) -> dict:
    """
    Remove background from image.
    
    Input:
        image_base64: Base64 encoded input image
        model: Optional model name (default: isnet-anime)
        alpha_matting: Optional bool for cleaner edges (default: False)
    
    Output:
        image_base64: Base64 encoded PNG with transparent background
    """
    image_b64 = input_data.get("image_base64")
    if not image_b64:
        return {"error": "No image_base64 provided"}
    
    image_bytes = base64.b64decode(image_b64)
    img = Image.open(io.BytesIO(image_bytes))
    
    model = input_data.get("model", "isnet-anime")
    use_matting = input_data.get("alpha_matting", False)
    
    session = REMBG_SESSION if model == "isnet-anime" else new_session(model)
    
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
    
    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    result_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return {"image_base64": result_b64}


# ============================================================================
# TOOL: ping - Health check
# ============================================================================
def ping_handler(input_data: dict) -> dict:
    """Simple health check."""
    return {"status": "ok", "tools": list(TOOLS.keys())}


# ============================================================================
# TOOL REGISTRY - Add new tools here
# ============================================================================
TOOLS = {
    "rembg": rembg_handler,
    "ping": ping_handler,
    # Future tools:
    # "upscale": upscale_handler,
    # "face_detect": face_detect_handler,
    # "composite": composite_handler,
}


# ============================================================================
# MAIN ROUTER
# ============================================================================
def handler(event):
    """
    Main RunPod serverless handler with tool routing.
    
    Input (event["input"]):
        tool: Tool name (default: "rembg")
        ... (tool-specific parameters)
    
    Output:
        Tool-specific output or error
    """
    try:
        input_data = event.get("input", {})
        tool_name = input_data.get("tool", "rembg")
        
        if tool_name not in TOOLS:
            return {"error": f"Unknown tool: {tool_name}. Available: {list(TOOLS.keys())}"}
        
        return TOOLS[tool_name](input_data)
    
    except Exception as e:
        return {"error": str(e)}


# Start RunPod serverless worker
runpod.serverless.start({"handler": handler})
