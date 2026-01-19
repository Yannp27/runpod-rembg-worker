FROM python:3.12-slim

WORKDIR /app

# Install rembg with GPU support
RUN pip install --no-cache-dir runpod "rembg[gpu]" pillow

# Pre-download models during build
RUN python -c "from rembg import new_session; new_session('isnet-anime'); print('Model cached')"

COPY handler.py .

CMD ["python", "-u", "handler.py"]
