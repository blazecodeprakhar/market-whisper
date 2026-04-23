import numpy as np
import pandas as pd

class SignalExtractor:
    """
    Extracts the 5 core microstructure signals to feed into the HMM.
    Requires a pandas DataFrame with columns: ['Open', 'High', 'Low', 'Close', 'Volume', 'Bid', 'Ask']
    If Bid/Ask are missing, Spread Memory will be simulated or skipped.
    """
    def __init__(self, rolling_window=20):
        self.window = rolling_window

    def compute_all_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['velocity_score'] = self._calc_velocity(df)
        df['volume_shape'] = self._calc_volume_shape(df)
        df['spread_memory'] = self._calc_spread_memory(df)
        df['body_ratio'] = self._calc_body_ratio(df)
        df['time_gravity'] = self._calc_time_gravity(df)
        
        # Drop initial NaN rows due to rolling windows
        df.dropna(inplace=True)
        return df[['velocity_score', 'volume_shape', 'spread_memory', 'body_ratio', 'time_gravity']]

    def _calc_velocity(self, df: pd.DataFrame) -> pd.Series:
        """
        Velocity Score: Rate of price change vs average.
        High = urgency. Low = indecision.
        """
        returns = df['Close'].pct_change()
        volatility = returns.rolling(window=self.window).std()
        # Z-score of the current return
        velocity = returns / (volatility + 1e-9) 
        return velocity.fillna(0)

    def _calc_volume_shape(self, df: pd.DataFrame) -> pd.Series:
        """
        Volume Shape Index: Is volume front-loaded or back-loaded?
        Approximated here by correlating volume surges with price direction.
        (A true intra-candle volume shape requires tick data).
        """
        # For OHLCV, we use the ratio of (Close-Open) to (High-Low) multiplied by relative volume
        price_move = df['Close'] - df['Open']
        total_range = df['High'] - df['Low']
        relative_move = price_move / (total_range + 1e-9)
        
        avg_vol = df['Volume'].rolling(window=self.window).mean()
        rel_vol = df['Volume'] / (avg_vol + 1e-9)
        
        return (relative_move * rel_vol).fillna(0)

    def _calc_spread_memory(self, df: pd.DataFrame) -> pd.Series:
        """
        Spread Memory: Compressing spread = accumulation. Widening = distribution.
        """
        if 'Bid' in df.columns and 'Ask' in df.columns:
            spread = df['Ask'] - df['Bid']
        else:
            # Proxy: High-Low range as a percentage of price
            spread = (df['High'] - df['Low']) / df['Close']
            
        avg_spread = spread.rolling(window=self.window).mean()
        spread_compression = avg_spread - spread
        return spread_compression.fillna(0)

    def _calc_body_ratio(self, df: pd.DataFrame) -> pd.Series:
        """
        Candle Body Ratio Stream: Body vs wick ratio.
        High body = conviction. High wick = rejection/fight.
        """
        body = (df['Close'] - df['Open']).abs()
        total_range = df['High'] - df['Low']
        ratio = body / (total_range + 1e-9)
        return ratio.rolling(window=self.window).mean().fillna(0)

    def _calc_time_gravity(self, df: pd.DataFrame) -> pd.Series:
        """
        Time Gravity: Weight signals by historical time-of-day behavior.
        Assuming index is DatetimeIndex.
        Morning (high volatility) vs Midday (chop) vs Close (momentum).
        """
        if not isinstance(df.index, pd.DatetimeIndex):
            return pd.Series(1.0, index=df.index) # Default neutral weight
            
        # Example synthetic gravity based on hour and minute
        # Real version would load weights from time_gravity.json
        hours = df.index.hour
        mins = df.index.minute
        time_decimal = hours + mins/60.0
        
        # Simple U-shape volatility curve proxy (high at open 9.5, low at 12, high at close 16)
        # We model this as a parabolic function
        gravity = (time_decimal - 12.75)**2 / 10.0 + 0.5
        return pd.Series(gravity, index=df.index)

if __name__ == "__main__":
    # Test with dummy data
    dates = pd.date_range('2023-01-01 09:30', periods=100, freq='5T')
    df = pd.DataFrame({
        'Open': np.random.randn(100).cumsum() + 100,
        'High': np.random.randn(100).cumsum() + 101,
        'Low': np.random.randn(100).cumsum() + 99,
        'Close': np.random.randn(100).cumsum() + 100.5,
        'Volume': np.random.randint(100, 1000, 100)
    }, index=dates)
    
    extractor = SignalExtractor()
    signals = extractor.compute_all_signals(df)
    print("Computed Signals Shape:", signals.shape)
    print(signals.head())
