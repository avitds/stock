from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    symbol: str

@app.post("/analyze")
async def analyze_stock(data: StockRequest):
    try:
        stock = yf.Ticker(data.symbol)
        hist = stock.history(period="1mo")

        if hist.empty:
            return {"status": "error", "message": "No data found"}

        # Basic Signal Logic: Moving Average Strategy
        hist['SMA_5'] = hist['Close'].rolling(window=5).mean()
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        latest = hist.iloc[-1]

        signal = "Hold"
        if latest['SMA_5'] > latest['SMA_20']:
            signal = "Buy"
        elif latest['SMA_5'] < latest['SMA_20']:
            signal = "Sell"

        return {
            "status": "success",
            "symbol": data.symbol.upper(),
            "latest_price": round(latest['Close'], 2),
            "signal": signal
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    symbol: str

@app.post("/analyze")
async def analyze_stock(data: StockRequest):
    try:
        stock = yf.Ticker(data.symbol)
        hist = stock.history(period="1mo")

        if hist.empty:
            return {"status": "error", "message": "No data found"}

        # Basic Signal Logic: Moving Average Strategy
        hist['SMA_5'] = hist['Close'].rolling(window=5).mean()
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        latest = hist.iloc[-1]

        signal = "Hold"
        if latest['SMA_5'] > latest['SMA_20']:
            signal = "Buy"
        elif latest['SMA_5'] < latest['SMA_20']:
            signal = "Sell"

        return {
            "status": "success",
            "symbol": data.symbol.upper(),
            "latest_price": round(latest['Close'], 2),
            "signal": signal
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
