# RunPod Serverless Multi-Tool Worker for Image Processing
# Based on NVIDIA CUDA for GPU inference with ONNX Runtime

FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python 3.11 and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Use python3.11 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Install core packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    runpod \
    pillow \
    numpy \
    onnxruntime-gpu \
    rembg

# Pre-download models during build (eliminates cold-start latency)
RUN python -c "from rembg import new_session; new_session('isnet-anime'); print('isnet-anime model cached')"

# Copy handler
COPY handler.py .

CMD ["python", "-u", "handler.py"]
