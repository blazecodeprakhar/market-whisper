# 🕯️ MarketWhisper: The Market's Subconscious, Made Visible

![MarketWhisper Interface](screenshot.png)

> **"Every price chart you've ever seen shows you what happened. MarketWhisper shows you what the market was feeling at every moment."**

MarketWhisper is a state-of-the-art, multi-model market edge detection and probabilistic execution system (code-named **PANTHEON-WHISPER**). It is designed to reconstruct the emotional narrative hidden inside order flow, volume patterns, and price microstructure, and render it as a living, breathing visual story in real-time. 

Not indicators. Not RSI. Not MACD. Something completely different.

## 🧠 The Magic Mechanism
Markets leave psychological fingerprints in their data that traditional traders never look at together. MarketWhisper reads these simultaneously to map the market's hidden emotional state.

`Price Velocity + Volume Shape + Time-of-Day Rhythm + Spread Compression + Candle Body Ratios + Institutional Footprint = The Hidden Emotional State`

The algorithm extracts these core microstructure signals and feeds them into a **Hidden Markov Model (HMM)** to output one of 7 discrete market states (e.g., *🌊 Drift, 🐋 Accumulation, 💥 Panic*), which then drives the visual dashboard.

---

## 🖥️ The Interface (The 3 Panels)

### Panel 1: The Pulse
A real-time organic waveform that physically changes shape based on market stress. 
- **Calm market (Drift):** Slow, smooth blue sine wave. 
- **Panic/Stops run:** Sharp, jagged red spikes. 
- **Accumulation:** Deep, slow purple pulse.
*You glance at it and instantly know what's happening without reading a single number.*

### Panel 2: The Memory Wall
A scrolling heatmap showing the historical progression of market "emotional states" as color blocks. It allows you to see exactly when the market transitioned from confusion → conviction → exhaustion → reversal. Like reading a mood history.

### Panel 3: The Whisper Feed
A live text feed that narrates what the market is doing in plain English, written in the style of a seasoned old-school tape reader's inner monologue:
> *09:47 — "Smart money quietly accumulating. Retail still selling. This divergence won't last long."*

This is algorithmically generated logic acting like pure intuition.

---

## ⚙️ Project Architecture

```text
marketwhisper/
├── core/
│   ├── signal_extractor.py  # Computes the 5 raw emotional signals
│   ├── hmm_classifier.py    # Hidden Markov State detection (7 states)
│   └── narrator.py          # Algorithmic whisper feed generator
├── ui/
│   ├── pulse_widget.py      # pyqtgraph animated waveform
│   ├── memory_wall.py       # Scrolling heatmap
│   ├── whisper_feed.py      # Live tape narration
│   └── main_window.py       # PyQt6 Layout
└── main.py                  # Simulation Engine & App Entry Point
```

### The 5 Signals
1. **Velocity Score:** Rate of price change vs. average volatility.
2. **Volume Shape Index:** Correlation of volume surges with price direction.
3. **Spread Memory:** Compression vs. Expansion of the Bid/Ask spread proxy.
4. **Candle Body Ratio:** Conviction vs. Rejection based on body-to-wick distribution.
5. **Time Gravity:** Market behavior weights based on time-of-day.

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/MarketWhisper.git
   cd MarketWhisper
   ```

2. **Set up a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install numpy pandas hmmlearn scikit-learn scipy statsmodels PyQt6 pyqtgraph yfinance
   ```

---

## 🎮 Usage

Run the application with the built-in random-walk live market simulator:

```bash
python main.py
```
*Note: The simulator generates realistic OHLCV price action every 2 seconds to feed the Hidden Markov Model and drive the visualization.*

---

## 🔮 Future Roadmap (The Pantheon Integration)
- [ ] Connect live `yfinance` or `alpaca-trade-api` order book feeds.
- [ ] Implement walk-forward optimization for the HMM parameters.
- [ ] Multi-timeframe regime detection via LSTMs.
- [ ] Strategy Execution Layer: Position sizing using Fractional Kelly Criterion based on HMM state confidence.

---
*Built for those who don't just want to predict the market, but want to feel its pulse.*
