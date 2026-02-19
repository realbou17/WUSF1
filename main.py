import dearpygui.dearpygui as dpg
import fastf1
from fastf1 import plotting
import numpy as np
from datetime import datetime, timezone
import os

class AppState:
    def __init__(self):     
        # Main variables
        self.current_view = "telemetry"
        self.telemetry_data = {}
        self.telemetry_data2 = {}
        self.track = {}
        self.latest_year = 0
        self.sessionID = {}
        self.session = {}
        self.hex_color = {}
        self.hex_color2 = {}
        self.r = 0
        self.g = 0
        self.b = 0
        self.r2 = 0
        self.g2 = 0
        self.b2 = 0
        self.driver = {}
        self.driver2 = {}
        self.lap_int = 0
        self.lap_int2 = 0
        self.lap_num2 = 0
        self.lap_num = 0
        self.lap = 0
        self.schedule = {}
        self.session_order = {}
        self.track_default = ""
        self.testing = 0

        # Colors
        self.use_team_colors = False
        self.driver_color = (200, 200, 200)     # rgb default
        self.driver2_color = (200, 200, 200)
        
        # Themes cache
        self.themes = {}

    def reset_session_data(self):
        self.telemetry_data.clear()
        self.telemetry_data2.clear()
        self.session = None
        self.driver = ""
        self.driver2 = ""
        self.lap = 0
        self.lap2 = 0

# Used for the whole program
state = AppState()

cache_dir = "fastf1_cache"
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

def load_latest_session():
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    state.latest_year = now.year
    state.schedule = fastf1.get_event_schedule(state.latest_year, include_testing=True)
    past_events = state.schedule[state.schedule['EventDate'] < now]

    while past_events.empty:
        state.latest_year -= 1
        state.schedule = fastf1.get_event_schedule(state.latest_year, include_testing=True)
        past_events = state.schedule[state.schedule['EventDate'] < now]
        print("There are no past events for", state.latest_year)

    last_event = past_events.iloc[-1]
    state.track = last_event['EventName']
    test =  state.schedule[state.schedule['EventFormat'] == 'testing']

    if last_event['RoundNumber'] == 0: 
        state.session_order.clear()
        state.session_order = ['Practice 3', 'Practice 2', 'Practice 1']
        state.testing = 1
        session_found = 0
        test_number = len(test)
        for i in range(test_number, 0, -1):
            for order in state.session_order:
                state.session = fastf1.get_testing_session(state.latest_year, i, order)
                state.session.load(laps=True, telemetry=False, weather=False)
                if state.session.date < now and not state.session.laps.empty:
                        session_found = 1
                        state.sessionID = order
                        print(f"Loaded latest session: {state.track} - {order}")
                        state.track_default = state.track + " " + str(i)
                break
            if session_found:
                break        
    else:
        state.track_default = state.track
        state.session_order = ['R', 'Q', 'S', 'SQ', 'SS', 'FP3', 'FP2', 'FP1']
        state.testing = 0
        for order in state.session_order:
            try:
                state.session = fastf1.get_session(state.latest_year, state.track, order)
                state.session.load(laps=False, telemetry=False, weather=False)
                if state.session.date < now:
                    state.sessionID = order
                    print(f"Loaded latest session: {state.track} - {order}")
            except:
                continue
load_latest_session()

def create_interface():
    dpg.create_context()
    with dpg.theme(tag="main_theme"):
        with dpg.theme_component(dpg.mvAll):
            # Main colors
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (18, 18, 22, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (22, 22, 28, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (25, 25, 32, 240))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 60, 70, 180))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (35, 35, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (230, 92, 0, 180))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (200, 70, 0, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (18, 18, 22, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (25, 25, 32, 255))
            
            # Text and important elements
            dpg.add_theme_color(dpg.mvThemeCol_Text, (235, 235, 240, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (110, 110, 125, 255))
            
            # Orange
            dpg.add_theme_color(dpg.mvThemeCol_Button, (230, 92, 0, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 125, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 70, 0, 255))     
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 50, 65, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (40, 40, 55, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (230, 92, 0, 180))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (255, 125, 40, 220))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (200, 70, 0, 255))
            
            # Rounded edges and spacing
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 5)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)

    # Custom colors for graphs
    with dpg.theme(tag="track_point_theme"):
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, (255, 105, 180, 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, (255, 105, 180, 255), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="track_line_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)
            
    with dpg.theme(tag="speed_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 0, 255), category=dpg.mvThemeCat_Plots)  # Blue
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 0, 255, 200), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="speed_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="rpm_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 105, 180, 255), category=dpg.mvThemeCat_Plots)  # Pink
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 105, 180, 200), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="rpm_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="gear_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 165, 0, 255), category=dpg.mvThemeCat_Plots)  # Orange
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 165, 0, 220), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="gear_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 220), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="throttle_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 0, 255), category=dpg.mvThemeCat_Plots)  # Green
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 255, 0, 255), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="throttle_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="brake_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 0, 0, 255), category=dpg.mvThemeCat_Plots)  # Red           
    with dpg.theme(tag="brake_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White

    with dpg.theme(tag="drs_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 0, 255), category=dpg.mvThemeCat_Plots)  # Yellow
    with dpg.theme(tag="drs_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White

    with dpg.theme(tag="purple_button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (128, 0, 128, 255), category=dpg.mvThemeCat_Core)  # Purple background
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (160, 32, 160, 255), category=dpg.mvThemeCat_Core)  # Lighter purple
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 0, 100, 255), category=dpg.mvThemeCat_Core)  # Darker purple

    dpg.create_viewport(title="WUS Telemetry", width=860, height=1100)

    with dpg.window(label="Real F1 Telemetry Graphs", width=1920, height=1008, tag="main_window"):
        dpg.toggle_viewport_fullscreen()
        dpg.bind_item_theme("main_window", "main_theme")

        with dpg.tab_bar(label="view"):
            dpg.add_tab_button(label="Telemetry Graphs", callback=lambda: switch_view("telemetry"))
            dpg.add_tab_button(label="Histogram", callback=lambda: switch_view("histogram"))
            dpg.add_tab_button(label="Statistics", callback=lambda: switch_view("stats"))

        with dpg.group(horizontal=True, tag="main_row"):
            with dpg.group(horizontal=False, tag="info", width=380):
                dpg.add_text("Fill inputs", wrap=500)
                dpg.add_text("Session:")
                dpg.add_combo(items=state.session_order, tag="session_input", width=260, default_value=state.sessionID)
                dpg.add_text("Track:")
                dpg.add_combo(items=state.schedule['EventName'].tolist(), tag="track_input", width=260, default_value=state.track_default, callback=refresh_track)
                dpg.add_text("Year:")
                dpg.add_input_text(tag="year_input", hint="E.g: 2025", width=260, default_value=state.latest_year)
                dpg.add_text("Driver (3 capital letters):")
                dpg.add_input_text(tag="driver_input", hint="E.g: PIA", width=260, default_value="PIA")
                with dpg.group(tag="driver_compare", show=False):
                    dpg.add_text("Driver to compare (3 capital letters):")
                    dpg.add_input_text(tag="driver2_input", hint="E.g: VER", width=260, default_value="VER")
                dpg.add_text("Lap (0 for fastest):", show=False)
                dpg.add_input_text(tag="lap_input", hint="E.g: 1", width=260, default_value=0, show=False)
                dpg.add_text("2nd driver lap (0 for fastest):", show=False)
                dpg.add_input_text(tag="lap_input2", hint="E.g: 1", width=260, default_value=0, show=False)
                dpg.add_spacer(height=5)
                dpg.add_checkbox(label="Compare", callback=compare_inputs, tag="Compare", default_value=False)
                dpg.add_spacer(height=5)
                dpg.add_button(label="Show Telemetry", callback=load_telemetry, height=22)
                dpg.add_spacer(height=5)
                dpg.add_checkbox(label="Team colors", callback=hex_to_rgb, tag="hex", default_value=False)
                dpg.add_spacer(height=5)
                dpg.add_text("", tag="result_text", wrap=1000)
            dpg.add_spacer(width=700)

            with dpg.group(horizontal=False, tag="track_side"):
                plot_track = dpg.add_plot(label="", height=400, width=650, tag="my_plot_track", zoom_mod=True, crosshairs=True, no_box_select=True, no_frame=True, no_menus=True, no_title=True, no_mouse_pos=True)
                dpg.add_plot_axis(dpg.mvXAxis, parent=plot_track, tag="x_axis", auto_fit=True, no_gridlines=True, no_highlight=True, no_tick_marks=True, no_tick_labels=True)
                dpg.add_plot_axis(dpg.mvYAxis, parent=plot_track, tag="y_axis", auto_fit=True, no_gridlines=True, no_highlight=True, no_tick_marks=True, no_tick_labels=True)
                dpg.add_line_series([], [], parent="y_axis", tag="track_line")
                dpg.bind_item_theme("track_line", "track_line_theme")
                dpg.add_scatter_series([], [], parent="y_axis", tag="track_point")

        with dpg.child_window(width=-1, height=70, tag="lap_selector_container", border=False, horizontal_scrollbar=True):
            dpg.add_text("Lap selector:")
        with dpg.child_window(width=-1, height=70, tag="lap_selector_container2", border=False, horizontal_scrollbar=True, show=False):
            dpg.add_text("Compared driver lap selector:")

        dpg.add_checkbox(label="Show info", callback=hide_inputs, tag="Info", default_value=True)

        with dpg.child_window(width=-1, height=160, tag="plot_container_speed", show=True):
            pass
        with dpg.child_window(width=-1, height=160, tag="plot_container_rpm", show=True):
            pass
        with dpg.child_window(width=-1, height=160, tag="plot_container_gear", show=True):
            pass
        with dpg.child_window(width=-1, height=160, tag="plot_container_throttle", show=True):
            pass
        with dpg.child_window(width=-1, height=160, tag="plot_container_brake", show=True):
            pass
        with dpg.child_window(width=-1, height=160, tag="plot_container_drs", show=True):
            pass
        with dpg.group(horizontal=False):
            with dpg.child_window(width=0, autosize_x=True, tag="hist_container", show=False):
                pass
        with dpg.group(horizontal=True):
            with dpg.child_window(width=0, autosize_x=False, tag="stats", show=False):
                pass
        with dpg.handler_registry():
            dpg.add_mouse_move_handler(callback=update_car_position)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def refresh_track():
    if dpg.get_value("track_input") != "Pre-Season Testing":
        state.session_order = ['R', 'Q', 'S', 'SQ', 'SS', 'FP3', 'FP2', 'FP1']
        state.testing = 0
    else: 
        state.session_order = ['Practice 1', 'Practice 2', 'Practice 3']
        state.testing = 1
    dpg.configure_item("session_input", items=state.session_order)

def switch_view(view):
    state.current_view = view

    if state.current_view == "telemetry":
        dpg.show_item("plot_container_speed")
        dpg.show_item("plot_container_rpm")
        dpg.show_item("plot_container_gear")
        dpg.show_item("plot_container_throttle")
        dpg.show_item("plot_container_brake")
        dpg.show_item("plot_container_drs")
        dpg.hide_item("hist_container")
        dpg.hide_item("stats")

    elif state.current_view == "histogram":
        dpg.hide_item("plot_container_speed")
        dpg.hide_item("plot_container_rpm")
        dpg.hide_item("plot_container_gear")
        dpg.hide_item("plot_container_throttle")
        dpg.hide_item("plot_container_brake")
        dpg.hide_item("plot_container_drs")
        dpg.show_item("hist_container")
        dpg.hide_item("stats")

    elif state.current_view == "stats":
        dpg.hide_item("plot_container_speed")
        dpg.hide_item("plot_container_rpm")
        dpg.hide_item("plot_container_gear")
        dpg.hide_item("plot_container_throttle")
        dpg.hide_item("plot_container_brake")
        dpg.hide_item("plot_container_drs")
        dpg.hide_item("hist_container")
        dpg.show_item("stats")
    update_plots()

def compare_inputs():
    Compare = dpg.get_value("Compare")

    if Compare:
        dpg.show_item("driver_compare")
        dpg.show_item("lap_selector_container2")
    else:
        dpg.hide_item("driver_compare")
        dpg.hide_item("lap_selector_container2")

def hide_inputs():
    Info = dpg.get_value("Info")
    Compare = dpg.get_value("Compare")
    if not Info:
        dpg.hide_item("info")
        dpg.hide_item("track_side")
        dpg.hide_item("lap_selector_container")
        dpg.hide_item("lap_selector_container2")
    else:
        dpg.show_item("info")
        dpg.show_item("track_side")
        dpg.show_item("lap_selector_container")
        if Compare:
            dpg.show_item("lap_selector_container2")

def select_lap_callback(sender, app_data, user_data):
    state.lap = user_data
    dpg.set_value("lap_input", user_data)
    load_data(None)
    update_plots()

def select_lap_callback2(sender, app_data, user_data):
    state.lap2 = user_data
    dpg.set_value("lap_input2", user_data)
    load_data(None)
    update_plots()

def load_session():
    dpg.set_value("result_text", "It might take long to load data, be patient and do not close this window.")

    Compare = dpg.get_value("Compare")
    session_input = dpg.get_value("session_input")
    state.track = dpg.get_value("track_input")
    year = dpg.get_value("year_input")
    state.driver = dpg.get_value("driver_input")
    state.driver2 = dpg.get_value("driver2_input") if Compare else {}

    if not state.track or not year or not state.driver:
        dpg.set_value("result_text", "Error: Complete state.track, year and driver.")
        return False
    
    try:
        year_int = int(year)
    except ValueError:
        dpg.set_value("result_text", "Error: Year must be numeric.")
        return False

    try:
        if state.testing == 1:
            state.session = fastf1.get_testing_session(year_int, 1, session_input)
            state.session.load()
        else:
            state.session = fastf1.get_session(year_int, state.track, session_input)
            state.session.load()
    except Exception as exc:
        dpg.set_value("result_text", f"The session could not be loaded: {exc}")
        return False
    return True
    
def load_data(user_data):
    Compare = dpg.get_value("Compare")
    state.lap = dpg.get_value("lap_input")
    state.lap2 = dpg.get_value("lap_input2") if Compare else 0

    dpg.delete_item("lap_selector_container", children_only=True)
    dpg.add_text("Lap selector:", parent="lap_selector_container")
    dpg.delete_item("lap_selector_container2", children_only=True) if Compare else None
    dpg.add_text("Compared driver lap selector:", parent="lap_selector_container2") if Compare else None
    
    try:
        driver_laps = state.session.laps.pick_driver(state.driver)
        driver_laps2 = state.session.laps.pick_driver(state.driver2) if Compare else None
        lap_numbers = driver_laps['LapNumber'].unique()
        lap_numbers2 = driver_laps2['LapNumber'].unique() if Compare else None
        fastest = driver_laps.pick_fastest()
        fastest2 = driver_laps2.pick_fastest() if Compare else None
        lap_fastest = fastest['LapNumber']
        lap_fastest2 = fastest2['LapNumber'] if Compare else None

        with dpg.group(horizontal=True, parent="lap_selector_container"):
            for lap_num in sorted(lap_numbers):
                button_tag = f"lap_button_{int(lap_num)}"
                if lap_num == lap_fastest:
                    dpg.add_button(
                            label=f"Lap {int(lap_num)}",
                            callback=select_lap_callback,
                            user_data=int(lap_num),
                            width=80,
                            tag=button_tag
                        )

                    dpg.bind_item_theme(button_tag, "purple_button_theme")
                else:
                    dpg.add_button(
                            label=f"Lap {int(lap_num)}",
                            callback=select_lap_callback,
                            user_data=int(lap_num),
                            width=80,
                            tag=button_tag
                        )

        if Compare:            
            with dpg.group(horizontal=True, parent="lap_selector_container2"):
                for state.lap_num2 in sorted(lap_numbers2):
                    button_tag2 = f"lap_button2_{int(state.lap_num2)}"
                    if state.lap_num2 == lap_fastest2:
                        dpg.add_button(label=f"Lap {int(state.lap_num2)}", callback=select_lap_callback2, user_data=int(state.lap_num2), width=80, tag=button_tag2)
                        dpg.bind_item_theme(button_tag2, "purple_button_theme")
                    else:
                        dpg.add_button(label=f"Lap {int(state.lap_num2)}", callback=select_lap_callback2, user_data=int(state.lap_num2), width=80, tag=button_tag2)
    except Exception as exc:
        dpg.set_value("result_text", f"Error loading laps: {exc}")
        return False

    try:
        state.lap_int = int(state.lap)
        state.lap_int2 = int(state.lap2)
        if state.lap_int == 0:
            telemetry = state.session.laps.pick_driver(state.driver).pick_fastest().get_telemetry()
            lap_fastest = state.session.laps.pick_driver(state.driver).pick_fastest()['LapNumber']
        else:
            lap = state.session.laps.pick_driver(state.driver).pick_lap(state.lap_int)
            telemetry = lap.get_telemetry()
        if Compare:
            if state.lap_int2 == 0:
                telemetry2 = state.session.laps.pick_driver(state.driver2).pick_fastest().get_telemetry()
                lap_fastest2 = state.session.laps.pick_driver(state.driver2).pick_fastest()['LapNumber']
            else:
                lap2 = state.session.laps.pick_driver(state.driver2).pick_lap(state.lap_int2)
                telemetry2 = lap2.get_telemetry()
    except Exception as exc:
        dpg.set_value("result_text", f"Telemetry not found: {exc}")
        return False
    
    state.telemetry_data = {
        "Distance": telemetry["Distance"].to_list(),
        "Speed": telemetry["Speed"].to_list(),
        "RPM": telemetry["RPM"].to_list(),
        "Gear": telemetry["nGear"].to_list(),
        "Throttle": telemetry["Throttle"].to_list(),
        "Brake": telemetry["Brake"].to_list(),
        "DRS": [1 if x >= 10 else 0 for x in telemetry["DRS"].to_list()],
        "Time": telemetry["Time"].dt.total_seconds().to_list(),
        "x": telemetry["X"].to_list(),
        "y": telemetry["Y"].to_list()
    }
    if Compare:
        state.telemetry_data2 = {
            "Distance": telemetry2["Distance"].to_list(),
            "Speed": telemetry2["Speed"].to_list(),
            "RPM": telemetry2["RPM"].to_list(),
            "Gear": telemetry2["nGear"].to_list(),
            "Throttle": telemetry2["Throttle"].to_list(),
            "Brake": telemetry2["Brake"].to_list(),
            "DRS": [1 if x >= 10 else 0 for x in telemetry2["DRS"].to_list()],
            "Time": telemetry2["Time"].dt.total_seconds().to_list(),
        }

def update_plots():
    Compare = dpg.get_value("Compare")
    state.driver = dpg.get_value("driver_input")
    state.driver2 = dpg.get_value("driver2_input")
    state.track = dpg.get_value("track_input")
    year = dpg.get_value("year_input")
    year_int = int(year) if year else 2025

    if not state.telemetry_data:
        dpg.set_value("result_text", "No telemetry data available. Please load telemetry first.")
        return

    for item in ["my_hist_speed", "my_hist_rpm", "my_hist_gear", "my_hist_throttle", "my_hist_brake",
                "my_plot_speed", "my_plot_rpm", "my_plot_gear", "my_plot_throttle", "my_plot_brake", "my_plot_drs"]:
     if dpg.does_item_exist(item):
         dpg.delete_item(item)

    minSpeed = min(state.telemetry_data["Speed"]) - 10
    maxSpeed = max(state.telemetry_data["Speed"]) + 10
    minRPM = min(state.telemetry_data["RPM"]) - 100
    maxRPM = max(state.telemetry_data["RPM"]) + 100
    minGear = min(state.telemetry_data["Gear"]) - 0.05
    maxGear = max(state.telemetry_data["Gear"]) + 0.08
    minThrottle = min(state.telemetry_data["Throttle"])
    maxThrottle = max(state.telemetry_data["Throttle"])
    minBrake = min(state.telemetry_data["Brake"]) - 0.035
    maxBrake = max(state.telemetry_data["Brake"]) + 0.05
    maxTime = max(state.telemetry_data["Time"]) + 2

    dpg.configure_item("track_line", y=state.telemetry_data["y"], x=state.telemetry_data["x"])

    if Compare and state.telemetry_data2:
        minSpeed = min(minSpeed, min(state.telemetry_data2["Speed"]) - 10)
        maxSpeed = max(maxSpeed, max(state.telemetry_data2["Speed"]) + 10)
        minRPM = min(minRPM, min(state.telemetry_data2["RPM"]) - 100)
        maxRPM = max(maxRPM, max(state.telemetry_data2["RPM"]) + 100)
        minGear = min(minGear, min(state.telemetry_data2["Gear"]) - 0.05)
        maxGear = max(maxGear, max(state.telemetry_data2["Gear"]) + 0.08)
        minThrottle = min(minThrottle, min(state.telemetry_data2["Throttle"]))
        maxThrottle = max(maxThrottle, max(state.telemetry_data2["Throttle"]))
        minBrake = min(minBrake, min(state.telemetry_data2["Brake"]) - 0.035)
        maxBrake = max(maxBrake, max(state.telemetry_data2["Brake"]) + 0.05)    

    if state.current_view == "histogram":
        # Speed Histogram
        speed_hist = dpg.add_plot(height=218, width=-1, label="Speed", tag="my_hist_speed", parent="hist_container", no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="km/h", parent=speed_hist, tag="x_axis_hist_speed", no_highlight=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="%", parent=speed_hist, tag="y_axis_hist_speed", no_highlight=True)
        hist_s, bins_s = np.histogram(a=state.telemetry_data["Speed"], bins=200)
        total_speed = len(state.telemetry_data["Speed"])
        hist_s_percent = (hist_s/total_speed) * 100
        bin_center_s = (bins_s[:-1] + bins_s[1:]) / 2
        dpg.add_bar_series(x = bin_center_s.astype(np.float64), y = hist_s_percent.astype(np.float64), parent="y_axis_hist_speed", label=f"{state.driver} Speed", tag="hist_line_speed", weight=0.8)
        dpg.set_axis_limits("x_axis_hist_speed", ymin=minSpeed, ymax=maxSpeed)
        dpg.set_axis_limits("y_axis_hist_speed", ymin=0, ymax=max(hist_s_percent))
        if Compare and state.telemetry_data2:
            hist_s2, bins_s2 = np.histogram(a=state.telemetry_data2["Speed"], bins=200)
            total_speed2 = len(state.telemetry_data2["Speed"])
            hist_s_percent2 = (hist_s2/total_speed2) * 100
            bin_center_s2 = (bins_s2[:-1] + bins_s2[1:]) / 2
            dpg.add_bar_series(x = bin_center_s2.astype(np.float64), y = hist_s_percent2.astype(np.float64), parent="y_axis_hist_speed", label=f"{state.driver2} Speed", tag="hist_line_speed2", weight=0.8)
            dpg.set_axis_limits("x_axis_hist_speed", ymin=minSpeed, ymax=maxSpeed)
            dpg.set_axis_limits("y_axis_hist_speed", ymin=0, ymax=max(hist_s_percent2))

        # RPM Histogram
        rpm_hist = dpg.add_plot(height=218, width=-1, label="RPM", tag="my_hist_rpm", parent="hist_container", no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, parent=rpm_hist, tag="x_axis_hist_rpm", no_highlight=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="%", parent=rpm_hist, tag="y_axis_hist_rpm", no_highlight=True)
        hist_r, bins_r = np.histogram(a=state.telemetry_data["RPM"], bins=200)
        total_rpm = len(state.telemetry_data["RPM"])
        hist_r_percent = (hist_r/total_rpm) * 100
        bin_center_r = (bins_r[:-1] + bins_r[1:]) / 2
        dpg.add_bar_series(x = bin_center_r.astype(np.float64), y = hist_r_percent.astype(np.float64), parent="y_axis_hist_rpm", label=f"{state.driver} RPM", tag="hist_line_rpm", weight=0.8)
        dpg.set_axis_limits("x_axis_hist_rpm", ymin=minRPM, ymax=maxRPM)
        dpg.set_axis_limits("y_axis_hist_rpm", ymin=0, ymax=max(hist_r_percent)+1)
        if Compare and state.telemetry_data2:
            hist_r2, bins_r2 = np.histogram(a=state.telemetry_data2["RPM"], bins=200)
            total_rpm2 = len(state.telemetry_data2["RPM"])
            hist_r_percent2 = (hist_r2/total_rpm2) * 100
            bin_center_r2 = (bins_r2[:-1] + bins_r2[1:]) / 2
            dpg.add_bar_series(x = bin_center_r2.astype(np.float64), y = hist_r_percent2.astype(np.float64), parent="y_axis_hist_rpm", label=f"{state.driver2} RPM", tag="hist_line_rpm2", weight=0.8)
            dpg.set_axis_limits("x_axis_hist_rpm", ymin=minRPM, ymax=maxRPM)
            dpg.set_axis_limits("y_axis_hist_rpm", ymin=0, ymax=max(hist_r_percent2)+1)

        # Gear Histogram
        gear_hist = dpg.add_plot(height=218, width=-1, label="Gear", tag="my_hist_gear", parent="hist_container", no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="Count", parent=gear_hist, tag="x_axis_hist_gear", no_highlight=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="%", parent=gear_hist, tag="y_axis_hist_gear", no_highlight=True)
        hist_g, bins_g = np.histogram(a=state.telemetry_data["Gear"], bins=8)
        total_gear = len(state.telemetry_data["Gear"])
        hist_g_percent = (hist_g/total_gear) * 100
        bin_center_g = (bins_g[:-1] + bins_g[1:]) / 2
        dpg.add_bar_series(x = bin_center_g.astype(np.float64), y = hist_g_percent.astype(np.float64), parent="y_axis_hist_gear", label=f"{state.driver} Gear", tag="hist_line_gear", weight=0.95)
        dpg.set_axis_limits("x_axis_hist_gear", ymin=minGear, ymax=maxGear)
        dpg.set_axis_limits("y_axis_hist_gear", ymin=0, ymax=max(hist_g_percent)+2)
        if Compare and state.telemetry_data2:
            hist_g2, bins_g2 = np.histogram(a=state.telemetry_data2["Gear"], bins=8)
            total_gear2 = len(state.telemetry_data2["Gear"])
            hist_g_percent2 = (hist_g2/total_gear2) * 100
            bin_center_g2 = (bins_g2[:-1] + bins_g2[1:]) / 2
            dpg.add_bar_series(x = bin_center_g2.astype(np.float64), y = hist_g_percent2.astype(np.float64), parent="y_axis_hist_gear", label=f"{state.driver2} Gear", tag="hist_line_gear2", weight=0.95)
            dpg.set_axis_limits("x_axis_hist_gear", ymin=minGear-0.5, ymax=maxGear+0.5)
            dpg.set_axis_limits("y_axis_hist_gear", ymin=0, ymax=max(hist_g_percent2)+2)
        dpg.set_axis_ticks("x_axis_hist_gear", (("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7), ("8", 8)))

        # Throttle Histogram
        throttle_hist = dpg.add_plot(height=218, width=-1, label="Throttle", tag="my_hist_throttle", parent="hist_container", no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="%", parent=throttle_hist, tag="x_axis_hist_throttle", no_highlight=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="%", parent=throttle_hist, tag="y_axis_hist_throttle", no_highlight=True)
        hist_t, bins_t = np.histogram(a=state.telemetry_data["Throttle"], bins=220)
        total_throttle = len(state.telemetry_data["Throttle"])
        hist_t_percent = (hist_t/total_throttle) * 100
        bin_center_t = (bins_t[:-1] + bins_t[1:]) / 2
        dpg.add_bar_series(x = bin_center_t.astype(np.float64), y = hist_t_percent.astype(np.float64), parent="y_axis_hist_throttle", label=f"{state.driver} Throttle", tag="hist_line_throttle", weight=0.8)
        dpg.set_axis_limits("x_axis_hist_throttle", ymin=minThrottle, ymax=maxThrottle)
        dpg.set_axis_limits("y_axis_hist_throttle", ymin=0, ymax=5)
        if Compare and state.telemetry_data2:
            hist_t2, bins_t2 = np.histogram(a=state.telemetry_data2["Throttle"], bins=200)
            total_throttle2 = len(state.telemetry_data2["Throttle"])
            hist_t_percent2 = (hist_t2/total_throttle2) * 100
            bin_center_t2 = (bins_t2[:-1] + bins_t2[1:]) / 2
            dpg.add_bar_series(x = bin_center_t2.astype(np.float64), y = hist_t_percent2.astype(np.float64), parent="y_axis_hist_throttle", label=f"{state.driver2} Throttle", tag="hist_line_throttle2", weight=0.8)
            dpg.set_axis_limits("x_axis_hist_throttle", ymin=minThrottle, ymax=maxThrottle)
            dpg.set_axis_limits("y_axis_hist_throttle", ymin=0, ymax=5)

    elif state.current_view == "stats":
        # Delete table if it exists
        if dpg.does_item_exist("stats_table"):
            dpg.delete_item("stats_table")

        if Compare:
            variables = (f"{state.driver} Speed", state.telemetry_data["Speed"]), (f"{state.driver2} Speed", state.telemetry_data2["Speed"]), (f"{state.driver} RPM", state.telemetry_data["RPM"]), (f"{state.driver2} RPM", state.telemetry_data2["RPM"]), (f"{state.driver} Gear", state.telemetry_data["Gear"]), (f"{state.driver2} Gear", state.telemetry_data2["Gear"]), (f"{state.driver} Throttle", state.telemetry_data["Throttle"]), (f"{state.driver2} Throttle", state.telemetry_data2["Throttle"]), (f"{state.driver} Brake", state.telemetry_data["Brake"]), (f"{state.driver2} Brake", state.telemetry_data2["Brake"]), (f"{state.driver} DRS", state.telemetry_data["DRS"]), (f"{state.driver2} DRS", state.telemetry_data2["DRS"])
        else:
            variables = (f"{state.driver} Speed", state.telemetry_data["Speed"]), (f"{state.driver} RPM", state.telemetry_data["RPM"]), (f"{state.driver} Gear", state.telemetry_data["Gear"]), (f"{state.driver} Throttle", state.telemetry_data["Throttle"]), (f"{state.driver} Brake", state.telemetry_data["Brake"]), (f"{state.driver} DRS", state.telemetry_data["DRS"])

        with dpg.table(parent="stats", tag="stats_table", header_row=True, resizable=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            # Columns
            dpg.add_table_column(label="Variable")
            dpg.add_table_column(label="Mean")
            dpg.add_table_column(label="Min")
            dpg.add_table_column(label="Max")
            dpg.add_table_column(label="Median")
            dpg.add_table_column(label="Standard deviation")

            # Rows
            for name, data in variables:
                data_np = np.array(data)
                with dpg.table_row():
                    dpg.add_text(name)
                    dpg.add_text(f"{np.mean(data_np):.2f}")
                    dpg.add_text(f"{np.min(data_np):.2f}")
                    dpg.add_text(f"{np.max(data_np):.2f}")
                    dpg.add_text(f"{np.median(data_np):.2f}")
                    dpg.add_text(f"{np.std(data_np):.2f}")

    elif state.current_view == "telemetry":
        real_height = ((dpg.get_item_height("plot_container_speed")-17) + (dpg.get_item_height("plot_container_rpm")-17) + (dpg.get_item_height("plot_container_gear")-17) + (dpg.get_item_height("plot_container_throttle")-17) + (dpg.get_item_height("plot_container_brake")-17) + (dpg.get_item_height("plot_container_drs")-17)) / 6 
        # Speed Graph
        plot_speed = dpg.add_plot(label="Speed", height=real_height, width=-1, tag="my_plot_speed", parent="plot_container_speed", crosshairs=True, zoom_mod=True, no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, parent=plot_speed, tag="x_axis_speed", no_highlight=True, no_tick_labels=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="(km/h)", parent=plot_speed, tag="y_axis_speed", no_highlight=True, tick_format="%.3g")
        dpg.add_line_series(x=state.telemetry_data["Distance"], y=state.telemetry_data["Speed"], parent="y_axis_speed", label=f"{state.driver} Speed", tag="speed_line")
        if Compare and state.telemetry_data2:
            state.driver2 = dpg.get_value("driver2_input")
            dpg.add_line_series(x=state.telemetry_data2["Distance"], y=state.telemetry_data2["Speed"], parent="y_axis_speed", label=f"{state.driver2} Speed", tag="speed_line2")
        dpg.set_axis_limits("y_axis_speed", ymin=minSpeed, ymax=maxSpeed)
         
        # RPM Graph
        plot_rpm = dpg.add_plot(label="RPM", height=real_height, width=-1, tag="my_plot_rpm", parent="plot_container_rpm", crosshairs=True, zoom_mod=True, no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, parent=plot_rpm, tag="x_axis_rpm", no_highlight=True, no_tick_labels=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="RPM", parent=plot_rpm, tag="y_axis_rpm", no_highlight=True)
        dpg.add_line_series(x=state.telemetry_data["Distance"], y=state.telemetry_data["RPM"], parent="y_axis_rpm", label=f"{state.driver} RPM", tag="rpm_line")
        if Compare and state.telemetry_data2:
            dpg.add_line_series(x=state.telemetry_data2["Distance"], y=state.telemetry_data2["RPM"], parent="y_axis_rpm", label=f"{state.driver2} RPM", tag="rpm_line2")
        dpg.set_axis_limits("y_axis_rpm", ymin=minRPM, ymax=maxRPM)
        dpg.set_axis_ticks("y_axis_rpm", (("7k", 7000), ("8k", 8000), ("9k", 9000), ("10k", 10000), ("11k", 11000), ("12k", 12000)))

        # Gear Graph
        plot_gear = dpg.add_plot(label="Gear", height=real_height, width=-1, tag="my_plot_gear", parent="plot_container_gear", crosshairs=True, zoom_mod=True, no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, parent=plot_gear, tag="x_axis_gear", no_highlight=True, no_tick_labels=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="Count", parent=plot_gear, tag="y_axis_gear", no_highlight=True, tick_format="%0.1f")
        dpg.add_line_series(x=state.telemetry_data["Distance"], y=state.telemetry_data["Gear"], parent="y_axis_gear", label=f"{state.driver} Gear", tag="gear_line")
        if Compare and state.telemetry_data2:
            dpg.add_line_series(x=state.telemetry_data2["Distance"], y=state.telemetry_data2["Gear"], parent="y_axis_gear", label=f"{state.driver2} Gear", tag="gear_line2")
        dpg.set_axis_limits("y_axis_gear", ymin=minGear, ymax=maxGear)

        # Throttle Graph
        plot_throttle = dpg.add_plot(label="Throttle", height=real_height, width=-1, tag="my_plot_throttle", parent="plot_container_throttle", crosshairs=True, zoom_mod=True, no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, parent=plot_throttle, tag="x_axis_throttle", no_highlight=True, no_tick_labels=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="%", parent=plot_throttle, tag="y_axis_throttle", no_highlight=True, tick_format="%.3g")
        dpg.add_line_series(x=state.telemetry_data["Distance"], y=state.telemetry_data["Throttle"], parent="y_axis_throttle", label=f"{state.driver} Throttle", tag="throttle_line")
        if Compare and state.telemetry_data2:
            dpg.add_line_series(x=state.telemetry_data2["Distance"], y=state.telemetry_data2["Throttle"], parent="y_axis_throttle", label=f"{state.driver2} Throttle", tag="throttle_line2")
        dpg.set_axis_limits("y_axis_throttle", ymin=minThrottle-2, ymax=maxThrottle+3)

        # Brake Graph
        plot_brake = dpg.add_plot(label="Brake", height=real_height, width=-1, tag="my_plot_brake", parent="plot_container_brake", crosshairs=True, zoom_mod=True, no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, parent=plot_brake, tag="x_axis_brake", no_highlight=True, no_tick_labels=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="on-off", parent=plot_brake, tag="y_axis_brake", no_highlight=True, tick_format="%.3g")
        dpg.add_line_series(x=state.telemetry_data["Distance"], y=state.telemetry_data["Brake"], parent="y_axis_brake", label=f"{state.driver} Brake", tag="brake_line")
        if Compare and state.telemetry_data2:
            dpg.add_line_series(x=state.telemetry_data2["Distance"], y=state.telemetry_data2["Brake"], parent="y_axis_brake", label=f"{state.driver2} Brake", tag="brake_line2")
        dpg.set_axis_limits("y_axis_brake", ymin=minBrake, ymax=maxBrake)

        # DRS Graph
        plot_drs = dpg.add_plot(label="DRS", height=real_height, width=-1, tag="my_plot_drs", parent="plot_container_drs", crosshairs=True, zoom_mod=True, no_frame=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, parent=plot_drs, tag="x_axis_drs", no_highlight=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="on-off", parent=plot_drs, tag="y_axis_drs", no_highlight=True, tick_format="%.3g")
        dpg.add_line_series(x=state.telemetry_data["Distance"], y=state.telemetry_data["DRS"], parent="y_axis_drs", label=f"{state.driver} DRS", tag="drs_line")
        if Compare and state.telemetry_data2:
            dpg.add_line_series(x=state.telemetry_data2["Distance"], y=state.telemetry_data2["DRS"], parent="y_axis_drs", label=f"{state.driver2} DRS", tag="drs_line2")
        dpg.set_axis_limits("y_axis_drs", ymin=-0.05, ymax=1.05)

    if Compare and state.telemetry_data2:
        dpg.set_value("result_text", f"Telemetry successfully loaded for {state.driver} - Lap: {state.lap_int if state.lap_int != 0 else "fastest"} and {state.driver2} - Lap: {state.lap_int2 if state.lap_int2 != 0 else "fastest"} {state.track} {year_int}")
    else:
        dpg.set_value("result_text", f"Telemetry successfully loaded for {state.driver} {state.track} {year_int} Lap: {state.lap_int if state.lap_int != 0 else "fastest"}")
    hex_to_rgb()

def update_car_position(user_data):
    if state.telemetry_data != {}:
        distance = state.telemetry_data["Distance"]
    
        plot_tags = ["my_plot_speed", "my_plot_rpm", "my_plot_gear", "my_plot_throttle", "my_plot_brake", "my_plot_drs"]
        is_hovered = any(dpg.is_item_hovered(tag)
            for tag in plot_tags
            if dpg.does_item_exist(tag))
        if not is_hovered:
            return
        try:
            mouse_pos = dpg.get_plot_mouse_pos()
            mouse_x = mouse_pos[0]
            idx = min(range(len(distance)), key=lambda i: abs(distance[i] - mouse_x))
            plot_x = state.telemetry_data["x"][idx]
            plot_y = state.telemetry_data["y"][idx]
            dpg.configure_item("track_point", x=[plot_x], y=[plot_y])
        except Exception:
            pass

def hex_to_rgb():
    state.driver = dpg.get_value("driver_input")
    state.driver2 = dpg.get_value("driver2_input")
    hex_enabled = dpg.get_value("hex")
    Compare = dpg.get_value("Compare")

    if not hex_enabled:
        bind_default_themes()
    else:
        try:
            state.hex_color = fastf1.plotting.get_driver_color(state.driver, state.session).lstrip('#')
            state.r = int(state.hex_color[0:2], 16)
            state.g = int(state.hex_color[2:4], 16)
            state.b = int(state.hex_color[4:6], 16)

            if dpg.does_item_exist("track_point_themeT") and dpg.does_item_exist("track_point"):
                    dpg.bind_item_theme("track_point", "track_point_theme")
            if dpg.does_item_exist("track_point_themeT"):
                dpg.delete_item("track_point_themeT")
            with dpg.theme(tag="track_point_themeT"):
                with dpg.theme_component(dpg.mvScatterSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, (state.r, state.g, state.b, 255), category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, (state.r, state.g, state.b, 255), category=dpg.mvThemeCat_Plots)

            if dpg.does_item_exist("speed_themeT"):
                dpg.delete_item("speed_themeT")
            with dpg.theme(tag="speed_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r, state.g, state.b, 200), category=dpg.mvThemeCat_Plots)
                with dpg.theme_component(dpg.mvBarSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (state.r, state.g, state.b, 200), category=dpg.mvThemeCat_Plots)

            if dpg.does_item_exist("rpm_themeT"):
                dpg.delete_item("rpm_themeT")
            with dpg.theme(tag="rpm_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r, state.g, state.b, 255), category=dpg.mvThemeCat_Plots)
                with dpg.theme_component(dpg.mvBarSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (state.r, state.g, state.b, 200), category=dpg.mvThemeCat_Plots)     
            if dpg.does_item_exist("gear_themeT"):
                dpg.delete_item("gear_themeT")                                  
            with dpg.theme(tag="gear_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r, state.g, state.b, 255), category=dpg.mvThemeCat_Plots)
                with dpg.theme_component(dpg.mvBarSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (state.r, state.g, state.b, 200), category=dpg.mvThemeCat_Plots)  

            if dpg.does_item_exist("throttle_themeT"):
                dpg.delete_item("throttle_themeT")                 
            with dpg.theme(tag="throttle_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r, state.g, state.b, 255), category=dpg.mvThemeCat_Plots)
                with dpg.theme_component(dpg.mvBarSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (state.r, state.g, state.b, 200), category=dpg.mvThemeCat_Plots)

            if dpg.does_item_exist("brake_themeT"):
                dpg.delete_item("brake_themeT")
            with dpg.theme(tag="brake_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r, state.g, state.b, 255), category=dpg.mvThemeCat_Plots)
            if dpg.does_item_exist("drs_themeT"):
                dpg.delete_item("drs_themeT")
            with dpg.theme(tag="drs_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r, state.g, state.b, 255), category=dpg.mvThemeCat_Plots)      

            if Compare:
                state.hex_color2 = fastf1.plotting.get_driver_color(state.driver2, state.session).lstrip('#')
                state.r2 = int(state.hex_color2[0:2], 16)
                state.g2 = int(state.hex_color2[2:4], 16)
                state.b2 = int(state.hex_color2[4:6], 16)

                if dpg.does_item_exist("speed_themeT2"):
                    dpg.delete_item("speed_themeT2")
                with dpg.theme(tag="speed_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r2, state.g2, state.b2, 255), category=dpg.mvThemeCat_Plots)
                    with dpg.theme_component(dpg.mvBarSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Fill, (state.r2, state.g2, state.b2, 200), category=dpg.mvThemeCat_Plots)

                if dpg.does_item_exist("rpm_themeT2"):
                    dpg.delete_item("rpm_themeT2")
                with dpg.theme(tag="rpm_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r2, state.g2, state.b2, 255), category=dpg.mvThemeCat_Plots)
                    with dpg.theme_component(dpg.mvBarSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Fill, (state.r2, state.g2, state.b2, 200), category=dpg.mvThemeCat_Plots)

                if dpg.does_item_exist("gear_themeT2"):
                    dpg.delete_item("gear_themeT2")
                with dpg.theme(tag="gear_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r2, state.g2, state.b2, 255), category=dpg.mvThemeCat_Plots)
                    with dpg.theme_component(dpg.mvBarSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Fill, (state.r2, state.g2, state.b2, 200), category=dpg.mvThemeCat_Plots)

                if dpg.does_item_exist("throttle_themeT2"):
                    dpg.delete_item("throttle_themeT2")
                with dpg.theme(tag="throttle_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r2, state.g2, state.b2, 255), category=dpg.mvThemeCat_Plots)
                    with dpg.theme_component(dpg.mvBarSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Fill, (state.r2, state.g2, state.b2, 200), category=dpg.mvThemeCat_Plots)
                        
                if dpg.does_item_exist("brake_themeT2"):
                    dpg.delete_item("brake_themeT2")
                with dpg.theme(tag="brake_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r2, state.g2, state.b2, 255), category=dpg.mvThemeCat_Plots)

                if dpg.does_item_exist("drs_themeT2"):
                    dpg.delete_item("drs_themeT2")
                with dpg.theme(tag="drs_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (state.r2, state.g2, state.b2, 255), category=dpg.mvThemeCat_Plots)
            bind_team_themes()
        except Exception as e:
            dpg.set_value("result_text", f"Team color error: {e}")

def bind_team_themes():
    if state.current_view == "telemetry":
        dpg.bind_item_theme("track_point", "track_point_themeT")
        dpg.bind_item_theme("speed_line", "speed_themeT")
        dpg.bind_item_theme("rpm_line", "rpm_themeT")
        dpg.bind_item_theme("gear_line", "gear_themeT")
        dpg.bind_item_theme("throttle_line", "throttle_themeT")
        dpg.bind_item_theme("brake_line", "brake_themeT")
        dpg.bind_item_theme("drs_line", "drs_themeT")
    elif state.current_view == "histogram":
        dpg.bind_item_theme("track_point", "track_point_themeT")
        dpg.bind_item_theme("hist_line_speed", "speed_themeT")
        dpg.bind_item_theme("hist_line_rpm", "rpm_themeT")
        dpg.bind_item_theme("hist_line_gear", "gear_themeT")
        dpg.bind_item_theme("hist_line_throttle", "throttle_themeT")

    if dpg.get_value("Compare"):
        if state.current_view == "telemetry":
            dpg.bind_item_theme("track_point", "track_point_themeT")
            if dpg.does_item_exist("speed_line2"):
                dpg.bind_item_theme("speed_line2", "speed_themeT2")

            if dpg.does_item_exist("rpm_line2"):
                dpg.bind_item_theme("rpm_line2", "rpm_themeT2")

            if dpg.does_item_exist("gear_line2"):
                dpg.bind_item_theme("gear_line2", "gear_themeT2")

            if dpg.does_item_exist("throttle_line2"):
                dpg.bind_item_theme("throttle_line2", "throttle_themeT2")

            if dpg.does_item_exist("brake_line2"):
                dpg.bind_item_theme("brake_line2", "brake_themeT2")

            if dpg.does_item_exist("drs_line2"):
                dpg.bind_item_theme("drs_line2", "drs_themeT2")

        elif state.current_view == "histogram":
            dpg.bind_item_theme("track_point", "track_point_themeT")
            if dpg.does_item_exist("hist_line_speed2"):
                dpg.bind_item_theme("hist_line_speed2", "speed_themeT2")
            if dpg.does_item_exist("hist_line_rpm2"):
                dpg.bind_item_theme("hist_line_rpm2", "rpm_themeT2")
            if dpg.does_item_exist("hist_line_gear2"):
                dpg.bind_item_theme("hist_line_gear2", "gear_themeT2")
            if dpg.does_item_exist("hist_line_throttle2"):
                dpg.bind_item_theme("hist_line_throttle2", "throttle_themeT2")

def bind_default_themes():
    if state.current_view == "telemetry":
        dpg.bind_item_theme("track_point", "track_point_theme")
        dpg.bind_item_theme("speed_line", "speed_theme")
        dpg.bind_item_theme("rpm_line", "rpm_theme")
        dpg.bind_item_theme("gear_line", "gear_theme")
        dpg.bind_item_theme("throttle_line", "throttle_theme")
        dpg.bind_item_theme("brake_line", "brake_theme")
        dpg.bind_item_theme("drs_line", "drs_theme")
    elif state.current_view == "histogram":
        dpg.bind_item_theme("track_point", "track_point_theme")
        dpg.bind_item_theme("hist_line_speed", "speed_theme")
        dpg.bind_item_theme("hist_line_rpm", "rpm_theme")
        dpg.bind_item_theme("hist_line_gear", "gear_theme")
        dpg.bind_item_theme("hist_line_throttle", "throttle_theme")

    if dpg.get_value("Compare"):
        if state.current_view == "telemetry":
            dpg.bind_item_theme("speed_line2", "speed_theme2")
            dpg.bind_item_theme("rpm_line2", "rpm_theme2")
            dpg.bind_item_theme("gear_line2", "gear_theme2")
            dpg.bind_item_theme("throttle_line2", "throttle_theme2")
            dpg.bind_item_theme("brake_line2", "brake_theme2")
            dpg.bind_item_theme("drs_line2", "drs_theme2")
        elif state.current_view == "histogram":
            dpg.bind_item_theme("hist_line_speed2", "speed_theme2")
            dpg.bind_item_theme("hist_line_rpm2", "rpm_theme2")
            dpg.bind_item_theme("hist_line_gear2", "gear_theme2")
            dpg.bind_item_theme("hist_line_throttle2", "throttle_theme2")

def load_telemetry(user_data):
    load_session()
    load_data(user_data)
    update_plots()
if __name__ == "__main__":
    create_interface()