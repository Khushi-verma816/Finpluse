# FinPulse Analytics

FinPulse Analytics is a Streamlit-based fintech analytics dashboard for exploring digital transaction trends, business KPIs, forecasting, and fraud/anomaly signals.

## Features

- Interactive dashboard with multi-page navigation
- KPI tracking for transaction volume, value, growth, and success rate
- Business insights and recommendations from transaction patterns
- Time-series trend analysis and forecasting (Prophet, ARIMA, Exponential Smoothing)
- Fraud detection using statistical rules and Isolation Forest
- Export options for KPI and analytics reports
- Theme toggle (light/dark) and filter controls

## Tech Stack

- Python
- Streamlit
- Pandas, NumPy
- Plotly
- scikit-learn
- Prophet
- statsmodels

## Project Structure

```text
finpulse_analytics/
├── requirements.txt
├── README.md
└── src/
    ├── analytics/
    │   ├── fraud_detection.py
    │   ├── kpi_calculator.py
    │   └── time_series.py
    └── dashboard/
        ├── app.py
        └── components.py


## Getting Started

### 1. Clone the repository

bash
git clone <your-repo-url>
cd finpulse_analytics


### 2. Create and activate a virtual environment

**Windows (PowerShell):**
powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1


**macOS/Linux:**
bash
python3 -m venv .venv
source .venv/bin/activate


### 3. Install dependencies

bash
pip install -r requirements.txt


### 4. Run the dashboard

bash
streamlit run src/dashboard/app.py


Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## How It Works

- The app currently generates sample transaction data in-memory for demo purposes.
- Analytics modules process the data for KPIs, business insights, forecasting, and anomaly detection.
- Dashboard pages visualize outputs with interactive Plotly charts and tables.

## Notes

- This version is analytics-focused and ready for portfolio/GitHub showcase.
- To move to production, connect real data sources and add automated tests/CI.
