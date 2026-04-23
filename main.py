import sys
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from core.signal_extractor import SignalExtractor
from core.hmm_classifier import MarketHMM
from core.narrator import Narrator
from ui.main_window import MainWindow

class MarketWhisperApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        
        self.extractor = SignalExtractor(rolling_window=5)
        self.hmm = MarketHMM()
        self.narrator = Narrator()
        
        # Train HMM on dummy data to initialize it
        print("Initializing Brain...")
        dummy_signals = pd.DataFrame(np.random.randn(500, 5), columns=['s1', 's2', 's3', 's4', 's5'])
        self.hmm.train(dummy_signals)
        print("Brain Initialized.")

        # Data Simulation State
        self.current_price = 100.0
        self.simulated_data = []
        
        # Setup Simulation Timer (every 2 seconds, simulate a new 1-minute candle)
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_next_tick)
        self.timer.start(2000)

    def generate_simulated_candle(self):
        """Generate a realistic random walk OHLCV candle"""
        volatility = np.random.uniform(0.1, 0.5)
        open_p = self.current_price
        close_p = open_p + np.random.normal(0, volatility)
        high_p = max(open_p, close_p) + abs(np.random.normal(0, volatility/2))
        low_p = min(open_p, close_p) - abs(np.random.normal(0, volatility/2))
        volume = int(np.random.uniform(100, 10000))
        
        self.current_price = close_p
        
        return {
            'Open': open_p,
            'High': high_p,
            'Low': low_p,
            'Close': close_p,
            'Volume': volume
        }

    def process_next_tick(self):
        # 1. Get new data
        new_candle = self.generate_simulated_candle()
        self.simulated_data.append(new_candle)
        
        df = pd.DataFrame(self.simulated_data)
        
        # Need at least 'rolling_window' candles to compute signals
        if len(df) < self.extractor.window:
            return
            
        # 2. Extract Signals
        signals_df = self.extractor.compute_all_signals(df)
        
        if signals_df.empty:
            return
            
        # Get the latest signal vector
        current_signal = signals_df.iloc[-1].to_dict()
        current_signal_arr = signals_df.iloc[-1:].values
        
        # 3. Classify State
        state_idx = self.hmm.predict_state(signals_df.iloc[-1:])[0]
        
        # 4. Generate Narrative
        narrative = self.narrator.generate_narration(state_idx, current_signal)
        
        # 5. Update UI
        self.window.update_dashboard(state_idx, narrative)

    def run(self):
        self.window.show()
        
        # Add initial welcome message
        self.window.feed.add_narrative("SYSTEM ONLINE. Initializing Pantheon-Whisper Subconscious Interface...")
        self.window.feed.add_narrative("Connecting to data feeds. Calibrating Hidden Markov Models...")
        self.window.feed.add_narrative("Listening to the market...")
        
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = MarketWhisperApp()
    app.run()
