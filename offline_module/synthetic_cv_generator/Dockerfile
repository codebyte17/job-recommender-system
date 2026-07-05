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
RUN pip install pandas numpy requests

# copy code + dataset
COPY cv_generator.py .
COPY input/sample_integrated_cleaned.v2.csv .

# output directory (PVC mount)
RUN mkdir -p /output

CMD ["python", "cv_generator.py"]