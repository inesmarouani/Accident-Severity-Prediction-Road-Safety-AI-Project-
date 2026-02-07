Bien sûr ! Voici le **README mis à jour**, sans la section **Methodology** et sans la partie **local development sans Docker**.

---

# 🚗 Accident Severity Prediction (Road Safety AI Project)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)
[![Docker%20Compose](https://img.shields.io/badge/Docker%20Compose-✓-blue.svg)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

---

## 📋 Table of Contents

* [Project Description](#-project-description)
* [Business Context](#-business-context)
* [Dataset](#-dataset)
* [Exploration & Notebook Steps](#-exploration--notebook-steps)
* [Results](#-results)
* [Prerequisites](#-prerequisites)
* [Project Structure](#-project-structure)
* [Deployment with Docker](#-deployment-with-docker)
* [Docker Hub](#-docker-hub)
* [Useful Commands](#-useful-commands)
* [Key Features](#-key-features)
* [Future Improvements](#-future-improvements)
* [License](#-license)
* [Contact](#-contact)

---

## 📖 Project Description

This project develops an AI model to predict the severity of road accidents based on accident circumstances (location, time, weather conditions, road type).
It includes model development, a REST API deployed with FastAPI, and an interactive dashboard built with Dash. The full stack is containerized with Docker and orchestrated using Docker Compose.

---

## 💼 Business Context

Road accidents are a major public safety issue with significant human, social, and economic costs. Manual analysis of accident data is complex and time-consuming.

**Automation via AI enables:**

* Better understanding of risk factors
* Prioritization of prevention measures
* Faster decision-making for road safety policies
* Improved emergency response allocation

---

## 📊 Dataset

### Data Source

Tabular accident data from France (2021–2024), combining multiple official datasets:

* Accident location and road type
* Time and date information
* Environmental conditions (weather, lighting, etc.)
* Accident context and circumstances
* Victim severity labels

### Data Characteristics

| Property     | Value                                      |
| ------------ | ------------------------------------------ |
| Period       | 2021–2024                                  |
| Observations | ~220,000 accidents                         |
| Features     | 50+ variables (after feature engineering)  |
| Target       | Binary severity (0: Non-severe, 1: Severe) |

---

## 🔎 Exploration & Notebook Steps

### 1. `accidents_routiers.ipynb`

**Data loading & initial exploration**

* Import and merge yearly CSV files
* Inspect data schema, missing values, and basic distributions

### 2. `EDA+feature engineering.ipynb`

**Feature engineering & preprocessing**

* Missing value treatment (drop columns with >70% missing)
* Encoding categorical variables
* Create aggregated features (`age_cat`, `nb_proteges`, `grav_accident`, etc.)
* EDA: correlations, temporal patterns, geographic distributions

### 3. `Modeling.ipynb`

**Model training & evaluation**

* Train XGBoost & LightGBM
* SHAP analysis for feature importance
* Hyperparameter tuning
* Evaluation (confusion matrix, ROC-AUC, classification report)

---

## 📈 Results

### Final Model (Binary Classification)

| Model        | Accuracy   | AUC      | Severe Recall |
| ------------ | ---------- | -------- | ------------- |
| **XGBoost**  | **72.95%** | **0.81** | 0.66          |
| **LightGBM** | **72.95%** | **0.81** | 0.67          |

**Key Insights:**

* Both models perform similarly
* Model is conservative (over-predicts severity), which is acceptable for safety
* Strong non-severe detection reduces false negatives

---

## 📦 Prerequisites

### For Docker deployment (recommended)

* Docker Desktop (includes Docker Compose)

---

## 📁 Project Structure

```
Accident-Severity-Prediction-Road-Safety-AI-Project/
│
├── back/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py
│   │   │   └── v1/
│   │   │       ├── api.py
│   │   │       └── endpoints/
│   │   │           └── accidents.py
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   ├── data/
│   ├── models_trained/
│   ├── migrations/
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
│
├── front/
│   ├── src/
│   │   ├── app.py
│   │   ├── assets/
│   │   ├── callbacks/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── services/
│   │   └── utils/
│   ├── data/
│   ├── Dockerfile
│   └── pyproject.toml
│
├── notebooks/
│   ├── accidents_routiers.ipynb
│   ├── EDA+feature engineering.ipynb
│   ├── Modeling.ipynb
│   └── data/
│
├── docker-compose.yml
├── README.md
├── .env.example
├── .gitignore
└── LICENSE
```

---

## 🐳 Deployment with Docker

### Architecture

```
front (Dash)  --->  back (FastAPI)  --->  db (Postgres)
   8050                8000               5432
```

### docker-compose.yml (production mode)

```yaml
services:
  db:
    image: postgres:13
    container_name: accident_severity_db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: accidents
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d accidents"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  back:
    image: inesmarouani/accident-back:latest
    container_name: accident_severity_back
    ports:
      - "8000:8000"
    environment:
      DB_USER: user
      DB_PASSWORD: password
      DB_NAME: accidents
      DB_HOST: db
      DB_PORT: 5432
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network

  front:
    image: inesmarouani/accident-front:latest
    container_name: accident_severity_front
    ports:
      - "8050:8050"
    environment:
      - API_BASE_URL=http://back:8000
      - DEBUG=False
    depends_on:
      - back
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
```

### Quick Start

```bash
git clone https://github.com/inesmarouani/accident-severity-prediction.git
cd Accident-Severity-Prediction-Road-Safety-AI-Project
cp .env.example .env
docker compose up
```

---

## 🏷️ Docker Hub

Images disponibles sur Docker Hub :

| Image                         | Tag      | Description     |
| ----------------------------- | -------- | --------------- |
| `inesmarouani/accident-back`  | `latest` | FastAPI backend |
| `inesmarouani/accident-front` | `latest` | Dash frontend   |

Pull:

```bash
docker pull inesmarouani/accident-back:latest
docker pull inesmarouani/accident-front:latest
```

---

## 🛠️ Useful Commands

### Start / Stop

| Command                     | Description                |
| --------------------------- | -------------------------- |
| `docker compose up --build` | Build + start all services |
| `docker compose up -d`      | Start in background        |
| `docker compose down`       | Stop and remove containers |
| `docker compose restart`    | Restart                    |

### Logs

| Command                     | Description       |
| --------------------------- | ----------------- |
| `docker compose logs`       | Logs all services |
| `docker compose logs back`  | Backend logs      |
| `docker compose logs front` | Frontend logs     |

---

## ✨ Key Features

* Full pipeline: data → preprocessing → model → API → dashboard
* SHAP interpretability
* Dockerized production deployment
* FastAPI + Dash + PostgreSQL

---

## 🔮 Future Improvements

* CI/CD pipeline for automatic build & push
* Monitoring (Prometheus/Grafana)
* Improved model calibration & ensemble methods
* More external data integration

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 📧 Contact

**Ines Marouani**

* Email: [ines.marouani69@gmail.com](mailto:ines.marouani69@gmail.com)
* GitHub: [@inesmarouani](https://github.com/inesmarouani)
* LinkedIn: [Ines Marouani](https://www.linkedin.com/in/ines-marouani-3016321b0/)

---

⭐ If you find this project useful, please consider giving it a star!
