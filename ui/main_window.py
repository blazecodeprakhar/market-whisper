from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from .pulse_widget import PulseWidget
from .memory_wall import MemoryWall
from .whisper_feed import WhisperFeed

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarketWhisper - The Market's Subconscious")
        self.resize(1000, 700)
        self.setStyleSheet("background-color: #050508; color: #E0E0E0;")
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Top Panel: Pulse
        pulse_container = QVBoxLayout()
        title1 = QLabel("PANEL 1 — THE PULSE (Current State)")
        title1.setStyleSheet("color: #606070; font-weight: bold; font-family: 'Inter', sans-serif;")
        self.pulse = PulseWidget()
        pulse_container.addWidget(title1)
        pulse_container.addWidget(self.pulse, stretch=3)
        
        # Middle Panel: Memory Wall
        wall_container = QVBoxLayout()
        title2 = QLabel("PANEL 2 — THE MEMORY WALL (History)")
        title2.setStyleSheet("color: #606070; font-weight: bold; font-family: 'Inter', sans-serif;")
        self.wall = MemoryWall(max_history=100)
        wall_container.addWidget(title2)
        wall_container.addWidget(self.wall, stretch=1)
        
        # Bottom Panel: Whisper Feed
        feed_container = QVBoxLayout()
        title3 = QLabel("PANEL 3 — THE WHISPER FEED (Narrative)")
        title3.setStyleSheet("color: #606070; font-weight: bold; font-family: 'Inter', sans-serif;")
        self.feed = WhisperFeed()
        feed_container.addWidget(title3)
        feed_container.addWidget(self.feed, stretch=2)
        
        main_layout.addLayout(pulse_container, stretch=3)
        main_layout.addLayout(wall_container, stretch=1)
        main_layout.addLayout(feed_container, stretch=2)
        
    def update_dashboard(self, state_idx: int, narrative: str):
        """Update all panels with the new state."""
        self.pulse.update_state(state_idx)
        self.wall.add_state(state_idx)
        if narrative:
            self.feed.add_narrative(narrative)
