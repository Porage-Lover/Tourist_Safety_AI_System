# Modular AI System for Intelligent Tourist Safety

This project implements the backend AI and ML services for the "Smart Tourist Safety Monitoring & Incident Response System". It is designed as a modular, scalable suite of microservices.

## Core Features & Modules

1.  **Data Ingestion Service (`services/data_ingestion.py`)**
2.  **Geospatial Risk Service (`services/geospatial_risk.py`)**
3.  **Behavioral Anomaly Service (`services/behavioral_anomaly.py`)**
4.  **Predictive Alert Service (`services/predictive_alert.py`)**

## Getting Started in VSCode

### Prerequisites

- Python 3.9+
- Visual Studio Code with the Python extension.

### Setup Instructions

1.  **Unzip the Project:** Extract the contents of this zip file.
2.  **Open in VSCode:** Open the extracted folder in VSCode.
3.  **Create & Activate Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows: .\venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    ```
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configure Environment Variables:**
    - Copy `.env.example` to a new file named `.env`.
    - Fill in your API keys in the `.env` file.
6.  **Run the Application:**
    ```bash
    uvicorn main:app --reload
    ```
7.  **Access the API:**
    - **API Root:** `http://127.0.0.1:8000/`
    - **Interactive API Docs:** `http://127.0.0.1:8000/docs`
