from __future__ import annotations
from typing import Any

class AppState:
    def __init__(self):    
        # UI
        self.current_view = "graphs"
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

        # Dimensions
        self.screen_w = 1920
        self.screen_h = 1080

        # Layout ratios
        self.tab_h = 60
        self.main_row_h = 0
        self.graph_h = 0
        self.SIDE_W = 0.20
        self.SPACER_W = 0.26
        self.TRACK_W = 0.34
        self.TRACK_H = 0.37
        self.LAP_H = 0.07
        self.HIST_ROW_H = 0.19
        self.SCAT_ROW_H = 0.357
        self.SPACER_H = 0.005
        self.INPUT_W = 0.13
        self.TELEMBUTTON_H = 0.035

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