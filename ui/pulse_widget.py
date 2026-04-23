import pyqtgraph as pg
from PyQt6.QtCore import QTimer
import numpy as np

class PulseWidget(pg.PlotWidget):
    """
    Panel 1 - The Pulse
    A real-time organic waveform that physically changes shape based on market stress.
    Calm market = slow sine wave. Panic = sharp jagged spikes.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackground('#0A0A0F') # Deep dark modern background
        self.hideAxis('left')
        self.hideAxis('bottom')
        self.setMouseEnabled(x=False, y=False)
        
        # State variables to hold waveform attributes
        self.phase = 0.0
        self.amplitude = 1.0
        self.frequency = 1.0
        self.jaggedness = 0.0 # Adds noise for panic
        self.color = (0, 200, 255) # Default cyan/blue for drift
        
        # Data array for the curve
        self.x = np.linspace(0, 10, 500)
        
        # Create a line curve
        self.curve = self.plot(pen=pg.mkPen(color=self.color, width=3))
        
        # Fill underneath the curve for a glowing effect
        self.curve.setFillLevel(-10)
        self.curve.setBrush(pg.mkBrush(color=(0, 200, 255, 30)))
        
        # Setup animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pulse)
        self.timer.start(30) # ~33 FPS
        
    def update_state(self, state_idx: int):
        """
        Update the visual parameters based on the HMM market state.
        0: 🌊 Drift -> slow sine
        1: 🔥 Ignition -> faster sine
        2: 🧱 Wall -> flatline with flickers
        3: 😴 Exhaustion -> low amplitude, slow
        4: 🐋 Accumulation -> deep slow pulse
        5: 💥 Panic -> high jagged spikes
        6: 🎯 Conviction -> smooth fast wave
        """
        if state_idx == 0: # Drift
            self._transition_to(amp=1.0, freq=1.0, jag=0.0, color=(0, 150, 255))
        elif state_idx == 1: # Ignition
            self._transition_to(amp=1.5, freq=2.0, jag=0.1, color=(255, 100, 0))
        elif state_idx == 2: # Wall
            self._transition_to(amp=0.2, freq=0.5, jag=0.3, color=(200, 0, 50))
        elif state_idx == 3: # Exhaustion
            self._transition_to(amp=0.5, freq=0.5, jag=0.0, color=(100, 100, 100))
        elif state_idx == 4: # Accumulation
            self._transition_to(amp=2.0, freq=0.3, jag=0.0, color=(150, 0, 200))
        elif state_idx == 5: # Panic
            self._transition_to(amp=3.0, freq=3.0, jag=1.5, color=(255, 0, 0))
        elif state_idx == 6: # Conviction
            self._transition_to(amp=2.0, freq=2.5, jag=0.0, color=(0, 255, 100))

    def _transition_to(self, amp, freq, jag, color):
        # In a real app, you would smoothly interpolate these values over time.
        # Here we jump directly for demonstration, but it can be easily tweened.
        self.target_amplitude = amp
        self.target_frequency = freq
        self.target_jaggedness = jag
        
        # We can update the curve color directly
        pen = pg.mkPen(color=color, width=3)
        self.curve.setPen(pen)
        self.curve.setBrush(pg.mkBrush(color=(color[0], color[1], color[2], 50)))
        
        # Hard assign for now (could be smooth transition)
        self.amplitude = amp
        self.frequency = freq
        self.jaggedness = jag

    def update_pulse(self):
        # Time progression
        self.phase -= 0.1 * self.frequency
        
        # Base wave
        y = np.sin(self.x * 2 + self.phase) * self.amplitude
        
        # Add a secondary frequency for organic feel
        y += np.sin(self.x * 5 - self.phase * 1.5) * (self.amplitude * 0.3)
        
        # Add jaggedness (noise)
        if self.jaggedness > 0:
            noise = (np.random.random(len(self.x)) - 0.5) * 2 * self.jaggedness
            y += noise
            
        self.curve.setData(self.x, y)
