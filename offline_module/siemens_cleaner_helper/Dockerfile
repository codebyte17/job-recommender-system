FROM python:3.10

WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN pip install --upgrade pip

# install PyTorch + CUDA (MANUAL, correct way)
RUN pip install --no-cache-dir \
    torch==2.5.1+cu121 \
    torchvision==0.20.1+cu121 \
    torchaudio==2.5.1+cu121 \
    --index-url https://download.pytorch.org/whl/cu121

# install the rest of your dependencies
COPY ../requirements.txt .

# IMPORTANT: remove torch from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# spaCy model
RUN python -m spacy download en_core_web_sm

# copy code
COPY .. .

CMD ["python", "jobs_cleaner.py"]