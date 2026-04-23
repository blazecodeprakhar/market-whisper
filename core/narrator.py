class Narrator:
    """
    Generates algorithmic commentary in the style of an old-school tape reader.
    Reacts to the current state and the previous state.
    """
    
    def __init__(self):
        self.last_state = -1
        self.consecutive_ticks = 0

    def generate_narration(self, current_state: int, signals: dict) -> str:
        """
        Produce a narrative string based on the state and raw signals.
        """
        # If state hasn't changed, increment tick counter
        if current_state == self.last_state:
            self.consecutive_ticks += 1
        else:
            self.consecutive_ticks = 0
            
        previous_state = self.last_state
        self.last_state = current_state
        
        velocity = signals.get('velocity_score', 0)
        spread = signals.get('spread_memory', 0)
        
        # New State Transitions
        if self.consecutive_ticks == 0:
            if current_state == 4: # Accumulation
                return "Smart money quietly accumulating. Spread is compressing. They are hiding their size."
            elif current_state == 1: # Ignition
                if previous_state == 4:
                    return "There it is. Accumulation phase over. Institutions just showed their hand. Momentum shifting."
                else:
                    return "Volume stepping in. Someone is trying to start a fire here."
            elif current_state == 2: # Wall
                return "Hitting a brick wall. Big offers refreshing at the ask. They aren't letting it through."
            elif current_state == 5: # Panic
                return "Stops getting run. Panic selling. Pure emotion right now, no logic."
            elif current_state == 6: # Conviction
                return "Clean trend. Good separation. Don't fight this tape, just ride the wave."
            elif current_state == 3: # Exhaustion
                if velocity < 0:
                    return "Sellers are tired. The tape is running out of fuel to the downside."
                else:
                    return "Buyers are exhausted. Volume drying up at the highs. Looking heavy."
            elif current_state == 0: # Drift
                return "Dead tape. Retail chopping each other up. Nothing to do but sit on hands."

        # Ongoing States (Sustained)
        else:
            if current_state == 4 and self.consecutive_ticks > 5:
                return "Still building a base. The longer it coils, the harder it will spring."
            elif current_state == 6 and self.consecutive_ticks > 5:
                return "Beautiful, orderly flow. The trend is your friend right now."
            elif current_state == 2 and self.consecutive_ticks > 3:
                return "Still can't break that wall. Absorption happening. Be careful."
            elif current_state == 5 and self.consecutive_ticks > 3:
                return "Blood in the streets. Waiting for the capitulation volume climax."
                
        # Fallback if no specific trigger
        return None # Return None if we don't have a new thing to say to avoid spamming

if __name__ == "__main__":
    n = Narrator()
    print(n.generate_narration(0, {}))
    print(n.generate_narration(4, {}))
    print(n.generate_narration(4, {}))
    print(n.generate_narration(1, {}))
