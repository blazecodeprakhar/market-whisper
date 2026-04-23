import numpy as np
import pandas as pd
from hmmlearn import hmm
import joblib
import os

class MarketHMM:
    """
    Hidden Markov Model classifier that maps the 5 microstructure signals
    into 7 discrete "market states" (emotional narrative).
    """
    
    STATE_NAMES = {
        0: "🌊 Drift (No one in control)",
        1: "🔥 Ignition (Breakout starting)",
        2: "🧱 Wall (Hitting hard resistance)",
        3: "😴 Exhaustion (Move running out of fuel)",
        4: "🐋 Accumulation (Smart money loading quietly)",
        5: "💥 Panic (Forced selling / stops hit)",
        6: "🎯 Conviction (Clean directional move)"
    }
    
    def __init__(self, n_components=7, model_path="data/hmm_model.pkl"):
        self.n_components = n_components
        self.model_path = model_path
        self.model = hmm.GaussianHMM(
            n_components=self.n_components, 
            covariance_type="full", 
            n_iter=1000,
            random_state=42
        )
        self.is_fitted = False
        
    def train(self, signals_df: pd.DataFrame):
        """
        Train the HMM on historical signal data.
        """
        print("Training HMM on historical signals...")
        X = signals_df.values
        self.model.fit(X)
        self.is_fitted = True
        self.save_model()
        print("HMM Training Complete.")
        
    def predict_state(self, signals_df: pd.DataFrame) -> np.ndarray:
        """
        Predict the most likely sequence of states.
        """
        if not self.is_fitted:
            self._try_load_model()
            
        if not self.is_fitted:
            raise ValueError("Model is not fitted. Call train() first or provide a pre-trained model.")
            
        X = signals_df.values
        hidden_states = self.model.predict(X)
        return hidden_states
        
    def predict_proba(self, current_signal: np.ndarray) -> np.ndarray:
        """
        Get the probability distribution of the current state.
        Useful for the visual pulse (blending colors based on probabilities).
        """
        if current_signal.ndim == 1:
            current_signal = current_signal.reshape(1, -1)
        # For a single observation, we can compute the posterior
        _, posteriors = self.model.score_samples(current_signal)
        return np.exp(posteriors)
        
    def get_state_name(self, state_idx: int) -> str:
        return self.STATE_NAMES.get(state_idx, "Unknown State")

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        
    def _try_load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_fitted = True

if __name__ == "__main__":
    # Test with dummy signal data
    print("Testing HMM Classifier...")
    dummy_signals = pd.DataFrame(np.random.randn(500, 5), columns=['s1', 's2', 's3', 's4', 's5'])
    classifier = MarketHMM()
    classifier.train(dummy_signals)
    states = classifier.predict_state(dummy_signals)
    print("First 10 predicted states:")
    for s in states[:10]:
        print(f"State {s}: {classifier.get_state_name(s)}")
