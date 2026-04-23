import asyncio
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from core.signal_extractor import SignalExtractor
from core.hmm_classifier import MarketHMM
from core.narrator import Narrator

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Core Engine Components
extractor = SignalExtractor(rolling_window=5)
hmm = MarketHMM()
narrator = Narrator()

# Initialize HMM
print("Initializing Brain...")
dummy_signals = pd.DataFrame(np.random.randn(500, 5), columns=['s1', 's2', 's3', 's4', 's5'])
hmm.train(dummy_signals)
print("Brain Initialized.")

current_price = 100.0
simulated_data = []

def generate_simulated_candle():
    global current_price
    volatility = np.random.uniform(0.1, 0.5)
    open_p = current_price
    close_p = open_p + np.random.normal(0, volatility)
    high_p = max(open_p, close_p) + abs(np.random.normal(0, volatility/2))
    low_p = min(open_p, close_p) - abs(np.random.normal(0, volatility/2))
    volume = int(np.random.uniform(100, 10000))
    current_price = close_p
    return {'Open': open_p, 'High': high_p, 'Low': low_p, 'Close': close_p, 'Volume': volume}

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Send initial welcome text
    await websocket.send_json({
        "type": "narrative",
        "text": "SYSTEM ONLINE. Connecting to Web Subconscious Interface..."
    })
    
    try:
        while True:
            # Generate tick
            new_candle = generate_simulated_candle()
            simulated_data.append(new_candle)
            df = pd.DataFrame(simulated_data)
            
            if len(df) >= extractor.window:
                signals_df = extractor.compute_all_signals(df)
                if not signals_df.empty:
                    current_signal = signals_df.iloc[-1].to_dict()
                    state_idx = int(hmm.predict_state(signals_df.iloc[-1:])[0])
                    narrative_text = narrator.generate_narration(state_idx, current_signal)
                    
                    payload = {
                        "type": "tick",
                        "state": state_idx,
                        "narrative": narrative_text
                    }
                    await websocket.send_json(payload)
            
            # Send an update every 2 seconds
            await asyncio.sleep(2)
            
    except WebSocketDisconnect:
        print("Client disconnected")
