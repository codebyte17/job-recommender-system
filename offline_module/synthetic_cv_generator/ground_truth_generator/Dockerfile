FROM python:3.11-slim

WORKDIR /app

# system dependencies (for pandas/numpy)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN pip install --upgrade pip

# install python dependencies (FIXED)
RUN pip install pandas numpy requests aiohttp tqdm

# copy code + dataset
COPY ./ground_truth_generation.py .
COPY input/dfsample_with_cvs.csv .

# output directory (PVC mount)
RUN mkdir -p /output

CMD ["python", "ground_truth_generation.py"]