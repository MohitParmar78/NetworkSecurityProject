# 🛡️ PhishGuard — Network Security Phishing Detection System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**A production-grade, end-to-end MLOps system for detecting phishing threats in network traffic.**

[🚀 Quick Start](#-getting-started) · [📐 Architecture](#️-architecture) · [🔌 API Reference](#-api-endpoints) · [🐳 Docker](#-running-with-docker)

</div>

---

## 📌 Overview

PhishGuard is a **fully automated, production-ready ML system** that classifies network connections as phishing or benign. Raw network features are ingested from MongoDB Atlas, processed through a modular MLOps pipeline (ingestion → validation → transformation → training → evaluation), and served via both a **FastAPI REST API** and a **Streamlit dashboard** — complete with experiment tracking, Docker deployment, and GitHub Actions CI/CD.

> Built to demonstrate full-stack MLOps engineering: from raw data to a live, monitored, containerised ML service.

---

## ✨ Key Features

| Feature | Details |
|---|---|
| 🔁 **Automated Training Pipeline** | Trigger full retraining via `GET /train` — no manual steps |
| 📊 **Experiment Tracking** | Every run logged to MLflow + DagsHub with metrics & artifacts |
| 🗄️ **Cloud Data Layer** | Raw phishing data ingested from and stored in MongoDB Atlas |
| 📁 **Bulk CSV Prediction** | Upload CSV → instant predictions rendered in UI and saved to disk |
| 🛡️ **Streamlit Dashboard** | Dark-themed, multi-page UI with threat visualisation and live inference |
| 🐳 **Docker Support** | Fully containerised — deploy anywhere with a single command |
| ⚙️ **GitHub Actions CI/CD** | Automated lint, test, build, and deploy on every push to `main` |
| 🧪 **Schema Validation** | Data schema enforced before training begins — catches drift early |
| 🔒 **Centralised Exception Handling** | Custom exception + logging layer across all pipeline stages |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      PhishGuard System                          │
│                                                                 │
│  MongoDB Atlas  ──►  Data Ingestion  ──►  Data Validation       │
│                                                  │              │
│                                                  ▼              │
│                             Data Transformation (sklearn pipe)  │
│                                                  │              │
│                                                  ▼              │
│                             Model Training  ──►  Evaluation     │
│                                                  │              │
│                              MLflow / DagsHub ◄──┘              │
│                                                  │              │
│                                         final_model/            │
│                                    model.pkl + preprocessor.pkl │
│                                                  │              │
│                         ┌───────────────┬─────────┴──────────┐  │
│                         ▼               ▼                     │  │
│                    FastAPI REST    Streamlit UI                │  │
│                    /train /predict  Dashboard                  │  │
│                         │                                      │  │
│                    Docker Container ◄── GitHub Actions CI/CD   │  │
└─────────────────────────────────────────────────────────────────┘
```

### ML Pipeline Stages

```
MongoDB  →  [1] Data Ingestion  →  [2] Data Validation  →  [3] Data Transformation
                                                                      ↓
                                               [5] Model Evaluation  ←  [4] Model Training
                                                      ↓
                                              final_model/model.pkl
                                           final_model/preprocessor.pkl
```

---

## 🗂️ Project Structure

```
NetworkSecurityProject/
│
├── networksecurity/                 # Core installable package
│   ├── components/                  # Pipeline stage implementations
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── model_evaluation.py
│   ├── pipeline/
│   │   └── training_pipeline.py     # Orchestrates all 5 stages
│   ├── utils/
│   │   ├── main_utils/utils.py      # load_object, save_object helpers
│   │   └── ml_utils/model/estimator.py  # NetworkModel wrapper
│   ├── exception/exception.py       # Custom exception class
│   ├── logging/logger.py            # Centralised logger
│   └── constant/training_pipeline.py  # DB names, paths, constants
│
├── .github/workflows/               # GitHub Actions CI/CD workflows
├── Network_Data/                    # Raw phishing dataset (CSV)
├── data_schema/                     # Schema YAML for validation
├── valid_data/                      # Output of validation stage
├── prediction_output/               # Saved prediction CSVs
├── templates/                       # Jinja2 HTML for FastAPI results
│
├── app.py                           # FastAPI application (train + predict)
├── streamlit_app.py                 # Streamlit dashboard (UI)
├── main.py                          # CLI entry point for pipeline
├── push_data.py                     # Push raw CSV data to MongoDB
├── Dockerfile                       # Container definition
├── requirements.txt                 # Python dependencies
└── setup.py                         # Package setup
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **ML / Data** | `scikit-learn`, `pandas`, `numpy`, `dill` |
| **Experiment Tracking** | `mlflow`, `dagshub` |
| **REST API** | `FastAPI`, `uvicorn`, `python-multipart` |
| **UI Dashboard** | `Streamlit` |
| **Database** | `pymongo`, `certifi` (MongoDB Atlas) |
| **DevOps** | `Docker`, GitHub Actions |
| **Config** | `python-dotenv`, `pyaml` |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/MohitParmar78/NetworkSecurityProject.git
cd NetworkSecurityProject
```

### 2. Set up environment variables

Create a `.env` file in the root:

```env
MONGODB_URL_KEY=mongodb+srv://<username>:<password>@cluster.mongodb.net/
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Push raw data to MongoDB (first run only)

```bash
python push_data.py
```

### 5a. Run the Streamlit Dashboard

```bash
streamlit run streamlit_app.py
# → http://localhost:8501
```

### 5b. Run the FastAPI application

```bash
python app.py
# → http://localhost:8000/docs (Swagger UI)
```

---

## 🐳 Running with Docker

```bash
# Build the image
docker build -t phishguard .

# Run the container
docker run -p 8000:8000 --env-file .env phishguard
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Redirects to `/docs` (Swagger UI) |
| `GET` | `/train` | Triggers the full ML training pipeline |
| `POST` | `/predict` | Upload CSV → returns HTML table with predictions |

### Example: Predict via cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@your_network_data.csv"
```

The response is a styled HTML table with a `predicted_column` appended (`1` = benign, `-1` = phishing). Results are also saved to `prediction_output/output.csv`.

---

## 📈 Experiment Tracking

Integrates with **DagsHub + MLflow** for full experiment lifecycle management. Each training run logs:

- **Parameters** — model hyperparameters
- **Metrics** — accuracy, F1-score, precision, recall
- **Artifacts** — trained model and preprocessor objects
- **Auto-promotion** — model is promoted to `final_model/` only if it outperforms the current baseline

Set up DagsHub credentials in your environment to enable remote tracking.

---

## 🔄 CI/CD Pipeline

GitHub Actions workflows in `.github/workflows/` handle:

| Workflow | Trigger | Action |
|---|---|---|
| **CI** | Every push / PR | Lint, unit tests, import checks |
| **CD** | Merge to `main` | Build Docker image, push to registry, deploy |

---

## 📋 Data Schema

The model expects **30 numeric network features** including:

`having_IP_Address`, `URL_Length`, `Shortining_Service`, `having_At_Symbol`, `double_slash_redirecting`, `Prefix_Suffix`, `having_Sub_Domain`, `SSLfinal_State`, `Domain_registeration_length`, `Favicon`, `port`, `HTTPS_token`, `Request_URL`, `URL_of_Anchor`, `Links_in_tags`, `SFH`, `Submitting_to_email`, `Abnormal_URL`, `Redirect`, `on_mouseover`, `RightClick`, `popUpWidnow`, `Iframe`, `age_of_domain`, `DNSRecord`, `web_traffic`, `Page_Rank`, `Google_Index`, `Links_pointing_to_page`, `Statistical_report`

**Target:** `-1` = Phishing, `1` = Benign

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open source. See the repository for details.

---

<div align="center">

Built with ❤️ by [Mohit Parmar](https://github.com/MohitParmar78)

⭐ Star this repo if you found it useful!

</div>
