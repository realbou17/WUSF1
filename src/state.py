from __future__ import annotations
from typing import Any

class AppState:
    def __init__(self):     
        # UI
        self.current_view = "telemetry"
        self.sessionID = ""
        self.track_default = ""
        self.latest_year = 0
        
        # Data
        self.telemetry_data = []
        self.track = ""
        self.session: Any = None
        self.drivers = []
        self.selected_laps = []

        # Calendar
        self.schedule: Any = None
        self.calendar = []
        self.testing = 0
        self.test_number = 0       
        self.session_order = []
        self.session_list = []
        self.is_sprint = False
        
        # Themes
        self.themes = {}
        self.hex_colors = []
        self.driver_colors = []

    def set_driver_color(self, index, hex_str):
        h = hex_str.lstrip('#')
        color = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        if index < len(self.driver_colors):
            self.driver_colors[index] = color
        else:
            self.driver_colors.append(color)

    def reset_session_data(self):
        self.telemetry_data.clear()
        self.session = None
        self.drivers = []
        self.selected_laps = []

# Used for the whole program
state = AppState()