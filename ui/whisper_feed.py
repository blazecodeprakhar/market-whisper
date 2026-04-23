from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont, QColor
import datetime

class WhisperFeed(QTextEdit):
    """
    Panel 3 - The Whisper Feed
    A live text feed that narrates what the market is doing in plain English.
    Written in the style of an old-school tape reader.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #0A0A0F;
                color: #A0A0B0;
                border: 1px solid #1A1A25;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
            }
        """)
        
    def add_narrative(self, text: str):
        if not text:
            return
            
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Colorize certain keywords
        formatted_text = text
        if "Smart money" in text or "Accumulation" in text:
            color = "#9600c8" # Purple
        elif "Panic" in text or "Wall" in text or "Blood" in text:
            color = "#ff0000" # Red
        elif "Ignition" in text or "fire" in text:
            color = "#ff6400" # Orange
        elif "Conviction" in text or "trend" in text:
            color = "#00ff64" # Green
        else:
            color = "#0096ff" # Blue/Neutral
            
        html = f"""
        <div style='margin-bottom: 8px;'>
            <span style='color: #505060;'>{timestamp} — </span>
            <span style='color: {color};'>{formatted_text}</span>
        </div>
        """
        self.append(html)
        
        # Scroll to bottom
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
