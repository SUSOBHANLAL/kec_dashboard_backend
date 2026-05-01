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
├── run.py
└── requirements.txt





API NAME 
http://127.0.0.1:5000/api/v1/forecast?ticker=TCS&model=arima



http://localhost:5000/api/v1/predict-model?ticker=HLL