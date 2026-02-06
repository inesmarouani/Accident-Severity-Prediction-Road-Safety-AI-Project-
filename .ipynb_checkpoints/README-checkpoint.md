# 🚗 Accident Severity Prediction (Road Safety AI Project)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

## 📋 Table of Contents
- [Project Description](#-project-description)
- [Business Context](#-business-context)
- [Dataset](#-dataset)
- [Methodology](#-methodology)
- [Results](#-results)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 📖 Project Description

This project develops an artificial intelligence model to predict the severity of road accidents based on accident circumstances (location, time, weather conditions, road type). The complete solution includes model development, REST API deployment, and an interactive web dashboard.

### Problem Statement
Develop a model capable of predicting accident severity based on its circumstances:

📍 Location (urban/rural, department, road type)
⏰ Temporal factors (hour, day, season)
🌤️ Atmospheric conditions (weather, lighting)
🛣️ Road characteristics (type, surface, infrastructure)

### Objectives

Build a high-performing binary classification model
Deploy the model via a REST API (FastAPI)
Create an interactive web interface for visualization and prediction (Dash)

### Deliverables

✅ ML Model: Binary classification (Non-severe vs. Severe) with 73% accuracy, 0.81 AUC

✅ REST API: FastAPI backend for real-time predictions

✅ Web Dashboard: Dash application with:
Interactive data visualizations,
Real-time prediction interface,

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
- **Period:** 2021-2024
- **Total Observations:** ~220,000 accidents
- **Features:** 50+ variables (after feature engineering)
- **Target Variable:** Binary classification (0: Non-severe, 1: Severe)

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
  ```
  nb_proteges, nbv, vma, lum, saison,
  localisation, trajet, age, is_passagers,
  circ, nb_usagers, atm, agg, col, situ
  ```

### 5. Model Training
**Models Tested:**
- XGBoost
- LightGBM

**Training Pipeline:**
1. ColumnTransformer encoding (OneHotEncoder for categorical, passthrough for numerical)
2. Train/test split (80/20)
3. Sample weighting to handle class imbalance
4. Hyperparameter tuning
5. Cross-validation

**Evaluation Strategy:**
- Classification reports (precision, recall, F1-score per class)
- Confusion matrices
- ROC curves (One-vs-Rest for multiclass, binary for final model)
- AUC scores

---

## 📈 Results

### Multiclass Classification (Initial Approach)
**Performance (3 classes: 0, 1, 2):**
- Overall Accuracy: **63%**
- Class 0 (Non-severe): Precision=0.85, Recall=0.73, F1=0.78, AUC=0.81
- Class 1 (Moderate): Precision=0.49, Recall=0.44, F1=0.47, AUC=0.73
- Class 2 (Severe): Precision=0.19, Recall=0.59, F1=0.29, AUC=0.83

**Challenge:** Classes 1 and 2 showed poor performance due to imbalance and similar explanatory factors.

---

### Binary Classification (Final Approach)
**Decision Rationale:**
1. ✅ Operational objective: Detect severe accidents (1 or 2) vs. non-severe (0)
2. ✅ SHAP analysis showed Classes 1 and 2 share similar drivers
3. ✅ Simplifies model while maintaining practical value

**Final Performance:**

| Model | Accuracy | Class | Precision | Recall | F1-Score | AUC |
|-------|----------|-------|-----------|--------|----------|-----|
| **XGBoost** | **72.95%** | Non-severe | 0.80 | 0.76 | 0.78 | **0.81** |
|  |  | Severe | 0.60 | 0.66 | 0.63 |  |
| **LightGBM** | **72.95%** | Non-severe | 0.80 | 0.76 | 0.78 | **0.81** |
|  |  | Severe | 0.61 | 0.67 | 0.63 |  |

**Interpretation:**
- ✅ Models correctly classify **~73%** of cases
- ✅ Strong performance on non-severe class (F1=0.78)
- ✅ Detects **~67%** of severe cases (recall=0.67)
- ⚠️ Moderate precision for severe class (0.60-0.61) → some false alarms
- ✅ AUC of 0.81 indicates good discriminative ability

**Key Insights:**
- Both models perform identically (XGBoost ≈ LightGBM)
- Model tends to over-predict severity (conservative approach, acceptable for safety applications)
- Strong non-severe detection ensures low false negative rate for critical cases

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Clone Repository
```bash
git clone https://github.com/yourusername/accident-severity-prediction.git
cd accident-severity-prediction
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

**Required Libraries:**
```
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
xgboost>=1.5.0
lightgbm>=3.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
plotly>=5.3.0
shap>=0.40.0
missingno>=0.5.0
```

---

## 🏗️ Deployment Architecture


┌─────────────────────────────────────────────────────────────┐
│                        User Interface                       │
│                     (Web Browser)                           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    Dash Dashboard (Port 8050)               │
│  ┌──────────────────────┐    ┌─────────────────────────┐    │
│  │  Visualization Tab   │    │    Prediction Tab       │    │
│  │  - Maps              │    │    - Input Form         │    │
│  │  - Charts            │    │    - Real-time Results  │    │
│  │  - Metrics           │    │    - Explanations       │    │
│  └──────────────────────┘    └─────────────────────────┘    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI REST API (Port 8000)               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Endpoints:                                          │   │
│  │  - POST /predict (single)                            │   │
│  │  - POST /predict/batch                               │   │
│  │  - GET /model/info                                   │   │
│  │  - GET /health                                       │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                     ML Model Layer                           │
│  ┌──────────────────┐         ┌──────────────────────┐      │
│  │  XGBoost Model   │         │  Preprocessor        │      │
│  │  (.pkl)          │ ◄─────► │  (ColumnTransformer) │      │
│  └──────────────────┘         └──────────────────────┘      │
└─────────────────────────────────────────────────────────────┘

## Technology Stack
### Backend:

🔹 FastAPI - Modern, fast API framework
🔹 Uvicorn - ASGI server for production
🔹 Pydantic - Data validation

### Frontend:

🔹 Dash/Plotly - Interactive web applications
🔹 Bootstrap - Responsive UI components

### ML/Data:

🔹 XGBoost/LightGBM - Gradient boosting models
🔹 Scikit-learn - Preprocessing pipeline
🔹 SHAP - Model interpretability
🔹 Pandas/NumPy - Data manipulation

### Deployment:


## 📁 Project Structure

```
accident-severity-prediction/
│
├── back/
│   ├── models/
│   │   ├── label_encoder.pkl
│   │   ├── pipeline.pkl
│   │   ├── pipeline_binaire.pkl
│   │   └── label_encoder_binaire.pkl
│   ├── Dockerfile
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
├── data/                  # CSV source
│   ├── carac-2021.csv
│   ├── lieux-2021.csv
│   └── ...
│
├── notebooks/
│   ├── data_cleaning.ipynb
│   ├── EDA+feature_engineering.ipynb
│   ├── Modeling.ipynb
│
├── docker-compose.yml
├── README.md
└── .gitignore
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

### 5. Production-Ready
- Modular code structure
- Reusable preprocessing pipeline
- Model serialization for deployment
---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Project Maintainer:** [Your Name]
- Email: ines.marouani69@gmail.com
- GitHub: [@inesmarouani](https://github.com/inesmarouani)
- LinkedIn: [Your LinkedIn]([https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/ines-marouani-3016321b0/))

**Project Link:** [https://github.com/yourusername/accident-severity-prediction](https://github.com/yourusername/accident-severity-prediction)

---

## 🙏 Acknowledgments

- French Road Safety Data provided by [Data Source]
- SHAP library for model interpretability
- XGBoost and LightGBM teams for excellent gradient boosting implementations
- Open-source community for tools and libraries

---

**⭐ If you find this project useful, please consider giving it a star!**
