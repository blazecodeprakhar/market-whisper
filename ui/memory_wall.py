import pyqtgraph as pg
import numpy as np

class MemoryWall(pg.PlotWidget):
    """
    Panel 2 - The Memory Wall
    A scrolling heatmap that shows the last N periods of market "emotional states" as color blocks.
    Not price. Pure state.
    """
    def __init__(self, parent=None, max_history=60):
        super().__init__(parent)
        self.max_history = max_history
        self.setBackground('#0A0A0F')
        self.hideAxis('left')
        self.hideAxis('bottom')
        self.setMouseEnabled(x=False, y=False)
        
        # State colors corresponding to the 7 states
        self.state_colors = [
            (0, 150, 255),    # 0: Drift (Blue)
            (255, 100, 0),    # 1: Ignition (Orange)
            (200, 0, 50),     # 2: Wall (Red)
            (100, 100, 100),  # 3: Exhaustion (Grey)
            (150, 0, 200),    # 4: Accumulation (Purple)
            (255, 0, 0),      # 5: Panic (Bright Red)
            (0, 255, 100)     # 6: Conviction (Green)
        ]
        
        self.history = []
        
        # We will use an ImageItem to act as a heatmap/color block sequence
        self.img = pg.ImageItem()
        self.addItem(self.img)
        
    def add_state(self, state_idx: int):
        """Add a new state to the wall and redraw."""
        self.history.append(state_idx)
        if len(self.history) > self.max_history:
            self.history.pop(0)
            
        self._update_display()
        
    def _update_display(self):
        if not self.history:
            return
            
        # Create an RGB array representing the history
        # Shape: (width, height, 3)
        # We'll make it 1 pixel high and len(history) pixels wide, then it will stretch
        img_data = np.zeros((len(self.history), 1, 3), dtype=np.uint8)
        
        for i, state in enumerate(self.history):
            color = self.state_colors[state] if state < len(self.state_colors) else (0,0,0)
            img_data[i, 0, :] = color
            
        self.img.setImage(img_data, autoLevels=False)
        self.img.setRect(pg.QtCore.QRectF(0, 0, len(self.history), 10))
