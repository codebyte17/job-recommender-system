# Job Recommendation System

An end-to-end job recommendation platform that automates job collection, data preprocessing, candidate profile generation, evaluation, and deployment.

The project consists of multiple independent modules, each responsible for a different stage of the recommendation pipeline.

For the final Job recommendation application : [Job Recommender](https://github.com/codebyte17/job-recommender-system/blob/main/job-recommendation-app/README.md)

---

# Table of Contents

- [Overview](#overview)
- [Project Architecture](#project-architecture)
- [Repository Structure](#repository-structure)
- [Project Modules](#project-modules)
  - [1. Data Collection](#1-data-collection)
  - [2. Data Preparation](#2-data-preparation)
  - [3. Offline Processing](#3-offline-processing)
  - [4. Datasets](#4-datasets)
  - [5. Recommendation Experiments](#5-recommendation-experiments)
  - [6. Utilities](#6-utilities)
  - [7. Application](#7-application)
- [Project Workflow](#project-workflow)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [License](#license)

---

# Project Modules

## 1. Data Collection

The **Data Collection** module is responsible for collecting/Scrapping job postings from multiple company career portals. Each supported company has its own scraper implementation that extracts job information and stores it in a standardized format **(MongoDB)** for downstream processing.

### Responsibilities

- Automated job scraping
- Company-specific scrapers
- Job Fields Extraction
- Database integration
- Incremental data collection

**Supported Companies**

- Siemens
- Mercedes-Benz

**Documentation**

```
jobs_scraper/README.md
```

---

## 2. Data Preparation

The initial stage of the recommendation pipeline focuses on transforming raw scraped data into structured datasets suitable for downstream processing. This module contains notebooks **(Experiments/notebooks)** used for exploratory analysis, preprocessing, feature preparation, and data validation.

these notebooks are dedicated to preparing the data rather than Embeddings generation or evaluating models.

### Responsibilities

- Data preprocessing
- Data cleaning
- Exploratory analysis
- Feature preparation
- Dataset validation

Note: some heavy preprocessing has done in the **offline_module** on BHT Cluster.
**Documentation**

```
experiments/README.md
```

---

## 3. Offline Processing

The Offline Processing module performs large-scale data transformation on a BHT cluster. It contains the preprocessing of Siemens jobs heavily irrelevant informations, Synthetic CVS  and Evaluation ground Truth generation.


### Responsibilities

- Cluster-based data cleansing
- Synthetic CV generation
- Ground truth generation
- Data transformation
- Dataset enrichment

The output of this module helps in the further data preparation, final Embeddings generation and Evaluation.

**Documentation**

```
offline_module/README.md
```

---

## 4. Datasets

This module stores all datasets produced throughout the pipeline.

### Structure

```
datasets/
├── raw/
├── processed/
└── evaluation/
```

Contains:

- Raw scraped jobs
- Processed datasets
- Ground truth datasets
- Evaluation datasets

---

## 5. Recommendation Experiments

After the datasets have been prepared, the recommendation experiments module **(Experiments/evaluation)** focuses on Embeddings generations, Re-Ranker Hyper parameters tuning with **Sweep** and Tracking in **Wandb**.

This module contains research code for generating embeddings, optimizing retrieval performance, and evaluating recommendation quality.Furthermore, storing the final Embeddings Vectors along with payloads on **Qdrant** VectorDB.

### Responsibilities

- Embedding generation
- Vector Database Integration (Qdrant)
- Similarity search
- Hybrid ReRanking
- Hyperparameter tuning
- Offline evaluation
- Weight and Biases for Evaluation Tracking

Evaluation metrics include:

- Precision@K
- Recall@K
- NDCG

**Documentation**

```
experiments/README.md
```

---

## 6. Utilities

Its primary responsibility is supporting the data preparation pipeline, particularly through the Skills Named Entity Recognition (Skills NER) system used during data transformation.

Final MongoDB data loading is also implemented here so that the end Software development Module used the Clean and transformed jobs data.
### Responsibilities

- Skills NER extraction
- Database utilities (Load the final Integrated Dataset which contains jobs of many companies)


---

## 7. Application

The Application module provides the production interface for serving personalized job recommendations.

It exposes the recommendation engine through APIs and integrates all components of the pipeline into a deployable system.

### Features

- REST APIs
- Recommendation service
- User Interface
- Uploading CV
- Production deployment
- Asynch Operation through Redis and Celery.

**Documentation**

```
job-recommendation-app/README.md
```


# Technologies Used

- Python
- Playwright
- BeautifulSoup
- FastAPI
- MongoDB
- Pymongo
- Pandas
- NumPy
- Sentence Transformers
- Scikit-learn
- Qdrant
- Docker
- Redis
- Celery
- Pytorch
- Weight and Biases
- Spacy
- Streamlit
- Kubernetes
- Ollama

---



# Documentation

| Module | Documentation |
|----------|---------------|
| Data Scraping | jobs_scraper/README.md |
| Offline Module | offline_module/README.md |
| Experiments | experiments/README.md |
| Datasets | datasets/README.md |
| Recommendation App | job-recommendation-app/README.md |
| Utilities | utils/README.md |

---

# License

This project is licensed under the MIT License.
