FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install CPU-only PyTorch
RUN pip install --no-cache-dir --default-timeout=1000 \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.7.1

# Install Transformers separately
RUN pip install --no-cache-dir --default-timeout=1000 \
    transformers==4.52.4

# Install remaining dependencies
RUN pip install --no-cache-dir --default-timeout=1000 \
    -r requirements.txt \
    --extra-index-url https://pypi.org/simple

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]