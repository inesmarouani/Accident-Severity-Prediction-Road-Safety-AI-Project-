# 🚗 Accident Severity Prediction (Road Safety AI Project)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)
[![Docker%20Compose](https://img.shields.io/badge/Docker%20Compose-✓-blue.svg)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

---

## 📋 Table of Contents
- [Project Description](#-project-description)
- [Business Context](#-business-context)
- [Dataset](#-dataset)
- [Methodology](#-methodology)
- [Results](#-results)
- [Prerequisites](#-prerequisites)
- [Project Structure](#-project-structure)
- [Deployment with Docker](#-deployment-with-docker)
- [Docker Hub](#-docker-hub)
- [Useful Commands](#-useful-commands)
- [Usage without Docker](#-usage-without-docker)
- [Key Features](#-key-features)
- [License](#-license)
- [Contact](#-contact)

---

## 📖 Project Description

This project develops an artificial intelligence model to predict the severity of road accidents based on accident circumstances (location, time, weather conditions, road type). The complete solution includes model development, a REST API deployed via FastAPI, and an interactive web dashboard built with Dash. The entire application is containerized with Docker and orchestrated with Docker Compose.

### Problem Statement
Develop a model capable of predicting accident severity based on its circumstances:

- 📍 Location (urban/rural, department, road type)
- ⏰ Temporal factors (hour, day, season)
- 🌤️ Atmospheric conditions (weather, lighting)
- 🛣️ Road characteristics (type, surface, infrastructure)

### Objectives

- Build a high-performing binary classification model
- Deploy the model via a REST API (FastAPI)
- Create an interactive web interface for visualization and prediction (Dash)
- Containerize and orchestrate the full stack with Docker Compose

### Deliverables

- ✅ **ML Model:** Binary classification (Non-severe vs. Severe) with 73% accuracy, 0.81 AUC  
- ✅ **REST API:** FastAPI backend for real-time predictions + PostgreSQL logging  
- ✅ **Web Dashboard:** Dash application with interactive visualizations and real-time prediction  
- ✅ **Dockerized Deployment:** Full stack running with a single `docker-compose up`

---

## 💼 Business Context

Road accidents represent a major public safety issue with significant human, social, and economic costs. Manual analysis of accident data is complex and time-consuming.

**Automation via AI enables:**
- ✅ Better understanding of risk factors
- ✅ Prioritization of prevention measures
- ✅ Faster decision-making for road safety policies
- ✅ Improved emergency response allocation

---

## 📊 Dataset

### Data Source
The project uses **tabular accident data from France (2021-2024)**, combining multiple official datasets:
- Accident location and road type
- Time and date information
- Environmental conditions (weather, lighting, etc.)
- Accident context and circumstances
- Victim severity labels

### Data Characteristics
| Property | Value |
|---|---|
| Period | 2021–2024 |
| Total Observations | ~220,000 accidents |
| Features | 50+ variables (after feature engineering) |
| Target Variable | Binary classification (0: Non-severe, 1: Severe) |

### Class Distribution
- **Non-severe accidents (Class 0):** ~140,000 (64%)
- **Severe accidents (Class 1+2):** ~80,000 (36%)

---

## 🔬 Methodology

### 1. Data Collection and Loading
- Import multi-year CSV files (2021-2024)
- Utility functions for schema extraction and concatenation
- Inner join on common columns across years
- Standardization of missing value codes (-1 → NaN)

### 2. Data Preprocessing

**Missing Value Handling:**
- Visualization using `missingno` matrices
- Removal of columns with >70% missing data
- Type conversion and normalization (lat/long, categorical encodings)

**Feature Engineering:**
- Aggregation at accident level (from user-level data)
- Creation of derived features:
  - `age_cat`: Age binning into 5 categories
  - `nb_proteges`: Protected road users count
  - Role indicators: `is_conducteur`, `is_passager`, `is_pieton`
  - Gender indicators: `is_femme`, `is_homme`
  - `grav_accident`: Binary severity target (merged classes 1 and 2)

### 3. Exploratory Data Analysis (EDA)
- Univariate distributions (histograms, boxplots)
- Correlation analysis (heatmap for numerical features)
- Geographic distribution analysis (France map visualization)
- Temporal patterns (weekend vs. weekday, seasonal effects)
- Categorical feature analysis vs. severity

**Key EDA Findings:**
- Strong predictors: `nb_usagers`, `localisation_pieton`, `trajet`, `col`, `catr`
- Moderate predictors: `circ`, `agg`, `lum`, `dep`
- Weak predictors: Road infrastructure features (low variance)
- Geographic patterns: Urban centers show higher accident density
- Temporal patterns: Weekdays have 2-3x more accidents than weekends

### 4. Feature Selection

**SHAP-based Feature Importance:**
- Analysis revealed that Classes 1 and 2 share similar drivers
- Justification for merging into binary classification
- Selection of 15 most important features:
  - `nb_proteges`, `nbv`, `vma`, `lum`, `saison`, `localisation_pieton`, `trajet`, `age_cat`, `is_passagers`, `circ`, `nb_usagers`, `atm`, `agg`, `col`, `situ`

### 5. Model Training

**Models Tested:** XGBoost, LightGBM

**Training Pipeline:**
1. ColumnTransformer encoding (OneHotEncoder for categorical, passthrough for numerical)
2. Train/test split (80/20)
3. Sample weighting to handle class imbalance
4. Hyperparameter tuning


**Evaluation Strategy:**
- Classification reports (precision, recall, F1-score per class)
- Confusion matrices
- ROC curves
- AUC scores

---

## 📈 Results

### Binary Classification (Final Approach)

**Decision Rationale:**
1. ✅ Operational objective: Detect severe accidents (1 or 2) vs. non-severe (0)
2. ✅ SHAP analysis showed Classes 1 and 2 share similar drivers
3. ✅ Simplifies model while maintaining practical value

**Final Performance:**

| Model | Accuracy | Class | Precision | Recall | F1-Score | AUC |
|---|---|---|---|---|---|---|
| **XGBoost** | **72.95%** | Non-severe | 0.80 | 0.76 | 0.78 | **0.81** |
| | | Severe | 0.60 | 0.66 | 0.63 | |
| **LightGBM** | **72.95%** | Non-severe | 0.80 | 0.76 | 0.78 | **0.81** |
| | | Severe | 0.61 | 0.67 | 0.63 | |

**Key Insights:**
- Both models perform identically (XGBoost ≈ LightGBM)
- Model tends to over-predict severity (conservative approach, acceptable for safety applications)
- Strong non-severe detection ensures low false negative rate for critical cases

---

## 📦 Prerequisites

### For Docker deployment (recommended)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (includes Docker Compose)

### For local development (without Docker)
- Python 3.8+
- pip or conda

---

## 📁 Project Structure

```
Accident-Severity-Prediction-Road-Safety-AI-Project/
│
├── back/
│   ├── models/
│   │   ├── label_encoder.pkl
│   │   ├── pipeline.pkl
│   │   ├── pipeline_binaire.pkl
│   │   └── label_encoder_binaire.pkl
│   ├── Dockerfile
│   ├── database.py
│   ├── models.py
│   ├── main.py
│   └── requirements.txt
│
├── front/
│   ├── data/
│   │   └── accidents_clean.csv
│   ├── Dockerfile
│   ├── dash_app.py
│   └── requirements.txt
│
│
│
├── notebooks/
│   ├── data_cleaning.ipynb
│   ├── EDA+feature_engineering.ipynb
│   ├── Modeling.ipynb
│   └── data/                  # CSV source
│     ├── carac-2021.csv
│     ├── lieux-2021.csv
│     └── ...
│
├── docker-compose.yml
├── README.md
├── .env.example
├── .dockerignore
└── .gitignore
```

---

## 🐳 Deployment with Docker

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Docker Compose                     │
│                                                     │
│  ┌─────────────────┐       ┌──────────────────┐    │
│  │   front          │       │   back            │    │
│  │  (Dash)          │ HTTP  │  (FastAPI)        │    │
│  │  Port 8050       │──────>│  Port 8000        │    │
│  │                  │       │  + PostgreSQL DB  │    │
│  └─────────────────┘       └──────────────────┘    │
│          │                         │                │
│          └────────────────────────┘                 │
│                  app-network                        │
└─────────────────────────────────────────────────────┘
```

### docker-compose.yml

```yaml
version: "3.8"

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
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d accidents"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - app-network
  back:
    #build:
      #context: ./back
      #dockerfile: Dockerfile
    container_name: accident_severity_back
    image: inesmarouani/accident-back:latest
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
    volumes:
      - ./back/data:/app/data   # dossier partagé entre hôte et conteneur
    networks:
      - app-network

  front:
    #build:
      #context: ./front
      #dockerfile: Dockerfile
    container_name: accident_severity_front
    image: inesmarouani/accident-front:latest
    ports:
      - "8050:8050"
    depends_on:
      - back
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  db_data:
```

### Quick Start

**1. Clone the repository:**
```bash
git clone https://github.com/inesmarouani/accident-severity-prediction.git
cd Accident-Severity-Prediction-Road-Safety-AI-Project
```

**2. Copy and configure environment file:**
```bash
cp .env.example .env
# Edit .env and set DB_USER, DB_PASSWORD, DB_NAME if needed
```

> PostgreSQL is defined as a service in docker-compose.yml; the DB_* variables in `.env` are used by the backend.

**3. Build and start containers:**
```bash
docker-compose up --build
```

**4. (Optional) Initialize or inspect the PostgreSQL database:**
- Connect to the Postgres container:
```bash
docker exec -it accident_severity_db psql -U $POSTGRES_USER -d $POSTGRES_DB
# psql> \dt   # list tables
# psql> SELECT count(*) FROM accident;
```
- Import a SQL script from the host:
```bash
docker exec -i accident_severity_db psql -U $POSTGRES_USER -d $POSTGRES_DB < back/init.sql
```

**5. Access services:**

| Service | URL |
|---|---|
| Dashboard (Dash) | http://localhost:8050 |
| API REST (FastAPI) | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## 🏷️ Docker Hub

Les images sont disponibles sur Docker Hub :

| Image | Tag | Description |
|---|---|---|
| `inesmarouani/accident-back` | `latest` | FastAPI + modèle ML + SQLite |
| `inesmarouani/accident-front` | `latest` | Dashboard Dash |

**Pull depuis Docker Hub :**
```bash
docker pull inesmarouani/accident-back:latest
docker pull inesmarouani/accident-front:latest
```

---

## 🛠️ Useful Commands

### Start / Stop

| Command | Description |
|---|---|
| `docker-compose up --build` | Build + start all services |
| `docker-compose up -d` | Start in background (detached) |
| `docker-compose down` | Stop and remove containers |
| `docker-compose restart` | Restart without rebuilding |

### Logs & Monitoring

| Commande | Description |
|---|---|
| `docker-compose logs` | Affiche les logs de tous les services |
| `docker-compose logs back` | Logs du backend uniquement |
| `docker-compose logs front` | Logs du frontend uniquement |
| `docker-compose logs -f back` | Logs en temps réel (`-f` = follow) |
| `docker ps` | Liste les conteneurs en cours d'exécution |

### Inspection des conteneurs

| Commande | Description |
|---|---|
| `docker exec -it accident_severity_back bash -c "ls -la /app"` | Lister les fichiers du back |
| `docker exec -it accident_severity_back bash -c "find /app -type f"` | Tous les fichiers récursivement |
| `docker network inspect app-network` | Vérifier le réseau partagé |

### Check PostgreSQL database

- Connect to the Postgres container:
```bash
docker exec -it accident_severity_db psql -U $POSTGRES_USER -d $POSTGRES_DB
# psql> \dt   # list tables
# psql> SELECT count(*) FROM accident;
```

- Export the DB from the container to the host:
```bash
docker exec -t accident_severity_db pg_dump -U $POSTGRES_USER $POSTGRES_DB > ./backup_${POSTGRES_DB}.sql
```

- Import a dump from the host into the container:
```bash
cat ./backup.sql | docker exec -i accident_severity_db psql -U $POSTGRES_USER -d $POSTGRES_DB
```

- Check health and connectivity:
```bash
docker-compose logs db
docker exec -it accident_severity_db pg_isready -U $POSTGRES_USER -d $POSTGRES_DB
```

### Docker Network

If the front cannot reach the back, check if the network exists:
```bash
docker network inspect app-network
```

If absent, re-trigger a full build:
```bash
docker-compose down
docker-compose up --build
```

---

## 🖥️ Usage without Docker

### Installation
```bash
pip install -r back/requirements.txt
pip install -r front/requirements.txt
```

### Démarrer le backend
```bash
cd back
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Démarrer le frontend
Dans un autre terminal, et en remplaçant l'URL du backend par `http://localhost:8000` dans `dash_app.py` :
```bash
cd front
python dash_app.py
```

---

## ✨ Key Features

### 1. Comprehensive Data Pipeline
- Multi-year data aggregation (2021-2024)
- Robust missing value handling
- Feature engineering at accident level

### 2. Advanced Feature Selection
- SHAP-based feature importance
- Reduction to 15 key predictive features
- Removal of low-variance features

### 3. Model Performance
- 73% accuracy on binary classification
- 81% AUC-ROC score
- 67% recall on severe accident detection

### 4. Interpretability
- SHAP analysis for feature importance
- Clear business-oriented explanations
- Actionable insights for road safety policies

### 5. Production-Ready Deployment
- Fully containerized with Docker
- Orchestrated with Docker Compose
- Shared network between services
- Persistent PostgreSQL database via volume mount
- Healthchecks on containers

---

## 🔮 Future Improvements

### Model Enhancement
- [ ] Threshold tuning to optimize precision/recall trade-off
- [ ] Test ensemble methods (stacking, voting)
- [ ] Explore CatBoost and other gradient boosting variants
- [ ] Implement focal loss for better class imbalance handling

### Feature Engineering
- [ ] Add temporal features (hour of day, rush hour indicator)
- [ ] Create interaction features (agg × vma, lum × atm)
- [ ] Include external data (population density, traffic volume)
- [ ] Geospatial features (distance to hospital, road quality index)

### Deployment
- [ ] Migrate SQLite to PostgreSQL for production (if any local SQLite artifacts remain)
- [ ] Add monitoring (Prometheus + Grafana)
- [ ] CI/CD pipeline for automatic image rebuilds
- [ ] Cloud deployment (AWS / GCP / Azure)

### Analysis
- [ ] Deep dive into false positives/negatives
- [ ] Regional analysis (department-level patterns)
- [ ] Temporal trends analysis (year-over-year changes)
- [ ] Cost-benefit analysis of prevention measures

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation accordingly
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Project Maintainer:** Ines Marouani
- Email: ines.marouani69@gmail.com
- GitHub: [@inesmarouani](https://github.com/inesmarouani)
- LinkedIn: [Ines Marouani](https://www.linkedin.com/in/ines-marouani-3016321b0/)

---

## 🙏 Acknowledgments

- French Road Safety Data (official datasets 2021-2024)
- SHAP library for model interpretability
- XGBoost and LightGBM teams for gradient boosting implementations
- Open-source community for tools and libraries

---

**⭐ If you find this project useful, please consider giving it a star!**