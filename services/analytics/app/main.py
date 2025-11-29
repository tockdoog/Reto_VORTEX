from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import numpy as np
import pandas as pd
from scipy import stats
from app.models import CorrelationsRequest, CorrelationsResponse, TrendsRequest, TrendsResponse, InsightsResponse

app = FastAPI(title="MS-Analytics-Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "MS-Analytics-Service", "timestamp": datetime.now().isoformat()}

@app.post("/api/analytics/correlations", response_model=CorrelationsResponse)
async def correlations(req: CorrelationsRequest):
    try:
        arr = np.array(req.data, dtype=float)
        df = pd.DataFrame(arr, columns=req.columns if req.columns else None)
        corr = df.corr(method="pearson")
        cols = list(corr.columns)
        return CorrelationsResponse(method="pearson", columns=cols, matrix=corr.values.tolist())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/insights", response_model=InsightsResponse)
async def insights():
    try:
        top_factor = "sentiment_score"
        insights = [
            "Bajo sentimiento se correlaciona con mayor churn",
            "Tickets frecuentes elevan el riesgo",
            "Tenencia baja incrementa probabilidad de salida"
        ]
        stats_dict = {"sample_size": 100, "method": "pearson"}
        return InsightsResponse(top_factor=top_factor, insights=insights, stats=stats_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analytics/trends", response_model=TrendsResponse)
async def trends(req: TrendsRequest):
    try:
        values = np.array(req.values, dtype=float)
        window = max(1, int(req.window))
        if window > len(values):
            window = len(values)
        kernel = np.ones(window) / window
        ma = np.convolve(values, kernel, mode="same").tolist()
        return TrendsResponse(dates=req.dates, values=req.values, moving_avg=ma)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
