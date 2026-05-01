PROJECT: Flask Stock Forecast API (Dockerized)

--------------------------------------------------
📁 PROJECT STRUCTURE
--------------------------------------------------

project/
│
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   └── forecast_routes.py
│   │
│   ├── models/
│   │   └── forecasting.py
│   │
│   ├── services/
│   │   └── data_service.py
│   │
│   ├── utils/
│   │   └── metrics.py
│   │
│   └── config.py
│
├── data/                  <-- Recommended: keep CSV files here
│   ├── HLL.csv
│   └── TCS.csv
│
├── run.py
├── requirements.txt
├── Dockerfile
└── .dockerignore


--------------------------------------------------
🚀 API ENDPOINTS
--------------------------------------------------

1. Forecast API
http://127.0.0.1:5000/api/v1/forecast?ticker=TCS&model=arima

2. Predict Model API
http://127.0.0.1:5000/api/v1/predict-model?ticker=HLL


--------------------------------------------------
⚙️ LOCAL SETUP
--------------------------------------------------

STEP 1: Clone Repository
git clone https://github.com/SUSOBHANLAL/kec_dashboard_backend.git
cd kec_dashboard_backend

STEP 2: Install Dependencies
pip install -r requirements.txt

STEP 3: Run Application
python run.py

Make sure Flask runs using:
app.run(host="0.0.0.0", port=5000)


--------------------------------------------------
🐳 DOCKER SETUP
--------------------------------------------------

STEP 1: Create Dockerfile

---------------------------------
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["python", "run.py"]
---------------------------------

STEP 2: Create .dockerignore

---------------------------------
__pycache__/
*.pyc
.env
venv/
.git
---------------------------------

STEP 3: Build Docker Image
docker build -t flask-api .

STEP 4: Run Container
docker run -p 5000:5000 flask-api


--------------------------------------------------
⚠️ CONFIGURATION NOTE (IMPORTANT)
--------------------------------------------------

If your CSV file paths are different from the default setup,
you MUST update them in:

app/config.py

Example:

CSV_FILES = {
    "HLL": "data/HLL.csv",
    "TCS": "data/TCS.csv"
}

If you move your data files to another folder, update the paths accordingly.

Example:

CSV_FILES = {
    "HLL": "new_folder/HLL.csv",
    "TCS": "new_folder/TCS.csv"
}

❗ IMPORTANT:
- Do NOT use Windows absolute paths like:
  E:\folder\file.csv

- Always use relative paths inside the project:
  data/file.csv

This is required for Docker to work correctly.


--------------------------------------------------
⚠️ COMMON ISSUES & FIXES
--------------------------------------------------

1. Error: could not convert string to float: '2,444.70'

Fix:
df['Price'] = df['Price'].str.replace(',', '').astype(float)


2. API not accessible from browser

Ensure Flask runs on:
app.run(host="0.0.0.0", port=5000)


3. CSV file not found inside Docker

- Make sure files exist inside /data folder
- Check config paths
- Rebuild Docker image after changes


--------------------------------------------------
💡 OPTIONAL (DEV MODE WITH VOLUME)
--------------------------------------------------

Run without rebuilding every time:

Windows:
docker run -p 5000:5000 -v %cd%:/app flask-api

Linux/Mac:
docker run -p 5000:5000 -v $(pwd):/app flask-api


--------------------------------------------------
✅ FEATURES
--------------------------------------------------

- Stock Forecasting (ARIMA / ML models)
- REST API with Flask
- Clean Modular Architecture
- Dockerized Deployment
- CSV-based Data Processing


--------------------------------------------------
📌 FUTURE IMPROVEMENTS
--------------------------------------------------

- Add Docker Compose (API + Database)
- Automate daily stock data download
- Deploy to cloud (AWS / Render)
- Add frontend dashboard (React)


--------------------------------------------------
👨‍💻 AUTHOR
--------------------------------------------------

Susobhan Lal

GitHub:
https://github.com/SUSOBHANLAL

--------------------------------------------------